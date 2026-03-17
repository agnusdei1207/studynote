+++
title = "22. 세마포어 (Semaphore)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Semaphore", "Synchronization", "Mutual-Exclusion", "PV-Operation", "Counting-Semaphore"]
draft = false
+++

# 세마포어 (Semaphore)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 세마포어는 **"다중 프로세스/스레드 간 **공유 자원 접근을 **제어하는 정수형 동기화 도구"**로, **Dijkstra**(1965)가 제안한 **P(rolaagen: 감소/대기)**와 **V(erhogen: 증가/신호)** 연산으로 **동기화**를 구현한다.
> 2. **가치**: **이진 세마포어**(Binary Semaphore, 0/1)는 **Mutual Exclusion**(상호 배제)를 위한 **Lock**으로 사용되고 **카운팅 세마포어**(Counting Semaphore)는 **제한된 개수의 자원**(Connection Pool, Buffer)을 관리한다.
> 3. **융합**: **운영체제의 커널**에서 **Process Synchronization**, **Producer-Consumer**, **Reader-Writer** 문제를 해결하며 **Java Semaphore**, **POSIX sem_wait/sem_post**, **System V semop**으로 **응용 프로그래밍** 가능하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
세마포어는 **"공유 자원에 대한 접근을 제어하기 위한 추상 데이터 타입"**이다.

**세마포어의 구조**:
- **정수 변수**: 사용 가능한 자원 수
- **Wait(P) 연산**: 자원 획득 (감소 후 음수면 대기)
- **Signal(V) 연산**: 자원 반납 (증가 후 대기 프로세스 깨움)

### 💡 비유
세마포어는 **"주차장 티켓"**과 같다.
- **티켓 개수**: 자원 수
- **티켓 획득**: P 연산 (없으면 대기)
- **티켓 반납**: V 연산 (대기자에게 티켓)

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         세마포어의 필요성                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Race Condition:
    • 여러 프로세스가 공유 변수 접근
    • 결과 예측 불가능
         ↓
Lock:
    • 단일 자원 보호
    • 다중 자원 관리 어려움
         ↓
Semaphore (Dijkstra, 1965):
    • 정수형 카운터
    • N개 자원 관리
         ↓
