+++
title = "D 래치 (D Latch)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# D 래치 (D Latch)

## 핵심 인사이트 (3줄 요약)
1. D 래치는 SR 래치의 금지 상태(S=R=1) 문제를 해결하기 위해 D(Data)와 E(Enable) 입력을 가지며, E=1일 때 D를 Q로 전달하고 E=0일 때 상태를 유지한다
2. D 래치는 "투명(Transparent)"한 특성을 가지며, Enable 활성화期间 입력이 직접 출력으로 전달되어 파이프라인 레지스터에 사용된다
3. 기술사시험에서는 D 래치의 투명성, D 플립플롭과의 차이, 셋업/홀드 시간, 타이밍 위반이 핵심이다

## Ⅰ. 개요 (500자 이상)

D 래치(Data Latch)는 **SR 래치의 금지 상태 문제를 해결하고 단일 데이터 입력으로 1비트 정보를 저장**하는 순차 논리 회로이다. SR 래치에서 S와 R이 동시에 1이 되는 금지 상태를 방지하기 위해, D 래치는 하나의 데이터 입력 D와 Enable 입력 E를 사용한다.

```
D 래치 기본 개념:
입력: D (Data), E (Enable 또는 Gate)
출력: Q (상태), Q' (반전 상태)

동작:
- E=1 (활성): Q ← D (투명 모드)
- E=0 (비활성): Q 유지 (래치 모드)
```

**D 래치의 핵심 특징:**

1. **단일 데이터 입력**: S, R 대신 D 하나만 필요
2. **금지 상태 없음**: D의 값에 따라 자동으로 S, R이 결정
3. **투명성(Transparency)**: E=1일 때 D의 변화가 즉시 Q에 반영
4. **레벨 트리거**: Enable 신호의 레벨(0 또는 1)에 반응

```
SR 래치에서 D 래치로의 변환:

S ← D
R ← D' (반전)

E=1: S=D, R=D'에 따라 동작
- D=1: S=1, R=0 → Set (Q=1)
- D=0: S=0, R=1 → Reset (Q=0)

E=0: S=0, R=0 → 상태 유지
```

D 래치는 파이프라인 레지스터, 버스 래치, 임시 저장 등에 사용되며, D 플립플롭과 달리 클럭의 레벨(에지가 아닌)에 반응한다는 점에서 차이가 있다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### D 래치 회로 구조

```
D 래치 회로 (NOR 기반):

E ───┐
     │
D ───┼──┐   ┌── NOR ─── Q
     │  └──┤    │
     │     └─┬─┴── NOR ← Q' 피드백
     └─── NOT  │
                │
             Enable에 의한 제어

구조:
S = D · E
R = D' · E

E=1: S=D, R=D' → D에 따라 Set/Reset
E=0: S=0, R=0 → 상태 유지
```

### 진리표

```
D 래치 진리표:
| E | D | Q(t+1) | 동작 |
|---|---|--------|------|
| 0 | X | Q(t) | 유지 (Latch) |
| 1 | 0 |   0   | Reset (Q←0) |
| 1 | 1 |   1   | Set (Q←1) |

E=0: D 값 무관, 이전 상태 유지
E=1: D 값이 Q로 전달
```

### 투명성 (Transparency)

```
D 래치 투명 모드:

E=1期间:
D 변화 → 즉시 Q에 반영

타이밍:
   D: ──┐   ┌───┐   ┌──
       │   │   │   │
   E: ────┴───┴───┴──→
       └─── 투명 ───┘

   Q: ────┐   ┌───┐   ┌──
       └───┘   └───┘   └──

투명 모드 (E=1):
- D 변화가 Q에 바로 반영
- 지연: 2-3 게이트
- Q는 D를 "따라감(Follow)"

래치 모드 (E=0):
- Q 값 고정 (저장)
- D 변화 무시
```

### 전파 지연 및 타이밍

