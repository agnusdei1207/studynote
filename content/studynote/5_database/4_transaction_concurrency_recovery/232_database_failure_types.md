+++
title = "232. 데이터베이스 장애 유형 - 트랜잭션부터 미디어 장애까지"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 232
+++

# 232. 데이터베이스 장애 유형 - 트랜잭션부터 미디어 장애까지

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스 장애(Failure)는 ACID(Transaction Properties) 특성을 위협하는 비정상 종료 사건이며, 영향 범위에 따라 논리적 오류인 **트랜잭션 장애**, 메모리 데이터 소실인 **시스템 장애**, 저장소 파괴인 **미디어 장애**로 체계화된다.
> 2. **가치**: 장애의 물리적/논리적 특성을 분석하여 ARIES(Algorithms for Recovery and Isolation Exploiting Semantics)와 같은 회복 알고리즘을 통해 **RTO (Recovery Time Objective)**와 **RPO (Recovery Point Objective)**를 수치화하고 최소화한다.
> 3. **융합**: OS의 페이지 폴트(Page Fault) 처리, 네트워크의 HA(High Availability) 클러스터링, 보안의 무결성 검증과 연결되는 데이터 무결성의 최후 방어선이다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
데이터베이스 장애란 트랜잭션(Transaction)의 원자성(Atomicity)과 지속성(Durability)을 보장할 수 없는 상태를 의미한다. 단순히 서비스가 중단되는 것을 넘어, 데이터 무결성(Integrity)이 깨지거나 영구 소실되는 치명적인 상황을 포함한다. 모든 DBMS(Database Management System)는 이러한 장애 상황을 가정하여 **로그 기반 회복(Log-based Recovery)** 기능을 필수 탑재하고 있다.

**2. 등장 배경 및 필요성**
① **기존 한계**: 데이터 양이 폭증함에 따라 파일 시스템 수준의 백업만으로는 가용성을 보장하기 어려워짐 (백업 시점과 장애 시점 사이의 데이터 유실 발생).
② **혁신적 패러다임**: **WAL (Write-Ahead Logging)** 프로토콜의 도입으로 '로그 먼저 기록, 데이터 변경 나중에' 전략을 통해 메모리 상태라도 디스크 로그를 통해 복구 가능하게 됨.
③ **현재의 비즈니스 요구**: 24/7 무중단 서비스가 요구되는 클라우드 환경에서 장애 유형을 세분화하여 밀리초 단위의 장애 복구(Failover)가 필수적임.

**3. ASCII 다이어그램: 장애 영향도 스펙트럼**
아래 다이어그램은 장애 발생 범위와 복구 난이도를 시각화한 것이다.

```text
[데이터베이스 장애 영향도 및 복구 비용 스펙트럼]

  (Local Impact)                                 (Global Impact)
       ↓                                                 ↓
       │                                                 │
  ┌────────┐      ┌──────────────┐      ┌───────────────────────┐
  │ 트랜잭션│      │   시스템 장애  │      │      미디어 장애       │
  │  장애   │      │ (System Crash)│      │    (Media Failure)   │
  └────────┘      └──────────────┘      └───────────────────────┘
       │                │                        │
       │                │                        │
  [영향 범위]      단일 트랜잭션          메모리 전체             디스크 저장소
       │                │                        │
       │                │                        │
  [주요 원인]      Deadlock, Error      정전, Kernel Panic     헤드 충돌, 디스크 파손
       │                │                        │
       │                │                        │
  [복구 자원]      메모리 내역          Redo Log (Disk)      Full Backup + Archive Log
       │                │                        │
       │                │                        │
  [복구 시간]      즉시 (ms)             빠름 (Sec)             느림 (Min ~ Hour)
       │                │                        │
       └────────────────┴────────────────────────┘
                         ▲
                         │
           복구 난이도 및 비용 (Cost) 증가 ▶
```
*(도해 해설)*: 트랜잭션 장애는 논리적 오류로 국한되어 `ROLLBACK`만으로 즉시 해결 가능하나, 오른쪽으로 갈수록 물리적 손상이 커져 로그 적용(Redo)이나 백업본 복원(Restore)이 필요하며, 복구 시간과 데이터 손실 가능성이 기하급수적으로 증가함을 보여준다.

