+++
title = "NW #20 나이퀴스트 채널 용량 (Nyquist Capacity) - 무잡음 채널"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #20 나이퀴스트 채널 용량 (Nyquist Capacity) - 무잡음 채널

> **핵심 인사이트**:
> 1. **본질**: 잡음(Noise)이 없는 이상적인 채널에서 대역폭(Bandwidth)과 신호 레벨 수(Multi-level)에 의해 결정되는 이론적 데이터 전송 상한선으로, 심볼 간 간섭(ISI)이 발생하지 않는 전송 속도의 한계를 수학적으로 정의합니다.
> 2. **가치**: 통신 시스템 설계 시 물리적 매체의 주파수 효율성을 극대화하는 기준이 되며, 변조(Modulation) 방식별 전송 효율을 bps 단위로 정량화하여 망 계획 수립 시 필수적인 지표를 제공합니다.
> 3. **융합**: 정보 통신 이론의 시초이자 A/D 변환(Pulse Code Modulation)의 기초이며, 샤논 용량(Shannon Capacity)과 결합하여 실무 환경에서의 '이상적 한계 vs 현실적 한계'를 분석하는 프레임워크를 제공합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**나이퀴스트 채널 용량 (Nyquist Channel Capacity)**은 1924년 해리 나이퀴스트(Harry Nyquist)가 제안한 이론으로, **잡음이 전혀 없는(Noiseless)** 이상적인 와이어 채널에서 오류 없이 데이터를 전송할 수 있는 최대 속도를 의미합니다. 이는 데이터 신호를 전기적 파형으로 변환하여 전송하는 **기저 대역(Baseband) 전송**의 핵심 원리입니다.

### 2. 작동 근간 및 배경
통신의 초창기에는 전신선을 통해 얼마나 많은 펄스를 보낼 수 있는가가 주된 관심사였습니다. 나이퀴스트는 주파수 대역폭 $B$를 가진 채널은 최대 초당 $2B$개의 독립적인 펄스(심볼)를 전송할 수 있음을 증명했습니다. 이는 **나이퀴스트 속도(Nyquist Rate)**라 불리며, **신호 처리(Signal Processing)**와 **변조 이론(Modulation Theory)**의 근간이 됩니다.

### 💡 비유
도로의 차선 수(대역폭)가 고정되어 있을 때, 단순히 1인승 승용차(1비트)만 보내는 것이 아니라, 대형 버스(다중 레벨 심볼)로 사람(비트)을 가득 채워 보내면 도로 혼잡(신호 간섭)을 일으키지 않고 운송 효율을 $log_2(M)$배만큼 높일 수 있는 것과 같습니다.

### 3. 발전 배경
① **기존 한계**: 단순한 ON/OFF(이진) 전송 방식은 전송 속도가 대역폭에 비례하여 선형적으로 증가하여 비효율적임.
② **혁신적 패라다임**: 하나의 심볼(Signal Element)이 여러 비트를 담을 수 있는 **다단 변조(M-ary Modulation)** 기법을 도입하여 효율 혁신.
③ **현재 비즈니스 요구**: 광섬유와 동축 케이블 등 고주파 대역폭을 활용하는 5G, Wi-Fi 7 등의 현대 통신에서 변조 효율(Spectral Efficiency)을 계산하는 필수 공식으로 활용됨.

### 📢 섹션 요약 비유
> 나이퀴스트 용량은 '도로의 폭(대역폭)이 정해졌을 때, 차선당 얼마나 많은 사람을 태운 버스(심볼 레벨)를 통과시킬 수 있는지'를 나타내는 물리적 법칙입니다. 버스가 너무 크면 인접 차선을 침범하듯, 레벨이 너무 높으면 잡음에 취약해집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 매개변수 분석

나이퀴스트 공식 $C = 2B \log_2 M$을 구성하는 핵심 요소들과 그 내부 동작은 다음과 같습니다.

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 단위/특징 |
|:---|:---|:---|:---|
| **$B$** | **Bandwidth (대역폭)** | 채널이 통과시킬 수 있는 주파수 범위. $0 \sim B$ Hz의 차단 주파수(Cutoff Frequency)를 가짐. | Hertz (Hz) |
| **$M$** | **Signal Level (신호 레벨 수)** | 하나의 심볼이 가질 수 있는 이산적인 상태의 개수 (예: Binary $M=2$, Quaternary $M=4$). | Integer ($2^k$) |
| **$L$** | **Bit Rate (비트 전송률, $C$)** | 1초 동안 전송되는 총 비트 수. 심볼 속도와 심볼당 비트 수의 곱. | bps (bits per second) |
| **$k$** | **Bits per Symbol** | $M = 2^k$ 관계를 만족. $k$가 1 증가할 때마다 레벨 수는 제곱으로 증가하여 SNR 요구치가 급격히 상승함. | bits/symbol |

