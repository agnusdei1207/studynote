---
title: "Basically Available, Soft State, Eventual Consistency"
date: "2024-05-22"
tags:
  - "studynote-bigdata"
weight: 124
---
## 핵심 인사이트 (3줄 요약)
- <strong>가용성 우선(Availability First):</strong> 데이터의 엄격한 일관성(ACID)을 희생하더라도, 대규모 분산 환경에서 중단 없는 서비스를 제공하는 NoSQL의 핵심 철학임.
- <strong>결과적 일관성(Eventual Consistency):</strong> 실시간으로 데이터가 일치하지 않을 수 있지만, 일정 시간이 지나면 모든 노드가 동일한 값을 갖게 됨을 보장함.
- **확장성 극대화:** 분산 시스템의 CAP 정리에서 가용성(A)과 파티션 감내(P)를 선택하여 전 세계 사용자에게 빠른 응답 속도를 제공함.

### Ⅰ. 개요 (Context & Background)
1. **RDBMS의 한계:** 전통적인 ACID(원자성, 일관성, 고립성, 지속성)는 데이터의 무결성을 보장하지만, 수천 개의 서버가 연결된 빅데이터 환경에서는 성능 저하와 가용성 하락을 유발함.
2. **BASE의 탄생:** 대규모 웹 서비스(Amazon, Google)에서 수평 확장(Scale-out)을 위해 일관성을 "결과적"으로 타협하되, 가용성을 극대화하는 새로운 트랜잭션 모델이 필요하게 됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- <strong>BASE Principle Workflow &amp; Distributed Replication</strong>
```text
[ Data Write (Node A) ]      [ Propagation Delay ]      [ Data Read (Node B) ]
+---------------------+      +-------------------+      +---------------------+
| Value = 10 (Update) | --- (Asynchronous Sync) ---> | Value = 5 (Soft State)|
+---------------------+                                 +---------------------+
                                       |                           |
                                       |                           v
                                       |                (Eventually Consistency)
                                       +--------------> | Value = 10 (Synced) |
                                                        +---------------------+
[ Key Pillars of BASE ]
1. BA: Basically Available (기본적 가용성)
2. S : Soft State (소프트 스테이트)
3. E : Eventual Consistency (결과적 일관성)
```

1. <strong>Basically Available (BA):</strong>
   - 시스템의 일부분에 장애가 발생하더라도, 전체 시스템이 멈추지 않고 기본적인 응답을 제공함. 완벽한 응답은 아니더라도 가용한 상태를 유지함.
2. <strong>Soft State (S):</strong>
   - 데이터의 상태가 외부의 입력 없이도 시간이 지남에 따라 변할 수 있음. 노드 간 동기화가 진행 중일 때, 특정 시점의 데이터는 "확정된 상태"가 아닐 수 있음을 의미함.
3. <strong>Eventual Consistency (E):</strong>
   - 특정 시간 동안 새로운 업데이트가 없다면, 결국 모든 복제본(Replica)은 동일한 값으로 수렴함. 일시적인 불일치를 허용하여 성능 병목을 제거함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | ACID (RDBMS) | BASE (NoSQL) | 융합 분석 |
| :--- | :--- | :--- | :--- |
| **핵심 가치** | 일관성 (Consistency) | 가용성 (Availability) | ACID는 신뢰성, BASE는 성능 |
| **시스템 상태** | 강한 일관성 (Strong) | 결과적 일관성 (Eventual) | 데이터 중요도에 따라 혼용 |
| <strong>트랜잭션 관리</strong> | 비관적 락 (Pessimistic) | 낙관적 방식 (Optimistic) | 동시성 제어 방식의 차이 |
| **확장성** | 수직 확장 (Scale-up) | 수평 확장 (Scale-out) | 빅데이터 처리는 수평 확장이 대세 |
| **사용 사례** | 금융, 결제, 인사 관리 | SNS, 로그, 카트, 댓글 | 정합성 vs 실시간성 선택 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
1. <strong>비즈니스 도메인별 선택 (Strategy):</strong>
   - **SNS 뉴스피드:** 친구의 글이 1초 늦게 보여도 문제없으므로 BASE가 적합함.
   - **계좌 이체:** 1원이라도 틀리면 치명적이므로 반드시 ACID를 유지해야 함.
2. **실무적 판단:** 현대 아키텍처는 "Polyglot Persistence"를 지향함. 주문 정보는 RDBMS(ACID)에, 대량의 상품 조회 로그는 NoSQL(BASE)에 저장하여 성능과 안전성을 동시에 확보하는 것이 핵심 설계 역량임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 전 지구적 규모의 분산 시스템(Global Distribution)에서 지연 시간(Latency)을 최소화하고, 무한한 확장을 가능하게 하여 현대 인터넷 서비스의 기술적 근간이 됨.
2. **결론:** BASE는 일관성을 포기한 것이 아니라, 성능을 위해 "일관성의 시점"을 늦춘 지혜로운 타협임. 분산 데이터베이스 설계자는 BASE 원칙을 통해 서비스 가용성의 임계치를 돌파할 수 있음.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 분산 데이터베이스, NoSQL
- **하위 개념:** 결과적 일관성, 가용성 (Availability)
- **연관 개념:** CAP 정리, PACELC 이론, ACID

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 분산 데이터베이스, NoSQL]
    |
    v
[하위 개념: 결과적 일관성, 가용성 (Availability)]
    |
    v
[연관 개념: CAP 정리, PACELC 이론, ACID]
```

이 흐름도는 상위 개념: 분산 데이터베이스, NoSQL에서 출발해 연관 개념: CAP 정리, PACELC 이론, ACID까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- **ACID 식당:** 주방장이 모든 테이블의 요리를 완벽하게 다 만들 때까지 손님을 한 명도 안 들여보내는 깐깐한 식당이에요.
- **BASE 식당:** 일단 손님을 다 받고 음식을 조금씩 주면서, 나중에는 모두가 맛있는 요리를 배부르게 먹을 수 있게 조절하는 인기 식당이에요.
- **결론:** 처음엔 조금 복잡해 보일 수 있어도, 결국에는 모두가 행복해지는 마법 같은 순서 맞추기랍니다.
