+++
title = "UCIe (Universal Chiplet Interconnect Express)"
date = "2026-03-14"
weight = 443
+++

# UCIe (Universal Chiplet Interconnect Express)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: UCIe (Universal Chiplet Interconnect Express)는 서로 다른 제조사, 공정, 아키텍처를 가진 반도체 다이(Die)들을 패키지(Package) 내에서 유기적으로 연결하기 위한 **개방형 표준 인터커넥트(Open Standard Interconnect)** 규격이다.
> 2. **가치**: 단일 Monolithic Die(단일 다이) 방식의 수율 저하(Yield Drop) 및 비용 상승 문제를 극복하여, '칩렛(Chiplet) 경제성'을 실현하고 설계 유연성을 극대화하며 시장 출시 기간(Time-to-Market)을 단축한다.
> 3. **융합**: 고대역폭 메모리(HBM)와 같은 2.5D/3D 패키징 기술 및 CXL(Compute Express Link) 프로토콜과 융합하여 '시스템 온 패키지(System-on-Package, SoP)' 패러다임의 표준 인터페이스로 자리 잡는다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 기술적 배경 및 정의
반도체 미세 공정이 3nm, 2nm 수준으로 나아감에 따라 단일 실리콘 웨이퍼(Silicon Wafer) 내에 집적하는 트랜지스터의 수는 천억 개를 넘어섰다. 그러나 다이(Die) 면적이 레티클 한계(Reticle Limit, 약 800mm²)에 근접함에 따라, 단일 칩 제조 시 수율(Yield)이 기하급수적으로 하락하고 광학 노광 공정의 난이도가 상승하는 물리적·경제적 한계에 직면했다. 이를 해결하기 위해 하나의 큰 칩을 기능별로 분리하여 제작한 후 패키지 내에서 결합하는 '칩렛(Chiplet)' 기술이 대두되었으나, 업체별로 상이한 인터페이스로 인해 호환성이 보장되지 않았다. 이에 인텔(Intel), AMD, ARM, TSMC, 삼성전자 등 반도체 산업 생태계 전반이 참여하여 만든 표준이 바로 UCIe이다.

#### 2. 기술적 필요성
- **비용 효율성**: 로직(Logic) 소자는 최신 미세 공정(예: 3nm)을 사용하고, 아날로그/RF/I/O 소자는 저비용의 성숙된 공정(예: 14nm/28nm)을 사용하여 공정별 최적화(Cost-Optimized)를 달성한다.
- **설계 재사용**: 한 번 설계하고 검증된 칩렛을 다른 제품군에도 재사용(Reuse)하여 설계 비용(NRE: Non-Recurring Engineering)을 절감한다.
- **성능 극복**: 온칩(On-chip) 버스에 준하는 초고대역폭과 초저지연(Low Latency) 통신을 패키지 수준에서 구현한다.

💡 **비유**: 레고 블록 조립과 같습니다. 서로 다른 모양과 색깔(기능과 공정)의 블록들을 끼워 맞춰 하나의 완성품을 만들려면, 모든 블록의 결합 돌기 인터페이스가 표준화되어 있어야 합니다. UCIe는 바로 그 '만능 연결 돌기' 역할을 합니다.

#### 3. 진화 흐름 (ASCII Diagram)
단일 칩 설계의 한계를 극복하기 위한 패키징 기술의 진화 과정은 다음과 같다.

```
+----------------------+      +-----------------------+      +-----------------------+
| [ SoC Era ]           |      | [ Multi-Chip Module ] |      | [ Chiplet Era (UCIe) ]|
| Monolithic Die        |      | 2.5D Package          |      | Disaggregated Die     |
+----------------------+      +-----------------------+      +-----------------------+
| +------------------+  |      | +----+  +----+        |      | +----+  +----+  +----+ |
| | Logic / Mem / I/O|  |      | |Die1|->|Die2| (Prop.)|      | |CPU |->|Mem |->|I/O | |
| | (Single Process) |  |      | +----+  +----+  Link  |      | |Std|  |Std|  |Std | |
| +------------------+  |      | (Wide Bus / Limited) |      | +----+  +----+  +----+ |
| * Reticle Limit    |  |      | * Silicon Interposer |      | * Standard Interface |
| * Low Yield (Big)  |  |      | * High Cost          |      | * Eco System / Flex  |
+----------------------+      +-----------------------+      +-----------------------+
```
*Prop.: Proprietary (사설 규격), Std.: Standard (표준 규격)*

**[다이어그램 해설]**
기존 SoC(System on Chip) 방식은 하나의 다이에 모든 것을 통합하여 크기가 커질수록 수율이 급격히 떨어지는 문제가 있었다. 이를 해결하기 위해 2.5D 패키징이 등장했으나, 당시에는 각 제조사마다 독자적인 연결 방식을 사용하여 호환이 불가능했다. UCIe는 이러한 칩렛 간 연결을 USB와 같은 표준으로 정의하여, 누구나 만든 칩렛을 조립하여 사용할 수 있는 생태계를 구축한다.

📢 **섹션 요약 비유**: 서로 다른 전자제품들을 USB 포트라는 표준으로 연결하여 PC를 확장하듯, 반도체 설계에도 '범용 연결 포트'를 도입하여 필요한 부품만 꽂아 사용하는 '반도체 모듈화 시대'를 여는 열쇠입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

UCIe 표준은 OSI 7계층 모델과 유사하게 계층적(Layered) 아키텍처를 따르며, 크게 **PHY (Physical Layer)**, **D2D (Die-to-Die Adapter)**, **Protocol Layer**의 세 계층과 이를 지원하는 부가 기능으로 구성된다.

#### 1. 주요 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 특이사항 (Internal Operations) | 프로토콜/표준 | 비유 (Analogy) |
|:---:|:---|:---|:---:|:---|
| **PHY (Physical Layer)** | 물리적 신호 전송 및 수신 | - **전송 매체**: Standard(Standard Package)와 Advanced(Interposer/Bridge) 모드 지원<br>- **데이터 레이트**: 20~40 Gbps/lane 이상 지원<br>- **회로**: Lin(Linear) 드라이버와 고감도 수신기 사용 | UCIe PHY Spec | 전기 신호가 흐르는 구리선 |
| **D2D Adapter** | Die 간 데이터 포맷 변환 및 흐름 제어 | - **프로토콜 변환**: Flit(Flow Control Unit) 단위 변환<br>- **CRC/ECC**: 데이터 무결성 검사 및 오류 정정<br>- **Link 파라미터 협상**: 폭, 속도, Lane 구성 협상 | UCIe D2D Spec | 통신 언어 변환기/번역기 |
| **Protocol Layer** | 상위 계층 프로토콜 처리 | - **지원 프로토콜**: PCIe (Peripheral Component Interconnect Express), CXL (Compute Express Link), RAW(Streaming)<br>- **Flit 기반 전송**: 고정 길이 패킷 단위로 처리하여 헤더 오버헤드 최소화 | PCIe/CXL | 사용자가 보내는 데이터 패킷 |
| **Sideband Signals** | 제어 및 상태 모니터링 | - **JTAG (Joint Test Action Group)** 기반 디버깅<br>- **전력 관리**: 상대방 Die의 전력 상태 확인 및 웨이크업 신호 | MIPI I3C | 데이터 옆에 있는 관리용 전화선 |
| **Clocking** | 동기화 | - **가변 클럭**: Forwarded Clock 및 Common Clock 모드 지원을 통한 유연한 동기화 | IEEE 1596 | 모든 움직임을 맞추는 초침 |

#### 2. UCIe 계층별 데이터 흐름 및 구조 (ASCII Diagram)
UCIe는 기존 PCIe/CXL 프로토콜을 그대로 사용할 수 있도록 설계되어 있어, 소프트웨어 스택의 변경 없이 하드웨어 물리 계층만 교체하여 성능을 끌어올릴 수 있다.

```
+--------------------------------------------------------------------------+
| [ Die A : Complex SoC ]                                       [ Die B ]   |
|                                                                          |
| +---------------------------+        +---------------------+             |
| |  Protocol Layer           |        | Protocol Layer     |             |
| | (PCIe / CXL / Streaming)  | <----> | (PCIe / CXL / Raw) |             |
| |  Transaction Layer (TLX)  |        |                     |             |
| +---------------------------+        +---------------------+             |
|          |  TLP/FLIT                         ^  |                         |
|          v                                   |  v                         |
| +---------------------------+        +---------------------+             |
| |  D2D Adapter              |        | D2D Adapter        |             |
| | (CRC, Retry, Credit Ctrl)| <----> | (Virtual Channel)  |             |
| |  - Link Training          |        |  - Link Equalization|             |
| +---------------------------+        +---------------------+             |
|          |  Raw Data / Symbol             |  |                         |
|          v                                |  v                         |
| +---------------------------+        +---------------------+             |
| |  PHY (Physical)           | <----> | PHY (Physical)      |             |
| |  - Lane 0~N (Diff. Pair)  |        |  - Lane 0~N         |             |
| |  - 128b/132b Encoding     |        |                     |             |
| +---------------------------+        +---------------------+             |
|          |________________[ Advanced Package Tech ]_________|            |
|          (Organic Substrate or Silicon Interposer)                      |
+--------------------------------------------------------------------------+
```

**[다이어그램 해설]**
1. **Protocol 계층**: 기존 x86 CPU나 GPU에서 사용하던 PCIe나 CXL 프로토콜 스택을 변경 없이 사용할 수 있어 호환성이 극대화된다. 이는 기존 소프트웨어 에코시스템을 그대로 계승할 수 있음을 의미한다.
2. **D2D Adapter**: 다이 간의 신뢰성 있는 전송을 위해 64비트 또는 256비트 단위의 Flit으로 데이터를 쪼개고, CRC(Cyclic Redundancy Check) 오류 검출 코드를 붙인다. 또한, 크레딧(Credit) 기반 흐름 제어를 통해 수신측 버퍼 오버플로우를 방지한다.
3. **PHY 계층**: 패키지의 종류에 따라 유기적 기판(Organic Substrate) 위에 직접 실장되는 Standard 모드와 실리콘 인터포저(Silicon Interposer)를 통하는 Advanced 모드로 나뉜다. Advanced 모드에서는 좁은 피치(Fine Pitch)의 미세 범프(Micro-bump)를 사용해 전송 속도와 대역폭을 비약적으로 높인다.

#### 3. 핵심 알고리즘 및 동작 메커니즘 (Credit-Based Flow Control)
UCIe는 플릿(Flit) 기반의 크레딧 기반 흐름 제어(Credit-Based Flow Control)를 사용한다.

```c
// [Pseudo-code: Credit-Based Flow Control in D2D Adapter]
// 송신측(Sender) 로직
void send_flit(Flit* data) {
    while (tx_credits[target_vc] == 0) {
        wait_for_credit_update(); // 수신측 버퍼에 공간이 생길 때까지 대기
    }
    tx_credits[target_vc]--;      // 크레딧 소진
    transmit_phy(data);           // 물리 계층으로 전송
}

// 수신측(Receiver) 로직
void receive_flit(Flit* data) {
    buffer_push(data);            // 버퍼에 저장
    update_rx_credits();          // 송신측으로 Credit 반환 신호 전송
}
```
위 메커니즘을 통해 패키지 내부라 할지라도 네트워크 상의 패킷 손실이나 오버플로우 없는 **신뢰성 있는 전송(Reliable Transport)**을 보장한다. 또한, **Lane Reversal** 기능을 포함하여 칩을 거꾸로 실장하더라도 신호선을 자동으로 매핑하여 조립 불량을 방지한다.

📢 **섹션 요약 비유**: 건물의 각 층(프로토콜)이 사용하는 언어가 다르더라도, 그 사이에 **동시통역기(D2D Adapter)**와 **고속 화물 엘리베이터(PHY)**가 설치되어 있어, 마치 한 건물 안에서 원활하게 업무가 처리되는 것과 같은 구조입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

UCIe는 기존의 칩 간 연결 기술인 PCIe, NVLink, SerDes 기술과 물리적 위치와 목적에서 명확히 구분된다.

#### 1. 심층 기술 비교 분석표

| 비교 항목 | On-Chip Bus (내부 버스) | On-Board (PCIe Gen5/x16) | UCIe (Advanced Package) |
|:---:|:---:|:---:|:---:|
| **물리적 거리** | < 20 mm | ~ 10 cm | < 2 mm (Interposer) |
| **대역폭 (Bandwidth)** | 1 ~ 10 TB/s | ~ 64 GB/s | 1 ~ 2 TB/s (초기) |
| **전력 효율 (pJ/bit)** | 0.1 ~ 0.5 | 10 ~ 20 (High) | < 0.5 (Low) |
| **지연 시간 (Latency)** | < 5 ns | 50 ~ 100 ns | 5 ~ 10 ns |
| **연결 대상** | Cores on Same Die | GPU/CPU on Motherboard | Logic Die + Memory/AI Die |
| **확장성** | 불가능 (Fixed) | 모듈 교체 가능 | 칩렛 교체 및 확장 용이 |

#### 2. 과목 융합 관점 분석
**[A. 반도체 공정 및 패키징 (Process & Packaging)]**
UCIe는 TSMC의 **SoIC (System on Integrated Chips)**, 삼성의 **X-Cube**, 인텔의 **Foveros**와 같은 3D 적층 기술의 데이터 고속도로 역할을 한다. 하이브리드 본딩(Hybrid Bonding) 기술과 결합할 경우, 범프(Bump) 없이 구리(Cu) 대 구리 직접 접합을 통해 UCIe의 PHY 계층을 더욱 얇고 빠르게 구현할 수 있다.

**[B. 시스템 아키텍처 및 메모리 (System Arch & Memory)]**
CPU와 고대역폭 메모리(HBM) 사이의 병목을 해소한다. 기존에는 DRAM 컨트롤러가 CPU 다이 내부에 위치해야 했으나, UCIe를 통해 메모리 칩렛을 CPU 다이 옆에 붙이는 **메모리 디스아그리거이션(Memory Disaggregation)**이 가능해져