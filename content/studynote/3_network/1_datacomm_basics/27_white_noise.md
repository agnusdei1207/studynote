+++
title = "NW #27 백색 잡음 (White Noise) 및 가우스 잡음"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #27 백색 잡음 (White Noise) 및 가우스 잡음

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 백색 잡음(White Noise)은 광대역 주파수 영역에서 균일한 전력 밀도를 가지며, 통신 채널의 내부 열 운동에 기인한 가산적(Additive) 간섭 신호이다.
> 2. **가치**: 이 모델링은 **AWGN (Additive White Gaussian Noise)** 채널을 통해 **SNR (Signal-to-Noise Ratio)**에 따른 이론적 전송 속도 한계인 **샤논 한계(Shannon Limit)**를 정의하는 절대적 척도가 된다.
> 3. **융합**: **무선 통신(Wireless Communication)**과 **오류 정정 부호(Error Correction Code)** 설계의 기반이 되며, **RF (Radio Frequency)** 회로 설계 시 노이즈 피겨(Noise Figure) 산정의 핵심 기준이다.

---

### Ⅰ. 개요 (Context & Background)

**백색 잡음(White Noise)**이란 '가시광선 스펙트럼에서 모든 파장이 섞여 백색을 이루는 현상'에 비유하여, 물리적으로 **모든 주파수 성분에 걸쳐 전력 스펙트럼 밀도(PSD, Power Spectral Density)가 균일한 확률 과정(Stochastic Process)**을 의미한다.

**💡 비유**:
백색 잡음은 마치 빨간색, 파란색, 초록색 등 모든 색의 빛이 뒤섞여 투명한 흰빛을 만들어내는 것과 같습니다. 마치 흰빛이 특정 색을 구별하지 않고 모두를 포함하듯, 백색 잡음은 특정 주파수(음역)를 골라내지 않고 전체 대역에 두루 걸쳐 존재하는 '전자기적 빗방울'과 같습니다.

**등장 배경**:
① **기존 한계**: 초기 통신 시스템은 단순한 신호 감쇠만을 고려했으나, 전자의 자발적인 움직임인 열 잡음(Thermal Noise)과 우주 방사선 등에 의한 비선형 왜곡이 식별됨.
② **혁신적 패러다임**: 1940년대 노리베트 위너(Norbert Wiener)와 클로드 섀넌(Claude Shannon)은 잡음을 '확률적 랜덤 변수'로 모델링하여, 정보 전송 능력을 수학적으로 정량화하는 정보 이론을 정립함.
③ **현재의 비즈니스 요구**: 5G/6G 및 고주파 **밀리미터파(Millimeter Wave)** 통신 환경으로 진입하며, 대역폭 확장에 따른 잡음 전력 증가가 시스템 성능을 좌우하는 핵심 변수로 부상함.

📢 **섹션 요약 비유**:
백색 잡음의 개념은 마치 "비가 올 때 빗방울의 크기가 고르게 내리는 장마철"과 같습니다. 어디에든(모든 주파수) 고르게 떨어지며(균일한 전력 밀도), 누군가가 의도한 것이 아니라 자연적으로 발생하는(열적 무작위성) 배경 현상이기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

통신 시스템 이론에서 잡음은 **AWGN (Additive White Gaussian Noise)** 모델로 표준화되어 분석된다. 이는 신호 처리 및 링크 버짓(Link Budget) 산정의 가장 기초가 되는 수학적 모델이다.

#### 1. AWGN 모델의 구성 요소 (3대 속성)

| 속성 (Element) | 전체 명칭 (Full Name) | 기술적 정의 (Definition) | 수학적/물리적 특성 |
|:---:|:---|:---|:---|
| **A** | **Additive (가산성)** | 수신 신호 $r(t)$에 잡음 $n(t)$가 더해지는 형태 | $r(t) = s(t) + n(t)$ (선형 중첩 원리) |
| **W** | **White (백색성)** | 주파수 영역에서 전력 스펙트럼 밀도가 상수(constant) | $S_n(f) = \frac{N_0}{2}$ (DC ~ 무한대 주파수까지 평탄) |
| **G** | **Gaussian (가우시안)** | 시간 영역에서 표본 분포가 정규 분포를 따름 | 중심 극한 정리(CLT)에 의해 자연 발생하는 잡음은 통계적으로 정규분포 수렴 |

#### 2. AWGN 채널 모델링 및 시스템 구조

아래 다이어그램은 송신된 신호가 채널을 거쳐 수신기에 도달하기까지 잡음이 섞이는 물리적 계층 구조를 도식화한 것이다.

