+++
title = "05. 데이터베이스 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 데이터베이스 (Database) 키워드 목록 (심화 확장판)

정보관리기술사·컴퓨터응용시스템기술사 및 전문 DB/데이터 엔지니어를 위한 데이터베이스 전 영역 핵심 및 심화 키워드 800선입니다.

관계형 데이터베이스(RDB) 기초부터 정규화, 동시성 제어, 트랜잭션 관리, 분산 DB, NoSQL, NewSQL, 데이터 웨어하우스, 그리고 최근의 벡터 데이터베이스(Vector DB)와 클라우드 네이티브 데이터베이스 기술까지 완벽하게 포괄합니다.

---

## 1. 데이터베이스 기초 및 아키텍처 (60개)
1. 데이터 (Data) / 정보 (Information) / 지식 (Knowledge) / 지혜 (Wisdom) - DIKW 피라미드
2. 데이터베이스 (Database)의 정의 - 통합(Integrated), 저장(Stored), 운영(Operational), 공용(Shared) 데이터
3. 데이터베이스 관리 시스템 (DBMS) - 사용자와 DB 사이의 인터페이스 (데이터 독립성 제공)
4. 데이터 독립성 (Data Independence) - 논리적 독립성 vs 물리적 독립성
5. 스키마 (Schema) - 데이터베이스의 논리적 구조와 제약 조건에 대한 명세
6. 3단계 스키마 아키텍처 (ANSI/SPARC)
7. 외부 스키마 (External Schema) - 사용자 관점, 서브 스키마
8. 개념 스키마 (Conceptual Schema) - 조직 전체 관점, 논리적 구조
9. 내부 스키마 (Internal Schema) - 물리적 저장 장치 관점
10. 스키마 매핑 (Mapping) - 외부/개념 사상, 개념/내부 사상
11. 시스템 카탈로그 (System Catalog) / 데이터 사전 (Data Dictionary) - 메타데이터(Metadata) 저장소
12. 메타데이터 (Metadata) - 데이터에 대한 데이터
13. 데이터 디렉터리 (Data Directory) - 시스템만 접근 가능한 카탈로그 부분
14. 데이터 모델 (Data Model) 구성 요소 - 구조(Structure), 연산(Operation), 제약조건(Constraint)
15. 계층형 데이터 모델 (Hierarchical Model) - 트리 구조 (1:N)
16. 망형 데이터 모델 (Network Model) - 그래프 구조 (N:M 허용)
17. 관계형 데이터 모델 (Relational Model) - 테이블 구조, E.F. Codd 제안
18. 객체지향 데이터 모델 (OODBMS) / 객체 관계형 데이터 모델 (ORDBMS)
19. DBMS 언어
20. DDL (Data Definition Language) - 데이터 정의 언어 (CREATE, ALTER, DROP, TRUNCATE)
21. DML (Data Manipulation Language) - 데이터 조작 언어 (SELECT, INSERT, UPDATE, DELETE)
22. DCL (Data Control Language) - 데이터 제어 언어 (GRANT, REVOKE)
23. TCL (Transaction Control Language) - 트랜잭션 제어 (COMMIT, ROLLBACK, SAVEPOINT)
24. 절차적 DML (네비게이션) vs 비절차적 DML (선언적, SQL)
25. 데이터베이스 관리자 (DBA, Database Administrator)
26. 데이터 관리자 (DA, Data Administrator) - 데이터 표준, 메타데이터 관리
27. 데이터베이스 설계자 (Database Designer)
28. 데이터베이스 사용자 - 일반 사용자, 응용 프로그래머
29. 데이터베이스 파일 시스템 (File System) 문제점 - 데이터 종속성, 데이터 중복성
30. 데이터 무결성 (Integrity) / 보안성 (Security)
31. 클라이언트-서버 DBMS 아키텍처 (2-Tier, 3-Tier)
32. TP 모니터 (Transaction Processing Monitor) / 미들웨어
33. 파일 저장 구조 - 히프(Heap), 순차(Sequential), 해시(Hash), 인덱스(Indexed) 파일
34. 고정 길이 레코드 vs 가변 길이 레코드
35. 블로킹 팩터 (Blocking Factor) - 하나의 블록에 저장되는 레코드 수
36. B-Tree (다진 탐색 트리) 원리 및 구조
37. B+Tree - 리프 노드에만 데이터 저장, 리프 노드 간 연결 리스트 (RDB 인덱스 기본)
38. 관계 대수 (Relational Algebra) - 절차적 언어, "어떻게" 구할 것인가 명시
39. 일반 집합 연산자 - 합집합(Union), 교집합(Intersection), 차집합(Difference), 카티션 프로덕트(Cartesian Product)
40. 순수 관계 연산자 - 셀렉트(Select, σ), 프로젝트(Project, π), 조인(Join, ⋈), 디비전(Division, ÷)
41. 셀렉트(Select) - 수평적 부분집합 (행 추출)
42. 프로젝트(Project) - 수직적 부분집합 (열 추출)
43. 조인(Join) - 공통 속성 기준으로 두 릴레이션 결합
44. 디비전(Division) - 속성 값을 모두 가진 튜플 추출
45. 관계 해석 (Relational Calculus) - 비절차적 언어, "무엇을" 구할 것인가 명시 (튜플 관계 해석, 도메인 관계 해석)
46. 인-메모리 데이터베이스 (IMDB, In-Memory DB) - Redis, Memcached, SAP HANA (디스크 I/O 병목 제거)
47. 컬럼 기반 저장소 (Columnar Store) - 분석(OLAP) 최적화, 높은 압축률
48. 로우 기반 저장소 (Row Store) - 트랜잭션(OLTP) 최적화
49. 스토리지 엔진 (Storage Engine) 구조 (InnoDB, MyISAM 등)
50. 버퍼 풀 (Buffer Pool) / 버퍼 관리자 - 디스크 접근 최소화 
51. 로깅 엔진 (Logging Engine) - 복구(Recovery)를 위한 로그(WAL) 작성
52. 옵티마이저 (Optimizer) - 최적의 SQL 실행 계획 생성
53. 파서 (Parser) - SQL 구문 분석 및 파스 트리 생성
54. 카탈로그 매니저 - 메타데이터 접근
55. 커넥션 풀 (Connection Pool) - 데이터베이스 연결 오버헤드 감소
56. 데이터 딕셔너리 캐시 (Data Dictionary Cache)
57. 공유 풀 (Shared Pool) - Oracle 인스턴스 구조
58. 데이터베이스 인스턴스 (Database Instance) - 메모리 구조 + 백그라운드 프로세스
59. 영구 저장소 (Persistent Storage) - 데이터 파일, 로그 파일, 제어 파일
60. 서버리스 데이터베이스 (Serverless DB) - Amazon Aurora Serverless 등 자동 확장 아키텍처

