---
title: "J2EE Framework Patterns"
date: "2026-04-21"
tags:
  - "studynote-design-supervision"
weight: 174
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: J2EE (Java 2 Platform, Enterprise Edition) 프레임워크 패턴은 웹 계층, 비즈니스 계층, 통합 계층 사이에서 반복되는 엔터프라이즈 문제를 표준화한 계층형 설계 패턴 묶음이다.
> 2. **가치**: Front Controller, DTO (Data Transfer Object), Session Facade, DAO (Data Access Object) 같은 패턴은 요청 진입점, 원격 호출 수, 트랜잭션 경계, 데이터 접근 책임을 분리해 대규모 시스템의 결합도를 낮춘다.
> 3. **판단 포인트**: 패턴의 이름을 외우는 것보다 "어떤 경계를 왜 분리하는가"가 중요하며, 현대 Spring/Jakarta EE 환경에서는 패턴의 의도는 살리되 Service Locator 같은 레거시 기법은 DI (Dependency Injection)로 대체하는 판단이 필요하다.

---

## Ⅰ. 개요 및 필요성

J2EE 패턴은 단순 객체 설계 기법이 아니라, 엔터프라이즈 웹 시스템이 반복해서 겪는 운영 문제에 대한 해법이다. 2000년대 초 J2EE 환경에서는 Servlet, JSP (JavaServer Pages), EJB (Enterprise JavaBeans), JNDI (Java Naming and Directory Interface), 원격 호출이 뒤섞이며 구조가 빠르게 복잡해졌다. 요청 처리 로직이 화면마다 흩어지고, 비즈니스 계층은 여러 원격 EJB를 잦게 호출했으며, 데이터 접근 코드는 서비스 로직에 섞였다. 이런 반복 문제를 "계층별 패턴 언어"로 정리한 것이 Core J2EE Patterns 계열이다.

이 패턴들이 중요했던 이유는 성능과 유지보수성 때문이다. 네트워크 왕복이 비싼 시대에는 자잘한 원격 호출이 곧 성능 저하였고, JNDI lookup 같은 인프라 의존 코드가 프레젠테이션 계층까지 침투하면 테스트와 교체가 어려웠다. 결국 J2EE 패턴은 "어떤 클래스가 예쁜가"보다 <strong>어떤 책임을 어느 계층 경계에 둬야 시스템이 견딜 수 있는가</strong>를 다뤘다.

```text
+----------------------------------------------------------------------+
| Enterprise pain points that created J2EE patterns                    |
+----------------------------------------------------------------------+
| Web tier       : duplicated request handling, auth, navigation       |
| Business tier  : chatty remote calls, unclear transaction boundary   |
| Integration    : SQL / JNDI / legacy access mixed into service code  |
|                                                                      |
| Pattern goal   : split entry, orchestration, transfer, persistence   |
+----------------------------------------------------------------------+
```

현재는 Jakarta EE라는 이름이 더 공식적이지만, 설계 패턴 명칭과 사고방식은 여전히 J2EE 패턴으로 널리 통한다. 즉 이 주제는 특정 프레임워크 버전보다 <strong>엔터프라이즈 계층 설계의 공통 문법</strong>으로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: J2EE 패턴은 대형 병원에서 접수창구, 진료과, 검사실, 약국의 역할을 나누는 운영 매뉴얼과 같다. 한 사람이 모두 처리하면 처음엔 빨라 보여도, 환자가 많아질수록 혼란이 폭발한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

J2EE 패턴의 핵심 원리는 네 가지다. 첫째, **단일 진입점**: 모든 웹 요청을 공통 지점에서 받아 공통 처리를 집중한다. 둘째, **원격 호출 축소**: 여러 번 왕복할 데이터를 DTO와 Facade로 묶는다. 셋째, **인프라 의존성 격리**: JNDI lookup, SQL (Structured Query Language), 메시징 같은 기술 세부사항을 상위 계층에서 숨긴다. 넷째, **계층 책임 분리**: 프레젠테이션은 화면 흐름, 비즈니스는 정책, 통합 계층은 저장/연계에 집중하게 만든다.

```text
+----------------------------------------------------------------------+
| J2EE pattern map across layers                                       |
+----------------------------------------------------------------------+
| Client                                                               |
|   |                                                                  |
|   v                                                                  |
| Front Controller -> Intercepting Filter -> Controller / View Helper  |
|   |                                                                  |
|   v                                                                  |
| Business Delegate -> Session Facade -> DTO / Assembler               |
|   |                                                                  |
|   v                                                                  |
| DAO / Repository-like access -> Database / Legacy / External Service |
|                                                                      |
| Service Locator sits beside container lookup when DI is unavailable  |
+----------------------------------------------------------------------+
```

