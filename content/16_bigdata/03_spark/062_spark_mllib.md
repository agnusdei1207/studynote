---
title: "Spark Mllib"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 62
---
## 핵심 인사이트 (3줄 요약)
1. <strong>스파크 MLlib (Machine Learning Library)</strong>는 대규모 분산 환경에서 동작하는 고성능 머신러닝 알고리즘 및 유틸리티를 제공하는 스파크의 핵심 컴포넌트이다.
2. Spark SQL의 DataFrame API를 기반으로 하는 <strong>'ML 파이프라인(ML Pipelines)'</strong> 아키텍처를 도입하여, 데이터 변환부터 모델 학습/평가까지의 과정을 표준화한다.
3. 반복적(Iterative) 연산이 많은 머신러닝 특성에 맞춰 <strong>인메모리 연산</strong>을 수행하므로, 기존 MapReduce 기반 도구보다 최대 100배 빠른 성능을 제공한다.

---

### Ⅰ. 개요 (Context & Background)
- **정의**: 스파크 에코시스템 내에서 분산 분류, 회귀, 군집, 추천 시스템 및 차원 축소 알고리즘을 수행하기 위한 라이브러리이다.
- **배경**: 단일 노드 머신러닝 라이브러리(scikit-learn 등)로는 처리 불가능한 '테라바이트(TB) 급 대용량 데이터'를 분산 병렬 학습하기 위해 고안되었다.
- **주요 활용**: 대규모 사용자 대상의 상품 추천 시스템, 실시간 로그 기반 사기 탐지(FDS), 대규모 텍스트 데이터의 토픽 모델링 등 빅데이터 분석의 최전선에서 활용된다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. ML 파이프라인(Pipeline) 구조
```text
[ Raw Data (DataFrame) ]
      |
      V [ Transformer ] (e.g., Tokenizer, Scaler) --> [ Transformed Data ]
      |
      V [ Estimator ] (e.g., Logistic Regression) --> [ Model (Transformer) ]
      |
      V [ Evaluator ] (e.g., BinaryClassificationEvaluator) --> [ Performance Metric ]
```

#### 2. 핵심 알고리즘 카테고리
- <strong>Classification &amp; Regression</strong>: 로지스틱 회귀, 랜덤 포레스트, GBT(Gradient Boosted Trees), SVM 등
- <strong>Collaborative Filtering</strong>: ALS(Alternating Least Squares) 기반의 대규모 추천 시스템 알고리즘
- <strong>Clustering</strong>: K-means, Gaussian Mixture, LDA(Latent Dirichlet Allocation) 등
- <strong>Dimensionality Reduction</strong>: PCA(주성분 분석), SVD(특이값 분해)

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Scikit-learn (Python) | Spark MLlib |
| :--- | :--- | :--- |
| <strong>처리 데이터 규모</strong> | 단일 노드 메모리 한계 (GB 수준) | 클러스터 분산 메모리 (TB/PB 수준) |
| **학습 방식** | 단일 CPU/GPU 위주 학습 | 수백 개의 워커 노드 병렬 학습 |
| <strong>API 편의성</strong> | 매우 높음, 라이브러리 풍부 | ML Pipeline 도입 후 매우 개선됨 |
| **병목 지점** | 연산 속도 및 메모리 부족 | 네트워크 셔플링(Shuffle) 발생 |
| **사용 사례** | 모델 연구 및 중소형 데이터 | 대규모 서비스 운영 및 배치 학습 |

---

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>데이터 엔지니어링의 중요성</strong>: MLlib 성능의 80%는 학습 알고리즘보다 앞단의 데이터 전처리(`VectorAssembler` 등)와 피처 엔지니어링 효율화에서 결정된다.
- <strong>하이퍼파라미터 튜닝 최적화</strong>: `CrossValidator`를 사용한 대규모 병렬 튜닝 시 클러스터 자원이 급격히 소모될 수 있으므로, 그리드 서치(Grid Search) 범위를 신중히 설정해야 한다.
- <strong>모델 서빙(Serving) 전략</strong>: 학습된 MLlib 모델을 실시간 추론에 사용할 경우, Spark 클러스터 오버헤드를 피하기 위해 PMML이나 MLeap 같은 표준 포맷으로 익스포트하여 경량 서버에서 서빙하는 방식이 선호된다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 데이터 분석가가 복잡한 분산 프로그래밍 지식 없이도 고성능 대규모 머신러닝 시스템을 직접 구축하고 배포할 수 있게 한다.
- **결론**: MLlib은 빅데이터 플랫폼으로서의 스파크의 가치를 완성하는 조각이다. 향후 딥러닝 프레임워크와의 연동(Spark deep learning pipelines) 및 분산 학습 표준화를 통해 데이터 과학의 대중화를 이끌 핵심 기술로 남을 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
1. <strong>Transformer</strong>: 데이터를 다른 데이터로 변환하는 알고리즘 (추론 포함)
2. **Estimator**: 데이터를 학습하여 모델(Transformer)을 생성하는 알고리즘
3. <strong>ALS (Alternating Least Squares)</strong>: 행렬 분해 기반의 추천 시스템 핵심 알고리즘

---

### 📈 관련 키워드 및 발전 흐름도

```text
[원시 피처 데이터 (Raw Feature Data) — DataFrame·RDD로 메모리 로딩]
    |
    v
[피처 엔지니어링 (Feature Engineering) — MLlib Pipeline으로 전처리·변환]
    |
    v
[모델 학습 (Model Training) — 분산 클러스터 병렬 알고리즘 수행]
    |
    v
[모델 평가 (Model Evaluation) — CrossValidator·TrainValidationSplit]
    |
    v
[모델 배포 (Model Serving) — MLflow·Spark Structured Streaming 연동]
```

이 흐름은 Spark MLlib가 피처 전처리부터 분산 학습·평가·서빙까지 머신러닝 파이프라인을 일원화하는 과정을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. "전교생 수만 명의 키와 몸무게 데이터를 보고, 어떤 아이가 운동을 잘할지 한꺼번에 알아맞히는 똑똑한 로봇 선생님이에요."
2. "혼자서 공부하는 게 아니라, 친구 로봇 수백 명과 함께 문제를 나눠서 풀기 때문에 아주 빠르게 정답을 찾아요."
3. "이게 바로 커다란 데이터를 공부해서 미래를 예측하는 '엠엘립'이라는 기술이랍니다!"
