+++
title = "71. CPLD (Complex Programmable Logic Device)"
date = "2026-03-14"
weight = 71
+++

# [CPLD (Complex Programmable Logic Device)]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPLD (Complex Programmable Logic Device)는 여러 개의 로직 블록(Function Block)을 프로그래밍 가능한 상호 연결 배열(PIA)로 결합한 고밀도 논리 소자로, 전원이 꺼져도 회로 정보를 유지하는 **비휘발성(Non-volatile)** 특성이 핵심이다.
> 2. **가치**: FPGA (Field-Programmable Gate Array)와 달리 내부 Flash 메모리에 설정을 저장하여 전원 인가 시 즉시 동작(Instant-on)하며, 신호 지연 시간(Tpd, Propagation Delay Time)이 고정적(Deterministic)이어서 고속/결정적 응답이 필요한 시스템 제어에 최적화되어 있다.
> 3. **융합**: SoC (System on Chip)나 고성능 CPU가 부팅되기 전까지 전원 시퀀스(Power Sequencing)를 감시하고 안정적인 전압을 공급하는 '시스템 감시자(Supervisor)' 역할을 수행하며, FPGA와 함께 보드의 설계 유연성을 극대화하는 상보적 관계를 형성한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
CPLD는 복잡한 조합 논리(Combinational Logic)과 순차 논리(Sequential Logic)를 하나의 칩 내에서 구현할 수 있는 사용자 프로그래밍 가능한 반도체 소자다. 내부적으로 PAL (Programmable Array Logic)이나 GAL (Generic Array Logic) 같은 소규모 논리 배열을 여러 개 집적하고, 이를 교차 연결(Crossbar) 방식의 매트릭스로 연결한 구조를 가진다. 

SPLD (Simple PLD)나 게이트 어레이(Gate Array) 로직을 디지털 회로에 구현할 때 발생하는 '보드 면적 증가'와 '전력 소모' 문제를 해결하기 위해 등장했다. FPGA가 내부 메모리(SRAM)에 설정을 저장해 외부에서 로딩해야 하는 반면, CPLD는 내부 플래시 메모리(Flash Memory)를 사용하여 전원을 켜자마자 설정이 완료되는 특징을 가진다.

#### 2. 탄생 배경 및 발전 과정
1. **SSI/MSI 시대의 한계**: 초기 디지털 회로는 74시리즈 TTL 같은 표준 부품을 수십, 수백 개 사용하여 회로를 구성했다. 이는 기판(PCB) 면적 증가, 배선 복잡도 증가, 전력 소모 증가, 신뢰성 저하 등의 문제가 있었다.
2. **PLD의 등장**: PAL, PLA, GAL과 같은 프로그래밍 가능 논리 소자가 나오면서 특정 로직을 하나의 칩으로 대체할 수 있게 되었다. 그러나 용량이 작아 수천 게이트 이상의 복잡한 회로를 구현하기엔 부족했다.
3. **CPLD의 혁신**: 여러 개의 PAL 블록을 칩 안에 넣고, 이들을 연결하는 스위칭 매트릭스(Interconnect)를 집적하여 고밀도 로직을 구현하면서도, 단일 칩 솔루션으로서의 경제성과 신뢰성을 확보했다.

#### 3. 기술적 위치 (Taxonomy)
디지지털 로직 구현의 스펙트럼에서 CPLD는 **ASIC (Application-Specific Integrated Circuit)**과 **FPGA** 사이의 중간 지점에 위치하며, 특히 **소용량·고속·비휘발성**이 필요한 영역에서 독보적인 위치를 차지한다.

```text
[Logic Device Spectrum]
 │<---------------- Complexity & Gate Count ----------------> │
 │
 │  ASIC/ASSP          CPLD                 FPGA
 │  (Fixed)           (Complex PLD)        (SRAM Based)
 │  ──────────────────────────────────────────────────────────
 │  [High Speed]      [Mid Speed]          [High Speed]
 │  [High Volume]     [Mid Volume]         [Low Volume]
 │  [NRE Cost $$$]    [No NRE Cost]        [No NRE Cost]
 │  [Non-Volatile]    [Non-Volatile]       [Volatile]
```

**[다이어그램 해설]**
위 다이어그램은 디지털 로직 소자의 선택 기준을 나타낸다. CPLD는 FPGA보다 게이트 수는 적지만, ASIC처럼 마스크 비용(NRE, Non-Recurring Engineering)이 들지 않고 FPGA와 같이 재프로그래밍이 가능하다. 무엇보다 중요한 차별점은 '비휘발성'과 '즉시 동작(Instant-on)' 특성으로 인해, 시스템의 핵심 제어 로직(Boot Logic)을 담당하는 1등 시민으로 사용된다.

