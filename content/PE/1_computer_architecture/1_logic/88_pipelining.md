+++
title = "파이프라이닝 (Pipelining)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "CPU"]
draft = false
+++

# 파이프라이닝 (Pipelining)

## 핵심 인사이트 (3줄 요약)
1. 파이프라이닝(Pipelining)은 명령어 실행을 여러 단계로 나누어 겹쳐 실행함으로써 처리량을 향상시키는 기술이다
2. 기술사시험에서는 5단계 파이프라인(IF, ID, EX, MEM, WB), Pipeline Hazard(Structural, Data, Control), 해결 기법이 핵심이다
3. CPI(Cycles Per Instruction)를 1에 가깝게 만들지만, Hazard로 인해 Stall이 발생하여 성능이 저하될 수 있다

## Ⅰ. 개요 (500자 이상)

파이프라이닝(Pipelining)은 **CPU의 명령어 실행을 여러 단계(Stage)로 나누어, 여러 명령어가 동시에 다른 단계를 수행하도록 하는 병렬 처리 기술**이다. 공장의 조립 라인과 같은 원리로, 단일 명령어 실행 시간은 줄지 않지만 전체 처리량(Throughput)은 크게 향상된다.

```
파이프라이닝 기본 개념:
정의: 명령어 실행 단계를 겹쳐서 실행
목적: 처리량(Throughput) 향상
원리: 시간적 병렬성 (Temporal Parallelism)

비파이프라인 vs 파이프라인:
비파이프라인:
  명령어 1: [단계1][단계2][단계3][단계4][단계5]
  명령어 2:                         [단계1][단계2]...

파이프라인:
  명령어 1: [단계1][단계2][단계3][단계4][단계5]
  명령어 2:        [단계1][단계2][단계3][단계4][단계5]
  명령어 3:               [단계1][단계2][단계3][단계4][단계5]
```

**파이프라이닝의 핵심 지표:**

1. **Throughput**: 단위 시간당 완료되는 명령어 수
2. **Latency**: 한 명령어의 실행 시간
3. **Speedup**: 비파이프라인 대비 성능 향상
4. **CPI**: Cycles Per Instruction (명령어당 사이클 수)

```
이상적인 파이프라인 성능:
- CPI = 1 (매 사이클마다 1 명령어 완료)
- Speedup = 파이프라인 단계 수 (이론적)

실제 성능:
- CPI > 1 (Hazard로 인한 Stall)
- Speedup < 단계 수 (Overhead, Hazard)
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 5단계 파이프라인

```
MIPS 5-Stage Pipeline:

1. IF (Instruction Fetch):
   - PC에서 명령어 가져오기
   - PC ← PC + 4

2. ID (Instruction Decode):
   - 명령어 해석
   - 레지스터 읽기
   - Imm 생성

3. EX (Execute):
   - ALU 연산
   - 주소 계산
   - 분기 조건 확인

4. MEM (Memory Access):
   - 데이터 로드/스토어
   - 분기 목적지 계산

5. WB (Write Back):
   - 결과 레지스터에 쓰기

타이밍 다이어그램:
Clock:    1    2    3    4    5    6    7
Inst 1:  IF   ID   EX   MEM  WB
Inst 2:       IF   ID   EX   MEM  WB
Inst 3:            IF   ID   EX   MEM  WB
Inst 4:                 IF   ID   EX   MEM  WB
Inst 5:                      IF   ID   EX   MEM  WB
```

### Pipeline Registers

```
파이프라인 레지스터 (Stage Latches):

IF/ID 레지스터:
- PC + 4
- Fetched Instruction
- (다음 단계로 전달)

ID/EX 레지스터:
- Decoded Opcode
- Register Values
- Immediate Value
- (해독된 정보)

EX/MEM 레지스터:
- ALU Result
- Zero Flag
- (EX 단계 결과)

MEM/WB 레지스터:
- Memory Data
- ALU Result
- (메모리/ALU 결과)

구조:
┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐
│IF │──→│ID │──→│EX │──→│MEM│──→│WB │
└───┘   └───┘   └───┘   └───┘   └───┘
  ↑                             ↓
  └─────────────────────────────┘
        (Feedback 경로)
```

### Pipeline Hazards

```
파이프라인 헤저드 (위험 상황):

