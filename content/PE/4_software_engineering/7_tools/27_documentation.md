+++
title = "27. 문서화 도구 (Documentation Tools)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Documentation", "Markdown", "API-Docs", "OpenAPI", "Docusaurus"]
draft = false
+++

# 문서화 도구 (Documentation Tools)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 문서화 도구는 **"코드, API, **아키텍처를 **문서**로 **변환**하고 **배포**하는 **도구"**로, **Markdown**, **reStructuredText**로 **작성**하고 **Static Site Generator**(SSG)로 **HTML**을 **생성**하며 **API Documentation**(OpenAPI/Swagger)로 **인터페이스**를 **자동화**한다.
> 2. **가치**: **코드 주석**에서 **자동으로 **API 문서**를 **생성**하고 **버전 관리**(Git)와 **연동**하며 **CI/CD 파이프라인**에서 **자동 빌드**하고 **Search**, **Internationalization**(i18n)을 **지원**한다.
> 3. **융합**: **Markdown**(Typora, Obsidian), **SSG**(Docusaurus, VuePress, MkDocs), **API Docs**(Swagger, Postman, Insomnia), **Code Docs**(Javadoc, Sphinx, JSDoc)가 **대표적**이며 **Docs as Code** 전략으로 **문서**를 **코드처럼** **관리**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
문서화 도구는 **"기술 문서를 작성하고 배포하는 도구"**이다.

**문서 유형**:
- **코드 문서**: 주석에서 생성
- **API 문서**: 인터페이스 명세
- **가이드**: 사용자 매뉴얼
- **아키텍처**: 설계 문서

### 💡 비유
문서화는 **"건물 설계도****와 같다.
- **설계도**: 문서
- **건축**: 코딩
- **유지보수**: 문서 활용

---

## Ⅱ. 아키텍처 및 핵심 원리

### Docs as Code 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Docs as Code Pipeline                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Write (Markdown/AsciiDoc)                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  docs/                                                                              │  │  │
    │  │  ├── index.md                                                                      │  │  │
    │  │  ├── api/                                                                          │  │  │
    │  │  │   └── users.md                                                                  │  │  │
    │  │  └── guide/                                                                        │  │  │
    │  │      └── getting-started.md                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  2. Git Commit & Push                                                                  │  │
    │    │                                                                                     │  │
    │    ▼                                                                                     │  │
    │  3. CI/CD Pipeline                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  - Build HTML                                                                        │  │  │
    │  │  │  - Deploy to Hosting (GitHub Pages, Netlify)                                      │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │    │                                                                                     │  │
    │    ▼                                                                                     │  │
    │  4. Published Site                                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### OpenAPI/Swagger

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         OpenAPI Specification (YAML)                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  openapi: 3.0.0                                                                        │  │
    │  info:                                                                                  │  │
    │    title: User API                                                                      │  │
    │    version: 1.0.0                                                                       │  │
    │  paths:                                                                                 │  │
    │    /users:                                                                              │  │
    │      get:                                                                               │  │
    │        summary: Get all users                                                           │  │
    │        responses:                                                                       │  │
    │          '200':                                                                         │  │
    │            description: Successful response                                               │  │
    │            content:                                                                      │  │
    │              application/json:                                                           │  │
    │                schema:                                                                  │  │
    │                  type: array                                                            │  │
    │                  items:                                                                 │  │
    │                    $ref: '#/components/schemas/User'                                    │  │
    │    /users/{id}:                                                                         │  │
    │      get:                                                                               │  │
    │        summary: Get user by ID                                                          │  │
    │        parameters:                                                                      │  │
    │          - name: id                                                                     │  │
    │            in: path                                                                     │  │
    │            required: true                                                               │  │
    │            schema:                                                                      │  │
    │              type: integer                                                              │  │
    │  components:                                                                            │  │
    │    schemas:                                                                             │  │
    │      User:                                                                              │  │
    │        type: object                                                                    │  │
    │        properties:                                                                      │  │
    │          id:                                                                            │  │
    │            type: integer                                                                │  │
    │          name:                                                                          │  │
    │            type: string                                                                 │  │
    │          email:                                                                         │  │
    │            type: string                                                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 문서화 도구 비교

| 도구 | 타입 | 특징 | 사용처 |
|------|------|------|--------|
| **Docusaurus** | SSG | React, Facebook | 프로젝트 문서 |
| **VuePress** | SSG | Vue, Markdown 블록 | Vue 프로젝트 |
| **MkDocs** | SSG | Python, 간단함 | 기술 문서 |
| **Sphinx** | Code Docs | Python, reST | Python 프로젝트 |
| **Swagger** | API Docs | OpenAPI, UI | REST API |
| **Javadoc** | Code Docs | Java, HTML | Java 프로젝트 |

### SSG 비교

| 기능 | Docusaurus | VuePress | MkDocs |
|------|-----------|----------|--------|
| **Framework** | React | Vue | Python |
| **설치** | npm | npm | pip |
| **플러그인** | 풍부 | 중간 | 간단 |
| **검색** | Built-in | Algolia | Built-in |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Docusaurus 설정
**상황**: 프로젝트 문서
**판단**:

```yaml
# docusaurus.config.js
module.exports = {
  title: 'My Project',
  tagline: 'Build amazing things',
  url: 'https://example.com',
  baseUrl: '/docs/',

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
      title: 'My Project',
      items: [
        {to: '/docs/intro', label: 'Docs', position: 'left'},
        {to: '/blog', label: 'Blog', position: 'left'},
        {href: 'https://github.com/user/repo', label: 'GitHub', position: 'right'},
      ],
    },
  },
};
```

---

## Ⅴ. 기대효과 및 결론

### 문서화 기대 효과

| 효과 | 문서 없음 | 문서 있음 |
|------|----------|----------|
| **Onboarding** | 느림 | 빠름 |
| **유지보수** | 어려움 | 쉬움 |
| **협업** | 불편 | 편리 |

### 모범 사례

1. **Docs as Code**: Git 관리
2. **자동화**: CI/CD 통합
3. **검색**: 쉬운 탐색
4. **버전 관리**: 여러 버전

### 미래 전망

1. **AI Docs**: 자동 생성
2. **Interactive**: 실행 가능
3. **Video**: 통합

### ※ 참고 표준/가이드
- **OpenAPI**: spec.openapis.org
- **Docusaurus**: docusaurus.io
- **MkDocs**: mkdocs.org

---

## 📌 관련 개념 맵

- [CI/CD](./21_pipeline.md) - 파이프라인
- [버전 관리](../5_process/17_version_control.md) - Git
- [코드 리뷰](../5_process/14_code_review.md) - 리뷰
