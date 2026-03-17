+++
title = "251. 3단계 커밋 (3PC, Three-Phase Commit) - 블로킹의 해법"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 251
+++

# 251. 3단계 커밋 (3PC, Three-Phase Commit) - 블로킹의 해법

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2PC (Two-Phase Commit)의 단일 장애점(SPOF, Single Point of Failure) 문제로 인한 **블로킹(Blocking) 상태**를 해결하기 위해, '예비 커밋(Pre-Commit)' 단계를 도입하여 비동기식 타임아웃 처리가 가능하게 한 분산 합의 프로토콜(Distributed Consensus Protocol)이다.
> 2. **가치**: 코디네이터(Coordinator)의 장애 발생 시, 참여자(Participant)들이 기다림 없이 일정 시간이 지나면 로그 상태를 기반으로 자율적으로 커밋 또는 롤백을 결정함으로써, 시스템 전체의 가용성(Availability)을 극대화한다.
> 3. **융합**: 분산 DB뿐만 아니라 분산 캐시 시스템 및 마이크로서비스 간의 데이터 일관성 유지에 응용되나, 네트워크 파티션(Network Partition) 환경에서의 데이터 정합성 이슈로 인해 실무에서는 더 강건한 Paxos나 Raft 알고리즘으로 대체되는 추세이다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
3PC (Three-Phase Commit) 프로토콜은 분산 트랜잭션 처리에서 원자성(Atomicity)을 보장하기 위한 합의 알고리즘의 일종이다. 기존의 2PC (Two-Phase Commit)가 트랜잭션 진행 중 코디네이터의 장애로 인해 참여자들이 무한 대기(Blocking) 상태에 빠지는 치명적 단점을 가지고 있음에 착안하여, 이를 해결하고자 '확신(Pre-Commit)'의 개념을 추가한 3단계 프로토콜을 정의한다.

**💡 비유**
2PC가 "결혼식 당일 신랑이 못 오면 식을 못 올리는 상황"이라면, 3PC는 "결혼식 전날에 하객들에게 다시 참석 확인을 받아두고, 당일에 신랑이 오지 않아도 하객들이 합의하여 식을 진행할 수 있게 하는 절차"와 같다.

**등장 배경**
① **기존 한계**: 2PC 방식에서는 코디네이터가 최종 커밋 명령을 전송하기 전에 장애가 발생하면, 참여자들은 트랜잭션 커밋 여부를 알 수 없어 리소스(Lock)를 잡은 상태로 영원히 대기해야 한다.
② **혁신적 패러다임**: 대기 상태를 해결하기 위해 타임아웃(Timeout) 기반의 상태 전이(State Transition) 로직을 도입하고, 중간 단계(Pre-Commit)를 통해 참여자 간의 정보 격차를 최소화한다.
③ **현재 비즈니스 요구**: 클라우드 환경과 같이 가용성이 생명인 시스템에서, 일부 노드의 장애가 전체 시스템을 멈추게 하는 블로킹 현상은 허용될 수 없으므로 비동기식 복구 메커니즘이 필수적이 되었다.

**ASCII 다이어그램: 블로킹 상태의 차이**

```text
[Concept: State Transition on Coordinator Failure]

      2PC (Blocking)                   3PC (Non-Blocking)
      =============                    ===================

   [Coordinator]                          [Coordinator]
       │   FAIL                              │   FAIL
       ▼                                     ▼
  [Before Commit]                      [Pre-Commit Confirmed]
       │                                     │
       ▼                                     ▼
 [Participants]                      [Participants]
       │                                     │
       ▼                                     ▼
   "LOCKED"                            "TIMEOUT"
   (Waiting forever)                  → "Auto Commit Decision"
                                         (Based on log state)
```

*해설*: 2PC에서는 코디네이터가 죽으면 참여자는 커밋할지 롤백할지 모르는 '불확실성(Uncertainty)' 상태에 빠진다. 반면 3PC에서는 참여자들이 이미 'Pre-Commit' 상태(모두가 Yes라고 함)임을 알고 있으므로, 타임아웃 시 스스로 "커밋해도 안전하다"고 판단할 수 있다.

> 📢 **섹션 요약 비유**: 2PC는 **"통신 두절된 약속 장소에서 친구가 올지 안 올지 모른 채 무작정 기다리는 것"**이라면, 3PC는 **"약속 전날에 '확실히 간다'는 확인을 받았으니, 당일에 연락이 안 되도 약속 장소에 가서 기다리는 것"**과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (표)**

