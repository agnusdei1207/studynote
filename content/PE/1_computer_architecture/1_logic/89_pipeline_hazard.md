+++
title = "파이프라인 헤저드 (Pipeline Hazard)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "CPU"]
draft = false
+++

# 파이프라인 헤저드 (Pipeline Hazard)

## 핵심 인사이트 (3줄 요약)
1. 파이프라인 헤저드는 파이프라인 효율을 저해하는 요소로, Structural(자원 경합), Data(데이터 의존성), Control(분기) 헤저드가 있다
2. 기술사시험에서는 RAW/WAR/WAW 의존성, Forwarding, Stall, Branch Prediction의 원리와 해결 기법이 핵심이다
3. 헤저드를 최소화하는 하드웨어/소프트웨어 기법이 파이프라인 성능을 결정한다

## Ⅰ. 개요 (500자 이상)

파이프라인 헤저드(Pipeline Hazard)는 **파이프라인에서 명령어가 원활하게 실행되지 못하고 대기해야 하는 상황**을 말한다. 헤저드로 인해 파이프라인에 Bubble(공백)이 발생하고 CPI가 1보다 커지며 처리량이 저하된다.

```
헤저드 기본 개념:
정의: 파이프라인 실행 방해 요소
결과: Stall, Bubble, CPI 증가
유형: Structural, Data, Control

영향:
- 명령어 완료 지연
- 파이프라인 효율 저하
- 하드웨어 복잡도 증가

성능 저하:
Stall Cycles / Total Cycles = 성능 저하율

예:
100 명령어, 10 Stalls
CPI = (100 + 10) / 100 = 1.1
성능 = 1 / 1.1 = 91% (이상적 대비)
```

**헤저드의 3대 유형:**

```
1. Structural Hazard (구조적 헤저드):
   - 하드웨어 자원 경합
   - 해결: 자원 복제, 분리

2. Data Hazard (데이터 헤저드):
   - 데이터 의존성
   - 해결: Forwarding, Stall

3. Control Hazard (제어 헤저드):
   - 분기 명령어
   - 해결: Prediction, Delay Slot
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Structural Hazard

```
구조적 헤저드:

정의:
두 명령어가 동시에 동일한 하드웨어 자원을 사용

예 1: 메모리 경합
IF 단계: 명령어 메모리 접근
MEM 단계: 데이터 메모리 접근

단일 포트 메모리: 경합 발생
해결: Harvard Architecture (분리된 메모리)

┌─────────────┐     ┌─────────────┐
│  I-Memory   │     │  D-Memory   │
│  (Instructions)│   │  (Data)     │
└─────────────┘     └─────────────┘

예 2: 레지스터 포트 경합
ID 단계: 2개 레지스터 읽기
WB 단계: 1개 레지스터 쓰기

3포트 필요: 2 Read + 1 Write
해결: 레지스터 포트 증설

예 3: ALU 경합
EX 단계: ALU 연산
Address 계산: ALU 필요

해결: 별도 Address ALU
```

### Data Hazard

```
데이터 헤저드:

정의:
명령어 간 데이터 의존성으로 인한 대기

1. RAW (Read After Write) - True Dependence:
   명령어 i가 쓴 값을 명령어 j가 읽어야 함

   I1: ADD R1, R2, R3   ; R1 ← R2 + R3
   I2: SUB R4, R1, R5   ; R4 ← R1 - R5
              ↑
          R1이 필요하지만 I1이 완료 안 됨

2. WAR (Write After Read) - Anti-Dependence:
   명령어 j가 쓰기 전에 i가 읽어야 함

   I1: ADD R1, R2, R3   ; R3 사용
   I2: SUB R3, R4, R5   ; R3에 쓰기
          ↑
      I1이 R3를 다 읽기 전에 I2가 쓰면 문제

3. WAW (Write After Write) - Output Dependence:
   두 명령어가 같은 레지스터에 쓰기

   I1: ADD R1, R2, R3   ; R1에 쓰기
   I2: SUB R1, R4, R5   ; R1에 쓰기
          ↑
     최종값이 어느 것인지?

의존성 확인:
distance = j - i (명령어 간격)

RAW: distance가 1이면 Hazard
WAR: Out-of-Order에서만 문제
WAW: Out-of-Order에서만 문제
```

### Data Hazard Detection

```
헤저드 감지 하드웨어:

ID 단계에서:
1. 현재 명령어의 Source 레지스터 확인
2. ID/EX 레지스터의 Destination 확인
3. EX/MEM 레지스터의 Destination 확인

조건:
if (ID/EX.MemRead and
    (ID/EX.Rt == IF/ID.Rs or ID/EX.Rt == IF/ID.Rt))
    Hazard detected
    Stall 필요

예:
LW R1, 0(R2)     ; Load (ID/EX.MemRead = 1)
ADD R3, R1, R4   ; R1 필요 (IF/ID.Rs == R1)
    ↑
ID/EX.Rt == IF/ID.Rs → Hazard!
```

### Data Hazard Resolution

```
해결 기법 1: Forwarding (Bypassing)

원리:
완료된 단계의 결과를 바로 사용

경로:
EX/MEM.Result → EX.ALU.Input
MEM/WB.Result → EX.ALU.Input
MEM/WB.MemoryData → EX.ALU.Input

적용 가능:
ADD R1, R2, R3   ; EX 단계 완료
SUB R4, R1, R5   ; EX 단계에서 R1 필요
    ↓
EX/MEM.Result → EX.A (Forwarding)

적용 불가:
LW R1, 0(R2)    ; MEM 단계에서 로드
ADD R3, R1, R4   ; EX 단계에서 R1 필요
    ↓
Forwarding 불가 (MEM 단계 완료 필요)
Stall 필요 (Load-Use Hazard)
```

```
해결 기법 2: Pipeline Stall (Bubble)

Stall 삽입:
- Hazard Unit이 감지
- PC, IF/ID 레지스터 Freeze
- ID/EX 레지스터에 Bubble 삽입

예 (Load-Use):
Cycle:  1   2   3   4   5   6
LW:    IF  ID  EX  MEM WB
ADD:       IF  ID  ST  EX  MEM WB
SUB:           IF  ID  EX  MEM WB
                        ↑
                    Stall Cycle (NOP)

CPI = 1 + (Stalls / Instructions)
```

```
해결 기법 3: Compiler Scheduling

원리:
의존성 있는 명령어 분리

Before:
LW R1, 0(R2)
ADD R4, R1, R5    ; Hazard
SUB R6, R7, R8

After (재배치):
LW R1, 0(R2)
SUB R6, R7, R8    ; 독립적 명령어 삽입
ADD R4, R1, R5    ; Hazard 해결

효과:
- Stall 없음
- 코드 크기 유지
- Compiler 최적화
```

### Control Hazard

```
제어 헤저드:

정의:
분기 명령어로 인한 파이프라인 흐름 변경

문제:
1. 분기 결정 전에 다음 명령어 IF
2. 분기 시 이미 가져온 명령어 무효

Cycle:  1   2   3   4   5   6
BEQ:    IF  ID  EX  MEM WB
Inst N:      IF  ID  EX  MEM WB
Inst N+1:        IF  ID  EX  MEM WB
                   ↓
            Branch taken, 무효!

Penalty:
2-3 명령어 무효
```

### Branch Prediction

```
정적 예측:

1. Always Taken:
   - 모든 분기를 실행으로 예측
   - Loop에 유리 (90% taken)

2. Always Not Taken:
   - 모든 분기를 무시로 예측
   - Fall-through에 유리

3. BTB (Branch Target Buffer):
   - 과거 분기 목적지 캐싱
   - Address → Target Address

동적 예측:

1-bit Saturating Counter:
State: {Taken, NotTaken}
- Predict correct: 유지
- Mispredict: 반전

2-bit Saturating Counter:
States: {00, 01, 10, 11}
00: Strong Not Taken
01: Weak Not Taken
10: Weak Taken
11: Strong Taken

Transition:
Taken:  state → max(state + 1, 11)
NotTaken: state → min(state - 1, 00)

2-level Adaptive:
Pattern History Table (PHT)
Global History Register (GHR)
BHR ⊕ Address → PHT Index

Tournament Predictor:
Local + Global + Meta predictor
최고 성능
```

### Branch Delay Slot

```
분기 지연 슬롯:

분기 명령어 다음 N개 명령어는
항상 실행 (분기 여부 무관)

예 (MIPS, 1 slot):
BEQ R1, R2, Target
ADD R3, R4, R5    ; 항상 실행
SUB R6, R7, R8    ; 분기 시 무시
J Target

Compiler 채움:
1. 유용한 명령어 (있으면)
2. NOP (없으면)

효과:
- Stall 없음
- 단순한 하드웨어
- Compiler 부담

문제:
- Slot을 채울 명령어 없음
- 코드 배치 제약
```

### Speculative Execution

```
추론 실행 (Speculation):

