---
title: "Realtime Olap"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 259
---
> **핵심 인사이트**
> 1. 실시간 OLAP(Real-Time OLAP)은 초 단위 이하 지연 시간으로 대용량 이벤트 데이터를 분석하는 시스템 — Hadoop/Hive 기반 배치 분석(시간 단위 지연)의 한계를 극복하고, "지금 이 순간" 수십억 행을 집계·필터링하는 능력이 핵심이다.
> 2. 컬럼형 저장소 + 벡터화 실행 + 사전 집계(Pre-aggregation)의 조합 — ClickHouse는 컬럼형 압축 저장 + SIMD 벡터화로 초당 수억 행 처리, Druid/Pinot은 인제스트 시 사전 집계로 쿼리 시 부하를 최소화하는 전략 차이가 있다.
> 3. 워크로드 특성이 엔진 선택을 결정 — 고빈도 업데이트(UPDATE/DELETE) -> ClickHouse, 이벤트 스트림 실시간 인제스트 + 밀리초 응답 -> Druid/Pinot, 기존 데이터 웨어하우스 대체 -> StarRocks가 각각 강점을 가진다.

---

## Ⅰ. 실시간 OLAP 등장 배경

```
전통 분석 아키텍처의 한계:

ETL 배치 파이프라인:
  이벤트 발생 -> Kafka -> Spark Batch(1시간) -> Hive -> 리포트

  지연: 1~24시간
  문제: "오늘 캠페인 효과를 내일 봄"

Lambda 아키텍처:
  배치 레이어 + 속도 레이어 병행
  복잡도 증가, 두 레이어 데이터 불일치 문제

실시간 OLAP 필요성:
  이벤트 발생 -> [실시간 OLAP 엔진] -> 쿼리 결과
  지연: < 1초

대표 사용 사례:
  광고 기술: 실시간 CTR(클릭률), 노출 집계
  게임: 실시간 DAU, 아이템 구매 현황
  금융: 실시간 거래 모니터링 대시보드
  IoT: 수천 센서 실시간 집계
  전자상거래: 실시간 재고 + 판매 추적

실시간 OLAP 엔진:
  ClickHouse (Yandex, 2016)
  Apache Druid (MetaMarkets, 2012)
  Apache Pinot (LinkedIn, 2013)
  StarRocks (구 DorisDB, 2021)
```

> 📢 **섹션 요약 비유**: 실시간 OLAP = 즉석 성적표 — 시험(이벤트) 끝나고 다음 날 성적(배치 분석) 대신 답안 제출 즉시 점수(실시간 OLAP). 광고, 게임, 금융에서 "지금 바로" 답이 필요!

---

## Ⅱ. ClickHouse

```
ClickHouse (클릭하우스):
  개발: Yandex (러시아 구글)
  목적: Yandex.Metrica 웹 분석
  특징: 컬럼형 DBMS, 고성능 집계

핵심 기술:

1. 컬럼형 저장 (Columnar Storage):
  행: [사용자, 이벤트, 시간, 가격]×10억
  컬럼: 가격 컬럼만 읽어 SUM 계산
  -> 불필요한 컬럼 I/O 없음

  압축률: 일반 대비 10~100배
  LZ4 / ZSTD 알고리즘 적용

2. 벡터화 실행 (Vectorized Execution):
  CPU SIMD 명령어 활용
  256비트 AVX: 한 번에 32개 값 처리

  SUM(price) 10억 행:
  일반: 10억 번 덧셈
  SIMD: 약 3,125만 번 (32배 빠름)

3. 파트 기반 쓰기 (MergeTree):
  쓰기: 작은 파트(Part)로 저장
  백그라운드 머지: 파트 주기적 병합
  (LSM과 유사하지만 OLAP 최적화)

  파티셔닝: 날짜별 파티션
  정렬 키: 자주 필터링하는 컬럼

벤치마크:
  쿼리: 100억 행 GROUP BY
  ClickHouse: ~5초
  Hive: ~300초 (60배 빠름)
  Spark: ~30초 (6배 빠름)

단점:
  UPDATE/DELETE: 비효율 (LSM 구조 특성)
  ACID: 부분적 지원
  JOIN: 큰 테이블 JOIN은 느림

적합 워크로드: 시계열, 로그 분석, 이벤트 스트림
```

