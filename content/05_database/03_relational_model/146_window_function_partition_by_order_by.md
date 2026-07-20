---
title: "Window Function Partition By Order By"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 146
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PARTITION BY는 <strong>Window 함수의 그룹화 기준</strong>이고, ORDER BY는 <strong>각 파티션 내 정렬 기준</strong>이며, 이 두 절이 Window 함수의 계산 범위와 순서를 결정한다.
> 2. **가치**: PARTITION BY 없이 ORDER BY만 쓰면 <strong>전체를 하나의 파티션</strong>으로 처리하고, PARTITION BY만 쓰면 <strong>정렬 없이 그룹별 집계</strong>만 수행한다. 조합에 따라 결과가 완전히 달라진다.
> 3. **판단 포인트**: ROW_NUMBER·RANK·DENSE_RANK는 **ORDER BY 필수**, SUM·AVG는 <strong>ORDER BY 유무에 따라 누적합/전체합</strong>이 결정된다.

---

## Ⅰ. 개요 및 필요성

```text
ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC)
  -> 부서별로 급여 높은 순 번호
SUM(sal) OVER (PARTITION BY dept)
  -> 부서별 전체 합계 (정렬 없음)
SUM(sal) OVER (PARTITION BY dept ORDER BY id)
  -> 부서별 누적 합계 (정렬 있음)
```

- **📢 섹션 요약 비유**: PARTITION BY는 **반 나누기**, ORDER BY는 <strong>석차 정하기</strong>이다. 반(부서)별로 석차(순위)를 매긴다.

---

## Ⅱ~Ⅴ. 결론

PARTITION BY+ORDER BY 조합이 <strong>Window 함수 결과를 결정</strong>하며, ORDER BY 유무에 따른 누적/전체 차이를 이해해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>PARTITION BY</strong> | 그룹화 |
| **ORDER BY** | 정렬 |
| **누적합** | ORDER BY 있음 |
| **전체합** | ORDER BY 없음 |
| **ROW_NUMBER** | ORDER BY 필수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[GROUP BY (그룹 축소)] -> [PARTITION BY (행 유지)]
    -> [ORDER BY + Frame (세밀 제어)]
    -> [현재: Named Window (SQL:2019)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. PARTITION BY는 <strong>반 나누기</strong>예요. "1반, 2반, 3반"으로 나눠요.
2. ORDER BY는 <strong>석차 정하기</strong>예요. 각 반에서 <strong>점수 높은 순</strong>으로 번호를 매겨요.
3. 나누기(PARTITION)와 정렬(ORDER)을 **합치면** 반별 석차가 나와요!