분기 예측에 따라 미리 실행
Misprediction 시 Rollback

과정:
1. Branch Prediction
2. Speculative Fetch
3. Speculative Execute
4. Resolution
5. Commit or Rollback

Reorder Buffer (ROB):
- 실행 순서 유지
- 추론 실행 상태 추적
- In-order Commit

장점:
- Branch Penalty 숨김
- ILP 증가

단점:
- 복잡한 하드웨어
- 잘못된 실행 낭비
```

## Ⅲ. 융합 비교

### 헤저드 유형 비교

| 헤저드 | 원인 | 해결 | 비용 |
|--------|------|------|------|
| Structural | 자원 경합 | 복제 | 높음 |
| Data RAW | 의존성 | Forwarding | 중간 |
| Data WAR/WAW | 명명 충돌 | Renaming | 낮음 |
| Control | 분기 | Prediction | 높음 |

### Forwarding 효과

| 상황 | Forwarding 없음 | Forwarding 있음 | 개선 |
|------|----------------|-----------------|------|
| EX → EX | 1 Stall | 0 Stall | 100% |
| MEM → EX | 2 Stalls | 0 Stall | 100% |
| Load → Use | 1 Stall | 1 Stall | 0% |

### 예측 기법 비교

| 기법 | 정확도 | 비용 | Penalty |
|------|--------|------|---------|
| Always NT | 50% | 0 | 중간 |
| 1-bit | ~70% | 낮음 | 중간 |
| 2-bit | ~85% | 낮음 | 작음 |
| 2-level | ~95% | 중간 | 작음 |

## Ⅳ. 실무 적용 및 기술사적 판단

### MIPS 헤저드 해결

```
MIPS R3000 Hazard Resolution:

1. Structural:
   - Separate I/D Cache
   - 3-port Register File (2R, 1W)
   - Dedicated Adder for PC

2. Data:
   - Forwarding from EX/MEM, MEM/WB
   - Stall for Load-Use

3. Control:
   - Branch Delay Slot (1)
   - Static Prediction (Not Taken)

Hazard Detection Unit:
   if (ID/EX.MemRead and
       ((ID/EX.Rt == IF/ID.Rs) or
        (ID/EX.Rt == IF/ID.Rt)))
       Stall = 1
```

### ARM 헤저드 해결

```
ARM Cortex Hazard Handling:

1. Data Hazard:
   - Full Forwarding network
   - Dynamic interlocking
   - Load/Store scheduling

2. Control Hazard:
   - Dynamic branch prediction
   - Return stack (for calls)
   - Indirect branch prediction

3. Structural:
   - Multiple execution units
   - Multi-port register file
   - Separate I/D TLB
```

### Register Renaming

```
레지스터 리네이밍:

WAW, WAR 의존성 제거

Architected Register → Physical Register

R1 (Archtected) → P5 (Physical)
R1 (Archtected) → P12 (Physical)

예:
I1: ADD R1, R2, R3   ; R1 → P1
I2: SUB R4, R1, R5   ; P1 사용 (RAW)
I3: MUL R1, R6, R7   ; R1 → P2 (WAW 제거)

Reorder Buffer (ROB):
- 할당된 Physical Register 추적
- Free List 관리
- Retirement 시 해제
```

## Ⅴ. 기대효과 및 결론

파이프라인 헤저드는 성능의 주 enemy다. Forwarding, Prediction, Renaming 등 하드웨어 기법과 Compiler Scheduling으로 최소화해야 한다.

```python
"""
파이프라인 헤저드 시뮬레이션
Pipeline Hazard Simulator
"""

