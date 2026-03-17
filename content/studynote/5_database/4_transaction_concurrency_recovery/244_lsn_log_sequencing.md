+++
title = "244. LSN (Log Sequence Number) - 데이터의 시간표"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 244
+++

# 244. LSN (Log Sequence Number) - 데이터의 시간표

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **LSN (Log Sequence Number)**은 트랜잭션 로그의 **순차성**을 보장하기 위해 로그 레코드마다 부여되는 단조 증가하는 유일 식별자(Unique Identifier)로, 데이터베이스의 시간 축(Temporal Axis)을 논리적으로 구현한 것이다.
> 2. **가치**: 시스템 장애 시 **ARIES (Algorithms for Recovery and Isolation Exploiting Semantics)**와 같은 복구 알고리즘에서 Redo(재수행)와 Undo(취소)의 범위를 결정하는 핵심 지표이며, **WAL (Write-Ahead Logging)** 프로토콜의 충실도를 검증하는 절대적 기준이 된다.
> 3. **융합**: OS의 파일 시스템 오프셋, 저장 장치의 물리적 블록 주소와 연계되어 로그 버퍼(Log Buffer)의 관리와 디스크 동기화(Sync) 효율성을 결정짓는 버퍼 관리자(Buffer Manager)의 핵심 파라미터로 작동한다.

---

### Ⅰ. 개요 (Context & Background) - [600자+]

**LSN (Log Sequence Number)**은 데이터베이스 복구 매커니즘의 기초가 되는 논리적 시계(Logical Clock)이다. 단순히 증가하는 숫자가 아니라, 트랜잭션이 데이터를 수정한 순서를 기록하여, 시스템이 다운되더라도 마지막 정상 상태로 되돌릴 수 있게 하는 "데이터의 시간표" 역할을 수행한다.

**💡 비유: 공사 현장의 안전 검토 도장**
건물을 지을 때, 각 공정(벽돌 쌓기, 배관, 전기 등)이 완료될 때마다 감독관이 공사 일지에 번호를 순서대로 기록하고 벽에도 같은 번호를 붙인다. 만약 공사 중단 사고가 발생하면, 복구 반장은 벽에 붙은 번호와 일지의 마지막 번호를 대조해 "어디까지 다시 지어야 할지(100번)" 혹은 "잘못 지어진 부분을 허물어야 할지(150번)"를 즉시 파악한다.

**등장 배경 및 필요성**
① **기존 한계**: 초기 데이터베이스는 시스템 충돌 시 모든 데이터를 덤프(Dump)했다가 다시 로드하는 방식을 사용했으나, 데이터가 테라바이트(TB) 단위로 커지면서 복구 시간이 수시간에서 수일로 증가하는 문제가 발생했다.
② **혁신적 패러다임**: 로그 순차 번호를 도입하여, 디스크에 쓰이지 않은 메모리 데이터(Dirty Page)만 로그를 통해 재연(Replay)함으로써 복구 시간을 획기적으로 단축하는 **로그 기반 복구(Log-based Recovery)** 방식이 도입되었다.
③ **현재의 비즈니스 요구**: 365일 24시간 내내 멈추지 않는 금융 거래나 항공 예약 시스템에서는 장애 발생 후 수초 내에 서비스를 재개해야 하므로, LSN을 활용한 정밀한 복구가 필수적이다.

**📢 섹션 요약 비유**:
LSN은 **'복잡한 철도 운행 시스템의 열차 번호'**와 같습니다. 철도 제어 센터는 어느 열차가 어디서 충돌했는지가 아니라, "1000번 열차가 마지막으로 통과한 시점"을 앎으로써, 그 뒤에 오는 모든 열차에 대해 출발 순서를 재조정하고 안전하게 운행을 재개할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,200자+]

#### 1. LSN의 구성 및 데이터 구조
LSN은 단순 정수일 수도 있지만, 대규모 시스템에서는 `Log File ID` + `Offset` 등의 복합 구조를 가진다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/규칙 (Protocol) |
|:---|:---|:---|:---|
| **Log Sequence Number (LSN)** | 로그 레코드의 주소 | 트랜잭션 commit/rollback 시 할당되며 단조 증가 | WAL Protocol 준수 |
| **PageLSN** | 데이터 페이지 헤더에 저장 | 해당 페이지를 마지막으로 수정한 트랜잭션의 LSN 저장 | LSN >= PageLSN이면 Dirty Page |
| **FlushedLSN** | 로그 버퍼 관리 정보 | 디스크에 안전하게 기록된 마지막 로그 레코드의 LSN | Checkpoint 시점 업데이트 |
| **PrevLSN** | 로그 레코드 내부 링크 | 같은 트랜잭션의 이전 로그 레코드를 가리킴 | Undo 시 역추적(Backward Traversal) |

#### 2. LSN과 페이지의 상관관계 (ASCII 구조)

데이터 페이지의 무결성을 위해 페이지 헤더(Header)에는 `PageLSN`이 필수적으로 포함된다.

```text
[Log Buffer & Disk Layout]

1. Log File (Physical Disk)                2. Buffer Pool (Memory)
+-------+-------+-------+-------+          +---------------------------+
| LSN1  | LSN2  | LSN3  | LSN4  | ...      | Page A (pageLSN: LSN2)    |
| T1:Update A| |T2:Insert B| |T3:Delete C| | Page B (pageLSN: LSN4)    |
+-------+-------+-------+-------+          +---------------------------+
  ▲         ▲         ▲         ▲             ▲             ▲
  │         │         │         └─ Redo Needed(Page C > Disk)│
  │         │         └───────────┘                      │
  │         └──────────────────────┐                      │
  │                              ─┼────────────────────────┘
  │                               │  Comparison: Log.LSN vs Page.pageLSN
  └───────> FlushedLSN (LSN2)     
  (이미 디스크에 저장됨)
```

**해설**:
1.  **도입**: LSN 기반 복구의 핵심은 로그 파일에 있는 변화 기록과 실제 데이터 페이지 상태의 동기화(Synchronization) 여부를 판단하는 데 있다.
2.  **다이어그램**: 위 다이어그램은 로그 파일이 순차적으로 기록되는 와중에(1), 버퍼 풀의 페이지들이 각기 다른 시점의 LSN을 가지고 있는 상황(2)을 보여준다.
3.  **해설**: `Page A`는 `pageLSN`이 `LSN2`이고, 로그 파일 역시 `LSN2`까지 디스크(FlushedLSN)에 기록되었으므로 안전한 상태이다. 하지만 `Page B`는 메모리에서 `LSN4`로 수정되었으나, 로그 파일이 디스크에 `LSN2`까지만 기록된 상황이라면 **WAL (Write-Ahead Logging)** 원칙 위반이므로 로그를 먼저 플러시해야 한다. 복구 시에는 `LSN3`과 `LSN4` 로그를 읽어 `Page B`와 `Page C`에 재적용(Redo)하게 된다.

#### 3. 핵심 알고리즘: ARIES 복구에서의 LSN 활용

```python
# Pseudo-code for Analysis Phase (Redo Logic)
# 분석 단계: Dirty Page Table(DPT)와 Transaction Table 구축

def analyze_and_redo(log_records, checkpoint_LSN):
    current_LSN = checkpoint_LSN
    
    # 1. Analysis: LSN을 따라가며 DPT 재구성
    # (LSN 순회하며 Dirty Page 목록 업데이트)
    
    # 2. Redo Pass: 가장 오래된 Dirty Page의 RecLSN부터 시작
    oldest_dirty_LSN = min(dpt.page_rec_lsn for dpt in dirty_page_table)
    
    for record in log_records[oldest_dirty_LSN :]:
        # 조건: 해당 로그가 수정한 페이지가 현재 메모리/디스크 상태보다 
        # 최신(LSN이 큼)인 경우에만 재수행
        if record.lsn >= get_page_lsn(record.page_id):
             redo(record) # 로그에 적힌 연산 재실행
             update_page_lsn(record.page_id, record.lsn)
```

**심층 동작 원리**:
1.  **추적 (Tracing)**: 복구 관리자는 체크포인트(checkpoint) 기록부터 시작하여 로그를 순차적으로 스캔한다. 각 `LSN`을 읽으며 어떤 페이지가 더티(Dirty) 상태였는지 파악한다.
2.  **필터링 (Filtering)**: 단순히 로그를 전부 재실행하는 것이 아니다. 데이터 페이지의 `pageLSN`과 로그의 `LSN`을 비교하여, 로그의 번호가 더 클 경우에만 "이 변경은 아래로 내려가지 못했다"고 판단하고 Redo 연산을 수행한다.
3.  **동기화 (Syncing)**: 모든 Redo가 완료되면, 시스템은 트랜잭션 테이블을 확인하여 커밋되지 않은 트랜잭션을 찾아내고, 해당 로그 레코드의 `PrevLSN`을 거슬러 올라가며 Undo 작업을 수행한다.

