+++
title = "779. ISO/IEC/IEEE 29119 소프트웨어 테스팅 국제 표준"
date = "2026-03-15"
weight = 779
[extra]
categories = ["Software Engineering"]
tags = ["Testing", "Quality", "ISO 29119", "Standards", "Test Process", "Test Documentation", "V-Model"]
+++

# 779. ISO/IEC/IEEE 29119 소프트웨어 테스팅 국제 표준

## 핵심 인사이트 (3줄 요약)
> 1. **본질 (Essence)**: 파편화된 기존 테스트 표준들을 통합하여, **소프트웨어 테스팅의 용어, 프로세스, 문서화, 기법**을 정의한 세계 최초의 통합 국제 표준으로, '리스크 기반 테스팅(RBT)'을 핵심 철학으로 삼음.
> 2. **구조 (Structure)**: **ISO (International Organization for Standardization)**, **IEC (International Electrotechnical Commission)**, **IEEE (Institute of Electrical and Electronics Engineers)**가 공동으로 제정한 5개 파트(Part 1~5)로 구성되어 있어, 전사적 차원의 정책 수립부터 프로젝트 단위의 동적 테스트 수행 및 자동화 키워드 주도 테스트까지 전 생애주기를 아우름.
> 3. **가치 (Value)**: 글로벌 아웃소싱 및 다국적 개발 환경에서 **테스트 산출물의 상호운용성(Interoperability)**을 보장하고, **TMMi (Test Maturity Model integration)**와 같은 성숙도 모델 평가의 객관적 근거가 되어 소프트웨어 품질 신뢰성을 정량적으로 향상시킴.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**ISO/IEC/IEEE 29119**는 소프트웨어 및 시스템 수명 주기 전반에 걸쳐 테스팅을 계획, 통제, 수행, 감시하고, 테스트 산출물을 문서화하기 위한 일련의 국제 표준입니다. 단순한 테스트 '기법'을 넘어, 조직의 테스트 문화를 체계화하고 프로세스를 정의하는 거버넌스(Governance) 프레임워크입니다.

### 2. 등장 배경: 표준의 통합과 진화
과거 소프트웨어 산업은 **IEEE 829** (Test Documentation), **IEEE 1008** (Unit Testing), **BS 7925-1** (Vocabulary) 등 국가별 또는 분야별로 파편화된 표준이 혼재하여 혼선을 빚었습니다.
1.  **기존 한계**: 조직별로 상이한 용어 사용으로 인한 커뮤니케이션 오류와 문서 호환성 부족.
2.  **혁신적 패러다임**: ISO와 IEEE가 합심하여 2013년부터 Part 1, 2, 3을 순차적으로 발표하며 '단일의 통합된 테스트 언어'를 구축.
3.  **현재의 비즈니스 요구**: Agile/DevOps 환경으로의 전환에 따라 경량화된 프로세스 적용과 리스크 기반 의사결정의 필요성 대응.

### 3. ASCII 다이어그램: 표준의 진화 맥락
아래 다이어그램은 ISO 29119가 기존 산재 표준들을 어떻게 통합하고 확장했는지를 보여줍니다.

```text
+-------------------------+       +-----------------------+       +-------------------------+
|  Legacy Standards (1990s)|       |  Early Integration    |       |  ISO 29119 Series (2013~)|
|  [Fragmented]           |  --->  |  (2000s)             |  --->  |  [Unified & Global]     |
+-------------------------+       +-----------------------+       +-------------------------+
| • IEEE 829 (Docs)       |       | • IEEE 829 Update     |       | • Part 1: Concepts      |
| • IEEE 1008 (Unit)      |       | • BS 7925 (Vocab/Tech)|       | • Part 2: Processes     |
| • BS 7925-1 (Vocab)     |       | • Context Specific    |       | • Part 3: Documentation  |
+-------------------------+       +-----------------------+       | • Part 4: Techniques     |
                                                                | • Part 5: Keyword Driven|
                                                                +-------------------------+
                                                                     │
                                                                     ▼
                                           [Goal] : Universal Interoperability & Quality Assurance
```

**다이어그램 해설**:
1990년대 미국(IEEE)과 유럽(BS) 중심으로 개별적으로 존재하던 표준들이 혼재하면서 발생했던 '표준 전쟁' 문제를 해결하기 위해, 2000년대 후반부터 글로벌 표준 기구들이 협력하기 시작했습니다. 그 결과물인 **ISO 29119**는 과거의 표준들을 단순히 폐지한 것이 아니라, 검증된 내용을 흡수(Absorb)하고 현대적인 개발 환경(Agile, DevOps)에 맞춰 **Tailoring(재정의/절삭)**이 가능한 형태로 발전시켰습니다. 특히 Part 5에 해당하는 키워드 주도 테스팅은 최근의 자동화 트렌드를 반영하여 추가된 확장 영역입니다.

