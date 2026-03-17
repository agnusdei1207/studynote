+++
title = "890-900. 광 백본망과 전송 기술 (OTN, ASON, SONET)"
date = "2026-03-14"
[extra]
category = "Advanced Comm"
id = 890
+++

# 890-900. 광 백본망과 전송 기술 (OTN, ASON, SONET)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 광 백본망은 인터넷의 물리적 대동맥으로, SDH/SONET의 **TDM (Time Division Multiplexing)** 기반 엄격한 동기화에서 OTN의 **WDM (Wavelength Division Multiplexing)** 기반 파장 단위 다중화, 그리고 ASON의 **GMPLS (Generalized Multi-Protocol Label Switching)** 기반 지능형 제어로 진화해왔습니다.
> 2. **가치**: 50ms 이내의 **RTO (Recovery Time Objective)**를 만족하는 SONET의 자가 복구망 구조와 OTN의 **FEC (Forward Error Correction)**를 통한 전송 거리 확보는 초고속 인터넷 서비스의 5 Nine(99.999%) 이상의 신뢰성을 보장합니다.
> 3. **융합**: 5G/6G 이동통신의 **Fronthaul** 트래픽 처리를 위해 ROF 기술과 결합하며, AI 기반 트래픽 예측을 통해 ASON 제어 평면의 경로 최적화가 지속적으로 진화되고 있습니다.

+++

### Ⅰ. 개요 (Context & Background)

광 백본망(Optical Backbone Network)은 국가 및 대륙 간 트래픽을 처리하는 초고속 통신망의 인프라로, 단순한 유리 섬유의 나열을 넘어 정밀한 **전송 제어(Transport Control)**와 **신호 처리(Signal Processing)** 기술이 집약된 시스템입니다.

초기 전송망은 **PDH (Plesiochronous Digital Hierarchy)** 방식을 사용하여 비동기식으로 데이터를 전송했으나, 대역폭 효율성이 낮고 관리가 어렵다는 한계가 있었습니다. 이를 극복하기 위해 등장한 것이 **SDH (Synchronous Digital Hierarchy)**와 북미 표준인 **SONET (Synchronous Optical Networking)**입니다. 이들은 엄격한 클럭 동기화를 통해 **TDM** 방식으로 대역폭을 분할하여 사용하며, 링(Ring) 구조를 통해 물리적 단선에도 불구하고 50ms 이내에 서비스를 복구하는 강력한 생존성(Survivability)을 제공합니다.

그러나 인터넷 데이터 트래픽의 폭발적 증가와 이더넷(Ethernet) 중심의 패킷 전송 패러다임 변화로 인해, 기존 SDH의 고정된 계층 구조는 효율성 문제를 야기했습니다. 이에 따라 광 파장(Wavelength) 자체를 채널로 사용하는 **DWDM (Dense Wavelength Division Multiplexing)** 기술과 다양한 프로토콜을 수용할 수 있는 **OTN (Optical Transport Network)**이 표준으로 자리 잡았습니다. 또한, 수동적인 망 관리를 넘어 라우팅 프로토콜을 도입하여 경로를 자동으로 설정하는 **ASON (Automatically Switched Optical Network)** 기술이 더해져 망의 자원 활용도와 유연성을 극대화하고 있습니다.

```ascii
[광 전송 기술의 진화 흐름]

   PDH (Plesiochronous)          SDH/SONET (TDM)                OTN (WDM/Packet)
  [ 비동기 계층 ]  -------->  [ 동기식 계층 (Ring) ]  -------->  [ 디지털 래퍼 (Mesh) ]
        (낮은 효율)              (TDM 기반 고정 대역)           (파장 기반 유연 대역)
                                  |                              |
                                   +--------> ASON (Control Plane) <----+
                                              (지능형 경로 설정 & 자가 복구)
```

이러한 진화 과정은 '정보의 하드웨어화'에서 '정보의 소프트웨어화'로의 변화를 반영합니다. 단순히 회선을 할당하던 방식에서, 파장을 할당하고 스스로 경로를 찾는 지능형 망으로 변모하고 있습니다.

📢 **섹션 요약 비유**: 광 전송망의 진화는 **'단일 선로의 철도'에서 '고속철도 네트워크'**, 그리고 **'자율 주행이 가능한 초고속 도로망'**으로 발전하는 과정과 같습니다. PDH는 단선 철도에서 열차를 보내는 것처럼 효율이 낮았고, SDH/SONET은 정해진 시간표에 맞춰 운행되는 고속철도처럼 정확하지만 경로가 rigid합니다. OTN은 여러 차선을 효율적으로 쓸 수 있는 광활한 고속도로 건설이며, ASON은 이 도로 위에서 상황에 따라 스스로 경로를 찾는 내비게이션 및 교통 제어 시스템을 도입한 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

