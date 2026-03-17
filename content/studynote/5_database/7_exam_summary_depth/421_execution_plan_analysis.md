+++
title = "421. 실행 계획 (Execution Plan) - 쿼리의 내부 지도"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 421
+++

# 421. 실행 계획 (Execution Plan) - 쿼리의 내부 지도

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 실행 계획은 사용자가 작성한 선언적 SQL(Structured Query Language)을 DBMS(Database Management System)가 이해하고 수행 가능한 **절차적 연산자(Operator)의 트리 구조**로 변환한 청사진입니다.
> 2. **가치**: 옵티마이저(Optimizer)가 수집한 통계 정보를 바탕으로 계산한 **Cost(비용)**와 **Cardinality(기대 행 수)**를 노출함으로써, 특정 쿼리의 성능 병목 구간(I/O, CPU, 네트워크)을 정량적으로 분석하고 튜닝할 수 있는 유일한 실마리를 제공합니다.
> 3. **융합**: 운영체제의 파일 시스템 접근 방식(Storage Engine)과 네트워크 프로토콜 간의 데이터 전송 로직이 결합된 지점이며, `EXPLAIN` 명령어를 통해 이러한 내부 동작을 가시화하는 데이터 엔지니어링의 핵심 도구입니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의**
실행 계획(Execution Plan)이란 관계형 데이터베이스 관리 시스템(RDBMS)의 **옵티마이저(Optimizer, 최적화기)**가 SQL 문을 분석하여, 해당 문장을 실행하기 위해 데이터를 어떤 순서로 어떤 방식으로 접근할지 결정한 내부적인 작업 절차입니다. 사용자는 "어떤 데이터를 가져와라(선언적)"라고 요청하지만, 데이터베이스 내부에서는 "어떤 인덱스를 쓰고, 어떤 알고리즘으로 조인하고, 메모리에 어떻게 올릴지(절차적)"를 결정해야 하며, 이 계획이 곧 실행 계획입니다.

**2. 💡 비유**
이는 마치 **'요리사에게 레시피를 내주는 과정'**과 같습니다. 고객(SQL 사용자)은 "맛있는 파스타를 달라"는 주문만 할 뿐이지만, 셰프(옵티마이저)는 냉장고(스토리지) 어디에서 재료를 꺼낼지, 어떤 냄비(메모리/조인 버퍼)를 쓸지, 불을 얼마나 세게(CPU Cost) 할지를 결정하는 구체적인 조리 계획표를 세우게 됩니다.

**3. 등장 배경 및 필요성**
① **기존 한계**: 초기 데이터베이스는 데이터 양이 적어 전체를 읽는 방식(Full Scan)으로도 충분했습니다. 하지만 테라바이트(TB)급 데이터가 쌓이면서 비효율적인 경로 탐색이 치명적인 성능 저하를 초래하게 되었습니다.
② **혁신적 패러다임**: **CBO(Cost-Based Optimizer, 비용 기반 옵티마이저)**의 등장입니다. 단순 규칙(Rule)이 아닌, 데이터 분포도와 시스템 자원(I/O, CPU)을 수학적으로 계산하여 최소 비용의 경로를 찾아내는 방식으로 발전했습니다.
③ **현재 비즈니스 요구**: 대규모 분산 처리 환경에서 복잡한 조인 쿼리가 수초 이상 지연되는 것을 방지하기 위해, 개발자는 이 실행 계획을 통해 '선제적 성능 진단'을 수행해야 합니다.

**4. 📢 섹션 요약 비유**
실행 계획은 **'네비게이션 앱의 세부 경로 안내'**와 같습니다. 사용자가 "집에 가줘"라고 명령(SQL)을 하면, 내비게이션(옵티마이저)은 실시간 교통 상황(통계 정보)을 고려해 "고속도로(인덱스)를 타고 5분 가다가 2번 출구(조인)로 빠져라"는 구체적인 운전 선회 로그(실행 계획)를 보여주는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 분석표**
실행 계획을 구성하는 핵심 요소들은 옵티마이저의 판단 근거가 됩니다.

