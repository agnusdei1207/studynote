+++
title = "416-420. TCP 연결 설정 및 종료 (Handshake)"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 416
+++

# 416-420. TCP 연결 설정 및 종료 (Handshake)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP (Transmission Control Protocol)의 신뢰성은 연결 지향성에서 기인하며, **3-Way Handshake**는 논리적 회선 개설을 위한 동기화(Synchronization) 과정이고, **4-Way Handshake**는 양방향(Full-Duplex) 스트림의 안전한 종료를 위한 절차이다.
> 2. **가치**: ISN (Initial Sequence Number)의 난수화를 통해 **Sequence Number Prediction Attack**을 방지하고, **TIME_WAIT** 상태를 통해 지연 패킷으로 인한 데이터 혼잡(Data Corruption) 및 **2MSL (Maximum Segment Lifetime)** 동안의 세션 복구를 보장한다.
> 3. **융합**: OSI 7계층의 **Transport Layer**에 위치하여 하위 **Network Layer(IP)**의 비신뢰성을 보완하며, 상위 **Application Layer(HTTP)**의 안정적인 통신을 담보하는 인터넷 통신의 핵심 인프라이다.

---

### Ⅰ. 개요 (Context & Background)

TCP (Transmission Control Protocol)는 네트워크 상에서 데이터를 오차 없이 순서대로 전송하기 위해 설계된 **연결 지향형**(Connection-Oriented) 프로토콜입니다. 이는 데이터를 보내기 전에 송신자와 수신자가 논리적인 회선(Logical Circuit)을 확립하고, 통신이 끝나면 이를 명확히 해제하는 전화 통신 방식과 유사합니다. 이 과정에서 필수적인 것이 **Handshake** 교환입니다.

**💡 비유**
TCP 연결 설정은 두 사람이 중요한 대화를 나누기 전에 "지금 들리나요?", "네, 당신 말도 들려요?"라고 서로 대화 채널이 열렸음을 확인하는 작업이며, 연결 종료는 "이만 끊겠습니다", "네, 알겠습니다"라고 서로의 마무리를 확인하는 정중한 인사입니다.

**등장 배경**
1.  **기존 한계**: 초기 네트워크망에서는 패킷 손실이나 순서 바뀜이 빈번했으며, 수신 측의 버퍼 상태를 고려하지 않은 무작정 전송은 네트워크 혼잡(Congestion)을 가중시켰습니다.
2.  **혁신적 패러다임**: TCP는 **RFC 793** (1981) 이후로 "Connection-oriented" 모델을 도입하여, **Three-way Handshake**를 통해 양쪽의 **Initial Sequence Number (ISN)**을 안전하게 교환하고 수신 윈도우(Receive Window) 크기를 협상하여 신뢰성을 확보했습니다.
3.  **현재의 비즈니스 요구**: 현대의 웹(HTTP/HTTPS), 금융 거래, 데이터베이스 복제 등 데이터 무결성이 생명인 서비스들은 TCP의 이러한 엄격한 연결 관리를 필수적으로 의존합니다.

**📢 섹션 요약 비유**: 연결 설정은 마치 고속도로에 진입하기 전 톨게이트에서 하이패스 단말기가 정상 작동하는지 **' 삐 소리'**를 서로 주고받으며 확인하는 과정과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

TCP 연결 설정과 종료는 플래그 비트(SYN, ACK, FIN)와 시퀀스 번호(Sequence Number)가 조합하여 작동하는 정교한 상태 머신(State Machine)입니다.

#### 1. 구성 요소 (State & Flags)
| 요소 | 역할 | 내부 동작 | 비고 |
|:---|:---|:---|:---|
| **SYN (Synchronize)** | 연결 요청 및 ISN 전달 | 송신측의 **Initial Sequence Number (ISN)**을 수신측에 알림 | 순서 시작점 |
| **ACK (Acknowledgment)** | 수신 확인 | `Ack Number = Expected Seq + 1` 형태로 다음 받을 번호 알림 | 누적 확인 |
| **FIN (Finish)** | 연결 종료 요청 | 더 이상 보낼 데이터가 없음을 선언 | Half-Close 유도 |
| **ISN (Initial Seq No)** | 초기 시퀀스 번호 | 보안 목적(예측 불가능성)을 위해 Random 생성 | **RFC 1948** 준수 |
| **2MSL** | 최대 세그먼트 수명 | 패킷이 네트워크에 존재할 수 있는 최대 시간의 2배 | 약 60초 (OS별 상이) |

#### 2. 3-Way Handshake (연결 설정) 메커니즘
이 과정은 양쪽 호스트가 각각 보낼 패킷의 번호를 **0이 아닌 무작위 값(ISN)**으로 동기화하는 핵심 과정입니다.

```ascii
[TCP 3-Way Handshake: Connection Establishment]

   Client                                              Server
   (Active Open)                                       (Passive Open)

1. [SYN] X=ISN_C -------------------------------------> | (SYN_SENT)
        |  (Send: SYN=1, Seq=X)                        | Listen
        |                                               v
2. [SYN+ACK] <----------------------------------------- Y=ISN_S, ACK=X+1
        |  (Recv: SYN=1, Ack=X+1)                      | (SYN_RCVD)
        |  (Send: SYN=1, Seq=Y, Ack=X+1)               |
3. [ACK] X+1 ----------------------------------------> | v
        |  (Send: ACK=1, Seq=X+1, Ack=Y+1)             | (ESTABLISHED)
   (ESTABLISHED) <------------------------------------- v
```
**(해설)**
1.  **Step 1 (SYN)**: 클라이언트는 `SYN` 플래그와 자신의 **ISN (Initial Sequence Number, 여기서는 X)**을 담아 전송합니다. 이때 `SYN_SENT` 상태로 대기합니다.
2.  **Step 2 (SYN+ACK)**: 서버는 `SYN`을 받으면 `X+1`을 **ACK Number**로 담아 수신을 확인함과 동시에, 자신의 **ISN (여기서는 Y)**을 포함한 `SYN` 패킷을 클라이언트로 보냅니다. 이를 **SYN+ACK**라 합니다.
3.  **Step 3 (ACK)**: 클라이언트는 서버의 **ISN(Y)**에 대해 `Y+1`을 **ACK Number**로 하여 최종 확인을 보냅니다. 이 패킷이 도착하면 서버는 연결을 수락하고 `ESTABLISHED` 상태가 되어 데이터 전송을 시작합니다.

#### 3. 4-Way Handshake (연결 종료) 메커니즘
TCP는 **Full-Duplex(전이중)** 통신이므로, 한쪽 방향의 스트림을 닫아도 다른 한쪽은 계속 보낼 수 있습니다. 이로 인해 종료 과정은 설정보다 한 단계가 더 복잡합니다.

```ascii
[TCP 4-Way Handshake: Connection Termination]

   Client                                              Server
   (Application Close)                                 (Application Close)

1. [FIN] Seq=u --------------------------------------> | (ESTABLISHED)
        |  (Send: FIN=1, Seq=u)                        | v
   (FIN_WAIT_1)                                        | (CLOSE_WAIT)
2. [ACK] v=u+1 <-------------------------------------- |
        |  (Recv: ACK=1, Ack=u+1)                      | v
   (FIN_WAIT_2)                                        | (Send remaining data...)
        |                                               | (App calls Close)
3. [FIN] --------------------------------------------> | v
        |  (Recv: FIN=1, Seq=w)                        | (LAST_ACK)
4. [ACK] w+1 ---------------------------------------> |
        |  (Send: ACK=1, Ack=w+1)                      | (CLOSED)
   (TIME_WAIT) ---------------------------------------> v
        |  (Wait 2MSL...)                              | 
   (CLOSED)                                            | 
```
**(해설)**
1.  **Step 1 (FIN)**: 클라이언트 애플리케이션이 `close()`를 호출하면 TCP는 `FIN` 패킷을 보냅니다. 클라이언트는 `FIN_WAIT_1` 상태가 됩니다.
2.  **Step 2 (ACK)**: 서버는 `FIN`을 받고 즉시 `ACK`를 보내며 `CLOSE_WAIT` 상태로 진입합니다. 이때 아직 보내지 못한 데이터가 있다면 계속 전송할 수 있습니다(Half-Close 상태).
3.  **Step 3 (FIN)**: 서버 애플리케이션이 종료를 처리하고 `close()`를 호출하면, 서버는 `FIN` 패킷을 클라이언트로 보냅니다. 상태는 `LAST_ACK`가 됩니다.
4.  **Step 4 (ACK)**: 클라이언트는 `FIN`에 대한 `ACK`를 보내고 `FIN_WAIT_2`에서 `TIME_WAIT` 상태로 넘어갑니다.

#### 4. 핵심 알고리즘: TIME_WAIT의 계산
클라이언트가 마지막 ACK를 보내고 바로 소켓을 닫지 않고 **TIME_WAIT** 상태로 대기하는 시간은 다음과 같이 정의됩니다.
$$ \text{Time}_{\text{wait}} = 2 \times \text{MSL} $$
여기서 **MSL (Maximum Segment Lifetime)**은 패킷이 네트워크 상에서 존재할 수 있는 최대 시간입니다(보통 30초~1분 추정). 따라서 **TIME_WAIT**은 약 1~4분 정도 지속됩니다.

