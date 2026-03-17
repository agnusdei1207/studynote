+++
title = "458-464. 테스트 더블과 서비스 가상화"
date = "2026-03-14"
[extra]
category = "Testing"
id = 458
+++

# 458-464. 테스트 더블과 서비스 가상화

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 테스트 더블(Test Double)은 실제 의존성(Real Component)을 대체하여 테스트 격리(Test Isolation)를 극대화하고, **SUT (System Under Test)**의 내부 로직 검증을 목적으로 하는 대체 객체 패턴입니다.
> 2. **가치**: Microservice Architecture(MSA) 환경에서 타 서비스의 장애나 미완성 상태에 얽매이지 않고, **테스트 커버리지(Test Coverage)**를 90% 이상으로 높이며 **CI/CD (Continuous Integration/Continuous Deployment)** 파이프라인의 안정성을 확보합니다.
> 3. **융합**: **TDD (Test-Driven Development)** 및 **DevOps** 자동화 프로세스와 결합하여, 개발 초기 단계부터 안정적인 코드 품질을 보장하고 레거시 시스템 마이그레이션 시의 리스크를 최소화합니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
테스트 더블(Test Double)은 xUnit 테스트 패턴(xUnit Test Patterns) 프레임워크에서 처음 정의된 개념으로, 테스트를 수행할 때 테스트 대상 시스템(SUT)이 의존하는 실제 컴포넌트(DOC, Depended-On Component)를 사용하는 대신, 테스트 목적에 맞게 동작을 조작하거나 단순화한 **대체 객체**를 의미합니다. 이는 단위 테스트(Unit Test)의 작성을 용이하게 하고, 외부 요인(네트워크 지연, DB 연결 실패 등)으로 인한 테스트의 불확실성(Flakiness)을 제거하는 핵심 전략입니다.

**💡 비유**
자동차 엔지니어가 엔진 성능을 테스트할 때, 실제 도로 사정이나 타이어 마모 상태와 같은 외부 변수를 배제하기 위해 '동력 계측기(Dyno)'에 엔진을 연결하여 구동하는 것과 같습니다.

**등장 배경**
1.  **기존 한계**: EAI (Enterprise Application Integration) 시절의 통합 테스트는 전체 시스템을 구동해야 하므로 테스트 비용이 고가이고, 특정 모듈 오류 시 전체 테스트가 불가능한 '스파게티 의존성' 문제가 존재했습니다.
2.  **혁신적 패러다임**: **TDD (Test-Driven Development)**의 등장과 함께 '격리(Isolation)'가 중요해지면서, 의존성을 끊고 로직 자체만을 검증하는 **단위 테스트(Unit Testing)**의 필요성이 대두되었습니다.
3.  **현재의 비즈니스 요구**: 클라우드 네이티브(Cloud Native) 환경과 MSA (Microservice Architecture)에서는 수십 개의 마이크로서비스가 얽혀 있으므로, 타 서비스의 배포 상태와 무관하게 독립적으로 개발 및 검증을 수행할 수 있는 **서비스 가상화(Service Virtualization)** 기술이 필수적입니다.

**📢 섹션 요약 비유**
테스트 더블과 서비스 가상화 도입은 **'영화 촬영 시의 스턴트맨과 CGI 합성 기술'**과 같습니다. 위험한 액션씬(외부 API 장애)이나 아직 세트장이 완공되지 않은 장면(개발 중인 타 서비스)을 배우가 직접 수행하기보다, 대역 배우(Stub/Mock)나 가상 배경(Virtual Service)을 활용하여 촬영(테스트)을 진행하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 및 상세 분석**

| 구분 (Element) | 정의 (Full Name) | 내부 동작 및 특성 | 주요 프로토콜/형식 | 사용 목적 |
|:---:|:---|:---|:---|:---|
| **Dummy** | **Dummy Object** | 인스턴스화는 되지만 내부 로직은 구현되지 않음. 주로 매개변수 리스트 채우기용으로 사용됨. | N/A | 컴파일러 오류 방지, 메서드 시그니처 충족 |
| **Stub** | **Test Stub** | 호출 시 미리 준비된(Hard-coded) 정적 응답을 반환. 내부 상태는 가지지 않음. | JSON, XML, cURL | 상태 기반 검증(State Verification) 지원 |
| **Spy** | **Test Spy** | Stub의 기능(값 반환)을 수행하며, 자신이 호출된 횟수/인자 등을 기록하는 캡처 기능 보유. | Wrapper Class | 호출 여부 및 이력 검증(Indirect Output) |
| **Mock** | **Mock Object** | 테스트 전 '기대(Expected)' 동작을 프로그래밍하고, 테스트 종료 시 이를 검증(Verify). | Hamcrest, Mockito | 행위 기반 검증(Behavior Verification) |
| **Fake** | **Fake Object** | 실제 로직이 구현되어 있으나, DB를 메모리(In-Memory)에 두는 등 운영 환경에 부적합한 방식. | H2, SQLite | **SUT** 통합 테스트, 성능 검증 |

