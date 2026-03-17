+++
title = "272. 멀티 마스터(Multi-Master) 복제 - 무한 확장의 양날의 검"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 272
+++

# 272. 멀티 마스터(Multi-Master) 복제 - 무한 확장의 양날의 검

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **Multi-Master Replication (멀티 마스터 복제)**은 분산 데이터베이스 환경에서 **모든 노드가 Master(주인)**의 역할을 수행하여 읽기(Read)와 쓰기(Write) 연산을 동시에 처리하고, 변경 데이터를 상호 간에 복제하는 **대칭형(Symmetric) 아키텍처**입니다.
> 2. **가치**: 특정 데이터 센터나 리전(Region)에 쓰기 연산이 집중되는 병목을 제거하여 **글로벌 규모의 쓰기 처리량(Write Throughput)**을 극대화하며, 임의의 노드 장애 시에도 데이터 손실 없이 즉각적인 **Failover (장애 조치)**가 가능한 고가용성(HA)을 제공합니다.
> 3. **융합**: 분산 환경의 고유한 데이터 불일치 현상인 **Update Conflict (갱신 충돌)**을 해결하기 위해 **Vector Clock (벡터 시계)**, **LWW (Last Write Wins)**, **Quorum (쿼럼)** 같은 정교한 합의 및 충돌 해결 알고리즘이 요구되며, 이는 분산 시스템 설계의 난이도를 높이는 핵심 요소가 됩니다.

+++

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의**
전통적인 **Replication (복제)** 기법인 Master-Slave(주-종) 구조에서는 쓰기가 가능한 노드가 Master 하나로 제한됩니다. 이에 반해, **Multi-Master Replication (MMR)**은 분산된 클러스터 내의 **모든 노드를 Primary(주 노드)**로 승격시킨 아키텍처입니다. 클라이언트는 어느 노드에든 데이터를 쓸 수 있으며, 각 노드는 트랜잭션을 로그(Log) 형태로 저장하여 다른 피어(Peer) 노드들에게 전파(Propagate)합니다. 이는 데이터베이스 관점에서 **Active-Active (액티브-액티브)** 구조로 정의되며, **Partition Tolerance (분할 내성)**과 **Availability (가용성)**을 최우선으로 하는 **CAP 정리**의 A와 P를 선택한 결과물입니다.

**2. 등장 배경 및 필연성**
- **기존 한계**: 단일 마스터 구조에서는 지리적으로 분산된 글로벌 서비스(예: 미국, 유럽, 아시아 사용자)의 경우, 아시아 사용자가 미국에 위치한 마스터 DB에 데이터를 쓸 때 발생하는 **Network Latency (네트워크 지연)**이 필연적입니다. 이는 쓰기 성능 저하와 직결됩니다.
- **패러다임 전환**: 모든 지역에 마스터를 두어 지역 내부에서 쓰기를 즉시 완료(WAN Latency 제거)하고, 백그라운드에서 노드 간 데이터를 동기화함으로써 **쓰기 성능의 무한 확장**을 꾀합니다.
- **비즈니스 요구**: 24/7 서비스 중단이 허용되지 않는 핀테크, 커머스 등의 분야에서 **Zero RTO (Recovery Time Objective, 복구 시간 목표)**를 달성하기 위한 필수 기술로 자리 잡았습니다.

**💡 비유**
이는 **'화이트보드 회의'**와 같습니다. 누구나(모든 노드) 보드의 어느 곳이든 내용을 추가할 수 있으며, 모든 참가자는 서로의 내용을 실시간으로 보고 베껴적습니다. 회의가 끝나면 모든 보드의 내용이 동일해야 하죠.

> **📢 섹션 요약 비유**: 멀티 마스터 복제는 **'팀 프로젝트의 공유 문서(Google Docs)'**와 같습니다. 누구나(모든 노드) 문서를 수정할 수 있고, 수정 내용이 실시간으로 모든 팀원에게 공유되지만, 두 사람이 동시에 같은 문장을 고치면 충돌(Conflict)이 발생하여 해결이 필요합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 동작**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Peer Node (피어 노드)** | 모든 노드가 Master 역할 수행 | 로컬 트랜잭션 처리 및 원격 트랜잭션 수용 | MySQL Group Replication | 회의 참여자 |
| **Replication Log (복제 로그)** | 변경 내용을 기록하는 저장소 | WAL (Write-Ahead Log) 기반의 순차적 기록 | Binlog, Write-Ahead Log | 회의록 |
| **Conflict Detection (충돌 감지)** | 동시성 수정 감지 | Primary Key, Timestamp, Vector Clock 비교 | Vector Clock, Version Vector | 겹치는 발언 체크 |
| **Conflict Resolution (충돌 해결)** | 충돌 시 최종 데이터 선택 | LWW, Semantic Merge, Quorum Vote | CRDT (Conflict-free Replicated Data Types) | 토론 후 결론 도출 |
| **Change Data Capture (CDC)** | 데이터 변경 사항 추출 및 전송 | 로그 스트리밍을 통한 이벤트 발행 | Kafka, Debezium | 배달부 |

