---
title: "Refactor Re Architect Cloud Native Msa"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 44
---
> **핵심 인사이트**
> 1. Re-factor(재구성)와 Re-architect(재설계)는 클라우드 마이그레이션 6R 전략의 가장 높은 가치를 창출하는 단계로 — Re-factor는 애플리케이션 코드를 PaaS/서버리스에 최적화하고, Re-architect는 모놀리스를 MSA(Microservices Architecture)로 근본적으로 재설계한다.
> 2. MSA 전환의 핵심 원칙은 도메인 주도 설계(DDD)의 바운디드 컨텍스트(Bounded Context)를 서비스 경계로 삼는 것으로 — 각 마이크로서비스는 독립적으로 배포·확장·장애 격리가 가능해야 하며, "두 피자 팀(Two-Pizza Team)"이 소유·운영할 수 있는 크기가 적절하다.
> 3. MSA 전환은 Strangler Fig Pattern(교살 무화과 패턴)으로 점진적으로 진행하는 것이 권장되며 — 모놀리스를 즉시 전부 전환하는 "Big Bang" 방식은 서비스 중단 리스크와 복잡성으로 인해 대부분 실패한다.

---

## Ⅰ. 클라우드 마이그레이션 6R

```
6R 마이그레이션 전략:

1. Retire (폐기):
   더 이상 필요 없는 애플리케이션 폐기
   예: 중복 CRM 시스템

2. Retain (유지):
   현재 온프레미스 유지 (규제, 레이턴시)
   예: 실시간 금융 거래 코어

3. Rehost (리호스팅, Lift & Shift):
   코드 변경 없이 클라우드로 이전
   빠르지만 클라우드 혜택 최소화

4. Replatform (리플랫폼):
   소규모 최적화 (RDS로 DB 이전 등)
   코드 변경 최소화

5. Re-factor / Re-purchase (재구성):
   클라우드 네이티브로 코드 재작성
   PaaS, 서버리스 활용

6. Re-architect (재설계):
   아키텍처 근본 변경 (MSA 전환)
   가장 많은 투자, 가장 큰 가치

Re-factor vs Re-architect:
  Re-factor:
    기존 기능 유지, 구현 방식 변경
    예: 모놀리스 -> Lambda + DynamoDB

  Re-architect:
    기능 분리, 서비스 경계 재정의
    예: 모놀리스 -> 10개 마이크로서비스

투자 vs 가치:
  Rehost: 비용 20~30% 절감 (이전 비용 낮음)
  Replatform: 비용 40~50% 절감
  Re-architect: 비용 60~80% 절감 + 민첩성 향상
```

> 📢 **섹션 요약 비유**: 6R은 이사 전략 — 짐 그대로 옮기기(Rehost), 조금 정리하기(Replatform), 새로 디자인하기(Re-architect). 비용은 커지지만 새 집을 제대로 활용할수록 효과도 커요.

---

## Ⅱ. MSA 설계 원칙

```
MSA (Microservices Architecture) 원칙:

핵심 원칙:
  1. 단일 책임 (Single Responsibility):
     하나의 서비스 = 하나의 비즈니스 기능

  2. 독립 배포 (Independent Deployment):
     각 서비스 독립적 CI/CD

  3. 기술 다양성 (Polyglot):
     서비스별 적합한 언어/DB 선택

  4. 장애 격리 (Fault Isolation):
     서비스 A 장애 -> 서비스 B 영향 최소화

  5. 분산 데이터 (Decentralized Data):
     서비스별 독립적 DB

DDD (Domain-Driven Design) 기반 서비스 분리:
  바운디드 컨텍스트 = 서비스 경계

  이커머스 도메인 분리:
  모놀리스: 하나의 코드베이스
    +-- 사용자, 주문, 상품, 결제, 배송...

  MSA:
    사용자 서비스 (User Service)
    상품 서비스 (Product Service)
    주문 서비스 (Order Service)
    결제 서비스 (Payment Service)
    배송 서비스 (Delivery Service)
    알림 서비스 (Notification Service)

서비스 통신:
  동기: REST API, gRPC
  비동기: 메시지 큐 (Kafka, RabbitMQ)

  이벤트 소싱 (Event Sourcing):
  상태 대신 이벤트 로그로 상태 재현

  CQRS (Command Query Responsibility Segregation):
  쓰기(Command)와 읽기(Query) 분리

Two-Pizza Team:
  Amazon: "팀이 피자 두 판으로 먹을 수 있는 규모" = 6~8명
  하나의 마이크로서비스 = 하나의 팀이 소유·운영
```

> 📢 **섹션 요약 비유**: MSA는 레스토랑 -> 푸드코트 전환 — 하나의 주방(모놀리스)에서 모든 요리를 만들다가, 각 음식별 전문점(마이크로서비스)으로 분리. 피자 가게가 파스타 가게와 독립적으로 운영.

---

## Ⅲ. Strangler Fig Pattern

```
Strangler Fig Pattern (교살 무화과 패턴):
  Martin Fowler 제안
  모놀리스 -> MSA 점진적 전환 전략

이름 유래:
  교살 무화과나무: 기존 나무를 감으며 천천히 대체
  -> 기존 시스템을 유지하면서 새 시스템이 점진적 대체

전환 단계:
  Stage 1: API Gateway 도입
    모든 트래픽 -> API Gateway
    처음에는 모두 모놀리스로 라우팅

  Stage 2: 기능 분리 시작
    가장 독립적인 기능부터 추출
    알림 서비스: 모놀리스에서 분리 (낮은 의존성)
    Gateway -> 알림: 신규 서비스
    Gateway -> 나머지: 모놀리스

  Stage 3: 점진적 분리 계속
    배송 -> 상품 -> 결제 순서로 분리
    각 분리 후 검증 (A/B 트래픽)

  Stage 4: 모놀리스 최소화
    핵심 기능만 남은 모놀리스

  Stage 5: 완전 대체
    모놀리스 폐기

Anti-Pattern (Big Bang):
  전체를 한번에 재설계
  -> 수개월~수년의 "개발 블랙홀"
  -> 서비스 중단 리스크
  -> 대부분 실패

Strangler 장점:
  비즈니스 연속성 유지
  점진적 위험 관리
  팀 학습 곡선 완화
```

> 📢 **섹션 요약 비유**: Strangler Fig는 점진적 집 수리 — 사람이 살면서 방 하나씩 리모델링. 전체 집을 비우고 한꺼번에 고치면(Big Bang) 살 곳이 없어지는 위험.

---

## Ⅳ. 클라우드 네이티브 패턴

```
클라우드 네이티브 패턴:

1. Circuit Breaker (회로 차단기):
   연쇄 장애 방지

   상태: Closed -> Open -> Half-Open
   실패 임계값 초과 시 Open -> 빠른 실패 반환
   일정 시간 후 Half-Open -> 재시도 허용

   도구: Resilience4j, Hystrix

2. Service Mesh:
   서비스 간 통신 인프라를 사이드카 프록시로 관리

   기능: 로드밸런싱, 암호화, 트레이싱, 레이트 리미팅

   Istio: 가장 많이 사용되는 Service Mesh
   Envoy 사이드카 프록시

3. API Gateway:
   단일 진입점 (Single Entry Point)
   인증, 라우팅, 로드밸런싱, 로깅

   AWS API Gateway, Kong, nginx

4. Sidecar Pattern:
   메인 컨테이너 옆에 보조 컨테이너
   로깅, 모니터링, 보안 에이전트

5. Saga Pattern:
   분산 트랜잭션 처리

   Choreography Saga: 이벤트 기반 자율 조율
   Orchestration Saga: 중앙 조율자(Orchestrator)

쿠버네티스(Kubernetes) 기반:
  컨테이너 오케스트레이션 표준
  자동 확장 (HPA, VPA)
  자가 치유 (Self-Healing)
  롤링 업데이트
  서비스 디스커버리
```

> 📢 **섹션 요약 비유**: Circuit Breaker는 전기 차단기 — 한 서비스가 망가져서 요청이 계속 오면, 전기 차단기처럼 "뚝!" 차단해서 전체 시스템이 쓰러지지 않도록 보호해요.

---

## Ⅴ. 실무 시나리오 — 이커머스 MSA 전환

```
대형 이커머스 모놀리스 -> MSA 전환:

배경:
  Java 모놀리스: 200만 라인 코드
  문제: 배포 6시간, 특정 기능 확장 불가
  목표: 마이크로서비스로 전환

전환 전략: Strangler Fig

Phase 1 (Q1): API Gateway 도입
  Kong Gateway 앞단 배치
  기존 모놀리스 유지
  -> 영향 없이 인프라 준비

Phase 2 (Q2): 알림 서비스 분리
  이메일/SMS 발송 기능 추출
  모놀리스 코드 비활성화
  Gateway에서 알림 요청 -> 신규 서비스 라우팅
  A/B 테스트로 안전 검증

  기술: Python FastAPI + AWS SQS + Lambda

Phase 3 (Q3~Q4): 상품/카탈로그 분리
  가장 높은 조회 트래픽 -> 독립 확장 필요
  기술: Go + Redis + Elasticsearch

  오토스케일링 효과:
  기존: 전체 모놀리스 스케일업 (비효율)
  신규: 상품 서비스만 스케일 (20->200 인스턴스)

Phase 4~6 (다음 해): 주문/결제/배송 분리

결과 (2년 후):
  배포 시간: 6시간 -> 15분
  장애 격리: 알림 장애 -> 결제 영향 없음
  팀 자율성: 각 팀 독립 배포 주 3회 이상
  인프라 비용: 20% 절감 (세밀한 스케일링)

교훈:
  서비스 경계 결정이 가장 중요 (DDD 필수)
  공유 DB 문제: 서비스마다 DB 분리가 핵심 난제
  분산 트랜잭션: Saga 패턴으로 해결
```

> 📢 **섹션 요약 비유**: 이커머스 MSA 전환은 대형마트 -> 전문점 거리 — 모든 것 파는 대형마트(모놀리스)를 식료품점·전자제품점·의류점(마이크로서비스)으로 분리. 각 점포가 독립적으로 영업!

---

## 📌 관련 개념 맵

```
Re-architect / MSA
+-- 설계 원칙
|   +-- DDD 바운디드 컨텍스트
|   +-- Two-Pizza Team
|   +-- 독립 배포, 분산 데이터
+-- 전환 전략
|   +-- Strangler Fig Pattern (점진적)
|   +-- 6R (Rehost~Re-architect)
+-- 패턴
|   +-- Circuit Breaker, Service Mesh
|   +-- Saga, API Gateway
+-- 인프라
|   +-- Kubernetes, 컨테이너
|   +-- Istio Service Mesh
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[SOA (2000s)]
서비스 지향 아키텍처 (무거운 ESB)
      |
      v
[MSA 개념화 (2014)]
Martin Fowler/James Lewis 명문화
Netflix, Amazon 사례 공개
      |
      v
[컨테이너 + 쿠버네티스 (2015~)]
Docker + K8s: MSA 인프라 표준
Service Mesh (Istio) 등장
      |
      v
[클라우드 네이티브 패턴 (2018~)]
CNCF: 표준 패턴 정립
Circuit Breaker, Saga 표준화
      |
      v
[현재: 서버리스 MSA]
Lambda Function as a Service
이벤트 드리븐 MSA 아키텍처
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. MSA는 대형마트 -> 전문점 거리 전환 — 하나의 큰 가게(모놀리스) 대신, 각 물건별 전문점(마이크로서비스)으로 분리해서 각자 독립 운영해요!
2. Strangler Fig는 점진적 집 수리 — 한꺼번에 헐고 짓는 대신(Big Bang), 사람이 살면서 방 하나씩 리모델링. 훨씬 안전해요.
3. Circuit Breaker는 전기 차단기 — 서비스 하나가 망가졌을 때 전체로 퍼지지 않도록 "뚝!" 차단해서 시스템을 보호해요!
