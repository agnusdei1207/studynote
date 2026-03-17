+++
title = "234. Redo (재실행) - 끈기 있는 데이터 반영"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 234
+++

# 234. Redo (재실행) - 끈기 있는 데이터 반영

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Redo (Re-do, 재실행)는 트랜잭션이 성공적으로 완료(Commit)되었으나, 시스템 장애로 인해 **데이터 파일(Data File)에 영구 반영되지 못한 변경 사항을 로그를 기반으로 재수행하여 복구하는 ACID 특성의 핵심 메커니즘**이다.
> 2. **가치**: 트랜잭션의 **영속성(Durability)**을 보장하는 최후의 보루로, "Commit된 데이터는 시스템이 멈추어도 절대 손실되지 않는다"는 데이터 무결성의 신뢰성을 제공하며, RPO(Recovery Point Objective)를 0에 근접하게 만든다.
> 3. **융합**: WAL (Write-Ahead Logging) 프로토콜과 결합하여 버퍼 관리(Buffer Management)의 효율성을 높이며, 복제(Replication) 및 백업(Backup) 복원 과정에서의 'Rollforward' 기능의 물리적 기반이 된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**Redo (Redo Log, 재실행 로그)**는 데이터베이스 시스템(DBMS)이 비정상 종료(Crash) 후 재시작될 때, **커밋(Commit)되었으나 디스크의 데이터 파일에는 반영되지 않은 트랜잭션들의 변경 사항을 다시 재현하는 복구 기법**이다. 이는 데이터베이스의 **원자성(Atomicity)**과 **영속성(Durability)**을 보장하기 위해 설계된 물리적 로그(Physical Log)의 일종이다.

일반적인 데이터베이스는 성능을 위해 데이터 변경을 즉시 디스크에 기록하지 않고, 메모리 상의 **Buffer Pool (Database Buffer Cache)**에 보관한다. 이때, 데이터는 아직 디스크에 쓰이지 않았더라도, 해당 변경 사항을 기록한 **Redo Log**는 즉시 비휘발성 저장소(NVMe/SAN)에 기록된다. 이를 통해 메모리 상의 데이터가 손실되더라도, 로그만 존재하면 동일한 작업을 "다시 실행(Redo)"하여 마지막 정상 상태로 복구할 수 있다.

#### 2. 💡 비유
은행 창구에서 **'거래 확인 스탬프'가 찍힌 전표(Commit)'는 손님에게 건넸지만, 아직 **'은행 원장(디스크)'에 기장을 하지 않은 상태**라고 이해할 수 있다. 만약 이때 정전이 나서 컴퓨터가 꺼지면, 창구 직원은 복구 후 **'전표 사본(Redo Log)'을 보고 다시 원장에 기록**하여 데이터를 맞춘다.

#### 3. 등장 배경 및 필요성
① **기존 한계**: 데이터를 변경할 때마다 매번 디스크의 데이터 파일을 Random Access 방식으로 기록하면, 디스크 헤드의 이동(Seek Time)이 빈번해져 성능이 급격히 저하된다.
② **혁신적 패러다임**: **로그 우선 기록(Write-Ahead Logging)** 방식과 **No-Force 정책**(커밋 시 즉시 디스크 데이터 갱신을 강제하지 않음)을 도입하여, 메모리에서의 작업을 자유롭게 하면서도 안정성을 확보함.
③ **현재 요구**: 클라우드 환경과 대용량 트래픽 환경에서 24/7 가용성을 유지하기 위해, 장애 발생 시 초 단위로 데이터를 일관성 있게 복구해야 하는 필수 요구사항이 됨.

#### 📢 섹션 요약 비유
Redo의 개념은 **'화가가 그림을 그리기 전, 먼저 밑그림을 복사해두는 것'**과 같습니다. 완성된 그림(메모리 데이터)이 찢어지더라도, 밑그림(Redo Log)을 보고 똑같이 다시 그려낼 수 있기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 (표)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/특징 | 비유 |
|:---|:---|:---|:---|:---|
| **Log Buffer** | Redo 로그를 메모리에 일시 저장 | 로그 생성 시 즉시 디스크 쓰기가 아닌 메모리에 축적 후 일괄 기록 (Group Commit) | Circular Buffer | **출입구의 임시 보관함** |
| **Redo Log File** | 로그를 영구 저장하는 순차 파일 | Log Buffer의 내용을 Append-Only 방식으로 기록 (Random I/O 회피) | WAL (Write-Ahead Logging) | **견고한 금고** |
| **LSN (Log Sequence Number)** | 로그 순서 및 고유 ID 관리 | 로그 레코드 생성 시 순차적으로 부여하여, Checkpoint 및 복구 시 순서 보장 | Monotonically Increasing | **일련 번호** |
| **Dirty Page** | 디스크와 다른 상태의 데이터 페이지 | 변경되었지만 아직 디스크에 Flush되지 않은 상태 (Redo의 대상) | Buffer Pool 상태 | **미송금 계산서** |
| **Checkpointer (CKPT)** | 복구 속도 최적화 및 로그 관리 | 주기적으로 Dirty Page를 디스크에 Flush하고, 해당 시점의 LSN을 기록 | Fuzzy Checkpoint | **중간 결산 시점** |

