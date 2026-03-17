+++
title = "293. 티아이디비 (TiDB) - 실시간 HTAP의 선두주자"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 293
+++

# 293. 티아이디비 (TiDB) - 실시간 HTAP의 선두주자

## # [TiDB (Titanium Database)]
### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **TiDB (Titanium Database)**는 MySQL Protocol과 100% 호환되며, **Compute-Storage Separation (컴퓨팅-스토리지 분리)** 아키텍처를 기반으로 무한 수평 확장이 가능한 오픈소스 **NewSQL** 데이터베이스이다.
> 2. **가치**: 행 기반 저장소(TiKV)와 열 기반 저장소(TiFlash)를 통해 **OLTP (Online Transaction Processing)**와 **OLAP (Online Analytical Processing)** 워크로드를 데이터 복제 없이 단일 클러스터에서 실시간으로 통합 처리(HTAP)한다.
> 3. **융합**: 분산 시스템 이론인 **Raft Consensus Algorithm (Raft 합의 알고리즘)**과 Google Spanner 기반의 분산 SQL 기술을 융합하여, 데이터 일관성을 유지하면서도 페타바이트 급 데이터 처리를 달성한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학
**TiDB (Titanium Database)**는 '장력과 내구성이 강한 티타늄'의 의미를 담아, 전통적인 RDBMS의 편의성과 NoSQL의 확장성을 동시에 확보한 **분산 관계형 데이터베이스管理系统 (Distributed Relational Database Management System)**이다. 기존 RDBMS가 수직적 확장(Scaling-up)의 한계에 부딪히고, NoSQL이 데이터 일관성 및 복잡한 쿼리 처리에 취약하다는 문제를 해결하기 위해 설계되었다. 핵심 철학은 '데이터베이스를 하나의 거대한 서버가 아닌, 무한히 확장 가능한 클러스터로 바라보는 것'이다.

### 💡 비유: 끊임없이 확장되는 '자가 조립식 레고 건물'
TiDB는 레고 블록으로 건물을 짓는 것과 같다. 더 큰 건물을 지어야 한다면(데이터 증가), 기둥(스토리지)만 추가로 꽂으면 되며, 건물의 입구(컴퓨팅)는 따로 분리되어 있어 사람이 몰려도 넓게 뚫어놓을 수 있다. 위에서 보면 하나의 건물이지만, 내부적으로는 수만 개의 블록이 힘을 합쳐 버티고 있는 구조다.

### 등장 배경
① **기존 RDBMS의 한계**: MySQL, Oracle 등은 데이터가 테라바이트(TB)를 넘어가면 쿼리 성능이 급격히 저하되거나, 비싼 하드웨어로 교체(Sharding)해야 하는 운영상의 고통이 존재했다.
② **NewSQL 패러다임의 등장**: Google Spanner(2012)와 Google F1이 증명한 것처럼, 분산 환경에서도 ACID 트랜잭션을 보장하며 SQL을 지원하는 기술적 가능성이 열렸다.
③ **실시간 데이터의 비즈니스 요구**: 데이터 웨어하우스(DW)로 데이터를 옮기는 배치 처리(Batch ETL) 방식은 데이터의 신선도가 떨어져, 현대의 실시간 의사결정(Real-time Analytics) 요구를 충족시킬 수 없게 되었다.

### 📢 섹션 요약 비유
TiDB는 **"단일 주방을 가진 거대 자동화 식당"**과 같습니다. 주방장(SQL Optimizer)이 주문(쿼리)을 받으면, 재료 보관 창고(Storage)가 여러 곳에 퍼져 있어도 이를 자동으로 수거해 요리합니다. 손님이 아무리 늘어나도 창고를 늘리면 되고, 주방장을 늘리면 대기열을 줄일 수 있어 확장이 자유롭습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (상세 표)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/기술 (Protocol) | 비유 (Analogy) |
| :--- | :--- | :--- | :--- | :--- |
| **TiDB Server** | **SQL Layer (Compute)** | Stateless하며 MySQL Protocol을 처리. Parser → Optimizer → Executor 과정을 거쳐 KV 키 생성 | MySQL Protocol / Golang | 주방장 (주문 받아서 지시) |
| **PD (Placement Driver)** | **Cluster Brain** | 클러스터 메타데이터 관리, TiKV 데이터 분배(Routing), 스케줄링 담당. etcd 기반(Raft) | HTTP / gRPC | 사령관 (지도 및 인력 배치) |
| **TiKV** | **Row-Oriented Storage** | Key-Value 형태(RocksDB 기반)로 데이터 저장. Raft Group을 통해 복제 및 일관성 유지 | Raft / gRPC | 창고 직원 (상자 단위 보관) |
| **TiFlash** | **Column-Oriented Storage** | TiKV 데이터를 실시간 복제하여 열 기반으로 변환. 분석 쿼리 가속 | Raft Learner / ClickHouse Engine | 통계 관리팀 (명세서 정리) |

