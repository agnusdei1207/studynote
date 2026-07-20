---
title: "Data Science Master Summary"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 693
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 사이언스 실무자는 **비즈니스 문제 정의 -> 데이터 수집/레이크 적재 -> EDA/전처리 -> 피처 엔지니어링 -> 모델링(통계·ML·DL) -> 평가/검증 -> 배포/모니터링(MLOps)** 의 전 사이클에 대한 엔드투엔드 방법론과, **추론통계(가설검정·인과추론) ↔ 예측모델링(Generalization) ↔ 의사결정(강화학습·밴딧)** 의 3축 패러다임을 정확히 구분하여 시스템화하는 역량이다.
> 2. **가치**: 정형 데이터에서 LightGBM/XGBoost/CatBoost 기반 분류·회귀 모델은 **AUC 0.85+ 안정적 도달**, 시계열에서는 Prophet/N-BEATS/TFT로 MAPE 5~10% 수준 운영, LLM/RAG 기반 비정형 분석까지 포함 시 **고객 VOC 처리시간 80%v, 마케팅 ROI 3~5배, 설비 예지보전 다운타임 30~50%v**의 정량적 가치를 창출한다.
> 3. **판단 포인트**: ①**통계적 유의성 vs 예측 성능** (p-value vs AUC의 분리 운용), ②**상관관계 vs 인과관계** (DAG·IV·PSM·DiD·RDD 도구 선택), ③**설명가능성 vs 정확도** (SHAP/LIME vs XGBoost/딥러닝 트레이드오프), ④**편향-분산 트레이드오프**, ⑤**개인정보보호(가명·익명·차등프라이버시) vs 데이터 활용**, ⑥**온라인(Online) vs 배치(Batch) 학습** — 이 6개 의사결정 축이 학습 정리의 핵심 분기점이다.

---

## Ⅰ. 개요 및 필요성

데이터 사이언스는 단순한 "데이터 분석"이 아니라, **데이터로부터 통찰을 추출하고 의사결정을 자동화하며, 이를 산업 현장에 배포·운영·갱신하는 전 과정을 다루는 융합 학문**이다. 4차 산업혁명·AI 기본법(2025. 1. 시행)·EU AI Act 등 규제 환경의 변화, 그리고 생성형 AI의 보편화로 인해 데이터 사이언스의 정의역(Domain)이 통계학·컴퓨터과학·도메인 지식·윤리·법률로 확장되었다.

기존 BI(Business Intelligence) 패러다임은 **"과거의 사실 확인"** (Descriptive Analytics)에 머물렀다면, 현대 데이터 사이언스는 **"무엇이 일어날 것인가"**(Predictive), **"왜 일어났는가"**(Diagnostic/Causal), **"무엇을 해야 하는가"**(Prescriptive)로 진화했다. 그러나 실무에서는 여전히 **CRISP-DM(1996, SPSS)**, **KDD(1996, Fayyad)**, **Microsoft TDSP(2017)**, **Google MLOps Levels(2021)** 등 성숙한 방법론 프레임워크를 기반으로 단계별 산출물을 정의해야 한다.

```text
[데이터 사이언스 엔드투엔드 파이프라인 아키텍처]

   +-----------------------------------------------------------------+
   |              Business Understanding (문제 정의)                  |
   |   KPI 정의: Precision@K? Revenue Lift? Churn Rate? DAU?          |
   +-----------------------------+-----------------------------------+
                                 v
   +-----------------------------------------------------------------+
   |              Data Acquisition & Data Lake 적재                  |
   |   Source --► Kafka/Airbyte --► Bronze(RAW) --► Silver(정제)      |
   |            --► Gold(Feature Mart) on Delta Lake/Iceberg          |
   |   [Lakehouse: S3+Delta, ADLS Gen2+Iceberg, BigLake, MinIO]      |
   +-----------------------------+-----------------------------------+
                                 v
   +-----------------------------------------------------------------+
   |            EDA + Data Preprocessing (전처리 80% 비중)            |
   |   결측치(MCAR/MAR/MNAR) | 이상치(IQR, Isolation Forest)         |
   |   인코딩(One-Hot/Target/Frequency) | 스케일링(Standard/Robust)  |
   |   클래스 불균형(SMOTE, ADASYN, class_weight)                    |
   +-----------------------------+-----------------------------------+
                                 v
   +-----------------------------------------------------------------+
   |        Feature Engineering & Feature Store (피처 저장)          |
   |   Feature Selection: Filter/Wrapper/Embedded (L1, Boruta)        |
   |   Feature Extraction: PCA, LDA, t-SNE, UMAP, AutoEncoder        |
   |   Feature Store: Feast, Tecton, Hopsworks, DynamoDB+Redis       |
   +-----------------------------+-----------------------------------+
                                 v
   +-----------------------------------------------------------------+
   |              Modeling (예측 / 인과 / 생성)                      |
   |   Statistical -► Linear/Logistic/Ridge/Lasso/GLM/Bayesian        |
   |   ML Tree -----► RandomForest / XGBoost / LightGBM / CatBoost   |
   |   DL ----------► MLP / CNN / RNN-LSTM / Transformer / LLM      |
   |   Causal ------► IV / PSM / DiD / RDD / Double-ML / CausalForest|
   |   TimeSeries --► ARIMA / Prophet / N-BEATS / TFT / DeepAR      |
   +-----------------------------+-----------------------------------+
                                 v
   +-----------------------------------------------------------------+
   |       Evaluation & Validation (성능 / 강건성 / 공정성)            |
   |   Hold-out / K-Fold / TimeSeries Split / Group K-Fold / LOO     |
   |   Metrics: RMSE/MAE/R², F1/AUC/AP, NDCG/MRR, Calibration(ECE)   |
   |   Fairness: Demographic Parity, Equalized Odds                  |
   +-----------------------------+-----------------------------------+
                                 v
   +-----------------------------------------------------------------+
   |      Deployment & MLOps (배포 / 모니터링 / 재학습)              |
   |   Shadow -► Canary -► Blue-Green -► A/B -► Full Rollout         |
   |   Monitor: Data Drift(KS, PSI), Concept Drift(ADWIN, Page-Hink) |
   |   Tooling: MLflow, Kubeflow, TFX, Airflow, BentoML, KServe     |
   +-----------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 데이터 사이언스 엔드투엔드 파이프라인은 **"병원 진료 시스템"**과 같다. 접수(데이터 수집) -> 문진·검진(EDA/전처리) -> 진단(피처/모델) -> 처방(예측) -> 수술(배포) -> 경과관찰(모니터링) -> 재진(재학습) 전 과정이 끊어지면 환자가 죽듯, 파이프라인이 끊기면 모델은 6개월 내 **모델 드리프트**로 폐기된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 통계적 추론(Statistical Inference)의 3대 기둥

| 구분 | 빈도주의(Frequentist) | 베이즈(Bayesian) | 인과추론(Causal) |
| :--- | :--- | :--- | :--- |
| 핵심 사고 | 반복 표본 평균, long-run frequency | 사전분포 + 데이터 = 사후분포 | 처치(T) -> 결과(Y)의 인과효과 식별 |
| 대표 기법 | t-test, ANOVA, χ², OLS, MLE | MCMC(HMC, NUTS), VI, BMA | IV, PSM, DiD, RDD, Synthetic Control |
| 산출물 | p-value, CI, 점추정량 | 사후분포, Credible Interval, Bayes Factor | ATE, ATT, CATE, Dose-Response |
| 도구 | R statsmodels, SAS | PyMC, Stan, NumPyro, JAGS | DoWhy, EconML, CausalML, CausalImpact |
| 적용 예 | A/B 테스트 p<0.05 판단 | 사전지식 결합한 소표본 추론 | 마케팅 처치의 실제 인과 Lift 측정 |

### 2) CRISP-DM vs TDSP vs MLOps Levels 3대 방법론 프레임워크

```text
[3대 방법론 프레임워크 단계 비교]

CRISP-DM (1996)          Microsoft TDSP (2017)         Google MLOps Levels (2021)
-------------            --------------------           -------------------------
① Business               ① Business Understanding       ① Level 0: Manual
② Data Understanding     ② Data Acquisition & Wrangling  ② Level 1: ML Pipeline
③ Data Preparation       ③ Modeling                      ③ Level 2: CI/CD Pipeline
④ Modeling               ④ Deployment                     ④ Level 3: Rapid Iteration
⑤ Evaluation             ⑤ Customer Acceptance          ⑤ Level 4: Full Automation
⑥ Deployment

특징: 도메인 무관 범용       특징: Agile·Git 연동·Role 정의   특징: 성숙도 5단계(0~4)
      6단계 순환              (Data Engineer, Modeler,         모델·데이터·코드 3축
                             Project Lead) 자동화 강조          자동화 통합 거버넌스
```

### 3) 데이터 전처리 핵심 기법 매트릭스

| 결측치 유형 | 정의 | 검정법 | 처리 기법 |
| :--- | :--- | :--- | :--- |
| **MCAR** (완전무작위) | 결측이 데이터 자체와 무관 | Little's MCAR Test | Listwise 삭제, 단일대치(평균/중앙/최빈) |
| **MAR** (무작위) | 다른 관측변수에 의존 | 패턴 분석, 로지스틱 회귀 | MICE(Multiple Imputation), KNN Imputer, MissForest |
| **MNAR** (비무작위) | 결측 자체가 결과에 영향 | 도메인 지식, Heckman Selection | 도메인 기반 모델링, Missing Indicator + 학습 |

| 스케일링 기법 | 수식/원리 | 적용 상황 | 주의점 |
| :--- | :--- | :--- | :--- |
| StandardScaler | (x-μ)/σ | 정규분포 가정, SVM·로지스틱·PCA | 이상치에 취약 |
| MinMaxScaler | (x-x_min)/(x_max-x_min) | 신경망 입력, 이미지 [0,1] 정규화 | 이상치에 매우 취약 |
| RobustScaler | (x-Q2)/(Q3-Q1) | 이상치 多 데이터 | 분포 보존력 다소 저하 |
| MaxAbsScaler | x/\|max\| | 희소 행렬(BoW, TF-IDF) | 음수 동시 처리 |
| QuantileTransformer | 균등분포/정규분포 매핑 | 비선형, 파워변환 | 랜덤 시드 고정 필요 |
| PowerTransformer(Yeo-Johnson) | Box-Cox 확장, 음수 가능 | 정규성 확보 | 0 이하 모두 처리 가능 |

### 4) 분류 모델별 손실함수 & 적합 데이터 형태

| 모델 | 손실함수 | 학습방식 | 정형데이터 | 고차원·희소 | 비정형(이미지/텍스트) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | Log Loss | Closed-form/SGD | ◎ | △ | × |
| Random Forest | Gini/Entropy | Bagging | ◎ | × | △ |
| XGBoost | Log Loss + Ω(f) | Boosting (2차 근사) | ◎ | ○ | × |
| LightGBM | Log Loss + GOSS·EFB | Histogram + Boosting | ◎ | ○ | × |
| CatBoost | LogLoss + Ordered TS | Oblivious Tree | ◎(범주多) | △ | × |
| SVM(Hinge) | Hinge + ‖w‖² | SMO/SGD | ○ | ◎ | △ |
| MLP | Cross-Entropy + L2 | Backprop | ○ | △ | ◎ |
| CNN | CE + Dropout | Backprop | × | × | ◎(이미지) |
| Transformer | CE + Label Smoothing | Backprop | △ | × | ◎(텍스트/LLM) |

### 5) 모델 평가 — 데이터 누수(Data Leakage) 방지 분할

```text
[Cross-Validation 분할 전략 비교]

  단순 K-Fold                    Stratified K-Fold            Group K-Fold
  +-+-+-+-+-+                  +-+-+-+-+-+                +-+-+-+-+-+
  |1|2|3|4|5|                  |1|2|3|4|5|                |A|A|B|B|C|
  +-+-+-+-+-+                  +-+-+-+-+-+                +-+-+-+-+-+
  - 회귀/균형 분류              - 불균형 분류                - 환자/사용자 단위
  - 시계열 X                     - 다중분류                   - 시계열 그룹
                                                              (예: 동일 환자 행위
                                                               가 train+test에
                                                               모두 들어가는
                                                               leakage 방지)

  TimeSeriesSplit               Nested K-Fold (Hyperparam)
  +-----+                        Outer: 성능 평가
  | Train|                       Inner: 하이퍼파라미터 튜닝
  |    CV|                       -> 정보 누출 차단
  +-----+
  |Test |
  +-----+
  - 시계열 미래 정보 차단
```

### 6) MLOps 성숙도 5단계 (Google MLOps Levels)

| Level | 명칭 | 핵심 산출물 | 자동화 범위 | 도구 스택 예시 |
| :--- | :--- | :--- | :--- | :--- |
| **L0** | Manual Process | Jupyter 노트북, 수동 배포 | 없음 | Notebook + 수동 스크립트 |
| **L1** | ML Pipeline | 학습 파이프라인 자동화 | 학습/재학습 트리거 | Airflow + MLflow + Docker |
| **L2** | CI/CD Pipeline | 코드/모델/데이터 검증, 자동 배포 | 학습+배포+테스트 | GitHub Actions + MLflow Registry + K8s |
| **L3** | Rapid Iteration | A/B 테스트, 자동 피드백 루프 | L2 + 실험관리 | TFX + Kubeflow + KServe + Prometheus |
| **L4** | Full Automation | Continuous Training (CT) | L3 + 데이터/모델 자동 갱신 | Vertex AI / SageMaker Pipelines / Aporia + Fiddler |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Data Versioning** | 데이터 스냅샷·라인리지 | DVC, Delta Lake(time travel), LakeFS, Pachyderm, Iceberg |
| **Experiment Tracking** | 하이퍼파라미터·지표·아티팩트 기록 | MLflow Tracking, Weights & Biases, Neptune, TensorBoard |
| **Model Registry** | 모델 버전·스테이지 관리 | MLflow Registry, BentoML, SageMaker Model Registry, Vertex AI |
| **Feature Store** | Online/Offline 피처 일관성 | Feast, Tecton, Hopsworks, DynamoDB+Redis (Online) / S3+Parquet (
