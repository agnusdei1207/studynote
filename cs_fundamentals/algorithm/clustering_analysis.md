# 군집분석 (Clustering Analysis)

## 1. 개요 및 정의

**군집분석(Clustering Analysis)** 또는 **군집화(Clustering)**는 비지도학습(Unsupervised Learning)의 대표적인 기법으로, 사전에 레이블(Label)이 없는 데이터를 유사성(Similarity)을 기준으로 여러 개의 그룹인 **군집(Cluster)**으로 분류하는 데이터 마이닝 기법이다. 군집 내의 데이터는 서로 유사하고, 군집 간의 데이터는 상이하게 배치되는 것을 목표로 한다.

---

## 2. 등장 배경 및 필요성

### 2.1 역사적 발전

| 시기 | 주요 발전 | 내용 |
|------|----------|------|
| **1950-1960년대** | 초기 군집 알고리즘 태동 | K-means, Hierarchical Clustering 등 기본 알고리즘 개발 |
| **1970-1980년대** | 이론적 정립 | DBSCAN(1996) 등 밀도 기반 알고리즘 개발, 거리 척도 연구 활성화 |
| **1990-2000년대** | 고차원 데이터 대응 | Spectral Clustering, Gaussian Mixture Model(GMM) 등 확률적 모델 도입 |
| **2010년대 이후** | 딥러닝 융합 | Deep Clustering, Self-Organizing Maps(SOM) 최적화, 대규모 데이터 처리 |

### 2.2 필요성

1. **데이터 구조 발견 (Data Structure Discovery):** 명시적 레이블이 없는 데이터셋에서 잠재적인 패턴과 구조를 식별
2. **데이터 압축 (Data Compression):** 군집 중심(Cluster Centroid)을 사용하여 데이터의 차원 축소 및 저장 공간 절약
3. **이상치 탐지 (Anomaly Detection):** 어떤 군집에도 속하지 않는 데이터를 이상치로 식별
4. **시장 세분화 (Market Segmentation):** 고객 행동, 소비 패턴 등을 기반으로 타겟 마케팅 전략 수립
5. **이미지 세분화 (Image Segmentation):** 컴퓨터 비전에서 픽셀 단위 군집화를 통해 객체 분리

---

## 3. 군집분석의 핵심 구성 요소

### 3.1 거리 척도 (Distance Metrics)

군집분석의 기초는 데이터 간의 유사성/비유사성을 정량화하는 거리 척도이다.

| 거리 척도 | 수학적 표현 | 특징 | 사용 사례 |
|----------|-------------|------|----------|
| **유클리드 거리 (Euclidean Distance)** | $d(x,y) = \sqrt{\sum_{i=1}^n (x_i - y_i)^2}$ | 직선 거리, 직관적이지만 고차원에서 차원의 저주 발생 | K-means, 일반적 군집화 |
| **맨해튼 거리 (Manhattan Distance)** | $d(x,y) = \sum_{i=1}^n \|x_i - y_i\|$ | 격자형 이동 거리, 이상치에 덜 민감 | 고차원 스파스 데이터 |
| **코사인 유사도 (Cosine Similarity)** | $cos(θ) = \frac{x \cdot y}{\|x\| \|y\|}$ | 벡터 방향 유사성, 크기 무시 | 텍스트 마이닝, NLP |
| **마할라노비스 거리 (Mahalanobis Distance)** | $d(x,y) = \sqrt{(x-y)^T Σ^{-1} (x-y)}$ | 변수 간 상관관계 고려, 스케일 불변성 | 다변량 통계, 이상치 탐지 |
| **자카드 거리 (Jaccard Distance)** | $d(A,B) = 1 - \frac{|A \cap B|}{|A \cup B|}$ | 집합 간 차이 | 텍스트, 범주형 데이터 |

