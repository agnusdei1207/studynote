+++
title = "191-200. 소프트웨어 설계 원칙 (Cohesion, Coupling)"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 191
+++

# 191-200. 소프트웨어 설계 원칙 (Cohesion, Coupling)

### # 소프트웨어 설계의 핵심 원칙
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 복잡도를 통제하기 위해 모듈 내부는 응집력을 높이고(High Cohesion), 모듈 간 의존성은 낮추는(Low Coupling) 구조적 정합성을 확보해야 함.
> 2. **가치**: 비즈니스 로직 변경 시 영향 범위를 최소화하여 유지보수 비용(Maintenance Cost)을 획기적으로 절감하고 시스템 수명을 연장함.
> 3. **융합**: 클린 아키텍처(Clean Architecture), 마이크로서비스(MSA) 등 현대 패러다임의 근간이 되는 이론적 토대.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
소프트웨어 공학(Software Engineering)에서 **모듈화(Modularity)**는 시스템을 독립적이고 상호 교환 가능한 부품으로 분해하는 행위입니다. 단순히 코드를 나누는 행위를 넘어, **변경의 파급효과(Controlled Propagation)**를 관리하는 핵심 전략입니다. 이때 모듈의 '품질'을 판단하는 정량적/정성적 척도가 바로 **응집도(Cohesion)**와 **결합도(Coupling)**입니다.

**2. 등장 배경**
① **기존 한계 (Spaghetti Code)**: 초기 개발에서는 절차적 프로그래밍(Procedural Programming)과 전역 변수(Global Variable)의 남용으로 인해, 특정 모듈 수정 시 연쇄적으로 사이드 이펙트(Side Effect)가 발생하는 '스파게티 코드' 문제가 대두됨.
② **혁신적 패러다임 (Structured Design)**: 1970년대 래리 콘스탄틴(Larry Constantine)과 에드워드 요던(Edward Yourdon) 등에 의해 구조적 설계(Structured Design) 이론이 정립되며, '강한 응집, 약한 결합'을 설계의 신조로 선포함.
③ **현재의 요구**: 클라우드 환경(Cloud Environment)과 대규모 분산 시스템에서는 수천 개의 마이크로서비스 간의 통신 비용과 오류 전파 경로를 최소화하기 위해 이 원칙이 더욱 절실함.

```ascii
+------------------+                     +------------------+
|   CHANGES IN     | --(Impact)--->      |   SYSTEM         |
|   MODULE A       |                     |   FAILURE?       |
+------------------+                     +------------------+
      | ^                                         | ^
      | |                                         | |
      v |                                         v |
(High Cohesion)                          (Low Coupling)
    |                                           |
    +---> Isolated Scope                        +---> Localized Effect
```
*도해: 높은 응집도는 변화를 모듈 내부에 가두고(Cage), 낮은 결합도는 변화가 외부로 전파되는 경로를 차단한다(Shield).*

**3. 💡 비유**
도시 계획에 비유하자면, **아파트 단지(High Cohesion)**는 주거 시설만 모아 생활 편의성을 높이고, **도로망(Low Coupling)**은 각 단지를 연결하되 서로 소음이나 교통 체증을 주지 않도록 격리하는 것과 같습니다.

> **📢 섹션 요약 비유**: 건물을 지을 때, 화장실 욕조, 변기, 세면대를 수도관로 긴밀히 연결해 배치하는 것이 **응집도**라면, 우리 집 화장실에서 물을 내려도 옆집 전기가 나가지 않도록 전기 배선을 따로 뽑는 것이 **결합도**입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 응집도 (Cohesion) - 내부의 결속력**
응집도는 모듈 내부 요소들이 얼마나 '한마음'으로 동작하는지를 나타내는 척도입니다. SRP(Single Responsibility Principle)의 실질적 지표입니다.

**[응집도의 7단계 계층 구조]**

