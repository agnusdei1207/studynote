+++
title = "SR 래치 (SR Latch)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# SR 래치 (SR Latch)

## 핵심 인사이트 (3줄 요약)
1. SR 래치는 S(Set)와 R(Reset) 입력에 의해 1비트 데이터를 저장하는 최소 순차 회로로, 두 개의 NOR 또는 NAND 게이트로 구성되며 피드백 경로가 상태를 유지한다
2. NOR 게이트 SR 래치는 활성 High 입력, NAND 게이트 SR 래치는 활성 Low 입력을 가지며, S=1이면 Q=1(Set), R=1이면 Q=0(Reset)으로 동작한다
3. 기술사시험에서는 SR 래치의 진리표, 금지 상태(S=R=1), 메모리 셀 기본 구조, 래치와 플립플롭의 차이가 핵심이다

## Ⅰ. 개요 (500자 이상)

SR 래치(Set-Reset Latch)는 **1비트 정보를 저장할 수 있는 가장 기본적인 순차 논리 회로**이다. 조합 회로가 입력에만 의존하여 출력을 결정하는 반면, 순차 회로는 현재 입력과 이전 상태에 따라 출력을 결정한다. SR 래치는 두 개의 게이트가 피드백 경로를 형성하여 상태를 유지한다.

```
SR 래치 기본 개념:
입력: S (Set), R (Reset)
출력: Q (상태), Q' (반전 상태)

상태:
- S=1: Q=1 (Set, 1 저장)
- R=1: Q=0 (Reset, 0 저장)
- S=R=0: 상태 유지 (Hold)
- S=R=1: 금지 (정의되지 않음)
```

**SR 래치의 핵심 특징:**

1. **비휘발성 메모리 기본 단위**: 전원이 공급되는 한 상태 유지
2. **피드백 구조**: 출력이 입력으로 피드백되어 상태 유지
3. **두 가지 구현**: NOR 게이트 또는 NAND 게이트로 구현

```
피드백 구조:
Q → R 게이트 입력
Q' → S 게이트 입력

이 피드백이 상태를 "래치(Latch)"시킴
```

SR 래치는 메모리 셀, 레지스터, 스위치 디바운싱 등 다양한 응용에 사용된다. 특히 SRAM(Static RAM)의 기본 저장 셀은 SR 래치의 변형이다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### NOR 게이트 SR 래치

```
NOR SR 래치 회로:

S ───┐
     │
     ├── NOR ─── Q
     │    │      │
R ────┼────────┤
     │  │       │
     │  └── NOR ─── Q'
     │         │
     └─────────┘ (피드백)

불 대수식:
Q = (S + R·Q')' = S' · (R + Q')
Q' = (R + S·Q)' = R' · (S + Q)
```

```
NOR SR 래치 진리표:
| S | R | Q(t+1) | Q'(t+1) | 동작 |
|---|---|--------|---------|------|
| 0 | 0 | Q(t) | Q'(t) | 유지 (Hold) |
| 0 | 1 |   0   |    1    | Reset (Q=0) |
| 1 | 0 |   1   |    0    | Set (Q=1) |
| 1 | 1 |   X   |    X    | 금지 |

설명:
- S=1, R=0: Q=1로 설정 (Set)
- S=0, R=1: Q=0로 설정 (Reset)
- S=0, R=0: 이전 상태 유지
- S=1, R=1: 정의되지 않음 (Q=Q'=1 불가능)
```

### NAND 게이트 SR 래치

```
NAND SR 래치 회로 (활성 Low):

S' ──┐
     │
     ├── NAND ─── Q
     │    │       │
R' ───┼─────────┤
     │  │        │
     │  └── NAND ─── Q'
     │          │
     └──────────┘ (피드백)

진리표:
| S' | R' | Q(t+1) | 동작 |
|----|----|--------|------|
| 0 | 0 |   X    | 금지 |
| 0 | 1 |   1    | Set |
| 1 | 0 |   0    | Reset |
| 1 | 1 | Q(t) | 유지 |

S'=0, R'=1 → Set (S 입력 활성)
S'=1, R'=0 → Reset (R 입력 활성)
```

