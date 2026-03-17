+++
title = "773. 3-Layer 아키텍처 (Presentation, Logic, Data)"
date = "2026-03-15"
weight = 773
[extra]
categories = ["Software Engineering"]
tags = ["Architecture", "3-Tier", "Presentation Layer", "Business Logic", "Data Layer", "Separation of Concerns"]
+++

# 773. 3-Layer 아키텍처 (Presentation, Logic, Data)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 시스템의 복잡도를 억제하기 위해 **Presentation (표현)**, **Business Logic (비즈니스 로직)**, **Data Persistence (데이터 영속성)**이라는 세 가지 논리적 관심사를 철저히 분리하여 계층화(Layered Architecture)하는 구조적 패턴입니다.
> 2. **가치**: **SoC (Separation of Concerns, 관심사의 분리)** 원칙을 통해 모듈 간 결합도(Coupling)를 낮추고 응집도(Cohesion)를 높여, UI 변경 시 비즈니스 규칙에 영향을 주지 않으며, 계층별 독립적인 **Scaling Out (수평 확장)**이 가능합니다.
> 3. **융합**: MVC(Model-View-Controller) 패턴이 프레젠테이션 내부의 구조라면, 3-Layer는 시스템 전체의 **N-Tier (다계층)** 물리 분배 기반이 되며, **MSA (Microservices Architecture, 마이크로서비스 아키텍처)**로 진화 시 각 서비스 내부의 표준 구조로 계승됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**3-Layer 아키텍처** (또는 3-Tier Architecture)는 소프트웨어를 기능적 역할에 따라 수평적으로 분할하여 배치하는 설계 패러다임입니다. 초기의 **Monolithic Architecture (모놀리식 아키텍처)**가 UI, 로직, 데이터가 하나의 실행 파일이나 프로세스에 밀집되어 유지보수가 어렵고 재사용성이 낮다는 한계를 극복하고자 등장했습니다. 이 패턴은 **계층(Layer)**이라는 상하위 개념을 도입하여, 상위 계층이 하위 계층의 서비스를 요청하고 그 결과를 받는 단방향 의존성을 강제합니다.

#### 2. 등장 배경 및 기술적 진화
① **기존 한계**: 1세대 웹 애플리케이션(CGI, ASP, JSP)에서는 HTML 코드 안에 DB 조회 쿼리와 업무 로직이 혼재되어, 디자이너와 개발자의 충돌 및 코드 중복(Duplication)이 심각했습니다.
② **혁신적 패러다임**: **Gang of Four (GoF)**의 디자인 패턴 영향과 객체 지향 프로그래밍(OOP)의 발전으로 인해 '책임의 분리'가 필수가 되었습니다. 이를 통해 로직을 UI 플랫폼(웹, 모바일, 데스크톱)으로부터 독립시키고자 했습니다.
③ **현재의 비즈니스 요구**: 클라우드 환경(Cloud Native)에서는 각 계층의 트래픽 패턴과 리소스 요구 사항이 다르므로, 이를 분리하여 독립적으로 **Auto-scaling (자동 확장)**할 수 있는 인프라가 필수적이 되었습니다.

#### 3. ASCII 다이어그램: 개념적 관점
아래 다이어그램은 각 계층이 가지는 '책임의 경계'를 시각화한 것입니다.

```text
       User Request
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (UI)                                         │
│  "나는 보여주고 입력받는 것이 전부이다."                          │
│  ├── View: 사용자에게 화면을 렌더링                              │
│  └── Controller: 사용자 입력을 해석하여 Logic 계층으로 전달       │
└─────────────────────────────────────────────────────────────────┘
             │ ▼ (DTO / Command Object)
┌─────────────────────────────────────────────────────────────────┐
│  LOGIC LAYER (Business Rules)                                    │
│  "나는 데이터의 가치을 판단하고 가공한다."                        │
│  ├── Service: 핵심 알고리즘 및 업무 처리(예: 할인율 계산)        │
│  └── Facade: 복잡한 하위 로직을 캡슐화하여 인터페이스 제공       │
└─────────────────────────────────────────────────────────────────┘
             │ ▼ (SQL / Repository Call)
┌─────────────────────────────────────────────────────────────────┐
│  DATA LAYER (Persistence)                                        │
│  "나는 데이터를 안전하게 저장하고 회수한다."                      │
│  ├── DAO/Data Access: DB 통신 인터페이스                         │
│  └── DBMS: 실제 데이터 저장소 (RDBMS, NoSQL)                     │
└─────────────────────────────────────────────────────────────────┘
```

> **해설**: 위 다이어그램은 각 계층을 둘러싼 박스가 '화학적 용기'와 같아서 외부와의 불필요한 반응(결합)을 차단한다는 것을 보여줍니다. Presentation은 '어떻게 보일지(View)'에만, Logic은 '무엇을 할지(Business Rule)'에만, Data는 '어떻게 저장할지(Persistence)'에만 집중하도록 캡슐화되어 있습니다.

