+++
title = "14. 인터럽트 (Interrupt)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Interrupt", "ISR", "Hardware-Interrupt", "Software-Interrupt", "Exception", "Interrupt-Controller"]
draft = false
+++

# 인터럽트 (Interrupt)

```text
Interrupt line becomes active
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │  Controller sends signal to CPU                                                       │
  │                                                                                         │
  │  [2. CPU Acknowledgement]                                                               │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │  CPU: • Finishes current instruction                                               │  │
  │  │      • Checks interrupt pin                                                        │  │
  │  │      • Sends INTA (Interrupt Acknowledge)                                         │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  │                              │                                                          │
  │                              ▼                                                          │
  │  [3. Interrupt Vector Transfer]                                                       │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │  PIC puts interrupt vector on data bus                                            │  │
  │  │  • Example: IRQ 0 → Vector 32 (Timer)                                               │  │
  │  │  • IRQ 1 → Vector 33 (Keyboard)                                                    │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  │                              │                                                          │
  │                              ▼                                                          │
  │  [4. Context Save]                                                                     │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │  CPU automatically pushes:                                                         │  │
  │  │  • SS (Stack Segment)                                                               │  │
  │  │  • ESP (Stack Pointer)                                                               │  │
  │  │  • EFLAGS (Status Register)                                                         │  │
  │  │  • CS, EIP (Return Address)                                                          │  │
  │  │  → Stack now contains execution context to restore later                             │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  │                              │                                                          │
  │                              ▼                                                          │
  │  [5. ISR Execution]                                                                     │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │  CPU jumps to ISR address based on interrupt vector:                                │  │
  │  │  • IDT[Vector] → ISR Address                                                          │  │
  │  │  • Example: Timer Interrupt → timer_isr()                                            │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  │                              │                                                          │
  │                              ▼                                                          │
  │  [6. IRET (Return from Interrupt)]                                                      │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │  ISR completes with IRET instruction:                                               │  │
  │  │  • Pops saved context (EIP, CS, EFLAGS, ESP, SS)                                    │  │
  │  │  • Execution resumes at interrupted instruction                                      │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Exception vs Interrupt

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Exception과 Interrupt 비교                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  구분              │  Exception        │  Interrupt                                 │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  발생 원인         │  CPU 내부        │  CPU 외부 (하드웨어)                        │
    │  예시              │  Divide by Zero,  │  Timer, Keyboard, Network                  │
    │                    │  Page Fault,      │                                             │
    │                    │  Invalid Opcode   │                                             │
    │  동기/비동기       │  동기             │  비동기                                      │
    │  발생 위치         │  명령어 실행 중   │  명령어 실행 완료 후                       │
    │  처리              │  ISR 또는 Trap     │  ISR                                         │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Polled I/O vs Interrupt-Driven I/O

| 구분 | Polled I/O | Interrupt-Driven |
|------|-----------|-----------------|
| **CPU 활용** | 낮음 (busy waiting) | 높음 |
| **응답 시간** | 일정 | 변동 |
| **복잡도** | 낮음 | 높음 |
| **적용** | 간단한 시스템 | 범용 시스템 |

### 과목 융합 관점 분석

#### 1. 운영체제 ↔ 인터럽트
- **System Call**: Software Interrupt (INT 0x80)
- **Scheduler**: Timer Interrupt
- **Device Driver**: ISR 구현

#### 2. 임베디드 ↔ 인터럽트
- **ARM NVIC**: Nested Vectored Interrupt Controller
- **Priority Levels**: 0~255
- **Interrupt Latency**: 실시간 성능

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 인터럽트 지연 최소화
**상황**: 실시간 시스템
**판단**:

```c
// 인터럽트 처리 최적화

// 1. ISR을 짧게 유지
void timer_isr(void) {
    // 최소한의 작업만 수행
    flag = 1;  // 플래그만 설정

    // 나중에 메인 루프에서 처리
}

// 2. Bottom Halves (Linux)
// - Softirq: 고우선순위, 빠름
// - Tasklet: Softirq 기반
// - Workqueue: 프로세스 컨텍스트

// 3. Interrupt Affinity
// CPU 특정 코어에 인터럽트 할당
$ echo 2 > /proc/irq/24/smp_affinity_list

// 4. Priority Inheritance
// 우선순위 역전 방지
```

---

## Ⅴ. 기대효과 및 결론

### 인터럽트 기대 효과

| 효과 | Polling | Interrupt |
|------|---------|-----------|
| **CPU 효율** | 낮음 | 높음 |
| **응답 시간** | 일정하지만 느림 | 빠름 |
| **시스템 부하** | 높음 (CPU) | 중간 (버스) |
| **구현 복잡도** | 낮음 | 높음 |

### 미래 전망

1. **Message Signaled Interrupts (MSI)**: 메모리 매핑
2. **APIC**: 다중 프로세서 지원
3. **ARM GIC**: 복수 인터럽트

### ※ 참고 표준/가이드
- **Intel SDM**: Vol 3A (Interrupt)
- **ARM GIC**: Generic Interrupt Controller
- **x86**: IDT, ISR

---

## 📌 관련 개념 맵

- [문맥 교환](../2_process_thread/83_context_switch.md) - ISR와 연계
- [PCB](../2_process_thread/88_pcb.md) - 컨텍스트 저장
- [예외 처리](./105_exception.md) - Exception
- [DMA](./106_dma.md) - I/O 최적화
