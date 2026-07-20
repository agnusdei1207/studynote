---
title: "Sre Philosophy"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 121
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SRE(Site Reliability 엔진ering)는 Google이 정립한 <strong>소프트웨어 엔지니어링으로 운영 문제를 해결</strong>하는 철학이며, "운영을 소프트웨어 문제로 다루겠다"는 원칙 아래 <strong>SLI/SLO/Error Budget</strong>으로 신뢰성을 정량 관리한다.
> 2. **가치**: 전통 Ops는 "장애 없이 100% 가용"을 목표로 하지만, SRE는 <strong>"100%는 잘못된 목표"</strong>라고 선언하고, Error Budget(허용 가능 장애 시간)을 활용하여 <strong>신뢰성과 혁신 속도의 균형</strong>을 유지한다.
> 3. **판단 포인트**: SLI(측정 지표)->SLO(목표 임계치)->Error Budget(남은 여유)->SLA(계약)의 계층 구조를 이해하고, Error Budget이 소진되면 <strong>피처 개발을 중단하고 신뢰성 개선에 집중</strong>하는 정책이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    SRE 핵심 계층                                      |
+-------------------------------------------------------+
|  SLI (Service Level Indicator)                        |
|   -> 측정: 요청 성공률, p99 레이턴시                   |
|                                                       |
|  SLO (Service Level Objective)                        |
|   -> 목표: 성공률 ≥ 99.9% (30일 기준)                |
|                                                       |
|  Error Budget = 100% - SLO = 0.1%                     |
|   -> 30일 × 0.1% = 43.2분의 장애 허용                |
|   -> 43.2분 소진 -> 피처 개발 중단, 안정화 집중!       |
|                                                       |
|  SLA (Service Level Agreement)                        |
|   -> 고객과의 계약 (SLO 미달 시 크레딧/위약금)        |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Error Budget은 매월 주어지는 <strong>용돈(43분)</strong>이다. 장애가 나면 용돈이 줄고, 다 쓰면 <strong>새 장난감(피처) 구매 금지(개발 중단)</strong>, 안정화에 집중해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SRE vs DevOps

| 비교 | DevOps | SRE |
|:---|:---|:---|
| **관점** | 문화·협업 | **구체적 구현 방법** |
| <strong>신뢰성</strong> | 정성적 | <strong>SLI/SLO 정량적</strong> |
| **운영** | 자동화 지향 | **소프트웨어로 해결** |
| <strong>관계</strong> | 철학 | **DevOps의 구체적 구현** |

### Toil 제거
- <strong>Toil</strong>: 수동·반복적·자동화 가능한 운영 작업.
- SRE 엔지니어는 <strong>Toil을 50% 미만으로 유지</strong>하고 나머지는 자동화·엔지니어링에 투자.

- **📢 섹션 요약 비유**: Toil은 매일 손으로 빨래하는 것이고, SRE는 세탁기(자동화)를 만들어 빨래 시간을 줄이고 나머지 시간에 새 옷(피처)을 만드는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 Ops | SRE |
|:---|:---|:---|
| **목표** | 100% 가용 | <strong>SLO (99.9% 등)</strong> |
| **장애** | 무조건 나쁨 | <strong>Error Budget 내면 OK</strong> |
| **혁신** | 변경 회피 | **Budget 내 혁신 장려** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### SRE 핵심 도서
- <strong>"Site Reliability 엔진ering"</strong> (Google, 2016): SRE 바이블.
- <strong>"The Site Reliability Workbook"</strong> (2018): 실무 가이드.

---

## Ⅴ. 기대효과 및 결론

SRE는 <strong>"완벽한 가용성은 잘못된 목표"</strong>라는 혁명적 관점으로, Error Budget을 통해 신뢰성과 혁신의 균형을 정량적으로 관리하는 현대 운영의 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>SLI</strong> | 서비스 수준 지표 (측정) |
| <strong>SLO</strong> | 서비스 수준 목표 (임계치) |
| <strong>Error Budget</strong> | 허용 장애 시간 (혁신 vs 안정) |
| <strong>Toil</strong> | 수동·반복 운영 작업 (제거 대상) |
| <strong>SLA</strong> | 고객과의 계약 (SLO 기반) |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 운영 (NOC, 100% 가용 목표, ~2000s)]
    |
    v
[DevOps 문화 (2009~) — Dev+Ops 협업]
    |
    v
[SRE (Google, 2003->2016 공개) — SLI/SLO/Error Budget]
    |
    v
[Platform Engineering (2022~) — SRE + 내부 개발자 플랫폼]
    |
    v
[현재: AIOps + SRE — AI 기반 자동 인시던트 대응]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SRE는 <strong>용돈(Error Budget)</strong>을 매달 받는 거예요. 장애가 나면 용돈이 줄어요.
2. 용돈이 다 떨어지면 <strong>새 장난감(피처) 사는 건 잠시 멈추고</strong> 안전(안정화)에 집중해요.
3. 덕분에 **너무 많이 놀지도(장애), 너무 공부만 하지도(변경 회피) 않는** 균형을 유지해요!
