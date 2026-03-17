+++
title = "577-580. SSR, SSG, ISR, PWA, WebAssembly"
date = "2026-03-15"
[extra]
category = "Architecture"
id = 577
+++

# 577-580. SSR, SSG, ISR, PWA, WebAssembly

### # 현대 웹 아키텍처 렌더링 및 실행 환경

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 웹 애플리케이션의 성능과 SEO 최적화를 위해 렌더링 타이밍(빌드/요청/중간)을 전략적으로 선택하고, WebAssembly를 통해 브라우저 연산 능력을 극대화하는 아키텍처 패러다임의 전환입니다.
> 2. **가치**: **LCP (Largest Contentful Paint)** 및 **CLS (Cumulative Layout Shift)** 같은 Core Web Vitals 지표를 획기적으로 개선하여 사용자 이탈률을 낮추고, 검색 엔진 노출 효과를 극대화하며, 네이티브 앱 수준의 UX를 웹에서 구현합니다.
> 3. **융합**: CDN (Content Delivery Network) 캐싱 전략, 백엔드 마이크로서비스와의 통합 비동기 처리, 그리고 AI/컴퓨터 비전 등 고성능 연산을 브라우저로 이동시키는 Client-Side Computing과의 시너지가 핵심입니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
전통적인 **CSR (Client-Side Rendering)** 방식은 서버가 빈 껍데기 HTML을 전송하고 브라우저에서 **JS (JavaScript)**로 콘텐츠를 그리는 방식이었습니다. 이는 풍부한 인터랙션을 제공했지만, 초기 로딩 속도 느림, **SEO (Search Engine Optimization)** 취약 등의 문제가 있었습니다. 이를 해결하기 위해 서버에서 HTML을 완성해서 보내는 **SSR (Server-Side Rendering)**, 빌드 타임에 미리 만들어 배포하는 **SSG (Static Site Generation)** 등이 등장했습니다. 최근에는 이를 융합한 **ISR (Incremental Static Regeneration)**과 같은 하이브리드 전략이 주류를 이루며, "어디서 렌더링할 것인가"는 현대 웹 아키텍처의 가장 중요한 의사결정 포인트가 되었습니다.

**2. 등장 배경**
① **기존 한계**: 모바일 환경에서의 느린 네트워크와 저사양 디바이스에서의 JS 실행 부하로 인한 "흰 바탕 화면(White Screen)" 현상.
② **혁신적 패러다임**: **HTTP/2**, **HTTP/3**의 등장과 서버 리소스의 가상화로 서버 렌더링 비용이 절감되고, **Edge Computing** 기반의 글로벌 분산 처리가 가능해짐.
③ **현재 비즈니스 요구**: 구글 등 검색 엔진의 **Core Web Vitals** 중심 랭킹 알고리즘 변경과 오프라인에서도 작동하는 앱 같은 웹(**PWA**)에 대한 요구가 급증함.

**3. 💡 섹션 요약 비유**
레스토랑에서 웨이팅 없이 즉시 식사를 할 수 있는 **도시락(SSG)**, 주문하면 조리해서 완성된 요리를 서빙해 주는 **레스토랑(SSR)**의 차이와 같습니다. 레스토랑은 신선하지만 느릴 수 있고, 도시락은 빠르지만 메뉴가 정해져 있습니다. 최근에는 미리 조리해둔 음식을 빠르게 제공하면서도 주문이 들어오면 신선하게 재료를 갈아 끼우는 **키토치(키오스크 + 도시락) 방식(ISR)**으로 진화하고 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 렌더링 전략 상세 비교표**
이 각각의 방식은 TCO (Total Cost of Ownership)와 개발 복잡도, 그리고 사용자 경험의 트레이드오프를 관리하는 기술입니다.

| 구분 | CSR (Client-Side Rendering) | SSR (Server-Side Rendering) | SSG (Static Site Generation) | ISR (Incremental Static Regeneration) |
| :--- | :--- | :--- | :--- | :--- |
| **Full Name** | Client-Side Rendering | Server-Side Rendering | Static Site Generation | Incremental Static Regeneration |
| **HTML 생성 시점** | 런타임 (브라우저) | 런타임 (서버) | 빌드 타임 (Build time) | 런타임 (요청 후 백그라운드) |
| **초기 로딩 속도** | 느림 (JS 다운로드 후 실행) | 빠름 (HTML 즉시 전송) | 가장 빠름 (CDN 전송) | 빠름 (캐시 우선) |
| **SEO 친화성** | 낮음 (크롤러 빈 문서 수집) | 높음 (완성된 문서 수집) | 최상 (완전 정적) | 높음 (재생성 주기 존재) |
| **서버 부하** | 낮음 (정적 리소스 only) | 높음 (매 요청 시 렌더링) | 없음 (빌드 시 1회) | 중간 (재생성 트리거 시) |
| **데이터 갱신** | 실시간 가능 | 실시간 가능 | 재빌드 필요 | TTL(생명주기) 기반 자동 갱신 |
| **대표 프레임워크** | React (SPA Mode) | Next.js, Nuxt.js | Gatsby, Hugo, Jekyll | Next.js (ISR) |

**2. 상세 아키텍처 다이어그램**
아래 다이어그램은 사용자 요청이 들어왔을 때 각 전략이 HTML을 생성하는 시점과 흐름을 시각화한 것입니다.

```ascii
[ A. CSR Architecture (Browser Heavy) ]
[User] ──(Request)──> [Server] ──(Empty HTML + JS)──> [Browser]
                                                    │
                                                    ├─▶ [JS Parse/Execute]
                                                    │      │
                                                    │      ▼
                                                    │   [Data Fetching (API)]
                                                    │      │
                                                    │      ▼
                                                    └─▶ [Render DOM]
                                                           (Very Long TTI)

[ B. SSR Architecture (Server Heavy) ]
[User] ──(Request)──> [Server (Node.js)] ──▶ [Data Fetching]
                           │                    │
                           ▼                    ▼
                     [Render HTML]         [Database]
                           │
                           ▼
                 [Fully Formed HTML] ──▶ [Browser]
                                          │
                                          ▼
                                  [View Content + Hydrate]
                                  (Fast LCP, Interactivity later)

[ C. SSG/ISR Architecture (Build & Edge) ]
[Build Time]              [Request Time]
   │                          │
   ▼                          ▼
[Data] ─▶ [Gen HTML] ─▶ [CDN Cache] ◀─(Hit)── [User]
   │          │              │
   │          │              └─▶ [User] (Stale)
   │          │                     │
   │          │                     ▼
   │          │              [Background Revalidate]
   │          │                     │
   │          ▼                     ▼
   └─ [ISR Trigger] ─▶ [Update Cache] ──(Next Request)──▶ [User]
```

**3. 심층 동작 원리**
- **CSR의 렌더링 흐름**: 서버는 `<div id="root"></div>`만 반환. 브라우저는 JS 번들을 다운로드하고 파싱한 후, **Virtual DOM**을 생성하고 실제 DOM과 비교하여 화면을 그립니다. 문제는 JS가 로딩되기 전까지 화면이 비어있어 사용자가 이탈할 가능성이 높습니다.
- **SSR의 Hydration (수화)**: 서버가 완성된 HTML을 보내면 사용자는 즉시 콘텐츠를 봅니다. 이후 브라우저에서 JS가 로드되면 기존 HTML에 이벤트 리스너를 붙이는 **Hydration** 과정이 일어납니다. 이는 '정적 HTML'을 '동적 앱'으로 만드는 과정입니다.
- **ISR의 갱신 로직**: 사용자가 요청하면 CDN은 먼저 캐시된 페이지를 반환합니다(Stale-While-Revalidate). 동시에 서버는 백그라운드에서 페이지를 다시 생성하여 캐시를 갱신합니다. 다음 사용자부터는 갱신된 페이지를 받습니다. 이는 일관된 성능(Cache HIT)과 데이터 최신화 사이의 균형을 제공합니다.

**4. 핵심 코드 예시 (ISR Logic)**
```javascript
// Next.js의 getStaticProps를 활용한 ISR 구현 예시
// TTL(Time To Live)을 설정하여 재생성 주기를 제어합니다.
export async function getStaticProps() {
  // 1. 데이터 소스(API, DB)에서 정보 조회
  const data = await fetch('https://api.example.com/posts').then(res => res.json());

  return {
    props: {
      posts: data,
    },
    // 2. revalidate: 초 단위. 10초마다 백그라운드에서 재생성 시도
    // - 사용자는 항상 캐시된 페이지를 즉시 받음
    // - 10초가 지나면 다음 요청부터 새로운 페이지 생성
    revalidate: 10, 
  };
}
```

**5. 💡 섹션 요약 비유**
마치 복잡한 고속도로 톨게이트에서 **하이패스 차선(SSG/ISR)**을 별도로 운영하여 병목을 해결하는 것과 같습니다. 일반 차량(CSR)은 매번 정지해야 하지만, 하이패스 차선은 이미 등록된 정보(캐시)를 통해 통행료를 결제(렌더링)하여 멈추지 않고 통과합니다. ISR은 통과 후 백그랜드에서 시스템이 자동으로 정산 내역을 갱신해주는 스마트 시스템과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: FCP vs TTI**
렌더링 전략은 **FCP (First Contentful Paint)**와 **TTI (Time to Interactive)** 두 지표의 상충 관계를 어떻게 해결하느냐에 달려 있습니다.

| 지표 | CSR (Problem) | SSR (Balanced) | SSG/ISR (Optimal) | 비고 |
|:---|:---|:---|:---|:---|
| **FCP (콘텐츠 표시)** | 느림 (JS 로딩 대기) | 빠름 | 즉시 | SEO 및 사용자 경험 직결 |
| **TTI (상호작용 가능)** | 느림 (Hydration 없음) | 중간 (Hydration 필요) | 빠름 (JS 경량화) | 앱 반응성 지표 |
| **TTFB (첫 바이트 수신)** | 빠름 | 느림 (서버 처리) | 매우 빠름 (CDN) | 서버/네트워크 성능 |

**2. PWA (Progressive Web App)와의 융합**
PWA는 단순한 렌더링 전략을 넘어 웹의 **'기능적 완결성'**을 높이는 기술 집합입니다.

| 핵심 요소 | 역할 및 기술 | 연관 기술 스택 |
|:---|:---|:---|
| **Service Worker** | 브라우저 백그라운드에서 네트워크 요청을 가로채고 캐싱하여 **오프라인 접근성**을 부여함. 자바스크립트 파일 내에 작성되는 별도의 스레드. | Cache API, Push API |
| **Web App Manifest** | 앱의 메타데이터(아이콘, 색상, 시작 화면 등)를 정의하여 '앱 설치' 경험을 제공. JSON 형식. | Link tag, Add to Home Screen |
| **HTTPS** | Service Worker는 보안 컨텍스트(HTTPS)에서만 작동하므로 보안 인증서가 필수. | TLS/SSL, PKI |

**3. WebAssembly (WASM)와의 융합**
WASM은 C++, Rust 등으로 작성된 코드를 브라우저에서 네이티브 속도로 실행하게 하는 바이너리 명령어 형식입니다.

- **CSP (Content Security Policy)** 관점: 일반적인 `eval()`이나 인라인 스크립트가 제한되는 환경에서도, WASM은 샌드박스 내에서 안전하게 고성능 연산을 수행할 수 있어 보안과 성능의 두 마리 토끼를 잡습니다.
- **Web Worker & WASM**: 메인 스레드를 차단하지 않고 무거운 연산(이미지 처리, 암호화, AI 추론)을 수행하기 위해 Web Worker 내에서 WASM을 실행하는 패턴이 표준으로 자리 잡고 있습니다.

```ascii
[PWA & WASM Integration]
    [Browser Main Thread]
           │
           ├─▶ [UI Rendering] (React/Vue)
           │
           └─▶ [Service Worker] (Network Control)
                  │
                  ├─▶ [Cache Storage] (Offline Assets)
                  │
                  └─▶ [Web Worker + WASM]
                         │
                         ▼
                   [Heavy Computation]
                   (Video Encoding / AI Model)
```

**4. 💡 섹션 요약 비유**
PWA는 **'오프라인 지도 앱'**과 같습니다. 지하철이나 터널(네트워크 단절)에 들어가도 미리 다운로드(캐싱)된 지도를 볼 수 있고, 위치를 추적할 수 있습니다. WebAssembly는 **'브라우저라는 여행 가방 안에 넣은 초소형 전동 공구 세트'**와 같습니다. 평소에는 가볍게 다니지만, 무거운 작업(연산)이 필요할 때 꺼내면 앱(App)만큼 강력한 힘을 발휘합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오별 의사결정 (Decision Matrix)**

| 시나리오 | 추천 전략 | 이유 및 고려사항 |
|:---|:---|:---|
| **대규모 이커머스 상세 페이지** | **ISR** | 상품 정보는 수시로 변하지만(재고, 가격), 트래픽이 폭주합니다. SSR로 인한 서버 과부하를 막고, SSG로 인한 정보 부재를 막기 위해 TTL(예: 30초) 기반 ISR이 최적입니다. |
| **기업 블로그 / 문서 사이트** | **SSG** | 콘텐츠가 생성될 때만 변화하므로 빌드 시 HTML을 미리 만들어 CDN에 배포하는 것이 비용/성능 면에서 가장 효율적입니다. |
| **실시간 대시보드 (SaaS)** | **CSR + SWR** | 데이터가 초 단위로 변하고 실시간 상호작용이 중요합니다. 빈 화면을 방지하기 위해 Skeleton UI를 사용하고, SWR(Stale-While-Revalidate)로 데이터를 갱신합