1. Structural Hazard (구조적 헤저드):
   - 하드웨어 경합
   - 두 명령어가 동일한 자원 요구

   예:
   - 명령어 메모리와 데이터 메모리가 분리되지 않음
   - IF 단계와 MEM 단계가 메모리 충돌

   해결:
   - Harvard Architecture (분리된 메모리)
   - 캐시 분리 (I-Cache, D-Cache)
   - 자원 복제

2. Data Hazard (데이터 헤저드):
   - 데이터 의존성
   - 아직 계산되지 않은 데이터 참조

   유형:
   a) RAW (Read After Write):
      - True Dependence
      - 명령어 i가 쓴 값을 명령어 j가 읽음

      ADD R1, R2, R3   ; R1 = R2 + R3
      SUB R4, R1, R5   ; R1이 필요하지만 아직 안 써짐

   b) WAR (Write After Read):
      - Anti-Dependence
      - 명령어 j가 쓰기 전에 i가 읽어야 함

      ADD R1, R2, R3   ; R3 사용
      SUB R3, R4, R5   ; R3에 쓰기

   c) WAW (Write After Write):
      - Output Dependence
      - 두 명령어가 같은 레지스터에 쓰기

   해결:
   - Forwarding (Bypassing)
   - Pipeline Stall (Bubble)
   - Out-of-Order Execution

3. Control Hazard (제어 헤저드):
   - 분기 명령어로 인한 흐름 변경
   - 이미 가져온 명령어 무효화

   예:
   BEQ R1, R2, Target
   ; 분기 결정 전에 다음 명령어 IF

   해결:
   - Branch Delay Slot
   - Branch Prediction
   - Speculative Execution
```

### Data Forwarding

```
데이터 포워딩 (Bypassing):

문제:
EX 단계에서 이전 명령어의 결과 필요
하지만 결과는 WB 단계에서야 완료

해결:
EX/MEM, MEM/WB 레지스터의 값 바로 전달

예:
ADD R1, R2, R3   ; EX 단계에서 계산
SUB R4, R1, R5   ; R1 필요

Forwarding 없이:
ADD: EX → MEM → WB (R1에 쓰기)
SUB:        ID → EX (R1 필요, 대기 필요)

Forwarding 있이:
ADD: EX → (결과 바로 전달)
SUB:     EX (결과 사용)

경로:
1. EX/MEM → EX (ALU 결과)
2. MEM/WB → EX (메모리 로드 값)
```

### Pipeline Stall (Bubble)

```
파이프라인 스톨 (Bubble):

데이터 의존성으로 인해 대기 필요

예 (Load-Use Hazard):
LW R1, 0(R2)     ; MEM 단계에서 로드
ADD R3, R1, R4   ; ID 단계에서 R1 필요

해결:
LW:  IF ID EX MEM WB
ADD:      IF ID(stall) EX MEM WB
SUB:            IF ID EX MEM WB

Stall = NOP 삽입
CPI > 1

해결 기법:
1. Compiler Scheduling
   - 의존성 있는 명령어 분리
   - 독립적 명령어 삽입

2. Hardware Interlocking
   - 자동 Stall 삽입
   - Hazard Detection Unit
```

### Branch Prediction

```
분기 예측 (Branch Prediction):

정적 예측 (Static):
1. Always Taken:
   - 모든 분기를 실행으로 예측
   - Loop에 유리

2. Always Not Taken:
   - 모든 분기를 무시로 예측
   - Fall-through에 유리

3. BTB (Branch Target Buffer):
   - 과거 이력으로 예측

동적 예측 (Dynamic):
1. 1-bit Prediction:
   - 1-bit saturating counter
   - Taken/Not Taken 상태

   0: Not Taken
   1: Taken

2. 2-bit Prediction:
   - 2-bit saturating counter

   00: Strong Not Taken
   01: Weak Not Taken
   10: Weak Taken
   11: Strong Taken

3. 2-level Adaptive:
   - Global History
   - Local History
   - GShare (Global + XOR)

4. Tournament:
   - 여러 예측기 결합
   - Meta-predictor

성능:
- Prediction Accuracy: 90-99%
- Misprediction Penalty: 10-20 cycles
```

### Branch Delay Slot

```
분기 지연 슬롯 (Branch Delay Slot):

분기 명령어 다음의 명령어는
항상 실행 (분기 여부 무관)

예 (MIPS):
BEQ R1, R2, Target
ADD R3, R4, R5   ; Delay Slot (항상 실행)
J  Target

장점:
- 파이프라인 Stall 없음
- 간단한 하드웨어

단점:
- Compiler가 Slot 채워야 함
- 종종 NOP 발생
- 코드 배치 어려움

사용:
- 항상 실행되는 코드
- 독립적 명령어
```

### Out-of-Order Execution

```
비순차 실행 (Out-of-Order):

순서와 다르게 명령어 실행
의존성 없는 명령어 먼저 실행

구성 요소:
1. Register Renaming:
   - WAW, WAR 의존성 제거
   - Architected → Physical Register

2. Reorder Buffer (ROB):
   - 프로그램 순서 유지
   - In-order Retirement

3. Reservation Stations:
   - 명령어 대기
   - Operand 준비 확인

4. Scoreboarding:
   - Data 의존성 추적

예:
1. ADD R1, R2, R3   ; R2 준비 안 됨
2. MUL R4, R5, R6   ; 실행 가능 (먼저 실행)
3. SUB R7, R8, R9   ; 실행 가능
4. XOR R10, R1, R11 ; R1 대기 (1번 완료 후)

성능:
- ILP (Instruction Level Parallelism) 증가
- CPI < 1 (Superscalar)
- 복잡한 하드웨어
```

## Ⅲ. 융합 비교

### 파이프라인 단계 수

| 단계 | 아키텍처 | 특징 | CPI |
|------|----------|------|-----|
| 5 | MIPS R3000 | 기본 | 1 |
| 6 | ARM7 | 분리된 MEM/WB | 1 |
| 8 | ARM9 | 분리된 ID/EX | ~1 |
| 10+ | Superpipeline | 깊은 파이프라인 | <1 |

### Hazard 해결 기법

| Hazard | 기법 | 효과 | 비용 |
|--------|------|------|------|
| Structural | 자원 분리 | 완전 | 높음 |
| Data | Forwarding | 대부분 | 중간 |
| Data | Stall | 완전 | 성능저하 |
| Control | Prediction | 부분 | 높음 |
| Control | Delay Slot | 완전 | 제한적 |

### 분기 예측 기법

| 기법 | 정확도 | 복잡도 | 사용 |
|------|--------|--------|------|
| Always NT | 50% | 낮음 | 초기 |
| 1-bit | ~70% | 낮음 | 단순 |
| 2-bit | ~85% | 낮음 | 일반 |
| 2-level | ~95% | 중간 | 고성능 |
| Tournament | ~97% | 높음 | 최신 |

## Ⅳ. 실무 적용 및 기술사적 판단

### MIPS 파이프라인

```
MIPS 5-Stage Pipeline:

IF:
  IR ← Mem[PC]
  PC ← PC + 4

ID:
  A ← Reg[IR[25-21]]
  B ← Reg[IR[20-16]]
  Imm ← SignExtend(IR[15-0])

EX:
  ALUOutput ← A op B
  (or) ALUOutput ← A + Imm

MEM:
  LMD ← Mem[ALUOutput]  (Load)

WB:
  Reg[IR[20-16]] ← ALUOutput
  (or) Reg[IR[20-16]] ← LMD

Hazard Detection:
  if (ID/EX.MemRead and
      (ID/EX.Rt == IF/ID.Rs or
       ID/EX.Rt == IF/ID.Rt))
    Stall: PC ← PC - 4
           IF/ID ← IF/ID (freeze)
```

### ARM 파이프라인

```
ARM Pipeline Evolution:

ARM7 (3-stage):
  Fetch → Decode → Execute
  - 단순한 파이프라인
  - 낮은 클럭 속도

ARM9 (5-stage):
  Fetch → Decode → Execute → Memory → Write
  - Harvard Architecture
  - 더 높은 클럭

ARM11 (8-stage):
  Fetch1 → Fetch2 → Decode → Execute1 →
  Execute2 → Memory1 → Memory2 → Write
  - Superpipeline
  - 고성능

Cortex-A (10+ stages):
  - Deep pipeline
  - Out-of-Order
  - Superscalar
```

### Superpipeline

```
슈퍼파이프라인:

깊은 파이프라인 (많은 단계)
각 단계가 더 얕은 작업

장점:
- 더 높은 클럭 속도
- 더 많은 파이프라인 병렬성

단점:
- Branch Penalty 큼
- 더 많은 Pipeline Register
- 더 큰 Overhead

예:
- Pentium 4: 31-stage (NetBurst)
- 비판: 지나치게 깊음
- Prescott: 31-stage

Modern:
- Core: 14-19 stages
- 절충 안택
```

### Superscalar

```
슈퍼스칼라:

여러 명령어 동시 발급 (Issue)
Multiple Issue Pipeline

구조:
┌─────────────────────────────────────┐
│          Instruction Fetch          │
└─────────────────────────────────────┘
           ↓
┌─────────┬─────────┬─────────┬─────────┐
│  Issue  │  Issue  │  Issue  │  Issue  │
│  Port 0 │  Port 1 │  Port 2 │  Port 3 │
└─────────┴─────────┴─────────┴─────────┘
     ↓        ↓        ↓        ↓
  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
  │ ALU │  │ ALU │  │ MEM │  │ FP  │
  └─────┘  └─────┘  └─────┘  └─────┘

예:
- Intel Core: 4-6 issue
- AMD Zen: 4-6 issue
- Apple M1: 8 issue (high perf)

성능:
- Peak CPI = 0.16 (6-issue) = 0.16
- Real CPI = 0.3-0.5
```

## Ⅴ. 기대효과 및 결론

파이프라이닝은 CPU 성능의 핵심이다. Hazard를 최소화하고 예측 정확도를 높여 CPI를 1에 가깝게 만드는 것이 목표다.

```python
"""
파이프라이닝 시뮬레이션
Pipeline Simulator
"""

class Pipeline:
    """5단계 파이프라인 시뮬레이션"""

    def __init__(self):
        # 파이프라인 레지스터
        self.if_id = {}
        self.id_ex = {}
        self.ex_mem = {}
        self.mem_wb = {}

        # 레지스터 파일
        self.regs = {f'R{i}': 0 for i in range(32)}
        self.pc = 0

        # 메모리
        self.memory = {}

        # 파이프라인 상태
        self.stages = ['IF', 'ID', 'EX', 'MEM', 'WB']
        self.cycle = 0

        # 통계
        self.instructions_completed = 0
        self.stalls = 0
        self.branches = 0
        self.mispredictions = 0

    def step(self, instruction=None):
        """한 사이클 실행"""
        self.cycle += 1
        print(f"\n=== Cycle {self.cycle} ===")

        # WB 단계
        self._wb_stage()

        # MEM 단계
        self._mem_stage()

        # EX 단계
        self._ex_stage()

        # ID 단계
        self._id_stage()

        # IF 단계
        self._if_stage(instruction)

    def _if_stage(self, instruction):
        """Instruction Fetch"""
        if instruction is None:
            # Bubble
            self.if_id = {'valid': False}
            print("IF: (Bubble)")
        else:
            self.if_id = {
                'valid': True,
                'pc': self.pc,
                'opcode': instruction[0],
                'operands': instruction[1:]
            }
            self.pc += 4
            print(f"IF: {instruction[0]} {', '.join(map(str, instruction[1:]))}")

    def _id_stage(self):
        """Instruction Decode"""
        if not self.if_id.get('valid', False):
            self.id_ex = {'valid': False}
            print("ID: (Bubble)")
            return

        opcode = self.if_id['opcode']
        operands = self.if_id['operands']

        # 레지스터 읽기
        reg_values = []
        for op in operands[:2]:  # 최대 2개
            if isinstance(op, str) and op.startswith('R'):
                reg_values.append(self.regs.get(op, 0))
            else:
                reg_values.append(op)

        self.id_ex = {
            'valid': True,
            'opcode': opcode,
            'operands': operands,
            'reg_values': reg_values
        }
        print(f"ID: Decoded {opcode}, operands: {reg_values}")

    def _ex_stage(self):
        """Execute"""
        if not self.id_ex.get('valid', False):
            self.ex_mem = {'valid': False}
            print("EX: (Bubble)")
            return

        opcode = self.id_ex['opcode']
        values = self.id_ex['reg_values']

        # ALU 연산
        if opcode == 'ADD':
            result = values[0] + values[1]
        elif opcode == 'SUB':
            result = values[0] - values[1]
        elif opcode == 'MUL':
            result = values[0] * values[1]
        elif opcode == 'LW':
            result = values[0] + values[1]  # 주소 계산
        else:
            result = 0

        self.ex_mem = {
            'valid': True,
            'opcode': opcode,
            'result': result,
            'dest': self.id_ex['operands'][2] if len(self.id_ex['operands']) > 2 else None
        }
        print(f"EX: {opcode} result = {result}")

    def _mem_stage(self):
        """Memory Access"""
        if not self.ex_mem.get('valid', False):
            self.mem_wb = {'valid': False}
            print("MEM: (Bubble)")
            return

        opcode = self.ex_mem['opcode']
        result = self.ex_mem['result']

        if opcode == 'LW':
            # Load from memory
            data = self.memory.get(result, 0)
            self.mem_wb = {
                'valid': True,
                'opcode': opcode,
                'result': data,
                'dest': self.ex_mem['dest']
            }
            print(f"MEM: Loaded {data} from addr {result}")
        elif opcode == 'SW':
            # Store to memory
            dest = self.ex_mem['dest']
            self.memory[dest] = result
            self.mem_wb = {'valid': True, 'opcode': opcode}
            print(f"MEM: Stored {result} to addr {dest}")
        else:
            self.mem_wb = {
                'valid': True,
                'opcode': opcode,
                'result': result,
                'dest': self.ex_mem['dest']
            }
            print(f"MEM: No memory operation")

    def _wb_stage(self):
        """Write Back"""
        if not self.mem_wb.get('valid', False):
            print("WB: (Bubble)")
            return

        opcode = self.mem_wb['opcode']
        if opcode in ['ADD', 'SUB', 'MUL', 'LW']:
            dest = self.mem_wb['dest']
            result = self.mem_wb['result']
            if dest:
                self.regs[dest] = result
                self.instructions_completed += 1
                print(f"WB: Wrote {result} to {dest}")
        else:
            self.instructions_completed += 1
            print("WB: Completed")

    def detect_hazard(self, inst1, inst2):
        """데이터 헤저드 감지"""
        # inst1이 inst2보다 먼저
        # inst2가 inst1의 결과를 사용하면 Hazard
        pass

    def get_stats(self):
        """통계 정보"""
        cpi = self.cycle / self.instructions_completed if self.instructions_completed > 0 else 0
        print(f"\n=== Statistics ===")
        print(f"Cycles: {self.cycle}")
        print(f"Instructions: {self.instructions_completed}")
        print(f"CPI: {cpi:.2f}")
        print(f"Stalls: {self.stalls}")
        if self.branches > 0:
            print(f"Branch Prediction Rate: {(1 - self.mispredictions/self.branches)*100:.1f}%")

    def dump_state(self):
        """현재 상태"""
        print(f"\nPC = 0x{self.pc:04X}")
        print(f"Registers: R0={self.regs['R0']}, R1={self.regs['R1']}, R2={self.regs['R2']}, R3={self.regs['R3']}")


def demo_pipeline():
    """파이프라인 실행 데모"""

    print("=" * 70)
    print("5단계 파이프라인 시뮬레이션")
    print("=" * 70)

    pipeline = Pipeline()

    # 테스트 프로그램
    program = [
        ('ADD', 'R0', 'R1', 'R2'),   # R2 = R0 + R1
        ('SUB', 'R2', 'R3', 'R4'),   # R4 = R2 - R3
        ('MUL', 'R4', 'R5', 'R6'),   # R6 = R4 * R5
        ('LW', 'R7', '100', 'R8'),   # R8 = Mem[R7+100]
    ]

    # 초기 레지스터 값
    pipeline.regs['R0'] = 10
    pipeline.regs['R1'] = 20
    pipeline.regs['R3'] = 5
    pipeline.regs['R5'] = 3

    print("\n### 초기 상태")
    pipeline.dump_state()

    # 파이프라인 실행
    for i in range(len(program) + 5):  # 5단계
        if i < len(program):
            inst = program[i]
        else:
            inst = None

        pipeline.step(inst)

    # 최종 상태
    print("\n### 최종 상태")
    pipeline.dump_state()
    pipeline.get_stats()


def demo_hazard():
    """데이터 헤저드 데모"""

    print("\n\n" + "=" * 70)
    print("데이터 헤저드 (Data Hazard)")
    print("=" * 70)

    explanation = """
    RAW (Read After Write) Hazard:

    ADD R1, R2, R3   ; EX 단계에서 R1 계산
    SUB R4, R1, R5   ; ID 단계에서 R1 필요 (대기!)

    타임라인:
    Cycle:  1    2    3    4    5    6
    ADD:   IF   ID   EX   MEM  WB
    SUB:        IF   ID   ST   EX   MEM  WB
                                ↑
                          Stall inserted

    해결: Forwarding
    - EX/MEM 레지스터에서 바로 R1 전달
    - Stall 불필요
    """
    print(explanation)


