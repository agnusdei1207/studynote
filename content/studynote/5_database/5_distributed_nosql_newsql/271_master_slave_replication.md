+++
title = "271. 마스터-슬레이브 (Master-Slave) 복제 - 읽기 분산의 정석"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 271
+++

# 271. 마스터-슬레이브 (Master-Slave) 복제 - 읽기 분산의 정석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **MSR (Master-Slave Replication)**은 쓰기 연산을 전담하는 단일 권한자(Master)와 데이터를 복제하여 읽기만 담당하는 다수의 노드(Slave)로 구성된 **비대칭형 데이터 아키텍처**로, 데이터 정합성을 보장하며 조회 성능을 극대화하는 고전적인 패턴입니다.
> 2. **가치**: **RDBMS (Relational Database Management System)**의 무결성(Acid)을 유지하면서도, **Read Intensive**한 웹 서비스 환경에서 **Horizontal Scaling (수평 확장)**을 통해 조회 처리량(Read TPS)을 선형적으로 늘릴 수 있는 가장 확실한 동시성 제어 기법입니다.
> 3. **융합**: **HA (High Availability)** 클러스터링의 핵심 기반이며, 장애 조치(Failover) 시 **Raft** 또는 **Paxos** 알고리즘과 연계하여 새로운 Master 선출(Promotion)을 자동화하는 분산 시스템의 기초가 됩니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**MSR (Master-Slave Replication)**은 데이터베이스 시스템에서 **단일 쓰기 권한(Single Source of Truth)**을 유지하면서 읽기 작업을 분산시키기 위해 설계된 아키텍처입니다.
마스터 노드는 트랜잭션의 원천으로서 데이터의 변경(CUD: Create, Update, Delete)을 독점하고, 슬레이브 노드들은 마스터의 데이터 사본(Replica)을 보유하여 일관성 있는 조회(Read) 서비스를 제공합니다. 이는 분산 시스템에서 발생할 수 있는 **데이터 충돌(Write Conflict)** 문제를 구조적으로 원천 봉쇄함으로써, 복잡한 분산 락(Distributed Lock)이나 합의 알고리즘의 오버헤드 없이 높은 데이터 신뢰성을 제공합니다.

#### 2. 등장 배경
① **일반적 하드웨어의 한계**: 단일 DB 서버의 **CPU (Central Processing Unit)** 및 I/O 대역폭 한계로 인해, 증가하는 트래픽을 감당하기 어려운 병목 현상 발생.
② **수직 확장의 비효율**: 고사양 서버(Scale-up)로의 교체 비용이 기하급수적으로 상승하고, 물리적 한계가 존재함.
③ **Read/Write 패턴의 불균형**: 대부분의 웹 서비스(SNS, 커머스)는 조회(Read) 요청이 쓰기(Write)의 5:1에서 10:1 이상의 비중을 차지함에 착안하여, 읽기 부하만 분리하여 처리하는 패러다임 등장.

#### 3. 💡 비유
이는 **"방송국의 뉴스 시스템"**과 유사합니다. 앵커(마스터)가 뉴스 원고를 쓰고 방송(쓰기)하면, 시청자들(슬레이브)은 그 내용을 확인(읽기)할 뿐 내용을 수정할 수 없습니다. 앵커는 오직 하나여야 뉴스의 정확성이 보장되지만, 시청자는 전 세계 몇 명이든 가능합니다.

#### 📢 섹션 요약 비유
마스터-슬레이브 복제는 **'유명 맛집의 본점과 체인점'** 운영 전략과 같습니다. 메뉴 개발과 레시피 수정(쓰기)은 본점(Master) 사장님이 단독으로 결정하고, 모든 체인점(Slave)은 본점에서 전송된 레시피대로만 요리를 해서 손님(클라이언트)에게 제공합니다. 이렇게 해야 맛의 퀄리티(데이터 정합성)가 유지되면서, 손님 북적임(트래픽)은 전국의 체인점들이 나누어 처리할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 및 역할
MSR 아키텍처를 구성하는 주요 엔티티와 내부 동작 메커니즘은 다음과 같습니다.

| 요소명 | 역할 | 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Master (Primary)** | **쓰기 전용 관리자** | 트랜잭션 처리 및 Redo Log 기록 | Binary Log / WAL | **본점 주방장** |
| **Slave (Replica)** | **읽기 전용 서버** | Master의 로그 수신 및 재현(Relay) | I/O Thread, SQL Thread | **지점 주방장** |
| **Binary Log** | **변경 이력 저장소** | Commit 시 데이터 변경 사항(행 단위/구문) 기록 | Row-based / Statement | **레시피 전달 팩스** |
| **Replication Thread** | **동기화 스레드** | <ul><li>**I/O Thread**: Master 로그를 Slave로 가져옴</li><li>**SQL Thread**: 가져온 로그를 실행</li></ul> | TCP/IP | **배달 직원 & 요리사** |
| **Connector/Proxy** | **요청 분배기** | SQL 문장 분석(Parsing)하여 Read/Write 라우팅 | MySQL Proxy / ProxySQL | **매장 안내 직원** |

