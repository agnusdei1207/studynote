+++
title = "768. 럼바우 객체 모델링 (객체/동적/기능 모델)"
date = "2026-03-15"
weight = 768
[extra]
categories = ["Software Engineering"]
tags = ["OOAD", "Rumbaugh", "OMT", "Object Modeling", "Dynamic Modeling", "Functional Modeling", "UML History"]
+++

# 768. 럼바우 객체 모델링 (객체/동적/기능 모델)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 제임스 럼바우(James Rumbaugh)가 제안한 **OMT (Object Modeling Technique)**는 시스템을 정적 구조, 동적 행동, 데이터 변환의 3가지 차원에서 입체적으로 분석하는 객체지향 분석(OOA) 방법론의 정수입니다.
> 2. **가치**: 단순한 코드 작성을 넘어 시스템의 '구조-상태-기능'을 모델링함으로써 요구사항 누락을 최소화하고, 현대 **UML (Unified Modeling Language)** 탄생의 학문적 토대를 마련했습니다.
> 3. **융합**: 정적 다이어그램(객체), 상태 다이어그램(동적), 자료 흐름도(기능)의 결합을 통해 임베디드 시스템 및 대규모 클라우드 아키텍처의 유스케이스를 명세하는 데 필수적인 패러다임을 제공합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**OOM (Object-Oriented Modeling)**의 일종인 OMT는 1991년 제임스 럼바우가 저서 *Object-Oriented Modeling and Design*을 통해 정립한 방법론입니다. 당시 구조적 분석(SA, Structured Analysis) 방법인 **DFD (Data Flow Diagram)**와 **ERD (Entity Relationship Diagram)**의 한계를 극복하고자, 실세계를 객체(Object) 중심으로 바라보되, 시스템의 '변화'와 '기능'까지 기술하기 위해 고안되었습니다.

#### 2. 💡 비유: 건축 설계의 3단계
럼바우의 3대 모델은 건물을 지을 때의 설계 과정과 유사합니다.
*   **객체 모델링**: 건물의 **구조적 설계도(뼈대)**. 기둥과 보(클래스)가 어디에 위치하고 어떻게 연결되었는지를 정의합니다. (가장 기본이 됨)
*   **동적 모델링**: 건물의 **스마트 홈 시스템(흐름)**. 거주자의 출입이나 조도 변화(이벤트)에 따라 조명이 켜지고 문이 열리는 상태 변화를 정의합니다.
*   **기능 모델링**: 건물의 **기계 설비 계산(로직)**. 냉난방 시스템이 현재 온도(입력)를 받아 설정 온도에 맞춰 에너지를 조절(출력)하는 데이터 처리 과정을 정의합니다.

#### 3. 등장 배경 및演进
① **구조적 분석(Structured Analysis)의 한계**: 데이터와 프로세스를 분리하여 분석함으로써, 요구사항 변경 시 유지보수가 어려운 문제가 존재했습니다.
② **객체지향 패러다임의 대두**: 현실 세계의 사물을 그대로 모델링함으로써 소프트웨어의 복잡도를 낮추려는 움직임이 일었습니다.
③ **OMT의 등장**: 객체(Object) 중심의 정적 모델링에, 상태(State)와 동작(Operation)을 통합하여 시스템을 3차원으로 분석하는 틀을 제시하며, 후에 UML 통합의 핵심 축이 되었습니다.

#### 📢 섹션 요약 비유
> "마치 영화 제작에서 **캐릭터 설정(객체)**을 먼저 완료하고, 그 다음 **대본과 연기(동적)**을 구상하며, 마지막으로 **특수효과(기능)**를 합성하여 완성작을 만드는 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 럼바우 3대 모델 상세 구조

럼바우 방법론은 시스템을 바라보는 3가지 시각(Viewpoint)을 제공하며, 이들은 상호 보완적입니다.

| 모델 명칭 | 영문 명칭 | 핵심 관점 (Perspective) | 주요 다이어그램 | 주요 표기 요소 | UML 선행자 |
|:---:|:---|:---|:---|:---|:---|
| **객체 모델링** | **Object Model** | **정적 구조 (Static Structure)** | **객체 다이어그램**<br>(Object Diagram) | 클래스(Class), 속성(Attribute)<br>연관(Association), 상속(Inheritance) | 클래스 다이어그램<br>(Class Diagram) |
| **동적 모델링** | **Dynamic Model** | **제어 흐름 (Control Flow)** | **상태 다이어그램**<br>(State Transition Diagram) | 상태(State), 이벤트(Event)<br>액션(Action), 활동(Activity) | 상태 머신 다이어그램<br>(State Machine Diagram) |
| **기능 모델링** | **Functional Model** | ** 데이터 변환 (Data Transformation)** | **자료 흐름도**<br>(Data Flow Diagram) | 프로세스(Process), 데이터 저장소(Data Store)<br>액터(Actor), 자료 흐름(Data Flow) | 액티비티 다이어그램<br>(Activity Diagram) |

