+++
title = "450. 2단계 잠킹 프로토콜(2PL) - 직렬성의 보증"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 450
+++

# 450. 2단계 잠킹 프로토콜(2PL) - 직렬성의 보증

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2단계 잠금(2PL, Two-Phase Locking)은 트랜잭션의 생명 주기를 '잠금 획득'과 '잠금 해제'라는 두 가지 상호 배타적인 단계로 엄격히 분리하여, **비직렬 스케줄(Non-serial Schedule)의 충돌 직렬 가능성(Conflict Serializability)을 수학적으로 보장하는 동시성 제어 프로토콜**이다.
> 2. **가치**: 복잡한 다중 트랜잭션 환경에서 데이터 무결성(Integrity)을 침해하지 않으면서도 동시 실행을 가능하게 하며, 관계형 데이터베이스 관리 시스템(RDBMS)의 트랜잭션 격리 수준(Transaction Isolation Level)을 구현하는 핵심 메커니즘으로 작용한다.
> 3. **융합**: 운영체제(OS)의 세마포어(Semaphore)나 상호 배제(Mutex) 개념을 DB 영역으로 확장한 것으로, 교착 상태(Deadlock) 발생 가능성이라는 내재적 위험과 연쇄 복귀(Cascading Rollback) 방지를 위한 성능 트레이드오프를 관리해야 한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
2단계 잠금(Two-Phase Locking, 2PL)은 데이터베이스 트랜잭션이 데이터 일관성을 유지하기 위해 따라야 하는 프로토콜이다. 이 프로토콜에 따르면, 트랜잭션은 잠금(Lock)을 획득하는 단계와 잠금을 해제하는 단계를 명확히 구분해야 하며, 이 두 단계가 섞이는 것을 금지한다. 2PL은 E. F. Codd의 관계형 모델 이후, 다중 사용자 환경에서 데이터베이스의 상태를 모순 없이 유지하기 위해 등장했다.

**기술적 배경 및 필요성**
초기의 파일 시스템이나 단순한 데이터베이스는 데이터 접근을 직렬화(Serialization)하여 처리했으나, 이는 시스템의 처리량(Throughput)을 급격히 저하시켰다. 사용자의 요청이 폭증함에 따라 **Time-sharing(시분할)** 개념을 도입하여 여러 트랜잭션을 동시에 실행해야 했으나, 이로 인해 **Lost Update(갱신 분실)**, **Dirty Read(모순 읽기)**, **Inconsistent Retrieval(비일관성 검색)** 문제가 발생했다. 2PL은 이러한 동시성 제어 문제를 해결하기 위해, 트랜잭션 간의 충돌을 '잠금'이라는 물리적 메커니즘으로 통제하는 규약을 제시했다.

**등장 배경 흐름**
1. ① **기존 한계**: 동시 실행 시 `Write-Write` 충돌이나 `Read-Write` 충돌로 인해 데이터 정합성이 깨지는 문제 발생.
2. ② **혁신적 패러다임**: 모든 트랜잭션을 마치 하나씩 실행하는 것처럼 간주하는 **직렬 가능성(Serializability)** 이론을 정립하고, 이를 물리적 잠금(Lock)을 통해 실현.
3. ③ **현재의 비즈니스 요구**: 금융권(계좌 이체), 예약 시스템(좌석 배정) 등 데이터 정합성이 생명인 분야에서 RDBMS의 표준 규약으로 자리 잡음.

> **💡 비유**: 2PL은 '전시회장의 유명 작품 감상'과 같습니다. 작품을 감상하려면(트랜잭션) 입장권(잠금)을 받아야 하고, 감상을 시작한 뒤에는 티켓을 반환하기 전까지 다른 작품의 티켓을 요청할 수 없으며, 티켓을 반환(해제)하고 나면 다시는 해당 작품을 볼 수 없게 됩니다.

**📢 섹션 요약 비유**: 2단계 잠금 프로토콜은 **'고속도로 진입 램프와 진출 램프의 엄격한 분리'**와 같습니다. 차량(트랜잭션)은 고속도로(리소스)에 진입하기 위해 램프를 타고 속도를 높이는(잠금 획득) 구간을 거치고, 일단 진입한 후에는 목적지에 도달할 때까지 감속하며 진출(잠금 해제)할 때까지 중간에 멈추거나 진입할 수 없습니다. 이 규칙 덕분에 모든 차량이 사고 없이 순서대로 통행할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (Table)**

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/유형 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Lock Manager (LM)** | 잠금 요청 중재 및 허가 | 트랜잭션의 요청을 큐(Queue)에 쌓고, Lock Table(Lock Table)을 참조하여 모드 호환성(Mode Compatibility) 검증 | `S-Lock`(공유), `X-Lock`(배타) | 교통 통제소 |
| **Lock Table (LT)** | 현재 잠금 상태 저장 | 데이터 항목별로 현재 잠금을 보유한 트랜잭션 ID와 모드를 저장 및 관리 | Hash Table 구조 활용 | 예약 대장 |
| **Growing Phase (GP)** | 잠금 획득 구간 | 트랜잭션 시작 후 첫 `Unlock` 연산 전까지. `Lock-S`, `Lock-X` 요청 가능 | 확장 단계 | 쇼핑 중(장바구니 채우기) |
| **Shrinking Phase (SP)** | 잠금 해제 구간 | 첫 `Unlock` 연산发生后. 모든 잠금을 해제하며, `Lock` 요청 불가 | 축소 단계 | 계산 및 퇴장 |
| **Lock Point** | 직렬성 결정 지점 | 트랜잭션이 보유한 잠금의 수가 최대가 되는 시점. 이 시점에 따라 트랜잭션 간 선후 관계가 결정됨 | Max Lock Time | 결제 완료 시점 |

**ASCII 구조 다이어그램: 2PL Lifecycle**
아래 다이어그램은 트랜잭션의 시간 흐름에 따른 잠금 상태 변화를 도식화한 것이다.

```text
   [ Transaction Lifecycle under 2PL Protocol ]

   Number of Locks Held
        ▲
     5  |              +------+
        |              |      |
     4  |          +---+      |
        |          |         |
     3  |      +---+         |
        |      |             |
     2  |  +---+             |          [ Strict 2PL Variation ]
        |  |                 |           (Unlock held until End)
     1  +--+                 +----------------------------->
        | Growing Phase      | Shrinking Phase
        | (Only Lock Ops)    | (Only Unlock Ops)
        └────────────────────┴────────────────────────────────▶ Time
                ▲                ▲
                |                |
          [Lock Point]        [First Unlock]
     (Locks: 1 -> Max)       (Locks: Max -> 0)

   Legend:
   +--- : Acquiring Locks (L())
   ---- : Holding Lock
   ---- : Releasing Locks (U())
```

**다이어그램 해설**
위 다이어그램은 트랜잭션 진행 시간(Time)에 따른 보유 잠금 수(Locks Held)의 변화를 나타낸다.
1. **확장 단계(Growing Phase)**: 트랜잭션이 시작된 직후, 필요한 데이터에 대해 잠금 요청(`Lock-S(x)` 또는 `Lock-X(y)`)을 수행한다. 이 구간에서 잠금의 개수는 증가하며, 어떠한 잠금도 해제되지 않는다.
2. **Lock Point (락 포인트)**: 트랜잭션이 획득한 잠금의 개수가 최대에 도달하는 순간이다. 시스템은 이 지점을 기준으로 트랜잭션 간의 직렬 가능성(Serializability)을 판단한다.
3. **축소 단계(Shrinking Phase)**: 최초의 잠금 해제(`Unlock(z)`) 연산이 발생하면 진입한다. 이후부터는 모든 잠금을 해제해 나가며, 절대 새로운 잠금을 요청할 수 없다.

**심층 동작 원리 (Pseudo Code)**
```sql
-- Pseudo-code for 2PL Protocol Enforcement
FUNCTION Transaction_Start():
    state = GROWING
    lock_count = 0

FUNCTION Lock_Request(Item, Mode):
    IF state == SHRINKING:
        ERROR "Cannot acquire lock in Shrinking Phase"
    ELSE:
        WAIT UNTIL Compatible(Item, Mode)
        GRANT Lock(Item, Mode)
        lock_count++
        Update_Lock_Point_IF_NEEDED()

FUNCTION Unlock_Request(Item):
    RELEASE Lock(Item)
    state = SHRINKING  -- State transition happens ONCE here
    lock_count--
```

**핵심 알고리즘: 엄격한 2PL (Strict 2PL)**
현대 RDBMS(MySQL, Oracle)는 쓰기 연산과 관련된 배타 잠금(X-Lock)에 대해 **Strict 2PL**을 적용한다.
- **규칙**: 트랜잭션이 커밋(Commit) 되거나 중단(Abort)될 때까지 모든 배타 잠금(X-Lock)을 유지한다.
- **이유**: 다른 트랜잭션이 커밋되지 않은 데이터(Uncommitted Data)를 읽는 것(Dirty Read)을 방지하고, 연쇄 복귀(Cascading Rollback)를 원천 차단하기 위함이다.

