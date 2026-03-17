+++
title = "18. 소프트웨어 인터럽트/트랩 (Software Interrupt/Trap)"
date = 2026-03-05
categories = ["studynotes-operating-system"]
tags = ["Software-Interrupt", "Trap", "Exception", "System-Call", "Operating-System"]
draft = false
+++

# 소프트웨어 인터럽트/트랩 (Software Interrupt/Trap)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 인터럽트(Trap)는 실행 중인 프로그램이 의도적(intentional) 또는 비의도적(unintentional)으로 발생시키는 동기적(Synchronous) 이벤트로, 시스템 호출(System Call)과 예외(Exception) 처리의 핵심 메커니즘이다.
> 2. **가치**: 사용자 모드(User Mode)에서 커널 모드(Kernel Mode)로의 안전한 진입 경로를 제공하며, 하드웨어 인터럽트와 유사한 처리 메커니즘을 공유하여 OS 코드의 모듈성과 일관성을 보장한다.
> 3. **융합**: 시스템 호출 인터페이스, 예외 처리(Debugger, Fault), 커널 모드 전환과 밀접하게 연계되며, 현대 OS의 보안 경계(Security Boundary)와 가상화(Virtualization)의 기초가 된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
소프트웨어 인터럽트(Software Interrupt), 일반적으로 **트랩(Trap)**은 CPU가 명령어를 실행하는 과정에서 프로그램 자신의 연산에 의해 발생하는 동기적 이벤트이다. 하드웨어 인터럽트가 외부 장치의 비동기적 신호인 반면, 트랩은 명령어 실행의 직접적인 결과로 발생하며 발생 시점이 예측 가능하다.

### 💡 비유
트랩은 **"책을 읽다가 모르는 단어가 나와서 사전을 찾으러 가는 행위"**와 같다.
- **예상 가능한 트랩(시스템 호출)**: 모르는 단어를 의도적으로 찾아보는 것 (계획된 행위)
- **예상 불가능한 트랩(예외)**: 책 페이지가 찢어져서 읽을 수 없는 상황 (예기치 않은 사건)
- **핸들러**: 사전을 찾아 뜻을 확인하고 다시 돌아와 읽기 계속 (OS 커널 처리)

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 한계
- **직접 하드웨어 접근 위험**: 사용자 프로그램이 하드웨어를 직접 제어하면 시스템 전체의 안정성 위협
- **모드 전환 필요**: 사용자 모드에서 커널 모드로 안전하게 진입할 메커니즘 부족
- **예외 처리의 통합**: 다양한 오류 상황을 일관된 방식으로 처리할 필요성

#### 2. 패러다임 변화
- **1960년대**: 초기 시스템 콜(Supervisor Call) 명령어 도입 (IBM System/360 SVC)
- **1970년대**: 유닉스에서 trap/int 0x80 기반 시스템 호출 구현
- **1980년대**: x86 INT 명령어, 소프트웨어 인터럽트 벡터 표준화
- **1990년대**: IA-32에서 sysenter/sysexit, syscall/sysret 기반 빠른 시스템 호출
- **현재**: SYSCALL/SYSRET, VDSO(Virtual Dynamic Shared Object) 기반 최적화

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|--------|-----------|-------------------|-----------|------|
| **트랩 명령어** | 커널 진입 요청 | INT n, SYSCALL, sysenter | x86 INT 0x80, syscall | 초인종 |
| **IDT 항목** | 트랩 핸들러 주소 | Trap Gate, Task Gate | IDTR 레지스터 | 주소록 |
| **예외 핸들러** | 오류 처리 루틴 | Fault, Abort, Trap 처리 | Page Fault Handler | 수리공 |
| **시스템 호출 테이블** | 서비스 디스패치 | syscall number → handler 함수 | sys_call_table[] | 서비스 안내 |
| **스택 프레임** | 문맥 저장 | User Stack → Kernel Stack | SS, ESP, EFLAGS push | 상자 보관 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    Software Interrupt/Trap 처리 아키텍처                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    User Mode                  Kernel Mode                 Hardware
      │                           │                           │
      │  [User Program]           │                           │
      │  ┌─────────────────────┐   │                           │
      │  │  application code   │   │                           │
      │  │  ...                │   │                           │
      │  │  INT 0x80 or syscall│───┼───────────────────────────┼────┐
      │  └─────────────────────┘   │                           │    │
      │                           │                           │    ▼
      │                           │    [Exception Entry]       ┌──────────────────┐
      │                           │    ┌─────────────────┐     │  CPU Control     │
      │                           │    │  IDT Lookup      │◄────┤  - Privilege    │
      │                           │    │  Vector #0x80    │     │    Check         │
      │                           │    └────────┬─────────┘     │  - Mode Switch    │
      │                           │             │               │  - Stack Switch  │
      │                           │             ▼               └──────────────────┘
      │                           │    [System Call Handler]   [IDT: Interrupt Descriptor Table]
      │                           │    ┌─────────────────┐     ┌─────────────────────────────┐
      │                           │    │  Save Context   │     │ Vector 0x00: Divide Error   │
      │                           │    │  - SS, ESP       │     │ Vector 0x01: Debug          │
      │                           │    │  - EFLAGS, CS,   │     │ Vector 0x02: NMI            │
      │                           │    │    EIP           │     │ Vector 0x03: Breakpoint     │
      │                           │    └────────┬─────────┘     │ ...                         │
      │                           │             │               │ Vector 0x80: System Call    │
      │                           │             ▼               │ Vector 0x80: → syscall_handler│
      │                           │    [Dispatch]             └─────────────────────────────┘
      │                           │    ┌─────────────────┐
      │                           │    │  sys_call_table │
      │                           │    │  [eax] → handler│
      │                           │    └────────┬─────────┘
      │                           │             │
      │                           │    ┌─────────▼────────────┐
      │                           │    │  Specific Handler     │
      │                           │    │  (read, write, fork)  │
      │                           │    └─────────┬────────────┘
      │                           │             │
      │                           │    [Kernel Service Execute]
      │                           │    ┌─────────────────┐
      │                           │    │  Requested      │
      │                           │    │  Operation      │
      │                           │    └────────┬─────────┘
      │                           │             │
      │                           │    [Return to User Mode]
      │                           │    ┌─────────────────┐
      │                           │    │  iret/sysret    │
      │                           │    │  Restore Context│
      │                           │    └────────┬─────────┘
      │                           │             │
      │  ◄─────────────────────────┼─────────────┘
      │  [Return to User Code]
      │  ┌─────────────────────┐
      │  │  continue execution │
      │  └─────────────────────┘
```

### 심층 동작 원리

#### 1. 트랩의 분류

**의도적 트랩 (Intentional Trap)**:
- **시스템 호출(Syscall)**: 커널 서비스 요청
- **디버깅(Breakpoint)**: INT 3, 프로그램 실행 중단
- **트레이싱(Single-step)**: TF 플래그, 명령어 단위 실행

**비의도적 트랩 (Unintentional Trap/Exception)**:
- **Fault(결함)**: 복구 가능, 수정 후 재실행 (Page Fault)
- **Trap(트랩)**: 복구 가능, 다음 명령어 실행 (Debug trap)
- **Abort(중단)**: 복구 불가, 프로세스 종료 (Machine Check)

#### 2. 시스템 호출 처리 과정

**x86 리눅스 예시**:
```text
사용자 공간:
    eax = 시스템 호출 번호 (예: __NR_write = 4)
    ebx, ecx, edx = 인자들
    int 0x80            ← 소프트웨어 인터럽트 발생

커널 공간 (entry_8064.S):
    1. IDT[0x80] → system_call 핸들러
    2. 사용자 스택 → 커널 스택 전환
    3. 레지스터 저장 (SAVE_ALL)
    4. sys_call_table[eax] 호출
    5. 서비스 루틴 실행 (sys_write)
    6. 반환값 → eax
    7. iret (사용자 모드 복귀)
```

**syscall/sysret (AMD64)**:
- 모델 특정 레지스터(MSR)을 통해 핸들러 주소 지정
- sysenter보다 빠르고 안전한 모드 전환
- SYSCALL64/SYSRET64 쌍 사용

#### 3. 예외(Exception) 처리

**Page Fault 처리**:
```text
1. 가상 주소 접근 → TLB 미스
2. 페이지 테이블 탐색 → Present 비트 = 0
3. #PF 예외 발생 (Vector 14)
4. 페이지 폴트 핸들러 실행
5. 디맨드 페이징(demand paging) 처리
   - 필요한 페이지를 디스크에서 로드
   - 프로세스 재개
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 심층 기술 비교표

| 특성 | 하드웨어 인터럽트 | 소프트웨어 인터럽트(Trap) |
|------|------------------|-------------------------|
| **발생 원인** | 외부 장치 신호 | 명령어 실행 결과 |
| **동기성** | 비동기적(Asynchronous) | 동기적(Synchronous) |
| **예측 가능성** | 예측 불가능 | 예측 가능(Trap) / 불가능(Exception) |
| **발생 시점** | 명령어 실행 중/후 | 명령어 실행 경계 |
| **처리 반환** | 같은 위치 복귀 | 같은 위치(Fault) or 다음 위치(Trap) |
| **주요 용도** | I/O 완료 알림 | 시스템 호출, 예외 처리 |
| **우선순위** | 낮음 ~ 중간 | 높음 |

### 과목 융합 관점 분석

#### 1. 컴퓨터 구조 ↔ 트랩
- **명령어 집합**: INT, SYSCALL, SYSENTER 명령어 설계
- **파이프라인**: 트랩 발생 시 파이프라인 플러시(Flush)
- **분기 예측**: 예측 불가능한 트랩이 성능에 미치는 영향

#### 2. 프로세스 관리 ↔ 트랩
- **시스템 호출**: fork(), exec(), wait() 등 프로세스 생성/제어
- **시그널**: SIGSEGV, SIGILL 등 예외 기반 시그널 전송
- **모드 전환**: 사용자 모드 ↔ 커널 모드 전환 오버헤드

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 시스템 호출 오버헤드 최적화
**상황**: 고빈도 시스템 호출이 병목인 마이크로서비스 환경
**판단**:
- INT 0x80 방식은 레거시 x86에서만 사용
- AMD64에서는 syscall/sysret 필수 사용
- VDSO(Virtual DSO)를 통해 gettimeofday 등을 사용자 공간에서 처리
- io_uring 등 리눅스 최신 기술로 시스템 호출 최소화

### 도입 시 고려사항 (체크리스트)

**기술적**:
- [ ] 트랩 핸들러에서 재진입(Reentrant) 불가능 제약 확인
- [ ] 스택 오버플로우 방지를 위한 커널 스택 크기
- [ ] 예외 처리의 지연 시간(Latency) 최소화

**운영적**:
- [ ] 예외 발생 빈도 모니터링 (/proc/interrupts)
- [ ] 커널 패닉(Kernel Panic) 대응 매뉴얼

### 주의사항 및 안티패턴

1. **트랩 핸들러 내 무한 루프**: 시스템 정지(Hang) 유발
2. **중첩된 예외**: Double Fault, Triple Fault → 시스템 리셋
3. **사용자 공간 포인터 검증 누락**: 커널 메모리 손상 가능성

---

## Ⅴ. 기대효과 및 결론

### 정량적/정성적 기대효과

| 지표 | 하드웨어 인터럽트 | 트랩(시스템 호출) | 비고 |
|------|------------------|------------------|------|
| 오버헤드 | 중간 | 낮음 ~ 중간 | SYSCALL 최적화 |
| 예측 가능성 | 불가능 | 가능 | 컴파일러 최적화 |
| 처리 지연 | 마이크로초 ~ 밀리초 | 나노초 ~ 마이크로초 | |
| 보안 검증 | IRQ별 | 사용자 검증 필요 | 파라미터 검증 |

### 미래 전망

1. **VDSO (Virtual Dynamic Shared Object)**: 시스템 호출을 사용자 공간으로 이전
2. **io_uring**: 비동기 I/O를 위한 새로운 인터페이스
3. **eBPF**: 커널 내 안전한 프로그래밍, 트랩 핸들러 사용자 정의

### ※ 참고 표준/가이드
- **Intel SDM Vol. 3A**: Chapter 6 (Interrupt and Exception Handling)
- **AMD64 Architecture Programmer's Manual**: Exception and Interrupt
- **POSIX 1003.1**: 시스템 호출 인터페이스 표준

---

## 📌 관련 개념 맵

- [하드웨어 인터럽트](./17_hardware_interrupt.md) - 외부 인터럽트 처리
- [모드 비트](./12_mode_bit.md) - 사용자/커널 모드 구분
- [시스템 호출](./13_system_call.md) - 시스템 호출 인터페이스
- [프로세스 상태](../2_process_thread/) - 트랩에 의한 상태 변화

---

## 👶 어린이를 위한 3줄 비유 설명

소프트웨어 인터럽트(트랩)은 **"선생님 손 들기 질문"**이에요.

1. **의도적인 트랩**: 선생님께 질문하려면 손을 들어야 해요. 그래야 선생님(커널)이 답변해 주세요.
2. **예상치 못한 트랩(예외)**: 공부하다가 갑자기 책이 찢어지거나 친구가 다치면, 선생님이 바로 와서 도와줘야 해요.
3. **결과**: 트랩이 발생하면 우리 공부(프로그램)는 잠깐 멈췄다가, 선생님의 도움을 받고 다시 계속할 수 있어요!
