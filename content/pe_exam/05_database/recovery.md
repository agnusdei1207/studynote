+++
title = "회복 기법 (Recovery)"
date = 2025-03-01

[extra]
categories = "pe_exam-database"
+++

# 회복 기법 (Recovery)

## 핵심 인사이트 (3줄 요약)
> **장애 발생 시 데이터베이스를 일관된 상태로 복원하는 기술**. WAL(Write-Ahead Logging), 체크포인트, ARIES 알고리즘이 핵심. ACID의 D(Durability)를 보장하며 REDO/UNDO로 갱신 복구.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 회복 기법(Recovery)은 **시스템 장애, 미디어 장애, 트랜잭션 장애 등이 발생했을 때 데이터베이스를 가장 최근의 일관된 상태(Consistent State)로 복원하는 DBMS의 핵심 기능**이다. ACID의 지속성(Durability)을 보장한다.

> 💡 **비유**: 회복 기법은 **"게임 세이브 포인트"** 같아요. 보스전에서 졌다면(장애!), 마지막 세이브 포인트(체크포인트)에서 다시 시작할 수 있죠. 그리고 로그(리플레이)를 보면 무엇을 했는지 알 수 있어요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 장애 시 데이터 손실**: 정전, 하드웨어 고장, 소프트웨어 버그로 데이터 손실
2. **기술적 필요성 - ACID의 D 보장**: 커밋된 트랜잭션은 영구적이어야 함
3. **시장/산업 요구 - 비즈니스 연속성**: 금융, 통신 등에서 데이터 손실은 치명적

**핵심 목적**: **장애 후 데이터 일관성 복원**과 **커밋된 트랜잭션의 지속성 보장**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **로그 파일** | 모든 변경 기록 | UNDO/REDO 정보 | 블랙박스 |
| **버퍼 매니저** | 메모리-디스크 관리 | Dirty Page 추적 | 작업 공간 |
| **체크포인트** | 주기적 상태 저장 | 복구 시작점 | 세이브 포인트 |
| **WAL** | 로그 선행 기록 | 데이터보다 로그 먼저 | 보험 |
| **ARIES** | 표준 회복 알고리즘 | Analysis-Redo-Undo | 복구 매뉴얼 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    장애 유형별 복구 전략                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   1. 트랜잭션 장애 (Transaction Failure)                            │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  원인: 논리 오류, 데드락, 사용자 취소                        │  │
│   │  복구: ROLLBACK → UNDO만 수행                               │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   2. 시스템 장애 (System/Crash Failure)                            │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  원인: 정전, HW 고장, SW 버그 (메모리 손실)                  │  │
│   │  복구: 재시작 → REDO + UNDO                                 │  │
│   │  - REDO: 커밋됐지만 디스크에 안 쓰인 것                      │  │
│   │  - UNDO: 커밋 안 됐는데 디스크에 쓰인 것                     │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   3. 미디어 장애 (Media Failure)                                    │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  원인: 디스크 손상, 헤드 크래시                              │  │
│   │  복구: 백업 복원 → 로그로 REDO                              │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    로그 파일 구조                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   LSN (Log Sequence Number): 로그 레코드 고유 번호                 │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  LSN  │ Type      │ TID  │ Page │ Before │ After  │ UndoNxt │  │
│   ├──────┼───────────┼──────┼──────┼────────┼────────┼─────────┤  │
│   │  1   │ BEGIN     │ T1   │  -   │   -    │   -    │    -    │  │
│   │  2   │ UPDATE    │ T1   │  P1  │  A=100 │  A=150 │    -    │  │
│   │  3   │ UPDATE    │ T1   │  P2  │  B=200 │  B=250 │    -    │  │
│   │  4   │ COMMIT    │ T1   │  -   │   -    │   -    │    -    │  │
│   │  5   │ BEGIN     │ T2   │  -   │   -    │   -    │    -    │  │
│   │  6   │ UPDATE    │ T2   │  P3  │  C=300 │  C=350 │    -    │  │
│   │  7   │ CKPT      │ -    │  -   │  T2    │   -    │    -    │  │
│   │  8   │ UPDATE    │ T2   │  P4  │  D=400 │  D=450 │    -    │  │
│   │  ←───────────── 장애 발생! ────────────────→                 │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   분석 결과:                                                       │
│   - T1: COMMIT 있음 → REDO 필요                                   │
│   - T2: COMMIT 없음 → UNDO 필요                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    ARIES 알고리즘 3단계                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  1. Analysis (분석)                                          │  │
│   │  - 마지막 체크포인트에서부터 로그 순차 스캔                  │  │
│   │  - RedoLSN 결정: REDO 시작점                                │  │
│   │  - Dirty Page Table (DPT) 구성                              │  │
│   │  - Active Transaction Table (ATT) 구성                      │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  2. Redo (재실행)                                            │  │
│   │  - RedoLSN부터 로그 순차 스캔                               │  │
│   │  - 커밋된 변경 사항을 디스크에 재적용                        │  │
│   │  - 데이터베이스를 장애 직전 상태로 복원                      │  │
│   │  - 페이지 LSN과 로그 LSN 비교로 중복 방지                    │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  3. Undo (취소)                                              │  │
│   │  - ATT에 있는 미완료 트랜잭션 취소                          │  │
│   │  - 로그 역순으로 처리                                        │  │
│   │  - CLR (Compensation Log Record) 기록                       │  │
│   │  - 모든 미완료 트랜잭션이 취소될 때까지 반복                 │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 트랜잭션 실행 (로그 기록) → ② 장애 발생 → ③ Analysis → ④ Redo → ⑤ Undo → ⑥ 정상 상태 복원
```

- **1단계 - 로그 기록**: 모든 변경을 로그에 기록 (WAL 원칙)
- **2단계 - 장애 발생**: 시스템 크래시, 정전 등
- **3단계 - Analysis**: 로그 분석으로 RedoLSN, ATT, DPT 구성
- **4단계 - Redo**: 커밋된 트랜잭션의 변경을 재적용
- **5단계 - Undo**: 미완료 트랜잭션의 변경을 취소
- **6단계 - 복원 완료**: 일관된 상태로 복구

**핵심 알고리즘/공식** (해당 시 필수):

```
[WAL (Write-Ahead Logging) 원칙]
"데이터 페이지가 디스크에 쓰이기 전에, 해당 변경을 기술한 로그가 먼저 디스크에 쓰여야 한다"