**테스트 더블 계층 및 의존성 주입 (DI) 구조**

아래 다이어그램은 **SUT (System Under Test)**가 **DOC (Depended-On Component)**에 의존하는 상황에서, **Test Runner**가 **DI (Dependency Injection)** 패턴을 통해 테스트 더블을 주입하는 메커니즘을 도식화한 것입니다.

```ascii
                    [ Test Runner (JUnit/TestNG) ]
                               |
                               | 1. 테스트 시나리오 정의
                               v
    +---------------------------------------------------------------+
    |                   SUT (System Under Test)                     |
    |   ----------------------------------------------------------  |
    |   +--------------+          +-----------------------------+   |
    |   |  Core Logic  | -------- |    Interface (Dependency)   |   |
    |   +--------------+          +-------------+---------------+   |
    |                                          ^                   |
    +------------------------------------------|-------------------+
                                               |
                                               | 2. 의존성 주입 (DI)
                                    +----------|-------------------+
                                    |          v                   |
                                    |   [ Test Double (Stub) ]     |
                                    |   - returnValue: "OK"        |
                                    |   - responseTime: 0ms        |
                                    +------------------------------+
```

**(해설)**
위 구조는 **전통적인 계약(Contract)에 의한 테스트** 패턴을 보여줍니다.
1.  **SUT**는 실제 구현체가 아닌 추상화된 **인터페이스(Interface)**에 의존하도록 설계됩니다. (DIP, Dependency Inversion Principle 준수)
2.  **테스트 러너(Test Runner)**는 `setUp()` 단계에서 실제 객체(`Real Service`) 대신 **스텁(Stub)**이나 **목(Mock)** 객체를 생성하여 SUT에 주입(Inject)합니다.
3.  이로써 SUT는 외부 환경(네트워크, DB)과 완전히 단절된 상태에서, 테스트 더블이 제공하는 예측 가능한 입력값에 대한 반응 로직만을 검증하게 됩니다.

**심층 동작 원리: 상태 검증 vs 행위 검증**

```python
# [Python Code Snippet: Mock을 활용한 행위 검증 예시]

from unittest.mock import Mock

# 1. Mock 객체 생성 (Doc - Depended-On Component 대역)
mock_db = Mock()

# 2. SUT에 주입 및 로직 실행
user_service = UserService(db=mock_db)  # Dependency Injection
user_service.update_user(1, "New Name")

# 3. 행위 검증 (Behavior Verification)
# 'update_user' 로직 내부에서 db.execute()가 정확히 1번 호출되었는지 확인?
mock_db.execute.assert_called_once_with(
    "UPDATE users SET name='New Name' WHERE id=1"
)
```

**핵심 메커니즘**:
-   **상태 검증(State Verification)**: 테스트 실행 후 SUT의 **최종 상태(State)**를 확인합니다. (예: `assert user.name == "New Name"`) 주로 **Stub**이나 **Fake**와 함께 사용됩니다.
-   **행위 검증(Behavior Verification)**: SUT가 **DOC를 올바르게 사용했는지(Interaction)**를 확인합니다. (예: DB의 `commit()`이 호출되었는가?) 주로 **Mock** 객체와 함께 사용됩니다.

**📢 섹션 요약 비유**
테스트 더블의 구조는 **'인형극과 조종사(Puppeteer)'**와 같습니다. 인형극(SUT)의 동작을 테스트하기 위해, 실제 배우(Real Component) 대신 목에 줄이 연결된 인형(Test Double)을 사용합니다. **상태 검증**은 인형의 손과 발이 최종적으로 어디에 위치했는지 확인하는 것이고, **행위 검증**은 조종사(Test Runner)가 줄을 당기는 순서와 횟수가 정확했는지를 확인하는 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: Test Double 유형 결정 매트릭스**

테스트 목적에 따라 적절한 더블을 선택하는 것은 성능과 유지보수성에 큰 영향을 미칩니다.

| 비교 항목 | **Stub (스텁)** | **Mock (목)** | **Fake (페이크)** |
|:---|:---|:---|:---|
| **주요 관심사** | SUT의 **결과(Output)** 값은 무엇인가? | SUT가 **DOC를 어떻게 호출**하는가? | SUT와 DOC의 **통합 로직**은 정상인가? |
| **테스트 종류** | 상태 기반 테스트 (State-Based) | 행위 기반 테스트 (Interaction-Based) | 통합 테스트 (Integration Test) |
| **구현 복잡도** | 낮음 (하드코딩된 값 반환) | 중간 (Expectation 설정 필요) | 높음 (실제 로직의 단순화된 구현) |
| **테스트 속도** | 매우 빠름 (ms 단위) | 빠름 (ms 단위) | 상대적으로 느림 (In-Memory DB 등) |
| **대표 예시** | 고정된 환율 정보 반환 | `EmailService.send()` 호출 확인 | **H2 Database**, InMemory Repository |

**과목 융합 관점**

1.  **데이터베이스 (DB) 및 OS 융합: Fake 활용**
    -   **실무 시나리오**: SQL 튜닝을 테스트할 때마다 실제 RDBMS를 띄우면 시간이 오래 걸립니다.
    -   **융합 해법**: **In-Memory DB (예: H2, HSQLDB)**를 **Fake**로 활용하여 OS 파일 I/O 과정을 생략하고, 쿼리 로직 검증만 수행하면 테스트 속도를 10배 이상 향상시킬 수 있습니다.

2.  **네트워크 및 보안 융합: Service Virtualization**
    -   **실무 시나리오**: 결제 모듈(PG사) 연동 테스트 시 실제로 카드를 찍을 수 없으며, 네트워크 지연(Latency)이나 보안 프로토콜(SSL/TLS 핸드셰이크) 오류 상황을 재현하기 어렵습니다.
    -   **융합 해법**: **SV (Service Virtualization)** 도구(예: WireMock, Hoverfly)를 사용하여 TCP/IP 레벨에서의 **Timeout**이나 **HTTP 500 Error** 등의 장애 상황을 인위적으로 주입하여, 시스템의 **회복 탄력성(Resilience)**과 **장애 격리(Fault Isolation)** 능력을 검증합니다.

**📢 섹션 요약 비유**
Stub과 Fake의 선택은 **'자동차 시운전(Stub) vs 모의 주행 연습기(Fake)'**의 차이와 같습니다. 단순히 핸들을 조작했을 때 바퀴가 돌아가는지만 확인하려면 시뮬레이터(Stub)로 충분하지만, 자동차 전체의 유기적인 움직임과 서스펜션 반응까지 확인하려면 실제 자동차를 간소화하게 만든 모의 주행 연습기(Fake)가 필요합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **상황 A: 외부 법규 API 연동**
    -   **문제**: 국세청 세무 확인 API는 테스트 환경을 제공하지 않거나, 사용 횟수 제한이 있어 CI/CD에서 자동 테스트가 불가능합니다.
    -   **의사결정**: **서비스 가상화(Virtual Asset)**를 구축합니다. 실제 API의 스펙(JSON Schema)을 기반으로 목 서버를 구축하고, 다양한 응답 케이스(성공, 실패, 지연)를 시뮬레이션합니다.

2.  **상황 B: 레거시 모듈 리팩토링**
    -   **문제**: 10년 된 Java 코드를 수정해야 하는데, 연관된 객체가 100개가 넘어 테스트 코드 작성이 불가능합니다.
    -   **의사결정**: 리팩토링 시작 전, **인터페이스 추출(Extract Interface)**을 수행한 후 의존성을 **Mock**으로 치환하여, 기존 로직을 깨지 않고 안전하게 코드를 수정합니다. (Characterization Test 활용)

**도입 체크리스트**

| 구분 | 체크항목 |
|:---|:---|
| **기술적** | □ 테스트 더블을 주입하기 위한 생성자/Setter가 존재하는가? <br> □ Mock의 설정(Expectation)이 실제 구현 로직과 불일치하지 않는가? (Overspecification 주의) |
| **운영/보안** | □ Fake DB에 들어가는 테스트 데이터가 민감 정보(PII)가 아닌가? <br> □ 가상화 서버(Virtual Service)가 운영 트래픽을 포섭하지 않도록 격리되었는가? |

**안티패턴 (Anti-Pattern)**

-   **Mock 과용(Overspecification)**: 내부 구현 사항(구체적인 메서드 호출 순서 등)을 지나치게 검증하여, **리팩토링(Refactoring)** 시 테스트 코드가 모두 깨지는 상황. (결합도 과다)
-   **SUT 내부 로직 테스트 실패**: 테스트하려는 대상(SUT)이 아닌 Mock 객체의 설정에 버그가 있어 "Green Bar(성공)"가 떴는데 실제로는 로직이 틀린 경우.

**📢 섹션 요약 비유**
테스트 더블을 활용한 테스트 작성은 **'안전 장치가 달린 자동차 조종 시험'**과 같습니다. Mock 설정은 **'주행 경로(GPS)'**입니다. 만약 GPS 설정이 잘못되면 운전자는 엉뚱한 길로