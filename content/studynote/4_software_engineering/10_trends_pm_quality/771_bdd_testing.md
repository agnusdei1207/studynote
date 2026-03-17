+++
title = "771. BDD Given-When-Then 행동 명세 테스트"
date = "2026-03-15"
weight = 771
[extra]
categories = ["Software Engineering"]
tags = ["Agile", "BDD", "Behavior Driven Development", "Gherkin", "Given-When-Then", "Testing", "Collaboration"]
+++

# 771. BDD Given-When-Then 행동 명세 테스트

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **TDD (Test-Driven Development)**의 기술적 한계를 극복하여, 코드 구현보다 비즈니스 **행동(Behavior)** 명세에 집중함으로써, 개발자와 비개발자 간의 '언어적 격차(Linguistic Gap)'를 해소하고 요구사항을 테스트 가능한 자연어로 정의하는 소프트웨어 엔지니어링 패러다임.
> 2. **표준화**: **Gherkin (Domain Specific Language)** 구문을 사용하여 작성된 시나리오가 곧 실행 가능한 테스트 코드가 되는 **'살아있는 문서(Living Documentation)'** 체계를 구축하며, 이는 CI/CD 파이프라인과 연동하여 지속적인 검증을 가능하게 함.
> 3. **가치**: 요구사항 정의 단계에서 발생하는 모호성(Ambiguity)을 제거하여 리스크를 사전에 완화하고, 회귀 테스트(Regression Test) 자산으로 활용함으로써 유지보수 비용을 최소화하며 비즈니스 가치 전달의 효율성을 극대화함.

---

### Ⅰ. 개요 (Context & Background)

**BDD (Behavior-Driven Development)**는 2003년경 댄 노스(Dan North)에 의해 제안된 소프트웨어 개발 방법론으로, 기존 **TDD (Test-Driven Development)**가 '테스트'라는 기술적 관점에만 집중하는 것을 비판하고 '행동'이라는 비즈니스 관점으로 전환했습니다. 전통적인 개발 프로세스에서 비즈니스 요구사항은 기획서에 머물고, 개발자는 이를 다시 코드로 해석하는 과정에서 '의미의 왜곡(Lost in Translation)'이 발생했습니다. BDD는 개발자, QA, 비즈니스 분석가가 동일한 언어를 사용하여 시스템의 예상되는 행동을 정의하고, 이것을 곧 테스트 코드로 자동화하는 것을 목표로 합니다.

소프트웨어의 복잡도가 높아짐에 따라 단순히 '코드가 잘 돌아가는가'를 넘어 '올바른 기능을 수행하는가'에 대한 검증이 중요해졌습니다. 이를 위해 **Ubiquitous Language (보편 언어)**를 도입하여 도메인 전문가와 개발자가 동일한 용어를 사용하도록 강제하며, 이를 **Given-When-Then** 포맷으로 형식화합니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  [Evolutionary Context]: From Unit Testing to Behavior Specification        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Unit Testing (TDD)                                                       │
│     └─ Focus: "Is the code logic correct?" (Developer-centric)              │
│        - Tests methods/functions (e.g., assertEquals(2, add(1,1)))          │
│                                                                             │
│  2. BDD (Evolution)                                                         │
│     └─ Focus: "Is the business behavior correct?" (Stakeholder-centric)     │
│        - Tests features/scenarios (e.g., User can withdraw cash)            │
│                                                                             │
│  [Key Difference]                                                            │
│  ┌──────────────┐       ┌──────────────┐                                    │
│  │   Developer  │───X───▶│    Business  │  (TDD: Language Barrier exists)   │
│  │  (Code/JUnit)│       │   (Natural)  │                                    │
│  └──────────────┘       └──────────────┘                                    │
│                                                                             │
│  ┌──────────────┐       ┌──────────────┐                                    │
│  │   Developer  │◀───✅──│    Business  │  (BDD: Shared Language via Gherkin)│
│  │  (Gherkin)   │       │   (Gherkin)  │                                    │
│  └──────────────┘       └──────────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 📢 섹션 요약 비유
"마치 건축주와 건축가가 복잡한 도면(코드)만 보고 다투는 대신, 생활 속에서 사용할 집의 모습을 '생활 시나리오(행동)'로 먼저 정리해놓고 나서 그것을 바탕으로 집을 짓는 것과 같습니다. 집이 완성되기 전에 '거실에서 커피를 마실 때 햇살이 들어온다'는 행동을 먼저 명세하는 것입니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

