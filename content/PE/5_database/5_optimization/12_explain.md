+++
title = "12. 실행 계획 (Explain Plan)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["Explain", "Execution-Plan", "Query-Plan", "Optimizer", "Access-Path"]
draft = false
+++

# 실행 계획 (Explain Plan)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 실행 계획은 **"Optimizer가 **수립한 **쿼리 실행 방법**에 대한 **상세 계획"**으로, **EXPLAIN**(MySQL), **EXPLAIN ANALYZE**(PostgreSQL), **Query Plan**(SQL Server)로 **조회** 가능하며 **Access Method**(Full Scan, Index Scan), **Join Method**, **연산 순서**를 **표시**한다.
> 2. **가치**: **느린 쿼리**의 **병목 원인**을 **파악**하고 **인덱스 추가**, **쿼리 재작성**, **힌트**(Hint) 사용으로 **성능을 개선**하며 **비용**(Cost)과 **실제 실행 시간**을 **비교**하여 **Optimizer의 판단**을 **검증**할 수 있다.
> 3. **융합**: **PostgreSQL EXPLAIN ANALYZE**는 **실제 실행 통계**(Actual Time, Rows)를 제공하고 **MySQL EXPLAIN FORMAT=JSON**은 **상세한 계획**을 보여주며 **Visual Explain Tool**(**pgAdmin**, **DBeaver**)로 **시각화** 가능하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
실행 계획은 **"DBMS가 쿼리를 실행하는 방법에 대한 계획"**이다.

**실행 계획의 구성**:
- **Access Path**: 테이블 접근 방법 (Full Scan, Index Scan)
- **Join Method**: 조인 방법 (Nested Loop, Hash, Merge)
- **Join Order**: 테이블 조인 순서
- **Operation**: 정렬(Sort), 집계(Aggregate), 필터(Filter)

### 💡 비유
실행 계획은 **"내비게이션 경로"**와 같다.
- **출발지 → 목적지**: 쿼리 실행
- **경로**: 실행 계획
- **교통 상황**: 비용(Cost)
- **예상 시간**: 비용 추정

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         실행 계획의 발전                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

System R (1970년대):
    • Rule-Based Optimizer
    • 단순 규칙
         ↓
Cost-Based (1980년대):
    • 통계 기반
    • 비용 모델
         ↓
현대:
    • EXPLAIN 명령어
    • Visual Explain
    • AI-Based Optimization
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### MySQL EXPLAIN

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MySQL EXPLAIN                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  EXPLAIN SELECT u.name, o.total                                                         │
    │         FROM users u                                                                   │
    │         JOIN orders o ON u.id = o.user_id                                              │
    │         WHERE u.status = 'active' AND o.created_at > '2026-01-01';                      │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  id │ select_type │ table │ type  │ possible_keys │ key           │ ref  │ rows │ filtered│ Extra         │
    │  │  ────────────────────────────────────────────────────────────────────────────────────  │  │
    │  │  1  │ SIMPLE      │ u     │ ref   │ idx_status    │ idx_status    │ const│ 1000 │ 100.00  │ Using where  │
    │  │  1  │ SIMPLE      │ o     │ ref   │ idx_user_id  │ idx_user_id  │ id   │    5 │  33.33  │ Using where  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [컬럼 설명]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • id: SELECT 순서                                                                   │  │
    │  │  • select_type: SIMPLE, PRIMARY, SUBQUERY, DERIVED 등                               │  │
    │  │  • type: 접근 유형 (성능 순)                                                         │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  system > const > eq_ref > ref > fulltext > ref_or_null > index_merge >       │  │  │
    │  │  │  unique_subquery > index_subquery > range > index > ALL                       │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │  • possible_keys: 사용 가능한 인덱스                                                 │  │
    │  │  • key: 실제 선택한 인덱스                                                           │  │
    │  │  • rows: 예상 검색 행 수                                                              │  │
    │  │  • Extra: 추가 정보                                                                 │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘
```

### PostgreSQL EXPLAIN

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         PostgreSQL EXPLAIN ANALYZE                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  EXPLAIN (ANALYZE, BUFFERS, VERBOSE) SELECT u.name, o.total                           │
    │         FROM users u                                                                   │
    │         JOIN orders o ON u.id = o.user_id                                              │
    │         WHERE u.status = 'active';                                                      │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Hash Join  (cost=123.45..234.56 rows=1000 width=64)                                │  │
    │  │    (actual time=5.234..12.456 rows=1000 loops=1)                                     │  │
    │  │    Hash Cond: (o.user_id = u.id)                                                    │  │
    │  │    ->  Seq Scan on orders o  (cost=0.00..89.50 rows=5000 width=32)                   │  │
    │  │          (actual time=0.012..3.456 rows=5000 loops=1)                               │  │
    │  │          Filter: (created_at > '2026-01-01'::date)                                  │  │
    │  │          Rows Removed by Filter: 1500                                               │  │
    │  │          Buffers: shared hit=32 read=45                                             │  │
    │  │    ->  Hash  (cost=22.00..22.00 rows=1000 width=32)                                 │  │
    │  │          (actual time=0.234..0.234 rows=1000 loops=1)                                │  │
    │  │          Buckets: 1024  Batches: 1  Memory Usage: 64kB                               │  │
    │  │          ->  Index Scan using idx_users_status on users u                           │  │
    │  │                (cost=0.28..22.00 rows=1000 width=32)                                 │  │
    │  │                (actual time=0.012..0.123 rows=1000 loops=1)                           │  │
    │  │                Index Cond: (status = 'active'::text)                                  │  │
    │  │                Buffers: shared hit=50                                                │  │
    │  │                                                                                  │  │
    │  │  Planning Time: 0.456 ms                                                            │  │
    │  │  Execution Time: 13.789 ms                                                          │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [필드 설명]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • cost: 예상 비용 (lower is better)                                                     │
    │  │  • rows: 예상 행 수                                                                   │
    │  │  • actual time: 실제 실행 시간 (ms)                                                    │
    │  │  • rows: 실제 반환 행 수                                                              │
    │  │  • loops: 반복 횟수                                                                   │
    │  │  • Buffers: 버퍼 사용 현황                                                           │
    │  │    - shared hit: 공유 버퍼에서 Cache Hit                                              │
    │  │    - read: 디스크에서 읽기                                                             │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘
```

### 실행 계획 시각화

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         실행 계획 트리                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Sort (ORDER BY created_at DESC)                                                   │  │
    │  │  cost=300, rows=1000                                                                │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Hash Join (u.id = o.user_id)                                                  │  │  │
    │  │  │  cost=200, rows=1000                                                            │  │  │
    │  │  │  ┌─────────────────────────────┐  ┌──────────────────────────────────────┐  │  │  │
    │  │  │  │  Seq Scan on users u       │  │  Index Scan on orders o             │  │  │  │
    │  │  │  │  Filter: status='active'   │  │  Index: idx_orders_user_id          │  │  │  │
    │  │  │  │  cost=50, rows=1000        │  │  cost=100, rows=5000               │  │  │  │
    │  │  │  └─────────────────────────────┘  └──────────────────────────────────────┘  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │
    │  [실행 순서]                                                                            │
    │  1. Seq Scan on users u (status='active' 필터링)                                         │
    │  2. Index Scan on orders o (idx_orders_user_id 사용)                                     │
    │  3. Hash Join (user_id 기반 조인)                                                       │
    │  4. Sort (created_at DESC 정렬)                                                        │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 접근 방식별 성능

| 접근 방식 | Cost | 적합 상황 |
|----------|------|----------|
| **Seq Scan** | 높음 | 소량 데이터, 전체 테이블 |
| **Index Scan** | 중간 | 범위 조회 |
| **Index Lookup** | 낮음 | 단일 행 조회 |
| **Bitmap Index Scan** | 중간 | OR 조건, 여러 인덱스 |

### 실행 계획 개선 사례

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         실행 계획 개선                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [문제 쿼리]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';                      │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Seq Scan on orders  (cost=0.00..1234.56 rows=1 width=100)                          │  │
    │  │    Filter: (user_id = 123 AND status = 'pending')                                   │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │  → Full Table Scan (느림!)                                                            │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [인덱스 추가 후]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CREATE INDEX idx_orders_user_status ON orders(user_id, status);                       │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Index Only Scan using idx_orders_user_status  (cost=0.42..8.44 rows=1 width=100)  │  │
    │  │    Index Cond: (user_id = 123 AND status = 'pending')                              │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │  → Index Only Scan (빠름!)                                                            │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [비교]
    • Cost: 1234.56 → 8.44 (146배 감소)
    • Access Method: Seq Scan → Index Only Scan
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 느린 쿼리 분석
**상황**: 주문 조회 쿼리 느림
**판단**:

```sql
-- 1. EXPLAIN ANALYZE로 실행 계획 확인
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, u.name, p.name
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
WHERE o.status = 'pending'
  AND o.created_at > '2026-01-01';

-- 2. 문제점 발견
-- → Nested Loop Join이 아닌 Seq Scan 여러 번 발생

-- 3. 인덱스 추가
CREATE INDEX idx_orders_status_created ON orders(status, created_at);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_product ON orders(product_id);

-- 4. 통계 정보 업데이트
ANALYZE orders;
ANALYZE users;
ANALYZE products;

-- 5. 다시 EXPLAIN
-- → Hash Join으로 변경, Cost 감소 확인

-- 6. 힌트 사용 (MySQL)
SELECT o.id, u.name, p.name
FROM orders o FORCE INDEX (idx_orders_status_created)
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
WHERE o.status = 'pending'
  AND o.created_at > '2026-01-01';

-- 7. Visual Tool 활용
-- → DBeaver, pgAdmin에서 시각화된 계획 확인
```

---

## Ⅴ. 기대효과 및 결론

### 실행 계획 분석 기대 효과

| 효과 | 분석 전 | 분사 후 |
|------|--------|--------|
| **병목 파악** | 어려움 | 명확 |
| **인덱스 활용** | 미확인 | 검증 |
| **조인 방식** | 알 수 없음 | 확인 |
| **Cost 절감** | - | O |

### 실행 계획 모범 사례

1. **정기 분석**: 느린 쿼리 로그 확인
2. **실제 실행**: ANALYZE 옵션 사용
3. **시각화**: 도구 활용 (pgAdmin, DBeaver)
4. **통계 관리**: 주기적인 ANALYZE
5. **힌트 최소화**: Optimizer에 맡기기

### 미래 전망

1. **AI Plan**: 자동 최적화
2. **Adaptive Plan**: 실행 중 변경
3. **Parallel Plan**: 병렬 처리

### ※ 참고 표준/가이드
- **PostgreSQL**: EXPLAIN Documentation
- **MySQL**: EXPLAIN Output Format
- **SQL Server**: Query Execution Plan

---

## 📌 관련 개념 맵

- [쿼리 최적화](./10_query_optimization.md) - 최적화 기법
- [통계 정보](./11_statistics.md) - 비용 추정
- [인덱스](../4_index/9_index.md) - 접근 방법
- [조인 알고리즘](./13_join.md) - 조인 방식
