+++
title = "228. Read Uncommitted (레벨 0) - 성능을 위한 격리의 포기"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 228
+++

# 228. Read Uncommitted (레벨 0) - 성능을 위한 격리의 포기

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Read Uncommitted (RU)는 트랜잭션 격리 수준(Transaction Isolation Level) 중 최하위 단계로, **Dirty Read(더티 리드, 반복 불가능한 읽기 허용)**를 통해 커밋되지 않은 중간 데이터(Middle State)까지 즉시 읽는 메커니즘이다.
> 2. **가치**: ACID(Atomicity, Consistency, Isolation, Durability) 특성 중 Isolation(격리성)을 희생하여 **Lock Contention(락 경합)을 '0'에 수렴하게 만들며**, OLTP(Online Transaction Processing) 환경이 아닌 대용량 조회(OLAP)나 로그 분석 환경에서 Latency(지연 시간)를 획기적으로 단축한다.
> 3. **융합**: DBMS(Database Management System)의 동시성 제어(Concurrency Control) 기법과 밀접하게 연관되며, 비정상 종료(Crash) 시 Rollback(롤백) 복구 로직과 충돌할 수 있어 데이터 웨어하우스(Data Warehousing)의 ETL(Extract, Transform, Load) 파이프라인처럼 일관성보다 처리량(Throughput)이 중요한 특수 영역에만 적용된다.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의 및 철학**
Read Uncommitted는 ANSI/ISO SQL 표준에서 정의한 가장 낮은 격리 수준입니다. 이 모드에서는 트랜잭션 A가 데이터를 수정하고 커밋(Commit)하지 않았더라도, 트랜잭션 B가 해당 데이터를 즉시 읽을 수 있습니다.
기술적으로는 데이터를 읽을 때 **S-Lock(Shared Lock, 공유 락)**을 획득하지 않음으로써 구현됩니다. 일반적인 격리 수준에서는 '읽기' 작업조차도 다른 트랜잭션의 '쓰기' 작업과 충돌하지 않도록 공유 락을 걸지만, Read Uncommitted는 이 락 자체를 생략하여 **'방해받지 않는 읽기(Lock-free Read)'**를 실현합니다. 이는 데이터의 정확성을 담보로 하지 않고, 오로지 처리 속도와 동시성을 극대화하는 데에만 집중한 접근법입니다.

**💡 비유: 공사 중인 건물의 무단 침입**
이는 아파트가 공사 중일 때 문이 잠겨 있더라도("커밋되지 않은 상태"), 아무 방해 없이 훔쳐보고 들어가서 인테리어 상태를 확인하는 것과 같습니다. 아직 공사가 다 끝나지 않아("미확정 데이터"), 집주인이 다시 허물어버릴 수도("롤백") 있는 상태지만, 보안 요원("락 매니저")의 제지 없이 마음대로 둘러볼 수 있는 상태입니다.

**등장 배경 및 필요성**
1.  **기존 한계**: 높은 격리 수준(Repeatable Read, Serializable)에서는 엄격한 Locking으로 인해 대규모 데이터 조회 시 병목이 발생하며, 대기 시간(Wait Time)이 급증했습니다.
2.  **혁신적 패러다임**: "정확하지 않아도 괜찮은 데이터"라면 굳이 기다릴 필요가 없다는 발상입니다. 특히 통계 시스템이나 모니터링 대시보드 등, 1%의 오차보다 100배의 속도가 중요한 영역에서 등장했습니다.
3.  **현재 비즈니스 요구**: 빅데이터(Big Data) 환경에서 실시간 스트리밍 로그를 분석하거나, 초당 수만 건 이상의 TPS(Transactions Per Second)를 처리해야 하는 배치(Batch) 처리에서 락 오버헤드(Lock Overhead)를 제거하기 위해 선택적으로 사용됩니다.

**📢 섹션 요약 비유**
Read Uncommitted는 **'안전장치를 해제하고 속도 위반을 하는 레이싱카'**와 같습니다. 운전자(트랜잭션)는 신호 대기(Lock 대기) 없이 질주할 수 있지만, 사고가 나면 데이터라는 짐이 엉망이 될 위험을 감수해야 하는 구조입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 및 동원 기술 (Component Analysis)**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 관련 프로토콜/명령어 (Protocol/Command) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **데이터 패킷 (Row/Page)** | 조회 대상 | 디스크 또는 버퍼 풀(Buffer Pool)에 저장된 실제 데이터 레코드 | SELECT 쿼리 대상 | 집주인이 없는 열린 방 |
| **트랜잭션 매니저 (Transaction Manager)** | 상태 관리 | 트랜잭션의 시작, 커밋, 롤백 명령을 관리하고 LSN(Log Sequence Number) 부여 | BEGIN TRANSACTION, COMMIT, ROLLBACK | 공사 총괄 |
| **락 매니저 (Lock Manager)** | 동시성 제어 | **RU 레벨에서는 READ 작업에 대해 아무런 락(S-Lock)을 요청하지 않음** | Lock Request = NULL | 출입 통제구 (작동 중지) |
| **버퍼 매니저 (Buffer Manager)** | 메모리 관리 | 디스크 I/O를 줄이기 위해 데이터 페이지를 메모리에 캐싱 | Page Fetch | 임시 창고 |
| **로그 파일 (Transaction Log)** | 복구 관리 | 변경 사항을 기록하며, RU로 읽은 데이터가 롤백될 시 파급력을 기록 | WAL (Write-Ahead Logging) | 블랙박스 |

