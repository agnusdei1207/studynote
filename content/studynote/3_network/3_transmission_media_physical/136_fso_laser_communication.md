+++
title = "136. 자유 공간 광통신 (FSO, Free Space Optics)"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 136
+++

# 136. 자유 공간 광통신 (FSO, Free Space Optics)

### # 자유 공간 광통신 (FSO, Free Space Optics)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 유리 매질(광섬유) 없이 대기나 진공이라는 '자유 공간'을 통해 레이저 빔을 송수신하여 데이터를 전송하는 광무선 통신(Optical Wireless Communication)의 일종.
> 2. **가치**: **RF (Radio Frequency)** 대역의 주파수 혼잡과 허가 문제를 해결하며, 광섬유 설치가 불가능한 지역에서 **1Gbps~10Gbps**급의 초고속 대역폭을 저비용으로 제공하는 "무선 광케이블" 역할.
> 3. **융합**: 5G/6G 백홀(Backhaul), 위성 간 링크(**ISL, Inter-Satellite Link**), 보안이 필요한 군사 통신망 등 물리적 매개물 설치가 곤란한 **Last-Mile** 접속 기술로 필수적.

---

### Ⅰ. 개요 (Context & Background)

**자유 공간 광통신(FSO, Free Space Optics)**은 광섬유(Optical Fiber)라는 물리적 전송로를 대체하여, 레이저 빔을 자유 공간(대기, 진공)을 통해 직접 전송 매체로 활용하는 통신 기술입니다. 기본적으로 빛의 직진성을 이용하며, 송신기와 수신기 간의 **LOS (Line-of-Sight)** 가 필수적입니다.

FSO는 기술적으로는 광섬유 통신의 광원(Laser)과 변조 방식을 그대로 사용하면서도, 전송 매질을 유리에서 공기로 변경한 하이브리드 형태입니다. 따라서 광대역의 장점은 그대로 계승하면서도, 설치의 유연성(무선)을 확보한 기술입니다.

#### 💡 개념 비유
이는 "수도관(광케이블)을 땅속에 묻지 않고, 강력한 물대포(레이저)를 쏘아 다음 건물의 물통(수신기)에 물을 공급하는 것"과 같습니다. 관을 묻을 필요 없이 즉시 물을 공급할 수 있지만, 바람(대기 난류)이 불거나 안개(산란)가 끼면 물이 제대로 닿지 않을 수 있습니다.

#### 등장 배경 및 필요성
1.  **기존 유선망의 한계**: 도심 지역의 굴착 공사(Civil Engineering) 비용 상승 및 도로 점용 허가의 어려움으로 인한 **FTTH (Fiber to the Home)** 및 건물 간 **LAN (Local Area Network)** 연결의 애로사항.
2.  **무선 주파수의 고갈**: **RF (Radio Frequency)** 기반의 **MW (Microwave)** 통신은 가용 주파수 대역이 포화 상태이며, 고주파수(밀리미터파)로 갈수록 전파 손실이 큼.
3.  **광대역 수요의 폭증**: 4K/8K 스트리밍 및 클라우드 서비스 확산으로 인해, 기존 **Wi-Fi**나 **LTE** 망에서 처리하기 힘든 기가비트급 급증 트래픽 처리 필요성 대두.

#### 📢 섹션 요약 비유
마치 복잡한 도로의 교차로(유선망 포화 상태)를 피하기 위해 하늘로 비행길(빛의 경로)을 새로 뚫어 비행기(데이터)를 빠르게 운항하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

FSO 시스템은 단순히 레이저 포인터를 쏘는 것이 아니라, 고도의 정렬과 변조, 오류 제어가 필요한 정밀 광학 시스템입니다.

#### 1. 핵심 구성 요소 (Component Analysis)

| 구성 요소 (Component) | 상세 기능 (Role) | 내부 동작 및 기술 사양 (Operation) | 관련 프로토콜/기술 | 비유 (Analogy) |
| :--- | :--- | :--- | :--- | :--- |
| **광송신기 (Optical Transmitter)** | 전기 신호를 광신호로 변환 | **LD (Laser Diode)** 또는 **LED** 사용. 직접 변조(Direct Modulation) 방식으로 데이터를 On/Keying. 주로 780nm~1550nm 대역 사용. | OOK (On-Off Keying), PWM | 송신 타워의 라이트 하우스 |
| **광수신기 (Optical Receiver)** | 광신호를 전기 신호로 복원 | **APD (Avalanche Photodiode)** 사용. 미약한 광신호를 증폭(Avalanche Effect)하여 전류로 변환. 고감도가 필수적임. | TTL 신호 복원, CDR | 빛을 모으는 거대한 접시 |
| **망원경 렌즈 시스템 (Telescope Optics)** | 빔의 Collimation 및 Focusing | 송신부는 빛을 평행하게 만들고(Collimation), 수신부는 모으는 렌즈 역할. **NA (Numerical Aperture)** 조정으로 수광 효율 최적화. | 광학 설계 (Optics) | 빛을 줄기로 만드는 렌즈 |
| **ATC (Auto Tracking Control)** | 빔의 경로 오차 수정 | 건물 흔들림이나 열적 현상으로 인한 **Beam Wander(빔 표류)**를 감지하고, 마이크로 액추에이터로 거울을 조절해 정렬 유지. | PID Control, Quadrant Detector | 흔들리는 바다 위의 자이로스코프 |
| **대기 보상기 (Atmospheric Compensator)** | 날씨/대기 난류 완화 | 안개나 비로 인한 감쇠(Attenuation)를 보상하기 위해 출력을 자동으로 높이거나, 오류 정정 부호 강화. | AGC (Auto Gain Control) | 어두워지면 밝기를 높이는 센서 등 |

#### 2. 시스템 아키텍처 및 데이터 흐름

FSO 통신은 물리 계층(Layer 1)에서 빛을 **진폭(Shifting)** 하여 데이터를 전송합니다. 가장 널리 쓰이는 방식은 **OOK (On-Off Keying)**입니다.

```ascii
      [Sender Side]                                     [Receiver Side]
+------------------+      Laser Beam (Light)     +------------------+
|  Data Source     |                            |  Data Sink       |
| (Switch/Server)  |                            | (Switch/Server)  |
+--------+---------+                            +--------+---------+
         |                                               |
         v                                               v
+------------------+                            +------------------+
|  Encoder & Mod   |   (1) Parallel Beam      |  Photo Detector  |
| (ECC / Scramble) |   ====================>  | (APD / PIN Diode) |
+--------+---------+   Space / Air Medium     +--------+---------+
         |                ^                            ^
         |                | (2) Scintillation          |
         v                v                            v
+------------------+   +------------------+   +------------------+
|   Tx Optics      |   | Atmos Channel    |   |   Rx Optics      |
| (Lens/LD Driver) |   | (Rain/Fog/Turb.) |   | (Filter/Lens)    |
+------------------+   +------------------+   +------------------+

    [Data Flow Description]
    ① Electrical Signal (Digital 0/1)
      ↓
    ② Laser Diode Driver (Current to Light Conversion)
      ↓
    ③ Beam Expander (Reducing Divergence Angle)
      ↓
    ④ Free Space Channel (Add Noise: Scintillation, Attenuation)
      ↓
    ⑤ Rx Lens (Collect Photons)
      ↓
    ⑥ APD (Photon to Electron, High Sensitivity)
      ↓
    ⑦ Signal Processing (CDR, Error Correction)
```

**다이어그램 해설**:
1.  **송신부(Tx)**: 네트워크 스위치로부터 온 1010 디지털 신호는 **LD Driver**를 거쳐 레이저 다이오드의 강한 빛 깜빡임으로 변환됩니다. 이때 단순히 직진성만 가지면 공기 중에서 쇠퇴(Attenuation)가 심하므로, **Beam Expander**를 통해 빔의 직경을 넓혀 발산각(Divergence Angle)을 줄입니다. (마치 손전등을 비출 때 렌즈를 통해 쨍하게 멀리 비추는 원리입니다)
2.  **전송 채널(Channel)**: 빛은 대기라는 매질을 통과합니다. 이 과정에서 **안개(Mie Scattering)**나 **비, 눈**, 그리고 대기 난류(공기의 굴절률 변화)로 인한 **Shimmer(심리터)** 현상이 발생하여 신호가 왜곡되거나 세기가 변할 수 있습니다.
3.  **수신부(Rx)**: 수신 렌즈는 넓은 범위에서 흩어진 빛을 모아 **APD (Avalanche Photodiode)**로 집중시킵니다. APD는 수광된 빛 광자(Photon)를 전자로 증폭하는 캐스케이드 효과를 통해, 미약한 신호라도 검출해냅니다. 이후 **CDR (Clock and Data Recovery)** 회로가 노이즈를 걸러내고 원래의 디지털 신호를 복원합니다.

#### 3. 핵심 이론 및 수식 (Optical Link Budget)

FSO의 링크 설계는 **Link Budget Equation**에 의해 지배됩니다. 수신된 전력 $P_r$은 다음과 같이 계산됩니다.

$$ P_r = P_t \times \left( \frac{D_r}{D_t + \theta L} \right)^2 \times T_{atm} \times T_{sys} $$

