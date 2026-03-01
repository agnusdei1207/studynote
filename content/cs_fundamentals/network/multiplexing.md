+++
title = "다중화 (Multiplexing)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 다중화 (Multiplexing)

## 핵심 인사이트 (3줄 요약)
> **하나의 통신 채널에 여러 신호를 동시에 전송**하는 기술. 주파수, 시간, 파장, 코드 등을 분할하여 자원을 공유한다. 통신 효율성을 높이는 핵심 기술이다.

## 1. 개념
다중화(Multiplexing)는 **하나의 전송 매체를 여러 사용자가 공유**할 수 있도록, 여러 신호를 하나로 합쳐 전송하고 수신 측에서 다시 분리하는 기술이다.

> 비유: "고속도로" - 한 도로에 여러 차선이 있어 많은 차가 동시에 이동

## 2. 기본 구조

```
┌──────┐                    ┌──────┐
│ 입력1 │                    │출력1 │
├──────┤   ┌────────┐        ├──────┤
│ 입력2 │──→│ 다중화 │════════│역다중화│──→│출력2 │
├──────┤   │  기    │  전송  │  기   │  ├──────┤
│ 입력3 │──→│        │════════│        │──→│출력3 │
└──────┘   └────────┘        └──────┘  └──────┘

Mux: 다중화기 (Multiplexer)
Demux: 역다중화기 (Demultiplexer)
```

## 3. 다중화 기법 종류

### 3.1 주파수 분할 다중화 (FDM)

```
개념: 주파수 대역을 나누어 사용

주파수
  ↑
  │  ┌───┐  ┌───┐  ┌───┐  ┌───┐
  │  │CH1│  │CH2│  │CH3│  │CH4│
  │  └───┘  └───┘  └───┘  └───┘
  └───────────────────────────→ 시간

특징:
- 아날로그 신호에 적합
- 보호 대역(Guard Band) 필요
- 예: 라디오 방송, 아날로그 TV
```

### 3.2 시분할 다중화 (TDM)

```
개념: 시간을 슬롯으로 나누어 사용

시간 슬롯
┌────┬────┬────┬────┬────┬────┐
│CH1 │CH2 │CH3 │CH1 │CH2 │CH3 │
└────┴────┴────┴────┴────┴────┘

종류:
- 동기식 TDM: 고정 슬롯 할당
- 비동기식 TDM: 필요시 슬롯 할당 (통계적 TDM)

특징:
- 디지털 신호에 적합
- 동기화 필요
- 예: 전화망, T1/E1
```

### 3.3 파장 분할 다중화 (WDM)

```
개념: 광섬유에서 파장(색상)을 나누어 사용

광섬유
═══════════════════════════════
  λ1  λ2  λ3  λ4  λ5  λ6 ...

종류:
- CWDM (Coarse): 20nm 간격, ~18채널
- DWDM (Dense): 0.8nm 간격, ~160채널

특징:
- 광섬유 대용량화
- 장거리 통신에 적합
```

### 3.4 코드 분할 다중 접속 (CDMA)

```
개념: 고유 코드로 신호를 구분

사용자1: 코드 A (1010) × 데이터
사용자2: 코드 B (1100) × 데이터
사용자3: 코드 C (0110) × 데이터

→ 같은 주파수, 같은 시간 사용 가능
→ 수신 측에서 코드로 분리

특징:
- 주파수/시간 효율 극대화
- 보안성 높음
- 예: 3G 이동통신, GPS
```

## 4. 비교표

| 기법 | 분할 자원 | 아날로그/디지털 | 장점 | 단점 |
|------|----------|----------------|------|------|
| FDM | 주파수 | 아날로그 | 단순 | 보호대역 낭비 |
| TDM | 시간 | 디지털 | 효율적 | 동기화 필요 |
| WDM | 파장 | 광통신 | 대용량 | 장비 고가 |
| CDMA | 코드 | 디지털 | 효율 최고 | 복잡 |

## 5. 상세 비교

### FDM vs TDM

| 항목 | FDM | TDM |
|------|-----|-----|
| 분할 | 주파수 | 시간 |
| 신호 | 아날로그 | 디지털 |
| 낭비 | 보호 대역 | 동기 오버헤드 |
| 간섭 | 주파수 간섭 | 없음 |
| 대역폭 | 고정 할당 | 슬롯 할당 |

### 동기식 vs 비동기식 TDM

```
동기식 TDM (Synchronous TDM):
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │  ← 고정 슬롯
└────┴────┴────┴────┘
단점: 빈 슬롯 낭비

비동기식 TDM (Statistical TDM):
┌────┬────┬────┬────┐
│ 1  │ 3  │ 2  │ 1  │  ← 필요시만
└────┴────┴────┴────┘
장점: 효율적, 단점: 주소 필요
```

