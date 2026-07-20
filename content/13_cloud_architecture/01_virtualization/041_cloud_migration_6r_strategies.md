---
title: "Cloud Migration 6R"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 41
---
> **핵심 인사이트**
> 1. 클라우드 마이그레이션 6R 전략은 AWS가 Gartner의 5Rs를 확장한 클라우드 이전 유형 분류 체계로, Retire(폐기)·Retain(유지)·Rehost(리호스트)·Replatform(리플랫폼)·Repurchase(재구매)·Refactor/Re-architect(재설계)의 6가지 경로를 제시한다.
> 2. 대부분의 기업 클라우드 전환에서 포트폴리오 분석 시 Rehost(Lift & Shift)가 60~70%를 차지하며 가장 빠른 이전이 가능하지만, 클라우드 네이티브 이점 극대화는 Refactor에서만 온전히 실현된다.
> 3. 6R 전략 선택의 핵심 변수는 비즈니스 가치(Value)·기술 복잡도·시간 제약·비용 효율성의 트레이드오프이며, 단일 전략이 아닌 애플리케이션별 맞춤 전략 선택이 성공적인 클라우드 전환의 원칙이다.

---

## Ⅰ. 6R 전략 개요

```
Cloud Migration 6R 전략:

[Retire] 폐기
  더 이상 사용하지 않는 시스템 종료
  클라우드 이전 없이 제거
  비율: 포트폴리오의 10~20%

[Retain] 유지 (보류)
  현재는 클라우드 이전 불필요 또는 불가
  레거시 의존성, 규제, 라이선스 문제

[Rehost] 리호스트 (Lift & Shift)
  수정 없이 그대로 클라우드 VM으로 이전
  빠르고 낮은 위험
  클라우드 최적화 없음 (비용 절감 제한)

[Replatform] 리플랫폼 (Lift, Tinker & Shift)
  핵심 아키텍처 유지, 일부 클라우드 서비스 활용
  예: DB -> RDS 이관, 앱서버 -> 관리형 컨테이너

[Repurchase] 재구매 (Drop & Shop)
  기존 솔루션 폐기 후 SaaS 전환
  예: 온프레미스 CRM -> Salesforce

[Refactor] 재설계 (Re-architect)
  클라우드 네이티브로 완전 재설계
  마이크로서비스, 서버리스, 컨테이너
  최고 비용·시간, 최대 클라우드 효과
```

> 📢 **섹션 요약 비유**: 6R은 이사 전략 — 버리기(Retire), 냅두기(Retain), 그대로 옮기기(Rehost), 일부 업그레이드(Replatform), 새로 구입(Repurchase), 완전 리모델링(Refactor).

---

## Ⅱ. 각 전략 상세 비교

```
6R 전략 상세 비교표:

전략         | 변경 수준 | 이전 속도 | 클라우드 효과 | 위험도
-------------|---------|---------|------------|-------
Retire       | 없음    | 즉시    | N/A        | 없음
Retain       | 없음    | 보류    | 낮음       | 낮음
Rehost       | 최소    | 빠름    | 중간       | 낮음
Replatform   | 부분    | 중간    | 높음       | 중간
Repurchase   | 높음    | 중간    | 높음       | 중간
Refactor     | 완전    | 느림    | 최고       | 높음

Rehost 특징:
  AWS Migration Hub, Server Migration Service
  VMware -> EC2 직접 이전
  비용: 온프레미스 대비 10~20% 절감

Replatform 특징:
  RDS 전환 (DB 관리 부담 감소)
  ECS/EKS 도입 (컨테이너화)
  코드 변경 최소화 + 클라우드 이점 일부 획득

Refactor 특징:
  MSA (마이크로서비스 아키텍처)
  Lambda/Fargate (서버리스)
  12-Factor App 원칙 적용
  비용: 최대 40~60% 절감 (올바르게 설계 시)
```

> 📢 **섹션 요약 비유**: Rehost=가구 그대로 이사, Replatform=일부 새 가구로 교체, Refactor=집 전체 인테리어 리모델링 — 효과와 비용 모두 비례.

---

## Ⅲ. 포트폴리오 분석 방법

```
애플리케이션 포트폴리오 분석:

1. 인벤토리 수집:
   모든 앱, 서버, DB, 의존성 파악
   7R 질문: 주요 기능, 사용 빈도, 기술 부채

2. 평가 기준:
   비즈니스 가치 (높음/중간/낮음)
   기술 복잡도 (높음/중간/낮음)
   클라우드 이전 용이성

3. 분류 매트릭스:

  비즈니스 가치
  ^ 높음  | Replatform | Refactor    |
           | 또는       |             |
  중간     | Rehost     | Replatform  |
           |            |             |
  낮음     | Retire     | Retain      |
           +------------+-------------->
                낮음         높음
                  기술 복잡도

4. 마이그레이션 파동 (Wave) 계획:
   Wave 1 (3~6개월): 간단한 Rehost 앱
   Wave 2 (6~12개월): Replatform 앱
   Wave 3 (12~24개월): Refactor 핵심 앱

5. 의존성 분석:
   앱 간 의존성 맵 -> 이전 순서 결정
   사이클릭 의존성 해소 후 이전
```

