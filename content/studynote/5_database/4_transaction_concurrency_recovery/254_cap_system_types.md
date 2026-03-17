+++
title = "254. CP vs AP vs CA 시스템 - 분산 데이터베이스의 성격"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 254
+++

# 254. CP vs AP vs CA 시스템 - 분산 데이터베이스의 성격

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **CAP 정리 (CAP Theorem)**에 따라 분산 시스템은 일관성, 가용성, 분단 허용성(P) 중 최대 두 가지까지만 보장할 수 있으며, 이 trade-off에 따라 시스템의 아키텍처가 결정된다.
> 2. **가치**: CP 시스템은 RTO(복구 시간 목표) 0에 가까운 데이터 무결성을, AP 시스템은 99.999% 이상의 고가용성을 제공하며, 도메인의 비즈니스 임계치(Criticality)에 따른 기술적 의사결정을 가능하게 한다.
> 3. **융합**: 분산 컴퓨팅 이론과 클라우드 네이티브 아키텍처의 접점이며, 최근에는 **NewSQL**을 통해 C와 A를 동시에 만족시키려는 하이브리드 시도로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 정의
**CAP 정리 (Consistency, Availability, Partition Tolerance Theorem)**는 2000년 Eric Brewer教授가 제안하고 2002년 Seth Gilbert 및 Nancy Lynch에 의해 증명된 분산 시스템의 이론적 기초입니다.

- **C (Consistency, 일관성)**: 분산 시스템 내 모든 노드가 동일한 시점에 동일한 데이터를 반환해야 하는 속성. **Atomic Consistency (원자적 일관성)** 또는 **Linearizability (선형성)**라고도 합니다.
- **A (Availability, 가용성)**: 클러스터 내 일부 노드에 장애가 발생하더라도, 시스템 전체가 계속해서 응답을 반환하여 항상 서비스가 가능해야 하는 속성. **High Availability (HA)**와 연결됩니다.
- **P (Partition Tolerance, 분단 허용성)**: 노드 간 통신망이 두절되거나(Partition), 메시지 유실/지연이 발생해도 시스템이 무너지지 않고 동작해야 하는 속성. 분산 시스템에서 물리적 네트워크 장애는 필연(Bubble)이므로, 실제 분산 환경에서는 P는 선택이 아닌 필수 사항으로 간주됩니다.

#### 등장 배경 및 필연성
과거의 단일 서버(Mainframe) 환경에서는 네트워크 분단(P)을 고려할 필요가 없었으나, 클라우드 컴퓨팅과 ** hyperscale (초대형) 아키텍처**로 넘어오면서 수천 대의 서버가 네트워크로 연결되었습니다. 이 과정에서 '네트워크는 신뢰할 수 있다'는 가정이 깨졌고, **Fallacies of Distributed Computing (분산 컴퓨팅의 오류)** 중 하나인 "네트워크는 신뢰할 수 있다"는 믿음이 버려지게 되었습니다. 따라서 현대의 분산 데이터베이스는 P를 기본 전제로 하며, 장애 상황에서 C와 A 중 무엇을 희생할 것인가에 철학을 두게 되었습니다.

```text
[ CAP 정리의 기하학적 구조 ]

         ▲ C (Consistency)
        ╱ ╲
       ╱   ╲  (선형성 보장: 모든 노드가 같은 값 반환)
      ╱     ╲
     ╱───────╲
    ╱ P       ╲ A
   ╱(분단 허용) ╲ (가용성 보장: 항상 응답)
  ╱             ╲
──────────────────────────────▶
(P는 분산 시스템의 상수(Constant)이므로,
 결국 C와 A 사이의 Trade-off로 귀결됨)
```

> **해설**: 상기 도해는 CAP 정리의 속성을 삼각형의 꼭짓점으로 표현한 것입니다. 분산 시스템에서 네트워크 분단(P)은 물리적 사실이므로 선택의 여지가 없습니다. 따라서 설계자는 분단 발생 시, 데이터 정합성을 지켜내기 위해 서비스를 중단(C)할 것인가, 아니면 오래된 데이터를 제공하더라도 서비스를 계속(A)할 것인가의 기로에 섭니다.

#### 📢 섹션 요약 비유
이는 **'복구 훈련 중인 소방관'**과 같습니다. 화재(네트워크 분단) 발생 시, 모든 소방관이 통신선(C)을 유지하며 안전을 확보하려 일을 멈추느냐(CP), 아니면 통신이 끊겨도 각자 현장에 뛰어들어 목숨을 구하느냐(AP)의 선택과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 구성 요소 및 상세 비교
분산 시스템의 성격을 결정하는 핵심 모듈과 그 동작 방식은 다음과 같습니다.

