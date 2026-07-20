---
title: "Model Monitoring Performance Degradation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 751
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모델 모니터링-성능 저하 감지-알림-재학습은 Data/Concept Drift를 통계적·분포적 방법으로 탐지하여 임계치 기반 트리거와 CI/CT 파이프라인을 통해 자동 재학습(Re-training) 및 배포(Re-deployment)를 수행하는 **MLOps 폐루프(Closed-loop) 모델 수명주기 관리 체계**이다.
> 2. **가치**: 도메인별 모델 정확도 열화를 평균 5~15% 이내로 억제하고, MTTR(Mean Time To Recovery)을 수동 대비 70% 단축하며, KSIC/금융/제조 분야에서 **모델 리스크 관리(TRM, Model Risk Management)** 컴플라이언스 요건 충족 및 운영 비용 절감을 실현한다.
> 3. **판단 포인트**: (a) 통계 검정(KS, PSI, KL-Div, ADWIN) 선택, (b) 알림 노이즈 최소화 vs 민감도(Sensitivity/Specificity) Trade-off, (c) 자동 재학습의 **Shadow·Canary·Blue-Green** 배포 전략, (d) **재학습 트리거 비용 vs 모델 성능 손실**의 경제적 균형점(Break-Even Point) 산정이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

운영 환경(Production)에 배포된 머신러닝 모델은 시간이 지남에 따라 입력 데이터의 분포 변화(Data Drift) 또는 목표 변수와 입력 변수 간 관계의 변화(Concept Drift)로 인해 성능이 점진적·급격하게 저하된다. 전통적 소프트웨어는 코드와 환경의 일관성이 유지되는 한 동일 작동을 보장하지만, **ML 모델은 "코드는 고정"되어도 "데이터는 유동"**이라는 특성 때문에 별도의 거버넌스가 요구된다. 이를 **"Model Decay"** 또는 **"Model Rot"**이라 하며, 단순한 재학습이 아닌 **탐지 -> 알림 -> 진단 -> 재학습 -> 검증 -> 배포**의 전 과정을 자동화해야 한다.

특히 금융·의료·자율주행 같은 **규제 산업**에서는 2011년 SR 11-7(연방준비은행), EU AI Act, 2023년 한국 금융위원회 「AI 신뢰성 평가 가이드」 등에서 모델의 **지속적 모니터링과 재검증**을 법적 의무로 명시하고 있어, 본 주제는 기술적·규제적 필수 영역으로 부상했다.

```text
[Model Lifecycle with Monitoring & Retraining]

  +----------------------------------------------------------------------+
  |                       1. Model Development Phase                      |
  |   +-----------+    +-----------+    +------------+                   |
  |   | Data Eng. | ->  | Train/Tune| ->  | Validation |                   |
  |   +-----------+    +-----------+    +------------+                   |
  +---------------------------------+------------------------------------+
                                    | Model Registry 등록
                                    v
  +----------------------------------------------------------------------+
  |                     2. Production Serving Phase                       |
  |   +--------------------------------------------------------+         |
  |   |           Inference Service (REST/gRPC, KServe)         |         |
  |   |           ^            ^            ^                  |         |
  |   |    Predict|    Predict|    Predict|  (Online/Batch)     |         |
  |   +----------+------------+------------+-------------------+         |
  +--------------+------------+------------+----------------------------+
                 |            |            |
                 v            v            v
  +----------------------------------------------------------------------+
  |                  3. Monitoring & Telemetry Layer                       |
  |   +--------------+   +--------------+   +--------------+             |
  |   | Input Drift  |   | Output Drift |   |  Performance |             |
  |   |  (PSI, KS)   |   | (Class Dist) |   | (Acc/F1/AUC) |             |
  |   +------+-------+   +------+-------+   +------+-------+             |
  |          +------------------+------------------+                     |
  |                             v                                         |
  |                  +----------------------+                             |
  |                  |  Alert Engine (Pager,|                             |
  |                  |  Slack, OpsGenie)    |                             |
  |                  +----------+-----------+                             |
  +-----------------------------+----------------------------------------+
                                | Trigger
                                v
  +----------------------------------------------------------------------+
  |                  4. Automated Retraining Pipeline                     |
  |   +----------+  +----------+  +----------+  +----------+            |
  |   | Data Pull|-> | Retrain  |-> | Validate |-> | Register |            |
  |   |(Feast)   |  |(Kubeflow)|  | (Champion|  |  (MLflow)|            |
  |   +----------+  +----------+  |  /Chal.) |  +----+-----+            |
  |                                +----------+       |                  |
  +---------------------------------------------------+------------------+
                                                      v
                                          +----------------------+
                                          | Staged Deployment    |
                                          | Shadow -> Canary 10%  |
                                          | -> 50% -> 100% (Prod)  |
                                          +----------------------+
```

**왜 필요한가? — 구(舊) vs 신(新) 패러다임 비교**

| 항목 | 전통 SW 운영 | ML 모델 운영 (MLOps) |
| :--- | :--- | :--- |
| 실패 패턴 | 버그, 메모리 누수, 네트워크 장애 | 데이터 분포 변화, 라벨 노이즈, **무음 실패(Silent Failure)** |
| 복구 방법 | 패치·롤백 (코드 자체 수정) | **재학습 + 모델 교체** (새로운 데이터로 모델 업데이트) |
| 모니터링 대상 | CPU, Memory, Latency, Error Rate | + **Data Drift, Concept Drift, Prediction Confidence, Fairness** |
| 검증 주기 | 릴리즈 시 1회 | **지속적(Continuous)** + 주기적(Periodic) |
| SLA 기준 | 응답시간, 가용성 | + 모델 정확도/공정성 유지율 |

- **📢 섹션 요약 비유**: ML 모델 운영은 마치 **"냉장고에 넣은 우유"**와 같다. 한 번 학습시켜서 배포했다고 끝이 아니라, 유통기한(데이터 신선도)이 있고 시간이 지나면 상한다. 매주 **냄새(Drift)를 맡고**, 상했다면 **새 우유로 교체(Retrain)**해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

모델 모니터링·재학습 시스템은 크게 **5개 레이어**로 구성된다: (1) **Telemetry 수집**, (2) **Drift Detection 엔진**, (3) **Alert & Routing**, (4) **CT(Continuous Training) Orchestrator**, (5) **Safe Deployment** 레이어.

```text
[상세 아키텍처: End-to-End MLOps Closed Loop]

  +--------------------------------------------------------------------+
  |                       A. Data Sources                                |
  |   [Live Stream] --- Kafka/Kinesis --+                              |
  |   [Batch Sink]   --- S3/HDFS   -----+                              |
  |   [Feedback Label] - Ground Truth --+                              |
  +-------------------------------------+------------------------------+
                                        v
  +--------------------------------------------------------------------+
  |             B. Telemetry & Feature Logging Layer                    |
  |   +----------------------------------------------------------+     |
  |   |  Feature Store (Feast / Tecton / Hopsworks)              |     |
  |   |  +------------+  +------------+  +------------+          |     |
  |   |  | Offline    |  | Online     |  | Monitoring |          |     |
  |   |  | Store      |  | Store (Redis| | Stats      |          |     |
  |   |  | (Parquet)  |  |  /DynamoDB)|  | (Sketch)   |          |     |
  |   |  +------------+  +------------+  +------------+          |     |
  |   +----------------------------------------------------------+     |
  |            |                  |                  |                 |
  |            v                  v                  v                 |
  |   +--------------+  +------------------+  +--------------+         |
  |   | Model Input  |  | Model Output     |  | Ground Truth |         |
  |   | Logging      |  | (Prediction,     |  | Collector    |         |
  |   | (Raw + Hash) |  |  Confidence)     |  | (Delayed)    |         |
  |   +------+-------+  +--------+---------+  +------+-------+         |
  +----------+-------------------+-------------------+-----------------+
             |                   |                   |
             v                   v                   v
  +--------------------------------------------------------------------+
  |               C. Drift Detection & Statistics Engine                 |
  |   +----------------+  +----------------+  +----------------+        |
  |   | Feature-level  |  | Prediction-    |  | Performance    |        |
  |   | Drift           |  | level Drift    |  | Degradation    |        |
  |   |                |  |                |  |                |        |
  |   | • KS Test      |  | • Chi-square   |  | • Accuracy     |        |
  |   | • PSI          |  | • JS-Div       |  | • F1/AUC       |        |
  |   | • Wasserstein  |  | • Class prior  |  | • RMSE/MAE     |        |
  |   | • KL-Div       |  |   shift        |  | • Calibration  |        |
  |   | • CUSUM        |  | • Confidence   |  |   Error (ECE)  |        |
  |   | • ADWIN        |  |   histogram    |  | • Business KPI |        |
  |   +--------+-------+  +--------+-------+  +--------+-------+        |
  |            +------------------+------------------+                 |
  |                               v                                     |
  |                  +------------------------+                         |
  |                  |  Drift Score Aggregator|                         |
  |                  |  + Statistical         |                         |
  |                  |    Process Control     |                         |
  |                  |  (SPC Chart, EWMA)     |                         |
  |                  +------------+-----------+                         |
  +-------------------------------+-------------------------------------+
                                  | Drift Score
                                  v
  +--------------------------------------------------------------------+
  |                D. Alert & Decision Layer                             |
  |   +-----------------+   +-----------------+   +-----------------+   |
  |   | Threshold-based |   | Anomaly-based   |   | Business-rule   |   |
  |   | (Static/Dynamic)|   | (IsolationForest|   | based           |   |
  |   |                 |   |  /LSTM-AE)      |   | (Segment, Region|   |
  |   +--------+--------+   +--------+--------+   +--------+--------+   |
  |            +---------------------+---------------------+            |
  |                                  v                                  |
  |             +-------------------------------------+                 |
  |             | Alert Manager (Alertmanager/PagerDuty)|               |
  |             | • Routing • Deduplication • Silencing|               |
  |             +--------------+----------------------+                 |
  +----------------------------+--------------------------------------+
                               | Severity(Info/Warn/Crit) + Trigger Action
                               v
  +--------------------------------------------------------------------+
  |           E. Continuous Training (CT) Orchestrator                  |
  |   +----------------------------------------------------------+     |
  |   |   Argo Workflows / Airflow / Kubeflow Pipelines          |     |
  |   |   +--------+ +--------+ +--------+ +--------+ +--------+|     |
  |   |   |Extract |->|Validate|->| Feature|->|  Train |->| Eval   ||     |
  |   |   | Data   | | Schema | | Engine | | (HP Opt)| |(Champ.)||     |
  |   |   +--------+ +--------+ +--------+ +--------+ +---+----+|     |
  |   |                                                    v     |     |
  |   |            +------------------------------------+         |     |
  |   |            |  Model Registry (MLflow/Vertex)    |         |     |
  |   |            |  • Versioning                      |         |     |
  |   |            |  • Stage: None->Staging->Production  |         |     |
  |   |            |  • Lineage (DVC, Metadata Store)   |         |     |
  |   |            +------------+-----------------------+         |     |
  |   +-------------------------+---------------------------------+     |
  +-----------------------------+---------------------------------------+
                                | Champion(신) vs Challenger(현행)
                                v
  +--------------------------------------------------------------------+
  |                   F. Safe Deployment Layer                           |
  |   +----------+   +----------+   +----------+   +----------+        |
  |   |  Shadow  | -> |  Canary  | -> |  A/B     | -> |  Blue/   |        |
  |   |  Mode    |   |   1~5%   |   |  Test    |   |  Green   |        |
  |   | (100% log|   |  Traffic |   | (50/50)  |   |  Switch  |        |
  |   |  parallel|   |          |   |          |   |          |        |
  |   +----------+   +----------+   +----------+   +----------+        |
  |                                                                  --|
  |   Istio/Envoy Traffic Splitting + Prometheus Auto-rollback       --|
  +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Telemetry Collector** | 입력/출력/피드백 데이터 캡처 | OpenTelemetry SDK, Vector, Fluent Bit; **결정론적 로깅**(동일 입력 ID에 동일 출력 ID)으로 학습-서빙 스큐(Skew) 탐지 |
| **Drift Detection Engine** | 통계적 분포 변화 정량화 | **PSI**: `Σ (P_ref - P_curr) × ln(P_ref/P_curr)`, 임계치 `<0.1 안정 / 0.1~0.2 경고 / >0.2 위험`. **KS-Test**: 누적 분포 함수 최대 차이로 비모수 검정 (p-value < 0.05 유의). **ADWIN**: 적응형 윈도우 기반 변화점 탐지로 메모리 효율적 |
| **Performance Monitor** | 실제 라벨 대비 정확도 측정 | **라벨 지연(Lag)**이 큰 경우 **Prequential Evaluation**(test-then-train) 또는 **Importance-Weighted AUC** 활용. 분류는 F1/AUC/LogLoss, 회귀는 RMSE/MAE/MAPE, 랭킹은 NDCG/MRR |
| **Alert & Orchestrator** | 임계치