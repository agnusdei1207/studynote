+++
title = "인터럽트 (Interrupt)"
date = "2026-03-14"
weight = 315
+++

# # [Interrupt] 인터럽트 시스템 아키텍처

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인터럽트(Interrupt)는 **CPU (Central Processing Unit)**의 정상 명령어 실행 흐름을 비동기적(Asynchronous) 또는 동기적(Synchronous) 이벤트에 의해 강제로 중단시키고, 제어를 커널 모드로 전환하여 우선 처리를 수행하는 하드웨어 및 소프트웨어 제어 메커니즘이다.
> 2. **가치**: 폴링(Polling) 방식의 **CPU (Central Processing Unit)** 사이클 낭비를 근본적으로 제거하여 시스템 응답성(Response Time)을 최적화하고, 다중 프로그래밍(Multiprogramming) 환경에서 **I/O (Input/Output)** 장치와의 병행 처리(Concurrency)를 가능하게 하는 현대 운영체제의 핵심 인프라이다.
> 3. **융합**: **DMA (Direct Memory Access)**와 연계하여 대용량 데이터 전송 시의 오버헤드를 최소화하고, **ISR (Interrupt Service Routine)** 내에서의 스케줄링(Scheduling) 및 가상 메모리(Virtual Memory) 페이징(Paging) 기능을 트리거하는 소프트웨어적인 트리거 역할을 수행한다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 정의**
인터럽트(Interrupt)는 **CPU (Central Processing Unit)**가 프로그램을 실행하는 도중에 긴급한 일이 발생하여 현재 수행 중인 명령어의 처리를 중단하고, 발생한 이벤트를 먼저 처리한 뒤 복귀하는 시스템 제어 기법이다. 이는 마치 직장인이 업무 중에 긴급 전화를 받기 위해 자리를 비웠다가 다시 업무로 복귀하는 것과 유사하다. 하지만 컴퓨터 시스템에서 이 동작은 나노초(ns) 단위의 매우 정교한 하드웨어 신호와 소프트웨어 로직에 의해 수행된다.

**등장 배경: 폴링(Polling)의 한계와 비효율**
초기의 컴퓨터 시스템은 **PIO (Programmed I/O)** 방식을 사용했다. **CPU (Central Processing Unit)**가 데이터 입출력을 위해 **I/O (Input/Output)** 컨트롤러의 상태 레지스터(Status Register)를 반복적으로 읽어(Retry Loop) "작업이 완료되었는가?"를 묻는 방식이었다. 이를 폴링(Polling) 또는 바쁜 대기(Busy Waiting)라고 한다. 이 방식은 데이터가 준비되지 않았을 때도 **CPU (Central Processing Unit)**가 무의미한 사이클을 소모하여 시스템 전체의 처리량(Throughput)을 급격히 떨어뜨리는 치명적인 결함이 있었다. 이를 해결하기 위해 **I/O (Input/Output)** 장치가 준비되었을 때 **CPU (Central Processing Unit)**에게 능동적으로 신호를 보내는 인터럽트 기반 시스템(Interrupt-driven System)이 도입되었다.

**기술적 파급 효과**
인터럽트의 도입은 단순히 **CPU (Central Processing Unit)**의 효율성을 높이는 것을 넘어, 현대 운영체제(OS)의 시분할(Time Sharing) 시스템을 가능하게 했다. **OS (Operating System)**는 타이머 인터럽트를 이용해 프로세스를 강제로 전환(Preemption)하여 다중 사용자에게 서비스를 제공하며, **MMU (Memory Management Unit)**의 페이지 부(Page Fault) 인터럽트를 통해 가상 메모리를 구현한다. 즉, 인터럽트 없이는 현대의 멀티태스킹(Multitasking) 환경 자체가 성립될 수 없다.

> 📢 **섹션 요약 비유**
> 요리사(CPU)가 오븐 앞에서 빵이 다 익었는지 1초에 한 번씩 계속 확인하느라 다른 요리를 못 하는(폴링 방식) 대신, 오븐에서 '띠동' 알람(인터럽트)이 울릴 때까지 다른 요리를 하다가 알람이 울리면 재빨리 달려가 빵을 꺼내는(인터럽트 기반) 것이 식당의 업무 효율을 극대화하는 방식입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

인터럽트 처리 과정은 하드웨어적인 신호 감지와 소프트웨어적인 문맥 교환(Context Switching)이 결합된 정교한 루틴이다. 이 과정은 크로스바 스위치(Crossbar Switch)나 **PIC (Programmable Interrupt Controller)**와 같은 컨트롤러, **CPU (Central Processing Unit)**의 명령어 사이클, 그리고 커널의 **ISR (Interrupt Service Routine)**이 유기적으로 작동한다.

