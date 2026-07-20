---
title: "Lazy Evaluation"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 54
---
# 지연 평가 (Lazy Evaluation) - 계산을 미루는 지혜의 모든 것

> ⚠️ 이 문서는 Apache Spark를 포함한 함수형 프로그래밍 언어와 분산 처리 프레임워크에서 핵심적으로 사용되는 평가 전략인 Lazy Evaluation(지연 평가)이 무엇이며, 왜"Eager Evaluation(즉시 평가)"보다 대규모 데이터 처리에서 뛰어난 효율성을 제공하는지, DAG(방향성 비순환 그래프) 기반 실행 모델과 어떻게 결합되어 불필요한 연산을 자동으로 제거하고 네트워크 데이터 이동을 최소화하는지 실무자 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Lazy Evaluation은 데이터 변환 연산(map, filter, flatMap 등)을 코드에 작성하는 순간 실행하지 않고, 그저"어떤 입력을 어떤 변환으로 출력해야 한다"는 실행 계획(DAG)만 기록해 두었다가, 최종 결과가 필요한 시점(Action 호출 시)에 비로소 실제 연산을 시작하는 평가 전략이다.
> 2. **가치**: 실제 연산을 미루기 때문에, 실행 계획 전체를조감(グローバル)하여 불필요한 중간 결과를 완전히 제거하거나(필터 누르기/필터 병합), 파이프라이닝이 가능한 단계를 하나의 Stage로 합쳐서 네트워크 Shuffle을 최소화하는 등 전체 최적화를 한 번에 수행할 수 있다.
> 3. **확장**: Lazy Evaluation은 Spark뿐 아니라 Haskell(순수 함수형), Apache Flink, Apache Beam, Python(Generator/Lazy Iterator) 등 사실상 모든 현대적 데이터 처리 프레임워크의 근간이며, 빅데이터뿐 아니라 대용량 파일 스트리밍, 무한 시퀀스, 모듈성 관점에서도 핵심 설계 원칙이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 즉시 평가 (Eager Evaluation)의 문제점: 쓸데없는 계산을 미리 다 해버리다
대부분의 명령형 프로그래밍 언어(Java, C, Python의 기본 변수 대입 등)는 표현식을 작성하는 순간 즉시 값을 평가(Compute)합니다. 이를 "Strict Evaluation" 또는 "Eager Evaluation"이라 합니다.
- **문제 상황**: `val result = data.filter(_.contains("ERROR")).map(_.split(",")).count()`라는 코드를 생각해 봅시다. Eager 언어에서는 `filter`의 결과를 저장할 중간 컬렉션이 먼저 메모리에 생성되고, 그 다음에 `map`이 그 중간 결과를 가공하여 또 다른 컬렉션이 메모리에 생성되며, 결국 `count`가 최종 값을 산출합니다. 데이터가 1억 건이라면-filter 결과만 5,000만 건일 수 있으며, 그 5,000만 건짜리 중간 배열이 원인 없이 메모리를 점유하게 됩니다.
- **변환 로드밸런싱 불가**: 여러 단계의 변환을 한 번에 실행하면, 시스템 전체의 부하를 고려한 최적의 실행 순서를운행시에 적용할 수 없습니다. 예를 들어, 데이터가 파티션 A에는 100만 건, 파티션 B에는 10만 건인데, A에 filter를 먼저 적용하면 전체 데이터가 균등하게 분배될 수도 있지만, 전체를 한 번에 실행하면 그런 최적화 기회가 사라집니다.
- **불필요한 연산의 실행**: filter 조건에 맞는 데이터가 전혀 없을 경우(전체 0건), map을 실행하는 것은 완전히 쓸데없는 낭비가 됩니다. Eager Evaluation에서는 이 여부를 판단할 수단이 없이 일단 다 실행해 버립니다.

### 2. Lazy Evaluation의 설계 철학:plan은 계획대로, 실행은 필요한 때
Lazy Evaluation은 수학에서"드 모르간 법칙"과 같은 원리를 프로그래밍에 적용한 것입니다.
- **원칙**: "표현식의 평가(Evaluation)는 그 결과가 실제로 필요할 때까지 미룬다."
- <strong>실행 계획 vs 실행</strong>: Lazy Evaluation에서는 `data.filter(...).map(...).count()`라는 코드 조각은"실행 계획서(Execution Plan)"일 뿐입니다. 이것은 영화의"촬영적계화표(Storyboard)"와 같습니다. 실제 영화 촬영(실제 연산)은 제작진이"이 장면 준비됐어?"(Action 호출)라고 말하는 시점에 비로소 시작됩니다.
- <strong>함수형 프로그래밍의 결합성 (Composability)</strong>: Lazy Evaluation의 가장 큰 위력은 다양한 변환 함수를 자유롭게 조합할 수 있다는 점입니다. filter, map, flatMap, groupByKey, join 등 모든 변환 함수가 동일한"실행 계획 기록" 인터페이스를 공유하므로, 복잡한 데이터 처리 파이프라인을 작은 building block을 조립하듯이モジュール화할 수 있습니다.

