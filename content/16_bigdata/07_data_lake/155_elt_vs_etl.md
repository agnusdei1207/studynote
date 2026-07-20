---
title: "Elt Vs Etl"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 155
---
## 핵심 인사이트 (3줄 요약)
1. ETL (Extract, Transform, Load)은 변환 후 적재하는 전통 방식으로 스토리지 비용이 비쌌던 온프레미스 DW 환경에 최적화되었으나, 클라우드 시대에는 <strong>먼저 적재하고 나중에 변환하는 ELT (Extract, Load, Transform)</strong>가 표준으로 전환되었다.
2. dbt (data build tool)는 ELT 패러다임의 핵심 도구로, 데이터 웨어하우스·레이크하우스 내부에서 SQL로 선언적 변환을 수행하며 테스트·문서화·리니지를 자동 관리한다.
3. ELT는 <strong>원시 데이터(Raw) 보존</strong>, **반복적 변환 가능**, <strong>타임 트래블 기반 소급 재처리</strong>를 가능하게 하여 데이터 파이프라인의 유연성과 감사 추적성을 극대화한다.

---

## Ⅰ. 개요 및 필요성

1990~2010년대 온프레미스 데이터 웨어하우스(Oracle, Teradata) 환경에서는 스토리지가 고가였고 컴퓨팅 자원도 제한적이었다. ETL은 이 제약 안에서 필요한 데이터만 정제·압축하여 DW에 적재하는 최적 방식이었다.

클라우드 시대(2010년 이후)에는 S3/ADLS 스토리지 비용이 온프레미스 대비 10~100분의 1 수준으로 하락하고, Spark/BigQuery/Snowflake의 분산 컴퓨팅이 변환 비용을 정규화했다. 이 변화가 ELT 패러다임으로의 전환을 이끌었다.

| 비교 항목 | ETL | ELT |
|:---|:---|:---|
| 변환 위치 | 스테이징 서버 (외부) | DW/레이크하우스 내부 |
| 원시 데이터 보존 | 없음 (변환 후 버림) | 있음 (Raw 계층 보존) |
| 스토리지 사용 | 최소화 (정제 후 적재) | 최대 (Raw + 변환 결과) |
| 재처리 유연성 | 낮음 (원본 없음) | 높음 (Raw에서 재변환) |
| 적합 환경 | 온프레미스 DW | 클라우드 DW / 레이크하우스 |
| 대표 도구 | Informatica, SSIS, Talend | dbt, Spark SQL, Dataflow |

> 📢 **섹션 요약 비유**: ETL은 식재료를 요리해서만 냉장고에 넣는 방식이고, ELT는 식재료를 그대로 냉장고에 넣고 필요할 때 꺼내서 요리하는 방식이다. 냉장고(스토리지)가 저렴해지면서 후자가 유리해졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------------------------+
|                   ETL vs ELT 비교                               |
+----------------------------------------------------------------+
|                                                                |
|  【ETL 흐름】                                                   |
|                                                                |
|  [소스] --Extract---> [스테이징 서버]                            |
|                      Transform (정제·집계)                      |
|                           |                                    |
|                           +--Load---> [DW] ---> [BI 도구]        |
|                                                                |
|  【ELT 흐름】                                                   |
|                                                                |
|  [소스] --Extract---> [레이크하우스 / 클라우드 DW]               |
|                      (Bronze: Raw 적재)                         |
|                           |                                    |
|                    Transform (dbt / Spark SQL)                  |
|                    Silver: 정제  Gold: 집계                     |
|                           |                                    |
|                           +---> [BI / ML 도구]                  |
|                                                                |
+----------------------------------------------------------------+
```

<strong>dbt (data build tool) 핵심 기능</strong>

| 기능 | 설명 | 장점 |
|:---|:---|:---|
| Model | SQL SELECT로 변환 정의 | 선언적, 재사용 가능 |
| Test | `not_null`, `unique`, `accepted_values` | 변환 결과 자동 품질 검사 |
| Documentation | `description` 필드로 컬럼 문서화 | 자동 데이터 카탈로그 생성 |
| Lineage Graph | 모델 간 의존성 자동 시각화 | 영향 분석 즉시 파악 |
| Materialization | Table / View / Incremental / Ephemeral | 성능·비용 트레이드오프 선택 |
| Seed | CSV로 정적 참조 데이터 관리 | 코드와 데이터 함께 버전 관리 |

**dbt Incremental 모델 패턴**
```text
-- models/silver/orders_cleaned.sql
-- dbt Jinja 매크로 사용
-- { { config(materialized='incremental',
--           unique_key='order_id',
--           on_schema_change='sync_all_columns') } }

SELECT
    order_id,
    customer_id,
    amount,
    created_at
