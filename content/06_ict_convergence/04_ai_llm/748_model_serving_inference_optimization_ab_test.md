---
title: "Model Serving Inference Optimization AB Test"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 748
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Triton/vLLM/TGI 기반 추론 서빙 환경에서 양자화(INT8/INT4/FP8), Continuous Batching, PagedAttention(KV-Cache), Speculative Decoding, FlashAttention 등 추론 최적화 기법을 **Production 트래픽의 일정 비율(예: 5~50%)로 분기 라우팅**하여 A/B 테스트를 수행, **latency(p50/p95/p99, TTFT, TPOT)·throughput(tokens/sec)·GPU SM utilization·TCO($/1M tokens)** 와 **품질 지표(Exact Match, ROUGE, LLM-as-Judge, Human Preference)** 간의 trade-off를 통계적으로 검증하는 MLOps 실험 프레임워크.
> 2. **가치**: 오프라인 벤치마크(Static Dataset)로 검증된 최적화 기법이라도 실제 사용자 쿼리 분포(Query Distribution Shift)와 긴 컨텍스트, 멀티턴 세션에서 품질 퇴화(Quality Degradation)가 발생 가능. A/B 테스트는 **Golden Set 대비 5~15% 정확도 손실이 발생할 수 있는 위험**을 사전에 탐지하고, GPU당 **30~70%의 TCO 절감** 또는 **2~4배 처리량 향상** 같은 최적화 효과를 정량적으로 입증하여 인프라 의사결정의 정당성(Auditability)을 확보.
> 3. **판단 포인트**: ① 트래픽 분배 단위(per-request vs per-session sticky) - LLM의 KV-Cache 재사용과 비용 직결, ② 통계 검정 방식(Frequentist Welch's t-test vs Bayesian Beta-Binomial vs Sequential Testing with mSPRT) - 조기 종료(Peeking) 오류 통제, ③ 검출력 확보를 위한 표본 크기(샘플 수, MDE 산정), ④ Cold Start 시 Warm-up 트래픽 분리, ⑤ 가드레일 지표(에러율, 5xx, OOM) 위반 시 자동 롤백 조건.

---

## Ⅰ. 개요 및 필요성

LLM 기반 서비스(ChatGPT 스타일의 멀티턴 대화, RAG 기반 Q&A, Code Completion, Embedding 서비스)의 운영 비용에서 **GPU Inference 비용이 60~80%**를 차지하며, 70B~405B급 모델의 경우 H100 1장당 시간당 수십만 원의 비용이 발생한다. 학습 주제 관점에서 이는 단순한 "성능 개선"이 아니라 **"비용 효율성, SLA 보장, 모델 거버넌스"**를 동시에 충족해야 하는 아키텍처 의사결정이다.

**전통적 접근의 한계**:
- **오프라인 벤치마크(Golden Set)**: 정적 데이터셋(예: MMLU, HumanEval, Ko-LLM-Leaderboard) 기준 정확도와 Throughput 측정. 그러나 실제 Production 트래픽은 **Long-tail 분포(긴 컨텍스트, 특수 도메인, 멀티모달)**, **다국어 혼용**, **Prompt Injection 시도** 등을 포함하므로 Offline 품질과 Online 품질의 괴리(Online-Offline Gap)가 평균 **7~20%** 발생.
- **Shadow Deployment(미러링)**: 신 모델이 추론만 수행하고 결과는 폐기. Throughput/Latency 측정은 가능하나, 사용자가 실제로 보지 않는 응답이므로 **End-to-End 품질 지표(클릭률, 재방문, Human Preference) 측정 불가**.
- **일괄 배포(Flip-the-Switch)**: 신 모델을 100% 트래픽으로 즉시 전환. 장애 발생 시 **완전 롤백 불가, 데이터 손실 위험**.

**A/B 테스트의 필요성**:
추론 최적화(예: FP16 -> FP8 양자화, Continuous Batching 도입, Speculative Decoding 적용)는 평균 latency는 1.5~3배 개선하지만, **수치 정밀도 저하로 환각(Hallucination)이 증가**하거나, **Speculative Decoding의 Draft Model이 잘못된 토큰을 생성할 경우 TTFT(Time To First Token)만 개선되고 전체 End-to-End latency가 오히려 증가**하는 등의 함정이 존재한다. 이를 정량적으로 측정·검증하지 않은 채 전량 배포하면 대규모 인시던트로 이어진다.

```text
        [Production Inference Optimization A/B Test - 트래픽 분배 개념도]

                        +---------------------------------------------+
                        |            User Request Stream              |
                        |   (Prompt + Session-ID + User-ID)           |
                        +---------------------+-----------------------+
                                              |
                                              v
                        +---------------------------------------------+
                        |      Traffic Splitter / Feature Flag        |
                        |   +-------------------------------------+   |
                        |   |  Hash(Session-ID) % 100            |   |
                        |   |  0~49  -> Variant A (Control)        |   |
                        |   |  50~99 -> Variant B (Treatment)      |   |
                        |   +-------------------------------------+   |
                        +------------+-------------------+------------+
                                     |                   |
                       +-------------v------+    +------v--------------+
                       |   Variant A        |    |   Variant B          |
                       |   (Control)        |    |   (Treatment)        |
                       | +----------------+ |    | +------------------+ |
                       | | FP16 / Static  | |    | | FP8 / Continuous | |
                       | | Batching       | |    | | Batching +       | |
                       | | Triton Serve   | |    | | PagedAttention   | |
                       | | Port 8001      | |    | | vLLM Port 8002   | |
                       | +--------+-------+ |    | +---------+--------+ |
                       +----------+---------+    +-----------+----------+
                                  |                          |
                                  v                          v
                       +----------------------------------------------+
                       |   Metrics Collection (OTLP -> Prometheus)     |
                       |  +-----------------------------------------+ |
                       |  |  Latency: TTFT, TPOT, p50/p95/p99       | |
                       |  |  Throughput: tokens/sec, RPS            | |
                       |  |  Cost: $/1M tokens, GPU-hours           | |
                       |  |  Quality: EM, ROUGE, LLM-Judge, CTR     | |
                       |  |  System: SM Util, OOM, 5xx              | |
                       |  +-----------------------------------------+ |
                       +----------------------+-----------------------+
                                              v
                       +---------------------------------------------+
                       |   Statistical Analysis & Decision Engine    |
                       |   (Welch's t-test / Bayesian / mSPRT)       |
                       |   -> 자동 승격(Promote) / 롤백(Rollback)     |
                       +---------------------------------------------+
```

**기존 운영 환경과의 비교**:
과거 CPU 기반의 전통 ML(XGBoost, LightGBM, LSTM) 서빙은 Triton/TorchServe의 Static Batching만으로 충분했으나, **LLM 시대의 Auto-Regressive Generation**은 토큰 단위(latency-arithmetic), KV-Cache 메모리 점유, Pre-fill vs Decode 단계 비대칭성으로 인해 최적화 공간이 기하급수적으로 확장되었다. 이에 따라 단일 Best Effort 최적화에서 **지속적 실험(Continuous Experimentation) 기반 A/B 테스트**가 표준 아키텍처로 자리 잡았다.

- **📢 섹션 요약 비유**: 자동차 회사가 새 엔진(FP8 양자화)을 출시할 때, 실험실의 트랙 테스트(Offline Benchmark)만 통과시키고 그대로 양산하는 것은 위험합니다. 실제 도로의 다양한 날씨·도로·운전자 습관(Production Traffic)에 일정 비율의 차량을 투입하여 주행 데이터(메트릭)와 고장률(에러)을 비교한 뒤 전량 적용하는 것과 같은 원리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

추론 최적화 A/B 테스트 시스템은 **4계층(4-Layer Architecture)**으로 구성된다. 각 계층은 명확한 책임 분리를 가지며, 학습 정리 작성 시 "결합도(Coupling) 낮음, 응집도(Cohesion) 높음" 원칙을 적용해야 한다.

```text
        [Inference Optimization A/B Test - 4-Layer Architecture]

  +----------------------------------------------------------------------+
  |  Layer 1: Traffic Routing & Experiment Configuration                |
  |  +--------------+  +--------------+  +--------------------------+  |
  |  | API Gateway  |  |  Service     |  | Experiment Config Store  |  |
  |  | (Kong/NGINX) |  |  Mesh        |  | (Statsig/GrowthBook/     |  |
  |  |  Header 기반 |  |  (Istio)     |  |  LaunchDarkly/내부 YAML) |  |
  |  |  라우팅      |  |  Weighted    |  |  - Variant 정의          |  |
  |  |              |  |  Routing     |  |  - 비율(Split) 설정      |  |
  |  +--------------+  +--------------+  |  - Sticky 세션 규칙      |  |
  |                                       +--------------------------+  |
  +----------------------------------------------------------------------+
                                  | Metadata (variant=B, exp_id=748)
                                  v
  +----------------------------------------------------------------------+
  |  Layer 2: Model Serving (Variant별 독립 서빙 인스턴스)              |
  |  +--------------------+         +------------------------------+    |
  |  | Variant A Cluster  |         | Variant B Cluster            |    |
  |  | (Control)          |         | (Treatment)                  |    |
  |  | - Triton Inference |         | - vLLM / TGI / TensorRT-LLM  |    |
  |  | - FP16 Weights     |         | - FP8 / INT4 (AWQ/GPTQ)      |    |
  |  | - Static Batching  |         | - Continuous Batching        |    |
  |  | - Standard KV-Cache|         | - PagedAttention (vLLM)      |    |
  |  | - GPU: A100 80GB×8 |         | - FlashAttention 3           |    |
  |  |                    |         | - GPU: H100 80GB×8           |    |
  |  +---------+----------+         +-----------+------------------+    |
  +------------+--------------------------------+----------------------+
               |                                |
               v                                v
  +----------------------------------------------------------------------+
  |  Layer 3: Observability & Telemetry                                 |
  |  +----------------+ +----------------+ +----------------------+     |
  |  | OpenTelemetry  | | Prometheus     | | Distributed Tracing  |     |
  |  | SDK (Auto-     | | (메트릭 저장)  | | (Tempo/Jaeger)       |     |
  |  |  instrument)   | |                | | - Trace ID 전파      |     |
  |  | - W3C TraceCxt | |