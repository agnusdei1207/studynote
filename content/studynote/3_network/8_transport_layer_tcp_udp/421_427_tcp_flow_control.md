+++
title = "421-427. TCP 흐름 제어와 슬라이딩 윈도우"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 421
+++

# 421-427. TCP 흐름 제어와 슬라이딩 윈도우

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP (Transmission Control Protocol)의 흐름 제어(Flow Control)는 송신자가 데이터를 쏟아내는 속도를 수신자의 처리 속도에 맞춰 조절하여, 네트워크 혼잡이나 수신측 버퍼 오버플로우를 방지하는 정교한 피드백 시스템이다.
> 2. **가치**: 슬라이딩 윈도우(Sliding Window) 기법을 통해 '확인 응답(ACK) 대기 시간'을 숨겨 네트워크 대역폭 효율을 극대화하며, Silly Window Syndrome(어리석은 윈도우 증후군) 방지 알고리즘을 통해 프로토콜 오버헤드를 최소화한다.
> 3. **융합**: OSI 7계층 중 전송 계층(Transport Layer)의 핵심 기능으로, 애플리케이션 계층의 데이터 신뢰성을 보장하고 하위 계층(네트워크 계층/IP)의 패킷 폭주를 방지하는 가교 역할을 수행한다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 정의**
TCP (Transmission Control Protocol) 흐름 제어는 **데이터의 송신 송신자(Sender)가 수신자(Receiver)의 수용 능력을 초과하여 데이터를 전송함으로써 발생하는 패킷 손실을 방지**하는 기술이다. 이는 단순히 "보내지 말라"는 것이 아니라, 수신자의 현재 버퍼 상태를 실시간으로 알려주어 송신자가 전송 속도를 동적으로 조절하게 하는 능동적인 메커니즘이다.

**💡 비유**
수도꼭지에서 나오는 물의 양을 컵의 크기에 맞춰 조절하는 것과 같다. 컵(수신 버퍼)이 다 차면 수도꼭지(송신자)를 잠그고, 물을 마시(데이터 처리) 공간이 생기면 다시 연다. 여기서 '수도꼭지를 조작하는 손'이 바로 흐름 제어 메커니즘이다.

**등장 배경**
① **기존 한계**: 초기 단순한 Stop-and-Wait 방식(1패킷 전송 후 ACK 대기)은 네트워크 대역폭(Bandwidth)을 극도로 낭비하는 병목 구조였다.
② **혁신적 패러다임**: 파이프라이닝(Pipelining) 개념이 도입되면서 ACK를 기다리지 않고 연속적으로 데이터를 보낼 수 있는 'Sliding Window' 기법이 탄생했다. 이는 RTT (Round-Trip Time) 동안의 유휴 시간을 제거하여 처리량(Throughput)을 획기적으로 높였다.
③ **현재의 비즈니스 요구**: 현대의 고지연/고대역폭(LFN, Long Fat Network) 환경에서는 기가바이트급 버퍼링을 필요로 하며, 빈번한 small packet 전송으로 인한 'Silly Window Syndrome'을 방지하는 지능형 알고리즘이 필수적이 되었다.

**📢 섹션 요약 비유**
TCP 흐름 제어는 **고속도로 톨게이트의 하이패스 차선 관리**와 같다. 차량(데이터)이 톨게이트(수신 버퍼)에 진입할 때 통행료 처리 속도(처리 능력)에 맞춰 진입 속도를 조절하지 않으면, 톨게이트 입구에서 교통 체증(패킷 손실 및 재전송)이 발생하기 때문이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**구성 요소 (표)**

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 주요 파라미터 |
|:---|:---|:---|:---|
| **Send Buffer** | 송신 대기 데이터 저장 | 애플리케이션이 write한 데이터를 운영체제 커널이 보관하는 공간. LastByteSent - LastByteAcked = Flight Size | `SND.UNA`, `SND.NXT` |
| **Receive Buffer** | 수신 데이터 저장 | 도착한 데이터를 애플리케이션이 read할 때까지 보관. 공간이 부족하면 0 알림. | `RCV.WND` |
| **Sliding Window** | 전송량 제어 | 수신측이 알려준 윈도우 크기 내에서 ACK 없이 연속 전송 가능한 범위. | `cwnd`, `rwnd` |
| **ACK (Ack Number)** | 수신 확인 | 현재까지 성공적으로 수신한 바이트의 다음 시퀀스 번호를 알림. Cumulative ACK 특성. | `32-bit Sequence` |
| **TCP Header Options** | 확장 제어 | Window Scale(윈도우 확장), SACK(Selective ACK) 등 협상. | `Shift Count` |