#### 1. 구성 요소 상세 분석
인터럽트 시스템을 구성하는 핵심 요소는 최소 5가지 이상의 모듈로 세분화된다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/버스 (Protocol/Bus) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Interrupt Source** | 이벤트 발생 주체 | 하드웨어 신호 전송(상승 에지), 소프트웨어 `INT` 명령어 실행 | IRQ Line, SW Instruction | 벨을 누르는 손님 |
| **PIC (Programmable Interrupt Controller)** | 중재 및 우선순위 판정 | 다중 IRQ를 수집하여 우선순위 인코딩, CPU에 단일 INTR 신호 송신 | APIC Bus, IRQ Vector Assignment | 전화 교환기(교환원) |
| **CPU (Central Processing Unit)** | 명령어 흐름 제어 | 명령어 사이클 종료 시 인터럽트 플래그(IF) 체크, 인터럽트 확인(ACK) 신호 전송 | System Bus, Control Signals | 업무 중인 사장님 |
| **IVT (Interrupt Vector Table)** | 주소 매핑 테이블 | 인터럽트 벡터 번호를 인덱스로 하여 해당 ISR의 메모리 주소 반환 | Memory Read (Physical Address) | 긴급 연락처 주소록 |
| **ISR (Interrupt Service Routine)** | 실제 처리 로직 | 레지스터 백업(PUSH), I/O 처리, 레지스터 복구(POP), IRET 명령어로 복귀 | Kernel Code Execution | 긴급 상황 처리반 |

#### 2. 인터럽트 처리 파이프라인 (ASCII 구조 다이어그램)

아래 다이어그램은 하드웨어 인터럽트가 발생했을 때, 사용자 모드(User Mode)의 프로세스가 커널 모드(Kernel Mode)로 전환되었다가 다시 복귀하기까지의 전체적인 흐름을 도식화한 것이다.

```text
[TIME FLOW]      User Process (Task A)                     Hardware/Kernel (Interrupt Context)
                  (Status: Running)                         (Status: Ready/Handled)
  ------------------------------------------------------------------------------------------
  1. Normal Exec  [Instruction i-1] --> [Instruction i] --> [Fetch Next Instruction]
                                                       |
                                          | [HARDWARE SIGNAL: IRQ Line asserted by Device]
                                          v
  2. Check Cycle  <--- [Interrupt Check Phase (End of Instruction Cycle)]
                  |
                  |--- CPU sends INTA (Interrupt Acknowledge) to PIC --->
                  |                                                              |
                  |<-- PIC returns Vector Number (e.g., 0x21) -------------------+
                  v
  3. Context Save [Implicit Context Switch by Hardware]
                  - CPU automatically saves PC (EIP), CS (Code Segment), Flags (EFLAGS)
                  - CPU switches to Kernel Stack (using Task State Segment or Stack Switch)
                  v
  4. Vectoring    [Lookup IVT/IDT] --> (Vector 0x21) --> Find ISR Address (e.g., 0xKERN_0821)
                                                                          |
                  -------------------------------------------------------->
                                                                    v
  6. ISR Exec     (Waiting...)                                [ISR: Keyboard Handler]
                                                                      - PUSH All Registers (General)
                                                                      - Read Scan Code from I/O Port
                                                                      - Convert to ASCII & Buffer to OS
                                                                      - EOI (End of Interrupt) to PIC
                                                                      - POP All Registers
                                                                      - IRET (Interrupt Return) Instruction
                  <-------------------------------------------------------
                  v
  7. Restore      [Implicit Context Restore by Hardware via IRET]
                  - Restore PC, CS, Flags
                  - Switch back to User Stack
                  v
  8. Resume       [Instruction i+1] --> [Instruction i+2] ...
                  (User Process continues exactly as if nothing happened)
```

#### 3. 심층 동작 원리 및 데이터 흐름
1.  **신호 발생 및 인지 (Interrupt Request & Check)**: 외부 장치(키보드 등)가 **PIC (Programmable Interrupt Controller)**의 핀에 신호를 보내면, **PIC (Programmable Interrupt Controller)**는 이를 우선순위에 따라 큐에 넣고 **CPU (Central Processing Unit)**의 INTR 핀을 활성화한다. **CPU (Central Processing Unit)**는 현재 실행 중인 명령어(Instruction)가 완전히 수행된 직후, 다음 명령어를 인출(Fetch)하기 전에 매 사이클마다 인터럽트 요청이 있는지 확인한다.
2.  **벡터 테이블 매핑 (Vectoring)**: **CPU (Central Processing Unit)**가 인터럽트를 승인(Acknowledge)하면, **PIC (Programmable Interrupt Controller)**는 데이터 버스를 통해 '인터럽트 벡터 번호(Interrupt Vector Number)'를 **CPU (Central Processing Unit)**에 전달한다. **CPU (Central Processing Unit)**는 이 번호를 인덱스로 하여 메모리(보통 0번지 혹은 **IDT (Interrupt Descriptor Table)**)에 위치한 **IVT (Interrupt Vector Table)**를 참조하여, 해당 이벤트를 처리하는 **ISR (Interrupt Service Routine)**의 메모리 주소를 로드한다.
3.  **문맥 교환 및 커널 진입 (Context Switch & Mode Switch)**: 하드웨어는 자동으로 현재의 **PC (Program Counter)**, 레지스터 상태(**EFLAGS**) 등을 **PCB (Process Control Block)**나 커널 스택(Kernel Stack)에 저장한다. 이때 권한 레벨(Ring 3 -> Ring 0)이 변경되며 사용자 모드에서 커널 모드로 전환된다.
4.  **서비스 루틴 실행 (Execution)**: **ISR (Interrupt Service Routine)**이 실행된다. 이때 하드웨어가 자동으로 저장하지 않는 범용 레지스터들(AX, BX 등)은 소프트웨어적으로 명시히 스택에 저장(PUSH)해야 한다. 실제 작업(데이터 읽기, 페이지 테이블 갱신 등)을 수행한 후 **EOI (End of Interrupt)** 명령어를 **PIC (Programmable Interrupt Controller)**에 보내 인터럽트 처리가 끝났음을 알린다.
5.  **복귀 (Return)**: `IRET` (Interrupt Return) 명령어가 실행되면, 저장해 두었던 **PC (Program Counter)**와 레지스터를 복원하고 원래의 명령어 흐름으로 되돌아간다.

