---
title: "Causal Inference Instrumental Counterfactual"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 688
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Pearl의 인과 사다리(Ladder of Causation) 3계층 — 관측(Association, P(Y|X)), 개입(Intervention, P(Y|do(X))), 반사실(Counterfactual, P(Y_x|X',Y')) — 중 반사실 층에 도달하기 위해 **도구변수(IV)**를 통해 미관측 교란변수(Unobserved Confounder, U) 하에서 일치성(Consistency)을 갖춘 처치효과(ATE/LATE)를 도출하는 인과추론의 정점 프레임워크.
> 2. **가치**: RCT가 불가능한 관측 데이터(검색엔진 로깅, 추천 클릭, 의료 EHR)에서도 **2SLS(2단계 최소자승법)**, GMM, LATE(Local Average Treatment Effect) 추정을 통해 처치효과 β를 일치 추정 가능. A/B테스트의 외적타당도 부재 시나리오(네트워크 효과, carry-over effect)에서 정책결정의 인과적 근거를 제공하여 의사결정 신뢰도 30~50% 향상.
> 3. **판단 포인트**: IV의 3대 가정 — (1) 관련성(Relevance): Cov(Z,X)≠0, (2) 배제제약(Exclusion Restriction): Z->Y 직접경로 차단, (3) 교환성(Exchangeability/Independence): Z ⊥ U — 을 통계적 검정(Sargan-Hansen J-test, F-stat≥10의 weak IV 진단)으로 검증할 수 있는지, 그리고 처치 이질성(Heterogeneous Treatment Effect) 하에서 LATE를 ATE로 일반화할 수 있는지가 핵심 트레이드오프.

---

## Ⅰ. 개요 및 필요성

관측 데이터에서 "X가 Y를 야기하는가?"라는 인과적 질문은 데이터 과학·IT 시스템 운영의 본질적 과제다. 전통적 머신러닝은 P(Y|X) 형태의 **조건부 확률(Association)** 만 학습하므로, "이 사용자에게 신규 UI를 적용했다면 전환율은?"과 같은 개입(do) 및 반사실(Counterfactual) 질문에는 구조적으로 답할 수 없다.

예를 들어, 전자상거래 플랫폼에서 "추천 알고리즘 A가 매출 Y를 증가시켰는가?"를 분석할 때, **고매출 사용자**가 **자발적으로 추천 A를 더 많이 클릭**했다면 단순 회귀분석은 선택편향(Selection Bias)을 유발한다. 이때 도구변수 Z(예: 무작위 추천 슬롯 위치, 가격 프로모션 쿠폰 무작위 배정)를 활용하면, Z는 X(추천 클릭)에 영향을 주지만 Y(매출)에는 X를 통해서만 영향을 주는 경로를 구성하여 U(사용자 선호도)의 교란효과를 제거할 수 있다.

**Old Paradigm vs New Paradigm**:
- Old: A/B 테스트만으로 인과효과 검증 -> 비용·윤리·네트워크 효과로 불가한 경우 다수
- New: 인과 그래프(DAG) + do-calculus + IV + 반사실 추정으로 **비실험 데이터에서도 인과효과** 정량화

```text
[인과 사다리 - Pearl's Ladder of Causation]

   +---------------------------------------------+
   |  Level 3: Counterfactual  P(Y_x | X', Y')   |  <- "만약 X였다면?"
   |       ^                                     |
   |       | do-calculus, Structural Causal Model|
   |       |                                     |
   |  Level 2: Intervention   P(Y | do(X))       |  <- "X를 적용한다면?"
   |       ^                                     |
   |       | Randomized Controlled Trial         |
   |       |                                     |
   |  Level 1: Association    P(Y | X)           |  <- "X일 때 Y는?"
   |       ^                                     |
   |       | Observational Data, ML/DL           |
   |       |                                     |
   |  Level 0: Fact           (X, Y) data        |
   +---------------------------------------------+

  [도구변수가 필요한 상황 - 전형적 DAG]

       Z (도구변수/IV)         U (미관측 교란변수)
        |                       |  +----------+
        |                       |  | (사용자   |
        v                       v  |  선호도,  |
       X (처치) -------------► Y  |  건강,    |
       (추천A클릭)     (매출/효과) |  동기 등) |
                                 |  +----------+
                                 |
        Z ⊥ U (독립)  ◄----  도구변수 핵심 가정
        Z -> X  (관련성) ◄--  강도 검증 필요 (F > 10)
        Z ↛ Y  (배제제약) ◄--  이론적 정당화 필요
```

- **📢 섹션 요약 비유**: 의사가 신약의 효과를 알아보고 싶을 때, 환자 자발적 복용은 병의 중증도와 묶여 있어(교란) 단순 비교가 불가합니다. 여기서 **추첨제 복약 알림 문자**(도구변수 Z)를 보내면, Z는 무작위이므로 병의 중증도(U)와 무관하면서 복약(X)을 유도하고, 그 결과 Y(치료효과)만 반영하게 됩니다 — 마치 바람(Z)이 나뭇잎(X)을 흔들어 결과를 보게 하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 반사실 분석(Counterfactual Analysis)의 수학적 토대

**Rubin Causal Model (RCM, Potential Outcomes Framework)**:
- 개체 i에 대해 두 잠재적 결과 Y_i(0), Y_i(1) 정의
- 개별 처치효과(ITE): τ_i = Y_i(1) − Y_i(0)
- **인과추론의 근본 문제(Fundamental Problem of Causal Inference)**: Y_i(0)와 Y_i(1)를 **동시에** 관측 불가
- ATE: E[Y(1)−Y(0)], ATT: E[Y(1)−Y(0)|X=1], ATU: E[Y(1)−Y(0)|X=0]

**Pearl의 Structural Causal Model (SCM)**:
- 외생변수 U, 내생변수 V, 구조방정식 f_i: V_i = f_i(pa_i, U_i)
- do-연산자: 그래프에서 X로 들어오는 화살표를 제거하고 X에 상수값 강제
- **do-calculus 3규칙**:
  1. Rule 1 (Insertion/Deletion of observations): P(y|do(x),z,w) = P(y|do(x),w) if (Y ⊥ Z | X,W) in G_X̄
  2. Rule 2 (Action/observation exchange): P(y|do(x),do(z),w) = P(y|do(x),z,w) if (Y ⊥ Z | X,Z,W) in G_X̄Z̄
  3. Rule 3 (Insertion/Deletion of actions): P(y|do(x),do(z),w) = P(y|do(x),w) if (Y ⊥ Z | X,W) in G_X̄Z(W)

### 2. 도구변수(IV) 메커니즘

도구변수 Z는 다음 3가지를 만족해야 한다:
1. **관련성(Relevance)**: Cov(Z,X) ≠ 0 -> 1단계 회귀의 F-통계량 > 10 (Staiger-Stock 규칙)
2. **독립성(Independence)**: Z ⊥ U -> 무작위배정, 자연실험, 정책 변화
3. **배제제약(Exclusion Restriction)**: Z -> Y 직접 경로 부재 (Y의 구조방정식에 Z 미포함)

**2단계 최소자승법(2SLS) 추정**:

1단계 (First Stage): X = π₀ + π₁·Z + v (π₁ ≠ 0 검증)
2단계 (Second Stage): Y = α + β·X̂ + ε (X̂는 1단계 예측치)

β_IV = Cov(Z,Y) / Cov(Z,X) (Wald Estimator, 단일 IV의 경우)

**LATE (Local Average Treatment Effect) — Imbens & Angrist (1994)**:
도구변수 Z가 이질적 처치효과 하에서 **준수자(Compliers)** 집단만의 평균 처치효과를 식별한다.

LATE = E[Y(1) − Y(0) | Complier] = (E[Y|Z=1] − E[Y|Z=0]) / (E[X|Z=1] − E[X|Z=0])

```text
[IV 추정 파이프라인 아키텍처]

   +--------------------------------------------------+
   | 1. DAG 정의 단계 (Causal Model Specification)   |
   |    - 도메인 지식을 통한 변수 관계 명세           |
   |    - 식별성(Identifiability) 분석: ID 알고리즘  |
   |    - 후门경로(Backdoor Paths) 탐색               |
   +----------------+---------------------------------+
                    v
   +--------------------------------------------------+
   | 2. IV 후보 선정 및 검증                          |
   |    - 관련성: 1st-stage F > 10 (weak IV 검정)    |
   |    - 배제제약: 도메인 논변 + Sensitivity 분석    |
   |    - 독립성: Placebo test, Balance test          |
   +----------------+---------------------------------+
                    v
   +--------------------------------------------------+
   | 3. 추정 단계                                     |
   |    - 2SLS / GMM (Hansen J-test)                 |
   |    - LATE 추정 (Imbens-Rubin 분포)              |
   |    - Doubly Robust IV (IVEWS, TSR)              |
   +----------------+---------------------------------+
                    v
   +--------------------------------------------------+
   | 4. 반사실 시뮬레이션 및 정책결정                  |
   |    - Individual Treatment Effect (ITE) 추정     |
   |    - Causal Forest (Wager-Athey 2018)            |
   |    - do(X=x) 하에서 Y 분포 예측                 |
   +--------------------------------------------------+

   [LATE의 4집단 분해 - Always-Taker / Never-Taker / Complier / Defier]

   +--------------+----------+----------+
   |  집단        | Z=0      | Z=1      | 처치효과
   +--------------+----------+----------+
   | Complier     | X=0      | X=1      | τ_C  <- IV가 식별
   | Always-Taker | X=1      | X=1      | -
   | Never-Taker  | X=0      | X=0      | -
   | Defier       | X=1      | X=0      | -τ_D
   +--------------+----------+----------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Causal DAG** | 인과 구조 시각화 및 식별성 분석 | 노드=변수, 방향성 엣지=인과관계, `do-calculus`로 개입 효과 계산, `backdoor criterion`/`front-door criterion` 적용 |
| **도구변수(IV)** | 미관측 교란의 효과 차단 | 1st-stage F≥10 강도 검증, Sargan-Hansen J-test로 과식별 제약 검정, 2SLS로 β_IV = Cov(Z,Y)/Cov(Z,X) 추정 |
| **반사실 추정기** | 잠재적 결과 Y(0), Y(1) 분포 추정 | T-learner/S-learner/X-learner, Causal Forest (GRF), TARNet, CFRNet (Balanced representation), Dragonnet |
| **Sensitivity Analyzer** | 미관측 교란에 대한 강건성 평가 | E-value (Vanderweele), Rosenbaum bounds, Oster (2019) δ bound, Cinelli & Hazlett (2020) Robustness Value |

### 3. 핵심 알고리즘 및 추정량

**Heckman 2단계 (Heckman 1979)** vs **IV 2SLS**: Heckman은 선택편향 보정, 2SLS는 내생성 보정.

**GMM (Generalized Method of Moments)**: E[Z·ε] = 0 모멘트 조건 최적화, 헤테로스케asticity-robust SE 가능 (Hansen J 통계량).

**Anderson-Rubin Test**: 약도구(Weak IV) 하에서도 유효한 신뢰구간 (C.I. 형태), F<10 상황에서도 강건.

**Exact IV (검정적 역전)**: LATE의 점근 정규성이 아닌 정확한 유한표본 신뢰구간 제공 (Imbens-Rubin 1997).

**Causal Forest (Wager-Athy 2018)**: 이질적 처치효과(CATE) 추정을 위한 알고리즘 — Honest splitting으로 과적합 방지, `best_linear_projection`으로 CATE 해석.

- **📢 섹션 요약 비유**: 도구변수는 **"세컨드 우산"**과 같습니다. 메인 우산(처치 X)이 비(결과 Y)를 막지만 바람(교란 U)이 우산을 흔들어 효과가 불확실할 때, 옆에서 두 번째 우산(IV Z)을 들고 바람의 방향을 정해주면, 메인 우산의 실제 차단 능력을 정확히 측정할 수 있습니다.

---

## Ⅲ. 비교 및 연결

### 1. 인과추론 방법론 비교

| 구분 | **RCT (무작위배정시험)** | **IV (도구변수)** | **PSM (성향점수매칭)** | **DiD (차이중차이)** | **RDD (회귀불연속)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **식별 가정** | 무작위배정 | 3대 IV 가정 | 조건부 독립성 (Ignorability) | 평행추세 (Parallel Trends) | 연속성 + 조작불가 |
| **추정 대상** | ATE | LATE (준수자 한정) | ATT | ATT (시간불변) | 국소 처치효과 (cutoff 부근) |
| **내생성 대응** | 본질적으로 해결 | 미관측 교란 제거 | 관측 교란 통제 | 시간불변 교란 통제 | cutoff 부근 교란 통제 |
| **데이터 요건** | 가장 까다로움 (실험) | 자연실험/정책 필요 | 관측 confounder 다수 필요 | 패널 데이터 (2기간+) | cutoff 변수 필요 |
| **표본 크기** | 크게 필요 | 보통 | 크게 필요 | 보통