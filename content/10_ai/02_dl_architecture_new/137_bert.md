---
title: "BERT (Bidirectional Encoder Representations from Transformers)"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BERT는 <strong>Transformer의 Encoder만 사용</strong>하여 양방향(Bidirectional)으로 문맥을 이해하는 사전 학습 언어 모델이며, MLM(Masked Language Model)과 NSP(Next Sentence Prediction)로 학습한다.
> 2. **가치**: GPT(->방향)는 왼쪽 문맥만 보지만, BERT는 **양쪽 문맥을 동시에** 참조하여 "bank"가 은행인지 강둑인지 정확히 판별하며, NLU(자연어 이해) 11개 벤치마크를 동시 갱신(2018)했다.
> 3. **판단 포인트**: BERT는 <strong>이해(Classification·NER·QA)에 강하고 생성에 약하며</strong>, GPT는 생성에 강하다. 현재는 Encoder-Decoder(T5)·Decoder-only(GPT)가 주류이나 BERT 계열은 임베딩·검색에 여전히 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
BERT = Transformer Encoder × 12/24 Layer
  MLM: "나는 [MASK] 이다" -> "학생" 예측 (양방향)
  NSP: "문장 A 다음에 B가 오는가?" (문장 관계)
  -> Fine-tuning: 분류·NER·QA·유사도
```

- **📢 섹션 요약 비유**: GPT는 소설 작가(앞->뒤 생성), BERT는 편집자(앞뒤 맥락으로 이해·교정)이다.

---

## Ⅱ~Ⅴ. 결론

BERT는 <strong>NLU의 기반 모델</strong>이며, 임베딩(Sentence-BERT)·검색(RAG Retriever)에서 여전히 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>BERT</strong> | 양방향 Encoder |
| <strong>MLM</strong> | 빈칸 채우기 학습 |
| <strong>GPT</strong> | 단방향 Decoder (대조) |
| <strong>Sentence-BERT</strong> | 문장 임베딩 |
| **RoBERTa** | BERT 개선 (NSP 제거) |

### 📈 관련 키워드 및 발전 흐름도

```text
[ELMo (2018)] -> [BERT (Google, 2018.10)]
    -> [RoBERTa (2019)] -> [ALBERT (경량)]
    -> [DeBERTa (2020)] -> [현재: E5/BGE — 임베딩 특화 BERT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BERT는 <strong>편집자</strong>예요. 문장의 **앞뒤를 다 보고** 의미를 이해해요.
2. GPT는 **소설 작가**(앞->뒤 쓰기), BERT는 **교정자**(앞뒤 맥락 파악)예요.
3. "bank"가 **은행인지 강둑인지** 앞뒤 문맥을 보고 정확히 알아내요!
