+++
title = "223. 낙관적 동시성 제어 (Optimistic Concurrency Control)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 223
+++

# 223. 낙관적 동시성 제어 (Optimistic Concurrency Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 낙관적 동시성 제어(OCC, Optimistic Concurrency Control)는 다중 사용자 환경에서 데이터 충돌이 드물다는 **낙관적 가정(Optimistic Assumption)**하에, 트랜잭션 진행 중 **락(Lock)을 사용하지 않고** 연산을 수행하다가 커밋 시점에 일관성을 검증하는 비관계형 데이터베이스 및 고성능 DBMS의 핵심 제어 기법이다.
> 2. **가치**: 데이터베이스 버퍼 관리자(Buffer Manager)의 락 관리 오버헤드와 트랜잭션 대기 시간(Latency)을 제거하여, 읽기 중심(Read-heavy)의 웹 애플리케이션에서 **초당 트랜잭션 처리량(TPS, Transactions Per Second)**을 획기적으로 향상시킨다.
> 3. **융합**: 분산 시스템의 **MVCC(Multi-Version Concurrency Control)**와 밀접하게 연결되며, JPA(Java Persistence API)의 `@Version` 어노테이션, NoSQL(Cassandra, DynamoDB 등)의 **CAS(Compare-And-Swap)** 연산, 그리고 HTTP 조건부 요청(ETag/If-Match)의 이론적 근간이 된다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**OCC (Optimistic Concurrency Control)**는 데이터베이스 트랜잭션 관리에서 데이터 무결성을 보장하기 위해 고안된 제어 기법의 하나입니다. 전통적인 **2PL (Two-Phase Locking)** 방식이 트랜잭션 시작과 동시에 락을 획득하여 다른 트랜잭션을 대기시키는 '비관적' 접근인 반면, OCC는 사용자들이 데이터를 동시에 수정하지 않을 것이라고 '낙관적으로' 가정합니다. 따라서 트랜잭션이 수행되는 동안에는 DB 리소스에 전혀 락을 걸지 않고, 각 트랜잭션은 자신만의 **작업 공간(Private Workspace)**인 로컬 버퍼에서 데이터를 사본으로 받아 작업합니다. 이후 커밋 요청 시점에 로그를 분석하여 **직렬 가능성(Serializability)**을 위반하는지 검증(Validation)합니다. 검증에 실패하면 해당 트랜잭션은 롤백(Rollback)되고 재시도됩니다.

**등장 배경 및 철학**
관계형 데이터베이스(RDBMS) 초기에는 락 기반 관리가 표준이었으나, 인터넷의 발전과 함께 수천만 명의 사용자가 동시에 접속하지만 실제로는 데이터를 '조회'하는 경우가 '수정'하는 경우보다 훨씬 많은 **OLTP(Online Transaction Processing)** 환경이 확산되었습니다. 이러한 환경에서는 락에 의한 대기 시간이 병목이 되었습니다. 이를 해결하기 위해 Kung와 Robinson이 1981년 제안한 방식이 OCC이며, 하드웨어의 발전(Multi-core CPU, 빠른 메모리)으로 인해 롤백 비용이 낮아지면서 현대의 고성능 시스템에서 핵심적인 기법으로 자리 잡았습니다.

**💡 비유**
이는 마치 **"카페에서 자유롭게 좌석 이용하기"**와 같습니다. 비관적 제어는 자리에 앉기 전에 직원에게 예약을 하고(락 획득), 예약된 자리는 아무도 앉지 못하게 막는 방식입니다. 반면, 낙관적 제어는 따로 예약 없이 일단 자리에 앉아서 편하게 쉽니다(작업 수행). 그러다 나갈 때(커밋 시점) "혹시 제가 앉아있는 동안 제 자리에 다른 분이 오셔서 예약표를 붙이셨나요?"라고 확인합니다. 만약 누군가 와서 예약해놨다면(충돌), 아쉽게도 다른 자리를 찾아야 합니다(롤백 및 재시도).

**📢 섹션 요약 비유**
비관적 락이 **'입장권을 끊고 줄 서는 놀이공원'**이라면, 낙관적 제어는 **'신용만 믿고 이용 후 결제하는 무인 카페'**와 같습니다. 충돌이 드문 상황에서는 절차가 간단하여 이동(처리) 속도가 훨씬 빠릅니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

OCC는 내부적으로 데이터베이스의 **버전 관리자(Version Manager)** 또는 **트랜잭션 처리기(Transaction Processor)**에 의해 다음과 같은 3단계 프로세스를 통해 엄격하게 관리됩니다.

