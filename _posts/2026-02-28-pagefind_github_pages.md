---
layout: note
categories: devops
title: GitHub Pages + Pagefind 정적 사이트 검색 구현
date: 2026-02-28
---

# GitHub Pages + Pagefind 정적 사이트 검색 구현

## 핵심 인사이트 (3줄 요약)

> **Pagefind**는 정적 사이트 빌드 후 HTML을 직접 인덱싱하여 서버 없이 검색을 제공하는 도구다.  
> GitHub Actions에서 Jekyll 빌드 → Pagefind 인덱싱 → GitHub Pages 배포 순으로 연결하면 된다.  
> Ruby/Gemfile 버전 불일치, `pagefind.js` 404, 빈 드롭다운 등 세 가지 함정을 주의해야 한다.

---

## 1. 개념

**Pagefind**는 정적 사이트(Static Site)를 위한 **클라이언트 사이드 전문 검색 엔진(Client-side Full-text Search Engine)**이다.

| 구분 | 설명 |
|------|------|
| **동작 방식** | 빌드 후 HTML 파일을 분석해 검색 인덱스를 생성, 브라우저에서 직접 쿼리 |
| **서버 불필요** | 별도 검색 서버(Elasticsearch, Algolia 등) 없이 정적 파일만으로 동작 |
| **번들 크기** | Pagefind JS 번들 + 인덱스 파일 합쳐 보통 수백 KB 이하 |
| **언어 지원** | 한국어 포함 다국어 지원 (`--force-language ko` 옵션) |

```
빌드 흐름:
  Jekyll Build → _site/*.html 생성
       ↓
  npx pagefind --site _site
       ↓
  _site/pagefind/pagefind.js 및 인덱스 파일 생성
       ↓
  브라우저에서 import('/pagefind/pagefind.js') 로 검색 실행
```

---

## 2. 등장 배경

| 기존 문제 | 설명 |
|-----------|------|
| **서버 의존성** | Elasticsearch, Solr 등은 별도 서버가 필요해 GitHub Pages 불가 |
| **Algolia 의존성** | 외부 SaaS 서비스로 무료 한도 제한, 데이터 외부 유출 우려 |
| **lunr.js 한계** | 클라이언트 전체 인덱스를 한 번에 로드해 대용량 사이트에서 느림 |
| **Jekyll 기본 검색 없음** | Jekyll 자체 검색 기능 미지원 |

Pagefind는 빌드 타임 인덱싱 + 런타임 청크 로딩 방식으로 위 단점을 모두 해결한다.

---

## 3. 구성 요소

| 구성 요소 | 위치 | 역할 |
|-----------|------|------|
| **pagefind CLI** | `devDependencies` | 빌드 후 HTML 인덱싱 |
| **pagefind.js** | `_site/pagefind/` | 브라우저에서 검색 쿼리 실행 |
| **인덱스 파일** | `_site/pagefind/*.pf_index` | 실제 검색 데이터 (청크 단위 로딩) |
| **GitHub Actions** | `.github/workflows/` | 빌드 자동화 파이프라인 |
| **검색 UI** | 레이아웃 HTML | 검색 입력 + 결과 드롭다운 |

---

## 4. 구현 방법 (단계별)

### 4.1 패키지 설치

```bash
npm install --save-dev pagefind
```

`package.json`:
```json
{
  "scripts": {
    "build": "bundle exec jekyll build && npx pagefind --site _site",
    "serve": "bundle exec jekyll serve"
  },
  "devDependencies": {
    "pagefind": "^1.4.0"
  }
}
```

### 4.2 GitHub Actions 워크플로우

`.github/workflows/deploy.yml`:
```yaml
name: Build and Deploy

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

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'          # ← 반드시 실제 존재하는 버전
          bundler-cache: true

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '24'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build Jekyll
        run: bundle exec jekyll build

      - name: Build Pagefind Index
        run: npx pagefind --site _site --glob "**/*.html" --force-language ko

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

> **핵심**: Jekyll 빌드로 `_site` 생성 → Pagefind가 `_site`를 인덱싱 → `_site째로 배포

### 4.3 Gemfile 설정

```ruby
source "https://rubygems.org"

ruby ">= 3.3"    # ← deploy.yml의 ruby-version과 반드시 일치

gem "jekyll", "~> 4.4"
gem "jekyll-feed"
gem "jekyll-seo-tag"
gem "jekyll-sitemap"
gem "jekyll-paginate"
```

### 4.4 검색 UI 구현 (레이아웃 HTML)

```html
<!-- 검색 입력창 -->
<div class="header-search" id="header-search-wrap">
  <input type="text" id="pagefind-search" placeholder="Search anything..." autocomplete="off">
  <div id="pagefind-dropdown"></div>
</div>

<script>
  var sInput = document.getElementById('pagefind-search');
  var sDrop  = document.getElementById('pagefind-dropdown');
  var sWrap  = document.getElementById('header-search-wrap');
  var pagefind = null;
  var pagefindLoading = false;
  var searchCache = {};

  // Focus 시 lazy load
  async function initPagefind() {
    if (pagefind || pagefindLoading) return;
    pagefindLoading = true;
    try {
      pagefind = await import('/pagefind/pagefind.js');
    } catch (e) {
      console.log('Pagefind not available');
    }
    pagefindLoading = false;
  }

  async function search(query) {
    if (!query) {
      sDrop.classList.remove('open');
      sDrop.textContent = '';
      return;
    }
    if (pagefindLoading) {
      sDrop.innerHTML = '<div class="pf-empty">Searching...</div>';
      sDrop.classList.add('open');
      return;
    }
    if (!pagefind) {
      sDrop.innerHTML = '<div class="pf-empty">No results</div>';
      sDrop.classList.add('open');
      return;
    }
    if (searchCache[query]) {
      renderResults(searchCache[query], query);
      return;
    }
    var result  = await pagefind.search(query);
    var results = await Promise.all(
      result.results.slice(0, 5).map(r => r.data())
    );
    searchCache[query] = results;
    renderResults(results, query);
  }

  function renderResults(results, query) {
    if (results.length === 0) {
      sDrop.innerHTML = '<div class="pf-empty">No results</div>';
    } else {
      var frag = document.createDocumentFragment();
      results.forEach(r => {
        var a = document.createElement('a');
        a.className = 'pf-result';
        a.href = r.url;
        a.textContent = r.meta.title || 'Untitled';
        frag.appendChild(a);
      });
      sDrop.textContent = '';
      sDrop.appendChild(frag);
    }
    sDrop.classList.add('open');  // 콘텐츠 채운 뒤 열기
  }

  var debounceTimer;
  sInput.addEventListener('focus', () => initPagefind());
  sInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => search(this.value.trim()), 200);
  });
  window.onclick = e => {
    if (!sWrap.contains(e.target)) sDrop.classList.remove('open');
  };
</script>
```

---

## 5. 주의사항 / 트러블슈팅

### ⚠️ 함정 1: Ruby 버전 불일치 (가장 흔한 원인)

GitHub Actions 빌드 실패 에러:
```
Your Ruby version is 3.3.x, but your Gemfile specified >= 4.0
```

**원인**: `deploy.yml`과 `Gemfile` 두 곳의 Ruby 버전이 다름  
**해결**: 반드시 양쪽 모두 같은 실제 존재하는 버전으로 일치시켜야 함

```diff
# deploy.yml
-  ruby-version: '4.0'
+  ruby-version: '3.3'

# Gemfile
- ruby ">= 4.0"
+ ruby ">= 3.3"
```

> Ruby 4.0은 2026년 현재 출시되지 않은 버전이다. `ruby/setup-ruby@v1`은 존재하지 않는 버전을 지정하면 빌드가 즉시 실패한다.

---

### ⚠️ 함정 2: pagefind.js 404 오류

```
Failed to load resource: 404 /pagefind/pagefind.js
```

**원인**: GitHub Actions 빌드 실패 → `_site/pagefind/` 폴더가 생성되지 않은 채 배포됨  
**확인 방법**:
1. `https://github.com/<user>/<repo>/actions` 에서 최신 워크플로우 확인
2. `Build Pagefind Index` 스텝이 실행됐는지 확인
3. 빌드 성공 후에도 404면 `_site` 업로드 경로 확인

---

### ⚠️ 함정 3: 빈 흰 박스 (빈 드롭다운) 노출

**증상**: 검색어 입력 시 아무 내용 없는 흰 박스가 뜸  
**원인**: `sDrop.classList.add('open')`을 콘텐츠 삽입 **전**에 실행하는 코드 패턴

```js
// ❌ 잘못된 패턴: 먼저 열고 나서 콘텐츠 채움
sDrop.classList.add('open');
search(q);  // 비동기 - pagefind 미로드 시 빈 채로 열림

// ✅ 올바른 패턴: 콘텐츠 채운 뒤 열기
function renderResults(results, query) {
  // ... 콘텐츠 삽입 ...
  sDrop.classList.add('open');  // 마지막에 열기
}
```

---

### ⚠️ 함정 4: 로컬에서는 검색 동작 안 함

`bundle exec jekyll serve`로 로컬 실행 시 Pagefind 인덱스가 없어 검색 불가.  
로컬에서 검색 테스트가 필요하면:

```bash
npm run build        # Jekyll 빌드 + Pagefind 인덱싱
npx jekyll serve --skip-initial-build
# 또는
cd _site && python3 -m http.server 4000
```

---

## 6. 검증 방법

| 확인 항목 | 방법 |
|-----------|------|
| Actions 빌드 성공 | `https://github.com/<user>/<repo>/actions` |
| pagefind.js 존재 | `https://<user>.github.io/<repo>/pagefind/pagefind.js` → 200 OK |
| 검색 동작 | 사이트에서 검색어 입력 후 결과 확인 |
| 브라우저 콘솔 | DevTools → Console에서 `Pagefind not available` 없는지 확인 |

---

## 7. 기술사적 판단

| 상황 | 권장 도구 |
|------|-----------|
| **GitHub Pages / Netlify 정적 사이트** | Pagefind ✅ |
| **대규모 콘텐츠 (1만 페이지+)** | Algolia, Meilisearch |
| **실시간 데이터 검색** | Elasticsearch |
| **내부 문서 사이트** | Pagefind / Fuse.js |

Pagefind는 서버리스(Serverless) 환경에서 검색이 필요한 기술 블로그, 문서 사이트에 최적이다.  
월 요금이 없고 외부 서비스 의존 없이 소유권을 완전히 가져갈 수 있다는 점에서 기술 부채가 없다.

---

## 8. 미래 전망

| 트렌드 | 설명 |
|--------|------|
| **Edge Computing** | Cloudflare Workers 등에서 경량 검색 서버 실행 가능 |
| **AI 검색** | 벡터 임베딩 기반 시맨틱 검색과 결합 가능성 |
| **WebAssembly** | Pagefind 자체가 Rust + WASM 기반으로 속도 지속 개선 중 |
| **인덱스 분할** | 대규모 사이트에서 청크 단위 지연 로딩으로 성능 향상 |

---

## 🧒 어린이를 위한 설명

### 📚 비유: 도서관 색인 카드

Pagefind는 **"도서관에 색인 카드를 미리 만들어두는 사람"**이에요.

- **책(HTML 페이지)**: 도서관에 있는 수많은 책
- **색인 카드(pagefind 인덱스)**: 어떤 단어가 몇 번 책 몇 페이지에 있는지 적은 카드
- **검색창**: 카드 서랍
- **GitHub Actions**: 새 책이 들어올 때마다 색인 카드를 자동으로 업데이트해주는 사서

🔍 여러분이 검색창에 단어를 치면, 색인 카드를 뒤져서 "이 책에 있어요!"라고 알려주는 거예요. 서버가 없어도 미리 카드를 만들어뒀기 때문에 바로 찾을 수 있답니다.

---

## 참고

- [Pagefind 공식 문서](https://pagefind.app)
- [ruby/setup-ruby GitHub Action](https://github.com/ruby/setup-ruby)
- [actions/deploy-pages](https://github.com/actions/deploy-pages)
