+++
title = "데이터베이스 정합성 및 동시성 제어 (Concurrency Control)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 데이터베이스 동시성 제어 (Concurrency Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다수의 사용자가 동시에 데이터베이스를 조회하고 갱신할 때, 트랜잭션의 실행 순서를 직렬화(Serializability)하여 데이터의 무결성과 일관성(ACID)을 보호하는 제어 메커니즘입니다.
> 2. **가치**: 갱신 손실(Lost Update), 오손 읽기(Dirty Read) 등 병행 수행 시 발생하는 치명적인 이상 현상을 방지하면서도, 시스템의 동시 처리량(Throughput)을 극대화하여 엔터프라이즈 시스템의 신뢰성을 보장합니다.
> 3. **융합**: 운영체제의 세마포어(Semaphore) 및 뮤텍스(Mutex) 원리를 데이터 블록/행 수준으로 확장한 개념이며, 분산 시스템에서의 분산 락(Distributed Lock) 및 합의 알고리즘으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**동시성 제어(Concurrency Control)**란 다중 사용자 환경의 DBMS에서 여러 트랜잭션이 동시에 실행될 때, 이들이 서로 간섭하지 않고 마치 순차적으로 실행된 것과 같은 결과(직렬 가능성, Serializability)를 보장하도록 스케줄링하는 기법입니다. 데이터의 일관성을 엄격하게 지키면서도 동시 처리 성능(병행성)을 떨어뜨리지 않는 최적의 균형점을 찾는 것이 동시성 제어의 핵심 목표입니다.

#### 2. 💡 비유를 통한 이해
동시성 제어는 **'1차선 교차로에서의 신호등 시스템'**과 같습니다.
- **제어가 없는 상태**: 신호등이 없는 교차로에 수많은 차들이 동시에 진입하면 충돌(데이터 파괴)이 발생하거나, 서로 눈치만 보다가 꼼짝도 못 하는 교착 상태(Deadlock)에 빠집니다.
- **락(Lock) 기반 제어**: 신호등을 설치하여 한 번에 한 방향의 차만 지나가게 합니다(안전함). 하지만 차가 한 대뿐일 때도 빨간불이면 기다려야 하므로 답답합니다(성능 저하).
- **MVCC (다중 버전 제어)**: 교차로 위로 고가도로와 지하차도(데이터의 여러 버전)를 뚫어, 직진하는 차(읽기)와 우회전하는 차(쓰기)가 서로 방해받지 않고 동시에 지나갈 수 있게 만든 최첨단 입체 교차로입니다.

#### 3. 등장 배경 및 발전 과정
1.  **초기 병행 수행의 한계 (이상 현상 발생)**: 초기 DB 시스템에서는 동시 접근을 허용하면 다음과 같은 문제가 발생했습니다.
    - **갱신 손실(Lost Update)**: 두 트랜잭션이 동시에 같은 데이터를 수정할 때, 나중에 수정된 결과만 남아 이전 결과가 사라지는 현상.
    - **오손 읽기(Dirty Read)**: 트랜잭션 A가 수정 중이고 아직 커밋하지 않은 데이터를 B가 읽어갔는데, A가 롤백해버려 B가 잘못된 데이터를 가지게 되는 현상.
    - **반복 불가능 읽기(Non-repeatable Read)**: 트랜잭션 내에서 같은 데이터를 두 번 읽었는데, 그 사이 다른 트랜잭션이 값을 수정/커밋하여 두 값이 달라지는 현상.
2.  **Locking 기법의 도입**: 이를 막기 위해 데이터에 자물쇠를 채우는 2PL(Two-Phase Locking) 프로토콜이 등장했으나, 읽기와 쓰기가 서로를 블로킹(Blocking)하여 성능이 크게 저하되었습니다.
3.  **현대의 패러다임 변화**: 하드웨어 성능 향상과 대용량 트래픽 처리를 위해 락을 최소화하는 낙관적 동시성 제어(Optimistic Concurrency Control)와, 버전을 관리하여 읽기/쓰기 충돌을 없앤 **MVCC(Multi-Version Concurrency Control)**가 현대 DBMS의 표준으로 자리 잡았습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 동시성 제어 주요 기법 (표)

