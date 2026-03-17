+++
title = "123. 뮤텍스 (Mutex)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Mutex", "Lock", "Mutual-Exclusion", "Synchronization", "Critical-Section"]
draft = false
+++

# 뮤텍스 (Mutex)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 뮤텍스(Mutual Exclusion, Mutex)는 **"한 번에 하나의 스레드만 공유 자원에 접근할 수 있도록 하는 상호 배제Lock 메커니즘"**으로, **Lock(잠금)**과 **Unlock(잠금 해제)** 연산을 통해 **Critical Section(임계 영역)**을 보호한다.
> 2. **가치**: **pthread_mutex**(POSIX), **std::mutex**(C++), **Lock**(Java, C#) 등 언어별 표준 라이브러리로 제공되며, **Spinlock**(바쁜 대기)과 대비하여 **Block Wait(대기 큐)**로 CPU를 절약하고 **OS 스케줄러**에 양보한다.
> 3. **융합**: **커널 모드 Mutex**(커널 동기화)와 **유저 모드 Mutex**(응용 프로그램)로 계층화되며, **futex**(Fast Userspace muTEX)는 **userspace와 kernel 간 하이브리드**로 빠른 Lock을 구현하고 **Reentrant Lock**, **Recursive Mutex**로 **Deadlock** 방지를 지원한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
뮤텍스(Mutex)는 **"공유 자원에 대한 상호 배제(Mutual Exclusion)를 보장하는 동기화 객체"**이다.

**뮤텍스의 2가지 상태**:
- **Locked(잠김)**: 한 스레드가 소유
- **Unlocked(잠금 해제)**: 다른 스레드가 획득 가능

### 💡 비유
뮤텍스는 **"화장실 열쇠"**와 같다.
- **열쇠(Mutex)**: 한 사람만 소유 가능
- **화장실(Critical Section)**: 공유 자원
- **사용**: 입장 → Lock → 사용 → Unlock → 퇴장

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         뮤텍스의 필요성                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

공유 변수 문제:
    • 여러 스레드가 동시에 변수 수정
    • 경쟁 상태(Race Condition) 발생
    • 데이터 무결성 깨짐
         ↓
상호 배제(Mutual Exclusion) 필요:
    • 한 번에 하나의 스레드만 접근
    • Dijkstra (1965): Semaphore 제안
    • 한 번만 신호(Semaphore=1) → Mutex
         ↓
뮤텍스 표준화:
    • POSIX Threads (pthread_mutex, 1995)
    • Win32 API (Mutex, 1993)
    • C++11 std::mutex (2011)
    • Java synchronized, Lock (1995)
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 뮤텍스 동작 원리

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         뮤텍스 Lock/Unlock 흐름                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [스레드 A와 스레드 B가 공유 변수 counter 증가]

    Thread A                                                    Thread B
    ┌─────────────────────┐                                 ┌─────────────────────┐
    │                     │                                 │                     │
    │  mutex.lock()       │                                 │                     │
    │  ┌────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Mutex: UNLOCKED → LOCKED                                                      │  │
    │  │  Owner: Thread A                                                               │  │
    │  │  Queue: []                                                                     │  │
    │  └────────────────────────────────────────────────────────────────────────────────┘  │
    │                     │                                 │  mutex.lock()       │
    │  ┌────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  [Critical Section]                                                             │  │  ┌───────────────────────────────────────────────────────────────┐  │
    │  │  counter = counter + 1                                                          │  │  │  Mutex: LOCKED (소유자: Thread A)                      │  │
    │  │                                                                                  │  │  │  → Thread B를 대기 큐(Wait Queue)에 추가                  │  │
    │  │  └────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                     │                                 │  [BLOCKED]           │
    │  mutex.unlock()     │                                 │  (대기 상태)          │
    │  ┌────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Mutex: LOCKED → UNLOCKED                                                        │  │  └───────────────────────────────────────────────────────────────┘  │
    │  │  Owner: -                                                                         │  │                             │                              │
    │  │  → Wait Queue 확인 → Thread B 깨움                                               │  │                             │                              │
    │  └────────────────────────────────────────────────────────────────────────────────┘  │                             │
    │                     │                                 │                             ▼                              │
    │                     │                                 │  ┌───────────────────────────────────────────────────────────────┐  │
    │                     │                                 │  │  Thread B: LOCK 획득                                           │  │
    │                     │                                 │  │  Owner: Thread B                                               │  │
    │                     │                                 │  └───────────────────────────────────────────────────────────────┘  │
    │                     │                                 │                             │                              │
    │                     │                                 │  ┌───────────────────────────────────────────────────────────────┐  │
    │                     │                                 │  │  [Critical Section]                                          │  │
    │                     │                                 │  │  counter = counter + 1                                        │  │
    │                     │                                 │  └───────────────────────────────────────────────────────────────┘  │
    │                     │                                 │                             │                              │
    │                     │                                 │  mutex.unlock()        │
    │                     │                                 │  Mutex: UNLOCKED        │
    └─────────────────────┘                                 └─────────────────────┘
```

### 뮤텍스 vs Spinlock

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         뮤텍스 vs 스핀락 비교                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [뮤텍스 (Mutex)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Lock 실패 시 대기 전략:                                                                  │
    │  1. 스레드를 BLOCKED 상태로 전환                                                         │
    │  2. OS에 CPU 양보 (Context Switch)                                                       │
    │  3. Wait Queue에서 대기                                                                   │
    │  4. Unlock 시 깨어남(Wakeup)                                                              │
    │                                                                                         │
    │  장점:                                                                                   │
    │  • CPU 낭비 없음                                                                         │
    │  │  긴 Critical Section에 적합                                                             │
    │                                                                                         │
    │  단점:                                                                                   │
    │  • Context Switch 오버헤드 (~µs 단위)                                                    │
    │  │  짧은 대기 시간에는 비효율적                                                             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [스핀락 (Spinlock)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Lock 실패 시 대기 전략:                                                                  │
    │  1. 계속해서 Lock 시도 (Busy Waiting)                                                      │
    │  2. CPU 점유하며 대기                                                                     │
    │  3. Unlock 즉시 감지                                                                      │
    │                                                                                         │
    │  장점:                                                                                   │
    │  • Context Switch 없음                                                                   │
    │  │  매우 짧은 대기(~수 µs)에 효율적                                                       │
    │                                                                                         │
    │  단점:                                                                                   │
    │  • CPU 낭비                                                                             │
    │  │  긴 Critical Section에 부적합                                                           │
    │  │  단일 코어에서 무의미                                                                  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [선택 기준]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Critical Section 길이 │  추천 Lock    │  이유                                           │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  짧음 (~수 µs)          │  Spinlock     │  Context Switch 오버허드보다 큼                        │
    │  김 (~ms 이상)          │  Mutex        │  CPU 낭비 방지                                    │
    │  중간                 │  Adaptive Mutex│  상황에 따라 동적 선택                               │
    │  커널 모드             │  Spinlock     │  스케줄러 호출 불가                                  │
    │  유저 모드             │  Mutex        │  OS 스케줄러 활용                                 │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 뮤텍스 종류

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         뮤텍스 종류별 특징                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [1. 일반 뮤텍스 (Normal Mutex)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 가장 기본적인 뮤텍스                                                                │
    │  │  Lock을 획득한 스레드만 Unlock 가능                                                     │
    │  │  다른 스레드가 Unlock 시 → Undefined Behavior                                         │
    │  │  재진입(Reentrant) 불가                                                              │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘
    │                                                                                         │
    │  C++: std::mutex                                                                        │
    │  pthread_mutex_t (PTHREAD_MUTEX_DEFAULT)                                                 │
    │                                                                                         │
    │  std::mutex mtx;                                                                         │
    │  mtx.lock();   // 또는 std::lock_guard<std::mutex> lock(mtx);                            │
    │  // critical section                                                                    │
    │  mtx.unlock(); // 자동으로 호출됨 (lock_guard 사용 시)                                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [2. 재진입 가능 뮤텍스 (Recursive Mutex)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 소유자 스레드가 여러 번 Lock 가능                                                        │
    │  │  Lock 획득 횟수를 추적 (Lock Count)                                                       │
    │  │  같은 횟수만큼 Unlock 필요                                                             │
    │  │  재귀 함수(Recursive Function)에서 유용                                                 │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘
    │                                                                                         │
    │  C++: std::recursive_mutex                                                                │
    │  pthread_mutex_t (PTHREAD_MUTEX_RECURSIVE)                                                │
    │  Java: ReentrantLock                                                                     │
    │                                                                                         │
    │  std::recursive_mutex mtx;                                                               │
    │  void recursive_function(int n) {                                                        │
    │      std::lock_guard<std::recursive_mutex> lock(mtx);                                     │
    │      if (n <= 0) return;                                                                 │
    │      // do something                                                                     │
    │      recursive_function(n - 1);  // 재진입 가능                                          │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [3. 타임아웃 뮤텍스 (Timed Mutex)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Lock 획득 시도에 시간 제한 설정                                                          │
    │  │  지정된 시간 내에 Lock 실패 시 포기                                                       │
    │  │  Deadlock 방지에 유용                                                                │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘
    │                                                                                         │
    │  C++: std::timed_mutex                                                                   │
    │  pthread_mutex_timedlock (POSIX)                                                         │
    │                                                                                         │
    │  std::timed_mutex mtx;                                                                   │
    │  if (mtx.try_lock_for(std::chrono::milliseconds(100))) {                                  │
    │      // Lock 획득 성공 (100ms 내)                                                        │
    │      // critical section                                                                 │
    │      mtx.unlock();                                                                      │
    │  } else {                                                                                │
    │      // Lock 획득 실패 (100ms 경과)                                                       │
    │      // 다른 처리                                                                        │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [4. Try Lock (즉시 Lock 시도)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Lock 즉시 시도                                                                       │
    │  │  Lock 가능 → Lock 획득                                                               │
    │  │  Lock 불가 → 즉시 반환 (대기 안 함)                                                   │
    │  │  비차단(Non-blocking) 로직에 유용                                                    │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘
    │                                                                                         │
    │  C++: mtx.try_lock()                                                                     │
    │  pthread_mutex_trylock (POSIX)                                                           │
    │  Java: lock.tryLock()                                                                   │
    │                                                                                         │
    │  std::mutex mtx;                                                                         │
    │  if (mtx.try_lock()) {                                                                   │
    │      // Lock 획득 성공                                                                  │
    │      // critical section                                                                 │
    │      mtx.unlock();                                                                      │
    │  } else {                                                                                │
    │      // Lock 획득 실패 (다른 작업)                                                        │
    │      // 다른 처리                                                                        │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 뮤텍스 구현 비교

| 언어/플랫폼 | 기본 Mutex | 재진입 | 타임아웃 | Try Lock |
|-----------|----------|--------|---------|----------|
| **C++11** | std::mutex | std::recursive_mutex | std::timed_mutex | try_lock |
| **POSIX** | pthread_mutex_t | PTHREAD_MUTEX_RECURSIVE | pthread_mutex_timedlock | pthread_mutex_trylock |
| **Java** | synchronized | ReentrantLock | lock.tryLock(100, TimeUnit) | lock.tryLock() |
| **Python** | threading.Lock | threading.RLock | lock.acquire(timeout=1) | lock.acquire(False) |

### 과목 융합 관점 분석

#### 1. 운영체제 ↔ 뮤텍스
- **Kernel Mutex**: 커널 모드 동기화
- **Futex**: Userspace + Kernel 하이브리드 (Linux)
- **Priority Inheritance**: 우선순위 역전 방지

#### 2. 분산 시스템 ↔ 뮤텍스
- **Distributed Lock**: Redis, Zookeeper, etcd
- **Leader Election**: 락을 통한 리더 선출
- **Redlock Algorithm**: Redis 분산 락

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 다중 락 순서
**상황**: 여러 Lock 획득 시 Deadlock 위험
**판단**:
1. **문제**: Thread A: Lock A → Lock B, Thread B: Lock B → Lock A (Deadlock)
2. **해결**:
   - 항상 같은 순서로 Lock 획득
   - std::lock으로 여러 Lock 동시 획득

```cpp
// 안전한 다중 락
#include <mutex>
#include <thread>

std::mutex mutex_a;
std::mutex mutex_b;

void thread_a() {
    // 항상 같은 순서로 Lock 획득 (A → B)
    std::lock(mutex_a, mutex_b);
    std::lock_guard<std::mutex> lock_a(mutex_a, std::adopt_lock);
    std::lock_guard<std::mutex> lock_b(mutex_b, std::adopt_lock);
    // critical section
}

void thread_b() {
    // 동일한 순서로 Lock 획득 (A → B)
    std::lock(mutex_a, mutex_b);
    std::lock_guard<std::mutex> lock_a(mutex_a, std::adopt_lock);
    std::lock_guard<std::mutex> lock_b(mutex_b, std::adopt_lock);
    // critical section
}
```

---

## Ⅴ. 기대효과 및 결론

### 뮤텍스 사용 기대 효과

| 케이스 | Mutex 미사용 시 | Mutex 사용 시 |
|--------|---------------|--------------|
| **공유 변수 수정** | Race Condition | Thread-safe |
| **Database 연결** | 동시 접속 제어 | Connection Pool |
| **파일 쓰기** | 데이터 섞임 | 순차적 쓰기 |
| **Counter** | 부정확한 카운트 | 정확한 카운트 |

### 미래 전망

1. **Hardware Transactional Memory (HTM)**: 하드웨어 Lock
2. **Lock-free Algorithm**: CAS 기반
3. **Actor Model**: 메시지 전달 동시성

### ※ 참고 표준/가이드
- **POSIX 1003.1**: pthread_mutex
- **C++11**: std::mutex
- **Java**: Lock interface

---

## 📌 관련 개념 맵

- [스레드 안전성](./120_thread_safety.md) - 동기화 필요성
- [데드락](./121_deadlock.md) - Mutex 오용 문제
- [기아 현상](./122_starvation.md) - 불공정 Lock
- [세마포어](./124_semaphore.md) - 카운팅 Lock
