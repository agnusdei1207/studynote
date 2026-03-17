+++
title = "259. Raft와 Paxos 알고리즘 - 분산 합의의 정수"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 259
+++

# 259. Raft와 Paxos 알고리즘 - 분산 합의의 정수

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Raft와 Paxos는 **Distributed Consensus (분산 합의)** 문제를 해결하기 위한 핵심 알고리즘이며, 네트워크 지연이나 노드 장애가 발생하는 **CAP Theorem (Consistency, Availability, Partition Tolerance)**의 제약 환경에서 **CP(Consistency & Partition Tolerance)** 모델을 기반으로 시스템의 데이터 일관성을 수학적으로 보장한다.
> 2. **가치**: **FLP Impossibility (비동기 네트워크에서 안전성과 생존성을 동시에 만족하는 완전한 분산 합의는 불가능)**라는 이론적 한계 속에서, **Liveliness (생존성)** 보장을 위해 **Leader-based (리더 기반)** 구조를 채택하여 실무 수준의 **RPO (Recovery Point Objective)=0** 및 **RTO (Recovery Time Objective)** 최소화를 실현한다.
> 3. **융합**: Cloud-Native 시대의 **Control Plane (제어 평면)** 데이터 저장소인 **etcd (Kubernetes 백엔드)**, Apache Kafka의 **KRaft mode**, 그리고 NewSQL 데이터베이스인 **TiDB** 등에서 **Metadata Management (메타데이터 관리)** 및 **Configuration Store (구성 저장소)**로써 필수적인 인프라 요소로 자리 잡았다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
분산 합의 알고리즘은 **Replicated State Machine (RSM, 복제 상태 기계)** 방식을 기반으로, 여러 노드로 구성된 클러스터가 단일한 논리적 코어를 형성하도록 하는 메커니즘이다.
- **Safety (안전성)**: 시스템이 잘못된 상태(예: 두 개의 다른 리더 존재, 데이터 분기)로 절대 전이되지 않음을 보장한다.
- **Liveness (생존성)**: 시스템이 장애 발생 시에도 계속해서 응답하고 연산을 수행할 수 있음을 보장한다.

#### 2. 등장 배경: FLP와 CAP의 간담
- **기존 한계**: 단일 서버의 **SPOF (Single Point of Failure, 단일 장애점)** 문제를 해결하기 위해 데이터 복제를 시도했으나, "읽기 일관성"과 "쓰기 가용성" 사이의 트레이드오프가 발생했다.
- **혁신적 패러다임**: 1989년 Leslie Lamport의 **Paxos**가 "안전성 증명"이라는 수학적 토대를 제공했으나, 너무나 복잡하여 실무 구현에 실패했다. 이후 2014년 Diego Ongaro와 John Ousterhout는 **"Raft: In Search of an Understandable Consensus Algorithm"**을 발표, 이해 가능한 구조(Leader Election, Log Replication, Safety의 명확한 분리)를 통해 대중화되었다.
- **현재 비즈니스 요구**: 멀티 리전(Multi-Region) **K8s (Kubernetes)** 클러스터와 대규모 분산 DB의 안정적인 운영을 위해 필수적인 요소가 되었다.

#### 💡 비유
이는 여러 명의 기사들이 복잡한 전술을 짜는 것이 아니라, **"왕(Leader)의 명령서(Log)를 복사하여 집행하는 시스템"**과 같다. 왕이 쓰러지면 기사들이 즉시 투표로 새 왕을 뽑고, 새 왕의 기록만을 정통으로 인정하는 것이다.

#### 📢 섹션 요약 비유
> 분산 합의 알고리즘의 도입은 **"대중가요 악보를 여러 사람이 따로 부르는 것이 아니라, 지휘자(Leader)의 지휘봉에 맞춰 합창(Consensus)하는 오케스트라"**로 진화한 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Raft 알고리즘은 이해를 돕기 위해 시스템의 동작을 **리더 선출(Leader Election)**, **로그 복제(Log Replication)**, **안전성(Safety)**의 세 가지 모듈로 명확히 분리한다.

#### 1. 구성 요소 (상세 표)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 파라미터 | 비유 |
|:---|:---|:---|:---|
| **Server State** | 노드의 현재 상태 | **Follower (추종자)**, **Candidate (입후보자)**, **Leader (지도자)** 3가지 상태 전이 | 시민, 입후보자, 대통령 |
| **Persistent State** | 비휘발성 저장소 | `currentTerm` (현재 임기), `votedFor` (투표 대상), `log[]` (로그 엔트리) | 헌법 기록부, 수첩 |
| **Volatile State** | 휘발성 상태 | `commitIndex` (커밋된 인덱스), `lastApplied` (적용된 인덱스) | 진행 상황판 |
| **RPC (Remote Procedure Call)** | 통신 프로토콜 | **RequestVote** (투표 요청), **AppendEntries** (로그 추가/하트비트) | 선거 운동, 명령 전달 |
| **Election Timeout** | 선출 타임아웃 | 랜덤 범위(예: 150ms~300ms) 설정을 통해 **Split Vote(분할 투표)** 방지 | 각자 다른 시계를 보고 기다림 |