**📢 섹션 요약 비유**: **3-Way Handshake**는 약속 장소에서 서로 눈을 맞추고 인사를 나누는 "만남의 루틴"이며, **4-Way Handshake**는 "나 먼저 갈게(ACK 확인 후 기다림)" -> "응, 남은 일 처리하고 갈게(FIN)" -> "그럼 조심해서 가(ACK)" -> "마지막까지 뒤를 돌아보며 배웅(TIME_WAIT)"하는 이별의 절차와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 3-Way vs 4-Way 구조적 비교
| 구분 | 3-Way Handshake | 4-Way Handshake |
|:---|:---|:---|
| **목적** | 논리적 연결 생성, 파라미터 동기화 | 논리적 연결 해제, 자원 해제 |
| **핵심 플래그** | SYN, ACK | FIN, ACK |
| **양방향 처리** | 한 번의 교환(SYN+ACK)으로 양방향 동시 설정 | 각 방향별 종료 요청(FIN)이 개별적으로 필요 |
| **주요 상태** | LISTEN → SYN_SENT → SYN_RCVD → ESTABLISHED | ESTABLISHED → FIN_WAIT1 → CLOSE_WAIT → TIME_WAIT |
| **패킷 수** | 3개 | 4개 |

#### 2. 타 과목 융합 관점 (OS & Security)
-   **OS (Operating System)와의 연계**: `TIME_WAIT` 상태는 OS 커널 레벨에서 자원을 점유합니다. 초당 수만 건의 연결을 생성/종료하는 웹 서버 환경에서, 이 포트가 즉시 재사용되지 않으므로 **"Too many open files"** 에러나 **EADDRNOTAVAIL** 에러를 유발할 수 있습니다. 이를 해결하기 위해 OS는 `SO_REUSEADDR` 옵션이나 `tw_reuse` 커널 파라미터를 제공합니다.
-   **Security (보안)와의 연계**: Handshake 과정 자체가 **DoS (Denial of Service)** 공격의 대상이 될 수 있습니다. 공격자가 SYN 패킷만 무수히 보내 `SYN_RECEIVED` 상태의 대기열(**Backlog Queue**)을 채워버리는 **SYN Flooding 공격**이 대표적입니다. 이를 방지하기 위해 **SYN Cookie** 기술이 사용되어, 서버가 자원을 할당하지 않고 암호학적 방식으로 ISN을 쿠키처럼 생성하여 공격을 회피합니다.

**📢 섹션 요약 비유**: 3-Way가 "문을 여는 열쇠 교환"이라면, 4-Way는 "방을 나서면서 불을 끄고 문을 잠그는 점검" 과정입니다. 하지만 너무 자주 드나들면(짧은 커넥션) 문을 잠그는 동안(또는 다시 여는 동안) 복도가 막혀 버리는(DoS) 혼잡 현상이 발생할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정
-   **Scenario A: 웹 서버의 갑작스러운 지연 (TIME_WAIT 누적)**
    -   **문제**: 고객사 웹 서버(Apache)가 특정 시간대마다 응답 속도가 급격히 느려집니다. `netstat` 명령어로 확인 결과 다수의 소켓이 `TIME_WAIT` 상태로 머물러 있었습니다.
    -   **판단**: HTTP/1.0 방식(Keep-Alive 미사용)을 사용하면 리소스 하나당 하나의 커넥션을 맺고 바로 끊어 `TIME_WAIT`이 폭발적으로 증가합니다.
    -   **해결**: HTTP **Persistent Connection (Keep-Alive)**를 활성화하여 하나의 커넥션으로 여러 요청을 처리하도록 설정 변경.

-   **Scenario B: 금융 권장 사이트와 연결 실패**
    -   **문제**: 방화벽 뒤의 클라이언트가 특정 금융권 서버에 접속 시 간헐적으로 연결이 실패(RST)합니다.
    -   **판단**: 방화벽이 일정 시간 유휴 상태인 연결을 끊었는데, 양쪽 끝단(OS)은 연결이 살아있다고 착각(Lingering State)하고 데이터를 보내려다가 **RST (Reset)**가 발생한 것입니다.
    -   **해결**: 방화벽의 TCP Session Timeout을 OS의 **Keepalive** 타이머보다 길게 설정하거나, 애플리케이션 레벨에서 주기적으로 **Ping-Pong (Heartbeat)** 패킷을 전송하여 세션을 유지하도록 설계 변경.

#### 2. 도입 체크리스트
-   **기술적**: `net.ipv4.tcp_tw_reuse` (TIME_WAIT 재사용), `net.ipv4.tcp_fin_timeout` (FIN 타임아웃) 등의 커널 파라미터 튜닝 여부 확인.
-   **운영/보안적**: **SYN Cookies** 활성화 여부, 방화벽 룰이 Handshake 플래그(SYN, ACK)를 정확히 필터링하는지(Stateful Inspection) 확인.

#### 3. 안티패턴 (Fatal Flaw)
-   **잘못된 Hard Close**: 4-Way Handshake를 거치지 않고 **RST** 패킷을 강제로 보내 연결을 끊는 로직 구현은 데이터 유실을 초래하며, 네트워크 장비의 상태 추적(State Tracking)을 무력화시켜 보안 장비에 경보를