### ASCII 구조 다이어그램: TiDB HTAP Logical Flow
아래는 사용자의 요청이 들어와서 처리되기까지의 계층별 데이터 흐름과 HTAP(Hybrid Transactional/Analytical Processing)의 분기 과정을 도식화한 것이다.

```text
+-----------------------------------------------------------------------+
|                          [ Client Application ]                       |
|                    (Standard MySQL Driver/Connector)                  |
+-------------------------------------+---------------------------------+
                                      | SQL Query
                                      v
+-----------------------------------------------------------------------+
|  1. TiDB Server Layer (SQL Processing & Smart Routing)                |
|  +-----------------+    +------------------+    +------------------+  |
|  | Parser & AST    | -> | Logical Planner  | -> | Physical Planner |  |
|  +--------+--------+    +--------+---------+    +--------+---------+  |
|           |                      |                       |            |
|           v                      v                       v            |
|  +---------------------------------------------------------------+    |
|  |         * TiDB Optimizer (Cost-based)                          |    |
|  |         1. Reads Statistics from PD                            |    |
|  |         2. Decides Execution Path (TP or AP path)              |    |
|  +---------------------------------------------------------------+    |
|           |                      ^                       |            |
+-----------|----------------------|-----------------------|------------+
            |                      |                       |
            | (Read Write)         | (Read Request)        | (Analytical)
            v                      |                       v
+-----------------------------------------------------------------------+
|  2. Storage Engine Cluster (Multi-model & High Availability)          |
|                                                                       |
|  [Group Replication: Region N] ------------------------------------>  |
|  +---------------------+    +---------------------+                   |
|  |  TiKV Store 1 (Leader) | -> |  TiKV Store 2 (Follower) | ... Raft Log|
|  |  (Row-based KV)     |    |  (Row-based KV)     |                   |
|  |  - RocksDB          |    |  - RocksDB          |                   |
|  +---------+-----------+    +---------------------+                   |
|            |                                                        |
|            | Raft Multi-Replication (Consensus)                      |
|            | (Strong Consistency Guarantee)                          |
|            v                                                        |
|  +---------------------+    +---------------------+                   |
|  |  TiKV Store 3       |    |  TiFlash Node 1     | (Columnar Copy)  |
|  |  (Row-based)        |    |  (Columnar)         |                   |
|  +---------------------+    |  - ClickHouse Engine|                   |
|                             +---------------------+                   |
|                                                                       |
+-----------------------------------------------------------------------+
            |                                ^
            | (Read Path)                     |
            +--------------------------------+
             Merged Result Set
```

#### 다이어그램 심층 해설
1.  **스마트 라우팅 (Smart Routing)**: 사용자가 SQL을 날리면 TiDB Server는 Optimizer를 통해 해당 쿼리의 성격을 판단한다.
    *   **Point Get/Insert (OLTP)**: 기본 키를 통한 단일 행 조회라면 TiKV로 직행한다.
    *   **Complex Aggregation (OLAP)**: 대량의 `SUM`, `GROUP BY` 쿼리라면 TiFlash로 라우팅하여 열 기반 스캔의 이점을 누리게 한다.
2.  **Raft Group의 확장**: TiKV와 TiFlash는 동일한 데이터를 보유하지만, 저장 형태가 다르다. TiKV는 Source of Truth(진실의 원천)로서 Raft Log를 통해 데이터를 TiFlash(Learner Role)로 동기화한다. 이 과정은 비동기적으로 이루어지지만 매우 빠르게 실시간성을 유지한다.
3.  **PD의 역할**: 각 노드의 상태를 모니터링하며, 데이터가 특정 노드에 치우치지 않도록 Region(데이터 조각, 약 96MB) 단위로 리밸런싱을 수행한다.

### 핵심 동작 메커니즘: 트랜잭션 및 데이터 분산
TiDB는 트랜잭션 처리를 위해 Google Percolator 모델을 기반으로 한 2단계 커밋(2-Phase Commit) 프로토콜을 사용한다.
1.  **Prewrite Phase**: 클라이언트가 데이터를 쓰면, TiKV는 잠금(Lock)을 획득하고 데이터를 메모리(RocksDB MemTable)에 기록한다. 이때 키의 버전을 `start_ts`(시작 타임스탬프)로 표기한다.
2.  **Commit Primary**: 기본 키(Primary Key)의 잠금을 해제하고 트랜잭션을 커밋한다.
3.  **Commit Secondaries**: 나머지 관련 키들의 잠금을 비동기적으로 해제한다.
이 메커니즘을 통해 분산 환경에서도 **ACID (Atomicity, Consistency, Isolation, Durability)** 속성을 엄격하게 준수한다.

### 핵심 코드 및 공식 (스케일 아웃 수식)
데이터 파티셔닝은 Range 기반으로 수행된다.
$$ K_{region} = \text{Hash}(Key) \pmod N \quad (\text{개념적 의사 코드, 실제는 Range Split}) $$
TiDB의 성능은 선형적으로 확장 가능하며, 이론적 처리량(TPS)은 다음과 같이 추정된다.
$$ Total\_TPS \approx \sum_{i=1}^{N} (TiKV\_Node\_Capacity_i \times Replication\_Factor\_Overhead) $$
*여기서 N은 노드의 개수이며, Raft 복제 오버헤드를 제외하면 노드 추가 시 성능이 직선적으로 상승한다.*

### 📢 섹션 요약 비유
TiDB의 아키텍처는 **"수천 대의 드론과 통신 시스템을 갖춘 물류 센터"**와 같습니다. 사령관(PD)이 드론(TiKV)의 위치와 배터리 상태를 실시간으로 파악하여 명령을 내리고, 주문 센터(TiDB Server)는 고객이 주문한 물건이 창고 어디에 있는지 즉시 파악하여 가장 가까운 드론에게 배차 명령을 내립니다. 또한, 모든 드론은 서로 통신(Raft)하여 어떤 드론이 추락하더라도 다른 드론이 물건을 대신 배송할 수 있도록 보장합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: TiDB vs. MySQL (Sharded)

| 비교 항목 (Criteria) | MySQL (Shared Storage / Vertical Scale) | MySQL (Sharded) | **TiDB (NewSQL / Shared Nothing)** |
|:---|:---|:---|:---|
| **확장성 (Scalability)** | 단일 서버 스펙에 종속됨 | 수동 샤딩 필요, 리밸런싱 어려움 | **자동 샤딩, 무한 수평 확장(Online DDL)** |
| **데이터 일관성 (Consistency)** | 강한 일관성 (Strong) | Cross-Shard 트랜잭션 보장 어려움 | **Global Strong Consistency (Raft)** |
| **고가용성 (Availability)** | Master-Slave (Failover 복잡) | 일부 샤드 장애 시 서비스 중단 가능 | **Auto Failover (Raft Leader Election)** |
| **분석 처리 (OLAP)** | 부하 발생 시 트랜잭션 저해 | 별도 DW 구축 필요 (ETL) | **HTAP (TiFlash 동시 활용)** |
| **운영 복잡도 (Ops)** | 단순함 | 매우 높음 (커넥션 라우팅, ID 생성 등) | **중간 (PD 자동화, K8s 친화적)** |

### 과목 융합 관점: OS/네트워크와의 시너지
1.  **운영체제(OS)와의 융합**:
    *   TiKV는 **RocksDB**를 사용하므로 OS의 I/O Scheduler와 파일 시스템(ext4, xfs) 설정에 매우 민감하다. 특히, 커널의 `Transparent Huge Pages (THP)`를 끄거나 `Swapiness`를 0으로 설정하는 등 OS 레벨의 튜닝이 분산 DB 성능에 직결된다.
2.  **네트워크와의 융합**:
    *   분산 환경이므로 노드 간 통신(Raft Replication) 지연이 성능을 좌우한다. 데이터 센터 간 **Cross-DC 배포** 시, 네트워크 파티션 발생에 대비한 Raft 멤버 배치 전략(예: Leader는 로컬, Follower는 원격)과 네트워크 대역폭 최적화가 필수적이다.

### 📢 섹션 요약 비유
기존 MySQL 샤딩은 **"물리적인 벽으로 나뉜 창고들을 사람이 직접 오가며 물건을 찾는 것"**과 같아서 관리가 어렵고 비효율적입니다. 반면 TiDB는 **"모든 창고가 디지털로 연결되어 로봇팔이 자동으로 물건을 전달하는 스마트 팩토리"**와 같습니다. 네트워크(도로)가 넓고 OS(바닥)가 단단해야 로봇팔(프로세스)이 더 빠르게 움직일 수 있는 상호 의존적인 관계입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오 및 의사결정 프로세스

#### 시나리오 A: 급성장하는 핀테크 서비스의 결제 시스템
*   **상황**: 사용자 수가 100만을 돌파하며, 단일 MySQL 인스턴스의 디스크 용량이 90%를 차지하고 커넥션 풀이 자주 고갈됨. 백업/복구 시간이 길어져 RTO(Recovery Time Objective) 위협.
*   **의사결정 1 (이관)**: MySQL 호환성이 100%이므로, 애플리케이션 코드 수정 없이 `mysqldump` 혹은 `DM (Data Migration)` 툴을 사용하여 TiDB로 전체 데이터를 이관.
*   **의