### 📢 섹션 요약 비유
> 마치 세계 각국이 서로 다른 철도 궤간(레일 간격)을 사용하던 시절에서, 전 세계를 횡단할 수 있는 '표준 궤간(Standard Gauge)'으로 통합한 것과 같습니다. 이를 열차가 국경을 넘나들 때마다 바퀴를 교체할 필요 없이, 아시아에서 유럽까지 한 번에 달릴 수 있게 된 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 (표) : 5개 파트 상세 분석
ISO 29119는 수직적(개념→운영) 및 수평적(문서화→기법) 구조를 가진 5개의 파트로 구성됩니다.

| Part | 명칭 (Full Name) | 핵심 역할 및 내부 동작 | 주요 산출물/Protocol | 실무적 비유 |
|:---:|:---|:---|:---|:---|
| **Part 1** | **Concepts & Definitions** | **용어 사전**: 테스트 용어, 목적, RBT(Risk-Based Testing) 철학 정의. | Glossary, Test Policy | 건축 법령의 총칙 및 용어 정의 |
| **Part 2** | **Test Processes** | **운영 매뉴얼**: 조직/관리/동적 테스트의 3계층 프로세스 정의. | Test Plan, SRS Review | 시공 프로세스 매뉴얼 (인력→자재→시공) |
| **Part 3** | **Test Documentation** | **양식 템플릿**: 30종 이상의 문서 템플릿 (Test Design, Log, Report 등). | Test Specification | 공사 일지, 검수 합격서 양식 |
| **Part 4** | **Test Techniques** | **기술 백과**: 블랙박스(동등분할), 화이트박스(제어흐름) 기법 정의. | Test Cases, Coverage | 정밀 시공 기법 가이드 (배합비, 용접법) |
| **Part 5** | **Keyword-Driven Testing** | **자동화 프레임워크**: 테스트 자동화를 위한 키워드 구조 정의. | Automation Script | 공장 자동화 로봇 제어 명령어 세트 |

### 2. 리스크 기반 테스팅 (RBT) 아키텍처
ISO 29119의 모든 프로세스는 '리스크(Risk)'를 중심으로 돌아갑니다. 리스크는 '발생 확률(Probability)'과 '영향도(Impact)'의 곱으로 정의되며, 이 점수가 높은 항목부터 테스트 우선순위를 부여합니다.

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                    ISO 29119 : Risk-Based Testing Workflow                    │
└───────────────────────────────────────────────────────────────────────────────┘

                 [Product Risks] (e.g., "Server Crash", "Data Loss")
                            │
                            ▼
          +-----------------------------------------------+
          │           Risk Assessment Process             │
          │    (Identification ◀─▶ Analysis ◀─▶ Evaluation)│
          +-----------------------------------------------+
                            │
                            ▼
              ┌─────────────────────────────────────┐
              │   ① High Risk Areas (Critical Path) │  ──▶ Priority 1 (More Testing)
              │   ② Medium Risk Areas               │  ──▶ Priority 2 (Standard)
              │   ③ Low Risk Areas                  │  ──▶ Priority 3 (Less/Auto)
              └─────────────────────────────────────┘
                            │
                            ▼
          +---------------------------------------------------------------+
          │                    Test Design & Execution                   │
          |  (Apply Part 4 Techniques: Boundary Value, State Transition..)|
          +---------------------------------------------------------------+
                            │
                            ▼
          +---------------------------------------------------------------+
          |           Test Reporting (Part 3) & Risk Reduction Evidence   |
          |   "Did we test enough to mitigate the risk to an acceptable  │
          |              level?"                                          |
          +---------------------------------------------------------------+
