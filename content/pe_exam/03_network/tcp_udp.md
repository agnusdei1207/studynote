+++
title = "TCP와 UDP (Transmission Control Protocol / User Datagram Protocol)"
date = 2025-03-01

[extra]
categories = "pe_exam-network"
+++

# TCP와 UDP (Transmission Control Protocol / User Datagram Protocol)

## 핵심 인사이트 (3줄 요약)
> **TCP**는 연결형 프로토콜로 신뢰성, 순서 보장, 흐름/혼잡 제어를 제공하며, **UDP**는 비연결형으로 빠른 전송에 집중한다. 파일 전송·웹·이메일은 TCP, 실시간 스트리밍·게임·DNS는 UDP가 적합하다. 최신 트렌드는 QUIC(HTTP/3)처럼 UDP 기반에 TCP 신뢰성을 더하는 하이브리드 방식이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: TCP(Transmission Control Protocol)와 UDP(User Datagram Protocol)는 **전송 계층(Transport Layer, OSI 4계층)**의 핵심 프로토콜로, 애플리케이션 데이터를 네트워크로 전송하는 방식을 정의한다. TCP는 **연결 지향형**으로 신뢰성 있는 데이터 전송을 보장하고, UDP는 **비연결형**으로 최소한의 오버헤드로 빠른 전송을 제공한다.

> 💡 **비유**:
> - **TCP는 "등기 우편"**: 수신 확인, 순서 보장, 분실 시 재발송. 느리지만 확실하다.
> - **UDP는 "엽서"**: 보내고 나면 끝. 확인 없음. 빠르지만 분실 가능.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - IP의 한계**: IP(Internet Protocol)는 최선형(Best-effort) 전달만 제공하여, 패킷 손실, 순서 뒤섞임, 중복 수신이 발생했다. 애플리케이션마다 신뢰성을 직접 구현해야 했다.
2. **기술적 필요성**: 다양한 애플리케이션 요구사항(신뢰성 vs 속도)을 만족하는 **두 가지 전송 방식**이 필요했다. 이메일/파일은 신뢰성이, 실시간 통신은 속도가 중요하다.
3. **시장/산업 요구**: 인터넷 확산과 함께 **웹, 이메일, 파일 전송** 등 신뢰성 필요 서비스와 **스트리밍, 게임, VoIP** 등 실시간 서비스가 동시에 성장했다.

**핵심 목적**: 애플리케이션의 특성에 맞는 전송 서비스를 제공하여, 신뢰성과 속도의 균형을 맞추는 것이다.

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **포트(Port)** | 애플리케이션 식별자 | 16비트(0~65535), 잘알려진/등록/동적 포트 | 아파트 호수 |
| **세그먼트/데이터그램** | 전송 계층 데이터 단위 | TCP: 세그먼트, UDP: 데이터그램 | 우편물 |
| **TCP 헤더** | 제어 정보 (20~60바이트) | Sequence, ACK, Flags, Window | 우편물의 배송 정보 |
| **UDP 헤더** | 최소 제어 정보 (8바이트) | Port, Length, Checksum만 | 엽서의 주소 |
| **소켓(Socket)** | 통신 종단점 | IP + Port, 양방향 통신 채널 | 우편함 |
| **슬라이딩 윈도우** | 흐름 제어 기법 | 송신 윈도우 크기로 전송량 조절 | 한 번에 보낼 수 있는 우편물 수 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TCP 헤더 구조 (20바이트 기본)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   0                   15                  31                               │
│   ┌─────────────────────┬─────────────────────┐                           │
│   │   Source Port (16)  │ Destination Port(16)│  0-3 bytes                │
│   ├─────────────────────┴─────────────────────┤                           │
│   │           Sequence Number (32)             │  4-7 bytes                │
│   ├────────────────────────────────────────────┤                           │
│   │         Acknowledgment Number (32)         │  8-11 bytes               │
│   ├────┬────┬───────────┬──────────────────────┤                           │
│   │HLEN│Res │  Flags    │    Window Size (16)  │  12-15 bytes              │
│   │4bit│6bit│  6bit     │                       │                           │
│   ├─────────────────────┼──────────────────────┤                           │
│   │   Checksum (16)     │  Urgent Pointer (16) │  16-19 bytes              │
│   ├─────────────────────┴──────────────────────┤                           │
│   │              Options (가변)                 │  20+ bytes                │
│   └────────────────────────────────────────────┘                           │
│                                                                             │
│   TCP Flags (6비트):                                                        │
│   ┌─────┬─────┬─────┬─────┬─────┬─────┐                                    │
│   │ URG │ ACK │ PSH │ RST │ SYN │ FIN │                                    │
│   │긴급 │확인 │밀어넣│재설정│연결설정│종료 │                                    │
│   └─────┴─────┴─────┴─────┴─────┴─────┘                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        UDP 헤더 구조 (8바이트 고정)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│   0                   15                  31                               │
│   ┌─────────────────────┬─────────────────────┐                            │
│   │   Source Port (16)  │ Destination Port(16)│  0-3 bytes                 │
│   ├─────────────────────┼─────────────────────┤                            │
│   │    Length (16)      │   Checksum (16)     │  4-7 bytes                 │
│   └─────────────────────┴─────────────────────┘                            │
│                                                                             │
│   특징: 8바이트로 매우 간단, 연결 설정 없음, 확인 응답 없음                 │
└─────────────────────────────────────────────────────────────────────────────┘

TCP 연결 관리:
┌─────────────────────────────────────────────────────────────────────────────┐
│  3-Way Handshake (연결 설정)                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Client                                    Server                          │
│    │                                         │                             │
│    │ ──────── SYN (SEQ=x) ────────────────→ │  1단계: 연결 요청            │
│    │           (SYN=1, ACK=0)                │     SYN_SENT 상태           │
│    │                                         │                             │
│    │ ←─────── SYN+ACK (SEQ=y, ACK=x+1) ───── │  2단계: 요청 수락 + 확인     │
│    │           (SYN=1, ACK=1)                │     SYN_RECEIVED 상태       │
│    │                                         │                             │
│    │ ──────── ACK (SEQ=x+1, ACK=y+1) ──────→ │  3단계: 최종 확인            │
│    │           (SYN=0, ACK=1)                │     ESTABLISHED 상태        │
│    │                                         │                             │
│    │            [연결 완료]                   │                             │
│    │←═══════════════════════════════════════→│                             │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  4-Way Handshake (연결 종료)                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Client                                    Server                          │
│    │                                         │                             │
│    │ ──────── FIN (SEQ=u) ────────────────→ │  1단계: 종료 요청            │
│    │           (FIN=1, ACK=0)                │     FIN_WAIT_1 상태         │
│    │                                         │                             │
│    │ ←─────── ACK (ACK=u+1) ──────────────── │  2단계: 요청 확인            │
│    │                                         │     CLOSE_WAIT 상태         │
│    │                                         │                             │
│    │ ←─────── FIN (SEQ=w) ──────────────── │  3단계: 서버 종료 요청        │
│    │           (FIN=1, ACK=1)                │     LAST_ACK 상태           │
│    │                                         │                             │
│    │ ──────── ACK (ACK=w+1) ──────────────→ │  4단계: 최종 확인            │
│    │                                         │     CLOSED 상태             │
│    │                                         │                             │
│    │  [TIME_WAIT: 2MSL 대기 후 CLOSED]       │                             │
│                                                                             │
│  MSL(Max Segment Lifetime): 세그먼트 최대 생존 시간 (일반적 2분)            │
│  TIME_WAIT: 마지막 ACK 유실 시 재전송 대기                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 데이터 생성 → ② 세그먼트/데이터그램 생성 → ③ 전송 → ④ 수신 확인(TCP) → ⑤ 재조립
```

- **TCP 데이터 전송 과정**:
  - **1단계 - 연결 설정 (3-Way Handshake)**:
    - 클라이언트가 SYN 패킷 전송 (초기 시퀀스 번호 x)
    - 서버가 SYN+ACK 응답 (자신의 시퀀스 y, 클라이언트 ACK x+1)
    - 클라이언트가 ACK 전송 (ACK y+1)
    - 양방향 연결 수립 완료

  - **2단계 - 데이터 전송 (슬라이딩 윈도우)**:
    - 송신측: 윈도우 크기만큼 연속 전송 (ACK 기다리지 않음)
    - 수신측: 순차적 수신 시 Cumulative ACK (예: ACK 101 = 100까지 수신)
    - 송신측: ACK 받은 만큼 윈도우 슬라이드

  - **3단계 - 흐름 제어 (Flow Control)**:
    - 수신측이 Window Size로 수신 가능량 통지
    - 송신측은 Window Size 이내로만 전송
    - Zero Window: 수신측 버퍼 꽉 차면 전송 중지

  - **4단계 - 혼잡 제어 (Congestion Control)**:
    - Slow Start: cwnd 1부터 지수 증가 (1→2→4→8...)
    - Congestion Avoidance: ssthresh 이후 선형 증가
    - Fast Retransmit: 중복 ACK 3회 시 즉시 재전송
    - Fast Recovery: cwnd 절반으로 줄이고 계속

  - **5단계 - 연결 종료 (4-Way Handshake)**:
    - 양측 각각 FIN 전송, ACK 응답
    - TIME_WAIT (2MSL) 후 완전 종료

- **UDP 데이터 전송 과정**:
  - **1단계 - 데이터그램 생성**: 헤더(8바이트) + 데이터
  - **2단계 - 전송**: 연결 설정 없이 즉시 전송
  - **3단계 - 수신**: 수신측에서 Checksum 검증만 수행
  - **특징**: 순서, 중복, 손실 모두 애플리케이션에서 처리

**핵심 알고리즘/공식** (해당 시 필수):
```
TCP 신뢰성 보장 메커니즘:
┌─────────────────────────────────────────────────────────────────┐
│  1. 순서 보장 (Sequence Number)                                 │
│     - 각 바이트에 고유 번호 부여                                 │
│     - SEQ=1000, LEN=100 → 다음 SEQ=1100                         │
│                                                                 │
│  2. 재전송 (Retransmission)                                     │
│     - RTO(Retransmission Timeout) 내 ACK 없으면 재전송          │
│     - RTO = RTT 변동성 고려한 동적 계산                          │
│     - RTO = SRTT + 4×RTTVAR (Jacobson/Karels 알고리즘)          │
│                                                                 │
│  3. 흐름 제어 (Flow Control)                                    │
│     - Window Size = min(rwnd, cwnd)                             │
│     - rwnd: 수신측 여유 버퍼 (Receiver Window)                  │
│     - cwnd: 송신측 혼잡 윈도우 (Congestion Window)              │
│                                                                 │
│  4. 혼잡 제어 (Congestion Control)                              │
│     - Slow Start: cwnd = cwnd × 2 (매 RTT)                      │
│     - Congestion Avoidance: cwnd = cwnd + 1 (매 RTT)            │
│     - Timeout 시: ssthresh = cwnd/2, cwnd = 1                   │
│     - 3 Duplicate ACKs: ssthresh = cwnd/2, cwnd = ssthresh + 3 │
└─────────────────────────────────────────────────────────────────┘

대역폭 지연 곱 (Bandwidth-Delay Product):
BDP = Bandwidth × RTT
예: 1Gbps 링크, RTT 50ms
BDP = 10^9 × 0.05 = 50MB (윈도우 크기가 최소 50MB여야 링크 활용)

TCP 처리량 공식:
Throughput = (Window Size) / RTT
예: Window=64KB, RTT=50ms
Throughput = 65536 / 0.05 = 1.31 Mbps
```

**코드 예시** (필수: Python 또는 의사코드):
```python
# TCP 슬라이딩 윈도우 시뮬레이터
import time
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class SegmentState(Enum):
    NOT_SENT = 0
    SENT = 1
    ACKED = 2

@dataclass
class Segment:
    seq: int
    data: bytes
    state: SegmentState = SegmentState.NOT_SENT
    send_time: float = 0

class TCPSimulator:
    def __init__(self, window_size: int = 4, segment_size: int = 1000,
                 rtt_ms: float = 50, loss_rate: float = 0.1):
        self.window_size = window_size  # 윈도우 크기 (세그먼트 수)
        self.segment_size = segment_size  # 세그먼트 크기 (바이트)
        self.rtt = rtt_ms / 1000  # RTT (초)
        self.loss_rate = loss_rate  # 패킷 손실률

        # 송신측 상태
        self.segments: List[Segment] = []
        self.base_seq = 0  # 가장 오래된 미확인 시퀀스
        self.next_seq = 0  # 다음 전송할 시퀀스

        # 통계
        self.bytes_sent = 0
        self.bytes_acked = 0
        self.retransmissions = 0

    def send_data(self, data: bytes):
        """데이터를 세그먼트로 분할하여 전송 준비"""
        for i in range(0, len(data), self.segment_size):
            segment_data = data[i:i+self.segment_size]
            self.segments.append(Segment(seq=i, data=segment_data))

    def transmit_window(self) -> List[Segment]:
        """현재 윈도우 내 세그먼트 전송"""
        import random

        transmitted = []
        window_end = min(self.base_seq + self.window_size, len(self.segments))

        for i in range(self.base_seq, window_end):
            seg = self.segments[i]
            if seg.state == SegmentState.NOT_SENT or \
               (seg.state == SegmentState.SENT and self._timeout(seg)):
                # 전송 (또는 재전송)
                seg.state = SegmentState.SENT
                seg.send_time = time.time()

                # 패킷 손실 시뮬레이션
                if random.random() < self.loss_rate:
                    print(f"  [LOSS] Segment {seg.seq} lost!")
                else:
                    transmitted.append(seg)
                    self.bytes_sent += len(seg.data)
                    if seg.state == SegmentState.SENT:
                        self.retransmissions += 1

                self.next_seq = i + 1

        return transmitted

    def _timeout(self, segment: Segment) -> bool:
        """타임아웃 확인"""
        return (time.time() - segment.send_time) > (self.rtt * 2)

    def receive_ack(self, ack_seq: int):
        """ACK 수신 처리 (Cumulative ACK)"""
        acked_count = 0
        for i in range(self.base_seq, min(ack_seq // self.segment_size + 1, len(self.segments))):
            if self.segments[i].state != SegmentState.ACKED:
                self.segments[i].state = SegmentState.ACKED
                self.bytes_acked += len(self.segments[i].data)
                acked_count += 1

        # 윈도우 슬라이드
        while (self.base_seq < len(self.segments) and
               self.segments[self.base_seq].state == SegmentState.ACKED):
            self.base_seq += 1

        return acked_count

    def is_complete(self) -> bool:
        """전송 완료 확인"""
        return all(seg.state == SegmentState.ACKED for seg in self.segments)

    def get_stats(self):
        """통계 반환"""
        return {
            'total_segments': len(self.segments),
            'bytes_sent': self.bytes_sent,
            'bytes_acked': self.bytes_acked,
            'retransmissions': self.retransmissions,
            'efficiency': f"{self.bytes_acked / self.bytes_sent * 100:.1f}%" if self.bytes_sent > 0 else "N/A"
        }


# UDP 시뮬레이터
class UDPSimulator:
    def __init__(self, loss_rate: float = 0.1):
        self.loss_rate = loss_rate
        self.packets_sent = 0
        self.packets_received = 0

    def send(self, data: bytes) -> bool:
        """UDP 패킷 전송 (연결 설정 없음)"""
        import random
        self.packets_sent += 1

        # Checksum 계산 (간소화)
        checksum = sum(data) % 65536

        # 패킷 손실 시뮬레이션
        if random.random() < self.loss_rate:
            print(f"  [UDP LOSS] Packet lost!")
            return False

        self.packets_received += 1
        return True

    def get_stats(self):
        return {
            'sent': self.packets_sent,
            'received': self.packets_received,
            'loss_rate': f"{(1 - self.packets_received/self.packets_sent)*100:.1f}%" if self.packets_sent > 0 else "N/A"
        }


# 성능 비교 테스트
def compare_protocols():
    print("=== TCP vs UDP 성능 비교 ===\n")

    data = b"Hello, Network!" * 1000  # 15KB 데이터

    # TCP 테스트
    print("[TCP 전송 시작]")
    tcp = TCPSimulator(window_size=4, rtt_ms=50, loss_rate=0.1)
    tcp.send_data(data)

    import random
    while not tcp.is_complete():
        transmitted = tcp.transmit_window()
        # ACK 시뮬레이션
        for seg in transmitted:
            if random.random() > 0.1:  # 90% ACK 도착
                tcp.receive_ack(seg.seq + len(seg.data))
        time.sleep(0.01)

    print(f"TCP 완료: {tcp.get_stats()}\n")

    # UDP 테스트
    print("[UDP 전송 시작]")
    udp = UDPSimulator(loss_rate=0.1)
    for i in range(0, len(data), 1000):
        packet = data[i:i+1000]
        udp.send(packet)

    print(f"UDP 완료: {udp.get_stats()}")


if __name__ == "__main__":
    compare_protocols()
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **TCP 장점**: 신뢰성, 순서 보장, 흐름/혼잡 제어 | **TCP 단점**: 높은 오버헤드, 느린 연결 설정 |
| **UDP 장점**: 빠른 전송, 낮은 오버헤드, 멀티캐스트 | **UDP 단점**: 신뢰성 없음, 순서 보장 없음 |
| **TCP 장점**: 양방향 전이중 통신 | **TCP 단점**: 헤더 크기 (20+ 바이트) |
| **UDP 장점**: 헤더 작음 (8바이트), 단순 | **UDP 단점**: 혼잡 제어 없어 네트워크 부하 가능 |

**TCP vs UDP 종합 비교** (필수: 최소 2개 대안):
| 비교 항목 | TCP | UDP |
|---------|-----|-----|
| **연결 방식** | 연결형 (3-Way Handshake) | 비연결형 |
| **신뢰성** | ★ 보장 (ACK, 재전송) | 미보장 |
| **순서 보장** | ★ 보장 (Sequence Number) | 미보장 |
| **흐름 제어** | ★ 있음 (슬라이딩 윈도우) | 없음 |
| **혼잡 제어** | ★ 있음 (Slow Start, AIMD) | 없음 |
| **전송 속도** | 느림 (오버헤드 큼) | ★ 빠름 |
| **헤더 크기** | 20~60바이트 | ★ 8바이트 |
| **멀티캐스트** | 불가능 | ★ 가능 |
| **실시간성** | 낮음 (지연 발생) | ★ 높음 |
| **적합 용도** | 파일, 웹, 이메일 | 스트리밍, 게임, DNS |
| **대표 앱** | HTTP, FTP, SMTP, SSH | DNS, DHCP, VoIP, 게임 |

> **★ 선택 기준**:
> - **TCP**: 데이터 무결성 중요, 순서 중요, 분실 용납 불가 (파일, 결제, 이메일)
> - **UDP**: 지연 최소화 중요, 약간의 손실 허용 (실시간 스트리밍, 게임, VoIP)

**전송 계층 프로토콜 비교**:
| 프로토콜 | 특징 | 용도 |
|---------|------|------|
| **TCP** | 신뢰성, 연결형 | 웹, 파일, 이메일 |
| **UDP** | 비신뢰, 비연결 | DNS, 스트리밍 |
| **SCTP** | 메시지 지향, 멀티홈 | 통신, 신호 |
| **QUIC** | UDP 기반 + TCP 신뢰성 | ★ HTTP/3 |
| **DCCP** | 비신뢰 + 혼잡제어 | 스트리밍 |

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **웹 서비스** | HTTP/2(TCP) 또는 HTTP/3(QUIC) 적용 | 페이지 로딩 30% 단축 |
| **실시간 스트리밍** | UDP + FEC(Forward Error Correction) | 지연 100ms 이하, 손실률 1% 이하 |
| **온라인 게임** | UDP + 애플리케이션 레벨 신뢰성 | 지연 50ms 이하, 패킷 손실 복구 |
| **파일 전송** | TCP BBR 혼잡 제어 알고리즘 | 대역폭 활용률 95% 이상 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1: 넷플릭스** - UDP 기반 스트리밍 + 적응형 비트레이트. FEC로 패킷 손실 복구, 지연 2초 이하 달성.
- **사례 2: 구글 HTTP/3 (QUIC)** - UDP 기반으로 0-RTT 연결, TCP Handshake 지연 제거. 페이지 로딩 30% 향상.
- **사례 3: 카카오톡 VoIP** - UDP + 자체 프로토콜로 음성 통화. 지연 150ms, 패킷 손실 5%까지 품질 유지.

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 애플리케이션 요구사항 분석 (신뢰성 vs 지연)
   - 네트워크 환경 (대역폭, 지연, 손실률)
   - 프로토콜 튜닝 (TCP Window, Keep-Alive)
   - 방화벽/NAT 통과 (UDP 차단 가능성)

2. **운영적**:
   - 모니터링 (RTT, 패킷 손실률, 처리량)
   - 장애 대응 (타임아웃, 재전송 설정)
   - 로드 밸런싱 (세션 유지)
   - 디버깅 (Wireshark, tcpdump)

3. **보안적**:
   - TCP: SYN Flood, TCP Reset 공격
   - UDP: Amplification 공격 (DNS, NTP)
   - 방화벽 규칙, 포트 필터링
   - TLS/DTLS 암호화

4. **경제적**:
   - 대역폭 비용 (TCP 오버헤드 고려)
   - CDN 활용 (지연 최소화)
   - 하드웨어 가속 (TCP Offload)
   - 클라우드 비용 (데이터 전송량)

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **TCP를 실시간에 사용**: TCP의 재전송·혼잡제어로 인해 지연 급증 → 실시간은 UDP + 앱 레벨 제어
- ❌ **UDP를 신뢰성 필요 서비스에 사용**: 파일 전송에 UDP 사용 시 데이터 손실 → TCP 또는 QUIC
- ❌ **윈도우 크기 튜닝 무시**: 고대역폭·고지연 링크에서 BDP > Window Size → 대역폭 낭비

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 TCP/UDP 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                    TCP / UDP (전송 계층)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IP ←──→ TCP/UDP ←──→ 포트                                      │
│   ↓         ↓           ↓                                       │
│  라우팅    흐름제어    소켓                                      │
│   ↓         ↓           ↓                                       │
│  OSI7계층  혼잡제어   HTTP/DNS                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| IP | 하위 계층 | TCP/UDP가 IP 위에서 동작 | `[IP](./ip.md)` |
| OSI 7계층 | 계층 구조 | 전송 계층(4계층) 프로토콜 | `[OSI 7계층](./osi_7layer.md)` |
| 포트 | 주소 식별 | 애플리케이션 구분 | `[포트](./port.md)` |
| 소켓 | 프로그래밍 인터페이스 | TCP/UDP 통신 종단점 | `[소켓](./socket.md)` |
| HTTP | 상위 계층 | TCP/UDP 기반 애플리케이션 | `[HTTP](./http.md)` |
| QUIC | 차세대 프로토콜 | UDP 기반 TCP 대체 | `[QUIC](./quic.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 신뢰성 | TCP로 데이터 무결성 보장 | 패킷 손실 0% |
| 성능 | UDP로 지연 최소화 | 응답 시간 50ms 이하 |
| 효율성 | 적절한 프로토콜 선택 | 대역폭 활용률 90% 이상 |
| 사용자 경험 | 서비스별 최적화 | 체감 품질 90% 이상 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**:
   - **QUIC (HTTP/3)**: UDP 기반으로 TCP의 신뢰성 + UDP의 속도 결합
   - **BBR 혼잡 제어**: Google의 새로운 혼잡 제어 알고리즘, 대역폭 추정 기반
   - **Multipath TCP**: 여러 네트워크 경로 동시 사용

2. **시장 트렌드**:
   - HTTP/3의 빠른 채택 (Chrome, Safari, Cloudflare)
   - 실시간 통신(WebRTC)의 UDP 활용 확대
   - 5G/6G에서의 초저지연 통신

3. **후속 기술**:
   - **MP-QUIC**: Multipath + QUIC 결합
   - **L4S (Low Latency, Low Loss, Scalable Throughput)**: 지연 기반 혼잡 제어
   - **SRP (Service Reflection Protocol)**: 서비스 지향 전송

> **결론**: TCP와 UDP는 인터넷의 **전송 계층 양대 산맥**으로, 각각 신뢰성과 속도라는 상보적 가치를 제공한다. 최근 QUIC(HTTP/3)처럼 UDP 기반에 TCP의 신뢰성을 더하는 하이브리드 방식이 대세이며, 5G/6G 시대의 초저지연 통신을 지원할 새로운 프로토콜이 계속 진화할 것이다.

> **※ 참고 표준**: RFC 793 (TCP), RFC 768 (UDP), RFC 9000 (QUIC), RFC 9001 (QUIC TLS), RFC 9002 (QUIC Loss Detection)

---

## 어린이를 위한 종합 설명 (필수)

**TCP와 UDP는 "편지 보내기" 방법이야!**

친구에게 편지를 보내고 싶어요. 두 가지 방법이 있어요.

**TCP는 "등기 우편"이야:**

1. 친구에게 "편지 보내도 돼?"라고 물어봐요 (SYN)
2. 친구가 "응, 보내!"라고 답해요 (SYN+ACK)
3. "알겠어, 지금 보낼게!"라고 확인해요 (ACK)
4. 편지를 보내고 **확인 도착**을 기다려요
5. 편지가 도착하면 친구가 "받았어!"라고 해요 (ACK)
6. 안 오면 **다시 보내요**

```
나 ──── "보내도 돼?" ────→ 친구
나 ←── "응, 보내!" ─────── 친구
나 ──── "알겠어!" ────────→ 친구
나 ──── [편지] ───────────→ 친구
나 ←── "받았어!" ────────── 친구
```

**장점**: 확실히 전달돼요! 순서도 지켜요!
**단점**: 느려요... 확인 많이 해야 해요.

**UDP는 "엽서"예요:**

1. 그냥 보내요! 끝!
2. 친구가 받았는지 몰라요
3. 빠르지만 잃어버릴 수 있어요

```
나 ──── [엽서] ────→ 친구 (끝!)
```

**장점**: 엄청 빨라요! 확인 안 기다려요!
**단점**: 잃어버리면 어쩔 수 없어요...

**언제 뭘 쓸까요?**

- 📄 **파일 보내기**: TCP (하나라도 잃어버리면 안 돼요!)
- 🎮 **온라인 게임**: UDP (빠르지 않으면 렉 걸려요!)
- 🎬 **동영상 보기**: UDP (살짝 끊겨도 괜찮아요)
- 📧 **이메일**: TCP (내용이 중요해요!)

**최신 기술 (QUIC):**

요즘은 **UDP를 쓰면서도 TCP처럼 확실하게** 보내는 새로운 방법도 있어요! 🚀

---