### 3.2 군집 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| **파티셔닝 군집 (Partitioning Clustering)** | 데이터를 K개의 비중첩 군집으로 분할 | K-means, K-medoids |
| **계층적 군집 (Hierarchical Clustering)** | 트리 구조(Dendrogram)로 군집 관계 표현 | Agglomerative, Divisive |
| **밀도 기반 군집 (Density-Based Clustering)** | 데이터 밀도가 높은 영역을 군집으로 식별 | DBSCAN, OPTICS |
| **그리드 기반 군집 (Grid-Based Clustering)** | 데이터 공간을 그리드로 분할하여 군집화 | STING, CLIQUE |
| **모델 기반 군집 (Model-Based Clustering)** | 확률 모델을 가정하여 군집화 | GMM, EM 알고리즘 |
| **그래프 기반 군집 (Graph-Based Clustering)** | 그래프 이론을 활용하여 군집 식별 | Spectral Clustering, CURE |

---

## 4. 주요 군집 알고리즘 및 비교

### 4.1 대표적 군집 알고리즘 상세 분석

#### 4.1.1 K-means 알고리즘

**핵심 원리:** 사전에 정의된 K개의 중심점(Centroid)을 기준으로 데이터를 할당하고, 중심점을 반복적으로 업데이트

**알고리즘 절차:**
```
1. K개의 초기 중심점을 무작위로 선택
2. 각 데이터 포인트를 가장 가까운 중심점에 할당
3. 각 군집의 새로운 중심점(평균) 계산
4. 중심점이 수렴할 때까지 2-3단계 반복
```

**수학적 최적화:**
$$J = \sum_{j=1}^K \sum_{i \in C_j} \|x_i - μ_j\|^2$$

- $C_j$: j번째 군집
- $μ_j$: j번째 군집의 중심점
- $J$: 군집 내 제곱 오차 합(Sum of Squared Errors, SSE) 최소화

**장단점:**
| 장점 | 단점 |
|------|------|
| 구현이 간단하고 이해하기 쉬움 | K값을 사전에 지정해야 함 |
| 대규모 데이터에 적용 가능 | 초기 중심점에 따라 결과가 달라짐 (Local Optimum) |
| 볼록(Convex) 형태 군집에 효과적 | 비구형(Non-convex) 군집 식별 불가 |
| 계산 복잡도가 낮음 ($O(nkt)$) | 이상치(Outlier)에 민감 |

**시간 복잡도:** $O(n \times k \times t \times d)$
- $n$: 데이터 포인트 수
- $k$: 군집 수
- $t$: 반복 횟수
- $d$: 차원 수

---

#### 4.1.2 DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

**핵심 원리:** 데이터 밀도가 연속적인 영역을 하나의 군집으로 정의, 노이즈(Noise) 자동 식별

**핵심 파라미터:**
- **ε (Epsilon, 반경):** 이웃 탐색 반경
- **MinPts (Minimum Points):** 핵심점(Core Point)이 되기 위한 최소 이웃 수

**점의 분류:**
```
[Core Point]     - ε 반경 내에 MinPts 이상의 이웃을 가진 점
[Border Point]   - Core Point의 이웃이지만 자신은 Core Point가 아닌 점
[Noise Point]    - Core Point도 Border Point도 아닌 점 (이상치)
```

**알고리즘 절차:**
```
1. 무작위 점을 선택하고 Core Point인지 확인
2. Core Point라면 ε-이웃 내 모든 점을 동일 군집으로 할당
3. 연결된 Core Point들을 통해 군집 확장 (Density-Reachable)
4. 모든 점이 처리될 때까지 반복
```

**장단점:**
| 장점 | 단점 |
|------|------|
| 군집 수 K를 미리 지정할 필요 없음 | ε과 MinPts 설정에 민감 |
| 임의 형태의 군집 식별 가능 | 밀도가 다른 군집을 동시에 식별 어려움 |
| 이상치(Noise) 자동 탐지 | 고차원 데이터에서 거리 척도 문제 발생 |
| 수행 결과가 결정론적(Deterministic) | 계산 복잡도가 높음 ($O(n^2)$ 또는 공간 인덱스 사용 시 $O(n \log n)$) |

---

#### 4.1.3 계층적 군집 (Hierarchical Clustering)

**핵심 원리:** 개별 데이터 포인트부터 시작하여 점진적으로 군집을 병합하거나, 전체 데이터에서 시작하여 분할

**접근 방식:**

| 방식 | 접근 | 설명 | 시간 복잡도 |
|------|------|------|-------------|
| **응집적(Agglomerative)** | 하향식 (Bottom-Up) | 개별 점에서 시작하여 유사한 군집을 병합 | $O(n^3)$ (기본), $O(n^2 \log n)$ (최적화) |
| **분할적(Divisive)** | 상향식 (Top-Down) | 전체 군집에서 시작하여 분할 | 더 높은 계산 비용 |

