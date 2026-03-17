+++
title = "675. 프로젝트 관리 WBS, CPM, PERT"
date = "2026-03-15"
weight = 675
[extra]
categories = ["Software Engineering"]
tags = ["Project Management", "WBS", "CPM", "PERT", "Scheduling", "Network Diagram"]
+++

# 675. 프로젝트 관리 WBS, CPM, PERT

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로젝트의 범위를 명확히 정의하고 통제하기 위해 **WBS (Work Breakdown Structure)**로 계층 분할한 후, 작업 간 의존성을 **CPM (Critical Path Method)**과 **PERT (Program Evaluation and Review Technique)** 네트워크로 모델링하여 시간과 비용을 최적화하는 정량적 관리 기법이다.
> 2. **메커니즘**: **CPM**은 결정론적(Deterministic) 접근으로 최장 경로(Critical Path)를 찾아 일정을 통제하고, **PERT**는 확률론적(Probabilistic) 3점 추정을 통해 불확실성이 높은 R&D 프로젝트의 기대치를 계산하는 상호 보완적 메커니즘을 가진다.
> 3. **가치 및 융합**: 단순한 진척률 점검을 넘어, 병목(Constraint) 리소스를 식별하여 **Crashing**이나 **Fast Tracking** 전략을 수립하고, **EVM (Earned Value Management)**과 연계하여 일정(SV) 및 원가(CV) 효율을 예측할 수 있는 프로젝트 통제의 핵심 인프라이다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
프로젝트 관리에서 가장 큰 위험은 '범위의 막연함(Scope Creep)'과 '일정의 불확실성(Uncertainty)'이다. 이를 해결하기 위해 **PMBOK (Project Management Body of Knowledge)** 가이드에 따르면, 무형의 목표를 유형의 산출물 단위로 쪼개는 **WBS** 작업이 선행되어야 한다. WBS가 '무엇을(What)' 만들지를 정의한다면, **CPM**과 **PERT**는 '언제(When)' 완료할지를 수리적으로 모델링하는 도구이다. 특히, 소프트웨어 공학에서 개발 공수(Effort)와 실제 달력 일정(Duration)을 구분하여 예측하는 데 이 기법들은 필수적이다.

### 2. 등장 배경 및 기술적 진화
- **① 한계**: 1950년대 이전의 간트 차트(Gantt Chart)는 시간 흐름은 보여주지만, 작업 간의 상호 의존성(Dependency)과 그로 인한 연쇄적 지연 효과를 분석하기 어려웠음.
- **② 혁신**: 1958년 듀폰(DuPont) 사가 **CPM**을, 미 해군이 폴라리스 미사일 개발을 위해 **PERT**를 개발. 네트워크 이론을 도입하여 수천 개의 작업을 동시에 관리.
- **③ 현대**: 최근 애자일(Agile) 환경에서도 스프린트(Sprint) 계획 시 백로그(Backlog)의 의존성 관리를 위해 CPM/PERT의 변형된 알고리즘이 적용되고 있음.

### 3. 핵심 용어 및 기술 아키텍처 개요
- **WBS (Work Breakdown Structure)**: 프로젝트의 작업 분류 구조. 범위 관리의 기준.
- **CPM (Critical Path Method)**: 주공정 관리 기법. 결정론적 일정 산정.
- **PERT (Program Evaluation and Review Technique)**: 프로그램 평가 및 검토 기법. 확률론적 일정 산정.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Project Management Control Tower                         │
│                                                                              │
│   [1. Scope Definition]          [2. Scheduling Model]         [3. Control] │
│                                                                              │
│   ┌─────────────────┐            ┌──────────────────────┐       ┌─────────┐ │
│   │      WBS        │──────────▶ │      CPM / PERT      │───────▶ │ EVM/CPI │ │
│   │ (Hierarchy)     │   Mapping  │ (Network Diagram)    │ Analysis│   SPI   │ │
│   └─────────────────┘            └──────────────────────┘       └─────────┘ │
│          ▲                              │                                 │
│          │                              │                                 │
│   Deliverables                 Dependency Matrix                    Risk Mgmt│
│   (Scope)                      (A→B, B→C...)                        (ROI)   │
└─────────────────────────────────────────────────────────────────────────────┘
```
> **도해 해설**: 위 다이어그램은 프로젝트 관리의 3계층 구조를 보여줍니다. 가장 상위의 **WBS**가 프로젝트의 범위를 정의하면, 이 작업들은 **CPM/PERT** 엔진으로 입력되어 네트워크상의 시간 계산(ES, EF, LS, LF 등)을 거칩니다. 이렇게 계산된 기준 계획(Baseline)은 실제 수행되는 데이터와 비교되어 **EVM(Earned Value Management)**의 지수(SPI/CPI) 산출 근거가 됩니다.

---

### 📢 섹션 요약 비유
"거대한 요리 사업을 시작할 때, WBS는 '요리 재료와 조리 순서가 적힌 레시피'를 만드는 단계이고, CPM/PERT는 이 레시피를 바탕으로 '주방장이 여러 요리를 동시에 부엌에서 돌리기 위해 타이머를 맞추는 과정'이라고 볼 수 있습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. WBS (Work Breakdown Structure): 세부 설계
**WBS**는 프로젝트의 목표를 달성하기 위해 필요한 모든 작업을 계층적으로 분해한 구조입니다. 소프트웨어 공학에서는 이를 통해 SRS(Software Requirements Specification)에 명시된 기능을 개발 태스크 단위로 변환합니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Action) | 주요 산출물 (Deliverable) | 비고 (Note) |
|:---|:---|:---|:---|:---|
| **Level 1 (프로젝트 전체)** | 최상위 통제 | 프로젝트 전체 범위 정의 | Project Charter | 100% 요약 |
| **Level 2 (인도물 중심)** | 주요 단계 관리 | 하위 시스템 및 단계 구분 (설계/개발/테스트) | SRS, HLD | S/W 생명주기 기반 |
| **Work Package (최하위)** | 실행 단위 | **80 Hour Rule**: 1인 2주 이내 수행 가능 | Source Code, Test Cases | 비용/일정 산정 기초 |
| **WBS Dictionary** | 정의 명세서 | 각 패키지의 기술 상세, 담당자, 선행 조건 기술 | Statement of Work (SOW) | 모호성 제거 |

### 2. CPM (Critical Path Method): 결정론적 경로 분석
**CPM**은 각 작업의 소요 시간이 **확정적(Deterministic)**으로 주어졌을 때, 네트워크 상에서 가장 긴 시간 경로를 찾는 알고리즘입니다. 여기서 중요한 개념은 **Slack (Float)**입니다.

#### 알고리즘 및 주요 파라미터
- **ES (Early Start)**: 작업이 가장 빨리 시작할 수 있는 시점.
- **EF (Early Finish)**: 작업이 가장 빨리 끝날 수 있는 시점 ($EF = ES + Duration$).
- **LS (Late Start)**: 프로젝트 지연을 초래하지 않으면서 가장 늦게 시작할 수 있는 시점.
- **LF (Late Finish)**: 프로젝트 지연을 초래하지 않으면서 가장 늦게 끝날 수 있는 시점.
- **Total Float (총 여유 시간)**: $LS - ES$ 또는 $LF - EF$. **0**인 작업들이 모인 경로가 **Critical Path**임.

```text
    [Activity On Node (AON) Network Diagram Example]

     (2 Days)      (5 Days)      (3 Days)
    [ A: Start ]───────────────────────────────▶
       │                                           │
       │ (3 Days)                                 │
       ▼                                           ▼
    [ B: Design ] ───(4 Days)──▶ [ D: Merge ] ───▶ [ Finish ]
                         │                          ▲
                         └──────(6 Days)────────────┘
                           [ C: Module Test ]

    [ Critical Path Calculation Result ]
    Path 1: Start → A → D (2+3 = 5 Days)
    Path 2: Start → B → C → D (3+4+6 = 13 Days) ★ Critical Path
    Path 3: Start → B → D (3+4 = 7 Days)

    => 가장 긴 경로(Path 2)인 13일이 프로젝트 총 소요 기간이 됨.
    => Path 2의 모든 작업은 Slack이 0임. (하루 지연되면 프로젝트가 1일 지연됨)
```
> **도해 해설**: 위 예시는 소프트웨어 개발 과정을 단순화한 네트워크입니다. **A(요구분석)**, **B(설계)**가 병렬로 수행되거나, **B**가 끝나야 **C(코딩)**가 시작되는 의존 관계를 보여줍니다. 경로별 소요 시간을 합산했을 때 가장 큰 값(13일)이 프로젝트 최소 완료 기간이 됩니다. 이 경로상의 작업(B, C)에 리소스를 집중해야 함을 시각적으로 알 수 있습니다.

### 3. PERT (Program Evaluation and Review Technique): 확률론적 분석
**PERT**는 작업 시간이 불확실할 때 사용합니다. 낙관적($O$), 비관적($P$), 그리고 가장 가능성이 높은($M$) 시간을 추정하여 기대 시간($T_e$)과 분산($V$)을 계산합니다.

#### 핵심 수식 및 코드 로직
- **기대 시간 (Expected Time, $T_e$)**: 
    $$T_e = \frac{O + 4M + P}{6}$$
    (Beta 분포를 가정한 가중 평균)
- **분산 (Variance, $\sigma^2$)**: 
    $$V = \left( \frac{P - O}{6} \right)^2$$
    (불확실성의 정도)

```python
# Python-style Pseudo-code for PERT Calculation
class Task:
    def __init__(self, name, optimistic, most_likely, pessimistic):
        self.name = name
        self.O = optimistic
        self.M = most_likely
        self.P = pessimistic
    
    def calculate_pert(self):
        # Beta Distribution Weighted Average
        self.expected_time = (self.O + (4 * self.M) + self.P) / 6
        # Standard Deviation (Risk Level)
        self.std_dev = (self.P - self.O) / 6
        self.variance = self.std_dev ** 2
        return self.expected_time

