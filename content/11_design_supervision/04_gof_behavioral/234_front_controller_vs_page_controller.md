---
title: "Front Controller vs Page Controller"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 234
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프론트 컨트롤러 (Front Controller) 는 모든 요청이 단일 진입점을 거치므로 인증·로깅·라우팅 등 공통 처리를 중앙화하고, 페이지 컨트롤러 (Page Controller) 는 각 URL이 개별 핸들러로 직접 연결된다.
> 2. **가치**: 프론트 컨트롤러는 횡단 관심사 (Cross-Cutting Concerns) 를 일원화해 중복을 제거하며, 페이지 컨트롤러는 단순 구조로 빠른 초기 개발이 가능하다.
> 3. **판단 포인트**: 공통 처리가 많고 URL 구조가 복잡하면 프론트 컨트롤러, 페이지가 적고 독립적이면 페이지 컨트롤러가 적합하다.

---

## Ⅰ. 개요 및 필요성
웹 애플리케이션에서 HTTP (HyperText Transfer Protocol) 요청을 어디서, 어떻게 받을 것인가는 전체 구조를 결정하는 핵심 설계 문제다. 초기 Servlet/JSP 기반 개발에서는 페이지 컨트롤러 방식이 자연스러웠다—URL마다 서블릿 하나가 대응하는 형태다. 그러나 인증 검사, 로깅, 트랜잭션 시작, 예외 처리 등 공통 로직이 모든 서블릿에 복사되는 문제가 발생했다.

프론트 컨트롤러 (Front Controller) 패턴은 이를 해결하기 위해 <strong>단일 서블릿</strong>이 모든 요청을 받아 공통 처리 후 적합한 핸들러로 위임하는 구조를 제안한다. Spring MVC의 `DispatcherServlet`, Struts의 `ActionServlet`이 대표적 구현체다.

| 패턴 | 도입 시기 | 대표 구현체 |
|:---|:---:|:---|
| Page Controller | 초기 Servlet (1997~) | 개별 Servlet, ASP 페이지 |
| Front Controller | 마틴 파울러 PEAA (2002) | Struts, Spring MVC, Django |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 페이지 컨트롤러는 건물 각 방에 별도 입구가 있는 구조이고, 프론트 컨트롤러는 정문 하나에서 모든 방문자를 안내 데스크가 체크하고 안내하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+-------------------------------------------------------------+
|                 Page Controller 구조                         |
|                                                             |
|  /login   --->  +------------------+                        |
|                |  LoginServlet    |---> login.jsp            |
|                | (인증 + 뷰 처리)  |                        |
|                +------------------+                        |
|  /order   --->  +------------------+                        |
|                |  OrderServlet    |---> order.jsp            |
|                | (인증 + 뷰 처리)  |  <- 중복!               |
|                +------------------+                        |
|  /profile --->  +------------------+                        |
|                |  ProfileServlet  |---> profile.jsp          |
|                | (인증 + 뷰 처리)  |  <- 중복!               |
|                +------------------+                        |
+-------------------------------------------------------------+
```

```
+-------------------------------------------------------------+
|               Front Controller 구조                          |
|                                                             |
|  모든 요청  --->  +------------------------------------+     |
|                 |  Front Controller (DispatcherServlet)|     |
|                 |  1. 인증 검사 (공통)                  |     |
|                 |  2. 로깅 (공통)                       |     |
|                 |  3. Handler Mapping                  |     |
|                 +--------------+---------------------+     |
|                                | 위임 (Dispatch)            |
|              +-----------------+------------------+        |
|              v                 v                  v         |
|  +-----------------+ +--------------+ +------------------+ |
|  |  LoginHandler   | | OrderHandler | |  ProfileHandler  | |
|  +--------+--------+ +------+-------+ +-------+----------+ |
|           v                 v                  v            |
|        login.jsp         order.jsp          profile.jsp     |
+-------------------------------------------------------------+
```

| 단계 | Page Controller | Front Controller |
|:---:|:---|:---|
| 요청 수신 | 각 서블릿 개별 수신 | DispatcherServlet 단일 수신 |
| 인증 처리 | 각 서블릿에 반복 코드 | Filter / Interceptor 중앙 처리 |
| 라우팅 | web.xml URL 매핑 | Handler Mapping 동적 결정 |
| 뷰 렌더링 | 각 서블릿이 직접 forward | View Resolver 통해 위임 |

- **📢 섹션 요약 비유**: 공항에서 모든 승객이 한 개의 보안 검색대(프론트 컨트롤러)를 통과한 뒤 게이트(핸들러)로 이동하는 것과 같다. 게이트별 보안 검사 중복이 사라진다.

---

## Ⅲ. 비교 및 연결
| 항목 | Page Controller | Front Controller |
|:---|:---|:---|
| 진입점 수 | URL 수 만큼 | 단일 (1개) |
| 공통 처리 | 중복 코드 | Filter/Interceptor 일원화 |
| 구현 복잡도 | 낮음 | 중간~높음 |
| 확장성 | 낮음 (파일 수 증가) | 높음 |
| 라우팅 유연성 | 낮음 (정적 매핑) | 높음 (동적, 정규식, REST) |
| 테스트 용이성 | 낮음 (서블릿 의존) | 높음 (MockMvc 등) |
| 적합 규모 | 소규모 사이트 | 중대형 웹 애플리케이션 |

```
요청 -> DispatcherServlet
          -> HandlerMapping (URL -> Controller 결정)
          -> HandlerAdapter (Controller 실행)
          -> ViewResolver (논리 뷰명 -> 물리 경로 변환)
          -> View (렌더링)
          -> 응답
