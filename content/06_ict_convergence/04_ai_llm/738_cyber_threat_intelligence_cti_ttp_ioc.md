---
title: "Cyber Threat Intelligence CTI TTP IOC"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 738
---
```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CTI는 위협 데이터를 "방향성(Planning) -> 수집(Collection) -> 가공(Processing) -> 분석(Analysis) -> 배포(Dissemination) -> 피드백(Feedback)"의 6단계 라이프사이클으로 순환시키는 체계이며, TTP는 MITRE ATT&CK 매트릭스(14개 Tactic, 200+ Technique)로 공격자의 행동 패턴을 표준화한 지식 체계, IOC는 Atomic(파일해시·IP·도메인) / Computed(fuzzy hash·sandbox 트리거) / Behavioral(프로세스 트리·레지스트리 변이) 3계층으로 분류된 침해 흔적의 기계 판독 가능한 디지털 증거이다.
> 2. **가치**: MISP + STIX 2.1 + TAXII 2.1 기반의 위협 인텔리전스 플랫폼(TIP)을 SIEM/SOAR/XDR에 연동할 경우 평균 탐지시간(MTTD) 약 63%, 평균 대응시간(MTTR) 약 48% 단축이 가능하며(IBM 2024 Cost of a Data Breach 기준), TTP 기반 헌팅은 IOC 단편 탐지 대비 신규 변종 0-day 공격에 대한 예측 탐지력을 3.2배 향상시킨다.
> 3. **판단 포인트**: ①상업용 피드(Recorded Future, Mandiant) vs 오픈소스(MISP, OTX) vs 내부 CTI의 3-way 혼합 비율, ②STIX 2.1의 Cyber Observable (SCO) / Indicator (SDO) / Relationship (SRO) 객체 모델 채택 여부, ③SIEM/SOAR 통합 시 TAXII 2.1 Discovery/Collection API의 rate-limit·인증서·OAuth 2.0 토큰 운영 정책, ④TTP 매핑 시 MITRE ATT&CK Navigator JSON v4 layer 포맷의 표준화 수준이 핵심 결정 변수이다.

---

## Ⅰ. 개요 및 필요성

시그니처 기반 탐지(Anti-Virus, IPS 룰)는 2010년 이후의 APT(Advanced Persistent Threat) 및 공급망 공격(SolarWinds SUNBURST 2020, 3CX Supply Chain 2023, XZ Utils Backdoor CVE-2024-3094)에서 한계가 명확히 드러났다. 공격자는 Living-off-the-Land Binary(PSExec, WMIC, PowerShell)·공인 M&A(M&A)인증서 서명·공급망 단계 멀웨어 삽입으로 정적 해시·IP 블랙리스트를 무력화한다. 이에 따라 방어 패러다임은 "이미지 단편의 IOC"에서 "공격자 행동의 TTP"로 이동해야 했으며, 이를 위해 ①STIX 2.1/TAXII 2.1로 표현·교환되는 위협 인텔리전스, ②MITRE ATT&CK으로 분류되는 TTP, ③YARA/Sigma/Snort 룰로 가공되는 IOC의 3축 통합 체계가 필요하다.

```text
[ 전통 시그니처 기반 탐지 vs CTI·TTP·IOC 통합 탐지의 패러다임 비교 ]

   +--------------------------+            +------------------------------+
   |  Legacy: Signature-Based |            |  Modern: CTI-Driven Defense  |
   +--------------------------+            +------------------------------+
   |                          |            |                              |
   |  Malware Hash -----> AV   |            |  External CTI --+            |
   |  Black IP   -----> FW     |            |  (STIX/TAXII)   |            |
   |  Known URL  -----> WAF    |            |                 v            |
   |  (정적 룰)                |            |  +----------------------+    |
   |                          |            |  |  Threat Intel Plat.  |    |
   |  ✗ Polymorphic 변종 무력 |            |  |  (MISP, ThreatQ,     |    |
   |  ✗ LOLBins 우회 무력     |            |  |   Anomali)           |    |
   |  ✗ M&A 코드서명 우회 무력|            |  +----------+-----------+    |
   |  ✗ Supply Chain 위장 무력|            |             | correlation    |
   |                          |            |             v               |
   |                          |            |  TTP: ATT&CK T1566.001      |
   |                          |            |        (Spearphishing)       |
   |                          |            |  IOC: SHA-256, C2 도메인,    |
   |                          |            |        YARA 룰, Sigma 룰     |
   |                          |            |             |               |
   |                          |            |             v               |
   |                          |            |  SIEM -> SOAR -> XDR 자동화   |
   |                          |            |  (탐지 -> 분석 -> 격리/차단)   |
   |                          |            |  (MTTD 63%v, MTTR 48%v)   |
   |                          |            |                              |
   |  한계: Known-Bad만 탐지  |            |  강점: Unknown-Threat 예측  |
   +--------------------------+            +------------------------------+
```

**필요성의 3대 배경**:
1. **공격자 비대칭의 해소**: 1,000명 이상의 위협 그룹(예: Lazarus, APT29, Kimsuky, FIN7)이 활동하며 공격 비용은 0에 수렴하지만 방어자는 모든 공격 경로를 차단해야 하는 비대칭을, 공유 인텔리전스로 분담한다.
2. **제로트러스트 + XDR 시대의 맥락화**: 디바이스·ID·네트워크·클라우드 로그를 단일 위협 그래프(Threat Graph)로 통합할 때 TTP 컨텍스트가 correlation의 핵심 차원이 된다.
3. **규제/컴플라이언스 요구**: K-ISMS-P(2024 개정), NIST SP 800-150(Guide to Cyber Threat Information Sharing), ISO/IEC 27027, 금융보안원 "금융회사 사이버보안 안전 가이드" 등에서 위협 정보 공유를 통제 항목으로 명시.

- **📢 섹션 요약 비유**: 시그니처 기반 탐지는 "이전에 본 현상범 사진"으로만 수배하는 것이고, CTI는 "CCTV·핏자국·지문·목격담"까지 모은 종합 수사 자료집이다. TTP는 "범인의 MO(수법 패턴)"이고 IOC는 "현장에 남긴 핏자국"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
[ CTI 처리·배포 아키텍처 (End-to-End) ]

                          +--------------------------------------+
                          |        외부/내부 위협 소스             |
                          |  • ISAC·CERT (KISA, KrCERT, FIRST)   |
                          |  • 상업용: Recorded Future, Mandiant  |
                          |  • 오픈소스: MISP, OTX, AbuseIPDB     |
                          |  • 내부: SIEM/EDR/XDR 로그, Honeypot |
                          |  • 다크웹: S2W DarkBERT, Intel471    |
                          +------------------+-------------------+
                                             | STIX 2.1 Bundle
                                             | (JSON over TAXII 2.1)
                                             v
   +--------------------------------