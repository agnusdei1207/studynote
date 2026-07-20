---
title: "Zachman Framework"
date: "2026-05-01"
tags:
  - "studynote-software-engineering"
weight: 55
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Zachman Framework는 기업 아키텍처를 질문 축과 관점 축으로 정리하는 분류 체계다.
> 2. **가치**: What/How/Where/Who/When/Why와 Planner/Owner/Designer/Builder/Subcontractor/Functioning Enterprise를 교차시켜 누락을 줄인다.
> 3. **판단 포인트**: 절차 모델이 아니라 아키텍처 산출물의 분류표로 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

기업 아키텍처는 범위가 넓고 이해관계자가 많다. Zachman Framework는 서로 다른 시각의 산출물을 체계적으로 정리하기 위해 쓰인다.

이 프레임워크는 "무엇을 알아야 하는가"를 구조화하는 데 강하다.

- **📢 섹션 요약 비유**: Zachman Framework는 도서관 책을 주제와 읽는 사람 기준으로 동시에 정리하는 표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Zachman은 질문 축(What, How, Where, Who, When, Why)과 관점 축(Planner, Owner, Designer, Builder, Subcontractor, Functioning Enterprise)을 교차시킨다.

```text
                Planner  Owner  Designer  Builder  Subcontractor  Enterprise
What               ○       ○       ○         ○          ○            ○
How                ○       ○       ○         ○          ○            ○
...
```

| 축 | 의미 | 예 |
| :--- | :--- | :--- |
| What | 데이터 | 엔터티 |
| How | 기능 | 프로세스 |
| Where | 위치 | 네트워크 |
| Who | 사람 | 역할 |
| When | 시점 | 일정 |
| Why | 이유 | 목표/규칙 |

핵심은 하나의 관점만 보면 빠지는 것이 생기므로, 질문과 관점을 교차해 전체를 보는 것이다.

- **📢 섹션 요약 비유**: Zachman Framework는 같은 집을 주소, 구조, 주민, 일정, 이유별로 다시 적어 보는 일이다.

---

## Ⅲ. 비교 및 연결

Zachman은 방법론이라기보다 분류 체계다. TOGAF 같은 프레임워크와 함께 쓰이기도 하지만 역할이 다르다.

| 항목 | Zachman | TOGAF |
| :--- | :--- | :--- |
| 성격 | 분류 체계 | 방법론 |
| 목적 | 누락 방지 | 설계/실행 가이드 |
| 강점 | 전방위 관점 | 절차화 |

Zachman은 산출물의 위치를 정리하는 데 강하고, 변환 절차는 상대적으로 약하다.

- **📢 섹션 요약 비유**: Zachman은 서랍장 라벨, TOGAF는 서랍을 정리하는 청소 순서다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 모든 산출물을 Zachman 행/열에 매핑해 누락을 찾는다. 특히 대규모 전환 프로젝트에서 유용하다.

### 체크리스트

1. 질문 축과 관점 축이 모두 채워지는가?
2. 특정 관점에만 치우치지 않는가?
3. 산출물 누락을 찾는 데 쓰이는가?
4. 방법론과 혼동하지 않는가?

### 안티패턴

- 프레임워크를 절차서처럼 오해하는 경우
- 표만 만들고 실제 산출물과 연결하지 않는 경우
- 모든 프로젝트에 무조건 적용하려는 경우

실무 관점에서는 Zachman Framework가 기업 아키텍처를 전체적으로 보는 분류 도구라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: Zachman은 방마다 붙이는 이름표와 같다.

---

## Ⅴ. 기대효과 및 결론

Zachman Framework는 기업 아키텍처의 누락을 줄이고, 다양한 이해관계자 관점을 연결한다. 큰 조직일수록 유용하다.

정리하면, 이 프레임워크는 무엇을, 왜, 어떻게, 누가, 어디서, 언제 설명할지 정리하는 지도다.

- **📢 섹션 요약 비유**: Zachman Framework는 큰 창고의 재고표다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| What/How | 기능/데이터 |
| Where/Who | 위치/역할 |
| When/Why | 시점/목표 |
| Planner~Enterprise | 관점 축 |
| TOGAF | 방법론 비교 |

### 📈 관련 키워드 및 발전 흐름도

```text
산출물 혼재
    |
    v
질문 축/관점 축 분류
    |
    v
Zachman Matrix
    |
    v
누락 확인 / 아키텍처 정렬
```

이 흐름은 복잡한 기업 아키텍처 산출물을 체계적으로 정리하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Zachman Framework는 장난감을 종류별로 정리하는 큰 표예요.
2. 누가 보느냐에 따라 같은 장난감도 다르게 분류해요.
3. 그래서 빠진 걸 찾기 쉬워요.
