+++
title = "데이터 웨어하우스 및 빅데이터"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# 데이터 웨어하우스 및 빅데이터

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 웨어하우스는 의사결정 지원을 위해 주제 중심, 통합, 시계열, 비휘발성 특성을 갖춘 분석 중심 저장소이며, OLAP 연산을 통해 다차원 분석을 가능하게 한다.
> 2. **가치**: ETL/ELT 파이프라인을 통해 운영 데이터를 분석 친화적 구조(스타/스노우플레이크 스키마)로 변환하고, 컬럼 기반 저장소와 MPP 아키텍처로 대용량 분석을 고속화한다.
> 3. **융합**: 데이터 레이크, 레이크하우스, 데이터 메시 등 최신 아키텍처는 정형/비정형 데이터 통합과 도메인 기반 분산 분석을 지향하며, 벡터 데이터베이스는 AI/LLM 시대의 핵심 인프라다.

---

### 학습 키워드 목록

#### 데이터 웨어하우스
- 데이터 웨어하우스 (DW) - 4대 특징
- 데이터 마트 (Data Mart) - 부서 중심
- ODS (Operational Data Store)
- ETL vs ELT 프로세스
- 스타 스키마, 스노우플레이크 스키마
- 팩트 테이블, 차원 테이블

#### OLAP
- OLAP 연산 - Roll-up, Drill-down, Slice, Dice, Pivot
- MOLAP, ROLAP, HOLAP
- 큐브 (Cube) 구조
- 다차원 모델링

#### 빅데이터 기술
- 데이터 레이크 - 스키마 온 리드
- Hadoop 생태계 - HDFS, MapReduce, Hive
- Spark - 인메모리 분산 처리
- Kafka/Flink - 스트림 처리

#### 최신 트렌드
- 데이터 레이크하우스 - Delta Lake, Iceberg
- 벡터 데이터베이스 - Milvus, Pinecone
- RAG (Retrieval-Augmented Generation)
- 데이터 메시 (Data Mesh)
- 데이터 패브릭 (Data Fabric)
