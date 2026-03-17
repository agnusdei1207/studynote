+++
title = "567-573. 이동통신 세대별 기술 (1G to 4G LTE)"
date = "2026-03-14"
[extra]
category = "Wireless & Mobile"
id = 567
+++

# 567-573. 이동통신 세대별 기술 (1G to 4G LTE)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이동통신의 진화는 주파수 효율성 극대화를 위해 **다중 접속(Multiple Access)** 기술을 '주파수(FDMA)'에서 '시간(TDMA)', '코드(CDMA)', 그리고 '주파수 효율성이 극대화된 부반송파(OFDMA)'로 변경해온 역사입니다.
> 2. **가치**: 음성 중심의 회선 교환(Circuit Switched) 망을 **All-IP 패킷 교환(Packet Switched)** 망으로 완전히 전환하여, 이동성이 보장된 상태에서 광대역 데이터를 초저지연으로 처리하며 IoT(사물인터넷) 기반을 마련했습니다.
> 3. **융합**: **안테나 기술(MIMO)**과 **디지털 신호 처리(DSP)**의 융합을 통해 스펙트럼 효율을 단위당 bps/Hz 단위로 획기적(1G 대비 10,000배 이상)으로 향상시켰습니다.

+++

### Ⅰ. 개요 (Context & Background)

이동통신 기술의 진화는 **"유선에 가까운 무선(Wireline-like Wireless Quality)"**을 구현하기 위한 끊임없는 노력입니다. 1G는 단순히 아날로그 신호를 전파에 실어 보내는 것에 그쳤으나, 2G에서는 디지털 변조 기술을 도입하여 보안성과 효율을 높였습니다. 3G에 이르러 멀티미디어 서비스가 가능해졌으나, 데이터 폭증에 대비하기 위한 패킷 기반 망으로의 전환이 필요했습니다. 이를 완성한 것이 4G LTE이며, 음성 통화조차 데이터 패킷으로 처리하는 **VoLTE (Voice over LTE)**를 통해 **PSTN (Public Switched Telephone Network)**의 회선 교환 방식을 무선망에서 완전히 퇴출시켰습니다.

#### 💡 비유
이동통신의 역사는 '도로 교통 체증을 해결하는 방식'의 발전과 같습니다.
- **1G**: 편도 1차선 도로에서 누가 먼저 가느라 싸우는 것 (경쟁)
- **2G**: 신호등을 설치해 순서대로 보내는 것 (TDMA) 또는 특정 코드를 가진 차만 통과하는 것 (CDMA)
- **3G**: 도로를 넓혀 고속 주행이 가능하게 한 것
- **4G**: 기존 도로 위에 2층, 3층 고가 도로를 건설하여 층별로 동시 주행하게 한 것 (OFDMA)

#### 📢 섹션 요약 비유
"진흙탕 길(1G)을 포장하고(2G), 고속도로를 뚫고(3G), 드디어 그 위에 하이패스 전용 차로가 설치된 초고속 인터넷 고속도로(4G)를 완성한 과정입니다."

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이동통신 시스템의 핵심은 제한된 **주파수 자원(Spectrum)**을 얼마나 효율적으로 나누어 쓰느냐에 달려 있습니다. 이를 결정하는 것이 **다중 접속(Multiple Access)** 기술입니다.

#### 1. 핵심 기술 분석

| 기술 | Full Name | 작동 원리 | 특징 및 단점 |
|:---|:---|:---|:---|
| **FDMA** | Frequency Division Multiple Access | 주파수 대역을 물리적으로 쪼개어 할당. | 간단하지만 대역 효율이 낮고, 주파수 간 간섭(Guard Band)이 필요함. (1G) |
| **TDMA** | Time Division Multiple Access | 같은 주파수를 시간 슬롯(Time Slot)으로 나누어 사용. | 디지털화 가능하나, 슬롯 할당 오버헤드 존재. (2G GSM) |
| **CDMA** | Code Division Multiple Access | 데이터에 고유한 부호(Walsh Code)를 실어, 같은 주파수/시간대에서 중첩 사용 후 복조. | 간섭에 강하며 용량이 크나, 전력 제어가 복잡함. (2G IS-95, 3G) |
| **OFDMA** | Orthogonal Frequency Division Multiple Access | 주파수 간격을 수학적으로 직교(Orthogonal)시켜 간섭을 최소화한 수천 개의 부반송파 사용. | **4G/LTE의 핵심**. 고속 페이딩에 강하고 대역 효율이 극대화됨. |

#### 2. 세대별 주파수 사용 변화 ASCII 다이어그램

```ascii
[주파수 자원 할당 방식의 진화]

1. FDMA (1G):       사용자A   간격   사용자B   간격   사용자C
    [=======]       [#######]       [#######]       [#######]
    (주파수 분할)

2. TDMA (2G):       주파수 1채널 내에서 시간 분할
    |---Time 1---|---Time 2---|---Time 3---|---Time 4---|
    [  User A  ]  [  User B  ]  [  User C  ]  [  User A  ]

3. CDMA (3G):       코드에 의한 중첩
    [User A Code: 1011] ──┐
    [User B Code: 1100] ──┼──> [ 모두 동시에 전송 (叠加) ] ──> 수신기에서 코드로 분리
    [User C Code: 0110] ──┘

4. OFDMA (4G):       직교 부반송파 (효율성 극대화)
    Subcarrier# ▂▂▂▃▃▃▅▅▅▆▆▆▇▇▇███ (빈틈없이 밀착)
    User 1      [--------][--------]
    User 2                  [--------][--------]
    User 3      [--------]
    (주파수/시간 2차원 자원 할당, 스케줄링 유연함)
```

#### 3. 심층 동작 원리: LTE의 쌍둥이 (OFDMA & MIMO)

**A. OFDMA (Orthogonal Frequency Division Multiplexing Access)**
데이터 전송 시 다중 경로(Multipath)로 인한 **페이딩(Fading)** 현상은 최대 적입니다. LTE는 좁은 대역폭의 수많은 부반송파(Subcarrier)를 병렬로 전송하여, 특정 주파수가 페이딩되더라도 다른 주파수는 살아남게 합니다. 이때 각 부반송파는 수학적으로 서로 영향을 주지 않는 **직교성(Orthogonality)**을 가지므로, 보호 대역(Guard Band) 없이 빈틈없이 배치될 수 있습니다.

**B. MIMO (Multiple-Input Multiple-Output)**
**MIMO (Multiple-Input Multiple-Output)**는 송수신 단에 다수의 안테나를 배치하여 동일한 주파수 자원을 사용하면서도 전송 속도를 안테나 수에 비례해 높이는 기술입니다. 단순히 다이버시티(Diversity, 신호 강건성)를 넘어, 서로 다른 데이터 스트림을 동시에 전송하는 **공간 분할 다중화(Spatial Multiplexing)**를 통해 주파수 효율($bps/Hz$)을 극대화합니다.

```c
// 의사코드: LTE 채 추정 및 복조 과정
Rx_Signal[y][t] = Channel_Matrix[y][x] * Tx_Signal[x][t] + Noise[y][t]

// 수신부에서는 채널 추정(Channel Estimation)을 통해
// 역행렬(Inverse Matrix) 또는 MMSE 알고리즘을 사용하여
// 원본 송신 신호 Tx_Signal을 복원해냄.
// 수식: H^-1 * Y = X (신호 분리)
```

#### 📢 섹션 요약 비유
"OFDMA는 사람이 타기 힘든 좁은 비탈길(주파수)을 수만 개의 좁은 계단(부반송파)으로 다져서 올라가는 기술이며, MIMO는 이 좁은 길 위로 여러 개의 차선(공간 스트림)을 만들어 동시에 질주하게 하는 고속도로 공법입니다."

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교표: 회선 교환 vs 패킷 교환

| 구분 | Circuit Switched (음성 중심) | Packet Switched (데이터 중심) |
|:---|:---|:---|
| **대표 세대** | 1G ~ 3G | 4G LTE / 5G |
| **자원 할당** | 통화 시작 시 끝까지 전용 선로 점유 | 패킷 단위로 필요할 때만 자원 사용 |
| **망 구성** | **MSC (Mobile Switching Center)** 중심 | **EPC (Evolved Packet Core)** 중심 (All-IP) |
| **지연 시간** | 낮음 (실시간 보장) | 변동 가능 (Best Effort, QoS 기술로 보완) |
| **효율성** | 유휴 시간(Silence)에도 자원 낭비 | 통신 중인 경우에만 자원 소모 (효율 극대화) |

#### 2. 세대별 스펙트럼 효율 및 데이터 속도 비교

