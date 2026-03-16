+++
title = "Service Discovery - 서비스 디스커버리"
weight = 772
+++

# Service Discovery - 서비스 디스커버리

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서비스 위치 자동 발견
> 2. **가치**: 동적 환경 지원
> 3. **융합:** Kubernetes, DNS, Load Balancer

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Service Discovery는 서비스 위치를 자동으로 발견합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Service Discovery                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              서비스 디스커버리 패턴                              │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  Client-side Discovery:                              │   │ │
│   │   │  Client ──→ Registry ──→ Service Instance            │   │ │
│   │   │         (조회)        (직접 호출)                      │   │ │
│   │   │                                                      │   │ │
│   │   │  Server-side Discovery:                              │   │ │
│   │   │  Client ──→ Load Balancer ──→ Service Instance       │   │ │
│   │   │         (요청)        (라우팅)                        │   │ │
│   │   │                                                      │   │ │
│   │   │  Service Registry:                                    │   │ │
│   │   │  ┌─────────────────────────────────────────────────┐│   │ │
│   │   │  │ Service Name  │ Address         │ Status       ││   │ │
│   │   │  │ user-service  │ 10.0.1.1:8080  │ UP           ││   │ │
│   │   │  │ user-service  │ 10.0.1.2:8080  │ UP           ││   │ │
│   │   │  │ order-service │ 10.0.2.1:8080  │ UP           ││   │ │
│   │   │  └─────────────────────────────────────────────────┘│   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: Service Discovery는 동적 환경에서 서비스를 찾습니다.

**📢 섹션 요약 비유:** Service Discovery = 전화번호부!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Registry** | 레지스트리 |
| **Registration** | 등록 |
| **Discovery** | 발견 |
| **Health Check** | 상태 확인 |
| **Load Balancing** | 부하 분산 |

**핵심 알고리즸:** 등록 → 발견 → 호출 → 상태 확인

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**Service Registry 도구**

| 도구 | 특징 |
|:---|:---|
| **Consul** | HashiCorp, KV 저장소 |
| **Eureka** | Netflix, AWS |
| **etcd** | CoreOS, Kubernetes |
| **Zookeeper** | Apache, 코디네이션 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** Kubernetes → 내장 Service Discovery
**시나리오 2:** VM 환경 → Consul
**시나리오 3:** 클라우드 → Cloud Map

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** DNS SRV Records

---

### 📌 관련 개념 링크**:
- [Microservices](./617_microservices.md)
- [Load Balancer](./582_load_balancer.md)
- [Kubernetes](./619_kubernetes.md)
