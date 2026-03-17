+++
title = "568. HDFS의 복제 및 고가용성 메커니즘"
date = "2026-03-14"
weight = 568
+++

# # [HDFS 복제 및 고가용성 메커니즘]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: HDFS (Hadoop Distributed File System)는 Commodity Hardware(범용 하드웨어)의 잦은 장애를 가정하여, 기본적으로 3-way Replication(3중 복제)과 Rack Awareness(랙 인식) 알고리즘을 통해 데이터 내구성을 물리적으로 보장한다.
> 2. **가치**: 단일 장애점(SPOF, Single Point of Failure)인 NameNode를 Active-Standby 구조로 이중화하여, RPO(Recovery Point Objective) ≒ 0, RTO(Recovery Time Objective) ≒ 수십 초 수준의 고가용성(HA, High Availability)을 달성하여 대규모 데이터 처리의 연속성을 확보한다.
> 3. **융합**: ZooKeeper를 활용한 분산 코디네이션과 QJM(Quorum Journal Manager) 기반의 메타데이터 동기화는 분산 시스템 설계에서의 CAP 정리(Consistency, Availability, Partition Tolerance) 간의 트레이드오프를 조정하는 정석적인 아키텍처 패턴을 보여준다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 정의**
HDFS (Hadoop Distributed File System)는 대용량 데이터를 저장하고 처리하기 위해 설계된 분산 파일 시스템이다. 그러나 기업용 스토리지인 SAN (Storage Area Network)이나 NAS (Network Attached Storage)와 달리, HDFS는 저렴한 Commodity Hardware(범용 하드웨어)의 집합체인 Cluster(클러스터) 위에서 구동된다. 이러한 환경에서는 하드디스크 장애, 네트워크 분할, 노드 전원 차단 등이 예외가 아닌 **일상적인 사건(Everyday Event)**으로 발생한다. 따라서 HDFS는 "Hardware Failure is the Norm"을 전제로 설계되었으며, 이를 극복하기 위해 데이터 자체를 복제하는 Data Replication(데이터 복제)과 시스템의 제어 탑인 NameNode의 고가용성(HA, High Availability)을 핵심 메커니즘으로 채택하고 있다.

**💡 비유**
HDFS의 철학은 "거대한 도서관을 건설할 때, 비싼 내화식 금고 대신 평범한 책장(노드)을 수십 개 놓고, 귀중한 책(데이터)을 여러 권 복사해 서로 다른 건물에 보관하는 관리 전략"과 같다. 화재가 나도 한 건물만 타면 책은 보존되는 원리다.

**등장 배경 (Background)**
1.  **기존 한계 (Legacy Limitation)**: 초기 Hadoop 1.0 시절에는 단일 NameNode 구조를 사용했다. 이로 인해 NameNode의 메모리 부족(OutOfMemoryError)이나 프로세스 장애 발생 시, 전체 클러스터가 단일 장애점(SPOF, Single Point of Failure)으로 인해 정지하는 치명적인 문제가 있었다. 또한, 유지보수를 위한 Planned Downtime조차 불가능하여 24/7 비즈니스 요구를 충족시키지 못했다.
2.  **혁신적 패러다임 (Paradigm Shift)**: Hadoop 2.0부터 Active NameNode와 Standby NameNode의 Hot Standby 구조가 도입되었다. 이는 ZooKeeper(ZK) 기반의 자동 장애 복구(Automatic Failover)를 통해 수동 복구의 불확실성을 제거하고 Zero Downtime에 가까운 가용성을 제공하는 혁신이었다.
3.  **현재의 비즈니스 요구 (Business Requirements)**: 데이터 양이 페타바이트(PB) 단위로 증가하고, AI/ML 학습용 데이터 레이크(Data Lake)로서의 역할이 중요해짐에 따라, 단순한 저장을 넘어 99.9999%의 가용성과 랙(Rack) 단위의 정전 사태에도 데이터 무손실을 보장하는 엔터프라이즈급 안정성이 필수가 되었다.

**📢 섹션 요약 비유**
HDFS의 신뢰성 설계는 **"천재지변에 대비해 중요한 보험 설계서를 3부 복사하여, 하나는 집 금고에, 하나는 사무실에, 하나는 지역 보험소에 맡겨두는 안전장치"**와 같다. 장소가 물리적으로 분리되어 있어 하나가 파괴되더라도 나머지를 통해 즉시 문서를 복구할 수 있다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

HDFS의 복제 및 고가용성 아키텍처는 크게 **데이터 레벨의 복구력(Data Plane Redundancy)**과 **메타데이터 레벨의 고가용성(Control Plane HA)**으로 나누어 볼 수 있다.