**📢 섹션 요약 비유**: 2PL의 아키텍처는 **'랜선 정리 기계'**와 같습니다. 우선 모든 케이블(데이터)을 뽑아서 엉키지 않게 정리한 후(Growing Phase), 정리가 끝나야 구멍에 꽂습니다(Shrinking Phase). 만약 정리 중에 꽂으려다가 멈추면(Deadlock), 다시 뽑아야 하므로, 보통은 모든 작업이 끝나고 나서야 한 번에 꽂게 됩니다(Strict 2PL).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교표**

| 구분 (Feature) | 기본 2PL (Basic 2PL) | 보수적 2PL (Conservative 2PL) | 엄격한 2PL (Strict 2PL) | 강력한 2PL (Rigorous 2PL) |
|:---|:---|:---|:---|:---|
| **락 포인트 (Lock Point)** | 불명확 (실행 중 변동) | 트랜잭션 시작 시점 | 마지막 연산 수행 시점 | 트랜잭션 종료 시점 |
| **잠금 획득 시점** | 실행 중 수시 | 시작 시 모든 락 획득 | 필요 시 즉시 | 필요 시 즉시 |
| **잠금 해제 시점** | 실행 중 수시 (최초 해제 이후) | 실행 중 수시 | 트랜잭션 종료 시 (Commit) | 트랜잝션 종료 시 |
| **연쇄 복귀 (Cascading)** | **가능 (취약)** | **가능 (취약)** | **불가능 (안전)** | **불가능 (안전)** |
| **교착 상태 (Deadlock)** | **가능성 높음** | **가능성 낮음** | **가능성 높음** | **가능성 높음** |
| **병행성 (Concurrency)** | **높음** | **낮음 (선점 차단)** | **중간** | **낮음** |

**과목 융합 관점**
1. **운영체제(OS)와의 시너지**: 2PL은 OS의 **교착 상태(Deadlock) 예지 및 회피(Cycle Detection)** 기술과 직접 연결된다. OS의 자원 할당 그래프(Resource Allocation Graph)를 DB의 Wait-for Graph로 변환하여 교착 상태를 탐지하고, 희생자(Victim)를 선정하여 Rollback시킨다.
2. **네트워크와의 오버헤드**: 분산 DB 환경에서 2PL을 구현하면 **2-Phase Commit(2PC, 2단계 커밋)** 프로토콜과 결합되어 네트워크 왕복(Round Trip)이 발생하여 Latency가 급격히 증가할 수 있다. 이를 최적화하기 위해 **Timestamp Ordering(타임스탬프 순서화)** 기법과 혼합하여 사용하기도 한다.

**정량적 지표 분석 (Decision Matrix)**
- **Concurrency Level**: Basic 2PL이 가장 높으나 데이터 무결성 위험이 크다.
- **Recovery Cost**: Strict 2PL은 Lock 유지 시간이 길어 병행성이 떨어지나, 복구 비용(Cascading Rollback 방지)이 0에 수렴한다.

> **📢 섹션 요약 비유**: 2PL의 변형들을 비교하는 것은 **'여행 짐 싸기 스타일'**을 정하는 것과 같습니다. "보수적 2PL"은 모든 짐을 미리 싸서 가져가는 것(준비 오래 걸림, 이동 중 자유 없음)이고, "기본 2PL"은 가다가 필요한 것을 사고 쓰고 버리는 것(유연하지만 분실 위험), "엄격한 2PL"은 여행 끝까지 모든 영수증과 짐을 챙겨 다니는 것(번거롭지만 정산 안전함)과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**
1. **상황**: 은행의 계좌이체 시스템에서 A계좌에서 돈을 출금하여 B계좌로 입금하는 `Transfer(A, B)` 트랜잭션이 있다.
2. **문제**: A에 대한 잠금을 풀고 B에 잠금을 걸 때, 다른 트랜잭션이 A의 잔고를 조회하여 오차를 발생시키거나(Non-repeatable Read), A의 잠금이 풀리기도 전에 B의 잠금을 기다리며 교착 상태(Deadlock)에 빠질 수 있다.
3. **판단**:
    - **데이터 무결성이 최우선인 경우**: `Strict 2PL`을 적용하여 트랜잭션 종료 시까지 모든 Lock을 유지한다. (Most Common)
    - **대량의 배치 작업(Batch Job)인 경우**: `Conservative 2PL`을 사용하여 시작 시 모든 리소스를 Lock하고, 중