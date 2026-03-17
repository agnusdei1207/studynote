+++
title = "781-785. RAN의 진화 (C-RAN, O-RAN, vRAN)"
date = "2026-03-14"
[extra]
category = "Mobile Architecture"
id = 781
+++

# 781-785. RAN의 진화 (C-RAN, O-RAN, vRAN)

### # 무선 접속망(RAN)의 진화와 개방형 아키텍처

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: RAN (Radio Access Network)은 단일 박스 구조에서 CU (Central Unit)/DU (Distribute Unit)/RU (Radio Unit)로의 기능적 분리(Function Split)와 가상화를 거쳐, 유연한 클라우드 네이티브 아키텍처로 진화하고 있습니다.
> 2. **가치**: C-RAN (Cloud RAN)을 통해 효율적인 자원 풀링(Pooling)과 간섭 제어(CoMP)를 실현하고, O-RAN (Open RAN)을 통해 벤더 락인(Vendor Lock-in)을 해제하여 장비 조달 비용을 약 30~40% 절감할 수 있습니다.
> 3. **융합**: SDN (Software Defined Networking) 기반의 비실시간 RIC (RAN Intelligent Controller)와 AI/ML이 결합되어, 무선 환경 변화에 실시간 대응하는 자율 최적화 네트워크(Self-Organizing Network)로 나아가고 있습니다.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 1. 개념 및 정의
RAN (Radio Access Network)의 진화는 단순한 속도 향상이 아니라, 기지국(BTS, Base Transceiver Station)이라는 거대한 '블랙 박스'를 **논리적 기능별로 분해(Disaggregation)**하고 **소프트웨어화**하는 혁신적인 과정입니다. 과거 단일 하드웨어로 처리되던 무선 프로토콜 스택을 3GPP 표준에 따라 CU, DU, RU로 분리하고, 이를 범용 x86 서버와 가상화 기술(vRAN)로 대체하여 구현합니다.

#### 2. 💡 비유
"과거에는 식당의 주방장이 혼자서 재료 손질, 조리, 플레이팅을 모두 했다면, 이제는 조리 과정을 공장(Central)에서 대량 생산하고, 현장에서는 조립만 하는 도시락 시스템과 같습니다. 게다가 O-RAN은 공장의 기계 규격을 표준화하여 삼성 기계와 LG 부품을 섞어 쓸 수 있게 한 것입니다."

#### 3. 등장 배경
① **기존 한계**: 전용 하드웨어(ASIC) 기반의 폐쇄적 구조로 인해 확장이 어렵고, 벤더 종속성으로 인한 높은 구축 비용(CAPEX) 및 유지보수 비용(OPEX) 발생.
② **혁신적 패러다임**: 가상화(Virtualization)와 SDN/NFV 기술의 성숙, 5G의 고대역폭/저지연 요구로 인한 C-RAN 도입 필요성 대두.
③ **현재의 비즈니스 요구**: MNO (Mobile Network Operator)들은 망 구성의 유연성을 확보하고, 특정 장비 제조사(Vendor)의 기술 종속을 피하기 위해 '개방형 인터페이스(Open Interface)'를 표준으로 요구함.

#### 4. 📢 섹션 요약 비유
> 마치 복잡한 고속도로 톨게이트 시스템에서, 인력이 모든 차량을 수동으로 처리하던 것을 자동화 시스템(CU)과 요금징수기(DU)로 분리하고, 다양한 제조사의 센서를 장착할 수 있는 표준 단자(O-RAN)를 만든 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 1. 구성 요소 상세 분석

| 구성 요소 (Full Name) | 역할 및 기능 | 내부 동작 및 파라미터 | 주요 프로토콜/표준 | 비유 |
|:---|:---|:---|:---|:---|
| **RU (Radio Unit)** | **RF 처리**: 아날로그 신호 변환, 증폭 | ADC/DAC 변환, 필터링, Beamforming<br>*(주파수: 3.5GHz, 28GHz)* | **O-RU**, **eCPRI**, **ROE** | 사람의 눈과 귀 (감각 기관) |
| **DU (Distributed Unit)** | **실시간 L2 처리**: 스케줄링, HARQ, MAC | TTI(Transmission Time Interval) 단위 처리<br>*(지연 요구: 수백 마이크로초)* | **F1 Interface**, **eCPRI** | 사람의 뇌간 (반사 신경) |
| **CU (Central Unit)** | **비실시간 L3 처리**: RRC, PDCP | Mobility Management, QoS 제어<br>*(지연 허용: 수 ms ~ 수십 ms)* | **E1 Interface**, **NG-C** | 사람의 대뇌피질 (사고/판단) |
| **RIC (RAN Intelligent Controller)** | **AI 기반 최적화**: 파라미터 튜닝 | Non-RT RIC: 장기 정책(AI)<br>Near-RT RIC: 단간 제어(Loop) | **A1**, **E2**, **O1** | 통제 타워 (운영 센터) |

