---
title: "ELT (Extract, Load, Transform)"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 227
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ELT(Extract, Load, Transform)는 원시 데이터를 먼저 클라우드 DW/레이크에 고속 적재(L)한 후, DW 내부의 강력한 MPP 컴퓨팅으로 데이터를 변환(T)하는 <strong>클라우드 네이티브 데이터 통합 방식</strong>이다.
> 2. **가치**: ETL의 변환 서버 병목을 제거하고, 원시 데이터를 보존하여 <strong>나중에 다른 관점으로 재분석</strong>할 수 있으며, 클라우드 DW의 수평 확장으로 빅데이터 규모에 탄력적 대응이 가능하다.
> 3. **판단 포인트**: dbt(data build tool)가 ELT 패러다임의 Transform 단계를 SQL 기반으로 표준화한 핵심 도구이며, <strong>Snowflake·BigQuery·Redshift + dbt</strong> 조합이 현대 클라우드 데이터 스택의 표준이다.

---

## Ⅰ. 개요 및 필요성

ETL 시대의 가장 큰 병목은 "변환 서버"였다. 아무리 빠르게 추출해도 중간 서버 성능이 한계였다. 클라우드 DW(BigQuery·Snowflake·Redshift)가 MPP(Massively Parallel Processing)로 수백 노드를 병렬 동원할 수 있게 되자, <strong>"왜 비싼 전용 서버에서 변환하지? DW 내부에서 하면 훨씬 빠르잖아"</strong>라는 인식이 생겼다.

```
[ETL 한계]
소스 -> 추출 -> [변환 서버 병목] -> DW 적재
                    ^ 이 병목이 ETL 전체 속도 결정

[ELT 개선]
소스 -> 추출 -> [DW에 원시 적재] -> [DW 내부 MPP 변환]
                                       ^ DW 수평 확장으로 병목 해소
```

ELT가 특히 효과적인 이유:
- 클라우드 DW는 스토리지-컴퓨팅 분리로 변환 시 컴퓨팅만 확장 가능
- 원시 데이터 보존으로 재분석·재처리 가능
- 데이터 엔지니어가 SQL만으로 변환 로직 작성 가능 (dbt)

📢 **섹션 요약 비유**: ELT는 식재료(원시 데이터)를 먼저 대형 주방(DW)으로 가져온 뒤, 수십 명의 요리사(MPP 노드)가 동시에 손질하는 방식이다. 작은 주방(ETL 서버) 한 곳에서 모든 걸 처리하는 ETL보다 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ELT 파이프라인 아키텍처

```
+------------------------------------------------------------+
|                     ELT 파이프라인                          |
|                                                            |
|  소스 시스템   --- Extract ---->  Raw/Staging Schema        |
|  (SaaS API,        (Fivetran,     (원시 테이블 그대로)       |
|   CDC,             Airbyte,                                |
|   플랫파일)         Custom)                                 |
|                                 v dbt Transform            |
|                              Marts Schema                  |
|                              (비즈니스 도메인 모델)           |
|                                 v                         |
|                              BI 도구 / ML 플랫폼             |
+------------------------------------------------------------+
```

### dbt(data build tool) 역할

```
[dbt 핵심 기능]
+--------------------------------------------------+
|              dbt (데이터 변환 프레임워크)             |
|                                                  |
|  .sql 파일  --->  SELECT * FROM raw_orders        |
|               WHERE created_at > '2024-01-01'   |
|               -> 자동으로 DW 내 VIEW/TABLE 생성   |
|                                                  |
|  기능:                                            |
|  ① SQL 기반 변환 로직 버전 관리 (Git)              |
|  ② 데이터 테스트 (NOT NULL, UNIQUE, 참조 무결성)  |
|  ③ 의존성 자동 해결 (DAG 생성)                    |
|  ④ 문서 자동 생성 (컬럼 설명, 계보)               |
|  ⑤ CI/CD 파이프라인 통합                          |
+--------------------------------------------------+
```

### Modern Data Stack 구성

| 계층 | 역할 | 주요 도구 |
|:---|:---|:---|
| **Extract & Load** | 소스 -> DW 원시 적재 | Fivetran, Airbyte, Stitch |
| **Storage** | 클라우드 DW | Snowflake, BigQuery, Redshift |
| **Transform** | DW 내 SQL 변환 | dbt, Dataform |
| <strong>Orchestration</strong> | 파이프라인 스케줄링 | Airflow, Prefect, Dagster |
| **BI & Analytics** | 시각화·분석 | Tableau, Looker, Metabase |
| <strong>Reverse ETL</strong> | DW -> SaaS 도구 역방향 | Census, Hightouch |

📢 **섹션 요약 비유**: dbt는 SQL로 된 레시피 북이다. 어떤 재료(원시 테이블)를 어떻게 조합(JOIN·집계)해 어떤 요리(비즈니스 테이블)를 만드는지 Git으로 관리되는 레시피북이며, 매번 같은 맛을 보장하는 자동화 주방이다.

---

## Ⅲ. 비교 및 연결

### ETL vs ELT 심층 비교

| 비교 항목 | ETL | ELT |
|:---|:---|:---|
| **변환 주체** | 전용 ETL 서버 | 클라우드 DW/레이크 |
| <strong>원시 데이터 보존</strong> | 미보존 (변환 후 적재) | 보존 (원시 테이블 유지) |
| **빅데이터 확장성** | 제한적 | 탁월 (DW MPP 활용) |
| **변환 도구** | Informatica, DataStage | dbt, SQL, Spark |
| <strong>데이터 이동량</strong> | 적음 (정제 후 이동) | 많음 (원시 그대로 이동) |
| <strong>DW 저장 비용</strong> | 낮음 | 높음 (원시+정제 중복) |
| <strong>스키마 유연성</strong> | 낮음 | 높음 (원시 보존) |
| **기술 요건** | ETL 전문가 | SQL 능숙 데이터 엔지니어 |
| **적합 환경** | 온프레미스, 레거시 | 클라우드 DW, 스타트업 |

### Reverse ETL (역방향 ETL)

ELT의 발전으로 등장한 개념으로, DW에서 분석·변환된 데이터를 <strong>운영 SaaS 도구(CRM·이메일·광고 플랫폼)로 역방향 동기화</strong>한다.

```
[Reverse ETL 흐름]
DW (Gold 테이블) ---> Census/Hightouch ---> Salesforce CRM
                                       ---> Marketo (이메일)
                                       ---> Google Ads
"분석 결과를 곧바로 마케팅 실행에 활용"
```

📢 **섹션 요약 비유**: Reverse ETL은 주방에서 완성된 요리(분석 결과)를 배달 앱(CRM·광고 플랫폼)으로 바로 전송하는 것이다. 창고(DW)에만 보관하지 않고, 요리를 손님(비즈니스 팀)에게 실시간으로 서빙한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### dbt 변환 모델 예시

```text
-- models/marts/sales/fact_daily_sales.sql
-- dbt Jinja: config(materialized='table')

WITH orders AS (
    SELECT * FROM stg_orders     -- ref('stg_orders')
    WHERE status = 'completed'
),
products AS (
    SELECT * FROM stg_products   -- ref('stg_products')
),
final AS (
    SELECT
        o.order_date,
        p.category,
        p.brand,
        SUM(o.amount)    AS total_sales,
        COUNT(o.order_id) AS order_count
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY 1, 2, 3
)

SELECT * FROM final
```

```yaml
# models/marts/sales/schema.yml
models:
  - name: fact_daily_sales
    description: "일별 카테고리별 매출 집계"
    columns:
      - name: total_sales
        tests:
          - not_null
      - name: order_count
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

### 실무 도입 단계

```
1단계: Extract & Load 자동화
       Fivetran으로 SaaS 소스 -> Snowflake Raw 스키마 자동 적재

2단계: dbt 변환 계층 구성
       Staging -> Intermediate -> Marts 3단계 모델 구조

