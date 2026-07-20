---
title: "Context Map / Anti-Corruption Layer Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 228
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ACL (Anti-Corruption Layer, 안티-커럽션 레이어)은 외부 시스템이나 다른 Bounded Context (바운디드 컨텍스트)의 도메인 모델이 우리 도메인 모델을 오염(Corrupt)시키지 못하도록 차단하는 DDD (Domain-Driven Design, 도메인 주도 설계) 번역 계층이다.
> 2. **가치**: 레거시 시스템이나 외부 서비스의 개념·용어·모델이 내부 도메인 언어를 잠식하는 것을 방지하여, 내부 도메인 모델의 순수성과 표현력(Expressiveness)을 유지한다.
> 3. **판단 포인트**: Context Map (컨텍스트 맵)은 바운디드 컨텍스트들 간의 관계를 지도(Map)로 표현한다 — ACL은 그 관계 유형 중 하나로, "우리가 주도권을 갖고 외부를 번역"하는 방어적 관계다.

---

## Ⅰ. 개요 및 필요성
대형 소프트웨어에서 "C고객(고객)"는 컨텍스트마다 다른 의미를 갖는다:

```
결제 컨텍스트: Customer { cardNumber, billingAddress, creditScore }
배송 컨텍스트: Customer { deliveryAddress, phone, deliveryPreference }
CRM 컨텍스트: Customer { leadScore, segment, contactHistory }
```

하나의 거대한 C고객 모델로 통합하면:
- 모델이 비대해지고 각 팀의 의도가 희석됨
- 변경 시 전체 시스템 영향도 증가
- 팀 간 조율 비용 폭증

**해결**: 컨텍스트별로 독립된 모델을 유지하되, 경계(Context)를 명확히 정의 -> Bounded Context.

```
레거시 시스템 통합:
  레거시 DB: CUST_TBL { CUST_ID, CUST_NM, ADDR_CD, STAT_FLG, ... }
             (약어, 코드값, 냄새나는 레거시 모델)

  ACL 없이 직접 참조:
    Order 도메인 내부에 CUST_NM, ADDR_CD 등 레거시 용어 침투
    -> 도메인 모델 오염, 가독성 파괴

  ACL 적용:
    CustomerAdapter.translate(CUST_TBL 레코드) -> Customer(name, address)
    Order 도메인은 깨끗한 Customer 모델만 참조
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: ACL은 공항 입국 심사관 — 어떤 외국인(외부 모델)이 들어오더라도 입국 심사관(ACL)이 우리나라 규정(내부 도메인 모델)에 맞게 처리하고, 의심스러운 것(오염 요소)은 걸러낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+-----------------------------------------------------------------+
|                   Context Map 관계 유형                          |
|                                                                 |
|  [주문 컨텍스트] ------- Shared Kernel -------- [결제 컨텍스트]  |
|      (공유 라이브러리로 일부 모델 공유)                            |
|                                                                 |
|  [주문 컨텍스트] --- Customer-Supplier ---> [재고 컨텍스트]        |
|      (주문=고객, 재고=공급자 -> 주문이 요구사항 정의)               |
|                                                                 |
|  [CRM 컨텍스트] ------ Conformist -------> [외부 SAP 시스템]      |
|      (외부 모델을 그대로 따름, 협상력 없음)                        |
|                                                                 |
|  [배송 컨텍스트] ---- ACL ---------------> [레거시 물류 시스템]    |
|      (번역 계층으로 레거시 모델 차단)       <- 우리가 번역           |
|                                                                 |
|  [공개 API 컨텍스트] - Open Host Service -> [다수의 소비자]        |
|      (표준화된 공개 프로토콜로 서비스 제공)                        |
|                                                                 |
|  [이벤트 컨텍스트] --- Published Language -> [다수의 소비자]       |
|      (표준 이벤트 스키마/메시지 형식 발행)                         |
+-----------------------------------------------------------------+
```

```
외부 시스템                   ACL                    내부 도메인
+-------------+        +-----------------+        +-------------+
|  레거시 API  |        |  +-----------+  |        | Order       |
|             |--HTTP-->|  | Adapter   |  |------->| Domain      |
| {CUST_ID:   |        |  | (외부 호출)|  |        |             |
|  "C001",    |        |  +-----+-----+  |        | Customer {  |
|  CUST_NM:   |        |        | 변환    |        |   name,     |
|  "홍길동",   |        |  +-----v-----+  |        |   address   |
|  STAT_FLG:  |        |  |Translator |  |        | }           |
|  "Y" }      |        |  |(모델 변환) |  |        +-------------+
+-------------+        |  +-----------+  |
                       +-----------------+
```

| 관계 유형 | 설명 | 팀 협력도 | 모델 독립성 |
|:---|:---|:---|:---|
| Shared Kernel | 두 팀이 공유 코어 모델 공동 관리 | 매우 높음 | 낮음 |
| C고객-Supplier | 공급자가 고객 요구사항 반영 | 높음 | 중간 |
| Conformist | 공급자 모델을 고객이 그대로 따름 | 낮음 | 낮음 |
| <strong>ACL</strong> | **번역 계층으로 외부 모델 차단** | **낮음** | **높음** |
| Published Language | 표준 공개 언어로 통신 | 중간 | 높음 |
| Open Host Service | 공개 API + 프로토콜 제공 | 중간 | 높음 |

- **📢 섹션 요약 비유**: Conformist는 "로마에 가면 로마법을 따른다" — 외부 모델 그대로 적용. ACL은 "로마 법률을 우리 언어로 번역해서 우리 법체계에 적용" — 외부 모델을 우리 언어로 변환.

---

## Ⅲ. 비교 및 연결
```java
// ACL 구현 예시 — 레거시 고객 시스템과의 통합
@Component
public class LegacyCustomerACL {
    private final LegacyCustomerServiceClient legacyClient;

    // Adapter: 외부 API 호출
    public LegacyCustomerDTO fetchFromLegacy(String custId) {
        return legacyClient.getCustomer(custId);  // 레거시 DTO
    }

    // Translator: 레거시 모델 -> 우리 도메인 모델 변환
    public Customer translate(LegacyCustomerDTO dto) {
        return Customer.of(
            CustomerId.of(dto.getCustId()),
            CustomerName.of(dto.getCustNm()),      // 약어 -> 명확한 이름
            Address.of(resolveAddressCode(dto.getAddrCd())),  // 코드 -> 의미
            CustomerStatus.from(dto.getStatFlg())  // Y/N -> Enum
        );
    }

    private String resolveAddressCode(String addrCd) {
        // 레거시 코드값을 실제 주소로 변환
        return addressCodeRepository.findById(addrCd)
            .map(AddressCode::getFullAddress)
            .orElseThrow();
    }
}
```

| 비교 항목 | ACL (Anti-Corruption Layer) | Adapter Pattern |
|:---|:---|:---|
| 목적 | 도메인 모델 오염 방지 (DDD 개념) | 인터페이스 호환성 해결 (GoF 패턴) |
| 관점 | 전략적 설계 (Strategic Design) | 전술적 설계 (Tactical Design) |
| 범위 | 컨텍스트 경계 전체 | 개별 클래스/인터페이스 |
| 포함 요소 | Adapter + Translator + Facade | 인터페이스 변환만 |

- **📢 섹션 요약 비유**: Adapter Pattern은 플러그 어댑터(220V -> 110V 변환), ACL은 외교관(두 나라 문화·법률·언어를 이해하고 양쪽에 맞게 해석)이다. 어댑터는 형태만 바꾸고, ACL은 의미를 번역한다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```
MSA(Microservice Architecture) 환경:

  [주문 서비스]    ACL    [외부 결제 게이트웨이]
       |          |       (PayPal, Stripe, KG이니시스)
       |          |       각 결제사마다 다른 API 모델
       |          v
       +--> PaymentACL
             +-- PaypalAdapter   (PayPal API 번역)
             +-- StripeAdapter   (Stripe API 번역)
             +-- KGiniAdapter    (KG이니시스 API 번역)
             |
             +--> 내부: Payment(amount, currency, method, status)
             (모든 결제사 차이를 ACL 내부에서 흡수)
```

```
외부 이벤트 -> ACL -> 내부 도메인 이벤트

외부: {"event": "ORDER_PLACED", "custId": "C001", "items": [...]}
ACL 변환: OrderPlacedEvent { customer: Customer{...}, lineItems: [...] }
내부 핸들러: OrderPlacedEvent를 처리 (레거시 필드명 없음)
```

| 상황 | ACL 적용 | 이유 |
|:---|:---|:---|
| 레거시 시스템과 통합 | 필수 | 레거시 모델 오염 방지 |
| 외부 SaaS API 연동 | 강력 권장 | API 변경에 내부 격리 |
| 같은 팀 내 컨텍스트 | 선택적 | 팀 협력으로 조율 가능 |
| Published Language | 불필요 | 이미 표준화된 인터페이스 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 해외 직구할 때 해외 사이트의 주소 체계(CITY-STATE-ZIP)를 한국 주소 체계(도-시-구-동)로 변환해주는 배송 대행지가 ACL — 내 집(내부 도메인)은 한국 주소 체계만 알면 된다.

---

## Ⅴ. 기대효과 및 결론
Context Map과 ACL 패턴은 대규모 소프트웨어 시스템의 전략적 설계 도구다:

**ACL의 핵심 기대효과**:
- <strong>내부 도메인 모델 순수성 유지</strong>: 외부 오염으로부터 격리
- **변경 격리**: 외부 시스템 API 변경이 내부에 미치는 영향 최소화
- **표현력 유지**: 도메인 전문가와 개발자가 공유하는 Ubiquitous Language 보존
- **테스트 용이성**: ACL을 Stub으로 대체하여 내부 도메인 독립 테스트

<strong>Context Map의 가치</strong>:
- 팀 간 협업 관계의 명시적 문서화
- 통합 방식(ACL, Conformist 등)의 의도적 선택
- 새로운 팀/서비스 추가 시 통합 전략 가이드

심화 학습에서는 <strong>6가지 Context Map 관계 유형</strong>과 <strong>ACL이 방어하는 것(도메인 모델 오염)</strong>을 명확히 서술하고, <strong>ACL의 내부 구성요소(Adapter + Translator)</strong> 를 설명하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: ACL은 나라의 관세청 + 세관 — 해외(외부 시스템)에서 들어오는 물건(모델)을 검사하고(번역), 국내 규격(도메인 모델)에 맞지 않는 것은 걸러내거나 변환하여 내부 시장(도메인)의 품질을 보호한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | DDD (Domain-Driven Design) | ACL이 속하는 전략적 설계 도구 |
| 핵심 개념 | Bounded Context | ACL이 지키는 경계의 단위 |
| 연관 개념 | Ubiquitous Language | ACL이 보호하는 내부 도메인 언어 |
| 유사 패턴 | Adapter Pattern | GoF 수준의 인터페이스 변환 |
| 연관 패턴 | Facade Pattern | ACL이 외부 시스템을 래핑하는 방식 |
| 컨텍스트 맵 관계 | Shared Kernel, C고객-Supplier, Conformist, Published Language | ACL과 비교되는 6가지 관계 유형 |
| 적용 사례 | MSA 결제 게이트웨이 통합 | ACL로 복수 결제사 API 번역 |

### 📈 관련 키워드 및 발전 흐름도
Bounded Context -> 컨텍스트 맵과 ACL 패턴 -> 통합 번역 계층

### 👶 어린이를 위한 3줄 비유 설명
1. ACL은 다른 나라(외부 시스템) 말을 우리말로 통역해주는 통역사 — 외국어(레거시 모델)가 우리 방(내부 도메인)에 직접 들어오지 못하게 막아줘.
2. 레거시 시스템의 이상한 약어(`CUST_NM`, `STAT_FLG`)를 우리가 이해하기 쉬운 말(`name`, `status`)로 바꿔주는 역할이 ACL이야.
3. 컨텍스트 맵은 우리 회사 부서들 사이의 협업 관계도 — "배송팀은 결제팀 시스템을 ACL로 번역해서 쓴다"처럼 각 팀이 어떻게 협업하는지 그림으로 보여줘.
