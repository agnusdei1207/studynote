---
title: "Time Series Interpolation Rollup Dashboard"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 187
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시계열 DB(Time-Series Database)는 타임스탬프를 기본 인덱스로 삼아 <strong>시간 순서 데이터의 고속 삽입·압축·집계</strong>에 특화된 스토리지로, 일반 RDBMS 대비 100배 이상의 성능 우위를 제공한다.
> 2. **가치**: 보간법(Interpolation)으로 결측 구간을 채우고 롤업(Rollup)으로 고해상도 데이터를 저해상도로 집계하여, <strong>Grafana 같은 대시보드가 어떤 시간 범위도 일관된 응답 속도로 시각화</strong>할 수 있게 한다.
> 3. **판단 포인트**: 카디널리티 폭발(Cardinality Explosion)—태그 조합 수의 급격한 증가—이 시계열 DB 성능 저하의 주범이며, 태그 설계 시 고카디널리티 값(userId, IP 등)을 태그가 아닌 필드(Field)로 분리하는 것이 학습 정리의 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 시계열 데이터의 특성

```
시계열 데이터 예시:
  2026-04-21T10:00:00  CPU=45%   메모리=60%  서버A
  2026-04-21T10:00:10  CPU=47%   메모리=61%  서버A
  2026-04-21T10:00:20  CPU=43%   메모리=59%  서버A
  ...
  초당 100개 메트릭 × 서버 1,000대 = 초당 100,000개 포인트

특성:
  1. 시간 순서성: 삽입은 항상 최신 시간으로 (추가 전용)
  2. 고빈도 쓰기: 초당 수백만 포인트
  3. 범위 쿼리: "최근 1시간" 같은 시간 범위 기반
  4. 집계 쿼리: 평균·최대·최소 등 집계 위주
  5. 데이터 감소: 오래된 데이터는 낮은 해상도로 보관
```

### 1.2 주요 시계열 DB 비교

| DB | 개발사 | 특징 | 쿼리 언어 |
|:---|:---|:---|:---|
| InfluxDB | InfluxData | 강력한 RP/CQ 기능 | InfluxQL / Flux |
| TimescaleDB | Timescale | PostgreSQL 확장 | SQL (표준 SQL 지원) |
| OpenTSDB | StumbleUpon | HBase 기반, 대규모 | HTTP API |
| Prometheus | CNCF | 풀 기반, 쿠버네티스 표준 | PromQL |
| ClickHouse | Yandex | 컬럼형, 초고성능 분석 | SQL |
| VictoriaMetrics | VM | Prometheus 호환, 효율적 | MetricsQL |

📢 **섹션 요약 비유**: 시계열 DB는 마치 의사의 심전도 기록지다. 시간 순서대로 심박수가 찍히고, "오전 10시부터 11시 사이 평균 심박수"를 순식간에 계산할 수 있어야 한다. 일반 메모장(RDBMS)에 심전도를 적으면 찾는 데 너무 오래 걸린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 시계열 DB 내부 구조 (InfluxDB 기준)

```
InfluxDB 데이터 모델:

  측정(Measurement) = 테이블 유사
  +------------------------------------------------------+
  |  Measurement: cpu_usage                              |
  +--------------+---------------------------------------+
  |  태그(Tags)   |  host="server01", region="ap-east"    |
  |  (인덱스 O)   |  -> 이 조합이 시리즈(Series)를 식별     |
  +--------------+---------------------------------------+
  |  필드(Fields) |  value=45.2, user=32.1, system=13.1   |
  |  (인덱스 X)   |  -> 실제 측정값 (인덱스 없음)           |
  +--------------+---------------------------------------+
  |  타임스탬프   |  2026-04-21T10:00:00Z                 |
  +--------------+---------------------------------------+

⚠️ 카디널리티 = 고유 시리즈 수 = 태그 조합 수
   host(1000대) × region(10) = 10,000 시리즈 -> 관리 가능
   host(1000대) × userId(100만) = 10억 시리즈 -> 폭발!
```

### 2.2 보간법 (Interpolation) 유형

