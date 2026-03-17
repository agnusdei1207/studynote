+++
title = "235. Undo (취소) - 결자해지의 무결성"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 235
+++

# 235. Undo (취소) - 결자해지의 무결성

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Undo (취소) 로깅은 트랜잭션의 원자성(Atomicity)을 보장하기 위해, 데이터 변경 전 원본 값을 Before Image (BI) 형태로 저장해 두었다가 트랜잭션 실패 또는 Rollback 요청 시 이를 복구하는 메커니즘입니다.
> 2. **가치**: 시스템 장애(Crash) 발생 시 미완료 트랜잭션을 자동으로 소거하여 데이터 무결성을 유지하며, MVCC (Multi-Version Concurrency Control) 환경에서는 일관된 읽기(Consistent Read)를 위한 과거 데이터 버전 제공의 핵심 자원이 됩니다.
> 3. **융합**: OS의 파일 시스템 로깅(Journaling)과 응용 프로그램의 '되돌리기(Ctrl+Z)' 기능의 근간이 되는 컴퓨터 과학의 보편적 회복 기법입니다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 철학**
Undo (취소)는 DBMS (Database Management System)에서 트랜잭션 관리자(Transaction Manager)가 수행하는 가장 기초적이고 중요한 회복(Recovery) 기능입니다. 트랜잭션이 데이터베이스에 변경을 가하려 할 때, DBMS는 변경 전의 원본 값(Data Before Image)을 별도의 저장소(Undo Log Tablespace/Rollback Segment)에 기록합니다. 이는 "하든 안 하든, 실행 전 상태로 돌릴 수 있어야 한다"는 트랜잭션의 All-or-Nothing 원칙을 물리적으로 구현하는 장치입니다.

**등장 배경 및 필요성**
1.  **기존 한계**: 데이터 디스크에 직접 쓰는(In-place update) 방식은 도중 장애 발생 시 데이터를 원상 복구할 방법이 없어, 데이터 정합성이 파괴되는 치명적인 결함이 있었습니다.
2.  **혁신적 패러다임**: **WAL (Write-Ahead Logging)** 프로토콜과 결합하여, 로그(Log)를 통해 데이터 이력을 추적하고 시스템 붕괴 후에도 안전하게 상태를 되돌릴 수 있는 구조가 도입되었습니다.
3.  **현재의 비즈니스 요구**: 24/7 서비스 환경에서 장애 시 즉각적인 복구와 대규모 트래픽 처리를 위한 Non-blocking 읽기를 제공하기 위해 Undo는 필수적인 요소로 자리 잡았습니다.

**💡 비유: 건축가의 청사진 보관**
건축가가 집을 리모델링(트랜잭션)하기 전에 반드시 리모델링 '전'의 사진과 설계도(Before Image)를 안전한 금고(Undo Log)에 보관해두는 것과 같습니다. 공사 중에 벽을 잘못 허물거나 고객이 취소를 해명 명령(Rollback)이 떨어지면, 금고에 있던 설계도를 꺼내어 다시 원래대로 복구합니다.

**📢 섹션 요약 비유**: Undo는 **'타임머신의 좌표 기록부'**와 같습니다. 미래(변경 후)로 나아가기 전에 현재 시점(변경 전)의 좌표를 기록해두어, 문제가 생기면 언제든지 그 시점으로 되돌아갈 수 있게 하는 시간 여행의 핵심 기술입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**구성 요소 및 역할**

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 프로토콜/구조 | 비유 |
|:---|:---|:---|:---|:---|
| **Undo Segment** | Undo 로그가 저장되는 물리적 저장소 | 트랜잭션별 할당된 영역에 변경 전 데이터 기록 | Circular Buffer (Ring) 구조 | 리모델링 자재 보관 창고 |
| **Transaction Table** | 현재 활성화된 트랜잭션의 상태 관리 | TX ID, 상태(Active/Committed), Undo Log 포인터 관리 | 메모리 상 SGA/Buffer Pool | 공사 현판 및 진행 상황판 |
| **Before Image** | 데이터 변경 전의 원본 값 | UPDATE/DELETE 시 즉시 캡처하여 로그에 기록 | Redo-Undo Record Format | 원본 보존된 벽지 조각 |
| **Rollback Pointer** | 데이터 행(Row)이 가리키는 Undo 주소 | 데이터 페이지 헤더에 존재, 이전 버전을 추적하는 링크 역할 | Linked List Node | 과거로 향하는 내비게이션 |
| **Purge Thread** | 더 이상 필요 없는 Undo 로그 정리 | Commit 이후, 오랫동안 참조되지 않은 로그 공간 회수 | Background Task | 쓰레기 치우는 청소부 |

**Undo 로그를 활용한 Rollback 흐름**

```text
[T1 트랜잭션 UPDATE 실행 및 롤백 시나리오]

   [DATA PAGE]            [UNDO LOG SPACE]               [TX TABLE]
    B=100  (Old)   ──▶   <Slot T1>: B=100 (BI)     ──▶   <T1>: Active
        │                    ▲                         │
        │ ROLLBACK           │ Undo Apply               │ ROLLBACK
        ▼                    │                         ▼
    B=200 (New)   ◀───   (1) Read BI=100           <T1>: Aborted
                           (2) Restore to B=100
                           (3) Delete Lock

   [해설]
   1. 사용자가 UPDATE B=200 실행 -> DBMS는 B=100을 Undo Log에 기록(Undo Record Write).
   2. B 값을 200으로 변경 (Data Buffer Update).
   3. 오류 발생 또는 사용자 ROLLBACK 호출.
   4. 트랜잭션 매니저는 Undo Slot T1을 읽어 원본 값(100)을 확인.
   5. 해당 값을 다시 데이터 페이지에 덮어쓰고(Data Restore), 잠금(Lock)을 해제함으로써 완료.
```

**심층 동작 원리: Undo 기반의 복구 연쇄 작용**
1.  **로깅 단계 (Logging)**: 트랜잭션이 `UPDATE table SET A=10 WHERE A=5`를 실행하면, DBMS는 실제로 A를 10으로 바꾸기 전에 Undo Log에 `A=5`라는 정보를 기록합니다. 이때 LSN (Log Sequence Number)이 부여되어 순서가 보장됩니다.
2.  **실행 단계 (Steal Policy)**: 메모리(Dirty Page) 상의 데이터는 커밋 전이라도 디스크로 쓰일 수 있습니다(Steal). 이때 디스크에 A=10이 기록되어도, 메모리에는 A=5(Undo)가 남아있으므로 안전합니다.
3.  **롤백 단계 (Compensation)**: Rollback 시, Undo 로그의 역순(후입선출, LIFO)으로 연산을 수행합니다. 주의할 점은, 이 Rollback 작업 자체도 시스템 장애에 대비해 **CLR (Compensation Log Record)**이라는 특수한 Redo 로그를 남깁니다. 이렇게 해야 복구 중간에 다시 죽어도, 재기동 후 "이미 완료된 취소 작업임"을 알고 재시행하지 않아 무한 루프를 막을 수 있습니다.

**핵심 코드 및 논리 (Pseudo-code)**
```sql
-- 트랜잭션 시작
BEGIN TX;

-- 1. Undo 생성 로직 (내부)
// UPDATE Employees SET Salary = 5000 WHERE Id = 1;
CurrentVal = ReadFromDisk(Id=1); // 3000
WriteUndoLog(TxID, OpType="UPDATE", Key="Id=1", OldValue="3000");

-- 2. 실제 변경
DataBuffer[Id=1].Salary = 5000; 

-- 3. 롤백 요청 발생
// ROLLBACK;

-- 4. Undo 적용 로직 (내부)
OldVal = ReadUndoLog(TxID); // 3000
DataBuffer[Id=1].Salary = OldVal; // 3000으로 복구
CommitCLR(TxID); // Compensating Log Record 기록
```

**📢 섹션 요약 비유**: Undo와 Rollback의 관계는 **'언두(Undo) 테이프를 뒤로 감는 것'**과 같습니다. 영화 촬영(트랜잭션) 도중 연기가 엉망이 되었다면, 감독은 촬영된 필름(Undo Log)을 참고하여 배우들에게 "바로 이전 상태(Old Value)로 돌아가라"고 지시합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: Undo vs. Redo**

| 구분 | Undo (취소) | Redo (재수행) |
|:---|:---|:---|
| **목적** | 실패한 트랜잭션의 흔적 제거 (Rollback) | 성공한 트랜잭션의 디스크 반영 보장 (Recovery) |
| **데이터 대상** | **Before Image** (변경 전 값) | **After Image** (변경 후 값) |
| **적용 시점** | Crash Recovery 시 미완료 TX 처리 / 명시적 ROLLBACK | Crash Recovery 시 커밋된 TX 처리 / 지연된 쓰기 |
| **순서 논리** | 미래 → 현재 (마지막 변경부터 취소: LIFO) | 과거 → 미래 (가장 오래된 변경부터 재수행: FIFO) |
| **물리적 위치** | Undo Tablespace / Rollback Segments | Redo Log Buffer / Online Redo Logs |

**과목 융합 관점 분석**

1.  **OS (운영체제)와의 융합 - Journaling File System**:
    리눅스의 ext4나 Windows의 NTFS 같은 현대 파일 시스템은 'Journaling' 기술을 사용합니다. 이는 데이터 블록을 쓰기 전에 메타데이터 변경 사항을 저널(Log)에 먼저 기록하는 기법으로, DB의 Undo/Redo와 정확히 동일한 원리입니다. 파일 시스템 손상 방지를 위한 핵심이죠.
2.  **네트워크와의 융합 - Transaction Isolation Level**:
    Undo 로그는 MVCC (Multi-Version Concurrency Control)의 근간이 됩니다. 네트워크상의 다른 사용자(세션)가 데이터를 읽을 때, DB는 Undo 로그를 스캔하여 해당 트랜잭션이 시작되기 이전의 데이터 일관성 뷰(Snapshot)를 제공합니다. 이를 통해 "내가 수정하는 중에 다른 사람은 옛날 데이터를 읽게 함으로써(Non-blocking Read)" 동시성을 극대화합니다.

**아키텍처 도해: MVCC에서의 Undo 역할**

```text
[DATA BLOCK HEADER]
-----------------
| Row 1 (A=50) | <-- Rollback Ptr --------> [Undo Log 1: A=40] (End of Chain)
| Row 2 (B=20) | <-- Rollback Ptr --------> [Undo Log 2: B=10] --[Undo Log 1: B=0]
-----------------
       ▲
       │ Read Request (SELECT * FROM Table)
       │
(1) 현재 데이터 페이지(Row 1)를 읽음.
(2) 이 데이터가 TX에 의해 Lock되어 있음을 확인.
(3) Undo Segment의 Rollback Ptr을 따라감.
(4) 내 Transaction Start Time보다 이전의 Undo Record(A=40)를 찾을 때까지 반복.
(5) A=40을 사용자에게 반환.
```

**📢 섹션 요약 비유**: Undo가 Redo와 함께 작동하는 것은 **'브레이크(Undo)와 엔진(Redo)'**의 관계입니다. 엔진(Redo)은 차를 앞으로 나아가게 하고(변경 사항 영구화), 브레이크(Undo)는 차를 멈추거나 후진하게 하여(변경 사항 취소) 위험한 상황에서 차량을 안전하게 제어합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**실무 시나리오 및 의사결정**

1.  **시나리오: 긴 트랜잭션에 의한 Undo 공간 부족 (Snapshot Too Old)**
    *   **상황**: 대량의 데이터 갱신 배치 작업이 2시간 동안 진행 중입니다. 이때 다른 세션에서 과거 데이터를 읽으려 Undo Segment를 스캔했으나, Undo Retention(보존) 시간이 초과되어 공간이 재사용됨으로써 데이터가 유실된 경우.
    *   **판단**: 가용성(Availability)을 위해 Undo 공간을 자동으로 확장(Autoextend)하도록 설정하되, 물리적 디스크 한계를 고려하여 `undo_retention` 파라미터를 조정해야 합니다.
    *   **해결**: 배치 작업 중에는 일관성 읽기 요청을 줄이거나, Flashback 기능을 위해 대용량 Undo Tablespace를 별도로 할당하는 전략이 필요합니다.

2.  **시나리오: 대용량 DELETE 수행 시 과도한 Undo 생성**
    *   **상황**: 테이블 전체를 삭제(DELETE)하면 각 행마다 Undo 로그가 생성되어 Undo 공간이 순식간에 차 오르고 성능이 저하됩니다.
    *   **대안**: `TRUNCATE` 명령어 사용 (Undo 생성 없이 디스크 할당 해제) 또는 Partition Drop을 고려해야 합니다. Undo 로그를 남기지 않는 DDL(Data Definition Language) 작업을 우선 검토하는 기술적 판단이 필요합니다.

**도입 체크리스트 (DBA 관점)**

| 구분 | 항목 | 설명 |
|:---|:---|:---|
| **운영** | Undo Tablespace 크기 | 최대 트랜잭션 크기와 Retention 시간을 고려하여 충분히 할당되었는가? |
| **운영** | Undo Retention 보장 | `RETENTION GUARANTEE` 설정을 통해 Flashback Query 등이 실패하지 않도록 하는가? |
| **보안** | 민감 정보 노출 | Undo 로그에 평문으로 저장된 카드 정보 등이 접근 권한 없는 사용자에게 노출되지 않도록 암호화(TDE)되었는가? |
| **성능** | Undo Contention | 과도한 동시성으로 인해 Undo Segment 헤더에 대한 경쟁(Latch Contention)이 발생하지 않는가? |

**안티패턴 (치명적 결함 사례)**
*   **무한 롤백 지옥**: 트랜잭션을 중간에 취소했는데, 취소(Rollback)하는 작업 자체가 수행했던 작업만큼이나 오래 걸려 시스템이 멈춘 상태로 남는 경우. 예방하려면 대량 작업은 소량 단위로 Commit 하거나(Consistency 고려), 작업을 멈추는 대신 진행 상태를 유지한 후 로직을 수정하는 방법