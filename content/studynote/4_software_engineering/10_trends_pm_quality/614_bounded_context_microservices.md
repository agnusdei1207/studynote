+++
title = "614. 바운디드 컨텍스트 마이크로서비스 식별 기준"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 바운디드 컨텍스트 (Bounded Context) 마이크로서비스 식별 기준

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDD의 바운디드 컨텍스트는 도메인 모델의 경계를 명확히 하며, 이를 마이크로서비스의 자연스러운 분리 기준으로 활용
> 2. **가치**: 서비스 간 결합도 최소화, 독립적 배포 가능, 데이터 일관성 경계 명확화 → TTM(Time-to-Market) 30~50% 단축
> 3. **융합**: 컨텍스트 매핑, ACL(Anti-Corruption Layer), Event Carrying Transfer Integration과 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**바운디드 컨텍스트 (Bounded Context)**는 도메인 주도 설계 (DDD, Domain-Driven Design)의 핵심 패턴으로, 특정 도메인 모델이 적용되는 명확한 경계를 의미합니다. 에릭 에반스(Eric Evans)가 정의한 이 개념은 **"같은 용어라도 컨텍스트에 따라 다른 의미를 가질 수 있음"**을 인정하고, 각 컨텍스트 내에서만 유비쿼터스 언어(Ubiquitous Language)가 유효하도록 보장합니다.

**마이크로서비스 아키텍처 (MSA, Microservices Architecture)**에서 바운디드 컨텍스트는 서비스 분리의 가장 중요한 기준이 됩니다. 각 마이크로서비스는 하나 이상의 바운디드 컨텍스트를 구현하며, 이는 **자연스러운 분산 경계**를 제공합니다.

### 💡 비유

대형 쇼핑몰을 생각해보세요. **의류부**, **식품부**, **전자제품부**는 각각 다른 용어와 프로세스를 사용합니다.
- 의류부: "사이즈", "시즌", "컬러"
- 식품부: "유통기한", "보관온도", "원산지"
- 전자제품부: "모델명", "사양", "보증기간"

같은 "재고"라도 부서마다 의미가 다릅니다. 이를 각 부서(컨텍스트)별로 명확히 분리하는 것이 바운디드 컨텍스트입니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 모놀리식** | 전체 시스템이 단일 코드베이스, 용어의 모호함, 변경 영향도 파악 어려움 | **명시적 경계 부재**로 인한 통합 유지보수 비용 폭증 |
| **② 기술적 분리** | 프레젠테이션/비즈니스/데이터 계층 분리만으로는 도메인 복잡도 해결 불가 | **도메인 중심 분리** 필요성 대두 |
| **③ DDD 등장** | 바운디드 컨텍스트로 도메인 경계 명확화, but 모놀리식 구현 | **컨텍스트별 독립 모델**링 가능 |
| **④ MSA 확장** | 바운디드 컨텍스트를 마이크로서비스로 자연스럽게 전환 | **물리적 분리**까지 완성 |

현재의 비즈니스 요구로서는 **클라우드 네이티브 환경에서의 독립적 확장성, 팀별 자율성(CoA, Conways Act), 폴리글롯 프로그래밍** 지원이 필수적입니다.

### 📢 섹션 요약 비유

