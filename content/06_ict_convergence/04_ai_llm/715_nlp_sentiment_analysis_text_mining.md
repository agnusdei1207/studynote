---
title: "NLP Sentiment Analysis Text Mining"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 715
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비정형 텍스트에서 형태소 분석(MeCab/KoNLPy), 임베딩(Word2Vec/BERT), 분류 모델(BiLSTM/Transformer) 파이프라인을 통해 문서·문장·속성 단위의 극성(Polarity: Positive/Negative/Neutral)과 감정 강도(Intensity)를 정량화하는 기법으로, Lexicon(사전 기반)·ML(SVM/Naive Bayes)·DL(BERT/KoELECTRA) 세 가지 패러다임이 계층적으로 결합되어 동작합니다.
> 2. **가치**: Gartner 보고 기준 고객VOC 분석 자동화로 VOC 처리량 약 80% 절감, NSAT(Net Sentiment Score) 기반 의사결정 시 제품 회수·CS 비용 15~40% 감소 효과가 보고되며, 실시간 소셜리스닝을 통한 브랜드 위기 탐지 리드타임을 24~72시간 -> 30분 이내로 단축시킵니다.
> 3. **판단 포인트**: 도메인 적응(Domain Adaptation)·라벨 편향·문맥 의존성(특히 반어법/풍자)·한국어 처리의 교착어 특성(조사/어미 변형)·저자원 도메인(의료/법률)의 F1-score 90% 이상 확보 여부가 핵심 트레이드오프이며, Lexicon 경량 모델과 LLM 고도화 모델의 하이브리드 아키텍처 설계가 실무 핵심입니다.

---

## Ⅰ. 개요 및 필요성

비정형 텍스트 데이터는 전 세계 데이터의 약 80~90%를 차지하며(IBM, 2024), 그 중 한국어 데이터는 교착어적 특성(조사·어미 변형, 띄어쓰기 비일관성, 한자어·외래어 혼재)으로 인해 영어 대비 처리 난이도가 1.5~2배 높은 것으로 알려져 있습니다. 감성 분석(Sentiment Analysis)과 텍스트 마이닝(Text Mining)은 이러한 비정형 데이터를 정형화된 인사이트로 변환하여, 마케팅·금융·의료·공공 정책 결정에 활용하는 핵심 기술입니다.

기존 설문조사·정형 리포트 기반의 VOC(Voice of Customer) 분석은 표본 크기 제한(통상 1,000~3,000명), 응답 편향(Response Bias), 분석 리드타임 2~4주로 한계가 있었습니다. NLP 기반 자동화는 1) 비정형 데이터의 실시간 수집(크롤링·API), 2) 전처리·특성 추출의 자동화, 3) 대규모 코퍼스에서 의미·감정·토픽의 패턴 추출을 가능케 하여 패러다임 전환을 이끌었습니다.

특히 2017년 Attention Is All You Need(Vaswani et al.) 이후 Transformer 기반 사전학습 모델(BERT, GPT, KoELECTRA, KLUE-RoBERTa)이 등장하면서, 별도 도메인 라벨링 없이도 문맥적 감성 분석이 가능해졌고, F1-score 기준 90% 이상의 정확도를 안정적으로 달성하는 시대가 도래했습니다.

