+++
title = "305. 오라클 RAC (Real Application Clusters) - 공유 디스크의 결집"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 305
+++

# 305. 오라클 RAC (Real Application Clusters) - 공유 디스크의 결집

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오라클 RAC는 여러 노드의 **인스턴스(Instance)**가 단일 **공유 디스크(Shared Disk)**를 동시에 액세스하여 데이터베이스를 운영하는 **'Active-Active' 클러스터링** 아키텍처이다.
> 2. **가치**: 하드웨어 장애 발생 시 서비스 중단(TPO: Time to Production)을 최소화하는 고가용성(HA, High Availability)과, 노드 추가를 통한 선형적 성능 확장(Scale-Up/Out)을 동시에 달성한다.
> 3. **융합**: **캐시 퓨전(Cache Fusion)** 기술을 통해 디스크 I/O 병목을 제거하고, **글로벌 캐시 서비스(GCS, Global Cache Service)** 및 **글로벌 인큐 서비스(GES, Global Enqueue Service)**로 분산 환경의 데이터 정합성을 ACID 수준으로 보장한다.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 철학**
오라클 RAC는 단일 서버의 한계를 넘어서기 위해 고안된 엔터프라이즈 데이터베이스 클러스터링 솔루션이다. 기존의 **'Active-Standby(대기-운영)'** 방식이 대기 서버의 자원 낭비를 초래하는 반면, RAC는 **'Active-Active'** 방식을 통해 모든 노드가 실시간으로 트랜잭션을 처리한다. 이를 위해 여러 인스턴스가 동일한 데이터 파일, 컨트롤 파일, 리두 로그를 공유하며, 각 노드의 버퍼 캐시(Between Buffer Cache) 간 데이터 동기화를 위한 고유의 통신 계층을 운영한다.

**💡 비유: 거대한 공유 주방**
여러 명의 셰프(인스턴스)가 하나의 거대한 냉장고와 조리대(공유 디스크)를 동시에 사용하여 요리를 완성하는 상황과 같다.

**등장 배경 및 패러다임**
1.  **기존 한계**: SMP(Symmetric Multi-Processing) 방식의 단일 서버는 CPU 확장에 물리적 한계가 있으며, 단일 장애점(SPOF, Single Point of Failure)으로 인해 장애 시 서비스가 완전히 중단되었다.
2.  **혁신적 패러다임**: **'Shared-Disk(공유 디스크)'** 모델을 도입하여 데이터를 분할(Sharding)하지 않고도 여러 서버가 병렬 처리가 가능해졌다. 특히, 노드 간 데이터 전송 시 느린 디스크 I/O 대신 고속 네트워크를 통한 메모리 전송을 가능하게 한 **'Cache Fusion'**이 게임 체인저였다.
3.  **비즈니스 요구**: 24/365 무중단 서비스가 필수적인 금융, 통신, 대형 커머스 환경에서 플랫폼 장애로 인한 다운타임(Downtime) 비용을 Zero에 가깝게 만들어야 하는 필연적인 요구에 의해 발전했다.

```text
[ Architecture Paradigm Shift ]

  Traditional SMP               Oracle RAC (Shared Disk)
  ┌───────────────┐            ┌──────┐  ┌──────┐  ┌──────┐
  │    Server     │            │Node 1│  │Node 2│  │Node 3│
  │ (CPU + Mem)   │            │Active│  │Active│  │Active│
  └───────┬───────┘            └───┬──┘  └───┬──┘  └───┬──┘
          │                        │       │        │
      [SPOF Risk]               (Interconnect - Private Network)
          │                        │       │        │
      ▼   ▼                    ▼   ▼       ▼        ▼
  ┌───────────────────┐    ┌─────────────────────────────┐
  │   Storage (Local)  │    │      Shared Storage         │
  └───────────────────┘    │ (Single Source of Truth)     │
                           └─────────────────────────────┘
```
*도해: SMP의 단일 장애점(SPOF) 위험과 달리, RAC는 다중 노드가 단일 스토리지를 공유하여 고가용성과 확장성을 동시에 확보함.*

