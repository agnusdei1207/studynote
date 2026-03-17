+++
title = "267. 데이터 분할 기법 (Fragmentation) - 물리적 최적화의 기술"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 267
+++

# 267. 데이터 분할 기법 (Fragmentation) - 물리적 최적화의 기술

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **데이터 분할(Fragmentation)**은 논리적인 전역 스키마(Global Schema)를 사용자의 접근 패턴과 네트워크 토폴로지에 맞춰 물리적인 단편(Fragment)으로 분리 저장하는 **분산 데이터베이스 설계(Distributed Database Design)의 핵심 기법**이다.
> 2. **가치**: **데이터 로컬리티(Data Locality)**를 극대화하여 네트워크 트래픽을 최소화하고, 병렬 처리(Parallel Processing)를 통해 질의 응답 시간(Query Response Time)을 획기적으로 단축시킨다.
> 3. **융합**: OS의 메모리 관리(Paging/Segmentation) 개념과 DB의 샤딩(Sharding) 아키텍처가 융합되며, 대용량 처리를 위한 수평적 확장성(Scale-out)의 기반을 제공한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**데이터 분할(Fragmentation)**이란 분산 데이터베이스 환경(Distributed Database Environment)에서 하나의 논리적 관계(Relation)를 여러 개의 물리적 조각(Fragment)으로 나누어 각기 다른 사이트(Site) 또는 노드(Node)에 할당하는 기술을 의미합니다. 단순한 데이터 복제(Replication)와 달리, 분할은 데이터를 부분 집합으로 쪼개어 **"필요한 데이터를 필요한 장소에"** 배치함으로써 전체 시스템의 효율성을 극대화하는 것을 목표로 합니다.

이 기술의 근간에는 **"데이터를 계산(Processing)이 일어나는 곳으로 가져가는 것"**이 **"계산을 데이터가 있는 곳으로 보내는 것"**보다 네트워크 비용 측면에서 훨씬 유리하다는 분산 컴퓨팅의 철학이 깔려 있습니다.

#### 2. 등장 배경 및 필요성
① **기존 중앙 집중식의 한계**: 단일 서버가 모든 데이터를 처리하며 발생하는 병목 현상(Bottleneck)과 네트워크 대역폭의 과부하.
② **네트워크 지연 최소화**: 지리적으로 분산된 지사에서 본사의 거대 테이블을 전체 조회할 때 발생하는 대기 시간(Latency) 제거 필요성.
③ **보안 및 프라이버시**: 급여 정보나 민감한 고객 정보 등 특정 속성(Column)에 대한 접근 제어를 물리적 단위로 격리할 필요성 대두.

#### 3. 분할의 3대 설계 원칙 (Correctness Rules)
데이터를 분할할 때 반드시 준수해야 할 수학적 무결성 규칙은 다음과 같습니다.

| 원칙 (Principle) | 설명 (Description) | 수학적 표현 (R: 릴레이션, Fi: 단편) |
|:---:|:---|:---:|
| **완전성**<br>(Completeness) | 릴레이션 내의 모든 데이터는 반드시 어느 한 단편에 속해야 한다. 데이터 누락을 허용하지 않는다. | $\cup F_i = R$ |
| **재구성성**<br>(Reconstructibility) | 분할된 모든 단편을 합치면(Join 또는 Union) 원본 릴레이션으로 무결성 있게 복원되어야 한다. | $R = \bowtie F_i$ (Vertical) <br> $R = \cup F_i$ (Horizontal) |
| **상호 배제성**<br>(Disjointness) | 하나의 튜플(행)은 원칙적으로 하나의 단편에만 속해야 한다. (중복 저장 방지, 단, Key 중복은 예외) | $F_i \cap F_j = \emptyset$ ($i \neq j$) |

```text
[데이터 분할의 논리적 개념도]

    [ Logical Global Relation R ]
    ─────────────────────────────
    │  (A, B, C, D, E, F, G, H) │
    ─────────────────────────────
              │
      ────────┼───────  (Split Operation)
              ▼
    ┌─────────┴─────────┐
    ▼                   ▼
[ Fragment F1 ]      [ Fragment F2 ]
─────────────        ─────────────
( A, B, C )          ( D, E, F, G, H )  ← Disjoint (Non-overlapping)
─────────────        ─────────────
    │                   │
    └───────┬───────────┘
            ▼
    [ Physical Distribution ]
  Site A (Local User)     Site B (HQ Analyst)
```
*도해 해설*: 논리적으로는 하나의 테이블이지만, 물리적으로는 사이트 A와 B로 나뉘어 저장됨을 보여줍니다. 사용자는 분할된 사실을 인식하지 못하고 투명하게(Transparency) 데이터에 접근합니다.

