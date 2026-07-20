---
title: "Textops Docops Automation"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 117
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TextOps/DocOps는 기술 문서를 <strong>코드처럼 Git으로 관리하고, CI/CD 파이프라인으로 빌드·검증·배포</strong>하는 Docs-as-Code 패러다임이며, 마크다운·AsciiDoc으로 작성한 문서를 자동으로 웹 사이트·PDF·API 문서로 변환한다.
> 2. **가치**: 위키·Confluence는 코드와 문서가 분리되어 문서가 빠르게 구식이 되지만, Docs-as-Code는 <strong>코드 PR에 문서 변경을 함께 포함</strong>하여 코드와 문서의 동기화를 보장한다.
> 3. **판단 포인트**: MkDocs(Material)·Docusaurus(React)·Hugo가 대표 SSG(Static Site Generator)이며, Vale(문법 린트)·markdownlint·OpenAPI Spec 검증을 CI에 통합하여 <strong>문서 품질을 자동 검증</strong>한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Docs-as-Code 파이프라인                             |
+-------------------------------------------------------+
|  1. 개발자: docs/ 디렉터리에 .md 파일 수정            |
|  2. PR 생성 -> CI 실행:                                |
|     - markdownlint (마크다운 문법 검증)                |
|     - Vale (영어 문체·용어 일관성)                     |
|     - linkchecker (깨진 링크 탐지)                     |
|  3. 리뷰어 Approve -> 머지                             |
|  4. CD: MkDocs build -> GitHub Pages 자동 배포         |
|  5. 결과: docs.example.com 자동 업데이트              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Docs-as-Code는 코드와 문서를 같은 공장(Git)에서 만들어, 코드가 바뀌면 설명서(문서)도 함께 바뀌는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SSG 도구 비교

| 도구 | 언어 | 테마 | 적합 |
|:---|:---|:---|:---|
| **MkDocs Material** | Python | **최고 (Material)** | 기술 문서 |
| **Docusaurus** | React | 커스터마이징 우수 | OSS 프로젝트 |
| **Hugo** | Go | 빠른 빌드 | 블로그·사이트 |
| **Sphinx** | Python | reStructuredText | API/SDK 문서 |

### 문서 품질 자동 검증

| 도구 | 역할 |
|:---|:---|
| **markdownlint** | 마크다운 문법 규칙 검증 |
| **Vale** | 영어 문체·용어 일관성 (Google Style) |
| **linkchecker** | 깨진 링크 자동 탐지 |
| **Spectral** | OpenAPI 스펙 린트 |

- **📢 섹션 요약 비유**: markdownlint는 맞춤법 검사기이고, Vale는 문체 교정 선생님이며, linkchecker는 참고문헌 확인 담당이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Wiki/Confluence | Docs-as-Code |
|:---|:---|:---|
| <strong>코드 동기화</strong> | 분리 (구식화) | <strong>동일 PR (동기화)</strong> |
| <strong>버전 관리</strong> | 위키 히스토리 | **Git 이력** |
| **리뷰** | 없음/약함 | <strong>PR 리뷰</strong> |
| <strong>CI 검증</strong> | 없음 | **린트·링크 검사** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 도입 체크리스트
1. 프로젝트 루트에 `docs/` 디렉터리 생성.
2. MkDocs/Docusaurus 초기화.
3. CI에 markdownlint + Vale 통합.
4. CD에 GitHub Pages/Netlify 자동 배포.

---

## Ⅴ. 기대효과 및 결론

| 지표 | Wiki | Docs-as-Code | 개선 |
|:---|:---|:---|:---|
| 코드-문서 동기화 | 수동 | <strong>PR 강제</strong> | 구식화 방지 |
| 문서 품질 | 주관적 | <strong>CI 자동 검증</strong> | 일관성 |
| 배포 | 수동 | **CD 자동** | 즉시 반영 |

Docs-as-Code는 GenAI와 결합하여 <strong>코드 변경 시 문서 자동 업데이트·API 문서 자동 생성</strong>이 가능해지고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Docs-as-Code</strong> | TextOps의 핵심 패러다임 |
| **MkDocs Material** | 가장 인기 있는 기술 문서 SSG |
| **Vale** | 문체·용어 일관성 린트 |
| **markdownlint** | 마크다운 문법 검증 |
| **GitHub Pages** | 정적 문서 사이트 무료 호스팅 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Wiki/Confluence (2000s) — 코드와 문서 분리]
    |
    v
[Docs-as-Code 개념 (2015~) — Git으로 문서 관리]
    |
    v
[MkDocs Material / Docusaurus (2018~) — 아름다운 문서 사이트]
    |
    v
[Vale + CI 통합 (2020~) — 문서 품질 자동 검증]
    |
    v
[현재: GenAI 문서 자동 생성 — 코드 변경 -> 문서 자동 업데이트]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 제품(코드)과 설명서(문서)를 **따로따로** 만들어서, 설명서가 맨날 옛날 것이었어요.
2. Docs-as-Code는 제품과 설명서를 <strong>같은 공장(Git)</strong>에서 만들어, 항상 최신 상태를 유지해요.
3. 로봇(CI)이 설명서의 <strong>맞춤법(lint)과 링크(linkchecker)를 자동 검사</strong>해서 품질도 보장해요!