class PipelineHazardSimulator:
    """파이프라인 헤저드 시뮬레이터"""

    def __init__(self):
        self.regs = {f'R{i}': 0 for i in range(32)}
        self.pipeline = [None] * 5  # IF, ID, EX, MEM, WB
        self.cycle = 0
        self.stalls = 0
        self.forwarding = True

    def execute_program(self, instructions):
        """프로그램 실행"""
        print("=" * 70)
        print("Pipeline Hazard Simulation")
        print("=" * 70)

        pc = 0
        complete = 0

        while complete < len(instructions):
            self.cycle += 1
            print(f"\n=== Cycle {self.cycle} ===")

            # 파이프라인 시프트
            complete += self._wb_stage()
            self._mem_stage()
            self._ex_stage()
            self._id_stage()

            # IF 단계
            if pc < len(instructions):
                inst = instructions[pc]
                self._if_stage(inst)
                pc += 1

            # 파이프라인 상태 출력
            self._dump_pipeline()

    def _if_stage(self, inst):
        """Instruction Fetch"""
        self.pipeline[0] = {'inst': inst, 'pc': self.cycle}
        print(f"IF: {inst[0]} {', '.join(map(str, inst[1:]))}")

    def _id_stage(self):
        """Instruction Decode (Hazard Detection)"""
        if self.pipeline[0] is None:
            self.pipeline[1] = None
            return

        inst = self.pipeline[0]['inst']
        opcode = inst[0]

        # 헤저드 확인
        hazard = self._detect_hazard(inst)
        if hazard:
            print(f"ID: {opcode} - HAZARD DETECTED ({hazard}), Stalling")
            self.stalls += 1
            self.pipeline[0] = None  # Freeze
            return

        # 헤저드 없으면 진행
        self.pipeline[1] = self.pipeline[0]
        self.pipeline[0] = None
        print(f"ID: Decoded {opcode}")

    def _detect_hazard(self, inst):
        """헤저드 감지"""
        if len(inst) < 3:
            return None

        # 현재 명령어가 읽는 레지스터
        src_regs = []
        for op in inst[1:2]:  # 첫 2개 소스
            if isinstance(op, str) and op.startswith('R'):
                src_regs.append(op)

        # EX/MEM, MEM/WB에 있는 쓰기 레지스터 확인
        for stage in [self.pipeline[2], self.pipeline[3]]:
            if stage is None:
                continue
            prev_inst = stage['inst']
            if len(prev_inst) >= 3:
                dst = prev_inst[-1]  # 목적지 레지스터
                if dst in src_regs:
                    # Forwarding으로 해결 가능한지 확인
                    if self.forwarding and stage == self.pipeline[2]:
                        return None  # EX/MEM에서 forwarding 가능
                    elif prev_inst[0] == 'LW':
                        return 'Load-Use (RAW)'
                    else:
                        return 'RAW'

        return None

    def _ex_stage(self):
        """Execute"""
        if self.pipeline[1] is None:
            self.pipeline[2] = None
            return

        inst = self.pipeline[1]['inst']
        self.pipeline[2] = self.pipeline[1]
        self.pipeline[1] = None
        print(f"EX: Executing {inst[0]}")

    def _mem_stage(self):
        """Memory Access"""
        if self.pipeline[2] is None:
            self.pipeline[3] = None
            return

        inst = self.pipeline[2]['inst']
        self.pipeline[3] = self.pipeline[2]
        self.pipeline[2] = None
        print(f"MEM: Accessing memory")

    def _wb_stage(self):
        """Write Back"""
        if self.pipeline[3] is None:
            return 0

        inst = self.pipeline[3]['inst']
        self.pipeline[3] = None
        print(f"WB: Completed {inst[0]}")
        return 1

    def _dump_pipeline(self):
        """파이프라인 상태"""
        stages = ['IF', 'ID', 'EX', 'MEM', 'WB']
        line = []
        for i, stage in enumerate(stages):
            if self.pipeline[i]:
                inst = self.pipeline[i]['inst']
                line.append(f"{stage}:{inst[0]}")
            else:
                line.append(f"{stage}:---")
        print("  │ " + " │ ".join(line))

    def get_stats(self):
        """통계"""
        print(f"\n=== Statistics ===")
        print(f"Total Cycles: {self.cycle}")
        print(f"Stalls: {self.stalls}")
        print(f"CPI: {self.cycle / max(1, self.cycle - self.stalls):.2f}")


def demo_raw_hazard():
    """RAW 헤저드 데모"""

    print("\n" + "=" * 70)
    print("RAW (Read After Write) Hazard Demo")
    print("=" * 70)

    sim = PipelineHazardSimulator()

    program = [
        ('ADD', 'R1', 'R2', 'R3'),   # R3 = R1 + R2
        ('SUB', 'R4', 'R3', 'R5'),   # R4 = R3 - R5 (RAW on R3)
        ('MUL', 'R6', 'R4', 'R7'),   # R6 = R4 * R7 (RAW on R4)
    ]

    sim.execute_program(program)
    sim.get_stats()


def demo_load_use_hazard():
    """Load-Use 헤저드 데모"""

    print("\n\n" + "=" * 70)
    print("Load-Use Hazard Demo")
    print("=" * 70)

    sim = PipelineHazardSimulator()

    program = [
        ('LW', 'R1', '0', 'R2'),    # R1 = Mem[R2 + 0]
        ('ADD', 'R3', 'R1', 'R4'),   # R3 = R1 + R4 (Load-Use!)
    ]

    sim.execute_program(program)
    sim.get_stats()