## 6. 실제 적용 사례

| 기술 | 다중화 방식 | 용도 |
|------|------------|------|
| 전화망 | FDM/TDM | 음성 통신 |
| T1/E1 | TDM | 디지털 전송 |
| ADSL | FDM | DSL 인터넷 |
| 이더넷 | - | 패킷 교환 |
| WiFi | CSMA/CA | 무선 LAN |
| 3G | CDMA | 이동통신 |
| 4G | OFDMA | LTE |
| 5G | OFDMA/NOMA | 차세대 통신 |
| 광통신 | WDM | 장거리망 |

## 7. 다중 접속 (Multiple Access)

```
다중화: 1:N 통신 (기지국 중심)
다중 접속: N:N 통신 (분산 환경)

구분:
- FDMA: Frequency Division Multiple Access
- TDMA: Time Division Multiple Access
- CDMA: Code Division Multiple Access
- OFDMA: Orthogonal FDMA (4G/5G)
```

## 8. 코드 예시

```python
import numpy as np

class FDM:
    """주파수 분할 다중화 시뮬레이션"""
    def __init__(self, num_channels=4, sample_rate=1000):
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.freqs = [100 + i*50 for i in range(num_channels)]

    def modulate(self, channel_idx, data):
        """각 채널을 다른 주파수로 변조"""
        t = np.linspace(0, 1, self.sample_rate)
        carrier = np.sin(2 * np.pi * self.freqs[channel_idx] * t)
        return data * carrier

    def multiplex(self, data_list):
        """다중화: 모든 신호 합성"""
        multiplexed = np.zeros(self.sample_rate)
        for i, data in enumerate(data_list):
            multiplexed += self.modulate(i, data)
        return multiplexed

class TDM:
    """시분할 다중화 시뮬레이션"""
    def __init__(self, num_channels=4, slot_size=10):
        self.num_channels = num_channels
        self.slot_size = slot_size

    def multiplex(self, data_list):
        """다중화: 시간 슬롯 할당"""
        frame = []
        for i in range(0, len(data_list[0]), self.slot_size):
            for ch_data in data_list:
                frame.extend(ch_data[i:i+self.slot_size])
        return frame

    def demultiplex(self, frame):
        """역다중화: 슬롯 분리"""
        channels = [[] for _ in range(self.num_channels)]
        frame_idx = 0

        while frame_idx < len(frame):
            for ch in range(self.num_channels):
                slot = frame[frame_idx:frame_idx+self.slot_size]
                channels[ch].extend(slot)
                frame_idx += self.slot_size

        return channels

# TDM 테스트
tdm = TDM(num_channels=3, slot_size=5)
data_list = [
    list(range(1, 21)),   # 채널 1
    list(range(101, 121)), # 채널 2
    list(range(201, 221))  # 채널 3
]

multiplexed = tdm.multiplex(data_list)
print("다중화된 프레임:", multiplexed[:30], "...")

demultiplexed = tdm.demultiplex(multiplexed)
print("채널 1 복원:", demultiplexed[0][:10], "...")
```

## 9. 장단점

### 다중화의 장점
- 통신 자원 효율적 사용
- 비용 절감
- 대용량 전송 가능
- 다수 사용자 지원

### 다중화의 단점
- 시스템 복잡도 증가
- 지연 발생 가능
- 동기화 이슈
- 장비 비용

## 10. 실무에선? (기술사적 판단)
- **광통신**: DWDM으로 대용량 전송
- **이동통신**: 세대별 다중화 진화 (FDMA→TDMA→CDMA→OFDMA)
- **DSL**: 주파수 분할로 음성/데이터 동시
- **위성통신**: 대역폭 효율화 핵심 기술

## 11. 관련 개념
- 변조/복조
- 주파수 스펙트럼
- 대역폭
- 다중 접속

---

## 어린이를 위한 종합 설명

**다중화는 "라디오 채널"과 같아요!**

### FDM (주파수 나누기) 📻
```
FM 88.1 - 노래방
FM 91.9 - 뉴스
FM 95.1 - 음악

각 주파수가 다른 방송을 해요!
```

### TDM (시간 나누기) ⏰
```
9:00 - 철수가 말해요
9:01 - 영희가 말해요
9:02 - 민수가 말해요
9:03 - 철수가 다시 말해요

시간을 번갈아 써요!
```

### CDMA (암호 나누기) 🔐
```
철수: "☆★☆" 암호로 말해요
영희: "●○●" 암호로 말해요

같은 시간, 같은 주파수여도
암호가 달라서 구분돼요!
```

**비밀**: 다중화 덕분에 많은 사람이 인터넷을 쓸 수 있어요! 🌐✨