> 📢 **섹션 요약 비유**
> 책을 읽다가(실행 중인 프로세스) 긴급 전화(인터럽트 요청)가 오면, 나는 지금 읽던 페이지 번호와 책갈피 위치를 메모장에 적어두고(상태 저장 Context Saving), 전화번호부(벡터 테이블)를 보고 해당 상담원(ISR)의 번호로 연결하여 상담을 받습니다. 상담이 끝나면 적어둔 메모장(스택)을 보고 다시 그 페이지로 돌아가 책을 읽는(복귀 Restore) 것과 같습니다. 이 모든 과정이 순식간에 일어나지만, 긴급 전화를 못 받으면(인터럽트 불능) 큰 일이 생기듯 시스템은 항상 대기 상태를 유지합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

인터럽트는 단순히 "신호"라는 개념을 넘어, 시스템의 다양한 계층(Layer)에서 발생하는 이벤트를 어떻게 분류하고 처리할지에 대한 철학이 담겨 있다. 이를 발생 시점과 주체에 따라 정량적으로 비교 분석한다.

#### 1. 인터럽트의 분류 및 상세 비교표

| 구분 (Classification) | 하드웨어 인터럽트 (Hardware Interrupt) | 소프트웨어 인터럽트 (Software Interrupt) / 예외 (Exception) |
|:---|:---|:---|
| **별칭 (Alias)** | 외부 인터럽트 (External Interrupt) | 내부 인터럽트 (Internal), Trap, SVC (Supervisor Call) |
| **발생 주체 (Source)** | **I/O (Input/Output)** 장치, 타이머, 전원 회로 등 외부 HW | 실행 중인 명령어(Instruction) 자체, 프로그램 코드 |
| **발생 시점 (Timing)** | 명령어 실행과 무관하게 비동기적(Asynchronous) 발생 가능 | 명령어 실행 중 동기적(Synchronous) 발생 (정확히 지점이 존재) |
| **주요 예시 (Examples)** | 키보드 입력, 마우스 클릭, 네트워크 패킷 수신, 디스크 I/O 완료 | 0으로 나누기(Divide Error), 페이지 부재(Page Fault), 시스템 콜(`INT 0x80`) |
| **CPU 개입(CPU Intervention)** | 현재 명령어가 끝난 직후 즉시 반응 | 예외는 명령어 실패 시 즉시, 시스템 콜은 명시적 호출 시 |
| **처리 소프트웨어 (Handler)** | **ISR (Interrupt Service Routine)** (Device Driver 영역) | Exception Handler, System Call Handler (Kernel 영역) |
| **제어 가능성 (Control)** | **PIC (Programmable Interrupt Controller)**를 통해 우선순위 제어, 마스킹 가능 | 치명적 에류(Fault)는 불가항, 시스템 콜은 의도적 호출 |

#### 2. 폴링(Polling) 대비 인터럽트(Interrupt) 방식의 융합 분석
OS 및 컴퓨터 구조 관점에서 인터럽트와 폴링은 상호 배타적이며, 상황에 따른 트레이드오프(Trade-off)가 존재한다.

```text
+------------------+---------------------------+---------------------------+
|    Metric        |  Polling (Busy Waiting)   |  Interrupt (Event Driven) |
+------------------+---------------------------+---------------------------+
| CPU Utilization | Low (데이터 없을 때 Loop)  | High (다른 작업 가능)      |
|                 |                           |                           |
| Latency         | Deterministic (Loop 주기) | Variable (처리 우선순위    |
|                 |                           | 및 ISR 로딩에 따라 달라짐) |
|                 |                           |                           |
| Throughput      | Low (CPU 낭비)            | High (최적화된 처리)       |
|                 |                           |                           |
| Implementation  | Simple (Loop only)        | Complex (HW support, ISR) |
|                 |