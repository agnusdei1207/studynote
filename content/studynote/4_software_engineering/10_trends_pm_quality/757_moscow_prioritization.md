+++
title = "757. MoSCoW 요구사항 우선순위 판별"
date = "2026-03-15"
weight = 757
[extra]
categories = ["Software Engineering"]
tags = ["Requirements", "Prioritization", "MoSCoW", "Agile", "Business Analysis", "Scope Management"]
+++

# 757. MoSCoW 요구사항 우선순위 판별

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 한정된 자원(시간, 예산, 인력) 내에서 시스템 성공의 핵심 조건을 보장하기 위해, 요구사항을 **Must have**, **Should have**, **Could have**, **Won't have**의 4가지 계층으로 분류하는 의사결정 프레임워크(Framework)이다.
> 2. **가치**: '모든 것을 다 하는 것'은 실패라는 애자일(Agile) 철학을 바탕으로, **동적 범위 관리(Dynamic Scope Management)**를 통해 납기 준수율을 90% 이상 끌어올리고 비즈니스 임팩트(Business Impact)를 극대화한다.
> 3. **융합**: **RMM (Requirements Management Tool)**, **백로그 관리(Backlog Management)**, **타임박싱(Timeboxing)** 기술과 결합하여, 프로젝트의 삼각 제약(범위, 시간, 비용)에서 가장 유연한 '범위'를 통제하는 핵심 레버리지로 작용한다.
## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**MoSCoW (Must, Should, Could, Won't)** 방법론은 영국의 소프트웨어 컨설턴트 Dai Clegg가 제안한 우선순위 부정(Prioritization) 기법이다.
이는 단순한 순위 매김이 아니라, **"이번 스프린트(Sprint)나 릴리스(Release)에서 무엇을 포기할 것인가(Zero-Sum Game)"**를 명확히 하는 협상 도구이다.
고객은 모든 요구사항이 '중요'이라고 주장하는 경향이 있으나, 시스템 아키텍처는 **MVP (Minimum Viable Product, 최소 기능 제품)**를 정의하여 '존재 자체의 의미'를 잃지 않는 선에서 자원을 집중해야 한다.

### 2. 등장 배경: 폭포수 모델의 한계와 애자일의 등장
① **전통적 한계**: 초기에 모든 요구사항을 고정하면(Fixed Scope), 개발 후반부에 갈수록 변경 비용이 기하급수적으로 증가하여 프로젝트가 실패하거나 납품이 지연됨.
② **패러다임 전환**: "불확실한 요구사항은 불확실한 상태로 두고, 가장 확실한 핵심 가치부터 개발하자"는 **애자일(Agile Manifesto)** 정신이 대두됨.
③ **비즈니스 요구**: **TTM (Time-to-Market, 시장 출시 시간)** 단축이 생존이 된 현재 환경에서, '완벽한 제품'보다 '적시에 출시된 제품'이 승자가 되는 상황이 반복됨.

### 3. 💡 비유: 응급실 트리아주 (Triage)
중환자실에서 의사가 환자를 분류하는 과정과 같다.
*   **Must have**: 심장이 멈춘 환자 (당장 처리 안 하면 사망/시스템 실패)
*   **Should have**: 골절된 환자 (매우 아프지만 당장 죽지는 않음/핵심 기능은 작동)
*   **Could have**: 감기에 걸린 환자 (치료하면 좋지만, 병상이 모자라면 대기 가능/개선 사항)
*   **Won't have**: 정기 검진을 온 사람 (다음 날짜로 예약 변경/이번 버전 제외)

### 📢 섹션 요약 비유
> "마치 배가 난파되었을 때, 구명보트의 자리가 한정되어 있어서 '누구를 태우고 누구를 바다에 띄워둘지'를 치열하게 결정해야 하는 상황과 같습니다. 모두를 구하려다가는 배가 가라앉기 때문입니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 심층 분석

