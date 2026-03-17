+++
title = "68. 밀리 머신 (Mealy Machine)"
date = "2026-03-14"
weight = 68
+++

# 68. 밀리 머신 (Mealy Machine)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 밀리 머신(Mealy Machine)은 유한 상태 머신(FSM: Finite State Machine)의 일종으로, 시스템의 출력이 **현재 상태(Present State)와 현재 입력(Input)의 조합**에 의해 순차적으로 결정되는 동 시스템 모델이다.
> 2. **가치**: 입력 변화가 클럭(CLK) 에지를 기다리지 않고 조합 논리(Combinational Logic)를 통해 즉시 출력에 반영되므로, 무어 머신(Moore Machine) 대비 **1 클럭 사이클의 지연 시간(Latency)을 제거**하여 초고속 응답이 가능하며, 일반적으로 더 적은 수의 상태(State)로 동일한 기능을 구현하여 하드웨어 자원을 절약할 수 있다.
> 3. **융합**: 통신 프로토콜의 핸드셰이킹(Handshaking), 고성능 버스 인터페이스(如 PCIe, AXI), 그리고 실시간 인터럽트 제어기와 같이 **처리량(Throughput)과 반응 속도가 생명인 현대 디지털 논리 회로 설계**의 핵심적인 아키텍처이다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
밀리 머신은 1955년 조지 H. 밀리(George H. Mealy)가 제안한 순차 논리 회로의 모델로, 출력 로직(Output Logic)이 상태 레지스터의 출력($Q$)뿐만 아니라 **외부 입력(Inputs)에 직접 의존**하는 것이 가장 큰 특징이다. 수학적으로 $Mealy = M \times \Sigma \rightarrow \Lambda$로 표현되며, 여기서 출력 $\Lambda$는 상태 $M$과 입력 $\Sigma$의 함수이다. 이는 출력값이 상태 노드 내부가 아닌 **상태 전이(Transition) 경로 상**에 존재한다는 것을 의미하며, 클럭의 동기화(Synchronization) 범위를 벗어나는 비동기적(Asynchronous) 특성을 내포하고 있다.

### 2. 💡 비유: 반응형 자동문
밀리 머신은 **"레이저 센서가 장착된 초고속 자동문"**과 같다.
- **무어 머신**: 문이 '닫힘' 상태일 때 센서가 사람을 감지하더라도, 제어 장치가 다음 클럭(사이클)을 기다려 '열림' 명령을 내리고, 그 다음에 모터가 작동하여 문이 열린다. (상태 $\rightarrow$ 출력)
- **밀리 머신**: 문이 '닫힘' 상태이더라도, 사람이 접근하는 순간(입력) 센서 신호가 즉시 모터 제어 신호(출력)와 결합하여 문이 열리기 시작한다. 상태 변화를 위한 별도의 대기 시간 없이 입력에 즉각 반응하는 것이다.

### 3. 등장 배경: 성능과 자원의 트레이드오프
- **하드웨어 자원 최적화**: 초기 디지털 설계에서 플립플롭(Flip-Flop)은 물리적으로 크고 전력을 많이 소모하는 자원이었다. 밀리 머신은 출력을 결정하기 위해 추가적인 상태(State)를 생성하지 않고 입력 변수를 활용함으로써, 무어 머신보다 적은 수의 상태 레지스터로 복잡한 제어 로직을 구현할 수 있었다.
- **저지연(Low-Latency) 요구사항**: 통신 및 데이터 처리 속도가 GHz 단위로 증가하면서, 클럭 사이클 한 번의 지연조차 치명적인 병목 구간이 되었다. 이에 따라 밀리 머신의 **'입력 즉시 출력(Immediate Response)'** 특성이 고성능 시스템 설계의 필수 요소로 부상했다.

### 📢 섹션 요약 비유
"마치 고속도로 톨게이트에서 하이패스 차로를 운영하여, 차량이 진입(입력)하는 즉시 차단봉이 올라가는(출력) 방식과 같아서, 별도의 정지 대기 시간(상태 변경 대기) 없이 흐름을 제어하는 시스템입니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석
밀리 머신은 크게 상태 저장 장치와 조합 논리 회로로 구성된다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/논리 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **상태 레지스터**<br>(State Memory) | 시스템의 현재 맥락($Q$) 저장 | 클럭 에지(Edge)에서만 값 변경. `D = NS, Q = NS(t-1)` | 동기식 (Synchronous) | 사수의 기억력 |
| **차기 상태 논리**<br>(NS Logic) | 다음 상태 결정 ($\delta$ 함수) | `NS = F(Input, Current_State)` 조합 | And-Or Gate Array | 사고 과정 |
| **출력 논리**<br>(Output Logic) | 실제 출력값 생성 ($\lambda$ 함수) | **`Output = G(Input, Current_State)`** (핵심) | 조합 논리 (Combinational) | 즉각 반사 신경 |
| **입력 필터**<br>(Input Filter) | 노이즈 제거 및 안정화 | 입구의 슈미트 트리거(Schmitt Trigger) 등 | 아날로그/디지털 믹스 | 망막의 노이즈 제거 |

