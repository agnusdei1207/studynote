+++
title = "마스터-슬레이브 플립플롭 (Master-Slave Flip-Flop)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# 마스터-슬레이브 플립플롭 (Master-Slave Flip-Flop)

## 핵심 인사이트 (3줄 요약)
1. 마스터-슬레이브 플립플롭은 두 개의 래치를 직렬로 연결하여 에지 트리거 동작을 구현하는 회로로, 클럭=1일 때 Master가 입력을 받고 클럭=0일 때 Slave로 전달하여 Race Condition을 방지한다
2. Master 래치는 Clk=1에서 활성(Transparent)되고 Slave는 Clk=0에서 활성되며, 이 직렬 구조는 입력이 출력에 투명하게 전달되는 것을 방지한다
3. 기술사시험에서는 마스터-슬레이브 구조의 에지 트리거 원리, Race Condition 방지, D 플립플롭 구현이 핵심이다

## Ⅰ. 개요 (500자 이상)

마스터-슬레이브 플립플롭(Master-Slave Flip-Flop)은 **두 개의 래치(Latch)를 직렬로 연결하여 클럭 에지 트리거 동작을 안정적으로 구현**하는 순차 회로이다. 일반적인 래치가 클럭의 활성 레벨에서 투명하게 동작하는 반면, 마스터-슬레이브 구조는 클럭의 에지에서만 데이터 전송이 발생하도록 설계되었다.

```
마스터-슬레이브 개념:
구조: 2개 래치 직렬 연결
- Master Latch: Clk=1에서 활성
- Slave Latch: Clk=0에서 활성

동작:
Clk=1: Master 활성, Slave 래치 (입력 → Master)
Clk=0: Master 래치, Slave 활성 (Master → Slave → 출력)

특징:
- 에지 트리거 동작
- 투명성 제거
- Race Condition 방지
- 안정적인 상태 저장
```

**마스터-슬레이브의 핵심 특징:**

1. **에지 트리거**: 클럭의 상승/하강 에지에서만 데이터 전송
2. **비투명성**: 입력이 출력에 즉시 반영되지 않음
3. **Race Condition 방지**: 두 단계 처리로 경쟁 조건 최소화
4. **안정성**: 메타스터빌리티 위험 감소

```
일반 래치 vs 마스터-슬레이브:
일반 래치:
- Enable=1: 투명 (입력 → 출력)
- Enable=0: 래치 (상태 유지)

마스터-슬레이브:
- Clk=1: Master 투명, Slave 래치
- Clk=0: Master 래치, Slave 투명
- 결국: 에지에서만 전송
```

마스터-슬레이브 플립플롭은 D 플립플롭, JK 플립플롭 등 모든 에지 트리거 플립플롭의 표준 구현 방식이다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 마스터-슬레이브 회로 구조

```
마스터-슬레이브 D 플립플롭 구조:

D ───┐
     │
     ├── Master Latch ─── Qm
     │    │              │
Clk ─┴────┴──────────────┤
     │                   │
Clk' ───────────────────┤
     │                   └── Slave Latch ─── Q
     │
R ───┘ (D의 반전, Reset용)

Clk'는 Clk의 반전 (Inverter)
```

### 동작 순서

```
1단계: Clk=0 → 1 (상승 에지)
- Master 래치 해제 (투명 모드 시작)
- Slave 래치 활성화 (이전 상태 유지)
- D → Master (입력 캡처)

2단계: Clk=1 (활성 상태)
- Master: D를 계속 추적 (투명)
- Slave: Master의 이전 출력 유지

3단계: Clk=1 → 0 (하강 에지)
- Master 래치 활성화 (마지막)
- Slave 래치 해제 (투명 모드 시작)
- Master → Slave (전송)

결과: Clk 상승/하강 에지마다 D → Q 전송
```

### 타이밍 다이어그램

