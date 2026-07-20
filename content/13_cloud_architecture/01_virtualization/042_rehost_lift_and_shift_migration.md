---
title: "Rehost Lift And Shift Migration"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 42
---
> **핵심 인사이트**
> 1. Rehost(Lift & Shift)는 클라우드 6R 전략 중 가장 빠르고 위험이 낮은 방법으로, 온프레미스 워크로드를 코드 수정 없이 클라우드 VM으로 이전하지만 클라우드 네이티브 최적화(PaaS, 서버리스, 오토스케일링)를 활용하지 못해 비용 절감 효과가 제한적이다.
> 2. AWS MGN(Application Migration Service), Azure Migrate, Google Migrate for Compute 엔진 같은 자동화 도구가 Rehost를 대폭 단순화했으나, 성공적인 Rehost는 반드시 네트워크 설계(VPC, 서브넷), 보안 그룹, 스토리지 용량 계획을 사전에 수립해야 한다.
> 3. Rehost는 종착점이 아닌 출발점 — 이전 후 안정화 기간(보통 3~6개월)을 거쳐 Re-platform 또는 Re-architect로 진화하는 단계적 클라우드 여정의 첫 번째 관문이다.

---

## Ⅰ. Rehost 개념 및 6R 위치

```
클라우드 6R 전략 (AWS 기준):

Retire: 사용 안 하는 시스템 폐기
Retain: 현재는 이전 안 함 (온프레미스 유지)
Rehost: 코드 변경 없이 클라우드 VM으로 이전 <- 오늘 주제
Replatform: 최소한의 최적화 (OS 업그레이드, 관리형 DB)
Repurchase: SaaS 전환 (On-prem CRM -> Salesforce)
Refactor/Re-architect: 마이크로서비스, 서버리스 전면 재설계

Rehost 적합 시나리오:
  데이터센터 계약 만료 임박
  규제 준수 목적 (클라우드 전환 의무)
  빠른 이전 필요 (legacy 기술 부채 해소 전)
  개발팀 역량이 현재 클라우드 네이티브 미달

Rehost = Lift & Shift:
  Lift: 온프레미스에서 워크로드 들어올리기
  Shift: 클라우드 환경으로 옮기기
  코드 변경 없음 (OS, 미들웨어, 앱 동일)
```

> 📢 **섹션 요약 비유**: Rehost는 이사할 때 가구를 그대로 옮기는 것 — 가구 배치 최적화(Re-architect)는 나중에, 일단 이사부터!

---

## Ⅱ. Rehost 도구 및 기술

```
주요 Rehost 자동화 도구:

AWS Application Migration Service (MGN):
  에이전트 설치 -> 지속 복제 -> 최종 컷오버
  소요 시간: 복제 완료 후 수분 내 컷오버
  지원: 물리 서버, VMware, 기타 클라우드

Azure Migrate:
  VMware/Hyper-V VM 발견 -> 의존성 분석 -> 이전
  Azure Site Recovery 기반 복제

Google Migrate for Compute Engine:
  VMware 워크로드 -> Google Compute Engine
  스트리밍 방식 (전체 복제 없이 부팅 가능)

이전 방식별 비교:
  에이전트 기반:
    장점: 물리 서버 포함, 세밀한 제어
    단점: 에이전트 설치 권한 필요

  에이전트리스:
    장점: VM에 에이전트 설치 불필요
    단점: 하이퍼바이저 접근 권한 필요

  콜드 마이그레이션:
    장점: 간단
    단점: 다운타임 발생

  핫 마이그레이션 (라이브 복제):
    장점: 다운타임 최소화
    단점: 복잡성, 비용
```

> 📢 **섹션 요약 비유**: Rehost 도구는 이사 회사 — 가구(워크로드)를 카탈로그로 정리하고, 트럭(에이전트)으로 옮기고, 새 집(클라우드)에 배치.

---

## Ⅲ. 사전 설계 — 네트워크 및 보안

```
Rehost 전 필수 설계 항목:

1. 네트워크 설계:
   VPC (Virtual Private Cloud) 구성
   서브넷 계획 (Public/Private/DB 계층)
   CIDR 블록 충돌 방지 (온프레미스 IP 대역과 분리)
   Transit Gateway / VPN / Direct Connect 연결

2. 보안 그룹 설계:
   Whitelist 기반 인바운드 규칙
   포트별 접근 제어 (22/3389/443 등)
   NACLs (Network Access Control Lists) 설계

3. 스토리지 계획:
   EBS 볼륨 유형 선택 (gp3, io2 등)
   기존 스토리지 용량 + 20% 여유
   스냅샷 정책 (RPO 달성)

4. IAM 계획:
   역할(Role) vs 사용자(User) 구분
   최소 권한 원칙 적용

5. 비용 추정:
   온프레미스 vs 클라우드 TCO 비교
   예약 인스턴스 vs 스팟 vs 온디맨드

도구:
  AWS Migration Evaluator
  Azure TCO Calculator
  Google Cloud Pricing Calculator
```

