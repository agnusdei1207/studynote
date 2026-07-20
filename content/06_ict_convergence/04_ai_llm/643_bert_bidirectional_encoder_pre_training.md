---
title: "BERT Bidirectional Encoder Pre-training"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 643
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BERT는 Transformer Encoder만을 비대칭으로 stacking하여 MLM(Masked Language Model)과 NSP(Next Sentence Prediction) 두 가지 비지도 사전학습 태스크로 **양방향 컨텍스트(Bidirectional Context)**를 동시 모델링하며, `[CLS]` 토큰의 pooled output이 문장 쌍 분류의 sentence-level representation 역할을 수행한다.
> 2. **가치**: 단일 사전학습 모델로 11개 NLP 다운스트림 태스크(질의응답, 개체명인식, 의미역결정, 문장분류 등)에서 기존 SOTA 대비 평균 +2.5~+7.0%p 성능 향상을 달성하며, **파라미터는 freeze하고 classification head만 fine-tune**하는 4~16 GPU·수십 GB VRAM급 학습 파이프라인을 표준화했다.
> 3. **판단 포인트**: "어떤 사전학습 목적함수를 선택할 것인가(MLM vs SOP vs ELECTRA의 RTD vs RoBERTa의 dynamic MLM)", "Fine-tuning 시 learning rate·epoch·batch size의 도메인 민감성", "Subword 단위 WordPiece 30,522 vocab의 OOV 처리 정책"이 실무 성능을 결정하는 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

2017년 Transformer가 기계번역 태스크로 제안된 이후, NLP 분야는 RNN/LSTM 기반의 순차적·단방향(unidirectional) 언어 모델의 한계—장기 의존성(long-range dependency) 손실, 좌->우 단방향(context-left-only) 정보 손실, 병렬화 불가—로부터 벗어나려는 시도가 활발해졌다. ELMo(2018)는 BiLLM을 통해 좌/우 문맥을 concat하는 "shallow bidirectional"을 도입했지만, ① LSTM의 50-step 장기 의존성 한계, ② task-specific architecture 변경의 부담, ③ layer별 독립적 feature extraction으로 인한 표현력 분산 문제를 안고 있었다.

BERT(Bidirectional Encoder Representations from Transformers, Devlin et al., Google, 2018-10)는 **Transformer Encoder의 self-attention이 본질적으로 양방향**이라는 점에 착안하여, 사전학습 단계에서부터 진정한 deep bidirectional representation을 학습하고, downstream task에서는 **단일 linear classifier만 교체**하는 transfer learning 패러다임을 완성했다. 이는 GPT-1(2018, decoder-only 12-layer)이 단방향 LM으로 한계를 보이던 시점에 등장하여, GLUE 80.5%, SQuAD v1.1 F1 93.2, MultiNLI 86.7% 등 11개 벤치마크에서 동시대 SOTA를 일거에 경신했다.

기존 패러다임과의 결정적 차이는 ① **사전학습(Pre-training) -> Fine-tuning의 2-stage** 표준화, ② task-specific architecture를 거의 변경하지 않는 **parameter sharing**, ③ 110M/340M 파라미터의 거대 모델을 **사전학습 1회 + 다수 downstream fine-tuning**으로 비용 분산하는 경제성 모델이다. 단, "사전학습 데이터 편향이 downstream으로 전이되는가", "few-shot 능력이 부족한가"라는 한계는 GPT-3(2020) 출현으로 다시 autoregressive decoder-only 패러다임의 부활을 촉발하게 된다.

