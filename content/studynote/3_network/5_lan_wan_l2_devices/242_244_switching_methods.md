+++
title = "242-244. 스위치의 프레임 전송 방식 (Switching Methods)"
date = "2026-03-14"
[extra]
category = "LAN/WAN & L2 Devices"
id = 242
+++

# 242-244. 스위치의 프레임 전송 방식 (Switching Methods)

> **1. 본질 (Essence)**: L2 스위치(Layer 2 Switch)가 수신한 프레임을 **버퍼링(Buffering) 없이 즉시 전송할지, 전체 수신 후 오류 검사(Error Check)를 수행할지**에 따라 전송 지연 시간(Latency)과 무결성(Integrity) 간의 트레이드-오프(Trade-off)를 결정하는 핵심 스위칭 펌웨어 로직입니다.
>
> **2. 가치 (Value)**: Cut-through 방식은 마이크로초(µs) 단위의 초저지연을 실현하여 HFT(High-Frequency Trading)와 같은 금융 네트워크에서 필수적이며, Store-and-Forward 방식은 CRC(Cyclic Redundancy Check) 기반의 완벽한 에러 회선을 제공하여 데이터 센터의 신뢰성을 보장합니다.
>
> **3. 융합 (Convergence)**: 컴퓨터 구조의 **캐시 메모리(Cache Memory)** 정책(Write-through vs Write-back)과 유사한 설계 철학을 가지며, OSI 7계층의 **데이터 링크 계층(Data Link Layer)** 물리적 주소 처리와 MAC 주소 테이블(MAC Address Table) 조회 프로세스와 직접 연결됩니다.

---

### Ⅰ. 개요 (Context & Background)

스위치(Switch)의 프레임 전송 방식은 데이터 프레임의 **포워딩 결정 시점**과 **버퍼링(Buffering) 사용량**을 결정하는 내부 아키텍처로, 네트워크의 성능(Performance)과 신뢰성(Reliability)의 균형을 좌우합니다.

**1. 개념 및 정의**
L2 스위치는 프레임을 수신하여 **목적지 MAC 주소(Destination MAC Address)**를 확인하고, MAC 주소 테이블(MAC Address Table)을 참조하여 출구 포트(Egress Port)를 결정합니다. 이때 스위치가 수신 프레임을 **언제까지 저장(Hold)하고 처리(Processing)하는가**에 따라 크게 **Store-and-Forward(저장 후 전송)**, **Cut-through(직접 전송)**, **Fragment-Free(단편 방지)**의 세 가지 방식으로 분류됩니다. 이는 본질적으로 **지연 시간(Latency) 최소화**와 **에러 전파(Error Propagation) 방지** 사이의 기술적 타협점입니다.

**2. 등장 배경 및 기술적 진화**
초기 이더넷(Ethernet) 환경인 공유 미디어(Shared Media, 허브 기반) 시대에는 CSMA/CD(Carrier Sense Multiple Access with Collision Detection) 기반의 충돌(Collision)이 빈번하여 **'충돌 폐기(Collision Discard)'** 로직이 중요했습니다. 하지만 스위칭 허브(Switching Hub)의 등장과 전이중(Full-Duplex) 통방식이 일반화되면서 충돌은 현저히 줄었습니다. 그러나 네트워크 트래픽의 폭발적 증가와 실시간 트래픽(Voice/Video)의 등장은 **'초저지연(Low Latency)'** 요구로 이어졌습니다. 이에 따라 단순한 Store-and-Forward 방식에서 벗어나, 헤더만 확인하고 바로 보내는 Cut-through 기술이 등장하였고, 이 두 극단을 절충하기 위해 Fragment-free 방식이 고안되었습니다.

**3. 비유적 이해**
이는 **택배 허브(Terminal)**에서 물건을 분류하는 원리와 같습니다. 모든 박스를 열어 내용물을 확인한 후 보내는 방법(Store-and-Forward), 주소 라벨만 보고 즉시 트럭에 싣는 방법(Cut-through), 박스를 던져보고 깨지는 소리가 나는지 확인 후 싣는 방법(Fragment-free) 중 하나를 선택하는 것과 같습니다.

> **📢 섹션 요약 비유**: 
> 마치 고속도로 **톨게이트(Tollgate)** 시스템과 같습니다. **Store-and-Forward**는 차량을 완전히 정지시켜 차적지와 화물 상태를 모두 확인한 후 통과시키는 방식이고, **Cut-through**는 차량이 지나가는 순간 번호판만 인식하여 바로 통과시키는 **하이패스(Hi-Pass)** 시스템과 유사합니다. **Fragment-Free**는 차량이 진입하는 순간 차체 결함 여부만 육안으로 빠르게 확인하는 **간이 검문** 방식에 비유할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스위칭 방식의 차이는 메모리 버퍼(Memory Buffer) 사용량과 **FCS(Frame Check Sequence)** 처리 시점에 달려있습니다.

**1. 구성 요소 및 파라미터 (Matrix)**

| 구성 요소 (Component) | 역할 (Role) | Store-and-Forward | Cut-through | Fragment-Free |
|:---|:---|:---:|:---:|:---:|
| **Ingress Buffer** | 수신 포트 버퍼링 | **Full Frame 저장** (FC까지) | **Byte Only** (Header만) | **64 Bytes 저장** |
| **Latency Factor** | 지연 시간 결정 요인 | Frame Size (비례) | Fixed (최소) | Fixed (소량) |
| **Error Handling** | 에러 처리 방식 | **CRC Check (완벽)** | **수행 안 함 (무조건 전송)** | Collision Check (Runts만) |
| **Processing Logic** | 포워딩 로직 | Store → CRC → Forward → TX | RX → Lookup → Forward (TX) | RX(64B) → Check → Forward |

**2. 스위칭 방식별 ASCII 다이어그램 및 데이터 흐름**

아래는 프레임 수신 지점(Ingress)에서 송신 지점(Egress)으로의 데이터 흐름과 처리 병목 지점(Bottleneck)을 시각화한 것입니다.

```ascii
[ Ethernet Frame Structure ]
+--------+--------+--------+------------+--------------------------+-----+
| Preamble|  DA   |  SA   |  Type/Len  |       Payload           | FCS |
| (8B)   | (6B)  | (6B)  |   (2B)     |     (46~1500B)          |(4B) |
+--------+--------+--------+------------+--------------------------+-----+
   ^          ^        ^                    
   |          |        |                    
   |          |        +---- Source MAC Address (출발지 MAC)
   |          +------------- Destination MAC Address (목적지 MAC)
   +------------------ SFD (Start Frame Delimiter)

[ 1. Store-and-Forward (안정성 우선) ]
+----------+       +---------------------------+       +----------+
| Ingress  |       |    Switch Fabric/Buffer   |       | Egress   |
|  Port    |======>| [RX: Full Frame]          |======>|  Port    |
+----------+       | [Process: CRC Check]      |       +----------+
                   | [Decision: Valid?]        |
                   +---------------------------+
  (주의: 끝까지 받아야 다음 단계로 진행 가능)
  Latency = Frame Reception Time + Processing Time

[ 2. Cut-through (속도 우선) ]
+----------+       +---------------------------+       +----------+
| Ingress  |       |    Switch Fabric          |       | Egress   |
|  Port    |=====>| [RX: DA(6B)]              |======>|  Port    |
+----------+      | [Decision: Lookup]       |       +----------+
                   | [Action: Stream Forward] |
                   +---------------------------+
  (특징: RX가 끝나기도 전에 TX가 시작됨 - Pipelining)
  Latency = Header Processing Time (Fixed)

[ 3. Fragment-Free (절충) ]
+----------+       +---------------------------+       +----------+
| Ingress  |       |    Switch Fabric/Buffer   |       | Egress   |
|  Port    |======>| [RX: 64 Bytes]            |======>|  Port    |
+----------+       | [Process: Runt Check]     |       +----------+
                   | [Decision: Safe?]         |
                   +---------------------------+
  (특징: 충돌로 인한 파편 프레임(Runt) 필터링이 목적)
```

**3. 심층 동작 원리 및 코드 로직**

*   **Store-and-Forward (저장 후 전송)**:
    가장 오래되고 견고한 방식입니다. 스위치는 목적지 포트(Egress Port)가 혼잡(Congestion) 상태인지 확인하기 위해 전체 프레임을 버퍼링합니다. 또한 FCS(Frame Check Sequence) 필드를 계산하여 **CRC(Cyclic Redundancy Check)** 오류를 검출합니다. 오류가 있으면 프레임을 폐기(Discard)하고, 오류가 없으면 MAC 주소 테이블을 조회하여 전송합니다. 이때 지연 시간은 **프레임 길이(Frame Size) / 포트 속도(Port Speed)**에 비례합니다. 예를 들어 1500바이트 프레임을 1Gbps 포트에서 받으면 약 12µs의 수신 지연이 발생합니다.

*   **Cut-through (컷스루)**:
    스위치가 수신 포트에서 프레임의 **DA(Destination MAC Address)**, 즉 처음 14바이트(Preamble 제외 6바이트)를 수신하는 즉시 **CAM(Content Addressable Memory)** 테이블을 조회하여 포워딩 경로를 결정합니다. 이때 FCS는 수신조차 하지 않습니다. 따라서 송신 측이 아직 프레임 전송을 다 보내기도 전에 수신 측 스위치는 이미 전송을 시작하는 **스트리밍(Streaming)** 형태가 됩니다.
    ```c
    // Pseudo-code: Cut-through Logic
    on_receive_first_14_bytes(frame):
        dest_mac = extract_dest_mac(frame)
        egress_port = mac_table.lookup(dest_mac)
        if egress_port EXISTS:
            start_forwarding(frame) // 즉시 전송 시작 (FCS 확인 없음)
    ```
    이 방식은 전체 프레임을 저장할 버퍼가 거의 필요 없으므로 고성능 스위치에서 선호됩니다.

*   **Fragment-Free (프래그먼트 프리)**:
    이더넷 표준(IEEE 802.3)에 따르면 정상적인 프레임은 최소 64바이트(헤더 18B + 데이터 46B + FCS 4B) 이상이어야 합니다. 충돌(Collision)이 발생하면 64바이트 미만의 조각난 **Runt Frame**이 발생합니다. Fragment-free 방식은 64바이트를 수신할 때까지 잠시 기다렸다가, 64바이트가 넘어가면 "충돌은 없었다"고 판단하고 즉시 포워딩을 시작합니다.

> **📢 섹션 요약 비유**: 
> **물류 센터의 컨베이어 벨트**와 같습니다. **Store-and-Forward**는 물건이 벨트 끝에 도착하여 상자를 완전히 검수팀에게 넘겨 **검수(Inspection)**를 마친 후 트럭에 싣는 것입니다. **Cut-through**는 물건이 벨트 위를 지나가는 순간 **주소 태그(Tag)**만 읽어서 바로 해당 트럭 라인으로 분류기(Diverter)로 던져버리는 고속 처리 방식입니다. **Fragment-Free**는 상자가 벨트에 올라온 직후 **무게 센서(Weight Sensor)**를 통과시켜, 너무 가벼운(깨진) 상자는 걸러내고 정상적인 상자는 바로 보내는 방식입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

세 가지 방식은 상호 배타적이지 않으며, 상황에 따라 **Adaptive(적응형)**으로 동작할 수도 있습니다.

**1. 기술 비교 분석표**

| 비교 항목 (Metric) | Store-and-Forward (저장 후 전송) | Cut-through (컷스루) | Fragment-Free (단편 방지) |
|:---|:---:|:---:|:---:|
| **지연 시간 (Latency)** | **High (높음)** <br> (Frame Size 의존적) | **Low (낮음)** <br> (Fixed 최소) | **Medium (중간)** |
| **에러 검출 (Error Check)** | Full CRC Check (모든 에러 차단) | **None (에러 전파 가능)** | Runt Frame Check (64B 까지만) |
| **스위치 내부 메모리** | Large Buffer Required | Minimal Buffer | Small Buffer (64B) |
| **주요 사용처** | 일반 기업 네트워크, WAN | 데이터 센터, HFT, SAN | 복잡한 LAN 환경 |
| **잘못된 프레임 전송** | 없음 (완벽 차단) | 있음 (Bad Frame도 전달) | 적음 (Runt Frame만 차단) |

**2. 과목 융합 분석 (OS/Arch/Network)**

*   **운영체제(OS)와의 연관**: OS의 I/O 버퍼링 전략과 연결됩니다. Store-and-Forward는 **Standard I/O (Buffered I/O)**와 유사하여 사용자 공간의 데이터 무결성을 보장하지만 오버헤드가 큽니다. Cut-through는 **Direct Memory Access (DMA)**나 Zero-Copy 기법처럼 커널 개입을 최소화하여 빠르게 데이터를 전달하려는 목적과 같습니다.
*   **컴퓨터 구조(Architecture)와의 연관**: CPU 파이프라이닝(Pipelining)과의 유사성이 있습니다. Store-and-Forward는 **Load-Use Hazard**가 발생해 데이터를 기다려야 하는 반면, Cut-through는 **Speculative Execution(예측 실행)**처럼 일단 주소를 보고 실행을 시작하여 성능을 높이지만, 잘못된 정보(에러 프레임)가 들어오면 롤백이 불가능한(전송해버린) 문제가 있습니다.

**3. 실무 성능 지표 (Metrics)**
*   **Cut-through Latency**: 보통 1Gbps 기준 약 4~5µs (바이트 수신 + 룩업).
*   **Store-and-Forward Latency**: 1500Byte 프레임 기준 약 12µs (수신 시간) + 2µs (처리) = 14µs 이상.
*   **HFT(High-Frequency Trading)**에서는 수 µs의 차이가 수십억 원의 승부를 가르기 때문에 **Cut-through** 방식이 거의 표준처럼 사용됩니다.

> **📢 섹션 요약 비유**: 
> **신호등 운영 방식**에 비유할 수 있습니다. **Store-and-Forward**는 신호등 앞에서 모든 차량이 완전히 정차하고 안전을 확인한 후 출발하는 **교통정리** 방식입니다. **Cut-through**는 신호등 없는 **자동차 전용 도로(Autobahn)**에서 운전자의 판단만으로 전속력으로 달리는 방식으로, 사고(에러) 위험은 있지만 이동 속도는 최상입니다. **Fragment-Free**는 신호등에 **카메라**를 설치하여 명백한 위반 차량만 걸러내고 나