**📢 섹션 요약 비유**: 데이터베이스 장애의 종류는 **'집무실의 사무 무결성'**을 위협하는 세 가지 사건과 같습니다. 트랜잭션 장애는 **'실수로 서류 한 장을 찢어버린 것'**(개인적으로 다시 쓰면 됨), 시스템 장애는 **'정전으로 컴퓨터가 꺼져 작성 중이던 문서가 날아간 것'**(전원 켜고 자동 저장 파일 복구), 미디어 장애는 **'화재가 나서 하드디스크 자체가 타버린 것'**(창고에 있던 예본 서류를 가져와야 함)에 비유할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 분석**
각 장애 유형은 DBMS의 계층(Layer)별로 다른 메커니즘을 트리거한다.

| 구성 요소 (Component) | 트랜잭션 장애 (Logical) | 시스템 장애 (Instance) | 미디어 장애 (Physical) |
|:---|:---|:---|:---|
| **발생 위치** | Application / Execution Engine | Buffer Pool / Cache Layer | Disk Storage / File System |
| **손실 대상** | 개념적 데이터 상태 | Dirty Page (메모리 상 변경분) | Data File & Log File |
| **탐지 메커니즘** | Exception Handling | Watchdog Timer, Heartbeat | I/O Error, ECC Check |
| **주요 복구 기법** | UNDO (Rollback) | REDO (Crash Recovery) | RESTORE + Rollforward |
| **핵심 데이터 구조** | Undo Log Segment | WAL (Redo Log) | Full Backup Set |

**2. ASCII 다이어그램: 로그 기반 회구(Recovery) 구조**
시스템 장애와 미디어 장애 복구의 핵심인 WAL 프로토콜의 동작 원리다.

```text
[ WAL(Write-Ahead Logging) 기반 장애 복구 아키텍처 ]

   ▶ 전제 조건: 변경은 로그(Log)에 먼저 기록되어야 디스크(DB File)에 반영될 수 있다.

  [1] 메모리 영역 (Volatile)                    [2] 디스크 영역 (Non-Volatile)
  ┌───────────────────────────────┐      ┌──────────────────────────────────────┐
  │         Buffer Pool            │      │          Storage Subsystem          │
  │  (Dirty Page Holding Area)     │      │                                      │
  │                                │      │  ┌──────────┐      ┌──────────────┐ │
  │  ┌────────┐   ┌────────┐      │      │  │ Data File│      │   Backup     │ │
  │  │Page A  │   │Page B  │ ◀──┐ │      │  │ (Main)   │      │   (Archive)  │ │
  │  │(Dirty) │   │(Clean) │    │ │      │  └──────────┘      └──────────────┘ │
  │  └────────┘   └────────┘    │ │      │          ▲                  ▲       │
  │       ▲                      │ │      │          │                  │       │
  │       │ Checkpointing        │ │      │          │                  │       │
  │       │ (Flush Dirty Pages)  │ │      │   ┌──────┴─────────┐  ┌─────┴───────┤│
  │       │                      │ └──────┼──▶│ Redo Log (WAL) │  │  Tape / Cloud││
  │       └──────────────────────┘        │   └────────────────┘  └─────────────┘│
  └───────────────────────────────┘      └──────────────────────────────────────┘
             │                                     │
             │ [Crash!]                             │ [Disaster!]
             │                                      │
  ┌──────────┴─────────────────────────────────────┴──────────────────────────┐
  │                           복구(Recovery) 수행                              │
  ├───────────────────────────────────────────────────────────────────────────┤
  │ [시스템 장애 복구]                                      │
  │ 1. Redo Log 스캔 시작 (LSN: Log Sequence Number 기준)                    │
  │ 2. Checkpoint 이후의 커밋된 트랜잭션 ▶ REDO 재반영 (데이터 파일 갱신)   │
  │ 3. Checkpoint 이후의 미커밋 트랜잭션 ▶ UNDO 처리 (Rollback)              │
  │                                                                           │
  │ [미디어 장애 복구]                                      │
  │ 1. Full Backup 복원 (Restore) to Data File                                 │
  │ 2. Archive Log 적용을 통해 시점 복구 (PITR: Point-In-Time Recovery)       │
  └───────────────────────────────────────────────────────────────────────────┘
```
*(도해 해설)*: 시스템 장애 발생 시, DBMS는 재시작 과정에서 Redo Log를 스캔한다. 체크포인트(Checkpoint) 이후의 커밋된 트랜잭션은 데이터 파일에 반영되지 않았을 수 있으므로 **Redo**를 수행하고, 커밋되지 않은 변경 사항은 **Undo**하여 일관성을 맞춘다. 미디어 장애는 데이터 파일 자체가 손상되었으므로 백업본을 먼저 복원(Restore)한 후 로그를 순차적으로 적용한다.

