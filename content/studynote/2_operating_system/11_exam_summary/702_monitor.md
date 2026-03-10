+++
title = "702. 모니터 (Monitor) 동기화 추상화"
weight = 702
+++

# 233. 모니터 (Monitor)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 락과 조건 변수를 캡슐화한 고수준 동기화 구조
> 2. **가치**: 안전하고 사용하기 쉬운 동기화 추상화
> 3. **융합**: 뮤텍스, 조건 변수, 객체 지향과 연관

---

## Ⅰ. 개요

### 개념 정의

모니터(Monitor)는 **데이터와 그 데이터에 접근하는 메서드를 캡슐화하고, 동시 접근을 자동으로 제어하는 고수준 동기화 구조**다. 락과 조건 변수를 내부적으로 관리한다.

### 💡 비유: 은행 창구
모니터는 **은행 창구**와 같다. 한 번에 한 사람만 창구에서 업무를 본다. 대기실에서 대기하다가 번호가 불리면 들어간다.

### 모니터 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                모니터 구조                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【모니터 구성 요소】                                                  │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  ┌─────────────────────────────────────────────────────┐     │ │
│  │  │                    Monitor                           │     │ │
│  │  │  ┌───────────────────────────────────────────────┐ │     │ │
│  │  │  │              공유 데이터                       │ │     │ │
│  │  │  │           (variables, state)                   │ │     │ │
│  │  │  └───────────────────────────────────────────────┘ │     │ │
│  │  │                                                     │     │ │
│  │  │  ┌─────────────┐  ┌─────────────┐                  │     │ │
│  │  │  │ Method 1    │  │ Method 2    │  ...             │     │ │
│  │  │  │ (락 자동)    │  │ (락 자동)    │                  │     │ │
│  │  │  └─────────────┘  └─────────────┘                  │     │ │
│  │  │                                                     │     │ │
│  │  │  ┌─────────────┐  ┌─────────────┐                  │     │ │
│  │  │  │ Condition   │  │ Condition   │  ...             │     │ │
│  │  │  │ Variable 1  │  │ Variable 2  │                  │     │ │
│  │  │  └─────────────┘  └─────────────┘                  │     │ │
│  │  │                                                     │     │ │
│  │  │  진입 큐: [대기 중인 스레드들]                        │     │ │
│  │  │  조건 큐: [조건 대기 스레드들]                        │     │ │
│  │  │                                                     │     │ │
│  │  └─────────────────────────────────────────────────────┘     │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【모니터 규칙】                                                       │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 한 번에 하나의 스레드만 모니터 진입                           │ │
│  │  2. 모니터 메서드 진입 시 자동으로 락 획득                        │ │
│  │  3. 모니터 메서드 종료 시 자동으로 락 해제                        │ │
│  │  4. 조건 변수로 대기/깨우기 가능                                  │ │
│  │  5. wait() 시 락 해제 후 대기, 깨어날 때 락 재획득                │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                모니터 상세                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【생산자-소비자 모니터】                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  monitor ProducerConsumer {                                    │ │
│  │      int count = 0;                                            │ │
│  │      condition not_full, not_empty;                            │ │
│  │                                                             │ │
│  │      void put(item) {                                          │ │
│  │          if (count == N)                                       │ │
│  │              not_full.wait();                                  │ │
│  │          buffer.add(item);                                     │ │
│  │          count++;                                              │ │
│  │          not_empty.signal();                                   │ │
│  │      }                                                             │ │
│  │                                                             │ │
│  │      item get() {                                              │ │
│  │          if (count == 0)                                       │ │
│  │              not_empty.wait();                                 │ │
│  │          item = buffer.remove();                               │ │
│  │          count--;                                              │ │
│  │          not_full.signal();                                    │ │
│  │          return item;                                          │ │
│  │      }                                                             │ │
│  │  }                                                             │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【Signal vs Broadcast】                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  signal(): 하나의 대기 스레드만 깨움                              │ │
│  │  broadcast(): 모든 대기 스레드 깨움                              │ │
│  │                                                             │ │
│  │  Signal semantics:                                              │ │
│  │  • Mesa: 깨어난 스레드가 조건 재확인 필요 (실제 사용)             │ │
│  │  • Hoare: 깨어난 스레드가 즉시 실행, 시그널러 대기               │ │
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
│  【Java synchronized】                                                │
│  ──────────────────                                                  │
│  public class BoundedBuffer<T> {                                    │
│      private final Queue<T> queue = new LinkedList<>();             │
│      private final int capacity;                                    │
│                                                                     │
│      public BoundedBuffer(int capacity) {                           │
│          this.capacity = capacity;                                  │
│      }                                                              │
│                                                                     │
│      public synchronized void put(T item) throws InterruptedException {
│          while (queue.size() == capacity) {                         │
│              wait();  // not_full 조건 대기                          │
│          }                                                          │
│          queue.add(item);                                           │
│          notifyAll();  // not_empty 조건 신호                        │
│      }                                                              │
│                                                                     │
│      public synchronized T take() throws InterruptedException {     │
│          while (queue.isEmpty()) {                                  │
│              wait();  // not_empty 조건 대기                        │
│          }                                                          │
│          T item = queue.remove();                                   │
│          notifyAll();  // not_full 조건 신호                        │
│          return item;                                               │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【C++ std::condition_variable】                                      │
│  ──────────────────                                                  │
│  #include <mutex>                                                    │
│  #include <condition_variable>                                       │
│  #include <queue>                                                    │
│                                                                     │
│  template<typename T>                                               │
│  class BoundedBuffer {                                              │
│      std::mutex mtx;                                                │
│      std::condition_variable not_full, not_empty;                   │
│      std::queue<T> queue;                                           │
│      size_t capacity;                                               │
│  public:                                                            │
│      void put(T item) {                                             │
│          std::unique_lock<std::mutex> lock(mtx);                    │
│          not_full.wait(lock, [this]{ return queue.size() < capacity; });│
│          queue.push(item);                                          │
│          not_empty.notify_one();                                    │
│      }                                                              │
│      T take() {                                                     │
│          std::unique_lock<std::mutex> lock(mtx);                    │
│          not_empty.wait(lock, [this]{ return !queue.empty(); });    │
│          T item = queue.front();                                    │
│          queue.pop();                                               │
│          not_full.notify_one();                                     │
│          return item;                                               │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  【Python threading.Condition】                                       │
│  ──────────────────                                                  │
│  import threading                                                   │
│  from collections import deque                                      │
│                                                                     │
│  class BoundedBuffer:                                               │
│      def __init__(self, capacity):                                  │
│          self.buffer = deque()                                      │
│          self.capacity = capacity                                   │
│          self.condition = threading.Condition()                     │
│                                                                     │
│      def put(self, item):                                           │
│          with self.condition:                                       │
│              while len(self.buffer) >= self.capacity:               │
│                  self.condition.wait()                              │
│              self.buffer.append(item)                               │
│              self.condition.notify()                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 락과 조건 변수를 캡슐화한 동기화 구조
• 구성: 공유 데이터, 메서드, 조건 변수
• 규칙: 한 번에 하나의 스레드만 진입
• Signal: 하나의 스레드 깨움
• Broadcast: 모든 스레드 깨움
• 구현: Java synchronized, Python Condition
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [조건 변수](./234_condition_variable.md) → 구성 요소
- [뮤텍스](./232_mutex.md) → 내부 구현
- [생산자-소비자](./237_producer_consumer.md) → 대표 패턴
- [동기화 개요](./221_synchronization_overview.md) → 상위 개념

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 모니터는 "은행 창구" 같아요!

**원리**: 한 사람씩 업무 봐요!

**효과**: 순서대로 처리해요!
