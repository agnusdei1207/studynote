---
title: "Flink Savepoint Checkpoint"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 83
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Flink의 Checkpoint (체크포인트)는 자동으로 주기적으로 스트리밍 상태 스냅샷을 저장하여 장애 복구를 지원하고, Savepoint (세이브포인트)는 사용자가 수동으로 트리거하여 애플리케이션 업그레이드·마이그레이션·디버깅에 사용하는 명시적 상태 보존 메커니즘이다.
- **가치**: 두 메커니즘 모두 Chandy-Lamport 분산 스냅샷 알고리즘을 기반으로 하여, 스트리밍 처리를 중단하지 않고도 글로벌 일관성 있는 상태를 캡처하므로 Exactly-Once 보장과 무중단 운영이 동시에 가능하다.
- **판단 포인트**: 체크포인트는 Flink가 내부적으로 관리하며 장애 복구 후 삭제될 수 있지만, 세이브포인트는 영구 저장이 목적이므로 버전 업그레이드나 클러스터 마이그레이션 전에는 반드시 세이브포인트를 생성해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 스트리밍 처리에서 상태(State)의 중요성

스트리밍 애플리케이션은 이전 이벤트의 정보를 기억해야 의미있는 결과를 낼 수 있다.

- **집계**: 지난 5분간 사용자별 구매 금액 합계 -> 이전 이벤트 기억 필요
- **조인**: 클릭과 구매 이벤트를 사용자 ID로 연결 -> 두 스트림 상태 유지
- <strong>CEP</strong>: 이상 패턴(로그인 실패 3회 -> 계정 잠금) -> 이벤트 시퀀스 기억

이 상태(State)가 대용량 장기 실행 스트리밍에서 중요해지면, 장애 시 상태 복구와 운영 중 상태 보존이 핵심 과제가 된다.

### 2. 체크포인트 vs 세이브포인트 개요

| 항목 | Checkpoint | Savepoint |
|:---|:---|:---|
| 트리거 | Flink 자동 (주기적) | 사용자 수동 |
| 목적 | 장애 복구 | 업그레이드/마이그레이션/디버깅 |
| 보존 정책 | 장애 복구 후 삭제 가능 | 영구 저장 (사용자 관리) |
| 포맷 | 내부 최적화 포맷 | 이식 가능한 외부 포맷 |

**📢 섹션 요약 비유**
> 체크포인트는 "게임 자동 저장"이고, 세이브포인트는 "중요한 게임 장면에서 직접 저장하는 슬롯 저장"이다. 자동 저장은 정전(장애)에 대비하고, 슬롯 저장은 나중에 다시 돌아와 이어하기 위한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Chandy-Lamport 분산 스냅샷 알고리즘

```
[Checkpoint 동작 과정]

JobManager의 CheckpointCoordinator
    |
    | 1. Barrier 주입 (Checkpoint ID N)
    v
Source Operator ---- [Barrier N] ----->
                                       +-------------------------+
                 ---- 이벤트 ----------> |  Operator A             |
                 ---- [Barrier N] -----> |  Barrier 수신           |
                                       |  -> 현재 상태 스냅샷 저장 |
                                       |  -> Barrier 하류로 전달  |
                                       +------------+------------+
                                                    | Barrier N 전달
                                                    v
                                       +-------------------------+
                                       |  Sink Operator          |
                                       |  모든 입력 Barrier N 수신|
                                       |  -> 체크포인트 완료 확인  |
                                       +-------------------------+
                                                    |
                                       JobManager에 완료 보고
```

**Barrier (배리어)**: 체크포인트 ID를 담은 특수 마커 메시지. 데이터 스트림에 삽입되어 각 연산자가 배리어 도착 시점의 상태를 스냅샷으로 저장하게 한다.

### 2. Checkpoint 설정

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// 체크포인트 활성화 (30초 간격)
env.enableCheckpointing(30_000);

// 체크포인트 옵션
CheckpointConfig config = env.getCheckpointConfig();
config.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);  // 정확히 한 번
config.setMinPauseBetweenCheckpoints(5_000);                  // 최소 5초 간격
config.setCheckpointTimeout(60_000);                          // 타임아웃 60초
config.setMaxConcurrentCheckpoints(1);                        // 동시 체크포인트 1개
// 외부 저장 체크포인트: 앱 종료 후에도 체크포인트 유지
config.enableExternalizedCheckpoints(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
);
```

### 3. Savepoint 운영

```bash
# 실행 중인 잡에 세이브포인트 트리거
flink savepoint <jobId> hdfs:///flink/savepoints

# 세이브포인트에서 재시작 (코드 업그레이드 후)
flink run -s hdfs:///flink/savepoints/savepoint-xxxxx \
          -c com.example.MyJob \
          my-job-v2.jar

# 세이브포인트 삭제
flink savepoint -d hdfs:///flink/savepoints/savepoint-xxxxx

# 세이브포인트 목록 확인 (REST API)
curl http://flink-jobmanager:8081/jobs/overview
```

### 4. 체크포인트 및 세이브포인트 저장 구조

| 구성 요소 | 저장 내용 |
|:---|:---|
| 연산자 상태 스냅샷 | KeyedState, OperatorState의 직렬화된 데이터 |
| 메타데이터 | 체크포인트 ID, 연산자 ID, 저장 경로 |
| 오프셋 정보 | Kafka 소스의 읽기 오프셋 (Exactly-Once 재시작용) |

**📢 섹션 요약 비유**
> Chandy-Lamport 알고리즘의 배리어는 "강을 따라 흘러가는 부표(Barrier)"와 같다. 각 어부(연산자)는 부표가 자기 앞을 지나는 순간 지금까지 잡은 물고기(상태)를 기록하고, 부표를 다음 강(하류 연산자)으로 보낸다.

---

## Ⅲ. 비교 및 연결

### 1. 체크포인트 모드 비교

| 모드 | 동작 | 장점 | 단점 |
|:---|:---|:---|:---|
| EXACTLY_ONCE | 배리어 정렬 후 스냅샷 | 정확히 한 번 보장 | 배리어 정렬 지연 |
| AT_LEAST_ONCE | 배리어 미정렬 | 낮은 지연 | 중복 처리 가능 |

### 2. 세이브포인트와 코드 변경

세이브포인트는 연산자 UID(Unique ID)를 기반으로 상태를 복원한다.

```java
// 연산자에 고정 UID 지정 (세이브포인트 호환성을 위해 필수)
stream
    .map(new MyMapper()).uid("my-mapper-uid")      // UID 명시적 지정
    .keyBy(e -> e.getUserId())
    .process(new MyProcess()).uid("my-process-uid");
```

UID 없이는 자동 생성 UID가 코드 변경마다 달라져 세이브포인트에서 상태를 복원하지 못할 수 있다.

**📢 섹션 요약 비유**
> 세이브포인트의 연산자 UID는 "직원 사번"과 같다. 이름(코드)이 바뀌어도 사번(UID)이 같으면 같은 직원으로 인식하고 기존 업무 내용(상태)을 이어받을 수 있다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. 운영 시나리오별 사용 가이드

| 시나리오 | 권장 도구 |
|:---|:---|
| 장애 자동 복구 | 체크포인트 (자동) |
| Flink 버전 업그레이드 | 세이브포인트 -> 업그레이드 -> 세이브포인트 재시작 |
| 비즈니스 로직 코드 변경 배포 | 세이브포인트 -> 배포 -> 세이브포인트 재시작 |
| 클러스터 마이그레이션 | 세이브포인트 -> 새 클러스터에서 재시작 |
| A/B 테스트 (같은 상태로 분기) | 세이브포인트 -> 두 잡에 각각 재시작 |

### 2. 체크리스트

- [ ] 체크포인트 간격: 30초~5분 (지연-오버헤드 트레이드오프)
- [ ] 체크포인트 저장소: HDFS/S3 (내구성 있는 분산 스토리지)
- [ ] 연산자 UID 명시적 지정 (`uid("...")`) — 세이브포인트 호환성 필수
- [ ] RocksDB StateBackend 사용 시 체크포인트 크기 증가 고려
- [ ] 배포 전 세이브포인트 생성 자동화 (CI/CD 파이프라인 통합)

**📢 섹션 요약 비유**
> 체크포인트-세이브포인트 전략은 "집 열쇠 관리"와 같다. 자동 체크포인트는 "스마트 잠금장치가 매 30분마다 현재 상태 기록"이고, 세이브포인트는 "이사 전 집 열쇠 복사본 만들기"다. 이사(업그레이드)후에도 새 집(클러스터)에서 복사본(세이브포인트)으로 들어갈 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| Exactly-Once 장애 복구 | 체크포인트로 중복/누락 없이 재시작 |
| 무중단 배포 | 세이브포인트 기반 코드 업그레이드 |
| 상태 이식성 | 세이브포인트로 클러스터 간 상태 이전 |
| 실험적 분기 | 같은 세이브포인트에서 여러 버전 테스트 |

### 2. 결론

Flink의 체크포인트와 세이브포인트는 <strong>상태 기반 스트리밍의 신뢰성과 운영성을 보장하는 두 기둥</strong>이다. 학습 정리에서는 Chandy-Lamport 알고리즘의 배리어 메커니즘, 체크포인트(자동·장애 복구)와 세이브포인트(수동·업그레이드)의 차이, 연산자 UID의 중요성을 논리적으로 서술하는 것이 핵심이다.

**📢 섹션 요약 비유**
> Flink의 체크포인트는 "비행 중 자동 기록되는 블랙박스"이고, 세이브포인트는 "파일럿이 장거리 비행 전 수동으로 만드는 비행 계획서 사본"이다. 사고(장애)는 블랙박스로 분석하고, 항로 변경(업그레이드)은 계획서 사본으로 새 항로를 이어간다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Chandy-Lamport 알고리즘 | 구현 기반 | 배리어 기반 글로벌 스냅샷 |
| Exactly-Once Semantics | 목적 | 체크포인트가 달성하는 처리 보장 수준 |
| State Backend | 저장 위치 | Heap/RocksDB -> HDFS/S3 체크포인트 |
| JobManager | 조율자 | CheckpointCoordinator가 내장 |
| Kafka Offset | 연동 개념 | 체크포인트에 오프셋 함께 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[스트리밍 상태 (Streaming State) — 연산자 상태]
    |
    v
[Chandy-Lamport 알고리즘 (글로벌 스냅샷)]
    |
    v
[체크포인트 (Checkpoint) — 자동 장애 복구]
    |
    v
[세이브포인트 (Savepoint) — 수동 버전 마이그레이션]
    |
    v
[정확히 한 번 처리 (Exactly-Once Semantics)]
```

스트리밍 처리의 신뢰성이 글로벌 스냅샷 이론에서 자동 체크포인트와 수동 세이브포인트를 거쳐 정확히 한 번 처리로 실현된 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

게임을 하다가 갑자기 정전이 나도(장애) 자동 저장(체크포인트)이 되어 있으면 아까 하던 곳에서 다시 시작할 수 있어요. 새로운 캐릭터 스킨(코드 업그레이드)을 입히기 전에는 특별 저장 슬롯(세이브포인트)에 수동으로 저장해 두어야 해요. 연산자 UID는 캐릭터의 이름을 바꿔도 "이 캐릭터가 내 캐릭터임"을 증명하는 고유 번호예요!
