+++
title = "167-170. 페이딩(Fading)과 다이버시티(Diversity) 기술"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 167
+++

# 167-170. 페이딩(Fading)과 다이버시티(Diversity) 기술

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 무선 채널의 **다중 경로(Multipath)** 현상과 **도플러 효과(Doppler Effect)**로 인해 발생하는 신호의 왜곡과 감쇠 현상인 **페이딩(Fading)**은 통신 품질 저하의 근본 원인이다.
> 2. **가치**: 페이딩으로 인한 **SNR (Signal-to-Noise Ratio)** 저하는 전송 속도 저하와 단절을 유발하며, 이를 극복하기 위한 **다이버시티(Diversity)** 기술은 5G/6G 시대의 쓰루풋(Throughput)을 보장하는 핵심 기술이다.
> 3. **융합**: 물리 계층(Physical Layer)의 전파 특성을 이해하고, 안테나 공학(안테나 배열)과 신호 처리(DSP, 필터 설계) 기술이 결합되어 안정적인 무선 링크를 구축한다.

---

### Ⅰ. 개요 (Context & Background) - 무선 환경의 불확실성

**개념**
**페이딩(Fading)**은 무선 통신 환경에서 송신기와 수신기 사이의 전파(Path)가 지형, 지물, 기상 조건 등의 외부 요인에 의해 시시각각 변화하여, 수신 신호의 진폭(Amplitude)과 위상(Phase)이 급격히 변동하는 현상을 말한다. 단순히 거리에 따른 신호 감쇠를 넘어, "거의 비슷한 시간과 위치에서도 신호 세기가 요동치는" 불안정성을 의미한다.

**💡 비유**
페이딩은 마치 **'수영장의 물결'**과 같다. 수영장 한가운데 서 있어도 주변의 사람들이 만드는 파동이 합쳐져 내 몸이 순간적으로 위로 솟구치기도 하고 가라앉기도 한다. 물의 높이(신호 세기)가 내가 움직이지 않아도 주변 환경에 의해 요동치는 것이다.

**등장 배경**
① **기존 한계**: 초기 무선 통신은 단일 안테나와 단일 주파수를 사용하여, 건물이나 산에 의해 신호가 막히거나(Shadows), 반사파 간의 상쇄 간섭으로 통신이 끊기는 문제가 있었다.
② **혁신적 패러다임**: 전파가 여러 경로로 도달한다는 다중 경로(Multipath) 자체를 비현실적인 현상이 아닌, 에너지 분산의 원인으로 분석하고 이를 **'통계적 확률 모델(레일리 페이딩, 라이스 페이딩)'**로 정량화하여 극복하려는 시도가 시작되었다.
③ **현재의 비즈니스 요구**: 이동 통신(Mobility) 환경에서 고속 데이터(5G, 자율주차)를 안정적으로 제공하기 위해 페이딩 예측 및 보상 기술이 필수적인 생존 문제가 되었다.

**📢 섹션 요약 비유**
무선 통신의 페이딩 현상을 이해하는 것은, **'울퉁불퉁한 비포장 도로에서 스포츠카를 몰 때 발생하는 진동과 충격'**을 분석하는 것과 같습니다. 도로 상태(채널 환경)에 따라 차량(신호)이 덜컹거리는 정도를 예측하고, 서스펜션(다이버시티)으로 이를 흡수하는 것이 핵심입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 페이딩의 상세 분류 및 물리적 메커니즘

페이딩은 신호 변동의 거리 스케일에 따라 **대규모 페이딩(Large-scale Fading)**과 **소규모 페이딩(Small-scale Fading)**으로 철저히 분류된다.

| 구분 요소 | 대규모 페이딩 (Large-scale) | 소규모 페이딩 (Small-scale) |
|:---|:---|:---|
| **물리적 원인** | 거리 증가, 대규모 지형지물(산, 빌딩) | 반사/회절/산란에 의한 다중 경로(Multipath) |
| **변동 주기** | 완만함 (Slow Fading) | 급격함 (Fast Fading) |
| **주요 모델** | Path Loss Model, Log-normal Shadowing | Rayleigh Fading, Ricean Fading |
| **영향 거리** | 수십 ~ 수백 미터 | 파장($\lambda$) 수십 분의 수준 (cm 단위) |

#### 2. 소규모 페이딩의 심화: 다중 경로와 도플러

소규모 페이딩은 **무선 채널의 임펄스 응답(Impulse Response)**이 시간에 따라 변화함으로써 발생한다. 핵심은 **도플러 주파수 천이(Doppler Shift)**와 **지연 확산(Delay Spread)**이다.

**가. 다중 경로 페이딩 (Multipath Fading)**
전파가 직접파(LOS, Line-of-Sight)뿐만 아니라 여러 반사체를 거쳐 수신안테나에 도달한다. 이때 각 경로의 길이가 다르므로 도착 시간이 상이하고, 위상이 합쳐져 ** constructive(보강)** 또는 **destructive(상쇄)** 간섭을 일으킨다.

*   **Flat Fading (Frequency Flat Fading)**: 전송 대역폭보다 채널의 **Coherence Bandwidth (상관 대역폭)**이 넓은 경우. 대역폭 전체가 동일하게 페이딩됨. (저속 전송 시 발생)
*   **Frequency Selective Fading (주파수 선택적 페이딩)**: 신호 대역폭이 상관 대역폭보다 넓은 경우. 특정 주파수 성분만 깊게 페이딩되어 신호가 왜곡됨. (고속 전송 시 치명적, **ISI(Inter-Symbol Interference)** 유발)

**나. 도플러 효과 (Doppler Effect)**
단말기가 이동 속도 $v$로 움직일 때, 전파의 수신 주파수 $f_d$만큼 천이되는 현상이다.
$$ f_d = \frac{v}{c} f_c \cos\theta $$
(여기서 $c$는 광속, $f_c$는 반송파 주파수, $\theta$는 이동 방향과 입사각)

이로 인해 채널이 시간에 따라 급격히 변하는 **Time-Selective Fading**이 발생한다.

#### 3. 페이딩 채널의 다이어그램 및 해설

아래는 다중 경로 환경에서 신호가 합성되는 현상을 도식화한 것이다.

```ascii
[Multipath Fading Channel Visualization]

   송신기(Tx)
      |
      |------------------ (Path 1: LOS, 강함)
      |                     /  <-- 신호 세기: +10dB
      |                    /   
      v                   v
   [수신기(Rx)] <--------+ (신호 합성점)
      ^                 ^
      |                 |  
      |---- (Path 2: Reflected, 늦음, 위상 반전)
      |      <-- 신호 세기: +9dB, Delay: 1us
      |
      |---- (Path 3: Reflected, 늦음)
             <-- 신호 세기: +6dB, Delay: 5us
      [결과] Phase 1과 2가 반대 위상이면 상쇄 -> Fading Hole (구멍) 발생
```

**다이어그램 해설**:
송신기에서 보낸 하나의 신호는 공간상의 여러 장애물에 부딪혀 경로(Path)가 분리된다. 수신기 입장에서는 '직진한 신호'와 '벽에 튕겨 늦게 온 신호'를 동시에 받게 된다. 만약 늦게 도착한 신호의 위상이 180도(반전)라면 직진 신호와 상쇄되어 신호가 0에 가까워지는 **Deep Fading(깊은 페이딩)**이 발생한다. 이 현상은 주파수 영역에서 특정 주파수만 구멍이 뚫리는 형태로 나타나며, **ISI (Inter-Symbol Interference, 심볼 간 간섭)**의 주원인이 된다.

#### 4. 핵심 공식 및 코드
**Mathematical Model (Rayleigh Fading)**
직접파가 없는 순수 반사 환경(NLOS)에서는 수신 신호의 포락선(Envelope)이 **레일리 분포**를 따른다.
$$ p(r) = \frac{r}{\sigma^2} e^{-r^2 / 2\sigma^2} \quad (r \ge 0) $$
반면, 직접파가 존재하면(LOS) **라이스 분포(Rician Distribution)**를 따르며, 이때 $K$-factor(Direct power / Multipath power)가 중요한 지표가 된다.

**Pseudo Code: Channel Power Estimation**
```python
# Python-style pseudo code for estimating Fading margin
def calculate_fading_margin(tx_power, path_loss_exp, distance, shadowing_std):
    """
    Calculate received power considering Large-scale fading
    """
    # Path Loss Model: PL(d) = PL(d0) + 10*n*log10(d/d0)
    mean_path_loss = 20 + 10 * path_loss_exp * math.log10(distance / 1.0) # d0=1m
    
    # Shadowing (Log-normal)
    shadowing_fading = random.gauss(0, shadowing_std)
    
    # Total Large-scale Fading Loss
    rx_power = tx_power - mean_path_loss - shadowing_fading
    
    return rx_power

# If rx_power < Sensitivity, Outage occurs.
```

**📢 섹션 요약 비유**
다중 경로 페이딩과 주파수 선택적 페이딩의 관계는 **'오케스트라 단원들이 각자 다른 시점에 연주하여 울리는 음향'**과 같습니다. 전체 주파수(모든 악기)가 아닌, 특정 악기(특정 주파수)의 소리가 홀에서 울림이 심해 못 들리는 현상이 주파수 선택적 페이딩입니다. 이를 해결하려면 시간차를 두고 보내거나(Time Diversity), 채널을 나눠서(OFDM) 보내야 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 페이딩 극복 기술 심층 비교

페이딩이라는 불확실성을 제거하기 위해 **다이버시티(Diversity, 분산)**와 **이퀄라이제이션(Equalization, 등화)** 기술이 사용된다.

| 기술 | 공간 다이버시티 (Space) | 주파수 다이버시티 (Frequency) | 시간 다이버시티 (Time) | 이퀄라이저 (Equalizer) |
|:---|:---|:---|:---|:---|
| **메커니즘** | 여러 안테나로 독립적 경로 확보 | **FHSS**, OFDM 등 다른 주파수 전송 | **Channel Coding**, Interleaving | 채널 역필터로 신호 왜곡 복원 |
| **대표 기술** | **MIMO**, Beamforming | OFDM Subcarriers | 재전송(ARQ), 인터리빙 | ZF, MMSE, MLSE |
| **핵심 지표** | 안테나 간격 > $\lambda/2$ | **Coherence Bandwidth** | Coherence Time | **Delay Spread** |
| **오버헤드** | 하드웨어(안테나, RF 체인) 증가 | 대역폭 효율 저하 가능성 | 지연 시간(Latency) 증가 | 연산 복잡도(COMPLEX) 극대화 |

*   **약어 정리**:
    *   **MIMO (Multiple-Input Multiple-Output)**: 다중 안테나를 사용한 송수신 기술.
    *   **FHSS (Frequency-Hopping Spread Spectrum)**: 주파수를 옮겨 다니며 통신하는 기술 (Bluetooth 등).
    *   **OFDM (Orthogonal Frequency Division Multiplexing)**: 직교하는 다수의 부반송파를 사용하는 방식 (4G LTE, Wi-Fi 표준).
    *   **ZF (Zero-Forcing)**: 간섭을 강제로 0으로 만드는 선형 등화 알고리즘.
    *   **MMSE (Minimum Mean Square Error)**: 잡음을 고려하여 오차 제곱 평균을 최소화하는 알고리즘.

#### 2. 과목 융합 관점

1.  **물리 계층 & 신호 처리 (DSP)**: 페이딩 채널을 보상하는 이퀄라이저는 **LMS (Least Mean Square)**나 **RLS (Recursive Least Squares)** 같은 적응형 필터(Adaptive Filter) 알고리즘을 사용한다. 이는 신호 처리 과목의 핵심 응용 분야다.
2.  **네트워크 성능 (QoS)**: 페이딩이 심한 환경에서는 **BER (Bit Error Rate)**이 급증하여, 상위 계층(TCP)에서 **吞吐量(Throughput)**이 급락하고 혼잡 제어(Congestion Control)가 잘못 작동할 수 있다. 따라서 MAC 계층에서 AMC (Adaptive Modulation and Coding) 기술을 통해 변조 방식(QPSK $\leftrightarrow$ 64QAM)을 동적으로 변경해야 한다.

#### 3. 다이버시티 이득 도식화

```ascii
[Diversity Gain Comparison]

Probability(Pe < Threshold) ^       (Log-Log Scale)
                                   |
      No Diversity ----------------|---------- * (Steep slope, Fading deep)
                                   |
      Diversity Order 2 (M=2) -----|------- *   (Less probability of deep fade)
                                   |
      Diversity Order 4 (M=4) -----|---- *       (Highly Reliable)
                                   |
      +----------------------------------------> SNR (dB)
        [해설] 다이버시티 차수(Order)가 높을수록 기울기가 가팔라져,
        낮은 신호 대 잡음비에서도 안정적인 통신이 가능해짐을 보여줌.
```

**📢 섹션 요약 비유**
페이딩 극복 기술들은 **'투자의 분산'** 전략과 유사합니다. 공간 다이버시티는 **'여러 증권사에 계좌를 분산하여 개장'**하는 것이고, 주파수 다이버시티는 **'여러 종목에 분산 투자'**하는 것이며, 이퀄라이저는 **'손실을 복구하는 헷지(Hedging) 기술'**과 같습니다. 하나의 경로가 망해도 전체 시스템은 무너지지 않습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision