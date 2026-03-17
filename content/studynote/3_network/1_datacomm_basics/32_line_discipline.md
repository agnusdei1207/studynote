+++
title = "NW #32 회선 제어 규약 (Line Discipline)"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #32 회선 제어 규약 (Line Discipline)

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: 회선 제어 규약(Line Discipline)은 공유 통신 매체에서 데이터 충돌을 방지하고 전송 순서를 부여하기 위한 '통신 규칙'으로, 누가(Speaker), 언제(Timing), 무엇을(Data) 전송할지를 결정하는 계층(Layer 2)의 핵심 메커니즘이다.
> 2. **가치**: 비동기식 환경에서의 신뢰성을 보장하며, 특히 결정론적(Deterministic) 지연이 요구되는 산업용 네트워크나 위성 통신에서 99.999%의 가용성을 유지하는 필수 요소이다.
> 3. **융합**: CSMA/CD(Carrier Sense Multiple Access with Collision Detection) 기반의 현대 이더넷과는 대조적인 중앙 집중 제어 방식을 보여주며, OSI 7계층의 데이터 링크 계층(Data Link Layer)과 MAC(Media Access Control) 서브계층의 기원이 되는 개념이다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
회선 제어 규약은 두 개 이상의 통신 장치(Station, Node)가 하나의 전송 매체를 공유하는 환경에서, **"누가 누구에게 말을 걸 권한을 가지는가"**를 정의하는 프로토콜이다. 단순히 물리적인 케이블 연결을 넘어, 논리적인 '송신권'을 할당하고 세션(Session)을 관리하는 일종의 통신 예법(Etiquette)에 해당한다. 이는 OSI 7계층 중 **데이터 링크 계층 (Data Link Layer)**의 주요 기능인 **흐름 제어 (Flow Control)**와 **오류 제어 (Error Control)**의 전제 조건이 된다.

**💡 비유**
이는 여러 명이 함께 사용하는 단일 톡톡이 있는 회의실에서, 동시에 말하여 소음이 발생하는 것을 막기 위해 사회자가 발언권을 넘기거나, 손을 들고 순서를 기다리는 '발언권 관리 시스템'과 같다.

**등장 배경**
① **기존 한계**: 초기 통신망에서는 단순한 Point-to-Point 연결이 주를 이루었으나, 통신망이 확장되면서 Multi-point(다중점) 환경에서 **충돌(Collision)**과 **교착 상태(Deadlock)**가 빈번히 발생했다.
② **혁신적 패러다임**: 중앙 집중형 **Primary Station(주국)**이 통신을 제어하는 Master-Slave 구조(Polling)와, 대등한 관계에서 상호 협의하여 권한을 획득하는 Peer-to-Peer 구조(ENQ/ACK)가 도입되었다.
③ **현재의 비즈니스 요구**: 현대의 고속 네트워크로 넘어가는 과도기적인 기술로, 현재에도 **산업용 제어 시스템(SCADA)**이나 **NFS (Network File System)** 등에서 우선순위 기반의 제어를 위해 여전히 응용되고 있다.

**📢 섹션 요약 비유**: 회선 제어 규약의 개념 정립은 '혼잡한 도로의 교통정리를 위해 신호등과 교통경찰을 도입한 것'과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**
회선 제어 규약을 구성하는 핵심 요소들은 물리적 회선의 연결부터 논리적 세션의 종료까지 주기를 형성한다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Mechanism) | 프로토콜/규약 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Primary Station (주국)** | 네트워크의 제어 권한을 가진 마스터 | Polling/Selection을 수행하고 링크의 상태를 모니터링함 | Master-Slave | 회의 진행자(사회자) |
| **Secondary Station (종국)** | 주국의 명령에 따라 데이터를 송수신 | Polling에 대해 응답하거나, Select되었을 때만 수신 준비 함 | Slave | 참가자 (청중) |
| **ENQ (Enquiry)** | 전송 가능 여부 문의 | 데이터 송신 전 상대방의 버퍼 상태 확인 요청 | ASCII Control Char | "지금 통화 가능해?" |
| **ACK (Acknowledge)** | 긍정 응답 | 수신 준비 완료 또는 데이터 정상 수신 확인 | 0x06 (ACK) | "그래, 보내." / "받았어." |
| **NAK (Negative Ack.)** | 부정 응답 | 수신 불가 상태이거나 에러 발생을 알림 | 0x15 (NAK) | "지금 안 돼." / "다시 보내." |
| **EOT (End of Trans.)** | 전송 종료 알림 | 모든 비트 전송이 완료되었음을 선언하고 회선 반납 | ASCII Control Char | "수고했어, 끝낼게." |

**ASCII 구조 다이어그램: 통신 제어 순서도**

