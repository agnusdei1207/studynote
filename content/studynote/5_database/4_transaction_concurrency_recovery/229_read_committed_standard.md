+++
title = "229. Read Committed (레벨 1) - 업무용 DB의 표준 격리"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 229
+++

# 229. Read Committed (레벨 1) - 업무용 DB의 표준 격리
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Read Committed (커밋된 읽기)는 트랜잭션이 **오직 커밋(Commit)이 완료된 데이터만 읽을 수 있도록 제한**하여, 데이터베이스 격리 수준(Isolation Level) 중 가장 기본적인 보안 장치인 '오손 읽기(Dirty Read)'를 원천 차단하는 트랜잭션 격리 수준이다.
> 2. **가치**: 대다수 상용 RDBMS(Relational Database Management System)인 Oracle, SQL Server, PostgreSQL 등의 기본 설정(Default)값으로, 데이터의 논리적 무결성과 시스템의 높은 동시 처리량(Throughput) 사이에서 가장 합리적인 균형점을 제공한다.
> 3. **융합**: MVCC(Multi-Version Concurrency Control) 아키텍처와 결합될 경우, 읽기 작업은 락(Lock) 없이 '커밋된 마지막 스냅샷(Snapshot)'을 접근하여, 쓰기 작업과의 블로킹(Blocking) 없이 초고속 동시성을 실현한다.
+++

### Ⅰ. 개요 (Context & Background)

Read Committed는 ANSI SQL 표준에서 정의하는 4단계 격리 수준 중 두 번째 단계에 해당하며, 현대 업무용 데이터베이스의 사실상 표준(De Facto Standard)으로 자리 잡은 격리 모드입니다. 이 모드의 핵심 철학은 "사용자는 아직 확정되지 않은 변경 사항을 볼 권리가 없다"는 것으로, 트랜잭션 간의 격리를 보장하기 위한 최소한의 장벽을 제공합니다.

기술적으로는 데이터를 읽는 시점에 해당 레코드(Record)나 페이지(Page)에 걸린 **공유 잠금(Shared Lock, S-Lock)**을 즉시 해제하거나(MSSQL 방식), **언두 로그(Undo Log)** 영역에 저장된 과거 버전의 데이터를 참조(MVCC 방식)함으로써 구현됩니다. 이로 인해 발생하는 대표적인 부작용은 **Non-Repeatable Read (비반복 읽기)**와 **Phantom Read (유령 읽기)**가 가능하다는 점입니다. 즉, 동일한 트랜잭션 내에서 두 번 동일한 데이터를 조회했을 때, 중간에 다른 트랜잭션이 커밋한 변경 사항이 반영되어 결과가 달라질 수 있습니다.

과거에는 하드웨어 자원이 제한적이어서 더 높은 격리 수준을 유지하기 어려웠으나, 현재는 대부분의 OLTP(Online Transaction Processing) 환경에서 이 수준이 "성능 저하 없이 데이터 신뢰성을 확보하는 최적의 지점"으로 인식됩니다. 특히 재무 회계나 결제와 같이 매우 엄격한 일관성이 요구되는 특수 상황을 제외하면, 일반적인 웹 서비스 및 업무 시스템에서는 이 수준이 널리 활용됩니다.

> **📢 섹션 요약 비유**: Read Committed는 **"결재가 완료된 공문서만 열람할 수 있는 규정"**과 같습니다. 팀원들이 결재를 올려 수정 중인 문서는 보이지 않으므로(Dirty Read 방지) 잘못된 정보에 기반한 의사결정을 내리지 않지만, 결재가 올라가는 동안 내 문서를 잠시 닐었다가 다시 열었을 때 최종 승인된 내용으로 바뀌어 있을 수 있습니다(Non-Repeatable Read 허용).

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Read Committed의 작동은 데이터베이스의 동시성 제어 메커니즘, 특히 **잠금(Locking) 기법**과 **다중 버전 동시성 제어(MVCC)**에 의해 크게 좌우됩니다.

