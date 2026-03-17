+++
title = "756. 잭맨 프레임워크 6x6 매트릭스"
date = "2026-03-15"
weight = 756
[extra]
categories = ["Software Engineering"]
tags = ["EA", "Zachman Framework", "Enterprise Architecture", "Modeling", "Governance"]
+++

# 756. 잭맨 프레임워크 6x6 매트릭스 (Recap)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기업의 정보 시스템 아키텍처를 정의하기 위해 6가지 관점(Perspective)과 6가지 기술 질문(Interrogative)을 교차시킨 **엔터프라이즈 아키텍처(EA, Enterprise Architecture)의 온톨로지(Ontology) 분류 체계**이다.
> 2. **구조적 통합**: '데이터(What), 기능(How), 네트워크(Where), 사람(Who), 시간(When), 동기(Why)'라는 6가지 기본 원형(Primitive)을 경영자부터 개발자까지 각기 다른 추상화 수준에서 조망하여, **"완전성(Completeness)"**을 보장한다.
> 3. **가치**: 특정 기술이나 방법론에 종속되지 않는 중립적인 스키마(Schema)를 제공하여, 복잡한 전사 자산의 투명성을 확보하고 비즈니스와 IT 간의 **의사소통 단절(Semantic Gap)**을 해소하는 기준점이 된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학
잭맨 프레임워크(Zachman Framework)는 1987년 존 잭맨(John Zachman)이 제안한 것으로, 건축학의 '설계 도면' 개념을 정보 시스템으로 확장한 것이다. 이는 단순한 분류표가 아니라, **"기업을 구성하는 모든 것(Enterprise Object)"**을 기술하는 **원자론적 분류 체계(Taxonomy)**이다.

### 💡 비유: 건축물의 설계 도면 세트
건물을 짓을 때 하나의 그림만으로는 부족하다.
1.  **주인(Owner)**은 방의 배치(평면도)를 알고 싶어 한다.
2.  **설계사(Designer)**는 구체적인 내부 인테리어와 전기 배선 도면을 필요로 한다.
3.  **시공사(Builder)**는 철근과 콘크리트의 배치(상세도면)를 요구한다.
잭맨 프레임워크는 이처럼 **"보는 사람의 관점"**에 따라 **"보여지는 결과물"**이 달라져야 함을 정의한다.

### 등장 배경
① **한계**: 초기 IT 개발은 기술 구현(How)에만 집중하여, 비즈니스 목적(Why)과 실제 운영(Who)의 괴리가 컸다.
② **혁신**: 시스템을 단순한 코드가 아닌, '복잡한 기업 활동의 거울'로 인식하고, 이를 기술하기 위한 공간적 좌표(Grid)를 제안했다.
③ **현재**: 디지털 전환(DT, Digital Transformation) 시대에 레거시와 신규 시스템의 통합 관점을 제공하는 가장 기초적인 거버넌스 도구로 활용된다.

### ASCII 다이어그램: 잭맨 매트릭스의 구조적 개요
아래는 36개의 셀(Cell)로 구성된 잭맨 프레임워크의 전체 구조도이다.

```text
      COLUMNS (Interrogatives / 기본 질문) ─────────────────────────────────────────┐
      ↓    ↓      ↓      ↓      ↓      ↓      ↓                                      │
      DATA   FUNCTION NETWORK PEOPLE TIME    MOTIVATION    │  (Primitive Types)      │
     (What)   (How)   (Where)  (Who)  (When)     (Why)     │                         │
ROWS ───────────────────────────────────────────────────────────────────────────────┘
(Perspectives)
1. Planner   ─────┼────────┼────────┼────────┼────────┼────────┼───── → Scope (범위)
   (경영자)       │        │        │        │        │        │
2. Owner     ─────┼────────┼────────┼────────┼────────┼────────┼───── → Business Model (업무 모델)
   (소유자)       │        │        │        │        │        │
3. Designer  ─────┼────────┼────────┼────────┼────────┼────────┼───── → System Model (시스템 모델)
   (설계자)       │        │        │        │        │        │
4. Builder   ─────┼────────┼────────┼────────┼────────┼────────┼───── → Technology Model (기술 모델)
   (구축자)       │        │        │        │        │        │
5. Sub-       ─────┼────────┼────────┼────────┼────────┼────────┼───── → Detailed Rep. (상세 표현)
 contractor      │        │        │        │        │        │
  (협력사)        │        │        │        │        │        │
6. Function  ─────┴────────┴────────┴────────┴────────┴────────┴───── → Working System (가동 시스템)
  System
   (운영자)

* 각 셀(Cell)은 독립적인 관점과 질문에 대한 답변을 문서화(Artifact)해야 함을 의미함.
```
**해설**: 위 표는 세로축(행)이 **"누가 보는가(Who)"**에 관한 것이고, 가로축(열)이 **"무엇을 보는가(What)"**에 관한 것이다. 가로축의 6가지(What, How, Where, Who, When, Why)는 모든 복잡한 시스템을 기술하기 위해 필수적인 원형(Primitive)들이며, 이들을 조합하면 기업의 모든 측면을 기술할 수 있다는 것이 잭맨의 핵심 가정이다.

