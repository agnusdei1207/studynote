+++
title = "658. 애자일 스크럼 (Scrum) 역할 분담"
date = "2026-03-15"
weight = 658
[extra]
categories = ["Software Engineering"]
tags = ["Agile", "Scrum", "Product Owner", "Scrum Master", "Development Team", "Project Management"]
+++

# 658. 애자일 스크럼 (Scrum) 역할 분담

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 예측 불가능한 복잡한 문제 해결을 위해 **투명성(Transparency)**, **검사(Inspection)**, **적응(Adaptation)**의 경험적 프로세스 관리 이론을 구현한 경량화된 아키텍처이다.
> 2. **구조**: 비즈니스적 가치를 최우선으로 정의하는 **PO (Product Owner)**, 프로세스 효율 및 장애물을 제거하는 **SM (Scrum Master)**, 실질적 구현을 담당하는 자기 조직화된 **DT (Development Team)**의 3개 역할이 삼위일체를 이룬다.
> 3. **효용**: 워터폴(Waterfall) 모델 대비 **TTM (Time to Market)**을 단축하고, 지속적인 피드백 루프를 통해 리스크를 조기에 흡수하여 프로젝트 실패율을 획기적으로 낮춘다.

---

### Ⅰ. 개요 (Context & Background)

**애자일(Agile)** 선언문의 핵심 가치인 "프로세스와 도구보다 개인과 상호작용"을 실천하기 위해 가장 널리 채택되는 프레임워크인 **스크럼(Scrum)**은, 1986년 하버드 비즈니스 리뷰에 게재된 '새로운 새로운 제품 개발 게임(The New New Product Development Game)' 논문에서 Takeuchi 및 Nonaka가 제시한 럭비의 대형(Scrum) 개념에서 유래하였습니다. 이는 변화하는 환경 속에서 정해진 계획의 고집보다는, 짧은 주기의 **반복(Iteration)**과 **점진적(Incremental)**인 개발을 통해 최종 목표에 유연하게 도달하는 경험적 접근법(Empirical Process Control)을 채택합니다.

전통적인 관리 방법론이 예측 가능한 환경에서의 '명령과 통제(Command and Control)'에 집중했다면, 스크럼은 불확실성이 높은 소프트웨어 개발 환경에서 **MVP (Minimum Viable Product, 최소 기능 제품)**를 빠르게 배포하고 시장의 반응을 검증하는 방식으로 진화했습니다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                     WATERFALL vs. SCRUM (변화 대응 방식)                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [Waterfall] : Plan -> Design -> Code -> Test -> Deploy                    │
│     (한 번의 큰 배팅. 중간에 변경 시 비용 기하급수적 증가)                     │
│                                                                            │
│     ▲                                                                     │
│     │  낭비(Waste) & 리스크 누적                                            │
│     ▼                                                                     │
│     ■----------------------------------------------------------------■    │
│     Time                                                                 │
│                                                                            │
│  [Scrum]     : ▩ -> ▩ -> ▩ -> ▩ -> ▩  (반복적 산출물)                       │
│     (짧은 주기마다 검증 및 수정 가능. 리스크 최소화)                           │
│                                                                            │
│     ▩ ▩ ▩ ▩ ▩                                                              │
│       ↕ ↕ ↕                                                               │
│    피드백 및 수정                                                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

이 아키텍처의 핵심은 '역할(Role)의 분리'에 있습니다. 비즈니스적 요구사항과 기술적 구현을 명확히 구분함으로써, 개발팀이 기술적 완성도에만 집중할 수 있는 환경을 제공합니다.

> **📢 섹션 요약 비유**:
> 스크럼은 **고속주행하는 F1 레이싱 팀**과 같습니다. 운전자(개발팀)는 속도를 내는 데 집중하고, 피트 크루(스크럼 마스터)는 타이어 교체 및 장애물 제거에 집중하며, 팀 오너(PO)는 경기 흐름을 보며 전략을 내리는 것처럼, 각자의 전문 영역에서 최고의 효율을 냅니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스크럼 팀은 보통 10명 이하로 구성되며, **계층(Hierarchy)** 없이 수평적으로 협업합니다. 각 역할은 상호 배타적이지만 보완적인 책임을 가집니다.

#### 1. 상세 역할 정의 및 책임 매트릭스

