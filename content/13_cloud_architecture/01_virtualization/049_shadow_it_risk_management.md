---
title: "Shadow It Risk Management"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 49
---
> **핵심 인사이트**
> 1. 클라우드 시대의 섀도 IT는 개인 SaaS 사용을 넘어 무단 클라우드 인프라 프로비저닝(Shadow Cloud)으로 확대 — 개발자가 신용카드로 AWS 계정을 직접 개설하거나, 팀이 IT 승인 없이 Azure 구독을 생성하면서 기업 보안 경계가 무너진다.
> 2. CSPM(Cloud Security Posture Management)이 클라우드 섀도 IT 탐지와 거버넌스의 핵심 도구 — 다중 클라우드 환경에서 리소스 구성 오류(Misconfiguration), 공개 S3 버킷, 과도한 권한을 자동으로 탐지하고 컴플라이언스 위반을 실시간으로 모니터링한다.
> 3. FinOps와 클라우드 거버넌스의 결합이 클라우드 섀도 IT의 비용 최적화 접근법 — 승인되지 않은 클라우드 리소스는 비용 추적이 안 되어 예산 초과와 낭비로 이어지며, 태깅(Tagging) 정책과 비용 할당이 가시성 확보의 첫걸음이다.

---

## Ⅰ. 클라우드 섀도 IT

```
클라우드 섀도 IT:
  IT 승인 없이 생성된 클라우드 리소스/서비스

유형:

1. 섀도 SaaS:
  개인 계정 SaaS (Salesforce 개인판, GitHub 개인)
  IT 모르는 SaaS 구독 (팀이 공유 카드로 결제)

2. 섀도 클라우드 (Shadow Cloud):
  개발자가 개인 카드로 AWS 계정 개설
  팀이 기업 계정 외부에 새 Azure 구독 생성
  GCP 프로젝트 무단 생성

  예:
  스타트업 개발팀: "프로덕션 배포가 느려서
  개인 AWS로 POC 시작 -> 그대로 프로덕션화"

3. 미승인 클라우드 서비스:
  기업이 Azure 쓰는데 팀이 AWS Lambda 무단 사용
  생성형 AI API 직접 결합

발생 원인:
  클라우드 계정 생성: 신용카드 하나로 5분
  vs 기업 IT 승인: 수주 대기

  비용:
  AWS 무료 티어: 12개월 무료
  -> "일단 써보고 나중에 승인"

위험:
  공개 S3 버킷: 데이터 유출
  취약한 구성: 공개 RDS, 개방 보안 그룹
  비용 폭발: 예산 통제 불가
  컴플라이언스: GDPR, PCI-DSS 위반
```

> 📢 **섹션 요약 비유**: 클라우드 섀도 IT = 사무실 밖 개인 사무실 차리기 — 회사 사무실(승인 클라우드) 절차 복잡해서 개인 임대(개인 AWS). 화재(보안 사고) 나도 회사가 모름. 비용도 개인 카드!

---

## Ⅱ. CSPM

```
CSPM (Cloud Security Posture Management):
  클라우드 환경의 보안 구성 오류 탐지 및 수정

주요 기능:

1. 리소스 가시성:
  모든 클라우드 계정/구독의 리소스 자동 발견

  지원: AWS, Azure, GCP, OCI 등 멀티클라우드

  발견:
  기업 승인 외 계정 탐지 (CIS Benchmark 기반)

2. 구성 오류 탐지 (Misconfiguration):
  고위험 사례:
  - S3 퍼블릭 접근 허용
  - 보안 그룹 0.0.0.0/0 인바운드 (모든 포트)
  - 루트 계정 MFA 미설정
  - 미암호화 EBS 볼륨 (민감 데이터)
  - CloudTrail 로깅 비활성화

  자동 점검: 수백 개 규칙 매일 실행

3. 컴플라이언스 모니터링:
  CIS AWS Foundations Benchmark
  PCI-DSS, HIPAA, GDPR, ISO 27001

  대시보드: 각 규정별 준수율 (%) 실시간

4. 자동 수정 (Auto-Remediation):
  고위험 오류: 자동 수정

  예:
  S3 퍼블릭 접근 활성화 탐지 -> 자동 차단
  (또는 알림 -> 수동 승인 후 차단)

주요 제품:
  Prisma Cloud (Palo Alto)
  Microsoft Defender for Cloud
  AWS Security Hub + Config
  Wiz, Orca Security
```

> 📢 **섹션 요약 비유**: CSPM = 클라우드 자동 안전 감사원 — 매일 전체 클라우드 자산 점검. 열린 창문(S3 퍼블릭), 잠금 없는 문(MFA 없음) 자동 탐지. 규정 준수율(%) 실시간 표시!

---

## Ⅲ. 클라우드 거버넌스 프레임워크

```
클라우드 거버넌스 핵심 요소:

1. 계정/구독 관리:
  AWS Organizations / Azure Management Group

  구조:
  루트 계정
  +-- 프로덕션 OU (Organizational Unit)
  |   +-- 프로덕션 계정
  |   +-- DR 계정
  +-- 개발 OU
  |   +-- 개발 계정
  +-- 보안 OU
      +-- 로깅 계정

  SCP (Service Control Policy):
  특정 서비스/리전 사용 제한 (전체 OU에 적용)

  예:
  "ap-northeast-2(서울) 외 리전 사용 금지"
  "S3 퍼블릭 액세스 설정 변경 금지"

2. 태깅 정책 (Tagging Policy):
  모든 리소스에 필수 태그:
  Owner: team-platform@company.com
  CostCenter: CC-1234
  Environment: production
  Project: project-alpha

  태그 없는 리소스: 자동 경보 + 정지 예고

3. 비용 거버넌스 (FinOps):
  예산 알림: 80%, 100% 초과 시 자동 알림
  사용되지 않는 리소스 자동 식별
  Reserved Instance / Savings Plan 분석

4. 접근 제어:
  최소 권한 IAM 정책
  Break-Glass 절차 (긴급 관리자 계정)
  IAM Access Analyzer
```

