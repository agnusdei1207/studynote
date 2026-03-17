+++
title = "677. CMMI 성숙도 5단계 (초기-관리-정의-정량-최적)"
date = "2026-03-15"
weight = 677
[extra]
categories = ["Software Engineering"]
tags = ["Process Improvement", "CMMI", "Maturity Model", "Quality Management", "Software Process"]
+++

# 677. CMMI 성숙도 5단계 (초기-관리-정의-정량-최적)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 조직의 프로세스 역량 성숙도를 5단계로 계층화하여 정의한 **CMMI (Capability Maturity Model Integration)** 모델로, 개인의 영웅주의에서 벗어나 조직 차원의 예측 가능한 시스템을 구축하는 것을 목적으로 한다.
> 2. **가치**: 프로젝트의 성공이 '운'이 아닌 '확률'이 되도록 만들며, 레벨 상승에 따라 결함 밀도 약 30~50% 감소, 일정 준수율 90% 이상 달성 등 정량적 품질 향상을 견인한다.
> 3. **융합**: 단순한 소프트웨어 개발 프로세스를 넘어, 통계적 품질 관리(SQC) 및 애자일(Agile) 방법론과 융합하여 현대적이고 유연한 조직 거버넌스 체계를 제공한다.

---

### Ⅰ. 개요 (Context & Background)

CMMI는 1980년대 미국 카네기 멜론 대학교 **SEI (Software Engineering Institute)**가 미 국방부의 의뢰를 받아 소프트웨어 개발의 난항을 해결하기 위해 탄생시켰습니다. 초기에는 **CMM (Capability Maturity Model)**이라 불렸으나, 후에 시스템 엔지니어링, 조달 등을 통합하여 **CMMI (Capability Maturity Model Integration)**로 발전했습니다.

소프트웨어 위기(Software Crisis) 상황에서 일관되지 않은 성과는 기술적 부재가 아닌 **프로세스 미성숙**에서 기인함을 밝혀냈습니다. CMMI는 이러한 프로세스를 정량적이고 체계적으로 진단·개선하기 위한 '프로세스 개선 프레임워크' 역할을 합니다.

**💡 개념 비유**
CMMI는 **'종합격투기(MMA) 선수의 훈련 체계'**와 같습니다. 초보선수(레벨 1)는 재능으로 싸우지만, 체계적인 훈련 루틴(레벨 2), 팀 전체 훈련 매뉴얼(레벨 3), 스파링 데이터 분석(레벨 4)을 거쳐, 시합 중 실시간 전술 수정(레벨 5)이 가능한 챔피언으로 성장합니다.

**등장 배경**
1. **기존 한계**: 우수한 개발자(Hero Developer) 의존 → 인력 이탈 시 프로젝트 붕괴.
2. **혁신적 패러다임**: '사람 중심'에서 '프로세스 중심'으로 전환 필요성 대두.
3. **현재 비즈니스 요구**: 대형 SI 프로젝트의 납기 준수와 품질 보증을 위한 객관적 프로세스 증명 수단 필요.

**아키텍처 도입 배경**
조직이 성숙해짐에 따라 프로세스의 복잡도와 관리 비용이 증가합니다. 이를 해결하기 위해 CMMI는 프로세스 영역(PA), 목표(Goal), 실천(Practice)의 계층 구조를 통해 무엇을 개선해야 할지 명확한 지도(Map)를 제공합니다.

```text
      [ 조직 성숙도 진화 방향 ]
            
   Level 5: Optimizing (최적화) ──┐
   ▲                               │
   │   (지속적 개선, 혁신)          │
   Level 4: Quantitatively Managed ─┼───> [ 데이터 기반 통제 (Data-Driven) ]
   ▲   (정량적 관리, 통계적 예측)   │
   │                               │
   Level 3: Defined (정의) ────────┼───> [ 표준화 프로세스 (Standardization) ]
   ▲   (조직 차원 표준, 테일러링)   │
   │                               │
   Level 2: Managed (관리) ────────┼───> [ 프로젝트별 통제 (Project Control) ]
   ▲   (요구사항, 일정, 품질 관리)   │
   │                               │
   Level 1: Initial (초기) ────────┴───> [ 개인 역량 의존 (Chaos/Heroism) ]
```
*도해 1: CMMI 성숙도 레벨별 진화 과정. 하단의 혼돈 상태에서 상단의 최적화 상태로 이동하며 프로젝트의 불확실성이 감소함.*

**해설**
위 다이어그램은 조직의 프로세스 성숙도가 낮은 단계(1단계)에서 높은 단계(5단계)로 이동함에 따라 프로젝트 관리의 패러다임이 어떻게 변화하는지를 시각화한 것입니다. **Level 1 (Initial)**에서는 프로젝트의 성공이 개인의 역량과 운에 달려 있어 결과를 예측하기 어렵습니다. **Level 2 (Managed)**에 도입하면 기본적인项目管理 프로젝트 관리(계획, 모니터링)가 도입되어 '반복 가능한' 성과를 낳습니다. **Level 3 (Defined)**는 조직 전체에 표준화된 프로세스가 정착되는 단계입니다. **Level 4 (Quantitatively Managed)**는 통계적 기법을 도입하여 프로세스 성과를 정량적으로 측정하고 예측합니다. 마지막으로 **Level 5 (Optimizing)**에서는 수집된 데이터를 기반으로 프로세스 자체를 혁신하여 지속적으로 최적화하는 단계에 이릅니다. 각 단계 상승 시 조직의 '예측 가능성(Predictability)'과 '통제 가능성(Controllability)'이 비약적으로 향상됩니다.

> **📢 섹션 요약 비유**: 마치 도로 교통 체계가 없는 시골 길(레벨 1)에서, 신호등이 설치되고(레벨 2), 교통 법규가 통일되며(레벨 3), 교통流 데이터에 따른 신호 최적화가 이루어지는(레벨 4), 드론을 활용한 교통 체계 진화가 일어나는(레벨 5) 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CMMI 아키텍처는 단순한 등급 체계가 아니라, 실제 조직이 수행해야 할 활동을 정의한 **구조적 프레임워크**입니다.

**구성 요소 (표)**
| 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 프로토콜/형식 | 비유 |
|:---|:---|:---|:---|:---|
| **PA** | **Process Area** | 프로세스 영역. 개선이 필요한 특정 활동 분야 (예: 요구사항 관리, 형상 관리) | CMMI 규격 정의 | 운동 종목 (예: 마라톤, 역도) |
| **SG** | **Specific Goal** | 특정 목표. 해당 PA를 달성하기 위해 반드시 충족해야 할 속성 | 달성 기준 (Achieved/Not Achieved) | 금메달 획득 조건 |
| **SP** | **Specific Practice** | 특정 실천. SG를 달성하기 위한 구체적인 활동 (예: 형상 항목 식별) | 활동 수행 (Performed) | 훈련 루틴 |
| **GG** | **Generic Goal** | 일반 목표. 모든 PA에 공통적으로 적용되는 인프라 수준의 목표 (예: 조직화) | 조직적 정착 (Institutionalized) | 체육관/장비 관리 |
| **GP** | **Generic Practice** | 일반 실천. GG를 달성하기 위한 기반 활동 (예: 조직 정책 수립) | 정책/훈련/검증 | 공통 훈련 규칙 |

**심층 동작 원리**
CMMI의 진정한 핵심은 프로세스가 **'단순히 존재하는 것'**에서 **'조직에 내재화(Institutionalization)'**되는 것입니다. 이는 **OPP (Organizational Process Performance)**와 **OPD (Organizational Process Definition)**라는 두 가지 핵심 메커니즘을 통해 구현됩니다.

1.  **정의 (Definition)**: 조직은 자신만의 **OSSP (Organizational Standard Process)**를 정의합니다. 이는 모든 프로젝트가 따르는 '기준서'입니다.
2.  **테일러링 (Tailoring)**: 프로젝트는 이 표준 프로세스를 그대로 가져오는 것이 아니라, 프로젝트의 특성(규모, 도메인, 난이도)에 맞춰 **테일러링(Tailoring)**합니다. 즉, 표준을 '수정'하는 것이 아니라 표준을 '선택 및 적용'하는 과정입니다.
3.  **적용 & 수집**: 프로젝트는 테일러링된 프로세스를 수행하며, 실시간 데이터(공수, 결함 수)를 수집합니다.
4.  **피드백 (Feedback)**: 수집된 데이터는 조직의 프로세스 자산 라이브러리(**PAL**: Process Asset Library)로 피드백 되어, 표준 프로세스를 개선하는 기반이 됩니다.

```text
   [ 조직 차원 (Organization) ]            [ 프로젝트 차원 (Project) ]
   
   ┌─────────────────────────────┐          ┌─────────────────────────────┐
   │   OPD (Organizational Process│  Tailor  │   PDP (Project Defined)     │
   │   Definition)                ─────────▶   Process)                   │
   │                             │          │                             │
   │   OSSP (Standard Process)   │          │   Project Plan              │
   │                             │          │   (Tailored Process)        │
   └─────────────────────────────┘          └─────────────────────────────┘
                  ▲                                   │
                  │                                   │ Data (Metrics)
                  │                                   │
   ┌─────────────────────────────┐          ┌─────────────────────────────┐
   │   PAL (Process Asset Library)◀─────────│   Execution & Measurement    │
   │                             │  Data    │                             │
   │   Lessons Learned           │          │   SPMC (Statistical Proj..) │
   │   Best Practices            │          │                             │
   └─────────────────────────────┘          └─────────────────────────────┘
```
*도해 2: 조직의 표준 프로세스(OPD)와 프로젝트의 테일러링된 프로세스(PDP) 간의 데이터 상호 작용 구조. 조직의 OSSP는 프로젝트에 의해 적용되고, 프로젝트의 성과 데이터는 다시 조직의 PAL을 풍부하게 만드는 선순환 구조를 가짐.*

**해설**
이 다이어그램은 CMMI 레벨 3 이상의 핵심 동작 원리인 **'표준화와 테일러링의 유기적 관계'**를 보여줍니다. 조직(Organization)은 **OPD (Organizational Process Definition)** 활동을 통해 **OSSP (Organizational Standard Process)**를 구축합니다. 이는 조직의 모든 노하우가 집약된 '마스터 레시피'입니다. 프로젝트 팀은 이 마스터 레시피를 프로젝트의 상황(예: 여름 시즌 한정 메뉴)에 맞춰 수정하는 **테일러링(Tailoring)**을 수행하여 **PDP (Project Defined Process)**, 즉 프로젝트 전용 계획서를 만듭니다. 프로젝트 수행 중 수집된 데이터(공수, 결함 등)는 다시 조직의 **PAL (Process Asset Library)**로 피드백 됩니다. 이 과정이 지속됨으로써, 조직의 표준 프로세스는 끊임없이 현장의 목소리를 반영하여 진화(Evolution)하게 됩니다.

**핵심 알고리즘: 테일러링 의사결정 프로세스**
```python
# [Pseudo-code] CMMI Level 3: Tailoring Decision Logic

def tailor_process(project_char, ossp_library):
    """
    프로젝트 특성(char)을 고려하여 OSSP를 테일러링하는 함수
    """
    selected_practices = []
    
    # 1. 프로젝트 스케일 확인
    if project_char.man_month < 10:
        selected_practices.append(ossp_library.lightweight_review)  # 경량 검토
    else:
        selected_practices.append(ossp_library.formal_inspection)   # 정식 검토
        
    # 2. 난이도(Criticality) 확인
    if project_char.criticality == 'HIGH':
        selected_practices.append(ossp_library.strict_audit_trail) # 엄격한 감사 추적
        
    # 3. 제약 조건(Calibration) 확인
    # 생략됨: 품질 목표와 자원 제약 간의 trade-off 분석
    
    return approved_process_plan(selected_practices)
```

> **📢 섹션 요약 비유**: 마치 거대한 프랜차이즈 본사(조직)가 시나리오 매뉴얼(OSSP)을 작성하면, 각 지점(프로젝트)은 현지 매출 데이터와 고객 층에 맞춰 메뉴와 시간표를 조정(테일러링)하여 운영하고, 그 결과를 다시 본사에 보고하여 본사 매뉴얼을 개선하는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

CMMI는 독립적으로 존재하는 것이 아니라 다른 품질 경영 기술과 유기적인 관계를 맺고 있습니다.

**1. CMMI vs ISO 9001 / SPICE (ISO/IEC 15504)**
| 구분 | **CMMI** | **ISO 9001** | **SPICE** |
|:---|:---|:---|:---|
| **대상** | 소프트웨어/시스템 엔지니어링 특화 | 전 산업에 적용되는 범용 품질 시스템 | 소프트웨어 프로세스 평가 (유럽 중심) |
| **구조** | 5단계 성숙도 (Step) | 단일 차원 (적합/부적합) | 프로세스 수준별 능력 (0~5등급) |
| **관계** | ISO 9001을 만족함 | CMMI의 상위 호환 개념(부분) | CMMI와 유사한 평가 모델 |

**2. 기술적 시너지: 정량적 관리 (Level 4)와 SQC (Statistical Quality Control)**
CMMI 레벨 4의 핵심은 **'정량적 관리'**입니다. 이는 제조업 분야의 **SQC (Statistical Quality Control)**를 소프트웨어에 적용한 것입니다.

**SPC (Statistical Process Control) 적용 예시**
```text
   [ 결함 