광 백본망의 핵심은 **전송 계층(Transport Layer)**의 물리적 구조와 **제어 계층(Control Layer)**의 소프트웨어 로직으로 나누어 볼 수 있습니다. 여기서는 SDH/SONET의 프레임 구조, OTN의 디지털 래퍼, 그리고 ASON의 제어 평면 아키텍처를 심층 분석합니다.

#### 1. 핵심 구성 요소 비교

| 구성 요소 | 전체 명칭 (Abbreviation) | 핵심 역할 | 내부 동작 메커니즘 | 주요 프로토콜/표준 | 비유 |
|:---:|:---|:---|:---|:---|:---|
| **SDH/SONET** | Synchronous Digital Hierarchy / Synchronous Optical Networking | **정밀 동기 전송** | 125µs(마이크로초) 단위의 프레임을 사용하여 Octet 단위로 정렬된 데이터를 전송. 포인터(Pointer) 기술로 클럭 오프셋 보정. | ITU-T G.707 / ANSI T1.105 | **정시 열차 시스템**: 정확한 시간에 맞춰 출발하고 도착하는 스케줄링. |
| **OTN** | Optical Transport Network | **멀티서비스 수용 및 전송** | **G.709** 표준의 디지털 래퍼 사용. 클라이언트 신호(IP, Ethernet, SDH)를 OPUk에 담고, ODUk 오버헤드와 OTUk FEC를 추가하여 파장에 실음. | ITU-T G.709, G.798 | **유니버설 컨테이너**: 내용물에 상관없이 표준 상자에 담아 운송하고 파손 여부를 감시. |
| **ASON** | Automatically Switched Optical Network | **지능형 경로 설정** | GMPLS 프로토콜 기반. UNI(사용자-망), INNI(망 내부), ENNI(외부 망 간) 인터페이스를 통해 연결 설정 요청을 처리하고 SPSC/LSP 경로를 계산. | ITU-T G.8080, IETF GMPLS | **자동 교환 시스템**: 전화 교환수가 수동으로 연결하던 것을 시스템이 자동으로 패칭(Patching). |

#### 2. SDH/SONET 전송 프레임 구조 및 동기화

SDH/SONET의 핵심은 **STS (Synchronous Transport Signal)** 프레임 구조입니다. 기본적인 전송 단위는 **STM-1 (Synchronous Transport Module level-1)** 또는 **OC-1 (Optical Carrier level-1)**이며, 이들은 **VT (Virtual Tributary)** 또는 **TU (Tributary Unit)**라는 하위 단위로 다중화됩니다.

```ascii
[SDH STM-1 프레임 구조 (9행 x 270열, 125µs 주기)]

+-------------------------------------------------------+
| Section Overhead (SOH) |  Pointer  |   Payload (VC-4)  |
+------------------------+-----------+-------------------+
| RSOH                   | MSOH      |   Path Overhead   |
(Regen Section)      (Multiplex Section)     (POH)
```

1.  **Section Overhead (SOH)**: 프레임의 성능 감시, 오류 수정 등을 담당합니다.
2.  **Pointer (포인터)**: SDH의 가장 혁신적인 기능으로, **클럭 주파수 차이로 인한 데이터의 위상차**를 흡수합니다. (동기화가 조금 어긋나도 데이터 손실이 없음)
3.  **Payload (페이로드)**: 실제 사용자 데이터가 들어가는 공간인 **VC (Virtual Container)**입니다.

#### 3. OTN (Optical Transport Network)의 디지털 래퍼와 FEC

OTN은 데이터를 감싸는 3단계 구조의 **디지털 래퍼(Digital Wrapper)** 기술을 사용합니다. 이는 클라이언트 신호(예: 10GbE, OC-192)에 **OAM (Operations, Administration, and Maintenance)** 정보와 **FEC (Forward Error Correction)** 코드를 추가합니다.

```ascii
[OTN G.709 디지털 래퍼 구조]

+-------------------------------------------------------------+
| OTUk (Optical Channel Data Unit-k)                         |
|   - FEC (Forward Error Correction) : 전송 오류 자체 복원    |
|   - OTUk OH : Overhead (OTN 관리 정보, TTI, BIP-8)          |
+-------------------------------------------------------------+
| ODUk (Optical Data Unit-k)                                 |
|   - ODUk OH : 경로 추적, 연결성 감시 (PM/TCM)               |
+-------------------------------------------------------------+
| OPUk (Optical Payload Unit-k)                              |
|   - OPUk OH : 페이로드 타입, 클라이언트 매핑 정보           |
+-------------------------------------------------------------+
| 클라이언트 신호 (Client Signal)                            |
|   (Ethernet, IP, SDH, Fibre Channel, etc.)                 |
+-------------------------------------------------------------+
```

*   **FEC (Forward Error Correction)**: **RS (Reed-Solomon)** 코드 등을 사용하여 데이터에 중복성(Parity)을 추가합니다. 수신측은 수신된 신호의 SNR (Signal-to-Noise Ratio)을 분석하여, 재전송 요청 없이 즉시 오류 비트를 복구합니다. 이는 광 증폭기 간격을 늘리고 전송 거리를 수천 km로 확장하는 데 결정적인 역할을 합니다.

#### 4. ASON 제어 평면 (Control Plane) 동작 원리

ASON은 기존의 전송망에 **IP 라우팅 개념**을 도입한 것입니다. 크게 **UNI (User-Network Interface)**, **I-NNI (Internal NNI)**, **E-NNI (External NNI)**로 구성됩니다.

*   **연결 설정 (Connection Setup)**:
    1.  소스 노드가 **CRSP (Connection Request)** 발생.
    2.  **제어 평면**은 **TE (Traffic Engineering)** 데이터베이스를 참조하여 사용 가능한 파장과 대역폭 확인.
    3.  **GMPLS RSVP-TE** 프로토콜을 사용하여 경로 설정 메시지(Path Message) 전송.
    4.  목적지 노드가 **Resv (Reservation)** 메시지로 응답하며 레이블(Lambda) 할당.
    5.  크로스 커넥트(Cross-Connect) 스위치가 물리적 경로 연결.

```ascii
[ASON 아키텍처: Control Plane vs Management Plane]

+------------------+     +------------------+     +------------------+
|   Management      |     |   Control Plane  |     |   Transport      |
|   Plane (MPLS-TD) |     |   (ASON/GMPLS)   |     |   Plane (DWDM)   |
+------------------+     +------------------+     +------------------+
| - 소프트웨어적 정책 | <-> | - 자원 발견       | <-> | - 광 스위칭      |
| - 정적 경로 설정   |     | - 동기적 경로 계산|     | - 데이터 전달    |
| - NMS 시스템 연동 |     | - 장애 복구(FRR) |     |                 |
+------------------+     +------------------+     +------------------+

        (정적 & 느림)            (동적 & 실시간)            (하드웨어)
```

이 구조를 통해 망 운영자는 **NMS (Network Management System)**에서 정적으로 경로를 설정하거나, ASON을 통해 트래픽 폭주 시 **SC (Soft-Permanent Connection)** 또는 **SNC (Switched Connection)** 모드로 즉각적으로 대역폭을 확보할 수 있습니다.

📢 **섹션 요약 비유**: **SDH**는 **'기차 시간표'**입니다. 모든 객차(데이터)는 시간표에 맞춰 연결되어 움직이며, 포인터 기술은 약간의 지연(연결 시간)을 허용하여 끊김 없이 연결합니다. **OTN**은 **'짐칸 도어와 보안 시스템이 있는 화물 컨테이너'**입니다. 내용물이 뭐든 컨테이너에 담기만 하면 되고, 컨테이너 외부의 센서(FEC)가 낙하나 파손을 감지하여 즉시 수리합니다. **ASON**은 **'지능형 교통 통제 센터'**입니다. 사고가 나거나 정체가 발생하면, 운전기사가 보고하기도 전에 시스템이 알아서 우회 도로를 찾아 신호등을 제어하고 차량을 유도합니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

광 전송 기술은 단순히 물리 계층의 기술을 넘어 상위 계층(L2/L3)과의 융합, 그리고 무선 구간과의 시너지를 창출합니다.

#### 1. SDH vs. OTN: 심층 기술 비교

| 비교 항목 | SDH / SONET | OTN (Optical Transport Network) |
|:---|:---|:---|
| **다중화 방식** | TDM (Time Division Multiplexing) | WDM + TDM (Hybrid) |
| **프레임 구조** | 정적 계층 (VC-12, VC-3, VC-4...) | 디지털 래퍼 (OPUk, ODUk, OTUk) |
| **오버헤드** | Section / Line / Path OH 복잡 | 직렬적 래퍼 구조, OAM 풍부 |
| **오류 제어** | BIP(Bit Interleaved Parity) 감시만 가능 | **FEC (Forward Error Correction)**로 실시간 비트 복구 |
| **수용 신호** | 주로 음성/E1/T1 중심 | **Any Service**: Ethernet, IP, SDH, Fiber Channel, CPRI 등 |
| **전송 효율** | 고정 대역 할당으로 낭비 발생 가능 | 파장 단위 풍부한 대역, GFP로 효율적 매핑