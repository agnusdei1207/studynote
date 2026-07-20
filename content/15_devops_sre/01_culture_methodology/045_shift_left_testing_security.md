---
title: "Shift Left Testing Security"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
weight: 45
---
> **핵심 인사이트**
> 1. 시프트 레프트(Shift Left)는 테스팅·보안 활동을 개발 생명주기의 왼쪽(초기 단계)으로 이동시키는 원칙 — 결함은 발견이 늦을수록 수정 비용이 기하급수적으로 증가하며(IBM: 운영 단계 결함 수정 비용 = 설계 단계의 100×), 초기 발견이 핵심이다.
> 2. 시프트 레프트 테스팅은 테스트 피라미드와 TDD(테스트 주도 개발)로 구현 — 단위 테스트(70%)·통합 테스트(20%)·E2E 테스트(10%) 비율로 빠른 피드백 루프를 만들어 CI/CD 파이프라인에서 자동 검증한다.
> 3. DevSecOps(시프트 레프트 보안)는 보안을 개발 프로세스에 내재화 — SAST(정적 분석)->DAST(동적 분석)->SCA(오픈소스 취약점)->컨테이너 스캔을 CI/CD 파이프라인에 자동화하며, "보안은 보안팀의 일"이 아닌 "모두의 일"로 만든다.

---

## Ⅰ. 시프트 레프트 개념

```
결함 수정 비용 곡선:

비용
^
100× |                              ×
     |                        ×
10×  |                  ×
     |           ×
1×   |     ×
-----+----------------------------->
    요구   설계   구현   테스트  운영
    분석

IBM 연구 (1970s, 여전히 통용):
  요구사항 단계: 1×
  설계 단계: 5×
  구현 단계: 10×
  테스트 단계: 20×
  운영 단계: 100×

시프트 레프트 전략:
  전통 워터폴:
  요구 -> 설계 -> 구현 -> [테스트] -> 운영
                              ^
                          테스트만 마지막에

  시프트 레프트:
  [테스트·보안]->[테스트·보안]->[테스트·보안] -> 운영
  요구          설계          구현

  각 단계에서 테스트·보안 활동 수행

세 가지 시프트 레프트:
  1. 테스팅 (Shift Left Testing)
  2. 보안 (DevSecOps / Shift Left Security)
  3. 성능 (Shift Left Performance)
```

> 📢 **섹션 요약 비유**: 시프트 레프트는 요리할 때 식재료 확인 — 완성 후 맛 없으면(운영 결함) 다 버려야. 재료 살 때(요구사항) 신선한지 확인하면 훨씬 저렴!

---

## Ⅱ. 시프트 레프트 테스팅

```
테스트 피라미드 (Test Pyramid):

        /       /  \  E2E 테스트 (10%)
      /----\  Selenium, Cypress
     /          /----------\ 통합 테스트 (20%)
   /            \  API 테스트, DB 테스트
  /---------------- \ 단위 테스트 (70%)
 /                    \  JUnit, pytest, Jest

단위 테스트 (Unit Test):
  개별 함수/메서드 독립 검증
  Mock/Stub으로 의존성 격리
  실행: 밀리초 단위 (빠름)
  피드백: 즉시

통합 테스트 (Integration Test):
  컴포넌트 간 상호작용 검증
  실제 DB, 외부 서비스 연동
  실행: 초~분 단위

E2E 테스트 (End-to-End):
  사용자 시나리오 전체 검증
  브라우저 자동화 (Selenium, Cypress)
  실행: 분~시간 단위 (느림)
  취약: 외부 의존성, 유지보수 비용

TDD (Test-Driven Development):
  Red-Green-Refactor 사이클:

  Red: 실패하는 테스트 먼저 작성
  v
  Green: 테스트 통과하는 최소 코드 작성
  v
  Refactor: 코드 정리 (테스트는 통과 유지)
  v (다시 Red)

CI 파이프라인 통합:
  커밋 -> 단위 테스트 자동 실행 (<5분)
  PR -> 통합 테스트 (<30분)
  main 브랜치 -> E2E 테스트 (<60분)
  실패 시 즉시 알림
```

> 📢 **섹션 요약 비유**: 테스트 피라미드는 건물 기초 — 단위 테스트(넓은 기초), 통합 테스트(벽), E2E(지붕). 기초가 탄탄해야 지붕이 올라가요. TDD는 청사진 먼저!

---

## Ⅲ. 시프트 레프트 보안 (DevSecOps)

```
DevSecOps 파이프라인:

코드 작성 -> SAST -> 빌드 -> SCA -> 테스트 -> DAST -> 배포

1. SAST (Static Application Security Testing):
   코드를 실행 없이 정적 분석

   탐지: 인젝션, 버퍼 오버플로우, 하드코딩 비밀

   도구:
   SonarQube: 멀티 언어, 코드 품질+보안
   Semgrep: 커스텀 규칙, 빠름
   Checkmarx, Veracode: 엔터프라이즈

   실행 위치: 커밋 또는 PR 단계

2. SCA (Software Composition Analysis):
   오픈소스 의존성 취약점 스캔

   탐지: CVE(Common Vulnerabilities and Exposures)

   도구:
   Snyk: 개발자 친화적
   OWASP Dependency-Check
   Dependabot (GitHub 내장)

   예: Log4j 취약점 (2021) -> SCA로 즉시 탐지

3. DAST (Dynamic Application Security Testing):
   실행 중인 앱을 외부에서 공격 시뮬레이션

   탐지: XSS, SQL 인젝션, CSRF

   도구:
   OWASP ZAP: 오픈소스 표준
   Burp Suite: 전문가용

   실행 위치: 테스트/스테이징 환경 배포 후

4. 컨테이너 보안:
   Trivy: 컨테이너 이미지 취약점 스캔
   Grype

   CI 통합:
   docker build -> trivy image scan
   High/Critical CVE -> 배포 차단

5. IaC 보안:
   Terraform, CloudFormation 코드 스캔
   Checkov, TFSec: 잘못된 보안 설정 탐지
   S3 버킷 public -> 차단
```

> 📢 **섹션 요약 비유**: DevSecOps는 공장 품질 검사 라인 — SAST(코드 검사기), SCA(부품 결함 검사), DAST(완성품 충격 테스트), 컨테이너(포장 검사). 각 단계마다 검사!

---

## Ⅳ. CI/CD 파이프라인 구성

```
시프트 레프트 CI/CD 파이프라인:

Stage 1 (Pre-commit, <1분):
  pre-commit hook:
  - 코드 포맷터 (Black, Prettier)
  - 린터 (ESLint, Pylint)
  - 비밀 스캔 (GitLeaks)

  실패 시: 커밋 차단

Stage 2 (CI - 단위 테스트, <10분):
  트리거: 모든 커밋
  - 단위 테스트 실행
  - SAST (SonarQube, Semgrep)
  - SCA (Snyk)

  실패 시: 브랜치 머지 차단

Stage 3 (CI - 통합 테스트, <30분):
  트리거: PR -> main
  - 통합 테스트
  - API 테스트
  - 컨테이너 이미지 빌드 + Trivy 스캔
  - IaC 보안 스캔 (Checkov)

Stage 4 (CD - 스테이징, <60분):
  트리거: main 머지
  - 스테이징 배포
  - E2E 테스트
  - DAST (OWASP ZAP)
  - 성능 테스트 (K6)

Stage 5 (CD - 프로덕션):
  트리거: 수동 승인 또는 자동
  - 블루/그린 또는 카나리 배포
  - 헬스 체크

실패 정책:
  Critical SAST/SCA: 즉시 차단 (blocker)
  High: 경고 + 7일 내 수정 의무
  Medium 이하: 리포트만
```

> 📢 **섹션 요약 비유**: 시프트 레프트 CI/CD는 공항 보안 검색 — 수하물(코드)이 여러 검색대(Stage)를 통과. 초기 검색대(Pre-commit)에서 걸리면 가장 빠르고 저렴하게 해결!

