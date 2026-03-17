+++
title = "111-112. ALOHA와 Slotted ALOHA 프로토콜"
date = "2026-03-14"
[extra]
category = "Physical & MAC Layer"
id = 111
weight = 112
+++

# 111-112. ALOHA와 Slotted ALOHA 프로토콜

## # [ALOHA 프로토콜]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 중앙 제어 없이 다수의 단말이 공유 매체를 통해 데이터를 전송하기 위해 고안된 최초의 **분산형 매체 접근 제어 (MAC, Medium Access Control)** 기술
> 2. **가치**: 복잡한 동기화 과정 없이 구현 가능하나, 순수 알로하는 최대 18.4%의 낮은 채널 효율을 보이며, 슬롯 알로하(Slotted ALOHA)를 통해 이론적 효율을 2배(36.8%)로 향상시킴
> 3. **융합**: 유선 이더넷의 **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)** 및 현대 무선 네트워크의 **RACH (Random Access Channel)** 개념의 시초가 됨

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
ALOHA 프로토콜은 1970년대 하와이 대학교의 노먼 아브라함슨(Norman Abramson) 교수 팀이 개발한 것으로, 지리적으로 분산된 섬 간의 무선 통신을 위해 설계된 최초의 무선 데이터 통신 프로토콜입니다. 이 기술은 '충돌(Collision)'이 발생하면 확률적으로 재전송을 시도하는 **임의 접근 방식 (Random Access Protocol)**의 효시입니다. 당대에는 패킷 교환 기술 자체가 초기 단계였으며, 유선 환경이 아닌 무선(Radio Frequency) 환경에서 여러 노드가 효율적으로 통신할 수 있는 수학적 모델을 제시했다는 점에서 통신사에 지대한 공헌을 했습니다.

**💡 비유**
마치 조용한 회의실에서 누군가 말을 걸고 싶을 때, 상대방이 다 말하고 있는지 확인하지 않고 내 말을 그냥 시작해버리는 것과 같습니다. 만약 운이 좋아 겹치지 않으면 대화가 성립되지만, 누군가 동시에 말을 걸면 둘 다 못 알아듣게 됩니다.

**등장 배경**
① **기존 한계**: 중앙 집중형 컴퓨팅에서 분산 컴퓨팅으로 넘어가는 시기, 고정된 회선 할당 방식은 비효율적이었습니다.
② **혁신적 패러다임**: "단말이 전송 권한을 얻기 위해 기다리기보다, 일단 보내고 문제가 생기면 다시 시도한다"는 ** contention-based (경쟁 기반)** 통신 패러다임을 도입했습니다.
③ **비즈니스 요구**: 하와이 제도와 같이 물리적 케이블铺设가 어려운 지역에서 저비용으로 데이터 네트워크를 구축해야 하는 현실적 요구가 있었습니다.

**📢 섹션 요약 비유**
ALOHA 프로토콜의 등장은 마치 복잡한 신호등 없는 교차로에서, 운전자들이 서로 눈치를 보며 "일단 진행해보고 충돌하면 뒤로 물러나기"를 하는 최초의 자율주행 교통 체계를 도입한 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

ALOHA 시스템의 핵심은 중앙의 스케줄러가 없이 **충돌(Collision)**과 **재전송(Retranmission)**을 통해 자원을 분배한다는 점입니다. 여기서 수학적 모델링의 핵심이 되는 '취약 시간(Vulnerable Time)'과 '시스템 처리율(Throughput)'의 관계를 심도 있게 분석해야 합니다.

#### 1. 구성 요소 및 동작 메커니즘

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/매커니즘 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Sender (송신 노드)** | 데이터 생성 및 전송 | 데이터 프레임 생성 후 즉시(Pure) 또는 슬롯 시작점에 전송 | Random Access | 사람 |
| **Receiver (수신 허브/서버)** | 신호 수집 및 ACK 브로드캐스팅 | 데이터 수신 시 CRC 오류 검사 후 ACK 전송 | ACK/NACK Scheme | 회의록 작성자 |
| **Channel (무선 채널)** | 매체 전달 | 공유 주파수 대역, 충돌 시 신호 왜곡 발생 | Shared Medium | 공기 중 |
| **Timer & Backoff** | 충돌 감지 및 재전송 제어 | ACK 타임아웃 시 `Random Backoff` 알고리즘으로 대기 시간 계산 | Binary Exponential Backoff (유사) | 기다림 타이머 |
| **Slot Generator (Slotted 전용)** | 시간 동기화 | 모든 노드에 동일한 타이밍 클럭을 제공하여 경계를 맞춤 | Synchronized Clock | 시보 소리 |

#### 2. Pure ALOHA의 상세 동작 및 수식

Pure ALOHA의 가장 큰 특징은 **'비동기식 (Asynchronous)'**이라는 점입니다. 노드는 데이터가 준비되는 즉시 전송을 시도합니다. 이때 **취약 시간(Vulnerable Time, $T_v$)**은 프레임 전송 시간($T_{fr}$)의 **2배**가 됩니다. 왜냐하면, 어떤 프레임이 전송되는 동안($T_{fr}$) 뿐만 아니라, 그 프레임이 끝나가는 시점에 새로운 프레임이 시작되더라도 끝부분이 겹치기 때문입니다.

**충돌 확률 도출 (이론적 배경)**
통계학적으로 평균 프레임 도착률을 $\lambda$라 할 때, $t$ 시간 동안 $k$개 프레임이 도착할 확률은 포아송 분포(Poisson Distribution)를 따릅니다. 채널 효율 $S$ (처리율)과 부하 $G$ (제공된 부하, $\lambda \times T_{fr}$)의 관계는 다음과 같습니다.

$$ S = G \times P[\text{No other traffic in vulnerable time}] $$
$$ P[\text{Success}] = e^{-2G} $$
$$ \therefore S = G \times e^{-2G} $$

여기서 $S$를 최대화하기 위해 $G$에 대해 미분($dS/dG = 0$)하면, 최적의 $G = 0.5$일 때 최대 처리율 **$S_{max} \approx 0.184$ (18.4%)**임을 알 수 있습니다.

```ascii
[Pure ALOHA의 충돌 시나리오]

      0                   T                   2T
      |-------------------|-------------------|
      A 시작:             [========= A 전송 ==========]
      B 시작:                  [======== B 전송 ========]
      C 시작:                               [======= C 전송 ======]
                                    ^       ^
                                    |-------|
                                   충돌 구간 (Collision)

* 분석:
1. 노드 A가 T=0에 전송 시작.
2. 노드 B가 T=0.4T에 전송 시작 -> 중간에 겹쳐서 A, B 모두 파괴됨.
3. 노드 C는 A가 끝나갈 때(1.8T) 시작했지만, A의 꼬리와 C의 머리가 겹침.
결과: A의 전송 구간 [0, T] 동안 시작된 B와, A의 전송이 끝나는 T 시점 이전에 시작된 C 모두와 충돌 가능성 존재.
=> 즉, 한 프레임을 보호하기 위해 T의 앞뒤 모두를 비워야 함 (총 2T 동안 다른 전송 불가).
```

#### 3. Slotted ALOHA의 상세 동작 및 개선

Slotted ALOHA는 이 **2T**라는 긴 취약 시간을 **1T**로 줄이기 위해 고안되었습니다. 핵심은 **'동기화 (Synchronization)'**입니다. 전송 시간을 일정한 단위인 **슬롯(Slot)**으로 나누고, 모든 노드는 이 슬롯의 시작 시점에만 전송을 시작할 수 있도록 강제합니다.

이로 인해 충돌은 **'완전한 겹침(Complete Overlap)'**으로만 발생하며, '부분 겹침(Partial Overlap)'은 사라집니다. 취약 시간이 $T$로 줄어들기 때문에 확률식은 다음과 같이 변형됩니다.

$$ S = G \times e^{-G} $$

이 식을 미분하여 최댓값을 구하면 $G=1$일 때 **$S_{max} \approx 0.368$ (36.8%)**로 Pure ALOHA보다 정확히 2배의 효율을 보입니다.

```ascii
[Slotted ALOHA의 시간 축 분할 및 동기화]

      |<--- Slot 1 --->|<--- Slot 2 --->|<--- Slot 3 --->|<--- Slot 4 --->|
Time: 0                T                2T               3T               4T
      |                 |                |                |                |
Sync: ^                 ^                ^                ^                |
      |                 |                |                |                |
NodeA [===== A의 데이터 =====]  (T=0에 시작)               |                |
NodeB |                 [===== B의 데이터 =====] (T에 시작)|
NodeC |                                  [==== C ====]  (충돌 발생)
NodeD |                                  [==== D ====]  (충돌 발생)

* 분석:
1. 모든 노드는 0, T, 2T 시점에만 전송 버튼을 누를 수 있음.
2. A와 B는 서로 다른 슬롯을 사용하여 충돌 없이 통신 성공 (50% 효율).
3. C와 D는 같은 시간(Slot 3)을 선택하여 완전히 겹침 -> 충돌.
4. 하지만 A의 슬롯이 끝나가는 시점에 B가 끼어드는 '부분 충돌'은 원천적으로 차단됨.
```

**핵심 알고리즘: 재전송 및 백오프 (Backoff)**
충돌이 발생했을 때, 모든 노드가 즉시 재전송을 시도하면 **'채널 포화(Channel Saturation)'** 상태에 빠집니다. 이를 방지하기 위해 다음과 같은 랜덤 지연 알고리즘을 사용합니다.

```python
# Pseudo-code for ALOHA Backoff Mechanism
def send_packet(packet):
    while True:
        transmit(packet)  # Send immediately or at next slot boundary
        
        if wait_for_ack(timeout):  # Success
            return SUCCESS
        else:  # Collision detected
            # Random Backoff Calculation
            # k: number of retransmission attempts
            # R: Random integer in range [0, 2^k - 1]
            wait_time = R * MAX_SLOT_TIME
            sleep(wait_time)
```

**📢 섹션 요약 비유**
Pure ALOHA를 도로에 비유하면, 운전자가 교차로에 진입할 때 신호등을 보지 않고 그냥 뛰어드는 것입니다. 다른 차량이 진입하는 순간 교차로는 꽉 막혀버립니다(S(n) 저하). 반면 Slotted ALOHA는 교차로 입구에 신호등을 설치하여, '초록불이 켜지는 타이밍(Slot Boundary)'에만 모든 차량이 동시에 출발하도록 통제하는 것입니다. 한 대만 나가면 좋지만, 여러 대가 동시에 나가면 여전히 충돌하지만, 적어도 진입하던 중에 다른 차랑 옆면으로 부딪히는 일은 막아줍니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Pure ALOHA vs. Slotted ALOHA

| 비교 항목 (Metric) | Pure ALOHA | Slotted ALOHA | 설명 (Description) |
|:---|:---|:---|:---|
| **전송 시점 (Tx Timing)** | 즉시 전송 (Immediate) | 슬롯 동기화 (Synchronized) | Slotted은 클럭 동기가 필수적임 |
| **취약 시간 ($T_v$)** | $2 \times T_{fr}$ | $1 \times T_{fr}$ | 충돌 가능 구간이 절반으로 감소 |
| **최대 효율 ($S_{max}$)** | 0.184 (18.4%) @ G=0.5 | 0.368 (36.8%) @ G=1 | Slotted이 정확히 2배의 성능 제공 |
| **복잡도 (Complexity)** | Low (단순 무작위) | Medium (타이밍 동기 필요) | Slotted은 시스템 클럭 유지 비용 발생 |
| **지연 시간 (Delay)** | 0 (No wait) | 0 ~ T (대기 발생) | Slotted은 데이터가 생겨도 다음 슬롯까지 기다려야 함 |
| **충돌 패턴** | 부분(Partial) & 완전(Complete) | 완전(Complete)만 발생 | Slotted은 패킷의 시작점이 항상 정렬됨 |

#### 2. 타 기술과의 융합 및 영향

ALOHA는 현대 네트워킹의 근간이 되는 **CSMA (Carrier Sense Multiple Access)** 계열 기술로 발전하는 교두보 역할을 했습니다.

① **CSMA/CD (Ethernet)**: ALOHA의 단순한 "보내고 보자" 방식에서 발전하여, **"캐리어 감지(Carrier Sense)"** 기능을 추가했습니다. 즉, 누군가 말하고 있으면 기다렸다가(Defer), 조용해지면 말하는 방식입니다. 이를 통해 불필요한 충돌을 획기적으로 줄였습니다.
② **Wi-Fi (CSMA/CA)**: 무선 환경에서는 충돌을 감지하기 어렵기 때문에, 전송 전에 **RTS/CTS (Request to Send / Clear to Send)** 제어 프레임을 통해 예약을 하고 전송하는 방식을 사용하며, 기본적인 백오프(Backoff) 알고리즘은 ALOHA의 정수를 계승하고 있습니다.
③ **RACH (Cellular Networks)**: 5G 및 LTE 네트워크에서 단말기가 기지국과 처음 연결될 때 사용하는 **랜덤 접속 채널(RACH)**은 Slotted ALOHA의 원리를 그대로 사용합니다. 단말은 프리앰블(Preamble)을 특정 슬롯에 전송하고, 충돌 여부를 기지국의 응답(MSG2)으로 판단합니다.

**📢 섹션 요약