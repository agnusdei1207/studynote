+++
title = "다중화 (Multiplexing)"
date = 2025-03-01

[extra]
categories = "pe_exam-network"
+++

# 다중화 (Multiplexing)

## 핵심 인사이트 (3줄 요약)
> **하나의 통신 채널에 여러 신호를 동시에 전송**하는 기술. 주파수(FDM), 시간(TDM), 파장(WDM), 코드(CDMA) 분할 방식이 있다. 통신 자원의 효율적 활용으로 대용량 전송과 비용 절감을 실현한다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 다중화(Multiplexing)는 **하나의 전송 매체(케이블, 무선 채널)를 여러 사용자나 신호가 공유**할 수 있도록, 여러 신호를 하나로 합쳐 전송하고 수신 측에서 다시 분리하는 기술이다. 다중화기(Multiplexer, MUX)에서 결합하고, 역다중화기(Demultiplexer, DEMUX)에서 분리한다.

> 💡 **비유**: 다중화는 **"고속도로"** 같아요. 한 도로에 여러 차선(주파수)이 있어 많은 차가 동시에 달릴 수 있죠. 또는 **"회의실"**과 같아요. 한 번에 한 사람만 말하면(TDM) 시간이 오래 걸리지만, 여러 사람이 동시에 다른 언어로 말하면(CDMA) 효율적이에요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 통신 자원 부족**: 전용선은 비싸고, 주파수 스펙트럼은 제한적. 케이블 설치 비용 증가로 인한 경제적 비효율. 단일 채널에 하나의 신호만 전송하면 자원 낭비.
2. **기술적 필요성 - 자원 공유**: 제한된 대역폭을 여러 사용자가 효율적으로 공유. 장거리 전송 비용 절감. 위성, 광케이블 등 고가 매체의 활용도 극대화.
3. **시장/산업 요구 - 대용량 통신**: 스마트폰 보급으로 이동통신 용량 급증. 인터넷 트래픽 폭발로 백본망 대역폭 확장 필요. IoT 기기 수십억 개 연결 요구.

**핵심 목적**: **통신 자원 효율화, 비용 절감, 대용량 전송, 다중 사용자 지원**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**다중화 기본 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                      다중화 시스템 구조                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  송신 측                              수신 측                           │
│  ┌──────┐                             ┌──────┐                          │
│  │입력 1│──┐                     ┌───│출력 1│                          │
│  ├──────┤  │   ┌────────┐        │   ├──────┤                          │
│  │입력 2│──┼──→│  MUX   │════════│──→│ DEMUX │──┼──→│출력 2│          │
│  ├──────┤  │   │다중화기│ 전송   │   │역다중화│  │   ├──────┤          │
│  │입력 3│──┤   │        │ 매체   │   │   기   │──┤                      │
│  ├──────┤  │   └────────┘        │   └────────┘  │   ┌──────┐          │
│  │입력 4│──┘                     └───────────────┘──→│출력 4│          │
│  └──────┘                                             └──────┘          │
│                                                                         │
│  MUX (Multiplexer): 여러 신호를 하나로 결합                             │
│  DEMUX (Demultiplexer): 결합된 신호를 다시 분리                         │
│  전송 매체: 동축케이블, 광섬유, 무선 채널 등                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**다중화 기법 비교** (필수: 표):
| 기법 | 분할 자원 | 아날로그/디지털 | 장점 | 단점 | 대표 용도 |
|------|-----------|-----------------|------|------|-----------|
| **FDM** | 주파수 | 아날로그 | 단순, 연속 전송 | 보호대역 낭비 | 라디오, 아날로그 TV |
| **TDM** | 시간 | 디지털 | 효율적, 동기식 | 동기화 필요 | 전화망, T1/E1 |
| **WDM** | 파장 | 광통신 | 대용량, 장거리 | 장비 고가 | 광 백본망 |
| **CDMA** | 코드 | 디지털 | 최고 효율, 보안 | 구현 복잡 | 3G 이동통신 |
| **OFDM** | 직교 주파수 | 디지털 | 멀티패스 강함 | PAPR 문제 | WiFi, LTE, 5G |

**FDM (주파수 분할 다중화)**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FDM (Frequency Division Multiplexing)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  주파수 (f)                                                             │
│     ↑                                                                   │
│     │  ┌────┐   ┌────┐   ┌────┐   ┌────┐                              │
│     │  │CH1│   │CH2│   │CH3│   │CH4│                              │
│     │  │    │   │    │   │    │   │    │                              │
│     │  └────┘   └────┘   └────┘   └────┘                              │
│     │   ←보호→←보호→←보호→                                             │
│     │   대역  대역  대역                                                │
│     └─────────────────────────────────────────────→ 시간               │
│                                                                         │
│  특징:                                                                  │
│  - 각 채널이 고유 주파수 대역 할당                                       │
│  - 보호 대역(Guard Band)으로 간섭 방지                                  │
│  - 연속 전송 가능 (항상 켜짐)                                           │
│  - 아날로그 신호에 적합                                                  │
│                                                                         │
│  예시: FM 라디오 (88~108MHz를 200kHz 간격)                              │
│        88.1, 88.3, 88.5... (각각 200kHz 간격)                           │
│                                                                         │
│  장점: 연속 전송, 단순 하드웨어                                         │
│  단점: 대역폭 낭비 (보호 대역), 주파수 간섭                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**TDM (시분할 다중화)**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TDM (Time Division Multiplexing)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  동기식 TDM (Synchronous TDM):                                          │
│  ┌────────┬────────┬────────┬────────┬────────┬────────┐               │
│  │  CH1   │  CH2   │  CH3   │  CH4   │  CH1   │  CH2   │               │
│  └────────┴────────┴────────┴────────┴────────┴────────┘               │
│       ↑ 고정 슬롯 할당 (빈 슬롯도 전송 → 낭비)                          │
│                                                                         │
│  비동기식 TDM (Statistical TDM / ATM):                                  │
│  ┌────────┬────────┬────────┬────────┬────────┐                        │
│  │  CH1   │  CH3   │  CH2   │  CH1   │  CH4   │  ← 필요시만            │
│  └────────┴────────┴────────┴────────┴────────┘     + 주소 정보        │
│       ↑ 동적 슬롯 할당 (낭비 없음, 오버헤드 있음)                       │
│                                                                         │
│  특징:                                                                  │
│  - 시간을 슬롯으로 나누어 순차적 전송                                    │
│  - 디지털 신호에 적합                                                    │
│  - 동기화이 필요 (클럭)                                                 │
│  - 대역폭 낭비 없음 (비동기식)                                          │
│                                                                         │
│  T1 프레임 예시:                                                        │
│  - 24개 음성 채널 + 1개 동기 비트 = 193비트                             │
│  - 8,000프레임/초 = 1.544 Mbps                                         │
│                                                                         │
│  장점: 대역폭 효율, 디지털 호환                                         │
│  단점: 동기화 필요, 버스트 트래픽에 비효율                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**WDM (파장 분할 다중화)**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WDM (Wavelength Division Multiplexing)               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  광섬유                                                                  │
│  ═══════════════════════════════════════════════════════                │
│    λ1   λ2   λ3   λ4   λ5   λ6   λ7   λ8 ...                           │
│    ↓    ↓    ↓    ↓    ↓    ↓    ↓    ↓                                │
│  ┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐                     │
│  │10G││10G││10G││10G││10G││10G││10G││10G│                      │
│  └────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘                     │
│                                                                         │
│  CWDM (Coarse WDM):                                                     │
│  - 파장 간격: 20nm                                                      │
│  - 채널 수: 8~18개                                                      │
│  - 용도: 단거리, 저가                                                   │
│  - 예: 1471nm ~ 1611nm                                                  │
│                                                                         │
│  DWDM (Dense WDM):                                                      │
│  - 파장 간격: 0.8nm (100GHz), 0.4nm (50GHz)                            │
│  - 채널 수: 40~160개                                                    │
│  - 용도: 장거리 백본, 대용량                                            │
│  - 예: C-band (1530~1565nm), L-band (1565~1625nm)                      │
│                                                                         │
│  전송 용량 예시:                                                         │
│  - 80채널 × 100Gbps = 8 Tbps (단일 광섬유)                              │
│  - 최신: 800Gbps/채널 × 100+ 채널 = 100+ Tbps                          │
│                                                                         │
│  장점: 초대용량, 장거리 무증폭                                          │
│  단점: 고가 장비, 정밀 파장 제어 필요                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**CDMA (코드 분할 다중 접속)**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CDMA (Code Division Multiple Access)                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  개념: 고유한 코드(스프레드 스펙트럼)로 신호 구분                        │
│                                                                         │
│  스프레딩 코드 예시:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 사용자 1: 코드 A = [+1, +1, +1, -1, -1, +1, -1, -1]            │   │
│  │ 사용자 2: 코드 B = [+1, -1, +1, +1, -1, -1, +1, -1]            │   │
│  │ 사용자 3: 코드 C = [-1, +1, -1, +1, +1, -1, -1, +1]            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  직교성(Orthogonality): 서로 다른 코드는 상관관계 0                     │
│  → A × B = 0, A × C = 0, B × C = 0                                     │
│  → 자신의 코드로만 복원 가능                                            │
│                                                                         │
│  동작 과정:                                                              │
│  송신: 데이터 × 스프레딩 코드 → 확산된 신호                             │
│  수신: 수신 신호 × 자신의 코드 → 원본 데이터 복원                       │
│                                                                         │
│  장점: 같은 주파수/시간 동시 사용, 보안성, 내간섭성                     │
│  단점: 전력 제어 중요, 복잡한 수신기                                     │
│                                                                         │
│  용도: 3G 이동통신, GPS, 군사 통신                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**OFDM (직교 주파수 분할 다중화)**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OFDM (Orthogonal FDM)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  특징: 서로 직교하는 다수의 부반파(subcarrier) 사용                     │
│                                                                         │
│  주파수                                                                  │
│     ↑                                                                   │
│     │   ┌─┐     ┌─┐     ┌─┐     ┌─┐                                   │
│     │   │ │ ┌─┐ │ │ ┌─┐ │ │ ┌─┐ │ │                                   │
│     │   │ │ │ │ │ │ │ │ │ │ │ │ │ │                                   │
│     │───┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴───                                │
│     │  f1   f2   f3   f4   f5   f6                                     │
│     └─────────────────────────────────────→                             │
│                                                                         │
│  직교성: 부반파 간격 = 1/심볼 기간                                       │
│  → 보호 구간 없이 간섭 없이 전송                                        │
│                                                                         │
│  장점:                                                                  │
│  - 멀티패스 페이딩에 강함 (주파수 선택적 페이딩 회피)                    │
│  - 스펙트럼 효율 높음                                                    │
│  - IFFT/FFT로 구현 용이                                                 │
│                                                                         │
│  단점:                                                                  │
│  - PAPR (Peak-to-Average Power Ratio) 높음                             │
│  - 주파수 오프셋에 민감                                                  │
│                                                                         │
│  용도: WiFi (802.11a/g/n/ac), LTE, 5G, DAB, DVB                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[FDM 대역폭 계산]

총 대역폭 = N × (채널 대역폭 + 보호 대역폭)

예: FM 라디오
- 채널 대역폭: 200kHz
- 보호 대역폭: (실질적으로 포함)
- 채널 수: 100개
- 총 대역폭: 20MHz (88~108MHz)

[TDM 프레임 구조]

T1 프레임: 193비트 = 24채널 × 8비트 + 1프레이밍 비트
T1 속도: 193비트 × 8000프레임/초 = 1.544Mbps

E1 프레임: 256비트 = 32채널 × 8비트 (CH0, CH16은 시그널링)
E1 속도: 256비트 × 8000프레임/초 = 2.048Mbps

[WDM 채널 용량]

CWDM: 18채널 × 10Gbps = 180Gbps
DWDM: 160채널 × 100Gbps = 16Tbps
최신: 100+ 채널 × 800Gbps = 80+ Tbps

[CDMA 처리 이득]

처리 이득(Gp) = 칩 속도 / 데이터 속도 = R_c / R_d
- 높을수록 간섭 억제能力强
- IS-95: Gp = 128 (9.6kbps 데이터, 1.2288Mcps 칩)

[OFDM 심볼 기간]

심볼 기간(Ts) = 1 / 부반파 간격(Δf)
FFT 크기(N) = 샘플링 주파수 / 부반파 간격