```
D 래치 타이밍 파라미터:

1. 셋업 시간 (t_setup):
   D가 E의 하강 에지 이전에 안정되어야 할 시간
   일반적으로 1-2 게이트 지연 이전

2. 홀드 시간 (t_hold):
   D가 E의 하강 에지 이후에 유지되어야 할 시간
   일반적으로 0-1 게이트 지연

3. 전파 지연 (t_pd):
   D → Q: 2-3 게이트 (E=1)
   E → Q: 1-2 게이트

타이밍 다이어그램:
   D: ───┐           ┌────┐
          │           │    │
   E: ───┴───────┬───┴────┴───
                 │   ↑
                 │   Latch (하강 에지)
                 │
  t_setup>│<t_hold>
```

### 메타스터빌리티

```
D 래치 메타스터빌리티:

셋업/홀드 위반 시:
- Q가 불안정한 상태로 진입
- 0과 1 사이를 오버슈팅
- 안정화까지 추가 시간 소요

회로적 원인:
- 피드백 경로가 데이터를 충분히 잠금
- 경쟁 조건 (Race Condition)
- 결정 시간 (Resolution Time)

복구:
- 안정화까지 2-3 게이트 추가
- 신뢰할 수 없는 값
- 설계에서 절대 피해야 함
```

### 다중 비트 D 래치

```
n비트 D 래치:

D[n-1:0] ──┬── D Latch 0 ── Q[0]
           ├── D Latch 1 ── Q[1]
           ├── ...         ── ...
           └── D Latch n-1 ── Q[n-1]
                    │
           E (공통 Enable)

용도:
- n비트 병렬 데이터 저장
- 레지스터 파일
- 버스 래치

지연:
- 각 비트 독립: 2-3 게이트
- 모든 비트 동시: 2-3 게이트
```

## Ⅲ. 융합 비교

### D 래치 vs D 플립플롭

| 비교 항목 | D 래치 | D 플립플롭 |
|----------|--------|-----------|
| 트리거 | 레벨 (Level) | 에지 (Edge) |
| 클럭 | 활성 상태에서 투명 | 상승/하강 에지에서만 |
| 투명성 | 있음 | 없음 |
| 셋업/홀드 | 필요 | 필요 |
| 응용 | 파이프라인 | 일반 레지스터 |
| 타이밍 제어 | 쉬움 | 어려움 |

### 래치 vs 플립플롭 설계

| 측면 | 래치 | 플립플롭 |
|------|------|----------|
| 타이밍 마진 | 낮음 | 높음 |
| 클럭 스큐 | 문제 있음 | 없음 |
| 합성 | 간단 | 복잡 |
| 속도 | 빠름 | 중간 |
| 면적 | 작음 | 큼 |
| 전력 | 낮음 | 중간 |

### 래치 종류 비교

| 타입 | 입력 | 출력 | 특징 | 응용 |
|------|------|------|------|------|
| SR 래치 | S, R | Q, Q' | 금지 상태 | 기본 |
| D 래치 | D, E | Q, Q' | 금지 없음 | 레지스터 |
| JK 래치 | J, K, Clk | Q, Q' | 토글 | 카운터 |
| T 래치 | T, Clk | Q, Q' | 토글 전용 | 카운터 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 파이프라인 레지스터

```
파이프라인 스테이지 간 래치:

Stage 1 ── D 래치 ── Stage 2 ── D 래치 ── Stage 3

클럭 분할:
Clk1: Stage 1 활성
Clk2: Stage 2 활성
Clk3: Stage 3 활성

타이밍:
Clk1=1: Stage 1 출력 → 래치 (투명)
Clk1=0: 래치에 값 저장 (Stage 2 입력)

장점:
- 오버랩 가능 (Clk1=0, Clk2=1)
- 최대 처리량
- 파이프라인 간 데이터 버퍼

단점:
- 타이밍 마진 감소
- 클럭 스큐 위험
```

