---
title: "LLMOps Large Language Model Operations"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 661
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLMOps는 LLM의 데이터 파이프라인·파인튜닝(LoRA/QLoRA, DPO/RLHF)·서빙(vLLM, TGI, Triton)·RAG(임베딩/벡터DB)·평가·모니터링·거버넌스를 통합 관리하는 End-to-End 운영 체계로, 전통 MLOps 대비 "비결정성·프롬프트 의존성·할루시네이션·토큰 비용"이라는 4대 변수를 추가로 다룬다.
> 2. **가치**: 체계적 LLMOps 적용 시 응답 p99 지연시간 30~60% 절감(연속배칭·KV-cache 최적화), 토큰 단위 비용 40~70% 절감(양자화·라우팅·캐싱), 할루시네이션율 50%v(RAG+Self-RAG+평가루프), 모델 교체·롤백·감사 시간 90%v(모델 레지스트리·프롬프트 버전관리·드리프트 탐지)를 달성할 수 있다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① 자체 파인튜닝 vs RAG vs 프롬프트엔지니어링(데이터·비용·유지보수성), ② 폐쇄형 API(OpenAI/Claude) vs 오픈소스 셀프호스팅(Llama 3, Mistral, Qwen) vs 하이브리드 라우팅, ③ 동기 응답 vs 스트리밍(SSE/WebSocket) vs 비동기 배치, ④ 단일 모델 vs MoE/Multi-model 라우팅이며, 데이터 거버넌스(개인정보·저작권)와 평가 자동화(LLM-as-Judge) 설계가成败를 가른다.

---

## Ⅰ. 개요 및 필요성

전통적인 MLOps는 **결정론적(deterministic) 모델**의 학습·배포·모니터링을 중심으로 발전해 왔으나, ChatGPT(2022.11) 이후 폭발적으로 확산된 LLM(대규모 언어 모델)은 운영 환경에서 다음과 같은 본질적 차이를 보인다.

| 차원 | 전통 ML(MLOps) | LLM(LM/LLMOps) |
| :--- | :--- | :--- |
| 출력 성격 | 결정론적(분류확률, 회귀값) | 비결정론적(자연어, temperature>0) |
| 학습 데이터 | 라벨된 정형/비정형 데이터 | 페타바이트 비정형 텍스트 + 휴먼 피드백 |
| 업데이트 방식 | 재학습/재배포(수 주) | 프롬프트/어댑터/RAG 인덱스 실시간 갱신 |
| 평가 지표 | Accuracy, F1, AUC | BLEU, ROUGE, BERTScore, LLM-as-Judge, Human Eval |
| 비용 구조 | GPU 학습 시간 | 추론 **토큰 단위** 과금 + 긴 컨텍스트 KV-cache |
| 위험 유형 | 데이터 드리프트, 성능 저하 | **할루시네이션**, 프롬프트 인젝션, 유독성, PII 누출 |

이로 인해 엔터프라이즈 환경에서는 LLM이 비즈니스에 직결되는 **신뢰성·안전성·비용·규제** 문제가 대두되며, 단순히 모델을 API로 호출하는 수준을 넘어 **데이터 수집·임베딩·프롬프트·파인튜닝·서빙·평가·모니터링·피드백 루프** 전 과정을 통합 관리하는 LLMOps 체계가 필수로 등장했다.

```text
+----------------------------------------------------------------------+
|                    LLMOps End-to-End Lifecycle                       |
|                                                                      |
|  +----------+   +----------+   +----------+   +----------+          |
|  | Data     |--->| Train /  |--->| Registry |--->| Deploy / |          |
|  | Pipeline |   | Fine-Tune|   |  (MLflow,|   | Serve    |          |
|  | (DVC,    |   | (LoRA,   |   |   W&B,   |   | (vLLM,   |          |
|  |  Airflow)|   |  DPO)    |   |   HF Hub)|   |  TGI,    |          |
|  +----------+   +----------+   |   etc.)  |   |  Triton) |          |
|       ^                         +----------+   +----+-----+          |
|       |                                              |                |
|       |                                              v                |
|  +----------+   +----------+   +----------+   +----------+          |
|  | Feedback |<---| Monitor  |<---| Evaluate |<---| RAG /    |          |
|  | Loop     |   | (Langfuse|   | (RAGAS,  |   | Inference|          |
|  | (Thumbs, |   |  Arize,  |   |  DeepEval|   | (Pinecone|          |
|  |  RLHF)   |   |  WhyLabs)|   |  LLM-J)  |   |  Weaviate|          |
|  +----------+   +----------+   +----------+   +----------+          |
+----------------------------------------------------------------------+
```

**기존 패러다임 대비 LLMOps가 필요한 핵심 이유 5가지**

