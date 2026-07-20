---
title: "MLOps Model Serving AB Test"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 660
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MLOps 모델 서빙 A/B 테스트는 동일 트래픽을 다중 모델 버전(Control vs Treatment)에 라우팅하여 예측 성능(accuracy/AUC), 시스템 성능(p99 latency/throughput), 비즈니스 KPI(CTR/CVR) 등 다차원 메트릭을 통계적으로 유의미하게 비교 검증하는 **Production-grade Online Controlled Experiment(OCE)** 프레임워크이며, 모델 레지스트리(MLflow/SageMaker Registry), 추론 서버(Triton/TF Serving), 서비스 메시(Istio/Envoy), 피처 스토어(Feast/Tecton), 실험 추적(MLflow Tracking/W&B), 메트릭 수집(Prometheus/Evidently AI)이 통합된 End-to-End 파이프라인이다.
> 2. **가치**: 오프라인 검증(AUC 0.85 -> 0.87)의 사소한 개선이 실제 운영 환경에서 DAU 기준 +1.2% 매출 증대로 이어지는 사례(Netflix, Uber)처럼, 모델 성능을 **추론이 아닌 의사결정 결과로 직접 측정**하여 비즈니스 임팩트 기반 의사결정 정당화를 가능케 한다. 또한 SRM(Sample Ratio Mismatch) 감지 및 Novelty Effect(신규 효과) 보정을 통해 False Positive 의사결정 위험을 약 40-60% 절감한다.
> 3. **판단 포인트**: 트래픽 분할은 **Sticky Session(쿠키/세션 해시) vs Stateless Random 분기**의 선택이 1차 결정 포인트이며, 메트릭은 **Proximal(즉시 관측 가능) vs Distal(잔여 효과까지 수일~수주 소요)** 구분에 따라 실험 기간을 7일 vs 30일로 결정한다. 또한 네트워크 효과(양쪽 그룹 간 간섭)와 데이터 누수(학습-서빙 skew)를 사전에 통제하지 못하면 A/B 결과의 신뢰도가 붕괴하므로, Shadow -> Canary(5%) -> A/B(50:50) -> Champion 승격의 점진적 단계 설계가 필수적이다.

---

## Ⅰ. 개요 및 필요성

기계학습 모델은 오프라인 검증(offline evaluation) 단계에서 높은 성능을 보였던 모델이 실제 운영 환경(production)에서는 데이터 분포 변화, 시스템 지연, 사용자 행동 패턴 등 다양한 요인으로 인해 의도한 성능을 발휘하지 못하는 **"Sim2Real Gap"** 또는 **"Training-Serving Skew"** 현상이 빈번히 발생한다. 이러한 문제를 해결하기 위해 MLOps 환경에서는 **Online Controlled Experiment(OCE)**, 즉 **A/B 테스트**를 모델 서빙(model serving) 파이프라인의 핵심 검증 단계로 도입한다.

전통적인 모델 배포 파이프라인은 `학습(Training) -> 검증(Validation) -> 배포(Deployment)`의 일회성 흐름이었으나, 이는 **(1) 모델의 진정한 가치를 사전에 알 수 없고**, **(2) 운영 중 발생하는 데이터 드리프트(data drift)나 컨셉 드리프트(concept drift)에 대한 적응성을 검증할 수 없으며**, **(3) 비즈니스 KPI와의 인과관계를 정량화할 수 없는** 한계를 갖는다. 반면 A/B 테스트 기반 모델 서빙은 "동일한 사용자 분포를 두 개 이상의 모델에 동시 노출시키고, 그 결과를 통계적으로 비교"함으로써 **인과 추론(causal inference)에 기반한 모델 성능 비교**를 가능케 한다.

특히 추천 시스템, 검색 랭킹, 광고 CTR 예측, 사기 탐지(FDS), 리스크 스코어링과 같은 비즈니스 코어 모델에서는 모델의 0.1% 성능 향상이 수십억 원의 매출 차이로 직결되므로, A/B 테스트는 **"ML 모델의 의사결정 ROI를 검증하는 가장 신뢰할 수 있는 툴"** 이라 할 수 있다.

```text
[ MLOps A/B Test for Model Serving - High-Level Architecture ]

                          +---------------------------------+
                          |  Model Registry (MLflow /       |
                          |  SageMaker / Vertex AI)         |
                          |  - v1.2.0 (Champion, baseline)   |
                          |  - v1.3.0-rc1 (Challenger, new)  |
                          |  - v2.0.0-exp (Treatment)        |
                          +----------------+----------------+
                                           |
                                           | Pull image / weights
                                           v
+--------------------+        +------------------------+        +----------------------+
|  User / Client     | -----> |   Edge / API Gateway   | -----> |  Service Mesh /      |
|  (Web/Mobile/API)  |  HTTPS |   (Kong / Ambassador)  |  gRPC  |  Traffic Splitter    |
|                    |        |   + JWT, Rate Limit     |        |  (Istio / Envoy /    |
|  user_id cookie    |        +------------------------+        |   NGINX Plus)        |
+--------------------+                                             +----------+-----------+
                                                                         |
                                                  Traffic Split: 90% v1.2.0 | 10% v1.3.0-rc1
                                                                         |
                                          +------------------------------+------------------------------+
                                          |                                                             |
                                          v                                                             v
                              +-----------------------+                                  +-----------------------+
                              | Model Serving v1.2.0  |                                  | Model Serving v1.3.0  |
                              | (Control, Champion)   |                                  | (Treatment, Challenger)|
                              | Triton / TF Serving   |                                  | Triton / TorchServe    |
                              | GPU A100, 4 replicas  |                                  | GPU H100, 2 replicas   |
                              +-----------+-----------+                                  +-----------+-----------+
                                          |                                                             |
                                          |  prediction + log_id + user_id + variant_id                 |
                                          v                                                             v
                              +---------------------------------------------------------------------+
                              |       Observability / Metrics Pipeline                            |
                              |  Prometheus + Evidently AI + Grafana + Sentry (errors)            |
                              |  - latency p50/p95/p99, throughput                                |
                              |  - model metrics: prediction drift, score distribution           |
                              |  - business KPIs: CTR, CVR, AOV, retention, LTV                  |
                              +---------------------------------------------------------------------+
                                                              |
                                                              v
                              +---------------------------------------------------------------------+
                              |    Experiment Analytics & Statistical Engine                      |
                              |  - Frequentist: t-test, z-test for proportions, CUPED              |
                              |  - Bayesian: Beta-Binomial, Thompson Sampling                     |
                              |  - Sequential: mSPRT, Always Valid Inference                       |
                              |  - SRM (Sample Ratio Mismatch) detection                         |
                              +---------------------------------------------------------------------+
                                                              |
                                                              v
                              +---------------------------------------------------------------------+
                              |    Decision / Auto-promotion / Auto-rollback                     |
                              |  - p-value < 0.05 AND uplift > MDE AND no SRM -> Promote          |
                              |  - latency SLO breach OR error spike -> Auto rollback            |
                              +---------------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm)**

| 구분 | 기존 일회성 배포 (Pre-MLOps) | MLOps A/B Test 기반 서빙 |
|------|------------------------------|--------------------------|
| **검증 시점** | 배포 전 오프라인 검증만 수행 | 배포 후 운영 환경에서 실증 검증 |
| **성능 기준** | RMSE, Accuracy, AUC 등 모델 메트릭 | 모델 메트릭 + 시스템 메트릭(latency, throughput) + 비즈니스 KPI |
| **롤백** | 장애 발생 시 수동 롤백 | SLO 위반 시 자동 롤백(Argo Rollouts, Flagger) |
| **데이터** | 정적 학습-검증 분할 | 동적 트래픽 분할, Online Learning 가능 |
| **결정 주체** | 데이터 사이언티스트 단독 판단 | 데이터 사이언 + PM + SRE 합의, 통계적 유의성 기반 |
| **드리프트 대응** | 배포 후 사후 인지 | 데이터/모델 드리프트 실시간 감지(Evidently, WhyLabs) |

- **📢 섹션 요약 비유**: A/B 테스트는 마치 **"두 가지 요리법으로 같은 손님 집단에 동시에 시식회"**를 여는 것과 같습니다. 한 그룹에게는 기존 레시피(Control), 다른 그룹에게는 신메뉴(Treatment)를 내어 "어떤 요리가 실제 매출을 더 올리는지" 인과적으로 측정하는 것이지, 주방에서만 시식하는(offline eval) 것과는 차원이 다릅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MLOps A/B 테스트의 아키텍처는 크게 **6개의 레이어**로 구성된다: **(1) Experiment Design Layer**, **(2) Model Serving Layer**, **(3) Traffic Routing Layer**, **(4) Feature Store / Data Layer**, **(5) Observability / Metrics Layer**, **(6) Statistics & Decision Layer**.

**Step-by-Step 흐름:**

1. **Experiment Design**: 가설 설정(예: "v1.3 모델은 CTR을 +2% 개선할 것"), Primary KPI 선정, Minimum Detectable Effect(MDE) 산정, Sample size 계산, 실험 기간 산출.
2. **Model Packaging**: Champion/Control과 Challenger/Treatment 모델을 ONNX/TorchScript/SavedModel로 변환하여 모델 레지스트리에 등록.
3. **Traffic Routing**: 사용자/세션 단위 해시(예: `hash(user_id) % 100 < 10`) 또는 서비스 메시의 weighted routing(예: Istio VirtualService의 weight 90/10)을 통해 분기.
4. **Sticky Assignment**: 한 사용자가 실험 기간 동안 동일 그룹에 노출되도록 쿠키/세션 토큰/헤더 기반 sticky 분기.
5. **Online Inference**: 각 모델이 독립된 추론 엔드포인트에서 예측을 반환. Feature는 **Online Feature Store(Feast/Tecton)** 에서 동일하게 lookup하여 분기 일관성 보장.
6. **Metric Logging**: `(user_id, variant_id, model_version, prediction, actual_label, latency_ms)`를 Kafka/Kinesis로 스트리밍.
7. **Real-time Aggregation**: Flink/Spark Streaming으로 메트릭을 윈도우 단위(1분/1시간/1일) 집계.
8. **Statistical Analysis**: 누적 데이터에 대해 Z-test(전환율), t-test(연속값), CUPED(분산 감소), Bayesian(Beta-Binomial) 등을 적용.
9. **Decision & Action**: p-value < α(0.05), MDE 충족, SRM 미감지 시 승격. SLO 위반 시 자동 롤백.

```text
[ A/B Test Routing & Logging - Detailed Sequence ]

  Client             Gateway           Splitter            Model A            Model B          Metrics Bus         Stats Engine
    |                   |                 |                    |                  |                  |                   |
    | GET /predict      |                 |                    |                  |                  |                   |
    | (X-User-Id: u123) |                 |                    |                  |                  |                   |
    |------------------>|                 |                    |                  |                  |                   |
    |                   | Route to /ab    |                    |                  |                  |                   |
    |                   |---------------> |                    |                  |                  |                   |
    |                   |                 | hash(u123)%100=42  |                  |                  |                   |
    |                   |                 | bucket 42 -> v1.3  |                  |                  |                   |
    |                   |                 | (sticky session)   |                  |                  |                   |
    |                   |                 |------------------->| predict()        |                  |                   |
    |                   |                 |  (parallel call)   |----------------->| predict()        |                   |
    |                   |                 |                    |                  |                  |                   |
    |                   |                 |<-------------------| score=0.83       |                  |                   |
    |                   |                 |<--------------------------------------| score=0.79       |                   |
    |                   |                 |                    |                  |                  |                   |
    |                   |                 |  v1.3 selected (42% bucket)             |                  |                   |
    |                   |                 |  -> use score=0.79                                                          |
    |                   |                 |                                                                  |                   |
    |                   |<----------------|          publish: {u123, "B", v1.3, 0.79, 12ms}                              |                   |
    |                   |                 |-------------------------------------------------------------------------->|                   |
    |                   |                 |                                                                  | aggregate         |
    |                   |                 |                                                                  |------------------>|
    |                   |                 |                                                                  |                   | CUPED, z-test
    |                   |                 |                                                                  |                   | p=0.012 < 0.05
    |                   |                 |                                                                  |                   | uplift=+3.2%
    |<------------------|                 |            return {prediction: 0.79, variant: "B"}                    |                   |
    | 200 OK            |                 |                                                                  |                   |
    | {pred:0.79}       |                 |                                                                  |                   | (decision: PROMOTE v1.3)
    |                   |                 |                                                                  |                   |
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Experiment Config Manager** | 실험 메타데이터(가설, KPI, MDE, 변형 정의) 관리 | GrowthBook, Eppo, Statsig, 내부 `experiment.yaml` (variant 정의, hash salt, traffic ratio, start/end date) |
| **Model Registry** | 모델 버전 관리, Stage 전이(None->Staging->Production->Archived) | MLflow Model Registry, AWS SageMaker Model Registry, Vertex AI Model Registry, DVC |
| **Inference Server** | 모델 로딩, 전처리/후처리, 배치/batching, GPU 가속 | NVIDIA Triton Inference Server (HTTP/gRPC, dynamic batching, ensemble model), TensorFlow Serving, TorchServe, BentoML, Seldon Core, KServe |
| **Traffic Splitter** | 사용자/세션 단위 결정론적 분기, 가중치 라우팅 | Istio VirtualService (weight-based), Envoy HeaderRoute, Linkerd SMI, NGINX Plus `split_clients`, AWS App Mesh, Cloudflare Workers |
| **Feature Store** | Training-Serving 일관성 보장, Online/Offline 동일성 | Feast (online: Redis/DynamoDB), Tecton, AWS SageMaker Feature Store, Google Vertex Feature Store, Hopsworks |
| **Experiment Assignment** | 해시 함수 기반 sticky 분기, salt 노출 방지 | `assignment = hash(user_id + experiment_salt) % 10000`, FNV/MurmurHash, 1-way consistent hashing, Interleaving(랭킹 모델용) |
| **Metrics Pipeline** | 이벤트 수집, 스트리밍 집계, 데이터레이크 적재 | Kafka/Pulsar/Kinesis -> Flink/Spark Streaming -> ClickHouse/BigQuery/Parquet on S3, Snowflake |
| **Statistical Engine** | 유의성 검정, 분산 감소, 다중 비교 보정, SRM 감지 | Frequentist(z/t/χ²), Bayesian(PyMC, Beta-Binomial), Sequential(mSPRT, e-values), MSLR/False Discovery Rate |
| **Decision & Rollout** | 승격/유지/중단 결정, 자동 롤백, 점진적 트래픽 확장 | Argo Rollouts (Analysis Template), Flagger, Seldon's Outlier Detector, AWS SageMaker Deployment Guardrails, LaunchDarkly |
| **Observability** | 시스템/모델/비즈니스 메트릭 통합 대시보드, 알림 | Prometheus + Grafana, OpenTelemetry traces, Evidently AI (data/model drift), WhyLabs, Arize AI, Fiddler AI |

**핵심 알고리즘 및 파라미터 심화:**

**(1) Sample Size 산정 (Two-proportion z-test 기준):**
```
n = (Z_{α/2} + Z_β)² × [p1(1-p1) + p2(1-p2)] / (p2-p1)²

예) Baseline CTR p1=0.10, 기대 CTR p2=0.105 (MDE=5% relative),
    α=0.05, Power=0.80 -> n ≈ 30,200 per variant
    DAU 10만명, 50:50 split -> 약 12일 필요
```

**(2) CUPED (Controlled-experiment Using Pre-Experiment Data) - 분산 감소 기법:**
```
Y_CUPED = Y - θ × (X - E[X])
where θ = Cov(Y, X) / Var(X), X = pre-experiment metric (예: 최근 14일 사용자별 CTR)
이 방식으로 분산 30-50% 감소 -> 실험 기간 동일 MDE 대비 40-50% 단축
```

**(3) SRM (Sample Ratio M