#### 2. RAN 기능 분리 (Functional Split) 아키텍처

기지국의 기능을 분리하는 기준(Option)에 따라 Fronthaul에 걸리는 대역폭 요구사항이 결정됩니다. 아래는 주요 Option들을 시각화한 것입니다.

```ascii
+------------------+----------------------+-----------------------------+
|     Option 3     |       Option 6       |          Option 7-2x       |
+------------------+----------------------+-----------------------------+
| [  L3 : RRC  ]   | [  L3 : RRC  ]       | [  L3 : RRC  ]             | CU
| [  L2 : PDCP ]   | [  L2 : PDCP ]       | [  L2 : PDCP ]             |
| [  L2 : RLC  ]   | [  L2 : RLC  ]       | [  L2 : RLC  ]             |
| [  L2 : MAC  ]   | -----------------    | [  L2 : MAC  ]             | DU
| [  L1 : PHY  ]   | [  L1 : PHY  ]       | [  L1 : High-PHY ]         |
| [  RF : analog]  | [  RF : analog]      | [  L1 : Low-PHY ]          | RU
|                  |                      | [  RF : analog]            |
+------------------+----------------------+-----------------------------+
<-- Very Low BW --> <--- Medium BW -----> <--- Very High Bandwidth -->
(CU-DU 분리)       (완전 분리)           (High-PHY 분리, eCPRI 활용)
```
*(해설: 5G 상용망에서는 주로 Fronthaul의 대역폭 효율성을 위해 Option 7-2x(PHY 계층 내부 분리)를 가장 많이 채용합니다.)*

#### 3. C-RAN vs vRAN vs O-RAN 상세 구조도

다음은 3가지 핵심 개념이 어떻게 망물리적으로 구성되는지를 보여주는 통합 다이어그램입니다.

```ascii
             [ 5G Core Network (AMF/SMF/UPF) ]
                          ↑
                     (Backhaul / N3/N2)
                          ↑
+------------------------+------------------------+------------------------+
|      C-RAN (Cloud RAN) Architecture      |
+---------------------------------------------------------------+
|  Central Office (Data Center)                               |
|  +-------------------+  +-------------------+  +-------------+ |
|  |  CU (Control)     |  |  DU (User Plane)  |  | vRAN Stack  | |
|  | [PDCP/RRC]        |  | [RLC/MAC/PHY-H]   |  | (x86 Server)| |
|  +---------+---------+  +---------+---------+  +------+------+  |
|            |                      |                    |         |
+------------+----------------------+--------------------+---------+
             |                      |                    |
             |        Midhaul (F1)  |  vRAN SW           |
             | (Ethernet/IP)        |  (Hypervisor)      |
             |                      |                    |
+------------+----------------------+--------------------+---------+
|      Edge / Cell Site (Tower)                            |
+---------------------------------------------------------------+
|            |                      |                    |         |
|  Fronthaul | eCPRI/ROE            | Management         | O-RAN   |
| (Dark Fiber)| (Low Latency)       | (Netconf/O1)       | W1/M1   |
|            |                      |                    |         |
|  +---------+---------+  +---------+---------+  +------+------+  |
|  |   RU (Radio Unit) |  |   RU (Radio Unit) |  | Near-RT RIC | |
|  | [RF/Low-PHY]      |  | [RF/Low-PHY]      |  | (Real-time) | |
|  +-------------------+  +-------------------+  +-------------+  |
+---------------------------------------------------------------+
             |                      |                    |
        (RF Signal)             (RF Signal)         (Control/Analytics)
             ↓                      ↓                    ↓
       [ Antenna ]              [ Antenna ]         [ A1 Interface ]
                                                           ↑
                                                     +-------+-------+
                                                     | Non-RT RIC    |
                                                     | (SMO/AI/ML)   |
                                                     +---------------+
```

#### 4. 심층 동작 원리 및 코드
1.  **Signal Flow**:
    *   **Downlink**: 5G Core -> CU (Packet Buffering, Header Compression) -> DU (Scheduling, MCS 결정, HARQ) -> RU (OFDM Modulation, DAC, RF Amplification) -> UE.
    *   **Uplink**: UE -> RU (ADC, FFT) -> DU (Channel Estimation, Demodulation) -> CU (PDCP Deciphering) -> Core.
2.  **vRAN Base Station Software Logic (Pseudo Code)**:
    vRAN의 핵심은 범용 서버의 CPU에서 L1/L2 기능을 수행하는 것입니다.

    ```python
    # Pseudo-code for vDU Real-time Scheduling Logic
    class vDU_Scheduler:
        def __init__(self):
            self.ue_metrics = {} # CQI (Channel Quality Indicator) map

        def run_tti_slot(self, frame, subframe):
            # 1. Uplink Channel Estimation (from RU via Fronthaul)
            cqi_report = self.receive_cqi_from_ru()

            # 2. MCS (Modulation and Coding Scheme) Decision
            # 높은 CQI -> 256QAM (높은 전송률), 낮은 CQI -> QPSK (높은 내성)
            mcs_level = self.calculate_adaptive_mcs(cqi_report)

            # 3. Resource Block (RB) Allocation
            # PF (Proportional Fair) 알고리즘 등을 활용하여 스케줄링
            allocation_map = self.allocate_rb(ue_list, policy="ProportionalFair")

            # 4. Transmit to CU/Encapsulate to eCPRI
            # 실시간성 확보를 위해 DPDK (Data Plane Development Kit) 사용
            self.send_to_ru_via_ecpri(allocation_map, mcs_level)
    ```

#### 5. 📢 섹션 요약 비유
> C-RAN은 여러 지점의 소방서에 있던 소방차들을 거대한 중앙 센터(CU/DU)에 모아두고, 현장에는 빠른 속도로 달릴 수 있는 오토바이(RU)만 배치해두는 전략입니다. vRAN은 소방차가 특수 차량이 아니라 일반 승합차를 개조하여 소방차처럼 쓰는 기술이며, O-RAN은 현장의 오토바이와 중앙의 승합차가 서로 다른 회사 제품이라도 무전기 규격만 맞으면 협동할 수 있게 한 '군대의 교전 규칙'과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. C-RAN vs D-RAN (Distributed RAN) 심층 분석

| 구분 | **D-RAN (Distributed)** | **C-RAN (Centralized)** |
|:---|:---|:---|
| **구조** | 기지국(BBU+RRU)가 각 사이트에 분산됨 | BBU(CU/DU)가 중앙에集中, RU만 현장 |
| **CAPEX (설비)** | 개별 사이트별 에어컨/방열 설비 비용 ↑ | 중앙 집중화로 방열 비용 절감, RU 설치 용이 |
| **OPEX (운영)** | 현장 방문 유지보수(MC) 빈번 | 원격 중앙 관리로 유지보수 인력 ↓ |
| **Fronthaul** | 내부 버스 (광케이블 연결 없음) | **eCPRI/ROE** 필요 (광케이블 포설 중요) |
| **성능** | 독립 동작, 간섭 제어 어려움 | **CoMP (Joint Transmission)** 가능, 셀 간 간섭 억제 |
| **지연(Latency)** | 매우 낮음 (내부 처리) | 전송 구간 추가에 따른 Latency 관리 필요 |

#### 2. 기술 표준 및 연관성 분석 (IEEE/3GPP)

| 표준/기술 | **3GPP (RAN)** | **O-RAN ALLIANCE** | **IEEE (Radio/Transport)** |
|:---|:---|:---|:---|
| **주력 포커스** | 무선 프로토콜, 인터페이스 표준화 | 개방형 인터페이스, 지능형 제어(RIC) | 물리층(RF), 이더넷 트래픽 패턴 |
| **주요 문서** | TS 38.401 (Architecture), TS 38.470 (F1) | WG4 (Open Fronthaul), WG2 (RIC) | 802.3ck (100G), 1914.1 (RoE) |
| **연관성** | 코어 기능 정의 | 3GPP 인터페이스 위에 '개방형'을 덧씌움 | eCPRI 패킷을 운반할 물리 계층 제공 |

#### 3. 융합 기술 시너지 및 오버헤드
*   **시너지 (Synergy)**:
    *   **엣지 컴퓨팅 (MEC)**: vRAN 서버에 MEC 플랫폼을 동시에 구축하여, 게임 클라이언트나 자율주차 제어 유닛을 기지국 바로 옆(CU/DU 위치)에 둠으로써 1ms 이내의 초저지연 서비스 구현 가능.
    *   **AI/ML**: O-RAN의 Near-RT RIC에서 UE의 이동 궤적을 예측하여, Handover 명령을 미리 수행하여 핸드오버 실패율을 최소화.
*   **오버헤드 (Overhead)**:
    *   **Fronthaul 대역폭**: Option 7-2x를 사용하더라도 25Gbps~100Gbps급 광케이블이 필요하며, 이를 운용하는 OPEX가 증가할 수 있음.
    *   **프로세싱 지연**: 범용 CPU(x86)를 사용하는 vRAN은 전용 칩(ASIC) 대신 디코딩 지연이 10~20us 정도 더 발생할 수 있어, 타이밍 싱크(Sync) 관리가 중요함.

#### 4. 📢 섹션 요약 비