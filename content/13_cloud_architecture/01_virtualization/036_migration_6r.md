---
title: "Migration 6R"
date: "2026-03-03"
tags:
  - "studynote-cloud-architecture"
weight: 36
---
> **핵심 인사이트**
> 1. 클라우드 마이그레이션 6R은 Rehost(리호스트)·Replatform(리플랫폼)·Repurchase(리퍼채스)·Refactor(리팩터)·Retire(리타이어)·Retain(리테인)으로 구성된 워크로드별 마이그레이션 전략 프레임워크다.
> 2. 모든 워크로드에 동일한 전략을 적용하는 것이 아니라 비즈니스 가치·기술적 복잡성·TCO(Total Cost of Ownership)를 기준으로 각 애플리케이션에 적합한 R을 선택해야 한다.
> 3. 대부분의 기업은 Rehost(리프트앤시프트)로 빠른 마이그레이션을 시작하고, 이후 Replatform·Refactor로 클라우드 네이티브 최적화를 진행하는 2단계 접근을 취한다.

---

## I. 6R 전략 개요

```
6R 전략 (Gartner + AWS 체계):

1. Rehost   : Lift & Shift (그대로 이전)
2. Replatform: Lift, Tinker & Shift (약간 최적화)
3. Repurchase: SaaS로 교체
4. Refactor : 클라우드 네이티브로 재설계
5. Retire   : 폐기 (사용 안 함)
6. Retain   : 현행 유지 (아직 이전 안 함)

최근 추가: 7th R = Relocate (VMware -> 클라우드 이동)
```

| R          | 변경 수준 | 속도 | 클라우드 최적화 | 비용  |
|-----------|---------|-----|------------|------|
| Rehost    | 없음    | 빠름 | 낮음       | 낮음 |
| Replatform| 최소    | 중간 | 중간       | 중간 |
| Repurchase| 교체    | 빠름 | 높음 (SaaS)| 구독 |
| Refactor  | 완전    | 느림 | 최고       | 높음 |
| Retire    | -       | 즉시 | -          | 절약 |
| Retain    | -       | -    | 없음       | 현행 |

> 📢 **섹션 요약 비유**: 이사할 때 — 그대로 옮기기(Rehost), 일부 정리 후 옮기기(Replatform), 가구 바꾸기(Repurchase), 집을 새로 짓기(Refactor), 쓸모없는 짐 버리기(Retire), 일단 두기(Retain).

---

## II. 각 R 상세 설명

### Rehost — 리프트 앤 시프트 (Lift & Shift)

```
기존: On-Premise 서버
이후: AWS EC2 (동일한 OS, 설정)

장점: 빠른 마이그레이션, 리스크 최소
단점: 클라우드 이점 미활용 (여전히 과도한 사양)
적합: 대량 마이그레이션 첫 단계, 구형 시스템
도구: AWS MGN, Azure Migrate
```

### Replatform — 약간의 최적화

```
기존: EC2 + 직접 관리 DB
이후: EC2 + RDS (관리형 DB로 교체)

변경 범위: OS/런타임 변경 없이 관리 서비스 활용
적합: DB, 미들웨어를 관리형으로 전환
예시: 자체 Tomcat -> AWS Elastic Beanstalk
```

### Repurchase — SaaS로 교체

```
기존: 사내 CRM 시스템 (자체 개발)
이후: Salesforce (SaaS)

적합: 표준화된 비즈니스 기능 (HR, CRM, ERP)
비용: 구축 비용 없음, 구독료
리스크: 데이터 마이그레이션, 사용자 적응
```

> 📢 **섹션 요약 비유**: Replatform은 집 구조는 그대로, 가스레인지만 인덕션으로 바꾸는 것 — 큰 공사 없이 효율은 높인다.

---

## III. Refactor — 클라우드 네이티브 재설계

```
기존: 모놀리식 Java EE 애플리케이션
이후: 마이크로서비스 + Kubernetes + Lambda

변경 범위:
  아키텍처 재설계 (모놀리스 -> MSA)
  서버리스 함수로 분리 (Lambda)
  컨테이너화 (Docker + K8s)
  이벤트 드리븐 아키텍처

비용: 높음 (6-18개월 개발)
이점: 자동 스케일링, 탄력성, 클라우드 최적 비용
```

> 📢 **섹션 요약 비유**: 집을 허물고 새로 짓는 것 — 가장 비싸고 오래 걸리지만, 결과는 현대식 스마트홈이 된다.

---

## IV. 마이그레이션 의사결정 기준

```
워크로드 분류 기준:
  비즈니스 가치 × 기술적 복잡성 매트릭스

              높은 가치   낮은 가치
복잡도 낮음:  Replatform  Rehost/Retire
복잡도 높음:  Refactor    Retain/Retire
```

| 판단 기준        | 질문                              |
|---------------|-----------------------------------|
| 비즈니스 가치   | 이 앱이 핵심 비즈니스에 중요한가?   |
| 기술적 부채     | 현재 아키텍처가 변경하기 쉬운가?    |
| TCO 비교       | 마이그레이션 후 비용이 절감되는가?  |
| 규정 준수       | 클라우드 이전 시 규정 이슈가 있는가?|

> 📢 **섹션 요약 비유**: 모든 짐을 같은 방법으로 옮기지 않듯이 — 골동품은 정성껏, 잡동사니는 버리고, 가구는 그냥 들고 가고.

---

## V. 실무 시나리오 — 은행 코어 시스템 마이그레이션

| 시스템          | 전략     | 이유                            |
|--------------|---------|--------------------------------|
| 웹/앱 서버      | Rehost  | 빠른 인프라 이전, 1단계          |
| 이메일 시스템   | Repurchase | Exchange -> Office365 교체     |
| 데이터 분석     | Replatform | 온프레미스 DB -> AWS RDS Redshift|
| 코어 뱅킹      | Retain   | 규제 준수, 레거시 복잡도 높음    |
| 보고 시스템    | Refactor | 서버리스 + 이벤트 드리븐 재설계  |
| 구형 MIS      | Retire   | 사용자 없음, 5년 된 레거시       |

> 📢 **섹션 요약 비유**: 은행 이전도 금고(코어뱅킹)는 마지막에, 사무용품(이메일)은 서비스로 교체, 오래된 보고서 시스템은 버리고 — 우선순위와 전략이 다르다.

---

## 📌 관련 개념 맵

```
클라우드 마이그레이션 6R
+-- Rehost: Lift & Shift, 빠름
+-- Replatform: 관리형 서비스 활용
+-- Repurchase: SaaS 교체
+-- Refactor: 클라우드 네이티브 재설계
+-- Retire: 폐기
+-- Retain: 현행 유지
+-- 관련 개념
    +-- TCO (Total Cost of Ownership)
    +-- 클라우드 네이티브 (12-Factor App)
    +-- Migration Factory
    +-- CAF (Cloud Adoption Framework)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 클라우드 전환 (2008~)]
Rehost(리프트앤시프트)가 유일한 전략
      |
      v
[5R 프레임워크 (Gartner, 2010s)]
Rehost, Refactor, Revise, Rebuild, Replace
      |
      v
[6R 표준화 (AWS 체계화)]
Retire, Retain 추가
마이그레이션 플레이북 체계화
      |
      v
[현재: 7R + AI 기반 마이그레이션]
Relocate (VMware -> 클라우드)
AWS Migration Hub, Azure Migrate AI 평가
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 이사 방법은 6가지 — 그대로 옮기기, 조금 고쳐 옮기기, 새 것 사기, 완전 새로 만들기, 버리기, 일단 두기예요.
2. 모든 짐을 같은 방법으로 이사하지 않듯이, 각 프로그램에 맞는 방법을 골라야 해요.
3. 비싸고 중요한 짐(코어 시스템)은 천천히 신중하게, 오래된 짐(구형 시스템)은 그냥 버리는 게 현명해요!
