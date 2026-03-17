+++
title = "405-406. TCP와 UDP의 특징 비교"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 405
+++

# 405-406. TCP와 UDP의 특징 비교

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP는 **연결 지향형(Connection-Oriented)** 프로토콜로 신뢰성과 순서 보장을 최우선으로 하며, UDP는 **비연결형(Connectionless)** 프로토콜로 처리 지연(Latency) 최소화를 추구합니다.
> 2. **가치**: TCP는 패킷 손실率为 0에 수렴하게 하여 데이터 무결성을 보장하지만 오버헤드가 크고, UDP는 약간의 손실을 감수하며 실시간 스트리밍에서 초당 프레임 전송률(FPS)을 극대화합니다.
> 3. **융합**: 최근 인터넷 트래픽 변화(QUIC 등)에 따라 TCP의 혼잡 제어 알고리즘을 UDP 위에 구현하여 신뢰성과 속도를 동시에 확보하는 하이브리드 형태로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)
### 개념 및 철학
전송 계층(Transport Layer, Layer 4)은 송수신 호스트의 프로세스 간 논리적 통신을 담당합니다. 이 계층의 핵심 과제는 '데이터를 빠르게 보낼 것인가(Throughput)', '안전하게 보낼 것인가(Reliability)' 사이의 트레이드오프(Trade-off)를 해결하는 것입니다.

*   **TCP (Transmission Control Protocol)**: 인터넷 프로토콜 스택의 표준 신뢰성 프로토콜입니다. 데이터의 정확한 전송을 위해 상호 합의(Handshaking) 과정을 거치며, 패킷이 분실되거나 손상되었을 때 이를 복구하는 메커니즘을 내제하고 있습니다.
*   **UDP (User Datagram Protocol)**: 최소한의 기능만을 제공하는 가벼운 프로토콜입니다. 데이터를 보내기 위해 연결을 설정하거나 상태를 유지하지 않으며, 수신 여부와 관계없이 데이터를 즉시 전송하는 '화이어 앤 포겟(Fire and Forget)' 방식을 채택합니다.

### 등장 배경 및 기술적 패러다임
1.  **기존 한계**: 초기 네트워크에서는 회선 교환 방식처럼 무결성이 보장되어야 했으나, 패킷 교환 환경에서는 네트워크 혼잡으로 인한 패킷 손실이 빈번했습니다.
2.  **혁신적 패러다임**: TCP는 ARQ(Automatic Repeat reQuest) 기술을 도입하여 끊김 없는 데이터 스트림을 제공하고, UDP는 멀티미디어 데이터처럼 '조금의 깨짐은 허용하되 지연은 없어야 하는' 트래픽의 등장으로 각광받게 되었습니다.
3.  **현재의 비즈니스 요구**: 5G/6G 시대로 넘어가며 초저지연(Ultra-Low Latency) 통신이 중요해지면서, TCP의 무거운 핸드셰이크를 개선한 QUIC(Quick UDP Internet Connections)처럼 UDP 기반의 신뢰성 프로토콜이 새로운 표준으로 자리 잡고 있습니다.

### 💡 개요 섹션 비유
전송 계층의 선택은 마치 물건을 배송할 때 '등기 우편(TCP)'을 보낼지, '일반 소포(UDP)'를 보낼지, 아니면 '현관문에 던지고 전단지(UDP)'를 날릴지 선택하는 것과 같습니다. 목적물의 중요도와 시급성에 따라 배송 방식의 무게와 비용이 결정됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
### 1. 구성 요소 및 동원 기술
전송 계층 프로토콜의 신뢰성과 효율성을 결정짓는 5가지 핵심 모듈은 다음과 같습니다.

| 요소 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 관련 프로토콜/기술 |
|:---|:---|:---|:---|
| **다중화 (Multiplexing)** | 여러 애플리케이션 데이터 구분 | **Port Number**를 사용하여 하나의 IP 주소에서 여러 세션 분리 | Sockets API |
| **Connection Mgmt** | 통신 회선 설정 및 해제 | **3-Way Handshake** (SYN/SYN-ACK/ACK) 및 4-Way Handshake | TCP Flags (SYN, FIN, ACK) |
| **Seq/ACK Num** | 순서 보장 및 분실 감지 | 모든 바이트에 번호를 부여하고, 수신 측은 다음 받을 번호를 알림 | TCP Header, Sliding Window |
| **Flow Control** | 송신 과잉 방지 | 수신 버퍼의 여유 공간(Window Size)을 송신 측에 피드백 | Receiver Window (rwnd) |
| **Congestion Control** | 네트워크 혼잡 회피 | 네트워크 상태에 따라 전송 속도(CWND)를 동적으로 가감 | AIMD (Additive Increase/Multiplicative Decrease) |

