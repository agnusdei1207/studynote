---
title: "Recommendation Collaborative Content Based"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 716
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 추천 시스템은 **협업 필터링(CF: User-Item Matrix의 잠재 요인 분해 - SVD/ALS/NMF)**과 **콘텐츠 기반 필터링(CBF: Item Feature Vector의 유사도 - TF-IDF, Word2Vec, BERT 임베딩)**이라는 두 축의 알고리즘 패러다임으로 구성되며, 실제 운영 환경에서는 이 둘을 결합한 **하이브리드 모델(Weighted, Switching, Cascade, Feature Augmentation)**로 진화하고 있습니다.
> 2. **가치**: Netflix Prize(2006)를 통해 입증된 것처럼, **정확도 10% 향상만으로도 수십억 달러의 매출 차이**가 발생하며, MAE·RMSE·NDCG@K·MAP·Hit Rate 등의 지표로 측정되는 추천 품질이 사용자 retention, CTR, GMV에 직접적인 영향을 미칩니다.
> 3. **판단 포인트**: **콜드 스타트(Cold Start)**, **데이터 희소성(Sparsity)**, **확장성(Scalability)**, **인기도 편향(Popularity Bias)**, **필터 버블(Filter Bubble)** 등 트레이드오프를 고려하여, 사용자 수 vs 아이템 수, 인터랙션 로그 유무, 실시간성 요구 수준에 따라 메모리 기반(Memory-Based) 또는 모델 기반(Model-Based) 접근을 결정해야 합니다.

---

## Ⅰ. 개요 및 필요성

정보 과부하(Information Overload) 시대에서 사용자가 합리적인 시간 내에 원하는 콘텐츠·상품·서비스를 발견하도록 돕는 것이 추천 시스템(Recommender System)의 핵심 임무입니다. 1990년대 초반 **Tapestry**(1992, Xerox PARC)에서 명시적 평점(Explicit Rating)을 활용한 협업 필터링이 처음 등장한 이래, Amazon의 Item-to-Item CF(2003), Netflix Prize(2006-2009), YouTube의 Deep Neural Network 추천(2016), Transformer 기반의 SASRec(2018), LLM을 활용한 제로샷 추천(2023~)까지 빠르게 발전해왔습니다.

```text
[추천 시스템 패러다임의 진화]

  1990s          2000s           2010s           2020s
  +-----+       +-----+        +-----+         +------+
  |Rule |------->| CF  |-------->| MF  |--------->|Deep+ |
  |Base |       |Neigh|        | +EM |         | LLM  |
  +-----+       +-----+        +-----+         +------+
                  |              |               |
                  v              v               v
              User×Item      SVD/ALS       SASRec, BERT4Rec,
              희소행렬        잠재요인       Mamba4Rec, LLM-Rec
```

**협업 필터링(CF)**은 "비슷한 취향의 사용자는 비슷한 아이템을 좋아한다"는 사회적 협업 가설에 기반하며, 다수의 사용자-아이템 인터랙션 행렬(Interaction Matrix)을 공동으로 분석합니다. 반면 **콘텐츠 기반 필터링(CBF)**은 "사용자가 과거에 선호했던 아이템과 유사한 특성을 가진 아이템을 추천한다"는 아이템 자체의 콘텐츠 메타데이터(텍스트, 이미지, 오디오, 장르, 카테고리, 태그 등)를 활용합니다.

실무에서는 단일 기법의 한계(콜드 스타트, 데이터 희소성, 동질화 문제)를 극복하기 위해 **하이브리드(Hybrid)** 방식이 주류입니다. Netflix는 전체 추천 파이프라인의 약 75%에서 콘텐츠 메타데이터를, 25%에서 협업 신호를 활용하는 **Feature Augmentation Hybrid** 구조를 사용합니다.

- **📢 섹션 요약 비유**: 협업 필터링은 **"책방에서 다른 손님이 함께 산 책"**(집단 지성)을 보는 것이고, 콘텐츠 기반은 **"내가 좋아하는 책의 표지와 저자, 주제"**(아이템 자체의 속성)를 다시 보는 것입니다. 두 가지 모두 쓰는 것이 실제 서점 직원의 머릿속입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 협업 필터링 (Collaborative Filtering) 상세

#### (1) 메모리 기반 (Memory-Based) CF

```text
[메모리 기반 협업 필터링 처리 흐름]

사용자 A -+                                  +--> 추천 아이템
사용자 B -+                                  |
사용자 C -+--> [User×Item 평점 행렬 R] --+---> [유사도 계산] --+
사용자 D -+                            |                    |
사용자 E -+                            +---> [이웃집계/가중합] -+
                                       |          ^
                                       v          |
                              +--------------+    |
                              |  r̂(u,i) =    |----+
                              |  Σ sim(u,v)·r(v,i)
                              |  -----------------
                              |  Σ |sim(u,v)|
                              +--------------+
```

**사용자 기반(User-Based) CF**:
- **피어슨 상관계수(Pearson Correlation)**:
  `sim(u,v) = Σ(r(u,i) - r̄(u))(r(v,i) - r̄(v)) / √[Σ(r(u,i) - r̄(u))² · Σ(r(v,i) - r̄(v))²]`