**연결법 (Linkage Methods):**

| 연결법 | 설명 | 특징 |
|--------|------|------|
| **Single Linkage** | 군집 간 가장 가까운 점 간 거리 사용 | 체인 효과(Chaining Effect) 발생 가능, 긴 군집 생성 |
| **Complete Linkage** | 군집 간 가장 먼 점 간 거리 사용 | 컴팩트한 군집 생성, 노이즈에 강함 |
| **Average Linkage** | 군집 간 모든 점 쌍의 평균 거리 사용 | 밸런스 잡힌 결과, 가장 널리 사용 |
| **Ward's Method** | 군집 간 분산 증가를 최소화 | 구형 군집에 적합, SSE 최소화 |

**덴드로그램 (Dendrogram):** 계층적 군집 결과를 시각화한 트리 구조, 수평 절단(Cut) 위치에 따라 다른 군집 수 도출 가능

---

#### 4.1.4 가우시안 혼합 모델 (Gaussian Mixture Model, GMM)

**핵심 원리:** 데이터가 여러 개의 다변량 정규분포(Multivariate Normal Distribution)의 혼합으로 생성되었다고 가정

**확률 모델:**
$$p(x) = \sum_{k=1}^K π_k \mathcal{N}(x \| μ_k, Σ_k)$$

- $π_k$: k번째 혼합 계수 (Mixing Coefficient), $\sum π_k = 1$
- $μ_k$: k번째 분포의 평균 벡터
- $Σ_k$: k번째 분포의 공분산 행렬

**EM (Expectation-Maximization) 알고리즘:**
```
[E-Step] 각 데이터가 각 군집에 속할 사후 확률(Responsibility) 계산
    γ(z_{nk}) = \frac{π_k \mathcal{N}(x_n \| μ_k, Σ_k)}{\sum_{j=1}^K π_j \mathcal{N}(x_n \| μ_j, Σ_k)}

[M-Step] 사후 확률을 기반으로 파라미터 업데이트
    π_k^{new} = \frac{1}{N} \sum_{n=1}^N γ(z_{nk})
    μ_k^{new} = \frac{\sum_{n=1}^N γ(z_{nk}) x_n}{\sum_{n=1}^N γ(z_{nk})}
    Σ_k^{new} = \frac{\sum_{n=1}^N γ(z_{nk}) (x_n - μ_k^{new})(x_n - μ_k^{new})^T}{\sum_{n=1}^N γ(z_{nk})}
```

**장단점:**
| 장점 | 단점 |
|------|------|
| 소프트 군집(Soft Clustering) 가능 - 각 데이터의 군집 소속 확률 제공 | 계산 복잡도 높음 |
| 타원형(Elliptical) 군집 식별 가능 | 정규분포 가정, 비정규 데이터에 약함 |
| EM 알고리즘을 통해 최대우도(Maximum Likelihood) 추정 | 로컬 옵티멈(Local Optimum)에 수렴 가능 |
| 확률적 프레임워크 기반으로 불확실성 모델링 | 초기화에 민감 |

---

### 4.2 알고리즘 종합 비교

| 비교 항목 | K-means | DBSCAN | Hierarchical | GMM |
|----------|---------|--------|--------------|-----|
| **군집 형태** | 구형(Convex) | 임의 형태 | 연결법에 따라 다름 | 타원형 |
| **군집 수(K)** | 사전 지정 필요 | 자동 결정 | 덴드로그램에서 선택 | 사전 지정 필요 |
| **노이즈 처리** | 불가 | 자동 식별 | 어려움 | 확률적 할당 |
| **소프트/하드** | 하드 | 하드 | 하드 | 소프트 |
| **시간 복잡도** | $O(nkt)$ | $O(n^2)$ | $O(n^3)$ | $O(nkt)$ |
| **초기화** | 민감 | 덜 민감 | 없음 | 민감 |
| **스케일 민감성** | 높음 | 중간 | 중간 | 중간 |
| **고차원** | 차원의 저주 문제 | 거리 척도 문제 | 거리 척도 문제 | 차원의 저주 문제 |