| 역할 (Role) | 전체 명칭 (Full Name) | 핵심 책임 (Accountability) | 주요 산출물 (Artifact) | 성공 측정 지표 (KPI) |
|:---:|:---|:---|:---|:---|
| **PO** | **Product Owner** | 제품 백로그(PBL) 관리, **ROI (Return on Investment)** 최적화, 의사결정 | User Story, Acceptance Criteria, PBL Priority | Released Feature Count, Business Value Delivered |
| **SM** | **Scrum Master** | 팀 코칭, ** impediment(장애물) 제거**, 프로세스 개선, 스트롱(Strong) 서번트 리더십 | Updated Scrum Board, Impediment List | Team Velocity Stability, Happiness Metric |
| **DT** | **Development Team** | **Increment(증분)** 개발, 테스트, 배포, 셀프 컴포지션(Self-composition) | Working Software (Potentially Releasable), Sprint Burndown Chart | Defect Density, Sprint Goal Success Rate |

#### 2. 스크럼 이벤트 및 데이터 흐름 아키텍처

스크럼의 정교한 작동은 5가지 이벤트(Ceremony)와 3가지 산출물(Artifact)의 상호작용으로 이루어집니다.

```text
   [ Stakeholders ] (고객/사용자)
          │ ▲
          │ │ (Feedback/Requirement)
          ▼ │
    ┌──────────────────┐
    │  PO (Product     │ ① Product Backlog (Prioritized by Value)
    │  Owner)          │──────────────────────────────────────┐
    └──────────────────┘                                      │
           │ decides "What"                                   │ PBL
           ▼                                                  │
    ┌──────────────────┐   Sprint Planning (Start)            ▼
    │ Sprint Backlog   │ ◀───────────────────────────┐   ┌─────────────┐
    │ (Selected Items) │                             │   │   Product   │
    └──────────────────┘                             │   │  Backlog    │
           │                                        │   └─────────────┘
           │ defines "How"                           │         ▲
           ▼                                        │         │
    ┌──────────────────────────┐  Daily Scrum       │         │
    │ Development Team (DT)    │ ◀───────┐          │         │
    │                          │         │ (Sync)   │         │
    │   [Sprint Execution]     │         └──────────┘         │
    │   Coding / Testing /     │                              │
    │   Integration /          │                              │
    └──────────────────────────┘                              │
           │ creates                                       │
           │      ③ Potentially Releasable Increment       │
           ▼ (Deliver)                                     │
    ┌──────────────────┐   Sprint Review (End)              │
    │   Increment      │ ────────────────────┐              │
    │  (Working SW)    │                     │ Demo/Inspect │
    └──────────────────┘                     ▼              │
             ▲                           [Stakeholders]     │
             │                                               │
    ┌─────────────────┐                                     │
    │  Sprint         │  Sprint Retrospective (Improve)     │
    │  Retrospective  │ ◀─────────────────────────────────────┘
    │                 │
    └─────────────────┘
      (Action Items)
```

**[다이어그램 심층 해설]**
위 다이어그램은 스크럼의 심장부인 **피드백 루프(Feedback Loop)**를 도식화한 것입니다.
1.  **요구사항 유입**: PO는 외부 이해관계자로부터 요구사항을 받아 **PBL(Product Backlog)**에 우선순위별로 적재합니다.
2.  **계획 수립**: **스프린트 계획 회의(Sprint Planning)**에서 PO는 '무엇(What)'을, DT는 '어떻게(How)' 할지 정의하여 **SBL(Sprint Backlog)**으로 구체화합니다.
3.  **실행 및 동기화**: 개발팀은 SBL을 기반으로 개발하며, 매일 **데일리 스크럼(Daily Scrum)**을 통해 진행 상황을 동기화하고 장애물을 식별합니다.
4.  **검증 및 적응**: 주기가 끝나면 **스프린트 리뷰(Review)**를 통해 결과물을 시연하고 피드백을 받으며, **스프린트 회고(Retrospective)**를 통해 팀 프로세스 자체를 개선합니다. 이러한 루프는 소프트웨어의 품질뿐만 아니라 팀의 성숙도를 지속적으로 높이는 핵심 메커니즘입니다.

> **📢 섹션 요약 비유**:
> 스크럼의 백로그와 스프린트는 **냉장고 재료와 식단**과 같습니다. Product Owner는 냉장고 재료를 관리하고, 개발팀은 그날의 식단(Sprint Backlog)을 정해 요리합니다. 매일 식사 후(Review) 식사 맛을 평가하고, 요리 도구를 정리하는 것(Retrospective)이 스크럼의 사이클입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

스크럼 역할 모델의 진정한 가치는 다른 기술 영역과 결합할 때 발휘됩니다. 특히 **DevOps**와 **AI** 분야와의 융합은 필수적입니다.

#### 1. 역할 비교: PM vs. Scrum Master

| 구분 | PM (Project Manager) | SM (Scrum Master) |
|:---|:---|:---|
| **권력 형태** | 수직적, 명령형 (Authority) | 수평적, 영향력 (Influence) |
| **목표** | 계획 준수, 일정 준수 | 프로세스 순찰, 팀 개선 |
| **작업 할당** | 일을 사람에게 할당 (Task Assignment) | 사람이 일을 스스로 선택 (Pull System) |
| **책임 소재** | 프로젝트 성공/실패 책임 | 팀의 효율성 및 코칭 책임 |
| **의사결정** | PM이 결정 | 팀이 합의하여 결정 (Consensus) |

#### 2. 기술 융합: 스크럼 + DevOps (CI/CD)

스크럼의 성공은 **DevOps** 문화와 도구(특히 **CI/CD**)에 의존적입니다.
*   **Problem**: 스크럼에서는 짧은 주기로 '잠재적으로 배포 가능한 제품(Potentially Releasable Increment)'을 만들어야 합니다. 하지만 수동 배포가 필요하다면 이는 불가능합니다.
*   **Solution**: **Jenkins**나 **GitLab CI**와 같은 파이프라인을 구축하여 코드 커밋 시 자동 빌드/테스트/배포가 이루어지도록 해야 합니다.
*   **Synergy**: PO는 언제든 기능을 릴리즈할 수 있는 신뢰(Deployability)를 얻고, DT는 반복적인 수동 작업(Manual Regression Testing)에서 해방되어 창의적인 개발에 집중합니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Scrum DevOps Integration Loop                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Scrum Event]          [DevOps Technical Action]          [Outcome]        │
│                                                                             │
│  Sprint Planning ─────▶ Feature Branch Strategy ─────▶ Focused Dev         │
│       │                                                  (Decoupled)       │
│       ▼                                                                     │
│  Daily Development ──▶ Git Commit/Push                                     │
│       │                 │                                                   │
│       │                 ▼                                                   │
│       │            [CI Pipeline] ─────────────────▶ Automated Test         │
│       │                 │ (Build/Unit/Integration)      (Fast Feedback)    │
│       │                 ▼                                                   │
│       ▼            [CD Pipeline] ─────────────────▶ Auto Deployment        │
│  Sprint Review  ◀──   │ (Staging/Production)           (On-Demand)         │
│       │                                                                       │
│       ▼                                                                       │
│  Sprint Retro ──────▶ Pipeline Optimization ──────▶ Faster Delivery        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **📢 섹션 요약 비유**:
> 스크럼과 DevOps의 관계는 **자동차 경주 주행과 연료 주입**과 같습니다. 아무리 운전자(스크럼 팀)가 실력이 좋아도 연료 주입(배포 파이프라인)을 위해 매번 차에서 내려야 한다면 경주에서 이길 수 없습니다. 연료 주입이 주행 중에 자동으로 이루어져야(CD) 경주에 집중할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

이론적인 역할 분담이 실제 프로젝트에서 충돌할 경우, 기술사 및 아키텍트는 어떻게 판단해야 하는가?

#### 1. 딜레마 사례: PO의 기능 추가 요구 vs. DT의 품질 유지 주장

*   **상황**: PO가 스프린트 중간에 긴급 이슈로 인해 새로운 기능을 추가하려 함(중간 변경). DT는 기술적 부채(Technical Debt)가 쌓이고 있어 리팩토링이 시급하다고 주장하며 반대함.
*   **기술사적 판단 (Decision Framework)**:
    1.  **안정성 우선 원칙**: **WIP (Work In Progress)**를 제한하고, 진행 중인 스프린트 목표(Sprint Goal)를 방해하는 요청은 PO라 할지라도 다음 스프린트로 미루도록 권장.
    2.  **교환 트레이드(Trade-off)**: 불가피하게 변경이 필요하다면, DT가 희생할 다른 기능을 PO가 명시적으로 제거(Swap)하도록 유도하여 범위(Scope) 고정을 유지.
    3.  **데이터 기반 설득**: DT는 단순한 거부가 아닌, "리팩토링 미진으로 인한 추후 버그 수정 비용이 현재 개발 비용의 3배("Clean Code" 근거) 예상"과 같은 정량적 근거를 제시해야 함.

#### 2. 안티패턴: "Proxy PO"와 "SM의 힘남(Tech Lead)화"

*   **Proxy PO**: 실제 의사결정 권한이 없는 임원이 PO 역할을 대행하거나, PO가 실무를 몰라 BA(Business Analyst)에게 의존만 하는 경우.
    *   **결과**: 백로그 우선순위가 모호해지고("PO가 정해줘야 하는데..."), 스프린트 중간 방향성이 수시로 바뀌어 팀이 피폐해짐.
*   **Micro-Managing SM**: SM이 단순히 회