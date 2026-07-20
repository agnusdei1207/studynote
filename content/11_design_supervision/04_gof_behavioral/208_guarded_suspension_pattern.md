---
title: "Guarded Suspension Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 208
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Guarded Suspension (가드 서스펜션) 패턴은 특정 가드 조건(Guard Condition)이 충족될 때까지 요청 스레드를 <strong>일시 중단(suspend)</strong>시키고, 조건이 만족되면 재개하는 동시성 제어 패턴이다.
> 2. **가치**: 생산자-소비자(Producer-Consumer) 패턴의 핵심 메커니즘으로, 빈 큐에서 소비하거나 가득 찬 큐에 넣으려는 시도를 CPU를 낭비하지 않고(busy-waiting 없이) 대기시킨다.
> 3. **판단 포인트**: 조건이 곧 만족될 것이 예상될 때 사용한다. 조건이 절대 만족되지 않을 위험이 있다면 타임아웃(Timeout)과 함께 사용한다.

---

## Ⅰ. 개요 및 필요성
조건이 충족될 때까지 반복문으로 대기하는 방식:

```java
// ❌ Busy-Waiting (CPU 낭비)
while (queue.isEmpty()) {
    // 아무것도 안 하고 계속 확인 -> CPU 100% 낭비
}
T item = queue.poll();
```

이는 CPU 사이클을 낭비하고 다른 스레드 실행 기회를 빼앗는다.

```java
// ✅ Guarded Suspension (wait/notify 기반)
synchronized (lock) {
    while (queue.isEmpty()) {   // Guard Condition
        lock.wait();            // 조건 불만족 -> suspend (CPU 반납)
    }
    return queue.poll();        // 조건 만족 -> 실행 재개
}

// 생산자가 아이템 추가 후 notify
synchronized (lock) {
    queue.add(item);
    lock.notifyAll();           // 대기 중인 소비자 깨우기
}
```

```
  Producer Threads            Consumer Threads
        |                           |
        | produce(item)             | consume()
        v                           v
  +---------------------------------------------+
  |       Shared Buffer (BlockingQueue)         |
  |                                             |
  |  [Guard: 가득 참] Producer -> wait()         |
  |  [Guard: 비어 있음] Consumer -> wait()       |
  |                                             |
  |  -> 조건 충족 시 notify()로 재개             |
  +---------------------------------------------+
```

- **📢 섹션 요약 비유**: 식당의 주문 대기표 — 테이블이 없을 때 손님(Consumer 스레드)이 쇼파에 앉아 기다린다. 직원이 "6번 테이블 준비됐습니다"라고 부를 때까지(notify) 무작정 서서 기다리지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  [ Guarded Suspension 실행 흐름 ]

  Thread A (Consumer)                Thread B (Producer)
       |                                    |
       | synchronized(lock)                 |
       | {                                  |
       |   while(!condition) {              |
       |     lock.wait();    --------------►|  (Thread A -> Wait Set)
       |   }                                |
       |   // 조건 충족 시 실행             |  synchronized(lock) {
       |   doWork();                        |    setCondition(true);
       | }                                  |    lock.notifyAll(); --►  Thread A 재개
                                            |  }
```

```java
// Java LinkedBlockingQueue 핵심 구현 (단순화)
public class SimpleBlockingQueue<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;
    private final Object lock = new Object();

    public void put(T item) throws InterruptedException {
        synchronized (lock) {
            while (queue.size() == capacity) {  // Guard: 가득 참
                lock.wait();
            }
            queue.add(item);
            lock.notifyAll();  // 소비자 깨우기
        }
    }

    public T take() throws InterruptedException {
        synchronized (lock) {
            while (queue.isEmpty()) {  // Guard: 비어 있음
                lock.wait();
            }
            T item = queue.poll();
            lock.notifyAll();  // 생산자 깨우기
            return item;
        }
    }
}
```

```
  Java `synchronized` + `wait/notify`  <-->  Condition Variable

  ReentrantLock 기반 (더 정교한 제어):
  +----------------------------------------------+
  |  Lock lock = new ReentrantLock();            |
  |  Condition notEmpty = lock.newCondition();   |
  |  Condition notFull  = lock.newCondition();   |
  |                                              |
  |  put():                                      |
  |    while (isFull)  notFull.await();  <- wait  |
  |    notEmpty.signal();                <- notify|
  |                                              |
  |  take():                                     |
  |    while (isEmpty) notEmpty.await(); <- wait  |
  |    notFull.signal();                 <- notify|
  +----------------------------------------------+
  -> 생산자/소비자 조건을 별도로 관리 가능
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 신호등의 초록불(Guard Condition) — 빨간불일 때 차들이 줄지어 기다리고(wait), 초록불이 켜지면(notifyAll) 한꺼번에 출발한다.

---

## Ⅲ. 비교 및 연결
| 방식 | CPU 사용 | 응답성 | 구현 복잡도 | 사용 상황 |
|:---|:---|:---|:---|:---|
| **Busy-Waiting** | 100% | 즉시 | 낮음 | ❌ 거의 사용 안 함 |
| **Guarded Suspension** | 0% (대기 중) | notify 시 | 중간 | 생산자-소비자 |
| **Timed Waiting** | 0% (대기 중) | 타임아웃 or notify | 중간 | 외부 이벤트 대기 |
| <strong>Polling with sleep</strong> | 낮음 | sleep 주기 | 낮음 | 단순 폴링 |

```
  데드락 발생 시나리오:
  - Thread A: lock1 점유, lock2 대기
  - Thread B: lock2 점유, lock1 대기
  -> 영원히 서로를 기다림 = 데드락

  Guarded Suspension에서의 주의:
  +------------------------------------------------+
  |  ❌ 위험: notifyAll() 누락                     |
  |    -> 생산자가 아이템 추가 후 알리지 않으면     |
  |       소비자가 영원히 대기 = 잠재적 데드락     |
  |                                                |
  |  ✅ 안전: while + notifyAll 패턴               |
  |    -> if 대신 while: spurious wakeup 방지       |
  |    -> notifyAll: 모든 대기 스레드 깨움          |
  |    -> 타임아웃: wait(5000) 최대 5초 대기        |
  +------------------------------------------------+
```

- **📢 섹션 요약 비유**: 경비원(Guard) 근무교대 — 교대 인원이 도착할 때까지 자리를 비우지 않고 기다린다(suspend). 교대 인원이 오면(notify) 임무를 넘기고 자리를 뜬다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 실무에서는 직접 구현보다 BlockingQueue 활용 권장
BlockingQueue<Task> taskQueue = new LinkedBlockingQueue<>(100);

// Producer (작업 추가)
Executors.newSingleThreadExecutor().submit(() -> {
    while (true) {
        Task task = fetchFromExternalSystem();
        taskQueue.put(task);  // 가득 차면 자동 대기 (Guarded Suspension 내장)
    }
});

// Consumer (작업 처리)
Executors.newFixedThreadPool(4).submit(() -> {
    while (true) {
        Task task = taskQueue.take();  // 비어 있으면 자동 대기
        process(task);
    }
});
```

- Guarded Suspension의 핵심: **Guard Condition + wait() + notifyAll()** 3요소
- `if` 대신 `while`을 사용하는 이유: **Spurious Wakeup (허위 깨움)** 방지
- `notify()` vs `notifyAll()` 차이: `notify()`는 임의 하나만 깨움 -> `notifyAll()` 권장
- 실무에서는 `java.util.concurrent.BlockingQueue`로 추상화 활용

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 응급실 대기 — 의사(Consumer)가 없을 때 환자(요청)는 대기실에서 기다린다. 의사가 준비되면(조건 충족) 호출받아 진료를 시작한다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| CPU 효율성 | busy-waiting 대비 CPU 사용률 제거 |
| 동기화 보장 | 조건 기반 안전한 공유 자원 접근 |
| 확장성 | 생산자·소비자 수를 독립적으로 조절 가능 |
| 배압(Back-Pressure) 구현 | 큐가 가득 차면 생산자 자동 제어 |

- <strong>Deadlock</strong>: notifyAll() 누락 시 영원한 대기 위험
- **Spurious Wakeup**: `if` 대신 `while`로 조건 재확인 필수
- <strong>Starvation (기아)</strong>: 특정 스레드가 항상 대기하는 상황 방지 -> 공정성(Fairness) 정책

Guarded Suspension (가드 서스펜션)은 멀티스레드 프로그래밍의 핵심 기법이다. Java의 `wait/notify`, `Condition.await/signal`, `BlockingQueue` 모두 이 패턴을 구현한 것이다. 생산자-소비자 아키텍처의 근간으로, 동시성과 효율성을 동시에 달성하는 방법이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Guarded Suspension은 "스마트한 대기" — 조건이 맞을 때까지 잠들어(wait) CPU를 낭비하지 않고, 조건이 충족되면 깨워달라고(notify) 요청하는 효율적인 대기 방식.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 동시성 패턴 (Concurrency Pattern) | 병렬 처리 설계 패턴 그룹 |
| 연관 개념 | Producer-Consumer Pattern | Guarded Suspension의 주요 적용 사례 |
| 연관 개념 | BlockingQueue (Java) | Guarded Suspension의 실용적 구현 |
| 연관 개념 | Condition Variable | POSIX 스레딩의 동일 개념 |
| 연관 개념 | Deadlock | 잘못 구현 시 발생하는 위험 |
| 연관 개념 | Monitor Object Pattern | Guarded Suspension의 상위 패턴 |

### 📈 관련 키워드 및 발전 흐름도
조건 대기 -> 가드 서스펜션 패턴 -> Producer-Consumer

### 👶 어린이를 위한 3줄 비유 설명
1. 엄마가 밥을 다 차릴 때까지 아이들은 식탁에서 기다려요(suspend).
2. "다 됐다!"라고 부르면(notify) 모두 달려와서 먹어요.
3. 밥이 없는데 계속 숟가락을 들고 서 있는 건(busy-waiting) 너무 피곤하잖아요!