| 세대 | 주요 기술 | 다운링크 속도 (이론적) | 주파수 효율 (bps/Hz) | 핵심 서비스 |
|:---|:---|:---|:---|:---|
| **1G** | AMPS (FDMA) | 약 2.4 Kbps | N/A (Analog) | 음성 통화 |
| **2G** | GSM (TDMA) | 9.6 ~ 14.4 Kbps | ~0.13 | 음성, SMS |
| **3G** | W-CDMA | 384 Kbps ~ 2 Mbps | ~1.0 | 영상 통화, 인터넷 |
| **4G** | LTE (OFDMA/MIMO) | 75 Mbps ~ 1 Gbps (LTE-A) | ~5.0 ~ 15.0 | HD 스트리밍, 클라우드 |

#### 3. 과목 융합 관점: 네트워크(OSI 7 Layer)와의 관계
이동통신의 진화는 OSI 7 Layer에서 **Layer 1(Physical)**의 변화가 **Layer 2~3(MAC/IP)**으로 확장된 과정입니다.
- **Physical Layer 변화**: 1G의 아날로그 변조에서 4G의 OFDM 변조로 진화하며 전송 용량이 획기적 증가.
- **Layer 2/3의 융합**: 4G는 **CS (Circuit Switched)** 도메인을 폐지하고 **PS (Packet Switched)** 도메인만 남겼습니다. 이는 음성 서비스가 단순히 '망'의 기능이 아니라 '앱(App)'과 같은 **VoIP (Voice over IP)** 패킷으로 처리됨을 의미하며, 이를 위해 **QoS (Quality of Service)** 보장을 위한 **EPS Bearers** 개념이 도입되었습니다.

#### 📢 섹션 요약 비유
"기존 3G까지가 '전용 회선으로 연결된 구내 전화망'이라면, 4G LTE는 회사 내의 모든 전화기, 팩스, 컴퓨터를 하나의 광랜(LAN) 스위치에 통합시켜서, 전화마저도 인터넷 데이터 패킷으로 쏙 들어가게 만든 '올인원 네트워크'와 같습니다."

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 음영 지역(Indoor/Hotspot) 커버리지 확보

**[문제 상황]**
고층 빌딩 내부나 지하와 같은 음영 지역에서는 **Macro Cell (기지국)**의 전파가 도달하기 어렵고, 건물 밀집으로 인한 **Shadowing** 현상이 발생합니다. 매크로 셀 출력을 단순히 높이는 것은 **Inter-cell Interference (셀 간 간섭)**을 유발하여 망 전체의 성능을 저하시킵니다.

**[의사결정 및 솔루션]**
이를 해결하기 위해 **Small Cell (Femtocell/Picocell)** 도입 및 **HetNet (Heterogeneous Network)** 아키텍처를 구성해야 합니다.

```ascii
[HetNet 아키텍처 개념도]

      ┌───────────────┐
      │  Macro Cell   │  (넓은 커버리지, 기지국 안테나 높이)
      │   (Coverage)  │
      │               │
      │  ┌─────────┐  │
      │  │SmallCell│  │  (좁은 범위, 고용량, 실내 설치)
      │  │ (Hotspot)│  │  ──> 가까운 거리에서 고속 데이터 제공
      │  └─────────┘  │
      └───────────────┘

[투자 대비 효율성 분석]
Macro Cell 증설: 설비비($$$$) > 용량 증가(x1.5)
Small Cell 도입:  설비비($)  > 용량 증가(x3.0) (특정 지역 조밀도 고려)
```

#### 2. 도입 체크리스트 (LTE/LTE-A 네트워크 설계)

| 구분 | 항목 | 검증 포인트 |
|:---|:---|:---|
| **기술적** | **Interference Management** | 셀 간 간섭 제어 기술(IRC, FFR)이 적용되었는가? |
| | **Backhaul** | Small Cell을 위한 유선/무선 백홀(Backhaul) 대역폭은 충분한가? |
| **운영·보안** | **Handover** | Macro-Small Cell 간 이동 시 핸드오버 실패율(RLF)이 1% 이하인가? |
| | **Authentication** | USIM 기반의 인증 키(Key) 생성이 MME(Mobility Management Entity)에서 안전하게 처리되는가? |

#### 3. 안티패턴 (Anti-Pattern)
- **Over-provisioning**: 매크로 셀 출력을 과도하게 높여 인접 셀에 심각한 간섭(Pilot Pollution)을 유발하는 잘못된 설계.
- **Legacy dependency**: 4G 망 내에서도 3G **CSFB (Circuit Switched Fallback)** 방식에 의존하여 음성 통화 시 데이터가 끊기도록 설계하는 것 (VoLTE 미도입).

#### 📢 섹션 요약 비유
"고속도로(매크로 셀)가 혼잡하다고 해