#### 2. 아키텍처: 3대 모델의 상호작용

이 세 모델은 독립적으로 존재하는 것이 아니라 밀접하게 연결됩니다. '객체'가 '상태'를 가지며, '기능'을 수행하는 구조입니다.

```text
      ┌──────────────────────────────────────────────────────────┐
      │                Rumbaugh OMT System View                  │
      └──────────────────────────────────────────────────────────┘
     
      [ 1. Object Model (Structure / Skeleton ) ]  ←─ 가장 기본적이고 중요
      ────────────────────────────────────────────────────────────
      +---------------------+       +----------------------+
      |      Class A        |<>-----|      Class B         |
      |  (Attributes: ...)  | 1:N   |  (Operations: ...)   |
      +---------------------+       +----------------------+
               ▲                                    ▲
               │ Identity                           │ Reference
               │                                    │
      ─────────┼────────────────────────────────────┼────────────────
      [ 2. Dynamic Model (State / Interaction ) ]   │
      ────────────────────────────────────────────────────────────────
      (Event) 'click'  ──▶  [ State: Idle ]  ──▶  [ State: Running ] 
                                    ▲               │
                                    │               ▼
                              (Time Event)    (Action: B.process())
                                                    │
      ──────────────────────────────────────────────┼────────────────
      [ 3. Functional Model (Transformation ) ]     │
      ────────────────────────────────────────────────────────────────
      Input (X) ──▶ [ Process: Calculate Logic ] ──▶ Output (Y)
                    └─ Data Store Read/Write
```

**다이어그램 해설:**
1.  **Object Model**: 시스템의 뼈대입니다. 클래스 A와 클래스 B가 연관 관계(`<>`)로 맺어져 있으며, 이들의 정적 스키마(Schema)를 정의합니다.
2.  **Dynamic Model**: 객체가 갖는 상태(Idle, Running)와 이를 변화시키는 이벤트(click, Time Event)를 기술합니다. 상태 전이 시 내부적으로는 연관된 객체(Class B)의 오퍼레이션(Operation)을 호출합니다.
3.  **Functional Model**: 상태 내에서 발생하는 구체적인 데이터 변환 로직입니다. 입력값 X를 받아 비즈니스 로직(Process)을 수행한 뒤 결과값 Y를 반환하는 과정을 DFD로 표현합니다.

#### 3. 심층 동작 원리 (Deep Dive Mechanism)

**A. 객체 모델링 (The "What")**
시스템을 구성하는 **Entity(실체)**를 식별하고 이들의 관계를 맺습니다.
*   **동작 메커니즘**: 현실 세계의 사물을 `Class`로 추상화하고, 이들이 데이터를 저장하는 `Attribute`와 행위를 정의하는 `Operation`을 명세합니다.
*   **관계(Relationship)**: 
    *   **일반화(Generalization)**: "is-a" 관계 (상속).
    *   **연관(Association)**: "has-a" 또는 "uses" 관계.
    *   **집합(Aggregation)**: 전체-부품(Part-of) 관계.

**B. 동적 모델링 (The "When")**
시스템의 **Control(제어)** 측면을 기술합니다.
*   **상태(State)**: 객체의 생명 주기 동안 특정 시간에 가지는 조건(Condition).
*   **이벤트(Event)**: 상태 변화를 유발하는 자극(Stimulus).
*   **상태 전이(State Transition)**: `State A --[Event]--> Action --> State B`의 수학적 그래프 모델을 따릅니다. 이는 임베디드 시스템의 **FSM (Finite State Machine)** 설계의 핵심입니다.

**C. 기능 모델링 (The "How")**
데이터의 **Flow(흐름)**와 **Transformation(변환)**을 기술합니다.
*   **프로세스(Process)**: 입력 데이터를 출력 데이터로 변환하는 알고리즘.
*   **액터(Actor)**: 시스템 외부에서 데이터를 입력하거나 출력을 받는 대상(사용자, 외부 센서 등).
*   **데이터 저장소(Data Store)**: 데이터가 저장되는 곳(DB, 파일).

#### 4. 핵심 알고리즘 및 코드 표현

동적 모델링에서 정의한 상태 전이 로직이 실제 코드(Java Style)로 구현되는 예시입니다.

