+++
title = "243. ARIES 알고리즘 - 현대 DBMS 복구의 표준"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 243
+++

# 243. ARIES 알고리즘 - 현대 DBMS 복구의 표준

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ARIES (Algorithms for Recovery and Isolation Exploiting Semantics)는 **분석(Analysis), 재실행(Redo), 실행 취소(Undo)**의 3단계 기법과 로그 기반 복구를 통해, 시스템 충돌(Crash) 후 데이터베이스를 일관성 있는 상태로 복원하는 알고리즘이다.
> 2. **가치**: "Repeating History" 철학을 통해 커밋된 트랜잭션의 완벽한 재연을 보장하고, 더티 페이지(Dirty Page)의 비휘발성 디스크 반영 여부에 관계없이 ACID를 준수하며, 수동 개입 없이 완전 자동화된 복구를 제공한다.
> 3. **융합**: OS의 파일 시스템 로깅(File System Logging) 기법과 WAL(Write-Ahead Logging) 프로토콜을 결합하여 Oracle, IBM DB2, MSSQL 등 상용 RDBMS의 핵심 엔진으로 자리 잡았다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
ARIES는 IBM 연구소에서 개발된 알고리즘으로, 데이터베이스가 트랜잭션 처리 중 시스템 장애(Crash)나 미디어 실패(Media Failure)로 인해 중단되었을 때, 데이터베이스를 **트랜잭션 원자성(Atomicity)**과 **지속성(Durability)**을 만족하는 일관된 상태로 복구하기 위한 복구 관리자(Recovery Manager)의 표준 프로토콜입니다. 이는 단순한 로그 적용을 넘어, 버퍼 관리(Buffer Management)와 복구 로직의 고도화를 통해 성능과 정확성을 동시에 확보하는 것이 핵심 목표입니다.

**💡 비유**
ARIES는 **'블록버스터 영화 촬영 현장의 모니터링 팀'**과 같습니다. 배우가 실수를 하거나 장비가 고장 나더라도(장애), 모든 장면을 찍은 대본(로그)과 촬영 현황판(체크포인트)을 바탕으로, 마지막까지 완성된 장면은 그대로 살리고, 완성되지 않은 장면은 폐기하여 완벽한 한 편의 영화(일관된 DB 상태)를 완성해 냅니다.

**등장 배경**
1.  **기존 한계**: 초기 DBMS는 변경된 데이터 페이지를 즉시 디스크에 쓰는 Shadow Paging 기법 등을 사용하여, 복잡한 로그 관리 없이 복구를 시도했습니다. 하지만 이는 동시성 제어(Concurrency Control)와의 충돌, 그리고 잦은 디스크 I/O로 인해 성능 병목을 초래했습니다.
2.  **혁신적 패러다임**: **WAL (Write-Ahead Logging)** 프로토콜과 **Steal/No-Force 버퍼 관리 정책**이 도입되면서 성능은 비약적으로 향상되었으나, 복구 로직이 매우 복잡해졌습니다. ARIES는 이러한 복잡한 상황(로그 순서, 페이지 상태 불일치)을 체계적으로 해결하기 위해 등장했습니다.
3.  **현재의 비즈니스 요구**: 24/7 무중단 서비스가 필수인 현대 환경에서, 초 단위의 장애 시간(RTO: Recovery Time Objective)도 허용하지 않는 수준의 신뢰성을 요구하게 되었습니다. ARIES는 자동화되고 빠른 복구 속도로 이 요구를 충족시키는 산업 표준이 되었습니다.

**📢 섹션 요약 비유**
ARIES는 마치 **'고속 톨게이트의 하이패스 시스템과 사고 기록부'**를 결합한 것과 같습니다. 차량(트랜잭션)은 멈추지 않고 통과(고속 처리)하며, 사고가 발생하면 기록부(로그)를 근거로 사고 직전 상황을 정확히 복원하여 원인을 소급하고 정리합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (표)**
ARIES 복구 체계를 지탱하는 핵심 구성 요소는 다음과 같습니다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/포맷 | 비유 |
|:---|:---|:---|:---|:---|
| **Log Record** | 변경 이력의 기록 | 데이터 변경 전후 이미지 및 트랜잭션 ID 포함 | LSN 기반 오름차순 | 현장 감독의 대본 |
| **LSN (Log Sequence Number)** | 로그의 고유 주소 | 로그 레코드와 데이터 페이지에 스탬프핑하여 순서 보장 | Offset 기반 Monotonic Increase | 촬영 순서 대 번호 |
| **DPT (Dirty Page Table)** | 더티 페이지 추적 | 메모리상 변경되었으나 디스크에 안 쓴 페이지 목록 관리 | `PageID: RecLSN` 형태 | 아직 편집 중인 필름 목록 |
| **TPL (Transaction Table)** | 트랜잭션 상태 관리 | 실행 중(Active), 커밋(Committed), 종료(Aborted) 상태 저장 | `TxID: LastLSN` 형태 | 배우들의 촬영 진행 상황판 |
| **CLR (Compensation Log Record)** | Undo 로깅 | 실행 취소 작업 자체를 로그로 남겨 중복 실행 방지 | `UndoNextLSN` 포함 | "이 장면 삭제함"이라는 삭제 기록 |

**ASCII 구조 다이어그램 + 해설**

아래는 ARIES의 핵심 데이터 구조인 로그와 메모리 페이지 간의 관계를 도식화한 것입니다.

```text
[ARIES 로그 & 버퍼 관리 구조]

DISK (Stable Storage)               MEMORY (Buffer Pool)
+-------------------+             +-----------------------------+
| Log File (WAL)    |             |  Buffer Pool (DB Pages)     |
| [LSN:001] BEGIN   |             | +-------+  +-------+        |
| [LSN:002] T1: A=1 |<---+       | | Pg_A  |  | Pg_B  |        |
| [LSN:003] T2: B=2 |    | Write | |(Dirty)|  |(Dirty)|        |
| [LSN:004] T1: C=3 |    | Ahead| +-------+  +-------+        |
| [LSN:005] CLR(Undo)|   |       |      ^        ^            |
| [LSN:006] ...     |   |       |      | Pin    | Pin         |
+-------------------+   |       +-----------------------------+
                         |
          +--------------+--------------+
          | LSN (Log Sequence Number)   |
          | - Log Record의 고유 ID      |
          | - Page Header에 기록됨      |
          | - 복구 시 순서 판단 기준    |
          +-----------------------------+

```

*(해설)*
1.  **로그 파일(Log File)**은 안정 저장소(Stable Storage)에 순차적으로 기록됩니다. LSN(001->002->...)을 통해 로그의 순서가 보장됩니다.
2.  **버퍼 풀(Buffer Pool)**의 데이터 페이지는 메모리에 상주하며 변경(Update)이 발생하면 'Dirty' 상태가 됩니다.
3.  ARIES는 데이터 페이지를 디스크에 쓰기 전에, 해당 변경 사항을 로그로 먼저 기록하는 **WAL (Write-Ahead Logging)** 원칙을 따릅니다.
4.  페이지마다 가장 오래된(디스크와 다른) 로그 주소인 `PageLSN`을 가지고 있어, 복구 시 어디부터 적용해야 할지 판단합니다.

**심층 동작 원리: 3단계 페이즈 (The Three Phases)**
ARIES는 복구 시 다음 세 가지 단계를 순차적으로 수행합니다.

1.  **분석 단계 (Analysis Phase)**:
    *   로그의 끝(가장 최신 LSN)부터 역순으로 스캔하거나, 마지막 체크포인트(Checkpoint) 레코드부터 시작하여 **Dirty Page Table (DPT)**와 **Transaction Table (TPL)**을 재구성합니다.
    *   이를 통해 어떤 트랜잭션이 장애 순간 활성화 상태였는지 파악합니다.
2.  **재실행 단계 (Redo Phase)**:
    *   DPT에 있는 페이지들에 대해, 해당 페이지의 `PageLSN`보다 큰 LSN을 가진 로그 레코드를 순차적으로 재실행합니다.
    *   핵심은 **"커밋 여부와 상관없이"** 로그에 기록된 모든 변경을 디스크에 반영한다는 것입니다. 이를 통해 장애 직전의 메모리 상태를 정확히 복제(Repeating History)합니다.
3.  **실행 취소 단계 (Undo Phase)**:
    *   분석 단계에서 식별된 '실패한 트랜잭션(Loser)'의 작업을 취소합니다.
    *   로그의 끝에서부터 거슬러 올라가며Undo 작업을 수행하며, 이 과정에서 다시 장애가 발생할 것에 대비해 **CLR (Compensation Log Record)**을 생성합니다.

**핵심 알고리즘 & 코드 (의사코드)**

```python
# ARIES Redo Phase Pseudocode (Concept)
def aries_redo(log_buffer, dirty_page_table):
    # Redo의 시작점: DPT에서 가장 작은 RecLSN 찾기
    min_lsn = get_min_rec_lsn(dirty_page_table)
    
    # 로그 순차 스캔
    for record in log_buffer.scan_from(min_lsn):
        page = load_page(record.page_id)
        
        # 조건: 페이지의 LSN이 로그의 LSN보다 작아야 적용함
        # (이미 반영된 페이지는 건너뜀)
        if page.PageLSN < record.LSN:
            apply_redo(page, record)
            page.PageLSN = record.LSN
            flush_page(page) # 디스크에 기록
```

**📢 섹션 요약 비유**
이 과정은 **'정밀한 사고 현장 복원 및 수사'**입니다. ① 분석은 흩어진 증거물과 목격자 진술을 모아 현장 재구성 도면을 만드는 단계이며, ② 재실행은 도면을 보고 사고 직전까지 상황을 그대로 연기해 보는 것(Repeating History)입니다. 마지막으로 ③ 실행 취소는 재연 과정에서 발견된 범법 행위(미완료 트랜잭션)만을 선별적으로 처분하여 정상적인 상태로 되돌리는 마무리 수사입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: 휘발성 vs 비휘발성 안정성**
ARIES의 정책을 대표적인 복구 정책과 비교 분석합니다.

| 비교 항목 | ARIES (Steal + No-Force) | Conservative (No-Steal + Force) | Shadow Paging |
|:---|:---|:---|:---|
| **버퍼 정책** | **Steal**: 미커밋 데이터도 디스크로 갱신 가능<br>**No-Force**: 커밋 시 즉시 디스크 쓰기 불필요 | **No-Steal**: 커밋 전까지 메모리 유지<br>**Force**: 커밋 시 즉시 디스크 반영 | 복제본 생성 후 변경 |
| **복구 복잡도** | 높음 (Undo/Redo 로직 필요) | 낮음 (Undo만 필요 or 로그 불필요) | 매우 낮음 (이전 버전으로 스왑) |
| **성능 (Concurrency)**| **최상** (버퍼 풀 자유로움) | 낮음 (버퍼 풀 부족 유발) | 매우 낮음 (페이지 복사 오버헤드) |
| **주요 용도** | **일반적인 고성능 RDBMS** | 간단한 임베디드 DB | 과거 DB, 간단한 파일 시스템 |

**과목 융합 관점**
1.  **OS (Operating System)와의 융합**:
    *   ARIES의 WAL 기법은 OS의 **파일 시스템 저널링(Journaling)**이나 **복사 오류 쓰기(COW: Copy-On-Write)**의 기반이 됩니다. 특히 리눅스의 ext4나 LVM(LVM(Logical Volume Manager) Snapshost)의 스냅샷 기능은 ARIES의 로그 기반 복구 아이디어를 차용하고 있습니다.
2.  **분산 시스템(Distributed System)과의 시너지**:
    *   분산 DB 환경에서의 **2단계 커밋(2PC, Two-Phase Commit)** 프로토콜의 각 참여자(Participant)는 개별적으로 ARIES 로직을 수행하여 로컬 장애에 대비합니다. 글로벌 트랜잭션의 원자성을 보장하기 위해 ARIES의 정확한 로그 기록은 필수적입니다.
    *   반면, 분산 환경에서의 복구(Replication Recovery)는 네트워크 파티션 문제로 인해 ARIES만으로는 부족하며, **Paxos/Raft** 합의 알고리즘과 결합된 로그 복제 방식이 요구됩니다.

**📢 섹션 요약 비유**
ARIES는 **'복잡한 기어박스가 장착된 스포츠카'**와 같습니다. 단순한 자동차(보수적 복구)는 속도가 느리지만 고장 나기 쉽지 않은 반면, ARIES는 복잡한 기어(복구 로직)를 가졌기에 운전(개발/운영)이 어려울 수 있지만, 최고의 속도(동시성)와 안전성을 동시에 제공하는 F1 머신입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**
1.  **시나리오: 대용량 트랜잭션 처리 중 전원 정전**
    *   **상황**: 배치 작업 중 100만 건의 데이터를 수정하던 중 서버가 꺼짐. 메모리(DRAM) 상의 더티 페이지는 모두 사라짐.
    *   **ARIES 판단**: 전원이 들어오면 DBMS는 시작과 함께 Redo Log를 스캔. 디스크의 페이지보다 나중에 생성된 로그를 찾아 수정 사항을 취소소하지 않고 다시 반영. 이후 커밋되지 않은 배치 작업 내역을 Undo 로그를 통해 롤백.
    *   **결과**: 데이터 0손실, 일관된 상태로 복구.
2.  **시나리오: 하드웨어 오류로 인한 티어(Torn) 페이지 발생**
    *   **상황**: 디스