#### 1. 핵심 구성 요소 및 동작 메커니즘

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 프로토콜/특징 | 비유 |
|:---|:---|:---|:---|:---|
| **S-Lock (Shared Lock)** | 읽기 일관성 보장 (잠금 기반 DB) | `SELECT` 수행 시 데이터에 걸며, **Read Committed에서는 즉시 해제**됨. | 짧은 유지 시간으로 병렬성 확보 | 책 읽을 때 눈으로만 훑고 바로 두는 것 |
| **X-Lock (Exclusive Lock)** | 쓰기 독점 보장 | `UPDATE/DELETE/INSERT` 시 부여하여, 커밋/롤백 전까지 타 트랜잭션의 접근(읽기 포함)을 차단함. | 트랜잭션 생존 기간 동안 유지 | 누군가 수정 중인 문서에 다른 사람이 손대지 못하게 함 |
| **Undo Log Segment** | 과거 데이터 백업 (MVCC 기반 DB) | 수정 발생 시 **Before Image**를 저장하며, 읽기 트랜잭션은 이 영역의 스냅샷을 조회함. | Rollback Segment / 물리적 로그 | 수정 전 원본을 보관하는 보관 서류함 |
| **TX Table (Transaction Table)** | 트랜잭션 상태 관리 (MVCC) | 특정 스냅샷이 현재 활성화된 트랜잭션에 의해 수정되었는지 판단하는 지표. | Commit SCN (System Change Number) | 각 문서의 결재 진행 상황을 알려주는 대장 |
| **Predicate Lock** (미사용) | 범위 쿼리 보안 | 이 격리 수준에서는 범위 잠금을 사용하지 않아 Phantom Read가 발생함. | Gap Lock 없음 | 빈 책장 구석에 빈 간판만 걸어두는 것 |

#### 2. 데이터 흐름 및 상태 전이 (ASCII)

아래 다이어그램은 시간의 흐름에 따라 두 트랜잭션(T1, T2)이 Read Committed 모드에서 데이터를 주고받는 과정을 도식화한 것입니다.

```text
[Time]    Transaction 1 (Writer)           Transaction 2 (Reader)         DB State
  ↓
  T1       BEGIN
  T2                                      BEGIN
  T3       UPDATE balance = 1000 ────────▶ [X-Lock 획득, Undo Log 생성]
           (Uncommitted: 1000)              (SELECT 시도 → S-Lock 대기 또는 Undo Read)
  T4                                      SELECT balance ───────▶ 500 (Old)
           ────────────────────────────────────────────────────────────────
           🔍 [해설]: T1이 아직 커밋하지 않았으므로, T2는 1000을 볼 수 없습니다.
              Locking 방식에서는 Blocking되며, MVCC 방식에서는 Undo Log의 500을 봅니다.
  T5       COMMIT! ───────────────────▶ [X-Lock 해제, 신규 데이터 1000 공개]
  T6                                      SELECT balance ───────▶ 1000 (New)
           ────────────────────────────────────────────────────────────────
           🔍 [해설]: T1이 커밋하자마자 T2는 즉시 변경된 값 1000을 읽습니다.
              같은 트랜잭션(T2) 내에서 조회 결과가 바뀌었으므로 'Non-Repeatable Read' 발생.
```

**[다이어그램 심층 해설]**
이 시나리오는 Read Committed의 **"Non-Repeatable Read 허용"** 특성을 명확히 보여줍니다.
1. **T4 시점**: 데이터 무결성을 위해 T1의 변경이 커밋되지 않은 상태이므로, T2는 이전 값(500) 혹은 대기 상태가 됩니다. 즉, **Dirty Read는 발생하지 않습니다.**
2. **T6 시점**: T1의 커밋 이후, T2의 두 번째 쿼리는 즉시 새로운 값(1000)을 반환합니다. T2 입장에서는 "방금 읽은 값이 500이었는데, 다시 읽으니 1000이 됐다"는 현상을 경험하게 됩니다.
3. **기술적 함의**: 이 동작 방식 덕분에 읽기 작업이 쓰기 작업의 완료를 기다리는 시간이 최소화되거나(MVCC), 읽기 잠금의 경합이 최소화되어 전체 시스템의 처리량(TPS)이 향상됩니다.

#### 3. 핵심 알고리즘: 유효성 검사 (Pseudo-code)

```sql
-- [Pseudo Code: Read Committed Validation Logic in MVCC]
FUNCTION read_committed_select(record_id, current_txn_id):
    
    -- 1. 버전 체인(Version Chain) 순회
    current_version = get_latest_version(record_id)
    
    WHILE current_version IS NOT NULL:
        -- 2. 트랜잭션 상태 확인 (Transaction Table)
        IF current_version.creator_txn_id IS COMMITTED THEN
            -- 수정한 트랜잭션이 커밋됨 -> 가시성(VISIBILITY) 확보
            RETURN current_version.data
            
        ELSE IF current_version.creator_txn_id IS ACTIVE THEN
            -- 아직 수정 중인 트랜잭션임 -> 이 버전은 건너뜀
            current_version = current_version.prev_version (Undo Log Access)
            
        ELSE IF current_version.creator_txn_id IS ABORTED THEN
            -- 롤백됨 -> 이 버전은 무시하고 이전 버전으로
            current_version = current_version.prev_version
            
        END IF
    END WHILE
    
    RETURN "RECORD_NOT_FOUND"
```

> **📢 섹션 요약 비유**: Read Committed의 내부 작동은 **"매장 전시장의 상품 가격표"**와 같습니다. 가격을 수정하는 직원(T1)이 스티커를 갈아 끼우는 동안, 손님(T2)은 아직 올려지지 않은 새 가격이 아닌, 시야에 보이는 기존 가격표를 보게 됩니다(Undo Log 참조). 하지만 직원이 수정을 마치고 붙여놓자마자(COMMIT), 그 뒤에 오는 손님은 즉시 바뀐 가격을 보게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

Read Committed를 이해하려면 격리 수준에 따른 데이터 정합성과 성능의 트레이드오프(Trade-off) 관계를 정량적으로 분석해야 합니다.

#### 1. 격리 수준 심층 기술 비교 (Metric vs Anomaly)

| 비교 항목 | Read Uncommitted (레벨 0) | Read Committed (레벨 1) | Repeatable Read (레벨 2) | Serializable (레벨 3) |
|:---|:---|:---|:---|:---|
| **데이터 정합성** | 매우 낮음 | 낮음 (Dirty Read만 차단) | 높음 (Non-Repeatable Read 차단) | 완벽 (Phantom Read 차단) |
| **동시성(Concurrency)** | 매우 높음 (Lock 경합 없음) | 높음 (짧은 S-Lock 또는 No Lock) | 중간 (긴 S-Lock, Range Lock) | 낮음 (순차 실행에 가까움) |
| **Latency (지연시간)** | 최저 | 낮음 | 중간 | 높음 |
| **Throughput (TPS)** | 최고 | 높음 (일반적인 웹 서비스 기준) | 중간 (금융 권장) | 낮음 |
| **구현 복잡도** | 낮음 | 낮음 | 중간 (Lock Escalation 등) | 높음 |

#### 2. 주요 이상 현상 (Anomaly) 허용 범위 시각화

```text
[Isolation Level Anomaly Matrix]

   ┃  Dirty Read   │  Non-Repeatable Read   │  Phantom Read
   ┃  (오손 읽기)  │  (비반복 읽기)          │  (유령 읽기)
━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RU  ┃      ✅ 허용  │      ✅ 허용            │      ✅ 허용
━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RC  ┃      ❌ 차단  │      ✅ 허용            │      ✅ 허용  ← 🎯 여기
(이 모드)  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RR  ┃      ❌ 차단  │      ❌ 차단            │      ✅ 허용 (MySQL 등)
━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SER ┃      ❌ 차단  │      ❌ 차단            │      ❌ 차단
```

**[비교표 해설]**
- **Read Committed (RC)**는 오직 **Dirty Read**만을 방어합니다.
- **Non-Repeatable Read 허용**: 다른 트랜잭션이 커밋한 데이터를 즉시 반영하기 때문입니다.
- **Phantom Read 허용**: 범위 쿼리 시 새로운 행이 추가되거나 사라지는 현상을 방지하지 않습니다(Gap Lock 미사용).
- **실무적 의미**: 대부분의 애플리케이션 로직(User Interface, Dashboard 등)은 데이터가 시시각각 변하는 것을 허용하므로(실시간성), 이 수준이 가장 무리없이 돌아갑니다.

#### 3. 타 과목 융합 및 상관관계
- **[운영체제(OS)]**: RC의 잠금 기반 구현은 OS의 **세마포어(Semaphore)** 및 **뮤텍스(Mutex)** 메커니즘과 연관되며, 데드락(Deadlock) 발생 빈도를 낮추는 전략(잠금 시간 단축)과 맞닿아 있습니다.
- **[네트워크]**: 높은 동시성 처리는 네트워크 **대기열(Queue)** 길이를 줄이고 서버의 **응답 시간(Response Time)**을 안정적으로 유지하는 데 기여합니다.

> **📢 섹션 요약 비유**: 격리 수준을 조정하는 것은 **'차량의 안전 장치와 속도 관계'**와 같습니다. Read Uncommitted는 헬멧도 없이 달리는 것(위험하지만 빠름), Read Committed는 **안전벨트를 착용하고 정속 주행**하는 것(가장 일반적), Serializable은 **역주행 방지를 위해 모든 차로를 단속**하는 것(안전하지만 교통 체증 심함)과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

시스템 아키텍트로서 Read Committed를 도입할 때는 업무의 특성에 맞는 정교한 튜닝과 판단이 필요합니다.

#### 1. 실무 시나리오 및 의사결정 프로세스

| 시