# Example: Module Development
dev_task = Task("Dev_Module", 3, 5, 13) # 3일, 5일, 최악 13일
print(f"Expected: {dev_task.calculate_pert()} days") 
# Output: 6.0 days
print(f"Variance: {dev_task.variance}") 
# Output: 2.77 (High Uncertainty)
```
> **도해 해설**: 위 코드는 PERT 계산의 로직을 보여줍니다. 개발 작업은 기술적 난관으로 인해 소요 시간 편차가 큽니다(3일~13일). 단순 평균(7일)이 아닌 PERT 공식(6일)을 사용하면, 가중치가 부여된 보다 현실적인 일정 산정이 가능합니다. 이를 통해 관리자는 "이 작업은 분산이 크니 리스크 관리(Risk Management) 대상이다"라고 판단할 수 있습니다.

---

### 📢 섹션 요약 비유
"CPM은 철도 선로를 깔듯이 시간을 확정하고, 그 중 가장 중요한 간선(주공정)을 찾아 집중 투자하는 **'철도 시공 표준'**이라면, PERT는 날씨와 교통 상황에 따라 도착 시간이 달라질 수 있는 배달 시스템에서 **'가장 그럴듯한 도착 시간'**을 통계적으로 예측하는 **'내비게이션 알고리즘'**과 같습니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: CPM vs PERT

| 비교 항목 (Criteria) | CPM (Critical Path Method) | PERT (Program Evaluation and Review Technique) |
|:---:|:---|:---|
| **시간 추정 모델** | **Deterministic (결정론적)** | **Probabilistic (확률론적)** |
| **입력 파라미터** | 단일 시간 추정치 (1-point) | **3점 추정 (3-point)**: Optimistic, Most Likely, Pessimistic |
| **수학적 분포** | 정규 분포(Normal Distribution) 가정 | **베타 분포(Beta Distribution)** 가정 |
| **주요 관리 포인트** | **Cost-Time Tradeoff** (Crashing 비용 최적화) | **Time Estimate & Risk** (기간 예측 신뢰도) |
| **활용 분야** | 건설, 제조 (공정이 정형화됨) | **R&D, 신제품 개발, IT 프로젝트** (불확실성 높음) |
| **속도(계산 복잡도)** | 빠름 (단순 경로 합산) | 느림 (기댓값/분산 계산 필요) |

### 2. 타 영역(운영체제/네트워크)과의 융합 관점

#### ① 운영체제(OS)와의 연계: CPU 스케줄링 vs 프로젝트 일정 관리
- **OS의 CPM**: CPU 스케줄러(예: CFS - Completely Fair Scheduler)는 태스크의 실행 시간(Time Quantum)과 우선순위에 따라 **Critical Task**부터 먼저 할당합니다. 이는 리소스(CPU)가 한정적일 때 병목을 최소화한다는 목적에서 프로젝트의 CPM과 논리적으로 동일합니다.
- **차이점**: OS는 마감(Deadline)이 밀리초 단위이고 선점형(Preemption)이 가능하지만, 프로젝트 관리는 일 단위이며 작업을 쉽게 끊을 수 없습니다(Non-preemptive characteristics).

#### ② 네트워크 이론과의 연계: 최단 경로 vs 최장 경로
- 네트워크 라우팅(예: OSPF)은 **비용(Cost)이 가장 낮은 최단 경로(Shortest Path)**를 찾지만, CPM/PERT는 **소요 시간이 가장 긴 최장 경로(Longest Path)**를 찾습니다. 이는 프로젝트의 완료 시간이 모든 선행 작업의 완료 시점 중 가장 늦은 시점에 의해 결정되기 때문입니다.

```text
    [ Conceptual Convergence Diagram ]

    Network Routing (OSPF)          Project Management (CPM)
    ======================          =======================
    Minimize Cost (Hop/Delay)       Maximize Time (Duration)
    (Cost: 10 +