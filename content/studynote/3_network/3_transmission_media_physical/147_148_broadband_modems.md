+++
title = "147-148. 초고속 인터넷 액세스= 케이블 모뎀과 xDSL"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 147
+++

# 147-148. 초고속 인터넷 액세스: 케이블 모뎀과 xDSL

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존의 아날로그 전화망(PSTN)과 CATV 망이라는 '레거시 구리선 인프라'를 교체 없이 디지털화하여 광대역(broadband)을 구현하는 **액세스 기술(AC, Access Circuit)의 집합**.
> 2. **가치**: 광케이블 매설 비용이 투입되지 않은 초기 인터넷 보급의 핵심이 되었으며, xDSL은 **전용 대역(Dedicated)**, 케이블 모뎀은 **공유 대역(Shared)**의 특징으로 서비스 품질(QoS)과 비용 효율성의 상충 관계를 보여줌.
> 3. **융합**: 물리 계층(Physical Layer)의 변조 기술(QAM)과 주파수 분할 다중화(FDM) 원리를 응용하며, 최근에는 광동작(FTTx)과 결합한 **하이브리드 접속망(HFC, FTTC)** 형태로 진화하여 FTTH(광랜)로 넘어가는 과도기적 기술로 정착함.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 기술적 배경 및 철학
초고속 인터넷의 초창기는 모든 가정에 광케이블(Optical Fiber)을 새로 깔는 것은 막대한 비용이 소요되는 비현실적인 선택지였습니다. 따라서 전 세계적으로 이미 포설되어 있는 **구리선(Copper Wire) 인프라**, 즉 전화용의 **UTP (Unshielded Twisted Pair)** 케이블과 TV 방송용의 **동축 케이블(Coaxial Cable)**을 활용하여 고속 디지털 데이터를 전송하는 기술이 개발되었습니다.

이들의 핵심 철학은 **'대역폭의 재발견'**입니다. 인간의 가청 주파수(음성)는 4kHz 미만, 아날로그 TV 방송 주파수도 수백 MHz 대역의 일부만 사용합니다. xDSL과 케이블 모뎀은 이 기존 서비스가 사용하지 않는 **'남는 고주파 대역(Idle High-frequency Band)'**을 데이터 통신용으로 빌려 쓰는 **FDM (Frequency Division Multiplexing, 주파수 분할 다중화)** 기술입니다.

#### 2. 등장 배경: 다이얼업의 한계
1990년대 다이얼업 모뎀(V.90 등)이 제공하는 56kbps 속도로는 웹 그래픽, 음악 스트리밍을 감당할 수 없었습니다. 이를 해결하기 위해 전화교환국에서 가정까지의 구간을 디지털화하여 음성(4kHz)과 데이터(25kHz~1.1MHz)를 물리적으로 분리하는 **xDSL (Digital Subscriber Line)** 기술이, 그리고 CATV 방송망을 양방향 통신망으로 변환하는 **케이블 모뎀** 기술이 각각 등장했습니다.

#### 3. 💡 개념 비유
전화선과 케이블 선을 '도로'라고 칩시다. xDSL과 케이블 모뎀은 도로를 넓히지 않고도, 사람(음성/영상)이 다니는 저층 공간 위에 비행기 데이터선이 지나가는 고층 공간(고주파)을 인공적으로 만들어 교통 체증을 해결한 것과 같습니다.

> **📢 섹션 요약 비유**: 마치 좁은 시골 도로(구리선) 위에 고가 도로(고주파 대역)를 추가로 건설하여, 기존 차량(음성/TV)은 아래로, 새로운 스포츠카(인터넷 데이터)는 위로 지나가게 하여 도로를 확장 없이 용량을 획기적으로 늘린 기술입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

본 섹션에서는 xDSL 계열의 대표 기술인 ADSL/VDSL과 케이블 인터넷의 구체적인 동작 원리와 아키텍처를 분석합니다.

#### 1. xDSL (Digital Subscriber Line)의 세부 기술
xDSL은 전화국(CO, Central Office)의 **DSLAM (Digital Subscriber Line Access Multiplexer)**과 가정의 **모뎀** 간의 구리선 회로에서 데이터를 송수신합니다. 가장 널리 쓰인 ADSL과 VDSL의 주파수 대역 배치와 변조 방식은 다음과 같습니다.

##### [표] xDSL 기술 비교 분석
| 구분 | ADSL (Asymmetric DSL) | VDSL (Very high-bit-rate DSL) | VDSL2 (G.vector 포함) |
|:---|:---|:---|:---|
| **다운로드 속도** | 최대 8 Mbps (ADSL2+는 24Mbps) | 최대 52 Mbps ~ 100 Mbps | 최대 200 Mbps ~ 1Gbps |
| **업로드 속도** | 최대 1 Mbps | 최대 2 Mbps ~ 6 Mbps | 최대 100 Mbps |
| **사용 거리** | 약 4.5km ~ 5.5km (감쇠 심함) | 약 300m ~ 1.4km (거리 민감) | 약 250m ~ 1km |
| **주파수 대역** | 25kHz ~ 1.1MHz | 0.138MHz ~ 12MHz | 0.138MHz ~ 30MHz (이론상 100MHz) |
| **변조 방식** | DMT (Discrete Multi-Tone) | DMT / QAM | DMT |
| **특징** | 음성(4kHz)과 공존, 거리에 따라 속도 편차 큼 | FTTC(Fiber to the Curb) 구성 시 유리 | 동선 내의 잡음 제거 기술(Vectoring) 적용 |

##### 1) ADSL의 동작 원리 (Splitter의 역할)
ADSL은 음성(아날로그)과 데이터(디지털)가 하나의 선에 섞여 있습니다. 이를 분리하기 위해 가정 측과 전화국 측에 **스플리터(Splitter)**라는 필터를 설치합니다.
*   **저역 통과 필터(Low Pass Filter)**: 4kHz 이하의 음성 신호만 전화기로 보냅니다.
*   **고역 통과 필터(High Pass Filter)**: 25kHz 이상의 데이터 신호만 ADSL 모뎀으로 보냅니다.
이때 사용되는 변조 방식은 **DMT (Discrete Multi-Tone)**입니다. DMT는 사용 가능한 주파수 대역을 4kHz 폭을 가진 256개의 부 채널(Tone/Bin)로 쪼개어, 잡음이 심한 구간은 쓰지 않고 잡음이 적은 구간에 많은 비트를 실어 보내는 적응형 기술입니다.

##### 2) VDSL과 FTTC (Fiber to the Curb)
VDSL은 주파수 대역이 매우 넓어 신호 감쇠(Attenuation)가 심합니다. 따라서 전화국(CO)에서 구리선을 직접 끌어오는 기존 방식 대신, 전화국 광케이블을 아파트 단자함(혹은 가로등 근처의 *Curb*)까지 끌어온 뒤, 마지막 몇백 미터만 구리선으로 연결하는 **FTTC** 방식을 주로 사용합니다. 이는 광케이블과 구리선의 하이브리드 형태로, 비용 대비 성능을 극대화한 설계입니다.

#### 2. 케이블 모뎀 (Cable Modem)과 DOCSIS 아키텍처
케이블 인터넷은 **HFC (Hybrid Fiber-Coaxial)** 망 위에서 작동합니다. 방송국 헤드엔드(Head-end)에서 가입자 집까지의 구간은 광케이블과 동축 케이블이 섞여 있으며, 이를 제어하는 프로토콜이 **DOCSIS (Data Over Cable Service Interface Specification)**입니다.

##### [도해] HFC 망 구조 및 데이터 흐름 (ASCII)

```ascii
[Internet] 
    │
[ CMTS / Edge Router ]  (헤드엔드 장비, 전송 속도 제어 및 RF 변환)
    │
    ├──(광케이블 : Backbone)────────────> [ Optical Node ] (광/전기 변환)
    │                                                      │
    │                                   (동축 케이블 : 공유 구간) <-- A구역
    │                                                      │
    ├───< Tap >────────────────────────────────────────────┘
    │                │
    │             (Splitter)
    │                │
    │          [케이블 모뎀] ──(이더넷)──> [PC/IPTV]
    │
    ▼
고주파 대역 활용 (50MHz~860MHz+)
- 다운스트림(Downstream): 헤드엔드 → 가입자 (6MHz 채널 단위, QAM 변조)
- 업스트림(Upstream):   가입자 → 헤드엔드 (5~42MHz 대역, 노이즈 취약)
```

**(해설)**
1.  **CMTS (Cable Modem Termination System)**: 케이블 망의 '게이트웨이' 역할을 합니다. 인터넷 데이터 패킷을 RF(Radio Frequency) 신호로 변조하여 동축 케이블로 내보냅니다.
2.  **공유 매체(Shared Media) 특성**: 그림과 같이 `Optical Node` 이후의 동축 케이블 구간은 해당 지역 가입자들이 모두 공유합니다. 즉, 이웃이 대용량 데이터를 다운로드하면 전체 대역폭을 경쟁하게 되어 속도가 저하될 수 있습니다. 이를 **DOCSIS 프로비저닝(Provisioning)** 기술로 QoS를 보장하지만, 본질적으로는 Best-Effort 성격을 띱니다.
3.  **변조 기술**: **QAM (Quadrature Amplitude Modulation)**을 사용하여 6MHz 폭의 TV 채널 하나에 수십~수백 Mbps의 데이터를 실어 보냅니다. DOCSIS 3.1부터는 OFDM을 사용하여 효율을 극대화했습니다.

#### 3. 핵심 알고리즘: DMT (Discrete Multi-Tone) 상세 (xDSL)
ADSL/VDSL의 핵심인 **OFDM(직교 주파수 분할 다중화)**의 일종인 DMT 동작은 다음과 같습니다.

```python
# [의사코드] DMT 시스템의 비트 로딩(Bit Loading) 과정
# 입력: 채널 특성(신호 대 잡음비, SNR), 목표 오류율(BER)
# 출력: 각 부 반송파(Tone)에 할당될 비트 수

tones = 256       # ADSL의 부 반송파 개수
bits_per_tone = [0] * tones

for i in range(1, tones): # Tone 0은 음성 보호용 제외
    snr = measure_snr(tone=i)
    
    # Shannon-Hartley 정리에 근거한 이론적 전송 용량 산출
    # Capacity = Log2(1 + SNR)
    capacity = log2(1 + snr)
    
    # 실용적 마진을 고려하여 할당 가능 비트 수 결정
    # SNR이 낮은 Tone은 0비트(사용 안 함), 높은 Tone은 15비트까지 할당
    bits_per_tone[i] = floor(capacity - margin)
    
    if bits_per_tone[i] < 0:
        bits_per_tone[i] = 0
```

이 코드는 ADSL 모뎀이 초기화(Handshake) 과정에서 회선 품질을 측정하고, 잡음이 많은 주파수는 버리거나 적은 비트를, 깨끗한 주파수에는 많은 비트를 할당하여 전체 전송량을 최적화하는 과정을 보여줍니다.

> **📢 섹션 요약 비유**: xDSL은 좁은 전화선을 갤러리(Gallery)로 만들어 낮은 층(음성)과 높은 층(데이터)으로 나눈 '이층 버스'와 같고, 케이블 모뎀은 아파트 단지로 들어오는 큰 도로를 모든 세대가 함께 쓰는 '공용 고속도로'와 같습니다. 전자는 도로 용량이 작지만 내 전용 도로라 속도가 일정하고, 후자는 도로가 넓지만 아침 저녁으로 출퇴근길(동시 접속자)이 막히면 정체가 발생합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: xDSL vs Cable Modem

| 비교 항목 | xDSL (ADSL/VDSL) | Cable Modem (HFC) |
|:---|:---|:---|
| **매체 구성** | 전용 회로(Dedicated). 전화국에서 가정까지 1:1 물리적 경로 보장 (맨 끝단 공유 장치 제외). | 공유 회로(Shared). Node 하위 가입자들과 대역폭 경합. |
| **대역폭 성격** | 정적 할당(Static). 계약 속도가 최대 대역폭이며 거리에 따라 감소. | 동적 할당(Dynamic). 혼잡도에 따라 실제 속도 변동폭 큼. |
| **거리 의존성** | **매우 높음**. 전화국으로부터의 거리가 속도를 결정하는 가장 큰 변수 (Attenuation). | **낮음**. 광케이블이 깔린 노드 위치까지는 거리 무관. |
| **품질(QoS)** | 안정적. 회선 독립으로 인해 Ping(Latency) 값이 일정함. 게임/화상에 유리. | 불안정 가능성. 이웃의 트래픽 영향을 받아 Latency가 튈 수 있음. |
| **설치 복잡도** | 간단. 기존 전화선 사용. Splitter만 연결. | 중간. 집 내 동축 케이블 상태 및 Tap 분배 확인 필요. |

#### 2. 과목 융합 관점
*   **물리 계층(Layer 1) 관점**: 두 기술 모두 **OSI 7계층**의 가장 하위인 물리 계층에 속하며, 신호를 변조(Modulation)하여 전송합니다. xDSL의 DMT와 케이블의 QAM 모두 **진폭과 위상을 변화시켜 정보를 담는 디지털 변조 기술**의 적용 사례입니다.
*   **보안(Security) 관점**: xDSL은 기본적으로 Point-to-Point 구조라 **스니핑(Sniffing, 도청)** 위험이 낮지만, 케이블 모뎀은 버스형(Bus