### 2. 프로토콜 스택 구조 및 캡슐화
TCP와 UDP는 IP 계층의 바로 상위에 위치하며, PDU(Protocol Data Unit) 단위가 서로 다릅니다.

```ascii
      +-----------------------+
      |   Application Layer   |  (HTTP, FTP, DNS...)
      +-----------------------+
              |     |
    +---------+     +---------+
    |   TCP (Segment)      UDP (Datagram) |
    | [可靠性 고비용]      [신속성 저비용] |
    +---------+     +---------+
              |     |
      +-----------------------+
      |    IP Layer (Packet)  |
      +-----------------------+
```
**(해설)**: TCP는 세그먼트(Segment) 단위로 데이터를 잘라 보내며, 헤더에 20바이트 이상의 제어 정보(번호, 윈도우 등)를 포함합니다. 반면 UDP는 데이터그램(Datagram) 단위로 8바이트의 헤더만을 붙여 최대한 빠르게 IP 계층으로 내보냅니다.

### 3. 핵심 동작 메커니즘 (TCP의 신뢰성)
TCP는 **Positive ACK with Retransmission**과 **Sliding Window** 메커니즘을 통해 신뢰성을 확보합니다.

```ascii
[Sliding Window를 통한 신뢰성 전송 예시]

송신자 (A)                                        수신자 (B)
   |                                               |
   | ---[1. Seq: 1, Len: 100 Bytes]---------------> | (수신 완료, ACK: 101 대기)
   | <---[2. ACK: 101, Win: 400]------------------- | (버퍼 여유 있음)
   | ---[3. Seq: 101, Len: 100 Bytes]------------> |
   | ---[4. Seq: 201, Len: 100 Bytes]------------> | (전송 중)
   | ---[5. Seq: 301, Len: 100 Bytes]------------> | (전송 중)
   |                X                              | [Packet Loss 발생!]
   | <---[3. Dup ACK: 202]------------------------ | (중복 확인응답 - 빠른 재전송 유도)
   | <---[4. Dup ACK: 202]------------------------ |
   | ---[5. Fast Retransmit: Seq: 202]----------> | (타이머 기다리지 않고 즉시 재전송)
   | <---[6. ACK: 401]--------------------------- | (순서 맞춰 정상 수신)
```
**(해설)**:
1.  **연결 설정**: 3-Way Handshake로 양쪽의 Initial Sequence Number(ISN)를 동기화합니다.
2.  **데이터 전송**: Sequence Number로 데이터의 순서를 부여하고, ACK 번호로 다음 받아야 할 데이터를 명시합니다.
3.  **혼잡 제어 (Reno/Cubic)**: 네트워크가 혼잡하다고 판단되면(3번의 중복 ACK 또는 타임아웃), 윈도우 크기를 절반으로 줄이는 AIMD 방식으로 대응합니다.
4.  **UDP 동작**: 위의 복잡한 과정 없이, 송신자는 그냥 Datagram을 목적지 Port로 쏘고 끝입니다.

### 4. 핵심 수식 및 코드 스니펫
네트워크 대역폭 효율을 결정하는 TCP 윈도우 크기 계산은 다음과 같습니다.

```python
# TCP Throughput Calculation (Bandwidth-Delay Product)
def calculate_max_throughput(rtt_sec, window_size_bytes):
    """
    TCP 윈도우 기반 최대 처리량 계산
    """
    # Throughput = Window Size / RTT
    # RTT (Round-Trip Time)가 클수록 윈도우를 크게 잡아야 같은 성치을 낸다.
    throughput_bps = (window_size_bytes * 8) / rtt_sec
    return throughput_bps

# Example: RTT 100ms (0.1s)에 64KB Window일 경우
# -> (65536 * 8) / 0.1 = 5,242,880 bps (약 5.24 Mbps)
```
**(해설)**: 지연 시간(Latency)이 긴 위성 통신이나 장거리 네트워크(LFN, Long Fat Network)에서는 신뢰성을 유지하려면 Window Scaling 옵션을 통해 버퍼 크기를 기하급수적으로 늘려야 병목이 발생하지 않습니다.

### 📢 섹션 요약 비유
**TCP**는 '고속도로 톨게이트'와 같습니다. 진입 전에 통행료(Handshake)를 내고, 차량이 막히면 속도를 줄이고(Congestion Control), 사고가 나면 보험 처리를 합니다. 반면 **UDP**는 '자전거 도로'나 '시골길'과 같습니다. 톨게이트도 없고, 신호등 없이 자유롭게 질주하지만, 중간에 도로가 공사 중이거나 구멍이 나도 알 방법이 없습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
### 1. TCP vs UDP 심층 기술 비교
단순한 기능 비교를 넘어, 실무 설계 시 영향을 미치는 정량적 지표를 분석합니다.

| 비교 항목 (Criteria) | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
|:---|:---|:---|
| **연결성 (Connection)** | **연결 지향형** (Virtual Circuit 생성)<br>Stateful (상태 유지 필요) | **비연결형** (Datagram 발사)<br>Stateless (상태 유지 안 함) |
| **신뢰성 (Reliability)** | **높음 (High)**<br>- 재전송(Retransmission)<br>- 순서 보장(Sequencing)<br>- 오류 검출(Checksum) | **낮음 (Low)**<br>- 최선의 노력(Best Effort)<br>- 순서 보장 없음<br>- 수신 확인 없음 |
| **오버헤드 (Overhead)** | **높음 (High)**<br>헤더 20~60바이트 (Options 포함)<br>Connection setup 시간 소요 | **낮음 (Low)**<br>헤더 고정 8바이트<br>설정 비용 0 |
| **흐름 제어 (Flow Control)** | O (Sliding Window) | X (Application Layer에 의존) |
| **전송 속도 (Speed)** | 느림 (제어 로직 지연 발생) | **매우 빠름** (Latency 최소화) |
| **브로드캐스트 (Broadcast)** | 불가능 (Unicast Only) | 가능 (Broadcast, Multicast 지원) |
| **대표 사용처** | HTTP/HTTPS, SSH, FTP, SMTP | DNS, VoIP, Streaming, Online Gaming |

### 2. 과목 융합 관점 (OS/보안과의 시너지 및 오버헤드)
*   **OS와의 융합 (Kernel Stacks & Buffers)**:
    *   **TCP Socket**: 커널 레벨의 `sk_buff` 구조체를 통해 수신 버퍼(Recv-Q)와 송신 버퍼(Send-Q)를 관리합니다. `backlog` 큐가 가득 차면 SYN Cookie를 사용하여 DoS를 방어합니다.
    *   **UDP Socket**: 별도의 연결 상태가 없으므로, 서버가 처리할 수 있는 속도보다 패킷이 빠르게 들어오면 **UDP Flood** 공격에 취약해질 수 있습니다.
*   **보안 (Security)**:
    *   TCP의 연결 설정 과정(3-Way Handshake)은 **TCP SYN Flooding** 공격의 표적이 됩니다.
    *   UDP는 포트를 스캔하기 어렵지만(응답이 없으므로), **Amplification Attack**(예: DNS Amp)의 악용 도구로 쓰이기도 합니다.

### 📢 섹션 요약 비유
비교 분석은 **'전문 택배사(TCP)'와 '급행 퀵 서비스(UDP)'의 선택**입니다. 단순히 "TCP가 좋다, UDP가 나쁘다"가 아닙니다. 고가의 장비(중요 데이터)를 보낼 때는 전문 택배사의 보험(TCP)이 필수지만, 배달 기사가 실시간으로 확인 사진(ACK)을 보내는 동안 음식이 식어버린다면(지연), 그냥 바쁘게 달리는 퀵 서비스(UDP)가 나을 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
### 1. 실무 시나리오 의사결정 프로세스
시스템 아키텍트는 서비스의 목적에 따라 다음과 같은 흐름으로 전송 계층을 결정해야 합니다.

```ascii
[Decision Flow Chart]
Start: 데이터 전송 요청
   |
   +---> [패킷 손실이 용인되는가?] (No)
   |        |
   |        +---> YES: **UDP 사용** (Streaming, TFTP, DNS)
   |        |
   |        +---> NO:  [데이터 순서가 중요한가?] (Yes)
   |                 |
   |                 +---> **TCP 사용** (HTTP, FTP)
   |                 |
   |                 +---> [실시간성(초저지연)이 필수인가?] (예: 금융권 HTS)
   |                          |
   |                          +---> TCP 최적화 또는 전용 UDP 기반 프로토콜(QUIC) 사용
```

### 2. 도입 체크리스트
*   **기술적 측면**:
    *   RTT(Round Trip Time)가 200ms를 넘는 글로벌 환경인가? → **TCP Tuning** 필요.
    *   PPS(Packets Per Second)가 100만을 넘는 초고주파 트래픽인가? → **UDP/Ethernet** 우선 고려.
*   **운영 및 보안 측면**:
    *   방화벽(FW) 규칙이 