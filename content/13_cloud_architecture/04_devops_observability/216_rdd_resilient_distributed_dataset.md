---
title: "RDD (Resilient Distributed Dataset)"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 216
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RDD(Resilient Distributed Dataset)는 Spark의 핵심 추상화로, 클러스터 전체에 분산된 '불변(Immutable)' 데이터 모음이며, 장애 시 계보(Lineage)를 역추적하여 잃어버린 파티션을 자동으로 재계산하는 내결함성 메커니즘을 내장한다.
> 2. **가치**: 데이터를 직접 복제하지 않고 "어떻게 생성됐는지"(변환 계보)를 기록하는 방식으로 내결함성을 구현하여, HDFS의 3벌 복제 대비 저장 오버헤드 없이 분산 데이터를 보호한다.
> 3. **판단 포인트**: RDD는 저수준 API로 유연하지만 최적화가 어렵다. 현대 Spark에서는 DataFrame/Dataset API를 우선 사용하고, 세밀한 제어가 필요할 때만 RDD를 직접 사용하는 것이 권장된다.

---

## Ⅰ. 개요 및 필요성

Spark를 설계할 때 Matei Zaharia가 직면한 문제는 두 가지였다: 1) 메모리에 데이터를 유지하는 것은 빠르지만 <strong>메모리는 휘발성</strong>이라 장애 시 데이터가 사라진다. 2) 기존 공유 메모리 시스템은 세밀한 업데이트를 지원하지만 <strong>분산 환경에서 내결함성 구현이 복잡</strong>하다.

RDD는 이 두 문제에 대한 우아한 해결책이다: <strong>데이터를 복제하는 대신 변환 과정을 기록한다.</strong> RDD A에서 map() 연산으로 RDD B가 생성됐다면, 이 관계(Lineage)를 DAG(Directed Acyclic Graph)로 기록한다. 노드 장애로 RDD B의 일부가 유실되면, Lineage를 따라 원본 RDD A에서 해당 파티션만 재계산한다.

RDD라는 이름은 세 가지 특성에서 왔다: **Resilient**(탄력적: 장애 시 자동 복구), **Distributed**(분산: 클러스터 전체에 파티션 분산), **Dataset**(데이터셋: 실제 데이터의 컬렉션).

📢 **섹션 요약 비유**: RDD의 Lineage 기반 복구는 레시피를 기억하는 것과 같다. 완성된 케이크(RDD B)가 엎질러지면, 레시피(Lineage)를 보고 재료(원본 RDD A)부터 다시 만들 수 있다. 케이크를 여러 개 복사해두는 것(3벌 복제)보다 레시피 한 장이 더 경제적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### RDD 주요 특성

| 특성 | 설명 |
|:---|:---|
| <strong>Immutable</strong> (불변) | 생성 후 수정 불가, 변환 시 새 RDD 생성 |
| **Distributed** (분산) | 클러스터 여러 노드에 파티션으로 분산 |
| <strong>Lazy Evaluation</strong> | 액션 호출 전까지 변환 연산 실행 안 됨 |
| **Fault Tolerant** | Lineage DAG로 장애 시 자동 재계산 |
| **In-Memory** | 기본적으로 메모리에 유지 (성능 핵심) |

### RDD 연산 유형

```
RDD 연산 두 가지:

1. 트랜스포메이션 (Transformation) - 새 RDD 반환, 지연 실행
   +-----------------------------------------------------+
   | map(f)      : 각 원소에 함수 f 적용                  |
   | filter(f)   : 조건 f를 만족하는 원소만 선택           |
   | flatMap(f)  : map + 중첩 해제                        |
   | groupByKey(): 같은 키로 그룹화                       |
   | reduceByKey(): 같은 키의 값들을 집계                  |
   | join()      : 두 RDD를 키로 조인                     |
   | distinct()  : 중복 제거                              |
   +-----------------------------------------------------+

2. 액션 (Action) - 즉시 실행, 결과 반환
   +-----------------------------------------------------+
   | count()     : 원소 수 반환                           |
   | collect()   : 모든 원소를 드라이버로 수집             |
   | first()     : 첫 번째 원소 반환                      |
   | take(n)     : 처음 n개 원소 반환                     |
   | reduce(f)   : 모든 원소를 f로 집계                   |
   | saveAsTextFile(): 파일로 저장                        |
   +-----------------------------------------------------+
```

### Lineage DAG 예시

```
  textFile("input.txt")     <- RDD[String] (원본)
         | map(split)
         v
  flatMap(words)             <- RDD[String] (단어 리스트)
         |
         v map(word -> (word,1))
  pairRDD                   <- RDD[(String, Int)]
         |
         v reduceByKey(_+_)
  wordCount                 <- RDD[(String, Int)] (결과)
         |
         v saveAsTextFile()  <- 액션! 이 시점에 전체 DAG 실행
```

### RDD Python 코드 예시

```python
sc = spark.sparkContext

# RDD 생성
rdd = sc.textFile("s3://mybucket/data.txt")

# 트랜스포메이션 (지연 실행 - 아직 실행 안 됨)
words = rdd.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)

# 액션 (이 시점에 전체 파이프라인 실행)
result = counts.collect()  # 드라이버로 수집
counts.saveAsTextFile("s3://mybucket/output")  # 저장

# 자주 사용하는 RDD는 캐시
counts.cache()
counts.count()  # 첫 액션 시 캐시에 저장
counts.count()  # 두 번째 호출은 캐시에서 즉시 반환
```

