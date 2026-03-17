+++
title = "752. 프로토타입 버리기 모델 vs 진화적 모델"
date = "2026-03-15"
weight = 752
[extra]
categories = ["Software Engineering"]
tags = ["SDLC", "Prototyping", "Throwaway Prototype", "Evolutionary Prototype", "Requirements", "User Feedback"]
+++

# 752. 프로토타입 버리기 모델 vs 진화적 모델

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자 요구사항의 모호성(Ambiguity)을 해소하기 위해 개발 생명주기(SDLC) 초기에 가시화된 결과물을 제작하여 피드백을 수집하는 **위험 완화(Risk Mitigation) 전략**이다.
> 2. **분화**: 요구사항을 확인한 뒤 폐기하는 **버리기 모델(Throwaway Prototyping)**은 명세서의 정확도를 높이는 데 집중하며, 지속적으로 확장하여 최종 제품이 되는 **진화적 모델(Evolutionary Prototyping)**은 시장 투입 시간(Time-to-Market) 단축에 유리함.
> 3. **가치**: 개발자와 사용자 간의 인지적 격차를 줄여 "만들어 보니 안 된다"는 치명적인 리스크를 개발 초기(초기 비용이 낮을 때)에 발견하고 수정하여 유지보수 비용을 획기적으로 절감함.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학
**프로토타입 (Prototype)**은 '원형(Original Form)'이라는 어원을 가지며, 소프트웨어 공학에서는 **실제 시스템의 일부 혹은 전체를 시뮬레이션하는 시제품**을 의미합니다. 사용자는 자신이 원하는 것을 언어나 문서로 명확히 설명하는 데 한계가 있으므로, "보고 나서야 무엇이 잘못되었는지 안다"는 경향이 강합니다. 이를 극복하기 위해 **구현 가능성(Feasibility)**을 사전에 검증하고, **사용자 인터페이스(UI/UX)**의 적합성을 판단하며, 요구사항의 **불완전성(Incompleteness)**을 보완하는 핵심적인 도구로 활용됩니다. 이는 **SDLC (Software Development Life Cycle, 소프트웨어 개발 생명주기)** 모델 중 폭포수 모델(Waterfall Model)의 '결과물 후반 확인'이라는 단점을 극복하기 위해 등장했습니다.

### 등장 배경 및 진화
1.  **기존 한계**: 문서 기반의 개발 방식론에서는 개발 완료 시점에서야 사용자가 "이게 제가 원하던 게 아닌데요?"라고 하는 경우가 빈번하여 전체 프로젝트가 실패하는 위험이 컸습니다.
2.  **혁신적 패러다임:** "초기에 실패하고 빠르게 배우라(Fail Fast, Learn Early)"는 애자일(Agile) 철학의 시초가 되며, 문서 중심에서 **실행 가능한 코드 중심(Working Code)**으로 패러다임이 이동했습니다.
3.  **현재의 비즈니스 요구**: MVP (Minimum Viable Product, 최소 기능 제품)를 통해 시장의 반응을 보고 비즈니스 모델을 검증하는 스타트업 및 4차 산업혁명 기술 개발 프로젝트에서 필수적인 공정으로 자리 잡았습니다.

### 💡 기술적 비유: 자동차 디자인의 '클레이 모델(Clay Model)'

```text
═══════════════════════════════════════════════════════════════════════════════
                     [ 프로토타이핑 유형화 비유 ]
═══════════════════════════════════════════════════════════════════════════════
 
   [ Type A: 버리기 모델 (Throwaway) ]          [ Type B: 진화적 모델 (Evolutionary) ]
   ───────────────────────────────            ────────────────────────────────────
                                                        ▲
      목적: 디자인(요구사항) 확인                      목적: 실제 주행(서비스) 제공
                                                        │
   1. 자동차 디자이너가 진흙(Clay)으로               1. 시제품 자동차를 만들어서
      전체적인 외관 곡선을 조각함.                     실제로 시운전(Test Run)을 함.
                                                        │
   2. 디자이너와 고객은 "이게 멋진가?"                2. "엔진 힘이 좀 약한데?" 하면
      라인을 보며 수정하며 논의함.                     엔진을 교체하고 바퀴를 추가함.
                                                        │
   3. 확정된 디자인图면을 바탕으로                   3. 이 시제품을 계속 고치고 
      진짜 철로 차량을 제작함.                          덧붙여서 판매용 완성차로 만듦.
                                                        │
   ★ 진흙 모델은 그대로 버려짐.                        ★ 시제품이 곧 완성차가 됨.
   
═══════════════════════════════════════════════════════════════════════════════
```

> **📢 섹션 요약 비유**: 프로토타이핑은 건축에서 **'모델하우스(모형)'**를 짓는 것과 같습니다. 단, '진화적 모델'은 그 모형을 점점 견고한 재료로 교체하며 **실제 살 수 있는 집으로 바꿔나가는 과정**이라는 점에서 차이가 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

프로토타입 모델은 목적에 따라 **TP (Throwaway Prototyping, 버리기 프로토타입)**과 **EP (Evolutionary Prototyping, 진화적 프로토타입)**로 완전히 분기됩니다.

### 1. 구성 요소 및 파라미터 분석 (Deep Dive Table)

| 구성 요소 | 버리기 모델 (Throwaway Prototyping) | 진화적 모델 (Evolutionary Prototyping) |
|:---:|:---|:---|
| **기술적 정의** | 요구사항 수집을 목적으로 하는 일회성 시뮬레이션 | 최종 시스템의 강건한 코어(Kernel)가 되는 개발 단계 |
| **품질 속성** | 신속성(Rapidity) 중심, 내구성 무시 | **확장성(Extensibility)** 및 **유지보수성(Maintainability)** 필수 |
| **개발 도구** | 와이어프레임, PPT, 스크립트 언어, Mock 데이터 | 실제 개발 언어(Java, C#, Python 등), DB 연동 |
| **아키텍처** | 수평적 프로토타입(Horizontal: UI 위주) | 수직적 프로토타입(Vertical: 핵심 로직 구현) |
| **주요 리스크** | 본 개발 시 재작성(Re-work)에 대한 거부감 | **Spaghetti Code(누더기 코드)**화로 인한 기술 부채 발생 |
| **적용 분야** | 대규모 SI, 임베디드 시스템, 핵심 알고리즘 검증 | 스타트업 MVP, SaaS 플랫폼, 게임 개발, AI 모델 튜닝 |
| **최종 산출물** | SRS (Software Requirements Specification, 요구사항 명세서) | **동작하는 소프트웨어 (Executable System)** |

### 2. 프로세스 및 상태 전이 다이어그램

아래는 두 모델의 선택과 수행 과정을 나타낸 **상태 기계(State Machine)** 형태의 공학적 다이어그램입니다. 프로토타입 제작 후 평가 결과에 따라 라이프사이클이 크게 갈립니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ 프로토타이핑 라이프사이클 ]                        │
└─────────────────────────────────────────────────────────────────────────────┘

   [Requirements Analysis]  ◀───────┐
        (요구사항 분석)                │
             │                        │ (Refinement, 재정의)
             ▼                        │
      [Prototyping] ──────────────────┤   User Feedback Loop
   (Rapid Construction, 신속 구축)     │       (사용자 피드백 루프)
             │                        │
             ▼                        │
    [User Evaluation] ────────────────┘
     (시연 및 피드백 수집)
             │
             ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │             CRITICAL DECISION POINT (의사결정 지점)             │
   │  "이 프로토타입을 버리고 다시 짤 것인가(Clean slate),           │
   │   아니면 이 프로토타입을 살려서 발전시킬 것인가(Refactor)?"      │
   └─────────────────────────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
 [ PATH A ]        [ PATH B ]
 (Throwaway)      (Evolutionary)
    │                 │
    ▼                 ▼
 [ DISCARD ]     [ ENGINEERING ]
  (폐기)         (공학적 재설계 및 추가 개발)
    │                 │
    ▼                 ▼
 [ Clean Design ]   [ Refactoring ]
  (새로운 설계)      (리팩토링 및 최적화)
    │                 │
    ▼                 ▼
 [ Implementation ]    │
 (정식 개발 구현)       │
    │                 │
    └────────┬────────┘
             ▼
      [ Final Product ]
      (최종 제품 인도)
