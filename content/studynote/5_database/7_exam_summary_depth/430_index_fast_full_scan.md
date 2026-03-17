+++
+++
title = "430. 인덱스 패스트 풀 스캔(Index Fast Full Scan) - 속도에 올인한 탐색"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 430
+++

# 430. 인덱스 패스트 풀 스캔(Index Fast Full Scan) - 속도에 올인한 탐색

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인덱스 패스트 풀 스캔(IFFS, Index Fast Full Scan)은 인덱스의 논리적 순서(논리적 ORDER BY)를 포기하고, 디스크 상의 **물리적 저장 순서대로 인덱스 세그먼트 전체를 Multi-Block I/O(다중 블록 입출력)** 방식으로 고속 읽는 실행 계획이다.
> 2. **가치**: 테이블 전체 스캔(Table Full Scan) 대비 **디스크 I/O 량을 획기적으로 감소**시키며, 병렬 처리(Parallel Query)와 결합하여 대용량 데이터의 집계 연산(Aggregation)에서 극대화된 처리량(Throughput)을 제공한다.
> 3. **융합**: 운영체제(OS)의 파일 시스템 캐시 및 Direct Path I/O 메커니즘과 연동하여 DBMS(Database Management System) 버퍼 캐시 우회를 통한 메모리 효율성을 극대화하는 하이브리드 최적화 기술이다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 정의
인덱스 패스트 풀 스캔(IFFS)은 오라클(Oracle) 등 상용 DBMS에서 제공하는 인덱스 액세스 방식의 일종입니다. 일반적인 인덱스 스캔(Index Range Scan, Index Full Scan)이 **B-Tree의 논리적 연결 리스트(Linked List)**를 따라 단일 블록(Single Block)을 순차적으로 읽는 것과 달리, IFFS는 인덱스를 구성하는 모든 리프 블록(Leaf Block)과 루트/분기 블록을 **'마치 일반 테이블처럼'** 취급하여 물리적으로 디스크에 저장된 순서대로 읽어 들입니다. 이때 핵심은 **'논리적 정렬(Sorted Order)'을 포기하고 대신 '물리적 읽기 성능(Physical Read Speed)'을 극대화**한다는 트레이드오프(Trade-off)에 있습니다.

#### 💡 비유
책에서 특정 주제를 찾을 때, 목차를 보고 페이지 순서대로 찾아가며 정독하는 것이 일반적인 인덱스 스캔이라면, IFFS는 책의 페이지 순서는 무시하고 책을 통째로 펼쳐서 필요한 단어들이 포함된 페이지만 빠르게 스캔너로 긁어 넘기는 방식입니다.

#### 등장 배경 및 패러다임
1.  **기존 한계**: 대용량 테이블에서 `COUNT(*)`와 같은 집계 연산 수행 시, 인덱스를 이용하면 논리적 순서를 따라야 하므로 Random Access가 발생하여 성능이 저하됨.
2.  **혁신적 패러다임**: 인덱스가 포함하는 컬럼만으로 쿼리를 해결할 수 있다면(커버링 인덱스), 굳이 테이블을 액세스하지 않고 인덱스 구조 자체를 '작은 테이블'처럼 빠르게 읽자는 아이디어 등장.
3.  **비즈니스 요구**: 실시간 분석(OLAP) 및 대용량 리포팅 환경에서 '정확한 순서'보다 '전체 데이터의 신속한 집계'가 중요해지며 IFFS 중요성 부각.

#### 📢 섹션 요약 비유
> 인덱스 패스트 풀 스캔은 **'도서관의 사서 대신 스캐너 기계'**를 이용하는 것과 같습니다. 책장에 꽂힌 순서(논리적 순서)는 무시한 채, 책 덩어리(인덱스 블록)를 통째로 긁어서 내용을 파악하므로 정렬은 되지 않지만, 전체 내용을 파악하는 속도는 인간이 따라갈 수 없을 만큼 빠릅니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 구성 요소 및 동원 기술
IFFS가 작동하기 위해서는 단순한 인덱스 구조 이상의 DBMS 내부 메커니즘이 필요합니다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Index Segment** | 데이터 저장소 | 테이블 데이터와 별도로 저장된 인덱스의 물리적 공간. 블록들이 연속적이지 않을 수 있음. | 찾고자 하는 단어가 적힌 책들의 묶음 |
| **Multi-Block I/O** | 고속 읽기 엔진 | Single Block I/O(`db file scattered read` 이벤트)를 통해 한 번의 I/O Call로 여러 블록을 메모리로 로딩. OS의 Read-ahead 기능 활용. | 한 손에 책 여러 권을 한꺼번에 집어 듦 |
| **Buffer Cache** | 데이터 버퍼링 | 읽힌 블록이 DB 버퍼 캐시에 적재됨 (Full Scan 시 Temporary 영역 활용 가능). | 책을 읽기 위해 책상에 펼쳐두는 공간 |
| **Optimizer (CBO)** | 의사결정 | 통계 정보를 바탕으로 IFFS가 Table Full Scan보다 비용(Cost)이 낮다고 판단되면 실행 계획 선택. | 가장 빠른 경로를 안내하는 내비게이션 |
| **Covering Index** | 조건 만족 | 쿼리에 필요한 모든 컬럼이 인덱스에 포함되어 있어 테이블 액세스가 불필요한 상태. | 사전만 보고도 뜻을 다 이해할 수 있는 상태 |

#### ASCII 구조 다이어그램: 논리적 읽기 vs 물리적 읽기
아래는 동일한 인덱스 구조를 읽는 두 방식의 극명한 차이를 도식화한 것입니다.

**A. Index Full Scan (논리적 접근 - 정순)**
```text
[B+Tree 구조]
     Root
      / \
  Br1     Br2
  /        \
L1(1,10) L2(11,20) L3(21,30)
  ▲        │         ▼
  └────────┴─────────┘
  [논리적 연결 리스트 따라 읽기]
  
  🔄 Read Order: L1 → L2 → L3
  ⚙️  I/O Mode: Single Block Read (한 줄씩)
  ✅ Result: 1, 2, ... 20, 30 (Sorted 보장)
```

**B. Index Fast Full Scan (물리적 접근 - 비정순)**
```text
[디스크 물리 블록 배치 상황 가정]
  Disk Layout: [ L3 ] [ L1 ] [ L2 ] 
               (섞여 있음)

  🔥 Read Process:
  1. Optimizer는 연결 포인터 무시
  2. HWM(High Water Mark) 아래 모든 블록 스캔 명령
  3. Multi-Block Read로 한꺼번에 로딩

  🔄 Read Order: L3 → L1 → L2 (물리적 순서)
  ⚙️  I/O Mode: **Multi-Block Read** (Scattered Read)
  ❌ Result: 25, 1, 15... (Unsorted)
  🚀 Speed: 매우 빠름 (I/O Call 횟수 감소)
```

#### 심층 동작 원리 및 알고리즘
1.  **실행 계획 수립**: CBO(Cost Based Optimizer)는 쿼리의 `SELECT` 리스트에 있는 컬럼이 인덱스에 모두 포함되어 있는지 확인합니다. 이때 인덱스의 B-Tree 높이(Height)보다 전체 블록 수가 스캔하기에 충분히 작다고 판단되면 IFFS를 선택합니다.
2.  **HWM 기반 스캔**: 세그먼트의 **HWM (High Water Mark)** 이하에 있는 모든 블록을 대상으로 합니다. 사용되지 않은 블록은 건너뜁니다.
3.  **Direct Path Read 가능성**: 대용량 테이블(Parallel Query 포함)의 경우, SGA(Buffer Cache)를 거치지 않고 PGA(Process Global Area)로 직접 데이터를 로드하는 **Direct Path Read**가 수행되어 버퍼 캐시 경합을 최소화합니다.
4.  **데이터 추출**: 블록을 읽으면서 해당 Row의 존재 여부만 확인하고 바로 클라이언트 또는 정렬 공간으로 전달합니다. 정렬이 필요한 경우(`ORDER BY` 절이 있음), 이후 별도의 Sort Operation이 수행됩니다.

#### 핵심 코드 및 힌트
SQL에서 강제로 IFFS를 유도하려면 `INDEX_FFS` 힌트를 사용합니다.

```sql
-- 예시: 사원 테이블에서 부서번호만 집계 (이름 컬럼은 인덱스에 없다고 가정 시 실패 가능)
-- 인덱스: EMP_IDX (DEPT_NO, SALARY)
SELECT /*+ INDEX_FFS(EMP EMP_IDX) */ COUNT(*)
FROM EMP;

-- 작동 원리 (의사코드)
Function IFFS_Execution():
  IndexSeg = LocateSegment("EMP_IDX");
  Blocks = GetAllBlocksBelowHWM(IndexSeg); // 물리적 블록 리스트
  
  Parallel_Loop(Blocks):
    Chunk = ReadMultiBlocks(Blocks, Size=1MB); // 대량 I/O
    For Each Row In Chunk:
      If Row.Visible():
        ResultCount++;
  Return ResultCount;
```