| 단계 | 명칭 (영문) | 설명 | 예시 | 비유 |
|:---:|:---|:---|:---|:---|
| **상** | **기능적 (Functional)** | 모든 요소가 단 하나의 기능 수행에 기여 (최상) | `calcTax()` 함수 내의 로직들 | 정형외과 의사들만 모인 팀 |
| ⑥ | 순차적 (Sequential) | 한 활동의 출력이 다른 활동의 입력이 됨 | 데이터 읽기 → 암호화 → 전송 | 생산라인 (조립→포장) |
| ⑤ | 통신적 (Communication) | 동일한 입출력 데이터를 사용 (순차적보다 약함) | 고객 데이터를 이용해 화면 출력/보고서 출력 | 같은 재료를 쓰는 요리사들 |
| ④ | 절차적 (Procedural) | 순서에 의해 묶임 (데이터 공유 안 함) | 로그인 → 인증 → 로깅 (기능은 다름) | 정해진 순서대로 업무 처리 |
| ③ | 시간적 (Temporal) | 시점(Time) 기반으로 묶임 | 시스템 시작 시 `init()` 모음 | 야간 근무조 직원들 |
| ② | 논리적 (Logical) | 기능적으로 유사하나 논리적으로만 묶임 | `printAll()` (원형, 삼각형, 사각형 출력) | '출력' 관련 부서 (데스크, 복사기) |
| **하** | **우연적 (Coincidental)** | 관련 없는 요소들이 무작위로 묶임 (최악) | `A`, `B`, `C` 함수를 한 파일에 저장 | 낯선 사람들의 모임 |

```ascii
[응집도 내부 동작 비교]

High Cohesion (Functional)         Low Cohesion (Coincidental)
+-------------------------+         +-------------------------+
|  Calculate_Salary()     |         |  Utils_Module()         |
|  +-- Get_Base()         |         |  +-- Print_Report()     |
|  +-- Get_Tax()          |         |  +-- Open_Door()        |
|  +-- Calc_Final()       |         |  +-- Kill_Process()     |
|  [모두 급여 계산에 기여] |         |  [전혀 상관없는 기능들]  |
+-------------------------+         +-------------------------+
```

**2. 결합도 (Coupling) - 모듈 간의 독립성**
결합도는 한 모듈이 다른 모듈을 얼마나 '꼼짝없이 의존'하는지를 나타냅니다. DIP(Dependency Inversion Principle)의 기반이 됩니다.

**[결합도의 6단계 계층 구조]**

| 단계 | 명칭 (영문) | 설명 | 파급 영향 | 비유 |
|:---:|:---|:---|:---|:---|
| **상** | **자료 (Data)** | 인수(Parameter)를 통한 기본 데이터만 전달 (최상) | 함수 인자 변경 시 | 빈 쟁반만 전달 |
| ⑤ | 스탬프 (Stamp) | 데이터 구조(Object, Array) 전달 | 구조 변경 시 연쇄 수정 | 다양한 반찬이 담긴 도시락 전달 |
| ④ | 제어 (Control) | 제어 플래그(Flag)를 전달하여 로직 제어 | 로직 흐름 변경 시 | "오늘은 옆집 가서 잠" (지시) |
| ③ | 외부 (External) | 외부 포맷/프로토콜/물체 공유 | 포맷 변경 시 | 이웃이 같은 우물 공유 |
| ② | 공통 (Common) | 전역 변수(Global Data) 공유 | 변수 하나가 시스템 전체 멈춤 | 칸막이 없는 열린 사무실 |
| **하** | **내용 (Content)** | 내부 데이터/로직을 직접 참조/변경 (최악) | 내부 구현 바뀌면 즉사 | 내 집 가방을 남이 뒤적거림 |

```ascii
[결합도별 데이터 흐름도]

A. Data Coupling (이상적)          B. Content Coupling (최악)

[Module A]    (int x)    [Module B]   [Module A]      >>Direct<<    [Module B]
  Logic  -----> Data ---->  Logic       Logic  ------> Memory       Logic
(구조 몰라도 됨)                         (B의 내부 RAM을 A가 킥킥대며 수정)
```

**3. 심층 동작 메커니즘**
- **Fan-in / Fan-out**: 
  - `Fan-in`: 특정 모듈을 호출하는 상위 모듈의 수. 높을수록 재사용성이 높으나, 과도하면 성능 병목 발생.
  - `Fan-out`: 특정 모듈이 호출하는 하위 모듈의 수. 높을수록 복잡도가 증가. 일반적으로 `Fan-out ≤ 7`을 권장.
- **정보 은닉 (Information Hiding)**: 
  - 모듈의 결합도를 낮추기 위한 기법. Parnas(1972) 제안.
  - 데이터(Data)와 로직(Procedure)을 캡슐화(Capsulation)하고 인터페이스(Interface)만 노출하여, 변경 시 다른 모듈로의 전파를 차단(Ripple Effect Prevention).

