+++
title = "NW #16 전파 지연 (Propagation Delay) - 거리/속도"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #16 전파 지연 (Propagation Delay) - 거리/속도

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전파 지연(Propagation Delay)은 신호가 매체를 통해 물리적 거리를 이동하는 시간($d/s$)으로, 전송 로직과 무관한 물리 법칙(빛의 속도)에 종속된 절대적 한계값이다.
> 2. **가치**: 고속 대역폭(Bandwidth) 아키텍처에서도 RTT (Round Trip Time)을 증가시켜 TCP (Transmission Control Protocol) 혼잡 제어 성능을 저하시키는 주요 병목 요인으로 작용한다.
> 3. **융합**: 5G/6G 네트워크와 자율주행에서 1ms 이하의 지연을 달성하기 위해 물리적 거리를 줄이는 엣지 컴퓨팅(Edge Computing) 및 저궤도 위성(LEO) 기술과 직접 연계된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**전파 지연(Propagation Delay, $d_{prop}$)**은 데이터의 비트(bit)가 송신자(송신 노드)에서 수신자(수신 노드)로 도달하기 위해 링크(매체)를 물리적으로 이동하는 데 걸리는 시간을 의미한다. 이는 처리(Processing) 지연, 큐잉(Queuing) 지연, 전송(Transmission) 지연과 함께 네트워크 총 지연 시간을 구성하는 4대 요소 중 하나이다.
전파 지연의 결정적인 특징은 **'소프트웨어적 최적화가 불가능한 물리적 제약'**이라는 점이다. 아무리 프로토콜을 효율화하거나 코딩을 잘해도, 신호가 빛의 속도($c$) 혹은 그 이하의 속도로 이동해야 하는 시간은 줄일 수 없다. 따라서 라우터(Router)나 스위치(Switch)의 성능 지표가 아닌, 전송 매체의 물리적 특성과 지리적 거리에 의해 결정된다.

#### 2. 배경 및 필연성
초기 인터넷(LAN 환경)에서는 거리가 짧아 전파 지연이 무시되었으나, 통신망이 전 지구적으로 확장되고 클라우드(Cloud) 시대가 도래하면서 장거리 통신에서 병목이 발생했다. 특히 위성 통신이나 대륙 간 해저 케이블 통신에서는 수백 밀리초(ms)의 지연이 발생하여 실시간 응용 서비스에 치명적임이 밝혀졌다. 이에 따라 전파 지연을 최소화하는 네트워크 토폴로지 설계가 중요해졌다.

#### 3. ASCII 다이어그램: 지연 구성 내 위치
전파 지연은 총 지연 시간의 마지막 단계이자 물리적 이동 단계이다.

```ascii
[ Total Nodal Delay Breakdown ]

| 1. Processing | 2. Queuing | 3. Transmission |==== 4. Propagation ====|
    (Check)        (Wait)        (Push Bits)        (Travel Distance)
                                                |
                                               / \
                                              /   \
                                             /     \
                                          Source     Destination
                                          (Router A)  (Router B)
                                            <-------->
                                             Distance
```
*(도입 설명)*: 위 다이어그램과 같이 전파 지연은 시스템 내부의 논리적 작업(처리, 대기)이 모두 끝난 후, 신호가 실제로 회선을 타고 날아가는 시간을 뜻한다.

📢 **섹션 요약 비유**: 전파 지연은 아무리 빠른 우편 배달부(처리 속도)가 편지를 챙겨도, 서울에서 부산까지 고속도로를 달리는 데 걸리는 **'물리적 주행 시간'**과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 수식 및 파라미터 분석
전파 지연의 핵심 공식은 단순 명료하지만, 그 내부 변수($s$)가 매체의 물리적 성질에 따라 결정된다.

$$d_{prop} = \frac{m}{s} = \frac{\text{Length of Link}}{\text{Propagation Speed}}$$

- **$d_{prop}$**: 전파 지연 시간 (Second, s)
- **$m$**: 전송 매체의 길이 / 물리적 거리 (Meter, m)
- **$s$: 매체 내 전파 속도 (Meter/sec, m/s)**
    - 이 값은 빛의 속도($c \approx 3 \times 10^8$ m/s)보다 항상 느리거나 같다.

#### 2. 매체별 속도 상수 (Speed Factor)
신호가 진공 상태가 아닌 매체를 통과할 때, 유전율(Permittivity)이나 굴절률(Refractive Index)로 인해 속도가 저하된다. 이를 엔지니어링할 때는 **VF (Velocity Factor)**라는 비율을 사용한다.

| 전송 매체 (Media) | 전파 속도 ($s$) | VF ($s/c$) | 비고 |
|:---:|:---:|:---:|:---|
| **Vacuum (진공)/Space** | $3.00 \times 10^8$ m/s | 1.00 (100%) | 이론적 최대치 |
| **Air (대기권)** | $\approx 2.99 \times 10^8$ m/s | 0.99 | 거의 빛의 속도 |
| **Optical Fiber (광섬유)** | $\approx 2.00 \times 10^8$ m/s | 0.67 | 코어 굴절률 $n=1.5$ 가정 |
| **Copper (UTP/Coax)** | $\approx 1.9 \sim 2.3 \times 10^8$ m/s | 0.65 ~ 0.77 | 절연체 종류에 따라 상이 |
| **Water (해저 환경)** | - | 0.75 | 전자기파 감쇠 심함 |

#### 3. ASCII 다이어그램: 매체별 속도 시각화
동일한 거리라도 매체에 따라 도착 시점이 달라짐을 확인할 수 있다.

```ascii
[ Propagation Speed Race (Distance: 1,000 km) ]

Start Line                                               Finish Line
  |                                                           |
  +--> [ Vacuum / Air ]   (v = c)   --------------------> O (t=3.3ms)
  |
  +--> [ Copper Cable ]   (v~0.7c)  ------------------->    O (t=4.7ms)
  |
  +--> [ Fiber Optic ]    (v~0.67c) ----------------->       O (t=5.0ms)
                                         ^              ^
                                         |              |
                                    (Fiber is slower than Vacuum)
```
*(도입 설명)*: 다이어그램은 1,000km를 이동할 때 광섬유가 진공 공기보다 약 1.7ms 느리게 도착함을 보여준다.
*(해설)*: 많은 사람들이 광섬유가 가장 빠르다고 생각하지만, 물리적으로는 공기 중(무선 주파수)이 가장 빠르다. 하지만 광섬유는 감쇠(Attenuation)가 적고 외부 간섭이 없어 장거리 데이터 무결성에는 가장 유리하다. 따라서 전파 지연 단축만을 위해 FSO (Free Space Optical) 통신을 고려하기도 한다.

#### 4. 실무 코드 및 계산 예시
엔지니어는 링크 설계 시 이 지연 값을 미리 산출하여 SLA (Service Level Agreement)를 준수하는지 확인한다.

```python
import ipaddress

# Constants
C = 299_792_458  # Speed of light in vacuum (m/s)
VF_FIBER = 0.67  # Velocity Factor for Fiber (SMF-28)

def calculate_propagation_delay(distance_km, medium_vf):
    """
    Calculates propagation delay in milliseconds.
    :param distance_km: Physical distance in kilometers
    :param medium_vf: Velocity Factor (0.0 ~ 1.0)
    """
    dist_m = distance_km * 1000
    speed = C * medium_vf
    delay_sec = dist_m / speed
    return delay_sec * 1000 # Convert to ms

# Scenario: New York to London (~5,585 km, roughly)
dist = 5585
fiber_delay = calculate_propagation_delay(dist, VF_FIBER)
vacuum_delay = calculate_propagation_delay(dist, 1.0)

print(f"Fiber Delay: {fiber_delay:.2f} ms")  # Result: ~27.76 ms
print(f"Theoretical Min Delay: {vacuum_delay:.2f} ms") # Result: ~18.6 ms
```

📢 **섹션 요약 비유**: 전파 지연의 속도 차이는 **'포장도로 vs 자갈길'**에서 달리기 속도가 다른 것과 같습니다. 비행기(진공)가 가장 빠르지만, 기차(광섬유)가 안전하고 정확하게 운행할 수 있는 것처럼 실무는 안정성과 속도 사이의 균형을 맞춰야 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Propagation vs Transmission
엔지니어는 종종 전파 지연과 전송 지연(Transmission Delay)을 혼동한다. 이를 명확히 구분하는 것이 성능 튜닝의 핵심이다.

| 비교 항목 | 전파 지연 (Propagation Delay) | 전송 지연 (Transmission Delay) |
|:---|:---|:---|
| **정의** | 비트가 매체를 통해 이동하는 시간 | 패킷의 모든 비트가 링크로 밀려나가는 시간 |
| **결정 요인** | **거리($d$), 매체 속도($s$)** | **패킷 크기($L$), 링크 대역폭($R$)** |
| **공식** | $d/s$ | $L/R$ |
| **줄이는 법** | 거리 단축 (Edge, CDN) | 대역폭 증설 (10Gbps $\to$ 100Gbps) |
| **물리적 성질** | 물리 법칙 (상대성 이론) | 전기/광학 신호 처리 능력 |

#### 2. ASCII 다이어그램: 두 지연의 차이

```ascii
[ Packet Lifecycle Visualized ]

  Time Axis ----->

  [ Transmission Delay (L/R) ]      [ Propagation Delay (d/s) ]
  |<---------------------------->|   |<----------------------->|
  
  Pushing Bits onto Wire           Bits traveling through the wire
  (Router Job)                     (Physics Job)
  
  |-Bit1-|-Bit2-|-Bit3-|-Bit4-|
    ^      ^      ^      ^
    |      |      |      |
  Start Tx           Last Bit Tx
                           \
                            \  First Bit Arrives (d_prop later)
                             \
                              V
                         |-Bit1-|-Bit2-|-Bit3-|-Bit4-|
                         |<---- Reception Tx Time ---->|
                         (Receiver sees all bits)
```
*(도입 설명)*: 송신자 입장에서 전송 지연은 패킷을 밀어내는 노력이고, 전파 지연은 첫 번째 비트가 도착지까지 가는 시간이다.
*(해설)*: **핵심은 전송 지연은 대역폭 업그레이드로 0에 수렴하게 만들 수 있지만, 전파 지연은 거리가 같으면 0으로 만들 수 없다.** 예를 들어 1Gbps 링크든 100Gbps 링크든 광섬유 100km를 통과하는 시간은 약 0.5ms로 동일하다. 따라서 WAN(Wide Area Network) 환경에서는 대역폭을 올려도 Latency가 줄어들지 않는 현상이 발생한다.

#### 3. TCP 프로토콜과의 융합 (Convergence)
TCP의 성능은 **BDP (Bandwidth-Delay Product)**에 의해 제한된다.
$$ \text{BDP (bits)} = \text{Bandwidth (bps)} \times \text{RTT (s)} $$
- $RTT$ (Round Trip Time)의 대부분은 전파 지연(왕복)이 차지한다.
- 전파 지연이 크면 BDP가 커져, TCP 윈도우(Window) 크기를 매우 크게 설정해야 대역폭을 100% 채울 수 있다.
- 고속 위성 링크(High Latency, High BW)에서는 적절한 Window Size를 맞추지 않으면 대역폭 낭비가 심각하다.

📢 **섹션 요약 비유**: 전송 지연은 **'수도관의 굵기'**를 키우는 것이고, 전파 지연은 **'수도관의 길이'**를 줄이는 것입니다. 아무리 굵은 관을 깔아도 파이프가 서울에서 부산까지 이어져 있다면 물이 나오는 데까지는 시간이 걸립니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 글로벌 게임 서버 최적화
**문제 상황**: 한국 서버에서 미국(버지니아) 리전을 이용하는 온라인 FPS 게임에서 핑(Ping)이 180ms 이상 발생하여 유저 이탈이 발생함.
**의사결정 과정**:
1.  **원인 분석**: 네트워크 병목 지점 확인. 결과적으로 광케이블 경로가 길어 전파 지연이 150ms 이상 소요되는 것으로 확인됨 (대역폭은 여유).
2.  **대안 검토**:
    *   대안 A: 회선 증설 (비용 상승, 전파 지연 $d/s$ 해결 불가).
    *   대안 B: UDP 프로토콜 최적화 (전파 지연 자체는 줄어들지 않음, 패킷 손실만 방지).
    *   대안 C: **엣지 컴퓨팅(Edge Computing) 도입**.
3.  **최종 판단**: 대안 C 채택. AWS CloudFront나 Local Zones를 통해 게임 서버 로직을 사용자 인근(일본 또는 서부 미국)으로 전진 배치하여 물리적 거리($d$)를 1/5로 단축. 전파 지연을 30ms 수준으로 감소.

#### 2. 도입 체크리스트
| 구분 | 항목 | 확인 포인트 |
|:---:|:---|:---|
| **기술적** | 라우팅 최적화 | **AS Path**가 물리적으로 최단 경로(지리적)를 보장하는가? (BGP 튜닝) |
| **기술적** | 매체 선택 | 동일 거리라면 굴절률이 낮은(Low Loss) 광섬유를 사용하여 $s$를 최적화했는가? |
| **운영/보안적** | 거리 가려내기 | 금융 거래 등에서 HFT(High Frequency Trading)를 위해 마이크로웨이브 무선망(빛보다 느리지만 꼬불꼬불한 케이블보다 직선 거리 짧음)을 고려하는가? |

#### 3. 안티패턴 (Anti-Pattern)
- **전파 지연을 대역폭으로 해결하려는 시도**: "