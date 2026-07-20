---
title: "Chain Of Thought Cot"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 146
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CoT는 <strong>"단계별로 생각해 봐(Let's think step by step)"를 프롬프트에 추가</strong>하여 LLM이 중간 추론 과정을 명시적으로 생성하게 하는 기법이며, 산술·논리·상식 추론 정확도를 크게 향상시킨다.
> 2. **가치**: LLM이 직접 답을 출력하면 <strong>추론 없이 패턴 매칭</strong>하여 오류가 많지만, CoT로 <strong>중간 단계를 생성</strong>하면 "왜 이 답인지"의 논리적 경로가 만들어져 정확도가 2~3배 향상된다.
> 3. **판단 포인트**: Zero-shot CoT("Let's think step by step")·Few-shot CoT(추론 과정 예시 포함)·Self-Consistency(다수 CoT 경로 중 다수결)·Tree-of-Thought(분기 탐색)로 진화했다.

---

## Ⅰ. 개요 및 필요성

```text
일반: "15+27×3=?" -> "96" (오답)
CoT: "15+27×3=? 단계별로:"
  -> "27×3=81, 15+81=96" (정답, 과정 명시)
Self-Consistency: 5번 CoT -> 다수결 -> 정답률^
Tree-of-Thought: 여러 분기 탐색 -> 최적 경로
```

- **📢 섹션 요약 비유**: CoT는 <strong>시험에서 풀이 과정 쓰기</strong>이다. 답만 쓰면 실수하지만, 풀이를 쓰면 정확해진다.

---

## Ⅱ~Ⅴ. 결론

CoT는 <strong>LLM 추론 능력 향상의 핵심 기법</strong>이며, Self-Consistency와 ToT로 고도화되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **CoT** | 단계별 추론 |
| <strong>Zero-shot CoT</strong> | 지시만으로 |
| **Few-shot CoT** | 예시 포함 |
| <strong>Self-Consistency</strong> | 다수결 |
| <strong>ToT</strong> | 분기 탐색 |

### 📈 관련 키워드 및 발전 흐름도

```text
[직접 답변 (2020)] -> [CoT (Wei et al., 2022)]
    -> [Zero-shot CoT (Kojima, 2022)]
    -> [Self-Consistency (Wang, 2023)]
    -> [현재: o1/o3 — 내부 CoT 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CoT는 <strong>시험에서 풀이 과정 쓰기</strong>예요. 답만 쓰면 실수해요.
2. "단계별로 생각해 봐" 하면 AI가 **풀이를 써서** 정확해져요.
3. 여러 번 풀어서(Self-Consistency) <strong>다수결</strong>로 정하면 더 정확해요!