#### 2. 아키텍처 구조 및 동작 흐름
아래 다이어그램은 클라이언트의 요청이 마스터와 슬레이브로 어떻게 분배되고, 데이터가 어떻게 동기화되는지를 나타냅니다.

**[도입 서술]**
애플리케이션 서버는 데이터 요청 발생 시 **SQL Routing Layer**를 거쳐 `INSERT/UPDATE/DELETE`는 Master로, `SELECT`는 Slave로 전송합니다. Master는 데이터 변경이 발생할 때마다 **Binary Log**에 기록하고, Slave의 **I/O Thread**가 이를 네트워크로 전송받아 **Relay Log**에 저장합니다. 이후 Slave의 **SQL Thread**가 Relay Log를 순차적으로 실행하여 Master와 동일한 데이터 상태를 만듭니다.

```text
[Master-Slave Replication Flow & Data Path]

     [ Application Server ]
             |
             v
    +------------------+          (Write Path: Single Source)
    | SQL Routing Layer| ------------------------------> INSERT/UPDATE/DELETE
    +------------------+                                        |
          |  |                                                    v
          |  | (Read Path: Distributed)              +-------------------------+
          |  +-------------------------------------> |  Master DB (Primary)    |
          |                                        | - Write Transaction     |
          |                                        | - Binary Log Generation |
          |                                        +-------------------------+
          |                                                  |
          |                        (1) Dump Binary Log       |
          +--------------------------------------------------> (Network Push)
                                                                     |
                                                                     v
      +------------------+                                 +------------------+
      |    Read Load     |                                 |    Slave DB 1    |
      | (SELECT Queries) | <-------------------------------| (Replica/Standby)|
      +------------------+    (3) Serve Data               | - I/O Thread     |
                                                         | - SQL Thread     |
                                                         | - Relay Log      |
                                                         +------------------+
```

**[다이어그램 해설]**
1.  **쓰기 경로(빨간색/화살표 ①)**: 모든 데이터 변경은 Master를 거쳐야 합니다. Master는 트랜잭션 커밋 시 변경 사항을 Binary Log에 기록합니다. 이 과정에서 **Durability (내구성)**이 보장됩니다.
2.  **복제 경로(데이터 전송)**: Slave의 I/O Thread가 Master에 접속하여 Binary Log 이벤트를 요청하고, Master는 변경된 내용을 실시간으로 전송합니다. Slave는 받은 내용을 로컬 디스크의 Relay Log에 기록합니다.
3.  **재현 경로(Slave 내부)**: Slave의 SQL Thread가 Relay Log를 읽어 실제 DB 데이터를 반영(Replay)합니다. 이 반영이 완료된 시점에야 Slave는 최신 데이터를 가진 상태가 되어 Read 요청을 처리할 준비가 됩니다.

#### 3. 핵심 동작 원리 (Step-by-Step)
1.  **트랜잭션 커밋**: 사용자가 `UPDATE` 실행 → Master DB InnoDB 엔진이 데이터 수정 → Binary Log에 기록 → Commit 완료.
2.  **로그 전송 (Dumping)**: Slave의 I/O Thread가 Master에 접속 → "마지막 읽은 위치(Binary Log Position) 이후의 로그를 줘" 요청 → Master 전송.
3.  **로그 재현 (Execution)**: Slave는 전송받은 로그를 Relay Log 저장 → SQL Thread가 순차적 읽기 및 실행 → Slave DB 데이터 업데이트.
4.  **일관성 확인**: `Seconds_Behind_Master` 값(MySQL 경우)을 통해 Slave가 Master보다 얼마나 뒤처져 있는지 모니터링.

#### 4. 핵심 알고리즘 및 코드 (Binary Log Position Check)
데이터베이스 관리자는 복제 상태를 점검하기 위해 다음과 같은 시스템 테이블을 조회합니다. 다음은 MySQL 복제 상태 확인을 위한 쿼리 예시입니다.

```sql
-- [MySQL/MariaDB] Slave 상태 확인 쿼리
-- Master와의 로그 포지션(Position) 차이를 확인하여 지연(Lag)을 측정합니다.

SHOW SLAVE STATUS\G

-- [주요 출력 파라미터 해석]
-- 1. Slave_IO_Running: Yes (마스터 로그를 가져오는 스레드가 살아있는가?)
-- 2. Slave_SQL_Running: Yes (로그를 실행하는 스레드가 살아있는가?)
-- 3. Master_Log_File vs Relay_Master_Log_file (현재 동기화 중인 로그 파일명)
-- 4. Exec_Master_Log_Pos (마지막으로 실행된 로그 위치)
-- 5. Seconds_Behind_Master (지연 시간, 0이어야 정상)
```

