+++
title = "인덱싱 및 성능 최적화"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# 인덱싱 및 성능 최적화

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인덱스는 데이터 검색 속도를 획기적으로 향상시키기 위해 별도의 저장 공간을 할당하여 구축하는 부가적인 데이터 구조로, B+Tree가 관계형 DBMS의 표준이다.
> 2. **가치**: 적절한 인덱스 설계는 풀 테이블 스캔(Full Table Scan)을 인덱스 레인지 스캔(Index Range Scan)으로 변환하여 디스크 I/O를 수십~수천 배 감소시키며, 쿼리 응답 시간을 밀리초 단위로 단축한다.
> 3. **융합**: 인덱스 튜닝은 옵티마이저 이해, 통계 정보 분석, 클러스터링 팩터, 선택도, 카디널리티 등 다양한 요소를 종합적으로 고려해야 하며, 과도한 인덱스는 DML 성능 저하를 초래한다.

---

### 학습 키워드 목록

#### 인덱스 구조
- B-Tree 인덱스 - 다진 탐색 트리 원리
- B+Tree 인덱스 - 리프 노드 연결 리스트, RDBMS 표준
- 해시 인덱스 - 동등 검색 최적화, 범위 검색 불가
- 비트맵 인덱스 - 낮은 분포도 컬럼에 적합
- 클러스터드 인덱스 - 물리적 정렬, 테이블당 1개
- 넌클러스터드 인덱스 - 보조 인덱스, 포인터 참조

#### 인덱스 설계
- 결합 인덱스 (Composite Index) - 선행 컬럼 순서
- 함수 기반 인덱스 (FBI)
- 커버링 인덱스 - Include Column
- 전역/지역 인덱스 (파티션 환경)

#### 성능 분석
- 실행 계획 (Execution Plan) 해석
- 선택도 (Selectivity), 카디널리티 (Cardinality)
- 클러스터링 팩터 (Clustering Factor)
- 인덱스 스캔 유형 - Range Scan, Fast Full Scan, Skip Scan
- 힌트 (Hint) 활용
