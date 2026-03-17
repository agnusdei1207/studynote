+++
title = "[Enterprise] #13. TOGAF (The Open Group Architecture Framework)"
date = "2026-03-17"
weight = 13
[extra]
keyword = "TOGAF_ADM_Architecture_Development_Method_Enterprise_Continuum"
+++

# TOGAF (The Open Group Architecture Framework)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TOGAF는 The Open Group에서 개발한 전 세계에서 가장 널리 사용되는 EA 프레임워크로, 아키텍처를 설계, 계획, 구현 및 관리하기 위한 상세 방법론인 ADM(Architecture Development Method)을 핵심으로 한다.
> 2. **가치**: 특정 기술이나 벤더에 종속되지 않는 개방형 표준을 지향하며, 비즈니스 요구사항을 중심으로 아키텍처의 생애주기를 반복(Iteration) 관리함으로써 엔터프라이즈의 일관된 변화를 주도한다.
> 3. **융합**: 잭맨 프레임워크의 분류 체계와 상호 보완적이며, 최근의 TOGAF 10 시리즈는 애자일(Agile) 및 디지털 트랜스포메이션 환경에 최적화된 모듈형 가이드를 제공한다.

+++

## Ⅰ. 개요 (Context & Background)

기업이 "우리는 EA를 하고 있다"라고 말할 때, 십중팔구는 **"TOGAF"** 방법론을 사용하고 있을 확률이 높다. 1990년대 중반 미 국방부의 TAFIM 모델을 기반으로 시작된 TOGAF는 현재 버전 10까지 진화하며 엔터프라이즈 아키텍처의 사실상 표준(De Facto Standard)이 되었다.

TOGAF가 중요한 이유는 단순히 "아키텍처가 무엇인가"를 정의하는 데 그치지 않고, **"아키텍처를 어떻게 만드는가(How-to)"**에 대한 단계별 레시피를 제공하기 때문이다. 이 레시피가 바로 ADM(Architecture Development Method)이다. 수많은 기업들이 TOGAF를 도입하는 이유는 검증된 베스트 프랙티스를 활용하여 아키텍처 구축의 시행착오를 줄이고, 전 세계 아키텍트들과 공통된 언어로 소통할 수 있기 때문이다.

📢 섹션 요약 비유: TOGAF는 아키텍처를 만들기 위한 '종합 요리 책'과 같아서, 어떤 재료(기술)가 들어오더라도 최고의 요리(엔터프라이즈 시스템)를 완성할 수 있는 상세 조리 순서(ADM)를 제공합니다.

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

TOGAF의 정수는 반복 순환 구조를 가진 ADM(Architecture Development Method)이다.

### 1. TOGAF ADM 순환 구조 (ASCII)

```text
              [ Preliminary ] (준비 단계)
                    │
                    ▼
          ┌──> (A) Architecture Vision <──┐
          │         (아키텍처 비전)        │
          │               │               │
    (H) Architecture      │        (B) Business Architecture
    Change Management     │           (비즈니스 아키텍처)
          ▲               ▼               │
          │      [ Requirements ]         ▼
          │      [ Management ]    (C) Information Systems
    (G) Implementation    ▲        Architectures (Data/App)
    Governance            │               │
          ▲               │               ▼
          │               │        (D) Technology Architecture
          │               ▼           (기술 아키텍처)
          └── (F) Migration Planning <────┘
              (이행 계획 수립)     (E) Opportunities & Solutions
                                   (기회 및 솔루션)
```

**[다이어그램 해설]**  
ADM은 중앙의 **요구사항 관리(Requirements Management)**를 중심으로 8개의 단계(Phase A~H)가 톱니바퀴처럼 맞물려 돌아가는 구조다. 한 번의 순환으로 끝나는 것이 아니라, 비즈니스 환경 변화에 따라 지속적으로 반복(Iteration)하며 아키텍처를 고도화한다. 특히 Phase B, C, D는 EA의 4대 도메인을 설계하는 핵심 구간이다.

### 2. ADM 주요 단계별 활동

| 단계 | 명칭 | 주요 활동 내용 | 핵심 산출물 |
|:---|:---|:---|:---|
| **A** | **Architecture Vision** | 이해관계자 확인, 범위 설정, 비전 수립 | 아키텍처 정의서 (Draft) |
| **B** | **Business Arch.** | 비즈니스 프로세스, 조직, 거버넌스 설계 | 목표 비즈니스 아키텍처 |
| **C** | **IS Architectures** | 데이터 및 애플리케이션 아키텍처 설계 | 목표 데이터/앱 아키텍처 |
| **D** | **Technology Arch.** | 인프라, 네트워크, 기술 참조 모델 설계 | 목표 기술 아키텍처 |
| **E** | **Opportunities & Sol.** | Gap 분석, 구축 옵션 식별, 패키지 선정 | 이행 및 마이그레이션 전략 |
| **F** | **Migration Planning** | 프로젝트 우선순위 결정, 로드맵 수립 | 상세 이행 로드맵 |
| **G** | **Impl. Governance** | 아키텍처 준수 여부 감시 및 기술 심의 | 아키텍처 컴플라이언스 보고서 |
| **H** | **Change Management** | 기술 변화 감시 및 아키텍처 갱신 주기 관리 | 신규 아키텍처 요구사항 |

### 3. TOGAF의 또 다른 핵심: Enterprise Continuum

TOGAF는 모든 것을 밑바닥부터 만드는 것을 권장하지 않는다. **엔터프라이즈 컨티뉴엄(Enterprise Continuum)**이라는 개념을 통해 기존의 자산을 재사용하도록 유도한다.

- **Foundation Architecture**: 가장 일반적인 아키텍처(예: 가상화 기술 표준).
- **Common Systems Architecture**: 특정 산업군 공통(예: 뱅킹 시스템 표준).
- **Industry Architecture**: 더 구체적인 산업 모델.
- **Organization-Specific Architecture**: 우리 회사만의 고유 아키텍처.
*왼쪽에서 오른쪽으로 갈수록 구체화(Specialization)된다.*

📢 섹션 요약 비유: ADM이 아키텍처를 만드는 '방법'이라면, 엔터프라이즈 컨티뉴엄은 이미 잘 만들어진 '기성 부품 상자'와 같아서, 이를 잘 골라 쓰면 훨씬 빠르고 튼튼하게 시스템을 조립할 수 있습니다.

+++

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

TOGAF와 다른 프레임워크 및 최신 트렌드와의 관계다.

### 1. Zachman vs TOGAF 심층 비교

| 구분 | Zachman Framework | TOGAF |
|:---|:---|:---|
| **본질** | 분류 체계 (Ontology) | 프로세스 (Methodology) |
| **강점** | "무엇을(What)" 관리할지 명확함 | "어떻게(How)" 만들지 명확함 |
| **구조** | 6x6 정적 매트릭스 | ADM 동적 순환 모델 |
| **보완 관계** | 잭맨의 칸(Cell)을 채우기 위해 | TOGAF의 ADM 절차를 수행함 |
| **비유** | 도서관의 분류 라벨 | 책을 쓰고 출판하는 과정 |

### 2. 과목 융합: 애자일(Agile)과 TOGAF 10

과거 TOGAF는 너무 무겁고 느리다는 비판을 받았다. 최신 **TOGAF 10**은 이를 보완한다.
- **Modular Framework**: 필요한 부분만 골라 쓰는 모듈형 구조.
- **Agile EA**: 2주 단위 스프린트에 맞춰 아키텍처를 점진적으로 설계하는 기법 도입.
- **Digital Transformation**: 클라우드 네이티브, AI 도입을 위한 별도의 가이드(Snapshot) 제공.

📢 섹션 요약 비유: 과거의 TOGAF가 두꺼운 백과사전 한 권이었다면, 최신 TOGAF는 상황에 맞춰 필요한 페이지만 꺼내 볼 수 있는 디지털 바인더와 같습니다.

+++

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 아키텍트가 TOGAF를 성공적으로 안착시키기 위한 의사결정 포인트다.

### 1. 실무 도입 시나리오: "글로벌 그룹사의 표준 EA 수립"
- **Strategy**: 전사 공통의 Foundation Architecture를 정의하고, 각 계열사(제조, 금융 등)는 Industry Architecture를 참고하여 자신들만의 Organization-Specific 아키텍처를 구축하게 함.
- **Process**: ADM의 Phase G(거버넌스)를 강화하여, 계열사들의 IT 프로젝트가 그룹 표준 기술(TRM)을 벗어나지 않도록 통제.

### 2. TOGAF 도입 체크리스트

| 점검 항목 | 확인 질문 | 기술사적 제언 |
|:---|:---|:---|
| **Tailoring 여부** | ADM의 모든 단계를 억지로 다 수행하려 하지 않는가? | 우리 조직에 맞는 "ADM Tailoring" 선행 필수 |
| **요구사항 관리** | 중앙의 요구사항 DB가 실시간으로 업데이트되는가? | Requirements Management 단계의 자동화 도구 도입 |
| **Gap 분석** | As-Is와 To-Be 사이의 기술적 격차를 정량적으로 분석했는가? | Phase E에서의 명확한 Gap 분석이 이행 성공의 핵심 |
| **역량 확보** | 조직 내에 인증(Certified)받은 아키텍트가 충분한가? | Architecture Capability Framework 구축 |

### 3. 안티패턴
- **"Methodology Fanatic"**: 비즈니스 가치보다 방법론의 절차(산출물 양)에 집착하는 경우. -> **해결**: 산출물을 최소화하고 비즈니스 의사결정에 집중.
- **"One-time ADM"**: ADM 사이클을 한 번 돌리고 종료하는 경우. -> **해결**: Phase H(변경 관리)를 통해 지속적인 선순환 체계 마련.

📢 섹션 요약 비유: TOGAF라는 지도를 너무 세세하게 그리느라 정작 여행(프로젝트)을 떠나지 못하는 우를 범해서는 안 되며, 지도는 걷는 도중에도 계속 수정되어야 합니다.

+++

## Ⅴ. 기대효과 및 결론 (Future & Standard)

TOGAF는 엔터프라이즈의 복잡성을 다루는 가장 성숙한 도구다.

| 기대효과 | 설명 |
|:---|:---|
| **ROI 최적화** | 이행 로드맵(Phase F) 기반의 체계적 투자를 통한 비용 낭비 제거 |
| **리스크 감소** | 거버넌스(Phase G)를 통한 보안 및 표준 미준수 리스크 사전 예방 |
| **유연성 증대** | 모듈형 아키텍처 설계를 통한 시장 변화 대응 속도 향상 |

미래의 TOGAF는 **"데이터 주도 아키텍처(Data-driven Architecture)"**로 진화할 것이다. 사람이 ADM 단계를 수동으로 밟는 것이 아니라, AI 아키텍트가 기업의 실시간 로그를 분석하여 자동으로 Gap을 식별하고 최적의 마이그레이션 경로(Phase E, F)를 제안하는 수준에 도달할 것으로 전망된다.

📢 섹션 요약 비유: TOGAF는 기업이라는 거대한 오케스트라의 지휘자와 같으며, 각 악기(부서/시스템)가 자신의 소리를 내면서도 전체적인 화음(비즈니스 목표)을 이룰 수 있게 해주는 마법의 악보입니다.

+++

### 📌 관련 개념 맵
| 관련 개념 | 관계 및 시너지 설명 |
|:---|:---|
| ADM (Architecture Development Method) | TOGAF의 핵심인 아키텍처 개발 생애주기 방법론 |
| Enterprise Continuum | 아키텍처 자산의 재사용을 위한 분류 및 저장 모델 |
| TRM (Technical Reference Model) | TOGAF에서 제공하는 기초적인 기술 표준 참조 모델 |
| Architecture Governance | 아키텍처가 계획대로 구현되고 유지되는지 통제하는 체계 |
| TOGAF Certified | 전 세계적으로 인정받는 EA 전문가 자격 제도 |

### 👶 어린이를 위한 3줄 비유 설명
1. 아주 커다란 성을 지을 때, 어떤 순서로 벽돌을 쌓고 지붕을 올릴지 적어놓은 "성 짓기 백과사전"이에요.
2. 성을 다 지은 후에도 어디가 고장 났는지 확인하고 고치는 방법까지 친절하게 알려준답니다.
3. 전 세계의 유명한 건축가들이 이 책을 보고 성을 짓기 때문에, 누구나 이 책만 있으면 멋진 성을 완성할 수 있어요.
