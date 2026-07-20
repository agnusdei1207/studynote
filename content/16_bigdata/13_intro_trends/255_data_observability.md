---
title: "Data Observability"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 255
---
> **핵심 인사이트**
> 1. 데이터 옵저버빌리티(Data Observability)는 파이프라인을 통해 흐르는 데이터의 상태를 실시간으로 감지·모니터링하는 능력으로 — 신선도(Freshness), 분포(Distribution), 볼륨(Volume), 스키마(Schema), 계보(Lineage) 5대 기둥으로 구성되며, 데이터 품질 이슈가 비즈니스에 도달하기 전에 사전 탐지한다.
> 2. 데이터 다운타임(Data Downtime)은 데이터 파이프라인 오류나 품질 저하로 분석/ML 모델이 오염된 데이터를 사용하게 되는 상태를 말하며 — 조직의 79%가 경험하지만 평균 발견 시간이 9시간 이상이라는 연구 결과는, 사후 탐지보다 실시간 옵저버빌리티 체계가 필수임을 보여준다.
> 3. Monte Carlo(오픈소스 아님, SaaS), Great Expectations(오픈소스), Soda Core(오픈소스)는 데이터 옵저버빌리티 도구의 대표 주자이며 — DataOps/MLOps 환경에서 데이터 계약(Data Contract)과 결합될 때 데이터 품질 SLA(Service Level Agreement)를 코드로 관리하는 "데이터 신뢰성 엔지니어링"으로 발전한다.

---

## Ⅰ. 데이터 옵저버빌리티 개념

```
데이터 옵저버빌리티 (Data Observability):

정의:
  데이터 파이프라인 내 데이터의 상태를 지속적으로
  모니터링·감지·진단하는 능력

배경:
  소프트웨어 옵저버빌리티 -> 데이터로 확장
  소프트웨어: 로그/메트릭/트레이스 -> MTTD(탐지), MTTR(복구)
  데이터: 품질 로그/메트릭/계보 -> 데이터 다운타임 최소화

데이터 다운타임 (Data Downtime):
  데이터 파이프라인 이슈로 데이터가 부정확/불완전/미사용
  평균 발견 시간: 9.1시간 (Monte Carlo 2022 연구)
  영향: 잘못된 ML 예측, 대시보드 오류, 비즈니스 결정 오류

  예시:
    ETL 파이프라인 오류 -> NULL 레코드 유입 -> KPI 대시보드 이상
    분석가가 오후에 발견 -> 오전 의사결정 이미 오염

5대 기둥 (Five Pillars):
  1. 신선도 (Freshness): 데이터가 최신인가?
  2. 분포 (Distribution): 값의 분포가 정상 범위인가?
  3. 볼륨 (Volume): 레코드 수가 예상 범위인가?
  4. 스키마 (Schema): 컬럼 구조가 변경되지 않았는가?
  5. 계보 (Lineage): 이 데이터는 어디서 왔는가?
```

> 📢 **섹션 요약 비유**: 데이터 옵저버빌리티는 데이터 건강검진 — 혈압(볼륨), 체온(신선도), 혈액 성분(분포), 신분증(스키마), 가족력(계보)을 매시간 자동 체크하는 데이터 건강 모니터링.

---

## Ⅱ. 5대 기둥 상세

```
5대 기둥 상세:

1. 신선도 (Freshness):
   마지막 업데이트 시간 모니터링

   모니터링 지표:
   - 테이블 마지막 업데이트 시간
   - 예상 업데이트 주기 대비 지연
   - NULL 비율의 시간적 변화

   경보 예시:
   - "orders 테이블 업데이트가 4시간 없음 (기대: 1시간)"

2. 분포 (Distribution):
   값의 통계적 분포 모니터링

   모니터링 지표:
   - Min/Max 범위
   - 평균/중앙값/표준편차
   - NULL/0 비율
   - 카테고리 값 분포 (새 카테고리 등장)

   경보 예시:
   - "price 컬럼 평균이 어제 대비 50% 급감"
   - "country 컬럼에 새 값 'ZZ' 등장"

3. 볼륨 (Volume):
   데이터 양 모니터링

   모니터링 지표:
   - 일별/시간별 레코드 수
   - 테이블 크기 증가율
   - 배치 처리 레코드 수 편차

   경보 예시:
   - "오늘 주문 레코드 2만건 (어제: 10만건) — 80% 감소"

4. 스키마 (Schema):
   데이터 구조 변경 모니터링

   모니터링 지표:
   - 컬럼 추가/삭제/이름 변경
   - 데이터 타입 변경
   - NOT NULL 제약 변경

   경보 예시:
   - "users 테이블 email 컬럼 삭제됨"
   - "amount 컬럼 type: INT -> VARCHAR 변경"

5. 계보 (Lineage):
   데이터 흐름 추적

   기능:
   - 데이터 소스 -> 변환 -> 최종 소비 경로 시각화
   - 이슈 발생 시 영향 범위 자동 파악
   - 근본 원인 분석 (Root Cause Analysis)

   계보 예시:
   raw_orders (S3) -> ETL (Spark) -> orders_dw (Redshift)
   -> dashboard (Tableau) -> kpi_report (PDF)

   이슈: raw_orders 스키마 변경
   -> 계보 추적: Tableau 대시보드까지 영향 자동 알림
```

