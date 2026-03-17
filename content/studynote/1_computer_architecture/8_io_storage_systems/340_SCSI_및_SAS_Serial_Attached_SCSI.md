+++
title = "340. SCSI 및 SAS (Serial Attached SCSI)"
date = "2026-03-14"
weight = 340
+++

# # [340. SCSI 및 SAS (Serial Attached SCSI)]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: SCSI (Small Computer System Interface)는 컴퓨터와 주변기기 간의 통신을 위한 표준 프로토콜 세트이며, SAS (Serial Attached SCSI)는 이를 병렬(Parallel) 전송 방식에서 직렬(Serial) 점대점(Point-to-Point) 방식으로 진화시켜 신뢰성과 속도를 극대화한 엔터프라이즈 스토리지 인터페이스입니다.
> 2. **가치**: 전이중(Full-Duplex) 통신, 이중 포트(Dual-Port) 지원, 그리고 강력한 명령어 큐(Queue) 처리를 통해 99.999%의 가용성을 요구하는 데이터 센터와 SAN (Storage Area Network) 환경에서 단일 장애점(SPOF)을 제거하는 핵심 역할을 수행합니다.
> 3. **융합**: SATA (Serial ATA)와의 물리적/전기적 호환성을 유지하며 비용 효율성을 확보하는 동시에, OSI 7계층 중 물리 계층(Physical Layer)과 데이터 링크 계층(Data Link Layer)의 기술적 집약체로서 향후 NVMe (Non-Volatile Memory express) 기반의 PCIe (Peripheral Component Interconnect Express) 패브릭과 공존할 하이브리드 스토리지 아키텍처의 기반을 이룹니다.

---

### Ⅰ. 개요 (Context & Background)

SCSI는 단순한 하드디스크 연결케이블을 넘어, 호스트(Host)와 장치(Device) 간의 지능적인 데이터 교환을 위한 **프로토콜(Protocol)**과 **물리적 규격(Physical Spec)**을 모두 아우르는 개념입니다. 초기에는 병렬(Parallel) 버스 방식을 사용하여 넓은 대역폭을 확보했으나, 신호 skew(신호 도착 시간 차)와 crosstalk(혼선) 문제로 인해 클럭 속도를 높이는 데 물리적 한계가 있었습니다. 이를 돌파하기 위해 등장한 SAS는 기존의 병렬 버스를 포기하고 고속 직렬(Serial) 통신 방식을 차용하되, SCSI의 강력한 명령어 세트는 그대로 계승했습니다.

**💡 비유**: 병렬 버스가 '8차선 도로를 달리는 자동차 행렬'이라면, 직렬 방식은 '고속철도 전용 선로를 달리는 열차'와 같습니다. 차선이 넓다고 무조건 빠른 것이 아니며, 신호 체계(직렬)가 개선되어야 정시 도착률(신뢰성)과 속도를 모두 잡을 수 있습니다.

**등장 배경**:
1.  **기존 한계**: 병렬 SCSI는 케이블이 두껍고 커넥터가 커서 랙(Rack) 내부의 공간 효율이 낮았으며, Daisy Chain(데이지 체인) 방식으로 인해 하나의 장치 장애가 전체 버스를 멈추게 하는 위험이 있었습니다.
2.  **혁신적 패러다임**: SATA(Serial ATA)의 등장으로 확인된 직렬 통신의 우수성(신뢰성, 케이블 길이 확보, 핫 플러그 지원)을 SCSI 명령어 세트와 결합하여 **SAS**라는 신개념이 탄생했습니다.
3.  **현재의 비즈니스 요구**: 클라우드와 빅데이터 시대로 접어들며, 대용량 처리뿐만 아니라 무중단 서비스를 위한 **이중화(Redundancy)**와 **원격 관리**가 필수적이 되었고, 이를 만족시키는 것이 SAS입니다.

📢 **섹션 요약 비유**: 병렬 SCSI가 복잡하고 헝클어진 전화선 묶음을 통해 구슬을 전달하던 구식 방식이었다면, SAS는 광케이블 수준의 정교함으로 데이터를 쏘아 보내는, 수천 개의 우편물을 실수 없이 분류하는 첨단 물류 터미널과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

SAS의 아키텍처는 물리적 계층(Phy), 링크 계층(Link), Transport 계층, 그리고 애플리케이션 계층(Application)으로 나뉘는 계층 구조를 가집니다. 가장 핵심은 물리적 포트가 **2개(Dual Port)**라는 점과, 네트워크 스위치처럼 동작하는 **Expander**가 있다는 점입니다.

