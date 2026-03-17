+++
title = "도메인 04: 소프트웨어 공학 (Software Engineering)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-software-engineering"
kids_analogy = "건물을 지을 때 설계도를 그리고, 튼튼한지 검사하고, 사람들이 살기 좋게 인테리어를 하는 모든 과정을 말해요. 코딩만 하는 게 아니라, '고장 나지 않는 튼튼한 프로그램'을 체계적으로 만드는 방법을 배우는 곳이랍니다."
+++

# 도메인 04: 소프트웨어 공학 (Software Engineering)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 복잡성(Complexity)과 비가시성(Invisibility)을 지닌 소프트웨어를 정해진 예산과 기간 내에 고품질로 개발, 유지보수하기 위한 공학적 원리, 방법론, 도구의 총체.
> 2. **가치**: 요구사항 분석부터 테스트, 배포에 이르는 생명주기(SDLC)를 통제하고 객체지향/디자인 패턴을 적용하여, 기술 부채(Technical Debt)를 억제하고 프로젝트의 파단을 원천 차단.
> 3. **융합**: 과거의 경직된 폭포수(Waterfall) 모델을 넘어 애자일(Agile) 철학과 데브옵스(DevOps) CI/CD 파이프라인이 결합된 '지속적 가치 인도(Continuous Value Delivery)' 체계로 완전한 결착을 이룸.

---

### Ⅰ. 개요 (Context & Background)
1960년대, 하드웨어 성능이 급증하면서 요구되는 소프트웨어의 규모도 기하급수적으로 팽창했다. 그러나 주먹구구식 코딩 기예(Art)에 의존하던 당시의 방식은 잦은 납기 지연, 예산 초과, 끔찍한 버그를 초래하며 이른바 **'소프트웨어 위기(Software Crisis)'**를 촉발시켰다.
**소프트웨어 공학(Software Engineering)**은 이 위기를 돌파하기 위해 탄생했다. 소프트웨어 개발을 벽돌을 쌓아 건물을 짓는 물리적 공학(Engineering)의 궤도로 끌어올리기 위해, 엄격한 프로세스(Process), 방법론(Methodologies), 정량적 품질 측정(Metrics)의 3대 요소를 도입했다. 오늘날의 소프트웨어 공학은 단순히 코드를 짜는 행위를 넘어, 고객의 모호한 비즈니스 요구를 정확히 추출(Requirements)하고, 변경에 유연한 아키텍처(Design)를 수립하며, 자동화된 검증(Testing)을 통해 시스템의 생명력을 연장하는 거대한 철학이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

소프트웨어 개발 생명주기(SDLC)는 시스템이 태어나서 폐기될 때까지의 전 과정을 규격화한 아키텍처 프레임워크다. 

#### 1. 핵심 공학 도메인
| 도메인 | 상세 역할 | 내부 동작/활용 기법 | 관련 산출물 및 표준 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Requirements** | 요구사항 공학 | 고객의 요구를 추출, 분석, 명세, 검증 및 추적 관리 | SRS (Software Req Spec) | 건축의 청사진 초안 |
| **Design/Architecture** | 설계 공학 | 시스템 컴포넌트 분할 및 인터페이스, DB 스키마 설계 | UML, 디자인 패턴 (GoF) | 철골 구조도 및 배관도 |
| **Implementation** | 구현 (Coding) | Clean Code, 리팩토링, 시큐어 코딩 원칙 적용 | Source Code, Git Commit | 실제 시공 작업 |
| **Testing/QA** | 검증 및 품질 보증 | V-Model 기반의 단위/통합/시스템/인수 테스트, 정적 분석 | Test Case, ISO/IEC 25010 | 안전 진단 및 감리 |
| **Maintenance** | 유지보수 및 형상 | 배포 후 버그 수정, 환경 적응(Adaptive), 버전 통제 | Git, CI/CD, Issue Tracker | 건물 리모델링 및 보수 |

#### 2. V-Model 테스트 아키텍처 및 애자일 스크럼(ASCII)
전통적인 폭포수 기반의 검증 모델(V-Model)은 각 개발 단계가 테스트 단계와 정확히 1:1로 결착되는 완벽한 대칭 구조를 가진다.
```text
    [ V-Model Testing Architecture ]
    
    (Requirements Analysis) ---------------------------> (Acceptance Testing)
             \                                                /
      (System Architecture Design) ----------------> (System Testing)
               \                                          /
           (Component Design) ----------------> (Integration Testing)
                 \                                    /
                  (Unit Design) -----------> (Unit Testing)
                           \                  /
                           [ Implementation (Code) ]
```
최신의 애자일 스크럼(Scrum) 아키텍처는 위 V-Model을 1~4주 단위(Sprint)로 끊임없이 반복하여 점진적 가치를 창출한다.
```text
    [ Agile Scrum Loop ]
    [Product Backlog] -> (Sprint Planning) -> [Sprint Backlog] -> [ 2-Week Sprint (Daily Standup) ] -> (Review) -> [Shippable Product]
```

#### 3. 객체지향 설계 원칙 (SOLID) 및 응집도/결합도 수식화
아키텍처의 품질을 결정하는 가장 중요한 원리는 **"응집도(Cohesion)는 최대화하고, 결합도(Coupling)는 최소화하라"**이다.
- **S (SRP)**: 단일 책임 원칙 (클래스는 단 하나의 변경 이유만 가져야 함).
- **O (OCP)**: 개방-폐쇄 원칙 (확장에는 열려있고, 변경에는 닫혀있어야 함 - Interface 활용).
- **L (LSP)**: 리스코프 치환 원칙 (자식 클래스는 부모 클래스를 완벽히 대체 가능해야 함).
- **I (ISP)**: 인터페이스 분리 원칙 (범용 인터페이스 하나보다 얇은 여러 개가 나음).
- **D (DIP)**: 의존성 역전 원칙 (구체화된 클래스보다 추상화된 인터페이스에 의존하라).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 개발 방법론 패러다임 비교: 폭포수 vs 애자일
| 비교 항목 | 폭포수 (Waterfall) | 애자일 (Agile / Scrum) | 기술적 파급 (시너지) |
| :--- | :--- | :--- | :--- |
| **프로세스 흐름** | 순차적, 하향식 (돌아갈 수 없음) | 반복적, 점진적 (Iterative & Incremental)| 요구사항 불확실성에 대한 방어력 |
| **요구사항 변경** | 변경을 오류나 실패로 간주 (경직성) | 변화를 환영하고 경쟁 우위로 활용 | 비즈니스 민첩성(Agility) 극대화 |
| **고객 참여도** | 프로젝트 초기(요구)와 말기(인수) | 전체 Sprint 주기에 걸쳐 상시 참여 | Product Market Fit (PMF) 적중률 증가 |
| **최종 산출물** | 프로젝트 종료 시점의 거대한 문서/시스템 | 주기마다 동작하는(Shippable) 소프트웨어 조각 | 빠른 피드백 루프 완성 |
| **적합한 도메인** | 요구사항이 명확한 국방, 항공, 인프라망 | 요구사항이 급변하는 B2C 웹, 모바일 서비스 | 도메인 특성에 따른 테일러링 필수 |

#### 2. 소프트웨어 아키텍처 구조 비교: Monolithic vs MSA
| 비교 항목 | 모놀리식 아키텍처 (Monolithic) | 마이크로서비스 아키텍처 (MSA) |
| :--- | :--- | :--- |
| **시스템 구조** | 모든 컴포넌트가 하나의 거대한 코드베이스로 통합 | 비즈니스 도메인(Bounded Context)별 독립된 서비스 |
| **결합도 (Coupling)** | 극도로 강한 결합 (하나의 DB, 메모리 공유) | 느슨한 결합 (API/이벤트 통신, 서비스별 개별 DB) |
| **확장성 (Scaling)** | 스케일 아웃 시 전체 시스템을 복제해야 함 (비효율) | 부하가 몰리는 특정 서비스 모듈만 스케일 아웃 가능 |
| **기술 부채 및 장애**| 작은 버그가 전체 시스템 패닉을 유발 (SPOF) | 특정 서비스의 장애가 타 서비스로 전파되지 않음 (Circuit Breaker) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1: 금융 코어 뱅킹 시스템의 MSA 차세대 전환**
- **문제 상황**: 20년 된 C/Java 기반의 모놀리식 코어 뱅킹 시스템이 수백만 줄의 스파게티 코드로 변질되어, 신규 대출 상품 하나를 출시하는 데 6개월이 소요됨.
- **기술사적 결단**: 무리한 빅뱅(Big-bang) 방식의 전면 재구축을 배제하고, **스트랭글러 피그(Strangler Fig) 패턴**을 도입한다. DDD(Domain-Driven Design)를 통해 비핵심 도메인(알림, 마이데이터 등)부터 점진적으로 분리하여 마이크로서비스로 전환하며, API Gateway를 앞단에 두어 레거시와 신규 시스템 간의 트래픽을 정교하게 라우팅하는 무중단 마이그레이션 아키텍처를 강제한다.

**시나리오 2: 글로벌 이커머스 플랫폼의 배포 병목 타파**
- **문제 상황**: 개발팀과 운영팀의 사일로(Silo)로 인해 정기 배포일마다 밤샘 작업과 치명적 롤백(Rollback)이 반복됨.
- **기술사적 결단**: 애자일 방법론과 DevOps 문화를 융합한다. GitHub Actions와 ArgoCD를 결합한 **GitOps 기반의 CI/CD 자동화 파이프라인**을 구축. 정적 코드 분석(SonarQube)과 80% 이상의 단위 테스트 커버리지를 통과하지 못하면 Merge를 원천 차단(Quality Gate)하고, **카나리(Canary) 배포**를 통해 1%의 유저에게만 선배포하여 에러를 관측(Observability)하는 안전망을 확보한다.

**도입 시 고려사항 (안티패턴)**
- **분산 시스템의 Fallacy 무시**: 네트워크는 항상 신뢰할 수 있고 지연이 0이라고 가정하는 안티패턴. 마이크로서비스 도입 시 서비스 간 동기식 HTTP 호출이 연쇄적으로 물려 있으면 타임아웃 폭풍(Cascading Failure)이 발생한다. 반드시 이벤트 기반(Kafka) 비동기 아키텍처와 서킷 브레이커(Circuit Breaker) 패턴을 조합해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량적 기대효과 (ROI)**
| 공학적 방법론 적용 | 적용 결과 및 정량적 지표 개선 (ROI) |
| :--- | :--- |
| **CI/CD 파이프라인 도입** | 수작업 배포 제로화, 배포 리드 타임(Lead Time) 주 단위에서 분 단위로 **99% 단축** |
| **정적 분석 및 TDD 적용** | 운영 환경의 치명적 결함(Defect) 발생률 **80% 이상 억제** (Shift-Left Testing 효과) |
| **객체지향 리팩토링** | 코드 순환 복잡도(Cyclomatic Complexity) 감소로 유지보수 비용(TCO) **40% 절감** |

**미래 전망 및 진화 방향**:
소프트웨어 공학의 미래는 'AI-Augmented Engineering'으로 압살된다. 깃허브 코파일럿(Copilot)과 같은 생성형 AI가 단순 코딩(Implementation)을 완벽히 대체함에 따라, 개발자의 역할은 '요구사항을 정교한 프롬프트로 변환'하고 생성된 코드의 '아키텍처 정합성을 감리'하는 상위 레벨의 오케스트레이터로 격상될 것이다. 

**※ 참고 표준/가이드**:
- ISO/IEC 25010: 소프트웨어 품질 평가(SQuaRE) 8대 주특성 국제 표준 (기능성, 신뢰성, 사용성, 효율성, 유지보수성 등).
- ISO/IEC 12207: 소프트웨어 생명주기 프로세스 국제 표준.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [`[애자일과 스크럼]`](@/PE/4_software_engineering/1_sdlc/_index.md): 불확실성 속에서 소프트웨어를 점진적으로 개발하는 현대적 프레임워크.
- [`[소프트웨어 테스트 (QA)]`](@/PE/4_software_engineering/2_quality/_index.md): 버그를 찾고 시스템의 신뢰성을 증명하는 화이트박스/블랙박스 기법.
- [`[디자인 패턴 (GoF)]`](@/PE/4_software_engineering/1_sdlc/_index.md): 반복되는 구조적 문제를 해결하기 위한 선배 아키텍트들의 객체지향 족보.
- [`[데브옵스 및 CI/CD]`](@/PE/15_devops_sre/_index.md): 공학적 개발 철학을 배포와 인프라 운영 영역까지 확장한 실천론.
- [`[마이크로서비스 (MSA)]`](@/PE/4_software_engineering/_index.md): 클라우드 시대에 응집도를 높이고 결합도를 끊어낸 궁극의 아키텍처 패턴.