```
마스터-슬레이브 타이밍:

   D: ──┐   ┌───┐   ┌──┐
      │   │   │   │
Clk: ───┴─┬─┴───┴───┴───
            ↑   ↑
          상승 하강

   Qm: ───┐   ┌───┐
        │   │   │
        └───┴───┴──→ Q
              ↑
          Slave 전송

시점:
t1: Clk 상승 (0→1)
    - Master 활성, D → Qm
t2: Clk=1 동안
    - Qm = D (투명)
t3: Clk 하강 (1→0)
    - Master 래치, Qm → Q
t4: Clk=0 동안
    - Q 유지
```

### Race Condition 방지

```
문제: 1단계 래치의 Race Condition

일반 래치 (Enable=1):
D ──────┐
         │
         ├── Latch ── Q
         │
         └── 피드백 (Q')

문제:
- Enable=1일 때 피드백이 즉시 반영
- 불안정한 루프 형성
- 메타스터빌리티 발생

해결: 마스터-슬레이브

1. Master와 Slave 분리:
   - Master: 입력 받기만
   - Slave: 출력하기만

2. 교차 클럭:
   - Clk (Master)
   - Clk' (Slave)

3. 동시 활성 방지:
   - 하나만 투명 상태
```

### 전파 지연

```
마스터-슬레이브 지연:

1단계 (Master):
- Latch setup: 1-2 게이트

2단계 (Slave):
- Latch setup: 1-2 게이트

3. 총 지연:
t_pd = 2-4 게이트

@ 100ps/게이트:
t_pd = 200-400ps
f_max = 2.5-5 GHz

실제:
- 셋업/홀드 고려
- 일반적으로 1-2 GHz
```

### 다양한 마스터-슬레이브 플립플롭

```
D 플립플립플롭 (MS):

D ── Master ── Slave ── Q

JK 플립플롭 (MS):

J, K ── Master ── Slave ── Q

T 플립플롭 (MS):

T ── Master ── Slave ── Q

구조:
- Master: JK FF 기반 (J=K=T)
- Slave: JK FF 기반 (J=K=T)
- T=1 시 토글
```

## Ⅲ. 융합 비교

### 래치 vs 마스터-슬레이브 플립플롭

| 비교 항목 | 래치 | MS 플립플롭 |
|----------|------|-------------|
| 트리거 | 레벨 | 에지 |
| 클럭 | Enable | Clock |
| 투명성 | 있음 | 없음 |
| Race Condition | 위험 | 방지 |
| 응용 | 파이프라인 | 레지스터 |

### 에지 트리거 구현

| 방식 | 구조 | 지연 | 복잡도 |
|------|------|------|--------|
| Edge Detector | Detector + Latch | 작음 | 작음 |
| Master-Slave | 2 LATCH | 중간 | 중간 |
| 6 Transistor | 6T SRAM | 빠름 | 큼 |

### 플립플롭 성능 비교

| 타입 | 지연 | 전력 | 면적 | 응용 |
|------|------|------|------|------|
| MS D FF | 중간 | 중간 | 중간 | 일반 |
| Pulsed Latch | 빠름 | 낮음 | 작음 | 고성능 |
| Sense Amp | 매우 빠름 | 낮음 | 매우 큼 | SRAM |

## Ⅳ. 실무 적용 및 기술사적 판단

### SRAM 셀 설계

```
6T SRAM 셀 (마스터-슬레이브):

   VDD
    │
  ┌─┴─┐
  │PM │ ── Q (Master)
  └┬─┘
  │NM │
  └┬─┘
    │ Q'
    │
  Word Line
    │
  Bit Line

구조:
- 2개 인버터 = MS 래치
- 2개 액세 트랜지스터

특징:
- 정적 유지 (리프레시 불필요)
- 빠른 액세
- 안정적 동작
```

### 고성능 플립플롭

```
Sense Amplifier 기반 플립플롭:

D ── Write Driver ── Storage Node
                      │
                      └─ Sense Amp ── Q
                              ↑
                         Clk 에지

특징:
- 빠른 속도
- 낮은 전력
- 큰 면적

응용:
- SRAM
- 레지스터 파일
- 캐시 태그
```