필수 조건:
1. Undo Rule: 로그의 old value가 디스크에 있어야 데이터 쓰기 가능
2. Redo Rule: 커밋 전에 로그의 new value가 디스크에 있어야 함

[체크포인트 종류]
1. 고정 체크포인트 (Consistent/Sharp Checkpoint):
   - 모든 트랜잭션 중단
   - 모든 버퍼 플러시
   - 시스템 정지 → 일관된 상태 보장
   - 단점: 서비스 중단

2. 퍼지 체크포인트 (Fuzzy Checkpoint):
   - 트랜잭션 계속 실행
   - 비동기 버퍼 플러시
   - <CKPT, active_tx_list> 로그 기록
   - 실제 DBMS 사용 방식

[ARIES 핵심 원칙]
1. WAL: 로그 선행 기록
2. Repeating History: Redo로 장애 직전 상태 정확히 재현
3. Logging Undos: Undo 작업도 로깅 (CLR)

[LSN (Log Sequence Number)]
- 로그 레코드의 고유 식별자 (증가)
- PageLSN: 페이지에 적용된 마지막 로그 LSN
- RecLSN: 페이지가 마지막으로 플러시된 시점 LSN

Redo 조건: LogLSN > PageLSN (로그가 페이지보다 최신)

[백업 전략 비교]
┌────────────┬───────────┬──────────┬──────────┐
│   유형     │  시간     │  공간    │  복구    │
├────────────┼───────────┼──────────┼──────────┤
│ Full       │  느림     │  큼      │  간단    │
│ Diff       │  중간     │  중간    │  중간    │
│ Incremental│  빠름     │  작음    │  복잡    │
│ Log        │  가장 빠름│  가장 작│  PITR    │
└────────────┴───────────┴──────────┴──────────┘

RPO (Recovery Point Objective): 복구 시점 목표
RTO (Recovery Time Objective): 복구 시간 목표
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import time

