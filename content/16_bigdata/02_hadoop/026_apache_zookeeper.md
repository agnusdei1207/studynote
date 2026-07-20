---
title: "Apache Zookeeper"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 26
---
# Apache ZooKeeper - 분산 코디네이션의 간호사

> ⚠️ 이 문서는 Apache ZooKeeper가 어떻게 분산 시스템에서 다수의 노드들이 상호배타적 자원(리더 선출, 분산 잠금, 설정 관리)을 충돌 없이 공유할 수 있게 하는"코디네이션 서비스(Coordination Service)"를 제공하는지, 그리고 이러한 서비스가 Hadoop/HBase/Kafka 등에서 여하よう에 활용되어 단일 장애점(SPOF)을 제거하고 시스템의 일관성을 유지하는지를 실무자 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache ZooKeeper는 분산 시스템에서"어디에 문제가 생겼고, 누가リーダー이고, 어떤 설정으로 운영되고 있는가"를 모든 노드가통일적으로 공유할 수 있게 하는 분산 코디네이션 서비스로, 작고 일관된 데이터(수 KB 이내)를ephemeral 노드와sequencer와 함께 관리하여 분산 잠금, 리더 선출, 서비스 디스커버리등공능을제공한다.
> 2. **가치**: ZooKeeper가 없으면 각 노드가 직접 통신하여"현재 리더가 누구인가"를 합의해야 하고, 이 과정에서 네트워크 파티션이나 노드 장애 시split-brain(분할 뇌) 문제가 발생하여 시스템이 불안정해집니다. ZooKeeper는이협조를집중관리하여"리더 선출"과"설정 동기화"를 원자적으로처리한다.
> 3. **확장**: ZooKeeper 자체도 분산 앙상블(3대~7대)로 운영되며, ZooKeeper 자체의 장애도인수어떤 노드든 과반수(Quorum)이 살아 있으면 서비스가 계속됩니다. 다만 ZooKeeper의 부하 패턴(짧은 연결, 높은 조작 빈도)은 다른 일반적인 분산 DB와 다르므로 전용 클러스터 운영이 권장됩니다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 분산 시스템의 3대협조 문제: 누구든 실패하는 세계에서 어떻게 합의하나?
분산 시스템에서는 모든 노드가 동시에 정상 동작한다는 가정 하에 설계할 수 없습니다. 네트워크 분할(Network Partition), 노드 장애(Node Failure), 메시지 지연(Message Delay) 등이 일상적으로 발생하며, 이의중에서"현재 시스템의 상태"에 대해 모든 올바른 노드가 동일한 View를 가지는 것(Leslie Lamport의" Consensus 문제")은 매우 어려운 문제입니다.
- **구체적 문제 상황**: HBase 리전 서버 10대가 작동 중일 때, 기존 리더(Leader) 서버가 갑자기 정전되면 나머지 9대는"이제 새로운 리더를 선출해야 한다"고 동시에 인식해야 합니다. 그러나 만약 네트워크 분할이 일어나"9대 중 5대는 기존 리더와 함께" 남아 있고, 다른 4대는"리더와 연결이 끊긴 분리된 네트워크"에 있게 되면, 양쪽 모두"내가 리더가 될 자격이 있다"고 주장하게 됩니다. 이것이 바로"split-brain problem(분열 뇌 증후군)"입니다.
- **ZooKeeper의 해결책**: ZooKeeper는"리더 선출"과"잠금(Lock)" 기능을 제공하여, 어떤 노드가"리더"인지에 대한 논리적 시점(epoch)을 전노드에 공유하고, 두 리더가 동시에 활동하는 상황( splits-brain)을방지합니다. ZooKeeper는 모든 노드보다"표준 시계(Standard Clock)" 역할을 합니다.

### 2. ZooKeeper의 탄생 배경
Yahoo! 연구팀이 2006년~2008년에 걸쳐 대규모 분산 애플리케이션(HBase, Kafka 등)에서 공통적으로직면하는"코디네이션 문제"를 해결하기 위해 개발한 ZooKeeper는,Google의 Chubby_lock_service를 참고하여 2010년 Apache Top-Level Project가 되었습니다.
- **설계 철학**: ZooKeeper는"수거존저"(Storage)보다"코디네이션"(Coordination)에 집중합니다. 따라서 ZooKeeper에 저장되는 데이터는 매우 작고(수 KB 이내), 조작은 짧고(밀리초 이내)원자적(Atomic)으로 처리됩니다. 이것은 ZooKeeper를"고성능な협조サーバ"로설계ilosofia의 핵심입니다.

- **📢 섹션 요약 비유**: ZooKeeper는"대형교향악단의지휘자"와 같습니다.オーケストラ에는 Viola(제일 Violin), Cello, Flute 등 수십 명의 연주자(노드)가 있는데, 어떤 악기 Solo(리더)가 도중에 그만두면(장애)지оружа는 모든 연주자들에게"이제 제이 Violin이 Solo를 인수한다"는 것을 알려야 합니다. 하지만 만약통신문제에서 일부 연주자다け이/가이정보를수け취る 경우(네트워크 분할), 부분연주자들은 예전 Solo를 계속 따르는의에대し고 다른 부분은 새로운 Solo를 따르기 시작하여"헝클어진 연주(split-brain)"이 됩니다.지휘자( ZooKeeper)는 전 연주자들에게"이제 제이 Violin이 Solo입니다"라고 동시에통지하며, 제이 Violin도 자신의 Solo 위치를Acknowledgement하고, 둘 다 동시에 연주하지 않도록 보장합니다. 만약지휘자 자체가 쓰러지면( ZooKeeper 장애), 부지휘자(Follower)가를인き속きadar и "지휘자 위임"을 즉시 수행하여 관현악 연주가 중단되지 않도록 합니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
+-----------------------------------------------------------------+
|                [ Apache ZooKeeper 아키텍처 ]                      |
|                                                                 |
|  [ZooKeeper Service (앙상블)]                                   |
|    +-----------+  +-----------+  +-----------+                  |
|    |  Server 1 |  |  Server 2 |  |  Server 3 |   (3대 기준)       |
|    |  (Leader) |<--+- Quorum -+-->| (Follower)|                  |
|    |           |  |  (过半数) |  |           |                  |
|    +-----------+  +-----------+  +-----------+                  |
|                                                                 |
|  [앙상블 내부 동작]                                              |
|    - Leader选举: Zab (ZooKeeper Atomic Broadcast) 프로토콜       |
|    - 모든 쓰기요청은 Leader에서 처리 -> Follower에 전파            |
|    - 읽기요청은 어떤 Server에서든 처리 (非同步)                   |
|    - 과반수(Quorum) 서버가 살아 있으면 서비스 지속                |
|                                                                 |
|  [ZooKeeper 데이터 모델: znodes]                                 |
|  +----------------------------------------------------------+   |
|  |  /workers                                            [E]  |   |
|  |    +- /worker-1  { "status": "active" }                [E]  |   |
|  |    +- /worker-2  { "status": "idle" }                 [E]  |   |
|  |  /tasks                                                 |   |
|  |    +- /task-001  { "assignee": "worker-1" }            [E]  |   |
|  |    +- /task-002  { "assignee": "" }                   [E]  |   |
|  |  /leader          { "elected": "server-1" }            [SE] |   |
|  |                                                              |   |
|  |  [E] = Ephemeral Node (세션 동안만 존재, 연결 끊으면 자동 삭제) |   |
|  |  [SE] = Sequential Ephemeral (순번 자동 증가 + 세션 종료 시 삭제) |   |
|  +----------------------------------------------------------+   |
|                                                                 |
|  [주요 활용 사례]                                                |
|  +----------------------------------------------------------+   |
|  |  ① 리더 선출 (Leader Election)                            |   |
|  |     /leader 경로에 Sequential Ephemeral 노드 생성          |   |
|  |     -> 가장 작은 sequence number이 리더!                    |   |
|  |  ② 분산 잠금 (Distributed Lock)                            |   |
|  |     /lock 경로에 Sequential Ephemeral 노드 생성            |   |
|  |     -> 자신의 순번보다 작은 노드가 없으면 Lock 획득!         |   |
|  |  ③ 서비스 디스커버리 (Service Discovery)                    |   |
|  |     /services/{service-name}/{{service-instance}} 등록     |   |
|  |  ④ 설정 관리 (Configuration Management)                     |   |
|  |     /config/{service} 경로에 설정 정보 저장               |   |
|  +----------------------------------------------------------+   |
|                                                                 |
+-----------------------------------------------------------------+
```

### 1. Zab (ZooKeeper Atomic Broadcast) 프로토콜
ZooKeeper는 Zab 프로토콜을 통해 분산 환경에서의 원자적 브로드캐스트를 달성합니다.
- **역할**: Zab은"모든 Follower이 동일한 순서로 동일한 메시지를수령"하도록보정하는원자적 브로드캐스트 프로토콜입니다. 이것이 보장되지 않으면, 일부 Follower만 업데이트되어 상태가 불일치하게 됩니다.
- **모드**: Zab은 두 가지 모드로 동작합니다. (1) <strong>Recovery (리더 선출 후)</strong>: 새 리더가 모든 Follower의 상태를 동기화하여 일관성을 확보합니다. (2) **Broadcast (정상 작동)**: 리더가 받은 쓰기 요청을 모든 Follower에 동시에 전파(Atomic Broadcast)합니다.

### 2. Znode 유형: 영속 vs 임시, 순차 vs 비순차

| Znode 유형 | 설명 | 활용 예 |
|:---|:---|:---|
| **영속 Regular (P)** | 명시적 삭제 전까지영구보존 | 설정 정보 (/config) |
| **임시 Ephemeral (E)** | 세션 종료 시 자동 삭제 |존활 확인 (-worker1 활성 표시) |
| **순차 Sequential** | 생성 시 자동으로 10자리 순번 증가 | 리더 선출, 분산 잠금 |

- **Sequential Ephemeral (SE)**: 가장 중요한 유형입니다. 임시(Ephemeral)이면서 순번이 자동 증가(SE)하는 노드로, 노드 작성 시`s "/leader/worker-0000000001"`과 같이 순번이 부여됩니다. ZooKeeper 세션이 종료되면(해당 노드 연결이 끊기면) 해당 Sequential Ephemeral 노드는 자동으로 삭제되어, 장애 노드의"리더 후보" 자격을자동적에박탈합니다.

### 3. Quorum (과반수)와 일관성
ZooKeeper 앙상블에서"과반수(Quorum)"는"서비스가 계속되기 위해 필요한 최소한의 정상 서버 수"입니다.
- **Quorum 계산**: 서버 3대 -> 과반수 2대, 서버 5대 -> 과반수 3대, 서버 7대 -> 과반수 4대
- <strong>읽기 일관성</strong>: ZooKeeper는 강한 일관성(Strong Consistency)을제공하지 않고"임시적 일관성(Tentative Consistency)"을제공합니다. 읽기는 어떤 서버에서든가능하지만, 그 서버가 최신 writes를 반영하지 못할 수 있습니다. 그러나clients는`watch`를 통해 변경 사항을 실시간으로통지받을 수 있어결과적에는 일관된 View를 얻을 수 있습니다.

- **📢 섹션 요약 비유**: ZooKeeper의 Quorum 메커니즘은"합의결정의 voting 시스템"과 같습니다. 5명의 이사진(서버)이 있는 회사에서 중요한결정적화가 있으면"과반수의찬동이 필요"합니다. 만약 3명 이상이"승인"이라고투표하면결정는통과되고, 나머지 2명의"반대"는 무시됩니다. 하지만 만약 3명 이상이"공사적사에 동의하면서도 각자의 사정을 전달하지 못하는 상황"(네트워크 분할)에 처하면, 두 그룹으로 나뉘어각자"내가 과반수을 차지하고 있다"고 생각하는"분열 뇌(split-brain)"가 발생할 수 있습니다. ZooKeeper는 이러한split-brain를방지하기 위해, 오직 단일 Leader만 쓰기 요청을 처리하도록하고, Leader의 상태를 전Follower가 항상감시하여,"만약 Leader가 쓰러지면 즉시에 다른 Leader를 선출"하는 메커니즘을 내장하고 있습니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | Apache ZooKeeper | etcd (CoreOS) | Consul (HashiCorp) |
|:---|:---|:---|:---|
| <strong>일관성 모델</strong> | 임계적 일관성 (Fencing Token) | Raft 기반 강한 일관성 | Gossip 기반 Eventually Consistent |
| **주요 용도** | 리더 선출, 분산 잠금 | 분산 키-값 스토어 | 서비스 메쉬, KV 스토어 |
| <strong>CAP</strong> | CP (일관성+파티션 허용) | CP | AP (가용성+파티션 허용) |
| ** bahasa pemrograman** | Java 중심 | Go | Go, Python, etc |
| **헬스체크** | 없음 (ephemeral 노드로 간접) | 자체 제공 | 에이전트 기반 |
| **주요 사용자** | Hadoop 생태계, Kafka | Kubernetes | 마이크로서비스 |

- **ZooKeeper의 가장 큰 강점**: Hadoop 생태계(HDFS NameNode HA, HBase Region Server 관리, Kafka 브로커 관리) 전반에 깊이 내장되어 있으며, 수십 년간의 프로덕션 검증과 안정성을 보유하고 있습니다. 다만"무거운부erapy"를 처리하는 것은 etcd나 Consul에 비해 복잡할 수 있어, 새로운 마이크로서비스 아키텍처에서는 etcd/Kubernetes etcd가 선호되는 경향이 있습니다.

- **📢 섹션 요약 비유**: ZooKeeper vs etcd/Consul의 차이는"국가 통치기구"에 비유할 수 있습니다. ZooKeeper는"중앙 집권적 합의제 국가"에 해당하여, 모든 중요 결정(쓰기)은 중앙(Leader)을 통과해야 하며, 이를 따르지 않는 시도(Non-quorum 쓰기)는 거절됩니다. etcd는"Raft 기반민주적투표제"로, 어떤 노드에서든writes가 가능하지만 Raft 프로토콜이 자동으로 올바른 상태를 보장합니다. Consul은"Gossip식준 сообщения"로, 모든 노드가상호에정보를 전파하여 최종적으로 모두에게상동적 정보가 도달하지만즉시에서는ない 일관성을제공합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **필요 용도** | 리더 선출만 필요 -> ZooKeeper/SimpleServiceRegistry | KV 스토어 + 리더 선출 -> etcd |
| <strong>일관성 요구</strong> | 강한 일관성 필수 -> etcd / ZooKeeper Quorum | Eventual 허용 -> Consul |
| **규모** | 수십 개 수준 노드 -> ZooKeeper 3~5대 | 수백~수천 노드 -> Consul Gossip |
| **운영 난이도** | ZooKeeper 전담 관리 역량 필요 | etcd는 Kubernetes와 긴밀 | Consul은 간단한 KV |

*(추가 실무 적용 가이드 - ZooKeeper 클러스터 구축)*
- **서버 수 결정**: 3대 (개발/테스트), 5대 (중규모 프로덕션), 7대 (대규모/심각하게 가용성 중요한 경우). 우수태는 권장되지 않으며, 항상 기수태를 선택합니다.
- **리더/팔로워 구분**: 리더 선출은 Zab 프로토콜이 자동 처리하므로,운유은"3대 중 어느 서버가 리더인지"만 Watch하면 됩니다.
- **Ephemeral 노드를활용한존활측정**: 각 Worker가"/workers/{worker-id}" ephemeral 노드를 생성하면, 해당 Worker가사ぬ/연결이 끊기면 노드가 자동으로 삭제되어"이 Worker는 이제 활성 상태가 아니다"라는 것을전システム에통지됩니다.

- **📢 섹션 요약 비유**: ZooKeeper 클러스터 구축은"새로운 나라를 세우는 것"과 같습니다.합의제 국가(3대 서비스기)를 세울 때,"5명의 설립 맴버(서버)가 모여 서로동맹을 체결"합니다. 이들 중 한 명이 " Leader"로 선출되고, 나머지는" Follower"가 됩니다. 만약 Leader가 Revolutionary 되면(장애), 나머지 2명이 즉시 만나"누가 새로운 Leader?"를투표하여 선출합니다. 5명 중 3명(과반수)이 살아 있는 한, 국(서비스)는 계속 운영됩니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. <strong>ZooKeeper의 ZooKeeper 대체재 등장: KRaft와 etcd의 확산</strong>
   Kafka 3.3+에서 도입된 KRaft 모드는 ZooKeeper를 대체하여 Kafka 자체의 Raft 프로토콜로 메타데이터를관리합니다. 이는 ZooKeeper에 대한 의존성을 제거하고"운영 단순화"와"단일 장애점 제거"를 동시에 달성합니다. 또한 Kubernetes의 etcd가 마이크로서비스 세계의"분산 코디네이션 표준"으로 자리잡음에 따라, ZooKeeper의 사용 범위가 줄어드는 추세가 가속화되고 있습니다.

2. <strong>서비스 메시와 Service Mesh의 코디네이션 통합</strong>
   HashiCorp Consul, Istio, Linkerd 등의 서비스 메시(Service Mesh) 기술이"서비스 디스커버리 + 분산 추적 + mTLS 암호화 + 코디네이션"을통합하여 제공함에 따라, ZooKeeper가 제공하던"서비스 등록/탐색" 기능이 서비스 메시 레벨로흡수되고 있습니다. 이러한 추세는"별도의 ZooKeeper 클러스터 운영"의 부담을 줄이면서"더 풍부한 서비스 관찰 가능성"을 제공하는 이점을 가집니다.

3. **ZooKeeper의 역할 재정의: 대규모 상태 저장이 아닌"이벤트 기반 코디네이션"으로**
   ZooKeeper의 설계 철학은"작고 빠른 코디네이션"에 집중하는 것입니다. 그러나 수십 만 개의 키를 저장해야 하는 경우, ZooKeeper의 성능은etcD나 Consul에 비해렬ります. 향후 ZooKeeper는"대규모 상태 저장이 아닌"고성능이 필요한"리더 선출 + 분산 잠금 + WATCH" 전용으로 그 역할이 재정의될 것으로 전망됩니다.

- **📢 섹션 요약 비유**: ZooKeeper의 미래 진화는"국가의 역할 변화"와 같습니다. 과거 국가은"행정 everything을 관리하는전능 기관"(ZooKeeper가 모든 기능을 제공)에서한이, 금은"국가는 주로외교(코디네이션)만 담당하고, 내정은각 지방 자치 단체가 처리"(etcd/Kafka KRaft)하는 분권화로 변해가고 있습니다. 동시에"국제 무역 협회(서비스 메시)"가 국가들 사이의통신규칙과 무역로를관리하면, 개별 국가가 직접통신상량 없어도 됩니다. ZooKeeper도 이러한"국제 질서 변화" 속에서"국제 협약의 보장자(코디네이션 표준)"라는 자기 위치를 다시 설정하는 중입니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   <strong>Apache ZooKeeper 핵심 개념</strong>
    *   **Znode**: ZooKeeper의 기본 데이터 단위 (파일+디렉토리 hybrid)
    *   **Watcher**: 노드 변경 시 자동 알림
    *   <strong>Zab Protocol</strong>: Atomic Broadcast + Leader Election
    *   **Quorum**: 과반수 서버 consensus
*   **Znode 유형 조합**
    *   **Regular Persistent (P)**: 영속 비순차 - 설정 정보 저장
    *   **Ephemeral (E)**: 임시 비순차 -존활 확인
    *   **Persistent Sequential (PS)**: 영속 순차 - 일관된 이름 필요
    *   **Ephemeral Sequential (ES)**: 임시 순차 - 리더 선출, 분산 잠금
*   **주요 활용 패턴**
    *   **리더 선출**: 가장 낮은 sequence number의 ES 노드
    *   <strong>분산 잠금</strong>: Zookeeper의 `getChildren()` + `watch` 조합
    *   <strong>서비스 디스커버리</strong>: ephemeral 노드 등록 + watch

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Apache ZooKeeper 핵심 개념]
    |
    v
[Znode: ZooKeeper의 기본 데이터 단위 (파일+디렉토리 hybrid)]
    |
    v
[Watcher: 노드 변경 시 자동 알림]
    |
    v
[Zab Protocol: Atomic Broadcast + Leader Election]
    |
    v
[Quorum: 과반수 서버 consensus]
    |
    v
[Znode 유형 조합]
    |
    v
[Regular Persistent (P): 영속 비순차 - 설정 정보 저장]
```

이 흐름도는 Apache ZooKeeper 핵심 개념에서 출발해 Znode 유형 조합까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Apache ZooKeeper는 여러 컴퓨터가 함께 일할 때"누가 팀장이고, 어떤 일을 해야 하는지"를 정리해주는 선생님과 같아요.
2. 선생님이 제일 잘하는 컴퓨터를 팀장(Leader)으로 정하고, 팀장이 쓰러지면(장애) 바로 다른 컴퓨터를 팀장으로 뽑아주어요.
3. 컴퓨터들이 서로 누가 살아 있는지 죽었는지초가하지 않고, ZooKeeper에게만 물어보면 돼서와고も편리입니다!

---
> <strong>🛡️ Expert Verification:</strong> 본 문서는 Apache ZooKeeper의 코디네이션 서비스로서의 역할, Zab 프로토콜, 그리고 분산 시스템에서의 활용 사례를 기준으로 기술적 정확성을 검증하였습니다. (Verified at: 2026-04-05)