### 타이밍 다이어그램

```
SR 래치 타이밍 (NOR):

   S: ────┐       ┌───────
          │       │
   R: ──────┐   ┌───┐
              │   │   │
   Q: ────────┘   └───┘
              Set   Reset
   0   ────────1─────0───
              유지   유지

시점 분석:
t1: S=1, R=0 → Q=1 (Set)
t2: S=0, R=0 → Q=1 유지
t3: S=0, R=1 → Q=0 (Reset)
t4: S=0, R=0 → Q=0 유지
```

### 전파 지연 분석

```
SR 래치 지연:

NOR 구현:
- 게이트 지연: t_NOR
- Q 업데이트: t_NOR (입력 → 출력)
- 피드백: 추가 t_NOR (상태 안정화)

총 지연: 2 × t_NOR

@ 100ps/NOR:
t_setup = 200ps
최대 클럭: 1 / 200ps = 5 GHz

실제:
- 셋업/홀드 시간 고려
- 일반적으로 1-2 GHz 범위
```

### 메타스터블 상태

```
금지 상태 (S=R=1, NOR):

NOR 게이트 출력:
Q = (1 + 1)' = 0
Q' = (1 + 1)' = 0

Q = Q' = 0 (불가능, 상호 보정 필요)

회로 동작:
- 두 NOR 게이트가 모두 0 출력
- 피드백 불안정
- 최종 상태는 게이트 지연에 따라 결정
- 경쟁 조건 (Race Condition)

실제 영향:
- 전력 소모 증가
- 신호 글리치 가능
- 설계에서 피해야 함
```

## Ⅲ. 융합 비교

### NOR vs NAND SR 래치

| 비교 항목 | NOR SR 래치 | NAND SR 래치 |
|----------|-------------|--------------|
| 활성 입력 | High (S=1, R=1) | Low (S'=0, R'=0) |
| 정상 상태 | S=R=0 | S'=R'=1 |
| Set 조건 | S=1, R=0 | S'=0, R'=1 |
| Reset 조건 | S=0, R=1 | S'=1, R'=0 |
| 금지 상태 | S=R=1 | S'=R'=0 |
| 게이트 수 | 2 NOR | 2 NAND |
| 응용 | 일반적 | 활성 Low 시스템 |

### 래치 vs 플립플롭

| 비교 항목 | 래치 | 플립플롭 |
|----------|------|----------|
| 클럭 | 없음 (Level sensitive) | 있음 (Edge triggered) |
| 입력 동기 | 즉시 반영 | 클럭 에지에서만 |
| 투명성 | 투명 (Transparent) | 불투명 |
| 응용 | 임시 저장, 디바운싱 | 레지스터, 메모리 |
| 안정성 | 낮음 (Glitch) | 높음 |

### 1비트 메모리 구현

| 방식 | 회로 | 속도 | 면적 | 전력 | 응용 |
|------|------|------|------|------|------|
| SR 래치 | NOR/NAND × 2 | 빠름 | 중간 | 높음 | SRAM 셀 |
| D 래치 | MUX + INV | 빠름 | 작음 | 중간 | 파이프라인 |
| D 플립플롭 | Master-Slave | 중간 | 큼 | 중간 | 레지스터 |

## Ⅳ. 실무 적용 및 기술사적 판단

### SRAM 셀 구조

```
6T SRAM 셀 (6개 트랜지스터):

       VDD
        │
    ┌───┴───┐
    │  PMOS │
    └───┬───┘
        │ Q
    ┌───┴───┐
    │  NMOS │ ← Bit Line
    └───┬───┘
        │
   Word Line

SR 래치 변형:
- 2개 인버터가 SR 래치 형성
- 2개 전달 트랜지스터 (Bit Line 접근)
- 총 6T = 4T (래치) + 2T (액세스)

특징:
- 정적: 리프레시 불필요
- 빠른 액세스
- 낮은 대기 전력
- 높은 셀 면적
```