FROM source('bronze', 'orders_raw')
WHERE status != 'cancelled'
-- incremental 조건: 마지막 실행 이후 데이터만 처리
-- AND created_at > (SELECT MAX(created_at) FROM this_model)
```

> 📢 **섹션 요약 비유**: dbt는 요리 레시피 북이다. 각 요리(모델)의 재료(소스)와 조리법(SQL)이 정해져 있고, 완성된 요리(결과 테이블)가 예상대로 나왔는지 검사(test)하는 과정도 포함된다.

---

## Ⅲ. 비교 및 연결

<strong>ELT 도구 비교</strong>

| 도구 | 실행 위치 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| dbt Core | DW/레이크하우스 내부 | 오픈소스, SQL 선언적 | Snowflake, BigQuery, Databricks |
| dbt Cloud | 관리형 SaaS | IDE + 스케줄러 + 협업 | 팀 규모 조직 |
| Spark SQL | 레이크하우스 | Python/Scala 병행 | 대규모 배치 변환 |
| Dataflow | GCP 관리형 | Apache Beam 기반 | GCP 생태계 |
| Glue | AWS 관리형 | Spark 기반, S3 통합 | AWS 생태계 |

**연관 개념 연결**

- <strong>Medallion Architecture</strong>: ELT의 Bronze->Silver->Gold가 Medallion 계층과 완벽히 매핑
- <strong>Data Product</strong>: dbt 모델이 Gold 계층 데이터 제품의 변환 로직을 담당
- <strong>Data Lineage</strong>: dbt가 자동으로 리니지 그래프를 생성하여 Unity Catalog와 연계

> 📢 **섹션 요약 비유**: ETL은 택배 물건을 포장해서 배송하는 방식이고, ELT는 원재료를 창고에 다 넣어두고 주문이 오면 그때 포장하는 방식이다. 창고(스토리지) 비용이 싸지면서 후자가 더 효율적이 됐다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>ELT 전환 체크리스트</strong>
- [ ] 원시 데이터를 Bronze 계층에 보존하는 파이프라인 설계
- [ ] dbt 프로젝트 초기화 및 소스 등록 (`dbt source freshness` 설정)
- [ ] Silver 모델: `materialized='incremental'` + `unique_key` 설정
- [ ] Gold 모델: `materialized='table'` + 파티션 설정
- [ ] `dbt test` 실행 CI/CD 파이프라인 통합

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| ETL -> ELT 전환 이유 | 클라우드 스토리지 저비용화, 분산 컴퓨팅 확장성 |
| dbt의 역할 | DW 내부 SQL 선언적 변환 + 테스트 + 리니지 자동화 |
| Incremental 모델 장점 | 전체 재처리 없이 새 데이터만 변환 -> 비용·시간 절감 |
| ELT 한계 | 원시 데이터 보존으로 스토리지 비용 증가, 민감 데이터 보안 관리 필요 |

> 📢 **섹션 요약 비유**: ELT 도입은 즉석 조리 냉장고를 도입하는 것이다. 모든 식재료를 신선하게 보관하고(Bronze), 필요할 때 빠르게 조리(dbt 변환)하여 서빙(Gold)한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 재처리 유연성 | Raw 보존으로 언제든 새 로직으로 소급 재처리 가능 |
| 운영 단순화 | 스테이징 서버 제거, DW 내부에서 모든 변환 처리 |
| 품질 가시성 | dbt test로 변환 결과 품질 자동 검증 |
| 협업 향상 | dbt 모델 = SQL 코드 -> Git 버전 관리 + 코드 리뷰 |

ETL에서 ELT로의 패러다임 전환은 클라우드 빅데이터 인프라 확산과 함께 이미 완료된 흐름이다. dbt는 현재 데이터 팀 표준 도구로 자리 잡았으며, Databricks·Snowflake·BigQuery 모두 네이티브 dbt 통합을 지원한다. 심화 학습에서는 <strong>ETL vs ELT 전환 이유</strong>, **dbt 핵심 기능**, <strong>Incremental 모델 동작 원리</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: ELT 시대는 사진 현상 방식의 변화와 같다. 필름 사진(ETL)은 찍자마자 현상해야 했지만, 디지털 사진(ELT)은 RAW 파일로 보관하고 필요할 때 다양한 방식으로 편집할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| dbt | ELT 핵심 도구 | SQL 선언적 변환·테스트·리니지 |
| Incremental 모델 | dbt 성능 최적화 | 신규 데이터만 처리 패턴 |
| Bronze 계층 | ELT 전제 조건 | Raw 데이터 영구 보존 |
| Data Lineage | 자동화 산출물 | dbt가 생성하는 모델 의존성 그래프 |
| Medallion Architecture | 연관 패턴 | ELT 흐름 = Bronze->Silver->Gold |
| Schema-on-Read | ELT 특성 | 적재 시 스키마 강제 않음 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[ETL (Extract-Transform-Load) — 소스에서 추출 후 변환, 타겟 DW에 적재]
    |
    v
[데이터 웨어하우스 (DW) — 정제된 구조적 데이터 중앙 저장소, ETL 전제]
    |
    v
[ELT (Extract-Load-Transform) — 원시 데이터 먼저 적재, 클라우드 DW에서 변환]
    |
    v
[데이터 레이크 (Data Lake) — 원시 데이터 무제한 적재, ELT 패러다임과 친화적]
    |
    v
[레이크하우스 (Lakehouse) — Delta Lake·Iceberg 기반 ELT + ACID 트랜잭션 통합]
```

이 흐름은 온프레미스 DW를 위한 ETL 패러다임이 클라우드 규모에서 ELT로 전환되고, 데이터 레이크하우스 아키텍처로 통합·발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. ETL은 재료를 사오자마자 다 손질해서 냉장고에 넣는 방식이고, ELT는 재료 그대로 일단 냉장고에 넣고 필요할 때 꺼내서 손질하는 방식이에요.
2. 냉장고(저장공간)가 저렴해지면서 미리 다 손질하지 않아도 되니 ELT 방식이 더 편리해졌어요.
3. dbt는 냉장고 안 재료를 어떻게 요리할지 레시피 북이에요. 레시피(SQL)를 코드로 기록해두면 언제나 같은 요리가 나와요.