def demo_branch_prediction():
    """분기 예측 데모"""

    print("\n\n" + "=" * 70)
    print("분기 예측 (Branch Prediction)")
    print("=" * 70)

    class BranchPredictor:
        """2-bit Saturating Counter 예측기"""

        def __init__(self):
            self.states = {}  # PC → state (00, 01, 10, 11)
            self.predictions = []
            self.correct = 0
            self.total = 0

        def predict(self, pc):
            state = self.states.get(pc, '10')  # 초기: Weak Taken
            taken = state in ['10', '11']
            self.predictions.append((pc, taken))
            return taken

        def update(self, pc, actual_taken):
            state = self.states.get(pc, '10')

            # State transition
            if actual_taken:
                if state == '00': state = '01'
                elif state == '01': state = '10'
                elif state == '10': state = '11'
                # 11 remains 11
            else:
                if state == '11': state = '10'
                elif state == '10': state = '01'
                elif state == '01': state = '00'
                # 00 remains 00

            self.states[pc] = state

            # Check prediction
            predicted = self.predictions[-1][1] if self.predictions else True
            if predicted == actual_taken:
                self.correct += 1
            self.total += 1

    # 시뮬레이션
    bp = BranchPredictor()

    # Branch history
    branches = [
        (0x1000, True), (0x1000, True), (0x1000, False),
        (0x1000, False), (0x1000, True), (0x1000, True),
        (0x2000, True), (0x2000, False), (0x2000, False),
    ]

    print("\n### 2-bit Predictor Simulation")
    for pc, taken in branches:
        predicted = bp.predict(pc)
        result = "✓" if predicted == taken else "✗"
        state = bp.states.get(pc, '10')
        print(f"PC={pc:04X}, Predicted={predicted:5}, Actual={taken:5}, State={state} {result}")
        bp.update(pc, taken)

    accuracy = bp.correct / bp.total * 100 if bp.total > 0 else 0
    print(f"\nAccuracy: {bp.correct}/{bp.total} = {accuracy:.1f}%")


def demo_comparison():
    """비교"""

    print("\n\n" + "=" * 70)
    print("파이프라이닝 기법 비교")
    print("=" * 70)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Pipeline Depth Comparison                      │
    ├───────────┬─────────────┬─────────────┬─────────────────────────────┤
    │ Depth     │ 예시        │ 클럭        │ 장점/단점                  │
    ├───────────┼─────────────┼─────────────┼─────────────────────────────┤
    │ 얕음 (3-5)│ ARM7, MIPS  │ 낮음 (~100MHz)│ 저전력, 단순함            │
    │           │ R3000       │             │                             │
    ├───────────┼─────────────┼─────────────┼─────────────────────────────┤
    │ 중간 (6-10)│ ARM9, Core │ 중간 (~1GHz) │ 균형                       │
    │           │ 2 Duo      │             │                             │
    ├───────────┼─────────────┼─────────────┼─────────────────────────────┤
    │ 깊음 (15+)│ NetBurst   │ 높음 (~3GHz) │ 고클럭, 큰 분기 페널티     │
    │           │ (Pentium 4)│             │                             │
    └───────────┴─────────────┴─────────────┴─────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Hazard Resolution Techniques                    │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │ Data Hazard:                                                        │
    │   1. Forwarding (Bypassing)                                        │
    │      - EX/MEM, MEM/WB → EX                                        │
    │      - 대부분의 RAW 해결                                           │
    │                                                                     │
    │   2. Pipeline Stall (Bubble)                                       │
    │      - Load-Use Hazard                                            │
    │      - NOP 삽입                                                    │
    │                                                                     │
    │   3. Compiler Scheduling                                          │
    │      - 의존성 분리                                                  │
    │      - Independent instruction 이동                                 │
    │                                                                     │
    │ Control Hazard:                                                     │
    │   1. Branch Delay Slot                                            │
    │      - 분기 다음 명령어 항상 실행                                   │
    │      - MIPS: 1 slot                                                │
    │                                                                     │
    │   2. Static Prediction                                            │
    │      - Always taken/not taken                                      │
    │      - BTB (Branch Target Buffer)                                  │
    │                                                                     │
    │   3. Dynamic Prediction                                           │
    │      - 1-bit, 2-bit saturating counter                             │
    │      - 2-level adaptive                                            │
    │      - Tournament predictor                                        │
    │                                                                     │
    │   4. Speculative Execution                                        │
    │      - 예측에 따라 미리 실행                                        │
    │      - Misprediction 시 Rollback                                   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_pipeline()
    demo_hazard()
    demo_branch_prediction()
    demo_comparison()