class LogRecordType(Enum):
    BEGIN = "BEGIN"
    UPDATE = "UPDATE"
    COMMIT = "COMMIT"
    ABORT = "ABORT"
    CKPT = "CKPT"
    CLR = "CLR"  # Compensation Log Record
    END = "END"

@dataclass
class LogRecord:
    """로그 레코드"""
    lsn: int
    type: LogRecordType
    tx_id: str
    page_id: Optional[str] = None
    old_value: Optional[any] = None
    new_value: Optional[any] = None
    undo_next_lsn: Optional[int] = None  # CLR용
    active_txs: Optional[List[str]] = None  # CKPT용

@dataclass
class Page:
    """데이터 페이지"""
    page_id: str
    data: Dict[str, any]
    page_lsn: int = 0

@dataclass
class Transaction:
    """트랜잭션 상태"""
    tx_id: str
    state: str  # active, committed, aborted
    last_lsn: int = 0

class WALManager:
    """WAL 로그 매니저"""

    def __init__(self):
        self.log_buffer: List[LogRecord] = []
        self.log_file: List[LogRecord] = []
        self.next_lsn = 1
        self.current_transactions: Dict[str, Transaction] = {}

    def begin_transaction(self, tx_id: str) -> int:
        """트랜잭션 시작 로그"""
        lsn = self._write_log(LogRecordType.BEGIN, tx_id)
        self.current_transactions[tx_id] = Transaction(tx_id, "active", lsn)
        return lsn

    def log_update(self, tx_id: str, page_id: str,
                   old_value: any, new_value: any) -> int:
        """갱신 로그 기록"""
        lsn = self._write_log(
            LogRecordType.UPDATE, tx_id,
            page_id, old_value, new_value
        )
        if tx_id in self.current_transactions:
            self.current_transactions[tx_id].last_lsn = lsn
        return lsn

    def commit_transaction(self, tx_id: str) -> int:
        """커밋 로그"""
        lsn = self._write_log(LogRecordType.COMMIT, tx_id)
        if tx_id in self.current_transactions:
            self.current_transactions[tx_id].state = "committed"
        self.flush_log()  # 커밋 시 로그 강제 플러시
        return lsn

    def abort_transaction(self, tx_id: str) -> int:
        """중단 로그"""
        lsn = self._write_log(LogRecordType.ABORT, tx_id)
        if tx_id in self.current_transactions:
            self.current_transactions[tx_id].state = "aborted"
        return lsn

    def checkpoint(self, active_txs: List[str]) -> int:
        """체크포인트 로그"""
        lsn = self._write_log(LogRecordType.CKPT, "", active_txs=active_txs)
        return lsn

    def _write_log(self, type: LogRecordType, tx_id: str,
                   page_id: str = None, old_value: any = None,
                   new_value: any = None, **kwargs) -> int:
        """로그 기록"""
        record = LogRecord(
            lsn=self.next_lsn,
            type=type,
            tx_id=tx_id,
            page_id=page_id,
            old_value=old_value,
            new_value=new_value,
            **kwargs
        )
        self.log_buffer.append(record)
        self.next_lsn += 1
        return record.lsn

    def flush_log(self) -> None:
        """로그 버퍼를 디스크에 기록"""
        self.log_file.extend(self.log_buffer)
        self.log_buffer.clear()