```
결측값 처리 시나리오:
시간:  10:00  10:10  10:20  10:30  10:40
CPU:   45     ?      ?      50     ?

1. LOCF (Last Observation Carried Forward):
   -> 45  45  45  50  50
   장점: 단순, 급격한 변화 없음
   단점: 실제 변화 반영 불가

2. 선형 보간 (Linear Interpolation):
   -> 45  46.7  48.3  50  50 (마지막은 LOCF)
   장점: 완만한 변화에 자연스러움
   단점: 급격한 변화 시 부정확

3. 스플라인 보간 (Spline Interpolation):
   -> 3차 다항식으로 더 부드러운 곡선
   장점: 자연스러운 곡선
   단점: 진동(Runge's phenomenon) 위험

4. NOCB (Next Observation Carried Backward):
   -> 45  50  50  50  (다음 값으로 채움)
   적합: 이벤트 기반 데이터

5. 평균 보간:
   -> (45+50)/2 = 47.5로 채움
   적합: 간단한 갭 채움
```

### 2.3 롤업 (Rollup) / 연속 집계 아키텍처

```
+----------------------------------------------------------+
|               데이터 롤업 계층 구조                         |
|                                                           |
|  원시 데이터 (1초 해상도, 30일 보관)                        |
|  2026-04-21T10:00:00  CPU=45                             |
|  2026-04-21T10:00:01  CPU=46                             |
|  ...                                                     |
|       v 롤업 (1분 집계, AVG/MAX/MIN)                      |
|  1분 집계 (1분 해상도, 6개월 보관)                          |
|  2026-04-21T10:00:00  AVG=45.2  MAX=67  MIN=43           |
|       v 롤업 (1시간 집계)                                  |
|  1시간 집계 (1시간 해상도, 2년 보관)                        |
|  2026-04-21T10:00:00  AVG=48.1  MAX=92  MIN=31           |
|       v 롤업 (1일 집계)                                   |
|  1일 집계 (1일 해상도, 10년 보관)                          |
|  2026-04-21        AVG=52.3  MAX=98  MIN=20              |
|                                                           |
|  저장 절감: 1초 × 86,400초/일 -> 1일 1개 = 86,400배 압축  |
+----------------------------------------------------------+
```

### 2.4 TimescaleDB 연속 집계 (Continuous Aggregates)

```sql
-- TimescaleDB 연속 집계 뷰 생성
CREATE MATERIALIZED VIEW cpu_hourly_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    host,
    AVG(cpu_usage) AS avg_cpu,
    MAX(cpu_usage) AS max_cpu,
    MIN(cpu_usage) AS min_cpu,
    COUNT(*) AS data_points
FROM cpu_metrics
GROUP BY bucket, host;

-- 자동 갱신 정책 (1시간마다 최근 2시간 재계산)
SELECT add_continuous_aggregate_policy(
    'cpu_hourly_avg',
    start_offset => INTERVAL '2 hours',
    end_offset   => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);
```

📢 **섹션 요약 비유**: 롤업은 마치 1초마다 찍은 수백만 장의 사진을 1분 단위로 대표 사진 하나로 줄이는 것이다. 오래된 사진일수록 더 많이 압축해서 저장 공간을 아끼면서도 "그 시간대의 대략적인 모습"은 유지한다.

---

## Ⅲ. 비교 및 연결

### 3.1 카디널리티 폭발 (Cardinality Explosion) 문제 분석

```
카디널리티 폭발 사례:

  정상 설계:
    태그: host (1,000), region (5), env (3)
    시리즈 수: 1,000 × 5 × 3 = 15,000 -> 관리 가능

  잘못된 설계:
    태그: host, region, env, user_id (1억), request_id (무한대)
    시리즈 수: 1,000 × 5 × 3 × 1억 = 1.5조 -> 메모리 초과!

카디널리티 폭발 증상:
  - 쿼리 속도 급격히 저하
  - 메모리 사용량 급증 (시리즈별 메타데이터)
  - TSM(Time-Structured Merge Tree) 파일 과다 생성
  - InfluxDB: "too many series" 오류

해결책:
  1. 고카디널리티 값 -> 태그 -> 필드(Field)로 이동
  2. 태그 수 최소화 (5개 이하 권장)
  3. 시리즈 카디널리티 제한 정책 설정
  4. 데이터 모델 재설계 (측정 분리)
```

### 3.2 Prometheus vs InfluxDB vs TimescaleDB 비교

| 항목 | Prometheus | InfluxDB | TimescaleDB |
|:---|:---|:---|:---|
| 수집 방식 | 풀(Pull) | 푸시(Push)/풀 | 푸시(Push) |
| 쿼리 언어 | PromQL | InfluxQL/Flux | SQL |
| 보관 정책 | 기본 15일 | 유연한 RP | 청크 기반 |
| 롤업 | Recording Rules | CQ (Continuous Query) | Continuous Aggregates |
| 쿠버네티스 연계 | 표준 (CNCF) | 별도 설정 | 별도 설정 |
| 장기 보관 | 외부 연계 필요 (Thanos) | 내장 | PostgreSQL 기반 |

