+++
title = "디멀티플렉서 (Demultiplexer, DEMUX)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# �멀티플렉서 (Demultiplexer, DEMUX)

## 핵심 인사이트 (3줄 요약)
1. 디멀티플렉서(DEMUX)는 1개 입력을 2^n개 출력 중 하나로 전달하는 조합 회로로, 멀티플렉서의 역기능을 수행하며 데이터 라우팅, 주소 디코딩, 메모리 쓰기 제어에 사용된다
2. n비트 선택선(Sel)에 따라 입력을 해당 출력으로 전송하며, 1-to-2, 1-to-4, 1-to-8 등이 있고 Enable 입력으로 출력 활성화를 제어한다
3. 기술사시험에서는 DEMUX와 MUX의 관계, 디코더와의 차이, 캐스케이딩, 데이터 라우팅 응용이 핵심이다

## Ⅰ. 개요 (500자 이상)

디멀티플렉서(Demultiplexer, DEMUX)는 **1개 입력 신호를 n비트 선택선에 의해 2^n개 출력 중 하나로 전달**하는 조합 논리 회로이다. 멀티플렉서(MUX)가 2^n개 입력 중 1개를 선택하여 1개 출력으로 내보내는 반면, DEMUX는 1개 입력을 받아 2^n개 출력 중 하나로 전송한다. 이러한 특성 때문에 "역다중화" 또는 "데이터 분배기"라고도 불린다.

```
DEMUX 기본 개념:
입력: Data (1비트 또는 n비트)
선택: Select Lines (n비트)
출력: 2^n개 (선택된 하나만 입력값, 나머지는 0)

1-to-2 DEMUX:
Sel=0: Output0 = Input, Output1 = 0
Sel=1: Output0 = 0, Output1 = Input
```

**주요 응용 분야:**

1. **데이터 라우팅**: CPU 내부에서 버스 데이터를 특정 레지스터나 장치로 전송
2. **메모리 쓰기 제어**: 주소 디코딩 결과를 바탕으로 데이터를 특정 메모리 셀에 쓰기
3. **통신 시스템**: 시분할 다중화(TDM)에서 각 채널로 데이터 분배
4. **I/O 장치 선택**: 주소에 따라 입출력 장치로 데이터 전송

```
TDM 시스템에서의 DEMUX:
고속 데이터 스트림 → DEMUX → 저속 채널들로 분배

채널 1 | 채널 2 | 채널 3 | 채널 4 | ...
   1      2      3      4    (시간 슬롯)
   ↓
DEMUX로 각 채널로 데이터 분배
```

DEMUX는 기본적으로 디코더와 유사한 회로 구조를 가지나, 디코더가 입력을 출력으로 변환하는 반면 DEMUX는 데이터 입력을 선택된 출력으로 전송한다는 점에서 차이가 있다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 1-to-2 디멀티플렉서

```
1-to-2 DEMUX 회로:

Input ──┬── AND(Y0) ── Y0
        │    │
Sel ────┤    │
        │    └── NOT (Y1용)
        └── AND(Y1) ── Y1
             │

진리표:
| Input | Sel | Y0 | Y1 |
|-------|-----|----|----|
|   0   |  0  | 0  | 0  |
|   0   |  1  | 0  | 0  |
|   1   |  0  | 1  | 0  |
|   1   |  1  | 0  | 1  |

Y0 = Input · Sel'
Y1 = Input · Sel
```

### 1-to-4 디멀티플렉서

```
1-to-4 DEMUX 회로:

Input ──┬── AND(Y0) ── Y0
        │    │
S1 ─────┤    └── NOT 조합
        │
S0 ─────┼── AND(Y1) ── Y1
        │    │
        └── AND(Y2) ── Y2
             │
        ┌───┴── AND(Y3) ── Y3
        │
     S1, S0으로 디코딩

진리표:
| Input | S1 S0 | Y3 Y2 Y1 Y0 | 활성 출력 |
|-------|-------|-------------|----------|
|   0   |  0 0  | 0  0  0  0 | - |
|   0   |  0 1  | 0  0  0  0 | - |
|   1   |  0 0  | 0  0  0  1 | Y0 |
|   1   |  0 1  | 0  0  1  0 | Y1 |
|   1   |  1 0  | 0  1  0  0 | Y2 |
|   1   |  1 1  | 1  0  0  0 | Y3 |

Y0 = Input · S1' · S0'
Y1 = Input · S1' · S0
Y2 = Input · S1 · S0'
Y3 = Input · S1 · S0
```

### Enable 입력이 있는 DEMUX

```
Enable 제어 1-to-4 DEMUX:

Enable ──┬── AND(Y0) ── Y0
         │    │
Input ───┤    │
         │    └── S1', S0' 조합
         │
         └── AND(Y1) ~ AND(Y3)

진리표:
| E | Input | S1 S0 | Y3 Y2 Y1 Y0 |
|---|-------|-------|-------------|
| 0 |   X   |  X X  | 0  0  0  0 | (모두 0)
| 1 |   0   |  0 0  | 0  0  0  0 |
| 1 |   1   |  0 0  | 0  0  0  1 |

E=0이면 모든 출력이 0 (비활성)
E=1이면 선택된 출력만 Input 값
```

### 캐스케이딩 (Cascading)

```
1-to-8 DEMUX (1-to-2 × 2개):

           ┌── 1-to-2 DEMUX ── Y0~Y3
S2 ────────┤
           └── 1-to-2 DEMUX ── Y4~Y7
               ↑
            S1, S0 사용

구조:
High DEMUX (S2 제어):
- S2=0: Low0 DEMUX 활성 → Y0~Y3
- S2=1: Low1 DEMUX 활성 → Y4~Y7

각 Low DEMUX:
- S1, S0으로 4개 출력 중 1개 선택
```

### DEMUX vs 디코더

```
디코더와 DEMUX의 차이:

디코더:
- 입력: n비트 코드
- 출력: 2^n개 (One-Hot)
- 기능: 코드 → 신호 분해

DEMUX:
- 입력: 1개 데이터 + n비트 선택
- 출력: 2^n개 (선택된 하나만 데이터)
- 기능: 데이터 라우팅

구조적 유사성:
- DEMUX = 디코더 + AND 게이트들
- 디코더 출력에 Input을 AND로 결합
```

## Ⅲ. 융합 비교

### DEMUX vs MUX

| 비교 항목 | DEMUX | MUX |
|----------|-------|-----|
| 입력 | 1개 데이터 | 2^n개 데이터 |
| 출력 | 2^n개 | 1개 |
| 선택 | n비트 → 1개 출력 | n비트 → 1개 입력 |
| 기능 | 분배 (Distribute) | 선택 (Select) |
| 역관계 | 역관계 | 역관계 |
| 응용 | 데이터 라우팅 | 버스 선택 |

### DEMUX 구현 방식

| 타입 | 구조 | 지연 | 면적 | 응용 |
|------|------|------|------|------|
| 1-to-2 | 2 AND | 1 게이트 | 최소 | 기본 |
| 1-to-4 | 4 AND + 디코더 | 2-3 게이트 | 작음 | 일반 |
| 1-to-8 | 8 AND + 3-to-8 디코더 | 3-4 게이트 | 중간 | 중형 |
| 1-to-16 | 계층적 | 4-5 게이트 | 큼 | 대형 |

### 데이터 분산 방식 비교

| 방식 | DEMUX | 브로드캐스트 | 크로스바 |
|------|-------|------------|---------|
| 1→1 | Yes | No | No |
| 1→N | Yes | Yes | Yes |
| N→N | No (캐스케이드) | Yes | Yes |
| 하드웨어 | O(N) | O(1) | O(N²) |

## Ⅳ. 실무 적용 및 기술사적 판단

### CPU 내부 버스 라우팅

```
CPU 데이터 버스 DEMUX:

ALU Result → 1-to-8 DEMUX → 레지스터 파일

Select Lines (3비트):
- 000: R0
- 001: R1
- ...
- 111: R7

지연:
- DEMUX: 2 게이트
- 레지스터 쓰기: 1 게이트
- 총: 3 게이트 @ 120ps = 360ps

파이프라인:
- WB 스테이지에 DEMUX 포함
- 결과를 목적 레지스터로 라우팅
```

### 메모리 쓰기 제어

```
메모리 인터페이스 DEMUX:

CPU 데이터 버스 → DEMUX → 메모리 뱅크 0~7

주소 디코딩:
- 상위 3비트 → DEMUX 선택
- 하위 비트 → 뱅크 내 주소

쓰기 사이클:
1. CPU 주소 출력
2. 상위 비트 디코딩
3. DEMUX가 데이터를 해당 뱅크로 전송
4. /WE (Write Enable) 활성

은닉:
- 각 뱅크는 독립적 쓰기 가능
- 병렬 쓰기로 대역폭 향상
```

### 통신 시스템 TDM

```
TDM 수신측 DEMUX:

고속 직렬 데이터 → 시리얼-병렬 변환 → DEMUX → 각 채널

1544 Kbps E1 회로 예시:
- 32 타임슬롯
- 각 슬롯: 64 Kbps
- DEMUX가 32 채널로 분배

지연:
- 시리얼-병렬: 1 비트 시간
- DEMUX: 2-3 게이트
- 총 지연: 무시할 수 있음 (클럭 동기)

구현:
- 5-to-32 DEMUX (복잡)
- 계층적 구조
```

## Ⅴ. 기대효과 및 결론

DEMUX는 데이터 분배의 핵심이다. 라우팅, 메모리 제어, 통신 분배에 필수적이다.

## 📌 관련 개념 맵

