+++
title = "24. 절차적 DML (네비게이션) vs 비절차적 DML (선언적, SQL)"
date = "2026-03-15"
weight = 24
[extra]
categories = ["Database"]
tags = ["DML", "Declarative", "Imperative", "SQL", "Navigation", "Relational Algebra"]
+++

# 24. 절차적 DML (네비게이션) vs 비절차적 DML (선언적, SQL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 조작 언어(DML)는 **"어떻게(How)" 데이터에 접근할지를 사용자가 제어하는 절차적 방식(Procedural)**과 **"무엇(What)"을 원하는지를 선언만 하고 처리 경로는 DBMS에 위탁하는 비절차적 방식(Non-Procedural/Declarative)**으로 대별된다.
> 2. **가치**: 비절차적 DML인 SQL (Structured Query Language)은 **데이터 독립성(Data Independence)**을 극대화하여, 저장 구조(Physical Schema)가 변경되어도 응용 프로그램 코드를 수정할 필요가 없게 하여 개발 생산성과 유지보수성을 획기적으로 개선했다.
> 3. **융합**: 최근의 NoSQL 및 NewSQL 데이터베이스 등장에도 불구하고, 선언적 질의의 편의성과 집합 처리의 성능을 대체할 만한 범용 대안은 없으며, 오히려 데이터 볼륨이 증가할수록 옵티마이저(Optimizer)의 힘을 빌리는 선언적 방식의 중요성이 커지고 있다.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**
절차적 DML (Procedural DML)은 데이터를 검색하거나 갱신하기 위해 데이터베이스 내의 **특정 경로(Navigation Path)**를 프로그래머가 명시적으로 기술해야 하는 언어 체계이다. 반면, 비절차적 DML (Non-Procedural DML)은 사용자가 원하는 데이터의 조건(명제)만 정의하면, DBMS (Database Management System)가 내부의 옵티마이저를 통해 최적의 접근 경로를 자동으로 결정하는 선언적 언어 체계이다. 전자는 "방법(Method)"을, 후자는 "목표(Goal)"를 강조한다.

**등장 배경: 복잡도의 폭발과 추상화의 필요성**
1960년대 ~ 70년대 초반의 계층형(Hierarchical) 및 망형(Network) DBMS 환경에서는 데이터 간의 관계를 포인터(Pointer)로 직접 연결했다. 개발자는 루트(Root) 세그먼트부터 시작하여 하위 세그먼트로 내려가는 복잡한 네비게이션 로직을 일일이 코딩해야 했다. 이는 **접근 경로 종속성(Access Path Dependency)** 문제를 야기했다. 1970년대 E.F. Codd가 관계형 모델(Relational Model)을 제창하며, 수학적 집합론에 기반하여 사용자의 질의와 물리적 저장 구조를 분리한 비절차적 언어(SQL)가 등장하였다.

**💡 핵심 비유**
절차적 언어는 **"도시 지도를 보며 택시 기사에게 '왼쪽으로 돌고, 직진하고, 유턴하여 건물 앞에 서라'고 운전까지 지시하는 것"**과 같다. 길 하나가 막혀도 목적지에 도달할 수 없다. 반면, 비절차적 언어은 **"목적지 주소만 말하고 운전은 기사에게 맡기는 것"**과 같다. 기사(옵티마이저)가 실시간 교통 상황(인덱스 유무, 데이터 분포)을 보아 가장 빠른 길(실행 계획)을 찾아주므로 승객(사용자)은 경로를 신경 쓰지 않아도 된다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ Development Paradigm ]                           │
│                                                                             │
│  [ Procedural DML ]                 [ Non-Procedural DML ]                  │
│                                                                             │
│  👷‍♂️ Developer (Driver)             🕴️ Developer (Passenger)               │
│     |                                    |                                  │
│     v                                    v                                  │
│  ┌─────────────────────┐            ┌─────────────────────┐                │
│  │    🚗 My Code        │            │    🚕 DBMS Engine   │                │
│  │  (I drive logic)    │            │  (System drives)    │                │
│  └─────────────────────┘            └─────────────────────┘                │
│     |                                    |                                  │
│     +--> 📍 Step 1: Get Pointer          +--> 🎯 "Bring me gold"             │
│     |    📍 Step 2: Follow Link              (Just declare intent)           │
│     |    📍 Step 3: Check Condition                                            │
│     |    ...                                                                    │
│     |                                                                            │
│     v (Direct Access)                                                       │
│  💾 DATA                                                                     │
│                                                                             │
│  ❌ Hard-coded Path                                                         │
│  ✅ Precise Control (Potentially Fast if perfect)                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**
마치 **자동 변속기(비절차적)**가 기어비 조절을 운전자 대신 자동으로 처리하여 운전의 복잡성을 줄여주는 것처럼, 비절차적 DML은 데이터 접근 경로를 DBMS에 위임하여 개발자가 비즈니스 로직에만 집중하게 한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 비교 (Component Analysis)**

