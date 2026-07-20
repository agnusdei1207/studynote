---
title: "Medallion Architecture"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 152
---
## 핵심 인사이트 (3줄 요약)
1. 메달리온 아키텍처(Medallion Architecture)는 Databricks가 제시한 Delta Lake 기반 <strong>Bronze->Silver->Gold 3계층 데이터 파이프라인 설계 표준</strong>으로, 각 계층이 점진적으로 데이터 품질을 높인다.
2. <strong>AutoLoader</strong>와 <strong>COPY INTO</strong>로 Bronze 계층에 증분 적재하고, MERGE INTO로 Silver의 SCD (Slowly Changing Dimension) 이력을 관리하며, dbt나 Spark SQL로 Gold 집계 테이블을 선언적으로 생성한다.
3. Delta Live Tables (DLT)를 활용하면 Bronze->Silver->Gold 전 파이프라인을 의존성 그래프 기반으로 선언하고, 데이터 품질 기대값(Expectations)을 코드로 관리할 수 있다.

---

## Ⅰ. 개요 및 필요성

Multi-Tier Architecture(009)가 개념적 설계 원칙이라면, 메달리온 아키텍처는 이를 <strong>Delta Lake 위에 구현한 Databricks 공식 패턴</strong>이다. Medallion이라는 이름은 Bronze->Silver->Gold가 올림픽 메달처럼 품질이 높아진다는 비유에서 유래했다.

핵심 차별점은 Delta Lake의 ACID 트랜잭션, 타임 트래블, 스키마 진화 기능을 활용하여 각 계층 간 데이터 이동을 신뢰성 있게 처리한다는 점이다. 기존 Hadoop 기반 레이크에서는 파이프라인 중간 실패 시 오염된 데이터가 남아있어 재처리가 복잡했으나, Delta Lake는 원자적 커밋으로 이 문제를 해결한다.

| 구분 | 개념 | Databricks 구현 |
|:---|:---|:---|
| Bronze | 원시 데이터 보존 | AutoLoader + Delta append-only |
| Silver | 정제·조인·이력 | MERGE INTO + SCD Type 2 |
| Gold | 집계·KPI | Spark SQL + dbt + DLT |
| 오케스트레이션 | 계층 간 의존성 | Databricks Workflows / DLT |

> 📢 **섹션 요약 비유**: 메달리온은 올림픽 선발 과정이다. 지역 예선(Bronze)->전국 선발전(Silver)->국가 대표 확정(Gold) 순으로 점진적으로 검증된 선수(데이터)만 최종 무대에 선다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|              Medallion Architecture (Databricks 구현)             |
+------------------------------------------------------------------+
|                                                                  |
|  +--------------+   AutoLoader / COPY INTO                       |
|  |  원본 소스    | ---------------------------> 🥉 BRONZE           |
|  |  (S3 Raw)   |                              Delta Table        |
|  +--------------+                             - 스키마: 원본 그대로|
|                                               - 파티션: 적재 날짜  |
|                                               - 모드: append-only |
|                                                      |           |
|                              MERGE INTO (upsert)     |           |
|                              + SCD Type 2 변환        |           |
|                                                      v           |
|                                              🥈 SILVER           |
|                                              Delta Table         |
|                                              - 중복 제거          |
|                                              - null 처리          |
|                                              - 비즈니스 키 정의    |
|                                              - 품질 기대값 검사    |
|                                                      |           |
|                              Spark SQL / dbt 집계    |           |
|                                                      v           |
|                                              🥇 GOLD             |
|                                              Delta Table         |
|                                              - 일별/월별 집계     |
|                                              - Star 스키마        |
|                                              - BI 최적화 파티션   |
|                                                      |           |
|                                          [Power BI / Tableau /   |
|                                           Databricks SQL]        |
+------------------------------------------------------------------+
```

<strong>Databricks 구현 도구 매핑</strong>

| 계층 | 핵심 도구 | 명령/기능 |
|:---|:---|:---|
| Bronze 수집 | AutoLoader | `cloudFiles` 소스, 자동 스키마 추론 |
| Bronze 수집 (배치) | COPY INTO | 멱등성 보장 파일 적재 |
| Silver 변환 | MERGE INTO | upsert + SCD Type 2 |
| 품질 검사 | DLT Expectations | `@dlt.expect`, `@dlt.expect_or_drop` |
| Gold 집계 | dbt / Spark SQL | 선언적 SQL 변환 |
| 파이프라인 관리 | Delta Live Tables | 의존성 자동 해결, 재처리 지원 |

> 📢 **섹션 요약 비유**: AutoLoader는 우체통처럼 새 편지가 오면 자동으로 감지해서 Bronze 서랍에 넣어준다. DLT는 편지 분류 시스템으로 Bronze->Silver->Gold 경로를 자동으로 처리한다.

---

## Ⅲ. 비교 및 연결

**AutoLoader vs COPY INTO 비교**

| 항목 | AutoLoader | COPY INTO |
|:---|:---|:---|
| 처리 방식 | 스트리밍 (신규 파일 자동 감지) | 배치 (명시적 실행) |
| 멱등성 | 처리된 파일 자동 추적 | 기본 멱등성 보장 |
| 스케일 | 수백만 파일 처리 가능 | 수천 파일 적합 |
| 스키마 추론 | 자동 (컬럼 추가 시 진화) | 수동 지정 |
| 사용 시점 | 지속적 스트리밍 파이프라인 | 일회성/주기적 배치 |

<strong>DLT (Delta Live Tables) 특징</strong>

- 선언적 파이프라인: `@dlt.table` 데코레이터로 의존성 자동 해결
- 품질 기대값: `@dlt.expect_or_drop("valid_price", "price > 0")` 형태로 품질 규칙 코드화
- 증분 처리 자동화: STREAMING TABLE로 선언 시 AutoLoader 기반 증분 처리 자동 구성
- 변경 데이터 캡처: `APPLY CHANGES INTO`로 CDC 스트림을 SCD 테이블로 변환

> 📢 **섹션 요약 비유**: DLT는 조립 라인 로봇과 같다. 각 공정(Bronze/Silver/Gold)을 담당하는 로봇이 이전 공정 완료 신호를 받으면 자동으로 작동하고, 불량품(품질 기대값 실패)은 자동으로 제거된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>Silver 계층 SCD Type 2 구현 패턴</strong>
```sql
MERGE INTO silver.customers AS target
USING bronze.customers_cdc AS source
ON target.customer_id = source.customer_id
  AND target.is_current = true
WHEN MATCHED AND source.updated_at > target.valid_from THEN
  UPDATE SET is_current = false, valid_to = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, email, valid_from, valid_to, is_current)
  VALUES (source.customer_id, source.name, source.email,
          source.updated_at, '9999-12-31', true)
```

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Medallion과 Multi-Tier 차이 | Medallion = Delta Lake 기반 구현 표준, Multi-Tier = 일반 설계 원칙 |
| AutoLoader 동작 원리 | S3/ADLS 이벤트 알림 구독 -> 신규 파일 자동 감지 -> Delta append |
| DLT Expectations 역할 | 품질 규칙 코드화 -> 위반 시 격리/드롭/경고 중 선택 가능 |
| Gold 파티션 전략 | 쿼리 필터 기준 컬럼(date, region) 파티션 + Z-ORDER 적용 |

> 📢 **섹션 요약 비유**: Medallion Architecture는 IKEA 조립 설명서와 같다. Delta Lake라는 표준 부품과 AutoLoader·DLT라는 전동 드라이버를 써서 누구나 같은 결과물을 만들 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 표준화 | Databricks 사용 조직 간 코드·아키텍처 재사용 |
| 신뢰성 | Delta ACID로 파이프라인 실패 시 오염 없음 |
| 품질 가시성 | DLT Expectations 대시보드로 계층별 품질 지표 실시간 모니터링 |
| 운영 효율 | AutoLoader 자동 스케일링으로 파일 수 증가에도 무중단 운영 |

메달리온 아키텍처는 Databricks 플랫폼의 베스트 프랙티스로 공식화되었으며, 비 Databricks 환경에서도 동일한 원칙을 Apache Spark + Iceberg/Hudi로 구현하는 사례가 늘고 있다. 심화 학습에서는 **AutoLoader vs COPY INTO 차이**, <strong>SCD Type 2 MERGE 패턴</strong>, <strong>DLT Expectations 품질 관리</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: 메달리온은 데이터의 올림픽 선발 시스템이다. 지역(Bronze)에서 전국(Silver)으로, 전국에서 국가 대표(Gold)로 올라가는 각 단계에서 심사(품질 검사)를 통과한 데이터만 최종 무대에 선다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| AutoLoader | Bronze 수집 | `cloudFiles` 기반 자동 증분 적재 |
| COPY INTO | Bronze 배치 수집 | 멱등성 보장 명령 |
| MERGE INTO | Silver 변환 | upsert + SCD Type 2 구현 |
| DLT | 파이프라인 관리 | 의존성 자동 해결, 품질 기대값 |
| SCD Type 2 | 이력 관리 | valid_from/valid_to/is_current 패턴 |
| dbt | Gold 집계 | SQL 선언적 변환 도구 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[원시 데이터 수집 (Raw Ingestion) — 다양한 소스에서 무결 저장]
    |
    v
[브론즈 레이어 (Bronze) — 원시 데이터 그대로 보존]
    |
    v
[실버 레이어 (Silver) — 정제·표준화·중복 제거]
    |
    v
[골드 레이어 (Gold) — 비즈니스 집계·분석용 최종 데이터]
    |
    v
[레이크하우스 (Lakehouse) — 메달리온 위에 ACID 트랜잭션 지원]
    |
    v
[데이터 메시 (Data Mesh) — 도메인별 메달리온 자율 관리]
```
메달리온 아키텍처는 원시 데이터의 가치를 브론즈->실버->골드 정제 단계로 점진적으로 높이며, 레이크하우스와 데이터 메시의 데이터 품질 기반을 제공한다.

### 👶 어린이를 위한 3줄 비유 설명
1. 메달리온은 그림 대회의 예선->본선->결선처럼, 데이터가 단계별로 더 좋아지는 여정이에요.
2. AutoLoader는 우편함을 자동으로 확인해서 새 편지가 오면 바로 Bronze 방에 넣어주는 로봇이에요.
3. 각 단계에서 품질 검사(DLT Expectations)를 통과해야만 다음 단계로 올라갈 수 있어요.
