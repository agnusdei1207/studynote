+++
title = "233-236. 이더넷 프레임 구조 (Ethernet Frame)"
date = "2026-03-14"
[extra]
category = "LAN/WAN & L2 Devices"
id = 233
+++

# 233-236. 이더넷 프레임 구조 (Ethernet Frame)

## # 이더넷 프레임 구조 (Ethernet Frame Structure)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 현대 LAN (Local Area Network)의 사실상 표준인 **Ethernet II (DIX 2.0)** 프레임은 물리 계층의 비트 열을 신뢰할 수 있는 데이터 링크 계층의 단위로 캡슐화하는 표준화된 컨테이너입니다.
> 2. **가치**: 48비트 MAC 주소 체계를 통한 정확한 송수신 지정과 **CRC-32 (Cyclic Redundancy Check)** 기반의 무결성 검증을 통해, 물리적인 신호 노이즈 환경에서도 **99.9999% 이상의 오류 없는 데이터 전송**을 보장합니다.
> 3. **융합**: L2 스위칭의 핵심 매커니즘이자 TCP/IP 스택의 IP 패킷을 운반하는 기본 트레일러로서, **Jumbo Frame** 기술을 통한 데이터 센터 효율화와 **VLAN Tagging**을 통한 가상화 네트워크 분리의 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

이더넷 프레임은 OSI 7계층 모델 중 **Data Link Layer (데이터 링크 계층, L2)**의 PDU (Protocol Data Unit)로, 상위 계층의 데이터 패킷이 물리적 매체(케이블, 광섬유)를 통해 전송되기 위해 겪어야 할 필수 포맷입니다. 본질적으로 이더넷은 **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)** 기반의 버스형 토폴로지에서 시작했으나, 현재는 스위칭 기술의 발전으로 **Full-Duplex (전이중)** 통신 방식이 주류입니다. 이에 따라 충돌 감지를 위한 최소 프레임 크기 제한은 완화되었으나, 하위 호환성을 위해 여전히 표준 규격은 유지되고 있습니다.

#### 💡 비유
이더넷 프레임은 기차의 화물 컨테이너와 같습니다. 내용물이 무엇이든(문서, 음성, 영상), 기차로 운반하려면 표준화된 형태의 컨테이너에 담아야 하며, 이 컨테이너에는 목적지와 출발지 정보가 반드시 부착되어야 분류실(스위치)에서 처리할 수 있습니다.

#### 등장 배경
① **기존 한계**: 초기 네트워크는 각 사마다 독자적인 케이블링과 신호 방식을 사용하여 호환 불가 문제 발생.
② **혁신적 패러다임**: 1980년대 Xerox, DEC, Intel이 공동 개발한 **DIX Ethernet** 표준이 등장하고, 이후 IEEE 802.3 위원회를 통해 산업 표준화.
③ **현재의 비즈니스 요구**: 1Gbps~400Gbps를 넘나드는 초고속 네트워크 환경에서 프레임 처리 오버헤드를 최소화하면서도 다양한 프로토콜(IP, ARP, MPLS 등)을 식별할 수 있는 유연한 구조가 요구됨.

📢 **섹션 요약 비유**: 마치 도로를 달리는 모든 차량이 특정한 **자동차 등록 번호판(MAC 주소)**과 **차종(EtherType)**을 부착하고 일정한 **차체 크기(MTU)** 규정을 준수해야 고속도로(인터넷)에 진입할 수 있는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
이더넷 프레임은 크게 MAC 헤더, 페이로드, FCS로 나뉘며, 앞부분에는 물리적 동기를 위한 Preamble이 추가됩니다.

| 구성 요소 (Component) | 크기 (Size) | 역할 및 내부 동작 | 비고 (Note) |
|:---|:---:|:---|:---|
| **Preamble (프리앰블)** | 7 Bytes | **물리적 동기화**: 수신측 NIC(Network Interface Card)가 신호를 감지하고 클럭을 동기화하기 위한 `10101010` 패턴 반복. | OSI 모델의 물리 계층에서 처리되어 캡처 툴에 미노출. |
| **SFD (Start Frame Delimiter)** | 1 Byte | **프레임 시작 알림**: `10101011` 패턴으로, Preamble과 구분되는 프레임의 실제 시작점을 명시. | |
| **Destination MAC** | 6 Bytes | **수신 주소**: 최종 목적지 MAC 주소. L2 Multicast/Broadcast 주소도 포함. | FF:FF:FF:FF:FF:FF는 브로드캐스트. |
| **Source MAC** | 6 Bytes | **송신 주소**: 프레임을 전송한 NIC의 고유 주소. | 스위치가 MAC 주소 테이블을 학습하는 데 사용. |
| **EtherType** | 2 Bytes | **상위 프로토콜 식별자**: Payload가 감싸고 있는 데이터의 종류를 식별. | 0x0800(IPv4), 0x86DD(IPv6), 0x8100(802.1Q VLAN). |
| **Payload (데이터)** | 46~1500 Bytes | **실제 데이터**: L3 계층의 패킷(IP)을 포함. | 1500 Bytes를 초과하면 Jumbo Frame or Fragmentation 필요. |
| **Padding (채움)** | 0~46 Bytes | **최소 크기 보장**: 전체 프레임이 64 Bytes 미만이면 0x00으로 채워 CSMA/CD 최소 크기 충족. | Full-Duplex 환경에서도 계산 로직상 존재. |
| **FCS (Frame Check Sequence)** | 4 Bytes | **무결성 검증**: 전체 프레임에 대한 CRC-32 값을 포함하여 전송 중 오류 검출. | 수신측에서 계산 값이 상이하면 프레임 폐기(Drop). |

#### 2. ASCII 구조 다이어그램
아래 다이어그램은 **Ethernet II** 프레임의 비트 단위 구조와 전송 순서를 시각화한 것입니다.

```ascii
+-----------------------------------------------------------------------------+
|                    [Ethernet II Frame Structure]                            |
+-----------------------------------------------------------------------------+
|  Physical Layer Sync (Not visible in Sniffing)                              |
+-----------------------------------------------------------------------------+
| Preamble (7B) | SFD (1B) | Dest MAC (6B) | Src MAC (6B) | Type (2B)         |
| 10101010...   | 10101011 | AA:BB:CC:...  | DD:EE:FF:... | 0x0800           |
+---------------+----------+---------------+--------------+-------------------+
| Payload (Data) + Padding (46 ~ 1500 Bytes)                                 |
| +-----------------------------------------------------------------------+   |
| |           IP Packet / ARP Packet etc. (Network Layer)                |   |
| +-----------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------+
| FCS (4B)                                                                    |
| [CRC-32 Error Check]                                                        |
+-----------------------------------------------------------------------------+
<------------------------- Minimum 64 Bytes ------------------------>
<------------------------------------- Maximum 1518 Bytes -------------------------------->
```

#### 3. 심층 동작 원리 및 알고리즘
이더넷 프레임 처리 과정은 송신과 수신으로 나뉘며, 특히 **FCS 계산**은 데이터 무결성의 핵심입니다.

**① CRC-32 (Cyclic Redundancy Check) 생성 다이어그램**
송신 NIC는 프레임을 전송하기 직전, 전체 비트 스트림에 대해 다항식 나눗셈 연산을 수행하여 나머지 값을 FCS 필드에 삽입합니다.

```text
Data Bits (D(x)) + Divisor (Generator Polynomial, G(x))
      |
      v
[  Bitwise XOR Shift Operation  ]
      |
      v
CRC Value (Remainder R(x)) --> Appends to Frame Tail
```
*(수식: $F(x) = x^{32} + x^{26} + x^{23} + ... + 1$)*

**② 수신 처리 로직 (의사코드)**
수신측 스위치나 NIC는 다음과 같은 로직으로 프레임의 유효성을 판단합니다.

```python
def process_ethernet_frame(raw_bits):
    # 1. 물리적 동기화 확인 (Preamble/SFD 제거)
    if not detect_sfd(raw_bits):
        return ERROR_PHYSICAL_SYNC
    
    # 2. 비트 스트림에서 MAC 헤더와 페이로드, FCS 분리
    dest_mac, src_mac, ethertype, payload, received_crc = parse_frame(raw_bits)
    
    # 3. CRC-32 무결성 검증 (FCS 제외한 나머지 부분으로 재계산)
    computed_crc = calculate_crc32(raw_bits_without_fcs)
    
    if computed_crc != received_crc:
        # CRC Mismatch 발생 시 프레임 폐기 ( silently dropped )
        increment_interface_counter("crc_error")
        return DROP_FRAME
    
    # 4. MAC 주소 필터링 (내 주소 또는 브로드캐스트/멀티캐스트 여부 확인)
    if dest_mac not in [my_mac, broadcast_mac, multicast_macs]:
        return DROP_FRAME
    
    # 5. EtherType을 확인하여 상위 계층(Routing Engine or Protocol Stack)으로 전달
    upper_layer_payload = decapsulate_payload(payload)
    deliver_to_upper_layer(ethertype, upper_layer_payload)
```

📢 **섹션 요약 비유**: 마치 귀중품이 배송될 때, 물건을 포장한 뒤 **봉인 테이프(FCS)**를 붙이고, 택배사에서는 이 봉인이 훼손되지 않았는지 확인하여 배송하는 과정과 같습니다. 내용물(Payload)이 아무리 비싸도 봉인이 뜯어져 있으면(오류) 수령을 거부합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

이더넷 프레임 구조는 단순한 데이터 패킷이 아니라, 네트워크 전체의 성능과 보안, 그리고 상위 프로토콜과 직결되는 중요한 요소입니다.

#### 1. Ethernet II vs IEEE 802.3 (Raw vs SNAP)
과거와 현재의 표준을 비교하고, 왜 현재가 선택되었는지 분석합니다.

| 비교 항목 | **Ethernet II (DIX 2.0)** | **IEEE 802.3 (Raw/SNAP)** |
|:---|:---|:---|
| **타입 필드 (2 Bytes)** | **EtherType** 사용 (값 > 1500) | **Length** 사용 (값 ≤ 1500) |
| **데이터 식별 방식** | 필드 값 자체로 상위 프로토콜(IP, ARP) 식별 | Length 뒤에 **LLC (Link Layer Control)** 헤더나 SNAP 헤더를 붙여 식별 |
| **TCP/IP 친화성** | ⭐⭐⭐⭐⭐ (매우 높음) | ⭐⭐ (복잡함, 오버헤드 유발) |
| **현재 사용률** | **99.9% (사실상 표준)** | 거의 사용되지 않음 (구형 장비) |

> **📌 기술사적 판단**: TCP/IP 스택의 지배력이 강해지면서, 불필요한 LLC 헤더 제거를 위해 **Ethernet II가 표준으로 자리 잡았습니다.**

#### 2. 과목 융합 분석 (OS, 컴구, 보안)

**① [OS & 컴퓨터 구조] MTU와 Fragmentation의 상관관계**
- **L2 MTU (Maximum Transmission Unit)**: 이더넷 프레임의 기본 페이로드가 **1500 Bytes**로 제한되어 있습니다.
- **L3 IP Datagram**: IP 패킷이 1500 Bytes를 넘어서면, 운영체제의 네트워크 스택은 이를 **Fragmentation (분절)** 시켜야 합니다.
- **성능 영향**: 분절은 라우터와 호스트의 CPU 부하를 유발하며(재조립 비용), **TCP MSS (Maximum Segment Size)** 조정을 통해 가능한 L2에서 분절이 발생하지 않도록 조율해야 합니다.

**② [보안] MAC Spoofing과 Sniffing**
- **무결성 결함**: FCS는 단순한 오류 검출용이지 보안용 인증이 아닙니다. 공격자가 소프트웨어적으로 **Source MAC**을 위조(Spoofing)하더라도 FCS를 재계산하여 우회할 수 있습니다.
- **Sniffing**: 허브 환경이나 ARP Spoofing 공격 시, 목적지가 자신이 아니더라도 NIC는 **Promiscuous Mode(혼합 모드)**로 설정하여 모든 프레임을 읽을 수 있습니다. 이는 **IEEE 802.1X(포트 보안)** 기술로 방어해야 합니다.

📢 **섹션 요약 비유**: 이더넷 프레임의 1500바이트 제한은 **고속도로의 터널 높이 제한**과 같습니다. 터널(L2)보다 높은 짐을 싣은 트럭(IP 패킷)은 무조건 높이를 낮추기 위해 잘려야(Fragmentation) 하므로, 처음부터 터널 높이에 맞춰 짐을 싣는 것이(MSS 조정) 효율적인 운송입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

네트워크 설계 시 이더넷 프레임 구조를 이해하면 성능 병목 현상을 해결하고 비용을 절감할 수 있습니다.

#### 1. 실무 시나리오 및 의사결정 프로세스

**Scenario 1. 데이터베이스 서버 간 전송 속도 저하**
*   **상황**: DB 서버 백업 시 1Gbps 링크를 꽉 채우는데도 처리량이 만족스럽지 않음.
*   **원인 분석**: 1Gbps 대역폭을 초당 약 81,000개의 프레임(약 12,000pps)을 처리해야 함. 각각의 프레임마다 **Interrupt(인터럽트)**와 **Memory Copy**가 발생하여 CPU 오버헤드가 폭증함.
*   **해결 전략 (Jumbo Frame)**:
    *   **결정**: MTU를 1500에서 **9000 Bytes**로 증설 (Jumbo Frame 활성화).
    *   **효과**: 같은 양의 데이터를 전송할 때 프레임 수가 1/6로 감소. CPU 오버헤드와 헤더 오버헤드가 획기적으로 줄어듦.

#### 2. 도입 체크리스트

| 구분 | 체크 항목 | 설명 |
|:---|:---|:---|
| **기술적** | **MTU Mismatch** | 경로 상의 장비들(L2/L3 스위치, 방화벽)이 동일한 MTU(1500 또는 9000)를 지원하는지 확인. |
| **성능** | **Rate Limiting** | L2 스위치