+++
title = "682. 마이크로 프론트엔드 웹팩 연계"
date = "2026-03-15"
weight = 682
[extra]
categories = ["Software Engineering"]
tags = ["Micro Frontends", "Module Federation", "Webpack", "Frontend Architecture", "Distributed Systems"]
+++

# 682. 마이크로 프론트엔드 웹팩 연계

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MSA (Microservices Architecture)의 철학을 프론트엔드로 확장한 아키텍처로, 단일 SPA (Single Page Application)의 복잡도를 분리하여 **독립적 배포 가능한 단위(Micro-apps)**로 구성하는 '분산형 프론트엔드' 패러다임이다.
> 2. **기술적 핵심**: Webpack 5의 **Module Federation (모듈 페더레이션)** 플러그인을 통해 빌드 타임 종속성을 제거하고, 런타임에 여러 독립된 빌드(Build) 간에 코드를 동적으로 로드 및 공유한다.
> 3. **가치**: 조직 간 기술 스택(Heterogeneous Tech Stack)의 자율성을 확보하며, 부분적인 배포(TTB: Time to Build)와 독립적인 확장성(Scalability)을 통해 대규모 웹 시스템의 복잡도를 제어한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**마이크로 프론트엔드 (Micro Frontends)**는 "하나의 앱을 누군가가 끝까지 책임지는(monolithic) 대신, 비즈니스 도메인별로 분리된 작은 앱들이 조합되어 하나의 사용자 경험을 제공하는" 아키텍처 스타일입니다. 이는 단순한 UI 컴포넌트 분리를 넘어, 빌드 시스템, 배포 파이프라인, 그리고 팀 조직 구조까지 포함하는 시스템적 접근 방식입니다.

#### 2. 등장 배경과 진화 과정
① **기존 한계**: 프론트엔드 규모가 거대해짐에 따라 발생하는 '거대한 SPA 문제'. 한 줄의 코드 수정을 위해 전체 코드를 다시 빌드하고 배포해야 하는 **CI/CD 파이프라인의 병목**과 팀 간 충돌(Conflict)이 발생했습니다.
② **혁신적 패러다임**: 백엔드의 **MSA (Microservices Architecture)** 성공 사례를 프론트엔드에 적용하고자 하는 시도가 시작되었습니다. 초기에는 `iframe`이나 `Web Components`가 사용되었으나, 2020년 Webpack 5가 발표하며 **Module Federation**이라는 강력한 표준이 등장했습니다.
③ **현재의 비즈니스 요구**: 금융, 이커머스 등 대규모 플랫폼은 '팀당 도메인(Team per Domain)' 구조를 요구하며, 각 팀이 React, Vue, Angular 등 서로 다른 프레임워크를 사용하면서도 하나의 페이지에서 조화롭게 작동해야 하는 요구가 증가했습니다.

#### 3. 💡 비유: 쇼핑몰 입점 구조
"백화점이 쇼핑몰의 진열장(브라우저 화면)을 제공하고, 각 브랜드(마이크로 앱)가 자신의 상품을 자유롭게 진열하고 교체하는 구조와 같습니다. 백화점(Shell)은 각 브랜드가 무엇을 팔고 있는지 알 필요 없이, 단지 지정된 공간만 할당하면 됩니다."

#### 📢 섹션 요약 비유
**"마이크로 프론트엔드는 거대한 완조 립(Pre-fabricated) 건물을 짓는 게 아니라, 각자의 공장에서 찍어낸 방을 현장에서 끼워 맞춰 조립하는 '모듈러 주택 건축' 방식과 같습니다."**

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 기술적 용어 및 정의
- **Module Federation (모듈 페더레이션)**: Webpack 5에 내장된 기능으로, 여러 개의 별도 빌드가 서로의 코드를 런타임에 동적으로 로드할 수 있게 해주는 메커니즘입니다.
- **Host (호스트)**: 일반적으로 애플리케이션의 셸(Shell)이나 메인 페이지로, 다른 Remote 앱을 참조하여 화면에 렌더링하는 컨테이너입니다.
- **Remote (리모트)**: Host에 로드되어 기능을 제공하는 독립적인 애플리케이션입니다.
- **Shared (공유 의존성)**: Host와 Remote 간에 중복 로드를 방지하기 위해 공유되는 라이브러리(예: React, ReactDOM, Lodash)입니다.

#### 2. 구성 요소 (상세 분석)

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/포맷 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **Container (Shell)** | 전체 앱의 레이아웃 및 라우팅 관리 | 브라우저 URL 변경 감지 → 해당 Remote 진입점(entry) 로드 | HTML5 History API | **아파트 건물 골조** |
| **Module Federation Plugin** | 빌드 시점에 의존성 주입 설정 | `remotes` 옵션을 통해 원격 진입점 URL(`remoteEntry.js`)을 명시 | JavaScript (ESM) | **화물 연결 컨테이너** |
| **remoteEntry.js** | Remote 앱의 Manifest 파일 | 해당 Remote가 노출(Expose)하는 모듈 목록과 Shared 설정 정보를 포함 | JSON/JS Object | **도서관 목록(카드 목록)** |
| **Shared Scope** | 라이브러리 버전 충돌 방지 | 런타임에 라이브러리 버전을 협상하여 단일 인스턴스(Singleton) 보장 | SemVer 비교 로직 | **공공 자전거 시스템** |

#### 3. 아키텍처 다이어그램 (Module Federation 동작 구조)
아래는 Host가 Remote 앱의 버튼 컴포넌트를 런타임에 가져와 렌더링하는 데이터 흐름입니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           [ BROWSER - CLIENT SIDE ]                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [ HOST APP (React Shell) ]                                                │
│  │   ├── import Button from 'checkout/Button';                             │
│  │   └── Webpack Runtime: "Is 'Button' loaded?"                            │
│  │          └── NO! -> Request Remote Entry                                │
│  │                                                                               │
│  ┌──────────────────────┐  ① HTTP GET /remoteEntry.js                  │
│  │  Webpack Runtime     │ <──────────────────────────────────────────┐    │
│  │  Container System    │                                           │    │
│  └──────────────────────┘                                           │    │
│          │                                                         │    │
│          │  ② Load 'Button' Module (Async)                         │    │
│          │ <───────────────────────────────────────────────────────┘    │
│          ▼                                                               │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │           [ SHARED SCOPE (Global Cache) ]                         │   │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐                        │   │
│  │  │ React   │  │ Lodash  │  │ Axios     │  (Check Version)       │   │
│  │  │ v18.x   │  │ v4.x    │  │ v1.x      │  -> Use Existing       │   │
│  │  └─────────┘  └─────────┘  └───────────┘                        │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ DISTRIBUTED NETWORK ]                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [ Remote Server A: Checkout ]          [ Remote Server B: Product ]     │
│  URL: https://checkout.com/             URL: https://product.com/         │
│  ┌──────────────────────┐              ┌──────────────────────┐          │
│  │  remoteEntry.js      │              │  remoteEntry.js      │          │
│  │  - Exposes: Button   │              │  - Exposes: Card     │          │
│  │  - Shared: React     │              │  - Shared: Vue       │          │
│  └──────────────────────┘              └──────────────────────┘          │
│       ▲                                      ▲                            │
│       └── Independent Deploy (CI/CD) ─────────┘                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[해설]**
1. **① Entry 로드**: Host 앱은 처음 `remoteEntry.js`만 로드합니다. 이 파일은 매우 가볍고 다운로드 속도가 빠릅니다.
2. **② 모듈 로드**: 사용자가 실제로 버튼이 필요한 화면으로 진입할 때, Webpack 런타임은 Remote 서버에 실제 코드(Chunk)를 요청합니다.
3. **Shared Scope**: Remote 앱에서 필요한 React 라이브러리가 Host 이미 메모리에 로드되어 있다면, Remote는 Host의 React를 재사용합니다(중복 다운로드 방지).

#### 4. 핵심 소스 코드 설정 (Webpack Config)

```javascript
// webpack.config.js (Host 측 설정)
const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");

module.exports = {
  // ...
  plugins: [
    new ModuleFederationPlugin({
      name: "host_app", // 전역 변수명 (window.host_app)
      remotes: {
        // "키": "이름@URL"
        checkout: "checkout_app@https://checkout.com/remoteEntry.js",
      },
      shared: {
        react: { singleton: true, requiredVersion: "^18.0.0" }, // 단일 인스턴스 강제
        "react-dom": { singleton: true, requiredVersion: "^18.0.0" },
      },
    }),
  ],
};
```

#### 📢 섹션 요약 비유
**"마치 '플러그인(Part-based)' 프로그래밍입니다. 메인 프로그램(Host)은 소켓만 정의하고, 실제 기능(Plugin)은 나중에 다운로드된 파일(Remote)에서 실행되는 방식이므로, 프로그램을 껐다 켜지 않아도 기능을 교체할 수 있습니다."**

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: IFrame vs Module Federation
마이크로 프론트엔드를 구현하는 여러 방식 중 기존 IFrame과 새로운 Module Federation을 비교 분석합니다.

| 비교 항목 | IFrame 방식 | Module Federation (MF) 방식 |
|:---:|:---|:---|
| **격리성 (Isolation)** | **완전 격리** (CSS, JS 전용 컨텍스트) | **논리적 격리** (Browser 컨텍스트 공유) |
| **네트워크 성능** | 각자 리소스를 중복 로드 (Connect/Handshake 비용 높음) | **资源共享 최적화** (Shared Scope로 중복 최소화) |
| **UX/UI 통합** | 부자연스러움 (Scroll 경계, Drag & Drop 제한) | **Native 앱과 유사** (단일 DOM 트리) |
| **데이터 통신** | `postMessage` API (비동기 메시징, 직렬화 필요) | **직접 참조** (Function 호출, Props 전달 가능) |
| **SEO (Search Engine)** | 내용 수집 어려움 (Robot 입장에서 별도 페이지) | **친화적** (SSR(Server-Side Rendering)과 연계 용이) |

#### 2. 과목 융합 관점
1. **운영체제(OS)와의 시너지**: Dynamic Import는 OS의 **Dynamic Linking (동적 연결)** 개념과 유사합니다. OS가 실행 시점에 `.dll`이나 `.so` 파일을 로드하여 메모리에 링크하듯, Webpack도 런타임에 모듈을 연결합니다.
2. **DB/데이터 분석**: **RDBMS (Relational Database)**의 정규화와 반대로, UI는 의도적으로 **비정규화(Denormalization)** 형태인 마이크로 앱으로 쪼갭니다. 하지만 상태 관리(Global State)는 중앙집중형(예: Redux, Zustand) 패턴과 분산형(Pub/Sub) 패턴의 선택 기로에 놓이게 됩니다.

#### 📢 섹션 요약 비유
**"IFrame은 각 팀이 완전히 밀폐된 '방'에서 일하다가 문을 통해 서류만 넘겨주는 것과 같지만, Module Federation은 하나의 거대한 사무실(Open Office)에서 파티션만 치고 일하는 것과 같습니다. 소통은 자유로우지만 '공간(CSS 변수)'이나 '공유프로그램(Library)' 사용 규칙을 엄격히 지켜야 충돌이 나지 않습니다."**

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 대형 이커머스 플랫폼 전환
- **문제 상황**: '마이페이지'는 5년 된 Angular 앱이고, 신규 '상품 목록'은 React 18로 개발 중입니다. 이를 하나의 페이지에 통합해야 하며, '마이페이지' 팀은 2주마다 배포를, '상품 목록' 팀은 하루에 여러 번 배포를 해야 합니다.
- **의사결정 과정**:
    1. **기술적 타당성**: Module Federation을 사용하여 Angular(Remote)와 React(Host)를 통합 가능한지 확인 (Webpack Module Federation은 Angular의 `angular.json` 설정이 가능함).
    2. **전략적 수립**: **Shell 앱(Host)**을 최소화(단순 라우터 역할)하고, 각 도메인을 Remote로 분리.
    3. **버전 관리 전략**: `react-dom` 같은 필수 라이브러리는 `singleton: true`로 설정하여 전체 앱에서 단 하나의 인스턴스만 실행되도록 강제.
- **결과**: 팀 간 배포 주기가 Decoupling되어, 한 팀의 배포 실패가 전체 서비스 다운타임으로 이어지지 않음.

#### 2. 도입 체크리스트 (운영 및 보안)
- **[기술적]**
    - [ ] 공통 UI 시스템(Design System)을 별도의 패키지로 분리하여 관리하고 있는가?
    - [ ] 각 앱 간의 통신(Routing, State) 프로토콜이 명확히 정의되었는가?
- **[운영/보안]**
    - [ ] **CORS (Cross-Origin Resource Sharing)** 및 **CSP (Content Security Policy)** 설정이 외부 Remote 접근을 허용하도록 안전하게 구성되었는가?
    - [ ] 의존성 공급망(Supply Chain) 공격 방지를 위해 `