+++
title = "435-439. TCP 혼잡 제어 모델의 진화 (Tahoe, Reno, Cubic, BBR)"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 435
+++

# 435-439. TCP 혼잡 제어 모델의 진화 (Tahoe, Reno, Cubic, BBR)

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 혼잡 제어(Congestion Control)는 네트워크의 처리 용량을 초과하는 트래픽을 조절하여 '혼잡 붕괴(Collapse)'를 방지하는 TCP (Transmission Control Protocol)의 핵심 메커니즘입니다.
> 2. **가치**: 패킷 손실(Loss) 기반의 보수적인 모델에서 지연 시간(RTT)과 대역폭(Bandwidth)을 실시간 측정하는 모델로 진화하며, 고속 네트워크(LFN, Long Fat Network)와 불안정한 무선망에서의 처리량(Throughput)을 획기적으로 개선했습니다.
> 3. **융합**: 네트워크 계층(OSI Layer 3)의 폐기(Drop) 정책(ECN 등)와 연동되며, 컴퓨터 구조(CPU 스케줄링)의 큐잉 이론을 응용하여 대기열 지연(Queueing Delay)을 최소화하는 방향으로 발전하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
TCP 혼잡 제어는 데이터 전송자(Sender)가 네트워크 내의 트래픽 부하를 예측할 수 없다는 전제 하에, 수신자의 수용 능력(Receive Window)뿐만 아니라 **네트워크의 병목 구간(Bottleneck) 처리 능력**을 초과하지 않도록 전송 속도를 조절하는 자율 제어 시스템입니다. 초기 인터넷은 링크 속도가 낮고 버퍼가 작아 패킷 손실(Loss)이 곧 '심각한 혼잡'을 의미했으나, 광섬유와 무선 기술의 발달로 손실이 반드시 혼잡을 의미하지 않는 환경으로 변화했습니다.

**💡 비유**
수도관에 물을 채우는 것과 같습니다. 너무 세게 물을 쏟아부으면(전송 속도 과다) 약한 배관(네트워크 링크)이 터지거나 물이 넘쳐흐릅니다(패킷 손실). 혼잡 제어는 수도꼭지를 수시로 조절하여 배관이 터지지 않는 선에서 최대한 물을 빨리 채우는 기술입니다.

**등장 배경 및 진화**
1.  **기존 한계 (Early Days)**: 1980년대 TCP Tahoe는 패킷 손실을 네트워크 붕괴의 신호로 간주하여 전송률을 급격히 떨어뜨렸습니다. 이는 낮은 대역폭에서는 안정적이었으나, 대역폭이 넓어지며 자원을 낭비하는 심각한 병목을 초래했습니다.
2.  **혁신적 패러다임 (Shift)**: 패킷 손실을 '죄악'으로 보는 시각에서 **'자원 경쟁의 결과'**로 해석하는 관점으로 변화했습니다. TCP Reno와 NewReno는 손실 발생 시 너무 가혹한 페널티를 완화(Fast Recovery)했고, Cubic은 수학적 함수를 도입해 고속 네트워크에서의 회복 속도를 극대화했습니다.
3.  **현재의 비즈니스 요구 (Modern Needs)**: 구글의 BBR은 패킷 손실과 무관하게 **RTT (Round Trip Time)**와 **BtlBw (Bottleneck Bandwidth)**를 측정하여 물리적 한계까지 끝까지 밀어붙이는 전략을 취함으로써, 지연 시간이 중요한 실시간 서비스(HTTP/2, gRPC, 스트리밍)의 품질을 보장합니다.

> **📢 섹션 요약 비유**: 고속도로(네트워크)에 차량(패킷)이 몰리기 시작할 때, 초반의 교통정책은 사고가 나면 도로 전체를 폐쇄하는(Tahoe) 방식이었으나, 점차 사고 구간만 통제하고 차선을 유지(Reno/Cubic)하다가, 이제는 인공위원으로 도로 용량을 실시간 감지하여 사고가 나기 직전의 최적 유량을 유지하는(BBR) 스마트 교통 시스템으로 진화했습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

혼잡 제어의 핵심은 **송신 측 혼잡 윈도우(CWND, Congestion Window)** 크기를 동적으로 제어하는 알고리즘입니다.

#### 1. 주요 구성 요소 비교

| 구성 요소 | 역할 및 내부 동작 | 관련 프로토콜/알고리즘 | 비유 |
|:---|:---|:---|:---|
| **ssthresh** (Slow Start Threshold) | 혼잡 윈도우가 지나치게 커지는 것을 방지하는 임계값. Slow Start에서 Congestion Avoidance로 전환하는 기준점. | Tahoe, Reno, Cubic | 레이서가 급가속을 멈추고 안정 속도로 진입하는 지점 |
| **AIMD** (Additive Increase / Multiplicative Decrease) | 윈도우를 더하며 증가시키다가(선형), 혼잡이 감지되면 곱하기로 감소시키는(지수) 전략. 네트워크 안정성을 보장하는 기본 원칙. | Reno, NewReno | 빙판길에서 미끄러지면 속도를 확 줄이고, 다시 천천히 가속하는 운전법 |
| **Fast Recovery** (빠른 회복) | 3중 중복 승인(3 Dup ACK)을 받으면 Slow Start로 가지 않고, ssthresh를 줄이고 선형적으로 증가 구간으로 바로 복귀하여 대역폭 낭비를 막음. | Reno, NewReno | 타이어가 펑크 나지 않았다면 차를 세우지 않고 타이어만 갈아끼우고 주행 계속 |
| **MinRTT** (Minimum RTT) | 일정 주기(예: 10초) 동안 측정한 RTT 중 최소값. 이를 통해 경로상의 고정 지연(Propagation Delay)을 추정. | BBR | 길이가 아무리 막혀도 "이 도로 통과하는 데 최소한 이 시간은 걸린다"는 물리적 한계치 |
| **Delivery Rate** | ACK 패킷의 도착 속도를 통해 실제 전송된 데이터 양을 측정. BBR에서 BtlBw를 추정하는 근거. | BBR | 출구 컨베이어 벨트에서 나가는 물건 개수를 세서 처리 능력을 계산 |

#### 2. 혼잡 제어 상태 전이 다이어그램 (State Machine)

TCP의 혼잡 제어는 크게 느린 시작(Slow Start), 혼잡 회피(Congestion Avoidance), 빠른 재전송(Fast Retransmit), 빠른 회복(Fast Recovery)의 상태를 순환합니다.

```ascii
                       [TCP Congestion Control State Machine]

      ┌─────────────────────┐
      │   (1) SLOW START     │
      │   cwnd = 1 (Init)    │
      │   Exponential Growth│ <--- (Packet Loss / Timeout)
      └─────────┬───────────┘      (To 1 MSS aggressively)
                │ cwnd >= ssthresh
                │ OR 3 Dup ACKs
                ▼
      ┌─────────────────────┐
      │ (2) CONGESTION AVOID │
      │   AIMD (Linear +1)   │
      │   Steady Growth      │
      └─────────┬───────────┘
                │ Packet Loss Detected
                ▼
      ┌─────────────────────┐       (Modern TCP Only)
      │  (3) FAST RECOVERY   │◄──────────────────────┐
      │   cwnd = ssthresh/2 │   (Retransmit Lost)   │
      │   "Inflated" cwnd    │                        │
      └─────────┬───────────┘                        │
                │ (Recv New ACK) / (Timeout)        │
                ▼                                    │
      ┌─────────────────────┐                        │
      │   Back to (1) or (2) │────────────────────────┘
      │   (Depend on Alg)    │
      └─────────────────────┘
```
*(해설: Tahoe는 Fast Recovery가 없어 Loss 발생 시 바로 Slow Start(1)로 이동하여 속도가 급감하지만, Reno 이후는 Fast Recovery(3) 상태를 거쳐 Congestion Avoidance(2)로 복귀하여 링크 효율을 유지합니다.)*

#### 3. 심층 동작 원리 및 수식

**① TCP Reno (AIMD 기반)**
Reno는 패킷 손실을 혼잡의 징후로 간주합니다. 윈도우 증가는 RTT마다 1 MSS (Maximum Segment Size)씩 증가(Additive)하다가, 3 Dup ACK 발생 시 반으로 줄입니다(Multiplicative).

*   **회복 시간 계산**: W 크기의 윈도우가 손실 후 다시 W로 복귀하려면 약 $O(W^2)$의 시간(Round Trips)이 필요합니다. 10 Gbps 네트워크에서 W는 매우 커지므로 손실 후 복구에 시간이 오래 걸립니다.

**② TCP Cubic (함수 기반)**
Cubic은 리눅스 커널 2.6.19 이상의 표준입니다. 시간 $t$에 대한 3차 함수를 사용하여 네트워크가 비어있을 때 빠르게 대역폭을 점유합니다.

*   **핵심 수식**: $W_{cubic}(t) = C \cdot (t - K)^3 + W_{max}$
    *   $C$: 스케일링 팩터 (상수)
    *   $W_{max}$: 직전 혼잡 발생 시의 윈도우 크기
    *   $K$: 마지막 손실 이후 윈도우가 $W_{max}$로 돌아오기까지 걸리는 시간
*   **동작**: 손실 후 윈도우를 급격히 줄였다가, 3차 곡선을 그리며 다시 $W_{max}$까지 빠르게(Concave up) 올린 후, 완만하게(Convex) 증가하여 안정화됩니다.

**③ TCP BBR (Model-based)**
BBR은 손실(Loss)과 무관하게 **전송 모델(Model)**을 기반으로 작동합니다.

*   **BtlBw (Bottleneck Bandwidth)**: 최근 10회 전송 패킷 중 **최대 전송률(Max Delivery Rate)**를 추정합니다.
*   **RTProp (Round Trip Propagation)**: 최소 RTT를 측정하여 물리적 전파 지연을 파악합니다.
*   **전송량 공식**: $Pacing\_Rate = BtlBw \cdot \min(1, \frac{RTProp}{RTT_{current}})$
*   **동작 사이클**: 1. Startup (파이프라인 채움) → 2. Drain (큐 비움) → 3. BW-Probing (대역폭 탐색) → 4. Cruising (RTProp 유지)
    *   BBR은 RTT가 급격히 늘어나는(Bufferbloat 발생) 것을 감지하면 미리 전송량을 줄여 큐(Queue)가 생기는 것을 원천 차단합니다.

> **📢 섹션 요약 비유**: Reno는 '한 걸음 물러서고 두 걸음 나아가는' 반복적인 방식으로 안정성을 추구하고, Cubic은 '밀렸을 때는 스포츠카처럼 급가속하고, 앞설 때는 크루즈 컨트롤로' 주행하는 방식입니다. 반면 BBR은 '내비게이션(실시간 측정)'을 보고 도로 상황을 알기 때문에, 앞차가 브레이크를 밟기 전에 미리 발을 떼어 연비(지연 시간)를 최적화하는 자율주행 차량입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. Loss-based vs. Delay-based 기술 비교 분석

| 비교 항목 | Loss-based (Tahoe, Reno, Cubic) | Delay-based (BBR, Vegas) |
|:---|:---|:---|
| **혼잡 판단 근거** | **Packet Drop** (ACK Timeout or 3 Dup ACK). 손실이 곧 혼잡이라는 가정. | **RTT Increase** (Queueing Delay). 패킷이 큐에 쌓여 지연이 발생하면 혼잡이라 판단. |
| **대역폭 활용 전략** | 큐(Buffer)가 가득 찰 때까지(전송 속도가 0이 될 때까지) 밀어붙인 후 땀(Fallback). | 큐에 패킷이 쌓이기 시작하면(지연 발생) 미리 조절하여 큐를 비워둠. |
| **버퍼 관리** | "Bufferbloat" 유발. 네트워크 큐를 꽉 채우는 전략을 사용하므로 지연이 심해짐. | "Keep Pipe Full but Queue Empty". 전송은 유지하되 대기열은 비워 지연을 최소화. |
| **주요 적용 분야** | 일반적인 대부분의 유선 네트워크. | 와이파이, 위성 통신, 5G 등 손실은 잦지만 지연에 민감한 실시간 서비스. |

#### 2. OSI 계층 및 시스템 융합 분석

**① 계층 간 상호작용 (Layer 3 & 4)**
- TCP의 혼잡 제어(Layer 4)는 라우터의 **Active Queue Management (AQM, Layer 3)** 정책과 밀접하게 연결됩니다. 전통적인 Loss-based TCP는 큐가 다 차서 패킷이 폐기(Drop Tail)될 때만 반응하여 'Global Synchronization' 현상(모든 TCP가 동시에 줄어듦)을 유발했습니다.
- 이를 해결하기 위해 네트워크 장비는 **ECN (Explicit Congestion Notification)**을 사용하여, 큐가 차기 전에 미리 TCP에 "혼잡임(CE Codepoint)"을 표시합니다. BBR과 같은 알고리즘은 ECN과 결합할 때 패킷 손실 없이도 대역폭을 공유하는 효율이 극대화됩니다.

**② 운영체제 커널 및 하드웨어 (OS & HW)**
- 혼잡 제어는 CPU의 스케줄링(Completely Fair Scheduler, CFS)과