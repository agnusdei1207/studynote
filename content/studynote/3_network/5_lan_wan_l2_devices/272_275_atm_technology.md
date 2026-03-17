+++
title = "272-275. ATM (비동기 전송 모드) 기술"
date = "2026-03-14"
[extra]
category = "LAN/WAN & L2 Devices"
id = 272
+++

# 272-275. ATM (비동기 전송 모드) 기술

### # ATM (Asynchronous Transfer Mode)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존 패킷 교환의 비효율성과 회선 교환의 경직성을 해소하기 위해, **53바이트 고정 길이 셀(Cell)** 기반의 하드웨어 스위칭을 통해 음성·데이터·영상을 통합 전송하는 연결 지향형(Connection-Oriented) 전송 기술.
> 2. **가치**: 고정된 셀 크기를 통해 **지연 시간(Jitter) 최소화** 및 QoS(Quality of Service) 보장을 실현하여, 멀티미디어 서비스에 최적화된 대역폭 효율성 제공.
> 3. **융합**: **B-ISDN (Broadband Integrated Services Digital Network)**의 실현체로, MPLS (Multiprotocol Label Switching)의 라벨 스위칭 개념과 현대 광통신망의 QoS 매커니즘에 시사점을 제공.

---

### Ⅰ. 개요 (Context & Background)

**ATM (Asynchronous Transfer Mode)**은 ITU-T(국제전신전화자문위원회)에 의해 표준화된 광대역 종합정보통신망인 **B-ISDN (Broadband Integrated Services Digital Network)**을 구현하기 위한 핵심 전송 방식입니다. 이는 기존의 패킷 교환(Packet Switching) 방식의 유연성과 회선 교환(Circuit Switching) 방식의 신뢰성을 결합한 '하이브리드' 전송 기술이라는 점에서 기술적 의의가 큽니다.

ATM의 가장 큰 특징은 전송 데이터를 가변 길이의 프레임(Frame)이 아닌, **고정된 53바이트의 셀(Cell)** 단위로 쪼개어 전송한다는 것입니다. 이러한 고정 길이 전송은 데이터의 길이가 들쭉날쭉한 경우 발생할 수 있는 전송 지연(Delay)과 지연 변동(Jitter)을 예측 가능하게 만들어, 실시간 음성이나 영상 서비스에 필수적인 QoS(Quality of Service)를 보장합니다. 또한, 비동기식 시분할 다중화(TDM)를 사용하여 사용자가 데이터를 보낼 때만 채널을 점유하므로, 기존 동기식 TDM 방식에 비해 대역폭 효율성을 극대화했습니다.

**💡 비유: 고속도로 톨게이트와 컨테이너**
이더넷(Ethernet)이 상자 크기가 제각각인 택배 트럭들이 섞여 길을 막는 도로系统이라면, ATM은 모든 화물을 **정확히 53kg짜리 표준 컨테이너(셀)**에 담아야만 진입할 수 있는 자동화된 초고속 물류 허브와 같습니다. 화물의 크기가 똑같으므로 로봇 팔(하드웨어 스위치)이 크기를 재거나 확인할 필요 없이 무조건 빠르게 옮길 수 있습니다.

#### 1. 등장 배경 및 기술적 필요성
① **기존 패킷 교환의 한계**: 이더넷이나 IP 망은 '최선의 노력(Best Effort)' 전송 방식을 채택하여, 데이터의 순서나 지연 시간을 보장하지 않았습니다. 이는 음성 통화처럼 실시간성이 중요한 서비스에는 치명적이었습니다.
② **STM (Synchronous Transfer Mode)의 한계**: 기존 전화망(PSTN)의 TDM 방식은 사용하지 않을 때도 대역폭을 점유하여 낭비가 심했습니다.
③ **ATM의 혁신**: **셀(Cell)**이라는 작은 단위로 모든 서비스를 통합하고, **가상 경로(Virtual Path)** 개념을 도입하여 하드웨어적인 고속 스위칭과 논리적인 회선 할당을 동시에 달성했습니다.

📢 **섹션 요약 비유**: ATM은 "택배 트럭들이 제멋대로 섞여 서로 길을 막는 일반 도로(패킷 교환)"와 "기차가 정해진 시간에만 달려야 하는 철도(회선 교환)"의 단점을 모두 해소하여, **"모든 화물을 표준 상자에 담아 24시간 멈추지 않고 컨베이어 벨트로 나르는 초고급 물류 센터"**와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

ATM 기술의 핵심은 **물리적인 전송 매체 위에 위치한 ATM 계층**과 그 위에서 다양한 상위 서비스를 ATM 셀로 변환해 주는 **AAL (ATM Adaptation Layer)**로 구성된 계층 구조입니다. 이 절에서는 ATM이 실제로 어떻게 셀을 처리하고 스위칭하는지에 대한 메커니즘을 심층 분석합니다.