#### 📢 섹션 요약 비유
이 과정은 **'악보 복사 및 연습'** 과정과 같습니다. 작곡가(Master)가 새로운 악보(Binary Log)를 완성하면, 제자들(Slave)은 악보를 배송(I/O Thread) 받아 자신의 악보집(Relay Log)에 넣습니다. 그 후, 제자들은 그 악보를 보며 연주(SQL Thread)를 하여 작곡가의 연주와 똑같이 만듭니다. 배송과 연습 시간이 걸리기 때문에, 제자가 연주를 시작할 때는 이미 작곡가는 다음 곡을 쓰고 있을 수 있습니다(Replication Lag).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 동기식 vs 비동기식 복제
MSR은 데이터 동기화 타이밍에 따라 시스템의 안정성과 성능이 크게 달라집니다. 이는 **CAP 정리(Theorem)**의 Consistency(일관성)와 Availability(가용성) 트레이드오프와 직결됩니다.

| 비교 항목 | 비동기 복제 (Asynchronous) | 반동기 복제 (Semi-Synchronous) | 동기 복제 (Synchronous) |
|:---|:---|:---|:---|
| **동작 방식** | Master가 Slave로 전송 후 즉시 클라이언트 응답 | **최소 1개의 Slave**가 로그 수신 확인을 보내오면 응답 | **모든 Slave**가 트랜잭션 완료해야 응답 |
| **성능 (Latency)** | **최고** (Slave 대기 시간 없음) | **중간** (1개 Slave ACK 대기) | **최저** (가장 느린 Slave에 의존) |
| **데이터 안전성** | 낮음 (장애 시 최신 데이터 유실 가능) | 높음 (1개 노드에는 확실히 저장됨) | 최고 (모든 노드에 저장됨) |
| **장애 복구 (RPO)** | 데이터 손실 발생 가능 | 데이터 손실 최소화 | 데이터 손실 없음 (Zero RPO) |
| **주요 용도** | 대부분의 웹 서비스, 캐시 용도 | 금융 거래, 결제 시스템 | 분산 DB(Cluster), 안전이 중요한 시스템 |

#### 2. 과목 융합 관점: OS 및 네트워크와의 시너지
-   **OS (Operating System)와 I/O Multiplexing**: 복제 과정에서 Slave는 Master의 로그를 기다리며 `Blocking I/O` 상태에 놓이게 됩니다. 효율적인 복제를 위해 OS 커널 레벨의 **I/O Multiplexing (select, poll, epoll 등)** 기술이 사용되어, 하나의 스레드로 수많은 Master-Slave 연결을 효율적으로 관리합니다.
-   **네트워크 혼잡 제어**: 대규모 트래픽 발생 시 Master-Slave 간 로그 전송이 망을 점유할 수 있습니다. 이때 **TCP (Transmission Control Protocol)**의 흐름 제어(Flow Control) 및 혼잡 제어(Congestion Control) 메커니즘이 작동하여 복제 속도가 조절됩니다. 네트워크 대역폭이 병목이 되어 Slave가 `Seconds_Behind_Master`가 급증하는 현상은 전형적인 **Network I/O Bottleneck**입니다.

#### 📢 섹션 요약 비유
비동기 복제는 **'편지 전달'**과 같습니다. 우체부(Master)가 편지를 우체함에 넣고 배달 완료라 생각하지만, 실제로 수신자(Slave)에게 배달되기까지 시간이 걸리고 중간에 분실될 위험도 있습니다. 반동기 복제는 **'등기 우편'**처럼 받는 사람이 도장을 찍어야(ACK) 배달이 완료된 것으로 간주하여 안전성을 높인 방식입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스
MSR 도입 시 고려해야 할 주요 의사결정 기준은 다음과 같습니다.

| 구분 | 문제 상황 | 의사결정 (Action) | 기술적 근거 |
|:---|:---|:---|:---|
| **성능** | 조회 속도가 느리고 DB CPU 100% | **Slave 추가 (Scale-out)** | 읽기 부하는 선형적으로 분산되어 처리 용량 증대 |
| **정합성** | 결제 완료 후 내역이 안 보임 | **Write 후 Read 전략 강제** | 방금 쓴 데이터는 Slave가 아닌 Master에서 조회 (Read-After-Write Consistency) |
| **장애** | Master 서버 다운 (Panic) | **자동 페일오버(Failover) 트리거** | Sentinel(Redis) 또는 MHA(MySQL)가 Slave를 Master