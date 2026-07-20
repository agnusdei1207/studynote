---
title: "Event Sourcing Msa"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 138
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Event Sourcing은 <strong>엔티티의 현재 상태를 저장하는 대신, 상태를 변경한 모든 이벤트(Event)를 순서대로 저장</strong>하고, 이벤트를 재생(Replay)하여 현재 상태를 복원하는 패턴이다.
> 2. **가치**: 상태만 저장하면 "왜 이 상태가 되었는지" 추적이 불가능하지만, Event Sourcing은 <strong>모든 변경 이력이 이벤트로 보존</strong>되어 감사(Audit)·디버깅·시간 여행(Time Travel) 쿼리가 가능하다.
> 3. **판단 포인트**: CQRS(Command Query Responsibility Segregation)와 자주 함께 사용하며, 이벤트 저장소(Event Store)가 핵심 인프라이다. 스냅샷으로 재생 성능을 최적화한다.

---

## Ⅰ. 개요 및 필요성

```text
기존: orders 테이블 -> UPDATE status='배송' (이전 상태 유실)
Event Sourcing: events 테이블 ->
  {주문 생성, 결제 완료, 배송 시작, 배달 완료}
  -> Replay -> 현재 상태 = '배달 완료'
  -> 감사: 언제·누가·무엇을 변경했는지 100% 추적
```

- **📢 섹션 요약 비유**: Event Sourcing은 <strong>은행 거래 내역</strong>이다. 잔고(상태)만 보는 것이 아니라 <strong>모든 입출금 기록(이벤트)</strong>을 보존한다.

---

## Ⅱ~Ⅴ. 결론

Event Sourcing은 <strong>감사·추적·재생이 중요한 도메인(금융·의료)의 핵심 패턴</strong>이며, CQRS와 함께 MSA의 고급 아키텍처를 구성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Event Sourcing</strong> | 이벤트 저장·재생 |
| <strong>CQRS</strong> | 명령·조회 분리 |
| **Event Store** | 이벤트 저장소 |
| <strong>Snapshot</strong> | 재생 성능 최적화 |
| <strong>Audit Trail</strong> | 감사 추적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CRUD (상태 저장)] -> [Event Sourcing (Martin Fowler, 2005)]
    -> [CQRS + ES (Greg Young, 2010)]
    -> [EventStoreDB (2012)] -> [Kafka as Event Store]
    -> [현재: Axon Framework — ES+CQRS 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Event Sourcing은 <strong>일기장</strong>이에요. 오늘 잔고(상태)만 보는 게 아니라 <strong>모든 용돈 기록(이벤트)</strong>을 남겨요.
2. 기록을 처음부터 **다시 읽으면(Replay)** 지금 잔고를 정확히 알 수 있어요.
3. "3일 전에 뭘 샀지?" 같은 <strong>시간 여행 질문</strong>에도 답할 수 있어요!
