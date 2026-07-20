---
title: "Kubeflow Kubernetes Ml Pipeline"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 167
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubeflow는 쿠버네티스(Kubernetes) 위에서 ML 워크로드를 오케스트레이션하는 플랫폼으로, 데이터 과학자가 컨테이너 기반의 재현 가능한 ML 파이프라인을 DAG (Directed Acyclic Graph)로 정의하고 실행할 수 있게 한다.
> 2. **가치**: Kubeflow Pipelines로 ML 워크플로우를 표준화하고, Katib으로 하이퍼파라미터 자동 최적화(AutoML)를 실행하며, KServe로 멀티 프레임워크 모델을 단일 플랫폼에서 서빙함으로써 MLOps 전 과정을 쿠버네티스 생태계 안에서 통합한다.
> 3. **판단 포인트**: Kubeflow는 강력하지만 쿠버네티스 운영 전문성이 필요하고 초기 설정이 복잡하므로, 클라우드 관리형(Vertex AI Pipelines, SageMaker)과 온프레미스/하이브리드 환경에서의 통제 필요성을 비교하여 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 Kubeflow란?

<strong>Kubeflow</strong>는 Google이 주도하여 개발한 쿠버네티스 기반의 오픈소스 ML 플랫폼으로, ML 모델의 개발부터 배포까지 전 과정을 쿠버네티스 클러스터에서 실행할 수 있도록 설계됐다.

```
쿠버네티스 (Kubernetes) 클러스터
+-----------------------------------------------------------------+
|                         Kubeflow                                |
+--------------+--------------+--------------+--------------------+
|  Kubeflow    |    Katib     |   KServe     |  Notebooks         |
|  Pipelines   |   (AutoML)   |  (모델 서빙)  |  (JupyterHub)      |
|              |              |              |                    |
|  DAG 기반    |  HPO         |  REST/gRPC   |  JupyterLab        |
|  ML 파이프   |  Grid/Random |  다중 프레임  |  GPU 지원          |
|  라인 실행   |  Bayesian    |  워크 서빙    |  팀 공유           |
|  컨테이너화  |  HyperBand   |  카나리 배포  |                    |
+--------------+--------------+--------------+--------------------+
|              |              |              |
|              Training       |              |
|              Operator       |              |
|  (TFJob, PyTorchJob,        |              |
|   MXNetJob, XGBoostJob)     |              |
+-----------------------------------------------------------------+
```

### 1.2 Kubeflow가 해결하는 문제

| 문제 | Kubeflow 해결 방법 |
|:---|:---|
| **환경 재현성** | 모든 단계를 Docker 컨테이너로 실행 |
| **자원 관리** | 쿠버네티스 기반 GPU/CPU 자동 할당 |
| <strong>파이프라인 오케스트레이션</strong> | DAG 기반 의존성 관리 |
| <strong>하이퍼파라미터 튜닝</strong> | Katib로 AutoML 자동화 |
| **모델 서빙 복잡성** | KServe로 멀티 프레임워크 단일 서빙 |
| **실험 추적** | MLflow 통합 |

📢 **섹션 요약 비유**: Kubeflow는 ML 버전의 쿠버네티스라고 할 수 있다. 쿠버네티스가 컨테이너 앱 배포를 자동화하듯, Kubeflow는 ML 모델의 학습->튜닝->서빙 과정을 자동화한다. 쿠버네티스 인프라 위에서 움직이므로 클라우드 네이티브 ML의 표준이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Kubeflow Pipelines 아키텍처