| 요소명 | 역할 | 내부 동작 메커니즘 | 프로토콜/상태 | 비유 |
|:---|:---|:---|:---|:---|
| **Coordinator**<br>(코디네이터) | 트랜잭션 총괄 및 의사결정 주도 | 전체 참여자에게 명령을 내리고 상태를 수집하며, **타임아웃 시 재시도 또는 중단** 로직을 수행 | CanCommit, PreCommit, DoCommit | 결혼식 주례자 |
| **Participant**<br>(참여자/노드) | 실제 데이터 처리 및 합의 참여 | 로그(Log)에 현재 상태를 영속화(Persist)하고, 코디네이터 장애 시 **자체적으로 복구 결정** 수행 | Initial, Ready, PreCommit, Committed | 하객(증인) |
| **Log Storage**<br>(안정 저장소) | 상태 정보 영구 저장 | 시스템 장애 발생 전 마지막 상태를 저장하여 장애 복구 시一致性(Roll-forward) 제공 | WAL (Write-Ahead Logging) | 녹음된 약속 내용 |
| **Network Channel**<br>(통신 채널) | 메시지 전송 계층 | **신뢰성 있는 전송(Reliable Delivery)**을 전제로 하나, 파티션 발생 시 타임아웃으로 처리 | TCP/IP | 우편/연락망 |
| **Timeout Monitor**<br>(감시자) | 비정상 상태 감지 | 일정 시간 응답이 없을 경우 대기(Wait) 상태를 해제하고 다음 단계(Commit/Abort)로 진행 | T_wait, T_precommit | 알람 시계 |

**ASCII 구조 다이어그램: 3PC 상태 전이 (State Transition Diagram)**

```text
[3PC State Machine & Message Flow]

       [Coordinator]                           [Participant]
           State                                   State
            │                                        │
   (1) CanCommit? (Query)                           │
  ─────────────────────────────────────────────────▶ │
            │                               ┌────────▶│ (Initial)
            │                               │         │
            │ ◄────────────────────────────────────────│
   (2) Vote (Yes/No)                        │         │
            │                          ┌─────┘         │
            │                          │               │
   All Votes "Yes"?                     │               │
      (No → Abort)                      │               │
            │                           │               │
   (3) PreCommit (Notify)               │               │
  ─────────────────────────────────────────────────▶ │
            │                           │         ┌──▶│ (Ready)
            │                           │         │   │
            │ ◄────────────────────────────────────────│
   (4) ACK (Acknowledged)               │         │   │
            │                           │         │   │
            │                           │         │   │
   (5) DoCommit (Final)                 │         │   │
  ─────────────────────────────────────────────────▶ │
            │                           │         │   │
            │                           │         └──▶│ (PreCommit)
            │                           │             │
            ▼                           │             ▼
         [Done]                      [Commit]    [Commit]
```

*해설*:
1. **CanCommit 단계**: 코디네이터가 트랜잭션 ID를 전파하고 참여자는 자원 여부 확인 후 'Yes/No' 투표.
2. **PreCommit 단계**: 모두가 'Yes'이면 코디네이터는 'PreCommit' 메시지를 보냄. 참여자는 이를 받으면 "곧 커밋된다"는 확신을 얻고 로그를 기록함. **이 단계가 핵심**.
3. **DoCommit 단계**: 코디네이터가 최종 'DoCommit'을 보내면 참여자는 실제 커밋 수행.
4. **장애 복구 시나리오**: 만약 2단계(PreCommit) 전파 후 코디네이터가 죽어도, 참여자는 "PreCommit 상태였다"는 로그를 보고 Timeout 시 스스로 Commit 수행.

**심층 동작 원리 (알고리즘 로직)**

1. **CanCommit (투표 단계)**:
   - Coordinator: `Global TID` 생성 및 `CanCommit?(tid)` 브로드캐스트.
   - Participant: 로컬 트랜잭션 실행 및 Lock 획득 시도. 가능하면 `Vote_Commit`, 불가능하면 `Vote_Abort` 응답.
   - *Timeout*: 참여자가 응답 없으면 Abort 가정.

2. **PreCommit (예비 단계 - **핵심**)**:
   - Coordinator: 모든 참여자로부터 `Vote_Commit` 수신 시 `PreCommit(tid)` 전송.
   - Participant: `PreCommit` 수신 시, "Commit이 확실시 됨"을 로그에 기록(WAL). `ACK` 전송.
   - *Blocking 해제*: 이 시점부터 참여자들은 "모두가 찬성했다"는 것을 알게 됨.

3. **DoCommit (실행 단계)**:
   - Coordinator: 모든 참여자로부터 `ACK` 수신 시 `DoCommit(tid)` 전송.
   - Participant: 실제 데이터 영속 저장(Commit) 및 `HaveCommitted` 메시지 전송. Lock 해제.