### 2. 수학적 모델링 및 ASCII 다이어그램

나이퀴스트 정리에 따르면, 대역폭 $B$인 채널에서 **심볼 속도(Symbol Rate, $Baud$)**의 최대치는 $2B$입니다. 여기에 다중 레벨링을 적용한 데이터 흐름은 다음과 같습니다.

```ascii
[ Nyquist Bit Rate Calculation Flow ]

      Input Data (Bits)
      -----------------     1. Grouping
             |               0100 0110 (8 bits)       [k = 2 bits/symbol]
             V                  |  |  |
      +-------------+          V  V  V
      |  Modulator  |     +---------+---------+       [M = 4 levels]
      |   (Encoder) |     | Symbol 1 | Symbol 2 |      (0, 1, 2, 3)
      +-------------+     +---------+---------+
             |                   |
      -----------------     2. Transmission
             |                   V
      Channel (Bandwidth B)   Pulse (Voltage) Shape
      Limit: 2 * B Pulses/sec
             |                   |
             V                   V
      Output per Second = (2 * B) symbols * k bits
      => C = 2 * B * log2(M)
```

**[다이어그램 해설]**
1.  **데이터 변환 과정**: 입력된 연속적인 비트 스트림은 $k$개씩 묶여서 하나의 심볼(Symbol)로 변환됩니다. $k=\log_2(M)$이므로, $M=4$인 경우 2비트가 1개 심볼이 됩니다.
2.  **심볼 전송 (Pulse Transmission)**: 채널의 물리적 대역폭 $B$는 '구멍의 크기'에 비유되며, 1초에 통과할 수 있는 펄스의 최대 개수는 **$2B$개**로 제한됩니다. 이는 **NRZ(Non-Return-to-Zero)**나 **Manchester** 인코딩 등의 선로 부호(Line Code) 설계 시 중요한 제약 조건이 됩니다.
3.  **용량 산출**: 결론적으로 전송 용량 $C$는 1초 동안 보낼 수 있는 최대 펄스 수($2B$)에 펄스 하나가 담는 정보량($\log_2 M$)을 곱하여 결정됩니다.

### 3. 핵심 알고리즘 및 코드
변조 레벨 $M$과 대역폭 $B$가 주어졌을 때, 이론적 최대 전송률을 계산하는 Python 함수는 다음과 같습니다.

```python
import math

def calculate_nyquist_capacity(bandwidth_hz, signal_levels_M):
    """
    Calculates the Nyquist Channel Capacity for a noiseless channel.
    
    Parameters:
    bandwidth_hz (float): Channel Bandwidth (B) in Hz
    signal_levels_M (int): Number of discrete signal levels (M), must be power of 2
    
    Returns:
    float: Maximum Data Rate (C) in bps
    """
    if signal_levels_M <= 0 or (signal_levels_M & (signal_levels_M - 1)) != 0:
        raise ValueError("Signal Levels (M) must be a positive power of 2.")
        
    bits_per_symbol = math.log2(signal_levels_M)
    max_baud_rate = 2 * bandwidth_hz  # Nyquist Rate: 2B pulses/sec
    
    capacity_bps = max_baud_rate * bits_per_symbol
    return capacity_bps

# Example: 3kHz Bandwidth with 8 Levels (8-PSK)
# M=8 implies log2(8) = 3 bits per symbol.
# Rate = 2 * 3000 * 3 = 18,000 bps
print(f"Capacity: {calculate_nyquist_capacity(3000, 8)} bps")
```

### 📢 섹션 요약 비유
> 나이퀴스트 공식은 마치 '고속도로 톨게이트'의 수용 능력을 계산하는 것과 같습니다. 톨게이트 문의 폭(대역폭)이 넓을수록, 그리고 차량 1대에 싣는 탑승객(비트) 수가 늘어날수록 1시간(1초)당 통과할 수 있는 총 인원(채널 용량)이 늘어나는 원리입니다. 하지만 차량이 너무 커지면(레벨 증가) 톨게이트를 통과하기 어려워질 것입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 나이퀴스트 vs 샤논 (The Two Pillars of Information Theory)

통신 공학에서 가장 중요하게 비교되는 두 가지 한계치는 **잡음 유무(Noise)**에 따른 차이를 보입니다.

| 비교 항목 (Criteria) | 나이퀴스트 용량 (Nyquist Capacity) | 샤논 용량 (Shannon Capacity) |
|:---|:---|:---|
| **환경 가정** | **무잡음 (Noiseless)** 이상적 채널 | **잡음 존재 (Noisy)** 실제 채널 |
| **결정 요인** | 대역폭($B$), 레벨 수($M$) | 대역폭($B$), **신호대잡음비(SNR)** |
| **수식** | $C = 2B \log_2 M$ | $C = B \log_2 (1 + \text{SNR})$ |
| **속도의 한계** | 유한 ($M$이 커질수록 증가) | 유한 ($B$와 전력에 의해 한계 존재) |
| **기술적 의의** | **디지털 변조(M-ary)**의 효율성 규명 | **오류 제어(Error Control)**의 물리적 한계 규명 |

### 2. 분석: 왜 $M$을 무한히 늘릴 수 없는가?
나이퀴스트 공식상으로는 $M \to \infty$이면 $C \to \infty$가 성립합니다. 그러나 실제로는 다음과 같은 이유로 불가능합니다.
*   **잡음에 대한 취약성**: 신호 레벨이 세밀해질수록 잡음이 섞여도 0과 1, 혹은 레벨 1과 레벨 2를 구별하기 어려워 **Bit Error Rate (BER, 비트 오류율)**이 급격히 증가합니다.
*   **회로 복잡도**: $M$이 증가할수록 수신부에서 정확한 레벨을 판별하기 위한 **ADC (Analog-to-Digital Converter)**의 해상도와 처리 전력이 필요합니다.

### 3. 타 영역(컴퓨터 구조)과의 융합
*   **메모리 대역폭**: DRAM이나 VRAM의 전송 속도(Memory Bandwidth) 산정 시 클럭(Clock) 주파수를 $B$로 보고, 한 클럭 당 전송되는 데이터 비트 수(DDR의 Prefetch 등)를 $M$의 역할로 해석하여 대역폭을 계산합니다.
    *   예: DDR4-3200 (3200 Mbps/pin) = $1600\,\text{MHz} (Clock) \times 2\,\text{(Data Rate)} \times \text{Bus Width}$

### 📢 섹션 요약 비유
> 나이퀴스트는 '도로가 이상적이고 차 사이의 거리를 완벽히 유지할 때'의 이론 통행 능력을 계산하고, 샤논은 '비가 오거나 안개가 끼는 등 악천후(잡음)를 고려할 때'의 현실적 통행 능력을 계산합니다. 아무리 도로가 넓어도 폭우(잡음)가 쏟아지면 작은 승용차들만 겨우 분간하고 통과해야 하는 이치입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정

#### Scenario 1: 기가 인터넷(Gigabit Ethernet) 망 설계
*   **상황**: 1Gbps 전송망을 구축해야 하는데, 구리선(Cat 5e)의 주파수 대역폭($B$)이 100MHz로 제한됨.
*   **의사결정**: 나이퀴스트 공식에 의해 대역폭만으로는 1Gbps를 낼 수 없음($2 \times 100\text{MHz} = 200\text{Mbps}$ 한계). 따라서 5-Level PAM-5 등의 레벨 변조와 **4개의 페어(Twisted Pair)를 병렬로 사용**하여 하나당 250Mbps씩 4선로를 합산하는 방식(1000BASE-T)으로 한계를 극복함.
*   **결과**: 물리적 매체의 한계를 회선 묶기(Bonding)와 복잡한 변조 기법으로 해결.

#### Scenario 2: 유선 방송(HFC)의 상향/하향 속도 차이
*   **상황**: 케이블 인터넷은 다운로드(최대 수백 MHz)가 업로드(최대 수십 MHz)보다 훨씬 빠름.
*   **의사결정**: 나이퀴스트 공식 $C \propto B$에 따라, 할당된 대역폭 자체가 다운로드 쪽이 넓기 때문에, 복잡한 변조 없이도 압도적인 전송 용량 차이가 발생함. 네트워크 엔지니어는 트래픽 패턴(비대칭)에 맞춰 대역폭을 할당.

### 2. 도입 체크리스트

| 구