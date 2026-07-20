---
title: "Skew Join"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 69
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Skew Join(데이터 쏠림 조인)은 분산 조인(Distributed Join)에서 특정 키(Key)에 데이터가 극단적으로 편중될 때 해당 파티션의 단일 태스크가 전체 쿼리 완료를 가로막는 문제를 해결하기 위한 최적화 기법이다.
- **가치**: AQE (Adaptive Query Execution)가 런타임 통계를 분석해 스큐 파티션을 자동으로 분할·병렬화하고, 수동으로는 솔팅(Salting) 기법으로 키를 인위적으로 분산하여 작업 시간을 수십 배 단축할 수 있다.
- **판단 포인트**: 쿼리 실행 중 특정 태스크만 `Straggler`로 오래 걸릴 때, `explain()` 또는 Spark UI의 Stage 탭에서 파티션별 데이터 크기 편차를 확인하고 Skew Join 여부를 먼저 의심해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 데이터 스큐(Data Skew)란?

분산 시스템에서 데이터를 파티션에 균등하게 배분하는 것이 성능의 핵심이다. 그러나 실무 데이터는 완전히 균등하지 않다.

- **예시**: 전자상거래 로그에서 `user_id`로 조인 시, 봇(Bot) 계정 1개가 전체 트랜잭션의 30%를 차지
- **예시**: `country = 'US'`가 전 세계 레코드의 70%를 차지하는 지역 데이터

조인 시 동일 키는 동일 파티션에 배정(Hash Partitioning)되므로 스큐 파티션 하나의 태스크가 수백 GB를 처리하는 동안 나머지 태스크들은 유휴 상태로 기다린다.

### 2. 증상 식별

- Spark UI -> Stages -> 태스크 Duration이 특정 태스크만 **수십 배** 더 긴 경우
- `SELECT count(*), key FROM table GROUP BY key ORDER BY count DESC LIMIT 10` -> 상위 키 집중 여부 파악

**📢 섹션 요약 비유**
> 데이터 스큐는 "은행 창구 10개 중 1번 창구에만 고객 100명이 몰리는 상황"이다. 나머지 9개 창구는 놀고 있는데 1번 창구 때문에 모두가 기다린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. AQE 자동 Skew Join 최적화 (Spark 3.0+)

```
+--------------------------------------------------------------+
|  Stage 1: 셔플 맵 출력 (Shuffle Map Output)                   |
|                                                              |
|  파티션 0: 10 MB  ████                                       |
|  파티션 1:  8 MB  ███                                        |
|  파티션 2: 500MB  ████████████████████████████████ <- 스큐!   |
|  파티션 3: 12 MB  ████                                       |
+------------------+-------------------------------------------+
                   | AQE 통계 분석
                   v
+--------------------------------------------------------------+
|  AQE 판단: 파티션 2가 임계값(skewedPartitionFactor × 중앙값)  |
|           초과 -> 자동 분할                                    |
|                                                              |
|  파티션 2a: 250MB (절반)  + 상대편 파티션 2 전체 복사         |
|  파티션 2b: 250MB (나머지) + 상대편 파티션 2 전체 복사        |
+--------------------------------------------------------------+
```

AQE Skew Join 활성화 설정:
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# 스큐 파티션 판단 기준: 중앙값의 N배 이상
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
# 최소 스큐 크기: N MB 이상
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```

### 2. 수동 솔팅(Salting) 기법

AQE를 사용할 수 없거나 더 세밀한 제어가 필요할 때 솔팅 기법을 사용한다.

```python
import pyspark.sql.functions as F

SALT_FACTOR = 10  # 솔트 범위

# 스큐 테이블: 키에 솔트값 추가 (0~9를 랜덤 접두사로 붙임)
skewed_df = large_df.withColumn(
    "salted_key",
    F.concat(F.col("join_key"), F.lit("_"), (F.rand() * SALT_FACTOR).cast("int"))
)

# 정상 테이블: 키를 SALT_FACTOR만큼 복제 (explode)
normal_df_replicated = normal_df.withColumn(
    "salted_key",
    F.explode(F.array([F.concat(F.col("join_key"), F.lit(f"_{i}")) for i in range(SALT_FACTOR)]))
)

# 솔팅된 키로 조인
result = skewed_df.join(normal_df_replicated, "salted_key")
```

### 3. 기법 비교

| 기법 | 자동/수동 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| AQE Skew Join | 자동 | 스큐 파티션 자동 분할 | 코드 변경 없음 | 임계값 튜닝 필요 |
| Salting | 수동 | 키에 솔트 추가 -> 균등 분산 | 세밀한 제어 | 정상 테이블 복제 비용 |
| Broadcast Join | 수동 | 소규모 테이블 전 Executor 복사 | 셔플 완전 제거 | 소규모 테이블에만 적용 가능 |
| Repartition by Key | 수동 | 조인 전 파티션 재조정 | 간단 | 스큐 자체는 해결 안 됨 |

**📢 섹션 요약 비유**
> AQE의 Skew Join은 "교통 혼잡 감지 시스템"과 같다. 특정 도로(파티션)가 막히면 자동으로 옆길(분할 파티션)을 열어 차량(데이터)을 나눠 보낸다. 솔팅은 처음부터 차량 번호판에 임의 숫자를 붙여서 여러 도로로 분산시키는 사전 계획이다.

---

## Ⅲ. 비교 및 연결

### 1. Skew Join과 Broadcast Join의 선택 기준

| 조건 | 권장 기법 |
|:---|:---|
| 소규모 테이블 (< 수백 MB) | Broadcast Join (셔플 완전 제거) |
| 대형 테이블 간 조인, 특정 키 스큐 | AQE Skew Join 자동 처리 |
| 스큐 키가 사전에 알려진 경우 | 수동 Salting |
| 스큐 키가 null 다수인 경우 | null 키 필터링 후 처리 |

### 2. 연결 개념

- **AQE (Adaptive Query Execution)**: Skew Join 자동 감지의 상위 프레임워크
- <strong>파티션 최적화</strong>: repartition/coalesce와 Skew Join은 파티션 균형 문제의 서로 다른 측면
- <strong>Data Serialization</strong>: 스큐 파티션 크기가 클수록 직렬화 비용도 증가

**📢 섹션 요약 비유**
> Skew Join 최적화를 고를 때는 "택배 분류 시스템"을 설계하는 것과 같다. 박스가 작으면 한 직원이 전부 들고 나눠주면 되고(Broadcast), 특정 지역 택배가 너무 많으면 자동으로 팀을 나누거나(AQE) 주소지에 임의 코드를 붙여 여러 팀으로 분산(Salting)한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Skew Join 진단 및 해결 프로세스

```
1단계: 진단
  -> Spark UI > Stages > 태스크별 Duration 확인
  -> 스큐 의심 키에 대해 cardinality 분석

