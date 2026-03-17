+++
title = "116-118. 동적/정적 다중 접속 방식 (PRMA, DAMA, PAMA)"
date = "2026-03-14"
[extra]
category = "Physical & MAC Layer"
id = 116
+++

# 116-118. 동적/정적 다중 접속 방식 (PRMA, DAMA, PAMA)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 통신 시스템의 핵심 자원인 주파수와 시간 슬롯을 효율적으로 분배하기 위해 고정된 맥락(Fixed Context)과 유연한 맥락(Flexible Context)을 결정하는 MAC (Medium Access Control) 계층의 할당 정책이다.
> 2. **가치**: 트래픽 패턴에 따라 대역폭 효율성(Spectral Efficiency)을 극대화하거나, 지연 시간(Latency)을 최소화하여 QoS (Quality of Service)를 보장하며, 채널 용량 대비 사용자 수를 최적화한다.
> 3. **융합**: 위성 통신(DAMA), 이동통신(PRMA), 전용망(PAMA) 등 망의 특성에 따라 선택되며, 5G 네트워크의 Dynamic Spectrum Sharing 기술과 OFDMA (Orthogonal Frequency Division Multiple Access) scheduling의 시초가 되는 이론적 기반이다.

---

### Ⅰ. 개요 (Context & Background)

**다중 접속(Multiple Access)** 기술은 제한된 무선 주파수 자원을 다수의 사용자가 공유하여 사용하기 위한 통신망의 근간입니다. 자원 할당의 철학에 따라 크게 **PAMA (Pre-Assigned Multiple Access)**와 **DAMA (Demand Assignment Multiple Access)**, 그리고 패킷 기반의 **PRMA (Packet Reservation Multiple Access)**로 나뉩니다.

과거의 음성 중심 통신은 회선 교환(Circuit Switched) 방식처럼 고정된 자원을 할당하는 PAMA가 주류였으나, 데이터 트래픽의 폭발적인 증가와 무선 자원의 희소성(Spectrum Scarcity) 문제가 대두되면서, 트래픽 양에 따라 유동적으로 자원을 배분하는 DAMA와 PRMA가 연구되고 도입되었습니다. 이는 희소성(Spatial/Temporal)을 해결하기 위한 근본적인 접근 방식의 차이입니다.

**💡 비유**
식당 자리(주파수)를 배정하는 것과 같습니다. 특정인을 위해 항상 비워두는 것(PAMA), 손님이 올 때만 안내하는 것(DAMA), 자리를 잡으면 잠시 독점하지만 오래 비우면 반납하는 것(PRMA)으로 나뉩니다.

**등장 배경**
1.  **기존 한계**: FDMA (Frequency Division Multiple Access)나 고정 할당 TDMA (Time Division Multiple Access)는 사용자가 발화하지 않을 때(Silence Period)에도 대역폭을 점유하여 자원이 낭비되었습니다.
2.  **혁신적 패러다임**: 제어 채널(Control Channel)을 도입하여 사용자의 요구(Demand)가 있을 때만 트래픽 채널(Traffic Channel)을 할당하는 **온-디맨드(On-demand)** 패러다임이 등장했습니다.
3.  **현재의 비즈니스 요구**: IoT (Internet of Things) 기기의 스파크(Sparse) 트래픽과 스트리밍의 대용량 트래픽이 혼재된 환경에서, 정적/동적 할당을 혼합한 Hybrid Scheduling이 5G 및 6G 표준의 핵심 과제로 자리 잡았습니다.

**📢 섹션 요약 비유**
고속도로 차선을 **전용 차선(버스 전용차럼 PAMA)**으로 만들어두느냐, **일반 차선(DAMA/PRMA)**으로 두어 상황에 따라 유동적으로 운영하느냐의 선택과 같습니다. 전용 차선은 버스가 없어도 비워두어야 하지만, 일반 차선은 정체 구간에서는 효율이 떨어질 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

동적/정적 할당 방식의 기술적 깊이를 이해하기 위해서는 채널 구조, 할당 알고리즘, 그리고 상태 전이(Transition) 메커니즘을 분석해야 합니다.

#### 1. 구성 요소 비교 (Component Comparison)

| 요소 (Component) | PAMA (Pre-Assigned) | DAMA (Demand Assigned) | PRMA (Packet Reservation) |
|:---:|:---|:---|:---|
| **핵심 철학** | 고정된 시간/주파수 자원 영구 부여 | 요청 시 즉시 자원 할당 및 회수 | 패킷 단위 예약 및 슬롯 동적 확보 |
| **제어 기관** | 고정된 스케줄 (Fixed Schedule) | 중앙 제어기 (Hub/Satellite) | 분산 경쟁 (Contend) + 예약 (Reserve) |
| **오버헤드** | 거의 없음 (No Signaling Overhead) | 할당 요청/해제 패킷 필요 | 충돌 해결 및 예약 유지 오버헤드 |
| **대기 시간** | 즉시 (Zero Latency) | Setup Delay 발생 (약 수 ms~수 백 ms) | 초기 경쟁 지연 후 안정적 (Variable) |
| **효율성** | 트래픽이 Full일 때 100% | Burst 트래픽에 최적화 | 음성(Data+Voice) 혼합에 최적화 |

