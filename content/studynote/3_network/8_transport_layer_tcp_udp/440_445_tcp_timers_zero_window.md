+++
title = "440-445. TCP 타이머와 영 윈도우 탐색"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 440
+++

# 440-445. TCP 타이머와 영 윈도우 탐색

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: TCP (Transmission Control Protocol)의 신뢰성과 흐름 제어는 시간 기반의 정교한 타이머 메커니즘에 의존하며, 이는 동적 네트워크 환경에 적응하기 위해 지속적으로 값을 업데이트한다.
> 2. **가치**: RTO (Retransmission Timeout)의 동적 계산은 불필요한 재전송을 줄여 대역폭 효율을 높이고, Keep-Alive 및 Persist 타이머는僵局(Deadlock) 상태를 해제하여 시스템 안정성을 보장한다.
> 3. **융합**: 네트워크 혼잡 제어(ConGestion Control)와 운영체제의 커널 자원 관리가 결합된 기술로, 클라우드 환경에서의 L4 로드 밸런서 설정 및 방화벽 세션 관리의 핵심이다.

---

## Ⅰ. 개요 (Context & Background)

TCP는 신뢰성을 보장하기 위해 '타이머'라는 시간적 개념을 도입하여 패킷 손실 및 상태 불확실성을 관리합니다. 단순히 데이터를 보내는 것을 넘어, "언제까지 응답을 기다릴 것인가(RTO)", "상대방이 살아있는가(Keep-Alive)", "보낼 수 있는 상태인가(Persist)"를 지속적으로 감시해야 합니다.

**💡 비유**
TCP 타이머는 **'택배 배송 시스템의 관제 센터'**와 같습니다. 고객(송신자)은 물건이 도착했는지 확인하기 위해 운송장(ACK)을 확인하고, 운송장이 조회되지 않으면 언제 클레임을 낼지(RTO) 결정해야 합니다. 또한, 고객이 잠시 자리를 비웠는지 확인하고(Keep-Alive), 수령 거부(Window 0) 상태라면 언제 수령 가능한지 계속 문의해야(Persist) 합니다.

**등장 배경**
1.  **기존 한계**: 초기 네트워크는 고정된 타임아웃 값을 사용하여, 네트워크 혼잡 시 불필요한 재전송 폭주로 인한 혼잡 붕괴(Collapse)가 발생했습니다.
2.  **혁신적 패러다임**: 1988년 Van Jacobson이 제안한 동적 타이머 알고리즘은 RTT(왕복 시간)를 실시간으로 측정하여 타임아웃 값을 적응적으로 조정하는 방식으로 패러다임을 전환했습니다.
3.  **현재의 비즈니스 요구**: 초저지연(Low Latency) 요구 및 방화벽/로드 밸런서의 세션 유지 비용 최적화를 위해, 불필요한 패킷을 최소화하면서도 연결 상태를 정확히 파악할 수 있는 정교한 타이머 전략이 요구됩니다.

**📢 섹션 요약 비유**
TCP 타이머 시스템은 **"복잡한 교통상황에서 내비게이션이 경로를 재계산하고, 교통체계가 고장 나지 않도록 신호등을 조정하는 교통 통제센터"**와 같습니다. 상황에 따라 기다림의 시간을 늘렸다 줄였다 하며 원활한 흐름을 유지합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

TCP의 타이머 시스템은 크게 데이터 전송의 신뢰성을 담당하는 '재전송 타이머'와 연결 상태 및 흐름 제어를 담당하는 '보조 타이머'로 구분됩니다. 이 섹션에서는 재전송 시점을 결정하는 RTO 측정 알고리즘과 영 윈도우(Zero Window) 상태 해결 메커니즘을 심층 분석합니다.

### 1. RTO (Retransmission Timeout) 측정 및 Karn's Algorithm

RTO를 결정하기 위해 TCP는 RTT(Round Trip Time)를 측정하지만, 네트워크 상황은 매번 다릅니다. 따라서 과거의 RTT 데이터를 바탕으로 **SRTT (Smoothed RTT)**와 **RTTVAR (RTT Variation)**를 계산하여 예측 오차를 최소화합니다.

**구성 요소 및 역할**
| 요소명 | 역할 | 내부 동작 | 프로토콜/수식 | 비유 |
|:---|:---|:---|:---|:---|
| **RTT** | 실제 왕복 시간 측정 | 데이터 전송(Timestamp) 후 ACK 수신까지의 시간 차이 계산 | $T_{current} - T_{send}$ | 주행 시간 |
| **SRTT** | 평활화된 RTT 유지 | 최신 RTT와 이전 SRTT를 가중 평균(Alpha=0.125) | $SRTT_{new} = (0.875 \times SRTT_{old}) + (0.125 \times RTT_{sample})$ | 평균 속도 |
| **RTTVAR** | RTT의 편차(Jitter) 측정 | 예측 불가능한 네트워크 지터 반영 | $VAR_{new} = (0.75 \times VAR_{old}) + (0.25 \times \lvert SRTT - RTT_{sample} \rvert)$ | 속도 편차 |
| **RTO** | 재전송 판단 기준 시간 | SRTT + 안전 마진(4x Variation)으로 설정 | $RTO = SRTT + (4 \times RTTVAR)$ | 타임아웃 설정 |

**ASCII 구조 다이어그램: RTO 계산 흐름**
```ascii
           [Sender]                                     [Receiver]
              |                                              |
              | --- [SEQ N, Timestamp Tx] ------------------> |
              |            (Data Transmission)               |
              |                                              |
              |                                              |
              | <---------------- [ACK N] ------------------- |
              |            (ACK Received)                    |
              |           (Timestamp Rx Echoed)               |
              |                                              |
(Internal Calculation at Sender)
RTT_Sample = Now - Timestamp_Tx
            |
            v
+-----------------------+
|  Update SRTT & RTTVAR |  <-- Weighted Moving Average
|  SRTT = 0.875*S + ... |
|  RTO = SRTT + 4*Var   |  <-- Conservative Timeout
+-----------------------+
            |
            v
      (Set RTO Timer)
```
*(해설: 송신자는 데이터를 보낼 때 타임스탬프를 기록하고, ACK를 받으면 그 차이를 RTT 샘플로 사용합니다. 이 샘플을 이동 평균(Exponential Moving Average)하여 SRTT를 갱신하고, 여기에 변동성(4*Var)을 더해 보수적인 RTO를 설정합니다.)*

**Karn's Algorithm (칸 알고리즘)**
재전송이 발생한 경우, ACK가 돌아왔을 때 이것이 '최초 전송'에 대한 응답인지 '재전송'에 대한 응답인지 모호합니다(Ambiguity Problem). 만약 재전송된 패킷의 RTT를 측정하면, 실제보다 짧게 측정되어 RTO가 비정상적으로 작아지는 현상이 발생합니다.
*   **해결책**: 재전송이 발생한 세그먼트에 대해서는 **RTT 샘플을 측정하지 않고 SRTT 계산에서 배제**합니다. 대신, 재전송이 발생할 때마다 RTO 값을 지수적으로 증가시켜(Exponential Backoff) 네트워크 부하를 줍입니다.

### 2. 영 윈도우 탐색 (Persist Timer)

수신 측의 버퍼(RBuffer)가 가득 차면 TCP 헤더의 `Window Size`를 0으로 설정하여 송신 측에 전송 중지를 요청합니다. 이후 수신 측이 버퍼를 비우고 `Window Update`를 보내지만, 이 패킷이 유실되면 **Deadlock** 상태에 빠지게 됩니다.
*   송신자: "보내지 말라 했으니 기다린다."
*   수신자: "보내라 했는데(Update 유실) 왜 안 보내?"

이를 해결하기 위해 송신자는 영 윈도우 상태가 지속되면, 윈도우가 0이 아닌지 확인하기 위해 주기적으로 1바이트 프로브(Probe)를 전송합니다.

**ASCII 구조 다이어그램: 영 윈도우 및 Persist 타이머**
```ascii
   Sender                                               Receiver
     |                                                      |
     | --- [Data] ---> (WIN=0通告) <--- [Window Update(WIN=0)]
     | (Stop Sending)                                      |
     |                                                      | (Buffer Full)
     |                                                      |
     | <=== [Persist Timer Starts] ====>                    |
     |                                                      |
     | --- [Probe Segment (1Byte)] -----------------------> | (Buffer Free?)
     |      "Is Window Open?"                               |
     |                                                      |
     | (If Buffer Still Full)                               |
     | <-------------------------------- [ACK (WIN=0)] ----- |
     | (Reset Persist Timer)                                |
     |                                                      |
     | (If Buffer Available)                                |
     | <-------------------------------- [ACK (WIN=1024)] --- |
     | (Resume Transmission)                                |
```
*(해설: Persist 타이머는 송신자가 일방적으로 대기만 하지 않도록 강제로 '찌르는(Poke)' 역할을 합니다. 이 프로브는 수신자로부터 현재 윈도우 상태를 응답받을 때까지 주기적으로 반복되어 교착 상태를 예방합니다.)*

