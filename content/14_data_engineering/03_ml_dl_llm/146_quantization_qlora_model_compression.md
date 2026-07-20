---
title: "Quantization Qlora Model Compression"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 146
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 양자화(Quantization)는 <strong>FP32/FP16 가중치를 INT8/INT4로 축소</strong>하여 메모리·연산을 줄이는 모델 압축 기법이며, QLoRA는 <strong>4비트 양자화된 모델에 LoRA를 적용</strong>하여 단일 소비자 GPU(24GB)에서 LLM Fine-tuning을 가능하게 했다.
> 2. **가치**: 7B 모델 FP16은 <strong>14GB 메모리</strong>이지만, 4비트 양자화 시 <strong>3.5GB</strong>로 축소되어 소비자 GPU에서 추론·학습이 가능하다.
> 3. **판단 포인트**: PTQ(Post-Training Quantization, 학습 후)·QAT(Quantization-Aware Training, 학습 중)로 구분하며, GPTQ·AWQ·bitsandbytes가 LLM 양자화의 핵심 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
FP16: 7B × 2B = 14GB
INT4: 7B × 0.5B = 3.5GB (4배 축소)
QLoRA = NF4 양자화 + LoRA + Double Quantization
  -> 단일 24GB GPU에서 65B 모델 Fine-tuning
```

- **📢 섹션 요약 비유**: 양자화는 <strong>고해상도 사진을 압축</strong>하는 것이다. 파일(메모리)은 작아지지만 품질(성능)은 거의 유지된다.

---

## Ⅱ~Ⅴ. 결론

양자화+QLoRA는 <strong>LLM 민주화의 핵심 기술</strong>이며, 소비자 GPU에서 대규모 모델 활용을 가능하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>양자화</strong> | FP->INT 축소 |
| <strong>QLoRA</strong> | 4비트+LoRA |
| **GPTQ** | PTQ 도구 |
| **AWQ** | 활성화 기반 양자화 |
| **NF4** | 정규 분포 4비트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[FP32 학습 (전통)] -> [FP16/BF16 Mixed Precision (2018)]
    -> [INT8 양자화 (2020)] -> [GPTQ (2022)]
    -> [QLoRA (2023)] -> [현재: AWQ·GGUF — 추론 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 양자화는 <strong>사진 압축</strong>이에요. 파일은 작아지지만 **사진은 거의 같아요**.
2. QLoRA는 <strong>압축 사진에 포스트잇(LoRA)</strong>을 붙이는 거예요. 빠르고 저렴해요.
3. 보통 컴퓨터에서도 **큰 AI를 돌릴 수** 있게 해줘요!
