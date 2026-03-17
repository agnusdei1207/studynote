+++
title = "466. 도큐먼트 DB와 MongoDB - 유연한 그릇의 미학"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 466
+++

# 466. 도큐먼트 DB와 MongoDB - 유연한 그릇의 미학

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 도큐먼트 데이터베이스(Document Database)는 데이터를 행과 열의 2차원 표(Table)가 아닌, **JSON(JavaScript Object Notation) 및 BSON(Binary JSON) 형태의 계층적 문서(Document)로 저장**하여 데이터의 자체 기술성(Self-describing)을 극대화하는 비관계형 데이터베이스(NoSQL)입니다.
> 2. **가치**: 사전에 스키마가 고정되지 않는 **스키마리스(Schema-less)** 특성으로 애자일 개발(Agile Development) 단계의 유연성을 제공하며, **중첩(Embedding)**을 통해 연관 데이터를 통합 저장하여 RDBMS(Relational DBMS)의 조인(Join) 연산 비용을 제거하고 조회 성능을 획기적으로 향상시킵니다.
> 3. **융합**: 객체 지향 프로그래밍(OOP)의 객체 모델과 1:1로 매핑되는 데이터 구조를 통해 ORM(Object-Relational Mapping)의 패러다임 임피던스 불일치 문제를 해결하며, ** 샤딩(Sharding)**을 통한 수평 확장(Horizontal Scaling)으로 대용량 트래픽 처리를 실현합니다.

---

### Ⅰ. 개요 (Context & Background)
