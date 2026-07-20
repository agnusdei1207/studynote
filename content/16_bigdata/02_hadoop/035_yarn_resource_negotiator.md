---
title: "Yarn Resource Negotiator"
date: "2026-03-04"
tags:
  - "studynote-bigdata"
weight: 35
---
## 핵심 인사이트 (3줄 요약)
- 하둡 2.0에서 도입되어, 단순 맵리듀스 전용 자원 관리 구조를 탈피하고 범용 분산 처리를 가능케 한 차세대 클러스터 OS임.
- 중앙 자원 관리자(Resource Manager)와 개별 앱별 관리자(Application Master)를 분리하여 확장성(Scalability)을 극대화함.
- 스파크(Spark), 플링크(Flink) 등 다양한 워크로드가 동일 클러스터 자원을 공유하여 실행될 수 있게 하는 멀티 테넌시(Multi-tenancy)의 핵심임.

### Ⅰ. 개요 (Context & Background)
하둡 1.0의 맵리듀스는 '자원 관리'와 '작업 모니터링'이 JobTracker 하나에 집중되어 병목 현상이 심했고, 오직 맵리듀스 코드만 실행 가능했다. 시스템 설계 관점에서 YARN(Yet Another Resource Negotiator)은 이 책임을 분산시켜 하둡을 '데이터 처리 애플리케이션 플랫폼'으로 진화시킨 핵심 아키텍처이다. CPU, 메모리 자원을 '컨테이너(Container)' 단위로 쪼개어 효율적으로 배분함으로써 클러스터 가동률을 비약적으로 높였다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
YARN은 크게 4가지 컴포넌트로 구성되며, 각 노드와 애플리케이션의 상태를 계층적으로 관리한다.

```text
[ YARN Cluster Architecture ]

         +-----------------------------+
         |      Resource Manager       | (Global Master)
         | [Scheduler] [App Manager]   |
         +--------------+--------------+
                        | (1. Request Container)
      +-----------------+-----------------+
      |                 |                 |
+-----+-------+   +-----+-------+   +-----+-------+
| Node Manager |   | Node Manager |   | Node Manager | (Slave)
| [Container]  |   | [App Master] |   | [Container]  |
+--------------+   +--------------+   +--------------+

[ Bilingual Core Components ]
- Resource Manager (RM): 클러스터 전체 자원(Total CPU/RAM) 관리 및 스케줄링.
- Node Manager (NM): 개별 워커 노드의 자원 사용 현황 모니터링 및 보고.
- Application Master (AM): 특정 작업(Job) 전담. RM과 자원 협상 후 NM에서 작업 실행.
- Container (컨테이너): CPU, Memory 등 자원 할당의 최소 논리 단위.
```

애플리케이션이 실행될 때 RM은 먼저 AM을 띄울 컨테이너 하나를 할당하고, 그 AM이 자신의 작업을 위해 추가 컨테이너를 RM에게 요청하여 실제 연산을 수행하는 '이중화된 협상' 구조를 가진다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 하둡 1.0 (JobTracker) | 하둡 2.0+ (YARN) |
| :--- | :--- | :--- |
| **자원 관리 단위** | 슬롯 (Map Slot, Reduce Slot) | <strong>컨테이너 (Generic Container)</strong> |
| **확장성 한계** | 노드 약 4,000대 수준 | <strong>노드 10,000대 이상 무한 확장</strong> |
| **다양성** | 오직 맵리듀스만 실행 | <strong>Spark, Flink, Hive 등 병행 실행</strong> |
| **장애 영향** | JT 장애 시 전체 클러스터 정지 | AM 장애는 해당 앱에만 국한됨 |
| **실무적 판단** | "데이터 처리 전용 엔진" | <strong>"분산 자원 운영체제(Cluster OS)"</strong> |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>(스케줄러 선택)</strong> 실무에서는 작업 성격에 따라 FIFO, Capacity(용량별 할당), Fair(모든 앱에 균등 배분) 스케줄러 중 하나를 선택해야 한다. 일반적으로 다수의 부서가 공유하는 환경에서는 <strong>Capacity Scheduler</strong>가 권장된다.
- **(자원 격리)** NM은 CGroups(Control Groups)를 통해 컨테이너 간의 자원 간섭을 물리적으로 제한하여, 특정 작업이 전체 노드의 CPU를 고갈시키는 현상을 방지해야 한다.
- **(Liveness 점검)** RM과 NM 간의 하트비트(Heartbeat) 통신 장애 시, YARN은 즉시 해당 노드의 작업을 다른 노드로 재할당(Re-run)하여 무결성을 보장한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
YARN은 하둡 생태계가 10년 넘게 살아남을 수 있었던 '심장'과 같은 기술이다. 현재는 쿠버네티스(Kubernetes)가 클라우드 네이티브 환경에서 그 역할을 대신하고 있지만, 대규모 온프레미스 빅데이터 클러스터에서는 여전히 YARN이 독보적인 성능을 보여준다. 향후 GPU 가속기 지원 강화 등 이종 자원(Heterogeneous Resources) 관리가 강화될 전망이다. 실무자는 YARN과 K8s의 특성을 이해하고 하이브리드 인프라 설계 역량을 갖추어야 한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- <strong>HDFS</strong>: 데이터가 저장된 물리 계층
- <strong>MapReduce / Spark</strong>: YARN 위에서 돌아가는 앱
- **Resource Manager**: 중앙 통제실
- <strong>Kubernetes (K8s)</strong>: 현대적 대안 플랫폼

### 📈 관련 키워드 및 발전 흐름도

```text
[하둡 v1 JobTracker — 리소스 관리와 작업 스케줄링을 단일 노드에서 담당, 병목]
    |
    v
[YARN (Yet Another Resource Negotiator) — ResourceManager·NodeManager 분리 아키텍처]
    |
    v
[ApplicationMaster — 각 앱이 자체 스케줄링 담당, 프레임워크 독립성 확보]
    |
    v
[컨테이너 (Container) — CPU·메모리 단위 자원 할당, 다중 프레임워크 공존]
    |
    v
[Kubernetes on YARN / 클라우드 네이티브 — YARN을 대체하는 컨테이너 오케스트레이션]
```

이 흐름은 하둡 v1의 JobTracker 병목을 해결하기 위해 YARN이 ResourceManager·ApplicationMaster로 분리 진화하고, 이후 Kubernetes 기반 클라우드 네이티브 스케줄러로 대체되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 학교 도서관에서 친구들이 각자 공부할 '책상(자원)'이 필요하다고 해보자.
- YARN은 누가 어떤 책상을 얼마나 오래 쓸지 결정하고 나눠주는 '도서관 선생님'이야.
- 선생님 덕분에 어떤 친구는 수학을 하고, 어떤 친구는 국어를 해도 서로 방해하지 않고 공부할 수 있단다!