> **📢 섹션 요약 비유**: CPLD는 **"재떨이에 이미 구겨진 담배처럼, 형태가 고정되어 있지만 언제든 바로 꺼내 피울 수 있는 준비된 상태"**와 같습니다. FPGA는 '물을 부어야 젤리가 굳는(로딩 과정)' 과정이 필요하지만, CPLD는 전원이라는 성냥불만 붙이면 이미 굳어있는 로직을 즉시 실행합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CPLD의 아키텍처는 "논리를 처리하는 블록"과 "이 블록들을 연결하는 도로"로 이해할 수 있다.

#### 1. 핵심 구성 요소 상세 분석 (5개 모듈)

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 기능 (Role) | 내부 동작 메커니즘 | 프로토콜/인터페이스 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|:---|
| **FB** | Function Block (Logic Array Block) | 논리 연산 수행 | AND-OR 배열을 통해 입력 신호를 조합하여 출력 생성 | Programmable AND/Fixed OR | 독립적인 사무실 (업무 처리) |
| **PIA** | Programmable Interconnect Array | 블록 간 연결 | 모든 FB의 입력/출력을 가상의 매트릭스로 연결, 지연 시간 최소화 | Crossbar Switch | 건물 내부의 복도 (통로) |
| **MC** | Macrocell | FB 내의 로직 셀 | 논리 연산 결과를 래치(Flip-Flop)하거나 출력 형태(인버스 등) 조절 | D-FF, MUX | 개별 직원의 작업台 |
| **I/O Block** | Input/Output Control Block | 외부 신호 입출력 | 전압 레벨 조정(TTL, CMOS 등), 드라이버 강도 조절 | 3.3V/5V Tolerance | 건물 출입구 (문) |
| **Flash/EEPROM** | Non-Volatile Memory | 회로 정보 저장 | JTAG을 통해 다운로드된 비트스트림(Bitstream)을 영구 저장 | JTAG (IEEE 1149.1) | 직원의 뇌/매뉴얼 (기억) |

#### 2. CPLD 내부 구조 다이어그램 (Architecture)

CPLD의 가장 대표적인 구조는 여러 개의 Function Block이 PIA에 의해 연결되는 형태다.

```text
          [ CPLD Architecture View ]
      ┌───────────────────────────────────┐
      │                                 │
      │  ┌───────────┐  ┌───────────┐  │
      │  │   I/O     │  │   I/O     │  │
 IN1 ──┼─│  Block    │  │  Block    │──┼─── OUT1
      │  │  (MC)     │  │  (MC)     │  │
      │  └─────┬─────┘  └─────┬─────┘  │
      │        │              │        │
 IN2 ──┼───────┼──────────────┼────────┼─── OUT2
      │        │    PIA       │        │
      │        │ (Interconnect│        │
      │        │   Array)     │        │
      │        │              │        │
      │  ┌─────┴─────┐  ┌─────┴─────┐  │
      │  │   FB 1    │  │   FB 2    │  │
      │  │ (AND-OR)  │  │ (AND-OR)  │  │
      │  │ + Config  │  │ + Config  │  │
      │  │  Memory   │  │  Memory   │  │
      │  └───────────┘  └───────────┘  │
      │                                 │
      └───────────────────────────────────┘
```

**[다이어그램 해설]**
1.  **PIA (Programmable Interconnect Array)**: 그림 중앙의 거대한 교차로 역할을 한다. 모든 Function Block의 입출력이 이곳에 연결된다. FPGA의 라우팅(Routing) 구조가 길이에 따라 지연 시간이 달라지는 것과 달리, CPLD의 PIA는 신호가 지나가는 경로가 물리적으로 거의 동일하게 설계되어 **시간적인 예측성(Deterministic Timing)**을 보장한다.
2.  **Function Block (FB)**: 그림 하단의 네모 박스들이다. 각 FB는 내부에 수십 개의 매크로셀(Macrocell)을 포함하며, 하나의 PAL22V10(대표적인 SPLD)과 유사한 구조를 가진다. 즉, Product Term(AND 배열)을 모아 Sum(OR 배열)을 만드는 구조다.
3.  **메모리 통합**: FB 옆에 붙어있는 Config Memory는 전원이 꺼져도 데이터를 지키는 플래시 메모리다. 전원이 켜지면 이 메모리의 내용이 즉시 로딩되어 로직이 동작한다.

#### 3. 핵심 동작 원리 및 타이밍

