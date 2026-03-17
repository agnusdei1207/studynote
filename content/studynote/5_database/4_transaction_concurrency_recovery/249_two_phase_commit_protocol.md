+++
title = "249. 2단계 커밋 (2PC, Two-Phase Commit) - 동기적 합의의 정석"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 249
+++

# 249. 2단계 커밋 (2PC, Two-Phase Commit) - 동기적 합의의 정석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2단계 커밋(2PC, Two-Phase Commit)은 분산 데이터베이스 환경에서 트랜잭션의 원자성(Atomicity)을 보장하기 위해, 모든 참여 노드(Participant)가 작업을 완료하고 준비(Ready) 상태에 돌입했을 때만 최종 커밋을 수행하는 **동기식 합의 프로토콜**입니다.
> 2. **가치**: "All or Nothing(전부 성공하거나 전부 실패)" 철학을 구현하여 금융 거래와 같은 데이터 정합성이 생명인 시스템에서 **Strong Consistency(강한 일관성)**를 제공합니다. 분산 트랜잭션 코디네이터(DTC, Distributed Transaction Coordinator)를 통해 복잡한 분산 환경을 단일 트랜잭션처럼 제어합니다.
> 3. **융합**: XA (eXtended Architecture) 표준 인터페이스와 결합하여 이종(異種) 데이터베이스 간의 트랜잭션을 조율하지만, 코디네이터 장애 시 전체 시스템이 멈추는 **Blocking(블로킹)** 문제와 **CAP 정리**의 CA(Consistency & Availability) 트레이드오프 관계에서 항상 고민거리를 제공합니다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 1. 개념 및 철학
**2단계 커밋(2PC, Two-Phase Commit)**은 분산 시스템에서 여러 노드에 걸친 데이터베이스 작업을 하나의 논리적 단위로 묶는 가장 대표적인 **분산 합의 프로토콜(Distributed Consensus Protocol)**입니다.
분산 데이터베이스의 가장 큰 적은 '네트워크 실패'와 '부분적 장애'입니다. 노드 A는 성공했는데 노드 B는 실패해서 데이터가 꼬이는 상황을 방지하기 위해, 2PC는 **'선 준비(Prepare), 후 실행(Commit)'**의 엄격한 계약 원칙을 도입했습니다.

- **핵심 용어 정의**:
    - **TM (Transaction Manager)**: 글로벌 트랜잭션을 총괄하는 코디네이터(Coordinator).
    - **RM (Resource Manager)**: 실제 데이터를 관리하는 참여자(Participant) 노드 (예: DB, WAS).
    - **Commit Protocol**: 트랜잭션의 결과를 결정하고 확정하는 일련의 규칙.

#### 2. 등장 배경 및 진화
① **기존 한계**: 단일 DB에서의 ACID 트랜잭션은 분산 환경(마이크로서비스, 샤딩)에서는 무력합니다. 네트워크 오류로 인한 데이터 불일치(Inconsistency)가 빈번히 발생했습니다.
② **혁신적 패러다임**: **XA 표준 (eXtended Architecture)**이 등장하면서, 서로 다른 DB 벤더(MySQL, Oracle 등) 간에도 트랜잭션을 묶을 수 있는 표준화된 인터페이스가 제공되었습니다. 2PC는 이를 구현하는 구체적 알고리즘입니다.
③ **현재의 비즈니스 요구**: 클라우드 환경으로 넘어오면서 가용성(Availability)이 중요해졌으나, 여전히 금융권의 핵심 결제 시스템 등에서는 데이터 정합성을 타협할 수 없어 2PC 계열의 알고리즘이 사용됩니다.

#### 3. 💡 비유
마치 **'원격 회의를 통한 중요 안건 표결'**과 같습니다. 회의 주재자(Coordinator)가 참석자들에게 "이 안건에 찬성할 준비가 되셨습니까?"라고 묻고(1단계), 모든 참석자가 "예"라고 하면 "가결"을 선포(2단계)합니다. 단 한 명이라도 반대하거나 답변이 없으면 회의는 무효가 되거나 무기한 연기됩니다.

#### 📢 섹션 요약 비유
2PC는 **'오프라인 동호회 회비 납부'**와 같습니다. 회장이 "회비 다 냈어?"라고 확인을 받기 전까지는(Commit Phase 전까지), 누구도 그 돈을 실제로 사용할 수 없고 계좌에서 출금해지지도 않습니다. 모두가 준비된 상태에서만 비로소 실제 금전적 거래가 일어납니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 1. 구성 요소 상세 분석

