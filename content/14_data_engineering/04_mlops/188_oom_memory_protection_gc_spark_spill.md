---
title: "Oom Memory Protection Gc Spark Spill"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 188
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OOM(Out of Memory)은 메모리 누수·과다 적재·비효율적 파티셔닝이 복합적으로 작용하여 JVM 힙이 고갈되는 현상으로, <strong>Spark 메모리 모델(Execution/Storage 통합 메모리)</strong>을 이해하고 Tungsten 엔진과 스필(Spill) 메커니즘을 활용하는 것이 핵심이다.
> 2. **가치**: G1GC·ZGC 같은 현대 JVM GC 튜닝과 Spark의 메모리 파라미터(spark.memory.fraction 등)를 최적화하면 <strong>수백 GB 데이터 처리 시 OOM 없이 안정적인 배치 파이프라인</strong>을 구축할 수 있다.
> 3. **판단 포인트**: OOM 디버깅 체크리스트—파티션 크기 확인(200MB 기준), 스큐(Data Skew) 제거, 브로드캐스트 조인 활용, 불필요한 캐시 해제—이 학습 정리에서 실무 역량을 보여주는 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 OOM 발생 원인 분류

```
OOM 원인 트리:
                    OOM (Out of Memory)
                         |
         +---------------+---------------+
    메모리 누수         과다 데이터      비효율 파티셔닝
    (Memory Leak)       (Data Volume)    (Bad Partitioning)
         |                   |                  |
  +- 클로저 참조        +- 큰 스테이지     +- 소수 파티션
  +- 정적 변수 누적     +- 넓은 조인      +- 데이터 스큐
  +- 브로드캐스트 남용   +- 집계 과부하    +- 잘못된 캐싱
  +- DataFrame 캐시 미해제+- UDF 비효율   +- 넓은 윈도우 함수
```

### 1.2 Spark OOM 발생 시 에러 패턴

```
Executor OOM:
  ERROR Executor: Exception in task
  java.lang.OutOfMemoryError: Java heap space
  -> 파티션 크기 과다, 집계 메모리 부족

Driver OOM:
  java.lang.OutOfMemoryError: GC overhead limit exceeded
  -> collect() / toPandas() 로 드라이버에 과다 데이터 수집

GC 관련:
  WARN GCTimeRatio: JVM is spending too much time in GC
  -> 실제 OOM 전 단계 경고, 즉시 대응 필요
```

📢 **섹션 요약 비유**: OOM은 마치 너무 많은 파일을 책상(메모리) 위에 올려놓아 더 이상 공간이 없어 작업을 멈추는 것과 같다. 파일을 서랍(디스크, Spill)에 잠깐 넣거나, 불필요한 파일을 버리는(GC) 것이 해결책이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Spark 메모리 모델 (Unified Memory Model)

```
+----------------------------------------------------------+
|                Spark Executor JVM 메모리 구조              |
|                                                           |
|  총 Executor 메모리 (spark.executor.memory = 4g 예시)     |
|  +-----------------------------------------------------+ |
|  |  Reserved Memory (300MB) - JVM 내부 사용            | |
|  +-----------------------------------------------------+ |
|  |  User Memory (40% × (4g-300MB) ≈ 1.5g)             | |
|  |  - UDF 데이터, 사용자 자료구조                        | |
|  +-----------------------------------------------------+ |
|  |  Spark Memory (60% × (4g-300MB) ≈ 2.2g)            | |
|  |  +---------------------------------------------+   | |
|  |  | Storage Memory (초기 50%, 동적 조정 가능)     |   | |
|  |  | - cache(), persist() 데이터                  |   | |
|  |  +---------------------------------------------+   | |
|  |  | Execution Memory (초기 50%, 동적 조정 가능)  |   | |
|  |  | - 셔플(Shuffle), 정렬(Sort), 조인(Join)      |   | |
|  |  | - 부족 시 -> Spill to Disk                   |   | |
|  |  +---------------------------------------------+   | |
|  +-----------------------------------------------------+ |
+----------------------------------------------------------+

핵심 파라미터:
  spark.memory.fraction          = 0.6 (Spark Memory 비율)
  spark.memory.storageFraction   = 0.5 (Storage/Execution 초기 비율)
  spark.executor.memory          = 4g  (총 Executor 메모리)
  spark.executor.memoryOverhead  = 0.1 (오프힙 overhead 비율)
```

### 2.2 Tungsten 엔진 (Off-Heap 메모리)

