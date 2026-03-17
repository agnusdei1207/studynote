+++
title = "773-780. 5G 슬라이싱과 무선 혁신 (Massive MIMO)"
date = "2026-03-14"
[extra]
category = "Mobile Architecture"
id = 773
+++

# 773-780. 5G 슬라이싱과 무선 혁신 (Massive MIMO)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **Network Slicing (네트워크 슬라이싱)**은 물리적 인프라를 **SDN (Software Defined Networking, 소프트웨어 정의 네트워킹)** 기반으로 논리적으로 분할하여, 서비스별로 요구되는 성능 지표를 독립적으로 보장하는 가상화 아키텍처이다.
> 2. **가치**: **Massive MIMO (Massive Multiple Input Multiple Output, 대규모 다중 안테나)** 기술을 통해 주파수 효율(Spectral Efficiency)을 비약적으로 높여, 동일 대역폭에서 최대 10배 이상의 용량 증대와 EE (Energy Efficiency, 에너지 효율) 개선을 달성한다.
> 3. **융합**: 슬라이싱은 컴퓨팅 자원의 **NFV (Network Function Virtualization, 네트워크 기능 가상화)**와 결합하여 코어망의 유연성을 확보하고, Massive MIMO는 무선구간에서 **Beamforming (빔포밍)**과 **Hybrid Beamforming (하이브리드 빔포밍)** 기술과 융합하여 공간 분리 다중(SDM)을 실현한다.

+++

### Ⅰ. 개요 (Context & Background)

5G (5th Generation Mobile Networks, 5세대 이동 통신) 시대의 가장 큰 과제는 다양한 서비스 요구사항을 하나의 망으로 수용하는 것이다. 기존의 '베스트 에포트(Best Effort)' 방식은 모든 데이터를 동등하게 취급하여, 긴급한 데이터가 일반 데이터와 섞여 지연되는 문제가 있었다. 이를 해결하기 위해 네트워크 자원을 물리적 건드림 없이 논리적으로 분할하는 슬라이싱 기술이 도입되었다.

동시에, 급증하는 트래픽을 처리하기 위해 무선 구간의 효율성을 극대화해야 했다. 이는 단순히 주파수 대역을 넓히는 것으로는 해결되지 않는다. 따라서 수십~수백 개의 안테나를 사용하여 전파를 공간적인 빔으로 쏘아 특정 사용자에게만 에너지를 집중시키는 Massive MIMO 기술이 5G의 핵심이 되었다.

**💡 비유**: 마치 거대한 하나의 고속도로(Physical Network)를, 일반 차량, 화물차, 긴급 차량을 위해 각기 다른 차선과 속도 제한이 적용된 분리된 도로(Virtual Slice)로 설계하는 것과 같다. 동시에, 도로 위의 신호등이나 안테나가 특정 차량에만 레이저처럼 빛을 비추어 유도하는 지능형 교통 시스템과도 같다.

**등장 배경**:
1.  **기존 한계**: 4G LTE (Long Term Evolution) 시스템에서는 eMBB (Enhanced Mobile Broadband) 위주의 설계로 인해 mMTC (Massive Machine Type Communications) 및 URLLC (Ultra-Reliable and Low Latency Communications) 요구사항을 동시에 만족시키는 데 한계가 존재함.
2.  **혁신적 패러다임**: SDN 컨트롤러를 통해 전체 망의 상태를 실시간으로 인식하고, NFV를 통해 네트워크 기능을 소프트웨어화함으로써, **'Network as a Service'** 개념을 도입.
3.  **비즈니스 요구**: 통신사(MNO) 망을 임대하여 산업체별 사설망으로 제공하는 B2B2B 모델의 확산으로 인해, 보안 및 QoS 보장이 필수적이 됨.

```ascii
[5G 서비스 요구사항 상관관계도]

      ┌───────────────────────────────────────────────────────┐
      │               5G Service Scenarios                    │
      └───────────────────────────────────────────────────────┘
                                │
      ┌─────────────────────────┼─────────────────────────────┐
      ▼                         ▼                             ▼
┌──────────────┐      ┌───────────────┐            ┌───────────────┐
│   eMBB       │      │   mMTC        │            │   URLLC       │
│ (고속 대용량) │      │ (대량 연결)    │            │ (초저지연 신뢰) │
└──────────────┘      └───────────────┘            └───────────────┘
      │                         │                             │
      ▼                         ▼                             ▼
   4K UHD Video            Smart Metering              Self-Driving
   VR/AR Streaming         IoT Sensors                 Remote Control
      │                         │                             │
      └─────────────────────────┴─────────────────────────────┘
                                │
                                ▼
               [ Required: Network Slicing + Massive MIMO ]
```