> 📢 **섹션 요약 비유**: ClickHouse = 초고속 계산기 — 100억 줄 엑셀에서 특정 컬럼만 뽑아 집계(SIMD). Hive 5분을 5초로. 컬럼만 읽고 CPU 한 번에 32개 처리!

---

## Ⅲ. Apache Druid와 Pinot

```
Apache Druid:
  아키텍처: 마이크로서비스 + Kafka 통합

  핵심 특징:
  1. 사전 집계 (Rollup):
    원본: 초당 100만 이벤트
    집계: 분당 사용자별 이벤트 수로 압축
    저장량: 100배 감소, 쿼리 100배 빠름

  2. 컬럼 사전 처리:
    인덱스: 비트맵 인덱스 자동 생성
    압축: 컬럼별 최적 압축

  3. 실시간 인제스트:
    Kafka -> Druid 실시간 (스트리밍)
    Druid -> S3/HDFS (배치 보완)

  노드 유형:
    Historical: 과거 데이터 쿼리
    MiddleManager: 실시간 인제스트
    Broker: 쿼리 라우팅
    Coordinator: 데이터 분배

  사용사례: Lyft, Netflix, Alibaba

Apache Pinot:
  개발: LinkedIn

  핵심 특징:
  1. 최저 지연 쿼리 (< 10ms):
    스타 트리 인덱스 (Star-Tree Index)
    자주 쓰는 집계를 미리 계산해 트리 형태로 저장

  2. Upsert 지원:
    실시간 업데이트 가능 (Druid는 어려움)
    사용자 프로필 실시간 업데이트 + 집계

  3. 멀티 스테이지 쿼리 엔진:
    복잡한 JOIN, 서브쿼리 지원

  사용사례: LinkedIn, Uber, Stripe

비교:
  Druid: 대용량 스트리밍, 집계 최적화
  Pinot: 초저지연, Upsert, LinkedIn 타입 집계
  ClickHouse: 복잡 SQL, 대용량 배치+스트리밍 혼합
```

> 📢 **섹션 요약 비유**: Druid = 미리 계산해 두는 주방 — 재료(원본) 사전 손질(Rollup)해서 요리 시간(쿼리) 단축. Pinot = 초고속 패스트푸드 — 메뉴 미리 준비(Star-Tree)로 10ms 내 제공!

---

## Ⅳ. StarRocks

```
StarRocks (스타록스):
  구 DorisDB -> StarRocks
  개발: 중국 빅테크, 2021 오픈소스

  포지셔닝: "통합 분석 플랫폼"
  OLAP + ETL 대체 (Spark 없애기)

핵심 특징:

1. MPP (Massively Parallel Processing):
  쿼리 자동 분산 실행
  각 노드 병렬 처리 후 집계

2. 벡터화 쿼리 엔진:
  ClickHouse와 유사 SIMD 최적화

3. CBO (Cost-Based Optimizer):
  쿼리 플랜 자동 최적화
  JOIN 순서, 인덱스 선택 자동화

4. 스토리지 유형:

  Primary Key 모델:
  Upsert 지원, 실시간 업데이트
  -> 전자상거래 재고 실시간 업데이트

  Aggregate 모델:
  SUM/MAX/MIN 사전 집계
  -> 광고 지표 집계

  Duplicate 모델:
  원본 데이터 그대로 저장
  -> 로그 분석

5. 데이터 레이크 통합:
  S3/HDFS/Iceberg/Delta Lake 직접 쿼리
  (데이터 이동 없이)
  External Catalog 기능

6. 실시간 + 배치:
  Kafka Stream 실시간 인제스트
  S3 배치 로딩 동시 지원

사용사례:
  JD.com, 이마트24, Meituan

성능:
  TPC-H 벤치마크: Spark 대비 5~10배 빠름
  실시간 인제스트 + 즉시 쿼리 가능
```

> 📢 **섹션 요약 비유**: StarRocks = 만능 분석 도구 — 실시간+배치, 데이터레이크+웨어하우스, SQL+스트리밍을 하나로. 여러 도구(Spark+Hive+Druid) 대신 StarRocks 하나!

---

## Ⅴ. 실무 시나리오 — 광고 기술 실시간 분석

```
광고 플랫폼 실시간 OLAP 아키텍처:

요구사항:
  일 이벤트: 500억 (노출+클릭+전환)
  쿼리: "광고주 X의 캠페인별 실시간 CTR"
  지연 목표: < 2초
  데이터 보존: 90일

문제:
  배치(Spark+Hive): 1시간 지연 -> 광고주 불만

기존 아키텍처:
  AdServer -> Kafka -> Spark(1시간) -> Hive -> BI

신규 아키텍처:
  AdServer -> Kafka -> [Druid 실시간] -> 대시보드
                  ↘ [S3 원본 저장] <- Spark 배치

  Druid 설정:
  Rollup: 초->분 집계 (광고주/캠페인/디바이스별)
  보존: 실시간 14일 (핫), S3 76일 (콜드)
  쿼리 패턴: GROUP BY 광고주, 캠페인, 날짜

결과:
  리포트 지연: 1시간 -> 1분 이내
  쿼리 응답: < 2초 (P99)
  스토리지: Rollup으로 원본 대비 95% 감소
  (500억 이벤트/일 -> 2.5억 집계 행/일)

광고주 피드백:
  "실시간 캠페인 최적화 가능해짐"
  "예산 소진 전 저성능 광고 즉시 중단"

비용 절감:
  Spark 클러스터 비용 40% 감소
  (배치 처리 감소)
```

> 📢 **섹션 요약 비유**: 광고 플랫폼 실시간 분석 — 광고 클릭 결과를 1시간 후가 아니라 1분 이내에 확인! Druid Rollup으로 데이터 95% 압축, 광고주는 즉시 최적화. 실시간이 돈!

---

## 📌 관련 개념 맵

```
실시간 OLAP
+-- 엔진
|   +-- ClickHouse (벡터화, 복잡 SQL)
|   +-- Apache Druid (스트리밍, Rollup)
|   +-- Apache Pinot (초저지연, Upsert)
|   +-- StarRocks (통합, 레이크하우스)
+-- 핵심 기술
|   +-- 컬럼형 저장소
|   +-- 벡터화 실행 (SIMD)
|   +-- 사전 집계 (Rollup)
|   +-- 비트맵 인덱스
+-- 비교 기준
    +-- 지연 시간
    +-- UPDATE 지원
    +-- 스트리밍 통합
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Dremel (Google, 2010)]
컬럼형 쿼리 엔진
실시간 OLAP 선구자
      |
      v
[Apache Druid (2012)]
실시간 이벤트 집계
비트맵 인덱스
      |
      v
[ClickHouse (2016)]
벡터화 실행 엔진
초고속 SQL OLAP
      |
      v
[Apache Pinot (2018 오픈소스)]
초저지연 OLAP
Star-Tree 인덱스
      |
      v
[StarRocks, DuckDB (2021~)]
레이크하우스 통합 OLAP
임베디드/클라우드 실시간 분석
      |
      v
[현재: AI 통합 OLAP]
벡터 임베딩 통합
AI 자연어 쿼리
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 실시간 OLAP = 즉석 성적표 — 시험 끝나고 다음 날 성적 대신 즉시 결과! 광고, 게임, 금융에서 "지금 바로" 100억 개 계산!
2. ClickHouse = 초고속 집계기 — 가격 컬럼만 뽑아(컬럼형) CPU 32개씩 더하기(SIMD). 100억 행도 5초!
3. Druid Rollup = 미리 손질된 재료 — 500억 이벤트를 인제스트 시 2.5억 집계로 압축. 쿼리 시 가볍게 바로 답변!
