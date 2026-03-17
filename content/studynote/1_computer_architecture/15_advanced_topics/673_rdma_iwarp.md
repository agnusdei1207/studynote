+++
title = "RDMA iWARP 프로토콜"
date = "2026-03-14"
weight = 673
+++

# 🧠 BrainScience PE 가이드라인: RDMA iWARP 프로토콜

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존의 광범위한 TCP/IP 이더넷 인프라를 그대로 활용하면서, 하드웨어 오프로딩을 통해 **제로 카피(Zero-Copy)**와 **커널 우회(Kernel Bypass)**를 실현하는 네트워크 프로토콜입니다.
> 2. **가치**: 네트워크 대기 시간(Latency)을 획기적으로 줄이고 CPU 부하를 90% 이상 절감하여, 데이터센터의 처리량(Throughput)을 극대화하고 TCO(Total Cost of Ownership)를 개선합니다.
> 3. **융합**: 로우 레벨의 하드웨어(RNIC) 제어부터 OS 커널 드라이버, 그리고 상위의 NVMe-oF나 AI 분산 학습 프레임워크까지 계층별 기술이 유기적으로 결합된 고성능 솔루션입니다.

---

### Ⅰ. 개요 (Context & Background)

RDMA (Remote Direct Memory Access, 원격 직접 메모리 접근) 기술은 기본적으로 네트워크로 연결된 두 시스템의 메모리 간 데이터를 호스트의 **CPU (Central Processing Unit)**, **OS (Operating System)** 개입 없이 직접 전송하는 기술입니다. 전통적인 소켓 통신(TCP/IP)은 데이터를 송수신할 때마다 커널 영역과 유저 영역 간의 **Context Switching (문맥 교환)**과 메모리 복사(Copy)가 발생하여 심각한 성능 병목을 유발합니다.

**iWARP (Internet Wide Area RDMA Protocol, 인터넷 광역 RDMA 프로토콜)**는 이러한 RDMA의 성능 이점을 포기하지 않으면서도, 가장 널리 배포된 네트워크 계층인 TCP/IP 위에서 구현되도록 설계된 표준 프로토콜입니다. 기존의 **InfiniBand**와 같은 전용 네트워크 장비를 도입하는 것은 막대한 비용이 드는 반면, iWARP는 기존의 이더넷 스위치와 라우터 인프라를 그대로 재사용할 수 있다는 강력한 경제적, 운영적 이점을 가집니다. 이는 데이터센터의 **Converged Network (융합 네트워크)** 구현에 있어 핵심적인 역할을 수행합니다.

📢 **섹션 요약 비유:** 복잡한 세관 통관 절차(커널, 프로토콜 스택)와 중간 창고(버퍼)를 거치지 않고, 출발지 공장의 부품을 목적지 공장의 생산 라인(메모리)으로 고속 화물차가 직통으로 운반해 주는 시스템입니다. 단, 이 고속 화물차는 일반 도로(TCP/IP) 위에서만 운영이 가능한 특수 차량입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

iWARP의 가장 큰 기술적 특징은 복잡한 계층 구조를 하드웨어인 **RNIC (RDMA-enabled Network Interface Controller, RDMA 지원 네트워크 인터페이스 카드)**로 통합하여 처리한다는 점입니다. 기존 소프트웨어 스택이 처리하던 TCP 연결 설정, 혼잡 제어, 패킷 재조립 등의 무거운 작업을 하드웨어 회로가 대행합니다.

#### 1. iWARP 프로토콜 스택 구성
iWARP는 IETF(Internet Engineering Task Force) 표준으로 정의된 3개의 상위 계층 프로토콜을 TCP 위에 올려 RDMA 기능을 구현합니다.

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 비유 |
|:---:|:---|:---|:---|
| **MPA** | Marker PDU Aligned Framing | TCP의 **Byte Stream(바이트 스트림)** 특성(경계가 없는 데이터 흐름)에 메시지 경계(Message Boundary)를 식별할 수 있는 **Marker(마커)**를 삽입하여 상위 계층이 데이터를 패킷 단위로 인식하게 함. | 도로에 흐릿하게 그어진 차선을 명확한 실선으로 다시 그어주는 작업 |
| **DDP** | Direct Data Placement | 수신된 패킷의 **Payload(페이로드)**를 분석하여, 이를 CPU가 복사하지 않고도 최종 목적지인 **Application Memory Buffer(애플리케이션 메모리 버퍼)**의 정확한 오프셋(Offset)에 직접 배치함. | 택배 상자를 분류실에 쌓아두지 않고, 수신자 방 책상 위 특정 좌표에 직접 내려놓음 |
| **RDMAP** | RDMA Protocol | RDMA의 의미(Semantics)인 **SEND, WRITE, READ** 명령을 정의하고, DDP를 통해 전달받은 데이터의 무결성을 검증하며 **Stag(Steering Tag)**를 관리하여 메모리 접근 권한을 제어함. | 메모리 주소와 접근 권한이 적힌 '보안 인증서'를 검증하고 출입을 허가하는 관리자 |
| **TOE** | TCP Offload Engine | TCP의 **3-Way Handshake**, **Sliding Window(슬라이딩 윈도우)** 흐름 제어, **ACK(Acknowledgment)** 재전송 처리 등을 하드웨어에서 전담하여 CPU 부하 제로(Zero)화. | 운전자(CPU)가 핸들을 잡지 않아도 목적지까지 자동 주행하는 오토파일럿 시스템 |

#### 2. 아키텍처 다이어그램 및 데이터 흐름
아래 다이어그램은 iWARP가 표준 이더넷 환경에서 어떻게 동작하는지를 보여줍니다.

```ascii
+--------------------------------------------------------------------------+
|  Host Server A (Sender)                                                  |
|  +----------------+        +-----------------------------------------+   |
|  | User Process   |        |   RNIC (Hardware)                        |   |
|  | (Application)  |        |   +-------------------+   +-----------+ |   |
|  |                | Write  |   | iWARP Logic       |   | MAC/PHY   | |   |
|  | [Data Buffer]  |------->|   | (RDMAP/DDP/MPA)   |-->| (Ethernet)| |   |
|  | Addr: 0x1000   | Verbs  |   | +---------------+ |   |           | |   |
|  +----------------+        |   | | TOE (TCP Eng) | |   |           | |   |
|            |               |   | +---------------+ |   |           | |   |
|            |               |   +-------------------+   +-----------+ |   |
|            |               +-----------------------------------------+   |
+------------|-------------------------------------------------------------+
             | 1. RDMA Write Request (Addr, Len, STag)
             v
+--------------------------------------------------------------------------+
|  Network Infrastructure (Standard Ethernet/TCP/IP)                      |
|  [ Switch / Router ] - No Special Config Required (Lossy OK)             |
+--------------------------------------------------------------------------+
             | 2. TCP Segments (Standard IP Routing)
             v
+--------------------------------------------------------------------------+
|  Host Server B (Receiver)                                                |
|  +-----------------------------------------+        +----------------+   |
|  |   RNIC (Hardware)                        |        | User Process   |   |
|  |   +-------------------+   +-----------+ |        | (Application)  |   |
|  |   | iWARP Logic       |   | MAC/PHY   | |        |                |   |
|  |   | (RDMAP/DDP/MPA)   |<--| (Ethernet)| |        | [Data Buffer]  |   |
|  |   | +---------------+ |   |           | |        | Addr: 0x5000   |   |
|  |   | | TOE (TCP Eng) | |   |           | |        | Direct Placed! |   |
|  |   | +---------------+ |   |           | |        +----------------+   |
|  |   +-------------------+   +-----------+ |               ^           |
|  +-----------------------------------------+               |           |
|            | 3. DMA Write directly to Buffer (No CPU)     |           |
+------------|-------------------------------------------------------------+
             | 4. Completion Notification (Interrupt/Polled)
             v
       CPU Notification Only (Data already there)
```

**[다이어그램 심층 해설]**
1.  **Zero-Copy Path (제로 카피 경로)**: 송신 측 애플리케이션이 `rdma_write()` 등의 **Verb(동사)** 함수를 호출하면, CPU는 메모리 버퍼의 주소와 길이를 담은 **WR (Work Request, 작업 요청)**을 **SQ (Send Queue, 송신 큐)**에 등록합니다. RNIC은 이를 확인하여 **DMA (Direct Memory Access, 직접 메모리 접근)** 엔진을 가동합니다.
2.  **TCP Offload & Framing**: RNIC 내부의 TOE가 TCP 세션을 관리하며 데이터를 패킷으로 자릅니다. 이때 MPA가 **FPDU (Formatted PDU)** 형태로 데이터를 포맷팅하여 TCP 바이트 스트림 상에서 메시지 단위가 보존되도록 합니다.
3.  **Direct Placement (직접 배치)**: 수신 측 RNIC은 패킷을 수신하면, DDP 계층이 헤더의 **Tag(태그)** 정보를 확인하여 **Virtual Address(가상 주소)**를 계산합니다. 그 후 데이터를 커널 버퍼를 거치지 않고(No Copy), 목표 애플리케이션 버퍼의 해당 오프셋에 직접 DMA를 쏩니다.
4.  **Completion (완료 신고)**: 모든 데이터 전송이 완료되면 RNIC은 **CQ (Completion Queue, 완료 큐)**에 엔트리를 쓰고, 이를 애플리케이션이 폴링하거나 CPU에 인터럽트를 발생시켜 작업 완료를 알립니다. **핵심은 데이터 복사가 단 한 번도 발생하지 않았다는 점입니다.**

#### 3. 핵심 소프트웨어 구조 (libibverbs)
iWARP는 벤더 중립적인 API 표준인 **libibverbs**를 사용합니다. 애플리케이션 개발자는 하부 프로토콜이 RoCE인지 iWARP인지 상관없이 동일한 코드를 작성할 수 있습니다.

```c
// 개념적 코드: iWARP RDMA Write 작업 등록
// 실무에서는 ibv_post_send 함수를 사용하며, RNIC 드라이버가 이를 처리함

struct ibv_send_wr wr; // Work Request
struct ibv_sge sge;    // Scatter/Gather Entry

// 1. 데이터가 위치한 메모리 주소와 크기 설정
sge.addr = (uint64_t)source_buffer; 
sge.length = DATA_SIZE;
sge.lkey = source_mr->lkey; // Local Key (Memory Protection)

// 2. 타겟 정보 설정 (네트워크를 통해 사전에 교환된 정보)
wr.wr.rdma.remote_addr = target_buffer_vaddr;
wr.wr.rdma.rkey = target_mr_rkey; // Remote Key (Access Right)

// 3. 작업 요청 타입: RDMA WRITE (Send with Immediate도 가능)
wr.opcode = IBV_WR_RDMA_WRITE;

// 4. Driver 함수 호출 (CPU가 이 함수를 호출하는 순간 제어권은 RNIC으로 넘어감)
// RNIC은 이 정보를 바탕으로 TCP/IP 패킷을 조립하여 전송
if (ibv_post_send(qp, &wr, &bad_wr)) {
    // 오류 처리
}
```

📢 **섹션 요약 비유:** 일반 택배 시스템(TCP/IP)을 이용하지만, 택배 기사(CPU)가 트럭에서 상자를 내려 분류실(커널 버퍼)에 넣고 다시 사무실로 가져가는 복잡한 과정을 생략합니다. 대신 트럭 뒤에 달린 자동 팔(RNIC)이 도착하자마자 수신자의 책상 위(애플리케이션 메모리)에 물건을 정확한 위치에 놓고 돌아갑니다. 도로(네트워크)는 일반 국도를 그대로 사용합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RDMA 구현 기술 비교 분석표
RDMA를 구현하는 대표적인 방식인 **InfiniBand**, **RoCE (RDMA over Converged Ethernet)**, **iWARP**를 기술적/운영적 관점에서 비교 분석합니다.

| 비교 항목 | InfiniBand (IB) | RoCE v2 (RDMA over Converged Ethernet) | iWARP (Internet Wide Area RDMA Protocol) |
|:---|:---|:---|:---|
| **전송 계층** | 전용 L2/L3 Physical Layer | **UDP (User Datagram Protocol)** / IP | **TCP (Transmission Control Protocol)** / IP |
| **네트워크 요구사항** | 전용 케이블/스위치/Cable | **Lossless(무손실)** 환경 필수 (PFC, ECN 설정) | 기존 **Lossy(손실 허용)** 이더넷 환경 사용 가능 |
| **혼잡 제어 (Congestion)** | 하드웨어 기반Credit 방식 | 스위치 기반 PFC/ECN (설정 난이도 높음) | **TCP 표준 혼잡 제어 알고리즘** 탑재 (안정적) |
| **지연 시간 (Latency)** | **최저 (Sub-microsec)** | 매우 낮음 (IB 대비 약간 높음) | 낮음 (TCP 처리 오버헤드로 인해 RoCE 대비 약간 높음) |
| **라우팅 (Routing)** | Subnet 내 라우팅 가능성 제한 | Layer 3 라우팅 가능 | **인터넷/WAN 라우팅 가능성 최상** |
| **도입 비용 (TCO)** | 매우 높음 (장비 교체 필요) | 중간 (스위치 설정/업그레이드 필요) | **낮음 (기존 인프라 재사용 가능)** |

#### 2. 기술적 상관관계 (Synergy & Trade-offs)
*   **TCP의 힘을 빌리는 iWARP**: iWARP는 TCP의 신뢰성(재전송, 순서 보장)을 그대로 하드웨어에서 구현합니다. 이는 패킷 손실이 빈번하게 발생하는 WAN(Long-distance network)이나 구형 네트워크 환경에서 **RoCE**가 가진 혼잡 붕괴(Congestion Collapse) 위험을 방지해 줍니다.
*   **OSI 7 Layer와의 융합**:
    *   **L2 (Data Link)**: 기존 이더넷 MAC 주소 방식을 그대로 사용.
    *   **L3 (Network)**: 기존 IP 라우팅 테이블 활용.
    *   **L4 (Transport)**: 기존 TCP 포트 기반 통신.
    *   **L5~7 (Session/Application)**: RDMA Verbs API를 통해 스토리지(NVMe-oF)나 데이터베이스(DBMS)와 통합.
*   **성능 저하 요인**: iWARP의 약점은 **TCP의 복잡성**을 하드웨어로 완전히 구현해야 하므로, RoCE 대비 **RNIC 칩셋의 가