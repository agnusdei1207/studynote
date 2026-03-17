+++
title = "438. 다차원 집계(ROLLUP, CUBE) - 합계의 파노라마"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 438
+++

# 438. 다차원 집계(ROLLUP, CUBE) - 합계의 파노라마

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **ROLLUP**과 **CUBE**는 **SQL (Structured Query Language)**의 **GROUP BY** 절을 확장한 연산자로, 단일 쿼리 수행으로 다차원 데이터에 대한 소계(Subtotal) 및 총계(Grand Total)를 자동 생성하는 집계 기능이다.
> 2. **가치**: 애플리케이션 단에서의 복잡한 로직 구현이나 다중 쿼리 실행을 배제하고, **DBMS (Database Management System)** 엔진 차원에서 집계를 수행함으로써 **OLTP (Online Transaction Processing)** 환경의 리소스를 절약하고 데이터 웨어하우스의 보고서 생성 성능을 획기적으로 향상시킨다.
> 3. **융합**: 데이터 웨어하우스 설계 시 핵심이 되는 **OLAP (Online Analytical Processing)** 연산을 SQL 표준으로 구현한 것이며, 비즈니스 인텔리전스(BI) 도구의 데이터 소스로 활용될 때 쿼리 최적화 핵심 기제가 된다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 정의
일반적인 **GROUP BY** 절은 지정된 컬럼의 조합에 대해 단일 레벨의 집계만 생성한다. 예를 들어, `GROUP BY A, B`는 A와 B가 모두 같은 행끼리만 묶어준다. 그러나 실무 비즈니스 보고서에서는 "지역별 합계"뿐만 아니라 "전체 지역 총계" 혹은 "지역 내 제품별 소계"와 같은 다차원 집계가 필수적이다.

여기서 등장하는 것이 **ROLLUP**과 **CUBE**다. 이들은 **GROUPING SETS**라는 개념의 구현체로, 사용자가 여러 **GROUP BY** 문을 **UNION ALL**로 연결하는 수고를 덜어준다. 

*   **ROLLUP**: 계층 구조(Hierarchy)를 가진 데이터의 집계에 적합하며, 지정된 컬럼 순서대로 누적 집계를 수행한다.
*   **CUBE**: 모든 차원(Dimension)에 대한 교차 집계(Cross-Tabulation)를 수행하여, 가능한 모든 조합의 합계를 생성한다.

#### 💡 비유
ROLLUP은 회계 장부에서 '페이지별 합계를 내고, 그 다음 챕터 합계를 내고, 마지막에 전체 총계를 내는' 과정과 같다. CUBE는 '사람의 눈으로 모든 가능한 변수 조합을 확인하며 3차원 입체적으로 보는' 방식과 같다.

#### 등장 배경
1.  **기존 한계**: 복잡한 리포팅을 위해 여러 개의 SELECT 문을 작성하고 UNION해야 했으므로, 코드가冗長(冗長)해지고 테이블을 여러 번 읽는 **I/O (Input/Output)** 부하가 발생했다.
2.  **혁신적 패러다임**: SQL:1999 표준에서 다차원 집계 연산이 도입되며, 단일 스캔(Single Scan)으로 다차원 결과를 도출하는 **Vector Aggregation** 기법이 도입되었다.
3.  **비즈니스 요구**: 데이터 웨어하우스와 **DW (Data Warehouse)** 환경이 확대되며, 대용량 데이터에 대한 실시간 분석 및 대시보드 제공 요구가 급증했다.

#### ASCII 다이어그램: Legacy vs Multi-dimensional Aggregation
아래는 기존 방식(UNION)과 ROLLUP/CUBE 방식의 데이터 처리 흐름을 비교한 것이다.

```text
[ Legacy Method vs. ROLLUP/CUBE ]

  Legacy (UNION ALL) Approach:          ROLLUP/CUBE Approach:
  (High I/O Overhead)                   (Single Scan Optimizer)

  SELECT A, B, SUM(C)                   SELECT A, B, SUM(C)
  FROM T GROUP BY A, B   ──┐            FROM T
                             │            GROUP BY ROLLUP(A, B)
  SELECT A,    SUM(C)       │                │
  FROM T GROUP BY A      ───┤                ▼
                             │           ┌──────────────┐
  SELECT       SUM(C)       │           │ Table Scan   │
  FROM T GROUP BY        ───┘           │ (Just 1 Pass) │
                                     └───────┬────────┘
                                             │
                                      [Aggregation Engine]
                                             │
                               ┌─────────────┼─────────────┐
                               ▼             ▼             ▼
                          (A, B) Sum      (A) Sum      ( ) Total
```
*   **해설**: 기존 방식은 테이블을 3번 읽어야 하지만(①세부집계, ②A집계, ③총계), ROLLUP/CUBE는 최적화된 엔진을 통해 테이블을 단 1회만 읽고 메모리 상에서 집계 결과를 분리하여 출력한다. 이는 대용량 처리에서 압도적인 성능 차이를 보인다.

> **📢 섹션 요약 비유**: 다차원 집계 도입은 마치 복잡한 세무 신고를 위해 각기 다른 서류를 따로 작성하던 것(UNION)을, 스마트한 세무 회사 프로그램(ROLLUP/CUBE)을 통해 입력 단 한 번으로 모든 보고서를 자동 생성하는 것과 같은 효율성을 제공합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 구성 요소 상세 분석
다차원 집계를 구성하는 핵심 요소들은 다음과 같다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **GROUP BY Columns** | 집계 기준 차원(Dimension) | 집계를 수행할 키(Key) 컬럼 리스트 | 엑셀 피벗 테이블의 행/열 라벨 |
| **Aggregation Function** | 수행 연산 | SUM, AVG, COUNT, MAX, MIN 등 데이터를 요약하는 함수 | 계산기의 연산 버튼 |
| **NULL Indicator** | 집계 레벨 식별 | 소계/총계 행에서 집계 기준 컬럼이 NULL로 표시됨 (실제 NULL과 구분 필요) | 빈 칸으로 처리된 상위 단계 |
| **GROUPING() Function** | NULL의 성분 판별 | 해당 컬럼이 집계로 인한 NULL이면 1, 실제 데이터면 0 반환 | "이 NULL은 애초에 없었던 데이터야" 판별기 |
| **GROUPING_ID()** | 비트마스크 레벨링 | 각 컬럼의 GROUPING 결과를 비트 단위로 결합하여 Level 식별자 생성 | 집계 깊이(ID) 부여 태그 |

#### ASCII 구조 다이어그램: ROLLUP vs CUBE Logic
두 연산의 내부 집계 논리(Growth Path)를 시각적으로 비교한다.

```text
[ Logic Comparison: ROLLUP vs CUBE ]
Scenario: Group by DEPT (D) and JOB (J)

  1. ROLLUP(D, J)             2. CUBE(D, J)
     (Hierarchical)               (Combinatorial)
  
  Step 1: (D, J)               Step 1: (D, J)
  Step 2:   (D)  ◄── Reduce    Step 2:   (D)  ◄── Combo
  Step 3:     () ◄── Reduce    Step 3: (J)   ◄── Combo
                             Step 4:   ()  ◄── Combo

  Tree View:                 Tree View:
       [Total]                    [Total]
         / \                       /  |  \
       [D]   ...                 [D] [J] ...
       / \                       / \ / \
     [J] ...                   [J] ...
```
*   **해설**: **ROLLUP**은 오른쪽에서 왼쪽으로 인자를 하나씩 제거해가며 계층적 집계(Level을 줄여나감)를 수행한다. 반면 **CUBE**는 $2^n$ (n은 컬럼 수) 개의 가능한 모든 부분 집합(Power Set)에 대해 집계를 수행한다. 따라서 3개 컬럼 기준 ROLLUP은 4개 레벨을 생성하지만, CUBE는 $2^3=8$개의 그룹을 생성한다.

#### 심층 동작 원리 및 GROUPING 함수
다차원 집계의 핵심은 생성되는 **NULL** 값의 의미를 해석하는 데 있다. 데이터 원본에 존재하는 NULL과 집계 과정에서 생성된 Super-Aggregate NULL을 구분하기 위해 **GROUPING()** 함수를 사용한다.

**동작 단계:**
1.  **Parsing**: SQL 엔진은 ROLLUP/CUBE 인자를 파싱하여 논리적 집계 셋(Grouping Sets)을 나열한다.
2.  **Scanning**: 테이블을 스캔하며 해시(Hashing) 또는 정렬(Sorting) 방식으로 그룹화를 수행한다.
3.  **Calculating**: 각 그룹별로 집계 함수(SUM 등)를 적용하여 결과를 버퍼에 적재한다.
4.  **Tagging**: 집계 레벨별로 GROUPING 비트를 계산한다. (例: ROLLUP(A,B)에서 A가 NULL이면 1, B가 NULL이면 2, 둘 다 NULL이면 3)

```sql
-- 코드 예시: CUBE를 활용한 매출 보고서
SELECT 
    CASE WHEN GROUPING(Region) = 1 THEN 'All Regions' ELSE Region END AS Region,
    CASE WHEN GROUPING(Item)    = 1 THEN 'All Items'    ELSE Item    END AS Item,
    SUM(Sales) AS TotalSales,
    GROUPING_ID(Region, Item) AS Lvl -- 집계 레벨 식별 (0:상세, 1:지역소계, 2:품목소계, 3:총계)
FROM SalesData
GROUP BY CUBE(Region, Item);
```

