+++
title = "Pagefind 완전 설명 — Rust + WASM 정적 검색 엔진"
date = 2026-02-28

[extra]
categories = "devops"
+++

# Pagefind 완전 설명 — Rust + WASM 정적 검색 엔진

## 한 줄 정의

> **정적 사이트(Static Site)를 위한 서버리스 전문 검색 엔진.** Rust로 작성되고 WebAssembly로 브라우저에서 실행된다.

---

## 1. 탄생 배경

정적 사이트(GitHub Pages, Netlify 등)는 **서버가 없다.** 서버가 없으니 검색 쿼리를 처리할 백엔드도 없다. 기존 해결책들의 문제:

| 기존 방법 | 문제점 |
|---|---|
| **Algolia** | 외부 서비스 의존, 유료, 데이터 외부 유출 |
| **lunr.js** | 브라우저에 전체 인덱스 로드 → 글 수 늘면 수백 MB |
| **Fuse.js** | 전체 데이터 메모리 로드, 대규모 불가 |
| **Elasticsearch** | 서버 필요, 정적 호스팅 불가 |

Pagefind는 이 모든 문제를 해결하기 위해 2022년 CloudCannon이 만들었다.

---

## 2. 핵심 작동 원리

**2단계로 작동한다: 빌드 타임 + 런타임**

### 빌드 타임 (인덱싱)

Zola/Jekyll 등으로 사이트를 빌드한 뒤 Pagefind CLI를 실행하면:

```bash
npx pagefind --site public
```

1. `public/` 안의 모든 `.html` 파일을 읽는다
2. 각 페이지의 텍스트를 추출, **역색인(Inverted Index)** 을 만든다
3. 역색인을 **알파벳/음절 단위 청크 파일**로 분할해 저장한다

```
public/pagefind/
  ├── pagefind.js          (~30KB, WASM 로더)
  ├── pagefind.wasm        (Rust 컴파일 검색 엔진)
  ├── index_a.pf_index     ("a"로 시작하는 단어들의 역색인)
  ├── index_r.pf_index     ("rust", "rayon" 등)
  ├── index_n.pf_index     ("network", "node" 등)
  └── data_xxxxx.pf_meta   (문서 제목, URL, 스니펫)
```

### 런타임 (검색)

사용자가 `"rust"` 를 입력하면:

```
① pagefind.js 초기화 (첫 focus 시 1회만, ~30KB)
       ↓
② "r"로 시작하는 청크 파일 1개만 fetch (index_r.pf_index, ~10KB)
       ↓
③ WASM 바이너리에서 역색인 조회 (네이티브 속도)
       ↓
④ "rust" 포함 문서 ID 목록 + 관련도 점수 반환
       ↓
⑤ 상위 5개 문서의 메타데이터(제목, URL, 스니펫) fetch
       ↓
⑥ JavaScript가 결과를 DOM에 렌더링
```

**이 과정에서 브라우저 메모리에 올라온 데이터: ~50KB** — 글이 10개든 10만 개든 동일.

---

## 3. 왜 메모리가 항상 일정한가

```
lunr.js : 메모리 = O(N)   (글 수에 선형 비례)
Pagefind: 메모리 = O(1)   (검색 1회당 청크 1~2개 고정)
```

**도서관 비유**:
- **lunr.js**: 도서관 모든 책의 색인을 통째로 복사해서 가방에 넣고 검색한다
- **Pagefind**: 색인 카드를 ㄱ/ㄴ/ㄷ... 서랍으로 나눠두고, 해당 서랍 하나만 꺼낸다

역색인 구조:
```
빌드 타임 생성:
  "rust"    → [문서 B (8%), 문서 D (20%)]
  "base64"  → [문서 A (15%)]
  "network" → [문서 A (5%), 문서 C (12%)]

→ index_r.pf_index 에는 "r"로 시작하는 단어 역색인만 저장 (~10KB)

런타임:
  "rust" 입력
  → index_r 1개 fetch (~10KB)
  → WASM 조회
  → 결과 반환 (총 메모리: ~50KB)
```

---

## 4. 왜 Rust + WASM인가

| 항목 | JavaScript | Rust → WASM |
|---|---|---|
| **실행 방식** | JIT 컴파일 (매번 최적화) | AOT 컴파일 (미리 최적화됨) |
| **GC** | 있음 (Pause 발생 가능) | 없음 (일정한 응답 속도) |
| **역색인 파싱** | 느림 | C 수준 속도 |
| **바이너리 크기** | — | wasm-opt으로 최소화 |
| **메모리 모델** | GC가 관리 | 선형 메모리, 수동 관리 |
| **검색 벤치마크** | 기준 1.0x | 2~10x 빠름 |

Pagefind의 `.pf_index` 파일은 JSON이 아닌 **바이너리 포맷**으로, WASM이 이를 파싱·조회하는 작업을 JS 대비 2~10배 빠르게 처리한다.

Rust를 선택한 이유:

| 이유 | 설명 |
|---|---|
| **Zero-cost abstractions** | 고수준 추상화가 런타임 오버헤드 없음 |
| **메모리 안전성** | GC 없이도 컴파일 타임에 메모리 오류 차단 |
| **wasm-pack 생태계** | Rust → WASM 변환 도구체인이 가장 성숙 |
| **병렬 인덱싱** | `rayon` 으로 빌드 타임 병렬 처리 |

---

## 5. 클라이언트 사이드 메모리 비교

