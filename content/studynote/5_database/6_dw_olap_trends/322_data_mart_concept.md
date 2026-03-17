+++
title = "322. 데이터 마트 (Data Mart) - 부서별 맞춤형 데이터"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 322
+++

# 322. 데이터 마트 (Data Mart) - 부서별 맞춤형 데이터

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 마트(Data Mart)는 전사적 데이터 웨어하우스(Enterprise Data Warehouse, EDW)의 방대한 데이터 중 특정 부서(예: 마케팅, 영업, 재무)나 비즈니스 라인(Business Line)에 국한된 데이터만을 추출·요약·집계하여 구축한 **'특화된 분석용 데이터 저장소'**다.
> 2. **가치**: DW(DW)의 복잡성과 성능 저하 문제를 해결하여, **쿼리 응답 속도(Query Response Time)를 획기적으로 개선**하고 현업 사용자에게 친숙한 스키마(Schema)를 제공함으로써 의사결정 속도를 단축시킨다.
> 3. **융합**: DW 구축 방법론론(Inmon vs Kimball)에 따라 종속형(Dependent)과 독립형(Independent)으로 나뉘며, 최근에는 데이터 레이크(Data Lake)와 가상화(Virtualization) 기술과 결합하여 물리적 이관 비용을 줄이는 **논리적 데이터 마트(Logical Data Mart)** 형태로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
데이터 마트는 단순히 DW의 데이터를 복사한 것이 아니라, **"특정 사용자의 관점(Viewpoint)에서 세상을 바라보는 데이터"**다. 전사적인 관점의 정규화(Normalization)된 데이터를 현업이 이해하기 쉬운 **차원 모델링(Dimensional Modeling)** 형태(Star Schema, Snowflake Schema)로 변환하여 제공한다. 이를 통해 사용자는 복잡한 테이블 조인(Join) 없이도 직관적인 비즈니스 질문을 던지고 답을 얻을 수 있다.

**2. 등장 배경 (Problem & Paradigm)**
① **DW의 병목 현상**: DW가 모든 부서의 모든 데이터를 통합하면서 용량이 페타바이트(PB) 단위로 증가함에 따라, 단순한 부서별 리포트 생성에도 전체 스캔(Full Table Scan)이 발생하여 성능이 저하되는 문제가 발생했다.
② **민첩한 의사결정의 요구**: 경영 환경의 변화 속도가 빨라지면서, 일주일에 한 번 돌아오는 배치(Batch) 리포트가 아닌 실시간(Real-time)에 가까운 애드혹(Ad-hoc) 쿼리 성능이 요구되었다.
③ **Self-BI의 확산**: IT 부서에 의존하지 않고 현업 사용자가 직접 데이터를 분석하는 '셀프 서비스 BI(Self-Service BI)' 문화가 확산되며, 사용자 친화적이고 경량화된 데이터 저장소의 필요성이 대두되었다.

**3. 구조적 위치**
데이터 웨어하우스가 단일 원천(Single Source of Truth)을 목표로 한다면, 데이터 마트는 **"다중 사용자를 위한 다중 뷰(Multiple Views for Multiple Users)"**를 제공하는 계층이다.

> **📢 섹션 요약 비유**: 데이터 웨어하우스가 **'모든 물건을 분류하여 보관하는 거대한 물류 센터(Distribution Center)'**라면, 데이터 마트는 **'편의점 편의점'**이나 **'매장 내 진열대'**와 같습니다. 고객(현업 부서)이 거대한 창고에서 물건을 찾는 대신, 필요한 상품만 미리 정리해둔 근처의 편의점에서 즉시 구매(분석)할 수 있도록 하는 셈입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소**

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Action) | 비유 (Analogy) |
|:---|:---|:---|:---|
| **데이터 추출 (Extraction)** | DW에서 필요 데이터 선정 | ETL(Extract, Transform, Load) 프로세스를 통해 소스 데이터를 식별하고 추출 | 물류 센터에서 상품 고르기 |
| **변환 및 요약 (Transform)** | 데이터 형태 변환 | 비즈니스 로직에 따라 Aggregation(Sum, Avg), 가공, Cleansing 수행 | 낱개 포장 → 세트 상품 포장 |
| **차원 모델 (Dimension)** | 분석의 축 제공 | 시간, 지역, 상품 등 Key 기준으로 데이터를 Slcing & Dicing 가능하게 함 | 필터 기준(예: "서울지역") |
| **팩트 테이블 (Fact Table)** | 실제 측정값 저장 | 수치 데이터(매출액, 수량)와 Foreign Key로 구조화된 중심 테이블 | 계산서의 세부 품목 |
| **메타데이터 (Metadata)** | 데이터 지도 제공 | 데이터의 정의, 출처, 갱신 주기 등을 기술하여 사용자 가이드 제공 | 상품 라벨 및 설명서 |

**2. 데이터 흐름 및 아키텍처 (ASCII Diagram)**

```text
      [ Data Mart Architecture : Top-Down & Bottom-Up Flow ]

┌─────────────────────────────────────────────────────────────────────┐
│                       Operational Systems (OLTP)                    │
│                     (ERP, CRM, SCM, SFA... )                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ ETL (Extract, Transform, Load)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Enterprise Data Warehouse (EDW) - 3NF                  │
│          (Normalized, Integrated, "Single Source of Truth")         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
         ┌──────────────────────┴──────────────────────┐
         │    Data Propagation / Transformation       │
         │ (Subset, Summarize, Denormalize to Star/Snowflake)       │
         └──────────────────────┬──────────────────────┘
                                ▼
      ┌───────────────────────────────────────────────────┐
      │           Dependent Data Mart Layer                │
      │  (Subject-Oriented, Performance Optimized)         │
      ├─────────────────┬─────────────────┬───────────────┤
      │   Sales DM      │    HR DM        │   Finance DM  │
      │ (Star Schema)   │ (Snowflake)     │ (Custom View) │
      ├─────────────────┴─────────────────┴───────────────┤
      │   • Fast Query Performance                        │
      │   • Departmental Terminology                      │
      │   • Aggregated Summaries (Pre-calculated)         │
      └───────────────────────┬───────────────────────────┘
                                │ BI / Analytics Tool
                                ▼
                      ┌────────────────────┐
                      │  End-User Insight  │
                      └────────────────────┘
```

**3. 심층 동작 원리 (Schema Deep Dive)**
데이터 마트의 핵심은 **'성능 최적화를 위한 의도적인 비정규화(Denormalization)'**다. DW의 제3정규형(3NF) 스키마는 데이터 중복을 최소화하여 무결성을 유지하지만, 쿼리 수행 시 수많은 테이블 조인(JOIN)을 유발하여 느리다. 반면, 데이터 마트는 조회 성능을 위해 **Star Schema(성jang Schema)**를 주로 사용한다.

*   **Fact Table**: 중심에 위치하며, 외래키(FK)와 측정값(Measures)을 가짐.
*   **Dimension Table**: Fact Table의 FK를 참조하며, 상세 설명 속성을 가짐.
*   **Pre-Aggregation**: 자주 쿼리되는 연산(예: 일별 매출 합계)은 미리 계산하여 저장함으로써 런타임 부하를 줄인다.

**4. 핵심 알고리즘 및 프로세스 (Pseudo Code)**
ETL 프로세스 중 가장 부하가 큰 '증분 로딩(Delta Load)'과 '요약(Aggregation)' 로직이다.

```sql
-- [Pseudo SQL: Incremental Update in Data Mart]
-- 1. Identify changes from DW (Staging)
CREATE TABLE Staging_Changes AS
SELECT *
FROM Enterprise_DW.Sales_Transactions
WHERE last_updated > :last_run_time;

-- 2. Update Fact Table (Type 2 SCD - Handling History)
MERGE INTO Mart_Sales.Fact_Revenue AS Target
USING Staging_Changes AS Source
ON (Target.transaction_id = Source.transaction_id)
WHEN MATCHED AND Source.is_deleted = TRUE THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET Target.amount = Source.amount, Target.updated_at = NOW()
WHEN NOT MATCHED THEN
    INSERT (transaction_id, amount, date_key, product_key)
    VALUES (Source.id, Source.amount, TO_DATE(Source.date), Source.prod_key);

-- 3. Refresh Aggregated Indexes (Materialized View Refresh)
REFRESH MATERIALIZED VIEW Mart_Sales.Monthly_Summary;
```

> **📢 섹션 요약 비유**: 데이터 마트 구축은 **'요리를 위한 재료 미리 손질하기'**와 같습니다. 거대한 냉장고(DW)에서 요리할 때마다 야채를 씻고 깎는 것(Join 연산)은 비효율적입니다. 데이터 마트는 미리 다듬어진 국물(요약 데이터)과 썰어둔 재료(차원 데이터)를 냉장 보관했다가, 주문이 들어오면 즉시 요리(Query)하여 내어놓는 **'밀키트(Meal Kit)' 센터**와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 유형별 비교 분석: 종속형 vs 독립형**

| 구분 | 종속형 데이터 마트 (Dependent DM) | 독립형 데이터 마트 (Independent DM) |
|:---|:---|:---|
| **데이터 원천** | **EDW (Enterprise Data Warehouse)** | **각 운영 시스템 (Legacy/OLTP)** |
| **아키텍처** | 하향식 (Top-Down: Inmon Approach) | 상향식 (Bottom-Up: Kimball Approach) |
| **데이터 정합성** | **높음 (High)** | 낮음 (Low, Silo 발생 가능) |
| **구축 기간** | 느림 (DW 구축 후 가능) | 빠름 (부서별 즉시 구축 가능) |
| **데이터 중복** | 최소화 (DW 기준 단일 버전) | 심각 (부서 간 중복 및 불일치) |
| **유지보수 비용** | 상대적으로 낮음 (중앙 관리) | 높음 (각각의 ETL 및 인터페이스 관리) |
| **적합 상황** | 전사적 데이터 표준이 중요한 대기업 | 특정 부서의 긴급한 분석 요구가 있을 때 |

**2. DW vs Data Mart 정량적 비교**

| 비교 지표 | 데이터 웨어하우스 (DW) | 데이터 마트 (Data Mart) |
|:---:|:---|:---|
| **데이터 범위** | 기업 전체 (Enterprise-wide) | 특정 부서/주제 (Departmental) |
| **데이터 상세도** | 상세 데이터 (Detail, Atomic) | 요약/집계 데이터 (Aggregated) |
| **스키마 구조** | 복잡 (정규화, 3NF) | 단순 (차원 모델, Star/Snowflake) |
| **사용자 층** | 데이터 관리자, 분석가 | 경영진, 일반 현업 사용자 |
| **Query 성능** | 느림 (초~수분, 대량 조인) | 빠름 (초단위, 인덱스 최적화) |
| **저장 매체** | 저렴한 대용량 디스크 (HDD/Cloud S3) | 고속 SSD/메모리 최적화 (In-Memory) |

**3. 타 기술 영역과의 융합 (Convergence)**

*   **[Database] OLAP (Online Analytical Processing) 엔진**:
    데이터 마트는 MOLAP(Multidimensional OLAP)이나 ROLAP(Relational OLAP) 엔진의 데이터 소스로 활용된다. 예를 들어, Microsoft Analysis Services(SSAS)나 Oracle Essbase 같은 OLAP 큐브(Cube)를 구축하기 위한 기반 데이터를 제공한다.
*   **[AI/ML] 데이터 사이언스 플랫폼**:
    데이터 마트는 AI 모델 훈련을 위한 **'피처 스토어(Feature Store)'**의 역할을 수행한다. 전체 데이터가 아닌 "마케팅 캠페인 반응률" 피처가 정의된 마트는 데이터 사이언티스트가 모델을 학습시키기 전 피처 엔지니어링을 수행하는 핵심 거점이 된다.

> **📢 섹션 요약 비유**: 독립형 마트가 서로 통신 없이 구축되는 것은 **'각자 자신만의 언어를 사용하는 섬나라(Silo)'**와 같습니다. 반면, 종속형 마트는 중앙 정부(DW)의 표준어를 사용하는 지사(Branch)와 같습니다. 최근은 이 둘을 융합하여, 물리적인 데이터 이동 없이 논리적으로만 필요한 정보를 빌려오는 **'공용 도서관 카드 시스템(Virtualization)'**처럼 진화하고 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 매트릭스**

*   **시나리오 A: 급증하는 트래픽으로 인한 DW 성능 저하**
    *   *상황*: 연말 결산 시즌, 재무팀의 대용량 쿼리로 인해 전사 DW의 CPU 사용률이 90%를 넘어 마케팅팀의 쿼리가 타임아웃(Time-out) 발생.
    *   *대책*: 재무팀용 데이터 마트를 별도로 구축하고, 스케줄링(Scheduling)을 통해 새벽 시간대에 DW로부터 데이터를 복사해 오도록 설정.
    *   *결과*: DW 부하 분산으로 전사 시스템 안정화 확보.

*   **시나리오 B: 데이터 정합성 이슈 (버전 관리)**
    *   *상황*: 독립형 마트와 DW의 '판매량' 수치가 다름. 경영진은 어떤 수치를 믿어야 할지 혼란.
    *   *대책*: **SSOT (Single Source of Truth)** 원칙을 강화. 데이터의 출처(Origin)를 시스템 데이터(Dictionary)에 명시하고, 마트에서의 수정을 금지하는 **Read-Only 권한**을 부여.
    *   *결과*: 데이터 신뢰성 회복 및 분석 리포트의 표준화 달성.

**2. 도입 체크리스트 (Real-World Checklist)**

| 구분 | 항목 | 점검 포인트 |
|:---|:---|:---|
| **기술적** | **슬라이싱(Slicing)** | 사용자가 보고 싶은 차원(Dimension) 기준(예: 시간대, 지역, 상품그룹)으로 빠르게 데이터를 쪼개볼 수 있는가? |
| **보안** | **RLS (Row