---

## 5. 군집 평가 지표 (Cluster Validation Metrics)

군집의 품질을 평가하는 지표는 크게 **내부 지표(Internal Index)**와 **외부 지표(External Index)**로 구분된다.

### 5.1 내부 지표 (Internal Validation)

레이블이 없는 데이터셋에서 군집 품질을 평가

| 지표 | 설명 | 해석 |
|------|------|------|
| **실루엣 계수 (Silhouette Coefficient)** | 개별 데이터의 군집 내 응집도와 군집 간 분리도의 비율 | -1~1 범위, 1에 가까울수록 좋음 |
| **Davies-Bouldin Index (DBI)** | 군집 간 거리와 군집 내 분산의 비율 | 작을수록 좋음 |
| **Calinski-Harabasz Index (CHI)** | 군집 간 분산과 군집 내 분산의 비율 | 클수록 좋음 |
| ** Dunn Index** | 최소 군집 간 거리와 최대 군집 직경의 비율 | 클수록 좋음 |

**실루엣 계수 계산:**
$$s(i) = \frac{b(i) - a(i)}{\max\{a(i), b(i)\}}$$

- $a(i)$: 데이터 i와 동일 군집 내 다른 점들 간 평균 거리 (Cohesion)
- $b(i)$: 데이터 i와 다른 군집 간 최소 평균 거리 (Separation)

### 5.2 외부 지표 (External Validation)

참조 레이블(Ground Truth)이 존재할 때 평가

| 지표 | 설명 | 해석 |
|------|------|------|
| **Adjusted Rand Index (ARI)** | 두 군집 간 일치도 측정, 우연 일치 보정 | 0~1, 1에 가까울수록 완벽 |
| **Normalized Mutual Information (NMI)** | 두 군집 간 상호 정보량 정규화 | 0~1, 1에 가까울수록 완벽 |
| **Fowlkes-Mallows Index (FMI)** | 정밀도(Precision)와 재현율(Recall)의 기하평균 | 0~1, 1에 가까울수록 완벽 |

---

## 6. 군집수 결정 방법

### 6.1 엘보우 방법 (Elbow Method)

K-means에서 SSE(군집 내 제곱 오차 합)의 감소율이 급격히 줄어드는 지점(K)을 선택

```
SSE 그래프
    SSE
     │
     │        ∙ (Elbow Point)
     │      ∙
     │    ∙
     │  ∙
     │∙
     └─────────────────→ K
```

### 6.2 실루엣 분석 (Silhouette Analysis)

각 K에 대한 평균 실루엣 계수를 계산하여 최적 K 선택

### 6.3 갭 통계 (Gap Statistic)

실제 데이터와 균등 분포(Uniform Distribution)로부터 생성된 데이터의 SSE 차이(Gap)를 계산

$$\text{Gap}(k) = \frac{1}{B} \sum_{b=1}^B \log(W_k^{(b)}) - \log(W_k)$$

- $W_k$: 실제 데이터의 SSE
- $W_k^{(b)}$: b번째 무작위 데이터의 SSE
- $B$: 부트스트랩 횟수 (일반적으로 10~100)

---

## 7. 차원 축소와 군집화 (Dimensionality Reduction + Clustering)

### 7.1 차원의 저주 (Curse of Dimensionality)

고차원 데이터에서 거리 척도가 의미를 잃는 현상

- 모든 점들이 거의 동일한 거리를 가짐
- 군집화 성능 저하
- 해결책: 차원 축소

### 7.2 차원 축소 기법

| 기법 | 원리 | 군집화와의 결합 |
|------|------|----------------|
| **PCA (Principal Component Analysis)** | 분산 최대 방향으로 차원 축소 | K-means 전처리, 구형 군집 효과적 |
| **t-SNE (t-Distributed Stochastic Neighbor Embedding)** | 지역 구조 보존하며 차원 축소 | 시각화, 군집 구조 확인 |
| **UMAP (Uniform Manifold Approximation and Projection)** | t-SNE보다 빠르고 전역 구조 보존 | 대규모 데이터 시각화 |
| **Autoencoder** | 신경망을 통한 비선형 차원 축소 | Deep Clustering, 잠재 공간 군집화 |

---

## 8. 실제 적용 사례 및 활용 분야

