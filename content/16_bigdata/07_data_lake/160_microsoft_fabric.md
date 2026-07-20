---
title: "Microsoft Fabric"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 160
---
## 핵심 인사이트 (3줄 요약)
1. Microsoft Fabric(2023)은 OneLake를 중심으로 Power BI·Azure Synapse·Azure Data Factory·Azure Databricks·Real-Time Analytics를 단일 SaaS 플랫폼으로 통합하여, <strong>전사 데이터를 하나의 논리적 데이터 레이크</strong>에서 관리한다.
2. <strong>OneLake</strong>는 조직 전체를 위한 단일 ADLS (Azure Data Lake Storage) Gen2 기반 데이터 레이크로, Shortcuts 기능을 통해 데이터를 물리적으로 복사하지 않고 다른 저장소의 데이터를 가상으로 참조할 수 있다.
3. Fabric SKU(F4~F2048)가 Power BI Premium, Azure Synapse, Data Factory 등 개별 서비스 라이선스를 대체하여 <strong>단일 용량 과금 모델</strong>로 TCO (Total Cost of Ownership) 최적화를 실현한다.

---

## Ⅰ. 개요 및 필요성

Microsoft의 데이터 서비스는 Azure Synapse Analytics, Azure Data Factory, Power BI, Azure Databricks, Azure Data Lake Storage 등이 각각 독립적으로 운영되어, 조직이 여러 서비스를 개별 계약·관리해야 하는 복잡성이 있었다. 데이터 사일로(Data Silo) 문제도 심각하여, 부서마다 별도 스토리지에 동일한 데이터를 중복 보관하는 경우가 빈번했다.

Microsoft Fabric은 이 분산된 Azure 데이터 서비스를 단일 SaaS 플랫폼으로 통합하며, OneLake라는 단일 조직 데이터 저장소가 모든 서비스의 스토리지 레이어를 공유한다.

| 기존 Azure 데이터 스택 | Microsoft Fabric |
|:---|:---|
| Azure Synapse Analytics | Fabric Synapse Data 엔진ering |
| Azure Data Factory | Fabric Data Factory |
| Power BI Premium | Fabric Power BI |
| Azure Data Lake Storage | OneLake (Fabric 내장) |
| Azure Machine Learning | Fabric Data Science |
| 개별 서비스 라이선스 | 단일 Fabric SKU |

> 📢 **섹션 요약 비유**: Fabric 이전은 각기 다른 회사의 앱(Word, Excel, PowerPoint)을 따로 구매하던 시절이었다면, Fabric은 Microsoft 365처럼 모든 데이터 서비스를 하나의 구독으로 통합한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|               Microsoft Fabric 아키텍처                           |
+------------------------------------------------------------------+
|                                                                  |
|  +---------------------------------------------------------+    |
|  |                Fabric 경험(Experience) 레이어              |    |
|  |                                                          |    |
|  |  Data       Data       Data      Power   Real-Time      |    |
|  |  Engineering Factory   Science   BI      Analytics       |    |
|  |  (Spark)    (Pipeline) (ML)      (Report)(Eventstream)  |    |
|  +--------------------+------------------------------------+    |
|                       |                                         |
|  +--------------------v------------------------------------+    |
|  |                OneLake (통합 스토리지)                    |    |
|  |                                                          |    |
|  |  +--------------------------------------------------+   |    |
|  |  |  조직 전체 단일 ADLS Gen2 인스턴스                  |   |    |
|  |  |  workspace1/  workspace2/  workspace3/            |   |    |
|  |  |  (테넌트당 하나)                                   |   |    |
|  |  +--------------------------------------------------+   |    |
|  |                                                          |    |
|  |  +---------------+   +-----------------------------+   |    |
|  |  |  Shortcuts    |   |  Delta Parquet 형식 (기본)   |   |    |
|  |  |  (가상 링크)   |   |  Iceberg 지원 (2024~)       |   |    |
|  |  |  AWS S3       |   |                             |   |    |
|  |  |  GCS          |   |  OneCopy: 단일 물리 복사본   |   |    |
|  |  |  Azure Blob   |   |  로 모든 서비스가 공유 접근  |   |    |
|  |  +---------------+   +-----------------------------+   |    |
|  +----------------------------------------------------------+    |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |  Fabric Capacity (SKU: F4~F2048)                           |  |
|  |  - 단일 용량 단위로 모든 경험 레이어 컴퓨팅 공유            |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

