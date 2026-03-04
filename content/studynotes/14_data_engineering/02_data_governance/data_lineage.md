+++
title = "데이터 리니지 (Data Lineage)"
date = "2026-03-04"
[extra]
categories = "studynotes-data-engineering"
+++

# 데이터 리니지 (Data Lineage)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터의 발생 원천(Source)부터 가공, 변환(ETL/ELT), 최종 소비 지점(BI/ML)까지의 전체 생애주기와 이동 경로를 시각적으로 매핑하고 추적하는 핵심 데이터 거버넌스 기술입니다.
> 2. **가치**: 장애 발생 시 근본 원인(Root Cause Analysis)을 수 분 내에 파악하고, 스키마 변경 전 하위 시스템에 미치는 영향(Impact Analysis)을 예측하여 전사적 데이터 파이프라인의 신뢰성과 투명성을 보장합니다.
> 3. **융합**: 복잡한 관계를 탐색하기 위해 그래프 데이터베이스(Graph DB)와 깊이 연관되며, GDPR/CCPA 등 개인정보 보호 컴플라이언스 추적 및 데이터옵스(DataOps) 자동화의 근간을 형성합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**데이터 리니지(Data Lineage)**, 우리말로 '데이터 족보' 또는 '데이터 계보'라 불리는 이 기술은 데이터가 "어디서 왔고(Origin), 어떤 과정을 거쳐 변형되었으며(Transformation), 현재 어디로 흘러가고 있는지(Destination)"를 기록한 메타데이터의 집합체입니다. 단순한 데이터 사전(Data Catalog)이 정적인 '상태'를 보여준다면, 리니지는 데이터의 동적인 '흐름(Flow)과 의존성(Dependency)'을 그래프 형태로 표현합니다.

#### 2. 💡 비유를 통한 이해
데이터 리니지는 **'유기농 농산물의 이력 추적 시스템'**과 같습니다.
- 대형 마트(BI 대시보드)에서 딸기(데이터)를 샀는데 농약이 검출(데이터 오류)되었습니다.
- 이력 추적 시스템(데이터 리니지)이 없다면 어느 농장(소스 DB)에서, 어떤 운송 트럭(ETL 도구)을 거쳐 이 딸기가 왔는지 알 수 없어 마트의 모든 딸기를 버려야 합니다.
- 반면 리니지가 구축되어 있으면 바코드 스캔 한 번으로 "A 농장에서 3월 2일에 B 트럭을 타고 온 딸기"임을 즉시 역추적하여, 원인이 된 농장만 신속히 차단할 수 있습니다.

#### 3. 등장 배경 및 발전 과정
1.  **데이터 파이프라인의 블랙박스화**: 과거에는 데이터 흐름이 RDBMS 내의 프로시저 정도로 단순했으나, 클라우드, 마이크로서비스(MSA), 데이터 레이크가 도입되면서 데이터 이동 경로가 거미줄처럼 얽혀 사람이 머리로 추적할 수 없는 지경에 이르렀습니다.
2.  **규제 및 컴플라이언스의 강화**: GDPR이나 금융당국의 규제는 "고객의 개인정보(PII)가 회사의 어느 서버, 어느 테이블에 저장되어 있고, 누가 접근하는지 정확히 소명할 것"을 강제하기 시작했습니다.
3.  **데이터 신뢰성(Data Trust)의 위기**: BI 대시보드의 숫자가 틀렸을 때 그 원인을 찾는 데 데이터 엔지니어가 며칠을 허비하는 일이 잦아지자, 자동화된 리니지 추적 솔루션(Apache Atlas, OpenLineage 등)의 도입이 필수적인 아키텍처 요소로 자리 잡았습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 데이터 리니지의 구성 요소 (표)