### 📢 섹션 요약 비유
> "마치 거대한 도시를 축소 모형으로 만들 때, **'전체 지도(Planner)', '건축 도면(Designer)', '상세 치수(Builder)'**를 구분해서 보관함에 따라 정리하듯, 잭맨은 복잡한 기업의 모습을 36개의 서랍으로 정리해두는 **'설계 도면 금고'**와 같습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

잭맨 프레임워크를 이해하기 위해서는 각 축(Row, Column)의 의미와 이들이 만나는 36개의 셀(Cell)이 어떤 **아티팩트(Artifact, 산출물)**를 요구하는지 심층 분석해야 한다.

### 1. 구성 요소 (표)

| 구분 | 요소명 | 역할 | 내부 동작 특징 | 대표 산출물 예시 |
|:---:|:---|:---|:---|:---|
| **Row** | **Scope** | 경영자의 관점 | 비용/효율 분석, 현황 파악 | 사업 계획서, 예산안 |
| (관점) | **Enterprise Model** | 업무 담당자의 관점 | 업무 흐름, 정보 요구사항 | 업무 프로세스図, UCD(Use Case Diagram) |
| | **System Model** | 아키텍트의 관점 | 논리적 데이터, 무결성, 설계 | ERD(ER Diagram), Class Diagram |
| | **Technology Model** | 설계자의 관점 | 물리적 배치, 네트워크, 인터페이스 | 네트워크 맵, 시스템 아키텍처 |
| | **Detailed Representation** | 개발자/시공자의 관점 | 실제 코드, DB 스키마, 컴포넌트 | Source Code, DDL |
| | **Functioning Enterprise** | 운영자의 관점 | 실제 가동 중인 인스턴스 | Runtime Environment, Production Data |
| **Col**| **Data (What)** | 중요한 자산 | 정적(Static)인 정보의 구조 | 개체(Entity) 정의서 |
| (질문) | **Function (How)** | 프로세스 | 동적(Dynamic)인 활동 및 변환 | 프로세스 명세서 |
| | **Network (Where)** | 분산 | 노드와 링크의 연결성 | 네트워크拓扑(Topology) |
| | **People (Who)** | 책임 | 조직과 역할 | 조직도, RACI 매트릭스 |
| | **Time (When)** | 변환 이력 | 상태 변화 및 타이밍 | 상태 전이図, 이벤트 로그 |
| | **Motivation (Why)** | 목적 | 업무 규칙과 제약 조건 | 업무 규칙(Business Rule) |

### 2. ASCII 구조 다이어그램: 관점별 세부도 (35mm Slide 원리)
잭맨 프레임워크의 핵심 원리 중 하나는 **"하나의 그림(단순화)은 세부 사항을 감춘다"**는 것이다. 각 행은 단순화된 세계에서 실제 구현된 세계로 나아가는 '변환(Transformation)' 과정을 나타낸다.

```text
[관점의 심화 Depth]
    ↑
    │  1. Scope (개괄)          2. Model (의미)           3. Structure (논리 구조)
    │  "그림은 무엇인가?"         "의미는 무엇인가?"          "어떻게 작동하는가?"
    │  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
    │  │   External      │      │   Logical       │      │   Physical      │
    │  │   View          │─────▶│   View          │─────▶│   View          │
    │  │   (Icon)        │      │   (Model)       │      │   (Detail)      │
    │  └─────────────────┘      └─────────────────┘      └─────────────────┘
    │          ▼                         ▼                         ▼
    │      그림 제목                  논리적 모델링             상세 명세서
    │
    └──────────────────────────────────────────────────────────────────────▶ [시간/상세도]
    
    * Builder 이후(4, 5, 6행)는 실제 구현 단계로, 물리적인 부품(Code, Hardware)으로 나뉨.
```

### 3. 심층 동작 원리: 기본 원형(Primitive)의 조합
잭맨은 모든 복잡한 시스템이 6가지 원형으로 환원될 수 있다고 주장한다.
- **결합 규칙**:
  - **What(데이터) + How(기능)**: 데이터가 기능에 의해 변환됨 (`Input -> Process -> Output`).
  - **Where(네트워크)**: 변환이 일어나는 물리적/논리적 위치.
  - **Who(사람)**: 기능을 수행하거나 트리거하는 주체.
  - **When(시간)**: 기능의 수행 시점(이벤트).
  - **Why(동기)**: 기능을 제어하는 규칙(정책).

### 4. 핵심 알고리즘/공식 & 코드: 셀 주소 지정 체계
실무에서 잭맨 매트릭스는 문서 분류 시스템(PKS, Public Key System)과 같이 활용된다. 예를 들어, **"우리 고객 데이터베이스의 비즈니스 정의는 어디에 있습니까?"**라는 질문에 대해 체계적으로 답할 수 있다.

```python
class ZachmanMatrix:
    """
    잭맨 프레임워크의 36개 셀을 정의하는 간단한 클래스.
    행과 열의 조합으로 아키텍처 결손(Architecture Gap)을 식별한다.
    """
    ROWS = {
        1: "Planner",
        2: "Owner", 
        3: "Designer",
        4: "Builder",
        5: "Subcontractor",
        6: "Functioning System"
    }
    
    COLS = {
        "DATA": "What",
        "FUNCTION": "How",
        "NETWORK": "Where",
        "PEOPLE": "Who",
        "TIME": "When",
        "MOTIVATION": "Why"
    }

    def locate_artifact(self, row: int, col_key: str) -> str:
        """
        특정 관점과 질문에 해당하는 아티팩트의 위치를 찾습니다.
        
        Args:
            row (int): 1(Planner) ~ 6(Functioning)
            col_key (str): 'DATA', 'FUNCTION' 등
            
        Returns:
            str: 셀 주소 및 설명 (예: "2-1: Owner/Data -> Semantic Model")
        """
        row_name = self.ROWS.get(row, "Unknown")
        col_name = self.COLS.get(col_key.upper(), "Unknown")
        
        # 예시: Row 2 (Owner) + Data (What) = 비즈니스 용어/사전
        if row == 2 and col_key == "DATA":
            return f"Cell({row}, {col_key}): {row_name}'s {col_name} View → Business Entity / Glossary"
            
        # 예시: Row 3 (Designer) + Function (How) = 애플리케이션 명세
        if row == 3 and col_key == "FUNCTION":
            return f"Cell({row}, {col_key}): {row_name}'s {col_name} View → Application Logic / Specification"
            
        return f"Cell({row}, {col_key}): Standard View"

# 실무 활용 예시
zm = ZachmanMatrix()
print(zm.locate_artifact(2, "DATA")) 
# Output: Cell(2, DATA): Owner's What View → Business Entity / Glossary
```
**해설**: 위 코드는 잭맨 프레임워크를 단순한 표가 아니라 **검색 가능한 데이터베이스 인덱스**로 모델링한 것이다. 실제 기술사 시험이나 현장에서는 "비즈니스 관점(Owner)의 데이터(What) 정의서가 없다"는 식의 **"결손(Gap) 분석"**을 수행할 때 이 좌표 개념을 사용한다.

### 📢 섹션 요약 비유
> "단어(단일 관점)만으로는 문장(시스템)의 의미를 완성할 수 없듯이, **'주어+목적어+동사+부사'** 등 6가지 문법 요소를 문장 구조마다(관점별로) 다르게 배열하는 것이 잭맨의 원리입니다. 즉, **'영어 문법의 6대 요소'**를 기업 시스템에 대입한 것과 같습니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

잭맨 프레임워크는 EA의 지형도라면, 다른 방법론들은 여행 가이드북이나 건설 공법과 같다.

### 1. 심층 기술 비교표 (Zachman vs. TOGAF vs. DoDAF)

| 구분 | **Zachman Framework** | **TOGAF (The Open Group Architecture Framework)** | **DoDAF (DoD Architecture Framework)** |
|:---|:---|:---|:---|
| **성격** | **분류 체계(Ontology)** | **프로세스(Methodology)** | **데이터 모델(Centric)** |
| **핵심 목표** | 존재하는 모든 것을 카탈로그화 (What exists?) | EA를 구축하고 개선하는 단계적 프로세스 (How to build?) | 군사 작전의 통합 시야 제공 (Interoperability) |
| **주요 산출물** |