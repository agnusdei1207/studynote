---
title: "SABSA (Sherwood Applied Business Security Architecture)"
date: "2026-04-05"
tags:
  - "studynote-security"
weight: 42
---
> **핵심 인사이트**
> 1. SABSA(Sherwood Applied Business Security Architecture)는 자크만 프레임워크(Zachman Framework)를 보안에 특화 적용한 보안 아키텍처 방법론으로, 비즈니스 요구사항에서 시작하여 논리·물리·기술 계층까지 "위에서 아래로(Top-down)" 보안을 설계하는 완전한 생명주기 프레임워크다.
> 2. SABSA의 6대 계층(Contextual->Conceptual->Logical->Physical->Component->Operational)과 6대 속성 열(What/How/Where/Who/When/Why)의 36셀 매트릭스는 비즈니스 컨텍스트부터 운영 절차까지 보안 아키텍처의 완전성을 보장한다.
> 3. SABSA의 가장 강력한 특징은 "비즈니스 목표 -> 보안 정책 -> 보안 아키텍처 -> 보안 통제"로 이어지는 추적 가능성(Traceability)으로, 각 보안 투자가 어떤 비즈니스 리스크를 해소하는지 경영진에게 설명할 수 있다.

---

## Ⅰ. SABSA 개요

```
SABSA (Sherwood Applied Business Security Architecture):

개발: John Sherwood, Andrew Clark, David Lynas
발표: 1995년 (영국 보안 컨퍼런스)
특징: 비즈니스 중심, 위험 기반 보안 설계

핵심 철학:
  "보안은 비즈니스를 위해 존재한다"
  기술 보안 솔루션 -> 비즈니스 요구사항 역추적
  불가능 (Top-down 설계 필요)

SABSA vs 타 프레임워크:
  SABSA: 보안 특화 아키텍처 방법론
  TOGAF: 일반 EA 방법론 (보안은 부분)
  ISO 27001: 보안 관리 체계 (운영)

  결합 사용:
  TOGAF(EA 프로세스) + SABSA(보안 아키텍처)
  SABSA 아키텍처 + ISO 27001 운영 체계

SABSA 활용 분야:
  금융, 의료, 국방, 정부 IT 보안 설계
  클라우드 보안 아키텍처
  Zero Trust 아키텍처 설계
```

> 📢 **섹션 요약 비유**: SABSA는 건물 보안 설계 도면 — 건물주 요구(비즈니스)에서 시작해서 자물쇠 규격(기술)까지 위에서 아래로 설계하는 완전한 청사진.

---

## Ⅱ. SABSA 6층 매트릭스

```
SABSA 아키텍처 레이어:

Row 1: Contextual (비즈니스 컨텍스트):
  What: 비즈니스 자산, 보호 대상
  Why:  비즈니스 리스크, 목표
  대상: CEO, 이사회

Row 2: Conceptual (개념 모델):
  What: 정보 보안 정책 목적
  How:  비즈니스 프로세스 보안 요구
  대상: CISO, 보안 전략 담당

Row 3: Logical (논리 보안 서비스):
  What: 정보 분류, 논리 자산
  How:  보안 서비스 (인증, 암호화, 로깅)
  대상: 보안 아키텍트

Row 4: Physical (물리 보안 메커니즘):
  What: 물리 자산 (서버, 네트워크)
  How:  보안 솔루션 (방화벽, IAM, SIEM)
  대상: 보안 엔지니어

Row 5: Component (보안 컴포넌트):
  What: 보안 제품/툴 사양
  How:  설정 파라미터, 규칙
  대상: 보안 관리자

Row 6: Operational (운영):
  What: 실제 보안 절차
  How:  운영 지침, SOP
  대상: 보안 운영팀 (SOC)
```

> 📢 **섹션 요약 비유**: SABSA 6층은 건물 층별 역할 — CEO(최고층), CISO(임원층), 아키텍트(설계층), 엔지니어(시공층), 관리자(설비층), 운영팀(현장).

---

## Ⅲ. SABSA 속성 (6질문)

```
SABSA 6대 속성 열:

What (자산): 무엇을 보호하는가?
  데이터, 시스템, 비즈니스 프로세스

How (기능): 어떻게 보안을 제공하는가?
  인증, 권한, 암호화, 감사

Where (위치): 어디에 보안을 적용하는가?
  경계(경계 보안), 네트워크, 시스템 내부

Who (사람): 누가 접근하는가?
  사용자 역할, 조직 구조, IAM

When (시간): 언제 보안이 필요한가?
  이벤트 기반, 세션, 주기적 감사

Why (동기): 왜 이 보안이 필요한가?
  비즈니스 리스크, 규제 컴플라이언스

SABSA 속성 분류 (Security Attributes):
  비즈니스 속성에서 보안 속성 도출

  예: "고객 신뢰 유지" (비즈니스 속성)
   -> "데이터 무결성 보장" (보안 속성)
   -> "DB 접근 감사 + 변경 불가 로그" (통제)
```

> 📢 **섹션 요약 비유**: SABSA 6질문은 보안 6하원칙 — 무엇을(What), 어떻게(How), 어디서(Where), 누가(Who), 언제(When), 왜(Why) 보호하는가.

---

## Ⅳ. SABSA 추적 가능성

```
SABSA 추적 가능성 (Traceability):

비즈니스 목표 -> 보안 통제 추적:

Level 1 (Contextual):
  비즈니스 리스크: "고객 개인정보 유출 시 법적 책임"

Level 2 (Conceptual):
  보안 목표: "개인정보 접근 최소화 및 감사"

Level 3 (Logical):
  보안 서비스: 접근 제어(IAM), 감사 로깅

Level 4 (Physical):
  보안 메커니즘: RBAC, SIEM, 암호화

Level 5 (Component):
  제품 사양: AWS IAM Policy, ELK Stack

Level 6 (Operational):
  운영 절차: 분기별 접근 권한 리뷰 SOP

가치:
  각 보안 투자 -> 비즈니스 리스크 해소 연결
  보안 ROI 설명 가능
  감사(Audit) 시 근거 제공

SABSA Business Attributes Profile:
  비즈니스 요구사항 -> 보안 속성으로 변환
  표준 약 40개 비즈니스 속성 카탈로그
```

> 📢 **섹션 요약 비유**: SABSA 추적 가능성은 회사 보안 투자 영수증 — "이 방화벽은 고객 개인정보 유출 리스크(비즈니스)를 막기 위한 것"을 증명하는 근거.

---

## Ⅴ. 실무 시나리오 — 클라우드 SABSA 적용

```
금융기관 클라우드 보안 아키텍처 SABSA 적용:

배경:
  레거시 온프레미스 -> AWS 클라우드 전환
  SABSA 기반 클라우드 보안 설계

Level 1 (Contextual) 분석:
  비즈니스 리스크: 금융 거래 데이터 유출
  규제 요구: 전자금융감독규정, PCI DSS
  목표: "고객 거래 데이터 기밀성·무결성 보장"

Level 2 (Conceptual) 보안 정책:
  "Zero Trust: 기본 거부, 명시적 허용"
  "최소 권한 원칙 전면 적용"
  "모든 접근 감사 로그 3년 보존"

Level 3 (Logical) 보안 서비스:
  IAM (신원 및 접근 관리)
  암호화 서비스 (전송 중/정지 상태)
  보안 이벤트 모니터링

Level 4 (Physical) 구현:
  AWS IAM + Cognito (인증/권한)
  AWS KMS (키 관리)
  AWS Security Hub + GuardDuty (SIEM)
  VPC + Security Group (네트워크 격리)

Level 6 (Operational):
  분기별 IAM 접근 권한 리뷰
  일일 보안 이벤트 모니터링
  연간 침투 테스트

결과:
  ISMS-P 인증 통과
  PCI DSS Level 1 준수 확인
  금융감독원 보안 감사 통과
```

> 📢 **섹션 요약 비유**: SABSA 클라우드 적용은 은행 금고 설계 — 은행장 요구(Level 1)에서 열쇠 규격(Level 5)까지 일관된 설계로 틈 없는 보안 구축.

---

## 📌 관련 개념 맵

```
SABSA
+-- 구조
|   +-- 6층 아키텍처 레이어
|   +-- 6대 속성 열 (What/How/Where/Who/When/Why)
|   +-- 36셀 보안 매트릭스
+-- 특징
|   +-- 비즈니스 중심 Top-down 설계
|   +-- 추적 가능성 (Traceability)
+-- 관계
|   +-- 자크만 프레임워크 보안 특화
|   +-- TOGAF, ISO 27001과 결합
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[SABSA 발표 (1995)]
자크만 프레임워크 보안 특화
비즈니스 중심 보안 설계 혁신
      |
      v
[SABSA Institute 설립 (2008)]
SABSA 자격증 프로그램
글로벌 보안 아키텍트 커뮤니티
      |
      v
[클라우드 보안 SABSA 적용 (2010s~)]
AWS/Azure/GCP 환경 SABSA 확장
CASB, CSPM 통합
      |
      v
[Zero Trust + SABSA (2019~)]
Zero Trust 아키텍처 설계에 SABSA 적용
NIST SP 800-207 참조 아키텍처
      |
      v
[현재: AI 보안 아키텍처 SABSA]
AI/ML 시스템 보안 요구사항 도출
LLM 보안 위협 비즈니스 영향 분석
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. SABSA는 회사 보안을 경영자(비즈니스)부터 기술자(시스템)까지 층층이 연결된 설계 도면으로 만드는 방법이에요!
2. "왜 이 보안이 필요한가?"를 항상 비즈니스 이유로 설명할 수 있도록 — 방화벽 하나도 "어떤 비즈니스 리스크를 막는가"를 추적할 수 있어요.
3. 자크만 프레임워크를 보안에 특화한 것 — "6층 아키텍처 × 6가지 질문"의 36칸 체크리스트로 보안 구멍을 찾아요!
