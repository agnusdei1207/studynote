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

> 이 가이드는 실제 macos + GitHub Pages 환경에서 직접 구현하고 발생한 모든 트러블슈팅을 포함한다.

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
│   │   ├── _index.md        ← 섹션 인덱스 (필수!)
│   │   ├── network/
│   │   │   ├── _index.md    ← 섹션 인덱스 (필수!)
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
│   ├── base.html            ← 기본 레이아웃 (site-wide JS 포함)
│   ├── index.html           ← 홈 페이지 템플릿
│   ├── page.html            ← 포스트 페이지
│   ├── section.html         ← 섹션(폴더) 페이지
│   └── icons/               ← SVG 아이콘 include용
│       ├── search.html
│       ├── copy.html
│       └── ...
├── static/                  ← 정적 파일 (Zola가 public/으로 그대로 복사)
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

> **핵심**: `base_url`에 레포 이름까지 포함해야 정적 파일 경로가 올바르게 생성된다.
> 예: `"https://username.github.io"` (❌) → `"https://username.github.io/studynote"` (✅)

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

**섹션 인덱스 파일 (`_index.md`)** — 모든 콘텐츠 디렉토리에 필수:
```toml
+++
title = "Network"
description = "네트워크 관련 노트"
sort_by = "title"
+++
```

### 4.3 Tera 템플릿 작성

**`templates/base.html`** (기본 레이아웃):

{% raw %}
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
    // Pagefind lazy load — focus 시 초기화
    var pagefind = null;
    async function initPagefind() {
      if (pagefind) return;
      try {
        // Zola get_url()이 실제 배포 URL을 삽입 (서브경로 포함)
        pagefind = await import('{ { get_url(path="/pagefind/pagefind.js") } }');
      } catch(e) { console.log('Pagefind not available'); }
    }
    document.getElementById('pagefind-search')
      .addEventListener('focus', initPagefind);
  </script>
</body>
</html>
```
{% endraw %}

> **중요**: 위 코드에서 `{ { ... } }` (공백 포함)는 실제 파일에서 `{ { ... } }`로 작성해야 한다.
> 이 문서 파일 자체가 Zola로 빌드되므로 `{ { } }`를 직접 쓰면 shortcode로 오인식된다.

**`templates/page.html`** (포스트 페이지):
{% raw %}
```html
{% extends "base.html" %}

{% block content %}
<article class="post-content">
  { { page.content | safe } }
</article>
{% endblock content %}
```
{% endraw %}

Liquid → Tera 핵심 차이:

| Jekyll Liquid | Zola Tera | 비고 |
|---|---|---|
| `content` | `page.content \| safe` | 필수 변경 |
| `'/' \| relative_url` | `get_url(path='/')` | URL 생성 |
| `page.date \| date: "%Y"` | `page.date \| date(format="%Y")` | 필터 문법 |
| `include icons/copy.html` | `include "icons/copy.html"` | 따옴표 추가 |
| `site.posts` | `section.pages` | 섹션 내 페이지 |
| `site.baseurl` | `config.base_url` | 설정값 접근 |

**`templates/section.html`** (섹션/폴더 페이지):
{% raw %}
```html
{% extends "base.html" %}

{% block content %}