CPLD의 핵심은 **Pin-to-Pin Delay (Tpd)**가 일정하다는 점이다.
$$ T_{Total} = T_{Input} + T_{Logic} + T_{Routing} + T_{Output} $$
FPGA의 경우 $T_{Routing}$이 배선 위치에 따라 $ns$ 단위로 크게 변하지만, CPLD는 PIA 구조 덕분에 $T_{Routing}$이 고정되어 있다. 따라서 항상 일정한 주파수로 동작하는 타이밍 크리티컬(Timing-Critical) 인터페이스(I2C, SPI, Chip Enable 제어 등)를 구현하기에 완벽하다.

#### 4. 코드/구현 예시 (VHDL 스타일 개념)
CPLD는 주로 상태 머신(FSM, Finite State Machine)을 구현하는 데 쓰인다.

```vhdl
-- CPLD를 이용한 Power Sequencing State Machine (Conceptual)
entity Power_Controller is
    Port ( CLK      : in  STD_LOGIC;   -- System Clock
           PGOOD_3V3: in  STD_LOGIC;   -- 3.3V Power Good Status
           EN_5V    : out STD_LOGIC;   -- Enable 5V Rail
           EN_CPU   : out STD_LOGIC);  -- Enable CPU Rail
end Power_Controller;

architecture Behavioral of Power_Controller is
    type state_type is (IDLE, PWR_5V, WAIT_CPU, ON);
    signal current_state : state_type := IDLE;
begin
    process(CLK)
    begin
        if rising_edge(CLK) then
            case current_state is
                when IDLE =>
                    EN_5V <= '1';      -- Step 1: Turn on 5V
                    current_state <= PWR_5V;
                when PWR_5V =>
                    if PGOOD_3V3 = '1' then -- Step 2: Check 3.3V Stability
                        EN_CPU <= '1';  -- Step 3: Turn on CPU
                        current_state <= ON;
                    end if;
                when ON => null;
            end case;
        end if;
    end process;
end Behavioral;
```

> **📢 섹션 요약 비유**: CPLD의 내부 구조는 **"각 팀(FB)이 독립적으로 업무를 보되, 회의실(PIA)을 통해 예약된 순서대로만 통신하는 대기실 시스템"**과 같습니다. 누구나 회의실에 갈 수는 있지만, 회의실에 도착하는 시간이 항상 정확하게 예약된 시간대로 일치하므로, 회의 일정(로직 타이밍)을 100% 신뢰할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석

CPLD는 독립적으로 쓰이기보다 타 시스템, 특히 **FPGA**와 **MCU**와의 관계 속에서 그 진가가 발휘된다.

#### 1. CPLD vs FPGA vs MCU 비교 분석

| 비교 항목 | CPLD | FPGA | MCU (Microcontroller) |
|:---|:---|:---|:---|
| **기본 구조** | AND-OR Plane (Macrocell) | LUT (Look-Up Table) + FF | ALU + Memory + Peripherals |
| **휘발성** | **비휘발성 (Flash/EEPROM)** | **휘발성 (SRAM)** | 비휘발성 (Flash Code) |
| **부팅 시간** | **즉시 (Instant-on, <1ms)** | 지연 발생 (Configuration Time) | 지연 발생 (Bootloader) |
| **지연 시간** | **고정적 (Deterministic)** | 가변적 (Routing dependent) | 소프트웨어 실행에 따른 불확실성 |
| **로직 용량** | ~10,000 Gates (낮음) | ~Millions Gates (매우 높음) | N/A (Sequential Logic) |
| **병렬 처리** | **하드웨어 병렬성** | **하드웨어 병렬성** | 순차 처리 (Software) |
| **적용 분야** | Glue Logic, Boot Loader, Prototyping | 고성능 신호 처리, AI 가속, 복잡한 알고리즘 | 일반 제어, UI, 데이터 처리 |

**[심층 분석]**
*   **속도 vs 용량**: CPLD는 레이턴시(Latency)가 매우 낮고 고정적이지만, 용량이 작아 복잡한 알고리즘을 구현하기 어렵다. FPGA는 용량이 커서 복잡한 알고리즘을 처리할 수 있지만, 핵심 로직의 지연 시간을 100% 보장하려면 상당한 노력(Place & Route)이 필요하다.
*   **전력**: CPLD는 정적 전력(Static Power)이 거의 없어 대기 모드에서 매우 유리하다. FPGA는 SRAM 셀이 수백만 개 있어 대기 전력이 상당히 높다.

#### 2. 시스템 융합 관점 (System Integration)

```text
      [System Co-design Example: Server Motherboard]

      ┌─────────────────────────────────────────────────┐
      │                                                 │
      │  ┌──────────┐      ┌──────────┐                │
      │  │   CPLD   │─────▶│  FPGA    │                │
      │  │ (Supervisor)     │(Worker)  │                │
      │  └───────┬───┘      └────▲─────┘                │
      │          │               │                      │
      │          │ [Power Seq]   │ [Data Proc]          │
      │          ▼