+++
title = "678. SPICE 프로세스 역량 평가"
date = "2026-03-15"
weight = 678
[extra]
categories = ["Software Engineering"]
tags = ["Process Improvement", "SPICE", "ISO 15504", "Capability Level", "Software Process"]
+++

# 678. SPICE 프로세스 역량 평가

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 프로세스의 품질과 성숙도를 측정하는 국제 표준 **ISO/IEC 15504**를 의미하며, '무엇을(What)' 하는 프로세스인지와 '얼마나 잘(How)' 하는지를 2차원으로 평가하는 체계이다.
> 2. **가치**: 조직 단위의 역량 뿐만 아니라 개별 프로세스(요구사항 분석, 코딩, 테스트 등)의 역량을 **핀셋으로 진단**할 수 있어 애자일 환경에서의 유연한 프로세스 개선(Roadmap)을 제공한다.
> 3. **융합**: 미국 중심의 **CMMI (Capability Maturity Model Integration)**와 대비되는 유럽 중심의 표준으로, 자동차 산업의 **A-SPICE (Automotive SPICE)** 등 산업별 특화 표준의 모태가 되어 글로벌 공급망(Supply Chain)의 품질 보증 기준으로 작동한다.

---

### Ⅰ. 개요 (Context & Background) - [600자+]

#### 1. 개념 및 정의
**SPICE (Software Process Improvement and Capability dEtermination)**는 소프트웨어 개발 조직의 프로세스 성숙도를 평가하고 개선하기 위한 국제 표준인 **ISO/IEC 15504**의 별칭이다. 이는 단순한 프로세스 준수 여부를 넘어, 프로세스가 조직의 비즈니스 목표를 얼마나 효과적으로 지원하는지를 정량적으로 평가하는 기술적 프레임워크다.

#### 2. 등장 배경 및 철학
1990년대 초반, 소프트웨어 산업의 급성장과 함께 각국마다 상이한 프로세스 평가 모델(미국의 CMM, 영국의 Bootstrap 등)이 난립하여 글로벌 협업 및 조달(Procurement)에 장애가 발생했다. 이를 해결하기 위해 ISO(International Organization for Standardization)와 IEC(International Electrotechnical Commission)가 공동으로 범용적이고 국제적으로 인정받는 표준을 제정했다.

#### 💡 비유: 피아노 학생의 레슨 평가
SPICE는 한 피아노 학생(조직)의 실력을 평가할 때, **'가락기(Gamme)·악상·암보(By heart)'** 등 세부 항목(프로세스 차원)마다 각각 **급수(능력 차원)**를 매기는 것과 같다. "가락기는 5급(완벽)인데 악상은 1급(초보)"이라는 식의 정밀한 진단이 가능하므로, 무엇을 먼저 연습해야 할지 명확히 알 수 있다.

#### 3. 기술적 배경: 2차원 모델의 필요성
기존의 단일 차원 모델(예: CMM Staged Representation)은 조직 전체가 한 단계씩 성장해야 한다는 계단식 구조라는 한계가 있었다. 반면, SPICE는 **'어떤 프로세스를'** 선정하여 **'어느 수준까지'** 평가할지 선택할 수 있는 **연속형(Continuous) 모델**을 채택하여, 특정 영역(예: 테스트)의 역량만 선별적으로 강화하려는 현대적 요구사항에 부합한다.

```text
   [Legacy Model vs SPICE]
   
   ┌──────────┐    ┌──────────────────────────────────────────┐
   │ CMMI     │    │ SPICE (ISO/IEC 15504)                    │
   │ Staged   │    │ (Continuous & Flexible)                  │
   │ (Ladder) │    │                                          │
   ├──────────┤    │                                          │
   │ Level 5  │    │     Process A (Test) ──▶ Level 5         │
   │   ▲      │    │     Process B (Design)▶ Level 3         │
   │ Level 4  │    │     Process C (Config) ─▶ Level 2       │
   │   ▲      │    │                                          │
   │ Level 3  │    │   (개별 프로세스의 독립적 성장 가능)     │
   │   ▲      │    └──────────────────────────────────────────┘
   │ Level 2  │
   │   ▲      │     ▶ 조직 전체가 한꺼번에 레벨업되는 부담 없이
   │ Level 1  │         필요한 부분만 고도화 가능.
   └──────────┘
```

#### 📢 섹션 요약 비유
> "마치 복잡한 자동차의 성능을 테스트할 때, 전체 점수를 매기는 것이 아니라 엔진 출력, 브레이크 성능, 연비 등 항목별로 별도의 등급(A, B, C)을 매겨서 정밀하게 세부 튜닝(Tuning)을 계획하는 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,200자+]