#### 2. 아키텍처 및 데이터 흐름

```text
      [ CLIENT REQUEST ] 🔽
           ▼
      +-----------------------------------+
      |  1️⃣  TRANSACTION MANAGER (Tx)     |
      |  - Begin Transaction              |
      |  - Update Data (Memory)           |
      +-----------------------------------+
           | (Update)
           ▼
      +-----------------------------------+
      |  2️⃣  BUFFER POOL (SGA/Shared)     |
      |  - Data Block: Modified (Dirty)   |
      |  - State: In-Memory Only          |
      +-----------------------------------+
           | (Log Generation)
           ▼
      +-----------------------------------+      Append      +------------------+
      |  3️⃣  LOG BUFFER (Memory)          |  --------------->|  4️⃣ REDO LOG FILE|
      |  - Sequential Write               |                  |  - Sequential I/O|
      +-----------------------------------+                  |  - Persistent    |
           |                                          |    +------------------+
           |  COMMIT Signal                           |           |
           ▼                                          ▼           ▼
      +---------------------------------------------------------------+
      |  5️⃣ LOG WRITER (LGWR) / Writer Process                        |
      |  - "Commit" 발생 시 Log Buffer -> Redo Log File로 즉시 Flush   |
      |  - 💡 COMMIT의 완료 조건: Log가 디스크에 쓰여졌는지 확인      |
      +---------------------------------------------------------------+
           ▼
      [ SUCCESS TO CLIENT ]
      (주의: 데이터 파일은 아직 예전 값, 로그는 최신 값)
```

#### 3. 다이어그램 심층 해설
위 다이어그램은 **WAL (Write-Ahead Logging)** 원칙을 시각화한 것이다. 사용자가 `Commit`을 요청하면, 데이터베이스는 변화된 데이터 페이지(Data Block)를 디스크에 쓰는 대신, **로그 버퍼(Log Buffer)에 있는 내용을 먼저 Redo Log File로 기록(LGWR)**한다. 이때 Redo Log 파일은 순차 쓰기(Sequential Write)만 수행하므로, 데이터 파일의 랜덤 쓰기(Random Write)보다 훨씬 빠르다.
따라서 시스템 장애(Crash)가 발생하면, 복구기(Recovery Manager)는 **Redo Log File**을 스캔하여 **LSN 1번부터 마지막 기록까지 순차적으로 재생(Rollforward)**함으로써, 데이터 파일의 내용을 최종 커밋 상태로 일치시킨다.

#### 4. 핵심 알고리즘: Redo의 Idempotency (멱등성)
Redo 로그의 핵심 원리 중 하나는 **멱등성(Idempotency)**이다. 복구 과정에서 로그를 한 번 적용하든, 여러 번 적용하든 결과는 동일해야 한다. 이를 위해 Redo 로그는 **논리적 로그(Logical Log, 예: "A값을 1 더해")가 아닌 물리적 로그(Physical Log, 예: "Offset 100에 50이라는 값 쓰기") 형태**를 주로 사용한다.

```sql
-- [논리적 로그의 문제점 예시]
-- 장애 전: A=10 -> Update A+10 (Log: +10) -> A=20 (Commit) -> Crash
-- 복구 시: A가 20인 상태에서 다시 Log(+10)를 적용하면 A=30이 되어버림 (오류 발생!)

-- [물리적 Redo 로그의 안전성 예시]
-- Log: {PageID: 5, Offset: 200, Value: 'Value_X'}
-- 복구 시: 무조건 해당 위치에 'Value_X'를 쓴다. (현재 값이 무엇이든 상관없이 최종값으로 덮어씀)
```
이러한 물리적 로그 방식은 복구 시점이 애매하거나, 이미 일부 적용된 상태에서 다시 적용해도 데이터 무결성이 깨지지 않음을 보장한다.

#### 📢 섹션 요약 비유
Redo의 작동 방식은 **'비행기의 블랙박스'**와 같습니다. 비행기(데이터)가 추락하더라도, 블랙박스(Redo Log)에 기록된 센서 값과 조작 기록을 순서대로(순차 읽기) 재연(Replay)하면 사고 직전의 상태를 정확히 복원할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Redo vs Undo