### 스위치 디바운싱

```
메커니컬 스위치 디바운싱:

스위치 → SR 래치 → 클린 출력

회로:
   VDD
    │
   ┌┴┐
   │ │ R (Pull-up)
   └┬┘
    │ Q
 스위치 ─── S
    │
   GND

동작:
- 스위치 닫힘 (S=GND): S=0, R=1 → Q=0
- 스위치 열림 (S=VDD): S=1, R=0 → Q=1
- 바운스: 래치가 첫 번째 변화만 캡처
- 출력: 깨끗한 신호

용도:
- 키보드 스위치
- 리미트 스위치
- 푸시 버튼
```

### 레지스터 파일

```
SR 래치 기반 레지스터:

N개의 SR 래치로 N비트 레지스터

Write:
- Write Enable=1: 입력 D → 래치 입력 S/R
- 클럭에 동기하여 쓰기

Read:
- Read Enable=1: 래치 출력 Q → 버스
- 비동기 읽기 가능

CPU 레지스터 파일:
- 32개 × 32비트 래치 배열
- 2포트 읽기, 1포트 쓰기
- 병렬 액세스

지연:
- 쓰기: 1 클럭
- 읽기: 조합 회로 (즉시)
```

## Ⅴ. 기대효과 및 결론

SR 래치는 순차 회로의 기초이다. 1비트 저장, 상태 유지, 메모리 셀의 핵심이다.

## 📌 관련 개념 맵

```
SR 래치
├── 구현
│   ├── NOR 게이트 (활성 High)
│   └── NAND 게이트 (활성 Low)
├── 동작
│   ├── Set (S=1): Q=1
│   ├── Reset (R=1): Q=0
│   ├── Hold (S=R=0): 상태 유지
│   └── 금지 (S=R=1): 정의되지 않음
├── 응용
│   ├── SRAM 셀 (6T)
│   ├── 스위치 디바운싱
│   └── 레지스터
└── 관련
    ├── D 래치
    ├── 플립플롭
    └── 메모리
```

## 👶 어린이를 위한 3줄 비유 설명

1. SR 래치는 스위치 두 개로 제어하는 1비트 기억 장치예요. Set 스위치를 누르면 1을 저장하고, Reset 스위치를 누르면 0을 저장해요
2. 두 스위치를 다 놓으면(Set=0, Reset=0) 이전에 저장한 값을 그대로 유지해요. 전원이 끊기지 않으면 값을 계속 기억해요
3. 컴퓨터 메모리의 가장 작은 단위처럼, 수많은 래치가 모여서 레지스터와 캐시 메모리를 만들어요