### 8.1 비즈니스 및 마케팅

| 분야 | 활용 사례 | 군집 알고리즘 |
|------|----------|--------------|
| **고객 세분화** | 구매 패턴, 연령, 지역 기반 고객 그룹화 | K-means, GMM |
| **상품 추천** | 유사한 상품 그룹화, 콘텐츠 기반 필터링 | Hierarchical |
| **시장 분석** | 경쟁사 포지셔닝 분석 | K-means |

### 8.2 정보 기술 및 데이터 과학

| 분야 | 활용 사례 | 군집 알고리즘 |
|------|----------|--------------|
| **이상치 탐지** | 네트워크 침입 탐지, 금융 사기 탐지 | DBSCAN, Isolation Forest |
| **이미지 처리** | 이미지 세분화, 컬러 양자화 | K-means |
| **자연어 처리** | 토픽 모델링, 문서 군집화 | Hierarchical, K-means |
| **추천 시스템** | 협업 필터링 기반 사용자 그룹화 | Spectral Clustering |

### 8.3 의료 및 생명과학

| 분야 | 활용 사례 | 군집 알고리즘 |
|------|----------|--------------|
| **유전체 분석** | 유전자 발현 패턴 기반 질병 분류 | Hierarchical, DBSCAN |
| **영상 진단** | 의료 영상 내 병변 군집화 | Fuzzy C-means |
| **약물 발견** | 화합물 구조 기반 군집화 | GMM |

---

## 9. 기술사적 판단 (Professional Engineer Judgment)

### 9.1 알고리즘 선택 가이드

| 상황 | 권장 알고리즘 | 이유 |
|------|--------------|------|
| 대규모 데이터(n > 100,000) | K-means, Mini-Batch K-means | 계산 효율성 우수 |
| 군집 수 미지수 | DBSCAN, Hierarchical | 군집 수 자동 결정 가능 |
| 비구형 군집 | DBSCAN, Spectral Clustering | 임의 형태 식별 가능 |
| 이상치 탐지 | DBSCAN, Isolation Forest | 노이즈 자동 식별 |
| 확률적 할당 필요 | GMM | 소프트 군집 제공 |
| 텍스트/범주형 데이터 | K-modes, K-prototypes | 코사인 유사도 기반 |

### 9.2 엔지니어링 고려사항

1. **데이터 전처리의 중요성:** 스케일링(Standardization, Normalization)은 거리 기반 군집 알고리즘(K-means, DBSCAN)의 성능에 결정적 영향

2. **초기화 민감성 관리:** K-means의 경우 K-means++ 초기화, GMM의 경우 여러 초기점에서 시도하여 최적 선택

3. **하이퍼파라미터 튜닝:** Grid Search, Random Search, Bayesian Optimization을 통해 최적 파라미터 탐색

4. **해석 가능성(Interpretability):** 비즈니스 의사결정 지원을 위해 군집 결과의 도메인 해석이 필수적

5. **확장성(Scalability):** 분산 처리(Spark MLlib, Dask), 스트리밍 데이터 처리(Micro-batch Clustering) 고려

6. **평가 지표의 문맥적 선택:** 내부 지표는 군집 품질, 외부 지표는 레이블 일치도 측정. 도메인 요구사항에 따라 선택

### 9.3 실무에서의 주요 이슈

| 이슈 | 설명 | 해결책 |
|------|------|--------|
| **차원의 저주** | 고차원에서 거리 척도 무력화 | 차원 축소, 특징 선택 |
| **스케일 민감성** | 변수 스케일 차이로 군집 왜곡 | 표준화(StandardScaler) |
| **초기화 의존성** | 결과 불안정성 | K-means++, 여러 실행 후 최적 선택 |
| **노이즈 민감성** | 이상치가 군집 파괴 | Robust 알고리즘(DBSCAN), 전처리 |
| **해석 어려움** | 군집의 비즈니스 의미 부여 | 도메인 전문가 협업, 시각화 |

---

## 10. 최신 동향 및 미래 전망

### 10.1 딥러닝 기반 군집화 (Deep Clustering)

