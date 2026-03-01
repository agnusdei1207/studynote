+++
title = "변조와 복조 (Modulation and Demodulation)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 변조와 복조 (Modulation and Demodulation)

## 핵심 인사이트 (3줄 요약)
> **변조**: 신호를 전송하기 적합한 형태로 변환. **복조**: 변조된 신호를 원래 신호로 복원. 반송파(Carrier)의 진폭, 주파수, 위상을 변화시켜 정보를 실어 보낸다.

## 1. 개념

### 변조 (Modulation)
**원신호(Baseband)를 반송파에 실어 전송 가능한 형태로 변환**하는 과정이다.

### 복조 (Demodulation)
**변조된 신호에서 원신호를 추출**하는 과정이다.

> 비유: "택배 포장" - 물건(신호)을 박스(반송파)에 담아 보내고, 받아서 다시 꺼내는 것

## 2. 변조의 필요성

```
1. 전송 효율
   - 안테나 크기: 파장의 1/4~1/2 필요
   - 저주파: 안테나가 너무 커짐
   - 고주파 변조: 안테나 크기 축소

2. 다중화
   - 여러 신호를 서로 다른 주파수로 전송
   - FDM 가능

3. 전파 특성
   - 주파수별 전파 특성 활용
   - 장거리/단거리 전송 선택

4. 잡음 내성
   - 변조 방식에 따른 잡음 저항성
```

## 3. 아날로그 변조

### 3.1 진폭 변조 (AM)
```
반송파의 진폭에 신호를 싣는 방식

원신호:     ∿∿∿∿
반송파:     ∿∿∿∿∿∿∿∿
AM 신호:   ▃▅▇▅▃▅▇▅▃  (진폭 변화)

특징:
- 구현 간단
- 잡음에 취약
- 대역폭: 2 × 신호 대역폭
- 예: AM 라디오 (535~1605 kHz)
```

### 3.2 주파수 변조 (FM)
```
반송파의 주파수에 신호를 싣는 방식

원신호:     ▂▔▂▔
FM 신호:   ∿∿∿≈≈≈∿∿  (주파수 변화)

특징:
- 잡음에 강함
- 대역폭 넓음
- 충실도 높음
- 예: FM 라디오 (88~108 MHz)
```

### 3.3 위상 변조 (PM)
```
반송파의 위상에 신호를 싣는 방식

특징:
- FM과 유사
- 디지털 변조의 기초
```

### 3.4 아날로그 변조 비교

| 항목 | AM | FM | PM |
|------|-----|-----|-----|
| 변화 대상 | 진폭 | 주파수 | 위상 |
| 잡음 내성 | 낮음 | 높음 | 높음 |
| 대역폭 | 좁음 | 넓음 | 넓음 |
| 복잡도 | 낮음 | 중간 | 높음 |
| 품질 | 낮음 | 높음 | 높음 |

## 4. 디지털 변조

### 4.1 ASK (Amplitude Shift Keying)
```
진폭으로 0/1 표현

1: ▔▔▔▔
0: ▂▂▂▂

예: 적외선 리모컨
```

### 4.2 FSK (Frequency Shift Keying)
```
주파수로 0/1 표현

1: ≈≈≈≈ (고주파)
0: ∿∿∿∿ (저주파)

예: 모뎀, DECT 전화기
```

### 4.3 PSK (Phase Shift Keying)
```
위상으로 0/1 표현

BPSK (2진):
1: ↗ (0°)
0: ↙ (180°)

QPSK (4진):
00: 0°
01: 90°
11: 180°
10: 270°

예: 위성통신, WiFi
```

### 4.4 QAM (Quadrature Amplitude Modulation)
```
진폭과 위상을 동시에 사용

16-QAM: 4비트/심볼
64-QAM: 6비트/심볼
256-QAM: 8비트/심볼

     Q
     ↑
  10│11
  ───┼───→ I
  00│01
     ↓

예: WiFi, LTE, 케이블 모뎀
```

### 4.5 디지털 변조 비교

| 변조 | 심볼당 비트 | 대역폭 효율 | 잡음 내성 |
|------|------------|------------|----------|
| BPSK | 1 | 낮음 | 높음 |
| QPSK | 2 | 중간 | 중간 |
| 16-QAM | 4 | 높음 | 낮음 |
| 64-QAM | 6 | 높음 | 낮음 |
| 256-QAM | 8 | 높음 | 매우 낮음 |

## 5. OFDM (직교 주파수 분할 다중화)

```
개념: 다수의 직교 부반송파에 데이터 분산 전송

┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│f1   │ │f2   │ │f3   │ │f4   │
└──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘
   └───────┴───────┴───────┘
              ↓
         하나의 채널

특징:
- 다중 경로 간섭에 강함
- 스펙트럼 효율 높음
- 4G/5G, WiFi, DVB에 사용

장점:
- 주파수 선택적 페이딩에 강함
- 심볼 간 간섭(ISI) 감소

단점:
- PAPR(첨두-평균 전력비) 높음
- 주파수 오프셋에 민감
```

## 6. 펄스 변조

### 6.1 PAM (Pulse Amplitude Modulation)
```
펄스의 진폭으로 신호 표현

원신호:   ∿∿∿∿
PAM:     ▂▅▇▅▃▅▇▅
```

### 6.2 PCM (Pulse Code Modulation)
```
아날로그 신호를 디지털로 변환

과정:
1. 표본화 (Sampling)
2. 양자화 (Quantization)
3. 부호화 (Encoding)

예: 전화 음성 (8kHz, 8bit = 64kbps)
```

### 6.3 PWM (Pulse Width Modulation)
```
펄스 폭으로 신호 표현

원신호:   ▂▅▇▅▃
PWM:     ┌──┐ ┌────┐ ┌──────┐
         │  │ │    │ │      │
      ───┘  └─┘    └─┘      └───

예: 모터 제어, LED 밝기 조절
```

## 7. 변조 효율 지표

| 지표 | 의미 | 공식 |
|------|------|------|
| 스펙트럼 효율 | bps/Hz | 전송률/대역폭 |
| 에너지 효율 | Eb/N0 | 비트 에너지/잡음 |
| BER | 비트 오류율 | 오류 비트/전체 비트 |
| SER | 심볼 오류율 | 오류 심볼/전체 심볼 |

## 8. 코드 예시

```python
import numpy as np
import matplotlib.pyplot as plt

class AnalogModulation:
    """아날로그 변조 시뮬레이션"""

    def __init__(self, fc=10, fs=1000, duration=1):
        self.fc = fc  # 반송파 주파수
        self.fs = fs  # 샘플링 주파수
        self.t = np.linspace(0, duration, fs * duration)

    def am_modulate(self, message, modulation_index=0.5):
        """AM 변조"""
        carrier = np.cos(2 * np.pi * self.fc * self.t)
        modulated = (1 + modulation_index * message) * carrier
        return modulated

    def fm_modulate(self, message, freq_deviation=5):
        """FM 변조"""
        # 위상 적분 = 순시 주파수
        phase = 2 * np.pi * self.fc * self.t + \
                2 * np.pi * freq_deviation * np.cumsum(message) / self.fs
        modulated = np.cos(phase)
        return modulated

class DigitalModulation:
    """디지털 변조 시뮬레이션"""

    def __init__(self, samples_per_symbol=100):
        self.sps = samples_per_symbol

    def bpsk_modulate(self, bits):
        """BPSK 변조"""
        symbols = 2 * np.array(bits) - 1  # 0→-1, 1→+1
        # 심볼 반복
        modulated = np.repeat(symbols, self.sps)
        return modulated

    def qpsk_modulate(self, bits):
        """QPSK 변조 (2비트씩)"""
        mapping = {
            (0, 0): (1, 1),
            (0, 1): (-1, 1),
            (1, 1): (-1, -1),
            (1, 0): (1, -1)
        }

        i_samples = []
        q_samples = []

        for i in range(0, len(bits), 2):
            i_val, q_val = mapping[(bits[i], bits[i+1])]
            i_samples.extend([i_val] * self.sps)
            q_samples.extend([q_val] * self.sps)

        return np.array(i_samples), np.array(q_samples)

    def constellation_plot(self, i, q):
        """성상도 그리기"""
        # 다운샘플링
        i_down = i[::self.sps]
        q_down = q[::self.sps]
        return i_down, q_down

# BPSK 테스트
dm = DigitalModulation(samples_per_symbol=50)
bits = [0, 1, 0, 0, 1, 1, 1, 0]
bpsk_signal = dm.bpsk_modulate(bits)
print(f"BPSK 변조: {len(bpsk_signal)} 샘플")
print(f"첫 10 샘플: {bpsk_signal[:10]}")

# QPSK 테스트
i, q = dm.qpsk_modulate(bits)
print(f"\nQPSK I채널: {i[:20]}")
print(f"QPSK Q채널: {q[:20]}")
```

## 9. 장단점

### 변조의 장점
| 장점 | 설명 |
|-----|------|
| 전송 거리 | 증가 |
| 안테나 크기 | 축소 |
| 다중화 | 가능 |
| 잡음 내성 | 향상 |

### 변조의 단점
| 단점 | 설명 |
|-----|------|
| 복잡도 | 증가 |
| 전력 소모 | 증가 |
| 대역폭 | 확장 필요 |
| 지연 | 발생 |

## 10. 실무에선? (기술사적 판단)
- **무선 통신**: 환경에 따른 적응형 변조 (AMC)
- **WiFi**: 환경에 따라 BPSK→256-QAM 선택
- **LTE/5G**: OFDM + QAM 조합
- **위성**: 강력한 오류 정정과 함께 QPSK

## 11. 관련 개념
- 반송파 (Carrier)
- 주파수 스펙트럼
- 대역폭
- 다중화

---

## 어린이를 위한 종합 설명

**변조는 "라디오 방송"과 같아요!**

### AM (진폭 변조) 📻
```
DJ 목소리가 크면 → 신호도 커져요
DJ 목소리가 작으면 → 신호도 작아져요

"진폭" = 소리의 크기
```

### FM (주파수 변조) 🎵
```
DJ 목소리가 높으면 → 주파수 올라가요
DJ 목소리가 낮으면 → 주파수 내려가요

"주파수" = 소리의 높낮이
```

### 디지털 변조 💾
```
0과 1을 전파로 보내요!

ASK: 1=크게, 0=작게
FSK: 1=높은음, 0=낮은음
PSK: 1=앞으로, 0=뒤로

QAM: 크기랑 방향 둘 다 써요!
```

**비밀**: 변조 덕분에 스마트폰으로 영상을 볼 수 있어요! 📱✨
