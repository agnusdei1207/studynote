---
title: "Databricks Platform"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 158
---
## 핵심 인사이트 (3줄 요약)
1. Databricks는 Apache Spark 창시자들이 설립한 회사로, Delta Lake·Unity Catalog·MLflow·Photon 엔진을 통합한 <strong>레이크하우스 올인원 플랫폼</strong>을 제공하며 컴퓨팅 네이티브(Compute-Native) 아키텍처로 차별화된다.
2. <strong>Photon 엔진</strong>은 C++ 기반 벡터화 쿼리 엔진으로 기존 Spark 대비 SQL 워크로드에서 최대 8배 성능을 달성하며, <strong>Auto Scaling</strong> 클러스터가 워크로드에 따라 노드를 자동으로 조정한다.
3. AWS·Azure·GCP 모두에서 동일한 API로 동작하는 멀티 클라우드 전략과, SQL 친화적 Snowflake와 코드 친화적 Databricks의 포지셔닝 차별화가 핵심 시장 대립 구도를 형성한다.

---

## Ⅰ. 개요 및 필요성

Apache Spark는 뛰어난 성능에도 불구하고 클러스터 설정, 라이브러리 호환성, ML 실험 관리, 데이터 거버넌스를 모두 직접 구성해야 하는 운영 복잡성이 있었다. Databricks는 이 모든 요소를 통합 플랫폼으로 제공하여, 데이터 엔지니어·데이터 과학자·BI 분석가가 하나의 환경에서 협업할 수 있게 한다.

Databricks Lakehouse Platform은 Delta Lake(저장), Unity Catalog(거버넌스), MLflow(ML 수명 주기), Workflows(오케스트레이션), SQL Analytics(BI)를 단일 통합 환경으로 제공한다.

| 이전 환경 (분산 도구) | Databricks 통합 |
|:---|:---|
| Hadoop + Spark 자체 클러스터 | 관리형 Spark 클러스터 |
| Hive + 별도 DW | Delta Lake 단일 스토리지 |
| 개별 ML 도구 (Jupyter 등) | MLflow + Feature Store |
| 별도 오케스트레이터 (Airflow) | Databricks Workflows |
| 별도 BI 도구 연결 | Databricks SQL + Serverless |

> 📢 **섹션 요약 비유**: Databricks는 스위스 아미 나이프다. 데이터 처리(Spark), ML 실험(MLflow), SQL 분석(Databricks SQL), 거버넌스(Unity Catalog)가 하나의 손잡이에 모두 달려 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|               Databricks Lakehouse Platform                       |
+------------------------------------------------------------------+
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              사용자 인터페이스 레이어                      |    |
|  |  Notebooks | Databricks SQL | ML Experiments | Workflows |    |
|  +---------------------------------------------------------+    |
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              컴퓨팅 레이어                                |    |
|  |  +--------------+  +--------------+  +--------------+   |    |
|  |  | All-Purpose  |  | Job Cluster  |  |  SQL          |   |    |
|  |  | Cluster      |  |  (배치 전용) |  |  Warehouse   |   |    |
|  |  | (개발/탐색)   |  |              |  |  (BI 전용)   |   |    |
|  |  +--------------+  +--------------+  +--------------+   |    |
|  |           Apache Spark + Photon Engine (C++ 벡터화)      |    |
|  +---------------------------------------------------------+    |
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              데이터/ML 레이어                              |    |
|  |  Delta Lake | Unity Catalog | MLflow | Feature Store     |    |
|  +---------------------------------------------------------+    |
|                                                                  |
|  +---------------------------------------------------------+    |
|  |              클라우드 스토리지 레이어                      |    |
|  |   AWS S3  |  Azure ADLS Gen2  |  Google Cloud Storage    |    |
|  +---------------------------------------------------------+    |
+------------------------------------------------------------------+
```

**핵심 제품·기능 상세**

| 제품/기능 | 역할 | 핵심 특징 |
|:---|:---|:---|
| Delta Lake | 저장 포맷 | ACID, 타임 트래블, Z-ORDER |
| Unity Catalog | 거버넌스 | 3계층 네임스페이스, Fine-Grained AC |
| MLflow | ML 수명 주기 | 실험 추적, 모델 레지스트리, 서빙 |
| Photon 엔진 | 쿼리 성능 | C++ 벡터화, SQL 최대 8배 가속 |
| Databricks SQL | BI 쿼리 | 서버리스 SQL 웨어하우스 |
| Workflows | 오케스트레이션 | DAG 기반 작업 의존성 관리 |
| AutoML | ML 자동화 | 자동 피처 엔지니어링·하이퍼파라미터 |
| Delta Live Tables | 파이프라인 | 선언적 스트리밍·배치 통합 파이프라인 |

> 📢 **섹션 요약 비유**: Photon 엔진은 자동차의 터보 엔진이다. 같은 도로(쿼리)를 달려도 기존 Spark(일반 엔진)보다 훨씬 빠르게 목적지(결과)에 도달한다.

---

## Ⅲ. 비교 및 연결

<strong>Databricks vs Snowflake — 핵심 대립 구도</strong>

| 항목 | Databricks | Snowflake |
|:---|:---|:---|
| 핵심 포지셔닝 | 코드 네이티브 (Python/Spark 중심) | SQL 네이티브 (ANSI SQL 중심) |
| ML/AI 지원 | 최고 수준 (MLflow, AutoML 내장) | Snowpark ML (2023~) |
| 스토리지 방식 | 오픈 포맷 (Delta/Iceberg on 객체 스토리지) | 독점 스토리지 포맷 |
| 스트리밍 | Spark Structured Streaming + DLT | Snowpipe (마이크로 배치) |
| 가격 모델 | DBU (Databricks Unit) 기반 | Credit 기반 |
| 주 사용자 | 데이터 엔지니어, ML 엔지니어 | SQL 분석가, BI 개발자 |
| 벤더 독립성 | 오픈 포맷 (Delta/Iceberg) | 높은 벤더 종속성 |

**연관 기술 연결**

- <strong>MLflow</strong>: Databricks에서 인큐베이션, 현재 LF AI&Data 재단 기증
- <strong>Delta Lake</strong>: Linux Foundation 기증, 벤더 중립화
- <strong>Apache Spark</strong>: Databricks 창업자들이 UC Berkeley AMPLab에서 개발

> 📢 **섹션 요약 비유**: Databricks는 종합 연구소(데이터 처리+ML+SQL 올인원)이고, Snowflake는 최고급 SQL 레스토랑(SQL에 특화)이다. 요리사(데이터 엔지니어)에게는 연구소가, 식품 분석가(BI 분석가)에게는 레스토랑이 더 편하다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**클러스터 유형별 최적 사용 시나리오**

| 클러스터 유형 | 특징 | 사용 시나리오 |
|:---|:---|:---|
| All-Purpose Cluster | 상시 실행, 협업 | 탐색적 분석, 개발·디버깅 |
| Job Cluster | 작업 시작 시 생성, 완료 후 종료 | 운영 배치 파이프라인 |
| SQL Warehouse | 서버리스 SQL 최적화 | BI 도구 연결, SQL 분석 |
| Instance Pools | 미리 워밍업된 VM | 빠른 클러스터 시작 필요 시 |

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Databricks 핵심 제품 구성 | Delta Lake + Unity Catalog + MLflow + Photon + Workflows |
| Photon 엔진 원리 | C++ 기반 벡터화 실행, JVM 오버헤드 제거, SIMD 활용 |
| Databricks vs Snowflake | Databricks = 코드 네이티브/ML, Snowflake = SQL 네이티브/BI |
| DBU(Databricks Unit) | 클러스터 유형·크기에 따른 가격 단위, 시간당 소비량 |

> 📢 **섹션 요약 비유**: Databricks 선택은 팀 구성에 따라 달라진다. Python/ML 중심 팀이라면 Databricks가 고향이고, SQL BI 중심 팀이라면 Snowflake가 더 자연스럽다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 통합 플랫폼 효율 | 여러 도구 연동 설정 제거, 단일 보안·거버넌스 |
| ML 가속 | MLflow·Feature Store로 ML 실험->배포 사이클 단축 |
| 비용 최적화 | Auto Scaling + Spot 인스턴스 + 작업 완료 종료 |
| 오픈 포맷 | Delta/Iceberg로 벤더 종속 최소화 |

Databricks는 2023년 기준 기업 가치 430억 달러로 평가되며, 2024년 IPO를 준비 중인 빅데이터 AI 플랫폼의 선두 기업이다. 레이크하우스 아키텍처의 레퍼런스 구현체로서 기업 데이터 플랫폼 표준에 가장 가까이 있다. 심화 학습에서는 <strong>Databricks 핵심 제품 구성</strong>, <strong>Photon 엔진 특성</strong>, <strong>Snowflake와의 포지셔닝 비교</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Databricks는 데이터 팀의 슈퍼 앱이다. 한 앱에서 데이터 수집·처리·ML·분석·시각화를 모두 처리하듯, 하나의 플랫폼에서 데이터 파이프라인부터 AI 모델 배포까지 완결된다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Delta Lake | 저장 레이어 | Databricks 핵심 오픈소스 기여 |
| Unity Catalog | 거버넌스 레이어 | 3계층 네임스페이스, 리니지 |
| MLflow | ML 수명 주기 | 실험·레지스트리·서빙 통합 |
| Photon 엔진 | 성능 가속 | C++ 벡터화, SQL 8배 향상 |
| DBU | 가격 단위 | 클러스터 유형별 시간당 단가 |
| Databricks SQL | BI 레이어 | 서버리스 SQL 웨어하우스 |

---


### 📈 관련 키워드 및 발전 흐름도

```text
[Apache Spark — 인메모리 분산 처리 엔진, 배치·스트림 통합]
    |
    v
[Databricks (Managed Spark) — Spark 완전 관리형 클라우드 플랫폼, 자동 최적화]
    |
    v
[Delta Lake — ACID 트랜잭션·스키마 진화·타임 트래블 지원 오픈 테이블 포맷]
    |
    v
[레이크하우스 (Lakehouse) — 데이터 레이크의 유연성 + 데이터 웨어하우스의 ACID·성능 통합]
    |
    v
[Unity Catalog + MLflow — 데이터·모델 거버넌스 통합, 엔드투엔드 AI/ML 파이프라인]
```
이 흐름은 순수 Spark 엔진이 데이터 품질 보장의 한계를 드러내자 Delta Lake의 ACID가 이를 보완하고, 레이크하우스 아키텍처와 통합 거버넌스로 발전하는 Databricks 플랫폼의 진화 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Databricks는 모든 도구가 한 건물에 있는 연구소예요. 데이터 수집, 분석, AI 훈련을 한 곳에서 다 할 수 있어요.
2. Photon 엔진은 자동차 터보 장치처럼, 같은 일을 훨씬 빠르게 해주는 특별 엔진이에요.
3. Spark 만든 사람들이 세운 회사라 마치 요리사가 직접 차린 레스토랑처럼, 도구와 플랫폼이 딱 맞게 설계되어 있어요.