*   $P_t$: 송신 전력 (Transmit Power)
*   $D_r$: 수신 렌즈 직경 (Receiver Aperture Diameter)
*   $D_t$: 송신 렌즈 직경
*   $\theta$: 빔 발산각 (Beam Divergence, mrad)
*   $L$: 전송 거리 (Range)
*   $T_{atm}$: 대기 투과율 (Atmospheric Transmission, 날씨에 따라 변동)

**실무적 판단**: 거리 $L$이 멀어질수록 신호는 제곱비로 약해지므로, 빔의 발산각 $\theta$을 수 밀리라디안(mrad) 이하로 줄이는 광학 설계가 관건입니다.

#### 📢 섹션 요약 비유
마치 요격하는 미사일이 레이저 유도 장비를 통해 표적의 미세한 움직임까지 실시간 보정하며 날아가는 것과 같습니다. 초음속으로 날아가는 미사일(데이터)이 바람(대기 난류) 밀리지 않으려면 끊임없이 궤도를 수정(ATC)하는 정밀 시스템이 필요합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

FSO는 다른 무선 통신 기술과 비교할 때 명확한 위치를 가집니다.

#### 1. 기술 심층 비교 (FSO vs. RF Microwave)

| 비교 항목 (Criteria) | **FSO (Free Space Optics)** | **RF Microwave (60-80GHz)** | **광섬유 (Fiber Optic)** |
|:---|:---|:---|:---|
| **전송 매체** | 빛 (Infrared Laser) | 전파 (Millimeter Wave) | 유리 (Glass Core) |
| **주파수 대역** | ~200THz (가시광선 근접) | ~60GHz (V-band, W-band) | ~200THz |
| **대역폭(Bandwidth)** | **초고속** (10Gbps~100Gbps) | 중고속 (1Gbps~10Gbps) | **최고속** (Tbps급) |
| **면허/인가 (License)** | **무면허 (License-free)** | 일부 국가에서 면허 필요 | 매설권 필요 |
| **보안성 (Security)** | **최상** (빔 좁음, 가시선 필요) | 중간 (전파 누설 가능) | 최상 (물리적 절연) |
| **취약 요인** | **날씨** (안개, 강우) | **강우** (Rain Fade), 간섭 | **물리적 절단** |
| **설치 난이도** | 쉬움 (사용자 설치 가능) | 중간 (안테na 정렬 필요) | 어려움 (굴착 공사) |

#### 2. 대기 날씨에 따른 가용률 분석 (Availability Analysis)

실무에서 FSO 도입 시 가장 중요한 지표는 **Availability(가용률)**입니다. 날씨에 따른 빛의 산란 정도는 파장에 따라 다릅니다.

```ascii
    [Atmospheric Attenuation vs. Wavelength]

    Attenuation (dB/km)
      ^
  100 |  ████  (Heavy Fog - Mie Scattering)
      |  ████  --> Short wave (850nm) suffers massively
      |
   10 |  ████  (Rain - Geometric Scattering)
      |  ████
      |
    1 |  ████  (Clear Weather)
      |  ████
      |_________________________________________> Wavelength (nm)
          850nm (Tx)          1550nm (Tx)

    Key Insight: 
    - 안개 입자의 크기와 파장이 비슷하면 산란이 극대화됩니다.
    - 따라서 1550nm 대역(Long Wave)을 사용하면 안개에 대한 내성이 850nm 대역보다 훨씬 높습니다.
```

#### 3. 타 과목 융합 관점
*   **네트워크 (OSI 7 Layer)**: FSO는 **OSI 7 Layer**의 물리 계층(Physical Layer, L1)에 속합니다. 즉, 상위 계층(TCP/IP)에서는 FSO인지 광케이블인지 구분하지 못하며, 단순히 케이블이 연결된 것으로 인식합니다.
*   **보안 (Security)**: FSO는 **Jamming(재밍)** 공격에 매우 취약합니다. 송신광원보다 더 강한 레이저 빔을 수신부로 쏘면 센서가 포화(Saturation)되어 통신이 마비될 수 있습니다. 이를 방지하기 위한 **Optical Filter(광학 필터)** 설계가 중요합니다.

#### 📢 섹션 요약 비유
마치 철도(광섬유)는 비가 와도 멈추지 않지만 부지가 필요하고, 비행기(RF)는 부지가 필요 없지만 악천후나 항공 교통에 민감한 것과 같습니다. FSO는 하늘을 나는 '고속 열차'와 같아서, 부지는 필요 없고(무선) 비행기보다 빠르지만(광속급), 갑자기 안개가 끼면 비행