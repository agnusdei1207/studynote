---
title: "Recommendation System Collaborative Deep Learning"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 669
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Collaborative Deep Learning(CDL)은 Stacked Denoising AutoEncoder(SDAE)로 콘텐츠 피처를 비선형 잠재공간에 임베딩하고, 이를 Probabilistic Matrix Factorization(PMF)의 Rating 잠재벡터와 Joint Bayesian Framework로 결합해 CF의 sparsity 문제와 Cold-start 문제를 동시에 완화하는 **"End-to-End SDAE + PMF 통합 확률 그래프 모델"** 이다.
> 2. **가치**: Netflix Prize 데이터셋에서 SVD++ 대비 RMSE 약 5~8% 개선, CiteULike 학술추천에서 Recall@100 약 12~15% 향상을 보이며, 별도 콘텐츠 메타데이터(텍스트/이미지/음성)만 있으면 신규 사용자·아이템에 대한 즉시 추천이 가능하여 **콘텐츠 기반 필터링과 협업 필터링의 장점을 결합**한다.
> 3. **판단 포인트**: ① **SDAE 사전학습 품질**(corruption ratio 0.3~0.5), ② **latent factor 차원 K=50~200**, ③ **하이퍼파라미터 λ_u, λ_v, λ_w, λ_n, a, b** 튜닝, ④ **Bayesian vs MAP 추론**, ⑤ **추천 시점의 Retrieval/Ranking 2-stage 분리 여부**가 성능·확장성·운영복잡도를 좌우한다.

---

## Ⅰ. 개요 및 필요성

전자상거래·OTT·뉴스 플랫폼이 폭발적으로 성장하면서 **수억 개 아이템 × 수억 명 사용자**의 명시적 평점(explicit feedback)은 평균 1% 미만, 암묵적 행동(implicit feedback)조차 사용자당 0.01% 이하로 존재하여 **극심한 데이터 희소성(sparsity)** 문제가 발생한다. 전통적인 Memory-based CF(User-KNN, Item-KNN)는 유사도 계산의 O(N²) 복잡도, Model-based CF(PMF, SVD++)는 **선형 잠재요인 모델**로 콘텐츠 부재 시 신규 아이템에 추천 불가능한 **Cold-start** 문제를 가진다. 한편 콘텐츠 기반 필터링(CBF)은 TF-IDF/Word2Vec 피처를 사용하나 사용자 선호 패턴을 포착하지 못한다. 2015년 Wang et al.이 제안한 CDL은 **SDAE의 비선형 표현력**과 **PMF의 확률적 잠재요인**을 하나의 Joint Bayesian Framework로 융합해 위 한계를 동시에 해결한다.

```text
        +-------------------------------------------------------------+
        |      Collaborative Deep Learning (CDL) End-to-End 파이프라인  |
        +-------------------------------------------------------------+

   [사용자 클릭/평점 행렬 R]                [아이템 콘텐츠 X0 (텍스트/이미지)]
        | N_users × M_items                       | M_items × p_features
        v                                        v
  +--------------+                        +--------------------+
  | Rating 관찰  |  R_ij ≠ 0              | SDAE 인코더-디코더 |
  | mask: I_ij  |  ---------►  --►        | X̂ = SDAE(X0 + ε)  |
  | 희소행렬     |                        | Corruption noise ε |
  +------+-------+                        +----------+---------+
         |                                           |
         |  CF branch: R ≈ U^T V                    |  Content branch: λ_w‖W_l‖²
         |  PMF likelihood p(R|U,V,σ²)              |  Encoder: h_l = sigmoid(W_l h_{l-1}+b_l)
         v                                           v
    +--------------------------------------------------------+
    |    Joint Bayesian Optimization (EM / SGD)             |
    |    max  L(U,V, {W_l},{b_l})                           |
    |    = - Σ‖R - U^T V‖² - λ_u‖U‖² - λ_v‖V - SDAE(X)‖² |
    +--------------------+-----------------------------------+
                         v
                 +--------------------+
                 | Top-K 추천 리스트  |
                 | score = U_i^T V_j |
                 +--------------------+
```

**기존 패러다임 대비 진보**:
- **1세대 CF**(User-KNN, 1990s): 유사도 기반, sparsity에 취약, 확장성 낮음
- **2세대 Model-based CF**(PMF/SVD++/Factorization Machines, 2008~2014): 잠재요인 학습, scalable하나 cold-start 한계
- **3세대 Hybrid**(LDA+CF, 2010s): 토픽모델 결합, 선형성 한계
- **4세대 CDL/Wide&Deep/DeepFM/NeuMF**(2015~현재): **비선형 딥러닝 + CF 융합**, cold-start 완화, end-to-end 학습

- **📢 섹션 요약 비유**: 마치 **낯선 사람에게 영화 취향을 물을 때**, 그 사람이 본 영화 목록(평점)만으로는 알 수 없지만 **그 사람이 쓴 리뷰 텍스트(콘텐츠)**까지 분석하면 취향을 더 정확히 추측하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CDL의 핵심은 **두 개의 생성 모델(Generative Model)** 을 Joint Optimization으로 묶는 것이다. 아이템 j에 대해 콘텐츠 X_j는 SDAE를 거쳐 잠재표현 V_j로 인코딩되며, V_j는 사용자의 잠재벡터 U_i와 내적하여 평점 R_ij를 생성한다.

```text
                       CDL 확률 그래프 모델 (PGM)
  +--------------------------------------------------------------+
  |                                                              |
  |   (a) Content branch (SDAE)             (b) CF branch (PMF)  |
  |                                                              |
  |   X̃_L  --►  h_L  --► ... --►  h_l  --►  V_j / X̂_j        |
  |   noisy      L-layer     middle     latent     recon          |
  |   input      encode      layer      vector    output          |
  |                                                              |
  |   W_l ~ N(0, λ_w⁻¹ I)              U_i ~ N(0, λ_u⁻¹ I_K)   |
  |   b_l ~ N(0, λ_w⁻¹ I)              V_j ~ N(U_i, λ_v⁻¹ I_K) |
  |   X̃_L = X_L + ε, ε~N(0, λ_n⁻¹ I)   R_ij ~ N(U_i^T V_j, σ²) |
  |                                                              |
  |                    +----------------------+                  |
  |                    |   Joint Posterior    |                  |
  |                    | p(U,V,{W,b}|R,X)     | ◄-- ELBO 최적화  |
  |                    +----------------------+                  |
  +--------------------------------------------------------------+
```

**SDAE 구조**: 입력층 X_0 ∈ ℝ^p -> L개의 은닉층 h_l = sigmoid(W_l h_{l-1} + b_l) -> 중간층 h_L/2 = 잠재벡터 E ∈ ℝ^K -> 디코더로 대칭 복원. **Corruption**: 입력에 dropout/masking noise 적용(비율 0.3~0.5)하여 robust feature 학습.

**Objective Function (Negative ELBO)**:

$$
\mathcal{L} = \sum_{i,j} \frac{I_{ij}}{2}(R_{ij} - U_i^T V_j)^2 + \frac{\lambda_u}{2}\|U\|_F^2 + \frac{\lambda_v}{2}\|V - f_e(X,W,b)\|_F^2 + \frac{\lambda_w}{2}\sum_l(\|W_l\|_F^2 + \|b_l\|_2^2) + \frac{\lambda_n}{2}\sum_j\|X_j - f_d(E_j)\|_2^2
$$

**업데이트 식 (EM-style, closed-form for U,V; SGD for W,b)**:

$$
U_i \leftarrow \left( V I_i V^T + \lambda_u I_K \right)^{-1} V R_i^T
$$
$$
V_j \leftarrow \left( U I^j U^T + \lambda_v I_K \right)^{-1} \left( U R^j + \lambda_v f_e(X_j, W, b) \right)
$$
$$
\{W_l, b_l\} \leftarrow \{W_l, b_l\} - \eta \frac{\partial \mathcal{L}_{\text{SDAE}}}{\partial W_l}
$$

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **SDAE Encoder f_e** | 콘텐츠 X_j -> K차원 잠재벡터 E_j | L개 은닉층, sigmoid 활성화, corruption ratio ρ ∈ {0.1, 0.3, 0.5}, Xavier 초기화 |
| **SDAE Decoder f_d** | E_j -> 원본 콘텐츠 X̂_j 재구성 | Encoder와 대칭 구조, reconstruction loss로 robust feature 학습 |
| **PMF Branch (U, V)** | 사용자·아이템 잠재벡터 학습 | U_i, V_j ∈ ℝ^K, N(0, λ⁻¹) prior, R_ij = U_i^T V_j + ε |
| **Joint Optimizer** | 두 모델을 ELBO로 통합 | EM 알고리즘: (1) U,V closed-form 갱신, (2) W,b SGD/Adam 갱신, 수렴까지 반복 |
| **Retrieval Layer** | Top-K 후보 생성 | ANNOY/FAISS로 U_i 유사 사용자 검색 또는 V_j 전체 코사인 유사도 Top-K |
| **Ranking Layer(Optional)** | CTR/CVR 예측 | NeuMF/DeepFM 등 2차 모델로 재정렬 (CDL output을 feature로 활용) |

**주요 하이퍼파라미터 (CiteULike-a 기준 Wang 2015)**:
- Latent dim K = 50~200 (보통 100)
- SDAE 구조: [p -> 200 -> 100] (encoder)
- Corruption ratio: 0.3
- λ_u = λ_v = 0.1, λ_w = 0.0001, λ_n = 1
- Learning rate η = 0.001, Adam optimizer
- Batch size = 256, Epochs = 100~200

- **📢 섹션 요약 비유**: SDAE는 **"번역가"**(텍스트->숫자공간으로 번역), PMF는 **"심판"**(숫자로 표현된 두 사람을 점수로 매김), 둘을 합치면 **"영화 평론가"** 처럼 콘텐츠와 취향을 동시에 이해하는 셈이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **CDL (Wang 2015)** | **NeuMF (He et al. 2017)** | **DeepFM (Guo et al. 2017)** | **Two-Tower (DSSM, 2013~)** | **LightGCN (He et al. 2020)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 아이디어** | SDAE+PMF 통합 | MF + MLP late fusion | FM + Deep component 공유 | User/Item 별도 임베딩 -> dot product | GCN으로 협업 신호 전파 |
| **콘텐츠 활용** | ✅ SDAE로 직접 통합 | ❌ ID만 (side-info 별도) | ❌ (FM은 sparse feature) | ✅ Item tower에 text/image 가능 | ❌ Interaction graph만 |
| **Cold-start** | ✅ 강력 (SDAE가 V 추론) | ❌ 신규 ID 학습 필요 | ❌ 신규 ID 필요 | ✅ Item tower는 pretrained 가능 | ❌ 신규 노드 cold |
| **학습 효율** | 중간 (EM+SGD) | 빠름 (end-to-end) | 매우 빠름 | 빠름 (분리 학습) | 빠름 (GCN) |
| **추론 속도** | 중간 (SDAE forward) | 매우 빠름 | 매우 빠름 | 매우 빠름 (ANN) | 빠름 |
| **확장성(M item)** | 제한적 (전체 SDAE 학습) | 좋음 (mini-batch) | 좋음 | 매우 좋음 (독립 tower) | 좋음 |

**연결 시스템**:
- **Feature Store (Feast/Tecton)**: 아이템 콘텐츠(임베딩)를 SDAE로 전처리 후 저장
- **ANN Index (FAISS/Milvus)**: V_j 임베딩을 IVF-PQ/HNSW로 인덱싱해 O(log M) 검색
- **Online Serving (Triton/TF Serving)**: User context 입력 -> U_i lookup -> Top-K
- **Kafka/Airflow**: 사용자 행동 로그를 SFT/online learning 파이프라인에 주입
- **A/B Test Framework (RecSys 실험 플랫폼)**: CDL vs NeuMF vs Random 등 다중군 실험

- **📢 섹션 요약 비유**: CDL이 **"혼자 요리하는 셰프"** 라면, NeuMF는 **"국과 메인요리를 따로 만들어 합치는 셰프"**, LightGCN은 **"친구 네트워크를 보며 추천하는 셰프"** 다. 어떤 셰프를 고르느냐는 **요리 재료(데이터)** 와 **고객(서비스 요구사항)** 에 달렸다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무자형 판단 체크리스트

1. **데이터 희소성 검증**: 사용자-아이템 평점/클릭 행렬의 sparsity(=`1 - nnz/(N×M)`)가 99.5% 이상이면 **콘텐츠 융합형(CDL/Two-Tower)** 필수, 99% 미만이면 순수 CF/LightGCN으로 충분한지 평가
2. **Cold-start 빈도 측정**: 신규 아이템 등록 주기가 시간당 1,000건 이상(뉴스/쇼핑몰)이고 신규 사용자 비율이 20% 이상이면 **콘텐츠 인코더 분리 학습 + Item tower pretrain** 구조 채택
3. **콘텐츠 임베딩 품질**: SDAE 입력이 raw text인 경우, **사전학습 임베딩(Word2Vec/BERT) + SDAE finetune**이 텍스트->잠재벡터 품질을 결정. 임베딩 차원 p ≥ 300, 코퍼스 100만 토큰 이상 권장
4. **추천 latency SLO 검토**: P99 latency ≤ 50ms 요구 시 **CDL 전체 forward는 부적합**(SDAE 5-layer ≈ 20ms), **Item 임베딩 사전계산 + User lookup + ANN** 구조로 분해
5. **Bias & Fairness**: CDL은 popularity bias를 가중치 평준화(popular item 가중치 v) 없이 그대로 학습 -> 노출 다양성 v, **inverse propensity weighting(IPW)** 또는 **re-ranking(DPP/MMR)** 적용 검토
6. **A/B Test 가설 설정**: CTR +X%, Watch-time +Y%, Catalogue Coverage +Z%(=MAU가 30일 내 본 카테고리 수), Long-tail Recall@K 개선치를 KPI로 사전 정의
7. **Multi-Armed Bandit 통합**: 탐색-활용 균형이 필요하면 ε-greedy/Thompson Sampling을 CDL score에 결합, 신규 아이템 노출 비율 5~10% 유지
8. **재학습 주기 결정**: 매시간 갱신 vs 일 1회 batch. Concept drift가 큰 도메인(뉴스)에서는 1시간, 안정 도메인(영화)은 1일 batch로 GPU 비용 절감

### 피해야 할 안티패턴

- **Full-batch SDAE 학습**: 수억 아이템에 SDAE full-batch SGD -> GPU OOM 발생. 반드시 **mini-batch (1024~8192)** 또는 **negative sampling** 적용
- **콘텐츠 미정규화 입력**: TF-IDF 벡터가 L2 정규화되지 않으면 SDAE 가중치 발산. **MaxAbsScaler + L2 normalize** 후 투입
- **CDL score를 logit으로 직접 노출**: 협업 점수만으로 노출 순위 결정 시 **filter bubble** 가속화. **Serendipity 지표** ≥ 5% 강제
- **Privacy 미고려**: 사용자 행동 로그에 PII 포함 시 **Differential Privacy(ε ≤ 1)** 또는 **Federated Learning** 적용 검토 (K-Anonymity ≤ 5)
- **Cold-start 지표 미측정**: 신규 아이템에 대한 Recall@K를 별도로 추적하지 않으면 **모델 개선이 long-tail에서 무효**화될 수 있음

- **📢 섹션 요약 비유**: CDL을 **"콘텐츠도 보고 취향도 보는 똑똑한 도서관 사서"** 라고 하면, 사서가 너무