#### 1. 구성 요소 및 상세 모듈
| 모듈 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 프로토콜/데이터 | 비고 |
|:---|:---|:---|:---|:---|
| **Read Phase (판독 단계)** | 데이터 추출 및 로그 기록 | 실제 DB 파일이 아닌 **Private Workspace**로 데이터 사본 복사. 읽기 레코드 목록(`read_set`)과 쓰기 레코드 목록(`write_set`)을 메모리에 유지. | Read Operation, Snapshot | Lock 없음 |
| **Validation Phase (검증 단계)** | 직렬 가능성(Serializability) 보장 | 커밋 요청 시, 현재 트랜잭션(`T_curr`)의 `read_set`이 활성화된 다른 트랜잭션(`T_active`)들의 `write_set`과 겹치는지 확인. | **Timestamp Ordering**, Validaion Rule | 핵심 알고리즘 |
| **Write Phase (기록 단계)** | 지속성(Persistence) 반영 | 검증 통과 시, Private Workspace의 변경사항을 실제 DB Disk에 flush하고 Log Buffer의 WAL(Write-Ahead Log)을 기록. | Commit, Physical I/O | Fail 시 Rollback |
| **Concurrency Control Manager** | 충돌 관리 및 스케줄링 | 다수 트랜잭션이 동시에 Validation 단계에 진입했을 때 순서를 부여하고, 충돌 시 Retry 로직(Exponential Backoff 등)을 제어. | Scheduler, Wait-Die | 분산 환경 필수 |

#### 2. OCC 상태 전이 및 동작 다이어그램
아래 다이어그램은 OCC의 전체 라이프사이클과 각 단계에서의 데이터 흐름을 도식화한 것입니다.

```text
[ OCC (Optimistic Concurrency Control) 상태 머신 및 데이터 흐름도 ]

   [USER]                      [TRANSACTION MANAGER]                     [DB STORAGE]
      |                               |                                        |
      | --- 1. BEGIN Tx -------------> | ---> Create Workspace (Copy Data)      |
      |                               |       (No Locks - Shared Read)         |
      |                               |                                        |
      | --- 2. READ/WRITE ----------> | <--- Fetch Data to Buffer              |
      |                               |      Update in Local Memory Only       |
      |                               |      (write_set: {A}, read_set: {B})   |
      |                               |                                        |
      | --- 3. COMMIT REQUEST ------> | ---> [ VALIDATION PHASE ] <--- Check   |
      |                               |      |                                  |
      |                               |      +-- Is read_set ∩ write_set(T_others) = ∅ ? 
      |                               |      |   (No intersection?)             |
      |                               |      |                                  |
      |                               |      +-- YES (Safe)                    +-- NO (Conflict)
      |                               |      |                                  |
      |                               |      v                                  v
      |                               | [ WRITE PHASE ]                 [ ABORT PHASE ]
      |                               |      |                                  |
      | <--- SUCCESS ---------------- |      +-- Apply to Disk               +-- Rollback Local
      |                               |          Release Workspace               Retry (Wait)
      |                               |                                        |
```

**다이어그램 해설**
1. **Read Phase**: 사용자가 데이터를 요청하면 DB는 락을 걸지 않고 데이터를 반환합니다. 트랜잭션 매니저는 이 시점부터 사용자의 변경 사항을 로컬 버퍼에 격리(Isolation)시킵니다. 따라서 다른 사용자는 이 변경 사항을 볼 수 없습니다.
2. **Validation Phase**: OCC의 '하트(Heart)'입니다. 트랜잭션이 커밋하려는 순간, 시스템은 "내가 읽은 데이터(`read_set`)를 내가 수정하는 동안 다른 놈이 수정했나?"를 검사합니다.
   - **Backward Validation**: 자신보다 먼저 들어온 트랜잭션과의 충돌을 검사.
   - **Forward Validation**: 자신보다 늦게 들어온 트랜잭션과의 충돌을 검사 (일반적으로 사용).
3. **Write vs Abort**: 검증에 성공하면 DB에 실제로 반영(Commit)하고, 실패하면 모든 작업을 취소(Rollback)합니다. 이때 오류는 `OptimisticLockException` 등으로 애플리케이션에 전달됩니다.

#### 3. 핵심 알고리즘 (Validation Check 의사코드)
```text
FUNCTION Validate(T_current):
    FOR each T_active in Active_Transactions:
        // CASE 1: T_active가 커밋을 완료했고, T_current가 읽는 데이터를 썼는가?
        IF (T_active.is_committed AND intersects(T_current.read_set, T_active.write_set)):
            RETURN FALSE; 
            
        // CASE 2: T_active가 아직 활성화 중이고, 쓰기 집합이 겹치는가? (쓰기-쓰기 충돌)
        IF (T_active.is_active AND intersects(T_current.write_set, T_active.write_set)):
            RETURN FALSE;
            
    RETURN TRUE; // 충돌 없음, 커밋 가능
```

**📢 섹션 요약 비유**
OCC의 Validation 단계는 **'숙제 제출 전 베끼기 검사'**와 같습니다. 친구들과 함께 도서관에서 공부할 때, 서로 다른 주제(데이터)를 공부했다면 그냥 내면 됩니다(검증 통과). 하지만 내가 공부하는 책을 친구가 먼저 빌려가서 썼다면(충돌), 선생님(DB)은 나중에 낸 내 숙제를 반려해버립니다(Abort).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

OCC는 단순히 "락을 안 쓰는 것"이 아니라, 시스템의 부하 분산과 데이터 일관성 사이의 정교한 트레이드오프(Trade-off)를 설계하는 기술입니다.

#### 1. 심층 기술 비교: OCC vs. 2PL vs. MVCC
| 비교 항목 | **OCC (낙관적)** | **2PL (비관적)** | **MVCC (다중 버전)** |
|:---|:---|:---|:---|
| **락(Lock) 사용 시점** | 커밋 시 (논리적 충돌 확인) | 트랜잭션 시작 즉시 (명시적 Lock) | 없음 (Undo Log 활용) |
| **대기 시간 (Latency)** | 매우 낮음 (블로킹 없음) | 높음 (Lock 획득 대기 발생) | 낮음 (Non-blocking Read) |
| **충돌 처리** | **롤백 후 재시도** (CPU 소모) | 대기 및 교착상태(Deadlock) 위험 | 버전 체이닝으로 회피 |
| **적합한 환경** | **Read-heavy, Conflict 듬봄** | Write-heavy, Conflict 빈번 | Read-Intensive (대부분의 최신 DB) |
| **DB 복구 복잡도** | 로그 관리 필요 | 복구 로직 복잡 | 스냅샷 유지 비용 높음 |

*참고: **MVCC (Multi-Version Concurrency Control)**는 OCC의 개념을 확장하여, 과거의 데이터 버전을 물리적으로 보존함으로써 읽기 작업이 쓰기 작업을 방해하지 않도록 하는 현대적 구현체입니다.*

#### 2. 과목 융합 분석
- **[운영체제 (OS) & 메모리]**: OCC의 `Private Workspace` 개념은 OS의 **Copy-on-Write (COW)** 기술과 맥락을 같이합니다. 프로세스가 `fork()` 될 때 실제 메모리 페이지를 복사하지 않고 포인터만 공유하다가, 쓰기가 발생할 때 페이지를 복사하는 방식입니다. 이는 불필요한 메모리 복사 오버헤드를 줄이는 효율적인 매커니즘입니다.
- **[분산 시스템]**: 분산 환경에서의 OCC는 분산 트랜잭션 원자성을 보장하기 위해 **2PC (Two-Phase Commit)** 프로토콜과 결합됩니다. Validation 단계에서 글로벌 충돌(Global Conflict)을 감지하고, Commit 결정이 내려지면 모든 노드에 변경 사항을 전파(Broadcast)합니다.

#### 3. 충돌률에 따른 성능 메트릭스 (정량적 분석)
OCC의 성능은 충돌 확률($P_c$)에 민감하게 반응합니다.
- **$P_c < 10\%$ (Low Contention)**: 처리량이 2PL 대비 **200%~300%** 이상 증가할 수 있음.
- **$P_c > 30\%$ (High Contention)**: 재시도(Retry) 횟수가 기하급수적으로 증가하여, 오히려 2PL보다 **TPS가 급락**할 수 있음. (Thrashing 현상 발생)

**📢 섹션 요약 비유**
OCC는 **'고속도로 통행료 징수 시스템'**과 비슷합니다. 차량(트랜잭션)이 적을 때는 하이패스(무료 징수)처럼 통과 속도가 매우 빠릅니다(고성능). 하지만 출퇴근길처럼 차량이 몰리는 시간(높은 충돌률)에는 하이패스 차선에서도 인식 오류가 자주 발생해, 결국 요금소 앞에서 정차하고 재시도해야 하는 정체가 발생합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 OCC를 도입할 때는 단순히 "빠르다"는 이유만으로는 안 됩니다. 충돌이 발생했을 때의 비용(Cost of Rollback)과 재시도 로직을 어떻게 구현할지가 성공의 관건입니다.

#### 1. 실무 시나리오 및 의사결정 프로세스
**상황 A: 인스타그램 게시물 조회 (Read 99%, Write 1%)**
- **판단**: OCC 적극 추천.
- **이유**: 조회가 압도적으로 많고 수정(좋아요 등)은 빈번하지 않습니다. 충돌 시 게시물을 다시 불러오는 것이 사용자 경험(U