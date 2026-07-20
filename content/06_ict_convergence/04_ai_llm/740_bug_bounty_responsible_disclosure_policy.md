---
title: "Bug Bounty Responsible Disclosure Policy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 740
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 버그 바운티와 책임 있는 공개(Responsible Disclosure) 정책은 ISO/IEC 29147(취약점 공개)·30111(취약점 처리) 표준을 기반으로, 외부 보안 연구자와 조직 간 **CVD(Coordinated Vulnerability Disclosure)** 라이프사이클을 협업적으로 운영하여 위협을 사전에 무력화하는 구조화된 취약점 관리 프레임워크임.
> 2. **가치**: Google·Microsoft·Apple 사례 기준 버그 바운티 참여 시 평균 **Critical 취약점 탐지 비용이 침투 테스트 대비 1/10 이하**, 평균 패치 적용 소요 시간 **37일 단축**, 외부 연구자 풀 확장으로 취약점 발견 커버리지를 **3~5배** 확대 가능하며, 법적 Safe Harbor 조항을 통해 연구자·조직 모두의 리스크를 동시 해소함.
> 3. **판단 포인트**: 공개 시점(90일 정책 vs 무제한 협의), 보상 등급 체계 설계(Tier 1~5, Critical 기준 $5,000~$250,000), In-Scope/Out-of-Scope 자산 경계 정의의 명확성, NDA·Safe Harbor·법적 면책 조항의 정합성, 그리고 기존 SOC·SIEM·VMS(Vulnerability Management System)와의 통합 거버넌스가 핵심 의사결정 요소임.

---

## Ⅰ. 개요 및 필요성

전통적 사이버 보안은 **내부 침투 테스트(Internal Pentest)**, **내부 Red Team**, 그리고 **Vendor Security Assessment**로 구성되어 왔으며, 이는 조직 내부 인력의 지식·경험 범위 안에서만 위협 시나리오를 발굴한다는 구조적 한계를 가진다. 그러나 2020년 이후 SolarWinds, Log4j, MOVEit과 같은 **공급망 공격(Supply Chain Attack)**과 **제로데이 취약점의 블랙마켓 거래**(제로데이 브로커인 Zerodium·CrowdStrike Intelligence 등의 시장 가격이 iOS RCE 기준 **$2.5M ~ $7M**에 육박) 증가로, 내부 진단만으로는 평균 **0-day exploit 공개 후 287일 이내**에 발생하는 대규모 피해를 예방할 수 없게 되었다.

이에 Google이 2010년 **Vulnerability Reward Program(VRP)**을 최초 상용화하고, 이후 Facebook(2011), Microsoft(2013), Apple(2016)이 차례로 도입하면서, **Crowdsourced Security** 모델이 글로벌 보안 전략의 표준으로 자리잡았다. 한국에서는 2023년 금융보안원이 **금융권 버그바운티**를, 과학기술정보통신부가 2024년 **주요정보통신기반시설 대상 버그바운티 가이드라인**을 발표하며 본격 도입이 가속화되었다.

```text
[기존 패러다임: 폐쇄형 보안 진단]                    [새로운 패러다임: 협업형 취약점 헌팅]
+----------------------+                            +------------------------------------+
|  내부 Red Team       |   ---> 한계 도달 --->         |  전 세계 40만+ 화이트해커            |
|  (5~20명, 연 2회)    |                            |  (HackerOne: 600만+ 연구자 등록)   |
+----------+-----------+                            +------------------+-----------------+
           |                                                       |
           v                                                       v
   +--------------+                                     +---------------------+
   |  알려진      |                                     |   In-Scope 자산     |
   |  공격벡터    |                                     |   • Web/API/Mobile  |
   |  중심 탐지   |                                     |   • IoT/펌웨어      |
   +--------------+                                     |   • Cloud/K8s      |
                                                        |   • AI/LLM         |
                                                        +----------+----------+
                                                                   |
   +--------------+                                     +----------v----------+
   |  침묵의 패치 | <---- 기존                             |  Triage -> Patch ->   |
   |  (블랙박스)  |      CVE 미공개 시                   |  Coordinated Public |
   +--------------+                                     |  Disclosure         |
                                                        +---------------------+
```

책임 있는 공개 정책은 단순히 "보상금을 주는 제도"가 아니라, **연구자의 익명성·법적 안전**, **조직의 자산 보호 의무**, **사용자의 안전 권리**, **CVE 발행·CVSS 스코어링**, 그리고 **국가 CERT·CSIRT 연계**까지 포괄하는 **Governance 체계**다. 이를 등한시할 경우, 연구자가 자신의 취약점 발견을 Twitter·GitHub 등에 즉시 게시하는 **Full Disclosure**로 이어져, 패치 적용 전 공격자에게 **N-day Exploit 제작 시간**을 제공하게 되는 최악의 시나리오가 발생한다.

