+++
title = "666. 요구사항 도출 JAD 페르소나"
date = "2026-03-15"
weight = 666
+++

# 666. 요구사항 도출 JAD 페르소나

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 프로젝트 실패의 주요 원인인 '요구사항의 불확실성'을 제거하기 위해, 이해관계자(Stakeholder)의 암묵적 지식과 잠재적 니즈를 체계적으로 표면화하고 합의하는 **요구공학(Requirements Engineering)의 핵심 프로세스**이다.
> 2. **기술적 가치**: 단순 질문 방식을 넘어 **JAD (Joint Application Design)** 워크숍을 통해 의사결정 지연을 해소하고, **페르소나(Persona)** 기반 시나리오 분석을 통해 사용자 중심 설계(UCD, User Centered Design)의 정확도를 획기적으로 높인다.
> 3. **융합 및 확장**: 최근에는 빅데이터 분석을 결합한 **정량적 페르소나(Quantitative Persona)** 도출과, 협업 도구(Collaborative Tools) 및 AI 기반 회의록 작성 기술을 통해 실시간 요구사항 정의 및 추적 가능성을 강화하는 방향으로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

**1. 요구사항 도출(Elicitation)의 딜레마와 정의**
요구사항 도출은 "사용자가 원하는 것(What)"을 "시스템이 해야 할 일(How)"로 변환하는 첫 단계입니다. 그러나 소프트웨어 위기(Software Crisis) 이후 지속적으로 보고되는 현장의 문제는, 사용자는 자신이 무엇을 원하는지 정확히 모르거나(Misunderstanding), 있어 보이게 말하거나(Ambiguity), 말로 표현하지 못하는 무언가(Tacit Knowledge)가 존재한다는 점입니다.
전통적인 인터뷰(Interview)나 설문조사(Questionnaire)는 1:1 단절된 커뮤니케이션으로 인해 정보의 누락이나 왜곡이 발생하기 쉽습니다. 이를 극복하기 위해 **협업(Collaboration)**과 **공감(Empathy)**이라는 인간 중심적 패러다임이 도입되었습니다.

**2. 등장 배경 및 진화**
① **한계**: 개발자와 사용자의언어 장벽으로 인한 개발 리소스 낭비(Re-work Cost) 발생.
② **패러다임 변화**: 1970년대 IBM에서 시작된 **JAD (Joint Application Design)** 기법이 등장하여, 사용자를 개발 초입부터 참여시키는 구조적 워크숍이 정착됨.
③ **심화**: 1990년대 앨런 쿠퍼(Alan Cooper) 등에 의해 제시된 **페르소나(Persona)** 개념이 UX 디자인 분야에서 도입되며, 추상적인 '다수의 사용자'가 아닌 '구체적 한 인물'에 대한 집중을 통해 요구사항의 퀄리티를 높이는 방법론이 정립됨.

**3. 핵심 개념 ASCII 매핑**

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    요구사항 도출의 접근 방식 변화                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [레거시 접근법] Waterfall Model 기반 1:1 인터뷰                             │
│  ────────────────────────────────────────────────────────                  │
│  User 1 → "나는 빨간 버튼을 원해."    → Developer → (개발 중)                │
│  User 2 → "나는 파란 버튼을 원해."    →            → "아, 빨간 줄 알았는데?"  │
│                          ↓                                                 │
│                    충돌 발생 & 재작업 (Rework)                               │
│                                                                             │
│  [모던 접근법] JAD + Persona 기반 협업                                       │
│  ────────────────────────────────────────────────────────                  │
│  (JAD Room)                                                                │
│  ┌───────────────────────────────────────────────────┐                     │
│  │  User 1, User 2, Developer, Facilitator           │                     │
│  │  ────────────────────────────────────────────    │                     │
│  │  "여기 '페르소나 김대리'가 사용할 화면입니다."        │                     │
│  │  "김대리는 급할 때가 많으니 빨간 '긴급' 버튼이       │                     │
│  │   필요하고, 평소엔 파란 '일반' 버튼을 쓰죠."         │                     │
│  │      → 즉각적인 합의(Domain Consensus) 도출          │                     │
│  └───────────────────────────────────────────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**
> "마치 복잡한 맞춤 집을 지을 때, 설계사, 목수, 그리고 거주할 가족이 전부 하나의 테이블에 둘러앉아(JAD), '이 집에서 사는 가상의 주인'을 설정하고 페르소나) 그 사람의 생활 패턴에 맞춰 현관문 위치를 결정하는 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. JAD (Joint Application Design)의 구조적 메커니즘**
JAD는 단순한 회의가 아니라, 철저하게 기획된 워크숍 형식의 의사결정 프로세스입니다. 핵심은 참여자들의 역할 분담과 토의의 구조화입니다.

