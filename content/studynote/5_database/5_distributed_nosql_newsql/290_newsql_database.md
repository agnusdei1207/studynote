+++
title = "290. NewSQL - RDBMS의 신뢰와 NoSQL의 확장을 융합하다"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 290
+++

# 290. NewSQL - RDBMS의 신뢰와 NoSQL의 확장을 융합하다

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NewSQL은 전통적인 **RDBMS (Relational Database Management System)**의 **ACID (Atomicity, Consistency, Isolation, Durability)** 속성과 SQL 호환성을 유지하며, NoSQL의 수평적 확장성을 구현하는 차세대 분산 데이터베이스 아키텍처이다.
> 2. **가치**: "일관성과 확장성은 trade-off 관계"라는 CAP 정리의 딜레마를 기술적 혁신(Consensus Protocol, Clock Sync 등)으로 극복하여, 금융권 등 높은 무결성이 요구되는 대규모 서비스에서 **Zero RTO (Recovery Time Objective)**와 **High TPS (Transactions Per Second)**를 동시에 달성한다.
> 3. **융합**: **Google Spanner**의 **TrueTime API**와 **Raft** 알고리즘을 기점으로, **CockroachDB**, **TiDB** 등 클라우드 네이티브 환경에 최적화된 오픈소스 기술이 폭발적으로 성장하고 있으며, **HTAP (Hybrid Transactional/Analytical Processing)** 구현의 핵심 기반으로 자리 잡았다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 1. 개념 및 철학
NewSQL은 기존 RDBMS가 가진 확장성의 한계(Scale-up 비용 상승, Sharding의 복잡성)와 NoSQL이 가진 데이터 일관성 및 트랜잭션 처리의 한계를 동시에 해결하고자 등장했다. 핵심은 "관계형 모델의 편리함을 포기하지 않으면서, 내부적으로는 완전히 새로운 분산 커널을 설계"하는 것이다. 이는 단순히 기존 RDBMS 위에 분산 캐시를 얹는 것이 아니라, 디스크 데이터 구조(B-Tree vs LSM-Tree), 네트워크 통신, 병행 제어(Control Concurrency) 전반을 재설계한 접근법이다.

#### 2. 💡 비유: 기존 방식의 한계
*   **RDBMS**는 거대한 단일 건물(스카이스크래퍼)을 짓는 것과 같다. 더 많은 사람(데이터)을 수용하려면 건물을 허물고 더 큰 건물을 지어야 하며(Scale-up), 이에는 물리적/시간적 한계가 있다.
*   **NoSQL**은 수많은 작은 텐트를 치는 것과 같다. 확장은 쉽지만, 텐트 간에 정보를 즉시 공유하거나 중앙 통제(트랜잭션)를 하는 것은 불가능에 가깝다.

#### 3. 등장 배경 및 변천
① **기존 한계**: 인터넷 서비스의 폭발적 성장으로 단일 서버(Shared-disk/Shared-everything) 아키텍처로는 처리 불가능한 수준의 트래픽 발생.
② **패러다임 전환**: 2000년대 중반 NoSQL의 등장으로 확장성은 해결되었으나, 데이터 정합성이 중요한 핀테크, 광고, 결제 시스템에서의 활용 제약 발생.
③ **현재 요구**: 클라우드 환경에서 자동 장애 복구와 지리적 분산을 기본으로 제공하는 **Cloud-Native Database**의 필요성 대두.

#### 4. 📢 섹션 요약 비유
> **NewSQL은 '하이패스가 설치된 초고속 열차'와 같습니다.** 기존 기차(RDBMS)는 안전하지만 느리고 선로를 깔기 비싸며, 텐트(NoSQL)는 빠르지만 짐을 잃어버릴 위험이 있습니다. NewSQL은 수많은 열차 칸을 분산 배치하면서도, 신호 시스템(Consensus)을 통해 마치 하나의 거대한 기차처럼 정확하고 안전하게, 그러나 매우 빠르게 데이터를 운반하는 시스템입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

NewSQL의 핵심은 **Storage Engine**의 분리와 **Consensus Algorithm(합의 알고리즘)**의 적용, 그리고 **Global Transaction Management**에 있다.

#### 1. 구성 요소 및 역할

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **State Machine Replication** | 데이터 복제 및 다중화 | 리더(Leader) 노드가 쓰기 요청을 로그(Log)로 기록하고 팔로워(Follower)에게 전파 | Raft / Paxos | 회의록 작성 및 투표 |
| **Distributed SQL Layer** | 질의 처리 및 최적화 | 사용자 SQL을 파싱하여 각 노드의 Partition으로 라우팅, 병렬 처리 계획 수립 | PostgreSQL Protocol | 교통 통제 센터 |
| **Key-Value Storage Engine** | 디스크 상 영구 저장 | 복잡한 Locking을 제거하고 MVCC(Multi-Version Concurrency Control)를 적용하여 Row-level 잠금 수행 | LSM-Tree / Bw-Tree | 고속화물 컨테이너 |
| **Global Transaction Manager** | 분산 트랜잭션 코디네이터 | 여러 노드에 걸친 트랜잭션의 원자성을 보장하기 위해 2단계 커밋(2PC)을 합의 알고리즘 위에 구현 | Distributed 2PC | 국제 결제 중계 시스템 |
| **Time Sync Service** | 전역 순서 보장 | 물리적 시계와 논리적 시계를 혼합하여 데이터 버전의 절대적 순서 부여 | TrueTime / HLC | 세계 표준시 atomic clock |

#### 2. 아키텍처: 계층별 분산 처리 흐름

NewSQL은 크게 **Stateless한 Compute Layer**와 **Stateful한 Storage Layer**로 나뉜다.

```text
[Client Request]
      │
      ▼
┌───────────────────────────────────────────────────────────────┐
│  [Stateless SQL Router / Compute Node]                        │
│  - Parsing, Optimization, Plan Execution                      │
│  - 일반적인 애플리케이션 서버처럼 수평 확장(Scale-out) 가능    │
└───────────────────────────────────────────────────────────────┘
      │  │  │
      │  └──┴─────▶ [ 1. Read Request ] ──▶ Distributed KV Store
      │
      ▼
┌───────────────────────────────────────────────────────────────┐
│  [Transaction Layer (Consensus Module)]                       │
│  - 쓰기 요청(WAL)을 Raft Log에 기록                           │
│  - 과반수 노드의 승인이 필요(Quorum Read/Write)               │
└───────────────────────────────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────────────────────────────┐
│  [Replication Group (Raft Group)]                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
│  │  Node 1 │  │  Node 2 │  │  Node 3 │  (Range-Based Sharding)│
│  │(Leader) │  │(Follower)│  │(Follower)│                      │
│  └────┬────┘  └────┬────┘  └────┬────┘                      │
│       │            │            │                            │
│       └────────────┴────────────┘                            │
│          Log Replication (Disk Sync)                          │
└───────────────────────────────────────────────────────────────┘
```

*   **도입 서술**: 위 다이어그램은 사용자의 쿼리가 SQL 레이어를 통해 해석된 후, 분산 합의 계층(Raft)을 거쳐 실제 데이터가 저장소에 샤딩(Sharding)되어 저장되는 과정을 보여줍니다. 핵심은 중앙의 트랜잭션 계층이 데이터의 파편화를 사용자에게 투명하게(Transparent하게) 만든다는 점입니다.

*   **해설**:
    1.  **Routing**: 클라이언트는 어느 노드에 접속해도 되지만, 보통 Smart Client나 Proxy가 해당 데이터가 소속된 파티션(Partition)의 리더 노드로 요청을 포워딩합니다.
    2.  **Consensus**: 쓰기 연산은 단순히 디스크에 쓰는 것이 아니라, Raft Group의 과반수(N/2 + 1)에게 로그 복제가 완료되어야 'Commit'됩니다. 이 과정에서 네트워크 분단 시에도 데이터 안전성이 보장됩니다.
    3.  **Sharding**: 테이블은 Primary Key를 기준으로 Range(범위)나 Hash 방식으로 쪼개져 각 Replication Group에 할당됩니다.

#### 3. 핵심 알고리즘: Raft 합의와 분산 트랜잭션

NewSQL의 신뢰성은 **Raft (Replicated and Fault-Tolerant)** 알고리즘에 기초한다.

*   **Leader Election**: 리더가 다운되면 임시 타임아웃(Timeout) 후 팔로워들이 투표를 통해 새 리더를 선출. 데이터 정합성을 위해 오직 리더만 쓰기를 허용.
*   **Log Replication**:
    1.  Leader: `AppendEntries` RPC 호출.
    2.  Follower: 로그 저장 후 성공 응답.
    3.  Leader: 과반수 응답 시 `Commit Index` 갱신 및 클라이언트에 응답.
*   **Concurrency Control**: 기존 RDBMS의 비용 높은 Lock 대신, **MVCC (Multi-Version Concurrency Control)**를 사용하여 읽기 작업은 최신 스냅샷을 읽고 쓰기 작업은 버전을 생성하여 충돌을 최소화합니다.

```sql
-- 의사코드: MVCC를 통한 Non-blocking Read
BEGIN TRANSACTION;
-- 시스템은 현재 트랜잭션 ID(Timestamp)보다 이전의 Committed 버전만 읽음
SELECT balance FROM accounts WHERE user_id = 1; 
-- (다른 트랜잭션이 해당 row를 쓰고 있더라도 Lock을 기다릴 필요 없음)
```

#### 4. 📢 섹션 요약 비유
> **NewSQL의 아키텍처는 '편의점 전산망'과 같습니다.** 본사(Cloud)에서는 모든 점포의 데이터를 실시간으로 동기화하지만, 각 점포(Node)는 독립적으로 매출을 처리하고 본사 서버(Leader)에만 보고합니다. 만약 본사 서버가 고장 나면 지역 대리점(Leader Candidate)이 즉시 본사 역할을 대체하여 매장 장애(Failover)가 발생하지 않도록 설계된 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 심층 기술 비교: RDBMS vs NoSQL vs NewSQL

| 구분 | Legacy RDBMS (MySQL/Oracle) | NoSQL (MongoDB/Cassandra) | NewSQL (CockroachDB/Spanner) |
|:---|:---|:---|:---|
| **일관성 모델** | 강한 일관성 (Strong) | 결과적 일관성 (Eventual) | 강한 일관성 (Strong) / Global |
| **확장성 (Scalability)** | 수직 확장 (Scale-up) | 수평 확장 (Scale-out) | 수평 확장 (Scale-out) |
| **트랜잭션 (Transaction)** | 단일 노드 ACID 지원 | 단일 Document/Key ACID | 분산 ACID (Global Serializability) |
| **데이터 스키마** | 정형 (Schema-on-write) | 비정형 (Schema-less) | 정형 (Relational) |
| **Sharding (샤딩)** | 애플리케이션 레벨 구현 필요 | Auto Sharding 지원 | 투명한 Auto Sharding |
| **장애 복구 (Failover)** | 수동 복구 또는 복잡한 클러스터링 | 빠르나 데이터 유실 가능성 | 자동 리더 선출, Zero RPO/RTO |

#### 2. 과목 융합 관점: OS/네트워크와의 시너지
*   **OS와의 연관 (Clock Synchronization)**:
    *   분산 트랜잭션에서 발생하는 쓰기 충돌(WW-conflict)을 해결하기 위해 NewSQL은 **HLC (Hybrid Logical Clock)**와 같은 고정밀 시간 동기화 기술을 사용합니다. 이는 OS 커널의 시간 관리자(Time Keeper)와 하드웨어의 NTP(Network Time Protocol) 클라이언트를 결합하여, 논리적 시계(Counter)와 물리적 시계의 괴리를 줄이는 기술입니다.
*   **네트워크와의 연관 (RPC Latency)**:
    *   분산 합의 과정에서 네트워크 왕복 시간(RTT: Round Trip Time)이 곧 지연시간(Latency)이 됩니다. 따라서 NewSQL은 데이터 센터 내부(WAN)뿐만 아니라 글로벌 환경에서도 동작하도록 **Paxos** 기반의 비동기 복제 로그를 최적화합니다.

#### 3. 📢 섹션 요약 비유
> **RDBMS는 '기차', NoSQL은 '자동차', NewSQL은 '플레인'입니다.** 기차(RDBMS)는 정확하지만 선로가 깔린 곳으로만 다니고, 자동차(NoSQL)는 어디든 갈 수 있지만 교통체증(데이터 정합성)에 취약합니다. NewSQL은 비행기처럼 전 세계 어디나 빠르게 이동하면서도, 정확한 시간에 도착해야 하는 스케줄(일관성)을 철저히 지키는 항공 관제 시스템을 탑재한 혁신적인 교통수단입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

#### 1. 실무 시나리오 및 의사결정 매트릭스
NewSQL 도입은 기술적 장점만으로 결정해서는 안 되며, 비즈니스 임계점(Tipping Point)을 고려해야 한다.

*   **Case A: 핀테크 결제 시스템 (금융권)**
    *   **상황**: 초당 10,000건 이상의 결제 요청, 중복 결제 0% 허용, 24시간 서비스.
    *   **Decision**: **NewSQL (TiDB, CockroachDB) 도입 필수**.
    *   **이유**: NoSQL을 쓰면 잔액 업데이트의 결과적 일관성 때문에 '잔고 부족'인데 결제가 성공하는 이중 지급 위험이 발생. RDBMS는 단일 서버로 처리량 한계 도달. NewSQL은 샤딩을 자동으로 처리하고 ACID를 보장하므로 유일한 해결책.

*