2단계: 기법 선택
  -> AQE 활성화 확인 (Spark 3.0+: 기본 true)
  -> 소규모 상대 테이블? -> Broadcast Join 힌트 적용
  -> 특정 키 스큐 심각? -> Salting 적용

3단계: 검증
  -> 재실행 후 태스크 Duration 균등화 확인
  -> 총 실행 시간 비교
```

### 2. 실무 체크리스트

- [ ] `spark.sql.adaptive.skewJoin.enabled = true` 확인
- [ ] 스큐 파티션 판단 팩터(`skewedPartitionFactor`) 데이터 특성에 맞게 조정
- [ ] 솔팅 적용 시 SALT_FACTOR는 스큐 배율의 1.5~2배 설정
- [ ] Null 키 처리 별도 로직 분리 (null은 하나의 파티션에 집중)
- [ ] 솔팅 후 정상 테이블 복제 크기가 메모리 한계를 초과하지 않는지 확인

**📢 섹션 요약 비유**
> Skew Join 해결책을 선택하는 것은 "병목 구간 해소 전략"이다. 작은 병목이면 길을 넓히고(Broadcast), 구조적 병목이면 진입 시간을 분산(Salting)하고, 자동차가 알아서 우회하게(AQE)도 할 수 있다. 세 가지를 병행하면 더 좋다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 수치 예시 |
|:---|:---|
| 스테이지 실행 시간 단축 | 스큐 해소 시 수 시간 -> 수십 분으로 단축 |
| 클러스터 자원 효율화 | 유휴 Executor 제거, CPU 활용률 균등화 |
| SLA(서비스 수준 협약) 안정화 | Straggler Task로 인한 지연 제거 |

### 2. 결론

Skew Join 최적화는 대규모 분산 조인을 다루는 모든 데이터 엔지니어가 반드시 이해해야 하는 <strong>분산 처리 성능 튜닝의 핵심</strong>이다. Spark 3.0+의 AQE가 많은 경우를 자동으로 처리하지만, 근본적인 데이터 편향 특성을 이해하고 솔팅 기법으로 사전 대응하는 능력이 실무자 수준의 역량이다.

**📢 섹션 요약 비유**
> Skew Join 최적화 없이 분산 조인을 하는 것은 "한 팀원에게만 전체 프로젝트를 몰아주고 다른 팀원들은 구경만 하게 두는 것"이다. AQE와 솔팅으로 일감을 공정하게 나누어야 팀 전체가 빠르게 완주한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| AQE (Adaptive Query Execution) | 상위 프레임워크 | Skew Join 자동 감지 및 분할의 엔진 |
| Broadcast Join | 대안 기법 | 소규모 테이블 조인 시 스큐 근원 제거 |
| Salting | 수동 대안 | 키 인위 분산으로 스큐 방지 |
| Shuffle Optimization | 연관 문제 | 셔플 자체를 줄이면 스큐 영향도 줄어듦 |
| 파티션 최적화 | 연관 문제 | 적정 파티션 수 설계가 스큐 예방에 기여 |


### 📈 관련 키워드 및 발전 흐름도

```text
[조인 연산 (Join Operation) — 분산 환경, 파티션 단위 병렬 처리]
    |
    v
[데이터 쏠림 (Data Skew) — 특정 키에 데이터 집중, 일부 태스크 지연]
    |
    v
[솔팅 기법 (Salting) — 키에 임의 접미사 추가, 파티션 분산]
    |
    v
[브로드캐스트 조인 (Broadcast Join) — 소형 테이블 전체 복제·전송]
    |
    v
[AQE (Adaptive Query Execution) — 런타임 파티션 재분배 자동화]
```
Skew Join은 데이터 쏠림으로 인한 특정 파티션 과부하를 솔팅·브로드캐스트·AQE로 완화하여 Spark 조인 성능을 균등하게 분산시킨다.
### 👶 어린이를 위한 3줄 비유 설명

교실에서 모둠별로 청소를 나눠서 하는데, 한 모둠에만 쓰레기가 산더미처럼 쌓여 있으면(데이터 스큐) 그 모둠은 한 시간 동안 치우고 나머지 모둠은 5분 만에 끝나고 기다려야 해요. 선생님(AQE)이 "저 모둠 쓰레기가 너무 많다" 고 보고 자동으로 두 팀으로 나눠줘요. 미리 쓰레기를 여러 통에 나눠 담아두면(Salting) 처음부터 공평하게 나눌 수 있어요!