> 📢 **섹션 요약 비유**: 5대 기둥은 데이터 상태 검침표 — 신선도=유통기한, 분포=영양성분, 볼륨=무게, 스키마=원재료, 계보=원산지. 5가지 모두 정상이면 "데이터 안전 확인!"

---

## Ⅲ. 도구 및 플랫폼

```
데이터 옵저버빌리티 도구:

1. Monte Carlo (상용 SaaS):
   자동 ML 기반 이상 탐지
   데이터 계보 자동 수집
   Slack 통합 알림
   지원: Snowflake, BigQuery, Redshift, dbt
   가격: 기업용 구독

2. Great Expectations (오픈소스):
   Python 기반 데이터 검증 라이브러리

   핵심 개념:
   - Expectation: 데이터 품질 규칙
   - Suite: 규칙 모음
   - Checkpoint: 파이프라인 내 검증 실행 지점

   예시:
   expect_column_values_to_not_be_null("user_id")
   expect_column_values_to_be_between("age", 0, 120)
   expect_table_row_count_to_be_between(1000, 1000000)

   실행 결과: HTML 리포트 + JSON 결과

3. Soda Core (오픈소스):
   YAML 기반 데이터 품질 체크

   checks.yml:
   checks for orders:
     - row_count > 0
     - missing_count(order_id) = 0
     - duplicate_count(order_id) = 0
     - avg(amount) between 10 and 1000

   실행: soda scan -d prod_db -c checks.yml

4. Apache Atlas:
   데이터 계보 전문 (Hadoop 생태계)
   엔터프라이즈 메타데이터 관리

5. dbt (data build tool) + 테스트:
   dbt test: YAML 기반 데이터 테스트
   dbt source freshness: 신선도 체크 내장

   schema.yml:
   models:
     - name: orders
       tests:
         - not_null: {column_name: order_id}
         - unique: {column_name: order_id}
```

> 📢 **섹션 요약 비유**: 도구 선택은 용도에 맞게 — Monte Carlo는 자동 의사, Great Expectations는 직접 쓰는 검진표, dbt test는 코드 안에 넣는 내장 체온계. 규모에 맞게 선택!

---

## Ⅳ. 데이터 계약

```
데이터 계약 (Data Contract):

정의:
  데이터 생산자(Producer)와 소비자(Consumer) 간의
  스키마, 품질, SLA를 명시한 공식 계약

  = API 계약의 데이터 버전

구조:
  dataContractSpecification: 0.9.3
  id: orders-v1
  info:
    title: Orders Data Contract
    version: 1.0.0
    owner: data-platform-team

  models:
    orders:
      fields:
        order_id: {type: string, required: true}
        amount: {type: number, minimum: 0}
        created_at: {type: timestamp}

  quality:
    - type: not_null
      field: order_id
    - type: custom
      engine: great-expectations
      expectation: expect_column_values_to_be_between

  SLA:
    freshness: 1 hour
    availability: 99.9%

데이터 계약 + 옵저버빌리티 통합:
  계약 위반 -> 자동 알림 -> 담당팀 티켓 생성
  계약 이력 -> 변경 추적 -> 영향 분석

이점:
  생산자: 명확한 품질 의무
  소비자: 신뢰할 수 있는 데이터 보장
  조직: 데이터 신뢰성 SLA 가시화
```

