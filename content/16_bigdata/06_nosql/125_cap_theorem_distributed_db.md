---
title: "CAP Theorem"
date: "2024-05-22"
tags:
  - "studynote-bigdata"
weight: 125
---
## 핵심 인사이트 (3줄 요약)
- <strong>분산의 불가능성:</strong> 일관성(C), 가용성(A), 파티션 감내(P) 세 가지를 분산 시스템에서 동시에 완벽하게 만족할 수 없다는 에릭 브루어의 이론임.
- **P는 필수:** 네트워크 단절(P)은 제어 불가능한 실재이므로, 실제 설계 시에는 CP(일관성 중심)와 AP(가용성 중심) 중 하나를 선택하는 트레이드오프가 핵심임.
- **아키텍처 가이드:** 시스템의 목적(금융 vs SNS)에 따라 어떤 특성을 우선시할지 결정하는 데이터베이스 설계의 가장 중요한 나침반 역할을 수행함.

### Ⅰ. 개요 (Context & Background)
1. <strong>분산 환경의 숙명:</strong> 노드가 여러 개로 나뉘어 데이터를 복제하는 환경에서는 네트워크 장애가 필연적으로 발생하며, 이때 데이터를 어떻게 처리할지가 시스템의 성격을 결정함.
2. <strong>트레이드오프 관계:</strong> 모든 것을 가질 수는 없으므로, 비즈니스 요건에 맞춰 "무엇을 버릴지"를 결정하는 엔지니어링적 통찰을 제공함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- <strong>CAP Theorem Triangle &amp; Node Interaction</strong>
```text
          [ Consistency ] (C)
              /   \
             /     \
      (CP)  /       \  (CA)
           /         \
          /           \
[ Partition ]-------[ Availability ]
 Tolerance (P)  (AP)      (A)

1. C: 모든 노드가 같은 시점에 같은 데이터를 보아야 함.
2. A: 일부 노드 장애 시에도 모든 요청에 응답해야 함.
3. P: 노드 간 네트워크 단절 시에도 시스템이 작동해야 함.
```

1. <strong>CP (Consistency + Partition Tolerance):</strong>
   - 네트워크 단절 시, 데이터 불일치를 막기 위해 서비스 응답을 거부(에러 반환)함. <strong>완벽한 데이터 무결성</strong>이 중요한 금융권, HBase, MongoDB(기본)가 대표적임.
2. <strong>AP (Availability + Partition Tolerance):</strong>
   - 네트워크 단절 시, 최신 데이터가 아닐지라도 일단 응답을 제공함. <strong>중단 없는 서비스</strong>가 중요한 SNS, Cassandra, DynamoDB가 대표적임.
3. <strong>CA (Consistency + Availability):</strong>
   - 네트워크 장애가 없음을 가정하므로 단일 노드 시스템(RDBMS)에 해당함. 분산 시스템에서는 P를 포기할 수 없으므로 사실상 성립하기 어려움.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | CP 시스템 (Consistency focus) | AP 시스템 (Availability focus) |
| :--- | :--- | :--- |
| **장애 대응** | 일관성을 위해 "느린 응답" 또는 "거절" | 가용성을 위해 "부정확한 응답" 허용 |
| **주요 기술** | Quorum, Paxos, Raft 합의 알고리즘 | Gossip Protocol, Vector Clock |
| <strong>데이터 정합성</strong> | 강한 정합성 (Strong Consistency) | 결과적 정합성 (Eventual Consistency) |
| **사용 사례** | 결제, 인벤토리 관리, 사용자 프로필 | 뉴스 피드, 댓글, 장바구니 |
| **철학적 기반** | ACID (안정성) | BASE (속도) |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
1. <strong>네트워크 장애(P)는 상수다 (Strategic View):</strong>
   - 분산 시스템에서 P를 선택하지 않는 것은 장애 시 시스템 전체 침묵을 의미함. 따라서 현대 클라우드 설계는 CP와 AP 사이의 균형점을 찾는 과정임.
2. **실무적 판단:** CAP 정리는 고정된 불변의 진리라기보다 '극한 상황에서의 기준'임. 최근에는 PACELC 정리를 통해 네트워크가 정상인 시점의 Latency와 Consistency 사이의 트레이드오프까지 고려하는 고도화된 설계가 필요함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 시스템 요구사항에 최적화된 데이터 저장소를 선택하고, 장애 상황에서도 비즈니스 연속성을 보장하는 구조적 설계를 가능하게 함.
2. **결론:** CAP 정리는 분산 아키텍트의 기초 문법임. 이를 통해 우리는 기술의 한계를 명확히 인식하고, 최선의 차선책을 선택할 수 있는 전문적 역량을 갖추게 됨.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 분산 시스템, NoSQL
- **하위 개념:** 일관성(C), 가용성(A), 파티션 감내(P)
- **연관 개념:** PACELC 정리, BASE 원칙, 합의 알고리즘 (Raft)

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 분산 시스템, NoSQL]
    |
    v
[하위 개념: 일관성(C), 가용성(A), 파티션 감내(P)]
    |
    v
[연관 개념: PACELC 정리, BASE 원칙, 합의 알고리즘 (Raft)]
```

이 흐름도는 상위 개념: 분산 시스템, NoSQL에서 출발해 연관 개념: PACELC 정리, BASE 원칙, 합의 알고리즘 (Raft)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- **통신 끊김(P):** 친구와 전화가 끊겼을 때 어떻게 할까요?
- <strong>CP 친구:</strong> "중요한 얘기니까 나중에 전화 연결되면 다시 할게!" 하고 전화를 아예 안 받아요.
- <strong>AP 친구:</strong> "아마도 어제 말한 그거일 거야!" 하고 일단 대답부터 해주고 끊어요.
- **결론:** 정답이 중요한지, 대답이 빠른 게 중요한지 고르는 시합이랍니다.
