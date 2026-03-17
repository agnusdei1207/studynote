+++
title = "513. 트리 구조와 CTE - 재귀 쿼리의 강력함"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 513
+++

# 513. 트리 구조와 CTE - 재귀 쿼리의 강력함

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CTE(Common Table Expression)는 복잡한 쿼리를 논리적인 임시 결과 집합으로 정의하는 기술이며, **재귀적 CTE(Recursive CTE)**는 이를 이용해 트리나 그래프 형태의 계층 데이터를 효율적으로 조회하는 기술이다.
> 2. **가치**: 과거의 복잡한 `CONNECT BY` 전용 문법을 대체하여 표준 SQL로 **조직도, 카테고리 계층, 부품 구조(BOM)** 등을 직관적으로 탐색하게 한다.
> 3. **융합**: '앵커 멤버(Anchor)'와 '재귀 멤버(Recursive)'의 결합 구조를 통해, 데이터의 깊이에 상관없이 전체 트리 구조를 평탄화(Flattening)하여 분석할 수 있게 돕는다.

+++

### Ⅰ. 재귀적 CTE(Recursive CTE)의 작동 원리

1. **앵커 멤버 (Anchor Member)**: 재귀의 시작점이 되는 최상위 노드(Root)를 먼저 선택합니다.
2. **재귀 멤버 (Recursive Member)**: 이전 단계의 결과와 테이블을 조인하여 하위 노드(Child)를 계속 찾아 나갑니다.
3. **종료 조건**: 더 이상 조인할 하위 노드가 없으면 연산을 멈추고 결과를 하나로 합칩니다 (UNION ALL).

+++

### Ⅱ. 트리 데이터 탐색 시각화 (ASCII Model)

```text
[ Hierarchical Structure: Org Chart ]

  (Root) [ CEO ]
           │
    ┌──────┴──────┐
  [ Dev Manager ] [ Sales Manager ] (Level 1)
    │               │
  [ Dev A ]       [ Sales A ]       (Level 2) ✅

[ Recursive CTE Logic ]
  WITH RECURSIVE Org_Tree AS (
    SELECT id, name, manager_id, 1 as level FROM Emp WHERE manager_id IS NULL -- 앵커
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1 FROM Emp e
    JOIN Org_Tree ot ON e.manager_id = ot.id                               -- 재귀 ✅
  ) SELECT * FROM Org_Tree;
```

+++

### Ⅲ. 실무적 의의: 왜 CTE인가?

- **가독성**: 서브쿼리가 중첩된 복잡한 SQL을 상단에 별도로 정의함으로써 코드의 가독성을 획기적으로 높입니다.
- **BOM (Bill of Materials) 분석**: 제품 하나를 만들기 위해 필요한 수만 개의 부품 계층 구조를 한 번의 쿼리로 펼쳐볼 수 있습니다.
- **경로 탐색**: 네트워크 망이나 소셜 인맥의 연결 경로를 추적하는 데 최적화되어 있습니다.

- **📢 섹션 요약 비유**: 재귀적 CTE는 **'족보 찾기'**와 같습니다. 먼저 시조 어르신(앵커)을 모시고, 그 어르신의 자식들(Level 1)을 찾고, 다시 그 자식들의 자식들(Level 2)을 꼬리에 꼬리를 물고 찾아 내려가는 과정입니다. 아무리 가계도가 복잡해도 이 규칙 하나만 있으면 온 집안 식구(전체 트리)를 순서대로 한 장의 종이에 정리할 수 있는 마법의 리스트와 같습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[WITH Clause]**: CTE를 선언하는 표준 SQL 문구.
- **[Anchor vs Recursive]**: 재귀 쿼리를 구성하는 두 가지 필수 파트.
- **[Cycle Prevention]**: 그래프 구조에서 무한 루프에 빠지지 않도록 주의해야 할 제약 사항.

📢 **마무리 요약**: **CTE & Recursive Query**는 계층적 데이터의 해답입니다. 복잡하게 얽힌 관계를 논리적인 선형 구조로 풀어냄으로써, 데이터 속에 숨겨진 질서를 명확히 드러냅니다.