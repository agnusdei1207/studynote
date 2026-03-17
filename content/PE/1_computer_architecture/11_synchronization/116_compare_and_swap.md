+++
title = "116. Compare-and-Swap (CAS) 연산"
date = 2026-03-05
categories = ["컴퓨터구조", "병렬처리", "동기화", "원자적연산"]
draft = false
+++

# Compare-and-Swap (CAS) 연산

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CAS(Compare-and-Swap)는 메모리 위치의 현재 값과 예상 값(Expected)을 비교하여 일치하면 새 값(New)을 저장하고, 불일치하면 실패를 반환하는 **원자적(Atomic) 읽기-수정-쓰기(RMW) 연산**으로, Test-and-Set의 ABA 문제를 해결하고 Lock-free 자료구조의 기반이 된다.
> 2. **가치**: 단일 명령어로 **Compare(비교) + Swap(교체)**를 원자적으로 수행하여 경합 상황에서의 Lock-free 알고리즘 구현이 가능하며, x86 CMPXCHG, RISC-V sc 등의 ISA 명령어와 Java AtomicInteger, C++ std::atomic으로 널리 지원된다.
> 3. **융합**:现代 멀티코어 환경의 **Lock-free 동시성 제어**의 핵심으로, 고성능 큐(Concurrent Queue), 해시 맵(Concurrent HashMap), 레퍼런스(Relaxed) 메모리 모델의 기반이며, ABA 문제 해결을 위해 **버전(Version) 번호**를 활용하여 확장성을 보장한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
Compare-and-Swap(CAS)는 **"메모리의 현재 값과 예상 값을 비교하여, 일치하면 새 값으로 원자적으로 교체하고 성공 여부를 반환하는 연산"**이다.

**수학적 정의**:
```
CAS(addr, expected, new)
    if (*addr == expected) {
        *addr = new;
        return true;  // 성공
    } else {
        return false; // 실패, 현재 값 반환
    }
```

### 💡 비유
CAS는 **"번호표 교환"**과 같다.
- **Compare**: "내 번호가 맞는가?" (현재 값과 예상 값 비교)
- **Swap**: "맞으면 새 번호로 교체" (새 값으로 변경)
- **원자성**: 번호표 확인과 교체를 한 번에 수행하여 중간에 다른 사람이 개입 불가

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         원자적 RMW 연산의 진화                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

1960년대: Test-and-Set (TAS)
         • 단순한 원자적 설정
         • Bus Locking으로 성능 문제
         • Spinlock 구현에 사용
         ↓
1970년대: Compare-and-Swap (CAS) 제안
         • IBM System/370에서 도입
         • TAS보다 유연함
         • ABA 문제 존재
         ↓
1990년대: LL/SC (Load-Linked/Store-Conditional)
         • MIPS, RISC-II에서 도입
         • ABA 문제 해결 (weak)
         • Bus Locking 없음
         ↓
2000년대~현재: 확장된 CAS variants
         • CAS2, CAS4, CAS8 (다중 워드)
         • ARM LL/SC, RISC-V lr/sc
         • Lock-free 자료구조 표준
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### CAS 연산 구성 요소

| 요소 | 설명 | 예시 | ISA |
|------|------|------|-----|
| **addr** | 대상 메모리 주소 | `&lock_var` | x86: r/m8 |
| **expected** | 예상 값 (비교 기준) | `0` (Unlock) | x86: r32 |
| **new** | 새 값 (교체 값) | `1` (Lock) | x86: r32 |
| **return** | 성공 여부 또는 현재 값 | `true/false` | ZF 플래그 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CAS 연산 동작 메커니즘                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    CPU0                    CPU1                    Memory (Shared Variable)
      │                       │                        │
      │                       │                        ▼
      │                       │                ┌─────────────────────┐
      │                       │                │ Lock Flag (0x1000)   │
      │                       │                │ 초기값: 0 (Unlock)   │
      │                       │                └─────────────────────┘
      │                       │                        ▲
      └───────────────────────┼────────────────────────┼────────┐
                             │                        │        │
                             ▼                        ▼        ▼
                      [T1: CAS(addr, 0, 1)]        [T2: CAS(addr, 0, 1)]
                      CPU0 시도                     CPU1 시도
                      ┌──────────────────┐      ┌──────────────────┐
                      │  CMPXCHG        │      │  CMPXCHG        │
                      │  [0x1000], rAX   │      │  [0x1000], rAX   │
                      └────────┬─────────┘      └────────┬─────────┘
                               │                           │
                               ▼                           ▼
                    ┌────────────────────────────────────────────────────────────────────────┐
                    │                    Cache Coherence Protocol (MESI)               │
                    │                               │                                 │
                    │    CPU0                  │                  CPU1              │
                    │  [Read]───┐               │              [Read]───┐              │
                    │    │      │               │                  │      │              │
                    │    ▼      │               │                  ▼      │              │
                    │  [Cache] │               │                [Cache] │              │
                    │    │      │               │                    │      │              │
                    │    ▼      │               │                    ▼      │              │
                    │  Bus Read │               │                 Bus Read │              │
                    │    │      │               │                    │      │              │
                    │    ▼      ▼               │                    ▼      ▼              │
                    │    ┌─────────────────────────────┐                          │              │
                    │    │  Both cores read value 0 │                          │              │
                    │    │  (Shared Cache Line)   │                          │              │
                    │    └─────────────────────────────┘                          │              │
                    │                               │                                 │              │
                    │    CPU0: rAX ← 0 (Expected)   │                                 │              │
                    │    CPU1: rAX ← 0 (Expected)   │                                 │              │
                    │                               │                                 │              │
                    │                               ▼                                 │              │
                    │                [CAS Atomic Execution - Race!]                     │              │
                    │                               │                                 │              │
                    │    ┌────────────────────────────────────────────────────────────┐    │              │
                    │    │  Cache Coherence: Bus Arbitration (CPU0 wins)        │    │              │
                    │    └────────────────────────────────────────────────────────────┘    │              │
                    │                               │                                 │              │
                    │    [CPU0 wins]                 [CPU1 loses]                      │              │
                    │         │                           │                          │              │
                    ▼         ▼                           ▼                          ▼              ▼
            CPU0 executes              CPU1 stalls (Retry)
            CAS successfully           CMPXCHG restarted
            Memory: 0 → 1
            ZF=1 (Success)               [T2 Retry]
                                        │
                                        ▼
                                    CPU1 reads Memory: 1
                                    expected=0, actual=1
                                    ZF=0 (Failure)
                                    Retry required
```

### 심층 동작 원리

#### 1. x86 CMPXCHG 명령어

**어셈블리 예시**:
```asm
; CAS(addr, expected, new)
MOV rax, [expected]    ; rax = expected
LOCK cmpxchg [addr], rbx  ; [addr]과 rax 비교, 같으면 rbx 저장
; ZF=1: 성공 (값이 rax와 같음)
; ZF=0: 실패 (값이 다름, rax에 현재 값 저장)
```

**x86 CMPXCHG 의사코드**:
```text
IF (ZF == 1) THEN
    ; CAS 성공
    temp ← [addr]
    [addr] ← rbx
    rbx ← temp
ELSE
    ; CAS 실패
    temp ← [addr]
    rbx ← temp
    [addr] ← temp (no change)
    rax ← temp (현재 값 반환)
END IF
```

#### 2. ABA 문제와 해결책

**ABA 문제**:
```
초기 상태: 공유 변수 = A
    T1: CAS(x, A, B) 시도
    T2: CAS(x, A, C) → 성공 (A → C)
    T3: CAS(x, C, A) → 성공 (C → A)
    T1: 재시도 - 현재 값 A가 예상 값 A와 같으므로 성공!
        문제: 중간에 값이 A → B → C → A로 변경되었음을 인지 못함
