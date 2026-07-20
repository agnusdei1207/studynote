---
title: "Migration Repurchase Saas"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 45
---
> **핵심 인사이트**
> 1. 클라우드 이전(Migration) 전략의 6R(또는 7R) 프레임워크 — Retire(폐기), Retain(유지), Rehost(Lift & Shift), Replatform(이식), Repurchase(SaaS 전환), Refactor(재설계), Relocate(이전)으로 각 워크로드에 최적 전략을 선택한다.
> 2. Repurchase(SaaS 재구매)는 사내 구축 소프트웨어를 SaaS로 교체 — 이메일(Exchange->Office 365), CRM(Siebel->Salesforce), ERP(온프레미스->SAP S/4HANA Cloud) 전환이 대표적이며, 초기 비용보다 장기 총소유비용(TCO) 분석이 핵심이다.
> 3. SaaS 전환의 핵심 과제는 데이터 이전(Data Migration)과 통합(Integration) — 수년간 축적된 레거시 데이터를 SaaS 데이터 모델로 변환하고, 기존 시스템과의 연동(API 통합)이 프로젝트 복잡성의 80%를 차지한다.

---

## Ⅰ. 클라우드 이전 6R

```
AWS 클라우드 이전 6R 프레임워크:

1. Retire (폐기):
   더 이상 필요 없는 애플리케이션 폐기

   예: 사용 안 하는 레거시 리포팅 도구
   판단: 사용자 < 5%, 비즈니스 가치 없음
   결과: 비용 절감, 복잡성 감소

2. Retain (유지):
   클라우드 이전 보류 (현재 위치 유지)

   이유: 규제, 최근 업그레이드, 기술 부채 해결 우선
   예: 6개월 내 EOL(End of Life) 예정 시스템

3. Rehost (Lift & Shift):
   코드·아키텍처 변경 없이 클라우드로 이전

   속도: 빠름 (가장 간단)
   비용: 초기 이전 이후 최적화 별도 필요
   예: VM -> EC2 1:1 이전
   도구: AWS MGN (Application Migration Service)

4. Replatform (이식):
   핵심 아키텍처 유지, 일부 최적화

   예: DB -> RDS (관리형 서비스), Tomcat -> Elastic Beanstalk
   비용 절감 + 운영 부담 감소

5. Repurchase (SaaS 재구매):
   기존 On-Premise 소프트웨어 -> SaaS 교체

   예: Exchange -> Microsoft 365
       Siebel -> Salesforce
   개발/운영 부담 완전 제거

6. Refactor / Re-architect (재설계):
   클라우드 네이티브 아키텍처로 완전 재설계

   예: 모놀리식 -> MSA + 컨테이너
   비용: 가장 높음, 장기 이익 최대
   적용: 핵심 비즈니스 차별화 서비스

선택 기준:
  ROI 기준: Rehost(최저) <- -> Refactor(최고)
  기간 기준: Retire -> Rehost -> Repurchase -> Refactor
```

> 📢 **섹션 요약 비유**: 6R은 이사 전략 — 버리기(Retire), 두고가기(Retain), 그대로 옮기기(Rehost), 포장 개선(Replatform), 새 가구로 교체(Repurchase), 집 자체를 새로(Refactor)!

---

## Ⅱ. Repurchase — SaaS 전환

```
Repurchase SaaS 전환 유형:

이메일/협업:
  On-Premise Exchange -> Microsoft 365 (Exchange Online)
  On-Premise 파일서버 -> SharePoint Online / Teams

  장점: 라이선스+서버+패치 비용 제거
  비용: 사용자당 월 $12~35 (M365 E3)

CRM:
  SAP CRM, Siebel -> Salesforce

  과정:
  1. 데이터 이전 (Customer, Account, Opportunity)
  2. 사용자 교육
  3. 통합 (ERP, 마케팅 자동화)
  4. 커스터마이제이션 (Flow, Apex)

ERP:
  SAP ECC -> SAP S/4HANA Cloud
  Oracle EBS -> Oracle Fusion Cloud

  복잡도 최고: 핵심 비즈니스 프로세스
  기간: 1~3년
  비용: 수억~수백억

HR/급여:
  자체 HR -> Workday, SAP SuccessFactors

보안:
  자체 방화벽/이메일 보안 -> 클라우드 SEG (Proofpoint, Mimecast)

의사결정 기준:
  SaaS 적합:
  - 공통 비즈니스 기능 (이메일, HR)
  - 차별화 필요 없음
  - 빠른 전환 필요

  자체 개발 적합:
  - 핵심 경쟁 우위 기능
  - 특수 비즈니스 프로세스
```

