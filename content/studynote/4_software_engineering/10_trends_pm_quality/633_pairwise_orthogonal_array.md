+++
title = "633. 페어와이즈 (Pairwise) 직교 배열 (Orthogonal Array)"
date = "2026-03-15"
weight = 633
[extra]
categories = ["Software Engineering"]
tags = ["Testing", "Black Box Testing", "Pairwise", "Orthogonal Array", "Combinatorial Testing"]
+++

# 633. 페어와이즈 (Pairwise) 직교 배열 (Orthogonal Array)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 결함의 다수가 단일 변수가 아닌 **2개 변수(Parameter) 간의 상호작용(Interaction)**에서 발생한다는 통계적 근거에 기반한 **조합 최적화(Combinatorial Optimization) 테스트 기법**이다.
> 2. **가치**: 모든 조합을 테스트하는 **Full Cartesian Product (완전 직적)** 방식의 기하급수적 비용 증가 문제를 해결하여, **Linear(선형) 또는 Logarithmic(로그) 수준**으로 테스트 케이스를 축소하면서도 핵심 결함을 검출하는 고효율 전략을 제공한다.
> 3. **융합**: 수학의 **OA (Orthogonal Array, 직교 배열)** 이론과 계산 과학의 **t-way covering array** 알고리즘을 결합하며, 실무에서는 **PICT (Pairwise Independent Combinatorial Testing)** 도구를 통해 HW/SW 호환성 테스트 및 설정 검증에 필수적으로 활용된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**페어와이즈 테스팅(Pairwise Testing)**, 또는 **All-Pairs Testing**은 시스템의 입력 매개변수들 중 가능한 모든 **2개 요소의 조합(Pair)**이 최소한 한 번씩은 테스트 케이스에 포함되도록 설계하는 **블랙박스 테스트(Black Box Testing)** 기법입니다. 이는 N개의 인자가 있을 때, N-way Interaction(상호작용) 중 가장 결함 발생 확률이 높은 2-way Interaction을 완벽하게 커버하는 데 중점을 둡니다.

#### 2. 💡 비유: 뷔페 음식 조합 테스트
새로운 뷔페 메뉴를 개발했다고 가정해 봅시다. 메인 요리(3종), 음료(3종), 디저트(3종)이 있습니다. 모든 조합($3 \times 3 \times 3 = 27$가지)을 먹어보며 배가 아픈지 확인하는 것은 현실적으로 불가능합니다. 페어와이즈 접근법은 "스테이크+콜라", "스테이크+아이스크림", "파스타+레몬에이드" 처럼 **음식 2가지 조합**이 모두 한 번씩 등장하도록 식단을 짭니다. 이를 통해 27번이 아닌 훨씬 적은 횟수(예: 9회)로도 음식 궁합에서 오는 배탈 원인을 대부분 찾아낼 수 있습니다.

#### 3. 등장 배경: 조합의 폭발(Combinatorial Explosion)
소프트웨어 설정(Config)의 복잡도가 높아짐에 따라 **Full Combination Test**는 비용 관리 측면에서 불가능해졌습니다.
- **① 기존 한계**: 10개의 옵션(Select Box)이 각각 3개의 값을 가진다면, $3^{10} = 59,049$개의 테스트가 필요함. (실행 불가능)
- **② 혁신적 패러다임**: 1970~80년대 통계학자(등)들이 제안한 직교 배열을 소프트웨어 테스트에 도입. "결함의 95% 이상이 2개 이하의 인자 조합에서 발생한다"는 **D.R. Cox의 원리**를 적용.
- **③ 비즈니스 요구**: CI/CD(Continuous Integration/Continuous Deployment) 환경에서 빌드/테스트 시간을 단축시키면서도 릴리스 품질을 보장해야 하는 절실한 요구가 대두됨.

#### 4. ASCII 다이어그램: 조합 수 증가 시각화

```text
[ 테스트 케이스 수 (N) 추이 ]

Input Factors (k) = 3 (예: OS, Browser, DB)
Levels per Factor (v) = 3

     (A) Full Cartesian Product                     (B) Pairwise (t=2)
  (모든 조합: v^k = 27 cases)                  (필수 쌍만: v^2 ~ O(N log N))
  
  Set 1: (OS1, Br1, DB1) -->                  Set 1: (OS1, Br1, DB1) *
  Set 2: (OS1, Br1, DB2) -->                  Set 2: (OS1, Br2, DB2) *
  Set 3: (OS1, Br1, DB3)        ...           Set 3: (OS2, Br3, DB1) *
  ... (생략: 수십 개의 행)                     ...
  Set 27: (OS3, Br3, DB3)                     Set 9: (OS3, Br3, DB3)  *
  
  [관찰]: Full의 경우 A-B, B-C, A-C의 모든   [관찰]: Pairwise는 모든 '쌍' 관계를
          조합이 중복 포함되어 낭비 심함.      최소한의 행으로 분산 배치함.
          
  Graph: /                                    Graph: _
        /|                                           |
       / |                                  ~O(N)    |
      /  |          (Exponential)                  /__
     /   |_________________________________        /
    /                                          __/
```

#### 5. 해설 (Deep Dive)
위 다이어그램은 입력 변수(요인)의 수가 늘어날 때, 전체 조합(Full) 방식은 지수 함수(Exponential) 형태로 테스트 비용이 폭발하는 반면, 페어와이즈 방식은 로그 선형(Log-Linear) 형태로 증가함을 보여줍니다. 실무적으로는 변수가 15개 이상 넘어가면 Full 테스트는 물리적으로 불가능하며, 페어와이즈는 이러한 **조합의 저주(Curse of Dimensionality)**를 깨는 유일한 대안이 됩니다.

> **📢 섹션 요약 비유**: 페어와이즈는 **"도시의 모든 신호등을 한 번에 다 맞추려 하지 않고, 가장 사고가 많이 나는 교차로(쌍)들의 신호 호환성만 집중적으로 최적화하는 교통 정책"**과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 내부 동작

페어와이즈 테스트를 구성하는 핵심 요소와 역할은 다음과 같습니다.

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 관련 용어 (Term) |
|:---:|:---|:---|:---|
| **Factor (요인)** | 시스템의 입력 변수 | 테스트 대상이 되는 독립적인 설정값 (예: 브라우저 종류) | Parameter, Variable |
| **Level (수준)** | 요인이 가질 수 있는 값 | 각 요인의 구체적인 옵션 (예: Chrome, FF, Safari) | Value, Symbol |
| **Tuple (튜플)** | 조합의 단위 | $t$개의 요인 값으로 구성된 집합 ($t=2$이면 Pair) | Combination, Set |
| **OA Generator** | 배열 생성 엔진 | 수학적 알고리즘을 사용해 중복 없는 배열을 계산하는 코어 로직 | Greedy Algorithm, IPO |
| **Constraints (제약조건)** | 불가능한 조합 필터링 | "iOS에는 IE가 없다"와 같이 논리적으로 불가능한 조합을 배제 | Forbidden Tuple |

#### 2. 직교 배열(Orthogonal Array, OA) 구조
수학적으로 페어와이즈는 **OA (Orthogonal Array)** 표기법으로 설명됩니다. 
- **표기식**: $L_N(S^K)$
  - $L$: 직교 배열
  - $N$: 행(Row)의 수, 즉 필요한 테스트 케이스 수
  - $S$: 각 열(Column)이 가질 수 있는 수준(Level)의 수
  - $K$: 열(Column)의 수, 즉 변수(Factor)의 수

#### 3. ASCII 다이어그램: 직교 배열 $L_9(3^4)$ 구조 예시

다음은 3개의 수준(Level: 0, 1, 2)을 가진 4개의 요인(Factor: A, B, C, D)을 테스트하는 $3^4 = 81$개 조합 중, 단 9개의 테스트 케이스($L_9$)로 모든 쌍(Pair)을 커버하는 직교 배열입니다.

```text
 [ 직교 배열 L_9(3^4) 구조도 ]
 
 +-------+-------+-------+-------+-----+--------------------------+
 | Row#  |  F_A  |  F_B  |  F_C  | F_D |        Covering Pairs    | 
 +-------+-------+-------+-------+-----+--------------------------+
 |   1   |   0   |   0   |   0   |  0  | (A,B),(A,C)...(C,D)      |
 |   2   |   0   |   1   |   1   |  1  | -> All unique pairs      |
 |   3   |   0   |   2   |   2   |  2  |    covered evenly        |
 |   4   |   1   |   0   |   1   |  2  |                          |
 |   5   |   1   |   1   |   2   |  0  |      [Balance Property] |
 |   6   |   1   |   2   |   0   |  1  |   Every pair appears     |
 |   7   |   2   |   0   |   2   |  1  |   exactly once!          |
 |   8   |   2   |   1   |   0   |  2  |                          |
 |   9   |   2   |   2   |   1   |  0  |                          |
 +-------+-------+-------+-------+-----+--------------------------+

 [커버리지 검증 예시: F_A와 F_B의 쌍]
   (0,0), (0,1), (0,2)
   (1,0), (1,1), (1,2)  -> 총 9개 쌍 모두 1회씩 존재 (검증 완료)
   (2,0), (2,1), (2,2)
```

#### 4. 해설 (Deep Dive)
위 다이어그램은 **Orthogonal (직교)**의 성질을 보여줍니다. 임의의 두 열(예: A와 B)을 선택했을 때, 가능한 모든 순서쌍(Ordered Pair)이 동일한 빈도(여기서는 1회)로 나타납니다. 이 성질은 데이터의 편향(Bias)을 제거하여 특정 변수 값이 특정 다른 변수 값과만 결합되는 '찌꺼기 상관관계'를 방지합니다. 이를 통해 우리는 9번의 실험만으로도 81번의 실험에서 얻을 수 있는 2차원 상호작용 정보를 완벽하게 추출할 수 있습니다.

#### 5. 핵심 알고리즘: IPO (In-Parameter-Order) Generalization
실무에서 OA가 존재하지 않는 복잡한 경우(예: 변수마다 Level 수가 다른 Mixed-Level)에는 **IPO** 알고리즘이 주로 사용됩니다.
1. **Horizontal Growth**: 2개의 인자를 선택하여 모든 쌍을 커버하는 초기 행을 생성합니다.
2. **Vertical Extension**: 새로운 인자가 추가되면, 기존 행에 값을 추가하되 아직 커버되지 않은 쌍을 생성하도록 값을 할당합니다.
3. **Uncovered Pair Completion**: 모든 쌍이 커버될 때까지 새로운 행을 추가합니다.

> **📢 섹션 요약 비유**: 페어와이즈의 직교 배열 설계는 **"수만 명의 손님을 초청한 파티에서, 단 9명의 테이블 시트만 배치해도 모든 사람들이 서로 최소 한 번씩은 악수를 하도록 자리를 배치하는 초고난도 좌석 배치 알고리즘"**과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 조합 테스팅 계층 구조

| 구분 | 1-Way (Single Mode) | **2-Way (Pairwise)** | 3-Way / 4-Way | Full Combination |
|:---:|:---:|:---:|:---:|:---:|
| **커버리지 범위** | 단일 변수 결함 | **2개 변수 간 상호작용** | 3~4개 변수 복합 상호작용 | 모든 상호작용 |
| **결함 검출율** | 낮음 (약 30%) | **높음 (약 80~90%)** | 매우 높음 (95%+) | 100% |
| **테스트 케이스 수** | $N \times L$ | **$O(N \log N)$** | $O(N^2 \sim N^3)$ | $L^N$ (폭발) |
| **주요 도구** | 단순 반복문 | **PICT, ACTS** | Jenny, Combinatorial Tool | 불가능 |
| **실무 적용성** | 단순 유효성 검사 | **설정/호환성 테스트** | 핵심 안전/임베디드 시스템 | 연구/단순 시스템 |

#### 2. 타 과목/기술 융합 시너지

- **SW <-> HW (하드웨어 융합)**: **호환성 매트릭스(Compatibility Matrix)** 테스트에 핵심적임.
  - 예: Windows(10/11) x CPU(Intel/AMD) x GPU(Nvidia/ATI) x RAM(8/16/32GB).
  - 페어와이즈를 적용하지 않으면 $2 \times 2 \times 2 \times 3 = 24$회가 필요하지만, 적용 시 약 9~12회로 압축 가능.
  
- **SW <-> AI (머신러닝 융합)**: **하이퍼파라미터 튜닝(Hyperparameter Tuning)**에 활용.
  - 딥러닝 모델 학습 시 Learning Rate, Batch Size, Optimizer 등의 조합을 찾을 때, 모든 조합(Grid Search)을 돌리는 대신 페어와이즈 샘플링을 통해 초기 성능 검증 범위를 좁히는 데 사용.

- **SW <-> Security (보안 융합)**: **Fuzzing (퍼징) 테스트의 입력 생성 최적화**.
  - 무작위 입력(Fuzz)을 생성할 때, 페어와이즈 전략을 적용하여 "시스템이 크래시 내는 주요 파라미터 조합"을 더 빨리 발견할 수 있음.

#### 3. ASCII 다이어그램: 결함 발견율 곡선 (Convergence Rate)

```text
 [ 결함 발견율 vs 상호작용 차수 (t-way) ]
 
      ^
 100%|                                     . . . . . . . . (Full Test)
 Defect|                                 . 
 Detec-|                             . 3-way Interaction
 tion  |                         .  
 Rate  |                     .