def demo_forwarding():
    """Forwarding 효과 데모"""

    print("\n\n" + "=" * 70)
    print("Forwarding Effect Demo")
    print("=" * 70)

    # Without forwarding
    print("\n### Without Forwarding:")
    sim_no_fw = PipelineHazardSimulator()
    sim_no_fw.forwarding = False

    program = [
        ('ADD', 'R1', 'R2', 'R3'),
        ('SUB', 'R4', 'R1', 'R5'),
    ]

    sim_no_fw.execute_program(program)

    # With forwarding
    print("\n\n### With Forwarding:")
    sim_fw = PipelineHazardSimulator()
    sim_fw.forwarding = True

    sim_fw.execute_program(program)


def demo_branch_hazard():
    """Branch 헤저드 데모"""

    print("\n\n" + "=" * 70)
    print("Branch Hazard Demo")
    print("=" * 70)

    explanation = """
    Control Hazard 발생:

    BEQ R1, R2, Target
    (분기 결정은 EX 단계에서)

    Cycle:  1   2   3   4   5
    BEQ:    IF  ID  EX  MEM WB
    N:           IF  ID  (취소)
    N+1:            IF  (취소)

    Penalty: 2 cycles

    해결:
    1. Branch Prediction: 미리 예측
    2. Delay Slot: 항상 실행
    3. Early Resolution: ID 단계에서 결정
    """

    print(explanation)


def demo_comparison():
    """비교"""

    print("\n\n" + "=" * 70)
    print("Hazard Resolution Comparison")
    print("=" * 70)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Data Hazard Resolution                          │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │ 1. Forwarding (Bypassing):                                         │
    │    - EX/MEM, MEM/WB → EX                                          │
    │    - 대부분 RAW 해결                                               │
    │    - Load-Use는 해결 안 됨                                          │
    │                                                                     │
    │ 2. Pipeline Stall:                                                 │
    │    - Hazard 시 Bubble 삽입                                         │
    │    - CPI 증가                                                      │
    │    - Load-Use에 필요                                               │
    │                                                                     │
    │ 3. Compiler Scheduling:                                           │
    │    - 의존성 분리                                                    │
    │    - 독립적 명령어 재배치                                           │
    │    - 소프트웨어 해법                                                │
    │                                                                     │
    │ 4. Register Renaming (Out-of-Order):                              │
    │    - WAR, WAW 제거                                                 │
    │    - Architected → Physical                                        │
    │    - ROB 관리                                                      │
    │                                                                     │
    ──────────────────────────────────────────────────────────────────────

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Control Hazard Resolution                       │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │ 1. Static Prediction:                                              │
    │    - Always Taken / Not Taken                                     │
    │    - BTB (Branch Target Buffer)                                   │
    │    - 50-70% 정확도                                                 │
    │                                                                     │
    │ 2. Dynamic Prediction:                                             │
    │    - 1-bit, 2-bit Saturating Counter                              │
    │    - 2-level Adaptive                                             │
    │    - 85-95% 정확도                                                 │
    │                                                                     │
    │ 3. Branch Delay Slot:                                             │
    │    - 분기 다음 명령어 항상 실행                                     │
    │    - Compiler 채움                                                  │
    │    - 완전한 해결                                                    │
    │                                                                     │
    │ 4. Speculative Execution:                                         │
    │    - 예측에 따라 미리 실행                                          │
    │    - Misprediction 시 Rollback                                     │
    │    - 높은 ILP                                                      │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Stall Cycles by Hazard Type                     │
    ├─────────────────────────────────────────────────────────────────────┤
    │ Hazard Type           │ No Resolution │ Forwarding │ Full Resolve │
    ├────────────────────────┼────────────────┼────────────┼──────────────┤
    │ RAW (EX → EX)         │ 1              │ 0          │ 0            │
    │ RAW (MEM → EX)        │ 2              │ 0          │ 0            │
    │ Load-Use              │ 1              │ 1          │ 0 (scheduling)│
    │ Branch (mispredict)   │ 2-3            │ 2-3        │ 1 (prediction)│
    └────────────────────────┴────────────────┴────────────┴──────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_raw_hazard()
    demo_load_use_hazard()
    demo_forwarding()
    demo_branch_hazard()
    demo_comparison()
