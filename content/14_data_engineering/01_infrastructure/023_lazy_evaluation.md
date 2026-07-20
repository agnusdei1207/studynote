---
title: "Lazy Evaluation"
date: "2026-04-29"
tags:
  - "studynote-data-engineering"
weight: 23
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지연 평가(Lazy Evaluation)는 식(Expression)의 결과가 실제로 필요한 시점까지 계산을 미루는 평가 전략으로, 불필요한 연산을 원천 차단하고 무한 시퀀스(Infinite Sequence) 같은 자료구조를 유한 메모리에서 처리할 수 있게 한다.
> 2. **가치**: Apache Spark·Haskell·Python Generator 등에서 핵심 설계 원칙으로 채택되어, 수억 건의 데이터셋 전체를 메모리에 올리지 않고 최종 필요한 결과만 계산하는 실행 계획 최적화(Query Plan Optimization)의 이론적 기반이 된다.
> 3. **판단 포인트**: 지연 평가는 실행 계획(Execution Plan)이 실제 데이터 처리 전에 생성되므로, Spark DAG(Directed Acyclic Graph)처럼 최적화기(Optimizer)가 연산 순서를 재배치하고 불필요한 스테이지를 제거할 수 있어 즉시 평가(Eager Evaluation) 대비 I/O와 CPU 비용을 대폭 절감한다.

---

## Ⅰ. 개요 및 필요성

지연 평가(Lazy Evaluation)는 함수형 프로그래밍(Functional Programming)에서 시작된 개념으로, 연산 결과가 명시적으로 요구될 때까지 계산을 지연시키는 프로그램 실행 전략이다.

즉시 평가(Eager Evaluation)에서는 `map(f, huge_list)`처럼 거대한 리스트 전체를 변환해 메모리에 올리지만, 결국 처음 10개 결과만 사용한다면 나머지 수백만 건의 연산은 낭비다. 지연 평가는 이 문제를 연산을 "레시피(실행 계획)"로만 기억하고, 결과가 필요할 때 그 레시피를 실행하는 방식으로 해결한다.

```text
+------------------------------------------------------------+
|           즉시 평가 vs 지연 평가 비교                         |
+------------------------------------------------------------+
|                                                            |
|  [즉시 평가 (Eager)]                                        |
|  data = [1..1000000]                                       |
|  result = filter(>100, map(*2, data))  <- 즉시 전체 실행     |
|  first_10 = take(10, result)                               |
|  -> 100만 번 연산 후 10개만 사용 (낭비!)                      |
|                                                            |
|  [지연 평가 (Lazy)]                                         |
|  data = [1..∞]  <- 무한 리스트 (메모리에 없음!)               |
|  result = filter(>100, map(*2, data))  <- 실행 계획만 기록   |
|  first_10 = take(10, result)  <- 여기서 실제 10번만 실행     |
|  -> 딱 10개 계산 (최적!)                                     |
+------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 지연 평가는 "배달 음식 미리 주문"이 아니라, 진짜 배고플 때 주문하는 것이다. 언제 먹을지 모르는데 미리 100인분 시켜두면 낭비지만, 먹으려는 순간 딱 필요한 만큼만 주문하면 낭비가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Spark의 지연 평가: Transformation vs Action

Apache Spark는 지연 평가를 RDD (Resilient Distributed Dataset, 분산 탄력 데이터셋) 연산의 핵심 원리로 채택한다.

| 구분 | 연산 예시 | 실행 시점 | 설명 |
|:---|:---|:---|:---|
| **Transformation (변환)** | map, filter, groupBy, join | 지연 — Action까지 실행 안 함 | DAG에 단계만 기록 |
| **Action (행동)** | collect, count, save, show | 즉시 실행 | DAG를 실제로 실행 트리거 |

```text
+----------------------------------------------------------+
|           Spark 지연 평가 DAG 최적화 흐름                  |
+----------------------------------------------------------+
|                                                          |
|  RDD.filter(condition)  <- Transformation 1 (기록만)       |
|     .map(transform)     <- Transformation 2 (기록만)       |
|     .join(other_rdd)    <- Transformation 3 (기록만)       |
|     .count()            <- Action! 여기서 DAG 실행         |
|                                                          |
|  Catalyst Optimizer 개입:                                 |
|  filter -> map -> join  ->  filter를 join 앞으로 이동!        |
|  (Predicate Pushdown: 데이터 줄인 후 join -> 비용 80% 절감)  |
+----------------------------------------------------------+
```

### Python Generator의 지연 평가

```python
# 즉시 평가: 100만 개 리스트 메모리에 올림
big_list = [x*2 for x in range(1_000_000)]