> **📢 섹션 요약 비유**: 데이터 분할은 **'거대한 도서관의 책을 지점별로 분류하여 이관하는 것'**과 같습니다. 본사(중앙 DB)에 모든 책이 있으면 시민이 너무 멀리 와야 하지만(지연), 과학 책은 과학관에, 예술 책은 예술관에(수직/수평 분할) 배치하면 대기 시간이 줄어들고 이용 효율이 극대화됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 분할의 주요 유형 및 구성 요소
데이터 분할은 크게 **수평 분할(Horizontal Fragmentation)**, **수직 분할(Vertical Fragmentation)**, 그리고 이들의 혼합형으로 나뉩니다.

| 구분 | 수평 분할 (Horizontal) | 수직 분할 (Vertical) |
|:---|:---|:---|
| **기반 연산** | **SELECT** (Selection) | **PROJECT** (Projection) |
| **단위** | **튜플(Tuple/Row)** 단위 분리 | **속성(Attribute/Column)** 단위 분리 |
| **결과물** | 부분 집합의 튜플 묶음 | 속성의 서브셋 묶음 |
| **주요 키** | 기존 PK 유지 | **반드시 PK 포함** (Join 복원을 위해) |
| **대표 예시** | 지역별 고객 정보 (서울/부산) | 기본 정보 + 상세 정보 (Profile/Auth) |

#### 2. 수평 분할 (Horizontal Fragmentation)
튜플을 기준으로 테이블을 나누는 방식입니다. 주로 **지리적 위치(Geolocation)**, **연도(Year)**, **부서(Department)** 등의 값에 따라 분할합니다.

```text
[수평 분할 아키텍처: 지역별 고객 관리]

   [Global Table: CUSTOMER]
┌──────────────────────────────────┐
│ ID │ Name   │ Region │ Order_Amt│
├──────────────────────────────────┤
│ 01 │ Kim    │ Seoul  │ 100      │
│ 02 │ Lee    │ Busan  │ 200      │
│ 03 │ Park   │ Seoul  │ 150      │
│ 04 │ Choi   │ Busan  │ 300      │
└──────────────────────────────────┘
        │
        │  Query: SELECT * FROM Customer WHERE Region = 'Seoul'
        │
        ▼  (Horizontal Fragmentation)
┌──────────────────┐      ┌──────────────────┐
│  Fragment H1     │      │  Fragment H2     │
│  (Seoul Site)    │      │  (Busan Site)    │
├──────────────────┤      ├──────────────────┤
│ ID │ Name   │ Amt │      │ ID │ Name   │ Amt │
├──────────────────┤      ├──────────────────┤
│ 01 │ Kim    │ 100 │      │ 02 │ Lee    │ 200 │
│ 03 │ Park   │ 150 │      │ 04 │ Choi   │ 300 │
└──────────────────┘      └──────────────────┘
```
*도해 해설*: 서울 지사 서버(H1)는 서울 고객 데이터만, 부산 지사 서버(H2)는 부산 고객 데이터만 독립적으로 저장합니다. 지사별로 발생하는 조회 질의(Local Transaction)가 네트워크를 타지 않고 로컬 디스크에서 해결되어 성능이 급상승합니다.

#### 3. 수직 분할 (Vertical Fragmentation)
속성(Column)을 기준으로 테이블을 나누는 방식입니다. 자주 접근하는 속성(Hot Data)과 드물게 접근하는 속성(Cold Data)을 분리하여 저장소 효율을 높입니다.

```text
[수직 분할 아키텍처: 프로젝트/레코드 분리]

   [Global Table: EMPLOYEE]
┌──────────────────────────────────────────────┐
│ Emp_ID │ Name │ Dept │ **Salary** │ **Memo** │
├──────────────────────────────────────────────┤
│  E001   │ Kim  │ IT   │ 5000      │ ...      │
│  E002   │ Lee  │ HR   │ 4000      │ ...      │
└──────────────────────────────────────────────┘
                   │
                   │  (Vertical Fragmentation)
        ┌──────────┴──────────┐
        ▼                     ▼
┌─────────────────────┐ ┌──────────────────────┐
│  Fragment V1        │ │  Fragment V2         │
│  (General Access)   │ │  (Secure Access)     │
├─────────────────────┤ ├──────────────────────┤
│ Emp_ID (PK)         │ │ Emp_ID (PK)          │
│ Name                │ │ Salary (Encrypted)   │
│ Dept                │ │ Memo                 │
└─────────────────────┘ └──────────────────────┘
        │                     │
    [Public Web]          [HR Private Node]
```
*도해 해설*: V1은 자주 조회하는 기본 정보(ID, 이름)를 담아 웹 서버가 빠르게 조회하게 하고, V2는 민감한 급여 정보를 담아 보안이 강화된 별도 노드에 배치합니다. 데이터 복원 시에는 `Emp_ID`를 기준으로 `Join` 연산을 수행합니다.

#### 4. 파생 수평 분할 (Derived Horizontal Fragmentation)
조인(Join) 관계에 있는 테이블 A와 B가 있을 때, 테이블 A를 분할한 기준(Predicate)에 따라 테이블 B를 같이 분할하는 기법입니다. 이는 분산 조인(Distributed Join) 비용을 최소화하기 위해 사용됩니다.

> **📢 섹션 요약 비유**: **'회사 조직도와 인사 명부'**로 비유할 수 있습니다. 수평 분할은 **'영업팀 직원 명부'와 '개발팀 직원 명부'**로 나누는 것(팀별 배치)이고, 수직 분할은 **'출퇴근부(이름, 부서)'**와 **'급여 명세서(연봉, 상여)'**를 따로 보관하는 것(접근 권한 및 용도별 분리)과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술적 비교 분석표 (Fragmentation vs. Replication vs. Sharding)

| 비교 항목 | 데이터 분할 (Fragmentation) | 데이터 복제 (Replication) | 샤딩 (Sharding) |
|:---|:---|:---|:---|
| **핵심 목적** | 데이터 분산 배치, 네트워크 최적화 | 가용성(Availability), 읽기 성능 증폭 | **규모 확장성(Scalability)** 확보 |
| **데이터 중복** | 없음 (Non-redundant) <br>*(일부 Key 중복 제외)* | 있음 (Full or Partial Copy) | 없음 (Disjoint) |
| **쓰기 성능** | 단일 노드에 기록하므로 빠름 | 여러 노드에 동기화 필요하여 상대적으로 느림 | 병렬 기록 가능하여 매우 빠름 |
| **복잡도** | 재구성 로직(Join/Union) 필요 | 동기화 충돌(Conflict) 해결 필요 | 라우팅(Routing) 로직 복잡 |
| **주요 사용처** | 분산 DB 테이블 설계 기본 | CDN, Read-Intensive 시스템 | 초대형 트래픽 웹 서비스 |

#### 2. 타 과목 융합 및 상관관계

① **운영체제(OS)와의 융합**: 데이터 분할의 **수평/수직** 개념은 OS의 메모리 관리 기법인 **페이징(Paging)**과 **세그먼테이션(Segmentation)**과 유사합니다.
- **Paging**: 논리 주소 공간을 고정 크기 페이지로 나누는 것 (≈ Horizontal Fragmentation의 Chunk 단위 분할).
- **Segmentation**: 논리적 단위(코드, 데이터, 스택)별로 나누는 것 (≈ Vertical Fragmentation의 속성별 분할).
- **시너지**: OS의 메모리 국소성(Locality of Reference) 원리가 DB의 Disk I/O 최적화로 그대로 투영됩니다.

② **네트워크와의 융합**: 분할된 데이터를 조합할 때 발생하는 **네트워크 비용(Communication Cost)**을 고려해야 합니다. **반정규화(Denormalization)** 전략과 결합하여, 빈번한 조인을 유발하는 분할을 피하거나, 자주 조합되는 단편을 같은 네트워크 세그먼트(LAN)에 배치하는 의사결정이 필요합니다.

#### 3. 비용 및 성능 메트릭 (Decision Matrix)
데이터 분할을 결정할 때 고려해야 할 정량적 지표입니다.

- **N.A. (Network Availability)**: 네트워크 대역폭이 한정적일수록 분할의 효과가 커집니다.
- **A.R. (Access Ratio)**: 전체 데이터 대비 지역적으로 접근하는 비율이 높을수록(>80%) 수평 분할이 유리합니다.
- **J.C. (Join Cost)**: 단편 간 조인 빈도가 높으면 수직 분할을 피하거나 공통 속성을 중복 저장(비용 희생)하는 전략이 필요할 수 있습니다.

> **📢 섹션 요약 비유**: **'여행 가방 패킹'**과 같습니다. 혼자 여행할 때는 모든 짐을 한 가방에 넣는 것(Replication에 가까움)이 나을 수 있지만, 대가족이 여행할 때는 가방을 용도별(옷 가방, 장난감 가방)으로 쪼개서(분할) 각자 나르는 것이(Negative Work 분산) 훨씬 효율적입니다. 하지만 나중에 옷가방과 신발가방을 따로 찾아야 하는 번거로움(Join Cost)은 감수해야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 프로세스
**상황**: 전국적인 지사를 