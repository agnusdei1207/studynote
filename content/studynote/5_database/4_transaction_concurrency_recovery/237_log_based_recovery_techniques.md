+++
title = "237. 로그 기반 회복 기법 - 변경의 모든 발자취"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 237
+++

# 237. 로그 기반 회복 기법 - 변경의 모든 발자취

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로그 기반 회복(Log-based Recovery)은 데이터베이스의 **ACID(Atomicity, Consistency, Isolation, Durability)** 속성 중 원자성과 영속성을 보장하기 위해, 트랜잭션에 의한 데이터 변경 이력을 순차적으로 기록한 **로그(Log Sequence Number, LSN)**를 기반으로 장애 발생 시 데이터를 일관된 상태로 복원하는 기술이다.
> 2. **가치**: 시스템 장애(Crash) 시 메모리(Disk Buffer)上의 유실된 데이터를 복구하고, 완료되지 않은 트랜잭션을 롤백(Rollback)하여 데이터 무결성을 유지한다. 이를 통해 RPO(Recovery Point Objective)를 0에 가깝게 최소화하여 비즈니스 연속성을 확보한다.
> 3. **융합**: 운영체제(OS)의 WAL(Write-Ahead Logging) 개념과 연결되며, 분산 데이터베이스 환경에서는 2PC(Two-Phase Commit) 프로토콜과 결합하여 전역 트랜잭션의 원자성을 보장하는 핵심 기반 기술로 작동한다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 정의
로그 기반 회복 기법은 트랜잭션(Transaction)이 수행한 모든 연산의 결과를 데이터베이스 데이터 파일에 즉시 반영하는 것이 아니라, 변경 사항을 먼저 안전한 **로그 파일(Log File/Journaling)**에 기록함으로써 장애에 대비하는 방법론이다.

이 기법의 철학은 "실행 취소(Undo)와 재실행(Redo)이 가능하다면, 데이터베이스 블록에 쓰는 시점을 늦추거나 쓰기 순서를 조작해도 무결성은 유지된다"는 데 있다. 모든 변경은 **LSN(Log Sequence Number)**이라는 고유 식별자를 통해 순서가 부여되며, 이는 디스크상의 로그 레코드와 메모리상의 페이지를 연결하는 고리 역할을 한다.

#### 등장 배경
1.  **기존 한계 (Shadow Paging 등)**: 데이터 페이지를 수정할 때마다 디스크의 복사본(Shadow)을 만드는 방식은 데이터 분할(Fragmentation)이 심하고, 다중 사용자 환경에서의 동시성 제어(Concurrency Control)가 어렵다는 단점이 있었다.
2.  **혁신적 패러다임 (WAL)**: 데이터를 먼저 쓰고 로그를 나중에 쓰는 기존 방식(Lazy Logging)은 로그 기록 전 장애 발생 시 복구가 불가능했다. **로그 선행 기법(Write-Ahead Logging)**은 "로그가 디스크에 안전하게 기록되기 전까지는 해당 트랜잭션에 의해 수정된 데이터 페이지를 디스크에 쓰지 않는다"는 원칙을 도입하여 이 문제를 해결했다.
3.  **현재의 비즈니스 요구**: 24/365 가용성이 요구되는 클라우드 환경에서, 서버 장애 시 수초 내에 복구해야 하는 요구사항을 충족시키기 위해 체크포인트(Checkpoint) 간격을 최적화하고 로그 볼륨을 관리하는 고도화된 알고리즘이 필요해졌다.

#### 💡 비유
건물을 지을 때 **'시공 일지'**를 매일 매일 상세히 작성하는 것과 같습니다. 만약 중간에 지진이 나서 건물이 무너져도, 일지를 보면 "어제까지 기둥은 다 세웠고, 오늘 지붕을 올리던 중이었다"는 것을 알 수 있습니다. 그러면 지붕 공사를 다시 하거나(Redo), 잘못 세운 벽을 허물고(Undo) 다시 지을 수 있습니다.

#### 📢 섹션 요약 비유
로그 기반 회복은 **"블랙박스를 단 고속열차"**와 같습니다. 사고가 나더라도 블랙박스(로그)에 기록된 운행 기록을 분석하여 사고 직전 상태로 정확히 복원할 수 있기에, 열차(데이터베이스)는 과감하게 고속으로(즉시 갱신 등) 운행할 수 있는 용기를 얻습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
로그 기반 회복 시스템을 구성하는 핵심 모듈과 그 역할은 다음과 같다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 상세 | 관련 프로토콜/용어 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Log Manager** | 로그 버퍼 관리 및 디스크 플러시 결정 | Main Memory의 Log Buffer에 로그 레코드를 순차적 기록. 버퍼가 찼거나 특정 이벤트 발생 시 Force Log를 수행. | WAL (Write-Ahead Logging) | **공책 작성자**: 연필로 일기장에 적고, 중요할 때마다 서류함에 보관. |
| **Log Record** | 변경 정보의 단위 | `<Lsn, TxID, PageID, PrevLSN, Type, UndoInfo, RedoInfo>`로 구성된 구조체. 연결 리스트 형태로 관리되기도 함. | CLS (Compensating Log Record) | **사건 기록**: 14:05분에 A계좌에서 10만원 출금 (이전 잔액: 100만원). |
| **Buffer Manager** | 데이터 버퍼와 디스크 동기화 | Dirty Page List를 관리하며, LSN과 Page_LSN을 비교하여 플러시(Flush) 시점을 결정. | Steal/No-Force Policy | **시공 팀장**: 일지(Log) 확인 후 작업(Data) 진행 여부 결정. |
| **Recovery Manager (RM)** | 장애 시 복구 수행 | ANALYZE -> REDO -> UNDO 단계를 수행하여 데이터베이스를 일관된 상태(Consistent State)로 변환. | ARIES Algorithm | **복구 팀장**: 재해 현장에서 일지를 보고 복구 지시를 내림. |
| **Checkpoint Record** | 복구 시작점 지정 | 특정 시점에 활성 트랜셕션 리스트와 Dirty Page List를 기록하여 복구할 로그 양을 줄임. | Fuzzy Checkpoint | **이정표**: "여기서부터 검사하면 됨"을 표시한 깃발. |

#### 2. 아키텍처 및 데이터 흐름 (ASCII)
다음은 트랜잭션 수행 중 로그가 기록되고, 장애 발생 시 복구가 이루어지기까지의 흐름도이다.

```text
     [ Transaction Execution Flow ]
      (Normal Operations)

  Transaction ──▶ [ Log Buffer (Mem) ] ──▶ [ Log File (Disk) ]
      │                   │
      │ (Update)          │ (WAL Protocol)
      ▼                   ▼
 [ Data Buffer ]      [ Force Log ]
   (Dirty Page)          (Must precede
      │                  Data Write)
      │
      ▼
 [ Data File ] ◀───── (DBWR Process)
   (Disk)

     [ Recovery Flow (Post-Crash) ]

   System Restart
       │
       ▼
 [ ANALYZE Phase ] ──▶ Find Last Checkpoint (LCP)
       │                  │
       │                  ▼
       │            [ REDO Phase ]
       │            (Repeat history)
       │            from LCP to End-Log
       │                  │
       │                  ▼
       │            [ UNDO Phase ]
       └──────────────▶ (Rollback uncommitted Tx)
```

**다이어그램 해설**:
1.  **정상 동작(Normal)**: 트랜잭션은 데이터를 수정하면 `Log Buffer`에 기록한다. WAL 원칙에 따라 이 로그가 `Log File(Disk)`로 플러시되어야만 `Data Buffer`의 변경 내용이 `Data File(Disk)`로 반영될 수 있다.
2.  **분석 단계(Analyze)**: 재시작 시 복구 관리자는 가장 최근의 `Checkpoint Record`를 찾는다. 이 시점 이후의 로그만 검사하면 되므로 복구 시간이 단축된다.
3.  **재실행 단계(Redo)**: 체크포인트 이후부터 로그 파일의 끝까지 순회하며, `COMMIT`된 트랜잭션과 `UNCOMMIT`된 트랜잭션의 모든 변경 사항을 디스크에 다시 적용한다. (Redo는 "모조리 다시 함"으로 수행함으로써 중복 적용의 문제를 회피)
4.  **취소 단계(Undo)**: 아직 `COMMIT`되지 않은 트랜잭션의 로그를 역순으로 찾아가며 변경 사항을 원래대로 돌려놓는다.

#### 3. 심층 동작 원리 (ALGORITHM)
로그 기반 회복의 핵심은 로그 레코드의 **Undo/Redo 가용성**과 **실행 시점**의 결정에 있다.

1.  **로그 유형 결정**:
    *   `T0`: `<Ti, Start>`
    *   `T1`: `<Ti, Xj, V1, V2>` (Xj 항목을 V1에서 V2로 변경)
    *   `T2`: `<Ti, Commit>`
    *   `T3`: `<Ti, Abort>`

2.  **복구 로직 (ARIES 알고리즘 기반)**:
    *   **Phase 1: Analysis** (로그 스캔 -> LSN 추적)
        *   가장 최근 `Checkpoint(LSN_c)`를 찾음.
        *   `LSN_c`부터 현재까지의 로그를 스캔하며 `Undo List`(미완료 Tx)와 `Redo List`(재반영 필요 Dirty Page)를 구축.
        *   *Logic:* `IF Log.Type == Commit THEN Remove(TxID) ELSE Add(TxID)`
    *   **Phase 2: Redo** (복구)
        *   `Redo List`에 있는 페이지들의 `Page_LSN`이 로그의 `LSN`보다 작은 경우에만 해당 로그의 `New Value`를 디스크에 기록.
        *   *Logic:* `IF Page_LSN < Log_LSN THEN Write(New_Value)`, `Set Page_LSN = Log_LSN`
    *   **Phase 3: Undo** (롤백)
        *   `Undo List`에 있는 트랜잭션을 대상으로 로그를 역순(Last to First)으로 탐색.
        *   `Old Value`를 데이터 페이지에 기록하고, 이를 나타내는 `CLR(Compensating Log Record)`을 생성하여 로그에 추가. (Undo 중 장애 발생 대비)
        *   *Logic:* `Write(Old_Value)`, `Write_Log(<Ti, Xj, V_undo>)`

#### 4. 핵심 알고리즘 및 수식
복구 시간($T_{recovery}$)은 체크포인트 간격($T_{cp}$)과 로그 생성 속도($R_{log}$)에 비례한다.
$$ T_{recovery} \approx \alpha \times T_{cp} \times R_{log} + \beta \times N_{dirty} $$
(여기서 $N_{dirty}$은 더티 페이지의 수, $\alpha, \beta$는 시스템 계수)

> **Redo Logic Example (Python-style Pseudo)**:
> ```python
> def redo_phase(logs, start_lsn):
>     for log in logs: # 순차 스캔
>         if log.lsn < start_lsn: continue
>         
>         page = load_page(log.page_id)
>         # 로그에 있는 변경이 디스크에 아직 반영되지 않았다면
>         if page.page_lsn < log.lsn: 
>             apply(page, log.new_value)
>             page.page_lsn = log.lsn
>             flush(page)
> ```

#### 📢 섹션 요약 비유
로그 기반 회복의 아키텍처는 **"영상 촬영 중인 감독실"**과 같습니다. 배우(데이터)가 실수를 하거나 조명이 나가도, 감독(복구 관리자)은 찍힌 필름(로그)을 보고 "Cut! 여기서 다시 찍어(Redo)" 혹은 "이 장면은 지워(Undo)"라고 정확한 지시를 내릴 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 지연 vs 즉시 (Deferred vs Immediate)

| 구분 | 지연 갱신 (Deferred Update) | 즉시 갱신 (Immediate Update) |
|:---|:---|:---|
| **정의** | 트랜잭션이 `COMMIT`되기 전까지 데이터베이스 버퍼나 디스크에 변경을 반영하지 않고 로그만 보관하는 방식. | 트랜잭션 진행 중에 로그 기록 후 즉시 데이터베이스 버퍼에 변경을 반영하는 방식. |
| **Undo 필요성** | **불필요 (No Undo)**. Commit 전 DB가 변경되지 않았으므로 지울 것이 없음. | **필요 (Undo)**. Commit 전 장애 발생 시 변경된 값을 되돌려야 함. |
| **Redo 필요성** | **필수 (Redo)**. Commit 시점에 로그의 결과를 DB에 한번에 반영해야 하므로, 장애 시 이를 다시 수행. | **필수 (Redo)**. 메모리에 반영되었으나 디스크로 가지 못한 데이터가 있을 수 있음. |
| **주요 사용처** | 주기억장치가 한정된 구형 시스템, Read-Intensive 시스템 | **현대 범용 DBMS** (Oracle, PostgreSQL 등), 성능이 중요한 OLTP 환경 |
| **Locking** | 긴 Lock 유지 가능 (Commit 시점 해제) | 짧은 Lock 유지 유도 (Concurrency 향상) |
| **복구 복잡도** | 단순 (Undo 로직 없음) | 복잡 (CLR 및 Undo 로직 필요) |

#### 2. OS 및 파일 시스템과의 융합
로그 기반 회복은 DBMS에 국한되지 않고 OS의 파일 시스템(Journaling File System: ext4, NTFS)에서도 핵심 기술로 사용된다.
*   **Metadta Journaling**: 파일 시스템은 메타데이터(아이노드, 비트맵) 변경 사항을 저널(로그)에 먼저 기록한 후 실제 디스크에 반영한다. 이를 통해 시스템 충돌 시 fsck(File System Check) 시간을 획기적으로 단축한다.
*   **Synergy**: DB의 WAL과 OS의 Journaling이 중복으로 작동할 때 성능 저하(Double Write)가 발생할 수 있으므로, 이를 최적화하기 위한 `O_DIRECT` I/O나 ` Barricade` 같은 기술이 융합되어 사용된다.

#### 📢 섹션 요약 비유
지연 갱신은 **"시험지를 제출하기 전까지 답안지에 아무것도 안 쓰고, 붙여둔 포스트잇에만 적어두