| 구분 | Redo (재실행) | Undo (취소) |
|:---|:---:|:---:|
| **목적** | **영속성(Durability)** 보장 | **원자성(Atomicity)** 보장 |
| **대상** | **Commit된 트랜잭션** (Disk 반영 안 된 것) | **Rollback 요청** 또는 **Crash 시 미완료 트랜잭션** |
| **시점** | Crash 후 복구 시 (Rollforward Phase) | Crash 후 복구 시 (Rollback Phase) 또는 사용자 요청 시 |
| **로그 성격** | **변경 전 후 값(P redo, A after image)** 또는 **물리적 재기록 값** | **변경 전 값(Undo Log, Before Image)** |
| **기술적 메커니즘** | Log의 "Redo Record"를 순차적으로 재생 | Log의 "Undo Record"를 역순으로 적용 (Compensating Transaction) |
| **성능 영향** | 순차 쓰기로 인해 적은 오버헤드 (Buffer로 Batch) | Rollback 시 많은 연산 필요 (잠금 경합 가능성 있음) |

#### 2. 아키텍처 융합 관점

**A. Buffer Management와의 시너지 (No-Force & Steal)**
데이터베이스는 **No-Force** (커밋 시 Dirty Page를 디스크에 쓰지 않음)와 **Steal** (커밋되지 않은 Dirty Page를 디스크에 쓸 수 있음) 정책을 사용하여 성능을 극대화한다. Redo 로그는 이러한 공격적인 버퍼 관리 전략을 가능하게 한다.
*   *관계*: Redo가 없다면, No-Force 정책을 쓸 수 없어 커밋마다 디스크 I/O가 발생해 성능이 폭락한다. Redo는 "로그만 기록되면 완료"라는 **Lazy Write**를 가능하게 한다.

**B. Replication (복제)와의 융합**
MySQL이나 Oracle의 **Physical Standby DB**는 마스터 DB로부터 Redo Log를 전송받아 적용함으로써 동기화한다.
*   *관계*: Redo는 **가장 원초적인 데이터 변경 단위**이므로, 이를 그대로 전송하여 복제본(Replica)을 만드는 것이 데이터 일치성을 보장하는 가장 확실한 방법이다. 복제 지연(Replication Lag)을 줄이기 위해 Redo Log의 배치(Batch) 크기와 전송 빈도를 튜닝하는 것이 주요 이슈가 된다.

**C. Checkpoint (검사점)와의 상관관계**
Redo 로그는 끊임없이 증가한다. 하지만 모든 로그를 다시 재생하면 복구 시간이 너무 오래 걸린다. 따라서 **Checkpoint**(현재 시점의 모든 Dirty Page를 디스크에 반영하는 작업)를 수행한다.
*   *수학적 관계*: `복구 시간 = (마지막 LSN - Checkpoint LSN) * 로그 적용 속도`. Checkpoint를 빈번하게 수행하면 Redo 로그가 덜 필요해져 복구가 빠르지만, 시스템 부하가 증가하는 트레이드오프(Trade-off) 관계가 있다.

#### 📢 섹션 요약 비유
Redo와 Undo의 관계는 **'비디오 편집 소프트웨어'**와 같습니다. Redo는 **'자동 저장(Auto-save)'된 기록**을 이용해 파일이 닫혔어도 마지막 저장 상태로 불러오는 기능이고, Undo는 사용자가 실수를 했을 때 **'되돌리기(Ctrl+Z)'**를 눌러 작업을 취소하는 기능입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스

| 시나리오 | 상황 | Redo 활용 및 기술적 판단 | 예상 지표 (Metric) |
|:---|:---|:---|:---|
| **S1. 전원 실패** | 정전으로 인한 DB 서버 Down | 최초 부팅 시 **Crash Recovery** 수행. Redo Log의 마지막 LSN까지 순차 적용(Rollforward). | RTO < 5분 (성능에 따라 다름) |
| **S2. 미디어 장애** | 디스크(Data File) 파손 | **Time-based Recovery**: 특정 시점(PITR)의 Redo Log(Archive Log)를 백업본에 순차 적용하여 완전 복구. | RPO = 0 (최신 상태 복구 가능) |
| **S3. 대용량 트랜잭션** | 배치 작업 중 장애 | Redo Log 파일이 가득 차지 않도록 **Log Switch** 발생 및 **Archiver Process**가 이를 백업으로 복사. | I/O Spike 관리 필요 |

#### 2. 도입 및 운영