---
title: "606. 옵저버 패턴(Observer Pattern) Pub/Sub 연계"
date: "2026-03-15"
type: "pe_exam"
id: 606
---

# 606. 옵저버 패턴(Observer Pattern) Pub/Sub 연계

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 옵저버(Observer) 패턴은 한 객체(Subject/Publisher)의 상태가 변경되면 **의존하는 모든 객체(Observer/Subscriber)에게 자동으로 알림**을 보내고 내용을 갱신하는 **일대다다(1:N) 의존성**을 정의하는 행위 패턴(Behavioral Pattern)이다.
> 2. **가치**: MVC(Model-View-Controller) 패턴의 Model-View 연동, 이벤트 드리븐(Event-Driven) 아키텍처, GUI 이벤트 처리의 기반이 되며, **Publisher와 Subscriber의 느슨한 결합(Loose Coupling)**을 통해 확장 가능한(Scalable) 시스템을 구축한다.
> 3. **융합**: Kafka, RabbitMQ 같은 메시지 큐(Message Queue)의 PUB/SUB 메커니즘, React/Vue의 상태 관리(Reactive State), RxJava(ReactiveX)의 Observable 패턴, 애플의 Notification Delegate 등 현대 소프트웨어 전반에 확장되고 있다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 옵저버 패턴이란 무엇인가? 신문사(Subject)이 뉴스를 발행하면, 이를 구독한 구독자(Observer)들에게 자동으로 배달되는 시스템과 유사하다. Subject는 Observer 리스트를 유지하고, 상태 변경 시 `notify()` 메서드를 호출하여 모든 Observer의 `update()` 메서드를 실행한다. 이때 Subject는 Observer의 구체적인 타입을 알 필요 없이 인터페이스(IObserver)만 통해 통신한다.

- **💡 비유**: 옵저버 패턴은 **"유튜브 채널 알림(Bell)"**과 같습니다. 구독자(Observer)가 채널(Subject)을 구독하면, 새로운 영상이 올라올 때마다 알림이 자동으로 전송됩니다. 채널 운영자는 구독자가 누구인지(Observer의 구체 타입) 알 필요 없이, 그저 "업로드 완료" 알림만 보내면 됩니다. 구독자 수는 1명이든 100만 명이든 채널 코드를 수정할 필요 없죠(Loose Coupling).

- **등장 배경**:
    1. **MVC 아키텍터(1979)**: Smalltalk UI에서 Model 데이터가 변경되면 View 화면이 자동 갱신되는 메커니즘 필요.
    2. **이벤트 드리븐 UI**: GUI(그래픽 사용자 인터페이스)에서 버튼 클릭, 키 입력 등 이벤트 핸들러(Event Handler)와의 분리.
    3. **분산 시스템 메시징**: 2000년대 PUB/SUB 메시징 시스템(JMS, AMQP)으로 확장.

- **📢 섹션 요약 비유**: 신문사가 각 구독자에게 신문을 직접 배달하는 대신, 우편함(PUB/SUB)에만 넣어두면 배달 시스템이 자동으로 각 가정으로 전달해주는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 옵저버 패턴 구성 요소

| 요소 | 역할 및 정의 | 기술적 구현 | 위배 시 증상 | 비유 |
|:---|:---|:---|:---|:---|
| **Subject(Publisher)** | 상태를 가지고 변경되는 객체 | `observers[]`, `attach()`, `detach()`, `notify()` | Observer 관리 불가 | 신문사 |
| **Observer(Subscriber)** | Subject의 변경에 관심 있는 객체 | `update()` 인터페이스 | 알림 수신 불가 | 구독자 |
| **Concrete Subject** | 구체적인 Subject 구현 | StockPrice, NewsFeed | - | 주식 사이트 |
| **Concrete Observer** | 구체적인 Observer 구현 | GraphView, EmailAlert | - | 차트, 알림 |

#### [옵저버 패턴 구조 다이어그램]