```
Tungsten (Code Generation + Off-Heap):

  On-Heap 방식 (JVM 객체):
    DataFrame Row -> Java Object -> GC 압력 증가
    객체 헤더 오버헤드: 각 Row에 16~32 바이트 추가

  Off-Heap 방식 (Tungsten):
    DataFrame Row -> Binary 인코딩 -> 직접 메모리 주소 접근
    -> GC 대상 아님, 캐시 친화적, 30~40% 성능 향상

  활성화:
    spark.memory.offHeap.enabled = true
    spark.memory.offHeap.size = 2g
```

### 2.3 JVM GC 알고리즘 비교

| GC 알고리즘 | 특징 | Spark 추천 여부 |
|:---|:---|:---|
| G1GC (Garbage First) | 대용량 힙, 정지 시간 예측 가능 | ✅ Spark 기본 권장 |
| ZGC | 초저지연 (< 1ms STW), JDK 15+ | ✅ 지연 민감 워크로드 |
| Shenandoah | ZGC 유사, Red Hat 개발 | ⚠️ 일부 버전 불안정 |
| CMS (Concurrent Mark Sweep) | 구형, JDK 14에서 제거됨 | ❌ 사용 금지 |
| Parallel GC | 처리량 최대화, 긴 정지 | ⚠️ 배치 전용 |

```
G1GC Spark 최적화 설정:
  -XX:+UseG1GC
  -XX:G1HeapRegionSize=16m      # Region 크기 (큰 데이터셋)
  -XX:InitiatingHeapOccupancyPercent=35  # 조기 GC 트리거
  -XX:MaxGCPauseMillis=200      # 최대 정지 시간 목표
  -XX:ConcGCThreads=4           # 동시 GC 스레드 수
```

### 2.4 Spill to Disk (디스크 스필) 메커니즘

```
+----------------------------------------------------------+
|                   Spill to Disk 흐름                       |
|                                                           |
|  집계/정렬/조인 연산 시작                                   |
|       v                                                  |
|  Execution Memory 사용 시작                               |
|       v                                                  |
|  메모리 한도 80% 도달?                                    |
|  +---- No ----+                                          |
|  |  계속 진행  |                                          |
|  +------------+                                          |
|  +---- Yes ---+                                          |
|  |  현재 버퍼를 로컬 디스크에 Spill 파일로 직렬화          | |
|  |  -> spark.local.dir 경로 (빠른 SSD 권장)               | |
|  |  메모리 해제 -> 나머지 처리 계속                         | |
|  +------------+                                          |
|       v                                                  |
|  모든 Spill 파일 + 메모리 결과 -> 최종 머지               |
|                                                           |
|  Spill 발생 확인:
|  Spark UI -> Stage -> Shuffle Spill (Memory/Disk)         |
+----------------------------------------------------------+
```

📢 **섹션 요약 비유**: Spill to Disk는 마치 책상(메모리)이 가득 차면 임시로 서랍(디스크)에 넣어두고 작업을 계속하는 것이다. 서랍에서 꺼내는 것(디스크 I/O)이 느려 성능은 저하되지만 OOM으로 작업이 실패하는 것보다는 낫다.

---

## Ⅲ. 비교 및 연결

### 3.1 데이터 스큐 (Data Skew) vs 균등 파티션

```
데이터 스큐 예시:
  파티션별 레코드 수:
  P0: 100만 개 <- 스큐 (특정 키 집중)
  P1: 1만 개
  P2: 5만 개
  P3: 8천 개

  -> P0 태스크만 OOM, 나머지는 유휴
  -> 전체 스테이지는 가장 느린 P0 기다림

스큐 해결 방법:
  1. 솔트(Salt) 키 기법:
     스큐 키에 무작위 접미사 추가 (key + "_0", "_1", ...)
     -> 인위적으로 파티션 분산

  2. 브로드캐스트 조인 (작은 테이블 < 10MB):
     spark.sql.autoBroadcastJoinThreshold = 10MB
     -> 셔플 없이 전 파티션에 복사

  3. 버킷팅 (Bucketing):
     파티션 키 사전 정렬 + 저장
     -> 셔플 단계 자체를 제거

  4. 적응형 쿼리 실행 (AQE, Adaptive Query Execution):
     spark.sql.adaptive.enabled = true
     -> 런타임 스큐 파티션 자동 분할
```

### 3.2 OOM 방지 파티션 설계

