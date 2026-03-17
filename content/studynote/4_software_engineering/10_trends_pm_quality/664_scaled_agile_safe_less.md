+++
title = "664. 대규모 애자일 SAFe, LeSS"
date = "2026-03-15"
weight = 664
[extra]
categories = ["Software Engineering"]
tags = ["Agile", "Scaling Agile", "SAFe", "LeSS", "Enterprise Agile", "Governance"]
+++

# 664. 대규모 애자일 SAFe, LeSS

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 팀의 애자일(Agile) 한계를 극복하여, 조직 전체의 **전략적 정렬(Alignment)**과 **실행력**을 동시에 확보하는 엔터프라이즈급 프레임워크다.
> 2. **가치**: **SAFe (Scaled Agile Framework)**는 포트폴리오 거버넌스를 통해 제품 로드맵과 예산을 연계하고, **LeSS (Large-Scale Scrum)**는 스크럼의 경량성을 유지하며 수평적 확장을 지향한다.
> 3. **융합**: 소프트웨어 정의(Software Defined) 비즈니스 환경에서 **MSA (Microservices Architecture)**와 **DevOps (Development and Operations)** 문화를 기반으로, 시장 출시(Time-to-Market) 속도를 30~50% 단축시키는 핵심 동력이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학
대규모 애자일(Scaled Agile)은 단일 팀(5~9명)의 효율성을 넘어, 수백 명 이상의 조직이 하나의 가치 흐름(Value Stream)을 따라 협업할 때 발생하는 **'소통의 비용 증가'**와 **'전략의 파편화'** 문제를 해결한다. 단순히 스크럼(Scrum)을 여러 번 반복하는 것이 아니라, 조직 구조, 리더십, 그리고 거버넌스(Governance)를 근본적으로 변화시켜 조직 차원의 **'애자일성(Agility)'**을 확보하는 것을 목표로 한다.

### 💡 비유: 소규모 밴드와 거대 교향악단
일렉트릭 밴드(인디 밴드)가 눈빛만 교환해도 즉흥 연주가 가능하다면, 100명의 교향악단은 지휘자, 악보, 파트장 없이는 소음만 만들어낼 뿐이다. 대규모 애자일은 이 거대한 조직이 **'소박한 팀의 자율성'**을 잃지 않으면서도 **'전체 연주의 조화'**를 이루어내도록 돕는 '악보와 지휘 체계'와도 같다.

### 등장 배경 및 패러다임
① **기존 한계 (Waterfall-Silo)**: 전통적인 폭포수 모델과 부서 간 사일로(Silo)는 요구사항 전달 과정에서의 왜곡(전화 게임 효과)과 통합(Integration) 시점의 병목을 초래했다.
② **혁신적 패러다임 (System Thinking)**: 애자일 코칭(Agile Coaching)의 선구자들은 **'낭비 제거(Waste)'**와 **'지연 된 비용(Cost of Delay)'**을 최소화하기 위해 팀 간 의존성을 관리하는 구조적 메커니즘을 개발했다.
③ **비즈니스 요구 (Adaptability)**: 급변하는 시장 요구에 맞춰 복잡한 시스템(SoS, System of Systems)을 빠르게 수정하고 배포해야 하는 생존의 요구로 대두되었다.

### 📢 섹션 요약 비유
> "단순히 자전거(작은 팀)를 많이 모아둔다고 기차(대형 프로젝트)의 속도가 나는 것이 아니다. 이들을 연결하는 **'연결기(Coupling)'**와 **'신호 시스템(Governance)'**이 필요하다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 대규모 애자일 확장 전략 비교

| 구분 | **SAFe (Scaled Agile Framework)** | **LeSS (Large-Scale Scrum)** |
|:---|:---|:---|
| **핵심 철학** | **Structure & Governance**<br>(체계와 계층을 통한 통제) | **Simplicity & De-scaling**<br>(기존 스크럼 구조 유지 및 최소 확장) |
| **조직 단위** | **ART (Agile Release Train)**<br>(5~12개 팀, 50~125명) | **Requirement Area**<br>(4~8개 팀씩 그룹화) |
| **PO/SM 구조** | **PO (Product Owner)** & **SM (Scrum Master)**<br>(팀 전담) | **One Product Backlog**<br>(전체 PO 1명 + Area PO) |
| **계획 주기** | **PI (Program Increment)**<br>(8~12주 고정 주기) | **Sprint**<br>(팀별 유연적 주기, 1~4주) |
| **적합 환경** | 대규모 하드웨어/소프트웨어 복합 시스템<br>,(보안/규제 중심 조직) | 순수 소프트웨어 개발<br>,(높은 자율성 요구 조직) |

### 2. SAFe (Scaled Agile Framework) 상세 구조

SAFe는 4-Level 구조(Team, Program, Large Solution, Portfolio)를 통해 전략 집행을 관리한다.

```text
      [ Portfolio Level ] (전사 전략, 예산, 거버넌스)
             │
      +------v------+
      |  Solution   | (Large Solution Level - 선택 사항)
      |  Train      | (여러 ART의 통합, 규모가 큰 솔루션)
      +------+------+
             │
+-----------v-------------------v------------------...---------+
|         Program Level (ART: Agile Release Train)            |
|   +-----------------------------------------------------+   |
|   | RTE (Release Train Engineer) / System Arch / Product Mgmt|   |
|   |   +----------------+ +----------------+ +--------+    |   |
|   |   | Agile Team 1   | | Agile Team 2   | |Team ...|    |   |
|   |   | (5~10 Members) | | (5~10 Members) | |        |    |   |
|   |   +----------------+ +----------------+ +--------+    |   |
|   +-----------------------------------------------------+   |
|            ^       ^        ^             ^                |
|            |_______|________|_____________|________________|
|                   Shared Backlog & synchronized PI           |
+---------------------------------------------------------------+
             │
      [Team Level] (개발/테스트/배포 스크럼 수행)
```

**(해설)**
1.  **Portfolio Level**: C-level 경영진이 참여하여 **Epic(큰 몫의 가치)**을 정의하고 예산(Lean Budget)을 할당한다.
2.  **ART (Agile Release Train)**: SAFe의 핵심 실행 단위다. 50~125명(5~12개 팀)이 **PI Planning**이라는 행사를 통해 동기화되어 8~12주 동안 함께 출발하고 도착하는 가상의 기차다.
3.  **RTE (Release Train Engineer)**: 기차의 기관사 역할을 하며, 장애물을 제거하고 흐름을 관리하는 최종 책임자(Scrum of Scrums Master)다.

### 3. LeSS (Large-Scale Scrum) 상세 구조

LeSS는 "Scrum is Scrum"이라는 철학 아래, 계층을 최소화한다.

```text
          [ Product Owner (Single) ]
                   │
        +----------v-----------+-----------+-------...
        |      Component Area (Feature Team)       |
        |  +--------------+   +--------------+    |
        |  | Team A (20%) |   | Team B (20%) |    |
        |  | (Req Area 1) |   | (Req Area 2) |    |
        |  +--------------+   +--------------+    |
        |        │                  │            |
        |        v                  v            |
        |     [ Scrum Master (서로 협력) ]       |
        +-----------------------------------------+
                   │
          [ Product Backlog (Single) ]
          (요구사항에 따라 팀이 유동적으로 착수)
```

**(해설)**
1.  **One Backlog**: 모든 팀이 단 하나의 **Product Backlog**를 바라본다. PO(제품 책임자)가 백로그의 우선순위를 정하면, 팀들은 Sprint Planning 시점에 이를 분배하여 인수(Sprint Backlog)한다.
2.  **Component to Feature**: 기존의 계층적 구조(Component Team)에서 벗어나, 고객 가치를 완성할 수 있는 **Feature Team** 중심으로 조직을 재편한다.
3.  **최소 관리**: SAFe의 ART 관리자(RTE)나 PI Planning 같은 거대한 행사 대신, **Overall Retrospective** 등을 통해 팀 간 조율을 수행한다.

### 4. 핵심 프로세스: PI (Program Increment) Planning
SAFe의 성공 가동 엔진인 **PI Planning**은 **Fix Variable(고정된 날짜, 가변적 범위)** 원칙을 따른다.

```text
1. 준비 (Pre-PI):
   Business Vision → Architectural Runway 준비

2. PI Planning (2일간 집중 워크숍):
   ├─ Day 1: Draft Plans (각 팀별 계획 수립)
   │          └─ Confidence Vote (투표: 확신 정도)
   └─ Day 2: Final Plans & Management Review (조율 및 문제 해결)

3. 실행 (Execution: 8~12주):
   Bi-weekly (2주마다) System Demo / Scrum of Scrums

4. 회고 (IP Iteration):
   Inspect & Adapt (개선안 도출)
```

**(해설)**
조직 전체가 모여서 "다음 8주 동안 우리가 무엇을 만들 것인가?"를 시각화(Sticky Notes)하고, 팀 간 의존성(Dependency)을 즉시 식별하여 조율한다. 이는 수개월 후의 통합 실패를 예방하는 가장 강력한 동기화 도구다.

### 📢 섹션 요약 비유
> "SAFe는 **'정확한 시간표에 따라 운행되는 고속열차(ART)'**처럼 강력한 동기화와 구조를, LeSS는 **'넓은 바다를 항해하는 함대'**처럼 각 배가 자율적으로 항해하되 임무를 공유하는 유연성을 강조한다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 아키텍처 관점: 모놀리식 vs MSA (Microservices Architecture)
대규모 애자일의 성공은 시스템 아키텍처와 뗄 수 없는 관계다.

| 분석 항목 | Monolithic Architecture (모놀리식) | Microservices Architecture (MSA) |
|:---|:---|:---|
| **의존성 (Dependency)** | 높음 (한 명이 바꾸면 전체가 위험) | 낮음 (서비스별 독립적 배포 가능) |
| **팀 구조 (Conway's Law)** | 계층적 구조(개발/테스트/배포 분리) | **Cross-functional**(자율 팀, 풀스택) |
| **적합 프레임워크** | **SAFe** (강한 통제와 정렬 필요) | **LeSS** (팀 간 독립성 높음) |

*   **Conway's Law (콘웨이의 법칙)**: 소프트웨어 구조는 이를 만드는 조직의 커뮤니케이션 구조를 닮게 된다.
    *   **Sinergy**: MSA를 도입하면 서비스 간 결합도가 낮아져, **LeSS**와 같은 자율성 높은 프레임워크를 적용하기 유리해진다. 반대로, 엔터프라이즈 레거시 시스템(단일 DB) 환경에서는 **SAFe**의 강력한 계층 관리가 필수적이다.

### 2. DevOps (Development and Operations)와의 시너지

```text
        [ Agile Planning ] (SAFe PI or LeSS Sprint)
               │
               v
        [ Continuous Delivery Pipeline ]
       /          │             \
      /           │              \
  CI (Build)   CD (Deploy)   Release on Demand
(Circle CI)   (Argo CD)      (Feature Flag)
      │            │               │
      └────────────┴───────────────┘
           (Automated Verification)
```

*   **융합 관계**: 대규모 애자일은 수많은 팀의 코드가 매일 수천 회씩 빌드되고 통합되는 환경을 전제한다. 따라서 **CI/CD (Continuous Integration/Continuous Deployment)** 파이프라인 구축과 **DevSecOps (Security)**의 자동화 없이는 불가능하다.
*   **Architectural Runway**: SAFe에서 말하는 활주로는 기술적 부채(Technical Debt)를 관리하며, 팀들이 미래의 요구사항을 빠르게 구현할 수 있도록 기반을 닦아두는 활동으로, DevOps 인프라의 안정성이 이를 결정한다.

### 📢 섹션 요약 비유
> "MSA와 대규모 애자일의 관계는 **'모듈형 소파**와 같다. 소파가 여러 덩어리로 나뉘어 있어야(MSA) 집안 구조(조직)에 맞춰 자유롭게 배치(팀 자율성)하고 이동(재배치)할 수 있다. 거대한 통 덩어리(모놀리식)는 옮길 때 이동 장비(SAFe의 거대 관리 조직)가 필요하다."

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 분석 및 의사결정 트리

**[Case A: 금융권 코어 시스템 전환 (High Regualation, High Risk)]**
*   **상황**: 수천 개의 레거시 모듈이 얽혀 있고, 보안 감사와 규정 준수(Compliance)가 엄격함.
*   **판단**: **SAFe 도입** (Large Solution or Portfolio).
*   **이유**:
    1.  **관리(Control)**: 감사 추적성을 위해 역할(Role)과 이벤트(Event)가 명확한 SAFe가 유리함.
    2.  **동기화(Alignment)**: 수많은 팀이 한 명이라도 시스템을 멈추면 장애(Financial Block) 발생. **PI Planning**을 통해 동기화 필수.

**[Case B: 빅데이터 플랫폼 신규 개발 (Creative, Uncertainty)]**
*   **상황**: 기술 진화가 빠르고, 어떤 기능이 유저를 사로잡을지 불확실함. 팀의 자율성과 속도가 중요.
*   **판단**: **LeSS 도입**.
*   **이유**:
    1.  **단순성(Simplicity)**: SAFe의 복잡한 행사/문서/역할 대신, 스크럼 기본 원칙에 집중.
    2.  **고객 중심**: Product Owner가 팀원과 직접 소통하며 피드백 루프를 최단화함.

### 2. 도입 체크리스트 (Success Factors)

| 구분 | SAFe 도입 시 확인사항 | LeSS 도입 시 확인사항 |
|:---|