> 📢 **섹션 요약 비유**: 포트폴리오 분석은 이사 짐 분류 — 자주 쓰는 것(가치 높음)은 먼저, 무거운 것(복잡한 것)은 나중에, 쓸모없는 것(폐기)은 버리기.

---

## Ⅳ. 마이그레이션 주요 도구

```
6R별 주요 도구 (AWS 기준):

공통:
  AWS Migration Hub: 마이그레이션 추적
  AWS Application Discovery Service: 의존성 발견

Rehost:
  AWS Server Migration Service (SMS)
  VMware Cloud on AWS
  CloudEndure Migration

Replatform:
  AWS Database Migration Service (DMS)
  Amazon ECS/EKS (컨테이너화)
  AWS Elastic Beanstalk

Repurchase:
  AWS Marketplace SaaS 제품
  Salesforce, SAP, ServiceNow 이전

Refactor:
  AWS Lambda (서버리스)
  Amazon EKS (쿠버네티스)
  AWS Step Functions (워크플로우)
  Amazon API Gateway

비용 분석 도구:
  AWS Migration Evaluator (TCO 분석)
  AWS Cost Explorer (이전 후 비용 추적)

타사 클라우드:
  Azure Migrate
  Google Cloud Migrate for Compute Engine
```

> 📢 **섹션 요약 비유**: 마이그레이션 도구는 이사 전문 업체 서비스 — Rehost는 용달 트럭, Refactor는 인테리어 회사.

---

## Ⅴ. 실무 시나리오 — 금융기관 클라우드 전환

```
금융기관 B사 클라우드 전환 사례:

배경:
  온프레미스 220개 애플리케이션
  데이터센터 계약 만료 18개월

포트폴리오 분석 결과:

Retire (15개, 6.8%):
  사용 없는 레거시 시스템
  즉시 폐기, 비용 절감

Retain (25개, 11.4%):
  규제/컴플라이언스 제약 시스템
  온프레미스 유지 (하이브리드)

Rehost (120개, 54.5%):
  Wave 1~2에서 빠른 이전
  평균 이전 기간: 4.2주/앱
  비용 절감: 18%

Replatform (35개, 15.9%):
  DB -> RDS, 앱서버 -> ECS 이관
  관리 부담 40% 감소

Repurchase (10개, 4.5%):
  HR, 이메일 -> SaaS 전환

Refactor (15개, 6.8%):
  핵심 거래 시스템 MSA 재설계
  Wave 3 (12~24개월)

결과 (18개월 완료):
  인프라 비용: 35% 절감
  장애 복구 시간(RTO): 4시간 -> 15분
  배포 빈도: 월 2회 -> 주 3회
```

> 📢 **섹션 요약 비유**: 금융기관 6R 전환은 대형 병원 이전 — ICU(핵심 거래)는 정밀 Refactor, 일반 병실(일반 앱)은 빠른 Rehost, 쓰지 않는 장비는 폐기.

---

## 📌 관련 개념 맵

```
클라우드 마이그레이션 6R
+-- 전략 분류
|   +-- Retire, Retain (이전 안 함)
|   +-- Rehost (Lift & Shift)
|   +-- Replatform (일부 변경)
|   +-- Repurchase (SaaS 전환)
|   +-- Refactor (완전 재설계)
+-- 포트폴리오 분석
|   +-- 비즈니스 가치 × 기술 복잡도 매트릭스
|   +-- Wave 계획
+-- 연관 개념
    +-- 클라우드 네이티브, MSA
    +-- TCO 분석, Migration Hub
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Gartner 5Rs 발표 (2010)]
클라우드 이전 전략 체계화
      |
      v
[AWS 6Rs 확장 (2016~)]
Retire 추가, 실무 표준화
Migration Hub, Discovery Service
      |
      v
[클라우드 퍼스트 정책 (2018~)]
기업 클라우드 전환 의무화
대규모 Rehost 파동 시작
      |
      v
[클라우드 스마트 전략 (2019~)]
무분별한 Lift & Shift 문제 인식
Refactor 필요성 강조
      |
      v
[현재: 하이브리드 멀티클라우드]
온프레미스 + 클라우드 Retain 병존
FinOps로 비용 최적화 강조
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 이전 6R은 이사할 때 짐 처리 방법 — 버리기(Retire), 그냥 두기(Retain), 그대로 옮기기(Rehost), 일부 새걸로(Replatform), 새로 구매(Repurchase), 완전 새집 꾸미기(Refactor)!
2. 대부분 기업은 빠른 이전을 위해 "그대로 옮기기(Rehost)"를 가장 많이 선택하지만, 진짜 클라우드 혜택은 "완전 새집 꾸미기(Refactor)"에서 나와요.
3. 올바른 전략은 앱마다 달라요 — 중요한 앱은 시간이 걸려도 Refactor, 간단한 앱은 빠른 Rehost로 먼저 이전!
