---
title: "Foundation Model"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 130
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Foundation Model은 <strong>대규모 데이터로 사전 학습(Pre-training)된 범용 AI 모델</strong>로, 다양한 하위 작업(NLP·Vision·코드)에 Fine-tuning 또는 Prompting으로 적응 가능하며, GPT·BERT·Stable Diffusion이 대표이다.
> 2. **가치**: 개별 작업마다 처음부터 모델을 학습하면 비용이 막대하지만, Foundation Model을 <strong>기반으로 미세 조정</strong>하면 소량 데이터로도 높은 성능을 달성할 수 있다(Transfer Learning).
> 3. **판단 포인트**: 스탠포드 HAI(2021)가 명명했으며, <strong>Emergent Abilities(창발 능력)</strong>—규모가 커지면 사전에 학습하지 않은 능력이 나타나는 현상—이 핵심 특성이다.

---

## Ⅰ. 개요 및 필요성

```text
Foundation Model = 대규모 데이터 + 대규모 파라미터 + 자기지도 학습
  -> 범용 표현 학습 -> 다양한 하위 작업에 적응
  예: GPT-4(텍스트), CLIP(이미지+텍스트), Codex(코드)
```

- **📢 섹션 요약 비유**: Foundation Model은 <strong>대학 교양 교육</strong>이다. 교양(사전 학습)을 받은 후 전공(Fine-tuning)을 선택하면 빠르게 전문가가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 특성 | 설명 |
|:---|:---|
| **사전 학습** | 대규모 비라벨 데이터 |
| **Transfer** | 하위 작업에 적응 |
| **Emergent** | 규모^ -> 새 능력 출현 |
| <strong>멀티모달</strong> | 텍스트+이미지+오디오 |

---

## Ⅲ~Ⅴ. 결론

Foundation Model은 <strong>현대 AI의 패러다임</strong>이며, 규모의 법칙(Scaling Law)에 의해 계속 발전하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Foundation Model</strong> | 범용 사전 학습 모델 |
| <strong>Emergent Abilities</strong> | 규모 확대 시 창발 |
| <strong>Fine-tuning</strong> | 하위 작업 적응 |
| **Scaling Law** | 규모와 성능의 관계 |
| <strong>Transfer Learning</strong> | 사전 학습 -> 전이 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Word2Vec (2013)] -> [BERT (2018)] -> [GPT-3 (2020)]
    -> [Foundation Model 명명 (Stanford HAI, 2021)]
    -> [GPT-4 / Gemini (2023~2024)]
    -> [현재: 오픈소스 FM — Llama·Mistral·Qwen]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Foundation Model은 <strong>대학 교양 교육</strong>이에요. 많이 배우면 <strong>뭐든 할 수 있는 기초</strong>가 돼요.
2. 교양(사전 학습) 후 <strong>전공(Fine-tuning)</strong>을 선택하면 빠르게 전문가가 돼요.
3. 정말 많이 배우면 **가르치지 않은 것도 알게 되는(창발)** 신기한 현상이 일어나요!