**구성 요소 상세 표**

| 요소명 (Component) | 역할 (Role) | 내부 동작 및 책임 (Internal Operation) | 프로토콜/기법 (Protocol) |
|:---|:---|:---|:---|
| **의장 (Facilitator)** | 중립적인 조율자 | 토의 주제를 이탈하지 않게 관리하고 갈등을 중재. 기술적 의사결정에 편향되지 않음. | 회의 진행 규칙(Rules of Engagement) |
| **기록자 (Scribe)** | 문서화 담당 | 화이트보드나 툴에 실시간으로 도출된 요구사항을 기록. 기술 용어를 비즈니스 용어로 변환. | UML (Unified Modeling Language), 유스케이스 작성 |
| **사용자 대표 (User Rep)** | 도메인 전문가 | 실제 업무 흐름(Workflow)과 고통 포인트(Pain Point)를 설명. 최종 결정권行使. | 도메인 지식 기반 검증 |
| **분석가 (Analyst)** | 기술 검증자 | 사용자 요구가 기술적으로 가능한지, 비용은 얼마나 드는지 실시간 피드백. | Feasibility Analysis (타당성 분석) |
| **경영진 (Executive)** | 스폰서 (Sponsor) | 예산 승인 및 최종 우선순위 결정. 장애물 제거. | Governance (거버넌스) |

**2. 페르소나 (Persona) 설계 원리 및 데이터 모델**
페르소나는 가짜 사용자(Fake User)가 아니라, 실제 데이터를 바탕으로 재구성된 **'고집쟁이 가상의 인물'**입니다. 단순한 인구통계학적 정보(나이, 성별)를 넘어 심리적 특성(Psychographics)을 포함해야 합니다.

**페르소나 구조도 (ASCII)**

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PERSONA ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Personal]                     [Context]          [Goal & Pain]            │
│  ─────────                     ─────────          ──────────────            │
│  Name: 김철수 (Persona)         Job: 영업 2팀장                               │
│  Age: 42                        Env: 이동이 잦은 외근직                       │
│  Tech: 스마트폰 중급             Freq: 시스템 접속 10회/일                     │
│                                 Device: 갤럭시 S24                            │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  🎯 PRIMARY GOAL (Core Needs)                                │           │
│  │  "이동 중에도 고객 정보를 3초 만에 검색해서 즉시 답변하고 싶다."          │           │
│  │                                                             │           │
│  │  😡 PAIN POINTS (Frustrations)                              │           │
│  │  ① 로그인할 때마다 복잡한 인증 절차가 귀찮음.               │           │
│  │  ② 지도 앱과 CRM 앱을 오가며 번거로움.                      │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                             │
│  ⇒ Derives Requirements:                                                   │
│    - Req #1: 생체 인증 기반 원클릱 로그인 지원                              │
│    - Req #2: CRM 내부 지도 API 연동                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**3. 요구사항 도출 프로세스 (JAD & Persona Fusion)**
요구사항 도출은 정적인 문서 작성이 아니라 동적인 협업의 결과물입니다. 이 과정에서 JAD와 페르소나는 시너지를 발휘합니다.

**Process Flow & Code Snippet**

```python
# [Pseudo-code] Persona-Based Requirement Filtering Logic

class RequirementSession:
    def __init__(self, session_id, facilitator):
        self.id = session_id
        self.raw_requirements = [] # Raw ideas
        self.persona = Persona("Kim-Chul-Soo") # Target Persona
    
    def conduct_jad_workshop(self, stakeholders):
        # Step 1: Brainstorming (No Criticism)
        for stakeholder in stakeholders:
            self.raw_requirements.extend(stakeholder.speak_ideas())
        
        # Step 2: Filtering based on Persona
        validated_reqs = []
        for req in self.raw_requirements:
            # Step 3: Persona Empathy Check
            if self.persona.does_solve_pain_point(req):
                score = self.calculate_value_complexity(req)
                if score > threshold:
                    validated_reqs.append(req)
        
        # Step 4: Consensus & Prioritization
        return self.prioritize(validated_reqs)

    def calculate_value_complexity(self, req):
        # MoSCoW Method (Must, Should, Could, Won't)
        return (req.business_value * self.persona.urgency) / req.dev_cost
```

