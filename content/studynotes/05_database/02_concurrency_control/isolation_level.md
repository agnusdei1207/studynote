+++
title = "트랜잭션 격리 수준 (Transaction Isolation Level)"
date = 2026-03-03
[extra]
categories = "studynotes-05_database"
tags = ["격리수준", "IsolationLevel", "DirtyRead", "MVCC", "Serializable", "SSI"]
+++

# 트랜잭션 격리 수준 (Transaction Isolation Level)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 격리 수준(Isolation Level)은 ACID 속성 중 고립성(Isolation)을 구현하기 위해, 동시에 실행되는 여러 트랜잭션이 서로의 변경 데이터에 접근하는 범위를 단계별로 정의하여 데이터 일관성과 시스템 동시성 사이의 트레이드오프(Trade-off)를 조절하는 메커니즘입니다.
> 2. **가치**: 부정확한 데이터 읽기(Dirty Read, Phantom Read 등)로 인한 비즈니스 로직 오류를 원천 차단하는 동시에, 잠금(Locking) 경쟁으로 인한 성능 저하를 최소화하여 대규모 트래픽 환경에서도 안정적인 트랜잭션 정합성을 보장합니다.
> 3. **융합**: 고전적인 2단계 잠금 규약(2PL)을 넘어, 최근에는 MVCC(Multi-Version Concurrency Control) 기술과 결합되어 읽기 작업이 쓰기 작업을 방해하지 않는 비차단(Non-blocking) 동시성 제어 아키텍처로 진화하였습니다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 
트랜잭션 격리 수준은 특정 트랜잭션이 다른 트랜잭션에서 변경한 데이터를 볼 수 있는 허용 범위를 결정하는 DBMS의 설정 값입니다. ANSI/ISO SQL 표준(SQL-92)은 데이터 정합성 유지와 시스템 처리량(Throughput) 극대화를 위해 격리 수준을 4단계(Read Uncommitted, Read Committed, Repeatable Read, Serializable)로 정의하고 있습니다. 이는 다중 사용자 환경에서 트랜잭션을 순차적으로 하나씩 실행하는 '직렬성(Serializability)'과, 여러 트랜잭션을 병렬로 실행하여 얻는 '성능' 사이에서 아키텍트가 선택할 수 있는 전략적 옵션입니다.

- **💡 비유**: 
격리 수준은 **"아파트 리모델링 현장의 가림막"**과 같습니다. 
1. **Read Uncommitted**: 가림막 없이 공사 현장이 다 보이는 상태입니다. 행인이 공사 중인 먼지투성이 벽(미완성 데이터)을 보고 "집이 다 지어졌다"고 오해할 수 있습니다.
2. **Read Committed**: 공사가 끝난 방만 가림막을 치우고 보여줍니다. 하지만 내가 거실을 보는 사이에 안방 공사가 끝나면, 잠시 후에 다시 봤을 때 안방의 모습이 달라져 있을 수 있습니다.
3. **Repeatable Read**: 내가 집 구경을 시작할 때의 전체 청사진을 사진으로 찍어서 보여줍니다. 공사가 더 진행되어도 나에게는 처음 찍은 사진 속 모습만 보입니다.
4. **Serializable**: 집 구경을 하는 동안에는 인부들이 아예 일을 멈추거나, 인부들이 일하는 동안에는 집 구경을 절대 할 수 없는 완벽한 통제 상태입니다.

- **등장 배경 및 발전 과정**:
  1. **데이터 정합성 파괴의 위협**: 초기 DBMS는 동시성 제어가 미비하여, 두 명이 동시에 계좌 이체를 할 때 금액이 증발하거나(Lost Update), 아직 커밋되지 않은 잘못된 정보를 읽어(Dirty Read) 연산 오류를 일으키는 등 금융 시스템에서 치명적인 결함이 발생했습니다.
  2. **성능과 일관성의 극한 대립**: 모든 트랜잭션을 직렬로 처리하면 데이터는 완벽하게 안전하지만, 사용자가 조금만 늘어나도 대기 시간이 수십 초로 늘어나는 문제가 발생했습니다. 이를 해결하기 위해 "어느 정도의 부정확함은 허용하되 성능을 챙기자"는 단계적 격리 개념이 도입되었습니다.
  3. **MVCC 기술의 도입**: 과거에는 락(Lock)을 걸어 다른 트랜잭션을 멈추게 하는 방식이 주를 이루었으나, 90년대 이후 데이터의 과거 버전을 스냅샷으로 관리하는 MVCC(Multi-Version Concurrency Control) 기술이 보편화되면서 "읽기는 쓰기를 막지 않고, 쓰기는 읽기를 막지 않는" 현대적 격리 수준 구현이 완성되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

