+++
title = "광통신 (Optical Communication)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 광통신 (Optical Communication)

## 핵심 인사이트 (3줄 요약)
> **빛(광)을 이용해 정보를 전송**하는 통신 방식. 광섬유를 통해 대용량, 장거리, 고속 전송이 가능하다. 현대 통신망의 핵심 인프라이다.

## 1. 개념
광통신은 **광섬유를 매체로 하여 빛의 신호로 데이터를 전송**하는 통신 기술로, 레이저나 LED가 발생시킨 빛을 광섬유를 통해 전달한다.

> 비유: "광케이블은 빛의 고속도로" - 빛의 속도로 데이터 전송

## 2. 광통신 시스템 구성

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  전기    │    │          │    │          │    │  전기    │
│  신호    │──→ │  광송신기 │════│  광섬유  │════│  광수신기 │──→ │  신호    │
│ (입력)   │    │ (E/O변환)│    │          │    │ (O/E변환)│    │ (출력)   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘

구성 요소:
1. 광송신기: 전기 → 광 변환 (E/O)
2. 광섬유: 광 전송 매체
3. 광수신기: 광 → 전기 변환 (O/E)
4. 광증폭기: 신호 증폭 (선택)
```

## 3. 광섬유 (Optical Fiber)

### 3.1 구조
```
┌─────────────────────────────┐
│         코어 (Core)          │ ← 빛이 지나가는 중심부
│         (n₁)                 │
├─────────────────────────────┤
│      클래드 (Cladding)       │ ← 전반사 유도
│         (n₂ < n₁)           │
├─────────────────────────────┤
│      버퍼 (Buffer)          │ ← 보호 피복
└─────────────────────────────┘

전반사 조건: n₁ > n₂
입사각 > 임계각 → 빛이 코어 내부에서 반사
```

### 3.2 광섬유 종류

| 종류 | 코어 크기 | 특징 | 용도 |
|------|----------|------|------|
| SMF (단일모드) | ~9μm | 장거리, 고속 | 장거리 통신 |
| MMF (다중모드) | 50~62.5μm | 단거리, 저가 | LAN, 데이터센터 |

```
SMF (Single Mode Fiber):
- 하나의 모드만 전파
- 분산 적음
- 레이저 광원 필요

MMF (Multi Mode Fiber):
- 여러 모드 전파
- 모드 간 분산 발생
- LED 광원 가능
```

### 3.3 광 손실 요인

```
1. 흡수 손실 (Absorption)
   - 재료 내 전자 에너지 흡수
   - 불순물 흡수

2. 산란 손실 (Scattering)
   - 레일리 산란: 밀도 불균일
   - 마이엘 산란: 불순물

3. 구조적 손실
   - 마이크로벤딩: 미세 굴곡
   - 매크로벤딩: 큰 굴곡

4. 연결 손실
   - 정렬 불량
   - 코어 직경 차이
```

## 4. 발광/수광 소자

### 4.1 발광 소자

| 소자 | 원리 | 특징 | 용도 |
|------|------|------|------|
| LED | 전계발광 | 저가, 넓은 스펙트럼 | 단거리 |
| LD (레이저다이오드) | 유도방출 | 좁은 스펙트럼, 고출력 | 장거리 |
| VCSEL | 수직공동 | 고효율, 병렬화 | 데이터센터 |

### 4.2 수광 소자

| 소자 | 원리 | 특징 |
|------|------|------|
| PIN 포토다이오드 | 광전효과 | 선형 응답 |
| APD (애벌란치 PD) | 눈사태 증폭 | 높은 감도 |

## 5. 광증폭기

### 5.1 EDFA (에르븀 첨가 광섬유 증폭기)
```
구조:
입력 광 ─→[WDM]─→[Er-doped Fiber]─→[WDM]─→ 출력 광
              ↑
         [펌프 레이저]

원리:
1. 펌프 레이저로 Er 이온 여기
2. 신호 광이 지나면 유도 방출
3. 신호 광 증폭

특징:
- 1550nm 대역 증폭
- 저잡음
- 광대역 (30~40nm)
```

### 5.2 라만 증폭기
```
원리: 라만 산란 이용

특징:
- 광대역
- 분산형 증폭
- 잡음 낮음
```

## 6. 파장 분할 다중화 (WDM)

```
개념: 여러 파장을 하나의 광섬유에 동시 전송

        λ₁ ──┐
        λ₂ ──┼──→ [MUX] ──→ 광섬유 ──→ [DEMUX] ──┼── λ₁
        λ₃ ──┤                                    ├── λ₂
        λ₄ ──┘                                    ├── λ₃
                                                   └── λ₄

CWDM (Coarse WDM):
- 20nm 간격
- 8~18 채널
- 단거리

DWDM (Dense WDM):
- 0.8nm 간격
- 40~160 채널
- 장거리, 대용량
```

## 7. 광교환 기술

```
광교환: 광 신호를 전기 변환 없이 광 상태에서 스위칭

종류:

1. 공간 분할형 광교환
   - MEMS 미러
   - 광 스위치

2. 파장 분할형 광교환
   - 파장 변환
   - 파장 라우팅

3. 시분할형 광교환
   - 광 지연선 이용

장점:
- 전기-광 변환 불필요
- 투명성 (프로토콜 독립)
- 대용량 처리
```

## 8. 광통신 시스템 성능

### 8.1 성능 지표
```
1. 전송 용량 (Capacity)
   - bps 단위
   - WDM: Tb/s급

2. 전송 거리 (Reach)
   - 증폭기 간격
   - SMF: 80~100km

3. BER (Bit Error Rate)
   - 목표: 10⁻¹² 이하
   - FEC로 개선

4. OSNR (Optical SNR)
   - 신호 대 잡음비
   - 높을수록 좋음
```

### 8.2 분산
```
1. 모드 분산 (MMF)
   - 모드 간 경로 차이
   - 대역폭 제한

2. 색분산 (Chromatic Dispersion)
   - 파장별 속도 차이
   - SMF: ~17ps/nm/km

3. 편광 모드 분산 (PMD)
   - 편광 간 속도 차이
   - 고속 전송 제한
```

## 9. 솔리톤 전송

```
개념: 비선형 효과와 분산 효과가 상쇄되어 펄스 형태 유지

특징:
- 장거리 무왜곡 전송
- 고속 (40Gb/s 이상)
- 광 증폭기와 조합

조건:
- 적정 펄스 폭
- 적정 파워
```

## 10. 코드 예시

```python
import numpy as np

class OpticalFiber:
    """광섬유 시뮬레이션"""

    def __init__(self, length=100, attenuation=0.2, dispersion=17):
        self.length = length           # km
        self.attenuation = attenuation  # dB/km
        self.dispersion = dispersion    # ps/nm/km

    def calculate_loss(self):
        """광 손실 계산"""
        total_loss = self.attenuation * self.length
        return total_loss

    def calculate_power(self, input_power_dbm):
        """출력 전력 계산"""
        loss = self.calculate_loss()
        output_power = input_power_dbm - loss
        return output_power

    def calculate_dispersion(self, bandwidth_nm):
        """분산 계산"""
        total_dispersion = self.dispersion * self.length * bandwidth_nm
        return total_dispersion  # ps


class WDMSystem:
    """WDM 시스템 시뮬레이션"""

    def __init__(self, num_channels=40, channel_spacing=0.8):
        self.num_channels = num_channels
        self.channel_spacing = channel_spacing  # nm
        self.base_wavelength = 1530  # nm

    def calculate_wavelengths(self):
        """파장 채널 계산"""
        wavelengths = [
            self.base_wavelength + i * self.channel_spacing
            for i in range(self.num_channels)
        ]
        return wavelengths

    def calculate_total_bandwidth(self):
        """전체 대역폭 계산"""
        return (self.num_channels - 1) * self.channel_spacing

    def calculate_capacity(self, bitrate_per_channel=10):
        """전체 용량 계산 (Gbps)"""
        return self.num_channels * bitrate_per_channel


class EDFA:
    """EDFA 광증폭기 시뮬레이션"""

    def __init__(self, gain=20, noise_figure=5):
        self.gain = gain            # dB
        self.noise_figure = noise_figure  # dB

    def amplify(self, input_power_dbm):
        """신호 증폭"""
        output_power = input_power_dbm + self.gain
        return output_power

    def calculate_osnr(self, input_osnr_db):
        """OSNR 계산"""
        # 간단화된 모델
        output_osnr = input_osnr_db - self.noise_figure
        return output_osnr


# 시뮬레이션
print("=== 광섬유 전송 시뮬레이션 ===")
fiber = OpticalFiber(length=80, attenuation=0.2)

input_power = 0  # dBm
output_power = fiber.calculate_power(input_power)
print(f"입력 전력: {input_power} dBm")
print(f"80km 전송 후: {output_power} dBm")
print(f"총 손실: {fiber.calculate_loss()} dB")

print("\n=== WDM 시스템 ===")
wdm = WDMSystem(num_channels=80, channel_spacing=0.8)
print(f"채널 수: {wdm.num_channels}")
print(f"전체 대역폭: {wdm.calculate_total_bandwidth():.1f} nm")
print(f"전체 용량 (10G/채널): {wdm.calculate_capacity(10)} Gbps")

print("\n=== EDFA 증폭 ===")
edfa = EDFA(gain=20, noise_figure=5)
amp_output = edfa.amplify(output_power)
print(f"증폭 후 전력: {amp_output} dBm")
print(f"증폭기 이득: {edfa.gain} dB")
```

## 11. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 대용량 | Tb/s급 전송 |
| 장거리 | 100km+ 무증폭 |
| 경량 | 동선의 1/10 |
| 전자파 간섭 없음 | 유리 매체 |
| 보안성 | 도청 어려움 |

### 단점
| 단점 | 설명 |
|-----|------|
| 높은 비용 | 장비, 설치 |
| 취약성 | 굴곡, 연결 |
| 복잡성 | 정밀 정렬 필요 |

## 12. 실무에선? (기술사적 판단)
- **백본망**: DWDM 필수
- **데이터센터**: MMF + VCSEL
- **해저 케이블**: EDFA + 솔리톤
- **FTTH**: PON 기술

## 13. 관련 개념
- 광섬유
- WDM
- EDFA
- 파장

---

## 어린이를 위한 종합 설명

**광통신은 "빛으로 편지 보내기"야!**

### 광섬유 💡
```
빛이 지나가는 얇은 유리관이에요!

┌──────────────────┐
│ ──────────────── │ ← 빛이 지나가요
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │ ← 벽이에요
└──────────────────┘

빛이 벽에 부딪혀도 튕겨서 계속 가요!
```

### WDM (무지개 통신) 🌈
```
빨강 파장: 채널 1
주황 파장: 채널 2
노랑 파장: 채널 3
...

하나의 광섬유에 여러 색이 함께 가요!
```

### EDFA (빛 증폭기) 🔦
```
빛이 멀리 가면 점점 어두워져요

EDFA가 빛을 다시 밝게 해줘요!
→ 더 멀리 갈 수 있어요!
```

**비밀**: 광케이블 덕분에 인터넷이 빨라요! 🚀✨