> **📢 섹션 요약 비유**: 다차원 집계의 동작 원리는 마치 '자동 요약 기능이 들어간 엑셀 피벗 테이블'을 코드로 구현하는 것과 같습니다. 특히 `GROUPING` 함수는 숫자가 '0'인지 실제 데이터가 누락된 'NULL'인지 구별해주는 '마커 펜'과 같아서, 보고서 작성 시 혼란을 방지해 줍니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: ROLLUP vs CUBE vs GROUPING SETS

| 비교 항목 | ROLLUP | CUBE | GROUPING SETS |
|:---|:---|:---|:---|
| **집계 형태** | 계층적 (n+1 레벨) | 조합적 ($2^n$ 레벨) | 사용자 정의 (선택적) |
| **컬럼 순서 의존성** | **높음 (High)** (순서가 결과 결정) | **없음 (None)** | 사용자 지정 |
| **데이터 생성량** | 적음 (Liniear) | 매우 많음 (Exponential) | 가변적 |
| **주요 용도** | 연간/월간 누적 보고서 | 심층 교차 분석 (Cross-Analysis) | 특정 소계만 필요한 불규칙 보고서 |
| **성능 부하** | 낮음 | 높음 (대용량 시 주의 필요) | 중간 (커스터마이징에 따라 다름) |

#### ASCII 다이어그램: Data Growth Explosion
컬럼이 추가될 때마다 증가하는 결과 행(Rows)의 수를 비교한 것이다.

```text
[ Result Set Size Growth Analysis ]

  Input: 2 Columns (A, B) with 2 values each (4 rows base)
  
  ROLLUP(A, B):           CUBE(A, B):
  (A,B), (A), ()          (A,B), (A), (B), ()
  -> 3 Sets               -> 4 Sets

  Input: 3 Columns (A, B, C)
  
  ROLLUP(A,B,C):          CUBE(A,B,C):
  (A,B,C), (A,B), (A), () -> 4 Sets
  
  (A,B,C), (A,B), (A,C), (A),   <- Massive
  (B,C),   (B),   (C),   ()     <- Explosion
  -> 8 Sets (2^3)
```
*   **해설**: ROLLUP은 컬럼이 늘어나도 선형적으로 결과가 늘어나지만, CUBE는 기하급수적으로 결과가 증가한다. 4개 컬럼에 CUBE를 적용하면 16개의 집합이 생성되므로, **BI (Business Intelligence)** 시스템에서 메모리 부족(Out of Memory) 오류가 발생할 수 있어 신중한 설계가 필요하다.

#### 타 과목 융합 관점
1.  **OS (Operating System)**: 대용량 메모리가 할당되어야 하므로, 데이터가 디스크(Swap)로 내려가지 않도록 Huge Page 설정 등 **Memory Management** 기술과 연계된다.
2.  **네트워크**: 클라이언트로 전송되는 데이터셋(Result Set)의 크기가 커질 수 있으므로 네트워크 대역폭을 점유할 수 있다. 압축 프로토콜 사용을 고려해야 한다.

> **📢 섹션 요약 비유**: ROLLUP은 '빌딩을 층별로 짓는 것'과 같아서 순서가 중요하고 자원이 적게 들지만, CUBE는 '모든 가능한 조합의 레고 블록을 다 조립해보는 것'과 같아서 모든 면을 확인할 수 있지만 블록(리소스)이 엄청나게 필요합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 실무 시나리오 및 의사결정
데이터 웨어하우스 구축 프로젝트에서 다음과 같은 상황을 가정한다.

1.  **상황 A: 정기 실적 보고서 (시/도 → 지역 → 전체)**
    *   **판단**: 데이터에 자연스러운 계층 구조가 존재함.
    *   **선택**: **ROLLUP** 사용. 컬럼 순서(시/도, 지역)를 철저히 지켜 인덱스 튜닝을 병행해야 함.
2.  **상황 B: 원인 규명을 위한 탐색적 분석 (지역×제품×채널)**
    *   **판단**: 어느 요소가 매출 하락의 주범인지 모든 조합을 검증해야 함.
    *   **선택**: **CUBE** 사용. 단, 데이터량이 과도하면 Materialized View(구체화 뷰)로 사전 집계하여 성능을 확보해야 함.
3.  **상황 C: 특정 소계만 필요한 UI (대시보드 위젯)**
    *   **판단**: 총계는 필요 없고, 지역별 합계와 제품별 합계만 개별적으로 필요함.
    *   **선택**: **GROUPING SETS** 사용. 불필요한 연산을 제거하여 쿼리 응답 속도를 최우선으로 높임.

#### 도입 체크리스트

| 구분 | 체크 항목 | 설명 |
|:---|:---|:---