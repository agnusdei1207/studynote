---
title: "Cyber Security Threat Intelligence CTI"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 698
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사이버 위협 인텔리전스(CTI)는 MITRE ATT&CK 프레임워크 기반의 TTP(Tactics, Techniques, Procedures), IoC(Indicators of Compromise: IP, 도메인, 파일 해시, YARA 룰), IoA(Indicators of Attack) 데이터를 STIX(Structured Threat Information eXpression) 2.1/TAXII(Trusted Automated eXchange of Intelligence Information) 2.1 표준으로 구조화하여, 위협 행위자(Threat Actor)의 의도·역량·기회(Intrusion Set) 간의 인과관계를 명세화한 증거 기반 의사결정 체계이다.
> 2. **가치**: CTI 운영 성숙 조직은 평균 탐지 시간(MTTD)을 21일에서 4시간 이내로 99% 단축하고, 사고 대응 비용을 $1.4M 절감하며(Cost of a Data Breach Report 2023), SOC 분석가의 Tier-1 알림 트리아지 시간을 약 70% 감소시켜, 사전 예방적 방어(Proactive Defense) 및 위협 헌팅(Threat Hunting) 역량으로 ROI를 확보한다.
> 3. **판단 포인트**: 전략적(Strategic)/운영적(Operational)/전술적(Tactical)/기술적(Technical) 4계층 인텔리전스 간의 디스클로저 정책(FBI/NSA 같은 Traffic Light Protocol: TLP:RED/AMBER/GREEN/CLEAR) 적용, 상업용 피드(Recorded Future, Mandiant, CrowdStrike) vs 오픈소스(MISP, AlienVault OTX) vs ISAC(Information Sharing and Analysis Center) 정보원의 트러스트 스코어링, 그리고 SIEM·SOAR·EDR·WAF·IPS·NDR과의 양방향 액션 가능한 통합(ACI: Actionable Cyber Intelligence) 설계가 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

전통적인 시그니처 기반 보안(Anti-Virus, Snort IDS 룰, YARA 룰)은 2010년 Stuxnet, 2017년 WannaCry/EternalBlue, 2020년 SolarWinds SUNBURST(UNC2452) 사건 이후, **제로데이·파일리스(Fileless)·LOLBins(Living Off the Land Binaries)·공급망 공격(Supply Chain Attack)**에 무력함이 증명되었다. 공격자는 멀티스테이지 킬체인(Kill Chain: Reconnaissance->Weaponization->Delivery->Exploitation->Installation->C2->Actions on Objectives)을 통해 평균 277일 이상潜伏(Lateral Movement)하며, 시그니처가 없는 행동 패턴과 정상 트래픽으로 위장한 C2(Command & Control) 통신을 수행한다.

이에 따라 **"알려진 위협(known-knowns)"에서 "예측 가능한 위협(known-unknowns)", 나아가 "발굴 가능한 위협(unknown-unknowns)"**으로 패러다임이 전환되었고, Gartner는 2026년까지 기업의 60%가 위협 인텔리전스 기능을 도입할 것으로 예측한다. CTI는 단순 위협 정보 공유를 넘어, **위협 기반 방어(Threat-Informed Defense)**, **공격자 관점의 적색팀(Red Team) 에뮬레이션(Breach and Attack Simulation: BAS)**, **헌팅 가설(Hypothesis-Driven Hunting)**의 기초 데이터를 제공하는 전략 자산으로 격상되었다.

```text
[전통 보안 vs 위협 인텔리전스 기반 보안의 패러다임 비교]

  +--------------------------+         +--------------------------+
  |   Signature-Based        |         |   Threat Intelligence    |
  |   (Reactive)             |   ---►  |   Based Defense          |
  |                          |  Shift   |   (Proactive)            |
  +--------------------------+         +--------------------------+

  1) 탐지 원천                    1) 탐지 원천
     - 자체 로그/시그니처              - 외부 위협 피드(Commercial)
     - IDS/IPS 룰셋                 - 오픈소스 위협 정보(OSINT)
                                   - ISAC/공공 위협 정보
                                   - 다크웹/크림마켓 모니터링

  2) 분석 패러다임                 2) 분석 패러다임
     - 단일 이벤트 매칭              - TTP 상관관계 분석
     - 알려진 악성코드 해시          - 행위 기반 베이스라인
     - 정적 룰 평가                 - 헌팅 가설 검증
                                   - 위협 헌팅(Proactive Hunt)

  3) 대응 방식                     3) 대응 방식
     - 룰 업데이트 후 대응           - 위협 행위자별 IOC 차단
     - 사고 후 사후 분석             - 예측 차단(Hunt & Block)
                                   - DECIDE->DETECT->DENY
                                     ->DISRUPT->DEGRADE->DECEIVE
                                     (D3FEND 프레임워크)

  [CTI 도입의 3대 동인]
  +------------------------------------------+
  | 1) Zero-Day/공급망 공격 대응력 강화      |
  | 2) 규제 준수: 보안공시(공정거래법),      |
  |    개인정보보호법, ISMS-P, PCI-DSS       |
  | 3) SOC 효율화: 알림 피로(Alert Fatigue)  |
  |    해소 및 분석가 1인당 처리량 향상      |
  +------------------------------------------+
```