주식 가격(StockPrice) 변경 시 여러 화면(Chart, Alert, Listing)이 동시에 갱신되는 구조를 시각화한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Observer Pattern Structure                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Subject Interface                                     Observer Interface│  │
│  │  ┌───────────────────────────────────────┐      ┌───────────────────────┐│  │
│  │  │ + attach(observer: Observer)         │      │ + update(data: any)  ││  │
│  │  │ + detach(observer: Observer)         │      └─────────▲───────────┘│  │
│  │  │ + notify()                           │                │ implements   │  │
│  │  └───────────────▲───────────────────────┘                │             │  │
│  │                  │                                          │             │  │
│  │        implements │                            ┌───────┴───────┐        │  │
│  │  ┌───────────────┴───────────────────────┐    │               │        │  │
│  │  │  Concrete Subject: StockPrice         │    │  Concrete Observer    │        │  │
│  │  │  ┌─────────────────────────────────┐   │    │  ┌─────────────────┐│        │  │
│  │  │  │ - price: double                 │   │    │  │ ChartObserver  ││        │  │
│  │  │  │ - observers[]: List<Observer>    │   │    │  │ ┌─────────────┐││        │  │
│  │  │  │ + setPrice(price) {              │   │    │  │ │ + update()  │││        │  │
│  │  │  │   this.price = price;             │   │    │  │ │   그래프 갱신│││        │  │
│  │  │  │   notify();  // 상태 변경 알림    │   │    │  │ └─────────────┘││        │  │
│  │  │  │ }                                │   │    │  └─────────────────┘│        │  │
│  │  │  │ + notify() {                      │   │    │                       │        │  │
│  │  │  │   for (Observer o : observers)      │   │    │  ┌─────────────────┐│        │  │
│  │  │  │     o.update(price);  // 다형성    │   │    │  │ AlertObserver ││        │  │
│  │  │  │ }                                │   │    │  │ ┌─────────────┐││        │  │
│  │  │  └─────────────────────────────────┘   │    │  │ │ + update()  │││        │  │
│  │  └───────────────────────────────────────────┘    │  │ │이메일/문자 발송│││        │  │
│  │                                                   │  │ └─────────────┘││        │  │
│  │                                                   │  └─────────────────┘│        │  │
│  └───────────────────────────────────────────────────────┼───────────────────┘        │  │
│                                                           │                          │  │
│  [동작 순서]                                               ▼                          │  │
│  1. ChartObserver.attach(stockPrice)                     │                          │  │
│  2. AlertObserver.attach(stockPrice)                     │  Observer 등록           │  │
│  3. stockPrice.setPrice(100.5)                           │                          │  │
│     3-1. notify() 호출                                    │                          │  │
│     3-2. ChartObserver.update(100.5) → 그래프 갱신        │                          │  │
│     3-3. AlertObserver.update(100.5) → 알림 발송          │                          │  │
│  4. AlertObserver.detach(stockPrice)  → 구독 취소          │                          │  │
│                                                                             │
│  ✅ Subject는 Observer의 구체 타입을 몰라도 됨 (Loose Coupling)               │
│  ✅ Observer 추가/제거 시 Subject 코드 수정 불필요 (OCP 준수)                │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상단 다이어그램은 옵저버 패턴의 핵심 구조를 보여준다. Subject(StockPrice)는 Observer 인터페이스만 알 뿐, 구체적인 Observer(ChartObserver, AlertObserver)의 타입을 알 필요가 없다(Polymorphism). `setPrice()`로 가격이 변경되면 `notify()`가 호출되고, 등록된 모든 Observer의 `update()`가 순차적으로 실행된다. 새로운 Observer(예: KafkaProducerObserver)를 추가하려면 Observer 인터페이스를 구현하고 `attach()`만 하면 되므로, Subject 코드는 전혀 수정할 필요가 없다(Open-Closed Principle 준수).

#### 심층 동작 원리: 푸시(Push) 모델 vs 풀(Pull) 모델

옵저버 패턴에서 Subject가 Observer에게 데이터를 **"보내는(Push)"** 방식과 Observer가 **"가져오는(Pull)"** 방식이 있다.

```
[Push Model - Subject가 데이터를 전송]
Subject.notify() {
    for (Observer o : observers) {
        o.update(this.data);  // Subject가 데이터를 결정하여 전송
    }
}

[Pull Model - Observer가 데이터를 가져옴]
Subject.notify() {
    for (Observer o : observers) {
        o.update(this);  // Subject 참조만 전달
    }
}
Observer.update(subject) {
    Data data = subject.getData();  // Observer가 필요한 데이터를 직접 조회
}
```

Push 모델은 Observer가 필요한 데이터를 정확히 알 때 적합하고, Pull 모델은 데이터가 크거나 Observer가 필요한 부분만 선택적으로 가져올 때 유리하다.

- **📢 섹션 요약 비유**: Push는 신문사가 뉴스를 집까지 배달하는 것이고, Pull은 독자가 우체통에서 신문을 찾아오는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 옵저버 vs Pub/Sub vs Event Bus

| 비교 항목 | 옵저버(Observer) | PUB/SUB | 이벤트 버스(Event Bus) |
|:---|:---|:---|:---|
| **결합도** | Subject-Observer 1:N 직접 연결 | 완전 분리(Anonymous) | 완전 분리 |
| **통신 방식** | 동기(Sync) 메서드 호출 | 비동기(Async) 메시지 | 비동기 메시지 |
| **확장성** | 프로세스 내부 확장 | 분산 시스템 확장 | 마이크로서비스 확장 |
| **예시** | Swing Listener, React State | Kafka, RabbitMQ | Axon, EventBus |
| **비유** | 뉴스레터 구독 | 라디오 방송 | SNS |

#### 2. MVC 패턴에서의 옵저버 적용

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                  Observer Pattern in MVC Architecture                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Model (Subject)                                                    │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ - data: BusinessEntity                                         │  │   │
│  │  │ + setData(data) {                                             │  │   │
│  │  │     this.data = data;                                          │  │   │
│  │  │     notifyObservers();  // 상태 변경 알림                    │  │   │
│  │  │ }                                                             │  │   │
│  │  │ + notifyObservers() { ... }                                   │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────┬───────────────────────────────────────┘   │
│                                │ notifies                                  │
│            ┌───────────────────┼───────────────────┬───────────────────┐    │
│            ▼                   ▼                   ▼                   ▼    │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │View 1 (Chart)│    │View 2 (Table)│    │View 3 (Form) │    │Controller   │  │
│  │Observer      │    │Observer      │    │Observer      │    │Observer    │  │
│  │update() →    │    │update() →    │    │update() →    │    │update() →  │  │
│  │차트 다시 그리기│    │테이블 갱신   │    │폼 필드 채우기│    │로직 처리   │  │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘  │
│                                                                             │
│  ✅ Model은 View/Controller의 존재를 몰라도 됨 (Loose Coupling)            │
│  ✅ 새로운 View 추가 시 Model 코드 수정 불필요 (OCP 준수)                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 과목 융합 관점

- **컴퓨터 구조(CA)**: 옵저버 패턴은 하드웨어 인터럽트(Interrupt) 핸들링의 소프트웨어적 표현이다. CPU가 입출력(I/O) 장치에 데이터를 요청한 후, 장치가 준비되면 인터럽트를 발생시키고, 인터럽트 핸들러(Interrupt Handler)가 이를 처리한다. 이때 CPU은 모든 장치를 직접 폴링(Polling)하지 않고, 장치가 능동적으로 알림을 보내는 Observer 구조로 설계된다.

- **운영체제(OS)**: 리눅스의 inotify 파일 시스템 감시, kobject 이벤트 시스템, epoll(Edge Polling) I/O 다중화는 모두 옵저버 패턴의 응용이다. 프로세스가 파일 변경 이벤트를 구독(Subscribe)하고, 커널이 이벤트를 발행(Publish)하면, 등록된 프로세스에게 알림이 전달된다.

- **데이터베이스(DB)**: 트리거(Trigger)는 옵저버 패턴의 DB 버전이다. 특정 테이블에 INSERT/UPDATE/DELETE가 발생하면, 트리거라는 "Observer"가 자동으로 실행되어 연관된 로직(로그 기록, 통계 집계)을 수행한다.

- **📢 섹션 요약 비유**: 인스타그램 팔로워(Observer)가 포스팅되면, 좋아요(Observer)를 누른 구독자들에게 알림이 자동으로 전송되는 것과 같습니다. 인스타그램은 누가 좋아요를 눌렀는지 관심 없이, 그저 "새 포스팅 있음" 알림만 보내면 되죠(Loose Coupling).

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **실무 시나리오 1: 주식 가격 알림 시스템**
    - **문제**: 특정 종목의 가격 변경 시 웹 화면, 모바일 앱, 이메일 알림, 슬랙 알림에 동시 전달 필요.
    - **의사결정**: Kafka PUB/SUB로 확장하여 StockPrice Producer가 가격 변경 이벤트를 발행, 각 컨슈머(Web, Mobile, Email, Slack)가 독립적으로 구독.
    - **결과**: 새로운 알림 채널(텔레그램) 추가 시 기존 시스템 코드 수정 불필요, 확장성 확보.

