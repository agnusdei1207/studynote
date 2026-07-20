---
title: "AB Testing Causal Inference Experiment"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 680
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: A/B 테스팅은 Rubin Causal Model(RCM)과 Potential Outcomes(Y(1), Y(0)) 프레임워크 위에서 "처치(Treatment)의 인과 효과 τ = E[Y(1)−Y(0)]"를 무작위 배정(Random Assignment)을 통해 편향(Bias) 없이 추정하는 통계적 실험 설계이며, SUTVA, Ignorability, Positivity 가정이 성립해야 인과 추론이 가능하다.
> 2. **가치**: CUPED 분산 감소 기법 적용 시 분산 30~50% 축소로 동일 검정력에서 샘플 수 ~50% 절감 가능하며, p-hacking·peeking 방지를 위한 sequential test(Always-Valid Inference, mSPRT) 적용 시 의사결정 속도 2~3배 향상, False Discovery Rate ≤ 0.05 통제 시 잘못된 출시 40% 감소 효과를 기대할 수 있다.
> 3. **판단 포인트**: 사용자 단위 vs 세션 단위 vs 클러스터 단위의 **Randomization Unit** 선택, 검정력(1−β=80%)·유의수준(α=0.05)·최소탐지효과(MDE) 간 트레이드오프, SRM(Sample Ratio Mismatch) 탐지 임계치(χ² p<0.001), Bonferroni vs BH-FDR 다중검정 보정 방식, 네트워크 간섭(Interference) 시 Cluster-Randomized 설계 도입 여부가 핵심 설계 변수이다.

---

## Ⅰ. 개요 및 필요성

