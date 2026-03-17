+++
title = "574-580. 5G 이동통신과 핵심 기술 (eMBB, URLLC, mMTC)"
date = "2026-03-14"
[extra]
category = "Wireless & Mobile"
id = 574
+++

# 574-580. 5G 이동통신과 핵심 기술 (eMBB, URLLC, mMTC)

## # 5G 이동통신 시스템 (5th Generation Mobile Communication System)

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 5G는 단순한 전송 속도의 향상을 넘어, **eMBB**(초고속), **URLLC**(초저지연), **mMTC**(초연결)라는 상충하는 요구사항을 **Network Slicing**(망 분할) 기술로 하나의 물리적 인프라에서 논리적으로 해결하는 **Softwarized Network**의 정점이다.
> 2. **가치**: 셀룰라 IoT의 확장으로 스마트 팩토리 및 자율주행 등 산업 디지털 전환(DX)의 인프라가 되며, 전송 지연(Latency) 1ms 이하와 연결 밀도 $10^6 devices/km^2$을 달성하여 현실과 가상을 잇는 매개체로 작용한다.
> 3. **융합**: SDN(Software Defined Networking)/NFV(Network Functions Virtualization) 기반의 Core Network와 MEC(Multi-access Edge Computing)를 결합하여 네트워크 지연을 극복하고, AI 기반의 자원 관리(RAN Intelligent Controller)와 융합하여 자립형 최적화(Self-Optimizing Network)를 실현한다.

+++

### Ⅰ. 개요 (Context & Background) - 5G 패러다임의 전환

**1. 개념 및 정의**
5G (5th Generation Mobile Communication System)는 IMT-2020 (International Mobile Telecommunications-2020) 표준에 따라 정의된 차세대 이동통신 기술이다. 이전 세대(3G, 4G)가 주로 '사람 간의 통신(H2H, Human to Human)'과 '이동 중 데이터 접속'에 초점을 맞췄다면, 5G는 **'사물과 사물의 통신(M2M, Machine to Machine)'**과 **'초고대역/초저지연'** 성능을 필수 조건으로 명시하였다. 이는 단순한 스펙업(Spec-up)이 아닌, 통신망을 다양한 산업군이 수용하는 **플랫폼화**하는 것을 핵심 철학으로 한다.

**2. 등장 배경: 4G의 한계와 새로운 수요**
4G LTE (Long Term Evolution) 시대에 모바일 트래픽은 폭발적으로 증가했으나, 스마트 팩토리나 자율주행차와 같은 실시간 제어 서비스에는 무선 구간의 불안정성(Jitter)과 지연(Latency)이 치명적인 한계로 작용했다.
- **① 기존 한계**: 주파수 자원의 고갈, 데이터 전송 속도의 물리적 한계, 증가하는 밀도 지원 불가.
- **② 혁신적 패러다임**: 증설(More Cell)이 아닌 **기술적 효율성(Spectrum Efficiency)**과 **네트워크 가상화(Virtualization)**를 통해 해결.
- **③ 비즈니스 요구**: Telco(통신사)의 매출 증대를 위한 B2B Vertical Market 개척(자동차, 제조, 의료 등).

**3. 기술적 특징**
5G는 6GHz 이하의 주파수뿐만 아니라 **Frequency Range 2 (FR2)**, 즉 24GHz~52GHz 대역의 **mmWave (Millimeter Wave)**를 적극 활용하여 대역폭을 확보한다. 또한, **CP (Cyclic Prefix)** 길이 최적화, **Numerology** (서브캐리어 간격 변화) 등을 통해 다양한 서비스 요구사항을 만족시킨다.

```ascii
[이동통신 세대별 패러다임 진화]

1G (AMPS)        2G (CDMA/GSM)       3G (WCDMA)        4G (LTE/LTE-A)           5G (IMT-2020)
+----+           +----+              +----+            +----+                  +----+
|음성|           |문자|              |영상|            |데이터 급증|          |초연결/지능|
+----+           +----+              +----+            +----+                  +----+
  |                |                   |                 |                       |
  v                v                   v                 v                       v
Analog           Digital Voice       Mobile Web        Mobile Broadband       Hyper-connected
(아날로그)       (디지지 음성)       (모바일 웹)       (브로드밴드)           (AI/IoT Platform)
                                                                                 |
                                                         +-----------------------+-----------------------+
                                                         |                       |                       |
                                                     [eMBB: Speed]          [URLLC: Latency]       [mMTC: Density]
```
*해설*: 1G에서 4G까지는 사람의 사용성(음성, 문자, 웹, 속도)을 중심으로 진화했으나, 5G는 서비스의 성격(Speed, Latency, Connection)에 따라 망 자체가 분화되는 구조적 진화를 겪었다. 특히 **eMBB**, **URLLC**, **mMTC**라는 삼각축이 등장하여 각기 다른 물리 계층 파라미터를 요구하게 되었다.

