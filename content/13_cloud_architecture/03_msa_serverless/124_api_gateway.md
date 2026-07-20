---
title: "Api Gateway"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 124
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: API Gateway는 <strong>MSA에서 모든 외부 요청의 단일 진입점(Single Entry Point)</strong>이며, 요청 라우팅·인증·Rate Limiting·로깅·응답 캐시를 수행하는 <strong>리버스 프록시 + 크로스커팅 관심사 처리기</strong>이다.
> 2. **가치**: 클라이언트가 수십 개 마이크로서비스의 엔드포인트를 직접 알면 <strong>서비스 URL 변경·인증 중복·CORS 관리</strong>가 불가능하지만, Gateway를 통해 <strong>단일 URL(api.example.com)로 모든 서비스에 접근</strong>할 수 있다.
> 3. **판단 포인트**: <strong>BFF(Backend For Frontend)</strong> 패턴과 결합하면 클라이언트별(Web/Mobile) 최적화된 API를 제공할 수 있으며, Kong·Envoy·AWS API Gateway가 대표 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    API Gateway 아키텍처                               |
+-------------------------------------------------------+
|  [Client] -> api.example.com                           |
|                |                                      |
|           [API Gateway]                               |
|            +-- 인증 (JWT 검증)                        |
|            +-- Rate Limiting (100 req/s)              |
|            +-- 라우팅 (/orders -> Order Service)      |
|            +-- 로깅·모니터링                          |
|            +-- 응답 캐시                              |
|                |                                      |
|    +-----------+-----------+                          |
|    v           v           v                          |
|  Order Svc  Payment Svc  User Svc                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: API Gateway는 호텔 프런트 데스크다. 모든 손님(요청)이 프런트(Gateway)를 거치며, 프런트가 신분 확인(인증)·방 배정(라우팅)·보안(Rate Limiting)을 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### API Gateway 핵심 기능

| 기능 | 설명 |
|:---|:---|
| <strong>라우팅</strong> | URL 패턴 -> 서비스 매핑 |
| <strong>인증</strong> | JWT/OAuth2 검증 |
| <strong>Rate Limiting</strong> | 과도한 요청 차단 |
| <strong>로드 밸런싱</strong> | 서비스 인스턴스 분배 |
| **응답 캐시** | 반복 요청 캐싱 |

- **📢 섹션 요약 비유**: Gateway는 공항의 보안 검색대 + 게이트 안내이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 직접 호출 | API Gateway |
|:---|:---|:---|
| **진입점** | 서비스마다 다름 | **단일** |
| <strong>인증</strong> | 서비스마다 구현 | **중앙 처리** |
| **CORS** | 복잡 | **Gateway에서 관리** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 대표 도구
- **Kong**: 오픈소스, 플러그인 생태계.
- <strong>Envoy Proxy</strong>: CNCF, 서비스 메시 데이터 플레인.
- <strong>AWS API Gateway</strong>: 관리형, Lambda 연동.

---

## Ⅴ. 기대효과 및 결론

API Gateway는 <strong>MSA의 필수 인프라</strong>이며, BFF·서비스 메시와 결합하여 현대 클라우드 네이티브 아키텍처의 통신 허브 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>API Gateway</strong> | MSA 단일 진입점 |
| <strong>BFF</strong> | 클라이언트별 맞춤 API |
| <strong>Rate Limiting</strong> | 과부하 방지 |
| <strong>Service Mesh</strong> | 서비스 간 통신 인프라 (보완 관계) |
| **Kong/Envoy** | 대표 API Gateway 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[로드 밸런서 (L4/L7, 2000s)]
    |
    v
[API Gateway (Netflix Zuul, 2013~)]
    |
    v
[Kong / Envoy (2015~) — 클라우드 네이티브 Gateway]
    |
    v
[BFF Pattern (2016~) — 클라이언트별 Gateway]
    |
    v
[현재: API Gateway + Service Mesh — 통합 네트워크 계층]
```

### 👶 어린이를 위한 3줄 비유 설명
1. API Gateway는 호텔 <strong>프런트 데스크</strong>예요. 모든 손님이 프런트를 거쳐요.
2. 프런트에서 <strong>신분증 확인(인증)</strong>하고, 너무 많은 손님이 오면 <strong>대기(Rate Limiting)</strong>시켜요.
3. 프런트가 없으면 손님이 **직접 방을 찾아야 해서** 혼란스러워요!
