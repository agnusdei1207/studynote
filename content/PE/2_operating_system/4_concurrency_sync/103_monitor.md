+++
title = "33. 모니터 (Monitor)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Monitor", "Synchronization", "Condition-Variable", "Hoare-Semantics", "Mesa-Semantics"]
draft = false
+++

# 모니터 (Monitor)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모니터는 **"공유 데이터**와 **동기화 **기능을 **캡슐화**한 **고급 동기화 **추상화"**로, **Mutex**(Lock)와 **Condition Variable**로 **구성**되며 **Hoare Semantics**(신호 즉시 전달)과 **Mesa Semantics**(신호 대기열)로 **구분**된다.
> 2. **동작 원리**: **enter**로 **진입**하고 **exit**로 **탈출**하며 **wait**()로 **조건 **대기**하고 **signal**()/**broadcast**()로 **대기 중인 **스레드**를 **깨운다**(Wakeup).
> 3. **융합**: **Java synchronized**, **wait/notify**, **pthread_cond_t**, **C++ std::condition_variable**가 **구현**을 **제공**하며 **Reader-Writer Problem**, **Producer-Consumer**를 **해결**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
모니터는 **"동기화를 캡슐화한 추상화"**이다.

**모니터 구성**:
- **Lock**: 상호 배제
- **Condition Variables**: 조건 대기
- **Invariant**: 불변 조건

### 💡 비유
모니터는 **"안내 데스크****와 같다.
- **대기실**: Condition Queue
- **호출**: Lock
- **번호표**: Signal

---

## Ⅱ. 아키텍처 및 핵심 원리

### 모니터 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Monitor Structure                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Class Monitor {                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  private:                                                                            │  │  │
    │  │      Lock mutex;                     // 상호 배제                                   │  │  │
    │  │      Condition cond;                // 조건 변수                                     │  │  │
    │  │      SharedData data;               // 공유 데이터                                   │  │  │
    │  │                                                                                       │  │  │
    │  │  public:                                                                             │  │  │
    │  │      void operation() {             // 모니터 메서드                                  │  │  │
    │  │          mutex.lock();             // enter (자동 호출)                              │  │  │
    │  │          while (!condition) {                                                   │  │  │
    │  │              cond.wait(mutex);    // 조건 대기                                     │  │  │
    │  │          }                                                                                │  │  │
    │  │          // Critical Section                                                          │  │  │
    │  │          cond.signal();             // 신호                                          │  │  │
    │  │          mutex.unlock();           // exit (자동 호출)                               │  │  │
    │  │      }                                                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Condition Variable

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Condition Variable Operations                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  wait(condition, mutex)                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. 현재 스레드를 condition queue에 추가                                               │  │  │
    │  │  2. mutex 해제                                                                         │  │  │
    │  │  3. 대기 (blocked)                                                                    │  │  │
    │  │  4. signal/broadcast 수신 시 깨어남                                                     │  │  │
    │  │  5. mutex 재획득                                                                       │  │  │
    │  │  6. 복귀                                                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  signal(condition)                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • condition queue의 한 스레드를 깨움                                                │  │  │
    │  │  │  • 대기열이 비면 아무 일 없음                                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  broadcast(condition)                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • condition queue의 모든 스레드를 깨움                                               │  │  │
    │  │  │  → 모두 경쟁하며 하나만 진입                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Hoare vs Mesa Semantics

| 구분 | Hoare | Mesa |
|------|-------|------|
| **Signal** | 즉시 전달 | 대기열 추가 |
| **Lock** | 즉시 이전 | 재획득 필요 |
| **Wait** | while 불필요 | while 필수 |

### Monitor vs Semaphore

| 구분 | Monitor | Semaphore |
|------|---------|-----------|
| **캡슐화** | O | X |
| **복잡도** | 높음 | 낮음 |
| **타입 안전** | O | X |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Java Monitor
**상황**: 생산자-소비자
**판단**:

```java
class BoundedBuffer {
    private final int[] buffer;
    private int count = 0;

    public synchronized void produce(int item) throws InterruptedException {
        while (count == buffer.length) {
            wait();  // 대기
        }
        buffer[count++] = item;
        notifyAll();  // 모두 깨움
    }

    public synchronized int consume() throws InterruptedException {
        while (count == 0) {
            wait();  // 대기
        }
        int item = buffer[--count];
        notifyAll();  // 모두 깨움
        return item;
    }
}
```

---

## Ⅴ. 기대효과 및 결론

### Monitor 기대 효과

| 효과 | 없음 | Monitor |
|------|------|---------|
| **추상화** | 낮음 | 높음 |
| **안전성** | 취약 | 강함 |
| **복잡도** | 단순 | 복잡 |

### 모범 사례

1. **while check**: Mesa 필수
2. **broadcast**: 다중 조건
3. **notifyAll**: 안전 선택
4. **timeout**: 대기 제한

### 미래 전망

1. **Actor Model**: 메시지 전달
2. **Coroutine**: 비동기
3. **Software TM**: 트랜잭션

### ※ 참고 표준/가이드
- **Hoare**: Monitors
- **Java**: synchronized, wait/notify
- **POSIX**: pthread_cond_t

---

## 📌 관련 개념 맵

- [뮤텍스](./101_mutex.md) - 상호 배제
- [세마포어](./102_semaphore.md) - 카운팅
- [데드락](./105_deadlock.md) - 교착
