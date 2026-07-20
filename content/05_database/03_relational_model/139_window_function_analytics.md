---
title: "Window Function Analytics"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 139
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Window Function은 <strong>GROUP BY 없이 행 단위로 집계·순위·이전/다음 행 참조</strong>를 수행하는 SQL:2003 표준 함수이며, OVER(PARTITION BY ... ORDER BY ...)로 윈도우를 정의한다.
> 2. **가치**: GROUP BY는 결과를 그룹별 1행으로 축소하지만, Window Function은 <strong>원본 행을 유지하면서 집계 결과를 함께 표시</strong>하여 상관 서브쿼리를 대체하고 성능을 크게 향상시킨다.
> 3. **판단 포인트**: ROW_NUMBER(순번)·RANK(순위)·SUM OVER(누적합)·LAG/LEAD(이전/다음 행)가 핵심이며, 페이지네이션·순위·이동 평균에 필수이다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT name, dept, sal,
  ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC) AS rn,
  RANK() OVER (ORDER BY sal DESC) AS rank,
  LAG(sal) OVER (ORDER BY sal) AS prev_sal
FROM emp;
```

- **📢 섹션 요약 비유**: Window Function은 <strong>반 전체 석차표</strong>이다. 각 학생(행)의 성적은 유지하면서 석차(순위)를 옆에 붙인다.

---

## Ⅱ~Ⅴ. 결론

Window Function은 <strong>현대 SQL 분석의 핵심</strong>이며, 상관 서브쿼리·자체 조인을 대체하여 성능과 가독성을 동시에 향상시킨다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ROW_NUMBER** | 순번 |
| **RANK** | 순위 (동점 건너뜀) |
| **DENSE_RANK** | 순위 (동점 안 건너뜀) |
| **LAG/LEAD** | 이전/다음 행 |
| **SUM OVER** | 누적합·이동 평균 |

### 📈 관련 키워드 및 발전 흐름도

```text
[GROUP BY (집계)] -> [상관 서브쿼리 (비효율)]
    -> [Window Function (SQL:2003)]
    -> [ROWS/RANGE Frame (세밀한 윈도우)]
    -> [현재: 대부분 DB 완전 지원 — 분석 쿼리 필수]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Window Function은 <strong>석차표</strong>예요. 각 학생 점수는 **그대로 두고 순위만 붙여요**.
2. GROUP BY는 "반 평균만" 보여주지만, Window는 **각 학생 + 반 평균** 모두 보여줘요.
3. "이전 시험보다 올랐나?"도 <strong>LAG</strong>로 쉽게 알 수 있어요!