| 기법 | 설명 | 특징 |
|------|------|------|
| **Deep Embedded Clustering (DEC)** | Autoencoder + K-means 결합 | 잠재 공간(Latent Space)에서 군집화 |
| **Deep Subspace Clustering** | 표현 학습과 군집화 공동 최적화 | 고차원 데이터 효과적 처리 |
| **Variational Autoencoder for Clustering** | 확률적 표현 학습 | GMM과 결합하여 소프트 군집 |

### 10.2 대규모 분산 군집화

- **Spark MLlib K-means:** 수십억 데이터 포인트 처리 가능
- **Online Clustering:** 스트리밍 데이터 실시간 군집화
- **GPU 가속화:** CUDA 기반 거리 계산 최적화

### 10.3 설명 가능한 AI (Explainable AI, XAI)와 군집화

- **SHAP (SHapley Additive exPlanations):** 군집 할당 기여도 분석
- **군집 특성 중요도:** 각 특징이 군집 형성에 미치는 영향력 분석
- **규칙 기반 군집 설명:** IF-THEN 규칙으로 군집 설명

### 10.4 미래 전망

1. **자동 머신러닝 (AutoML):** 자동 군집 알고리즘 선택 및 하이퍼파라미터 튜닝
2. **멀티뷰 군집화 (Multi-view Clustering):** 여러 데이터 소스 통합 군집화
3. **페더레이티드 러닝 기반 군집화:** 프라이버시 보존 분산 군집화
4. **시공간 데이터 군집화:** 위치 기반 서비스(LBS), 모빌리티 데이터 분석
5. **그래프 신경망(GNN) 기반 군집화:** 소셜 네트워크, 지식 그래프 군집화

---

## 11. 정리 및 요약

| 개념 | 핵심 내용 |
|------|----------|
| **군집분석** | 비지도학습을 통한 데이터의 유사성 기반 그룹화 |
| **거리 척도** | 유클리드, 맨해튼, 코사인, 마할라노비스 등 데이터 특성에 따라 선택 |
| **주요 알고리즘** | K-means(구형, 빠름), DBSCAN(임의 형태, 노이즈 처리), Hierarchical(계층 구조), GMM(확률적) |
| **평가 지표** | 실루엣 계수, DBI, CHI(내부), ARI, NMI(외부) |
| **군집수 결정** | 엘보우 방법, 실루엣 분석, 갭 통계 |
| **기술사적 판단** | 데이터 특성, 규모, 도메인 요구사항에 따라 알고리즘 선택 및 하이퍼파라미터 튜닝 |
| **미래 전망** | 딥러닝 융합, AutoML, 분산 처리, 설명 가능성 강화 |

---

## 📚 참고 자료

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
2. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd Edition). Springer.
3. Aggarwal, C. C., & Reddy, C. K. (2013). *Data Clustering: Algorithms and Applications*. CRC Press.
4. Jain, A. K., Murty, M. N., & Flynn, P. J. (1999). Data clustering: A review. *ACM Computing Surveys*, 31(3), 264-323.
5. Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. *KDD*, 226-231.
6. Scikit-learn: Machine Learning in Python. (2024). *https://scikit-learn.org/stable/modules/clustering.html*

---

# [부록] 쉽게 이해하는 군집분석 (학교 친구들 나누기)

## 🎒 학교 친구들을 그룹으로 나눠보자!

여러분 반에 30명의 친구들이 있다고 상상해 보세요. 선생님이 "비슷한 성격끼리 그룹을 만들어서 프로젝트를 해보자!"라고 하셨어요. 하지만 아직 누가 누구랑 잘 맞을지 아무도 몰라요. 이럴 때 **군집분석**을 쓰면 정말 쉽게 그룹을 만들 수 있어요! 🎉

---

## 🌟 군집분석이 뭐죠?

**"비슷한 것끼리 모아주는 똑똑한 방법"**이에요!

예를 들어:
- 🏀 농구 좋아하는 친구들끼리 모아서 "운동 그룹"
- 📚 공부 열심히 하는 친구들끼리 모아서 "공부 그룹"
- 🎨 그림 잘 그리는 친구들끼리 모아서 "미술 그룹"

이렇게 자동으로 **비슷한 친구들을 찾아서 그룹(군집)으로 만들어주는 거예요!**

---

## 🔍 어떻게 친구들을 찾나요?

### 방법 1: K-means (케이-민즈) - "미리 정해진 그룹 만들기"