- **구성 요소 (표)**:

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|----------|----------|------|------|------|
| **Snapshot/Undo Log** | 이전 데이터 버전 관리 | 데이터가 수정될 때 원본 데이터를 Undo 세그먼트에 복사하여, 다른 트랜잭션이 과거 시점의 데이터를 읽을 수 있게 합니다. | MVCC (Multi-Version) | 과거의 사진 앨범 |
| **Transaction ID (TID)** | 트랜잭션 고유 식별자 | 각 트랜잭션에 순차적인 번호를 부여하여, 특정 레코드가 해당 트랜잭션 시점에서 유효한지 판단하는 기준이 됩니다. | Logical Clock | 입장 번호표 |
| **Read View / Snapshot** | 가시성(Visibility) 정의 | 트랜잭션 시작 시 활성 상태인 다른 트랜잭션 목록을 캡처하여, 어떤 버전을 읽을 수 있는지 결정하는 필터 역할을 합니다. | Visibility Check | 특정 시점의 필름 |
| **Shared/Exclusive Lock** | 공유 및 배타 잠금 | 데이터를 읽거나(S-Lock) 쓸 때(X-Lock) 소유권을 주장하여 다른 트랜잭션의 접근을 제어합니다. | 2-Phase Locking (2PL) | 회의실 예약 키 |
| **Next-Key Lock** | 범위 기반 잠금 | 인덱스 레코드와 그 사이의 간격(Gap)을 동시에 잠가, 유령 읽기(Phantom Read)를 방지합니다. | Gap Lock | 복도 통제 |

- **정교한 구조 다이어그램 (MVCC 기반 격리 메커니즘)**:

```text
===================================================================================================
                                [ MVCC (Multi-Version Concurrency Control) ]
===================================================================================================
[ Database Storage ]                                     [ Undo Log / Rollback Segment ]
+------------------------------------+                  +-----------------------------------------+
| Row ID | Data | Last_TID | RollPtr |                  | Undo Blk 1: [TID: 50 | Data: 1000]      |
+--------+------+----------+---------+                  +-----------------------------------------+
| RID_1  | 2000 |   100    |  Ptr1 --+----------------> | Undo Blk 2: [TID: 80 | Data: 1500]      |
+--------+------+----------+---------+                  +-----------------------------------------+
                                                        | Undo Blk 3: [TID: 20 | Data: 500 ]      |
                                                        +-----------------------------------------+

[ Transaction A (TID: 110, Level: Repeatable Read) ]     [ Transaction B (TID: 120, Level: Read Committed) ]
---------------------------------------------------     ---------------------------------------------------
1. SELECT Data FROM RID_1;                              1. UPDATE Data=3000 WHERE RID_1;
   - A는 TID 110임.                                      - B는 TID 120으로 기록됨.
   - 현재 RID_1의 Last_TID는 100.                        - RID_1의 Data는 3000으로 변경됨.
   - 100 < 110 이므로 가시성 인정(OK).                    - 기존 2000은 Undo Log로 복사됨.
   - 결과: 2000 반환                                     - 아직 COMMIT 안 함!

2. (B의 Update 후) SELECT Data FROM RID_1;              2. (Update 후) SELECT Data FROM RID_1;
   - 가상의 스냅샷(Read View) 유지.                      - 매 쿼리마다 새 Read View 생성.
   - 현재 데이터는 3000(TID 120).                        - TID 120(나 자신)이 쓴 것임.
   - 120 > 110(A의 시작점)이므로 무시.                    - 결과: 3000 반환 (나의 변경분)
   - RollPtr 따라 Undo Log 추적.
   - TID 100 데이터 발견. 결과: 2000 반환 (일관성 유지)
===================================================================================================
```

- **심층 동작 원리 (이상 현상과 격리 수준의 관계)**:

1. **Dirty Read (오손 읽기)**: 트랜잭션 A가 데이터를 수정하고 커밋하지 않았는데, 트랜잭션 B가 그 값을 읽는 현상입니다. A가 롤백될 경우 B는 존재하지 않는 데이터를 근거로 연산하게 됩니다. (Read Uncommitted에서 발생)
2. **Non-Repeatable Read (반복 불가능한 읽기)**: 트랜잭션 A가 데이터를 읽고 작업하는 중, 트랜잭션 B가 해당 데이터를 수정/삭제하고 커밋하면, A가 다시 읽었을 때 값이 달라지는 현상입니다. (Read Committed 이하에서 발생)
3. **Phantom Read (유령 읽기)**: 트랜잭션 A가 일정 범위의 데이터를 읽었는데, 트랜잭션 B가 그 범위에 새 데이터를 삽입하고 커밋하면, A가 다시 조회했을 때 없던 데이터(유령)가 나타나는 현상입니다. (Repeatable Read 이하에서 발생, 단 MySQL은 Gap Lock으로 방지)

- **핵심 알고리즘 & 실무 코드 예시 (MVCC 가시성 체크 로직 - Pseudo Code)**:

```python
class TransactionManager:
    def __init__(self):
        self.active_transactions = set() # 현재 실행 중인 TID 목록
        self.min_active_tid = 0 # 가장 오래된 트랜잭션 ID

    def can_read_version(self, current_tx, row_version_tid):
        """
        current_tx: 읽기를 수행하는 트랜잭션 객체
        row_version_tid: 데이터 레코드에 적힌 수정 트랜잭션 ID
        """
        # 1. 내가 쓴 데이터는 무조건 볼 수 있음
        if row_version_tid == current_tx.tid:
            return True
            
        # 2. 트랜잭션 시작 전 이미 커밋된 데이터는 볼 수 있음
        if row_version_tid < current_tx.snapshot_min_tid:
            return True
            
        # 3. 트랜잭션 시작 후 생성된 데이터는 볼 수 없음
        if row_version_tid > current_tx.snapshot_max_tid:
            return False
            
        # 4. 트랜잭션 시작 시점에 활성 상태(미커밋)였던 트랜잭션의 데이터는 볼 수 없음
        if row_version_tid in current_tx.active_tid_list_at_start:
            return False
            
        return True # 그 외의 경우는 가시성 인정
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

- **심층 기술 비교 (격리 수준별 특징 및 이상 현상 매트릭스)**:

| 격리 수준 | Dirty Read | Non-Repeatable | Phantom Read | 구현 메커니즘 | 성능 오버헤드 |
|-----------|------------|----------------|--------------|---------------|---------------|
| **READ UNCOMMITTED** | 발생 가능 | 발생 가능 | 발생 가능 | Lock 최소화 (No Lock Read) | 최저 (Very Low) |
| **READ COMMITTED** | **방지** | 발생 가능 | 발생 가능 | 쿼리 단위 Read View (MVCC) | 낮음 (Low) |
| **REPEATABLE READ** | **방지** | **방지** | 발생 가능(표준) | 트랜잭션 단위 Read View (MVCC) | 중간 (Medium) |
| **SERIALIZABLE** | **방지** | **방지** | **방지** | 2PL (Lock 기반) 또는 SSI | 최고 (High) |

- **과목 융합 관점 분석**:
  1. **[보안 융합] 데이터 오염 및 부채널 공격**: 낮은 격리 수준(Read Uncommitted)은 미확정된 데이터 노출을 통해 시스템의 내부 상태를 유추하게 하는 보안 취약점이 될 수 있습니다. 금융권 컴플라이언스(ISMS, PCI-DSS 등)에서는 최소 Read Committed 이상의 격리 수준 적용을 강제합니다.
  2. **[네트워크 융합] 분산 트랜잭션과 CAP 이론**: 분산 데이터베이스 환경에서 격리 수준을 높이면(Consistency 향상), 노드 간 동기화 지연으로 인해 가용성(Availability)이 떨어지게 됩니다. 기술사는 비즈니스 특성에 따라 일관성(C)과 가용성(A) 사이의 타협점을 격리 수준 설정을 통해 결정해야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **기술사적 판단 (실무 시나리오)**:
  1. **온라인 쇼핑몰 선착순 이벤트 (재고 관리)**:
     - **상황**: 수만 명이 동시에 '재고 차감'을 수행할 때, Read Committed 수준에서는 Lost Update가 발생하여 재고보다 더 많은 상품이 팔리는 현상 발생.
     - **전략**: `SELECT ... FOR UPDATE` 구문을 사용하여 조회 시점에 배타적 잠금(X-Lock)을 획득함으로써, 격리 수준과 관계없이 비관적 동시성 제어(Pessimistic Locking)를 적용하여 정합성을 확보합니다.
  2. **대규모 배치 통계 리포트 생성**:
     - **상황**: 수시간 동안 실행되는 통계 쿼리가 실행되는 동안 다른 트랜잭션들이 데이터를 계속 수정하여, 리포트의 합계 수치가 맞지 않는 불일치 발생.
     - **전략**: 해당 세션의 격리 수준을 `REPEATABLE READ`로 상향하여 트랜잭션 시작 시점의 일관된 스냅샷을 보장받거나, 읽기 전용 복제본(Read Replica) 서버에서 쿼리를 수행하여 운영 서버의 부하를 분산합니다.
  3. **Deadlock(교착 상태) 빈번 발생 시**:
     - **상황**: Serializable 수준 사용 중, 여러 트랜잭션이 서로의 락이 풀리기를 무한정 대기하는 데드락 발생.
     - **전략**: 격리 수준을 한 단계 낮추고(Read Committed), 애플리케이션 계층에서 '낙관적 락(Optimistic Lock, 버전 컬럼 활용)'을 사용하여 충돌 시 재시도(Retry)하는 로직으로 전환합니다.

- **도입 시 고려사항 (체크리스트)**:
  - **기술적**: 사용 중인 DBMS의 기본 격리 수준 확인 (Oracle/PostgreSQL은 Read Committed, MySQL은 Repeatable Read가 기본).
  - **운영적**: 격리 수준 상향 시 Undo 세그먼트 사용량 급증으로 인한 Tablespace 부족 현상 모니터링 필수.
  - **애플리케이션**: ORM(JPA, Hibernate) 사용 시 영속성 컨텍스트가 제공하는 1차 캐시와 DB 격리 수준 사이의 괴리로 인한 데이터 혼선 주의.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량적/정성적 기대효과**:

| 효과 영역 | 내용 | 목표 수치 |
|---------|-----|-----------|
| **데이터 정합성** | 트랜잭션 간 데이터 간섭으로 인한 오류 근절 | 무결성 위반 0건 |
| **시스템 처리량** | MVCC 활용을 통한 동시 사용자 수 증대 | TPS 200% 이상 향상 |
| **운영 안정성** | 락 대기 시간(Lock Wait) 감소 및 타임아웃 방지 | 평균 대기 시간 50ms 미만 |

- **미래 전망 및 진화 방향**:
  클라우드 네이티브 데이터베이스와 분산 SQL 환경이 도래하면서, 기존의 단일 노드 중심 격리 수준을 넘어 **'인과적 일관성(Causal Consistency)'**이나 **'외부 일관성(External Consistency)'**과 같은 분산 시스템 특화 격리 모델이 도입되고 있습니다. 또한, 구글의 Spanner처럼 원자 시계(Atomic Clock)를 활용하여 전 지구적 범위에서 Serializable 격리를 보장하는 기술이 상용화되고 있으며, 향후 AI 기반의 쿼리 분석을 통해 트랜잭션별 최적의 격리 수준을 자동 추천하는 자율형 DBMS(Autonomous DB)로 발전할 것입니다.

- **※ 참고 표준/가이드**: 
  - ANSI/ISO SQL-92 (ISO/IEC 9075) Isolation Levels.
  - PostgreSQL SSI (Serializable Snapshot Isolation) Whitepaper.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[ACID 원칙](@/studynotes/05_database/01_relational_model/acid.md)**: 격리 수준이 구현하고자 하는 원자성, 일관성, 고립성, 지속성의 근간.
- **[MVCC (다중 버전 동시성 제어)](@/studynotes/05_database/02_concurrency_control/_index.md)**: 현대적 DBMS가 Lock 없이 격리 수준을 구현하는 핵심 알고리즘.
- **[낙관적 락 vs 비관적 락](@/studynotes/05_database/02_concurrency_control/concurrency_control.md)**: 격리 수준의 한계를 애플리케이션 측면에서 보완하는 동시성 제어 기법.
- **[2단계 잠금 규약 (2PL)](@/studynotes/05_database/_index.md)**: 직렬 가능성을 보장하기 위한 고전적 락 관리 프로토콜.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **격리 수준**은 도서관에서 여러 사람이 책을 고칠 때 서로 방해하지 않게 규칙을 정하는 것과 같아요.
2. 가장 낮은 단계는 옆 사람이 낙서하는 것까지 다 보이는 것이고, 가장 높은 단계는 내가 책을 다 읽을 때까지 아무도 도서관에 못 들어오게 하는 것이에요.
3. 적당한 규칙을 정해야 데이터가 엉망이 되지 않으면서도, 많은 사람이 기다리지 않고 도서관을 이용할 수 있답니다!
