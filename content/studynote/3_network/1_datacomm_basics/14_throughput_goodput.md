+++
title = "NW #14 처리량 (Throughput) 및 굿풋 (Goodput)"
date = "2026-03-14"
[extra]
categories = "studynote-network"
weight = 14
+++

# NW #14 처리량 (Throughput) 및 굿풋 (Goodput)

> **핵심 인사이트**
> 1. **본질**: **대역폭 (Bandwidth)**이 이론적인 상한선이라면, **처리량 (Throughput)**은 물리적/환경적 제약을 반영한 실제 성능이며, **굿풋 (Goodput)**은 오버헤드와 오류를 제외한 최종 사용자 가치 지표이다.
> 2. **가치**: 네트워크 튜닝의 목표는 단순히 처리량을 높이는 것이 아니라, 프로토콜 오버헤드와 패킷 손실을 최소화하여 굿풋(Goodput)을 극대화하는 데 있다.
> 3. **융합**: 전송 계층(TCP/QUIC)의 혼잡 제어(Congestion Control)와 데이터 링크 계층의 MTU 설정, 그리고 애플리케이션 계층의 데이터 압축 기술이 상호작용하여 전체적인 유효 전송량을 결정한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 정의 및 위계
네트워크 성능 논의에서 가장 흔히 혼동되는 개념인 **대역폭**, **처리량**, **굿풋**은 엄격한 위계를 가진다. **대역폭**은 매체가 가진 이론적인 최대 전송 능력이며, **처리량 (Throughput)**은 실제 환경(잡음, 충돌, 프로토콜 제어) 하에서 측정되는 **유효 비트 전송률 (Effective Data Transfer Rate)**이다. 마지막으로 **굿풋 (Goodput)**은 애플리케이션 입장에서 본, 재전송된 패킷과 각종 헤더를 제외한 **순수 애플리케이션 데이터의 전송 속도**를 의미한다.

#### 2. 등장 배경과 필요성
초기 네트워크(10Mbps 시대)에는 회선 속도가 병목이었으나, 100Gbps 이상의 고속 네트워크가 보편화된 현재, 단순 링크 속도보다 **"실제 데이터가 얼마나 빨리 도착하는가"**가 더 중요한 지표가 되었다. 특히 무선 네트워크(WLAN, 5G) 환경에서는 패킷 손실률이 높아 처리량은 높지만 굿풋은 급격히 떨어지는 현상이 발생하므로, 이를 정밀히 분석하고 최적화하는 기술이 필수적이다.

```ascii
[ Network Performance Hierarchy ]
      
 LEVEL 1: [ BANDWIDTH (Potential) ] ................. 10 Gbps (Theoretical Limit)
            |
            |---> (Physical Constraints: Noise, Distance)
            |
 LEVEL 2: [ THROUGHPUT (Actual) ] ................... 8.5 Gbps (Wire bits + Headers + Retx)
            |
            |---> (Protocol Overhead: TCP/IP Header, Ethernet Frame)
            |
 LEVEL 3: [ GOODPUT (Application View) ] ........... 6.2 Gbps (Pure User Data)
```
*(해설: 그림은 대역폭이라는 넓은 그릇 안에, 물리적 한계로 인한 처리량이 있고, 그 안에 프로토콜 비효율을 제거한 굿풋이 존재하는 포함 관계(Inclusion Relationship)를 보여줍니다.)*

📢 **섹션 요약 비유**: 고속도로 도로의 **차선 수(대역폭)**가 아무리 넓어도, 교통 체증과 신호 대기로 인해 실제 주행 가능한 속도가 제한되는 **처리량**과 같으며, 승객(데이터) 입장에서는 차가 달리는 시간보다 목적지에 도착해서 내리는 시간인 **굿풋**이 진짜 체감 속도인 셈입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상관관계 분석

| 구분 | 요소명 | 역할 | 내부 동작 및 주요 파라미터 | 비유 |
|:---:|:---|:---|:---|:---|
| **물리적** | **Bandwidth** | 최대 전송 용량 제공 | 주파수 대역, 변조 방식(QAM), 채널 코딩 | 파이프의 굵기 |
| **링크층** | **MTU (Maximum Transmission Unit)** | 단일 프레임 크기 결정 | 1500 Byte (Ethernet), Fragmentation 여부 결정 | 화물 박스 크기 |
| **네트워크층** | **Packet Loss** | 처리량 감소 요인 | Bit Error Rate (BER), Queue Overflow (Drop Tail) | 도로상의 파손/분실 |
| **전송층** | **TCP Overhead** | 굿풋 저하 요인 | Header Size (20~60 Byte), Acknowledgment (ACK) 오버헤드 | 영업별 서류 작업 시간 |
| **응용층** | **Compression** | 굿풋 증가 기술 | Lempel-Ziv (LZ), Huffman 알고리즘, 압축률 | 짐을 부피 압축 |

#### 2. 굿풋(Goodput) 산출 심화 및 메커니즘
굿풋은 단순히 '속도'가 아니라 '효율'의 척도이다. 이를 수식적으로 정의하면 다음과 같다.

$$ \text{Goodput} = \frac{\text{Application Data Size (bits)}}{\text{Total Transmission Time (s)}} $$

또한, 처리량($T$)과 오버헤드($O$), 재전송률($L$)을 통해 다음과 같이 표현할 수 있다.

$$ \text{Goodput} = T \times (1 - \text{Loss Rate}) \times \frac{\text{MSS}}{\text{MSS} + \text{Header Size}} $$

여기서 핵심은 **MSS (Maximum Segment Size)**와 **Header Size**의 비율이다. 패킷 크기가 작을수록(Chatty Application) Header 비중이 커져 굿풋이 급격히 하락한다.

```ascii
[ Goodput vs Throughput Data Flow ]
       
 Sender Host                                      Receiver Host
   |                                                    ^
   | [Data Payload: 1460 Bytes]                         |
   | [TCP Header: 20 Bytes]                             |
   | [IP Header: 20 Bytes]                              |
   | [Eth Header: 18 Bytes]                             |
   |------------> (Physical Transfer: 1518 Bytes) ----->|
   |                  ^                                 |
   |                  | (Throughput measures this total)|
   |                  |                                 |
   |                  |<-- Application Re-assembles --->|
   
   (Throughput) = 1518 Bytes / Time
   (Goodput)    = 1460 Bytes / Time
```
*(해설: 그림은 하나의 이더넷 프레임이 전송될 때, 처리량은 헤더를 포함한 총 1518바이트를 측정하지만, 굿풋은 사용자가 실제 쓰는 1460바이트(MSS)만을 유효 데이터로 간주함을 시각화했습니다.)*

#### 3. 핵심 알고리즘: TCP Window Size와 처리량의 관계
처리량은 **TCP Sliding Window** 크기와 **RTT (Round Trip Time)**에 의해 결정된다.

$$ \text{Throughput} = \frac{\text{Window Size (bits)}}{\text{RTT (s)}} $$

이는 네트워크 대역폭이 아무리 넓어도, 윈도우 크기가 작거나 RTT가 길면(위성 통신 등) 처리량이 제한됨을 의미한다. 이를 **Bandwidth-Delay Product (BDP)**라고 한다.

📢 **섹션 요약 비유**: 우체부가 편지를 배달할 때, 편지 내용물(굿풋)보다 봉투와 우표비(처리량)가 더 비싸거나 배달 시간이 너무 길다면, 효율이 나쁜 우편 시스템인 것입니다. 이를 해결하기 위해 편지 내용을 최대한 꽉 채워 보내는(MSS 최적화) 것이 관건입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 처리량(Throughput) vs 굿풋(Goodput) 심층 비교

| 비교 기준 | 처리량 (Throughput) | 굿풋 (Goodput) |
|:---|:---|:---|
| **측정 레벨** | Transport / Network Layer (L3/L4) | Application Layer (L7) |
| **측정 대상** | Frame / Segment 단위의 전체 비트 수 | 순수 Application Payload (Bytes) |
| **주요 영향 요인** | 대역폭, 신호 대 잡음비(SNR), 채널 품질 | 패킷 재전송(Retx), 프로토콜 오버헤드, 압축 |
| **성능 저하 시나리오** | 물리적 거리, 전자기 간섭 | 암호화 오버헤드(TLS), 작은 패킷 잦은 전송 |
| **관리자 관점** | "회선이 터지나?" (Link Health) | "서비스가 빠른가?" (User XP) |

#### 2. 과목 융합 분석 (OS & 컴퓨터 구조)
네트워크의 굿풋은 **OS (Operating System)**의 **스케줄링**과 **컴퓨터 구조**의 **메모리 대역폭**과 직결된다.
- **수신 과부하 (Receive Overhead)**: CPU가 인터럽트 방식으로 패킷을 하나씩 처리하면 컨텍스트 스위칭(Context Switching) 비용이 발생하여 굿풋이 떨어진다.
- **Zero-Copy 기법**: 커널 공간과 유저 공간 간의 데이터 복사를 제거(DMA 활용)하여 CPU 부하를 줄이면, 네트워크 처리량은 그대로면서 CPU가 처리 가능한 굿풋이 증가한다.
- **Pacing (Rate Control)**: 송신 버퍼가 순간적으로 터져 나가면 네트워크 스위치 큐에서 패킷 손실이 발생한다. 리눅스 **FQ (Fair Queueing)** 스케줄러와 같은 Pacing 기법을 사용하면 트래픽을 균등하게 분배하여 전체적인 굿풋을 평탄화(Flattening)할 수 있다.

```ascii
[ System Bottleneck Analysis ]
        
  Network Card (PHY) --(10Gbps)---> [ Switch Queue ]
                                          ^
                                          | (1. Packet Loss if Queue Full)
                                          v
  Kernel (Driver) ----------> [ Ring Buffer ] 
                                        ^
                                        | (2. Copy Overhead)
  Application (User) --------> [ Memory ]
```
*(해설: 그림은 네트워크 카드에서 애플리케이션까지 데이터가 이동하는 경로에서, 처리량 병목은 주로 스위치 큐(1)에서 발생하고, 굿풋 병목은 메모리 복사(2) 과정에서 발생함을 보여줍니다.)*

📢 **섹션 요약 비유**: 택배 회사의 트럭(처리량)이 아무리 빨라도, 물류 센터의 직원(OS/CPU)이 물건을 내리느라 바쁘면 고객에게 배송 완료 알림(굿풋)이 늦어집니다. 즉, 도로 위 속도와 창고의 처리 속도를 통합적으로 최적화해야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 성능 이슈 해결을 위한 의사결정 트리
네트워크 엔지니어는 링크 스피드가 10Gbps임에도 불구하고 파일 전송 속도가 100Mbps에 불과할 경우 다음과 같은 프로세스로 분석해야 한다.

1.  **Step 1 (Physical Check)**: `ifconfig` 또는 `ethtool`을 통해 **CRC Error** 및 **Collision** 비율 확인. 물리적 문제라면 케이블 교체.
2.  **Step 2 (Throughput Check)**: `iperf` 툴로 테스트. 대역폭의 90% 이상 나온다면 링크는 정상.
3.  **Step 3 (Goodput Check)**: 애플리케이션 전송 속도가 느리다면 **MTU 문제** or **TCP Window Size** 문제일 확률 90%. (특히 WAN 환경)
4.  **Step 4 (Optimization)**:
    -   **LAN 환경**: **Jumbo Frame (MTU 9000)** 활성화하여 프레임 당 페이로드 비율 증가.
    -   **WAN 환경**: **TCP Window Scaling** 옵션 활성화하여 BDP(Bandwidth-Delay Product) 대응.

#### 2. 도입 체크리스트
- [ ] **L2 계층**: **MTU (Maximum Transmission Unit)** 불일치(Mismatch)로 인한 단편화(Fragmentation)가 없는가?
- [ ] **L4 계층**: 혼잡 제어 알고리즘이 **BBR** 또는 **Cubic**으로 최적화되어 있는가?
- [ ] **OS 커널**: **TCP Buffer**(`net.ipv4.tcp_rmem/wmem`)가 대기 시간에 비해 너무 작게 설정되어 있지 않은가?

#### 3. 안티패턴 (Anti-Pattern)
- **TCP Small Queues**: 웹 서버가 매우 작은 크기의 패킷(수십 바이트)을 수천 개씩 전송할 경우, 헤더 비중이 50%를 넘어 대역폭의 절반이 낭비된다. **HTTP/2** 또는 **HTTP/3 (QUIC)**의 **Frame Multiplexing**을 통해 하나의 패킷에 여러 메시지를 담아야 한다.

```ascii
[ Optimization Effect Comparison ]
       
   (BEFORE) Little Packet Storm
   | [Data][Head] | [Data][Head] | [Data][Head] | ... -> High Overhead, Low Goodput
   ^
   | Latency Spike
   
   (AFTER) Aggregation (TCP Segmentation Offloading / HTTP/2)
   | [Big Data Chunk][Head] ---------------> Low Overhead, High Goodput
   |
   | Bulk Transfer
```
*(해설: 그림은 조각난 패킷을 난발하던 기존 방식과, 이를 하나로 묶어서 전송(Bulking)함으로써 헤더 오버헤드를 획기적으로 줄이는 최적화 과정을 비교했습니다.)*

📢 **섹션 요약 비유**: 관공서 민원실에 직원이 한 명일 때, 서류를 한 장씩 떼어내어 내는 것(작은 패킷)보다, 업무를 묶어서 한 번에 처리하는 것(데이터 묶음)이 업무 효율(굿풋)이 훨씬 높습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적 기대효과
처리량 및 굿풋 최적화 기술 적용 시 다음과 같은 성능 향상을 기대할 수 있다.

| 기술 적용 분야 | 대상 지표 | 기대 효과