```text
[텍스트 마이닝 & 감성 분석 전체 시스템 아키텍처]

 +-------------------------------------------------------------------------+
 |                          DATA INGESTION LAYER                           |
 |  +----------+  +----------+  +----------+  +----------+  +----------+  |
 |  |   Web    |  |  Social  |  |   E-     |  |   IoT    |  | Internal |  |
 |  | Crawling |  |   API    |  | Commerce |  |  Log/    |  |   CRM    |  |
 |  |(Scrapy)  |  |(Twitter/ |  | Review   |  |  Sensor  |  | /ERP     |  |
 |  |          |  |  Naver)  |  |   API    |  |   Text   |  |  Text    |  |
 |  +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+-----+  |
 |       +--------------+-----+-------+-------------+--------------+       |
 +-----------------------------+-------------------------------------------+
                               v
 +-------------------------------------------------------------------------+
 |                    PRE-PROCESSING LAYER (전처리)                        |
 |  +------------+  +------------+  +------------+  +------------+        |
 |  | Cleansing  |-->| Tokenizing |-->|  Morpheme  |-->|   NER &    |        |
 |  |(HTML/특수  |  |  (MeCab/   |  |  Analysis  |  | POS Tagging|        |
 |  |  문자 제거)|  |  Kiwi)     |  |  (KoNLPy)  |  |            |        |
 |  +------------+  +------------+  +------------+  +------------+        |
 +-------------------------------------+-----------------------------------+
                                       v
 +-------------------------------------------------------------------------+
 |                  FEATURE EXTRACTION & MODELING LAYER                    |
 |  +------------+  +------------+  +------------+  +------------+        |
 |  |  Lexicon   |  |    ML      |  | Deep Learn |  | Transformer|        |
 |  |   Based    |  |  (SVM,NB,  |  |  (CNN,     |  |  (BERT,    |        |
 |  | (VADER,    |  |  LR, RF)   |  |  BiLSTM,   |  | KoELECTRA, |        |
 |  |  KNU)      |  |  TF-IDF    |  |  Attention)|  |  KLUE)     |        |
 |  +-----+------+  +-----+------+  +-----+------+  +-----+------+        |
 |        +-------+-------+-------+-------+-------+-------+                |
 |                v               v               v                         |
 |        +--------------------------------------------+                  |
 |        |   HYBRID ENSEMBLE / STACKING                |                  |
 |        |   (Lexicon + ML + DL 다중 모델 앙상블)     |                  |
 |        +--------------------------------------------+                  |
 +-------------------------------------+-----------------------------------+
                                       v
 +-------------------------------------------------------------------------+
 |                  INSIGHT & VISUALIZATION LAYER                          |
 |  +------------+  +------------+  +------------+  +------------+        |
 |  | Sentiment  |  |  Topic     |  |  Aspect-   |  |  Dashboard |        |
 |  |  Score     |  |  Modeling  |  |  Based SA  |  | (Kibana/   |        |
 |  |  (Polarity |  |  (LDA,     |  | (속성별    |  |  Tableau/  |        |
 |  |   + 강도)  |  |  BERTopic) |  |  극성)     |  |  Grafana)  |        |
 |  +------------+  +------------+  +------------+  +------------+        |
 +-------------------------------------------------------------------------+
```

**기존 vs 새로운 패러다임 비교**:
- **기존(Legacy)**: 정형 설문(다중선택, 5점 척도) -> SPSS 통계 분석 -> 정성 보고서 작성 -> 의사결정 (2~4주 소요)
- **신규(Modern)**: 비정형 텍스트 실시간 수집 -> 자동 전처리 -> 딥러닝 분류/추출 -> 대시보드 시각화 -> 자동 알림 (수 분~수 시간)

- **📢 섹션 요약 비유**: 감성 분석은 마치 **"수많은 손님들의 흩어진 수다를 AI 통역사가 실시간으로 받아쓰고, 그중 '칭찬·불만·제안'으로 자동 분류해 점장에게 알림을 보내는 시스템"**과 같습니다. 텍스트 마이닝은 그 통역사가 뽑아낸 단어들 사이의 숨은 연관관계(예: "배터리"와 "불만"의 동시출현)를 지도 위에 표시해 큰 흐름을 보여주는 일입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. 핵심 처리 파이프라인 (5단계)

1. **수집(Collection)**: Web Crawling(Scrapy/BeautifulSoup), Streaming API(Kafka + Spark Streaming), RSS 피드, 내부 CRM 텍스트
2. **전처리(Preprocessing)**: HTML 태그 제거, 정규식 기반 클렌징, 중복 제거(Hashing/Deduplication), 노이즈 필터링
3. **형태소 분석(Tokenization & Morphological Analysis)**: 한국어의 경우 **MeCab-ko**(속도 최우선, mecab-ko-dic), **Kiwi**(신조어·띄어쓰기 보정 우수), **KoNLPy의 OKT/Mecab/Hannanum/Kkma** 중 사용
4. **특성 벡터화(Vectorization)**: TF-IDF, Word2Vec/SGNS, FastText(Subword), Contextualized Embedding(BERT hidden states)
5. **분류/추출(Classification/Extraction)**: 감성 극성 분류, NER(개체명 인식), ABSA(속성 기반 감성 분석), 관계 추출

### B. 주요 알고리즘별 동작 원리

- **Lexicon 기반**: 감성 사전(KNU, SentiWordNet, VADER)을 lookup하여 단어별 polarity(-1 ~ +1) 합산 -> S = Σ(w_i · p_i) / √N (정규화)
- **ML 기반(지도학습)**: TF-IDF 벡터 -> SVM(커널 트릭으로 고차원 분리), Naive Bayes(P(c|d) ∝ P(c)∏P(w_i|c)), Logistic Regression
- **DL 기반**: BiLSTM(양방향 시퀀스) + Attention(중요 단어 가중치), CNN(n-gram 필터), Transformer(Self-Attention)
- **사전학습 언어모델(PLM)**: MLM(Masked Language Modeling) + NSP(Next Sentence Prediction) 사전학습 -> Fine-tuning on 감성 데이터 (보통 1,000~10,000 라벨)