# 지연 평가: 필요할 때 하나씩 생성
lazy_gen = (x*2 for x in range(1_000_000))
first_10 = [next(lazy_gen) for _ in range(10)]  # 10번만 실행
```

- **📢 섹션 요약 비유**: Spark의 Transformation은 요리 레시피를 책에 적어두는 것(기록), Action은 레시피를 보고 실제 요리를 시작하는 것(실행)이다. 레시피가 모이면 Optimizer가 "이 순서가 더 효율적이다"라며 순서를 재배치해 준다.

---

## Ⅲ. 비교 및 연결

| 평가 전략 | 언어/시스템 | 메모리 | 최적화 가능 | 무한 시퀀스 |
|:---|:---|:---|:---|:---|
| **즉시 평가 (Eager)** | Python list, Java, C | 즉시 소비 | 어려움 | 불가 |
| <strong>지연 평가 (Lazy)</strong> | Haskell, Spark RDD, Python Generator | 필요 시 소비 | 가능 (Optimizer) | 가능 |
| <strong>부분 지연 (Short-Circuit)</strong> | Python and/or, Java &&·｜｜ | 조건부 소비 | 조건부 | 불가 |

지연 평가는 Haskell에서 기본 평가 전략이며, Scala·Kotlin에서는 `lazy val`, `Sequence`로 선택적 지연 평가를 지원한다. 데이터 엔지니어링에서는 Spark SQL의 Catalyst Optimizer가 지연 평가 기반 실행 계획을 물리 실행 계획(Physical Plan)으로 최적화하는 과정이 핵심이다.

- **📢 섹션 요약 비유**: 즉시 평가는 식당에 앉자마자 메뉴 전체를 주문하는 것이고, 지연 평가는 먹고 싶은 것이 결정됐을 때만 주문하는 것이다. 웨이터(Optimizer)는 주문 목록을 보고 가장 효율적인 조리 순서를 알아서 조정해 준다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오: Spark 잡 성능 최적화
10억 건 로그 데이터에서 오류 코드 500인 건만 집계하는 Spark 잡이 느리다.

1. **문제**: `join` 후 `filter`를 수행하는 잘못된 연산 순서 (Transformation 기록 순서 오류).
2. **분석**: Spark UI에서 DAG를 확인 -> Join Stage 전 데이터가 10억 건.
3. **해결**: `filter(error_code == 500)`을 `join` 앞으로 이동 (Predicate Pushdown 활용).
4. **결과**: Join 대상 데이터 90% 감소 -> 잡 실행 시간 75% 단축.

### 체크리스트
- `collect()`는 드라이버 메모리로 전체 RDD를 가져오므로 대용량 데이터에 절대 사용 금지.
- `persist()`/`cache()`로 자주 재사용하는 RDD를 메모리에 체크포인트.
- `explain()`으로 Spark SQL 실행 계획(Physical/Logical Plan) 확인 후 최적화 여부 점검.

### 안티패턴
- Spark DataFrame 연산을 Action 없이 무한정 체이닝하는 코드. Transformation이 수백 단계 쌓이면 DAG가 지나치게 커져 Catalyst Optimizer의 최적화 비용 자체가 폭증한다. 중간에 `checkpoint()`로 Lineage를 잘라주는 것이 필요하다.

- **📢 섹션 요약 비유**: Transformation을 무한 체이닝하는 건 요리 레시피를 1000페이지까지 적어두는 것과 같다. 레시피 자체를 읽는 데 너무 오래 걸려 정작 요리를 시작하지 못하는 상황이 된다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **I/O 최소화** | 불필요 데이터 처리 원천 차단 | I/O 60~80% 절감 |
| **메모리 효율** | 무한 시퀀스도 유한 메모리로 처리 | OOM 에러 방지 |
| **최적화 기회** | Optimizer의 실행 계획 재배치 허용 | 잡 시간 50~75% 단축 |

지연 평가는 Spark SQL의 Adaptive Query Execution (AQE, 적응형 쿼리 실행)과 결합하여 실행 중 실시간으로 파티션 크기와 조인 전략을 동적으로 최적화하는 방향으로 진화하고 있다. 데이터 엔지니어는 지연 평가의 원리를 이해해야 Spark 잡 성능 튜닝과 비용 최적화를 실질적으로 수행할 수 있다.

- **📢 섹션 요약 비유**: 지연 평가는 슬기로운 학생이 수업 전 예습을 전부 다 하는 대신, 선생님이 실제로 질문하는 부분만 집중해서 공부하는 전략이다. 쓸데없는 공부(연산)를 줄이고, 진짜 필요한 것만 깊게 파는 효율의 극한이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Spark RDD/DataFrame</strong> | 지연 평가 기반 분산 데이터셋; Transformation-Action 구조 |
| <strong>DAG (Directed Acyclic Graph)</strong> | Spark의 실행 계획 그래프; 지연 평가로 빌드된 후 Action으로 실행 |
| <strong>Catalyst Optimizer</strong> | Spark SQL의 지연 평가 기반 논리·물리 실행 계획 최적화기 |
| **Python Generator** | 파이썬에서 지연 평가를 구현하는 `yield` 기반 이터레이터 |
| **Predicate Pushdown** | 필터 조건을 데이터 소스 근처로 이동시켜 처리 데이터 최소화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[함수형 프로그래밍 (Haskell) — 기본 평가 전략으로 지연 평가]
    |
    v
[Python Generator / Scala Lazy Val — 선택적 지연 평가]
    |
    v
[Spark RDD Transformation — 분산 지연 평가 + DAG]
    |
    v
[Catalyst Optimizer — 지연 평가 기반 실행 계획 최적화]
    |
    v
[AQE (Adaptive Query Execution) — 런타임 동적 최적화]
```
함수형 언어의 지연 평가 개념이 Python Generator, Spark RDD로 이어지며, Catalyst Optimizer와 AQE를 통해 런타임 적응형 최적화로 진화하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 지연 평가는 숙제를 미리 다 하는 게 아니라, **선생님이 물어볼 때만** 그 부분을 푸는 영리한 공부법이에요!
2. 수학 문제 100개 중 10개만 물어볼 거라면, 100개 다 풀어두는 건 낭비잖아요 — 지연 평가는 딱 필요한 것만 계산한답니다.
3. 스파크(Spark)라는 데이터 처리 도구는 이 방법 덕분에 수억 개의 데이터도 메모리 걱정 없이 빠르게 처리할 수 있어요!
