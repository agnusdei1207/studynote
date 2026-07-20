---
title: "Kubeflow Mlops Orchestration"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 113
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubeflow는 Kubernetes 위에서 <strong>ML 워크플로 전체(데이터 전처리 -> 학습 -> 하이퍼파라미터 튜닝 -> 서빙 -> 모니터링)</strong>를 선언적으로 오케스트레이션하는 CNCF 기반 <strong>MLOps 플랫폼</strong>이다.
> 2. **가치**: 주피터 노트북에서 실험한 모델을 프로덕션에 올리려면 Docker화·스케줄링·GPU 할당·A/B 서빙 등 <strong>"ML의 마지막 1마일"</strong>을 해결해야 하며, Kubeflow Pipelines가 이를 <strong>DAG(방향 비순환 그래프)로 자동화</strong>한다.
> 3. **판단 포인트**: Kubeflow는 K8s 운영 역량이 전제되므로 **진입 장벽이 높으며**, 소규모 팀에는 Vertex AI(GCP)·SageMaker(AWS) 같은 관리형 MLOps가 더 적합할 수 있다.

---

## Ⅰ. 개요 및 필요성

데이터 과학자의 87%가 "주피터 노트북에서 잘 되던 모델이 프로덕션에서 안 된다"고 말한다. 이 간극을 <strong>"ML 기술 부채(Hidden Technical Debt)"</strong>라 하며, Kubeflow는 이를 해소한다.

```text
+-------------------------------------------------------+
|    Kubeflow 핵심 컴포넌트 아키텍처                     |
+-------------------------------------------------------+
|  +----------+  +----------+  +----------+            |
|  | Notebooks|  | Pipelines|  |  Katib   |            |
|  | (실험)   |  | (파이프  |  | (HP 튜닝)|            |
|  |          |  |  라인)   |  |          |            |
|  +----+-----+  +----+-----+  +----+-----+            |
|       |              |              |                 |
|       v              v              v                 |
|  +--------------------------------------+             |
|  |        Kubernetes Cluster           |             |
|  |  GPU Node Pool + CPU Node Pool      |             |
|  +----------+---------------------------+             |
|             |                                         |
|  +----------v----------+                              |
|  |   KServe (모델 서빙) |  Canary / A-B 배포         |
|  +---------------------+                              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Kubeflow는 ML 공장의 <strong>컨베이어 벨트 시스템</strong>이다. 원재료(데이터) 투입 -> 가공(전처리) -> 조립(학습) -> 품질 검사(평가) -> 출하(서빙)가 자동으로 흘러간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 컴포넌트

| 컴포넌트 | 역할 | 비유 |
|:---|:---|:---|
| **Notebooks** | 주피터 노트북 서버 (GPU 자동 할당) | 실험실 |
| **Pipelines** | 전처리->학습->평가 DAG 오케스트레이션 | 컨베이어 벨트 |
| **Katib** | 하이퍼파라미터 자동 튜닝 (Bayesian/Random) | 실험 계획 로봇 |
| **KServe** | 모델 서빙 (Canary·A/B·오토스케일링) | 제품 배송 |
| <strong>Training Operators</strong> | TFJob·PyTorchJob (분산 학습) | GPU 병렬 공장 |

- **📢 섹션 요약 비유**: Katib는 요리사(모델)에게 "소금을 얼마나 넣어야 맛있는지" 수백 번 시도해주는 <strong>AI 미식가</strong>다.

---

## Ⅲ. 비교 및 연결

| 비교 | Kubeflow | SageMaker | Vertex AI |
|:---|:---|:---|:---|
| **인프라** | 자체 K8s | AWS 관리형 | GCP 관리형 |
| **유연성** | **최고** | 중간 | 중간 |
| **운영 부담** | **높음** | 낮음 | 낮음 |
| <strong>벤더 종속</strong> | 없음 (OSS) | AWS | GCP |
| **적합** | 대규모, K8s 역량 보유 | AWS 중심 | GCP 중심 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 도입 판단 기준
1. **K8s 운영 팀 존재**: 있으면 Kubeflow, 없으면 관리형.
2. **멀티클라우드 요구**: 있으면 Kubeflow (벤더 중립).
3. <strong>GPU 워크로드 규모</strong>: 대규모 분산 학습 -> Kubeflow Training Operators.

### 안티패턴
- <strong>5인 팀이 Kubeflow 직접 운영</strong>: K8s 운영 부담 > ML 개발 시간 -> 관리형 추천.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 ML 배포 | Kubeflow | 개선 |
|:---|:---|:---|:---|
| 모델 배포 주기 | 월 1회 | **일 수회** | CI/CD 수준 |
| 실험 추적 | 수동 엑셀 | <strong>자동 메타데이터 저장</strong> | 재현성 확보 |
| HP 튜닝 | 수동 그리드 | **Katib 자동 (Bayesian)** | 최적 파라미터 자동 탐색 |

Kubeflow는 <strong>LLM 시대의 Fine-tuning 파이프라인·RAG 서빙</strong>과 결합하여 GenAI Ops 플랫폼으로 진화 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Kubeflow Pipelines</strong> | ML 워크플로 DAG 오케스트레이션 |
| **Katib** | 하이퍼파라미터 자동 튜닝 |
| **KServe** | K8s 네이티브 모델 서빙 (Canary/A-B) |
| <strong>MLflow</strong> | 실험 추적 경쟁 도구 (경량) |
| <strong>MLOps</strong> | Kubeflow가 구현하는 상위 규율 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 ML 배포 (주피터 -> Docker -> 수동 서빙)]
    |
    v
[Kubeflow 0.x (2018, Google) — K8s 기반 ML 플랫폼 시작]
    |
    v
[Kubeflow Pipelines v2 (2022~) — DAG 성숙, Katib 통합]
    |
    v
[KServe (2021~) — Knative 기반 모델 서빙 표준화]
    |
    v
[현재: GenAI Ops — LLM Fine-tuning·RAG 파이프라인 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Kubeflow는 공장의 <strong>자동 컨베이어 벨트</strong>예요. 재료(데이터)를 넣으면 완제품(AI 모델)이 나와요.
2. Katib라는 로봇은 **"소금 얼마, 설탕 얼마"를 수백 번 바꿔가며** 제일 맛있는 레시피를 찾아줘요.
3. 다 만들어진 제품은 KServe라는 <strong>택배 시스템</strong>이 고객에게 배달(서빙)해준답니다!
