+++
title = "225. Undo 세그먼트 (롤백 세그먼트) - 데이터의 과거를 기억하는 곳"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 225
+++

# 225. Undo 세그먼트 (롤백 세그먼트) - 데이터의 과거를 기억하는 곳

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Undo 세그먼트는 데이터베이스의 **ACID (Atomicity, Consistency, Isolation, Durability)** 속성 중 원자성과 격리성을 보장하기 위해, DML (Data Manipulation Language) 실행 시 변경 전 데이터 이미지(Before Image)를 저장하는 **시스템 테이블스페이스 내의 전용 저장 영역**이다.
> 2. **가치**: 트랜잭션의 롤백(Rollback)을 지원하여 데이터 무결성을 지키고, MVCC (Multi-Version Concurrency Control) 환경에서 Non-blocking Read를 구현하여 데이터베이스의 **동시 처리량(Concurrency)과 읽기 일관성(Read Consistency)**을 동시에 만족시키는 핵심 매커니즘이다.
> 3. **융합**: Redo 로그가 '장애 발생 시 데이터베이스 복구(Forward Recovery)'를 담당한다면, Undo 세그먼트는 '트랜잭션 취소 및 논리적 복구(Backward Recovery)'와 '일관성된 뷰 제공'을 담당하며, 이 둘의 상호 보완적 결합을 통해 트랜잭션 관리자(Transaction Manager, TM)의 신뢰성이 완성된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
Undo 세그먼트(롤백 세그먼트)는 DBMS (Database Management System)에서 데이터 변경이 발생할 때, 변경되기 전의 원본 정보를 보관하는 특수한 저장소이다. 이는 단순한 백업이 아니라, 트랜잭션이라는 논리적 작업 단위가 "하나의 원자"처럼 취급되도록 만드는 기억 장치이다. 사용자가 실수를 하였거나 시스템 오류로 인해 작업이 중단되었을 때, 이 저장소에 있는 정보를 사용해 데이터를 직전의 안전한 상태로 되돌린다.

#### 2. 💡 비유: 시간 여행의 타임머신
데이터베이스의 테이블 데이터블록(Data Block)은 현재의 현실이지만, Undo 세그먼트는 과거의 기록을 보관하는 **'보관 창고'** 혹은 **'타임머신'**과 같다. 우리가 현재 현실을 수정하더라도, 언제든 타임머신을 타고 과거로 돌아가(ROLLBACK) 원래대로 되돌릴 수 있도록 안전장치를 해두는 것이다.

#### 3. 등장 배경 및 필요성
① **기존 한계**: 트랜잭션이 실패하거나 사용자가 취소를 요청할 때, 디스크의 데이터를 이미 덮어쓴 상태라면 원상 복구가 불가능해진다. 또한, 동시성 제어에서 Lock을 지나치게 오래 걸면 성능이 급격히 저하된다.
② **혁신적 패러다임**: 변경 전 데이터를 별도로 분리 보관함으로써, **원본 데이터의 복구 가능성**을 보장하고, Lock 없이도 과거 시점의 데이터를 읽을 수 있는 **MVCC 기반의 비차단 읽기(Non-blocking Read)** 환경을 제공하게 되었다.
③ **현재의 비즈니스 요구**: 365일 24시간 내려가지 않는(High Availability) 시스템과 대규모 트래픽 처리를 위해, Undo 데이터를 통한 읽기 일관성 제공은 선택이 아닌 필수가 되었다.

#### 4. 📢 섹션 요약 비유
마치 작가가 원고를 수정할 때, 수정하기 전의 원본을 항상 복사해 두는 장소라고 보면 된다. 수정이 마음에 들지 않으면 원본을 꺼내 붙여넣고, 독자에게는 아직 수정이 완료되지 않은 원본을 보여줌으로써, 작가의 수정 작업이 독자의 읽기 activity를 방해하지 않게 하는 것이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 매트릭스
Undo 세그먼트는 단순한 파일이 아니며, 효율적인 관리를 위해 논리적 구조를 갖는다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 (Internal Logic) | 연관 프로토콜/명령어 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Undo Header** | 세그먼트의 메타 정보 관리 | 트랜잭션 테이블(Transaction Table) 슬롯 매핑, 상태(Active/Committed) 관리 | `BEGIN TRAN` | 대장장이의 작업 대장 |
| **Undo Slot** | 개별 트랜잭션의 저장 공간 | 트랜잭션별 할당되며, 연결 리스트(Linked List) 형태로 Undo Record 연결 | Undo Chain | 작업자의 개인 작업대 |
| **Undo Record** | 변경 전 데이터의 실제 저장소 | `<UBA:Undo Block Address, SCN:Sytem Change Number, Data>` 구조 저장 | `UPDATE`, `DELETE` | 수정 전 페이지의 사본 |
| **Undo Tablespace** | 물리적 저장소 (디스크) | 데이터 딕셔너리에 의해 관리되며, Retention 기간 동안 보존됨 | `CREATE UNDO TABLESPACE` | 원본 보관 창고 건물 |

