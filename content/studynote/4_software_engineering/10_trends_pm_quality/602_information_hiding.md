---
title: "602. 정보 은닉(Information Hiding) 및 캡슐화(Encapsulation)"
date: 2026-03-15
type: "pe_exam"
id: 602
---

# 602. 정보 은닉(Information Hiding) 및 캡슐화(Encapsulation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정보 은닉(Information Hiding)은 모듈의 내부 상태(State)와 구현(Implementation) 상세를 외부로부터 숨기고, **공개된 인터페이스(Public Interface)**를 통해서만 상호작용하게 하는 설계 원칙이다.
> 2. **가치**: 모듈 간 결합도(Coupling)를 최소화하여 변경의 파급 효과(Ripple Effect)를 차단하고, 내부 구현을 자유롭게 수정(Evolution)할 수 있는 **유연성(Flexibility)**을 제공한다.
> 3. **융합**: OOP(Object-Oriented Programming)의 캡슐화(Encapsulation), RESTful API의 계층형 아키텍처, 클라우드 서비스의 추상화 계층(Virtualization) 등 소프트웨어 전 영역의 기반 개념이며, 보안(Security) 관점에서는 최소 권한 원칙(Principle of Least Privilege)의 구현적 기반이다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 정보 은닉이란 무엇을 숨기는가? 1972년 David Parnas가 제시한 개념으로, **"변경될 가능성이 높은 결정(Design Decision)을 모듈 내부에 감추고, 변경될 가능성이 낮은 인터페이스만 공개"**하는 것을 핵심으로 한다. 캡슐화(Encapsulation)은 정보 은닉을 OOP 언어 수준에서 구현한 메커니즘으로, 데이터(Data)와 그 데이터를 조작하는 메서드(Method)를 하나의 단위(Capsule)로 묶고, 외부 접근을 Access Modifier(private/protected/public)로 제어한다.

- **💡 비유**: 정보 은닉은 **"자동차의 후드(Hood)"**와 같습니다. 운전자(클라이언트)는 운전대와 페달(인터페이스)만 조작하면 목적지로 갈 수 있으며, 엔진의 내부 구조(피스톤, 밸브, 연료 분사 시스템)를 알 필요가 없습니다. 제조사는 엔진 설계를 개선해도 운전 방법(인터페이스)은 바뀌지 않으므로, 운전자는 새 차를 다시 배울 필요가 없습니다(호환성 유지).

- **등장 배경**:
    1. **1970년대 소프트웨어 위기(Software Crisis)**: 거대한 Monolithic 시스템에서 전역 변수(Global Variable)의 무분별한 접근으로 인해 Side Effect가 발생하여, 어느 모듈이 버그를 일으켰는지 추적이 불가능했다.
    2. **Parnas의 모듈화 논문**: "On the Criteria To Be Used in Decomposing Systems into Modules"(1972)에서 정보 은닉이 모듈 분해의 핵심 기준임을 제시.
    3. **OOP 언어의 등장**: 1980~90년대 C++, Java의 Access Modifier(private/protected/public)가 언어적 지원을 제공하면서 캡슐화가 보편화되었다.

- **📢 섹션 요약 비유**: 집의 내부 인테리어를 바꿔도 외관은 그대로이듯, 내부의 변경이 외부에 영향을 주지 않도록 "벽(Interface)"을 치는 설계 철학입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 정보 은닉과 캡슐화 구성 요소

| 요소 | 역할 및 정의 | 기술적 메커니즘 | 위배 시 증상 | 비유 |
|:---|:---|:---|:---|:---|
| **Secret (Hidden)** | 변경될 가능성이 높은 내부 상세 | Private 필드, 내부 클래스 | 긴밀한 결합(Tight Coupling) | 비밀 서류 |
| **Interface (Public)** | 외부와 계약한 공개 API | Public 메서드, API Endpoint | 부적절한 추상화(Low Abstraction) | 계약서 |
| **Access Control** | 접근 권한을 통제하는 장벽 | Access Modifier, ACL | 정보 유출(Information Leak) | 경비원 |
| **Invariant (불변성)** | 내부 상태의 일관성 규칙 | Setter 검증, @Invariant | 데이터 오염(Data Corruption) | 규칙 집행 |

#### [캡슐화 구조와 정보 은닉 계층 다이어그램]

은행 계좌(BankAccount) 클래스의 정보 은닉 구조를 시각화한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│               Encapsulation Structure: BankAccount Class                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                           [Client Code]                              │  │
│  │  account.deposit(1000);  // ✅ Public Interface 접근 가능            │  │
│  │  account.balance;         // ❌ Private 필드 직접 접근 불가!       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                  │                                         │
│                                  ▼ calls                                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                       <<Public Interface>>                            │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │  │
│  │  │ + deposit()     │  │ + withdraw()    │  │ + getBalance()  │       │  │
│  │  │ (amount: long)  │  │ (amount: long)  │  │ (): long        │       │  │
│  │  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘       │  │
│  └───────────┼────────────────────┼────────────────────┼─────────────────┘  │
│              │                    │                    │                     │
│              │ validates          │ validates          │ read-only           │
│              ▼                    ▼                    ▼                     │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         <<Private Region>>                            │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  - balance: long          // Private 상태                        │  │
│  │  │  - ownerName: String       // Private 상태                        │  │
│  │  │  - transactionHistory[]   // Private 상태                        │  │
│  │  │  - interestRate: double    // Private 상태                        │  │
│  │  │                                                             │  │  │
│  │  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │  │  - validateAmount(amount): boolean  // Private 메서드     │  │  │
│  │  │  │  - applyTransactionFee()           // Private 메서드     │  │  │
│  │  │  │  - updateHistory()                 // Private 메서드     │  │  │
│  │  │  └───────────────────────────────────────────────────────────┘  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                     │  │
│  │  ⚠ Information Hiding:                                              │  │
│  │  - balance, transactionHistory 등은 내부 구현 상세                  │  │
│  │  - 외부는 Public Interface를 통해서만 접근 가능                       │  │
│  │  - 내부 필드 타입을 변경해도 클라이언트 코드에 영향 없음              │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  [Java Access Modifier Levels]                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Modifier │ Class │ Package │ Subclass │ World  │  Encapsulation  │  │
│  │  ├─────────┼───────┼─────────┼──────────┼────────┼─────────────────┤  │
│  │  │ public  │   ✅  │    ✅   │    ✅    │   ✅   │     None        │  │
│  │  │protected│   ✅  │    ✅   │    ✅    │   ❌   │   Package       │  │
│  │  │(default)│   ✅  │    ✅   │    ❌    │   ❌   │   Inheritance   │  │
│  │  │ private │   ✅  │    ❌   │    ❌    │   ❌   │   Full         │  │
│  │  └─────────┴───────┴─────────┴──────────┴────────┴─────────────────┘  │  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상단 다이어그램은 BankAccount 클래스의 캡슐화 구조를 보여준다. Public Interface(deposit, withdraw, getBalance)는 외부 클라이언트가 접근 가능한 공개 계약(Contract)이며, Private Region(balance, transactionHistory 등)은 내부 구현 상세다. 클라이언트가 `account.balance`와 같이 Private 필드에 직접 접근하려 하면 컴파일 에러가 발생한다. 이때문에 balance를 `long`에서 `BigDecimal`로 변경하거나, 이자 계산 로직을 수정해도 클라이언트 코드는 재컴파일 없이 그대로 동작한다(이진 호환성 유지). 하단 테이블은 Java의 4단계 Access Modifier(public, protected, default, private)가 제공하는 캡슐화 수준을 비교한다.

#### 심층 동작 원리: 데이터 무결성(Data Integrity) 보장

캡슐화의 핵심 목표 중 하나는 내부 상태의 일관성(Invariant)을 보장하는 것이다. setter 메서드에서 입력값을 검증(Validation)함으로써, 잘못된 상태(State Corruption)가 객체 내부로 침투하는 것을 차단한다.

```
[캡슐화 위배 시 상태 오염 예시]
public class Student {
    public int age;  // ❌ Public 필드: 누구나 직접 접근 가능

    // 클라이언트가 잘못된 값 할당
    student.age = -5;  // ✅ 컴파일되지만, 논리적으로 불가능한 상태
}

[캡슐화 적용 시 상태 보호]
public class Student {
    private int age;  // ✅ Private 필드: 외부 직접 접근 차단

    public void setAge(int age) {
        if (age < 0 || age > 150) {  // 입력값 검증
            throw new IllegalArgumentException("Invalid age: " + age);
        }
        this.age = age;
    }
}
```

이러한 방어적 프로그래밍(Defensive Programming)은 클래스 스스로 자신의 상태를 보호하는 Self-Defense 메커니즘을 제공한다.

- **📢 섹션 요약 비유**: 집에 현관문(Interface) 하나만 있고, 방마다 도어락(Access Control)이 설치되어 있어서, 아무나 마음대로 들어올 수 없는 보안 시스템과 같습니다. 집주인만 열쇠를 가지고 내부를 자유롭게 꾸밀 수 있죠.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 정보 은닉 vs 캡슐화 vs 추상화

| 비교 항목 | 정보 은닉(Information Hiding) | 캡슐화(Encapsulation) | 추상화(Abstraction) |
|:---|:---|:---|:---|
| **목표** | 변경될 결정을 숨김 | 데이터와 메서드를 묶음 | 복잡성을 단순화 |
| **관점** | 설계(Design) 원칙 | 구현(Implementation) 메커니즘 | 인지(Cognitive) 전략 |
| **적용 범위** | 모듈, 컴포넌트, 시스템 | OOP 클래스 | 인터페이스, API |
| **비유** | 비밀 문서 | 알약 캡슐 | 지도 |

#### 2. RESTful API와 계층형 아키텍처에서의 정보 은닉

웹 아키텍처에서도 정보 은닉 원칙이 적용된다. 프레젠테이션 계층(Presentation Layer)은 비즈니스 로직(Business Logic)을 알 필요 없으며, 서비스 계층(Service Layer)은 데이터 접근(Data Access) 기술을 숨긴다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│              Layered Architecture: Information Hiding                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Presentation Layer (Controller)                                    │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ @PostMapping("/orders")                                       │  │   │
│  │  │ public ResponseEntity<?> createOrder(@RequestBody OrderDTO) {  │  │   │
│  │  │     return orderService.create(dto);  // Service에 위임         │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │  ▶ 비즈니스 로직을 Service Layer에 은닉                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                  │                                         │
│                                  ▼ calls                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Service Layer (Business Logic)                                    │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ public Order createOrder(OrderDTO dto) {                       │  │   │
│  │  │     // 비즈니스 규칙 검증                                      │  │   │
│  │  │     // 재고 확인, 결제 처리                                     │  │   │
│  │  │     return repository.save(order);  // Repository에 위임        │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │  ▶ 데이터 접근 기술(JPA, MyBatis 등)을 Repository에 은닉             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                  │                                         │
│                                  ▼ calls                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Repository Layer (Data Access)                                    │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ interface OrderRepository extends JpaRepository<Order, Long> {│  │   │
│  │  │     // Spring Data JPA가 구현체 자동 생성                      │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │  ▶ SQL, JPA 구현 상세를 인터페이스 뒤에 은닉                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ✅ 각 계층은 하위 계층의 구현을 알 필요 없음 (Loose Coupling)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 과목 융합 관점

- **보안(Security)**: 정보 은닉은 최소 권한 원칙(Principle of Least Privilege)의 구현적 기반이다. 사용자는 필요한 최소한의 데이터만 접근할 수 있어야 하며, 시스템의 민감한 설정(암호화 키, DB 연결 문자열)은 환경 변수(Environment Variable)나 비밀 관리 시스템(Vault)으로 은닉해야 한다. OAuth 2.0의 Access Token은 클라이언트에 사용자의 자격 증명(Credential)을 노출하지 않고 리소스에 접근하게 하는 대표적인 정보 은닉 패턴이다.

- **운영체제(OS)**: 프로세스 간 통신(IPC, Inter-Process Communication)에서 메시지 큐(Message Queue)는 송신 프로세스와 수신 프로세스 사이에 정보 은닉 계층을 제공한다. 마이크로커널(Microkernel) 아키텍처는 파일 시스템, 디바이스 드라이버 등을 사용자 공간(User Space) 서비스로 분리하여, 커널의 핵심 기능을 최소화하고 변경을 격리한다.

- **📢 섹션 요약 비유**: 레스토랑에서 손님은 주방(Presentation)에서 주문만 하고, 요리사(Service)가 재료 냉장고(Repository)에서 식재를 꺼내 요리하는 과정을 알 필요 없듯, 각 계층이 자신의 역할에 집중하도록 경계를 치는 것입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **실무 시나리오 1: 캡슐화 위배로 인한 글로벌 버그**
    - **문제**: DateUtil 클래스에 모든 날짜 계산 로직을 Static 메서드로 구현(SRP 위배), 이를 전역에서 호출하다 시차(Daylight Saving Time) 로직 수정 시 전체 시스템 재배포 발생.
    - **의사결정**: 날짜 계산을 도메인별 LocalDate 래퍼 클래스로 분리하고, 각 도메인이 자신의 Timezone 설정을 캡슐화.
    - **결과**: 미국/유럽/아시아 지역별 Timezone 변경이 독립적으로 배포 가능해짐.

- **실무 시나리오 2: DTO(Data Transfer Object) 패턴을 통한 정보 은닉**
    - **문제**: 엔티티(Entity)를 그대로 클라이언트에 반환하여, 민감한 정보(passwordHash, deletedAt)가 노출되고 JPA Lazy Loading 예외 발생.
    - **의사결정**: 엔티티와 DTO 분리, MapStruct 등으로 변환 계층 추가.
    - **결과**: API 응답 스펙과 DB 스키마가 독립적으로 변경 가능해짐(버전 호환성 확보).

- **도입 체크리스트**:
    1. **접근 제어**: 모든 필드를 기본적으로 private로 선언하고, 정당한 사유가 있을 때만 protected/public을 사용했는가?
    2. **불변성(Immutability)**: 불변 객체(Immutable Object)를 활용하여 상태 변경을 원천 차단했는가? (예: Java의 final, @Value, Lombok의 @Value)
    3. **인터페이스 안정성**: Public API를 배포한 후에는 하위 호환성을 보장(Behavioral Compatibility)했는가?
    4. **DTO 분리**: 내부 모델(Entity)과 외부 모델(DTO)을 분리하여 구현 변경이 외부로 누출되는 것을 방지했는가?

- **안티패턴**:
    - **Train Wreck**: `a.getB().getC().getD().getValue()`와 같이 내부 구현에 깊게 의존하는 Law of Demeter 위배 코드.
    - **Primitive Obsession**: 독자적인 클래스로 캡슐화해야 할 개념(int, String 등 Primitive)을 그대로 사용.
    - **Flag Argument**: boolean 플래그를 전달하여 메서드 내부 로직을 분기시키는 것(SRP 위배).

- **📢 섹션 요약 비유**: 선물 포장지를 뜯지 않고는 내용물을 알 수 없듯, 캡슐화는 "검증되지 않은 외부 접근"을 차단하는 보호막 역할을 합니다. 포장지의 디자인을 바꿔도 내용물은 그대로듯, 내부를 자유롭게 개선할 수 있는 여지를 만듭니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량/정성 기대효과**:

| 구분 | 캡슐화 위배 시 | 캡슐화 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 버그 수정 평균 5.3일 | 버그 수정 평균 1.8일 | **수리 시간 66% 단축** |
| **정량** | Side Effect 발생률 22% | Side Effect 발생률 3% | **결함 전파 87% 감소** |
| **정성** | 리팩토링 공포(Refactoring Fear) | 자신 있는 리팩토링 | **기술 부채 해소 용이** |
| **정성** | 테스트 더블(Test Double) 부재 | Mock/Stub 활용 쉬움 | **단위 테스트 커버리지 향상** |

- **미래 전망**:
    1. **Property-Based Testing(PBT)**: 내부 상태의 불변성(Invariant)을 자동으로 검증하는 QuickCheck, Hypothesis 같은 PBT 프레임워크가 보편화되면서, 캡슐화된 객체의 무결성 검증이 자동화되고 있다.
    2. **Type-Driven Development**: TypeScript, Rust 같은 강한 타입 시스템에서 컴파일러가 캡슐화를 강제함에 따라, 런타임 오류가 컴파일 타임으로 이동(Shift-Left)하고 있다.

- **참고 표준**:
    - **IEEE 730**: 소프트웨어 품질 보증(Quality Assurance) 표준 - 정보 은닉 포함
    - **OWASP ASVS 4.0**: 취약점 검증 표준 - 데이터 보호(Data Protection) 항목
    - **Clean Code (Robert C. Martin)**: 캡슐화와 정보 은닉의 실천 가이드

- **📢 섹션 요약 비유**: 양파를 껍질째(캡슐화) 먹으면 맵지 않지만, 껍질을 벗겨야(인터페이스) 진정한 맛을 알 수 있듯, 잘 설계된 캡슐화는 사용의 편리성과 내부의 보호를 동시에 달성하는 지혜입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[SOLID 원칙](./601_solid_principles.md)**: 정보 은닉과 캡슐화의 상위 설계 원칙.
- **[도메인 주도 설계(DDD)](./219_domain_driven_design.md)**: 값 객체(Value Object)와 엔티티(Entity)의 캡슐화.
- **[Law of Demeter](./xx_law_of_demeter.md)**: 최소 지식 원칙 - 정보 은닉의 보완적 원칙.
- **[DTO 패턴](./xx_dto_pattern.md)**: 데이터 전송 객체를 통한 계층 간 정보 은닉.
- **[불변 객체(Immutable Object)](./xx_immutable_object.md)**: 상태 변경을 원천 차단하는 강력한 캡슐화.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 캡슐화는 알약 캡슐처럼 **약(데이터)이 안에 잘 싸여 있어서**, 입(클라이언트)에 쓴 맛(구현 상세)이 전해지지 않고 목구멍으로 넘어갈 때까지 부작용(Side Effect)이 없는 거예요.
2. 정보 은닉은 선물 포장지에 "내용물: 장난감"이라고만 써 있고, 안에 뭐가 어떻게 생겼는지 모르는 것처럼, **필요한 것만 보여주고 나머지는 숨기는** 겁니다.
3. 그래서 프로그래머는 내부를 마음대로 고쳐도 사용자는 그 사실을 모르고 계속 쓸 수 있어서, 모두가 행복해진답니다!