- **코사인 유사도(Cosine Similarity)**: `sim(u,v) = (r_u · r_v) / (||r_u||₂ · ||r_v||₂)`
- **스피어맨 순위 상관(Spearman's Rank)**: 평점이 아닌 순위로 유사도 산정 -> 이상치에 강건
- **조정 코사인(Adjusted Cosine)**: 아이템별 평균 평점을 차감하여 사용자 평가 기준 편향 보정

**아이템 기반(Item-Based) CF** (Amazon이 대규모 시스템에서 채택):
- 아이템 간 동시 발생(Co-occurrence) 행렬에서 조정 코사인 유사도 계산
- 시간 복잡도: User-Based는 O(m²) -> Item-Based는 O(n²) (단, m:사용자 << n:아이템 이므로 사전 계산으로 절감)
- Amazon 논문(2003)에 따르면, m·n이 클수록 Item-Based가 User-Based 대비 약 28배 빠른 응답 시간

#### (2) 모델 기반 (Model-Based) CF

```text
[행렬 분해(Matrix Factorization) 구조]

원본 행렬 R (m × n)           잠재 요인 행렬
+--------------+              +---------+         +----------+
| 5  ?  3  ?  |              | P (m×k) |   Qᵀ    | ? 1  4 ? |
| ?  4  ?  2  |    ≈         |         | (k×n)   | 3  ?  2 5 |
| 4  ?  ?  5  |              | 사용자  |         |  ?  2  ? 1|
| ?  3  4  ?  |              | 잠재요인|         |  2  ?  3 ?|
+--------------+              +---------+         +----------+
   m × n                          k                    k

   손실함수: L = Σ_{(u,i)∈Ω} (r(u,i) - μ - b_u - b_i - p_u·q_iᵀ)²
            + λ(||p_u||² + ||q_i||² + b_u² + b_i²)
```

**핵심 알고리즘**:

| 알고리즘 | 핵심 아이디어 | 계산 복잡도 | 특징 |
|:---|:---|:---|:---|
| **SVD (Singular Value Decomposition)** | R = UΣVᵀ, 상위 k개 특이값만 유지 | O(mn·k²) | 비결측치 가정으로 사전 imputation 필요 (Funk SVD로 개선) |
| **Funk SVD / RSVD** | 관측값만으로 p_u, q_i 직접 학습 (SGD) | O(Ω·k) | Netflix Prize 우승팀(Bell & Koren) 채택 |
| **ALS (Alternating Least Squares)** | P 고정한 채 Q 최적화 -> Q 고정한 채 P 최적화 반복 | O(k·(m+n)+nnz) | 병렬화·분산 처리에 최적, Spark MLlib 표준 |
| **BPR (Bayesian Personalized Ranking)** | 관측 > 미관측 쌍의 쌍별 순위 손실 | O(Ω·k) | 암묵적 피드백에 강점, AUC 최적화 |
| **NMF (Non-negative Matrix Factorization)** | 비음수 제약 분해 | O(Ω·k) | 해석 가능성 우수 (parts-based representation) |
| **PMF (Probabilistic MF)** | 가우시안 사전분포로 정규화 | O(Ω·k) | 베이지안 확장 가능 (BPR-MF 등) |
| **Deep MF / NeuMF** | MF + MLP 비선형 결합 | O(Ω·k·d) | 비선형 상호작용 포착, NCF (He et al., 2017) |

### 2. 콘텐츠 기반 필터링 (Content-Based Filtering) 상세

```text
[콘텐츠 기반 추천 파이프라인]

[Item 메타데이터] ---> [Feature Extraction] ---> [Item Profile Vector]
   + 장르 (범주형)      + TF-IDF / BM25              |
   + 감독/작가 (범주형)  + Word2Vec / GloVe            |
   + 줄거리 (텍스트)     + BERT / SBERT               v
   + 포스터 (이미지)     + ResNet/ViT 임베딩     [코사인 유사도]
   + 오디오 (음악)                                |      |
                                                v      v
[User Profile] -------------------------> [Top-K 유사 아이템]
   가중합: p(u) = Σ r(u,i)·w_i                    ^
                                              [Threshold Filter]
```

**핵심 기술 스택**:
- **TF-IDF**: `tfidf(t,d) = tf(t,d)·log(N/df(t))` — 문서 내 단어의 중요도 가중치
- **BM25 (Okapi)**: `score(q,d) = Σ IDF(qi)·(f(qi,d)·(k1+1)) / (f(qi,d)+k1·(1-b+b·|d|/avgdl))` — TF-IDF의 확장으로 문서 길이 정규화 추가
- **Word2Vec / Doc2Vec (Gensim)**: 아이템 설명 텍스트를 100~300차원 임베딩으로 변환, Item2Vec으로 확장
- **BERT / SBERT (Sentence-Transformer)**: 768차원 문맥 임베딩, 코사인 유사도로 의미적 유사성 측정
- **다중 모달 임베딩**: 이미지(CNN), 오디오(CLAP), 메타데이터(범주 임베딩)를 concat 후 MLP로 통합 표현 학습
- **사용자 프로파일링**: `p(u) = Σ r(u,i)·item_profile(i) / Σ |r(u,i)|` — Rocchio 알고리즘(1971) 또는 의사반응 피드백(Pseudo-Relevance Feedback)으로 점진적 갱신

### 3. 하이브리드 추천 시스템 (Hybrid)

```text
[하이브리드 추천 시스템 통합 패턴]

+-------------------------------------------------------------+
|                    Hybrid Recommender                         |
|                                                             |
|  +------------+    +------------+    +--------------------+ |
|  |    CBF     |    |     CF     |    |  Knowledge-Based   | |
|  |  Engine    |    |   Engine   |    | (Rule/Demographic) | |
|  +-----+------+    +-----+------+    +---------+----------+ |
|        |                 |                     |            |
|        +---------+-------+---------------------+            |
|                  v                                          |
|  +------------------------------------------------------+  |
|  |  [통합 전략: Combiner / Switcher / Cascade / Mixer]   |  |
|  +------------------------+-----------------------------+  |
|                           v                                |
|                  [최종 추천 Top-K]                          |
+-------------------------------------------------------------+
```

**7가지 하이브리드 패턴 (Burke 2002)**:

1. **Weighted**: `score(u,i) = α·score_CBF + β·score_CF + γ·score_KB`, α+β+γ=1
2. **Switching**: 컨텍스트에 따라 알고리즘 전환 (콜드 스타트 시 CBF -> 데이터 축적 후 CF)
3. **Cascade**: 1차(CBF)가 후보군 생성 -> 2차(CF)가 재순위
4. **Feature Augmentation**: CF 입력에 CBF 피처를 추가 (가장 보편적)
5. **Feature Combination**: 두 소스의 피처를 통합 후 단일 모델
6. **Meta-Level**: CF가 학습한 사용자 모델 자체를 CBF의 입력으로 사용
7. **Mixed**: 여러 추천을 동시에 제시 (UI 레벨 통합)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **데이터 수집/ETL** | 로그·메타데이터 정제 | Kafka -> Flink(실시간) / Spark Batch(일배치) / Snowflake(분석) |
| **피처 스토어** | Item/User 피처의 온라인-오프라인 일관성 제공 | Feast, Tecton, Hopsworks — p99 latency < 10ms |
| **임베딩 서비스** | 사전학습 벡터의 실시간 조회 | FAISS, Milvus, Pinecone, Qdrant (ANN: HNSW, IVF-PQ) |
| **CF 모델 서빙** | 학습된 잠재요인 행렬로 Top-K 후보 생성 | Two-Tower Model (YouTube DNN) — user/item tower 독립 인코딩 |
| **CBF 모델 서빙** | 콘텐츠 메타데이터 임베딩 유사도 계산 | BERT 서빙 (TorchServe, Triton Inference Server) |
| **재순위(Reranker)** | 비즈니스 룰·다양성·신선도 적용 | LambdaMART, MMR (Maximal Marginal Relevance), DPP |
| **A/B 테스트 프레임워크** | 온라인 실험 및 인과효과 측정 | 균형 배정 해시(Bucketed Hash), 분산분석(ANOVA), CUPED |

**수학적 핵심 - Matrix Factorization 손실함수**:
```
L = Σ_{(u,i)∈Ω} (r_ui - μ - b_u - b_i - p_uᵀq_i)²
    + λ(Σ ||p_u||² + Σ ||q_i||² + Σ b_u² + Σ b_i²)
```
- μ: 전역 평균, b_u: 사용자 편향, b_i: 아이템 편향, p_u, q_i: k차원 잠재 벡터
- 정규화(λ)로 과적합 방지, **implicit feedback**에서는 confidence weight `c_ui = 1 + α·log(1+r_ui/ε)` 적용 (Hu et al. 2008)

- **📢 섹션 요약 비유**: 추천 엔진은 **"주방의 셰프"**와 같습니다. 협업 필터링은 **다른 손님들이 자주 같이 시킨 메뉴**(사회적 신호), 콘텐츠 기반은 **재료와 조리법의 유사성**(아이템 속성)이고, 좋은 셰프는 둘 다 보고, 조리 시간(실시간성)과 손님 취향(개인화)을 고려해 최종 요리(추천)를 냅니다.

---

## Ⅲ. 비교 및 연결

### 1. CF vs CBF 핵심 비교

| 구분 | 협업 필터링 (CF) | 콘텐츠 기반 (CBF) |
|:---|:---|:---|
| **입력 데이터** | 사용자-아이템 인터랙션 행렬 (R) | 아이템 메타데이터, 사용자 프로파일 |
| **핵심 가정** | "비슷한 사용자는 비슷한 취향" | "과거 선호 아이템과 유사한 속성" |
| **대표 알고리즘** | User/Item KNN, MF(SVD/ALS), NeuMF, LightGCN | TF-IDF + Rocchio, Embedding(KNN), Deep