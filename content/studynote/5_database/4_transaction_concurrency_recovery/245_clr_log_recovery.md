+++
title = "245. Compensation Log Record (CLR) - 복구의 반복 방지권"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 245
+++

# 245. Compensation Log Record (CLR) - 복구의 반복 방지권

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CLR (Compensation Log Record)은 트랜잭션의 Atomicity (원자성)을 보장하기 위한 ARIES (Algorithms for Recovery and Isolation Exploiting Semantics) 복구 알고리즘의 핵심 구성요소로, **Undo (취소) 연산 자체를 Redo (재수행) 가능한 형태의 로그 레코드로 기록하는 메커니즘**입니다.
> 2. **가치**: 복구(Recovery) 도중 2차 장애(Crash)가 발생하더라도, 이미 완료된 Undo 작업을 재실행하지 않음으로써 **복구의 Idempotency (멱등성)**을 보장하고, 데이터베이스의 Consistency (일관성)가 깨지는 것을 방지합니다.
> 3. **융합**: OS의 체크포인팅(Checkpointing) 기법과 결합하여 복구 속도를 최적화하며, 분산 데이터베이스 환경에서의 2단계 커밋(2PC, Two-Phase Commit) 프로토콜 안정성에 기여합니다.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 개념 및 철학
데이터베이스 회복 알고리즘에서 가장 까다로운 문제는 **'복구하는 도중 다시 죽는 경우'**입니다. 시스템 장애로 인해 트랜잭션을 롤백(Rollback)해야 하는 상황에서, 롤백 연산(Update의 반대 작업)을 수행하는 중간에 시스템이 또 다운되면 어떻게 될까요? 단순한 로그 방식에서는 재시작 후 로그를 처음부터 다시 읽으며 Undo를 시도합니다. 이때, 이미 취소된 연산을 다시 취소하려 하면 데이터 무결성이 심각하게 훼손됩니다.

**CLR (Compensation Log Record)**은 이러한 **Nested Crash (중첩 장애)** 상황을 해결하기 위해 고안된 '보험'과 같은 기술입니다. "나는 방금 B라는 로그를 취소(Undo)했다"라는 사실을 별도의 로그로 남김으로써, 재부팅 후 시스템이 "아, B는 이미 처리됐구나"라고 인지하게 만듭니다. 이는 단순한 기록이 아니라, **복구 로직을 'Undo/Redo'의 이중 부담에서 'Redo-only'의 단순한 구조로 변형**하는 설계 패러다임의 전환입니다.

#### 등장 배경
1.  **기존 한계**: Undo 로그는 실행 취소 명령이므로, 로그 자체를 다시 실행할 수 없음. (Redo 불가능)
2.  **혁신적 패러다임**: "Undo 연산 자체를 새로운 Redo 가능한 로그로 정의한다"는 ARIES의 설계 철학 도입.
3.  **비즈니스 요구**: 24/365 무중단 서비스 환경에서 복구 신뢰도(Reliability)는 선택이 아닌 필수 생존 문제.

#### ASCII 다이어그램: 중첩 장애 시나리오
아래 다이어그램은 복구 중 장애가 발생했을 때, CLR이 없으면 데이터가 꼬이는 이유를 보여줍니다.

```text
[상황: 계좌 이체 중 장애 발생 및 재시작]

1. 정상 로그:  [T1: A=100 (이전: 50)] ── [T1: B=200 (이전: 150)]
                |
                v
2. 💥 장애 발생 (Commit 안 됨)
3. 복구 시작 (Undo 진행): 
   ──▶ [Undo B 실행: B->150 복구] ──💥 2차 장애 발생! (여기서 끝)

4. 재부팅 후 (CLR 없는 경우):
   로그 스캔 중 "T1: B=200" 발견 -> "이거 취소해야지!" (B->150)
   ⚠️ 문제: B는 이미 150으로 돌아왔는데 다시 150으로 만듦. 
            만약 중간에 다른 값이었다면 데이터 오류 발생.

5. 재부팅 후 (CLR 있는 경우):
   1차 복구 시점에 [CLR: Undo-B] 로그 기록 완료.
   2차 재시작 후 "T1: B=200" 발견 -> "해당 LSN의 NextLSN을 확인."
   "이미 [CLR: Undo-B]가 있네? 그럼 패스(Pass)!" ✅
```

> **해설**: 위의 다이어그램과 같이 CLR은 **'이미 지나간 길'**을 표시합니다. 2차 장애로 인해 복구가 중단되더라도, 시스템은 로그 스트림(Log Stream)에 남겨진 흔적(CLR)을 보고 중복 작업을 방지합니다. 이는 복구 과정을 **Stateless (상태 비저장)** 하거나 **Idempotent (멱등)** 한 방식으로 만듭니다.