> 📢 **섹션 요약 비유**: 5G의 등장은 **'단순한 도로 확장'에서 '교통 통제 시스템의 지능화'로의 전환**과 같습니다. 4G까지는 차량(데이터)이 늘어나면 도로(주파수)를 넓히는 것이 전부였다면, 5G는 승용차, 화물차, 긴급 차량이 섞여 달리도록 신호등을 제어하고 차선을 동적으로 할당하여 사고 없이 최대한 많은 차를 고속으로 운영하는 **'지능형 교통 시스템(ITS)'**을 도입한 것입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 5G NR (New Radio) 무선 접속 기술 구조**
5G의 무선 구조는 Flexibility(유연성)가 핵심이다. 다양한 주파수 대역과 서비스 요구사항을 수용하기 위해 파라미터를 가변적으로 조정한다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Mechanism) | 주요 파라미터/프로토콜 |
|:---|:---|:---|:---|
| **Numerology** | OFDM 심볼 구조 정의 | $\mu (0\sim4)$ 값에 따라 **SCS (Subcarrier Spacing)**를 15kHz~120kHz까지 가변 조정. 주파수가 높을수록 SCS를 넓혀 페이딩(Doppler) 영향 최소화. | SCS = $15 \times 2^\mu$ kHz |
| **Frame Structure** | 전송 타이밍 기준 | 10ms 길이의 무선 프레임(Radio Frame)을 10개의 서브프레임(1ms)으로 분할. TDD(Time Division Duplex) 기반의 Dynamic Frame 구조 사용. | SS/PBCH Block (Sync Signal) |
| **SSB (SS/PBCH Block)** | 초기 동기 및 접속 | UE (User Equipment)가 망에 접근하기 위한 **Synchronization Signal**과 **System Information**을 전달. 빔 형성(Beamforming)된 형태로 전송됨. | PSS/SSS (PSS: Primary SS) |
| **BWP (Bandwidth Part)** | 전력 절약 및 유연성 | UE가 전체 대역폭이 아닌 특정 부분대역만 할당받아 수신하여 **RF (Radio Frequency)** 전력 소모를 줄임. | Adaptation, Power Saving |
| **DCI (Downlink Control Info)** | 상향/하향 스케줄링 | gNB(Base Station)가 UE에게 "어떤 자원(RB)으로, 어떤 MCS(변조 방식)로, 언제 보낼지"를 지시하는 메시지. | PDCCH (Physical DCCH) |

**2. 핵심 무선 기술: Massive MIMO & Beamforming**
데이터 전송 속도와 주파수 효율을 높이기 위해 **Antenna Port** 수를 대폭 늘리고 전파를 좁은 빔(Beam)으로 쏘는 기술이다.

```ascii
[Massive MIMO 및 Beamforming 동작 원리도]

      < 기존 4G Antenna (섹터 방식) >            < 5G Massive MIMO (빔포밍 방식) >
      
      +---------------+                         +---------------+
      |   [Antenna]   |                         | [64/128 Ant.] |
      +---------------+                         +---------------+
             |                                           |
             v                                           v
      ~~~~~~~~~~~~~~~~ 전파 널리 퍼짐      [       ]      [       ]
      ~~~~~~~~~~~~~~~~ (Interference)       [Beam 1]      [Beam 2]
      ~~~~~~~~~~~~~~~~ (Energy Waste)      [       ]      [       ]
                                                   |          |
                                                   v          v
                                              +-------+  +-------+
                                              |  UE A |  |  UE B |
                                              +-------+  +-------+
```
*해설*: 기존 LTE는 안테나에서 전파를 사방으로 퍼뜨려(섹터) 필요 없는 방향으로도 에너지가 낭비되고 간섭이 발생했다. 반면 5G는 수십 개 이상의 안테나(Massive MIMO)를 통해 각 UE(User Equipment)로 향하는 위상차(PH)를 계산하여 전파를 레이저처럼 특정 지점에 집중시킨다. 이를 통해 **SINR (Signal to Interference plus Noise Ratio)**을 극대화하고 셀 경계(Cell Edge) 성능을 획기적으로 개선한다.

**3. 핵심 알고리즘 및 코드: Hybrid Automatic Repeat Request (HARQ)**
신뢰성을 보장하기 위한 오류 제어 절차이다.