```

Spring의 `DispatcherServlet`은 프론트 컨트롤러 패턴의 교과서적 구현이다. `@Controller`, `@RequestMapping`이 바로 이 구조 위에서 동작한다.

- **📢 섹션 요약 비유**: 프론트 컨트롤러는 오케스트라의 지휘자다. 각 악기(핸들러)는 자신의 파트만 연주하고, 지휘자가 전체 흐름과 타이밍을 조율한다.

---

## Ⅳ. 실무 적용 및 실무자 판단
1. **Filter Chain (필터 체인)**: 인증, CORS (Cross-Origin Resource Sharing), 압축 등을 필터로 조합
2. **Interceptor (인터셉터)**: preHandle / postHandle로 컨트롤러 전후 처리
3. **Exception Handler (예외 핸들러)**: `@ControllerAdvice`로 전체 예외를 중앙 처리
4. <strong>RESTful 라우팅</strong>: `/users/{id}` 같은 경로 변수 처리가 자연스럽다

- 레거시 시스템 유지보수
- 극단적으로 단순한 정적 사이트 (파일 서버 수준)
- PHP (Hypertext Preprocessor) 파일 기반 라우팅 (파일명 = URL)

"왜 Spring MVC는 프론트 컨트롤러를 채택했는가?" — 답은 <strong>관심사 분리 + 중복 제거</strong>다. 비즈니스 로직과 인프라 로직(인증, 로깅)을 섞지 않기 위해 단일 진입점을 두고 책임을 위임 체인으로 분산시켰다.

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 소규모 가게는 각 직원이 문도 열고 계산도 하지만, 대형 마트는 입구에 보안요원(프론트 컨트롤러)이 있고 각 코너(핸들러)는 상품 처리만 한다.

---

## Ⅴ. 기대효과 및 결론
프론트 컨트롤러 패턴 도입의 실질적 효과:

- **중복 코드 감소**: 인증 코드가 1개 필터로 통합 -> 서블릿 N개 × 인증 로직 제거
- **변경 영향 최소화**: 공통 정책(예: JWT -> Session 전환)을 한 곳만 수정
- **테스트 가능성**: MockMvc로 컨트롤러를 서블릿 컨테이너 없이 테스트
- <strong>REST API (Representational State Transfer Application Programming Interface) 지원</strong>: URL 패턴 매핑, HTTP 메서드 분기를 선언적으로 처리

현대 웹 개발에서 프론트 컨트롤러는 사실상 표준이다. Express.js (Node.js), Django (Python), Laravel (PHP) 모두 단일 진입점 구조를 채택한다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 모든 편지가 우체국 중앙 분류 센터를 거쳐 각 우체통으로 배달되듯, 프론트 컨트롤러는 모든 요청의 중앙 분류소다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | MVC 패턴 | 프론트/페이지 컨트롤러가 속하는 패턴 범주 |
| 하위 개념 | DispatcherServlet | Spring MVC의 Front Controller 구현체 |
| 하위 개념 | Handler Mapping | 요청 URL -> 핸들러 매핑 컴포넌트 |
| 연관 개념 | Filter / Interceptor | 공통 처리를 담당하는 프론트 컨트롤러 확장 |
| 연관 개념 | View Resolver | 논리 뷰명을 물리 경로로 변환 |
| 대조 개념 | Page Controller | 페이지별 개별 컨트롤러 패턴 |

### 📈 관련 키워드 및 발전 흐름도
웹 요청 진입점 -> 프론트 컨트롤러 vs 페이지 컨트롤러 -> API gateway/handler mapping

### 👶 어린이를 위한 3줄 비유 설명
1. 페이지 컨트롤러는 각 교실마다 선생님이 출석도 부르고 수업도 하는 거야.
2. 프론트 컨트롤러는 교장 선생님(Front Controller)이 학교 입구에서 모든 학생을 체크하고 교실로 안내하는 거야.
3. 교장이 한 명이니까, 규칙이 바뀌면 교장 선생님만 알려주면 모든 교실에 자동으로 적용돼!