> 📢 **섹션 요약 비유**: Repurchase는 식당 부엌 교체 — 직접 만든 낡은 냉장고(On-Premise) 버리고, 최신 렌탈 냉장고(SaaS) 구독. 수리 걱정 없이 음식(비즈니스)만!

---

## Ⅲ. SaaS 데이터 이전

```
SaaS 데이터 이전 (Data Migration):

주요 단계:

1. 데이터 현황 분석:
   소스 DB 스캔
   데이터 품질 이슈 파악 (중복, 누락, 오류)
   이전 범위 결정 (전체 vs 최근 X년)

2. 데이터 매핑:
   소스 스키마 ↔ SaaS 데이터 모델 매핑

   예: Siebel -> Salesforce
   Siebel: ACCOUNT.ACCOUNT_NAME -> SF: Account.Name
   Siebel: S_CONTACT.FST_NAME -> SF: Contact.FirstName

3. ETL 구축:
   Extract: 소스 DB에서 데이터 추출
   Transform: 매핑에 따라 변환 + 정제
   Load: Salesforce API로 업로드

   도구: Informatica, Talend, MuleSoft, CSV + Data Loader

4. 검증:
   건수 일치 확인
   샘플링 검증 (수동)
   업무팀 UAT

5. 컷오버:
   이전 일정 (주말 또는 야간)
   최종 델타 이전 (마지막 변경분)
   전환 완료

이전 복잡성:
  간단: 이메일 (메일박스 이전)
  중간: CRM 고객 데이터
  복잡: ERP (수십 년 트랜잭션 이력)

  ERP 이전 전략:
  신규 이력: SaaS
  구 이력: 아카이브 또는 레거시 병행
```

> 📢 **섹션 요약 비유**: SaaS 데이터 이전은 이사짐 정리 — 낡은 집(레거시)에서 짐(데이터) 꺼내고, 새 집(SaaS) 크기에 맞게 정리(변환)해서 옮겨요. 이사짐이 많을수록 복잡!

---

## Ⅳ. TCO 분석

```
SaaS 전환 TCO (Total Cost of Ownership) 분석:

On-Premise CRM 5년 TCO:
  하드웨어: 1억 (서버 × 3)
  SW 라이선스: 3억 (Siebel 영구)
  DBA/운영 인력: 연 5천 × 5 = 2.5억
  기반 SW (OS, DB): 0.5억
  데이터센터 (전력, 공간): 0.3억
  패치/업그레이드: 연 2천 × 5 = 1억
  -----------------------------
  5년 총비용: 8.3억

Salesforce 5년 TCO:
  구독료: 사용자 50명 × $150/월 × 12 × 5 = $450,000 ≈ 6억
  구현/커스터마이징: 2억
  통합 유지: 연 3천 × 5 = 1.5억
  교육: 0.3억
  -----------------------------
  5년 총비용: 9.8억

단순 숫자만 보면 On-Premise가 저렴!

추가 가치 고려:
  Salesforce: 자동 업그레이드 (신기능 포함)
  On-Premise: 업그레이드 프로젝트 별도 비용

  Salesforce: 모바일·AI 기능 즉시 제공
  On-Premise: 추가 개발 필요

  Salesforce: 글로벌 접근 (원격 근무)
  On-Premise: VPN 필수

TCO 결론:
  단기(3년): On-Premise 유리할 수 있음
  장기(5년+): SaaS 경쟁력 증가
  기회비용 포함 시: SaaS 우위

  핵심: 숫자만 보지 말고 전략적 유연성 포함 평가
```

