---
title: "Data Lake"
date: "2026-03-04"
tags:
  - "cloud_architecture"
  - "studynote-cloud-architecture"
weight: 219
---
## 핵심 인사이트 (3줄 요약)
- <strong>무제한 원시 데이터 저장:</strong> 정형(DB), 반정형(JSON, Log), 비정형(이미지, 영상) 데이터를 가공 없이 원본 그대로 대량 저장할 수 있는 중앙 저장소이다.
- <strong>스키마 온 리드 (Schema-on-Read):</strong> 데이터를 저장할 때 스키마를 정의하지 않고, 나중에 데이터를 읽어서 분석할 때 필요에 따라 구조를 입히는 유연한 방식이다.
- **클라우드 스토리지 기반:** 저렴한 클라우드 오브젝트 스토리지(AWS S3 등)를 활용하여 비용 효율적인 데이터 거버넌스를 구축할 수 있다.

### Ⅰ. 개요 (Context & Background)
데이터 레이크(Data Lake)는 기업의 흩어진 모든 데이터를 한곳에 모으는 거대한 저수지 역할을 한다. 기존의 데이터 웨어하우스(DW)가 정제된 데이터만을 담는 '생수통'이라면, 데이터 레이크는 흙탕물(Raw Data)까지도 모두 받아두었다가 필요할 때 정수해서 사용하는 철학을 가지고 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데이터 레이크는 수집(Ingest), 저장(Store), 처리(Process), 분석(Analyze)의 다계층 구조로 이루어진다.

```text
[ Architecture of Data Lake & Pipeline ]

   [ Data Sources ]       [ Data Lake Layers ]       [ Consumption ]
   +--------------+      +----------------------+      +--------------+
   | RDBMS (SQL)  |----->| Raw Layer (Landing)  |----->| Data Science |
   +--------------+      +----------------------+      +--------------+
   | Logs (JSON)  |----->| Standardized Layer   |----->| ML Modeling  |
   +--------------+      +----------------------+      +--------------+
   | Files (CSV)  |----->| Curated Layer (Gold) |----->| BI Dashboard |
   +--------------+      +----------------------+      +--------------+

* Storage: Object Storage (AWS S3, Azure Data Lake Storage)
* Metadata: Glue Catalog, Hive Metastore
* Processing: Spark, Presto, Athena
```

**핵심 메커니즘:**
1. <strong>Raw Layer:</strong> 원본 데이터가 변조 없이 적재되는 구간 (감사 로그용)
2. **Standardized Layer:** 데이터 형식을 Parquet/Avro 등으로 통일하고 메타데이터를 태깅한 구간
3. **Curated Layer:** 분석 목적에 맞게 조인/집계된 최종 정제 데이터 구간
4. **Decoupling:** 저장(Storage)과 연산(Compute)을 분리하여 자원을 독립적으로 확장한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 데이터 레이크 (Data Lake) | 데이터 웨어하우스 (Data Warehouse) |
| :--- | :--- | :--- |
| <strong>데이터 형태</strong> | 모든 데이터 (정형/반정형/비정형) | 정제된 정형 데이터 위주 |
| <strong>스키마 적용</strong> | 읽을 때 적용 (Schema-on-Read) | 저장할 때 적용 (Schema-on-Write) |
| **비용/확장성** | 낮음 / 무제한 확장 가능 | 높음 / 확장에 따른 비용 부담 큼 |
| **사용자** | 데이터 사이언티스트, ML 엔지니어 | 비즈니스 분석가, 현업 관리자 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
**실무 적용 사례:**
- <strong>IoT 센서 데이터 분석:</strong> 수만 개의 센서에서 쏟아지는 원시 로그를 S3에 일단 모두 담아두고, 필요한 지표만 스파크(Spark)로 분석한다.
- <strong>이미지/영상 AI 학습:</strong> 대량의 멀티미디어 파일을 데이터 레이크에 보관하며 딥러닝 모델의 학습 데이터셋으로 공급한다.

**실무적 판단:**
"데이터 레이크는 자칫 관리 소홀로 인해 <strong>데이터 늪(Data Swamp)</strong>으로 변질될 위험이 있다. 이를 방지하기 위해서는 강력한 <strong>메타데이터 카탈로그</strong>와 <strong>데이터 리니지(Lineage)</strong> 추적 기능이 필수적으로 병행되어야 한다."

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데이터 레이크는 빅데이터 분석과 AI 혁신의 핵심 기반이다. 최근에는 데이터 레이크의 유연성과 DW의 트랜잭션 성능을 결합한 <strong>데이터 레이크하우스(Data Lakehouse)</strong> 아키텍처로 진화하며 기업 데이터 플랫폼의 새로운 표준이 되고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- <strong>Data Swamp:</strong> 관리되지 않아 쓸 수 없게 된 데이터 레이크
- <strong>Object Storage:</strong> 데이터 레이크의 물리적 기반
- <strong>ETL vs ELT:</strong> 데이터 레이크 적재 시 ELT 방식 선호

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 레이크는 아주 큰 상자에 장난감, 책, 그림, 일기장을 몽땅 담아두는 '마법 상자'예요.

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS (구조화 데이터만 저장)
    |
    v
Data Lake: 비정형 + 정형 데이터 원시 저장
    +-► S3 · GCS · ADLS (오브젝트 스토리지)
    +-► Schema-on-Read: 읽을 때 스키마 적용
    |
    v
Data Lakehouse: Lake + Warehouse 통합 (Delta · Iceberg)
```
2. 예전에는 장난감 통, 책꽂이로 다 나눠야 했지만, 이제는 일단 상자에 다 넣어두고 나중에 놀고 싶을 때 꺼내서 정리하면 돼요.
3. 상자가 아주 커서 세상 모든 물건을 다 담아도 끄떡없답니다!
