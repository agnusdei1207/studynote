+++
title = "401-404. 전송 계층의 역할과 포트 번호"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 401
+++

# 401-404. 전송 계층의 역할과 포트 번호

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전송 계층(Transport Layer, L4)은 OSI 7계층에서 **호스트 간 통신**을 담당하는 네트워크 계층(L3)과 달리, **프로세스 간 통신(Process-to-Process Delivery)**을 담당하여 종단 시스템(End System) 내의 특정 애플리케이션에 데이터를 정확히 전달하는 계층이다.
> 2. **가치**: **Segmentation(세그먼트화)**과 **Multiplexing(다중화)** 기능을 통해 불안정한 네트워크 환경에서 신뢰성(Reliability)을 보장하고, 포트 번호(Port Number)를 통해 하나의 IP 주소로 다중의 세션을 동시에 처리할 수 있게 한다.
> 3. **융합**: 소프트웨어 정의 네트워킹(SDN) 및 컨테이너 오케스트레이션 환경에서 L4 로드 밸런싱의 핵심 기술이며, TCP(Transmission Control Protocol)와 UDP(User Datagram Protocol)의 선택은 애플리케이션 성능(Latency vs Throughput)을 결정짓는 중요한 변수다.

---

### Ⅰ. 개요 (Context & Background)

전송 계층은 OSI 7계층(Open Systems Interconnection Model)의 제4계층(Layer 4)으로, **네트워크 계층(L3, Internet Layer)**이 '목적지 호스트(Computer)'까지 데이터를 배달하는 '우편배달원' 역할을 한다면, 전송 계층은 그 호스트 내에서 실행되는 수많은 **프로세스(Process)** 중 실제 데이터를 받아야 할 **'수신인(애플리케이션)'을 찾아주는 '비서(Receptionist)'** 역할을 수행한다.

L3 계층인 IP(Internet Protocol)는 비연결형이며 데이터그램 단위로 전송하여 패킷의 순서가 보장되지 않거나 유실될 수 있다. 반면, 전송 계층은 상위 애플리케이션에게 **논리적인 통신 회선(Logical Communication Channel)**을 제공하여, 마치 전용선을 쓰는 것처럼 안정적인 통신 환경을 추상화해 제공한다. 이를 위해 **포트 번호(Port Number)**라는 식별자를 사용하여 IP 주소 하나로 웹, 메일, 파일 전송 등 다양한 서비스가 혼선 없이 동작하도록 제어한다.

💡 **비유**: IP 주소가 '오피스텔 건물 주소'라면, 전송 계층은 건물 입구에서 '호수(101호, 202호)'를 확인하고 정확히 해당 호실로 배달해 주는 **'건물 관리실'**의 기능과 같다.

#### 등장 배경
1.  **기존 한계**: 초기 인터넷은 단일 애플리케이션 통신이 주를 이루었으나, PC가 고성능화되며 한 사용자가 웹 서핑, 메신저, 파일 다운로드를 동시에 수행하는 멀티태스킹 환경이 도래함. IP만으로는 데이터를 어느 프로그램에 전달해야 할지 식별 불가.
2.  **혁신적 패러다임**: **포트 번호(Port Number)** 개념을 도입하여 **소켓(Socket)**이라는 통신 창구를 생성, 논리적인 채널 분리가 가능해짐. 또한, **TCP**를 통해 네트워크의 혼잡이나 오류를 애플리케이션이 알지 못하게 은폐하고 신뢰성을 제공.
3.  **현재의 비즈니스 요구**: 클라우드 컴퓨팅 환경에서 수만 개의 마이크로서비스가 통신해야 하므로, 전송 계층의 **포트 관리**와 **연결 상태 추정(Connection Tracking)**은 보안 및 로드 밸런싱의 핵심 요소가 됨.

📢 **섹션 요약 비유**: 전송 계층은 **'대형 병원 접수처'**와 같습니다. 환자(데이터)가 병원(IP 주소)에 오면, 접수처에서는 예약 번호(포트 번호)를 확인하여 내과, 외과, 소아과(프로세스) 중 정확한 진료실로 안내합니다. 단순히 병원 문 앞에 데려다주는 것(IP 계층)을 넘어, 정확한 의사에게 연결해 주는 것이 전송 계층의 핵심 역할입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

전송 계층의 핵심은 **Multiplexing(다중화)**과 **Demultiplexing(역다중화)** 과정이다. 송신 측은 여러 개의 소켓에서 나온 데이터를 헤더에 포트 번호를 포함(캡슐화) 하여 하나의 네트워크 흐름으로 묶고, 수신 측은 도착한 데이터의 포트 번호를 보고 적절한 소켓으로 분배한다.

#### 1. 구성 요소 (표)
| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/규격 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Port Number** | 프로세스 식별자 | 16비트 필드(0~65535)로 Source/Destination 구분 | Well-Known, Registered, Dynamic | 사서함 번호 |
| **Socket** | 통신 종단점 (Endpoint) | `IP Address + Port Number` 조합, 파일 디스크립터로 관리 | BSD Socket API | 전화기 수화기 |
| **Segment** | 전송 단위 (PDU) | TCP 헤더 + Data (MTU에 맞춰 분할), Seq/Ack 번호 관리 | TCP, UDP | 편지 봉투 |
| **Window Size** | 흐름 제어 | 수신 버퍼의 여유 공간을 알려 송신 속도 조절 (Byte 단위) | Sliding Window | 창구 근무자 |
| **Checksum** | 오류 검출 | 헤더와 데이터의 2의 보수 합으로 전송 중 비트 변조 감지 | CRC 방식 (TCP/UDP) | 배송 시 봉인 스티커 |

#### 2. 포트 번호 세분화 및 동작 원리
포트 번호는 16비트로 표현되어 **0부터 65,535**까지의 범위를 가지며, IANA(Internet Assigned Numbers Authority)에 의해 관리된다.

1.  **Well-Known Ports (0 ~ 1023)**:
    *   **권한**: 시스템 레벨의 권한(Admin, Root)이 필요하며, 시스템 부팅 시 고정된 데몬(Daemon)이 점유.
    *   **목적**: 전 세계적으로 통용되는 표준 서비스. 사용자가 임의로 변경할 시 연결 불가.
    *   **예시**: `22` (SSH - Secure Shell), `80` (HTTP), `443` (HTTPS - HTTP over TLS/SSL).
2.  **Registered Ports (1024 ~ 49151)**:
    *   **권한**: 일반 사용자(User-level) 프로세스가 바인딩(Bind) 가능.
    *   **목적**: 특정 벤더(Vendor)나 애플리케이션을 위해 IANA에 등록된 포트.
    *   **예시**: `3306` (MySQL), `1433` (MS-SQL), `8080` (HTTP Proxy/Alt).
3.  **Dynamic/Private Ports (49152 ~ 65535)**:
    *   **권한**: 클라이언트가 통신을 시작할 때 운영체제(OS)가 자동으로 할당.
    *   **목적**: 일시적인(Ephemeral) 연결 생성. 서버로부터의 응답을 수신하기 위한 임시 구멍.
    *   **예시**: 웹 브라우저가 사이트에 접속할 때 생성되는 무작위 포트.

```ascii
[ TCP/IP 4계층 encapsulation 과정 ]

+---------------------+
|   Application       |  (DATA)
+---------------------+
|       Transport     |  [TCP Header: Src Port: 49152 | Dst Port: 80] + Data
+---------------------+  => 전송 계층이 포트 번호를 붙여 논리적 주소 완성
|    Network (IP)     |  [IP Header: Src IP: 1.1.1.1 | Dst IP: 2.2.2.2] + Seg
+---------------------+  => 인터넷 계층이 세계 주소(IP)를 붙임
|   Link (MAC/Eth)    |  [Eth Header: Src MAC | Dst MAC] + Packet + [FCS]
+---------------------+  => 데이터링크 계층이 물리적 주소(MAC)를 붙임

[ 수신 측 Demultiplexing 과정 ]
Network Layer(L3)가 IP를 확인하고 컴퓨터로 전달
      ↓
Transport Layer(L2)가 TCP Header를 확인 (Port 80)
      ↓
Port 80으로 Listen 중인 Web Server Process로 데이터 전달 (Queue에 적재)
```

#### 3. 심층 동작 원리 (TCP Handshake & Teardown)
신뢰성 있는 통신을 위해 TCP는 **3-Way Handshake**로 연결을 설정하고, **4-Way Handshake**로 연결을 종료한다.

1.  **Connection Establishment (연결 설정)**:
    *   **SYN (Synchronize)**: 클라이언트가 서버에게 연결 요청. `Initial Sequence Number(ISN)` 전송.
    *   **SYN+ACK**: 서버가 요청을 수락하고, 자신의 ISN과 클라이언트의 ISN+1을 Ack로 전송.
    *   **ACK**: 클라이언트가 서버의 ISN+1을 전송하며 연결 확립(ESTABLISHED).
2.  **Data Transfer (데이터 전송)**:
    *   Sequence Number로 순서 보장, Checksum으로 무결성 검증, Ack로 수신 확인.
3.  **Connection Termination (연결 해제)**:
    *   **FIN**: 종료 요청.
    *   **ACK**: 종료 확인.
    *   **FIN**: 상대방도 종료 요청.
    *   **ACK**: 최종 확인 및 **TIME_WAIT** 상태 진입(잔여 패킷 처리).

#### 4. 핵심 알고리즘 및 코드 (Python Socket)
소켓 프로그래밍의 핵심은 소켓 생성 -> 바인딩 -> 리스닝 -> 수락의 과정이다.

```python
# Python TCP Server Socket Example (Conceptual)
import socket

# 1. 소켓 생성 (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 소켓 옵션 설정 (주소 재사용 - TIME_WAIT 상태에서 즉시 재사용)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. 바인딩 (IP 0.0.0.0 -> 모든 인터페이스, Port 8080)
server_socket.bind(('0.0.0.0', 8080))

# 4. 리스닝 (Backlog 큐: 5)
server_socket.listen(5)
print("Server listening on port 8080...")

while True:
    # 5. 수락 (새로운 연결마다 새로운 소켓 생성)
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    # 6. 데이터 송수신
    data = client_socket.recv(1024)
    if data:
        client_socket.send(data) # Echo back
        
    # 7. 종료
    client_socket.close()
```

📢 **섹션 요약 비유**: 전송 계층의 소켓 통신은 **'전화 연결'**과 같습니다. 상대방의 전화번호(IP)를 누르는 것만으로는 부족하며, 내 전화기(소켓)가 전화선을 잡고 있는지 확인해야 합니다. 통화 중(TIME_WAIT)에 다시 전화를 걸면 '통화 중입니다'라는 메시지가 뜨듯, 포트 번호는 **'현재 통화 가능한 회선 번호'** 역할을 하여 동시 통화(세션)를 관리합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

전송 계층은 단순한 데이터 전송을 넘어 보안, 네트워크 성능, 애플리케이션 구조와 밀접하게 연관되어 있다.

#### 1. TCP vs UDP 심층 기술 비교
인터넷 표준인 RFC 793(TCP), RFC 768(UDP)를 바탕으로 한 비교 분석.

| 비교 항목 | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
|:---|:---|:---|
| **연결 방식** | **Connection-Oriented (연결형)**<br>1:1 가상 회선 설정 및 해제 필요 | **Connectionless (비연결형)**<br>Handshake 없이 바로 전송 (Fire-and-Forget) |
| **신뢰성** | **높음 (High)**<br>재전송, 순서 보장, 흐름 제어, 혼잡 제어 | **낮음 (Low)**<br>패킷 유실 시 복구 안 함 (Best-Effort) |
| **오버헤드** | **높음**<br>헤더 크기 20~60 Bytes, 상태 정보 유지 필요 | **낮음**<br>헤더 크기 8 Bytes, 상태 비유지(Stateless) |
| **전송 속도** | 상대적으로 느림 (확인 절차로 인한 지연) | 매우 빠름 (확인 절차 없음) |
| **지표 (Metrics)** | Throughput보다 **Reliability** 우선 | Latency가 중요한 실시간 서비스에 적합 |
| **대표 서비스** | Web(HTTP/HTTPS), Email(SMTP), File Transfer(FTP) | Streaming, VoIP, Online Gaming, DNS |

#### 2. 과목 융합 관점 (OS, 보안, 데이터베이스)

1.  **운영체제 (OS)와의 융합: TCB (Transmission Control Block)**
    *   전송 계층의 상태 정보(State)는 OS 커널(Kernel) 영역의 **TCB**에 저장된다.
    *   **Three-Way Handshake** 과정에서 `SYN Flooding` 공격이 발생하면, 서버는 **SYN_RECV** 상태의 TCB가 대기열(Backlog Queue)을 가득 채워 정상 서비스를 거부한다. 이를 방지하기 위해 OS는 **SYN Cookies** 기술을 사용하여 커널 메모리를 아끼면서 연결을 시도한다.
2.  **보안 (Security)과의 융합: Firewall & NAT**
    *   **Stateful Inspection**: 방화벽이 TCP 세션의 상태(ESTABLISHED, FIN_WAIT 등)를 추적하여, 정상적인 핸드셰이크 과정을 거치지 않은 패킷은 차단한다. 이는 전