다음은 Point-to-Point 환경에서 송신국과 수신국 간의 세션 설정 및 데이터 전송, 종료 과정을 도식화한 것이다.

```ascii
   [Sender]                                        [Receiver]
      |                                                |
      |  1. Request to Send (RTS) / Enquire (ENQ)     |
      |----------------------------------------------->|
      |                                                |
      |                            2. Acknowledge (ACK)|
      |<-----------------------------------------------|
      |   (Permission Granted)                         |
      |                                                |
      |  3. Data Transmission (Block)                  |
      |----------------------------------------------->|
      |                                                |
      |  4. Acknowledge (ACK) / Checksum OK            |
      |<-----------------------------------------------|
      |                                                |
      |  5. End of Transmission (EOT)                  |
      |----------------------------------------------->|
      |                                                |
      |                 (Session Terminated)           |
      |                                                |
```

**심층 동작 원리: ENQ/ACK 핸드셰이킹 매커니즘**
이 과정은 소프트웨어적 레벨에서 3-Way Handshake와 유사한 **2-Way Handshake** 혹은 **3-Way Handshake**로 구현된다.
1. **Setup Phase**: 송신자(Transmitter)는 `ENQ` 문자(0x05)를 전송하여 회선이 유휴(Idle) 상태이고 수신자가 준비되었는지 확인한다.
2. **Acknowledge Phase**: 수신자(Receiver)는 버퍼 여유가 있다면 `ACK`를, 그렇지 않다면 `NAK`를 반환한다. 만약 `ACK` 수신 전에 타임아웃(Timeout)이 발생하면 송신자는 재시도(Retry) 로직을 수행한다.
3. **Data Transfer Phase**: 데이터 프레임(Frame) 전송 후 수신자는 CRC(Cyclic Redundancy Check) 등을 통해 에러를 검증하고 다시 `ACK`를 반환한다.
4. **Teardown Phase**: 송신자는 `EOT`(0x04)를 전송하여 세션을 종료한다.

**핵심 알고리즘 및 코드 스니펫 (의사코드)**
다음은 단순한 Stop-and-Wait 방식의 회선 제어 로직을 나타낸 것이다.

```python
# Pseudocode: ENQ/ACK Line Discipline Logic (Sender Side)

MAX_RETRY = 3
TIMEOUT_LIMIT = 2000  # ms

def transmit_data(data_frame):
    retry_count = 0
    
    # 1. Line Discipline: Request Permission
    while retry_count < MAX_RETRY:
        send_control_char("ENQ")  # Enquiry
        response = wait_for_response(timeout=TIMEOUT_LIMIT)
        
        if response == "ACK":
            break  # Permission granted
        elif response == "NAK":
            wait_delay()
        retry_count += 1
    
    if retry_count >= MAX_RETRY:
        raise ConnectionError("Line Discipline Failed: Link not established")

    # 2. Data Transfer
    send_frame(data_frame)
    
    # 3. Termination Check
    if wait_for_response() == "ACK":
        send_control_char("EOT")  # End of Transmission
        return True
    else:
        return False # Error handling required
```

**📢 섹션 요약 비유**: 회선 제어 아키텍처는 '복잡한 비즈니스 계약서의 협상 과정'과 같습니다. 계약 성사(ACK) 전까지는 계속 물의보고(ENQ)를 하고, 일이 끝나면 계약을 종료(EOT)하는 절차를 밟는 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: ENQ/ACK vs. Poll/Select**

| 구분 (Criteria) | ENQ/ACK (Peer-to-Peer) | Poll/Select (Master-Slave) |
|:---|:---|:---|
| **네트워크 토폴로지** | Point-to-Point (1:1) | Multipoint (1:N) |
| **제어 주체** | 통신을 원하는 당사자 (Peer) | Primary Station (주국) |
| **추가/제거 용이성** | 구성 변경 시 양쪽 설정 필요 | 주국만 알면 됨 (확장성 우수) |
| **오버헤드 (Overhead)** | 데이터가 있는 경우에만 제어 프레임 발생 | 주국이 주기적으로 Polling을 계속 수행 (Idle Traffic 발생) |
| **결정론성 (Deterministic)** | 상대적으로 낮음 (경쟁 발생 가능) | 매우 높음 (Priority 보장 가능) |
| **대표 사례** | **BSC (Binary Synchronous Communication)** | **IBM SDLC (Synchronous Data Link Control)** |

**과목 융합 관점 분석**

