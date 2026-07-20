---
title: "Smart Grid Demand Response DR VPP"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 732
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DR(Demand Response)과 VPP(Virtual Power Plant)는 분산에너지자원(DER)을 **OpenADR 2.0b/2.0c, IEEE 2030.5, IEC 61850** 등 표준 프로토콜 기반의 양방향 통신으로 집계(Aggregation)하여, 발전소와 동등한 **예비력(Reserve), 주파수조정(Frequency Regulation), 용량(Capacity)** 자원으로 계통에 제공하는 ICT-전력 융합 시스템이다.
> 2. **가치**: 첨두부하 절감을 통한 발전설비 증설 억제(LCOE 기준 약 10~15% 설비비 절감), 신재생 변동성 흡수로 ESS 단독 대비 약 **2.5배**의 비용효율, 소비자에게 피크시간 약 **30~50%** 요금 절감 및 보조서비스 수익 약 **50~150만원/MW/년**의 정량적 편익을 창출한다.
> 3. **판단 포인트**: 통신 표준(OpenADR vs IEEE 2030.5), 집계 단위(VEN 단위 약 100kW~10MW), 시장 참여 형태(용량시장/에너지시장/보조서비스), 보안 프레임워크(**IEC 62351, NERC CIP**), 그리고 기존 EMS·SCADA·AMI 시스템과의 인터페이스 경계 설계가 핵심 의사결정 요소이다.

---

## Ⅰ. 개요 및 필요성

전 세계 전력계통은 화석연료 의존 탈피(RE100·탄소중립), 신재생 비중 확대(2030년 재생에너지 20% 이상 의무화), 그리고 냉난방 부하 증가와 EV 충전 부하로 인한 **Duck Curve(오리 등 곡선)** 심화에 직면해 있다. 한국의 경우 여름철 최대부하가 약 **110GW**(2023년 기준)를 돌파하며, 경부하-중부하-첨두부하 간의 격차가 약 3배에 이른다. 전통적 공급중심(Generation Follows Load) 패러다임은 **피크발전기(LNG 복합, 10kV/kW 단가)**의 상시 건설을 요구하나, 연간 가동률이 5~10%에 불과하여 설비이용률과 수익성이 모두 떨어진다.

**DR(Demand Response, 수요반응)**은 전력요금 신호 또는 인센티브에 반응하여 소비자가 자발적으로 부하를 감축·이동시키는 메커니즘이며, **VPP(Virtual Power Plant, 가상발전소)**는 DER(태양광, 풍력, BESS, EV, DR, 연료전지, 수요자원)을 **클라우드 기반 DERMS(Distributed Energy Resource Management System)**로 통합하여 단일 발전단위처럼 제어·거래하는 구조이다. 즉, **DR = 소비자 행동 변화**, **VPP = DR을 포함한 모든 DER의 통합 가시화·제어**의 관계로, VPP가 DR을 포괄하는 상위 개념이라 할 수 있다.

```text
[전통적 공급중심 그리드]                       [스마트 그리드 DR/VPP 기반]

  발전소 --- 송전 --- 배전 --- 부하               DER(DG,ESS,EV,DR) --+
  (1:N 일방향)                                       |  AMI/SmartMeter
  한전 -> 수용가                                      |  양방향 ICT       |
  고정요금/계시별요금                          +------+------+            |
                                            |   DERMS     | <-----------+
                                            | (집계/Agg)  |
                                            +------+------+
                                                   | OpenADR 2.0b
                                                   | IEEE 2030.5
                                                   | IEC 61850-7-420
                                                   v
                                          전력시장(PX/ISO/RTO)
                                          - 용량시장(Capacity)
                                          - 에너지시장(Energy)
                                          - 보조서비스(Ancillary)
                                          -> 한전 DR 시장(현물/계약형)
```

기존 SCADA 기반 중앙집중식 EMS는 154kV 이상 송전계통에 최적화되어 있어, **수요측 22.9kV 이하 배전단**의 소규모·분산 자원을 실시간(1~4초 주기) 제어하기에는 한계가 있다. 또한 신재생 출력은 기상변동에 따라 4초~수분 단위로 출력이 흔들리므로, **1차 주파수 응답(FCR)** 자원이 필수적이며 VPP가 이를 경제적으로 제공한다.