```
디멀티플렉서
├── 정의: 1입력 → 2^n출력 중 선택
├── 종류
│   ├── 1-to-2 DEMUX
│   ├── 1-to-4 DEMUX
│   ├── 1-to-8 DEMUX
│   └── 1-to-16 DEMUX
├── 응용
│   ├── 데이터 라우팅
│   ├── 메모리 쓰기 제어
│   ├── TDM 채널 분배
│   └── I/O 장치 선택
└── 관련
    ├── MUX (역기능)
    ├── 디코더 (유사 회로)
    └── 버스 시스템
```

## 👶 어린이를 위한 3줄 비유 설명

1. 디멀티플렉서는 철도 분기기 같아요. 한 개의 열차가 들어와도 스위치에 따라 다른 선로로 보내는 거예요
2. 선택선이 00이면 0번 선로로, 01이면 1번 선로로, 10이면 2번 선로로 열차를 보내요
3. 컴퓨터가 CPU에서 계산한 결과를 선택된 레지스터나 메모리 칩으로 보낼 때 디멀티플렉서가 사용돼요

```python
# 디멀티플렉서 시뮬레이션

from typing import List


class Demultiplexer:
    """디멀티플렉서 시뮬레이션"""

    def __init__(self, num_outputs: int):
        """
        1-to-N DEMUX 생성

        Args:
            num_outputs: 출력 수 (2의 거듭제곱)
        """
        if num_outputs not in [2, 4, 8, 16]:
            raise ValueError("출력 수는 2, 4, 8, 16이어야 합니다")

        self.num_outputs = num_outputs
        self.select_bits = num_outputs.bit_length() - 1
        self.name = f"1-to-{num_outputs} Demultiplexer"

    def demux(self, data: int, select: int, enable: int = 1) -> List[int]:
        """
        데이터 분배

        Args:
            data: 입력 데이터 (0 또는 1)
            select: 선택선 값
            enable: 활성화 신호

        Returns:
            출력 리스트 (길이 = num_outputs)
        """
        if not 0 <= select < self.num_outputs:
            raise ValueError(f"선택선은 0 ~ {self.num_outputs - 1} 범위여야 합니다")

        outputs = [0] * self.num_outputs

        if enable:
            outputs[select] = data

        return outputs

    def truth_table(self) -> None:
        """진리표 출력"""
        print(f"\n{'='*60}")
        print(f"{self.name} 진리표")
        print(f"{'='*60}")
        print(f"{'Input':<6} {'Select':<6} {'Enable':<6} {'Outputs':<20}")
        print("-" * 60)

        for enable in [0, 1]:
            for data in [0, 1]:
                for select in range(self.num_outputs):
                    outputs = self.demux(data, select, enable)
                    output_str = ''.join(map(str, outputs))
                    print(f"{data:<6} {select:<6} {enable:<6} {output_str:<20}")

        print("="*60)


class DataRouter:
    """데이터 라우터 시뮬레이션"""

    def __init__(self, num_channels: int):
        self.demux = Demultiplexer(num_channels)

    def route_data(self, data_stream: List[tuple]) -> dict:
        """
        데이터 스트림 라우팅

        Args:
            data_stream: [(data, select), ...] 튜플 리스트

        Returns:
            채널별 데이터 수신 딕셔너리
        """
        channels = {i: [] for i in range(self.demux.num_outputs)}

        for data, select in data_stream:
            outputs = self.demux.demux(data, select)
            for i, val in enumerate(outputs):
                if val:
                    channels[i].append(val)

        return channels


def demonstration():
    """DEMUX 데모"""
    print("="*60)
    print("디멀티플렉서 (Demultiplexer) 데모")
    print("="*60)

    # 1-to-4 DEMUX
    demux4 = Demultiplexer(4)
    demux4.truth_table()

    # 데이터 라우팅
    print("\n[데이터 라우팅]")
    router = DataRouter(4)

    # 채널 0, 1, 2, 3로 데이터 전송
    data_stream = [
        (1, 0),  # 데이터 1 → 채널 0
        (1, 1),  # 데이터 1 → 채널 1
        (0, 2),  # 데이터 0 → 채널 2
        (1, 3),  # 데이터 1 → 채널 3
        (1, 0),  # 데이터 1 → 채널 0
        (1, 2),  # 데이터 1 → 채널 2
    ]

    channels = router.route_data(data_stream)

    print(f"\n입력 데이터 스트림:")
    for data, select in data_stream:
        print(f"  Data {data} → Channel {select}")

    print(f"\n채널별 수신 데이터:")
    for ch, data_list in channels.items():
        print(f"  Channel {ch}: {data_list}")

    # CPU 버스 라우팅 시뮬레이션
    print(f"\n[CPU 레지스터 라우팅]")
    print("ALU 결과 = 0xFF")
    print("목적 레지스터: R3 (select = 3)")

    alu_result = 0xFF
    dest_reg = 3
    outputs = demux4.demux(1, dest_reg)  # 1 = 쓰기 활성

    print(f"쓰기 신호: {outputs}")
    print(f"R{dest_reg} ← 0xFF (쓰기 활성)")


if __name__ == "__main__":
    demonstration()
```
