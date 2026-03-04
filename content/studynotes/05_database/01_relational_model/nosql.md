+++
title = "NoSQL (Not Only SQL)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# NoSQL (Not Only SQL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 관계형 데이터베이스(RDBMS)의 엄격한 스키마와 수직적 확장(Scale-up)의 한계를 극복하고, 빅데이터의 3V(Volume, Velocity, Variety)를 수용하기 위해 설계된 분산형 비정형 데이터 저장 기술입니다.
> 2. **가치**: CAP 이론(Consistency, Availability, Partition Tolerance)을 바탕으로 가용성과 수평적 확장성(Scale-out)을 극대화하며, 고정되지 않은 스키마를 통해 비즈니스의 민첩한 변화에 즉각 대응할 수 있는 데이터 기반을 제공합니다.
> 3. **융합**: 클라우드 네이티브 아키텍처, 마이크로서비스(MSA)의 폴리글랏 퍼시스턴스(Polyglot Persistence), 그리고 실시간 데이터 스트리밍(Kafka, Flink) 분석 환경의 핵심 저장소 역할을 수행합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**NoSQL**은 단순히 "SQL이 없다"는 의미가 아니라 "Not Only SQL"의 약자로, 전통적인 관계형 데이터 모델과 SQL 인터페이스를 넘어 다양한 데이터 저장 형식을 지원하는 데이터베이스 기술군을 총칭합니다. 관계형 데이터베이스가 데이터의 '정합성(Consistency)'과 '구조화(Normalization)'에 집중한다면, NoSQL은 분산 환경에서의 '확장성(Scalability)'과 '유연성(Flexibility)'에 초점을 맞춥니다.

#### 2. 💡 비유를 통한 이해
NoSQL은 **'거대한 창고와 가변형 수납 박스'**에 비유할 수 있습니다.
- **RDBMS**: 칸막이가 딱딱 나누어진 '약통'과 같습니다. 정해진 칸(스키마)에 정해진 약(데이터)만 넣어야 하며, 칸을 늘리려면 약통 전체를 새로 사야 합니다(Scale-up).
- **NoSQL**: 크기가 제각각인 물건을 아무렇게나 담을 수 있는 '오픈형 수납 박스'입니다. 박스가 부족하면 옆에 똑같은 박스를 하나 더 사다 놓으면 그만입니다(Scale-out). 내용물이 장난감이든, 책이든, 옷이든 상관없이 빠르게 담고 뺄 수 있습니다.

#### 3. 등장 배경 및 발전 과정
1.  **기존 기술의 치명적 한계**: 2000년대 초반, 구글과 아마존 같은 웹 자이언트들은 폭발적인 트래픽 성장에 직면했습니다. RDBMS는 데이터가 늘어날수록 성능이 급격히 저하되었고, 여러 서버에 데이터를 나누어 저장하기 위한 샤딩(Sharding) 구현이 매우 복잡하고 관리 비용이 높았습니다.
2.  **혁신적 패러다임의 도입 (CAP의 출현)**: Eric Brewer의 CAP 이론은 "분산 시스템에서 일관성, 가용성, 단절 내성을 모두 만족시킬 수 없다"는 것을 증명했습니다. 이에 따라 일관성을 조금 양보하더라도 가용성을 극대화하는 **BASE(Basically Available, Soft state, Eventually consistent)** 철학이 등장하며 NoSQL의 전성기가 시작되었습니다.
3.  **데이터의 비정형화**: 소셜 미디어, 로그 데이터, 센서 데이터 등 미리 정의된 테이블 구조에 넣기 힘든 데이터가 전체의 80% 이상을 차지하게 되면서, 유연한 스키마를 가진 NoSQL의 필요성이 강제되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. NoSQL 데이터 모델 분류 (표)

| 모델 분류 | 주요 특징 | 내부 동작 메커니즘 | 대표 솔루션 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Key-Value** | 가장 단순한 형태, 속도 최우선 | 해시 테이블(Hash Table) 기반 데이터 접근 | Redis, Riak | 사물함 번호키 |
| **Document** | JSON/BSON 형태의 유연한 저장 | 스키마-리스(Schema-less), 계층 구조 표현 | MongoDB, CouchDB | 라벨이 붙은 서류 봉투 |
| **Column-Family** | 대량의 컬럼과 압축에 최적화 | Sparse Matrix 저장, 컬럼 기반 I/O | Cassandra, HBase | 항목별 요약 장부 |
| **Graph** | 데이터 간의 관계(Node, Edge) 추적 | 인접 리스트(Adjacency List), Traversal | Neo4j, JanusGraph | 인맥 지도 |

#### 2. 분산 아키텍처 및 데이터 일관성 메커니즘 (ASCII 다이어그램)

