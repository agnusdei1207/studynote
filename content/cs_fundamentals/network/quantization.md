+++
title = "양자화 (Quantization)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 양자화 (Quantization)

## 핵심 인사이트 (3줄 요약)
> **연속적인 아날로그 값을 이산적인 디지털 값으로 변환**하는 과정. 표본화된 신호를 일정 단계로 반올림. 양자화 오차가 발생하며, 단계가 많을수록 정밀도가 높다.

## 1. 개념
양자화(Quantization)는 **연속적인 아날로그 값을 유한한 레벨의 이산적 값으로 근사**하는 과정으로, PCM(Pulse Code Modulation)의 핵심 단계이다.

> 비유: "성적 등급 매기기" - 0~100점을 A, B, C, D, F로 구분

## 2. 양자화 과정

```
아날로그 신호 → [표본화] → [양자화] → [부호화] → 디지털 신호

과정:
1. 표본화 (Sampling)
   - 시간 축 이산화

2. 양자화 (Quantization)
   - 진폭 축 이산화

3. 부호화 (Encoding)
   - 양자화된 값을 이진수로
```

## 3. 양자화 종류

### 3.1 균일 양자화 (Uniform Quantization)
```
모든 단계가 동일한 크기

입력 범위: 0 ~ 8V, 8레벨

진폭
 8V ───┬─── 111
       │
 7V ───┼─── 110
       │
 6V ───┼─── 101
       │
 5V ───┼─── 100
       │
 4V ───┼─── 011
       │
 3V ───┼─── 010
       │
 2V ───┼─── 001
       │
 1V ───┼─── 000
       │
 0V ───┴───

단계 크기 (Δ) = V_max / 2^n
```

### 3.2 비균일 양자화 (Non-uniform Quantization)
```
신호 크기에 따라 다른 단계 크기

작은 신호: 작은 단계 (정밀)
큰 신호: 큰 단계 (거침)

이유:
- 음성 신호는 작은 진폭이 많음
- 작은 신호의 정밀도 향상

압신(Companding):
- 송신: 압축 (Compress)
- 수신: 확장 (Expand)
- μ-law (북미), A-law (유럽)
```

## 4. 양자화 오차 (Quantization Error)

### 4.1 정의
```
양자화된 값과 원래 값의 차이

오차 범위: -Δ/2 ≤ e ≤ +Δ/2

예:
원래 값: 3.7V
양자화 값: 4V
오차: 0.3V

최대 오차: Δ/2
```

### 4.2 양자화 잡음
```
SQNR (Signal-to-Quantization Noise Ratio)

SQNR = 1.76 + 6.02n dB

n: 비트 수

예:
8비트: 1.76 + 48.16 = 49.92 dB
16비트: 1.76 + 96.32 = 98.08 dB

특징:
- 비트가 1개 증가할 때마다 6dB 향상
- 신호 품질은 비트 수에 비례
```

## 5. 선형 vs 비선형 양자화

| 항목 | 선형 (균일) | 비선형 (비균일) |
|------|-----------|----------------|
| 단계 | 동일 | 가변 |
| 구현 | 단순 | 복잡 |
| SQNR | 신호 크기에 따라 변화 | 일정 |
| 용도 | 오디오 CD | 전화망 |

## 6. 압신 법칙 (Companding)

### 6.1 μ-law (미국/일본)
```
y = (ln(1 + μ|x|) / ln(1 + μ)) * sgn(x)

μ = 255 (표준)

특징:
- 북미, 일본 표준
- T1 회선
```

### 6.2 A-law (유럽/한국)
```
        A|x| / (1 + ln(A))         for |x| < 1/A
y = {
        (1 + ln(A|x|)) / (1 + ln(A))  for |x| ≥ 1/A

A = 87.6 (표준)

특징:
- 유럽, 한국 표준
- E1 회선
- μ-law보다 구현 단순
```

## 7. PCM (Pulse Code Modulation)

```
전체 과정:

아날로그 신호
     │
     ▼
┌─────────────┐
│  표본화     │  fs ≥ 2fmax (Nyquist)
│  (Sampling) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  양자화     │  n비트 → 2^n 레벨
│(Quantizing) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  부호화     │  이진 코드
│  (Encoding) │
└──────┬──────┘
       │
       ▼
  디지털 신호

전화 음성:
- 표본화: 8kHz
- 양자화: 8비트
- 전송률: 64kbps
```

## 8. 델타 변조 (Delta Modulation)

```
1비트 양자화:

이전 값과 비교:
- 증가: 1
- 감소: 0

     ▲
     │    ∿∿∿∿∿∿∿
     │   /\/\/\/\/\
     │  /          Δ (계단 크기)
     │ /
     └─────────────→ 시간

장점:
- 단순한 구현
- 낮은 비트율

단점:
- 슬로프 과부하
- 과잉 진동
```

## 9. 코드 예시

