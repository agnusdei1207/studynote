---
title: "Sql Outer Join Left Right Full"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 134
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OUTER JOIN은 <strong>매칭되지 않는 행도 NULL로 채워서 포함</strong>하는 JOIN이며, LEFT(왼쪽 전체)·RIGHT(오른쪽 전체)·FULL(양쪽 전체)로 구분된다.
> 2. **가치**: "주문이 없는 고객 목록"·"담당자가 없는 프로젝트 목록" 등 <strong>비매칭 데이터를 찾는 데 필수</strong>이며, LEFT JOIN이 가장 빈번하게 사용된다.
> 3. **판단 포인트**: LEFT JOIN + WHERE right.id IS NULL -> <strong>비매칭만 추출</strong>하는 Anti-Join 패턴이 실무에서 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
LEFT JOIN:  왼쪽 전체 + 오른쪽 매칭 (없으면 NULL)
RIGHT JOIN: 오른쪽 전체 + 왼쪽 매칭 (없으면 NULL)
FULL JOIN:  양쪽 전체 (없으면 NULL)
Anti-Join:  LEFT JOIN WHERE right.id IS NULL -> 비매칭만
```

- **📢 섹션 요약 비유**: LEFT JOIN은 "A반 전체 명단 + B반 겹치는 사람 표시, 안 겹치면 빈칸"이다.

---

## Ⅱ~Ⅴ. 결론

OUTER JOIN은 <strong>비매칭 데이터 분석의 핵심 연산</strong>이며, Anti-Join 패턴이 실무에서 가장 자주 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>LEFT JOIN</strong> | 왼쪽 전체 보존 |
| <strong>RIGHT JOIN</strong> | 오른쪽 전체 보존 |
| **FULL OUTER** | 양쪽 전체 |
| <strong>Anti-Join</strong> | 비매칭만 추출 |
| **NULL** | 매칭 없을 때 채움 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cartesian Product] -> [INNER JOIN (교집합)]
    -> [OUTER JOIN (SQL-92)] -> [Anti-Join 패턴]
    -> [LATERAL JOIN (SQL:2003)] -> [현재: Semi-Join 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LEFT JOIN은 <strong>A반 전체 명단</strong>이에요. B반에서 겹치는 사람은 표시하고 <strong>안 겹치면 빈칸</strong>이에요.
2. "주문 안 한 고객"을 찾으려면 **빈칸(NULL)인 사람만** 뽑으면 돼요.
3. 이 방법(Anti-Join)은 **실무에서 정말 많이** 사용한답니다!
