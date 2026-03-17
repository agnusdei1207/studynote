+++
title = "41. 스펙터/멜트다운 (Spectre/Meltdown)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Spectre", "Meltdown", "Side-Channel", "Speculative-Execution", "Security"]
draft = false
+++

# 스펙터/멜트다운 (Spectre/Meltdown)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스펙터/멜트다운은 **"추측 **실행**(Speculative Execution)**과 **캐시 **사이드 **채널**(Cache Side Channel)**을 **이용**한 **하드웨어 **보안 **취약점\"**으로, **프로세서 **내부 **최적화**가 **메모리 **보안 **경계**를 **우회**하여 **데이터 **유출**이 **가능**하다.
> 2. **유형**: **Meltdown**(KAISER, **Page Table Isolation)**는 **User → Kernel **메모리 **접근**을 **우회**하고 **Spectre**(Bounds Check **Bypass, **Branch Target Injection)**는 **다른 **프로세스**의 **데이터**를 **추론**한다.
> 3. **완화**: **OS**(KPTI, **RETPOLINE)**, **Compiler**(retpoline, **LFENCE)**, **Microcode**(Intel **IBRS, **STIBP)** **패치**로 **완화**하고 **Constant-Time **Programming**, **Secure **Speculation**으로 **방어**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
스펙터/멜트다운은 **"추측 실행 취약점"**이다.

**취약점 유형**:
| 유형 | 대상 | 영향 | 완화 |
|------|------|------|------|
| **Meltdown** | Kernel memory | 모든 프로세스 | KPTI |
| **Spectre V1** | Bounds check | Same process | LFENCE |
| **Spectre V2** | Branch target | Cross-process | RETPOLINE |
| **Spectre V4** | Speculative store | Same process | SSBD |

### 💡 비유
사이드 채널은 ****진동 **누설 ****과 같다.
- **실제 데이터**: 진동 내용
- **캐시 타이밍**: 진동 크기
- **추측 실행**: 원격 측정

---

## Ⅱ. 아키텍처 및 핵심 원리

### 사이드 채널 공격 원리

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Side Channel Attack Concept                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Core Idea: Measure cache state to infer secret data
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Attacker Process                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Probe: Access shared memory locations                                          │  │  │
    │  │     - If cached: Fast access (~10 cycles)                                         │  │  │
    │  │     - If not cached: Slow access (~200 cycles)                                    │  │  │
    │  │                                                                                       │  │  │
    │  │  2. Measure access time:                                                           │  │  │
    │  │     - Fast = Victim accessed this location recently                                 │  │  │
    │  │     - Slow = Victim did not access                                                   │  │  │
    │  │                                                                                       │  │  │
    │  │  3. Repeat for multiple locations → Reconstruct victim's data pattern               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Meltdown 공격

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Meltdown Attack (Variant 3)                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Speculative execution ignores permission checks
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Normal code (user process)                                                         │  │
    │  int kernel_value = *(int*)0xFFFFFFFFFFFF000;  // Kernel address                        │  │
    │  → Segmentation fault (permission denied)                                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Meltdown Exploit:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Attacker code (user process)                                                        │  │
    │  char kernel_data[4096];                                                                 │  │
    │                                                                                         │  │
    │  // Step 1: Flush probe_array from cache                                                │  │
    │  for (int i = 0; i < 256; i++) {                                                         │  │
    │      _mm_clflush(&probe_array[i * 4096]);  // CLCACHE instruction                         │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  // Step 2: Read kernel data via speculative execution                                   │  │
    │  // Note: This requires the value to be loaded into a register                          │  │
    │  asm volatile (                                                                          │  │
    │      "1: movzx (%1), %0\n"                    // Read kernel address                    │  │  │
    │      "   shl $12, %0\n"                      // Multiply by 4096                         │  │  │
    │      "   mov (%2, %0), %0\n"                  // Access probe_array[value * 4096]        │  │
    │      :                                                                                   │  │
    │      : "r"(kernel_address), "r"(probe_array)                                            │  │
    │      : "0"(dummy_register)                                                               │  │
    │  );                                                                                      │  │
    │                                                                                         │  │
    │  // Step 3: Even though exception occurs, cache state changed!                            │  │
    │                                                                                         │  │
    │  // Step 4: Measure which probe_array entry is cached                                   │  │
    │  for (int i = 0; i < 256; i++) {                                                         │  │
    │      if (access_time(&probe_array[i * 4096]) < THRESHOLD) {                              │  │
    │          // Entry i is cached → Kernel data value was i                                  │  │
    │          return i;                                                                       │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → Exception occurred but cache side effect remains                                      │  │
    │  → Attacker can read any kernel memory byte by byte                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Spectre V1 (Bounds Check Bypass)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Spectre V1: Bounds Check Bypass                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Vulnerable Code Pattern:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Normal code                                                                         │  │
    │  if (index < array_size) {                   // Bounds check                            │  │
    │      value = array[index];                 // Safe access                              │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → CPU speculates that index < array_size (if branch predictor says likely)               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Attack:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Attacker controls array_size (training)                                             │  │
    │  for (int i = 0; i < 10000; i++) {                                                      │  │
    │      if (malicious_index < 30000) {   // Always true (training)                          │  │
    │          dummy = array[malicious_index];                                                │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    │  → Branch predictor learns: "this branch is usually taken"                               │  │
    │                                                                                         │  │
    │  // Actual attack                                                                        │  │
    │  malicious_index = secret_value;      // Out of bounds!                                 │  │
    │  if (malicious_index < array_size) {  // Speculatively taken (misprediction)              │  │
    │      value = array[secret_value];   // Accesses attacker-controlled memory               │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → Although fault occurs, cache state leaks secret_value                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Mitigation: LFENCE
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  if (index < array_size) {                                                                 │  │
    │      _mm_lfence();  // Serialize: Wait until all previous operations complete              │  │
    │      value = array[index];                                                                │  │
    │  }                                                                                       │  │
    │  → Speculation prevented, bounds check validated before access                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Spectre 변이 비교

| 변이 | 공격 | 취약점 | 완화 |
|------|------|--------|------|
| **V1** | Bounds check | Same process | LFENCE |
| **V2** | indirect branch | Cross-process | RETPOLINE |
| **V3** | Exception handling | Kernel memory | KPTI |
| **V4** | Speculative store | Same process | SSBD |

### KPTI (Kernel Page Table Isolation)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         KPTI (KAISER) Mitigation                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Before KPTI:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Single Page Table per Process                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User Process Page Table:                                                            │  │  │
    │  │  │  User Space (0x00000000 - 0x7FFFFFFF)  ────  User Code/Data                      │  │  │  │
    │  │  │  Kernel Space (0xFFFFFFFF80000000+) ────  Kernel Memory (MAPPED)                │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  → Meltdown can read kernel memory                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    After KPTI:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Two Page Tables per Process                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User Mode Page Table:                                                                 │  │  │
    │  │  │  User Space (0x00000000 - 0x7FFFFFFF)  ────  User Code/Data                      │  │  │  │
    │  │  │  Kernel Space (0xFFFFFFFF80000000+) ────  NOT MAPPED (empty)                     │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │                                                                                         │  │
    │  │  Kernel Mode Page Table:                                                                │  │  │
    │  │  │  User Space (0x00000000 - 0x7FFFFFFF)  ────  User Code/Data (mapped)              │  │  │  │
    │  │  │  Kernel Space (0xFFFFFFFF80000000+) ────  Kernel Memory (MAPPED)                │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → On system call: Switch to kernel page table (TLB flush)                              │  │
    │  → On return: Switch back to user page table (TLB flush)                                 │  │
    │  → Meltdown cannot read kernel memory (not mapped in user page table)                    │  │
    │  → Performance cost: TLB flush on every syscall (~5-10%)                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### RETPOLINE (Spectre V2 Mitigation)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RETPOLINE: Return Trampoline                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Indirect calls vulnerable to branch target injection
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Vulnerable indirect call                                                            │  │
    │  void (*func_ptr)();                                                                     │  │
    │  func_ptr();  // CPU speculates target based on history                                  │  │
    │  → Attacker can poison BTB to steer prediction to gadget code                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    RETPOLINE Solution:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Replace indirect call with return trampoline                                         │  │
    │  asm volatile (                                                                          │  │
    │      "call 1f\n"                      // Push return address, jump to label 1            │  │
    │      "1:\n"                                                                            │  │
    │      "capture_sp:\n"                                                                  │  │
    │      "   pause\n"                       // Hint CPU: spin (not speculative)               │  │
    │      "   lfence\n"                      // Serialize (alternative)                       │  │
    │      "   jmp capture_sp\n"              // Infinite loop until return resolves         │  │
    │      "2:\n"                                                                            │  │
    │      "   mov %0, (%1)\n"                 // Store target address on stack                │  │
    │      "   ret\n"                          // Return to target (safe)                        │  │
    │      :                                                                                   │  │
    │      : "r"(func_ptr), "r"(stack_slot)                                                    │  │
    │  );                                                                                      │  │
    │                                                                                         │  │
    │  → Return instruction uses RSB (Return Stack Buffer) which is not attacker-controlled  │  │
    │  → Indirect call converted to safe return instruction                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 클라우드 보안 강화
**상황**: 멀티테넌트 환경
**판단**: CPU 마이크로코드 + OS 패치

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Cloud Provider Mitigation                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Required Actions:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Microcode Update (Intel/AMD)                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • IBRS (Indirect Branch Restricted Speculation)                                   │  │  │
    │  │  • STIBP (Single Thread Indirect Branch Predictors)                                 │  │  │
    │  │  • SSBD (Speculative Store Bypass Disable)                                          │  │  │
    │  │  → Updates delivered via BIOS/firmware or OS loader                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. OS Patches                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Linux: KPTI (Kernel Page Table Isolation), PTI                                    │  │  │
    │  │  • Windows: Kernel VA Isolation, Retpoline                                          │  │  │
    │  │  • macOS: KPTI equivalent                                                             │  │  │
    │  │  → Requires reboot to activate                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. Compiler Patches                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • GCC/Clang: -mretpoline, -mlfence                                                    │  │  │
    │  │  • Recompile all applications for full protection                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  4. Application Changes (Constant-Time Programming)                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Avoid data-dependent branches                                                     │  │  │
    │  │  • Use bitwise operations instead of conditional logic                              │  │  │
    │  │  • Flush cache after sensitive operations                                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 완화 방법 기대 효과

| 완화 | 성능 영향 | 보안 효과 |
|------|----------|----------|
| **KPTI** | 5-30% | Meltdown |
| **RETPOLINE** | 5-15% | Spectre V2 |
| **LFENCE** | 3-10% | Spectre V1 |
| **SSBD** | 2-5% | Spectre V4 |

### 모범 사례

1. **패치**: 즉시 적용
2. **모니터링**: 공격 탐지
3. **격리**: 민감 데이터
4. **암호화**: 추가 보호

### 미래 전망

1. **Hardware**: CET, ARM PAC
2. **ISA**: BTI, SCI
3. **Formal verification**: 사이드 채널 증명
4. **Quantum**: 내성성

### ※ 참고 표준/가이드
- **Intel**: Speculative Execution Side Channel
- **ARM**: Spectre/BHB
- **Google**: Project Zero

---

## 📌 관련 개념 맵

- [분기 예측](./15_branch_prediction/130_branch_prediction.md) - BTB
- [캐시](./7_cache/87_cache.md) - 사이드 채널
- [보안](../../9_security/71_system_security.md) - 하드웨어 보안
