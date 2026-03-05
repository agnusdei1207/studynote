+++
title = "31. 그래프 데이터베이스 (Graph Database)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["Graph-Database", "RDF", "SPARQL", "Property-Graph", "Gremlin"]
draft = false
+++

# 그래프 데이터베이스 (Graph Database)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 그래프 DB는 **\"노드**(Nodes, **Vertices)**와 **관계**(Edges, **Relationships)**로 **데이터**를 **저장**하고 **Traverse**(탐색)**로 **쿼리**하는 **DB\"**로, **SNS**(소셜 **네트워크), **Fraud Detection**, **Recommendation**에 **사용**된다.
> 2. **모델**: **Property Graph**(Neo4j, **Amazon Neptune**)와 **RDF**(Resource Description Framework, **Jena**, **Virtuoso)**가 **대표적**이며 **Cypher**(Neo4j), **Gremlin**(TinkerPop), **SPARQL**(RDF)**가 **쿼리 **언어**이다.
> 3. **작동**: **Node** → **Relationship** → **Property **Traversal**으로 **연결 **데이터**를 **검색**하고 **Index-Free Adjacency**로 **O(1)** **관계 **탐색**이 **가능**하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
그래프 DB는 **"관계 중심 데이터베이스"**이다.

**데이터베이스 비교**:
| 구분 | RDBMS | Graph DB |
|------|-------|----------|
| **모델** | Table | Node/Edge |
| **관계** | Foreign Key | Edge |
| **조인** | Expensive | Traversal |
| **용도** | 정형 | 연결 |

### 💡 비유
그래프 DB는 ****지하철 **노선도 ****와 같다.
- **역**: Node
- **노선**: Edge
- **환승**: Relationship

---

## Ⅱ. 아키텍처 및 핵심 원리

