+++
title = "NoSQL 및 NewSQL"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# NoSQL 및 NewSQL

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL(Not Only SQL)은 스키마리스(Schemaless), 수평적 확장(Scale-out), 분산 아키텍처를 특징으로 하여 대량의 비정형 데이터 처리와 고가용성을 목표로 하는 데이터베이스 패러다임이다.
> 2. **가치**: 키-값, 문서, 컬럼 패밀리, 그래프 등 다양한 데이터 모델을 제공하여 사용 사례에 최적화된 저장소 선택이 가능하며, NewSQL은 RDBMS의 ACID와 NoSQL의 수평 확장성을 결합한다.
> 3. **융합**: 폴리글랏 퍼시스턴스(Polyglot Persistence) 전략으로 마이크로서비스별 최적 DB를 혼용하고, CAP 이론과 결과적 일관성 모델을 이해한 설계가 필수적이다.

---

### 학습 키워드 목록

#### NoSQL 데이터 모델
- [274. NoSQL 개요](./274_nosql_overview.md) - 정의, 특징, 등장 배경
- 키-값 저장소 - Redis, Memcached, DynamoDB
- 문서 저장소 - MongoDB, CouchDB (JSON/BSON)
- 컬럼 패밀리 저장소 - HBase, Cassandra
- 그래프 저장소 - Neo4j, Amazon Neptune

#### 분산 아키텍처
- 샤딩 (Sharding) - 수평 파티셔닝
- 일관된 해싱 (Consistent Hashing)
- 복제 (Replication) - 동기식/비동기식
- CAP 정리와 PACELC
- 결과적 일관성 (Eventual Consistency)
- BASE 속성

#### 주요 NoSQL 제품
- Redis - 인메모리 데이터 구조, 영속성 옵션
- MongoDB - 레플리카 셋, 샤드 클러스터
- Cassandra - 링 구조, 가십 프로토콜, 튜너블 컨시스턴시
- Elasticsearch - 역색인, 분산 검색 엔진

#### NewSQL
- Google Spanner - 트루타임(TrueTime)
- CockroachDB - 생존성 극대화
- TiDB - HTAP 지원
- 클라우드 네이티브 데이터베이스
