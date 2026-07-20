---
title: "Data Lake"
date: "2024-05-22"
tags:
  - "studynote-bigdata"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
1. 정형, 반정형, 비정형 데이터를 포함한 방대한 원시 데이터(Raw Data)를 목적에 관계없이 <strong>원래의 형식 그대로 저장</strong>하는 거대 저장소이다.
2. 저장 시점에 스키마를 정의하지 않는 <strong>스키마 온 리드(Schema-on-Read)</strong> 방식을 사용하여 데이터 수집의 유연성과 저비용성을 극대화한다.
3. 데이터 웨어하우스(DW)의 폐쇄성을 극복하고 빅데이터 분석 및 머신러닝을 위한 통합 기반 인프라 역할을 수행한다.

---

### Ⅰ. 개요 (Context & Background)
기존의 데이터 웨어하우스는 데이터를 저장하기 전에 엄격하게 정제하고 구조화해야 했기에 비정형 데이터 처리에 한계가 있었다. 데이터 레이크는 저렴한 클라우드 스토리지(S3, HDFS)를 활용하여 일단 모든 데이터를 '호수'에 쏟아부은 뒤, 분석가가 필요할 때 꺼내서 가공할 수 있게 하는 패러다임의 전환을 가져왔다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데이터 레이크는 수집(Ingest), 저장(Store), 가공(Process), 소비(Consume)의 4단계 아키텍처를 가진다.

```text
[ Data Lake Architecture / 데이터 레이크 아키텍처 ]

    Sources (Log, IoT, DB)         Data Lake (S3, HDFS)            Analysis & ML
    +-------------------+       +-----------------------+       +-------------------+
    | [Structured]      |       |  Landing / Raw Zone   |       |   BI Dashboards   |
    | [Semi-structured] | ----> |  (Schema-on-Read)     | ----> |   (Tableau, PBI)  |
    | [Unstructured]    |       +-----------+-----------+       +---------+---------+
    +---------+---------+                   |                             |
                                            v                             v
                                +-----------+-----------+       +---------+---------+
                                |  Curated / Gold Zone  | ----> |  Machine Learning |
                                |  (Processed Data)     |       |  (PyTorch, Spark) |
                                +-----------------------+       +-------------------+
```

1. <strong>스키마 온 리드 (Schema-on-Read)</strong>: 데이터를 읽을 때 구조를 부여한다. (유연성 극대화)
2. **비용 효율성**: 범용 x86 서버나 저가형 객체 스토리지를 사용하여 DW 대비 약 1/10 이하의 비용으로 저장 가능하다.
3. **거버넌스 필수**: 데이터 카탈로그와 메타데이터 관리가 없으면 '데이터 늪(Data Swamp)'으로 전락할 위험이 크다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 데이터 웨어하우스 (DW) | 데이터 레이크 (Data Lake) |
| :--- | :--- | :--- |
| <strong>데이터 형태</strong> | 정형 (Structured) | 모든 형태 (Raw Format) |
| <strong>스키마 방식</strong> | Schema-on-Write (저장 시 정의) | Schema-on-Read (읽을 때 정의) |
| **사용자** | 비즈니스 분석가 (BI) | 데이터 과학자, 엔지니어 |
| **저장 비용** | 비쌈 (고성능 스토리지) | 저렴함 (Object Storage) |

---

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
1. <strong>메들리온 아키텍처 (Medallion Architecture)</strong>: 데이터를 Bronze(원시), Silver(정제), Gold(집계) 계층으로 나누어 관리함으로써 데이터 품질을 보장해야 한다.
2. <strong>델타 레이크(Delta Lake) 도입</strong>: 데이터 레이크의 한계인 트랜잭션(ACID) 부재를 해결하기 위해 오픈 테이블 포맷을 도입하여 '데이터 레이크하우스'로 진화하는 추세다.
3. **실무 관점의 판단**: 데이터 레이크는 분석의 자유도를 높이지만 보안과 권한 관리가 매우 까다롭다. AWS Lake Formation 같은 도구를 통해 미세 권한 제어(Fine-grained access control)를 반드시 구축해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데이터 레이크는 현대 기업의 디지털 자산 창고이다. 향후에는 물리적으로 흩어진 레이크들을 연결하는 데이터 패브릭(Data Fabric)과 분산된 거버넌스를 지향하는 데이터 메시(Data Mesh)로 발전할 것이며, 이는 AI/ML 기반의 의사결정을 가속화하는 핵심 동력이 될 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Big Data Architecture, Data Infrastructure
- **하위 개념**: S3, HDFS, Azure Data Lake Store (ADLS)
- **연관 개념**: Data Swamp, Schema-on-Read, Medallion Architecture, Lakehouse

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Data Warehouse]
    |
    v
[Data Lake]
    |
    v
[Schema-on-Read]
    |
    v
[Lakehouse]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>데이터 레이크</strong>: 세상의 모든 장난감을 일단 거대한 창고에 다 넣어두는 거예요.
2. **유연함**: 나중에 "로봇만 가지고 놀래!"라고 할 때 그제서야 로봇을 골라내서 노는 방식이에요.
3. **주의사항**: 정리를 안 하고 막 던져넣기만 하면 나중에 원하는 걸 찾을 수 없는 '쓰레기산'이 될 수 있어요.
