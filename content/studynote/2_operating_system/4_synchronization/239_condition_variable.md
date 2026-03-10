+++
title = "239. 조건 변수 (Condition Variable) - x.wait(), x.signal()"
weight = 239
+++

# 239. 원자적 연산 (Atomic Operations)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 중단 없이 한 번에 완료되는 연산
> 2. **가치**: 락 없는 동기화의 기반
> 3. **융합**: CAS, 메모리 모델, 락 프리와 연관

---

## Ⅰ. 개요

### 개념 정의

원자적 연산(Atomic Operations)은 **실행 도중 중단되지 않고, 한 번에 완전히 수행되는 연산**이다. 다중 스레드 환경에서 락 없이 안전하게 공유 변수를 조작할 수 있게 한다.

### 💡 비유: 자판기 버튼
원자적 연산은 **자판기 버튼**과 같다. 한 번 누르면 음료가 나올 때까지 멈추지 않는다. 중간에 끊기지 않는다.

### 원자적 연산 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                원자적 연산 구조                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 원자적 연산】                                                  │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  연산              설명                    사용 예시              │ │
│  │  ────                  ────                        ────          │ │
│  │  load              원자적 읽기              flags 확인            │ │
│  │  store             원자적 쓰기              flags 설정            │ │
│  │  add/sub           원자적 덧셈/뺄셈        카운터                │ │
│  │  inc/dec           원자적 증가/감소        참조 카운트            │ │
│  │  and/or/xor        원자적 비트 연산        플래그 조작            │ │
│  │  swap/xchg         원자적 교환             타임아웃 설정          │ │
│  │  CAS               비교 후 조건부 교환      락 프리 알고리즘       │ │
│  │  fetch_add         이전 값 반환하며 증가    카운터                │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【비원자적 vs 원자적】                                                │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  비원자적 (위험):                                                 │ │
│  │  counter++;  // LOAD → ADD → STORE (중단 가능)                 │ │
│  │                                                             │ │
│  │  원자적 (안전):                                                   │ │
│  │  atomic_inc(&counter);  // 단일 원자적 명령                     │ │
│  │                                                             │ │
│  │  문제 상황:                                                        │ │
│  │  스레드 A: LOAD(10) ──────────────────► ADD(11) ──────► STORE   │ │
│  │  스레드 B:         LOAD(10) ──► ADD(11) ──► STORE               │ │
│  │                                          ↑                       │ │
│  │                                   덮어쓰기!                        │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【하드웨어 지원】                                                     │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  x86:                                                             │ │
│  │  • LOCK prefix: 메모리 연산 원자적 수행                          │ │
│  │  • XCHG: 교환                                                    │ │
│  │  • CMPXCHG: CAS                                                  │ │
│  │  • XADD: 교환 후 덧셈                                            │ │
│  │                                                             │ │
│  │  ARM:                                                             │ │
│  │  • LDREX/STREX: Load/Store Exclusive                            │ │
│  │  • LDAXR/STLXR: Acquire/Release 변형                            │ │
│  │  • CAS, SWP: 아키텍처 v8.1+                                      │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                원자적 연산 상세                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【CAS (Compare-And-Swap)】                                           │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  bool CAS(int* ptr, int expected, int new_value) {              │ │
│  │      if (*ptr == expected) {                                     │ │
│  │          *ptr = new_value;                                       │ │
│  │          return true;                                            │ │
│  │      } else {                                                    │ │
│  │          return false;                                           │ │
│  │      }                                                           │ │
│  │  }  // 이 전체가 원자적으로 실행                                  │ │
│  │                                                             │ │
│  │  사용 예시 (락 프리 카운터):                                       │ │
│  │  void atomic_inc(int* counter) {                                 │ │
│  │      int old;                                                    │ │
│  │      do {                                                        │ │
│  │          old = *counter;                                         │ │
│  │      } while (!CAS(counter, old, old + 1));                      │ │
│  │  }                                                               │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【Fetch-and-Add】                                                    │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  int fetch_and_add(int* ptr, int value) {                        │ │
│  │      return atomic_add(ptr, value);  // 이전 값 반환              │ │
│  │  }                                                               │ │
│  │                                                             │ │
│  │  // 사용 예시                                                     │ │
│  │  int ticket = fetch_and_add(&next_ticket, 1);                    │ │
│  │  while (current_serving != ticket) { /* 대기 */ }                │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【ABA 문제】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 스레드 A: ptr 읽음 (값=A)                                     │ │
│  │  2. 스레드 B: ptr를 B로 변경                                      │ │
│  │  3. 스레드 B: ptr를 다시 A로 변경 (다른 객체)                      │ │
│  │  4. 스레드 A: CAS(ptr, A, C) 성공! (잘못됨)                       │ │
│  │                                                             │ │
│  │  해결: 더블 워드 CAS, 버전 카운터, hazard pointer                 │ │
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
│  【C11 stdatomic.h】                                                  │
│  ──────────────────                                                  │
│  #include <stdatomic.h>                                             │
│                                                                     │
│  atomic_int counter = 0;                                            │
│  atomic_flag lock = ATOMIC_FLAG_INIT;                               │
│                                                                     │
│  // 기본 연산                                                        │
│  atomic_store(&counter, 10);                                        │
│  int val = atomic_load(&counter);                                   │
│  atomic_fetch_add(&counter, 1);                                     │
│  atomic_fetch_sub(&counter, 1);                                     │
│                                                                     │
│  // CAS                                                              │
│  int expected = 10;                                                 │
│  if (atomic_compare_exchange_strong(&counter, &expected, 20)) {     │
│      // 성공: counter = 20                                           │
│  } else {                                                           │
│      // 실패: expected = 현재 값                                     │
│  }                                                                  │
│                                                                     │
│  // Exchange                                                         │
│  int old = atomic_exchange(&counter, 30);                           │
│                                                                     │
│  【C++ std::atomic】                                                  │
│  ──────────────────                                                  │
│  #include <atomic>                                                   │
│                                                                     │
│  std::atomic<int> counter{0};                                        │
│  std::atomic<bool> flag{false};                                      │
│                                                                     │
│  // 연산자 오버로딩                                                   │
│  counter++;                    // fetch_add                          │
│  counter--;                    // fetch_sub                          │
│  counter = 10;                // store                               │
│  int val = counter;            // load                               │
│                                                                     │
│  // 명시적 연산                                                       │
│  counter.fetch_add(1);                                               │
│  counter.compare_exchange_weak(expected, desired);                   │
│  counter.exchange(0);                                                │
│                                                                     │
│  // 메모리 순서 지정                                                   │
│  counter.store(1, std::memory_order_release);                        │
│  val = counter.load(std::memory_order_acquire);                      │
│                                                                     │
│  【GCC Built-in】                                                     │
│  ──────────────────                                                  │
│  int counter = 0;                                                   │
│                                                                     │
│  __sync_fetch_and_add(&counter, 1);                                 │
│  __sync_fetch_and_sub(&counter, 1);                                 │
│  __sync_bool_compare_and_swap(&counter, 0, 1);                      │
│  __sync_val_compare_and_swap(&counter, 0, 1);                       │
│  __sync_lock_test_and_set(&lock, 1);                                │
│  __sync_lock_release(&lock);                                        │
│                                                                     │
│  __atomic_fetch_add(&counter, 1, __ATOMIC_SEQ_CST);                 │
│  __atomic_compare_exchange_n(&counter, &expected, desired,          │
│                               false, __ATOMIC_SEQ_CST,              │
│                               __ATOMIC_SEQ_CST);                     │
│                                                                     │
│  【Linux 커널】                                                        │
│  ──────────────────                                                  │
│  atomic_t counter = ATOMIC_INIT(0);                                 │
│                                                                     │
│  atomic_set(&counter, 10);                                          │
│  int val = atomic_read(&counter);                                   │
│  atomic_inc(&counter);                                              │
│  atomic_dec(&counter);                                              │
│  atomic_add(5, &counter);                                           │
│  atomic_sub(3, &counter);                                           │
│                                                                     │
│  if (atomic_dec_and_test(&counter)) {                               │
│      // counter가 0이 됨                                             │
│  }                                                                  │
│                                                                     │
│  // 64-bit                                                           │
│  atomic64_t big_counter;                                            │
│  atomic64_inc(&big_counter);                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 중단 없이 완료되는 연산
• 기본: load, store, add, sub
• 고급: CAS, fetch_add, exchange
• 하드웨어: LOCK prefix, LDREX/STREX
• 문제: ABA 문제
• 활용: 락 프리 자료구조
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [CAS](./240_cas.md) → 핵심 원자적 연산
- [원자성](./225_atomicity.md) → 기본 속성
- [메모리 모델](./226_memory_model.md) → 순서 보장
- [스핀락](./230_spinlock.md) → 구현 활용

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 원자적 연산은 "자판기 버튼" 같아요!

**원리**: 누르면 끝까지 진행돼요!

**효과**: 중간에 끊기지 않아요!