```
파티션 크기 권장 기준:
  최적 파티션 크기: 100~200 MB

  파티션 수 계산:
    데이터 크기 / 목표 파티션 크기 = 필요 파티션 수
    100GB / 128MB = ~800개 파티션

  설정:
    spark.sql.shuffle.partitions = 800  (셔플 후 파티션 수)
    df.repartition(800)                 (명시적 파티셔닝)

  주의:
    파티션 수 너무 적음 -> OOM (큰 파티션)
    파티션 수 너무 많음 -> 오버헤드 (작은 파티션, 스케줄링 비용)
```

### 3.3 메모리 최적화 기법 비교

| 기법 | 효과 | 적용 케이스 |
|:---|:---|:---|
| 파티션 재조정 | 균일한 메모리 사용 | 데이터 스큐 |
| 브로드캐스트 조인 | 셔플 메모리 제거 | 작은 테이블 (< 10MB) |
| AQE 활성화 | 런타임 스큐 자동 처리 | Spark 3.0+ |
| 컬럼 선택 (Projection Pushdown) | 불필요한 컬럼 조기 제거 | 와이드 스키마 |
| 술어 푸시다운 (Predicate Pushdown) | 파일 수준 필터링 | 파케이(Parquet) 파일 |
| 캐시 관리 | 불필요한 캐시 해제 | 장시간 실행 잡 |
| Off-Heap 활성화 | GC 압력 감소 | 대용량 집계 |

📢 **섹션 요약 비유**: 데이터 스큐는 마치 이삿짐을 옮길 때 한 트럭에 모든 가구를 싣고 나머지 트럭은 비어있는 것과 같다. 솔트 키 기법은 소파를 반으로 분해해서 여러 트럭에 나눠 싣는 방법이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 Spark OOM 디버깅 체크리스트

```
단계별 OOM 진단 프로세스:

  1단계: Spark UI 확인
  +- Stage 탭 -> Shuffle Spill (Memory/Disk) 크기 확인
  +- Executor 탭 -> GC Time (20% 초과 시 GC 튜닝 필요)
  +- Tasks 탭 -> 태스크별 실행 시간 불균형 (스큐 확인)

  2단계: 로그 분석
  +- "java.lang.OutOfMemoryError: Java heap space"
  |   -> spark.executor.memory 증가 or 파티션 수 증가
  +- "GC overhead limit exceeded"
  |   -> G1GC 파라미터 튜닝 or 메모리 증가
  +- "Container killed by YARN for exceeding memory limits"
      -> spark.executor.memoryOverhead 증가 (기본 10%)

  3단계: 코드 최적화
  +- collect() / toPandas() 대용량 호출 제거
  +- 불필요한 cache() / persist() 해제 (.unpersist())
  +- UDF 대신 내장 함수 (SQL 함수) 사용
  +- 넓은 스키마 -> 필요 컬럼만 select()
```

### 4.2 Spark 메모리 파라미터 튜닝 가이드

```
Executor 메모리 설정:
  spark.executor.memory         = 8g   # JVM 힙
  spark.executor.memoryOverhead = 2g   # 오프힙 오버헤드
  spark.memory.offHeap.enabled  = true
  spark.memory.offHeap.size     = 4g   # Tungsten 오프힙

메모리 분배:
  spark.memory.fraction         = 0.75 # Spark Memory 비율 (기본 0.6)
  spark.memory.storageFraction  = 0.3  # Storage 비율 (기본 0.5)

GC 설정 (G1GC):
  spark.executor.extraJavaOptions = "-XX:+UseG1GC
    -XX:G1HeapRegionSize=16m
    -XX:+PrintGCDetails
    -XX:+PrintGCTimeStamps"

AQE (Adaptive Query Execution):
  spark.sql.adaptive.enabled                   = true
  spark.sql.adaptive.coalescePartitions.enabled = true
  spark.sql.adaptive.skewJoin.enabled          = true
```

### 4.3 학습 정리 핵심 포인트

```
Spark OOM 방지 설계 시 필수 언급:
  ✓ Spark 통합 메모리 모델: Execution vs Storage 동적 공유
  ✓ Tungsten + Off-Heap으로 GC 압력 감소
  ✓ G1GC 추천 (대용량 힙, 예측 가능한 정지 시간)
  ✓ Spill to Disk: OOM 방지 최후 수단, SSD 사용 권장
  ✓ AQE 활성화: 런타임 스큐·파티션 자동 최적화
  ✓ 파티션 크기 100~200MB 유지 (너무 크거나 작으면 문제)
  ✓ 브로드캐스트 조인 기준: 10MB (spark.sql.autoBroadcastJoinThreshold)
  ✓ Driver OOM: collect/toPandas 제한, writeTo 사용 권장
```

