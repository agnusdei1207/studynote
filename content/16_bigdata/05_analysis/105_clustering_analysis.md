---
title: "Clustering Analysis"
date: "2024-03-20"
tags:
  - "studynote-bigdata"
weight: 105
---
## 핵심 인사이트 (3줄 요약)
- <strong>비지도 학습(Unsupervised):</strong> 정답(Label)이 없는 상태에서 데이터 간의 유사성(Similarity/Distance)만을 기준으로 그룹을 나누는 탐색적 기법.
- <strong>응집도와 분리도:</strong> 같은 군집 내의 데이터는 가깝게(Intra-cluster), 서로 다른 군집 간의 데이터는 멀게(Inter-cluster) 배치하는 것이 핵심 목표임.
- <strong>도메인 통찰:</strong> 고객 세분화나 이미지 분할처럼 대규모 데이터 내에 숨겨진 구조와 패턴을 발견하는 데 탁월함.

### Ⅰ. 개요 (Context & Background)
- **정의:** 데이터 포인트들 간의 거리를 계산하여 유사한 속성을 가진 개체들을 하나의 집단(Cluster)으로 묶는 분석 방법론임.
- **활용 동기:** 데이터의 특징이 너무 많거나 정답이 명확하지 않을 때, 우선적으로 데이터의 성질을 파악하기 위한 전처리 단계로 활용됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **거리 측정 방식:** Euclidean, Manhattan, Cosine Similarity 등.
- <strong>Bilingual ASCII Diagram:</strong>
```text
[Clustering Process & Results / 군집화 프로세스 및 결과]

   Before Clustering             After Clustering (K-Means)
   (Unlabeled Data)              (Segmented Groups)
   ----------------              ------------------
     .  .   .  .                  ( G1 )      ( G3 )
   .  .   .  .  .                  .  .        .  .
     .  .   .                     .  .          .
   .  .  .  .  .                  ( G2 )
                                   .  .  .

[Major Algorithms / 주요 알고리즘]
1. K-Means: Partitioning based on Centroids (K clusters)
2. Hierarchical: Tree-based grouping (Dendrogram)
3. DBSCAN: Density-based (High density vs Noise)
4. Gaussian Mixture (GMM): Probability-based (Normal Dist.)
```
- **최적의 K 찾기:** Elbow Method (SSE 감소폭), Silhouette Score (응집도/분리도 지수).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | K-Means 군집화 | DBSCAN (밀도 기반) | 계층적 군집화 |
| :--- | :--- | :--- | :--- |
| **군집 형성 방식** | 중심점(Centroid) 기준 | 데이터 밀도 기준 | 계층적 트리 구조 |
| **장점 (Pros)** | 연산이 매우 빠름 | 비정형 모양(Crescent) 가능 | 군집 수를 미리 정할 필요 없음 |
| **단점 (Cons)** | K값을 미리 정해야 함 | 파라미터(eps) 설정 민감 | 대용량 데이터 시 연산 부하 |
| <strong>이상치(Outlier) 처리</strong> | 취약 (평균 왜곡) | 강함 (Noise로 자동 분류) | 중간 |
| **비유 (Analogy)** | 반장 선거하기 | 사람들 모여있는 곳 찾기 | 가족 족보 그리기 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>군집 타당성(Validation) 평가:</strong> 지도 학습과 달리 정답이 없으므로 <strong>실루엣 계수</strong>가 0.5 이상인지 확인하고, 각 군집의 비즈니스적 의미(예: VIP 고객, 이탈 위험군)를 해석하는 과정이 필수적임.
- <strong>차원의 저주(Curse of Dimensionality):</strong> 변수가 너무 많으면 거리 계산의 의미가 사라지므로, 군집화 전 <strong>PCA</strong>나 <strong>t-SNE</strong>를 통한 차원 축소 전처리가 실무적 권고 사항임.
- <strong>하이브리드 전략:</strong> 군집화 결과를 새로운 변수(Label)로 사용하여 지도 학습 모델에 입력값으로 넣는 파이프라인(Stacking) 구성도 효과적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- <strong>초개인화 서비스:</strong> 타겟 마케팅이나 추천 시스템의 기초가 되어 고객 만족도를 극대화함.
- <strong>데이터 품질 향상:</strong> 이상치 탐지를 통해 데이터 정제(Cleaning)의 정확도를 높임.
- **결론:** 군집화는 빅데이터 분석의 출발점이며, 최근에는 딥러닝 임베딩 벡터와 결합하여 비정형 데이터(이미지, 텍스트)의 고차원 군집화로 발전하고 있음.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Unsupervised Learning, Data Mining
- **하위 개념:** K-Means++, Dendrogram, Silhouette Score
- **연관 기술:** PCA (Dimensionality Reduction), Mahalanobis Distance, C고객 Segmentation

### 📈 관련 키워드 및 발전 흐름도

```text
[비지도 학습 (Unsupervised Learning)]
    |
    v
[클러스터링 (Clustering)]
    |
    v
[K-평균 (K-Means)]
    |
    v
[실루엣 계수 (Silhouette Score)]
```

이 흐름도는 비지도 학습에서 클러스터링과 K-평균, 실루엣 계수로 평가가 이어지는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. **장난감 정리 비유:** 뒤섞인 블록들을 색깔별로 모으거나, 크기가 비슷한 인형끼리 모아서 정리 상자에 담는 거예요.
2. **운동장 비유:** 운동장에 모인 학생들 중에서 친한 친구들끼리 동그랗게 모여 보라고 하는 것과 같아요.
3. **옷 정리 비유:** 계절에 맞춰 여름 옷은 여름 옷끼리, 겨울 옷은 겨울 옷끼리 옷장에 따로 넣어두는 마법이에요.
