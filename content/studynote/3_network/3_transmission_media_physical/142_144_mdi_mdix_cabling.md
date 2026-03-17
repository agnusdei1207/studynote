+++
title = "142-144. 이더넷 케이블 배선과 MDI/MDI-X"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 142
+++

# 142-144. 이더넷 케이블 배선과 MDI/MDI-X

> **1. 본질**: 이더넷(Ethernet) 물리 계층에서 신호의 송수신(Tx/Rx) 회로를 물리적으로 또는 논리적으로 매칭시켜 통신을 성립시키는 배선 기술과 인터페이스 표준이다.
> **2. 가치**: 장비 간 핀(Pin) 배열 호환성을 해결하여 물리적 연결성을 보장하며, Auto-MDIX 기술을 통해 운영 효율을 극대화하고 설치 비용을 절감한다.
> **3. 융합**: OSI 7계층 중 물리 계층(Layer 1)의 전기적 신호 전송 원리와 데이터 링크 계층(Layer 2)의 MAC(Medium Access Control) 주소 통신 간의 물리적 매개체 역할을 수행한다.

---

### Ⅰ. 개요 (Context & Background)

이더넷(Ethernet)은 IEEE 802.3 표준에 기반하여 가장 널리 사용되는 유선 LAN(Local Area Network) 기술이다. 초기 이더넷 환경에서는 두 장비를 연결할 때, 각 장비의 포트 핀 배치가 송신(Tx)인지 수신(Rx)인지에 따라 케이블을 물리적으로 다르게 제작해야 했다. 이는 **MDI (Medium Dependent Interface)**와 **MDI-X (Medium Dependent Interface-Crossover)**라는 상호 보완적인 포트 표준과 UTP(Unshielded Twisted Pair) 케이블의 배선 방식(T568A/T568B)에 대한 이해를 전제로 한다.

과거 네트워크 관리자는 PC와 스위치 같은 '이종 장비' 연결 시엔 다이렉트 케이블을, PC와 PC 혹은 스위치와 스위치 같은 '동종 장비' 연결 시엔 크로스오버 케이블을 사용해야 했다. 이러한 물리적 제약은 네트워크 확장 시 혼란을 가중시켰으나, **Auto-MDIX (Automatic Medium-Dependent Interface Crossover)** 기술의 등장으로 소프트웨어적 자동 감지 및 스위칭이 가능해지며 하드웨어적 복잡도가 대폭 감소했다.

```ascii
[이더넷 연결 방식의 진화 과정]
┌──────────────────────┐     ┌───────────────────────┐     ┌─────────────────────────┐
│     수동 배선 시대      │  →  │   Auto-MDIX 도입 시대    │  →  │    Universal 통신 시대    │
├──────────────────────┤     ├───────────────────────┤     ├─────────────────────────┤
│ • Direct / Cross      │     │ • 논리적 핀 매핑         │     │ • PHY Chip 자동 협상      │
│ • 케이블 물리적 구분    │     │ • 케이블 종류 무관       │     │ • Plug & Play           │
│ • 관리자 주의 필요     │     │ • 설치 효율성 증대       │     │ • 자동 복구 및 유지보수   │
└──────────────────────┘     └───────────────────────┘     └─────────────────────────┘
```
*도입 1*: 이 그림은 케이블 배선 기술이 물리적 제약에서 논리적 자유로 진화해온 과정을 보여줍니다.
*도입 2*: 초기에는 장비의 종류에 따라 다른 케이블이 강제되었으나, 기술 발전에 따라 장비가 스스로 선을 바꿔 연결하는 지능화된 단계로 넘어왔음을 시각화했습니다.

**💡 비유**
자동차로 비유하자면, 초보 운전자는 운전석과 조수석의 위치가 국가마다 다를 경우(영국 vs 한국) 핸들을 바꿔야 하는 스트레스(크로스오버)를 겪었지만, 요즘자동차처럼 운전석이 스스로 좌우로 이동하여 어느 나라 도로에든 맞춰지는 **'오토 드라이빙 시스템'(Auto-MDIX)**이 탑재된 셈입니다.

**등장 배경**
① **물리적 한계**: 10BASE-T/100BASE-TX 시절 두 쌍의 선(1,2/3,6)만을 사용하여 전이중(Full-Duplex) 통신을 하려면 송신선과 수신선이 교차 접속되어야 했다.
② **혁신적 패러다임**: PHY(Physical Layer) 칩의 로직이 발전하며, 전기적 신호를 감지하여 내부 회로를 소프트웨어적으로 제어(Swapping)하는 기술이 개발되었다.
③ **현재 요구**: 클라우드 및 데이터센터 환경에서는 수천 개의 포트를 연결해야 하므로, 케이블 타입을 고민할 필요 없는 자동화 기능이 필수적이다.