- **📢 섹션 요약 비유**: 피크시간의 `댄스(춤)`은 모두가 같은 박자에 춤을 추는 것이고, DR/VPP는 각자 `다른 박자`로도 출석을 인정받아 요금 할인을 받는, 즉 **"전력계통의 카풀/우버 풋(Flexible Pool)"** 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

VPP-DR 시스템은 일반적으로 **3계층(Tier)** 아키텍처로 구성된다. **Tier-1 현장(Edge)**: DER 자산(PCS, BMS, EMS, Smart Meter), **Tier-2 집계(Aggregation)**: VEN(Virtual End Node) 게이트웨이·Aggregator, **Tier-3 상위(Cloud/Market)**: VTN(Virtual Top Node)·DERMS·ADMS·전력시장 인터페이스.

핵심 통신 흐름은 다음과 같다. ① VTN(한전 수요반응 서버)이 시장가·계통 신뢰도 신호(Price, Reliability Event, Direct Control)를 **OpenADR 2.0b EiEvent/Report Service**로 Publish. ② VEN(소비자 측 EMS, 예: ABB Ability, Hitachi DERMS, 자체 게이트웨이)가 EiEvent를 수신하여 ③ 로컬 DER(BESS 충방전, HVAC setpoint 조정, ESS SOC 관리) 및 부하 감축 계획 수립. ④ VEN이 oadrReport로 감축 실적(kW·kWh·10분 단위)을 VTN에 보고. ⑤ VTN이 검증을 거쳐 **정산·보상**(DR 시장 정산단가 × 감축량)을 수행.

```text
                     [Tier-3: 상위 제어/시장 계층]
   +----------------------------------------------------------+
   |  VTN (Virtual Top Node) - 한전 DRMS, AGC/ADMS           |
   |  +- OpenADR 2.0b VTN Server (e.g., EPRI DRMS, Cisco)    |
   |  +- DERMS 최적화 엔진 (MILP, SLP, Heuristic)            |
   |  +- 시장 인터페이스: KEPCO DR, KPX, ISO/RTO, P2P 블록체인|
   |  +- IEC 61970 CIM / 61968 메시지 버스                   |
   +--------------------+-------------------------------------+
                        |  TLS 1.2+, X.509 PKI
                        |  (IEC 62351 보안)
                        v
   +----------------------------------------------------------+
   | [Tier-2: 집계/관문 계층 - Aggregator/VEN 게이트웨이]      |
   |                                                          |
   |   VEN Gateway (On-Premise / Edge)                         |
   |   +- OpenADR 2.0b VEN Client (e.g., OpenLEADR, VOLTTRON) |
   |   +- Modbus TCP / DNP3 / IEC 61850 MMS                  |
   |   +- DER 디스패치·예측 모듈 (LSTM, XGBoost)              |
   |   +- 로컬 시장 Proxy (수요-공급 매칭)                    |
   +------+-----------------------------+---------------------+
          | RS-485/CAN/LTE/PLC          | Wi-SUN/LoRaWAN/MQTT
          v                             v
   +---------------------+    +------------------------------+
   |[Tier-1: 현장 계층]   |    | [Tier-1: 현장 계층]          |
   |  BESS PCS + BMS     |    |  건물 BAS/BMS (BACnet/Modbus)|
   |  PV 인버터 (Modbus) |    |  HVAC·조명·EV충전기 (OCPP)   |
   |  Smart Meter (DLMS) |    |  공장 PLC (Siemens S7)       |
   |  Fuel Cell (PCS)    |    |  데이터센터 UPS/PDU          |
   |  EV V2G (CHAdeMO)   |    |  냉동창고·양돈장 부하         |
   +---------------------+    +------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **VTN (Virtual Top Node)** | DR 이벤트 생성, 시장 정산, 계통 신뢰도 판단 | OpenADR 2.0b의 `oadrDistributeEvent`로 PAYLOAD(`simple`, `price`, `loadcontrol`, `program`) 전달. Ramping(램프업/다운) 파라미터(분 단위) 지정 |
| **VEN (Virtual End Node)** | 현장 DER·부하의 측정·제어·보고 | OpenADR `EiRegisterParty`, `oadrReport`로 10분 단위 실측치 송신. IEEE 2030.5의 IEEE 1815(DNP3-SA) 지원 가능 |
| **DERMS (DER Management System)** | 수백~수천 VEN의 최적 스케줄링 | MILP/MILP+Heuristic로 비용최소·탄소최소 목적함수. SOC 안전제약(20~80%), 부하복원 시간, 페어링(Pairing) 제약 반영 |
| **AMI / Smart Meter** | 15분~1시간 단위 소비 측정, 양방향 통신 | KEPCO AMI는 LTE-M 기반 15분 수집. DLMS/COSEM, IDIS 규격. 자동 수요반응(ADR) 트리거의 데이터 소스 |
| **Edge EMS / 게이트웨이** | 로컬 폴루프 제어, VEN↔필드 디바이스 변환 | Raspberry Pi 4 + Node-RED, 또는 Siemens LOGO!, ABB Ability EDCS. OCPP 1.6/2.0.1로 EV 충전 제어 |
| **전력시장/정산 시스템** | KPX·한전 DR 시장 입찰, 정산 | 시간대별 SMP(시스템한계가격), DR 입찰 곡선 등록, 실적 검증 Baseline(조정고객 기준부하 CBL) 산정 |
| **사이버보안 계층** | 인증·무결성·기밀성 보장 | IEC 62351-6(통신 보안), X.509 클라이언트 인증서, TLS 1.3, NIST IR 8259 기반 IoT 보안 |

**핵심 파라미터 및 알고리즘**:
- **베이스라인 산정**: 10/15분 단위 **CBL(Customer Baseline Load)** = 최근 5영업일 동일 시간대 가중평균 × 조정계수(Factor: 0.7~1.3). 한전 DR 시장은 `High 4 of 5(최근 5일 중 최고치 4개 제외 평균)` 방식 채택.
- **감축량 검증**: `감축량 = Baseline - 실제수요 - 조정량`. ±20% 이내 오차 시 통상 `성능계수(Performance Factor, 0.5~1.0)` 적용.
- **보조서비스 응답속도**: 1차 주파수응답(FCR) = 0.5초 이내 50%, 4초 이내 100%. FFR(Fast Frequency Response) = 1초 이내 응답. BESS는 FCR 적합, DR은 보통 1~10분 단위 반응(Reg-D 신호 등).
- **집계 규모(Aggregation Size)**: 한전 DR 현물시장 최소 단위 = 100kW(2020년 이후 1MW에서 100kW로 완화). 미국 PJM 주파수조정 시장 최소 100kW, CAISO DERP = 500kW.

- **📢 섹션 요약 비유**: VPP는 마치 **"수천 명의 소규모 발전원을 한 명의 지휘자(DERMS)가 지휘하는 오케스트라"**이며, VEN은 각 악기, OpenADR는 악보 전달 통로, BESS는 즉석에서 박자를 맞추는 드럼 역할을 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **DR (수요반응)** | **VPP (가상발전소)** | **Microgrid (마이크로그리드)** |
| :--- | :--- | :--- | :--- |
| **대상 자원** | 부하(공장, 빌딩, 데이터센터) | DER 전체(부하, PV, BESS, EV, FC) | 특정 지역 내 DER(자가운영) |
| **제어 범위** | 감축·이동(Load Shedding/Shift) | 출력 상하 양방향(Generation & Load) | 독립 운전(Island) 가능 |
| **통신** | OpenADR 2.0b 단방향/양방향 혼합 | OpenADR 2.0b/c, IEEE 2030.5, IEC 61850-7-420 | IEC 61850 기반 내부 통신, OpenADR 상위 |
| **시장 참여** | DR 입찰(감축량), 첨두절감 | 에너지/용량/보조서비스 3개 시장 동시 | 자가소비 + 잉여 전력 계통 역송전 |
| **인프라 투자** | 저(요금 신호 + EMS) | 중(VEN 게이트웨이, DERMS 라이선스) | 고(보호협조, PMS, ESS 규모 1MW 이상) |
| **정산 단가** | 약 5~15만원/MWh (한전 DR) | 약 10~30만원/MWh (스프링) + 용량가 | 자체 수익모델 또는 PPA |
| **계통 연계** | 항상 계통연계(Grid-Connected) | 기본 계통연계, 일부 islanding | 계통연계/독립 양면 |
| **예측 필수성** | 부하예측(중요) | DER 다중