```python
# SR 래치 시뮬레이션

from typing import Tuple


class NOR_SRLatch:
    """NOR 게이트 SR 래치"""

    def __init__(self, initial_q: int = 0):
        """
        SR 래치 초기화

        Args:
            initial_q: 초기 Q 값 (0 또는 1)
        """
        self.q = initial_q
        self.q_prime = 1 - initial_q

    def set_inputs(self, s: int, r: int) -> Tuple[int, int]:
        """
        S, R 입력 설정

        Args:
            s: Set 입력 (0 또는 1)
            r: Reset 입력 (0 또는 1)

        Returns:
            (q, q_prime): 새로운 상태
        """
        if s not in [0, 1] or r not in [0, 1]:
            raise ValueError("S, R은 0 또는 1이어야 합니다")

        if s == 1 and r == 1:
            # 금지 상태
            raise ValueError("S=R=1은 금지된 상태입니다")

        if s == 1 and r == 0:
            # Set
            self.q = 1
            self.q_prime = 0
        elif s == 0 and r == 1:
            # Reset
            self.q = 0
            self.q_prime = 1
        # else: s=0, r=0 → 상태 유지

        return self.q, self.q_prime

    def get_state(self) -> Tuple[int, int]:
        """현재 상태 반환"""
        return self.q, self.q_prime

    def reset(self):
        """래치 리셋 (Q=0)"""
        self.q = 0
        self.q_prime = 1


class NAND_SRLatch:
    """NAND 게이트 SR 래치 (활성 Low)"""

    def __init__(self, initial_q: int = 0):
        self.q = initial_q
        self.q_prime = 1 - initial_q

    def set_inputs(self, s_prime: int, r_prime: int) -> Tuple[int, int]:
        """
        S', R' 입력 설정 (활성 Low)

        Args:
            s_prime: S' 입력 (0 또는 1, 0=활성)
            r_prime: R' 입력 (0 또는 1, 0=활성)

        Returns:
            (q, q_prime): 새로운 상태
        """
        if s_prime not in [0, 1] or r_prime not in [0, 1]:
            raise ValueError("S', R'은 0 또는 1이어야 합니다")

        if s_prime == 0 and r_prime == 0:
            # 금지 상태
            raise ValueError("S'=R'=0은 금지된 상태입니다")

        if s_prime == 0 and r_prime == 1:
            # Set (S' 활성)
            self.q = 1
            self.q_prime = 0
        elif s_prime == 1 and r_prime == 0:
            # Reset (R' 활성)
            self.q = 0
            self.q_prime = 1
        # else: s'=1, r'=1 → 상태 유지

        return self.q, self.q_prime


class SwitchDebouncer:
    """스위치 디바운싱 (SR 래치 활용)"""

    def __init__(self):
        self.latch = NOR_SRLatch(initial_q=0)

    def process_switch(self, raw_signal: list) -> list:
        """
        노이즈 있는 스위치 신호 정리

        Args:
            raw_signal: [0, 1, 0, 1, 1, 1, ...] (바운스 포함)

        Returns:
            정리된 신호 리스트
        """
        clean_output = []

        for signal in raw_signal:
            # 신호를 S, R로 변환
            if signal == 1:
                s, r = 1, 0  # Set
            else:
                s, r = 0, 1  # Reset

            try:
                self.latch.set_inputs(s, r)
            except ValueError:
                pass  # 금지 상태 무시

            clean_output.append(self.latch.get_state()[0])

        return clean_output


def demonstration():
    """SR 래치 데모"""
    print("="*60)
    print("SR 래치 (SR Latch) 데모")
    print("="*60)

    # NOR SR 래치
    print("\n[NOR SR 래치 진리표]")
    print(f"{'S':<3} {'R':<3} {'Q(t+1)':<8} {'Q'(t+1)':<8} {'동작':<10}")
    print("-" * 40)

    latch = NOR_SRLatch()

    test_cases = [
        (0, 0, "유지"),
        (0, 1, "Reset"),
        (1, 0, "Set"),
    ]

    # 초기 상태: Q=0
    print(f"초기: Q={latch.q}")

    for s, r, action in test_cases:
        old_q = latch.q
        latch.set_inputs(s, r)
        print(f"{s:<3} {r:<3} {latch.q:<8} {latch.q_prime:<8} {action:<10}")

    # 금지 상태 시도
    print("\n[금지 상태 시도]")
    try:
        latch.set_inputs(1, 1)
    except ValueError as e:
        print(f"  S=1, R=1 → {e}")

    # NAND SR 래치
    print(f"\n[NAND SR 래치 (활성 Low)]")
    nand_latch = NAND_SRLatch()
    nand_latch.set_inputs(0, 1)  # Set
    print(f"  S'=0, R'=1 → Q={nand_latch.q} (Set)")
    nand_latch.set_inputs(1, 0)  # Reset
    print(f"  S'=1, R'=0 → Q={nand_latch.q} (Reset)")

    # 스위치 디바운싱
    print(f"\n[스위치 디바운싱]")
    debouncer = SwitchDebouncer()

    # 바운스 있는 신호
    noisy_signal = [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
    print(f"입력 (바운스): {noisy_signal}")

    clean = debouncer.process_switch(noisy_signal)
    print(f"출력 (정리):  {clean}")


if __name__ == "__main__":
    demonstration()
```