#### 1. ATM 셀 구조 및 필드 분석
ATM 셀은 **5바이트의 헤더(Header)**와 **48바이트의 페이로드(Payload)**로 구성된 총 53바이트의 고정 길이를 가집니다. 헤더의 구조는 **UNI (User-Network Interface, 사용자-망 인터페이스)**와 **NNI (Network-Network Interface, 망 간 인터페이스)**에 따라 약간씩 다릅니다.

**[표] ATM 셀 헤더 필드 상세 분석 (UNI 기준)**

| 요소명 (Bit) | 역할 및 내부 동작 | 비고/용도 |
|:---|:---|:---|
| **GFC (Generic Flow Control)** (4비트) | 로컬 망 내부에서의 혼잡 제어 및 흐름 제어. 일반적으로 0으로 설정되어 사용되지 않음. | 멀티플렉싱을 위한 공유 매체 접근 제어용 |
| **VPI (Virtual Path Identifier)** (8비트) | **가상 경로 식별자**. 여러 개의 가상 채널(VCC)을 하나의 묶음으로 관리하기 위한 파이프 라벨. | 교환기에서 경로를 대표적으로 라우팅할 때 사용 (하나의 파이프) |
| **VCI (Virtual Channel Identifier)** (16비트) | **가상 채널 식별자**. 최종 목적지 또는 연결 지점을 식별하는 세부 주소. | VPI 내의 개별 채널 (하나의 전화 회선) |
| **PTI (Payload Type Indicator)** (3비트) | 페이로드가 사용자 데이터인지, 시스템 관련 정보(OAM)인지, 혹은 셀이 혼잡을 경험했는지를 표시 | QoS 및 흐름 제어를 위한 플래그 |
| **CLP (Cell Loss Priority)** (1비트) | **셀 손실 우선순위**. 망 혼잡 시 1로 표시된 셀을 먼저 폐기하여 중요한 데이터(0)를 보호함. | 트래픽 형상(Shaping) 및 약속된 속도 policing |
| **HEC (Header Error Control)** (8비트) | 헤더 오류 수정. CRC 방식을 사용하여 헤더의 비트 오류를 검출 및 수정. **동기화**에도 활용됨. | PHY 계층과 ATM 계층의 경계에서 정렬에 핵심적 역할 |

#### 2. ATM 계층 구조 및 스위칭 메커니즘
ATM은 연결 지향형(Connection-Oriented) 서비스입니다. 데이터 전송 전에 반드시 **SVC (Switched Virtual Circuit)** 또는 **PVC (Permanent Virtual Circuit)** 설정 절차를 거쳐야 합니다. 이 과정에서 송수신 경로 상의 모든 스위치는 **VPI/VCI 매핑 테이블**을 구축하게 됩니다.

```ascii
+-------------------+       +-------------------+       +-------------------+
|   Source End      |       |  ATM Switch       |       |  Dest End         |
|  (User Device)    |       |  (Cross-connect)  |       |  (User Device)    |
+-------------------+       +-------------------+       +-------------------+
| AAL Layer         |       |                   |       | AAL Layer         |
| [48 Byte Payload] |       | [Routing Table]   |       | [Reassembly]      |
|      + 5 Byte Hdr |       |                   |       |      + 5 Byte Hdr |
+--------+----------+       +--------+----------+       +--------+----------+
         |                           |                           |
         |  Cell: [VPI:1, VCI:A]     |                           |
         +-------------------------->                           |
         |                           |                           |
         |                   In: (1, A) -> Out: (2, B)          |
         |                   (Label Swapping)                   |
         |                           |                           |
         |                           |   Cell: [VPI:2, VCI:B]    |
         |                           +-------------------------->|
         |                           |                           |

[Logic Flow]
1. 송신단은 AAL 계층에서 데이터를 48바이트로 조각낸 뒤 ATM 헤더(VPI/VCI)를 부착.
2. 스위치는 수신한 셀의 VPI/VCI를 인덱스로 하여 라우팅 테이블을 참조.
3. 새로운 VPI/VCI로 헤더를 교체(Label Swapping)하여 출력 포트로 전송.
4. 수신단은 누적된 48바이트 페이로드를 AAL 계층에서 원래 데이터로 재조립(Reassembly).
```

#### 3. 핵심 동작: HEC를 이용한 셀 동기화 (Self-Healing)
ATM 망은 프리앰블(Preamble) 같은 비트 동기 신호를 별도로 보내지 않습니다. 대신 **HEC 필드**를 사용하여 경계를 찾습니다.
* 수신측은 들어오는 비트 스트림을 1비트씩 이동시키며 HEC 계산을 수행합니다.
* 특정 위치에서 HEC 계산이 성공하면 "여기가 셀의 시작점(Hunt State)"으로 간주하고, 53바이트마다 경계를 설정(Sync State)합니다.
* 만약 연속하여 에러가 발생하면 다시 동기화 과정을 반복합니다.