#### 1. 구성 요소 (표)
| 요소명 | 역할 | 내부 동작 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Initiator (초기자)** | 데이터 전송을 시작하는 호스트(HBA) | SCSI CDB (Command Descriptor Block) 전송 | 물건을 주문하는 고객 |
| **Target (타겟)** | 요청을 받아 처리하는 디스크 장치 | FIS (Frame Information Structure) 처리 | 주문을 받아 물건을 포장하는 창고 |
| **SAS Expander (확장기)** | 포트 수를 확장하고 경로를 설정(Switching) | STP (SATA Tunneling Protocol), SSP 지원 | 전화망의 교환기 (Switch) |
| **Phy (Physical Layer)** | 물리적 신호를 복조/변조 및 8b/10b 인코딩 | OOB (Out-of-Band) 신호로 속도 협상 | 전파를 송수신하는 안테나 |
| **Port (포트)** | 물리적 연결 단위 (Phy x 1 or x 4) | Wide Port (Phy x 4 Narrow Port 묶음) | 다차선 진입로 |

#### 2. SAS 아키텍처 토폴로지
아래 다이어그램은 하나의 Initiator가 Expander를 통해 여러 대의 디스크와 SATP(SATA Tunneling Protocol)를 통해 SATA 디스크까지 제어하는 구조를 보여줍니다.

```text
   [Host Server]
      |  |
   (HBA Card)
   |         | (Dual Path/Redundancy)
   v         v
+----------------+       +-----------------------+
| Initiator      |------>|  SAS Expander         |-----> [SAS Disk 1] (Target)
| (Port 0, Port1)|       |  (Wide Port 4x Phy)   |-----> [SAS Disk 2] (Target)
+----------------+       +-----------------------+      |
   ^   ^    ^                       |                |
   |   |    |                       | (STP)          v
   |   |    +-----------------------+-----------> [SATA Disk] (STP Target)
   |   |            (Connection)
   |   +-----------------------------------------> [Tape Drive]
   |
   +---> (Secondary Path for Failover)
```
*   **해설**:
    1.  **Point-to-Point**: SCSI와 달리 SAS는 1:1 직접 연결입니다. bandwidth를 다른 장치와 나눠 쓰지 않아 전이중(Full-Duplex) 통신이 가능합니다.
    2.  **Multipathing (다중 경로)**: 위 그림의 `Secondary Path`와 같이, 한 개의 디스크에 두 개의 케이블을 연결하여 Active-Standby 또는 Active-Active 구성을 만들 수 있습니다.
    3.  **STP (SATA Tunneling Protocol)**: SAS 컨트롤러가 SATA 명령어를 SAS 프레임에 담아 쏘아 줌으로써, SAS 백플레인에 저렴한 SATA 디스크를 혼용해서 장착할 수 있게 해줍니다.

#### 3. 심층 동작 원리: Connection & Flow Control
SAS는 **Connection-Oriented** 프로토콜입니다. 데이터 전송 전에 반드시 논리적 연결(Connection)을 맺어야 합니다.
1.  **OPEN 요청**: Initiator가 Target으로 "OPEN_ORIGIN" 프레임을 보냅니다.
2.  **승인**: Target이 "OPEN_ACCEPT"로 응답하면 연결이 성립됩니다.
3.  **데이터 전송**: SSD/HDD에서 데이터를 읽어 보냅니다.
4.  **종료**: 전송이 끝나면 연결을 해제(CLOSE)하여 다른 장치가 버스를 사용할 수 있게 합니다.
이 과정은 스토리지 대기열(Queue) 깊이가 깊을 때(예: NCQ, Native Command Queuing) 효율적인 순서 재배열(Reordering)을 가능하게 하여 랜덤 I/O 성능을 극대화합니다.

📢 **섹션 요약 비유**: SAS 도로망은 진입 전에 미리 톨게이트(Handshake)를 통과하고 배정된 차로를 달리는 고속도로 시스템입니다. 중간에 교차로(Expander)에서 경로를 재조정해도 목적지까지 혼잡 없이 도달할 수 있으며, 2층 교량(Dual Port)이 있어 아래층 도로가 막혀도 위층 도로로 우회할 수 있는 완벽한 교통 체계입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

SAS를 이해하기 위해서는 SATA와의 기술적 차이를 명확히 인지하고, PCI Express 기반의 NVMe와의 관계를 이해해야 합니다.

#### 1. 심층 기술 비교 (SAS vs SATA)
비교 항목은 물리적 커넥터 핀 호환성을 고려하여 SATA의 단순성을 SAS의 강력함을 대조합니다.

| 비교 항목 | SAS (Serial Attached SCSI) | SATA (Serial ATA) | 분석 및 의사결정 기준 |
|:---|:---|:---|:---|
| **신호 전압** | 차동 신호 (Differential), 고전압 | 낮은 전압, 단순 화로 | SAS가 전자기적 잡음(EMI)에 강해 랙 밀집 환경에서 안정적 |
| **포트 구조** | **Dual-Port (2개 포트)** 지원 | Single-Port (1개 포트) | SAS는 HBA 이중화 가능 → **High Availability (HA) 필수** |
| **통신 방식** | **Full-Duplex** (동시 송수신) | Half-Duplex (송수신 분리) | 지속적인 R/W가 발생하는 DB 서버는 SAS가 유리 |
| **프로토콜** | SCSI Command Set (TCP/IP 같은 복잡함) | ATA Command Set (단순함) | SAS는 우선순위 제어, 에러 복구 명령어가 풍부함 |
| **케이블 길이** | 최대 8m~10m (Expander 포함) | 최대 1m~2m | 센터 간 연결이나 복잡한 랙 배선 시 SAS가 유리 |
| **비용** | 상대적으로 매우 높음 | 매우 낮음 (소비자용) | **TCO(총소유비용)**와 가용성 간의 트레이드오프 필요 |

#### 2. 과목 융합 관점 (OS & 네트워크)
-   **운영체제(OS)와의 연계**: OS는 SAS 드라이브를 블록 디바이스(`/dev/sd*` 등)로 인식합니다. SAS의 **TCQ (Tagged Command Queuing)** 기능은 OS 커널의 I/O 스케줄러(CFQ, Deadline 등)와 시너지를 일으켜, 랜덤 I/O 환경에서 헤드(HHead)의 이동 거리를 최소화하여 성능을 30% 이상 향상시킵니다.
-   **네트워크(Network)와의 유사성**: SAS Expander는 네트워크의 **L2 스위치**와 동일한 역할을 합니다. SAS 주소(SAS Address)는 MAC 주소처럼 고유하며, Expander는 이 SAS 주소를 기반으로 프레임을 라우팅(Routing)합니다. 즉, 스토리지 네트워크가 곧 LAN(Local Area Network)의 구조를 띠는 셈입니다.
-   **NVMe와의 관계**: NVMe는 CPU가 직접 SSD를 제어하는 방식이므로 SCSI의 오버헤드(Overhead)가 없습니다. 따라서 초저지연(Low Latency)이 필요한 영역에서는 SAS가 NVMe에게 자리를 내어주고, **NL-SAS (Nearline SAS)**라 불리는 대용량 고밀도 HDD 영역에서 여전히 강세를 보입니다.

📢 **섹션 요약 비유**: SATA가 '나홀로 운전하는 일반 승용차'라면, SAS는 '교통 정보(TCQ)를 실시간 공유받고 사이렌을 울리며 긴급 출동하는 구급차'와 같습니다. NVMe는 이 도로 위를 날아다니는 '헬리콥터'라고 할 수 있죠. 헬리콥터가 등장했지만, 구급차가 필요한 상황(대량 수송, 안정성)은 여전히 존재합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

엔터프라이즈 환경에서 SAS 단순한 기술 선택이 아니라 '비즈니스 지속성(BCP)'을 위한 필수 요소입니다.

#### 1. 실무 시나리오 및 의사결정
**[시나리오: 대형 은행의 핵심 DB 서버 구축]**
-   **문제 상황**: 24시간 365일 결제 시스템이 중단되면 안 됨. 예산은 넉넉하나 장애 발생 시 RTO (Recovery Time Objective)는 0에 수렴해야 함.
-   **기술적 판단**:
    1.  **SAS 12Gb/s Dual-Port HBA** 채택: OS 장애 차단을 위해 Multipathing 드라이버 설치.
    2.  **RAID 10 (1+0) 구성**: SAS의 성능을 100% 활용하되 쓰기 성능 저하를 방지.
    3.  **Expander 비용 vs. Port 밀도**: 16개 포트가 필요할 때, Expander 방식 JBOD(Just a Bunch Of Disks)를 쓸지 HBA 포트를 늘릴지 선택. Expander는 지연(Latency)을 유발할 수 있으므로, 초고속 트랜잭션 처리 시스템에서는 Expander 없이 HBA 직결을 선호하는 경향이 있음.
-   **결과**: 하나의 케이블이 탈락되어도 다른 경로로 트래픽이 자동 분산되며, 5년 이상 무중단 가동 가능.

#### 2. 도입 체크리스트 (Checklist)
구분 | 체크항목 | 설명
:---|:---|:---|
**기술적**| **가용성 요구사항**| 99.99% 이상의 가용성이 필요하면 SAS 필수. (SATA는 포트 단일 장애로 전체 디스크 끊김)
| **I/O 패턴** | 랜덤 읽기/쓰기가 빈번한 데이터베이스 환경인가? → SAS의 Command Queue 효율 극대화
| **지연 시간** | 1