class ARIESRecovery:
    """ARIES 회복 알고리즘 구현"""

    def __init__(self, log_file: List[LogRecord], pages: Dict[str, Page]):
        self.log_file = log_file
        self.pages = pages

    def recover(self) -> Tuple[Set[str], Set[str]]:
        """전체 회복 수행"""
        # 1. Analysis
        redo_lsn, att, dpt = self.analysis()

        # 2. Redo
        self.redo(redo_lsn, dpt)

        # 3. Undo
        undone = self.undo(att)

        return set(dpt.keys()), undone

    def analysis(self) -> Tuple[int, Dict[str, int], Dict[str, int]]:
        """Analysis 단계"""
        # 마지막 체크포인트 찾기
        ckpt_lsn = 0
        ckpt_active_txs = []

        for record in self.log_file:
            if record.type == LogRecordType.CKPT:
                ckpt_lsn = record.lsn
                if record.active_txs:
                    ckpt_active_txs = record.active_txs

        # ATT (Active Transaction Table): tx_id -> last_lsn
        att: Dict[str, int] = {tx: 0 for tx in ckpt_active_txs}

        # DPT (Dirty Page Table): page_id -> rec_lsn
        dpt: Dict[str, int] = {}

        # 체크포인트 이후 로그 분석
        for record in self.log_file:
            if record.lsn < ckpt_lsn:
                continue

            if record.type == LogRecordType.BEGIN:
                att[record.tx_id] = record.lsn

            elif record.type == LogRecordType.UPDATE:
                att[record.tx_id] = record.lsn
                if record.page_id and record.page_id not in dpt:
                    dpt[record.page_id] = record.lsn

            elif record.type == LogRecordType.COMMIT:
                if record.tx_id in att:
                    del att[record.tx_id]

            elif record.type == LogRecordType.ABORT:
                if record.tx_id in att:
                    del att[record.tx_id]

        # Redo 시작점 계산
        redo_lsn = ckpt_lsn if ckpt_lsn > 0 else 1
        if dpt:
            redo_lsn = min(dpt.values())

        return redo_lsn, att, dpt

    def redo(self, redo_lsn: int, dpt: Dict[str, int]) -> None:
        """Redo 단계"""
        for record in self.log_file:
            if record.lsn < redo_lsn:
                continue

            if record.type == LogRecordType.UPDATE:
                page = self.pages.get(record.page_id)
                if page:
                    # Redo 필요 조건: LogLSN > PageLSN
                    if record.lsn > page.page_lsn:
                        # 실제 갱신 수행
                        page.data['value'] = record.new_value
                        page.page_lsn = record.lsn
                        print(f"REDO: LSN {record.lsn}, Page {record.page_id}, "
                              f"Value → {record.new_value}")

    def undo(self, att: Dict[str, int]) -> Set[str]:
        """Undo 단계"""
        undone_txs = set()

        # 미완료 트랜잭션의 로그를 역순으로 처리
        for tx_id in list(att.keys()):
            print(f"\nUNDO Transaction {tx_id}:")
            last_lsn = att[tx_id]

            # 역순으로 로그 탐색
            for record in reversed(self.log_file):
                if record.tx_id != tx_id:
                    continue
                if record.lsn > last_lsn:
                    continue

                if record.type == LogRecordType.UPDATE:
                    page = self.pages.get(record.page_id)
                    if page:
                        # Undo 수행
                        page.data['value'] = record.old_value
                        print(f"  UNDO: LSN {record.lsn}, Page {record.page_id}, "
                              f"Value → {record.old_value}")

                elif record.type == LogRecordType.BEGIN:
                    undone_txs.add(tx_id)
                    break

        return undone_txs

class BufferManager:
    """버퍼 매니저 (Steal/No-FORCE 정책)"""

    def __init__(self, pages: Dict[str, Page], wal: WALManager):
        self.pages = pages
        self.wal = wal
        self.buffer: Dict[str, Page] = {}
        self.dirty_pages: Set[str] = set()

    def get_page(self, page_id: str) -> Page:
        """페이지 가져오기"""
        if page_id in self.buffer:
            return self.buffer[page_id]

        page = self.pages.get(page_id, Page(page_id, {'value': 0}))
        self.buffer[page_id] = page
        return page

    def update_page(self, tx_id: str, page_id: str,
                    old_value: any, new_value: any) -> None:
        """페이지 갱신 (로그 먼저 기록 - WAL)"""
        # 1. 로그 기록
        self.wal.log_update(tx_id, page_id, old_value, new_value)

        # 2. 버퍼의 페이지 갱신
        page = self.get_page(page_id)
        page.data['value'] = new_value
        page.page_lsn = self.wal.next_lsn - 1
        self.dirty_pages.add(page_id)

    def flush_page(self, page_id: str) -> None:
        """페이지를 디스크에 기록"""
        if page_id in self.buffer:
            page = self.buffer[page_id]
            self.pages[page_id] = page
            self.dirty_pages.discard(page_id)

    def flush_all(self) -> None:
        """모든 dirty 페이지 플러시"""
        for page_id in list(self.dirty_pages):
            self.flush_page(page_id)