**핵심 알고리즘 (의사코드)**

```python
# Participant Logic for Timeout Handling (Pseudo-code)

def on_timeout(current_state, logged_state):
    """
    타임아웃 발생 시 상태에 따른 자율 복구 로직
    """
    if current_state == INIT:
        # 아무 합의도 안 이루어짐 -> 안전하게 중단
        return "ABORT"
    
    elif current_state == READY:
        # 투표는 했으나 다른 노드 상태를 모름 -> 안전하게 중단
        return "ABORT"
    
    elif current_state == PRE_COMMIT:
        # 중요: 'PreCommit' 상태라면 누구도 반대하지 않았음을 의미
        # 코디네이터가 죽었어도 우리끼리 커밋해도 데이터 정합성 유지됨
        if logged_state == "PREPARED":
            return "COMMIT" # Non-blocking decision!
        else:
            return "ABORT"

# 3PC는 이 타임아웃 핸들러를 통해 자원을 영구 점유하지 않음.
```

> 📢 **섹션 요약 비유**: 3PC의 아키텍처는 **'구명보트 탑승 절차'**와 같습니다. 승무원(Coordinator)이 "탈 준비 됐어요?"(CanCommit) 물어보고, "그럼 탑승하세요"(PreCommit)라고 확인시켜준 뒤, 최종적으로 "출발하세요"(DoCommit)라고 외칩니다. 만약 승무원이 "탑승하세요"까지 말한 후 기절해도, 승객들은 "우리 모두 탔으니 출발하자"고 할 수 있는 권한을 얻게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교 (2PC vs 3PC)**

| 비교 항목 | 2단계 커밋 (2PC) | 3단계 커밋 (3PC) |
|:---|:---|:---|
| **구조 (Structure)** | Prepare (Locked) → Commit | CanCommit → **PreCommit** → DoCommit |
| **Blocking 특성** | **Blocking** (Coordinator 장애 시 무한 대기 가능) | **Non-Blocking** (Timeout으로 자율 해결 가능) |
| **메시지 복잡도** | 낮음 (Round trip 2회) | 높음 (Round trip 3회, Log 쓰기 빈번) |
| **장애 복구** | 외부 개입 필요하거나 복잡함 | 자율적 복구 가능 (설계에 따름) |
| **일관성 모델** | Strong Consistency (상시 보장) | Strong Consistency (보장하나 지연 시간 증가) |
| **네트워크 비용** | 적음 (Latency 낮음) | 큼 (Latency 높음, RTT 1회 추가) |

**과목 융합 관점 분석**

1.  **운영체제(OS) & 분산 시스템 (Distributed System)**:
    - 3PC는 분산 환경에서의 **락(Lock) 관리 전략**과 밀접하게 연관된다. 2PC가 교착상태(Deadlock)의 형태로 변할 수 있는 무한 대기를 해결하기 위해 **타임아웃 기반의 락 해제** 메커니즘을 도입한 것으로 볼 수 있다. 이는 커널의 뮤텍스(Mutex) 대기 시간 초과(Timeout)와 유사한 맥락이다.

2.  **네트워킹 (Networking)**:
    - **네트워크 파티션(Network Partition)** 문제와 깊은 관련이 있다. 3PC는 특정 노드 간의 통신이 두절되었을 때, 타임아웃을 통해 시스템이 멈추지 않도록 한다. 그러나 CAP 이론에서 C(Consistency)와 A(Availability) 사이의 트레이드오프를 완전히 해결하지는 못하며, 파티션 상황에서의 데이터 정합성을 보장하기 어려운 경우가 있다 (Split-brain 문제 완화).

**정량적 의사결정 매트릭스 (Latency 비교)**

```text
[Network Round-Trip Time (RTT) Comparison]

Assume Network Latency = L

2PC Total Time = 2L (Prepare + Commit)
3PC Total Time = 3L (CanCommit + PreCommit + DoCommit)

% Latency Increase = (3L - 2L) / 2L = 50% Performance Degradation
```

*해설*: 안정성(Stability)은 3PC가 높지만, 성능(Performance)은 약 50% 저하될 수 있다. 따라서 실시간 성능이 중요한 금융 거래보다는, 데이터 안정성이 중요한 배치 처리나 로깅 시스템에 더 적합할 수 있다.

> 📢 **섹션 요약 비유**: 2PC는 **"일방 통행식 고속도로"**로서 앞차가 고장 나면 뒤의 모든 차가 막히는 구조이다. 3PC는 **"우회로가 있는 고속도로"**를 건설하여 앞차가 고장 나면 옆 차로로 우회하거나 스스로 판단하여 운행을 이어가게 하지만, 도로를 건설하는 데 더 많은 비