### 3.3 Grafana 대시보드 연동 아키텍처

```
+----------------------------------------------------------+
|              Grafana 통합 모니터링 스택                     |
|                                                           |
|  메트릭 수집: Prometheus / InfluxDB                        |
|  로그 수집:   Loki / Elasticsearch                        |
|  트레이싱:    Jaeger / Tempo                              |
|                     v                                    |
|               Grafana (시각화)                             |
|  +-------------------------------------------------+    |
|  |  대시보드 패널:                                   |    |
|  |  - 시계열 차트: CPU, 메모리, 네트워크 트렌드       |    |
|  |  - 히트맵: 요청 분포, 지연 분포                   |    |
|  |  - 게이지: 현재 상태 (녹/황/적 신호등)            |    |
|  |  - 테이블: 상위 N개 이슈 서버                     |    |
|  +-------------------------------------------------+    |
|                     v                                    |
|              AlertManager (알림)                          |
|  임계값 초과 -> Slack / PagerDuty / Email 발송             |
+----------------------------------------------------------+
```

📢 **섹션 요약 비유**: Grafana + Prometheus 스택은 마치 비행기 조종석 계기판이다. 수천 개의 센서 데이터를 실시간으로 모아서, 조종사가 한눈에 모든 상태를 볼 수 있게 정리해주고, 이상이 생기면 경고등을 켜준다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 IoT 센서 시계열 파이프라인 설계

```
+----------------------------------------------------------+
|           IoT -> 시계열 DB -> 대시보드 파이프라인             |
|                                                           |
|  센서 레이어                                              |
|  온도·습도·전력 센서 × 10,000개 -> MQTT 브로커              |
|       v                                                  |
|  수집 레이어                                              |
|  Telegraf (InfluxData 에이전트) -> InfluxDB                |
|  - 플러그인: MQTT, Kafka, Modbus, OPC-UA 지원            |
|       v                                                  |
|  처리 레이어                                              |
|  Kapacitor (스트림 처리) 또는 Flux 스크립트               |
|  - 이상값 탐지 (3σ 이상 = 알림)                           |
|  - 보간법 적용 (결측값 처리)                               |
|       v                                                  |
|  시각화 레이어                                            |
|  Grafana -> InfluxDB 데이터소스                           |
|  - 실시간 대시보드 (5초 자동 갱신)                         |
|  - 경보 규칙 (임계값 초과 시 SMS 발송)                    |
+----------------------------------------------------------+
```

### 4.2 데이터 보관 정책 (Retention Policy)

```sql
-- InfluxDB 보관 정책 및 연속 쿼리 예시

-- 1초 데이터: 30일 보관
CREATE RETENTION POLICY "raw_30d" ON "iot_db"
  DURATION 30d REPLICATION 1 DEFAULT;

-- 1분 집계: 1년 보관 (자동 집계)
CREATE RETENTION POLICY "1m_1y" ON "iot_db"
  DURATION 365d REPLICATION 1;

-- 연속 쿼리 (1분마다 실행, 1분 집계 생성)
CREATE CONTINUOUS QUERY "cq_1m" ON "iot_db"
BEGIN
  SELECT mean(temperature) AS temp_mean,
         max(temperature)  AS temp_max
  INTO "1m_1y"."temperature_1m"
  FROM "raw_30d"."temperature_raw"
  GROUP BY time(1m), location
END;
```

### 4.3 학습 정리 핵심 포인트

```
시계열 DB 설계 시 필수 언급:
  ✓ 카디널리티 폭발 방지: 고카디널리티 값 -> 필드(Field)
  ✓ 보간법 선택 기준:
    - 센서 데이터 (완만한 변화) -> 선형 또는 스플라인
    - 이벤트 기반 데이터 -> LOCF
    - 결측 비율 높음 -> 평균 보간 주의
  ✓ 롤업 설계: 원시(초) -> 1분 -> 1시간 -> 1일 계층
  ✓ 보관 정책 (RP) + 연속 쿼리 (CQ) 연계
  ✓ Grafana 대시보드: 변수(Variables)로 동적 필터링
  ✓ AlertManager 경보 체계: PagerDuty/Slack 연동
  ✓ 백필(Backfill): 과거 데이터로 롤업 소급 생성
```