#### 4. 심층 코드: 셀 라우팅 의사 코드 (C-Style)
```c
// ATM Switching Logic (Conceptual)
typedef struct {
    int incoming_port;
    int vpi_in;
    int vci_in;
    int outgoing_port;
    int vpi_out;
    int vci_out;
} ATM_Routing_Entry;

// Incoming Cell Processing
void process_atm_cell(ATM_Cell cell) {
    // 1. Lookup Routing Table based on Incoming Port & VPI/VCI
    ATM_Routing_Entry route = lookup_table(cell.port, cell.header.vpi, cell.header.vci);
    
    // 2. Error Check (HEC)
    if (calculate_crc8(cell.header) != cell.header.hec) {
        discard_cell(cell); 
        increment_error_counter();
        return;
    }

    // 3. Label Swapping (Core Mechanism)
    cell.header.vpi = route.vpi_out;
    cell.header.vci = route.vci_out;

    // 4. Congestion Control (CLP Check)
    if (is_congested(route.outgoing_port) && cell.header.clp == 1) {
        discard_cell(cell); // Low priority dropped
    } else {
        send_to_port(route.outgoing_port, cell);
    }
}
```

📢 **섹션 요약 비유**: ATM 스위칭 방식은 마치 고속철도 역에서 **"기차(셀)가 표(VPI/VCI)를 보이면, 역무원(스위치)이 복잡하게 물어볼 것 없이 바로 다른 선로로 전철기를 돌려주는 방식"**과 같습니다. 기차의 내용물이 무엇인지는 중요하지 않으며, 오직 표에 적힌 번호에 따라 기계적으로 경로를 바꿔주므로 처리 속도가 극도로 빠릅니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

ATM 기술은 단순한 전송 기술을 넘어 계층 간의 데이터를 적응시키는 **AAL (ATM Adaptation Layer)**이라는 독특한 계층을 통해 다양한 상위 프로토콜과 융합됩니다. 또한, 현대의 IP 네트워킹 기술인 MPLS와 기사적인 비교 분석이 필요합니다.

#### 1. AAL (ATM Adaptation Layer) 서비스 클래스 분석
상위 계층에서 온 데이터(SDU)를 ATM 계층이 처리할 수 있는 48바이트 페이로드(CS-PDU)로 변환하고, 수신측에서 다시 원래대로 복원하는 역할을 담당합니다.

**[표] AAL 클래스별 특성 및 비교 분석**

| 구분 | AAL1 | AAL2 | AAL5 (가장 널리 사용됨) | AAL3/4 |
|:---:|:---:|:---:|:---:|:---:|
| **대상 트래픽** | **CBR** (Constant Bit Rate) | **VBR** (Variable Bit Rate) | **VBR / UBR** (Data) | **Connectionless Data** |
| **핵심 예시** | 음성 전화, 비디오 회의 | 압축 영상 (MPEG) | **IP over ATM**, 이더넷 브리징 | SMDS (Switched Multimegabit Data Service) |
| **타이밍 특성** | 실시간성 매우 중요 | 실시간성 중요 | 비실시간 (Best Effort) | 비실시간 |
| **오류 제어** | 손실된 셀 복구 시도 | 손실된 셀 복구 시도 | 단순 오류 검출만 수행 | 순차 번호(SN) 사용 |
| **오버헤드** | 1바이트 (SNP, SNP) 포인터 사용 | 3바이트 (SN 필드) | 추가 오버헤드 없음 (SEAL) | 4바이트 (CRC-10 등) |
| **구조적 특징** | SAR(Service Specific) | SAR(Service Specific) | 단순화된 구조 (Simple and Efficient Adaptation Layer) | 복잡한 다중화 |

*   **AAL1**: 음성처럼 일정한 속도로 흘러가는 데이터를 위해 설계됨. 데이터가 유실되지 않도록 하기 위한 타이밍 정보를 포함.
*   **AAL5**: 오늘날의 인터넷 데이터 트래픽을 위해 주로 사용됨. 8바이트의 트레일러(Trailer)만 덧붙여 최대한 효율적으로 48바이트를 채움.

#### 2. 기술적 융합 심층 분석: ATM vs. IP (MPLS)

**[표] 패킷 교환(IP)과 ATM의 기술적 대조**

| 비교 항목 | IP (Internet Protocol) | ATM (Asynchronous Transfer Mode) |
|:---|:---|:---|
| **데이터 단위** | 가