# 시뮬레이션
if __name__ == "__main__":
    print("=== Database Recovery Simulation ===\n")

    # 초기화
    pages = {
        "P1": Page("P1", {"value": 100}),
        "P2": Page("P2", {"value": 200}),
        "P3": Page("P3", {"value": 300}),
    }

    wal = WALManager()
    buffer = BufferManager(pages, wal)

    # 트랜잭션 실행
    print("=== Transaction Execution ===")

    # T1: 커밋되는 트랜잭션
    wal.begin_transaction("T1")
    buffer.update_page("T1", "P1", 100, 150)
    buffer.update_page("T1", "P2", 200, 250)
    wal.commit_transaction("T1")
    print("T1: COMMITTED")

    # T2: 커밋 안 되는 트랜잭션 (장애 발생)
    wal.begin_transaction("T2")
    buffer.update_page("T2", "P3", 300, 350)
    print("T2: Active (no commit yet)")

    # 체크포인트
    wal.checkpoint(["T2"])
    print("CHECKPOINT taken")

    # T2 추가 갱신
    buffer.update_page("T2", "P1", 150, 180)
    print("T2: Updated P1")

    # 장애 발생! (로그는 디스크에 있지만, 일부 페이지는 안 쓰임)
    print("\n=== CRASH! ===")
    print(f"Log records: {len(wal.log_file)}")

    # 회복 수행
    print("\n=== ARIES Recovery ===")
    recovery = ARIESRecovery(wal.log_file, pages)
    redone, undone = recovery.recover()

    print(f"\nRecovery complete!")
    print(f"Redone pages: {redone}")
    print(f"Undone transactions: {undone}")

    print("\n=== Final State ===")
    for page_id, page in pages.items():
        print(f"{page_id}: value = {page.data['value']}")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **데이터 보호**: 장애 시 손실 방지 | **오버헤드**: 로그 기록 비용 |
| **일관성 보장**: 항상 일관된 상태로 복구 | **저장 공간**: 로그 파일 크기 |
| **무결성 유지**: 부분 완료 방지 | **복구 시간**: 대용량 DB는 시간 소요 |
| **감사 추적**: 모든 변경 이력 보존 | **복잡성**: 구현 및 운영 난이도 |

**회복 기법 비교** (필수: 최소 2개 대안):
| 비교 항목 | 지연 갱신 (Deferred) | 즉시 갱신 (Immediate) |
|---------|---------------------|----------------------|
| **로그 시점** | 커밋 시 | 실행 즉시 |
| **UNDO 필요** | X | ★ O |
| **REDO 필요** | ★ O | O |
| **로그 내용** | new 값만 | old + new 값 |
| **장점** | UNDO 불필요 | 실시간 반영 |
| **단점** | 메모리 부족 시 문제 | 복잡함 |

| 비교 항목 | ARIES | Shadow Paging |
|---------|-------|---------------|
| **복구 방식** | REDO + UNDO | 페이지 교체 |
| **성능** | ★ 높음 | 낮음 (페이지 복사) |
| **복잡도** | 높음 | 낮음 |
| **현대 DBMS** | ★ 표준 | SQLite (부분) |

> **★ 선택 기준**: 현대 DBMS는 ARIES가 사실상 표준

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융 코어뱅킹** | 동기식 로그, RPO=0 | 데이터 손실 0건 |
| **전자상거래** | 비동기식 + 주기적 체크포인트 | TPS 50% 향상, RPO 1분 |
| **로그 분석 시스템** | 증분 백업 + 로그 백업 | 복구 시간 80% 단축 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 - Oracle**: ARIES 기반 REDO/UNDO, Flashback Technology로 특정 시점 복구
- **사례 2 - PostgreSQL**: WAL 기반 PITR(Point-in-Time Recovery), 스트리밍 복제
- **사례 3 - MySQL InnoDB**: Doublewrite Buffer로 페이지 손상 방지, ARIES 변형 적용

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 로그 파일 별도 디스크 저장 (I/O 분산)
   - 체크포인트 간격 튜닝 (5~10분 권장)
   - 로그 파일 크기 관리
   - 백업과 연계한 복구 전략