📢 **섹션 요약 비유**: RDD의 트랜스포메이션과 액션은 요리 주문과 조리의 관계다. 트랜스포메이션은 레시피 작성(재료 준비, 조리 순서 계획)이고, 액션은 실제 요리 시작이다. 주문이 들어오기(액션) 전까지는 준비만 하고 실제 조리는 하지 않는다(Lazy).

---

## Ⅲ. 비교 및 연결

### RDD vs DataFrame vs Dataset

| 항목 | RDD | DataFrame | Dataset |
|:---|:---|:---|:---|
| Spark 버전 | 1.x | 2.x | 2.x |
| 언어 | Python/Scala/Java | Python/Scala/Java | Scala/Java 전용 |
| 스키마 | 없음 (비정형) | ✅ (컬럼명+타입) | ✅ (타입 안전) |
| Catalyst 최적화 | ❌ | ✅ | ✅ |
| Tungsten 메모리 | ❌ | ✅ | ✅ |
| 성능 | 낮음 | 높음 | 높음 |
| 사용 권장 | 저수준 제어 필요 시 | 구조화 데이터 | 타입 안전 필요 시 |

📢 **섹션 요약 비유**: RDD->DataFrame->Dataset의 진화는 메모 지->엑셀 스프레드시트->데이터베이스 테이블의 진화와 같다. 메모지는 자유롭지만 검색이 어렵고, 엑셀은 컬럼이 있어 분석이 쉬우며, DB는 타입 검증까지 된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>RDD 직접 사용이 필요한 상황</strong>:
```python
# 1. 비구조화 데이터 처리
rdd = sc.textFile("s3://raw-logs/*.log")
parsed = rdd.map(lambda line: parse_custom_format(line))

# 2. 저수준 파티셔닝 제어
rdd_partitioned = rdd.partitionBy(numPartitions=200,
                                   partitionFunc=custom_hash)

# 3. 외부 라이브러리와 통합
rdd.mapPartitions(lambda records:
                  process_with_native_lib(records))

# 4. 장시간 실행 중 체크포인팅 (Lineage 절단)
rdd.checkpoint()  # Lineage가 너무 길어질 때 중간 저장
```

<strong>DataFrame API 우선 사용 권장</strong>:
```python
# DataFrame API: Catalyst 옵티마이저가 자동 최적화
df = spark.read.parquet("s3://mybucket/data/")
result = df.filter(df.age > 30) \
           .groupBy("department") \
           .agg({"salary": "avg"}) \
           .orderBy("avg(salary)", ascending=False)
result.show()
```

**실무자 판단 포인트**:
- Lineage가 매우 길어지면(수십 단계의 트랜스포메이션) 장애 시 재계산 시간이 길어진다. `checkpoint()`로 중간 결과를 디스크에 저장하여 Lineage를 절단한다.
- `collect()`는 전체 RDD를 드라이버 메모리로 가져오므로, 대용량 데이터에 사용 시 OutOfMemoryError 발생. 결과가 큰 경우 `take(n)` 또는 `saveAsTextFile()` 사용.
- Spark 3.x에서 DataFrame과 Dataset은 내부적으로 동일 (Dataset[Row] = DataFrame).

📢 **섹션 요약 비유**: checkpoint()는 긴 게임 세이브 포인트와 같다. 너무 오래 진행하다가 죽으면 처음부터 다시 해야 하므로(Lineage 재계산), 중간에 세이브(checkpoint)해두면 그 지점부터 다시 시작할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 내결함성 | Lineage 기반 자동 복구, 복제 비용 없음 |
| 유연성 | 모든 데이터 타입, 커스텀 로직 처리 가능 |
| 분산 처리 | 수천 노드에 자동 파티션 분배 |
| 메모리 최적화 | cache()/persist()로 반복 처리 최적화 |

RDD는 Spark의 철학을 가장 순수하게 담은 추상화다. "불변 + 변환 계보"라는 두 원칙이 분산 시스템의 복잡한 내결함성 문제를 우아하게 해결한다. DataFrame/Dataset이 대부분의 경우를 커버하지만, RDD의 원리를 이해해야 Spark의 본질을 파악할 수 있다.

📢 **섹션 요약 비유**: RDD는 Spark의 DNA다. 눈에 보이는 것은 DataFrame이지만, 그 안에는 RDD의 원리가 흐른다. DataFrame을 잘 쓰려면 RDD를 이해해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Lineage (계보) | RDD 내결함성의 핵심 메커니즘 |
| 지연 평가 (Lazy Evaluation) | 트랜스포메이션이 즉시 실행되지 않는 이유 |
| DataFrame / Dataset | RDD를 기반으로 한 고수준 스키마 기반 API |
| DAG (Directed Acyclic Graph) | Spark가 실행 계획을 표현하는 방식 |
| checkpoint() | 긴 Lineage를 절단하여 복구 시간 단축 |
| Catalyst Optimizer | DataFrame이 RDD보다 빠른 이유 (자동 최적화) |

### 👶 어린이를 위한 3줄 비유 설명

1. RDD는 레시피를 기억하는 요리책처럼, 데이터가 어떻게 만들어졌는지 기록해둬서 잃어버려도 다시 만들 수 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
RDD: 불변 · 분산 · 지연 평가 · Lineage 기반 복구
    |
    v
DataFrame / Dataset: 스키마 기반 · Catalyst 최적화
    |
    v
Spark SQL: SQL 인터페이스 + Predicate Pushdown
```
2. 트랜스포메이션은 레시피 적기(아직 안 만들었어), 액션은 실제 요리 시작이야. 손님 주문이 와야(액션) 요리를 시작해.
3. 자주 쓰는 결과는 cache()로 저장해두면, 매번 처음부터 만들 필요 없이 이미 만들어진 것을 바로 꺼내 쓸 수 있어.