```text
<<< Leaderless Distributed Cluster (Cassandra Style) >>>

       [ Client Request ]
             |
             v (Coordinate Node)
    +--------+--------+
    |       Node A    | <--- Write (Quorum R+W > N)
    +--------+--------+
    /        |        \
[Replica 1] [Replica 2] [Replica 3]
  Node B      Node C      Node D

<<< Data Partitioning: Consistent Hashing >>>

       0 |---------| 2^32-1
         |    *    |  <-- Hash(Key1) -> Node B
         |  *      |  <-- Hash(Key2) -> Node C
         |      *  |  <-- Hash(Key3) -> Node D
         |   *     |  <-- Hash(Key4) -> Node B (Ring structure)

[ 메커니즘 해설 ]
1. Consistent Hashing: 노드 추가/제거 시 데이터 재배치(Re-balancing)를 최소화하는 해싱 알고리즘.
2. Quorum Consensus: N개 복제본 중 W개 성공 시 쓰기 완료, R개 읽기 시 최신성 보장 (R+W > N 공식).
3. Hinted Handoff: 노드 다운 시 임시로 다른 노드에 데이터를 저장했다가 복구 시 전달하는 고가용성 기술.
4. Read Repair: 읽기 시 복제본 간 데이터 불일치를 발견하면 최신 버전으로 자동 복구.
```

#### 3. 심층 동작 원리: LSM-Tree (Log-Structured Merge-Tree)
많은 NoSQL(Cassandra, HBase, RocksDB)이 쓰기 성능 극대화를 위해 LSM-Tree 구조를 사용합니다.
1.  **쓰기 단계 (Memory-First)**:
    - 데이터가 들어오면 먼저 **Commit Log**에 순차 기록(Durability)하고, 메모리상의 **MemTable**에 정렬하여 저장합니다.
    - 임계치에 도달하면 MemTable을 디스크의 **SSTable(Sorted String Table)** 파일로 플러시(Flush)합니다. 이 과정은 순차 쓰기(Sequential Write)이므로 매우 빠릅니다.
2.  **읽기 및 정리 단계 (Merge & Compact)**:
    - 읽기 시에는 MemTable과 여러 SSTable들을 조회합니다. (Bloom Filter를 사용하여 불필요한 파일 조회 방지)
    - 백그라운드에서 **Compaction** 프로세스가 실행되어 여러 SSTable을 병합(Merge)하고 중복/삭제된 데이터를 정리하여 읽기 효율을 높입니다.

