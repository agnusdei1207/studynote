+++
title = "242. 우선순위 역전 (Priority Inversion) - 하위 프로세스가 락을 쥐고 있어 상위 프로세스 대기"
weight = 242
+++

# 242. Double-Checked Locking (이중 확인 잠금)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 락 획득 전후로 조건을 두 번 확인
> 2. **가치**: 불필요한 락 획득 회피, 성능 최적화
> 3. **융합**: 싱글톤, 지연 초기화, 메모리 모델과 연관

---

## Ⅰ. 개요

### 개념 정의

Double-Checked Locking(DCL)은 **락 획득 전에 조건을 먼저 확인하고, 락 획득 후에 다시 확인하여 불필요한 락 획득을 줄이는 최적화 패턴**이다. 주로 싱글톤과 지연 초기화에 사용된다.

### 💡 비유: 입장권 확인
Double-Checked Locking은 **입장권 확인**과 같다. 입구에서 대충 보고, 안에서 다시 꼼꼼히 확인한다. 굳이 안 들어가도 될 사람은 입구에서 보낸다.

### Double-Checked Locking 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                Double-Checked Locking 구조                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 패턴】                                                         │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  // 첫 번째 확인 (락 없이)                                        │ │
│  │  if (instance == null) {                    // Check 1        │ │
│  │      lock();                                                 │ │
│  │      {                                                       │ │
│  │          // 두 번째 확인 (락 내부)                                │ │
│  │          if (instance == null) {            // Check 2        │ │
│  │              instance = new Singleton();                      │ │
│  │          }                                                      │ │
│  │      }                                                           │ │
│  │      unlock();                                               │ │
│  │  }                                                               │ │
│  │  return instance;                                             │ │
│  │                                                             │ │
│  │  효과:                                                             │ │
│  │  • 첫 생성 후에는 락 획득 없이 빠르게 반환                          │ │
│  │  • 생성 시에만 락 획득                                            │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【vs 단일 확인】                                                       │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  단일 확인 (매번 락):                                             │ │
│  │  lock();                                                         │ │
│  │  if (instance == null) {                                        │ │
│  │      instance = new Singleton();                                │ │
│  │  }                                                               │
│  │  unlock();                                                       │
│  │  // 매 호출마다 락 → 비효율                                        │ │
│  │                                                             │ │
│  │  Double-Checked:                                                 │ │
│  │  // 첫 생성 후에는 락 없이 반환 → 효율                              │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【안전하지 않은 DCL (Java 예전)】                                       │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  // 잘못된 구현                                                   │ │
│  │  if (instance == null) {                    // Check 1        │ │
│  │      synchronized(this) {                                     │ │
│  │          if (instance == null) {            // Check 2        │ │
│  │              instance = new Singleton();  // 문제!               │ │
│  │              // 1. 메모리 할당                                    │ │
│  │              // 2. 생성자 호출                                    │ │
│  │              // 3. instance에 할당                                │ │
│  │              // 2-3 재배치 가능!                                  │ │
│  │          }                                                      │
│  │      }                                                           │ │
│  │  }                                                               │
│  │  return instance;  // 미완성 객체 반환 가능                       │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                Double-Checked Locking 상세                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【안전한 구현 방법】                                                   │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. volatile 사용 (Java)                                         │ │
│  │     private volatile static Singleton instance;                  │ │
│  │     // volatile: happens-before 보장                             │ │
│  │                                                             │ │
│  │  2. atomic + memory_order (C++)                                  │ │
│  │     std::atomic<Singleton*> instance;                            │ │
│  │     instance.store(p, std::memory_order_release);                │ │
│  │     instance.load(std::memory_order_acquire);                    │ │
│  │                                                             │ │
│  │  3. 정적 초기화 (가장 안전)                                        │ │
│  │     static Singleton& getInstance() {                            │ │
│  │         static Singleton instance;  // C++11 스레드 안전          │ │
│  │         return instance;                                          │ │
│  │     }                                                             │ │
│  │                                                             │ │
│  │  4. std::call_once (C++11)                                       │ │
│  │     static std::once_flag flag;                                   │ │
│  │     static Singleton* instance;                                   │ │
│  │     std::call_once(flag, []{ instance = new Singleton(); });     │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【재배치 문제】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  instance = new Singleton();                                     │ │
│  │                                                             │ │
│  │  정상 순서:                                                        │ │
│  │  1. 메모리 할당                                                   │ │
│  │  2. 생성자 호출 (필드 초기화)                                      │ │
│  │  3. instance 변수에 참조 할당                                      │ │
│  │                                                             │ │
│  │  재배치 가능 (1-3-2):                                              │ │
│  │  1. 메모리 할당                                                   │ │
│  │  3. instance 변수에 참조 할당 (null 아님)                          │ │
│  │  // 여기서 다른 스레드이 instance 사용 → 미완성 객체!               │ │
│  │  2. 생성자 호출                                                   │ │
│  │                                                             │ │
│  │  해결: memory_order_release/acquire 또는 volatile                 │ │
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
│  【C++11 안전한 DCL】                                                  │
│  ──────────────────                                                  │
│  class Singleton {                                                  │
│      static std::atomic<Singleton*> instance;                       │
│      static std::mutex mtx;                                         │
│  public:                                                            │
│      static Singleton* getInstance() {                              │
│          Singleton* tmp = instance.load(std::memory_order_acquire);│
│          if (tmp == nullptr) {                                      │
│              std::lock_guard<std::mutex> lock(mtx);                 │
│              tmp = instance.load(std::memory_order_relaxed);        │
│              if (tmp == nullptr) {                                  │
│                  tmp = new Singleton();                             │
│                  instance.store(tmp, std::memory_order_release);    │
│              }                                                      │
│          }                                                          │
│          return tmp;                                                │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  【C++11 정적 지역 변수 (권장)】                                         │
│  ──────────────────                                                  │
│  class Singleton {                                                  │
│  public:                                                            │
│      static Singleton& getInstance() {                              │
│          static Singleton instance;  // C++11: 스레드 안전           │
│          return instance;                                           │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  【C++11 std::call_once】                                              │
│  ──────────────────                                                  │
│  #include <mutex>                                                    │
│  class Singleton {                                                  │
│      static std::once_flag flag;                                    │
│      static Singleton* instance;                                    │
│  public:                                                            │
│      static Singleton* getInstance() {                              │
│          std::call_once(flag, []{                                  │
│              instance = new Singleton();                            │
│          });                                                        │
│          return instance;                                           │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  【Java 안전한 DCL (volatile)】                                         │
│  ──────────────────                                                  │
│  public class Singleton {                                           │
│      private volatile static Singleton instance;                    │
│      public static Singleton getInstance() {                        │
│          if (instance == null) {                                    │
│              synchronized (Singleton.class) {                       │
│                  if (instance == null) {                            │
│                      instance = new Singleton();                    │
│                  }                                                  │
│              }                                                      │
│          }                                                          │
│          return instance;                                           │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【Java Initialization-on-demand Holder (권장)】                        │
│  ──────────────────                                                  │
│  public class Singleton {                                           │
│      private static class Holder {                                  │
│          static final Singleton INSTANCE = new Singleton();          │
│      }                                                              │
│      public static Singleton getInstance() {                        │
│          return Holder.INSTANCE;                                    │
│      }                                                              │
│  }                                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 락 전후로 조건 두 번 확인
• 목적: 불필요한 락 회피
• 위험: 재배치로 미완성 객체 반환
• 해결: volatile, atomic, release/acquire
• 권장: 정적 지역 변수, call_once
• 패턴: 싱글톤, 지연 초기화
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [메모리 모델](./226_memory_model.md) → 재배치 문제
- [원자적 연산](./239_atomic_operations.md) → 구현 기반
- [뮤텍스](./232_mutex.md) → 락 획득
- [happens-before](./227_happens_before.md) → 순서 보장

### 👶 어린이를 위한 3줄 비유 설명

**개념**: Double-Checked Locking은 "입장권 확인" 같아요!

**원리**: 입구에서 보고 안에서 다시 봐요!

**효과**: 빠르게 지나가요!