> 📢 **섹션 요약 비유**: 이전 전 설계는 이사 전 평면도 그리기 — 어느 방에 어떤 가구 놓을지 미리 계획 안 하면 이사 당일 혼돈.

---

## Ⅳ. Rehost 절차 및 컷오버

```
Rehost 표준 절차:

Phase 1 — 발견 및 평가:
  인벤토리: 서버 목록, CPU/메모리/스토리지 현황
  의존성 매핑: 서버 간 통신 패턴 분석
  적합성 평가: 라이선스 이슈, OS 지원 여부 확인

Phase 2 — 파일럿 이전:
  비핵심 시스템 선택 (테스트/개발 환경)
  도구 검증 및 절차 확인

Phase 3 — 웨이브 계획:
  의존성 기반 이전 그룹 정의
  각 웨이브별 컷오버 일정

Phase 4 — 복제 및 테스트:
  지속적 데이터 복제 시작
  클라우드에서 테스트 (기능, 성능, 보안)
  사용자 수용 테스트 (UAT)

Phase 5 — 컷오버:
  최종 동기화 (델타 변경분)
  DNS 전환 (Route53 / Azure DNS)
  소스 시스템 트래픽 차단
  클라우드 서비스 라이브

Phase 6 — 안정화:
  모니터링 집중 (CloudWatch, Azure Monitor)
  소스 시스템 유지 (롤백 대비, 통상 30일)
  이슈 해결 후 소스 폐기

RTO/RPO 목표:
  컷오버 다운타임: 최소화 (수분~수시간)
  데이터 손실: 최소화 (마지막 동기화 이후 델타만)
```

> 📢 **섹션 요약 비유**: Rehost 컷오버는 비행기 탑승 — 게이트 닫히는 순간(DNS 전환)이 컷오버, 그 전까지는 탑승 준비(복제, 테스트).

---

## Ⅴ. 실무 한계 및 다음 단계

```
Rehost 한계:

비용:
  클라우드 네이티브 아키텍처 대비 30~50% 비용 증가
  이유: 오토스케일링/PaaS 미활용, 온디맨드 VM 비용

성능:
  네트워크 지연: 온프레미스 대비 레이턴시 증가 가능
  스토리지: 로컬 NVMe -> 네트워크 EBS 성능 차이

보안/컴플라이언스:
  클라우드 보안 모델 적용 필요 (책임 분담 모델)
  라이선스 이슈 (BYOL vs 클라우드 라이선스)

기술 부채:
  레거시 OS/미들웨어 그대로 이전
  클라우드 네이티브 이점 미활용

Rehost 이후 최적화 경로:

  Rehost (리프트 앤 시프트)
        |
        v
  Re-platform (최소 최적화):
    RDS 관리형 DB 전환
    OS 업그레이드 (Amazon Linux 2)
    Elastic Load Balancer 적용
        |
        v
  Re-architect (클라우드 네이티브):
    마이크로서비스 분리
    컨테이너 (ECS/EKS)
    서버리스 (Lambda)
    오토스케일링 그룹

TCO 개선 시점:
  Rehost: 이전 직후 비용 동일 또는 소폭 증가
  Re-platform: 6개월~1년 후 15~25% 절감
  Re-architect: 1~2년 후 40~60% 절감
```

> 📢 **섹션 요약 비유**: Rehost는 첫 집 구매 — 인테리어(최적화)는 나중에, 일단 이사(이전)가 먼저. 살면서 조금씩 고쳐나가는 것.

---

## 📌 관련 개념 맵

```
Rehost (Lift & Shift)
+-- 6R 전략 위치
|   +-- Retire/Retain/Rehost/Replatform/Repurchase/Refactor
+-- 도구
|   +-- AWS MGN, Azure Migrate, Google Migrate
+-- 설계
|   +-- VPC, 보안 그룹, IAM, 스토리지
+-- 절차
|   +-- 발견 -> 파일럿 -> 웨이브 -> 복제 -> 컷오버 -> 안정화
+-- 이후 여정
|   +-- Re-platform -> Re-architect
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[가상화 시대 (2000s)]
VMware 가상 머신, V2V/P2V 이전
      |
      v
[퍼블릭 클라우드 초기 (2008~)]
AWS EC2 등장, 수동 이전 방식
      |
      v
[Lift & Shift 용어 정립 (2013~)]
Gartner 5R -> AWS 6R 프레임워크
      |
      v
[자동화 마이그레이션 도구 (2016~)]
AWS SMS -> MGN, Azure Migrate 출시
복제 기반 자동화 이전
      |
      v
[현재: 하이브리드 마이그레이션]
Rehost + Re-platform 동시 진행
CloudOps 자동화 통합
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. Rehost는 이사할 때 가구를 그대로 옮기는 것 — 가구 디자인(코드)을 바꾸지 않고 새 집(클라우드)으로 이사해요!
2. 빠르게 이사할 수 있지만 새 집 구조에 맞춰 가구를 배치하지 않아 공간 활용이 비효율적일 수 있어요.
3. 이사 후에 조금씩 인테리어(Re-platform -> Re-architect)를 개선하면 결국 훨씬 좋은 집이 돼요.
