+++
title = "안테나 (Antenna)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 안테나 (Antenna)

## 핵심 인사이트 (3줄 요약)
> **전기 신호를 전자기파로 변환하여 공간으로 방사**하는 장치. 이득, 지향성, 주파수 특성이 핵심 파라미터. 무선 통신의 필수 구성 요소이다.

## 1. 개념
안테나는 **전기 신호를 전자기파로 변환하여 방사(송신)하거나, 전자기파를 전기 신호로 변환(수신)하는 장치**이다.

> 비유: "라디오 방송탑" - 전기 신호를 전파로 바꿔 멀리 보냄

## 2. 안테나 원리

### 2.1 전자기파 방사
```
교류 전류가 흐르면 전자기파 방사

    전기장 (E)
        ↑
        │  /  /
        │ /  /  전자기파
        │/  /   전파 방향 →
    ────●───────→
       /│ /
      / │/
     ↓  전류 (I)
    자기장 (H)

공진 조건:
안테나 길이 ≈ λ/2 (반파장 다이폴)
```

### 2.2 프리스 전송 공식
```
수신 전력:

Pr = (Pt × Gt × Gr × λ²) / (4π × d)²

Pt: 송신 전력
Gt: 송신 안테나 이득
Gr: 수신 안테나 이득
λ: 파장
d: 거리

경로 손실 (dB):
L = 20log₁₀(d) + 20log₁₀(f) + 32.44

특징:
- 거리 2배 → 6dB 손실
- 주파수 2배 → 6dB 손실
```

## 3. 안테나 특성

### 3.1 이득 (Gain)
```
정의: 등방성 안테나 대비 전력 집중도

단위:
- dBi: 등방성 안테나 기준
- dBd: 반파장 다이폴 기준
- dBi = dBd + 2.15

예:
- 다이폴: 2.15 dBi
- 패치 안테나: 6~9 dBi
- 파라볼라: 20~40 dBi
```

### 3.2 방사 패턴 (Radiation Pattern)
```
지향성 안테나:

         주엽 (Main Lobe)
              ↑
             /│\
            / │ \
           /  │  \
  부엽 ←─/───┼───\─→ 부엽
(Side Lobe)  │  (Side Lobe)
           \  │  /
            \ │ /
             \│/
              ↓
         후엽 (Back Lobe)

주요 지표:
- 반전력 빔폭 (HPBW): -3dB 지점 각도
- 전후비 (F/B): 주엽/후엽 비
- 부엽 레벨: 주엽 대비 부엽 크기
```

### 3.3 대역폭 (Bandwidth)
```
정상 동작하는 주파수 범위

표현:
- 절대 대역폭: Hz
- 상대 대역폭: (fH - fL) / fc × 100%

예:
- 협대역: < 10%
- 광대역: > 100%
```

### 3.4 임피던스 (Impedance)
```
일반적으로 50Ω (무선) 또는 75Ω (방송)

정재파비 (VSWR):
VSWR = (1 + |Γ|) / (1 - |Γ|)

Γ: 반사 계수

반사 손실 (Return Loss):
RL = -20log₁₀(|Γ|) dB

기준:
- VSWR < 1.5: 양호
- VSWR < 2.0: 허용
- VSWR > 3.0: 불량
```

## 4. 안테나 종류

### 4.1 다이폴 안테나 (Dipole)
```
구조:
     ╱╲
    ╱  ╲
   ╱    ╲
──┘    └──
  λ/2  λ/2

특징:
- 기본형 안테나
- 이득: 2.15 dBi
- 무지향성 (수평면)

용도: 라디오, TV
```

### 4.2 모노폴 안테나 (Monopole)
```
구조:
     │
     │  λ/4
     │
─────┴──────
   접지면

특징:
- 다이폴의 절반
- 접지면 필요
- 이득: 5.15 dBi

용도: 휴대폰, 차량
```

### 4.3 파라볼라 안테나 (Parabolic)
```
구조:
    ┌─────────────┐
    │  ╭───────╮  │
    │ (  반사면  ) │
    │  ╰───────╯  │
    └──────┬──────┘
           │
         급전기

특징:
- 높은 이득
- 높은 지향성
- 이득 ∝ 직경² × 주파수²

용도: 위성통신, 레이더
```

### 4.4 패치 안테나 (Patch/Microstrip)
```
구조:
┌─────────────────┐ ← 유전체 기판
│  ┌───────────┐  │
│  │   패치    │  │ ← 방사체
│  └───────────┘  │
│                 │
└────────┬────────┘
       급전점

특징:
- 소형, 경량
- 제작 용이
- 이득: 6~9 dBi

용도: WiFi, 휴대폰
```

### 4.5 어레이 안테나 (Array)
```
구조:
┌───┬───┬───┬───┐
│   │   │   │   │
│ ● │ ● │ ● │ ● │  ← 복수 안테나 소자
│   │   │   │   │
└───┴───┴───┴───┘
  ↑   ↑   ↑   ↑
  위상/진폭 제어 → 빔포밍

특징:
- 빔 조향 가능
- 높은 이득
- MIMO 기반

용도: 5G 기지국, 레이더
```

### 4.6 안테나 비교표

| 종류 | 이득 | 빔폭 | 대역폭 | 용도 |
|------|------|------|--------|------|
| 다이폴 | 2 dBi | 78° | 넓음 | 라디오 |
| 모노폴 | 5 dBi | 78° | 넓음 | 휴대폰 |
| 패치 | 6-9 dBi | 60° | 중간 | WiFi |
| 파라볼라 | 20-40 dBi | <5° | 좁음 | 위성 |
| 어레이 | 가변 | 가변 | 넓음 | 5G |

## 5. 안테나 응용

### 5.1 빔포밍 (Beamforming)
```
위상 배열로 빔 방향 제어

┌──────────────────────┐
│   ●  ●  ●  ●  ●     │
│   ↑  ↑  ↑  ↑  ↑     │
│   위상 차이로        │
│   빔 방향 제어       │
└──────────┬───────────┘
           ↓
      ╲   ╲   ╲
       ╲   ╲   ╲
        ╲   ╲   ╲
         빔

이득:
- 신호 집중
- 간섭 억제
- 셀 용량 증대
```

### 5.2 MIMO (Multiple Input Multiple Output)
```
다중 안테나 시스템

송신측                     수신측
┌───┐                     ┌───┐
│TX1│─────────────────────│RX1│
├───┤                     ├───┤
│TX2│─────────────────────│RX2│
├───┤                     ├───┤
│TX3│─────────────────────│RX3│
├───┤                     ├───┤
│TX4│─────────────────────│RX4│
└───┘                     └───┘

이점:
- 다이버시티
- 공간 멀티플렉싱
- 빔포밍
```

## 6. 코드 예시

```python
import numpy as np

class Antenna:
    """안테나 시뮬레이션"""

    def __init__(self, name, gain_dbi, frequency):
        self.name = name
        self.gain_dbi = gain_dbi
        self.gain_linear = 10 ** (gain_dbi / 10)
        self.frequency = frequency  # Hz
        self.wavelength = 3e8 / frequency

    def calculate_path_loss(self, distance):
        """자유 공간 경로 손실"""
        # FSPL = 20*log10(d) + 20*log10(f) - 147.55
        loss_db = 20 * np.log10(distance) + 20 * np.log10(self.frequency) - 147.55
        return loss_db

    def calculate_received_power(self, tx_power_dbm, distance, rx_antenna_gain_dbi=0):
        """수신 전력 계산"""
        path_loss = self.calculate_path_loss(distance)
        rx_power = tx_power_dbm + self.gain_dbi + rx_antenna_gain_dbi - path_loss
        return rx_power


class DipoleAntenna(Antenna):
    """다이폴 안테나"""

    def __init__(self, frequency):
        super().__init__("Dipole", 2.15, frequency)

    def get_radiation_pattern(self, theta):
        """방사 패턴 (수직면)"""
        # E(θ) ∝ cos(π/2 × cos(θ)) / sin(θ)
        pattern = np.abs(np.cos(np.pi/2 * np.cos(theta)) / np.sin(theta + 1e-10))
        return pattern / np.max(pattern)


class ParabolicAntenna(Antenna):
    """파라볼라 안테나"""

    def __init__(self, frequency, diameter, efficiency=0.55):
        self.diameter = diameter
        self.efficiency = efficiency
        wavelength = 3e8 / frequency

        # 이득 계산: G = η × (πD/λ)²
        gain_linear = efficiency * (np.pi * diameter / wavelength) ** 2
        gain_dbi = 10 * np.log10(gain_linear)

        super().__init__("Parabolic", gain_dbi, frequency)

    def get_beamwidth(self):
        """반전력 빔폭 (HPBW)"""
        wavelength = 3e8 / self.frequency
        hpbw = 70 * wavelength / self.diameter  # degrees
        return hpbw


class PhasedArray:
    """위상 배열 안테나 시뮬레이션"""

    def __init__(self, num_elements, element_spacing, frequency):
        self.num_elements = num_elements
        self.spacing = element_spacing  # 파장의 배수
        self.frequency = frequency
        self.wavelength = 3e8 / frequency

    def calculate_array_factor(self, theta, steering_angle=0):
        """배열 인자 계산"""
        k = 2 * np.pi / self.wavelength
        d = self.spacing * self.wavelength

        # 스트라이빙 위상
        beta = k * d * np.sin(np.radians(steering_angle))

        # 배열 인자
        psi = k * d * np.sin(np.radians(theta)) - beta
        AF = np.abs(np.sin(self.num_elements * psi / 2) / (self.num_elements * np.sin(psi / 2 + 1e-10)))

        return AF / np.max(AF)

    def calculate_gain(self, element_gain_dbi=6):
        """배열 이득"""
        # G_array = G_element + 10*log10(N)
        return element_gain_dbi + 10 * np.log10(self.num_elements)


# 시뮬레이션
print("=== 안테나 이득 비교 ===")
freq = 2.4e9  # 2.4 GHz

dipole = DipoleAntenna(freq)
parabolic = ParabolicAntenna(freq, diameter=0.3)

print(f"다이폴 이득: {dipole.gain_dbi:.2f} dBi")
print(f"파라볼라(30cm) 이득: {parabolic.gain_dbi:.2f} dBi")
print(f"파라볼라 빔폭: {parabolic.get_beamwidth():.1f}°")

print("\n=== 경로 손실 및 수신 전력 ===")
tx_power = 20  # dBm
distances = [10, 100, 1000]

for d in distances:
    rx_power = dipole.calculate_received_power(tx_power, d, dipole.gain_dbi)
    loss = dipole.calculate_path_loss(d)
    print(f"거리 {d:4d}m: 경로손실 {loss:.1f}dB, 수신전력 {rx_power:.1f}dBm")

print("\n=== 위상 배열 안테나 ===")
array = PhasedArray(num_elements=8, element_spacing=0.5, frequency=freq)

print(f"소자 수: {array.num_elements}")
print(f"배열 이득: {array.calculate_gain():.1f} dBi")

# 빔포밍 각도별 이득
angles = [-30, 0, 30]
steer = 0
print(f"\n빔포밍 (조향각: {steer}°):")
for angle in angles:
    af = array.calculate_array_factor(angle, steering_angle=steer)
    print(f"  {angle:3d}°: 배열인자 = {af:.3f}")
```

## 7. 장단점

### 고이득 안테나
| 장점 | 단점 |
|-----|------|
| 장거리 통신 | 좁은 커버리지 |
| 간섭 감소 | 정확한 정렬 필요 |
| 낮은 전력 | 크기/무게 |

### 소형 안테나
| 장점 | 단점 |
|-----|------|
| 소형/경량 | 낮은 이득 |
| 저렴 | 좁은 대역폭 |
| 통합 용이 | 성능 제한 |

## 8. 실무에선? (기술사적 판단)
- **기지국**: 고이득 어레이 안테나
- **단말기**: 소형 패치/모노폴
- **위성**: 파라볼라 (C/Ku/Ka대역)
- **5G**: Massive MIMO (64+ 소자)

## 9. 관련 개념
- 전자기파
- 빔포밍
- MIMO
- 전파 전파

---

## 어린이를 위한 종합 설명

**안테나는 "전파 안테나"의 줄임말이에요!**

### 안테나가 뭘 하는 거예요? 📡
```
전기 신호 → [안테나] → 전파 (공기 중으로)
전파 → [안테나] → 전기 신호

마치 마이크와 스피커 같아요!
```

### 안테나 모양 📻
```
다이폴: ─────  (막대 모양)
모노폴:   │    (한쪽만)
파라볼라: ◢◣  (새총 모양)
패치:    □   (네모난 판)
```

### 이득이 높으면? 🔊
```
전파가 한쪽으로 집중돼요!

낮은 이득:
   ╱ ╲ ╱ ╲
  ╱   ╲   ╲
 모든 방향으로

높은 이득:
      ↓
      ↓
      ↓
 한쪽으로만
```

**비밀**: 스마트폰 안에도 안테나가 숨어 있어요! 📱✨