1. **그룹 수 정하기:** "우리 반 3개 그룹으로 나눌래!" → K = 3
2. **처음에는 그냥 랜덤하게 나눠요:** 아무 그룹이나 배정
3. **다시 생각해서 옮겨요:** "어? 이 친구는 공부 그룹에 더 잘 맞겠다!"
4. **반복해서 최적의 그룹 찾기:** 그룹 변화가 없을 때까지 반복

**비유:** 반장이 "먼저 대충 나눠놓고, 계속 수정해서 완벽한 그룹 만들기!"

---

### 방법 2: DBSCAN (디비스캔) - "모이는 친구들끼리 그룹"

1. **밀착해서 있는 친구들 찾기:** "이 친구 주변에 친구가 많이 있네?"
2. **자동으로 그룹 만들기:** 붙어 있는 친구들끼리 그룹
3. **혼자 있는 친구는 외톨이:** 그룹에 들어가지 못한 친구는 "노이즈"

**비유:** 운동장에서 떼로 모여 있는 친구들끼리 자연스럽게 그룹 만들기!

---

### 방법 3: 계층적 군집 (Hierarchical) - "점점 합치기"

1. **처음에는 모두 혼자:** 30명 = 30개 그룹
2. **비슷한 두 그룹 합치기:** "이 친구랑 저 친구 성격이 비슷하네? 합치자!"
3. **반복:** 15개 → 10개 → 5개 → 3개 → 1개
4. **원하는 크기에서 끊기:** "3개 그룹으로 충분해!" 여기서 멈춤

**비유:** 조별과제 팀 만들 때, 먼저 2명씩 짝 짓고, 나중에 짝끼리 합쳐서 팀 만들기!

---

## 🤔 언제 어떤 방법을 쓸까요?

| 상황 | 쓰는 방법 | 이유 |
|------|----------|------|
| **그룹 수를 정해져 있을 때** | K-means | "우리 반 3개 그룹으로 나눠!" |
| **자연스럽게 모여 있는 친구들** | DBSCAN | "놀이터에서 떼로 노는 애들 모으기" |
| **계층적인 관계가 중요할 때** | Hierarchical | "우리 가족 → 우리 가문 → 우리 마을" |
| **확실하지 않은 경우** | GMM | "이 친구는 60% 공부 그룹, 40% 놀이 그룹" |

---

## 📊 군집이 잘 되었는지 어떻게 아나요?

### 실루엣 계수 (Silhouette Coefficient)

> **"그룹 안에서는 똑똑하게 뭉치고, 그룹 사이는 쫙 떨어져 있는지?"**

- **점수 1.0:** 완벽해요! 👍
- **점수 0.5:** 괜찮아요! 👌
- **점수 0.0:** 별로예요... 😐

**비유:** 학급 반 배치를 할 때
- 좋은 배치: "공부 잘하는 애들이 한 반에 다 모이고, 운동하는 애들은 다른 반!"
- 나쁜 배치: "공부하는 애들이 반마다 흩어져 있어서 반마다 비슷해요"

---

## 🎯 실생활 예시

### 1. 쇼핑몰 추천 시스템
- 여러분이 장난감을 많이 사면 → "장난감 좋아하는 친구" 그룹
- 그 그룹의 친구들이 또 사는 장난감 → 여러분에게도 추천!

### 2. 사진 정리 앱
- 여러분이 찍은 사진들에서
- 비슷한 색깔, 비슷한 장소 → 자동으로 그룹 폴더 만들어줘요!

### 3. 뉴스 앱
- 스포츠 뉴스끼리 모아서 "스포츠 카테고리"
- 연예 뉴스끼리 모아서 "연예 카테고리"

---

## 🧠 기억하세요!

> **"군집분석은 비슷한 것끼리 자동으로 찾아주는 똑똑한 방법이에요!"**

1. **K-means:** 미리 정해진 수만큼 그룹 만들기
2. **DBSCAN:** 자연스럽게 모여 있는 애들끼리 그룹
3. **Hierarchical:** 점점 합쳐가면서 그룹 만들기
4. **평가:** 그룹 안은 똑똑하게, 그룹 사이는 떨어져 있어야 해요!

이제 여러분도 데이터 과학자가 된 기분이지 않아요? 🚀
