---
title: "MLOps Machine Learning Lifecycle Management"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 746
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MLOps는 ML 모델의 **데이터 수집->피처 엔지니어링->학습->검증->배포->모니터링->재학습** 전 주기를 **코드-데이터-모델-메타데이터의 4축 버전관리**와 **CI/CD/CT(Continuous Training)** 파이프라인으로 자동화하는 DevOps 확장 엔지니어링 체계이다. 핵심은 Kubeflow/MLflow/TFX/SageMaker/Vertex AI 등 **선언적 파이프라인 오케스트레이터**, **Feature Store**, **Model Registry**, **Model Serving**의 4계층 통합이다.
> 2. **가치**: Forbes(2023) 조사에서 MLOps 도입 기업은 모델 배포 주기 **평균 9.6배 단축**(20.5개월->2.1개월), 운영 비용 **40~60% 절감**, 모델 성능 저하(Drift) 감지 후 자동 재학습으로 **AUC 12~18% 회복**을 달성한다. 무엇보다 **재현성·감사추적·규제 준수(EU AI Act, SR 11-7)** 라인을 기술적으로 보장하여 "Black Box AI" 리스크를 정량화한다.
> 3. **판단 포인트**: 실무적 핵심은 **MLOps 성숙도 Level 0/1/2(Google 기준)** 중 어디까지 도입할지, **배치 vs 실시간 스트리밍 추론 아키텍처** 선택, **Shadow/Canary/A/B Test 배포 전략**, **Data Drift·Concept Drift·Label Drift** 3종 감지 임계치 설정, 그리고 **GPU 자원 스케줄링(Karpenter+Volcano vs Kubeflow TrainerServer)**과 **Feature Store 일관성(Training-Serving Skew 방지)** 판단이다.

---

## Ⅰ. 개요 및 필요성

전통적 ML 개발은 **"Notebook에서 데이터 분석 -> 스크립트로 학습 -> PM에게 ppt 전달 -> 인프라팀이 수동 배포"** 의 1회성 사이클이었다. 그러나 실제 운영 환경에서는 (1) **데이터 분포 변화(Data Drift)** 로 모델 AUC가 6개월 내 15% 이상 하락하고, (2) **재현성 부재**로 "어떤 데이터로 학습했는지" 추적 불가하며, (3) **수동 배포**로 신규 모델 반영까지 3~6개월이 소요되고, (4) **규제 요구**(EU AI Act Article 9, 금융감독원 SR 11-7, 의료기기 FDA SaMD) 충족이 불가능하다.

MLOps(Machine Learning Operations)는 **ML 시스템의 안정성·확장성·재현성·거버넌스**를 엔지니어링 수준으로 끌어올리기 위해 등장한 **MLDevOps + DataOps + ModelOps** 융합 discipline이다. Google은 2020년 논문 *"Hidden Technical Debt in ML Systems"* (Sculley et al.)에서 ML 시스템의 실제 코드 비중은 5% 미만이며 나머지 95%가 **데이터·피처·설정·인프라**라는 점을 입증했고, 이 부채를 갚는 유일한 해법이 MLOps임을 보였다.

```text
                  MLOps 머신러닝 생명주기(ML Lifecycle) v3.0
 +----------------------------------------------------------------------+
 | ① Problem Framing --> ② Data Mgmt --> ③ Feature Eng --> ④ Model Train |
 |                                                                      |
 | ⑨ Retrain Trigger <--- ⑧ Monitor <--- ⑦ Serving <--- ⑤ Validate <--- ⑥ |
 |                                                                      |
 |        +--------------------------------------------------+          |
 |        |  MLOps Cross-cutting Concerns (4축 버전관리)     |          |
 |        |  · Code (Git)                                    |          |
 |        |  · Data  (DVC / Delta Lake / LakeFS / Datasets)  |          |
 |        |  · Model (MLflow / DVC / Model Registry)         |          |
 |        |  · Metadata/Lineage (OpenLineage / Marquez)      |          |
 |        +--------------------------------------------------+          |
 +----------------------------------------------------------------------+

       +------------+   +------------+   +------------+
       | Data Sci.  |   | ML Eng.    |   | SRE/Platform|
       |  Notebook  |   |  Pipeline  |   |  K8s/Cloud  |
       |  EDA/HP   |   |  CI/CD/CT  |   |  GPU/IaC    |
       +-----+------+   +-----+------+   +-----+------+
             +-----------------+-----------------+
                               v
                 +---------------------------+
                 |  Feature Store (Online/Offline) |
                 |  Feast · Tecton · DynamoDB+Redis |
                 +---------------------------+
                               v
                 +---------------------------+
                 |  Model Serving (Multi-variant)  |
                 |  Seldon · BentoML · TF Serving · Triton |
                 +---------------------------+
```

**기존(MLOps 이전) vs 신규(MLOps 도입 후) 비교**
- *기존*: 모델 = `.pkl` 파일 + Jupyter Notebook, 배포 = `scp` 또는 Docker 수동 빌드, 모니터링 = 서버 CPU/RAM만 관찰
- *신규*: 모델 = **서명·리니지·메트릭이 결합된 Model Registry 아티팩트**, 배포 = **GitOps(Argo CD) 기반 선언적 배포**, 모니터링 = **데이터·예측·성능·공정성·설명가능성 5종 통합 대시보드**

