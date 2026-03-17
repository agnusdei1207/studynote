+++
title = "15. CMMI (Capability Maturity Model Integration) - 프로세스 개선의 이정표"
date = "2026-03-14"
weight = 15
[extra]
categories = ["Software Engineering"]
tags = ["Software Process", "CMMI", "Capability Maturity Model", "Governance", "Quality Management"]
+++

# 15. CMMI (Capability Maturity Model Integration) - 프로세스 개선의 이정표

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CMMI (Capability Maturity Model Integration)는 조직의 프로세스 역량을 정량적으로 측정하고 시스템적으로 개선하기 위한 **범용 프로세스 참조 모델**이자 **구조적 진단 프레임워크**입니다.
> 2. **가치**: 단순한 수행 방법론을 넘어, 프로젝트의 비용, 일정, 품질을 예측 가능한 범위 내에서 통제 가능하게 만들며, 납기 준수율을 20% 이상 향상시키고 결함률을 획기적으로 낮추는 **성과 창출의 엔진** 역할을 합니다.
> 3. **융합**: 초기 소프트웨어 개발(SW)에서 시작하여 시스템 엔지니어링(SE), 사람(People), 서비스(SVC), 데이터 관리(DM) 등으로 확장되었으며, Agile/DevOps와 같은 현대적 개발 방법론과의 융합(Agile CMMI)을 통해 지속적인 배포 환경에서의 거버넌스를 강화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
CMMI는 미국 카네기 멜런 대학교 소프트웨어 공학 연구소(SEI, Software Engineering Institute)에서 주도하여 개발한 프로세스 개선 참조 모델입니다. 본래의 SW-CMM (Capability Maturity Model for Software)의 한계를 극복하기 위해 시스템 공학, 통합 프로덕트 개발(IPPD), 공급원 출처(Sourcing) 등 다양한 분야의 성숙도 모델을 통합(Integration)한 것이 핵심입니다. 이는 **"우수한 프로세스가 우수한 결과를 보장한다"**는 전제하에, 조직의 현재 역량 수준을 진단하고 점진적이고 체계적으로 성숙시키는 로드맵을 제공합니다.

**2. 등장 배경: 난개발의 종식**
1990년대 후반, 소프트웨어 산업이 고도화됨에 따라 조직별로 산발적으로 도입된 개별 프로세스들이 서로 충돌하거나 중복되는 '프로세스 스파게티' 현상이 발생했습니다. 기존의 단일 목적 모델(SW-CMM, SE-CMM 등)은 복잡한 시스템 개발 환경에서 유연성을 잃고 오히려 비효율을 초래했습니다. 이를 해결하기 위해 탄생한 CMMI는 **"제품을 어떻게 만드는가(How)"**에 대한 최적의 실무 베스트 프랙티스(Best Practice) 집합체로 자리 잡았습니다. 특히 최근 2.0 버전부터는 성능 중심(Performance-Based)으로 전환하여, 단순한 프로세스 준수가 아닌 비즈니스 성과 실현을 강조하고 있습니다.

**3. 비유를 통한 이해**
CMMI를 **'피아노 연주자의 체계적인 레슨 커리큘럼'**으로 이해할 수 있습니다. 초보 연주자(Level 1)는 연습할 때마다 실수가 나오고 결과물이 들쭉날쭉하지만, 정규 커리큘럼(CMMI)에 따라 기본기(기본 프로세스)를 익히고 스케일 연습(정의된 프로세스)을 거쳐 고난도 곡을 해석하여 자신만의 연주(최적화된 프로세스)를 하게 되면, 어떤 무대(프로젝트)에서도 일정한 수준 이상의 연주(품질)를 보장할 수 있게 됩니다.

**4. 구조적 다이어그램: 프로세스 개선의 사이클**

```text
      [ CMMI: The Process Improvement Engine ]

      +---------------------------------------------------+
      |            Business Objectives & Goals            |
      +---------------------------|-----------------------+
                                  v
      +---------------------------------------------------+
      |   Process Areas (PAs) - Specific & Generic Goals |
      |   (Requirements, Planning, QA, Risk Mgmt...)     |
      +---------------------------|-----------------------+
                                  v
      +---------------------------------------------------+
      |         Institutionalization (Process Assets)     |
      |   +------------------+       +------------------+  |
      |   | Org. Training    |<----->| Org. Process Def |  |
      |   +------------------+       +------------------+  |
      +---------------------------------------------------+
            ^                                 |
            |(Feedback Loop: Maturity Gap)   |
            +---------------------------------+
```
*도해 해설: 위 다이어그램은 비즈니스 목표를 달성하기 위해 프로세스 영역(PA)들이 조직화(Institutionalization)되는 구조를 보여줍니다. 프로세스 자산(Asset)이 축적됨에 따라 피드백 루프를 통해 성숙도 격차(Gap)를 줄여나가는 CMMI의 순환 구조를 나타냅니다.*

