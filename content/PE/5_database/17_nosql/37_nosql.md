+++
title = "37. NoSQL 데이터베이스 (NoSQL Databases)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["NoSQL", "MongoDB", "Cassandra", "Redis", "CAP-Theorem"]
draft = false
+++

# NoSQL 데이터베이스 (NoSQL Databases)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL은 **"비관계형**(Non-**Relational)** **데이터베이스**로 **SQL**을 **사용**하지 **않고 **스키마**가 **유연**하며 **수평 **확장**(Horizontal **Scaling)**에 **최적화**되어 **있다.
> 2. **데이터 모델**: **Document**(MongoDB)**, **Key-Value**(Redis)**, **Column-Family**(Cassandra)**, **Graph**(Neo4j)**가 **있고 **CAP **Theorem**(Consistency, **Availability, **Partition **Tolerance)**에서 ** trade-off**가 **존재**한다.
> 3. **분산**: **Sharding**(데이터 **분산)**과 **Replication**(복제)**로 **확장성**과 **가용성**을 **보장**하고 **Eventual **Consistency**(최종 **일관성)**를 **허용**하여 **성능**을 **향향**시킨다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
NoSQL은 **"Not Only SQL"** 데이터베이스다.

**NoSQL 유형**:
| 유형 | 대표 DB | 데이터 모델 | 사용처 |
|------|---------|-------------|--------|
| **Document** | MongoDB | JSON/BSON | 콘텐츠, 프로필 |
| **Key-Value** | Redis, DynamoDB | Key-Value | 캐시, 세션 |
| **Column** | Cassandra, HBase | Wide Column | 시계열, 로그 |
| **Graph** | Neo4j | Node/Edge | 소셜, 추천 |

### 💡 비유
NoSQL은 ****폴더 ****철 ****과 같다.
- **Document**: 파일
- **Key-Value**: 색인
- **Column**: 엑셀
- **Graph**: 연결망

---

## Ⅱ. 아키텍처 및 핵심 원리

### Document Database (MongoDB)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MongoDB Document Model                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Document Structure (BSON):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  {                                                                                      │  │
    │      "_id": ObjectId("507f1f77bcf86cd799439011"),                                        │  │
    │      "name": "John Doe",                                                                │  │
    │      "email": "john@example.com",                                                       │  │
    │      "age": 30,                                                                         │  │
    │      "address": {                                                                       │  │
    │          "street": "123 Main St",                                                       │  │
    │          "city": "New York",                                                            │  │
    │          "zip": "10001"                                                                 │  │
    │      },                                                                                 │  │
    │      "hobbies": ["reading", "gaming"],                                                  │  │
    │      "orders": [                                                                        │  │
    │          {"orderId": "ORD001", "total": 100},                                           │  │
    │          {"orderId": "ORD002", "total": 200}                                            │  │
    │      ],                                                                                 │  │
    │      "createdAt": ISODate("2024-01-01T00:00:00Z")                                       │  │
    │  }                                                                                      │  │
    │  → Flexible schema: each document can have different fields                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Query Examples:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Find users aged 25-35                                                              │  │
    │  db.users.find({ age: { $gte: 25, $lte: 35 } })                                          │  │
    │                                                                                          │  │
    │  // Find users in NYC with "gaming" hobby                                               │  │
    │  db.users.find({                                                                         │  │
    │      "address.city": "New York",                                                         │  │
    │      hobbies: "gaming"                                                                   │  │
    │  })                                                                                      │  │
    │                                                                                          │  │
    │  // Aggregation: Average order value by age group                                        │  │
    │  db.users.aggregate([                                                                    │  │
    │      { $unwind: "$orders" },                                                             │  │
    │      { $group: {                                                                         │  │
    │          _id: "$age",                                                                    │  │
    │          avgOrderValue: { $avg: "$orders.total" }                                        │  │
    │      }}                                                                                  │  │
    │  ])                                                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Key-Value Store (Redis)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Redis Data Structures                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Data Types:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Strings                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  SET user:1000:name "John Doe"                                                       │  │  │
    │  │  GET user:1000:name  → "John Doe"                                                    │  │  │
    │  │  INCR counter  → 1 (atomic increment)                                                │  │  │
    │  │  EXPIRE session:abc 3600  (delete after 1 hour)                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. Hashes (Field-Value pairs)                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  HSET user:1000 name "John Doe" email "john@example.com"                              │  │  │
    │  │  HGET user:1000 name  → "John Doe"                                                    │  │  │
    │  │  HGETALL user:1000  → {name: "John Doe", email: "john@example.com"}                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. Lists (Ordered, duplicate allowed)                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  LPUSH queue:tasks "task1" "task2" "task3"                                            │  │  │
    │  │  RPOP queue:tasks  → "task1" (FIFO)                                                   │  │  │
    │  │  LLEN queue:tasks  → 2                                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  4. Sets (Unordered, unique)                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  SADD tags:article:100 "tech" "programming" "database"                                │  │  │
    │  │  SISMEMBER tags:article:100 "tech"  → 1 (true)                                        │  │  │
    │  │  SMEMBERS tags:article:100  → {"tech", "programming", "database"}                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  5. Sorted Sets (Score-based ordering)                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  ZADD leaderboard 1000 "player1" 1500 "player2" 800 "player3"                         │  │  │
    │  │  ZRANGE leaderboard 0 -1 WITHSCORES  → ["player3", 800, "player1", 1000, ...]         │  │  │
    │  │  ZRANK leaderboard "player2"  → 2 (rank)                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Column-Family Store (Cassandra)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Cassandra Data Model                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Keyspace → Column Family → Row → Columns
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Keyspace: ecommerce                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Column Family: users                                                                │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │  │
    │  │  │  Partition Key: user_id                                                           │  │  │  │  │
    │  │  │  Clustering Key: created_at (DESC)                                                │  │  │  │  │
    │  │  │                                                                                    │  │  │  │  │
    │  │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │  │  │
    │  │  │  │  Row Key: user_1000                                                             │  │  │  │  │  │
    │  │  │  │  Columns:                                                                       │  │  │  │  │  │
    │  │  │  │  │  created_at: 2024-01-01  │  name: "John"  │  email: "john@..." │  ...    │  │  │  │  │  │
    │  │  │  │  ───────────────────────────────────────────────────────────────────────────────────  │  │  │  │  │  │
    │  │  │  │  │  created_at: 2024-01-02  │  action: "login"  │  ip: "1.2.3.4"  │  ...    │  │  │  │  │  │
    │  │  │  │  │  created_at: 2024-01-03  │  action: "purchase"  │  amount: 100  │  ...    │  │  │  │  │  │
    │  │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
    │  → Wide columns: Each row can have different columns                                    │  │
    │  → Partition key determines data distribution across nodes                               │  │
    │  → Clustering key determines ordering within partition                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Query Examples (CQL):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  -- Create table                                                                         │  │
    │  CREATE TABLE users (                                                                    │  │
    │      user_id UUID,                                                                      │  │
    │      created_at TIMESTAMP,                                                              │  │
    │      name TEXT,                                                                         │  │
    │      email TEXT,                                                                        │  │
    │      PRIMARY KEY (user_id, created_at)                                                   │  │
    │  ) WITH CLUSTERING ORDER BY (created_at DESC);                                           │  │
    │                                                                                          │  │
    │  -- Insert data                                                                          │  │
    │  INSERT INTO users (user_id, created_at, name, email)                                   │  │
    │  VALUES (uuid(), toTimestamp(now()), 'John', 'john@example.com');                        │  │
    │                                                                                          │  │
    │  -- Query (must include partition key)                                                   │  │
    │  SELECT * FROM users WHERE user_id = ?;                                                   │  │
    │  SELECT * FROM users WHERE user_id = ? AND created_at > ?;                                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### NoSQL 데이터베이스 비교

| DB | 유형 | CAP 선택 | 일관성 | 확장성 | 사용처 |
|----|------|----------|--------|--------|--------|
| **MongoDB** | Document | CP | 강함 | 수평 | 일반 |
| **Redis** | Key-Value | AP | 약함 | 수평 | 캐시 |
| **Cassandra** | Column | AP | 최종 | 수평 | 대량 |
| **Neo4j** | Graph | CA | 강함 | 수직 | 연결 |

### CAP Theorem

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CAP Theorem Trade-offs                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Consistency vs Availability (Partition Tolerance is required):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CP (Consistency + Partition Tolerance):                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Priority: Data consistency                                                        │  │  │
    │  │  • Sacrifice: Availability (reject writes during partition)                           │  │  │
    │  │  • Example: MongoDB, HBase                                                           │  │  │
    │  │  → Good: Financial systems                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  AP (Availability + Partition Tolerance):                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Priority: Always available                                                        │  │  │
    │  │  • Sacrifice: Consistency (eventual consistency)                                      │  │  │
    │  │  • Example: Cassandra, DynamoDB                                                       │  │  │
    │  │  → Good: Social media, caching                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  CA (Consistency + Availability):                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Priority: Consistency + availability                                              │  │  │
    │  │  • Sacrifice: Partition tolerance (single region)                                    │  │  │
    │  │  • Example: RDBMS, Single-node Redis                                                  │  │  │
    │  │  → Good: Traditional monoliths                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Sharding

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MongoDB Sharding                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Sharded Cluster:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Mongos Routers (Query Routers)                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  mongos-1        mongos-2        mongos-3                                            │  │  │
    │  │  └──────────────────┬──────────────────┘                                            │  │  │
    │  └─────────────────────┼──────────────────────────────────────────────────────────────────  │  │
    │                        ▼                                                                     │  │
    │  Config Servers (Metadata)                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  config-1 (primary)    config-2 (secondary)    config-3 (secondary)                   │  │  │
    │  │  → Stores: shard key ranges, chunk locations                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                        │                                                                     │  │
    │                        ▼                                                                     │  │
    │  Shard Servers (Data Nodes)                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Shard A (Primary)         Shard B (Primary)         Shard C (Primary)                │  │  │
    │  │  Shard A (Secondary)      Shard B (Secondary)      Shard C (Secondary)               │  │  │
    │  │  │                                                                                     │  │  │
    │  │  │  Chunk 1: user_id: 0-9999                                                         │  │  │
    │  │  │  Chunk 2: user_id: 10000-19999                                                     │  │  │
    │  │  │  Chunk 3: user_id: 20000-29999                                                     │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
    │  → Data distributed by shard key (e.g., user_id)                                         │  │
    │  → Mongos routes queries to relevant shards                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 소셜 미디어 피드 NoSQL 설계
**상황**: 사용자 포스트, 팔로워, 타임라인
**판단**: Redis + Cassandra

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Social Media Feed Storage                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Millions of posts per day                                                            │  │
    │  • Real-time feed generation                                                            │  │
    │  • Follower queries                                                                      │  │
    │  • High availability (24/7)                                                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Architecture:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Redis (Hot Data, Real-time)                                                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  // User timeline (sorted set)                                                        │  │  │
    │  │  ZADD timeline:user:1000 <timestamp> <post_id>                                        │  │  │
    │  │  ZREVRANGE timeline:user:1000 0 99  (latest 100 posts)                               │  │  │
    │  │                                                                                       │  │  │
    │  │  // Follower cache (set)                                                               │  │  │
    │  │  SADD followers:user:1000 user:2001 user:2002 user:2003                                │  │  │
    │  │  SMEMBERS followers:user:1000  (all followers)                                         │  │  │
    │  │                                                                                       │  │  │
    │  │  // Post cache (hash)                                                                  │  │  │
    │  │  HSET post:12345 content "Hello!" author_id 1000 likes 5                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. Cassandra (Persistent Storage)                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  CREATE TABLE posts (                                                                 │  │  │
    │  │      post_id UUID PRIMARY KEY,                                                        │  │  │
    │  │      user_id UUID,                                                                    │  │  │
    │  │      content TEXT,                                                                    │  │  │
    │  │      created_at TIMESTAMP,                                                            │  │  │
    │  │      likes COUNT,                                                                    │  │  │
    │  │  ) WITH CLUSTERING ORDER BY (created_at DESC);                                        │  │  │
    │  │                                                                                       │  │  │
    │  │  CREATE TABLE user_posts (                                                            │  │  │
    │  │      user_id UUID,                                                                    │  │  │
    │  │      created_at TIMESTAMP,                                                            │  │  │
    │  │      post_id UUID,                                                                    │  │  │
    │  │      content TEXT,                                                                    │  │  │
    │  │      PRIMARY KEY (user_id, created_at, post_id)                                        │  │  │
    │  │  ) WITH CLUSTERING ORDER BY (created_at DESC);                                        │  │  │
    │  │  → Fast lookup of user's posts                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. Write Path:                                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User creates post                                                                    │  │  │
    │  │  └─> 1. Write to Redis (timeline, cache)                                             │  │  │
    │  │  └─> 2. Write to Cassandra (persistent)                                               │  │  │
    │  │  └─> 3. Fanout to followers' timelines (async)                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### NoSQL 기대 효과

| DB | 쓰기 처리량 | 읽기 지연시간 | 확장성 |
|----|-------------|---------------|--------|
| **MongoDB** | 50K ops/s | 5ms | 수평 |
| **Redis** | 100K ops/s | 1ms | 수평 |
| **Cassandra** | 1M+ ops/s | 10ms | 수평 |

### 모범 사례

1. **MongoDB**: 문서, JSON
2. **Redis**: 캐시, 세션
3. **Cassandra**: 시계열, 로그
4. **Neo4j**: 그래프, 소셜

### 미래 전망

1. **Multi-Model**: ArangoDB
2. **Serverless**: DynamoDB on-demand
3. **Edge**: Cloudflare Workers KV
4. **AI**: Vector DB

### ※ 참고 표준/가이드
- **MongoDB**: Manual
- **Redis**: Best Practices
- **Cassandra**: Docs

---

## 📌 관련 개념 맵

- [관계형 DB](./2_relational/20_rdbms.md) - SQL
- [분산 DB](./15_distributed/35_distributed_db.md) - CAP
- [NewSQL](./13_newsql/33_newsql.md) - ACID
