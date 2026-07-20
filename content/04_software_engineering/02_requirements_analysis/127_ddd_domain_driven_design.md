---
title: "Ddd Domain Driven Design"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 127
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDD는 <strong>복잡한 비즈니스 도메인을 소프트웨어 모델의 중심에 놓고</strong>, 도메인 전문가와 개발자가 <strong>유비쿼터스 언어(Ubiquitous Language)</strong>를 공유하여 모델과 코드를 일치시키는 설계 방법론이다.
> 2. **가치**: 기술 중심 설계는 비즈니스 로직이 여기저기 흩어지고 도메인 전문가의 의도와 코드가 괴리되지만, DDD는 <strong>도메인 모델이 곧 코드</strong>가 되어 변경에 강하고 이해하기 쉬운 시스템을 만든다.
> 3. **판단 포인트**: <strong>전략적 설계</strong>(Bounded Context·Context Map)와 **전술적 설계**(Entity·Value Object·Aggregate·Repository)를 구분하고, MSA의 서비스 경계가 Bounded Context와 일치해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    DDD 전략적·전술적 설계                             |
+-------------------------------------------------------+
|  [전략적 설계 — 큰 그림]                              |
|   Bounded Context: 도메인별 경계                     |
|   Context Map: BC 간 관계 (ACL, OHS, CF)             |
|   Ubiquitous Language: 공통 용어                     |
|                                                       |
|  [전술적 설계 — 코드 레벨]                            |
|   Entity (식별자), Value Object (불변)               |
|   Aggregate (일관성 경계), Repository (저장소)        |
|   Domain Service, Domain Event                       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: DDD는 회사 조직도(전략: 부서 경계)와 업무 매뉴얼(전술: 역할·규칙)을 동시에 설계하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 전술적 패턴

| 패턴 | 설명 | 예 |
|:---|:---|:---|
| **Entity** | 식별자로 구분 | 주문(OrderId) |
| **Value Object** | 값으로 동등성 판단 | 금액(Money) |
| <strong>Aggregate</strong> | 일관성 경계 | 주문+주문항목 |
| **Repository** | Aggregate 저장소 | OrderRepository |
| <strong>Domain Event</strong> | 도메인 변화 알림 | OrderPlaced |

- **📢 섹션 요약 비유**: Aggregate는 가족(한 가장이 대표)이고, Entity는 가족 구성원(주민번호로 구분), Value Object는 주소(값이 같으면 동일)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 데이터 중심 | DDD |
|:---|:---|:---|
| **시작점** | DB 테이블 | <strong>도메인 모델</strong> |
| **용어** | 기술 용어 | <strong>도메인 용어</strong> |
| **변경** | DB 변경 -> 전파 | **모델 변경 = 코드 변경** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### DDD + MSA
- Bounded Context = 마이크로서비스 경계.
- Domain Event = 서비스 간 비동기 통신.
- Anti-Corruption Layer = 레거시 시스템 격리.

---

## Ⅴ. 기대효과 및 결론

DDD는 <strong>복잡한 비즈니스 도메인을 다루는 대규모 시스템 설계의 핵심 방법론</strong>이며, MSA 서비스 경계 설계의 이론적 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Bounded Context</strong> | 도메인 경계 (=MSA 서비스) |
| <strong>Ubiquitous Language</strong> | 도메인 전문가+개발자 공통 용어 |
| <strong>Aggregate</strong> | 일관성 경계 (트랜잭션 단위) |
| <strong>Domain Event</strong> | 서비스 간 비동기 통신 |
| **Event Storming** | DDD 분석 워크숍 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 중심 설계 (ERD 기반, ~2000s)]
    |
    v
[DDD (Eric Evans, 2003) — 도메인 중심]
    |
    v
[CQRS + Event Sourcing (2010~)]
    |
    v
[DDD + MSA (2014~) — Bounded Context = Service]
    |
    v
[현재: Event Storming + DDD — 협업 기반 도메인 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DDD는 <strong>레고 설명서</strong>처럼 만들 물건(도메인)을 먼저 이해하고 설계하는 거예요.
2. 만드는 사람(개발자)과 주문한 사람(고객)이 <strong>같은 이름(유비쿼터스 언어)</strong>으로 부르면 혼동이 없어요.
3. 큰 레고를 <strong>작은 묶음(Bounded Context)</strong>으로 나누면 여러 팀이 동시에 만들 수 있답니다!