#### 📢 섹션 요약 비유
CLR은 **'복구 작업자가 남긴 작업 일지'**와 같습니다. 건물을 철거(Undo)하다가 퇴근 전에 "오늘 2층까지 철거 완료"라는 일지(CLR)를 남겨두는 것입니다. 다음 날 출근해서 다시 2층을 철거하러 가지 않고, 일지를 확인하고 바로 1층부터 시작하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 구성 요소 상세 분석
CLR은 단순한 텍스트 로그가 아니며, 데이터베이스 엔진이 해석하는 구조화된 데이터 객체입니다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 데이터 타입 |
|:---|:---|:---|:---|
| **LSN (Log Sequence Number)** | 로그의 고유 주소 | 해당 CLR 레코드의 물리적 위치. 로그 스트림 내의 절대적 순서 보장 | BigInt / Offset |
| **UndoNxtLSN** | **가장 중요한 포인터** | *이번에 Undo를 완료했으니, 다음에는 이 LSN을 취소해라*라고 가리키는 역방향 링크드 리스트의 포인터 | LSN (Ref) |
| **Type** | 레코드 구분 | 이 레코드가 CLR임을 식별 (일반 Update 로그와 구분) | Enum |
| **TransID** | 트랜잭션 식별 | 어떤 트랜잭션의 롤백 과정에서 생성된 로그인지 식별 | Transaction ID |
| **PrevLSN** | 연결 고리 | 같은 트랜잭션의 이전 로그를 가리킴 (Undo 체인 유지) | LSN (Ref) |

#### 아키텍처: Undo Chain & CLR 삽입 구조
아래 구조는 ARIES 알고리즘에서 트랜잭션의 Undo 연산이 수행될 때, 로그가 어떻게 변화하는지 시각화한 것입니다.

```text
[Log Storage (Buffer or Disk)]

[LSN: 100] T1: Update A (10 -> 20), PrevLSN: NULL
      |
      v (트랜잭션 진행)
[LSN: 101] T1: Update B (30 -> 40), PrevLSN: 100
      |
      v (Commit 실패 / Crash 발생 -> Undo 시작)
      |
[LSN: 102] T1: CLR (Undo for LSN 101) 
             - Action: Set B back to 30
             - UndoNxtLSN: 100 (다음엔 100번을 취소해라)
             - PrevLSN: 101 (논리적 흐름 유지)
      |
      v (Undo 계속 진행)
[LSN: 103] T1: CLR (Undo for LSN 100)
             - Action: Set A back to 10
             - UndoNxtLSN: NULL (더 이상 취소할 게 없다)
             - PrevLSN: 102
```

> **해설**:
> 1.  **형성(Generation)**: 시스템이 LSN 101에 대한 취소 연산(B->30)을 수행하면서, 그 사실을 기록한 LSN 102를 생성합니다.
> 2.  **연결(Linkage)**: LSN 102의 `UndoNxtLSN` 필드는 **100**을 가리킵니다. 이는 "LSN 101은 끝났으니, 이제 LSN 100을 취소해라"는 의미입니다.
> 3.  **포인터 따라가기**: 복구 루틴은 단순히 로그를 역순으로 읽는 것이 아니라, **가장 최근 CLR의 `UndoNxtLSN`**을 따라가며 남은 작업을 찾아냅니다.

#### 심층 동작 원리 (3-Phase Recovery Protocol)
1.  **Analysis (분석) 단계**: LSN (Log Sequence Number)을 스캔하며 어떤 트랜잭션이 완료되지 않았는지 파악 (Undo List 작성).
2.  **Redo (재수행) 단계**: Checkpoint LSN부터 끝까지 로그를 읽으며, Dirty Page에 기록되지 않은 변경 사항을 모두 반영. **여기서 CLR도 로그이므로 Redo 대상이 됩니다.** (CLR을 통해 Undo 상태를 복구!)
3.  **Undo (취소) 단계**: 로그의 끝에서부터 거꾸로 읽으며 Undo List에 있는 트랜잭션을 취소.
    *   **일반 로그 발견**: 원래 값으로 복구 후, **CLR을 기록**하고 `UndoNxtLSN` 갱신.
    *   **CLR 발견**: "이미 취소된 작업이구나" -> 이를 건너뛰고(`UndoNxtLSN` 참조) 다음 미완료 작업으로 이동.

#### 핵심 코드 및 알고리즘 (Pseudo-code)
```sql
-- Pseudo-code for ARIES Undo Logic with CLR
WHILE (UndoList is NOT empty) {
    CurrentLSN = FindLatestLSN(UndoList);
    
    READ_LOG_RECORD(CurrentLSN);

    IF (Record.Type == CLR) {
        -- CLR을 만나면 이미 처리된 것으로 간주하고 포인터를 이동
        CurrentLSN = Record.UndoNxtLSN;
        CONTINUE;
    }
    
    IF (Record.Type == UPDATE) {
        -- 1. 실제 데이터 페이지에 Old Value 적용 (Restore)
        RESTORE_PAGE(PageID, Record.OldValue);
        
        -- 2. 보상 로그(CLR) 기록 (이 작업이 Redo 가능하도록!)
        NewCLR = WRITE_COMP_LOG(
            TransID: Record.TransID,
            TargetLSN: CurrentLSN, 
            UndoNxtLSN: Record.PrevLSN
        );
        
        -- 3. 포인터 갱신
        CurrentLSN = Record.PrevLSN;
    }
    
    FLUSH_LOG(); -- WAL (Write-Ahead Logging) 원칙에 따라 로그 먼저 디스크 기록
}
```

#### 📢 섹션 요약 비유
이 과정은 **'미로 탈출에서 실시간으로 지도를 수정하는 것'**과 같습니다. 원래 갔던 길(Undo)을 되돌아오면서, "이 길은 막혔으니 뒤로 돌아가세요"라고 새로운 표지판(CLR)을 세웁니다. 만약 탈출 도중에 다시 잠이 들더라도, 깨어나서 표지판(CLR)을 보고 바로 올바른 경로로 돌아갈 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 심층 기술 비교: Undo Logging vs. CLR (ARIES)
복구 알고리즘의 진화 과정에서 CLR이 차지하는 위치를 비교 분석합니다.

| 구분 | 전통적 Undo Logging | ARIES (with CLR) |
|:---|:---|:---|
| **복구 방식** | 복구 시 로그를 다시 실행하는 연산 수행 | **Redo-only**: 로그를 순차적으로 재실행하여 상태 복구 |
| **중첩 장애 처리** | Undo 로그가 사라지거나 재싖� 불가능하여 데이터 정합성 위험 | CLR이 Undo 연산 자체를 영구 기록하여 **안전하게 재복구 가능** |
| **로그 스캔 방향** | Undo 시 역방향 스캔만 수행 | Redo는 정방향, Undo는 역방향(단, CLR로 최적화) |
| **성능 (RTO)** | 중첩 장애 시 재시작 비용이 매우 높음 | **빠른 재시작**: 이미 처리된 부분을 건너뛰어 복구 시간 단축 |
| **구현 복잡도** | 상대적으로 단순함 | **매우 복잡함**: 로그 체인 관리 및 LSN 연결이 중요 |

#### 과목 융합 관점
1.  **운영체제 (OS) - 재진입 가능성 (Reentrancy)**:
    OS의 시그널 핸들러나 인터럽트 루틴은 "Reentrant"해야 합니다. 중단되었다가 다시 시작되어도 문제가 없어야 한다는 것입니다. CLR은 데이터베이스 복구 루틴을 **Reentrant**하게 만드는 장치입니다.
2.  **네트워크 - TCP 재전송 및 멱등성**:
    네트워크에서 패킷이 유실되어 재전송되는 상황을 가정해 봅시다. 수신 측 서버는 같은 요청을 두 번 받아도 중복 처리를 하지 않아야 합니다(Idempotency). CLR은 "이미 취소된 로그"에 대해 "이미 수신(처리) 완료된 패킷"으로 간주하여 드롭(Drop)하는 네트워크 계층의 로직과 유사합니다.

#### 📢 섹션 요약 비유
CLR은 마치 **'소포 배송의 운송장 번호'**와 같습니다. 그냥 물건(데이터)을 옮기는 것(Undo)이 아니라, "이 물건은 어디서 와서 어디로 갔는지" 운송장에 기록(CLR)해 둡니다. 중간에 배송트럭이 고장 나더라도, 운송장만 있으면 물건이 어디 있는지 정확히 찾아서 배송을 이어서 할 수 있습니다. (기존 방식은 트럭이 고장 나면 물건 위치를 알 수 없는 것과 같습니다.)

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

#### 실무 시나리오: 대용량 트랜잭션 롤백 시나리오
**상황**: 금융권 결제 배치 작업 중 1시간 동안 1억 건의 데이터를 수정하던 도중 장애 발생. DB가 롤백을 시작하는데, 롤백(undo) 자체가 수분에서 수십 분이 걸리는 상황.

**의사결정 과정**: