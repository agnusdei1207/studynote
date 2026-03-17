+++
title = "NW #28 충격 잡음 (Impulse Noise) 및 열 잡음 (Thermal Noise)"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #28 충격 잡음 (Impulse Noise) 및 열 잡음 (Thermal Noise)

> **핵심 인사이트**
> 1. **본질**: **열 잡음(Thermal Noise)**은 도체 내부 전자의 열운동으로 인한 불가피한 물리적 현상이며, **충격 잡음(Impulse Noise)**은 외부 기기나 자연 현상으로 발생하는 순간적이고 고진폭의 전기적 스파크(Spike) 현상이다.
> 2. **가치**: 두 잡음의 특성(지속성 vs 순간성)을 정확히 이해하여 **SNR (Signal-to-Noise Ratio)**을 개선하고, **버스트 에러(Burst Error)**를 **인터리빙(Interleaving)** 기술로 극복함으로써 5G/광통신과 같은 고속 디지털 통신의 신뢰성을 확보한다.
> 3. **융합**: 아날로그 신호 처리(증폭기/필터)와 디지털 신호 처리(FEC/인터리빙)가 융합되어 물리 계층(Layer 1)의 무결성을 보장하며, 상위 계층(TCP/IP)의 재전송 부하를 최소화한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
통신 시스템에서 잡음(Noise)은 신호의 전송 품질을 저하시키는 주요 요인이다. 이 중 **열 잡음(Thermal Noise)** 또는 **존슨-나이퀴스트 잡음(Johnson-Nyquist Noise)**은 저항이나 도체 내부의 전자들이 열에너지에 의해 무작위로 운동하면서 발생하는 기본적인 잡음으로, 절대 온도 0K가 아닌 이상 물리적으로 완전히 제거할 수 없는 **내부 잡음(Internal Noise)**이다. 반면, **충격 잡음(Impulse Noise)**은 번개, 전동기의 스위칭, 전력선 커플링 등 외부 환경적 요인에 의해 순간적으로 발생하는 고진폭의 비연속적 신호로, 주로 **외부 잡음(External Noise)**에 속한다.

#### 2. 등장 배경 및 비즈니스적 필요성
초기 전화망(Voice Analog) 시대에는 인간의 청각 특성상 잠시 발생하는 '틱' 소리가 큰 문제가 되지 않았다. 그러나 데이터 통신과 디지털 변조 방식(QAM, OFDM 등)이 발전하면서, 충격 잡음은 순간적으로 수백~수천 비트를 오염시켜 데이터 프레임 전체를 폐기하게 만드는 **치명적 결함(Fatal Flaw)**으로 부상했다. 이에 따라 물리 계층에서의 잡음 저감 설계와 데이터 링크 계층에서의 오류 제어(FEC, ARQ)가 필수적인 기술 과제가 되었다.

#### 3. 잡음의 시간-주파수 영역적 이해
열 잡음은 주파수 영역(Frequency Domain)에서 전 대역에 걸쳐 균일한 에너지 분포(백색 잡음, White Noise)를 가지며, 시간 영역(Time Domain)에서는 항상 존재하는 연속적인 바닥(Noise Floor)을 형성한다. 반면, 충격 잡음은 시간 영역에서 아주 짧은 폭(Duration)을 가지지만 진폭(Amplitude)이 매우 크고, 주파수 영역에서는 광대역 스펙트럼을 가진다.

**ASCII 다이어그램: 시간 영역에서의 두 잡음 비교**
```text
   Amplitude (Voltage)
      ^
      |        _._          (Impulse Noise)
      |       /   \        <--- High Amplitude, Short Duration
      |      /     \
      |  ___/       \___
      | |             |
      | |             |      (Thermal Noise)
  0V -+ ~~~~~~~~~~~~~~+~~~~~> <--- Continuous, Random, Low Amplitude
      | |             |
      | |             |
      |_|_____________|__________________> Time
        t1            t2

      * Thermal Noise: 무작위 요동(fluctuation)이 항상 존재
      * Impulse Noise: 특정 시점(t1)에서 급격한 Spike 발생
```

> 📢 **섹션 요약 비유**: 열 잡음은 '텅 빈 조용한 방에서도 들리는 공기의 미세한 흐름 소리'와 같아서 환기 시스템을 가동(통신 시스템 ON)하는 한 항상 존재하는 배경음(Sound Floor)입니다. 반면 충격 잡음은 '조용히 책을 보는데 갑자기 옆에서 풍선이 펑 터지는 소리'와 같아서, 발생 빈도는 낮지만 그 순간만큼은 모든 정보를 들리지 않게 만드는 폭음과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 열 잡음 (Thermal Noise)의 심층 원리
열 잡음은 도체 내的自由電子(Free Electrons)의 열운동(Thermal Agitation)에 기인한다. 이를 수학적으로 정의한 것이 **존슨-나이퀴스트 공식(Johnson-Nyquist Formula)**이다.

**핵심 공식 및 파라미터:**
$$ N = k \cdot T \cdot B $$

- **$N$ (Noise Power)**: 잡음 전력 (Watt, 단위: W)
- **$k$ (Boltzmann Constant)**: 볼츠만 상수 ($1.380649 \times 10^{-23} J/K$)
- **$T$ (Temperature)**: 절대 온도 (Kelvin, 단위: K), 상온(17℃)은 약 290K로 표준화
- **$B$ (Bandwidth)**: 시스템의 측정 대역폭 (Hertz, 단위: Hz)

**실무 적용:**
잡음 전력은 절대 온도($T$)와 대역폭($B$)에 비례한다. 따라서 고감도 수신 시스템(LNA 설계 등)에서는 $N$을 줄이기 위해 초저잡음 증폭기(LNA) 냉각 기술을 사용하거나, 필요 이상의 넓은 대역폭을 필터링(Filtering)하여 잡음 에너지 주입을 최소화한다. **SNR (Signal-to-Noise Ratio)**은 신호 전력 $S$를 잡음 전력 $N$으로 나눈 값($S/N$)으로, 통신 품질의 척도가 된다.

**ASCII 다이어그램: 열 잡음 발생 메커니즘 및 주파수 스펙트럼**
```text
      [Conductor Internal View]           [Frequency Domain Spectrum]
      +----------------------------+       Power Spectral Density (PSD)
      |  e-  e-    e-  e-    e-    |              ^
      |   \/  e-  \/   e-  \/      |              |
      |   /\    e- /\    e- /\     |              |   kT (Constant)
      |  /  \  e- /  \  e- /  \    |              |-----------------
      | /    \e-/    \e-/    \   e-|              |
      +----------------------------+              +------------------> Frequency
              (Random Thermal Motion)              0         B (Bandwidth)
      
      * 전자의 불규칙한 충돌이 미세한 전압 변동(V_n)을 유발
      * 주파수에 상관없이 일정한 전력 밀도(kT)를 가짐 => "White Noise"
```

#### 2. 충격 잡음 (Impulse Noise)의 파괴적 메커니즘
충격 잡음은 주로 **Switching Transient(스위칭 과도 현상)** 혹은 **ESD (Electro-Static Discharge)**에 의해 발생한다. 디지털 통신에서 이는 **Burst Error(버스트 에러)**라는 독특한 형태의 오류를 유발한다. 단일 비트 오류(Random Error)가 아니라, 연속된 비트 열(Bit Stream)이 한꺼번에 뒤집히는 현상이다.

**ASCII 다이어그램: 버스트 에러(Burst Error) 발생 과정**
```text
      [Time Line of Bit Transmission]
      Sync | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | Sync
           ^
           | (Normal Transmission)
      -------------------------------------------------
           ^
      ...  | <---[IMPULSE NOISE]---> | ...
           ^
           | (Corrupted Period)
      Sync | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | Sync
               ^^^^^^^^^^^^^^
               [Burst Error Length]
               
      * 잡음 지속 시간 동안 전송된 복수의 비트가 동시에 에러 발생
      * Hamming Distance 등 일반적인 FEC 코드로는 복구 불가능
```

#### 3. 대응 아키텍처: 인터리빙(Interleaving)
충격 잡음을 극복하기 위해 물리 계층에서 가장 널리 사용되는 기술이 **인터리빙(Interleaving)**이다. 이는 데이터의 순서를 섞어(Spread) 전송함으로써, 발생한 버스트 에러를 수신부에서 흩어진 랜덤 에러(Random Error)로 변환하여 **FEC (Forward Error Correction)** 코드가 수정할 수 있도록 돕는다.

> 📢 **섹션 요약 비유**: 열 잡음은 '화면에 끼어있는 항상 켜져 있는 정전기 노이즈'라면, 충격 잡음은 '순간적으로 카메라 플래시가 터져 화면이 온통 희게 변하는 것'과 같습니다. 이를 해결하기 위한 인터리빙은 '책의 페이지 순서를 뒤죽박죽 찍어서 보내는 것'과 같습니다. 만약 중간 페이지가 구멍이 나더라도(버스트 에러), 전체를 다시 조립하면 구멍이 곳곳에 흩어져 있어 내용을 유추하기(FEC 복구) 쉬워지는 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 잡음 특성 심층 비교 분석표

| 분석 기준 (Criteria) | 열 잡음 (Thermal Noise) | 충격 잡음 (Impulse Noise) |
|:---:|:---|:---|
| **물리적 기원 (Origin)** | **내부 요인**: 전자의 열운동 (Johnson-Nyquist Effect) | **외부 요인**: 기계 스위칭, 번개, 전기 스파크 |
| **시간적 특성 (Time Domain)** | **연속적 (Continuous)**: 시간축 상 항상 존재 | **과도적 (Transient)**: 수 $\mu s$~$ms$의 짧은 펄스 |
| **주파수적 특성 (Freq Domain)** | **백색 (White)**: 전 대역 균일 분포 | **광대역 (Wideband)**: 낮은 주파수부터 RF까지 스펙트럼 |
| **확률 분포 (Distribution)** | 가우시안 분포 (Gaussian Distribution) 따름 | 비가우시안 (Non-Gaussian), 중심 극한 정리 불적용 |
| **수학적 모델링** | $N = kTB$ (결정론적 예측 가능) | 무작위 과정(Stochastic Process), 예측 어려움 |
| **주요 영향 (Impact)** | **SNR 감소**: 신호의 명확성을 지속적으로 흐릿하게 만듦 | **Burst Error**: 데이터 블록 자체를 파괴하여 프레임 손실 유발 |
| **주요 대응 (Countermeasure)** | **냉각**, 저잡음 증폭기(LNA), 대역폭 제한 | **차폐(Shielding)**, 인터리빙(Interleaving), 필터링 |

#### 2. 기술 스택 융합 및 시너지/오버헤드
- **Layer 1 (Physical) vs Layer 2 (Data Link)**: 충격 잡음으로 인한 버스트 에러를 해결하기 위해 물리 계층에서 인터리빙을 적용하면, 신호를 수신하고 재배열(De-interleaving)해야 하므로 **지연 시간(Latency)**이 필연적으로 증가한다. 실시간성이 중요한 **VoIP나 IIoT(Industrial IoT)** 환경에서는 인터리빙 깊이(Interleaving Depth)를 낮추고 상위 프로토콜(TCP Retransmission)에 의존하는 등 트레이드오프(Trade-off) 설계가 필요하다.
- **전력 전자(Power Electronics)와의 융합**: 충격 잡음의 주요 원인인 인버터나 모터 구동부(Switching Power Supply)에 **EMI (Electromagnetic Interference)** 필터와 페라이트 코어(Ferrite Core)를 적용하여 전도성 노이즈를 사전에 차단함으로써 통신 품질을 확보한다.

> 📢 **섹션 요약 비유**: 열 잡음은 '비 오는 날의 안개'와 같아서 전체적으로 시계를 흐리게 하므로 전방탐지거리(SNR)를 늘리는 조명(신호 증폭)이 필요합니다. 반면 충격 잡음은 '앞차가 던진 돌멩이'와 같아서 순간적으로 앞유리(데이터 프레임)가 깨지는 사고를 내므로, 이를 방지하기 위해 안전장치(인터리빙)를 통해 충격을 분산시키는 설계가 필요합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 잡음 저감 설계 체크리스트 (Design Checklist)
| 구분 | 확인 항목 (Check Item) | 기술적 고려사항 (Technical Note) |
|:---:|:---|:---|
| **환경** | 설치 환경의 온도 및 전자파 환경 파악 | 고온 환경($T$ 증가) 시 열 잡음 전력 선형 증가 감안 |
| **케이블링** | 차폐선(STP/UTP) 및 접지(Grounding) 상태 | 충격 잡음 유입 경로 차단을 위해 피복 접지 저항 최소화 |
| **구성품** | LNA (Low Noise Amplifier) NF Figure | 열 잡음 지배 환경에서는 NF가 낮은(성능이 좋은) 증폭기 선택 필수 |
| **디지털 신호처리** | 인터리빙 Depth 설정 | 버스트 길이에 맞춰 Depth 최적화 (지연 시간 vs 오류 복구력 트레이드오프) |

#### 2. 실무 시나리오 및 의사결정 (Scenario)

**[시나리오 A] 공장 자동화(Factory Automation) 시스템의 통신 장애**
- **상황**: 대형 전동기가 기동할 때마다 무선 패킷 손실이 급증함.
- **분석**: 전동기의 스위칭 노이즈(충격 잡음)에 의해