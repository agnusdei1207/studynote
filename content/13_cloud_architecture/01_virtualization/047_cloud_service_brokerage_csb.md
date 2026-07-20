---
title: "Cloud Service Brokerage Csb"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 47
---
> **핵심 인사이트**
> 1. CSB(Cloud Service Brokerage)는 클라우드 서비스 소비자와 제공자 사이에서 중개·통합·커스터마이징·거버넌스 역할을 수행하는 개체 — Gartner가 정의한 클라우드 컴퓨팅 참조 모델의 핵심 구성 요소로, 멀티 클라우드 환경의 복잡성을 관리한다.
> 2. CSB의 세 가지 역할 — 중개(Intermediation: 서비스 부가가치 추가), 집계(Aggregation: 여러 클라우드 통합), 차익거래(Arbitrage: 비용 최적화를 위한 자동 클라우드 전환)로 구성되며, 현대 CSB는 이 세 역할을 통합 제공한다.
> 3. FinOps와 CSB의 융합이 현대 트렌드 — 단순 중개를 넘어 클라우드 비용 최적화(FinOps), 보안 정책 일관성(CASB), 거버넌스 자동화를 통합하는 클라우드 관리 플랫폼(CMP)으로 진화하고 있다.

---

## Ⅰ. CSB 개요와 역할

```
NIST 클라우드 참조 모델:

클라우드 소비자 (Consumer)
     <->
[CSB - Cloud Service Broker]
     <->
클라우드 제공자 (Provider: AWS, Azure, GCP)

CSB 3대 역할 (Gartner):

1. 중개 (Intermediation):
  클라우드 서비스에 부가가치 추가

  예:
  AWS S3 + 암호화 + 접근 통제 + DLP
  -> 기업 규정 준수 스토리지 서비스

  보안 CSB: 클라우드에 보안 레이어 추가

2. 집계 (Aggregation):
  여러 클라우드 서비스를 단일 인터페이스로

  예:
  AWS + Azure + GCP + SaaS 앱들
  -> 단일 대시보드, 단일 청구, 단일 정책

  멀티 클라우드 관리 플랫폼

3. 차익거래 (Arbitrage):
  여러 클라우드 간 가격/성능 비교 후 자동 선택

  예:
  컴퓨팅 작업 시작 -> CSB가 현재 스팟 가격 비교
  AWS: $0.10/시간, GCP: $0.08/시간
  -> GCP 자동 선택

  한계: 이식성(Portability) 이슈
  클라우드별 API 차이 -> 이동 어려움
```

> 📢 **섹션 요약 비유**: CSB는 여행사 — 여러 항공사(클라우드)를 비교해서 좋은 것 골라주고(차익거래), 패키지로 묶어주고(집계), 여행 보험 추가(중개). 소비자는 여행사만 상대!

---

## Ⅱ. 클라우드 관리 플랫폼 (CMP)

```
CMP (Cloud Management Platform):
  CSB 기능을 포함한 통합 클라우드 관리 도구

주요 CMP 기능:

1. 비용 관리 (FinOps):
  멀티 클라우드 비용 가시성
  태그 기반 비용 배분 (팀/프로젝트)
  이상 비용 알림
  예약 인스턴스 최적화 추천

2. 거버넌스:
  보안 정책 일관성 (모든 클라우드)
  규정 준수 자동 검사 (GDPR, SOX)
  승인 워크플로우

3. 운영 자동화:
  IaC 배포 (Terraform 통합)
  자동 프로비저닝/디프로비저닝
  사이즈 최적화 추천

4. 보안:
  CSPM (Cloud Security Posture Management)
  오설정 탐지 (공개 S3 버킷 등)
  통합 IAM

대표 CMP 도구:

CloudHealth (VMware):
  비용 최적화 특화
  멀티 클라우드 비용 통합 뷰

Apptio Cloudability:
  FinOps 특화
  비용 배분, 예측

HashiCorp Terraform Cloud:
  IaC 자동화 특화
  멀티 클라우드 프로비저닝

Flexera:
  SAM(소프트웨어 자산) + CMP 통합
  라이선스 최적화

자체 구축:
  Kubernetes + Crossplane
  오픈소스 멀티 클라우드 추상화
```

