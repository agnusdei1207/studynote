+++
title = "151-153. 물리 계층(1계층) 통신 장비"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 151
+++

# 151-153. 물리 계층(1계층) 통신 장비

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **OSI (Open Systems Interconnection) 7계층** 중 가장 하위인 물리 계층(Physical Layer, Layer 1)의 기능적 한계를 극복하기 위한 신호 증폭 및 매체 변환 장비들을 의미하며, **MAC 주소(Media Access Control Address)**와 같은 상위 계층 정보는 처리하지 않는다.
> 2. **가치**: 전송 거리 연장(Repeater)과 다중 포트 연결(Hub)을 통해 네트워크의 물리적 영역을 확장하나, **스위칭(Switching) 기능이 없는 더미 허브(Dummy Hub)**는 충돌 도메인(Collision Domain)을 분리하지 못해 대역폭 효율이 급격히 저하된다.
> 3. **융합**: 최근에는 단순 리피터 기능이 스위치나 라우터에 흡수되었으며, 트랜시버는 광통망(FTTH, Data Center) 핵심 모듈인 **SFP (Small Form-factor Pluggable)** 등으로 진화하여 고속 Ethernet 기반의 100Gbps 이상 환경을 지원한다.

---

### Ⅰ. 개요 (Context & Background)

물리 계층(Physical Layer, Layer 1) 장비는 네트워크 데이터 전송의 가장 기초가 되는 하드웨어 영역이다. 1계층 장비의 핵심 역할은 케이블을 통해 이동하는 비트열(Bit stream) 형태의 **아날로그/디지털 신호**가 전송 거리가 멀어짐에 따라 감쇠(Attenuation)되거나 외부 노이즈(Noise)로 인해 왜곡되는 현상을 물리적으로 해결하는 것이다. 이 계층의 장비들은 데이터의 **논리적 주소(IP Address)**나 **MAC 주소**, 상위 **프로토콜(Protocol)** 헤더를 이해하지 못하며, 단순히 전압 레벨을 감지하고 증폭하거나 연결 형태를 변경하는 역할만 수행한다. 초기 LAN(Local Area Network) 구축 단계에서는 코axial 케이블과 UTP(Unshielded Twisted Pair) 케이블의 물리적 거리 제한을 극복하기 위해 필수적이었으나, 스위칭 기술의 발달과 함께 스마트한 기능은 상위 계층 장비로 이동하였다.

**💡 비유**
물리 계층 장비는 '국도의 톨게이트'나 '음성 증폭기'와 같다. 차량(데이터) 안에 누가 탔는지(내용) 어디로 가는지(주소)는 전혀 확인하지 않고, 단순히 도로(케이블)가 끊기지 않도록 이어주거나(리피터), 여러 차로가 모이는 분기점(허브) 역할만 수행한다.

**등장 배경**
1.  **기존 한계**: 전기 신호는 구리선(UTP 등)을 지나면서 저항과 용량 성분으로 인해 거리가 멀어질수록 파형이 뭉개지고 신호 대 잡음비(SNR)가 악화되어 수신 측에서 0과 1을 구별할 수 없게 됨.
2.  **혁신적 패러다임**: 이를 해결하기 위해 신호가 약해지기 전에 중간에 '중계기'를 두어 신호를 재생(Regeneration)하거나, 여러 장비를 연결하기 위해 '허브'라는 집선 장치 도입.
3.  **현재의 비즈니스 요구**: 과거에는 단순 연결이 목적이었으나, 현재는 **PoE (Power over Ethernet)**처럼 데이터와 함께 전력까지 공급하는 고기능성 허브나, 고속 광통신을 위한 **트랜시버(Transceiver)** 모듈 형태로 데이터 센터 등에서 핵심적인 인프라 역할을 수행 중.

**📢 섹션 요약 비유**: 물리 계층 장비는 전기 신호라는 '달리기 선수'가 지치지 않도록 물을 주고 쉬게 해주는 '급소'(리피터)이자, 여러 갈래 길에서 하나의 길로 모아주거나 흩어지게 해주는 '로터리(허브)' 역할을 담당한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

물리 계층 장비는 크게 신호 증폭(Repeater), 다중 포트 연결(Hub), 매체 변환(Transceiver) 기능으로 세분화할 수 있다. 특히 허브(Hub)는 기술적 진화에 따라 Dummy, Switching, Intelligent 등 세부 카테고리가 나뉘며, 이는 Layer 1에서 Layer 2로 넘어가는 과도기적 아키텍처를 보여준다.

#### 1. 주요 구성 요소 및 동작 매커니즘

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/규격 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **AUI (Attachment Unit Interface)** | 외부 트랜시버 연결 포트 | NIC와 트랜시버 간의 디지털 신호 인터페이스 제공 | IEEE 802.3 | 마더보드 확장 슬롯 |
| **Repeat Circuit** | 신호 재생 및 타이밍 복원 | 입력된 RP(RP=1) 신호의 식별을 통해 0/1을 판별하고 클록 신호에 동기화하여 재생성 | Physical Layer Signaling | 노이즈 제거 및 복원 필터 |
| **MAU (Medium Attachment Unit)** | 매체 결합 장치 | 디지털 신호를 매체(전기/광)에 적합한 아날로그 파형으로 변조(Modulation) 및 역변조(Demodulation) | PMA (Physical Medium Attachment) | 변압기/모뎀 |
| **SNMP Agent** | 관리 정보 수집 (Intelligent Hub) | Hub 내부의 포트 상태, 트래픽 양, 충돌 횟수를 카운팅하여 관리 서버에 전송 | SNMP (Simple Network Management Protocol) | 감시 카메라 |

#### 2. 상세 신호 처리 다이어그램

```ascii
   [ A ]          [ B ]          [ C ]
    |              |              |
    | (Weak/Noisy)|              |
    +------------->|              |
         (Attenuated Signal)      |
                  |              |
              [ Repeater ]        |
                  |              |
         (Signal Regeneration)   |
                  |              |
      1. Clock Recovery (위상 복원)
      2. Signal Amplification (증폭)
      3. Collision Detection (충돌 감지 후 SQE 신호 생성)
                  |              |
                  +------------->+
                 (Clean Signal)
```
*(해설: 리피터는 단순히 전압을 높이는 것이 아니라, 디지털 신호의 식별자(Threshold)를 판별하여 0과 1을 다시 만들어내는 'Digital Regeneration' 과정을 수행한다. 이 과정에서 Jitter(지터)를 제거하여 신호 품질을 원상 복구한다.)*

#### 3. 허브(Hub)의 데이터 플로우와 충돌 도메인

**더미 허브(Dummy Hub)**의 가장 큰 특징은 **Shared Media (공유 매체)** 구조이다. 하나의 포트에 들어온 신호는 다른 모든 포트로 전송(Flooding)되며, 이는 동시 전송 시 **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)** 알고리즘에 의존할 수밖에 없게 만든다.

**HUB 동작 Pseudocode**:
```python
def hub_process(incoming_port, frame):
    # 1계층이므로 목적지 주소 확인 불가. 무조건 전체 브로드캐스트.
    if incoming_port.link_status == UP:
        for port in all_ports:
            if port != incoming_port:
                port.send(frame) # Blocking 방식, 병목 발생
```
반면, **스위칭 허브(Switching Hub)**는 내부에 **ASIC (Application-Specific Integrated Circuit)** 스위칭 패브릭이 장착되어 있어 **MAC 주소 테이블(MAC Address Table)**을 참조하여 특정 포트로만 스위칭한다. 이는 단순 1계층 기능을 넘어 2계층(Data Link Layer) 기능을 수행함을 의미한다.

#### 4. 트랜시버(Transceiver)와 MAU
트랜시버는 송신기(Transmitter)와 수신기(Receiver)의 결합체이다. NIC(Network Interface Card) 내부의 MAC 계층 로직과 외부의 물리적 매체(광케이블, 동축케이블) 사이의 전기적 특성(임피던스, 파장)을 매칭시킨다. 과거 10BASE5 시절에는 외장형 탭(Vampire Tap)을 사용하였으나, 현재는 SFP/SFP+ 모듈 형태로 메인보드나 스위치에 직접 장착된다.

**📢 섹션 요약 비유**: 더미 허브는 '공중전화 부스'가 하나인 마을이다. 한 사람이 전화를 쓰면 온 마을 사람들이 그 소리를 듣고(Broadcast), 다른 사람은 사용을 기다려야 한다(Shared Bandwidth). 스위칭 허브는 각 가정마다 전화기가 따로 있는 것과 같아서, 프라이버시도 보장되고(Non-blocking), 통신 효율이 훨씬 높다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

1계층 장비는 단독으로 존재하기보다 상위 계층(2계층 스위치, 3계층 라우터) 장비 내부에 모듈 형태로 내장되거나, 연동되어 사용된다.

#### 1. 심층 기술 비교표 (Repeater vs Hub vs Transceiver)

| 비교 항목 | 리피터 (Repeater) | 더미 허브 (Dummy Hub) | 스위칭 허브 (Switching Hub) | 트랜시버 (Transceiver) |
|:---|:---|:---|:---|:---|
| **OSI 계층** | Layer 1 (Physical) | Layer 1 (Physical) | Layer 2 (Data Link) | Layer 1 (Physical) |
| **핵심 기능** | 신호 증폭 및 재생 | 멀티포트 신호 복제 | MAC 주소 기반 스위칭 | 매체 변환 (전기 $\leftrightarrow$ 광) |
| **주소 처리** | None | None (Flooding) | MAC Address Learning | None |
| **대역폭** | Point-to-Point 전용 | Total Bandwidth / N (Shared) | Dedicated per Port | 매체 대역폭에 종속 |
| **Collision Domain** | 1개 (연속됨) | 1개 (전체 포트 공유) | N개 (포트당 1개) | N/A (Point-to-Point) |
| **지연(Latency)** | Bit time 수준 (极低) | Bit time 수준 (极低) | Microsecond 수준 (검색 지연) | 수 ns 수준 (변환 지연) |

#### 2. 타 영역(물리/보안)과의 융합
*   **물리(L1)와 전기/광학**: 트랜시버 기술은 전기통신 이론(변조/복조)과 밀접하게 연관된다. 예를 들어, 광 트랜시버는 LED나 VCSEL을 사용하여 전기 신호를 광 펄스로 바꾸며, 이때 전압 레벨과 파장(Wavelength, ex 1310nm, 1550nm)이 핵심 파라미터가 된다.
*   **보안(L2)과의 상관관계**: 더미 허브는 모든 패킷을 모든 포트로 뿌리기 때문에, 특정 포트를 **Promiscuous Mode(무차별 모드)**로 설정하면 **Sniffing(도청)**이 매우 쉽다. 반면, 스위칭 허브는 기본적으로 타 포트 트래픽이 보이지 않아 보안성이 높으나, **ARP Spoofing** 등을 통해 이를 우회할 수 있다.
*   **성능 오버헤드**: 리피터나 더미 허브를 사용하여 네트워크를 무한히 연결할 수는 없다. **5-4-3 Rule** (이더넷 규칙)에 따라, 신호의 왕복 시간(Round Trip Time)이 **Slot Time(512bit time)**을 초과하면 충돌 감지가 불가능해져 네트워크가 마비된다.

**📢 섹션 요약 비유**: 리피터는 '연료 보급차'처럼 거리만 늘려줄 뿐이고, 더미 허브는 '차가 많은 1차선 도로'에서 횡단보도를 만드는 것과 같아서 지름길(U-Turn)이 없어 사고(충돌)가 나면 전체가 막힌다. 스위칭 허브는 각 차량이 비행기를 타고 다니는 것과 같아 서로 충돌할 일이 없다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 설계에서 1계층 장비를 선정할 때는 비용(Cost)과 성능(Performance), 그리고 확장성(Scalability) 사이의 균형을 고려해야 한다.

#### 1. 실무 시나리오 및 의사결정

*   **시나리오 A: 노후 공장 구내 망 확장**
    *   **상황**: 200m 떨어진 센서 데이터를 UTP 케이블로 가져와야 함.
    *   **의사결정**: 이더넷 케이블의 이론적 거리 한계(100m)를 초과하므로, 중간 지점(100m 지점)에 **Repeater** 혹은 **PoE Extender**를 설치하여 신호를 재생해야 한다. 단, 단순 리피터보다는 충돌 도메인을 분리할 수 있는 **L2 Switch**를 중계 장비로 사용하는 것이 현대적인 추세이다.
*   **시나리오 B: 소규모 사무실 보안 구축**
    *   **상황**: 예산이 적고 5대의 PC만 연결하며 데이터 보안이 중요하지 않음.
    *   **의사결정**: 허브(Hub)는 현재 단종되거나 가격이 스위치와 비슷하여 잘 사용하지 않는다. 가성비 좋은 **Unmanaged Switch**를 사용하여 개인 대역폭을 확보하는 것이 타당하다.
*   **시나리오 C: 데이터 센터 광케이블 연결**
    *   **상황**: 서버 랙에서 코어 스위치까지 40km 거리 연결.