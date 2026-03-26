+++
title = "분산 Consensus 알고리즘 (Paxos, Raft)"
description = "분산 시스템에서 합의를 달성하는 Paxos와 Raft 알고리즘에 대해 설명"
date = 2024-01-01
weight = 35

[taxonomies]
subjects = ["database"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Consensus 알고리즘은 분산 시스템에서 여러 노드가 하나의 값에 대해 합의를 달성하는 프로토콜로, Paxos와 Raft가 대표적이다.
> 2. **가치**: 네트워크 분단이나 노드 장애 상황에서도 시스템이 일관된 상태를 유지할 수 있게 한다.
> 3. **융합**: Raft는"understandability"를 핵심 설계 목표로, Paxos의 복잡도를 낮추어 구현하기 쉽게 만든 것이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념
Consensus(합의)란 분산 시스템에서 여러 노드가某个 proposal에 대해同一한 결정에 도달하는 것이다. Leslie Lamport의 Paxos(1990년)가最初的의 Consensus 알고리즘이며, Diego Ongar 등의 Raft(2014년)는 Paxos를보다 구현 쉽게 再設計한 것이다.

### 필요성
분산 환경에서는 네트워크 지연, 장애, 메시지 유실 등이 발생할 수 있으므로,"어떤 값이 결정되었는가"에 대해 모든 정상 노드가 동일하게 동의하는 것이 필수적이다.

### 섹션 요약 비유
Consensusは会议室の决议와 같다. 다양한意见가 있지만、全員が同じ conclusion에 도달해야_action할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Raft vs Paxos

```text
  ┌───────────────────────────────────────────────────────────────────────┐
  │                    Raft의 세 가지 역할                                   │
  ├───────────────────────────────────────────────────────────────────────┤
  │
  │   [역할]                                                             │
  │
  │   Leader ──▶ 모든 요청을 처리 (Write)                                 │
  │    │                                                               │
  │    ├──-follower에게 로그 replication                                 │
  │    └── heartbeat 전송                                                │
  │                                                                       │
  │   Follower ──▶ Leader의 명령 수신 및 처리                             │
  │    │                 │                                               │
  │    │                 └── votes (选举 시)                               │
  │    │                                                               │
  │    Candidate ──▶ Leader 선출竞选                                 │
  │                                                                       │
  │   [选举 과정]                                                        │
  │
  │   ① 임기 초과 (Election Timeout) 발생                                │
  │   ② Follower → Candidate 전환                                       │
  │   ③ RequestVote 요청을 다른 노드에 전송                               │
  │   ④多数同意了으면 Leader로 선출                                       │
  │   ⑤ 새로운 Leader는 Heartbeat를 전송하여任을巩固                        │
  │
  └───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Raft는 Leader 기반 Consensus 알고리즘으로, 모든 쓰기 요청은 Leader를 통해 처리된다. Leader는 로그 엔트리를 Follower에게复制하고,多数의Follower가 복제되면 해당 엔트리을 COMMIT한다. Leader가故障하면残りのノードは election timeout 후新一轮选举を実施する. Paxos와의 核心적 차이는,Raft은Leader라는 명확한 역할이 있어算法の 흐름을 이해하기 쉽지만, Paxos는 역할 구분이 모호하여 구현이 어렵다는 점이다. 그러나 功能적으로는 둘 다 Consensus를 보장한다.

### 로그 복제 과정

| 단계 | 동작 |
|:---|:---|
| **1. 클라이언트 요청** | Leader가 로그 엔트리 수신 |
| **2. 로컬 기록** | Leader가 로그 엔트리.append |
| **3. 복제 요청** | Follower에게 AppendEntries 전송 |
| **4. Follower 처리** | 로그 기록 후 응답 |
| **5.多数确认** | Majority로부터 응답 시 COMMIT |
| **6. 응답** | Leader가 클라이언트에게 응답 |

### 섹션 요약 비유
Raft의 로그 복제는회의록 작성과 같다. Chair Person(Leader)이회의内容를 기록(로그 엔트리 추가)하고,全出席者(Follower)에게 동시 전달(AppendEntries)하여,多数が同時に同意하면(Commit)그会议록은 공식記録이 된다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: Paxos vs Raft

| 구분 | Paxos | Raft |
|:---|:---|:---|
| **설계 목표** | 이론적 정확성 | 구현 용이성 |
| **역할 구분** | 모호 | 명확 (Leader/Follower/Candidate) |
| **구현 난이도** | 높음 | 낮음 |
| **공식 증명** | 있음 | 미흡 |
| **채택 사례** | Google's Chubby | etcd, CockroachDB, TiKV |

### 섹션 요약 비유
Paxos와 Raft의関係は数学の証明と易しい解説書の関係과 같다. 둘 다同一个定理(Consensus)를証明하지만、表現 방법이 다르다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 — etcd**: Kubernetes의 메타데이터 저장소로 Raft를 사용하여, 클러스터 상태의 일관성을 보장한다. Leader选举으로故障 대응하고,日志复制로 데이터の冗長성을 제공한다.

### 안티패턴
- **Election Timeout 과도**: timeout이 길면 그 동안 시스템이 응답 불가 상태가 된다.
- **Split Brain**: 네트워크 파티션이 양쪽에 각각 Leader가 생기는 상황. Raft는 이를 방지하지만, 구현 실수로 발생할 수 있다.

### 섹션 요약 비유
Consensus 알고리즘의 Split Brain問題은 두 나라가 동시에"이 섬은 내 것이야"라고 선언하는 것과 같다. 둘 다 正統性을 주장하지만, 결국 하나만 인정받아야 한다.

---

## Ⅴ. 결론

### Consensus選択 가이드

| 상황 | 권장 알고리즘 |
|:---|:---|
| **구현 용이성** | Raft |
| **공식적 검증** | Paxos |
| **高性能要求** | Raft (优化된 variant) |
| **장애 다양성** | Multi-Paxos |

### 섹션 요약 비유
Consensus 알고리즘选择은 도구 선택과 같다. Hammer(Paxos)로도钉을 박을 수 있지만、드라이버(Raft)가 더 사용하기 쉽다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **2PC** | Consensus와类似하지만, 2PC는 장애 시 blocking 문제가 있고, Consensus는 없다. |
| **CAP 이론** | Consensus 알고리즘은 CAP의 C(일관성)을 보장하는 메커니즘이다. |
| **复制** | Consensus 알고리즘은 로그 replication를 통해 일관성을 보장한다. |
| **Leader选举** | Raft의 핵심 메커니즘으로,故障 시 새로운 Leader를 선출한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. Consensusは「班長決める」みと 같くて、全員が同じ人を選ぶと一致性保つ、有效な行動ことができる.
2. Raftはその议长选举をより简单にした方法で、紧急時に谁が议长代理になるか明確に决めている.
3. 计算机も複数の子供がものを轮流で游玩するtasニュ、分担して交流するにおいても、consensus泡消えるがないように主动的な判断乏しい.
