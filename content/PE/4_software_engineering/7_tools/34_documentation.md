+++
title = "34. 문서화 도구 (Documentation Tools)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Documentation", "OpenAPI", "Swagger", "Docusaurus", "Docs-as-Code"]
draft = false
+++

# 문서화 도구 (Documentation Tools)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 문서화 도구는 **"소프트웨어 **문서**를 **자동화**하고 **관리**하는 **시스템"**으로, **OpenAPI/Swagger**(API **스펙), **Docusaurus**(정적 **사이트), **MkDocs**(Markdown **사이트), **Javadoc/Sphinx**(코드 **문서)가 **대표적**이다.
> 2. **Docs-as-Code**: **Markdown**, **YAML**, **JSDoc 같은 **텍스트 **기반 **형식**으로 **문서**를 **작성**하고 **Git**으로 **버전 **관리**하며 **CI/CD**로 **자동 **배포**한다.
> 3. **API 문서**: **OpenAPI Specification**(OAS)으로 **API **스펙**을 **정의**하고 **Swagger UI**, **Redoc**로 **시각화**하며 **코드 **생성**(Codegen)으로 **클라이언트 **SDK**를 **자동 **생성**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
문서화 도구는 **"기술 문서 관리 시스템"**이다.

**문서 유형**:
- **API 문서**: OpenAPI/Swagger
- **사용자 가이드**: Docusaurus, GitBook
- **코드 문서**: Javadoc, Sphinx
- **아키텍처**: C4 Model, Mermaid

### 💡 비유
문서화 도구는 ****자동 **매뉴얼 **생성기 ****와 같다.
- **코드/스펙**: 원본
- **도구**: 번역기
- **문서**: 결과물

---

## Ⅱ. 아키텍처 및 핵심 원리

### Docs-as-Code 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Docs-as-Code Pipeline                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Developer writes docs in Markdown/YAML alongside code                                 │  │
    │    │                                                                                   │  │
    │    ▼                                                                                   │  │
    │  Git Push                                                                                │  │
    │    │                                                                                   │  │
    │    ▼                                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  CI/CD Pipeline                                                                      │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  1. Lint: markdownlint, vale                                                     │  │  │  │
    │  │  │  2. Build: Docusaurus, MkDocs, Hugo                                               │  │  │  │
    │  │  │  3. Test: Broken links, spelling                                                 │  │  │  │
    │  │  │  4. Deploy: Netlify, Vercel, GitHub Pages                                        │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │    │                                                                                   │  │
    │    ▼                                                                                   │  │
    │  Published Documentation Site                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### OpenAPI Specification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         OpenAPI Specification (YAML)                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  openapi: 3.0.0                                                                         │  │
    │  info:                                                                                  │  │
    │    title: User API                                                                      │  │
    │    version: 1.0.0                                                                       │  │
    │  servers:                                                                               │  │
    │    - url: https://api.example.com/v1                                                    │  │
    │  paths:                                                                                 │  │
    │    /users:                                                                              │  │
    │      get:                                                                               │  │
    │        summary: List all users                                                          │  │
    │        parameters:                                                                      │  │
    │          - name: limit                                                                  │  │
    │            in: query                                                                    │  │
    │            schema:                                                                      │  │
    │              type: integer                                                              │  │
    │        responses:                                                                       │  │
    │          '200':                                                                         │  │
    │            description: Successful response                                             │  │
    │            content:                                                                     │  │
    │              application/json:                                                          │  │
    │                schema:                                                                  │  │
    │                  type: array                                                            │  │
    │                  items:                                                                 │  │
    │                    $ref: '#/components/schemas/User'                                    │  │
    │      post:                                                                              │  │
    │        summary: Create user                                                             │  │
    │        requestBody:                                                                     │  │
    │          content:                                                                       │  │
    │            application/json:                                                            │  │
    │              schema:                                                                    │  │
    │                $ref: '#/components/schemas/NewUser'                                     │  │
    │        responses:                                                                       │  │
    │          '201':                                                                         │  │
    │            description: User created                                                    │  │
    │  components:                                                                            │  │
    │    schemas:                                                                             │  │
    │      User:                                                                              │  │
    │        type: object                                                                     │  │
    │        properties:                                                                      │  │
    │          id:                                                                            │  │
    │            type: integer                                                                │  │
    │          name:                                                                          │  │
    │            type: string                                                                 │  │
    │          email:                                                                         │  │
    │            type: string                                                                 │  │
    │            format: email                                                                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 문서화 도구 비교

| 도구 | 용도 | 형식 | 빌드 |
|------|------|------|------|
| **Swagger UI** | API 문서 | OpenAPI/YAML | Static |
| **Redoc** | API 문서 | OpenAPI/YAML | Static |
| **Docusaurus** | 사이트 | Markdown/MDX | React |
| **MkDocs** | 사이트 | Markdown | Python |
| **Sphinx** | 코드 문서 | reStructuredText | Python |

### Javadoc/Sphinx 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Code Documentation                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Java (Javadoc):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  /**                                                                                     │  │
    │   * Calculates the factorial of a number.                                                │  │
    │   *                                                                                      │  │
    │   * @param n the number to calculate factorial for                                       │  │
    │   * @return the factorial of n                                                          │  │
    │   * @throws IllegalArgumentException if n is negative                                      │  │
    │   * @see MathUtils#power                                                                 │  │
    │   */                                                                                     │  │
    │  public static BigInteger factorial(int n) {                                             │  │
    │      if (n < 0) throw new IllegalArgumentException("n must be non-negative");               │  │
    │      BigInteger result = BigInteger.ONE;                                                │  │
    │      for (int i = 2; i <= n; i++) {                                                     │  │
    │          result = result.multiply(BigInteger.valueOf(i));                                │  │
    │      }                                                                                    │  │
    │      return result;                                                                      │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Python (Sphinx):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  def factorial(n: int) -> int:                                                           │  │
    │      """Calculate the factorial of a number.                                             │  │
    │                                                                                          │  │
    │      Args:                                                                               │  │
    │          n: The number to calculate factorial for. Must be non-negative.                 │  │
    │                                                                                          │  │
    │      Returns:                                                                            │  │
    │          The factorial of n.                                                             │  │
    │                                                                                          │  │
    │      Raises:                                                                             │  │
    │          ValueError: If n is negative.                                                   │  │
    │                                                                                          │  │
    │      Example:                                                                            │  │
    │          >>> factorial(5)                                                                │  │
    │          120                                                                             │  │
    │      """                                                                                 │  │
    │      if n < 0:                                                                           │  │
    │          raise ValueError("n must be non-negative")                                      │  │
    │      result = 1                                                                          │  │
    │      for i in range(2, n + 1):                                                           │  │
    │          result *= i                                                                     │  │
    │      return result                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Swagger UI 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Swagger UI Output                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User API v1.0                                 [Try it out]    ▼                     │  │  │
    │  │  ────────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │                                                                                       │  │  │
    │  │  GET /users                                                                 [Execute]   │  │  │
    │  │  List all users                                                                      │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Parameters:                                                                      │  │  │  │
    │  │  │  Name │  Type  │  Required  │  Description                                       │  │  │  │
    │  │  │  ─────┼────────┼───────────┼─────────────────────────────────────────────────────│  │  │  │
    │  │  │  limit│ integer│  No       │  Maximum number of results                          │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │  │
    │  │  Responses:                                                                         │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  200                                                                             │  │  │  │
    │  │  │  [                                                                              │  │  │  │
    │  │  │    {                                                                             │  │  │  │
    │  │  │      "id": 1,                                                                    │  │  │  │
    │  │  │      "name": "John Doe",                                                         │  │  │  │
    │  │  │      "email": "john@example.com"                                                 │  │  │  │
    │  │  │    }                                                                             │  │  │  │
    │  │  │  ]                                                                              │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### Docusaurus 설정

```javascript
// docusaurus.config.js
module.exports = {
  title: 'My Project Docs',
  tagline: 'Build better software',
  url: 'https://docs.example.com',
  baseUrl: '/',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/user/repo/edit/main/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'My Docs',
      items: [
        {to: '/docs/intro', label: 'Docs', position: 'left'},
        {to: '/blog', label: 'Blog', position: 'left'},
        {href: 'https://github.com/user/repo', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {title: 'Docs', items: [{label: 'Guide', to: '/docs/intro'}]},
        {title: 'Community', items: [{label: 'Stack Overflow', href: 'https://...'}]},
      ],
    },
  },
};
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: API 문서 자동화
**상황**: REST API 문서 작성
**판단**: OpenAPI + Swagger UI

```yaml
# .github/workflows/docs.yml
name: Generate API Docs

on:
  push:
    paths:
      - 'openapi.yaml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate Swagger UI
        run: |
          docker run --rm -v $PWD:/local \
            swaggerapi/swagger-ui \
            cp /local/openapi.yaml /local/swagger.html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

---

## Ⅴ. 기대효과 및 결론

### 문서화 기대 효과

| 효과 | 없음 | 도구 |
|------|------|------|
| **최신성** | 오래됨 | 자동 |
| **검색** | 어려움 | 쉬움 |
| **버전 관리** | 불가 | Git |

### 모범 사례

1. **코드 근접**: Markdown 파일을 코드와 함께
2. **자동화**: CI/CD로 배포
3. **버전**: Git Tag로 문서 버전 관리
4. **검토**: PR로 문서 리뷰

### 미래 전망

1. **AI 문서**: 자동 생성
2. **Interactive**: Try-it-out 기능
3. **Multi-format**: PDF, HTML, API

### ※ 참고 표준/가이드
- **OpenAPI**: specification.opendocs.org
- **Docusaurus**: docusaurus.io
- **Diataxis**: diataxis.fr (Framework)

---

## 📌 관련 개념 맵

- [린터](./7_tools/30_linter.md) - 문서 Lint
- [CI/CD](./13_devops_sre/1_pipeline.md) - 자동 배포
- [버전 관리](./8_collaboration/32_vcs.md) - Git