전통적인 의사결정은 직관, HiPPO(Highest-Paid Person's Opinion), 또는 단순 전·후 비교에 의존했다. 그러나 사용자 행동 데이터가 Big Data로 축적되고, ML 기반 추천·검색·광고 최적화가 고도화되면서 **"어떤 변경이 실제 KPI(전환율, ARPU, Retention)에 인과적 영향을 미쳤는가"**를 정량적으로 판별해야 할 필요성이 대두되었다. 이때 단순한 A/B 평균 비교는 (1) **Selection Bias**(처리군/대조군 분포 차이), (2) **Confounding**(체크아웃 버튼 개선 후 매출 상승이 계절 효과인지 변경 효과인지 구분 불가), (3) **Simpson's Paradox**(전체 평균과 세그먼트별 평균의 부호 반대) 등으로 인해 오해를 낳는다. 따라서 **Pearl의 DAG(Directed Acyclic Graph) + Rubin의 Potential Outcomes** 두 축을 결합한 인과 추론 기반 A/B 실험 설계가 데이터 주도 의사결정(Decision Intelligence)의 핵심 인프라로 자리 잡았다. Google·Microsoft·Meta·Netflix·Amazon·쿠팡·토스·당근마켓 등 모든 대형 플랫폼은 자체 실험 플랫폼(예: Google Optimize 360 -> 내부 시스템, Microsoft ExP, Meta PlanOut, Netflix A/B Platform)을 운영하며, 일 평균 수천~수만 건의 실험을 병행한다.

```text
[ A/B Testing Causal Inference 전체 아키텍처 ]

  +----------------------------------------------------------------------+
  | ① 실험 설계 (Experimental Design)                                   |
  |   - 가설 설정 (H1: 신규 UI -> CVR +2%p)                              |
  |   - MDE/α/power -> 표본 크기 산출 (Power Analysis)                  |
  |   - Randomization Unit 결정 (User / Session / Cluster)             |
  |   - Truncation 기간, Stratification(국가/플랫폼) 결정               |
  +----------------+-----------------------------------------------------+
                   v
  +----------------------------------------------------------------------+
  | ② 트래픽 분배 (Traffic Allocation & Assignment)                     |
  |   - Hash(uid + salt + experiment_id) % 100 -> bucket                |
  |   - Feature Flag Service(LaunchDarkly/Statsig) or 내부 SDK         |
  |   - Layer/Mutually Exclusive 처리, Holdout(5~10%) 보전              |
  +----------------+-----------------------------------------------------+
                   v
  +----------------------------------------------------------------------+
  | ③ 로그 수집 (Telemetry Pipeline)                                    |
  |   - Exposure Event(사용자가 variant 노출 시)  <- SRM 검증 핵심      |
  |   - KPI Event(purchase, click, view)                                 |
  |   - Kafka -> Flink/Spark Streaming -> S3/BigQuery/Snowflake         |
  +----------------+-----------------------------------------------------+
                   v
  +----------------------------------------------------------------------+
  | ④ 통계 분석 & 인과 추론 (Causal Analysis)                          |
  |   - SRM 검정 (Chi-square, p<0.001)                                  |
  |   - A/A Sanity Check                                                  |
  |   - Point Estimate + 95% CI (t-test / Welch's / Bootstrap)          |
  |   - CUPED 분산 감소, Stratified Estimator                           |
  |   - Sequential Test (mSPRT / Always-Valid CI)                       |
  |   - Heterogeneous Treatment Effect (Causal Forest, BART)            |
  |   - FDR 보정 (BH procedure)                                          |
  +----------------+-----------------------------------------------------+
                   v
  +----------------------------------------------------------------------+
  | ⑤ 의사결정 & 학습 (Decision & Learning)                             |
  |   - 승자(Winner) Variant 전량 배포 (Ramp-up)                        |
  |   - 장기 효과(90일 Retention) Holdout 관찰                          |
  |   - 실험 카탈로그·지식 그래프 적재 -> 다음 가설 생성                  |
  +----------------------------------------------------------------------+
```

과거 가설검정 중심의 빈도주의(Frequentist) p-value 의존 접근은 **p-hacking**(유의할 때까지 반복 peeking), **Multiple Testing**(50개 지표 동시 검정 시 2.5개 Type I 오류), **Novelty/Primacy Effect**(신규 UI 초반 일시적 과대 효과)로 인해 오해의 소지가 컸다. 2020년 이후 업계는 (1) **사전 등록(Pre-registration)된 가설 + 단일 Primary Metric**, (2) **Sequential Testing**으로 인한 α-spending 통제, (3) **CUPED**·**Stratified RCT**로 분산 축소, (4) **Causal Forest** 등 머신러닝 인과 모델로 사용자별 HTE(Heterogeneous Treatment Effect) 추정으로 패러다임이 이동했다.

- **📢 섹션 요약 비유**: A/B 테스트는 "두 약을 똑같은 병에 든 환자 1,000명씩 나눠 투여하고 한 달 후 혈압을 비교하는 Randomized Controlled Trial"과 같다. 핵심은 **"우연이 아닌 약의 효과"**를 분리해내는 무작위 배정이며, 환자(사용자) 특성이 비슷하도록 층화(Stratification)하고, 사전에 필요한 환자 수(Power Analysis)를 계산하며, 단 1회만 판단(Pre-registration)해야 거짓 양성(p-hacking)을 막을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 인과 추론 수학적 토대

**Potential Outcomes Framework (Neyman-Rubin Causal Model)**

| 기호 | 의미 |
| :--- | :--- |
| $Y_i(1)$ | 사용자 $i$가 Treatment(T=1)를 받았을 때의 잠재 결과(Counterfactual) |
| $Y_i(0)$ | 사용자 $i$가 Control(T=0)을 받았을 때의 잠재 결과 |
| $T_i \in \{0,1\}$ | 실제 배정된 처치 (0=Control, 1=Treatment) |
| $X_i$ | 공변량(Covariate) 벡터 (사전 행동, 디바이스, 지역 등) |
| $Y_i^{obs} = T_i Y_i(1) + (1-T_i)Y_i(0)$ | 관측된 결과 (Fundamental Problem of Causal Inference) |
| $\tau = E[Y(1)-Y(0)]$ | **Average Treatment Effect (ATE)** — 인과 효과 |
| $\tau_{SATE} = \frac{1}{N}\sum Y_i$ | Sample ATE (Finite-sample) |

**필요 가정 (Identifiability Conditions)**
1. **SUTVA (Stable Unit Treatment Value Assumption)**: 한 사용자의 처치가 다른 사용자의 결과에 영향을 주지 않음(Non-Interference) + 처치 형태가 일관(Stable). 네트워크 효과가 존재하면 Violation -> Cluster-Randomized 또는 Switchback Design 사용.
2. **Ignorability / Unconfoundedness**: $(Y(1),Y(0)) \perp T \mid X$ — 공변량을 조건부로 하면 배정이 효과와 독립.
3. **Positivity / Overlap**: $0 < P(T=1 \mid X=x) < 1$ for all $x$ — 모든 strata에 처치/대조군 존재.

### 2. 표본 크기 산출 (Power Analysis)

$$
n_{\text{per arm}} = \frac{(z_{1-\alpha/2} + z_{1-\beta})^2 \cdot 2\sigma^2}{\Delta^2}
$$

- $z_{1-\alpha/2}=1.96$ ($\alpha=0.05$), $z_{1-\beta}=0.84$ ($\text{power}=80\%$)
- $\Delta$: MDE (Minimum Detectable Effect), 예: CVR 3.0% -> 3.5%, 즉 $\Delta=0.005$
- $\sigma^2$: KPI 분산 (CVR의 경우 $p(1-p)$)

예) CVR baseline 5%, MDE +0.5%p, 양측 검정, power 80% -> 약 **30,000/arm = 60,000** 사용자 필요. CUPED 적용 시 효과적 분산 $\sigma^2(1-\rho^2)$로 감소($\rho$=사전·사후 상관, 통상 0.3~0.6).

### 3. Randomization Unit (배정 단위)

