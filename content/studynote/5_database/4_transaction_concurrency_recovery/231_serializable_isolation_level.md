+++
title = "231. Serializable (레벨 3) - 완벽한 고립의 정점"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 231
+++

# 231. Serializable (레벨 3) - 완벽한 고립의 정점

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL 표준에서 정의하는 최상위 격리 수준으로, **여러 트랜잭션(T1, T2...)이 동시에 실행되더라도 그 결과가 반드시 시간축 상의 어떤 순서대로(직렬) 실행한 것과 수학적으로 동일함을 보장**하는 가장 엄격한 격리(Serializability) 원리이다.
> 2. **가치**: 비반복 읽기(Non-Repeatable Read)와 유령 읽기(Phantom Read)를 포함한 모든 동시성 이상 현상(Concurrency Anomaly)을 완벽히 차단하여, 데이터 무결성(Integrity)을 '절대적' 수준으로 보장한다.
> 3. **융합**: 읽기 작업 시에도 공유 락(S-Lock)을 트랜잭션 종료 시까지 유지하거나, 인덱스 범위에 갭 락(Gap Lock) 및 넥스트 키 락(Next-Key Lock)을 거는 방식(주로 MySQL InnoDB)으로 구현되며, 분산 DB의 정합성 확보에도 핵심적인 역할을 한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**Serializable (직렬화 가능성)**은 데이터베이스 트랜잭션 격리 수준(Transaction Isolation Level) 중 가장 높은 단계(레벨 3)이다. 단순히 데이터의 일관성을 넘어, 동시에 실행된 병렬 트랜잭션의 결과 집합(Result Set)이 "어떤 순서대로 하나씩 실행했을 때의 결과와 정확히 일치함"을 수학적으로 보장한다. 이는 ANSI/ISO SQL 표준(ANSI/ISO SQL Standard)에서 정의하는 이상적인 격리 모델이다.

**💡 비유: 도서관의 단독 대관**
일반적인 상황(낮은 격리 수준)에서는 여러 사람이 도서관에 들어와 책을 보고的书架에 꽂아도 서로 모르는 사이에 책 내용이 바뀔 수 있다. 하지만 Serializable은 **도서관 전체를 한 사람이 단독으로 대관한 것과 같다**. 대관하는 동안은 문이 잠겨 있어 다른 누구도 들어오거나 나갈 수 없으므로, 책의 내용이 대관 시작 시점과 종료 시점이 완벽히 동일함을 보장한다.

**등장 배경: 데이터의 신뢰도 위기**
1.  **기존 한계 (Repeatable Read)**: 트랜잭션 내에서 동일한 레코드를 두 번 읽을 때는 내용이 같지만, 새로운 행(Row)이 추가되는 **유령 읽기(Phantom Read)** 현상은 막지 못했다.
2.  **혁신적 패러다임 (Serial Execution)**: "겉보기에 직렬(Serializable)"인 것을 넘어, 실제로 논리적으로 순서를 강제하여 유령 데이터 자체의 생성을 차단하는 물리적 락킹(Locking) 또는 순차적 예약(Serialization) 기법이 도입되었다.
3.  **현재의 비즈니스 요구**: 금융 결제, 재고 관리 등 1원의 오차나 1개의 재고 오차도 허용되지 않는 **초고무결성(High Integrity)** 시스템에서 필수적인 선택지가 되었다.

**📢 섹션 요약 비유**
Serializable은 도로에서 모든 차량에게 **"모든 신호등을 빨간 불로 켜고, 한 대씩 번호표를 뽑아 교차로를 건너게 하는 것"**과 같습니다. 교통 사고(데이터 불일치)는 0%에 수렴하지만, 전체 교통 흐름(처리량)은 바닥으로 떨어지게 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (표)**
Serializable을 구현하기 위해 DBMS(DataBase Management System) 내부에서 동작하는 핵심 메커니즘은 다음과 같다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Shared Lock (S-Lock)** | 읽기 무결성 보호 | `SELECT` 실행 시 획득하며, **트랜잭션 종료(COMMIT/ROLLBACK) 시까지 해제하지 않음**. 다른 트랜잭션의 쓰기를 방지. | 책을 읽는 동안 다른 사람이 수정하는 것을 원천 봉쇄 |
| **Range Lock (Predicate Lock)** | 범위 데이터 보호 | `WHERE` 조건에 일치하는 **인덱스 범위 자체에 락**을 걸어, 해당 범위 내의 INSERT를 방지함 (유령 읽기 차단). | 빈 책꽂이 공간까지 "여기는 건드리지 마"라고 표시 |
| **Next-Key Lock** | 범위+레코드 락 (MySQL) | **Record Lock + Gap Lock**의 결합. 인덱스 레코드와 그 바로 앞 빈 공간(Gap)을 함께 잠금. | 책과 책 사이 빈틈을 포함하여 구간 전체를 점유 |
| **SSI (Serializable Snapshot Isolation)** | 비락킹 구현 (PostgreSQL 등) | 락 대신 스냅샷을 활용하되, 쓰기 충돌(Write Skew) 가능성이 있으면 트랜잭션을 강제로 중단(Abort)시킴. | 충돌 감지 시 시간을 되돌려 다시 처리하게 함 |

**ASCII 구조 다이어그램: Serializable 락킹 메커니즘 (Range Lock)**
아래는 유령 읽기(Phantom Read)를 방어하기 위해 **인덱스 범위 락(Gap Lock)**이 어떻게 동작하는지 도식화한 것이다. T1이 `id BETWEEN 10 AND 20`을 조회하면, 그 사이의 빈 공간까지 잠긴다.

```text
[Serializable Range Locking Structure]

  Table: Accounts (Indexed by ID)

  [ID: 05]     (Gap)     [ID: 10]     (Gap)     [ID: 20]     (Gap)     [ID: 30]
     │                      │                       │                       │
     │                      │                       │                       │
     └──────────────────────┼───────────────────────┼───────────────────────┘
                            │                       │
                            ▼                       ▼
                 [ LOCKED GAP (Range) ]      [ LOCKED GAP (Range) ]
                 👁️ T1: S-Lock Active       👁️ T1: S-Lock Active
     
     
  T1 Transaction: SELECT * FROM Accounts WHERE ID >= 10 AND ID < 30;
  -> 결과: 10, 20 반환. 
  -> 내부 동작: ID=10~30 사이의 모든 인덱스 키와 빈 공간(Gap)에 S-Lock 획득.

  ------------------------------------------------------------------
  
  T2 Transaction: INSERT INTO Accounts VALUES (15); 
       │
       ├── ① [ID:10]과 [ID:20] 사이의 Gap이 잠겨 있음을 감지
       └── ② ❌ BLOCKED (Lock Wait Timeout 발생 가능)

  ------------------------------------------------------------------
  
  Result: T1은 범위 내에 새로운 데이터가 들어오는 것을 완벽히 차단함.
```

**다이어그램 해설**
이 다이어그램은 **S-Lock**이 단순히 존재하는 레코드(Record)뿐만 아니라, **데이터가 삽입될 수 있는 빈 공간(Gap)** 까지 확장된다는 점을 보여준다. 
1. **도입**: T1이 조건부 검색을 수행하면 DBMS는 B-Tree 인덱스 상에서 조건을 만족하는 리프 노드뿐만 아니라, 인접한 빈 공간(Gap)에도 '간격 락(Gap Lock)'을 설정한다.
2. **구조**: 화살표로 표시된 것처럼, [ID:10]과 [ID:20] 사이의 가상의 공간이 T1에 의해 점유된다.
3. **동작**: T2가 새로운 레코드(ID:15)를 삽입(Insert)하려 하면, 데이터 파일의 여유 공간이 아닌 **인덱스의 논리적 간격**이 잠겨 있어 락 매니저(Lock Manager)가 이를 즉시 차단한다. 이것이 바로 유령 읽기가 발생하지 않는 이유이다.

**심층 동작 원리: 2PL (Two-Phase Locking)의 적용**
Serializable은 보통 **2단계 락킹(Two-Phase Locking, 2PL)** 프로토콜을 기반으로 동작한다.
1.  **성장 단계 (Growing Phase)**: 트랜잭션 시작 후 `LOCK` 명령어만 수행 가능하며, 락을 획득(S/X-Lock Acquire)하는 단계이다. (읽기 시작)
2.  **축소 단계 (Shrinking Phase)**: 트랜잭션이 첫 번째 `UNLOCK`을 수행하면, 이후에는 어떤 락도 획득할 수 없고 해제(Unlock)만 수행한다.
    *   *이때, Serializable은 축소 단계(락 해제)가 트랜잭션 커밋(Commit) 시점까지 미뤄지는 '엄격한 2PL(Strict 2PL)'을 사용한다.*

**핵심 알고리즘 및 코드**
아래는 Serializable 환경에서 발생할 수 있는 데드락 상황과 이를 해결하기 위한 로직을 보여주는 Pseudo-Code이다.

```sql
-- T1: A 계좌에서 B 계좌로 송금 (Serializable Isolation)
BEGIN TRANSACTION;
    -- 1. 읽기 시 S-Lock 획득 (트랜잭션 종료 시 유지)
    SELECT balance FROM Accounts WHERE id = 'A'; 
    
    -- 2. 갱신 시 X-Lock(Exclusive Lock) 획득 (S-Lock에서 업그레이드됨)
    UPDATE Accounts SET balance = balance - 1000 WHERE id = 'A';
    
    -- [T2가 여기서 B를 읽거나 쓰려고 시도하면 Block됨]
    
    UPDATE Accounts SET balance = balance + 1000 WHERE id = 'B';
COMMIT; -- 여기서 모든 락 해제
```

**📢 섹션 요약 비유**
Serializable은 **'보안 검색대의 1차선 정책'**과 같습니다. 검색대 직원은 내 가방을 검사하고 난 뒤(S-Lock), 내가 완전히 영역을 벗어날 때(COMMIT)까지 다음 사람에게 가방을 건네주지 않습니다. 검사대는 지극히 안전하지만, 줄은 뒤로 늘어나기 마련입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교표**
Serializable은 격리 수준의 정점에 있으며, 하위 수준인 Repeatable Read와의 기술적 차이는 명확하다.

| 구분 | Repeatable Read (레벨 2) | **Serializable (레벨 3)** |
|:---|:---|:---|
| **동시성 이상 방어** | Non-Repeatable Read, Dirty Read 방어 | 모든 이상 현상(Phantom Read 포함) 완전 차단 |
| **락킹 범위** | Row (레코드) 단위 기반 | **Row + Range (범위)** 단위 기반 |
| **구현 비용** | 중간 (인덱스 락 필요) | 매우 높음 (범위 락 또는 충돌 감시 오버헤드) |
| **Throughput (TPS)** | 높음 (동시 처리 유리) | 낮음 (병목 발생 빈번) |
| **Write Skew** | 발생 가능 (DB 종류 따름) | **차단됨** |

**과목 융합 관점: OS 및 네트워크와의 시너지**
1.  **운영체제 (OS) & 동시성 제어**: Serializable의 락 관리는 OS의 **세마포어(Semaphore)** 및 **뮤텍스(Mutex)** 메커니즘과 직결된다. 하지만 DB의 락은 테이블, 페이지, 로우 등 세분화된 계층 구조를 가지며, 이를 관리하기 위해 **Lock Manager(Lock Manager)** 라는 독립된 DBMS 내부 모듈이 전담한다.
2.  **네트워크 & 분산 트랜잭션**: 분산 환경에서 Serializable을 보장하기 위해서는 **2단계 커밋(2PC, Two-Phase Commit)** 프로토콜이 필수적이다. 모든 노드가 동일한 시점에 데이터를 일관되게 유지해야 하므로, 네트워크 지연(Latency)이 전체 성능에 치명적인 영향을 미친다.
3.  **오버헤드**: 락 획득/해제 및 교착 상태(Deadlock) 감지를 위한 **Wait-for Graph** 순환 검사가 주기적으로 발생하므로 CPU 연산 자원을 상당히 소모한다.

**ASCII 다이어그램: 격리 수준별 데이터 가시성 (Matrix)**
어떤 현상이 방지되는지 시각적으로 비교한다.

```text
[Isolation Level Defense Matrix]

Level      | Dirty Read | Non-Repeatable | Phantom Read | Performance
-----------|:----------:|:--------------:|:------------:|:-----------:
Read Uncomm|     ❌     |       ❌       |      ❌      |   ⚡️ High
-----------|------------|----------------|--------------|-------------
Read Comm  |     ✅     |       ❌       |      ❌      |   ⚡️ Med-High
-----------|------------|----------------|--------------|-------------
Repeatable |     ✅     |       ✅       |      ❌      |   🚗 Med
-----------|------------|----------------|--------------|-------------
SERIALIZBLE|     ✅     |       ✅       |      ✅      |   🐌 Low
                                 ▲
                                 |
                    [ Target Feature: Absolute Safety ]
```

**📢 섹션 요약 비유**
Serializable과 하위 수준의 차이는 **'독립 서재'와 '열람실'의 차이**와 같습니다. 열람실(Repeatable Read)은 자기 책상이 보이지만, 누군가 들어와서 옆 자리에 앉거나 걸어 다니는 것(유령 데이터)은 볼 수 있습니다. 독립 서재(Serializable)는 문을 걸어 잠그므로 내가 보는 것 외에는 세상에 존재하는 그 어떤 것도 내 시야에 들어오지 않습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오: 의사결정 매트릭스**
1.  **시나리오 A: 결제 시스템 (충천 독점)**
    *   상황: 사용자가 잔고를 확인하고 결제를 진행할 때, 확인 사이에 다른 곳에서 돈이 인출되면 잔고가 부족해질 수 있다.
    *   판단: **Serializable** 사용. 잔고 조회 시 범위 락을