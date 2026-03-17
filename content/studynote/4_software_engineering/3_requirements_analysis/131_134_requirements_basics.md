+++
title = "Untitled"
date = "2026-03-14"
+++

# 131-134. 요구공학의 본질과 요구사항의 유형
> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: 요구공학(Requirements Engineering)은 고객의 **암묵적(Needs)**인 욕구를 **형식적(Specifications)**인 기술 명세로 변환하여, 개발 비용 증가 방지와 시스템 오작동을 예방하는 소프트웨어 공학의 뼈대입니다.
> 2. **가치**: 요구사항 결함을 찾아내는 비용은 `요구사항 분석 단계`에 비해 `유지보수 단계`에서 약 **100~200배** 폭증하므로, 초기 정합성 확보가 프로젝트 ROI(Return On Investment)를 결정합니다.
> 3. **융합**: 최근에는 `AI 기반 요구사항 자동화` 및 `DevOps 파이프라인`과의 연계를 통해, 정적 문서를 넘어 살아있는 테스트 케이스로 관리하는 **Requirements-as-Code (RaaC)** 패러다임으로 진화하고 있습니다.
date = "2026-03-14"
+++

### Ⅰ. 개요 (Context & Background) - [500자+]

요구공학(Requirements Engineering, RE)은 소프트웨어 시스템이 가져야 할 특성과 제약 조건을 이해관자자(Stakeholders)로부터 도출하여, 시스템 설계 및 구현이 가능한 형태로 정의하고 관리하는 **생명주기 전반(Lifecycle-wide)**에 걸친 활동입니다.

이는 단순히 '문서를 작성하는 행위'가 아니라, 고객의 머릿속에 있는 **모호한 추상화(Abstraction) 단계**를 개발자가 이해할 수 있는 **명확한 논리(Logic) 단계**로 변환하는 인지적 공학 과정입니다.

**💡 비유**
건축에서 설계도면이 없이 철근을 쌓고 시멘트를 부을 수 없듯이, 요구사항 명세서는 소프트웨어의 '설계도면'이자 '법적 계약서'입니다.

**등장 배경**
① **기존 한계**: 1970~80대 폭포수(Waterfall) 모델 시절, 개발 후반에 가서 "내가 원한 건 이게 아니다"라는 말이 나오며 천문학적인 비용이 발생 ( Boehm의 꺾은선 그래프 참조).
② **혁신적 패러다임**: 소프트웨어 위기(Software Crisis) 극복을 위해 정형 요구사항 분석 기법과 프로토타이핑(Prototyping)이 도입되었습니다.
③ **현재의 비즈니스 요구**: 급변하는 시장 환경 속에서 `애자일(Agile)` 방법론과 결합하여, 변경 유연성을 유지하면서도 개발 범위(Scope)를 철저히 통제하려는 ** Requirements Engineering (RE) 4.0** 이 필요합니다.

```ascii
[Boehm의 비용 증가 곡선: 수정 비용의 폭발적 증가]

     Cost (Log Scale)
      ^
      |                                      (Maintenance)
      |                                   /  (x100 ~ x200)
      |                                /
      |                             / (Testing)
      |                          /   (x10 ~ x20)
      |                       / 
      |                    /  (Coding)
      |                 /     (x1 ~ x5)
      |              /  (Design)
      |           /     (x1)
      |        /
      |     /  (Requirements)
      |  /     (Base Cost)
      +-----------------------------------------> Time
```

**해설**: 위 다이어그램은 Barry Boehm이 제시한 것으로, 요구사항 단계에서의 버그 수정 비용을 1이라고 했을 때, 유지보수 단계에서는 그 비용이 100배 이상 뛴다는 것을 보여줍니다. 즉, 요구사항을 잘못 정의하고 내려가는 것은 "내려갈 때는 에스컬레이터를 타지만, 올라올 때는 엄청난 무게를 짊어지고 계단을 기어오르는 것"과 같습니다.

> **📢 섹션 요약 비유**: 요구공학은 거대한 빌딩을 짓기 전에 토목 설계사가 땅을 정밀하게 조사하고 청사진을 그리는 단계입니다. 흙이 무르거나 설계를 잘못 그리면, 100층 빌딩을 짓고 난 뒤라도 다시 허물어야 하니까요.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

요구공학의 핵심은 **요구사항의 유형화(Type Classification)**와 **프로세스 수행(Process Execution)**입니다. 요구사항은 크게 무엇을 하는지를 정의하는 기능적 요구사항과 어떻게 잘 수행해야 하는지를 정의하는 비기능적 요구사항으로 나뉩니다.

#### 1. 구성 요소 상세 분석

