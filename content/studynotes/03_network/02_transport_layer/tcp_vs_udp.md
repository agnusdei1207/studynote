+++
title = "TCP vs UDP (전송 계층 프로토콜)"
description = "OSI 7계층 중 전송 계층의 핵심인 TCP와 UDP의 내부 아키텍처, 3-Way Handshake, 혼잡 제어 메커니즘을 심도 있게 비교 분석합니다."
date = 2024-05-20
[taxonomies]
tags = ["Network", "Transport Layer", "TCP", "UDP", "Congestion Control"]
+++

# TCP vs UDP (전송 계층 프로토콜)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP와 UDP는 OSI 7계층의 전송 계층(Transport Layer)에서 동작하며, 종단 간(End-to-End) 애플리케이션 프로세스 간의 논리적 통신을 제공합니다. TCP는 연결 지향적이고 신뢰성 있는 바이트 스트림을 보장하는 반면, UDP는 비연결형으로 신뢰성을 포기하는 대신 극단적인 속도와 가벼운 오버헤드를 추구합니다.
> 2. **가치**: 이 두 프로토콜의 선택은 비즈니스 서비스의 성격을 결정짓습니다. 데이터의 무결성이 중요한 금융/웹 서비스(HTTP)는 TCP를 통해 패킷 유실 제로를 달성하며, 실시간성이 생명인 미디어 스트리밍이나 게임, IoT 센서 데이터 수집은 UDP를 통해 지연 시간(Latency)을 최소화합니다.
> 3. **융합**: 현대 네트워크는 양 극단의 한계를 극복하기 위해, UDP 위에서 TCP의 신뢰성을 애플리케이션 레벨로 이식한 QUIC(HTTP/3) 프로토콜로 진화하며 전송 계층의 패러다임을 근본적으로 혁신하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

**개념**  
전송 계층(Transport Layer)은 하위 계층(Network Layer, IP)이 제공하는 '호스트 간(Host-to-Host)의 불안정한 데이터 전달' 기능을 기반으로, 실제 데이터를 소비하는 '프로세스 간(Process-to-Process)의 통신'을 포트 번호(Port Number)를 통해 다중화(Multiplexing)하는 계층입니다. 
- **TCP (Transmission Control Protocol)**: 송신자와 수신자 간에 가상의 논리적 연결(Connection)을 확립하고, 순서 제어(Sequence), 오류 제어(Error), 흐름 제어(Flow), 혼잡 제어(Congestion) 메커니즘을 통해 데이터의 완벽한 도착을 보장하는 무거운(Heavy-weight) 프로토콜입니다.
- **UDP (User Datagram Protocol)**: 데이터 묶음(Datagram)에 출발지/목적지 포트 번호와 데이터 손상 여부를 확인하는 단순한 체크섬(Checksum)만 덧붙여 IP 계층으로 밀어 넣는, '던지고 잊어버리는(Fire-and-Forget)' 형태의 가벼운(Light-weight) 프로토콜입니다.

**💡 비유: 등기 우편(TCP)과 일반 엽서(UDP)**  
- **TCP (등기 우편)**: 발송자가 수신자에게 전화를 걸어 "지금부터 중요한 서류 100장을 보낼 테니 받을 준비 하세요(3-Way Handshake)"라고 확인합니다. 우체국은 각 서류에 번호를 매기고, 수신자가 특정 번호의 서류를 못 받았다고 연락하면 그 서류만 다시 복사해서 보내줍니다(재전송). 우체국의 배달망이 꽉 차면 하루에 보내는 양을 스스로 줄입니다(혼잡 제어). 무조건 도착하지만 시간이 오래 걸립니다.
- **UDP (일반 엽서)**: 친구의 주소(IP)와 우편함 번호(Port)만 적어서 우체통에 마구 집어넣습니다. 엽서가 중간에 비에 젖어 찢어지거나 배달부가 잃어버려도 아무도 신경 쓰지 않습니다(신뢰성 없음). 순서가 뒤죽박죽으로 도착할 수도 있습니다. 하지만 우체국에서 복잡한 확인 절차를 거치지 않으므로 전송 속도는 압도적으로 빠릅니다.

**등장 배경 및 발전 과정**  
1. **기존 기술의 치명적 한계점**: 초창기 인터넷(ARPANET)은 패킷 스위칭 네트워크로, 라우터 장애나 선로 노이즈로 인해 패킷이 유실(Drop)되거나 순서가 뒤바뀌어(Out-of-order) 도착하는 일이 빈번했습니다. 당시 애플리케이션 개발자들은 매번 네트워크의 이런 불안정성을 직접 코딩하여 복구해야 하는 끔찍한 오버헤드에 시달렸습니다.
2. **혁신적 패러다임 변화**: Vint Cerf와 Bob Kahn은 1974년 논문에서 네트워크의 복잡성을 하위 계층에 숨기고, 호스트의 운영체제가 신뢰성을 책임지는 TCP/IP 아키텍처를 제안했습니다. 초기에는 하나의 프로토콜이었으나, "모든 트래픽이 신뢰성을 필요로 하지는 않는다(예: 음성 통신)"는 철학에 따라 신뢰성을 보장하는 TCP와 다중화 기능만 제공하는 UDP로 분리(Decoupling)되었습니다.
3. **비즈니스적 요구사항**: 모바일 기기의 폭발적인 증가와 4K 비디오 스트리밍, 대규모 멀티플레이어 온라인(MMO) 게임 산업이 커지면서, TCP의 고질적인 Head-of-Line(HoL) Blocking(앞선 패킷이 유실되면 뒤의 패킷도 멈추는 현상)이 치명적인 병목으로 작용했습니다. 이에 따라 최근에는 구글 주도로 UDP 기반의 QUIC 프로토콜이 등장하여, 웹 생태계의 뼈대(HTTP/3)를 완전히 재구축하는 패러다임 전환이 일어나고 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

TCP와 UDP의 아키텍처적 차이는 헤더(Header) 구조와 연결을 관리하는 상태 머신(State Machine)의 유무에서 극명하게 갈립니다.

**구성 요소 (전송 계층 메커니즘)**

| 요소명 | 상세 역할 | 내부 동작 메커니즘 (TCP/UDP 적용) | 관련 필드/알고리즘 | 비유 |
|---|---|---|---|---|
| **Multiplexing / Demultiplexing** | 단일 IP 주소로 들어온 패킷을 적절한 애플리케이션 프로세스로 분배 | 소켓(Socket) 생성 시 할당된 출발지/목적지 Port 번호를 기반으로 바인딩 | Source/Destination Port 필드 | 아파트(IP)의 각 호실(Port) 우편함 |
| **Connection Management (TCP 전용)** | 통신 전/후에 논리적 파이프라인(세션)을 초기화 및 해제 | 연결 시 SYN, SYN-ACK, ACK 패킷 교환, 종료 시 FIN, ACK 교환 | 3-Way Handshake, 4-Way Handshake | 통화 시작 전 "여보세요?", 끊을 때 "끊을게" |
| **Reliable Data Transfer (TCP 전용)** | 패킷 손실, 훼손, 중복, 순서 바뀜을 감지하고 복구 | 수신 측은 누적 확인 응답(Cumulative ACK)을 보내고, 송신 측은 타임아웃 시 재전송 | Sequence Number, ACK Number, Retransmission Timer | 홈쇼핑 택배 배송 확인 서명 및 오배송 시 재발송 |
| **Flow Control (TCP 전용)** | 수신자의 메모리 버퍼가 넘치지 않도록 송신자의 전송 속도를 조절 | 수신자가 ACK에 자신의 남은 버퍼 크기(Window Size)를 담아 보냄 | Receive Window 필드, Sliding Window 알고리즘 | 물을 마시는 사람의 입 크기에 맞춰 물을 부어주는 속도 조절 |
| **Congestion Control (TCP 전용)** | 네트워크 전체(라우터 큐 등)의 붕괴를 막기 위해 송신량을 스스로 억제 | 패킷 유실을 네트워크 혼잡으로 간주하고 전송 창(Congestion Window, cwnd) 크기를 줄임 | Slow Start, AIMD, Fast Retransmit / Fast Recovery | 명절 고속도로 진입 램프 신호등(양재 IC 램프 미터링) |

**정교한 구조 다이어그램 (TCP 3-Way Handshake & 상태 전이)**

```ascii
========================================================================================
[ TCP Connection Establishment & Data Transfer Phase ]
========================================================================================

    [ Client (Active Open) ]                                   [ Server (Passive Open) ]
    State: CLOSED                                              State: LISTEN
         │                                                            │
         │ (1) SYN (seq=x, SYN=1)                                     │
         ├───────────────────────────────────────────────────────────▶│
   State: SYN_SENT                                                    │
         │                                                            │
         │ (2) SYN-ACK (seq=y, ack=x+1, SYN=1, ACK=1)                 │
         │◀───────────────────────────────────────────────────────────┤
         │                                                      State: SYN_RCVD
         │                                                            │
         │ (3) ACK (seq=x+1, ack=y+1, ACK=1)                          │
         ├───────────────────────────────────────────────────────────▶│
   State: ESTABLISHED                                           State: ESTABLISHED
         │                                                            │
========================================================================================
[ TCP Data Transfer with Sliding Window & Loss Recovery ]

         │ (4) Data Packet 1 (seq=x+1, len=100)                       │
         ├───────────────────────────────────────────────────────────▶│ Buffer: [x+1 ~ x+100]
         │ (5) Data Packet 2 (seq=x+101, len=100)  [LOST IN NETWORK] ✖│
         │ (6) Data Packet 3 (seq=x+201, len=100)                     │
         ├───────────────────────────────────────────────────────────▶│ Buffer: [Gap!] -> [x+201 ~ x+300]
         │                                                            │
         │ (7) DUP-ACK for Packet 2 (ack=x+101)                       │ (Server requests missing packet)
         │◀───────────────────────────────────────────────────────────┤
         │ (8) DUP-ACK for Packet 2 (ack=x+101)                       │
         │◀───────────────────────────────────────────────────────────┤
         │ (9) DUP-ACK for Packet 2 (ack=x+101)                       │
         │◀───────────────────────────────────────────────────────────┤
         │                                                            │
 [Fast Retransmit Triggered!]                                         │
 (3 DUP-ACKs received, don't wait for timeout)                        │
         │                                                            │
         │ (10) Retransmit Packet 2 (seq=x+101, len=100)              │
         ├───────────────────────────────────────────────────────────▶│ Buffer: [x+1 ~ x+300] Contiguous!
         │                                                            │
         │ (11) Cumulative ACK (ack=x+301)                            │
         │◀───────────────────────────────────────────────────────────┤
         ▼                                                            ▼
========================================================================================
```

**심층 동작 원리: TCP 혼잡 제어 (Congestion Control) 메커니즘**
TCP의 꽃이라 불리는 혼잡 제어는 패킷 드랍을 피드백으로 삼아 송신 속도(`cwnd`: Congestion Window)를 동적으로 조절하는 알고리즘(TCP Reno, Cubic, BBR 등)입니다.

① **Slow Start (지수적 증가)**: 연결 초기, `cwnd`를 1 MSS(Maximum Segment Size)로 시작합니다. ACK를 받을 때마다 `cwnd`를 1씩 증가시킵니다. 결과적으로 RTT(Round Trip Time)마다 `cwnd`는 1, 2, 4, 8로 **지수적(Exponential)**으로 폭발적으로 증가하여 가용 대역폭을 빠르게 탐색합니다.
② **Congestion Avoidance (가산적 증가)**: `cwnd`가 임계치인 `ssthresh`(Slow Start Threshold)에 도달하면, 혼잡 회피 단계로 진입합니다. 이때부터는 RTT마다 `cwnd`를 1 MSS씩만 증가시키는 **AIMD(Additive Increase Multiplicative Decrease)**의 가산적 증가를 수행합니다.
③ **Fast Retransmit & Fast Recovery (빠른 재전송/복구)**: 위 다이어그램처럼 수신자가 동일한 ACK를 3번 연속(3 Duplicate ACKs) 보내면, 송신자는 타임아웃(RTO)을 기다리지 않고 즉시 해당 패킷을 재전송합니다(Fast Retransmit). 이 경우 단순한 네트워크 지연이나 부분적 손실로 판단하여 `ssthresh`를 현재 `cwnd`의 절반으로 줄이고, `cwnd`도 절반으로 줄인 후(Multiplicative Decrease) 다시 가산적 증가를 시작합니다(Fast Recovery).
④ **Timeout (타임아웃, 심각한 혼잡)**: 만약 3 Dup-ACK조차 오지 않고 일정 시간(RTO)이 경과하면, 네트워크가 극심하게 붕괴되었다고 판단합니다. `ssthresh`를 절반으로 줄이지만, **`cwnd`는 자비 없이 1 MSS로 추락**시켜 Slow Start부터 다시 시작합니다.

**핵심 알고리즘 실무 예시: UDP 소켓 프로그래밍을 통한 커스텀 신뢰성 구현 (Python)**
UDP는 뼈대만 제공하므로, 실무에서 게임 서버나 WebRTC는 UDP 위에서 필요한 만큼만의 신뢰성(예: Sequence Number 부착 및 직접 재전송)을 직접 구현합니다.

```python
import socket
import struct
import time

# 커스텀 UDP 프로토콜: 4바이트 SeqNum + 데이터
# struct format: '!I' (네트워크 바이트 오더, Unsigned Int 4 bytes)
HEADER_FORMAT = '!I'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def run_udp_reliable_client(server_ip, server_port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2.0) # 재전송을 위한 타임아웃 설정
    
    seq_num = 1
    max_retries = 3
    
    # 1. 헤더(시퀀스 번호) + 데이터 결합
    packet = struct.pack(HEADER_FORMAT, seq_num) + message.encode('utf-8')
    
    for attempt in range(max_retries):
        try:
            print(f"[Attempt {attempt+1}] Sending Seq={seq_num}, Data={message}")
            # 2. UDP로 패킷 발송 (Fire)
            client_socket.sendto(packet, (server_ip, server_port))
            
            # 3. ACK 대기
            ack_data, _ = client_socket.recvfrom(1024)
            ack_num = struct.unpack(HEADER_FORMAT, ack_data[:HEADER_SIZE])[0]
            
            if ack_num == seq_num:
                print(f"[Success] Received ACK={ack_num} from Server")
                break
                
        except socket.timeout:
            print(f"[Timeout] Packet lost. Retransmitting Seq={seq_num}...")
            continue
    else:
        print("[Error] Max retries exceeded. Connection failed.")
        
    client_socket.close()

# [실무 시나리오]
# TCP의 무거운 3-Way Handshake 없이, 단일 패킷 단위로만 재전송을 보장하는 초경량 프로토콜 구현
# 게임 캐릭터의 좌표 이동 등 유실되어도 무방한 데이터는 ACK 없이 전송하고, 
# '아이템 획득' 같은 중요 이벤트만 위 코드를 통해 애플리케이션 레벨에서 ACK를 요구하도록 분기 처리함.
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: TCP vs UDP 엔터프라이즈 아키텍처 관점 분석**

| 비교 지표 (Metric) | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
|---|---|---|
| **연결성 (Connection)** | **Connection-oriented**. 통신 전 가상 회선 구축 필수 | **Connectionless**. 연결 설정 없이 즉시 전송 |
| **신뢰성 보장 메커니즘** | 순서 보장(Seq Num), 손실 복구(ACK/Retransmit), 데이터 무결성(Checksum) 등 100% 보장 | 체크섬(Checksum)만 존재. 유실, 순서 뒤바뀜, 중복 수신 모두 애플리케이션 책임 |
| **전송 오버헤드 (Header Size)** | **최소 20 Bytes** ~ 최대 60 Bytes. (복잡한 제어 필드 포함) | **고정 8 Bytes**. (Source Port, Dest Port, Length, Checksum이 전부) |
| **제어 로직 (Control Logic)** | 송신자와 네트워크 상태를 고려한 Flow Control / Congestion Control 내장 | 어떠한 제어 로직도 없음. 네트워크가 터지든 말든 최고 속도로 송출 |
| **전송 형태 (Data Paradigm)** | **Byte Stream**. 경계(Boundary)가 없음. 수신 시 버퍼에서 알아서 잘라 읽어야 함(Application Framing 필요) | **Datagram**. 메시지 경계가 명확함. 보낸 크기 그대로 수신됨 |
| **Head-of-Line Blocking** | 발생함. 앞 패킷이 유실되면 뒤 패킷이 도착했어도 애플리케이션에 전달 불가(대기) | **발생하지 않음**. 독립적인 데이터그램이므로 도착하는 즉시 처리 가능 |
| **주요 활용 비즈니스** | 웹(HTTP/1.1, HTTP/2), 파일 전송(FTP), 이메일(SMTP), 원격 접속(SSH) | 실시간 스트리밍(WebRTC, RTP), 멀티플레이어 게임, DNS 조회, SNMP |

**과목 융합 관점 분석 (Network × Security × OS)**
1. **Network × Security (DDoS 공격의 매개체)**:
   - **TCP SYN Flood**: 공격자가 위조된 IP로 대량의 SYN 패킷만 서버에 보내고 ACK를 응답하지 않습니다. 서버의 OS는 `SYN_RCVD` 상태로 연결 대기열(Backlog Queue)을 유지하다가 메모리가 고갈되어 서비스 거부 상태에 빠집니다. (해결책: SYN Cookie 기술 적용).
   - **UDP Amplification (증폭 공격)**: UDP의 '연결(Handshake) 없음'과 'IP 스푸핑(위조)의 용이성'을 악용한 공격입니다. 공격자가 자신의 IP를 타겟 서버의 IP로 위조한 뒤, NTP나 DNS 서버에 1바이트짜리 질의를 보냅니다. 취약한 서버는 타겟 IP로 수천 바이트의 응답(증폭)을 쏟아내어 타겟의 대역폭을 마비시킵니다.
2. **Network × OS (Zero-Copy와 커널 바이패스)**: 고성능 서비스에서는 TCP/IP 스택을 통과하며 발생하는 커널 버퍼와 유저 버퍼 간의 컨텍스트 스위칭 및 메모리 복사 오버헤드가 문제가 됩니다. 이를 해결하기 위해 OS는 `sendfile()` 같은 **Zero-Copy** API를 제공하거나, 아예 커널 스택을 우회하고 유저 스페이스에서 네트워크 카드를 직접 제어하는 **DPDK (Data Plane Development Kit)** 기술로 진화하여 100Gbps 이상의 회선 속도를 소화합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**기술사적 판단 (실무 시나리오)**
- **시나리오 1: 모바일 환경에서 HTTP/2(TCP) 기반 영상 서비스의 잦은 버퍼링**
  - **문제 상황**: 지하철이나 이동 중인 환경에서는 기지국 핸드오버(Handover)나 터널 진입 시 패킷 유실률(Packet Loss Rate)이 1~5%까지 치솟습니다. HTTP/2는 단일 TCP 커넥션 안에서 여러 스트림을 다중화하므로, 패킷 하나만 유실되어도 전체 스트림이 멈추는 **TCP HoL Blocking** 현상이 발생하여 심각한 버퍼링이 생깁니다.
  - **기술사적 의사결정**: 전송 계층 프로토콜을 TCP에서 **UDP 기반의 QUIC (HTTP/3)** 프로토콜로 마이그레이션해야 합니다. QUIC은 UDP 위에 구축되어 스트림 단위의 독립적인 에러 제어를 수행하므로, 스트림 A의 패킷이 유실되어도 스트림 B는 지연 없이 렌더링됩니다. 또한 0-RTT 핸드셰이크를 지원하여 초기 연결 지연을 극적으로 단축시킵니다.

- **시나리오 2: 초당 수백만 건의 IoT 센서 데이터를 수집하는 백엔드 아키텍처**
  - **문제 상황**: 수십만 대의 스마트팩토리 온도 센서가 1초마다 데이터를 전송. TCP를 사용할 경우 서버 측 소켓 File Descriptor 고갈 및 TCP 상태 머신 관리(TIME_WAIT 등)로 인한 메모리/CPU 오버헤드로 서버가 뻗음.
  - **기술사적 의사결정**: 센서 데이터의 특성상 100개 중 1~2개가 누락되어도 다음 초의 데이터로 보간(Interpolation)이 가능하므로, **과감하게 UDP 수집으로 전환**합니다. 대신 페이로드 내부에 타임스탬프와 센서 ID를 포함시켜, 서버(Application Layer)에서 순서 역전이나 중복을 필터링(Idempotency 보장)하도록 설계합니다.

**도입 시 고려사항 (체크리스트)**
- **기술적 고려사항 (TCP Tuning)**: 리눅스 커널에서 대용량 트래픽 처리 시 기본 TCP 버퍼 크기는 턱없이 작습니다. `/etc/sysctl.conf`를 튜닝하여 `net.core.rmem_max`, `net.ipv4.tcp_window_scaling` 등을 활성화하고 버퍼를 메가바이트 단위로 확장(BDP - Bandwidth Delay Product 최적화)해야 합니다. 고대역폭-고지연(LFN) 망에서는 BBR 같은 최신 혼잡 제어 알고리즘으로 커널 설정을 변경해야 합니다.
- **운영/보안적 고려사항 (방화벽 및 NAT 통과)**: 엔터프라이즈 방화벽(L4)은 상태(Stateful)를 추적합니다. TCP는 SYN/FIN을 통해 세션 상태를 명확히 알 수 있어 관리가 쉽지만, UDP는 상태가 없으므로 방화벽 통과(NAT Traversal, STUN/TURN/ICE)를 위한 별도의 홀펀칭(Hole Punching) 아키텍처 구축 비용이 발생합니다.
- **안티패턴 (Anti-patterns)**: 무조건 신뢰성이 중요하다고 실시간 화상회의(Zoom)의 음성 데이터까지 TCP로 전송하는 것은 최악의 설계입니다. 음성 데이터가 1초 뒤에 완벽하게 도착해봐야 아무 쓸모가 없습니다. 유실된 음성은 버리고 다음 음성을 재생하는 UDP 기반의 RTP가 정석입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량적/정성적 기대효과**
트래픽의 본질에 맞게 TCP와 UDP(혹은 QUIC)를 적재적소에 배치했을 때의 아키텍처 개선 효과입니다.

| 지표 | 레거시 아키텍처 (All TCP) | 최적화 아키텍처 (실시간 UDP/QUIC 도입) | 개선 효과 |
|---|---|---|---|
| **초기 연결 지연 (First Byte RTT)** | 3-RTT (TCP+TLS, 약 300ms) | 0-RTT ~ 1-RTT (약 50ms) | **초기 로딩 속도 80% 이상 단축** |
| **패킷 유실 시 지연 폭발** | HoL Blocking으로 인한 전체 화면 멈춤 | 독립 스트림 처리로 끊김 없는 재생 | **사용자 체감 품질(QoE) 극대화** |
| **서버 자원(Socket/Memory) 소모** | 연결 유지 오버헤드로 동접자 10만 한계 | 상태 없는 UDP 수신으로 무한대 확장 | **서버 인프라 비용 50% 절감** |

**미래 전망 및 진화 방향**
전송 계층의 미래는 **"커널 영역(TCP)에서 유저 영역(UDP 기반 커스텀 프로토콜)으로의 주도권 이동"**으로 요약됩니다. 과거 40년간 전송 계층의 절대 강자였던 TCP는 느린 커널 업데이트 주기와 경직된 헤더 구조(Middlebox Ossification)로 인해 혁신의 한계에 부딪혔습니다. 
구글과 IETF가 표준화한 **QUIC**은 UDP의 빈 껍데기를 활용하여 애플리케이션(유저 스페이스) 레벨에서 TCP의 신뢰성과 TLS 1.3의 보안성을 동시에 구현해 냈습니다. 향후 5년 내에 클라우드, 스트리밍, API 게이트웨이 간의 통신은 무거운 TCP 스택을 버리고 QUIC과 같은 차세대 UDP 기반 프로토콜로 완전히 대체될 전망입니다.

**※ 참고 표준/가이드**
- **RFC 793**: Transmission Control Protocol (TCP 원본 규격).
- **RFC 768**: User Datagram Protocol (UDP 원본 규격).
- **RFC 9000**: QUIC: A UDP-Based Multiplexed and Secure Transport.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [OSI 7계층 (OSI 7 Layer)](@/studynotes/03_network/01_network_fundamentals/osi_7_layer.md): TCP와 UDP가 동작하는 4계층 전송 계층의 상하위 역할 모델.
- [소켓 프로그래밍 (Socket API)](@/studynotes/03_network/_index.md): 애플리케이션에서 TCP/UDP를 호출하기 위한 인터페이스.
- [QUIC 프로토콜 (HTTP/3)](@/studynotes/03_network/_index.md): UDP 기반으로 TCP의 한계를 극복한 차세대 전송 프로토콜.
- [TCP 혼잡 제어 (Reno/Cubic/BBR)](@/studynotes/03_network/02_transport_layer/_index.md): 네트워크 붕괴를 막기 위한 심화 윈도우 조절 알고리즘.
- [네트워크 주소 변환 (NAT)](@/studynotes/03_network/02_transport_layer/_index.md): UDP가 NAT 환경을 통과하기 위해 필요한 STUN/TURN 메커니즘 연계.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **TCP는 뭐고 UDP는 뭔가요?**: 컴퓨터끼리 메시지를 주고받는 배달부들이에요. TCP는 '안전제일 등기우편'이고, UDP는 '스피드제일 일반엽서'랍니다.
2. **어떤 차이가 있나요?**: TCP는 배달 전에 수신자에게 전화를 걸고, 잃어버리면 다시 복사해서 100% 갖다 줘요. 하지만 UDP는 확인 전화도 없고 잃어버려도 무시한 채 엄청난 속도로 마구 던져요!
3. **언제 쓰나요?**: 절대 틀리면 안 되는 은행 돈 송금이나 웹사이트 접속에는 꼼꼼한 TCP를 쓰고, 중간에 좀 끊겨도 무조건 빨라야 하는 유튜브 라이브 영상이나 온라인 게임에는 쿨한 UDP를 쓴답니다.
