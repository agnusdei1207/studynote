---
title: "Lora Low Rank Adaptation"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 135
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LoRA는 <strong>사전 학습된 가중치 행렬 W를 동결하고, 저랭크 행렬 A·B(rank r ≪ d)만 추가 학습</strong>하여 W' = W + BA로 적응하는 PEFT 기법이다. 학습 파라미터가 <strong>전체의 0.1~1%</strong>로 극적으로 줄어든다.
> 2. **가치**: 70B LLM의 Full FT는 A100 8장+ 필요하지만, QLoRA(4bit+LoRA)는 <strong>24GB GPU 1장</strong>으로 가능하여 개인/소규모 팀의 LLM 커스텀을 실현했다.
> 3. **판단 포인트**: rank r=8~64, target modules=q_proj/v_proj가 표준이며, 여러 LoRA 어댑터를 <strong>동적으로 교체(LoRA Swap)</strong>하여 하나의 베이스 모델로 다양한 도메인에 대응한다.

---

## Ⅰ. 개요 및 필요성

```text
LoRA: W' = W + BA  (W: 동결, B·A: 학습)
  W: d×d (수십억 파라미터)
  B: d×r, A: r×d (r=8~64, 극소수)
  -> 학습 파라미터: 2dr (전체의 ~0.5%)
```

- **📢 섹션 요약 비유**: LoRA는 <strong>건물(W)을 그대로 두고 간판(BA)만 바꾸는</strong> 것이다. 건물 전체를 리모델링하는 것보다 100배 빠르고 저렴하다.

---

## Ⅱ~Ⅴ. 결론

LoRA는 <strong>LLM Fine-tuning의 사실상 표준</strong>이며, QLoRA·DoRA·LoRA+로 계속 발전하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>LoRA</strong> | 저랭크 어댑터 |
| <strong>QLoRA</strong> | 4bit 양자화 + LoRA |
| <strong>DoRA</strong> | 방향/크기 분리 LoRA |
| <strong>LoRA Swap</strong> | 어댑터 동적 교체 |
| <strong>Hugging Face PEFT</strong> | LoRA 구현 라이브러리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Full Fine-tuning (2018)] -> [Adapter (2019)]
    -> [LoRA (2021, Microsoft)] -> [QLoRA (2023)]
    -> [DoRA (2024)] -> [현재: LoRA+ · GaLore — 차세대]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LoRA는 건물(AI)을 **그대로 두고 간판만 바꾸는** 거예요.
2. 건물 전체를 공사하는 것보다 <strong>100배 빠르고 저렴</strong>해요.
3. 간판만 바꿔도 <strong>완전히 다른 가게(도메인)</strong>처럼 보인답니다!