| 단위 | 장점 | 단점 | 사용 사례 |
| :--- | :--- | :--- | :--- |
| **User-level (uid)** | SUTVA 만족 용이, 분산 작음 | 신규 가입자 부족 시 시간 소요 | UI 변경, 추천 알고리즘 |
| **Session-level** | 빠른 데이터 누적 | 동일 사용자가 두 variant 경험 -> Carry-over | 검색 결과 순서 |
| **Page-view** | 노출 단위 | 매우 noisy, SRM 빈번 | 광고 배치 |
| **Cluster (geo/shard)** | Network Interference 통제 | 분산 큼, ICC 고려 필요 | Push 알림, 가격 변경 |
| **Switchback (시간)** | Network 효과 모델링 | Time-of-Day 효과 confound | 시장가(Marketplace) 가격 |

배정 함수: `bucket = crc32(experiment_id + ":" + user_id) % 10000 / 10000.0` 후 `[0,0.5)=Control, [0.5,1.0)=Treatment` 등의 결정적 해시(Deterministic Hash)로 재현성·멱등성 보장.

### 4. 시스템 아키텍처

```text
[ A/B Testing Platform 내부 구조 — Layered Architecture ]

  +---------------------------------------------------------------------+
  |   Experimentation UI (Web Console)                                  |
  |   - 가설 카드 / Metric Catalog / Layer/Conflict Validator           |
  |   - Pre-registration of Primary KPI & α-spending function          |
  +------------------------+--------------------------------------------+
                           | gRPC / REST
  +------------------------v--------------------------------------------+
  |   Configuration & Assignment Service                                |
  |   +--------------+  +--------------+  +------------------------+  |
  |   | Experiment DB|  | Feature Flag |  | Assignment Hash Engine |  |
  |   | (MySQL/PG)   |  | Cache(Redis) |  | Murmur3(uid+salt)      |  |
  |   +--------------+  +--------------+  +------------------------+  |
  |   - Layered allocation (Mutually Exclusive Experiments)            |
  |   - Sticky bucketing, Ramp-up, Kill-switch                          |
  +------------------------+--------------------------------------------+
                           | SDK (iOS/Android/Web/Server)
  +------------------------v--------------------------------------------+
  |   Client/Server SDK                                                  |
  |   - getVariant('exp_2024_rec_v3') -> 'control' | 'treatment_A'      |
  |   - Fire 'exposure' event with timestamp, uid, exp_id, variant     |
  +------------------------+--------------------------------------------+
                           |
  +------------------------v--------------------------------------------+
  |   Event Ingestion (Kafka / Kinesis / PubSub)                        |
  |   - exposure, click, purchase, churn, latency, error                 |
  |   - Exactly-Once Semantics via dedup key (uid+exp_id+ts)           |
  +------------------------+--------------------------------------------+
                           |
  +------------------------v--------------------------------------------+
  |   Streaming ETL (Flink / Spark Structured Streaming)                |
  |   - De-duplication, late-arrival handling (event_time + 3d)        |
  |   - Out-of-order correction (Watermark)                             |
  +------------------------+--------------------------------------------+
                           |
  +------------------------v--------------------------------------------+
  |   Warehouse (BigQuery / Snowflake / Redshift / Iceberg on S3)       |
  |   - fact_exposure, fact_metric, dim_user_strata                      |
  +------------------------+--------------------------------------------+
                           |
  +------------------------v--------------------------------------------+
  |   Causal Analytics Engine (Python / R / Spark)                      |
  |   - SRM/AA checks -> ATE, CUPED, Sequential, HTE, FDR                |
  |   - Jupyter/Statsig/Eppo/Databricks Notebooks                       |
  +---------------------------------------------------------------------+
```

### 5. 핵심 구성 요소 역할

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Assignment Service** | 사용자별 variant 결정 | Murmur3/SHA-256 Hash 기반 결정적 버킷팅, Layer(Mutually Exclusive), Sticky(세션/쿠키) 보장, Redis 캐시로 100k QPS 처리 |
| **Feature Flag SDK** | 클라이언트 측 분기 처리 | LaunchDarkly, Statsig, Unleash, Split.io; Server-Side Evaluation, Bootstrap from CDN, Offline fallback |
| **Exposure Logger** | 노출 시점 기록 (≠ Click) | `event_time`, `uid`, `exp_id`, `variant` 4-tuple -> SRM 및 ITT( Intention-to-Treat) 분석의 기준점 |
| **Metric Store** | KPI 사전 정의·카탈로그화 | Conversion Rate, ARPPU, DAU/MAU, n-day Retention, p99 Latency; 비율/평균/분위/비율비(Metric Ratio) 구분 |
| **Statistics Engine** | 인과 효과 추정 | t-test, Welch's t, Bootstrap BCa, Bayesian Beta-Binomial, mSPRT(α-spending=0.05), CUPED 공변량 보정 |
| **Decision Service** | 출시/중단/연장 자동화 | Pre-registered rule (e.g., uplift>0 & 95%CI_lo>−0.1%p & SRM OK & ≥7d) -> CI/CD 연동으로 Ramp-up 트리거 |

### 6. Sequential Testing (Peeking 문제 해결)

빈도주의 t-test를 매일 보면 Type I 오류가 1−(1−0.05)^k ≈ 1−0.95^k 로 누적. **Always-Valid Confidence Sequence** (Howard et al., 2021)