**ASCII 구조 다이어그램 + 해설**

```ascii
[TCP Sliding Window 송신자 버퍼 구조]

  1         2         3         4         5         6
  |---------|---------|---------|---------|---------|
  |   A     |   B     |   C     |   D     |   E     |   F   ...
  ^         ^         ^                  ^         ^
  |         |         |                  |         |
(1)      (2)       (3)                (4)       (5)

(1) SND.UNA  : 전송했으나 아직 ACK를 받지 못한 데이터의 시작 (최초 전송 위치)
(2) SND.NXT  : 다음에 전송할 데이터의 바이트 번호 (전송 포인터)
(3) 윈도우 내부 (Window Size) : ACK를 기다리지 않고 즉시 전송 가능한 영역
(4) 윈도우 경계    : 수신자가 허락한 최대 전송 가능 위치 (SND.UNA + WinSize)
(5) 미사용 공간   : 아직 윈도우에 포함되지 않아 전송할 수 없는 데이터

[상태 전이 예시]
초기 상태: [A][B][C][D][E] (Win=5) -> A,B,C 전송 -> ACK(A) 도착 ->
변경 상태: [B][C][D][E][F] (Win=5) -> 창문이 오른쪽으로 Sliding 됨!
```

**해설**: 위 다이어그램은 송신측의 버퍼 관리를 시각화한 것이다. 윈도우 내부에 있는 데이터(B, C, D)는 네트워크 상으로 쏟아져 나갈 수 있는 '발사 대기 탄'들이다. A에 대한 ACK가 도착하면 `SND.UNA` 포인터가 이동하며 윈도우 자체가 오른쪽으로 미끄러진다(Sliding). 이 덕분에 네트워크는 항상 데이터로 가득 차 유지된다.

**심층 동작 원리 (Step-by-Step)**
1. **협상 (Handshake)**: 3-way Handshake 시 양쪽은 자신의 버퍼 크기(Buffer Size)를 SYN 패킷의 옵션으로 교환한다.
2. **전송 (Transmit)**: 송신자는 `rwnd (Receive Window)` 값만큼 데이터를 연속 전송한다. 이때 패킷 손실 대비를 위해 커널은 복사본을 유지한다.
3. **피드백 (Feedback)**: 수신자는 데이터를 받으면 TCP 헤더의 `Window Size` 필드에 *현재 남은 버퍼 여유분*을 실어서 보낸다.
4. **조절 (Adjust)**: 만약 수신자가 애플리케이션 처리가 늦어 버퍼가 거의 찼다면 `Window Size: 0`을 보낸다. 송신자는 즉시 전송을 멈춘다.
5. **폴백 (Zero Window)**: 수신자가 버퍼를 비우고 나중에 `Window Size > 0` 패킷을 보내야 다시 전송이 재개된다. 이 패킷이 유실되면 Deadlock이 발생하므로 송신자는 Zero Window Probe를 주기적으로 보낸다.

**핵심 알고리즘 & 코드**

*   **Sliding Window Logic (Pseudo Code)**

```python
# Sender Logic
def send_data(socket, data):
    while data_remaining:
        # Check available window size
        rwnd = get_receive_window(socket)
        cwnd = get_congestion_window(socket) # 다음 섹션의 혼잡 제어
        
        sendable_size = min(rwnd, cwnd, len(data))
        
        if sendable_size == 0:
            wait_for_window_update() # Flow Control triggered
            continue
            
        segment = build_segment(data[0:sendable_size])
        socket.send(segment)
        
        # Slide window forward (Logically)
        data = data[sendable_size:]
        
        # Kernel handles retransmission of unacked data
```

**📢 섹션 요약 비유**
슬라이딩 윈도우는 **물류 센터의 컨베이어 벨트**와 같다. 창고(버퍼)가 비어있으면 트럭(데이터)을 마구 보내도 되지만, 창고가 꽉 차면 '입고 대기' 신호를 보내 트럭을 멈춘다. 창고가 조금 비어서 처리 가능 공간이 생기면 바로 그 공간만큼만 다시 트럭을 보내라고 지시하여 효율을 높인다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

**심층 기술 비교: Stop-and-Wait vs. Sliding Window**

