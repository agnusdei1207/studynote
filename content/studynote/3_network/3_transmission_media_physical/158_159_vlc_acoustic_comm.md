+++
title = "158-159. 이색(異色) 통신 매체: 가시광 통신과 음향 통신"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 158
+++

# 158-159. 이색(異色) 통신 매체: 가시광 통신과 음향 통신

> ### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전자기파(RF)의 물리적 한계(간섭, 수중 감쇠)를 극복하기 위해 광대역 가시광선과 수중 음파를 매체로 활용하는 **PHY (Physical Layer) 계층의 대안 기술**.
> 2. **가치**: 병원/항공기 등 RF 제한 구역에서의 **EMC (Electromagnetic Compatibility)** 확보 및 수중 환경에서의 장거리 연결성 제공.
> 3. **융합**: LED 조명 인프라와의 융합(IoT) 및 해양 센서 네트워크, 로봇 공학 등 특수 목적 통신의 핵심 인프라.

---

### Ⅰ. 개요 (Context & Background)

**통신 매체의 패러다임 전환**: 현대 사회의 무선 통신은 주로 RF (Radio Frequency) 대역에 의존하지만, 주파수 자원의 고갈, 전자파 간섭(EMI), 그리고 매질의 물리적 특성(물, 금속 구조물)으로 인해 데이터 전송이 불가능한 영역이 존재합니다. 이를 해결하기 위해 **'빛'**과 **'소리'**라는 고전적인 물리 현상을 첨단 디지털 변조 기술과 결합한 **이색 통신 매체 (Heterogeneous Communication Media)**가 주목받고 있습니다.

**💡 비유**: 
무선랜(Wi-Fi)이 보이지 않는 '공기 중의 소음'을 이용해 대화한다면, 가시광 통신은 '등대의 불빛'을, 수중 통신은 '물속의 울림'을 이용해 대화하는 것과 같습니다.

**등장 배경**:
1. **스펙트럼 위기 (Spectrum Crisis)**: RF 주파수 자원의 포화 상태로 인한 새로운 대역(Big Bandwidth) 확보 필요성 대두.
2. **EMI 간섭 회피**: 의료기기(수술실), 항공기, 발전소 등 전자기파 간섭이 치명적인 환경에서의 무선 데이터 수요 증가.
3. **수중 탐사의 확대**: 해양 자원 개발, 해저 케이블 감시, 무인 잠수정(AUV) 제어를 위한 수중 데이터 망 구축의 어려움(RF의 수중 감쇠).

📢 **섹션 요약 비유**: 
마치 복잡하고 시끄러운 시장( RF 혼잡 구간 )에서는 말보다는 불빛이나 수신호로 의사를 소통하고, 소리가 안 들리는 물속에서는 물을 타고 울리는 몸짓으로 대화하듯, 환경에 맞는 매체를 선택하는 전략입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 RF 대체 기술인 **VLC (Visible Light Communication)**와 **수중 음향 통신 (Underwater Acoustic Communication)**의 내부 동작 메커니즘과 물리 계층 아키텍처를 심층 분석합니다.

#### 1. 구성 요소 상세 비교

| 구성 요소 | VLC (가시광 통신) | Underwater Acoustic (음향 통신) |
|:---|:---|:---|
| **송신기 (Tx)** | **LED (Light Emitting Diode)** 또는 Laser Diode. 전류의 ON/OFF 속도로 빛을 깜빡여 데이터를 실음. | **Transducer (Projector)**. 전기 신호를 진동판(피에조 소자)의 물리적 운동으로 변환하여 음압(SPL) 발생. |
| **매질 (Medium)** | 공기 중의 가시광선 대역 (380~750nm THz 대역). 자유 공간 경로 손실(LOS) 따름. | 해수/담수. 밀도가 높아 음파 전파가 잘 됨(약 1,500m/s), 온도/염분에 따라 굴절률 변화. |
| **변조 방식** | **OOK (On-Off Keying)**, VPPM, OFDM. 빛의 세기(Intensity)를 제어. | **FSK (Frequency Shift Keying)**, PSK. 주파수나 위상을 변조하여 다중 경로 페이딩 극복. |
| **수신기 (Rx)** | **PD (Photodiode)** 또는 Image Sensor (CAM). 빛의 세기 변화를 전류로 검출. | **Hydrophone**. 수중의 미세한 압력 변화(음파)를 전기 신호로 복원. |
| **주요 프로토콜** | **IEEE 802.15.7** (LR-WPAN), Li-Fi Alliance 규격. | **WHOI Micro-Modem**, JANUS (NATO 표준). |

#### 2. VLC (Visible Light Communication) 동작 메커니즘

**A. 조도 통신 (Intensity Modulation)**
데이터는 빛의 파장이 아닌 **광도(Luminous Intensity)**의 세기로 코딩됩니다. LED는 1초에 수천만 번 점멸할 수 있으며, 이를 인간의 눈은 인지하지 못하지만 포토다이오드는 고속 디지털 신호로 인식합니다.

**B. 양방향 통신의 한계와 해결책 (Full-Duplex Challenge)**
* **다운링크**: 조명 → 스마트폰 (광신호 수신).
* **업링크**: 스마트폰 → 조명 (IR 적외선 LED 사용 또는 RF 백홀 사용).
*   → 빛을 역으로 쏘아 올리는 것은 전력 소모와 기기 발열 문제로 인해 일반적으로 **Infrared (적외선)**을 별도로 사용하거나 비대칭 통신으로 설계합니다.

```ascii
[ VLC Downlink Data Flow ]

[ Data Source ]
      | (Binary Data)
      v
[ Driver IC ] --- (Current) ---> [ LED Array ]
                                    |
                                    | (Light Intensity Modulation)
                                    | ON  = Logic 1
                                    | OFF = Logic 0
                                    v
                              < Air Medium > (LOS required)
                                    |
                                    v
[ Smart Device ]
[ Front Cam ] --> [ Photo Sensor ] --> [ ADC ] --> [ Demodulator ] --> [ Data ]
    (Rolling Shutter Effect 사용 시 2차원 바코드 인식 가능)
```

**다이어그램 해설**:
1. **Driver IC**는 네트워크 계층(L3)에서 내려온 패킷을 PHY 계층의 비트 스트림으로 변환하여 LED의 전류를 제어합니다.
2. **Light Intensity Modulation** 과정에서는 인간의 깜빡임 인지 융합(Flicker Fusion Threshold) 한계(약 60Hz 이상)를 훨씬 상회하는 MHz 급 주파수를 사용하여 눈부심 없이 데이터를 실어 보냅니다.
3. **수신부**에서는 Rolling Shutter 방식의 CMOS 센서를 이용해 노출 라인 주사(Sampling)를 통해 고속 광신호를 저속 주파수 패턴으로 변환하여 복원하는 기술도 활용됩니다.

#### 3. 수중 음향 통신 (Underwater Acoustic)의 심층 원리

**A. 물리적 속도와 지연 (Latency)**
음파의 수중 전파 속도는 약 $c = 1,500$ m/s입니다. RF의 빛의 속도($3 \times 10^8$ m/s)에 비해 약 20만 배 느립니다. 이는 프로토콜 설계 시 **Huge Propagation Delay**로 작용하여, 육상용 TCP/IP 프로토콜을 그대로 사용할 수 없게 만듭니다(Timeout 문제 발생).

**B. 다중 경로 (Multipath) 페이딩**
수면 반사, 해저 반사, 수층 굴절 등으로 인해 신호가 여러 경로를 통해 도착하여 심각한 간섭(Inter-Symbol Interference)을 유발합니다.

```ascii
[ Underwater Acoustic Channel Model ]

  (Ship/Buoy)        AUV / Sensor
      ^                   ^
      | (Uplink)          | (Downlink)
      |                   |
  [ Hydrophone ]      [ Transducer ]
      ^                   ^
      | <--- Signal ------>|
      |                   |
  ~~~~~~~ Water Surface (Reflection) ~~~~~~~
   |   |  ^        ^     |   |
   |   |  | \      |     |   |
   |   |  |  \     |     |   |
   |   |  |   \    |     |   |
   |   |  |    \   |     |   | <--- Multipath Effect
   |   |  |     \  |     |   |
   |   |  |      \ |     |   |
  ~~~~~~~~~~~ Sea Bed (Reflection) ~~~~~~~~~~

  Path 1: Direct Path (Shortest, Fastest)
  Path 2: Surface Reflection (Phase Shift)
  Path 3: Bottom Reflection (High Attenuation)
```

**다이어그램 해설**:
수중 음향 채널은 직접파(Direct Path)뿐만 아니라 표면과 해저에서 반사된 신호들이 수신기에 서로 다른 시간에 도착하며 겹치는 **심각한 다중 경로 문제**를 가집니다. 이를 해결하기 위해 **Rake Receiver**나 **Equalizer** 등의 복잡한 신호 처리 기법이 요구되며, 이는 수신기의 전력 소모를 크게 증가시키는 주요 요인이 됩니다.

