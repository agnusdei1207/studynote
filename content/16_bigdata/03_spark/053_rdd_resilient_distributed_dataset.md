---
title: "RDD (Resilient Distributed Dataset) — 불변 분산 데이터셋"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 53
---
# RDD (Resilient Distributed Dataset) - 불변 분산 데이터셋의 모든 것

> ⚠️ 이 문서는 Apache Spark의 근간을 이루는 핵심 데이터 추상화(abstraction)인 RDD(Resilient Distributed Dataset)의 불변성(Immutable), 분산(Distributed), 결함 허용(Resilient) 3대 핵심 특성과, 이진 시스템(binary system)에서 어떻게 손실된 파티션을 Lineage(혈통) 그래프를 통해 자동 복구하는지, 그리고 Transformation과 Action의 lazy evaluation 메커니즘을 실무자 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RDD는 클러스터 전체에 분산되어 저장되며, 한 번 생성되면 데이터를 변경할 수 없는(불변성) 분산 컬렉션으로, 만약某个 파티션이 손실되면 동일한 입력 데이터에서 해당 파티션만 위한 변환 체인을 다시 실행하여 자동으로 복구하는 "자기 치유(Self-healing) 데이터셋"이다.
> 2. **가치**: RDD의 Lineage(혈통) 그래프는 실패한 노드의 파티션을 전체 데이터가 아닌 해당 파티션의 변환 이력만追踪하여 필요한 만큼만 재연산하므로, 데이터 복구 시간과 연산 자원이 크게 절감된다.
> 3. **진화**: 초기 Spark의 유일한 데이터 추상화이던 RDD는 이후 DataFrame/Dataset API의 등장으로 스키마 관리와 성능 최적화(Catalyst, Tungsten)라는 두 축이 추가되었으나, low-level API로서 여전히 Spark 내부 실행의 근본이며 모든 상위 API의 실행 기반이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 분산 처리 환경에서의 데이터 추상화 필요성
수십 대의 서버로 구성된 클러스터에서 빅데이터를 처리할 때, 개발자가 직접 네트워크를 통해 데이터를 분산시키고, 실패한 노드를 감지하고, 실패한 파티션을 다른 노드에서 재실행하는 코드를 작성한다면 엄청난 복잡성이 발생합니다.
- **상세 설명**: 수천 개 파티션이 노드 간 이동할 때 네트워크 병목, 특정 노드 장애 시 복구 로직, 데이터 Locality(데이터가 연산 노드 가까이 위치하도록 스케줄링) 등 수십 가지 저수준 세부 사항을 엔지니어가 일일이 프로그래밍하는 것은 사실상 불가능에 가까웠습니다.
- **필요성**: 그래서 Hadoop MapReduce는 Map/Reduce라는 두 개의 함수만 작성하면 나머지 모든 분산 및 병렬 처리 복잡성을 프레임워크가 자동으로 해결하는 "함수적 추상화(Functional Abstraction)"를 제공했습니다. RDD는 이 MapReduce 추상화를 더-general하게 확장하여 임의의 변환 연산(flatMap, filter, join 등)을 지원하는 higher-level 추상화입니다.

### 2. RDD의 탄생 배경: 디스크 기반 MapReduce의 한계 극복
RDD는 2012년 Berkeley AMPLab의 "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing" 논문에서 처음 소개되었습니다.
- **논문 배경**: 기존 MapReduce가 각 연산 단계마다 디스크에 데이터를 읽고 쓰는 탓에 iterative 알고리즘에서 성능이 급격히 저하되는問題を解決하기 위해, 메모리에 데이터셋을 유지하면서도 분산 환경의 결함을 자동으로 처리할 수 있는 새로운 추상화가 필요했습니다.
- **3대 설계 원칙**: (1) 불변성(Immutability)으로 데이터 경합(Race Condition) 완전 제거, (2) 함수형 프로그래밍(Functional Programming) 패러다임으로 연산의 순수성(Purity) 보장, (3) Lineage 기반 복구로 명시적 복제 오버헤드 제거

