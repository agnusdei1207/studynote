---
title: "Peft"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 134
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PEFT는 <strong>Foundation Model의 전체 파라미터 중 극소수(0.1~1%)만 추가·학습</strong>하여 도메인 적응하는 기법의 총칭이며, LoRA·Adapter·Prefix Tuning·Prompt Tuning이 대표이다.
> 2. **가치**: 70B LLM을 Full FT하려면 A100 8장+가 필요하지만, PEFT(QLoRA)로는 <strong>소비자 GPU 1장(24GB)</strong>으로도 Fine-tuning이 가능하여 민주화를 실현한다.
> 3. **판단 포인트**: LoRA(저랭크 행렬)가 성능 대비 효율 최고이며, 여러 LoRA 어댑터를 교체하여 <strong>하나의 베이스 모델로 다양한 도메인에 대응</strong>할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
Full FT:       100% 파라미터 학습 (비용^^)
LoRA:          저랭크 행렬만 학습 (~1%)
Adapter:       작은 모듈 삽입 (~3%)
Prefix Tuning: 프리픽스 벡터 학습 (<0.1%)
Prompt Tuning: 소프트 프롬프트 학습 (<0.01%)
```

- **📢 섹션 요약 비유**: Full FT는 집 전체 리모델링, LoRA는 벽지만 교체, Prompt Tuning은 액자만 바꾸기이다.

---

## Ⅱ~Ⅴ. 결론

PEFT는 <strong>LLM 시대의 필수 기술</strong>이며, LoRA/QLoRA가 사실상 표준으로 소규모 팀의 AI 커스텀을 가능하게 했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>PEFT</strong> | 효율적 미세 조정 총칭 |
| <strong>LoRA</strong> | 저랭크 어댑터 (표준) |
| <strong>QLoRA</strong> | 양자화+LoRA |
| <strong>Adapter</strong> | 모듈 삽입형 |
| <strong>Prompt Tuning</strong> | 소프트 프롬프트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Full Fine-tuning (2018)] -> [Adapter (2019)]
    -> [Prefix Tuning (2021)] -> [LoRA (2021)]
    -> [QLoRA (2023)] -> [현재: DoRA·LoRA+ — 차세대 PEFT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. PEFT는 **집 전체를 리모델링하지 않고 벽지만 바꾸는** 거예요.
2. 벽지(LoRA)만 바꿔도 <strong>분위기(성능)가 완전히</strong> 달라져요.
3. 비용이 <strong>100분의 1</strong>로 줄어서 누구나 AI를 맞춤 제작할 수 있답니다!