예: WiFi 802.11a
- 부반파 간격: 312.5kHz
- 심볼 기간: 3.2μs
- FFT 크기: 64
```

**코드 예시** (필수: Python 다중화 시뮬레이터):
```python
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from enum import Enum

# ============================================================
# 다중화 기법 시뮬레이터
# ============================================================

class MultiplexType(Enum):
    FDM = "Frequency Division"
    TDM = "Time Division"
    CDMA = "Code Division"


@dataclass
class Channel:
    """채널 정보"""
    id: int
    name: str
    data: List[float]  # 신호 데이터


class FDMSimulator:
    """주파수 분할 다중화 시뮬레이터"""

    def __init__(self, num_channels: int, sample_rate: int = 1000):
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.base_frequency = 100  # 기본 주파수 (Hz)
        self.channel_spacing = 50  # 채널 간격 (Hz)

    def modulate(self, channel: Channel, carrier_freq: float) -> np.ndarray:
        """AM 변조 (단순화)"""
        t = np.arange(len(channel.data)) / self.sample_rate
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        return channel.data * carrier

    def multiplex(self, channels: List[Channel]) -> np.ndarray:
        """다중화: 모든 채널 신호 결합"""
        multiplexed = np.zeros(sum(len(ch.data) for ch in channels))

        for i, channel in enumerate(channels):
            carrier_freq = self.base_frequency + i * self.channel_spacing
            modulated = self.modulate(channel, carrier_freq)
            multiplexed[:len(modulated)] += modulated

        return multiplexed

    def demultiplex(self, multiplexed: np.ndarray, channel_idx: int) -> np.ndarray:
        """역다중화: 특정 채널 복원"""
        carrier_freq = self.base_frequency + channel_idx * self.channel_spacing
        t = np.arange(len(multiplexed)) / self.sample_rate
        carrier = np.sin(2 * np.pi * carrier_freq * t)

        # 동기 검파
        demodulated = multiplexed * carrier * 2
        return demodulated


class TDMSimulator:
    """시분할 다중화 시뮬레이터"""

    def __init__(self, num_channels: int, slot_size: int = 100):
        self.num_channels = num_channels
        self.slot_size = slot_size  # 각 슬롯의 샘플 수

    def multiplex(self, channels: List[Channel]) -> np.ndarray:
        """동기식 TDM 다중화"""
        # 각 채널에서 슬롯만큼씩 번갈아 가져옴
        total_samples = min(len(ch.data) for ch in channels)
        num_frames = total_samples // self.slot_size

        multiplexed = []
        for frame in range(num_frames):
            for ch in channels:
                start = frame * self.slot_size
                end = start + self.slot_size
                multiplexed.extend(ch.data[start:end])

        return np.array(multiplexed)

    def demultiplex(self, multiplexed: np.ndarray, channel_idx: int) -> np.ndarray:
        """역다중화: 특정 채널 복원"""
        demultiplexed = []
        total_slots = len(multiplexed) // self.slot_size

        for slot in range(channel_idx, total_slots, self.num_channels):
            start = slot * self.slot_size
            end = start + self.slot_size
            demultiplexed.extend(multiplexed[start:end])

        return np.array(demultiplexed)

    def get_frame_structure(self) -> str:
        """프레임 구조 시각화"""
        frame = "TDM 프레임 구조:\n"
        frame += "┌" + "┬".join(["─" * 10] * self.num_channels) + "┐\n"
        frame += "│" + "│".join([f"  CH{i+1}   " for i in range(self.num_channels)]) + "│\n"
        frame += "└" + "┴".join(["─" * 10] * self.num_channels) + "┘"
        return frame


class CDMASimulator:
    """코드 분할 다중 접속 시뮬레이터"""

    def __init__(self, num_users: int, code_length: int = 8):
        self.num_users = num_users
        self.code_length = code_length
        self.codes = self._generate_walsh_codes()

    def _generate_walsh_codes(self) -> np.ndarray:
        """Walsh-Hadamard 코드 생성"""
        # Hadamard 행렬 생성
        H = np.array([[1]])
        while H.shape[0] < self.code_length:
            H = np.block([[H, H], [H, -H]])
        return H[:self.num_users]

    def spread(self, data: np.ndarray, user_idx: int) -> np.ndarray:
        """스프레딩: 데이터 × 코드"""
        code = self.codes[user_idx]
        spread_data = np.repeat(data, self.code_length) * np.tile(code, len(data))
        return spread_data

    def multiplex(self, user_data: List[np.ndarray]) -> np.ndarray:
        """다중화: 모든 사용자 신호 결합"""
        max_len = max(len(d) for d in user_data) * self.code_length
        multiplexed = np.zeros(max_len)

        for user_idx, data in enumerate(user_data):
            spread = self.spread(data, user_idx)
            multiplexed[:len(spread)] += spread

        return multiplexed

    def despread(self, multiplexed: np.ndarray, user_idx: int) -> np.ndarray:
        """디스프레딩: 특정 사용자 데이터 복원"""
        code = self.codes[user_idx]
        num_symbols = len(multiplexed) // self.code_length

        despread_data = []
        for i in range(num_symbols):
            segment = multiplexed[i * self.code_length:(i + 1) * self.code_length]
            # 상관 연산
            correlation = np.sum(segment * code) / self.code_length
            despread_data.append(correlation)

        return np.array(despread_data)

    def check_orthogonality(self) -> str:
        """코드 직교성 확인"""
        result = "Walsh 코드 직교성 검사:\n"
        for i in range(self.num_users):
            for j in range(i + 1, self.num_users):
                dot = np.sum(self.codes[i] * self.codes[j])
                result += f"  Code {i} × Code {j} = {dot}\n"
        return result


class WDMSimulator:
    """파장 분할 다중화 시뮬레이터"""

    def __init__(self, num_channels: int = 8, is_dense: bool = False):
        self.num_channels = num_channels
        self.is_dense = is_dense

        if is_dense:
            self.spacing = 0.8  # nm (DWDM)
            self.base_wavelength = 1530  # nm (C-band)
        else:
            self.spacing = 20  # nm (CWDM)
            self.base_wavelength = 1471  # nm

    def get_channel_wavelengths(self) -> List[float]:
        """각 채널의 파장 계산"""
        return [self.base_wavelength + i * self.spacing
                for i in range(self.num_channels)]

    def get_capacity(self, channel_rate_gbps: float = 100) -> str:
        """전체 용량 계산"""
        total = self.num_channels * channel_rate_gbps
        return f"총 용량: {self.num_channels} 채널 × {channel_rate_gbps}Gbps = {total}Gbps"

    def print_config(self) -> str:
        """설정 정보 출력"""
        wavelengths = self.get_channel_wavelengths()
        config = f"WDM 설정 ({'DWDM' if self.is_dense else 'CWDM'}):\n"
        config += f"  채널 수: {self.num_channels}\n"
        config += f"  파장 간격: {self.spacing}nm\n"
        config += f"  파장 범위: {wavelengths[0]:.1f}nm ~ {wavelengths[-1]:.1f}nm\n"
        return config


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         다중화 기법 시뮬레이터")
    print("=" * 60)

    # 1. TDM 시뮬레이션
    print("\n1. TDM (시분할 다중화) 시뮬레이션")
    print("-" * 40)

    tdm = TDMSimulator(num_channels=4, slot_size=100)

    channels = [
        Channel(1, "음성1", list(np.sin(np.linspace(0, 4*np.pi, 500)))),
        Channel(2, "음성2", list(np.cos(np.linspace(0, 4*np.pi, 500)))),
        Channel(3, "데이터1", list(np.random.randn(500))),
        Channel(4, "데이터2", list(np.random.randn(500))),
    ]

    print(tdm.get_frame_structure())

    multiplexed = tdm.multiplex(channels)
    print(f"\n다중화된 데이터 길이: {len(multiplexed)} 샘플")

    recovered = tdm.demultiplex(multiplexed, 0)
    print(f"복원된 CH1 데이터 길이: {len(recovered)} 샘플")

    # 2. CDMA 시뮬레이션
    print("\n\n2. CDMA (코드 분할 다중 접속) 시뮬레이션")
    print("-" * 40)

    cdma = CDMASimulator(num_users=4, code_length=8)

    print(cdma.check_orthogonality())

    user_data = [
        np.array([1, -1, 1, 1]),   # 사용자 1
        np.array([-1, 1, -1, 1]),  # 사용자 2
        np.array([1, 1, -1, -1]),  # 사용자 3
        np.array([-1, -1, 1, 1]),  # 사용자 4
    ]

    multiplexed = cdma.multiplex(user_data)
    print(f"다중화된 데이터 길이: {len(multiplexed)} 칩")

    for user_idx in range(4):
        recovered = cdma.despread(multiplexed, user_idx)
        print(f"사용자 {user_idx+1} 복원: {np.round(recovered, 2)}")

    # 3. WDM 설정
    print("\n\n3. WDM (파장 분할 다중화) 시뮬레이션")
    print("-" * 40)

    cwdm = WDMSimulator(num_channels=8, is_dense=False)
    print(cwdm.print_config())
    print(cwdm.get_capacity(10))

    dwdm = WDMSimulator(num_channels=80, is_dense=True)
    print(dwdm.print_config())
    print(dwdm.get_capacity(100))
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| FDM 장점 | FDM 단점 |
|----------|----------|
| 연속 전송 가능 (항상 켜짐) | 보호 대역으로 대역폭 낭비 |
| 구현 단순, 하드웨어 간단 | 주파수 간섭 문제 |
| 아날로그/디지털 모두 가능 | 채널 수 제한 |
| 라디오, TV 등 광범위 사용 | 주파수 할당 복잡 |

| TDM 장점 | TDM 단점 |
|----------|----------|
| 대역폭 효율적 사용 | 동기화 필수 |
| 디지털 시스템 호환 | 버스트 트래픽에 비효율 |
| 보호 대역 불필요 | 클럭 오류 시 전체 영향 |
| 전화망 등 검증된 기술 | 지연 발생 가능 |

| CDMA 장점 | CDMA 단점 |
|-----------|-----------|
| 최고 스펙트럼 효율 | 구현 매우 복잡 |
| 보안성 높음 | 전력 제어 중요 |
| 내간섭성 강함 | 단말기 가격 높음 |
| 소프트 핸드오버 | 셀 경계 간섭 |

**다중화 기법 종합 비교** (필수: 최소 2개 대안):
| 비교 항목 | FDM | TDM | WDM | CDMA | OFDM |
|-----------|-----|-----|-----|------|------|
| **분할 자원** | 주파수 | 시간 | 파장 | 코드 | 직교 주파수 |
| **신호 타입** | 아날로그 | 디지털 | 광 | 디지털 | 디지털 |
| **스펙트럼 효율** | 낮음 | 중간 | ★ 높음 | ★★ 최고 | ★ 높음 |
| **구현 복잡도** | ★ 낮음 | 중간 | 높음 | ★★ 최고 | 높음 |
| **멀티패스 내성** | 낮음 | 중간 | 높음 | 높음 | ★★ 최고 |
| **보안성** | 낮음 | 낮음 | 중간 | ★ 높음 | 중간 |
| **대표 용도** | 라디오 | 전화망 | 광통신 | 3G | ★★ 4G/5G/WiFi |
| **비용** | 낮음 | 중간 | 높음 | 높음 | 중간 |

> **★ 선택 기준**:
> - **FDM**: 아날로그 신호, 단순 구현, 비용 중심 (라디오 방송)
> - **TDM**: 디지털 음성, 전화망, 동기식 전송 (T1/E1)
> - **WDM**: 광통신 대용량, 장거리 백본 (해저 케이블)
> - **CDMA**: 이동통신, 보안 필요, 스펙트럼 효율 (3G)
> - **OFDM**: 무선 광대역, 멀티패스 환경 (WiFi, LTE, 5G)

**동기식 vs 비동기식 TDM 비교**:
| 비교 항목 | 동기식 TDM | 비동기식 (통계적) TDM |
|-----------|------------|----------------------|
| 슬롯 할당 | 고정 | 동적 (요청시) |
| 빈 슬롯 | 존재 (낭비) | 없음 |
| 주소 정보 | 불필요 | 필요 |
| 오버헤드 | 낮음 | 높음 (주소) |
| 효율 | 버스트 트래픽에 낮음 | ★ 높음 |
| 구현 | 단순 | 복잡 |
| 예 | T1/E1, SONET/SDH | ATM, 프레임 릴레이 |

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|-----------|-----------------|------------------|
| **광 백본망** | DWDM 80채널 × 100Gbps로 해저 케이블 구성 | 8Tbps 대용량, 비용 70% 절감 |
| **이동통신** | 5G NR에서 OFDM + Massive MIMO | 주파수 효율 3배, 지연 1ms |
| **엔터프라이즈** | CWDM으로 데이터센터 간 연결 | 8파장 × 10G, 설치비 50% 절감 |
| **위성통신** | FDM/TDM 하이브리드로 트랜스폰더 공유 | 대역폭 활용률 90% 이상 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1: 구글 해저 케이블 (FASTER)** - 일본-미국 간 DWDM 60Tbps 전송. 100Gbps × 100파장 × 6페어. 9,000km 무증폭 구간에 EDFA 배치.
- **사례 2: SK텔레콤 5G** - OFDM 기반 NR(New Radio)로 3.5GHz 대역 활용. mmWave 28GHz에서 400MHz 대역폭으로 10Gbps 달성.
- **사례 3: KT 광액세스** - GPON으로 1:64 분기비. 단일 광섬유로 64가구에 2.5Gbps 제공. TDM으로 업/다운링크 분할.

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 신호 특성 (아날로그 vs 디지털)
   - 대역폭 요구사항
   - 전송 거리와 매체 특성
   - 기존 인프라 호환성

2. **운영적**:
   - 동기화 유지 (TDM)
   - 전력 제어 (CDMA)
   - 파장 안정성 (WDM)
   - 장애 격리 및 복구

3. **보안적**:
   - 채널 간 간섭 방지
   - 도청 방지 (CDMA 보안성)
   - 암호화 필요성
   - 물리적 보안

4. **경제적**:
   - 초기 장비 비용
   - 주파수 사용료
   - 운영 비용
   - 확장성과 ROI

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **FDM 보호 대역 무시**: 간섭 발생으로 신호 품질 저하 → 충분한 보호 대역 설계 필수
- ❌ **TDM 동기화 오류**: 클럭 불일치로 슬롯 경계 오류 → 정밀 클럭 동기화 (GPS/PTP) 필요
- ❌ **CDMA 전력 제어 소홀**: 근-원거리 문제(Near-Far Problem) → 정밀 전력 제어 루프 필수

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 다중화 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                    Multiplexing                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   변조 ←──→ 다중화 ←──→ 다중 접속                                │
│     ↓          ↓          ↓                                     │
│   AM/FM      FDM/TDM    FDMA/TDMA                               │
│   QAM       WDM/CDMA    CDMA/OFDMA                              │
│     ↓          ↓          ↓                                     │
│   무선통신   광통신     이동통신                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 변복조 | 선행 기술 | 다중화된 신호의 변조/복조 | `[변조](./modulation.md)` |
| 무선 통신 | 응용 분야 | 무선 채널에서 다중화 적용 | `[무선통신](./wireless_communication.md)` |
| 이동통신 | 응용 분야 | FDMA/TDMA/CDMA/OFDMA 진화 | `[이동통신](./mobile_communication.md)` |
| 광통신 | 응용 분야 | WDM 기반 대용량 전송 | `[광통신](./optical_communication.md)` |
| 안테나 | 하드웨어 | 무선 다중화 신호 송수신 | `[안테나](./antenna.md)` |
| 이더넷 | 대안 기술 | 패킷 교환 방식의 다중화 | `[이더넷](./ethernet.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|-----------|-------------|-------------|
| **대역폭 효율** | 단일 매체로 다중 신호 전송 | 스펙트럼 효율 90% 이상 |
| **비용 절감** | 전송 매체 및 장비 공유 | 설치 비용 60% 절감 |
| **확장성** | 채널 추가로 용량 증설 | 선형적 용량 확장 |
| **신호 품질** | 디지털 다중화로 잡음 제거 | BER 10^-9 이하 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**:
   - **FlexO (Flexible OTN)**: OTN 프레임의 유연한 다중화, 400G/800G 지원
   - **SDM (Space Division Multiplexing)**: 다중 코어 광섬유로 차세대 대용량
   - **NOMA (Non-Orthogonal Multiple Access)**: 5G/6G의 비직교 다중 접속

2. **시장 트렌드**:
   - 데이터센터 간 400G/800G 연결 수요 폭증
   - 위성 인터넷(Starlink)의 FDM/TDM 하이브리드
   - IoT를 위한 저전력 다중화 기술

3. **후속 기술**:
   - ** coherent O**FDM: 광통신에서 OFDM과 코히어런트 검파 결합
   - **Massive MIMO**: 수십 개 안테나로 공간 다중화 (Spatial Multiplexing)
   - **Full Duplex**: 동일 주파수로 동시 송수신 (자기 간섭 제거)

> **결론**: 다중화는 통신 자원의 **효율적 활용을 위한 핵심 기술**이다. FDM에서 시작해 TDM, CDMA, OFDM으로 진화하며 스펙트럼 효율을 극대화해 왔다. 5G/6G 시대에는 OFDM과 Massive MIMO의 공간 다중화, 그리고 광통신의 SDM까지 결합하여 Tbps급 초고속 통신을 실현할 것이다. 기술사는 각 기법의 장단점과 적용 환경을 이해하고, 하이브리드 다중화 전략을 수립할 수 있어야 한다.

> **※ 참고 표준**: ITU-T G.694.1 (DWDM 격자), ITU-T G.694.2 (CWDM 격자), 3GPP TS 36.211 (LTE OFDM), IEEE 802.11 (WiFi OFDM), ITU-T G.709 (OTN)

---

## 어린이를 위한 종합 설명 (필수)

**다중화는 "고속도로에서 많은 차가 동시에 달리는 방법"이에요!**

상상해 보세요. 도로가 하나뿐이면 한 번에 한 대의 차만 지나갈 수 있어요. 그러면 너무 느리겠죠? 😢

다중화는 이 문제를 해결하는 **똑똑한 방법**이에요!

```
[다중화 없이]               [다중화 있이]

  ┌───┐                      ┌───┬───┬───┬───┐
  │ 🚗 │                      │ 🚗 │ 🚙 │ 🚌 │ 🚕 │
  └───┘                      └───┴───┴───┴───┘
    ↓                            ↓ ↓ ↓ ↓
  ═════                        ═══════════
  도로 1개                      도로 4차선
  (한 대씩만)                   (4대 동시에!)
```

**FDM (주파수 분할) = "라디오 채널"**

```
라디오를 생각해 보세요!

FM 88.1MHz → KBS 라디오 📻
FM 89.1MHz → MBC 라디오 📻
FM 91.9MHz → SBS 라디오 📻

각 방송국이 **다른 주파수**를 써서
동시에 방송할 수 있어요!
→ 이게 바로 FDM이에요! 🎵
```

**TDM (시분할) = "한 사람씩 말하기"**

```
회의실에서 한 번에 한 사람만 말하면...

사람1: "안녕하세요" (5초)
      ↓ 기다려요...
사람2: "반가워요" (5초)
      ↓ 또 기다려요...
사람3: "잘 있어요" (5초)

→ 하지만 아주 빠르게 번갈아 말하면
   모두가 동시에 말하는 것처럼 들려요!
   이게 TDM이에요! ⏰
```

**WDM (파장 분할) = "무지개 빛"**

```
광케이블은 빛(파장)을 이용해요!

빨강 빛 → 데이터 1 🔴
주황 빛 → 데이터 2 🟠
초록 빛 → 데이터 3 🟢
파랑 빛 → 데이터 4 🔵

하나의 광케이블에 **여러 색의 빛**을 보내면
한 번에 엄청 많은 데이터를 보낼 수 있어요!
→ 이게 WDM이에요! 🌈
```

**CDMA (코드 분할) = "다른 언어로 말하기"**

```
방에 4명이 있어요. 동시에 말하면 시끄럽겠죠?

하지만! 각자 **다른 언어**로 말하면?

철수: "안녕하세요" (한국어) 🇰🇷
Mary: "Hello" (영어) 🇺🇸
田中: "こんにちは" (일본어) 🇯🇵
Pierre: "Bonjour" (프랑스어) 🇫🇷

→ 자기 언어만 들으면 돼요!
   이게 CDMA의 원리예요! 🗣️
```

**핵심 한 줄:**
> 다중화 = 하나의 도로(채널)에 여러 차(신호)가 동시에 달리는 똑똑한 방법!

---