> 📢 **섹션 요약 비유**: 데이터 계약은 데이터 배달 약속 — "이 데이터는 매 시간 갱신하고, NULL은 없고, 레코드 수는 최소 1만건". 공급자가 약속을 어기면 자동으로 알람이 울려요.

---

## Ⅴ. 실무 시나리오 — ML 모델 데이터 모니터링

```
E커머스 추천 ML 모델 데이터 파이프라인 모니터링:

파이프라인:
  원본 이벤트 (Kafka)
    -> ETL (Spark Streaming)
    -> 피처 스토어 (Redis + Snowflake)
    -> ML 모델 추론 서버
    -> 추천 결과 API

문제 상황 (데이터 다운타임 발생):
  오전 9:00 — Spark ETL 이슈 발생
    user_id 컬럼 일부 NULL 유입 (스키마 변경 버그)

  오전 9:00 ~ 오후 2:00 (5시간):
    ML 모델: NULL user_id 데이터 학습
    추천 API: 이상 추천 결과 반환

  오후 2:00:
    분석가가 KPI 대시보드 이상 발견 -> 조사 시작

  오후 4:00 (7시간 후):
    근본 원인 발견, 파이프라인 수정

옵저버빌리티 도입 후:
  Great Expectations 적용:
    expect_column_values_to_not_be_null("user_id")
    expect_column_values_to_be_between("session_duration", 0, 3600)

  Soda 신선도 모니터링:
    피처 스토어 마지막 업데이트 체크 (1분 주기)

  알림 흐름:
  오전 9:02 — NULL 비율 0.01% -> 경보 트리거 (기준: 0.001%)
  오전 9:03 — Slack 알림: "user_id NULL 이상 탐지 in feature_store"
  오전 9:05 — ML 모델 서빙 자동 일시 중단 (피처 품질 SLA 위반)
  오전 9:10 — 엔지니어 원인 파악
  오전 9:30 — 파이프라인 수정 및 재시작

결과:
  데이터 다운타임: 7시간 -> 30분
  비즈니스 영향: 5시간 오염 -> 30분 이내 격리
  ROI: 추천 수익 손실 방지 (약 $10만)
```

> 📢 **섹션 요약 비유**: ML 파이프라인 옵저버빌리티는 자동 식품 검사 — 오염된 재료(NULL 데이터)가 요리(ML 모델)에 들어가기 전에 입구에서 자동 탐지. 손님(사용자)에게 나쁜 음식이 가지 않도록!

---

## 📌 관련 개념 맵

```
데이터 옵저버빌리티
+-- 5대 기둥
|   +-- 신선도 (Freshness)
|   +-- 분포 (Distribution)
|   +-- 볼륨 (Volume)
|   +-- 스키마 (Schema)
|   +-- 계보 (Lineage)
+-- 도구
|   +-- Monte Carlo (SaaS)
|   +-- Great Expectations (오픈소스)
|   +-- Soda Core (오픈소스)
|   +-- dbt test
+-- 관련 개념
|   +-- 데이터 다운타임
|   +-- 데이터 계약 (Data Contract)
|   +-- DataOps, MLOps
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[데이터 품질 관리 (1990s~)]
수동 데이터 검증
ETL 품질 체크
      |
      v
[소프트웨어 옵저버빌리티 (2010s)]
로그/메트릭/트레이스 3요소
MTTD, MTTR 최소화
      |
      v
[데이터 옵저버빌리티 탄생 (2018~)]
Barr Moses (Monte Carlo) 개념 정립
5대 기둥 프레임워크
      |
      v
[도구 생태계 성숙 (2020~)]
Great Expectations, Soda
Monte Carlo 상용 SaaS
dbt test 통합
      |
      v
[현재: 데이터 계약 + 옵저버빌리티]
Data Contract 표준화
MLOps 파이프라인 통합
자동 ML 이상 탐지
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 데이터 옵저버빌리티는 데이터 건강검진 — 혈압(볼륨), 체온(신선도), 혈액 성분(분포)을 매 시간 자동으로 재주는 의료 시스템!
2. 5대 기둥 — 신선도·분포·볼륨·스키마·계보를 항상 체크하면 "데이터가 어디서 와서 어떤 상태인지" 다 알 수 있어요.
3. 이상이 생기면 즉시 알람 — 오염된 데이터가 ML 모델이나 대시보드로 가기 전에 자동으로 잡아줘요!
