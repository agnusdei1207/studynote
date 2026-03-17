# 428. 테이블 풀 스캔(Full Table Scan) - 전수 조사의 미학

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **FTS (Full Table Scan)**는 데이터베이스 **옵티마이저 (Optimizer)**가 인덱스를 경유하지 않고 테이블의 **HWM (High Water Mark)**까지 모든 데이터 블록을 순차적으로 읽어들이는 가장 원초적인 접근 경로(Access Path)이다.
> 2. **가치**: 소량 데이터를 조회할 때는 비효율적이나, 전체 데이터의 대다수(보통 10~20% 이상)를访问해야 하거나 대량의 **Batch Processing** 환경에서는 **Multi-Block I/O**의 이점을 살려 **Random Access**보다 월등한 처리량(**Throughput**)을 자랑한다.
> 3. **융합**: **OS (Operating System)**의 **Page Cache** 히트율을 극대화하고, 디스크 헤드의 **Seek Time**을 최소화하는 순차 액세스 특성을 활용하여, 데이터 웨어하우스 및 OLAP 환경에서 핵심적인 성능 최적화 기법으로 작용한다.

---

### Ⅰ. 개요 (Context & Background)

**FTS (Full Table Scan)**는 데이터베이스 관리자(**DBA**)가 흔히 "성능 저하의 원인"으로 지목하지만, 실제로는 옵티마이저가 비용 기반 최적화(**CBO, Cost-Based Optimization**)를 통해 선택하는 매우 합리적인 실행 계획 중 하나이다.

**개념적 정의 및 철학**
인덱스를 사용하는 **Index Scan**이 "책의 목차(Index)를 보고 원하는 페이지로 바로 이동하는 과정"이라면, **FTS**는 "책의 첫 페이지부터 마지막 페이지까지 빈틈없이 읽어 나가는 과정"이다. 이때 데이터베이스는 단일 블록을 하나씩 읽는 **Single Block Read** 방식이 아니라, 디스크 I/O 횟수를 줄이기 위해 한 번의 시스템 호출로 여러 블록(예: 16개, 32개 등)을 메모리로 로드하는 **Multi-Block Read** 기술을 활용한다.

**등장 배경 및 기술적 필요성**
1.  **기존 한계**: 인덱스는 랜덤 액세스 방식이므로, 데이터가 넓게 분산되어 있을 경우 디스크 헤드가 잦은 이동(**Seek**)을 해야 하여 대량 데이터 처리에 불리하다.
2.  **혁신적 패러다임**: 읽기 연산의 **Locality(지역성)**을 최대한 활용하여, 순차적인 I/O로 처리함으로써 대역폭(**Bandwidth**)을 효율적으로 사용하고 **Buffer Cache**의 효율을 높이는 접근법이 요구됨.
3.  **비즈니스 요구**: 실시간 단건 조회보다는 전체 리포트 생성, 일괄 삭제, 대량 통계 집계 등 대량 데이터를 다루는 **Batch Job** 및 **OLAP (Online Analytical Processing)** 환경에서의 필수적인 처리 전략으로 자리 잡음.

**📢 섹션 요약 비유**:
테이블 풀 스캔은 마치 **"도서관에서 책 전체를 흩날리는 페이지를 찾기보다는, 처음부터 끝까지 차근차근 읽으며 필요한 내용을 모두 수집하는"** 정독법과 같습니다. 책을 펼쳐 딱 한 줄을 찾을 때는 목차를 보는 게(인덱스) 빠르지만, 책의 내용을 요약해야 한다면(대량 조회) 차라리 쭉 읽는 것이(풀 스캔) 더 빠르고 효율적입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 및 동원 기술**

| 요소명 | 역할 | 내부 동작 메커니즘 | 주요 파라미터/특징 |
|:---|:---|:---|:---|
| **HWM (High Water Mark)** | 스캔의 종료 지점표 | 데이터가 실제로 저장된 가장 높은 블록의 위치를 표시함. FTS는 HWM 이하의 블록만 읽음. | DELETE로 데이터가 삭제되어도 HWM은 내려가지 않아 빈 블록을 읽는 **Water Mark Issue** 발생 가능. |
| **Multi-Block I/O** | 대량 데이터 로딩 엔진 | 한 번의 `db file scattered read` Call로 여러 개의 블록을 **DB Buffer Cache**에 할당. | `DB_FILE_MULTIBLOCK_READ_COUNT` 파라미터로 제어(보통 16~128). |
| **Optimizer (CBO)** | 실행 계획 판단부 | 통계 정보를 기반으로 인덱스 경로 비용 vs FTS 경로 비용을 산출하여 최소 비용 선택. | 데이터 분포도, 클러스터링 팩터 고려. |
| **Buffer Cache** | 데이터 중계 저장소 | 읽혀진 블록을 메모리에 캐싱. FTS는 일반적으로 **LRU (Least Recently Used)** 리스트의 콜드 부분에 로드되어 장기적 점유 방지. | SGA(System Global Area) 영역 내 관리. |