> 📢 **섹션 요약 비유**: CMP는 멀티 클라우드 원격 관리 — 여러 집(클라우드)을 한 앱으로 관리. 전기(비용), 보안(정책), 청소(자동화) 통합 관리. 집마다 따로 안 가도 돼요!

---

## Ⅲ. CASB (Cloud Access Security Broker)

```
CASB (Cloud Access Security Broker):
  클라우드 서비스 보안 특화 CSB

  위치: 기업 사용자 ↔ 클라우드 SaaS 사이

CASB 4가지 기둥 (Gartner):

1. 가시성 (Visibility):
  어떤 클라우드 서비스가 사용 중?
  Shadow IT 탐지:
  "직원들이 승인 안 된 Dropbox 사용 중!"

  5,000명 직원 -> 평균 900개 클라우드 서비스 사용 (통계)

2. 규정 준수 (Compliance):
  데이터가 클라우드에서 규정 준수 여부
  GDPR: EU 데이터가 EU 밖으로 나가나?
  DLP: 민감 데이터 클라우드 업로드 차단

3. 데이터 보안 (Data Security):
  클라우드 저장 데이터 암호화
  DRM (디지털 권한 관리)
  콘텐츠 검사 + 분류

4. 위협 보호 (Threat Protection):
  악의적 클라우드 사용 탐지
  계정 탈취 탐지 (비정상 로그인)
  랜섬웨어 탐지 (대량 파일 변경)

CASB 배포 방식:
  프록시 (Proxy): 트래픽 인라인 차단
  API (Out-of-Band): SaaS API로 데이터 검사
  에이전트: 엔드포인트 설치

주요 도구:
  Netskope: 시장 리더
  Microsoft Defender for Cloud Apps (MCAS)
  Zscaler CASB
  McAfee MVISION Cloud
```

> 📢 **섹션 요약 비유**: CASB는 회사 클라우드 경비원 — 직원이 어떤 클라우드 쓰는지 감시(가시성), 기밀 파일 개인 드롭박스 전송 차단(데이터 보안), 이상 행동 탐지(위협 보호)!

---

## Ⅳ. FinOps와 클라우드 최적화

```
FinOps (Financial Operations):
  클라우드 비용 문화적 접근
  "비즈니스 팀+엔지니어+재무팀 협업으로 클라우드 비용 최적화"

FinOps 3단계 (사이클):

1. 알림 (Inform):
  누가 얼마 쓰는지 가시성
  태그 기반 비용 배분
  예산 초과 알림

  도구: AWS Cost Explorer, CloudHealth

2. 최적화 (Optimize):
  낭비 제거:
  사용 안 하는 리소스 정리
  올바른 사이즈 (Right Sizing)

  예약 인스턴스:
  On-Demand 대비 40~60% 절감
  1년 또는 3년 약정

  스팟 인스턴스:
  여분 용량 사용 -> 70~90% 절감
  중단 내성 워크로드 (ML 학습, 배치)

3. 운영 (Operate):
  지속적 비용 최적화 문화
  엔지니어가 비용 인식
  비용 이상 자동 알림

클라우드 비용 낭비 패턴:
  좀비 리소스: 사용 안 하는 VM (업계 30~40%)
  과도한 사이즈: m5.4xlarge -> m5.xlarge
  미사용 예약: 예약하고 안 씀
  데이터 이전 비용: 클라우드 내 네트워크 비용 간과
  개발/테스트 환경: 24×7 실행 (업무 시간만 필요)

ROI:
  FinOps 도입 기업: 평균 28% 클라우드 비용 절감
  (Flexera 2024 State of the Cloud)
```

> 📢 **섹션 요약 비유**: FinOps는 클라우드 가계부 — "누가 얼마 썼나(알림)" + "불필요한 것 끄기(최적화)" + "비용 의식 문화(운영)". 평균 28% 절감 = 1억 쓰면 2,800만원 아끼기!

---

## Ⅴ. 실무 시나리오 — 중견기업 CSB 구축

```
중견 제조사 (직원 2,000명) CSB 도입:

현황:
  AWS 70%, Azure 30% 혼용
  클라우드 월 청구: 5억원

  문제:
  멀티 클라우드 비용 통합 뷰 없음
  각 클라우드 별도 거버넌스 -> 정책 불일치
  사용 안 하는 리소스 파악 불가
  보안팀: Shadow IT 우려

CSB 솔루션 설계:

계층 구조:
  기업 사용자/팀
       <->
  [CSB 레이어: CloudHealth + CASB]
       <->
  AWS + Azure 멀티 클라우드

CloudHealth (CMP) 도입:
  1. 비용 통합 대시보드:
  AWS + Azure 단일 뷰
  팀별 태그 비용 배분 (부서별 차지백)

  2. 최적화 추천:
  발견: 좀비 EC2 42개 (월 1,200만원 낭비)
  미사용 RDS 8개 (월 400만원)
  사이즈 초과 60개 (월 800만원)

  -> 즉시 조치: 월 2,400만원 절감

CASB (Netskope) 도입:
  Shadow IT 탐지:
  직원들이 사용 중인 미승인 서비스 발견:
  개인 Dropbox/Google Drive -> 업무 파일 공유

  정책:
  기밀 문서(DLP 분류) -> 미승인 클라우드 차단
  승인 서비스(SharePoint, Box): 허용

결과 (6개월):
  클라우드 비용: 5억원 -> 3.3억원 (34% 절감)
  정책 일관성: AWS+Azure 동일 보안 정책
  Shadow IT: 직원 인식 제고 + 공식 채널 사용
  ROI: 솔루션 비용 6개월 내 회수
```

> 📢 **섹션 요약 비유**: 중견사 CSB 구축 결과 — 멀티 클라우드 가계부(CMP) 열어보니 2,400만원 낭비 발견! 경비원(CASB) 배치하니 직원 개인 클라우드 사용 차단. 6개월에 솔루션 비용 회수!

---

## 📌 관련 개념 맵

```
CSB (Cloud Service Brokerage)
+-- 역할
|   +-- 중개 (Intermediation)
|   +-- 집계 (Aggregation)
|   +-- 차익거래 (Arbitrage)
+-- 구현
|   +-- CMP (Cloud Management Platform)
|   +-- CASB (보안 브로커)
|   +-- FinOps (비용 최적화)
+-- 대표 도구
    +-- CloudHealth, Apptio
    +-- Netskope, MCAS (CASB)
    +-- Terraform Cloud (IaC)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[CSB 개념 등장 (2011)]
Gartner 클라우드 참조 모델
멀티 클라우드 복잡성 인식
      |
      v
[CASB 탄생 (2012)]
Gartner: CASB 용어 정의
Shadow IT 문제 부각
      |
      v
[FinOps 개념화 (2018)]
Cloud Financial Management
비용 문화 운동
      |
      v
[SASE 통합 (2019~)]
네트워크+보안+CSB 통합
Gartner SASE 프레임워크
      |
      v
[현재: AI FinOps]
AI 비용 예측/최적화
자동 Right-Sizing
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. CSB는 여행사 — 여러 항공사(AWS, Azure, GCP)를 비교해서 가장 좋은 것 골라주고, 패키지로 묶어주고, 보험(보안)까지 추가!
2. CASB는 회사 클라우드 경비원 — 직원이 개인 드롭박스에 기밀 파일 올리면 차단. 허락된 클라우드만 사용 가능!
3. FinOps는 클라우드 가계부 — 5억 쓰다가 가계부 열어보니 2,400만원 낭비 발견. 끄고 줄이니 1.7억원 절감!