#### 4. 실무 수준의 구현 예시 (MongoDB Aggregation)
```javascript
// 복잡한 비정형 데이터 분석을 위한 Aggregation Pipeline 예시
db.orders.aggregate([
  // 1. 특정 기간 내 주문 필터링 (Index 활용)
  { $match: { order_date: { $gte: ISODate("2024-01-01") } } },
  
  // 2. 주문 상품 배열을 개별 문서로 분리
  { $unwind: "$items" },
  
  // 3. 상품 카테고리별 매출 합산 및 평균 계산
  { 
    $group: { 
      _id: "$items.category", 
      total_sales: { $sum: { $multiply: ["$items.price", "$items.quantity"] } },
      avg_quantity: { $avg: "$items.quantity" }
    } 
  },
  
  // 4. 매출액 순으로 정렬
  { $sort: { total_sales: -1 } },
  
  // 5. 상위 10개 카테고리만 결과로 출력
  { $limit: 10 }
]);
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. CAP 이론에 따른 NoSQL 분류 심층 비교

| 유형 | 집중 목표 | 주요 특징 | 해당 NoSQL | 실무 시나리오 |
| :--- | :--- | :--- | :--- | :--- |
| **CP** | 일관성(C) + 단절 내성(P) | 모든 노드가 최신 데이터를 가질 때까지 응답 지연 가능 | MongoDB, Redis, HBase | 금융 거래, 재고 관리 |
| **AP** | 가용성(A) + 단절 내성(P) | 일부 데이터가 구버전일지라도 언제나 응답 보장 | Cassandra, DynamoDB, Riak | SNS 피드, 장바구니, 로그 수집 |
| **CA** | 일관성(C) + 가용성(A) | 분산 환경이 아닌 단일 노드 DB의 특성 (네트워크 분절 시 장애) | 전통적 RDBMS (MariaDB 등) | 소규모 로컬 애플리케이션 |

#### 2. 과목 융합 관점 분석 (OS & 네트워크)
- **메모리 맵 파일(MMap)**: MongoDB 등은 OS의 Virtual Memory 관리 기법인 mmap을 활용하여 디스크 I/O를 OS에 위임합니다. 이는 OS 레벨의 페이지 캐시 효율을 극대화하는 전략입니다.
- **가십 프로토콜(Gossip Protocol)**: 마스터가 없는 NoSQL 클러스터(Cassandra)는 노드 간 상태 정보를 네트워크를 통해 주기적으로 교환하여 장애를 탐지하고 멤버십을 관리합니다. 이는 분산 네트워크 알고리즘의 실무 적용 사례입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 1: 이커머스 실시간 주문 폭주**
  - 상황: 블랙 프라이데이 이벤트로 RDBMS의 쓰기 지연 발생.
  - 전략: 주문 데이터는 RDBMS에 유지하되, 상품 조회 및 실시간 랭킹은 **Redis(Key-Value)**를 캐시로 도입하고, 장바구니나 상세 정보는 **MongoDB(Document)**로 분산하여 부하를 격리합니다 (폴리글랏 퍼시스턴스).
- **시나리오 2: 전 세계 멀티 리전 서비스 구축**
  - 상황: 미국, 유럽, 아시아에서 동일한 데이터를 지연 시간 없이 접근해야 함.
  - 전략: 복제(Replication) 지연을 감수하더라도 **Eventual Consistency** 모델을 지원하는 **Cassandra**를 선택하여, 각 리전에서 로컬 읽기/쓰기가 가능하도록 아키텍처를 설계합니다.

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **데이터 모델링 역량**: NoSQL은 '쿼리 중심 모델링'이 필수입니다. 조인(Join)이 불가능하므로 미리 결과를 합쳐두는 역정규화(Denormalization) 전략을 수립했는가?
- [ ] **일관성 수준 선택**: 비즈니스 로직에서 '최종 일관성'을 수용할 수 있는가? 아니면 반드시 Quorum 설정이 필요한가?
- [ ] **운영 복잡도**: 분산 클러스터의 백업, 노드 추가 시 리밸런싱, 모니터링 체계가 구축되어 있는가?

#### 3. 안티패턴 (Anti-patterns)
- **RDBMS처럼 사용하기**: NoSQL에서 무리하게 복잡한 조인을 애플리케이션 레벨에서 구현하거나, 모든 데이터를 하나의 문서에 때려 넣는 'God Document' 패턴은 성능의 재앙을 불러옵니다.
- **부적절한 샤드 키(Shard Key) 선택**: 특정 노드에만 데이터가 몰리는 'Hotspot' 현상을 유발하여 클러스터 전체 성능을 저하시킵니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- **정량적**: 데이터 처리 용량(TPS) 10배 이상 향상, 하드웨어 비용(Scale-out 대비 Scale-up 비용) 40% 이상 절감.
- **정성적**: 스키마 변경 시 다운타임 제거로 서비스 배포 속도(Time-to-Market) 가속화.

#### 2. 미래 전망
NoSQL은 이제 RDBMS와 대립하는 관계가 아닌, 서로의 장점을 흡수하는 **멀티 모델 데이터베이스(Multi-model DB)**로 진화하고 있습니다. 예를 들어, PostgreSQL은 JSON 처리를 강화하고, MongoDB는 다중 문서 ACID 트랜잭션을 지원하기 시작했습니다. 또한, 구글 스패너(Spanner)와 같은 **NewSQL**은 NoSQL의 확장성과 RDBMS의 ACID를 동시에 잡으려 하고 있습니다.

#### 3. 참고 표준/가이드
- **BASE**: 가용성과 상태 변화를 중시하는 분산 데이터베이스 이론.
- **ISO/IEC JTC 1/SC 32**: 데이터 관리 및 교환 관련 국제 표준화 기구의 동향 참고.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[CAP 이론](@/studynotes/05_database/01_relational_model/nosql.md)**: NoSQL 설계의 근간이 되는 분산 시스템의 3요소 트레이드오프.
- **[샤딩(Sharding)](@/studynotes/05_database/01_relational_model/nosql.md)**: 데이터를 여러 서버에 분산하여 수평적 확장을 구현하는 기술.
- **[폴리글랏 퍼시스턴스(Polyglot Persistence)](@/studynotes/05_database/01_relational_model/nosql.md)**: 용도에 맞는 다양한 DB를 혼합하여 사용하는 아키텍처 전략.
- **[Eventual Consistency](@/studynotes/05_database/01_relational_model/nosql.md)**: 분산 환경에서 시간이 지나면 결국 모든 노드의 데이터가 일치하게 되는 모델.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **레고 상자**: RDBMS가 모양마다 칸이 정해진 통이라면, NoSQL은 아무 모양이나 마구 담을 수 있는 큰 상자 같아요. (유연성)
2. **동네 편의점**: 손님이 많아지면 편의점 건물을 으리으리하게 짓는 대신, 동네마다 편의점을 여러 개 만드는 것과 같아요. (수평 확장)
3. **친구들과의 소문**: 친구 한 명에게 비밀을 말하면, 시간이 좀 지나야 모든 친구가 그 소문을 알게 되는 것과 비슷해요. (최종 일관성)
