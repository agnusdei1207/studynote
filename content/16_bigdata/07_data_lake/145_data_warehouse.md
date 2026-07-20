---
title: "Data Warehouse"
date: "2024-05-22"
tags:
  - "studynote-bigdata"
weight: 145
---
## 핵심 인사이트 (3줄 요약)
1. 기업의 의사결정을 지원하기 위해 여러 시스템의 데이터를 <strong>주제 중심적, 통합적, 시계열적, 비휘발성</strong>으로 구성한 데이터 저장소이다.
2. 저장 전 데이터를 정규화하고 가공하는 <strong>스키마 온 라이트(Schema-on-Write)</strong> 방식을 사용하여 높은 쿼리 성능과 데이터 신뢰성을 보장한다.
3. 비즈니스 인텔리전스(BI)와 리포팅의 핵심 인프라이며, 최근에는 클라우드 기반의 MPP(Massive Parallel Processing) 아키텍처로 진화했다.

---

### Ⅰ. 개요 (Context & Background)
운영 시스템(OLTP)은 트랜잭션 처리에 최적화되어 있어 복잡한 분석 쿼리에는 부적합하다. 데이터 웨어하우스는 빌 인먼(Bill Inmon)과 랄프 킴벌(Ralph Kimball)의 이론을 바탕으로, 과거부터 현재까지의 데이터를 분석하기 좋은 형태로 통합하여 기업의 전략적 의사결정을 돕는 기술이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데이터 웨어하우스는 ETL 과정을 통해 원천 시스템에서 데이터를 가져와 전용 저장소에 적재한다.

```text
[ Data Warehouse Architecture / 데이터 웨어하우스 아키텍처 ]

    Source Systems (ERP, CRM)          Data Warehouse (DW)             BI & Analytics
    +-------------------+       +-----------------------+       +-------------------+
    | [Operational DB]  |       |     [Staging Area]    |       |  Reporting Tools  |
    | [Flat Files]      | ----> |     [Data Vault]      | ----> |  (SQL, Dashboards)|
    | [External API]    |       +-----------+-----------+       +---------+---------+
    +---------+---------+                   |                             |
                                            v                             v
                                +-----------+-----------+       +---------+---------+
                                |      Data Marts       | ----> |  Ad-hoc Analysis  |
                                | (Sales, Finance, etc) |       |  (Excel, BI)      |
                                +-----------------------+       +-------------------+
```

1. <strong>4대 특징 (Inmon)</strong>:
   - **주제 중심적 (Subject Oriented)**: 고객, 상품 등 특정 주제별 데이터 구성.
   - **통합적 (Integrated)**: 전사의 데이터를 표준화된 포맷으로 통합.
   - **시계열적 (Time Variant)**: 과거의 이력 데이터를 보존.
   - **비휘발성 (Non-volatile)**: 한 번 적재된 데이터는 삭제되지 않음.
2. **모델링**: 스타 스키마(Star Schema)와 눈송이 스키마(Snowflake Schema)를 사용하여 분석 속도를 최적화한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 데이터 웨어하우스 (DW) | 운영 데이터베이스 (OLTP) |
| :--- | :--- | :--- |
| **주요 목적** | 의사결정 지원 및 분석 | 일상적 트랜잭션 처리 |
| <strong>데이터 범위</strong> | 과거 이력 포함 (수년) | 현재 상태 위주 (수개월) |
| **작업 단위** | 복잡한 대량의 쿼리 | 작고 빠른 트랜잭션 |
| **핵심 기술** | OLAP, MPP, Columnar Storage | SQL, Indexing, Normalization |

---

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
1. **MPP 아키텍처**: 최신 클라우드 DW(Snowflake, BigQuery)는 수많은 컴퓨팅 노드를 병렬로 사용하여 수조 건의 데이터를 초 단위로 쿼리한다.
2. **ELT의 부상**: 클라우드 DW의 강력한 연산력을 활용하기 위해 정제 작업을 DW 내부에서 수행하는 ELT(Extract, Load, Transform) 방식이 선호된다.
3. **실무 관점의 판단**: DW는 품질이 검증된 'Single Source of Truth'여야 한다. 데이터 정합성(Consistency)과 계보 관리가 뒷받침되지 않으면 신뢰할 수 없는 분석 결과를 낳게 된다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데이터 웨어하우스는 사라지지 않고 데이터 레이크와 결합하여 '데이터 레이크하우스'로 진화하고 있다. 정형 데이터의 정밀함과 비정형 데이터의 방대함을 동시에 아우르는 하이브리드 전략이 향후 기업 데이터 아키텍처의 표준이 될 것이며, 이는 AI 기반의 자동화된 통찰(Augmented Analytics)을 이끌어낼 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Data Infrastructure, Business Intelligence
- **하위 개념**: Data Mart, ETL/ELT, Star Schema, OLAP
- **연관 개념**: OLTP vs OLAP, MPP, Data Lakehouse

---

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: Data Infrastructure, Business Intelligence]
    |
    v
[하위 개념: Data Mart, ETL/ELT, Star Schema, OLAP]
    |
    v
[연관 개념: OLTP vs OLAP, MPP, Data Lakehouse]
```

이 흐름도는 상위 개념: Data Infrastructure, Business Intelligence에서 출발해 연관 개념: OLTP vs OLAP, MPP, Data Lakehouse까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>데이터 웨어하우스</strong>: 학교 도서관에서 책들을 종류별(과학, 소설)로 아주 깔끔하게 정리해둔 책장과 같아요.
2. **정확함**: 이름표가 정확하게 붙어 있어서, 내가 원하는 정보를 아주 빠르게 찾을 수 있어요.
3. **용도**: "지난달에 대출이 가장 많았던 책이 뭐지?" 같은 어려운 질문에 대답할 때 최고예요.