📢 **섹션 요약 비유**: 5G 슬라이싱과 Massive MIMO의 도입 배경은 마치 복잡한 항만 시스템을 개편하는 것과 같습니다. 원래는 모든 배가 한 부두에 섞여 있어 효율이 낮았지만(기존 망), 이제는 컨테이너선(고속 데이터), 유조선(대량 센서), 긴급 구조선(자율주행)을 위한 전용 부두(슬라이스)를 따로 만들고, 각 선박에 정밀한 레이더 유도(Massive MIMO)를 제공하여 항만 혼잡을 해소한 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 네트워크 슬라이싱을 구현하는 기술적 스택과 Massive MIMO의 신호 처리 원리를 심층 분석한다.

#### 1. 구성 요소 및 아키텍처 (Slicing & Massive MIMO)

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **SDN Controller** | Software Defined Networking Controller | 네트워크 전체를 제어하는 두뇌. Northbound API로 비즈니스 의도를 수신하고, Southbound API로 장비를 제어하여 슬라이스를 생성/삭제/수정함. | OpenFlow, NETCONF | 교통 통제 센터 |
| **NFVI** | Network Functions Virtualization Infrastructure | 가상화된 네트워크 기능(VNF)이 구동되는 하드웨어/소프트웨어 리소스 풀. 서버, 스토리지, 스위치로 구성됨. | KVM, Docker | 클라우드 서버 팜 |
| **gNodeB (gNB)** | Next Generation NodeB | 5G 무선 접속망(RAN)의 기지국. Massive MIMO 안테나 어레이와 신호 처리 디지털 유닛(DU/RU)을 포함. | 5G NR, FAPI | 빔포밍 라이트하우스 |
| **RF Transceiver** | Radio Frequency Transceiver | 디지털 신호를 아날로그 전파로 변환하고, 수십~수백 개의 안테나 포트를 통해 빔을 형성하는 아날로그 프론트엔드. | Beamforming, Phase Shifting | 빔 조명 장치 |
| **Network Slice** | Network Slice | 종단 간(E2E) 논리적 망. RAN 슬라이스, Core 슬라이스, Transport 슬라이스로 구성되며, 각각 독립적인 **S-NSSAI (Single Network Slice Selection Assistance Information)** 식별자를 가짐. | HTTP/2, SBI | 전용 고속 도로 |

#### 2. 슬라이싱 아키텍처 및 데이터 흐름

**도입**: 네트워크 슬라이싱은 단순히 데이터를 분리하는 것이 아니라, 제어평면(Control Plane, CP)과 사용자평면(User Plane, UP)을 독립적으로 구성하는 **CUPS (Control and User Plane Separation)** 구조를 기반으로 한다. UE (User Equipment)가 망 접속 시, 자신의 요구에 맞는 슬라이스를 식별하고 할당받는 절차(Registration & Slice Selection)가 필수적이다.

```ascii
[5G Network Slicing Architecture (E2E)]

┌─────────────────────────────────────────────────────────────────────────┐
│                        5G Core Network (5GC)                            │
│  ┌─────────────────┐    ┌─────────────────────────────────────────┐   │
│  │   AMF (Access   │    │  SMF (Session Mgmt) + UPF (User Plane)  │   │
│  │ Mobility Mgmt)  │◄───┤   (Slice A: URLLC / High Security)      │   │
│  └────────┬────────┘    │   ┌─────────────────────────────────┐   │   │
└───────────┼─────────────┤   │  SMF + UPF (Slice B: eMBB / BW)   │   │   │
            │             │   └─────────────────────────────────┘   │   │
            ▼             └─────────────────────────────────────────┘   │
      [N1/N2 Interface]                                              │
            ▼                                                          │
┌─────────────────────────────────────────────────────────────────────┐│
│                         RAN (Radio Access Network)                  ││
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              ││
│  │   gNB - CU   │  │   gNB - DU   │  │   gNB - RU   │              ││
│  │ (Control)    │  │ (Real-time)  │  │ (RF/Array)   │              ││
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              ││
└─────────┼─────────────────┼─────────────────┼─────────────────────┘┘
          │                 │                 │
          ▼                 ▼                 ▼
    [ Slice 1 ]        [ Slice 2 ]        [ Slice 3 ]
     (Guaranteed)      (Best Effort)      (Priority)
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                    [Air Interface: Beams]
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
    [UE: Auto]          [UE: Phone]        [UE: Sensor]
```

