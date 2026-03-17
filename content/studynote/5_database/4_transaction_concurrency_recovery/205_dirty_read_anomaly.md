+++
title = "205. 오손 읽기 (Dirty Read) - 미확정 데이터의 유혹"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 205
+++

# 205. 오손 읽기 (Dirty Read) - 미확정 데이터의 유혹

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오손 읽기(Dirty Read)는 트랜잭션의 **원자성(Atomicity)**을 위배하여, **커밋(Commit)** 되지 않은 중간 상태의 데이터를 다른 트랜잭션이 참조하는 데이터 무결성 침해 현상이다.
> 2. **가치**: `Read Uncommitted` (읽기 미확정) 격리 수준에서만 발생하며, 데이터 정합성을 희생하고 극한의 처리량(Throughput)을 확보해야 하는 매우 제한된 로깅/분석 시나리오에서만 고려됩니다.
> 3. **융합**: 동시성 제어(Concurrency Control)와 ACID 특성의 트레이드오프 관계를 보여주는 핵심 사례로, `MVCC` (Multi-Version Concurrency Control)나 `Locking` (잠금) 기반의 격리 수준 상향 조정을 통해 방지합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
**오손 읽기 (Dirty Read)**란, 특정 트랜잭션이 데이터베이스의 상태를 변경(INSERT, UPDATE, DELETE)하였으나 아직 트랜잭션을 종료(`COMMIT`)하지 않은 **활성 상태(Active State)**에서, 다른 트랜잭션이 해당 변경된 데이터를 읽어들이는 비정상적인 현상을 의미합니다.

관계형 데이터베이스(RDBMS)의 트랜잭션 처리는 기본적으로 **ACID** 원칙을 따릅니다. 그중 **원자성(Atomicity)**은 "트랜잭션 내의 연산은 모두 성공하거나, 하나라도 실패하면 아무 일도 없었던 것처럼(Rollback) 원복되어야 한다"는 원칙입니다. 오손 읽기는 이 원자성을 보장하기 전, 즉 "아직 확정되지 않은 데이터"를 바라보게 되어, `T1`이 롤백될 경우 `T2`는 결코 존재하지 않았던 데이터를 기반으로 로직을 수행하게 되는 치명적인 논리적 오류를 유발합니다.

#### 등장 배경 및 비즈니스 임팩트
1.  **기존 한계**: 초기 데이터베이스 시스템에서는 트랜잭션 간의 격리가 엄격하지 않아, 동시 처리 시 잦은 데이터 충돌 및 데드락(Deadlock)이 발생했습니다.
2.  **성능 패러다임**: 시스템의 응답 속도(Latency)를 높이고 처리량(TPS)을 극대화하기 위해, 데이터 정합성보다는 동시성을 우선시하는 **Read Uncommitted** 격리 수준이 도입되었습니다.
3.  **현재의 비즈니스 요구**: 금융권이나 결제 시스템 등 데이터 정합성이 생명인 영역에서는 절대 허용되지 않으나, 대용량 로그 분석이나 통계 집계 등 오차가 허용되는 배치(Batch) 처리 환경에서는 극히 드물게 활용됩니다.

#### 💡 핵심 비유
오손 읽기는 **"작성자가 아직 저장 버튼을 누르지 않은 문서를, 다른 사람이 몰래 훔쳐보는 것"**과 같습니다. 작성자가 결국 문서를 폐기(Rollback)한다면, 훔쳐본 사람은 실제 존재하지 않는 정보를 가지고 잘못된 행동을 하게 됩니다.

#### 📢 섹션 요약 비유
이 섹션의 내용을 관통하는 비유는 **"서류 접수처의 대리석 카운터"**입니다. 아직 접수 도장이 찍히지 않은(Commit 전) 서류 위에 손을 올려놓고 있는 상태에서, 다른 직원이 그 내용을 엿보는 것과 같습니다. 언제든 신청이 철회될 수 있는 불안정한 상태입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 구성 요소 (동적 상태 테이블)
오손 읽기는 트랜잭션의 라이프사이클과 데이터 잠금(Locking) 메커니즘과 밀접한 관련이 있습니다.