현대 OS:
    • Mutex (이진 세마포어)
    • Counting Semaphore
    • Monitor, Condition Variable
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### P/V 연산 정의

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         P/V 연산 (Dijkstra)                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [P 연산 (Wait, Proberen: "to test")]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  void P(semaphore *S) {                                                                │
    │      S->value--;                // 자원 카운터 감소                                       │
    │      if (S->value < 0) {       // 자원이 없으면                                          │
    │          add_process(S->queue); // 대기 큐에 추가                                        │
    │          block();               // 프로세스 블록 (sleep)                                 │
    │      }                                                                                      │
    │  }                                                                                      │
    │                                                                                         │
    │  • 자원 획득 요청                                                                         │
    │  • 즉시 사용 가능하면 진행                                                                │
    │  • 없으면 대기 큐에서 Block                                                              │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [V 연산 (Signal, Verhogen: "to increment")]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  void V(semaphore *S) {                                                                │
    │      S->value++;               // 자원 카운터 증가                                       │
    │      if (S->value <= 0) {      // 대기 중인 프로세스 있으면                                │
    │          remove_process(S->queue); // 대기 큐에서 제거                                    │
    │          wakeup(P);             // 프로세스 깨움 (ready)                                 │
    │      }                                                                                      │
    │  }                                                                                      │
    │                                                                                         │
    │  • 자원 반납                                                                             │
    │  • 대기 중인 프로세스 있으면 깜                                                            │
    │  • 없으면 카운터만 증가                                                                  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Binary Semaphore vs Counting Semaphore

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         세마포어 종류                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Binary Semaphore (Mutex)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 값: 0 또는 1만 가능                                                                   │
    │  │  • 용도: 상호 배제 (Mutual Exclusion)                                                  │
    │  │  • Lock과 유사                                                                        │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Semaphore mutex = 1;  // 초기값 1 (잠금 해소 상태)                                    │  │
    │  │                                                                                      │  │
    │  │  P(&mutex);               // 잠금 획득 (0으로 변경)                                    │  │
    │  │  // Critical Section                                                               │  │
    │  │  V(&mutex);               // 잠금 반납 (1로 변경)                                      │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Counting Semaphore]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 값: 0 ~ N (자원 개수)                                                                │
    │  │  • 용도: 제한된 자원 관리                                                             │
    │  │  • 예: DB Connection Pool (5개), Buffer (10개)                                         │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Semaphore resources = 5;  // 5개 자원 가능                                          │  │
    │  │                                                                                      │  │
    │  │  // 자원 획득                                                                          │  │
    │  │  P(&resources);            // 카운터: 5→4→3...                                       │  │
    │  │  // Resource 사용                                                                    │  │
    │  │  V(&resources);            // 카운터: 0→1→2...                                       │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 세마포어 구현

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         세마포어 구현 (Spinlock vs Blocking)                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Spinlock Semaphore]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Busy Waiting (CPU 점유)                                                              │
    │  │  • 짧은 Critical Section에 적합                                                       │
    │  │                                                                                      │
    │  struct semaphore {                                                                     │
    │      int value;                                                                         │
    │      struct process *queue;                                                             │
    │  };                                                                                     │
    │                                                                                         │
    │  void P(semaphore *S) {                                                                │
    │      while (test_and_set(&S->value) == 0) {  // Atomic Test                             │
    │          // Spin (CPU 낭비)                                                              │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Blocking Semaphore]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Process Block (Context Switch)                                                       │
    │  │  • 긴 Critical Section에 적합                                                          │
    │  │                                                                                      │
    │  struct semaphore {                                                                     │
    │      int value;                                                                         │
    │      struct queue wait_queue;   // 대기 큐                                               │
    │  };                                                                                     │
    │                                                                                         │
    │  void P(semaphore *S) {                                                                │
    │      S->value--;                                                                        │
    │      if (S->value < 0) {                                                                │
    │          current->state = BLOCKED;                                                       │
    │          enqueue(&S->wait_queue, current);                                               │
    │          schedule();  // 다른 프로세스로 Context Switch                                  │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Semaphore vs Mutex vs Monitor

| 구분 | Semaphore | Mutex | Monitor |
|------|-----------|-------|---------|
| **값** | 정수 (0~N) | 이진 (0/1) | 객체 |
| **소유자** | 없음 | 있음 | Condition |
| **해제** | 누구나 | 소유자만 | Signal |
| **용도** | 자원 카운팅 | 상호 배제 | 복잡한 동기화 |

### Producer-Consumer 문제 해결

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Producer-Consumer (Bounded Buffer)                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Buffer: N개 슬롯                                                                     │
    │  • Semaphore: empty_items(N), full_items(0), mutex(1)                                   │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Producer                                                                          │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  while (true) {                                                                 │  │  │
    │  │  │      P(&empty_items);   // 빈 슬롯 있는지 확인 (없으면 대기)                        │  │  │
    │  │  │      P(&mutex);         // Buffer 잠금                                           │  │  │
    │  │  │      // Critical Section: Buffer에 데이터 삽입                                     │  │  │
    │  │  │      buffer[in] = item;                                                         │  │  │
    │  │  │      in = (in + 1) % N;                                                          │  │  │
    │  │  │      V(&mutex);         // Buffer 잠금 해제                                       │  │  │
    │  │  │      V(&full_items);    // 채워진 슬롯 증가 (Consumer 깨움)                        │  │  │
    │  │  │  }                                                                                │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │                                                                                       │  │
    │  │  Consumer                                                                            │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  while (true) {                                                                 │  │  │
    │  │  │      P(&full_items);    // 채워진 슬롯 있는지 확인 (없으면 대기)                      │  │  │
    │  │  │      P(&mutex);         // Buffer 잠금                                           │  │  │
    │  │  │      // Critical Section: Buffer에서 데이터 제거                                   │  │  │
    │  │  │      item = buffer[out];                                                         │  │  │
    │  │  │      out = (out + 1) % N;                                                         │  │  │
    │  │  │      V(&mutex);         // Buffer 잠금 해제                                       │  │  │
    │  │  │      V(&empty_items);   // 빈 슬롯 증가 (Producer 깨움)                           │  │  │
    │  │  │      // consume(item);                                                          │  │  │
    │  │  │  }                                                                                │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Connection Pool 구현
**상황**: DB Connection 5개 제한
**판단**:

```java
// Java Semaphore 예시
import java.util.concurrent.Semaphore;

public class ConnectionPool {
    private final Semaphore semaphore;
    private final Connection[] connections;

    public ConnectionPool(int poolSize) {
        this.semaphore = new Semaphore(poolSize);  // 카운팅 세마포어
        this.connections = new Connection[poolSize];
        // Initialize connections
    }

    public Connection getConnection() throws InterruptedException {
        semaphore.acquire();  // P 연산 (자원 획득)
        return getAvailableConnection();
    }

    public void releaseConnection(Connection conn) {
        releaseToPool(conn);
        semaphore.release();  // V 연산 (자원 반납)
    }
}

// 사용
ConnectionPool pool = new ConnectionPool(5);

Connection conn1 = pool.getConnection();  // 획득 (5→4)
Connection conn2 = pool.getConnection();  // 획득 (4→3)
Connection conn3 = pool.getConnection();  // 획득 (3→2)
// ...
pool.releaseConnection(conn1);  // 반납 (카운터 증가, 대기 중인 스레드 깨움)
```

---

## Ⅴ. 기대효과 및 결론

### 세마포어 기대 효과

| 효과 | 세마포어 없을 시 | 세마포어 있을 시 |
|------|-------------|---------------|
| **Race Condition** | 발생 | 방지 |
| **자원 관리** | 어려움 | 카운팅 가능 |
| **기아 현상** | - | 우선순위 부여로 해결 |

### 미래 전망

1. **Futex**: Linux Fast Userspace Mutex
2. **RW Lock**: Reader-Writer 최적화
3. **RCTLock**: Read-Copy-Update

### ※ 참고 표준/가이드
- **Dijkstra (1965)**: Semaphore 원론
- **POSIX**: sem_wait, sem_post
- **Java**: java.util.concurrent.Semaphore

---

## 📌 관련 개념 맵

- [동기화 개요](./93_synchronization_overview.md) - 기초
- [Mutex Lock](./98_mutex_lock.md) - 이진 세마포어
- [모니터](./99_monitor.md) - 고급 동기화
- [교착상태](./101_deadlock.md) - 문제점