#### 1. SPICE의 2차원 참조 모델 (Two-Dimensional Architecture)
SPICE 평가 모델은 **'프로세스 차원(Process Dimension)'**과 **'능력 차원(Capability Dimension)'**이라는 두 개의 축으로 구성된다. 이 행렬(Matrix) 구조는 IT 아키텍처에서의 **관심사 분리(Separation of Concerns)** 원칙을 적용한 것이다.

| 차원 | 구분 | 설명 | 실무 예시 |
|:---:|:---|:---|:---|
| **수평 축** | **프로세스 차원** | **"무엇을 하는가?"** <br>조직이 수행해야 할 업무 활동의 분류 (카테고리) | 요구사항 분석, 코딩, 테스트, 프로젝트 관리 등 |
| **수직 축** | **능력 차원** | **"얼마나 잘 하는가?"** <br>프로세스가 목표를 달성하는 성숙도 정도 (레벨 0~5) | 계획이 있는가? 조직 차원에서 표준화되었는가? 통제되는가? |

#### 2. 프로세스 카테고리 (Process Categories)
SPICE는 프로세스를 5개의 주요 카테고리로 분류하며, 이는 소프트웨어 생명 주기(SDLC) 전반을 포괄한다.

1.  **CUS (Customer-Supplier)**: 고객과 직접적인 연관이 있는 프로세스 (요구사항 분석, 운영, 제공)
2.  **ENG (Engineering)**: 시스템의 구현과 유지보수를 담당하는 핵심 엔지니어링 프로세스
3.  **SUP (Support)**: 다른 프로세스를 지원하는 활동 (QA, 문서화, 형상 관리)
4.  **MAN (Management)**: 프로젝트 및 조직의 관리 활동
5.  **ORG (Organization)**: 조직의 비즈니스 목표 설정과 프로세스 개선 등 조직 차원의 활동

#### 3. 심층 능력 수준 (Capability Levels 0~5)
능력 차원은 프로세스의 성숙도를 0레벨부터 5레벨까지 정의하며, 각 레벨은 상위 레벨로 가기 위한 선행 조건(Prerequisite)이 된다.

| 레벨 | 명칭 (Full Name) | 핵심 속성 (Process Attribute) | 실무적 의미 |
|:---:|:---|:---|:---|
| **0** | **Incomplete (불완전)** | PA 1.1 미달성 | 프로세스가 수행되지 않거나 목표를 달성하지 못함. |
| **1** | **Performed (수행됨)** | **PA 1.1 (Process Performance)** | 프로세스가 수행되고 결과물이 나옴. (개인의 능력에 의존) |
| **2** | **Managed (관리됨)** | **PA 2.1 (Performance Management)** | 계획이 수립되고, 모니터링/조정됨. (Project 단위 관리) |
| **3** | **Established (확립됨)** | **PA 3.1 (Process Definition)** | 조직의 표준 프로세스가 정의되고 적용됨. (Organization 표준화) |
| **4** | **Predictable (예측 가능함)** | **PA 4.1 (Process Quantitative Analysis)** | 통계적 기법으로 성과가 정량 관리됨. (Dev, Six Sigma) |
| **5** | **Optimizing (최적화됨)** | **PA 5.1 (Process Innovation)** | 지속적인 개선과 혁신이 이루어짐. (Automated Improvement) |

#### 4. 상세 평가 구조 (ASCII)

```text
============================================================================
                     [ ISO/IEC 15504 평가 구조도 ]
============================================================================

               [ Process Dimension (수평적 영역) ]
┌────────────────────────────────────────────────────────────────────────────┐
│   CUS (고객-공급자) │ ENG (엔지니어링) │ SUP (지원) │ MAN (관리) │ ORG (조직)│
├────────────────────────────────────────────────────────────────────────────┤
│  예) 요구사항  │  예) 설계      │  예) QA   │  예) PM   │  예) 교육  │
│      분석    │      구현       │     형상  │      일정 │      개선  │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ (Cross-Cutting Evaluation)
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│               [ Capability Dimension (수직적 심도) ]                        │
│                                                                            │
│  Level 5: Optimizing (최적화)      ◀─ 혁신 및 자동화                      │
│  Level 4: Predictable (예측 가능)  ◀─ 정량적 관리 (통계적 수치)            │
│  Level 3: Established (확립됨)    ◀─ 표준 프로세스 수립 및 수행           │
│  Level 2: Managed (관리됨)        ◀─ 계획, 모니터링, 조정                  │
│  Level 1: Performed (수행됨)      ◀─ 기본 수행 (결과물 도출)               │
│  Level 0: Incomplete (불완전)     ◀─ 수행 안 됨                           │
└────────────────────────────────────────────────────────────────────────────┘

   [Example: '설계(Design)' 프로세스의 평가 결과]
   ────────────────────────────────────────
   설계 프로세스는 '수행됨(1)'은 만족하지만, 계획된 관리(2)가 부족하여
   Level 1로 판정됨. ▶ Action Item: 설계 검토 계획(WIP) 수립 필요.
```

