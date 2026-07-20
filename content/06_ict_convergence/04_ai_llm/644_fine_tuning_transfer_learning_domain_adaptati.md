---
title: "Fine Tuning Transfer Learning Domain Adaptation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 644
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 대규모 사전학습 모델(LLM/VLM/Foundation Model)의 파라미터 공간을 소스 도메인 $\mathcal{D}_S$에서 타겟 도메인 $\mathcal{D}_T$으로 적응시키기 위해, Feature Extractor 동결 + Task-Specific Head 재학습(Frozen Feature Extraction), 부분 파라미터 미세조정(LoRA, Adapter, Prefix-Tuning), 그리고 도메인 불변 표현 학습(DANN, MMD, CORAL, Adversarial DA)을 결합한 **계층적 파라미터 재사용 및 분포 정렬(Alignment) 메커니즘**.
> 2. **가치**: 사전학습 활용 시 학습 데이터 요구량을 **90% 이상 절감**(ImageNet-1K 1.28M -> 1,000~10,000샘플), 수렴 속도 **3~10배 단축**, GPU 학습 비용 **1/100 수준**(A100 7,000시간 -> 70시간), Catastrophic Forgetting 억제를 통한 멀티태스크 일반화 성능 확보.
> 3. **판단 포인트**: (1) Frozen vs Full Fine-tuning vs PEFT(LoRA) trade-off, (2) 도메인 갭 측정($\mathcal{H}\Delta\mathcal{H}$-divergence, MMD) 기반 전략 선택, (3) 1st-order(MMD, CORAL) vs Adversarial(GRL) 정렬 기법, (4) Catastrophic Forging 방어(EWC, LwF, Replay Buffer), (5) 레이어별 Learning Rate 차별화(LLRD)와 Warm-up 정책.

---

## Ⅰ. 개요 및 필요성

현대 엔터프라이즈 AI 시스템은 **수직적 데이터 희소성(Vertical Data Sparsity)** 문제에 직면한다. 의료 영상·산업 결함·금융 사기·법률 문서 등 도메인 특화 데이터는 라벨링 비용이 막대하며(의료 영상 1건당 $30~$300, 영상당 10만건 수집 시 수십억 원), 수집 가능한 절대량도 제한적이다. 동시에 GPT-4, LLaMA-3, SAM, DINOv2 등 **Foundation Model**(사전학습 모델)의 등장으로 수십억~수천억 파라미터에 걸친 일반화된 표현력이 범용 자산화되었다.

그러나 Foundation Model은 **Inductive Bias가 소스 도메인(Source Domain, 예: WebText, LAION-5B)** 에 편향되어 있어, 타겟 도메인(Target Domain)에서 직접 추론 시 **Distribution Shift**로 인해 성능이 급격히 저하된다. 이를 수학적으로 표현하면 다음과 같다:

$$P_S(X, Y) \neq P_T(X, Y), \quad \text{where } P_S(X) \neq P_T(X)$$

여기서 $X$는 입력, $Y$는 라벨이며, **Covariate Shift**($P(X)$만 다름), **Concept Shift**($P(Y|X)$만 다름), **Label Shift**($P(Y)$만 다름) 등으로 세분화된다.

**파인 튜닝(Fine-Tuning) + 전이 학습(Transfer Learning) + 도메인 적응(Domain Adaptation)**은 위 문제를 해결하기 위한 3대 핵심 축이다:
- **전이 학습**: 소스 태스크 $\mathcal{T}_S$에서 학습한 지식을 타겟 태스크 $\mathcal{T}_T$로 전달(Transfer)
- **파인 튜닝**: 사전학습된 $\theta_{pre}$를 타겟 데이터 $\mathcal{D}_T$로 재조정
- **도메인 적응**: 소스-타겟 간 분포 차이를 명시적으로 최소화(Explicit Alignment)

```text
+------------------------------------------------------------------------+
|           Foundation Model 기반 적응형 학습 파이프라인 (End-to-End)         |
+------------------------------------------------------------------------+
|                                                                        |
|  +------------------+         +------------------+                     |
|  |  Phase 1:        |         |  Phase 2:        |                     |
|  |  Pre-Training    |         |  Domain-Specific |                     |
|  |  (Self-Superv.)  |         |  Continual Pretrain|                   |
|  |                  |         |                  |                     |
|  |  • MLM / NSP     | -------->|  • 100B Tokens   |                     |
|  |  • Contrastive   | Backbone|  • Domain Corpus |                     |
|  |  • MAE / DINO    | Reuse   |  • MLM Continue  |                     |
|  +------------------+         +--------+---------+                     |
|           |                            |                               |
|           |  θ_pre-trained             v                               |
|           |                  +------------------+                      |
|           |                  |  Phase 3:        |                      |
|           |                  |  Domain Adaptation|                     |
|           |                  |  (DANN / MMD /   |                      |
|           |                  |   CORAL / AdaBN) |                      |
|           |                  +--------+---------+                      |
|           |                           |                                |
|           |                           v                                |
|           |                  +------------------+                      |
|           |                  |  Phase 4:        |                      |
|           |                  |  Task-Specific   |                      |
|           |                  |  Fine-Tuning     |                      |
|           |                  |  (LoRA / Adapter)|                      |
|           |                  +--------+---------+                      |
|           |                           |                                |
|           |                           v                                |
|           |                  +------------------+                      |
|           |                  |  Phase 5:        |                      |
|           |                  |  Inference +     |                      |
|           |                  |  Online Adapta-  |                      |
|           |                  |  tion (TENT)     |                      |
|           |                  +------------------+                      |
|                                                                        |
+------------------------------------------------------------------------+

  Distribution Shift의 단계적 완화:
  ---------------------------------------------------------------------->
  Source Domain (WebText) ---> General Domain ---> Vertical Domain ---> Task
   P_S(X,Y)  ·  Massive     · 100B tokens  · 10B tokens  · 10K~100K samples
```