**2. 핵심 아키텍처: 데이터 동기화 및 흐름**

아래 다이어그램은 클라이언트가 서로 다른 리전의 노드에 쓰기를 수행하고, 이가 다른 노드로 복제되는 과정입니다.

```text
   [Region Asia]                      [Region US]
      Client A                          Client B
         │                                  │
         │ 1. Write (A=100)                 │ 3. Write (A=150) [Conflict Context]
         ▼                                  ▼
┌────────────────┐                 ┌────────────────┐
│   Node A       │                 │   Node B       │
│   (Master)     │                 │   (Master)     │
│ ┌────────────┐ │                 │ ┌────────────┐ │
│ │ Local DB   │ │   2. Replicate  │ │ Local DB   │ │
│ │ (A=100)    │ ├────────────────> │ │ (A=150)    │ │
│ └────────────┘ │   (Log Shipping) │ └────────────┘ │
│ ▲              │ <────────────────│              │ │
│ │ 5. Merge     │   4. Replicate   │ │ 6. Resolve  │ │
│ │ (A=150/LWW)  │                 │ │ (Conflict)  │ │
└────────────────┘                 └────────────────┘
```
*(해설: ① 클라이언트 A가 아시아 노드에 A 값을 100으로 변경. ② 이 변경 사항은 미국 노드로 비동기 복제됨. ③ 그 사이 클라이언트 B가 미국 노드에 A 값을 150으로 변경. ④ 이 변경 사항은 아시아 노드로 복제됨. ⑤ 아시아 노드는 A=100을 가진 상태에서 A=150 업데이트를 수신. ⑥ 충돌 해소 로직(예: 최신 시간 승인)에 따라 최종 값 150을 확정.)*

**3. 심층 동작 원리: 충돌 해결 메커니즘 (Deep Dive)**
Multi-Master의 가장 큰 기술적 난제는 **Write Skew (쓰기 왜곡)**와 **Conflict Resolution (충돌 해결)**입니다.
1.  **비동기 복제 (Asynchronous Replication)**: 노드 간 데이터 동기화를 위해 즉시적인 합의(2PC 등)를 사용하면 쓰기 지연이 발생합니다. 따라서 대부분의 MMR은 '일단 쓰고 나중에 복제'하는 비동기 방식을 사용합니다.
2.  **충돌 감지 (Detection)**: **Primary Key (기본 키)**가 다른 노드에서 동시에 업데이트되었을 때를 감지합니다. 이때 단순 타임스탬프만으로는 판단이 어렵기 때문에, **Vector Clock (벡터 시계)**을 사용하여 "이벤트의 논리적 순서"를 파악합니다.
3.  **충돌 해소 (Resolution)**:
    *   **LWW (Last Write Wins)**: 타임스탬프가 가장 큰 트랜잭션을 승자로 선정. 가장 구현이 쉽지만 데이터 손실 가능성이 있음.
    *   **Application Level Merge**: '장바구니 합치기' 등 비즈니스 로직 단계에서 데이터를 통합.

**4. 핵심 알고리즘 및 코드 (Pseudo-code)**
아래는 **Vector Clock**을 활용한 버전 충돌 확인 로직의 예시입니다.

```python
# Pseudo-code: Conflict Detection using Vector Clock
class DataItem:
    def __init__(self, value, vector_clock):
        self.value = value
        self.vector_clock = vector_clock # {'NodeA': 1, 'NodeB': 2}

def resolve_conflict(local_item, remote_item):
    """
    로컬 데이터와 원격 수신 데이터의 충돌을 판단하고 해결함.
    """
    local_vc = local_item.vector_clock
    remote_vc = remote_item.vector_clock
    
    # 1. Check Causality (인과관계 확인)
    # if local_vc happened before remote_vc
    if all(local_vc[k] <= remote_vc.get(k, 0) for k in local_vc):
        return remote_item # Remote wins (안전한 병합)
    
    # 2. Check Reverse Causality
    if all(remote_vc[k] <= local_vc.get(k, 0) for k in remote_vc):
        return local_item # Local wins (안전한 병합)
        
    # 3. Concurrent Update (동시 갱신 -> CONFLICT!!)
    # 실무에서는 여기서 LWW(타임스탬프 비교) 또는 예외 처리 발생
    print("⚠️ CONFLICT DETECTED: Manual Merge or LWW required")
    
    # LWW Logic Example
    if remote_item.timestamp > local_item.timestamp:
        return remote_item
    else:
        return local_item
```

