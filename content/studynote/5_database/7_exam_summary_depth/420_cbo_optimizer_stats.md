+++
title = "420. 옵티마이저 CBO와 시스템 통계 - 데이터의 경제학"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 420
+++

# 420. 옵티마이저 CBO와 시스템 통계 - 데이터의 경제학

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CBO (Cost-Based Optimizer)는 데이터 딕셔너리(Data Dictionary)에 저장된 시스템 통계를 기반으로 각 실행 계획의 예상 비용(Cost)을 수학적으로 계산하여, 자원 사용량이 최소화되는 경로를 선택하는 확률론적 쿼리 엔진이다.
> 2. **가치**: RBO(Rule-Based Optimizer)의 정적 규칙 한계를 극복하여, 데이터의 분도(Skew)나 규모 변화에 따라 동적으로 최적화된 실행 계획을 수립하며, 이는 대용량 트랜잭션 처리(OLTP) 및 배치 처리(OLAP) 성능의 근간이 된다.
> 3. **융합**: OS의 I/O 서브시스템 비용 모델과 컴퓨터 아키텍처의 CPU 코어 사용률을 결합하여 비용을 산정하며, AI/ML 기반의 자동 진단 및 튜닝(Autonomous Database)으로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

**개념**
CBO (Cost-Based Optimizer, 비용 기반 옵티마이저)는 관계형 데이터베이스 관리 시스템(RDBMS)의 SQL 엔진이 쿼리를 실행할 때, **"어떤 경로로 데이터에 접근하는 것이 전체 시스템 자원(I/O, CPU, Memory)을 가장 적게 소모하는가?"**를 판단하는 핵심 의사결정 모듈이다. 단순히 규칙에 따르는 것이 아니라, 테이블의 행 수, 인덱스의 높이(Height), 데이터 분포도(Selectivity) 등의 **통계적 확률**을 바탕으로 비용을 계산한다.

**💡 비유**
CBO는 **'실시간 교통 정보(Traffic Data)를 활용하는 스마트 내비게이션'**과 같다. 단순히 "고속도로가 국도보다 빠르다"는 고정된 규칙(RBO)을 따르는 것이 아니라, 현재 도로의 소통 상황(데이터 분포), 거리(I/O 양), 신호 대기 시간(CPU 연산)을 고려하여 "지금은 우회 도로가 5분 더 빠르다"라고 최적의 경로를 제시한다.

**등장 배경**
1.  **기존 한계**: 초기 옵티마이저인 RBO(Rule-Based Optimizer)는 데이터의 양이나 분포와 상관없이 rankings(순위)에 따른 고정된 규칙만 적용했다. 예를 들어 "인덱스가 있으면 무조건 인덱스를 탄다"는 논리는, 데이터가 전체의 90%에 달할 때 오히려 인덱스를 경유하는 Random I/O가 Table을 읽는 Sequential I/O보다 느려지는 부조화를 낳았다.
2.  **혁신적 패러다임**: 1990년대 중반 Oracle 7 등장과 함께 데이터 분석 기술이 도입되면서, **"실제 데이터의 물리적 상태를 반영하자"**는 패러다임이 등장했다. 이는 단순 규칙을 넘어 수학적 모델링을 통한 비용 산정(Cost Calculation)의 시대를 열었다.
3.  **현재의 비즈니스 요구**: TB~PB급 대용량 데이터 환경에서는 쿼리 실행 계획의 1% 차이가 수 분, 수 시간의 성능 차이로 이어진다. 따라서 CBO는 데이터베이스 성능 튜닝의 가장 중요한 통제 포인트(Control Point)가 되었다.

**📢 섹션 요약 비유**: CBO는 마치 **'복잡한 물류 센터의 배송 관제 시스템'**과 같습니다. 단순히 "트럭이 크면 무조건 많이 싣는다"는 규칙(RBO)을 고수하기보다, 현재 창고의 재고 위치(데이터 분포), 도로 상태(디스크 상태), 배송 마감 시간(쿼리 성능 요구사항)을 종합 분석하여 가장 적은 비용으로 물건을 배송하는 최적의 루트를 찾아주는 두뇌와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CBO의 내부 작동은 크게 **후보군 생성(Search Space)**, **비용 산정(Cost Estimation)**, **계획 선택(Plan Selection)**의 3단계로 이루어지며, 이 과정에서 시스템 통계(System Statistics)는 필수적인 입력 변수가 된다.

#### 1. 구성 요소 및 상세 동작

CBO 옵티마이저의 주요 내부 모듈과 역할은 다음과 같다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 파라미터 | 관련 통계 (Stats) |
|:---|:---|:---|:---|
| **Query Transformer** | 쿼리 변환 | 뷰 병합(View Merging), 조건 전달(Predicate Pushing), 비 materialized 뷰 재작성 | N/A |
| **Estimator** | 비용 예측 | Selectivity(선택도), Cardinality(기수성) 계산 <br> *Sel = 1 / Num_distinct* | Column Histogram, NDV |
| **Plan Generator** | 계획 생성 | Access Path 결정, Join Method 선택, Join Order 순열 조합 | Table Blocks, Index BLevel |
| **Cost Model** | 비용 모델 | I/O Cost(#BlockReads) + CPU Cost(CPUCycles) <br> *Total Cost = IO + CPU + Network* | SysStats (IOTiming, CPUSpeed) |

#### 2. ASCII 구조 다이어그램: CBO 최적화 파이프라인

아래는 SQL 문장이 입력되어부터 최종 실행 계획이 결정되기까지의 내부 흐름도이다.

```text
[ SQL Parsing ] ──▶ [ Query Transformer ] ──▶ [ Optimizer Core (CBO) ]
                         (Rewrite)                     │
                                                        │
           ┌────────────────────────────────────────────┼───────────────────┐
           │                                            │                   │
           ▼                                            ▼                   ▼
   [ Statistics Manager ]                     [ Plan Generator ]    [ Cost Model ]
   (Dictionary Cache)                         (Search Space)         (Math Model)
   - Table: 1M rows                                │                    |
   - Col_A: Dist(100)                              │                    |
   - Hist: Skewed                                  ▼                    ▼
           │                         [ Plan 1: Index Scan ]      [ Cost Calc ]
           │                         [ Plan 2: Full Scan ]       (I/O + CPU)
           │                         [ Plan 3: Hash Join ]            │
           └───────────────────(Info Feed)──────────────┴──────────────┘
                                        │
                                        ▼
                            [ Decision Matrix ]
                            Plan 1: Cost 500
                            Plan 2: Cost 120 ✅ (Lowest)
                            Plan 3: Cost 800
                                        │
                                        ▼
                            [ Final Execution Plan ] ──▶ [ Executor Engine ]
```

**다이어그램 해설**:
1.  **Statistics Manager**: 데이터 딕셔너리에서 수집된 통계 정보(행 수, 컬럼 카디널리티, 히스토그램 등)를 조회하여 Optimizer Core로 전달한다.
2.  **Plan Generator**: 가능한 모든 실행 경로(인덱스 스캔, 전체 스캔, 조인 순서 변경 등)를 생성한다.
3.  **Cost Model**: 각 계획에 대해 `I/O Cost` (디스크 블록 읽기 횟수)와 `CPU Cost` (연산 비용)를 합산하여 총비용(Total Cost)을 산출한다. 이때 Clustering Factor(클러스터링 팩터)가 인덱스 스캔 비용에 큰 영향을 미친다.
4.  **Decision Matrix**: 최소 비용을 가진 Plan 2를 선택하여 실행 엔진으로 전달한다.

#### 3. 핵심 알고리즘 및 공식

CBO의 핵심은 비용을 산정하는 수학적 모델이다.

*   **Selectivity (선택도)**: 특정 조건에 의해 반환될 행의 비율 (0.0 ~ 1.0).
    $$ \text{Selectivity} = \frac{\text{조건을 만족하는 행 수}}{\text{전체 행 수 (Num\_rows)}} $$
    *   예: `Unique Column = Value` $\rightarrow$ Selectivity = $1 / \text{Num\_distinct}$
*   **Cardinality (기수성)**: 조건을 만족하는 예상 행 수.
    $$ \text{Cardinality} = \text{Selectivity} \times \text{Num\_rows} $$
*   **Total Cost (총 비용)**:
    $$ \text{Cost} = (\# \text{Single Block Reads} \times \text{SRWAIT}) + (\# \text{MultiBlock Reads} \times \text{MRWAIT}) + (\# \text{CPU Cycles} \times \text{CPUSPEED}) $$
    *(SRWAIT: Single Block Wait Time, MRWAIT: Multi Block Wait Time)*

**코드 스니펫 (Oracle DBMS_STATS 예시)**
통계 정보 수집이 CBO의 판단에 미치는 영향을 보여주는 실무 명령어다.

```sql
-- 1. 통계 정보 수집 (Estimate Percent 활용)
-- 표본 추출(ESTIMATE)을 통해 전체 테이블 스캔 부하를 줄이면서도 높은 정확도 달성
BEGIN
    DBMS_STATS.GATHER_TABLE_STATS(
        ownname => 'SCOTT',
        tabname => 'EMP',
        estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE, -- AI 기반 자동 샘플링
        method_opt => 'FOR ALL COLUMNS SIZE AUTO', -- 히스토그램 자동 생성
        degree => 8 -- 병렬 처리
    );
END;

-- 2. 통계 정보 확인 및 비교 (오브젝트 별)
SELECT * FROM DBA_TAB_STATISTICS 
WHERE OWNER = 'SCOTT' AND TABLE_NAME = 'EMP';
```

**📢 섹션 요약 비유**: CBO의 최적화 과정은 **'대형 마트의 계산대 개설 시뮬레이션'**과 같습니다. 점장(옵티마이저)은 손님 수(데이터 건수)와 담긴 물건의 개수(데이터 크기)를 분석하여, "계산대 1개를 10분 쓰는 것과 3개를 3분 쓰는 것 중 어떤 게 더 효율적인가?"를 시뮬레이션(비용 계산)합니다. 이때 고객의 혼잡도(Selectivity)를 정확히 알지 못하면, 계산대를 너무 많이 열거나(과도한 메모리 사용) 너무 적게 열어(병목 발생) 손해를 보게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: RBO vs CBO

옵티마이저의 진화 과정과 CBO의 장단점을 분석한다.

| 비교 항목 | RBO (Rule-Based Optimizer) | CBO (Cost-Based Optimizer) |
|:---|:---|:---|
| **작동 기반** | 미리 정의된 순위 규칙 (Ranking) (예: Index Scan > Full Scan) | 통계 기반 수학적 비용 모델 (Cost Model) |
| **데이터 인지** | 데이터 분포, 행 수 무시 (Data Independent) | 데이터 분포, 행 수, 리프 블록 수 반영 (Data Aware) |
| **장점** | 계산 부하가 없어 실행 계획 수립이 매우 빠름 (일관된 결과) | 데이터 특성에 따라 항상 최적의 경로 선택 가능 (유연함) |
| **단점** | 데이터가 많을 때 인덱스 사용이 비효율적일 수 있음 | 통계 정보가 부정확하면 최악의 계획 선택 가능 (오버헤드) |
| **지원 여부** | Oracle 10g 이후 deprecated, 현재는 거의 사용 안 함 | 대부분의 현대 RDBMS(Oracle, MySQL 8.0, PostgreSQL)의 기본 |

#### 2. 과목 융합 관점 (OS & Data Structure)

*   **융합 1: 운영체제(OS)와의 관계**
    *   CBO가 계산하는 비용의 핵심은 **I/O**다. OS 커널의 파일 시스템(File System)이 HDD(Hard Disk Drive)인지 SSD(Solid State Drive)인지에 따라 `Random I/O`와 `Sequential I/O`의 비용이 다르다.
    *   *Example:* SSD 환경에서는 Random I/O의 비용이 HDD 대비 획기적으로 낮으므로, CBO가 과거에는 인덱스 스캔을 기피했더라도 SSD에서는 더 적극적으로 인덱스를 활용하도록 비용 모델이 튜닝되어야 한다.

*   **융합 2: 자료 구조와의 관계**
    *   **B-Tree Index (Balanced Tree)**: CBO는 인덱스의 높이(B-Level/Height)를 확인하여 비용을 산정한다. 높이가 3인 인덱스는 3번의 I/O가 필요하므로, 전체 테이블 스캔의 비용과 비교하여 판단한다.
    *   **Clustering Factor**: 데이터가 디스크 상에 인덱스 순서와 얼마나 정렬되어 있는지를 나타내는 지표로, CBO가 "Index Scan 후 Table Access"를 할지 "Full Table Scan"을 할지 결정하는 가장 중요한 척도가 된다.

**📢 섹션 요약 비유**: RBO와 CBO의 차이는 **'종이 지도(RBO)와 실시간 내비게이션(CBO)'**의 차이입니다. 종이 지도는 "이 도로는 고속도로니까 무조건 빠르다"는 정설(규칙)을 따르지만, 공사 중이거나 정체 구간을 모릅니다. 반면 내비게이션은 현재 도로의 노면 상태(OS I/O 성능)와 차량 밀집도(Cardinality)를 실시간으로 반영하여, 비록 지름길(인덱스)이라도 속도가 느리면 우회로(Full Scan)를 추천하는 지능형 판단을 내립니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실제 업무 환경에서 CBO를 통제하고 최적의 성능을 끌어내기 위한 전략을 다룬다.

#### 1. 실무 시나리오 및 의사결정

**시나리오 1: 갑자기 느려진 쿼리 (Plan Regression)**
*   **상황**: 어제 잘 되던 쿼리가 갑자기 10배 느려짐.
*   **원인**: 배치 작업으로 인해 데이터의 양이 급증했는데 통계 정보 갱신이 안 되었거나, 반대로 아주 적은 데이터를 가진 상태에서 "10000건이 있다"는 오래된 통계를 참조하여 잘못된 계획(Index Scan을 선택했어야 함을 Full Scan 선택)을 수립한 경우.
*   **대응**: `DBMS_STATS.GATHER_TABLE_STATS`를 즉시 수행하여 통계 정보를 실체화