**Read Uncommitted 상태 전이 및 Dirty Read 시나리오**

아래 ASCII 다이어그램은 두 개의 트랜잭션(T1: 쓰기, T2: 읽기)이 동시에 실행될 때, Read Uncommitted 레벨에서 데이터가 어떻게 오염되는지를 보여줍니다.

```text
[TIME FLOW]  T1 (Writer)                 LOCK RESOURCE        T2 (Reader Under RU)
     ▼
  [T1 Start]  UPDATE User SET Money = 0  [X-Lock 획득]
     │        WHERE ID = 'KIM'           (독점 락 획득 완료)
     │
  [T1 Write]  Money: 100 -> 0            [X-Lock 유지 중]   
     │                                                       
     │                                                          [T2 Start]
     │        ┌────────────────────────────────────────────────────────┐
     │        │  🔍 T2: SELECT Money FROM User WHERE ID = 'KIM'       │
     │        │  └───────────> 👀 S-Lock(공유락) 요청 안 함!          │
     │        │                       │                              │
     ▼        ▼                       ▼                              ▼
  [T1 State]  (Memory Buffer)          (Disk)                  [T2 Read Value]
             Money = 0                                        '0'을 읽음! ✅
                                                              (커밋 안 된 값)
     │
     │        💥 ERROR! ROLLBACK!
     │        (돈이 실수로 0원이 되어버림)  [X-Lock 해제 및 복구]
     ▼
  [T1 End]   Money: 0 -> 100 (원복)     (이제 값은 다시 100원)
             
                                                                 [T2 Process]
                                                                 '돈이 0원이네?'
                                                                 😱 폐업 처리 진행...
                                                                 (실제로는 100원인데!)
```

**다이어그램 심층 해설**
1.  **X-Lock(Exclusive Lock) 지점**: T1이 데이터를 수정하면서 X-Lock을 걸었습니다. 일반적인 격리 수준에서는 T2가 이 데이터를 읽으려면 T1이 끝날 때까지 대기해야 합니다(Blocking).
2.  **S-Lock 생략 지점(핵심)**: T2는 Read Uncommitted 모드이므로, 읽기 시도를 할 때 Lock Manager에게 "잠시만 읽을 수 있게 해주세요"라고 부탁(S-Lock 요청)하지 않습니다. 그냥 무조건 읽습니다.
3.  **Dirty Read 발생**: T2는 메모리 상에만 존재하고 아직 디스크에 영구히 반영되지 않은(Commit되지 않은) '0'이라는 값을 읽어갑니다. 이후 T1이 롤백되어 다시 100이 되었지만, T2는 이미 '0'이라는 거짓 정보를 바탕으로 로직을 수행해버렸습니다.

**심층 동작 원리 및 논리 (Locking Strategy)**
Read Uncommitted의 핵심은 **No Locking on Read**입니다.
일반적인 데이터베이스 엔진(InnoDB 등)에서 읽기 작업은 기본적으로 MVCC(Multi-Version Concurrency Control)를 통해 구현되지만, 이는 높은 격리 수준에서의 얘기입니다. 낮은 격리 수준에서는 아예 락 검사 자체를 생략합니다.
```sql
-- Microsoft SQL Server 예시 (명시적 힌트 사용)
SELECT Balance FROM Accounts WITH (NOLOCK);
```
위 쿼리는 Read Uncommitted와 동일하게 작동합니다. 내부적으로 Lock Manager의 Grant Queue(승인 대기열)에 들어가지 않고, 무조건 Latest Row(최신 행)를 반환합니다. 이 과정에서 발생하는 성능 이득은 대기 시간(Wait Time)의 제거입니다.