#### 2. ASCII 구조 다이어그램: Undo Chain 구조
아래는 DML 문이 실행될 때 메모리(SGA)와 디스크 사이에서 데이터가 이동하고 저장되는 흐름을 도식화한 것이다.

```text
      [ SGA (System Global Area) - Buffer Cache ]                [ Physical Disk ]
         
  Data Block (Buffer)                               Undo Segment (Buffer)        Undo Tablespace
 +------------------+                           +---------------------+       +------------------+
 | ROW 1: X = 100   |   (1) Before Image       | Undo Block # 1024   |       | Undo Datafile    |
 | ROW 2: Y = 200   | ---------------------->  | [Slot 1]            | <---- | (Retained)       |
 +------------------+   (Copy to Buffer)       | - SCN: 100012       |       +------------------
        ^                                       | - Data: X=100      |              ^
        |                                       | - RowID: 0,0       |              |
        | (2) Update Value                      +---------------------+              |
        v                                       | Undo Block # 1025   |              |
 +------------------+                           | [Slot 2]            |              | (4) DBWR
 | ROW 1: X = 500   |                           | - SCN: 100013       |              | (Write)
 +------------------+                           +---------------------+              |
        ^                                                                  |
        |                                                                  |
        | (3) Read Consistency Query                                       |
        +------------------------------------------------------------------+
                  User T2 reads X (SCN < 100013)
                  It uses Undo Record (X=100) to construct 'Past View'
```

**[다이어그램 해설]**
1.  **Before Image 복사**: 트랜잭션 T1이 `UPDATE`를 실행하면, DBMS는 먼저 기존 값(X=100)을 메모리 내 Undo Buffer 영역으로 복사한다.
2.  **데이터 변경**: 실제 데이터 블록의 버퍼 캐시는 새로운 값(X=500)으로 변경되고, 데이터 블록 헤더에는 가장 최근 Undo Record의 위치(UBA)가 기록된다.
3.  **일관성 읽기(Consistent Get)**: 이후 트랜잭션 T2가 데이터를 조회하면, DBMS는 현재 데이터 블록의 SCN(시스템 변경 번호)을 확인한다. T1이 아직 커밋되지 않았거나 T2의 조회 시점이 T1보다 이전이라면, 데이터 블록 대신 Undo Segment의 레코드(X=100)를 읽어 사용자에게 반환한다.
4.  **영구 저장**: Dirty Buffer는 주기적으로 DBWR (Database Writer) 프로세스에 의해 디스크의 데이터파일로, Undo Buffer는 Undo 테이블스페이스로 기록된다.

#### 3. 심층 동작 원리: Undo 기반의 복구 연쇄
Undo 레코드는 단순히 한 번의 변경만 저장하는 것이 아니라, 연쇄적인 수정(이전 값에 덮어쓰기)을 추적할 수 있는 연결 리스트(LinkedList) 구조를 가진다. 이를 **CR (Consistent Read) Block Construction**이라 한다.

1.  **DML 실행**: 사용자가 컬럼 값을 `A -> B`, `B -> C`로 두 번 변경했다고 가정한다.
2.  **Undo 체인 생성**:
    *   가장 최근의 Undo 레코드에는 `B` 값이 저장되고, 이전 Undo 레코드를 가리키는 포인터가 존재한다.
    *   그 이전 Undo 레코드에는 `A` 값이 저장된다.
3.  **롤백 실행 시**: `ROLLBACK` 명령이 들어오면 DBMS는 가장 최근 Undo 레코드(`B`를 가짐)를 읽어 데이터블록에 복구하고, 그 다음 포인터를 따라가 `A`를 복구하는 과정을 반복한다.

#### 4. 핵심 코드 및 수식
```sql
-- 의사 코드(Pseudo-code)로 보는 Undo 처리 과정
FUNCTION UPDATE_ROW(row_id, new_value):
    -- 1. Lock 획득 및 Undo Record 생성
    old_value = READ_FROM_DISK(row_id)
    undo_rec = CREATE_UNDO_RECORD(txn_id, row_id, old_value, current_SCN)
    WRITE_TO_UNDO_SEGMENT(undo_rec)
    
    -- 2. 데이터 변경 (Redo 로그 생성과 동시에)
    data_block = GET_BUFFER(row_id)
    data_block.value = new_value
    data_block.undo_ptr = ADDRESS_OF(undo_rec) -- 데이터 블록에 Undo 위치 기록
    data_block.last SCN = INCREMENT_SCN()
    
    RETURN SUCCESS
```

