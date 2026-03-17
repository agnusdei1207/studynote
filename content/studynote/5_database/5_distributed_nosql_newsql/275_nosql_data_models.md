+++
title = "275. NoSQL의 4대 데이터 모델 - 목적에 따른 저장의 기술"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 275
+++

# 275. NoSQL의 4대 데이터 모델 - 목적에 따른 저장의 기술

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL(Not Only SQL) 데이터 모델은 RDBMS(Relational Database Management System)의 정형화된 스키마라는 한계를 넘어, **Key-Value, Document, Column-Family, Graph** 4가지 물리적 저장 구조를 통해 데이터의 성격에 맞는 최적화된 저장소를 제공한다.
> 2. **가치**: CAP 정리(Theorem)에 기반하여 분산 환경에서의 확장성(Scalability)과 가용성(Availability)을 극대화하며, RDBMS의 조인(Join) 연산 비용을 제거하거나 관계형 질의를 최적화하여 대용량 트래픽 처리에서 압도적인 성능 저로(Latency) 감소를 달성한다.
> 3. **융합**: 현대 MSA(Microservices Architecture)에서는 폴리글랏 퍼시스턴스(Polyglot Persistence) 전략을 통해, 하나의 비즈니스 도메인 내에서라도 세션 저장엔 Redis, 로그엔 Cassandra, 추천엔 Neo4j와 같이 각기 다른 NoSQL 저장소를 융합하여 사용하는 것이 표준 아키텍처로 자리 잡았다.

---

### Ⅰ. 개요 (Context & Background) - NoSQL의 등장과 철학

NoSQL은 "No SQL"이 아니라 "Not Only SQL"을 의미하며, 관계형 데이터베이스의 ACID(Atomicity, Consistency, Isolation, Durability) 특성을 일부 희생하고 대용량 분산 처리를 가능하게 하는 데이터베이스 패러다임을 의미합니다. 기존 RDBMS는 수직적 확장(Scale-up)에 한계가 있었고, 수평적 확장(Scale-out)을 위한 Sharding(Sharding)이 복잡하다는 문제가 있었습니다. 특히 SNS(Social Networking Services)와 같은 대규모 웹 서비스에서는 테이블 간의 복잡한 관계보다는 **단순하고 빠른 데이터 접근**이 더 중요한 요구로 대두되었습니다.

이에 따라 등장한 NoSQL은 데이터의 일관성보다 가용성과 분산 처리를 우선시하는 **BASE(Basically Available, Soft state, Eventually consistent) 모델**을 채택합니다. 여기서 핵심은 **"데이터를 어떻게 저장하느냐"**, 즉 **데이터 모델(Data Model)**의 차이입니다. NoSQL은 크게 집합(Aggregate) 지향 모델(KV, Document, Column)과 관계 지향 모델(Graph)으로 나뉘며, 각각의 물리적 저장 방식이 데이터 접근 패턴을 결정합니다.

> **💡 개념 비유: 도시 교통 체계**
> RDBMS가 모든 도로를 신호등(관계 제약)으로 엄격하게 통제하는 **'계획 도시'**라면, NoSQL은 목적지에 따라 고속도로, 지하철, 골목길 등 자유롭게 이동할 수 있는 **'다중 모드 교통망'**과 같습니다. 모든 차량을 같은 도로에 몰아넣지 않고, 데이터의 성격에 맞는 전용 차로를 만들어 병목을 방지하는 것이 핵심입니다.

**등장 배경**
1.  **기존 한계**: RDBMS의 스키마 변경 비용(Schema Migration) 부담, 대용량 데이터 처리 시 Join 연산의 성능 저하.
2.  **혁신적 패러다임**: 수평적 확장(Sharding)의 용이성, Schema-less(스키마리스) 설계로 인한 개발 속도 향상, WAL(Write-Ahead Logging)과 LSM-Tree(Log-Structured Merge-Tree) 등을 통한 쓰기 성능 최적화.
3.  **현재 비즈니스 요구**: 실시간 빅데이터 처리, IoT 데이터 수집, 실시간 추천 시스템 등 초고속 쓰기/읽기가 요구되는 환경.

**📢 섹션 요약 비유**: NoSQL의 도입은 **'수도꼭지의 변화'**와 같습니다. 과거의 RDBMS가 양제 수전(정해진 틀과 압력)이라면, NoSQL은 고압 세척기, 정수기, 가습기 등 **용도에 따라 물을 사용하는 기구가 달라지는 것**과 같습니다. 물의 성격(데이터)에 따라 가장 적합한 배관을 선택하는 것이 NoSQL 설계의 첫걸음입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - 4대 모델의 내부 구조

NoSQL의 4대 데이터 모델은 데이터를 물리적으로 어떻게 인코딩하고 저장하는지에 따라 구분됩니다. 이를 이해하기 위해서는 각 모델의 **내부 데이터 레이아웃**과 **접근 알고리즘**을 살펴보아야 합니다.

#### 1. 모델별 구성 요소 비교

| 구분 | Key-Value (키-값) | Document (문서) | Column-Family (칼럼 패밀리) | Graph (그래프) |
|:---|:---|:---|:---|:---|
| **데이터 구조** | 해시 테이블 (Hash Map) | 트리 / JSON / XML | 다차원 맵 (Sorted Map) | 노드 & 엣지 (Adjacency List) |
| **저장 단위** | Value (Blob) | Document (BSON, JSON) | Column (Cell) | Vertex + Relationship |
| **핵심 최적화** | O(1) 조회 속도 | 계층형 데이터 직렬화 | 희소 행렬(Sparse Matrix) 처리 | 인접 노드 순회 (Traversal) |
| **내부 동작** | In-Memory Hashing | B-Tree Indexing | LSM-Tree Compaction | Index-free Adjacency |
| **주요 프로토콜** | Binary Protocol (TCP) | Wire Protocol (OP_QUERY) | CQL / Thrift / RPC | Cypher / Gremlin |

#### 2. 데이터 모델별 물리적 저장 구조 ASCII 다이어그램

아래 다이어그램은 각 NoSQL 모델이 데이터를 메모리나 디스크에 저장하는 방식의 개념적 차이를 도식화한 것입니다.

```text
+=============================================================================+
|                    NoSQL 4대 모델의 물리적 저장 구조 비교                     |
+=============================================================================+

[A] Key-Value Store (Hash Table / In-Memory)
-----------------------------------------------------------------------
Key Space          | Value Space (Blob)
-----------------------------------------------------------------------
"user:1001"    --->| {Byte Stream: "Profile Data..."}
"product:55"   --->| {Byte Stream: "JSON String..."}
"session:abc"  --->| {Byte Stream: "TTL=1200s..."}
(해시 충돌 없이 1차 접근 보장, O(1))

[B] Document Store (Tree Structure)
-----------------------------------------------------------------------
DocumentID: "order_2024"
  ├── MetaData: _id, _index
  └── Data: { "userId": "kim", 
              "items": [
                  { "id": 1, "qty": 2, "price": 5000 },
                  { "id": 5, "qty": 1, "price": 12000 }
              ],
              "total": 22000 }
(데이터 자체가 구조를 가짐, 애플리케이션과 1:1 매핑)

[C] Column-Family Store (Wide Column / Sparse Matrix)
-----------------------------------------------------------------------
RowKey: "User#Kim2024"
-----------------------------------------------------------------------
Column Family "Profile"        | Column Family "Activity"
+------------------+---------+  +------------------+---------+
| Column Key       | Value   |  | Column Key       | Value   |
+------------------+---------+  +------------------+---------+
| "name"           | "Kim"   |  | "2024-01-01"     | "Login" |
| "age"            | 30      |  | "2024-01-02"     | "Post"  |
| (NULL)           | (SKIP)  |  | "2024-01-03"     | "Like"  |
+------------------+---------+  +------------------+---------+
(칼럼이 동적으로 추가 가능, NULL 값 비용 0)

[D] Graph Store (Network Structure)
-----------------------------------------------------------------------
(Node: User) -------------------> (Node: Product)
      |                                   ^
   [Edge: BUY]                        [Edge: BOUGHT_BY]
      |                                   |
      v                                   |
(Node: Category) <--------------- (Node: User)
                    [Edge: BELONGS_TO]
(관계를 포인터로 연결, 조인 없이 순회)

+=============================================================================+
```

#### 3. 심층 동작 원리 및 핵심 알고리즘

**① Key-Value Model**
- **내부 메커니즘**: 대부분의 KV 저장소는 데이터를 주 메모리(RAM)에 적재하고, 백엔드로 디스크를 사용합니다. Key를 해싱(Hashing)하여 메모리 주소를 계산하므로 시간 복잡도는 **O(1)**입니다.
- **기술적 특징**: TTL(Time-To-Live) 기반의 자동 만료 지원, EP(Expire/Purge) 알고리즘. 분산 환경에서는 Consistent Hashing(일관성 해싱)을 사용하여 노드 장애 시 데이터 재배치를 최소화합니다.
- **코드 예시 (Redis CLI)**:
  ```bash
  # Set User Session with Expiration
  SET session:user:1001 "eyJhbGciOiJIUzI1NiIs..." EX 3600
  
  # Get Session
  GET session:user:1001
  ```

**② Document Model**
- **내부 메커니즘**: 데이터를 BSON(Binary JSON) 형태로 직렬화하여 저장합니다. 문서 내부의 필드에 인덱스(Index)를 생성할 수 있으며, 쿼리 엔진은 B-Tree 구조를 사용하여 복잡한 조건(Criteria)을 만족하는 문서를 빠르게 검색합니다.
- **기술적 특징**: **Aggregation Pipeline**(집계 파이프라인)을 통해 RDBMS의 GROUP BY나 JOIN과 유사한 처리를 가능하게 합니다. 하지만 다중 트랜잭션 처리(Multi-Document ACID)는 상대적으로 느리거나 제한적일 수 있습니다.

