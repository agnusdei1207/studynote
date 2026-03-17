+++
title = "361-363. 소프트웨어 복잡도와 메트릭 (McCabe, Halstead, CK)"
date = "2026-03-14"
[extra]
category = "Quality Management"
id = 361
+++

# 361-363. 소프트웨어 복잡도와 메트릭 (McCabe, Halstead, CK)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 복잡도는 주관적인 감이 아닌, 제어 흐름(Control Flow)과 어휘(Vocabulary), 설계 구조(Design Structure)를 수치화하여 정량적으로 측정해야 하는 객체적 지표입니다.
> 2. **가치**: McCabe의 $V(G)$는 결함 예측, Halstead의 Volume은 노동량 산정, CK 메트릭스는 리팩토링 포인트 도출을 통해 유지보수 비용을 최소화하고 테스트 커버리지를 최적화합니다.
> 3. **융합**: 정적 분석(Static Analysis) 도구와 CI/CD 파이프라인을 결합하여, 코드 병합(Merge Request) 시점에 품질 기준(Threshold)을 초과하는 복잡한 코드를 자동으로 검출하고 차단하는 DevOps 품질 관리가 핵심입니다.

---

### Ⅰ. 개요 (Context & Background)

**개념**
소프트웨어 메트릭(Software Metrics)은 소프트웨어의 특성을 정량적으로 측정한 값입니다. 특히 복잡도(Complexity) 메트릭은 시스템의 내부 품질을 진단하는 척도로, 소프트웨어가 얼마나 많은 자원을 소비하고 얼마나 많은 결함을 내재할 확률이 높은지를 예측합니다. 이는 단순한 코드 라인 수(Line of Code)를 넘어, 제어의 흐름, 연산자의 사용 빈도, 객체 간의 결합도 등 다차원적 분석을 필요로 합니다.

**💡 비유**
도시 교통 상황을 분석하는 것과 같습니다. 단순히 도로의 총 길이(Km)가 중요한 것이 아니라, 교차로와 고차로 입구(분기)가 얼마나 복잡한지(McCabe), 차량과 신호등의 밀도(Halstead), 그리고 건물 간의 연결 통로가 얽히고설킨 정도(CK)를 파악해야 교통 체증(버그)을 예방할 수 있습니다.

**등장 배경**
1.  **기존 한계**: 초기 소프트웨어 개념에서는 크기(LOC, Lines of Code)만으로 생산성을 판단했으나, 기능의 복잡도에 비례하여 결함이 급증한다는 '콘웨이 법칙(Conway's Law)'과 소프트웨어 난이도의 비선형성을 설명하지 못했습니다.
2.  **혁신적 패러다임**: 1970년대 McCabe는 그래프 이론을 도입하여 논리적 복잡도를 정의했고, Halstead는 정보 이론(Information Theory)을 적용하여 코드를 언어적 구조로 해석했습니다. 이후 1990년대 객체지향(OOP)이 대두되며 Chidamber & Kemerer는 클래스 기반의 설계 복잡도를 제안했습니다.
3.  **현재의 비즈니스 요구**: 모던 애자일(Modern Agile) 환경에서는 '기술 부채(Technical Debt)' 관리가 중요해졌습니다. 정적 분석 도구(SonarQube 등)를 통해 이러한 메트릭스를 실시간으로 모니터링하고, 리팩토링 우선순위를 결정하는 데이터 기반 품질 관리(Data-Driven Quality Management)가 필수적입니다.

📢 **섹션 요약 비유**: 건물을 짓는 데 철근(코드)의 양만 세는 것이 아니라, 설계도의 구조적 안정성(복잡도)을 계산하여 무너질 위험을 미리 예측하는 '구조 안전 진단'과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

소프트웨어 복잡도 측정은 크게 절차적 코드의 흐름을 보는 McCabe, 언어적 요소를 보는 Halstead, 그리고 객체지향적 구조를 보는 CK 메트릭스로 나뉩니다.

#### 1. 구성 요소 비교

| 분류 | 메트릭 명칭 (Full Name) | 핵심 측정 대상 | 주요 산식 및 파라미터 | 정량적 판단 기준 (Threshold) |
|:---|:---|:---|:---|:---|
| **절차적** | **McCabe Cyclomatic Complexity** | 제어 흐름의 분기 수 | $V(G) = E - N + 2P$<br>($E$: 화살표, $N$: 노드, $P$: 연결 요소) | **1~10**: 안전<br>**11~20**: 위험<br>**21+**: 리팩토링 필수 |
| **어휘적** | **Halstead Length & Volume** | 연산자/피연산자의 빈도 | $V = (N_1 + N_2) \times \log_2(n_1 + n_2)$<br>($N$: 총 수, $n$: 고유 수) | 난이도(Difficulty)와 노력(Effort) 산출<br>Volume이 클수록 이해도 저하 |
| **OOP 구조** | **CBO (Coupling Between Objects)** | 클래스 간 결합도 | A 클래스가 다른 클래스의 메서드/속성을 사용하는 횟수 | **0~3**: 낮음 (좋음)<br>**7+**: 높음 (나쁨, 변경 파급 높음) |

#### 2. McCabe 제어 흐름 그래프 (Control Flow Graph) 구조
소스 코드의 실행 경로를 노드(Node)와 에지(Edge)로 모델링하여 복잡도를 시각화합니다.

```ascii
      [Start]
        │
        ▼
   (Node A) ──────────────┐
        │                  │
        ▼ (if statement)   │
    ┌─────────┐            │
    │  Edge   │            │
    └─────────┘            │
   ▲         ▲            │
   │         │ (Loop)     │ (Edge: 화살표의 개수)
   ▼         │            │
 (Node B)    │            │
   │         │            │
   └─────────┘            │
        │                  │
        ▼                  │
   [End Node] ◀────────────┘

   [분석 해설]
   1. V(G) = E - N + 2*P (P는 연결된 그래프 수, 보통 1)
   2. 이는 '경로(Path)의 독립성'을 의미하며, 기본 경로 테스트(Base Path Testing)를 설계하는 데 필수적인 개수임.
```

#### 3. 심층 동작 원리 및 수식
**[McCabe의 순환 복잡도 (Cyclomatic Complexity)]**
수식 $V(G) = \pi + 1$ (여기서 $\pi$는 조건문(판단 노드)의 개수)을 주로 사용합니다. 이는 테스트 케이스(Test Case)의 최소 개수를 결정하는 지표가 됩니다.

**[Halstead의 소프트웨어 과학 (Software Science)]**
코드를 텍스트의 집합으로 보고 정보량을 계산합니다.
- **Program Length ($N$)**: 전체 연산자($N_1$) + 전체 피연산자($N_2$)
- **Program Vocabulary ($n$)**: 고유 연산자($n_1$) + 고유 피연산자($n_2$)
- **Volume ($V$)**: $N \times \log_2 n$ (비트 단위의 프로그램 양)
- **Difficulty ($D$)**: $n_1 / 2 \times N_2 / n_2$ (코드를 작성하기 얼마나 어려운가)
- **Effort ($E$)**: $D \times V$ (프로그램을 구현하는 데 드는 정신적 노력)
> 실무에서는 **Volume 지표**가 일정 수준(예: 함수당 1000 이상)을 넘으면 모듈 분할(Split)을 권장합니다.

```python
# [Python 예시: McCabe Complexity Check]
# 함수 내부의 분기문(if, elif, for, while) 개수 + 1

def calculate_grade(score, extra_credit):
    # 1. 시작
    base = "F"
    
    # 2. if문 (Predicate Node 1)
    if score > 90:
        base = "A"
    # 3. elif문 (Predicate Node 2)
    elif score > 80:
        base = "B"
    
    # 4. 중첩 if문 (Predicate Node 3)
    if extra_credit: 
        base = "+" + base # 복잡도 상승
        
    return base

# V(G) = 3 (분기점) + 1 = 4
# 의미: 이 함수를 완전히 테스트하려면 최소 4가지 경로가 필요함.
```

**[CK 메트릭스 (Chidamber-Kemerer Metrics)]**
OOP(Object-Oriented Programming)의 품질을 좌우하는 6가지 지표입니다.
1.  **WMC (Weighted Methods per Class)**: 메서드의 복잡도 합. 높을수록 클래스가 너무 많은 역할을 함(God Object anti-pattern).
2.  **DIT (Depth of Inheritance Tree)**: 상속 트리의 깊이. 깊을수록 재사용성은 높으나, 이해도가 떨어지고 하위 클래스의 복잡도가 증폭됨.
3.  **NOC (Number of Children)**: 자식 클래스의 수. 너무 많으면 추상화가 제대로 안 되었을 수 있음.
4.  **CBO (Coupling Between Objects)**: **가장 중요한 지표**. 다른 클래스와 메시지를 주고받는 횟수. 결합도가 높으면 재사용성이 급격히 감소함.
5.  **RFC (Response For a Class)**: 클래스가 응답할 수 있는 메서드의 총합(상속받은 포함). 높을수록 테스트가 어려움.
6.  **LCOM (Lack of Cohesion of Methods)**: 메서드 간의 응집도 부족 정도. 인스턴스 변수를 공유하지 않는 메서드 쌍의 수.

📢 **섹션 요약 비유**: McCabe는 도시의 '교차로 갯수'로 복잡함을 재고, Halstead는 도로에 쓰인 '표지판과 신호등의 밀도'로 재며, CK는 건물들 사이의 '연결 다리 얽힘 상태'를 재어, 도시 전체의 혼잡도(시스템 복잡성)를 진단하는 종합 교통 분석 시스템과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

각 메트릭스는 서로 다른 관점을 제공하며, 이를 통합하여 시스템의 건전성을 판단해야 합니다.

#### 1. 심층 기술 비교: McCabe vs Halstead

| 비교 항목 | McCabe (Structural) | Halstead (Lexical) |
|:---|:---|:---|
| **접근 방식** | 그래프 이론(Graph Theory) 기반, 제어 흐름 중심 | 정보 이론(Information Theory) 기반, 토큰(Token) 중심 |
| **측정 단위** | 분기(Branch)의 개수 | 연산자/피연산자의 빈도와 분산 |
| **주요 용도** | **테스트 커버리지** 최소 기준 설정, 화이트 박스 테스트 경로 선정 | **유지보수 비용** 예측, 프로그램 난이도(수행 시간, 버그 수) 추정 |
| **장점** | 분기 에러(Bug)가 발생하기 쉬운 지점을 정확히 찾아냄 | 코드의 "정신적 복잡도"를 계량화하여 개발자의 인지 부하를 예측 가능 |
| **단점** | 단순 반복문(Loop)이나 데이터 구조의 복잡성은 반영 못 함 | 단순 반복되는 코드도 복잡하게 계산될 수 있음 (공통 로직 처리 시) |

#### 2. 과목 융합 관점
- **[SW 공학 + 네트워크]**: 대규모 분산 시스템(MSA)에서는 **CBO(Coupling Between Objects)**가 네트워크 지연(Latency)과 직결됩니다. 서비스 간 결합도가 높으면 API 호출이 빈번해져 네트워크 병목을 유발합니다.
- **[SW 공학 + 보안]**: 복잡도는 **보안 취약점(Vulnerability)**과 비례합니다. McCabe 복잡도가 높은 함수는 보통 입력 검증(Input Validation)이 누락되거나 예외 처리가 불완전할 확률이 높습니다. OWASP Top 10 공격들은 종종 복잡한 로직의 구석진 곳에서 발생합니다.
- **[SW 공학 + 인공지능]**: 최근 AI 모델(Like GPT)이 코드를 생성할 때, **Halstead Volume** 지표를 활용하여 생성된 코드의 가독성을 모니터링하는 연구가 진행되고 있습니다.

📢 **섹션 요약 비유**: 의사가 환자를 진단할 때 혈압 검사(McCabe: 흐름 압력)와 혈액 검사(Halstead: 구성 성분)를 병행하여 종합적인 건강 상태를 판단하는 것과 같습니다. 하나만 보면 놓치는 병(버그)이 있기 때문입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

복잡도 메트릭을 단순한 보고서용 숫자로 끝내지 않고, 실제 개발 프로세스 개선(Improve Process)에 활용하는 전략이 필요합니다.

#### 1. 실무 시나리오: 레거시 시스템 리팩토링
- **문제 상황**: 10년 된 결제 모듈의 `PaymentService.process()` 함수가 2,000줄이 넘고, 수정 시마다 사이드 이펙트(Side Effect)가 발생함. McCabe 지표가 65, Halstead Volume이 15,000을 기록함.
- **의사결정 과정**:
    1.  **정적 분석(Static Analysis)** 실행으로 복잡도 핫스팟(Hot Spot) 지도 생성.
    2.  **McCabe 20 이상**인 로직을 별도의 함수로 추출(Extract Method) 수행.
    3.  **CBO(결합도)**가 높은 로직을 인터페이스(Interface)로 분리하여 의존성 주입(DI) 패턴 적용.
    4.  **리팩토링 후** 재측정하여 복잡도가 15 미만으로 낮아질 때까지 반복.

#### 2. 도입 체크리스트
기술적/운영적 관점에서 메트릭스 도입 시 확인해야 할 사항입니다.

|