- **📢 섹션 요약 비유**: 마치 "우리 아파트의 하자"를住户들이 직접 찾아보고, 시공사·관리사무소가 함께 보수를 진행한 뒤, 합리적인 시점에 하자 보수 내역서를 공개하는 **하자 보수 신고제도와 헌장**과 같다. 무작정 TV에 "이 아파트 균열 있어요!"라고 외치는 것과 정반대 접근이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

책임 있는 공개 정책과 버그 바운티 시스템은 5-Tier 아키텍처로 구성되며, 각 계층은 명확한 책임 분배와 SLA(Service Level Agreement)를 통해 운영된다.

```text
                       +-----------------------------------------+
                       |  Tier 5: 공개(Public Disclosure) 단계  |
                       |  • CVE 발급 / Mitre 등록               |
                       |  • Security Advisory 게시               |
                       |  • 패치 배포 완료 확인 후 7~30일        |
                       +----------------+------------------------+
                                        |
+----------------------+   +-------------v--------------+   +--------------------+
|  Tier 0:             |   |  Tier 2: Triage/검증       |   |  Tier 4: 패치 및    |
|  헌장·정책 수립 단계  |--->|  • 보고서 신뢰도 평가      |--->|  재발 방지 단계     |
|  • security.txt      |   |  • 재현(Reproduction) 검증 |   |  • 코드 패치        |
|  • /.well-known/     |   |  • 영향도 분석(CVSS 4.0)  |   |  • WAF 룰 적용      |
|  • CoC(Code of       |   |  • 내부 보안팀 에스컬레이션|   |  • 회귀 테스트      |
|    Conduct) 정의      |   +-------------+--------------+   +--------------------+
+----------------------+                 |
        ^                                v
+--------------------------------------------------------------------+
|  Tier 1: 접수(Ingestion) 단계                                       |
|  • HackerOne / Bugcrowd / Intigriti / 자체 플랫폼                 |
|  • PGP 암호화 채널 / Signal / ProtonMail                           |
|  • 다중 채널 보안: HackerOne + Email + Signal + Bug Bounty Portal |
+--------------------------------------------------------------------+
        ^                                ^
        |                                |
+-------+--------+               +-------+---------+
| 외부 연구자     |               | 내부 자발적      |
| (Ethical       |               | 신고자           |
|  Hacker)       |               | (Internal       |
|                |               |  Whistleblower) |
+----------------+               +-----------------+
```

### 핵심 구성 요소 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **security.txt (RFC 9116)** | 표준화된 정책 진입점 | `https://example.com/.well-known/security.txt` 경로에 `Contact`, `Encryption`, `Expires`, `Preferred-Languages`, `Canonical`, `Policy` 필드 정의. 최소 1년 주기 갱신. Google, Facebook, Microsoft 모두 준수. |
| **Triage Pipeline** | 보고서 우선순위·신뢰도 판정 | 자동화 스크리닝(중복 검사, CWE 매핑, PoC 정적 분석) -> 1차 Triage(인니어, SLA: 24~48h) -> 2차 Validation(Senior Researcher, SLA: 5 영업일) -> Critical/High는 24h 내 온콜 에스컬레이션. Google Median Time-to-Triage: **6 hours 21 minutes (2023)**. |
| **보상 산정 엔진 (Reward Calculation Engine)** | CVSS 4.0 기반 등급별 보상 산출 | `Base Score × Asset Criticality × Exploitability Factor × Report Quality Bonus` 공식. 예: Critical RCE in Production = `$30,000` (기본) + `$10,000` (제목 asset) + `$5,000` (Chain Bonus). HackerOne Median Bounty: **$500**, Microsoft Max: **$100,000**, Apple Max: **$2,000,000** (2024년 11월 신규 인상). |
| **Safe Harbor 조항** | 연구자 법적 보호 | DMCA 1201(i) 예외, CFAA Anti-Trafficking 면책, EU NIS2 Directive Article 12 "Proactive Security Research" 보호, 한국 정보통신망법·형사정책국 가이드라인 준수. Google의 **"Don't be evil" 정책**처럼 명시적 "Good Faith" 정의 필수. |
| **CVE·CWE 발행 매핑** | 표준화된 취약점 분류 | MITRE CVE Authority에 CNA( CVE Numbering Authority )로 등록하여 자체 발행. CWE(Common Weakness Enumeration)로 `CWE-79(XSS)`, `CWE-89(SQLi)`, `CWE-94(Code Injection)`, `CWE-502(Deserialization)`, `CWE-787(Out-of-bounds Write)` 등 분류. CVSS 4.0 벡터로 영향도 정량화. |
| **Disclosed Status 관리기** | 공개·미공개·조율 상태 추적 | `Reported -> Triaged -> Accepted -> Disclosed (Public) / Won't Fix / Informative / Duplicate / N/A` 7단계 상태 머신. HackerOne Hacktivity API로 부분 공개(Redacted) 지원. |
| **PR·법무 협의 워크플로우** | 공개 시점·법적 검증 | Critical 취약점의 경우, 패치 배포 -> 30~90일 보유 -> 그 후 Public Advisory. 사안별 고객 통지 의무(GDPR Art.33 72h Rule) 및 SEC 8-K 공시 의무와 정합성 검증. |

