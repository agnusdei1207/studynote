---
title: "Micro Frontends Deployment"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 111
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이크로 프론트엔드(Micro Frontends)는 모놀리식 프론트엔드 앱을 <strong>비즈니스 도메인별로 독립 개발·배포·운영 가능한 단위</strong>로 분해하여, 백엔드 MSA의 원칙을 프론트엔드에 적용한 아키텍처다.
> 2. **가치**: 팀 A가 "검색" 마이크로 FE를, 팀 B가 "결제" 마이크로 FE를 <strong>서로 다른 릴리즈 주기·기술 스택</strong>으로 독립 배포할 수 있어, 대규모 조직의 <strong>프론트엔드 배포 병목을 해소</strong>한다.
> 3. **판단 포인트**: Webpack Module Federation·Single-SPA·iframe 등 통합 방식의 트레이드오프를 이해하고, <strong>공유 디자인 시스템(Design System)과 라우팅 규약</strong>으로 UX 일관성을 보장해야 한다.

---

## Ⅰ. 개요 및 필요성

백엔드는 MSA로 서비스별 독립 배포가 가능하지만, 프론트엔드는 여전히 하나의 거대 SPA(Single Page App)로 묶여있는 경우가 많다. 10개 팀이 1개 프론트엔드 repo에서 코드를 수정하면 <strong>머지 충돌·빌드 시간 폭발·배포 큐 대기</strong>가 발생한다.

```text
+-------------------------------------------------------+
|    모놀리식 FE vs 마이크로 프론트엔드                   |
+-------------------------------------------------------+
|  [모놀리식 FE]                                        |
|   10팀 -> 1개 Repo -> 1개 빌드 -> 1개 배포              |
|   -> 머지 충돌, 빌드 30분, 배포 큐 대기                |
|                                                       |
|  [마이크로 FE]                                        |
|   팀 A: 검색 FE -> 독립 Repo -> 독립 배포              |
|   팀 B: 결제 FE -> 독립 Repo -> 독립 배포              |
|   팀 C: 상품 FE -> 독립 Repo -> 독립 배포              |
|         v          v          v                       |
|   Shell App (호스트)가 런타임에 합체                   |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 모놀리식 FE는 10명이 1개 도화지에 동시에 그림을 그리는 것이고, 마이크로 FE는 각자 캔버스에 그린 후 전시회(Shell App)에서 합치는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 통합 방식 비교

| 방식 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| <strong>Module Federation</strong> | Webpack 5 런타임 모듈 공유 | 코드 공유 효율, JS 네이티브 | Webpack 종속 |
| **Single-SPA** | 각 FE를 독립 앱으로 등록, 라우팅 기반 전환 | 프레임워크 혼용 가능 | 러닝 커브 |
| **iframe** | 페이지 내 독립 프레임 | 완벽 격리 | SEO 불리, UX 불연속 |
| **Web Components** | Custom Elements + Shadow DOM | 표준 기반 | 생태계 미성숙 |

### Module Federation 핵심
Host(Shell) 앱이 빌드 시점이 아닌 **런타임에** Remote 앱의 JS 번들을 동적으로 로드한다. Remote 앱은 독립적으로 빌드·배포되며, Host는 Remote의 최신 버전을 자동으로 반영한다.

- **📢 섹션 요약 비유**: Module Federation은 레고 본체(Host)에 블록(Remote)을 끼워 넣는 것이다. 블록은 별도 공장에서 만들고, 본체는 어떤 블록이든 규격만 맞으면 끼운다.

---

## Ⅲ. 비교 및 연결

| 비교 | 모놀리식 FE | 마이크로 FE |
|:---|:---|:---|
| **배포 단위** | 전체 앱 | 도메인별 독립 |
| **팀 자율성** | 낮음 (공유 repo) | **높음 (독립 repo)** |
| <strong>기술 스택</strong> | 통일 필수 | 혼용 가능 |
| <strong>초기 복잡도</strong> | 낮음 | 높음 (인프라 구성) |
| **적합 조직** | 소규모 (1~3팀) | **대규모 (5팀+)** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 성공 조건
1. **공유 디자인 시스템**: 각 FE가 같은 버튼·색상·타이포를 사용하여 UX 일관성 보장.
2. <strong>라우팅 규약</strong>: `/search/*`는 검색 FE, `/checkout/*`는 결제 FE처럼 경로 기반 분배.
3. <strong>버전 관리</strong>: 공유 라이브러리 breaking change 시 Semantic Versioning 엄수.

### 안티패턴
- **3팀 미만에서 마이크로 FE 도입**: 인프라 복잡도만 증가하고 배포 병목이 없음 -> 모놀리식 유지가 효율적.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 모놀리식 FE | 마이크로 FE | 개선 |
|:---|:---|:---|:---|
| 배포 빈도 | 주 1회 (큐 대기) | **일 수회 (팀별 독립)** | 5x |
| 빌드 시간 | 30분 (전체) | <strong>3분 (도메인별)</strong> | 90% 단축 |
| 팀 자율성 | 머지 충돌 빈발 | **완전 독립** | 생산성 향상 |

마이크로 프론트엔드는 <strong>Next.js Zones·Vite Federation</strong>과 결합하여 SSR(Server-Side Rendering) 환경에서도 독립 배포가 가능한 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>MSA (Microservices)</strong> | 백엔드 독립 배포 -> 프론트엔드로 확장 |
| <strong>Module Federation</strong> | Webpack 5 런타임 모듈 공유 기술 |
| **Single-SPA** | 프레임워크 혼용 마이크로 FE 오케스트레이터 |
| **Design System** | UX 일관성을 보장하는 공유 컴포넌트 라이브러리 |
| <strong>BFF (Backend for Frontend)</strong> | 마이크로 FE별 전용 API 게이트웨이 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
[모놀리식 SPA (2010s) — React/Angular 단일 앱]
    |
    v
[iframe 기반 분리 (초기) — 완벽 격리, 나쁜 UX]
    |
    v
[Single-SPA (2018~) — 라우팅 기반 FE 오케스트레이션]
    |
    v
[Webpack Module Federation (2020) — 런타임 코드 공유]
    |
    v
[현재: Vite Federation + SSR — 차세대 마이크로 FE 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 10명이 <strong>1개 도화지</strong>에 동시에 그림을 그려서 서로 부딪혔어요.
2. 마이크로 프론트엔드는 각자 <strong>자기 캔버스</strong>에 그린 후 전시회에서 합치는 거예요.
3. 덕분에 한 친구가 그림을 수정해도 **다른 친구 그림은 안 망가지고**, 전시회도 훨씬 빨리 열 수 있답니다!
