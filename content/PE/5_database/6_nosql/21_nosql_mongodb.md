+++
title = "21. NoSQL (MongoDB)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["NoSQL", "MongoDB", "Document-Database", "BSON", "Aggregation"]
draft = false
+++

# NoSQL (MongoDB)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MongoDB는 **"문서 **지향**(Document-Oriented) **NoSQL **데이터베이스"**로, **BSON**(Binary JSON) **형식**으로 **JSON**과 유사한 **문서**를 **저장**하고 **Schema-less**(스키마 없음)으로 **유연한 **데이터 **모델**을 **지원**하며 **Sharding**으로 **수평 **확장**이 **가능**하다.
> 2. **특징**: **Embedding**(포함)으로 **JOIN**을 **줄이고** **Indexing**으로 **검색**을 **최적화**하며 **Replica Set**으로 **고가용성**을 **제공**하고 **Aggregation Pipeline**으로 **복잡한 **데이터 **처리**를 **지원**한다.
> 3. **융합**: **RDBMS**(관계형)와 **달리** **ACID**보다 **Eventual Consistency**를 **우선**하고 **CAP Theorem**에서 **AP**(Availability + Partition Tolerance)를 **선택**하며 **Ad-hoc Query**에 **적합**하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
NoSQL은 **"Not Only SQL"** 데이터베이스다.

**NoSQL 유형**:
- **Document**: MongoDB, Couchbase
- **Key-Value**: Redis, DynamoDB
- **Column**: Cassandra, HBase
- **Graph**: Neo4j, ArangoDB

### 💡 비유
NoSQL은 **"폴더식 파일 정리****와 같다.
- **문서**: 파일
- **컬렉션**: 폴더
- **유연함**: 형식 자유

---

## Ⅱ. 아키텍처 및 핵심 원리

### MongoDB 데이터 모델

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MongoDB Document Model                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  {                                                                                     │  │
    │    "_id": ObjectId("507f1f77bcf86cd799439011"),                                       │  │
    │    "name": "John Doe",                                                                 │  │
    │    "email": "john@example.com",                                                        │  │
    │    "age": 30,                                                                         │  │
    │    "address": {                                                                       │  │
    │      "street": "123 Main St",                                                          │  │
    │      "city": "New York",                                                               │  │
    │      "state": "NY",                                                                   │  │
    │      "zip": "10001"                                                                   │  │
    │    },                                                                                  │  │
    │    "orders": [           // Embedded (1:N 관계 포함)                                     │  │
    │      {                                                                                │  │
    │        "orderId": "order1",                                                           │  │
    │        "amount": 100                                                                   │  │
    │      },                                                                               │  │
    │      {                                                                                │  │
    │        "orderId": "order2",                                                           │  │
    │        "amount": 200                                                                   │  │
    │      }                                                                                │  │
    │    ],                                                                                 │  │
    │    "createdAt": ISODate("2026-03-06T00:00:00Z")                                       │  │
    │  }                                                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Aggregation Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Aggregation Pipeline                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  db.orders.aggregate([                                                                  │  │
    │    { $match: { status: "completed" } },      // WHERE                                   │  │
    │    { $group: {                                        // GROUP BY                          │  │
    │        _id: "$customerId",                                                              │  │
    │        total: { $sum: "$amount" },                                                      │  │
    │        count: { $sum: 1 }                                                               │  │
    │    }},                                                                                 │  │
    │    { $sort: { total: -1 } },                  // ORDER BY                                │  │
    │    { $limit: 10 }                              // LIMIT                                   │  │
    │  ])                                                                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### RDBMS vs NoSQL

| 구분 | RDBMS | NoSQL |
|------|-------|-------|
| **Schema** | 고정 | 유연 |
| **Query** | SQL | Ad-hoc |
| **확장** | 수직 | 수평 |
| **ACID** | 강함 | 유연 |

### NoSQL 유형 비교

| 유형 | 대표 | 용도 |
|------|------|------|
| **Document** | MongoDB | 유연 데이터 |
| **Key-Value** | Redis | 캐시 |
| **Column** | Cassandra | 대량 쓰기 |
| **Graph** | Neo4j | 관계 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: MongoDB 설계
**상황**: Blog 서비스
**판단**:

```javascript
// Embedding (1:N)
{
  _id: "post1",
  title: "My Post",
  content: "...",
  comments: [
    { user: "Alice", text: "Great!" },
    { user: "Bob", text: "Nice!" }
  ]
}

// Referencing (N:N)
// User
{
  _id: "user1",
  name: "Alice",
  posts: ["post1", "post2"]  // 참조
}

// Post
{
  _id: "post1",
  title: "My Post",
  author_id: "user1"  // 참조
}
```

---

## Ⅴ. 기대효과 및 결론

### NoSQL 기대 효과

| 효과 | RDBMS | NoSQL |
|------|-------|-------|
| **스키마** | 엄격함 | 유연함 |
| **확장성** | 제한적 | 높음 |
| **일관성** | 강함 | 유연함 |

### 미래 전망

1. **Multi-Model**: 단일 DB
2. **ACID**: 강화
3. **Serverless**: Cloud

### ※ 참고 표준/가이드
- **MongoDB**: mongodb.com
- **BSON**: bsonspec.org

---

## 📌 관련 개념 맵

- [ACID](./4_transaction.md) - 트랜잭션
- [Replica Set](./15_replication.md) - 복제
- [Sharding](./14_sharding.md) - 샤딩
