---
title: "Prompt Engineering"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프롬프트 엔지니어링은 <strong>LLM에 입력하는 지시문(Prompt)을 체계적으로 설계</strong>하여 원하는 출력을 얻는 기법이며, Zero-shot·Few-shot·CoT(Chain-of-Thought)가 핵심 전략이다.
> 2. **가치**: 같은 모델이라도 프롬프트에 따라 <strong>출력 품질이 10배+ 차이</strong>가 나며, 모델 재학습 없이 <strong>프롬프트만으로 새 작업에 적응</strong>할 수 있어 비용 효율적이다.
> 3. **판단 포인트**: CoT("단계별로 생각해봐")가 추론 성능을 크게 향상시키며, 역할 부여("너는 전문 편집자야")·출력 형식 지정(JSON)·Few-shot 예시가 실무 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
Zero-shot: 예시 없이 지시만 제공
Few-shot: 2~5개 입출력 예시 제공
CoT: "단계별로 생각해 봐" -> 추론 과정 명시
역할 부여: "너는 시니어 백엔드 개발자야"
출력 형식: "JSON으로 응답해 줘"
```

- **📢 섹션 요약 비유**: 프롬프트 엔지니어링은 <strong>AI에게 잘 질문하는 기술</strong>이다. 질문이 좋아야 답이 좋다.

---

## Ⅱ~Ⅴ. 결론

프롬프트 엔지니어링은 <strong>LLM 활용의 가장 비용 효율적 방법</strong>이며, CoT·Few-shot·역할 부여가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Zero-shot</strong> | 예시 없이 |
| **Few-shot** | 예시 제공 |
| <strong>CoT</strong> | 추론 과정 명시 |
| **역할 부여** | 페르소나 설정 |
| **구조화 출력** | JSON 지정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Zero/Few-shot (GPT-3, 2020)] -> [CoT (2022)]
    -> [Self-Consistency (2023)] -> [Tree-of-Thought (2023)]
    -> [현재: Agent Prompt — 도구 호출·반복 추론]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 프롬프트 엔지니어링은 <strong>AI에게 잘 질문</strong>하는 거예요.
2. "단계별로 생각해 봐(CoT)"라고 하면 <strong>더 정확한 답</strong>을 줘요.
3. **좋은 질문 = 좋은 답** — 질문하는 기술이 중요해요!
