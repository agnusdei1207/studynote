---
title: "Transfer Learning"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 132
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transfer Learning은 <strong>대규모 데이터로 사전 학습된 모델의 지식을 새로운 작업에 전이(재활용)</strong>하는 학습 기법이며, Foundation Model 시대의 핵심 패러다임이다.
> 2. **가치**: 처음부터 학습하면 GPU·데이터·시간이 막대하지만, 사전 학습 모델을 전이하면 <strong>소량 데이터로도 높은 성능</strong>을 달성(Few-shot)할 수 있다.
> 3. **판단 포인트**: Feature Extraction(동결)·Fine-tuning(미세 조정)·LoRA(효율적 미세 조정)를 구분하고, 도메인 유사도에 따라 전략을 선택한다.

---

## Ⅰ. 개요 및 필요성

```text
사전 학습 (ImageNet 100만장) -> 범용 표현 학습
  -> Fine-tuning (의료 X-ray 1000장) -> 전문 모델
  소량 데이터로도 높은 성능!
```

- **📢 섹션 요약 비유**: Transfer Learning은 <strong>대학 교양(사전 학습) 후 전공(Fine-tuning) 선택</strong>이다. 교양을 건너뛰면 전공도 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 방식 | 설명 | 데이터량 |
|:---|:---|:---|
| **Feature Extraction** | 모델 동결, 마지막 층만 | 극소량 |
| <strong>Fine-tuning</strong> | 전체/일부 층 재학습 | 중간 |
| <strong>LoRA/QLoRA</strong> | 저랭크 행렬만 학습 | **효율적** |

---

## Ⅲ~Ⅴ. 결론

Transfer Learning은 <strong>현대 AI의 기본 패러다임</strong>이며, LoRA/QLoRA로 소규모 팀도 LLM을 커스텀할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Transfer Learning</strong> | 지식 전이 |
| <strong>Fine-tuning</strong> | 전체 모델 미세 조정 |
| <strong>LoRA</strong> | 효율적 파라미터 미세 조정 |
| <strong>Foundation Model</strong> | 전이의 원천 |
| <strong>Domain Adaptation</strong> | 도메인 차이 극복 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ImageNet Pre-training (2012)] -> [ULMFiT (NLP 전이, 2018)]
    -> [BERT/GPT Fine-tuning (2018~)]
    -> [LoRA (2021) — 효율적 미세 조정]
    -> [현재: QLoRA + Prompt Tuning — 초효율 전이]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Transfer Learning은 **대학 교양(사전 학습)** 후 <strong>전공(Fine-tuning)</strong>을 고르는 거예요.
2. 교양을 열심히 하면 **어떤 전공이든 빨리** 배울 수 있어요.
3. LoRA는 **전공 한두 과목만** 추가로 듣는 효율적인 방법이에요!