| 분류 | 상세 역할 및 특징 | 내부 동작 메커니즘 | 활용 주체 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **비즈니스 리니지 (Business Lineage)** | 비즈니스 용어 간의 관계 표현 | 논리적 데이터 모델과 비즈니스 용어집(Glossary) 매핑 | C-Level, 현업 사용자 | 지하철 노선도 (큰 흐름) |
| **테크니컬 리니지 (Technical Lineage)** | 물리적 테이블/컬럼 단위의 이동 추적 | SQL 파싱, ETL 도구 메타데이터 크롤링 | 데이터 엔지니어, DBA | 지하철 배선도 (물리적 구조) |
| **오퍼레이셔널 리니지 (Operational Lineage)** | 실제 실행된 Job의 상태 및 통계 | 런타임 로그 수집, Airflow/Spark API 연동 | 시스템 운영자 (SRE) | 지하철 실시간 관제판 |
| **수집기 (Ingestion Engine)** | 이기종 시스템에서 메타데이터 추출 | Push(API/Webhook) 및 Pull(Log/DB Crawling) 혼합 | - | 정보 수집 안테나 |
| **저장소 및 탐색 엔진** | 노드와 엣지 형태의 데이터 저장/쿼리 | Property Graph DB (Neo4j, JanusGraph) 활용 | - | 관계형 뇌 구조 |

#### 2. 리니지 데이터 수집 아키텍처 (ASCII 다이어그램)

```text
<<< Data Lineage Architecture (Based on OpenLineage Standard) >>>

[ Source Systems ]      [ Transformation ]      [ Consumption ]
   MySQL / Kafka          Airflow / Spark       Tableau / Superset
        |                       |                       |
        +---------+-------------+-------------+---------+
                  | (1. Emit Run-time Metadata JSON)
                  v
===================================================================
[ Metadata Ingestion API (REST / Kafka Topic) ]
===================================================================
                  | (2. Parse & Validate)
                  v
[ Lineage Construction Engine ] (SQL Parser / Dependency Builder)
                  | (3. Extract Nodes(Entities) & Edges(Relations))
                  v
[ Graph Database (e.g., Neo4j / Apache Atlas) ]
  (Table A) ---[derived_from]---> (Table B) ---[consumed_by]---> (Dashboard)
===================================================================
                  | (4. Graph Traversal Query)
                  v
[ User Interface ]
  - Impact Analysis (Forward Traversal)
  - Root Cause Analysis (Backward Traversal)
```

#### 3. 심층 동작 원리: 리니지 자동 추출 기법 (SQL Parsing vs 런타임 후킹)
데이터 리니지를 구축하는 기술적 핵심은 쿼리와 코드를 분석하여 종속성을 뽑아내는 것입니다.
1.  **정적 SQL 파싱 (Static SQL Parsing)**:
    - 데이터베이스의 쿼리 히스토리(Query History)를 스캔하여 `INSERT INTO target_table SELECT a, b FROM source_table` 같은 SQL 문을 AST(Abstract Syntax Tree)로 분해합니다.
    - AST를 순회하며 Source와 Target을 식별하고 엣지(Edge)를 생성합니다. (복잡한 뷰나 다중 조인 분석에 강함).
2.  **런타임 후킹 메커니즘 (Run-time Hooking)**:
    - Apache Spark나 Flink 같은 분산 처리 엔진이 Job을 실행할 때, **OpenLineage API** 등을 통해 "어떤 입력 파일을 읽어서, 어떤 스키마로 변환하여, 어디에 썼는지"에 대한 메타데이터 이벤트(JSON)를 리니지 서버로 실시간(Push)으로 전송합니다.

#### 4. 실무 수준의 구현 예시 (OpenLineage JSON 이벤트 포맷)
```json
// [상황] Spark Job이 실행될 때 발생하는 리니지 이벤트 (부분 발췌)
{
  "eventType": "COMPLETE",
  "eventTime": "2024-03-04T10:00:00Z",
  "run": {
    "runId": "123e4567-e89b-12d3-a456-426614174000"
  },
  "job": {
    "namespace": "my-spark-cluster",
    "name": "daily_sales_aggregation"
  },
  "inputs": [{ // 역추적(Root Cause)의 대상
    "namespace": "s3://raw-data-bucket",
    "name": "sales_events",
    "facets": {
      "schema": { "fields": [ { "name": "amount", "type": "INT" } ] }
    }
  }],
  "outputs": [{ // 영향도 분석(Impact)의 대상
    "namespace": "postgres://dw-server",
    "name": "fact_sales_daily"
  }]
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 정적 리니지(Static) vs 동적 리니지(Active/Dynamic) 비교

| 비교 항목 | 수동/정적 리니지 (Passive/Static) | 동적/액티브 리니지 (Active/Dynamic) |
| :--- | :--- | :--- |
| **구축 방식** | 개발자가 수기로 문서화 / 주1회 배치 크롤링 | 시스템(Airflow/Spark)이 실행 시점마다 자동 발송 |
| **최신성 보장** | 매우 낮음 (실제 시스템과 문서가 불일치할 확률 높음) | 매우 높음 (실시간 동기화 보장) |
| **활용 범위** | 단순 감사(Audit)용 증빙 자료 | 장애 발생 시 실시간 알람 및 파이프라인 자동 중단(Circuit Breaker) |
| **도입 난이도** | 낮음 (기존 시스템 수정 불필요) | 높음 (전체 데이터 파이프라인 코드에 SDK 심어야 함) |

#### 2. 과목 융합 관점 분석 (알고리즘 및 보안)
- **자료구조 (Graph Traversal)**: 리니지는 본질적으로 방향성 비순환 그래프(DAG, Directed Acyclic Graph)입니다. 특정 컬럼 변경 시 영향을 받는 대시보드를 찾기 위해서는 그래프를 정방향으로 순회하는 **BFS/DFS 알고리즘**이 활용되며, 이는 RDBMS의 재귀 쿼리(Recursive CTE)보다 그래프 DB에서 압도적으로 빠르게 수행됩니다.
- **보안 (Zero Trust & PII Tracking)**: 보안 과목의 컴플라이언스와 융합됩니다. 주민등록번호 같은 민감 데이터(PII)가 태깅된 노드(테이블)가 있을 때, 리니지 그래프를 통해 해당 노드와 연결된 모든 하위 복제 테이블들에 자동으로 **마스킹(Masking)** 및 **접근 통제(ACL)** 정책을 전파시킬 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 1: CEO 보고용 매출 대시보드의 데이터 오류 발생**
  - 상황: 대시보드의 매출액이 전일 대비 50% 폭락하여 비상이 걸림.
  - 판단: 데이터 엔지니어는 리니지 툴의 **역방향 추적(Backward Traversal)** 기능을 실행합니다. 대시보드 -> 데이터 마트 -> DW -> ETL Job -> 소스 DB 순으로 추적하여, 새벽에 소스 DB의 환율 테이블 API가 실패하여 NULL 값이 들어간 것을 즉각적으로 특정(Root Cause Analysis)하고 조치합니다.
- **시나리오 2: 핵심 마스터 테이블의 컬럼 타입 변경(INT -> BIGINT)**
  - 상황: 주문 번호가 한계에 달해 데이터 타입을 변경해야 함.
  - 판단: 테이블 변경 전, 리니지 툴에서 **영향도 분석(Impact Analysis)**을 수행합니다. 해당 컬럼을 참조하는 30개의 후속 배치 Job과 5개의 Tableau 대시보드 목록을 추출하고, 관련 담당자들에게 사전 공지를 발송하여 변경으로 인한 연쇄 장애를 원천 차단합니다.

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **표준화된 프로토콜**: 파이프라인 도구마다 각기 다른 방식으로 리니지를 수집하면 통합이 불가능합니다. OpenLineage와 같은 업계 표준을 도입하여 벤더 종속성을 피했는가?
- [ ] **성능 오버헤드**: 수만 개의 Spark Task가 실행될 때 리니지 이벤트 발송으로 인해 메인 데이터 처리 파이프라인의 성능이 저하되지 않도록 비동기 처리(Async) 구조를 갖추었는가?
- [ ] **컬럼 레벨(Column-level) 지원**: 단순히 테이블 간의 관계만 보여주는 것은 실무에서 반쪽짜리입니다. A테이블의 '주문액' 컬럼이 B테이블의 '총합계' 컬럼으로 어떻게 연산되어 들어갔는지(Transformation Logic) 정밀하게 추적 가능한가?

#### 3. 안티패턴 (Anti-patterns)
- **'그림만 예쁜' 리니지 도입**: 툴은 화려하지만, 정작 회사 내 데이터 거버넌스 위원회나 데이터 오너십(Data Ownership) 문화가 없다면 리니지는 아무도 보지 않는 값비싼 대시보드로 전락합니다. 기술 도입 전 사람과 프로세스(조직 문화)의 정비가 선행되어야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- **정량적**: 데이터 장애 원인 파악 시간(MTTR) 90% 단축 (수 일 -> 수 분), 스키마 변경 시 발생하는 연쇄 장애(Regression) 0건 달성.
- **정성적**: 데이터 파이프라인의 완전한 가시성 확보로 현업(비즈니스 팀)이 IT팀을 거치지 않고 스스로 데이터의 출처를 신뢰할 수 있게 됨(Data Democratization).

#### 2. 미래 전망 및 진화 방향
데이터 리니지는 단순히 족보를 보여주는 시각화 도구를 넘어, **AI 기반의 능동형(Active) 데이터옵스(DataOps)**로 진화하고 있습니다. 머신러닝이 리니지 그래프를 분석하여 "내일 A 테이블의 변경이 예정되어 있으니, B 대시보드가 깨질 확률이 95%입니다"라고 사전에 예측하고 경고하는 시스템이 표준이 될 것입니다.

#### 3. 참고 표준/가이드
- **OpenLineage**: 데이터 파이프라인 운영 메타데이터 수집을 위한 오픈소스 산업 표준.
- **DAMA-DMBOK (Data Management Body of Knowledge)**: 데이터 아키텍처 및 메타데이터 관리/리니지에 관한 글로벌 표준 지식 체계.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[데이터 거버넌스 (Data Governance)](@/studynotes/14_data_engineering/02_data_governance/_index.md)**: 데이터 리니지가 달성하고자 하는 궁극적인 목표인 데이터 관리 체계.
- **[데이터 레이크하우스 (Data Lakehouse)](@/studynotes/14_data_engineering/01_data_architecture/data_lakehouse.md)**: 리니지 추적의 주요 대상이 되는 현대적인 복합 데이터 아키텍처.
- **[그래프 데이터베이스 (Graph DB)](@/studynotes/05_database/01_relational_model/nosql.md)**: 복잡한 리니지의 노드와 엣지를 가장 효율적으로 저장하고 탐색하는 저장소.
- **[Apache Airflow](@/studynotes/_index.md)**: 리니지 이벤트를 방출(Emit)하는 가장 대표적인 데이터 파이프라인 오케스트레이션 도구.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **마법의 발자국**: 눈밭을 걸어가면 발자국이 남듯이, 데이터가 시스템 안을 돌아다닐 때마다 '내가 여기 지나갔어!' 하고 마법의 발자국을 남기는 거예요.
2. **범인 찾기 놀이**: 만약 요리에 소금 대신 설탕이 들어갔다면, 발자국을 거꾸로 따라가서 언제 설탕 통을 잘못 열었는지 금방 찾아낼 수 있어요.
3. **미리 조심하기**: 반대로 수도관을 고치기 전에, 이 물이 어느 방으로 흘러가는지 미리 지도를 보고 사람들에게 "물 끊깁니다!" 하고 알려줄 수도 있답니다.