```java
// 💡 Concept: Mapping State Model to Code
public class DoorController {
    
    // [Object Model] Attribute Definition
    private DoorState currentState = DoorState.CLOSED;

    // [Dynamic Model] State Transition Logic
    // Event: 'click' received from User
    public void handleClickEvent() {
        switch (currentState) {
            case CLOSED:
                // Action: Change state, Activate Motor
                this.currentState = DoorState.OPENING;
                activateMotor(OpenDirection.UP);
                break;
                
            case OPENING:
                // Action: Ignore or Stop (Emergency Stop)
                this.currentState = DoorState.STOPPED;
                break;
                
            case OPEN:
                // Action: Start Closing
                this.currentState = DoorState.CLOSING;
                break;
            // ... (Other states)
        }
    }
    
    // [Functional Model] Data Transformation Logic (Internal Process)
    private void activateMotor(OpenDirection dir) {
        // Input: Direction -> Process: PWM Signal Calculation -> Output: Motor Voltage
        int pwmValue = calculatePWM(dir); 
        hardwareInterface.sendSignal(pwmValue);
    }
}
```

#### 📢 섹션 요약 비유
> "마치 **자동차 설계도면**을 그리는 것과 같습니다. **차체와 부품들의 배치도(객체 모델)**를 그리고, **운전자의 브레이크 페달 조작에 따른 제동 로직(동적 모델)**을 설계하며, 마지막으로 **연료가 엔진을 거쳐 동력으로 변환되는 과정(기능 모델)**을 수식으로 증명하는 과정입니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 럼바우(OMT) vs 부치(Booch) vs 야콥슨(OOSE)

UML 통합 이전의 3대 주요 방법론론 비교 분석입니다.

| 비교 항목 | 럼바우 (OMT) | 부치 (Booch) | 야콥슨 (OOSE) |
|:---|:---|:---|:---|
| **핵심 초점** | **분석(Analysis)** 중심 | **설계(Design)** 중심 | **유스케이스(Use Case)** 중심 |
| **주요 표기법** | OMT Diagrams (Object, State, DFD) | Booch Diagrams (Class, Object, State, Module) | Use Case + Objectory |
| **상세화 수준** | 개념적/논리적 모델링에 강함 | 구현(Inheritance, Message Passing)에 강함 | 요구사항 정의 및 사용자 관점에 강함 |
| **UML 기여도** | 구조 다이어그램(클래스)의 기초 제공 | 구현 다이어그램, 프로세스 뷰 기초 제공 | 유스케이스 다이어그램, 액티비티 기초 제공 |
| **특징** | "삼각형 균형(Object+Dynamic+Functional)" | "마이크로/매크로 프로세스" | "드라이버(Use Case) 중심 개발" |

#### 2. 기술적 시너지: 정형 기법(Formal Method)과의 융합

**동적 모델링(Dynamic Model)**의 상태 기계(State Machine) 개념은 소프트웨어 공학의 정형 기법(ES-V, VDM)과 연결됩니다.

```text
┌─────────────────────────────────────────────────────────────┐
│          Synergy with Formal Verification (Z-Notation)      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [ OMT State Diagram ]          [ Formal Specification ]   │
│                                                             │
│   State S1 --[Op(x)]--> S2    =>    S1' = InitState         │
│                                       Op(x) == (val > 0)    │
│                                       NextState = S2        │
│                                                             │
│   → SW 시스템의 안전성(Safety)과 생존성(Liveness)을 수학적   │
│     증명이 가능한 논리로 변환 가능.                          │
│     (예: 철도 신호 시스템, 원자력 발전소 제어 로직)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이러한 접근은 복잡한 **임베디드 시스템**이나 **블록체인 스마트 컨트랙트**의 논리를 검증할 때 매우 유용합니다.

#### 3. DFD (Structured) vs OMT (Object) Paradigm Shift

| 특징 | 구조적 분석 (SA/DFD) | 객체지향 분석 (OOM/OMT) |
|:---|:---|:---|
| **중심** | **Function(기능)** 중심 | **Object(객체)** 중심 |
| **데이터와 프로세스** | 분리되어 있음 (Decoupled) | 객체 내부에 캡슐화 (Encapsulated) |
| **변경에 대한 대응** | 기능 변경 시 전체 DFD 수정 영향 | 객체 인터페이스가 안정적일 경우 내부 로직 변경의 파급 최소화 |
| **현실 모방** | 어려움 | 용이함 (Real-world mapping) |

#### 📢 섹션 요약 비유
> "마치 **지도 제작**의 진화와 같습니다. 단순히 '길(기능)'만 표시하던 **고물 지도(구조적 분석)**에서, **지형, 건물, 교통 흐름(객체+상태)**을 입체적으로 수록한 **내비게이션 지도(UML/OMT)**로 패러다임이 이동