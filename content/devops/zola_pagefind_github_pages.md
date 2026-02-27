+++
title = "Zola + Pagefind로 GitHub Pages 검색 구현 완전 가이드"
date = 2026-02-28

[extra]
categories = "devops"
+++

# Zola + Pagefind로 GitHub Pages 검색 구현 완전 가이드

## 핵심 인사이트 (3줄 요약)

> **Zola**는 Rust로 만든 정적 사이트 생성기(SSG)로, Jekyll 대비 수십~수백 배 빠른 빌드 속도를 제공한다.  
> **Pagefind**는 빌드된 HTML을 인덱싱해 서버 없이 브라우저에서 전문 검색을 제공하는 Rust + WASM 도구다.  
> GitHub Actions에서 Zola 빌드 → Pagefind 인덱싱 → GitHub Pages 배포 순으로 연결하면 10만 글도 수 분 내 배포 가능하다.

---

## 1. 개념

### Zola

**Zola**는 Rust로 작성된 단일 바이너리 정적 사이트 생성기(SSG)다.

| 항목 | 설명 |
|------|------|
| **언어** | Rust (컴파일 언어, GC 없음) |
| **템플릿 엔진** | Tera (Jinja2/Liquid와 유사, 문법 90% 호환) |
| **출력 디렉토리** | `public/` |
| **설정 파일** | `config.toml` |
| **빌드 속도** | 10만 글 기준 1~3분 (Jekyll은 2~4시간) |
| **의존성** | 단일 바이너리 하나 (Ruby/Node 불필요) |

### Pagefind

**Pagefind**는 CloudCannon이 개발한 정적 사이트 전용 클라이언트 사이드 검색 엔진이다.

| 항목 | 설명 |
|------|------|
| **언어** | Rust + WebAssembly |
| **동작 방식** | 빌드된 HTML 파싱 → 검색 인덱스 생성 |
| **메모리 효율** | 청크 단위 지연 로딩 (전체 인덱스 미로드) |
| **서버 불필요** | 순수 정적 파일만으로 동작 |
| **한국어 지원** | `--force-language ko` 옵션 |

---

## 2. 등장 배경

| 기존 문제 | 설명 |
|-----------|------|
| **Jekyll 빌드 속도** | Ruby 단일 스레드, 글 수에 선형 비례해 느려짐 |
| **Algolia 의존성** | 외부 SaaS, 月 $29+, 데이터 외부 유출 우려 |
| **lunr.js 한계** | 전체 인덱스를 한 번에 메모리에 로드 |
| **서버 검색 불가** | GitHub Pages는 서버리스 환경 |

Zola + Pagefind 조합은 위 문제를 모두 해결한다.

---

## 3. 전체 디렉토리 구조

```
studynote/
├── config.toml              ← Zola 설정
├── content/                 ← 모든 마크다운 콘텐츠
│   ├── _index.md            ← 홈 페이지
│   ├── cs_fundamentals/
│   │   ├── _index.md        ← 섹션 인덱스
│   │   ├── network/
│   │   │   ├── _index.md
│   │   │   └── base64.md    ← 실제 포스트
│   │   └── ...
│   ├── programming/
│   │   ├── _index.md
│   │   └── rust/
│   │       ├── _index.md
│   │       └── trait.md
│   └── devops/
│       ├── _index.md
│       └── zola_pagefind.md
├── templates/               ← Tera 템플릿
│   ├── base.html            ← 기본 레이아웃
│   ├── index.html           ← 홈 페이지 템플릿
│   ├── page.html            ← 포스트 페이지
│   ├── section.html         ← 섹션(폴더) 페이지
│   └── icons/               ← SVG 아이콘
│       ├── search.html
│       ├── copy.html
│       └── ...
├── static/                  ← 정적 파일 (Zola가 public/으로 복사)
│   └── assets/css/style.css
├── package.json
└── .github/workflows/deploy.yml
```

---

## 4. 구현 방법 (단계별)

### 4.1 config.toml 설정

```toml
base_url = "https://<username>.github.io/<repo>"
title = "My Site"
description = "사이트 설명"
compile_sass = false
build_search_index = false   # Pagefind가 담당하므로 false

[markdown]
highlight_code = false       # highlight.js 등 외부 라이브러리 사용 시

[extra]
github_username = "username"
```

> **핵심**: `base_url`에 `/` 뒤 경로(repo명)까지 포함해야 정적 파일 경로가 올바르게 생성된다.

### 4.2 콘텐츠 파일 작성 (TOML front matter)

```toml
+++
title = "Base64 인코딩"
date = 2026-02-27

[extra]
categories = "cs_fundamentals-network"
+++

# Base64 인코딩

마크다운 본문...
```

**섹션 인덱스 파일** (`_index.md`):
```toml
+++
title = "Network"
description = "네트워크 관련 노트"
sort_by = "title"
+++
```

### 4.3 Tera 템플릿 작성

**`templates/base.html`** (기본 레이아웃):

```html
<!DOCTYPE html>
<html lang="ko-KR">
<head>
  <meta charset="utf-8">
  <title>{% block title %}{ { config.title } }{% endblock title %}</title>
  <link rel="stylesheet" href="{ { get_url(path='assets/css/style.css') } }">
</head>
<body>
  <header>
    <a href="{ { get_url(path='/') } }">홈</a>
    <input type="text" id="pagefind-search" placeholder="Search...">
    <div id="pagefind-dropdown"></div>
  </header>

  <main>
    {% block content %}{% endblock content %}
  </main>

  <script>
    // Pagefind lazy load
    async function initPagefind() {
      try {
        const pf = await import('{ { get_url(path="/pagefind/pagefind.js") } }');
        return pf;
      } catch(e) { return null; }
    }
    // ... 검색 로직
  </script>
</body>
</html>
```

**`templates/page.html`** (포스트 페이지):
```html
{% extends "base.html" %}

{% block content %}
<article class="post-content">
  { { page.content | safe } }   {# { { content } } 가 아닌 page.content | safe #}
</article>
{% endblock content %}
```

**`templates/section.html`** (섹션/폴더 페이지):
```html
{% extends "base.html" %}

{% block content %}
<div class="folder-list">

  {# 하위 섹션(폴더) #}
  {% for sub_path in section.subsections %}
    {% set sub = get_section(path=sub_path) %}
    <a href="{ { sub.permalink } }">📁 { { sub.title } }</a>
  {% endfor %}

  {# 이 섹션의 포스트 #}
  {% for page in section.pages %}
    <a href="{ { page.permalink } }">📄 { { page.title } }</a>
  {% endfor %}

</div>
{% endblock content %}
```

**`templates/index.html`** (홈 페이지 - 최신글 3개):
```html
{% extends "base.html" %}

{% block content %}
{# 각 섹션에서 페이지를 수집해 최신 3개 표시 #}
{%- set dl = get_section(path="cs_fundamentals/digital_logic/_index.md") -%}
{%- set nw = get_section(path="cs_fundamentals/network/_index.md") -%}
{%- set rust = get_section(path="programming/rust/_index.md") -%}
{%- set devops = get_section(path="devops/_index.md") -%}
{%- set all = dl.pages | concat(with=nw.pages) | concat(with=rust.pages) | concat(with=devops.pages) -%}
{%- set sorted = all | sort(attribute="date") | reverse -%}

{% for page in sorted | slice(end=3) %}
  <a href="{ { page.permalink } }">{ { page.title } }</a>
{% endfor %}
{% endblock content %}
```

> **Tera vs Liquid 주요 차이점**

| Jekyll Liquid | Zola Tera | 비고 |
|---|---|---|
| `{ { content } }` | `{ { page.content \| safe } }` | 필수 변경 |
| `{ { '/' \| relative_url } }` | `{ { get_url(path='/') } }` | URL 생성 |
| `{ { page.date \| date: "%Y" } }` | `{ { page.date \| date(format="%Y") } }` | 필터 문법 |
| `{% include icons/copy.html %}` | `{% include "icons/copy.html" %}` | 따옴표 추가 |
| `site.posts` | `section.pages` | 섹션 내 페이지 |
| `site.baseurl` | `config.base_url` | 설정값 접근 |

### 4.4 package.json

```json
{
  "name": "studynote",
  "scripts": {
    "build": "zola build && npx pagefind --site public --glob \"**/*.html\" --force-language ko",
    "serve": "zola serve"
  },
  "devDependencies": {
    "pagefind": "^1.4.0"
  }
}
```

### 4.5 GitHub Actions (deploy.yml)

```yaml
name: Build and Deploy (Zola)

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '24'
          cache: 'npm'

      - name: Install Node dependencies
        run: npm ci

      - name: Install Zola
        run: |
          ZOLA_VERSION="0.19.2"
          curl -sSL "https://github.com/getzola/zola/releases/download/v${ZOLA_VERSION}/zola-v${ZOLA_VERSION}-x86_64-unknown-linux-gnu.tar.gz" \
            | tar xzf - -C /usr/local/bin
          zola --version

      - name: Build Zola
        run: zola build           # → public/ 생성

      - name: Build Pagefind Index
        run: npx pagefind --site public --glob "**/*.html" --force-language ko
        # → public/pagefind/ 생성

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public            # Zola 출력 디렉토리

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url } }
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**흐름 요약**:
```
push to main
    ↓
Zola build → public/*.html 생성
    ↓
Pagefind 인덱싱 → public/pagefind/pagefind.js 생성
    ↓
public/ 전체 GitHub Pages 배포
    ↓
브라우저에서 import('/studynote/pagefind/pagefind.js') 로 검색
```

---

## 5. Jekyll에서 Zola로 마이그레이션하기

### 5.1 포스트 front matter 변환

```yaml
# Jekyll YAML (before)
---
layout: note
title: "Base64 인코딩"
date: 2026-02-27
categories: cs_fundamentals-network
original_path: cs_fundamentals/network
---
```

```toml
# Zola TOML (after)
+++
title = "Base64 인코딩"
date = 2026-02-27

[extra]
categories = "cs_fundamentals-network"
original_path = "cs_fundamentals/network"
+++
```

> **자동 변환 스크립트 (Python)**:
> ```python
> import os, re
>
> def convert(content):
>     m = re.match(r'^---\n(.+?)\n---\n', content, re.DOTALL)
>     if not m: return content
>     fm = {}
>     for line in m.group(1).split('\n'):
>         if ':' in line:
>             k, _, v = line.partition(':')
>             fm[k.strip()] = v.strip()
>     toml = ['+++',
>             f'title = "{fm.get("title","")}"',
>             f'date = {fm.get("date","")}',
>             '[extra]']
>     for k in ('categories', 'original_path'):
>         if k in fm:
>             toml.append(f'{k} = "{fm[k]}"')
>     toml.append('+++')
>     return '\n'.join(toml) + '\n' + content[m.end():]
> ```

### 5.2 파일 이동

```
_posts/2026-02-27-base64.md  →  content/cs_fundamentals/network/base64.md
_posts/2026-02-27-trait.md   →  content/programming/rust/trait.md
```

- 날짜 접두사(`2026-02-27-`) 제거
- `_posts/` 대신 섹션 디렉토리 내부로 이동
- `_index.md` (섹션 인덱스 파일) 각 디렉토리에 추가

### 5.3 레이아웃 파일 변환

| Jekyll (`_layouts/`) | Zola (`templates/`) |
|---|---|
| `default.html` | `base.html` |
| `note.html` | `page.html` |
| `folder.html` | `section.html` |
| `_includes/icons/` | `templates/icons/` |

---

## 6. Pagefind JavaScript 연동

검색 UI는 순수 JavaScript로 구현한다. Zola 템플릿(`base.html`)에 포함:

```js
var pagefind = null;
var searchCache = {};

// Focus 시 한 번만 lazy load
async function initPagefind() {
  if (pagefind) return;
  try {
    pagefind = await import('{ { get_url(path="/pagefind/pagefind.js") } }');
  } catch(e) {
    console.log('Pagefind not available (dev mode)');
  }
}

async function search(query) {
  if (!query || !pagefind) return;
  if (searchCache[query]) { renderResults(searchCache[query]); return; }
  const result = await pagefind.search(query);
  const data = await Promise.all(result.results.slice(0,5).map(r => r.data()));
  searchCache[query] = data;
  renderResults(data);
}

function renderResults(results) {
  const drop = document.getElementById('pagefind-dropdown');
  if (!results.length) {
    drop.innerHTML = '<div class="pf-empty">No results</div>';
  } else {
    drop.innerHTML = results.map(r =>
      `<a class="pf-result" href="${r.url}">${r.meta.title}</a>`
    ).join('');
  }
  drop.classList.add('open');
}

// 방향키 네비게이션
document.getElementById('pagefind-search').addEventListener('keydown', function(e) {
  const items = Array.from(document.querySelectorAll('.pf-result'));
  let idx = items.findIndex(el => el.classList.contains('pf-active'));
  if (e.key === 'ArrowDown') { idx = Math.min(idx+1, items.length-1); }
  else if (e.key === 'ArrowUp') { idx = Math.max(idx-1, 0); }
  else if (e.key === 'Enter' && idx >= 0) {
    window.location.href = items[idx].href; return;
  }
  items.forEach(el => el.classList.remove('pf-active'));
  if (items[idx]) items[idx].classList.add('pf-active');
});
```

---

## 7. 주의사항 / 트러블슈팅

### ⚠️ base_url 경로 필수 포함

```toml
# ❌ 잘못됨: 경로 누락
base_url = "https://username.github.io"

# ✅ 올바름: 레포 이름까지 포함
base_url = "https://username.github.io/studynote"
```

`get_url(path="assets/css/style.css")` 가 `https://username.github.io/studynote/assets/css/style.css`를 생성해야 한다.

### ⚠️ public/ 디렉토리를 artifact로 업로드

```yaml
# ❌ Jekyll 잔재: _site/ 업로드
- uses: actions/upload-pages-artifact@v3
  with:
    path: _site   # 틀림

# ✅ Zola 출력: public/ 업로드
- uses: actions/upload-pages-artifact@v3
  with:
    path: public  # 올바름
```

### ⚠️ Tera에서 전역 페이지 목록 없음

Zola의 Tera 템플릿은 `site.posts` 같은 전역 목록을 지원하지 않는다. 홈 페이지에서 최신 글을 보여주려면 각 섹션을 명시적으로 불러와 합쳐야 한다:

```tera
{%- set s1 = get_section(path="cs_fundamentals/network/_index.md") -%}
{%- set s2 = get_section(path="programming/rust/_index.md") -%}
{%- set all = s1.pages | concat(with=s2.pages) | sort(attribute="date") | reverse -%}
{% for page in all | slice(end=3) %}...{% endfor %}
```

### ⚠️ 로컬에서 검색 동작 안 함

`zola serve`로 로컬 실행 시 Pagefind 인덱스가 없으므로 검색 불가.
로컬 검색 테스트:
```bash
zola build && npx pagefind --site public --force-language ko
cd public && python3 -m http.server 8080
```

### ⚠️ 섹션 `_index.md` 누락 시 빌드 에러

```
Error: Failed to build site: content/cs_fundamentals/network is not a section
```
모든 콘텐츠 디렉토리에 `_index.md`가 있어야 한다:
```bash
touch content/cs_fundamentals/network/_index.md
```

---

## 8. 빌드 서버 성능 비교 (SSG 도구 비교)

| 항목 | Jekyll (Ruby) | Hugo (Go) | **Zola (Rust)** |
|------|--------------|-----------|-----------------|
| **빌드 시간 (100글)** | ~10초 | ~0.5초 | **~0.3초** |
| **빌드 시간 (10,000글)** | ~5분 | ~5초 | **~3초** |
| **빌드 시간 (100,000글)** | 2~4시간 | ~1분 | **~2분** |
| **Actions 콜드 스타트** | +15초 (Ruby 설치) | +3초 | **+3초** |
| **메모리 사용 (빌드 중)** | 높음 (Ruby GC) | 낮음 | **매우 낮음** |
| **의존성** | Ruby + Bundler | Go 바이너리 | **단일 바이너리** |
| **병렬 처리** | 제한적 | ✅ | **✅ Rayon 기반** |

> Zola는 Rust의 **Rayon** 라이브러리로 CPU 코어 수만큼 병렬 렌더링을 수행한다. 4코어 머신에서 Hugo 대비 비슷하거나 빠른 속도를 낸다.

---

## 8-1. Rust가 클라이언트 사이드에서 유리한 이유 (Pagefind 기준)

Pagefind는 **Rust → WebAssembly(WASM)** 로 컴파일된다. 브라우저에서 실행되는 검색 엔진이 왜 Rust/WASM인지가 핵심이다.

### 왜 JavaScript가 아닌 Rust + WASM인가?

| 비교 항목 | JavaScript 검색 (lunr.js, Fuse.js) | Rust + WASM (Pagefind) |
|-----------|-------------------------------------|------------------------|
| **인덱스 로딩** | 전체 인덱스를 한 번에 로드 | **청크 단위 지연 로딩** |
| **메모리 사용** | 인덱스 크기 = 메모리 사용 | **검색어별 필요한 청크만** |
| **실행 속도** | JS 엔진 JIT에 의존 | **WASM: 네이티브에 가까운 속도** |
| **GC 중단** | GC Pause로 검색 지연 가능 | **Rust: GC 없음, 일정한 응답속도** |
| **정밀도** | 단순 문자열 매칭 위주 | **역색인(Inverted Index) 기반** |
| **글 10만 개 지원** | 인덱스 수백 MB → 브라우저 OOM | **청크 로딩으로 수 MB만 사용** |

### 클라이언트 사이드 메모리 사용량 비교

| 검색 도구 | 글 1,000개 | 글 10,000개 | 글 100,000개 |
|-----------|-----------|------------|------------|
| **lunr.js** | ~5MB (전체 로드) | ~50MB ❌ | 수백 MB → 크래시 ❌ |
| **Fuse.js** | ~3MB (전체 로드) | ~30MB ❌ | 수백 MB → 크래시 ❌ |
| **Pagefind (WASM)** | **~50KB** | **~50KB** | **~50KB** |

> Pagefind의 런타임 메모리가 글 수와 무관하게 일정한 이유: **검색어에 해당하는 인덱스 청크만 네트워크에서 가져와 사용 후 버린다.**

### Rust WASM의 구체적 이점

```
사용자가 "rust"를 검색

JavaScript 검색 엔진:
  → 전체 index.json (50MB) 메모리에 상주
  → 50MB 중 "rust" 관련 부분 순회
  → 결과 반환

Pagefind (Rust WASM):
  → "r"로 시작하는 청크 파일 1개 (~10KB) 다운로드
  → WASM 바이너리에서 역색인 조회 (네이티브 속도)
  → 결과 반환
  → 청크 캐시 (재검색 시 재다운로드 없음)
  → 총 메모리: ~50KB
```

### WASM이 JS보다 빠른 이유

| 항목 | JavaScript | WebAssembly |
|------|-----------|-------------|
| **파싱** | 소스코드 → 파싱 → AST → JIT | **사전 컴파일된 바이너리 직접 실행** |
| **최적화** | 런타임 JIT 최적화 (불안정) | **AOT 최적화 (일정한 성능)** |
| **메모리 모델** | GC가 관리 (Pause 발생) | **선형 메모리, 수동 관리 (Pause 없음)** |
| **연산 집약 작업** | 느림 | **C/C++ 수준 속도** |
| **검색 벤치마크** | 기준값 1.0x | **2~10x 빠름** |

### 실제 검색 응답속도 비교 (글 10,000개 기준)

| 도구 | 첫 검색 (콜드) | 재검색 (캐시) | 메모리 |
|------|--------------|-------------|--------|
| **lunr.js** | 200~500ms (인덱스 로딩) | ~10ms | ~50MB |
| **Fuse.js** | 300~800ms (인덱스 로딩) | ~20ms | ~30MB |
| **Pagefind** | **50~150ms** (청크 다운) | **<5ms** | **~1MB** |

### 왜 Rust → WASM인가? (Go, C++ 대비)

Pagefind가 Rust를 선택한 이유:

| 이유 | 설명 |
|------|------|
| **Zero-cost abstractions** | 고수준 추상화가 런타임 오버헤드 없음 |
| **메모리 안전성** | GC 없이도 메모리 오류(dangling pointer, buffer overflow) 컴파일 타임 차단 |
| **wasm-pack 생태계** | Rust → WASM 변환 도구체인이 가장 성숙 |
| **크기 최적화** | `wasm-opt` 등을 통해 WASM 바이너리 최소화 가능 |
| **병렬 처리** | `rayon`, `tokio`로 인덱싱 단계 병렬화 |

---

## 9. 기술사적 판단

**현재 (2026) 최적 조합**: 소규모~중규모 기술 블로그/문서 사이트에서는 **Zola + Pagefind + GitHub Pages**가 비용 0원으로 사용할 수 있는 가장 완성도 높은 스택이다.

| 규모 | 추천 |
|------|------|
| ~1,000글 | Jekyll 또는 Zola 모두 OK |
| 1,000~50,000글 | **Zola 강력 추천** |
| 50,000글+ | **Zola 필수** (Jekyll로는 사실상 불가) |
| 검색 실시간성 필요 | Algolia / Meilisearch |

---

## 10. 미래 전망

| 트렌드 | 설명 |
|--------|------|
| **Rust 생태계 확장** | Zola, Pagefind 모두 Rust 기반으로 지속 성장 중 |
| **WASM 검색 고도화** | 벡터 임베딩 기반 시맨틱 검색과 결합 가능 |
| **AI 생성 콘텐츠** | 대량 글 자동 생성 시 빠른 빌드 도구 필수 |
| **Edge 배포** | Cloudflare Pages 등과 조합해 CDN 엣지 배포 |

---

## 🧒 어린이를 위한 설명

### 🏗️ 비유: 레고 + 도서관 색인

- **Zola (Rust)**: 설계도(마크다운)를 보고 레고 집(HTML)을 초고속으로 완성하는 로봇. Rust로 만들어서 거의 쉬지 않고 일한다.
- **Pagefind**: 레고 집이 완성된 후, 집 안 모든 방을 돌아다니며 "이 방에는 '네트워크'라는 단어가 있어!" 라고 색인 카드를 만드는 도서관 사서.
- **GitHub Actions**: 새 레고 설계도가 올라올 때마다 자동으로 로봇(Zola)을 깨우고, 사서(Pagefind)를 불러 색인을 갱신한 뒤, 전 세계 방문자에게 집을 공개하는 자동화 시스템.

---

## 참고

- [Zola 공식 문서](https://www.getzola.org/documentation/)
- [Tera 템플릿 문서](https://keats.github.io/tera/)
- [Pagefind 공식 문서](https://pagefind.app/)
- [Zola GitHub Releases](https://github.com/getzola/zola/releases)
- [actions/deploy-pages](https://github.com/actions/deploy-pages)