### 동기식 시스템 설계

```
마스터-슬레이브 활용:

CPU 데이터패스:

Stage 1 ── MS D FF ── Stage 2 ── MS D FF ── Stage 3

동기:
- 공통 클럭
- 모든 FF 동시 상승 에지
- 파이프라인 동기

장점:
- 타이밍 예측 가능
- 합성 간단
- STA 용이

단점:
- 최대 클럭 제한
- 스큐 관리 필요
```

## Ⅴ. 기대효과 및 결론

마스터-슬레이브는 에지 트리거의 표준이다. 안정적인 동기화를 제공한다.

## 📌 관련 개념 맵

```
마스터-슬레이브 플립플롭
├── 구조
│   ├── Master Latch (Clk=1 활성)
│   └── Slave Latch (Clk=0 활성)
├── 동작
│   ├── Clk=0→1: Master 투명 시작
│   ├── Clk=1: Master 래치, Slave 추적
│   └── Clk=1→0: Master→Slave 전송
├── 특징
│   ├── 에지 트리거
│   ├── 비투명성 제거
│   └── Race Condition 방지
├── 구현
│   ├── D FF (MS)
│   ├── JK FF (MS)
│   └── T FF (MS)
└── 응용
    ├── SRAM 셀
    ├── 레지스터
    └── 동기 시스템
```

## 👶 어린이를 위한 3줄 비유 설명

1. 마스터-슬레이브 플립플랊은 두 방으로 나뉜 창고 같아요. 첫 번째 방(Master)에서 데이터를 받아두고, 문이 닫히면 두 번째 방(Slave)으로 전달해요
2. 클럭이 1일 때 Master가 열려서 D를 받고, 클럭이 0이 되면 Master가 닫히고 Slave가 열려서 Master에 있던 데이터를 출력으로 보내요
3. 이렇게 두 단계로 나누면 데이터가 덜덜� 보내져서 안정적으로 저장할 수 있어요. CPU의 레지스터가 이 방식으로 만들어져요

```python
# 마스터-슬레이브 플립플롭 시뮬레이션

from typing import List


class MasterSlaveDFF:
    """마스터-슬레이브 D 플립플롭 시뮬레이션"""

    def __init__(self):
        """MS D 플립플롭 초기화"""
        # Master 래치 상태
        self.master_q = 0
        self.master_q_prime = 1

        # Slave 래치 상태 (출력)
        self.slave_q = 0
        self.slave_q_prime = 1

        self.prev_clk = 0

    def clock(self, d: int, clk: int) -> tuple:
        """
        클럭에 따른 상태 변화

        Args:
            d: Data 입력
            clk: 클럭 신호

        Returns:
            (q, q_prime): 출력 상태
        """
        if d not in [1, 0] or clk not in [1, 0]:
            raise ValueError("D, Clk는 0 또는 1이어야 합니다")

        # 상승 에지 검출
        if self.prev_clk == 0 and clk == 1:
            # Master 활성화, Slave 래치
            self.master_q = d
            self.master_q_prime = 1 - d
        # 하강 에지 검출
        elif self.prev_clk == 1 and clk == 0:
            # Master 래치, Slave 활성화
            self.slave_q = self.master_q
            self.slave_q_prime = self.master_q_prime

        self.prev_clk = clk
        return self.slave_q, self.slave_q_prime

    def get_state(self) -> tuple:
        """현재 상태 반환"""
        return self.slave_q, self.slave_q_prime

    def get_master_state(self) -> tuple:
        """Master 상태 반환"""
        return self.master_q, self.master_q_prime


class MultiBitMSDFF:
    """다중 비트 MS D 플립플롭"""

    def __init__(self, bits: int):
        """
        n비트 MS D 플립플롭

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.ffs = [MasterSlaveDFF() for _ in range(bits)]

    def clock(self, data: int, clk: int) -> List[int]:
        """
        클럭에 따른 상태 변화

        Args:
            data: 입력 데이터 (정수)
            clk: 클럭 신호

        Returns:
            상태 리스트
        """
        if not (0 <= data < 2**self.bits):
            raise ValueError(f"데이터는 {self.bits}비트 범위 내여야 합니다")

        outputs = []
        for i in range(self.bits):
            bit = (data >> i) & 1
            self.ffs[i].clock(bit, clk)
            outputs.append(self.ffs[i].get_state()[0])

        return outputs

    def get_state(self) -> int:
        """전체 상태를 정수로 반환"""
        value = 0
        for i in range(self.bits):
            value |= self.ffs[i].get_state()[0] << i
        return value


class SynchronousPipeline:
    """동기식 파이프라인"""

    def __init__(self, stages: int, bits: int = 8):
        """
        파이프라인 초기화

        Args:
            stages: 스테이지 수
            bits: 데이터 비트 수
        """
        self.stages = stages
        self.bits = bits
        self.registers = [MultiBitMSDFF(bits) for _ in range(stages)]

    def cycle(self, input_data: int, clk: int) -> List[int]:
        """
        한 파이프라인 사이클

        Args:
            input_data: 입력 데이터
            clk: 클럭 신호 (0→1→0)

        Returns:
            각 스테이지 출력
        """
        outputs = []

        # 입력 → 첫 번째 레지스터
        self.registers[0].clock(input_data, clk)
        outputs.append(self.registers[0].get_state())

        # 레지스터 간 데이터 전송
        for i in range(1, self.stages):
            prev_data = self.registers[i-1].get_state()
            self.registers[i].clock(prev_data, clk)
            outputs.append(self.registers[i].get_state())

        return outputs


def demonstration():
    """마스터-슬레이브 플립플롭 데모"""
    print("="*60)
    print("마스터-슬레이브 플립플롭 (Master-Slave FF) 데모")
    print("="*60)

    # MS D FF
    print("\n[마스터-슬레이브 D 플립플롭]")
    ms_dff = MasterSlaveDFF()

    # 시뮬레이션
    test_sequence = [
        (1, 0, "초기"),
        (0, 1, "무시 (Clk=0)"),
        (1, 1, "상승 에지, D=1 → Master=1"),
        (0, 0, "무시 (Clk=1)"),
        (0, 1, "하강 에지, Master→Slave=1"),
        (1, 1, "상승 에지, D=1 → Master=1"),
        (1, 0, "하강 에지, Master→Slave=1"),
        (0, 1, "상승 에지, D=0 → Master=0"),
    ]

    print(f"{'D':<3} {'Clk':<4} {'Master Q':<10} {'Slave Q':<9} {'설명':<20}")
    print("-" * 50)

    for d, clk, desc in test_sequence:
        q, _ = ms_dff.clock(d, clk)
        mq, _ = ms_dff.get_master_state()
        print(f"{d:<3} {clk:<4} {mq:<10} {q:<9} {desc:<20}")

    # 8비트 레지스터
    print(f"\n[8비트 레지스터 (MS FF 기반)]")
    reg_8bit = MultiBitMSDFF(8)

    # 데이터: 0xAA → 0x55 → 0xFF
    test_data = [0xAA, 0x55, 0xFF]

    for data in test_data:
        # 클럭 사이클 (0→1→0)
        reg_8bit.clock(data, 1)
        print(f"D=0x{data:02X} → Q=0x{reg_8bit.get_state():02X}")

    # 파이프라인
    print(f"\n[3단계 파이프라인]")
    pipeline = SynchronousPipeline(stages=3, bits=4)

    # 데이터 10, 20, 30을 3사이클 통과
    for cycle in range(5):
        if cycle == 0:
            input_data = 10
        elif cycle == 1:
            input_data = 20
        elif cycle == 2:
            input_data = 30
        else:
            input_data = 0  # NOP

        outputs = pipeline.cycle(input_data, 1)
        print(f"Cycle {cycle}: Input={input_data:2d}, Outputs={[f'{o:2d}' for o in outputs]}")


if __name__ == "__main__":
    demonstration()
```
