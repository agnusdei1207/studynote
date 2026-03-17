+++
title = "268. 수평 분할 (Horizontal Fragmentation) - 행 단위의 분산"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 268
+++

# [Database] 수평 분할 (Horizontal Fragmentation) - 행 단위의 분산

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 수평 분할(Horizontal Fragmentation)은 전역 관계(Global Relation)의 튜플(Tuple, 행)들을 **조건부 서술어(Predicate)**에 따라 분리하여 여러 노드에 분산 저장하는 분산 데이터베이스의 핵심 설계 기법이다.
> 2. **가치**: **관계 대수(Relational Algebra)**의 선택(Selection, $\sigma$) 연산을 물리적 저장 단계에서 수행하여, 불필요한 데이터 액세스를 최소화하고 질의 처리 성능(Query Processing Performance)을 획기적으로 향상시킨다.
> 3. **융합**: 분산 데이터베이스(Distributed DB)의 기본이자 현대 클라우드 환경의 **샤딩(Sharding)** 및 **파티셔닝(Partitioning)** 기술의 이론적 근간이 되며, 대용량 처리를 위한 필수 아키텍처이다.

+++

### Ⅰ. 개요 (Context & Background)

#### 개념 및 정의
**수평 분할(Horizontal Fragmentation)**이란 논리적으로 하나의 전역 테이블(Relation)을 구성하는 튜플들의 집합을, 특정 조건(Selection Predicate)에 따라 여러 부분집합(Fragment)으로 나누어 서로 다른 네트워크상의 노드(Node)에 할당하는 기법을 의미합니다. 이때 각 단편(Fragment)은 원본 테이블과 **동일한 스키마(Schema, Attribute 구조)**를 유지하며, 데이터의 '양'을 나누는 행위입니다.

수학적으로는 관계 $R$을 $R_1, R_2, \dots, R_n$으로 분할할 때, 다음 두 가지 조건을 만족해야 합니다.
1. **완전성(Completeness)**: $R = R_1 \cup R_2 \cup \dots \cup R_n$ (모든 데이터는 어느 한 단편에 반드시 속함)
2. **상호 배제性(Disjointness)**: $i \neq j$ 일 때, $R_i \cap R_j = \emptyset$ (특정 데이터는 두 개 이상의 단편에 중복 저장되지 않음. 단, 예외적으로 중복 허용 시 '차등 중복'이라 함)

#### 등장 배경 및 필요성
중앙 집중형 데이터베이스 시스템(Centralized DBMS)에서는 데이터가 단일 서버에 집중됨에 따라 디스크 I/O 병목과 네트워크 지연이 발생합니다. 특히, **지리적으로 분산된 지사(MapReduce)** 혹은 **특정 카테고리의 트래픽이 집중되는 환경**에서는 모든 데이터를 스캔(Scan)해야 하므로 비효율적입니다.
이를 해결하기 위해 데이터를 '행' 단위로 쪼개어 접근 빈도가 높은 데이터를 특정 로컬 서버(Local Node)로 물리적 접근성을 높이는 **네트워킹 효과**를 누리고자 등장했습니다. 이는 분산 투명성(Distributed Transparency)을 제공하면서도 성능을 최적화하는 전략입니다.

> **📢 섹션 요약 비유**:
> 수평 분할은 **'거대한 하나의 전화번호부'를 지역별로 묶어서 각 구청에 따로 보관하는 것**과 같습니다. 전체 주민을 대상으로 찾는 것이 아니라, '서울 거주자'는 구청 A, '부산 거주자'는 구청 B에 두어, 특정 지역 사람을 찾을 때 엄청나게 빠르게 찾을 수 있게 하는 원리입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 내부 동작 메커니즘
수평 분할 시스템은 크게 **전역 스키마(Global Schema)**, **분할 정의(Fragmentation Schema)**, **배치 매핑(Allocation Map)**으로 구성됩니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 | 비고 |
|:---|:---|:---|:---|
| **Selection Predicate** | 분할 기준 | SQL의 `WHERE` 절에 해당하는 조건식($C_i$)을 정의 | 예: `Region = 'SEOUL'` |
| **Global Relation (R)** | 원본 데이터 | 논리적으로 통합된 전체 테이블 | 사용자는 이것만 인식 |
| **Fragment ($R_i$)** | 물리적 단편 | $R_i = \sigma_{Ci}(R)$ 연산 결과로 생성된 부분 집합 | 스키마는 $R$과 동일 |
| **Node (Site)** | 저장 공간 | $R_i$를 실제로 저장하고 처리하는 물리적 서버 | 네트워크 비용 최소화 고려 |
| **Reconstruction Rule** | 데이터 복원 | 모든 단편에 **UNION(합집합, $\cup$)** 연산을 적용하여 $R$ 복원 | 분산 질의 처리 시 필수 |

#### 2. ASCII 구조 다이어그램: 수평 분할의 데이터 흐름
아래는 지역(Region) 조건에 따라 전체 `Sales` 테이블을 수평 분할하여 지사별 서버에 저장하는 아키텍처를 도식화한 것입니다.

```text
      [ GLOBAL SCHEMA: Sales(Employee, Dept, Region, Salary) ]
                        |
                        | (Logic Definition)
                        | F1: σ Region='SEOUL' (Sales)
                        | F2: σ Region='PUSAN' (Sales)
                        | F3: σ Region='OTHER' (Sales)
                        |
           ┌────────────┴────────────┐
           ▼                         ▼
    +---------------+         +---------------+
    |   Site 1 (Seoul)        |   Site 2 (Busan)
    | [ Fragment 1 ]          | [ Fragment 2 ]
    └───────────────┘         └───────────────┘
    | Emp | Dept | Reg | Sal | | Emp | Dept | Reg | Sal |
    | E1  | D1   | SEO | 100 | | E2  | D2   | PUS | 200 |
    | E3  | D1   | SEO | 300 | | E4  | D2   | PUS | 400 |
    └───────────────────────┘ └───────────────────────┘
           ▲                         ▲
           |                         |
      [Local Query]             [Local Query]
   "SEOUL 직원 월급 합계"    "PUSAN 직원 월급 합계"
      (Scan only F1)            (Scan only F2)
```
**(해설)**
1.  **Global Schema** 단계에서는 사용자가 하나의 통합된 테이블을 인식합니다.
2.  **Horizontal Fragmentation** 엔진이 정의된 술어(Predicate)를 통해 튜플들을 분류합니다. 이는 관계 대수의 선택(Selection) 연산 $\sigma$에 해당합니다.
3.  분할된 Fragment 1은 서울 노드(Site 1)에, Fragment 2는 부산 노드(Site 2)에 물리적으로 저장됩니다.
4.  사용자가 "서울 직원 조회" 요청을 하면, 시스템은 전체 네트워크를 스캔하지 않고 **Site 1에만 질의를 전송**하여 불필요한 트래픽을 차단합니다.

#### 3. 핵심 알고리즘 및 복원 원리
수평 분할의 수학적 정합성을 보장하기 위해 **재구성(Reconstruction)** 규칙이 필수적입니다.

$$ R = \bigcup_{i=1}^{n} R_i $$

위 식은 분할된 모든 조각 $R_i$를 합집합($\cup$) 하면 원본 관계 $R$이 되어야 함을 의미합니다.

*   **단순 수평 분할 (Primary Horizontal Fragmentation)**:
    하나의 속성(Attribute)에 대한 단순 조건으로 분할합니다. (예: 지역별)
*   **유도 수평 분할 (Derived Horizontal Fragmentation)**:
    조인(Join) 연산의 효율을 높이기 위해, 연관된 테이블을 상위 테이블의 분할 조건에 맞춰 동일하게 분할합니다. (예: `Customer` 테이블을 지역별로 나누었다면, `Order` 테이블도 고객 지역별로 나누어 Semi-join 비용을 줄임)

> **📢 섹션 요약 비유**:
> 수평 분할의 원리는 **'식당 키친의 주문서 분류'**와 같습니다. 모든 주문서(테이블)를 한 곳에 두면 혼잡하니, **배달 주문(조건A)**은 A 데스크에, **매장 주문(조건B)**은 B 데스크에 행(주문서) 단위로 나누어 둡니다. 데스크별 주방장은 자신의 주문서만 보면 되므로 업무 속도가 빨라지고, 전체를 합치면(Union) 오늘의 총매출을 알 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술적 심층 비교: 수평 vs 수직
데이터 분산 설계 시 수평 분할과 대비되는 **수직 분할(Vertical Fragmentation)**과의 기술적 차이점을 분석합니다.

| 비교 항목 (Metric) | 수평 분할 (Horizontal Fragmentation) | 수직 분할 (Vertical Fragmentation) |
|:---|:---|:---|
| **분할 단위** | **튜플(Tuple, Row)** | **속성(Attribute, Column)** |
| **관계 대수 연산** | $\sigma$ (Selection) | $\pi$ (Projection) |
| **스키마 구조** | 분할 후 스키마 동일 ($Full Schema$) | 분할 후 스키마 상이 ($Subset$) |
| **주요 사용 케이스** | **데이터 양(Payload) 분산**<br>지역/날짜/카테고리 기준 분리 | **보안/접속 빈도 분리**<br>민감 정보 분리, 자주 쓰는 컬럼 분리 |
| **결합(Join) 비용** | 단편 간 Join 불필요 (Union만 필요) | **재조회 시 Join 연산 필수 (오버헤드 큼)** |
| **데이터 복원** | $R = \cup R_i$ (합집합) | $R = \bowtie R_i$ (교차 조인) |