#### 2. 채널 구조 및 데이터 흐름 (Channel Structure & Flow)

PAMA는 단순한 매핑이지만, DAMA와 PRMA는 복잡한 제어 루프를 가집니다. 아래는 DAMA/PRMA 시스템의 일반적인 동작 흐름도입니다.

```ascii
      [ DAMA / PRMA System Operational Flow ]

+----------------+       Request      +------------------+
|  User Terminal | ----------------> | Central Controller|
|    (MS/UE)     | <----------------- |   (Hub / BTS)    |
+----------------+    Assign Slot    +------------------+
       |                                |      |
       |  1. Request (Reservation)      |  2. Find Free Slot
       v                                v      v
+-------------------------------------------------------+
|             Uplink Channel (Time/Frequency)           |
|                                                       |
|  Frame 1: [Ctrl][Data][Data][Idle][Idle][Data][Idle]  |
|  Frame 2: [Ctrl][Data][Data][User A][User A][Idle]... |
|           <--- A에게 예약된 슬롯 할당됨 --->          |
|                                                       |
+-------------------------------------------------------+
```

#### 3. 심층 동작 원리 (Deep Dive Mechanics)

**A. PAMA (FDMA/TDMA 고정 모드)**
가장 기초적인 방식으로, $f(t)$라는 주파수나 $t$ 시간 슬롯을 특정 사용자 $U_i$에게 영구적 사상(Mapping)합니다.
$$ Slot_{i} \mapsto User_{k}, \quad \forall t $$
- **장점**: 충돌(Collision) 가능성이 0이며, 스케줄링 로직이 필요 없어 하드웨어 구현이 단순합니다.
- **단점**: $\sum Traffic_{i} < Bandwidth$인 경우, 남은 자원이 Idle 상태로 방치되어 **Channel Utilization**이 급격히 떨어집니다.

**B. DAMA (요구 할당)**
위성 통신(VSAT 등)에서 주로 사용합니다. 별도의 **신호 채널(Signaling Channel)**을 통해 자원을 요청합니다.
1.  **요청 (Request)**: 단말기가 Random Access(예: ALOHA) 방식으로 제어기에게 "Capacity Needed" 메시지 전송.
2.  **스케줄링 (Scheduling)**: 제어기는 전체 자원 풀(Pool)을 확인하고, 가용한 슬롯을 찾아 **Assignment Map**을 브로드캐스팅.
3.  **할당 및 해제**: 통신 종료 시 "Release" 신호를 보내면 자원이 풀(Pool)로 복귀됩니다.

**C. PRMA (패킷 예약)**
무선 구간에서 음성(Voice)의 간헐성(Silence)을 이용하여 효율을 높이는 방식입니다.
- **동작 원리**: 
  - 초기 패킷은 Slotted ALOHA 방식으로 경쟁(Contend)하여 빈 슬롯을 잡습니다.
  - 슬롯 확약에 성공하면, 다음 프레임부터는 경쟁 없이 해당 슬롯을 독점(Reserved)합니다.
  - 음성의 침묵 구간(Silence Gap)이 감지되면 슬롯을 해제하여 다른 사용자가 경쟁할 수 있게 합니다.
- **핵심 코드 로직 (Pseudo-code)**:
```python
def PRMA_Terminal(voice_packet):
    if has_reservation:
        transmit_in_reserved_slot(voice_packet)
    else:
        if min_free_slot_available(): 
            result = attempt_transmission(voice_packet) # ALOHA Contention
            if result == SUCCESS:
                set_reservation_status(True) # 확약 성공
        else:
            buffer_packet(voice_packet) # 대기
```

**📢 섹션 요약 비유**
마치 **복잡한 고속도로 톨게이트**와 같습니다. PAMA는 모든 차량이 전용 차로를 가지며(Dedicated Lane), DAMA는 교통 상황 센터가 실시간으로 차선을 늘려주는 방식(Smart Lane)입니다. PRMA는 하이패스 차로에서 통행권을 따낸 뒤, 계속 통과하다가 멈추면 통행권을 뺏기는 구조와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 (Quantitative Analysis)

