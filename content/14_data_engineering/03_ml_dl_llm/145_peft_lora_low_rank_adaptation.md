---
title: "Peft Lora Low Rank Adaptation"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 145
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LoRA는 <strong>사전 학습된 가중치 행렬 W에 저랭크 분해 행렬(A·B)을 추가</strong>하여, 전체 파라미터의 <strong>0.1~1%만 학습</strong>하면서도 Full Fine-tuning과 유사한 성능을 달성하는 PEFT(Parameter-Efficient Fine-Tuning) 기법이다.
> 2. **가치**: 7B 모델 Full FT는 <strong>GPU 메모리 112GB+(FP16)</strong> 필요하지만, LoRA는 <strong>추가 파라미터만 학습</strong>하여 단일 GPU(24GB)로도 가능하다. QLoRA(4비트 양자화+LoRA)는 더 적은 메모리로 가능하다.
> 3. **판단 포인트**: 랭크 r(4~64)이 핵심 하이퍼파라미터이며, r이 클수록 표현력^ 비용^. 어텐션 레이어(Q·V)에 적용하는 것이 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
LoRA: W' = W + ΔW = W + B·A
  W: 고정 (사전 학습 가중치)
  B: d×r, A: r×d (r << d, 예: r=16, d=4096)
  학습 파라미터: 2×r×d (vs 원래 d×d)
  -> 99%+ 파라미터 절감
```

- **📢 섹션 요약 비유**: LoRA는 **교과서(W)에 포스트잇(ΔW)을 붙이는** 것이다. 교과서는 그대로 두고 포스트잇만 바꾸면 된다.

---

## Ⅱ~Ⅴ. 결론

LoRA는 <strong>LLM Fine-tuning의 사실상 표준</strong>이며, QLoRA로 소비자 GPU에서도 학습이 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>LoRA</strong> | 저랭크 적응 |
| <strong>QLoRA</strong> | 4비트+LoRA |
| <strong>PEFT</strong> | 효율적 미세 조정 |
| **랭크 r** | 핵심 하이퍼파라미터 |
| <strong>Adapter</strong> | LoRA의 전신 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Full Fine-tuning (비용^)] -> [Adapter (2019)]
    -> [LoRA (Microsoft, 2021)] -> [QLoRA (2023)]
    -> [DoRA (2024)] -> [현재: LoRA+ — 학습률 분리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LoRA는 <strong>교과서에 포스트잇</strong>을 붙이는 거예요. 교과서는 안 바꿔요.
2. 포스트잇(저랭크 행렬)만 **새로 쓰면** 되니까 빠르고 저렴해요.
3. 교과서(사전 학습)는 <strong>그대로 보존</strong>하면서 새 내용만 추가해요!