BDD의 아키텍처는 **'자연어 명세서'**와 **'실행 가능한 코드'** 사이의 간극을 메우는 도구들과 프로세스로 구성됩니다. 핵심은 **Gherkin Syntax**를 사용하여 작성된 Feature 파일이 **Test Runner (e.g., JUnit, NUnit)**에 의해 실행될 때, 각 라인이 호출하는 **Step Definition (Glue Code)**을 통해 실제 애플리케이션 로직과 연결되는 메커니즘입니다.

#### 1. 핵심 구성 요소 상세

| 구성 요소 (Component) | 역할 (Role) | 상세 동작 (Internal Behavior) | 관련 도구/표기 (Tools) |
|:---:|:---|:---|:---|
| **Feature File** | 명세서 (Spec) | Gherkin 언어로 작성된 텍스트 파일로 비즈니스 시나리오를 정의. `.feature` 확장자 사용. | Cucumber, SpecFlow, Behave |
| **Gherkin Syntax** | DSL (Domain Specific Language) | Given(상태), When(행위), Then(결과)의 구조화된 키워드를 제공. | `Given`, `When`, `Then`, `And`, `But` |
| **Step Definition** | 접착제 (Glue Code) | 자연어 한 줄 한 줄에 매핑되는 실제 코드 함수(Java, Python 등). 정규 표현식(Regex)을 통해 매칭됨. | `@Given("^user is logged in$")` |
| **Test Runner** | 엔진 (Engine) | Feature 파일을 해석하고 Step Definition을 찾아 실행하는 테스트 프레임워크. | JUnit, TestNG, Pytest |
| **Application Code** | 구현체 (SUT) | 실제 비즈니스 로직이 구현된 코드. Step Definition을 통해 호출됨. | Spring Boot, Django, Node.js |

#### 2. Gherkin Syntax 내부 매커니즘 및 파싱

Gherkin은 선언형 언어로, 코드를 실행하는 것이 아니라 **'무엇을(What)'** 할지만 정의합니다. 테스트 러너는 이 텍스트를 파싱(Parsing)하여 정규 표현식(Regex) 매칭을 수행합니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  [BDD Execution Flow & Regex Matching Mechanism]                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Feature File (Natural Language)                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Feature: Login System                                             │    │
│  │   Scenario: Valid Login                                           │    │
│  │     Given user navigates to login page                            │    │
│  │     When user enters "admin" and "password123"                    │    │
│  │     Then user should be redirected to dashboard                   │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│           │                                                                 │
│           ▼ (Parsing & Mapping)                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ 2. Step Definition (Code Glue) - Java Example                      │    │
│  │                                                                      │    │
│  │ @Given("^user navigates to login page$")                            │    │
│  │ public void userNavigatesToLoginPage() {                            │    │
│  │     driver.get("http://example.com/login");                         │    │
│  │ }                                                                    │    │
│  │                                                                      │    │
│  │ @When("^user enters \"([^\"]*)\" and \"([^\"]*)\"$")                 │    │
│  │ public void userEntersCredentials(String username, String password) {│    │
│  │     loginPage.typeUser(username);                                   │    │
│  │     loginPage.typePass(password);                                   │    │
│  │ }                                                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│           │                                                                 │
│           ▼ (Invoking Business Logic)                                       │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ 3. System Under Test (SUT)                                         │    │
│  │     [AuthController] ──▶ [AuthService] ──▶ [Database]             │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: 스텝(Step)의 생명주기

1.  **Match (매칭)**: Test Runner는 Feature 파일의 각 라인을 읽고, 사전에 정의된 Step Definition들의 정규 표현식(Regex)과 비교하여 일치하는 함수를 찾습니다. 만약 찾지 못하면 "Undefined Step" 오류를 반환합니다.
2.  **Execute (실행)**: 매칭된 함수가 실행됩니다. 이때 파라미터가 있다면 Gherkin에서 추출한 값을 전달합니다 (예: `"admin"` 문자열).
3.  **Report (보고)**: 실행 결과(Pass/Fail)가 Test Runner에 기록되며, 이는 HTML 형태의 리포트로 시각화되어 비개발자에게도 전달됩니다.

#### 4. 핵심 코드 구조 (Java/Cucumber Style)

```java
// 실무 레벨 코드: 의존성 주입을 통한 모듈화
public class LoginSteps {
    private LoginPage loginPage;
    private DashboardPage dashboardPage;

    // PicoContainer 혹은 Spring이 Context를 통해 자동 주입
    public LoginSteps(LoginPage loginPage, DashboardPage dashboardPage) {
        this.loginPage = loginPage;
        this.dashboardPage = dashboardPage;
    }

    @Given("^the user is on the login page$")
    public void init() {
        loginPage.open();
    }

    @When("^he logs in using username as \"([^\"]*)\" and password \"([^\"]*)\"$")
    public void login(String username, String password) {
        loginPage.login(username, password);
    }

    @Then("^he should be redirected to the dashboard page$")
    public void verifyRedirect() {
        assertTrue(dashboardPage.isDisplayed());
    }
}
```

#### 📢 섹션 요약 비유
"자동차의 내비게이션 시스템에 목적지를 설정하는 과정과 유사합니다. 운전자(사용자)는 '단순한 버튼 조작(Given-When)'으로 목적지를 입력하지만, 내부적으로는 위성(GPS)과 데이터베이스(Step Definition)가 복잡하게 연동되어 연산을 수행한 뒤, 최적의 경로(Then)를 화면에 보여줍니다. 사용자는 내부 연산 알고리즘을 알 필요 없이 목적지라는 '행동'만 정의하면 됩니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

BDD는 단순한 테스트 기법이 아니라 요구공학(Requirements Engineering), 품질 관리(Quality Assurance), 그리고 애자일 프로세스를 잇는 융합적 기법입니다.

#### 1. 심층 기술 비교: TDD vs BDD

| 구분 (Criteria) | **TDD (Test-Driven Development)** | **BDD (Behavior-Driven Development)** |
|:---|:---|:---|
| **주요 관심사 (Focus)** | **구현의 정확성 (How it works)** | **시스템의 행동 (What it does)** |
| **작성 주체 (Author)** | 개발자 (Developer) | **3 Amigos (Dev, QA, PO)** 공동 작업 |
| **언어 (Language)** | **프로그래밍 언어** (Java, C#, Py) | **자연어** (English/Korean + Gherkin) |
| **테스트 단위 (Granularity)** | 단위(Unit), 메서드(Method) | **기능(Feature), 시나리오(Scenario)** |
| **코드 예시 (Syntax)** | `assertEquals(200, response.getStatusCode())` | `Then 사용자는 성공 메시지를 받아야 한다` |
| **회귀 테스트 (Regression)** | 빠름, 단위 테스트용 | 상대적 느림, E2E(End-to-End) 검증용 |

#### 2. 아키텍처적 융합: ATDD 및 삼자 회의

**ATDD (Acceptance Test-Driven Development)**는 BDD와 밀접하게 연관됩니다. BDD는 ATDD의 구현 방법론 중 하나로 볼 수 있습니다. 여기서 핵심은 **'Three Amigos (세 명의 친구)'** 회의입니다. 개발자(Dev), 테스터(QA), 비즈니스(PO)가 모여 시나리오를 작성함으로써 '개발 착수 전' 결함을 90% 이상 제거할 수 있습니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  [The Three Amigos Collaboration Cycle]                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     [ Business Analyst (PO) ]  "What" (비즈니스 가치)                        │
│           │                                                                 │
│           ├─── communication ───┐                                          │
│           │                     │                                          │
│           ▼                     ▼                                          │
│     [ Developer (Dev) ]    [ Tester (QA) ]                                 │
│      "How" (구현 가능성)      "Validation" (검증 시나리오)                    │
│           │                     │                                          │
│           └─────── ▶  CONSENSUS ◀───────┘                                 │
│                     │                                                      │
│                     ▼                                                      │
│             (Shared Understanding)                                         │
│                     │                                                      │
│                     ▼                                                      │
│        ✍️ Writing Gherkin Scenarios Together ✍️                           │
│                                                                             │
│  Result:                                                                   │
│  - Developer: 구현 로직에 대한 확신                                          │
│  - QA: 자동화 테스트 시나리오 확보                                           │
│  - PO: 요구사항이 반영된 테스트 결과물 확보                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. CI/CD 파이프라인과의 융합 (Synergy)

BDD 시나리오는 단순한 문서가 아니므로 **CI (Continuous Integration)** 파이라인(Jenkins, GitLab CI, GitHub Actions)에 통합되어야 합니다. 소스 코드가 커밋될 때마다 BDD 테스트가 실행되어, 새로운 버그(Regression)가 발생했는지 즉시 감지합니다. 이때 성능 저하를 방지하기 위해, UI 테스트는 Mock을 활용하거나 주요 경로만 테스트하는 전략이 필요합니다.

#### 📢 섹션 요약 비유
"건축에서 '설