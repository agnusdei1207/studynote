---
title: "Pre Commit Hook Linting"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 119
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Pre-commit Hook은 `git commit` 실행 직전에 <strong>자동으로 린터·포매터·보안 스캔을 실행</strong>하여, 품질 기준을 충족하지 못한 코드의 커밋을 차단하는 <strong>Shift Left 품질 관리 메커니즘</strong>이다.
> 2. **가치**: CI에서 린트를 실행하면 커밋->푸시->CI 실패->수정->재커밋의 <strong>피드백 루프가 10분 이상</strong>이지만, Pre-commit Hook은 커밋 시점에 <strong>즉시(수 초) 피드백</strong>하여 불량 코드가 리포지토리에 들어가는 것을 원천 차단한다.
> 3. **판단 포인트**: `pre-commit` 프레임워크(Python)가 사실상 표준이며, ESLint·Prettier·Black·Ruff·gitleaks(시크릿 탐지)·commitlint(커밋 메시지 규약)를 조합하여 팀 전체에 일관된 품질 기준을 적용한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Pre-commit Hook 워크플로                            |
+-------------------------------------------------------+
|  1. git commit -m "feat: add login"                   |
|  2. Pre-commit Hook 자동 실행:                        |
|     ✅ trailing-whitespace (공백 제거)                |
|     ✅ end-of-file-fixer (파일 끝 개행)               |
|     ✅ ruff (Python 린트)                             |
|     ❌ gitleaks (API Key 탐지!) -> 커밋 차단!         |
|  3. 개발자: 시크릿 제거 -> 재커밋                     |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Pre-commit Hook은 공항 보안 검색대이다. 위험물(시크릿·린트 에러)이 발견되면 비행기(커밋)에 탑승할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### pre-commit 프레임워크 설정

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
  - repo: https://github.com/gitleaks/gitleaks
    hooks:
      - id: gitleaks
```

### 주요 Hook 카테고리

| 카테고리 | 도구 | 역할 |
|:---|:---|:---|
| **포매팅** | Prettier, Black | 코드 스타일 자동 정리 |
| **린팅** | ESLint, Ruff | 코드 품질·에러 탐지 |
| **보안** | gitleaks, detect-secrets | 시크릿 유출 방지 |
| **커밋 규약** | commitlint | 커밋 메시지 형식 검증 |

- **📢 섹션 요약 비유**: Pre-commit은 편집자(포매터) + 교정자(린터) + 보안 검사관(gitleaks)이 원고(코드)를 출판(커밋) 전에 검수하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | CI 린트만 | Pre-commit + CI |
|:---|:---|:---|
| **피드백 시간** | 10분+ | **수 초** |
| **불량 코드 커밋** | 가능 | **차단** |
| <strong>개발자 경험</strong> | 느린 루프 | **즉시 수정** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 팀 도입 전략
1. `.pre-commit-config.yaml` 리포지토리에 커밋.
2. `pre-commit install` -> 모든 팀원 자동 적용.
3. CI에서도 `pre-commit run --all-files`로 이중 검증.

---

## Ⅴ. 기대효과 및 결론

| 지표 | CI 린트만 | Pre-commit | 개선 |
|:---|:---|:---|:---|
| 피드백 루프 | 10분 | **3초** | 200× |
| 시크릿 유출 | CI에서 발견 | **커밋 전 차단** | 원천 방지 |
| CI 실패율 | 높음 | **낮음** | 효율 ^ |

Pre-commit Hook은 <strong>Shift Left의 가장 극단적 구현</strong>이며, 비용 대비 효과가 가장 높은 DevOps 실천이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **pre-commit 프레임워크** | Hook 관리 도구 (사실상 표준) |
| **gitleaks** | 시크릿(API Key) 탐지 Hook |
| **commitlint** | 커밋 메시지 형식 검증 |
| **Shift Left** | 품질 검증을 가장 앞 단계로 이동 |
| <strong>CI 린트</strong> | Pre-commit의 보완 (이중 검증) |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 코드 리뷰 (린트 없음)]
    |
    v
[CI 린트 (Jenkins/GitHub Actions, 2015~)]
    |
    v
[pre-commit 프레임워크 (2018~) — 커밋 전 자동 검증]
    |
    v
[gitleaks + commitlint 통합 (2020~)]
    |
    v
[현재: AI Lint — GenAI가 코드 품질 자동 개선 제안]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Pre-commit Hook은 <strong>공항 보안 검색대</strong>예요. 짐(코드)에 위험물(에러)이 있으면 비행기(커밋)에 못 타요.
2. 보안 검색은 **몇 초만에 끝나서** 공항(CI)까지 가지 않아도 바로 알 수 있어요.
3. 덕분에 나쁜 코드가 <strong>리포지토리에 들어가는 것을 원천 차단</strong>할 수 있답니다!
