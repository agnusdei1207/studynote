+++
title = "41. 코드 리뷰 (Code Review)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Code-Review", "Pull-Request", "Best-Practices", "Feedback", "Quality"]
draft = false
+++

# 코드 리뷰 (Code Review)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 코드 리뷰는 **"개발자 **간 **코드 **검토**를 **통해 **품질**을 **향상**시키고 **지식 **공유**를 **촉진**하는 **협업 **프로세스\"**로, **Pull Request**(GitHub), **Merge Request**(GitLab)**를 **통해 **진행**하고 **CI**(Continuous Integration)**로 **자동화**한다.
> 2. **관점**: **Correctness**(정확성), **Readability**(가독성), **Maintainability**(유지보수성), **Performance**(성능), **Security**(보안)**을 **검토**하며 **Design**(설계), **Test**(테스트 **커버리지), **Documentation**(문서)**를 **확인**한다.
> 3. **프로세스**: **Self-Review**(자가 **검토)** → **Submit**(PR **생성)** → **Automated Check**(CI/Lint)** → **Peer Review**(동료 **검토)** → **Address Feedback**(수정)** → **Approve**(승인)** → **Merge**(병합)**으로 **이루어진다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
코드 리뷰는 **"협업적 코드 검토"**이다.

**리뷰 유형**:
| 유형 | 방식 | 장점 | 단점 |
|------|------|------|------|
| **Pair Programming** | 실시간 | 즉시 피드백 | 비쌈 |
| **Pull Request** | 비동기 | 유연함 | 지연 |
| **Over-the-shoulder** | 1:1 | 간단 | 확장X |
| **Tool-assisted** | 자동화 | 빠름 | 한계 |

### 💡 비유
코드 리뷰는 ****게시판 **검토 ****와 같다.
- **저자**: 작성자
- **리뷰어**: 편집자
- **변경**: 수정사항

---

## Ⅱ. 아키텍처 및 핵심 원리

### Pull Request Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Pull Request Process                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Developer                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Create branch: git checkout -b feature/new-login                                │  │  │
    │  │  2. Make changes + commit                                                           │  │  │
    │  │  3. Push: git push origin feature/new-login                                        │  │  │
    │  │  4. Create PR on GitHub/GitLab                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Automated Checks                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  CI Pipeline                                                                          │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  • Lint: ESLint, Pylint, Golangci-lint                                           │  │  │  │
    │  │  │  • Format: Prettier, Black, gofmt                                                  │  │  │  │
    │  │  │  • Test: pytest, jest, go test                                                     │  │  │  │
    │  │  │  • Build: Compile, package                                                         │  │  │  │
    │  │  │  • Security: SAST, dependency scan                                                 │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │           Status: ✅ Passing or ❌ Failed                                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Manual Review                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Reviewer(s)                                                                          │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  • Review code diff                                                                │  │  │  │
    │  │  │  • Leave comments (inline or general)                                             │  │  │
    │  │  │  • Request changes or Approve                                                     │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │           Status: 🔵 Changes Requested or ✅ Approved                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Address Feedback                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Developer addresses comments → Push new commits → CI re-runs                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Merge                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Squash merge / Merge commit / Rebase                                             │  │  │
    │  │  • Delete branch                                                                      │  │  │
    │  │  • Deploy to staging/production                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 리뷰 체크리스트

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Code Review Checklist                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Functionality (기능적 관점):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  □ Does the code implement the requirements?                                          │  │
    │  □ Are edge cases handled? (null, empty, invalid input)                                │  │
    │  □ Are errors properly handled and logged?                                              │  │
    │  □ Are there sufficient tests? (unit, integration)                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Code Quality (코드 품질):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  □ Is the code readable and self-documenting?                                          │  │
    │  □ Are variable/function names descriptive?                                             │  │
    │  □ Is the code DRY (Don't Repeat Yourself)?                                             │  │
    │  □ Are functions small and single-purpose?                                             │  │
    │  □ Are there comments explaining complex logic?                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Performance (성능):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  □ Are there obvious performance issues? (O(n²) where O(n) possible)                   │  │
    │  □ Are database queries optimized? (indexes, N+1 queries)                               │  │
    │  □ Is caching used appropriately?                                                       │  │
    │  □ Are large files processed in chunks/streams?                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Security (보안):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  □ Is user input validated and sanitized?                                               │  │
    │  □ Are secrets/credentials not hardcoded?                                               │  │
    │  □ Are SQL queries parameterized? (prevent injection)                                   │  │
    │  □ Are sensitive data logged/encrypted?                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 리뷰어 유형

| 유형 | 장점 | 단점 | 적합 |
|------|------|------|------|
| **Domain Expert** | 정확성 | 편향 가능 | 복잡 로직 |
| **Fresh Eyes** | 새 관점 | 학습 곡선 | 일반 코드 |
| **Auto-Review** | 일관성 | 한계 | 스타일 |

### 피드백 패턴

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Constructive Feedback Pattern                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Bad Feedback:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  "This code is bad. Rewrite it."                                                       │  │
    │  → Not helpful, vague, discouraging                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Good Feedback:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Observation   │  Why it's a problem   │  Suggested fix                              │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  The loop has  │  O(n²) complexity    │  Use a hash map to reduce                   │  │
    │  │  nested loops │  which is slow for     │  to O(n):                                   │  │
    │  │                │  large inputs          │  result = {}                                │  │
    │  │                │                        │  for item in items:                         │  │
    │  │                │                        │      result[item.id] = item                 │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Comment Types:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  🔵 Question: "Why did you choose this approach?"                                       │  │
    │  💡 Suggestion: "Consider using X instead of Y"                                         │  │
    │  ⚠️  Issue: "This will cause problem when..."                                          │  │
    │  ✅ Approval: "Looks good to me"                                                         │  │
    │  🎉 Praise: "Great use of pattern here!"                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 보안 취약점 리뷰
**상황**: SQL Injection 가능성
**판단**: Parameterized Query 요청

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Security-Focused Code Review                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Code Under Review:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  def get_user(username):                                                                  │  │
    │      query = f"SELECT * FROM users WHERE username = '{username}'"                         │  │
    │      return db.execute(query)                                                             │  │
    │                                                                                         │  │
    │  → Vulnerable to SQL injection: username = "admin' OR '1'='1"                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Review Comments:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Reviewer: ⚠️  Security: SQL Injection Vulnerability                                     │  │
    │                                                                                         │  │
    │  This code is vulnerable to SQL injection. An attacker could provide:                    │  │
    │  username = "admin' OR '1'='1" --"                                                        │  │
    │                                                                                         │  │
    │  Resulting query:                                                                        │  │
    │  SELECT * FROM users WHERE username = 'admin' OR '1'='1' --'                              │  │
    │  → Returns all users, bypasses authentication                                            │  │
    │                                                                                         │  │
    │  Suggested fix:                                                                          │  │
    │  ```python                                                                                │  │
    │  def get_user(username):                                                                │  │
    │      query = "SELECT * FROM users WHERE username = %s"                                   │  │
    │      return db.execute(query, (username,))  # Parameterized                              │  │
    │  ```                                                                                     │  │
    │                                                                                         │  │
    │  Or use an ORM:                                                                          │  │
    │  ```python                                                                                │  │
    │  def get_user(username):                                                                │  │
    │      return User.objects.get(username=username)                                          │  │
    │  ```                                                                                     │  │
    │                                                                                         │  │
    │  Please address before merging.                                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 코드 리뷰 기대 효과

| 효과 | 설명 | 수치 |
|------|------|------|
| **버그 감소** | 조기 발견 | 60-80% |
| **지식 공유** | 팀 성장 | +30% |
| **품질** | 일관성 | +40% |
| **온보딩** | 학습 | +50% |

### 모범 사례

1. **범위**: 400 LOC 이하
2. **속도**: 24시간 내
3. **톤**: 존중, 건설적
4. **승인**: 최소 1명

### 미래 전망

1. **AI 리뷰**: GitHub Copilot
2. **자동화**: 더 많은 CI
3. **비동기**: Async workflow
4. **매트릭**: Review analytics

### ※ 참고 표준/가이드
- **Google**: Code Review Guide
- **Facebook**: Internal Docs
- **Amazon**: Two-Pizza Team

---

## 📌 관련 개념 맵

- [CI/CD](./10_cicd/36_ci_cd_tools.md) - 자동화
- [테스트](./25_testing/95_testing.md) - 커버리지
- [버전 관리](./3_vcs/31_version_control.md) - Git Flow

