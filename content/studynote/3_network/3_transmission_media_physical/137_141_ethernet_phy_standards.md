+++
title = "137-141. 이더넷 물리 계층 표준의 진화 (IEEE 802.3 PHY)"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 137
+++

# [이더넷 물리 계층 표준의 진화]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**= 이더넷 PHY (Physical Layer) 표준은 물리적 매체(구리/광)의 주파수 대역폭 한계를 극복하기 위해, NRI (Near-end Crosstalk) 제거와 고차 PAM (Pulse Amplitude Modulation) 변조 및 레인(Lane) 병렬화 기술로 진화해왔습니다.
> 2. **가치**= 10Mbps에서 800Gbps로의 비약적인 대역폭 확장은 단순한 속도 상승이 아니라, AI/ML 훈련 workload를 위한 ultra-low latency와 백플레인(Backplane) 전력 효율의 혁신을 의미합니다.
> 3. **융합**= L2 스위칭(MAC Layer)의 TCAM(Ternary Content-Addressable Memory) 처리 속도와 직결되며, 광통신(Component)과 전자 신호 처리(DSP) 기술의 융합이 집약된 결과물입니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
이더넷은 현재 LAN(Local Area Network) 및 데이터센터의 사실상 표준(de facto standard)입니다. IEEE 802.3工作组(Working Group)은 OSI 7계층 중 가장 하위에 있는 물리 계층과 데이터 링크 계층의 MAC(Media Access Control) 부분을 표준화합니다. 특히 물리 계층(PHY)은 비트 스트림을 전기적 신호나 광신호로 변환하여 매체에 실는 역할을 담당합니다.

이더넷 표준의 명명법은 `[Speed][Signal Type][Media Type]`의 구조를 가지며, 기술의 진화 방향을 압축적으로 보여줍니다.
*   **Speed**: 전송 속도 (예: 10, 100, 1000...)
*   **BASE**: Baseband (베이스밴드), 즉 변조 없이 디지털 신호를 직접 전송하는 방식. 광대역 아날로그 신호(Broadband)를 쓰지 않음을 의미합니다.
*   **Media Type**:
    *   **T**: Twisted Pair (구리선, UTP/STP)
    *   **S**: Short Wavelength (광섬유, 850nm, 멀티모드 주로 사용)
    *   **L**: Long Wavelength (광섬유, 1310/1550nm, 싱글모드 주로 사용)
    *   **C**: Copper (동축 케이블, 고속 직결용)
    *   **K**: Backplane (기판 내 배선)

#### 2. 등장 배경
① **초기의 한계 (Shared Media)**: 초창기 10Mbps 시절은 충돌 감지(CSMA/CD)를 위해 반이중(Half-Duplex) 방식을 사용했으나, 스위칭 기술의 도입으로 전이중(Full-Duplex)이 가능해지며 속도 확장의 문이 열렸습니다.
② **대역폭의 요구 (Bandwidth Hunger)**: 인터넷 폭발과 클라우드 컴퓨팅, 그리고 최근 AI/딥러닝 모델의 훈련 데이터 양이 기하급수적으로 증가함에 따라, 1Gbps 이더넷은 병목 지점이 되었습니다.
③ **물리적 한계의 극복**: 구리선(UTP)은 주파수가 높아질수록 신호 감쇠(Attenuation)와 노이즈, crosstalk(누화) 현상이 심해집니다. 이를 극복하기 위해 단순히 클럭 속도를 높이는 것을 넘어, **DSP(Digital Signal Processing)** 기반의 복잡한 코딩과 변조 기술이 도입되었습니다.

#### ASCII: 이더넷 표준 명명법 파싱
```ascii
   [ETHERNET NAMING CONVENTION DECODER]
   
   +--------+-----------+--------------------+
   | SPEED  | SIGNAL    | MEDIA TYPE         |
   +--------+-----------+--------------------+
   | 1000   | BASE      | -T                 |
   |   |    |   |       |  |                 |
   |   v    |   v       |  v                 |
   | 1 Gbps | Baseband  | Twisted Pair (Copper)
   
   EXAMPLE: 1000BASE-LX
   -> 1 Gbps, Baseband, Long wavelength (Single Mode Fiber)
```
*   **해설**: 이 명명법은 엔지니어가 케이블의 종류와 전송 거리, 속도를 즉시 파악하게 해줍니다. 기술이 복잡해질수록 표준명 뒤에 붙는 알파벳의 종류도 다양해졌습니다(예: ZR, DWDM 등).

> **📢 섹션 요약 비유**: 이더넷 물리 계층의 진화는 마치 단순한 비포장 도로(10BASE-T)에서 출발하여, 트럭의 속도를 높이고(클럭업), 도로의 차선을 넓히고(레인 병렬화), 심지어 화물 적재 방식부터 혁신하여(고차 변조), 고속철도 같은 초고속 물류망(800GbE)을 구축해온 과정과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이더넷 물리 계층은 크게 **PCS (Physical Coding Sublayer)**, **PMA (Physical Medium Attachment)**, **PMD (Physical Medium Dependent)** 계층으로 나뉩니다. 여기서는 구리선(UTP) 기반의 기술적 진화와 광케이블의 WDM(Wavelength Division Multiplexing) 기술을 심층 분석합니다.

#### 1. 구성 요소 상세 분석 (PHY Layers)

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 관련 기술/프로토콜 |
|:---:|:---|:---|:---|
| **PCS** (Physical Coding Sublayer) | 데이터를 전송에 적합한 코드로 변환 | 8b/10b, 64b/66b 인코딩, Auto-negotiation | IEEE 802.3 Clause |
| **PMA** (Physical Medium Attachment) | 병렬 데이터를 직렬(Serial)로 변환 | SerDes (Serializer/Deserializer), 매체 타이밍 복구 | PLL (Phase Locked Loop) |
| **PMD** (Physical Medium Dependent) | 실제 매체로 신호 송수신 | 드라이버 송신, 신호 감지, 매체 인터페이스 | DAC, Optical Module |

#### 2. 구리선(UTP) 이더넷의 진화: 10Gbps와 PAM 변조
구리선으로 10Gbps를 전송하는 것은 **기적과도 같은 기술**입니다. `10GBASE-T`는 단순한 전압 높낮이가 아닌 복잡한 DSP를 사용합니다.

#### ASCII: PAM 변조 기술 비교 (Manchester vs PAM-5 vs PAM-4)
```ascii
   [MODULATION TECHNIQUE EVOLUTION]
   
   1. Manchester (10BASE-T)
   Clock: _-_-_-_-_-_-_-_-
   Data : ___-----___-----
   -> Low efficiency (2 symbols for 1 bit)

   2. PAM-5 (1000BASE-T) - 5 Voltage Levels (-2, -1, 0, +1, +2)
   
   Level ^      *     *     *     (Constellation Diagram)
         |      | \   | \   | \
         |   *  |  \  |  \  |  *
         |   |  |   \ |   \|
         |___*__*____*____*________> Time
          -2 -1  0  +1  +2
   -> 4D-PAM5 (4 pairs) + Trellis Coding

   3. PAM-4 (400GBASE-T/ Optical) - 4 Voltage Levels (00, 01, 10, 11)
   
   Level ^      [01]  [11]
         |      [00]  [10]
         |___________________> Time
   
   -> 2 Bits per Symbol (Higher Density, Lower SNR required)
```
*   **해설**: `10BASE-T`는 맨체스터 인코딩을 써서 대역폭 효율이 50%에 불과했습니다. `1000BASE-T`는 **PAM-5**를 통해 심볼당 2비트를 전송하려 시도했으나, 전압 레벨 간 간격이 좁아지면서 노이즈에 취약해졌습니다. 이를 해결하기 위해 **4개의 페어를 동시에 활용**하고 `DSQ (Double Square)` 매트릭스를 사용합니다. 최신 400G/800G 광 이더넷은 **PAM-4** 변조를 사용하여 레이저의 밝기(진폭)를 4단계로 조절해 1심볼 당 2비트 정보를 전송합니다.

#### 3. 광섬유(Fiber) 아키텍처: WDM과 레인(Lane)
광케이블 대역폭을 확장하는 방법은 한 가닥의 광섬유 속도를 높이는 것보다, 여러 파장(Wavelength)을 섞어 보내는 **WDM** 방식이 효율적입니다.

#### ASCII: 400GbE 시리얼/병렬 구조 (IEEE 802.3bs)
```ascii
   [400GBASE-SR8 / 400GBASE-LR8 ARCHITECTURE]
   
   MAC Client
      |
      v
   400 Gbps Media Access Control
      |
      | (Reconciliation)
      v
   < PCS (Physical Coding Sublayer ) >
      | -> 64b/66b Encoding
      |
      v
   < PMA (Multiplexing) >
      | 1 : 8 De-multiplexing (Split)
      | 8 Lanes of 53.125 Gbps PAM-4 signals
      v
   +-------------------------------+
   |  Lane 1 | Lane 2 | ... | Lane 8 | (Parallel Optics)
   +-------------------------------+
      |        |             |
      v        v             v
   (Fiber Ribbon / MPO Connector) -> to Switch/Server
```
*   **해설**: 400GbE를 구현하기 위해 가장 널리 쓰이는 방식은 **8개의 레인(Lane)**을 병렬로 묶는 것입니다. 각 레인은 약 50Gbps(PAM-4 기준)의 속도를 내며, 이를 물리적으로는 MPO(Multi-fiber Push On) 커넥터를 통해 광섬유 리본으로 연결합니다. 이는 전기적 신호를 한 줄로 보내기엔 물리적 한계(손실, 전자기 간섭)가 명확하기 때문입니다.

