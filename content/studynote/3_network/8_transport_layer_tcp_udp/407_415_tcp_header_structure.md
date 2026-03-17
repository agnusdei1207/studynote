+++
title = "407-415. TCP 세그먼트 헤더 구조 분석"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 407
+++

# 407-415. TCP 세그먼트 헤더 구조 분석

> ### 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP (Transmission Control Protocol) 헤더는 데이터그램 방식의 신뢰성 없는 네트워크 위에 **가상 회선(Virtual Circuit)**을 구축하기 위한 제어 정보의 집합체입니다.
> 2. **가치**: Seq/Ack 번호를 통한 **바이트 단위의 순서 보장**과 Window를 통한 **흐름 제어(Flow Control)**를 통해, 네트워크 혼잡도에 따라 전송 속도를 조절하며 데이터 유실率为 0%에 수렴하게 만듭니다.
> 3. **융합**: L3(IP 계층)의 라우팅 정보와 결합하여 **Pseudo Header**를 생성함으로써, 엉뚱한 호스트로의 전송을 방지하는 계층 간(Double-Layer) 무결성 검증 메커니즘을 제공합니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
TCP (Transmission Control Protocol)는 OSI 7계층의 **전송 계층(Transport Layer)** 에 속하며, 신뢰성 없는 IP (Internet Protocol) 네트워크 위에서 **신뢰성 있는(Reliable)** 바이트 스트림 서비스를 제공하는 프로토콜입니다. TCP 헤더는 이러한 신뢰성을 구현하기 위해 송수신 호스트 간의 상태를 동기화하고, 데이터의 순서를 관리하며, 네트워크 혼잡을 제어하는 **제어 패킷(Control Packet)**의 핵심부입니다. 기본적으로 **20바이트의 고정 헤더**와 최대 40바이트의 **옵션(Options)** 필드로 구성되어 총 60바이트를 초과할 수 없습니다.

#### 등장 배경
① **기존 한계**: 초기 인터넷은 단순한 데이터 전송이 목적이었으나, 파일 전송이나 웹 서비스 등 데이터의 순서가 중요하고 유실이 용납되지 않는 서비스가 등장함에 따라 기존의 비연결형 프로토콜(UDP 등)으로는 한계가 발생했습니다.
② **혁신적 패러다임**: **3-way Handshake**를 통해 논리적인 연결을 설정하고, **Sequence Number**와 **Acknowledgment Number** 기반의 **슬라이딩 윈도우(Sliding Window)** 기법을 도입하여 효율적인 흐름 제어와 오류 제어를 동시에 달성했습니다.
③ **현재의 비즈니스 요구**: 웹(HTTP/HTTPS), 이메일(SMTP), 파일 전송(FTP) 등 대부분의 인터넷 트래픽이 TCP를 사용하며, 고속 네트워크(10Gbps 이상) 환경에서도 **대역폭 지연 곱(Bandwidth-Delay Product)**을 최적화하기 위해 헤더의 옵션 필드(Window Scale, SACK 등)가 적극 활용됩니다.

#### 💡 비유
TCP 헤더는 **등기 우편물에 붙는 운송장**입니다. 단순히 주소(IP)만 적는 것이 아니라, "이 물건이 전체 짐 중 몇 번째 상자인지(Seq)", "수신자가 몇 번째까지 받았는지 확인 서명을 했는지(Ack)", "받을 공간이 남는지(Window)", "긴급 물건인지(URG)" 등의 관리 정보를 상자 위에 빽빽하게 적어서, **중간에 상자가 떨어지거나 순서가 섞여도 원래 상태로 완벽하게 복원**되게 합니다.

#### 📢 섹션 요약 비유
TCP 헤더는 마치 **복잡한 물류 센터의 분류 시스템**과 같습니다. 수천 개의 패키지가 뒤섞여도, 각 상자에 붙은 바코드(순서 번호)와 확인 시스템(ACK)을 통해 하나도 빠짐없이 정확한 순서로 고객에게 전달될 수 있도록 통제하는 거대한 관제 센터의 핵심 운영 매뉴얼입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
TCP 헤더는 20~60바이트의 크기로, 비트 단위로 쪼개어진 복잡한 필드들로 구성됩니다.

| 요소명 | 비트 수 | 역할 | 내부 동작 메커니즘 | 프로토콜 관계 | 비유 |
|:---|:---:|:---|:---|:---|:---|
| **Src/Dst Port** | 16/16 | **프로세스 식별** | IP가 목적지 **컴퓨터**를 찾는다면, Port는 그 안의 **프로세스(앱)**를 찾음. Well-known(0-1023)과 Dynamic(1024+) 범위 존재 | Multiplexing (Demultiplexing) | 건물의 호수(아파트 동/호) |
| **Seq Number** | 32 | **송신 바이트 순서** | 전체 데이터 스트림에서 현재 세그먼트의 **첫 바이트**가 갖는 오프셋. ISN(Initial Seq Number)에서 시작하여 바이트 수만큼 증가 | Reliability, Ordering | 페이지 번호 |
| **Ack Number** | 32 | **수신 확인 요청** | **Cumulative ACK** 방식. "내가 N번까지 잘 받았으니, 다음엔 N+1번을 보내라"는 의미. 송신 버퍼 관리의 핵심 | Flow Control, Retransmission | 영수증의 "다음에 줄 상품 번호" |
| **Data Offset** | 4 | **헤더 길이** | 4바이트 단위. 헤더 길이가 가변(Option)이므로 데이터가 시작되는 지점을 알림 (min 5, max 15) | Parsing | 목차의 쪽수 |
| **Flags** | 6 | **제어 비트** | URG, ACK, PSH, RST, SYN, FIN의 6가지 플래그로 연결 상태 및 데이터 특성 제어 | Connection Mgmt | 전보의 "긴급", "확인" 등 도장 |
| **Window Size** | 16 | **수신 버퍼 여유** | **Flow Control**의 핵심. 현재 내 수신 버퍼(RCV Buffer)에 남은 공간을 알림. 0이면 전송 중지 | Congestion Avoidance | 창고에 남은 공간 (비우기 전까진 보내지 마) |
| **Checksum** | 16 | **오류 검출** | 헤더+데이터+**Pseudo Header**를 포함한 모든 비트에 대한 2의 보수 연산. 1비트 오류도 감지 | Error Detection | 포장 테이프의 위변조 방지 스티커 |

#### 2. ASCII 구조 다이어그램 (Layout)
아래 다이어그램은 TCP 헤더의 전체적인 메모리 레이아웃을 32비트 워드(Word) 단위로 시각화한 것입니다.

```ascii
                     TCP Segment Header Layout (Memory Map)

      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |          Source Port          |       Destination Port        |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |                        Sequence Number                        |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |                    Acknowledgment Number                      |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |  Data |           |U|A|P|R|S|F|                               |
     | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
     |       |           |G|K|H|T|N|N|                               |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |           Checksum            |         Urgent Pointer        |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |                    Options                    |    Padding    |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |                             Data                              |
     ++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+++

     Legend:
     URG: Urgent Pointer field significant
     ACK: Acknowledgment field significant
     PSH: Push Function
     RST: Reset the connection
     SYN: Synchronize sequence numbers
     FIN: No more data from sender
```

**다이어그램 해설**:
1.  **포트 식별 (0~31비트)**: 상위 16비트에 출발지(Source), 하위 16비트에 목적지(Destination) 포트가 위치하여 End-to-End 통로를 확정합니다. Big-Endian 방식(네트워크 바이트 오더)으로 저장됩니다.
2.  **상대적 순서 (32~95비트)**: **Sequence Number**는 데이터의 순서를, **Acknowledgment Number**는 수신 확인을 의미합니다. 이 두 필드가 TCP의 신뢰성을 책임지는 핵심 엔진입니다.
3.  **제어 및 상태 (96~127비트)**: **Data Offset**은 헤더의 끝과 데이터의 시작점을 알려줍니다. 6개의 **Control Bits(Flags)**는 비트 단위로 작동하며, 예를 들어 `SYN=1, ACK=0`은 연결 요청이고, `SYN=1, ACK=1`은 연결 수락을 의미합니다.
4.  **흐름 제어 및 무결성 (128~191비트)**: **Window Size**는 수신측의 처리 능력을 알려 송신측이 전송량을 조절하게 하여(Stop-and-Wait 대신 Sliding Window 구현), 체크섬은 전송 중 데이터 변조를 감지합니다.

#### 3. 심층 동작 원리 (Interaction)

**가. 시퀀스 번호와 확인 응답 (Seq & Ack 동기화)**
TCP는 **바이트 스트림(Byte Stream)** 서비스이므로, 데이터를 보낼 때마다 Seq Number를 바이트 수만큼 증가시킵니다.
*   **동작 흐름**:
    1.  송신 A: `Seq=1000`, Length=100 (1000~1099 바이트 전송)
    2.  수신 B: 잘 받음. `Ack=1100` 송신 ("1100번째 바이트를 기다림")
    3.  송신 A: Ack 1100 확인. 다음 패킷 `Seq=1100` 전송.
이때 Ack Number는 **Cumulative(누적)** 방식이므로, 중간에 패킷이 누락되면 이후 패킷을 받아도 Ack는 계속 누락된 바이트의 위치를 가리키며, 송신자는 이를 통해 유실을 감지하고 **Retransmission(재전송)**을 수행합니다.

**나. 플래그 비트의 미세한 제어**
*   **SYN (Synchronize)**: 연결 설정(3-way handshake) 단계에서 Seq Number를 초기화하고 동기화하는 역할.
*   **ACK (Acknowledgment)**: Ack Number 필드의 유효성을 나타내는 스위치. SYN 패킷을 제외한 거의 모든 패킷에서 1로 설정됨.
*   **FIN (Finish)**: 연결 종료 시, 보낼 데이터가 더 이상 없음을 알림.
*   **RST (Reset)**: 포트가 닫혀 있거나 세션이 유효하지 않을 때 강제로 연결을 끊는 '비상 브레이크'.
*   **PSH (Push)**: 버퍼링 없이 즉시 상위 애플리케이션으로 데이터를 전달하라는 명령 (예: Telnet 입력 시).
*   **URG (Urgent)**: 정상적인 데이터 처리 순서를 무시하고 긴급 데이터(Urgent Pointer가 가리키는 위치)를 먼저 처리해야 함을 알림.

#### 4. 핵심 알고리즘 및 코드 예시
다음은 소켓 프로그래밍 시 헤더 구조를 다루는 C언어 구조체 예시입니다.

```c
// POSIX 표준 TCP 헤더 구조체 정의 (sys/tcp.h)
struct tcphdr {
    u_short th_sport;     // source port
    u_short th_dport;     // destination port
    tcp_seq th_seq;       // sequence number
    tcp_seq th_ack;       // acknowledgement number
    u_int th_off:4;       // data offset (header length)
    u_int th_x2:4;        // (unused)
    u_char th_flags;      // flags field
    u_short th_win;       // window size
    u_short th_sum;       // checksum
    u_short th_urp;       // urgent pointer
};

// TCP 플래그 확인 매크로
#define TH_FIN  0x01
#define TH_SYN  0x02
#define TH_RST  0x04
#define TH_PUSH 0x08
#define TH_ACK  0x10
#define TH_URG  0x20

// 예: 패킷이 SYN 패킷인지 확인
if (tcp_hdr->th_flags & TH_SYN) {
    // 연결 설정 요청(SYN) 패킷 감지 로직 수행
    handle_connection_establishment();
}
```

#### 📢 섹션 요약 비유
TCP 헤더의 작동은 마치 **복잡한 고속도로 톨게이트 시스템**과 같습니다. 각 차량(패킷)은 번호판(Seq)을 가지고 진입하며, 진입을 확인하는 영수증(Ack)을 발부받습니다. 톨게이트 게이트(Window Size)는 도로 여유 용량에 따라 차량 진입을 조절하고, 도로 공사 중단이나 사고 발생 시 관리자(RST, FIN)가 진입을 제어하는 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 (TCP vs UDP Headers)
TCP 헤더의 복잡성을 이해하기 위해 경량 프로토콜인 UDP (User Datagram Protocol)와 비교합니다.

| 비교 항목 | TCP Header (20~60 Bytes) | UDP Header (8 Bytes) | 기술적 영향 (Implication) |
|:---|:---|:---|:---|
| **크기 (Min)** | **20 Bytes** (Fixed) | **8 Bytes** (Fixed) | TCP는 12바이트의 **Overhead(시퀀스, 확인번호, 윈도우 등)**가 더 발생하여, 작은 패킷 전송 시 효율이 UDP보다 낮음. |
| **필드 구성** | Seq, Ack, Window, Flags, Offset | Port(2), Len(2), Checksum(2) | UDP는 **Connectionless(비연결형)**로 Seq/Ack가 없어 **신뢰성을 제공하지 않음**. |
| **오류 제어** | **Retransmission(재전송) 지원** (Ack 기반) | Checksum(오류 검출)만 존재, 복구 불가 | TCP는 **In-order Delivery(순서 보장)**, UDP는 데이터 순서가 뒤바둘 수 있음. |
| **흐름 제