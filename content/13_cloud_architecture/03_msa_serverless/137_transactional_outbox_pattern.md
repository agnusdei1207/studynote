---
title: "Transactional Outbox Pattern"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transactional Outbox는 <strong>비즈니스 데이터와 이벤트를 같은 DB 트랜잭션으로 저장(Outbox 테이블)</strong>한 후, 별도 프로세스(CDC·Polling)가 Outbox에서 이벤트를 읽어 메시지 브로커로 발행하는 패턴이다.
> 2. **가치**: "주문 저장 + Kafka 발행"을 별도로 하면 <strong>DB 저장 성공·Kafka 발행 실패</strong> 시 불일치가 발생하지만, Outbox는 <strong>단일 트랜잭션으로 원자성을 보장</strong>한다.
> 3. **판단 포인트**: Debezium(CDC 기반)이 Outbox 이벤트를 실시간 캡처하여 Kafka로 전달하는 것이 표준 구현이며, Polling 방식은 지연이 있다.

---

## Ⅰ. 개요 및 필요성

```text
1. 비즈니스 로직: INSERT orders + INSERT outbox (같은 트랜잭션)
2. CDC (Debezium): outbox 테이블 변경 감지 -> Kafka 발행
3. 소비자: Kafka에서 이벤트 소비
-> DB 트랜잭션 = 이벤트 발행 원자성 보장
```

- **📢 섹션 요약 비유**: Outbox는 **보내야 할 편지를 우편함(Outbox)에 넣으면 우체부(Debezium)가 가져가는** 것이다.

---

## Ⅱ~Ⅴ. 결론

Transactional Outbox는 <strong>MSA 이벤트 발행의 원자성 보장 표준 패턴</strong>이며, Debezium+Kafka가 핵심 구현이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Outbox** | 이벤트 원자성 보장 |
| <strong>CDC</strong> | 변경 데이터 캡처 |
| **Debezium** | CDC 오픈소스 |
| <strong>Kafka</strong> | 이벤트 브로커 |
| <strong>Saga</strong> | Outbox와 함께 사용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[직접 Kafka 발행 (문제: 불일치)]
    -> [Outbox 패턴 (2016~)]
    -> [Debezium CDC (2017~)]
    -> [현재: Outbox + Saga + CQRS — 통합 패턴]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Outbox는 **보내야 할 편지를 우편함에 넣는** 거예요.
2. 편지와 일기(비즈니스 데이터)를 <strong>동시에 저장</strong>해서 빠뜨리지 않아요.
3. 우체부(Debezium)가 우편함을 확인하고 <strong>확실히 배달</strong>해요!
