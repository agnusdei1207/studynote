---
title: "Lazy Evaluation"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 217
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Spark의 지연 평가(Lazy Evaluation)는 트랜스포메이션(map, filter 등) 연산을 즉시 실행하지 않고 DAG(유향 비순환 그래프)에 기록했다가, 액션(count, save 등)이 호출될 때 Catalyst Optimizer가 전체 실행 계획을 최적화한 후 한 번에 실행하는 방식이다.
> 2. **가치**: 개별 연산을 즉시 실행하면 불필요한 중간 데이터가 생성되지만, 지연 평가를 통해 Optimizer가 연산 순서 재배치·불필요한 단계 제거·푸시다운(Predicate Pushdown) 등의 최적화를 적용하여 실제 실행 비용을 최소화한다.
> 3. **판단 포인트**: 지연 평가는 Spark 성능 최적화의 핵심이지만, 잘못 이해하면 `collect()`를 루프 안에서 호출하거나 불필요한 `show()`를 남발하여 오히려 성능을 해치는 함정에 빠질 수 있다.

---

## Ⅰ. 개요 및 필요성

수학에서 함수 `f(x) = 2x + 1`을 정의할 때, x 값을 알지 못해도 함수를 정의할 수 있다. x가 주어질 때(즉, 실제 계산이 필요할 때)만 결과가 계산된다. Spark의 지연 평가는 이와 정확히 같은 원리다.

`df.filter(df.age > 30).groupBy("dept").count()`라는 Spark 코드를 작성할 때, 처음 두 연산(filter, groupBy)은 즉시 실행되지 않는다. `.count()` 액션이 호출될 때, Spark의 Catalyst Optimizer가 이 세 연산 전체를 하나의 실행 계획으로 보고 최적화를 수행한 후 클러스터에 제출한다.

지연 평가의 핵심 이점은 <strong>전체 맥락을 알고 최적화한다</strong>는 것이다. 각 연산을 따로 실행하면 filter의 결과를 임시 저장 후 groupBy에 전달해야 하지만, 지연 평가를 통해 Optimizer가 "filter를 먼저 하면 groupBy의 데이터 크기가 줄어든다"는 것을 알고 최적 순서로 실행한다.

📢 **섹션 요약 비유**: 지연 평가는 출장 여행 계획과 같다. 서울->부산->광주->서울 순서를 바로 예약하지 않고, 모든 방문지를 먼저 정한 후 여행사(Optimizer)에게 최적 경로(비용·시간 최소화)를 계산해달라고 맡기는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DAG 실행 계획 최적화 과정

```
  사용자 코드 (PySpark/Scala)
       |
       v
  +---------------------------------------------------------+
  |              Catalyst Optimizer                          |
  |                                                          |
  |  1단계: Logical Plan (논리적 계획)                        |
  |     filter(age>30) -> groupBy(dept) -> count()            |
  |                    |                                    |
  |  2단계: Optimized Logical Plan (최적화 논리 계획)          |
  |     Predicate Pushdown: filter를 데이터 소스로 내림       |
  |     Column Pruning: 필요한 컬럼만 읽음                    |
  |                    |                                    |
  |  3단계: Physical Plan 선택 (물리적 실행 계획)              |
  |     Join 방식: BroadcastHashJoin vs SortMergeJoin        |
  |     실제 실행 방식 결정                                   |
  |                    |                                    |
  |  4단계: Code Generation (Tungsten)                       |
  |     JVM 바이트코드 직접 생성 -> 최적 실행                  |
  +---------------------------------------------------------+
       |
       v
  Spark Executor에서 최적화된 Job 실행
```

### 주요 최적화 기법

| 최적화 | 설명 | 효과 |
|:---|:---|:---|
| **Predicate Pushdown** | 조건(filter)을 데이터 소스에 최대한 가까이 적용 | 읽는 데이터 양 감소 |
| <strong>Column Pruning</strong> | 필요한 컬럼만 선택하여 읽기 | I/O 최소화 |
| <strong>Join 재정렬</strong> | 작은 테이블을 먼저 처리 | 네트워크 셔플 감소 |
| **Constant Folding** | 상수 표현식을 컴파일 타임에 계산 | 런타임 오버헤드 제거 |
| <strong>Broadcast Join</strong> | 작은 테이블을 모든 노드에 브로드캐스트 | 대규모 셔플 제거 |

### 지연 평가 실습 예시

```python
# 모두 트랜스포메이션 - 즉시 실행 안 됨, DAG에 기록만
df = spark.read.parquet("s3://data/orders/")   # 데이터 로딩도 지연!
filtered = df.filter(df.status == "completed")  # 지연
selected = filtered.select("user_id", "amount") # 지연
grouped = selected.groupBy("user_id")           # 지연
result = grouped.sum("amount")                  # 지연

# 아직 아무것도 실행되지 않았다!

# 액션 호출 시점에 전체 DAG가 최적화되어 실행됨
result.show()    # 이 순간 실행! Optimizer가 최적화 후 클러스터에 제출

# DAG 실행 계획 확인
result.explain(mode="extended")  # 논리적/물리적 계획 출력
```

📢 **섹션 요약 비유**: Catalyst Optimizer는 GPS 내비게이션과 같다. 출발지·경유지·도착지를 모두 입력받은 후(모든 트랜스포메이션 수집), 최적 경로를 계산하여(실행 계획 최적화), 한 번에 안내를 시작한다(액션 실행). 경유지마다 경로를 따로 계산하지 않는다.

---

## Ⅲ. 비교 및 연결

### Eager Evaluation vs Lazy Evaluation

| 항목 | Eager Evaluation | Lazy Evaluation (Spark) |
|:---|:---|:---|
| 실행 시점 | 각 연산 즉시 | 액션 호출 시 일괄 |
| 최적화 가능성 | 낮음 (개별 최적화) | 높음 (전체 맥락 최적화) |
| 디버깅 | 쉬움 (즉시 결과) | 어려움 (에러가 액션 시 발생) |
| 메모리 효율 | 낮음 (중간 결과 저장) | 높음 (파이프라인 융합) |
| 언어 | Python(기본), pandas | Spark, Haskell |

### 함수 합성(Pipeline Fusion)

```python
# 지연 평가 없이 (가정):
step1 = df.map(f1)        # 10M 행 생성, 저장
step2 = step1.filter(f2)  # 1M 행 생성, 저장 (9M 버려짐)
step3 = step2.map(f3)     # 1M 행 처리

# 지연 평가 (Spark): Pipeline Fusion
# f1 -> f2 -> f3를 하나의 단계로 합쳐서 실행
# 불필요한 중간 결과 저장 없음, 메모리 효율 최대화
```

📢 **섹션 요약 비유**: Pipeline Fusion은 공장 컨베이어 벨트와 같다. 자동차 부품을 1단계 가공 후 창고에 저장하고, 다시 꺼내서 2단계 가공 후 저장하는 대신, 컨베이어 벨트에서 1->2->3단계를 연속으로 처리하여 중간 저장 없이 완성차를 만든다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>지연 평가의 함정 - 흔한 실수</strong>:
```python
# ❌ 잘못된 패턴: 루프에서 collect() 호출
for user_id in user_ids:  # user_ids = large list
    df.filter(df.user_id == user_id).collect()  # 매번 Job 생성!
    # -> 수천 개의 별도 Job 생성 = 극도로 느림

# ✅ 올바른 패턴: 한 번에 처리
result = df.filter(df.user_id.isin(user_ids)).collect()

# ❌ 잘못된 패턴: 개발 중 너무 많은 show() 호출
df.filter(...).show()          # Job 실행 1번
df.filter(...).groupBy().show() # Job 실행 또 1번 (filter 재실행!)

# ✅ 올바른 패턴: 중간 결과 cache()로 재사용
filtered = df.filter(...).cache()
filtered.show()               # Job 실행 1번 + 캐시
filtered.groupBy().show()     # 캐시에서 즉시 처리
```

<strong><code>explain()</code>으로 실행 계획 분석</strong>:
```python
# 실행 계획 확인 (성능 진단의 시작)
df.filter(df.age > 30).groupBy("dept").count().explain()

# 출력 예시:
# == Physical Plan ==
# *(2) HashAggregate(keys=[dept#0], functions=[count(1)])
# +- Exchange hashpartitioning(dept#0, 200)
#    +- *(1) HashAggregate(keys=[dept#0], functions=[partial_count(1)])
#       +- *(1) Project [dept#0]             <- Column Pruning 적용
#          +- *(1) Filter (isnotnull(age#1) AND (age#1 > 30))  <- Pushdown 적용
#             +- *(1) FileScan parquet [age#1,dept#0]  <- 필요한 컬럼만 읽음
```

**실무자 판단 포인트**:
- `explain()` 출력에서 `FileScan`의 컬럼 수가 적으면 Column Pruning이, Filter가 FileScan 바로 위에 있으면 Predicate Pushdown이 적용된 것이다.
- 지연 평가로 인해 에러가 액션 시점에서야 발생한다. 개발 단계에서 `sample()`로 소량 데이터로 먼저 테스트하면 빠른 디버깅이 가능하다.
- `adaptive query execution(AQE)` (Spark 3.0+): 실행 중 통계 기반으로 동적 계획 재최적화.

📢 **섹션 요약 비유**: `explain()`은 GPS 내비게이션에서 "경로 상세 보기"를 누르는 것과 같다. 어떤 도로를 왜 선택했는지, 어디서 최적화가 이루어졌는지 확인할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 자동 최적화 | 개발자가 최적화를 몰라도 Catalyst가 처리 |
| 불필요한 연산 제거 | 사용하지 않는 컬럼·조건을 자동 제거 |
| 파이프라인 융합 | 여러 연산을 하나의 단계로 합쳐 중간 저장 제거 |
| Pushdown 최적화 | 데이터 소스 레벨에서 필터링으로 I/O 최소화 |

지연 평가는 Spark를 단순한 분산 처리 엔진을 넘어 <strong>자동 최적화 플랫폼</strong>으로 만드는 핵심이다. 개발자는 "무엇을 처리할 것인가"(논리적 계획)만 표현하고, Catalyst Optimizer가 "어떻게 처리할 것인가"(물리적 계획)를 결정한다. 이 선언적(Declarative) 프로그래밍 모델이 Spark DataFrame의 가장 강력한 특성이다.

📢 **섹션 요약 비유**: 지연 평가와 Catalyst Optimizer의 관계는 요리사(개발자)와 자동 주방 시스템(Optimizer)의 관계다. 요리사는 "오늘 메뉴는 파스타, 스테이크, 디저트"만 결정하고, 시스템이 재료 구매 순서·조리 시간·오븐 온도를 자동으로 최적화한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Catalyst Optimizer | 지연 평가를 활용하여 실행 계획을 최적화하는 Spark 핵심 |
| DAG (방향성 비순환 그래프) | 트랜스포메이션 연산들이 기록되는 실행 계획 구조 |
| Predicate Pushdown | 데이터 소스로 필터 조건을 내려보내는 I/O 최적화 |
| RDD / DataFrame | 지연 평가가 적용되는 Spark 데이터 추상화 |
| cache() / persist() | 반복 사용 데이터를 메모리에 유지하여 재계산 방지 |
| AQE (Adaptive Query Execution) | Spark 3.0의 실행 중 동적 최적화 기능 |

### 👶 어린이를 위한 3줄 비유 설명

1. 지연 평가는 여행 계획을 세울 때, 각 교통편을 바로 예약하는 대신 모든 일정을 다 정한 후 여행사에 최적 루트를 부탁하는 것이야.

### 📈 관련 키워드 및 발전 흐름도

```text
Eager Evaluation: 즉시 실행 (최적화 기회 없음)
    |
    v
Lazy Evaluation: DAG 구축 -> Action 호출 시 실행
    +-► Catalyst Optimizer: 실행 계획 최적화
    +-► Predicate Pushdown · Partition Pruning
    |
    v
Adaptive Query Execution (AQE): 런타임 동적 최적화
```
2. Spark도 filter, groupBy, count 같은 연산을 모두 모아두었다가, "결과를 줘!"(액션) 할 때 한 번에 최적화해서 실행해.
3. 덕분에 "필요한 자료만 가져오기(Pushdown)", "중간 저장 없이 연속 처리(Pipeline Fusion)" 등의 자동 최적화가 가능해.
