+++
title = "무선 통신 (Wireless Communication)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 무선 통신 (Wireless Communication)

## 핵심 인사이트 (3줄 요약)
> **전파(무선 매체)를 통해 정보를 전송**하는 통신 방식. 안테나, 변조, 다중화 기술이 핵심이다. 이동통신, WiFi, 블루투스 등 다양한 서비스에 활용된다.

## 1. 개념
무선 통신은 **유선 케이블 없이 전파를 이용해 정보를 전송**하는 기술로, 안테나를 통해 전기 신호를 전파로 변환하여 공간으로 방사한다.

> 비유: "무전기" - 케이블 없이 목소리를 전파에 실어 보냄

## 2. 무선 통신 시스템

```
┌─────────┐                      ┌─────────┐
│ 송신기   │                      │ 수신기   │
│ ┌─────┐ │    전파 (EM Wave)    │ ┌─────┐ │
│ │변조 │ │  ←─────────────────→  │ │복조 │ │
│ │기   │ │                      │ │기   │ │
│ └──┬──┘ │                      │ └──┬──┘ │
│    │    │                      │    │    │
│ ┌──┴──┐ │    ┌──────────┐      │ ┌──┴──┐ │
│ │안테나│ │───→│   공간   │─────→│ │안테나│ │
│ └─────┘ │    └──────────┘      │ └─────┘ │
└─────────┘                      └─────────┘

핵심 요소:
1. 안테나: 전기↔전파 변환
2. 변조: 정보를 전파에 실음
3. 전파 매체: 공기, 진공
4. 채널: 주파수 대역
```

## 3. 전파 (Radio Wave)

### 3.1 전파의 성질
```
전파 = 전자기파 (Electromagnetic Wave)

구성:
- 전기장 (E)
- 자기장 (H)
- 서로 수직
- 진행 방향에 수직

특성:
- 빛의 속도로 전파 (c ≈ 3×10⁸ m/s)
- 반사, 굴절, 회절, 간섭
- 주파수별 특성 다름
```

### 3.2 전파의 분류

| 대역 | 주파수 | 파장 | 특성 | 용도 |
|------|--------|------|------|------|
| VLF | 3~30kHz | 100~10km | 지표파 | 항해 |
| LF | 30~300kHz | 10~1km | 지표파 | 라디오 |
| MF | 300~3000kHz | 1km~100m | 지표파+전리층 | AM 라디오 |
| HF | 3~30MHz | 100~10m | 전리층 반사 | 단파 |
| VHF | 30~300MHz | 10~1m | 가시선 | FM, TV |
| UHF | 300~3000MHz | 1m~10cm | 가시선 | TV, 이동통신 |
| SHF | 3~30GHz | 10~1cm | 직진성 | 위성, 레이더 |
| EHF | 30~300GHz | 1~0.1cm | 감쇠 큼 | 밀리미터파 |

### 3.3 전파 전파 특성
```
1. 지표파 (Ground Wave)
   - 지표면을 따라 전파
   - 저주파에서 강함

2. 직접파 (Direct Wave)
   - 송수신 안테나 간 직접
   - 가시선 필요

3. 전리층 반사파 (Sky Wave)
   - 전리층에서 반사
   - HF 대역, 장거리

4. 회절파 (Diffracted Wave)
   - 장애물 뒤로 회절
   - 저주파에서 강함
```

## 4. 안테나 (Antenna)

### 4.1 안테나 원리
```
변환:
전기 신호 ──→ [안테나] ──→ 전파 (송신)
전파 ──→ [안테나] ──→ 전기 신호 (수신)

원리:
- 교류 전류가 흐르면 전자기파 방사
- 공진 주파수 = 안테나 길이의 2배수
```

### 4.2 안테나 지향 특성
```
무지향성 (Omnidirectional):
    │
  ──┼──  모든 방향으로 동일
    │

지향성 (Directional):
    ╱
   ╱  특정 방향으로 집중
  │
```

### 4.3 안테나 종류

| 종류 | 구조 | 특징 | 용도 |
|------|------|------|------|
| 다이폴 | ───── | 기본형 | 라디오 |
| 모노폴 | ┴ | 접지 이용 | 휴대폰 |
| 파라볼라 | ◢◣ | 고이득 | 위성 |
| 패치 | □ | 소형 | WiFi |
| 슬롯 | ▭ | 평판 | 기지국 |
| 어레이 | ─┴─ | 빔포밍 | 5G |

### 4.4 안테나 성능 지표
```
1. 이득 (Gain)
   - 기준 안테나 대비 전력 비
   - 단위: dBi (등방성 기준)

2. 지향성 (Directivity)
   - 전력 집중도

3. 방사 패턴 (Radiation Pattern)
   - 방사 세기의 공간 분포

4. 대역폭 (Bandwidth)
   - 정상 동작 주파수 범위

5. 임피던스 (Impedance)
   - 일반적으로 50Ω
```

## 5. 페이딩 (Fading)

### 5.1 페이딩 현상
```
신호 세기가 시간에 따라 변하는 현상

원인:
- 다중 경로 (Multipath)
- 장애물 차단
- 이동에 의한 변화
```

### 5.2 페이딩 종류

```
대규모 페이딩 (Large Scale):
- 경로 손실 (Path Loss)
- 그림자 효과 (Shadowing)

소규모 페이딩 (Small Scale):
- 다중 경로 간섭
- 시간 선택적: 시간에 따라 변화
- 주파수 선택적: 주파수에 따라 변화

형태:
- 평탄 페이딩: 전 대역폭 영향
- 선택적 페이딩: 특정 주파수 영향
```

## 6. 다이버시티 (Diversity)

```
개념: 여러 독립 경로로 신호 수신하여 신뢰성 향상

종류:

1. 공간 다이버시티 (Space Diversity)
   - 여러 안테나 사용
   - 간격: λ/2 이상

2. 주파수 다이버시티 (Frequency Diversity)
   - 여러 주파수 사용

3. 시간 다이버시티 (Time Diversity)
   - 여러 시간에 반복 전송

4. 편파 다이버시티 (Polarization Diversity)
   - 수직/수평 편파 사용

합성 방식:
- 선택 합성: 최고 신호 선택
- 등이득 합성: 위상 정렬 후 합성
- 최대비 합성: SNR 가중 합성
```

## 7. 다중 접속

### 7.1 다중 접속 기술

```
FDMA (주파수 분할):
┌───┬───┬───┬───┐
│f1 │f2 │f3 │f4 │
└───┴───┴───┴───┘

TDMA (시간 분할):
├─1─┼─2─┼─3─┼─1─┤

CDMA (코드 분할):
┌───────────────┐
│ 코드로 구분    │
└───────────────┘

OFDMA (직교 주파수 분할):
┌─┬─┬─┬─┬─┬─┬─┬─┐
│1│2│3│1│2│3│4│5│
└─┴─┴─┴─┴─┴─┴─┴─┘
```

### 7.2 세대별 특징

| 세대 | 다중접속 | 특징 | 서비스 |
|------|----------|------|--------|
| 1G | FDMA | 아날로그 | 음성 |
| 2G | TDMA | 디지털 | 음성+SMS |
| 3G | CDMA | 패킷 | 데이터 |
| 4G | OFDMA | 광대역 | 영상 |
| 5G | OFDMA/NOMA | 초연결 | IoT/자율주행 |

## 8. 코드 예시

```python
import numpy as np
import random

class RadioWave:
    """전파 시뮬레이션"""

    def __init__(self, frequency):
        self.frequency = frequency  # Hz
        self.c = 3e8  # 빛의 속도
        self.wavelength = self.c / frequency

    def calculate_path_loss(self, distance):
        """자유 공간 경로 손실 계산"""
        # FSPL = 20*log10(d) + 20*log10(f) + 20*log10(4π/c)
        loss_db = 20 * np.log10(distance) + \
                  20 * np.log10(self.frequency) + \
                  20 * np.log10(4 * np.pi / self.c)
        return loss_db


class Antenna:
    """안테나 시뮬레이션"""

    def __init__(self, gain_dbi=0, efficiency=1.0):
        self.gain = gain_dbi
        self.efficiency = efficiency

    def calculate_effective_area(self, wavelength):
        """유효 개구면 계산"""
        # A_e = (G * λ²) / (4π)
        gain_linear = 10 ** (self.gain / 10)
        return (gain_linear * wavelength ** 2) / (4 * np.pi)


class WirelessChannel:
    """무선 채널 시뮬레이션"""

    def __init__(self, num_paths=3):
        self.num_paths = num_paths

    def rayleigh_fading(self, num_samples):
        """레일리 페이딩 생성"""
        # 복소 가우시안 → 레일리 분포
        h = (np.random.randn(num_samples) + 1j * np.random.randn(num_samples)) / np.sqrt(2)
        return h

    def multipath_channel(self, signal):
        """다중 경로 채널 시뮬레이션"""
        delays = np.random.rand(self.num_paths) * 10  # 샘플 지연
        gains = np.random.randn(self.num_paths) + 1j * np.random.randn(self.num_paths)

        output = np.zeros(len(signal) + int(max(delays)), dtype=complex)
        for i in range(self.num_paths):
            delay = int(delays[i])
            output[delay:delay+len(signal)] += gains[i] * signal

        return output[:len(signal)]


class DiversityCombiner:
    """다이버시티 합성"""

    @staticmethod
    def selection_combining(signals):
        """선택 합성: 가장 강한 신호 선택"""
        powers = [np.mean(np.abs(s)**2) for s in signals]
        best_idx = np.argmax(powers)
        return signals[best_idx]

    @staticmethod
    def mrc_combining(signals, noise_powers):
        """최대비 합성 (MRC)"""
        weights = []
        for i, signal in enumerate(signals):
            power = np.mean(np.abs(signal)**2)
            weight = signal / noise_powers[i]
            weights.append(weight)

        combined = sum(w * s for w, s in zip(weights, signals))
        return combined


# 시뮬레이션
print("=== 전파 경로 손실 ===")
wave = RadioWave(frequency=2.4e9)  # 2.4 GHz (WiFi)
print(f"주파수: {wave.frequency/1e9} GHz")
print(f"파장: {wave.wavelength*100:.2f} cm")

for dist in [1, 10, 100, 1000]:
    loss = wave.calculate_path_loss(dist)
    print(f"거리 {dist:4d}m: 손실 {loss:.1f} dB")

print("\n=== 레일리 페이딩 ===")
channel = WirelessChannel()
fading = channel.rayleigh_fading(1000)
print(f"평균 이득: {np.mean(np.abs(fading)**2):.4f}")
print(f"표준편차: {np.std(np.abs(fading)**2):.4f}")