```text
+--------------------------------------------------------------------+
|         BERT 이전 NLP 파이프라인 (Task-specific Architectures)    |
|                                                                    |
|  [Tokenize] -> [Word2Vec/GloVe] -> [LSTM/Conv/CNN] -> [Task Head]    |
|                                  ^ task마다 architecture 재설계   |
|                                  ^ 단방향/양방향 LSTM 별도 학습     |
+--------------------------------------------------------------------+
                              |
                              v  Pre-training + Fine-tuning 통합
+--------------------------------------------------------------------+
|                BERT 이후 표준 파이프라인 (2018~)                    |
|                                                                    |
|  Stage 1: Pre-training (1회, 수천 GPU·days)                        |
|    [Corpus 3.3B words] -> [WordPiece] -> [Transformer-Encoder]     |
|                                ^ MLM 15% mask + NSP                |
|                                ^ 양방향 self-attention              |
|                                                                    |
|  Stage 2: Fine-tuning (Task별 수 시간~수 일)                       |
|    [Downstream data] -> [Frozen-BERT + Linear classifier]           |
|                       ^ 분류/QA/NER/추출 모두 동일한 input format  |
+--------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: BERT 이전의 NLP는 **"문제마다 새 다리를 일일이 건설하는 토목 공사"**였고, BERT는 **"한 번 만든 고속도로 8차선(Transformer) 위에 어떤 차(QA·NER·감성분석)든 마음껏 달릴 수 있게 한 민자 고속도로"**다. 도로(사전학습 모델)는 한 번만 닦고, 차(태스크)만 바꾸면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

BERT의 핵심은 **Transformer Encoder 레이어를 N개 적층**한 self-attention 구조에서 발생한다. 입력 토큰은 ① Token Embedding(WordPiece subword), ② Segment Embedding(문장 A/B 구분), ③ Position Embedding(절대 위치, sinusoidal이 아닌 learned)의 합산으로 표현되며, 각 레이어에서 Multi-Head Self-Attention(MHA) -> Add & LayerNorm -> Feed-Forward(FFN, 4×hidden) -> Add & LayerNorm을 거친다. MHA의 핵심은 **Query·Key·Value로 사영된 hidden state 사이의 scaled dot-product `softmax(QKᵀ/√dₖ)V`** 이며, 모든 토큰이 모든 토큰을 동시에 attend하여 양방향 문맥이 단일 layer에서 융합된다.

사전학습은 두 가지 비지도 태스크로 구성된다. 첫째, **MLM(Masked Language Model)**은 입력 토큰의 15%를 무작위로 선택하여 ① 80%는 `[MASK]` 토큰으로, ② 10%는 무작위 토큰으로, ③ 10%는 원본 그대로 치환한 뒤, 원래 토큰을 복원하도록 학습한다. 80/10/10 분기는 fine-tuning 단계에 `[MASK]`가 등장하지 않는 mismatch를 완화하고, encoder가 context word를 그대로 "copy"하지 못하도록 강제하는 regularizer다. 둘째, **NSP(Next Sentence Prediction)**은 50%는 실제 연속 문장쌍(IsNext), 50%는 서로 무관한 문장쌍(NotNext)을 binary classification하며, `[CLS]` 토큰의 최종 hidden state가 입력 쌍의 관계를 encode한다.

Fine-tuning 단계에서는 `[CLS]` 위치에 classification head(`tanh` -> `Linear(C×H)`)를 부착하거나, 질문·지문·답 후보의 start/end span을 예측하는 QA head를 부착한다. 모든 파라미터가 end-to-end로 학습되며, learning rate 2e-5~5e-5, batch 16~32, epoch 2~4의 작은 스케일이 안정적 수렴의 표준이다.

```text
        [CLS]   The   [MASK]   sat    on    the    mat    .    [SEP]
          |      |     |        |      |     |      |      |      |
          v      v     v        v      v     v      v      v      v
Token :   T[CLS]  T_The  T_cat  T_sat  T_on  T_the  T_mat  T_._  T[SEP]
Seg   :    0       0     0      0      0     0      0      0      0
Pos   :    0       1     2      3      4     5      6      7      8
          +---------------+------------------------------------------+
                                   |
                                   v  (Element-wise Sum)
                          Embedding E ∈ ℝ^(L×H)
                                   |
       +---------------------------+---------------------------+
       v                           v                           v
   +-------+  +-------+  ...   +-------+  <- N = 12 (Base) / 24 (Large)
   | Layer |  | Layer |        | Layer |
   |  ×1   |  |  ×2   |        |  ×N   |
   +---+---+  +---+---+        +---+---+
       | Q·Kᵀ/√d -> softmax -> V  (12~16 heads)
       | Add & LayerNorm
       | FFN: H -> 4H -> H (GeLU)
       | Add & LayerNorm
       +-------------------------------+
                       |
                       v
       [CLS]_h  ->  C ∈ ℝ^H  (pooled output for classification)
       각 위치 h  ->  token별 representation (NER/QA용)
                                   |
          +------------------------+------------------------+
          v                        v                        v
   Pre-training Head 1:   Pre-training Head 2:    Fine-tuning Head:
   MLM: 각 [MASK]/치환     NSP: [CLS] pooled ->      Task-specific
   위치에서 vocab          Sigmoid(IsNext)         (Linear, CRF,
   softmax 복원                                     Span head 등)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **WordPiece Tokenizer** | Subword 단위 토큰화 | 30,522 vocab(영어 base), BPE와 유사한 greedy longest-match + likelihood 기반 merge; OOV·형태론·합성어 처리의 기본 단위, 한국어·일본어 등 비공식 언어는 mecab/soynlp/kiwi 기반 별도 tokenizer 필요 |
| **Embedding Sum** | 3개 embedding의 element-wise addition | Token + Segment(0/1) + Learned Position; sinusoidal이 아닌 **학습 가능한 절대 위치 임베딩**(max 512), 이를 통해 같은 layer에서도 위치 정보 보존 |
| **Multi-Head Self-Attention** | 문맥 융합 | `head_i = softmax(QWᵢQ · KWᵢKᵀ / √dₖ)VWᵢV`; BERT-base H=768, A=12 -> dₖ=64; Multi-head가 서로 다른 부분공간(구문·의미·지시 등)을 병렬 학습 |
| **Feed-Forward Network (FFN)** | 비선형 변환 | `FFN(x) = max(0, xW₁ + b₁)W₂ + b₂` (ReLU) 또는 GeLU; hidden 4H intermediate; position-wise 적용으로 attention이 만든 representation을 refine |
| **Pre-training Task: MLM** | 15% 마스킹 단어 복원 | 80% `[MASK]`, 10% random token, 10% original; 예측 시 **전체 vocab에 대한 softmax**로 cross-entropy loss 계산; non-mask 위치는 loss에서 제외(`-100` 라벨) |
| **Pre-training Task: NSP** | 문장 간 관계 분류 | 50/50 binary, `[CLS]`의 pooled vector를 tanh -> Linear(2) -> Softmax; 실제 downstream NLI·QA 태스크와 유사 형태여서 transfer 유리 (단, 후속 연구 RoBERTa(2019)는 NSP의 효과성을 부정하고 dynamic MLM만으로 SOTA 달성) |
| **Pre-training Data** | 거대 unsupervised corpus | English Wikipedia 2.5B words + BooksCorpus 0.8B words = **3.3B words**; 단일 epoch 학습(SQuAD/Wikipedia의 반복 노출 방지), 128 batch × 1M steps |
| **Configuration (Base/Large)** | 모델 크기 | Base: L=12, H=768, A=12, FFN=3072, **110M params** / Large: L=24, H=1024, A=16, FFN=4096, **340M params**; Large는 Fine-tuning 시 1e-5~3e-5 LR이 안정적, 너무 크면 catastrophic forgetting |
| **Special Tokens** | 시퀀스 구조 명시 | `[CLS]`(분류용 pooled), `[SEP]`(문장 구분), `[PAD]`(배치 정렬, attention mask=0), `[MASK]`(MLM 전용, fine-tuning 시 미사용), `[UNK]`(vocab 밖 토큰) |
| **Pooled Output** | 문장·문장쌍 표현 | `[CLS]`의 마지막 hidden state를 Tanh -> Linear(H×H) 통과 -> C ∈ ℝ^H; NSP 사전학습 시 학습된 weight이 downstream 분류 head와 semantic 정렬 |
| **Fine-tuning Hyperparams** | 안정적 수렴 | learning rate 2e-5~5e-5, batch 16~32, epochs 2~4, max_seq_len 128(분류)/384(QA), weight decay 0.01, warmup 10%, AdamW(β₁=0.9, β₂=0.999, ε=1e-6), dropout 0.1 |

**핵심 공식 및 알고리즘 요약**:
- **Scaled Dot-Product Attention**: `Attention(Q,K,V) = softmax(QKᵀ/√dₖ)V`, 스케일링은 dₖ 증가 시 dot-product 분산이 커져 softmax gradient가 saturate되는 문제 완화
- **MLM Loss**: `L_MLM = -Σ_{i∈M} log P(xᵢ | x̃)`, M은 15% 마스킹된 위치 집합, x̃는 corruption된 입력
- **Joint Pre-training Loss**: `L = L_MLM + L_NSP` (단순 합산, 가중치는 동일)
- **Fine-tuning Objective**: `P(y|x) = softmax(W_o · h_[CLS] + b_o)`, 분류 태스크는 cross-entropy, QA 태스크는 start/end span probability의 joint log-likelihood

- **📢 섹션 요약 비유**: BERT의 MLM은 **"신문에서 15% 단어를 검게 칠하고 80%는 빈칸, 10%는 엉뚱한 단어, 10%는 원래 단어로 바꾼 뒤, 주변 단어만 보고 원래 단어를 맞히기"**다. 빈칸 80%만 정답이면 단순히 mask 패턴을 외우니까, 10%는 엉뚱한 단어로 교란하고 10%는 정상으로 두어 **"진짜 복원 능력"**을 길러주는 것이다. 옆사람(좌/우 문맥)을 동시에 들여다볼 수 있다는 점이 단방향 GPT와 결정적으로 다르다.

---

## Ⅲ. 비교 및 연결

BERT는 **사전학습 패러다임의 3대 축**(encoder-only / decoder-only / encoder-decoder) 중 encoder-only 계열의 표준이다. 비교군으로는 ① ELMo(BiLSTM, shallow bidirectional), ② GPT-1/2/3(decoder-only, autoregressive), ③ T5/BART(encoder-decoder, seq2seq)가 대표적이다.

| 구분 | **ELMo (2018-02)** | **GPT-1 (2018-06)** | **BERT-Base (2018-10)** | **RoBERTa (2019-07)** | **GPT-3 (2020-05)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | BiLSTM (forward + backward LM concat) | Transformer Decoder (12 layers, masked self-attn) | **Transformer Encoder (12 layers, full self-attn)** | Transformer Encoder (BERT와 동일, large 24L) | Transformer Decoder (96 layers, 175B params) |
| **방향성** | Shallow bidirectional (좌/우 concat