---
title: "ICT Standardization ITU IEEE 3GPP Strategy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 775
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ITU는 IMT(International Mobile Telecommunications) 비전 및 주파수 배분을 통해 거버넌스·정책 표준을 정립하고, IEEE는 802 계열 근거리·개인영역 액세스 규격(802.3 Ethernet/802.11 WLAN/802.15 WPAN)을, 3GPP는 RAN·SA·CT 3대 TSG 체계를 통해 Release 기반 이동통신 시스템 규격(2G->5G-Advanced->6G)을 주도하는, **상호보완적 3축 글로벌 ICT 표준화 거버넌스**이다.
> 2. **가치**: ITU-T G.7713/Y.1706 분배 제어, IEEE 802.11be MLO(Multi-Link Operation) 46Gbps, 3GPP Release 18 AI/ML 기반 NWDAF(New Radio)·네트워크 슬라이싱 같은 구체적 규격을 통해, **전 세계 80억 가입자가 단일 호환 인터페이스로 5G/6G·Wi-Fi·광대역 통합 서비스**를 이용 가능하게 하며, SEP(Standard Essential Patent) FRAND 라이선싱으로 단일 글로벌 시장 형성에 기여한다.
> 3. **판단 포인트**: ① OSI 7계층·전송계층(예: IEEE 802.11 PHY ↔ 3GPP NR PHY) 및 정책계층(ITU-R WRC 주파수 합의) 어디에 최적화할지 ② IT/통신/미디어 컨버전스 시 ITU-T H.626 vs IEEE 1901 vs 3GPP MEC 중 어느 SDO(Standards Development Organization) 로드맵을 따를지 ③ 표준 채택 시점의 TBT(Technical Barriers to Trade) 대응 및 ETSI/3GPP/IEEE 상호인증(예: 3GPP 5G NR-U vs IEEE 802.11ax 공존) 전략을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

ICT 표준화는 **다수의 벤더가 독자적 규격으로 장비를 출시함에 따라 상호운용성(Interoperability) 붕괴, 국가별 파편화된 시장, Network Effect 미실현**이라는 1980년대 이후 고질적 문제를 해결하기 위한 핵심 메커니즘이다. ITU는 UN 산하의 정부간 기구로 **주파수 배분·국제전기통신규칙(International Telecommunication Regulations, ITR)**을 통해 거버넌스를 형성하고, IEEE-SA(Standards Association)는 **산업 주도 디팩토(De Facto) 표준**을, 3GPP는 **7개 OPO(Organizational Partner: ARIB·ATIS·CCSA·ETSI·TSDSI·TTA·TTC) 협약**을 통해 이동통신 RAN·코어·단말의 글로벌 단일 규격을 제공한다.

1990년대 GSM(2G) 시기에 유럽 ETSI가 유럽 단일 규격을 만든 것이 3GPP의 모태가 되었고, 2000년대 IEEE 802.11g(54Mbps) 보급으로 WLAN이 데이터 트래픽의 60% 이상을 흡수하면서, 모바일 오프로드·5G NR-U(Unlicensed)와 같은 **수직적·수평적 컨버전스**가 가속화되었다. 실무자 입장에서 ICT 표준화 전략은 **R&D 투자 회수, 시장 진입 시점(First-Mover), 지적재산권(IP) 포트폴리오**를 결정짓는 핵심 의사결정이다.

```text
+------------------------------------------------------------------------------+
|           Global ICT Standardization Ecosystem (2024~2030)                   |
|                                                                              |
|  +---------------------+    +---------------------+    +-----------------+  |
|  |       ITU (UN)      |    |      IEEE-SA        |    |     3GPP        |  |
|  |  (정부간 거버넌스)   |    |   (산업 주도)        |    |  (이동통신 OPO)  |  |
|  +----------+----------+    +----------+----------+    +--------+--------+  |
|             |                          |                        |            |
|   +---------+---------+      +---------+----------+   +--------+--------+   |
|   | ITU-R WRC, IMT    |      | 802.11 Wi-Fi (PHY) |   | TSG-RAN (NR/LTE)|   |
|   | - 주파수 24-47GHz  |      | 802.3 Eth (MAC/PHY)|   | TSG-SA (System) |   |
|   | - IMT-2030 6G     |      | 802.15 (BLE/Zigbee)|   | TSG-CT (Core)   |   |
|   | - Rec. M.2150     |      | 1901 (PLC/Powerline)|  | Release 15-20   |   |
|   +-------------------+      +--------------------+   +-----------------+   |
|   | ITU-T SG (Study   |      | 802.1 (Bridging)   |   | 5G-Adv (R18)    |   |
|   |  Group): 13/15/17 |      | 1588 (PTP), 802.1X |   | 6G (R21~)       |   |
|   | - G.7713 (DCM)    |      | 802.11be (Wi-Fi 7) |   | - AI/ML NWDAF   |   |
|   | - H.626 (M2M/IoT) |      | - MLO 320MHz       |   | - ISAC, NTN     |   |
|   | - Y.3170 (AITrans)|      | 802.11ay 60GHz     |   | - Network Slicing|   |
|   +-------------------+      | 802.11bb LiFi      |   |                 |   |
|   | ITU-D (개발도상국) |      | 802.22 WRAN        |   |                 |   |
|   | - Capacity Buil.  |      |                    |   |                 |   |
|   | - ICT for Dev.    |      |                    |   |                 |   |
|   +---------+---------+      +----------+---------+   +--------+--------+   |
|             |                            |                     |            |
|             +------------+---------------+----------+----------+            |
|                          v                          v                       |
|        +---------------------------------------------------------+         |
|        |       Inter-SDO Coordination Bodies (조정의 다리)        |         |
|        | - oneM2M (IoT): 3GPP + ETSI + TIA + OMA + others       |         |
|        | - IETF (Internet): TCP/IP, IPv6, QUIC, TLS 1.3         |         |
|        | - ETSI: EN 300-series (Harmonized Standards -> EU RED)  |         |
|        | - ISO/IEC JTC1: SC42 (AI), SC7 (SW Eng)                |         |
|        | - 3GPP ↔ IEEE LAA/LWA: LTE-WLAN Aggregation (R13)     |         |
|        | - ITU-T FG NET-2030 ↔ 3GPP: 6G Use Cases               |         |
|        +---------------------------------------------------------+         |
|                          |                                                  |
|                          v                                                  |
|        +---------------------------------------------------------+         |
|        |  Standardization Stack in Real Networks (Layering)     |         |
|        |  L7 App: W3C, IETF (HTTP/3)                            |         |
|        |  L4-5:  IETF (TCP/UDP/QUIC)                            |         |
|        |  L3:    IETF (IP), 3GPP (5GC, SBA)                     |         |
|        |  L2:    IEEE 802.11/802.3, 3GPP MAC/RLC                |         |
|        |  L1:    3GPP NR (FR1/FR2), IEEE 802.11 PHY, ITU-R Freq |         |
|        +---------------------------------------------------------+         |
+------------------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교**:
- **기존(2000s)**: 단일 SDO 중심, 국가별/계층별 폐쇄 규격 (예: GSM vs CDMA2000, Wi-Fi vs HiperLAN2)
- **신규(2020s)**: 다중 SDO 협력·IP 기반 통합, **Open RAN(O-RAN ALLIANCE)+3GPP TS 38.401**, **5G NR-U + IEEE 802.11ax 동적共存(ETDE 303 387)**, **AI-native 네트워크(3GPP Rel-18 NWDAF + ITU-T Y.3170 AITrans)**

- **📢 섹션 요약 비유**: ITU가 **UN 본부**(국제 외교 결정), IEEE가 **국가 공업 협회**(산업 현장의 디테일), 3GPP가 **글로벌 자동차 협회**(실제 도로 운행 규칙)라서, 6G 자율주행차를 만들려면 세 단체의 규칙이 모두 호환되어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ICT 표준화 3대 기구의 **계층적·기능적 분업 구조**는 다음과 같이 정의된다.

```text
+-----------------------------------------------------------------------+
|        Functional Layering of ITU, IEEE, 3GPP Standards              |
|                                                                       |
|   +-------------------------------------------------------------+    |
|   | TIER 1: ITU (Global Spectrum & Vision Layer)                |    |
|   |  - ITU-R SG5/SG6/SG1:  WRC(World Radiocom. Conference)     |    |
|   |  - IMT-2020(5G) Rec. M.2150 -> IMT-2030(6G) Rec. M.2160    |    |
|   |  - ITU-T Study Groups:                                     |    |
|   |     SG13 (Future Networks), SG17 (Security), SG20 (IoT)    |    |
|   |  - ITU-T Focus Groups: AI/ML, Quantum, IMT-2030             |    |
|   +--------------------+----------------------------------------+    |
|                        | (Spectrum allocation, Framework Vision)      |
|                        v                                              |
|   +-------------------------------------------------------------+    |
|   | TIER 2: 3GPP (Mobile Cellular Detailed Spec Layer)         |    |
|   |  +----------+   +----------+   +----------+                |    |
|   |  | TSG-RAN  |   |  TSG-SA  |   |  TSG-CT  |                |    |
|   |  | WG1 PHY |   | WG2 Sys  |   | WG1 NAS  |                |    |
|   |  | WG2 MAC |   | WG3 Sec  |   | WG3 CT4  |                |    |
|   |  | WG3 RAN |   | WG4 OAM  |   | WG4 CT5  |                |    |
|   |  | WG4 RAN |   | WG5 Tel  |   | WG6 CT6  |                |    |
|   |  | WG5 RAN |   | WG6 Mgt  |   +----------+                |    |
|   |  +----------+   +----------+                                |    |
|   |  - Releases: Rel-15 (5G NR NSA) -> R18 (5G-Adv) -> R20 (6G)  |    |
|   |  - Specs: TS 38.211(Phy), 38.300(Overall), 38.401(NG-RAN) |    |
|   |  - Output: 5000+ TS/TR documents per Release              |    |
|   +--------------------+----------------------------------------+    |
|                        | (Detailed Cell/System spec)                   |
|                        v                                              |
|   +-------------------------------------------------------------+    |
|   | TIER 3: IEEE-SA (Local/PAN/Access Layer)                   |    |
|   |  - IEEE 802 LMSC (LAN/MAN Standards Committee)             |    |
|   |  - Working Groups: 802.1/.3/.11/.15/.16/.22/.24            |    |
|   |  - Output: ~700 active standards, ~2,000 in portfolio     |    |
|   |  - Industry Connections (Pre-standards research)            |    |
|   +--------------------+----------------------------------------+    |
|                        | (PHY/MAC detailed implementation)             |
|                        v                                              |
|   +-------------------------------------------------------------+    |
|   | Real Network Implementation (L1~L7 stack)                  |    |
|   |  Smartphone/IoT -> 3GPP NR + 5GC + IEEE 802.11ax/bt + IPv6  |    |
|   +-------------------------------------------------------------+    |
+-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ITU-R (무선통신국)** | 주파수 스펙트럼 국제 분배·궤도/위성 등록, IMT 비전 정의 | WRC-23 결정(예: 6GHz IMT 식별, 12.75–13.25GHz 등 5G/6G 추가), IMT-2030 6G Framework Rec. M.2160(6 usage scenarios: Immersive Comm, Hyper Reliable, Massive Comm, AI/Comm, Ubiquitous, Digital Twin) |
| **ITU-T (전기통신표준화국)** | 유무선 네트워크·서비스·보안 Recommendations | SG13(미래망·IMT-2020 beyond) Y.3170 AI-enabled networking, SG17(보안) X.805, SG20(IoT·스마트시티) Y.4000 시리즈, Focus Group 2030(Net2030)에서 차세대 패킷 구조(Flexible Network Service) 제안 |
| **ITU-D (개발국)** | 개발도상국 역량 강화, ICT 지표(e-Health, e-Education) | Connect 2030 Agenda, ICT 개발 지수(IDI) 산정, WTSA(세계전기통신표준화총회) 정책 조정 |
| **IEEE-SA** | 산업 주도 단일/이종 액세스 기술 표준화 | 802.11be(2024): MLO + 320MHz + 4096-QAM -> 46Gbps, 802.11ay(60GHz, 100Gbps), 802.11bb(빛 기반 LiFi), 1901(PLC), 802.22(WRAN TV White Space), 1547(DER/스마트그리드), 7000-series 의료 AI/IoT |
| **3GPP TSG-RAN** | RAN(Radio Access Network) 무선 인터페이스 규격 | RAN1: 물리계층(NR numerology μ=0..5