```
+-----------------------------------------------------------------+
|                  Kubeflow Pipelines 내부 구조                   |
+------------------------------------------------------------------+
|                                                                  |
|  Python Pipeline DSL                                             |
|  @dsl.pipeline 데코레이터로 DAG 정의                             |
|         |                                                        |
|         v                                                        |
|  Pipeline SDK -> YAML/JSON 컴파일                                |
|         |                                                        |
|         v                                                        |
|  +---------------------------------------------+               |
|  |  Kubeflow Pipelines 백엔드                   |               |
|  |  +--------------+  +----------------------+ |               |
|  |  |  API Server  |  |  Pipeline Persistence| |               |
|  |  |  (REST API)  |  |  (MySQL)             | |               |
|  |  +--------------+  +----------------------+ |               |
|  |  +--------------+  +----------------------+ |               |
|  |  |  Scheduler   |  |  Artifact Store      | |               |
|  |  |  (Argo WF)   |  |  (MinIO/S3)          | |               |
|  |  +--------------+  +----------------------+ |               |
|  +---------------------------------------------+               |
|         |                                                        |
|         v 각 단계는 쿠버네티스 Pod로 실행                        |
|  +----------+ +----------+ +----------+ +----------+          |
|  | 데이터   |->| 피처     |->| 학습     |->| 평가     |          |
|  | 전처리   | | 엔지니어 | | Pod      | | Pod      |          |
|  | Pod      | | 링 Pod   | |          | |          |          |
|  +----------+ +----------+ +----------+ +----------+          |
+------------------------------------------------------------------+
```

### 2.2 Kubeflow Pipelines Python DSL 예시

```python
from kfp import dsl
from kfp.components import func_to_container_op

# 컴포넌트 정의
@func_to_container_op
def preprocess_data(data_path: str) -> str:
    """데이터 전처리 컴포넌트"""
    import pandas as pd
    df = pd.read_csv(data_path)
    # 전처리 로직...
    output_path = "/mnt/data/processed.parquet"
    df.to_parquet(output_path)
    return output_path

@func_to_container_op
def train_model(data_path: str, epochs: int = 10) -> str:
    """모델 학습 컴포넌트"""
    # 학습 로직...
    model_path = "/mnt/models/model.pkl"
    return model_path

@func_to_container_op
def evaluate_model(model_path: str, threshold: float = 0.9) -> bool:
    """모델 평가 컴포넌트"""
    # 평가 로직...
    return accuracy >= threshold

# 파이프라인 정의 (DAG)
@dsl.pipeline(
    name='ML Training Pipeline',
    description='전처리 -> 학습 -> 평가 -> 배포'
)
def ml_pipeline(data_path: str, epochs: int = 10):
    # 단계 1: 데이터 전처리
    preprocess_task = preprocess_data(data_path=data_path)

    # 단계 2: 모델 학습 (전처리 완료 후 실행)
    train_task = train_model(
        data_path=preprocess_task.output,
        epochs=epochs
    )

    # 단계 3: 모델 평가
    eval_task = evaluate_model(
        model_path=train_task.output
    )

    # 단계 4: 조건부 배포 (평가 통과 시만)
    with dsl.Condition(eval_task.output == 'true'):
        deploy_task = deploy_model(
            model_path=train_task.output
        )
```

### 2.3 Katib (하이퍼파라미터 최적화)

```
+-----------------------------------------------------------------+
|                    Katib 아키텍처                                |
+------------------------------------------------------------------+
|                                                                  |
|  목표 메트릭: Maximize Accuracy                                  |
|  하이퍼파라미터 검색 공간:                                       |
|    learning_rate: [0.0001, 0.01] (log uniform)                  |
|    batch_size: [16, 32, 64, 128] (discrete)                     |
|    optimizer: ['adam', 'sgd', 'rmsprop'] (categorical)          |
|                                                                  |
|  Katib Controller ---> 검색 알고리즘 선택                        |
|                                                                  |
|  +-------------------------------------------------+           |
|  |  Trial 1: lr=0.001, bs=32, opt=adam -> Acc=0.91 |           |
|  |  Trial 2: lr=0.01,  bs=64, opt=sgd  -> Acc=0.88 |           |
|  |  Trial 3: lr=0.0001,bs=16, opt=adam -> Acc=0.93 |           |
|  |  ...                                             |           |
|  |  Trial N: lr=0.002, bs=32, opt=adam -> Acc=0.95 | <- 최적   |
|  +-------------------------------------------------+           |
+------------------------------------------------------------------+
```

#### Katib 검색 알고리즘 비교

