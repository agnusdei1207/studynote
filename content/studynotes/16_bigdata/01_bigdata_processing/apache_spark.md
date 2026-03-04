+++
title = "Apache Spark (아파치 스파크)"
description = "인메모리 기반의 초고속 분산 데이터 처리 엔진, 스파크의 아키텍처와 최적화 원리"
date = 2024-05-24
[taxonomies]
tags = ["Big Data", "Spark", "In-memory", "Distributed Computing", "RDD"]
+++

# Apache Spark (아파치 스파크)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 스파크는 하둡 맵리듀스(MapReduce)의 디스크 I/O 병목을 극복하기 위해 제안된 **인메모리(In-memory) 기반 분산 데이터 처리 엔진**으로, DAG(Directed Acyclic Graph) 스케줄링을 통해 연산 경로를 최적화합니다.
> 2. **가치**: 반복적인 머신러닝 알고리즘이나 실시간 스트리밍 분석에서 하둡 대비 최대 100배 빠른 성능을 제공하며, 단일 엔진에서 SQL, 스트리밍, 그래프 연산을 모두 지원하는 통합(Unified) 플랫폼의 가치를 실현합니다.
> 3. **융합**: 데이터 레이크하우스(Data Lakehouse)의 핵심인 Delta Lake, Apache Iceberg와 결합하여 정형/비정형 데이터의 ACID 트랜잭션을 보장하고, AI 프레임워크와의 연동을 통해 빅데이터 분석의 표준으로 자리잡았습니다.

---

### Ⅰ. 개요 (Context & Background)

아파치 스파크(Apache Spark)는 대규모 데이터 처리를 위해 설계된 오픈소스 분산 컴퓨팅 프레임워크입니다. 2009년 UC 버클리 대학의 AMPLab에서 개발된 스파크는 "데이터를 디스크가 아닌 메모리에 두고 처리하자"는 단순하지만 강력한 아이디어에서 시작되었습니다. 스파크는 단순한 데이터 처리를 넘어 SQL 엔진(Spark SQL), 실시간 스트리밍 처리(Spark Streaming), 머신러닝 라이브러리(MLlib), 그래프 처리(GraphX) 기능을 하나의 스택에 통합하여 빅데이터 분석의 모든 단계를 아우르는 범용 엔진으로 발전했습니다.

**💡 비유: 전 부대에 메모장(칠판)을 보급한 사령관**
과거의 하둡(Hadoop MapReduce)은 병사들이 작전 수행 중 중간 결과를 매번 땅바닥(디스크)에 깊게 파서 기록하고, 다음 병사가 이를 다시 파내어 읽어야 하는 매우 느린 방식이었습니다. 반면, 스파크는 모든 병사에게 전술용 화이트보드(In-memory)를 지급한 것과 같습니다. 병사들은 중간 결과를 화이트보드에 빠르게 적고 동료에게 보여줌으로써 작전 속도를 획기적으로 높였습니다. 비가 오거나 화이트보드가 지워지면(장애 발생), 사령관이 미리 기록해둔 작전 계보(Lineage)를 보고 처음부터 다시 그려내면 되므로 안전성까지 확보한 스마트한 시스템입니다.

**등장 배경 및 발전 과정:**
1. **기존 기술(Hadoop MapReduce)의 치명적 한계점**: 하둡은 맵(Map) 단계와 리듀스(Reduce) 단계 사이의 중간 데이터를 반드시 로컬 디스크에 쓰고 읽어야 하는 복제(Replication) 과정을 거칩니다. 이로 인해 심각한 **디스크 I/O 및 네트워크 오버헤드**가 발생하며, 특히 여러 번의 반복 연산이 필요한 머신러닝 알고리즘이나 인터랙티브 쿼리에서 성능이 기하급수적으로 저하되었습니다.
2. **혁신적 패러다임 변화 (RDD와 In-memory)**: 스파크는 **RDD(Resilient Distributed Dataset)**라는 불변(Immutable)의 분산 객체 개념을 도입했습니다. 데이터를 메모리에 상주시키면서, 데이터의 손실이 발생하면 원본부터의 연산 이력(Lineage)을 추적해 복구하는 방식으로 내결함성(Fault Tolerance)과 고성능을 동시에 달성했습니다.
3. **비즈니스적 요구사항**: 기업들은 수 페타바이트의 데이터를 실시간으로 분석하여 비즈니스 통찰력을 얻길 원합니다. 배치 처리뿐만 아니라 실시간 로그 분석, AI 모델 학습을 단일 인프라에서 경제적으로 수행해야 하는 요구에 부응하며 스파크는 빅데이터의 사실상 표준(De-facto Standard)이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스파크 아키텍처는 마스터-슬레이브 구조를 기반으로 클러스터 자원을 효율적으로 분배하고 작업을 스케줄링합니다.

#### 주요 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 컴포넌트 | 비유 |
|---|---|---|---|---|
| **Driver Program** | 애플리케이션의 뇌 역할, 메인 함수 실행 | 사용자 코드를 분석하여 DAG(실행 계획)를 생성하고, 태스크를 스케줄링하여 Executor에 할당 | SparkContext, DAGScheduler | 오케스트라의 지휘자 |
| **Cluster Manager** | 클러스터 전체의 자원(CPU, Memory) 관리 | 드라이버의 요청에 따라 태스크 수행을 위한 컨테이너 리소스를 할당 및 해제 | YARN, Kubernetes, Mesos | 공연장 대관 및 좌석 관리인 |
| **Executor** | 실제 연산을 수행하는 슬레이브 프로세스 | 할당받은 태스크를 개별 스레드에서 실행하고 데이터를 메모리나 디스크에 저장(Caching/Storage) | TaskRunner, BlockManager | 악기를 연주하는 단원들 |
| **RDD (Resilient Distributed Dataset)** | 스파크의 기본 데이터 추상화 모델 | 데이터를 파티션 단위로 나누어 클러스터 노드에 분산 저장하며, 지연 연산(Lazy Evaluation) 방식으로 처리 | Lineage, Partitioning | 작전 수행을 위한 분산 지도 조각들 |
| **DAG (Directed Acyclic Graph)** | 작업 간의 의존 관계를 나타내는 그래프 구조 | 연산의 흐름을 분석하여 셔플(Shuffle)이 필요한 구간을 기준으로 스테이지(Stage)를 나누어 최적화 | TaskSet, Stage, Pipeline | 작전의 전체 흐름도(순서도) |

#### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                                 [ APACHE SPARK CLUSTER ARCHITECTURE ]
========================================================================================================

    [ DRIVER PROGRAM ]                   [ CLUSTER MANAGER ]             [ WORKER NODE (Executor) ]
  +----------------------+             +---------------------+         +--------------------------+
  |  SparkSession        |             |                     |         |  +--------------------+  |
  |  (User Code)         |  Resource   |  Standalone / YARN  | Allocate|  | Task 1 | Task 2    |  |
  |          |           |  Request    |  Kubernetes / Mesos | Container|  +--------------------+  |
  |  [ DAG Scheduler ]   |<----------->|                     |<------->|  | Block Manager(Mem) |  |
  |          |           |             +---------------------+         +--------------------------+
  |  [ Task Scheduler ]  |                                             [ WORKER NODE (Executor) ]
  |          |           |             [ DATA SOURCE ]                 +--------------------------+
  |  [ Scheduler Backend]|<----------->[ HDFS / S3 / Kafka ]<--------->|  | Task 3 | Task 4    |  |
  +----------------------+                                             |  +--------------------+  |
             |                                                         |  | Block Manager(Mem) |  |
             +-------------------( Launch Tasks )--------------------->+--------------------------+

========================================================================================================
                                  [ SPARK EXECUTION LOGIC: DAG ]
========================================================================================================

  [ RDD 1 ] --(map)--> [ RDD 2 ] --(filter)--> [ RDD 3 ] --(join)--> [ RDD 4 ] --(action: collect)
  
  <----------- STAGE 1 (Narrow Dependency) ----------->   <--- SHUFFLE --->   <----- STAGE 2 ----->
  (Pipelining: No data movement between nodes)            (Wide Dependency)   (Join / GroupBy)