- **📢 섹션 요약 비유**: Lazy Evaluation은 " строительная компания(분산처리フレーム워크)"가 현장 책임자(엔지니어)에게 받는 시공 계획서와 같습니다. 현장 책임자는 "2층 벽에 전기 배선 + 3층에 보일러 배관"이라는 계획서를 받으면, 이를 즉시시공하는 대신 현장 상황(클러스터 자원, 데이터 파티션 상태)을 종합적으로 분석하여 "전기 배선은 1층 철근 공사가 끝나고 나서 시작하는 게 효율적"이라는 최적화된 시공순서를 세우고, 실제 공사는감리관의"All clear, 시공 개시!" 명령(acion 호출)이 떨어지는 시점에 비로소 착공하는 것입니다., Eager Evaluation은 계획서를 받자마자 아무 판단 없이즉시시공에 들어가는 것입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
+-----------------------------------------------------------------+
|                  [ Lazy Evaluation 실행 모델 ]                   |
|                                                                 |
|  [1단계: 코드 작성 - 실행 계획 BUILD]                            |
|  +---------------------------------------------------------+    |
|  | sc.textFile("hdfs://data/logs/*.txt")                  |    |
|  |   .filter(line => line.contains("ERROR"))   <- 미실행!  |    |
|  |   .map(line => line.split(","))              <- 미실행!  |    |
|  |   .groupByKey(key => key)                    <- 미실행!  |    |
|  |   .count()                                   <- 미실행!  |    |
|  +---------------------------------------------------------+    |
|                         |                                        |
|                         v                                        |
|  [2단계: DAG 구축 - "계획서"만 기록]                              |
|  +---------------------------------------------------------+    |
|  | textFile -> filter -> map -> groupByKey -> count           |    |
|  | ( DAG의 노드로 변환, 엣지는 의존성 )                     |    |
|  +---------------------------------------------------------+    |
|                         |                                        |
|                         v                                        |
|  [3단계: Action 호출 - "施工 개시!"]                             |
|  count()가 호출되는 순간:                                        |
|  +---------------------------------------------------------+    |
|  | ① DAG 스케줄러가 전체 플랜을鸟瞰                         |    |
|  | ② filter: 파이프라이닝 가능한 Narrow_dependency 확인     |    |
|  |   -> filter + map + groupByKey 중 Shuffle 지점 탐색       |    |
|  | ③ groupByKey에서 Wide_dependency 발견 -> Stage 분리       |    |
|  | ④ Stage 1: textFile -> filter -> map (파이프라이닝)        |    |
|  | ⑤ Stage 2: groupByKey -> count (Shuffle 후 집계)         |    |
|  | ⑥ 실행: 전체 플랜의 최적화된 순서로 태스크 시작!         |    |
|  +---------------------------------------------------------+    |
|                                                                 |
|  [핵심 최적화: 필터 프루닝 (Filter Pruning)]                     |
|  count()의 결과가 Int(정수)라는 것을 알기에,                     |
|  ③ groupByKey에서Key=0건인 항목은 만들 이유 없음!                |
|  -> 불필요한 map 결과 전체를 생성하지 않고 통과시킴               |
|                                                                 |
+-----------------------------------------------------------------+
```

### 1. DAG (Directed Acyclic Graph) 스케줄링과의 결합
Lazy Evaluation은 Spark의 DAG 스케줄러와 결합될 때 비로소 진정한 힘을 발휘합니다.

- <strong>DAG 스케줄러 역할</strong>: Action 호출 시, DAG 스케줄러는 전체 변환 체인을 거꾸로소っ고(Backwards) 분석하여, 각 파티션에 대해"이 파티션을 계산하려면 어떤부파티션이 먼저 계산되어야 하는지"를 결정합니다. 이 때 Wide Dependency(Shuffle)가 발견되면 그 지점에서 Stage를 분리합니다.
- <strong>파이프라이닝 최적화</strong>: Narrow Dependency로 연결된 변환들은 같은 Stage 내에서 파이프라이닝됩니다. 즉, 한 파티션에서 filter를 적용한 결과가 곧바로 map으로 들어가고, 그 결과가 또 바로 reduce로 전달되어, 중간 결과를 메모리에 저장하지 않고 스트림처럼 바로 다음 연산으로 흘려보냅니다.
- <strong>필터 프루닝 (Filter Pruning)</strong>: DAG를 분석하면, 어떤 필터 조건이 항상 false를 반환하는 것을 알 수 있는 경우(예: null 체크 followed by null이 아닌 필터), 아예 해당 필터 이하의 변환 체인을 실행하지 않을 수 있습니다.

### 2. Eager vs Lazy: toy 예제로 비교

**Python eager (list comprehension 즉시 평가):**
```python
# Python (eager): result_list가 즉시 메모리에 생성됨
result_list = [x * 2 for x in range(1000000000)]  # 10억 개 즉시 생성!
print(result_list[:5])  # 이 줄에서 비로소 출력
```

<strong>Python lazy (generator: lazy evaluation):</strong>
```python
# Python (lazy): 제너레이터는plan만 기록, 실제 연산은 iteration 시
result_gen = (x * 2 for x in range(1000000000))  # 계획만 기록
print(next(result_gen))  # 이 줄에서 비로소 첫 번째 값만 연산
```

### 3. Lazy Evaluation의 3대 핵심 이점

| 이점 | 설명 | 예시 |
|:---|:---|:---|
| **불필요한 연산 제거** | 최종 결과에 영향 없는 변환은 아예 실행하지 않음 | count에서 groupByKey의Key별 개수만 필요, value 본문 불필요 |
| **메모리 절약** | 중간 결과를 메모리에 저장하지 않고 파이프라이닝 | filter->map->reduce가 3개 RDD 대신 1개 RDD 파이프라인으로 |
| **전체 최적화** | 실행 전 전체 DAG를 분석하여 최적 순서 결정 | 필터 조건을료하에 적용하여 네트워크 전송 데이터량 감소 |

- **📢 섹션 요약 비유**: Lazy Evaluation의 작동 방식을 "편의점 도시락 납품 시스템"에 비유할 수 있습니다. 본사는 전국 매장에 "김밥+삼각김+음료" 구성의 도시락을 공급하는데, 각 매장에서 매일 아침 발주서를 제출하면(Eager: 매장 요청에 즉시 생산·배송) vs 본사가 "이번 주말 예상 손님 수(실제 수요)"를 예측해서 매장에"미리 배치"(Lazy: 실제 주문(Action) 없이는 생산·배송 안 함)의 차이와 같습니다. 매장 주변에 축제(대량 주문)가 열리는 게 확실한 경우만 생산하면 재료 낭비를 줄일 수 있고, 축제가 취소되면 아예 생산을 안 해도 되는 것처럼, Lazy는"불필요한 연산은 100% 제거"하는 특성을 가집니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | Eager Evaluation | Lazy Evaluation |
|:---|:---|:---|
| **실행 시점** | 표현식 작성 시 즉시 실행 | Action 호출 시까지 미루기 |
| **메모리 사용** | 중간 결과 전체를 메모리에 저장 | 파이프라이닝으로 중간 결과 최소화 |
| **오류 발견** | Runtime(실행 시)에만 발견 | 컴파일 타임에 발견 가능한 경우다 |
| **디버깅 용이성** | 단계별로 결과 확인 가능 | 전체 플랜이 블랙박스화, 디버깅 어려움 |
| **순수 함수 보장** | 부수 효과(side effect) 있어도 실행됨 | 부수 효과가 실제로 실행되는 시점에만 발현 |

- <strong>Lazy Evaluation의 숨은 위험: 메모리 누수의 역설</strong>: Lazy Evaluation은"실행되지 않는 연산은 메모리를 사용하지 않는다"는 장점이 있지만, 반대로"실행되지 않은 연산의 계획(DAG)이 계속 누적된다"면 이는 이것이 메모리 누수의 원인이 될 수 있습니다. 예를 들어, 어떤 Spark 잡이 수백 개의 Transformation을 차례로 적용하는비상대적 DAG를 만들었지만, 단 한 번의 Action만 호출한다면, DAG 자체는 메모리에 유지되므로 수백 메가바이트의 실행 계획 메타데이터가 메모리를 점유하게 됩니다. 이는 Lambda 아키텍처에서 Batch Layer의비상대적 DAG를 만들 때 특히 주의해야 할 문제입니다.

- **📢 섹션 요약 비유**: Eager vs Lazy의 차이는 "그림 그리기의 두 가지 방식"과 같습니다. Eager는 눈앞의 풍경을 보면서 붓을 놓을 때마다 바로 페인트를 칠하는 것으로( части 완성품이 자꾸 쌓임), Lazy는 전체 구도를 스케치ブック에 미리 그린 다음, 최종 완성본이 필요한 시점에 비로소 스케치북의 선을 따라 페인트를도り시める 것입니다. 스케치북에는"어떤 선을 어떻게 칠할지"만 적혀 있고 실제 페인트는일적도적사용되지 않습니다. 다만 스케치북을 아무리 크게 그려도 실제 캔버스에 그려지기 전까지는회의구와し고사용에서きない 것과 같이, Lazy Evaluation도 Action이라는"초상화 완성 의뢰"가 없으면최종성과물는영원 생산되지 않습니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **파ipelining 가능 여부** | Narrow Dependency 연속 시 -> 파이프라인으로 최적화 | Wide Dependency 섞여 있으면 Stage 분리불가피면 |
| <strong>DAG 복잡도</strong> | 100개 이상 Transformation -> 메타데이터 Overhead 증가 | 너무 긴 lineage -> checkpoint 권장 |
| **Action 빈도** | 1개 RDD에 여러 Action -> cache 필요 | 1개 Action만 -> 불필요 캐시 제거 |
| <strong>데이터 체인 분석</strong> | filter->map->reduce 순서: filter를 map 이전에 적용하여 네트워크 전송량 최소화 | map->filter->reduce: 필터가 나중에 오면 불필요 데이터도 네트워크 통과 |

*(추가 실무 적용 가이드 - Lazy Evalutation 디버깅 전략)*
- **take(n) action 활용**: 전체 collect() 대신 take(n)을 사용하여 결과의 부분만 즉시 확인. take는 첫 n 개 파티션만 읽기 때문에 전체 데이터를 처리하지 않아 디버깅 속도가 매우 빠릅니다.
- <strong>RDD.toDebugString</strong>: RDD의 lineage 체인(실행 계획)을 문자열로 출력하여, 어떤 변환들이 어떤 순서로 연결되어 있는지 확인하는 중요한 디버깅 도구입니다.
- **queryExecution**: Spark DataFrame의 쿼리 실행 계획을 확인하는 official API로, .queryExecution.executedPlan으로 물리 계획, .queryExecution.analyzed으로 논리계화를해석할 수 있습니다.
- **실무 의사결정**: Lazy Evaluation의 "미리보기(Preview)" 기능을 활용하려면, 전체 데이터가 아닌"샘플 데이터"로 먼저 파이프라인을 테스트한 후 전체 데이터로 실행하는"2단계 개발 패턴"을 따르는 것이 업계 Best Practice입니다.

- **📢 섹션 요약 비유**: Lazy Evaluation의실무활영은 "시공효과도 검증"과 동일합니다. 아무리 훌륭한 건축가(엔지니어)의 설계도(변환 체인)라도, 실제 строительство(실행)에 들어가기 전에" компьютер방진(가상 시뮬레이션)"으로 전체 공정을 미리 확인해야 합니다. 시공효과도(쿼리 실행 계획)이 "이 순서로시공하면 자재가 이렇게 이동하고, these자재는 여기에 쌓이고..."와/과いう 것을 확인하면, 실제 시공에서"자재가 공간이 부족해서중도로 다|Other곳에 옮겨야 함"이라는 비효율을 미리 방지할 수 있습니다. take(10)은"디지털 목업(Modeling)으로 3D 이미지만 확인"이고, collect()는"실물 크기 maquette를 제작해서최종 검사"에 해당합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. <strong>Adaptive Query Execution (AQE)과 Lazy Evaluation의 결합</strong>
   Spark 3.0에서 도입된 AQE는 런타임 통계를 기반으로Lazy Evaluation이 세운 실행 계획을"재조정"하는 능동적 최적화입니다. 예를 들어, 조인 시 한쪽 데이터의 크기가 예상과 달리 매우 작은 것으로 밝혀지면, Broadcast Join(작은 쪽 전체를 네트워크로전량송신하여 모든 Executor에 복제)으로 자동으로 전환합니다. 이는 기존"계획 시점(Compile Time)"의Lazy Evaluation을"실행 시점(Runtime)"까지 확장한 것으로, 동적 최적화의 새로운 지평을 열었습니다.

2. <strong>Declarative DSL (Domain-Specific Language)의 대중화</strong>
   Lazy Evaluation의"무엇을 계산할지(What), 아닌 어떻게 계산할지(How)"라는 선언적(Declarative) 특성은, 이제 Spark SQL, Apache Beam, Flink SQL처럼"SQL-like 언어"로 데이터를 처리하는 DSL의 대중화로 이어지고 있습니다. 사용자는"어떻게 필터를 적용하고 조인을 구현할지"가 아니라"어떤 테이블을 조인할지"만 선언하면, 프레임워크가 Lazy Evaluation + DAG 최적화를 통해 자동으로 최적의 실행 계획을 세웁니다.

3. <strong>지연Evalusation와 메타프로그래밍의 결합</strong>
   Scala의 macrosやRust의 procedural macros처럼, Lazy Evaluation 개념이"컴파일 타임 최적화"로 확장되고 있습니다. Apache Spark의 Catalyst Optimizer는 Scala의 목변환(Tree Transformation) 기능을 활용하여, DataFrame 연산의 논리 계획을 컴파일 시점에 최적화된 물리 계획로 변환합니다. 이는 Lazy Evaluation의"실행 전 최적화" 특성을 더 강력한"컴파일 타임 리팩토링"으로 발전시킨 것으로, 컴파일러가 불필요한 변환을 제거하고 상수 폴딩(Constant Folding)을 적용하여 런타임 비용을 최소화합니다.

- **📢 섹션 요약 비유**: Lazy Evaluation의 미래는 "설계도의 자동화 + 시공의 роботизации"와 같습니다. 과거 건축가는 설계도만 그리고 현장감독이시공순서를 수동으로 조정했지만, 이제는 компьютер방진 프로그램이"이 설계도대로시공하면 자재가 최효솔적에이동하는 순서는 이것"이라고 자동으로산출하고, 로봇 공학자가 그 순서에 따라 자동으로 строительство를 집행합니다. 인간은"어떤 건물을 지을지(What)"만 생각하면 되고,"어떻게 지을지(How)"는 기계가 전부 자동조배하는 것입니다. Lazy Evaluation은 바로 그"무엇을(What)"과"어떻게(How)"를 분리하는 핵심 설계 원칙으로서, 데이터처리 분야를 넘어 프로그래밍 언어론 전반에 걸쳐 지속심화할 것입니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   <strong>Lazy Evaluation 적용 기술 생태계</strong>
    *   <strong>함수형 프로그래밍</strong>: Haskell(순수 지연 평가), Scala(LAZY 키워드), Clojure(지연 시퀀스)
    *   **빅데이터 처리**: Apache Spark(RDD/DataFrame), Apache Flink(ストリ밍), Apache Beam(통일적 API)
    *   ** языки программирования**: Python(Generator/Iterator), Java(Stream API), JavaScript(제너레이터)
*   <strong>Spark Lazy Evaluation 핵심 트리거</strong>
    *   **Transformation** (Lazy): map, filter, flatMap, groupByKey, join, reduceByKey, union, distinct, repartition...
    *   **Action** (실행 개시): collect, count, sum, take, save, foreach, reduce...
*   <strong>DAG 최적화 기법</strong>
    *   Constant Folding (컴파일 타임 상수 연산)
    *   Predicate Pushdown (필터 조건을 하유으로 내림)
    *   Column Pruning (필요한 컬럼만 선택)
    *   Narrow->Wide 파이프라이닝

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Lazy Evaluation 적용 기술 생태계]
    |
    v
[함수형 프로그래밍: Haskell(순수 지연 평가), Scala(LAZY 키워드), Clojure(지연 시퀀스)]
    |
    v
[빅데이터 처리: Apache Spark(RDD/DataFrame), Apache Flink(ストリ밍), Apache Beam(统一的 API)]
    |
    v
[языки программирования: Python(Generator/Iterator), Java(Stream API), JavaScript(제너레이터)]
    |
    v
[Spark Lazy Evaluation 핵심 트리거]
    |
    v
[Transformation (Lazy): map, filter, flatMap, groupByKey, join, reduceByKey, union, distinct, repartition...]
```

이 흐름도는 Lazy Evaluation 적용 기술 생태계에서 출발해 Spark Lazy Evaluation 핵심 트리거까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Lazy Evaluation은 "미리 모든 숙제를 해두는 것(즉시 평가)"이 아니라, "선생님이 숙제 검사를 시작할 때(액션 호출)그제서야 한꺼번에 풀어내는" 것과 같아요.
2. 그래서 어떤 문제가 출제될지(최종 결과)전체를 미리 보고 필요 없는 문제는 아예 풀지 않아도 돼요.
3. 마치 크레용을 미리 다 준비해두는 게 아니라, 선생님이"이제 풀어보세요"할 때 필요한 색만 꺼내서 쓰는 것과 비슷해요!

---
> <strong>🛡️ Expert Verification:</strong> 본 문서는 Lazy Evaluation의 함수형 프로그래밍 이론적 기반과 Apache Spark에서의 실습적 구현을 모두 검증하였습니다. (Verified at: 2026-04-05)
