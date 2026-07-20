---
title: "Itsm It Service Management"
date: "2026-04-05"
tags:
  - "studynote-enterprise-systems"
weight: 46
---
> **핵심 인사이트**
> 1. ITSM(IT Service Management)은 IT 서비스를 비즈니스 관점에서 설계·제공·개선하는 통합 접근법 — 기술 운영(Technology Operations)이 아닌 서비스 가치 창출에 초점을 맞추며, ITIL이 사실상 표준 프레임워크를 제공한다.
> 2. ITSM의 핵심 KPI는 MTTR·MTBF·SLA 준수율·FCR — 이 지표들이 IT 서비스 품질을 정량화하며, 개선 목표와 투자 우선순위 결정의 기준이 된다.
> 3. 현대 ITSM은 DevOps·SRE와 통합 — 전통 ITSM의 변경관리는 DevOps CI/CD와 충돌할 수 있으며, "경량 변경 관리(Light-Weight CAB)"와 "자동화된 변경 승인"으로 속도와 안정성을 동시에 확보하는 방향으로 진화하고 있다.

---

## Ⅰ. ITSM 가치 체계

```
ITSM 가치 창출 모델:

전통 IT 관리:
  IT 팀: "인프라 운영, 기술 문제 해결"
  사용자: "IT에 뭔가 이상해요"

  비즈니스와 단절

ITSM 접근:
  IT 팀: "서비스를 통한 비즈니스 가치 창출"
  사용자: "서비스 소비자 (Customer)"

  비즈니스 목표 ↔ IT 서비스 정렬

ITSM 핵심 개념:

서비스 카탈로그 (Service Catalog):
  IT가 제공하는 서비스 목록
  사용자 관점으로 기술

  예:
  - 이메일 서비스 (Microsoft 365)
  - ERP 시스템 접근
  - VPN 연결
  - 노트북 지급

서비스 레벨 관리 (SLM):
  SLA (고객과 합의):
  "이메일 서비스: 99.9% 가용성, 2분 내 이메일 배달"

  OLA (내부 운영 합의):
  "네트워크팀은 이메일 서버 업타임 99.95% 보장"

  UC (외부 계약):
  "Microsoft 365: 99.9% 보장 (MS 공약)"

ITSM 가치 지표:
  TCO 최적화
  서비스 가용성
  사용자 만족도 (CSAT)
  IT 직원 생산성
```

> 📢 **섹션 요약 비유**: ITSM은 IT를 서비스업으로 — 호텔(IT팀)이 단순히 건물 관리가 아니라 투숙객(사용자) 경험을 창출. 서비스 카탈로그는 호텔 서비스 목록!

---

## Ⅱ. 핵심 ITSM KPI

```
ITSM 핵심 성과 지표:

인시던트 관리:
  MTTR (Mean Time To Repair/Restore):
  인시던트 발생 -> 서비스 복구까지 평균 시간
  목표: P1 < 4시간, P2 < 8시간

  MTBF (Mean Time Between Failures):
  장애 간 평균 간격
  목표: MTBF 증가 (= 장애 감소)

  인시던트 재발률:
  동일 원인 재발 비율 (문제 관리 효과)
  목표: < 10%

서비스 데스크:
  FCR (First Contact Resolution):
  첫 접촉에서 해결된 비율
  목표: 70%+

  백로그 (Backlog):
  미해결 티켓 수 (증가하면 이상)

  CSAT (Customer Satisfaction):
  사용자 만족도 설문
  목표: 4.2/5.0+

변경 관리:
  변경 성공률:
  총 변경 중 장애 없이 성공한 비율
  목표: 95%+

  긴급 변경 비율:
  전체 변경 중 긴급 비율
  목표: < 5% (높으면 계획 부재 신호)

SLA:
  SLA 준수율:
  목표 SLA 달성 비율
  목표: 99%+ (P1 SLA)

가용성:
  서비스 가용성 =
  (합의 서비스 시간 - 다운타임) / 합의 서비스 시간 × 100%
  99% = 월 7.2시간 다운타임
  99.9% = 월 43분
```

> 📢 **섹션 요약 비유**: ITSM KPI는 배달 서비스 지표 — MTTR(배달 지연 해결 시간), MTBF(배달 사고 간격), FCR(첫 전화로 해결), CSAT(고객 별점)!

---

## Ⅲ. ITSM과 DevOps 통합

```
전통 ITSM vs DevOps 충돌:

전통 ITSM 변경 관리:
  모든 변경 -> CAB 검토 (1주 주기)
  -> 검토·승인 후 배포
  -> 통제됨, 느림

  DevOps 목표: 하루 수십~수백 배포

충돌:
  DevOps 팀: "CAB이 속도를 막는다"
  ITSM 팀: "변경 관리 없으면 장애 증가"

  -> 현실: 변경 관련 장애가 전체의 60~70%

해결: 경량화된 변경 관리

1. 변경 유형 재분류:
   표준 변경 (Standard): 사전 승인 불필요
   - 이미 승인된 패턴 (예: AWS 오토스케일링)
   - CI/CD 파이프라인 자동 배포

   일반 변경 (Normal): 경량 CAB
   - Slack/Jira 기반 비동기 승인 (24시간)

   긴급 변경 (Emergency): 사후 검토
   - 신속 배포 후 24시간 내 사후 보고

2. 자동화된 변경 승인:
   모든 테스트 통과 + SAST + SCA
   -> 저위험 변경 자동 승인

   사람 검토: 고위험 변경만

3. 변경 실패율 추적:
   DORA 지표: Change Failure Rate (CFR)
   목표: < 15% (Elite: < 5%)

SRE와 ITSM 융합:
  Error Budget: 허용 오류 예산
  -> SLA 99.9% = 0.1% 오류 예산
  -> 오류 예산 소진 -> 기능 개발 중단
  -> 안정성 우선
```

> 📢 **섹션 요약 비유**: ITSM+DevOps는 빠른 배달+안전 — 빠른 배달(DevOps)을 위해 안전 검사(ITSM)를 자동화. 저위험 소포는 자동 통과, 위험 화물만 검사!

---

## Ⅳ. ITSM 도구 선택

```
ITSM 도구 비교:

Enterprise:
  ServiceNow:
  - 업계 1위, 풀 기능
  - 높은 비용, 높은 유연성
  - AI/ML 통합
  - 사용처: 대기업

BMC Helix (Remedy):
  - 레거시 대기업 시장
  - 강력한 CMDB
  - 복잡한 커스터마이징

Mid-Market:
  Jira Service Management (Atlassian):
  - 개발팀 친화적
  - Jira/Confluence 통합
  - DevOps 워크플로우
  - 비용 경쟁력

Freshservice:
  - 사용하기 쉬움
  - AI 기반 티켓 분류
  - 중소기업 대상

SMB:
  Zendesk:
  - 고객 서비스 중심
  - 사용 편의성 우수
  - IT 적용 증가

오픈소스:
  OTRS: 무료 ITSM
  iTop: ITIL 기반

선택 기준:
  규모: 사용자 수, 티켓 볼륨
  통합: 모니터링, CI/CD, 협업 도구
  예산: 라이선스 + 구현 + 운영
  ITIL 준수도: 기능 깊이
  사용성: 서비스 데스크 담당자
```

> 📢 **섹션 요약 비유**: ITSM 도구 선택은 ERP 선택 — 대기업은 SAP/오라클(ServiceNow), 중소기업은 더 가벼운 것(Freshservice). 기능 많을수록 복잡하고 비싸요!

---

## Ⅴ. 실무 시나리오 — 통신사 ITSM 혁신

```
대형 통신사 ITSM 최적화:

현황:
  IT 인원 2,000명
  월 티켓: 80,000건
  FCR: 45% (낮음)
  MTTR P1: 8시간 (목표 4시간)
  ITSM 도구: BMC Remedy (레거시, 비싸고 복잡)

문제 분석:
  FCR 낮음:
  -> L1 담당자 권한/지식 부족
  -> 불필요한 에스컬레이션

  높은 MTTR:
  -> CMDB 부정확 -> 영향 분석 오래 걸림
  -> 담당자 수동 배정

개선 계획 (18개월):

1. ServiceNow 이관:
   AI 기반 티켓 분류·자동 배정
   예측 인텔리전스 활성화

2. 지식 관리 강화:
   상위 100개 인시던트 지식 문서화
   L1 참조 가이드 -> FCR 향상

3. CMDB 정확도 개선:
   자동 발견(Discovery) 도구 활용
   주간 정합성 검사

4. 변경 관리 경량화:
   표준 변경 확대 (전체 변경의 60%)
   긴급 변경 비율 목표 5% 이하

결과 (18개월):
  FCR: 45% -> 72%
  MTTR P1: 8시간 -> 3.2시간
  월 티켓: 80,000 -> 65,000 (15% 감소)
  긴급 변경 비율: 18% -> 6%
  CSAT: 3.4 -> 4.1/5.0
  비용: BMC Remedy 유지보수 -> ServiceNow 이관 후 3년 TCO 15% 절감
```

> 📢 **섹션 요약 비유**: 통신사 ITSM 혁신은 콜센터 업그레이드 — AI 분류기(자동 배정), 지식 시스템(L1 권한 강화), CMDB 지도(영향 분석). FCR 45%->72% = 고객 절반 더 빠른 해결!

---

## 📌 관련 개념 맵

```
ITSM
+-- 프레임워크
|   +-- ITIL 4 (주류)
|   +-- ISO 20000 (표준)
+-- 핵심 KPI
|   +-- MTTR, MTBF
|   +-- FCR, CSAT
|   +-- SLA 준수율
+-- DevOps 통합
|   +-- 경량 변경 관리
|   +-- DORA 지표 (CFR)
|   +-- Error Budget (SRE)
+-- 도구
    +-- ServiceNow (엔터프라이즈)
    +-- Jira Service Management (개발자)
    +-- Freshservice, Zendesk
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 IT 관리 (1980s)]
기술 중심, 직접 운영
      |
      v
[ITIL v2/v3 (2000s)]
서비스 수명주기
전 세계 ITSM 표준화
      |
      v
[DevOps 등장 (2009~)]
ITSM과 DevOps 충돌
변경 관리 경량화 논의
      |
      v
[ITIL 4 + SRE 융합 (2019~)]
속도+안정성 균형
Error Budget, DORA 지표
      |
      v
[현재: AI 기반 ITSM]
AI 티켓 분류, 예측 인텔리전스
AIOps (이상 자동 탐지)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. ITSM은 IT를 서비스업으로 — 단순 기술 관리가 아니라 사용자(고객)에게 서비스를 제공한다는 마음가짐. 호텔처럼 투숙객 만족이 목표!
2. FCR은 첫 전화 해결 — "AS기사 한 번만 오면 끝!" 비율. 높을수록 사용자 만족, IT 비용 절감!
3. ITSM+DevOps는 빠른 배달+안전 검사 — 자동화로 빠르게 배포하면서, 위험한 변경만 검토. 속도와 안정성 둘 다!
