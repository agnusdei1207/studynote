---
title: "1 Mini Spec"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 145
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Mini-Spec은 <strong>DFD의 최하위 프로세스(기본 프로세스)의 로직을 구조적 영어(Structured English)·의사결정표·의사결정트리</strong>로 상세 기술하는 프로세스 명세서이다.
> 2. **가치**: DFD는 "무엇을" 보여주지만 <strong>"어떻게 변환하는지"</strong>는 보여주지 않으며, Mini-Spec이 각 프로세스의 **입력->변환 규칙->출력을 명확히** 정의한다.
> 3. **판단 포인트**: 구조적 영어(IF-THEN-ELSE, DO-WHILE), 의사결정표(Decision Table, 복합 조건), 의사결정트리(Decision Tree, 시각적) 중 상황에 맞는 표현을 선택한다.

---

## Ⅰ. 개요 및 필요성

```text
구조적 영어:
  IF 고객.등급 = 'VIP' THEN
    할인율 = 20%
  ELSE IF 고객.등급 = '일반' THEN
    할인율 = 5%
  ENDIF

의사결정표: 조건 조합 -> 행동 매핑 (복합 조건에 적합)
```

- **📢 섹션 요약 비유**: Mini-Spec은 <strong>요리 레시피</strong>이다. DFD가 "볶음밥 만들기"라면, Mini-Spec은 <strong>재료·순서·불세기</strong>를 상세히 적는다.

---

## Ⅱ~Ⅴ. 결론

Mini-Spec은 <strong>DFD 프로세스의 로직 명세 도구</strong>이며, 구조적 영어·의사결정표·의사결정트리가 3대 표현 방법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Mini-Spec** | 프로세스 명세서 |
| **구조적 영어** | IF-THEN-ELSE |
| **의사결정표** | 복합 조건 매핑 |
| **의사결정트리** | 시각적 조건 분기 |
| <strong>DFD</strong> | Mini-Spec의 상위 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DFD (1978)] -> [Mini-Spec (구조적 분석)]
    -> [의사결정표 (복합 조건)]
    -> [UML 활동 다이어그램 (대안)]
    -> [현재: BDD/Gherkin — Given-When-Then 형식]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Mini-Spec은 <strong>요리 레시피</strong>예요. "볶음밥" 만드는 <strong>순서와 방법</strong>을 적어요.
2. "VIP면 20% 할인, 일반이면 5% 할인"처럼 **규칙을 정확히** 써요.
3. DFD가 <strong>큰 그림</strong>이면, Mini-Spec은 <strong>세부 설명</strong>이에요!