```

#### 심층 동작 원리: RDD Lineage와 Shuffle 최적화
스파크 성능의 핵심은 **"데이터 이동(Shuffle)을 최소화하고, 장애 발생 시 계보를 통해 복구한다"**는 점에 있습니다.

**1. RDD 의존성 관리: Narrow vs Wide Dependency**
- **Narrow Dependency**: 1:1 대응 관계(map, filter). 데이터 이동 없이 각 파티션에서 독립적으로 연산이 가능하며 파이프라이닝(Pipelining) 기법으로 속도가 매우 빠릅니다.
- **Wide Dependency**: N:M 대응 관계(join, groupByKey). 데이터가 다른 노드로 이동해야 하는 **셔플(Shuffle)**이 발생합니다. 이는 네트워크 비용과 디스크 I/O를 유발하는 가장 큰 병목 구간입니다.

**2. Catalyst Optimizer (Spark SQL)**
스파크는 사용자가 작성한 SQL이나 DataFrame 코드를 그대로 실행하지 않고, Catalyst라는 최적화 엔진을 통해 실행 계획을 수립합니다.
- **Analysis**: 카탈로그 정보를 바탕으로 쿼리 오류 확인.
- **Logical Optimization**: 'Filter Pushdown'(필터링을 미리 수행)이나 'Projection Pruning'(필요한 컬럼만 읽기) 등을 적용.
- **Physical Planning**: 실제 실행 가능한 물리적 전략(예: Broadcast Hash Join 사용 여부) 수립.
- **Code Generation**: 런타임에 최적화된 자바 바이트코드를 생성하여 실행 성능 극대화.

**실무 수준의 구현 코드 (PySpark, DataFrame API & Window Function)**

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# 1. Spark 세션 초기화 (애플리케이션 이름 및 리소스 설정)
spark = SparkSession.builder \
    .appName("LogAnalysisPipeline") \
    .config("spark.executor.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .get_OrCreate()

# 2. 데이터 로드 (Schema 추론 및 멀티라인 지원)
raw_logs = spark.read.json("s3://logs/api_access_log/*.json")

# 3. 데이터 정제 및 엔지니어링 (DataFrame API 활용)
# 불필요한 데이터 필터링 및 시간대별 윈도우 연산 수행
processed_df = raw_logs.filter(F.col("status") == 200) \
    .withColumn("event_time", F.to_timestamp("timestamp")) \
    .withColumn("hour", F.hour("event_time"))

# 4. 분석: 사용자별 누적 방문 횟수 계산 (Window Function 활용)
# 셔플을 최소화하기 위해 'user_id' 기준 파티셔닝 전략 사용
window_spec = Window.partitionBy("user_id").orderBy("event_time")
final_df = processed_df.withColumn("visit_rank", F.rank().over(window_spec))

# 5. 최적화된 실행 계획 확인 (Explain)
final_df.explain(True)

# 6. 결과 저장 (Partitioning 전략으로 병렬 I/O 극대화)
final_df.write.partitionBy("hour").parquet("s3://analytics/user_behavior/")

# 7. 캐싱을 통한 반복 연산 성능 향상
final_df.cache()
print(f"Total Rows: {final_df.count()}") # Action 수행 시 실제 연산 발생

spark.stop()
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: Spark vs Hadoop MapReduce vs Flink

| 평가 지표 | Hadoop MapReduce | Apache Spark | Apache Flink |
|---|---|---|---|
| **처리 모델** | 배치 (Batch Only) | **마이크로 배치 (Micro-batch)** / 배치 | **네이티브 스트리밍 (Real-time)** |
| **속도 (성능)** | 느림 (디스크 기반) | **매우 빠름 (인메모리 기반)** | 매우 빠름 (저지연 특화) |
| **메모리 관리** | JVM 수동 관리 | **Unified Memory (Storage + Execution)** | Managed Memory (Off-heap 지원) |
| **API 지원** | Low-level (Java 기반) | **High-level (SQL, Python, Scala)** | High-level (DataStream API) |
| **상태 관리** | 불가능 | **Checkpointing (Lineage)** | State Backend (RocksDB) |
| **학습 곡선** | 높음 | **낮음 (익숙한 언어 지원)** | 중간 |

#### 과목 융합 관점 분석
- **[OS/메모리 + Spark]**: 스파크의 성능을 좌우하는 것은 **GC(Garbage Collection) 오버헤드**입니다. JVM 상에서 수십억 개의 객체를 생성하면 GC가 발생하여 시스템이 멈추는 'Stop-the-world' 현상이 발생합니다. 이를 해결하기 위해 스파크는 **프로젝트 텅스텐(Project Tungsten)**을 도입하여 JVM 힙 대신 운영체제의 **Off-heap 메모리**를 직접 관리하고, 바이너리 포맷으로 데이터를 직렬화하여 메모리 효율을 극대화했습니다. 이는 OS의 메모리 관리 기법을 애플리케이션 레벨로 끌어올린 소프트웨어 공학의 정수입니다.
- **[데이터베이스 + Spark]**: 스파크는 NoSQL(MongoDB, Cassandra)과 RDBMS(MySQL, Oracle)를 모두 연결하는 거대한 **Federated Query Engine** 역할을 합니다. 특히 하둡의 HDFS 위에 ACID 트랜잭션을 구현하는 Delta Lake와 융합되어, DW(Data Warehouse)의 신뢰성과 Data Lake의 확장성을 동시에 갖춘 **Lakehouse** 아키텍처의 핵심 엔진으로 기능합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 기술사적 판단 (실무 시나리오)
- **시나리오 1: 셔플링 중 발생하는 Out of Memory (OOM) 해결**
  - **문제**: 대규모 Join 시 한쪽 노드로 데이터가 몰리는 **데이터 스큐(Data Skew)** 현상으로 특정 Executor의 메모리가 터지는 사고가 발생합니다.
  - **전략적 의사결정**: 작은 테이블은 모든 노드에 복사하는 **Broadcast Hash Join**을 강제(`F.broadcast()`)하거나, 스큐가 발생한 키에 임의의 소금값(Salting)을 추가하여 데이터를 고르게 분산시키는 전략을 수립합니다. 또한 `spark.sql.adaptive.enabled=true`(AQE)를 설정하여 실행 중에 파티션을 동적으로 병합하도록 아키텍처를 조정합니다.
- **시나리오 2: 실시간 로그 스트리밍 처리 지연(Latency) 최적화**
  - **문제**: Spark Streaming의 기본 마이크로 배치 주기가 1초인데, 인입되는 트래픽이 몰려 배치가 밀리는 'Scheduling Delay'가 발생합니다.
  - **전략적 의사결정**: **Spark Structured Streaming**으로 전환하고, 'Continuous Processing Mode'를 검토하여 지연 시간을 밀리초(ms) 단위로 단축합니다. 또한 스테이트풀(Stateful) 연산 시 윈도우 크기를 최적화하고 체크포인트 저장소로 S3 대신 저지연인 로컬 SSD 기반의 저장소를 활용하도록 구성합니다.
- **시나리오 3: 비용 최적화를 위한 서버리스(Serverless) 스파크 도입**
  - **문제**: 24시간 클러스터를 켜두기에는 야간 시간대 자원 낭비가 심하고 관리 인력이 부족합니다.
  - **전략적 의사결정**: **Amazon EMR Serverless 또는 Google Cloud Dataproc Serverless**를 도입합니다. 작업이 있을 때만 자원을 할당받고 끝나면 즉시 반납하며, 사용한 자원(vCPU/Mem) 단위로 과금되는 모델을 채택하여 TCO(Total Cost of Ownership)를 40% 이상 절감합니다.

#### 주의사항 및 안티패턴 (Anti-patterns)
- **Iteration 중 `collect()` 사용**: 수십 테라의 데이터를 드라이버 노드로 한꺼번에 가져오려는 `collect()` 함수 호출은 드라이버의 OOM을 유발하는 가장 대표적인 안티패턴입니다. 데이터는 반드시 `saveAsParquet()` 등을 통해 분산 저장소로 직접 써야 합니다.
- **불필요한 `repartition()` 남발**: 파티션 수를 늘리겠다고 무작정 `repartition()`을 호출하면 네트워크 전체에 데이터 셔플이 발생합니다. 파티션을 줄일 때는 셔플이 없는 `coalesce()`를 사용해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 정량적/정성적 기대효과
| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 배치/스트리밍/ML/SQL 코드를 하나로 통합하여 개발 및 유지보수 생산성 비약적 향상<br>- 클라우드 네이티브 환경(K8s)으로의 유연한 이식성 확보 |
| **정량적 효과** | - 하둡 맵리듀스 대비 반복 연산 속도 **최대 100배 향상**<br>- 셔플 최적화 및 AQE 도입 시 쿼리 성능 **30~50% 추가 개선**<br>- 데이터 레이크 구축 시 데이터 신뢰성(ACID) 99.9% 보장 |

#### 미래 전망 및 진화 방향
- **Spark on Kubernetes (K8s)**: 기존 YARN 기반에서 쿠버네티스 네이티브 실행 환경으로 완전히 이전하고 있습니다. 자원 격리(Isolation)와 오토스케일링이 더욱 정교해질 것입니다.
- **Photon 엔진과 가속기 지원**: Databricks가 개발한 C++ 기반의 벡터화 쿼리 엔진 'Photon'이 스파크에 통합되어 가고 있으며, GPU 및 FPGA 가속기를 활용한 딥러닝 연산 지원이 더욱 강화될 것입니다.
- **Serverless & Zero-management**: 인프라 설정을 AI가 대신 해주는 'No-ops' 스파크 서비스가 대중화되어 사용자는 로직에만 집중하게 될 것입니다.

**※ 참고 표준/가이드**: 
- 데이터 처리 시 **개인정보 보호법 및 GDPR** 준수를 위해 스파크 파이프라인 상에 **비식별화(Anonymization) 모듈**을 내재화해야 하며, 분산 처리 시 데이터 유실 방지를 위한 **IEEE 1012(소프트웨어 검증 및 확인)** 기준에 따른 체크포인트 무결성 검증 프로세스가 권고됩니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- `[RDD & Lineage](@/studynotes/16_bigdata/_index.md)`: 스파크의 근본 데이터 모델이자 장애 복구의 핵심 메커니즘.
- `[Spark SQL & Catalyst](@/studynotes/16_bigdata/_index.md)`: 고수준 쿼리 최적화를 담당하는 지능형 실행 계획 수립 엔진.
- `[Delta Lake](@/studynotes/16_bigdata/_index.md)`: 스파크 위에서 데이터 신뢰성과 성능을 보장하는 오픈소스 저장 레이어.
- `[YARN / Kubernetes](@/studynotes/16_bigdata/_index.md)`: 스파크 클러스터의 물리적 자원을 할당하고 관리하는 인프라 소프트웨어.
- `[Shuffle & Skew](@/studynotes/16_bigdata/_index.md)`: 분산 컴퓨팅의 최대 적이며, 스파크 성능 튜닝의 80%를 차지하는 핵심 이슈.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **아파치 스파크가 뭔가요?**: 아주아주 많은 데이터를 한꺼번에 계산해야 할 때, 수천 대의 컴퓨터에 **"너희 각자 공부한 걸 공책(메모리)에 적어서 서로 빠르게 공유해!"**라고 지시하는 아주 똑똑한 대장님이에요.
2. **어떻게 작동하나요?**: 옛날 방식처럼 종이에 일일이 쓰고 지우는 게 아니라, 컴퓨터의 '기억력(메모리)'을 직접 사용하기 때문에 눈 깜빡할 사이에 계산이 끝나요. 중간에 누가 답을 까먹어도 처음부터 어떻게 풀었는지 적어둔 일기장(Lineage)을 보고 금방 기억해낸답니다.
3. **왜 좋은가요?**: 복잡한 수학 문제도, 실시간으로 쏟아지는 뉴스 분석도 이 대장님만 있으면 아주 빠르고 정확하게 끝낼 수 있어서, 현대의 인공지능과 빅데이터 세상을 만드는 데 없어서는 안 될 보물 같은 기술이에요!
