+++
title = "31. 뮤텍스 (Mutex)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Mutex", "Lock", "Synchronization", "Mutual-Exclusion", "Race-Condition"]
draft = false
+++

# 뮤텍스 (Mutex)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 뮤텍스는 **"상호 배제**(Mutual Exclusion)를 **제공**하는 **동기화 도구"**로, **하나의 스레드**만 **Critical Section**(임계 영역)에 **진입**할 수 있게 **하고** **잠금**(Lock)과 **해제**(Unlock)로 **작동**하며 **Binary Semaphore**(값이 0 또는 1)로 **구현**된다.
> 2. **동기화 원칙**: **pthread_mutex_lock**으로 **진입**하고 **pthread_mutex_unlock**으로 **탈출**하며 **이미 잠긴 Mutex**를 **다시 Lock**하면 **Blocking**(대기)하고 **Deadlock**을 **방지**하기 위해 **소유자**(Owner)가 **반드시 해제**해야 한다.
> 3. **융합**: **POSIX pthread**(pthread_mutex_t), **Windows CRITICAL_SECTION**, **C++ std::mutex**, **Java synchronized**, **Python threading.Lock**가 **언어별** **구현**을 **제공**하며 **Recursive Mutex**, **Timed Mutex**, **Spinlock**으로 **확장**된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
뮤텍스는 **"한 번에 하나의 스레드만 허용하는 잠금 장치"**이다.

**뮤텍스 특징**:
- **상호 배제**: 동시 접근 차단
- **Blocking**: 잠겨 있으면 대기
- **소유권**: Lock을 가진 스레드만 해제
- **Binary**: 0(잠김) 또는 1(열림)

### 💡 비유
뮤텍스는 **"화장실 열쇠****와 같다.
- **화장실**: 임계 영역
- **열쇠**: Mutex
- **사용 중**: Lock
- **비움**: Unlock

---

## Ⅱ. 아키텍처 및 핵심 원리

### POSIX Mutex API

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         POSIX Mutex API                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. 초기화 (Initialization)                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  #include <pthread.h>                                                               │  │  │
    │  │                                                                                    │  │  │
    │  │  pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;  // 정적 초기화                   │  │  │
    │  │                                                                                    │  │  │
    │  │  // 또는 동적 초기화                                                                 │  │  │
    │  │  pthread_mutex_t mutex;                                                             │  │  │
    │  │  pthread_mutex_init(&mutex, NULL);                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  2. 사용 (Lock/Unlock)                                                                 │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  void* thread_func(void* arg) {                                                      │  │  │
    │  │      pthread_mutex_lock(&mutex);                                 │  │  │
    │  │      // Critical Section                                                              │  │  │
    │  │      pthread_mutex_unlock(&mutex);                               │  │  │
    │  │      return NULL;                                                                      │  │  │
    │  │  }                                                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Mutex vs Semaphore

| 구분 | Mutex | Semaphore |
|------|-------|-----------|
| **값** | 0 또는 1 | 0 이상의 정수 |
| **소유권** | 있음 | 없음 |
| **용도** | 상호 배제 | 리소스 카운팅 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 뱅킹 계좌
**상황**: 잔액 업데이트
**판단**: Mutex로 동시성 제어

```c
#include <pthread.h>

typedef struct {
    int balance;
    pthread_mutex_t lock;
} BankAccount;

void deposit(BankAccount *account, int amount) {
    pthread_mutex_lock(&account->lock);
    account->balance += amount;
    pthread_mutex_unlock(&account->lock);
}
```

---

## Ⅴ. 기대효과 및 결론

### Mutex 기대 효과

| 효과 | 없음 | Mutex |
|------|------|-------|
| **Race Condition** | 발생 | 방지 |
| **데이터 일관성** | 깨짐 | 유지 |

### 미래 전망

1. **Lock-free**: CAS, Atomic
2. **Actor Model**: 메시지 전달

### ※ 참고 표준/가이드
- **POSIX**: pthread_mutex
- **C++**: std::mutex
- **Java**: synchronized

---

## 📌 관련 개념 맵

- [세마포어](./102_semaphore.md) - 카운팅 Lock
- [모니터](./103_monitor.md) - 고급 동기화
- [데드락](./105_deadlock.md) - 교착 상태
