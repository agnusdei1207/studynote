+++
title = "38. 병렬 가감산기"
date = "2026-03-14"
weight = 38
+++

# # [38. 병렬 가감산기 (Parallel Adder-Subtractor)]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 병렬 가감산기(Parallel Adder-Subtractor)는 **2의 보수법(2's Complement Method)**의 수학적 원리를 하드웨어적으로 구현하여, 단일 회로 내에서 덧셈과 뺄셈을 모드 전환 없이 즉시 수행하는 통합 연산 장치다.
> 2. **가치**: 뺄셈을 수행하기 위한 별도의 하드웨어 감산기(Subtractor) 설계를 배제하여 **CPUs (Central Processing Units)** 및 **ASICs (Application-Specific Integrated Circuits)**의 게이트 수(Gate Count)와 전력 소모를 획기적으로 최적화한다.
> 3. **융합**: **ALU (Arithmetic Logic Unit)**의 데이터패스(Data Path) 설계에 필수적이며, **ISA (Instruction Set Architecture)**의 산술 명령어 세트(Arithmetic Instruction Set)를 효율적으로 실행하는 하드웨어적 근간이 된다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 병렬 가감산기는 $n$-비트의 이진수 $A$와 $B$에 대해, 제어 신호 $M$ (Mode)의 값에 따라 $A+B$ 또는 $A-B$를 연산하는 조합 논리 회로(Combinational Logic Circuit)다.
- **기술적 철학**: 디지털 회로에서 뺄셈 $A - B$는 $A + (\bar{B} + 1)$, 즉 '피감수 $B$의 2의 보수를 취한 후 덧셈'으로 정의된다. 병렬 가감산기는 이 수학적 정의를 **XOR (Exclusive OR) 게이트**의 '조건부 반전(Conditional Inversion)' 성질과 전가산기(Full Adder)의 캐리(Carry) 특성을 이용해 하드웨어에 직접 구현한 장치다.

- **💡 비유**: 병렬 가감산기는 **"방향 전환 가능한 고속도로 톨게이트"**와 같다.
    - 평소(모드 0)에는 모든 차량이 그대로 통과하지만(덧셈),
    - 특정 스위치를 누르면(모드 1), 진입 차선의 도로 색상을 반전시켜(1의 보수) 통행료 1원(캐리 1)을 추가로 받음으로써(2의 보수), 결과적으로 반대 방향으로 흐르게 만드는(뺄셈) 원리다.

- **등장 배경**:
    1.  **공간 효율성의 압박**: 초창기 컴퓨터는 가산기와 감산기가 물리적으로 분리되어 있어 회로 면적이 낭비되었고, 이는 클럭 스피드(Clock Speed)의 병목이 되었다.
    2.  **보수 연산(Complement Arithmetic)의 정립**: '음수의 표현'을 2의 보수로 통일하면서, 뺄셈 논리를 단순 가산기로 대체할 수 있는 수학적 기반이 마련되었다.
    3.  **VLSI (Very Large Scale Integration)** 발전: 수만 개의 트랜지스터를 하나의 칩에 집적하면서, '자원 재사용(Resource Sharing)'을 통해 칩 면적을 줄이는 설계 트렌드가 강화되었다.

> **📢 섹션 요약 비유**: 마치 칼날의 각도를 조절하여 '썰기(덧셈)'와 '깎기(뺄셈)'를 모두 수행하는 정밀 가공 기계처럼, 회로 하나로 두 가지 산술 연산을 오가는 효율적인 설계 철학이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
가감산기는 크게 데이터 입력부, 조건부 반전부, 그리고 합산부로 나뉜다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Control Signal (M)** | 모드 선택 | 0일 땐 Add 모드, 1일 땐 Subtract 모드 설정. 최하위 비트의 Carry-In으로 직접 연결됨. | 기관차의 진행 레버 |
| **XOR Gate Array** | 입력 데이터 반전 | 피감수 $B$와 $M$을 입력. $M=1$일 때 $B \oplus 1 = \bar{B}$ (Inverted B) 출력하여 1의 보수 생성. | 편집증 지우개 |
| **Full Adder (FA)** | 합산 연산 | $Sum = A \oplus B \oplus Cin$. $Cout$ 생성. 병렬 연결을 통해 n-비트 처리. | 실질적인 계산 엔진 |
| **Carry Logic** | 2의 보수 완성 | $M=1$일 때, 첫 번째 FA의 $Cin$에 1을 공급하여 $\bar{B} + 1$ (2의 보수) 연산 완료. | 마지막 퍼즐 조각 |
| **Overflow Detector** | 에러 플래그 | MSB의 $C_{in}$과 $C_{out}$을 XOR하여 오버플로우 발생 여부를 OS(Status Register)에 알림. | 사이렌 경보기 |

#### 2. 회로 구조 및 데이터 흐름 (ASCII Diagram)

아래 다이어그램은 4비트 병렬 가감산기의 구조를 보여준다. 제어 신호 $M$이 모든 XOR 게이트와 최하위 $C_{in}$에 연결되어 제어 권한을 쥐고 있음을 주목하라.

```text
      ┌─────────── 제어 신호 M (Mode Select: 0=Add, 1=Sub) ───────────┐
      │                                                               │
      ▼                                                               │
      ┌───┐     ┌───┐     ┌───┐     ┌───┐                           │
 A3 ──┤   │     │   │     │   │     │   │                           │
      │   │     │   │     │   │     │   │                           │
 B3 ──┤XOR├──┐  │XOR│─┐   │XOR│─┐   │XOR│─┐       ┌──────────────┐  │
      │   │  │  │   │ │   │   │ │   │   │ │       │              │  │
 M ───┤   │  │  │   │ │   │   │ │   │   │ │       │   4-bit      │  │
      └───┘  │  └───┘ │   └───┘ │   └───┘ │       │ Parallel     │  │
             │  ▲    │   ▲    │   ▲    │       │ Adder-Sub   │  │
             └──┤    └───┤    └───┤    └───┬───┤ (Logic Core)│  │
                │        │        │        │   │              │  │
                ▼        ▼        ▼        ▼   └───────┬──────┘  │
              ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐         │         │
          ┌───┤ FA3 │─┤ FA2 │─┤ FA1 │─┤ FA0 │         │         │
          │   └─────┘ └─────┘ └─────┘ └─────┘         │         │
          │      ▲       ▲       ▲       ▲             ▼         ▼
          │      │       │       │       │         Carry Chain (Ripple)
          └─Cout│◀──C3  │◀──C2  │◀──C1  │◀──Cout │     (or CLA Logic)
               │       │       │       │       │
               └───────┴───────┴───────┴───────┘
                         │
                         ▼
                      S3 S2 S1 S0 (Sum Result)
```