📢 **섹션 요약 비유**: Spark OOM 디버깅은 마치 막히는 도로(GC, Spill)를 찾아 교통 정리를 하는 것이다. Spark UI는 CCTV로 어디가 막히는지 보여주고, 파티션 재조정은 좁은 도로에 차를 분산시키는 우회로 설치다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 메모리 최적화 효과

| 최적화 기법 | 효과 |
|:---|:---|
| G1GC -> ZGC 전환 | GC 정지 시간 200ms -> 1ms 이하 |
| AQE 활성화 | 스큐 파티션 자동 처리로 안정성 향상 |
| Tungsten Off-Heap | GC 부담 30~40% 감소, 처리량 향상 |
| 파티션 최적화 | OOM 발생률 80% 이상 감소 |
| 브로드캐스트 조인 | 셔플 메모리 100% 제거 (해당 조인) |

### 5.2 메모리 최적화 의사결정 트리

```
+------------------------------------------------------+
|          Spark OOM 해결 의사결정 트리                   |
|                                                      |
|  OOM 발생                                            |
|       v                                              |
|  Driver OOM? -> collect/toPandas 제거 -> 해결          |
|       v No                                           |
|  Executor OOM?                                       |
|       v                                              |
|  GC Time > 20%? -> G1GC/ZGC 튜닝 -> 개선 확인         |
|       v No                                           |
|  스큐 파티션? -> AQE/Salt 키 -> 균등화                 |
|       v No                                           |
|  파티션 크기 > 200MB? -> 파티션 수 증가              |
|       v No                                           |
|  캐시 미해제? -> unpersist() 추가                     |
|       v No                                           |
|  메모리 파라미터 증가 (executor.memory)              |
+------------------------------------------------------+
```

📢 **섹션 요약 비유**: Spark OOM 최적화 의사결정 트리는 마치 건강 검진 체크리스트와 같다. 혈압(GC Time)이 높으면 약(GC 튜닝)을 쓰고, 허리(파티션 균형)가 나쁘면 자세를 고치고, 그래도 안 되면 더 큰 침대(메모리)를 사용한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 장애 | OOM (Out of Memory) | JVM 힙 고갈로 프로세스 종료 |
| 메모리 관리 | GC (Garbage Collection) | 불필요한 객체 메모리 회수 |
| 현대 GC | G1GC / ZGC / Shenandoah | 대용량·저지연 GC 알고리즘 |
| Spark 최적화 | Tungsten | 코드 생성 + 오프힙 바이너리 처리 |
| 안전 밸브 | Spill to Disk | 메모리 부족 시 디스크로 임시 저장 |
| 핵심 문제 | 데이터 스큐 (Data Skew) | 파티션 불균형으로 일부 OOM |
| 자동 최적화 | AQE (Adaptive Query Execution) | 런타임 통계 기반 자동 최적화 |
| 조인 최적화 | 브로드캐스트 조인 | 소규모 테이블 전 파티션 복사 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>OOM</strong>은 마치 책상 위에 책을 너무 많이 쌓아서 결국 책상이 무너지는 것처럼, 컴퓨터가 한꺼번에 너무 많은 데이터를 기억하려다 뻗어버리는 상황이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
OOM (Out of Memory) 발생
    |
    v
원인 진단
    +-► JVM: 힙 부족 · GC 오버헤드 · 메모리 누수
    +-► Spark: Executor 메모리 · Shuffle 스필 · 데이터 스큐
    +-► GPU: VRAM 부족 · 배치 크기 과다
    |
    v
방어 전략
    +-► GC 튜닝 (G1GC · ZGC) · 힙 조정
    +-► Spark: 파티션 수 증가 · Spill to Disk · AQE
    +-► GPU: Mixed Precision · Gradient Checkpointing
    |
    v
프로액티브 모니터링 -> OOM 사전 경보 · 자동 스케일링
```
2. <strong>GC(쓰레기 수거)</strong>는 마치 수업 중에 가끔 선생님이 "이제 필요 없는 노트 버려라!"라고 하는 것처럼, 컴퓨터가 사용이 끝난 데이터를 자동으로 치워서 공간을 만드는 작업이에요—너무 자주 하면 수업이 멈추니 조절이 중요해요.
3. <strong>Spill to Disk</strong>는 책상이 가득 찼을 때 당장 쓰지 않는 책을 임시로 사물함(디스크)에 넣어두는 것처럼, 메모리가 부족하면 데이터를 디스크에 잠깐 저장하고 나중에 다시 꺼내 작업을 계속하는 방법이에요.
