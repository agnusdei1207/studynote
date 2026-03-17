+++
title = "672. 소프트웨어 비용 산정 COCOMO"
date = "2026-03-15"
weight = 672
[extra]
categories = ["Software Engineering"]
tags = ["Cost Estimation", "COCOMO", "Boehm", "Software Metrics", "Project Management"]
+++

# 672. 소프트웨어 비용 산정 COCOMO

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 배리 보헴(Barry Boehm)이 1981년 제안한 **COCOMO (Constructive Cost Model)**는 소프트웨어 규모(KDSI)와 개발 공수(Person-Month) 간의 비선형 관계를 수학적 모델로 정형화한 **하이브리드 비용 산정 기법**이다.
> 2. **가치**: 단순한 인원 투입 방식이 아닌, 프로젝트의 복잡도(Complexity)와 제약 조건(Constraints)을 **비용 동인(Cost Drivers)**으로 정량화하여, 개발 초기 위험을 완화하고 **RTO (Recovery Time Objective)** 및 예산 오차율을 최소화한다.
> 3. **융합**: **FP (Function Point)** 방식과 보완적이며, 현대의 **敏捷(Agile)** 개발 환경에서는 **COCOMO II** 모델로 진화하여 **ROI (Return on Investment)** 분석 및 **KPI (Key Performance Indicator)** 관리의 핵심 지표로 활용된다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학: "공짜 점심은 없다" (No Free Lunch)
소프트웨어 공학에서 가장 어려운 문제 중 하나는 "얼마나(cost) 언제(time)"라는 질문에 과학적으로 답하는 것이다. 1970년대 후반까지 소프트웨어 비용 산정은 감(Gut feeling)에 의존하거나 단순히 코드 라인 수(Line of Code)에 비례하는 선형적으로 계산되었다. 그러나 시스템이 복잡해질수록 의사소통 오버헤드(Brooks's Law)가 기하급수적으로 증가함에 따라, 기존의 선형 모델은 실제와 맞지 않는다는 한계가 드러났다.
이를 해결하기 위해 배리 보헴은 수천 개의 프로젝트 데이터를 회귀 분석하여, 소프트웨어 규모가 증가함에 따라 노력이 어떤 **지수 함수(Exponential Function)** 형태로 증가하는지 정의한 것이 바로 COCOMO이다. 이는 단순한 공식을 넘어, 소프트웨어 위험 관리의 시초가 되는 이론적 토대이다.

### 2. 배경 및 역사
- **1970년대**: 미 국방부 등 대형 프로젝트에서 일정 준수 실패가 빈발. 객관적인 견적 도구의 필요성 대두.
- **1981년**: **COCOMO 81** 발표. Basic, Intermediate, Detailed 모델 제시.
- **1990년대**: RAD(Rapid Application Development), 재사용(Reuse) 등장으로 기존 모델의 한계 발생.
- **2000년**: **COCOMO II** 발표. 객체지향, 프로토타이핑, 비즈니스 프로세스 재설계(BPR) 환경 반영.

### 3. 💡 비유: 트랜피게이트 교통 흐름
소프트웨어 비용 산정은 마치 고속도로 톨게이트의 차량 처리량을 예측하는 것과 같다.
- 단순한 시스템(Organic)은 일반 차량이 자율적으로 통과하는 것과 같아 예측이 쉽지만,
- 복잡한 임베디드 시스템(Embedded)은 톨게이트 안에서 화물차의 하역, 검사, 연료 주입이 동시에 일어나는 복합 터미널과 같다. 차량 한 대(LOC)가 증가할 때마다 예상치 못한 정체 병목(Complexity)이 발생하여 처리 시간(Man-Month)이 2배, 3배로 늘어나는 현상을 모델링한 것이다.

### 4. ASCII: 비선형 비용 증가 시각화 (The Mythical Man-Month)

```text
      (Effort: MM)
        ^
        |                     / [Embedded Mode] (High Complexity)
        |                    /
        |                   /
        |                  /  <-- 노이만-노만 효과 (Communication Overhead)
        |                 /
        |                /
        |               / 
        |              /
        |             / [Semi-Detached Mode]
        |            /
        |           /
        |          /
        |         /
        |        /
        |       /
        |      /
        |     / [Organic Mode] (Linear-ish)
        |    /
        |   /
        |  /
        | /
        +------------------------------------------------> (Size: KDSI)
           50      100      200      300
```
*그림 설명: 시스템 복잡도가 높아질수록(E).)

