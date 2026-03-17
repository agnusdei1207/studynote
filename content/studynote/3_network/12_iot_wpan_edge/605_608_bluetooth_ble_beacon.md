+++
title = "605-608. 블루투스와 BLE 기술 분석"
date = "2026-03-14"
[extra]
category = "IoT & Edge"
id = 605
+++

# 605-608. 블루투스와 BLE 기술 분석

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단순한 Peripherals(주변기기) 연결을 넘어, 2.4GHz ISM Band를 기반으로 한 Ad-hoc(임시) 네트워킹과 극저전력 데이터 교환을 지원하는 WPAN(Wireless Personal Area Network) 표준.
> 2. **가치**: Classic Bluetooth는 고대역폭 오디오/데이터 전송의 편리성을, BLE(Bluetooth Low Energy)는 Coin Cell(코인 배터리)로 수년간 작동하는 에너지 효율성을 제공하여 IoT 생태계 확장의 핵심 인프라가 됨.
> 3. **융합**: 스마트폰의 중앙 제어(Hub) 역할과 Beacon 기술을 통한 실내 위치 기반 서비스(LBS), 그리고 Mesh 네트워킹을 통한 스마트 홈/빌딩 자동화까지 사물간 연결성의 범용 플랫폼으로 진화 중임.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 철학**
블루투스(Bluetooth)는 1994년 에릭슨(Ericsson)이 개발을 시작하여, 1998년 Bluetooth Special Interest Group (SIG, 블루투스 특별 interest 그룹)에 의해 표준화된 근거리 무선 통신 기술입니다. 본래 10세기 덴마크의 국왕 하랄드 블루투스(Harald Blåtand)가 스칸디나비아 반도를 통일한 역사적 사실에서 착안하여, 서로 다른 기기들을 '통일(연결)'한다는 의미를 담고 있습니다.

기술적으로는 IEEE 802.15.1 표준을 기반으로 하며, 2.4GHz ISM (Industrial, Scientific, and Medical) 대역을 사용합니다. 초기에는 RS-232 시리얼 케이블을 무선화하는 것(UART Cable Replacement)이 주 목적이었으나, 현재는 오디오 전송, 데이터 통신, 장치 제어 등 광범위한 영역을 아우릅니다.

**등장 배경: 유선의 굴레에서 벗어나다**
① **기존 한계**: 기기 간 연결을 위한 수많은 케이블(Infrared 포트는 직진성으로 인해 불편)과 IrDA(Infrared Data Association)의 높은 대기 전력 및 정렬 문제.
② **혁신적 패러다임**: 주파수 대역 공유 문제를 해결하기 위해 FHSS (Frequency-Hopping Spread Spectrum, 주파수 호핑 확산 스펙트럼) 기술을 도입하여 2.4GHz 대역의 혼잡함과 간섭을 극복하고, Ad-hoc 방식으로 즉석에서 네트워크(Piconet)를 구성하는 편리성 제공.
③ **현재 요구**: 단순 연결을 넘어 IoT 환경에서 배터리 효율이 극도로 중요해짐에 따라, Classic 블루투스와는 완전히 다른 프로토콜 스택을 가진 BLE가 등장하여 시장을 주도하게 됨.

**💡 비유**
블루투스는 마치 사람들이 모국어 없이도 수화(Handshake)로 즉시 대화를 시작할 수 있게 해주는 '보편적인 통역 관리자'와 같습니다.

**📢 섹션 요약 비유**
블루투스의 등장은 마치 복잡하게 꼬인 전화기 코드(유선)를 가위로 싹둑 잘라내고, 텔레파시(무선)로 자유롭게 대화하는 세상을 연 것과 같습니다. 서로 다른 기기들이 '약속된 주파수'라는 언어를 통해 수많은 방해(잡음) 속에서도 콩잡은 콩나무처럼 정확하게 소통하는 원리입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**구성 요소 (표)**
| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비고/비유 |
|:---|:---|:---|:---|
| **L2CAP** (Logical Link Control and Adaptation Protocol) | 데이터 다중화 및 세분화 | 상위 계층의 패킷을 적절한 크기로 쪼개서 ACL 링크로 전달. | 데이타 포장 |
| **SDP** (Service Discovery Protocol) | 서비스 검색 | 주변 기기가 제공하는 서비스(프린터, 오디오 등) 목록을 찾음. | 상품 목록 확인 |
| **RFCOMM** (Radio Frequency Communication) | 시리얼 포트 에뮬레이션 | RS-232 시리얼 케이블 대체. 가상의 COM 포트 생성. | 레거시 호환 |
| **HCI** (Host Controller Interface) | 호스트-컨트롤러 간 인터페이스 | 호스트(소프트웨어 스택)와 컨트롤러(하드웨어) 간의 명령 표준. | 운전자-엔진 연결 |
| **Link Manager** | 링크 설정 및 관리 | 인증, 암호화(Pairing), 전력 모드 제어 담당. | 경비 통제 |
| **Baseband** | 물리적 링크 제어 | FHSS 제어, 패킷 구성, 오류 정정(FEC). | 도로 포장 |

**네트워크 토폴로지 (Piconet & Scatternet)**
블루투스는 기본적으로 마스터(Master)-슬레이브(Slave) 구조를 가집니다.

1.  **Piconet (피코넷)**: 하나의 Master와 최대 7개의 Active Slave(활성 슬레이브)로 구성된 최소 통신 단위입니다. Master는 시간 슬롯(Time Slot Division Duplexing)을 할당하여 통신을 제어합니다.
2.  **Scatternet (스캐터넷)**: 특정 기기가 하나의 Piconet에서는 Master로, 다른 Piconet에서는 Slave로 동작하며(Bridge 역할), 두 개 이상의 Piconet을 연결하는 확장된 네트워크 형태입니다.

```ascii
      [블루투스 네트워크 토폴로지: Piconet과 Scatternet]

   (Device A)          (Device B)
    Slave 1             Slave 2
        \               /
         [  Master  ]  <------- Piconet 1
              |
        [ Bridge (Master/Slave) ]  <-- 두 망을 연결하는 다리
              |
      [  Master  ]                 <------- Piconet 2
        /      |      \
    Slave 3  Slave 4  Slave 5
```
*(도해 해설)*: 위 다이어그램은 Piconet A와 Piconet B가 중간 기기(Bridge)를 통해 Scatternet을 이루는 구조입니다. 중앙의 Bridge 기기는 Piconet 1에서는 Slave로 마스터의 명령을 듣지만, Piconet 2에서는 Master로서 슬레이브들을 제어하는 이중 역할을 수행합니다. 이를 통해 네트워크 규모를 확장할 수 있습니다.

**심층 동작 원리: AFH (Adaptive Frequency Hopping)**
블루투스는 2.4GHz 대역에서 1MHz 간격의 79개 채널(MHz)을 사용합니다. 전자레인지, 와이파이(Wi-Fi) 등의 간섭을 피하기 위해 AFH 기술을 사용합니다.
1.  송수신 쌍은 1,600회/초(Hop Rate)의 빠른 속도로 채널을 이동합니다.
2.  Master가 Hop Sequence(점프 순서)를 결정하고 Slave에게 알립니다.
3.  특정 채널에서 잡음(Noise)이 싫하면, 해당 채널을 Hop Sequence에서 제외(Blacklist)하고 깨끗한 채널만 사용하여 데이터 무결성을 보장합니다.

**핵심 알고리즘 및 코드 (연결 설정)**
```c
// Pseudo-code for Bluetooth Connection Logic
// [레거시 Classic Security Pairing 단계 예시]

struct BT_Device {
    u8 addr[6]; // BD_ADDR (48-bit MAC Address)
};

// 1. Inquiry (기기 검색)
void inquiry_devices() {
    // Inquiry Access Code (IAC)를 broadcast로 송신
    // 주변 기기(FHS 패킷)로부터 응답 수집
}

// 2. Page (연결 요청)
void connect_to_device(u8* target_addr) {
    // Page Scan 모드인 타겟에게 ID 패킷 전송
    // Clock Offset 정보를 이용해 빠르게 동기화
    establish_link(target_addr);
}

// 3. Link Key Exchange (인증 및 키 생성)
u16 link_key = generate_E0_key(pin_code, random_number);
if (authenticate(link_key) == SUCCESS) {
    encryption_mode = ON;
}
```
*(해설)*: 실무 코드에서는 HCI Commands를 소켓 인터페이스를 통해 전송합니다. 연결 과정은 Inquire(탐색) -> Page(호출) -> Link Setup(링크 설정) -> LMP(Link Manager Protocol) negotiation(협상) -> Service Search(서비스 검색) 순으로 진행되며, 이 과정에서 Security Handler가 개입하여 Pairing(페어링)을 수행합니다.

**📢 섹션 요약 비유**
피코넷 구조와 호핑 기술은 마치 복잡한 **교차로와 신호등 시스템**과 같습니다. 마스터는 능숙한 교통경찰관이 되어 7명의 행인(슬레이브)에게 순서대로 보행 신호를 주어 질서를 유지하고, 1,600번 쏘카쏘카 튀어 다니는 호핀은 **축구 선수가 상대 수비수(Wi-Fi/전자레인지)를 피해 드리블하여 골(데이터 전송)을 성공시키는 동선**과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

블루투스 기술은 크게 **Classic Bluetooth (BR/EDR)**와 **Bluetooth Low Energy (BLE)**로 나뉩니다. 이 둘은 물리적 계층(파장)은 같으나 프로토콜 스택이 완전히 상이합니다.

**심층 기술 비교표**

| 구분 | Classic Bluetooth (BR/EDR) | Bluetooth Low Energy (BLE) |
|:---|:---|:---|
| **전체 명칭** | Bluetooth Basic Rate / Enhanced Data Rate | Bluetooth Low Energy |
| **목적** | 대용량 데이터 스트리밍 (오디오, 파일) | 초저전력 작은 데이터 패킷 전송 |
| **대역폭** | 1~3 Mbps (높음) | 1 Mbps (낮음) |
| **연결 유지** | 항상 연결 유지 (Continuous) | 간헐적 연결 (Intermittent) |
| **대기 시간** | 짧음 (Real-time 가능) | 상대적으로 김 (하지만 Connection Event 주기로 조절) |
| **전력 소모** | 높음 (와트(W) 단위) | 극히 낮음 (밀리와트(mW) 이하) |
| **채널 수** | 79 channels (1MHz 간격) | 40 channels (2MHz 간격, 3개 광고 채널) |
| **패킷 크기** | 큰 패킷 지원 | 매우 작은 패킷 (최대 257 Byte) |
| **대표 프로파일** | A2DP, SPP, HFP | GATT, GAP, Beacon |
| **심층 기술** | SCO(Synchronous Connection-Oriented) 링크 사용하여 음성 전용 채널 보장 | Connection Interval을 ms 단위로 설정하여 Sleep 모드 유지 |

**과목 융합 관점 (OS, Network, HW)**
*   **Network & HW**: BLE의 **Advertising(광고)** 메커니즘은 TCP/IP의 Handshake와 달리 Connectionless입니다.广播 패킷을 지속적으로 쏘는 것은 UDP의 Unreliable 특성과 유사하지만, 물리적으로는 주기적으로 깨어나므로 전력 제어가 가능합니다.
*   **OS**: 모바일 OS(Android/iOS)에서는 BLE 장치를 스캔할 때 시스템 레벨에서 중복 필터링을 수행하여 배터리를 아끼고, Foreground/Background 상태에 따라 스캔 주파수를 다르게 적용하는 정책을 가집니다.

**비교 ASCII 다이어그램: Duty Cycle**

```ascii
   [Classic vs BLE: Duty Cycle 비교]

   Classic (Keep-Alive)
   |---------|---------|---------| (높은 전력 소모)
    ^       ^         ^
   TX/RX   TX/RX     TX/RX

   BLE (Deep Sleep & Burst)
   |  |                       |  |       (매우 낮은 전력 소모)
   Active (3ms)  Sleep (100ms)  Active
```
*(도해 해설)*: Classic 블루투스는 연결되어 있는 동안 계속 전파를 주고받거나(RX) 대기 상태를 유지하기 위해 전력을 소모합니다. 반면 BLE는 99% 이상을 Deep Sleep 상태로 보내다가, 정해진 때(Connection Interval)에만 잠깐 깨어나 데이터를 폭발적으로(Burst) 보내고 다시 잠듭니다. 이 '휴면의 비율'이 곧 배터리 수명을 결정합니다.

**📢 섹션 요약 비유**
Classic과 BLE의 관계는 **'기차'와 '택시'의 차이**와 같습니다. Classic 블루투스는 많은 사람(데이터)을 태우고 정해진 선로(연결 유지)를 달리는 기차라 연료가 많이 들지만, 택시(BLE)는 손님이 부를 때만 출동하고 손님이 내리면 차를 끄고 대기하기 때문에 연료 효율이 훨씬 높습니다. 혹은 **물을 긷는 펌프(Classic)**와 **물을 뿌리는 분무기(BLE)**의 차이로 볼 수도 있습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**실무 시나리오: IoT 센서 네트워크 구축**

*   **상황 1: 공장 내 설비 진동 센서 (300ms 주기, 20Byte 데이터)**
    *   **의사결정**: BLE **Mesh** 네트워크 채택.
    *   **이유**: 배터리 교체가 어려운 구석진 곳의 센서는 전력 소모가 적어야 함. 중계기 역할을 하는 노드들이 신호를 릴레이하여 전파 도달 거리를 확장할 수 있음. Wi-Fi는 전력 소모가 너무 크고, Zigbee는 별도의 게이트웨이가 필요함. 스마트폰과의 호환성을 고려하여 BLE 선택.

*   **상황 2: 고음질 무선 이어폰 (T