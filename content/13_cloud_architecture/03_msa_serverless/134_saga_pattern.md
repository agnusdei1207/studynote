---
title: "Saga Pattern"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 134
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Saga는 <strong>여러 마이크로서비스에 걸친 비즈니스 트랜잭션을 로컬 트랜잭션의 시퀀스로 분해</strong>하고, 실패 시 <strong>보상 트랜잭션(Compensating Transaction)</strong>으로 롤백하는 패턴이다.
> 2. **가치**: 2PC의 블로킹·단일 장애점 문제 없이 <strong>서비스 자율성을 유지</strong>하면서 데이터 일관성(Eventual Consistency)을 달성한다.
> 3. **판단 포인트**: <strong>Choreography(이벤트 기반, 각 서비스 독립)</strong> vs <strong>Orchestration(중앙 오케스트레이터)</strong> — 서비스 수가 적으면 Choreography, 복잡하면 Orchestration(Temporal/Cadence).

---

## Ⅰ. 개요 및 필요성

```text
Choreography: 주문->이벤트->결제->이벤트->배송 (각자 독립)
Orchestration: 오케스트레이터->주문, ->결제, ->배송 (중앙 제어)
실패 시: 보상 트랜잭션 (주문 취소, 결제 환불)
```

- **📢 섹션 요약 비유**: Choreography는 재즈 즉흥(각자 연주), Orchestration은 교향곡(지휘자 지휘)이다.

---

## Ⅱ~Ⅴ. 결론

Saga는 <strong>MSA 분산 트랜잭션의 사실상 표준</strong>이며, Temporal/Cadence가 Orchestration Saga의 대표 프레임워크이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Saga</strong> | 분산 트랜잭션 패턴 |
| **Choreography** | 이벤트 기반 (독립) |
| <strong>Orchestration</strong> | 중앙 제어 (Temporal) |
| <strong>보상 트랜잭션</strong> | 실패 시 되돌리기 |
| <strong>Eventual Consistency</strong> | 최종 일관성 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (1990s)] -> [Saga 이론 (Garcia-Molina, 1987)]
    -> [MSA Saga 재발견 (2014~)]
    -> [Choreography (Kafka 이벤트)]
    -> [Orchestration (Temporal/Cadence, 2020~)]
    -> [현재: Durable Execution — Saga 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Saga는 <strong>릴레이 달리기</strong>예요. 각 선수가 자기 구간을 달리고 **바톤을 넘겨요**.
2. 한 선수가 넘어지면(실패) <strong>그 구간만 다시 달려요(보상 트랜잭션)</strong>.
3. 전원이 동시에 출발하는 것(2PC)보다 <strong>빠르고 안전</strong>하답니다!