#### 2. 타 과목 융합 분석
*   **운영체제(OS)와의 연계**: 수평 분할은 OS의 **메모리 관리(Memory Management)** 전략 중 **페이징(Paging)**이나 **세그먼테이션(Segmentation)**과 개념적으로 통합니다. 하지만 OS는 주소 공간을 나누는 반면, DB는 논리적 데이터 집합을 나눕니다. 또한, 병렬 처리는 **멀티 스레딩(Multi-threading)** 환경에서 각 스레드가 독립적인 테이블 단편(Fragment)을 액세스하여 **Lock Contention(잠금 경합)**을 최소화하는 효과를 냅니다.
*   **네트워크(Network)와의 연계**: 수평 분할의 궁극적 목표는 **네트워크 트래픽 최소화**입니다. **Query Optimization(질의 최적화)** 과정에서 '관련없는 노드로의 패킷 전송'을 차단하여 **Latency(지연 시간)**를 획기적으로 줄입니다.

> **📢 섹션 요약 비유**:
> 수평 분할과 수직 분할의 차이는 **'책'을 나누는 방식**과 같습니다. **수평 분할**은 '책의 내용(행)'을 나누어 A권(1화~10화), B권(11화~20화)으로 만드는 것이고, **수직 분할**은 '책의 구성(열)'을 나누어 텍스트만 모은 책과 그림만 모은 책으로 만드는 것입니다. 내용을 나눈 수평 분할은 이어 읽기가 쉽지만(Union), 구성을 나눈 수직 분할은 다시 합칠 때 페이지 번호를 매치시켜야 하므로(Join) 복잡합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정
**[Scenario 1: 대규모 이벤트 트래픽]**
쇼핑몰 블랙프라이데이 행사 시간에 `Order` 테이블에 쓰기(Insert) 연산이 몰리는 상황입니다.
*   **Decision**: **수평 분할(Sharding)** 도입.
*   **Logic**: `Order_ID`의 해시(Hash) 값 혹은 `Region`을 기준으로 테이블을 10개로 쪼개어 10대의 DB 서버에 분산 배치합니다.
*   **Effect**: **Lock Contention**이 1/10로 감소하고, 트랜잭션 처리량(TPS)이 선형적으로 증가합니다.

**[Scenario 2: 개인정보 보호 규정(GDPR) 준수]**
유럽 지역 고객의 정보를 EU 내부에만 존재해야 하는 법적 제약이 있습니다.
*   **Decision**: **지역 기반 수평 분할(Geo-based Sharding)**.
*   **Logic**: `Region = 'EU'`인 고객 데이터만 물리적으로 유럽 데이터 센터 노드에 할당하고, 다른 지역 노드에서는 접근을 차단합니다.

#### 2. 도입 체크리스트 (Anti-Pattern 포함)
| 구분 | 체크리스트 항목 | 설명 |
|:---|:---|:---|
| **기술적** | **Data Skew(데이터 치우침) 검증** | 특정 노드에만 데이터가 몰리는 현상을 방지하기 위해 분할 키(Partition Key)의 카디널리티(Cardinality)와 분포도를 분석했는가? |
| **운영적** | **Re-partitioning 비용** | 추후 분할 기준을 변경하거나 노드를 추가할 때의 데이터 재배치(Resharding) 비용과 다운타임을 감당할 수 있는가? |
| **보안적** | **노드별 보안 정책** | 분산된 노드 간의 데이터 동기화 시 암호화 통신(SSL/TLS)이 적용되는가? |

**⚠️ 안티패턴 (Anti-Pattern)**:
*   **잘못된 분할 키 선정**: "성별(Gender)"과 같은 카디널리티가 낮은(2~3개) 컬럼으로 수평 분할을 수행하면, 데이터가 고르게 퍼지지 않고 2~3개의 노드에만 집중되어 병렬 처리 효과가 사라집니다. 이를 **Skewed Fragmentation**이라 합니다.

> **📢 섹션 요약 비유**:
> 수평 분할 설계는 **'고속도로 톨게이트 차선 배치'**와 같습니다. 차량(데이터)을 무조건 나누는 게 아니라, **화물차(무