**③ Column-Family Model**
- **내부 메커니즘**: Google Bigtable 논문에서 유래했습니다. 데이터는 RowKey를 기준으로 정렬되어 저장되지만, 칼럼(Column)은 가변적입니다. 물리적으로는 LSM-Tree(Log-Structured Merge-Tree)를 사용하여 쓰기 작업(Write)을 메모리에 버퍼링했다가 디스크의 SSTable(Sorted String Table)로 배치(Batch) 처리합니다. 이로 인해 **쓰기 성능(Write Throughput)**이 극도로 높습니다.
- **기술적 특징**: 압축률이 높고, 칼럼 단위로 저장되므로 특정 데이터만 조회할 때 I/O 비용을 절감할 수 있습니다.

**④ Graph Model**
- **내부 메커니즘**: **Index-free Adjacency**(인덱스 없는 인접) 특성을 가집니다. 노드는 직접 인접한 노드의 포인터(Edge)를 가지고 있으므로, RDBMS처럼 전체 테이블을 스캔하거나 인덱스를 찾을 필요 없이 포인터를 따라가듯 그래프를 순회합니다. 이는 관계가 복잡할수록 O(N)이 아닌 관계의 깊이에 따라 탐색하는 비약적인 성능 향상을 제공합니다.
- **기술적 특징**: Cypher, Gremlin 등의 그래프 쿼리 언어를 사용하여 연결 요소(Connected Components), 최단 경로(Shortest Path) 등을 계산합니다.

**📢 섹션 요약 비유**: 4대 모델의 아키텍처 차이는 **'도서관의 분류법'**과 같습니다. KV는 **'보관함 번호로 바로 찾는 수납'**이며, Document는 **'목차가 있는 파일'**, Column은 **'날짜순으로 정리된 두꺼운 장부'**, Graph는 **'참고문헌(인용)을 따라 옮겨 다니는 연구 논문'**과 같습니다. 찾는 정보의 성격이 무엇이냐에 따라 가장 빠른 길이 달라집니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

각 NoSQL 모델은 고유한 강점을 가지지만, 특정 작업에서는 치명적인 약점을 가지기도 합니다. 올바른 기술 선정을 위해 정량적 지표와 타 영역(운영체제, 네트워크)과의 관계를 분석해야 합니다.

#### 1. 심층 기술 비교 분석표

| 비교 항목 | Key-Value (Redis) | Document (MongoDB) | Column (Cassandra) | Graph (Neo4j) |
|:---|:---|:---|:---|:---|
| **주요 용도** | 캐싱, 세션, 랭킹 | CMS, 카탈로그, 로그 | 시계열, 분석, 메시징 | SNS, 지식 그래프 |
| **읽기 패턴** | Key로 단일 조회 (Key-Get) | 복잡한 쿼리, 필터 검색 | RowKey 기반 범위 스캔 | 관계 탐색 (BFS/DFS) |
| **쓰기 패턴** | 매우 빠름 (In-Memory) | 빠름 (Insert) | 매우 빠름 (Append-only) | 느림 (관계 갱신 비용) |
| **데이터 볼륨** | RAM 크기에 의존 | 디스크 한계까지 확장 가능 | 페타바이트(PB)급 처리 가능 | 단일 장비 확장 한계 |
| **확장성(Scalability)** | Sharding 지원 (Cluster) | Sharding 지원 | 완벽한 수평 확장(Masterless) | 주로 수직적 확장(Scale-up) |
| **일관성(Consistency)** | 강한 일관성 / 결과적 일관성 선택 가능 | 강한 일관성 (Primary-Secondary) | 튜너블(Tunable) 일관성 | ACID 지원 (트랜잭션) |
| **주요 병목** | 메모리 리소스 비용 | 대용량 데이터 수정(Update) | 컴팩션(Compaction) 시 부하 | 전체 그래프 스캔 |

#### 2. 타 과목 융합 관점 분석

**① 컴퓨터 구조와의 융합 (Architecture & I/O)**
- **SSD와 시계열(Column) DB**: Column-Family Store는 LSM-Tree를 사용하여 Random Write를 Sequential Write로 바꿉니다. 이는 **HDD의 회전 지연(Rotational Latency)**이나 **SSD의 쓰기 증폭(Write Amplification)** 문제를 완화하여 하드웨어 수명을 늘리고 성능을 높이는 융합 설계입니다.
- **메모리 계층 구조와 KV DB**: Redis와 같은 KV 스토어는 OS의 **Buddy System**이나 **Slab Allocation** 메커니즘을 사용하여 메모리 단편화를 최소화합니다. 데이터를 항상 **L1/L2 캐시**가 아닌 **DRAM**에 상주시켜 웹 서버의 **TPS**(Transactions Per Second)를 극대화합니다.

**② 네트워크와의 융합 (