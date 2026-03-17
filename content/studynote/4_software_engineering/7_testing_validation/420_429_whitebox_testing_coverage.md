+++
title = "420-429. 화이트박스 테스트와 커버리지 (MC/DC)"
date = "2026-03-14"
[extra]
category = "Testing"
id = 420
+++

# 420-429. 화이트박스 테스트와 커버리지 (MC/DC)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 화이트박스 테스트(White-box Test)는 내부 논리와 제어 흐름을 가시화하여 결함을 탐지하는 구조 기반 검증 기법입니다.
> 2. **가치**: SW 결함으로 인한 사고 비용을 선제적으로 차단하며, 특히 MC/DC (Modified Condition/Decision Coverage)는 사망자가 발생할 수 있는 시스템(Catastrophic)의 잠재적 오류를 99% 이상 검출합니다.
> 3. **융합**: 정적 분석 도구(Static Analysis)와 CI/CD 파이프라인 결합을 통해 코드 품질 지표를 자동화하고, 임베디드 및 항공 산업의 안전성 표준(DO-178C)을 충족합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**화이트박스 테스트(White-box Test)** 또는 **구조 기반 테스트(Structure-based Test)**는 소프트웨어의 내부 작동을 세부적으로 수행하는 테스트 방법론입니다. 테스트자는 소스 코드(Source Code), 알고리즘, 설계도 등 내부 구조를 완전히 이해하고 있다는 가정하에, 논리적인 경로와 조건절을 분석합니다. 이는 '유리 상자(Glass Box) 테스트'라고도 불리며, 단순히 입력값에 대한 출력값만 확인하는 블랙박스 테스트와 대조됩니다.

### 2. 기술적 배경 및 필요성
- **한계 극복**: 초기 프로그래밍에서는 단순 실행(Execution)으로 오류를 찾았으나, 소프트웨어의 복잡도(Cyclomatic Complexity)가 폭증하며 내부의 눈에 보이지 않는 경로(Logical Path)에서 결함이 발생하기 시작함.
- **품질 보증**: 소프트웨어가 처리해야 할 모든 논리적 조합을 수행해 보지 않으면, 특정 조건에서만 발생하는 휴면 버그(Heisenbug)가 배포 단계에서 터질 가능성이 존재함.
- **표준화 요구**: 산업계 전반에서 SW 품질을 정량적으로 수치화하여 보증할 수 있는 척도(Scale)의 필요성 대두.

```ascii
       [ 블랙박스 vs 화이트박스 ]

       +-----------------------+          +-----------------------+
       |      BLACK BOX        |          |      WHITE BOX        |
       |      (Function)       |          |      (Structure)      |
       +-----------------------+          +-----------------------+
       |  Input  --> [ ? ] --> Output     |  Code   --> [ Trace ] |
       +-----------------------+          |       Analysis        |
                                       +-----------------------+
                                       | [ 알고리즘 로직 검증 ] |
                                       | [ 모든 경로 수행 확인 ] |
                                       +-----------------------+
```
*해설: 블랙박스가 기능적 요구사항을 만족하는지 확인하는 '외부 관점'이라면, 화이트박스는 소프트웨어 내부의 복잡한 톱니바퀴가 예상대로 회전하는지 직접 들여다보는 '내부 관점'입니다.*

### 3. 💡 비유
프로그래머가 작성한 코드는 **복잡한 미로 지도**와 같습니다. 화이트박스 테스트는 지도를 손에 들고 미로의 모든 통로를 직접 걸어다니며 "이 길은 막혀있지 않은가?", "이곳을 지나면 반드시 저곳으로 연결되는가?"를 확인하는 과정입니다.

### 📢 섹션 요약 비유
화이트박스 테스트는 **투명한 자동차 후드를 열고 엔진 내부의 피스톤 운동과 밸브 열림/닫힘을 육안으로 검사하며, 연결 파이프의 누수 여부를 확인하는 정비 공장의 정밀 진단 과정**과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 코드 커버리지 (Code Coverage) 상세 분석
테스트의 완성도를 측정하는 핵심 지표인 **커버리지(Coverage)**는 단순한 실행 비율을 넘어 논리적 완전성을 보장해야 합니다. 테스트 대상의 복잡도와 안전성 요구 수준에 따라 다음과 같은 단계로 적용됩니다.

| Level | 명칭 (Name) | 정의 (Definition) | 한계 및 특이사항 |
|:---:|:---|:---|:---|
| **1** | **구문 커버리지**<br>(Statement Coverage) | 소스 코드의 **실행 가능한 모든 문장(Statement)**을 최소 1회 이상 실행. | 가장 기초적이며 낮은 수준. `if`문의 조건이 `True`여서 실행되었더라도 `False` 경로의 내부 로직은 검증 불가. |
| **2** | **결정 커버리지**<br>(Decision/Branch Coverage) | 프로그램의 **모든 분기점(Branch)**에서 `True`와 `False` 결과를 최소 1회 이상 생성. | `else`가 없는 `if`문 등을 포함하여 모든 진입/진출 경로 확인. 구문 커버리지를 상호 포함함. |
| **3** | **조건 커버리지**<br>(Condition Coverage) | 복합 조건식 내의 **개별 조건(Atomic Condition)**이 최소 1회 이상 `True`/`False`를 가짐. | 결정 커버리지와 독립적이지 않음. 각 조건이 `True`/`False`여도 전체 결과가 항상 `True`가 나올 수도 있음. |
| **4** | **조건/결정 커버리지**<br>(Condition/Decision Coverage) | 개별 조건과 전체 결정 결과 모두를 만족시키는 조합. | 업계 표준 품질 수준이나, 상호 독립성 검증에는 부족함. |
| **5** | **MC/DC**<br>(Modified Condition/Decision Coverage) | **각 조건이 독립적으로** 결정 결과에 영향을 미침을 증명. | Safety-Critical 시스템(항공, 원전) 필수 표준. |
| **6** | **경로 커버리지**<br>(Path Coverage) | 가능한 **모든 실행 경로**를 테스트. (Loop $n$회 등) | 이론적 완벽성을 제공하나, 경로의 조합 폭발(Combinatorial Explosion)으로 인해 현실적으로 전체 적용이 불가능. |

### 2. MC/DC (Modified Condition/Decision Coverage) 심층 분석
**MC/DC**는 DO-178C(항공 SW 표준) 등에서 Level A(잔향사 발생 가능성 있는 SW)에 대해 요구하는 가장 엄격한 커버리지 중 하나입니다.

*   **독립성 독립(Independence)**: 복합 조건식 `A and B`에서, `A`의 값이 바뀔 때 전체 결과가 바뀌더라도, 이것이 `B`의 상태와 무관하게 증명되어야 합니다.
*   **요건 충족을 위한 최소 조건**:
    1.  각 조건이 `True`/`False`를 가짐.
    2.  각 결정이 `True`/`False`를 가짐.
    3.  각 조건이 결과에 독립적으로 영향을 미치는 쌍(Coupling)이 존재.

```ascii
   [ MC/DC 독립성 증명 예시 ]
   로직: Result = (A or B) and C
   
   Test Case Set:
   ┌───┬───┬───┬───────────┐
   │ A │ B │ C │  Result   │  설명
   ├───┼───┼───┼───────────┤
   │ T │ T │ T │    T      │  [베이스]
   ├───┼───┼───┼───────────┤
   │ F │ T │ T │    F      │  A의 변화(F)가 결과를 T→F로 변경 (B,T / C,T 고정)
   ├───┼───┼───┼───────────┤
   │ T │ F │ T │    T      │  B의 변화(F)가 결과에 영향 없음 (독립성 입증 불가 - 재시도 필요)
   └───┴───┴───┴───────────┘
   
   [수정된 Test Case]
   Case 1: A=T, B=F, C=T → Result=T
   Case 2: A=F, B=F, C=T → Result=F (A의 독립성 입증 성공: B는 F로 고정, 결과 변화)
   Case 3: A=T, B=T, C=T → Result=T (B의 독립성 입증: A=T, C=T 고정, 결과 변화)
```
*해설: 위 표는 MC/DC를 만족하는 테스트 케이스 설계 과정입니다. 특정 조건(A)을 변경할 때, 다른 조건(B, C)을 고정시킨 상태에서 결과가 바뀌면 A가 독립적인 영향력을 가진다고 증명하는 것입니다.*

### 3. 루프 테스팅 (Loop Testing)
화이트박스 테스트의 또 다른 축은 반복문(Iteration)의 검증입니다.

```ascii
       [ 루프 테스트 전략 ]

       (Simple Loop Strategy)
       ┌───────────────────────────────┐
       │   1. Skip Loop (0 회)          │ --> 경계값 미충족 검증
       │   2. One Pass (1 회)           │ --> 초기 조건 검증
       │   3. Two Passes (2 회)         │ --> 반복 재진입 검증
       │   4. Typical Passes (m 회)     │ --> 정상 수행 검증
       │   5. Max-1 Passes (n-1 회)     │ --> 최대 경계 직전 검증
       │   6. Max Passes (n 회)         │ --> 최대 경계 검증
       └───────────────────────────────┘
       
       [Nested Loop] → [Concentric Strategy]
       Outer Loop를 Min으로 고정하고 Inner Loop를 전체 테스트 후,
       순차적으로 Outer Loop 값을 증가시키며 검증.
```

### 4. 핵심 알고리즘: McCabe의 복잡도(Metric)
테스트 케이스의 최소 개수를 결정하는 정량적 지표입니다.
$$ V(G) = E - N + 2P $$
( $E$: Edge 수, $N$: Node 수, $P$: Connected Component 수 )

```python
# Cyclomatic Complexity Calculation Example
def test_logic(a, b, c):
    if a > 0:        # Node 1, Decision 1
        if b > 0:    # Node 2, Decision 2 (Nested)
            c = 1    # Node 3
    else:
        if c > 0:    # Node 4, Decision 3
            c = 2    # Node 5
    return c         # Node 6

# 구조 분석:
# Node: 6개, Region: 3개 (화이트박스 시각화)
# V(G) = 3 (Predicate Nodes) + 1 = 4
# 최소 4개의 테스트 케이스가 필요함을 의미
```

### 📢 섹션 요약 비유
화이트박스와 커버리지는 **보석상이 다이아몬드(코드)를 감정할 때, 일반 눈으로 전체를 보는 것(구문)에서 시작해, 확대경으로 각 면의 깨짐 유무(결정)를 보고, 최신 기기로 각 결정이 빛을 어떻게 분산시키는지(MC/DC) 분석하는 과정**과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 블랙박스 vs 화이트박스 기술 비교

| 구분 | 화이트박스 테스트 (White-box) | 블랙박스 테스트 (Black-box) |
|:---|:---|:---|
| **관점 (Perspective)** | **내부**: 코드, 알고리즘, 논리 흐름 | **외부**: 입력(Input)과 출력(Output) |
| **담당자 (Performer)** | 개발자 (Developer), 시스템 아키텍트 | 테스터 (QA), 사용자 (User) |
| **방법론 (Method)** | 제어 흐름 그래프, 데이터 흐름 분석 | 동등 분할(Equivalence Partitioning), 경계값 분석 |
| **도구 (Tools)** | JUnit, JaCoCo, Gcov, SonarQube | JIRA, Selenium, Postman |
| **결함 탐지** | "코드가 **어떻게** 작동하지 않는가?" | "요구사항이 **무엇을** 못하는가?" |
| **시점 (Timing)** | 개발 초기 단계(Unit Test 단계)부터 가능 | 통합 테스트 및 시스템 테스트 단계 |

### 2. 데이터 흐름 테스팅 (Data Flow Testing)과의 시너지
단순한 제어 흐름(Control Flow)을 넘어 변수의 생명주기를 추적하는 **DFT (Data Flow Testing)**는 화이트박스 테스트의 심화 단계입니다.
*   **DU Chain (Definition-Use Chain)**: 변수가 정의(Define)된 지점부터 사용(Use)되는 지점까지의 흐름을 추적합니다.
*   **P-Use / C-Use**: 조건문(Usage in Predicate)에서의 사용과 연산(Usage in Computation)에서의 사용을 분리하여, 정의되지 않은 변수가 사용되는 결함을 사전에 차단합니다.

```ascii
   [ Data Flow Anomaly Example ]
   
   1. int x = 10;      -- (d: definition)
   2. if (y > 5) {     
   3.     x = x + 5;   -- (c-use: computation use)
   4. }
   5. return x;        -- (c-use)
   
   [Analysis]
   변수 'y'는 사용(Use)되었지만 정의(Define)된 적이 없음.
   -> "Undefined Variable" Anomaly 탐지 가능.
   이는 화이트박스(정적 분석)만이 가능한 탐지임.
```

### 3. 정적 분석(Static Analysis)과의 융합
최신 현장에서는 수동 화이트박스 테스트보다는 **SAST (Static Application Security Testing)** 도구가 자동으로 화이트박스 커버리지를 측정합니다.
*   **Synergy**: 테스트 코드 작성 시 SonarQube 등이 실시간으로 커버리지를 시각화하여, 개발자가 "테스트가 부족한 분기"를 즉시 보완하게 함.

### 📢 섹션 요약 비유
화이트박스와 블랙박스의 융합은 **자동차 설계사(화이트박스)가 엔진 열을 시뮬레이션하는 동시에, 운전자(블랙박스)가 실제로 운전을 하