> 📢 **섹션 요약 비유**: TCO는 총 유지비용 — 새 차(SaaS) 월 리스료 vs 중고차(On-Premise) 구입 후 수리비+보험. 겉 가격만 보지 말고 5년 총비용을 비교!

---

## Ⅴ. 실무 시나리오 — 글로벌 제조업 M365 전환

```
글로벌 제조업체 Microsoft 365 전환:

배경:
  전 세계 30개국, 임직원 5만명
  On-Premise Exchange 2013 (EOL 2023.10)
  자체 파일 서버 수백 대

전환 결정:
  Exchange 2013 EOL -> 강제 이전 필요
  신규 Exchange 서버 vs M365 선택
  TCO 분석: 5년 기준 M365 2억 절감
  -> M365 E3 선택

이전 전략:
  물결 방식 (Wave Approach):
  Wave 1: 본사 + 한국 (2,000명) — 파일럿
  Wave 2~5: 지역별 순차 이전 (각 1만명)
  총 기간: 8개월

기술 과제:
  DNS 변경: MX 레코드 -> EOP(Exchange Online Protection)
  메일 데이터: Exchange Migration (ExchangeGUID 매핑)
  공유 폴더: SharePoint Online 마이그레이션
  (SharePoint Migration Tool)

  통합:
  SAP ↔ M365 (Azure AD SSO)
  Teams ↔ 화상회의 레거시 -> Teams Rooms

결과:
  이전 완료: 8개월 (계획 대비 -1개월)
  TCO 절감: 연 4억원
  사용자 만족도: 4.2/5.0
  보안: ATP (Advanced Threat Protection) 도입
  원격근무 지원 크게 향상 (COVID-19 기간 중 완료)

  교훈:
  "사용자 변화관리 80%, 기술 20%"
  현지화 교육이 채택률 결정적
  IT-HR 협업 필수
```

> 📢 **섹션 요약 비유**: M365 이전은 전국 지사 동시 이사 — 한 번에 5만 명 이사는 불가능, 물결(Wave)로 지역별 순차 이전. 기술보다 직원들 적응(변화관리)이 더 중요!

---

## 📌 관련 개념 맵

```
클라우드 이전 전략 (6R)
+-- Retire / Retain
+-- Rehost (Lift & Shift)
+-- Replatform
+-- Repurchase (SaaS)
|   +-- 이메일: M365
|   +-- CRM: Salesforce
|   +-- ERP: SAP Cloud
+-- Refactor (MSA/Cloud Native)
+-- 핵심 활동
    +-- TCO 분석
    +-- 데이터 이전 (ETL)
    +-- 통합 (API/iPaaS)
    +-- 변화 관리
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[클라우드 초기 이전 (2010s)]
Lift & Shift 주류
"빠른 이전"
      |
      v
[SaaS 폭발적 성장 (2012~)]
Salesforce, Workday, ServiceNow
Repurchase 트렌드 가속
      |
      v
[6R 프레임워크 (2017)]
AWS 마이그레이션 전략 공식화
워크로드별 최적 전략
      |
      v
[현재: 클라우드 네이티브 우선]
Refactor / 클라우드 네이티브
SaaS First 정책 (비커스텀 기능)
멀티클라우드 전략
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 6R은 이사 전략 6가지 — 버리기(Retire), 그대로(Rehost), 일부 고치기(Replatform), 새 가구로 교체(Repurchase), 집 새로(Refactor)! 상황에 맞는 방법 선택!
2. Repurchase는 구독 서비스 교체 — 직접 만든 낡은 냉장고(Exchange) 버리고, 매달 구독하는 새 냉장고(M365)로! 수리 걱정 끝!
3. TCO가 핵심 — "월 구독료(SaaS)가 비싸 보여도" 5년 총비용(서버+인건비+업그레이드) 합치면 SaaS가 저렴할 수 있어요!