#### 📢 섹션 요약 비유
마치 **'고급 레스토랑의 주방 시스템'**과 같습니다. 홀 직원(Presentation)은 주방장(Logic)이 요리하는 방법을 몰라도 주문을 받을 수 있어야 하며, 주방장은 창고(Data)에 재료가 얼마나 남았는지 구체적으로 몰라도 요리할 수 있어야 합니다. 서로의 역할이 분리되어 있어야 한쪽이 바빠도 다른 쪽은 일사불란하게 돌아갈 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 심층 분석 (Component Detail)
3-Layer 아키텍처의 핵심은 계층 간의 **인터페이스(Interface)**를 통해 느슨한 결합(Loose Coupling)을 유지하는 것입니다.

| 요소 (Element) | 전체 명칭 (Full Name) | 핵심 역할 | 주요 기술 스택 및 파라미터 |
|:---|:---|:---|:---|
| **UI Controller** | User Interface Controller | 클라이언트의 HTTP 요청을 수신하고, 파라미터 검증(Validation) 후 Service Layer로 호출 | Spring MVC `@Controller`, ASP.NET Core `Controller`, Express.js Router |
| **DTO** | Data Transfer Object | 계층 간 데이터 전송용 객체. 로직을 포함하지 않은 순수한 데이터 구조체 | Java POJO, C# Class, JSON Schema |
| **Service Interface** | Service Interface | 비즈니스 로직의 계약(Contract) 명세. 다형성(Polymorphism) 보장 지점 | Java `interface`, C# `interface`, Type Definition |
| **Domain Model** | Domain Business Logic | 실제 업무 규칙(예: 재고 계산, 이자 적립)을 수행하는 순수 로직 영역 | POJO, Entity, Domain Object |
| **Repository** | Data Access Repository | DB와의 세션을 관리하고, CRUD(Create, Read, Update, Delete) 작업 수행 | JPA `Repository`, MyBatis `Mapper`, DAO Pattern |

#### 2. 계층 간 통신 메커니즘 (Communication Flow)
데이터의 흐름은 **Request (요청)**와 **Response (응답)**로 나뉘며, 직렬화(Serialization) 과정을 거칩니다.

1. **요청 (Downward Flow)**: Client → HTTP Request → **Controller** (DTO 변환) → **Service** (전달) → **Repository** (SQL 생성) → DB
2. **응답 (Upward Flow)**: DB → ResultSet → **Repository** (Entity 매핑) → **Service** (가공) → **Controller** (JSON 직렬화) → Client

#### 3. ASCII 다이어그램: 데이터 흐름 및 의존성
아래는 사용자가 '주문 조회'를 요청했을 때의 내부 동작 시퀀스입니다.

```text
   [ CLIENT BROWSER ]
          │ ① GET /orders/123
          ▼
┌───────────────────────────────────────────────────┐
│ Presentation Layer                                 │
│ (Controller)                                       │
│ ② DTO { orderId: 123 } 생성 및 전달                │
└────────────────────┬──────────────────────────────┘
                     │ ▼
┌────────────────────▼──────────────────────────────┐
│ Logic Layer (Service)                              │
│ ③ DTO를 기반으로 도메인 로직 실행                  │
│    예: "해당 주문에 대한 배송비 계산 로직 수행"      │
└────────────────────┬──────────────────────────────┘
                     │ ▼
┌────────────────────▼──────────────────────────────┐
│ Data Layer (Repository)                            │
│ ④ SELECT * FROM ORDERS WHERE ID = 123             │
│    DB Cursor 획득 -> Entity Object Mapping         │
└────────────────────┬──────────────────────────────┘
                     │ ▼
               [ DATABASE ]
                     │ ▲ (Return Entity)
┌────────────────────┴──────────────────────────────┐
│ Data Layer                                        │
│ ⑤ Entity -> Service로 반환                        │
└────────────────────┬──────────────────────────────┘
                     │ ▲
┌────────────────────┴──────────────────────────────┐
│ Logic Layer                                       │
│ ⑥ Service Logic 처리 완료 -> 결과 DTO 생성        │
└────────────────────┬──────────────────────────────┘
                     │ ▲
┌────────────────────┴──────────────────────────────┐
│ Presentation Layer                                │
│ ⑦ DTO -> JSON Serialization -> HTTP 200 Response  │
└───────────────────────────────────────────────────┘
```

> **해설**: 이 다이어그램은 **의존성 역전(Dependency Inversion)** 원칙을 암시합니다. 상위 계층이 하위 계층을 호출하지만, 하위 계층은 인터페이스를 통해 상위의 추체화된 요구사항에 의존하게 됩니다. 실무적으로 중요한 점은 **Presentation Layer가 Data Layer에 대한 지식이 전혀 없어야 한다**는 것입니다. 즉, Controller에서 직접 SQL을 작성하거나 DB Connection을 맺는 것은 안티패턴(Anti-pattern)입니다.

#### 4. 핵심 알고리즘 및 코드 예시 (Java/Spring 기준)

```java
// [Presentation Layer] - 사용자 요청 처리
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @Autowired
    private OrderService orderService; // Logic Layer 의존성만 가짐

    // 클라이언트는 DB 구조를 몰라도 DTO만 받음
    @GetMapping("/{id}")
    public Response<OrderResponseDTO> getOrder(@PathVariable Long id) {
        // 1. DTO 변환 및 전달
        return Response.ok(orderService.findOrderById(id));
    }
}

// [Logic Layer] - 비즈니스 규칙 처리
@Service
@Transactional
public class OrderServiceImpl implements OrderService {

    @Autowired
    private OrderRepository orderRepository; // Data Layer Interface 의존

    @Override
    public OrderResponseDTO findOrderById(Long id) {
        // 2. 데이터 조회
        OrderEntity entity = orderRepository.findById(id)
                              .orElseThrow(() -> new BusinessEx("Not Found"));
        
        // 3. 비즈니스 로직 (예: 사용자 권한에 따른 가격 마스킹)
        if (!CurrentUser.isAdmin()) {
            entity.hideSensitiveData();
        }
        
        // 4. DTO로 변환하여 반환
        return new OrderResponseDTO(entity);
    }
}

// [Data Layer] - 데이터 접근 관심사
@Repository
public interface OrderRepository extends JpaRepository<OrderEntity, Long> {
    // DB에 종속적인 쿼리는 여기서 숨김 (Hibernate, JPA 등이 처리)
}
```

#### 📢 섹션 요약 비유
마치 **'자동차 공장의 컨베이어 벨트'**와 같습니다. 조립(Logic)을 하는 작업자는 부품이 어느 창고(Data)에서 왔는지, 완성차가 누구에게 팔릴지(Presentation) 몰라도 됩니다. 각 공정(계층)이 정해진 **인터페이스(부품 전달 주머니)**를 통해 물품만 주고받으면, 공장 전체의 효율이 최적화되는 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 3-Layer vs MVC vs Clean Architecture

| 비교 항목 | **3-Layer Architecture** | **MVC (Model-View-Controller)** | **Clean Architecture (Onion)** |
|:---|:---|:---|:---|
| **관심사 범위** | **전체 시스템** 아키텍처 | 주로 **Presentation Layer** 내부의 구조 | 전체 시스템의 **의존성 방향** 규정 |
| **주 목적** | 물리적 분리 및 배포 단위 분리 | UI 로직과 비즈니스 로직의 분리 (단일 계층 내) | 프레임워크, DB, UI로부터 도메인 로직 보호 |
| **데이터 흐름** | 상단(상위)에서 하단(하위)으로의 **단방향** 흐름 강제 | Model이 View와 Controller에 의존하거나 통신하는 **양방향** 가능 | 외부(Ring)가 내부(Core)를 의존하는 **내부 집중** 흐름 |
| **의존성** | 하위 계층(DB)이 상위 계층에 영향을 줄 수 있음 | Model(데이터)이 View를 업데이트함 | 도메인(Core)이 가장 중심, 외부 변화로부터 자유로움 |

#### 2. ASCII 다이어그램: MVC와의 관계
아래 다이어그램은 MVC 패턴이 3-Layer 아키텍처의 **Presentation Layer 내부**에 위치하는 경우를 보여줍니다.

```text
┌────────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           MVC Pattern Implementation                     │  │
│  │                                                          │  │
│  │  [ VIEW ] ────────▶ [ CONTROLLER ] ────────▶ [ MODEL ]   │  │
│  │    ▲                                   │                 │  │
│  │    │                                   ▼                 │  │
│  │    │                        (DTO transfer)                │  │
│  │    │                                    │                 │  │
│  └────┴────────────────────────────────────┘                 │  │
└──────────────────────────────┬───────────────────────────────┘
                               │ ▼ (Service Call)
┌──────────────────────────────▼───────────────────────────────┐
│                  LOGIC LAYER (Service)                        │
└──────────────────────────────┬───────────────────────────────┘
                               │ ▼
┌──────────────────────────────▼───────────────────────────────┐
│                  DATA LAYER (DAO/DB)                          │
└───────────────────────────────────────────────────────────────┘
```

> **해설**: Spring MVC와 같은 웹 프레임워크를 사용할 때, `@Controller`와 `View`를 포함한 웹 모듈이 Presentation Layer가 됩니다. 이때 MVC의 Model은 DB의 Entity가 아닌 **DTO(Data Transfer Object)**