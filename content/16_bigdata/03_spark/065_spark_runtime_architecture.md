---
title: "Executor / Driver / Cluster Manager"
date: "2024-03-23"
tags:
  - "studynote-bigdata"
weight: 65
---
## 핵심 인사이트 (3줄 요약)
- 스파크 런타임 아키텍처는 작업을 총괄하는 드라이버(Driver), 실제 연산을 수행하는 실행기(Executor), 그리고 자원을 중계하는 클러스터 매니저(Cluster Manager)로 구성된다.
- 드라이버는 사용자 코드를 DAG(유향 비순환 그래프)로 변환하여 테스크를 생성하며, 실행기는 할당받은 테스크를 독립된 JVM 프로세스에서 병렬 처리한다.
- 클러스터 매니저는 스파크 애플리케이션 외부에서 CPU/메모리 자원을 동적으로 할당하고 관리하여 다중 사용자 환경에서의 공정성을 보장한다.

### Ⅰ. 개요 (Context & Background)
아파치 스파크의 강력한 성능은 '분산 병렬 처리'에서 나온다. 하지만 수많은 서버가 어떻게 질서 있게 협업하는지 이해하려면 그 이면의 <strong>런타임 아키텍처(Runtime Architecture)</strong>를 파악해야 한다. 드라이버가 전체 전략을 짜고, 클러스터 매니저가 전장을 준비하면, 실행기가 실제 전투(연산)를 수행하는 일련의 유기적 흐름이 스파크의 핵심이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
스파크는 마스터-워커(Master-Worker) 구조를 기본으로 하며, 각 컴포넌트 간의 통신은 전용 프로토콜을 통해 이루어진다.

```text
[ Spark Runtime Components Architecture ]
(스파크 런타임 컴포넌트 아키텍처)

      +------------------------+
      |      Driver Node       |
      | +--------------------+ |
      | | SparkContext/Session| | <----+ (Req/Alloc Resources)
      | | DAG Scheduler      | |      |
      | | Task Scheduler     | |      |
      | +----------+---------+ |      |     +--------------------+
      +------------|-----------+      +---->|  Cluster Manager   |
                   | (Tasks)                | (YARN, K8s, Mesos) |
                   v                        +---------+----------+
      +------------------------+                      |
      |      Worker Node       |                      | (Allocated)
      | +--------------------+ |                      |
      | |     Executor       | | <--------------------+
      | | (JVM Process)      | |
      | | - Tasks / Threads  | |
      | | - Cache / Storage  | |
      | +--------------------+ |
      +------------------------+
```

1. **Driver (드라이버):** 사용자의 `main()` 함수가 실행되는 프로세스다. 고수준 연산을 DAG로 쪼개고, 각 스테이지(Stage)별로 테스크(Task)를 생성해 실행기에게 전달한다.
2. **Executor (실행기):** 워커 노드에서 실행되는 JVM 프로세스다. 드라이버로부터 테스크를 받아 실행하고, 결과를 메모리나 디스크에 저장(Cache)한다. 애플리케이션 종료 시까지 유지된다.
3. **Cluster Manager (클러스터 매니저):** 애플리케이션 간의 자원 할당을 조정한다. YARN(Hadoop), Mesos, Kubernetes, 혹은 스파크 내장 Standalone 매니저가 이 역할을 수행한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 컴포넌트 (Component) | 드라이버 (Driver) | 실행기 (Executor) | 클러스터 매니저 (Manager) |
| :--- | :--- | :--- | :--- |
| **주요 역할** | 전체 계획 및 테스크 배포 | 실제 데이터 연산 및 저장 | 자원(CPU/MEM) 할당 중계 |
| **생명 주기** | 애플리케이션의 시작과 끝 | 애플리케이션 실행 중 유지 | 시스템 전반 상주 (공용) |
| **비유** | 오케스트라의 지휘자 | 악기 연주자 (단원) | 공연장 대관 관리자 |
| **실패 시 영향** | 애플리케이션 전체 중단 | 해당 테스크 재실행 가능 | 새로운 앱 실행 불가 |
| <strong>핵심 모니터링</strong> | JVM Heap, DAG 흐름 | CPU 사용률, GC, Shuffle | 할당/가용 리소스 현황 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
**실무적 판단 (Technical Insight):**
런타임 구성 요소 간의 불균형은 성능 저하의 주범이다.
- <strong>Driver OOM:</strong> 드라이버가 너무 많은 데이터를 수집(`collect`)하면 메모리 부족(OOM)으로 전체 앱이 죽는다. 데이터는 최대한 실행기 내에서 처리해야 한다.
- **Dynamic Allocation:** 클러스터 매니저 설정을 통해 워크로드에 따라 실행기 개수를 동적으로 조절하면 클라우드 비용을 획기적으로 줄일 수 있다.
- <strong>Data Locality:</strong> 드라이버는 가급적 데이터가 있는 실행기 노드에 테스크를 배치하려 노력(Scheduling)하여 네트워크 오버헤드를 줄인다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
스파크의 아키텍처는 하둡의 정적인 맵리듀스 구조를 극복하고 탄력적인 분산 컴퓨팅을 완성했다. 최근에는 서버리스(Serverless) 기술과 결합하여 '클러스터 매니저'의 존재감이 인프라 단으로 숨겨지고 있으며, 개발자는 오직 로직(Driver)에만 집중하는 추세다. 하지만 고성능 데이터 처리를 위해선 여전히 각 컴포넌트 간의 상호작용과 메모리 배치 원리를 이해하는 것이 필수적이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념:** Distributed Operating System, Parallel Processing
- **유사 개념:** MapReduce Master/Slave, MPI (Message Passing Interface)
- **하위 개념:** DAG (Directed Acyclic Graph), Shuffle Service, RDD Lineage


### 📈 관련 키워드 및 발전 흐름도

```text
[MapReduce — 디스크 기반 배치, 반복 연산 시 I/O 오버헤드 극심]
    |
    v
[Apache Spark — 인메모리 RDD, Driver-Executor 분산 런타임 아키텍처]
    |
    v
[DAG 스케줄러 (DAG Scheduler) — 스테이지·태스크 분리, 파이프라인 최적화]
    |
    v
[클러스터 매니저 (YARN / Kubernetes) — 리소스 할당·컨테이너 수명 관리]
    |
    v
[Spark Structured Streaming — 마이크로 배치로 배치·스트리밍 통합 처리]
```

이 흐름은 디스크 I/O 병목의 MapReduce에서 인메모리 Spark으로 패러다임이 전환되고, DAG 스케줄러로 최적화된 뒤 클러스터 매니저와 통합되며 Structured Streaming으로 배치·스트리밍이 통합되는 Spark 아키텍처 진화를 보여준다.


### 👶 어린이를 위한 3줄 비유 설명
- 거대한 레고 성을 만드는 팀워크와 같아요.
- 설계도를 보고 "너는 성벽, 너는 지붕을 만들어"라고 지시하는 대장이 '드라이버'예요.
- 실제로 브릭을 끼우고 만드는 팀원이 '실행기'이고, 이들에게 레고 브릭과 책상을 빌려주는 관리자가 '클러스터 매니저'랍니다!