**📢 섹션 요약 비유**
RTO 계산은 **"내비게이션이 교통 정체 상황을 학습하여 목적지 도착 시간을 예측하고 업데이트하는 것"**과 같습니다. 과거 데이터를 바탕으로 평균(SRTT)을 내되, 예측이 틀릴 것을 대비해 넉넉하게(Variance) 잡습니다. **Persist Timer**는 **"계산기 앞에서 매장 직원에게 '계산해줄 준비 됐니?'라고 1분마다 물어보는 것"**과 같아서, 직원의 "됐다"는 신호를 놓쳐도 영업이 중단되지 않게 합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

TCP 타이머는 전송 계층의 독립적인 문제가 아니라, 운영체제의 커널 자원 관리 및 네트워크 하드웨어의 성능과 직결됩니다.

### 1. Keep-Alive vs Persist vs Time-Wait 비교

| 구분 | Keep-Alive Timer | Persist Timer | Time-Wait State |
|:---|:---|:---|:---|
| **목적** | **연결 생존 확인** (Idle 상태 모니터링) | **흐름 제어 복구** (Zero Window 해제) | **지연 패킷 처리** (연결 종료 안전장치) |
| **작동 시점** | 데이터 교환 없이 일정 시간 경과 시 | 수신 윈도우가 0일 때 | Active Close 후 FIN ACK 수신 후 |
| **주체** | 애플리케이션/OS 설정 | TCP 스택(커널) 강제 | TCP 스택 자동 |
| **주요 파라미터** | idle_time (보통 2시간) | Retransmission interval (RTO 기반) | 2MSL (Max Segment Lifetime, 약 60~240초) |
| **과부하 위험** | 서버 자원(Sessions) 낭비 | 프로브 패킷 오버헤드 | 포트 고갈(Port Exhaustion) |

### 2. 타 영역과의 융합 (OS & Hardware)

*   **OS (운영체제) 커널 최적화**: 리눅스 커널에서 `tcp_retries2` 등의 파라미터는 RTO 폭주를 제어합니다. 또한, Keep-Alive를 너무 짧게 설정하면(예: 10초) 서버의 불필요한 CPU/메모리 사용량이 급증하는 **Thundering Herd** 문제가 발생할 수 있습니다.
*   **네트워크 보안 (Firewall)**: 방화벽은 연결 상태(Connection Tracking)를 유지하는데, **Time-Wait** 상태가 길어지면 방화벽 테이블이 가득 차 새로운 연결이 거부될 수 있습니다. 이를 위해 `tcp_tw_reuse` 옵션 등을 활용하여 자원을 재사용하는 전략이 필요합니다.

**ASCII 비교 분석: 타이머 별 네트워크 트래픽 패턴**
```ascii
   [Keep-Alive] (Long Interval)          [Persist] (Adaptive Interval)          [Time-Wait] (Fixed)
        |                                      |                                       |
   (Idle Traffic)                          (Data Stuck)                          (Closing Phase)
        |                                      |                                       |
........|..............                    ======|=====>                            ----->| (FIN)
        |  KA                                 | Probe                                    ^ |
        |  KA                                 | Probe                                    | | (Wait 2MSL)
        |  KA                                 | Update (Open)                            | v
........|..............                          v                                       |
(연결 유지, 트래픽 거의 없음)            (전송 재개)                            (포트 점유 중 해제)
```

**📢 섹션 요약 비유**
Keep-Alive는 **"오랫동안 만나지 않은 친구에게 가끔 안부 문자를 보내 연결을 유지하는 것"**이고, Persist는 **"막힌 파이프를 뚫어주기 위해 주기적으로 펌프를 작동하는 것"**입니다. 이 과정에서 OS는 이 모든 일정을 관리하는 비서이며, 방화벽은 출입 명부를 관리하는 경비원으로서 너무 많은 방문자(Time-Wait)가 있을 경우 입구를 막지 않도록 조율해야 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 서비스 운영 시 타이머 설정 오류는 서비스 장애나 성능 저하의 직접적인 원인이 됩니다. 특히 방화벽, 로드 밸런서(L4 Switch), WAS(Web Application Server) 간의 타이머 설정 불일치는 '고질적인 연결 끊김' 현상을 유발합니다.

### 1. 실무 시나리오 및 의사결정

**시나리오 A: DB Connection Pool에서 갑작스러운 'Connection Reset' 발생**
*   **상황**: WAS와 DB 사이에 방화벽이 존재. DB에서 8시간 동안 쿼리가 없으면 방화벽이 연결을 끊음(Unidle Timeout). WAS의 Keep-Alive는 2시간 설정.
*   **문제**: 방화벽보다 WAS의 유휴 시간이 길어, 방화벽이 먼저 연결을 끊으면 WAS는 여전히 연결이 살어있다고 착각함.
*   **해결**: WAS의 `keepalive` 설정을 방화벽 `timeout`보다 짧게 설