---

## Ⅴ. 실무 시나리오 — 핀테크 DevSecOps

```
핀테크 스타트업 DevSecOps 도입:

배경:
  빠른 기능 출시 + 금융 보안 규제
  PCI DSS (결제 카드 산업 보안 표준) 준수 필요
  현황: 수동 보안 검토 -> 출시 지연 2주

문제:
  보안팀: "배포 전 보안 검토 필요"
  개발팀: "일정 촉박한데 왜 항상 보안이..."
  -> 갈등, 지연

DevSecOps 도입:

1. 파이프라인 보안 자동화:
  GitHub Actions:

  - pr_check.yml:
    Semgrep SAST, Snyk SCA, Trivy
    Critical -> PR 머지 차단

  - staging_deploy.yml:
    OWASP ZAP DAST (API 엔드포인트)
    고위험 발견 -> 알림 + 수동 검토

2. 개발자 보안 교육:
  시큐어 코딩 가이드라인 내부 위키
  "왜 이 취약점이 위험한지" 컨텍스트 제공

3. 보안 챔피언 제도:
  각 스쿼드(팀)에 보안 담당자 1명 지정
  -> 보안 주도 (보안팀 병목 제거)

결과 (6개월):
  Critical 취약점: 배포 전 평균 99% 탐지
  출시 지연 (보안 이슈): 2주 -> 0.5일
  PCI DSS 감사: 자동화 증거로 준비 시간 70% 절감
  개발팀 보안 이슈 인지율: 30% -> 85%

ROI:
  보안 침해 방지 비용 (추정): 수십억
  DevSecOps 구축 비용: 5천만원
  보안팀 코드 리뷰 시간: 주 40시간 -> 5시간
```

> 📢 **섹션 요약 비유**: DevSecOps는 공장 품질 내재화 — 별도 품질팀(보안팀)이 마지막에 검사하는 대신, 각 작업자(개발자)가 만들면서 바로 검사. 불량(취약점) 초기에 잡기!

---

## 📌 관련 개념 맵

```
시프트 레프트
+-- 테스팅
|   +-- 테스트 피라미드
|   +-- TDD (Red-Green-Refactor)
|   +-- CI 자동화
+-- 보안 (DevSecOps)
|   +-- SAST (정적 분석)
|   +-- SCA (의존성)
|   +-- DAST (동적 분석)
|   +-- 컨테이너 보안 (Trivy)
|   +-- IaC 보안 (Checkov)
+-- 파이프라인
|   +-- Pre-commit Hook
|   +-- CI/CD Stage별 자동화
+-- 문화
    +-- 보안 챔피언
    +-- DevSecOps 협업
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 워터폴 (1970~2000s)]
마지막 단계 테스트·보안
높은 수정 비용
      |
      v
[애자일 + TDD (2000s)]
반복 개발 + 단위 테스트
시프트 레프트 테스팅 시작
      |
      v
[DevOps + CI/CD (2010s)]
자동화된 테스트 파이프라인
빠른 피드백 루프
      |
      v
[DevSecOps (2015~)]
보안 파이프라인 통합
SAST/DAST/SCA 자동화
      |
      v
[현재: Platform Engineering]
내부 개발자 플랫폼
보안·테스트 셀프서비스
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 시프트 레프트는 조기 검사 — 완성된 제품(운영)에서 결함 발견이면 다 뜯어야. 재료 확인(요구사항)에서 미리 잡으면 훨씬 쉬워요!
2. 테스트 피라미드는 집 기초 — 단위 테스트(기초) 많이, 통합(벽) 적당히, E2E(지붕) 조금. 기초가 튼튼해야 집이 안전!
3. DevSecOps는 모두가 보안팀 — 보안 전문가만 보안 책임지는 게 아니라, 개발자도 코딩할 때 자동으로 보안 체크. 팀 전체가 보안 수호자!