| 패턴 | 주 계층 | 해결하려는 문제 | 현대적 해석 |
| :--- | :--- | :--- | :--- |
| Front Controller | Presentation | 요청 분산 처리, 공통 전처리 중복 | `DispatcherServlet`, Application Programming Interface (API) Gateway의 축소판 |
| Intercepting Filter | Presentation | 인증, 로깅, 인코딩 같은 횡단 관심사 | Servlet Filter, Spring Filter Chain |
| DTO | Boundary | 잦은 원격 호출, 과도한 내부 모델 노출 | API Request/Response DTO, record |
| Business Delegate | Presentation ↔ Business | 원격 서비스 호출 캡슐화 | 서비스 클라이언트 래퍼, adapter |
| Session Facade | Business | 여러 원격 호출과 트랜잭션 경계 정리 | Application Service, transactional facade |
| DAO | Integration | SQL/저장소 접근 코드 분리 | `@Repository`, Spring Data JPA (Java Persistence API), persistence adapter |
| Service Locator | Infrastructure | 서비스 lookup 중복 | 과거 JNDI 캡슐화, 현재는 DI로 대체 권장 |

여기서 중요한 것은 패턴들이 독립적으로 존재하지 않는다는 점이다. 예를 들어 Front Controller가 요청을 모으면, 그 아래에서 공통 필터가 보안/로그를 처리하고, 비즈니스 호출은 Session Facade로 모아 트랜잭션을 정의하며, 외부로 나가는 데이터는 DTO로 정리되고, 저장소 접근은 DAO로 분리된다. 즉 J2EE 패턴은 개별 기법 모음이 아니라 <strong>경계마다 다른 책임을 부여하는 협업 구조</strong>다.

또한 현대 프레임워크는 많은 패턴을 내장한다. Spring MVC는 Front Controller를, Spring Transaction은 Facade의 트랜잭션 경계를, Spring Data JPA는 DAO의 구현 부담을 크게 줄였다. 그래서 오늘날 중요한 것은 패턴 구현 코드를 재현하는 일이 아니라, <strong>프레임워크가 이미 제공하는 패턴적 성질을 이해하는 것</strong>이다.

- **📢 섹션 요약 비유**: J2EE 패턴은 공연장을 운영할 때 입장 게이트, 안내 요원, 무대 감독, 창고 담당을 나누는 방식과 같다. 각 역할이 분명해야 관객이 많아져도 공연이 꼬이지 않는다.

---

## Ⅲ. 비교 및 연결

J2EE 패턴은 GoF (Gang of Four) 패턴, DDD (Domain-Driven Design), Spring 관례와 자주 비교된다. 차이는 해결 범위에 있다. GoF가 클래스와 객체 협력의 미시 구조를 다룬다면, J2EE는 웹 요청, 원격 호출, 저장소 연동 같은 <strong>시스템 경계의 거시 구조</strong>를 다룬다.

| 비교 축 | J2EE 패턴 | GoF 패턴 | DDD / 현대 Spring |
| :--- | :--- | :--- | :--- |
| 주 관심사 | 계층 경계와 엔터프라이즈 협력 | 객체 생성·구조·행위 | 도메인 모델과 프레임워크 생산성 |
| 대표 문제 | chatty call, lookup, request routing | 객체 조립, 확장성, 재사용성 | 비즈니스 의미, DI, 테스트 용이성 |
| 대표 패턴 | Front Controller, Session Facade, DAO | Factory Method, Adapter, Proxy | Repository, Application Service, DI |
| 현대 적용 | 의도는 유지, 구현은 단순화 | 여전히 세부 설계에 유효 | J2EE 의도를 더 높은 수준에서 흡수 |

특히 Service Locator는 현대 환경에서 중요한 비교 포인트다. J2EE 초기에는 JNDI lookup 비용과 중복을 줄이는 유용한 패턴이었지만, DI 컨테이너가 보편화된 뒤에는 의존성이 코드 밖에서 숨겨져 테스트가 어려워지는 문제가 더 커졌다. 따라서 <strong>DI가 가능한 환경에서는 Service Locator를 습관적으로 넣지 않는 판단</strong>이 중요하다.

DAO와 Repository도 구분해야 한다. DAO는 저장 기술 중심 추상화에 가깝고, Repository는 도메인 애그리게이트 중심 추상화다. 즉 J2EE 패턴의 DAO 정신은 여전히 중요하지만, 도메인 주도 설계가 강한 시스템에서는 Repository가 더 높은 수준의 해법일 수 있다.

- **📢 섹션 요약 비유**: GoF가 방 안 가구를 어떻게 배치할지 정하는 법이라면, J2EE 패턴은 집 안에 현관, 거실, 주방, 창고를 어떻게 나눌지 정하는 설계도에 가깝다. 둘 다 필요하지만 문제의 크기가 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 패턴을 많이 쓰는 것이 능사가 아니다. 중요한 것은 **어떤 분리 비용이 실제로 이득을 주는지** 판단하는 것이다. 모든 계층에 Delegate, Facade, DTO, DAO를 무조건 겹겹이 쌓으면 오히려 단순 생성·조회·수정·삭제 (CRUD) 시스템에서 과설계가 된다. 반대로 대규모 시스템에서 이 경계를 생략하면 로직이 화면·서비스·데이터베이스 (DB) 코드에 뒤섞여 변경 비용이 폭발한다.

| 상황 | 권장 패턴 해석 | 이유 |
| :--- | :--- | :--- |
| 웹 요청의 공통 인증·로깅·예외 처리 필요 | Front Controller + Filter | 진입점 통합과 횡단 관심사 분리가 효과적이다. |
| 여러 서비스/저장소를 묶어 하나의 업무를 완료 | Session Facade / Application Service | 트랜잭션 경계와 유스케이스 orchestration이 명확해진다. |
| 외부 호출이나 원격 서비스가 많음 | DTO + client adapter | 네트워크 경계를 넘는 데이터 형식을 안정화한다. |
| 저장 기술 교체 가능성이 큼 | DAO 또는 Repository | 비즈니스 로직을 인프라 세부 구현에서 분리한다. |
| Spring Boot 단순 모놀리식 로컬 호출 중심 | Service Locator 생략 | DI가 이미 더 나은 해법을 제공한다. |

### 자주 발생하는 안티패턴

- DAO 안에 비즈니스 규칙과 트랜잭션 로직을 함께 넣는 구성
- DTO를 엔티티처럼 재사용해 계층 경계를 흐리는 설계
- 모든 호출이 로컬인데도 EJB 시절 습관처럼 Delegate/Facade를 중첩하는 구조
- 패턴 이름은 맞지만 실제 책임이 뒤섞여 있는 "껍데기 패턴"

### 학습 정리 포인트

1. J2EE 패턴은 계층 분리와 원격 호출 최적화 문제에서 등장했다.
2. 현대 프레임워크는 다수의 패턴을 내장하지만 패턴의 의도는 그대로 남아 있다.
3. Service Locator는 역사적으로 의미가 있으나, DI 환경에서는 안티패턴이 될 수 있다.
4. DAO, DTO, Front Controller는 여전히 자주 쓰이지만, 도메인 복잡도와 운영 경계에 맞게 선택해야 한다.

결국 설계감리 관점의 질문은 "이 패턴을 썼는가"가 아니라, <strong>요청 진입점, 업무 경계, 데이터 경계가 설계 문서와 코드에서 일관되게 분리되어 있는가</strong>다.

- **📢 섹션 요약 비유**: 패턴 적용은 부엌에 칼을 몇 자루 두느냐가 아니라, 칼·도마·냉장고가 제자리에 있어 요리가 엉키지 않게 만드는 주방 동선 설계와 같다.

---

## Ⅴ. 기대효과 및 결론

J2EE 프레임워크 패턴을 올바르게 이해하면 엔터프라이즈 시스템의 구조를 "기술 조각 모음"이 아니라 "경계와 책임의 조합"으로 볼 수 있다. 그 결과 요청 처리, 트랜잭션, 데이터 접근, 원격 통신을 분리해 유지보수성과 테스트 가능성, 팀 간 협업 효율을 높일 수 있다. 특히 레거시 Java 시스템을 modernize할 때도 어떤 경계를 살리고 무엇을 걷어낼지 판단하는 기준이 된다.

다만 모든 패턴이 오늘날 동일한 무게를 갖는 것은 아니다. 일부는 EJB/JNDI 시대의 제약을 반영한 해법이므로, 현대 Jakarta EE나 Spring에서는 더 단순한 방법으로 구현하는 편이 낫다. 따라서 J2EE 패턴을 외울 때는 "구현 세부"보다 <strong>분리하려던 문제와 설계 의도</strong>를 중심에 두는 것이 가장 중요하다.

- **📢 섹션 요약 비유**: 오래된 도시의 교통 규칙을 공부하는 이유는 오래된 마차를 다시 타기 위해서가 아니라, 왜 길을 일방통행으로 나눴는지 이해해 오늘의 도로도 더 잘 설계하기 위해서다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Front Controller | 프레젠테이션 계층의 단일 진입점 패턴이다. |
| DTO (Data Transfer Object) | 계층/원격 경계의 데이터 전송 효율과 형식 안정성을 담당한다. |
| DAO (Data Access Object) | 저장소 접근 책임을 비즈니스 로직에서 분리한다. |
| Session Facade | 유스케이스 단위의 업무 조합과 트랜잭션 경계를 제공한다. |
| DI (Dependency Injection) | Service Locator를 대체하는 현대적 의존성 관리 방식이다. |
| Repository | DAO 정신을 도메인 중심으로 확장한 현대 패턴이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Servlet / JSP / EJB complexity
    |
    v
Core J2EE Patterns
    |
    +- request entry unification
    +- remote call reduction
    +- transaction boundary definition
    +- persistence isolation
    |
    v
Spring / Jakarta EE simplification
    |
    v
Repository / DI / API-driven enterprise patterns
```

이 흐름은 J2EE 패턴이 레거시 제약을 해결하는 언어에서 출발해, 현대 프레임워크의 설계 의도로 흡수되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. J2EE 패턴은 큰 학교에서 정문 선생님, 담임 선생님, 창고 담당 선생님 일을 나눠 맡기는 규칙이에요.
2. 누구나 자기 일만 잘하면 학교가 커져도 덜 헷갈리고 문제가 생겨도 어디를 고쳐야 할지 쉬워져요.
3. 요즘 학교는 더 좋은 도구를 쓰지만, "역할을 나눠서 운영한다"는 생각은 그대로 중요해요.