3단계: 테스트 및 문서화
       dbt test + dbt docs generate -> 데이터 품질 자동 검증

4단계: 오케스트레이션
       Airflow DAG 또는 dbt Cloud 스케줄러로 일일 배치

5단계: Reverse ETL (선택)
       Census로 Snowflake Gold -> Salesforce 고객 세그먼트 동기화
```

📢 **섹션 요약 비유**: Modern Data Stack은 레고 블록 세트다. Fivetran(Extract+Load), Snowflake(Storage), dbt(Transform), Airflow(Orchestration), Tableau(BI)라는 각각의 블록을 조립하여 데이터 파이프라인을 완성한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **처리 속도 향상** | ETL 변환 서버 병목 제거, DW MPP로 수~수십 배 속도 |
| <strong>원시 데이터 보존</strong> | 재분석·새로운 비즈니스 요건 발생 시 재처리 가능 |
| **민첩성** | SQL 기반 dbt로 변환 로직 빠른 수정 및 배포 |
| **비용 최적화** | ETL 전용 서버 제거, 클라우드 DW 컴퓨팅 온디맨드 |
| <strong>데이터 계보</strong> | dbt 의존성 DAG로 소스~타겟 전체 계보 자동 문서화 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong>DW 비용 증가</strong> | 원시 데이터 보존으로 스토리지 및 컴퓨팅 비용 ^ |
| <strong>데이터 거버넌스</strong> | DW 내 원시 테이블 과잉 -> 정리 정책 필요 |
| **SQL 의존성** | 복잡한 ML 피처, 비정형 처리는 Python/Spark 병행 필요 |
| **실시간 한계** | 기본적으로 배치 지향, 실시간 처리는 스트리밍 파이프라인 별도 |

📢 **섹션 요약 비유**: ELT는 큰 창고(DW)에 재료를 다 쌓아두고 요리하는 방식이다. 창고 공간(DW 비용)은 더 필요하지만, 언제든 다른 레시피(분석 관점)로 요리할 수 있고, 주방(DW MPP)이 크니 한꺼번에 많은 양을 빠르게 처리할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| ETL | ELT의 전신, 변환 위치(외부 서버)가 핵심 차이 |
| dbt (data build tool) | ELT Transform 단계의 표준 SQL 변환 프레임워크 |
| 클라우드 DW | ELT 변환 엔진 역할 담당 (Snowflake, BigQuery) |
| Fivetran/Airbyte | ELT의 Extract+Load 자동화 도구 |
| Apache Airflow | ELT 파이프라인 스케줄링·오케스트레이션 |
| Reverse ETL | DW -> 운영 SaaS 역방향 데이터 동기화 |
| Schema-on-Read | ELT에서 원시 적재 후 변환하는 철학과 연결 |

### 👶 어린이를 위한 3줄 비유 설명
1. ELT는 장난감(데이터)을 일단 큰 방(DW)에 다 가져온 뒤, 방 안에서 여러 명이 함께 정리하는 것이다. 한 명(ETL 서버)이 바깥에서 다 정리하고 들어오는 것보다 훨씬 빠르다.

### 📈 관련 키워드 및 발전 흐름도

```text
ETL: 외부 서버에서 변환 (병목)
    |
    v
ELT: DW/Lake 내부에서 변환 (BigQuery · Snowflake MPP)
    +-► dbt: SQL 기반 변환 오케스트레이션
    +-► Materialized View · CTAS
    |
    v
Reverse ETL: DW -> SaaS 도구로 데이터 역전달
```
2. dbt는 "이 장난감들을 이렇게 분류해라"라는 정리 규칙서(SQL 파일)다. 규칙서를 고치면 다음번에 자동으로 새로운 방식으로 정리된다.
3. 원시 데이터를 보존하는 것은 장난감 설명서를 버리지 않는 것과 같다. 나중에 다른 방법으로 조립(재분석)하고 싶을 때 다시 꺼내볼 수 있다.