| 구성 요소 | CP 시스템 (Consistency) | AP 시스템 (Availability) | CA 시스템 (Single Node) |
|:---|:---|:---|:---|
| **핵심 철학** | **Safety First (안전성 최우선)** | **Liveness First (생존성 최우선)** | **Ideal World (이상적 세계)** |
| **분단(P) 발생 시** | 쓰기/읽기 거부 또는 타임아웃 | 장애 노드 제외 후 **Stale Data (부실 데이터)** 반환 | 시스템 다운 또는 Split Brain |
| **복제 전략** | **Synchronous Replication (동기식 복제)** | **Asynchronous Replication (비동기식 복제)** | N/A (단일 저장소) |
| **데이터 정합성** | Strong Consistency (강한 일관성) | Eventual Consistency (최종 일관성) | ACID 보장 |
| **대표 솔루션** | HBase, MongoDB (Safe Mode), etcd, Consul | Cassandra, DynamoDB, CouchDB, Riak | RDBMS (Standalone), Redis Sentinel |

#### CP 시스템: 동기식 복제와 커밋 프로토콜
CP 시스템은 쓰기 요청이 발생했을 때, 과반수의 노드(Majority Quorum) 또는 리더 노드의 확인을 받기 전까지 응답을 주지 않습니다.

```text
[ CP System: Synchronous Write Flow ]

   Client
      │
      │ ① Write Request (Data X = 10)
      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Leader (Master Node)                     │
│  │                                                         │
│  │ ② Propagate Write & Lock                               │
│  ├───────────────┬───────────────┐                        │
│  ▼               ▼               ▼                        │
│ Follower 1     Follower 2     Follower 3                  │
│ (ACK)         (ACK)          (NO ACK / Net Fail)          │
│                                                          │
│ ③ Quorum Check: (2/3) < 50%? ──▶ [WAIT] or [FAIL]      │
└─────────────────────────────────────────────────────────────┘
      │
      │ ④ Return "Error/Timeout" to Client
      ▼
   Client (Service Blocked)
```

> **해설**:
> 1. **도입**: CP 시스템은 데이터의 신뢰성을 위해 **Raft** 또는 **Paxos**와 같은 합의 알고리즘을 사용합니다.
> 2. **다이어그램**: 위 도표는 네트워크 분단으로 인해 Follower 3과 연결이 끊어졌을 때의 상황을 보여줍니다. 리더는 과반수(Majority)의 승인을 받지 못했으므로, 클라이언트에게 에러를 반환하거나 대기시킵니다.
> 3. **동작**: 결과적으로 클라이언트는 서비스 불능 상태가 되지만, 시스템 전체는 **Split Brain (분할 뇌)** 상태를 방지하고 데이터가 깨지는 것을 막습니다. **CP 시스템은 데이터를 잃지 않기 위해 서비스의 가용성을 희생**합니다.

#### AP 시스템: 비동기 복제와 낙관적 잠금
AP 시스템은 일단 로컬 디스크에 쓰기 기록을 완료하면 즉시 클라이언트에게 성공을 응답합니다. 백그라운드에서 다른 노드로 데이터를 복제하며, **Vector Clock (벡터 클럭)** 또는 **Gossip Protocol (고스립 프로토콜)**을 통해 버전 충돌을 해결합니다.

```text
[ AP System: Asynchronous Write & Conflict Resolution ]

   Client A                Client B
      │                       │
      │ ① Write(X=10)         │ ② Write(X=20) [During Partition]
      ▼                       ▼
   Node A                   Node B
 (Updated OK)             (Updated OK)
      │                       │
      │───────────────────────│───X Network Partition
      │                       │
      │ ③ Gossip Sync         │
      ◀───────────────────────│  (Reconnected)
      │                       │
   [CONFLICT DETECTED: X_v(10) vs X_v(20)]
   │
   ▼ ④ Resolve: "Last Write Wins" (LWW) or Application Merge
   Result: X = 20 (or App-specific logic)
```

> **해설**:
> 1. **도입**: AP 시스템은 **Dynamo 스타일** 아키텍처를 따릅니다. 데이터베이스는 항상 쓰기 가능(Write Available) 상태를 유지합니다.
> 2. **다이어그램**: 네트워크가 끊기는 순간, 양쪽 노드는 독립적으로 데이터를 업데이트합니다(①, ②). 사용자는 즉시 응답을 받습니다. 재연결(③) 후, 시스템은 두 버전의 데이터 충돌을 감지하고 **Conflict Resolution (충돌 해결)** 로직을 수행합니다.
> 3. **동작**: 이 과정에서 사용자는 순간적으로 다른 값을 보거나(Eventual Consistency), 쓰기가 덮어씌워질 수 있는 위험이 있지만, 서비스는 단 한 순간도 중단되지 않습니다.

#### 핵심 알고리즘: Quorum (N, R, W)
분산 시스템의 성격을 튜닝하는 핵심 수식은 다음과 같습니다.
$$ R + W > N $$
- **N**: 복제본 개수 (Replication Factor)
- **R**: 읽기 작업에 참여하는 최소 노드 수
- **W**: 쓰기 작업에 참여하는 최소 노드 수

```python
# Consistency Level 결정 로직 (Pseudo-code)

def check_consistency(N, R, W):
    # Strong Consistency (CP 경향)
    if W > N // 2:
        return "CP System: Write majority required"
    
    # High Availability (AP 경향)
    if R + W <= N:
        return "AP System: Risk of stale data"
    
    # Balanced
    if R + W > N:
        return "Balanced: Consistency guaranteed"
```

#### 📢 섹션 요약 비유
CP는 **'법관의 재판'**과 같아서 증거가 확실할 때까지 판결을 내리지 않아 억울한 일(데이터 오염)이 없으나 재판이 늦어지고, AP는 **'민주주의 투표'**와 같아서 개표가 다 끝나지 않아도 일단 개표 결과를 발표하여 속도는 빠르나 추후 번복(데이터 수정)될 여지가 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: 정량적 지표

| 비교 항목 | CP System (예: HBase) | AP System (예: Cassandra) |
|:---|:---|:---|
| **Latency (지연 시간)** | 높음 (동기 확인 필요) | 낮음 (로컬 완료 후 응답) |
| **Throughput (처리량)** | 낮음 (병목 발생 가능) | 매우 높음 (분산 처리 용이) |
| **Data Accuracy** | 100% (Strong) | 99.% (Eventually) |
| **Failure Impact** | 일부 서비스 중단 발생 | 서비스 유지, 데이터 부정합 가능 |
| **Use Case** | 재무, 결제, 항공 예약 | SNS 피드, 로그 수집, IoT |

#### 타 과목 융합 관점
1.  **네트워크와의 융합**: **PACELC Theorem** (Partition/Average-case Latency)에 따라, 네트워크가 정상일 때도 CP 시스템은 지연 시간(Latency)이 발생합니다. AP 시스템은 네트워크 비용을 줄이기 위해 **Read Repair**나 **Hinted Handoff** 같은 기술을 사용하여 지연을 숨깁니다.
2.  **OS와의 융합**: 분산 파일 시스템(예: **HDFS** in Hadoop)은 CP에 가까운 설계를 하여 데이터 분실을 방지하는 반면, **캐싱 시스템 (Redis Cluster)**은 성능을 위해 일관성을 희생하는 AP 성향을 보이기도 합니다.

#### 비교 시나리오: 장애 상황 시 시스템 반응

```text
[ Network Partition 발생 시 상태 비교 ]

┌────────────────────────────────────────────────────────────┐
│ Scenario: Leader와 Follower 간의 네트워크 두절             │
└────────────────────────────────────────────────────────────┘

[ CP Architecture (e.g., etcd) ]         [ AP Architecture (e.g., Cassandra)

 Node A (Leader)                          Node A (Replica 1)
   │                                      │
 X │──────(Network Cut)───────X           X │──────(Network Cut)───────X
   │                                      │
 Node B (Follower)                       Node B (Replica 2)
   │                                      │
 [Status]         Follower loses contact │  [Status]         Both nodes become 'Master'
   ▼                                      ▼
 "STOP" writes if Leader lost  │          "ACCEPT" writes to both A & B
 (Prevent Split Brain)         │          (Users may see different data)
                                  │
 Result: Service Unavailable   │          Result: Service Available
         (But Data Safe)                  (But Data Conflicted)
```

> **해설**: 이 도표는 장애 발생 시점의 결정적인 차이를 보여줍니다. CP는 **Safe Mode**로 진입하여 시스템을 보호하고, AP는 **Degraded Mode**로 진입하여 기능을 유지합니다. 현대의 클라우드 아키텍처는 이 둘을 적절히 혼합하여 사용합니다.

#### 📢 섹션 요약 비유
CP는 **'경찰의 봉쇄선'**처럼 사고(장애)가 나면 안전 확보를 위해 도로를 전면 차단하고, AP는 **'우회 도로'**처럼 본선이 막히면 덜 빠르더라도 골목길을 통해라도 차량(데이터)이 이동하게 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 실무 시나리오 및 의사결정 매트릭스
시스템 설계 시 다음 플로우차트