> **📢 섹션 요약 비유**: **응집도**는 '전문성'입니다. 9회말 투수만 던지는 것이 기능적 응집도이고, 투수가 타석도 서고 라디오도 진행하는 것은 우연적 응집도입니다. **결합도**는 '연애 관계'입니다. 서로 껴안고 있는 것(Content Coupling)보다는, 서로 편지를 주고받는 것(Data Coupling)이 헤어졌을 때 훨씬 덜 아픕니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 상관관계 분석표 (Correlation Analysis)**

| 구분 | 목표 | 설계 방향 | 주요 패턴/기술 | 장점 | 단점 |
|:---:|:---:|:---:|:---|:---|:---|
| **응집도** | **높임(High)** | 모듈을 기능 단위로 세분화 | Strategy Pattern, Facade Pattern | 이해도 향상, 디버깅 용이 | 모듈 수 증가 관리 부담 |
| **결합도** | **낮춤(Low)** | 인터페이스 중심 설계, DI(Dependency Injection) 적용 | API, RESTful, Event Bus | 유지보수성 극대화, 병렬 개발 가능 | 데이터 동기화 비용 증가 |

**2. 타 과목 융합 관점**

1.  **데이터베이스 (DB)와의 관계**: 
    - 높은 응집도와 낮은 결합도는 데이터 정규화(Normalization)의 목표와 일맥상통합니다. 정규화는 데이터 중복을 줄여(응집), 이상 현상(Anomaly)을 방지(결합 감소)합니다. 역정규화(Denormalization)는 성능을 위해 결합도를 의도적으로 높이는 트레이드오프(Trade-off) 사례입니다.
2.  **네트워크와의 관계**: 
    - **OSI 7계층**은 계층 간 결합도를 낮추기 위한 완벽한 설계 사례입니다. 물리 계층이 바뀌어도 응용 계층에 영향을 주지 않습니다. 반면, 모놀리식(Monolithic) 네트워크 대신 마이크로서비스(MSA)를 채택하면 서비스 간 결합도는 낮아지지만, 네트워크 트래픽 결합도(Latency Dependency)는 관리 포인트가 됩니다.

```ascii
[좋은 설계 vs 나쁜 설계의 변화 파급도]

Before: High Coupling (Low Cohesion)
      [User Class] --(Change Code)--> [System Crash] (All modules linked)
      
After: Low Coupling (High Cohesion)
      [User Class] --(Change)--> [Log Module] (Only affected)
           |                          ^
           | (Interface Call)         | (Unchanged)
           v                          |
       [Product Module] --------> [Inventory Module]
```

**3. 정량적 의사결정 매트릭스**
- **변경 영향도 분석 (Change Impact Analysis)**:
  - 좋은 설계: 1줄 코드 수정 시 연관 모듈 변경 수 ≤ 1개
  - 나쁜 설계: 1줄 코드 수정 시 연관 모듈 변경 수 ≥ 5개 (도미노 현상)

> **📢 섹션 요약 비유**: 자동차 설계에서 **엔진(Engine)**과 **타이어(Tire)**는 각각 완벽하게 자체적으로 돌아가게 만들고(높은 응집도), 그 사이를 표준화된 볼트와 너트(낮은 결합도)로만 연결해야, 엔진을 6기통으로 바꿔도 타이어를 바꿀 필요가 없습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 프로세스**

*   **상황 1: 거대한 'God Class' 발견 (낮은 응집도)**
    *   **문제**: `OrderManager` 클래스가 주문 생성, 결제, 알림 발송, 로그 저장까지 전부 담당함.
    *   **의사결정**: **SRP(단일 책임 원칙) 위배** 판정. 기능별 분리(Split) 수행.
    *   **해결**: `OrderService`, `PaymentService`, `NotificationService`로 분리하여 응집도를 '기능적(Functional)' 수준으로 상향.
*   **상황 2: 타사 라이브러리 업데이트 시 시스템 전체 오류 (높은 결합도)**
    *   **문제**: A사 캘린더 라이브러리를 코드 곳곳에서 `import`하여 직접 사용. 라이브러리 버전 업 시 컴파일 에러 발생.
    *   **의사결정**: **내용 결합(Content Coupling) 판정**. 인터페이스 분리 필요.
    *   **해결**: **Facade 패턴** 또는 **Adapter 패턴** 적용. 외부 라이브러리 변경 사항이 우리 시스템으로 직접 전달되지 않도록 방어막(Wrapper) 구축.

**2. 설계 체크리스트 (Checklist)**

| 구분 | 점검 항목 | 확인 방법 |
|:---:|:---|:---|
| **기술적** | 단일 목적성? | 함수나 클래스 이름이 'And'를 포함하지 않는가? (예: `PrintAndSave`