| 약어 (Abbreviation) | 전체 명칭 (Full Name) | 정의 (Definition) | 내부 동작 메커니즘 (Mechanism) | 기술적 판단 기준 |
|:---:|:---|:---|:---|:---|
| **M** | **Must have** | 필수 요구사항 | 시스템의 핵심 기능. 이것이 없으면 시스템 자체가 **Deploy 불가**하거나 비즈니스 목적이 **'NULL'**이 되는 항목. | **Failure Criteria**: 결함 발생 시 Critical 타입의 버그로 분류되며, 핫픽스(Hotfix) 대상 1순위. |
| **S** | **Should have** | 중요 요구사항 | 시스템의 완성도를 높이는 항목. 없으면 불편하지만 **Workaround(우회)**가 가능하거나 수동 처리로 대체 가능. | **High Priority**: 다음 스프린트로의 이월(Defer)이 가능하지만, 고객 만족도에 큰 영향을 미침. |
| **C** | **Could have** | 선택 요구사항 | ROI (Return on Investment)가 낮거나, 기술적 구현 난이도 대비 파급 효과가 적은 항목. 스프린트의 **Buffer** 역할. | **Nice-to-have**: 스프린트 중간에 Velocity가 높을 때만 수행. |
| **W** | **Won't have** | 미제외/현재 미수행 요구사항 | 단순히 '하지 않는 것'이 아니라 **'이번 버전에는 하지 않기로 합의'**한 항목. 추후 Backlog의 맨 뒤로 보내짐. | **Out of Scope**: 요구사항 명세서(SRS)에 명시하여 '실행하지 않음'을 문서화하여 예방 조치. |

### 2. 우선순위 결정 메커니즘 및 데이터 흐름

MoSCoW 분류는 단순한 태깅이 아니라, 이해관계자(Stakeholders) 간의 합의 프로세스다.

```text
+------------------------------------------------------------------+
|                    [ Stakeholder Workshop ]                      |
|           (Product Owner, Tech Lead, Client, Users)              |
+---------------------------+--------------------------------------+
                            │
                            ▼
      +---------------------------------------------------------------+
      |  1. INPUT: Raw Requirements List (All Wants)                  |
      |  - "로그인이 필요해", "다크 모드도 필요해", "AI 추천도..."      |
      +---------------------------------------------------------------+
                            │
                            ▼
      +---------------------------------------------------------------+
      |  2. FILTER: Business Value vs. Technical Cost Matrix          |
      |     (Value is High / Cost is Low) --> MUST (Best ROI)         |
      |     (Value is High / Cost is High) --> SHOULD (Strategic)     |
      |     (Value is Low  / Cost is Low)  --> COULD (Filler)         |
      |     (Value is Low  / Cost is High) --> WON'T  (Waste)         |
      +---------------------------------------------------------------+
                            │
                            ▼
      +---------------------------------------------------------------+
      |  3. OUTPUT: Prioritized Backlog                               |
      |      ┌─────────────────────────────────────┐                  |
      │      │ Sprint N+1 Scope (Must Only)        │                  |
      │      │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │                  |
      │      │ │ M-1 │ │ M-2 │ │ M-3 │ │ M-4 │... │ <── Commitment   |
      │      │ └─────┘ └─────┘ └─────┘ └─────┘    │                  |
      │      └─────────────────────────────────────┘                  |
      +---------------------------------------------------------------+
```

### 3. 핵심 알고리즘 및 코드 로직 (Pseudo-code)
백로그 관리 시스템에서 우선순위를 자동 정렬하는 로직 예시다.

```python
# Python-like Pseudocode for Backlog Prioritization

def prioritize_backlog(requirements, total_sprint_capacity):
    """
    요구사항 리스트를 MoSCoW 규칙에 따라 정렬하고
    스프린트 용량에 맞게 슬라이싱하는 함수
    """
    # 1. Categorization (Business Value Score)
    # Score: Must=100, Should=75, Could=50, Won't=0
    for req in requirements:
        if req.negotiated_priority == 'Must':
            req.score = 100
        elif req.negotiated_priority == 'Should':
            req.score = 75
        elif req.negotiated_priority == 'Could':
            req.score = 50
        else:
            req.score = 0

    # 2. Sorting (High Score First)
    sorted_reqs = sorted(requirements, key=lambda x: x.score, reverse=True)

    # 3. Filtering (Knapsack Problem Approach)
    # 스프린트 총 용량(Effort Points)을 초과하지 않는 선까지 'Must'와 'Should'를 채우고,
    # 남은 공간에 'Could'를 채움.
    committed_backlog = []
    current_effort = 0

    for req in sorted_reqs:
        if current_effort + req.effort <= total_sprint_capacity:
            committed_backlog.append(req)
            current_effort += req.effort
        elif req.score == 100: 
            # 용량 초과 시에도 Must라면 협상이 필요하지만
            # 여기서는 예외로 처리하고 경고 발생
            raise Exception("Scope Exceeded: Too many Must-haves!")
        else:
            # 나머지는 W (Won't for this sprint)로 처리
            req.status = "Deferred" 
            
    return committed_backlog
```

### 📢 섹션 요약 비유
> "건물을 지을 때, 기둥과 벽(Must)을 먼저 세우지 않고 인테리어 조명(Could)이나 정원 조경(Won't)부터 시작하는 사람은 없습니다. 무너지지 않으려면 구조적 안전성(MVP)을 확보한 뒤에 미적 가치를 추구해야 하는 것과 같습니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: MoSCoW vs Kano Model

| 비교 항목 | MoSCoW Analysis | Kano Model (카노 모델) |
|:---|:---|:---|
| **관점** | **제약 관리 (Constraints)** | **심리학적 만족도 (Satisfaction)** |
| **주요 용도** | 프로젝트 범위(Scope) 결정, 일정 관리 | 제품 경험(UX) 설계, 기능 계획 |
| **분류 기준** | 비즈니스 임팩트, 필수 여부 | 당연적(基本), 일원적(一元), 매력적(魅力) |
| **시나리오** | "예산이 없으니 뺄 것을 정함" | "어떤 기능을 넣으면 고객이 환호하는가?" |
| **융합 시너지** | Kano 모델로 '매력적 요소'를 찾아내더라도, MoSCoW에 의해 'Could'로 분류되어 **늦춰질 수 있음(지연의 미학)**. | Kano의 '당연적 품질'을 MoSCoW의 'Must'로 자동 매핑하여 **기본기 부재 방지**. |

### 2. 과목 융합 관점: 네트워크 및 보안 (Security & Network)
요구사항 우선순위는 단순히 기능(Functionality)에만 국한되지 않는다.
*   **보안 융합**: 보안 요구사항(암호화, 접근 제어)은 사용자가 "원하지 않아도(Must)" 반드시 포함되어야 한다. 이를 **NFR (Non-Functional Requirement, 비기능적 요구사항)**과 결합하여 가중치를 부여한다.
*   **네트워크 융합**: **QoS (Quality of Service, 서비스 품질)** 개념과 유사하다.
    *   Must = **Premium Traffic** (항상 보장, 대역폭 우선 배정)
    *   Could = **Best Effort** (네트워크 혼잡 시 폐기 가능)

### 3. 의사결정 매트릭스 (Decision Matrix)

```text
      [High Business Value]
            ▲
            │
      M     │    S
 (Critical) │ (Important)
            │
◄───────────┼───────────► [Low Implementation Cost]
            │
      C     │    W
(Optional)  │ (Drop)
            │
            ▼
      [Low Business Value]
```
*   **M (Must)**: 가치가 높고 구현이 쉬운 '저개비 열매'.
*   **S (Should)**: 가치가 높지만 구현이 어려움 (기술적 과제).
*   **C (Could)**: 구현은 쉽지만 가치가 낮음.
*   **W (Won't)**: 가치도 낮고 구현도 어려움 (No-Brainer).

### 📢 섹션 요약 비유
> "고속도로의 차선 다이어그램과 같습니다. MoSCoW는 '버스 전용 차선(Must)'과 '일반 차선(Should)', 그리고 '갓길(Could)'을 구분하는 것입니다. Kano 모델은 운전자가 느끼는 '편안함(Satisfaction)'을 측정하는 것이라면, MoSCoW는 차량이 '멈추지 않게 흘러가게 하는(Latency 관리)' 교통 체계입니다."

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 핀테크 앱 MVP 출시
신규 뱅킹 앱 출시 프로젝트에서 1차 릴리스(2개월) 목표를 달성해야 한다.

*   **상황**: 보안 인증서(공동인증서) 연동 모듈 개발 이슈로 예산이 20% 초과 예상.
*   **적용**:
    *   **Must**: 계좌 이체, 잔액 조회, 생체 인증 (핵심 자금 이동).
    *   **Should**: 이체 내역 엑셀 다운로드 (중요하지만 모바일에서는 조회만 해도 됨).
    *   **Could**: 챗봇 상담, 다크 모드, 폰트 크기 조절 (UX 개선).
    *   **Won't**: 주식 투자 기능, 소액 결제 카드 (금융사 업무 추진 중).

*   **Decision**:
    1.  예산 부족으로 인해 'Could' 항목(챗봇, 다크 모드)을 전원 제외.
    2.  'Should' 항목 중 엑셀 다운로드를 2차 버전으로 연기.
    3.  절감한 예산을 'Must'인 보안 인증 연동에 투자하여 **안정성(Security)**을 확보.

### 2. 도입 체크리스트 (Validation Checklist)
*   **기술적 확인 (Technical)**:
    *   'Must' 항목 간의 **의존성(Dependency)**은 없는가? (하나가 막히면 다른 것도 막히는 순환 의존 방지)
    *