**구조 및 데이터 흐름 (ASCII 다이어그램)**

아래는 옵티마이저가 FTS를 선택했을 때의 내부 아키텍처와 데이터 흐름을 도식화한 것이다.

```text
[ SQL Execution Flow: Full Table Scan Architecture ]

[ Client Process ]          [ Server Process ]          [ SGA (Memory) ]          [ Storage ]
   |                             |                            |                         |
   |-- 1. SELECT * FROM Emp      |                            |                         |
   |                             |                            |                         |
   |                             |  2. Parse & Optimize       |                         |
   |                             |  (CBO decides FTS is cheaper)                   |
   |                             |  (Cost: I/O + CPU)         |                         |
   |                             |                            |                         |
   |                             |  3. Get HWM Location        |                         |
   |                             |  (Segment Header)           |                         |
   |                             |                            |                         |
   |                             |  4. Initiate Multi-Block Read                        |
   |                             |  <=========================> 5. Load Blocks (1,2,3...)
   |                             |     Scattered Read (Sequential)   |                   |
   |                             |                                   |                   |
   |                             |  6. Predicate Filter              |                   |
   |                             |  (Apply WHERE clause)             |                   |
   |                             |  (e.g., SAL > 5000)               |                   |
   |                             |                                   |                   |
   |<---- 7. Return Rows ---------|                                   |                   |
   |                             |                                   |                   |

   [ Legend ]
   Step 4-5: 한 번의 I/O Call로 디스크의 연속된 블록을 통째로 읽어옴 (Sequential Access)
   Step 6:  Filter는 데이터가 메모리에 올라온 후 수행됨 (Late Materialization)
```

**다이어그램 해설**
1.  **Multi-Block I/O (Step 4~5)**: FTS의 핵심은 단일 블록을 읽는 Random I/O가 아니라, 연속된 디스크 공간에서 물리적으로 인접한 블록들을 한꺼번에 읽어오는 `db file scattered read` 이벤트 발생 지점입니다. 이는 디스크 헤드의 이동(Seek)을 최소화하여 순차 읽기의 처리 속도를 극대화합니다.
2.  **Filtering (Step 6)**: 데이터는 일단 테이블 전체를 다 읽은 후(또는 읽히는 과정에서) WHERE 절 조건에 의해 필터링됩니다. 따라서 인덱스 스캔처럼 미리 데이터를 좁히고 접근하는 방식이 아니라, 일단 가져오고 걸러내는 방식을 사용합니다.
3.  **Buffer Cache 활용**: 읽힌 블록은 SGA 내의 Buffer Cache에 적재되지만, FTS에 의해 읽힌 블록은 버퍼 캐시의 LRU(Least Recently Used) 알고리즘 상에서 **Cold End**에 위치하게 되어 다른 쿼리에 의해 빠르게 밀려날 가능성이 높습니다. 이는 전체 캐시를 대량 FTS가 점유하는 것을 방지하기 위한 방어 기제입니다.

**심층 동작 원리 및 알고리즘**
FTS의 성능을 결정짓는 가장 중요한 수식은 **I/O Cost** 계산입니다.

```text
[ Cost Estimation Logic (Simplified) ]

Total FTS Cost = (Number of Blocks / MultiBlock_Read_Count) + CPU_Cost

* Number of Blocks: 테이블의 총 블록 수 (HWM 아래 모든 블록)
* MultiBlock_Read_Count: 한 번의 I/O Call로 읽는 블록 수 (OS 및 DB 설정 종속)
* CPU_Cost: 읽어온 데이터에서 WHERE 조건을 검사(Row-by-Row)하는 비용
```

**📢 섹션 요약 비유**:
FTS는 마치 **"고속도로 요금소의 하이패스 차선(Multi-Lane)"**과 같습니다. 일반 차선(Single Block)이 차례대로 하나씩 통과하는 반면, 하이패스 차선은 여러 대의 차량을 묶어서 동시에 처리하듯, 한 번의 I/O로 수십 개의 데이터 블록을 확 훑고 지나가기 때문에 전체 교통량(처리량)이 압도적으로 높아질 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**Index Range Scan vs Full Table Scan (정량적/구조적 비교)**

