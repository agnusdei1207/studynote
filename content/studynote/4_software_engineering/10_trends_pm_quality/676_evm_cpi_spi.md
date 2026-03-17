+++
title = "676. EVM (Earned Value Management) SPI, CPI 계산"
date = "2026-03-15"
weight = 676
[extra]
categories = ["Software Engineering"]
tags = ["Project Management", "EVM", "SPI", "CPI", "Cost Management", "Performance Metrics"]
+++

# 676. EVM (Earned Value Management) SPI, CPI 계산

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로젝트의 **범위(Scope)**, **일정(Schedule)**, **비용(Cost)**이라는 3대 제약 조건을 통합적으로 관리하기 위해, 계획된 가치(PV)와 실제 성과(EV), 그리고 투입된 실제 비용(AC)을 결합하여 현재 성과를 정량화하는 **통합 성과 관리 기법(Integrated Performance Management)**이다.
> 2. **가치**: 단순한 진척률(%)이 아닌 **CPI (Cost Performance Index)**와 **SPI (Schedule Performance Index)**를 통해 현재의 생산성 저하 및 지연 요인을 조기에 탐지하며, 이를 기반으로 최종 비용(EAC)과 완료 예정일(EDAC)을 정밀하게 예측하여 객관적인 의사결정을 지원한다.
> 3. **융합**: 소프트웨어 공학의 **WBS (Work Breakdown Structure)**와 **기능점수(Function Point)** 분석과 결합하여, 단순 노무 투입이 아닌 '기능적 완성도'에 기반한 정교한 성과 측정을 가능하게 하며, 최근에는 **Agile EVM**과 연계되어 스크럼(Scrum) 환경의 번다운 차트와 융합되는 추세이다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학: "주관적 보고의 배제"
소프트웨어 프로젝트의 현장에서 흔히 발생하는 "90% 완료 증후군(90% Complete Syndrome)"—진척된 것 같지만 끝이 보이지 않는 상태—를 극복하기 위해 고안되었다. EVM (Earned Value Management)은 프로젝트의 현재 상태를 단순히 "몇 % 진행"이라는 상대적 개념이 아니라, **"기획된 예산 대비 실제로 만들어낸 가치는 얼마인가?"**라는 절대적 가치(금액)로 환산하여 판단한다. 이는 프로젝트 관리를 '예술(감)'의 영역에서 '과학(수치)'의 영역으로 끌어올리는 도구이다.

#### 2. 등장 배경 및 필요성
1960년대 미국 국방부(DOD)의 C/SCSC(Cost/Schedule Control Systems Criteria)에서 시작되어, 현재는 PMI(PMI, Project Management Institute) 및 ISO 21508 표준으로 정착되었다. 소프트웨어 개발의 경우, 생산성이 인건비에 의존도가 높고 불확실성이 크므로, 단순히 "예산을 절반 썼다"는 사실이 "일을 절반 했다"는 것을 의미하지 않는다. EVM은 이러한 **비용 소모와 가치 창출의 괴리**를 시각화하여, 프로젝트가 붕괴되기 전에 구조적 위기를 감지한다.

#### 3. EVM 기본 다이어그램 (개념적 도해)

```text
   [Project Status: Time Lag & Cost Overrun Scenario]
   ^ Cost ($)
   │
   │                                      ___________[ EAC ] (Estimate at Completion)
   │                                   __/   (Projected Final Cost)
   │                                __/
 BAC _____________________________/    (Budget at Completion)
 (Total Budget)                  /|    
                              /   |    
                            /     |    
                          /       |    ● [Current Point] (Analysis Date)
                        /         |    / 
                      /           |   /   <-- The 'S' Curve Gap
                    /             |  /    
        PV _______/               | /      
      (Planned)                   |/       
       (Baseline)                /|    ● AC (Actual Cost: Work done)
                               / |     
                             /   |    ● EV (Earned Value: Value delivered)
                           /     |     
   └───────────────────────────────────────────────────────────> Time
              Now        Analysis Date          Planned Finish
```
> **도해 해설**: 위 그래프는 전형적인 위기 상황의 프로젝트 모습입니다.
> - **PV (Planned Value)**: 원래 계획(S-Curve)보다 아래에 위치하여 **일정이 지연**되었음을 보여줍니다.
> - **AC (Actual Cost)**: EV보다 위에 위치하여 **비용 초과**가 발생했음을 나타냅니다.
> - **EAC (Estimate at Completion)**: 현재 추세선이 뻗어나가는 방향(BAC 상단)을 보면, 프로젝트가 종료될 때 예산(BAC)을 훨씬 초과하여 비용이 발생할 것임을 예측할 수 있습니다.