**해설**: 위 다이어그램은 3GPP 표준화 기반의 5G 아키텍처를 단순화한 것이다.
1.  **UE (User Equipment)**는 접속 시 `S-NSSAI` ID를 AMF (Access and Mobility Management Function)로 전송한다.
2.  **AMF**는 요청을 분석하여 해당 슬라이스가 지원되는 **SMF (Session Management Function)** 및 **UPF (User Packet Forwarding)**로 라우팅한다.
3.  **RAN** 구간인 gNB는 사용자별로 다른 무선 자원(빔, 시간 슬롯)을 할당한다. 예를 들어, URLLC 슬라이스(Slice 1) 사용자에게는 우선 순위가 가장 높은 무선 자원을, eMBB 슬라이스(Slice 2) 사용자에게는 남는 대역폭을 할당한다.
4.  이 과정에서 **Network Slice Selection Function (NSSF)**가 개입하여 적절한 네트워크 인스턴스를 선택하는 의사결정을 수행한다.

#### 3. Massive MIMO 및 빔포밍 원리

**도입**: Massive MIMO는 단순히 안테나 수를 늘리는 것이 아니다. 채널 행렬(Channel Matrix)의 차원을 확대하여 '공간 자유도(Spatial Degrees of Freedom)'를 확보하는 기술이다. 이를 통해 **SDMA (Space Division Multiple Access, 공간 분할 다중 접속)**가 가능해지며, 같은 주파수 자원을 공간적으로 분리된 사용자가 공유할 수 있다.

**심층 동작 원리**:
1.  **CSI-RS (Channel State Information-Reference Signal)**: 기지국은 파일럿 신호를 송신하고, UE는 채널 상태 정보를 피드백한다.
2.  **Beamforming Vector Calculation**: 기지국은 수신한 CSI를 바탕으로 채널 행렬($H$)에 대응하는 프리코딩 매트릭스($W$)를 계산한다. 주로 **SVD (Singular Value Decomposition, 특이값 분해)** 알고리즘이 사용된다.
    *   수식: $y = H W x + n$
3.  **Hybrid Beamforming**: 디지털 빔포밍(Baseband)과 아날로그 빔포밍(RF Phase Shifter)을 결합하여 하드웨어 비용과 전력 소모를 줄이며 수백 개의 안테나를 제어한다.

```ascii
[Massive MIMO 빔포밍 신호 흐름]

Digital Data Stream
      │
      ▼
[  Baseband Unit (BBU) / Digital Beamforming  ]
│ ┌──────────────────────────────────────────┐ │
│ │   x1 ──┐                                 │ │
│ │   x2 ──┼─► [ Precoding W_digital ]       │ │
│ │   ... ──┘     (Maximize SNR)            │ │
│ └──────────────────────────────────────────┘ │
      │ (Data streams: Layers)
      ▼
[ RF Transceiver Unit / Analog Beamforming ]
│ ┌──────────────────────────────────────────┐ │
│ │  Phase Shifter Array ◄── [ W_analog ]    │ │
│ │      ────┬────┬────┬────┬────            │ │
│ └─────────┼────┼────┼────┼───────────────── │ │
            │    │    │    │
            ▼    ▼    ▼    ▼   (Physical Antenna Ports)
           ╱    ╱    ╱    ╱    ╱
         //  //  //  //  //  (Antenna Array: 64T64R, 128T128R)

   [ Signal Propagation in Air ]
      │    │   ↖  ↗
      └────┼────☁  (Narrow Beams targeted to UEs)
           │    ↙  ↘
           ▼
      [UE 1]  [UE 2]
```

**해설**:
*   **Digital Beamforming**: 데이터 스트림 레벨에서 신호의 위상과 크기를 조절하여 데이터 간 간섭을 제거하는 기능. 유연하지만 RF 체인 수가 많아지면 비용이 급증한다.
*   **Analog Beamforming**: 위상 변이기(Phase Shifter)를 사용하여 전파 자체의 방향을 물리적으로 조정. 빔의 이득(Gain)을 높이는 역할을 한다.
*   **Beam Management**: 사용자의 이동에 따라 빔이 끊기지 않도록 최적의 빔 페어(Beam Pair)를 지속적으로 추적하고 변경하는 절차가 수행된다.

**핵심 알고리즘 (Zero-Forcing 예시)**: