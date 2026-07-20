---
title: "Red Team Blue Team Purple Team Security"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 739
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 레드팀(공격 시뮬레이션), 블루팀(방어·탐지·대응), 퍼플팀(양 팀 간의 협업 촉진 및 지식 통합)을 통해 MITRE ATT&CK 매트릭스 기반의 실제 공격자 TTP(Tactics, Techniques, Procedures)를 모사하고, 탐지 커버리지·MTTD(Mean Time To Detect)·MTTR(Mean Time To Respond)을 정량적으로 측정·개선하는 적응형 보안 검증(Adaptive Security Validation) 체계입니다.
> 2. **가치**: 단순 침투 테스트가 1회성 스냅샷인 반면, 퍼플팀 운영은 (1) MITRE ATT&CK Navigator 기반 탐지 갭(Detection Gap)을 20~40% 축소, (2) SOC 분석가의 알림 피로도(Alert Fatigue)를 Tier 1 알림 1건당 처리 시간 30% 단축, (3) EDR/SIEM 룰의 회색 영역(Grey Area) 탐지율 85% 이상 달성이라는 정량적 효과를 제공합니다.
> 3. **판단 포인트**: 운영 성숙도(CMM 1~5단계)에 따라 (a) RED-only 모드(연 1~2회 TIBER-EU/CBEST 정적 평가) -> (b) BLUE+RED 격리 모드(분기별 BAS 도구 활용) -> (c) Purple 통합 모드(Continuous Automated Red teaming, CARTA 기반 지속 검증)로 단계적 전환이 필요하며, 예산·법적 책임 소재(Active Defense 시점)·내부 통제(Change Management)·SOC 인력 역량(Tier 1~3)을 종합 고려해야 합니다.

---

## Ⅰ. 개요 및 필요성

전통적 침투 테스트(Penetration Test)는 연 1~2회, 2~4주 단위로 수행되어 발견된 취약점이 다음 분기 패치 윈도우까지 방치되는 '점(Point)' 평가였습니다. 하지만 SolarWinds(2020), Colonial Pipeline(2021), Log4j(2021) 등 공급망 공격과 Living-off-the-Land(LotL) 기반 지속 위협(APT) 증가는, 알려지지 않은 제로데이의 평균 탐지 시점이 277일(Mandiant M-Trends 2023)에 달하는 현실을 노출시켰습니다. 이러한 환경에서 CISO는 "우리 환경에서 MITRE ATT&CK 14개 전술 중 어느 단계가 탐지되는가?"라는 질문에 즉시 답할 수 있어야 하며, 이를 위해 Red/Blue/Purple Team 기반의 **지속적 적대자 에뮬레이션(Continuous Adversary Emulation)** 패러다임이 등장했습니다.

특히 금융권은 EU의 TIBER-EU(2018), 영국의 CBEST, 싱가포르의 AASE(Adversarial Attack Simulation Exercises), 한국 금융보안원의 FSD(Financial Security Drill) 등을 통해 규제 차원에서 레드팀 훈련을 의무화하고 있으며, ISO/IEC 27001:2022 통제 항목 A.5.7(Threat intelligence), A.8.16(Monitoring activities), NIST CSF 2.0의 DE.CM(Continuous Monitoring)·RS.MI(Mitigation) 기능과 직접 매핑됩니다.

```text
   [전통 침투 테스트]                              [Red/Blue/Purple Team]
   +--------------+                          +------------------------------+
   |  연 1~2회    |                          |  지속적(Continuous) 운영    |
   |  2~4주 스프린트|                          |  BAS + 에뮬레이션 + 자동화   |
   |  블랙박스/그레이박스|                        |  ATT&CK 기반 정량 측정      |
   |  보고서 위주  |                          |  탐지 규칙 + 플레이북 갱신   |
   +------+-------+                          +--------------+---------------+
          |                                                 |
          v                                                 v
   알려진 취약점 스냅샷                              탐지 갭 + MTTD/MTTR KPI
   (스태틱 리스크 뷰)                               (다이내믹 포즈러 뷰)
```

**왜 필요한가?**
- **시간 차원의 비대칭 해소**: 공격자 dwell time 277일 vs 방어자 패치 주기 30~90일 -> 24/7 지속 검증 체계 필요
- **시뮬레이션-실제 갭(Simulation-Real Gap) 축소**: 침투 테스트의 70%는 내부자/내부망 시나리오 미반영, 퍼플팀은 LotL(예: PowerShell LOLBins, WMI Event Subscription)까지 다룸
- **탐지 엔지니어링(Detection Engineering) 파이프라인화**: Sigma 룰 -> Splunk SPL/Elastic KQL -> EDR Telemetry 검증 사이클을 자동화
- **규제·보험 요건 대응**: SEC Cybersecurity Disclosure Rule(2023), 한국 금융·공공기관 ISMS-P 인증심사 시 통제 항목으로서의 실증적 증거 확보

- **📢 섹션 요약 비유**: 연 1회 건강검진 vs 매일 Apple Watch로 실시간 심전도를 측정하는 차이 — 후자는 이상 징후가 생기는 즉시 "알림 -> 조치" 피드백 루프가 돌아갑니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Red/Blue/Purple Team 운영의 기술적 핵심은 **공격자 관점의 TTP 인벤토리**, **방어자 관점의 탐지 파이프라인**, **통합 관점의 자동화·측정 프레임워크** 3개 축으로 구성됩니다. ATT&CK Enterprise v14 기준 14개 전술(Tactics), 202개 기법(Techniques), 424개 하위 기법(Sub-Techniques)을 체계적으로 매핑해야 합니다.

```text
                       +---------------------------------------------+
                       |       Threat Intelligence Platform (TIP)     |
                       |  MISP / OpenCTI / Anomali / ThreatQuotient  |
                       +-----------------+---------------------------+
                                         | STIX 2.1 / TAXII 2.1
                                         v
       +-------------------+    +--------------------+   +--------------------+
       |    RED TEAM       |    |   PURPLE TEAM      |   |    BLUE TEAM       |
       |   (공격 시뮬레이션) |◄--►|  (통합·조정·자동화) |◄--►|  (방어·탐지·대응)   |
       +---------+---------+    +---------+----------+   +----------+---------+
                 |                        |                          |
   +-------------+----------+  +----------+----------+  +-----------+----------+
   | • Cobalt Strike (C2)   |  | • MITRE Caldera     |  | • SIEM: Splunk /     |
   | • Brute Ratel (C2)     |  | • Vectr (Metrics)   |  |   Elastic / QRadar   |
   | • Mythic / Havoc       |  | • ATT&CK Navigator  |  | • EDR: CrowdStrike / |
   | • Sliver (C2, Go)      |  | • Atomic Red Team   |  |   SentinelOne / Wazuh|
   | • Atomic Red Team      |  | • Stratus Red Team  |  | • NDR: Vectra /      |
   |   (GitHub, 1,000+ tests)|  | • Plextrac          |  |   Darktrace / Corelight|
   | • Caldera (자동 에뮬)   |  | • AttackIQ / SafeBreach| | • SOAR: Tines /     |
   | • RTA (Red Team Automation)| | • BAS Continuous    |  |   Cortex XSOAR       |
   | • Nmap / Masscan / Nessus| |   Validation Platform| | • TIP + CTI          |
   +------------------------+  +---------------------+  +----------------------+
                                         |
                                         v
                       +---------------------------------------------+
                       |  측정 KPI: MTTD, MTTR, Detection Coverage % |
                       |  출력: ATT&CK Heatmap (14 Tactics × N Tech) |
                       |  액션: Sigma 룰 배포 / SOAR 플레이북 업데이트|
                       +---------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Red Team (공격 측)** | 실제 공격자 TTP 모사, 침투 경로·이메일·웹·물리·내부 측면 시뮬레이션 | (1) C2 프레임워크(Cobalt Strike Beacon, Sliver gRPC, Brute Ratel) — HTTPS/Malleable C2/DNS-over-HTTPS으로 탐지 회피<br>(2) 초기 침투: Spear-Phishing(Macro, LNK, ISO), Watering-Hole, Supply Chain(예: 3CX, SolarWinds)<br>(3) MITRE Caldera의 Adversary Profile(APT29 Cozy Bear, FIN7, Lazarus) JSON을 임포트해 자동 운영<br>(4) Atomic Red Team 1,000+ 테스트 중 환경에 맞는 TTP 선택 실행<br>(5) OPSEC: Beacon Block Hooking, ETW Patch, AMSI Bypass |
| **Blue Team (방어 측)** | 탐지·분석·포함·복구(Detect/Analyze/Contain/Recover) | (1) SIEM의 Correlation Rule(Splunk SPL, Elastic EQL) — Sigma 룰 -> 다중 로그 정규화<br>(2) EDR의 Telemetry(Sysmon, ETW, eBPF) — ProcessCreate, ImageLoad, DriverLoad, NetworkConnect, AMSI/ETW Event<br>(3) 위협 헌팅(Hypothesis-driven Hunt) — Atomic Red Team 실행 후 IOC/IOA 검증<br>(4) SOAR 플레이북 — 자동 격리(EDR Network Containment), 계정 비활성화(AD Disable), IOC 차단(Firewall, DNS Sinkhole)<br>(5) Forensics: Velociraptor, KAPE, MemProcFS 기반 메모리/디스크取证 |
| **Purple Team (통합·조정)** | Red의 공격 시나리오 ↔ Blue의 탐지 커버리지를 매핑하고 자동화 | (1) **MITRE ATT&CK Navigator JSON**을 입력/출력 표준으로 사용 — 탐지된 Technique는 녹색, 미탐지는 빨간색 히트맵<br>(2) Vectr/Plextrac로 양 팀의 진척도 대시보드 제공<br>(3) AttackIQ/SafeBreach/Guardicore(Centra) 같은 BAS(Breach and Attack Simulation) 플랫폼으로 24/7 지속 검증<br>(4) Purple Team Exercise 워크숍 — 1회 2~4시간, 1주 단위 Sprint, 시나리오별 (Pre-Attack -> Execute -> Detect? -> Hunt? -> Mitigate?) 체크리스트 |
| **측정·지표 체계** | ROI 입증 및 탐지 성숙도 정량화 | (1) **Detection Coverage %** = (탐지된 Sub-Technique 수 / 전체 활성 Sub-Technique 수) × 100 — 목표 80% 이상<br>(2) **MTTD (Mean Time To Detect)** — 첫 알림 발생 -> 분석가 확인, 목표 < 1시간<br>(3) **MTTR (Mean Time To Respond/Remediate)** — 분석가 확인 -> 격리 완료, 목표 < 4시간<br>(4) **False Positive Rate** — Tier 1 알림 중 오탐 비율, 목표 < 15%<br>(5) **Time to Patch Detection Gap** — 미탐지 TTP 발견 후 탐지 룰 배포까지 걸린 시간 |

**핵심 프로토콜·기술 심화**:

- **ATT&CK Navigator JSON 포맷**: `{"name":"Finance Red Team","versions":[{"attackVersion":"14","technique":[{"techniqueID":"T1059.001","score":1,"color":"#33ff66"},{"techniqueID":"T1003.001","score":0,"color":"#ff3333"}]}]}` — Purple Team 회의의 단일 진실 공급원(SoT)
- **Sigma 룰 변환 체인**: Sigma(YAML) -> SIEM 고유 문법(Splunk SPL, Elastic KQL, Chronicle YARA-L) 자동 변환 via `sigmac` / `uncoder.io`
- **Sysmon 구성 베스트프랙티스**: `DriverLoad`(EID 6), `ProcessCreate`(EID 1, Parent/Child 관계), `ImageLoad`(EID 7, Signed/Unsigned), `PipeEvent`(EID 17/18, C2 채널), `WmiEventConsumer`(EID 19~21, 지속화) — 최소 30개 이상 이벤트 ID 운영
- **칼데라(Caldera) Adversary Profile 예시**: `apt29.json`은 T1078(Valid Accounts) -> T1059.001(PowerShell) -> T1003.001(LSASS Dump) -> T1021.002(SMB Lateral) -> T1041(C2 Exfil) 5단계 자동 오케스트레이션

- **📢 섹션 요약 비유**: 레드팀은 "도둑 역할의 소방관 훈련용 연기 발생기", 블루팀은 "연기 감지하는 연기 감지기 + 스프링클러", 퍼플팀은 "두 장비를 동시에 시뮬레이션해서 감지기 민감도를 1초 단위로 튜닝하는 관제사"입니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Red Team (침투 테스트 진화형)** | **Blue Team (SOC 운영형)** | **Purple Team (협업·자동화형)** |
| :--- | :--- | :--- | :--- |
| **목적** | 공격자 관점의 리스크 실증, 익스플로잇 가능성 검증 | 탐지·대응·복구의 운영 효율성 극대화 | 양 팀의 지식·자동화·메트릭 통합 |
| **주 사용 프레임워크** | TIBER-EU, CBEST, PTES, OWASP WSTG, NIST SP 800-115 | NIST CSF 2.0(DE/RS/RC), MITRE D3FEND, SOC-CMM | MITRE ATT&CK + D3FEND 매핑, CARTA(Gartner), Vectr/Plextrac |
| **시나리오 소스** | 위협 인텔리전스(APT29, Lazarus, FIN7) 기반 Adversary Emulation | MITRE ATT&CK Top 20, 내부 위협 헌팅 가설 | ATT&CK Navigator Heatmap, BAS 도구 결과 |
| **도구 (대표 3개)** | Cobalt Strike(상용), Sliver(오픈소스), MITRE Caldera(오픈소스) | Splunk/Elastic SIEM + CrowdStrike/SentinelOne EDR + XSOAR/Tines SOAR | AttackIQ/SafeBreach(BAS), Vectr(통합 대시보드), Stratus Red Team |
| **측정 KPI** | 침투 성공률, Critical 자산 도달 시간, 데이터 유출 시뮬레이션 | MTTD, MTTR, 알림 처리량, Tier 1~3 에스컬레이션 비율 | Detection Coverage %, Time-to-Detect-Gap, False Negative Rate, Purple Cycle Time |
| **소요 시간/주기** | 연 1~4회, 프로젝트당 4~12주 | 24/7 상시 운영 + 월간 hunt | Sprint 주제(2~4주) + 지속적 자동화 검증 |
| **법적 책임** |