**📢 섹션 요약 비유**
> "JAD는 모두가 모여 뇌를 하나로 합치는 '합창 연습'과 같고, 페르소나는 그 합창의 주인공이 될 '특정 인물'의 취향에 맞춰 악보를 수정하는 '맞춤 편곡' 과정과 같습니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기법별 비교 분석: 인터뷰 vs 설문 vs JAD vs 관찰**
어떤 기법을 선택할 것인가는 프로젝트의 상황(Context)에 따라 달라집니다. 정량적 지표를 활용한 의사결정 매트릭스가 필요합니다.

**Comparison Matrix**

| 구분 | 인터뷰 (Interview) | JAD (Joint App Design) | 관찰 (Observation) | 설문 (Survey) |
|:---|:---|:---|:---|:---|
| **대상** | 개별 이해관계자 | 그룹(다수) | 사용자 환경 | 다수(대규모) |
| **데이터 깊이** | 깊음 (Qualitative) | 중간~깊음 | 매우 깊음 (암묵지) | 얕음 (Quantitative) |
| **합의 도출** | 어려움 (편향 가능) | **즉각적 합의 가능** | N/A (분석 필요) | 통계적 추정 |
| **비용/시간** | 높음 / 중간 | **높음 / 짧음 (집중)** | 매우 높음 / 김 | 낮음 / 짧음 |
| **주요 리스크** | 인터뷰어의 편향 | 도멘인 전문가 부재 비용 | 헤이써스 효과(Hawthorne) | 응답률 저조/오답 |

**2. 타 영역과의 융합 (Convergence)**
① **UI/UX 디자인 (User Experience)**: 페르소나는 UI 와이어프레임 작성 시 개발자의 '주관적 디자인'을 배제하고, 페르소나의 '시선 흐름(Eye Tracking)'을 예측하게 하여 **UI 사용성(Usability)**을 사전에 검증하게 합니다.
② **애자일 프로세스 (Agile Methodology)**: JAD는 애자일의 **스프린트 계획 회의(Sprint Planning)**이나 **백로그 수련(Refinement)** 세션의 핵심 메커니즘으로 활용됩니다. 실무에서는 PO(Product Owner)가 페르소나를 들먹이며 스토리(Story)의 우선순위를 조정합니다.
③ **AI 분석 (Artificial Intelligence)**: 전통적인 페르소나는 상상에 기반하지만, 최근에는 로그 데이터나 VOD(Voice of Data)를 클러스터링(Clustering)하여 **데이터 기반 페르소나(Data-driven Persona)**를 도출하는 기술과 융합되고 있습니다.

**📢 섹션 요약 비유**
> "인터뷰가 '낚시대를 던져 하나를 낚는 것'이라면, JAD는 '그물을 던져 한꺼번에 여러 마리를 잡되, 살아있는 놈만 골라내는 선별 과정'이며, 관찰법은 '물속에 직접 뛰어들어 물고기 습성을 연구하는 잠수'와 같습니다."

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오: 핀테크 앱 보안 vs 편의성 갈등 해결**
- **문제 상황**: 금융 앱 개발 시, 보안팀은 "복잡한 2차 비밀번호(2FA)"를, 마케팅팀은 "소셜 로그인(간편 로그인)"을 고집함. 의견 충돌로 개발이 멈춤(Blocker 발생).
- **전략적 접근 (JAD + Persona 활용)**:
    1. **페르소나 부활**: '20대 대학생 김민지(페르소나 A)'와 '50대 자영업자 이영호(페르소나 B)'를 테이블 위에 올림.
    2. **JAD 세션 진행**:
        - "민지님은 복잡한 입력이 싫어서 이탈(Unclogging)할 가능성이 높습니다."
        - "영호님은 보안 해킹 위험에 매우 민감합니다."
    3. **솔루션 도출**: 두 페르소나의 니즈를