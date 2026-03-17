+++
title = "18. 로드 밸런싱 (Load Balancing)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["Load-Balancing", "HAProxy", "ProxySQL", "Pgpool-II", "Read-Splitting"]
draft = false
+++

# 로드 밸런싱 (Load Balancing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로드 밸런싱은 **"여러 DB **서버에 **요청을 **분산**시켜 **성능**을 **최적화**하고 **가용성**을 **높이는 **기술"**으로, **L4**(TCP/IP) 또는 **L7**(Application) **로드 밸런서**가 **요청**을 **분배**하고 **Health Check**로 **서버 상태**를 **감시**한다.
> 2. **알고리즘**: **Round Robin**, **Least Connections**, **IP Hash**, **Weighted**로 **분산**하며 **Read Splitting**(읽기 분산)을 통해 **Primary**가 **쓰기**를 **처리**하고 **Replica**가 **읽기**를 **분산**처리**한다.
> 3. **융합**: **ProxySQL**(MySQL), **Pgpool-II**(PostgreSQL), **HAProxy**, **Nginx**가 **대표적**이며 **Connection Pooling**으로 **DB 연결**을 **재사용**하고 **Query Routing**으로 **Smart Sharding**을 **지원**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
로드 밸런싱은 **"요청을 여러 서버에 분산하는 기술"**이다.

**로드 밸런싱 목적**:
- **분산**: 요청 분배
- **성능**: 병렬 처리
- **가용성**: 장애 회피
- **확장**: 수평 확장

### 💡 비유
로드 밸런싱은 **"은행 창구 관리자****와 같다.
- **고객**: 요청
- **창구**: DB 서버
- **관리자**: 로드 밸런서

---

## Ⅱ. 아키텍처 및 핵심 원리

### 로드 밸런싱 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         DB Load Balancing Architecture                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  Application
    Read Requests  ────────────────────────┐
    Write Requests ───────────┐            │
                              ▼            ▼
  Load Balancer (ProxySQL / Pgpool-II)
    Query Router:
      • Write → Primary (Single)
      • Read  → Replica (Multiple)
    Health Check: TCP/SQL Query Ping
                │    │    │    │
                ▼    ▼    ▼    ▼
  Primary  Replica1 Replica2 Replica3 Replica4
   (R/W)    (R)     (R)     (R)     (R)
```

### 로드 밸런싱 알고리즘

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Load Balancing Algorithms                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  1. Round Robin (순차 할당)
    Request 1 → Replica 1
    Request 2 → Replica 2
    Request 3 → Replica 3
    Request 4 → Replica 1 (Loop)

  2. Least Connections (최소 연결)
    Replica 1: 10 connections ───────→ Request to Replica 3 (only 2)
    Replica 2: 15 connections             │
    Replica 3: 2 connections  ────────┘

  3. IP Hash (IP 해시)
    hash(client_ip) % replica_count → Replica
    • 동일 클라이언트는 항상 같은 Replica
    • Session Consistency 보장

  4. Weighted (가중치)
    Replica 1: weight=3  ────→ 60% of traffic
    Replica 2: weight=1  ────→ 20% of traffic
    Replica 3: weight=1  ────→ 20% of traffic
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 로드 밸런서 비교

| 도구 | DB | 유형 | 특징 |
|------|-----|------|------|
| **ProxySQL** | MySQL | L7 | Query Cache, Query Routing |
| **HAProxy** | All | L4/L7 | 범용, 고성능 |
| **Pgpool-II** | PostgreSQL | L7 | Connection Pool, Replication |
| **Nginx** | All | L7 | Reverse Proxy |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: ProxySQL 설정
**상황**: MySQL 로드 밸런싱
**판단**:

```sql
-- ProxySQL Query Rules

-- Write to Primary
INSERT INTO mysql_query_rules (rule_id, active, match_pattern, destination_hostgroup, apply)
VALUES (1, 1, '^SELECT.*FOR UPDATE', 10, 1);

-- Read from Replicas
INSERT INTO mysql_query_rules (rule_id, active, match_pattern, destination_hostgroup, apply)
VALUES (2, 1, '^SELECT', 20, 1);

-- Load to ProxySQL
LOAD MYSQL QUERY RULES TO RUN;
SAVE MYSQL QUERY RULES TO DISK;
```

---

## Ⅴ. 기대효과 및 결론

### 로드 밸런싱 기대 효과

| 효과 | 단일 DB | 로드 밸런싱 |
|------|--------|-----------|
| **읽기 성능** | 제한됨 | N배 증가 |
| **가용성** | 낮음 | 높음 |
| **확장성** | 어려움 | 쉬움 |

### 모범 사례

1. **Health Check**: 주기적 검사
2. **Connection Pool**: 재사용
3. **Timeout**: 적절한 설정

### 미래 전망

1. **Smart Routing**: AI 기반
2. **Auto-scaling**: 자동 확장
3. **Service Mesh**: 통합 관리

### ※ 참고 표준/가이드
- **ProxySQL**: proxysql.com
- **Pgpool-II**: pgpool.net
- **HAProxy**: haproxy.org

---

## 📌 관련 개념 맵

- [복제](./15_replication.md) - 데이터 복제
- [클러스터링](./16_clustering.md) - 클러스터
- [장애 조치](./17_failover.md) - Failover
