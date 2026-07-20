---
title: "Msa Microservices Architecture"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 122
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MSA는 <strong>애플리케이션을 비즈니스 도메인 단위의 독립 서비스로 분리</strong>하여, 각 서비스가 <strong>자체 DB·코드베이스·배포 파이프라인</strong>을 가지고 독립적으로 개발·배포·스케일링되는 아키텍처다.
> 2. **가치**: 모놀리식에서는 주문 기능 수정이 전체 재배포를 요구하지만, MSA에서는 <strong>주문 서비스만 독립 배포</strong>하므로 배포 빈도^·장애 격리^·팀 자율성^이 가능하다.
> 3. **판단 포인트**: MSA의 <strong>분산 시스템 복잡도(서비스 디스커버리·분산 트랜잭션·관측성)</strong>를 관리할 역량이 없으면 오히려 모놀리식보다 비효율적이며, <strong>Conway's Law에 따라 팀 구조를 먼저 분리</strong>해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    MSA 아키텍처                                       |
+-------------------------------------------------------+
|  [API Gateway]                                        |
|     +--> 주문 서비스 (Order) -- DB_Order              |
|     +--> 결제 서비스 (Payment) -- DB_Payment          |
|     +--> 재고 서비스 (Inventory) -- DB_Inventory      |
|     +--> 사용자 서비스 (User) -- DB_User              |
|                                                       |
|  각 서비스: 독립 배포·스케일링·기술 스택 자유        |
|  서비스 간 통신: REST / gRPC / 이벤트(Kafka)         |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 모놀리식은 대형 백화점(모든 매장이 한 건물)이고, MSA는 쇼핑몰(각 매장이 독립 건물, 독립 운영)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MSA 핵심 패턴

| 패턴 | 설명 |
|:---|:---|
| <strong>API Gateway</strong> | 외부 요청의 단일 진입점 |
| <strong>Service Discovery</strong> | 서비스 위치 동적 탐색 |
| <strong>Circuit Breaker</strong> | 장애 서비스 호출 차단 |
| <strong>Saga</strong> | 분산 트랜잭션 (보상 트랜잭션) |
| <strong>CQRS</strong> | 읽기/쓰기 모델 분리 |

- **📢 섹션 요약 비유**: Circuit Breaker는 전기 차단기다. 한 서비스(콘센트)가 합선되면 해당 라인만 차단하여 전체 정전(장애 전파)을 방지한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 모놀리식 | MSA |
|:---|:---|:---|
| **배포** | 전체 | <strong>서비스별</strong> |
| **장애** | 전파 | **격리** |
| **복잡도** | 낮음 | <strong>높음 (분산)</strong> |
| **팀** | 기능별 | <strong>서비스별 (풀스택)</strong> |

---

## Ⅳ. 실무 적용 및 실무자 판단

### MSA 도입 판단
- ✅ 팀 5+, 도메인 복잡, 배포 빈도 높음 -> MSA.
- ❌ 팀 소규모, 초기 스타트업 -> Monolith First.

---

## Ⅴ. 기대효과 및 결론

MSA는 <strong>대규모 조직의 빠른 배포·독립 스케일링</strong>을 가능하게 하지만, 분산 시스템 복잡도를 관리할 <strong>플랫폼 엔지니어링 역량</strong>이 전제 조건이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>API Gateway</strong> | MSA의 단일 진입점 |
| <strong>Saga</strong> | 분산 트랜잭션 패턴 |
| <strong>Service Mesh</strong> | 서비스 간 통신 인프라 (Istio) |
| <strong>DDD</strong> | 서비스 경계 설계 (Bounded Context) |
| **Conway's Law** | 팀 구조 = 시스템 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
[모놀리식 (전통)]
    |
    v
[SOA (2005~) — 서비스 지향, ESB 중심]
    |
    v
[MSA (2014, Netflix·Amazon) — 경량 서비스 분리]
    |
    v
[Service Mesh (Istio, 2018~) — 통신 인프라 표준화]
    |
    v
[현재: Modular Monolith + MSA — 상황별 최적 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 모놀리식은 모든 가게가 <strong>한 건물에 있는 백화점</strong>이에요. 한 곳 수리하면 전체가 불편해요.
2. MSA는 가게마다 <strong>독립 건물인 쇼핑몰</strong>이에요. 한 가게만 수리해도 다른 가게는 정상 영업!
3. 하지만 가게가 너무 많으면 **관리가 복잡해지니까** 적당한 규모가 중요해요!