| 지표 (Metrics) | PAMA (Fixed) | DAMA (Dynamic) | PRMA (Packet/Res) |
|:---|:---:|:---:|:---:|
| **채널 효율 (Utilization)** | 낮음 ($\rho \ll 1$일 때) | 높음 ($\rho \to 1$) | 매우 높음 (Voice Activity $<0.4$) |
| **접속 지연 (Access Delay)** | 0 (Deterministic) | Variable (Setup Delay) | Low (After Reservation) |
| **복잡도 (Complexity)** | Low | Medium (Control Overhead) | High (Contention Logic) |
| **트래픽 적합성** | Constant Bit Rate (CBR) | Bursty Traffic | Voice + Data (Integrated) |
| **대표적 적용** | 전용선, 아날로그 TV | 위성 링크, 케이블 모뎀 | GSM, DECT, 초기 무선 데이터 |

#### 2. 과목 융합 관점 (OS/Network Convergence)

-   **[네트워크 & OSI]**: 이 기술들은 OSI 7계층 중 **Data Link Layer (Layer 2)**의 MAC sublayer에서 동작합니다. PAMA는 TDM (Time Division Multiplexing)의 고정 개념과 연결되며, DAMA는 현대 이더넷의 **CSMA/CD**나 무선 LAN의 **CSMA/CA**와 함께 "공유 매체 접근 제어"의 양대 산맥을 이룹니다.
-   **[운영체제 & 스케줄링]**: OS의 프로세스 스케줄링과 완벽히 대응됩니다.
    -   PAMA $\approx$ **GCD (Guaranteed Cycle Exec)**: 항상 자원을 보장받는 Real-time Task.
    -   DAMA $\approx$ **Dynamic Priority/EDF**: 요청이 들어왔을 때 CPU 시간을 할당하는 방식.
-   **[성능 분석]**: DAMA 시스템의 평균 지연 시간은 $M/M/1$ 또는 $M/D/1$ 큐잉 모델로 해석할 수 있으며, PRMA의 성능 분석은 Markov Modulated Poisson Process (MMPP) 모델을 사용하여 음성 패킷의 손실율(Packet Dropping Probability)을 예측합니다.

**📢 섹션 요약 비유**
운영체제가 **CPU 코어**를 프로세스에 배정하는 것과 동일합니다. PAMA는 코어 1개를 아무도 안 써도 특정 프로그램에게만 주는 것이고, DAMA는 프로그램이 "일해!"라고 요청할 때만 OS가 코어를 할당하는 **Time Sharing** 시스템입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 시스템 설계 시 단순히 "최신 기술"인 PRMA를 선택하는 것이 항상 정답은 아닙니다.

#### 1. 실무 시나리오 및 의사결정 (Decision Matrix)

**Case A: 지상파 방송 송신 시스템 (설계 조건: 24시간 100% 트래픽)**
-   **상황**: 데이터 흐름이 끊기지 않고 대역폭을 항상 점유해야 함.
-   **판단**: **PAMA (Fixed TDM)** 선택.
-   **이유**: DAMA/PRMA의 제어 패킷 오버헤드가 낭비이며, Setup Delay는 허용되지 않음. 회선 교환(Circuit) 방식이 최적.

**Case B: 해상 저궤도 위성(LEO) 군단 통신망 (설계 조건: Sparse/Random 트래픽)**
-   **상황**: 수백 대의 단말기가 가끔씩 위치 보고나 메시지를 전송.
-   **판단**: **DAMA** 선택.
-   **이유**: PAMA로 할당하면 자원의 99%가 낭비됨. 요청 시에만 주파수를 할당하여 자원 효율을 극대화해야 함.

**Case C: 이동통신망 음성 서비스 (설계 조건: 음성 품질 보장, 다수 사용자)**
-   **상황**: 사람이 말하는 시간(Speech Activity)은 40% 미만.
-   **판단**: **PRMA** 기반의 TDMA (예: GSM 등 초기 셀룰러).
-   **이유**: 침묵 시간에 슬롯을 회수하여 다른 사용자의 패킷이나 제어 신호를 보냄으로써 시스템 용량을 2배 이상 확보 가능.

#### 2. 도입 체크리스트 (Checklist)

-   **[기술적]** 트래픽 패턴의 **Burstiness (폭발성)**이 얼마인가? (Peak-to-Average Ratio)
-   **[운영적]** 중앙 제어기(Hub)의 **단일 장애점(SPOF)** 문제와 DAMA 제어 채널의 혼잡(Radiation Storm) 대비책이 있는가?
-   **[보안적]** PRMA의 경우, 슬롯을 선점하기 위한 DoS 공격(Denial of Service)에 대한 방어 로직이 존재하는가?

**📢 섹션 요약 비유**
공연장을 예약하는 것과 같습니다. **PAMA**는 연극이 없는 날에도 극장을 통째로 빌려주는 것(비효율). **DAMA**는 "공연할 때만 연락주세요"라고