#### 📢 섹션 요약 비유
> "EVM은 마치 **복잡한 고속도로 톨게이트**를 지나는 차량을 관리하는 것과 같습니다. 단순히 '몇 대의 차가 지났는가(PV)'가 아니라, '실제로 통행료를 낸 차량은 몇 인가(EV)'와 '도로 유지보수비로 얼마를 썼는가(AC)'를 비교하여, 도로(프로젝트)가 돈을 잃고 있는지, 아니면 교통체증(지연)으로 인해 손해가 발생하는지를 즉각적으로 판단하는 고속 통계 시스템입니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석 (Components & Parameters)
EVM의 정확도는 **WBS (Work Breakdown Structure)**의 세분화 수준에 달려있다. 각 작업 패키지(Work Package)는 계측 가능한 단위(Measurable Unit)로 정의되어야 한다.

| 요소 (Element) | 전체 명칭 (Full Name) | 수학적 정의 (Formula) | 내부 동작 및 의미 (Operation) |
|:---:|:---|:---:|:---|
| **PV** | **Planned Value**<br>(계획된 가치) | $\sum (Planned\ Work \times Budget\ Rate)$ | 기준선(Baseline)에 따라 **'특정 시점까지 해야 할 일'**의 승인된 예산. |
| **EV** | **Earned Value**<br>(획득 가치/성과치) | $\sum (Actual\ Completed\ Work \times Budget\ Rate)$ | 실제 완료된 작업량에 **기획된 단가를 적용**한 가치. (실제 쓴 돈이 아님) |
| **AC** | **Actual Cost**<br>(실제 비용) | $\sum (Actual\ Costs)$ | 완료된 작업을 수행하는 데 **실제로 투입된 비용**. (인건비+재료비) |
| **BAC** | **Budget At Completion**<br>(완료시 총예산) | Total PV at End of Project | 프로젝트 기본 계획 상의 전체 예산. |
| **CPI** | **Cost Performance Index**<br>(비용수행지수) | $EV / AC$ | 투입된 1달러당 **얼마의 가치를 창출했는가**? (1.0 미만이면 초과) |
| **SPI** | **Schedule Performance Index**<br>(일정수행지수) | $EV / PV$ | 계획된 1시간/1달러 가치 대비 **얼마나 일을 진행했는가**? (1.0 미만이면 지연) |

#### 2. 핵심 알고리즘 및 예측 로직 (Prediction Logic)
현재의 성과(CPI, SPI)가 미래에도 지속된다고 가정할 때, 최종 결과를 예측하는 공식이다.

**A. EAC (Estimate at Completion) 계산 시나리오**
프로젝트의 상황에 따라 다른 공식을 사용해야 한다.
- **Scenario 1 (Typical)**: 현재의 CPI 문제가 원인을 해결하지 못해 프로젝트 종료 시까지 지속될 경우.
  $$EAC = \frac{BAC}{CPI}$$
- **Scenario 2 (Atypical)**: 현재의 일회성 문제였으며, 앞으로는 계획대로(BAC 기준) 진행될 경우.
  $$EAC = AC + (BAC - EV)$$

**B. VAC (Variance at Completion)**
$$VAC = BAC - EAC$$
(음수(-)면 예산 초과, 양수(+)면 예산 절감)

#### 3. 소프트웨어 EVM 데이터 흐름 및 상태 전이도

```text
      [WBS 기반 기획 단계]             [측정 단위(Work Package) 생성]
             (Budgeting)  -------------------------->  PV (Baseline)
                                                          │
                                                          ▼
           ┌─────────────────────────────────────────────────────────┐
           │               [Execution & Measurement Loop]            │
           │                                                         │
      [진행(Progress)]                                             [성과 분석]
   엔지니어 작업 수행   ──>  진척률(%) 산출       ---->   EV (획득 가치)
       (Input)              (Completion %)                 │
                                                          │
                                                          ▼
      회계/ERP 시스템   <----  인건비/Cloud비용 지급           │
      (Financials)       -------------------------------->  AC (실제 비용)
                                                          │
                                                          ▼
                  ┌─────────────────────────────────────────────────────┐
                  │         [Index Engine (CPU of EVM)]                │
                  │                                                     │
                  │  CPI = EV / AC    SPI = EV / PV                    │
                  │  CV = EV - AC     SV = EV - PV                     │
                  │       (Variance = 차액, Index = 비율)              │
                  └─────────────────────────────────────────────────────┘
                                    │
                                    ▼
                          [Forecasting Model]
                           EAC, ETC 계산
                       (미래의 비용/일정 예측)
```
> **도해 해설**: 이 다이어그램은 EVM의 심장부인 루프 구조를 보여줍니다.
> 1. **PV**는 초기에 고정된 기준선입니다.
> 2. **AC**는 돈이 나갈 때마다 증가합니다(과거 지향적).
> 3. **EV**는 기능이 완성될 때만 증가합니다(현재 지향적).
> 4. **Index Engine**에서 이 세 값이 충돌하며 **CPI**와 **SPI**라는 두 개의 지표가 생성되고, 이는 다시 **Forecasting Model**로 들어가 미래를 수정하는 피드백 루프를 형성합니다. 즉, EVM은 단순한 보고서가 아니라 **프로젝트를 제어하는 사이버네틱스(Cybernetics) 시스템**입니다.

#### 4. 실무 코드 및 로직 (Python/Pseudocode Snippet)
```python
# Pseudo-code for EVM Core Engine
def calculate_evm_metrics(bac, actual_cost, planned_value, earned_value):
    # 1. Calculate Performance Indices
    try:
        cpi = earned_value / actual_cost
        spi = earned_value / planned_value
    except ZeroDivisionError:
        return "Error: AC or PV cannot be zero."

    # 2. Forecasting (Typical Scenario assumption)
    # If CPI < 1.0, we assume this trend continues
    eac = bac / cpi
    
    # 3. Calculate Variance (Cost Variance, Schedule Variance)
    cv = earned_value - actual_cost  # Negative is Over Budget
    sv = earned_value - planned_value # Negative is Behind Schedule

    # 4. Decision Logic for Alert
    status = "NORMAL"
    if cpi < 0.9 or spi < 0.9:
        status = "CRITICAL: RECOVERY ACTION NEEDED"
    elif cpi < 1.0 or spi < 1.0:
        status = "WARNING: MONITOR CLOSELY"
    
    return {
        "CPI": round(cpi, 2),
        "SPI": round(spi, 2),
        "EAC": round(eac, 2),
        "Status": status
    }
```

#### 📢 섹션 요약 비유
> "EVM의 계산 로직은 **자동차의 내비게이션**과 같습니다. 내비게이션은 현재 위치(EV)와 목적지(BAC) 그리고 현재 속도(CPI/SPI)를 실시간으로 계산하여, '현재 속도로 가면 약 15분 늦는다(EAC)'라고 예측합니다. 단순히 '앞으로 10km 남았다'는 고정된 정보(PV)를 주는 것이 아니라, 운전자의 주행 습관(실제 성과)을 반영하여 도착 시간을 동적으로 재산정하는 원리입니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. EVM vs Agile Burndown Chart (성과 관리 패러다임 비교)

| 비교 항목 (Criteria) | **EVM (Earned Value Management)** | **Agile Burndown Chart (번다운 차트)** |
|:---|:---|:---|
| **핵심 철학 (Philosophy)** | **가치 중심 (Value-Based)**: '돈을 얼마나 써서 얼마의 가치를 만들었는가?' | **작업 중심 (Effort-Based)**: '남은 일(Remaining Work)이 얼마나 줄어들고 있는가?' |
| **비용 통합 (Cost)** | **O**: PV/AC/EV 모두 금전적 가치로 연결됨. | **X**: 주로 '스토리 포인트'나 '업무 시간' 사용, 실제 비용 연결 약함. |
| **일정 가시화 (Schedule)** | **SPI** 지표를 통해 수치화된 지연/단축 표현. | 시각적인 그래프의 기울기(Slope)로 직관적 판단. |
| **적합 환경 (Context)** | 대규모 **정형 프로젝트 (Waterfall)**, 발주처가 보고를 요구할 때. | 변동이 잦은 **애자일 스크럼 (Scrum)**, 팀 자기 주도적 관리. |
| **단점 (Cons)** | WBS 유지보수가 번거로움, 너무 관료적일 수 있음. | '완료(Definition of Done)'의 정의에 따라 그래프가 왜곡될 수 있음. |

#### 2. 융합 시너지: 기능점수(FP)와의 결합
EVM을 소프트웨어 프로젝트에 적용할 때 가장 큰 난관은 **"일의 양(Progress)"을 어떻게 측정하느냐**이다. 단순히 '코딩 중 50%'라는 식의 측정은 신뢰할 수 없다.
- **해결책**: **FP (Function Point)** 기법을 활용하여 '기능적 완성도'를 금액으로 환산한다.
- **융합 효과**: "이번 스프린트에 20FP(기능점수)를 완료하여 500만 원(EV)의 가치를 창출함"과 같이, 개발자의 주관적 감이 아닌 고객 가치(Value) 기반의 EV 산출이 가능해진다.

#### 3. 다이어그램: Waterfall EVM vs Agile EVM 시각화

```text
[Waterfall EVM - Macro View]          [Agile EVM (Simplified) - Micro View]
^ Cost ($)                            ^ Remaining Effort (Story Points)
|                                      |
|    ● [Sprint 2 End]                  |       _______
|   /                                  |      /
|  /                                   |     /
| /