1. **비결정성 관리**: 동일 입력에 temperature=0.7에서 매번 다른 출력이 발생 -> 재현성·회귀 테스트·감사 추적 필요
2. **컨텍스트 비용 폭증**: 컨텍스트가 2배로 늘어나도 KV-cache·attention 계산은 **O(n²)**로 증가 -> 비용 최적화 필수
3. **할루시네이션·안전성**: 의료·법률·금융 도메인에서 오답이 곧 사고로 직결 -> RAG·가드레일·사실 검증 파이프라인 요구
4. **빠른 모델 진화**: 주 단위로 새 모델(GPT-4o, Claude 3.5, Llama 3.3, Qwen2.5 등) 출시 -> 멀티모델 라우팅·A/B·블루/그린 배포 전략 필요
5. **규제·컴플라이언스**: EU AI Act, 한국 AI기본법(2026 시행), GDPR, SOC2, ISO 42001 대응을 위한 데이터 거버넌스·모델 카드·로그 보존 체계 필요

- **📢 섹션 요약 비유**: 전통 MLOps가 **공장 자동화 라인**이었다면, LLMOps는 **매 순간 다른 요리를 만드는 셰프의 주방**을 관리하는 일이라, 레시피(프롬프트)·재료(RAG 데이터)·화력(GPU 자원)·위생(가드레일)을 동시에 통제해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LLMOps의 7계층 아키텍처는 다음과 같이 구성된다.

```text
+-------------------------------------------------------------------------+
| L7  Governance & Security  | AI Act, PII Masking, RBAC, Audit Log      |
| L6  Observability          | Trace, Span, Token Cost, Drift, Toxicity  |
| L5  Evaluation             | RAGAS, Faithfulness, LLM-as-Judge, A/B    |
| L4  Application & Prompt   | LangChain, LlamaIndex, Prompt Registry    |
| L3  RAG & Retrieval        | Embedding, Vector DB, Re-ranker, Cache    |
| L2  Inference Serving      | vLLM, TGI, Triton, Router, Load Balancer  |
| L1  Foundation Model Layer | Base LLM, Adapter (LoRA), Quantized Model |
| L0  Data & Knowledge       | Raw Docs, ETL, Chunking, Embedding Index  |
+-------------------------------------------------------------------------+
```

### 계층별 핵심 컴포넌트

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Data Pipeline (L0)** | 원문 수집·정제·청킹·임베딩 | Airflow/Dagster로 코퍼스 ETL, Unstructured.io·pdfplumber로 문서 파싱, LangChain `RecursiveCharacterTextSplitter`(512~1024 토큰, 10~20% 오버랩) -> OpenAI text-embedding-3 / BGE-M3 / E5 / Cohere embed-v3 |
| **Foundation Model (L1)** | 베이스 모델 + 어댑터 | Llama-3.1-405B, Qwen2.5-72B, Mistral-Large, Solar, HyperClovaX; PEFT(LoRA r=16, α=32), QLoRA(4-bit NF4 + Double Quant), merged/separate 어댑터 아카이빙 |
| **Serving (L2)** | 저지연·고처리량 추론 | **vLLM** (PagedAttention, continuous batching으로 24× throughput), **TGI** (Rust 기반, HF tokenizers), **NVIDIA Triton** (dynamic batching + ensemble), **SGLang** (RadixAttention, 5× 속도), **TensorRT-LLM**, OpenLLM |
| **RAG & Retrieval (L3)** | 외부 지식 결합 | Query rewriting( HyDE, multi-query) -> Hybrid Search(BM25 + Dense) -> **Reciprocal Rank Fusion** -> Cross-Encoder Re-rank( bge-reranker-v2, Cohere Rerank 3) -> Top-k -> LLM context injection; **Self-RAG / CRAG**로 self-correction |
| **Orchestration (L4)** | 워크플로우·프롬프트 관리 | LangChain/LlamaIndex/LangGraph, **Prompt Registry**(LangSmith Prompt Hub, Helicone), semantic cache(GPT-Cache, GPTCache), function calling/Tool use, Agent(ReAct, Plan-and-Execute, BabyAGI, AutoGen, CrewAI) |
| **Evaluation (L5)** | 자동 정량 평가 | **RAGAS**(Context Precision/Recall, Faithfulness, Answer Relevancy), **DeepEval**(G-Eval, hallucination, toxicity), **Braintrust**, **Promptfoo**, **LM-Eval-Harness**, LLM-as-Judge(GPT-4 judge with CoT), human-in-the-loop Argilla |
| **Observability (L6)** | 트레이싱·메트릭·드리프트 | **Langfuse**(OSS, OpenTelemetry 호환), **Arize Phoenix**, **WhyLabs**, **Helicone**, **MLflow Tracing**; 메트릭: TTFT, TPOT, tokens/sec, cost/req, retrieval hit rate, faithfulness score, prompt/completion drift(PSI, KL-divergence) |
| **Governance (L7)** | 보안·규제·감사 | PII Detection(Presidio, Microsoft), Prompt Injection 방어( Rebuff, Lakera Guard, NeMo Guardrails, Guardrails AI), Jailbreak 분류기, Rate limiting, 데이터 마스킹, Model Card( 책임·한계 명시), AI Risk Management( NIST AI RMF, ISO/IEC 23894) |

### 핵심 알고리즘·파라미터 심화

**(1) RAG 파이프라인 정밀 제어**

```
Query -> Query Expansion(Multi-Query/HyDE)
     -> Hybrid Retrieval(α·BM25 + (1-α)·Dense)
     -> RRF(Rank k=60)
     -> Cross-Encoder Rerank(top-50->top-5)
     -> Context Window(4K~128K)
     -> LLM Generation
     -> Self-Check(Faithfulness NLI)
     -> Stream Response
```

- **청킹 전략**: 고정 사이즈(512t, 10% overlap) < 의미 기반 청킹(Embedding 시맨틱 경계 탐지) < Parent-Document Retriever(요약 인덱스 -> 원문 반환) < ColBERTv2(토큰 단위 late interaction)
- **임베딩 캐싱**: 동일 청크 중복 임베딩 방지(ttl 24h, LRU 10K), 80%v 비용 절감
- **리트리버 라우팅**: 도메인별 다중 벡터DB(법률 vs 일반), query classifier로 자동 라우팅

**(2) 파인튜닝 전략 비교**

| 기법 | 학습 파라미터 | GPU 메모리 | 사용 시점 |
| :--- | :--- | :--- | :--- |
| Full Fine-Tune | 100% (70B 기준 ~140GB) | A100 80GB × 8+ | 도메인 완전 전이, 거대 컴퓨 |
| **LoRA**(r=16) | 0.1~1% | ~16GB | 일반 도메인 적응, 가성비 우수 |
| **QLoRA** (4bit NF4) | 0.1~1% | ~6GB | 단일 A100/4090에서도 70B 학습 |
| **DPO/ORPO/KTO** | 어댑터만 | ~12GB | 선호도 정렬(RLHF 대체) |
| Prompt Tuning | 0.01% | ~2GB | Few-shot, 빠른 프로토타이핑 |

**(3) 추론 최적화 핵심 기법**

- **KV-Cache** + **PagedAttention**(vLLM): 토큰 단위 메모리 페이징, fragmentation 제거 -> 24× throughput
- **Continuous Batching**: 시퀀스 종료 시 즉시 신규 요청 삽입, GPU utilization 90%^
- **Speculative Decoding**: 작은 draft 모델이 5~10 토큰 생성 -> 큰 모델이 일괄 검증 -> 2~3× 속도
- **Quantization**: FP16 -> INT8(GPTQ, AWQ) -> INT4/FP4(NF4) -> 정확도 손실 <2%, 메모리 50~75%v
- **FlashAttention-2/3**: attention을 tiling + SRAM 재활용으로 O(n²) 메모리 -> O(n) 축소
- **MoE(Mixture of Experts)**: Mixtral 8×7B는 47B 파라미터 중 13B만 활성화 -> 추론 비용 대폭 절감

**(4) 평가 자동화 (LLM-as-Judge)**

```
Input: (question, context, answer, reference)
Judge LLM(GPT-4o, Claude 3.5)
  ↳ CoT: "Let me evaluate step by step..."
  ↳ 5-point Likert + Faithfulness + Relevance + Coherence
Output: {score, reason}
  ↳ Inter-Judge Agreement( Cohen's κ > 0.7 검증 필수)
```

- **G-Eval**: GPT-4에 평가 기준을 자동 생성하게 한 후 채점, 인간 상관관계 0.86+
- **PANEL/Prometheus**: 오픈소스 judge 모델로 비용 절감
- Pairwise A/B Testing: 동일 입력에 대해 두 모델 출력 비교, Bradley-Terry 모델로 Elo 산출

- **📢 섹션 요약 비유**: RAG는 **시험 공부할 때 교과서 펴놓고 답하는 것**, 파인튜닝은 **과외 선생님에게 반복 학습시키는 것**, 프롬프트엔지니어링은 **"제발 이렇게 답해줘"라는 부탁 쪽지**를 붙이는 것이다 — 세 가지를 동시에 쓰면 비서가 가장 똑똑해진다.

---

## Ⅲ. 비교 및 연결

### 1) MLOps vs LLMOps vs AIOps vs PromptOps

| 구분 | MLOps | LLMOps | AIOps | PromptOps |
| :--- | :--- | :--- | :--- | :--- |
| 대상 모델 |