마치 도시 계획에서 **행정구역(구/군)**을 명확히 구분하는 것과 같습니다. 각 구역마다 독립적인 도시 계획(도메인 모델)을 수립하면서도, 필요에 따라 도로/철도(인터페이스)로 연결하는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 프로토콜/기법 | 비유 |
|:---|:---|:---|:---|:---|
| **Ubiquitous Language** | 컨텍스트 내 공통 언어 | 도메인 전문가와 개발자가 동일한 용어 사용 | 도메인 용어집, 코드 명명법 | 외국어 사전 |
| **Context Mapper** | 컨텍스트 간 관계 정의 | 팀 간(Partnership), 상향식(OHS), 공유 커널(SDK) 식별 | CML(Context Mapping Language) | 지도 제작소 |
| **Anti-Corruption Layer** | 외부 모델 변환 | 인터페이스/어댑터로 외부 컨텍스트의 잡음 차단 | Facade, Adapter, Translator | customs 관세 |
| **Domain Event** | 컨텍스트 간 비동기 연계 | 상태 변경 이벤트 발행으로 느슨한 결합 | Kafka, RabbitMQ, AMQP | 우편 시스템 |
| **Aggregate Root** | 트랜잭션 경계 | 애그리게이트 루트를 통해서만 접근 제어 | Idempotency 키, 버전 관리 | 가문의 종손 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    바운디드 컨텍스트 매핑 (Context Mapping)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  Partnership   ┌──────────────────┐                  │
│  │  Sales Context   │◄──────────────►│  Inventory Context│                  │
│  │  (주문 컨텍스트)  │                 │  (재고 컨텍스트)  │                  │
│  └────────┬─────────┘                 └────────┬─────────┘                  │
│           │                                    │                             │
│           │ OHS (Open Host Service)            │                             │
│           ▼                                    │                             │
│  ┌──────────────────┐                 ACL      │                             │
│  │  Shipping Context│◄────────────────────────┤                             │
│  │  (배송 컨텍스트)  │    Anti-Corruption      │                             │
│  └──────────────────┘         Layer           │                             │
│                                                │                             │
│  ┌──────────────────┐  Shared Kernel  ┌──────▼─────────┐                   │
│  │  Payment Context │◄───────────────►│  User Context  │                   │
│  │  (결제 컨텍스트)  │                 │  (사용자 컨텍스트)│                   │
│  └──────────────────┘                 └────────────────┘                   │
│                                                                             │
│  [범례]                                                                   │
│  Partnership: 긴밀한 협력, 양방향 통신                                     │
│  OHS: 프로토콜/인터페이스 공개, 단방향 의존                               │
│  ACL: 외부 모델로부터 내부 모델 보호                                       │
│  Shared Kernel: 공통 코드/모델 공유                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Partnership (동반자 관계)**: Sales와 Inventory 컨텍스트는 양방향으로 긴밀히 협력하며, 실시간 동기 통신이 필요합니다. 주문 생성 시 재고 즉시 확인이 예시입니다.

2. **OHS (Open Host Service)**: Sales 컨텍스트가 Shipping 컨텍스트를 위해 공개된 서비스/프로토콜을 제공합니다. Shipping은 Sales의 내부 구현을 알지 못해도 됩니다.

3. **ACL (Anti-Corruption Layer)**: Shipping이 Inventory의 "잔고수량"이라는 용어를 자신의 "출단가능수량"으로 변환하여 자신의 도메인 모델을 보호합니다. 어댑터 패턴과 퍼사드 패턴이 활용됩니다.

4. **Shared Kernel (공유 커널)**: Payment와 User가 인증/권한 같은 핵심 도메인 객체를 공유합니다. 변경 시 협의가 필요하지만, 중복 코드를 방지합니다.

### 심층 동작 원리

```
① 도메인 분석 (Subdomain 식별)
   └─> Core Domain: 핵심 경쟁력 (예: 추천 알고리즘)
   └─> Supporting Subdomain: 지원 기능 (예: 결제)
   └─> Generic Subdomain: 범용 기능 (예: 로그인)

② 바운디드 컨텍스트 후보 추출
   └─> 각 Subdomain을 하나 이상의 BC로 매핑
   └─> 팀 규모(2피자 팀: 6~10명) 고려

③ 컨텍스트 매핑 관계 정의
   └─> Customer/Supplier, Upstream/Downstream 식별
   └─> ACL 필요 여부 판단

④ 마이크로서비스로의 전환
   └─> 1 BC = 1 MS (이상적)
   └─> 또는 1 MS = N BC (운영 효율성 고려)
   └─> 데이터베이스 분리 필수 (Database per Service)
```

### 핵심 알고리즘: BC 식별 점수법

```typescript
/**
 * 바운디드 컨텍스트 분리 점수 계산
 * 높을수록 독립된 마이크로서비스로 분리 유리
 */
interface BCScoreFactors {
  ubiquitiousLanguageClarity: number;  // 유비쿼터스 언어 명확성 (1-5)
  dataCohesion: number;               // 데이터 응집도 (1-5)
  changeFrequency: number;            // 변경 빈도 (1-5)
  teamIndependence: number;           // 팀 독립성 (1-5)
  scalabilityNeeds: number;           // 확장성 요구 (1-5)
}

function calculateBCScore(factors: BCScoreFactors): number {
  // 가중평균: 언어 명확성과 데이터 응집도를 최우선
  const weights = {
    ubiquitiousLanguageClarity: 0.3,
    dataCohesion: 0.25,
    changeFrequency: 0.2,
    teamIndependence: 0.15,
    scalabilityNeeds: 0.1
  };

  return Object.entries(factors).reduce((score, [key, value]) => {
    return score + (value * weights[key as keyof BCScoreFactors]);
  }, 0);
}

// 예시: 추천 시스템 vs 사용자 관리
const recommendationBC: BCScoreFactors = {
  ubiquitiousLanguageClarity: 5,  // "상품 유사도", "협업 필터링" 등 독자적 용어
  dataCohesion: 5,                // 추천 모델, 사용자 행동 이력 밀접히 연관
  changeFrequency: 5,             // 알고리즘 빈번한 변경
  teamIndependence: 5,            // ML 팀이 독립 운영
  scalabilityNeeds: 5             // 대규모 연산 필요
};
// Score: 5.0 → 독립 서비스 강력 추천

const userManagementBC: BCScoreFactors = {
  ubiquitiousLanguageClarity: 3,  // "사용자", "권한" 등 범용 용어
  dataCohesion: 4,
  changeFrequency: 2,             // 안정적 스키마
  teamIndependence: 3,
  scalabilityNeeds: 3
};
// Score: 3.05 → 범용 서비스로 통합 고려
```

### 📢 섹션 요약 비유

여러 종류의 **전문 의료진(내과, 외과, 영상의학과)**이 각자의 진료 기록(컨텍스트)을 유지하면서, 환자의 기본 정보(공유 커널)만 공유하고, 필요시 회진(컨텍스트 매핑)으로 협진하는 것과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: 모놀리식 vs MSA vs 모듈러 모놀리스

| 비교 항목 | Monolithic | MSA (BC 기반) | Modular Monolith |
|:---|:---|:---|:---|
| **배포 단위** | 전체 애플리케이션 | BC별 독립 배포 | 모듈 단위 (단일 프로세스) |
| **데이터 저장소** | 단일 DB | Database per BC | 단일 DB + 스키마 분리 |
| **통신 방식** | 인프로세스 메서드 | HTTP/gRPC/Message Queue | 인프로세스 인터페이스 |
| **트랜잭션** | ACID 로컬 트랜잭션 | Saga 패턴 (분산 트랜잭션) | ACID 로컬 트랜잭션 |
| **운영 복잡도** | 낮음 (단일 서버) | 높음 (오케스트레이션) | 중간 |
| **확장성** | 수직적 확장만 가능 | 수평적 확장 (BC별) | 수직적 확장 |
| **팀 자율성** | 낮음 (전체 조율 필요) | 높음 (BC별 팀) | 중간 (모듈 경계 준수) |
| **도입 적합도** | 소규모 팀, 단순 도메인 | 대규모 팀, 복잡 도메인 | MSA 전 단계 |

### 과목 융합 관점

**1) 데이터베이스 관점 (데이터 중심 아키텍처)**

바운디드 컨텍스트는 **데이터 소유권의 명확한 분리**를 요구합니다. 각 BC는 자신만의 데이터베이스 스키마를 가지며, 이는 다음과 같은 데이터베이스 설계 원칙과 연결됩니다:

- **데이터 정규화**: 각 BC 내에서 3NF 이상 정규화 수행
- **참조 무결성**: FK(Foreign Key)는 BC 내부에서만 허용, BC 간은 ID 참조
- **데이터 중복**: BC 간 필요한 데이터는 이벤트를 통해 비동기 복제 (CQRS 고려)

```
[안티패턴] BC 간 직접 DB 접근
┌─────────────┐         ┌─────────────┐
│  Order MS   │────────>│  Customer DB│  ❌ 결합도 증가
└─────────────┘  직접조회└─────────────┘

[올바른 패턴] API 또는 이벤트 기반
┌─────────────┐  REST API ┌─────────────┐
│  Order MS   │──────────>│Customer MS  │  ✅ 느슨한 결합
└─────────────┘           └─────────────┘
      │                        │
      │ OrderCreated 이벤트     │
      └────────────────────────┘
```

**2) 네트워크/분산 시스템 관점 (CAP 정리)**

BC를 물리적으로 분리하면 **분산 시스템의 트레이드오프**를 고려해야 합니다:

- **CP (Consistency + Partition Tolerance)**: 금융 거래처럼 강한 일관성 필요 → 동기 통신, 2PC 고려
- **AP (Availability + Partition Tolerance)**: SNS 좋아요처럼 결과적 일관성 허용 → 비동기 이벤트
- **결과적 일관성 (Eventual Consistency)**: 도메인 이벤트를 통한 최종 일관성 보장

### 📢 섹션 요약 비유

마치 **연방제 국가**와 같습니다. 각 주(BC)가 독자적인 법률(도메인 모델)과 행정부(데이터베이스)를 가지지만, 연방 정부(공유 커널/인터페이스)가 공통 서비스를 제공하고 주 간 분쟁(ACL)을 중재합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 이커머스 플랫폼 MSA 전환**

기존 모놀리식电商 시스템을 DDD 기반 MSA로 전환하는 상황입니다.

```
[1단계] 도메인 분석 및 Subdomain 식별
┌────────────────────────────────────────────────────────────┐
│ Core Domain (핵심 경쟁력)                                  │
│  └─ 추천 엔진 (Recommendation) → 독립 MS                  │
│  └─ 재할인 정책 (Pricing) → 독립 MS                       │
│                                                            │
│ Supporting Subdomain (지원)                                │
│  └─ 상품 카탈로그 (Catalog)                               │
│  └─ 주문 관리 (Order Management)                          │
│  └─ 재고 관리 (Inventory)                                 │
│                                                            │
│ Generic Subdomain (범용)                                   │
│  └─ 사용자 인증 (Authentication) → SaaS 활용 고려         │
│  └─ 알림 서비스 (Notification) → SaaS 활용 고려           │
└────────────────────────────────────────────────────────────┘

[2단계] 바운디드 컨텍스트 정의 및 매핑
Catalog ──────┐
               │ Shared Kernel (Product ID)
Order ─────────┤
               │
Inventory ─────┘

Order ──OHS──> Shipping (ACL 포함)

[3단계] 마이크로서비스로 구현
- Catalog Service: 상품 조회, 검색 (CQRS 적용)
- Order Service: 주문 생성, 상태 관리 (Saga 패턴)
- Inventory Service: 재고 확보, 예약
- Shipping Service: 배송 시작, 추적
```

**의사결정 과정**:
1. **팀 규모 고려**: 각 BC를 2피자 팀(6~10명)이 담당 가능한지 확인
2. **데이터 독립성**: 각 BC의 데이터를 다른 BC가 직접 조회하지 않도록 설계
3. **API 설계**: BC 간 통신은 명시적인 API(REST/gRPC) 또는 이벤트로 제한

**Scenario 2: 핀테크 결제 시스템**

```
┌─────────────────────────────────────────────────────────────┐
│                    결제 도메인 BC 분리                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                          │
│  │Payment Core  │ (결제 코어: 승인, 취소)                  │
│  │  BC          │                                          │
│  └──────┬───────┘                                          │
│         │                                                  │
│         │ ACL                                              │
│         ▼                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │PG Adapter   │  │Wallet BC     │  │Billing BC    │    │
│  │(외부 PG 연동)│  │(지갑)        │  │(청구서)      │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  Payment Core은 "거래(Transaction)"이라는 용어를 사용하지만,│
│  Wallet은 "잔액 차감", Billing는 "청구 금액"이라는 용어 사용│
│  → ACL을 통해 용어와 모델 변환                              │
└─────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **도메인 분석** | Core/Supporting/Generic Subdomain 식별 완료 | |
| **용어 정의** | 각 BC별 유비쿼터스 언어 용어집 작성 | |
| **데이터 경계** | BC 간 DB 직접 접근 제거, API/이벤트로만 통신 | |
| **팀 구성** | 각 BC를 담당할 2피자 팀 편성 가능 | |
| **CI/CD** | BC별 독립적인 배포 파이프라인 구축 | |
| **모니터링** | BC 간 호출 추적 (Distributed Tracing) 가능 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **ACL 구현** | 외부 BC로부터 내부 모델 보호 계층 존재 | |
| **인가** | BC 간 API 호출에 대한 인가(mTLS/JWT) 적용 | |
| **Rate Limiting** | BC 간 호출에 대한 속도 제한 적용 | |
| **롤백 계획** | Saga补偿 트랜잭션 정의 완료 | |
| **데이터 격리** | 각 BC의 데이터베이스 접근 권한 분리 | |

### 안티패턴

**❌ 분산 모놀리스 (Distributed Monolith)**

```
// 안티패턴: BC를 물리적으로 분리했지만 논리적으로 강결합
OrderService.createOrder() {
  // ① 동기 호출로 재고 확인 (결합도 높음)
  inventoryClient.checkStock(productId);

  // ② 동기 호출로 배송 정보 생성
  shippingClient.createShipping(orderId);

  // ③ 동기 호출로 알림 발송
  notificationClient.sendNotify(orderId);

  // 어느 하나라도 실패하면 전체 실패 (분산의 이점 상실)
}
```

**개선 방안**:

```typescript
// 올바른 패턴: 이벤트 기반 비동기 연계
OrderService.createOrder() {
  // ① 주문 생성
  const order = this.orderRepository.save(order);

  // ② 도메인 이벤트 발행
  this.eventPublisher.publish(new OrderCreatedEvent({
    orderId: order.id,
    productId: order.productId,
    quantity: order.quantity
  }));

  // 나머지는 이벤트 구독자가 비동기 처리
}

// Inventory Service (이벤트 구독자)
@EventListener(OrderCreatedEvent)
async handleOrderCreated(event: OrderCreatedEvent) {
  // 재고 예약 및 실패 시补偿 트랜잭션 발행
}
```

### 📢 섹션 요약 비유

마치 **아파트 단지**와 같습니다. 각 세대(BC)가 독립적인 구조를 가지지만, 수도/전기/가스(공유 커널)는 공급처에서 통합 관리하고, 세대 간에는 방문(인터페이스)을 통해서만 교류합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **배포 리드 타임** | 2주 (전체 시스템) | 30분 (BC별) | **95% 단축** |
| **팀 자율성** | 1명의 PM 결정 대기 | 팀별 자율적 결정 | **决策 속도 3배 향상** |
| **코드 충돌** | 주 5회 이상 | 거의 없음 | **개발 효율 40% 향상** |
| **확장성** | 전체 시스템 확장 | BC별 독립적 확장 | **비용 효율 50% 향상** |
| **기술 부채** | 전체에 영향 | BC 내부로 한정 | **리스크 분산** |

### 미래 전망

1. **BC 자동 식별**: LLM 기반 코드베이스 분석으로 바운디드 컨텍스트 후보 자동 추천
2. **다이나믹 BC**: 런타임에 BC 경계를 동적으로 조정하는 애플리케이션 (Server Functions)
3. **BC as a Service**: 바운디드 컨텍스트 템플릿을 SaaS로 제공 (예: Ververica Platform)

### 참고 표준

- **Domain-Driven Design Reference** (Eric Evans, 2003)
- **Implementing Domain-Driven Design** (Vaughn Vernon, 2013)
- **Microservices Patterns** (Chris Richardson, 2018)
- **CNCF Microservices Architecture White Paper** (Cloud Native Computing Foundation)

### 📢 섹션 요약 비유

스마트폰의 **앱 생태계**와 같습니다. 각 앱(BC)이 독립적으로 개발/배포되지만, 운영체제(공유 커널)와 인터페이스를 통해 협력하며, 전체 플랫폼의 가치를 극대화합니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[도메인 주도 설계 (DDD)](./613_ddd_basics.md)**: DDD 전술적 패턴 (Entity, Value Object, Aggregate)과 바운디드 컨텍스트의 관계
- **[애그리게이트 루트](./615_aggregate_root.md)**: 트랜잭션 경계와 BC의 관계
- **[마이크로서비스 아키텍처](./556_msa.md)**: MSA 전체 아키텍처와 BC의 위치
- **[CQRS](./621_cqrs.md)**: BC 내부의 조회/명령 분리 패턴
- **[사가 패턴](./619_saga_pattern.md)**: BC 간 분산 트랜잭션 관리

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: 학교에서 학년마다 사용하는 교실이 다르고, 선생님별로 수업 방식이 다른 것처럼, 컴퓨터 프로그램도 일하는 영역을 나누어 각자의 방식(언어)을 사용할 수 있게 하는 것입니다.

**2) 원리**: 축구부는 축구 용어로, 밴드부는 음악 용어로 소통하면서도, 학교라는 큰 틀 안에서 서로 협력하는 것처럼, 각 영역이 독립적으로 일하면서 필요할 때만 연락하는 구조를 만듭니다.

**3) 효과**: 반별로 자율적으로 일할 수 있어서 한 반에서 생긴 문제가 다른 반에 영향을 주지 않고, 각 반에서 더 빠르고 좋은 아이디어를 시도할 수 있게 됩니다.
