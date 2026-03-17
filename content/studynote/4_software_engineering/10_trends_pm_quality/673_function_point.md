+++
title = "673. 기능점수 (FP) 내부논리파일(ILF) 외부연계파일(EIF)"
date = "2026-03-15"
weight = 673
[extra]
categories = ["Software Engineering"]
tags = ["Function Point", "FP", "Cost Estimation", "Software Metrics", "ILF", "EIF"]
+++

# 673. 기능점수 (FP) 내부논리파일(ILF) 외부연계파일(EIF)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어의 규모를 개발자의 관점(LOC, Lines Of Code)이 아닌, 사용자가 인식하는 기능적 가치(Functionality)로 정량화하는 ISO/IEC 24570 표준 산정 기법입니다.
> 2. **구조**: 시스템의 데이터 저장소를 **ILF (Internal Logical File)**와 **EIF (External Interface File)**로 분류하여, 단순 필드 수(DET)와 논리적 그룹(RET)을 기반으로 복잡도를 측정합니다.
> 3. **가치**: 요구사항 변경 시 가격 변동의 객관적 근거를 제공하며, 개발 생산성(MM/FP)과 품질(Defects/FP)을 분석하는 프로젝트 관리의 핵심 지표로 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

**기능점수(FP, Function Point)** 분석은 소프트웨어 개발의 난제인 "얼마나 비싼가?"에 대해 기술적 중립성을 유지하며 답을 제시하는 방법론입니다. 1979년 IBM의 알란 알브레히트(Alan Albrecht)가 제안하여 1986년 IFPUG(International Function Point Users Group)가 표준화했습니다.

소프트웨어 공학 초기에는 코드의 라인 수(LLC, SLOC 등)로 규모를 재었으나, 비즈니스 로직이 복잡한 1줄의 코드가 단순 출력 코드 100줄보다 가치가 크다는 역설을 해결하지 못했습니다. FP는 이를 "사용자 트랜잭션(Transaction)"과 "데이터 파일(Data Function)"의 조합으로 해결하여, 구현 언어(C, Java, Python)의 종류와 무관하게 일관된 비용 산정이 가능하게 만들었습니다.

#### 💡 비유: 집짓기의 '평수' vs '벽돌 수'

건물을 지을 때 쓰인 벽돌의 개수(LOC)는 시공사의 재료 낭비 여부를 나타낼 뿐, 집의 가치를 대변하지 못합니다. 반면, 평수(방 개수, 화장실 개수 등)는 거주자(사용자)가 체감하는 공간의 가치(FP)를 정확히 반영합니다. 즉, FP는 소프트웨어라는 건물의 '설계도면상의 면적'을 재는 도구입니다.

#### 아키텍처적 배경 및 진화

```text
[ 1970s: LOC 중심 ]          [ 1980s~: FP 중심 ]           [ Modern: Value/Agile ]
┌──────────────┐            ┌──────────────┐             ┌──────────────────┐
│  코드 라인수  │            │  기능점수(FP)  │             │  스토리 포인트/   │
│  (SLOC/LOC)  │  ───▶  병목 │ (User View)  │  ───▶  발전  │  밸류 기반 측정   │
└──────────────┘            └──────────────┘             └──────────────────┘
   [문제점]                     [해결책]                     [고도화]
   • 언어 의존적                  • 사용자 관점                 • 민첩성 반영
   • 효율성 반영 불가              • 기술 독립적                 • 비즈니스 가치 중심
   • 생산성 비교 어려움            • 생산성 지표화
```

**해설:**
과거 기술 중심의 측정에서 벗어나, FP 등장으로 사용자 요구사항(Request)과 결과(Output)를 기준으로 한 측정이 가능해졌습니다. 이는 소프트웨어 공학이 '생산(Process)' 중심에서 '가치(Value)' 중심으로 패러다임이 전환되는 핵심적인 계기가 되었습니다. 최근에는 애자일(Agile) 환경과 맞물려 더 가볍고 빠른 스토리 포인트(Story Point)로 진화하고 있으나, 정형화된 대규모 프로젝트의 정산 및 사외 검증용으로는 여전히 FP가 금융 및 공공 분야의 표준으로 자리 잡고 있습니다.

> **📢 섹션 요약 비유**: 기능점수(FP)는 "벽돌을 몇 개 쌓았느냐(LOC)"가 아니라, "방이 몇 개이고 엘리베이터가 있는가(기능)"를 따져 집값을 매기는, 부동산 감정평가사의 '평수 산출 공식'과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

FP의 핵심은 시스템의 경계(Boundary)를 설정하고, 그 내부와 외부를 오가는 **데이터(Data)**와 **트랜잭션(Transaction)**을 식별하는 것입니다. 특히 이 섹션에서는 데이터 저장소의 성격을 규정하는 **ILF**와 **EIF**의 구조적 메커니즘을 심층 분석합니다.

#### 1. 데이터 기능 구성 요소 상세 분석

데이터 기능은 시스템 내부의 데이터를 저장하고 관리하는 논리적 그룹을 의미하며, 물리적인 테이블(Table) 구조와 1:1 대응하지 않을 수 있음에 주의해야 합니다.

| 구분 요소 | 내부논리파일 (ILF) | 외부연계파일 (EIF) |
|:---:|:---|:---|
| **Full Name** | **Internal Logical File** | **External Interface File** |
| **주인(Owner)** | **내부 시스템 (Self)** | **외부 시스템 (External)** |
| **CRUD 권한** | Create, Read, Update, Delete (CRUD 가능) | **Read (조회) Only** |
| **데이터 제어** | 시스템이 데이터의 생명주기(Life Cycle) 전체 관리 | 시스템이 데이터를 수정할 수 없음 (참조만) |
| **물리적 위치** | 내부 DB (주로 DBMS 내) | 외부 시스템 DB (API나 파일 연동) |
| **비유** | 내 집 서재에 있는 **나만의 책장** | 동네 도서관에 있는 **공공 책장(대출 목록)** |

#### 2. 복잡도 결정 요소 (RET & DET)

ILF와 EIF의 점수는 단순히 파일의 개수가 아니라 내부의 복잡성을 나타내는 두 가지 지표로 결정됩니다.

1.  **RET (Record Element Type)**: 논리적 데이터 그룹의 수입니다.
    *   예: '회원' ILF 내에 '기본 정보'와 '추가 정보(상세)'가 있으면 RET = 2입니다.
2.  **DET (Data Element Type)**: 사용자가 인식하고 식별 가능한 필드(Attribute)의 수입니다.
    *   예: '회원명', '생년월일' 등은 해당하나, 내부 시스템용 'Created_at' 등은 사용자가 식별하지 못하면 제외할 수 있음(업무 규칙에 따름).

#### 3. 기능점수 산정 아키텍처 및 흐름

FP 산정은 사용자의 요구사항을 분석하여 데이터 모델을 도출하고, 이를 카운팅하는 절차를 따릅니다.

```text
+-----------------------------------------------------------------------+
│                     [ Function Point Analysis Process ]               |
+-----------------------------------------------------------------------+
│                                                                       │
│ 1. Boundary Setting (시스템 경계 설정)                                │
│    ┌───────────────────────┐          ┌───────────────────────┐       │
│    │    User / External    │          │    External System    │       │
│    └───────────────────────┘          └───────────────────────┘       │
│              ▲  ▼                               ▲                     │
│    ────────────────────────────────────────────────────────          │
│    │                    APPLICATION BOUNDARY          │               │
│    │  (Scope of Measurement: Our System)             │               │
│    ────────────────────────────────────────────────────────          │
│                                                                       │
│ 2. Data Function Identification (데이터 기능 식별)                    │
│    ┌─────────────────────────────────────────────────────────────┐   │
│    │                                                             │   │
│    │  [ILF (Internal Logical File)]        [EIF (External...)]   │   │
│    │   ┌───────┐    ◀── (CRUD)           ┌───────┐ ◀── (Read)   │   │
│    │   │ TABLE │                          │ API   │              │   │
│    │   └───────┘                          └───────┘              │   │
│    │      │                                   │                   │   │
│    │      ├─ RET(Row Group Count)            └─ DET/REF Count     │   │
│    │      └─ DET(Field Count)                                    │   │
│    └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│ 3. Rating (복잡도 산정)                                              │
│    ┌─────────────────────────────────────────────────────────────┐   │
│    │                   COMPLEXITY MATRIX                         │   │
│    │   ┌─────────────────────┬─────┬─────┬─────┐                 │   │
│    │   │   DET \ RET         │ 1   │ 2~6 │ 6+  │                 │   │
│    │   ├─────────────────────┼─────┼─────┼─────┤                 │   │
│    │   │ 1 ~ 19 (Low)        │ Low │ Low │ Avg │                 │   │
│    │   │ 20 ~ 50 (Avg)       │ Low │ Avg │ High│                 │   │
│    │   │ 51+      (High)     │ Avg │ High│ High│                 │   │
│    │   └─────────────────────┴─────┴─────┴─────┘                 │   │
│    │     ※ 위 표는 예시이며, ILF/EIF별 상세 매트릭스 적용 필요    │   │
│    └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
+-----------------------------------------------------------------------+
          │
          ▼
   Unadjusted FP (UFP) Summation
```

**해설:**
위 다이어그램은 사용자 요구사항을 물리적 구현이 아닌 논리적 데이터 흐름으로 변환하는 과정을 보여줍니다. 특히 **Boundary(경계)** 설정이 가장 중요하며, 내부 DB에 있더라도 타 시스템에서 주로 관리하고 우리가 읽기만 하는 테이블(예: 공공 기관 코드표)은 **ILF가 아닌 EIF**로 분류되어야 합니다. 이런 구분적 오류는 FP 산정의 정확도를 크게 떨어뜨리는 주요 원인이 됩니다.

#### 4. 핵심 식별 알고리즘 (Pseudo-Code)

```pseudo
// 데이터 기능 식별 및 분류 알고리즘
FUNCTION ClassifyDataFunction(dataGroup, systemBoundary):
    INIT complexityScore = 0
    
    // 1. 경계(Boundary) 판단
    IF dataGroup.IsInside(systemBoundary) THEN
        // 내부에 있는 데이터 -> ILF 후보
        IF dataGroup.HasCRUD() THEN
            RETURN "ILF (Internal Logical File)"
            // 점수 산정: RET(Data Sub-groups)와 DET(Attributes) 개수 카운팅 후 매트릭스 매칭
        END IF
    ELSE
        // 외부에 있는 데이터 -> EIF 후보
        IF dataGroup.IsReferencedOnly() THEN
            RETURN "EIF (External Interface File)"
            // 점수 산정: RET(참조하는 그룹)와 DET(참조하는 필드) 개수 카운팅
        END IF
    END IF
    
    // 2. 복잡도 계산 (Logic)
    IF (RET_Count < 2 AND DET_Count < 20) THEN
        RETURN Complexity.LOW
    ELSE IF (RET_Count > 6 OR DET_Count > 50) THEN
        RETURN Complexity.HIGH
    ELSE
        RETURN Complexity.AVERAGE
    END IF
END FUNCTION
```

> **📢 섹션 요약 비유**: ILF와 EIF의 구분은 마치 **"내 냉장고(ILF)"와 "편의점 냉장고(EIF)"**의 차이와 같습니다. 내 냉장고는 식재료를 넣고 빼고 요리(CRUD)하는 주체가 '나'지만, 편의점 냉장고는 음료를 사서(Read) 마시고 다시 넣지 않습니다. FP는 이 '냉장고'의 크기(RET)와 들어있는 물건 개수(DET)를 따져 시스템의 복잡도를 계산합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

기능점수 분석은 단순히 점수를 매기는 것을 넘어, 소프트웨어의 품질(Quality)과 요구사항 관리(Requirement Engineering)와의 시너지를 냅니다.

#### 1. ILF vs EIF: 기술적 및 비즈니스적 비교 분석

| 비교 항목 | ILF (Internal Logical File) | EIF (External Interface File) |
|:---|:---|:---|
| **데이터 주체성** | **Master (Owner)** | **Slave (Consumer)** |
| **유지보수 비용** | 매우 높음 (CRUD 로직, 백업, 회복 필요) | 상대적으로 낮음 (연동 인터페이스 오류 처리만 고려) |
| **테스트 범위** | 데이터 정합성, 무결성, 트랜잭션 처리 | 인터페이스 연결성, 데이터 포맷 검증 |
| **변경 영향도** | 시스템 전체에 퍼져있는 종속성(Dependency) 발생 | 연계 모듈에 국한된 영향 |
| **점수 가중치** | 일반적으로 EIF보다 높음 (관리 복잡도 반영) | 일반적으로 낮음 |

#### 2. 타 영역(Requirements, QA)과의 융합

기능점수는 프로젝트 관리 전반에서 '통용 화폐'와 같은 역할을 합니다.

**① 요구사항 공학(Requirements Engineering)과의 융합: RTM 연계**
요구사항 추적 매트릭스(RTM, Requirements Traceability Matrix)를 작성할 때, 각 요구사항 ID가 어느 FP 기능(ILF/EIF/EI 등)과 매핑되는지 명시하면, 기능 누락을 방지할 수 있습니다.
*   *Synergy*: "회원 가입 요구사항(REQ-001) → 회원 ILF 식별 + 회원 가입 EI 식별"

**② 소프트웨어 품질 보증(SQA, Software Quality Assurance)과의 융합**
FP를 기반으로 결함 밀도(Defect Density)를 측정합니다.
*   *Metric*: `전체 결함 수 / 총 FP` = 결함 밀도 (Defects per FP)
*   *활용*: ILF의 복잡도가 높은데 테스트 케이스가 부족하다면 리스크로 사전 차단.

```text
[ Convergence Graph: FP & Quality ]

Quality (