```

#### ③ 다이어그램 심층 해설 (200자+)
이 다이어그램은 소프트웨어 위험 관리의 **분기점(Risk Divergence)**을 시각화한 것입니다. 핵심은 **`User Evaluation`** 단계 이후입니다. 버리기 모델(Path A)은 프로토타입 자체의 품질보다는 **프로토타입을 통해 얻은 '지식(Knowledge)'**에 가치를 두며, 코드를 폐기하고 더 나은 아키텍처로 다시 시작(Clean Slate)하는 비용을 감수합니다. 반면, 진화적 모델(Path B)은 프로토타입이 가진 **관성(Inertia)**을 활용해 빠르게 완성품을 만드는 대신, 초기 설계에 없던 기능을 덧붙이며 발생하는 **기술 부채(Technical Debt)**를 관리하기 위해 필연적으로 **`Refactoring`**(코드 재구성) 과정을 거쳐야만 합니다. 아키텍트는 이 지점에서 시간, 비용, 품질의 트레이드오프를 결정해야 합니다.

### 3. 핵심 알고리즘 및 의사결정 로직 (Pseudo-code)

어떤 모델을 선택할지 결정하는 **의사결정 트리(Decision Tree)** 로직입니다.

```python
def select_prototyping_strategy(req_uncertainty, time_pressure, technical_debt_tolerance):
    """
    프로토타입 전략 선정 함수
    Args:
        req_uncertainty (float): 요구사항 불확실성 (0.0 ~ 1.0)
        time_pressure (bool): 시간 긴박성 여부
        technical_debt_tolerance (str): 기술 부채 허용 수준 ('Low', 'High')
    Returns:
        str: 추천 전략
    """
    
    if req_uncertainty > 0.7:
        # 요구사항이 너무 불확실하면, 정밀한 코딩보다는 가시화가 중요함
        if technical_debt_tolerance == 'Low':
            return "THROWAWAY (Quick Mockup only)"
        else:
            return "EVOLUTIONARY (Start with MVP, Pivot expected)"

    elif time_pressure == True and technical_debt_tolerance == 'High':
        # 시장에 빨리 내놔야 하고 코드 품질이 나중 문제가 안 된다면
        return "EVOLUTIONARY (MVP to Product)"
        
    else:
        # 규모가 크고 안정성이 중요한 시스템 (금융, 항공 등)
        return "THROWAWAY (Use Prototype only for Spec Confirmation)"
```

> **📢 섹션 요약 비유**: 마치 **'드레스 피팅(Fitting)'**과 같습니다. '버리기 모델'은 종이로 대충 옷 모양을 오려보고 치수만 재는 견본 단계이고, '진화적 모델'은 실제 원단을 대고 자르다가 "여기는 좀 조여야지" 하면서 실제 옷을 수정해가는 **단계적 봉제** 과정입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술적 상관관계 매트릭스 (SDLC Models)

| 구분 | Waterfall (폭포수) | Prototype (프로토타입) | Spiral (나선형) | Agile (애자일) |
|:---:|:---:|:---:|:---:|:---:|
| **주기적 특성** | 선형 (Linear) | **반복적 (Iterative)** | 순환적 (Cyclic) | **반복적 (Iterative)** |
| **사용자 참여** | 낮음 (Low) | **매우 높음 (Very High)** | 중간 (Medium) | 지속적 (Continuous) |
| **위험 관리** | 후반 발견 | **초기 해결 (Early Resolution)** | 위험 분석 중심 | 매 Sprint 검증 |
| **문서화 중요성** | 매우 높음 | 낮음 (Prototype 대체) | 높음 | 낮음 (Working Code) |
| **요구사항 변경** | 불가능에 가까움 | **유연함 (Flexible)** | 유연함 | 극도로 유연함 |

*   **관계 설명**: 프로토타입 모델은 나선형 모델의 **'위험 분석(Risk Analysis)'** 단계 내에서 사용되는 핵심 기법이며, 애자일(Agile)의 **'스프린트(Sprint)'** 산출물을 만드는 기반이 되기도 합니다. 즉, 프로토타입은 더 큰 개발 방법론 내부에 포함된 **하위 기술(Tactic)**입니다.

### 2. 타 과목 융합 분석: DB/데이터 관점

*   **Database (DBMS)**: 버리기 모델에서는 **정규화(Normalization)** 되지 않은 가짜 데이터(Mock Data)나 CSV 파일을 사용하여 속도를 냅니다. 반면, 진화적 모델에서는 초기에 **ERD (Entity Relationship Diagram)**를 설계하고 실제 DB 스키마가 적용되므로, **Migration(데이터 이주)** 비용이 고려되어야 합니다.
*   **Network**: 진화적 모델을 사용할 경우, API 규격이 계속 변경될 수 있으므로 클라이언트와 서버 간의 **버전 관리(Versioning)** 전략(예: `/v1/user`, `/v2/user`)이 필수적입니다.

### 3. 비용 분석