| 요소명 | 역할 | 내부 동작 | 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|
| **Active State** | 트랜잭션 활성화 상태 | 데이터 변경 명령 실행 후 커밋 대기 중 | `BEGIN TRANSACTION` | 주문서 작성 중 (펜을 들고 있는 상태) |
| **Rollback Segment** | 되돌리기 영역 | 변경 전 원본 데이터(Image)를 백업 저장 | UNDO 로그 | 수정 전 원본 사본 보관함 |
| **Exclusive Lock** | 배타적 잠금 (쓰기) | 다른 트랜잭션의 쓰기/읽기 시도 차단 | `X-Lock` (잠금 모드) | "여기 쓰는 중이니 들어오지 마시오" 표지 |
| **Shared Lock** | 공유 잠금 (읽기) | 다른 트랜잭션의 읽기는 허용, 쓰기는 차단 | `S-Lock` (Read Committed 등) | "읽기 전용, 수정 금지" 스티커 |
| **Buffer Cache** | 버퍼 캐시 | 메모리상의 데이터 블록 관리 영역 | DBMS 메모리 풀 | 임시 서류 보관함 |

#### ASCII 구조 다이어그램: 오손 읽기 발생 구조
오손 읽기는 `Read Uncommitted` 수준에서만 발생하며, 쓰기 트랜잭션이 `X-Lock`(배타 잠금)을 가지고 있더라도, 읽기 트랜잭션이 이를 무시하고 데이터에 접근할 때 발생합니다.

```text
[ Dirty Read Architecture & Locking Flow ]

   Transaction Manager          Lock Manager              Data Storage
   (트랜잭션 관리자)             (잠금 관리자)              (디스크/버퍼)
         |                           |                           |
   T1: UPDATE Point SET val=500   -->  Request X-Lock  -------->   [Old Data: 100]
         |                           |                           |
         |                           | <--- Granted X-Lock --------> (Lock Acquired)
         |                           |                           |
         v                           |                           |
   (Write to Buffer)                |                           |
   (Status: ACTIVE)                 |                           |
         |                           |                           |
   T2: SELECT Point (Read Uncommitted)                      [New Data: 500]
         |                           |                           |
         |      Request S-Lock       |      (Ignored or         |
         |      (or No Lock Req)     |       No Wait)           |
         |                           |                           |
         +-------------------------->--------------------------->  💥 DIRTY READ!
         |                           |                           |
   (T2 reads '500')                 |                           |
         |                           |                           |
   T1: ROLLBACK!  ---------------->  Release X-Lock  -------->   (Restore to 100)
         |                           |                           |
         v                           v                           v
   Result: T2 processed logic based on '500' which never existed.
```

#### 심층 동작 원리 및 코드
1.  **단계 1 (데이터 변경)**: `T1`이 `UPDATE` 문을 실행하면, DBMS는 해당 행(Row)에 `X-Lock` (Exclusive Lock)을 획득하고, 이전 값을 Undo Log에 기록한 후 메모리 블록의 데이터를 `100`에서 `500`으로 변경합니다. 상태는 `ACTIVE`로 남습니다.
2.  **단계 2 (비정상 접근)**: `T2`가 `SELECT`를 시도합니다. 정상적인 격리 수준(`Read Committed` 이상)이라면 `T1`의 `X-Lock` 때문에 대기(Block)해야 합니다. 하지만 `Read Uncommitted` 설정 하에서는 `T2`가 대기 없이 잠금을 무시하고 메모리상의 변경된 값(`500`)을 읽어갑니다.
3.  **단계 3 (트랜잭션 실패)**: `T1`에서 오류가 발생하거나 사용자가 취소하여 `ROLLBACK`이 호출됩니다. DBMS는 Undo Log를 참조하여 데이터를 다시 `100`으로 복구하고 `X-Lock`을 해제합니다.
4.  **단계 4 (논리적 모순)**: `T2`는 이미 사라진 `500`이라는 값을 가지고 연산을 수행했습니다. 예를 들어, `500` 원이 있다고 판단해 물건을 결제했는데, 실제로는 `100` 원만 있어 잔고 부족으로 실패하는 등의 시스템 불일치가 발생합니다.

**[SQL Scenario: MySQL/MariaDB]**
```sql
-- Session 1 (T1)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
UPDATE accounts SET balance = 500 WHERE user_id = 1;
-- Commit 하지 않음 (상태: Active)

-- Session 2 (T2) - 동시 실행
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE user_id = 1;
-- 결과: 500 (Dirty Data!)

-- Session 1 (T1)
ROLLBACK; -- 데이터는 다시 100으로 복구됨.
-- 하지만 T2는 이미 500이라는 잘못된 정보를 사용했음.
```

#### 📢 섹션 요약 비유
오손 읽기의 내부 메커니즘은 **"날씨를 예보하는 도중에, 지도에 그려지지 않은 가상의 저기압을 보고 배를 출항시키는 것"**과 같습니다. 그 저기압(데이터)은 사라질 수도 있고(롤백), 유지될 수도 있지만(커밋), 출항해버린 배(트랜잭션 T2)는 되돌릴 수 없습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 트랜잭션 격리 수준(TI Levels) 기술 비교 분석표
오손 읽기는 격리 수준에 따른 발생 가능성이 명확히 나뉩니다. 아래는 각 수준에서의 Dirty Read 허용 여부와 메커니즘 비교입니다.

| 구분 | 격리 수준 | 오손 읽기 가능성 | 내부 동작 메커니즘 | 성능 (TPS) | 실무 사용 용도 |
|:---|:---|:---:|:---|:---:|:---|
| **Level 1** | **Read Uncommitted** | **가능 (O)** | `X-Lock`을 무시하고 데이터 페이지를 직접 읽음 | ⭐⭐⭐⭐⭐ | 대용량 로그 분석, 거의 사용 안 함 |
| **Level 2** | **Read Committed** | **불가능 (X)** | 커밋된 데이터만 읽음 (Statement 기준) | ⭐⭐⭐⭐ | **대부분의 RDBMS 기본값 (Oracle, PostgreSQL 등)** |
| **Level 3** | **Repeatable Read** | **불가능 (X)** | 트랜잭션 내에서 읽은 데이터 스냅샷 유지 (MVCC) | ⭐⭐⭐ | MySQL(InnoDB) 기본값, 재고 관리 등 |
| **Level 4** | **Serializable** | **불가능 (X)** | 트랜잭션 간 완벽한 격리, 범위 잠금 등 | ⭐⭐ | 금융 결제, 계좌 이체 등 가장 엄격한 곳 |

#### 2. 데이터베이스 별 구현 메커니즘 융합 분석
오손 읽기를 방지하거나 허용하는 방식은 DBMS의 아키텍처에 따라 다릅니다.

*   **Locking 기반 (SQL Server 등 Read Committed 사용 시)**:
    *   `T1`이 데이터를 수정하면 `X-Lock`이 유지되는 동안, `T2`의 읽기 요청(`S-Lock` 요청)이 `Lock Wait` 상태로 대기합니다.
    *   **시너지/오버헤드**: 데이터 정합성이 완벽하지만, Lock 경합(Containment)이 심해 병행 처리 성능이 저하될 수 있습니다.
*   **MVCC (Multi-Version Concurrency Control) 기반 (MySQL(InnoDB), PostgreSQL)**:
    *   `T1`이 데이터를 수정하면 새 버전의 데이터를 생성(Undo Log 형태로 관리)하지만, `Read Committed` 이상에서는 `T2`가 과거의 커밋된 버전(Old Version)을 바라봅니다. Lock 없이 읽기가 가능하므로 성능이 뛰어납니다.
    *   **시너지/오버헤드**: `T2`가 `T1`의 작업을 방해하지 않아 Non-blocking 읽기가 가능하지만, Undo 영역을 관리하는 추가적인 저장소 공간 및 `Version Chain`을 스캔하는 비용이 발생합니다.

#### 3. 네트워크와의 연관성 (분산 DB 환경)
분산 데이터베이스 환경(Distributed Database)에서 오손 읽기는 더욱 치명적입니다.
*   **2PC (Two-Phase Commit)**: 분산 환경에서는 노드 간의 합의가 필요합니다. 노드 A는 커밋했으나 노드 B가 롤백할 경우, 노드 A를 읽은 클라이언트는 오손 데이터를 가지게 되어 **분산 트랜잭션 불일치(Distributed Anomaly)**가 발생합니다.

#### 📢 섹션 요약 비유
격리 수준을 조정하는 것은 **"회의실의 문(Under Lock)을 얼마나 꽉 닫을 것인가"**와 같습니다. 문을 활짝 열어두면(Read Uncommitted) 소음(오염된 데이터)이 들어오지만 통행(성능)은 자유롭습니다. 반대로 문을 잠그면(Serializable) 조용하지만, 사람들은 문 앞에서 줄을 서야 합니다(대기 시간 증가). 현대적인 오피스(MVCC)는 **"유리 벽을 설치"**하여 소음을 막으면서도 시야(동시성)는 확보합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 프로세스

**시나리오 A: 초실시간 대시보드 (Log Analysis)**
*   **상황**: 1초에 10만 건 이상의 로그가 쌓이는 IoT 센서 모니터링 시스템. 데이터는 참고용이며, 몇 건의 오차가 있어도 추세를 파악하는 것이 목적.
*   **의사결정**: `Read Uncommitted`를 고려해 볼 수 있음. 하지만 최신 하드웨어 성능 향상으로 인해 굳이 위험을 감수할 이유는 없어 보임. 일반적으로 `Read Committed` 사용 권장.
*   **예외**: 아주 잠깐의 스냅샷을 찍어야 하는 특수 쿼리에서만 사용 가능.

**시나리오 B: 재고 관리 시스템 (Inventory Management)**
*   **상