- **실무 시나리오 2: React 상태 관리의 옵저버 패턴**
    - **문제**: 부모 컴포넌트의 상태 변경 시 자식 컴포넌트에게 자동으로 전달 필요.
    - **의사결정**: Context API 또는 Redux(상태 관리 라이브러리)를 활용하여 옵저버 패턴 적용.
    - **결과**: Props Drilling(Props를 깊게 전달) 문제 해결, 컴포넌트 간 결합도 감소.

- **도입 체크리스트**:
    1. **결합도(Coupling) 확인**: Subject와 Observer가 인터페이스를 통해 통신하는가? (구체 클래스 의존 피하기)
    2. **메모리 누수(Memory Leak) 확인**: Observer가 해제될 때 `detach()` 호출되어 참조가 제거되는가?
    3. **성능 고려**: Observer 수가 수백만 개일 때마다 순차적 `notify()` 호출의 성능 문제는 없는가?
    4. **동기/비동기 선택**: 즉시 반영이 필요하면 Sync 메서드 호출, 비동기 처리가 가능하면 메시지 큐 활용.

- **안티패턴**:
    - **Chaining Notification**: Observer가 `update()`에서 다시 상태를 변경하여 무한 루프(Infinite Loop) 발생.
    - **Observer Leak**: Observer를 `detach()`하지 않아 가비지 컬렉션(Garbage Collection) 대상에서 제외.
    - **Race Condition**: 멀티스레드 환경에서 `notify()` 도중 Observer 리스트가 수정되어 ConcurrentModificationException 발생.

- **📢 섹션 요약 비유**: 구독자 해지 신청을 받지 않는 신문사는 스팸 메일을 계속 보내게 되어, 고객 불만이 폭주하듯, 옵저버 패턴도 생명주기(Lifecycle) 관리에 신경 써야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량/정성 기대효과**:

| 구분 | 옵저버 미적용 시 | 옵저버 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 새 UI 추가 시 기존 코드 5곳 수정 | Observer 추가만으로 완료 | **수정 범위 100% 감소** |
| **정량** | 폴링(Polling)으로 CPU 30% 사용 | 이벤트 기반 0.1% 사용 | **CPU 효율 99.7% 개선** |
| **정성** | Subject-Observer 강한 결합 | 느슨한 결합 | **확장성 대폭 향상** |
| **정성** | 동기 처리로 인해 Blocking | 비동기 PUB/SUB | **응답성(Response) 개선** |

- **미래 전망**:
    1. **Reactive Streams**: RxJava, Project Reactor가 옵저버 패턴을 데이터 스트림(Data Stream)으로 확장하여, 비동기 데이터 흐름을 함수형(Functional)으로 처리하는 패러다임이 보편화되고 있다.
    2. **WebSocket Server-Sent Events**: 실시간 양방향 통신에서 옵저버 패턴이 기본 메커니즘으로 활용된다.

- **참고 표준**:
    - **Gang of Four Book**: "Design Patterns" - Observer Pattern 챕터
    - **Reactive Manifesto**: Reactive 시스템의 핵심 원칙
    - **Observer Pattern UML**: OMG 표준 다이어그램

- **📢 섹션 요약 비유**: 과거에는 신문사가 배달부를 직접 고용했지만, 현대에는 우편 시스템(PUB/SUB)을 통해 전 세계 독자에게 신문을 배달하듯, 옵저버 패턴도 분산 메시징 시스템으로 진화하고 있습니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[행위 패턴(Behavioral Patterns)](./566_behavioral_patterns.md)**: 옵저버가 속한 상위 카테고리.
- **[MVC 패턴](./210_mvc_pattern.md)**: 옵저버의 대표적 응용 사례.
- **[Kafka/PUB/SUB](./xx_messaging_queue.md)**: 옵저버의 분산 시스템 확장.
- **[Reactive Programming](./327_reactive.md)**: 옵저버를 데이터 스트림으로 확장.
- **[이벤트 버스(Event Bus)](./xx_event_bus.md)**: MSA 환경의 옵저버 구현.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 옵저버 패턴은 유튜브에 **"좋아요"를 누르면** 새 영상 알림이 자동으로 오는 것처럼, 구독자가 구독을 신청하면 새로운 소식이 있을 때마다 **자동으로 알려주는 시스템**이에요.
2. 신문사(Subject)는 누가 신문을 읽는지(Observer) 알 필요 없이, 그냥 신문만 내면 독자들이 각자 신문을 가져가게 되는 거죠.
3. 그래서 새로운 독자가 생겨도 신문사는 아무것도 바꿀 필요가 없어서, 아주 편리하고 확장하기 쉬워진답니다!