**3. 심층 동작 원리: ARIES 알고리즘**
실무에서 주로 사용되는 ARIES 알고리즘의 세 단계 복구 절차는 다음과 같다.
1.  **Analysis (분석)**: 로그를 순회하며 마지막 체크포인트 이후의 커밋/미커밋 트랜잭션을 식별 (`Undo List`, `Redo List` 작성).
2.  **Redo (재실행)**: Redo List에 있는 트랜잭션의 로그 레코드를 로그 순서대로 재실행하여 데이터베이스 상태를 장애 직전(또는 커밋 시점)으로 복구.
3.  **Undo (취소)**: Undo List에 있는 트랜잭션의 변경사항을 역순으로 취소(Rollback)하여 데이터베이스 일관성 회복.

**4. 핵심 알고리즘 및 메커니즘**
```sql
-- 로그 레코드의 기본 구조 (개념적)
<LSN, Prev_LSN, TransID, Type, PageID, Before_Image, After_Image>

-- 예시: UPDATE 문 실행 시 WAL 로그 기록 과정
BEGIN TRANSACTION;
-- [Log Record: Update] LSN=105, Page=42, Before='A', After='B'
UPDATE Table SET Col = 'B' WHERE Page = 42;
COMMIT; -- [Log Record: Commit] LSN=106
-- Flush Log to Disk (Force Log at Commit)
```

**📢 섹션 요약 비유**: 로그 기반 복구 시스템은 **'회계장부와 금고'**의 관계와 같습니다. 모든 거래는 즉시 금고(DB File)에 넣기 전에 **볼펜으로 회계장부(Log)에 먼저 기록**해야 합니다. 점원이 실수로 쓰러지거나(시스템 장애) 금고가 고장 나면(미디어 장애), **장부를 보고 거꾸로 더듬어 가며** 마지막 정상 상태를 복구할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 심층 비교 분석표**

| 비교 항목 | Transaction Abort | System Crash (Soft Crash) | Media Failure (Hard Crash) |
|:---|:---|:---|:---|
| **정의** | 논리적 오류로 인한 실행 중단 | 시스템 진동으로 인한 메모리 소실 | 저장 장치의 물리적 파손 |
| **영향도** | 단일 트랜잭션 (일부) | DB 인스턴스 전체 (DB Level) | 노드(Node) 전체 손실 |
| **데이터 손실** | 없음 (Atomicity 보장) | 체크포인트 이후 데이터 잠재적 손실 | 마지막 백업 이후 데이터 손실 |
| **복구 메커니즘** | `ROLLBACK` (Undo만 사용) | `CRASH RECOVERY` (Redo + Undo) | `RESTORE` (Restore + Redo) |
| **복구 자료** | Undo Log Segment | Online Redo Log | Offline Backup + Archived Log |
| **RTO (복구 시간 목표)** | 0 (즉시) | 수 초 ~ 수 분 | 수 시간 (용량 의존적) |

**2. ASCII 다이어그램: RPO/RPO 매트릭스 비교**
장애 유형에 따른 허용 가능한 데이터 손실과 복구 시간의 관계를 도식화한다.

```text
[ 장애 유형별 복구 목표 (RPO/RTO) 관계도 ]

    Data Loss (RPO)
         │
      High│                     ● Media Failure
         │                   (Restore from Tape/Cloud)
         │                  /
         │                 /
      Med│                /
         │               /     ● System Failure
         │              /     (Replay Logs)
         │             /
         │            /
       Low│          /
         │         /
         │        /
         │       /
      Zero│──────●──────────────────────
         │   Transaction Failure
         │   (Rollback in Memory)
         └────────────────────────────────────▶ Recovery Time (RTO)
          Low                                     High

  * Key Insight:
  - Transaction: RPO=0, RTO≈0 (메모리 상 연산 취소)
  - System: RPO≈0 (Log만 있다면), RPO=Seconds~Mins
  - Media: RPO=Hours (백업 주기 의존), RTO=Hours
```
*(도해 해설)*: 그래프에서 볼 수 있듯이, 시스템 장애는 로그가 남아있는 한 RPO(데이터 손실 시점)를 0에 가깝게 가져갈 수 있으나, 미디어 장애는 백업 주기에 따라 RPO가 크게 벌어질 수 있다. 이는 **PITR (Point-In-Time Recovery)** 구성의 중요성을 시사한다.

**3. 타 영역(운영체제/네트워크)과의 융합**
- **OS (Operating System)**: DBMS의 `Dirty Page` 개념은 OS의 `Page Cache`와 유사하다. 그러나 DBMS는 이중 쓰기(Double Write) 등을 통해 OS의 페이지 캐시가 가