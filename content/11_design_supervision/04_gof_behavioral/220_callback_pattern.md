---
title: "Callback Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 220
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Callback (콜백) 패턴은 함수를 인수로 전달하여 특정 이벤트나 작업 완료 시점에 호출되도록 하는 역전된 제어(Inversion of Control) 메커니즘이다 — "나중에 전화해줄게" 방식의 비동기 통지.
> 2. **가치**: 비동기 작업 완료 후 취해야 할 행동을 호출자가 직접 정의하고 전달할 수 있어, 호출자와 비동기 실행자를 느슨하게 결합한다.
> 3. **판단 포인트**: 콜백 지옥(Callback Hell / Pyramid of Doom)은 중첩 콜백이 만드는 가독성·유지보수성 붕괴다 — Promise, async/await, Observable이 이를 해결하는 발전된 패턴이다.

---

## Ⅰ. 개요 및 필요성
동기 방식으로 비동기 결과를 기다리면:
```java
// 동기 블로킹: 결과가 올 때까지 스레드 멈춤
String result = httpGet("https://api.example.com/data"); // 수백 ms 블로킹
process(result);
```

이벤트 기반/비동기 환경에서는 스레드를 블로킹할 수 없다.

콜백 방식으로 해결:
```javascript
// 비동기: 요청만 하고 완료 시 콜백 호출
httpGet("https://api.example.com/data", function(error, result) {
    if (error) handleError(error);
    else process(result); // 완료 후 호출
});
// 이 라인은 httpGet 완료를 기다리지 않고 즉시 실행
doOtherWork();
```

| 유형 | 설명 | 특징 |
|:---|:---|:---|
| 동기 콜백 (Sync Callback) | 호출 즉시 실행 | 블로킹, 예측 가능한 순서 |
| 비동기 콜백 (Async Callback) | 이벤트/완료 후 호출 | 논블로킹, 실행 순서 불확실 |

```javascript
// 동기 콜백: Array.forEach, Array.map
[1, 2, 3].forEach(n => console.log(n)); // 즉시, 순서대로 실행

// 비동기 콜백: setTimeout, addEventListener
setTimeout(() => console.log("1초 후 실행"), 1000);
element.addEventListener("click", () => console.log("클릭됨")); // 이벤트 발생 시
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 콜백은 식당에서 "음식 나오면 문자 주세요" 방식 — 음식이 나올 때까지 자리에 앉아 기다리지(블로킹) 않고, 카운터 번호표(콜백 함수)를 주고 다른 일을 하다가 호출받는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+--------------------------------------------------------------+
|                    Callback Pattern 흐름                     |
|                                                              |
|  +----------+  1. 작업 요청 + 콜백 함수 전달                  |
|  |  Caller  |-----------------------------------------+     |
|  | (호출자)  |                                         |     |
|  +----------+                                         v     |
|                                           +-----------------+|
|                                           | Async Executor  ||
|                                           | (비동기 실행자)  ||
|                                           |  예: Timer,     ||
|  +----------+  2. 다른 작업 계속 수행      |  IO, Network   ||
|  |  Caller  |                             +--------+--------+|
|  | 다른 일 중|                                      |         |
|  +----------+                    3. 작업 완료       |         |
|                                                    |         |
|  +----------+  4. 콜백 함수 호출됨                  |         |
|  |  Callback|<------------------------------------+         |
|  |  Handler |  (에러, 결과 데이터 전달)                      |
|  +----------+                                              |
+--------------------------------------------------------------+
```

비동기 작업이 체인처럼 연결될 때:

```javascript
// 콜백 지옥: 가독성 파괴, 에러 처리 분산
getUser(userId, function(err, user) {
    if (err) handleError(err);
    else getOrders(user.id, function(err, orders) {
        if (err) handleError(err);
        else getOrderDetails(orders[0].id, function(err, details) {
            if (err) handleError(err);
            else getProduct(details.productId, function(err, product) {
                if (err) handleError(err);
                else {
                    console.log(product); // 실제 목적은 이 한 줄
                }
            });
        });
    });
});
// 피라미드 형태 -> "Pyramid of Doom"
```

```
콜백 (Callback)
  +-> 문제: 중첩, 에러 처리 분산
       +-> Promise (ES6)
            +-> 문제: .then() 체인 길어짐
                 +-> async/await (ES2017)
                      +-> 추가: Observable/RxJS (반응형 스트림)
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 콜백 지옥은 러시아 마트료시카 인형 — 인형 속에 인형이 계속 들어가서, 진짜 원하는 인형(비즈니스 로직)을 꺼내려면 겹겹이 쌓인 껍데기(에러 처리, 조건문)를 다 벗겨야 한다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 표현 방식 | 에러 처리 | 가독성 | 사용 환경 |
|:---|:---|:---|:---|:---|
| Callback | 함수 인수 전달 | 각 콜백마다 | 낮음 (중첩) | Node.js (초기) |
| Promise | `.then().catch()` | `.catch()` 통합 | 중간 | 모든 JS 환경 |
| async/await | `await` 키워드 | `try/catch` | 높음 (동기처럼) | ES2017+ |
| Observable (RxJS) | 스트림 연산자 | `.catchError()` | 중간~높음 | Angular, 반응형 |
| CompletableFuture | `.thenApply()` | `.exceptionally()` | 중간 | Java |

```
동기 콜백 실행:
  호출자 -> sort([3,1,2], compareFn)
  실행: compareFn이 sort() 내부에서 즉시, 반복 호출
  반환: 정렬 완료 후 sort()가 반환

비동기 콜백 실행:
  호출자 -> setTimeout(cb, 1000)
  실행: 1000ms 후 Event Loop가 cb를 호출
  반환: setTimeout()은 즉시 반환 (cb 실행 전)
```

- **📢 섹션 요약 비유**: 동기 콜백은 요리사가 "썰어줘" 라고 부르면 즉시 도와주는 보조 요리사, 비동기 콜백은 타이머를 맞춰두고 "알람 울리면 오븐 꺼줘" 라고 부탁하는 것이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 콜백 인터페이스 정의
@FunctionalInterface
public interface Callback<T> {
    void onComplete(T result, Throwable error);
}

// 비동기 작업자
public class AsyncService {
    public void fetchData(String id, Callback<String> callback) {
        CompletableFuture.supplyAsync(() -> loadData(id))
            .whenComplete((result, error) -> callback.onComplete(result, error));
    }
}

// 사용
service.fetchData("123", (result, error) -> {
    if (error != null) log.error("실패", error);
    else processResult(result);
});
```

콜백 패턴은 Observer (옵저버) 패턴의 단순화된 형태다:

| 비교 | Callback | Observer |
|:---|:---|:---|
| 구독자 수 | 1개 (일반적) | N개 가능 |
| 지속성 | 일회성 (보통) | 지속적 구독 |
| 취소 | 어려움 | 구독 해제(unsubscribe) |
| 스트림 처리 | 부적합 | 적합 (RxJS, Reactor) |

```javascript
// Node.js 표준 콜백 규약: (error, result) 순서
fs.readFile('file.txt', 'utf8', (err, data) => {
    if (err) {
        console.error('읽기 실패:', err);
        return;
    }
    console.log('파일 내용:', data);
});
```

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: Node.js의 Error-First 콜백은 소방서 보고 규약처럼 — 항상 "이상 없음/있음" 상황 보고(err)를 먼저 하고, 문제 없을 때만 세부 정보(data)를 보고한다.

---

## Ⅴ. 기대효과 및 결론
콜백 패턴은 비동기 프로그래밍의 출발점이자, 현대 비동기 패턴들(Promise, async/await, Reactive Streams)의 원형이다:

**장점**:
- 단순하고 범용적 — 어떤 환경에서도 구현 가능
- 이벤트 기반 시스템(GUI, 네트워크, 타이머)에 자연스럽게 적합
- 낮은 추상화 오버헤드

**콜백 지옥의 대안 선택 기준**:

| 상황 | 권장 패턴 |
|:---|:---|
| 단순 비동기 1~2 단계 | Callback 직접 사용 |
| 다단계 비동기 체인 | Promise 또는 async/await |
| 여러 이벤트 스트림 | Observable (RxJS, Reactor) |
| Java 다단계 비동기 | CompletableFuture |

콜백 패턴을 이해하면 Promise, async/await의 설계 의도와 문제 해결 방식을 깊이 이해할 수 있다. 심화 학습에서는 <strong>콜백 지옥의 문제점과 Promise/async/await로의 발전 과정</strong>을 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 콜백은 오래된 호출기(삐삐) — 메시지(콜백 인수)를 받아서 직접 행동(콜백 로직)해야 한다. Promise는 스마트폰 알림 — 여러 알림을 체계적으로 관리하고, async/await는 마치 직접 통화하는 것처럼 자연스럽게 비동기를 동기 코드처럼 쓸 수 있다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 제어 역전 (Inversion of Control) | 콜백이 구현하는 핵심 원칙 |
| 연관 패턴 | Observer Pattern | 콜백의 다중 구독자 확장 |
| 발전 패턴 | Promise/Future | 콜백 지옥을 해결한 상위 추상화 |
| 발전 패턴 | async/await | Promise의 문법적 설탕 |
| 발전 패턴 | Observable (RxJS) | 이벤트 스트림 처리를 위한 반응형 확장 |
| 구현체 | Node.js EventEmitter | 비동기 이벤트 기반 콜백 시스템 |
| 연관 패턴 | Command Pattern | 콜백 함수를 커맨드 객체로 캡슐화 |

### 📈 관련 키워드 및 발전 흐름도
이벤트 통지 -> 콜백 패턴 -> 비동기 흐름 제어

### 👶 어린이를 위한 3줄 비유 설명
1. 콜백은 피자 배달 주문 — "피자 다 되면 전화(콜백)해줘" 하고 전화번호(콜백 함수)를 알려주면, 완성됐을 때 전화가 온다.
2. 콜백 지옥은 "피자 오면 콜라 주문하고, 콜라 오면 아이스크림 주문하고, 아이스크림 오면 케이크 주문해" 처럼 주문이 주문을 낳아서 종이가 삐뚤빼뚤해지는 것이야.
3. Promise와 async/await는 콜백 지옥을 없애줘서 "피자, 콜라, 아이스크림, 케이크를 차례로 기다리자" 처럼 깔끔하게 쓸 수 있게 해줘.