1.  **네트워크 vs. 컴퓨터 구조 (Interrupt vs. Polling)**:
    *   회선 제어의 Poll/Select 방식은 컴퓨터 구조의 **폴링 인터럽트 (Polling Interrupt)** 방식과 논리적으로 동일하다. CPU(Primary)가 주기적으로 주변 장치(Secondary)의 상태를 확인하여 데이터 처리를 수행한다.
    *   반면, ENQ/ACK는 **하드웨어 인터럽트(Interrupt)**와 유사하다. 주변 장치가 CPU에게 "서비스 필요(ENQ)"를 요청하고, CPU가 이를 수락(ACK)하는 비동기적 흐름을 가진다.

2.  **네트워크 vs. 운영체제 (Lock & Semaphore)**:
    *   회선 제어는 본질적으로 **공유 자원(Shared Resource)**인 회선에 대한 **상호 배제(Mutual Exclusion)** 메커니즘이다. 이는 OS의 세마포어(Semaphore)나 뮤텍스(Mutex) 개념과 맞닿아 있으며, Deadlock(교착 상태) 방지를 위해 타임아웃(Time-out) 등의 기법을 사용한다는 점에서 공통점을 찾을 수 있다.

**📢 섹션 요약 비유**: ENQ/ACK는 '자유 시장 경쟁(수요가 있을 때만 거래)'과 같고, Poll/Select는 '관 주도의 할당 경제(주기적인 배급)'와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정 매트릭스**

1.  **시나리오 A: 소규모 제어 루프 (저지연/고신뢰성 필수)**
    *   상황: 자동차 제조 라인의 로봇 팔 제어 통신.
    *   **결정**: **Polling 방식 도입**.
    *   이유: 마스터가 주기적으로 슬레이브를 체크하므로, 최대 지연 시간(Latency)을 예측할 수 있어 결정론적(Deterministic) 동작이 보장됨. 충돌 위험이 없어 안정적임.

2.  **시나리오 B: 대규모 센서 네트워크 (에너지 효율 중요)**
    *   상황: 야적장의 수천 개의 온도 센서.
    *   **결정**: **ENQ/ACK ( contention 기반) 방식 고려**.
    *   이유: 센서가 데이터를 가지지 않았을 때 계속 Polling을 수행하는 것은 대역폭 낭비. 센서가 이벤트 발생 시 `ENQ`를 보내는 Interrupt-driven 방식이 에너지 효율이 높음 (단, 충돌 처리 필요).

**도입 체크리스트**
*   **기술적**: RTT(Round Trip Time)가 제어 간격(Polling Interval)보다 작은지 확인? (Yes -> Polling 적합)
*   **운영적**: 단일 장애점(SPOF, Single Point of Failure)에 대한 이중화(Master Redundancy)가 되어 있는가?
*   **보안적**: 무단 스테이션이 링크에 접속을 시도할 때 이를 차단하는 인증(Authentication) 절차가 포함되어 있는가?

**안티패턴 (Anti-pattern)**
*   **고속 LAN에서의 Software Polling**: 1Gbps 이상의 고속 이더넷에서 소프트웨어적으로 Polling을 구현하면 CPU 사용률이 급증하여 Context Switching 오버헤드로 인해 시스템 성능이 급격히 저하된다. 이 경우 하드웨어 인터럽트 기반의 DMA(Direct Memory Access)를 병행해야 한다.

**📢 섹션 요약 비유**: 회선 제어 방식의 선택은 '택시 운행 방식'을 결정하는 것과 같습니다. 요금을 받고 빠르게 이동해야 하는 개인 택시(ENQ/ACK)가 있고, 정해진 노선과 시간을 지키는 시내버스(Polling)가 있습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량/정성 기대효과**

| 지표 (Metrics) | 개선 전 (No Discipline) | 개선 후 (Line Discipline Applied) |
|:---|:---|:---|
| **데이터 충돌률** | > 30% (High Jitter) | < 0.1% (Controlled) |
| **네트워크 효율성** | 40% (Retransmission High) | 85% (Optimized Flow) |
| **지연 시간 편차** | Unpredictable (예측 불가) | Deterministic (예측 가능) |
| **보안성** | 도청 및 데이터 파손 위험 높음 | 세션 기반 인증으로 무결성 확보 |

**미래 전망 및 표준**
과거에는 IBM BISYNC나 SDLC와 같이 독점적 프로토콜이었으나, 현재는 **HDLC (High-Level Data Link Control)**, **PPP (Point-to-Point Protocol)**의 핵심 요소로 통합되어 표준화되었다. 최근에는 **MQTT (Message Queuing Telemetry Transport)**와 같은 IoT 프로토콜의 Pub/Sub 구조에서 Polling 개념이 발전적으로 적용되고 있다.

**관련 표준**
*   **ISO 3309**: HDLC 프레임 구조
*   **ISO 4335**: HDLC 요소 (프로시저)
*   **RFC 1662**: