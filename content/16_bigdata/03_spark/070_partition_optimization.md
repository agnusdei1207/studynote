---
title: "Partition Optimization"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 70
---
## 핵심 인사이트 (3줄 요약)

- **본질**: 스파크에서 파티션 수는 병렬 처리의 단위이며, `repartition()`은 전체 셔플(Shuffle)을 수반하며 파티션 수를 늘리거나 줄이고, `coalesce()`는 셔플 없이 기존 파티션을 합쳐 수를 줄이는 것이 핵심 차이다.
- **가치**: 파티션이 너무 적으면 병렬성이 낮아 CPU가 유휴 상태가 되고, 너무 많으면 태스크 스케줄링 오버헤드와 소형 파일 문제가 발생하므로 `cores × 2~4`를 기준으로 조정하는 것이 성능 튜닝의 첫 번째 점검 항목이다.
- **판단 포인트**: `spark.sql.shuffle.partitions` 기본값 200은 소규모 데이터에는 과도하고 대규모 데이터에는 부족하므로, 실행 전 데이터 크기를 추정하여 파티션당 128~200MB 기준으로 조정하거나 AQE (Adaptive Query Execution)의 자동 병합 기능을 활용한다.

---

## Ⅰ. 개요 및 필요성

### 1. 파티션이 중요한 이유

스파크에서 파티션(Partition)은 <strong>작업의 최소 실행 단위</strong>다. 하나의 파티션은 하나의 태스크(Task)로 실행되고, 하나의 태스크는 하나의 코어(Core)에서 실행된다.

```
파티션 수 = 태스크 수 = (이론상 최대) 병렬 처리 수
```

- **파티션 < 코어 수**: 일부 코어 유휴 -> 클러스터 자원 낭비
- **파티션 >> 코어 수**: 태스크 스케줄링 오버헤드, 소형 파일 문제
- <strong>파티션 크기 불균형 (스큐)</strong>: 특정 태스크만 오래 걸리는 Straggler 문제

### 2. 파티션 관련 주요 설정

| 설정 키 | 기본값 | 영향 범위 |
|:---|:---|:---|
| `spark.sql.shuffle.partitions` | 200 | SQL/DataFrame 셔플 후 파티션 수 |
| `spark.default.parallelism` | 코어 수 × 2 | RDD 연산 기본 병렬성 |
| `spark.sql.files.maxPartitionBytes` | 128 MB | 파일 읽기 시 파티션당 최대 크기 |
| `spark.sql.adaptive.coalescePartitions.enabled` | true (3.0+) | AQE 파티션 자동 병합 |

**📢 섹션 요약 비유**
> 파티션은 "공장의 생산 라인 수"다. 라인이 1개면 작업자 100명이 있어도 줄 서서 기다려야 하고, 라인이 10만 개면 라인 관리 비용이 생산 비용보다 커진다. 적정 수가 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. repartition() vs coalesce() 동작 비교

```
    [repartition(N)]                    [coalesce(N)]
    -----------------                   ----------------
    파티션 A --- 셔플 ---> 신규 파티션 1  파티션 A ---------> 합쳐진 파티션 1
    파티션 B --- 셔플 ---> 신규 파티션 2  파티션 B -----+
    파티션 C --- 셔플 ---> 신규 파티션 3  파티션 C -----+-> 합쳐진 파티션 2
    파티션 D --- 셔플 ---> 신규 파티션 N  파티션 D ----------> 합쳐진 파티션 3

    · 전체 셔플 발생 (네트워크 I/O^)   · 셔플 없음 (로컬 병합)
    · 파티션 수 증가/감소 모두 가능     · 파티션 수 감소만 가능
    · 균등한 데이터 분포 보장           · 파티션 크기 불균형 가능
```

### 2. 파티션 최적화 전략

```python
# 데이터 크기 기준 파티션 계산
# 권장: 파티션당 100~200 MB
total_data_gb = 100  # 100 GB 데이터
partition_size_mb = 128
optimal_partitions = (total_data_gb * 1024) // partition_size_mb  # ≈ 800

# 코어 수 기준
num_cores = 200  # 클러스터 총 코어
target_partitions = num_cores * 3  # ≈ 600

# 셔플 파티션 설정
spark.conf.set("spark.sql.shuffle.partitions", "600")

# 데이터 크기에 따른 동적 조정 (AQE)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionNum", "50")
```

### 3. repartition vs coalesce 선택 기준

| 상황 | 권장 API | 이유 |
|:---|:---|:---|
| 파티션 수 늘리기 | `repartition(N)` | coalesce는 늘릴 수 없음 |
| 파티션 수 줄이기 (소량 감소) | `coalesce(N)` | 셔플 없이 빠르게 처리 |
| 파티션 수 줄이기 (대폭 감소) | `repartition(N)` | coalesce는 데이터 불균형 위험 |
| 특정 컬럼으로 재분배 | `repartition(N, col)` | 후속 조인/집계 셔플 제거 |
| 파일 저장 전 파티션 수 조정 | `coalesce(N)` | 셔플 없이 소형 파일 문제 해결 |

**📢 섹션 요약 비유**
> `repartition`은 "이사할 때 물건을 전부 꺼내서 새롭게 정리"하는 것이고, `coalesce`는 "이웃 방들을 합쳐서 큰 방으로 만들되 짐은 그대로 두는 것"이다. 셔플(이사)은 비싸다.

---

## Ⅲ. 비교 및 연결

### 1. AQE의 자동 파티션 최적화

AQE (Adaptive Query Execution)는 셔플 후 실제 데이터 크기를 확인하고 파티션을 자동으로 병합한다.

```
셔플 후 200개 파티션 -> AQE 분석
  파티션 150개: 1 KB 이하 (대부분 비어 있음)
  파티션 50개: 128~256 MB

-> AQE 결정: 빈 파티션 자동 병합 -> 실제 50개 파티션으로 줄임
```

`spark.sql.adaptive.coalescePartitions.enabled=true` (기본값: true in Spark 3.0+)

### 2. 파티션 최적화 vs Skew Join 관계

파티션 최적화는 파티션 수를 조절하는 것이고, Skew Join은 파티션 내 데이터 크기 불균형을 해소하는 것이다. 두 문제는 다른 레이어에서 발생하므로 모두 점검해야 한다.

**📢 섹션 요약 비유**
> AQE의 파티션 자동 병합은 "마트 계산대 수 자동 조절"과 같다. 손님이 적은 시간대에는 계산대(파티션) 수를 줄여 직원(코어)이 낭비되지 않게 한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. 파티션 튜닝 실무 워크플로우

```
Step 1: 현재 파티션 수 확인
  df.rdd.getNumPartitions()

Step 2: 파티션별 크기 측정
  df.groupBy(F.spark_partition_id()).count().show()

Step 3: 목표 파티션 수 계산
  target = max(총_데이터_MB // 128, 총_코어_수 * 2)

Step 4: 조정
  df_opt = df.repartition(target)  # 또는 coalesce

Step 5: AQE 활성화 확인
  spark.sql("SET spark.sql.adaptive.enabled=true")
```

### 2. 소형 파일 문제와 파티션

Parquet 저장 시 파티션 수 = 출력 파일 수이므로, 과도한 파티션은 소형 파일 문제(Small File Problem)를 유발한다.

```python
# 저장 전 파티션 최적화
df.coalesce(10).write.parquet("/output/path")  # 소규모 결과
df.repartition(100).write.parquet("/output/path")  # 균등 크기 필요
```

### 3. 체크리스트

- [ ] `spark.sql.shuffle.partitions` = 코어 수 × 2~4 (기본 200에서 조정)
- [ ] AQE 활성화 (`spark.sql.adaptive.enabled=true`)
- [ ] 파일 저장 전 `coalesce()` 또는 `repartition()` 적용으로 소형 파일 방지
- [ ] 조인 전 조인 키로 `repartition(col)` 적용 시 후속 셔플 제거 가능

**📢 섹션 요약 비유**
> 파티션 튜닝은 "다리 차선 수 결정"과 같다. 차량이 적은데 차선이 너무 많으면 유지 비용만 들고, 차량이 많은데 차선이 적으면 정체가 심하다. 교통량(데이터 크기)에 맞는 차선 수(파티션)를 결정해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 최적화 항목 | 기대 효과 |
|:---|:---|
| 적정 파티션 수 설정 | CPU 활용률 극대화, 불필요한 태스크 오버헤드 제거 |
| coalesce 사용 | 셔플 비용 없이 파티션 축소 |
| AQE 자동 병합 | 소규모 셔플 파티션 자동 제거 |
| 저장 전 coalesce | 소형 파일 수 감소 -> 다음 읽기 성능 향상 |

### 2. 결론

파티션 최적화는 Spark 성능 튜닝의 **가장 기초적이면서도 효과가 큰** 항목이다. `repartition`과 `coalesce`의 차이를 정확히 이해하고, AQE의 자동 최적화를 활용하되, 데이터 특성에 맞게 수동 조정하는 판단력이 중요하다.

**📢 섹션 요약 비유**
> 파티션 최적화 없는 Spark 튜닝은 "타이어 공기압 확인 없이 F1 레이싱에 출전하는 것"이다. 기본 중의 기본이지만 이것 하나만 잘 잡아도 레이스 성적이 크게 달라진다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| AQE (Adaptive Query Execution) | 자동화 수단 | 셔플 후 파티션 자동 병합 |
| Skew Join | 연관 문제 | 파티션 내 데이터 편중 문제 |
| Shuffle Optimization | 상위 개념 | 셔플 비용 최소화 전략의 일부 |
| Small File Problem | 영향 | 과도한 파티션 = 소형 파일 양산 |
| Broadcast Join | 셔플 제거 | 소규모 테이블 조인 시 셔플 자체를 없앰 |

### 📈 관련 키워드 및 발전 흐름도

```text
[RDD (탄력적 분산 데이터셋) — 기본 파티션으로 클러스터 분산 처리]
    |
    v
[파티션 최적화 — coalesce·repartition·partitionBy로 편향 해소]
    |
    v
[Adaptive Query Execution (AQE) — 런타임 통계 기반 동적 파티션 재조정]
    |
    v
[Delta Lake Z-Order — 데이터 레이아웃 최적화로 스킵 I/O 극대화]
```
Spark 파티션 최적화는 데이터 편향을 제거하고 병렬성을 극대화하며, AQE와 Delta Lake의 Z-Order 클러스터링으로 더욱 지능적으로 발전하고 있다.

### 👶 어린이를 위한 3줄 비유 설명

숙제를 반 친구 30명이 나눠 하는데, 문제를 1개만 나누면 1명이 다 하고 29명은 놀아야 하고, 반대로 1000개로 나누면 나누는 데만 시간이 다 걸려요. `repartition`은 숙제를 전부 섞어서 새로 나누는 것이고, `coalesce`는 옆 친구 것을 합쳐서 뭉치는 것이에요. 선생님(AQE)이 자동으로 알맞게 조정해주기도 해요!
