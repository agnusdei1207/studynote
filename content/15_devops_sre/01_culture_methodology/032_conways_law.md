---
title: "Conway's Law"
date: "2026-03-03"
tags:
  - "studynote-devops-sre"
weight: 32
---
> **핵심 인사이트 3줄**
> 1. 콘웨이의 법칙(Conway's Law)은 "조직이 설계하는 시스템은 해당 조직의 커뮤니케이션 구조를 그대로 반영한다"는 원칙으로, 1967년 Mel Conway가 제시했다.
> 2. 역 콘웨이 기동(Inverse Conway Maneuver)은 원하는 아키텍처(마이크로서비스)를 먼저 설계하고, 그에 맞게 팀 구조를 재편해 시스템이 아키텍처를 따르게 하는 전략이다.
> 3. Team Topologies 프레임워크는 콘웨이의 법칙을 의도적으로 활용해 Stream-aligned·Platform·Enabling·Complicated-subsystem 4가지 팀 유형으로 조직을 최적화한다.

---

## Ⅰ. 콘웨이의 법칙 원문과 의미

> *"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."*
> — Mel Conway, 1967

```
조직 구조         ->    시스템 아키텍처
--------------------------------------
팀 A (DB)          ->    DB 레이어
팀 B (백엔드)      ->    API 서버
팀 C (프론트엔드)  ->    UI 레이어
팀 D (인프라)      ->    인프라 레이어
```

### 왜 발생하는가?

- 팀 간 커뮤니케이션 비용이 높아 경계를 시스템 경계로 만든다
- 팀 내부는 강하게 결합(high cohesion), 팀 간은 느슨하게 결합(loose coupling)
- 조직의 권력 구조가 API 설계에 반영된다

📢 **섹션 요약 비유**: 콘웨이의 법칙은 "회사 조직도가 곧 소프트웨어 구조도"라는 법칙이다 — 부서가 나뉘어 있으면 코드도 똑같이 나뉜다.

---

## Ⅱ. 콘웨이의 법칙 실제 사례

### 사례 1 — 모놀리식 -> 마이크로서비스 실패

```
기존 조직: 단일 개발팀 (모놀리식 아키텍처)
     v
마이크로서비스 도입 시도 (팀 구조 변경 없음)
     v
결과: "분산 모놀리식" — 서비스는 분리됐지만
     팀이 같아 경계가 없고, 배포도 함께 진행
```

### 사례 2 — Amazon Two-Pizza Rule

```
팀 크기: 피자 두 판으로 먹일 수 있는 인원 (6~10명)
   v
자체 소유 서비스 -> 독립 배포 -> 마이크로서비스 아키텍처
```

- 팀이 작아야 서비스도 작고 독립적이 된다

📢 **섹션 요약 비유**: 콘웨이의 법칙 사례는 집 설계와 같다 — 가족이 3명인데 방 10개짜리 집을 지으면 빈 방만 생기고, 10명 대가족에게 방 2개짜리 집은 혼돈이 된다.

---

## Ⅲ. 역 콘웨이 기동 (Inverse Conway Maneuver)

역 콘웨이 기동(Inverse Conway Maneuver)은 <strong>원하는 시스템 아키텍처를 먼저 정의하고, 그 아키텍처를 자연스럽게 만들어낼 수 있는 팀 구조로 조직을 재편</strong>하는 전략이다.

```
원하는 아키텍처 결정 (마이크로서비스)
     v
서비스 경계 정의 (도메인 주도 설계, DDD)
     v
팀을 서비스 경계에 맞게 재구성
     v
각 팀이 독립적으로 자기 서비스 소유·배포
     v
시스템 아키텍처가 자연스럽게 마이크로서비스가 됨
```

📢 **섹션 요약 비유**: 역 콘웨이 기동은 선수 포지션에 맞게 팀을 짜는 것이다 — 포워드 공격 전술(아키텍처)을 먼저 결정하고, 그 포지션에 맞는 선수(팀원)를 배치한다.

---

## Ⅳ. Team Topologies — 콘웨이 법칙의 의도적 활용

Matthew Skelton·Manuel Pais가 제시한 <strong>Team Topologies 프레임워크</strong>는 4가지 팀 유형으로 조직을 최적화한다.

| 팀 유형                     | 역할                              | 예시                    |
|---------------------------|----------------------------------|------------------------|
| Stream-aligned Team        | 고객 가치 흐름 직접 제공           | 주문·결제·배송 팀        |
| Platform Team              | 내부 플랫폼 제공, 인지 부하 감소   | 인프라·CI/CD·관측성 팀  |
| Enabling Team              | 역량 전파·CoP(실천 공동체) 지원   | DevOps·보안 전문가 팀   |
| Complicated-Subsystem Team | 특수 도메인 전문성 집중            | ML·암호화·결제 게이트웨이|

### 팀 상호작용 모드

```
Collaboration: 함께 문제 해결 (일시적)
X-as-a-Service: 플랫폼 소비 (상시)
Facilitating: 지식 전수 (한시적)
```

📢 **섹션 요약 비유**: Team Topologies는 축구 팀 포메이션이다 — 공격수(Stream-aligned), 미드필더(Platform), 코치(Enabling), 골키퍼(Complicated-subsystem)가 각자의 역할을 명확히 해야 팀이 잘 돌아간다.

---

## Ⅴ. 콘웨이 법칙과 DevOps 문화

### 조직 사일로(Silo) 문제

```
개발팀 [Dev] ------- 벽 ------- 운영팀 [Ops]
   |                                   |
 코드 배포 요청                 배포 거부/지연
   |                                   |
 "운영이 막는다"               "개발이 불안정하다"
```

### DevOps로 해결

```
Before (콘웨이 법칙 폐해):
  Dev팀 -> Ops팀 -> 배포 -> SRE팀 (각각 다른 도구·문화)

After (역 콘웨이 기동):
  풀스택 Product Team (Dev+Ops+QA 통합)
  -> You Build It, You Run It (아마존 원칙)
```

📢 **섹션 요약 비유**: DevOps는 요리사가 직접 홀 서빙도 하는 구조다 — 요리(개발)와 서비스(운영)를 한 팀이 담당하면 음식이 맛없으면 본인도 직접 고객 불만을 듣게 된다.

---

## 📌 관련 개념 맵

```
콘웨이의 법칙 (Conway's Law)
+-- 핵심 주장
|   +-- 조직 커뮤니케이션 구조 = 시스템 아키텍처
+-- 활용 전략
|   +-- 역 콘웨이 기동 (Inverse Conway Maneuver)
|   +-- DDD (Domain-Driven Design) 경계 설정
+-- 조직 설계 프레임워크
|   +-- Team Topologies
|   |   +-- Stream-aligned Team
|   |   +-- Platform Team
|   |   +-- Enabling Team
|   |   +-- Complicated-Subsystem Team
|   +-- Spotify 모델 (Squad·Tribe·Chapter·Guild)
+-- 연관 개념
    +-- Two-Pizza Rule (Amazon)
    +-- DevOps / SRE
    +-- 마이크로서비스 아키텍처
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              콘웨이의 법칙 발전 흐름                             |
+--------------+--------------------+-----------------------------+
| 1967년       | Conway 논문 발표   | "How Do Committees Invent?"  |
| 2000년대     | 마이크로서비스 등장 | 콘웨이 법칙 재조명           |
| 2010년       | Thoughtworks 검증  | 역 콘웨이 기동 개념화        |
| 2014년       | Spotify 모델 공개  | 팀 설계 실전 사례            |
| 2019년       | Team Topologies 책  | 체계적 팀 위상 설계          |
| 2020년대     | Platform Engineering| 내부 개발자 플랫폼 표준화   |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
조직 구조 -> 콘웨이 법칙 -> 시스템 아키텍처 미러링
    v              v
팀 설계 -> 역 콘웨이 -> MSA 자연스러운 구현
    v
Team Topologies -> Platform Engineering -> 인지 부하 최소화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 콘웨이의 법칙은 "동네 친구끼리 팀을 만들면 동네별로 팀이 나뉜다"는 법칙이다 — 어울리는 사람들이 같은 팀(코드 모듈)이 된다.
2. 역 콘웨이 기동은 포지션을 먼저 정하고 선수를 뽑는 것이다 — 공격수 전술을 먼저 짜고, 그 포지션에 맞는 선수를 선발한다.
3. Team Topologies는 회사 조직도를 소프트웨어 설계도처럼 그리는 것이다 — 팀 경계가 곧 서비스 경계가 되도록 의도적으로 구성한다.