2. **운영적**:
   - 정기적 복구 훈련 (DR Drill)
   - RPO/RTO SLA 정의
   - 모니터링 (로그 지연, 체크포인트)
   - 자동화된 백업 스케줄
3. **보안적**:
   - 로그 파일 암호화
   - 접근 권한 관리
   - 백업 미디어 보안
4. **경제적**:
   - 백업 저장소 비용
   - 복구 시간 비용
   - HA 구성 비용

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **로그 없이 갱신**: WAL 위반 → 장애 시 복구 불가
- ❌ **체크포인트 생략**: 복구 시간 무한 증가
- ❌ **백업 미검증**: 복구 시 백업 손상 발견
- ❌ **로그 공간 부족**: 트랜잭션 중단

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 회복 기법과 밀접하게 연관된 핵심 개념들

┌─────────────────────────────────────────────────────────────────┐
│  회복 기법 핵심 연관 개념 맵                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [트랜잭션] ←──→ [회복기법] ←──→ [백업전략]                    │
│       ↓              ↓               ↓                          │
│   [ACID]        [WAL/로그]      [HA/DR]                        │
│       ↓              ↓               ↓                          │
│   [동시성제어]  [체크포인트]   [분산복구]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **트랜잭션** | 선행 개념 | 회복의 대상 단위 | `[트랜잭션](../transaction.md)` |
| **동시성 제어** | 보완 개념 | 롤백 시 동시성 고려 | `[동시성제어](./concurrency_control.md)` |
| **분산 DB** | 확장 개념 | 분산 환경 회복 | `[분산DB](./distributed_database.md)` |
| **HA/DR** | 확장 개념 | 고가용성/재해복구 | `[HA](../06_ict_convergence/cloud/_index.md)` |
| **백업 전략** | 필수 요소 | 미디어 장애 복구 | `[백업](./recovery.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **데이터 보호** | 장애 시 손실 방지 | RPO 0~1분 |
| **복구 속도** | 빠른 서비스 재개 | RTO 5분 이내 |
| **일관성** | 항상 일관된 상태 | 데이터 정합성 100% |
| **감사** | 변경 이력 추적 | 전체 이력 보존 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: PMEM(지속성 메모리) 활용, 로그 없는(Lock-free) 회복, AI 기반 장애 예측
2. **시장 트렌드**: 클라우드 네이티브 DB의 자동 복구, 멀티 리전 DR, RPO 0 달성
3. **후속 기술**: 분산 합의 기반 회복 (Raft/Paxos), Blockchain-inspired immutability

> **결론**: 회복 기법은 데이터베이스 신뢰성의 핵심으로, ARIES 알고리즘을 기반으로 한 WAL + 체크포인트 조합이 현대 DBMS의 표준이다. RPO/RTO 요구사항에 맞는 백업-복구 전략 수립과 정기적인 복구 훈련이 필수적이다.

> **※ 참고 표준**: ARIES Paper (Mohan et al., 1992), WAL Protocol, ACID Properties

---

## 어린이를 위한 종합 설명 (필수)

**회복 기법**은(는) 마치 **"게임의 세이브 포인트"** 같아요.

RPG 게임을 해본 적 있나요? 어려운 보스전 앞에서 항상 세이브를 하죠. 그리고 보스한테 지면(장애 발생!), 마지막 세이브 포인트에서 다시 시작해요. 잃어버린 아이템도 다시 찾을 수 있죠!

데이터베이스도 마찬가지예요:
- **로그(Log)**: 내가 무엇을 했는지 기록한 "리플레이" 같은 거예요
- **체크포인트(Checkpoint)**: 정기적으로 저장하는 "세이브 포인트"예요
- **REDO**: "아, 마지막 세이브 이후에 이걸 했지!" 하고 다시 실행하는 것
- **UNDO**: "이건 실수였어, 다시 되돌리자!" 하고 취소하는 것

**WAL(Write-Ahead Logging)**은 중요한 규칙이에요:
"게임을 저장하기 전에, 무엇을 할지 먼저 적어둬라!"
그래야 뭔가 잘못돼도 기록을 보고 다시 할 수 있으니까요.

회복 기법 덕분에 정전이 나거나 컴퓨터가 고장 나도, **중요한 데이터를 잃지 않고 되찾을 수 있어요**! 🎮💾
