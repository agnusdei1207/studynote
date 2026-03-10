+++
title = "273. 세큐어 코딩에서의 동기화 약점 (TOCTOU: Time of Check to Time of Use)"
weight = 273
+++

# 273. 락 큐 (Lock Queue)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 락 대기 스레드를 관리하는 큐 자료구조
> 2. **가치**: 공정성 보장, 스레드 관리
> 3. **융합**: 락 웨이터, 스케줄링, FIFO와 연관

---

## Ⅰ. 개요

### 개념 정의

락 큐(Lock Queue)는 **락 획득을 대기하는 스레드들을 순서대로 관리하는 큐 자료구조**다. 공정성, 스레드 관리, 교착상태 분석에 사용된다.

### 💡 비유: 은행 대기번호
락 큐는 **은행 대기번호**와 같다. 번호표를 받고 순서를 기다린다. 먼저 온 사람이 먼저 서비스받는다.

### 락 큐 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                락 큐 구조                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 구조】                                                         │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  struct lock_queue {                                              │ │
│  │      struct list_head head;  // 큐 헤드                            │ │
│  │      spinlock_t lock;        // 큐 보호 락                          │ │
│  │      int count;              // 웨이터 수                           │ │
│  │  };                                                              │ │
│  │                                                             │ │
│  │  struct waiter {                                                   │ │
│  │      struct list_head list;  // 연결 리스트                        │ │
│  │      struct task_struct *task;  // 대기 스레드                      │ │
│  │      int flags;                                                    │ │
│  │  };                                                              │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【동작】                                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  enqueue (락 획득 실패 시):                                          │ │
│  │  1. waiter 구조체 생성                                              │ │
│  │  2. waiter.task = current                                          │ │
│  │  3. list_add_tail(&waiter.list, &queue.head)                      │ │
│  │  4. schedule()  // 대기                                             │ │
│  │                                                             │ │
│  │  dequeue (락 해제 시):                                               │ │
│  │  1. waiter = list_first_entry(&queue.head)                        │ │
│  │  2. list_del(&waiter.list)                                        │ │
│  │  3. wake_up_process(waiter.task)                                  │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【큐 시각화】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  head ──► [waiter1] ──► [waiter2] ──► [waiter3] ──► null         │ │
│  │             T2          T3          T4                           │ │
│  │              ↑                                             │ │
│  │          dequeue 대상                                        │ │
│  │                                                             │ │
│  │  enqueue: list_add_tail()  // 끝에 추가                             │ │
│  │  dequeue: list_first_entry()  // 앞에서 제거                         │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                락 큐 상세                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【큐 정책】                                                            │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. FIFO (First-In-First-Out):                                    │ │
│  │     • 공정성 보장                                                   │ │
│  │     • 일반적인 락 큐                                                │ │
│  │                                                             │ │
│  │  2. 우선순위 큐:                                                    │ │
│  │     • 높은 우선순위 먼저                                              │ │
│  │     • 실시간 시스템                                                 │ │
│  │     • rt_mutex                                                      │ │
│  │                                                             │ │
│  │  3. LIFO (Last-In-First-Out):                                      │ │
│  │     • 처리량 향상                                                    │ │
│  │     • 불공정                                                        │ │
│  │     • 스핀락                                                         │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【구현별 큐】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  Linux mutex:                                                      │ │
│  │  • wait_list: 연결 리스트                                           │ │
│  │  • FIFO                                                            │ │
│  │  • optimistic spinning                                             │ │
│  │                                                             │ │
│  │  Linux rt_mutex:                                                    │ │
│  │  • waiters: 레드블랙트리 (우선순위)                                   │ │
│  │  • 우선순위 상속                                                     │ │
│  │                                                             │ │
│  │  MCS 락:                                                            │ │
│  │  • 연결 리스트                                                       │ │
│  │  • 각 노드에서 스핀                                                   │ │
│  │                                                             │ │
│  │  Java AQS:                                                          │ │
│  │  • CLH 변형 큐                                                      │ │
│  │  • FIFO                                                            │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【장단점】                                                             │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  장점:                                                              │ │
│  │  • 공정성 보장                                                       │ │
│  │  • 기아 방지                                                        │ │
│  │  • 스레드 관리 용이                                                   │ │
│  │  • 교착상태 분석 가능                                                 │ │
│  │                                                             │ │
│  │  단점:                                                               │ │
│  │  • 오버헤드                                                          │ │
│  │  • 메모리 사용                                                       │ │
│  │  • 큐 관리 락 필요                                                   │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Linux 커널 mutex 큐】                                               │
│  ──────────────────                                                  │
│  // kernel/locking/mutex.c                                          │
│  struct mutex {                                                      │
│      atomic_long_t owner;                                            │
│      spinlock_t wait_lock;                                           │
│      struct list_head wait_list;  // 락 큐                           │
│  };                                                                  │
│                                                                     │
│  // enqueue                                                          │
│  static void __sched __mutex_lock_slowpath(struct mutex *lock)      │
│  {                                                                   │
│      struct mutex_waiter waiter;                                     │
│      waiter.task = current;                                          │
│      list_add_tail(&waiter.list, &lock->wait_list);                 │
│      set_current_state(TASK_UNINTERRUPTIBLE);                       │
│      schedule();                                                     │
│  }                                                                   │
│                                                                     │
│  // dequeue                                                          │
│  static void __mutex_unlock_slowpath(struct mutex *lock)            │
│  {                                                                   │
│      struct mutex_waiter *waiter;                                    │
│      waiter = list_first_entry(&lock->wait_list,                    │
│                                 struct mutex_waiter, list);         │
│      list_del(&waiter->list);                                        │
│      wake_up_process(waiter->task);                                  │
│  }                                                                   │
│                                                                     │
│  【C++ 조건 변수 + 큐】                                                 │
│  ──────────────────                                                  │
│  #include <mutex>                                                    │
│  #include <condition_variable>                                       │
│  #include <queue>                                                    │
│                                                                     │
│  class LockQueue {                                                   │
│      std::queue<std::thread::id> waiters;                           │
│      std::mutex mtx;                                                 │
│      std::condition_variable cv;                                     │
│      bool locked = false;                                            │
│                                                                     │
│  public:                                                            │
│      void lock() {                                                  │
│          std::unique_lock<std::mutex> lk(mtx);                      │
│          waiters.push(std::this_thread::get_id());                  │
│          cv.wait(lk, [this] {                                       │
│              return !locked &&                                       │
│                  waiters.front() == std::this_thread::get_id();     │
│          });                                                         │
│          waiters.pop();                                              │
│          locked = true;                                              │
│      }                                                              │
│                                                                     │
│      void unlock() {                                                │
│          std::lock_guard<std::mutex> lk(mtx);                        │
│          locked = false;                                             │
│          cv.notify_all();                                            │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  【Java AbstractQueuedSynchronizer (AQS)】                            │
│  ──────────────────                                                  │
│  // CLH 큐 변형                                                       │
│  // java.util.concurrent.locks.AbstractQueuedSynchronizer           │
│                                                                     │
│  // 웨이터 노드                                                        │
│  static final class Node {                                          │
│      volatile Node prev;                                             │
│      volatile Node next;                                             │
│      volatile Thread thread;                                         │
│      volatile int waitStatus;                                        │
│  }                                                                   │
│                                                                     │
│  // 큐에 추가                                                         │
│  private Node enq(final Node node) {                                │
│      for (;;) {                                                      │
│          Node t = tail;                                              │
│          node.prev = t;                                              │
│          if (compareAndSetTail(t, node)) {                           │
│              t.next = node;                                          │
│              return t;                                               │
│          }                                                          │
│      }                                                              │
│  }                                                                   │
│                                                                     │
│  【Go runtime 큐】                                                     │
│  ──────────────────                                                  │
│  // runtime/sema.go                                                  │
│  // 세마포어 대기 큐                                                   │
│  type sudog struct {                                                 │
│      g       *g                                                      │
│      next    *sudog                                                  │
│      prev    *sudog                                                  │
│      // ...                                                           │
│  }                                                                   │
│                                                                     │
│  【성능 비교】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  큐 타입          enqueue     dequeue     공정성                 │ │
│  │  ────────          ──────        ──────        ────                │ │
│  │  연결 리스트        O(1)         O(1)         FIFO               │ │
│  │  레드블랙트리        O(log n)      O(log n)      우선순위           │ │
│  │  스핀락 (큐 없음)    -           -           불공정               │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【언제 사용할까?】                                                      │
│  ──────────────────                                                  │
│  • 공정성 필요 시: FIFO 큐                                            │
│  • 실시간 시스템: 우선순위 큐                                          │
│  • 높은 처리량: 스핀락 또는 불공정                                       │
│  • 교착상태 방지: 타임아웃 + 큐                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 락 대기 스레드 관리 큐
• 정책: FIFO, 우선순위, LIFO
• 구현: 연결 리스트, 레드블랙트리
• 장점: 공정성, 기아 방지
• 단점: 오버헤드, 메모리
• 활용: mutex, AQS, rt_mutex
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [락 웨이터](./272_lock_waiter.md) → 큐의 원소
- [공정성](./274_fairness.md) → 큐 정책
- [MCS 락](./269_mcs_lock.md) → 큐 기반 락
- [조건 변수](./234_condition_variable.md) → 큐 활용

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 락 큐는 "은행 대기번호" 같아요!

**원리**: 번호표 받고 순서를 기다려요!

**효과**: 공정하게 차례가 와요!