| 요소명 | 역할 | 내부 동작 (Mechanism) | 주요 프로토콜/명령어 | 비유 |
|:---:|:---|:---|:---|:---|
| **Coordinator** (TM) | **트랜잭션 총괄** | 분산 트랜잭션의 시작/종료를 관리하고, 참여자의 투표 결과를 취합하여 최종 명령(Commit/Rollback)을 내림. **Global Transaction ID(GXID)** 할당 및 로그 관리. | `Prepare`, `Commit`, `Rollback` | 회의 주재자 |
| **Participant** (RM) | **자원 관리자** | 실제 DB 연산을 수행. `Prepare` 요청 시 수행할 연산을 로그에 기록(LSN Log)하고 **Lock**을 획득한 상태로 대기함. | `Ready`, `Abort`, `ACK` | 주주 혹은 참여자 |
| **Transaction Log** | **복구 불변성** | 장애 발생 시 복구를 위한 영속적 기록 장치. Prepare 상태 로그가 남아있으면 장애 복구 후 다시 투표 여부를 묻는다. | WAL (Write-Ahead Logging) | 회의록 |
| **Lock Manager** | **동시성 제어** | Prepare 단계에서 다른 트랜잭션이 해당 데이터를 접근하지 못하도록 배타적 락(X-Lock)을 유지함. | 2PL (Two-Phase Locking) | 경비원 |

#### 2. 2PC 상태 전이 및 데이터 흐름

2PC는 엄격한 순서를 가진 상태 기계(State Machine)로 동작합니다. 다음은 트랜잭션이 성공하는 **Happy Path**와 실패하는 **Failure Path**를 포함한 완전한 다이어그램입니다.

**[ASCII Diagram: 2PC State Transition & Message Flow]**

```text
   Phase 1: Voting (Prepare)              Phase 2: Completion (Commit)
   -------------------------              ---------------------------

   Coordinator                Participant (Node A, B, ...)
   ------------              ------------------------------
        |                              |
        |   1. GLOBAL_PREPARE          |  (예상) Write-Ahead Log
        |   (ID: TRX-001)              |  (Uncommitted) Locking...
        |----------------------------->|
        |                              |
        |                              | [Processing...]  <--- 락(Lock) 유지 시작
        |                              |
        |   2. READY (Vote: YES)       |
        |<-----------------------------|
        |   (or NO/Timeout)            |  (if Timeout -> Rollback)
        |                              |
   [Decision Logic]             ------------------------------
   (All YES?)                         |
        |                             |
   (YES) | (NO)                       |
     \   |   /                        |
      \  |  /                         |
       v v v                          |
        |                             |
   3. GLOBAL_COMMIT                  |
   (or GLOBAL_ROLLBACK)              |
   ------------------------------>   |
        |                             |
        |   4. ACK (Applied)          |  [COMMIT] -> Release Lock
        |<-----------------------------|
        |                             |
   [End Transaction]             ------------------------------
```

#### 3. 심층 동작 원리 (Deep Dive)

**Phase 1: The Commit Request Phase (Prepare Phase)**
1. **시작**: 코디네이터(Coordinator)가 글로벌 트랜잭션을 시작하고 모든 참여자(Participant)에게 `PREPARE` 명령을 전송합니다.
2. **실행 및 락킹**: 참여자는 트랜잭션에 포함된 연산을 수행하되, **아직 커밋하지는 않습니다.** 대신 로그(Log)에 "준비 완료" 상태를 기록하고, 관련 리소스에 **쓰기 잠금(Write Lock)**을 겁니다.
3. **응답**: 참여자는 작업이 가능하면 `READY(Commit 가능)`, 불가능하면 `NO`를 응답합니다.

**Phase 2: The Commit Phase**
1. **결정**: 코디네이터는 모든 투표를 모읍니다.
   - **All YES**: `GLOBAL_COMMIT` 명령 전송.
   - **Any NO / Timeout**: `GLOBAL_ROLLBACK` 명령 전송.
2. **확정**: 참여자는 최종 명령에 따라 실제 커밋을 수행하거나 롤백하고 락을 해제한 후 `ACK`를 보냅니다.
3. **완료**: 모든 `ACK`를 받으면 코디네이터는 트랜잭션을 종료합니다.

#### 4. 핵심 코드 의사코드 (Pseudo-Code)

```python
# Coordinator Logic
def two_phase_commit(participants):
    # Phase 1: Prepare
    votes = []
    for p in participants:
        try:
            vote = p.send_prepare()   # "Can you commit?"
            if vote != "READY":
                return abort_transaction()
            votes.append(vote)
        except TimeoutError:
            return abort_transaction() # Blocking occurs here

    # Phase 2: Commit (If all voted YES)
    for p in participants:
        p.send_commit()               # "Do commit!"
        # 기다림 (Blocking)
        p.wait_for_ack()
    
    return "TRANSACTION_COMMITTED"
```

#### 📢 섹션 요약 비유
2PC의 두 단계는 마치 **'도마 위의 닭'**과 같습니다. 1단계(Prepare)는 요리사가 "이 닭으로 요리해도 되나?"라고 확인하고 칼을 높이 든 상태입니다. 2단계(Commit)가 떨어지는 순간에야 비로소 닭이 조리됩니다. 도마 위에 있는 동안은 다른 요리사(다른 트랜잭션)가 그 닭을 건드릴 수 없는 **'락(Lock)'** 상태에 놓입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 2PC vs 3PC (Three-Phase Commit)
분산 환경에서의 안전성과 성능을 비교 분석합니다.

| 구분 | 2PC (Two-Phase Commit) | 3PC (Three-Phase Commit) |
|:---|:---|:---|
| **단계 수** | Prepare → Commit | CanCommit? → PreCommit → DoCommit |
| **Blocking** | **Blocking (블로킹)**<br>Coordinator 장애 시 무한 대기 가능 | **Non-Blocking (논블로킹)**<br>Timeout 설정을 통해 장애 복구 가능 |
| **네트워크 비용** | 상대적으로 낮음 (2번의 왕복) | 높음 (3번의 왕복) |
| **구현 복잡도** | 간단함 (대부분의 DB 표준) | 매우 복잡함 (거의 실용화되지 않음) |
| **CAP 정리** | CA (Consistency & Availability)<br>장애 시 A 희생 | CP (Consistency & Partition Tolerance)<br>네트워크 분단 상황 처리에 유리 |

#### 2. RDBMS (ACID) vs NoSQL (BASE) 및 Saga 패턴
트랜잭션 관리 방식의 근본적 차이를 분석합니다.

| 특성 | **2PC (RDBMS/XA)** | **Saga Pattern (MSA/NoSQL)** |
|:---|:---|:---|
| **일관성 모델** | **Strong Consistency**<br>트랜잭션 도중 중간 상태 노출 안 함 | **Eventual Consistency**<br>중간 단계의 임시 일관성 상태 노출 가능 |
| **성능 (Latency)** | **낮음 (High Latency)**<br>모든 노드 동기 대기 필요 | **높음 (Low Latency)**<br>비동기 메시징 처리 가능 |
| **로직 방식** | **Undo/Redo Log**<br>시스템 수준의 자동 복구 | **Compensating Transaction**<br>비즈니스 로직 수준의 수동 취소 처리 |
| **락(Lock)** | **Pessimistic Lock**<br>Prepare 시간 동안 전체 리소스 락 | **Optimistic/No Lock**<br>별도의 글로벌 락 없음 |

#### 3. 융합 관점: 네트워크 및 운영체제와의 시너지
- **OS (Operating System)**: 2PC의 WAL(Write-Ahead Logging) 기법은 OS의 페이지 캐시 관리 및 파일 시스템의 `fsync()` 호출과 밀접하게 연관됩니다. 디스크 I/O 성능이 2PC의 전체 성능을 좌우합니다.
- **네트워크 (Network)**: 네트워크 지연(Latency)은 2PC의 치명적인 적입니다. `Commit Phase`에서 코디네이터와 참여자 간의 RTT(Round Trip Time)가 그대로 트랜잭션 처리 시간에 더해집니다.

#### 📢 섹션 요약 비유
2PC와 Saga의 차이는 **'예식장 결혼(2PC)'과 '동거 후 혼인 신고(Saga)'**의 차이와 같습니다. 2PC는 모든 절차가 끝날 때까지 법적으로 부부가 아닌 상태(락)를 유지하며 엄격하지만 느립니다. Saga는 일단 살아보고(Commit) 안 맞으면 헤어지는(Compensating Transaction) 절차를 밟는 자유롭지만 헤어질 때 복잡한 방식입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

#### 1. 실무 시나리오: 도입 의사결정 매트릭스
시스템 아키텍트는 다음과 같은 상황에서 2PC 도입을 고려해야 합니다.

| 상황 | 2PC 도입 추천 (O) | 대안 모색 (X) |
|:---|:---:|:---:|
| **데이터 정합성** | 금융 결제, 재무 회계 (1원 오차 허용 안 함) | SNS 좋아요 수, 조회수 (약간의 오차 허용) |
| **시스템 환경** | 단일 데이터베이스 혹은 네트워크 지연이 매우 낮은 LAN 환경 | 전 세계 분산된 클라우드 환경 (WAN) |
| **볼륨/TPS** | 낮은 TPS (초당 수백 건 이하)의 핵심 트랜잭션 | 높은 TPS (초당 수만 건 이상)의 대량 처리 |

#### 2. 도입 체크리스트

**[기술적 검사]**
- [ ] **네트워크 안