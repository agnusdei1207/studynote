+++
title = "265. 낙관적 병행성 제어 (Optimistic Concurrency Control)"
weight = 265
+++

# 265. 락 순서 규칙 (Lock Ordering)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 락 획득 순서를 일관되게 유지
> 2. **가치**: 교착상태 예방의 핵심 원칙
> 3. **융합**: 교착상태, 순환 대기, 환형 의존성과 연관

---

## Ⅰ. 개요

### 개념 정의

락 순서 규칙(Lock Ordering)은 **모든 락에 전역 순서를 부여하고, 항상 같은 순서로 락을 획득하는 규칙**이다. 순환 대기를 방지하여 교착상태를 예방한다.

### 💡 비유: 계단 오르기
락 순서 규칙은 **계단 오르기**와 같다. 1층 → 2층 → 3층 순서로만 올라간다. 2층에서 1층으로 내려가지 않는다. 그러면 서로 부딪히지 않는다.

### 락 순서 규칙 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                락 순서 규칙 구조                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【교착상태 발생 (순서 없음)】                                           │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  T1: lock(A) → lock(B) → unlock(B) → unlock(A)                    │ │
│  │  T2: lock(B) → lock(A) → unlock(A) → unlock(B)                    │ │
│  │                                                             │ │
│  │  시간 ↓:                                                            │ │
│  │  T1: lock(A) ──────┐                                               │ │
│  │                    ↓                                               │ │
│  │  T2:          lock(B) ──────┐                                      │ │
│  │                             ↓                                      │ │
│  │  T1:          lock(B) 대기... (T2가 B 보유)                         │ │
│  │  T2:          lock(A) 대기... (T1이 A 보유)                         │ │
│  │                             ↓                                      │ │
│  │                    교착상태!                                         │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【교착상태 예방 (순서 규칙)】                                           │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  규칙: 항상 A → B 순서로 락 획득 (A < B)                               │ │
│  │                                                             │ │
│  │  T1: lock(A) → lock(B) → unlock(B) → unlock(A)                    │ │
│  │  T2: lock(A) → lock(B) → unlock(B) → unlock(A)  // 같은 순서!       │ │
│  │                                                             │ │
│  │  시간 ↓:                                                            │ │
│  │  T1: lock(A) ────────────[lock(B)]──[unlock(B)]──[unlock(A)]       │ │
│  │                    ↑                                               │ │
│  │  T2:         [A 대기]──[lock(A)]──[B 대기]──[lock(B)]──...         │ │
│  │                             ↑                                      │ │
│  │                    T1이 A 놓을 때까지 대기                            │ │
│  │                    → 순환 없음 → 교착상태 없음                         │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【순서 결정 방법】                                                      │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 주소 기반:                                                      │ │
│  │     if (&lock_a < &lock_b) { lock(&lock_a); lock(&lock_b); }       │ │
│  │                                                             │ │
│  │  2. ID 기반:                                                        │ │
│  │     if (lock_a.id < lock_b.id) { ... }                             │ │
│  │                                                             │ │
│  │  3. 이름 기반:                                                      │ │
│  │     // 알파벳 순서: account_lock → user_lock                        │ │
│  │                                                             │ │
│  │  4. 계층 기반:                                                      │ │
│  │     // 레벨 1 → 레벨 2 → 레벨 3                                       │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                락 순서 규칙 상세                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【구현 기법】                                                         │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. std::lock (C++11) - 임의 순서 자동 처리:                        │ │
│  │     std::lock(lock_a, lock_b);  // 교착상태 없이 모두 획득            │ │
│  │     std::lock_guard<std::mutex> lg_a(lock_a, std::adopt_lock);   │ │
│  │     std::lock_guard<std::mutex> lg_b(lock_b, std::adopt_lock);   │ │
│  │                                                             │ │
│  │  2. scoped_lock (C++17) - 더 간단:                                  │ │
│  │     std::scoped_lock lock(lock_a, lock_b);  // RAII               │ │
│  │                                                             │ │
│  │  3. try_lock 루프:                                                  │ │
│  │     while (true) {                                                  │ │
│  │         lock(a);                                                    │ │
│  │         if (try_lock(b)) break;                                     │ │
│  │         unlock(a);                                                  │ │
│  │         // 백오프...                                                  │ │
│  │     }                                                              │ │
│  │                                                             │ │
│  │  4. 계층적 락:                                                      │ │
│  │     class HierarchicalLock {                                       │ │
│  │         int level;                                                  │ │
│  │         void lock() {                                               │ │
│  │             assert(current_level < level);  // 검증                  │ │
│  │         }                                                           │ │
│  │     };                                                              │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【주의사항】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 모든 코드 경로에서 동일한 순서 유지                                  │ │
│  │  2. 콜백 함수 내부에서 락 획득 시 주의                                   │ │
│  │  3. 동적 락 순서 결정 시 일관성 유지                                    │ │
│  │  4. 서드파티 라이브러리 락 순서 확인                                    │ │
│  │  5. 락 순서 문서화                                                    │ │
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
│  【C++ 주소 기반 순서】                                                │
│  ──────────────────                                                  │
│  void transfer(Account& from, Account& to, int amount) {            │
│      // 주소 기반 순서 결정                                             │
│      std::mutex* first = &from.mutex;                               │
│      std::mutex* second = &to.mutex;                                │
│      if (first > second) std::swap(first, second);                  │
│                                                                     │
│      std::lock_guard<std::mutex> lg1(*first);                       │
│      std::lock_guard<std::mutex> lg2(*second);                      │
│                                                                     │
│      from.balance -= amount;                                        │
│      to.balance += amount;                                          │
│  }                                                                  │
│                                                                     │
│  【C++ std::scoped_lock (C++17)】                                    │
│  ──────────────────                                                  │
│  void transfer(Account& from, Account& to, int amount) {            │
│      // 자동으로 교착상태 없이 획득                                      │
│      std::scoped_lock lock(from.mutex, to.mutex);                   │
│                                                                     │
│      from.balance -= amount;                                        │
│      to.balance += amount;                                          │
│  }                                                                  │
│                                                                     │
│  【C++ std::lock + adopt_lock】                                       │
│  ──────────────────                                                  │
│  void transfer(Account& from, Account& to, int amount) {            │
│      // 교착상태 없이 획득                                              │
│      std::lock(from.mutex, to.mutex);                               │
│                                                                     │
│      // RAII로 관리 (이미 획득된 락 인수)                               │
│      std::lock_guard<std::mutex> lg1(from.mutex, std::adopt_lock); │
│      std::lock_guard<std::mutex> lg2(to.mutex, std::adopt_lock);   │
│                                                                     │
│      from.balance -= amount;                                        │
│      to.balance += amount;                                          │
│  }                                                                  │
│                                                                     │
│  【Java synchronized 순서】                                           │
│  ──────────────────                                                  │
│  public void transfer(Account from, Account to, int amount) {       │
│      // ID 기반 순서                                                  │
│      Account first = from.id < to.id ? from : to;                   │
│      Account second = from.id < to.id ? to : from;                  │
│                                                                     │
│      synchronized (first) {                                         │
│          synchronized (second) {                                    │
│              from.balance -= amount;                                │
│              to.balance += amount;                                  │
│          }                                                          │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【계층적 락 (디자인 패턴)】                                            │
│  ──────────────────                                                  │
│  class HierarchicalMutex {                                          │
│      std::mutex internal_mutex;                                     │
│      const int level;                                               │
│      static thread_local int this_thread_level;                     │
│                                                                     │
│  public:                                                            │
│      HierarchicalMutex(int level) : level(level) {}                 │
│                                                                     │
│      void lock() {                                                  │
│          assert(this_thread_level < level);  // 검증                  │
│          internal_mutex.lock();                                     │
│          this_thread_level = level;                                 │
│      }                                                              │
│                                                                     │
│      void unlock() {                                                │
│          this_thread_level = level - 1;                             │
│          internal_mutex.unlock();                                   │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  // 사용                                                              │
│  HierarchicalMutex level1(1), level2(2);                            │
│  level1.lock();  // OK                                              │
│  level2.lock();  // OK (1 < 2)                                      │
│  level1.lock();  // assert 실패! (2 > 1)                             │
│                                                                     │
│  【락 순서 검증 도구】                                                  │
│  ──────────────────                                                  │
│  // Clang ThreadSanitizer                                           │
│  // g++ -fsanitize=thread -g                                        │
│  // 런타임에 교착상태 감지                                               │
│                                                                     │
│  // Helgrind (Valgrind)                                             │
│  // valgrind --tool=helgrind ./program                              │
│                                                                     │
│  // Rust: 타입 시스템으로 컴파일 시 검증                                   │
│  // 순서 위반 시 컴파일 에러                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 락에 전역 순서 부여, 일관된 획득
• 목적: 순환 대기 방지, 교착상태 예방
• 방법: 주소, ID, 이름, 계층 기반
• C++: std::lock, scoped_lock
• Java: synchronized 중첩 순서
• 검증: TSan, Helgrind
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [교착상태](./291_deadlock.md) → 예방 대상
- [순환 대기](./294_circular_wait.md) → 방지 조건
- [락 그래프](./275_lock_graph.md) → 분석 도구
- [락 홀더](./271_lock_holder.md) → 보유자

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 락 순서 규칙은 "계단 오르기" 같아요!

**원리**: 1층 → 2층 → 3층 순서로만 올라가요!

**효과**: 서로 부딪히지 않아요!
