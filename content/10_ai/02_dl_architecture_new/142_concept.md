---
title: "Concept"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 142
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스케일링 법칙(Scaling Laws)은 <strong>모델 크기(N)·데이터양(D)·컴퓨팅(C)이 멱법칙(Power Law)에 따라 Loss를 예측 가능하게 감소</strong>시킨다는 OpenAI/DeepMind의 실증적 발견이며, Emergence는 <strong>일정 규모 이상에서 예측 불가능한 새 능력</strong>이 갑자기 나타나는 현상이다.
> 2. **가치**: 스케일링 법칙 덕분에 <strong>학습 전에 최적 모델 크기·데이터량을 계획</strong>할 수 있으며(Chinchilla Optimal), Emergence(CoT·번역·코딩)는 대규모 투자의 정당성을 제공한다.
> 3. **판단 포인트**: Chinchilla(2022)는 "모델 크기와 데이터를 균형있게"가 최적이라 입증, LLaMA(2023)는 "더 많은 데이터로 작은 모델도 강하다"를 보여줬다.

---

## Ⅰ. 개요 및 필요성

```text
스케일링 법칙: L(N,D) ∝ N^(-α) + D^(-β)
  N: 파라미터 수, D: 데이터 토큰 수
  α, β ≈ 0.07 (멱법칙)
Emergence: 10B+ 모델에서 CoT·ICL 능력 갑자기 등장
Chinchilla: N과 D를 1:20 비율로 균형
```

- **📢 섹션 요약 비유**: 스케일링은 <strong>연습량과 실력의 관계</strong>이다. 연습할수록 실력이 올라가고, 어느 순간 <strong>갑자기 새 기술(Emergence)</strong>이 터진다.

---

## Ⅱ~Ⅴ. 결론

스케일링 법칙은 <strong>LLM 투자 계획의 근거</strong>이며, Emergence는 대규모 모델의 핵심 가치이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Scaling Laws** | 멱법칙 Loss 감소 |
| **Emergence** | 창발적 능력 |
| **Chinchilla** | 최적 N:D 비율 |
| <strong>CoT</strong> | Emergence 사례 |
| **LLaMA** | 데이터 중심 스케일링 |

### 📈 관련 키워드 및 발전 흐름도

```text
[GPT-3 스케일링 (2020)] -> [Scaling Laws (Kaplan, 2020)]
    -> [Chinchilla (DeepMind, 2022)]
    -> [LLaMA (Meta, 2023, 데이터 중심)]
    -> [현재: 추론 시간 스케일링 (Test-time Compute)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 스케일링은 **연습할수록 실력이 올라가는** 법칙이에요.
2. 어느 순간 <strong>갑자기 새 기술(Emergence)</strong>이 터져요! 자전거 갑자기 타는 것처럼.
3. AI도 **충분히 크고 많이 배우면** 예상 못 한 능력이 나타나요!