#### 5. 📢 섹션 요약 비유
이는 **'독립된 계산서'**를 작성하는 것과 같다. 데이터블록이라는 실제 장부에 바로 펜으로 수정하는 대신, 수정하기 전의 내용을 Undo 영역이라는 '별도의 계산용 종이'에 적어둔다. 나중에 수정을 취소해야 하면 그 종이를 보고 지우개로 지우고 다시 적으면 되고, 다른 사람이 장부를 볼 때는 수정 중인 내용 대신 '계산용 종이에 적힌 확정된 내용'을 보여주어 혼란을 막는 원리이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Redo vs Undo
DBMS의 안정성을 책임지는 두 로그 메커니즘의 비교 분석이다.

| 구분 | Redo Log (재실행 로그) | Undo Log (되돌림 로그/세그먼트) |
|:---|:---|:---|
| **목적** | **Durability (지속성)**: 장애 발생 시 **커밋된 데이터의 복구** | **Atomicity (원자성)**: 트랜잭션 **취소 및 일관성 제공** |
| **저장 데이터** | 변경 **후(NEXT IMAGE)**의 데이터 또는 변경 로그 (물리적/논리적) | 변경 **전(BEFORE IMAGE)**의 데이터 (논리적) |
| **방향성** | Forward Recovery (과거 -> 현재로 복원) | Backward Recovery (현재 -> 과거로 복원) |
| **성능 지표** | 디스크 I/O 집중, Sequential Write (LGWR) | 읽기 일관성 시 `CR Block` 생성 시 지연 발생 가능 |
| **공간 관리** | Circular 사용 (오버라이팅됨) | Retention 정책에 따라 유지 (되도록 Overwrite 지양) |

#### 2. 과목 융합 관점
-   **OS (Operating System)와의 관계**: OS의 **Shadow Paging** 기술과 유사하지만, DBMS는 Undo를 통해 더 효율적인 I/O를 수행한다. 또한, OS의 **Copy-on-Write** 기법이 메모리 페이지 단위로 수행되는 것과 달리, Undo는 레코드/블록 단위의 세밀한 제어를 가능하게 한다.
-   **트랜잭션 처리 (Concurrency)와의 시너지**: Lock 기반의 2PL (Two-Phase Locking) 프로토콜에서는 읽기 작업까지 Lock을 걸어야 하므로 병목이 발생한다. 하지만 Undo 세그먼트를 활용한 MVCC 모델에서는 **Writer(쓰기)와 Reader(읽기)가 서로 차단(Block)하지 않으므로**, 트랜잭션 처리량(TPS)이 획기적으로 증가한다.
-   **오버헤드 관리**: Undo 데이터의 지속적인 생성은 관리 오버헤드와 디스크 공간 부담을 준다. 따라서 **Automatic Undo Management (AUM)** 모드에서는 `UNDO_RETENTION` 파라미터를 통해 과거 데이터를 얼마나 오래 보관할지 튜닝하는 것이 중요하다.

#### 3. 📢 섹션 요약 비유
Redo와 Undo의 관계는 **'보험'과 '환불'**의 관계와 유사하다. Redo는 작업을 완료했는데 사고(장애)가 났을 때 다시 복구해주는 보험증권이라면, Undo는 작업을 진행하다가 마음이 바뀌었을 때 결제를 취소하고 돌려받을 수 있게 해주는 환불 정책이다. 이 두 가지가 모두 있어야 안심하고(ACID) 거래(트랜잭션)를 진행할 수 있다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정
**Scenario A: 대량 갱신 작업 중 공간 부족 (ORA-01555 Snapshot Too Old Error)**
-   **상황**: 배치 작업으로 인해 Undo 데이터가 폭발적으로 증가하는 와중에, 긴 조회 쿼리가 실행됨.
-   **문제**: Undo 공간이 꽉 차서 오래된 데이터가 덮어씌워지는 Overwrite가 발생.
-   **해결**:
    1.  **기술적**: `UNDO_TABLESPACE` 크기를 증설하거나, `UNDO_RETENTION` 파라미터 값을 초당 최대 Undo 생성량을 고려하여 적절히 상향 조정한다.
    2.  **운영적**: 긴 배치 작업을 조각내어 수행하거나, 업무 시간 외(야간)에 수행하여 조회 쿼리와 겹치지 않게 한다.

**Scenario B: 트랜잭션 롤백 지연 (Long Rollback Time)**
-   **상황**: 실수로 대량의 DELETE를 수행하여 10억 건을 삭제함. ROLLBACK 명령을 수행했으나 완료되지 않음.
-   **원인**: 롤백은 Undo 레코드를 읽어 역순으로 복구하는 과정이므