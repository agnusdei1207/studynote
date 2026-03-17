+++
title = "237-241. L2 스위치의 동작 원리와 MAC 주소 테이블"
date = "2026-03-14"
[extra]
category = "LAN/WAN & L2 Devices"
id = 237
+++

# 237-241. L2 스위치의 동작 원리와 MAC 주소 테이블

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: L2 스위치(Layer 2 Switch)는 **MAC (Media Access Control)** 주소를 기반으로 프레임을 필터링하고 전달하여, 물리적인 **충돌 도메인(Collision Domain)**을 포트 단위로 분할하는 지능형 네트워크 장비이다.
> 2. **가치**: 허브(Hub) 기반의 공유 미디어 방식에서 발생하는 충돌(Collision)과 대역폭 낭비를 제거하여, 전이중(Full-Duplex) 통신을 통해 네트워크 효율을 극대화하고 대역폭을 포트 수만큼 독립적으로 확보한다.
> 3. **융합**: **CAM (Content Addressable Memory)** 하드웨어를 활용한 고속 주소 검색 기술과 **STP (Spanning Tree Protocol)**와의 연계를 통해 루프 구조를 제어하며, 이는 3계층 라우팅 및 보안 VLAN 설계의 기초가 된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**L2 스위치(Layer 2 Switch)**는 OSI 7계층 모델 중 **데이터 링크 계층(Data Link Layer, Layer 2)**에서 동작하는 네트워크 장비로, 수신된 이더넷 프레임(Frame)의 **MAC 헤더(MAC Header)**를 분석하여 목적지 장비로 데이터를 전송(Forwarding)한다. 이 과정에서 단순히 신호를 증폭하는 리피터(Repeater)나 허브(Hub)와 달리, 소프트웨어 로직과 전용 하드웨어(ASIC)를 결합하여 **"누가 어디에 있는지"**를 파악하고 데이터의 흐름을 제어한다.

#### 2. 💡 비유
전화기가 없던 시절의 마을 방송(허브)과 전화 교환수(스위치)의 차이와 같다. 허브는 마을 공동 우물가에서 누군가 소리치면 모든 주민이 듣는 것과 같아서, 동시에 두 사람이 말하면 소음(충돌)이 발생한다. 스위치는 각 집에 전화기를 놓아주고, 교환수가 전화를 거는 사람과 받는 사람을 연결해주는 것과 같아서 여러 통화가 동시에 진행된다.

#### 3. 등장 배경 및 진화
① **공유 미디어의 한계 (Legacy)**: 초기 이더넷은 버스(Bus)형 토폴로지 기반의 CSMA/CD 방식을 사용하여, 한 번에 한 장비만 전송 가능한 **반드반(Half-Duplex)** 환경이었다. 네트워크 규모가 커질수록 충돌 확률이 급증하여 유효 대역폭이 급격히 감소하는 문제가 발생했다.
② **스위칭 기술의 도입 (Innovation)**: 이를 해결하기 위해 **브리지(Bridge)** 기술이 발전하였고, 이를 하드웨어적으로 고속화한 것이 스위치이다. 포트별로 **충돌 도메인(Collision Domain)**을 물리적으로 분리함으로써 논리적으로는 하나의 네트워크이나 물리적으로는 독립적인 회선을 제공하게 되었다.
③ **현재의 비즈니스 요구 (Modern)**: 현재는 **가상화(Virtualization)**와 클라우드 환경에 대응하기 위해 VXLAN 오버레이 등과 결합하여 수천만 개의 MAC 주소를 학습하는 하이퍼바이저 내부 스위치(OVS) 등으로 진화하고 있다.

#### 4. 📢 섹션 요약 비유
마치 복잡한 고속도로 톨게이트에서 하이패스 차선(고속 패스)을 별도로 운영하여, 각 차량이 다른 차량과 충돌 없이 자신만의 전용 차로로 목적지까지 빠르게 이동할 수 있게 해주는 교통 통제 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스위치의 지능형 동작은 내부의 **MAC 주소 테이블(MAC Address Table)**, 일명 **CAM 테이블(CAM Table)**에 의존한다.