### Property Graph Model

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Property Graph Model (Neo4j)                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Example: Social Network
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Nodes (Person, Post)                                                                  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  (Person:1) {name: "Alice", age: 30, location: "Seoul"}                              │  │  │
    │  │  (Person:2) {name: "Bob", age: 25, location: "Busan"}                                │  │  │
    │  │  (Person:3) {name: "Charlie", age: 35, location: "Seoul"}                            │  │  │
    │  │  (Post:101) {content: "Hello world!", created: "2026-03-06"}                         │  │  │
    │  │  (Post:102) {content: "Graph DB is cool!", created: "2026-03-06"}                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Relationships (Directed, Typed)                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  (Person:1)-[:FRIENDS_WITH {since: 2020}]->(Person:2)                                │  │  │
    │  │  (Person:1)-[:FRIENDS_WITH {since: 2021}]->(Person:3)                                │  │  │
    │  │  (Person:2)-[:FRIENDS_WITH {since: 2021}]->(Person:3)                                │  │  │
    │  │  (Person:1)-[:POSTED {timestamp: 1234567890}]->(Post:101)                            │  │  │
    │  │  (Person:3)-[:LIKES {timestamp: 1234567900}]->(Post:101)                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Visual Representation:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │         Alice (Person:1)                                                                 │  │
    │              │    │                                                                       │  │
    │      FRIENDS│    │POSTED                                                                 │  │
    │              ▼    ▼                                                                       │  │
    │  ┌─────Bob─────┐  Post:101                                                               │  │
    │  │             ◄───────LIKES─── Charlie (Person:3)                                      │  │
    │  │    │ FRIENDS                                                                         │  │
    │  │    └───────────────────┐                                                              │  │
    │  └────────────────────────┘                                                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Index-Free Adjacency

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Index-Free Adjacency                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    RDBMS Join (Expensive):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  SELECT p.name, f.name                                                                   │  │
    │  FROM person p                                                                           │  │
    │  JOIN friendship f ON p.id = f.person1_id                                                │  │
    │  WHERE p.id = 1;                                                                         │  │
    │                                                                                         │  │
    │  Execution:                                                                              │  │
    │  1. Index scan on person table (O(log n))                                                │  │
    │  2. Index scan on friendship table (O(log m))                                            │  │
    │  3. Nested loop join (O(n × m) worst case)                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Graph Traversal (O(1) per hop):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Cypher query: Find Alice's friends                                                   │  │
    │  MATCH (a:Person {name: "Alice"})-[:FRIENDS_WITH]->(f:Person)                            │  │
    │  RETURN f.name;                                                                          │  │
    │                                                                                         │  │
    │  Execution:                                                                              │  │
    │  1. Find Alice node (O(1) with name index)                                               │  │
    │  2. Follow FRIENDS_WITH relationships (O(1) direct access via node pointer)              │  │
    │  3. Return friend nodes                                                                  │  │
    │                                                                                         │  │
    │  Storage:                                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Node Record (Alice):                                                                 │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  id: 1, label: "Person", props: {name: "Alice", age: 30}                          │  │  │  │
    │  │  │  first_relationship: 0x1000    →  →  →  →  →  →  →  →  →  →  →  →  →  →  →  →  →  →  →  →  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │                                                                                       │  │  │
    │  │  Relationship Record (at 0x1000):                                                     │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  id: 1, type: "FRIENDS_WITH", start_node: 1, end_node: 2                          │  │  │  │
    │  │  │  next_relationship: 0x2000                                                        │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Cypher Query Language

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Cypher Query Examples                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Find friends of friends (2-hop):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  MATCH (me:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)-[:FRIENDS_WITH]->(fof)      │  │
    │  WHERE fof.name <> "Alice" AND NOT (me)-[:FRIENDS_WITH]->(fof)                           │  │
    │  RETURN fof.name, COUNT(*) AS common_friends                                             │  │
    │  ORDER BY common_friends DESC                                                            │  │
    │  LIMIT 10;                                                                               │  │
    │                                                                                         │  │
    │  → Finds people 2 hops away, excludes direct friends and self                           │  │
    │  → Counts common friends as relevance score                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Find shortest path:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  MATCH path = shortestPath(                                                              │  │
    │      (start:Person {name: "Alice"})-[*]-(end:Person {name: "Charlie"})                   │  │
    │  )                                                                                       │  │
    │  RETURN [node IN nodes(path) | node.name] AS path_names, length(path) AS hops;          │  │
    │                                                                                         │  │
    │  → Uses BFS (Breadth-First Search) internally                                            │  │
    │  → Returns shortest sequence of relationships                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Recommend posts based on friends' likes:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  MATCH (me:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)-[:LIKES]->(post:Post)        │  │
    │  WHERE NOT (me)-[:LIKES]->(post) AND NOT (me)-[:POSTED]->(post)                          │  │
    │  RETURN post.content, COUNT(DISTINCT friend) AS like_count                               │  │
    │  ORDER BY like_count DESC, post.created DESC                                             │  │
    │  LIMIT 10;                                                                               │  │
    │                                                                                         │  │
    │  → Collaborative filtering: Recommend posts liked by friends                             │  │
    │  → Excludes posts Alice already liked or posted                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 그래프 DB 비교

| DB | 모델 | 언어 | 사용처 |
|----|------|------|--------|
| **Neo4j** | Property Graph | Cypher | 범용 |
| **Amazon Neptune** | Property Graph | Gremlin, SPARQL | AWS |
| **ArangoDB** | Multi-model | AQL | Hybrid |
| **Jena** | RDF | SPARQL | Semantic Web |

