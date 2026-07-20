---
title: "Cyber Physical System CPS Convergence Security"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 786
---
# 786. 사이버 물리 시스템 CPS 융합 보안 (Cyber-Physical System CPS Convergence Security)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사이버 물리 시스템(CPS)은 센싱(Sensing)·네트워킹(Networking)·제어(Control)·액추에이션(Actuation)이 실시간 폐루프(Closed-Loop)로 결합된 시스템으로, IT(정보기술)와 OT(운영기술)가 융합되는 환경에서 발생한다. 보안의 패러다임이 CIA(기밀성·무결성·가용성)에서 **Safety+Security+Resilience+Privacy**의 4축 융합 신뢰성 모델로 전환되는 것이 핵심이다.
> 2. **가치**: Stuxnet(2010), BlackEnergy(2015, 우크라이나 전력망), TRITON/TRISIS(2017, SIS 타깃), Colonial Pipeline(2021) 등 사이버-물리 공격은 인명 피해와 국가 기반시설 마비로 직결된다. 글로벌 평균 OT 인시던트 다운타임 비용은 **1일 2백만~3백만 USD**(Ponemon 2023), 스마트팩토리 전체 장애 시 연간 매출의 **3~7% 손실**이 발생하며, IEC 62443·NIS2·K-ISMS-P 등 규제 준수 및 보험 인수를 위한 필수 요건이다.
> 3. **판단 포인트**: ① IT-OT 경계에서 **Purdue 모델 기반 존(Zone)·컨듀잇(Conduit) 분리** vs. **Zero Trust 마이크로세그먼테이션**의 아키텍처 선택, ② 레거시 OT 프로토콜(예: Modbus/TCP, DNP3)의 보안 강화 시 **가용성(Availability) 손실 위험** vs. 보안성 확보, ③ Safety(기능안전, IEC 61508/61511)와 Security의 **동시 공학적 설계(Safety-Security Co-engineering)** 여부, ④ 실시간 결정제어(예: 1ms 이내 응답 요구) 환경에서 **암호화·인증 오버헤드** 허용 범위, ⑤ AI/ML 이상탐지의 **False Positive가 OT 운영에 미치는 영향** 관리가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적으로 산업 현장의 운영기술(OT: Operational Technology)은 공기 차단(Air-gap)·폐쇄망·독자 프로토콜을 통해 IT 환경과 분리되어 왔다. 그러나 **Industry 4.0, Industrial IoT(IIoT), 5G URLLC, AIoT, Digital Twin** 등의 확산으로 스마트팩토리·스마트그리드·자율주행·의료 IoT·자율주행 드론 등 **CPS**가 보편화되면서, **IT-OT-Convergence(융합)**는 선택이 아닌 생존 전략이 되었다. 한국 정보통신산업진흥원(NIPA) 통계에 따르면 2024년 기준 국내 스마트공장 보급률이 약 4만 개소를 돌파하며, 사이버-물리 공격 표면은 기하급수적으로 증가했다.

그러나 사이버 공격의 **임팩트(Impact)** 측면에서 CPS는 기존 IT 시스템과는 질적으로 다른 도전을 제기한다. 단순 데이터 유출이 아닌 **물리적 세계(Physical World)로의 직접적 파급**이 발생한다. 2010년 이란 원심분리기 파괴(Stuxnet), 2014년 독일 제철소 고로(Blast Furnace) 제어시스템 손상으로 인한 대규모 물리적 손상, 2017년 사우디아라비아 Tritoneer(Triton/TRISIS) 공격에 의한 안전계장(SIS) 무력화 시도, 2021년 미국 최대 송유관 Colonial Pipeline 셧다운 등은 CPS 보안의 **Safety·Security 융합**이 단순한 정보보호 차원을 넘어 **국가 안보·인명 안전·환경 보호**와 직결됨을 입증했다.

```text
[전통적 IT-OT 분리 환경]                    [CPS 융합 환경]
  +------------+                          +------------------------------+
  |  IT 망     |   Air-gap                |    Enterprise / Cloud        |
  | (ERP,CRM)  | ◄----------------------► |  +----------------------+    |
  +------------+      (단절)              |  |   IT Zone (L4-L5)    |    |
                                          |  |   ERP·MES·Analytics  |    |
  +------------+                          |  +----------+-----------+    |
  |  OT 망     |                          |             | Diode/Conduit  |
  | (SCADA,PLC)|                          |  +----------v-----------+    |
  +------------+                          |  |  DMZ / Industrial    |    |
   레거시 프로토콜                          |  |  DMZ (L3.5)          |    |
   독자 폐쇄망                              |  +----------+-----------+    |
   수명 20~30년                             |             |                |
                                          |  +----------v-----------+    |
  -> 보안 사고 시 데이터 유출에 그침         |  |  OT Zone (L0-L3)    |    |
                                          |  |  SCADA·HMI·PLC·DCS  |    |
                                          |  +----------+-----------+    |
                                          |             | Fieldbus      |
                                          |  +----------v-----------+    |
                                          |  |  Physical Process    |    |
                                          |  |  (Sensor/Actuator)   |    |
                                          |  +----------------------+    |
                                          +------------------------------+
                                          -> 보안 사고 시 인명/환경/시설 피해
```

기존 IT 보안 프레임워크(예: ISO 27001, 일반 ISMS)는 **데이터의 기밀성(C)·무결성(I)** 위주이며, 가용성(A)은 상대적으로 낮다. 반면 OT/CPS는 **가용성이 최우선**(예: 발전소 제어신호 1ms 지연 허용 불가, 항공기 플라이 바이 와이어 10ms 이내)이며, 24/7 무중단 운영, 15~30년의 장수명 자산, 패치 불가 레거시 시스템 등의 제약이 따른다. 따라서 **CPS 융합 보안**은 IT 보안 원칙을 OT 환경에 **맥락 적합적으로 재해석·확장**하는 작업이며, 단순히 IT 보안 도구를 이식하는 것이 아니다.

- **📢 섹션 요약 비유**: **"자동차와 비행기의 결합"** — 자동차(세계 최고의 보안을 가진 IT 시스템)와 비행기(실시간 결정제어가 필수인 OT 시스템)를 합쳐 만든 '드론 택시'를 생각하면 된다. 자동차 보안 사고가 데이터를 유출하는 데 그친다면, 비행기 결합 시스템의 보안 사고는 인명 피해로 직결되므로, 보안을 자동차 기준이 아니라 **비행기 안전 인증 기준**(DO-178C + ED-202A)으로 설계해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CPS 융합 보안 아키텍처의 출발점은 **Purdue Reference Model(ANSI/ISA-99)**이며, 이를 IEC 62443의 **Zone-Conduit 모델**로 정형화하고, NIST CSF(Identify·Protect·Detect·Respond·Recover) + IEC 62443 SL(보안 레벨) + IEC 61508 SIL(기능안전 무결성 레벨)을 **동시 공학(Co-engineering)**한다.

```text
+---------------------------------------------------------------------+
|                   CPS Convergence Security Architecture              |
+---------------------------------------------------------------------+
|                                                                       |
|  Layer 5: Enterprise / Cloud                                         |
|   +- ERP, Cloud Analytics, AI/ML Risk Engine, GRC                    |
|   |   보안: CASB, SASE, Cloud Security Posture Mgmt(CSPM)             |
|   |   표준: ISO 27001, SOC 2, K-ISMS-P                                |
|   +----------------------------------------------+                   |
|                                                  | Zero Trust Gateway|
|                                                  | (ZTNA: BeyondCorp)|
|  Layer 4: Site Business Planning & Logistics       |                  |
|   +- MES, MOM, Historian, Reporting                |                  |
|   |   보안: RBAC, MFA, Application Whitelisting   |                  |
|   +----------------------------------------------+                  |
|                          ^                                            |
|   --------------- Industrial DMZ (L3.5) ---------------              |
|   [Unidirectional Security Gateway (Data Diode),                    |
|    ICS-aware Firewall (e.g., SEL-3620, Hirschmann EAG),              |
|    Jump Server w/ PAM (CyberArk, WALLIX),                            |
|    OT-Native SIEM (Dragos, Nozomi, Claroty)]                         |
|                          ^                                            |
|  Layer 3: Site Operations (Operations & Control)                    |
|   +- SCADA Server, HMI, Engineering Workstation,                    |
|   |   Historian, Patch Server (offline repo)                         |
|   |   보안: Application Whitelisting, Code Signing,                  |
|   |         Anti-Malware (ICS-tuned), Log Forwarding                 |
|   +----------------------------------------------+                  |
|                                                  | Conduit          |
|  Layer 2: Area Supervisory Control                 | (MTU/MRU,        |
|   +- PLC, DCS Controller, RTU, Operator Station   |  Cell/Router)    |
|   |   프로토콜: Modbus/TCP, DNP3, IEC 61850, IEC 60870-5-104        |
|   |   보안: MACsec/Modbus-TLS, DNP3-SA, IEC 62351-3/4/5             |
|   |   (단, 레거시 단말은 무인증 -> 네트워크 분리 + 모니터링)          |
|   +----------------------------------------------+                  |
|                          ^                                            |
|  Layer 1: Basic Control (Local Control)                              |
|   +- PLC, Smart RTU, Loop Controller, Sensor Hub                     |
|   |   보안: Trusted Boot (TPM 2.0), Secure Firmware Update,          |
|   |         Hardware Root of Trust                                    |
|   +----------------------------------------------+                  |
|                                                  | Sensor Bus       |
|  Layer 0: Physical Process                         | (4-20mA, HART,  |
|   +- Sensors, Actuators, Valves, Motors, Drives   |  Foundation      |
|   |   보안: Tamper Detection, Physical Security   |  Fieldbus)       |
|   |   표준: IEC 61508 SIL 1~4 (Functional Safety) |                  |
|   +----------------------------------------------+                  |
|                                                                       |
|  ★ Cross-cutting:                                                    |
|   • ICS-Specific SIEM/SOAR + ICS Protocol DPI                       |
|   • MITRE ATT&CK for ICS (T0836~T0859) 기반 Threat Hunting          |
|   • Digital Twin 기반 Anomaly Detection (Physics-informed ML)        |
|   • Safety-Security Co-engineering (Hazard Log + Threat Model)       |
|   • SBOM + Firmware SBOM (CycloneDX, SPDX)                          |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **물리 계층 (L0) & 기본제어 (L1)** | 실제 공정 측정 및 직접 제어. 기능안전(IEC