```c
// [의사코드] 5G NR HARQ Process 동작 시나리오
// UE는 DL (Downlink) 데이터 수신 시 CRC 오류 검증

function receive_PDSCH(dciv_msg, tb_data):
    crc_val = calculate_CRC(tb_data)
    
    if crc_val == SUCCESS:
        // 1. 데이터 상위 계층 전달
        deliver_to_mac(tb_data)
        // 2. ACK (Acknowledgment) 전송
        send_uci(ACK)
    else:
        // 데이터 손상 발생
        // 3. 버퍼에 임시 저장 (Soft Combining을 위해)
        store_soft_buffer(tb_data)
        // 4. NAK (Negative Acknowledgment) 전송 -> gNB가 재전송
        send_uci(NAK)
```
*해설*: 5G는 Chase Combining과 IR (Incremental Redundancy) 방식을 혼합하여 재전송 효율을 높인다. 네트워크 슬라이스마다 **RAN (Radio Access Network)** 상에서 HARQ 타이머나 최대 재전송 횟수를 다르게 설정하여 URLLC(Ultra-Reliable Low Latency)용 슬라이스는 신속한 폐기를, eMBB용 슬라이스는 끈질긴 재전송을 수행하도록 구성할 수 있다.

> 📢 **섹션 요약 비유**: 5G 아키텍처는 **'대형 조명 시스템'**과 같습니다. 기존 방식이 전체 방을 환하게 비추는 **'전등'**이었다면, 5G는 수많은 LED 소자를 제어하여 특정 사람(사용자)만 따라 움직이며 비추는 **'무대 조명(Spotlight)'** 시스템입니다. 이를 통해 불필요한 빛(간섭)은 줄이고 내가 원하는 곳에만 강력한 빛을 집중시켜 효율을 극대화합니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 5G 3대 서비스 시나리오 심층 비교**
ITU-R IMT-2020에서 제시한 3대 핵심 시나리오는 물리 계층(RAN)에서 상이한 요구사항을 가진다.

| 비교 항목 | **eMBB** (Enhanced Mobile Broadband) | **URLLC** (Ultra-Reliable Low Latency Comm.) | **mMTC** (Massive Machine Type Comm.) |
|:---|:---|:---|:---|
| **핵심 목표** | 전송 속도(Throughput), 대역폭 | 지연 시간(Latency), 신뢰성(Reliability) | 연결 밀도(Connection Density), 배터리 수명 |
| **주요 지표** | **Peak Rate**: 20Gbps (DL), 10Gbps (UL) <br> **Experience Rate**: 100Mbps (이동 중) | **Latency**: 1ms (Over-the-air) <br> **Reliability**: 99.999% (5-nines) | **Density**: $1,000,000 units/km^2$ <br> **Battery Life**: 10+ years |
| **주요 기술** | mmWave (주파수 확장), Massive MIMO, CA (Carrier Aggregation) | Short TTI (Transmission Time Interval), Mini-slot, Grant-free transmission, SC-FDM | Narrowband IoT, Low Cost/Complexity UE, Deep Coverage |
| **대표 서비스** | 4K/8K UHD 스트리밍, VR/AR, Cloud Gaming | 자율주행(C-V2X), 원격 로봇 수술, 스마트 그리드 제어 | 스마트 시티(가로등/수도), 홈 IoT, Asset Tracking |

**2. 네트워크 슬라이싱 (Network Slicing) 분석**
물리적인 망 하나를 여러 개의 논리적 망(Slice)으로 분리하여 운영하는 기술이다. 가상화 기술(NFV/SDN)이 필수적이다.

```ascii
[Network Slicing 및 E2E 자원 할당 구조]

┌────────────────────────────────────────────────────────────────────┐
│                   5G Standalone Core Network (SBA)                 │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Slice #1     │  │ Slice #2     │  │ Slice #3     │            │
│  │ [eMBB]       │  │ [URLLC]      │  │ [mMTC]       │            │
│  │ BW: 100MHz   │  │ Latency:<1ms │  │ Devices: 1M  │            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
└─────────┼──────────────────┼──────────────────┼───────────────────┘
          │                  │                  │
          v                  v                  v
┌────────────────────────────────────────────────────────────────────┐
│              RAN (Radio Access Network) - gNB (CU/DU)              │
│  ┌──────────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ NUMOLOGY: Low SCS    │  │ NUMOLOGY: HighSCS│  │ NUMOLOGY: ? │ │
│  │ Frame: Full Buffer   │  │ Frame: Mini-slot │  │ Frame: Long │ │
│  └────────────────