| 비교 항목 | Index Range Scan (인덱스 범위 스캔) | Full Table Scan (풀 테이블 스캔) |
|:---|:---|:---|
| **Access Method** | **Random Access** (논리적/물리적 분산) | **Sequential Access** (물리적 인접) |
| **I/O 단위** | Single Block Read (블록 1개씩) | Multi-Block Read (블록 N개씩) |
| **Target Selectivity** | **높음 (High Selectivity)**<br>데이터의 소수 (~5~10%) | **낮음 (Low Selectivity)**<br>데이터의 다수 (~20% 이상) |
| **CPU 비용** | 낮음 (인덱스 키 비교 후 일부만 접근) | 높음 (모든 Row에 대해 Filter 수행) |
| **Buffer Cache** | 핫 항목(Hot)으로 유지되어 재사용 유리 | 콜드(Cold) 영역에 저장되어 빠르게 소거됨 |
| **주요 사용처** | OLTP (주문 조회, 마이페이지 등) | Batch, Reporting, 대량 데이터 Export |
| **결정 임계점(Tipping Point)** | - | **약 10~20%** (Oracle 기준, 분포도에 따라 가변) |

**과목 융합 관점: OS 및 하드웨어와의 시너지**

1.  **OS (Operating System) - File System & Page Cache**:
    *   FTS는 데이터베이스 레벨의 `Multi-Block Read`뿐만 아니라, **OS 레벨의 Read-Ahead(예측 읽기)** 기능과 결합하여 시너지를 냅니다. 순차적으로 읽는 패턴을 파악한 OS 커널은 앞으로 필요할 데이터를 미리 디스크에서 메모리로 캐싱하여(**Prefetching**), 데이터베이스가 실제 디스크를 접근하기 전에 데이터가 준비되도록 돕습니다.

2.  **Computer Architecture (H/W) - Disk Physics**:
    *   **HDD (Hard Disk Drive)** 환경에서는 헤드가 이동하는 **Seek Time**이 병목입니다. 인덱스 스캔은 잦은 Seek를 유발하지만, FTS는 트랙을 따라 연속 읽기(**Rotation**)만 하므로 물리적인 한계 속도에 근접하여 데이터를 읽을 수 있습니다. (SSD 환경에서는 Seek Time이 무의미해졌으나, I/O 패킷 오버헤드 감소를 위해 여전히 FTS가 유리함).

**📢 섹션 요약 비유**:
인덱스 스캔은 **"도심지를 운전하며 여러 곳을 방문(택배 배달)"**하는 것과 같아서 방문할 때마다 출발하고 멈추는(stop-and-go) 비용이 높은 반면, 풀 스캔은 **"고속도로를 통해 목적지까지 직진"**하는 것과 같아서 일단 출발하면 중간에 멈추지 않고 최대 속도로 질주하는 항공 모드 같은 접근 방식입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정 매트릭스**

1.  **시나리오 A: 대량 데이터 재계산 (Nightly Batch)**
    *   **상황**: 매일 밤 12시에 전체 고객의 누적 포인트를 재계산하는 배치 잡(Job).
    *   **판단**: 전체 고객의 100%를 접근해야 함. 인덱스를 통해 일일이 접근하면 `db file sequential read`가 수백만 번 발생함.
    *   **결론**: **FTS 강제 추천**. `/*+ FULL(CUSTOMER) */` 힌트를 사용하여 처리 시간을 수시간에서 수분으로 단축.

2.  **시나리오 B: 소규모 Lookup Table (코드성 테이블)**
    *   **상황**: 국가 코드, 지역 코드와 같이 행이 50개 미만인 테이블 조인.
    *   **판단**: 테이블 크기가 너무 작아 디스크 I/O 자체가 1회면 끝남. 인덱스를 경유하는 논리적 연산만 늘어남.
    *   **결론**: **FTS 무시(자동 선택)**. 옵티마이저가 자동으로 FTS를 선택하며, 인덱스 생성을 하지 않는 것이 관리 차원에서 유리함.

3.  **시나리오 C: 인덱스 컬럼 변형 사용**
    *   **상황**: `WHERE SUBSTR(NAME, 1, 3) = 'KIM'` 과 같이 컬럼을 가공하여 조회.
    *   **판단**: 인덱스가 있더라도 컬럼이 변형되면 일반 B-Tree 인덱스는 무력화됨(Function-Based Index 제외).
    *   **결론**: **FTS 불가피**. 이를 피하려면 함수기반 인덱스 생성을 검토해야 하나, 불가능하다면 FTS를 최적화하는 방향(가공 로직 수정 등)으로 튜닝.

**도입 체크리스트**

| 구분 | 체크 항목 | 비고 |
|:---|:---|:---|
| **기술적** | **Selectivity(선택도)** 확인 | `전체 ROW 수 / 추출 ROW 수`가 0.1(10%) 이상인가? |
| | **HWM 관리** | `ALTER TABLE ... MOVE` 혹은 `SHRINK`를 통해 공간 낭비를 제거했는가? |
| | **I/O 분포** | 디스크 병목이 발생하지 않도록 배치 시간을 분산했는가? |
| **운영적** | **Lock