### 5. 등장 배경 요약
① 기존 선형 모델의 예측 실패 (일정 지연, 예산 초과) → ② **回归分析(Regression Analysis)** 기반의 경험적 공식 도입 → ③ 프로젝트 의사결정 지원을 위한 객관적 근거 자료 생성.

> **📢 섹션 요약 비유**: 마치 고속도로 건설 시, 단순한 지형에는 4차선 도로를 만들듯 일정하게 비용이 드지만, 산악 지형(Embedded)에 터널과 교량을 복합적으로 건설해야 할 때는 길이가 조금만 늘어나도 공사 비용과 기간이 폭발적으로 증가하는 '난이도 계수'를 적용하는 견적 시스템과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석
COCOMO는 크게 **규모(Scale)**, **모드(Mode)**, **비용 동인(Cost Drivers)**으로 구성된다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 프로토콜/지표 | 비유 |
|:---:|:---|:---|:---|:---|
| **KDSI (Kilo Delivered Source Instructions)** | 입력 변수 | 코드 라인 수(주석/공백 제외)를 1,000단위로 측정 | `Scale Factor` | 집의 연면적 (㎡) |
| **Development Mode** | 난이도 구분 | 프로젝트 특성에 따라 지수 $b$를 결정 (1.05~1.20) | `Complexity Index` | 지역 구분 (평지 vs 산지) |
| **Cost Drivers** | 보정 계수 | 인력, 프로젝트, 환경 등 15개(또는 17개) 요인의 가중치 곱 | `Multiplier (0.7~1.9)` | 자재 가격, 인건비 변동 |
| **PM (Person-Month)** | 출력 결과 (공수) | 1인 1달 업무량을 기준으로 총 투입 시간 산출 | `Effort` | 총 공사 기간 |
| **TDEV (Time to Develop)** | 출력 결과 (기간) | 노동 레이버定理(Rayleigh Curve)을 기반으로 최적 일정 산출 | `Schedule` | 준공 예정일 |

### 2. ASCII: COCOMO 모델의 계층 구조 (Hierarchy)

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                         COCOMO MODEL HIERARCHY                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. Basic COCOMO (기본 모델)                                                │
│     └── Input: KDSI (Size) ───> Output: PM (Effort)                        │
│         • 가장 단순함. 초기 필터링 용도.                                     │
│                                                                            │
│  2. Intermediate COCOMO (중간 모델)                                         │
│     └── Input: KDSI + 15 Cost Drivers ───> Output: PM (Adjusted Effort)    │
│         • PM(Effort) = a * (KDSI)^b * ∏(Cost Drivers)                       │
│         • 각 Cost Driver는 매우 낮음(Very Low)부터 매우 높음(Extra High)까지│
│           계수를 가짐 (예: RELY=1.40).                                      │
│                                                                            │
│  3. Detailed COCOMO (상세 모델)                                             │
│     └── Input: KDSI + Phase-specific Drivers ───> Output: PM (Phase Effort)│
│         • 프로젝트 단계(요구/설계/코딩/테스트)별로 다른 Cost Driver 적용.   │
│         • 가장 정밀함. 계획 수립 시 활용.                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```
*해설: 기본 모델은 단순히 크기만 보지만, 상세 모델로 갈수록 프로젝트의 맥락(Context)을 반영하여 정밀도(Precision)를 높인다.*

### 3. 핵심 수식 및 알고리즘
COCOMO의 핵심은 노력(Effort)이 규모(Size)의 $b$승에 비례한다는 점이다.

#### A. 기본 공식 (Basic Model Equation)
$$ E = a \times (KDSI)^b $$
$$ T_{dev} = c \times (E)^d $$

여기서:
- **$E$**: Effort (Person-Month, PM)
- **$T_{dev}$**: Development Time (Months)
- **$a, b, c, d$**: 계수 (모드별 상이)

#### B. 3가지 모드별 상수 테이블 (Coefficient Table)

| 모드 (Mode) | $a$ (Effort Coeff) | $b$ (Scale Exponent) | $c$ (Time Coeff) | $d$ (Time Exponent) | 시스템 특징 |
|:---:|:---:|:---:|:---:|:---:|:---|
| **Organic** | 2.4 | 1.05 | 2.5 | 0.38 | 단순 업무, 소규모 팀 |
| **Semi-Detached** | 3.0 | 1.12 | 2.5 | 0.35 | 트랜잭션, 중간 복잡도 |
| **Embedded** | 3.6 | 1.20 | 2.5 | 0.32 | 실시간, 강한 제약 조건 |

#### C. 코드로 보는 동작 원리 (Pythonic Pseudocode)
```python
def calculate_cocomo_basic(kdsi, mode='Organic'):
    """
    Calculate Person-Month (PM) based on Basic COCOMO 81.
    """
    constants = {
        'Organic': {'a': 2.4, 'b': 1.05},
        'Semi-Detached': {'a': 3.0, 'b': 1.12},
        'Embedded': {'a': 3.6, 'b': 1.20}
    }
    
    if mode not in constants:
        raise ValueError("Invalid Mode")
        
    params = constants[mode]
    
    # 핵심 공식: 규모(KDSI)가 증가하면 b의 지수승만큼 비용이 증가함
    effort_pm = params['a'] * (kdsi ** params['b'])
    
    # 일정 산출 (Rayleigh-Norden 曲线 근사)
    time_months = 2.5 * (effort_pm ** 0.38)
    
    return {
        "Effort (PM)": round(effort_pm, 2),
        "Duration (Month)": round(time_months, 2),
        "FTE (Full-time Equivalent)": round(effort_pm / time_months, 2)
    }

