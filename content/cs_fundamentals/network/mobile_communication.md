+++
title = "이동통신 (Mobile Communication)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 이동통신 (Mobile Communication)

## 핵심 인사이트 (3줄 요약)
> **이동 중에도 통신이 가능**한 무선 통신 시스템. 셀룰러 구조로 주파수 재사용을 통해 대용량 서비스 제공. 1G~5G로 진화하며 속도와 서비스가 확장되었다.

## 1. 개념
이동통신은 **이동하는 사용자에게 무선으로 음성/데이터 서비스를 제공**하는 시스템으로, 셀(Cell)이라는 작은 서비스 영역으로 구성된다.

> 비유: "벌집 구조" - 각 방(셀)에서 같은 주파수를 재사용

## 2. 셀룰러 구조

```
개념: 서비스 영역을 작은 셀로 분할

     △     △     △
    ╱ ╲   ╱ ╲   ╱ ╲
   ◇───◇───◇───◇
    ╲ ╱   ╲ ╱   ╲ ╱
     ▽     ▽     ▽
    ╱ ╲   ╱ ╲   ╱ ╲
   ◇───◇───◇───◇
    ╲ ╱   ╲ ╱   ╲ ╱
     ▽     ▽     ▽

각 셀: 기지국(BS) 하나가 커버
인접 셀: 다른 주파수 사용
멀리 떨어진 셀: 주파수 재사용 가능
```

### 2.1 셀 종류

| 셀 타입 | 반경 | 용도 |
|---------|------|------|
| Macro Cell | 1~10km | 일반적 |
| Micro Cell | 100m~1km | 도심 |
| Pico Cell | 10~100m | 실내 |
| Femto Cell | ~10m | 가정 |

### 2.2 주파수 재사용
```
클러스터: N개의 셀이 모든 주파수를 사용

재사용 거리:
D = R × √(3N)

R: 셀 반경
N: 클러스터 크기 (4, 7, 12, ...)

예: N=7
D = R × √21 ≈ 4.58R
```

## 3. 이동통신 시스템 구성

```
┌─────────────────────────────────────────┐
│            핵심망 (Core Network)        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │   HLR   │  │   VLR   │  │   MSC   │ │
│  └─────────┘  └─────────┘  └─────────┘ │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───┴───┐  ┌───┴───┐  ┌───┴───┐
│  BS1  │  │  BS2  │  │  BS3  │
└───┬───┘  └───┬───┘  └───┬───┘
    │          │          │
  셀1        셀2        셀3

구성 요소:
- MS: 이동국 (단말기)
- BS: 기지국 (Base Station)
- MSC: 이동교환국 (Mobile Switching Center)
- HLR: 가입자 위치 등록기 (Home)
- VLR: 방문자 위치 등록기 (Visitor)
```

## 4. 핸드오버 (Handover)

```
개념: 이동 중 통화 유지를 위해 셀 간 이동

Hard Handover:
- 기존 연결 끊고 새 연결
- "끊고 연결"

Soft Handover:
- 기존 연결 유지하며 새 연결
- "연결하고 끊기"

판단 기준:
1. 수신 신호 강도 (RSS)
2. 신호 대 잡음비 (SNR)
3. 셀 용량
4. 단말 속도
```

### 4.1 핸드오버 과정
```
1. 측정 (Measurement)
   MS가 이웃 셀 신호 측정

2. 보고 (Report)
   BS로 측정 결과 전송

3. 결정 (Decision)
   네트워크가 핸드오버 결정

4. 실행 (Execution)
   새 셀로 연결 이동
```

## 5. 이동통신 세대별 진화

### 5.1 1G (1세대)
```
시기: 1980년대
방식: 아날로그
다중접속: FDMA
서비스: 음성만
예: AMPS, TACS

특징:
- 음성 품질 낮음
- 보안 취약
- 용량 적음
```

### 5.2 2G (2세대)
```
시기: 1990년대
방식: 디지털
다중접속: TDMA, CDMA
서비스: 음성, SMS
예: GSM, IS-95(CDMA)

특징:
- 디지털 음성
- 암호화 지원
- 문자 서비스
```

### 5.3 3G (3세대)
```
시기: 2000년대
방식: 디지털 광대역
다중접속: CDMA, WCDMA
서비스: 음성, 데이터, 영상
예: WCDMA, CDMA2000

특징:
- 광대역 데이터
- 영상 통화
- 모바일 인터넷
속도: 384kbps~2Mbps
```

### 5.4 4G (4세대)
```
시기: 2010년대
방식: 전 패킷
다중접속: OFDMA
서비스: 고속 데이터
예: LTE, LTE-A

특징:
- All-IP 네트워크
- VoLTE (음성도 패킷)
- 광대역 서비스
속도: 100Mbps~1Gbps
```

