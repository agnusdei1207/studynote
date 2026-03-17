+++
title = "18. PSP & TSP - 개인과 팀의 조화로운 프로세스"
date = "2026-03-16"
+++

# 18. PSP & TSP - 개인과 팀의 조화로운 프로세스

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PSP (Personal Software Process)는 소프트웨어 개발자가 개인의 작업 시간, 결함, 크기 등을 정량적으로 측정하여 자기 완료(Self-Control) 능력을 기르는 훈련 체계이며, TSP (Team Software Process)는 이러한 자기 관리형 인재들이 모여 자율 주도적으로 프로젝트를 수행하는 팀 워크 방법론이다.
> 2. **가치**: 주관적인 '감(Feeling)'이 아닌 객관적인 '데이터(Metrics)'에 기반하여 공수(Effort)와 일정(Schedule)을 예측함으로써, 소프트웨어 프로젝트의 고질적인 문제인 일정 지연과 잦은 결함 발생을 획기적으로 해결하여 생산성을 2배 이상 향상시킨다.
> 3. **융합**: CMMI (Capability Maturity Model Integration)의 Level 4/5 정량적 관리(Quality Management) 실천 도구로서, 현대 애자일(Agile)의 메트릭스 기반 개발 및 DevOps의 데이터 주도 문화와 맥락을 같이하며 고성과 조직(High-Performance Team) 구축의 핵심 근간이 된다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
소프트웨어 위기(Software Crisis)가 대두되면서 많은 조직이 프로세스 개선에 투자했으나, 개발자 개인의 역량이 뒷받침되지 않으면 프로세스는 무용지물이 되곤 했습니다. 이를 해결하기 위해 SEI (Software Engineering Institute)의 와츠 험프리(Watts Humphrey)는 **"프로세스를 개선하려면 프로세스를 사용하는 사람, 즉 엔지니어가 먼저 변해야 한다"**는 철학을 바탕으로 PSP를, 이를 확장하여 TSP를 고안했습니다.

**2. 등장 배경 및 필요성**
① **개발자의 맹목적 비관/낙관**: "이번 주에는 끝낼 수 있을 것 같다"는 근거 없는 희망이나 공포로 인해 일정이 실패함.
② **CMMI의 실천 부재**: 조직 차원의 프로세스는 정의되어 있으나, 개인이 어떻게 해야 할지 구체적 가이드 부재.
③ **데이터 기반 문화의 정착**: '정량적 관리(Quantitative Management)'를 통해 프로젝트의 불확실성을 제거하고 예측 가능한 엔지니어링 추구.

**3. 💡 비유 (Analogy)**
PSP는 **'항공 조종사의 비행 일지(Flights Log)'**와 같습니다. 조종사는 매 비행마다 이륙 시간, 경로, 연료 소모량, 기상 상태를 기록하여 다음 비행의 완벽한 계획을 세웁니다. 이러한 준비된 조종사들이 모여 '에어 트래픽 컨트롤'이라는 거대한 시스템(TSP) 속에서 조화를 이루며 안전하고 정확하게 항공기를 운항하는 것과 같습니다.

**📢 섹션 요약 비유**: 개인이 자신의 컨디션과 기록을 완벽히 관리하는 '마라톤 선수의 훈련 일지'가 모여, 팀 전체가 우승을 위해 작전을 짜는 '팀 전술'로 확장되는 과정입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. PSP (Personal Software Process)의 구성 요소**
PSP는 개발자가 코딩(Coding)하는 시간 뿐만 아니라, 계획(Planning)하고 검토(Review)하는 시간까지 모두 측정하고 관리하는 체계입니다. 크게 **개선 프로세스(Improvement Loop)**와 **측정 프로세스(Measurement Loop)**로 나뉩니다.

| 구성 요소 (Component) | 역할 (Role) | 상세 동작 (Mechanism) | 주요 산출물 (Artifact) | 비고 (Note) |
|:---:|:---|:---|:---|:---|
| **SCRIPT (스크립트)** | 단계별 가이드 | 각 개발 단계(계획, 설계, 코딩, 테스트)의 수행 절차 정의 | Process Script | 표준화된 작업 절차 |
| **FORM (폼)** | 데이터 수집 | 시간, 결함, 크기(Size) 등을 기록하는 서식 | Time/Defect Log | 객관적 데이터 원천 |
| **STANDARD (표준)** | 기준선 제공 | 결함 유형별 분류표, 크기 산정표 제공 | Size Standard | 데이터의 일관성 확보 |
| **PROXY (대치치)** | 크기 예측 | 실제 LOC(Line of Code)가 없을 때, 관련 객체/메서드 수로 추정 | Estimated Proxy | 초기 프로젝트 예측력 |
| **METHOD (방법론)** | 품질 개선 | 설계 검토(Design Review), 코드 검토(Code Review) 방법론 | Review Checklist | 결함 조기 제거 |

**2. PSP의 심층 동작 원리: 계획-추적-분석 루프**
PSP는 단순한 기록이 아니라, 과거 데이터를 현재 프로젝트의 **Plan(계획)**에 적용하고, 실제 수행한 **Actual(실적)**과 비교하여 분석하는 피드백 시스템입니다.

```text
[ PSP Improvement Cycle ]

      ┌──────────────────────────────────────────────┐
      │          1. PLAN (계획 수립)                 │
      │   - 과거 데이터 기반 크기 산정(Size Est.)     │
      │   - 예상 결함 밀도(Defect Density) 설정      │
      │   - 리스크 사전 식별                         │
      └───────────────┬──────────────────────────────┘
                      ▼
      ┌──────────────────────────────────────────────┐
      │       2. DO & MEASURE (개발 및 측정)          │
      │   ┌────────┐  ┌────────┐  ┌────────┐       │
      │   │Design │→ │ Coding │→ │ Compile│       │
      │   └────▲───┘  └────▲───┘  └────▲───┘       │
      │        │Time/Defect Log (Real-time Tracking) │
      └───────────────┬──────────────────────────────┘
                      ▼
      ┌──────────────────────────────────────────────┐
      │       3. POST MORTEM (사후 분석)              │
      │   - 계획(Plan) vs 실적(Actual) 분석          │
      │   ├── 수치적 오차(Cumulative Error) 계산     │
      │   ├── 결함 제거 효율성 검증                  │
      │   └── 다음 프로젝트를 위한 프로세스 업데이트 │
      └──────────────────────────────────────────────┘
```

**3. 핵심 알고리즘: PROBE (PROxy-Based Estimating)**
PSP의 가장 강력한 무기는 **PROBE** 방법론입니다. 이는 아직 코드가 작성되지 않은 상태에서 과거 데이터(회귀 분석)를 기반으로 작업량을 예측하는 기법입니다. 수식은 다음과 같습니다.

> **예측 LOC = $\beta_0 + \beta_1 \times$(객체/메서드 수)**

여기서 $\beta_0, \beta_1$은 개발자가 과거 10개 이상의 프로젝트 데이터를 통해 도출한 회귀 계수(Regression Coefficient)입니다. 이를 통해 예상 결함 수와 시간을 산출합니다.

```python
# PROBE Methdology Pseudo-code
class PSP_Estimator:
    def estimate_size(self, new_item_count, historical_data):
        # Linear Regression: y = a + bx
        # x: Item Count, y: Actual LOC
        beta_1, beta_0 = self.calculate_regression(historical_data)
        
        estimated_loc = beta_0 + (beta_1 * new_item_count)
        
        # Predict Time based on historical productivity (LOC/Hour)
        estimated_time = estimated_loc / self.get_avg_productivity()
        
        # Predict Defects based on historical Defect Density
        estimated_defects = estimated_loc * self.get_avg_defect_density()
        
        return estimated_loc, estimated_time, estimated_defects
```

**4. TSP (Team Software Process)의 팀 구조 및 프로세스**
TSP는 PSP를 완료한(즉, 자기 관리 능력이 있는) 팀원들이 모여 프로젝트를 수행하는 방법론입니다. 팀은 단순한 집단이 아니라 **자율 주도 팀(Self-Directed Team)**으로 운영됩니다.

*   **역할(Role) 기반 구조**: 프로젝트 리더(PL), 설계 리더, 구현 리더, 품질 관리자 등 명확한 역할 부여.
*   **Launch (착수 미팅)**: 프로젝트 시작 시 4일 이상의 워크숍을 통해 팀 규칙(Team Charter), 목표, 계획을 수립.

```text
[ TSP Operational Architecture ]

┌───────────────────────────────────────────────────────────┐
│                    TSP Team Structure                     │
├───────────────────┬───────────────────┬───────────────────┤
│ [Role: Project Leader]      [Role: Planning Manager]      │
│ - Goal Setting               - Schedule Tracking          │
│ - Interface Mgmt             - Risk Management            │
├───────────────────┼───────────────────┼───────────────────┤
│ [Role: Design Manager]      [Role: Implementation Leader] │
│ - Architecture               - Development                │
│ - Technology Selection       - Code Review                │
├───────────────────┼───────────────────┼───────────────────┤
│ [Role: Quality Manager]     [Role: Support Manager]       │
│ - Process Adherence          - Environment/Legal          │
│ - Defect Analysis            - Documentation              │
└───────────────────┴───────────────────┴───────────────────┘
                            ▼
          ┌─────────────────────────────────────┐
          │       Development Cycles            │
          │  ┌──────────┐    ┌──────────┐       │
          │  │Strategy  │    │Development│      │
          │  └──────────┘    │Post-Mortem│       │
          │   (Plan)         └──────────┘ (Eval)│
          └─────────────────────────────────────┘
```

**해설 (Diagram Explanation)**:
TSP는 수평적이거나 무질서한 팀이 아니라, 각 팀원이 **자신의 분야를 책임지는 전문가 역할**을 수행하는 체계적인 구조입니다. 각 매니저는 자신의 성과를 PSP 데이터를 통해 팀에 보고하며, 전체 팀은 **Launch(착수)** 단계에서 설정한 전략을 기반으로 **Cycle(주기)** 를 돌며 진행 상황을 점검합니다. 이때 각 개인은 자신의 PSP 데이터를 통해 팀 목표에 기여하고 있는지 실시간으로 확인합니다.

**📢 섹션 요약 비유**: PSP는 정비사가 비행기의 나사 하나하나를 점검하고 기록하는 '미세한 정비 매뉴얼'이라면, TSP는 그런 정비사들이 모여 비행기의 안전한 비행 경로를 짜고 비행 중 서로 소통하는 '공중 교통 관제 시스템'과 같습니다. 개인의 데이터 정확도가 전체 시스템의 안정성을 결정합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. PSP/TSP vs 애자일(Agile) 방법론 비교**
많은 사람들이 PSP/TSP를 **전통적(Waterfall)**이라고 오해하지만, 실제로는 **데이터 기반의 애자일(Data-Driven Agile)**과 매우 유사하며 상호 보완적입니다.

| 비교 항목 | PSP/TSP | 전통적 애자일 (Traditional Agile) | 융합적 시사점 |
|:---|:---|:---|:---|
| **계획 (Planning)** | **정량적 예측**: 과거 데이터(Log)를 기반으로 매우 정밀한 규모/일정 예측 | **상대적 예측**: Story Point 등 개발자의 주관적 감각에 의존 | PSP의 데이터 예측력으로 애자일의 불확실성 보완 가능 |
| **품질 (Quality)** | **사전 예방**: 개인의 개별 검토(Peer Review)로 결함 조기 제거 | **사후 검증**: 테스트 주도 개발(TDD), 인수 테스트 | TSP의 품질 지표를 이용해 애자일 팀의 '기술 부채' 시각화 가능 |
| **진단 (Metrics)** | **Hard Metrics**: 시간, 결함 수, 컴파일 시간 등 객관적 수치 사용 | **Soft Metrics**: 번다운 차트, 속도(Velocity) 등 추세 위주 | PSP를 통해 수집된 하드 데이터가 애자일 대시보드의 정확도 높임 |
| **수정 주기 (Cycle)** | TSP Cycle (Build~Inspect~Learn) | Sprint (1~2 Weeks Iteration) | TSP의 구조적 루프를 Sprint Planning으로 대체하여 적용 가능 |

**2. 타 과목 융합 관점 (Convergence)**
*   **SW 공학(Management)**: **CMMI (Capability Maturity Model Integration)**의 Level 4(Quantitatively Managed)와 Level 5(Optimizing)를 달성하기 위한 실질적인 도구입니다. 조직의 프로세스 성숙도가 높아질수록 개인의 능력(PSP)이 프로젝트 성공에 미치는 영향이 결정적이 됩니다.
*   **통신 및 네트워킹 (Data Flow)**: 프로젝트 진행 상황을 추적하는 **Dashboard** 구축 시, 네트워크를 통해 각 개발자의 로그가 실시간으로 수집되어 중앙 서버에 집계되는 구조는 분산 데이터베이스 및 클라우드 아키텍처와 연계됩니다.
*   **데이터베이스 (DB)**: 수집된 방대한 결함 데이터와 시간 데이터를 저장하기 위해 설계된 **Repository**는 데이터베이스 정규화와 인덱싱 기술이 필요하며, 이를 분석하는 과정은 데이터 마이닝(Data Mining) 기술과 연결됩니다.

**📢 섹션 요약 비유**: PSP/TSP는 '인체의 신경계와 면역 체계'와 같습니다. 개인의 신경(PSP)이 끊임없이 자극을 감지하고 뇌(TSP)로 보고하며, 이를 통해 전체 몸(조직)이 스스로 학습하고 강해져 외부 바이러스(결함/장애)에 대응하는 것입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**
*   **Case 1: 일정 준수율이 낮은 팀**
    *   **상황**: 매번 스프린트(Sprint) 일정을 못 지키는 팀.
    *   **PSP 적용**: 팀원들에게 최근 3개월간의 작업 시간과 결함 수를 로그(Log)로 작성하게 하고