# Example: 100 KDSI (10만 라인) 규모의 임베디드 시스템
print(calculate_cocomo_basic(100, 'Embedded'))
# Result: Effort는 약 570 PM, Duration은 약 24개월 소요 예상
```

### 4. 15가지 비용 동인 (Cost Drivers)
상세 모델에서는 $\prod_{i=1}^{15} EM_i$ (Effort Multiplier)를 위 공식에 곱해준다. 주요 동인은 다음과 같다:
1. **RELY (Required Software Reliability)**: 신뢰성 요구도 (생명/재산 위험 시 1.40 이상)
2. **DATA (Data Base Size)**: 데이터베이스 크기 (테스트 데이터 비율)
3. **CPLX (Product Complexity)**: 알고리즘 복잡도 (수치 통제 vs 단순 로직)
4. **TIME (Execution Time Constraint)**: 실행 시간 제약 (CPU 사용률 %)
5. **STOR (Main Storage Constraint)**: 메모리 제약 (RAM 사용률 %)
6. **VIRT (Virtual Machine Volatility)**: 가상 머신 변경 빈도 (OS 변화)
7. **TURN (Computer Turnaround Time)**: 컴퓨터 응답 시간
8. **PCAP (Programmer Capability)**: 프로그래머 능력 (매우 높음 0.7 ~ 낮음 2.0)
9. **AEXP (Application Experience)**: 해당 분야 경험
10. **VEXP (Virtual Machine Experience)**: 플랫폼 경험 (OS, DB 등)
11. **LEXP (Language Experience)**: 언어 경험 (Java, C 등)
12. **MODP (Modern Programming Practices)**: 최신 기법 사용 (구조화 설계 등)
13. **TOOL (Software Tools)**: 도구 지원 (IDE, CI/CD 도구 수준)
14. **SCED (Required Development Schedule)**: 일정 압박 (촉박하면 비용 증가)

> **📢 섹션 요약 비유**: 마치 복잡한 레고 조립 키트의 설명서와 같습니다. 단순히 조각 수(KDSI)로만 시간을 예측하는 것이 아니라, 조립하려는 모형의 종류(자동차 vs 우주선, Mode)와 조립자의 숙련도(Programmer Capability), 그리고 사용하는 공구(Software Tools)의 수준을 모두 고려하여 조립 시간을 보정(Calibration)하는 정교한 매뉴얼 시스템입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 소프트웨어 산정 기법 비교 (LOC vs FP vs COCOMO)

| 구분 | LOC (Line of Code) 기반 | FP (Function Point) 기반 | COCOMO |
|:---:|:---|:---|:---|
| **측정 단위** | 물리적 라인 수 | 사용자 기능(Input/Output/Inquiry) | 로그 방정식 (Logarithmic) |
| **언어 의존성** | 높음 (Java 100줄 $\neq$ C 100줄) | 없음 (언어 무관) | 중간 (입력이 LOC인 경우 높음) |
| **산정 시점** | 개발 후반 (코딩 완료 시) | **개발 초기 (요구사항 분석 시)** | 전 단계 (COCOMO II) |
| **정확도** | 구현물에 대한 정확도 높음 | 개념적 크기에 대한 정확도 높음 | 모델별 상이 (상세 모델 시 높음) |
| **주요 용도** | 생산성 측정 (Productivity) | 견적, 품질 측정 | **일정 계획, 의사결정 지원** |

### 2. ASCII: 비용 산정 기법의 포지셔닝 (Market Positioning)

```text
      [Phases of Softw