### 버스 래치

```
CPU 내부 버스 래치:

     ALU
      │
      ↓
  [D Latch] ← Bus Buffer
      │
   Internal Bus
      │
      ├─ [D Latch] → Register File
      ├─ [D Latch] → Memory
      └─ [D Latch] → I/O

동작:
1. ALU 결과 버퍼링
2. 버스 충돌 방지
3. 비동기 데이터 전송

지연:
- 래치: 2 게이트
- 버스 구동: 1-2 게이트
- 총: 3-4 게이트
```

### 타이밍 위반 방지

```
설계 고려사항:

1. 셋업 시간 확보:
   - D 경로 지연 최소화
   - E 지연 최대화 (경로 조정)

2. 홀드 시간 확보:
   - D 경로 지연 삽입
   - 버퍼 배치

3. 클럭 경로 조정:
   - Clock Skew 최소화
   - Clock Tree 사용

STA (Static Timing Analysis):
- Worst-case 분석
- Setup/Slack 확인
- Hold Slack 확인
```

## Ⅴ. 기대효과 및 결론

D 래치는 데이터 저장의 기본이다. 투명성을 활용한 파이프라인에 필수적이다.

## 📌 관련 개념 맵

```
D 래치
├── 구조
│   ├── D 입력 (Data)
│   ├── E 입력 (Enable)
│   └── Q, Q' 출력
├── 동작
│   ├── E=1: 투명 (Q ← D)
│   └── E=0: 래치 (Q 유지)
├── 특성
│   ├── 투명성 (Transparency)
│   ├── 금지 상태 없음
│   └── 레벨 트리거
├── 타이밍
│   ├── 셋업 시간
│   ├── 홀드 시간
│   └── 전파 지연
└── 응용
    ├── 파이프라인
    ├── 버스 래치
    └── 레지스터
```

## 👶 어린이를 위한 3줄 비유 설명

1. D 래치는 문처럼 열림(E=1)과 닫힘(E=0) 상태가 있는 1비트 저장 장치예요. 문이 열려 있으면 D가 가진 값이 그대로 Q로 통과하고, 문이 닫히면 Q 값이 고정돼요
2. E=1일 때는 D가 0이면 Q도 0이 되고, D가 1이면 Q도 1이 돼요. E가 0이 되면 D가 변해도 Q는 변하지 않고 이전 값을 유지해요
3. 컴퓨터 파이프라인에서 데이터를 잠시 저장하고 다음 단계로 넘길 때 D 래치를 사용해요

```python
# D 래치 시뮬레이션

from typing import List, Tuple


class DLatch:
    """D 래치 시뮬레이션"""

    def __init__(self, initial_q: int = 0):
        """
        D 래치 초기화

        Args:
            initial_q: 초기 Q 값
        """
        self.q = initial_q
        self.q_prime = 1 - initial_q

    def set_inputs(self, d: int, e: int) -> Tuple[int, int]:
        """
        D, E 입력 설정

        Args:
            d: Data 입력 (0 또는 1)
            e: Enable 입력 (0 또는 1)

        Returns:
            (q, q_prime): 새로운 상태
        """
        if d not in [0, 1] or e not in [0, 1]:
            raise ValueError("D, E는 0 또는 1이어야 합니다")

        if e == 1:
            # 투명 모드: Q ← D
            self.q = d
            self.q_prime = 1 - d
        # else: e == 0 → 상태 유지

        return self.q, self.q_prime

    def get_state(self) -> Tuple[int, int]:
        """현재 상태 반환"""
        return self.q, self.q_prime


class MultiBitDLatch:
    """다중 비트 D 래치"""

    def __init__(self, bits: int):
        """
        n비트 D 래치

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.latches = [DLatch() for _ in range(bits)]

    def set_inputs(self, data: int, enable: int) -> List[int]:
        """
        다중 비트 입력

        Args:
            data: 입력 데이터 (정수)
            enable: Enable 신호

        Returns:
            상태 리스트
        """
        if not (0 <= data < 2**self.bits):
            raise ValueError(f"데이터는 {self.bits}비트 범위 내여야 합니다")

        outputs = []
        for i in range(self.bits):
            bit = (data >> i) & 1
            self.latches[i].set_inputs(bit, enable)
            outputs.append(self.latches[i].get_state()[0])

        return outputs

    def get_state(self) -> int:
        """전체 상태를 정수로 반환"""
        value = 0
        for i in range(self.bits):
            value |= self.latches[i].get_state()[0] << i
        return value


class PipelineRegister:
    """파이프라인 레지스터 시뮬레이션"""

    def __init__(self, stages: int, bits: int = 8):
        """
        파이프라인 레지스터

        Args:
            stages: 파이프라인 스테이지 수
            bits: 데이터 비트 수
        """
        self.stages = stages
        self.latches = [MultiBitDLatch(bits) for _ in range(stages)]
        self.current_clock = [0] * stages

    def clock_cycle(self, stage_data: List[int]) -> List[int]:
        """
        한 클럭 사이클 실행

        Args:
            stage_data: 각 스테이지의 입력 데이터

        Returns:
            각 스테이지의 출력 데이터
        """
        outputs = []

        for i in range(self.stages):
            # 클럭 패턴 생성 (교차 활성)
            enable = 1 if (i + self.current_clock[i]) % 2 == 1 else 0

            data = stage_data[i] if i < len(stage_data) else 0
            result = self.latches[i].set_inputs(data, enable)

            # 정수로 변환
            value = 0
            for j, bit in enumerate(result):
                value |= bit << j

            outputs.append(value)

            if enable:
                self.current_clock[i] += 1

        return outputs


def demonstration():
    """D 래치 데모"""
    print("="*60)
    print("D 래치 (D Latch) 데모")
    print("="*60)

    # D 래치
    print("\n[D 래치 진리표]")
    print(f"{'E':<3} {'D':<3} {'Q(t+1)':<8} {'동작':<10}")
    print("-" * 30)

    latch = DLatch()

    test_cases = [
        (0, 0, "유지"),
        (0, 1, "유지"),
        (1, 0, "Q←0"),
        (1, 1, "Q←1"),
    ]

    for e, d, action in test_cases:
        old_q = latch.q
        latch.set_inputs(d, e)
        state_str = f"{latch.q} ({'변경' if latch.q != old_q else '유지'})"
        print(f"{e:<3} {d:<3} {state_str:<8} {action:<10}")

    # 다중 비트 D 래치
    print(f"\n[8비트 D 래치]")
    latch8 = MultiBitDLatch(8)

    print(f"Enable=0, Data=0xFF: {latch8.set_inputs(0xFF, 0)}")
    print(f"  상태 유지: {latch8.get_state():08b} (0)")

    print(f"Enable=1, Data=0xAA: {latch8.set_inputs(0xAA, 1)}")
    print(f"  Q ← D: {latch8.get_state():08b} (170)")

    print(f"Enable=0, Data=0x55: {latch8.set_inputs(0x55, 0)}")
    print(f"  상태 유지: {latch8.get_state():08b} (170)")

    print(f"Enable=1, Data=0x55: {latch8.set_inputs(0x55, 1)}")
    print(f"  Q ← D: {latch8.get_state():08b} (85)")

    # 파이프라인 시뮬레이션
    print(f"\n[3단계 파이프라인]")
    pipeline = PipelineRegister(stages=3, bits=4)

    # 데이터: [10, 20, 30]
    stage_data = [10, 20, 30]

    print(f"입력: {stage_data}")

    for cycle in range(5):
        outputs = pipeline.clock_cycle(stage_data)
        print(f"클럭 {cycle}: 출력 = {outputs}")


if __name__ == "__main__":
    demonstration()
```