**핵심 구성 요소 상세**

| 구성 요소 | 역할 | 핵심 특징 |
|:---|:---|:---|
| OneLake | 통합 스토리지 | 조직당 하나, ADLS Gen2 기반, Delta 포맷 |
| Shortcuts | 가상 데이터 참조 | 복사 없이 S3/GCS/Azure Blob 데이터 접근 |
| Lakehouse | 데이터 엔지니어링 | Delta 기반 Bronze/Silver/Gold 구현 |
| Data Warehouse | SQL 분석 | 완전 관리형 SQL 웨어하우스 |
| Eventstream | 실시간 스트리밍 | Kafka 호환, Real-Time Analytics 연동 |
| Fabric Capacity | 과금 단위 | 모든 경험 공유 컴퓨팅 자원 |

> 📢 **섹션 요약 비유**: OneLake는 조직의 공용 하드드라이브다. 어느 부서(워크스페이스)의 어느 앱(경험)을 써도 같은 하드드라이브에서 파일을 읽고 쓰므로 중복 저장이 없다.

---

## Ⅲ. 비교 및 연결

**Fabric vs 경쟁 플랫폼 비교**

| 항목 | Microsoft Fabric | Databricks | Snowflake |
|:---|:---|:---|:---|
| 통합 범위 | BI + 데이터 엔지니어링 + ML + 스트리밍 | 데이터 엔지니어링 + ML | DW + 제한적 레이크 |
| BI 도구 | Power BI 내장 (최강) | Databricks SQL (제한적) | Tableau/Power BI 외부 연결 |
| ML/AI | Fabric Data Science | MLflow 최고 수준 | Snowpark ML |
| 스트리밍 | Eventstream (관리형) | Structured Streaming | Snowpipe |
| 과금 모델 | 단일 Capacity SKU | DBU 기반 | Credit 기반 |
| 멀티 클라우드 | Azure 중심 (AWS/GCS Shortcut) | 완전 멀티 클라우드 | 완전 멀티 클라우드 |

**OneLake와 Shortcuts 활용 패턴**

- **교차 워크스페이스 공유**: 다른 팀의 Lakehouse 테이블을 Shortcut으로 참조 (복사 없음)
- **레거시 연동**: Azure Blob이나 AWS S3의 기존 데이터를 Shortcut으로 즉시 연결
- <strong>멀티 클라우드 패브릭</strong>: GCS/S3 데이터를 OneLake에 Shortcut으로 포함, Fabric 경험 레이어로 분석

> 📢 **섹션 요약 비유**: OneLake Shortcuts는 Google Drive 공유 폴더와 같다. 다른 사람의 파일을 내 드라이브에 복사하지 않고 링크로 연결하면, 항상 최신 원본에 접근하면서 저장 공간은 쓰지 않는다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**Fabric 도입 의사 결정 기준**

- **Microsoft 친화 조직**: Power BI + Azure 스택 이미 사용 중인 기업에서 최적 ROI
- <strong>BI-데이터 통합 요구</strong>: 데이터 엔지니어링 결과를 즉시 Power BI로 시각화해야 할 때
- **비용 단순화**: 여러 Azure 서비스 라이선스를 Fabric 단일 SKU로 통합할 때
- **레거시 현대화**: Azure Synapse/ADF를 Fabric으로 마이그레이션하는 로드맵

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| OneLake 핵심 원칙 | 조직당 단일 ADLS Gen2, OneCopy (단일 물리 복사본) |
| Shortcuts 동작 원리 | 가상 링크로 외부 스토리지를 OneLake 네임스페이스에 연결, 복사 없음 |
| Fabric SKU 특징 | F4~F2048, CU(컴퓨팅 단위) 공유로 모든 경험 레이어 동시 실행 |
| Fabric vs Azure Synapse | Fabric = 통합 SaaS 플랫폼, Synapse = 개별 서비스 (마이그레이션 대상) |

> 📢 **섹션 요약 비유**: Fabric 도입은 오피스텔에서 사무실 건물로 이사하는 것이다. 개별 방(Azure 서비스)을 따로 빌리던 것을 하나의 건물(Fabric)로 통합하여 복도(OneLake)를 공유하고 관리비(라이선스)를 절감한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 데이터 사일로 해소 | OneLake로 부서별 중복 스토리지 통합 |
| TCO 절감 | 개별 서비스 라이선스 -> 단일 Fabric SKU |
| 분석 속도 향상 | 데이터 엔지니어링->BI를 같은 플랫폼에서 즉시 연결 |
| 거버넌스 일원화 | Microsoft Purview 통합으로 OneLake 전체 데이터 거버넌스 |

Microsoft Fabric은 2023년 GA(General Availability) 이후 Microsoft 최대 데이터 플랫폼 투자로 주목받고 있다. Power BI 기반 조직과 Azure 중심 기업에서 가장 빠른 도입 속도를 보이며, Databricks·Snowflake와의 3파전이 빅데이터 플랫폼 시장의 핵심 경쟁 구도를 형성한다. 심화 학습에서는 **OneLake 원칙(조직당 단일 레이크)**, **Shortcuts 메커니즘**, <strong>Fabric SKU 과금 모델</strong>이 핵심 논점이다.

> 📢 **섹션 요약 비유**: Microsoft Fabric은 데이터 세계의 Microsoft 365다. Word·Excel·PowerPoint가 Office 365로 통합됐듯, Synapse·ADF·Power BI·Data Science가 하나의 플랫폼으로 통합되어 데이터 업무의 모든 순간을 연결한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| OneLake | 핵심 스토리지 | 조직당 단일 ADLS Gen2, OneCopy |
| Shortcuts | 가상 참조 | 데이터 복사 없는 외부 스토리지 연결 |
| Fabric Capacity | 과금 단위 | F4~F2048 SKU, 모든 경험 공유 |
| Lakehouse (Fabric) | 데이터 엔지니어링 | Delta 기반, Notebooks, Spark |
| Eventstream | 실시간 처리 | Kafka 호환 스트리밍 |
| Microsoft Purview | 거버넌스 통합 | OneLake 전체 데이터 카탈로그·리니지 |

---


### 📈 관련 키워드 및 발전 흐름도

```text
[분산 데이터 웨어하우스 (Distributed DW) — 구조화 데이터, SQL 중심]
    |
    v
[데이터 레이크 (Data Lake) — 비정형·반정형 포함, 스키마 온 리드]
    |
    v
[Azure Synapse Analytics — DW + Lake 통합, SQL + Spark 혼용]
    |
    v
[Microsoft Fabric — OneLake 단일 저장소, 통합 SaaS 분석 플랫폼]
    |
    v
[Lakehouse 아키텍처 (Delta Lake / OneLake) — ACID + 분석 통합 표준화]
```
Microsoft Fabric은 OneLake라는 단일 저장소 위에 데이터 엔지니어링·과학·BI를 통합한 SaaS 분석 플랫폼으로, Lakehouse 아키텍처의 완성형이다.
### 👶 어린이를 위한 3줄 비유 설명
1. Microsoft Fabric은 학교의 모든 과목(데이터 수집, 분석, ML, 보고서)을 하나의 교실(Fabric)에서 배우는 통합 수업이에요.
2. OneLake는 반 전체가 쓰는 공용 책장이에요. 모두가 같은 책(데이터)을 쓰니 똑같은 책을 여러 권 살 필요가 없어요.
3. Shortcut은 다른 반 책장의 책을 우리 반에서도 볼 수 있게 해주는 도서관 링크 시스템이에요 (복사 없이 원본 그대로).
