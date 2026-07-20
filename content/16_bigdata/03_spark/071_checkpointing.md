---
title: "Checkpointing"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 71
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Spark 체크포인팅(Checkpointing)은 RDD/DataFrame의 리니지(Lineage, 변환 계보)를 HDFS/S3 같은 안정적인 저장소에 물리적으로 스냅샷을 저장하여 리니지 체인을 단절하고, 장애 발생 시 처음부터 재연산하지 않고 체크포인트 지점에서 재시작할 수 있게 하는 메커니즘이다.
- **가치**: 수십 단계의 변환이 쌓인 장기 실행 작업이나 스트리밍에서 상태(State)를 관리할 때, 리니지가 너무 길어져 JVM 스택 오버플로나 재연산 비용이 폭증하는 문제를 체크포인팅으로 근본적으로 해결한다.
- **판단 포인트**: 체크포인팅은 `cache()`/`persist()`와 다르다. `cache()`는 메모리에 데이터를 보존하되 리니지는 유지하고 Executor 재시작 시 소실되지만, 체크포인팅은 리니지를 끊고 안정적 외부 스토리지에 영구 저장한다.

---

## Ⅰ. 개요 및 필요성

### 1. Lineage와 Fault Tolerance

스파크는 RDD의 변환 이력(Lineage)을 DAG(Directed Acyclic Graph)로 추적하여 장애 시 재연산(Recomputation)으로 결함 허용을 달성한다. 그러나 리니지가 길어질수록 두 가지 문제가 발생한다.

- **재연산 비용 폭발**: 10단계 변환의 파티션이 하나 유실되면 10단계 전체를 재연산
- <strong>드라이버 메모리/스택 한계</strong>: 리니지가 수백 단계가 되면 TaskScheduler의 DAG 직렬화 크기가 커져 OOM(Out of Memory) 발생

### 2. 체크포인팅이 필요한 상황

1. <strong>반복적 ML 알고리즘</strong>: PageRank, 그래프 알고리즘, EM 알고리즘 등 수십~수백 이터레이션
2. <strong>Structured Streaming</strong>: 상태 저장 연산(StatefulAggregation)의 상태 백업
3. <strong>장기 실행 파이프라인</strong>: 수 시간 이상 실행되는 ETL 파이프라인

**📢 섹션 요약 비유**
> 리니지(Lineage)는 "요리 레시피 전체를 기억하는 것"이다. 30단계 레시피를 외우다가 중간에 실수하면 처음부터 다시 시작해야 한다. 체크포인팅은 15단계 완성된 중간 결과물을 냉동고(HDFS)에 저장하는 것 — 이후 실수해도 냉동고에서 꺼내 15단계부터 이어가면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 체크포인팅 동작 원리

```
체크포인팅 전:
  Input --> T1 --> T2 --> T3 --> T4 --> T5 --> T6 --> T7 --> Output
  (Lineage: 7단계 변환 기억)

  장애 발생 (T6 파티션 유실) -> T1~T6 전체 재연산 필요!

체크포인팅 후:
  Input --> T1 --> T2 --> T3 --> [체크포인트: HDFS 저장]
                                   v
                              T4 --> T5 --> T6 --> T7 --> Output
  (T4 이후 Lineage만 기억)

  장애 발생 (T6 파티션 유실) -> HDFS에서 T3 체크포인트 로드 -> T4~T6만 재연산!
```

### 2. RDD 체크포인팅 사용법

```python
# 1. 체크포인트 디렉토리 설정 (안정적 분산 스토리지 권장)
sc.setCheckpointDir("hdfs:///spark/checkpoints")

# 2. 체크포인팅 전 persist() 호출 권장 (디스크 쓰기 중복 방지)
rdd = rdd.persist()

# 3. 체크포인팅 설정
rdd.checkpoint()

# 4. 액션 실행 시 HDFS에 실제 저장됨
rdd.count()  # 이 시점에 checkpoint 파일 생성

# 5. 이후 이 RDD의 리니지는 체크포인트 파일을 가리킴
print(rdd.toDebugString())  # ReliableCheckpointRDD
```

### 3. Structured Streaming 체크포인팅

```python
query = df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "hdfs:///streaming/checkpoint/") \
    .outputMode("append") \
    .start("/output/streaming")
```

스트리밍 체크포인트는 다음을 저장한다:
- 현재까지 처리한 오프셋(Offset)
- 집계 연산의 상태(State)
- 완료된 마이크로배치 메타데이터

### 4. 체크포인팅 유형 비교

| 유형 | 저장 위치 | 리니지 단절 | 사용 대상 |
|:---|:---|:---|:---|
| Reliable Checkpoint | HDFS/S3 (내구성^) | 완전 단절 | RDD, Spark Streaming |
| Local Checkpoint | Executor 로컬 디스크 | 부분 단절 | 빠르지만 Executor 장애 시 유실 |
| Streaming Checkpoint | HDFS/S3 | 상태 저장 | Structured Streaming |

**📢 섹션 요약 비유**
> 체크포인팅은 "게임 세이브 포인트"와 같다. 30분 게임 후 세이브(체크포인트)하면, 이후 죽어도 세이브 지점부터 재시작한다. HDFS에 저장하면 컴퓨터가 꺼져도 안전하다.

---

## Ⅲ. 비교 및 연결

### 1. 체크포인팅 vs cache()/persist()

| 항목 | cache() / persist() | checkpoint() |
|:---|:---|:---|
| 저장 위치 | Executor 메모리/디스크 | HDFS/S3 (외부 안정 스토리지) |
| 리니지 처리 | 유지 (재연산 가능) | 완전 단절 (재연산 불가) |
| Executor 재시작 시 | 데이터 소실, 리니지로 재연산 | 체크포인트에서 복구 |
| 사용 목적 | 반복 참조 성능 최적화 | 리니지 단절, 내구성 보장 |
| 비용 | 메모리 사용 | HDFS 쓰기 비용 |

### 2. 연결 개념

- **Lineage**: 체크포인팅이 단절하는 대상
- <strong>Structured Streaming Watermark</strong>: 스트리밍에서 체크포인팅과 함께 상태 만료 관리
- <strong>Fault Tolerance</strong>: 체크포인팅의 근본 목적

**📢 섹션 요약 비유**
> `cache()`는 "책 내용을 머릿속에 외워두는 것"(빠르지만 잠들면 사라짐)이고, `checkpoint()`는 "책 내용을 필사해 금고에 보관하는 것"(느리지만 영구 보존)이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. 체크포인팅 적용 기준

| 조건 | 체크포인팅 권장 여부 |
|:---|:---|
| 리니지 깊이 > 20~30단계 | ✅ 강권장 |
| ML 반복 알고리즘 (PageRank 등) | ✅ 매 N 이터레이션마다 |
| Structured Streaming 상태 저장 | ✅ 필수 (withWatermark, groupBy) |
| 단순 배치 변환 (< 10단계) | ❌ 불필요 (오버헤드) |

### 2. 실무 주의사항

```python
# 패턴: persist() 후 checkpoint() 호출
# 이유: checkpoint()는 액션 실행 시 HDFS 쓰기 + 리니지 단절이 같이 일어남
#      persist() 없으면 액션 실행 시 재연산 후 HDFS 저장 (이중 비용)
rdd = rdd.persist(StorageLevel.MEMORY_AND_DISK)
rdd.checkpoint()
rdd.count()  # persist된 데이터를 HDFS에 쓰기 (재연산 불필요)
```

### 3. 체크리스트

- [ ] 체크포인트 경로는 신뢰성 있는 분산 스토리지 (HDFS, S3, Azure ADLS) 사용
- [ ] `checkpoint()` 호출 전 `persist()` 먼저 적용
- [ ] 스트리밍 쿼리는 `checkpointLocation` 필수 설정
- [ ] 체크포인트 디렉토리 용량 관리 (주기적 정리 필요)
- [ ] LocalCheckpoint는 내구성 없으므로 프로덕션에서 사용 금지

**📢 섹션 요약 비유**
> 체크포인팅 설정은 "장거리 여행 중 주유소에서 기름을 채우는 것"이다. 중간에 차가 멈춰도(장애) 최근 주유소(체크포인트)에서 다시 출발할 수 있다. 주유 없이 무한정 달리다가 멈추면 처음 출발지로 돌아가야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 재연산 비용 절감 | 체크포인트 이전 단계 재연산 제거 |
| JVM 안정성 향상 | 과도한 리니지로 인한 스택 오버플로 방지 |
| 스트리밍 내구성 | 상태 저장 스트리밍 장애 복구 가능 |
| 장기 실행 작업 신뢰성 | 수 시간 실행 작업의 중간 결과 보존 |

### 2. 결론

체크포인팅은 Spark의 <strong>fault tolerance 아키텍처의 핵심 보완 장치</strong>다. 리니지 기반 복구가 강력하지만 무한히 쌓이면 오히려 취약점이 되는 역설을 해결하며, 특히 스트리밍 상태 관리에서는 없어서는 안 될 필수 메커니즘이다.

**📢 섹션 요약 비유**
> 체크포인팅 없는 장기 Spark 작업은 "세이브 없이 100층 던전을 도전하는 것"이다. 99층에서 죽으면 1층부터 다시 시작해야 한다. 10층마다 세이브(체크포인팅)하면 최악의 경우에도 9층만 다시 하면 된다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Lineage (리니지) | 단절 대상 | 체크포인팅으로 변환 계보를 끊음 |
| cache() / persist() | 보완 기술 | 메모리 캐시 + 체크포인팅 같이 사용 권장 |
| Structured Streaming | 응용 영역 | 상태 저장 스트리밍의 핵심 내구성 메커니즘 |
| Fault Tolerance | 목적 | 장애 복구 비용을 체크포인트 이후로 한정 |
| HDFS / S3 | 저장 대상 | 신뢰성 있는 외부 스토리지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Spark RDD 리니지 (Lineage) — 변환 이력 그래프 축적]
    |
    v
[체크포인팅 (Checkpointing) — HDFS에 RDD 물리 저장, 리니지 절단]
    |
    v
[스트리밍 체크포인트 — 오프셋·상태(State) 주기적 영속화]
    |
    v
[WAL (Write-Ahead Log) — 장애 복구 전 로그 선기록]
    |
    v
[장애 복구 (Fault Recovery) — 체크포인트 지점에서 재연산 최소화]
```
Spark의 리니지가 길어질수록 재연산 비용이 폭발하므로, 체크포인팅으로 중간 상태를 영속화해 장애 복구 시 재연산 범위를 최소화한다.

### 👶 어린이를 위한 3줄 비유 설명

레고 블록으로 큰 성을 만들다가 중간에 다 무너지면 처음부터 다시 만들어야 하는데, 체크포인팅은 30번째 블록 쌓았을 때 사진을 찍어두는 것(HDFS 저장)이에요. 무너지면 30번째 사진 보고 거기서부터 이어서 만들면 되니까 훨씬 빠르죠! `cache()`는 잘 기억해두는 것이지만, 체크포인팅은 사진을 찍어 서랍에 보관하는 거예요.