📢 **섹션 요약 비유**: 카디널리티 폭발 방지는 마치 도서관 분류 시스템에서 "책 제목"을 분류 번호로 쓰지 않는 것과 같다. 책 제목은 수백만 가지라 색인이 폭발적으로 커지므로, "분야(컴퓨터)+ 저자 첫 글자"처럼 카디널리티가 낮은 값으로 인덱스를 만들어야 한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 시계열 DB 도입 효과

| 효과 | 정량 지표 |
|:---|:---|
| 쿼리 성능 향상 | RDBMS 대비 100~1,000배 빠른 시계열 쿼리 |
| 저장 효율 | 시계열 특화 압축으로 10~50배 용량 감소 |
| 대시보드 응답성 | 수십억 포인트도 초단위 집계 응답 |
| 이상 탐지 | 실시간 스트림 처리 + 경보로 장애 선제 대응 |

### 5.2 시계열 데이터 생명주기 관리

```
+------------------------------------------------------+
|            시계열 데이터 생명주기                        |
|                                                      |
|  핫(Hot) 저장소: SSD, 최근 30일                       |
|  -> 1초 해상도, 빠른 쓰기/읽기                          |
|       v 롤업 + RP                                    |
|  웜(Warm) 저장소: HDD, 최근 1년                       |
|  -> 1분 해상도, 집계된 통계                             |
|       v 롤업 + RP                                    |
|  콜드(Cold) 저장소: S3/Glacier, 장기 보관              |
|  -> 1시간/1일 해상도, Parquet 변환 저장                 |
|       v 분석 시                                      |
|  레이크하우스 쿼리: Athena/Spark로 과거 분석            |
+------------------------------------------------------+
```

📢 **섹션 요약 비유**: 시계열 데이터 생명주기는 마치 신문 보관과 같다. 이번 주 신문은 책상 위(핫 저장소)에, 지난달 신문은 책장에(웜), 5년 전 신문은 창고에(콜드) 보관하고, 필요할 때만 창고에서 꺼내 열람한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 DB | InfluxDB / TimescaleDB | 시계열 특화 데이터베이스 |
| 결측값 처리 | 보간법 (Interpolation) | 선형, 스플라인, LOCF, NOCB |
| 집계 압축 | 롤업 (Rollup) | 고해상도 -> 저해상도 집계 |
| 자동화 집계 | 연속 집계 (Continuous Aggregates) | 실시간 집계 뷰 자동 갱신 |
| 성능 장애 | 카디널리티 폭발 | 태그 조합 과다로 시리즈 수 폭증 |
| 보관 정책 | RP (Retention Policy) | 기간별 해상도·보관 정책 |
| 시각화 | Grafana + Prometheus | 표준 모니터링 대시보드 스택 |
| 데이터 계층 | 핫/웜/콜드 스토리지 | 데이터 나이별 저장 매체 분리 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>시계열 DB</strong>는 마치 매초마다 체온을 재서 기록하는 의료 기기처럼, 시간 순서대로 쌓이는 데이터를 가장 빠르게 저장하고 "지난 1시간 평균 체온"을 순식간에 계산할 수 있는 특별한 기록장이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS (범용, 시계열 비최적화)
    |
    v
시계열 DB (InfluxDB · TimescaleDB · Prometheus)
    +-► 시간 기반 파티셔닝 · 압축 (Gorilla · Delta-of-Delta)
    +-► 보간법 (Interpolation): 선형 · 스플라인 · LOCF
    +-► 롤업 (Rollup): 5분 -> 1시간 -> 1일 집계
    |
    v
실시간 대시보드 (Grafana · Kibana)
    |
    v
IoT · 모니터링 · 금융 틱 데이터 분석
```
2. <strong>보간법</strong>은 체온계가 잠깐 고장나서 몇 분간 데이터가 없을 때, "아까 36.5도였고 나중에 37도가 됐으니, 그 사이에는 36.7도 정도였겠지"라고 빈 칸을 채우는 방법이에요.
3. <strong>카디널리티 폭발</strong>은 마치 도서관에서 모든 책의 제목을 색인으로 만들면 색인 카드가 책보다 더 많아지는 것처럼, 너무 다양한 태그를 사용하면 데이터베이스의 색인이 폭발적으로 커지는 문제예요.