| 기법 명칭 | 핵심 동작 원리 | 장점 | 단점 / 한계 | 적용 시나리오 |
| :--- | :--- | :--- | :--- | :--- |
| **락킹 (Locking / 2PL)** | 데이터 접근 전 Lock 획득, 사용 후 Unlock | 구현이 직관적, 완벽한 직렬성 보장 | 교착 상태(Deadlock) 발생 가능, 동시성 저하 | 전통적인 RDBMS 기본 동작 |
| **타임스탬프 순서 (Timestamp Ordering)** | 트랜잭션 시작 시 부여된 시스템 시간에 따라 순서 결정 | Lock을 사용하지 않아 교착 상태 없음 | 충돌 시 롤백 비율이 높음 (연쇄 복귀 가능성) | 분산 DB의 트랜잭션 순서 정렬 |
| **낙관적 검증 (Optimistic Validation)** | 트랜잭션 수행 시에는 검증하지 않고, 커밋 시점에 일괄 검증 | 읽기 위주 환경에서 최고의 성능 발휘 | 쓰기 충돌 빈번 시 롤백 오버헤드 극심 | 충돌이 적은 게시판 읽기/조회 시스템 |
| **다중 버전 (MVCC)** | 쓰기 발생 시 원본을 유지하고 새로운 버전을 생성, 읽기는 과거 버전을 참조 | 읽기(Read)와 쓰기(Write)가 서로를 블로킹하지 않음 | 버전 관리로 인한 추가 스토리지(Undo/Vacuum) 필요 | PostgreSQL, Oracle, MySQL 등 현대 DBMS |

#### 2. 핵심 알고리즘 아키텍처 (ASCII 다이어그램)

```text
<<< 2PL (Two-Phase Locking) Protocol >>>

Lock Acquired
  ^
  |      [ Growing Phase ]          [ Shrinking Phase ]
  |     (락을 획득하기만 함)          (락을 반납하기만 함)
  |       *                       *
  |     *   *                   *   *
  |   *       *               *       *
  | *           *           *           * (Commit / Rollback)
  +-------------------(Lock Point)----------------------> Time
  ※ 락 포인트(Lock Point)를 지나면 새로운 락을 획득할 수 없음.

<<< MVCC (Multi-Version Concurrency Control) Visibility >>>

[ Undo Log / Rollback Segment ]
+-------------------------+
| Transaction ID: 100     | <--- (Read View of Tx 102)
| Balance: $500           |
+-------------------------+
           ^ (Pointer)
           |
[ Main Table Data ]
+-------------------------+
| Transaction ID: 101     | <--- (Active Uncommitted Write)
| Balance: $400           |
+-------------------------+

[ 메커니즘 해설 (MVCC) ]
1. Tx 101이 잔액을 $400으로 수정 중(아직 커밋 안됨). 원본 $500은 Undo Log로 복사.
2. Tx 102가 조회를 요청. 시스템은 Tx 101이 아직 활성 상태임을 확인.
3. Tx 102는 Main Table을 무시하고 포인터를 따라 Undo Log의 $500(과거 버전)을 읽음.
4. 결과적으로 쓰기(Tx 101)와 읽기(Tx 102)가 락 경합 없이 동시에 진행됨.
```

#### 3. 심층 동작 원리: 트랜잭션 격리 수준 (Isolation Level)
ANSI/ISO SQL 표준은 동시성과 일관성의 트레이드오프를 조절하기 위해 4단계의 격리 수준을 정의합니다.
1.  **Read Uncommitted (Level 0)**: 락을 아예 걸지 않음. Dirty Read 발생. 실무 사용 불가.
2.  **Read Committed (Level 1)**: 커밋된 데이터만 읽음. 오라클/PostgreSQL의 기본값. 같은 쿼리를 두 번 실행하면 값이 달라지는 Non-repeatable Read 발생 가능.
3.  **Repeatable Read (Level 2)**: 트랜잭션 시작 시점의 스냅샷을 읽음. MySQL(InnoDB)의 기본값. 하지만 다른 트랜잭션이 새로운 행을 삽입(Insert)하면 없던 데이터가 나타나는 **Phantom Read** 발생 가능. (단, InnoDB는 넥스트 키 락으로 이를 방지함).
4.  **Serializable (Level 3)**: 가장 엄격한 수준. 읽기 작업에도 공유 락(Shared Lock)을 걸어 직렬화함. 성능이 매우 느림.

#### 4. 실무 수준의 락(Lock) 구현 및 교착 상태(Deadlock) 회피 코드 예시
```sql
-- [상황] 재고(Inventory)를 차감하는 실무 쿼리

-- 1. 비관적 락 (Pessimistic Lock - RDBMS)
-- FOR UPDATE를 사용하여 다른 트랜잭션이 이 행을 읽거나 수정하지 못하게 독점락(X-Lock)을 검.
BEGIN;
SELECT stock_quantity FROM items WHERE item_id = 1 FOR UPDATE;
UPDATE items SET stock_quantity = stock_quantity - 1 WHERE item_id = 1;
COMMIT;

-- 2. 낙관적 락 (Optimistic Lock - Application Level)
-- 버전(Version) 컬럼을 두어, 락 없이 읽고 업데이트 시점에 버전이 일치하는지 확인.
-- WHERE version = 1 조건이 실패하면 누군가 먼저 수정한 것이므로 애플리케이션에서 재시도(Retry) 처리.
UPDATE items 
SET stock_quantity = stock_quantity - 1, version = version + 1 
WHERE item_id = 1 AND version = 1;
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 비관적 제어(Pessimistic) vs 낙관적 제어(Optimistic) 심층 비교

| 비교 지표 | 비관적 제어 (2PL / FOR UPDATE) | 낙관적 제어 (Version Column) |
| :--- | :--- | :--- |
| **기본 철학** | "충돌이 무조건 발생할 것이다" | "충돌은 거의 발생하지 않을 것이다" |
| **락 획득 시점** | 데이터 조회(Select) 시점부터 즉시 | 락 미사용, 데이터 갱신(Update) 시점에 검증 |
| **성능 오버헤드** | DB 레벨의 락 관리 비용 증가 (Deadlock 위험) | 충돌 발생 시 애플리케이션 레벨의 롤백 및 재시도(Retry) 오버헤드 |
| **트래픽 성향** | 업데이트(Write)가 매우 잦은 환경에 적합 | 조회(Read)가 압도적으로 많은 환경에 적합 |
| **적용 사례** | 금융권 계좌 이체, 한정판 상품 결제 | 위키백과 편집, 게시판 수정, 상품 리뷰 |

#### 2. 과목 융합 관점 분석 (운영체제 및 분산 시스템)
- **OS 뮤텍스/세마포어와의 융합**: DBMS의 락(Lock) 매니저는 내부적으로 OS가 제공하는 동기화 객체(Mutex, Spinlock)를 사용하여 구현됩니다. 너무 잦은 락 경합은 OS의 Context Switching 비용을 폭증시켜 CPU 사용률만 100%를 찍고 실제 처리량은 0에 수렴하는 'Thrashing' 현상을 유발합니다.
- **분산 시스템의 CAP 정리**: 단일 DB에서의 동시성 제어가 분산 환경(마이크로서비스)으로 넘어가면, '분산 락(Redis Redlock 등)'이나 보상 트랜잭션을 통한 'SAGA 패턴'으로 진화해야 합니다. 이는 네트워크 지연으로 인한 락 점유 시간 증가 문제를 해결하기 위함입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 1: 데드락(Deadlock)의 빈번한 발생**
  - 상황: 서로 다른 트랜잭션이 테이블 A와 B를 교차로 업데이트하면서 데드락 모니터에 알람이 폭주.
  - 판단: 기술사는 **"자원 접근 순서의 일관성"** 규칙을 강제해야 합니다. 모든 애플리케이션에서 무조건 테이블 A를 먼저 락킹하고 테이블 B를 락킹하도록 트랜잭션 로직을 리팩토링(Refactoring)하여 환형 대기(Circular Wait)를 원천 차단합니다.
- **시나리오 2: 초당 10만 건의 선착순 쿠폰 발급 (티켓팅)**
  - 상황: RDBMS의 행 락(Row Lock)으로는 병목을 감당할 수 없어 DB가 다운됨.
  - 판단: RDBMS 동시성 제어의 한계입니다. DB 진입 전, **Redis(Single-thread 구조)**를 활용하여 메모리 상에서 원자적(Atomic)으로 재고를 차감하거나, Kafka와 같은 메시지 큐를 두어 쓰기 작업을 비동기 직렬화(Event Sourcing)하는 아키텍처로 전환해야 합니다.

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **적정 격리 수준 평가**: 무조건 Serializable이 좋은 것이 아닙니다. 업무 성격 상 Phantom Read를 허용해도 되는 통계/집계 화면이라면 Read Committed로 낮추어 동시성을 높여야 합니다.
- [ ] **MVCC의 Vacuum/Undo 관리**: PostgreSQL이나 Oracle 환경에서는 너무 긴 트랜잭션(Long-running Transaction)이 존재하면 과거 버전 데이터가 정리(Garbage Collection)되지 않아 디스크 공간이 고갈되는 Table Bloat 현상을 모니터링해야 합니다.

#### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **락 잡고 외부 API 호출**: 트랜잭션을 시작하고 DB 락을 잡은 상태에서 수 초가 걸리는 외부 결제 API를 호출하는 패턴. 외부 통신이 지연되면 DB 락이 풀리지 않아 전체 시스템이 마비됩니다. 락의 보유 시간은 밀리초(ms) 단위로 최소화해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- **정량적**: MVCC 및 낙관적 락 도입을 통해 기존 2PL 대비 동시 처리량(TPS) 300% 이상 향상, 데드락 발생률 0% 수렴.
- **정성적**: 다중 사용자 환경에서도 데이터 무결성이 보장되어 기업 시스템의 신뢰도(Trust)와 서비스 연속성을 확보합니다.

#### 2. 미래 전망 및 진화 방향
클라우드 네이티브 환경이 가속화됨에 따라 단일 DB의 동시성 제어를 넘어 **Global Concurrency Control**이 중요해지고 있습니다. Google Spanner와 같은 NewSQL은 원자 시계(TrueTime API)를 활용하여 지리적으로 분산된 노드 간에 락 없이 전역적으로 완벽한 외부 일관성(External Consistency)과 직렬성을 보장하는 형태로 진화하고 있습니다.

#### 3. 참고 표준/가이드
- **ISO/IEC 9075 (SQL Standard)**: 트랜잭션 격리 수준 및 동시성 제어에 대한 국제 규격.
- **IEEE 754**: 연산의 정밀성과 관련된 동시성 처리 기준 (금융 데이터 처리 시 참고).

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[ACID](@/studynotes/05_database/01_relational_model/acid.md)**: 동시성 제어가 궁극적으로 수호하고자 하는 트랜잭션의 4대 속성 (특히 I - 격리성).
- **[트랜잭션 격리 수준 (Isolation Level)](@/studynotes/05_database/02_concurrency_control/concurrency_control.md)**: 성능과 일관성을 조율하는 4단계 스펙.
- **[MVCC (Multi-Version Concurrency Control)](@/studynotes/05_database/02_concurrency_control/concurrency_control.md)**: 락을 회피하여 성능을 높이는 현대적 동시성 제어 아키텍처.
- **[교착 상태 (Deadlock)](@/studynotes/02_operating_system/01_process_management/deadlock.md)**: OS와 DB 모두에서 발생하는 자원 경쟁의 극단적 상태.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **신호등 지키기**: 사거리에 차들이 마구잡이로 달리면 꽝 부딪히겠죠? 동시성 제어는 차들이 순서대로 지나가도록 신호등을 켜주는 역할을 해요.
2. **도서관 책 빌리기**: 내가 재미있는 책을 읽고 있을 때 다른 친구가 그 책에 낙서를 하거나 뺏어가지 못하게 잠깐 자물쇠를 걸어두는 거예요. (락킹)
3. **사진 찍어두기**: 자물쇠 때문에 기다리기 지루하니까, 책의 원본은 놔두고 복사본 사진을 여러 장 찍어서 친구들에게 나눠주면 동시에 볼 수 있어요! (MVCC)