**📢 섹션 요약 비유**
마치 일반 전화기와 팩스기를 연결할 때, 전화선의 규격이 서로 다르면 중간에 잭 변환기를 꽂아야 하는 번거로움이 있었으나, 요즘은 '스마트 허브'가 연결된 기기를 자동으로 인식하여 선을 알아서 바꿔주는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이더넷 케이블링의 핵심은 **TIA/EIA-568** 표준에 정의된 핀 배열과 송수신 쌍의 매칭이다. UTP 케이블 내부의 8개 구리선(Twisted Pair)은 각각의 색상과 목적을 가지며, 이를 어떻게 배열하느냐에 따라 다이렉트(Straight-through)와 크로스오버(Crossover)로 나뉜다. 특히 10Mbps/100Mbps 속도에서는 **1, 2번 핀(송신)**과 **3, 6번 핀(수신)**만 사용되므로 이 두 쌍의 연결이 핵심이다. (Gigabit 이상에서는 4쌍 모두 활용)

#### 1. 구성 요소 상세 분석

| 요소명 (Component) | 전체 명칭 (Full Name) | 역할 (Role) | 내부 동작 (Internal Behavior) | 비고/비유 |
|:---|:---|:---|:---|:---|
| **T568B** | EIA/TIA-568B | 일반적인 배선 표준 | 백색-주황, 주황(1,2 Tx) / 백색-녹색, 파랑(3,6 Rx) 배치 | 한국/미국 주력 표준 |
| **T568A** | EIA/TIA-568A | 대체 배선 표준 | 백색-녹색, 녹색(1,2) / 백색-주황, 파랑(3,6) 배치 | 구형 장비/정부 시설 일부 사용 |
| **MDI** | Medium Dependent Interface | 단말기 포트 타입 | 1,2번을 송신(Tx), 3,6번을 수신(Rx)로 사용 | PC, Router, Server (DTE) |
| **MDI-X** | Medium Dependent Interface-X | 허브/스위치 포트 타입 | 내부 회로가 교차되어 1,2번이 Rx, 3,6번이 Tx | Switch, Hub (DCE) |
| **Auto-MDIX** | Automatic MDI-X | 자동 감지 및 전환 | PHY 칩이 Link Pulse를 감지해 Tx/Rx 논리적 스왑 | Gigabit 급 이상 지원 |

#### 2. 핀 배열 다이어그램 및 배선 구조

아래 다이어그램은 RJ-45 커넥터의 단면도이며, 8개의 핀 위치를 나타낸다.

```ascii
    [ RJ-45 Connector (View from top with clip down) ]
    -------------------------------------
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
    -------------------------------------
      ^   ^   ^           ^   ^
      |   |   |           |   |
    Tx+ Tx- Rx+         Rx- (Unused in 10/100M)
    (Orange) (Green)        (Brown/Blue)

    T568B Color Code (End 1 vs End 2)
    -----------------------------------------
    Pin | Function  | Direct (End2) | Crossover (End2)
    -----------------------------------------
     1  | Tx+ (W-O) | Tx+ (W-O)     | -> Rx+ (W-G)
     2  | Tx- (O)   | Tx- (O)       | -> Rx- (G)
     3  | Rx+ (W-G) | Rx+ (W-G)     | -> Tx+ (W-O)
     4  | (Bi-Direct)|              |
     5  | (Bi-Direct)|              |
     6  | Rx- (G)   | Rx- (G)       | -> Tx- (O)
     7  | (Bi-Direct)|              |
     8  | (Bi-Direct)|              |
```
*다이어그램 해설*:
1.  **기능(Function)**: 1, 2번 핀은 데이터를 보내는 송신선(Tx), 3, 6번 핀은 데이터를 받는 수신선(Rx)입니다.
2.  **Direct (다이렉트)**: 양쪽 끝의 핀 배치가 완전히 동일합니다(T568B - T568B). 이는 서로 다른 타입의 포트(MDI ↔ MDI-X)를 연결할 때 사용합니다. 상대방이 내부적으로 선을 바꿔주기 때문입니다.
3.  **Crossover (크로스오버)**: 한쪽 끝의 1, 2번(Tx)이 반대편 3, 6번(Rx)에 연결되도록 배치합니다(T568B - T568A). 이는 동일한 타입의 포트(MDI ↔ MDI)를 연결할 때 사용합니다.