> **📢 섹션 요약 비유**: 충돌 해결 메커니즘은 **'팀원들과 같은 엑셀 파일을 동시에 편집할 때의 버전 관리'**와 같습니다. A 팀원이 10번째 줄을, B 팀원이 10번째 줄을 동시에 수정했다면, 나중에 저장한 사람의 내용이 덮어씌워지거나(LWW), 두 내용을 강제로 합치는(Manual Merge) 과정이 필요합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Single-Master vs. Multi-Master**

| 비교 항목 | Single-Master (Active-Standby) | **Multi-Master (Active-Active)** |
|:---|:---|:---|
| **쓰기 확장성 (Write Scalability)** | 낮음 (Master 1대의 리소스에 종속) | **높음 (모든 노드가 처리 가능)** |
| **데이터 일관성 (Consistency)** | **강한 일관성 (Strong Consistency)** 가능 | **결과적 일관성 (Eventual Consistency)** |
| **복잡도 (Complexity)** | 상대적으로 낮음 (Failover Logic만 필요) | **매우 높음 (Conflict Resolution 필수)** |
| **장애 조치 (Failover)** | 승격(Promotion) 시간 필요 (RTO 발생) | **Zero RTO (즉시 전환 가능)** |
| **충돌 (Conflict)** | 발생하지 않음 | **반드시 발생 (핵심 과제)** |

**2. 성능 및 비용 분석 (Quantitative Metrics)**
- **TPS (Transactions Per Second)**: 노드가 N개일 때, 이론적 최대 쓰기 TPS는 $N \times \text{SingleNode\_TPS}$에 근접할 수 있으나, **Conflict Resolution (충돌 해결)** 및 **Replication Traffic (복제 트래픽)** 오버헤드로 인해 실제 효율은 약 60~80% 수준인 경우가 많음.
- **Latency (지연 시간)**: 로컬 리전 사용자는 DB에 직접 접속하므로 Network Latency가 거의 없으나(1ms 이내), **Global Read** 시 데이터 동기화 지연(GC Lag)으로 인해 최신 데이터를 즉시 읽지 못할 수 있음.

**3. 타 영역(네트워크/OS)과의 융합 시너지 및 오버헤드**
- **네트워크 융합**: **WAN (Wide Area Network)** 환경에서는 노드 간 **Packet Loss**나 **Jitter**가 발생할 수 있습니다. 이를 해결하기 위해 **TCP Keepalive** 조정 및 **Application-level Acknowledgment**가 필수적입니다. 또한, 데이터 동기화 트래픽이 폭주하여 사용자 트래픽을 방해하지 않도록 **QoS (Quality of Service)** 정책을 통해 복제 트래픽 대역폭을 제어해야 합니다.
- **OS 융합**: 고속 복제를 위해 OS 커널 레벨의 **Zero-Copy (sendfile)** 기능을 적극 활용하여 로그 전송 시 CPU 부하를 줄여야 합니다.

> **📢 섹션 요약 비유**: Single-Master는 **'모두가 대기하는 하나의 팩스기'**이고, Multi-Master는 **'모두에게 보이는 메신저 단체 채팅방'**입니다. 팩스기는 한 번에 하나씩 보내야 해서 느리지만 순서가 명확하고, 채팅방은 동시에 다양한 말이 쏟아져서(R/W) 빠르지만 무슨 말이 먼저 나왔는지 헷갈릴 수(Conflict) 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 프로세스**

- **시나리오 A: 글로벌 이커머스 플랫폼 확장**
    - **문제**: 미국 본사 DB에 유럽/아시아 사용자의 주문(쓰기)이 몰리며 지연 발생. 미국 센터 장애 시 전 서비스 장애.
    - **의사결정**: **Multi-Master Replication** 도입. 리전별로 마스터 DB 구축.
    - **전략**: '재고 감소'와 같은 중요 데이터는 **Optimistic Locking (낙관적 잠금)**을 통해 충돌 시 트랜잭션을 거부(Rollback)하여 정합성을 보장하고, '장바구니' 같은 유연한 데이터는 **Last-Writer-Wins**로 우선 처리.

- **시나리오 B: 24시간 운영되는 핀테크 시스템**
    - **문제**: 정기 점검(RTO) 없이 이중화 구성을 유지해야 함.
    - **의사결정**: Active-Active 구성을 통해 데이터 센터 단위 재해(Disaster)에 대비.
    -