- **📢 섹션 요약 비유**: CTI는 마치 **"전염병 감시 시스템(KOID·KCDC)"**과 같다. 각 병원에서 환자가 발생하면 증상·바이러스 타입을 WHO에 보고하고, 이를 토대로 국민들에게 예방접종·마스크 권고를 내리듯, 전 세계 보안 조직에서 악성코드·C2 IP·해킹 그룹 정보를 공유·분석하여 **우리 조직에 예방 차원의 차단 정책(Threat Intel-driven Blocklist)**을 자동 배포하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CTI 라이프사이클은 Gartner의 6단계 모델(Direction -> Collection -> Processing -> Analysis -> Dissemination -> Feedback)로 구성되며, OASIS CTI TC가 표준화한 **STIX 2.1 Domain Objects(SDO)**: `Indicator`, `Malware`, `Threat Actor`, `Intrusion Set`, `Campaign`, `Attack Pattern`, `Tool`, `Infrastructure`, `Vulnerability`와 **STIX Cyber-observable Objects(SRO)**: `IPv4-Addr`, `Domain-Name`, `File`, `URL`, `Email-Addr`, `Windows-Registry-Key` 간의 관계(`Relationship Object`)로 표현된다.

```text
[CTI 플랫폼(TIP) 아키텍처 및 데이터 흐름 상세도]

  +-------------------------------------------------------------+
  |                  [외부 위협 정보원 (Sources)]                |
  |                                                              |
  |  +------------+  +------------+  +------------+  +--------+|
  |  | Commercial |  |   OSINT    |  |   ISAC     |  | 내부   ||
  |  | Feeds      |  | (Twitter/X |  |  ·FS-ISAC  |  | 티어2  ||
  |  | ·Mandiant  |  |  GitHub    |  |  ·KISA     |  | 분석   ||
  |  | ·Recorded  |  |  AbuseIPDB |  |  ·KrCERT   |  | 결과   ||
  |  |  Future    |  |  VirusTotal|  |  ·금융보안원|  |        ||
  |  +-----+------+  +-----+------+  +-----+------+  +---+----+|
  |        |               |               |              |     |
  |        +---------------+---------------+--------------+     |
  |                          | TAXII 2.1 / STIX 2.1            |
  |                          | (HTTPS + JSON+JWT, 5061/tcp)     |
  |                          v                                   |
  |  +-------------------------------------------------------+ |
  |  |   [수집 계층: Collection Engine]                       | |
  |  |   - TAXII Server (poll channel, push channel)        | |
  |  |   - RSS/Atom, Email (.eml -> STIX 변환), RSS, MISP    | |
  |  |   - RSS/REST API -> Flume/Kafka                       | |
  |  +---------------------+---------------------------------+ |
  |                        v                                     |
  |  +-------------------------------------------------------+ |
  |  |   [처리 계층: STIX/TAXII 정규화 파이프라인]           | |
  |  |   - cti-taxii-server, cti-stix-elevator               | |
  |  |   - MISP Core / PyMISP (correlate event)              | |
  |  |   - STIX2 Python lib -> STIX 1.x -> 2.1 마이그레이션   | |
  |  +---------------------+---------------------------------+ |
  |                        v                                     |
  |  +-------------------------------------------------------+ |
  |  |   [분석 계층: TIP(Threat Intelligence Platform)]      | |
  |  |   - MISP, OpenCTI, ThreatConnect, Anomali            | |
  |  |   - 관계 그래프(Neo4j) · 상관관계 룰                 | |
  |  |   - 중복 제거, 신뢰도 스코어링(0~100), 컨텍스트 태깅 | |
  |  +---------------------+---------------------------------+ |
  |                        |                                     |
  |                        v                                     |
  |  +-------------------------------------------------------+ |
  |  |   [배포 계층: Actionable Integration]                | |
  |  |   - SIEM: Splunk ES (STIX app), QRadar, Elastic      | |
  |  |   - SOAR: Cortex XSOAR, Splunk SOAR (Phantom)        | |
  |  |   - EDR: CrowdStrike Falcon, SentinelOne, Wazuh      | |
  |  |   - NDR: Vectra AI, Darktrace, Corelight             | |
  |  |   - Firewall/IPS: Palo Alto, Fortinet, Cisco Firepower| |
  |  |   - DNS: RPZ(Response Policy Zone), Cisco Umbrella   | |
  |  +-------------------------------------------------------+ |
  +-------------------------------------------------------------+

  [CTI 라이프사이클 6단계 (NIST SP 800-150)]
  +------------+   +------------+   +------------+
  | Direction  |--►| Collection |--►| Processing |
  | (우선순위)  |   | (수집)     |   | (정규화)   |
  +-----+------+   +-----+------+   +-----+------+
        v                v                v
  +------------+   +------------+   +------------+
  |  Feedback  |◄--|Disseminat. |◄--|  Analysis  |
  |  (피드백)  |   | (배포)     |   |  (심층분석)|
  +------------+   +------------+   +------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **위협 정보원 (Threat Source)** | 원시 데이터 제공 | Commercial(Recorded Future, Mandiant, CrowdStrike Falcon Intel, Digital Shadows), OSINT(MISP, AlienVault OTX, VirusTotal Graph, AbuseIPDB, Shodan), ISAC(FS-ISAC, H-ISAC, KISA/한국인터넷진흥원, 금융보안원), 내부 분석 결과(Incident Report) |
| **수집 엔진 (Collection)** | TAXII/STIX/REST API/Email로 데이터 수신 | TAXII 2.1(HTTPS 기반 poll/push 채널, `taxii2-client` Python lib, 인증은 JWT Bearer), RSS/Crawler, MISP `PyMISP` API, Kafka/NiFi 스트리밍 |
| **처리·정규화 (Processing)** | 비정형->STIX 2.1 JSON 변환, 중복 제거, 신뢰도 부여 | `cti-stix-elevator`(1.x->2.1 변환), MISP Galaxy(Threat Actor, Tool 클러스터 매핑), Levenshtein/Fuzzy Hashing(ssdeep, tlsh) 중복 제거, TLP 자동 태깅 |
| **분석·맥락화 (Analysis)** | TTP·인물·인프라·캠페인 관계 추론 | MITRE ATT&CK(Enterprise/ICS/Mobile) 매핑, Diamond Model 분석(Adversary·Capability·Infrastructure·Victim), Pyramid of Pain(Hashes->IP->Domain->Artifacts->TTP), 그래프 DB(Neo4j, OpenCTI) |
| **배포 채널 (Dissemination)** | SIEM/SOAR/EDR/네트워크 장비에 액션 가능한 형태로 전송 | STIX 2.1 Bundle -> SIEM lookup table, SOAR playbook trigger(예: Splunk SOAR의 `phantom.cti.update`), EDR IOC 차단, DNS RPZ zone, Firewall deny rule 자동 배포 |
| **피드백 (Feedback)** | 인텔리전스 정확도 측정, 재조정 | KPI: 정확도(Precision), 재현율(Recall), IoC 유효기간(half-life), False Positive Rate, 분석가 활용도, MTTD/MTTR |

**Pyramid of Pain (David Bianco)**: 단순 해시(쉬움)->IP 주소(어려움)->도메인(더 어려움)->네트워크/호스트 아티팩트(매우 어려움)->**TTP(가장 어려움)** 순으로, 상위 단계가 공격자에게 더 큰 비용을 부과한다. CTI는 상위 TTP 단계의 탐지에 집중해야 한다. 예: Lazarus Group(추정 DPRK)의 "AppleJeus" 캠페인은 T1486(Data Encrypted for Impact), T1059(Command and Scripting Interpreter), T1071(Application Layer Protocol: HTTPS) 등 ATT&CK Technique ID로 명세화한다.

- **📢 섹션 요약 비유**: CTI 파이프라인은 **"국제형사경찰(Interpol) 공조 시스템"**과 같다. 각국 경찰(외부 위협 정보원)이 용의자 명세(STIX 객체)를 표준 양식(STIX 2.1)으로 본부에 보내면, 본부는 데이터베이스(TIP)에서 기존 사건과 교차 조회(상관관계) 후, 수배차·차단 목록(Actionable)을 전 세계 지부(SIEM/SOAR/EDR)에 즉시 배포한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **CTI (Threat Intelligence)** | **SIEM (Security Information & Event Management)** | **SOAR (Security Orchestration, Automation & Response)** | **EDR (Endpoint Detection & Response)** |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | 위협 정보 수집·맥락화·예측 | 로그 수집·상관규칙 탐지 | 사고 대응 자동화·오케스트레이션 | 엔드포인트 행위 탐지·포렌식 |
| **데이터 형태** | STIX 2.1/TAXII 2.1, IoC, TTP | 로그(Syslog, CEF, LEEF), 이벤트, 플로우 | Playbook(DSL: YAML/JSON), 케이스 티켓 | 프로세스 트리, 파일 이벤트, 메모리 덤프 |
| **주요 기능** | 위협 정보 통합·스코어링·맥락화 | 실시간 상관분석·이상탐지·대시보드 | 자동 티켓 생성·격리·사용자 통지 | 행위기반 탐지·원격 포렌식·격리 |
| **대표 제품** | MISP, OpenCTI, ThreatConnect, Anomali, Recorded Future, Mandiant