- **📢 섹션 요약 비유**: MLOps는 **자동차 공장의 조립 라인**과 같다. 과거에는 장인이 한 대씩 수제작하던 자동차(R&D 노트북 ML)를, **로봇 팔(Kubeflow Pipelines)**이 **부품 입고(DVC 데이터 버전)** -> **차체 용접(피처 변환)** -> **엔진 장착(학습)** -> **품질 검정(검증)** -> **시운전(Canary 배포)** -> **주행 데이터 모니터링(Drift 감지)** -> **리콜(자동 재학습)** 까지 끊김 없이 이어주는 **완전 자동화 라인**으로 재설계한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MLOps 플랫폼은 통상 7계층 아키텍처로 구성된다. 각 계층은 **느슨한 결합(Loose Coupling)** 과 **표준 인터페이스(OCI, MLflow API, OpenLineage Spec)** 로 연결되어야 한다.

```text
       MLOps 7계층 참조 아키텍처 (CNCF MLOps Roadmap 2024 기준)
 +---------------------------------------------------------------+
 |  L7. 거버넌스/컴플라이언스  (EU AI Act, ISO/IEC 42001, SR11-7)|
 |       Model Card · Data Card · Audit Log · Access Control    |
 +---------------------------------------------------------------+
 |  L6. 모니터링/옵저버빌리티 (Evidently · WhyLabs · Grafana)    |
 |       Drift · Bias · Explainability · Latency · Business KPI |
 +---------------------------------------------------------------+
 |  L5. 서빙/추론              (Triton · BentoML · Seldon · vLLM)|
 |       Online · Batch · Edge · Streaming · Multi-armed Bandit |
 +---------------------------------------------------------------+
 |  L4. 모델 레지스트리         (MLflow · Vertex Model Registry) |
 |       Versioning · Stage(Staging/Prod) · Lineage · Sign-off  |
 +---------------------------------------------------------------+
 |  L3. 피처 스토어             (Feast · Tecton · AWS Feature Store)|
 |       Online (Redis/DynamoDB) + Offline (Iceberg/BigQuery)   |
 |       Point-in-Time Join · Training-Serving Skew 방지        |
 +---------------------------------------------------------------+
 |  L2. 파이프라인 오케스트레이션 (Kubeflow Pipelines · Airflow · Argo)|
 |       DAG · CI/CT(Continuous Training) · Hyperparameter Tun.|
 +---------------------------------------------------------------+
 |  L1. 데이터/컴퓨트 인프라     (K8s · Karpenter · Volcano · Spot)|
 |       GPU Pool(T4/A100/H100) · S3/MinIO · Delta/Iceberg     |
 +---------------------------------------------------------------+
       ^ 모든 계층을 관통: IaC(Terraform) + GitOps(Argo CD) + Observability
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **데이터 버전관리(Data VCS)** | Raw/Feature 데이터의 **불변 스냅샷** 생성 및 재현성 보장 | **DVC**(Git+Hash), **Delta Lake**(ACID Transaction), **LakeFS**(Git-like Branching), **Pachyderm**(Data Pipeline 버전관리). 데이터의 SHA-256 해시를 Git Commit에 매핑하여 "어떤 commit = 어떤 데이터"를 1:1 추적 |
| **피처 스토어(Feature Store)** | Online/Offline 일관된 피처 제공, **Training-Serving Skew** 제거 | **Feast**(OSS 표준, Parquet+Redis), **Tecton**(상용, 실시간 변환 Lambda), **Vertex AI Feature Store**(BigQuery+Vertex Online). 핵심은 **Point-in-Time Correctness** — 학습 시점 기준으로 시계열 누수 없이 join 보장 |
| **파이프라인 오케스트레이터** | DAG 기반 ML 워크플로 자동 실행·재시도·캐싱 | **Kubeflow Pipelines**(Argo Workflow 기반, K8s-native), **Apache Airflow**(범용 DAG), **Metaflow**(Netflix, AWS 통합), **Flyte**(Lyft, K8s-native). **Argo Events**로 트리거(Event-driven CT) 구현 |
| **실험 추적(Experiment Tracking) & Model Registry** | 하이퍼파라미터·메트릭·아티팩트 기록, 모델 수명주기 관리 | **MLflow Tracking**(OSS 표준, REST API+UI), **Weights & Biases**(상용, Sweep+Reports), **Neptune.ai**, **Vertex Experiments**. **Model Registry**는 모델을 `Staging->Production` Stage 전이 + **Model Signature**(입출력 스키마) 검증 + **Lineage** 추적 |
| **CI/CD/CT 자동화** | 코드 변경 시 **자동 학습·검증·배포·재학습** | **CI**: GitHub Actions/GitLab CI -> Lint/Unit Test -> Feature Store 스키마 검증. **CD**: **Argo CD** GitOps -> Canary(Istio 5%->50%->100%) -> Shadow Mode. **CT(Continuous Training)**: **Evidently AI**가 Drift 감지 -> Airflow Trigger -> 재학습 -> A/B Test |
| **모델 서빙(Model Serving)** | 고吞吐/저지연 추론, 다중 모델·다중 변형(Multi-variant) | **NVIDIA Triton Inference Server**(GPU, Dynamic Batching, TensorRT), **BentoML**(Python-native, Dockerize), **Seldon Core**(K8s, Canary/Shadow 내장), **TF Serving**(TensorFlow 특화), **vLLM**(LLM 특화, PagedAttention), **KServe**(K8s-native, Serverless) |
| **모니터링/옵저버빌리티** | **5종 Drift** + 성능 + 비즈니스 메트릭 통합 관찰 | **Evidently AI**(OSS, 100+ 메트릭), **WhyLabs**(상용), **Arize Phoenix**(LLM 추적), **NannyML**(정답 라벨 부재 시 성능 추정). **Evidently**는 **Data Drift(KS-test, PSI)·Prediction Drift·Concept Drift·Target Drift·Model Performance Drift**를 자동 계산 |
| **컴퓨트 오케스트레이션** | GPU/캐시/스토리지 자원 효율적 스케줄링 | **Karpenter**(AWS, Spot 최적화), **Volcano**(K8s Gang Scheduling, ML 워크로드 특화), **Ray**(분산 학습/추론), **KubeRay**(Ray on K8s). A100/H100 GPU는 시간당 수백만 원 -> **Spot Instance + Preemption Tolerance** 필수 |

**핵심 메커니즘: Training-Serving Skew 제거**

가장 치명적인 ML 운영 장애 원인은 **학습 환경과 서빙 환경의 피처 변환 로직 불일치**이다. 이를 해결하기 위해 **(1) 동일한 피처 변환 코드를 Python 패키지(`features/transform.py`)로 빌드 -> (2) 학습 파이프라인과 Online Serving 양쪽에서 동일 모듈 import -> (3) 피처 정의는 YAML/JSON으로 선언(`feature_store.yaml`) -> (4) CI에서 스키마 회귀 테스트** 4단계를 강제한다. Tecton의 경우 **Lambda 아키텍처**로 배치(Tecton-managed Spark)와 스트리밍(Flink) 양쪽에서 동일 변환을 자동 실행한다.

**자동 재학습(CT, Continuous Training) 트리거 설계**

| 트리거 유형 | 감지 방법 | 임계치 권장 | 재학습 범위 |
| :--- | :--- | :--- | :--- |
| **Data Drift** (입력 분포 변화) | PSI(Population Stability Index) | PSI > 0.2 | 재학습 |
| **Concept Drift** (입출력 관계 변화) | Adversarial Validation AUC, KL-Divergence | AUC > 0.7 | 재학습 |
| **Performance Drift** (성능 저하) | 라벨 도착 후 Recall/Accuracy 모니터링 | Recall < Baseline − 10% | 재학습 + 피처 재검토 |
| **Data Quality** | Great Expectations 체크 | Pass Rate < 99% | 경고 -> ETL 조사 |
| **Schedule-based** | Cron/Event | 월 1회 / 분기 1회 | 정기 재학습 |
| **Shadow Model** | 신규 모델을 Shadow로 운영 후 비교 | 신규 모델 PR-AUC > 현행 + 2% | 자동 승격 |

- **📢 섹션 요약 비유**: MLOps 7계층은 **항공기의 이중/삼중冗長(Redundancy) 시스템**과 같다. 비행(L1~L7)·항법(피처 스토어)·통신(모니터링)·자동조종(CI/CD/CT)·블랙박스(Lineage)·정비 매뉴얼(IaC)·인증서(거버넌스) 모두 별도 계층으로 분리되어, 한 층이 실패해도 다른 층이 안전하게 착륙시킨다. 특히 **컴퓨트 자원처럼 치명적인 자원**은 **Volcano(우선순위) + Karpenter(탄력성) + Spot(비용)** 3중 보험으로 운용한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **MLOps** | **DevOps** | **AIOps** | **DataOps** |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 대상** | ML 모델·데이터·피처 | 애플리케이션 코드 | IT 운영 로그·메트릭 | 데이터 파이프라인·품질 |
| **자동화 단위** | **CT(Continuous Training)** + CI/CD | CI/CD (Build/Test/Deploy) | 이상탐지·근인분석 자동화 | 데이터 품질·스키마 진화 자동화 |
| **버전관리 4축** | Code + **Data + Model + Config** | Code + Config | 로그/메트릭 자체 | Data + Schema + Pipeline |
| **배포 산출물** | 모델 아티팩트(.pt/.pkl) + 서빙 컨테이너 + 피처 정의 | 컨테이너 이미지 + IaC | 대시보드/알람 룰 | 데이터셋 + 품질 리포트 |
| **테스트 유형** | Unit + Integration + **Model A/B + Fairness + Robustness** | Unit + Integration + E2E + Load | Anomaly Detection Test | Data Quality + Schema + Lineage |
| **도구 스택** |