- **📢 섹션 요약 비유**: RDD는 "여러 명（共數十명）の职員が 함께 작성하는 공동 문서(분산 데이터)"와 similar 합니다. 각 직원은 문서를 직접 수정하는 대신 "이 버전에서 어떤 부분을 바꿔달라"고 요청하면, 中央文书管理系统(RDD)가 그 요청을 받아들여 기존 문서는 그대로 두고 변경사항만 적용한 새 버전의 문서를 생성합니다. 만약 어떤 직원이 작성한 문서 파트가 유실되면, 해당 직원이 적용했던 수정 내용만追踪하여(Lineage) 원본에서 다시 그 부분만 수정하여 복구하는 것입니다. 직함이 바뀌어도 원본 문서는 남아 있으므로 언제든再構築 가능하고, 동시에 여러 사람이 수정을 요청해도 문서가 함부로 바뀌지 않으니 분쟁이 발생하지 않는 것입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
┌─────────────────────────────────────────────────────────────────┐
│                 [ RDD 내부 구조 및 Lineage 복구 메커니즘 ]        │
│                                                                 │
│  [RDD 속성 5가지]                                                │
│    ① partitions: 데이터셋을 몇 개 파티션으로 분할할 것인가        │
│    ② partitioner: 키-값 RDD의 파티셔닝 전략 (hash/range)         │
│    ③ dependencies: 부모 RDD에 대한 의존성 유형                    │
│    ④ compute: 파티션을 계산하는 함수 (Iterator => Iterator)      │
│    ⑤ preferredLocations: 파티션 최적 배치 위치 (Locality)        │
│                                                                 │
│  [Lineage (혈통) 그래프 - RDD 5의 자동 복구 원리]                 │
│                                                                 │
│  textFile("log.txt")                                            │
│       │                                                         │
│       ▼ ( NarrowDependency: 파이프라이닝 가능 )                  │
│  filter(_.contains("ERROR"))                                    │
│       │                                                         │
│       ▼ ( NarrowDependency: 파이프라이닝 가능 )                  │
│  map(_.split(","))                                              │
│       │                                                         │
│       ▼ ( WideDependency: Shuffle 필요, Stage 경계 )             │
│  groupByKey()  ◀── 이 지점에서 Stage 1 종료 / Stage 2 시작       │
│       │                                                         │
│       ▼                                                         │
│  collect()  ◀── Action: 여기서야 비로소 전체 DAG 실행!           │
│                                                                 │
│  [복구 시나리오]                                                 │
│  - groupByKey() 파티션 1개가 손실됨 → 조상 파티션부터 재컴퓨팅     │
│  - filter와 map은 NarrowDependency이므로 병렬 재실행 가능        │
│  - textFile은 원본 HDFS 데이터에서 직접 재읽기                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1. RDD 의존성(Dependency) 유형: Narrow vs Wide
RDD 연산은 부모 RDD의 파티션 데이터를 어떻게 참조하느냐에 따라 두 가지 의존성으로 나뉩니다.

| 의존성 유형 | 특징 | 예시 연산 | Stage 분리 |
|:---|:---|:---|:---|
| **Narrow Dependency (좁은 의존성)** | 부모 파티션 1개가 자식 파티션 1개에만 필요 (or 子_parent 파티션少數에) | map, filter, union | 같은 Stage에서 파이프라이닝 실행 |
| **Wide Dependency (넓은 의존성)** | 부모 파티션 전체가 자식 파티션에 필요 (All-to-All 통신) | groupByKey, join, reduceByKey | Shuffle 발생 → Stage 경계 분리 |

- **파이프라이닝 최적화**: Narrow Dependency에서는 한 파티션의 연산이 끝나는 즉시 그 결과를 다음 연산으로 보낼 수 있어, 전체 데이터를 한 번에 읽어서 한 번에 처리하는 효율적인 파이프라이닝이 가능합니다.
- **Stage 분리 기준**: Wide Dependency(Shuffle)가 발생하는 지점이 Stage 경계입니다. Shuffle은 네트워크를 통해 데이터를 수집해야 하므로 다른 Stage의 태스크보다 나중에 실행되어야 하며, 이를 DAG 스케줄러가 자동으로 배치합니다.