```

**다이어그램 해설**:
이 아키텍처는 **"우리가 무한한 시간과 자원을 가지고 있지 않다면, 가장 위험한 곳부터 집중해야 한다"**는 실용주의 철학을 보여줍니다.
1.  **Risk Assessment**: 먼저 프로젝트 초기에 요구사항 분석과 함께 '위험 목록'을 작성합니다.
2.  **Prioritization**: 이 리스크 점수에 따라 테스트 노력(Effort)을 배분합니다.
3.  **Mitigation**: 테스트 결과 '잔여 리스크(Residual Risk)'가 비즈니스에서 허용 가능한 수준으로 낮아졌는지 판단하여 종료(Exit Criteria) 결정을 내립니다. 이 과정은 단순히 버그를 찾는 것을 넘어, **프로젝트 실패 가능성을 관리하는 활동**입니다.

### 3. 심층 동작 원리: 테스트 프로세스 (Part 2 상세)
Part 2는 테스트를 3개의 계층(Layer)으로 정의합니다.

1.  **Organizational Test Process**: 경영진이 수행하는 **전사적 차원의 정책(Policy)** 수립 단계입니다. 테스트 조직의 구조, 역할, 독립성을 보장합니다.
2.  **Test Management Process**: 프로젝트 관리자(PM)가 수행하는 **프로젝트 단위의 제어** 단계입니다.
    *   ** Planning (계획)**: 범위, 일정, 자원, 리스크 분석.
    *   ** Control & Monitoring (통제/감시)**: 진척도 추적, 메트릭(Metric) 측정, 재계획.
    *   ** Completion (완료)**: 테스트 종료 보고서 발간 및 인도.
3.  **Dynamic Test Process**: 테스터가 수행하는 **실제 테스팅 실행** 단계입니다.
    *   **Test Design & Implementation**: 테스트 케이스 작성 및 데이터 준비.
    *   **Test Environment Setup**: 테스트 베드 구성.
    *   **Test Execution**: 스크립트 실행 및 로그 기록.
    *   **Test Incident Reporting**: 결함(Defect) 보고 및 추적.

### 4. 핵심 알고리즘: 리스크 우선순위 계산 (Pseudo Code)
ISO 29119에서 권장하는 리스크 분석의 간단한 알고리즘입니다.

```python
# Risk-Based Testing Priority Algorithm
def calculate_test_priority(requirements):
    test_plan = []
    
    for req in requirements:
        # 1. Identify Risks for this requirement
        risk_items = identify_risks(req)
        
        for risk in risk_items:
            # 2. Calculate Risk Score
            # P: Probability (1~5), I: Impact (1~5)
            risk_score = risk.probability * risk.impact 
            
            # 3. Determine Test Level based on Score
            if risk_score >= 15: # Critical
                level = "Exhaustive"
                technique = ["Exploratory", "Boundary Value"]
            elif risk_score >= 8:  # High
                level = "Deep"
                technique = ["Equivalence Partitioning"]
            else:                 # Low
                level = "Basic"
                technique = ["Smoke Test"]
                
            test_plan.append({
                "req_id": req.id,
                "risk_score": risk_score,
                "priority": level,
                "techniques": technique
            })
            
    # Sort by Risk Score (Descending)
    return sorted(test_plan, key=lambda x: x['risk_score'], reverse=True)
```

### 📢 섹션 요약 비유
> 마치 응급실(Triage)에 도착한 환자를 분류하는 것과 같습니다. 가슴이 뜯어진 중증 환자(고위험 기능)는 즉시 수술실(집중 테스트)로 보내고, 감기에 걸린 가벼운 환자(저위험 기능)는 대기 시간을 두고 약을 지어주는(간단 테스트) 방식으로, 한정된 의료 인력(테스트 자원)으로 생존율(품질)을 극대화하는 시스템입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: ISO 29119 vs IEEE 829 vs Agile Testing
각 표준과 방법론이 포커스하는 축이 다릅니다.

| 구분 | **IEEE 829** (Legacy) | **ISO 29119** (Modern Standard) | **Agile Testing** (Methodology) |
|:---|:---|:---|:---|
| **초점** | 문서화의 **구조**와 **형식** | 프로세스의 **체계성**과 **통합** | **속도**와 **협업**, **유연성** |
| **프로세스** | 계획 → 설계 → 실행 → 보고 (선형적) | **3계층 프로세스** (조직/관리/수행) | **Iterative** (스프린트 내반복) |
| **문서화** | 문서 중심 (Heavyweight) | **Risk-based Tailoring** (가능) | **Working Software** 중심 (문서 최소화) |
| **적합성** | 방대한 시스템, 안전 중시 시스템 | **모든 환경** (Waterfall & Agile) | 변화가 잦은 스타트업, 웹 서비스 |

### 2. 과목 융합 관점: TMMi (성숙도)와의 연계
ISO 29119는 **TMMi (Test Maturity Model integration)**와 밀접한 관련이 있습니다.
- **TMMi (Test Maturity Model integration)**: "우 회사의 테스트 역량이 몇 레벨인가?"를 평가하는 **진단 도구(Diagnostic Tool)**.
- **ISO 29119**: "그 레벨에 도달하기 위해 무엇을 해야 하는가?"를 정의한 **실행 가이드(Execution Guide)**.
- **시너지**: TMMi 레벨 2(관리)나 레벨 3(정의)을 달성하기 위해, ISO 29119 Part 2(프로세스)의 활동을 증거(Audit Evidence)로 활용할 수 있습니다.

```text
┌────────────────────────────────────────────────────────