| 알고리즘 | 원리 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| <strong>Grid Search</strong> | 모든 조합 탐색 | 완전 탐색 | 경우의 수 기하급수적 증가 | 소수 파라미터 |
| **Random Search** | 무작위 샘플링 | 빠름, 효율적 | 보장 없음 | 대부분 기본 선택 |
| **Bayesian Optimization** | 사전 정보 활용 | 효율적 수렴 | 계산 비용 높음 | 비싼 실험 |
| **HyperBand** | 조기 종료 기반 | 빠른 탐색 | 학습 곡선 필요 | 딥러닝 |
| <strong>NAS (Neural Architecture Search)</strong> | 네트워크 구조 탐색 | 자동 아키텍처 | 매우 높은 비용 | 대규모 딥러닝 |

### 2.4 KServe (모델 서빙)

```
+-----------------------------------------------------------------+
|                     KServe 아키텍처                              |
+------------------------------------------------------------------+
|                                                                  |
|  InferenceService (CRD)                                         |
|  +------------------------------------------------------+      |
|  |  Transformer (선택)    Predictor          Explainer  |      |
|  |  전처리/후처리 ->       (모델 서빙)    ->   예측 설명  |      |
|  |  Triton/TF Serving /   SHAP/LIME                     |      |
|  |  PyTorch/Sklearn       (선택)                        |      |
|  +------------------------------------------------------+      |
|                                                                  |
|  지원 프레임워크:                                                |
|  +-----------------------------------------------------+       |
|  | TensorFlow | PyTorch | Sklearn | XGBoost | LightGBM |       |
|  | ONNX       | Triton  | HuggingFace | MLflow | Custom|       |
|  +-----------------------------------------------------+       |
|                                                                  |
|  서빙 기능:                                                      |
|  - REST/gRPC 자동 엔드포인트                                    |
|  - 카나리 배포 (canaryTrafficPercent)                           |
|  - 자동 스케일링 (KNative 기반)                                 |
|  - 배치 추론 (InferenceGraph)                                   |
+------------------------------------------------------------------+
```

📢 **섹션 요약 비유**: Kubeflow Pipelines는 자동화된 공장 조립 라인과 같다. 각 작업(컴포넌트)은 독립적인 컨테이너 기계이고, DAG는 조립 순서도이며, Katib은 최적 재료 배합(하이퍼파라미터)을 자동으로 찾아주는 레시피 최적화 로봇이다.

---

## Ⅲ. 비교 및 연결

### 3.1 Kubeflow vs MLflow vs SageMaker

| 항목 | Kubeflow | MLflow | AWS SageMaker |
|:---|:---|:---|:---|
| **유형** | 오픈소스 플랫폼 | 오픈소스 라이브러리 | 클라우드 관리형 |
| **파이프라인** | 완전 지원 (KFP) | 제한적 | 완전 지원 |
| **실험 추적** | MLflow 연동 | 핵심 기능 | SageMaker Experiments |
| <strong>AutoML</strong> | Katib | 없음 | Autopilot |
| **모델 서빙** | KServe | mlflow serve | SageMaker Endpoints |
| **인프라 요구** | 쿠버네티스 클러스터 | 최소 | AWS 계정 |
| **비용** | 인프라 비용만 | 무료 | 사용량 기반 |
| <strong>온프레미스</strong> | 완전 지원 | 완전 지원 | 제한적 |
| **학습 곡선** | 가파름 (K8s 지식 필요) | 완만 | 중간 |

### 3.2 Training Operators (분산 학습)

```
TFJob (분산 TensorFlow 학습):
+---------------------------------------------+
|  TFJob                                       |
|  +-- Chief Pod (1개): 마스터 워커           |
|  +-- Worker Pod (4개): 데이터 병렬 학습     |
|  +-- PS Pod (2개): 파라미터 서버            |
+---------------------------------------------+

PyTorchJob (분산 PyTorch 학습):
+---------------------------------------------+
|  PyTorchJob                                  |
|  +-- Master Pod (1개)                       |
|  +-- Worker Pod (N개): DDP 분산 학습        |
+---------------------------------------------+
```

### 3.3 Kubeflow vs Airflow 비교

| 항목 | Kubeflow Pipelines | Apache Airflow |
|:---|:---|:---|
| **목적** | ML 파이프라인 특화 | 범용 워크플로우 |
| **실행 단위** | 쿠버네티스 Pod | 다양한 Executor |
| **ML 특화** | 아티팩트 추적, 시각화 | 없음 (플러그인 필요) |
| **확장성** | 쿠버네티스 스케일링 | CeleryExecutor/K8s |
| **재현성** | 컨테이너 기반 완전 | 환경 의존 |
| **사용 편의성** | 어려움 | 상대적으로 쉬움 |

📢 **섹션 요약 비유**: Kubeflow vs Airflow 비교는 ML 전문 병원(Kubeflow)과 종합 병원(Airflow)의 차이다. ML 전문 병원은 ML 치료에 특화된 장비(아티팩트 추적, AutoML)를 갖추고 있고, 종합 병원은 모든 과가 있어 다용도로 활용 가능하다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 Kubeflow 배포 옵션

| 옵션 | 설명 | 적합 환경 |
|:---|:---|:---|
| **kubeflow/manifests** | 공식 Kustomize 배포 | 온프레미스, GKE |
| **Kubeflow on AWS** | EKS 기반 최적화 | AWS 환경 |
| **Kubeflow on GCP** | GKE 기반 최적화 | GCP 환경 |
| **Charmed Kubeflow (Ubuntu)** | Ubuntu 기반 간편 설치 | Ubuntu K8s |
| <strong>Vertex AI Pipelines</strong> | Kubeflow Pipelines API 호환 | GCP 완전 관리형 |

### 4.2 심화 학습 핵심 포인트

<strong>Q. Kubeflow의 핵심 컴포넌트와 각각의 역할을 설명하시오.</strong>

| 컴포넌트 | 역할 |
|:---|:---|
| **Kubeflow Pipelines** | Python DSL로 ML 워크플로우 DAG 정의·실행, 아티팩트 추적 |
| **Katib** | 하이퍼파라미터 최적화 (Grid, Random, Bayesian, HyperBand) |
| **KServe** | 멀티 프레임워크 모델 서빙 (REST/gRPC, 카나리 배포) |
| <strong>Training Operators</strong> | 분산 학습 (TFJob, PyTorchJob) |
| **Notebooks** | JupyterHub 기반 팀 협업 노트북 환경 |
| **Central Dashboard** | 모든 컴포넌트 통합 UI |

<strong>Q. Katib의 하이퍼파라미터 최적화 알고리즘(Bayesian vs Random Search)을 비교하시오.</strong>

- **Random Search**: 균일 분포로 무작위 샘플링, 구현 단순, 병렬 실행 용이, 검색 공간이 넓을 때 효과적
- **Bayesian Optimization**: 이전 시도 결과를 사전 확률로 활용하여 다음 시도 위치를 결정, 실험 횟수가 적을 때 효율적, 비싼 학습(수 시간) 실험에 적합
- **HyperBand**: 조기 종료(Early Stopping)를 통해 성능 낮은 조합을 빠르게 제거, 대규모 탐색에 효율적

### 4.3 Kubeflow 도입 시 체크리스트

```
+--------------------------------------------------------------+
|            Kubeflow 도입 체크리스트                           |
+--------------------------------------------------------------+
|  인프라                                                       |
|  □ 쿠버네티스 1.21+ 클러스터 준비                            |
|  □ GPU 노드 (nvidia-device-plugin) 설치                      |
|  □ 스토리지 클래스 (NFS, Ceph) 구성                         |
|  □ 로드 밸런서 또는 Istio Ingress 설정                      |
+--------------------------------------------------------------+
|  팀 역량                                                     |
|  □ 쿠버네티스 운영 경험 (최소 1명)                           |
|  □ Python + Docker 역량                                      |
|  □ Kubeflow Pipelines SDK 학습                               |
+--------------------------------------------------------------+
|  대안 검토                                                   |
|  □ 클라우드 관리형 (Vertex AI, SageMaker) 비용 비교          |
|  □ Apache Airflow로 충분한지 검토                            |
+--------------------------------------------------------------+
```

