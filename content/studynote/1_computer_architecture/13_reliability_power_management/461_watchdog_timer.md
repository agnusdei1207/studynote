+++
title = "워치독 타이머 (Watchdog Timer)"
date = "2026-03-14"
weight = 461
+++

# 🧠 브레인 사이언스 PE 가이드라인: 워치독 타이머 (Watchdog Timer)

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: WDT (Watchdog Timer)는 MCU (Microcontroller Unit)의 정상 동작을 감시하는 독립된 하드웨어 카운터로, 시스템이 정해진 시간 내에 '킥(Kick)' 신호를 보내지 않으면 자동으로 하드웨어 리셋(Hardware Reset)을 발생시켜 시스템을 복구하는 최후의 안전장치입니다.
> 2. **가치**: 무인 감시 시스템이나 원격지 임베디드 장비에서 소프트웨어적 교착 상태(Deadlock)나 무한 루프(Infinite Loop)로 인한 다운 타임(Downtime)을 방지하여, 하드웨어적 수준의 복원력(Resilience)과 가용성(Availability)을 극대화합니다.
> 3. **융합**: 단순한 타이머를 넘어 OS (Operating System)의 hang-up 감지, 보안 시스템의 무결성 검증, 그리고 안전 임계(Safety-Critical) 시스템의 IEC 61508 표준 준수를 위한 핵심 요소로 발전하고 있습니다.

---

## Ⅰ. 개요 (Context & Background) - 워치독 타이머의 철학과 작동 원리

워치독 타이먤(WDT, Watchdog Timer)는 컴퓨터 시스템, 특히 임베디드 시스템에서 소프트웨어 오류로 인한 시스템 멈춤(Hang-up)을 감지하고 자동으로 복구하는 하드웨어 모듈입니다. 이는 인간의 개입이 불가능한 환경에서 시스템의 신뢰성을 보장하는 필수적인 기술입니다.

### 1. 개념 및 정의
WDT는 일정 주기로 카운트를 증가시키는 타이머로, 시스템이 정상적으로 동작하고 있다면 이 타이머가 만료(Timeout)되기 전에 소프트웨어가 명시적으로 타이머 값을 초기화(Reset/Clear)해야 합니다. 이 초기화 동작을 흔히 **"킥 더 독(Kick the Dog)"** 또는 **"독 밥 주기"**라고 표현합니다.
*   **정상(Normal) 상태**: 프로그램 카운터(PC)가 정상적인 흐름을 따르며 주기적으로 WDT 레지스터를 갱신함.
*   **비정상(Abnormal) 상태**: 인터럽트 비활성화, 무한 루프, 프로그램 카운터 오염 등으로 인해 WDT 갱신 코드가 실행되지 않음.

### 2. 등장 배경 및 필요성
초기의 컴퓨팅 환경에서는 운영자가 시스템을 수동으로 리셋할 수 있었으나, 우주 항공, 자율 주행차, 의료 기기, 원격 통신 장비 등 **Human-in-the-loop(사람 개입)가 불가능한 환경**으로 확장됨에 따라 자기 복구 능력이 필수적이 되었습니다. WDT는 이러한 환경에서 발생할 수 있는 **Transient Fault(일시적 결함)** 로 인한 시스템 정지를 막는 최후의 방어선입니다.

### 3. 동작 메커니즘 시각화
아래 다이어그램은 WDT의 시간 기반 동작 흐름을 도식화한 것입니다.

```ascii
시간 (Time)  ------------------------------------------------->
[Start]       [Kick]       [Kick]       [Fail!]       [Reset]
  |             |             |             |             |
  v             v             v             v             v
+---+         +---+         +---+         +---+         +---+
| 5 |         | 5 |         | 5 |         | 5 |         | 5 |  <-- WDT Counter
| 4 |         | 4 |         | 4 |         | 4 |         | 4 |
| 3 |         | 3 |         | 3 |         | 3 |         | 3 |
| 2 |         | 2 |         | 2 |         | 2 |         | 2 |
| 1 |         | 1 |         | 1 |         | 1 |         | 1 |
| 0 |         | 0 |         | 0 |         | 0 |         | 0 |
+---+         +---+         +---+         +---+         +---+
  ^             ^             ^             ^             ^
  |             |             |             |             |
System Watchdog Refresh  Refresh  Timeout   System
Alive  (Kick Dog)    (Kick Dog) (0 Reached) Reboot
```
*   **해설**: 시스템은 타이머가 0에 도달하기 전에 카운트를 다시 최대값(5)으로 되돌려야 합니다. 만약 4번째 시도에서 시스템이 멈춰 '킥'을 수행하지 못하면 카운터는 0이 되고 즉시 리셋 신호가 트리거됩니다.

> 📢 **섹션 요약 비유**:
> 혼자 살고 있는 독거 어르신의 식사 여부를 확인하는 복지 시스템과 같습니다. 정해진 시간(매일 점심)까지 냉장고를 열거나 식사를 했다는 신호('킥')를 보내지 않으면, 센터는 어르신이 쓰러졌다고 판단하여 119 구급대(리셋)를 자동으로 호출합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

WDT는 단순한 카운터가 아니라, 메인 시스템과 독립적인 클럭 소스와 리셋 경로를 가진 하드웨어 블록으로 설계되어야 합니다.

### 1. 구성 요소 상세 분석표

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/인터페이스 | 비유 (Analogy) |
|:---:|:---|:---|:---:|:---|
| **독립 클럭 소스**<br>(Independent Clock) | 메인 CPU 멈춤 시에도 WDT 구동 | RC Oscillator나 외부 Crystal 사용 | CLK_IN | 심장 박동기 배터리 |
| **프리스케일러**<br>(Prescaler) | 타임아웃 주기 설정 세분화 | 입력 클럭을 분주하여 카운터 속도 조절 | SCALER_REG | 초침/분침 기어 |
| **카운터 레지스터**<br>(Counter Register) | 감시 시간의 흐름 저장 | 클럭에 맞춰 감소 또는 증가 | WDT_CNT | 모래 시계 |
| **리셋 로직**<br>(Reset Logic) | 리셋 신호 생성 및 전파 | 카운터 언더플로우/오버플로우 시 트리거 | RST_OUT | 비상 브레이크 |
| **킥 인터페이스**<br>(Kick Interface) | SW와의 통신 창구 | 특정 주소 쓰기 시 카운터 초기화 | WDT_SR (Service Reg) | 경비원 호출 버튼 |

### 2. 하드웨어 연결 구조 및 흐름

```ascii
   [System Power Rails] --+-----------------------------+------------------+
                          |                             |                  |
                       [VCC]                         [VCC]              [VCC]
                          |                             |                  |
                          v                             v                  v
+-----------------------+   |   +----------------------------------------+   |
|        CPU Core       |   |   |         Watchdog Timer (WDT)           |   |
|   (Main Processor)    |   |   |                                        |   |
|                       |   |   |  +----------------------------------+  |   |
|  Application Code:    |   |   |  |  Clock Gen (Independent 32kHz RC) |  |   |
|  while(1) {           |   |   |  +----------------------------------+  |   |
|    system_tick();     |   |   |                |                     |   |
|    wdt_reset();  <----+---+---|----------------|                     |   |
|  }                    |       |                v                     |   |
+-----------------------+       |  +----------------------------------+  |   |
         ^                     |  |  Prescaler & Counter Logic (Down) |  |   |
         | (CPU Halt)          |  +----------------------------------+  |   |
         |                     |                |                     |   |
    [System Hang]             |                v                     |   |
                             |  +----------------------------------+  |   |
                             |  |   Comparison & Reset Generator    |  |   |
                             |  +----------------------------------+  |   |
                             |                |                     |   |
                             |                | (Timeout)            |   |
                             |                v                     |   |
                             |  +----------------------------------+  |   |
                             |  |     System Reset Control Logic    |  |   |
                             |  +----------------------------------+  |   |
                             |                |                     |   |
                             +----------------|---------------------+   |
                                              | (Hard Reset Signal)  |
                                              v                        v
                                         +------------------------------+
                                         |      Entire MCU Reset        |
                                         +------------------------------+
```
*   **해설**: 
    1.  **독립성**: WDT는 CPU가 멈추더라도 자체 클럭(Clock Gen)에 의해 동작해야 하므로 전원 라인이나 클럭 소스를 공유하지 않거나, 공유하더라도 LPO(Low Power Oscillator) 등을 통해 독립성을 유지해야 합니다.
    2.  **신호 경로**: `wdt_reset()` 명령은 메모리 맵 입출력(MMIO)을 통해 WDT의 서비스 레지스터에 값을 씁니다. 이 신호가 끊기면 카운터는 0이 되고, Reset Generator는 **NMI (Non-Maskable Interrupt)** 혹은 **HARD RESET** 신호를 MCU의 리셋 핀(RST)으로 직접 보냅니다.

### 3. 핵심 알고리즘 및 코드 구현
아래는 임베디드 시스템에서 WDT를 초기화하고 주기적으로 갱신하는 의사 코드(Pseudo-code)입니다. 이는 레지스터 수준의 접근을 보여줍니다.

```c
// [Register Definition]
#define WDT_LOAD_VAL   0xFFFF    // 최대 카운트 값 (Timeout 결정)
#define WDT_CTRL_BASE  0x40001000 // WDT 컨트롤 레지스터 베이스 주소
#define WDT_KEY        0x12345678 // KICK 비밀키 (잘못된 접근 방지)

volatile uint32_t * const pWDT_Counter = (uint32_t*)(WDT_CTRL_BASE + 0x00);
volatile uint32_t * const pWDT_Ctrl    = (uint32_t*)(WDT_CTRL_BASE + 0x08);

/**
 * @brief 시스템 시작 시 WDT 초기화
 * @note 타임아웃을 1초로 설정하고 리셋 기능을 활성화함
 */
void System_Init_WDT(void) {
    *pWDT_Counter = WDT_LOAD_VAL; // 카운터 초기값 로드
    *pWDT_Ctrl    = 0x01;         // WDT Enable bit set
    
    // 주의: 부팅 시간이 길다면 이 함수가 끝나기 전에 리셋이 걸릴 수 있음
    // 일반적으로 부팅 직후가 아니라, 부팅 완료 후 메인 루프 진입 전 활성화
}

/**
 * @brief 워치독 킥 (Kick the Dog)
 * @detail 안전장치로 특정 키 순서를 요구하는 경우가 많음
 */
void WDT_Refresh(void) {
    // 1단계: Unlock Sequence (옵션)
    *pWDT_Ctrl = 0x1ACCE551; 
    
    // 2단계: 카운터 리셋 (0부터 다시 시작)
    *pWDT_Counter = WDT_LOAD_VAL;
    
    // 3단계: Lock (옵션)
    *pWDT_Ctrl = 0x1ACCE551; 
}

// [Main Loop]
int main(void) {
    System_Init_WDT();

    while(1) {
        // 1. 주요 작업 수행 (Sensor Read, Comm, etc.)
        Task_MainProcess(); 

        // 2. 작업이 정상 완료되었을 때만 워치독 리셋
        // 만약 Task_MainProcess()에서 무한 루프에 빠지면 이 코드는 실행되지 않음
        WDT_Refresh(); 
    }
}
```

> 📢 **섹션 요약 비유**:
> 여행자가 폭포로 떨어지는 강물을 건너는 밧줄 다리를 건너는 상황입니다. (CPU Loop)
> 건너는 동안 수면제(킥 신호)를 먹인 호랑이(WDT)가 뒤에서 쫓아옵니다.
> 여행자가 계속해서 호랑이에게 수면제를 던져주면(Kick) 호랑이는 잠들어 있습니다.
> 하지만 여행자가 중간에 다리가 끊어져서 추락하거나(CPU Hang), 너무 느리게 움직이면,
> 수면제 효과가 풀린 호랑이가 여행자를 물어버려 강제로 시작점으로 되돌려 보냅니다(Reset).

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

WDT는 단순한 하드웨어 회로를 넘어, 시스템의 안전성 등급(SIL)과 운영체제의 커널 패닉 복구와 깊이 연관되어 있습니다.

### 1. 내부 워치독(Internal WDT) vs 외부 워치독(External WDT) 비교

| 비교 항목 (Criteria) | 내부 워치독 (Internal WDT) | 외부 워치독 (External WDT) |
|:---|:---|:---|
| **통합도 (Integration)** | MCU/SoC Die 내부에 통합 | 별도의 외부 IC (Supervisor IC) |
| **비용 (Cost)** | 추가 비용 $0 (내장) | $0.5 ~ $2.0 (BOM 추가) |
| **신뢰성 (Reliability)** | 중간<br>(CPU 전원/클럭 의존도 높음) | 매우 높음<br>(CPU 완전 독립적 동작) |
| **복잡도 (Complexity)** | 낮음 (소프트웨어 설정만) | 높음 (PCB 라우팅, 회로 설계) |
| **주요 용도 (Use Case)** | 일반 소비자 가전, IoT 센서 | 의료기기, 자동차(ISO 26262), 우주항공 |
| **CPU 정지 감지** | CPU 정지 시 WDT도 멈추거나<br>Clk Dependency로 불확실 | CPU가 완전히 꺼져도 독립적으로 리셋 감시 가능 |

### 2. 타 기술 영역과의 융합 (Convergence)

**A. OS (Operating System) 커널과의 시너지**
리눅스 커널이나 RTOS (Real-Time OS)는 소프트웨어적으로 각 태스크의 수행 상태를 모니터링하는 **Watchdog Thread**를 운영합니다. 하지만 OS 자체가 치명적인 버그로 멈추면(Crash/Panic), 소프트웨어 워치독은 동작하지 않습니다. 따라서 HW WDT와 SW WDT를 **2단계 계층 구조(Tiered Watchdog)**로 구성하여, SW WDT가 먼저 처리하고, 그것이 실패하면 HW WDT가 최종적으로 시스템을 리셋하는 방식이 일반적입니다.

**B.