| 구성 요소 (Component) | 영문 명칭 (Full Name) | 역할 및 내부 동작 | 수학적/기술적 의미 |
|:---|:---|:---|:---|
| **ID** | Operation Identifier | 실행 순서 식별자. 보통 안쪽(하위)에서 바깥쪽(상위)으로 숫자가 증가하며 수행됨. | 트리(Tree) 구조의 깊이(Depth) |
| **Operation** | Node Type | 수행될 단위 작업 (예: `TABLE ACCESS`, `HASH JOIN`, `SORT`) | 관계 대수(Relational Algebra) 연산자 |
| **Name** | Object Name | 접근 대상 객체명 (테이블명, 인덱스명) | 논리적/물리적 스토리지 주소 지정자 |
| **Rows** | Cardinality (기수성) | 각 단계에서 반환될 것으로 예상되는 행의 개수. 정확도가 중요함. | `Selectivity * Total Rows`. 조인 비용 결정의 핵심 변수 |
| **Bytes** | Data Volume | 예상되는 데이터 양 (Byte 단위). 메모리 사용량 예측에 활용. | `Rows * Row Size`. PGA 메모리 할당 크기 결정 |
| **Cost** | Optimizer Cost | 옵티마이저가 산출한 상대적인 자원 소모비용 (I/O + CPU). 절대값보다 비교값이 중요함. | 단위 페이지 I/O 비용 + CPU 사이클 비용의 가중합 |
| **Time** | Elapsed Time | 예상 소요 시간 (초/분). | Cost를 실제 시간 단위로 환산한 추정치 |

**2. 실행 계획 트리 구조 및 흐름 (ASCII)**

아래는 인덱스를 활용해 부서(Department)가 'IT'인 직원들의 급여(Salary)를 집계하는 과정을 도식화한 것입니다.

```text
[ Execution Plan Tree & Data Flow ]

   Operation (Id)          Object           Rows  Cost  💡 Internal Logic
---------------------------------------------------------------------------
  0. SELECT STATEMENT      -                  5    12    [ Result Output ]
       △
  1.  HASH GROUP BY        -                  5    12    [ Aggregation : SUM(Salary) ]
       △
  2.   HASH JOIN           -                100    10    [ Join : EMP ⇔ DEPT ]
       △                   △
  3.    TABLE ACCESS       EMP (Emp Dept)   100     4    [ Probe : Read by RowID ]
       BY INDEX ROWID      |
       |                   |
  4.    INDEX RANGE SCAN   EMP_DEPT_IDX     100     2    [ Access : Find IT Dept ]
                           |
                           △
  5.    TABLE ACCESS FULL  DEPT              10     3    [ Build : Load Dept Info ]
---------------------------------------------------------------------------

  [ 📥 Reading Order: Bottom-Up (Depth-First) ]
  ① Step 4~5 (Read Inputs) ──▶ ② Step 2 (Join) ──▶ ③ Step 1 (Group) ──▶ ④ Step 0 (Return)
```

**3. 심층 동작 원리 및 메커니즘**

실행 계획은 결코 평면적으로 수행되지 않으며, **트리(Tree)의 잎(Leaf) 노드에서 뿌리(Root) 노드로 향하는 Bottom-Up 방식**으로 동작합니다.

① **자식 노드(Child Node) 수행**: 가장 먼저 실행되는 것은 가장 깊이 들어간 단계(Indent가 가장 많은 부분)입니다. 위 예시에서 `INDEX RANGE SCAN`과 `TABLE ACCESS FULL`이 가장 먼저 실행되어 데이터를 읽습니다.
② **부모 노드(Parent Node)로 데이터 전달(Pass)**: 자식 노드가 데이터를 읽어 부모에게 전달합니다. `HASH JOIN`은 두 자식 노드(EMP, DEPT)로부터 데이터를 모두 받아야만 조인 작업을 시작할 수 있습니다.
③ **조인 및 연산**: 부모 노드는 받은 데이터를 가공합니다. 필터링(`FILTER`), 정렬(`SORT ORDER BY`), 집계(`HASH GROUP BY`) 등이 이 단계에서 수행됩니다.
④ **최종 결과 반환**: 최상위 `SELECT STATEMENT` 단계까지 도달하면 결과가 사용자에게 반환됩니다.

**4. 핵심 알고리즘 및 코드 (SELECTivity)**

옵티마이저가 인덱스를 탈지 말지 결정하는 핵심 공식은 **Selectivity(선택도)**입니다.

```sql
-- 공식: Selectivity = (Distinct Count of Column Value) / (Total Row Count)

-- 예시: Employees 테이블에 10,000명이 있고, 부서(Department)가 100개라면?
-- Selectivity(Department) = 100 / 10,000 = 0.01 (1%)

-- 옵티마이저 판단 로직 (Pseudo-Code)
IF (Selectivity < 0.05) THEN  -- 선택도가 5% 미만이면
    USE_INDEX_PATH();         -- 인덱스 범위 스캔 (INDEX RANGE SCAN) 선택
ELSE
    USE_FULL_SCAN_PATH();     -- 풀 테이블 스캔 (TABLE ACCESS FULL) 선택
END IF;
```

**5. 📢 섹션 요약 비유**
이 과정은 **'자동차 조립 라인의 흐름'**과 같습니다. 가장 기초 부품(데이터 행, Row)이 컨베이어 벨트(자식 노드)를 타고 올라오면, 중간 공정(조인/필터링)에서 부품을 결합하고 불량품을 걸러내며, 최종적으로 완성차(최종 쿼리 결과)가 출고되는 상위 단계로 이동하는 구조입니다. 각 공정별 예상 소요 시간(Cost)이 사전에 산정되어 있는 셈입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 접근 방식 비교: Index Scan vs. Full Scan**

| 비교 항목 | Index Scan (인덱스 스캔) | Full Table Scan (전체 테이블 스캔) |
|:---|:---|:---|
| **동작 원리** | 인덱스 리프 블록을 경유하여 ROWID로 테이블 접근 | 테이블의 **HWM(High Water Mark)** 아래에 있는 모든 블록을 순차 읽기 |
| **I/O 패턴** | **Random Access I/O** (논리적 위치 건건이 이동) | **Sequential I/O** (물리적으로 인접한 블록을 연속 읽기) |
| **적합 상황** | 데이터 일부(5~10% 이하) 조회, 정확한 매칭 | 대부분의 데이터 조회, 대용량 배치 작업 |
| **성능 영향** | 소량 데이터는 빠름, 다량에서는 Single Block Read 부하 발생 | 디스크 헤드 이동이 적어 대량 처리 시 유리 (Multi Block Read) |
| **DB 융합 관점** | **OS(운영체제)** 관점에서의 페이지 캐시(Page Cache) 히트율 변동 발생 | **Storage(스토리지)** 계층에서의 순차 읽기 최적화(Sequential Prefetch) 활용 가능 |

**2. 옵티마이저 모델 비교: RBO vs. CBO**

| 특징 | RBO (Rule-Based Optimizer) | CBO (Cost-Based Optimizer) |
|:---|:---|:---|
| **기준** | 미리 정해진 우선순위 규칙 (예: 인덱스 있으면 무조건 사용) | 통계 정보(Statistics)를 바탕으로 비용(Cost) 계산 |
| **정확도** | 데이터 분포를 고려하지 않아 비효율 가능성 높음 | 현재 데이터 상황을 반영하여 합리적인 선택 |
| **현행 표준** | 폐기 (Legacy) | **현재 표준 (Oracle 10g+, PostgreSQL 등)** |

**3. 타 과목 융합 관점**

- **[운영체제(OS)와의 융합]**: 실행 계획의 `Cost`는 결국 OS의 **시스템 콜(System Call)** 횟수와 **버퍼 캐시(Buffer Cache)** 관리 전략과 연결됩니다. `Multi Block Read` 설정은 OS의 I/O 배치 크기와 직접적인 상관관계가 있습니다.
- **[네트워크와의 융합]**: 분산 데이터베이스 환경에서의 실행 계획은 **네트워크 대기 시간(Latency)**을 고려해야 합니다. 데이터를 가져오는 곳(Remote)으로 보낼지 로컬에서 가져올지(Local) 결정하는 것이 실행 계획에 포함됩니다.

**4. 📢 섹션 요약 비유**
인덱스 스캔과 풀 스캔의 선택은 **'도서관에서 책 찾기'** 방식의 차이와 같습니다. 원하는 책이 한 권(소량 데이터)이라면 목차(인덱스)를 보고 서가 바로 찾아가는 것이 빠르지만(랜덤 액세스), 책장의 책 대부분(대량 데이터)을 옮겨야 한다면 목차를 보지 않고 그 줄(블록) 전체를 싹 긁어오는 것이(순차 액세스) 더 효율적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

- **상황 1: 예상 행 수(Cardinality)와 실제 행 수의 차이**
    - **현상**: 실행 계획상 `Rows`가 1건으로 예상되었는데 실제로는 100만 건이 나오는 경우.
    - **판단**: 통계 정보가 오래되었거나 히스토그램이 없음.
    - **대책**: `ANALYZE TABLE` 혹은 `DBMS_STATS.GATHER_TABLE_STATS` 명령어로 최신 통계 정보를 수집해야 함.

- **상황 2: "TABLE ACCESS FULL" 경고 발생**
    - **현상**: 인덱스 컬럼으로 조회했음에도 불구하고 전체 스캔이 발생.
    - **판단**: 암묵적 형변환(Implicit Type Conversion)이 의심됨. (예: 문자열 컬럼에 숫자형 조건 `WHERE col = 123` 사용)
    - **대책**: 데이터 타입을 일치시켜 인덱스 탈생을 유도함.

- **상황 3: Nested Loops vs Hash Join**
    - **현상**: 소량 테이블 조인임에도 Hash Join이 발생하여 느림.
    - **판단**: Hash Join은 해시 테이블 생성(메모리/CPU 오버헤드)이 필요하므로, 소량 데이터는 Nested Loops가 유리함.
    - **대책**: 힌트(Hint, 예: `/*+ USE_NL(A B) */`)를 사용하여 실행 계획을 강제 변경.

**2. 도입 체