📢 **섹션 요약 비유**: Kubeflow 도입은 수제 요리 공방을 산업용 자동화 식품 공장으로 전환하는 것과 같다. 처음엔 설비 투자(K8s 구축)가 크지만, 대량 생산 단계에서는 수동 대비 압도적인 효율성과 재현성을 제공한다. 단, 공장 운영 전문가(K8s 엔지니어)가 반드시 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 Kubeflow 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 |
|:---|:---|:---|:---|
| **파이프라인 재현성** | 환경 의존, 불확실 | 컨테이너 기반 완전 재현 | 100% 재현 가능 |
| **자원 활용률** | GPU 유휴 시간 많음 | 쿠버네티스 자동 스케줄링 | GPU 활용률 30% 향상 |
| **HPO 자동화** | 수동 실험 반복 | Katib 자동 탐색 | 실험 시간 60% 단축 |
| **모델 서빙** | 프레임워크별 개별 서버 | KServe 통합 | 운영 복잡도 감소 |
| **팀 협업** | 개인 환경 의존 | 공유 클러스터 | 실험 공유 용이 |

### 5.2 결론

Kubeflow는 ML 워크로드를 클라우드 네이티브 방식으로 운영하려는 조직의 MLOps 플랫폼 표준이다. 파이프라인 자동화(KFP), 하이퍼파라미터 최적화(Katib), 멀티 프레임워크 서빙(KServe)의 통합이 ML 생산성을 크게 향상시키지만, 쿠버네티스 운영 역량이 선행 조건이다.

📢 **섹션 요약 비유**: Kubeflow는 ML 버전의 항공 관제 시스템과 같다. 수많은 ML 파이프라인 비행기(Pipelines)가 이착륙하고, 최적 연료 배합(Katib)을 자동 계산하며, 승객(추론 요청)을 가장 빠른 경로로 안내하는(KServe) 완전 자동화 관제탑이다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 기반 인프라 | Kubernetes (쿠버네티스) | Kubeflow의 실행 환경 |
| 핵심 컴포넌트 | Kubeflow Pipelines | DAG 기반 ML 파이프라인 |
| 핵심 컴포넌트 | Katib | 하이퍼파라미터 자동 최적화 |
| 핵심 컴포넌트 | KServe | 멀티 프레임워크 모델 서빙 |
| 비교 도구 | Apache Airflow | 범용 워크플로우 오케스트레이션 |
| 비교 도구 | MLflow | 실험 추적 + 모델 레지스트리 |
| 비교 도구 | AWS SageMaker | 클라우드 관리형 ML 플랫폼 |
| 상위 개념 | MLOps | Kubeflow는 MLOps 실행 플랫폼 |
| 연관 | CT (Continuous Training) | Kubeflow Pipelines로 CT 구현 |
| 연관 | 분산 학습 | TFJob, PyTorchJob 분산 학습 지원 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. Kubeflow는 LEGO 공장 조립 라인 같아요. 각 부품(컨테이너)은 독립적으로 만들고, 조립 순서(DAG)에 따라 자동으로 완성 제품(학습된 모델)을 만들어요.
2. Katib은 레시피 최적화 로봇이에요. 소금을 얼마나 넣을지(하이퍼파라미터) 여러 번 시험해서 가장 맛있는 비율(최적 파라미터)을 자동으로 찾아줘요.
3. KServe는 다국어 통역사 같아요. TensorFlow로 만들든 PyTorch로 만들든 어떤 모델이든 하나의 API로 통역해서 사람들이 이용할 수 있게 해줘요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 ML 실험 (노트북 기반)
    |
    v
ML 파이프라인 자동화
    +-► Kubeflow Pipelines: K8s 기반 DAG 파이프라인
    +-► Katib: 하이퍼파라미터 자동 최적화
    +-► KServe: 멀티 프레임워크 모델 서빙
    |
    v
컨테이너 기반 재현성 (Docker + K8s)
    |
    v
SageMaker Pipelines · Vertex AI Pipelines (클라우드 관리형)
    |
    v
LLMOps 파이프라인: 프롬프트 관리 · RAG · PEFT 스케줄링
```