### 5.5 5G (5세대)
```
시기: 2020년대~
방식: NR (New Radio)
다중접속: OFDMA, NOMA
서비스: eMBB, URLLC, mMTC

특징:
- 초고속 (10Gbps+)
- 초저지연 (1ms)
- 대규모 연결
- 네트워크 슬라이싱

용도:
- eMBB: 8K 스트리밍
- URLLC: 자율주행
- mMTC: IoT 대규모 연결
```

## 6. 세대별 비교

| 항목 | 1G | 2G | 3G | 4G | 5G |
|------|-----|-----|-----|-----|-----|
| 방식 | 아날로그 | 디지털 | 광대역 | All-IP | NR |
| 속도 | - | 9.6k | 2M | 1G | 10G+ |
| 지연 | - | - | 100ms | 10ms | 1ms |
| 서비스 | 음성 | +SMS | +데이터 | +영상 | +IoT |

## 7. 전력 제어

```
목적:
1. 배터리 절약
2. 간섭 최소화
3. 용량 증대

방식:
- 개방루프: 단말이 자체 측정으로 제어
- 폐루프: 기지국이 명령으로 제어

종류:
- 순방향: BS → MS 전력 제어
- 역방향: MS → BS 전력 제어
```

## 8. 코드 예시

```python
import numpy as np
import random

class Cell:
    """셀 시뮬레이션"""

    def __init__(self, cell_id, center, radius, frequency):
        self.cell_id = cell_id
        self.center = center  # (x, y)
        self.radius = radius
        self.frequency = frequency
        self.users = []

    def is_in_cell(self, position):
        """위치가 셀 내부인지 확인"""
        dist = np.sqrt((position[0] - self.center[0])**2 +
                       (position[1] - self.center[1])**2)
        return dist <= self.radius

    def calculate_signal_strength(self, position, tx_power=40):
        """신호 강도 계산"""
        dist = np.sqrt((position[0] - self.center[0])**2 +
                       (position[1] - self.center[1])**2)
        dist = max(dist, 0.001)  # 0으로 나누기 방지

        # 자유 공간 경로 손실 (간소화)
        path_loss = 20 * np.log10(dist) + 20 * np.log10(self.frequency) + 32.4
        rx_power = tx_power - path_loss
        return rx_power


class MobileStation:
    """이동국 시뮬레이션"""

    def __init__(self, ms_id, position):
        self.ms_id = ms_id
        self.position = position
        self.serving_cell = None
        self.history = []

    def move(self, dx, dy):
        """이동"""
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def measure_signals(self, cells):
        """주변 셀 신호 측정"""
        measurements = {}
        for cell in cells:
            signal = cell.calculate_signal_strength(self.position)
            measurements[cell.cell_id] = signal
        return measurements


class HandoverManager:
    """핸드오버 관리"""

    def __init__(self, hysteresis=3, ttt=0.5):
        self.hysteresis = hysteresis  # 히스테리시스 (dB)
        self.ttt = ttt  # Time to Trigger (초)

    def should_handover(self, measurements, serving_cell_id):
        """핸드오버 필요 여부 판단"""
        if serving_cell_id is None:
            return max(measurements, key=measurements.get)

        serving_signal = measurements[serving_cell_id]
        best_neighbor = max(measurements, key=measurements.get)
        neighbor_signal = measurements[best_neighbor]

        # 조건: 이웃 셀이 현재 셀보다 hysteresis만큼 강함
        if neighbor_signal > serving_signal + self.hysteresis:
            return best_neighbor

        return None


# 시뮬레이션
print("=== 셀룰러 네트워크 시뮬레이션 ===")

# 셀 생성 (7셀 클러스터)
cells = [
    Cell(1, (0, 0), 1000, 2100),      # 중앙
    Cell(2, (1732, 1000), 1000, 1900),  # 우상
    Cell(3, (1732, -1000), 1000, 2000), # 우하
    Cell(4, (0, 2000), 1000, 1800),    # 상
    Cell(5, (0, -2000), 1000, 2200),   # 하
    Cell(6, (-1732, 1000), 1000, 2300), # 좌상
    Cell(7, (-1732, -1000), 1000, 2400),# 좌하
]

# 이동국 생성
ms = MobileStation(1, (0, 0))
handover_mgr = HandoverManager(hysteresis=3)

# 이동 시뮬레이션
print("\n이동 시뮬레이션:")
for step in range(10):
    # 이동 (우측으로 이동)
    ms.move(200, 0)

    # 신호 측정
    measurements = ms.measure_signals(cells)

    # 최적 셀 찾기
    best_cell = max(measurements, key=measurements.get)
    best_signal = measurements[best_cell]

    # 핸드오버 판단
    new_cell = handover_mgr.should_handover(measurements, ms.serving_cell)

    if new_cell and new_cell != ms.serving_cell:
        print(f"Step {step+1}: 위치 {ms.position}")
        print(f"  핸드오버! Cell {ms.serving_cell} → Cell {new_cell}")
        print(f"  신호: {measurements[new_cell]:.1f} dBm")
        ms.serving_cell = new_cell
    else:
        print(f"Step {step+1}: 위치 {ms.position}, 서빙 셀: {ms.serving_cell or best_cell}")