| 구분 | 절차적 DML (Procedural / Navigation) | 비절차적 DML (Declarative / SQL) |
|:---|:---|:---|
| **작업 단위** | **Record-at-a-time**<br>(하나의 레코드씩 순차 처리) | **Set-at-a-time**<br>(레코드의 집합을 한 번에 처리) |
| **접근 메커니즘** | **Navigation**<br>(포인터 체인, 링크 따라가기) | **Optimization**<br>(관계 대수/해석 변환 및 비용 기반 최적화) |
| **데이터 독립성** | 낮음 (Low)<br>(물리적 구조 변경 시 코드 영향 큼) | 높음 (High)<br>(Logical/Physical Independence 보장) |
| **성능 결정 요인** | 프로그래머의 작성 스킬<br>(루프 효율, 포인터 관리) | **옵티마이저(Optimizer)**의 효율성<br>(통계 정보, 실행 계획) |
| **대표 언어** | DL/I (Data Language/I), IMS (Information Management System), CODASYL DB TG | **SQL (Structured Query Language)**, QBE (Query by Example) |

**2. 심층 동작 원리: Record vs Set**

절차적 DML은 C언어의 포인터와 유사하게 **커서(Cursor)** 혹은 **Get Next** 명령어를 통해 데이터를 하나씩 로드하여 애플리케이션 버퍼로 가져온 뒤 필드를 검사한다. 반면, 비절차적 DML은 WHERE 절로 정의된 **술어(Predicate)**를 만족하는 튜플(Tuple)의 전체 집합을 수학적 연산(Selection, Projection, Join)으로 정의하고, 이를 실행 엔진에 넘긴다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│               [ Processing Flow: Procedural vs Declarative ]               │
│                                                                             │
│  < SCENARIO: Find employees with Salary > 5000 >                           │
│                                                                             │
│  [ 1. Procedural (App-Level Loop) ]        [ 2. Declarative (Set-Level) ]  │
│                                                                             │
│  ┌─────────────────────┐                  ┌─────────────────────┐           │
│  │   Application       │                  │   Application       │           │
│  │   Program           │                  │   Program           │           │
│  └──────────┬──────────┘                  └──────────┬──────────┘           │
│             │                                        │                       │
│             │ 1. Open Cursor                         │                       │
│             │ 2. Fetch Record                        │                       │
│             │    (Get Next)                          │                       │
│             │ 3. If (Sal > 5000)                     │                       │
│             │       Print;                           │                       │
│             │ 4. Loop to 2                           │                       │
│             │                                        │                       │
│             ▼                                        ▼                       │
│  ┌─────────────────────┐                  ┌─────────────────────┐           │
│  │   DBMS Interface    │                  │   DBMS Interface    │           │
│  │   (Record I/O)      │                  │   (Set I/O)         │           │
│  └─────────────────────┘                  └─────────────────────┘           │
│             │                                        │                       │
│             │  (Frequent Network Calls)              │  (Single Command)     │
│             ▼                                        ▼                       │
│  ┌─────────────────────┐                  ┌─────────────────────┐           │
│  │   Disk I/O          │                  │   Query Optimizer   │           │
│  │   (Random Access)   │                  │   ────────────────  │           │
│  │                     │                  │   - Scan Table?     │           │
│  │                     │                  │   - Use Index?      │           │
│  │                     │                  │   - Hash Join?      │           │
│  │                     │                  └──────────┬──────────┘           │
│  │                     │                             │                       │
│  │                     │                             ▼                       │
│  │                     │                  ┌─────────────────────┐           │
│  │                     │                  │   Bulk Processing   │           │
│  │                     │                  │   (Set Operation)   │           │
│  │                     │                  └─────────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**다이어그램 해설**
왼쪽의 절차적 모델은 애플리케이션과 DBMS 간의 **Context Switching**이 매 레코드마다 발생하여 오버헤드가 크다. 개발자가 인덱스가 있다는 사실을 알고 코드를 짜야만 성능이 보장된다. 반면, 오른쪽의 비절차적 모델은 질의 자체가 집합(Set)으로 넘어가므로, DBMS 내부의 옵티마이저가 전체 데이터를 보고 가장 효율적인 벌크 연산(Bulk Operation) 경로를 선택한다. **"하나씩 퍼올리는 양동이(절차적) vs 물 펌프로 한 번에 긷어오는 호스(비절차적)"**의 차이와 같다.

**3. 핵심 알고리즘 및 메커니즘**
비절차적 DML의 핵심은 **질의 변환(Query Transformation)** 과정이다.
1.  **파싱(Parsing):** SQL 문장을 구문 트리(Parse Tree)로 변환.
2.  **검증(Validation):** 스키마(Schema) 메타데이터를 참조하여 테이블/컬럼 존재 여부 및 권한 확인.
3.  **최적화(Optimization):**
    *   **논리적 최적화:** 불필요한 조건 제거, 뷰(View) 병합.
    *   **물리적 최적화:** 후보 실행 계획(Candidate Plans) 생성, 비용 추정(Cost Estimation), 최종 계획 선택.
    *   *수식 예시:* $\text{Cost} = (\text{CPU\_Cost} \times \text{CPU\_Factor}) + (\text{IO\_Cost} \times \text{IO\_Factor})$

**📢 섹션 요약 비유**
절차적 방식은 **"음식점 주방장이 주문이 들어올 때마다 마트에 가서 재료를 하나씩 사 오는 과정"**이며, 비절차적 방식은 **"주문서를 모아서 한꺼번에 도매시장에서 대량으로 사 오는 (Bulk Buy) 과정"**과 같아 시스템 자원 효율성이 압도적으로 높다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 상세 비교 (Quantitative & Qualitative)**

| 평가 지표 | 절차적 접근 (Procedural) | 비절차적 접근 (Declarative: SQL) |
|:---|:---|:---|
| **데이터 독립성** | **물리적 독립성 낮음**<br>인덱스 추가나 파일 위치 변경 시 코드 반영 필수 | **물리적/논리적 독립성 높음**<br>스키마 변경이 최소화됨 |
| **사용자 생산성** | 낮음 (Low)<br>복잡한 루프 및 에러 핸들링 필요 | 높음 (High)<br>간결한 문법으로 빠른 개발 가능 |
| **성능 잠재력** | 개발자가 경로를 완벽히 제어하면<br>특수 케이스에서 매우 빠를 수 있음 | 옵티마이저가 통계 정보를 바탕으로<br>대부분의 상황에서 최적화 수행 |
| **동시성 제어** | 레코드 단위 잠금(Lock)을<br>명시적으로 제어 가능 | 트랜잭션(Transaction) 단위로<br>자동 관리됨 |
| **응용 분야** | 실시간 임베디드 시스템,<br>매우 큰 단일 레코드 처리 | 일반적인 비즈니스 애플리케이션,<br>데이터 웨어하우스, 분석 |

**2. OS 및 소프트웨어 공학적 융합 관점**

*   **OS와의 연계 (Memory Management):** 절차적 DML의 네비게이션 방식은 OS의 **페이징(Paging)** 기술과 밀접하다. 포인터를 따라가다가 페이지 폴트(Page Fault)가 발생하면 성능이 급격히 저하된다. 반면, 비절차적 DML은 DBMS가 **버퍼 매니저(Buffer Manager)**를 통해 미리 필요한 페이지를 시스템 버퍼에 올리는 예측 가능한 I/O 패턴을 생성한다.
*   **컴파일러 이론 (Compiler Theory):** SQL의 최적화 과정은 컴파일러의 코드 최적화와 동일한 원리를 갖는다. SQL을 중간 코드(관계 대수)로 변환하고, 이를 다시 기계어(실행 계획)로 최적화하는 과정은 프로그래밍 언어 컴파일러의 **중간 표현(IR)** 최적화와 같다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Paradigm Shift in Data Access ]                        │
│                                                                             │
│  File System & Network DB (Procedural)     Relational DB (Declarative)      │
│                                                                             │
│  📂 Data is tightly coupled to Logic    🧩 Data is Abstracted (Set)         │
│                                                                             │
│  👉 Application Logic contains           👉 Application Logic contains       │
│     "Where to find data"                    "What to find"                  │
│                                                                             │