**[다이어그램 해설]**
1.  **제어 로직 (Control Line)**: $M$ 신호는 회로의 하단부가 아닌 상단부에서 모든 XOR 게이트를 제어한다. 이는 '조건부 반전'의 핵심이다.
2.  **데이터 패스 (Data Path)**:
    -   **$M=0$ (Add Mode)**: XOR 게이트는 버퍼(Buffer)처럼 작동($B \oplus 0 = B$). $C_{in}$도 0. 따라서 회로는 일반적인 **Ripple Carry Adder**로 기능한다.
    -   **$M=1$ (Subtract Mode)**: XOR 게이트는 인버터(Inverter)처럼 작동($B \oplus 1 = \bar{B}$). 동시에 $C_{in}$이 1이 되므로, 결과적으로 $A + (\bar{B} + 1) = A + (2's \ Complement \ of \ B)$, 즉 **뺄셈**을 수행한다.
3.  **캐리 전파 (Carry Propagation)**: LSB(Least Significant Bit)에서 MSB(Most Significant Bit)로 캐리가 연쇄적으로 전달되며 합을 계산한다.

#### 3. 핵심 알고리즘 및 타이밍 분석
가감산기의 성능은 캐리가 전파되는 지연 시간에 의해 결정된다.

```verilog
// 1-bit Adder-Subtractor Module Behavior (Verilog Pseudo-code)
module add_sub_unit (input a, b, m, cin, output sum, cout);
    wire b_xor;
    
    // Step 1: Conditional Inversion (XOR Logic)
    // M=1 일 때 b가 반전됨 (1's Complement)
    assign b_xor = b ^ m; 

    // Step 2: Full Addition with Carry Logic
    // M=1 일 때, cin(최종적으로 m)이 1이 되어 2의 보수 완성
    assign {cout, sum} = a + b_xor + cin;
endmodule

// Total Latency Calculation (Ripple Carry 기준)
// T_total = T_XOR + T_FA + T_XOR + (N-1)*T_Ripple
// 실무적으로는 CLA(Carry Look-ahead)를 사용하여 T_Ripple을 제거함.
```

> **📢 섹션 요약 비유**: 마치 변신 로봇이 장비를 갈아끼는 것이 아니라, 내부의 기어 배치만 재조정하여 즉시 다른 모드(지상/비행)로 전환하는 것처럼, XOR 게이트라는 '스마트한 스위치'를 통해 회로 자체의 변형 없이 연산 모드를 순식간에 바꾼다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 아키텍처 심층 비교: 직렬(Serial) vs 병렬(Parallel)

| 비교 항목 | 직렬 가감산기 (Serial Adder-Subtractor) | 병렬 가감산기 (Parallel Adder-Subtractor) |
|:---|:---|:---|
| **데이터 처리 방식** | 비트를 하나씩 차례대로 시프트하며 연산 | 모든 비트를 동시에(Simultaneous) 입력 및 연산 |
| **속도 (Latency)** | 느림 (Clock Cycles = Bit Width) | **빠름 (Gate Delay only)** |
| **하드웨어 복잡도** | 단순 (FA 1개 + Shift Register) | 복잡 (FA N개 + Interconnects) |
| **전력 소모** | 낮음 (작동하는 소자가 적음) | 높음 (Glitching 발생 빈도 높음) |
| **용도** | 초저전력 IoT 센서, 메모리 내 연산 | 일반 범용 **CPU/GPU**의 ALU |

#### 2. 오버플로우 탐지 방식 비교 (Signed vs Unsigned)
시스템 아키텍트는 연산 결과를 어떻게 해석할지 명확히 정의해야 한다.

```text
┌───────────────────────────────────────────────────────────────┐
│                    Overflow Detection Logic                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Case A: Unsigned (부호 없는 정수)                            │
│  - Condition: Carry-Out (Cout) == 1                          │
│  - Ex: 255(11111111) + 1(00000001) = 0 with Carry(1)         │
│                                                               │
│  Case B: Signed (부호 있는 정수, 2's Complement)              │
│  - Condition: (Cin of MSB) XOR (Cout of MSB) == 1            │
│  - Ex: 127(01111111) + 1(00000001) = -128(10000000)          │
│    (Cin=1, Cout=0 -> V=1, Overflow Occurred!)                │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```
**과제 융합 관점**: 컴퓨터 구조(Computer Architecture)에서 **ISA**는 위 두 가지 경우 모두를 고려해야 한다. 예를 들어 x86의 `ADD` 명령어는 **CF (Carry Flag)**와 **OF (Overflow Flag)**를 동시에 업데이트하여, 소프트웨어 개발자가 데이터 타입에 따라 적절한 플래그를 선택하게 한다.

> **📢 섹션 요약 비유**: 트럭이 터널을 통과할 때, '높이 제한(부호)'에 따라 사고가 난 것인지, '무게 제한(비트 초과)'에 따라 사고가 난 것인지 구분하는 것처럼, 하드웨어는 결과값에 따라 서로 다른 경고 플래그를 동시에 제기해야 소프트웨어가 안전하게 처리할 수 있다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 고성능 ALU 설계에서의 타이밍 최적화
- **상황**: 32비트 RISC 프로세서 설계 중, 단일 클럭 사이클(1 Cycle) 내에 모든 산술 연산을 완료해야 한다.
- **문제**: 병렬 가감산기의 **캐리 리플(Carry Ripple)** 경로가 너무 길어서 Critical Path가 됨.
- **해결 (기술적 판단)**:
    1.  **Ripple Carry Parallel Adder** 포기.
    2.  **CLA (Carry Look-ahead Adder)** 기반의 가감산기로 변경: 캐리를 미리 계산하는 로직(G/P 생성 및 PG 블록)을 추가하여 지연 시간을 $O(n)$에서 $O(\log n)$으로 최적화.
    3.  **CSA (Carry Save Adder)** 도입 고려: 곱셈기(Multiplier) 내부의 부분합(Partial Product) 가산 시 XOR 기반 가감산기 구조를 응용하여 캐리 무시 후 최종 합산.

#### 2. 도입 체크리스트 및 안티패턴

| 구분 | 체크 항목 | 설명 |
|:---|:---|:---|
| **설계** | **Timing Margin** | XOR 게이트의 지연이 클럭 주기(Tclock) 내에 수용되는가? (특히 M 신호가 변경될 때의 Glitch 주의) |
| **검증** | **Code Coverage** | 시뮬레