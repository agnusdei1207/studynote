---
title: "Flink Architecture"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 81
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Apache Flink (아파치 플링크)의 아키텍처는 클러스터를 조율하는 JobManager (잡매니저)와 실제 연산을 실행하는 TaskManager (태스크매니저)의 마스터-워커 구조로, 사용자 프로그램을 JobGraph (잡 그래프, DAG)로 변환하고 각 연산자(Operator)를 태스크로 분해하여 분산 실행한다.
- **가치**: Flink는 진정한 이벤트 단위(Per-Event) 처리와 정밀한 상태(State) 관리 메커니즘을 제공하여, Spark의 마이크로배치 대비 지연 시간이 수 배 낮고 이벤트 시간(Event Time) 처리의 정확도가 높다.
- **판단 포인트**: Flink의 강점은 <strong>체크포인팅 기반 Exactly-Once</strong> 보장과 <strong>풍부한 상태 백엔드(State Backend)</strong> 선택지(Heap, RocksDB)이며, 고처리량(High Throughput)보다 <strong>저지연(Low Latency) + 상태 정확성</strong>이 요구되는 워크로드에 최적이다.

---

## Ⅰ. 개요 및 필요성

### 1. Flink의 탄생 배경

2010년 베를린 공과대학(TU Berlin)의 연구 프로젝트 Stratosphere에서 시작한 Flink는 배치와 스트리밍을 <strong>통합된 연산 모델</strong>로 처리하려는 목표로 설계됐다. 핵심 철학은 "배치 처리는 유한한 스트림(Bounded Stream)이다"라는 관점이다.

### 2. Flink vs 1세대 스트리밍 엔진

| 항목 | Apache Storm | Spark Streaming (DStream) | Apache Flink |
|:---|:---|:---|:---|
| 처리 방식 | 이벤트 단위 | 마이크로배치 | 이벤트 단위 |
| 상태 관리 | 사용자 책임 | 제한적 | 풍부한 내장 State API |
| Exactly-Once | 어려움 | 가능 | 기본 제공 |
| 이벤트 시간 처리 | 미지원 | 제한적 | 완전 지원 (Watermark) |

**📢 섹션 요약 비유**
> Flink의 등장은 "1세대 스마트폰과 현재 스마트폰의 차이"다. Storm이 통화만 되는 구형 스마트폰이라면, Flink는 GPS·카메라·앱 모두 갖춘 최신 스마트폰이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Flink 클러스터 아키텍처

```
+-----------------------------------------------------------------+
|  클라이언트 (Client)                                             |
|  · 사용자 코드 컴파일 -> JobGraph 생성                            |
|  · JobGraph를 JobManager에 제출                                  |
+----------------------------+------------------------------------+
                             | JobGraph 제출
                             v
+-----------------------------------------------------------------+
|  JobManager (마스터)                                             |
|                                                                 |
|  +------------------+  +------------------+  +--------------+  |
|  | Dispatcher       |  |  JobMaster        |  | ResourceMgr  |  |
|  | (잡 수신·등록)   |  |  (잡 조율·실행)   |  | (자원 관리)  |  |
|  +------------------+  +------------------+  +--------------+  |
|                                                                 |
|  · Checkpoint Coordinator (체크포인트 조율)                      |
|  · High Availability: ZooKeeper 기반 리더 선출                  |
+----------------------------+------------------------------------+
                             | Task 배포
                +------------+------------+
                v            v            v
+-----------------+ +-----------------+ +-----------------+
|  TaskManager 1  | |  TaskManager 2  | |  TaskManager N  |
|                 | |                 | |                 |
|  Task Slot: 4   | |  Task Slot: 4   | |  Task Slot: 4   |
|  +---+ +---+   | |  +---+ +---+   | |  ...            |
|  |T1 | |T2 |   | |  |T3 | |T4 |   | |                 |
|  +---+ +---+   | |  +---+ +---+   | |                 |
+-----------------+ +-----------------+ +-----------------+
```

### 2. 핵심 구성 요소

| 구성 요소 | 역할 | 특징 |
|:---|:---|:---|
| JobManager | 클러스터 조율자 | JobGraph 실행 조율, 체크포인트 트리거, 장애 복구 |
| Dispatcher | 잡 수신 및 등록 | REST API로 잡 제출 수신, JobMaster 생성 |
| JobMaster | 단일 잡 조율 | ExecutionGraph 유지, 태스크 스케줄링 |
| ResourceManager | 자원 관리 | TaskManager의 TaskSlot 관리, YARN/K8s 통합 |
| TaskManager | 실행 노드 | 실제 연산자(Operator) 실행, JVM 프로세스 1개 |
| TaskSlot | 실행 단위 | TaskManager 내 격리된 실행 공간, 메모리 분할 |

### 3. JobGraph와 ExecutionGraph 변환 과정

```
사용자 코드 (DataStream/Table API)
    |
    v
StreamGraph (논리적 연산자 DAG)
    | 연산자 체이닝 (Operator Chaining)
    v
JobGraph (체이닝 최적화된 DAG, 클라이언트->JobManager 전송)
    | 병렬도(Parallelism) 적용
    v
ExecutionGraph (물리적 실행 계획, 태스크 인스턴스 포함)
    |
    v
TaskManager의 Task Slot에 배포·실행
```

<strong>연산자 체이닝(Operator Chaining)</strong>: 네트워크 I/O 없이 연결 가능한 연산자들을 하나의 스레드에서 실행 -> 직렬화/역직렬화 비용 제거

**📢 섹션 요약 비유**
> Flink 아키텍처는 "건설 현장 구조"와 같다. JobManager는 현장 소장(전체 조율), ResourceManager는 인력 파견 회사(TaskSlot 관리), TaskManager는 각 시공팀(실제 작업), Task Slot은 팀원 개인(격리된 실행 공간)이다.

---

## Ⅲ. 비교 및 연결

### 1. Flink vs Spark 아키텍처 비교

| 비교 항목 | Apache Spark | Apache Flink |
|:---|:---|:---|
| 마스터 | Driver (단일) | JobManager (HA 가능) |
| 워커 | Executor | TaskManager |
| 실행 단위 | Task (파티션) | Task (TaskSlot) |
| 스트리밍 방식 | 마이크로배치 | 이벤트 단위 |
| 상태 백엔드 | 없음 (RDD/DataFrame) | Heap / RocksDB StateBackend |
| 체크포인트 | 수동 (RDD), 자동 (Streaming) | 자동 (Chandy-Lamport 알고리즘) |

### 2. Flink State Backend 선택

| 백엔드 | 저장 위치 | 적합한 상황 |
|:---|:---|:---|
| HashMapStateBackend | JVM Heap | 소규모 상태, 빠른 접근 |
| EmbeddedRocksDBStateBackend | 로컬 디스크 (RocksDB) | 대용량 상태 (GB~TB) |
| 체크포인트 저장소 | HDFS/S3 | 모든 백엔드의 체크포인트 저장 |

**📢 섹션 요약 비유**
> Flink의 State Backend 선택은 "작업 도구 보관 방식"이다. 자주 쓰는 작은 도구(소규모 상태)는 책상 위(Heap)에, 부피 큰 장비(대용량 상태)는 창고(RocksDB)에 보관한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Flink 클러스터 구성 체크리스트

- [ ] JobManager HA 설정: ZooKeeper 기반 리더 선출 구성
- [ ] TaskManager 메모리 튜닝: `taskmanager.memory.process.size` (최소 4GB 권장)
- [ ] TaskSlot 수 = CPU 코어 수 (일반적으로 1:1)
- [ ] State Backend: 상태 크기가 수 GB 초과 -> RocksDB 선택
- [ ] 체크포인트 간격: 기본 10초 (지연-오버헤드 트레이드오프)
- [ ] 병렬도(Parallelism): TaskSlot 총 수와 일치하도록 설정

### 2. Flink 고가용성(HA) 설정

```yaml
# flink-conf.yaml (고가용성 설정)
high-availability: zookeeper
high-availability.zookeeper.quorum: zk1:2181,zk2:2181,zk3:2181
high-availability.storageDir: hdfs:///flink/ha/
high-availability.zookeeper.path.root: /flink
```

**📢 섹션 요약 비유**
> Flink의 HA 설정은 "회사에 부장이 2명이지만 항상 1명만 결재권을 가지는 구조"다. ZooKeeper가 어느 JobManager가 현재 리더인지 결정하고, 리더가 쓰러지면 즉시 후보(Standby)를 리더로 승격시킨다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 저지연 처리 | 이벤트 단위 처리로 밀리초~수 초 지연 달성 |
| Exactly-Once 보장 | 체크포인팅 기반 정확히 한 번 처리 |
| 대규모 상태 관리 | RocksDB로 TB 규모 상태도 안정적 처리 |
| 배치+스트리밍 통합 | 동일 API로 유한/무한 데이터 처리 |

### 2. 결론

Flink 아키텍처의 핵심은 <strong>JobManager의 중앙 조율 + TaskManager의 분산 실행 + 체크포인팅 기반 상태 내구성</strong>이다. 학습 정리에서는 JobManager/TaskManager/TaskSlot의 역할을 명확히 구분하고, 연산자 체이닝과 JobGraph->ExecutionGraph 변환 과정, 그리고 HA 설계 고려사항을 함께 서술하면 완성도 높은 답안이 된다.

**📢 섹션 요약 비유**
> Flink 클러스터는 "세계적인 교향악단"과 같다. 지휘자(JobManager)가 악보(JobGraph)를 보며 각 파트(TaskManager)에 지시하고, 각 단원(TaskSlot)이 자기 파트를 정확히 연주한다. 지휘자가 쓰러져도(HA) 부지휘자(Standby JobManager)가 즉시 지휘봉을 잡는다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Checkpoint (Flink) | 핵심 메커니즘 | 체크포인트 코디네이터가 JobManager에 내장 |
| DataStream API | 프로그래밍 인터페이스 | JobGraph 생성의 원천 |
| State Backend | 상태 저장 | TaskManager의 로컬 상태 저장 방식 |
| ZooKeeper | HA 의존성 | JobManager 리더 선출 |
| Operator Chaining | 최적화 기법 | JobGraph 내 연산자 통합으로 네트워크 비용 절감 |

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 처리 (Batch Processing)]
    |
    v
[스트림 처리 (Stream Processing)]
    |
    v
[Apache Flink (Apache Flink)]
    |
    v
[이벤트 시간 (Event Time)]
```

이 흐름도는 배치 처리와 스트림 처리가 Apache Flink와 이벤트 시간 모델로 통합되는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

Flink 클러스터는 큰 공장 같아요. 사장님(JobManager)이 공장 전체 일정을 관리하고, 각 작업 팀장(TaskManager)이 팀원들(TaskSlot)을 이끌며 실제 물건을 만들어요. 공장이 쓰러지지 않도록 부사장님(Standby JobManager)이 항상 대기하고, 매 10초마다 진행 상황을 창고(HDFS)에 저장해 두어서 정전이 나도 다시 시작할 수 있어요!