**핵심 알고리즘: 격리 수준 판단 로직**
```text
Function OnReadRequest(Transaction T, Resource R):
    IF T.IsolationLevel == READ_UNCOMMITTED:
        # 락 확인 없이 바로 현재 버전 반환
        Return R.CurrentVersion 
    ELSE:
        # 다른 레벨은 락 확인 또는 MVCC 스냅샷 확인 필요
        AcquireLock(R, SHARED)
        Return SafeVersion(R)
```

**📢 섹션 요약 비유**
이 원리는 **'소란스러운 시장에서 귀를 막고 외치는 사람'**과 같습니다. 상대방(쓰기 트랜잭션)이 무슨 말을 하든, 혹은 그 말이 취소될지도 모르는데, 나는 그저 내 눈에 보이는 대로 즉시 받아적기만 하면 되므로, 소통의 오류보다는 기록의 속도가 중요한 상황입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**격리 수준별 기능 비교 분석표 (Technical Comparison Matrix)**

| 격리 수준 (Isolation Level) | Dirty Read 발생 여부 | Non-Repeatable Read 발생 여부 | Phantom Read 발생 여부 | 락 경합 (Lock Contention) | 성능 (Performance) | 주요 사용 용도 |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **Read Uncommitted (L0)** | **O (발생)** | **O (발생)** | **O (발생)** | **최저 (거의 없음)** | **최고** | 로그 분석, 통계 |
| Read Committed (L1) | X | O | O | 중간 | 중간 | 일반적인 웹 서비스 |
| Repeatable Read (L2) | X | X | O (MySQL는 X) | 높음 | 낮음 | 금융 거래, 재고 관리 |
| Serializable (L3) | X | X | X | 최대 (Deadlock 빈발) | 최저 | 은행 업무, 결제 시스템 |

> **참고**: 
> *   **Dirty Read**: 커밋되지 않은 데이터 읽기 (RU 특징)
> *   **Non-Repeatable Read**: 한 트랜잭션 내에서 같은 쿼리를 다시 실행했을 때 결과가 다름
> *   **Phantom Read**: 범위 검색 시 새로운 행이 나타남

**과목 융합 관점 분석 (Cross-Domain Analysis)**

1.  **운영체제(OS)와의 융합: 공유 자원과 스핀락(Spinlock)**
    *   **연관성**: 데이터베이스의 테이블(Table)이나 행(Row)은 OS 관점에서는 파일 시스템상의 **Critical Section(임계 영역)**입니다.
    *   **시너지/오버헤드**: RU는 이 임계 영역에 들어갈 때 커널 락(Kernel Lock)이나 DB 락을 걸지 않으므로, **Context Switching(문맥 교환)** 비용이 발생하지 않습니다. 반면, 데이터 정합성이 깨지면 OS 레벨에서 복구 불가능한 파일 시스템 오류로 이어질 수 있습니다.
2.  **네트워크(Network)와의 융합: TCP의 패킷 유실 vs UDP**
    *   **연관성**: 격리 수준의 차이는 네트워크 프로토콜의 선택과 유사합니다. **Read Uncommitted는 UDP(User Datagram Protocol)**와 같습니다. UDP는 데이터가 순서대로 도착하거나 도착했다는 확신이 없더라도(정합성 포기), 일단 끊김 없이 최대한 빠르게 데이터를 보내는(성능 우선) 방식입니다. 반면, Serializable은 TCP(Transmission Control Protocol)처럼 확인 절차(3-way Handshake와 유사한 Lock 과정)를 거쳐 확실한 데이터 전송을 보장합니다.
3.  **보안(Security)과의 융합: 무결성(Integrity) 위배**
    *   **연관성**: 보안의 3대 요소인 CIA(C, Confidentiality; I, Integrity; A, Availability) 중, Read Uncommitted는 **Integrity(무결성)**을 명백히 훼손합니다. 데이터가 수정 중인 상태를 노출하므로, 보안 감사(Audit) 로그가 신뢰할 수 없게 되는 치명적인 약점이 있습니다.

**📢 섹션 요약 비유**
격리 수준의 선택은 **'택배 배송 서비스의 등급'**과 같습니다. Read Uncommitted는 **'왁자지껄한 시장 바닥에 그냥 물건을 던져두고 오는 퀵 서비스'**입니다. 받는 사람(T2)이 집이 없는데도 물건을 가져갈 수도(Dirty Read) 있고, 약속된 시간에 안 올 수도 있지만, 배송비(비용)는 가장 싸고 배송 속도(Performance)는 가장 빠릅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정 프로세스**

1.  **시나리오 A: 대용량 로그 분석 시스템 (Data Warehouse)**
    *   **상황**: 매일 자정에 하루치 방문 로그(약 5억 건)를 집계하여 리포트를 생성해야 한다.
    *   **의사결정**: 집계 과정 중에 일부 트랜잭션이 롤백되어