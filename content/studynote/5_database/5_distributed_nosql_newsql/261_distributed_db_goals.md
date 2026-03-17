+++
title = "261. 분산 데이터베이스(Distributed Database)의 목표"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 261
+++

# 261. 분산 데이터베이스(Distributed Database)의 목표

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 데이터베이스(Distributed Database)의 궁극적 목표는 물리적으로 분산된 저장소를 논리적으로 통합하여, 사용자에게 **단일 시스템 이미지(Single System Image)**를 제공하는 투명성(Transparency)을 확보하는 데 있다.
> 2. **가치**: 중앙 집중식 시스템의 병목을 해소하여 **확장성(Scalability)**을 확보하고, 데이터 복제(Replication)를 통해 **고가용성(High Availability)** 및 장애 격리(Failure Isolation)를 달성하여 RTO(복구 시간 목표)를 획기적으로 단축한다.
> 3. **융합**: 분산 컴퓨팅(Distributed Computing) 이론과 네트워킹 기술이 결합된 구조로, CAP 정리(Consistency, Availability, Partition Tolerance)의 상충 관계를 이해하여 클라우드 네이티브(Cloud-Native) 아키텍처의 기반을 설계하는 데 필수적이다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
분산 데이터베이스(DDB)는 지리적으로 분산된 컴퓨터 노드들에 데이터를 저장하고 관리하되, 사용자에게는 하나의 통합된 시스템처럼 보이게 만드는 데이터베이스 시스템입니다. 단순히 데이터를 여러 곳에 나누어 두는 것(Sharding)을 넘어, 네트워크로 연결된 각 노드가 **분산 처리(Distributed Processing)** 및 **공유(Shared Data)** 기능을 수행합니다. 여기서 핵심은 물리적인 분산성과 논리적인 통합성의 동시 달성입니다.

**2. 등장 배경 및 필요성**
① **기존 한계**: 단일 서버(Centralized DB)의 경우, 처리량(TPS) 한계, 단일 장애점(SPOF) 취약성, 장거리 네트워크 지연(Latency) 문제가 존재했습니다.
② **혁신적 패러다임**: 'Shared Nothing' 아키텍처를 기반으로 각 노드가 독립적인 CPU와 디스크를 가지며 네트워크로만 통신하는 방식이 도입되었습니다.
③ **비즈니스 요구**: 글로벌 서비스 확장, 24/7 무중단 서비스, 대용량 트래픽 처리를 위한 수평적 확장(Scale-out)의 필수성이 대두되었습니다.

**3. 핵심 용어**
- **DDBMS (Distributed Database Management System)**: 분산 데이터베이스를 관리하는 미들웨어로, 트랜잭션 관리, 분산 질의 처리, 동시성 제어를 담당합니다.
- **Transparency (투명성)**: 분산 환경의 복잡성(위치, 복제, 이동 등)을 사용자가 인지하지 못하게 은폐하는 성질입니다.

```text
[중앙 집중식 vs 분산 데이터베이스 비교]

▶ 중앙 집중식 (Centralized)           ▶ 분산 데이터베이스 (Distributed)
 ┌─────────────┐                   ┌───────┐     ┌───────┐
 │   Client    │                   │Client │     │Client │
 └──────┬──────┘                   └───┬───┘     └───┬───┘
        │                              │             │
        ▼                              ▼             ▼
 ┌─────────────────┐             ┌──────────┐ ┌──────────┐
 │   Single DB     │             │ Node A   │ │ Node B   │
 │  (Bottleneck)   │             │(Fragment)│ │(Replica) │
 └─────────────────┘             └────┬─────┘ └────┬─────┘
                                      │           │
                                      └─────┬─────┘
                                            ▼
                                    [ Network / DDBMS ]
```
*해설: 중앙 집중식은 모든 데이터가 하나의 점에 집중되어 병목이 발생하지만, 분산형은 데이터가 여러 노드에 분산되어 부하를 분산하고 장애 허용 능력을 갖습니다.*