#### 1. 구성 요소 및 역할 (Component Table)

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Replication Monitor** | 복제 감시 및 관리자 | NameNode가 주기적으로 블록 상태를 스캔(Periodic Scan)하여, 손실된 블록이나 복제본이 부족한 언더-리플리케이션 블록을 감지하고 다른 DataNode로 복제를 명령함. | Block Report Protocol | 주문 제조 관리자 |
| **Rack Awareness Algorithm** | 물리적 배치 전략 수립 | 클라이언트의 IP 트리(Topology Script)를 참조하여 노드의 랙(Rack) 위치를 파악. 쓰기 시 복제본을 서로 다른 랙에 분산 배치하여 랙 단위 장애에 대비함. | Network Topology Script | 지리학자/도시 계획가 |
| **QJM (Quorum Journal Manager)** | 메타데이터 동기화 엔진 | Active NameNode의 Edits 로그를 JournalNode 클러스터(홀수 개)에 다수결 원칙(Majority Vote)으로 기록하여, Standby NameNode가 이를 읽고 메모리 상태를 동기화함. | TCP / RPC | 공식 회의록 작성자 |
| **ZKFC (ZK Failover Controller)** | 건강 상태 모니터링 및 선출 | NameNode의 헬스체크(Heartbeat)를 수행하고, 장애 발생 시 ZooKeeper에게 리더 선출을 요청하여 Failover를 트리거함. | RPC / ZAB Protocol | 개인 비서 및 집달리 |
| **ZooKeeper (ZK)** | 분산 코디네이터 (조정자) | 클러스터의 락(Lock)을 관리하고, 오직 하나의 Active 노드만 존재하도록 보장하는 분산 락 서비스를 제공. | ZAB (ZooKeeper Atomic Broadcast) | 투표 관리 위원회 |
| **DataNode** | 블록 저장소 실행 | 실제 블록 데이터를 디스크에 저장하며, NameNode에게 주기적으로 생존 신호(Heartbeat)와 블록 리포트(Block Report)를 전송함. | Data Transfer Protocol | 창고지기 |

#### 2. 랙 인식(Rack Awareness) 배치 구조도

HDFS는 기본적으로 3개의 복제본(Replica)을 생성하며, 네트워크 대역폭과 데이터 안전성의 균형을 맞추기 위해 지능적인 배치 전략을 따른다. 이 과정은 클라이언트의 쓰기 요청 시 파이프라인(Pipeline)을 형성하며 진행된다.

```text
      [ Data Flow & Placement Strategy ]

                Client (Writer)
                     │
                     ▼ (Write Request)
      ┌───────────────────────────────────────────────────┐
      │  Cluster Topology        [ Network Switch ]      │
      ├───────────────────────────────────────────────────┤
      │  (1) Local Placement                             │
      │      Data is written to Node 1 (Local Node)      │
      │                               │                  │
      │  [ Rack 1 ]         ┌───────────────────────┐    │
      │  ┌─────────────┐    │  Node 1 (DataNode)    │    │
      │  │ Switch A    │    │  ┌─────────────────┐  │    │
      │  └──────┬──────┘    │  │ Block Replica 1 │◀─┼────┘ (Ack)
      │         │           │  └─────────────────┘  │
      │  ┌──────┴──────┐    └───────────────────────┘    │
      │  │  Node 2     │                              │
      │  │ (Backup)    │<───┐                         │
      │  └─────────────┘    │                         │
      │                     │ (Replica Stream)        │
      ├─────────────────────┼─────────────────────────┤
      │  [ Rack 2 ]         │                         │
      │  ┌─────────────┐    │    │  Pipeline Flow     │
      │  │ Switch B    │    │    │      (2)           │
      │  └──────┬──────┘    │    ▼                    │
      │  ┌──────┴──────┐    └───────────────────────┐ │
      │  │  Node 3     │    │  Node 3 (DataNode)    │ │
      │  │ ┌────────┐  │    │  ┌─────────────────┐  │ │
      │  │ │Replica│  │    │  │ Block Replica 2 │  │ │
      │  │ │  2    │  │    │  └─────────────────┘  │ │
      │  │ └────────┘  │    └───────────────────────┘ │
      │  └─────────────┘                              │
      │  ┌─────────────┐    └───────────────────────┐ │
      │  │  Node 4     │    │  Node 4 (DataNode)    │ │
      │  │ ┌────────┐  │    │  ┌─────────────────┐  │ │
      │  │ │Replica│  │    │  │ Block Replica 3 │  │ │
      │  │ │  3    │  │    │  └─────────────────┘  │ │
      │  │ └────────┘  │    └─────────────────────┘ │
      │  └─────────────┘                               │
      └───────────────────────────────────────────────────┘
```