#### 📢 섹션 요약 비유
> 인덱스 패스트 풀 스캔은 **'벽돌 공장에서 벽돌을 나를 때, 질서 정연하게 쌓는 것보다 일단 포크레인으로 한 번에 긁어서 트럭에 싣는 것'**과 같습니다. 포크레인(멀티 블록 I/O)은 한 번에 많은 양을 옮기지만, 벽돌이 트럭에 실리는 순서는 무질서합니다. 하지만 벽돌을 다 옮겨서 전체 개수를 세는 목적이라면 가장 효율적인 방법입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: 정량적/구조적 분석
인덱스 스캔 방식 간의 기술적 차이와 성능 지표를 비교 분석합니다.

| 비교 항목 | Index Range Scan (IRS) | Index Fast Full Scan (IFFS) | Table Full Scan (TFS) |
|:---|:---|:---|:---|
| **액세스 범위** | 특정 범위 (Range) | 전체 인덱스 (All Blocks) | 전체 테이블 (All Blocks) |
| **읽기 순서** | 논리적 (Key Order) | **물리적 (Disk Order)** | 물리적 (Disk Order) |
| **I/O 방식** | Single Block Read (Random I/O 성격) | **Multi-Block Read (Sequential I/O)** | Multi-Block Read (Sequential I/O) |
| **정렬 보장** | ✅ 보장 (Sorted) | ❌ 미보장 (Unsorted) | ❌ 미보장 (Unsorted) |
| **대용량 처리** | 부적합 (Random Access 비용) | **유리 (High Throughput)** | 유리 (하지만 I/O 양이 많음) |
| **주요 Wait Event** | `db file sequential read` | `db file scattered read` | `db file scattered read` |

#### 과목 융합 관점 분석
1.  **운영체제(OS) & 아키텍처**: IFFS는 OS 레벨의 **파일 시스템 캐시(File System Cache)** 전략과 연관이 깊습니다. Sequential I/O 패턴은 OS의 Read-Ahead(예상 읽기) 알고리즘을 가장 효율적으로 활용합니다. 디스크의 헤드(Head) 이동을 최소화하는 회전 지연(Rotational Latency) 감소 원리와 직결됩니다.
2.  **네트워크 & 분산 DB**: RAC(Real Application Clusters) 환경에서 IFFS는 Interconnect(노드 간 통신망)를 통한 블록 전송보다는 로컬 디스크 스캔을 유도하여 노드 간 캐시 퓨전(Cache Fusion) 오버헤드를 줄이는 데 기여할 수 있습니다.
3.  **데이터 모델링**: 컬럼 개수가 매우 많은 광폭(Wide) 인덱스는 IFFS 수행 시 읽어야 하는 디스크 량이 늘어나 오히려 테이블 전체 스캔보다 느려질 수 있으므로, IFFS를 고려한다면 인덱스 구성을 최적화(Slim)해야 합니다.

#### 📢 섹션 요약 비유
> 일반 인덱스 스캔이 **'기차가 역 순서대로 정차하며 승객을 태우는 것'**이라면, IFFS는 **'버스가 정류장 순서를 무시하고 고속도로를 질주하며 이용객을 수송하는 것'**과 같습니다. 기차는 순서가 보장되지만 느리고, 버스는 순서가 뒤죽박죽이지만 연료 효율(I/O 효율)과 운송 속도가 압도적으로 높습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 실무 시나리오 및 의사결정
**시나리오 1: 대용량 집계 쿼리 튜닝**
- **상황**: 1억 건의 주문 테이블(`ORDERS`)에서 `COUNT(*)`를 수행. 인덱스는 `ORDERS_PK (ORDER_ID)` 존재.
- **문제**: `ORDER_ID` 인덱스를 통해 논리적 스캔 시, 너무 많은 단일 블록 I/O 발생으로 초당 처리량(TPS) 저하.
- **의사결정**: 쿼리가 `ORDER_ID`만 필요하므로(커버링), 테이블 액세스 없이 `ORDERS_PK` 인덱스에 대해 **`/*+ INDEX_FFS(ORDERS ORDERS_PK) */`** 힌트를 부여.
- **결과**: I/O 방식이 `Scattered Read`로 변경되며 처리 시간 50% 단축.

**시나리오 2: 정렬이 필요한 리포팅**
- **상황**: 고객 테이블에서 `SELECT NAME FROM CUSTOMERS ORDER BY NAME` 실행. 인덱스 `CUST_IDX (NAME)` 존재.
- **의사결정**: IFFS는 비정렬 데이터를 반환하므로, `ORDER BY` 연산을 위해 별도의 `SORT ORDER BY` 단계가 필요합니다.
- **판단**: 만약 IFFS 비용 + 소트 비용 > Index Full Scan(이미 정렬됨) 비용이라면, IFFS를 사용하지