{# 브레드크럼: section.ancestors로 부모 섹션 자동 생성 #}
<div class="breadcrumb">
  <a href="{ { get_url(path='/') } }">root</a>
  {% for ancestor in section.ancestors %}
    {% set anc = get_section(path=ancestor) %}
    <span>/</span>
    <a href="{ { anc.permalink } }">{ { anc.title } }</a>
  {% endfor %}
  <span>/</span>
  <span>{ { section.title } }</span>
</div>

<div class="folder-list">
  {# 하위 섹션(폴더) - Jekyll site.html_pages 루프 불필요 #}
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
{% endraw %}

**`templates/index.html`** (홈 페이지 - 최신글):
{% raw %}
```html
{% extends "base.html" %}

{% block content %}
{# 각 섹션을 명시적으로 불러와 합산 (Tera는 전역 site.posts 없음) #}
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
{% endraw %}

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
        # → public/pagefind/ 생성 (이 단계 후에 배포해야 검색 동작)

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public            # ← Zola 출력 디렉토리 (Jekyll의 _site/ 아님!)

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

전체 빌드 흐름:
```
push to main
    ↓
Zola build → public/*.html 생성
    ↓
Pagefind 인덱싱 → public/pagefind/pagefind.js 생성
    ↓
public/ 전체 GitHub Pages 배포
    ↓
브라우저: import('/studynote/pagefind/pagefind.js') → 검색 동작
```

---

## 5. Jekyll에서 Zola로 마이그레이션하기

### 5.1 포스트 front matter 변환

Jekyll YAML:
```yaml
---
layout: note
title: "Base64 인코딩"
date: 2026-02-27
categories: cs_fundamentals-network
original_path: cs_fundamentals/network
---
```

Zola TOML:
```toml
+++
title = "Base64 인코딩"
date = 2026-02-27

[extra]
categories = "cs_fundamentals-network"
original_path = "cs_fundamentals/network"
+++
```

자동 변환 스크립트 (Python):
```python
import os, re

def convert(content):
    m = re.match(r'^---\n(.+?)\n---\n', content, re.DOTALL)
    if not m: return content
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    toml = ['+++',
            f'title = "{fm.get("title","")}"',
            f'date = {fm.get("date","")}',
            '[extra]']
    for k in ('categories', 'original_path'):
        if k in fm:
            toml.append(f'{k} = "{fm[k]}"')
    toml.append('+++')
    return '\n'.join(toml) + '\n' + content[m.end():]
```

### 5.2 파일 이동

```
_posts/2026-02-27-base64.md  →  content/cs_fundamentals/network/base64.md
_posts/2026-02-27-trait.md   →  content/programming/rust/trait.md
```

- 날짜 접두사(`2026-02-27-`) 제거
- `_posts/` 대신 섹션 디렉토리 내부로 이동
- `_index.md` (섹션 인덱스) 각 디렉토리에 추가

### 5.3 레이아웃 파일 변환

| Jekyll | Zola | 비고 |
|---|---|---|
| `_layouts/default.html` | `templates/base.html` | 전체 레이아웃 |
| `_layouts/note.html` | `templates/page.html` | 포스트 |
| `_layouts/folder.html` | `templates/section.html` | section.subsections로 단순화 |
| `_includes/icons/` | `templates/icons/` | 그대로 복사 |
| `assets/` | `static/assets/` | Zola가 public/으로 복사 |

---

## 6. Pagefind JavaScript 연동

검색 UI 전체 구현 코드 (templates/base.html 내 script 블록):

```js
var sInput = document.getElementById('pagefind-search');
var sDrop  = document.getElementById('pagefind-dropdown');
var sWrap  = document.getElementById('header-search-wrap');
var pagefind = null;
var searchCache = {};
var activeIdx = -1;

// 검색 입력창 focus 시 lazy load (첫 focus 때 한번만 로드)
async function initPagefind() {
  if (pagefind) return;
  try {
    // Zola 템플릿에서는 get_url(path="/pagefind/pagefind.js") 로 작성
    pagefind = await import('https://username.github.io/studynote/pagefind/pagefind.js');
  } catch(e) {
    console.log('Pagefind not available (dev mode)');
  }
}

async function search(query) {
  if (!query || !pagefind) return;
  if (searchCache[query]) { renderResults(searchCache[query], query); return; }
  const result = await pagefind.search(query);
  const data = await Promise.all(result.results.slice(0,5).map(r => r.data()));
  searchCache[query] = data;
  renderResults(data, query);
}

function renderResults(results, query) {
  if (!results.length) {
    sDrop.innerHTML = '<div class="pf-empty">No results</div>';
  } else {
    const frag = document.createDocumentFragment();
    results.forEach(r => {
      const a = document.createElement('a');
      a.className = 'pf-result';
      a.href = r.url;
      a.textContent = r.meta.title || 'Untitled';
      frag.appendChild(a);
    });
    sDrop.textContent = '';
    sDrop.appendChild(frag);
  }
  sDrop.classList.add('open'); // 콘텐츠 채운 뒤 마지막에 열기 (빈 박스 방지)
}

// 방향키 + Enter 네비게이션
sInput.addEventListener('keydown', function(e) {
  const items = Array.from(sDrop.querySelectorAll('.pf-result'));
  if (e.key === 'ArrowDown') { activeIdx = Math.min(activeIdx+1, items.length-1); }
  else if (e.key === 'ArrowUp') { activeIdx = Math.max(activeIdx-1, 0); }
  else if (e.key === 'Enter' && activeIdx >= 0) {
    window.location.href = items[activeIdx].href; return;
  }
  items.forEach((el,i) => el.classList.toggle('pf-active', i === activeIdx));
});

// 200ms debounce
var timer;
sInput.addEventListener('focus', initPagefind);
sInput.addEventListener('input', function() {
  activeIdx = -1;
  clearTimeout(timer);
  timer = setTimeout(() => search(this.value.trim()), 200);
});
window.onclick = e => { if (!sWrap.contains(e.target)) sDrop.classList.remove('open'); };
```

---

## 7. Rust가 클라이언트 사이드에서 유리한 이유

Pagefind는 **Rust → WebAssembly(WASM)** 로 컴파일된다.

### JavaScript 검색 vs Rust + WASM 검색

| 비교 항목 | lunr.js / Fuse.js (JS) | Pagefind (Rust WASM) |
|-----------|------------------------|----------------------|
| **인덱스 로딩** | 전체 인덱스를 한 번에 로드 | 검색어별 청크 1개만 로드 |
| **메모리 사용** | 인덱스 크기 = 메모리 | 검색 1회당 ~50KB 고정 |
| **GC 중단** | GC Pause로 지연 가능 | Rust: GC 없음 |
| **정밀도** | 단순 문자열 매칭 | 역색인(Inverted Index) |
| **10만 글 지원** | 수백 MB → 브라우저 OOM | 청크 로딩으로 항상 ~50KB |

### 클라이언트 사이드 메모리 비교

| 검색 도구 | 글 1,000개 | 글 10,000개 | 글 100,000개 |
|-----------|-----------|------------|------------|
| **lunr.js** | ~5MB | ~50MB ❌ | 수백 MB → 크래시 ❌ |
| **Fuse.js** | ~3MB | ~30MB ❌ | 수백 MB → 크래시 ❌ |
| **Pagefind (WASM)** | **~50KB** | **~50KB** | **~50KB** |

메모리가 글 수와 무관한 이유: **검색어에 해당하는 인덱스 청크만 네트워크에서 가져와 사용한다.**

역색인 구조:
```
빌드 타임:
  "rust"    → [문서 B (8%), 문서 D (20%)]
  "base64"  → [문서 A (15%)]
  "network" → [문서 A (5%), 문서 C (12%)]
     ↓
  index_r.pf_index  ("r"로 시작하는 모든 단어 역색인, ~10KB)
  index_n.pf_index  ("n"으로 시작, ~10KB)
  ...

런타임:
  "rust" 입력 → index_r.pf_index 1개만 fetch (~10KB)
  → WASM에서 역색인 조회 → 결과 반환
  → 총 메모리: ~50KB
```

### 실제 검색 응답속도 비교 (글 10,000개 기준)

| 도구 | 첫 검색 (콜드) | 재검색 (캐시) | 메모리 |
|------|--------------|-------------|--------|
| **lunr.js** | 200~500ms (인덱스 로딩) | ~10ms | ~50MB |
| **Fuse.js** | 300~800ms (인덱스 로딩) | ~20ms | ~30MB |
| **Pagefind** | **50~150ms** (청크 fetch) | **<5ms** | **~1MB** |

---

## 8. 빌드 도구 비교 (SSG)

| 항목 | Jekyll (Ruby) | Hugo (Go) | **Zola (Rust)** |
|------|--------------|-----------|-----------------||
| **빌드 시간 (100글)** | ~10초 | ~0.5초 | **~0.3초** |
| **빌드 시간 (10,000글)** | ~5분 | ~5초 | **~3초** |
| **빌드 시간 (100,000글)** | 2~4시간 | ~1분 | **~2분** |
| **Actions 콜드 스타트** | +15초 (Ruby 설치) | +3초 | **+3초** |
| **메모리 사용 (빌드 중)** | 높음 (Ruby GC) | 낮음 | **매우 낮음** |
| **병렬 처리** | 제한적 | ✅ | **✅ Rayon** |
| **의존성** | Ruby + Bundler | Go 바이너리 | **단일 바이너리** |
| **GitHub Pages 호환** | ✅ 공식 네이티브 | ✅ Actions | **✅ Actions** |

---

## 9. 트러블슈팅 (실제 발생한 문제 전부)

### ⚠️ 트러블 1: Zola 빌드 실패 — Shortcode 오인식

**오류 메시지**:
```
Error: Failed to build site
Reason: Found usage of a shortcode named `get_url` but we do not know about it.
```

**원인**: Zola 콘텐츠 파일(`.md`) 안에서 `{ { get_url(...) } }` 형태가 있으면, 코드 블록 내부라도 Zola가 shortcode 호출로 인식해 에러를 낸다. Tera 문법(템플릿)을 설명하는 문서를 작성할 때 특히 주의.

**해결**: `{ { } }` 안에 공백을 추가해서 shortcode 패턴에서 벗어나게 이스케이프

```diff
- { { get_url(path='/') } }
+ { { get_url(path='/') } }
```

또는 Python 스크립트로 일괄 처리:
```python
import re
content = re.sub(r'(?<!\$)\{\{', '{ {', content)
content = re.sub(r'\}\}', '} }', content)
content = content.replace('${{', '${{')  # GitHub Actions 표현식 복원
```

> 이 문제로 Run #25, #26이 연속 실패 → Pagefind 인덱스가 배포되지 않아 검색 결과 0건이 됐다.

---

### ⚠️ 트러블 2: 검색 결과 0건 (pagefind.js 404)

**현상**: 검색창에 무엇을 입력해도 항상 "No results" 표시. 콘솔에 `Pagefind not available` 반복 출력.

**원인**: GitHub Actions 빌드가 실패하거나, Pagefind 인덱싱 단계가 스킵되면 `public/pagefind/` 디렉토리가 생성되지 않은 채 배포됨.

**진단**:
1. Actions 탭에서 최근 워크플로 상태 확인
2. `build` 잡의 **"Build Pagefind Index"** 스텝이 성공했는지 확인
3. `https://<user>.github.io/<repo>/pagefind/pagefind.js` 직접 접속 → 200 OK 여부 확인

**해결**: 빌드 실패 원인 수정 후 재배포. 해결 순서:
```
1. 빌드 실패 원인 파악 (Actions 로그)
2. 원인 수정 후 push
3. Actions에서 "Build Pagefind Index" 스텝 성공 확인
4. pagefind.js URL 200 OK 확인
5. 실서버에서 검색 동작 확인
```

---

### ⚠️ 트러블 3: base_url 경로 누락

**오류**: CSS/JS 등 정적 파일 경로가 `/studynote/assets/css/style.css`가 아닌 `/assets/css/style.css`로 생성됨 (404)

```toml
# ❌ 잘못됨: 서브경로 누락
base_url = "https://username.github.io"

# ✅ 올바름: 레포 이름까지 포함
base_url = "https://username.github.io/studynote"
```

---

### ⚠️ 트러블 4: `public/` 대신 `_site/` 업로드

Jekyll에서 마이그레이션 시 artifact 경로를 바꾸지 않은 경우:

```yaml
# ❌ Jekyll 잔재
- uses: actions/upload-pages-artifact@v3
  with:
    path: _site

# ✅ Zola 출력
- uses: actions/upload-pages-artifact@v3
  with:
    path: public
```

---

### ⚠️ 트러블 5: `_index.md` 누락 시 빌드 에러

```
Error: content/cs_fundamentals/network is not a section
(or is not indexed)
```

**원인**: 콘텐츠 하위 디렉토리에 `_index.md`가 없으면 Zola가 섹션으로 인식하지 못함.

**해결**: 모든 콘텐츠 디렉토리에 `_index.md` 추가:
```bash
# 일괄 생성 예시
for dir in content/cs_fundamentals/*/; do
  echo '+++\ntitle = "Section"\n+++' > "${dir}_index.md"
done
```

---

### ⚠️ 트러블 6: 로컬에서 검색 동작 안 함

`zola serve`는 Pagefind 인덱스를 생성하지 않으므로 로컬에서 검색 불가.

**로컬 검색 테스트 방법**:
```bash
zola build && npx pagefind --site public --force-language ko
cd public && python3 -m http.server 8080
# → http://localhost:8080 에서 검색 테스트
```

---

### ⚠️ 트러블 7: `pages-build-deployment` 실패 무시

GitHub Pages 설정에서 Jekyll 빌더가 기본 활성화된 경우, 우리 Zola Actions와 별도로 `pages-build-deployment` 잡이 자동 실행되어 실패한다. **이건 무시해도 된다.** 우리 `Build and Deploy (Zola)` 워크플로가 이미 배포를 담당하고 있다.

혼란을 피하려면 GitHub Settings → Pages에서 Source를 "GitHub Actions"로 명시 설정.

---

## 10. 성능 정리

| 규모 | Jekyll | **Zola** | Pagefind 클라이언트 메모리 |
|------|--------|---------|--------------------------|
| ~1,000글 | OK | OK | ~50KB |
| ~10,000글 | 느림 | **빠름** | ~50KB |
| ~50,000글 | 매우 느림 | **빠름** | ~50KB |
| ~100,000글 | 사실상 불가 | **~2분** | ~50KB |

---

## 11. 기술 선택 가이드

| 상황 | 추천 |
|------|------|
| ~1,000글, 마이그레이션 비용 부담 | Jekyll 유지 |
| 1,000~50,000글 목표 | **Zola 강력 추천** |
| 50,000글+ 목표 | **Zola 필수** |
| 실시간 검색, 동적 데이터 | Algolia / Meilisearch |

---

## 🧒 어린이를 위한 설명

- **Zola (Rust)**: 설계도(마크다운)를 보고 레고 집(HTML)을 초고속으로 완성하는 Rust 로봇.
- **Pagefind**: 집 완성 후 모든 방을 돌며 "이 방엔 'network' 단어가 있어!"라고 색인 카드를 만드는 사서. 방이 100만 개여도 원하는 단어 해당 서랍만 열어본다 → 항상 빠르고 메모리 효율적.
- **GitHub Actions**: 새 설계도가 올라올 때마다 자동으로 Zola 로봇을 깨우고, Pagefind 사서를 불러 색인 갱신 후 전 세계에 공개하는 자동화 시스템.

---

## 참고

- [Zola 공식 문서](https://www.getzola.org/documentation/)
- [Tera 템플릿 문서](https://keats.github.io/tera/)
- [Pagefind 공식 문서](https://pagefind.app/)
- [Zola GitHub Releases](https://github.com/getzola/zola/releases)
- [actions/deploy-pages](https://github.com/actions/deploy-pages)