**📢 섹션 요약 비유**
마치 고속도로 톨게이트에서 하나의 요금소(데이터베이스)를 운영하되, 여러 차선(노드)을 동시에 개방하여 차량(트랜잭션)을 처리하고, 특정 차선이 막혀도 다른 차선으로 원활하게 우회시키는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**구성 요소 상세 분석**
RAC의 안정성과 성능은 클러스터웨어(Clusterware) 계층과 데이터베이스 계층의 유기적인 결합에 달려있다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/특징 | 비유 |
|:---|:---|:---|:---|:---|
| **Clusterware** (Cluster Ready Services) | 노드 관리 및 장애 감시 | 각 노드의 하트비트(Heartbeat)를 모니터링하여 Split-Brain 방지 및 VIP 관리 | CSS/CRS/EVM | 시스템 운영자 |
| **Interconnect** | 노드 간 고속 통신망 | Cache Fusion을 위한 데이터 블록 전송 및 메시징 | UDP (High-speed), Infiniband | 전용 택배 도로 |
| **Shared Disk** | 데이터 저장소 | 모든 노드가 접근 가능한 스토리지 (ASM, NFS 등) | ASM ACFS, Raw Device | 공유 창고 |
| **SGA (System Global Area)** | 버퍼 캐시 공유 | 로컬 버퍼 캐시와 원격 버퍼 캐시(GES/GCS 관리)를 통합 관리 | Memory to Memory | 작업대 |
| **Voting Disk** | 쿼럼(Quorum) 관리 | 과반수(Majority) 노드만 생존 시 클러스터 유지 판단 | File/Block | 안전표 |

**핵심 기술: Cache Fusion (캐시 퓨전) 메커니즘**
RAC의 성능을 결정짓는 가장 중요한 기술이다. 기존 클러스터 방식(Shared Disk)에서는 노드 A가 수정한 데이터 블록을 디스크에 기록(Flush)해야만 노드 B가 읽을 수 있어 디스크 I/O 병목이 발생했다. **Cache Fusion**은 데이터를 디스크로 내리지 않고, Interconnect를 통해 노드 A의 메모리 버퍼에서 노드 B의 메모리 버퍼로 직접 전송하는 방식이다. 이 과정은 **GCS (Global Cache Service)**에 의해 제어되며, 데이터 락(Lock)의 상태를 관리하기 위해 **GES (Global Enqueue Service)**가 협력한다.

```text
[ Cache Fusion Data Flow ]

   Node A (Requestor)          Node B (Holder)          Shared Disk
   ┌─────────────────┐         ┌─────────────────┐      ┌──────────────┐
   │  Buffer Cache   │         │  Buffer Cache   │      │  Data Files  │
   │                 │         │                 │      │              │
   │   (Need Data)   │────────▶│  (Has Block X)  │      │              │
   └─────────────────┘  ① Req  └─────────────────┘      └──────────────┘
          │                      │    │
          │                      │    │ ③ Direct Transfer
          │   ② Grant Lock       │    │   (Block X via Interconnect)
          │ ◀────────────────────┘    │
          ▼                          ▼
   [Consistent Read]           [Write Intent Log]
   
   *Old Way (No Fusion): Node B writes to Disk → Node A reads from Disk
   *RAC Way (Fusion):   Node B sends to Node A (Zero-Copy) via Private Net
```
*도해: 디스크를 거치지 않는 고속 메모리 간 전송이 어떻게 지연 시간(Latency)을 줄이는지 보여줌.*

**심층 동작 원리: Split-Brain Resolution (스플릿 브레인 방지)**
네트워크 분단 등으로 인해 노드 간 통신이 두절되었을 때, 각 노드가 스스로 클러스터의 주인이라고 생각하여 데이터를 충돌시키는 현상을 방지해야 한다. 이를 위해 **Voting Disk**를 사용한다.
1.  각 노드는 하트비트를 주고받다가 장애 발생 시 Voting Disk에 접근을 시도한다.
2.  과반수(Majority)의 표를 얻은 그룹만이 생존(Survivor)하고, 소수는 강제로 재부팅(Eviction)되어 데이터 분산을 방지한다. 이를 **I/O Fencing**이라고 한다.

```text
[ Split-Brain Prevention Logic ]

   Situation: Network Partition between Node 1, 2 and Node 3
   
   [ Sub-Cluster A ]       [ Sub-Cluster B ]
   Node 1  ◀──✂───▶  Node 3
   Node 2                 (Isolated)
   
   Voting Disk (The Judge)
   ┌───────────────────────┐
   │ 1. Node 1: Vote YES   │
   │ 2. Node 2: Vote YES   │
   │ 3. Node 3: Vote NO    │
   └───────────────────────┘
   
   Result: Node 1 & 2 (2/3 Majority) → STAY (DB Service Up)
           Node 3 (1/3 Minority)    → REBOOT (Suicide to prevent corruption)
```

**핵심 알고리즘: GCS Resource Control (수식적 표현)**
데이터 블록의 일관성은 아래와 같은 락 모드(Lock Mode) 승격 및 변환(Convert) 과정을 통해 관리된다. 
- **N (Null)**: 로컬 버퍼 캐시에 없음
- **S (Shared)**: 읽기 권한 보유 (다수 노드 S 가능)
- **X (Exclusive)**: 쓰기 권한 보유 (단일 노드만 X 가능)

> $State_{Block} = \{Node, Mode, SCN\}$
> Where $Mode \in \{N, S, X\}$ and $SCN$ ensures transaction ordering.

```sql
-- Simplified Logic for Cache Fusion Request
-- Node A requests Block X in 'Exclusive' mode
IF Node_B.Has_Block(X, Mode='S') THEN
    SEND_REQUEST(Node_B, 'CONVERT', X, 'S->X');
    -- Node B flushes relevant redo, sends block to A
    RECEIVE_BLOCK(Node_A, X);
    COMMIT_MODE(Node_A, X, 'X');
END IF;
```

**📢 섹션 요약 비유**
팀 프로젝트를 하는 도중 서류(데이터)가 필요할 때, 서버컴퓨터(공유 디스크)에 올렸다가 내려받는 게 아니라, 옆자리 팀원(노드)이 USB나 메신저(Interconnect)로 화면을 바로 공유해주는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

**심층 기술 비교: RAC vs Replication (Data Guard)**
오라클 엔터프라이즈 환경에서 고가용성을 위한 두 가지 주요 전략을 비교한다.

| 구분 | Oracle RAC (Real Application Clusters) | Oracle Data Guard (Replication) |
|:---|:---|:---|
| **아키텍처** | **Active-Active** (모든 노드가 Read/Write 가능) | **Active-Passive** (대기 사이트는 대기 중) |
| **데이터 복제 방식** | **Shared Disk** (단일 데이터 소스) | **Storage Replication** (물리적 복제본) |
| **장애 복구 시간** | **Near-Zero** (초 단위, 세션 유지 가능) | **Fast** (분~십분 단위, Failover 필요) |
| **거리 제약** | 짧음 (동일 데이터센터, 고속 LAN 필요) | 김 (원격 데이터센터, WAN 가능) |
| **주요 용도** | **성능 확장** (Scalability) + HA | **재해 복구** (Disaster Recovery) |

**과목 융합 관점: OS와 네트워크의 상관관계**
1.  **OS/컴퓨터 구조 융합**: RAC는 OS의 **IPC (Inter-Process Communication)** 메커니즘을 넘어서 노드 간 통신을 해야 한다. 이를 위해 **UDP** 프로토콜을 기반으로 한 오버헤드가 적은 통신을 사용하며, CPU의 **NUMA (Non-Uniform Memory Access)** 아키텍처를 고려하여 메모리 로컬리티를 최적화해야 한다. Context Switching 비용을 줄이는 Dedicated Server Process 모델이 필수적이다.
2.  **네트워크 융합**: Interconnect는 지연 시간(Latency)이 극도로 낮아야 한다. 패킷 손실 시 TCP 재전송보다는 빠른 **UDP** 기반 RAC 프로토콜이 선호되며, 네트워크 대역폭이 병목이 되지 않도록 **Jumbo Frame (MTU 9000)** 설정이 권장된다.

```text
[ Network Architecture for RAC ]

   Client Side                   Data Center Side
   
   [User] ───▶ [VIP (Virtual IP)] ───▶ [Public Network (Eth0)]
                    │                      (User Traffic)
                    ▼
              [Service Load Balancer]
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   [Node 1: Public IP]    [Node 2: Public IP]
        │                       │
        └───────┬───────────────┘
                ▼
   [Private Network (Interconnect)]
        (Cache Fusion Traffic - UDP/High-Speed)
        │                       │
   [Node 1: Priv IP]       [Node 2: Priv IP]
        │                       │
        └───────────┬───────────┘
                    ▼
            [Shared Storage (SAN/NAS)]
```
*도해: 사용자 트래픽과 노드 간 동기화 트래픽이 물리적으로 분리된 네트워크를 통해 병목을 방지함.*

**📢 섹션 요약 비유**
RAC는 여러 명이 같은 화이트보드에 같이 그림을 그리는 '협업 작업'이고, Data Guard는 같은 그림을 똑같이 복사해서 멀리 있는 다른 사무실에 보관해두는 '보험'과 같습니다. 목적(확장 vs 보존)이 다릅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**실무 시나리오 및 의사결정**
1.  **상황: 급증하는 트래픽 처리 (TPS 5,000 → 15,000)**
    *   **분석**: 단일 서버의 CPU가