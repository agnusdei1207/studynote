+++
title = "428-434. TCP 혼잡 제어 (Congestion Control)"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 428
+++

# 428-434. TCP 혼잡 제어 (Congestion Control)

> **1. 본질**: 흐름 제어(Flow Control)가 '수신자의 버퍼 상태'를 고려하는 것이라면, 혼잡 제어(Congestion Control)는 '네트워크 망(Link/Router)의 처리 용량'을 고려하여 송신 속도를 조절하는 TCP (Transmission Control Protocol)의 핵심 메커니즘입니다.
> **2. 가치**: 패킷 유실 시 단순 재전송으로 인한 망 과부하(Congestive Collapse)를 방지하며, AIMD (Additive Increase Multiplicative Decrease) 알고리즘을 통해 네트워크 대역폭을 여러 발신자가 공평하고 효율적으로 공유하도록 보장합니다.
> **3. 융합**: OSI 7계층 중 전송 계층(Transport Layer)의 기능으로, 라우터(Router)의 큐(Queue) 관리 정책(예: RED, AQM)와 상호작용하며, 최근에는 BBR (Bottleneck Bandwidth and Round-trip propagation time) 같은 최신 혼잡 제어 알고리즘과의 비교 연구가 활발합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
TCP 혼잡 제어는 송신 호스트가 네트워크 내의 패킷 처리량 한계를 초과하여 패킷이 유실되는 것을 방지하기 위해, 네트워크의 혼잡 상태를 추정하고 전송 윈도우(Window)의 크기를 동적으로 조절하는 기술입니다. 송신자는 수신자의 수신 가능 용량을 나타내는 `RWND (Receiver Window)`와 네트워크의 혼잡 상태를 나타내는 `CWND (Congestion Window)` 중 **더 작은 값**을 실제 전송량으로 결정합니다.

수식으로 표현하면 다음과 같습니다.
$$Effective Window = \min(RWND, CWND)$$

### 2. 등장 배경 및 필요성
① **기존 한계**: 초기 인터넷은 단순한 'Stop-and-Wait' 방식이나 고정된 윈도우 크기를 사용했으나, 대역폭이 증가하며 패킷 손실이 발생할 때마다 네트워크 전체가 마비되는 '혼잡 붕괴(Congestive Collapse)' 현상이 발생.
② **혁신적 패러다임**: 1984년 Van Jacobson이 혼잡 제어 알고리즘을 도입하여, 패킷 손실을 '네트워크 혼잡의 신호'로 해석하고 즉시 전송량을 줄이는 자체 조절 기능을 TCP 탑재.
③ **현재 요구**: 클라우드 및 스트리밍 서비스의 증가로 인해, 단순한 패킷 손실 기반 제어를 넘어 지연 시간(Latency)과 대역폭을 동시에 고려하는 고도화된 알고리즘의 필요성 대두.

### 3. 핵심 변수: CWND와 ssthresh
*   **CWND (Congestion Window)**: 네트워크 상황에 따라 송신자가 자율적으로 조절하는 윈도우 크기.
*   **ssthresh (Slow Start Threshold)**: 슬로우 스타트(Slow Start) 단계에서 혼잡 회피(Congestion Avoidance) 단계로 넘어가기 위한 임계값. 패킷 손실 발생 시 CWND 값의 절반으로 갱신됨.

> 📢 **섹션 요약 비유**: 혼잡 제어는 **'안개 낀 고속도로에서의 visibility(가시거리)'**와 같습니다. 운전자(송신자)는 앞차의 간격(ACK)을 통해 도로 상황을 확인하며, 안개가 짙으면 속도를 줄이고(CWND 감소), 도로가 맑으면 속도를 높여(CWND 증가) 사고(망 붕괴)를 미연에 방지합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

TCP 혼잡 제어는 크게 네 가지 단계로 구성되며, 각 단계는 네트워크의 피드백(ACK 수신 및 유실)에 따라 상태 전이(State Transition)를 일으킵니다.

### 1. 구성 요소 상세 분석

| 요소 (Module) | 역할 (Role) | 내부 동작 (Internal Logic) | 트리거 조건 (Trigger) |
|:---:|:---|:---|:---|
| **Slow Start** | 네트워크 대역폭 급속 탐색 | 초기 CWND를 1 MSS로 시작, 매 RTT(Round Trip Time)마다 CWND를 2배로 지수적 증가 (`CWND *= 2`) | 연결 초기 또는 타임아웃 후 재시작 |
| **Congestion Avoidance** | 안정적인 대역폭 점유 | CWND가 `ssthresh`에 도달하면, 매 RTT마다 1 MSS씩만 선형 증가 (`CWND += 1`) | `CWND >= ssthresh` |
| **Fast Retransmit** | 패킷 유실 조기 감지 및 재전송 | 중복된 ACK(Duplicate ACK)가 3개 누적되면 타이머 만료 전 즉시 패킷 재전송 | `3 Dup ACKs` 수신 |
| **Fast Recovery** | 네트워크 혼잡 해后 빠른 복귀 | CWND를 1로 초기화하지 않고, `ssthresh` 값(손실 시 CWND의 절반)으로 설정 후 혼잡 회피 단계로 바로 진입 | Fast Retransmit 수행 후 |

> *참고: MSS (Maximum Segment Size)는 TCP가 한 번에 전송할 수 있는 최대 데이터 크기.*

### 2. 혼잡 제어 상태 전이 다이어그램 (State Machine)

아래 다이어그램은 CWND의 크기 변화와 알고리즘의 상태 전이를 시각화한 것입니다.

```ascii
[CWND Size Graph over Time]
   ^
   |                               (Packet Loss / Timeout)
   |                                    |
   |                                    v
   |      /|\                 _________/
   |     / | \               /         
   |    /  |  \             /           
   |   /   |   \           /            
   |  /    |    \         /             
   | /     |     \       /              
   |/      |      \     /               
   |-------+-------\---/----------------> ssthresh (Threshold Line)
   |        | Slow   \ / Congestion    
   |        | Start   X  Avoidance     
   |        |        / \               
   |        |       /   \              
   |        |      /     \             
   |       /|     /       \            
   |      / |    /         \           
   |     /  |   /           \          
   |    /   |  /             \         
   |   /    | /               \        
   |  /     |/                 \       
   | /      | Fast Recovery     \      
   |/       | (if 3 Dup ACKs)    \     
   +-----------------------------------> Time
```

**다이어그램 해설**:
1.  **Slow Start**: 연결 시작 시 CWND는 1 MSS에서 시작하며 기하급수적으로(1, 2, 4, 8...) 증가하여 `ssthresh` 선에 도달합니다.
2.  **Congestion Avoidance**: `ssthresh`에 도달한 후에는 증가율을 낮춰(선형적으로) 천천히 증가하며 네트워크의 여유 용량을 테스트합니다.
3.  **손실 감지 (Loss Detection)**:
    *   **Case A (3 Dup ACKs)**: 패킷이 유실되었으나 일부 패킷은 통과하고 있는 상황입니다. `Fast Retransmit/Fast Recovery`가 발동되어 CWND를 절반(`ssthresh`)으로 줄이고 선형 증가 구간으로 복귀합니다.
    *   **Case B (Timeout)**: 네트워크가 완전히 막힌 상태입니다. CWND를 1로 초기화하고 `ssthresh`를 절반으로 줄인 뒤, 다시 `Slow Start` 단계부터 시작합니다.

### 3. 핵심 알고리즘 및 의사 코드

**AIMD (Additive Increase Multiplicative Decrease)**
혼잡 제어의 수학적 기반은 AIMD입니다. 망이 여유로울 때는 '합(더하기)'으로 천천히 증가시키고, 혼잡하면 '곱(나누기)'으로 단호하게 감소시킵니다.

```c
// Pseudo-code for TCP Reno Congestion Control

// 초기화
CWND = 1; // MSS 단위
ssthresh = Initial_Threshold;

while (connection_active) {
    packet = send_next_packet();

    // 수신 확인 응답 대기
    event = wait_for_event(); 

    if (event == ACK_RECEIVED) {
        if (CWND < ssthresh) {
            // [Slow Start] 지수 증가
            CWND *= 2; 
        } else {
            // [Congestion Avoidance] 선형 증가
            // (실제로는 매 ACK마다 1/CWND씩 증가시켜 RTT마다 1씩 증가하게 구현)
            CWND += 1; 
        }
    }
    else if (event == THREE_DUPLICATE_ACKS) {
        // [Fast Retransmit & Fast Recovery]
        ssthresh = CWND / 2; // 임계치를 절반으로 갱신
        CWND = ssthresh;     // 윈도우를 절반으로 줄임 (Reset to half)
        retransmit_lost_packet(); // 즉시 재전송
        // Congestion Avoidance 단계로 바로 진입
    }
    else if (event == TIMEOUT) {
        // [严重的 혼잡 - Slow Start로 리셋]
        ssthresh = CWND / 2;
        CWND = 1; // 처음부터 다시 시작
    }
}
```

> 📢 **섹션 요약 비유**: TCP 혼잡 제어는 **'사람이 붐비는 시장의 입구'**를 관리하는 것과 같습니다.
> 1. **Slow Start**: 문을 열었을 때 아주 조금씩 사람을 들여보내며, 문제가 없으면 인원을 2배, 4배로 늘려 빠르게 수용력을 테스트합니다.
> 2. **Congestion Avoidance**: 어느 정도 붐비기 시작하면(ssthresh 도달), 사람을 한 명씩 조심스럽게 추가하여 너무 붐비지 않게 합니다.
> 3. **Fast Retransmit/Recovery**: 어떤 사람이 "지나갈 수 없다!"고 외치는 소리(Dup ACK)가 들리면, 입구를 막지 않고 통행 속도를 절반으로 줄여 흐름을 유지합니다.
> 4. **Timeout**: 만약 아무도 움직일 수 없을 정도로 꽉 막히면, 문을 완전히 닫고 다시 조금씩 사람을 들여보내기 시작합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술 비교 분석표: Reno vs. Tahoe vs. CUBIC

| 구분 | TCP Tahoe | TCP Reno | TCP CUBIC (Modern) |
|:---|:---|:---|:---|
| **특징** | 혼잡 제어의 초기 표준 | Fast Recovery 추가로 Reno 현재 사실상 표준 | 리눅스 커널 기본, 고대역폭 지향 |
| **손실 대응** | 타임아웃 또는 3 Dup ACKs 시 **무조건 Slow Start**로 감 (CWND=1) | 3 Dup ACKs 시 **Fast Recovery** 진행 (CWND=half) | 혼잡 윈도우를 3차 함수로 조절하여 대역폭 빠르게 점유 |
| **장점** | 구현이 간단함 | 망이 완전히 막히지 않았다면 속도 회복이 빠름 | Long Fat Network(LFN) 환경에서 효율적 |
| **단점** | 불필요하게 속도를 많이 줄여 Throughput 낮음 | 단일 패킷 유실에 대해 과도하게 반응할 수 있음 | 기존 TCP와의 혼잡 시 공정성 문제 발생 가능 |

### 2. OSI 7 Layer와의 융합 관점

*   **Network Layer (L3)와의 시너지**: TCP의 혼잡 제어는 전송 계층(L4)의 'End-to-End' 제어 방식입니다. 반면, IP 라우터(L3)에서 수행하는 **ECN (Explicit Congestion Notification)**이나 **Active Queue Management (AQM, 예: RED 알고리즘)**와 연동하여, 패킷이 유실되기 전에 미리 혼잡을 알려주는 방향으로 발전하고 있습니다.
*   **OS와의 상관관계**: OS의 Kernel Socket Buffer(`sk_buff`) 크기 설정은 CWND의 상한선을 결정합니다. 아무리 TCP가 혼잡 제어를 잘해도, OS의 소켓 버퍼가 작으면 실제 성능은 나오지 않습니다.

> 📢 **섹션 요약 비유**: 자동차(TCP)의 속도 제어와 도로 신호체계(Router/Network)의 관계와 같습니다. 예전에는 교통체증이 심해져서 차들이 멈춰야만(Router Drop) 그제서야 운전자가 "아 막힌가보다" 하고 속도를 줄였습니다(Reactive). 하지만 최근에는 도로 전광판을 통해 앞이 막힌다는 것을 미리 알려주어(ECN), 차들이 멈추기 전에 속도를 줄이는 **지능형 교통 통제(Proactive)**로 진화하고 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정

**[Scenario 1] 대용량 파일 전송 서버의 튜닝**
*   **상황**: 대역폭이 높지만 지연 시간(RTT)이 긴 해외 망으로 대용량 데이터를 전송해야 함.
*   **문제**: 기본 TCP 설정으로는 Slow Start로 너무 오랜 시간이 걸려 전송 효율이 낮음.
*   **의사결정**:
    1.  `initcwnd` (Initial Congestion Window) 값을 기본값(3~10 MSS)에서 30 MSS 이상으로 튜닝.
    2.  TCP 알고리즘을 기본 Cubic에서 BBR(Bottleneck Bandwidth and Round-trip propagation time)로 변경하여 RTT에 덜 민감하게 처리.

**[Scenario 2] 실시간 스트리밍 서비스의 버벅임 현상**
*   **상황**: 모바일 환경에서 WiFi/LTE가 자주 바뀌며 패킷 손실이 빈번하게 발생.
*   **문제**: 매번 손실 시 CWND가 절반으로 줄어들면서 영상이 버퍼링됨.
*   **의사결정**:
    1.  UDP 기반의