---
title: "NLP NER Sentiment Analysis Summarization"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 666
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NER(개체명 인식)·감성 분석·자동 요약은 비정형 텍스트에서 **구조화(Structured Information)**, **극성 판별(Polarity)**, **의미 압축(Semantic Compression)**을 수행하는 3대 핵심 NLP 태스크이며, 현대에는 Transformer Encoder/Decoder 구조(KoBERT, KLUE-BERT, BART, T5, GPT 계열) 위에서 End-to-End로 통합 구현된다.
> 2. **가치**: 콜센터 VOC 분석 자동화 시 **처리량 80% 이상 향상**, 뉴스/법령/계약서 요약을 통한 **MTTR(Mean Time To Read) 70% 단축**, NER 기반 지식그래프 구축으로 **검색 정확도 35~50% 개선** 등 정량적 ROI가 입증된 기술이다.
> 3. **판단 포인트**: 도메인·언어(한국어 형태소 복잡도)·지연시간(SLO)·라벨 데이터 규모에 따라 **Rule+ML 하이브리드 vs. Fine-tuned PLM vs. LLM(Zero-shot/In-context)** 중 최적 아키텍처를 선택해야 하며, 추론 비용과 정확도·재현율·해석가능성(XAI) 간 트레이드오프가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

자연어 처리(NLP)는 사람이 사용하는 비정형 텍스트 데이터를 기계가 이해·생성·변환할 수 있도록 하는 AI의 핵심 분야다. 그중 **개체명 인식(NER)**, **감성 분석(Sentiment Analysis)**, **자동 요약(Automatic Summarization)**은 산업 현장에서 가장 빈번하게 요구되는 3대 태스크로, ① BI/CRM 데이터의 구조화, ② VOC(Voice of Customer)·SNS 모니터링, ③ 보고서·약관·판결문 등의 지식 노동 자동화에 직결된다.

과거에는 **사전기반(Lexicon-based)**, **통계기반(HMM/CRF/SVM)** 방식이 주를 이루었으나, 한국어는 교착어적 특성(조사·어미 변화), 띄어쓰기 오류, 신조어·은어, 장르별 문체 변동이 극심하여 정밀도(F1)가 70%대에 그쳤다. 2018년 **BERT(Bidirectional Encoder Representations from Transformers)** 등장 이후, **사전학습 언어모델(Pre-trained Language Model, PLM)** 기반 Fine-tuning이 표준이 되었고, **KoBERT, KLUE-BERT, KoBigBird, KR-ELECTRA** 등 한국어 특화 모델이 F1 90% 이상의 성능을 보인다. 최근에는 **GPT-4, Claude, LLaMA3, HyperCLOVA X** 같은 LLM의 In-context Learning·Zero-shot 능력을 활용하여 라벨링 비용 없이도 NER/감성/요약을 통합 수행하는 추세로 패러다임이 전환되고 있다.

```text
[ 비정형 텍스트 입력 흐름 -> 3대 NLP 태스크 통합 파이프라인 ]

   +----------------------------------------------------------------+
   |  Raw Text Sources (콜센터 transcripts / 뉴스 / 계약서 / SNS)   |
   +-------------------------------+--------------------------------+
                                   | ① 전처리
                                   v
   +----------------------------------------------------------------+
   |  Preprocessing: 형태소 분석(Mecab/Okt) -> 정규화 -> 토큰화(BPE)  |
   |                -> 불용어 제거 -> Subword Encoding (WordPiece)     |
   +-------------------------------+--------------------------------+
                                   | ② 임베딩 (768~4096d)
                                   v
   +----------------------------------------------------------------+
   |  Shared Encoder Backbone (KoBERT / KLUE-RoBERTa / BERT-base)   |
   |   +-► NER Head (Token Classification + CRF)                   |
   |   +-► Sentiment Head (Sequence Classification, ABSA)          |
   |   +-► Summarization Head (Encoder-Decoder: BART/T5/HSG)       |
   +-------------------------------+--------------------------------+
                                   | ③ 태스크별 출력
                +------------------+------------------+
                v                  v                  v
        +------------+      +------------+      +------------+
        |  NER 출력  |      | 감성 출력  |      |  요약 출력  |
        | [ORG:삼성] |      | 부정(0.92) |      | "주요 쟁점 |
        | [PER:홍길동|      | 대상:배터리|      |  3가지로  |
        |  [LOC:서울]|      | ABSA 감성  |      |  요약..."  |
        +------------+      +------------+      +------------+
                |                  |                  |
                +------------------+------------------+
                                   v
   +----------------------------------------------------------------+
   |  Downstream: 지식그래프 / 대시보드 / 알림 / Search Index       |
   +----------------------------------------------------------------+
```

**📢 섹션 요약 비유**: NLP 파이프라인은 마치 **"식당 주방"**과 같다. 손님(원시 텍스트)이 들어오면, 前처리(세미·손질) -> 공통 냉장고(임베딩) -> 3가지 요리(NER·감성·요약) -> 플레이팅(시각화) 순으로 흘러간다. 한 번 손질해 둔 재료(Shared Encoder)를 여러 요리에 재활용하는 것이 모던 NLP의精髓다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. NER (Named Entity Recognition, 개체명 인식)

NER은 문장 내 토큰에 대해 **BIO / BIOES 태깅 스킴**으로 라벨링하는 **Token Classification** 태스크다. 현대 아키텍처는 **Transformer Encoder + Softmax (또는 CRF)**로 구성된다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Token Embedding** | 토큰별 벡터 변환 | WordPiece(영어), Mecab+OOV(한국어) -> 768d 벡터 |
| **Contextual Encoder** | 문맥 반영 양방향 인코딩 | 12-layer Transformer, Multi-Head Self-Attention, [CLS]/[SEP] 포함 |
| **NER Head (Classifier)** | 각 토큰별 클래스 예측 | `nn.Linear(hidden, num_labels)` -> Softmax 또는 CRF |
| **CRF Layer (선택)** | 라벨 시퀀스 전이 제약 학습 | Viterbi 디코딩으로 `B-PER -> I-PER`는 가능, `B-PER -> I-LOC`는 차단 |
| **한국어 특화 모듈** | 형태소 정보 융합 | MeCab-ko + 음절/자모 임베딩 결합, KoSpacing으로 띄어쓰기 보정 |

**핵심 수식 (CRF Loss)**:
$$P(y|x) = \frac{\exp\left(\sum_i (W_{y_i} h_i + T_{y_{i-1}, y_i})\right)}{Z(x)}$$
- $W_{y_i}$: Emission score, $T_{y_{i-1}, y_i}$: Transition score
- 학습 시 Negative Log-Likelihood 최소화, 추론 시 **Viterbi 알고리즘**으로 최적 시퀀스 탐색

### B. 감성 분석 (Sentiment Analysis)

감성 분석은 문서/문장/속성(Aspect) 단위로 **극성(Positive/Negative/Neutral)**과 **강도(Intensity)**를 예측한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Document-level Classifier** | 문서 전체 감성 판별 | BERT[CLS] -> Dense -> Softmax (3~5 class) |
| **Aspect-Based SA (ABSA)** | 속성별 감성 분리 | Aspect Term Extraction (ATE) + Aspect Sentiment Classification (ASC) |
| **Lexicon Layer (Hybrid)** | 사전 기반 보조 점수 | KNU 감성사전, SentiWordNet, KOSAC — 도메인 특화 사전 매칭 |
| **Fine-grained Head** | 5~7단계 강도 회귀 | Ordinal Regression, Sigmoid 출력 + Threshold Tuning |
| **Multilingual Extension** | 다국어 통합 | XLM-RoBERTa, mBERT, mDeBERTa — 한국어/영어/일본어 통합 |

**ABSA 4-Tuple 태스크**: `{Aspect Category, Opinion Term, Sentiment Polarity, Opinion Holder}` — 예: `"이 노트북의 배터리는 정말 별로다"` -> `{배터리, 별로, 부정, 화자}`

### C. 자동 요약 (Summarization)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Extractive Selector** | 원문에서 핵심 문장 선택 | TextRank(PageRank on Sentence Graph), BERTSumExt (Transformer + Interval Segment Embedding), Lead-3 Baseline |
| **Abstractive Generator** | 새로운 문장 생성 | Encoder-Decoder(BART, T5, PEGASUS), Pointer-Generator Network with Coverage |
| **Hybrid Reranker** | 추출+생성 결합 | Candidate Generation (Extractive) -> Rerank (Cross-Encoder) -> Paraphrase (Seq2Seq) |
| **Long-Input Handler** | 긴 문서 처리 | Sparse Attention (Longformer, BigBird), Hierarchical Attention (HSG), Chunk-and-Merge |
| **Constrained Decoding** | 환각(Hallucination) 억제 | Extractiveness Constraint, Faithfulness Scoring (FactCC, QAGS) |

**📢 섹션 요약 비유**: NER은 **"문서에서 형광펜 치기"**, 감성 분석은 **"온도계로 기분 재기"**, 요약은 **"긴 영화를 1분 예고편으로 편집하기"**다. 셋 다 원본을 그대로 두면서 의미만 추출/변환한다는 점은 공통이다.

```text
[ 통합 아키텍처: Multi-Task Learning (MTL) with Shared Encoder ]

                    Input: "삼성전자의 신형 갤럭시 배터리는 훌륭하지만, 가격은 비싸다."
                                          |
                          +---------------+---------------+
                          v                                v
                  [Mecab 형태소 분석]               [WordPiece Tokenizer]
                  삼성/NNG 전자/NNG ...               ['삼성', '##전자', '##의', ...]
                          |                                |
                          +---------------+----------------+
                                          v
                  +--------------------------------------------+
                  |    Shared Transformer Encoder (12 layers)  |
                  |  KoBERT-large / KLUE-RoBERTa-large         |
                  |  Hidden=1024, Heads=16, FFN=4096          |
                  +--------+----------+----------+-------------+
                           |          |          |
              +------------+          |          +------------+
              v                       v                        v
     [NER Head + CRF]         [Sentiment Head]        [Summarization Decoder]
       BIO Tagging            [CLS] Pooling             (BART Decoder)
              |                       |                        |
              v                       v                        v
   [B-ORG, I-ORG, O,          logits=[neg:0.05,         "갤럭시 배터리는
    B-PROD, O, O, ...]         neu:0.10, pos:0.85]      우수하나 고가"
           |                          |                       |
           v                          v                       v
       NER Result              Aspect: 배터리(+),         Summary
       [ORG:삼성전자]          가격(-)                    (Extractive or
       [PROD:갤럭시]            ABSA: Mixed                Abstractive)
```

**MTL Loss 결합식**:
$$L_{total} = \alpha L_{NER} + \beta L_{Sentiment} + \gamma L_{Sum} + \lambda \|\theta_{shared}\|_2$$
- 일반적으로 $\alpha, \beta, \gamma$는 1.0, Shared Layer는 LR을 0.1배로 낮춰 Catastrophic Forgetting 방지

---

## Ⅲ. 비교 및 연결

### A. 3대 태스크 접근 방식 비교

| 구분 | Rule/Lexicon | Traditional ML | Deep Learning (PLM Fine-tune) | LLM (Zero/Few-shot) |
| :--- | :--- | :--- | :--- | :--- |
| **NER** | 정규식 + Gazetteer | CRF, SVM, MEM | BiLSTM-CRF, BERT-CRF, KoBERT | GPT-4 + Function Calling, GLiNER |
| **감성 분석** | SentiWordNet 매칭 | Naive Bayes, SVM, LR | TextCNN, BiLSTM-Attention, KoBERT | GPT-4, Claude Sonnet, Llama3-Instruct |
| **요약** | Lead-3, TF-IDF | TextRank, LexRank | BERTSum, BART, T5, PEGASUS | GPT-4, Claude-3, HyperCLOVA X |
| **학습 데이터** | 0 (사전만) | 수만~수십만 라벨 | 수만 라벨 + 100GB 사전학습 | 0~수십 예시(In-context) |
| **추론 속도** | <1ms | 5~20ms | 50~200ms (GPU) | 1~10s (API), 100~500ms (vLLM) |
| **정확도 (한국어 평균 F1)** | 60~75% | 75~85% | 88~94% | 80~92% (도메인 의존) |
| **해석 가능성** | ★★★★★ | ★★★★ | ★★ | ★ |
| **운영비 (1M req 기준)** | $0.1 | $5 | $30 | $300~2,000 |
| **도메인 적응** | 수동 사전 추가 | 재학습 | Fine-tune (LoRA 가능) | Prompt Engineering + RAG |

### B. Extractive vs. Abstractive 요약

| 기준 | Extractive (TextRank/BERTSum) | Abstractive (BART/T5/GPT) |
| :--- | :--- | :--- |
| **출력 형태** | 원문 문장 그대로 발췌 | 새로운 문장 생성 |
| **Faithfulness** | 높음 (환각 없음) | 낮음 (환각 위험) |
| **유창성** | 원문