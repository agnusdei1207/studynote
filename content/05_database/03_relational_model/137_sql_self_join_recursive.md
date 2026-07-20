---
title: "Sql Self Join Recursive"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self JOIN은 같은 테이블을 <strong>별칭(Alias)을 달리하여 자기 자신과 조인</strong>하는 것이고, Recursive CTE(Common Table Expression)는 <strong>WITH RECURSIVE로 계층·트리 구조를 재귀 탐색</strong>하는 SQL:1999 표준 문법이다.
> 2. **가치**: 조직도(직원-상사)·부품 BOM(Part-SubPart)·카테고리 계층 등 <strong>트리 구조 데이터를 SQL로 탐색</strong>하는 데 필수이며, Oracle의 CONNECT BY보다 Recursive CTE가 표준이다.
> 3. **판단 포인트**: 무한 루프 방지를 위해 <strong>MAX RECURSION DEPTH</strong> 설정이 필수이며, PostgreSQL·MySQL 8+·SQL Server 모두 지원한다.

---

## Ⅰ. 개요 및 필요성

```text
Recursive CTE:
  WITH RECURSIVE org AS (
    SELECT id, name, mgr_id FROM emp WHERE mgr_id IS NULL  -- Anchor
    UNION ALL
    SELECT e.id, e.name, e.mgr_id FROM emp e JOIN org o ON e.mgr_id = o.id  -- Recursive
  ) SELECT * FROM org;
```

- **📢 섹션 요약 비유**: Recursive CTE는 <strong>가계도 탐색</strong>이다. 시조(Anchor)부터 시작하여 자손을 재귀적으로 찾는다.

---

## Ⅱ~Ⅴ. 결론

Recursive CTE는 <strong>계층·그래프 데이터 탐색의 SQL 표준</strong>이며, CONNECT BY(Oracle 전용)를 대체한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Self JOIN</strong> | 자기 참조 |
| **Recursive CTE** | 재귀 계층 탐색 |
| **Anchor** | 재귀 시작점 |
| **CONNECT BY** | Oracle 전용 (비표준) |
| <strong>BOM</strong> | 부품 계층 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Self JOIN (기본)] -> [CONNECT BY (Oracle, 1990s)]
    -> [Recursive CTE (SQL:1999 표준)]
    -> [Materialized Path / Nested Set (대안)]
    -> [현재: Graph Query (Neo4j) — 복잡 계층 전용]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Self JOIN은 <strong>같은 가족사진에서 부모와 자식</strong>을 찾는 거예요.
2. Recursive CTE는 **가계도를 위에서 아래로** 쭉 따라가는 거예요.
3. 시조(할아버지)부터 시작해서 **자손을 계속 찾아** 내려가요!
