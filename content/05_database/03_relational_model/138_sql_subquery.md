---
title: "Sql Subquery"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 138
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서브쿼리(Subquery)는 <strong>SQL 문 안에 중첩된 또 다른 SELECT 문</strong>이며, WHERE·FROM·SELECT·HAVING 절에서 사용할 수 있고, 스칼라·인라인 뷰·상관(Correlated) 서브쿼리로 구분된다.
> 2. **가치**: JOIN으로 해결하기 어려운 **"평균보다 높은 급여의 직원"·"각 부서의 최고 급여"** 등의 복합 조건을 <strong>직관적으로 표현</strong>할 수 있다.
> 3. **판단 포인트**: 상관 서브쿼리는 <strong>외부 쿼리 행마다 실행</strong>되어 성능이 나쁘므로, 가능하면 <strong>JOIN이나 Window Function으로 대체</strong>한다.

---

## Ⅰ. 개요 및 필요성

```text
스칼라:  SELECT (SELECT MAX(sal) FROM emp) FROM dual
인라인:  SELECT * FROM (SELECT ... ) AS t
WHERE절: SELECT * FROM emp WHERE sal > (SELECT AVG(sal) FROM emp)
상관:    SELECT * FROM emp e WHERE sal > (SELECT AVG(sal) FROM emp WHERE dept_id = e.dept_id)
```

- **📢 섹션 요약 비유**: 서브쿼리는 <strong>질문 속의 질문</strong>이다. "평균이 얼마야?"를 먼저 답하고, 그 답으로 "평균보다 높은 사람은?"을 묻는다.

---

## Ⅱ~Ⅴ. 결론

서브쿼리는 <strong>복합 조건 표현의 핵심</strong>이지만, 성능을 위해 JOIN·CTE·Window Function 대체를 항상 고려한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **스칼라** | SELECT 절 서브쿼리 |
| <strong>인라인 뷰</strong> | FROM 절 서브쿼리 |
| **상관** | 외부 참조 (성능v) |
| **CTE** | 서브쿼리 대안 |
| <strong>Window Function</strong> | 상관 서브쿼리 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[기본 서브쿼리 (SQL-86)] -> [상관 서브쿼리 (SQL-92)]
    -> [CTE (SQL:1999)] -> [Window Function (SQL:2003)]
    -> [현재: 옵티마이저 자동 서브쿼리->JOIN 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 서브쿼리는 <strong>질문 속의 질문</strong>이에요. "평균이 얼마야?" -> "평균보다 높은 사람은?"
2. 먼저 <strong>안쪽 질문에 답</strong>하고, 그 답으로 <strong>바깥 질문</strong>에 답해요.
3. 하지만 너무 많이 쓰면 **느려지니까** 다른 방법(JOIN)도 알아야 해요!
