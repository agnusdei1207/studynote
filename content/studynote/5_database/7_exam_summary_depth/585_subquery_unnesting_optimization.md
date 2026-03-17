+++
title = "585. 서브쿼리 언네스팅(Unnesting) - 중첩의 벽을 허무는 최적화"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 585
+++

# 585. 서브쿼리 언네스팅(Unnesting) - 중첩의 벽을 허무는 최적화

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서브쿼리 언네스팅(Unnesting)은 옵티마이저가 중첩된 서브쿼리를 **동등한 결과가 보장되는 일반 조인(Join) 문장으로 변환하여 메인 쿼리와 동일한 계층으로 펼치는 최적화 기법**이다.
> 2. **가치**: 서브쿼리가 메인 쿼리의 행마다 반복 실행되는 비효율(Filter 방식)을 제거하고, 해시 조인이나 소트 머지 조인 등 **다양한 실행 경로를 선택할 수 있게 하여 쿼리 성능을 비약적으로 향상**시킨다.
> 3. **융합**: '쿼리 변환(Query Transformation)' 기술의 핵심이며, 세미 조인(Semi-join) 및 안티 조인(Anti-join) 알고리즘과 융합되어 복잡한 SQL의 물리적 실행 효율을 완성한다.

+++

### Ⅰ. 언네스팅의 작동 원리 (Transformation)

- **전통적 방식 (Filter)**: 서브쿼리가 메인 쿼리의 '필터'로 작동. 메인 쿼리 한 줄 읽을 때마다 서브쿼리 실행 (Nested Loop와 유사). 💥
- **언네스팅 방식 (Join)**: 서브쿼리를 하나의 가상 테이블(Inline View)로 만들고 메인 테이블과 조인함. ✅
- **장점**: 조인 순서를 바꿀 수 있고(Leading), 대량 데이터 처리에 유리한 해시 조인 등을 활용할 수 있습니다.

+++

### Ⅱ. 언네스팅 변환 시각화 (ASCII Model)

```text
[ Subquery Unnesting Process ]

  (Before: Nested)
  SELECT * FROM Emp 
  WHERE DeptID IN (SELECT ID FROM Dept WHERE Loc='Seoul');
  ──▶ [ Logical Filter ] : For each Emp, scan Dept. 💥

  (After: Unnested & Joined) ✅
  SELECT Emp.* FROM Emp, Dept 
  WHERE Emp.DeptID = Dept.ID AND Dept.Loc='Seoul';
  ──▶ [ Hash Join ] : Build Hash(Dept) and Probe(Emp). ✅
```

+++

### Ⅲ. 언네스팅이 불가능하거나 제한되는 경우

1. **중복 발생 위험**: 서브쿼리 결과에 중복이 있을 때 이를 일반 조인으로 바꾸면 메인 쿼리 결과까지 중복될 수 있습니다 (이 경우 `DISTINCT`나 세미 조인을 사용).
2. **상관 서브쿼리의 복잡성**: 메인 쿼리의 여러 컬럼이 복잡하게 얽혀 있는 경우 언네스팅 효율이 떨어질 수 있습니다.
3. **힌트 강제**: `/*+ UNNEST */` 힌트를 통해 수동으로 유도하거나, `/*+ NO_UNNEST */`를 통해 서브쿼리 형태를 유지하게 할 수 있습니다.

- **📢 섹션 요약 비유**: 서브쿼리 언네스팅은 **'번거로운 확인 절차를 명단 대조로 바꾸는 것'**과 같습니다. 예전 방식(Filter)이 손님(메인 쿼리)이 올 때마다 일일이 장부를 뒤져서 "이 손님 블랙리스트인가요?(서브쿼리)"라고 묻는 것이라면, 언네스팅은 아예 블랙리스트 명단(서브쿼리 결과)을 복사해서 카운터 옆에 붙여두고 손님 명단과 한 번에 대조(Join)하는 효율적인 방식입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Query Transformation]**: 옵티마이저가 쿼리를 더 나은 형태로 다시 쓰는 과정.
- **[Semi-join]**: IN 이나 EXISTS 서브쿼리를 언네스팅할 때 주로 쓰이는 조인 방식.
- **[Anti-join]**: NOT IN 이나 NOT EXISTS 서브쿼리를 언네스팅하는 방식.

📢 **마무리 요약**: **Subquery Unnesting**은 쿼리 최적화의 꽃입니다. '중첩'이라는 논리적 감옥에 갇힌 데이터를 '조인'이라는 넓은 광장으로 끌어내어 시스템의 잠재력을 폭발시킵니다.