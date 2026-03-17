+++
title = "48. 동기화 기법 (Synchronization Primitives)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Synchronization", "Mutex", "RWLock", "Condition-Variable", "Barrier"]
draft = false
+++

# 동기화 기법 (Synchronization Primitives)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 동기화 기법은 **"여러 **스레드**가 **공유 **자원**에 **접근**할 때 **데이터 **경쟁**(Race Condition)**을 **방지**하는 **메커니즘\"**으로, **Mutex**(상호 **배제), **RWLock**(읽기-쓰기 **락)**, **Condition Variable**(대기/통지), **Semaphore**(카운팅 **신호)**가 **대표적**이다.
> 2. **구현**: **Atomic**(원자적 **연산)**으로 **락**을 **구현**하고 **Futex**(Fast Userspace **Mutex), **Spinlock**(Busy **waiting)**, ** adaptive **Mutex**(CPU **절전)**로 **성능**을 **최적화**한다.
> 3. **패턴**: **Critical Section**(임계 **영역)**을 **최소화**하고 **Lock Hierarchy**(락 **순서)**를 **준수**하며 **Deadlock**(교착 **상태)**을 **방지**하기 **위해 **try_lock, **timeout**을 **사용**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
동기화는 **"스레드 간 조율"**이다.

**동기화 기법 비교**:
| 기법 | 용도 | 단위 | 복잡도 |
|------|------|------|--------|
| **Mutex** | 상호 배제 | 1 | 낮음 |
| **RWLock** | 읽기/쓰기 | N+1 | 중간 |
| **Semaphore** | 카운팅 | N | 중간 |
| **Barrier** | 집합 지점 | N | 높음 |

### 💡 비유
동기화는 ****화장실 **칸 ****과 같다.
- **락**: 문 잠금
- **대기**: 줄 서기
- **신호**: 사용 완료

---

## Ⅱ. 아키텍처 및 핵심 원리

### Mutex (Mutual Exclusion)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Mutex Lock Operation                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Basic Usage:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;                                     │  │
    │  int shared_counter = 0;                                                                │  │
    │                                                                                         │  │
    │  void* thread_func(void* arg) {                                                         │  │
    │      for (int i = 0; i < 1000000; i++) {                                                │  │
    │          pthread_mutex_lock(&lock);     // Enter critical section                       │  │
    │          shared_counter++;                // Only one thread executes                    │  │
    │          pthread_mutex_unlock(&lock);   // Exit critical section                        │  │
    │      }                                                                                    │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Mutex Implementation (Simplified):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  struct mutex {                                                                          │  │
    │      atomic_int state;  // 0=unlocked, 1=locked                                          │  │
    │      queue wait_queue;  // Waiting threads                                               │  │
    │  };                                                                                      │  │
    │                                                                                         │  │
    │  void mutex_lock(mutex_t* m) {                                                           │  │
    │      while (atomic_exchange(&m->state, 1) == 1) {  // CAS (Compare-And-Swap)             │  │
    │          // Already locked, wait                                                         │  │
    │          enqueue(&m->wait_queue, current_thread);                                        │  │
    │          block_current_thread();                                                         │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  void mutex_unlock(mutex_t* m) {                                                         │  │
    │      atomic_store(&m->state, 0);                                                         │  │
    │      if (!empty(&m->wait_queue)) {                                                       │  │
    │          thread* next = dequeue(&m->wait_queue);                                         │  │
    │          wake_thread(next);                                                              │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### RWLock (Read-Write Lock)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Read-Write Lock                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Use Case: Multiple readers, single writer
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;                                  │  │
    │  char shared_buffer[1024];                                                               │  │
    │                                                                                         │  │
    │  // Reader (can run concurrently with other readers)                                     │  │
    │  void* reader(void* arg) {                                                               │  │
    │      pthread_rwlock_rdlock(&rwlock);    // Multiple readers allowed                     │  │
    │      printf("Read: %s\n", shared_buffer);                                                │  │
    │      pthread_rwlock_unlock(&rwlock);                                                     │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  // Writer (exclusive access)                                                            │  │
    │  void* writer(void* arg) {                                                               │  │
    │      pthread_rwlock_wrlock(&rwlock);    // Blocks all readers and writers                │  │
    │      strcpy(shared_buffer, "New data");                                                  │  │
    │      pthread_rwlock_unlock(&rwlock);                                                     │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    RWLock Implementation:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  struct rwlock {                                                                         │  │
    │      atomic_int readers;  // -1=writer held, 0=unlocked, >0=reader count                 │  │
    │      queue write_waiters;                                                                │  │
    │  };                                                                                      │  │
    │                                                                                         │  │
    │  void rdlock(rwlock_t* rw) {                                                             │  │
    │      while (1) {                                                                          │  │
    │          int r = atomic_load(&rw->readers);                                              │  │
    │          if (r >= 0 && atomic_compare_exchange_weak(&rw->readers, &r, r + 1))           │  │
    │              break;  // Acquired read lock                                               │  │
    │          if (r == -1) {                                                                  │  │
    │              // Writer active, wait                                                      │  │
    │              enqueue(&rw->write_waiters, current_thread);                                 │  │
    │              block_current_thread();                                                      │  │
    │          }                                                                                │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  void wrlock(rwlock_t* rw) {                                                             │  │
    │      // Atomically transition from 0 to -1                                               │  │
    │      while (!atomic_compare_exchange_weak(&rw->readers, &(int){0}, -1)) {                │  │
    │          enqueue(&rw->write_waiters, current_thread);                                     │  │
    │          block_current_thread();                                                          │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Condition Variable

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Condition Variable Pattern                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Use Case: Wait for condition to become true
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;                                     │  │
    │  pthread_cond_t cond = PTHREAD_COND_INITIALIZER;                                         │  │
    │  int work_available = 0;                                                                 │  │
    │                                                                                         │  │
    │  // Consumer thread                                                                      │  │
    │  void* consumer(void* arg) {                                                             │  │
    │      pthread_mutex_lock(&mutex);                                                         │  │
    │      while (!work_available) {               // Always loop (spurious wakeup)             │  │
    │          pthread_cond_wait(&cond, &mutex);   // Releases lock, waits for signal           │  │
    │      }                                                                                    │  │
    │      work_available = 0;                                                                 │  │
    │      consume_work();                                                                     │  │
    │      pthread_mutex_unlock(&mutex);                                                       │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  // Producer thread                                                                      │  │
    │  void* producer(void* arg) {                                                             │  │
    │      pthread_mutex_lock(&mutex);                                                         │  │
    │      produce_work();                                                                     │  │
    │      work_available = 1;                                                                 │  │
    │      pthread_cond_signal(&cond);          // Wake one waiting thread                      │  │
    │      pthread_mutex_unlock(&mutex);                                                       │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Why always loop?
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  pthread_mutex_lock(&mutex);                                                             │  │
    │  while (!condition) {                       // NOT if (!condition)                        │  │
    │      pthread_cond_wait(&cond, &mutex);                                                   │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  Reasons for spurious wakeup:                                                            │  │
    │  1. Implementation detail (futex is signal-based)                                        │  │
    │  2. Multiple threads signaled, only one gets condition                                  │  │
    │  3. Signal happened before wait                                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 동기화 기법 비교

| 기법 | 스레드 | 공유 | 읽기 | 쓰기 |
|------|--------|------|------|------|
| **Mutex** | 1 | 전용 | X | X |
| **RWLock** | N+1 | 전용 | O | X |
| **Semaphore** | N | 카운트 | O | O |
| **Barrier** | N | 집합 | - | - |

### Semaphore

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Semaphore (Counting)                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Binary Semaphore (Mutex-like):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  sem_t sem;                                                                              │  │
    │  sem_init(&sem, 0, 1);         // Initial value = 1 (binary)                            │  │
    │                                                                                         │  │
    │  sem_wait(&sem);               // P operation (decrement, wait if < 0)                   │  │
    │  critical_section();                                                                    │  │
    │  sem_post(&sem);               // V operation (increment, wake if <= 0)                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Counting Semaphore (Resource management):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  sem_t db_connections;                                                                   │  │
    │  sem_init(&db_connections, 0, 10);   // Max 10 connections                               │  │
    │                                                                                         │  │
    │  void* worker(void* arg) {                                                               │  │
    │      sem_wait(&db_connections);      // Acquire connection                              │  │
    │      if (sem_trywait(&db_connections) == 0) {  // Non-blocking attempt                  │  │
    │          do_database_work();                                                             │  │
    │          sem_post(&db_connections);   // Release connection                             │  │
    │      } else {                                                                              │  │
    │          handle_unavailable();                                                            │  │
    │      }                                                                                    │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → Max 10 threads can access DB simultaneously                                          │  │
    │  → Other threads block until a connection is released                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Barrier (Thread Synchronization)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Barrier (Rendezvous Point)                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Use Case: Parallel computation phases
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  pthread_barrier_t barrier;                                                             │  │
    │  pthread_barrier_init(&barrier, NULL, 4);  // 4 threads must arrive                     │  │
    │                                                                                         │  │
    │  void* worker(void* arg) {                                                               │  │
    │      int id = *(int*)arg;                                                                │  │
    │                                                                                         │  │
    │      // Phase 1: Compute partial result                                                  │  │
    │      partial_result = compute_phase1(id);                                                │  │
    │      pthread_barrier_wait(&barrier);  // Wait for all 4 threads                         │  │
    │                                                                                         │  │
    │      // Phase 2: Combine results (only thread 0, but all waited)                        │  │
    │      if (id == 0) {                                                                       │  │
    │          final_result = combine(partial_results);                                        │  │
    │      }                                                                                    │  │
    │      pthread_barrier_wait(&barrier);  // Wait for combine to finish                      │  │
    │                                                                                         │  │
    │      // Phase 3: Use final result                                                        │  │
    │      use_result(final_result);                                                           │  │
    │      return NULL;                                                                         │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → Ensures all threads complete phase 1 before any starts phase 2                        │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 생산자-소비자 큐
**상황**: 멀티스레드 큐
**판단**: Mutex + Condition Variable

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Thread-Safe Queue                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  typedef struct {                                                                       │  │
    │      int buffer[100];                                                                   │  │
    │      int head;                           // Read index                                   │  │
    │      int tail;                           // Write index                                  │  │
    │      int count;                          // Items in queue                                │  │
    │      pthread_mutex_t mutex;                                                              │  │
    │      pthread_cond_t not_empty;    // Wait for items                                   │  │
    │      pthread_cond_t not_full;     // Wait for space                                   │  │
    │  } Queue;                                                                                 │  │
    │                                                                                         │  │
    │  void enqueue(Queue* q, int item) {                                                      │  │
    │      pthread_mutex_lock(&q->mutex);                                                      │  │
    │      while (q->count == 100) {               // Queue full                              │  │
    │          pthread_cond_wait(&q->not_full, &q->mutex);                                    │  │
    │      }                                                                                    │  │
    │                                                                                         │  │
    │      q->buffer[q->tail] = item;                                                          │  │
    │      q->tail = (q->tail + 1) % 100;                                                      │  │
    │      q->count++;                                                                          │  │
    │                                                                                         │  │
    │      pthread_cond_signal(&q->not_empty);   // Wake one consumer                         │  │
    │      pthread_mutex_unlock(&q->mutex);                                                    │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  int dequeue(Queue* q) {                                                                  │  │
    │      pthread_mutex_lock(&q->mutex);                                                      │  │
    │      while (q->count == 0) {                 // Queue empty                              │  │
    │          pthread_cond_wait(&q->not_empty, &q->mutex);                                   │  │
    │      }                                                                                    │  │
    │                                                                                         │  │
    │      int item = q->buffer[q->head];                                                      │  │
    │      q->head = (q->head + 1) % 100;                                                      │  │
    │      q->count--;                                                                          │  │
    │                                                                                         │  │
    │      pthread_cond_signal(&q->not_full);    // Wake one producer                         │  │
    │      pthread_mutex_unlock(&q->mutex);                                                    │  │
    │      return item;                                                                         │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 동기화 기법 기대 효과

| 기법 | 스케일링 | 오버헤드 | 사용처 |
|------|---------|----------|--------|
| **Mutex** | 낮음 | 낮음 | 범용 |
| **RWLock** | 중간 | 중간 | 읽기 많음 |
| **Semaphore** | 중간 | 중간 | 자원 관리 |
| **Barrier** | 높음 | 높음 | 병렬 연산 |

### 모범 사례

1. **임계영역**: 최소화
2. **락 순서**: 일관성
3. **타임아웃**: try_lock
4. **RAII**: 자동 해제

### 미래 전망

1. **Lock-free**: CAS, RCU
2. **Transactional**: TM
3. **Actor**: 메시지 기반
4. **Coroutine**: 비선점형

### ※ 참고 표준/가이드
- **POSIX**: pthreads
- **C++**: std::mutex
- **Java**: java.util.concurrent

---

## 📌 관련 개념 맵

- [스레드 안전성](./2_process_thread/106_thread_safety.md) - Race Condition
- [데드락 예방](./6_deadlock/111_deadlock_prevention.md) - 교착 상태
- [프로세스 vs 스레드](./2_process_thread/107_process_vs_thread.md) - 공유