📢 **섹션 요약 비유**: 
가시광 통신은 고속도로에서 질주하는 스포츠카처럼 '넓은 대역폭'으로 엄청난 양의 데이터를 나르지만, 터널(장애물)을 만나면 끊깁니다. 반면 수중 음향 통신은 울퉁불퉁한 산길을 천천히 걸어가는 도보 여행자처럼 데이터는 조금 실어 나르지만, 어두운 바닷속이라는 극한 환경을 견디며 멀리까지 이동할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

본 섹션에서는 두 기술의 정량적 지표를 비교하고, 타 IT 기술과의 융합 관점을 분석합니다.

#### 1. 정량적/정성적 기술 비교 매트릭스

| 구분 | **VLC / Li-Fi** | **RF (Wi-Fi, 5G)** | **Underwater Acoustic** |
|:---|:---:|:---:|:---:|
| **전송 매체** | 가시광 (380~750nm) | 전자기파 (Sub-6 / mmWave) | 음파 (Acoustic Wave) |
| **대역폭** | **극히 넓음 (THz 급)** | 넓음 (MHz ~ GHz) | **매우 좁음 (kHz 급)** |
| **전송 속도** | **초고속** (최대数十 Gbps 이론치) | 고속 (Mbps ~ Gbps) | **저속** (bps ~ kbps) |
| **전파 지연** | 무시할 수 있음 (ns) | 매우 낮음 (µs~ms) | **매우 큼** (초 단위 Latency) |
| **커버리지** | 실내 단거리 (LOS 필수, 약 10m) | 광역 (수백 m ~ 수 km) | 장거리 (수 km ~ 수십 km) |
| **주요 장애 요인**| 차광, 벽 투과 불가 | 전파 간섭, 누수 보안 | 잡음, 다중 경로, 도플러 효과 |
| **보안성** | **뛰어남** (공간 격리 용이) | 낮음 (투과되어 유출됨) | 높음 (물이라는 물리적 장벽) |
| **전력 효율** | 조명과 병행 시 효율 높음 | 기본 전력 소모 높음 | 송신 시 고전력 필요 |

#### 2. 과목 융합 분석

**A. 보안 (Security)과의 융합: Quantum-Safe Channel**
*   **RF 공통 취약점**: Wi-Fi는 벽을 뚫고 나가기 때문에 외부 해커의 무선 도청(Wardriving)이 가능합니다.
*   **VLC의 시사점**: 빛은 방 안에 갇히기 때문에 **'방 밖으로는 아예 신호가 존재하지 않는다'**는 물리적 보안(Physical Layer Security)을 제공합니다. 이는 기밀성이 중요한 국방/금융 시설에서 IDF(Internet Data Firewall) 역할을 수행할 수 있습니다.

**B. 전력/배터리 (Power)와의 융합: Energy Harvesting**
*   수중 센서 노드는 배터리 교체가 어렵습니다. Acoustic 통신은 송신 전력이 높아 에너지 효율이 좋지 않습니다.
*   반면, VLC 수신기(PD)는 약한 빛 에너지를 수집하여 **에너지 하베스팅(Energy Harvesting)**을 병행, 저전력 IoT 센서를 영구적으로 구동할 수 있는 시너지가 있습니다.

```ascii
[ Comparison: Bandwidth vs Distance ]

^
|
|   * Wi-Fi (High BW, Mid Range)
|          *
|
|                * VLC (Very High BW, Short Range)
|                       *
|
|                                              * Acoustic (Very Low BW, Long Range)
|
+----------------------------------------------------> Distance
```

📢 **섹션 요약 비유**: 
VLC는 사람이 많은 번화가(데이터) 내부에서 엘리베이터(광 채널)를 타고 빠르게 이동하는 셈이지만, 엘리베이터가 없는 곳은 못 갑니다. 음향 통신은 남극이나 깊은 산속(수중)에서 철저한 훈련을 받고 엄청난 체력을 써서(고전력) 느리게 도보로 이동하는 특수부대와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실제 현장에서 이 기술들을 도입할 때 고려해야 할 전략적 의사결정 프로세스를 다룹니다.

#### 1. 실무 시나리오별 의사결정 가이드

**Scenario A: 스마트 팩토리의 로봇 팔 제어 (RF 간섭 우심)**
*   **상황**: 용접 로봇 다수가 가동되어 스파크(EMI 노이즈)가 심한 환경. 유선은 로봇의 움직임을 제한함.
*   **의사결정**: RF(Wi-Fi)는 간섭으로 패킷 손실이 발생해 제어 지연이 생길 수 있음. **VLC(Li-Fi)** 도입 검토.
*   **이유**: 높은 대역폭으로 실시간 HD 영상 전송 가능 + 광원(LED 조명) 기반으로 전력 효율 우수.
*   **판단**: 단, 로