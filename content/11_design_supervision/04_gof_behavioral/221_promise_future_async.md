---
title: "Promise/Future Async Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 221
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Promise / Future (프로미스/퓨처)는 "아직 완료되지 않은 비동기 연산의 미래 결과"를 나타내는 객체로, 콜백 지옥(Callback Hell)을 탈피하고 비동기 연산을 체이닝(Chaining)으로 표현하는 비동기 패턴이다.
> 2. **가치**: Promise 상태 기계(Pending -> Fulfilled/Rejected)와 `.then()/.catch()` 체이닝으로 다단계 비동기 흐름을 선형 코드로 표현할 수 있어 가독성과 에러 처리가 획기적으로 개선된다.
> 3. **판단 포인트**: `async/await`는 Promise의 문법적 설탕(Syntactic Sugar) — Promise 위에서 동작하며, `await`는 Promise가 완료될 때까지 현재 함수를 일시 중단하되 스레드를 블로킹하지 않는다.

---

## Ⅰ. 개요 및 필요성
```javascript
// 콜백 지옥 (Before)
getUser(id, (err, user) => {
    if (err) return handleErr(err);
    getOrders(user.id, (err, orders) => {
        if (err) return handleErr(err);
        getProduct(orders[0].productId, (err, product) => {
            if (err) return handleErr(err);
            console.log(product);
        });
    });
});

// Promise 체이닝 (After)
getUser(id)
    .then(user => getOrders(user.id))
    .then(orders => getProduct(orders[0].productId))
    .then(product => console.log(product))
    .catch(err => handleErr(err)); // 에러 중앙 처리
```

```
+----------------------------------------------------------+
|               Promise State Machine                      |
|                                                          |
|   +-------------+                                        |
|   |   PENDING   | <- 초기 상태 (비동기 작업 진행 중)        |
|   |  (대기 중)   |                                        |
|   +------+------+                                        |
|          |                                               |
|    +-----+-----+                                         |
|    |           |                                         |
|    v           v                                         |
| +----------+ +----------+                                |
| |FULFILLED | | REJECTED |                                |
| |(이행 완료)| |(거부/실패)|                                |
| +----------+ +----------+                                |
|                                                          |
|  ※ 한번 결정(Settled)되면 상태 변경 불가 (불변)            |
+----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Promise는 식당 예약 확인서 — "아직 확정 안 됨(Pending)", "예약 확정(Fulfilled)", "예약 불가(Rejected)" 세 가지 상태가 있고, 한번 결정되면 다시 바꿀 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
Promise 생성:
  new Promise((resolve, reject) => {
      // 비동기 작업
      resolve(result);  // 성공 -> FULFILLED
      reject(error);    // 실패 -> REJECTED
  });

체이닝 API:
  .then(onFulfilled)           -> 성공 시 실행, 새 Promise 반환
  .catch(onRejected)           -> 실패 시 실행 (.then(null, onRejected))
  .finally(onFinally)          -> 성공/실패 무관 항상 실행 (정리 작업)

병렬 처리 API:
  Promise.all([p1, p2, p3])    -> 모두 완료 시 완료 (하나라도 실패 -> 실패)
  Promise.allSettled([...])    -> 모두 완료 시 완료 (실패 포함 결과 반환)
  Promise.race([p1, p2])       -> 첫 번째 완료/실패된 것 반환
  Promise.any([p1, p2])        -> 첫 번째 성공한 것 반환
```

```javascript
// Promise 체이닝
function fetchUserData(id) {
    return getUser(id)
        .then(user => getOrders(user.id))
        .then(orders => enrichOrders(orders))
        .catch(err => { throw new Error("사용자 데이터 오류: " + err.message); });
}

// async/await (동일 로직, 동기 코드처럼 읽힘)
async function fetchUserData(id) {
    try {
        const user   = await getUser(id);
        const orders = await getOrders(user.id);
        return await enrichOrders(orders);
    } catch (err) {
        throw new Error("사용자 데이터 오류: " + err.message);
    }
}
```

| JavaScript Promise | Java CompletableFuture | 설명 |
|:---|:---|:---|
| `.then(fn)` | `.thenApply(fn)` | 값 변환 (map) |
| `.then(() => promise)` | `.thenCompose(fn)` | Promise 반환 함수 (flatMap) |
| `.catch(fn)` | `.exceptionally(fn)` | 에러 처리 |
| `.finally(fn)` | `.whenComplete(fn)` | 항상 실행 |
| `Promise.all([...])` | `CompletableFuture.allOf(...)` | 모두 완료 대기 |

```text
+--------------+    +--------------+    +--------------+
| Input/State  |--->| Control Point |--->| Output/Action |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: async/await는 마법 안경 — 비동기 코드(구불구불한 실)를 쓰면 마치 직선처럼 보여주는 착시 안경이다. 실제 실행은 여전히 비동기(구불구불)지만, 읽기는 동기처럼 자연스럽다.

---

## Ⅲ. 비교 및 연결
```
Promise.all([A, B, C]):
  A: ------✓--
  B: ------------✓--
  C: --------------✓--
  결과: C 완료 후 [A결과, B결과, C결과] (모두 성공)
  하나라도 실패 -> 즉시 실패

Promise.race([A, B, C]):
  A: ------✓--           <- 가장 빠름
  결과: A 결과 (나머지는 무시)

Promise.allSettled([A, B, C]):
  모두 완료 후 [{status:"fulfilled",value:...}, {status:"rejected",...}]
  (실패해도 모두 기다림)

Promise.any([A, B, C]):
  첫 번째 성공한 결과 반환 (모두 실패 시 AggregateError)
```

| 언어/플랫폼 | Promise 유사체 | async/await | 비고 |
|:---|:---|:---|:---|
| JavaScript | `Promise` | `async/await` (ES2017) | 표준 |
| Java | `CompletableFuture` | 없음 (구조적 동시성 Java 21+) | 명시적 체이닝 |
| Kotlin | `Deferred` | `suspend fun` | 코루틴 기반 |
| C# | `Task<T>` | `async/await` (C# 5.0) | 선구자 |
| Python | `asyncio.Future` | `async/await` (Python 3.5) | — |
| Rust | `Future` | `async/await` (Rust 1.39) | Zero-cost 추상화 |

- **📢 섹션 요약 비유**: Promise.all은 모든 주문이 나올 때까지 기다리는 단체 식사, Promise.race는 가장 빨리 나오는 음식 먼저 먹기, Promise.allSettled는 누군가 주문 실수해도 다 나올 때까지 기다려서 결과 확인하기이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```javascript
// 순차 처리 (비효율적 — 직렬로 기다림)
async function sequential() {
    const a = await fetchA();   // 100ms
    const b = await fetchB();   // 100ms
    // 총 200ms
    return [a, b];
}

// 병렬 처리 (효율적 — 동시 실행)
async function parallel() {
    const [a, b] = await Promise.all([fetchA(), fetchB()]);
    // 총 max(100ms, 100ms) = 100ms
    return [a, b];
}
```

```java
// 비동기 체인 + 스레드 풀 지정
CompletableFuture<String> result =
    CompletableFuture.supplyAsync(() -> fetchUser(id), executor)
    .thenComposeAsync(user -> fetchOrders(user.getId()), executor)
    .thenApplyAsync(orders -> summarize(orders), executor)
    .exceptionally(ex -> "오류: " + ex.getMessage());

// 타임아웃 (Java 9+)
result.orTimeout(5, TimeUnit.SECONDS)
      .exceptionally(ex -> "타임아웃");
```

| 실수 | 문제 | 해결 |
|:---|:---|:---|
| `await`를 반복문 내부에서 순차 사용 | 직렬 실행 -> 느림 | `Promise.all()` 병렬화 |
| `.catch()` 누락 | 미처리 거부(UnhandledRejection) | 모든 체인에 `.catch()` |
| `async` 없이 `await` 사용 | SyntaxError | 함수에 `async` 명시 |
| CompletableFuture에서 blocking 호출 | 스레드 풀 고갈 | `thenComposeAsync` 사용 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: `await`를 반복문 안에서 쓰는 것은 식당에서 메뉴 하나 시키고 먹고, 또 시키고 먹는 것 — `Promise.all()`은 메뉴를 한번에 다 시켜서 동시에 나오게 하는 것이다.

---

## Ⅴ. 기대효과 및 결론
Promise/Future 패턴은 콜백 지옥을 해결하고 비동기 코드의 가독성을 혁신적으로 개선했다:

**핵심 기대효과**:
- **선형 코드 흐름**: 다단계 비동기 체인을 읽기 쉽게 표현
- **중앙화된 에러 처리**: `.catch()` / `try/catch` 하나로 모든 에러 처리
- <strong>병렬 처리 용이</strong>: `Promise.all()` 한 줄로 병렬 비동기 실행
- **언어 표준화**: 모든 현대 언어/플랫폼에서 동일한 개념

**한계**:
- 무한 스트림(이벤트 스트림) 처리에는 Observable이 더 적합
- 취소(Cancellation) 지원이 약함 (AbortController 별도 필요)
- Kotlin Coroutine, Java Virtual Thread가 새로운 대안으로 부상

심화 학습에서는 **Promise 상태 기계(Pending/Fulfilled/Rejected)**, **async/await가 Promise의 문법적 설탕임**, <strong>Promise.all vs Promise.race 차이</strong>를 명확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Promise는 은행 대기번호표 — 번호를 받고(Pending), 창구에서 처리되면(Fulfilled) 호출, 처리 불가하면(Rejected) 다른 창구(catch) 안내. async/await는 창구 앞에 직접 서서 기다리는 것처럼 쓰지만 실제로는 번호표 시스템이 돌아가고 있다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 비동기 프로그래밍 (Async Programming) | Promise가 해결하는 근본 문제 영역 |
| 전신 패턴 | Callback Pattern | Promise가 해결한 콜백 지옥의 원인 |
| 문법적 설탕 | async/await | Promise를 동기 코드처럼 표현하는 키워드 |
| 구현체 | Java CompletableFuture | Java의 Promise 유사체 |
| 구현체 | Kotlin Coroutine | 경량 스레드 기반 비동기 |
| 발전 패턴 | Observable (RxJS/Reactor) | 다중 비동기 이벤트 스트림 처리 |
| 연관 패턴 | Monad Pattern | CompletableFuture는 모나드 |

### 📈 관련 키워드 및 발전 흐름도
콜백 비동기 -> Promise/Future 비동기 패턴 -> structured concurrency

### 👶 어린이를 위한 3줄 비유 설명
1. Promise는 은행 대기표 — "아직 처리 중(Pending)", "처리 완료(Fulfilled)", "처리 불가(Rejected)" 세 가지 상태가 있고, 완료되면 다음 할 일(.then())을 알아서 실행해줘.
2. async/await는 마법 일시정지 버튼 — `await` 앞에서 잠깐 멈추고 결과를 받을 때까지 기다리지만, 다른 친구들(다른 코드)은 계속 놀게 해줘.
3. `Promise.all()`은 모든 친구가 준비될 때까지 기다렸다가 같이 출발하는 것이고, `Promise.race()`는 제일 빨리 준비된 친구를 따라가는 것이야.
