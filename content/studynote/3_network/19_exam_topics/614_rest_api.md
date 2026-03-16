+++
title = "REST API (Representational State Transfer) - REST API"
weight = 614
+++

# REST API (Representational State Transfer) - REST API

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리소스 기반 웹 아키텍처
> 2. **가치**: 무상태, 표준 HTTP
> 3. **융합:** HTTP Methods, JSON, URL

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

REST는 리소스를 HTTP로 표현하는 아키텍처입니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REST API                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              REST 원칙                                         │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  1. Client-Server: 관심사 분리                        │   │ │
│   │   │  2. Stateless: 상태 없음                              │   │ │
│   │   │  3. Cacheable: 캐시 가능                              │   │ │
│   │   │  4. Uniform Interface: 통일된 인터페이스              │   │ │
│   │   │  5. Layered System: 계층화                            │   │ │
│   │   │                                                      │   │ │
│   │   │  리소스 표현:                                         │   │ │
│   │   │  GET    /users          → 사용자 목록                 │   │ │
│   │   │  GET    /users/1        → 사용자 1 조회               │   │ │
│   │   │  POST   /users          → 사용자 생성                 │   │ │
│   │   │  PUT    /users/1        → 사용자 1 전체 수정          │   │ │
│   │   │  DELETE /users/1        → 사용자 1 삭제               │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: REST는 리소스를 URL로, 동작을 HTTP Method로 표현합니다.

**📢 섹션 요약 비유:** REST API = 리소스 주소!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Resource** | URI로 식별 |
| **Representation** | JSON/XML |
| **Method** | HTTP Verb |
| **Stateless** | 상태 없음 |

**핵심 알고리즸:** URI → Method → 처리 → Representation

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**REST vs GraphQL vs gRPC**

| 항목 | REST | GraphQL | gRPC |
|:---|:---|:---|:---|
| **유연성** | 중간 | 높음 | 낮음 |
| **성능** | 중간 | 중간 | 높음 |
| **학습** | 쉬움 | 중간 | 어려움 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 공개 API → REST
**시나리오 2:** 내부 서비스 → gRPC
**시나리오 3:** 복잡한 쿼리 → GraphQL

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** Roy Fielding 논문

---

### 📌 관련 개념 링크**:
- [HTTP](./556_http.md)
- [HTTP Methods](./558_http_methods.md)
- [JSON](./617_json.md)