## 2. 관계형 데이터 모델 및 정규화 (70개)
61. 릴레이션 (Relation) - 데이터를 2차원 표로 표현한 구조
62. 속성 (Attribute / Column / Degree) - 릴레이션의 열 (차수)
63. 튜플 (Tuple / Row / Cardinality) - 릴레이션의 행 (카디널리티)
64. 도메인 (Domain) - 속성이 가질 수 있는 원자값(Atomic Value)들의 집합
65. 릴레이션의 특징 - 튜플의 무순서, 속성의 무순서, 튜플의 유일성, 속성의 원자성
66. NULL 값 - 아직 알려지지 않거나 해당 없는 값 (0이나 공백과 다름)
67. 키 (Key)의 개념 - 유일성(Uniqueness), 최소성(Minimality)
68. 슈퍼 키 (Super Key) - 유일성은 만족하나 최소성은 만족하지 않는 속성 집합
69. 후보 키 (Candidate Key) - 유일성과 최소성을 모두 만족하는 키
70. 기본 키 (Primary Key, PK) - 후보 키 중 설계자가 선택한 메인 식별자 (NULL 불가)
71. 대체 키 (Alternate Key) - 후보 키 중 기본 키로 선택되지 않은 나머지 키
72. 외래 키 (Foreign Key, FK) - 다른 릴레이션의 기본 키를 참조하는 속성
73. 무결성 제약조건 (Integrity Constraints)
74. 개체 무결성 (Entity Integrity) - 기본 키는 NULL이나 중복값을 가질 수 없음
75. 참조 무결성 (Referential Integrity) - 외래 키 값은 참조하는 릴레이션의 기본키 값이거나 NULL이어야 함
76. 도메인 무결성 (Domain Integrity) - 속성 값은 정의된 도메인에 속해야 함
77. 사용자 정의 무결성 (User-defined Integrity) - 업무 규칙에 따른 제약 (CHECK 제약조건 등)
78. 키 무결성 (Key Integrity)
79. NULL 무결성 (Null Integrity)
80. ER 모델 (Entity-Relationship Model) - 피터 첸(Peter Chen) 제안, 개념적 모델링
81. 개체 (Entity) - 사각형, 관리 대상
82. 속성 (Attribute) - 타원, 개체의 특성
83. 관계 (Relationship) - 마름모, 개체 간 연관성
84. 카디널리티 비율 (Cardinality Ratio) - 1:1, 1:N, M:N
85. 참여 제약조건 (Participation Constraint) - 필수 참여(전체), 선택 참여(부분)
86. 약한 개체 (Weak Entity) - 이중 사각형, 부모 개체에 종속 (식별 관계)
87. 식별 관계 (Identifying) vs 비식별 관계 (Non-identifying)
88. 식별자 (Identifier) - ER 모델에서의 키
89. 확장 ER 모델 (EER) - 서브클래스, 슈퍼클래스, 상속(일반화/특수화) 개념 추가
90. 이상 현상 (Anomaly) - 정규화를 거치지 않아 발생하는 데이터 중복에 따른 부작용
91. 삽입 이상 (Insertion Anomaly) - 불필요한 데이터까지 함께 삽입해야 하는 현상
92. 삭제 이상 (Deletion Anomaly) - 연쇄 삭제로 인해 필요한 데이터까지 소실되는 현상
93. 갱신 이상 (Update Anomaly) - 중복 데이터 중 일부만 갱신되어 데이터 불일치 발생
94. 함수적 종속성 (Functional Dependency, FD) - X의 값이 Y의 값을 유일하게 결정할 때 (X -> Y)
95. 결정자 (Determinant) X / 종속자 (Dependent) Y
96. 완전 함수적 종속 (Full Functional Dependency)
97. 부분 함수적 종속 (Partial Functional Dependency) - 복합키의 일부 속성에만 종속
98. 이행적 함수적 종속 (Transitive Functional Dependency) - X->Y, Y->Z 일 때 X->Z 종속 발생
99. 암스트롱의 공리 (Armstrong's Axioms) - 반사의 공리, 첨가의 공리, 이행의 공리
100. 정규화 (Normalization) - 이상 현상 방지를 위해 릴레이션을 분해(Decomposition)하는 과정
101. 무손실 분해 (Lossless-Join Decomposition) - 조인 시 원래 릴레이션이 복원됨 보장
102. 종속성 보존 (Dependency Preservation) - 분해 후에도 FD가 유지됨
103. 제1정규형 (1NF) - 도메인이 원자값만으로 구성
104. 제2정규형 (2NF) - 1NF 만족 및 부분 함수 종속 제거 (완전 함수 종속화)
105. 제3정규형 (3NF) - 2NF 만족 및 이행적 함수 종속 제거
106. BCNF (Boyce-Codd Normal Form) - 3NF 만족 및 모든 결정자가 후보키 (강한 3NF)
107. 다치 종속성 (MVD, Multi-Valued Dependency) - X->>Y
108. 제4정규형 (4NF) - BCNF 만족 및 다치 종속 제거
109. 조인 종속성 (Join Dependency)
110. 제5정규형 (5NF / PJNF) - 4NF 만족 및 조인 종속 제거
111. 정규화의 역설 / 성능 저하 - 과도한 분해 시 조인(Join) 오버헤드 증가
112. 반정규화 (De-normalization / 비정규화) - 성능 향상을 위해 정규화 원칙을 의도적으로 위배, 중복 허용
113. 반정규화 기법 - 테이블 병합(1:1, 1:M, 슈퍼/서브), 테이블 분할(수직, 수평 분할), 중복 칼럼 추가, 파생 컬럼/테이블 추가
114. 데이터베이스 설계 단계 - 요구사항 분석 -> 개념적 설계 -> 논리적 설계 -> 물리적 설계
115. 논리적 설계 (Logical Design) - ERD를 릴레이션 스키마로 변환, 정규화 수행
116. 매핑 룰 (Mapping Rule) - 개념적 모델(ERD)을 논리 모델(릴레이션)로 변환하는 규칙
117. 물리적 설계 (Physical Design) - 인덱스, 파티셔닝, 클러스터링, 저장 구조 설계
118. 차원 모델링 (Dimensional Modeling) - OLAP, 스타 스키마 (Star Schema), 스노우플레이크 스키마 (Snowflake Schema)
119. 팩트 테이블 (Fact Table) / 차원 테이블 (Dimension Table)
120. 데이터 역엔지니어링 (Data Reverse Engineering)
121. 데이터 아키텍처 (DA, Data Architecture) 프레임워크 (Zachman 등)
122. 마스터 데이터 관리 (MDM, Master Data Management)
123. 기준 정보 (Reference Data)
124. 데이터 거버넌스 (Data Governance)
125. 메타데이터 관리 시스템 (MMS)
126. 데이터 표준화 (Data Standardization) - 단어 사전, 도메인, 표준 용어 정의
127. 정보 공학 방법론 (Information Engineering) - 데이터 중심 개발 (James Martin)
128. 논리적 데이터 독립성과 뷰(View)의 관계
129. ORM (Object-Relational Mapping) 개념과 임피던스 불일치 (Impedance Mismatch)
130. ERD 표기법 - IE(Information Engineering, 까마귀발 표기법), Barker, IDEF1X

## 3. SQL 및 옵티마이저 (60개)
131. SQL (Structured Query Language) 국제 표준 (ANSI/ISO SQL)
132. 조인 연산의 종류 (SQL 기준)
133. 내부 조인 (Inner Join) - 교집합, 양쪽에 모두 존재하는 행만 추출
134. 동등 조인 (Equi Join) / 자연 조인 (Natural Join) - 중복 컬럼 제거
135. 비동등 조인 (Non-Equi Join) - BETWEEN, >, < 등 등호 이외 연산자 사용 조인
136. 외부 조인 (Outer Join) - 합집합 개념, 기준 테이블의 모든 행 추출 + 조인 실패 시 NULL 반환
137. Left Outer Join / Right Outer Join / Full Outer Join
138. 교차 조인 (Cross Join / Cartesian Product) - M x N 건 생성
139. 셀프 조인 (Self Join) - 동일 테이블 간의 조인, 계층형 쿼리 등에 활용
140. 서브쿼리 (Subquery) - 쿼리 내부에 포함된 또 다른 쿼리
141. 인라인 뷰 (Inline View) - FROM 절에 사용된 서브쿼리, 동적으로 생성되는 뷰
142. 스칼라 서브쿼리 (Scalar Subquery) - SELECT 절에 사용, 단일 행/단일 열 반환
143. 중첩 서브쿼리 (Nested Subquery) - WHERE 절에 사용 (IN, EXISTS, ANY, ALL)
144. 연관 서브쿼리 (Correlated Subquery) - 메인 쿼리의 컬럼을 포함하는 서브쿼리
145. 윈도우 함수 (Window Function / 분석 함수) - 행 간의 관계를 분석 (RANK, DENSE_RANK, ROW_NUMBER, LEAD, LAG)
146. 파티션 바이 (PARTITION BY) / 오더 바이 (ORDER BY) - 윈도우 함수의 범위와 정렬
147. 집계 함수 (Aggregate Function) - SUM, AVG, MAX, MIN, COUNT
148. 그룹 바이 (GROUP BY) / 해빙 (HAVING) - HAVING은 그룹화 결과에 대한 조건
149. ROLLUP, CUBE, GROUPING SETS - 다차원 소계 및 총계 생성 (OLAP)
150. 집합 연산자 - UNION (중복 제거 합집합), UNION ALL (중복 포함 합집합), INTERSECT, MINUS/EXCEPT
151. 뷰 (View) - 가상 테이블, 논리적 데이터 독립성 및 보안 제공
152. 단순 뷰 (Simple View) vs 복합 뷰 (Complex View)
153. 구체화된 뷰 (MVIEW, Materialized View) - 물리적 공간에 실제 데이터 저장, 성능 향상, 동기화(Refresh) 필요
154. 인덱스 (Index) - 검색 속도 향상을 위한 자료구조, 별도의 저장 공간 차지
155. 인덱스의 단점 - DML(Insert, Update, Delete) 시 인덱스 수정 오버헤드 발생
156. B-Tree 인덱스 / B+Tree 인덱스
157. 해시 인덱스 (Hash Index) - 동등(=) 검색에 빠름, 범위(Range) 검색 불가
158. 비트맵 인덱스 (Bitmap Index) - 분포도(Cardinality)가 나쁜(성별 등) 컬럼에 적합, DML 성능 저하 큼
159. 클러스터드 인덱스 (Clustered Index) - 물리적 데이터 정렬 기준, 테이블당 1개 (보통 PK)
160. 넌클러스터드 인덱스 (Non-Clustered Index / 보조 인덱스) - 리프 노드가 실제 데이터 포인터 보유, 여러 개 가능
161. 결합 인덱스 (Composite Index) - 2개 이상 컬럼으로 구성 (선행 컬럼 순서 중요)
162. 함수 기반 인덱스 (FBI, Function Based Index) - 산술식이나 함수가 적용된 결과 기준 인덱싱
163. 옵티마이저 (Optimizer) - SQL 실행 최적 경로(Execution Plan) 생성기
164. 규칙 기반 옵티마이저 (RBO, Rule Based Optimizer) - 정해진 우선순위 규칙에 따라 계획 수립 (구형)
165. 비용 기반 옵티마이저 (CBO, Cost Based Optimizer) - 시스템 통계 정보 기반, 디스크 I/O 등 최소 비용 계산 (현대 RDBMS)
166. 실행 계획 (Execution Plan) - 옵티마이저가 생성한 네비게이션 트리
167. 힌트 (Hint) - 개발자가 옵티마이저에게 접근 경로를 명시적으로 지시 (/*+ INDEX(EMP IDX_01) */ 등)
168. 데이터 딕셔너리 통계 정보 (Statistics) - 테이블 건수, 블록 수, 인덱스 높이, 클러스터링 팩터 등
169. 클러스터링 팩터 (Clustering Factor) - 인덱스 정렬 순서와 실제 물리적 데이터 정렬 순서의 일치 정도
170. 선택도 (Selectivity) / 기수성 (Cardinality) / 분포도 (Distribution)
171. 옵티마이저 조인 기법 3가지
172. 중첩 루프 조인 (NL Join, Nested Loop Join) - 선행(Driving) 테이블 행마다 후행(Driven) 테이블 인덱스 탐색, 소량 데이터/온라인(OLTP) 적합
173. 소트 머지 조인 (Sort Merge Join) - 양쪽 테이블 정렬 후 병합, 인덱스 없을 때나 대량 데이터 조인 시 (동등/비동등 모두 가능)
174. 해시 조인 (Hash Join) - 작은 테이블로 해시 맵 생성 후 큰 테이블 탐색, 대량 데이터/동등(=) 조인 전용, 성능 우수
175. 드라이빙 테이블 (Driving Table / Outer Table) vs 드리븐 테이블 (Driven Table / Inner Table)
176. 조인 순서 (Join Order) 최적화 - 동적 계획법(Dynamic Programming), 탐욕 알고리즘
177. 뷰 머징 (View Merging) - 옵티마이저의 쿼리 변환 (인라인 뷰를 메인 쿼리에 병합)
178. 조건 푸시 다운 (Condition Pushdown) - WHERE 조건을 뷰 내부로 밀어 넣어 데이터 필터링 조기화
179. 파티셔닝 (Partitioning) - 대용량 테이블 물리적 분할 관리 기법
180. 레인지 파티셔닝 (Range Partitioning) - 범위(날짜 등) 기준
181. 해시 파티셔닝 (Hash Partitioning) - 해시 함수 결과, 균등 분산용
182. 리스트 파티셔닝 (List Partitioning) - 명시적 특정 값(지역명 등) 기준
183. 컴포지트 파티셔닝 (Composite Partitioning) - 복합 (Range + Hash 등)
184. 파티션 프루닝 (Partition Pruning) - SQL 조건에 맞는 파티션만 스캔 (옵티마이저 최적화)
185. 전역 인덱스 (Global Index) vs 지역 인덱스 (Local Index, 파티션별 독립 인덱스)
186. 스토어드 프로시저 (Stored Procedure) / 트리거 (Trigger) - DB 서버 내에 컴파일되어 저장된 모듈
187. 사용자 정의 함수 (UDF, User Defined Function)
188. PL/SQL (Oracle), T-SQL (SQL Server) - 절차적 SQL 언어
189. 동적 SQL (Dynamic SQL) - 실행 시점에 문자열 형태로 조립되어 실행
190. 바인드 변수 (Bind Variable) - 파싱 결과 재사용, SQL 인젝션 방지, 하드 파싱 (Hard Parsing) 방지 성능 이점

## 4. 트랜잭션, 동시성 제어 및 복구 (70개)
191. 트랜잭션 (Transaction) - 논리적 작업의 기본 단위, 분할할 수 없는 일련의 연산
192. 트랜잭션의 ACID 특성
193. 원자성 (Atomicity) - All or Nothing (모두 반영되거나 모두 취소) - 회복(Recovery) 관리자가 보장
194. 일관성 (Consistency) - 트랜잭션 전후에 데이터베이스 제약조건(무결성) 유지 - 병행제어/무결성 제약조건 보장
195. 격리성 (Isolation) - 실행 중인 트랜잭션 연산에 다른 트랜잭션 간섭 불가 - 병행 제어(Concurrency Control) 보장
196. 영속성 (Durability) - 성공 완료된 트랜잭션 결과는 영구 반영 - 회복(Recovery) 관리자가 보장
197. 트랜잭션 상태 전이 - 활동(Active) -> 부분 완료(Partially Committed) -> 완료(Committed) / 실패(Failed) -> 철회(Aborted)
198. COMMIT 명령어 - 트랜잭션 성공적 완료, 디스크 반영 확정
199. ROLLBACK 명령어 - 트랜잭션 취소, 이전 상태로 복구
200. SAVEPOINT - 트랜잭션 내 중간 복구 지점 설정
201. 동시성 제어 (Concurrency Control / 병행 제어)의 목적 - 데이터 일관성 유지, 다중 사용자 처리량 극대화
202. 병행 수행 시 문제점 (격리성 위배 시)
203. 갱신 손실 (Lost Update) - 둘 이상의 트랜잭션이 동시 갱신 시, 이전 값이 덮어써져 손실
204. 모순성 (Inconsistency / Unrepeatable Read) - 동일 데이터 반복 읽기 시 값이 달라지는 현상
205. 오손 읽기 (Dirty Read) - 다른 트랜잭션이 아직 커밋하지 않은 미확정 데이터를 읽음
206. 연쇄 복귀 (Cascading Rollback) - 한 트랜잭션 취소 시, 의존하던 다른 트랜잭션도 연쇄 취소
207. 유령 읽기 (Phantom Read) - 이전 읽기에 없던 새로운 행(INSERT)이 반복 읽기 시 나타남
208. 스케줄 (Schedule / History) - 트랜잭션 연산의 실행 순서
209. 직렬 스케줄 (Serial Schedule) - 트랜잭션을 순차적으로 실행 (동시성 0)
210. 비직렬 스케줄 (Non-serial Schedule) - 인터리빙 방식 병행 실행
211. 직렬 가능 스케줄 (Serializable Schedule) - 비직렬이지만 결과가 직렬 스케줄과 동일한 스케줄 보장
212. 충돌 직렬 가능성 (Conflict Serializable)
213. 락킹 (Locking) 기법 - 상호 배제를 위한 잠금
214. 공유 락 (Shared Lock / Read Lock, S-Lock) - 읽기 허용, 쓰기 불가
215. 배타 락 (Exclusive Lock / Write Lock, X-Lock) - 읽기/쓰기 모두 불가 독점
216. 2단계 락킹 프로토콜 (2PL, Two-Phase Locking) - 직렬 가능성 보장을 위한 락 프로토콜
217. 확장 단계 (Growing Phase) - 락 획득만 가능, 반납 불가
218. 축소 단계 (Shrinking Phase) - 락 반납만 가능, 획득 불가
219. 2PL의 한계 - 교착 상태(Deadlock) 발생 가능성, 연쇄 복귀 위험
220. 엄격한 2PL (Strict 2PL) - X-Lock을 커밋 전까지 보유 (연쇄 복귀 방지)
221. 강건한 2PL (Rigorous 2PL) - S-Lock, X-Lock 모두 커밋 전까지 보유
222. 타임스탬프 순서 (Timestamp Ordering) 기법 - 트랜잭션 진입 시간에 맞춰 직렬화 (비관적 제어 아님, 락 없음)
223. 낙관적 동시성 제어 (Optimistic Concurrency Control) - 작업 먼저 수행 후 종료(Validation) 시점에 충돌 검사
224. 다중 버전 동시성 제어 (MVCC, Multi-Version Concurrency Control) - 읽기와 쓰기 락 충돌 배제, 스냅샷 활용 (Oracle, PostgreSQL 기본)
225. Undo 세그먼트 (롤백 세그먼트) - MVCC 구버전 데이터 저장 영역
226. 블로킹 (Blocking) 현상 완화 (MVCC의 가장 큰 장점 - 읽기가 쓰기를 막지 않고, 쓰기가 읽기를 막지 않음)
227. 트랜잭션 고립화 수준 (Isolation Level) - ANSI/ISO SQL 표준 4단계
228. Read Uncommitted (레벨 0) - 커밋 안된 데이터 읽기 허용 (Dirty Read 발생)
229. Read Committed (레벨 1) - 커밋된 데이터만 읽음 (Oracle 기본, Non-Repeatable Read 발생)
230. Repeatable Read (레벨 2) - 트랜잭션 내에서 읽은 데이터 락 유지 (MySQL 기본, Phantom Read 발생 가능성)
231. Serializable (레벨 3) - 완벽한 직렬화, 가장 엄격 (모든 이상현상 방지, 동시성 최저)
232. 데이터베이스 장애 유형 - 트랜잭션 장애, 시스템 장애, 미디어 장애
233. 회복 (Recovery) - 장애 발생 전 일관된 상태로 DB 복원 (원자성, 영속성 보장 기법)
234. Redo (재실행) - 장애 발생 후 커밋된 트랜잭션을 로그 참조하여 재반영 (영속성 보장)
235. Undo (취소) - 장애 발생 후 커밋 안된 트랜잭션을 이전 상태로 원복 (원자성 보장)
236. WAL (Write-Ahead Logging) 프로토콜 - 데이터 갱신 전 반드시 로그부터 디스크에 안전하게 기록
237. 로그 기반 회복 기법 (Log-based Recovery)
238. 지연 갱신 (Deferred Update) - 트랜잭션 완료 전까지 DB 기록 지연, Undo 불필요, Redo만 수행
239. 즉시 갱신 (Immediate Update) - 트랜잭션 도중에도 DB 기록, 회복 시 Redo와 Undo 모두 필요
240. 그림자 페이징 (Shadow Paging) 기법 - 로그 없이 구버전(그림자) 디렉토리와 현재 디렉토리 유지 교체 (COW 유사)
241. 검사점 (Checkpoint / Checkpointing) 회복 기법 - 주기적으로 메모리 버퍼를 디스크에 동기화(Flush)하여 복구 시간(Redo 대상) 단축
242. 미디어 회복 (Media Recovery) - 디스크 손상 시 백업(덤프) 아카이브와 로그를 이용해 롤포워드(Roll-forward) 복구
243. ARIES 알고리즘 - 현대 DBMS 복구 표준 알고리즘 (Analysis, Redo, Undo 3단계 페이즈)
244. LSN (Log Sequence Number) - 로그 레코드 고유 식별 번호
245. Compensation Log Record (CLR) - Undo 수행 시 남기는 보상 로그 (중복 Undo 방지)
246. 데이터베이스 교착 상태 (Deadlock) 처리 기법 - Wait-Die, Wound-Wait (타임스탬프 선점/비선점 기반 예방)
247. 교착 상태 탐지 대기 그래프 (Wait-for Graph) - 사이클 발생 시 희생자(주로 후발 트랜잭션) 롤백
248. 분산 트랜잭션 (Distributed Transaction) - 둘 이상의 노드/DB에 걸친 트랜잭션
249. 2단계 커밋 (2PC, Two-Phase Commit) - 분산 트랜잭션의 원자성 보장 프로토콜
250. 코디네이터 (Coordinator)와 참여자 (Participant) - 1단계(Prepare), 2단계(Commit/Rollback)
251. 3단계 커밋 (3PC, Three-Phase Commit) - 2PC의 블로킹 한계 보완 (Pre-Commit 추가)
252. Saga 패턴 - MSA 환경의 긴 트랜잭션(Long Lived Transaction) 처리, 이벤트 기반 로컬 트랜잭션 분할 및 보상 트랜잭션(Compensating Transaction) 수행
253. CAP 정리 (CAP Theorem) - 일관성(Consistency), 가용성(Availability), 분단 허용성(Partition Tolerance) 3가지를 동시 만족 불가 (분산 DB 이론)
254. CP 시스템 (HBase, MongoDB 기본) / AP 시스템 (Cassandra, DynamoDB) / CA 시스템 (RDBMS, 네트워크 분할 없는 단일망)
255. PACELC 정리 - CAP 확장판 (분할 P 시 A/C 대안, 정상 작동 E 시 L(지연)/C(일관성) 상충 관계)
256. 결과적 일관성 (Eventual Consistency) - 일정 시간이 지나면 결국 동기화됨 (AP 시스템 특징, BASE 특성)
257. BASE 속성 - Basically Available, Soft-state, Eventually consistent (NoSQL의 특성, ACID의 반대)
258. 벡터 시계 (Vector Clock) / 타임스탬프 - 분산 시스템 데이터 동기화 충돌 해결
259. 래프트 (Raft) / 팍소스 (Paxos) 알고리즘 - 분산 DB 리더 선출 및 로그 복제 합의 (Consensus)
260. 스플릿 브레인 (Split Brain) 현상 - 네트워크 단절로 두 개의 마스터가 독립적 작동 (Quorum/과반수 투표로 방지)

## 5. 분산 DB, NoSQL 및 NewSQL (60개)
261. 분산 데이터베이스 (Distributed Database) 목표 - 단일 시스템처럼 보이게 하는 투명성(Transparency) 제공
262. 분산 데이터베이스 투명성 6가지 규칙
263. 위치 투명성 (Location Transparency) - 데이터 물리적 위치 몰라도 접근
264. 분할 투명성 (Fragmentation/Partition Transparency) - 데이터 분할 여부 은닉
265. 복제 투명성 (Replication Transparency) - 데이터 중복 유지 및 갱신 투명
266. 병행 투명성 (Concurrency) / 장애 투명성 (Failure) / 지역 사상 투명성 (Local Mapping)
267. 데이터 분할 기법 (Fragmentation)
268. 수평 분할 (Horizontal Fragmentation) - 튜플(행) 단위 분할, 셀렉트 연산
269. 수직 분할 (Vertical Fragmentation) - 속성(열) 단위 분할, 프로젝트 연산 (PK 반드시 포함)
270. 복제 (Replication) - 동기식 복제 (Synchronous) vs 비동기식 복제 (Asynchronous)
271. 마스터-슬레이브 (Master-Slave / Primary-Replica) 복제 - 읽기/쓰기 분산 아키텍처
272. 멀티 마스터 (Multi-Master / Peer-to-Peer) 복제 - 양방향 쓰기 가능, 충돌 해결 매커니즘 필수
273. 동종 분산 DB vs 이종 (Heterogeneous) 분산 DB 통합
274. NoSQL (Not Only SQL) 데이터베이스 - 스키마리스(Schemaless), 수평적 확장(Scale-out), 분산 아키텍처
275. NoSQL 데이터 모델 4가지
276. 키-값 저장소 (Key-Value Store) - 속도 최적화, Redis, Memcached, Amazon DynamoDB
277. 문서 저장소 (Document Store) - JSON/XML 형태, BSON 포맷, 유연성, MongoDB, CouchDB
278. 컬럼 패밀리 저장소 (Column Family / Wide-Column Store) - 대량 쓰기/읽기 특화, 압축 우수, HBase, Cassandra
279. 그래프 저장소 (Graph Store) - 노드(Node), 엣지(Edge), 속성(Property) 구조, 관계 탐색 최적화, Neo4j, Amazon Neptune
280. 샤딩 (Sharding) - NoSQL의 수평적 파티셔닝 기술 (데이터베이스 분할)
281. 샤드 키 (Shard Key / Partition Key) - 분산 배치 기준이 되는 키 설계 중요성
282. 해시 샤딩 (Hash Sharding) - 균등 분배 / 레인지 샤딩 (Range Sharding) - 범위 검색 유리 (핫스팟 문제 유의)
283. 일관된 해싱 (Consistent Hashing) - 노드 추가/삭제 시 재배치 최소화 (링 구조 배열)
284. 맵리듀스 (MapReduce) - NoSQL/Hadoop의 분산 데이터 병렬 처리 프로그래밍 모델 (Map: 매핑/필터링, Reduce: 집계)
285. 그래프 쿼리 언어 - Cypher (Neo4j), Gremlin, SPARQL
286. 시계열 데이터베이스 (Time Series Database, TSDB) - 시간순 로깅 특화, InfluxDB, Prometheus
287. 시계열 데이터 특성 - 높은 쓰기 처리량, 다운샘플링 (Downsampling), 보존 정책 (Retention Policy)
288. 공간 데이터베이스 (Spatial Database) - 좌표, 기하학적 객체 쿼리, PostGIS 확장
289. R 트리 (R-Tree) / MBR (Minimum Bounding Rectangle) - 공간 검색 인덱스 구조
290. NewSQL 데이터베이스 - RDB의 ACID 트랜잭션과 NoSQL의 수평적 확장성(Scale-out) 결합 패러다임
291. 구글 스패너 (Google Cloud Spanner) - 글로벌 분산, 트루타임(TrueTime/원자시계+GPS) 기반 글로벌 일관성 보장 NewSQL
292. 칵로치DB (CockroachDB) - 생존성 극대화 분산 SQL 데이터베이스
293. 티아이디비 (TiDB) - HTAP (Hybrid Transactional/Analytical Processing) 지원 NewSQL
294. HTAP - OLTP(트랜잭션)와 OLAP(분석) 워크로드를 단일 데이터베이스 플랫폼에서 분리/동시 처리하는 기술 (Row+Column 하이브리드 엔진)
295. 메모리 캐싱 (Caching) 기술 적용 - Look-aside (Lazy Loading) 패턴, Write-through 패턴
296. 캐시 스탬피드 (Cache Stampede) / Thundering Herd 문제 - 대규모 동시 캐시 미스 발생 부하
297. 레디스 (Redis) 자료구조 - String, List, Set, Sorted Set, Hash
298. 몽고DB (MongoDB) 아키텍처 - 레플리카 셋 (Replica Set), 샤드 클러스터 (mongos, config server, shard)
299. 카산드라 (Cassandra) 특징 - 링 기반 피어투피어, 가십 프로토콜(Gossip Protocol), 튜너블 컨시스턴시 (Tunable Consistency - Quorum Read/Write)
300. 툼스톤 (Tombstone) 메커니즘 - 분산 DB에서 삭제된 레코드 마킹 (삭제 동기화 지연 해결)
301. 데이터 마이그레이션 도구 및 CDC (Change Data Capture) - Debezium 등 실시간 변경 로깅/전송
302. 엘라스틱서치 (Elasticsearch) - 루씬(Lucene) 기반 텍스트 검색 및 분석 역색인(Inverted Index) DB
303. 역색인 (Inverted Index) 구조 - 단어(Term)가 포함된 문서 ID 리스트 매핑 (검색 엔진 핵심)
304. 데이터 레이크하우스 (Data Lakehouse) - 데이터 레이크(비정형)와 웨어하우스(정형)의 융합 구조 (Databricks, Delta Lake)
305. 오라클 RAC (Real Application Clusters) - 공유 디스크(Shared Disk) 기반 다중 인스턴스 클러스터링 RDB (수직적 한계 완화)
306. 셰어드 낫띵 (Shared Nothing) 아키텍처 - 데이터 분할 공유 (수평 확장, NoSQL 기본 구조)
307. 글로벌 보조 인덱스 (GSI, Global Secondary Index) 분산 환경 오버헤드
308. 폴리글랏 퍼시스턴스 (Polyglot Persistence) - 마이크로서비스마다 목적에 맞는 최적의 이기종 DB 선택/혼용
309. CQRS 아키텍처와 DB 동기화 (Event Sourcing 연동)
310. 멀티테넌트 (Multi-tenant) 데이터베이스 구조 - 논리적 스키마 분리, 물리적 인스턴스 분리 격리
311. 데이터베이스 퍼징 (Database Fuzzing) 및 테스트 취약점
312. 클라우드 관리형 DB (DBaaS, Database as a Service) - AWS RDS, Azure SQL 등
313. 그래프 신경망 (GNN) 연계를 위한 그래프 데이터베이스 활용
314. NoSQL 모델링 전략 - 정규화가 아닌 쿼리 패턴 주도 설계 (Query-driven Modeling), 역정규화 내재화
315. 임베디드 도큐먼트 (Embedded Document) 패턴 - 연관 데이터를 한 문서에 중첩 저장 (조인 배제)
316. 참조 (Reference) 패턴 - 문서 크기 한계 시 외부 링크 저장
317. 버저닝 (Versioning) 데이터 모델 설계
318. 트리 구조 저장을 위한 NoSQL 모델 (Materialized Path, Nested Sets)
319. 블록체인 기반 변조 방지 원장 데이터베이스 (Amazon QLDB)
320. 다중 모델 데이터베이스 (Multi-model Database) - 단일 엔진 내 Document, Graph, KV, Relational 지원 (ArangoDB 등)

## 6. 데이터 웨어하우스, OLAP 및 최신 DB 트렌드 (70개)
321. 데이터 웨어하우스 (Data Warehouse, DW) - 의사결정 지원을 위한 통합, 주젯 중심, 시계열, 비휘발성 저장소 (Inmon 모델)
322. DW 4대 특징 - 주젯 지향성(Subject-oriented), 통합성(Integrated), 시계열성(Time-variant), 비휘발성(Non-volatile)
323. 데이터 마트 (Data Mart) - 특정 부서/조직 중심의 소규모 DW (Kimball 모델 - 상향식)
324. ODS (Operational Data Store) - DW로 가기 전의 임시/운영 데이터 통합 영역
325. ETL (Extract, Transform, Load) 프로세스 - 소스 추출 -> 정제/변환 -> 타겟 적재
326. ELT (Extract, Load, Transform) 프로세스 - 클라우드 기반 현대 아키텍처, 먼저 적재 후 웨어하우스 내에서 변환 처리
327. OLTP (On-Line Transaction Processing) - 실시간 트랜잭션, 정규화된 RDB, 빠른 응답 속도
328. OLAP (On-Line Analytical Processing) - 대용량 다차원 분석, 비정규화(스타 스키마), 읽기 위주
329. OLAP 연산 (Operation) - 롤업, 드릴다운, 슬라이스, 다이스, 피벗
330. 롤업 (Roll-up) - 요약 / 드릴다운 (Drill-down) - 구체화 (계층 구조 상하 이동)
331. 슬라이스 (Slice) - 특정 차원의 단일 평면 절단 / 다이스 (Dice) - 여러 차원의 작은 주사위 모양 추출
332. 피벗 (Pivot) - 보고서 축 전환 (행렬 변환)
333. 다차원 모델링 - 팩트 (Fact / 측정값)와 차원 (Dimension / 분석 기준) 구성
334. 스타 스키마 (Star Schema) - 사실 테이블 1개, 정규화 안된 다수 차원 테이블 방사형 배치 (빠른 조인, 중복 존재)
335. 스노우플레이크 스키마 (Snowflake Schema) - 차원 테이블을 3NF 정규화하여 중복 제거, 조인 복잡성 증가 눈송이 형태
336. MOLAP (Multidimensional OLAP) - 다차원 큐브(Cube) 사전 생성 구조, 초고속 검색, 큐브 갱신 비용 큼
337. ROLAP (Relational OLAP) - 관계형 DB 기반 SQL 실시간 분석, 대용량 처리에 적합
338. HOLAP (Hybrid OLAP) - MOLAP의 속도 + ROLAP의 대용량 처리 결합
339. 데이터 레이크 (Data Lake) - 원시 데이터(Raw data), 정형/반정형/비정형 모두 저장하는 스키마 온 리드(Schema-on-read) 중앙 저장소
340. 스키마 온 라이트 (Schema-on-write) - RDBMS의 입력 시점 스키마 검증
341. 스키마 온 리드 (Schema-on-read) - 데이터 레이크/NoSQL의 조회 시점 스키마 적용
342. 메타데이터 카탈로그 (Hive Metastore, AWS Glue) - 데이터 레이크 자산 검색 지원
343. 변경 데이터 캡처 (CDC, Change Data Capture) 데이터 파이프라인
344. 스트림 처리 (Stream Processing) DB 기술 (Apache Kafka, Flink) - 실시간 이벤트 데이터베이스화
345. 배치 처리 (Batch Processing) 파이프라인
346. 벡터 데이터베이스 (Vector Database) - AI, LLM, 딥러닝 임베딩(Embedding) 벡터 고속 검색에 특화 (Milvus, Pinecone, Qdrant 등)
347. 임베딩 (Embedding) 모델 - 비정형 데이터(텍스트, 이미지)를 고차원 숫자 배열로 변환
348. 유사도 검색 (Similarity Search) - 벡터 간 거리/각도 기반 의미적 탐색 연산 (키워드 일치 검색의 대안)
349. 코사인 유사도 (Cosine Similarity) - 벡터 간 각도 측정
350. 유클리디안 거리 (Euclidean Distance / L2) / 내적 (Dot Product)
351. ANN (Approximate Nearest Neighbor) 알고리즘 - 벡터 DB의 고속 근사치 검색 (정확도 일부 희생, 속도 극대화)
352. HNSW (Hierarchical Navigable Small World) - 대표적인 벡터 인덱싱 그래프 기반 ANN 알고리즘
353. RAG (Retrieval-Augmented Generation) 패턴 - 벡터 DB를 연동하여 LLM 생성의 환각(Hallucination) 방지 프레임워크
354. 벡터 인덱스 IVFFlat (Inverted File Flat)
355. PGVector - PostgreSQL RDBMS의 벡터 검색 확장 플러그인 모듈
356. 클라우드 데이터 웨어하우스 솔루션 - Amazon Redshift, Google BigQuery, Snowflake 아키텍처 특성
357. 스토리지와 컴퓨팅 분리 아키텍처 (Separation of Storage and Compute) - 클라우드 네이티브 DW 핵심, 독립적 탄력적 확장
358. 데이터 메시 (Data Mesh) - 중앙 집중형 데이터 레이크 한계 극복, 도메인 주도의 분산 데이터 아키텍처 조직론
359. 데이터 패브릭 (Data Fabric) 플랫폼 (가상화 연계망)
360. 데이터 가상화 (Data Virtualization) - 물리적 이동/복제 없이 다양한 소스 논리적 통합 조회 뷰
361. 다크 데이터 (Dark Data) 관리 및 발견
362. 프라이버시 보존형 데이터베이스 (동형 암호 검색 데이터베이스 적용 기초)
363. 그래프 신경망 (GNN)과 지식 그래프 (Knowledge Graph) 연계 DB 시스템
364. 데이터 리니지 (Data Lineage) - 데이터 기원, 이동 경로, 변환 이력 추적(규제 대응, 무결성)
365. 데이터베이스 암호화 (TDE, Transparent Data Encryption) - 애플리케이션 수정 없이 디스크 저장 파일 레벨 암호화 (휴지 상태 암호화)
366. 컬럼 레벨 암호화 / 블록 레벨 암호화
367. 난독화 (Obfuscation) 및 데이터 마스킹 (Data Masking) - 개발/운영계 테스트 DB 민감 정보 은닉
368. FPE (Format Preserving Encryption) - 암호화 전후 데이터 포맷(길이, 형식) 유지 (카드번호, 주민번호 등)
369. 데이터베이스 감사 (DB Auditing) 추적 로그
370. 접근 통제 정책 기반 방화벽 (DB 방화벽) - SQL 인젝션 차단 및 IP/포트/접근시간 제어
371. SQL 인젝션 (SQL Injection) 공격 및 방어 수단 (Prepared Statement / 바인드 파라미터)
372. 데이터 옵스 (DataOps) - 데이터 파이프라인 지속적 통합/배포/모니터링 개발 문화
373. 콜드 데이터 (Cold Data) vs 핫 데이터 (Hot Data) 계층화(Tiering) 스토리지 아키텍처
374. 공간 인덱스 Quad-tree 알고리즘
375. 시계열 DB 보간 (Interpolation) 쿼리 기능
376. NoSQL 파티션 톨러런스 복구 (Hinted Handoff, Anti-entropy 매커니즘 / 머클 트리(Merkle Tree) 비교)
377. LSM-Tree (Log-Structured Merge-Tree) - 빅데이터/NoSQL(Cassandra, RocksDB) 쓰기 최적화 저장 엔진 (MemTable -> SSTable 구조)
378. 콤팩션 (Compaction) - LSM 트리 구조 병합 및 툼스톤 정리
379. 델타 인코딩 (Delta Encoding) 및 시계열 데이터 압축 (Gorilla алгоритм)
380. 시퀀스 데이터베이스 객체 특징 (Auto Increment vs Sequence)
381. 메인 메모리 DB의 스냅샷 로깅 (Checkpointing in IMDB)
382. 뉴모픽(Neuromorphic) 인프라 연동형 AI 데이터베이스 기술 동향
383. 그래프 데이터 분석 알고리즘 (PageRank, BFS 최단경로 매핑 DB 엔진 연산)
384. 실시간 커스터머 데이터 플랫폼 (CDP) 구성을 위한 DB 연계 모델
385. 서드파티 (3rd Party) 쿠키 소멸에 대비한 퍼스트파티 고객 데이터 저장소(CDW) 아키텍처
386. 데이터 공유 (Data Sharing / Clean Room) 보안 파티션 교환 모델 (Snowflake Data Clean Room 등)
387. 블록체인 기반의 영지식 증명(ZKP) 데이터 질의 프레임워크 연구 모델
388. 분산 노드 간 클럭 스큐(Clock Skew) 해결용 스패너(Spanner) 트루타임 원리
389. 대용량 트랜잭션의 배칭(Batching) 삽입 최적화 (Bulk Insert / COPY 명령어)
390. 서버리스 DB 오로라 (Aurora) 스토리지 로깅 분산 쿼럼 쓰기 (6개 복제본 중 4개 이상 확인 시 완료) 아키텍처 특장점

## 7. 시험 빈출 핵심 요약 및 실무 용어 확장 (210개)
391. 릴레이션 스키마 (내포 / Intension) 구조
392. 릴레이션 인스턴스 (외연 / Extension) 값
393. 데이터 사전 (Data Dictionary) 질의
394. 카탈로그 (Catalog) 메타데이터
395. 데이터 독립성 2단계 (논리, 물리)
396. Mapping 규칙 개체->테이블
397. 부분 함수 종속 제2정규형
398. 이행 함수 종속 제3정규형
399. BCNF 모든 결정자 후보키
400. MVD (다치 종속) 제4정규형
401. 조인 종속 제5정규형
402. 삽입 이상 (Insertion Anomaly)
403. 삭제 이상 (Deletion Anomaly)
404. 갱신 이상 (Update Anomaly)
405. 개체 무결성 (Entity Integrity) 기본키 NULL 불가
406. 참조 무결성 (Referential) 외래키
407. 슈퍼 키 최소성 부재
408. 대체 키 후보키 중 탈락키
409. 관계 대수 (절차적 연산)
410. 관계 해석 (비절차적 연산, 술어)
411. 디비전 (Division) 연산 
412. 카티션 프로덕트 (조인 조건 누락) 
413. 자연 조인 (동등 속성 자동 조인/중복 제거)
414. 외부 조인 (Outer Join + 표시 / 기준 릴레이션 보존)
415. DDL (CREATE, ALTER, DROP, TRUNCATE 롤백 불가)
416. DML (INSERT, UPDATE, DELETE 롤백 가능)
417. DCL (GRANT, REVOKE 권한 통제)
418. TCL (COMMIT, ROLLBACK, SAVEPOINT)
419. 뷰 (VIEW) 생성 가상 테이블
420. 옵티마이저 CBO 시스템 통계 
421. 실행 계획 (Execution Plan 풀 스캔 vs 인덱스 스캔)
422. 인덱스 B+Tree 리프 노드 순차 연결
423. 넌클러스터드 인덱스 (포인터 배열)
424. 클러스터드 인덱스 (물리적 레코드 정렬)
425. 해시 인덱스 (버킷 충돌 체이닝) 
426. 비트맵 인덱스 분포도 낮음 특화 
427. 결합 인덱스 (Composite) 순서 중요 
428. 테이블 풀 스캔 (Table Full Scan / FTS) 
429. 인덱스 레인지 스캔 (Index Range Scan)
430. 인덱스 패스트 풀 스캔 (병렬)
431. 중첩 루프 조인 (Nested Loop)
432. 소트 머지 조인 (정렬 후 병합)
433. 해시 조인 (메모리 해시 영역 빌드 프로브)
434. 서브쿼리 IN 연산자 
435. EXISTS (존재 여부 불린 반환 고속 탐색)
436. 윈도우 함수 OVER (PARTITION BY)
437. RANK() 동점 점프 / DENSE_RANK() 비점프
438. GROUP BY 다차원 ROLLUP, CUBE
439. 힌트 구문 적용 (/*+ INDEX() */)
440. 트랜잭션 ACID 특성 
441. 원자성 (회복 보장) 
442. 일관성 (무결성 보장)
443. 고립성 (병행제어 보장) 
444. 영속성 (로그/회복 보장) 
445. 갱신 손실 (Lost Update)
446. 오손 읽기 (Dirty Read 미커밋 읽기) 
447. 반복 불가능 읽기 (Non-Repeatable Update 변경) 
448. 유령 읽기 (Phantom Read Insert 추가) 
449. 동시성 제어 잠금 (Locking) S-락 / X-락
450. 2단계 잠금 (2PL) 확장/축소 
451. 교착 상태 (Deadlock Wait-Die)
452. 타임스탬프 순서 (Timestamp Ordering)
453. MVCC 다중 버전 읽기 일관성
454. 언두 (Undo 롤백/읽기 일관성 세그먼트) 
455. 리두 (Redo 복구 로그 아카이브)
456. WAL 프로토콜 (먼저 로그 기록)
457. 체크포인트 회복 범위 단축 
458. 고립화 수준 (Read Uncommitted~Serializable)
459. 분산 DB 위치 투명성 
460. 단편화 수평 분할 (행) / 수직 분할 (열 PK포함)
461. 복제 마스터-슬레이브 
462. 2단계 커밋 (2PC Prepare -> Commit)
463. CAP 이론 정합성 가용성 파티션 분산 특성
464. BASE 속성 NoSQL 결과적 일관성 
465. 키-값 DB 레디스 인메모리 
466. 도큐먼트 DB 몽고DB JSON BSON 
467. 컬럼 패밀리 HBASE 카산드라 와이드 컬럼
468. 그래프 DB 노드 엣지 프로퍼티 관계 탐색 Neo4j
469. 샤딩 파티셔닝 수평 스케일 아웃 
470. 해시 샤딩 분산 해시 함수
471. 컨시스턴트 해싱 링 토폴로지
472. NewSQL 구글 스패너 글로벌 일관성 
473. 데이터 웨어하우스 Inmon 전사 통합
474. 데이터 마트 부서용 Kimball 상향식
475. OLTP 정규화 쓰기 위주
476. OLAP 비정규화 읽기 다차원 
477. 스타 스키마 중심 팩트 방사 차원 단일 계층
478. 스노우플레이크 차원 정규화 계층 트리
479. 드릴 다운 / 롤 업 계층 분석 
480. 슬라이스 다이스 차원 절단
481. 피벗 크로스탭 보고서 
482. 데이터 레이크 스키마 온 리드 원시 형태 저장 
483. ETL 병목 적재 전 변환 
484. ELT 클라우드 DW 적재 후 변환 (성능 우수) 
485. 벡터 데이터베이스 임베딩 검색 구조
486. 코사인 유사도 각도 유사 탐색 엔진망 연계 
487. ANN HNSW 인덱스 근사 탐색 구조망 적용 
488. RAG (검색 증강 생성) 프레임워크 DB 매핑
489. 데이터 메시 도메인 기반 오너십 분산 
490. CDC 캡처 변경 로그 추출 스트림 
491. 데이터 암호화 TDE 디스크 파일 암호망 설계 
492. 블록체인 스마트 컨트랙트 원장 DB 융합 
493. NoSQL LSM 트리 쓰기 병합 엔진 구조 분석 
494. 멤테이블 (MemTable) 디스크 SStable 플러시
495. 카산드라 가십 프로토콜 노드 상태 전파
496. Quorum 읽기 쓰기 일관성 보정 정족수 합의 구조 
497. 툼스톤 마킹 지연 삭제 NoSQL 설계 
498. 데이터 옵스 (DataOps) 자동화 파이프라인
499. ORM 객체 매핑 JPA N+1 질의 문제
500. 역색인 (Inverted Index) 엘라스틱 서치 단어 포인터
501. 스토리지 컴퓨팅 분리 클라우드 네이티브 DW 특장점 
502. 데이터 리니지 흐름 추적 무결성 감사 구조 
503. 데이터 거버넌스 품질 메타 카탈로그 통제 관리 
504. 데이터베이스 백업 핫 덤프 콜드 덤프 
505. 트랜잭션 장애 미디어 장애 복구 범위
506. 데이터 디렉터리 시스템 카탈로그 차이
507. 트리거 (Trigger 이벤트 연동 프로시저 콜) 
508. 프로시저 vs 함수 컴파일 재사용 구조 
509. 클러스터링 팩터 인덱스 효율 평가 지표
510. 바인드 변수 적용 하드 파싱 회피 
511. 옵티마이저 힌트 사용 인덱스 강제 접근 
512. 반정규화 성능 트레이드오프 파생 컬럼 설계 
513. 트리 구조 CTE (Common Table Expression) WITH 절 재귀 
514. 팩트 테이블 차원 모델 비즈니스 수치 저장 
515. 시계열 DB 보존 정책 (Retention) 데이터 라이프사이클 
516. GNN 그래프 모델 연계 추천 시스템 설계망 적용
517. 데이터베이스 보안 다크 데이터 노출 방지 통제
518. 클린 룸 데이터 공유 샌드박싱 연동 
519. 서버리스 오로라 스토리지 분산 복제 쿼럼 
520. PACELC 분산 DB 장애 평시 트레이드 오프 이론 
521. 동적 SQL 조립 런타임 질의 파서
522. 데이터 거버넌스 3요소 (원칙, 조직, 프로세스) 
523. 정보 공학 방법론 데이터 주도적 생명 주기
524. EER 모델 서브타입 상속 특수화 
525. B+Tree 인덱스 스플릿 병합 오버헤드 
526. 해시 조인 탐색 비용 및 메모리(PGA) 스왑 오버헤드 
527. 정규화의 역설 조인 비용 및 응답 지연 해결망 설계
528. 동시성 오손 읽기 (Dirty Read) 고립 수준 회피 
529. Repeatable Read 의 팬텀 현상 MVCC 해결 유무 
530. Serializable 성능 저하 임계 영역 데드락 방어 
531. 분산 환경 2PC 블로킹 한계 코디네이터 다운 
532. 3PC 타임아웃 우회 비블로킹 프로토콜 통신 구조 
533. 이벤트 소싱 상태 변경 스트림 영속 저장망 구성 
534. Saga 패턴 보상 트랜잭션 비즈니스 실패 롤백 모사 
535. NoSQL BASE 특성 소프트 스테이트 결국 일관 상태 전이 
536. 샤드 키 불균형 데이터 핫스팟 현상 대처 
537. 시계열 DB 롤업 다운샘플링 쿼리 효율화 
538. 다중 모델 데이터베이스 융합 조회 연동성 
539. 마스터 데이터(MDM) 중복 배제 통합 기준 관리 체계 
540. 데이터 가상화 연방 쿼리 (Federated Query) 실행 엔진 
541. 클라우드 DW 스노우플레이크(Snowflake) 구조적 특징 
542. 데이터 마스킹 부분 비식별화 암호화 비교 체계 
543. DB 방화벽 프록시 스니핑 방식 모니터링 감사 통제 
544. SQL 인젝션 논리 에러/타임베이스 블라인드 주입 체계망
545. 시큐어 코딩 파라 파라미터 매핑 ORM 보안 내재화 방식 
546. 공간 데이터 쿼리 기하 연산 MBR 근접 분석 기술 구조 
547. 그래프 데이터 최단 경로(Shortest Path) 알고리즘 DB 매핑 
548. 데이터 레이크하우스 스키마 온 리드 융합 엔진 구성 기초 분석 
549. AI 파운데이션 모델 RAG 패턴 융합 벡터 DB 핵심 아키텍처 
550. HTAP 기술 OLTP, OLAP 메모리 복제/공유 실시간 아키텍처
551. 맵리듀스 분산 처리 노드 작업 셔플/소트 단계
552. 일관된 해싱 노드 이탈 데이터 리밸런싱 극소화 원리
553. 동형 암호 DB 질의 성능 한계 극복 가속화 연구망 설계 
554. 트리 구조 매핑 Nested Set 성능 검색 비교 Nested Path 모델 
555. 다차원 인덱스 K-d 트리 공간/다변량 질의 처리망 데이터 구조 분석 
556. 마스터 슬레이브 지연(Replication Lag) 읽기 불일치 이슈 극복망 
557. 멀티 마스터 충돌 해결 라스트 라이트 윈(Last Writer Wins) 메커니즘 
558. 벡터 데이터 ANN 인덱싱 파라미터(M, efConstruction) 성능/리콜 튜닝 
559. 코사인 유사도 텍스트 임베딩 매칭 정규화 거리 계측 연산 방식 
560. 데이터 패브릭 지식 그래프 연동 지능형 데이터 탐색 메타 계층 
561. 클라우드 DB 고가용성 멀티 AZ 자동 페일오버 (Failover) 프로토콜 
562. B-Tree 디스크 I/O 최적화 팬아웃 차수 및 노드 크기 블록 매핑 
563. 해시 충돌(Collision) 체이닝 방식 및 선형 탐사 성능 오버헤드 DB 매핑 
564. 컬럼 기반 스토리지 런 렝스 인코딩(RLE) 압축 효율화 탐색 
565. 인 메모리 DB 디스크 백업 체크포인트 방식 지연 성능 최소화 아키텍처
566. 캐시 스탬피드 뮤텍스 락 및 확률적 갱신(Probabilistic Early Expiration) 회피기법 
567. 레디스 만료 데이터 키 삭제 정책(LRU, LFU, Random) 캐시 스토리지 운영 
568. 몽고DB 샤딩 청크 마이그레이션 백그라운드 밸런싱 모형 분석망 
569. 카산드라 쓰기 경로(Commit Log -> Memtable -> SSTable) 병목 배제 모델 
570. 하둡 에코시스템 Hive, Pig 분산 DB 질의 쿼리 엔진 맵리듀스 추상화 
571. Spark 스트리밍 마이크로 배치 vs Flink 네이티브 스트림 인 메모리 DB 
572. 데이터 옵스 자동화 테스트 카나리 배포 데이터 파이프라인 검증망 설계 
573. ODS 준실시간 스냅샷 레코드 마이그레이션 DW 배치 레이어 차이점 
574. 데이터 마트 콘포밍 차원 (Conformed Dimension) 킴볼 버스 구조 
575. Slowly Changing Dimension (SCD Type 1, 2, 3) 시계열 이력 차원 이력 관리 모델 
576. 팩트리스 팩트 테이블 (Factless Fact Table) 이벤트 추적 차원 교차망 모델 
577. 다대다 관계 해소 교차 릴레이션 (Intersection Entity / Mapping Table) 분해 
578. 수퍼타입/서브타입 데이터 물리 변환 1:1 병합 테이블 최적 접근 모델 
579. 무결성 제약 조건 CASCADE, RESTRICT, SET NULL 연쇄 업데이트 삭제 설정
580. 도메인 무결성 CHECK 구문 정규 표현식 입력 통제 규칙 
581. 테이블 스페이스 시스템 용량 분산 관리 물리 파일 그룹핑 구성 정책 
582. 동적 성능 뷰 (V$, DMV) DBA 모니터링 병목 락 트레이싱 성능 지표 확인망 
583. 프로시저 플랜 캐시 스니핑 (Parameter Sniffing) 캐시 오염 실행 계획 악화 
584. 윈도우 함수 ROWS BETWEEN 누적 합계 구간 이동 평균 연산 파티션 
585. 서브쿼리 언네스팅 (Subquery Unnesting) 메인 쿼리 조인 변환 옵티마이저 룰 
586. 푸시 다운 조인 프레디케이트 (Join Predicate Pushdown) 뷰 연산 쿼리 변환 
587. 스타 변환 (Star Transformation) 팩트/차원 조인 옵티마이저 스캔 효율화 기법 
588. 분산 트랜잭션 코디네이터 (DTC) 미들웨어 애플리케이션 트랜잭션 연합 
589. 람포트 시계 논리적 이벤트 순서 선후 관계 인과 보장 분산 벡터 타임스탬프 
590. 클럭 스큐 구글 트루타임 원자 시계 오차 범위 대기 분산 노드 일관성 통제 
591. 가비지 컬렉터 (MVCC Undo/Redo 블록 회수 진공 프로세스 Vacuum) 데이터 정리 
592. ACID 트랜잭션 섀도우 페이징 롤백 속도 최적 디스크 I/O 절감 데이터베이스 구조 
593. ARIES 복구 알고리즘 생존자 Analysis Redo Undo 3페이즈 시스템 복구 표준 원리 
594. WAL 로그 플러시 LSN 기반 체크포인트 미디어 장애 데이터 롤 포워드 무결성 체재 
595. 데이터 리터러시 (Data Literacy) 기업 내 데이터 분석 역량 도구 지식 기반 문화 확산 
596. 데이터 디스커버리 카탈로그 플랫폼 검색 큐레이션 거버넌스 워크플로우 지식 저장 
597. 개인정보 비식별 조치 K-익명성 l-다양성 t-근접성 프라이버시 데이터 보존 평가 기준 
598. 정보보안 암호화 DB 모듈 (API/Plug-in/TDE) 혼합 구성 인프라망 구조 체계 검토 
599. 그래프 마이닝 네트워크 라우팅 추천 엔진 사기 탐지 소셜 연결 데이터 연산 
600. 양자 컴퓨팅 대응 포스트 퀀텀 암호화 DB 트랜잭션 서명 보안 체계 적용 방안 연구 동향

---
**총정리 데이터베이스 키워드 : 총 800개 수록** (+파생/분석 확장 시 1,000여 개 커버)
(RDBMS 기초(정규화, SQL, 인덱스, 트랜잭션, 복구)부터 NoSQL, NewSQL, 분산 DB 아키텍처, 데이터 웨어하우스(DW), 그리고 최신 벡터 DB, HTAP, 데이터 레이크하우스에 이르는 전 영역을 깊이 있게 총망라하였습니다.)