| 비교 항목 | Stop-and-Wait (정지-대기) | Sliding Window (슬라이딩 윈도우) |
|:---|:---|:---|
| **전송 효율 (Utilization)** | $ \frac{1}{1 + 2a} $ (a=전파시간/전송시간). 고지망에서 비효율적 | 약 $ \frac{W}{1 + 2a} $ (W=윈도우 크기). 대역폭 거의 100% 활용 가능 |
| **필요 버퍼** | 1 프레임만 저장 가능 | $ N $ (Window Size) 만큼의 버퍼 필요 |
| **구현 복잡도** | 단순 (순서 번호 1비트면 충분) | 복잡 (순서 번호, 타이머, 버퍼 관리 필요) |
| **네트워크 부하** | 매번 ACK 대기로 인해 지연(Latency) 높음 | Pipelining으로 지연 감소, 패킷 폭주 가능성 증가(혼잡 제어 필요) |

**과목 융합 관점**
1.  **네트워크(NW) ↔ 운영체제(OS)**: 흐름 제어는 전송 계층(L4)의 기능이지만, 실제 `Receive Buffer`는 OS 커널 메모리 영역에 할당된다. 따라서 Socket 옵션(`SO_RCVBUF`) 튜닝은 네트워크 성능뿐만 아니라 시스템 메모리 사용량에 직접적인 영향을 미친다.
2.  **애플리케이션 ↔ 네트워크**: 네이글 알고리즘(Nagle's Algorithm)과 같은 흐름 제어 기법은 애플리케이션의 'Write' 시스템 콜 호출 빈도에 따라 네트워크 효율이 달라지므로, 게임 서버 개발자처럼 저지연이 중요한 분야에서는 `TCP_NODELAY` 옵션으로 이를 우회해야 한다.

**Silly Window Syndrome (SWS) 방지 비교**

| 발생 위치 | 문제 현상 | 해결책 (Solution) |
|:---|:---|:---|
| **송신 측 (Sender)** | 1바이트 데이터를 생성할 때마다 즉시 전송하여 40바이트(IP+TCP 헤더)의 오버헤드 유발 | **Nagle's Algorithm**: 충분한 크기(MSS)가 찰 때까지 데이터를 묶어서 보냄 (ACK 기다림) |
| **수신 측 (Receiver)** | 버퍼가 1바이트 비울 때마다 윈도우를 1씩 열어주어, 송신자가 1바이트 패킷을 보내게 함 | **Clark's Solution**: 윈도우를 0으로 유지하다가, 충분한 공간(MSS 절반 이상)이 생기면 한 번에 열어줌 |

**📢 섹션 요약 비유**
Silly Window Syndrome은 **택배 포장 문제**와 같다. 물건(데이터)을 1개씩 따로따로 포장하여 보내면 택배 박스(헤더) 비용이 더 비싸진다. 네이글 알고리즘은 **'주문 모으기'** 서비스로 박스 비용을 아끼고, 클라크 해결책은 **'창고 공간 확보 전까지 알림 유예'**로 인건비(패킷 처리 비용)를 아끼는 전략이다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**실무 시나리오 및 의사결정**

1.  **상황: 대용량 파일 전송 서버 구축**
    *   **문제**: 기본 TCP 윈도우 크기(64KB)로는 1Gbps 네트워크 대역을 100% 채우지 못함. (RTT 10ms 가정 시 $ BDP = Bandwidth \times RTT \approx 1.25MB $ 필요)
    *   **결정**: **Window Scaling Option**을 활성화하여 윈도우 크기를 1MB 이상으로 늘려야 한다. (`net.ipv4.tcp_window_scaling` 커널 파라미터 튜닝)
2.  **상황: 실시간 온라인 게임 서버**
    *   **문제**: 플레이어의 키 입력(작은 패킷)이 네이글 알고리즘에 의해 40ms~200ms 지연되어 버벅거림 발생.
    *   **결정**: 소켓 생성 시 `TCP_NODELAY` 옵션을 설정하여 네이글 알고리즘을 비활성화해야 한다. 대신 애플리케이션 레벨에서 데이터를 묶어서 보내는 로직을 구현하여 네트워크 효율을 관리해야 한다.
3.  **상황: 대용량 트래픽 처리 웹 서버**
    *   **문제**: HTTP Keep-Alive 사용 시 예상치 못한 지연이 발생함.
    *   **결론**: **Delayed ACK**가