#### 2. Raft 아키텍처 및 상태 전이 다이어그램

아래 다이어그램은 노드의 상태가 시간과 장애에 따라 어떻게 변화하는지를 도시한 것이다.

```text
            [ Raft State Machine & Data Flow ]

        +---------------------------------------------------------+
        |  [Log Database] (Persistent)                            |
        |  Index:   1  |  2  |  3  |  4  |  5                     |
        |  Term:    1  |  2  |  2  |  3  |  3                     |
        |  Data:  [x=1][x=2][x=3][y=1][y=2]  <-- AppendEntries    |
        +---------------------------------------------------------+
                     ▲            ▲            ▲
                     |            |            | (Replication)
                     |            |            |
    +----------------+            |            +-----------------+
    |                             |                             |
[ Follower ] <---(Heartbeat/Append)---+---(Timeout)--> [ Candidate ]
    |   ▲                          |  |  |                      |
    |   |                          |  |  |  (RequestVote RPC)    |
    |   |                          |  ▼  ▼                      |
    |   |                       (Grant Vote)                 |
    |   |                          |  |  |                      |
    |   +------------------(Majority Votes Received)-----------+
    |                                   |
    |                                   v
    +--------------------------- [ Leader ]
                                      |
                                      +---> (Client Request 받기)
                                      +---> (Log Append to Followers)
                                      +---> (Commit Index Update)
```

**[다이어그램 해설]**
1.  **Follower (추종자)**: 초기 상태이자 정상 상태다. Leader로부터 주기적으로 `AppendEntries` RPC(Heartbeat)를 받으면 타이머를 리셋한다.
2.  **Candidate (입후보자)**: Heartbeat가 일정 시간(`Election Timeout`) 동안 없으면, 스스로 리더 선거를 시작한다. `currentTerm`을 1 증가시키고, 자기 자신에게 투표한 후 타 노드들에게 `RequestVote` RPC를 보낸다.
3.  **Leader (지도자)**: 과반수(Majority, $N/2 + 1$)의 투표를 얻으면 리더가 된다. 모든 클라이언트 요청을 받아 로그에 기록하고, 이를 팔로워들에게 복제한 뒤 커밋한다.

#### 3. 핵심 알고리즘 및 로직 (Go Style Pseudo-code)

리더의 로그 복제 로직은 다음과 같은 로직을 따른다.

```go
// Leader's Loop for each Follower
func (rf *Raft) sendAppendEntries(serverId int) {
    prevLogIndex := rf.nextIndex[serverId] - 1
    prevLogTerm := rf.log[prevLogIndex].Term
    
    // Prepare AppendEntries RPC Arguments
    args := AppendEntriesArgs{
        Term:         rf.currentTerm,
        LeaderId:     rf.me,
        PrevLogIndex: prevLogIndex,
        PrevLogTerm:  prevLogTerm,
        Entries:      rf.log[prevLogIndex+1:], // Send new entries
        LeaderCommit: rf.commitIndex,
    }

    // Send RPC
    reply := &AppendEntriesReply{}
    ok := rf.peers[serverId].Call("Raft.AppendEntries", args, reply)

    if ok {
        if reply.Success {
            // Successful: Update nextIndex and matchIndex
            rf.nextIndex[serverId] = rf.getLastLogIndex() + 1
            rf.matchIndex[serverId] = rf.getLastLogIndex()
            
            // Commit Rule: If N is committed, update commitIndex
            if rf.matchIndex[serverId] > rf.commitIndex {
                rf.updateCommitIndex()
            }
        } else {
            // Conflict: Follower's log differs. Decrement nextIndex (Backtrack)
            rf.nextIndex[serverId]-- 
        }
    }
}
```

#### 📢 섹션 요약 비유
> Raft의 동작 원리는 **"복사 기계 장부"**를 관리하는 회계사와 같습니다. 모든 지점은 본사(Leader)의 장부 내역을 그대로 베껴 적고(Append), 본사가 도장을 찍으면(Commit) 그제야 그 내역이 확정되는 것입니다. 본사가 연락이 두절되면 각 지점은 자신의 시계를 보고 가장 먼저 기한을 확인한 사람이 임시 회계사(Candidate)가 되어 동료들에게 "내가 회계를 맡겠다"고 캠페인(RequestVote)을 벌입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. Paxos vs Raft: 기술적 심층 비교

| 비교 항목 | Paxos (Classic/Multi) | Raft |
|:---|:---|:---|
| **결정 방식** | **Proposer (제안자)**가 **Acceptor (수락자)**들에게 제안 번호(Proposal Number)를 증가시키며 승인을 요청함. | **Leader (제안자)**가 독점적으로 제안하며, **Follower (수락자)**는 오직 Leader의 로그만 수락함. |
| **로그 일관성** | 로그 엔트리의 순서가 보장되지 않을 수 있으며, Hole(구멍)이 발생할 수 있음. | 로그는 항상 연속적이며 순서가 엄격히 보장됨 (No Holes). |
| **구현 복잡도** | **Very High**. Paxos는 Basic Paxos(단일 합의)를 설명하나, 실무엔 Multi-Paxos(다중 합의)가 필요하며 구현마다 상이함. | **Moderate**. 알고리즘이 명확히 분리되어 있어 표준화된 구현이 존재함. |
| **리더 선출** | 별도의 메커니즘으로 구현해야 함 (Paxos 원문에선 미포함). | 핵심 알고리즘 내에 **Leader Election**이 포함되어 있음. |
| **성능 특성** | 리더 경쟁(Proposer conflict)이 발생하면 **Livelock (생존성 교착)** 상태가 될 가능성이 있어 Latency가 편차가 큼. | 리더가 존재하는 한 **안정적인 처리량(Throughput)** 제공. |

#### 2. 분산 시스템 융합 관점 (Cross-Domain)

- **운영체제(OS)와의 융합**: 분산 파일 시스템(예: **GFS, HDFS**)의 **Metadata Node (메타데이터 노드)**의 HA(High Availability) 구성에 사용되어, Single Master의 장애를 극복한다.
- **네트워크와의 융합**: SDN(Software Defined Network) 컨트롤러(예: ONOS) 등에서 네트워크 토폴로지 정보의 일관성을 유지하기 위해 Raft 기반의 클러스터링을 사용한다.
- **AI/ML과의 융합**: 분산 학습 환경(Parameter Server)에서 모델 파라미터의 버전 관리 및 체크포인팅을 위한 상태 동기화 메커니즘으로 응용된다.

#### 📢 섹션 요약 비유
> Paxos는 **"자유 민주주의 의회"**와 같습니다. 누구든지 발의할 수 있고(Proposer), 다수결로 법안을 통과시키지만, 발의권이 서로 충돌하면 회의가 난상토론으로 흐러질 위험이 있습니다. 반면 Raft는 **"입헌 군주제 내각"**과 같습니다. 총리(Leader)가 모든 법안을 제출하고, 국회의원(Follower)은 이에 대해 찬반 표결만 하면 되므로, 처리 속도가 빠르고 정책 일관성이 유지됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실제 대규모 시스템에서의 합의 알고리즘 도입 시 고려해야 할 전략적 판단 기준과 시나리오를 다룬다.

#### 1. 실무 시나리오 및 의사결정 매트릭스

**시나리오 1: Kubernetes Control Plane의 장애 복구 속도 개선**
- **상황**: K8s 마스터 노드 3대 중 1대가 **Network Partition (네트워크 분리)** 되어 **Minority**에 고립됨.
- **의사결정**: Raft 기반 etcd는 과반수(2대)의 연결을 유지하므로, 쿠버네티스 API 서버는 계속 정상 작동함. 고립된 노드는 리더 선출에 실패하여 타임아웃 후 자동으로 복구 대기 상태로 전이됨.
- **결과**: 사용자 파드(Pod) 생성/삭제 등의 중요 운영이 중단되지 않음 (**Zero Downtime**).

**시나리오 2: 금융 거래 시스템의 데이터 일관성**
- **상황**: 계좌 이체 중 데이터베이스 **Leader**가 셧다운됨.
- **의사결정**: 아직 복제되지 않은 로그가 메모리에 남아 있으므로, **Follower**가 새 **Leader**가 될 때 이 로그는 소멸됨 (Consistency 우선).
- **Trade-off**: 일부 거래 데이터 유실 가능성(RPO > 0)을 감수하더라도, **이중 지급(Double Spending)** 같은 데이터 불일치 상황은 막아야 함. 따라서 **Linearizable Consistency (선형성)**를 위해 Raft를 사용.

#### 2. 도입 체크리스트

| 구분 | 체크 항목 | 설명 |
|:---|:---|:---|
| **기술적** | **Quorum Size** |