### RDF Model (Triple Store)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RDF Triple Model                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Triple Structure: (Subject, Predicate, Object)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  (Alice, knows, Bob)                                                                   │  │
    │  (Alice, knows, Charlie)                                                               │  │
    │  (Bob, knows, Charlie)                                                                 │  │
    │  (Alice, age, 30)                                                                      │  │
    │  (Bob, age, 25)                                                                        │  │
    │  (Charlie, age, 35)                                                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    SPARQL Query:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  PREFIX foaf: <http://xmlns.com/foaf/0.1/>                                              │  │
    │                                                                                         │  │
    │  SELECT ?friend ?age                                                                    │  │
    │  WHERE {                                                                                │  │
    │    ?alice foaf:name "Alice" .                                                           │  │
    │    ?alice foaf:knows ?friend .                                                          │  │
    │    ?friend foaf:age ?age .                                                              │  │
    │    FILTER (?age > 28)                                                                   │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → Finds friends of Alice older than 28                                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 사기 탐지 (Fraud Detection)
**상황**: 금융 거래 사기 감지
**판단**: Neo4j + 실시간 탐지

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Fraud Detection with Graph DB                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Data Model:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Nodes: Account, Device, IP, Transaction, Merchant                                      │  │
    │  Relationships: TRANSFER, ACCESSED_FROM, SAME_IP, SAME_DEVICE                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Fraud Patterns:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Pattern 1: Circular Money Transfer                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  MATCH (a:Account)-[:TRANSFER]->(b:Account)-[:TRANSFER]->(c:Account)-[:TRANSFER]->(a) │  │  │
    │  │  WHERE a <> b AND b <> c AND c <> a                                                  │  │  │
    │  │  RETURN a, b, c, sum(t1.amount + t2.amount + t3.amount) AS cycle_amount              │  │  │
    │  │                                                                                       │  │  │
    │  │  → Detects money laundering cycles (A→B→C→A)                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Pattern 2: Shared suspicious attributes                                                 │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  MATCH (acc:Account)-[:ACCESSED_FROM]->(dev:Device)<-[:ACCESSED_FROM]-(other:Account)│  │  │
    │  │  WHERE acc.id <> other.id                                                             │  │  │
    │  │  WITH acc, COLLECT(DISTINCT other) AS shared_accounts                                │  │  │
    │  │  WHERE size(shared_accounts) >= 5                                                    │  │  │
    │  │  RETURN acc.id, shared_accounts                                                       │  │  │
    │  │                                                                                       │  │  │
    │  │  → Detects accounts accessing from same device (5+ accounts = suspicious)             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Pattern 3: Fast multiple transactions                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  MATCH (a:Account)-[r:TRANSFER]->(:Account)                                           │  │
    │  │  WHERE a.id = "ACC123" AND r.timestamp > timestamp() - 3600  // Last 1 hour           │  │  │
    │  │  WITH a, COUNT(r) AS tx_count, SUM(r.amount) AS total_amount                          │  │  │
    │  │  WHERE tx_count > 10 AND total_amount > 10000                                        │  │
    │  │  RETURN a.id, tx_count, total_amount                                                  │  │  │
    │  │                                                                                       │  │  │
    │  │  → Detects burst transactions (10+ tx, $10K+ in 1 hour)                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 그래프 DB 기대 효과

| 워크로드 | RDBMS | Graph DB |
|----------|-------|----------|
| **Joins** | 느림 | 빠름 |
| **Depth** | 제한 | 무제한 |
| **스키마** | 엄격 | 유연 |
| **확장** | 수직 | 수평 |

### 모범 사례

1. **모델링**: 도메인 관계 중심
2. **Index**: 속성 색인
3. **Traversal**: 짧은 경로
4. **Batch**: 대량 삽입

### 미래 전망

1. **Hybrid**: Multi-model DB
2. **Distributed**: 분산 그래프
3. **AI**: Graph ML (GNN)
4. **Real-time**: 스트리밍 그래프

### ※ 참고 표준/가이드
- **Neo4j**: neo4j.com/docs
- **W3C**: RDF, SPARQL
- **Apache**: TinkerPop

---

## 📌 관련 개념 맵

- [NoSQL 개요](./1_nosql/21_nosql_overview.md) - 비관계형 DB
- [벡터 DB](./10_nosql/30_vector_db.md) - 유사성 검색
- [Neo4j](./9_consensus/29_distributed_consensus.md) - 분산 합의