> **📢 섹션 요약 비유**: 분산 데이터베이스의 개념은 **'하나의 기업 본사에 모든 직원이 출근하는 것(중앙 집중식)'에서 '각 지사에 직원들이 분산되어 근무하되 본사의 지시 하나로 통합 운영되는 것(분산식)'**으로 변화하는 것과 같습니다. 지사별로 업무를 처리하므로 효율적이며, 한 지사가 재해로 입어도 다른 지사가 업무를 승계할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 역할**
분산 데이터베이스 시스템(DDBS)은 크게 전역 스키마(Global Schema), 사용자 인터페이스, 분산 데이터베이스 관리 시스템(DDBMS), 그리고 물리적 노드(Local DB)로 구성됩니다. 이들은 긴밀하게 협력하여 데이터의 일관성과 투명성을 유지합니다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 |
|:---|:---|:---|
| **Global Schema** | 전체 데이터의 논리적 구조 정의 | 모든 로컬 데이터베이스를 통합한 뷰(View)를 제공하며, 사용자는 이 스키마를 통해 질의를 수행함. |
| **User Processor** | 사용자 요청을 분산 질의로 변환 | 사용자의 SQL을 받아 **Global Query**로 파싱하고, 접근 가능한 노드를 결정함. |
| **DDBMS (Distributed DBMS)** | 핵심 제어 엔진 | 트랜잭션 관리, 동시성 제어(2PL, Timestamp), 분산 커밋(2PC) 등을 수행. |
| **Local DB (Node)** | 물리적 데이터 저장소 | 자신의 **Local Schema**에 따라 데이터 저장 및 인덱싱 수행. 독립적인 DBMS 일 수도 있음. |
| **Network** | 노드 간 통신 채널 | 메시지 전달 프로토콜(TCP/IP 등)을 통해 데이터 패킷과 제어 신호 교환. |

**2. 아키텍처 다이어그램**
분산 데이터베이스의 참조 아키텍처(Reference Architecture)는 크게 상위 레벨의 글로벌 관리자와 하위 레벨의 로컬 관리자로 계층화됩니다.

```text
[분산 데이터베이스 참조 아키텍처]

      User Application
             │
             ▼
┌───────────────────────────────────────┐
│         User Interface Layer           │
│  (SQL Parser / Application Interface) │
└───────────────────┬───────────────────┘
                    │ Global Query
                    ▼
┌───────────────────────────────────────┐
│           Global Schema                │  ← 1. 논리적 통합 (Single Image)
│  (Global Conceptual / External Schema)│
└───────────────────┬───────────────────┘
                    │ Transformation
                    ▼
┌───────────────────────────────────────┐
│         DDBMS (Distribution Mgr)       │  ← 2. 분산 처리 (Coordination)
│  • Query Decomposition                │
│  • Concurrency Control (Lock Mgr)     │
│  • Recovery Manager                   │
└─────┬───────────┬───────────┬─────────┘
      │           │           │
      ▼           ▼           ▼
  [Site 1]     [Site 2]     [Site 3]      ← 3. 물리적 분산 (Autonomy)
  Local DBMS   Local DBMS   Local DBMS
    Disk        Disk        Disk
```
*해설: 이 구조는 **창(Window)** 모델이라 불립니다. 사용자는 상위의 Global Schema만 바라보며, DDBMS가 질의를 분해하여 각 로컬 사이트(Site)에 명령을 내립니다. 각 Local DBMS는 자신의 데이터에 대해 자율성(Autonomy)을 가집니다.*

**3. 6가지 투명성 (6 Types of Transparency)**
DDBMS가 목표로 하는 '투명성'의 구체적 단계는 다음과 같습니다.

1.  **분할 투명성 (Fragmentation Transparency)**: 하나의 테이블이 쪼개져(Remaining, Horizontal, Vertical) 있어도 사용자는 모름.
2.  **위치 투명성 (Location Transparency)**: 데이터가 어느 노드에 있는지 알 필요 없음.
3.  **지역 매핑 투명성 (Local Mapping Transparency)**: 로컬 DBMS의 데이터 모델(관계형, 계층형 등)을 몰라도 접근 가능.
4.  **중복 투명성 (Replication Transparency)**: 데이터가 여러 복제본으로 존재해도 일관성이 유지되는 것처럼 보임.
5.  **장애 투명성 (Failure Transparency)**: 특정 노드가 고장 나도 트랜잭션이 롤백되거나 다른 노드로 대체됨.
6.  **동시성 투명성 (Concurrency Transparency)**: 다수 사용자가 동시에 데이터를 수정해도 결과가 일관됨.

> **📢 섹션 요약 비유**: DDBMS의 아키텍처는 **'통합 번역 시스템'**과 같습니다. 사용자는 '영어(사용자 언어)'로 주문(질의)을 하면, 통합 번역기(DDBMS)가 이를 각 지역별 언어(로컬 시스템)로 번역하여 지사에 지시합니다. 사용자는 지사가 내부적으로 어떤 언어를 쓰고, 재료가 어디에 있는지 전혀 몰라도 원하는 결과를 얻을 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 중앙 집중식 vs 분산 데이터베이스 (정량적 비교)**

| 비교 항목 | 중앙 집중식 DB (Centralized) | 분산 데이터베이스 (Distributed) | 비고 |
|:---|:---|:---|:---|
| **성능 (Performance)** | 단일 CPU/디스크 한계로 높은 부하 시 Latency 급증 | **병렬 처리(Parallelism)** 가능, 쿼리 응답 시간 단축 | Scale-up vs Scale-out |
| **신뢰성 (Reliability)** | **SPOF(Single Point of Failure)** 취약, 전체 다운 | **고가용성(HA)**, 일부 노드 장애 시 서비스 지속 | MTBF 평균 고장 시간 감소 |
| **확장성 (Scalability)** | 비용 선형적 증가, 물리적 한계 명확 | **수평적 확장(Sharding)** 용이, 비용 효율적 | 데이터 양의 선형적 증가 대응 |
| **데이터 공유** | 용이하지만 네트워크 병목 발생 가능 | 복잡하지만 네트워크 부하 분산 가능 | WAN 환경에서 유리 |
| **복잡도 (Complexity)** | 구조 단순, 관리 용이 | 트랜잭션 관리, 동기화 매우 복잡 | CAP 정리 딜레마 존재 |

**2. 타 과목 융합 분석**

- **[OS 및 컴퓨터 구조] Multi-threading & IPC**:
    분산 DB의 각 노드는 독립적인 프로세스(Process)로 실행됩니다. 따라서 노드 간 통신을 위해서는 **IPC (Inter-Process Communication)** 기술이 네트워크 레벨로 확장된 RPC(Remote Procedure Call)가 필수적입니다. 또한, 로컬 노드 내부에서의 트랜잭션 처리는 OS의 **Lock Manager**와 **Shared Memory** 기술을 적극 활용합니다.

- **[네트워크] Latency & Bandwidth**:
    분산 데이터베이스의 성능은 네트워크 대역폭과 지연 시간에 직접적인 영향을 받습니다. **분산 질의 처리(Distributed Query Processing)** 시, 데이터 전송량을 줄이기 위해 관계 대수(Relational Algebra) 최적화가 필수적입니다. 예를 들어, 조인(Join) 연산 시 데이터를 보내는 것이 아니나, 조인을 수행할 수 있는 함수를 보내는 것이 네트워크 트래픽을 획기적으로 줄일 수 있습니다.

```text
[분산 쿼리 처리 최적화 예시: Semi-Join]

❌ 비효율적 방법 (R 전송)
Site A ----------------------------> Site B
   │                                 │
   └──── (Table R 전체 전송) ──────> │
                                    │ (Join 수행 & 결과 반환)

✅ 효율적 방법 (Semi-Join)
Site A <---------------------------- Site B
   │                                 │
   └──── (Join Key 요청) <───────────│
   │                                 │
   └──── (조건에 맞는 Row만 전송) ─> │ (Join 수행 & 결과 반환)
   => 네트워크 트래픽 최소화 (Minimize Data Transfer)
```
*해설: 단순히 조인하려는 테이블 전체를 전송하는 것보나, 조인 키를 먼저 보내 필요한 로우만 필터링해서 가져오는 Semi-Join 기법은 네트워크 비용이 높은 분산 환경에서 필수적인 최적화 기법입니다.*

**3. 데이터 분할 전략 (Data Partitioning)**
- **수평 분할 (Horizontal Fragmentation)**: 행(Row) 단위 분리. (예: 지역별 고객 데이터). 특정 노드에 부하가 집중되는 **Hotspot** 현상을 방지하기 위해 해시(Hash) 기반 분할을 주로 사용함.
- **수직 분할 (Vertical Fragmentation)**: 열(Column) 단위 분리. (예: 자주 조회하는 속성과 그렇지 않은 속성 분리). 네트워크 트래픽 감소 효과.

> **📢 섹션 요약 비유**: 분산 데이터베이스의 데이터 처리와 분할은 **'대형 물류 센터의 허브 시스템'**과 같습니다. 하나의 거대한 창고(Centralized)에 모든 물건을 넣으면 출고 지연이 발생하지만, 지역별 창고(Partition)에 물건을 나누어 넣고, 필요한 경우 창고 간 긴급 배송(Network)을 조율하면 전체 배송 속도(Performance)와 안정성(Reliability)을 동시에 확보할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 도입 시나리오 및 의사결정**

- **시나리오 A: 글로벌 서비스 확장**
    - **상황**: 미국 본사 서버가 하나만 있는데, 유럽/아시아 사용자가 급증하여 접속 지연(Latency)이 심각함.
    - **판단**: 데이터의 지역적 분산이 필수적. **지리적 분할(Geographical Partitioning)**을 통해 유