#### 1. 구성 요소 및 핵심 모듈

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **MAC 주소 테이블**<br>(MAC Address Table) | 목적지 경로 저장소 | 포트 번호와 MAC 주소를 매핑하여 저장. <br>**CAM (Content Addressable Memory)** 사용 시 O(1) 시간복잡도로 검색. | IEEE 802.1D | 교환수의 전화번호부 |
| **ASIC / NPU**<br>(Switching Engine) | 고속 스위칭 엔진 | 프레임 헤더를 분석하고 테이블을 룩업(Lookup)하여 <br>수신 포트에서 송신 포트로 데이터를 복사/전송. | Hardware Logic | 고속 분류기 |
| **입력 큐**<br>(Ingress Queue) | 수신 버퍼링 | 포트로 들어오는 프레임을 일시 저장. <br>**Head-of-Line (HOL) Blocking** 방지 기능 포함. | QoS (Queueing) | 입구 대기실 |
| **출력 큐**<br>(Egress Queue) | 송신 버퍼링 | 송신 포트가 전송 중일 때 프레임을 대기시킴. <br>**Congestion Management**를 위한 큐 큐(Queue) 관리. | IEEE 802.1Q (Priority) | 출구 대기실 |
| **제어 평면**<br>(Control Plane) | 학습 및 관리 | **프로토콜 프로세서**가 새로운 MAC 주소를 학습(Learning)하고 <br>오래된 주소를 삭제(Aging)하는 로직 수행. | SNMP / STP | 관리자 |

#### 2. MAC 주소 테이블 구조 및 학습 메커니즘

스위치는 전원이 켜지면 빈 상태의 MAC 테이블(Forwarding Database)을 가지게 되며, 다음과 같은 동작 프로세스를 통해 테이블을 채워 나간다.

```ascii
      [   L2 스위치 내부 구조   ]

  Ingress Port          Switch Fabric         Egress Port
       |                       |                    ^
       v                       v                    |
  [ Ingress Queue ] --> [ ASIC Lookup ] --> [ Egress Queue ]
                             |
                             v
                  +-----------------------+
                  |   MAC Address Table   |
                  | (CAM / TCAM Memory)   |
                  +-----------------------+
                  | MAC Address   | Port  |
                  |---------------|-------|
                  | AA:AA:AA:AA   |  1    |  <--- Learning (수신)
                  | BB:BB:BB:BB   |  2    |
                  | CC:CC:CC:CC   |  3    |
                  +---------------+-------+

[ 동작 흐름 예시: PC A(PC1)가 PC C(PC3)에게 데이터 전송 ]

(1) 수신 (Receive): PC A(Frame Src: AA, Dst: CC) ---> Port 1

(2) 학습 (Learning): 스위치는 "Port 1에 AA가 있구나" 인지 후 테이블에 기록

(3) 룩업 (Lookup): 목적지 CC 주소로 테이블 검색
      -> 검색 결과: Port 3에 존재함 확인

(4) 전달 (Forwarding): Port 3으로만 프레임을 스위칭
      -> Port 2에는 데이터가 전송되지 않음 (보안 및 대역폭 절약)
```

**[다이어그램 해설]**
위 다이어그램은 스위치 내부에서 프레임이 처리되는 데이터 경로(Data Plane)와 제어 경로(Control Plane)의 상호작용을 보여줍니다. 수신 포트(Ingress)에서 들어온 프레임은 **ASIC (Application Specific Integrated Circuit)** 엔진에 의해 즉시 분석됩니다. 엔진은 프레임 헤더의 **출발지 MAC 주소(Source MAC)**를 추출하여 MAC 테이블에 해당 포트 번호(Port 1)와 매핑시켜 저장(Learning)합니다. 동시에 **목적지 MAC 주소(Destination MAC)**를 키(Key)로 하여 테이블을 검색(Lookup)하는데, 이때 **CAM (Content Addressable Memory)**의 특수한 하드웨어적 회로 덕분에 수백만 개의 주소 중에서도 단 1 클럭의 딜레이로 목적지 포트(Port 3)를 찾아냅니다. 찾은 결과를 바탕으로 스위치 패브릭(Fabric)은 데이터를 목적지 포트로만 스위칭하며, 이 과정은 소프트웨어 개입 없이 하드웨어적으로 처리되므로 와이어 스피드(Wire Speed)로 전송이 가능합니다.

#### 3. 5대 핵심 동작 프로세스 (Deep Dive)

**① 학습 (Learning)**
*   **정의**: 스위치는 프레임이 들어온 포트(Source Port)와 프레임 헤더에 있는 **출발지 MAC 주소(Source MAC Address)**를 쌍으로 묶어 MAC 테이블에 기록하는 동작입니다.
*   **메커니즘**: `Address Table.add(Port_ID, Source_MAC)` 함수가 실행됩니다.
*   **주의점**: MAC 주소는 **유니캐스트(Unicast)** 주소여야 하며, 브로드캐스트(FF:FF:FF:FF:FF:FF)나 멀티캐스트 주소는 학습하지 않습니다.

**② 전달 (Forwarding)**
*   **정의**: 목적지 MAC 주소가 테이블에 존재하고, 그 목적지가 수신 포트와 다른 경우에만 해당 포트로 프레임을 내보내는 동작입니다.
*   **성능 지표**: 이 과정은 **Store-and-Forward (저장 후 전송)** 방식이 일반적이므로, **Latency (지연 시간)**는 프레임 전체 수신 시간 + 룩업 시간 + 출력 큐 대기 시간의 합으로 결정됩니다.

**③ 플러딩 (Flooding)**
*   **정의**: 목적지 MAC 주소가 테이블에 없는 **알 수 없는 유니캐스트(Unknown Unicast)**이거나, 브로드캐스트/멀티캐스트 프레임인 경우, 수신 포트를 제외한 **모든 포트(All Ports)**로 프레임을 복제하여 전송합니다.
*   **이유**: 스위치는 목적지가 어디 있는지 모르기 때문에, 네트워크 상에 목적지가 있을 가능성이 있는 모든 경로로 데이터를 쏘아 답을 기다리는 전략을 취합니다.

**④ 필터링 (Filtering)**
*   **정의**: 목적지 MAC 주소가 **수신 포트와 동일한 포트**에 연결된 장비인 경우, 프레임을 다른 포트로 내보내지 않고 내부에서 폐기(Drop)하는 동작입니다.
*   **효과**: 불필요한 트래픽이 백본(Backbone)이나 다른 세그먼트로 유출되는 것을 방지하여 전체 네트워크의 대역폭을 절약합니다.

**⑤ 에이징 (Aging)**
*   **정의**: MAC 테이블의 메모리 효율성과 이동성(Mobility)을 위해, 일정 시간 동안 통신이 없는 엔트리(Entry)를 자동으로 삭제하는 기능입니다.
*   **메커니즘**: 각 엔트리마다 **타이머(Timer, 기본 300초)**가 존재하며, 해당 주소로부터 프레임이 수신될 때마다 타이머가 리셋(Reset)됩니다. 타이머가 만료되면 `Table.remove(MAC_Address)`가 수행됩니다.

#### 4. 핵심 알고리즘: MAC 러닝 및 플러딩 의사코드

```python
# Pseudo-code for L2 Switch Forwarding Logic
class L2Switch:
    def __init__(self):
        # Key: MAC_Addr, Value: {Port, Last_Updated_Time}
        self.mac_table = MacTable() 
        self.aging_time = 300 # seconds

    def process_frame(self, frame, ingress_port):
        src_mac = frame.header.src_mac
        dst_mac = frame.header.dst_mac

        # 1. Learning Process (항상 수행)
        # 출발지 MAC이 테이블에 없거나, 포트가 변경되었으면 업데이트
        if self.mac_table.get(src_mac) is None:
            self.mac_table.add(src_mac, ingress_port)
            print(f"[LEARN] {src_mac} is on Port {ingress_port}")
        else:
            self.mac_table.update_timer(src_mac)

        # 2. Forwarding Decision
        if is_broadcast(dst_mac) or is_multicast(dst_mac):
            # Flooding required
            self.flood_frame(frame, ingress_port)
        
        elif self.mac_table.get(dst_mac) is None:
            # Unknown Unicast -> Flooding
            print(f"[FLOOD] Destination {dst_mac} unknown. Flooding...")
            self.flood_frame(frame, ingress_port)
            
        else:
            # Known Unicast
            egress_port = self.mac_table.get(dst_mac).port
            
            if egress_port == ingress_port:
                # Filtering: Drop frame
                print(f"[FILTER] Src and Dst on same port {ingress_port}. Dropping.")
                return
            
            # Forwarding: Send to specific port
            self.send_frame(frame, egress_port)
            print(f"[FWD] {src_mac} -> {dst_mac} via Port {egress_port}")

    def flood_frame(self, frame, ingress_port):
        for port in self.ports:
            if port.id != ingress_port:
                port.send(frame)
```

#### 5. 📢 섹션 요약 비유
스위치의 동작 원리는 **은행의 고객 관리 시스템**과 유사합니다. 은행원(스위치)은 방문하는 고객(**Source MAC**)의 얼굴과 창구 번호(**Port**)를 기억장치(**CAM Table**)에 저장합니다(**Learning**). 누군가 돈을 보내려 할 때, 받는 사람(**Dest MAC**)이 기억나면 그 창구로만 안내(**Forwarding**)하고, 기억나지 않으면 방송(**Flooding**)을 돌려 찾습니다. 오랫동안 보이지 않는 고객 정보는 주기적으로 데이터베이스에서 정리(**Aging**)합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 허브(Hub) vs 스위치(Switch)

| 비교 항목 | 허브 (Hub / Repeater) | L2 스위치 (L2 Switch) | 설명 |
|:---|:---|:---|:---|
| **동작 계층** | **OSI 1계층 (Physical Layer)** | **OSI 2계