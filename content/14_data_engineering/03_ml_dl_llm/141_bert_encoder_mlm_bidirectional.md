---
title: "Bert Encoder Mlm Bidirectional"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 141
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BERT Encoder는 <strong>Transformer Encoder를 12/24층 쌓아</strong> MLM(15% 마스킹)과 NSP로 양방향 사전 학습한 모델이며, [CLS] 토큰으로 분류·유사도, 각 토큰 출력으로 NER·QA를 수행한다.
> 2. **가치**: BERT-Base(110M)·BERT-Large(340M)의 사전 학습 후, <strong>소량의 라벨 데이터로 Fine-tuning</strong>하면 11개 NLU 벤치마크를 동시 갱신(2018)하여 "사전 학습+미세 조정" 패러다임을 확립했다.
> 3. **판단 포인트**: WordPiece 토크나이저(30K vocab), 최대 512 토큰, [CLS]+SEP] 특수 토큰이 입력 구조이며, Sentence-BERT로 임베딩·검색에 특화된 변형이 활용된다.

---

## Ⅰ. 개요 및 필요성

```text
BERT 입력: [CLS] 문장A [SEP] 문장B [SEP]
  -> Token Embedding + Segment Embedding + Position Embedding
  -> Encoder × 12 -> 출력
  [CLS] 벡터: 분류·유사도
  각 토큰 벡터: NER·QA 태깅
```

- **📢 섹션 요약 비유**: BERT는 <strong>독해 시험의 달인</strong>이다. 지문(양방향 문맥)을 완벽히 이해하고, 질문(Fine-tuning)에 따라 답을 내놓는다.

---

## Ⅱ~Ⅴ. 결론

BERT Encoder는 <strong>NLU의 사전 학습 표준</strong>을 확립했으며, 임베딩·검색·분류에서 여전히 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>BERT Encoder</strong> | 12/24층 Transformer |
| **[CLS]** | 분류·유사도 토큰 |
| **WordPiece** | 서브워드 토크나이저 |
| <strong>Fine-tuning</strong> | 소량 라벨 적응 |
| <strong>Sentence-BERT</strong> | 임베딩 특화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Word2Vec (2013)] -> [ELMo (2018)] -> [BERT (2018)]
    -> [RoBERTa (2019)] -> [DeBERTa (2020)]
    -> [Sentence-BERT (SBERT, 2019)]
    -> [현재: E5/BGE — 임베딩 모델 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BERT는 <strong>독해 시험 달인</strong>이에요. 지문의 <strong>앞뒤를 다 이해</strong>해요.
2. [CLS] 토큰은 <strong>전체 요약 점수</strong>예요. 이걸로 분류·비교를 해요.
3. 적은 연습(Fine-tuning)만으로도 <strong>다양한 시험</strong>을 잘 볼 수 있어요!