| 분류 | 구성 요소 (Component) | 정의 및 역할 | 내부 동작 및 프로토콜/지표 | 관련 표준 및 비고 |
|:---|:---|:---|:---|:---|
| **기능적 요구사항**<br>(Functional Req.) | **서비스(Service)** | 시스템이 입력에 대해 어떤 출력을 내놓는지 | 유스케이스(Use Case) 기술, `[Actor] → [System] → [Response]` | IEEE 830 SRS 표준 |
| | **비즈니스 규칙(Business Rule)** | 도메인의 제약 조건 및 정책 | 조건문(If-Then-Else), 상태 전이(State Transition) | BRMS(Business Rule Management System) 연동 |
| | **데이터 요구사항(Data Req.)** | 정보의 저장, 흐름, 형식 | ERD(Entity Relationship Diagram), JSON/XML 스키마 | ACID 트랜잭션 고려 |
| **비기능적 요구사항**<br>(Non-functional Req.) | **성능(Performance)** | 처리량, 응답 시간 | Latency < 100ms, Throughput > 1,000 TPS | TPC-C 벤치마킹 |
| | **보안(Security)** | 기밀성, 무결성, 가용성 | 인증(AuthN), 인가(AuthZ), 암호화(AES-256) | OWASP Top 10 준수 |
| | **신뢰성(Reliability)** | 고장 시 회복력 | MTBF(Mean Time Between Failures), RPO/RTO | HA(High Availability) 클러스터링 |
| | **사용성(Usability)** | 사용자 학습 곡선, 인터페이스 | UCD(User Centered Design), 클릭 수 최소화 | WCAG 접근성 가이드 |

#### 2. 요구공학 프로세스 상세 다이어그램

```ascii
[요구사항 공학의 5단계 수명 주기 (Iterative Model)]

          [Stakeholders]           [Analysts]               [Developers]
               |                       |                        |
    +----------v----------+   +--------v--------+     +--------v--------+
    |   1. Elicitation    |-->|   2. Analysis   |---->| 3. Specification|
    |  (도출: 질문/관찰)  |   | (협상: 모순해소) |     | (SRS 작성: 모델링)|
    +----------+----------+   +--------+--------+     +--------+--------+
               ^                       |                        |
               |                       v                        |
    +----------+----------+   +--------+--------+     +--------v--------+
    |   5. Management    |<--| 4. Verification |<----|   Validation    |
    | (혀상관리: 버전관리)|   | (검증: 오류검출) |     | (확인: 사용자확인)|
    +---------------------+   +-----------------+     +-----------------+
    
    Key Artifacts: User Story, Use Case Diagram, SRS (Software Requirements Specification)
    Tools: IBM DOORS, JIRA, Confluence, SysML
```

**해설**:
1.  **도출(Elicitation)**: 브레인스토밍, 인터뷰, 워크숍 등을 통해 숨어있는 요구사항을 발굴합니다. 이때 "말하는 것(Said)"과 "진짜 원하는 것(Meant)" 사이의 간극을 해소해야 합니다.
2.  **분석(Analysis)**: 도출된 요구사항 간의 충돌(Conflict)을 해결하고 우선순위(MoSCoW: Must, Should, Could, Won't)를 매깁니다. 개념적 모델링이 이루어지는 단계입니다.
3.  **명세(Specification)**: `SRS (Software Requirements Specification)` 문서화. 자연어와 혼란을 막기 위해 정형화된 언어나 UML(Unified Modeling Language)을 사용합니다.
4.  **검증 및 확인(V&V)**:
    *   **Verification (검증)**: "명세서가 명확하게 작성되었는가?" (Syntax 오류 검사)
    *   **Validation (확인)**: "이것이 정말 고객이 원하는 시스템인가?" (Semantic 오류 검사)

> **📢 섹션 요약 비유**: 기능적 요구사항은 자동차의 '엔진, 핸들, 브레이크' 같은 장치입니다. 비기능적 요구사항은 자동차가 '시속 300km로 달릴 수 있는가(성능)', '충돌해도 에어백이 터지는가(안전성)', '운전하기 편한가(사용성)'에 대한 조건입니다. 아무리 좋은 장치(기능)를 달아도, 100km 밖에 못 가거나(성능 부족) 자주 고장 난다면(신뢰성 부족) 그 자동차는 가치가 없습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

요구사항은 시각화 표기법에 따라, 그리고 산출물의 성격에 따라 크게 구분됩니다. 이를 단순 비교를 넘어 실무적 트레이드오프 관점에서 분석합니다.

#### 1. 심층 기술 비교: 구조적 방법 vs 객체지향 방법 (OOA)

| 비교 항목 | Structured Analysis (구조적 분석) | Object-Oriented Analysis (객체지향 분석) |
|:---|:---|:---|
| **핵심 관점** | **Process(기능)** 중심 | **Object(객체/데이터)** 중심 |
| **주요 다이어그램** | DFD (Data Flow Diagram)<br>STD (State Transition Diagram) | UML (Unified Modeling Language)<br>- Use Case, Class, Sequence Diagram |
| **데이터와 절차** | 데이터와 기능을 분리하여 기술 (Entity-Rel 분리) | 데이터와 행동을 **캡슐화(Capsulation)**하여 모델링 |
| **재사용성** | 낮음 (모듈 결합도가 높을 수 있음) | 높음 (상속/위임 통한 다형성 활용) |
| **실무 적용성** | 임베디드 시스템, 간단한 스크립트 | 대규모 엔터프라이즈 시스템, MSA (Microservices Architecture) |

#### 2. 산출물 포맷 비교: 자연어 vs 정형 언어

| 구분 | 자연어 (Natural Language) | 정형 언어/모델 (Formal/Model-Based) |
|:---|:---|:---|
| **표기 예시** | "사용자는 ID와 비밀번호로 로그인해야 한다." | `Login(User_ID, Pwd) -> (Success_Token) OR (Fail_Exception)` |
| **장점** | 이해관자자가 읽기 쉽고, 문서화가 직관적임. | 모호함(Ambiguity) 제거, 자동 테스트 생성 가능. |
| **단점** | 이중 해석 가능, 문맥 의존적임. | 학습 난이도가 높고, 일반 사용자가 보기 힘듦. |

**과목 융합 관점**:
*   **데이터베이스 (DB)**: 요구사항 분석 단계에서 도출된 **데이터 요구사항**은 바로 `ERD (Entity Relationship Diagram)`로 연결되어 DB 스키마 설계의 기초가 됩니다. 정규화 과정은 데이터 요구사항의 정합성을 검증하는 과정이기도 합니다.
*   **소프트웨어 설계 (Design)**: 요구사항 분석이 완료되지 않으면 **UI/UX 디자인**과 **아키텍처 설계(HLD/LLD)**를 시작할 수 없습니다. 특히 `SOLID 원칙`에 입각한 설계는 '변경 가능한 요구사항'을 격리시키는 데 그 목적이 있습니다.

> **📢 섹션 요약 비유**: 요구사항 분석은 마치 건축의 '설계도면' 작업입니다. **구조적 방법**은 "방-부엌-화장실" 배치를 나열하는 평면도라면, **객체지향 방법**은 "가구, 전기, 수도 배관"이 어떻게 얽혀 있는지 입체적으로 보여주는 3D 모델링과 같습니다. 집이 복잡할수록 3D 모델(객체지향)이 더 안전합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

실제 프로젝트 현장에서 요구사항은 "곧 죽어라" 바뀝니다(Requirement Volatility). 이를 관리하지 못하면 `Scope Creep (범위의 괴물)` 현상이 발생하여 프로젝트가 실패합니다.

#### 1. 실무 시나리오 및 의사결정
*   **Case A (위험 회피)**: 보안 시스템 구축 시 요구사항이 모호한 경우?
    *   **판단**: **Prototyping (프로토타이핑)**을 먼저 구현하여 고객에게 피드백을 받는다. 문서만으로는 인증/인가 로직의 예외 상황을 모두 커버할 수 없기 때문이다.
*   **Case B (현실적 타협)**: 비기능적 요구사항 중 "성능"과 "보안"이 충돌할 경우?
    *   **판단**: **Trade-off Analysis** 수행. 예를 들어 모든 트랜잭션에 대한 암호화(보안)는 레이턴시(Latency)를 증가시킨다(성능 저하). 이 경우 TPS(Transactions Per Second) 요구사항을 만족하는 최소한의 보안 알고리즘(AES 대신 경량화 암호)을 선택하거나 하드웨어 업그레이드를 검토해야 한다.

#### 2. 도입 체크리스트 (Technical & Operational)
*   [ ] **추적성(Traceability) 확보**: 요구사항 ID(ID_001)가 설계, 소스코드, 테스트케이스까지 연결되었는가? → `Requirement Traceability Matrix (RTM)`
*   [ ] **검증 가능성(Verifiability)**: 요구사항이 "좋은 사용자 경험을 제공해야 한다"처럼 모호하지 않은가? → "클릭 횟수가 3회 이내여야 한다"로 정량화되었는가?

#### 3. 안티패턴 (Anti-pattern)
*   **Gold Plating (금도금)**: 개발자가 "이거 나중에 필요할 것 같아