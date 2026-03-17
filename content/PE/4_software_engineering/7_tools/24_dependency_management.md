+++
title = "24. 의존성 관리 (Dependency Management)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Dependency", "Package-Manager", "Semantic-Versioning", "Transitive-Dependency", "Dependency-Hell"]
draft = false
+++

# 의존성 관리 (Dependency Management)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 의존성 관리는 **"프로젝트가 필요로 하는 **외부 라이브러리**를 **자동으로 **다운로드**, **설치**, **업데이트**하고 **충돌**(Conflict)을 **해결**하는 **도구"**로, **Semantic Versioning**(Semver)으로 **호환성**을 **보장**하고 **Dependency Graph**로 **Transitive Dependency**(전이 의존성)를 **관리**한다.
> 2. **가치**: **수동 의존성 관리**의 **복잡함**과 **오류 가능성**을 **제거**하고 **재현 가능한 **빌드**를 **보장**하며 **보안 취약점**(Vulnerability)을 **빠르게 **식별**하고 **License Conflict**를 **감지**한다.
> 3. **융합**: **JavaScript**(npm, yarn, pnpm), **Python**(pip, poetry, pipenv), **Java**(Maven, Gradle), **Go**(go mod)가 **언어별** **패키지 매니저**를 **사용**하며 **Central Repository**(npm, PyPI, Maven Central)와 **Private Registry**(Artifactory, Nexus)로 **구성**된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
의존성 관리는 **"외부 라이브러리를 관리하는 시스템"**이다.

**의존성 관리 기능**:
- **Download**: 라이브러리 다운로드
- **Install**: 프로젝트에 설치
- **Update**: 최신 버전으로 업데이트
- **Resolve**: 버전 충돌 해결

### 💡 비유
의존성 관리는 **"장보 정리"**와 같다.
- **필요한 것**: 라이브러리
- **정리**: 버전 관리
- **공급**: 설치

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         의존성 관리 발전                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Manual (1990년대):
    • 직접 다운로드
    • CLASSPATH 설정
         ↓
Package Manager (2000년대):
    • npm, pip
    • 자동 의존성 해결
         ↓
Modern (2010년대~):
    • Lockfile (package-lock.json, yarn.lock)
    • Semantic Versioning
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### Semantic Versioning (Semver)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Semantic Versioning (Semver)                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  형식: MAJOR.MINOR.PATCH                                                                │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  MAJOR (주 버전):             MINOR (부 버전):              PATCH (수선 버전)        │  │
    │  │  • 호환 불가 API 변경        • 기능 추가                   • 버그 수정                 │  │
    │  │  │                           │  • 하위 호환 가능               │                           │  │
    │  │  │  0.x.x → 1.0.0 (Breaking)    │ 1.2.0 → 1.3.0 (Backward Compatible)  │ 1.2.3 → 1.2.4 (Bug Fix)     │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Transitive Dependency

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         전이 의존성 (Transitive Dependency)                                │
└─────────────────────────────────────────────────────────────────────────────────────────└──────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  프로젝트 ─→ Library A ─→ Library C (버전 1.0)                                           │
    │              └─→ Library B ──┼→ Library C (버전 2.0) ← 충돌!                                    │
    │                              │                                                    │
    │                              └→ Library D ─→ Library C (버전 2.0)                             │
    │                                                                                         │
    │  → Dependency Resolver가 Graph 분석으로 해결                                             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Lockfile

```
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [package-lock.json (Node.js/npm)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  {                                                                                    │  │
    │    "name": "myapp",                                                                 │  │
    │    "version": "1.0.0",                                                            │  │
    │    "lockfileVersion": 2,                                                               │  │
    │    "requires": true,                                                                 │  │
    │    "dependencies": {                                                                  │  │
    │      "express": {                                                                     │  │
    │        "version": "4.18.2",                                                           │  │
    │        "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",          │  │
    │        "integrity": "sha512-..."                                                          │  │
    │      },                                                                                 │  │
    │      "lodash": {                                                                      │  │
    │        "version": "4.17.21",                                                          │  │
    │        "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",         │  │
    │        "integrity": "sha512-..."                                                          │  │
    │      }                                                                                 │  │
    │    }                                                                                  │  │
    │  }                                                                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [yarn.lock (Yarn)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Deterministic installs                                                                  │  │
    │  • Flat dependency structure                                                            │  │
    │  → 재현 가능한 빌드                                                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 패키지 매니저 비교

| 도구 | 언어 | Lockfile | 특징 |
|------|------|----------|------|
| **npm** | JavaScript | package-lock.json | 거대적 표준 |
| **yarn** | JavaScript | yarn.lock | 빠름, determinist |
| **pnpm** | JavaScript | pnpm-lock.yaml | 디스크 공유, 빠름 |
| **pip** | Python | requirements.txt | Lock 없음 (poetry로 해결) |
| **poetry** | Python | poetry.lock | 의존성 + 패키징 관리 |
| **Maven** | Java | (pom.xml) | declarative |
| **Gradle** | JVM | Gradle lock files | Groovy/Kotlin DSL |
| **go mod** | Go | go.sum | go.mod |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: npm 의존성 관리
**상황**: Node.js 프로젝트
**판단**:

```bash
# package.json
{
  "name": "myapp",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^7.0.0",
    "dotenv": "^16.0.0"
  }
}

# 설치
npm install
# package-lock.json 생성

# 업데이트
npm update
# 안전한 업데이트 (caret range 내)

# 감사 (보안 취약점)
npm audit
npm audit fix
```

---

## Ⅴ. 기대효과 및 결론

### 의존성 관리 기대 효과

| 효과 | 관리 없음 | 관리 있음 |
|------|---------|----------|
| **버전 충돌** | 빈번 | 자동 해결 |
| **보안** | 취약점 있음 | 식별 가능 |
| **재현성** | 어려움 | 보장 |
| **설치 속도** | 느림 | 빠름 |

### 모범 사례

1. **Lockfile Commit**: 버전 관리
2. **Private Registry**: 내부 라이브러리
3. **Semantic Versioning**: 호환성 유지
4. **Regular Audit**: 보안 점검
5. **Minimal Dependencies**: 불필요 의존성 제거

### 미래 전망

1. **Zero-Install**: 빠른 설치
2. **Monorepo**: 다중 패키지
3. **Dependabot**: 자동 보안 PR

### ※ 참고 표준/가이드
- **npm**: docs.npmjs.com
- **yarn**: yarnpkg.com
- **poetry**: python-poetry.org

---

## 📌 관련 개념 맵

- [빌드 도구](./23_build_tools.md) - 빌드 실행
- [CI/CD](./21_pipeline.md) - 자동화
- [보안](./25_security.md) - 취약점 관리
- [모듈 시스템](../3_architecture/23_module_system.md) - 아키텍처
