+++
title = "703. 백파이어링 FP LOC 역산"
date = "2026-03-15"
weight = 703
[extra]
categories = ["Software Engineering"]
tags = ["Cost Estimation", "Function Point", "LOC", "Backfiring", "Software Metrics", "Estimation Technique"]
+++

# 703. 백파이어링 FP LOC 역산

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 공학의 표준 규모 산정 기법인 **기능점수(Function Point, FP)**와 물리적 코드량인 **LOC (Lines of Code)** 사이의 상관관계를 이용하여, 기 구축된 소스코드로부터 역추정하여 FP를 도출하는 간이 산정 기법이다.
> 2. **가치**: 소프트웨어 개발 비용 산정의 '골드 스탠다드'인 FP 산정의 어려움을 LOC의 객관적 측정 가능성으로 보완하여, 문서가 부족한 레거시 시스템의 현업 실무(Real-world) 규모 파악과 생산성(Benchmarking) 분석을 신속하게 수행한다.
> 3. **융합**: 소프트웨어 재공학(Re-engineering) 및 프로젝트 후속 산정 시, 코딩 표준과 언어별 추상화 수준(Abstraction Level)을 고려한 통계적 회귀 분석(Regression Analysis) 기법과 결합하여 정밀도를 높인다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**백파이어링(Backfiring)**은 소프트웨어 공학에서 사용하는 규모 산정 기법의 하나로, 시스템의 논리적 요구사항을 분석하여 기능점수를 산출하는 '정방향' 프로세스와 반대로, 이미 개발이 완료되어 존재하는 **물리적 소스 코드(SLOC, Source Lines of Code)**를 측정한 후, 이를 역산(Back-calculation)하여 기능점수(FP)를 추정하는 방식입니다. 이는 일종의 '경험적 계수 모델(Empirical Coefficient Model)'에 속하며, 언어별 생산성 지수를 활용합니다.

### 2. 💡 핵심 비유: 건물의 층고를 이용한 층수 추정
```text
      [ 전문가의 정밀 설계 (FP 산정) ]              [ 일반인의 판단 (백파이어링) ]
      
  🔍 내부 구조를 모두 파악                       🏗️ 외부 높이(LOC)만 측정
  ────────────────────                          ────────────────────
  1. 방 개수 파악 (입력/출력/조회)                1. 줄자로 높이 측정
  2. 복잡도 계산 (파일/논리)                      2. "이 건물은 층고가 평균 3m
  3. 정확한 기능점수(10FP) 도출                      이니까 30m 높이면 10층이겠다"
  ↓
   정확함 ▶  However, 매우 비싸고 느림                  빠름 ▶  However, 오차 범위 존재
```

### 3. 등장 배경 및 필요성
① **정규 FP 산정의 한계**: 정규 기능점수(IFPUG) 산정은 전문가의 자격이 필요하고, 상세 설계서 및 요구사항 명세서를 완벽하게 분석해야 하므로 시간과 비용이 많이 소요됨.
② **레거시 시스템의 문서 부재**: 오래된 시스템은 설계서가 유실되었거나 현재 버전과 다른 경우가 빈번함. 하지만 소스코드는 존재함.
③ **빠른 규모 추정의 요구**: 유지보수 재계약, 타 시스템과의 생산성 비교(Benchmarking), 초기 타당성 조사 등에서 "정확성보다는 속도"가 요구되는 상황에서 등장.

### 📢 섹션 요약 비유
> 마치 복잡한 설계도 없이 오래된 성곽의 규모를 알기 위해, 성벽의 전체 둘레(LOC)를 측정한 후 "이 시대의 건축 양식(언어)으로는 보통 100m당 망대 1개(1FP)를 짓는다"는 경험식을 적용하여 군사력을 추정하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 및 파라미터
백파이어링은 수학적으로 **`FP = Total LOC / Table Value`** 형태를 가지며, 다음과 같은 세부 파라미터로 구성됩니다.

| 구성 요소 (Component) | 역할 (Role) | 상세 내역 (Detail) | 비고 (Note) |
|:---:|:---|:---|:---|
| **LOC (SLOC)** | **Input (입력값)** | 실제 소스 코드의 물리적 줄 수(주석/공백 제외) | `CLOC` 등의 도구로 자동 측정 |
| **Language Level** | **Divisor (분모)** | 1 FP를 구현하는 데 필요한 평균 LOC 수 | 언어별 추상화 수준 반영 |
| **Table Value** | **Coeff (계수)** | Jones(1991), Capers Jones 등의 통계 데이터 | 예: Java≈55, C≈128 |
| **VAF (Value Adjustment Factor)** | **Refiner (수정계수)** | 비기능적 요구사항(성능, 신뢰성 등)을 고려한 보정치 | ±0.75~1.25 배율 적용 |

### 2. ASCII 다이어그램: 백파이어링 데이터 흐름 및 변환 프로세스
이 다이어그램은 소스 코드가 기능점수로 변환되는 알고리즘적 절차를 도식화한 것입니다.

```text
[ Phase 1: Data Collection ]       [ Phase 2: Calculation ]          [ Phase 3: Verification ]
+------------------------+         +---------------------------+       +--------------------------+
|  Source Repository     |         |  Conversion Engine        |       |  Expert Validation       |
|  (Legacy System)       |         |  (Math Model)             |       |  (QE / Architect)        |
+------------------------+         +---------------------------+       +--------------------------+
|  - Java Files          |         |  Formula:                 |       |  1. Complex Adjust       |
|  - SQL Scripts         |   LOC   |  FP = LOC ----------------> |  FP   |  2. Rule of Thumb Check |
|  - Config Files        | ----->  |       Table Factor(Lang)  | ----> |  3. Historical Compare   |
+------------------------+         +---------------------------+       +--------------------------+
        |                                ^                             |
        |                                |                             |
        v                                |                             v
[Tooling: CLOC, SonarQube]    [Lookup: Jones Table]           [Output: Est. Size Report]
(Automated Counting)          (Lang Specific Coeff)           (Cost Basis)
```

* **[도해 설명]**
    1.  **Phase 1 (데이터 수집)**: `CLOC (Count Lines of Code)` 도구 등을 사용하여 주석(Comment)과 공백 라인(Blank Line)을 제외한 순수 코드 라인인 **SLOC (Source Lines of Code)**를 수집합니다. 물리적 LOC를 그대로 사용할 경우 오차가 커지므로 논리적 LOC 표준화가 선행되어야 합니다.
    2.  **Phase 2 (변환 엔진)**: 수집된 LOC를 언어별 계수(Table Value)로 나눕니다. 여기서 언어별 계수는 '언어의 레벨(Language Level)'을 의미하며, 낮은 수준의 언어(어셈블리어 등)일수록 1 FP를 구현하는 데 더 많은 코드가 필요하므로 분모가 커져 결과적으로 FP가 작게 산출됩니다.
    3.  **Phase 3 (검증 및 보정)**: 산출된 FP는 아키텍트의 전문적 판단에 의해 보정됩니다. 특정 모듈이 알고리즘 복잡도가 매우 높거나(Abnormal Logic), 라이브러리 재사용률이 극단적으로 높은 경우에는 기계적 계산 결과에 가중치를 조정합니다.

### 3. 핵심 알고리즘 및 실무 코드 (Python Style Pseudo-code)
백파이어링은 복잡한 수식이 아니지만, **언어별 가중치 처리**와 **보정 계수 적용**이 핵심입니다.

```python
# [Pseudo-code] Backfiring Logic Implementation
# 언어별 1 FP당 평균 LOC (Capers Jones Table 일부 발췌)
LANG_TABLE = {
    'Assembler': 320,   # 저수준 언어: 많은 코드가 필요함
    'C': 128,
    'C++': 53,
    'Java': 53,
    'Python': 40,       # 고수준 언어: 적은 코드로 많은 기능
    'SQL': 21
}

def calculate_fp(total_loc, language, complexity_factor=1.0):
    """
    LOC를 기반으로 기능점수(FP)를 역산하는 함수
    :param total_loc: 총 소스 코드 라인 수 (SLOC)
    :param language: 프로그래밍 언어 명
    :param complexity_factor: 프로젝트 복잡도 보정 계수 (0.8 ~ 1.25)
    :return: 추정 기능점수 (Estimated FP)
    """
    if language not in LANG_TABLE:
        raise ValueError("Unsupported language for backfiring table")

    # 1. 기본 역산 공식 (FP = LOC / Ratio)
    base_fp = total_loc / LANG_TABLE[language]
    
    # 2. 복잡도 보정 (VAF 혹은 전문가 판단 반영)
    # ex) 복잡한 알고리즘 연산이 많으면 가중치 증가
    adjusted_fp = base_fp * complexity_factor
    
    return round(adjusted_fp, 2)

# Example Case: 100,000 Lines of Java Project
est_fp = calculate_fp(100000, 'Java', complexity_factor=1.1)
# Result: approx 2075 FP
```

### 📢 섹션 요약 비유
> 마치 금광에서 원석을 캐내면(NOLOC), 전문가가 이것의 순도를 검사하기 위해 비중(Specific Gravity)을 측정하는 것과 같습니다. 같은 무게라도 금(고수준 언어)과 구리(저수준 언어)는 부피(LOC)가 다르기 때문에, 이 비율(Table Value)을 알면 무게(FP)를 역산해낼 수 있는 원리입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 정규 FP 산정 vs 백파이어링 (정량적·구조적 비교)

| 비교 항목 | 정규 기능점수 (IFPUG) | 백파이어링 (Backfiring) | Best Practice |
|:---|:---|:---|:---|
| **접근 방향** | Forward (Requirements $\to$ FP) | **Reverse (LOC $\to$ FP)** | 초기: FP $\leftrightarrow$ 유지보수: 백파이어링 |
| **데이터 소스** | 설계서, 유스케이스, 사용자 인터뷰 | **소스 코드(SVN/Git)** | 문서가 최신이라면 FP 우선 |
| **언어 의존성** | 없음 (Technology Independent) | **높음 (Language Dependent)** | 하이브리드 방식 권장 |
| **정확도(Accuracy)** | ± 10% (High) | ± 30~50% (Medium/Low) | 백파이어링은 추정용으로만 사용 |
| **측정 비용(Cost)** | High (전문가 인건비) | **Low (자동화 도구 활용)** | 예산 제약 시 대안으로 활용 |
| **주요 사용자** | 고객사, 계약 담당자 | PM, 아키텍트, 품질 관리자 | 내부 의사결정 지원용 |

### 2. 다른 분야와의 융합: COCOMO 모델과의 시너지
백파이어링은 단순히 크기만 재는 것이 아니라, 소프트웨어 공학의 다른 비용 산정 모델인 **COCOMO (Constructive Cost Model)**과 연결될 때 강력한 위력을 발휘합니다.

$$ \text{Effort (Person-Month)} = C \times (\text{E-KLOC})^E \times \text{EAF} $$

*   **연결 점**: 백파이어링을 통해 LOC를 FP로 바꾼 뒤, 다시 이를 KLOC(Kilo Lines of Code)로 환산하면, COCOMO 모델의 입력 변수로 사용할 수 있습니다.
*   **융합 효과**: 문서가 없는 레거시 시스템의 LOC를 백파이어링으로 환산하여 FP 규모를 파악한 후, 향후 Java로 재개발(Re-engineering) 시 얼마나 많은 인력(MM)이 필요한지 **다른 언어로의 이기종 변환 비용을 예측**할 수 있습니다.

### 📢 섹션 요약 비유
> GPS(정규 FP)는 위성(요구사항)을 보며 정확한 위치를 알려주지만, 터널(코드만 있는 상황) 안에 들어가면 신호가 끅깁니다. 이때 자이로스코프(백파이어링)가 마지막 확인된 속도와 방향(코드량)을 기반으로 현재 위치를 추정하는 것처럼, 두 기법은 상호 보완적으로 사용됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 레거시 시스템의 유지보수 단가 산정

*   **문제 상황 (Problem)**:
    금융권 핵심 레거시 시스템(약 15년 전 구축)의 유지보수 계약을 갱신해야 한다. 그러나 최초 요구사항 정의서(SRD)나 설계서(SDD)가 존재하지 않아 기능점수(FP)를 알 수 없어, "고객사는 너무 비싸다", "개발사는 인건비가 부족하다"는 싸움이 반복됨.
*   **백파이어링 적용 (Action)**:
    1.  현재 운영 중인 소스 코드(Spring Framework, Java, SQL 포함)를 `CLOC` 도구로 분석.
    2.  **결과**: 총 350,000 Lines. (Java 70%, SQL 30%)
    3.  **환산**:
        *   Java(53배): 245,000 / 53 ≈ 4,622 FP
        *   SQL(21배): 105,000 / 21 ≈ 5,000 FP
        *   **Total Est. FP**: 약 9,600 FP (대형 시스템급)
    4.  **결과 제시**: 이 시스템은 약 9,600 FP 규모이며, 업계 평균 생산성(8 FP/Man-Month)을 고려할 때 유지보수 인력은 최소 10명 이상이 필요함을 객관적으로 입증.
*   **결과 (Outcome)**:
    근거 없는 협상이 아닌, 코드 기반의 수치화된 자료를 통해 고객사를 설득