**📢 섹션 요약 비유**:
LSN 기반 복구는 **'타임 머신 영화의 장면 스크립트'**와 같습니다. 영화가 중간에 멈췄을 때(시스템 다운), 연출가(복구 관리자)는 스크립트(LSN)를 보며 "현재 화면에 비친 배우의 위치가 50초 대본인데, 60초 대본까지 촬영했다"는 것을 확인하고, 그 격차만큼만 다시 촬영하여 완벽한 마지막 장면을 복원합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술적 비교 분석: LSN vs Timestamp vs SCN

| 비교 항목 (Criteria) | LSN (Log Sequence Number) | Timestamp (타임스탬프) | SCN (System Change Number - Oracle) |
|:---|:---|:---|:---|
| **정체성** | **물리적/논리적 로그의 순서** | 논리적 시간 (측정 단위) | 논리적 시간 (시스템 전역 단위) |
| **성격** | 저장소(LSB)의 오프셋 기반 | 시스템 클럭 혹은 논리적 카운터 | 메모리 내 증가 카운터 |
| **주요 용도** | WAL, Media Recovery, Crash Recovery | 동시성 제어(MVCC), 순서 보장 | 데이터 일관성, Replication Sync |
| **성능 영향** | 디스크 I/O와 밀접하게 연관 (Sequential Write) | 네트워크 지연 시간(Skew) 민감 | 고유 번호 할당 오버헤드 발생 가능 |
| **Granularity** | **Byte-level** (매우 세밀함) | Transaction-level | Statement-level |

#### 2. 타 영역 융합 관점

**[DB + OS] Double Buffering & File System**
OS의 파일 시스템(File System)은 블록 단위로 쓰기를 수행한다. LSN은 데이터베이스가 OS에게 쓰기 요청을 보내기 직전, 로그 파일 먼저 안전하게 기록했는지(`fsync`) 확인하는 **성능 병목 지점(Checkpoint)**이 된다. PostgreSQL의 `WAL buffer`나 Oracle의 `Log Buffer`가 `LSN`을 기준으로 OS의 `Page Cache`와 데이터를 동기화한다.

**[DB + Network] Distributed Log**
Kafka나 RabbitMQ와 같은 메시지 큐 시스템에서도 메시지의 순서를 보장하기 위해 **Offset**이라는 개념(사실상 LSN의 변형)을 사용한다. 데이터베이스의 복제(Replication) 과정에서 마스터 DB는 LSN을 슬레이브 DB로 전송하여, "나는 지금 500번까지 처리했으니, 너도 500번까지 읽어라"라고 명확히 지시한다.

**📢 섹션 요약 비유**:
LSN은 **'국제 우편의 추적 번호(Tracking Number)'**와 같습니다. 단순히 편지를 보낸 시각(Timestamp)만으로는 도착 순서를 보장할 수 없지만, 편지 처리국마다 찍히는 처리 인증 번호(LSN)를 통해, 수신자는 "10번 편지가 오지 않았는데 11번이 왔네? 문제가 생겼네"라고 정확히 판단하고 누락된 편지를 요청할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 과정

**상황 1: 데이터베이스 장애 복구 로그 분석**
- **문제**: 금융 서버가 정전으로 강제 종료됨. 재부팅 후 로그 파일(Log file)이 10GB, 데이터 파일이 1TB임.
- **의사결정**: 전체 데이터를 복구하는 것(1TB 스캔)은 수시간이 걸림.
- **LSN 활용**: 최신 체크포인트(Checkpoint) LSN을 확인하여 그 시점 이후의 로그 레코드(예: 50MB)만 스캔하고, Dirty Page Table(DPT)을 기준으로 Redo 수행. **복구 시간을 수시간에서 수분으로 단축.**

**상황 2: 복제(Replication) 지연 발생**
- **문제**: Standby DB가 Master DB를 따라가지 못하고 지연(Lag)이 발생함.
- **의사결정**: 단순 쿼리 속도 문제인지, 네트워크 대역폭 문제인지 확인 필요.
- **LSN 활용**: Master의 `Current LSN`과 Standby의 `Applied LSN` 차이(LSN Gap)를 모니터링. 만약 갭이 수백만 단위라면 **I/O 병목**으로 판단하여 디스크 성능을 업그레이드하거나 네트워크 대역폭을 늘리는 기술적 결정을 내림.

#### 2. 도입 및 운영 체크리스트

| 구분 | 체크항목 | 설명 |
|:---|:---|:---|
| **설계** | LSN 크기 및 포맷 | LSN이 `BIGINT` (8byte)인지 확인. 4byte의 경우 로그 파일 크기 제한 발생 가능. |
| **성능** | WAL 속도와 LSN 발생률 | 너무 잦은 커밋은 LSN 할당 및 로그 플러시 오버헤드 유발. Batch 처리로 LSN 할당 