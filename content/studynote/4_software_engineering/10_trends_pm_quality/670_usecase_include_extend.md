+++
title = "670. 유스케이스 포함(Include) 확장(Extend)"
date = "2026-03-15"
weight = 670
+++

# 670. 유스케이스 포함(Include) 확장(Extend)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **UML (Unified Modeling Language)**의 유스케이스 다이어그램에서 기능적 요구사항 간의 **논리적 의존성**을 정의하는 메커니즘으로, 시스템의 복잡성을 제어하고 모듈의 재사용성을 극대화하는 핵심 설계 패턴이다.
> 2. **구조적 차이**: `<<include>>`는 기본 유스케이스 실행을 위해 **필수적(Mandatory)**인 하위 기능을 분리하는 것이며, `<<extend>>`는 특정 조건에서 **선택적(Optional)**으로 발생하는 부가 기능이나 예외 상황을 독립시키는 전략이다.
> 3. **설계 가치**: 이 두 관계를 적절히 활용함으로써 **DRY (Don't Repeat Yourself)** 원칙을 준수하여 중복을 제거하고, 단일 책임 원칙(SRP)에 기반하여 변경 영향도를 최소화하는 유지보수성 높은 요구사항 모델을 설계할 수 있다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**유스케이스(Use Case)** 모델링은 이바 야콥슨(Ivar Jacobson)이 제안한 **OOSE (Object-Oriented Software Engineering)** 방법론의 핵심 요소로, 시스템의 내부 구조가 아닌 **행위자(Actor)**의 관점에서 시스템이 제공하는 가치를 정의한다.
여기서 **포함(Include)**과 **확장(Extend)** 관계는 복잡한 유스케이스 간의 연결을 구조화하기 위한 수단이다.
- **Include**: "A를 하려면 B가 무조건 필요하다"는 **强制的 의존성**을 표현한다. (예: 로그인 필요한 인증 기능)
- **Extend**: "A를 하는 도중 C라는 조건이 되면 D를 할 수 있다"는 **조건부 분기**를 표현한다. (예: 결제 중 할인 쿠폰 적용)

#### 2. 등장 배경 및 필요성
① **중복의 문제**: 여러 유스케이스에서 동일한 로그인, 인증, 로깅 과정이 반복되면 변경 시 유지보수 비용이 기하급수적으로 증가한다.
② **복잡도 관리**: 하나의 거대한 유스케이스에 모든 예외 상황과 부가 기능을 포함하면 가독성이 떨어지고 이해관자별 요구사항을 분리하기 어렵다.
③ **변경의 파급**: 시스템 요구사항은 변하기 마련이다. 포함과 확장을 통해 변동성이 큰 모듈(확장)과 안정적인 모듈(포함)을 분리하여 시스템의 유연성을 확보해야 한다.

#### 3. UML 표기법 시각화 (Structure)

```text
      [ Base Use Case ] 
            │
            │  1. <<include>>
            ├──────────────────────────▶ [ Included Use Case ]
            │  (Required)               (Mandatory Execution)
            │
            │  2. <<extend>>
            ◀───────────────────────────  [ Extending Use Case ]
       (Extension Points)              (Conditional Execution)
```
*   **해설**:
    *   **<<include>>**: 기본 유스케이스(Base)가 피포함 유스케이스(Included)를 호출한다. 화살표 방향은 의존하는 방향(기본 → 포함)을 가리킨다.
    *   **<<extend>>**: 확장 유스케이스(Extending)가 기본 유스케이스(Base)의 동작을 침범하여 기능을 추가한다. 화살표 방향은 확장 → 기본을 가리킨다.

> **📢 섹션 요약 비유**:
> 유스케이스 설계는 **'전자제품 설계서'**를 작성하는 것과 같습니다.
> **포함(Include)**은 TV를 켤 때 **'반드시 전원이 연결되어야 하는'** 내부 회로 연결과 같고, **확장(Extend)**은 필요에 따라 **'선택적으로 연결할 수 있는'** HDMI 케이블이나 외부 스피커와 같습니다. 기본 기능에 꼭 필요한 부분은 포함으로, 상황에 따라 추가되는 기능은 확장으로 정의하여 설계의 논리를 명확히 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 세부 구성 요소 분석 (Component Analysis)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/조건 (Protocol) | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **Base Use Case** (기본 유스케이스) | 시스템의 핵심 사용 흐름 정의 | Actor의 직접적인 목표를 달성하는 메인 로직 수행 | Include 관계 시 피포함 UC 호출 조건 생성 | 식당의 '메인 요리' |
| **Included Use Case** (피포함 UC) | 공통 히여사항 제공 | 기본 UC로부터 제어권을 넘겨받아 로직 실행 후 복귀 | 항상 실행됨 (무조건적 의존) | '식사 전 손 씻기' (필수) |
| **Extending Use Case** (확장 UC) | 부가 기능 또는 예외 처리 | 특정 Extension Point에서 조건을 확인하여 로직 삽입 | `guard condition`이 `true`일 때만 실행 | '식사 후 커피 마시기' (선택) |
| **Extension Point** (확장 지점) | 확장이 삽입될 위치 명시 | 기본 흐름 중 확장 UC가 개입할 단계를 정의 | 명시된 단계(Step)에서만 삽입 가능 | '식사가 끝나는 시점' |

#### 2. 포함(Include) 관계의 심층 메커니즘

포함 관계는 **재사용성(Reusability)**을 극대화하기 위해 사용된다. 여러 유스케이스에서 동일하게 반복되는 로직(예: 인증, DB 로깅, 유효성 검사)을 별도의 유스케이스로 분리한다.

```text
+-----------------------------------------------------+
|                [ 계좌 이체 (Transfer Funds) ]       |
|                                                     |
|  1.本金入力 (Input Amount)                          |
|  2. ┌──────────────────────────────────────────┐   |
|     │ <<include>>                              │   |
│     └─▶ [ 인증 확인 (Authenticate User) ]       │   |
│          (ID/PW Check, Session Valid)           │   |
│  3. └──────────────────────────────────────────┘   |
│     (Returns Success/Failure)                      │
│  4. Execute Transaction                            │
+-----------------------------------------------------+
```
*   **해설**: `계좌 이체` 유스케이스는 성공하기 위해 `인증 확인`이라는 기능을 **반드시** 거쳐야 한다. 만약 `인증 확인` 로직이 변경되더라도(예: 생체 인증 추가), 이를 포함하는 모든 유스케이스(이체, 조회, 해지 등)를 수정할 필요 없이 `인증 확인` 유스케이스 하나만 수정하면 된다. 이는 **Composite Pattern**의 구조적 이점과 일맥상통한다.

#### 3. 확장(Extend) 관계의 싱층 메커니즘

확장 관계는 **유연성(Flexibility)**과 **선택적 행위(Optional Behavior)**를 표현한다. 기본 유스케이스의 복잡성을 줄이기 위해, 특정 조건(Guard Condition)에서만 발생하는 로직을 분리한다.

```text
[ 상품 결제 (Process Payment) ]        [ 사은품 증정 (Add Free Gift) ]
                ▲                                   │
                │                                   │
                │           <<extend>>             │
                └───────────────────────────────────┘
                  (Condition: Total Amount > $100)
                  (Insert Point: After Payment Success)
```
*   **해설**: `상품 결제`는 그 자체로 완결성을 가진다. 하지만 결제 금액이 100달러를 넘는(Condition) 경우에만 `사은품 증정`이라는 행위가 뒤따른다. 확장 관계는 기본 흐름에 영향을 주지 않으면서 기능을 **'플러그인(Plugin)'** 형태로 추가하는 개념이다.

#### 4. 핵심 설계 원칙 (Best Practices)

> **"Include is about IS-A relationship of behavior; Extend is about CAN-BE relationship of behavior."**

- **Include 적용 기준**:
    1.  중복되는 로직이 최소 2곳 이서 발생할 때
    2.  해당 로직이 없으면 기본 기능이 논리적으로 완료되지 않을 때
- **Extend 적용 기준**:
    1.  기본 흐름을 복잡하게 만드는 예외 상황(Exception)이나 오류(Error) 처리일 때
    2.  향후 추가될 가능성이 높은 옵션 기능(Optional Feature)일 때

> **📢 섹션 요약 비유**:
> 포함(Include)과 확장(Extend)의 차이는 **'도시의 수도관'**과 같습니다.
> **포함**은 모든 가정집으로 물을 공급하는 **'주배관(Main Line)'**으로서, 이것이 없으면 생존 자체가 불가능한 필수 연결입니다. 반면, **확장**은 주배관에서 뻗어나오는 **'세탁기 전용 호스'**와 같습니다. 세탁기(확장 UC)는 필요할 때만 연결(extend)되며, 꽂히지 않아도 수도 시스템(기본 UC)은 정상 작동합니다. 시스템의 '생존 여부'가 아니라 '편의성/부가 기능'을 결정할 때 확장을 사용합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 포함(Include) vs 확장(Extend) 심층 비교 분석

| 비교 항목 | 포함 (`<<include>>`) | 확장 (`<<extend>>`) |
|:---|:---|:---|
| **의존성 방향** | Base → Included (Base가 Included에 의존) | Extending → Base (Extending이 Base에 의존) |
| **실행 조건** | **无条件** (Unconditional) | **有条件** (Conditional, Guard Condition) |
| **필수 여부** | **필수** (Without it, Base is incomplete) | **선택** (Without it, Base is complete) |
| **목적** | 중복 코드 제거 (De-duplication) | 예외 처리/기능 추가 (Feature Extension) |
| **OOP 패턴 연계** | Composition (Has-a 관계) | Decorator Pattern (기능 장식) |
| **비유** | 자동차의 엔진 (없으면 못 감) | 자동차의 네비게이션 (없어도 감) |

#### 2. SW 아키텍처 및 코드(C++) 구현 관점의 융합

유스케이스 관계는 곧 소프트웨어의 **제어 흐름(Control Flow)**과 **모듈 결합도(Coupling)**로 이어진다.

```cpp
// [C++ Pseudo Code: Include Relationship]
class PaymentSystem {
public:
    void processPayment() {
        // 1. Authentication (Included Use Case)
        // processPayment()는 Authenticates 객체의 메서드를 '반드시' 호출해야 함.
        if (!authenticator->verifyUser()) { 
            throw SecurityException(); 
        }
        
        // 2. Core Logic
        chargeCreditCard();
    }
private:
    Authenticator* authenticator; // Composition (Strong coupling)
};

// [C++ Pseudo Code: Extend Relationship]
class NotificationSystem {
public:
    void onPaymentSuccess() {
        sendSMS();
        
        // 3. Promotional Notification (Extending Use Case)
        // 조건에 부합할 때만 promoSender->send()가 실행됨.
        if (user->hasSubscription()) {
            promoSender->sendPromo(); // Optional logic
        }
    }
};
```
*   **기술적 해설**:
    *   `<<include>>`는 `PaymentSystem` 클래스가 `Authenticator`를 **강하게 결합**되어 소유(Composition)하는 형태로 구현된다.
    *   `<<extend>>`는 `NotificationSystem`이 `PromoSender`를 **느슨하게 결합**되어 호출하거나, 이벤트 드리븐 방식(Event-Driven)으로 뒤늦게 연결되는 형태이다.
    *   이는 **AOP (Aspect-Oriented Programming)**의 횡단 관심사(Cross-cutting Concern)와도 연결된다. 로깅이나 보안(Include)은 핵심 로직에 깊숙이 관여하며, UI 테마 변경이나 특정 이벤트(Extend)는 횡단적으로 부가된다.

#### 3. 프로젝트 관리(PM)와의 시너지 (WBS 분리)

- **Include 관계**: **WBS(Work Breakdown Structure)** 상에서 병렬 작업이 어렵다. 선행되는 공통 모듈이 먼저 개발되어야 후속 모듈 개발이 가능하다.
- **Extend 관계**: 스크럼(Sprint) 백로그에서 **우선순위가 낮은 스토리**로 분리하기 용이하다. 기본 기능(Base UC)을 먼저 개발하고, 여유가 될 때 확장 기능(Extending UC)을 붙이는 개발 전략이 가능하다.

> **📢 섹션 요약 비유**:
> 이 관계들은 **'건축 공사의 시공 순서'**와 같습니다.
> **포함(Include)**은 **'기둥과 foundation'**을 쌓는 일과 같습니다. 이것이 완료되지 않으면 지어진다는 보장도 없이 벽돌을 쌓을 수 없으므로, 가장 먼저 확정하고 자원을 투입해야 합니다.
> **확장(Extend)**은 **'인테리어 공사'**나 **'정원 조성'**과 같습니다. 건물의 구조적인 완성(Base UC)에는 영향을 주지 않으므로, 예산과 시간에 따라 자유롭게 선택하여 시공하거나 나중에 추가(Refactoring)할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 금융감독원 전자전표 시스템 구축

대규모 공공 프로젝트에서 유스케이스 포함/확장의 결정은 시스템의 성능과 보안 안정성을 좌우한다.

- **상황**: 사용자가 전자세금계산서를 발행(`Issue Bill`)하는 시스템을 설계 중이다.
- **문제 1 (보안)**: 발행, 조회, 수정 시마다 '사용자 신원 확인' 로직이 반복된다.
    -   **기술사적 판단 (A)**: `<<include>>` 관계로 **[인증(Authenticate)]** 유스케이스를 분리한다.
    -   **효과**: 인증 알고리즘