> 📢 **섹션 요약 비유**: 클라우드 거버넌스 = 도시 계획 — AWS Organizations(행정구역), SCP(건축 규제), 태깅(주소 등록 필수), FinOps(세금 납부). 무단 건물(섀도 클라우드)은 철거!

---

## Ⅳ. 멀티클라우드 가시성

```
멀티클라우드 섀도 IT 문제:
  기업이 AWS 주력 -> 팀이 Azure, GCP도 사용
  단일 콘솔로 전체 가시성 필요

통합 가시성 도구:

Wiz:
  에이전트리스 (에이전트 설치 불필요)
  AWS/Azure/GCP/K8s 통합 스캔

  공격 경로 분석:
  "인터넷 -> 공개 VM -> 과도한 권한 역할 -> DB 접근"
  최고 위험 경로 우선 시각화

Prisma Cloud:
  CSPM + CWPP (Cloud Workload Protection)
  컨테이너/서버리스도 지원

클라우드 에셋 목록 (Asset Inventory):
  전체 클라우드 리소스 목록 (계정별)
  미승인 계정/구독 탐지

  AWS Config:
  모든 리소스 변경 이력 기록
  ConfigRule: 컴플라이언스 규칙 평가

실시간 알림 체계:
  새 계정 생성 -> 즉시 보안팀 알림
  고위험 구성 오류 -> PagerDuty 에스컬레이션
  대용량 데이터 전송 -> 이상 탐지 알림
```

> 📢 **섹션 요약 비유**: 멀티클라우드 가시성 = 위성 지도 — Wiz/Prisma Cloud가 AWS+Azure+GCP 전체를 위성으로 내려다봄. 불법 건물(섀도 클라우드), 잠금 없는 창고(S3 퍼블릭) 한눈에!

---

## Ⅴ. 실무 시나리오 — 클라우드 거버넌스 구축

```
글로벌 제조기업 멀티클라우드 거버넌스:

배경:
  AWS(메인) + Azure(M365) + GCP(ML)
  개발팀이 무단으로 AWS 계정 5개 생성 발견
  월 클라우드 비용: 예산 대비 140% 초과 (원인 불명)

현황 조사 (CSPM 도입):
  Wiz로 전체 클라우드 스캔:

  발견된 섀도 리소스:
  - 미승인 AWS 계정: 5개
  - 공개 S3 버킷: 12개 (데이터 유출 위험)
  - MFA 없는 루트 계정: 3개
  - 2년 이상 미사용 EC2: 67대 (월 $8,500 낭비)

  고위험 발견:
  개발팀 AWS 계정 중 1개에
  테스트용 고객 데이터 5만 건 저장 (GDPR 위반!)

즉시 조치:
  1. 공개 S3 -> 즉시 차단
  2. 고객 데이터 -> 격리 후 삭제
  3. GDPR DPA에 위반 신고 (72시간 이내)
  4. 미사용 EC2 67대 정지

거버넌스 수립:
  AWS Organizations로 계정 통합
  SCP: 서울 리전 외 사용 금지
  태깅 정책 강제 적용
  월간 비용 리뷰 (FinOps)

결과 (3개월):
  월 클라우드 비용: -32% (미사용 리소스 제거)
  섀도 클라우드 리소스: 95% 감소
  CSPM 점수: 34% -> 89%
  GDPR 위반 재발: 0건
```

> 📢 **섹션 요약 비유**: 클라우드 거버넌스 구축 = 도시 무허가 건물 정비 — CSPM으로 전체 스캔(위성 지도). 무허가(섀도) 5개 계정, 12개 열린 창고 발견. 정비 후 비용 32% 절감, GDPR 위반 0건!

---

## 📌 관련 개념 맵

```
클라우드 섀도 IT
+-- 유형
|   +-- 섀도 SaaS
|   +-- 섀도 클라우드 (무단 계정)
|   +-- 미승인 클라우드 서비스
+-- 탐지
|   +-- CSPM (Wiz, Prisma Cloud)
|   +-- AWS Config, Security Hub
+-- 거버넌스
|   +-- AWS Organizations + SCP
|   +-- 태깅 정책
|   +-- FinOps (비용 거버넌스)
+-- 관련
    +-- CASB (SaaS 제어)
    +-- Zero Trust
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[클라우드 셀프서비스 확산 (2010s)]
신용카드로 클라우드 계정 생성
섀도 클라우드 시작
      |
      v
[CSPM 등장 (2015~)]
클라우드 구성 오류 자동 탐지
Dome9, Evident.io
      |
      v
[멀티클라우드 (2017~)]
AWS+Azure+GCP 병존
통합 가시성 필요
      |
      v
[Wiz, Orca (2020~)]
에이전트리스 CSPM
공격 경로 분석
      |
      v
[현재: AI 기반 CNAPP]
Cloud Native Application Protection
예측적 리스크 탐지
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 섀도 IT = 개인 사무실 차리기 — 신용카드로 5분에 AWS 계정 생성. 회사 모르는 클라우드 = 보안·비용 사각지대!
2. CSPM = 자동 안전 감사원 — 매일 전체 클라우드 점검. 열린 S3(잠금 없는 창고), MFA 없는 계정 자동 탐지. 컴플라이언스 준수율 실시간!
3. AWS Organizations = 도시 계획 — 계정(구역) 분리, SCP(건축 규제), 태깅(주소 등록). 무허가 건물(섀도 클라우드) 자동 발견!