### 핵심 알고리즘 및 파라미터: 보상 등급 산정 모델

```
+------------------------------------------------------------------+
|                  Bounty Amount = B × M × Q × C                    |
+------------------------------------------------------------------+
|  B = Base Amount (CVSS 등급별)                                    |
|      Critical(9.0~10.0) : $5,000  / High(7.0~8.9) : $1,500       |
|      Medium(4.0~6.9)    : $500    / Low(0.1~3.9)  : $100         |
|                                                                   |
|  M = Asset Multiplier (자산 중요도)                              |
|      Production Main Domain : ×10 / Staging : ×2 / Dev : ×1      |
|      Mobile App(배포중)     : ×8  / Internal API  : ×5            |
|                                                                   |
|  Q = Quality Bonus (보고서 품질)                                 |
|      PoC + Repro Steps + Impact Description : ×1.5               |
|      Patch Suggestion 포함                    : ×2.0              |
|                                                                   |
|  C = Chain Bonus (연쇄 취약점)                                   |
|      SSRF -> RCE 같은 Attack Chain 구성 시 : ×3.0                  |
|      단일 취약점만                        : ×1.0                  |
+------------------------------------------------------------------+
```

이 모델을 **HackerOne의 실제 사례**에 대입하면, Shopify의 "Bug Bounty Plus" 프로그램에서 보고된 *Shopify Subdomain Takeover + Auth Bypass Chain*은 CVSS 9.8( Base $5,000 ) × Asset 8(Production) × Quality 2.0(Patch 포함) × Chain 3.0 = **$240,000**이 산정되어 실제로 지급된 사례가 있다.

### 시간 정책(Timing Policy)의 핵심 트레이드오프

| 정책 유형 | 정책 명 | 공개 시점 | 적용 사례 | 트레이드오프 |
| :--- | :--- | :--- | :--- | :--- |
| **Hard Deadline** | Google 90-day Policy | 보고 후 정확히 90일 | Google Project Zero | 연구자 만족 ^, 패치 지연 시 영하 노출 |
| **Soft Deadline** | Microsoft "Patch Tuesday" | 다음 Patch Tuesday (주2회) | MSRC | 안정적 배포, 긴급 취약점 대응 늦음 |
| **Negotiated** | HackerOne Disclose | 양측 합의 시 무기한 | 많은 상용 SaaS | 유연성 ^, 분쟁 가능성 ^ |
| **Embargo** | CERT/CC Coordinated | 익명 사전 공개, 패치 후 공개 | 국가 CERT | 정보 통제, 일부 연구자 불만 |

- **📢 섹션 요약 비유**: 의료 시스템의 **"의약품 부작용 보고 및 회수 시스템"**과 같다. 환자가 부작용을 발견하면(연구자), 제약사(Triage)에 신고하고, 임상 검증(Triage)을 거쳐, 회수·대체 의약품 출시(패치), 그리고 의학저널에 사례 보고(공개)까지의 단계적 절차가 규격화되어 있다. 동시에 **"의료진의 선의의 보고는 면책"**이라는 Safe Harbor 조항이 연구자를 보호한다.

---

## Ⅲ. 비교 및 연결

### 유사 개념과의 정밀 비교

| 구분 | 전통적 침투 테스트 (Pentest) | Red Team 운영 | 버그 바운티 + 책임 있는 공개 |
| :--- | :--- | :--- | :--- |
| **실행 주체** | 외부 Vendor(연 1~2회) | 내부 Red Team(연 4~12회) | 전 세계 Crowdsourced 연구자 |
| **탐지 범위** | 의뢰된 스코프 한정 (Black/Grey Box) | TIBER-EU·CBEST 등 시나리오 기반 | In-Scope 자산에 대한 무제한 시간·시도 |
| **지속성** | 단발성 (2~6주) | 캠페인 단위 (1~3개월) | **연중무휴 24/7** 상시 운영 |
| **평균 비용** |