+++
title = "SQL 및 옵티마이저"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# SQL 및 옵티마이저

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL(Structured Query Language)은 관계형 데이터베이스에서 데이터를 정의, 조작, 제어하기 위한 선언적 표준 언어이며, 옵티마이저는 이를 가장 효율적인 실행 계획으로 변환하는 DBMS의 핵심 엔진이다.
> 2. **가치**: 선언적 SQL과 비용 기반 옵티마이저(CBO)의 결합은 개발자가 "무엇을 원하는가"만 명시하면 DBMS가 "어떻게 최적으로 수행할까"를 자동으로 판단하게 하여 생산성과 성능을 동시에 확보한다.
> 3. **융합**: SQL 최적화는 통계 정보, 인덱스 구조, 조인 알고리즘, 메모리 관리 등 DBMS 내부 아키텍처 전반의 이해를 요구하며, 쿼리 튜닝은 기술사 필수 역량이다.

---

### 학습 키워드 목록

#### SQL 기본 및 조인
- [131. SQL 표준](./131_sql_standard.md) - ANSI/ISO SQL 표준
- [132. 내부 조인](./132_inner_join.md) - Inner Join, Equi Join, Natural Join
- 외부 조인 - Left/Right/Full Outer Join
- 서브쿼리 - Inline View, Scalar Subquery, Correlated Subquery
- 윈도우 함수 - RANK, DENSE_RANK, ROW_NUMBER, LEAD, LAG
- 집합 연산자 - UNION, UNION ALL, INTERSECT, MINUS

#### 인덱스 및 옵티마이저
- 인덱스 기본 - B+Tree, Hash, Bitmap 인덱스
- 클러스터드/넌클러스터드 인덱스
- 옵티마이저 - RBO vs CBO
- 실행 계획 분석
- 조인 기법 - NL Join, Sort Merge Join, Hash Join
- 파티셔닝 - Range, Hash, List Partitioning
