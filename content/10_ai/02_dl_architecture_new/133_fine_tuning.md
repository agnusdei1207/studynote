---
title: "Fine Tuning"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 133
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Fine-tuning은 <strong>사전 학습된 Foundation Model의 가중치를 도메인 특화 데이터로 추가 학습하여 특정 작업 성능을 최적화</strong>하는 기법이며, Full Fine-tuning·LoRA·Prompt Tuning으로 구분된다.
> 2. **가치**: 사전 학습 모델은 범용이라 특정 도메인(의료·법률)에서 정확도가 부족하지만, Fine-tuning으로 <strong>소량 도메인 데이터만으로도 전문 모델 수준</strong>을 달성한다.
> 3. **판단 포인트**: Full FT(전체 가중치)는 비용^, LoRA(저랭크 어댑터)는 <strong>파라미터의 1% 미만만 학습</strong>하여 효율적이며, QLoRA(양자화+LoRA)로 소비자 GPU에서도 LLM Fine-tuning이 가능하다.

---

## Ⅰ. 개요 및 필요성

```text
Full FT:     전체 가중치 재학습 (GPU 많이 필요)
LoRA:        저랭크 행렬만 추가 학습 (효율적)
QLoRA:       4bit 양자화 + LoRA (소비자 GPU 가능)
Prompt Tuning: 프롬프트 벡터만 학습 (가장 경량)
```

- **📢 섹션 요약 비유**: Full FT는 집 전체 리모델링, LoRA는 벽지·가구만 교체, Prompt Tuning은 인테리어 소품만 바꾸기이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 방식 | 학습 파라미터 | GPU | 성능 |
|:---|:---|:---|:---|
| **Full FT** | 100% | 많이 | 최고 |
| <strong>LoRA</strong> | ~1% | **적음** | 우수 |
| <strong>QLoRA</strong> | ~1% | **최소** | 우수 |
| **Prompt** | <0.1% | 극소 | 보통 |

---

## Ⅲ~Ⅴ. 결론

LoRA/QLoRA는 <strong>LLM Fine-tuning의 사실상 표준</strong>이며, 소규모 팀도 도메인 특화 AI를 구축할 수 있게 했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Fine-tuning</strong> | 사전 학습 후 도메인 적응 |
| <strong>LoRA</strong> | 저랭크 어댑터 (효율적) |
| <strong>QLoRA</strong> | 양자화+LoRA (소비자 GPU) |
| **SFT** | Supervised Fine-tuning |
| <strong>RLHF</strong> | 인간 피드백 강화학습 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ImageNet Fine-tuning (2012)] -> [BERT Fine-tuning (2018)]
    -> [GPT-3 Few-shot (2020)] -> [LoRA (2021)]
    -> [QLoRA (2023)] -> [현재: DoRA·LoRA+ — 차세대 효율 FT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Fine-tuning은 **대학 졸업생이 회사에서 실무를 배우는** 거예요.
2. LoRA는 <strong>핵심 과목만 추가 수강</strong>하는 효율적인 방법이에요.
3. QLoRA 덕분에 <strong>작은 컴퓨터</strong>로도 AI를 맞춤 교육할 수 있답니다!
