---
title: "Observer Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 192
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 옵저버 패턴 (Observer Pattern)은 GoF 행위 패턴으로, 객체(Subject/Publisher)의 상태 변화가 발생할 때 이에 의존하는 다수의 객체(Observer/Subscriber)에게 자동으로 통지·갱신하는 일대다(1:N) 의존 관계를 정의하는 패턴이다.
> 2. **가치**: Subject가 Observer를 직접 알지 못하고 인터페이스를 통해 통지하므로, Observer를 동적으로 추가·제거할 수 있고 Subject와 Observer 간 결합도가 낮아진다. 이벤트 기반 시스템, MVC 아키텍처, 리액티브 프로그래밍의 근간이다.
> 3. **판단 포인트**: 옵저버 패턴에서 Subject가 모든 Observer에 동기적으로 통지하면 느린 Observer가 Subject를 블로킹할 수 있다. 비동기 이벤트 큐(EventBus, 메시지 브로커)로 발행-구독을 분리하거나, Observer 통지를 별도 스레드로 처리하여 이 문제를 해결해야 한다.

---

## Ⅰ. 개요 및 필요성

옵저버 패턴은 객체 간의 1:N 의존 관계를 느슨한 결합으로 구현한다. 예를 들어 스프레드시트에서 데이터(Subject)가 변경되면 차트·집계 테이블·요약 뷰(Observer)가 자동으로 갱신된다. 데이터가 각 뷰를 직접 알지 못해도 된다.

실세계 예시: ① 유튜브 구독 알림(Subject: 유튜버, Observer: 구독자), ② 주식 가격 모니터(Subject: 주가 데이터, Observer: 차트·알림·봇), ③ MVC 패턴의 Model-View 통신(Model이 Subject, View가 Observer), ④ 스프링의 ApplicationEvent-ApplicationListener.

```text
+-------------------------------------------------------------+
|            옵저버 패턴 구조                                  |
+-------------------------------------------------------------+
|  Subject (발행자)                                           |
|  + registerObserver(o: Observer)                            |
|  + removeObserver(o: Observer)                              |
|  + notifyObservers()                                        |
|       |                                                     |
|       | (1:N 통지)                                          |
|       +---> Observer A: update(data)                         |
|       +---> Observer B: update(data)                         |
|       +---> Observer C: update(data)                         |
|                                                             |
|  Subject는 Observer 인터페이스만 알고 구체 클래스 모름      |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 신문사(Subject)가 구독자(Observer)에게 새 호(이벤트)를 발송한다. 신문사는 구독자 명단(인터페이스)만 관리하고, 각 구독자가 신문을 어떻게 읽는지 알 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

옵저버 패턴의 두 가지 통지 방식: ① Push 방식: Subject가 데이터를 Observer에게 직접 전달(`update(data)`), ② Pull 방식: Subject가 변경만 통지하고 Observer가 필요한 데이터를 Subject에서 요청. Pull 방식이 Observer와 Subject 간 결합도가 더 낮다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| Push (데이터 전달) | 단순, Observer가 모든 데이터 수신 | 중간 |
| Pull (변경 통지만) | Observer가 필요 데이터만 요청 | 낮음 |
| EventBus (비동기) | 느슨한 결합, 비동기 처리 | 매우 낮음 |

```text
+-------------------------------------------------------------+
|       스프링 ApplicationEvent 기반 옵저버                   |
+-------------------------------------------------------------+
|  // Subject (이벤트 발행)                                   |
|  @Service class OrderService {                              |
|    applicationEventPublisher.publishEvent(                  |
|      new OrderCompletedEvent(orderId));                     |
|  }                                                          |
|                                                             |
|  // Observer (이벤트 구독)                                  |
|  @EventListener class EmailNotificationService {            |
|    void onOrderCompleted(OrderCompletedEvent event) { ... } |
|  }                                                          |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 알림 시스템(Subject)이 이벤트를 발생시키면 이메일 서비스·SMS 서비스·푸시 알림 서비스(Observer)가 각자의 방식으로 처리한다. 알림 시스템은 각 서비스 내부를 알 필요 없다.

---
## Ⅲ. 비교 및 연결

옵저버 패턴과 미디에이터 패턴의 차이: 옵저버는 Subject가 Observer에게 통지하는 1:N 관계이고, 미디에이터는 모든 객체가 미디에이터를 통해 N:N으로 통신한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 통신 방향 | 1:N (Subject -> Observers) | N:N (모두 ↔ Mediator) |
| 결합도 | Subject ↔ Observer 낮음 | 모든 객체 ↔ Mediator |
| 적합한 경우 | 이벤트 통지, 구독 | 복잡한 객체 간 협력 |

- **📢 섹션 요약 비유**: 옵저버는 방송국(Subject)이 시청자(Observer)에게 일방적으로 방송하는 것이고, 미디에이터는 채팅방(Mediator)에서 모든 참여자가 소통하는 것이다.

---
## Ⅳ. 실무 적용 및 실무자 판단

리액티브 프로그래밍(RxJava, Project Reactor)은 옵저버 패턴의 함수형·비동기 확장이다. `Observable`(Subject)과 `Observer`를 함수형 스트림으로 표현하여, 비동기·비블로킹 이벤트 처리를 우아하게 구현한다.

### 판단 체크리스트
1. Subject와 Observer가 인터페이스로 느슨하게 연결되어 Observer를 동적으로 추가·제거할 수 있는가?
2. 동기 통지 시 느린 Observer가 Subject를 블로킹하는 문제를 해결했는가?
3. 메모리 누수 방지를 위해 Observer가 더 이상 필요 없을 때 구독 해제(removeObserver)가 되는가?
4. 이벤트 순환(Subject가 Observer를 통지하고 Observer가 다시 Subject를 변경하는 무한 루프)을 방지하는가?
5. 옵저버 수가 많을 때 성능 최적화를 위해 비동기 이벤트 버스(EventBus)를 사용하는가?

- **📢 섹션 요약 비유**: 구독 서비스(Subject)에서 탈퇴(removeObserver)를 처리하지 않으면, 더 이상 관심 없는 구독자(Observer)에게 계속 알림이 가서 메모리 낭비(누수)가 발생한다.

---

## Ⅴ. 기대효과 및 결론

옵저버 패턴을 적용하면 Subject와 Observer 간 결합도가 낮아져 새 Observer를 쉽게 추가할 수 있다. 이벤트 기반 아키텍처(EDA), MVC, 리액티브 프로그래밍의 근간이 되어 현대 소프트웨어 전반에 적용된다.

한계는 동기 통지 시 성능 문제, 복잡한 이벤트 연쇄로 인한 디버깅 어려움, 메모리 누수(Observer 미제거) 위험이다. 리액티브 스트림(Project Reactor)이 이러한 문제를 함수형으로 해결한 현대적 구현이다.

- **📢 섹션 요약 비유**: 유튜브 알림처럼, 크리에이터(Subject)가 영상 업로드(이벤트)를 하면 구독자(Observer) 전원에게 자동으로 알림이 간다. 크리에이터는 구독자 수가 얼마든 알림 메커니즘을 알 필요 없다.

---

### 📌 관련 개념 맵

[이벤트 기반 통신] -> [옵저버 패턴] -> [스프링 ApplicationEvent] -> [리액티브 프로그래밍(RxJava)] -> [메시지 브로커(Kafka)]

| 개념 | 연결 포인트 |
|:---|:---|
| 발행-구독(Pub/Sub) | 옵저버의 분산 시스템 확장 |
| 리액티브 프로그래밍 | 옵저버 패턴의 함수형·비동기 확장 |
| 이벤트 주도 아키텍처(EDA) | 옵저버 패턴의 아키텍처 수준 적용 |
| 미디에이터 패턴 | 옵저버 패턴과 대비되는 N:N 통신 패턴 |

### 📈 관련 키워드 및 발전 흐름도

[GoF Observer(1994)] -> [MVC Model-View 통신] -> [이벤트 버스(EventBus)] -> [RxJava·Project Reactor] -> Kafka 기반 분산 옵저버]

### 👶 어린이를 위한 3줄 비유 설명

1. 옵저버 패턴은 유튜브 알림처럼, 크리에이터(Subject)가 영상을 올리면 구독자(Observer)에게 자동 알림이 가요.
2. 크리에이터는 구독자들이 어디서 알림을 받는지 알 필요 없어요.
3. 스프링의 이벤트 시스템이 바로 이 패턴을 사용해요!