### 2. 아키텍처 및 데이터 흐름
아래 다이어그램은 입력이 출력 로직으로 직접 연결되는 밀리 머신의 구조적 특징을 보여준다.

```text
      ┌───────────────────────────────────────────────────────────────────┐
      │                 Mealy Machine Architecture                        │
      │                                                                   │
      │  [Inputs]                                                          │
      │    X ────────┬─────────────────────┬───────────────┐              │
      │              │                     │               │              │
      │              ▼                     ▼               │              │
      │       ┌─────────────┐       ┌─────────────┐        │              │
      │       │  Next State │       │   Output    │        │              │
      │       │  Decoding   │       │  Decoding   │        │              │
      │       │  Logic (F)  │       │  Logic (G)  │◄───────┤              │
      │       └──────┬──────┘       └──────┬──────┘        │              │
      │              │                     │               │              │
      │              ▼                     │               │              │
      │       ┌─────────────┐               │               │              │
      │  +───▶│ State       │               │               │              │
      │  │    │ Registers   │───────────────┘               │              │
      │  │    │ (Flip-Flops)│  Current State (Q)            │              │
      │  │    └─────────────┘                             │              │
      │  │         ▲                                     │              │
      │  │         │                                     │              │
      │  └─────────┘                                     │              │
      │        CLK (Clock)                               │              │
      │                                                  ▼              │
      │                                           ┌─────────────┐      │
      │                                           │   Outputs   │      │
      │                                           └─────────────┘      │
      └───────────────────────────────────────────────────────────────────┘
      
      * Key: Inputs affect Output Logic DIRECTLY (No Clock wait)
```

**[다이어그램 해설]**
이 다이어그램에서 가장 주목해야 할 점은 **입력 라인(Inputs)이 출력 논리(Output Decoding Logic) 블록으로 곧바로 연결되어 있는 경로(빨간색 화살표 연상)**다. 무어 머신이라면 입력이 상태 레지스터를 거쳐 다음 클럭에 반영된 후에야 출력이 바뀌겠지만, 밀리 머신은 상태 레지스터를 거치지 않는 '지름길(Ushort-cut)'이 존재한다. 따라서 입력 $X$가 0에서 1로 변하는 순간, 조합 논리를 통해 출력 $Y$가 즉시 1로 변한다. 이는 클럭 주파수와 무관하게 매우 빠른 반응 속도를 제공하지만, 동시에 입력에 포함된 미세한 노이즈(Glitch)까지 출력으로 전파시키는 위험을 내포한다.

### 3. 상태 전이도 (State Diagram) 표기법
밀리 머신의 상태도는 천이 선(Transition Arc) 위에 `입력 / 출력`을 명시하여 표기한다.

```text
      (입력 X=0) / (출력 Y=0)        (입력 X=1) / (출력 Y=1)
      ┌─────────────────────┐      ┌─────────────────────┐
      │                     │      │                     │
      ▼                     │      │                     ▼
   ┌─────┐ 1/1    ┌─────┐ 1/0 ┌─────┐ 0/0        ┌─────┐
   │  S0 │───────▶│  S1 │─────│  S2 │────────────▶│  S0 │
   └─────┘        └─────┘     └─────┘             └─────┘
      ▲ 0/1             │   0/1   │
      └─────────────────┘         └───────────────────┘
      
   * 표기: 입력값 / 출력값
   * 해석: S0 상태에서 입력 1이 들어오면, 출력은 1이 되면서 S1으로 상태가 바뀐다.
```

### 4. 핵심 알고리즘 및 Verilog 코드
밀리 머신의 출력은 입력의 변화에 민감하므로, 합성(Synthesis) 시 타이밍(Timing) 최적화가 필수적이다.

```verilog
// [Mealy Machine Example] Edge Detector
module Mealy_Detector (
    input wire clk,          // Clock (CLk)
    input wire rst_n,        // Active Low Reset
    input wire data_in,      // Serial Input
    output reg detected      // Output (Mealy: depends on Input & State)
);

    // State Encoding
    parameter IDLE = 1'b0, CHECK = 1'b1;
    reg current_state, next_state;

    // State Register (Sequential Logic)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) current_state <= IDLE;
        else        current_state <= next_state;
    end

    // Next State & Output Logic (Combinational Logic)
    always @(*) begin
        next_state = current_state;
        detected = 1'b0; // Default Output

        case (current_state)
            IDLE: begin
                if (data_in) begin
                    next_state = CHECK;
                    // 밀리 머신 특징: 상태 변화와 무관하게 입력에 의해 출력 결정
                    detected = 1'b0; 
                end
            end
            CHECK: begin
                if (data_in) begin
                    next_state = CHECK;
                    detected = 1'b0;
                end
                else begin
                    next_state = IDLE;
                    // 입력이 1->0으로 떨어지는 즉시 출력 1 (Edge Detect)
                    detected = 1'b1; 
                end
            end
        endcase
    end
endmodule
```

### 📢 섹션 요약 비유
"마치 피겨 스케이팅 선수가 심판의 신호(입력)를 보자마자 바로 점프를 준비(출력)하는 것처럼, 밀리 머신은 현재 위치(상태)뿐만 아니라 외부 신호에 즉각적으로 반응하여 동작을 결정하는 매우 민감한 회로입니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 무어 머신(Moore Machine) vs 밀리 머신(Mealy Machine) 심층 분석

| 구분 (Criteria) | 무어 머신 (Moore Machine) | 밀리 머신 (Mealy Machine) | 기술적 분석 (Technical Insight) |
|:---|:---|:---|:---|
| **출력 함수** | $Output = f(State)$ | **$Output = f(State, Input)$** | 밀리는 입력에 대한 출력 함수의 차수가 더 높음. |
| **응답 속도** | 상태 변경 후 출력 생성 (Max 1 CLK 지연) | 입력 즉시 출력 생성 (**0 CLK 지연**) | 밀리는 CPI(Cycles Per Instruction) 관점에서 유리함. |
| **상태 수** | 상대적으로 **많음** (복잡도 높음) | 상대적으로 **적음** (최적화 유리) | 예: 시퀀스 생성기에서 밀리는 상태를 절반으로 줄일 수 있음. |
| **타이밍 안정성** | **우수** (동기화된 출력) | 취약 (글리치 전파 가능) | 무어는 출력이 플립플롭을 거치므로 Hazard-free. |
| **회로 복잡도** | 출력 로직이 단순해짐 | 출력 로직이 입력에 의존하여 복잡해질 수 있음 | Critical Path가 길어질 수 있어 주의 필요. |

### 2. 다각도 분석: 타이밍 및 합성 관점

```text
      ┌─────────────────────────────────────────────────────┐
      │   Timing Comparison: Moore vs Mealy                 │
      ├─────────────────────────────────────────────────────┤
      │                                                     │
      │   [Input Waveform]      _-_-_-_-_-_-_-_-_-_-_       │
      │                                                     │
      │   [Moore Output]   ________^^^^^^^^^^^^^^____       │
      │      (Wait CLK)    ▲        (Delayed Response)      │
      │                     1 Cycle Latency                 │
      │                                                     │
      │   [Mealy Output]   ______^^^^^^^^^^^^^^______       │
      │      (Immediate)   ▲                                │
      │                     Instantaneous Response          │
      │                                                     │
      └─────────────────────────────────────────────────────┘
```

**[융합 분석]**
- **컴퓨터 구조(Computer Architecture)**: CPU의 파이프라인(Pipeline) 제어 로직에서 데이터 헤저드(Hazard)를 감지하고 해결하는 로직은 수 사이클의 손실을 막기 위해 밀리 머신 특성을 활용하여 설계되는 경우가 많다.
- **네트워크(Networking)**: 패킷 스위칭 시스템에서 헤더 정보를 파싱하여 즉시 라우팅 결정을 내려야 할 때, 밀리 기반의 CAM(Content Addressable Memory) 제어 로직이 사용된다.

### 📢 섹션 요약 비유
"무어 머신이 '매일 같은 시간에 버스가 오는' 공공 교통 시스템이라면, 밀리 머신은 '손님을 태우자마자 출발하는' 콜밴 시스템과 같습니다. 콜밴은 효율이 좋지만(상태 수 적음), 예상치 못한 승객(입력 노