+++
title = "36. 메모리 일관성 모델 (Memory Consistency Model)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Memory-Model", "Consistency", "Sequential", "Weak", "Relaxed"]
draft = false
+++

# 메모리 일관성 모델 (Memory Consistency Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 메모리 일관성 모델은 **"멀티코어 **시스템**에서 **메모리 **연산 **순서**를 **보장**하는 **규칙"**으로, **Strong**(SC, **TSO)와 **Weak**(Relaxed, **Release**/**Consistency)로 **구분**된다.
> 2. **종류**: **Sequential Consistency**(SC)는 **프로그램 **순서**를 **보장**, **Total Store Order**(TSO)는 **쓰기 **순서**만 **보장**, **Weak Ordering**은 **동기화 **연산**으로 **순서**를 **명시**한다.
> 3. **하드웨어**: **x86**는 **TSO**(Strong **Buffer), **ARM**은 **Weak**(Load-**Linked/**Store-**Conditional), **RISC-V**는 **RVWMO**(Release **Consistency)를 **사용**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
메모리 일관성 모델은 **"메모리 연산 순서 규칙"**이다.

**연산 재배치 문제**:
- **Compiler**: 최적화로 순서 변경
- **CPU**: Out-of-Order 실행
- **Memory**: 캐시 비순차 flush

### 💡 비유
메모리 일관성은 ****여러 **사람이 **동시에 **책 **쓰기 ****와 같다.
- **SC**: 모두가 같은 순서로 인지
- **Weak**: 순서가 달라도 허용

---

## Ⅱ. 아키텍처 및 핵심 원리

### Sequential Consistency (SC)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Sequential Consistency                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Definition: The result of any execution is the same as if the operations of all
    processors were executed in some sequential order, and the operations of each
    individual processor appear in this sequence in the order specified by its program.

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Thread 1                 Thread 2                                                  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  x = 1                   (initially x = 0, y = 0)                                 │  │  │
    │  │  y = 1                   print(x, y)                                              │  │  │
    │  │                                                                                       │  │  │
    │  │  Possible outcomes under SC:                                                        │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  1. Thread 1 executes first:     (0, 0) ✗                                       │  │  │  │
    │  │  │  2. Thread 2 executes first:     (1, 0) or (0, 1)                              │  │  │  │
    │  │  │  3. Interleaved:                    (1, 1) ✓ (print sees both writes)               │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │                                                                                       │  │  │
    │  │  (0, 0) impossible because prints occur after assignments in program order           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Weak Ordering

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Weak Ordering                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Principle: Data ordering preserved only by synchronization operations                   │  │
    │                                                                                         │  │
    │  Without Synchronization:                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Thread 1:                    Thread 2:                                             │  │  │
    │  │  x = 1                        if (x == 1)                                      │  │  │
    │  │  y = 1                            print(y)                                │  │  │
    │  │                                                                                       │  │  │
    │  │  Weak Model Outcome: (0, 0) ✓                                                       │  │  │
    │  │  → Loads reordered, writes not visible yet                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  With Synchronization:                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Thread 1:                    Thread 2:                                             │  │  │
    │  │  x = 1                        lock(l)                                         │  │  │
    │  │  release(l)                   if (x == 1)                                      │  │  │
    │  │                                print(y)                                │  │  │
    │  │                                acquire(l)                               │  │  │
    │  │                                                                                       │  │  │
    │  │  → Release establishes happens-before relationship                                   │  │  │
    │  │  → Thread 2 sees x = 1                                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 일관성 모델 비교

| 모델 | 순서 보장 | 성능 | 구현 |
|------|-----------|------|------|
| **SC** | 전체 | 낮음 | 어려움 |
| **TSO** | 쓰기 | 중간 | 중간 |
| **PSO** | Partial Store | 높음 | 중간 |
| **Weak** | 동기화 | 매우 높음 | 복잡 |

### x86 TSO (Total Store Order)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         x86 Memory Model (TSO)                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Guarantees:                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Loads are not reordered with other loads                                        │  │  │
    │  │  2. Stores are not reordered with other stores                                      │  │  │
    │  │  3. Loads are not reordered with earlier stores                                     │  │  │
    │  │  4. Stores may be delayed in store buffer                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Store Buffer Example:                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Thread 1:                    Thread 2:                                             │  │  │
    │  │  x = 1                        if (x == 1)                                      │  │  │
    │  │  r1 = y                       y = 1                                            │  │  │
    │  │                                                                                       │  │  │
    │  │  → r1 = 0 possible! (x=1 in buffer, y=1 committed first)                             │  │  │
    │  │  → Store-Load reordering allowed                                                      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Fix (MFENCE):                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  x = 1                                                                                  │  │  │
    │  │  mfence  ← forces store buffer flush                                                  │  │  │
    │  │  r1 = y                                                                                │  │  │
    │  │  → r1 = 1 guaranteed                                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### ARM Weak Memory Model

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         ARM Memory Ordering                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Load-Load / Load-Store reordering allowed                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Thread 1:                    Thread 2:                                             │  │  │
    │  │  x = 1                        x = 1                                            │  │  │
    │  │  r1 = y                       r2 = y                                           │  │  │
    │  │                                                                                       │  │  │
    │  │  → (r1=0, r2=0) possible!                                                               │  │  │
    │  │  → Loads can be executed before stores                                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────~┘  │  │
    │                                                                                         │  │
    │  Barriers:                                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  DMB (Data Memory Barrier):    Orders data accesses                                 │  │  │
    │  │  DSB (Data Synchronization):    Completes preceding accesses                           │  │  │
    │  │  ISB (Instruction Synchronization): Flush pipeline                                   │  │  │
    │  │                                                                                       │  │  │
    │  │  Load-Acquire / Release-Store (C++11 atomic):                                        │  │  │
    │  │  x.store(1, memory_order_release)                                                     │  │  │
    │  │  r1 = y.load(memory_order_acquire)                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### C++11 Memory Order

```cpp
// Sequentially Consistent (strongest)
std::atomic<int> x{0}, y{0};
// Thread 1:
x.store(1, std::memory_order_seq_cst);
r1 = y.load(std::memory_order_seq_cst);

// Acquire-Release (weaker, still synchronized)
// Thread 1:
x.store(1, std::memory_order_release);
// Thread 2:
if (x.load(std::memory_order_acquire) == 1) {
    // All writes before release visible
}

// Relaxed (weakest, no synchronization)
std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);
// No ordering guarantees with other memory
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 락프리 큐 구현
**상황**: 멀티프로듀서-소비자
**판단**: Acquire-Release

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Lock-Free Queue with Acquire-Release                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Producer:                                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  node->next = nullptr;                                                                │  │  │
    │  │  // Release: Ensure node initialized before publishing                                 │  │  │
    │  │  tail.store(node, memory_order_release);                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Consumer:                                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  // Acquire: Ensure we see initialized node                                          │  │  │
    │  │  node = head.load(memory_order_acquire);                                             │  │  │
    │  │  // Read node->data (guaranteed to see producer's write)                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 메모리 모델 기대 효과

| 모델 | 성능 | 프로그래밍 | 사용처 |
|------|------|-----------|--------|
| **SC** | 낮음 | 쉬움 | 알고리즘 검증 |
| **TSO** | 중간 | 중간 | x86 서버 |
| **Weak** | 높음 | 어려움 | 모바일, 임베디드 |

### 모범 사례

1. **기본**: Sequentially Consistent
2. **최적화**: Acquire-Release
3. **카운터**: Relaxed
4. **펜스**: dmb, mfence

### 미래 전망

1. **C++**: memory_order_explicit
2. **RISC-V**: RVWMO
3. **Hardware**: Hybrid models

### ※ 참고 표준/가이드
- **x86**: Intel Manual
- **ARM**: Barrier Litmus Tests
- **C++**: atomic memory order

---

## 📌 관련 개념 맵

- [캐시 일관성](./11_synchronization/122_cache_coherence.md) - 하드웨어 동기화
- [스레드 안전성](../../2_operating_system/2_process_thread/106_thread_safety.md) - 동기화
- [멀티코어](./1_logic/97_multicore.md) - 병렬 처리