---

**📢 섹션 요약 비유**: CMMI 도입은 **'복잡한 대형 건축 현장에 투입된 정밀한 설계도와 건축 규격서'**와 같습니다. 자재(프로세스)가 어디에 어떻게 쓰일지 정의되어 있고, 작업 순서(순서)가 명확히 명시되어 있어 누가 작업하더라도 동일한 품질의 건물(제품)을 지을 수 있도록 보장해 줍니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 (Components)**
CMMI는 단순한 규칙의 집합이 아니라 목표(Goal)와 실무(Practice)의 계층 구조로 되어 있습니다.

| 구성 요소 (Component) | 역할 (Role) | 상세 설명 (Detail) | 비고 |
|:---|:---|:---|:---|
| **Process Area (PA)** | 관리 영역 | 프로세스 개선이 필요한 특정 활동 분야 (예: 요구사항 개발, 기술적 해결) | 25개(DEV) ~ 20개(SVC) |
| **Specific Goal (SG)** | 특정 목표 | 해당 PA를 달성하기 위해 **반드시** 충족해야 하는 특성 | "목표를 달성하려면?" |
| **Specific Practice (SP)** | 특정 실무 | SG를 달성하기 위한 구체적인 활동 | 예: 유지 보수를 위한 기술 솔루션을 설계하라 |
| **Generic Goal (GG)** | 일반 목표 | 해당 PA가 조직에 **제도화(Institutionalized)** 되기 위해 필요한 조건 | 프로세스가 조직의 문화로 정착되도록 함 |
| **Generic Practice (GP)** | 일반 실무 | GG를 달성하기 위한 활동 (훈련, 자산 할당, 검증 등) | 모든 PA에 공통적으로 적용됨 |

**2. 표현 방법 (Representations)**
CMMI는 조직의 문화와 상황에 맞춰 두 가지 관점 중 하나를 선택하여 적용할 수 있습니다.

**① 단계형 (Staged Representation)**
조직 전체의 성숙도를 한 단계 한 단계씩 높여나가는 **계단식(Serial)** 접근법입니다.

```text
      [ Staged Representation: The Maturity Ladder ]

      Level 5: Optimizing (최적화) -- ▶ 프로세스 혁신과 양적 개선
           |
      Level 4: Quantitatively Managed (정량적 관리)
           |     (프로세스가 통계적으로 관리됨)
           |
      Level 3: Defined (정의됨) -- ▶ 조직 표준 프로세스(OSP) 적용
           |     (프로세스가 표준화됨)
           |
      Level 2: Managed (관리됨) -- ▶ 기본적인 프로젝트 관리(계획/요구사항/협상)
           |     (요구사항이 관리됨)
           |
      Level 1: Initial (초기) -- ▶ 성공이 개인의 능력에 의존 (Hero Dependent)
```
*도해 해설: 단계형은 성숙도 레벨(Maturity Level)이라는 개념을 사용합니다. Level 1은 '혼돈' 상태이며, Level 2는 프로젝트가 관리되는 단계, Level 3는 조직 차원에서 프로세스가 표준화되는 단계입니다. Level 4와 5는 통계적 기법을 활용하여 프로세스 자체를 예측 가능하고 최적화하는 고도화 단계입니다.*

**② 연속형 (Continuous Representation)**
특정 프로세스 영역(PA)만을 선택하여 집중적으로 개선하는 **별도의(Separate)** 접근법입니다. 각 PA에 대해 역량 레벨(CL 0~3)을 부여합니다.

```text
      [ Continuous Representation: Capability Profiling ]

      Process Area : [REQM] [PP]  [PMC] [SAM] ...
      Capability      CL3   CL2   CL1   CL3 ...

      Capability Levels (CL):
       CL 0: Incomplete (미완성)
       CL 1: Performed (수행됨) - 기본적인 실행
       CL 2: Managed (관리됨)   - 프로젝트 차원의 관리
       CL 3: Defined (정의됨)   - 조직 차원의 표준화 (Tailoring 포함)
```
*도해 해설: 연속형은 조직이 가장 취약한 부분이나 우선순위가 높은 영역(예: Requirements Development)만 골라 집중 육성할 때 유용합니다. 이를 통해 조직은 **'역량 프로필(Profile)'**을 생성하여 강점과 약점을 한눈에 파악할 수 있습니다.*

**3. 심층 동작 원리: PIID (Process Improvement Implementation Derivation)**
CMMI 인증 심사(Appraisal) 시 가장 중요한 매커니즘은 **CMMI Appraisal Method for Process Improvement (CMMI-SCAMPI)** 입니다. 이는 조직이 실제로 CMMI 모델을 따르고 있는지 검증하는 엄격한 프로토콜입니다.
1.  **Plan**: 심사 범위와 계획 수립
2.  **Briefing**: 관계자 대상 브리핑
3.  **Data Collection**: 문서 검토, 인터뷰, 증거(Objective Evidence) 수집
4.  **Data Consolidation**: 수집된 데이터를 증거 백서(Evidence Package)로 정리
5.  **Rating**: PA 별 목표 달성 여부를 **Satisfactory(충족)** 또는 **Not Satisfactory(미충족)**로 평가
6.  **Reporting**: 최종 진단서(Findings) 발행

**4. 핵심 알고리즘/의사결정: 고성과 프로세스의 수식**
CMMI Level 4 이상에서는 **Process Performance Baseline (PPB)**와 **Process Performance Model (PPM)**을 사용합니다. 프로젝트의 성공 예측을 위해 단순 경험치가 아닌 수식을 활용합니다.

```python
# CMMI Level 4+ Quantitative Management Simulation

def check_process_quality(actual_metric, ppb_lcl, ppb_ucl):
    """
    PPB (Process Performance Baseline)를 기반으로
    현재 프로젝트 지표가 통계적 관리 상태에 있는지 확인
    """
    # LCL: Lower Control Limit, UCL: Upper Control Limit
    if ppb_lcl <= actual_metric <= ppb_ucl:
        return "In Control (Normal Operation)"
    elif actual_metric > ppb_ucl:
        return "Out of Control (Critical Defect Detected)"
    else:
        return "Out of Control (Exceptional Efficiency - Update Model?)"

# Example: Defect Density (Defects/KLOC)
current_defects = 45.0
project_ppb = {'lcl': 20.0, 'ucl': 50.0} # Historical Data
status = check_process_quality(current_defects, project_ppb['lcl'], project_ppb['ucl'])
print(f"Project Status: {status}")
```

---

**📢 섹션 요약 비유**: CMMI의 아키텍처는 **'자동차의 연료 시스템과 내비게이션'**과 같습니다. 단계형(Staged)은 '자동차 조립 순서'처럼 1단계(엔진), 2단계(바퀴) 순으로 완성형을 만들어가는 방식이고, 연속형(Continuous)은 '내비게이션 경로 설정'처럼 목적지(개선하고 싶은 특정 프로세스)에 맞춰 필요한 부분만 업그레이드하는 방식입니다. 둘 다 최종적으로는 안전하고 빠른 주행(비즈니스 목표 달성)을 목표로 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: CMMI v1.3 vs CMMI v2.0**
CMMI는 최근 2018년 발표된 v2.0 버전을 통해 대폭 개편되었습니다.

| 구분 (Criteria) | CMMI v1.3 (Legacy) | CMMI v2.0 (Next Gen) |
|:---|:---|:---|
| **구조** | 3가지 별도 모델 (DEV, SVC, ACQ) | 하나의 통합 모델 (Integration 완성) |
| **목표 수준** | SG(특정 목표)와 GG(일반 목표) 구분 | 단순화된 **Practice Levels** (수행/관리/정의/최적화) |
| **검증 방식** | SCAMPI A/B/C 방법 (복잡함) | **CMMI Appraisal** (유연한 검증, Bits/Bytes 지원) |
| **Agile 지원** | Agile 가이드를 별도 문서로 제공 | 모델 자체에 Agile 실무가 통합됨 |

**2. 타 분야 융합 관점**

**① CMMI + Agile (DevOps)의 만남**
과거 CMMI는 "무거운 문서 작업(Heavy Documentation)"의 대명사로 여겨져 Agile(애자일)과 상충되는 것으로 여겨졌습니다. 그러나 **CMMI v2.0**은 "프로세스를 얼마나 문서화했느냐"가 아니라 "얼마나 잘 수행하고 품질을 관리하느냐"에 초점을 맞춥니다. 예를 들어, **Backlog Refinement**나 **Sprint Retrospective**는 CMMI의 `PP(Peformance Management)`나 `OPD(Organizational Process Definition)` 실무와 완벽하게 매핑됩니다.
- **시너지**: Agile의 **"반복적인 개발(Iterative Development)"**은 CMMI Level 3의 "반복적인 프로세스 수행"과 연결되며, CI/CD 파이프라인의 자동화된 테스트는 CMMI Level 4의 "정량적 관리"를 위한 완벽한 데이터 소스가 됩니다.

**② CMMI vs ISO 9001 (품질 경영 시스템)**
ISO 9001이 **"적합성(Fitness for purpose)"**에 초점을 맞춰 프로세스가 존재하는지를 확인한다면, CMMI는 **"역량(Capability)"**에 초점을 맞춰 프로세스가 **잘 작동하고 있는지(Performance)**를 더 깊이 있게 평가합니다. ISO가 '수료증'이라면 CMMI는 '성적 증명서(A+)'와 같습니다.

**3. 다이어그램: 통합 모델 구조**

```text
      [ CMMI Constellations in v2.