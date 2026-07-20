---
title: "Sql Inner Join Intersection"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 133
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: INNER JOIN은 <strong>두 테이블에서 조인 조건을 만족하는 행만 반환</strong>하는 교집합(∩) 연산이며, 가장 기본적이고 빈번한 JOIN 유형이다.
> 2. **가치**: 정규화로 분리된 테이블의 데이터를 <strong>의미 있는 하나의 결과로 결합</strong>하며, 매칭되지 않는 행은 자동 제외되므로 <strong>결과가 항상 완전한 데이터</strong>이다(NULL 없음).
> 3. **판단 포인트**: Equi-Join(=), Non-Equi-Join(<,>), Natural Join(동일 컬럼명 자동 매칭)을 구분하고, <strong>인덱스가 JOIN 성능을 결정</strong>한다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT e.name, d.dept_name
FROM emp e INNER JOIN dept d ON e.dept_id = d.id
-> 양쪽 모두 매칭되는 행만 반환 (교집합)
```

- **📢 섹션 요약 비유**: INNER JOIN은 **양쪽 명단에 모두 있는 사람만** 뽑는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| JOIN 알고리즘 | 설명 |
|:---|:---|
| <strong>Nested Loop</strong> | 소규모, 인덱스 활용 |
| <strong>Hash Join</strong> | 대규모, 동등 조건 |
| <strong>Merge Join</strong> | 정렬된 데이터 |

---

## Ⅲ~Ⅴ. 결론

INNER JOIN은 <strong>SQL의 가장 기본 연산</strong>이며, 인덱스·실행 계획 최적화가 성능의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>INNER JOIN</strong> | 교집합 (양쪽 매칭) |
| <strong>Equi-Join</strong> | = 조건 |
| <strong>Natural Join</strong> | 동일 컬럼 자동 매칭 |
| <strong>Hash Join</strong> | 대규모 최적화 |
| <strong>실행 계획</strong> | EXPLAIN ANALYZE |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cartesian Product] -> [Theta Join (조건)] -> [Equi-Join (=)]
    -> [INNER JOIN (SQL-92)] -> [Hash/Merge Join 최적화]
    -> [현재: Adaptive Join — 런타임 최적 알고리즘 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. INNER JOIN은 **양쪽 명단에 모두 있는 사람만** 뽑아요.
2. A반 명단과 B반 명단에서 **겹치는 사람만** 결과에 나와요.
3. 안 겹치는 사람은 **자동으로 빠지니** 결과에 빈칸(NULL)이 없어요!