**구시대(Pre-2018) vs 현대(Post-2020) 패러다임 비교**:
- **구시대**: 도메인별 **Scratch 학습**(ResNet, BERT를 의료/법률/금융 데이터로 From-Scratch 학습) -> 데이터 부족, 과적합, 학습 비용 폭증
- **현대**: Foundation Model **사전학습 -> 도메인 적응 -> 태스크 파인튜닝**의 3단계 파이프라인, PEFT(Parameter-Efficient Fine-Tuning)로 0.1~1% 파라미터만 업데이트

- **📢 섹션 요약 비유**: 거대한 국립중앙도서관(사전학습 모델)에서 필요한 책만 골라서 내 도메인 책장으로 옮긴 뒤(Transfer), 책 표지만 한글 번역(Adaptation)하고, 마지막으로 내가 원하는 주제별 색인 시스템(파인튜닝)을 만드는 과정입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전이 학습은 **무엇을(What) 이송할 것인가**에 따라 4가지 관점으로 분류된다( Pan & Yang, IEEE TKDE 2010):

1. **Instance-based Transfer**: 소스 데이터에서 가중치 $w(x) = P_T(x)/P_S(x)$로 중요 샘플 재선별 (TrAdaBoost)
2. **Feature-representation Transfer**: 도메인 불변(Invariant) Feature 공간으로 매핑 $\phi: \mathcal{X} \rightarrow \mathcal{Z}$
3. **Parameter-based Transfer**: 사전학습 파라미터 $\theta_{pre}$를 사전(Prior)으로 사용 (Bayesian: $P(\theta_T | \mathcal{D}_T) \propto P(\mathcal{D}_T | \theta_T) P(\theta_T | \theta_{pre})$)
4. **Relational-knowledge Transfer**: 관계 그래프/규칙 이송 (Graph Neural Network)

```text
+----------------------------------------------------------------------+
|      Feature-based Domain Adaptation 아키텍처 (DANN 변형)              |
+----------------------------------------------------------------------+
|                                                                      |
|   Source Domain          Shared Feature Extractor        Target Dom. |
|   x_s ~ P_S(x,y)                  G_f                    x_t ~ P_T(x) |
|        |                    (e.g., ResNet-50,             |          |
|        |                     BERT-base,                  |          |
|        |                     LLaMA-7B)                   |          |
|        |                           |                     |          |
|        |                           v                     |          |
|        |                  +-----------------+            |          |
|        |                  |   f = G_f(x)    |            |          |
|        |                  |   ∈ R^d         |            |          |
|        |                  +--------+--------+            |          |
|        |                           |                     |          |
|        |              +------------+------------+        |          |
|        |              v                         v        |          |
|        |     +----------------+        +----------------+|          |
|        |     | Label Predictor |        | Domain Classifier|        |
|        |     |   G_y(f)       |        |   G_d(f)        ||          |
|        |     |                |        |   (0: Source,   ||          |
|        |     |  L_y = CE(ŷ,y) |        |    1: Target)   ||          |
|        |     +--------+-------+        +--------+-------+|          |
|        |              |                         |        |          |
|        |              |                         |        |          |
|        |              |  +------------------+   |        |          |
|        |              |  | Gradient Reversal|   |        |          |
|        |              |  |  Layer (GRL)     |<---+        |          |
|        |              |  |  λ · ∂L_d/∂θ_f  |              |          |
|        |              |  +------------------+              |          |
|        |              v                                    |          |
|        |     Total Loss:                                   |          |
|        |     L_total = (1/n)Σ L_y(ŷ_i, y_i)               |          |
|        |              + λ · (1/n)Σ L_d(d_i, d̂_i)          |          |
|        |              + μ · R(θ)   [Regularization]       |          |
|        |                                                   |          |
|        |  ※ Adversarial: G_y는 L_y 최소화, G_d는 L_d 최대화  |          |
|        |  ※ λ는 0 -> 1 스케줄로 점진 증가                   |          |
|                                                                      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Frozen Feature Extractor** | 저수준/중수준 일반 Feature 추출 | ImageNet Pretrained ResNet/ViT, BERT-base, Layer 1~N 동결(requires_grad=False), Layer-wise Learning Rate Decay(LLRD) 적용 |
| **Task-Specific Head** | 타겟 태스크 분류/회귀 수행 | 신규 FC Layer (768->num_classes), Xavier/Kaiming 초기화, 학습률 η_head = 1e-3, η_backbone = 1e-5 (Δ=100배) |
| **LoRA / Adapter** | PEFT(Parameter-Efficient Fine-Tuning) | LoRA: $W' = W + \Delta W = W + BA$, $B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k}$, rank $r=4\sim 64$ (기본 8), α=16. 학습 파라미터 0.1~1%. Adapter: Houlsby Adapter $H \leftarrow W + \text{down}(H)\rightarrow\text{up}(H)$, $H \in \mathbb{R}^{d \times 64}$ 병목 |
| **Domain Alignment Module** | 소스-타겟 분포 정렬(Alignment) | MMD(Maximum Mean Discrepancy): $\text{MMD}^2 = \|\mathbb{E}[\phi(X_S)] - \mathbb{E}[\phi(X_T)]\|^2_{\mathcal{H}}$ (RBF kernel $\phi$). CORAL: $L_{CORAL} = \frac{1}{4d^2}\|C_S - C_T\|_F^2$, $C = (X-\bar{X})(X-\bar{X})^T$. DANN: GRL(Gradient Reversal Layer) 기반 Adversarial. AdaBN: BatchNorm 통계량만 $\mu_T, \sigma_T^2$로 교체 |
| **Forgetting Mitigation** | Catastrophic Forgetting 방지 | EWC(Elastic Weight Consolidation): $L = L_T + \lambda \sum_i F_i (\theta_i - \theta^*_{pre,i})^2$, Fisher Information $F_i$로 중요 가중치 보호. LwF(Learning without Forgetting): Knowledge Distillation $L_{KD} = -\sum_i p_T^{(i)} \log p_S^{(i)}$. Replay Buffer: 5~10% 소스 데이터 유지 |
| **Self-Training / Pseudo-Labeling** | Unlabeled 타겟 데이터 활용 | FixMatch: confidence > τ (0.95) 샘플만 pseudo-label, weak->strong augmentation. Noisy Student: Teacher->Student iterative, noise injection (Dropout, RandAugment) |
| **Continual Learning Module** | 순차적 다중 도메인 적응 | Progressive Neural Networks: 측면 컬럼(Column) 추가, 이전 태스크 동결. AdapterFusion: Multi-Task Adapter 간 Attention 융합 |

### 핵심 알고리즘 및 수식

**1. MMD (Maximum Mean Discrepancy, Gretton et al., 2012)**:
$$\text{MMD}^2(\mathcal{D}_S, \mathcal{D}_T) = \left\| \frac{1}{n_S}\sum_{i=1}^{n_S}\phi(x_i^S) - \frac{1}{n_T}\sum_{j=1}^{n_T}\phi(x_j^T) \right\|_{\mathcal{H}}^2$$

**2. CORAL (Sun & Saenko, 2016)**:
$$L_{CORAL} = \frac{1}{4d^2}\|X_S^T X_S - X_T^T X_T\|_F^2$$

**3. DANN Loss (Ganin et al., 2016)**:
$$L = \frac{1}{n}\sum_{i=1}^{n} L_y(x_i^S, y_i) - \lambda \left[ \frac{1}{n}\sum_{i=1}^{n} L_d(x_i^S, 0) + \frac{1}{m}\sum_{j=1}^{m} L_d(x_j^T, 1) \right]$$

**4. LoRA Forward Pass**:
$$h = W_0 x + \frac{\alpha}{r} B A x, \quad W_0 \in \mathbb{R}^{d \times k} \text{ (frozen)}, \quad \Delta W = BA \in \mathbb{R}^{d \times k}$$

**5. EWC Penalty (Kirkpatrick et al., 2017)**:
$$L_{EWC}(\theta) = L_T(\theta) + \lambda \sum_i F_i (\theta_i - \theta_{pre,i})^2, \quad F_i = \mathbb{E}_{(x,y)\sim \mathcal{D}_S}\left[\left(\frac{\partial \log p(y|x,\theta)}{\partial \theta_i}\right)^2\right]$$

### Layer-wise Learning Rate Decay (LLRD) 구현 예시 (HuggingFace)

```python
def get_llrd_params(model, base_lr=1e-5, decay=0.95):
    params = []
    for i, layer in enumerate(model.encoder.layer):
        lr = base_lr * (decay ** (model.config.num_hidden_layers - i - 1))
        params.append({"params": layer.parameters(), "lr": lr})
    return params  # 출력층에 가까울수록 높은 lr
```

- **📢 섹션 요약 비유**: 다국적 대기업의 본사 시스템(Foundation Model)에 각 국가 지사(Domain)가 연결되어 있는데, 본사 정책은 유지하되(Backbone Freeze), 현지 시장에 맞게 영업 전략만 수정(Head