```

**해결책: Versioned CAS**:
```
struct Node {
    int value;
    int version;
};

bool CAS_V(Node* ptr, int expected_version, int new_value, int new_version) {
    if (ptr->version == expected_version) {
        ptr->value = new_value;
        ptr->version = new_version;
        return true;
    }
    return false;
}
```

#### 3. Lock-free 큐 구현

```c
// CAS 기반 Lock-free 큐 (Michael-Scott Queue)
struct Node {
    T data;
    Node* next;
};

class LockFreeQueue {
    Node* head;
    Node* tail;

    void enqueue(T value) {
        Node* node = new Node(value);
        Node* old_tail = tail;
        // CAS로 tail 업데이트 (원자적)
        while (!cas(&tail, old_tail, node)) {
            old_tail = tail;  // 실패 시 재시도
        }
        old_tail->next = node;
    }

    T dequeue() {
        if (head == tail) return empty;
        Node* old_head = head;
        // CAS로 head 업데이트 (원자적)
        while (!cas(&head, old_head, old_head->next)) {
            // 재시도
        }
        T value = old_head->data;
        delete old_head;
        return value;
    }
};
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### TAS vs CAS vs LL/SC 비교

| 특성 | Test-and-Set | CAS | LL/SC |
|------|--------------|-----|-------|
| **복잡도** | 단순 | 중간 | 복잡 |
| **ABA 문제** | 예 | 예 | 아님(weak) |
| **Bus Locking** | O(LOCK#) | X(최신 ISA) | X |
| **기능** | 원자적 설정만 | 비교+설정 | 조건부 저장 |
| **ISA 지원** | x86 BTS | x86 CMPXCHG | MIPS LL, ARM LDXR |
| **용도** | Spinlock, PIC | Lock-free | Lock-free, RISC |

### 과목 융합 관점 분석

#### 1. SMP ↔ CAS
- **Cache Coherence**: CAS는 캐시 라인을 M(Modified) 상태로 변경
- **False Sharing**: CAS 반복 실패의 주요 원인
- **해결**: 캐시 라인 정렬(Cache Line Alignment), 패딩

#### 2. 인터럽트 컨트롤러 ↔ CAS
- **8259A PIC**: TAS를 사용했으나 최신 APIC는 CAS 기반
- **MSI(Message Signaled Interrupts**: CAS 기반 인터럽트 등록

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 고빈도 Lock-free 큐 구현
**상황**: 초당 100만 건의 메시지 처리 needed
**판단**:
1. **Mutex Lock**: 병목으로 성능 저하
2. **CAS 기반 Lock-free 큐**: 높은 처리량
3. **배치 처리**: CAS 실패 시 여러 엔큐 후 재시도

---

## Ⅴ. 기대효과 및 결론

### CAS 기반 Lock-free 성능

| 지표 | Mutex Lock | CAS Lock-free | 향상 폭 |
|------|-----------|--------------|---------|
| 처리량 | 50M ops/s | 200M ops/s | 300% |
| 지연 시간 | 20ns | 5ns | 75% 감소 |
| 확장성 | 낮음 (Lock 경합) | 높음 | 무한 확장 가능 |

### 미래 전망

1. **Transactional Memory**: 하드웨어적 트랜잭션 지원
2. **RISC-V Atomic**: lr/sc 표준화
3. **ARM LDXR/STXR**: LL/SC ARM 버전

### ※ 참고 표준/가이드
- **x86 SDM**: LOCK prefix, CMPXCHG 명령어
- **C++ std::atomic**: CAS 래퍼
- **Java AtomicInteger**: compareAndSet()

---

## 📌 관련 개념 맵

- [Test-and-Set](./118_test_and_set.md) - CAS의 선행 기술
- [하드웨어 동기화](./115_hardware_synchronization.md) - 동기화 개요
- [Spinlock](../../2_operating_system/4_concurrency_sync/) - TAS 기반 Lock
- [캐시 일관성](./104_cache_coherence.md) - CAS와의 관계
