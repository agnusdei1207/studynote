+++
title = "5. 데이터베이스"
description = "관계형 DB, NoSQL, 트랜잭션, 정규화, 분산 DB, 데이터 웨어하우스"
sort_by = "title"
weight = 5
+++

# 제5과목: 데이터베이스

데이터베이스 설계, 관리, 최적화의 핵심 개념을 다룹니다.

## 핵심 키워드

### DBMS 기초
- [DBMS](dbms.md) - 데이터베이스 관리 시스템
- [데이터 모델링](data_modeling.md) - ERD, 개념/논리/물리 모델
- [정규화](normalization.md) - 1NF~BCNF, 이상 현상 제거

### 관계형 데이터베이스
- [관계형 DB 기초](relational/relational_db.md) - 릴레이션, 키, 제약조건
- [SQL](relational/sql.md) - DDL, DML, DCL, TCL
- [인덱스](db_index.md) - B-Tree, Hash, 클러스터드 인덱스

### 트랜잭션 / 동시성
- [트랜잭션](transaction.md) - ACID 특성
- [동시성 제어](concurrency_control.md) - 잠금, MVCC, 직렬화
- [회복](recovery.md) - 로그, 체크포인트, REDO/UNDO

### 분산 / 고급 DB
- [분산 데이터베이스](distributed_database.md) - 복제, 샤딩, 2PC
- [NoSQL](nosql/nosql_overview.md) - MongoDB, Redis, Cassandra
- [데이터 웨어하우스](data_warehouse.md) - OLAP, Star/Snowflake 스키마
- [데이터 마이닝](data_mining.md) - 분류, 군집, 연관 규칙