```python
import numpy as np
import matplotlib.pyplot as plt

class Quantizer:
    """양자화 시뮬레이션"""

    def __init__(self, bits=8, vmin=0, vmax=255):
        self.bits = bits
        self.levels = 2 ** bits
        self.vmin = vmin
        self.vmax = vmax
        self.step = (vmax - vmin) / self.levels

    def quantize(self, value):
        """균일 양자화"""
        # 클리핑
        value = np.clip(value, self.vmin, self.vmax)

        # 양자화
        level = int((value - self.vmin) / self.step)
        quantized = self.vmin + level * self.step + self.step / 2

        return quantized, level

    def dequantize(self, level):
        """역양자화"""
        return self.vmin + level * self.step + self.step / 2

    def calculate_error(self, original, quantized):
        """양자화 오차 계산"""
        return abs(original - quantized)


class MuLawCompander:
    """μ-law 압신 시뮬레이션"""

    def __init__(self, mu=255):
        self.mu = mu

    def compress(self, x):
        """압축"""
        return np.sign(x) * np.log(1 + self.mu * np.abs(x)) / np.log(1 + self.mu)

    def expand(self, y):
        """확장"""
        return np.sign(y) * (np.power(1 + self.mu, np.abs(y)) - 1) / self.mu


class PCM:
    """PCM 시뮬레이션"""

    def __init__(self, sample_rate=8000, bits=8):
        self.sample_rate = sample_rate
        self.bits = bits
        self.quantizer = Quantizer(bits, -1, 1)

    def encode(self, analog_signal, duration):
        """PCM 부호화"""
        # 표본화
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples)
        samples = analog_signal(t)

        # 양자화 및 부호화
        encoded = []
        for sample in samples:
            _, level = self.quantizer.quantize(sample)
            encoded.append(level)

        return encoded, samples

    def decode(self, encoded):
        """PCM 복호화"""
        return [self.quantizer.dequantize(level) for level in encoded]


# 시뮬레이션
print("=== 균일 양자화 ===")
q8 = Quantizer(bits=8, vmin=0, vmax=255)
q4 = Quantizer(bits=4, vmin=0, vmax=255)

values = [10.3, 50.7, 128.9, 200.1, 250.5]

print("8비트 양자화:")
for v in values:
    qv, level = q8.quantize(v)
    error = q8.calculate_error(v, qv)
    print(f"  {v:.1f} → {qv:.2f} (레벨 {level}), 오차: {error:.2f}")

print("\n4비트 양자화:")
for v in values:
    qv, level = q4.quantize(v)
    error = q4.calculate_error(v, qv)
    print(f"  {v:.1f} → {qv:.2f} (레벨 {level}), 오차: {error:.2f}")

print("\n=== μ-law 압신 ===")
compander = MuLawCompander(mu=255)

test_values = [0.1, 0.3, 0.5, 0.7, 0.9]
for x in test_values:
    compressed = compander.compress(x)
    expanded = compander.expand(compressed)
    print(f"  {x:.1f} → 압축: {compressed:.3f} → 확장: {expanded:.3f}")

print("\n=== PCM ===")
pcm = PCM(sample_rate=8000, bits=8)
signal = lambda t: np.sin(2 * np.pi * 440 * t)  # 440Hz 사인파

encoded, samples = pcm.encode(signal, 0.01)  # 10ms
decoded = pcm.decode(encoded)

print(f"샘플 수: {len(encoded)}")
print(f"처음 5 샘플: {encoded[:5]}")
print(f"SQNR 이론값: {1.76 + 6.02 * 8:.2f} dB")
```

## 10. 장단점

### 균일 양자화
| 장점 | 단점 |
|-----|------|
| 구현 단순 | 동적 범위 제한 |
| 빠름 | 작은 신호 품질 낮음 |

### 비균일 양자화
| 장점 | 단점 |
|-----|------|
| 넓은 동적 범위 | 구현 복잡 |
| 일정한 SQNR | 비선형성 |

## 11. 실무에선? (기술사적 판단)
- **오디오 CD**: 16비트 선형 양자화
- **전화망**: 8비트 A-law/μ-law
- **전문 오디오**: 24비트 이상
- **음성 코덱**: 적응형 양자화

## 12. 관련 개념
- 표본화 (Sampling)
- PCM
- 압신 (Companding)
- SQNR

---

## 어린이를 위한 종합 설명

**양자화는 "성적 등급"과 같아요!**

### 균일 양자화 📏
```
점수 → 등급

90-100: A
80-89: B
70-79: C
60-69: D
0-59: F

모든 등급 범위가 같아요 (10점)
```

### 비균일 양자화 📊
```
점수 → 등급

95-100: A+
90-94: A
80-89: B
60-79: C
0-59: F

높은 점수는 세분, 낮은 점수는 넓게!
```

### 양자화 오차 😅
```
원래 점수: 92점
등급: A (90-94)

어디에 해당하는지 정확히 몰라요!
이 차이가 오차예요
```

**비밀**: 양자화 덕분에 아날로그 음악이 디지털로 저장돼요! 🎵✨