```text
[Transformer 기반 감성 분류 내부 동작 메커니즘]

   Input: "이 폰은 가격은 비싸지만, 카메라 성능은 정말 훌륭하다"
                              |
   +--------------------------v--------------------------+
   |  1) Tokenization (WordPiece / SentencePiece)        |
   |     ["이", "##폰", "##은", "가격", "##은", "비싸",   |
   |      "##지만", ",", "카메라", "성능", "##은",         |
   |      "정말", "훌륭", "##하다"]                        |
   +--------------------------+--------------------------+
                              v
   +------------------------------------------------------+
   |  2) Embedding = Token + Segment + Position           |
   |     각 토큰 -> 768-dim vector (BERT-base)             |
   |     + Self-Attention: 각 토큰이 다른 모든 토큰 참조  |
   +--------------------------+--------------------------+
                              v
   +------------------------------------------------------+
   |  3) Multi-Head Self-Attention × 12 layers            |
   |     Q·K^T -> softmax -> 가중치 × V                    |
   |     Head 1~12가 서로 다른 관계(품사/의존/대조) 학습   |
   |                                                      |
   |     "비싸지만" <--> "훌륭하다" (대조 관계 캡처)        |
   |     "카메라"     <--> "성능"     (속성-평판 연결)       |
   +--------------------------+--------------------------+
                              v
   +------------------------------------------------------+
   |  4) [CLS] token pooled representation -> Dense(3)     |
   |     Softmax -> [Positive: 0.78, Neutral: 0.05,        |
   |                Negative: 0.17]                        |
   +--------------------------+--------------------------+
                              v
   Output: Aspect-Based Sentiment
     - 속성 {카메라}: Positive (0.92)
     - 속성 {가격}:  Negative  (0.85)
     - 종합(문서):  Positive (0.65)  <- 가중 평균
```

### C. 한국어 처리의 특수성

| 현상 | 예시 | 처리 방법 |
|:---|:---|:---|
| 교착어 | "가까웠다 -> 가깝 + 었 + 다" | 형태소 분리 + 어간 추출 |
| 띄어쓰기 비일관성 | "진짜좋아요" / "진짜 좋아요" | BERT의 Subword로 흡수 |
| 신조어·줄임말 | "존맛탱", "갓생", "TMI" | 신조어 사전 + kiwi 등 최신 tokenizer |
| 한자어·외래어 혼재 | "서비스 quality" | 다국어 임베딩(mBERT) 또는 정규화 |
| 반어/풍자 | "대박이다 진짜..." (부정) | 문맥 모델 + 감정 강도 feature 병합 |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **형태소 분석기** | 토큰 분리 + 품사 태깅 | MeCab-ko (F1 ≈ 97%), Kiwi (신조어 95%+), KoNLPy OKT (개발 편의성) |
| **임베딩 모듈** | 토큰 -> 밀집 벡터 변환 | Word2Vec(SGNS, 차원 100~300), FastText(Subword OOV 대응), BERT(768~1024-dim, 문맥 반영) |
| **분류 모델** | 극성(Polarity) 판별 | BiLSTM+Attention(중소규모 데이터), KoELECTRA(70M 파라미터, 한국어 SOTA), LLM(GPT-4/Claude, Zero/Few-shot) |
| **속성 추출기(ABSA)** | 속성-감정 페어 추출 | LSTM-CRF 시퀀스 라벨링, BERT-MRC(질의응답 기반), Instruction-Tuning LLM |
| **토픽 모델러** | 잠재 주제 추출 | LDA(통계적, gensim), BERTopic(HNSW + c-TF-IDF, 최신), Top2Vec |
| **평가/모니터링** | 성능/드리프트 감시 | Accuracy, Macro-F1, Cohen Kappa, Calibration(ECE), Data Drift(PSI/KS-test) |

### D. 핵심 수식 및 파라미터

- **TF-IDF**: `tfidf(t,d) = tf(t,d) · log(N / df(t))`
- **Attention Score**: `Attention(Q,K,V) = softmax(QK^T / √d_k)V`
- **Loss(감성 분류)**: `L = -Σ y_i log(ŷ_i) + λ‖θ‖²` (L2 정규화)