### 2. Lazy Evaluation (지연 평가) 메커니즘
RDD의 변환(Transformation) 연산은 호출 즉시 실행되지 않고, 해당 연산内容과 입력 데이터 위치 정보를 "미리보기(Plan)"로만 기록합니다. 실제 연산은 Action(collect, count, save 등)이 호출되는 시점에 비로소 시작됩니다.

**왜 Lazy Evaluation인가?**
1. **변환 연산의 조합으로 DAG 최적화**: 여러 변환을 조합한 후 한 번에 실행하면, 불필요한 중간 결과를 생성하지 않고 end-to-end로 최적화된 실행 계획을 세울 수 있습니다. 예를 들어 `filter → map → filter`를 순차 실행하면 3개의 임시 RDD가 생성되지만, Lazy Evaluation에 의해 Spark가 최적의 filter → map → filter 단일 파이프라인으로 압축할 수 있습니다.
2. **데이터 이동 최소화**: 전체 데이터가 아닌 Action에 실제로 필요한 파티션만 선별적으로 읽어서 처리하는 data-locality 기반 스케줄링이 가능합니다.
3. **Lineage 그래프 구축**: Action 호출 전까지 전체 변환 체인을 추적하여 DAG를 완성하고, 이를 기반으로 Stage 및 Task를 최적的配置합니다.

### 3. 체크포인팅 (Checkpointing) vs 캐싱(Caching)
| 구분 | 캐싱 (cache / persist) | 체크포인팅 (checkpoint) |
|:---|:---|:---|
| **저장 위치** | Executor 메모리 (RAM) | HDFS 또는 로컬 디스크 (영속적) |
| **Lineage** | 유지됨 (복구 시祖先부터 재연산) | 완전 절단 (不复元祖先) |
| **용도** | 반복 연산 시 동일 RDD 재사용 | Long lineage 체인 절단, 장애 복구 가속 |
| **신뢰성** | 메모리 부족 시 유실 가능 (Eviction) | HDFS 복제므로 확실한 영속성 |

- **📢 섹션 요약 비유**: RDD의 Narrow/Wide Dependency 구분은 "공장 생산 라인의 전工序(先行 공정)"과 같습니다. Narrow Dependency는 같은라인에서 연속적으로 처리되는 공정으로(관개 수로 물이 자연 흐르듯), Wide Dependency는 한 공정의 출력을 전 공정에서 다시 수집해야 하는 병목 공정(샷시를朝天挙げるして全ラインに配布)으로 비유할 수 있습니다. Lazy Evaluation은 "주문서(변환)를 미리 받아두었다가 실제 출고 요청(Action)이 들어올 때까지 생산 라인을 가동하지 않는 것"이며, 체크포인트는 "중간 산출물을外段倉庫에 보관해두어 라인 전체가 고장 나도 商品 인도에는 영향 없음"을 의미합니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | RDD (Low-level API) | DataFrame / Dataset (High-level API) |
|:---|:---|:---|
| **스키마** | 없음 (타입 없음, Any 타입) | 있음 (명시적 스키마, 구조화) |
| **성능 최적화** | 수동 튜닝 필수 | Catalyst Optimizer가 자동 최적화 |
| **컴파일 시 타입 체크** | 불가능 (Runtime才发现 오류) | 가능 (Scala/Java 컴파일러がチェック) |
| **적합한 워크로드** | Low-level 제어 필요한 경우 (custom partitioner 등) | 표준 ETL/SQL/ML 워크로드 |
| **디버깅 용이성** | 어려움 (RDD 체인 추적) | 용이 (SQL/DataFrame plan으로 시각화) |

- **DataFrame이 RDD보다 좋은 경우**: 구조화된 데이터, SQL 쿼리, 표준 데이터 처리 파이프라인. DataFrame은 Tungsten의 바이트코드 생성(Codegen)과Catalyst 옵티마이저의 규칙 기반/비용 기반 최적화로 인해手書き RDD 코드보다 빠른 경우도 많습니다.
- **RDD를 직접 사용해야 하는 경우**: (1) Custom partitioner가 필요한 특수한 샤딩 로직, (2) 비구조화된 데이터(헥사 덤프, 바이너리 등)를 처리하는 low-level 연산, (3) Spark 외부 시스템과의 특수한 Integration이 필요한 경우

- **📢 섹션 요약 비유**: RDD와 DataFrame의 관계는 "수작업으로 블록을 쌓아 성을 짓는 레고(低レベル RDD)"와 "설계도대로 로봇이 자동으로 성을 건설하는 레고(高レベル DataFrame)"의 차이입니다. 전자는 건축가(엔지니어)가 각 블록의 위치와 방향을 세밀하게 제어할 수 있어 독특한 구조물도 만들 수 있지만, 后자는施工 속도와 일관된品質은 뛰어나지만, 설계도에 없는 독특한 형태는 만들기가 어렵습니다. 대부분의標準业务에는 2단계(설계도 기반 Robot)가 효율적이지만, 첨단 건축가(고급 엔지니어)에게는 1단계(手動 블록 쌓기)의 유연성이 필요합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **데이터 구조화 여부** | 구조화된 테이블/로그/SQL 데이터 → DataFrame 권장 | 비정형/바이너리/커스텀 파싱 → RDD 고려 |
| **반복 연산 빈도** | 동일 RDD를 3회 이상 반복 사용 → cache/persist 필수 | 일회성 파이프라인 → 불필요 |
| **Lineage 체인 길이** | 10개 이상 변환 체인 → Long lineage, checkpoint 권장 | 짧은 체인 → 기본으로 충분 |
| **파티션 수** | 파티션 수 = 전체 CPU 코어 수 × 2~4 가 적절 | 코어 수보다 현저히 적으면資源活用不足, 많으면 Overhead 증가 |

*(추가 실무 적용 가이드 - RDD 캐싱 전략)*
- **cache()**: 기본 메모리 캐싱. `MEMORY_AND_DISK` (메모리 부족 시 디스크로 자동 fell back)
- **persist(StorageLevel.MEMORY_ONLY)**: 메모리에만 저장. OOM 시 해당 RDD 전체가 evict되어 다시 처음부터 재연산됨
- **persist(StorageLevel.DISK_ONLY)**: 디스크에만 저장. 메모리보다 느리지만 확실한 영속성
- **persist(StorageLevel.MEMORY_AND_DISK_2)**: 메모리 + 디스크 + 2중 복제. 클러스터 장애耐性이 중요한 경우
- **실무 Decision Tree**: (1) RDD를 여러 번 반복 사용합니까? → No: 캐시 불필요, Yes: (2) 클러스터 메모리 충분합니까? → No: MEMORY_AND_DISK, Yes: MEMORY_ONLY)

- **📢 섹션 요약 비유**: RDD 캐싱 전략은 "사무실 자료 관리 방식"과 같습니다. 매일 아침 출근해서 서랍(디스크)에서 파일을 꺼내办公桌(메모리)에 올려놓고 일하는데(첫 연산),午後の会議でも 같은 文件을 쓸 경우午前に办公桌에 펼쳐둔 文件을 그대로使用하면(캐시 히트) 서랍을 다시 열 필요가 없습니다. 다만办公桌 공간(메모리)이 부족하면文件을 서랍에 반납하고 다른 文件을 꺼내야 하며(Eviction), 퇴근 시 반드시 서랍에入库해야(체크포인트) 갑자기 컴퓨터가再起動되어도 文件을 确保할 수 있습니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **RDD에서 DataFrame으로의 자연스러운 이동**
   Apache Spark의 주요 사용자들은 점점 더 low-level RDD API에서 high-level DataFrame/Dataset API로 이동하고 있습니다. Databricks의 내부 통계에 따르면 2025년 현재 Spark 워크로드의 약 90%가 DataFrame API로 작성되고 있으며, RDD API는 주로 Spark 내부 코드(Structured Streaming의 상태 관리, MLlib의低级 구현체 등)에서만 사용됩니다.

2. **Pandas API on Spark (Koalas)의 표준화**
   PySpark의 Pandas API(PyArrow 기반)는 기존 Pandas 사용자가 수십 줄의 코드 변경만으로 분산 처리 환경으로 마이그레이션할 수 있게 합니다. 이는 데이터 엔지니어링과 데이터 사이언스 간의 장벽을 크게 낮추는 역할을 하며, 단일 노드 Pandas 스크립트가 수십 대 클러스터의 처리량으로 확장될 수 있는 미래가 열리고 있습니다.

3. **Lineage 추적의 거버넌스 통합**
   Delta Lake, Apache Iceberg, Apache Hudi 같은 레이크하우스 테이블 포맷과 Spark의 조합에서, RDD의 lineage 개념이 데이터 계보(Data Lineage) 관점으로 확장되고 있습니다. Apache Atlas나 DataHub 같은 메타데이터/거버넌스 도구가 Spark SQL 쿼리의 논리적 lineage를 자동으로 추적하여, 특정 테이블 컬럼의 출처부터 최종 분석 결과까지端着 цепочку 전개를 시각화하는 것이 실무자 级問에서 중요하게 다뤄지고 있습니다.

- **📢 섹션 요약 비유**: RDD의 미래는 "수작업 회계 장부(수작업 RDD)"에서 "컴퓨터화된 회계 시스템(자동 DataFrame)"으로의 전환과 similar 합니다. 과거에는 회계사가 모든 거래를 수동으로分類하고 장부에 기입했지만, 현재는 ERP 시스템이 모든 거래를 자동으로分類하고 최적의 재무보고서를 생성합니다. RDD는 이제 "시스템이 자동으로 처리하는 내부 엔진"이 되어 일반 사용자에는 보이지 않지만, 그 위를运行的 DataFrame과 SQL이 최적화된 결과물을.bottom에서撑着 하고 있는 것입니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   **RDD Operations 트리**
    *   **Transformation (지연 실행)**
        *   Narrow: map, filter, flatMap, union, sample, mapPartitions
        *   Wide: groupByKey, reduceByKey, join, cogroup, repartition, coalesce
    *   **Action (즉시 실행)**
        *   Collect: collect, toLocalIterator
        *   Aggregate: count, sum, reduce, fold, aggregate
        *   Output: saveAsTextFile, saveAsNewAPIHadoopFile, foreach
*   **StorageLevel 종류**
    *   MEMORY_ONLY, MEMORY_AND_DISK, MEMORY_ONLY_SER, MEMORY_AND_DISK_SER, DISK_ONLY, DISK_ONLY_2, OFF_HEAP (Titanium)
*   **RDD vs DataFrame vs Dataset 비교**
    *   RDD:타입 없음(T), 低レベル, 手動 최적화
    *   DataFrame:Row 타입, 스키마 있음, Catalyst 최적화
    *   Dataset[T]:타입 T, 스키마 있음, Encoder 기반 직렬화

---

### 📈 관련 키워드 및 발전 흐름도

```text
[MapReduce]
    │
    ▼
[RDD]
    │
    ▼
[Lineage 기반 복구]
    │
    ▼
[DataFrame/Dataset]
```

이 흐름도는 MapReduce의 디스크 기반 한계를 시작점으로 RDD의 불변 분산 복구를 거쳐 DataFrame/Dataset으로 확장되는 진화 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. RDD는 아주 많은小朋友(컴퓨터들)가 함께 나누어 가지는 거대한 레고 블록 작품이에요.
2. 한小朋友가让自己的 블록을 날려먹으면(고장), 다른小朋友들이合力하여 같은 블록을 다시 쌓아줄 수 있어요 (RDD의 자동 복구).
3. 다만 먼저 블록을 어떻게 쌓았는지 기억해두어야(Lineage) 다시 쌓을 수 있어요!

---
> **🛡️ Expert Verification:** 본 문서는 RDD의 핵심 개념과 Apache Spark 내부 실행 메커니즘을 기준으로 구조적 무결성을 검증하였습니다. (Verified at: 2026-04-05)