#### 4. 핵심 알고리즘: LDPC 및 RS-FEC
고속 통신은 비트 오류율(BER)을 높입니다. IEEE 802.3 표준(특히 200G/400G 이상)은 **FEC (Forward Error Correction)**를 필수로 채택합니다.
*   **RS-FEC (Reed-Solomon FEC)**: (528, 514) 코드를 사용하여 오류를 정정합니다. 오버헤드는 약 5.4%입니다.
*   **Algorithm Flow**: `Encode at TX -> Channel -> Detect Errors at RX -> Correct using Parity Check bits`

> **📢 섹션 요약 비유**: 구리선 이더넷(10GBASE-T)의 PAM 변조와 DSP는 마치 소음이 심한 시장에서 두 사람이 대화하는 상황과 같습니다. 목소리(신호)를 크게 하는 것(증폭)만으로는 안 되고, 서로 다른 높이로 말하는 사람들을 동시에 구별해 듣는 고도의 집중력(DSP, Echo Cancellation)과, 혹시 못 알아들을까 봐 문장마다 '해설'(FEC)을 붙여 보내는 안전장치가 필요합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Copper vs. Optical
데이터센터 내에서의 선택(ToR Switch <-> Server)을 위해 정량적/구조적 분석을 수행합니다.

| 비교 항목 | Copper (Twisted Pair/DAC) | Optical (Fiber) |
|:---|:---|:---|
| **대표 규격** | 10GBASE-T, 25GBASE-CR, 100GBASE-CR4 | 100GBASE-SR4, 400GBASE-FR4 |
| **전송 거리** | 짧음 (DAC: 3~5m, UTP: 최대 100m) | 김 (MMF: 100~500m, SMF: 10km~40km) |
| **지연 시간 (Latency)** | **매우 낮음** (<0.5µs for DAC) | 상대적으로 높음 (SerDes/O-E 변환 오버헤드) |
| **전력 소모 (Power)** | 높음 (DSP 처리 및 Heat 발생) | 낮음~중간 (Transceiver 소모) |
| **비용 (Cost)** | 케이블 저렴, 인터페이스 복잡 | 모듈(Transceiver) 고가, 케이블 저렴 |
| **주요 용도** | 랙 내(Top of Rack) 서버 연결 | 스위치 간 연결, Long-haul 전송 |

#### 2. 과목 융합 관점
*   **컴퓨터 구조 (Computer Architecture)와의 관계**: CPU와 메모리 속도 차이를 줄이기 위해 버스 속도를 높이듯, 네트워크도 **PCIe(Peripheral Component Interconnect Express)** 버스의 **Gen5/Gen6** 속도(32Gbps~64Gbps)를 네트워크 인터페이스 카드(NIC)가 처리해야 합니다. 800Gbps를 처리하려면 CPU의 I/O 병목을 막기 위해 **RDMA (Remote Direct Memory Access)** 기술을 통한 Zero-copy 전송이 필수적입니다.
*   **OS (Operating System)와의 관계**: 커널 레벨의 인터럽트 핸들링(Interrupt Handling) 비용을 줄이기 위해 DPDK (Data Plane Development Kit)나 Kernel Bypass 기술이 사용되며, 이는 물리 계층의 속도가 너무 빨라 소프트웨어 스택을 따라가지 못하기 때문에 발생한 융합 기술입니다.

> **📢 섹션 요약 비유**: 전선(Copper)과 광섬유(Fiber)의 선택은 도심지 통근 방식과 같습니다. DAC(구리선)는 **지하철**과 같아서 정거장(Rack) 간 이동이 빠르고 빈번할 때 유리하지만, 서울에서 부산까지(Data center 간) 이동해야 한다면 비행기나 KTX(광케이블)를 이용하는 것이 효율적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 데이터센터 구축 시 의사결정 매트릭스
AI 학습용 GPU 서버 클러스터를 구축할 때, GPU 간 통신(NVLink over Fabric)과 외부 스토리지 연결을 위해 어떤 PHY를 선택할 것인가?