| 검색 도구 | 글 1,000개 | 글 10,000개 | 글 100,000개 |
|-----------|-----------|------------|------------|
| **lunr.js** | ~5MB | ~50MB ❌ | 수백 MB → 크래시 ❌ |
| **Fuse.js** | ~3MB | ~30MB ❌ | 수백 MB → 크래시 ❌ |
| **Pagefind (WASM)** | **~50KB** | **~50KB** | **~50KB** |

---

## 6. 실제 성능 수치

| 규모 | 전체 인덱스 크기 | 검색당 로드 | 첫 검색 응답 |
|---|---|---|---|
| 1,000글 | ~50KB | ~5KB | <100ms |
| 10,000글 | ~325KB | ~20KB | ~100ms |
| 100,000글 | ~4~8MB | ~50KB | ~300ms |

| 도구 | 첫 검색 (콜드) | 재검색 (캐시) | 메모리 |
|------|--------------|-------------|--------|
| **lunr.js** | 200~500ms | ~10ms | ~50MB |
| **Fuse.js** | 300~800ms | ~20ms | ~30MB |
| **Pagefind** | **50~150ms** | **<5ms** | **~1MB** |

---

## 7. 주요 특징

| 특징 | 설명 |
|---|---|
| **한국어 지원** | `--force-language ko` 옵션 |
| **검색어 하이라이트** | 결과에 매칭 단어 자동 강조 |
| **다국어** | 언어별 인덱스 자동 분리 |
| **필터링** | 특정 섹션/태그로 검색 범위 제한 가능 |
| **커스텀 메타** | `data-pagefind-meta` 속성으로 커스텀 데이터 인덱싱 |
| **페이지 제외** | `data-pagefind-ignore` 속성으로 특정 요소 제외 |
| **CDN 친화적** | 청크 파일이 작아 CDN 캐싱 최적 |
| **서버 불필요** | 순수 정적 파일만으로 동작 |

---

## 8. HTML 연동 방법

```html
<!-- 검색 입력창 -->
<input type="text" id="pagefind-search" placeholder="Search...">
<div id="pagefind-dropdown"></div>

<script>
var pagefind = null;

// Focus 시 lazy load — 한 번만 실행
async function initPagefind() {
  if (pagefind) return;
  try {
    pagefind = await import('/pagefind/pagefind.js');
  } catch(e) {
    console.log('Pagefind not available');
  }
}

// 검색 실행
async function search(query) {
  if (!query || !pagefind) return;
  const result = await pagefind.search(query);
  const data = await Promise.all(
    result.results.slice(0, 5).map(r => r.data())
  );
  renderResults(data);
}

function renderResults(results) {
  const drop = document.getElementById('pagefind-dropdown');
  drop.innerHTML = results.map(r =>
    `<a href="${r.url}">${r.meta.title}</a>`
  ).join('');
}

document.getElementById('pagefind-search')
  .addEventListener('focus', initPagefind);

var timer;
document.getElementById('pagefind-search')
  .addEventListener('input', function() {
    clearTimeout(timer);
    timer = setTimeout(() => search(this.value.trim()), 200);
  });
</script>
```

### 특정 요소 인덱싱 제어

```html
<!-- 이 요소만 인덱싱 (나머지 제외) -->
<article data-pagefind-body>
  ...본문...
</article>

<!-- 이 요소는 인덱싱에서 제외 -->
<nav data-pagefind-ignore>...</nav>

<!-- 커스텀 메타데이터 추가 -->
<span data-pagefind-meta="author">홍길동</span>
```

---

## 9. 한계

| 한계 | 설명 |
|---|---|
| **오프라인 불가** | 청크 파일을 네트워크에서 fetch해야 함 |
| **실시간 인덱싱 불가** | 글 추가 시 반드시 재빌드 + 재배포 필요 |
| **로컬 개발 검색 불가** | `zola/jekyll serve` 환경에서는 인덱스가 없음 |
| **시맨틱 검색 불가** | 키워드 매칭 기반 (AI 벡터 검색 아님) |

---

## 10. 사용 적합성

| 상황 | Pagefind 적합도 |
|---|---|
| GitHub Pages / Netlify 정적 사이트 | ✅ 최적 |
| 기술 블로그 / 문서 사이트 | ✅ 최적 |
| 대용량 콘텐츠 (10만 글+) | ✅ 가능 |
| 실시간 데이터 검색 | ❌ Elasticsearch 사용 |
| AI 시맨틱 검색 | ❌ 벡터 DB 사용 |
| 동적 서버 사이트 | ❌ 서버 검색 엔진 사용 |

---

## 🧒 어린이를 위한 설명

Pagefind는 **도서관 사서** 같은 존재예요.

1. **사서가 색인 카드를 만든다** (빌드 타임): 도서관(사이트)이 완성되면, 사서(Pagefind)가 모든 책을 읽고 "이 책에는 'rust'라는 단어가 있어!"라고 카드를 ㄱ/ㄴ/ㄷ 서랍에 정리한다.

2. **손님이 단어를 말하면** (런타임): "rust 찾아줘"라고 하면, 사서는 'ㄹ' 서랍(~10KB)만 열어서 바로 찾아준다. 책이 100만 권이어도 그 서랍만 열면 된다.

3. **서버가 필요 없다**: 사서(카드 색인)가 이미 정리돼 있어서, 도서관장(서버)이 없어도 손님이 직접 서랍을 열어볼 수 있다.

---

## 참고

- [Pagefind 공식 문서](https://pagefind.app/)
- [Pagefind GitHub](https://github.com/CloudCannon/pagefind)
- [CloudCannon 블로그 — Pagefind 소개](https://cloudcannon.com/blog/introducing-pagefind/)