```ascii
      [ Transmitter ]             [ Channel (Medium) ]              [ Receiver ]
      (Signal Source)              (Air / Fiber / Copper)           (Demodulator)
           |                              |                              |
           |  s(t)                        |                              |
           |  (Clean Signal)              |  n(t) (AWGN Source)          |
           |----------+                   |          ^                   |
           |          |                   |          |                   v
           |          v                   |          |           [  LNA  ]      r(t) = s(t) + n(t)
                      \                  |          /            (Low Noise    ----------> [ ADC ]
                       \                 |         /              Amplifier)        |
                        \                |        /                                 v
                         +----( Adder )---+-------+                         [ DSP / Decoder ]
                                            |                                         |
                                            v                                         v
                                      Thermal Noise                               Bit Stream
                                    (Johnson-Nyquist)                           (Data Recovery)
```

**(다이어그램 해설)**
1. **신호원(Source)**: 순수한 정보 신호 $s(t)$가 생성됨.
2. **채널(Channel) & 가산기(Adder)**: 전송 매체(공기, 동선 등) 내부에서 자연적으로 발생하거나 외부에서 유입된 잡음 $n(t)$가 신호 $s(t)$에 선형적으로 더해짐. 이 과정이 **Additive**의 핵심임.
3. **수신기 Front-end**: 수신 안테나로 들어온 $r(t) = s(t) + n(t)$는 먼저 **LNA (Low Noise Amplifier, 저잡음 증폭기)**를 거침. 이 과정에서 신호를 증폭함과 동시에 LNA 자체의 내부 잡음도 추가됨.
4. **DSP (Digital Signal Processing)**: **ADC (Analog-to-Digital Converter)**를 거쳐 디지털화된 신호는 복조 및 **FEC (Forward Error Correction, 순방향 오류 수정)** 알고리즘을 통해 잡음으로 인한 오류를 정정함.

#### 3. 심층 동작 원리: 열 잡음(Thermal Noise) 발생 메커니즘

모든 도체 내부의 자유 전자는 온도가 0K(절대 온도)가 아닌 이상, 무작위적인 열 운동(Thermal Agitation)을 한다. 이 불규칙한 움직임이 전압의 미세한 요동(Fluctuation)으로 나타나는 것이 **존슨-나이퀴스트 잡음(Johnson-Nyquist Noise)**이며, AWGN의 주요 물리적 원인이다.

- **잡음 전력 공식 (Thermal Noise Power)**:
  $$ N = k \cdot T \cdot B $$
  - $N$: 잡음 전력 (Watt)
  - $k$: **볼츠만 상수 (Boltzmann Constant)** ($1.38 \times 10^{-23} J/K$)
  - $T$: 절대 온도 (Kelvin). 상온($17^{\circ}C$) 약 290K 기준 사용.
  - $B$: 시스템 대역폭 (Hz). **대역폭이 넓을수록 잡음 전력은 선형적으로 증가함.**

#### 4. 핵심 알고리즘 및 코드: AWGN 발생 시뮬레이션 (Python/NumPy)

시뮬레이션에서는 "상자형 잡음(Box-Muller Transform)"을 이용해 균등 분포를 가우시안 분포로 변환하여 AWGN을 생성한다.

```python
import numpy as np

def generate_awgn(signal, snr_db):
    """
    신호에 AWGN을 추가하는 함수
    :param signal: 원본 신호 배열 (복소수 또는 실수)
    :param snr_db: 목표 SNR (dB)
    :return: 잡음이 섞인 신호 (Noisy Signal)
    """
    # 1. 신호 전력 계산 (Energy Calculation)
    sig_avg_watts = np.mean(signal ** 2)
    
    # 2. 목표 SNR에 따른 잡음 전력 계산
    # SNR(dB) = 10 * log10(Signal_Power / Noise_Power)
    # Noise_Power = Signal_Power / 10^(SNR/10)
    snr_linear = 10 ** (snr_db / 10.0)
    noise_avg_watts = sig_avg_watts / snr_linear
    
    # 3. 표준 편차(Standard Deviation) 산출
    # Gaussian Noise는 표준 편차 sigma에 비례하여 크기 결정
    noise_std_dev = np.sqrt(noise_avg_watts)
    
    # 4. 가우시안 분포(정규분포) 난수 생성 (0 평균, sigma 표준편차)
    noise = np.random.normal(0, noise_std_dev, len(signal))
    
    return signal + noise
```

📢 **섹션 요약 비유**:
AWGN 모델의 작동은 마치 "고속도로에서 라디오 주파수에 들어오는 '치지직' 하는 백색 소음"과 같습니다. 목소리(신호)가 아무리 또렷해도, 자동차 엔진 소리나 타이어 소음(열 잡음)이 섞여 들리기 때문에, 우리는 소음을 걸러내거나(LNA 최적화), 목소리를 더 크게 해야(SNR 개선) 상대방에게 의미를 전달할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

잡음은 단순히 성능을 저하시키는 요소가 아니라, 시스템 설계 시 **타협점(Trade-off)**을 결정하는 중요한 지표이다.

#### 1. 심층 기술 비교: 잡음 유형 및 특성 분석

| 구분 (Comparison) | 백색 잡음 (White Noise) | 유색 잡음 (Colored Noise) | 임펄스 잡음 (Impulse Noise) |
|:---|:---|:---|:---|
| **정의 (Definition)** | 모든 주파수에서 균일한 PSD | 특정 주파수 대역 편중됨 | 짧고 강한 스파이크(Spike) 형태 |
| **PSD 형태** | 플랫(Flat) / 상수 $N_0/2$ | 주파수에 따라 변동 ($1/f$ 등) | 불규칙한 폭발적 파형 |
| **대표 원인** | **열 잡음 (Thermal Noise)** | 회로 권선, 기계적 진동 | 번개, 스위칭 서지, 전기 점화 |
| **대응 방식** | 대역폭 제한, LNA 최적화 | **이퀄라이저(Equalizer)** | **Interleaver**, 클리핑(Clipping) |
| **주요 영역** | AWGN 채널 이론, 유선/무선 기본 | 전원 라인, 아날로그 회로 | 전력선 통신(PLC), 산업용 센서 |

#### 2. 과목 융합 관점: 정보 통신과 신호 처리의 상관관계

① **정보 통신 이론 (Information Theory)과의 융합**:
- **샤논 채널 용량 공식 (Shannon-Hartley Theorem)**: 잡음이 채널 용량 $C$를 어떻게 제한하는지 수학적으로 규명함.
  $$ C = B \cdot \log_2 \left( 1 + \frac{S}{N} \right) $$
  여기서 $N$이 바로 잡음 전력이다. **신호 대 잡음비 (SNR)**이 1일 때(0dB)보다 10dB 높을 때 전송 용량이 급격히 증가함.
- **변조 방식(Modulation)과의 관계**: **QAM (Quadrature Amplitude Modulation)**과 같은 고차 변조는 잡음에 매우 민감하다. 잡음이 조금만 늘어나도 **Constellation Diagram(성상도)** 위의 점들이 겹쳐져 오류가 발생하므로, Adaptive Modulation(적응형 변조) 기술을 통해 잡음 수준에 따라 변조 차수를 낮추는 전략이 필수적임.

② **디지털 신호 처리 (DSP) 및 임베디드 시스템과의 시너지**:
- **ADC (Analog-to-Digital Converter)** 분해능과 잡음: **SQNR (Signal-to-Quantization-Noise Ratio)** 관점에서 양자화 잡음(Quantization Noise) 또한 백색 잡음으로 모델링되어 시스템 성능을 예측하는 데 사용됨.
- **오버샘플링 (Oversampling)**: ADC의 샘플링 레이트를 높여 양자화 잡음을 넓은 주파수 대역으로 펼쳐놓고, 필터링하여 유효 **ENOB (Effective Number of Bits)**를 높이는 기술은 잡음의 성질을 이용한 대표적인 우회 전략임.

📢 **섹션 요약 비유**:
잡음과 통신 시스템의 관계는 마치 "교실 수업과 소음의 관계"와 같습니다. 선생님(송신자)이 목소리를 크게 하거나(신호 전력 증폭), 혹은 아주 작은 목소리라도 마이크(증폭기)를 사용하면 되지만, 교실의 문을 활짝 열어놓는 것(대역폭 증가)은 밖의 소음까지 더 불러오기 때문에 신호를 더 정교하게(오류 정정) 보내야만 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 통신 엔지니어는 잡음을 제거하는 것이 불가능함을 인지하고, 잡음 환경에서 최적의 성능을 내도록 시스템을 **최적화(Optimization)**해야 한다.

#### 1. 실무 시나리오 및 의사결정 매트릭스

| 시나리오 (Scenario) | 문제 상황 (Problem) | 의사결정 로직 (Decision Logic) | 기술적 대응 (Solution) |
|:---|:---|:---|:---|
| **위성 통신 수신기 설계** | 약한 신호 수신, 우주 공기 냉각 불가 | 수신기 앞단의 잡음 지수(NF)를 낮추는 것이 최우선 | **LNA (Low Noise Amplifier)** 채용, $G/T$ (Gain over Noise Temperature) 최적화 |
| **고속 SerDes