#### 3. 심층 동작 원리: 다이렉트 vs 크로스오버

이더넷은 **DTE (Data Terminal Equipment)**와 **DCE (Data Communication Equipment)** 간의 통신이다.
*   **DTE (PC, Router)**: 데이터를 생성하는 주체로, **MDI** 포트를 가진다. 1,2번으로 말하고(Tx), 3,6번으로 듣는다(Rx).
*   **DCE (Switch, Hub)**: 데이터를 중계하는 장비로, **MDI-X** 포트를 가진다. DTE의 말을 듣기 위해 1,2번을 귀(Rx)로, 3,6번을 입(Tx)로 설정한다.

**① 다이렉트 케이블 매커니즘 (DTE ↔ DCE)**
PC(MDI)의 송신(1,2) 선이 그대로 Switch(MDI-X)의 수신(1,2) 핀에 연결된다. 스위치 내부의 회로(MDI-X)가 이미 입력을 위한 배선으로 되어 있으므로 케이블은 직선이어야 한다.

**② 크로스오버 케이블 매커니즘 (DTE ↔ DTE)**
PC(MDI)와 PC(MDI)를 연결한다고 가정하자. 둘 다 1,2번으로 밖에 소리를 지르고 있으므로 직선으로 연결하면 '충돌(Collision)'이 발생한다. 따라서 케이블 단계에서 PC A의 1,2(Tx)를 PC B의 3,6(Rx)으로 강제로 연결해야 통신이 가능하다.

```ascii
[신호 흐름 비교: 다이렉트 vs 크로스오버]

CASE 1: PC (MDI) ---[Direct]--- Switch (MDI-X)
PC Tx(1) ------> Switch Rx(1)  (Signal Received OK)
PC Rx(3) <------ Switch Tx(3)  (Signal Received OK)

CASE 2: PC (MDI) ---[Crossover]--- PC (MDI)
PC_A Tx(1) --\   /-- PC_B Rx(3) (Cable Swap handles this)
PC_A Rx(3) --/   \-- PC_B Tx(1)
```
*다이어그램 해설*:
CASE 1은 서로 반대 성격을 가진 장비 간의 연결로, 케이블이 직선을 유지합니다. CASE 2는 동일한 성격을 가진 장비 간의 연결으로, 케이블이 송수신 선을 물리적으로 교차(Cross)시켜서 신호가 상대방의 수신 포트로 들어가도록 유도합니다.

#### 4. 핵심 기술: Auto-MDIX (자동 감지)

```c
/* PHY Chip Pseudo-Code for Auto-MDIX */
function auto_negotiate(link_partner) {
    // 1. Send Fast Link Pulse (FLP) to detect connection
    // 2. Check if Link Partner is responding
    
    if (no_link_established()) {
        // 3. If no link, swap internal Tx/Rx logic
        swap_tx_rx_pins();
        
        // 4. Retry detection
        if (link_up()) {
            print("Connection established via Auto-MDIX crossover");
        } else {
            // 5. Try again or fail
            swap_tx_rx_pins(); // Revert
        }
    }
}
```
*코드 설명*: 실제 PHY 칩(Realtek, Intel 등)의 펌웨어는 링크가 처음에 살아나지 않으면 내부 레지스터 값을 변경하여 송신과 수신 핀의 논리적 배치를 바꿉니다. 이 과정은 수 밀리초 내에 일어나므로 사용자는 인지하지 못합니다.

**📢 섹션 요약 비유**
마치 우체부가 편지를 배달할 때, 보내는 사람의 우체통(MDI)과 받는 사람의 우체통(MDI-X)이 서로 반대 구조여야 편지가 꽂힌다는 원리입니다. 만약 우체통이 똑같은 구조라면, 중간에 편지를 뒤집어서 넣어주는 특수한 택배 박스(크로스 케이블)를 써야 합니다. 요즘은 똑똑한 우체부(Auto-MDIX)가 우체통 모양을 보고 편지를 알아서 뒤집어서 넣어줍니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교표

| 비교 항목 | 다이렉트 케이블 (Straight) | 크로스오버 케이블 (Crossover) | Auto-MDIX (Logical Crossover) |
|:---|:---|:---|:---|
| **물리적 배선** | 양쪽 T568B - T568B | 한쪽 T568A - T568B (혼합) | 물리적으로는 보통 Direct 케이블 사용 |
| **주요 연결 대상** | 이종 계층 (PC ↔ Switch) | 동종 계층 (PC ↔ PC, Switch ↔ Switch) | 모든 장비 (Universal) |
| **Pin 1,2 역할** | 송신(Tx) → 송신(