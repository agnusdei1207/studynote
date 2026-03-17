+++
title = "236. WAL (Write-Ahead Logging) 프로토콜 - 데이터베이스 생존의 제1원칙"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 236
+++

# 236. WAL (Write-Ahead Logging) 프로토콜 - 데이터베이스 생존의 제1원칙

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: WAL (Write-Ahead Logging)은 트랜잭션 처리 시 데이터 블록을 비휘발성 저장소에 기록하기 전에, 변경 사항을 로그 형태로 먼저 기록하여 **원자성(Atomicity)과 내구성(Durability)**을 보장하는 데이터베이스 회복 복구의 핵심 프로토콜이다.
> 2. **가치**: 무거운 랜덤 디스크 I/O(Random I/O)를 가벼운 순차 I/O(Sequential I/O)로 치환하여 트랜잭션 지연 시간(Latency)을 획기적으로 단축하며, 시스템 장애 발생 시 데이터 무결성을 유지한다.
> 3. **융합**: OS (Operating System)의 버퍼 캐시 및 커널 분산 페이지 캐시(Dirty Page Writeback) 메커니즘과 연동되어, 컴퓨터 구조(CA)의 저장 장장치 계층 구조를 기반으로 최적의 성능을 설계한다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
WAL (Write-Ahead Logging) 프로토콜은 "변경될 데이터의 영향(After-Image)을 로그에 먼저 기록한 후, 실제 데이터 페이지를 디스크에 반영한다"는 원칙을 의미합니다. 이는 데이터베이스가 **ACID (Atomicity, Consistency, Isolation, Durability)** 속성을 준수하기 위해 반드시 필요한 구조적 제약 조건입니다. WAL을 통해 DBMS (Database Management System)는 트랜잭션 커밋 시점에 데이터 파일 전체를 디스크에 쓰는 비효율을 제거하고, 로그 파일(Log File)에 대한 **fsync()** 시스템 콜 한 번만으로 영속성을 확보합니다.

#### 등장 배경: ① 기존 한계 → ② 혁신적 패러다임 → ③ 현재 요구
1.  **기존 한계**: 디스크는 섹터(Sector) 단위로 데이터를读写하며, 특히 데이터 파일의 임의 위치에 기록하는 랜덤 액세스는 **HDD (Hard Disk Drive)**의 헤드 이동(Seek Time)을 유발하여 성능 병목을 초래합니다.
2.  **혁신적 패러다임**: 로그는 항상 파일의 끝부분(Append)에만 순차적으로 기록되므로, 쓰기 위치가 고정되어 있습니다. 이를 이용해 '로그 먼저 기록 -> 나중에 데이터 반영'이라는 비동기적 전략을 수립하여 동시성 처리량(Throughput)을 극대화했습니다.
3.  **현재의 비즈니스 요구**: 24시간 365일 중단 없는 서비스(24/7 Non-stop Service) 요구사항이 증가함에 따라, 장애 발생 직전 시점으로의 복구 시간을 최소화하고(RPO: Recovery Point Objective 0에 근접), 데이터베이스 버퍼 관리의 효율성을 높이는 필수 기술로 자리 잡았습니다.

#### 💡 핵심 비유
> WAL은 **"음식점 주방에서 주문서(로그)를 먼저 걸고, 요리가 다 되면 나중에 바치는 것"**과 같습니다. 주문서(로그) 걸이만 완료되면 손님(트랜잭션)에게는 "주문 완료(Commit)"라는 확신을 줄 수 있습니다. 실제 요리(데이터 기록)가 늦게 완성되더라도 주문서가 남아 있으니, 주방장이 쓰러지더라도(장애) 주문서를 보고 다시 요리(복구)할 수 있습니다.

#### 📢 섹션 요약 비유
> **고속도로의 무선 통행료 징수 시스템과 같습니다.** 차량(데이터)이 일일이 정차해서 통행료를 내는(랜덤 I/O) 대신, 차량 번호(로그)만 찍히면 무사 통과시키고(Commit), 나중에 관리 센터에서 한꺼번에 정산하는(Checkpoint) 방식으로 병목을 해결합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 연관 프로토콜/용어 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Log Buffer** (메모리) | 로그 기록을 위한 메모리 공간 | 변경 로그를 일단 모아두었다가 특정 크기나 시간마다 디스크로 플러시 | `fsync`, OS Cache | 손님의 임시 주문 메모지 |
| **Redo Log File** (디스크) | 비휘발성 로그 저장소 | 순차 기록(Sequential Write)만 수행하며 랜덤 I/O를 회피 | WAL Protocol, Append Only | 영구 보관되는 주문 대장 |
| **Buffer Pool** (메모리) | 데이터 페이지 캐시 | 실제 데이터 페이지를 메모리에 로드하여 수정, **Dirty Page** 생성 | LRU Algorithm | 조리대 / 재료 보관함 |
| **Data File** (디스크) | 실제 데이터 저장소 | Checkpoint 이벤트 시 Buffer Pool의 Dirty Page를 기록 | Page I/O | 완성된 요리가 나가는 식탁 |
| **LSN** (Log Sequence Number) | 로그 순서 보장 번호 | 로그 레코드에 부여하는 monotonic increasing number (예: `0x1A2B`) | Checkpoint LSN | 주문 순서 번호표 |

#### WAL 기반 트랜잭션 처리 흐름 (아키텍처)

아래는 사용자의 `UPDATE` 요청부터 디스크 반영까지의 전체 생애 주기(Lifecycle)를 도식화한 것입니다.

```text
[T Phase: Transaction Execution & WAL Protocol Flow]

    Client Request
         │
         ▼
┌───────────────────────────────────────────────────────────┐
│  1. Parsing & Execution (MySQL/PostgreSQL Engine)         │
│     - Query 실행 계획 수립                                 │
└───────────────────────┬───────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│  2. Log Buffer (Volatile Memory)                          │
│     ┌─────────────────────────────────────────┐           │
│     │ [REDO LOG] LSN:1001 | TID:50 | Page:5   │           │
│     │ "Col A 변경: 10 -> 20"                  │ ◀── 기록   │
│     └─────────────────────────────────────────┘           │
└───────────────────────┬───────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│  3. Buffer Pool (Data Page Cache)                         │
│     ┌──────────────────┐    ┌──────────────────┐          │
│     │ Data Page (Dirty)│    │ Index Page      │          │
│     │ (Modified)       │    │ (Updated)       │          │
│     └──────────────────┘    └──────────────────┘          │
└───────────────────────┬───────────────────────────────────┘
                        │
                        ▼
         [ COMMIT Command Issued ] ◀── 사용자 입력
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│  4. WAL Protocol Enforcement (Strict Rule)                │
│     ▶ Log Buffer → Disk (Redo Log) File                  │
│     ▶ System Call: fsync(file_descriptor)                │
│     ⚠️  "로그가 디스크에 안 찍히면 절대 커밋 성공 응답 안 함" │
└───────────────────────┬───────────────────────────────────┘
                        │
                  [SUCCESS] ◀── 사용자에게 반환
                        │
                        │ (Background / Deferred)
                        ▼
┌───────────────────────────────────────────────────────────┐
│  5. Checkpoint Process (Async Writeback)                  │
│     ▶ Dirty Page → Data File (Real Data)                 │
│     ▶ Writes the actual heavy data blocks                 │
└───────────────────────────────────────────────────────────┘
```

#### 심층 동작 원리 및 수식
WAL의 정확성은 **LSN (Log Sequence Number)**에 의해 보장됩니다. 복구 관리자(Recovery Manager)는 다음의 불변 법칙을 따릅니다.

1.  **로그 선행 기록 법칙 (WAL Rule)**:
    `LSN(Page) >= LSN(Redo Log)` 이어야 데이터 페이지를 디스크에 쓸 수 있습니다.
    *의미: 페이지에 있는 변경 내용을 담은 로그가 먼저 디스크에 있어야 한다.*

2.  **지연 쓰기 (Steal & Force Policy)**:
    *   **Steal**: 트랜잭션이 커밋되지 않았더라도, 해당 페이지를 디스크에 쓸 수 있다 (단, 로그는 먼저 기록). → 버퍼 부족 문제 해결.
    *   **Force**: 트랜잭션 커밋 시, 로그는 반드시 디스크로 플러시된다. → 내구성 보장.

#### 핵심 코드 로직 (Pseudo-Code)
```c
// DBMS Kernel Internal Logic
void commit_transaction(Transaction *txn) {
    // 1. 로그 버퍼에 로그 레코드 생성 (LSN 할당)
    LogRecord *record = create_log_record(txn);
    
    // 2. 로그 버퍼 -> 로그 파일 (디스크)로 강제 기록
    // fsync는 디스크 컨트롤러까지 완료를 보장함
    if (fsync(log_file_fd) != 0) {
        return FAILURE; 
    }
    
    // 3. 여기서부터 트랜잭션은 "Committed" 상태로 간주됨
    txn->state = COMMITTED;
    notify_client("Commit Success");
    
    // 4. 데이터 파일(Data File)에 대한 기록은 백그라운드 스레드가
    //    Checkpoint 시점에 비동기적으로 처리함.
}
```

#### 📢 섹션 요약 비유
> **"현금 증서(Cash Receipt) 발급기"**와 같습니다. 고객(트랜잭션)이 돈을 내면, 은행원(DB)이 당장 통장에 정확히 입금 처리(데이터 기록)를 완료하지 않았더라도, 일단 영수증(로그)을 소급하여 발급해줍니다. 나중에 은행 정산 시간(Checkpoint)에 장부를 정리하면 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: WAL vs No-WAL (Shadow Paging)

| 구분 | WAL (Write-Ahead Logging) | Shadow Paging (그림자 페이지 기법) | 비고 |
|:---|:---|:---|:---|
| **쓰기 방식** | In-place Update (제자리 수정) | Out-of-place Update (새 위치 복사 후 수정) | |
| **성능 특성** | 로그는 순차 기록(빠름) <br> 데이터는 랜덤 기록(느림) | 수정 시마다 전체 페이지 복사 발생 <br> -> 쓰기 폭증 | WAL이 쓰기 유리 |
| **복구 복잡도** | Redo + Undo 로그 필요 <br> 복잡하지만 유연함 | 마지막 유효 페이지 포인터만 가리키면 됨 <br> 구조 단순 | |
| **용량 효율성** | 로그 파일(Circular)으로 관리 | 오래된 페이지 버전 관리 어려움( fragmentation) | |
| **주요 사용처** | **MySQL InnoDB, PostgreSQL, Oracle** 등 대부분의 현대 DBMS | SQLite, Git (Object Store), 일부 임베디드 DB | |

#### 과목 융합 관점
1.  **운영체제 (OS)와의 시너지**:
    *   WAL의 성능은 OS의 **Buffer Cache** 및 **fsync()** 시스템 콜의 효율에 종속적입니다. 리눅스 커널의 I/O 스케줄러(CFQ, Deadline, Noop)가 로그 디스크의 순차 쓰기 얼마나 잘 보장해주느냐가 DB 전체 성능을 좌우합니다.
2.  **컴퓨터 구조 (CA)와의 시너지**:
    *   **NVRAM (Non-Volatile Random Access Memory)**의 등장이 WAL의 패러다임을 흔들고 있습니다. 메모리가 비휘발성이라면 굳이 디스크에 로그를 남길 필요 없이, 메모리에 데이터를 쓰는 것만으로도 영속성을 확보할 수 있게 되어 WAL 로직이 대폭 단순화될 수 있습니다.

#### 정량적 성능 지표 (가상의 벤치마크)
*   **로그 쓰기 (Sequential)**: 200 MB/s (HDD 기준)
*   **데이터 쓰기 (Random)**: 2 MB/s (HDD, Seek Time 포함)
*   **결론**: WAL을 통해 사용자는 200 MB/s의 성능으로 응답을 받고, 2 MB/s의 느린 작업은 백그라운드로 떠넘기는 **"속도의 사기"**를 부리는 셈입니다.

#### 📢 섹션 요약 비유
> **"일기장과 SNS 피드"**의 차이와 같습니다. Shadow Paging은 일기를 쓸 때마다 책 전체를 다시 베껴 써야 해서(전체 복사) 느리지만, WAL은 SNS에 피드를 올리는 것처럼(로그 추가) 내 이력을 계속 추가만 하면 되므로 훨씬 효율적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 실무 시나리오 및 의사결정 프로세스

1.  **시나리오 A: 이중화(Dual Write) 지연 병목**
    *   **문제**: WAL 로그를 `Disk A`와 `Disk B`에 동기식으로 이중화(Mirroring)하면 커밋 시간이 디스크 2회 분량 소요.
    *   **해결**: `Group Commit` 기법 도입. 여러 트랜잭션의 로그를 모아서 한 번의 fsync로 처리.
    *   **결정**: 손실 허용 시간(RPO)과 응답 속도(RTO)를 교환하여 NVRAM나 반도체 디스크(SSD)를 활용한 ZIL (ZFS Intent Log) 영역 배치.

2.  **시나리오 B: 데이터베이스 크래시(Crash) 복구**
    *   **상황**: 전원 차단 후 재부팅 시 `Dirty Page`는 사라지고 `Redo Log`만 존재.
    *   **복구 로직**:
        1.  `Checkpoint LSN` 이후의 로그 스캔.
        2.  `LS