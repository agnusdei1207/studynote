+++
title = "43. 품질 보증 (QA) vs 품질 제어 (QC)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["QA", "QC", "Quality-Assurance", "Quality-Control", "Testing"]
draft = false
+++

# 품질 보증 (QA) vs 품질 제어 (QC)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **QA**(Quality Assurance)는 **"프로세스** 중심**의 **예방 **활동**이고 **QC**(Quality Control)는 **"제품** 중심**의 **검증 **활동**이며 **QA**는 **품질 **시스템**을 **수립**하고 **QC**는 **품질 **기준**을 **만족**하는지 **확인**한다.
> 2. **QA**: **프로세스** **개선**, **표준** **준수**, **코드** **리뷰**, **설계** **검토**를 **포함**하고 **QC**: **테스트**, **검사**, **측정**, **결함** **추적**을 **포함**한다.
> 3. **목표**: **QA**는 **"**올바른 **것**을 **만드는 **방법\\\"**을 **보장**하고 **QC**는 **"**만들어진 **것**이 **올바른지**\\\"**를 **확인**하며 **둘 다 **필수**적이고 **상호 **보완**적이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
**QA와 QC의 차이**

| 구분 | QA (품질 보증) | QC (품질 제어) |
|------|----------------|----------------|
| **초점** | 프로세스 | 제품 |
| **목표** | 결함 예방 | 결함 발견 |
| **시점** | 개발 전반 | 개발 후반 |
| **방식** | 프로세스 수립 | 테스트/검사 |
| **책임** | 전체 팀 | QA 팀 |
| **질문** | "방법이 맞나?" | "결과가 맞나?" |

### 💡 비유
QA는 **요리사 레시피**, QC는 **접시에 담기 전 맛보기**.
- **QA**: 요리 방법, 위생, 재료 선정
- **QC**: 완성 요리 맛, 온도, 외관

---

## Ⅱ. 아키텍처 및 핵심 원리

### QA 활동

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         QA (Quality Assurance) Activities                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Process Definition (프로세스 정의):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • SDLC (Software Development Life Cycle) 정의                                         │  │
    │  • Coding Standards (코딩 표준)                                                         │  │
    │  • Review Guidelines (리뷰 가이드라인)                                                  │  │
    │  • Documentation Standards (문서화 표준)                                               │  │
    │  • CI/CD Pipeline (지속 통합/배포)                                                      │  │
    │                                                                                         │  │
    │  Example:                                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  - All code must be reviewed before merge                                           │  │  │
    │  │  - Unit tests required for all functions                                           │  │  │
    │  │  - Static analysis must pass (SonarQube)                                            │  │  │
    │  │  - Documentation must be updated with code changes                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Standards Compliance (표준 준수):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • ISO 9001 (Quality Management System)                                                 │  │
    │  • ISO/IEC 27001 (Information Security)                                                 │  │
    │  • CMMI (Capability Maturity Model Integration)                                         │  │
    │  • IEEE Standards (730, 829, 1008, etc.)                                                 │  │
    │  • Industry-specific (HIPAA, PCI-DSS, SOC2)                                             │  │
    │                                                                                         │  │
    │  Compliance Verification:                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  - Regular audits (internal/external)                                               │  │  │
    │  │  - Gap analysis                                                                     │  │  │
    │  │  - Corrective actions                                                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Training & Awareness (교육 및 인식):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Onboarding training (신규 입사자 교육)                                               │  │
    │  • Security awareness (보안 인식)                                                       │  │
    │  • Tool training (JUnit, Selenium, etc.)                                                 │  │
    │  • Process workshops (프로세스 워크샵)                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    4. Code Reviews (코드 리뷰):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Purpose:                                                                                │  │
    │  • Find bugs early (초기 버그 발견)                                                      │  │
    │  • Knowledge sharing (지식 공유)                                                        │  │
    │  • Ensure consistency (일관성 보장)                                                      │  │
    │                                                                                         │  │
    │  Review Types:                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Type             │  Format     │  Participants  │  Focus                            │  │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  Self-Review      │  Async      │  Author        │  Basic correctness               │  │  │
    │  │  Peer Review      │  Async/Sync │  1-2 peers     │  Logic, style                    │  │  │
    │  │  Team Review      │  Sync       │  Entire team   │  Architecture, design            │  │  │
    │  │  Expert Review    │  Async      │  Domain expert │  Security, performance           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Review Checklist:                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  □ Functionality correct?                                                           │  │  │
    │  │  □ Error handling complete?                                                         │  │  │
    │  │  □ Tests added/updated?                                                             │  │  │
    │  │  □ Documentation updated?                                                           │  │  │
    │  │  □ No security vulnerabilities?                                                     │  │  │
    │  │  □ Performance acceptable?                                                          │  │  │
    │  │  □ Code follows style guide?                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### QC 활동

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         QC (Quality Control) Activities                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Testing Levels (테스트 레벨):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Unit Testing (단위 테스트):                                                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Scope: Single function/method                                                    │  │  │
    │  │  • Who: Developer                                                                    │  │  │
    │  │  • Tools: JUnit, NUnit, pytest, Jest                                                 │  │  │
    │  │  • Coverage: Target >80%                                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Integration Testing (통합 테스트):                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Scope: Module/Service interaction                                                │  │  │
    │  │  • Who: Developer + Tester                                                           │  │  │
    │  │  • Focus: APIs, databases, external services                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  System Testing (시스템 테스트):                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Scope: Entire system                                                              │  │  │
    │  │  • Who: QA Team                                                                       │  │  │
    │  │  • Types: Functional, Performance, Security, Usability                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Acceptance Testing (인수 테스트):                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Scope: Business requirements                                                       │  │  │
    │  │  • Who: Users/Stakeholders                                                            │  │  │
    │  │  • Goal: Confirm "Fit for purpose"                                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Testing Techniques (테스트 기법):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Black-Box Testing:                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • No knowledge of internal structure                                                 │  │  │
    │  │  • Techniques: Equivalence partitioning, Boundary value analysis, State transition   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  White-Box Testing:                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Internal code structure visible                                                    │  │  │
    │  │  • Techniques: Statement coverage, Branch coverage, Path coverage                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Gray-Box Testing:                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Partial knowledge of internals                                                    │  │  │
    │  │  • Combines black-box and white-box                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Defect Tracking (결함 추적):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Lifecycle: New → Assigned → In Progress → Fixed → Verified → Closed                      │  │
    │                                                                                         │  │
    │  Severity Levels:                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  S1: Critical (System crash, data loss)                                              │  │  │
    │  │  S2: High (Major feature broken, workaround exists)                                  │  │  │
    │  │  S3: Medium (Minor feature broken, easy workaround)                                  │  │  │
    │  │  S4: Low (Cosmetic issue, no impact)                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Metrics:                                                                                │  │
    │  • Defect Density (defects per KLOC)                                                    │  │
    │  • Defect Removal Efficiency (DRE)                                                       │  │
    │  • Escape Rate (production defects)                                                      │  │
    │  • Mean Time to Resolve (MTTR)                                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### QA vs QC 상세 비교

| 관점 | QA (품질 보증) | QC (품질 제어) |
|------|----------------|----------------|
| **정의** | 프로세스 품질 보장 | 제품 품질 검증 |
| **목표** | 결함 예방 | 결함 발견 |
| **시점** | 개발 시작부터 | 개발 완료 후 |
| **활동** | 프로세스, 표준, 교육 | 테스트, 검사, 측정 |
| **산출물** | 프로세스 문서 | 테스트 보고서 |
| **책임자** | 전체 팀, 관리자 | QA 팀, 테스터 |
| **중점** | "How" (방법) | "What" (결과) |

### QA/QC 통합 모델

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Integrated QA/QC Model                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Development Lifecycle with QA/QC:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Phase           │  QA Activities              │  QC Activities                      │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  Requirements   │  Review completeness      │  -                                  │  │
    │                  │  Define acceptance criteria│                                     │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  Design         │  Review architecture       │  Prototype testing                │  │
    │                  │  Check standards compliance│                                     │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  Coding         │  Code reviews               │  Unit testing                     │  │
    │                  │  Static analysis            │  Code coverage                   │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  Integration    │  Process monitoring         │  Integration testing              │  │
    │                  │                            │  API testing                      │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  System Test    │  Test process validation    │  System testing                   │  │
    │                  │                            │  Performance testing              │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  Deployment     │  Release standards          │  Acceptance testing               │  │
    │                  │  Rollback procedures        │  Smoke testing                    │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  Maintenance    │  Post-release review        │  Regression testing               │  │
    │                  │  Process improvement        │  Monitoring                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: QA/QC 조직 구성
**상황**: 스타트업 개발팀 품질 조직 설계
**판단**: centralized vs decentralized

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         QA/QC Organization Models                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Centralized Model (중앙 집중형):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Structure:                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  QA Director                                                                         │  │  │
    │  │     ├─ Test Automation Team                                                         │  │  │
    │  │     ├─ Manual Testing Team                                                          │  │  │
    │  │     ├─ Performance Team                                                              │  │  │
    │  │     └─ Security Team                                                                 │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Advantages:                                                                            │  │
    │  • Consistent standards/tools                                                           │  │
    │  • Resource sharing (specialists)                                                       │  │
    │  • Career path for QA engineers                                                         │  │
    │                                                                                         │  │
    │  Disadvantages:                                                                          │  │
    │  • Bottleneck (all teams compete for QA)                                                 │  │
    │  • Less context about specific product                                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Decentralized (Embedded) Model:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Structure:                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Product A Team  ┌── Dev Lead                                                       │  │  │
    │  │                 ├── Developers                                                     │  │  │
    │  │                 └── Embedded QA                                                     │  │  │
    │  │                                                                                  │  │  │
    │  │  Product B Team  ┌── Dev Lead                                                       │  │  │
    │  │                 ├── Developers                                                     │  │  │
    │  │                 └── Embedded QA                                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Advantages:                                                                            │  │
    │  • Faster feedback (same team)                                                          │  │
    │  • Better product knowledge                                                             │  │
    │  • Shared responsibility for quality                                                    │  │
    │                                                                                         │  │
    │  Disadvantages:                                                                          │  │
    │  • Inconsistent standards across teams                                                  │  │
    │  • QA engineer isolation (only one in team)                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Hybrid Model (Center of Excellence):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Central QA CoE defines standards, tools, training                                     │  │
    │  • Embedded QAs in product teams                                                        │  │
    │  • Specialists (perf, security) centralized                                              │  │
    │  → Best of both approaches                                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### CI/CD에서의 QA/QC

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         QA/QC in CI/CD Pipeline                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Automated Quality Gates:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Developer Commit                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  ▼ Static Analysis (SonarQube, ESLint) ──→ FAIL → Block                           │  │  │
    │  │  ▼ Unit Tests (JUnit, pytest) ──────────→ FAIL → Block                            │  │  │
    │  │  ▼ Code Coverage (80% min) ────────────→ FAIL → Block                             │  │  │
    │  │  ▼ Security Scan (SAST) ───────────────→ FAIL → Block                             │  │  │
    │  │  ▼ Build Artifact                                                                      │  │  │
    │  │  ▼ Deploy to Dev Environment                                                          │  │  │
    │  │  ▼ Integration Tests ─────────────────→ FAIL → Alert                               │  │  │
    │  │  ▼ Deploy to QA Environment                                                           │  │  │
    │  │  ▼ Automated UI Tests (Selenium) ────→ FAIL → Alert                               │  │  │
    │  │  ▼ Performance Tests (k6) ────────────→ FAIL → Alert                               │  │  │
    │  │  ▼ Manual QA (exploratory testing)                                                    │  │  │
    │  │  ▼ Deploy to Staging                                                                   │  │  │
    │  │  ▼ Acceptance Testing ─────────────────→ FAIL → Block                              │  │  │
    │  │  ▼ Deploy to Production                                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Quality Metrics Dashboard:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Code Coverage (trend)                                                                  │  │
    │  • Test Pass Rate (%)                                                                     │  │
    │  • Defect Escape Rate (per release)                                                       │  │
    │  • Mean Time to Recovery (MTTR)                                                           │  │
    │  • Deployment Frequency                                                                  │  │
    │  • Lead Time for Changes                                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 품질 관리 기대 효과

| 측정 항목 | QA 영향 | QC 영향 | 목표 |
|----------|---------|---------|------|
| **결함 발견 시점** | 조기 발견 | 후반 발견 | 가능한 조기 |
| **재작업 비용** | 감소 | 증가 | 최소화 |
| **고객 불만** | 감소 | 감소 | 0에 근접 |
| **개발 속도** | 초기 느림 | 전체 빠름 | 균형 |

### 모범 사례

1. **Shift Left**: QA 활동을 개발 초기로 이동
2. **테스트 자동화**: 회귀 테스트 자동화
3. **지속적 개선**: retrospectives, metrics
4. **문화 조성**: "Quality is everyone's job"

### 미래 전망

1. **AI 테스팅**: 자동 테스트 생성
2. **Chaos Engineering**: 회복성 테스트
3. **Observability**: 프로덕션 모니터링
4. **DevSecOps**: 보안 품질 통합

### ※ 참고 표준/가이드
- **ISO 9001**: 품질 경영 시스템
- **ISO/IEC 25010**: 소프트웨어 품질 모델
- **CMMI**: 성숙도 모델
- **ISTQB**: 테스트 인증

---

## 📌 관련 개념 맵

- [테스트 도구](./26_testing_tools.md) - 자동화
- [리팩토링](./42_refactoring.md) - 코드 품질
- [CI/CD](./44_cicd.md) - 파이프라인
- [코드 리뷰](./31_formatter.md) - 개발 프로세스
