+++
title = "NW #21 샤논의 채널 용량 (Shannon Capacity) - 잡음 채널"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #21 샤논의 채널 용량 (Shannon Capacity) - 잡음 채널

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 샤논-하틀리 정리는 정보 이론(Information Theory)의 핵심으로, **대역폭(Bandwidth)**과 **신호 대 잡음비(SNR, Signal-to-Noise Ratio)**라는 두 가지 물리적 한계가 결합된 채널의 이론적 최대 전송 속도를 정의한다.
> 2. **가치**: **C (Channel Capacity)**는 오류 없는(Error-free) 통신이 가능한 절대적인 상한선으로, 어떤 **FEC (Forward Error Correction)** 기술도 이 한계를 초과하여 정보를 전송할 수 없음을 수학적으로 증명한다.
> 3. **융합**: **MIMO (Multiple-Input Multiple-Output)** 및 **OFDM (Orthogonal Frequency Division Multiplexing)** 등 현대 무선 통신 기술의 효율성을 평가하고, 5G/6G 스펙트럼 효율 목표를 설정하는 물리 계층(Physical Layer)의 기준이 된다.

---

### Ⅰ. 개요 (Context & Background)

**정의 및 철학**
1948년 클로드 샤논(Claude Shannon)이 발표한 "통신의 수학적 이론"에서 정의한 샤논의 채널 용량은, **잡음(Noise)**이 존재하는 통신 채널에서 **오류 확률(Error Probability)을 0으로 수렴시키면서 전송할 수 있는 최대 정보 전송률**을 의미한다. 이는 단순한 속도의 제한을 넘어, 디지털 통신 시스템이 신뢰성을 보장하기 위해 달성해야 할 이상적인 목표지점을 설정한다. 이 이론은 **AWGN (Additive White Gaussian Noise, 가산성 백색 가우시안 잡음)** 모델을 기반으로 하며, 통신 시스템 설계 시 "어떻게 하면 더 빠르게"가 아니라 "어떻게 하면 더 신뢰하게"라는 근본적인 질문에 대한 해답을 제공한다.

**💡 비유**
도로의 차선 수가 넓고 도로 위 짐을 나르는 트럭(신호)과 오토바이(잡음)가 섞여 있다고 가정할 때, 도로 관리자가 "아무리 사고가 나지 않게 운전해도 시간당 통과할 수 있는 차량의 수는 이것이다"라고 정해놓은 물리적 법칙과 같다.

**등장 배경**
1. **기존 한계**: 초기 통신에서는 잡음으로 인한 오류를 줄이기 위해 단순히 신호의 세기를 높이거나 반복 전송하는 방식에 의존했으나, 효율성에는 명확한 한계가 존재했다.
2. **혁신적 패러다임**: 샤논은 '정보'를 수학적으로 정량화(Entropy)하여, 대역폭과 전력을 어떻게 배분해야 한정된 자원 안에서 최대의 정보를 전달할 수 있는지를 증명했다.
3. **현재의 비즈니스 요구**: 5G/6G 시대로 넘어가며 스펙트럼 자원의 희소성이 대두됨에 따라, 한정된 주파수 자원(B) 내에서 샤논 한계에 근접하는 기술(극한의 효율화)이 필수적인 생존 전략이 되었다.

**📢 섹션 요약 비유**
샤논 용량은 '카페가 시끄러울 때(잡음), 옆자리 친구의 말을 얼마나 정확하고 빠르게 알아들을 수 있는지'를 결정짓는 자연의 물리 법칙과 같습니다. 아무고토 없이 크게 소리치면(SNR 증가) 듣기 쉽지만, 물리적으로 내 성대(전력)에는 한계가 있기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 샤논-하틀리 공식 (Shannon-Hartley Theorem)**
이론의 핵심은 다음 공식으로 요약된다.

$$C = B \cdot \log_{2}(1 + \text{SNR})$$

여기서 $C$는 **Channel Capacity (bps)**, $B$는 **Bandwidth (Hz)**, $\text{SNR}$은 신호 전력 대 잡음 전력의 비($\frac{S}{N}$, 선형 스케일)이다. 이 공식은 **로그(Logarithm)** 함수의 특성을 통해 전력 증가에 따른 수확 체감(Diminishing Returns)을 설명한다.

**2. 구성 요소 및 상관관계 분석**

| 구성 요소 (Component) | 약어 (Abbreviation) | 역할 (Role) | 내부 동작 및 특성 (Behavior) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **채널 용량** | Capacity (C) | 이론적 최대 전송 속도 | 오류율 0에 수렴하는 상한선. bps 단위 | 파이프를 통해 통과할 수 있는 최대 물량 |
| **대역폭** | Bandwidth (B) | 주파수 자원의 폭 | $C$에 **선형적(Linear)**으로 영향. $B$가 2배면 $C$도 2배. | 도로의 차선 수 (차선이 늘어나면 통과 차량도 늘어남) |
| **신호 전력** | Signal Power (S) | 정보를 전달하는 에너지 | 송신기의 출력. 높일수록 SNR 증가하지만 간섭 유발. | 내 목소리 크기 |
| **잡음 전력** | Noise Power (N) | 채널의 열잡음/간섭 | AWGN 등으로 모델링. $N$이 감소해야 $C$가 크게 증가. | 카페 내의 배경 소음 |
| **신호 대 잡음비** | SNR (Signal-to-Noise Ratio) | 통신 품질의 척도 | 주로 **dB (Decibel)**로 표현. $C$에는 **로그(Log)** 함수로 영향. | 목소리와 소음의 크기 비율 |

**3. ASCII 다이어그램: 대역폭 vs SNR의 기여도**

```ascii
[ Shannon Capacity Characteristics ]

   Capacity (C)
     ^
     |       / S/N High (Power Limited)
     |      /   <--- Logarithmic Growth (Slow)
     |     /
     |    /      Log Scale (B)
     |   /_______
     |  /
     | /  Bandwidth Dominated (Linear Growth)
     |/__________________________________> Input Resource
      (Increase B)          (Increase S/N)

    ① Increasing B (Bandwidth) --> Linear capacity increase
    ② Increasing S/N (Power)   --> Logarithmic capacity increase
    => Strategy: Expanding B is more efficient than boosting Power(S).
```

**해설**
위 다이어그램은 샤논 공식에서 대역폭($B$)과 신호 대 잡음비($S/N$)의 증가가 채널 용량($C$)에 미치는 영향력의 차이를 시각화한 것이다.
- **Bandwidth ($B$)**: 그래프 우측처럼 자원을 투입하면 용량이 **선형적(1:1 비례)**으로 증가한다. 따라서 통신 시스템 설계 시 주파수 대역을 넓히는 것이 가장 효과적이다.
- **SNR ($S/N$)**: 그래프 좌측 상단처럼 로그 함수의 꼴을 가진다. 초기에는 전력을 높이면 효과가 크지만, 일정 수준 이상부터는 수평에 가까워지며 수확 체감이 발생한다. 즉, 전력만으로는 한계가 있다는 것을 의미한다.

**4. 심층 동작 원리: 오류 정정의 개입**
샤논의 정리는 "용량 $C$ 이하로 전송하면, 충분히 복잡한 부호화(Coding) 기술을 통해 오류 확률을 0으로 만들 수 있다"는 역설적인 증명을 포함한다. 이는 **FEC (Forward Error Correction)** 코드 블록 길이가 무한히 길어질 때 달성 가능하다. 반대로 $C$를 초과하여 전송을 시도하면, 아무리 훌륭한 코드를 써도 오류는 필연적으로 발생한다.

**5. 핵심 계산 로직 (Code Snippet)**

```python
# Shannon Capacity Calculator
import math

def calculate_shannon_capacity(bandwidth_hz, snr_db):
    """
    샤논 용량 계산 함수
    :param bandwidth_hz: 대역폭 (Hz)
    :param snr_db: 신호 대 잡음비 (dB, Decibel)
    :return: 채널 용량 (bps)
    """
    # 1. 변환: dB(dB) -> Linear Scale (Ratio)
    # 공식: SNR(linear) = 10^(SNR(dB) / 10)
    snr_linear = 10 ** (snr_db / 10.0)

    # 2. 계산: C = B * log2(1 + SNR)
    # math.log(x, 2)는 밑이 2인 로그 계산
    capacity_bps = bandwidth_hz * math.log(1 + snr_linear, 2)

    return capacity_bps

# Example: 전화선 (V.92 모뎀 기준)
# B = 3500 Hz, SNR = 35 dB (양호한 회선)
print(f"{calculate_shannon_capacity(3500, 35) / 1000:.2f} kbps")
# Result: ~40.9 kbps (이론적 최대치)
```

**📢 섹션 요약 비유**
마치 복잡한 고속도로 톨게이트에서 하이패스 차선(고속 패스)을 별도로 운영하여 병목을 해결하는 것과 같습니다. 대역폭을 늘리는 것은 차선 자체를 늘리는 것(직관적이고 효과적)과 같고, SNR을 높이는 것은 차량 성능을 업그레이드하는 것(비싸고 효과는 체감됨)과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

이 섹션에서는 샤논 공식이 실제 물리 계층 기술들과 어떻게 상호작용하는지, 그리고 한계를 극복하기 위한 현대적인 접근 방식을 분석한다.

**1. 기술 스펙트럼별 샤논 한계 달성률 분석**

| 기술 분류 | 대표 기술명 | 샤논 한계와의 거리 (Gap) | 특징 및 시사점 |
|:---:|:---|:---|:---|
| **레거시 코딩** | Convolutional Code | ~3~5 dB Gap | 구현이 간단하나 샤논 한계에서 멀음. 효율 낮음. |
| **근접 코딩** | **Turbo Code**, **LDPC (Low-Density Parity-Check)** | ~0.1~1 dB Gap | LTE, 5G, Wi-Fi 등 현대 통신에 사용됨. **Shannon Limit**에 근접. |
| **용장 코딩** | **Polar Code** | ~0.5 dB Gap (특정 조건) | 5G **eMBB (Enhanced Mobile Broadband)** 제어 채널로 채택됨. |

**2. 다이버시티(Diversity) 기술을 통한 용량 극복**
단일 안테나 시스템에서는 전력 증가(SNR 향상)에 한계가 있으므로, 공간적 자원을 활용하여 샤논 공식의 형태를 변형한다.

$$C_{\text{MIMO}} = \min(N_t, N_r) \cdot B \cdot \log_{2}(1 + \text{SNR})$$

- $N_t$: 송신 안테나 수
- $N_r$: 수신 안테나 수
- **시사점**: 안테나를 추가하여 **Spatial Multiplexing (공간 다중화)**을 수행하면, 대역폭($B$)을 늘리지 않아도 채널 용량($C$)을 안테나 수에 비례하여 선형적으로 증대시킬 수 있다.

**3. ASCII 다이어그램: 코딩 이득(Coding Gain) 시각화**

```ascii
[ Shannon Limit and Coding Performance ]

     BER (Bit Error Rate)
     ^
 0.1|    [No Coding]  <-- 전력을 많이 써야 BER 확보
     |       /
     |      /
 10^-3|----/----------- [Turbo/LDPC Code] (Same BER with Less Power)
     |   /   ^--- Coding Gain (Approx 5-10dB)
     |  /
     | /
 10^-6|________________________ [Shannon Limit]
     |  <--- Theoretical Wall
     +-------------------------------------> Eb/N0 (Energy per bit to Noise power spectral density)
                (Required Signal Quality)
```

**해설**
- **No Coding (무코딩)**: 오류율(BER)을 낮추기 위해서는 $E_b/N_0$ (신호 품질)을 비약적으로 높여야 한다.
- **Channel Coding (코딩 적용)**: **Turbo Code**나 **LDPC**와 같은 오류 정정 부호를 사용하면, 동일한 오류율을 유지하기 위해 필요한 신호 품질($E_b/N_0$)이 훨씬 낮아진다. 이를 **Coding Gain**이라 하며, 결과적으로 같은 전력으로 더 높은 용량($C$)을 낼 수 있거나, 같은 용량을 전력을 아껴서 달성할 수 있게 한다.
- **Shannon Limit**: 점선은 이론적으로 도달할 수 없는 벽이다. 5G/6G 기술들은 이 벽에 바짝 붙어서 달리는 자동차와 같다.

**과목 융합 관점**
- **네트워킹 & 프로토콜**: 상위 계층인 **TCP (Transmission Control Protocol)**의 혼잡 제어(Congestion Control)는 이러한 물리적 한계($C$)를 초과하여 데이터를 보내지 않도록 전송율(Rate)을 조절한다.
- **신호 처리(Signal Processing)**: **FFT (Fast Fourier Transform)**를 이용한 OFDM은 주파수 선택적 페이딩(Fading)을 평탄화하여 유효 SNR을 최적화함으로써 전체 채널 용량을 극대화하는 기법이다.

**📢 섹션 요약 비유**
샤논 한계가 '100점 만점' 시험이라면, 과거의 통신 기술은 80점대에 머물렀으나, **Turbo Code**와 **LDPC** 같은 최신 오류 정정 기술은 '학습 법'을 개선하여 99.9점(샤논 한계 근접)까지 성적을 올린 천재들과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 과정**

| 시나리오 | 문제 상황 (Problem) | 샤논 공식 기반 분석 (Analysis) | 기술적 결정 (Decis