**(해설: Write Pipeline)**
1.  **Replica 1 (Local Rack)**: 클라이언트는 가장 가까운 노드(혹은 자신이 속한 랙)에 첫 번째 복제본을 쓴다. 이는 쓰기 지연시간(Latency)을 최소화하기 위함이다.
2.  **Replica 2 (Remote Rack)**: DataNode 1은 다른 랙(Rack 2)에 있는 DataNode 3으로 데이터를 전달한다. 이는 "랙 단위 정전"이나 스위치 장애에 대비한 핵심 전략이다.
3.  **Replica 3 (Remote Rack, Same Node)**: DataNode 3은 같은 랙(Rack 2) 내의 다른 노드(DataNode 4)에 마지막 복제본을 전달한다. 이는 복제본 2와 3 사이의 네트워크 트래픽이 랙 간 링크(Cross-Rack Link)를 거치지 않도록 하여 비용을 절감한다.

#### 3. 고가용성(HA) 메커니즘 상세

**심층 동작 원리 (Deep Dive)**
HDFS HA는 **"메타데이터 동기화"**와 **"자동 장애 복구(Automatic Failover)"** 두 가지 축으로 작동한다.

1.  **메타데이터 동기화 (Metadata Sync via QJM)**:
    -   기존 Secondary NameNode 방식(주기적 Checkpoint)은 데이터 유실 가능성이 있었다. HA 환경에서는 Active NameNode가 네임스페이스 변경(Edits Log)을 발생시킬 때마다, QJM을 통해 JournalNode 클러스터(보통 3대, 5대)에 실시간으로 기록한다.
    -   Standby NameNode는 JournalNode들로부터 Edits Log를 읽어 자신의 메모리(Namespace)에 적용한다. 이 과정에서 Standby는 항상 Active와 거의 동일한 상태를 유지하며, Checkpoint도 주기적으로 수행하여 FSImage 파일을 생성한다.
    -   JournalNode 클러스터는 과반수(Majority)가 기록 성공을 응답해야 커밋되므로, 일관성(Consistency)을 강력하게 보장한다.

2.  **장애 감지 및 전환 (Failover via ZKFC & ZK)**:
    -   각 NameNode에는 ZKFC (ZooKeeper Failover Controller)라는 데몬이 붙어 있다.
    -   ZKFC는 ZooKeeper와 세션을 유지하며 주기적으로 Health Monitor를 통해 자신의 NameNode 상태를 점검한다.
    -   Active NameNode 장애(Heartbeat 실패 등)가 감지되면, 해당 ZKFC는 세션을 잃고, Standby 측 ZKFC가 ZooKeeper의 잠금(Lock)을 획득하려 시도한다.
    -   잠금을 획득하면 Standby가 Active 상태로 전환(Promote)된다.

#### 4. 핵심 알고리즘: Fencing (안전 확보)

Fencing은 이전 Active 노드가 여전히 살아있어 데이터를 쓰거나 수정하려는 **Split-brain(뇌 분할)** 현상을 방지하기 위해, 가장 최근에 선출된 노드만이 시스템을 제어하도록 보장하는 절차다.

```python
# Pseudo-code for Fencing Logic in HA Failover
def promote_to_active(new_active_nn, shared_storage_jns):
    # 1. Claim Leader Lock in ZooKeeper
    # 분산 락을 획득하여 시스템의 유일한 제어자임을 선포
    if not acquire_zk_lock("/hadoop-ha/nameservice1"):
        raise Exception("Another node is already Active or Locked")

    # 2. Fence previous Active (Ensure it cannot write)
    # 이전 Active가 쓰기 못하게 강제로 제거
    # Method A: Revoke write access to JournalNodes (Epoch Numbering)
    prev_active_epoch = get_current_epoch(shared_storage_jns)
    if not fence_journal_nodes(prev_active_epoch, new_active_nn):
        # Method B: Force kill if graceful fencing fails (SSH Fencing)
        force_ssh_kill(previous_active_nn_ip)

    # 3. Load latest state from JournalNodes
    # 최신 메타데이터를 로드하여 메모리 상태 복구
    load_edits_and_fsimage(new_active_nn)

    # 4. Start serving requests
    # 서비스 포트 오픈 및 클라이언트 요청 처리 시작
    start_rpc_server(new_active_nn)
```

**📢 섹션 요약 비유**
HDFS의 고가용성 아키텍처는 **"기장(Active)과 부기장(Standby)이 동일한 비행 계획서(Journal)를 실시간 공유하며 비행하는 여객기"**와 같다. 기장이 쓰러지면 즉시 부기장이 조종간을 잡으며, 이때 관제탑(ZooKeeper)은 쓰러진 기장이 다시 깨어나더라도 조