#### 5. 핵심 평가 알고리즘 (Process Attribute Scoring)
SPICE 평가자(Assessor)는 각 프로세스에 대해 **PA (Process Attribute)**의 달성률을 0% ~ 100% 사이로 판단한 뒤, 이를 **N (Not Achieved)**, **P (Partially Achieved)**, **L (Largely Achieved)**, **F (Fully Achieved)** 등급으로 변환한다.

```python
# SPICE Scoring Logic (Pseudo-code)
def calculate_process_attribute_rating(achievement_percentage):
    if 0 <= achievement_percentage < 15:
        return 'N'  # Not Achieved (0% ~ 15% 미달)
    elif 15 <= achievement_percentage < 50:
        return 'P'  # Partially Achieved (15% ~ 50% 달성)
    elif 50 <= achievement_percentage < 85:
        return 'L'  # Largely Achieved (50% ~ 85% 달성)
    elif 85 <= achievement_percentage <= 100:
        return 'F'  # Fully Achieved (85% 이상 달성)
    else:
        raise ValueError("Invalid percentage")

# Rating to Level Mapping
# Level 2를 얻으려면:
#   PA 1.1 (Process Performance) must be 'F'
#   AND PA 2.1 (Performance Management) must be 'F' or 'L' (depending on target profile)
```

#### 📢 섹션 요약 비유
> "건물을 지을 때, '설계', '조적', '배관' 등의 공종(프로세스)마다 각각 기능사, 기사, 기술사(능력 레벨)가 누구인지를 확인하고, 부족한 부분이 있으면 자격증 과정을 이수시키는 것과 같은 구조화된 인력 관리 시스템과 같습니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [1,000자+]

#### 1. CMMI vs SPICE: 기술적 상세 비교

| 구분 | **CMMI (Capability Maturity Model Integration)** | **SPICE (ISO/IEC 15504)** |
|:---|:---|:---|
| **주도** | 미국 국방부 후원, SEI (Software Engineering Institute) 주관 | 유럽 중심, ISO/IEC 국제 표준화 기구 |
| **표준성** | 사실상의 표준 (De Facto), 특정 기관 인증 필요 | 공식적인 국제 표준 (De Jure) |
| **평가 모델** | **Staged (단계형)**: Level 1~5를 조직 전체가 획득 | **Continuous (연속형)**: 개별 프로세스의 Level을 개별 산출 |
| **테일러링** | 상대적으로 덜 유연함 (전체 성숙도에 집중) | 매우 유연함 (필요한 프로세스만 선택하여 평가 가능) |
| **Process Attributes** | Goal & Practice 중심 (Specific/Generic Goals) | Process Attribute (PA) 중심 (성과 지표 중심) |
| **적합성** | 대규모 조직, 전사적 차원의 개선 추진 시 유리 | 특정 부서나 강화하고 싶은 특정 프로세스 영역 선정 시 유리 |

#### 2. 산업별 파생 표준 (A-SPICE & MedTech)

SPICE의 가장 큰 강점은 산업별 특성에 맞춰 **Profile**을 확장할 수 있다는 점이다.

*   **Automotive SPICE (A-SPICE)**: 자동차 산업에서 OEM(완성차 업체)이 Tier-1, Tier-2 협력사의 SW 품질을 평가할 때 의무적으로 사용하는 표준이다. **ISO 26262 (Functional Safety)**와 연계되어, SW 결함이 인명에 미치는 영향을 관리하는 핵심 축이다.
*   **SPICE for Medical (MedTech)**: 의료 소프트웨어 개발 시 FDA나 CE 인증을 위한 품질 시스템 증빙 자료로 활용된다.

#### 3. 기술 스택 융합: DevOps & Metrics

최근 SPICE는 **DevOps** 및 **Agile** 환경과의 융합이 논의된다. 전통적인 SPICE는 문서화된 프로세스를 중시하지만, **DevOps**는 코드화된 인프라(IaC)와 자동화 파이프라인을 중시한다.

*   **Synergy**: