+++
title = "16. 빅데이터 키워드 목록"
date = 2026-03-04
[extra]
categories = "studynotes-bigdata"
+++

# 빅데이터 (Big Data) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 빅데이터 전 영역 기술사 수준 핵심 키워드
> ⚡ 빅데이터 기술사 문제: 단순 플랫폼 나열이 아닌 **아키텍처 선택 근거 + 법·제도 + 비즈니스 가치 + 미래 전망** 통합 서술 요구

---

## 1. 빅데이터 개론 / 특성 — 22개

1. 빅데이터 정의 — 3V: Volume(양) / Velocity(속도) / Variety(다양성) (Laney, 2001)
2. 5V — 3V + Veracity(정확성) + Value(가치)
3. 7V — 5V + Visualization(시각화) + Variability(가변성)
4. 빅데이터 도입 필요성 — 데이터 폭증(제타바이트 시대), 비정형 데이터 급증
5. 비정형 데이터 유형 — 텍스트/이미지/동영상/음성/로그/SNS/IoT 센서
6. 반정형 데이터 — JSON/XML/HTML/CSV — 스키마 부분 보유
7. 빅데이터 생태계 — 수집→저장→처리→분석→시각화→활용
8. 빅데이터 vs 전통적 데이터 — RDBMS 한계(수평 확장 불가, 고정 스키마)
9. 데이터 폭증 요인 — IoT/SNS/모바일/센서/영상 CCTV
10. 데이터 민주화 (Data Democratization) — 셀프서비스 분석, 시민 데이터 과학자
11. 데이터 경제 (Data Economy) — 데이터 자산화, 데이터 거래소
12. 마이데이터 (MyData) — 개인정보 자기결정권, 금융 마이데이터
13. 공공 빅데이터 — 공공데이터포털, 행정안전부, 데이터 개방 정책
14. 데이터바우처 사업 — 중소기업 데이터 구매·가공 지원
15. 오픈데이터 원칙 — FAIR (Findable/Accessible/Interoperable/Reusable)
16. 유럽 데이터 전략 — Data Spaces, Gaia-X
17. 국가 데이터 정책 — 데이터기본법, 데이터 산업 진흥법
18. 데이터 주권 (Data Sovereignty) — 국가별 데이터 현지화 규제
19. 개인정보 비식별화 — k-익명성 / l-다양성 / t-근접성
20. 데이터 정형화 비율 — 전체 데이터 중 정형 < 20%, 비정형 > 80%
21. 제타바이트 시대 — 2025년 전 세계 생성 데이터 ~175 ZB
22. 데이터 자산 평가 — 재무적 가치화, ISO/IEC 22123

---

## 2. Hadoop 에코시스템 심화 — 28개

1. Apache Hadoop — 분산 스토리지(HDFS) + 분산 처리(MapReduce) + 자원 관리(YARN)
2. HDFS (Hadoop Distributed File System) — 블록 128MB, 3중 복제, NameNode/DataNode
3. NameNode — 메타데이터 관리, SPOF 우려 → Secondary NameNode / HA NameNode
4. DataNode — 실제 데이터 블록 저장, 주기적 Heartbeat
5. Rack Awareness — 같은 랙 두 복제본 방지, 장애 복구 최적화
6. MapReduce — Map(분산 처리)/Shuffle&Sort/Reduce(집계) 3단계
7. Map 함수 — 입력 → (Key, Value) 쌍 출력
8. Reduce 함수 — 동일 Key의 Value 집계, 최종 결과 출력
9. Shuffle & Sort — Map 출력을 Reduce로 분배 (네트워크 병목)
10. YARN (Yet Another Resource Negotiator) — 자원 관리, Application Master / Container
11. Apache Hive — SQL on Hadoop, HQL, 메타스토어(MySQL/PostgreSQL), 배치형
12. Apache HBase — NoSQL on HDFS, 열 지향, 실시간 랜덤 R/W, ZooKeeper 의존
13. Apache Pig — 데이터 흐름 스크립트 언어 (Pig Latin), 복잡한 ETL
14. Apache Sqoop — RDBMS ↔ HDFS 데이터 임포트/익스포트
15. Apache Flume — 로그 수집 에이전트, Source/Channel/Sink 구조
16. Apache Oozie — Hadoop 워크플로우/코디네이터 스케줄러
17. Apache Zookeeper — 분산 코디네이션 서비스, 리더 선출, 잠금
18. Apache Ambari — Hadoop 클러스터 관리 GUI
19. Cloudera CDH / HDP (Hortonworks) → CDP (Cloudera Data Platform)
20. Apache Tez — DAG 기반 실행 엔진, Hive/Pig 속도 개선
21. Apache Kafka (Hadoop 연동) — Flume 대체, 내구성/처리량↑
22. Apache Storm — 초기 실시간 처리, Spout/Bolt 토폴로지
23. Apache Samza — LinkedIn, Kafka 네이티브 스트리밍
24. HDFS 페더레이션 (Federation) — 다중 NameNode, 네임스페이스 분산
25. HDFS ViewFS — 파일 시스템 투명 접근
26. Small File Problem — HDFS 비효율, HAR/Sequence File/ORC로 해결
27. 데이터 직렬화 — Avro / Protocol Buffers / Thrift / Kryo
28. Hadoop 보안 — Kerberos 인증, Ranger(권한)/Atlas(카탈로그)

---

## 3. 분산 처리 / 스파크 심화 — 24개

1. Apache Spark — 인메모리 분산 처리, MapReduce 대비 최대 100배 빠름
2. RDD (Resilient Distributed Dataset) — 불변, 분산, 결함 허용, Lineage 기반 복구
3. Transformation vs Action — Lazy Evaluation (변환은 지연, 액션은 즉시)
4. DataFrame / Dataset — 스키마 기반, Catalyst 최적화, Type-safe
5. Spark SQL — SQL 쿼리로 DataFrame 처리, Hive 메타스토어 연동
6. Catalyst Optimizer — 논리 → 물리 실행 계획 최적화
7. Tungsten Engine — CPU/메모리 최적화, Codegen, Off-heap 메모리
8. AQE (Adaptive Query Execution) — 런타임 통계 기반 자동 최적화 (Spark 3.0+)
9. Spark Streaming (DStream) — 마이크로배치 스트리밍 (구세대)
10. Structured Streaming — DataFrame API 스트리밍, 연속 처리, Watermark
11. MLlib — 분산 ML 라이브러리 (분류/회귀/군집/추천/PCA)
12. GraphX — 분산 그래프 처리, PageRank
13. Spark 배포 모드 — Local / Standalone / YARN / Kubernetes / Mesos
14. Executor / Driver / Cluster Manager — Spark 실행 구조
15. Shuffle 최적화 — spark.sql.shuffle.partitions, AQE 코어리스
16. 데이터 직렬화 — Kryo > Java, 성능 차이
17. Broadcast Join — 소규모 테이블을 모든 Executor에 복사
18. Skew Join — 데이터 쏠림 해결 (AQE 자동 분할)
19. 파티션 최적화 — repartition / coalesce, 코어 수 × 2~4
20. 체크포인팅 (Checkpointing) — Lineage 단절, 장애 복구 가속
21. Spark History Server — 완료 작업 로그 조회, UI
22. Delta Lake on Spark — ACID 트랜잭션, MERGE INTO, 타임 트래블
23. Photon Engine (Databricks) — 네이티브 벡터화 Spark 실행 엔진
24. Apache Spark 3.5+ 개선 — ANSI SQL 확대, Python API 강화

---

## 4. 스트리밍 / 실시간 처리 — 22개

1. 스트리밍 처리 필요성 — 실시간 이상 감지, 즉각 대응 의사결정
2. Apache Flink — 상태 기반 스트리밍, 이벤트 시간 처리, Exactly-Once
3. Flink 아키텍처 — JobManager / TaskManager / JobGraph
4. DataStream API / Table API & SQL — Flink 두 계층
5. Flink Savepoint / Checkpoint — 상태 저장, 재시작 지점
6. 이벤트 시간 (Event Time) vs 처리 시간 (Processing Time)
7. Watermark — 지연 이벤트 허용 임계, 늦은 데이터 트리거
8. 윈도우 연산 — 텀블링 / 슬라이딩 / 세션 / 글로벌 윈도우
9. 정확히 한 번 (Exactly-Once Semantics) — 2PC + Idempotent Sink
10. Apache Kafka — 내구성 있는 메시지 큐, 스트리밍 기반
11. Kafka 파티셔닝 전략 — 키 기반 / 라운드로빈 / 커스텀
12. Consumer Lag — Kafka 소비 지연 모니터링, Burrow / JMX
13. Kafka MirrorMaker 2 — 클러스터 간 복제, DR
14. Amazon Kinesis Data Streams — 샤드 기반, AWS 관리형
15. Google Pub/Sub — Kafka 대안, GCP, 글로벌 분산
16. Azure Event Hubs — Kafka 호환 API, AMQP 지원
17. Apache Pulsar — Kafka 대안, 컴퓨팅/스토리지 분리, 멀티 테넌시
18. 람다 아키텍처 — 배치(Speed Layer) + 실시간(Batch Layer) + Serving Layer
19. 카파 아키텍처 — 스트리밍만으로 단순화, Kafka + Flink
20. 스트리밍 SQL — ksqlDB (Confluent) / Flink SQL / Spark Structured Streaming
21. CEP (Complex Event Processing) — 패턴 이벤트 감지, Flink CEP
22. 실시간 OLAP — Apache Druid / Apache Pinot / ClickHouse — ms 지연 쿼리

---

## 5. 빅데이터 분석 기법 — 26개

1. 기술 통계 (Descriptive Statistics) — 평균/중앙값/분산/분포 요약
2. 추론 통계 (Inferential Statistics) — 표본 → 모집단 추론, 가설 검정
3. 탐색적 데이터 분석 (EDA) — 패턴 발견, 이상치 탐지, 시각화
4. 회귀 분석 (Regression) — 단순/다중/다항/릿지/라쏘/엘라스틱넷
5. 분류 (Classification) — 로지스틱 회귀 / 트리 / SVM / 앙상블
6. 군집화 (Clustering) — K-Means / DBSCAN / 계층적 / Gaussian Mixture
7. 연관 규칙 (Association Rules) — Apriori / FP-Growth, 지지도/신뢰도/향상도
8. 장바구니 분석 (Market Basket Analysis) — 구매 패턴, 교차 판매
9. 감성 분석 (Sentiment Analysis) — 긍/부정/중립, BERT 기반 심화
10. 텍스트 마이닝 (Text Mining) — TF-IDF / Word2Vec / BERT / LLM
11. 소셜 네트워크 분석 (SNA) — 중심성 / 커뮤니티 탐지 / 영향력
12. 이상 탐지 (Anomaly Detection) — 통계 기반 / ML 기반 / 딥러닝 기반
13. 시계열 분석 (Time Series) — ARIMA / SARIMA / Prophet / LSTM / Transformer
14. 공간 분석 (Spatial Analysis) — 지리정보시스템(GIS), PostGIS
15. 그래프 분석 (Graph Analytics) — PageRank / 커뮤니티 탐지 / 최단 경로
16. 텍스트 요약 — 추출적(Extractive) / 추상적(Abstractive) 요약
17. 토픽 모델링 — LDA / BERTopic / NMF
18. 개체명 인식 (NER) — 인물/장소/조직/날짜 추출
19. 이미지 분석 — CNN 기반 분류/탐지/분할 대용량 배치
20. 로그 분석 — 이상 감지, 보안 이벤트, 패턴 발견
21. 클릭스트림 분석 — 사용자 행동 패턴, 전환율 최적화
22. A/B 테스트 — 실험적 방법론, 통계적 유의성
23. 추천 시스템 — 협업 필터링 / 콘텐츠 기반 / 하이브리드
24. 예측 분석 (Predictive Analytics) — 이탈 예측, 대출 부도, 장비 고장
25. 처방적 분석 (Prescriptive Analytics) — 최적 의사결정 제안
26. 인과 추론 (Causal Inference) — 상관≠인과, DoWhy, 반사실 분석

---

## 6. NoSQL 데이터베이스 — 20개

1. NoSQL 등장 배경 — RDBMS 수평 확장 한계, BASE 원칙
2. BASE 원칙 — Basically Available / Soft State / Eventually Consistent
3. CAP 정리 — Consistency / Availability / Partition Tolerance (2개만 선택)
4. PACELC 이론 — CAP 확장, 지연 vs 일관성 트레이드오프
5. 키-값 (Key-Value) DB — Redis / DynamoDB / Riak — 빠른 조회, 단순 구조
6. Redis — 인메모리, Pub/Sub, 자료구조(String/List/Set/Hash/ZSet), 클러스터
7. 문서형 (Document) DB — MongoDB / CouchDB / Firestore
8. MongoDB 아키텍처 — ReplicaSet / Sharding / Mongos / Config Server
9. 컬럼 패밀리 (Column Family) DB — Cassandra / HBase / ScyllaDB
10. Cassandra — 마스터 없는 링 구조, 토큰 기반 일관성 해시, 튜닝 가능한 일관성
11. 그래프 DB — Neo4j / Amazon Neptune / Memgraph — 관계 쿼리 최적화
12. Cypher 쿼리 언어 (Neo4j) — MATCH / WHERE / RETURN
13. 시계열 DB — InfluxDB / TimescaleDB / QuestDB — 시간 기반 인덱싱
14. 검색 엔진 DB — Elasticsearch / OpenSearch — 역색인, 전문 검색
15. 다중 모델 DB — ArangoDB / SurrealDB — 여러 NoSQL 모델 지원
16. NewSQL — CockroachDB / TiDB / YugabyteDB — SQL + 수평 확장 + ACID
17. 인메모리 DB — Redis / Memcached / SAP HANA — 마이크로초 응답
18. 일관성 수준 선택 — Strong / Bounded Staleness / Session / Consistent Prefix / Eventual
19. 멀티 마스터 복제 — CouchDB / DynamoDB Global Tables
20. 스키마리스 설계 패턴 — 임베딩 vs 참조, 데이터 중복 허용 설계

---

## 7. 데이터 레이크 / 레이크하우스 — 18개

1. 데이터 레이크 (Data Lake) — 원시 데이터 저장, Schema-on-Read, 저비용
2. 데이터 스왐프 (Data Swamp) — 거버넌스 부재, 레이크 변질 위험
3. 데이터 웨어하우스 (DW) — 구조화, Schema-on-Write, 높은 성능
4. 레이크하우스 (Lakehouse) — 레이크(유연성) + DW(ACID/성능), Delta Lakehouse
5. Delta Lake — ACID on Parquet, 타임 트래블, MERGE, 스키마 강제
6. Apache Iceberg — 오픈 테이블 포맷, 히든 파티셔닝, 스냅샷
7. Apache Hudi (Hadoop Upserts Deletes Incrementals) — Uber, CDC 지원
8. Unity Catalog (Databricks) — 레이크하우스 통합 거버넌스
9. 다중 계층 아키텍처 — Bronze(원시) / Silver(정제) / Gold(집계) — Medallion
10. Medallion Architecture — Delta Lake 기반 3계층, Databricks 표준
11. 데이터 메시 (Data Mesh) — 도메인 분권, 데이터 제품화, 연합 거버넌스
12. 데이터 제품 (Data Product) — API 인터페이스, SLA, 품질 지표 보유
13. ELT vs ETL — 클라우드에서 ELT가 주류 (먼저 적재 후 변환)
14. 데이터 패브릭 (Data Fabric) — 위치 무관 지능형 데이터 연결, Gartner
15. 데이터 분석 서비스 — Amazon EMR / Azure HDInsight / GCP Dataproc
16. Databricks — Spark 기반 레이크하우스 플랫폼, Unity Catalog
17. Snowflake on Data Lake — External Table, Iceberg 지원
18. Microsoft Fabric — One Lake, Power BI + Synapse + Data Factory 통합

---

## 8. 빅데이터 시각화 — 14개

1. 데이터 시각화 원칙 — 목적 명확성 / 간결성 / 데이터 잉크 비율 (Tufte)
2. 차트 유형 선택 — 비교(막대)/추세(선)/비율(파이/도넛)/분포(히스토그램/박스)
3. 대시보드 설계 — KPI 중심, 5초 규칙, 인터랙티브
4. Tableau — 드래그앤드롭, VizQL, Extract/Live 연결
5. Power BI — Microsoft 생태계 통합, DAX, Dataflow
6. Looker / Looker Studio — Google, LookML 시맨틱 레이어
7. Apache Superset — 오픈소스, SQL Lab, 다양한 차트
8. Grafana — 메트릭/로그/추적 통합 시각화, 알람
9. Kibana — ELK Stack 시각화, 로그 분석
10. D3.js — JavaScript 기반 커스텀 인터랙티브 시각화
11. Plotly / Dash — Python 기반 인터랙티브 시각화
12. 네트워크 시각화 — Gephi / Cytoscape — 그래프 시각화
13. 지리공간 시각화 — Kepler.gl / Folium / Deck.gl — 지도 기반
14. 빅데이터 시각화 도전 — 수십억 개 포인트, 집계/샘플링/렌더링 최적화

---

## 9. 빅데이터 플랫폼 / 아키텍처 — 16개

1. 빅데이터 플랫폼 선택 기준 — 데이터 규모 / 실시간 여부 / 비용 / 기술 역량
2. On-Premise Hadoop vs Cloud 비교 — 초기 비용 vs OPEX, 유연성
3. 빅데이터 참조 아키텍처 — 수집→저장→처리→분석→서비스→관리
4. 모던 데이터 스택 (MDS) — Fivetran + Snowflake + dbt + Tableau
5. 실시간 + 배치 통합 플랫폼 — Unified Batch/Streaming (Spark/Flink)
6. 데이터 허브 (Data Hub) — 중앙 데이터 집계 및 배포 계층
7. 멀티클라우드 데이터 플랫폼 — Snowflake / Databricks 멀티클라우드 지원
8. 서버리스 빅데이터 — AWS Athena / BigQuery / Redshift Serverless
9. 데이터 오케스트레이션 — Apache Airflow / Dagster / Prefect
10. 데이터 카탈로그 통합 — Glue Catalog / DataHub / OpenMetadata / Alation
11. 확장성 설계 — 수평 확장 / 샤딩 / 파티셔닝 / 클러스터 자동 확장
12. 데이터 컴프레션 전략 — Snappy(속도) / Zstd(압축률) / Gzip(호환성)
13. 컬럼 기반 파일 포맷 — Parquet / ORC / Iceberg / Arrow — 조회 최적화
14. 빅데이터 비용 최적화 — Spot Instance / 컴퓨팅-스토리지 분리 / RI
15. 데이터 이동 비용 — Egress 비용, 리전 내 데이터 로컬화
16. 하이브리드 분석 — 온프레미스 + 클라우드 버스팅

---

## 10. 빅데이터 거버넌스 / 품질 / 법규 — 18개

1. 데이터 거버넌스 정의 — 데이터 소유·관리·사용 원칙 체계
2. 데이터 거버넌스 구성 요소 — 정책/표준/역할/프로세스/도구
3. 데이터 스튜어드 (Data Steward) — 도메인 데이터 책임자
4. 데이터 소유자 (Data Owner) — 비즈니스 책임, 접근 승인
5. 데이터 품질 차원 — 완전성/정확성/일관성/적시성/유일성/유효성
6. 데이터 품질 관리 도구 — Great Expectations / Deequ / Soda Core
7. 데이터 계보 (Data Lineage) — 열 수준 계보, 영향 분석, Apache Atlas
8. 메타데이터 관리 — 비즈니스/기술/운영 메타데이터 3유형
9. 마스터 데이터 관리 (MDM) — 황금 레코드, 중복 제거
10. 데이터 보안 — 암호화(전송/저장) / 접근 제어 / 감사 로그 / DLP
11. 개인정보보호법 빅데이터 특례 — 가명처리 허용 (2020년 데이터 3법)
12. GDPR Article 89 — 과학적 연구 목적 빅데이터 처리 특례
13. 데이터 비식별화 기법 — 데이터 마스킹 / 가명화 / 집계화 / 노이즈 추가
14. 차등 프라이버시 (Differential Privacy) — 통계 쿼리 + 노이즈, Apple/Google
15. 합성 데이터 (Synthetic Data) — 원본과 유사 통계적 특성, 개인정보 대체
16. 데이터 윤리 (Data Ethics) — 알고리즘 편향, 공정성, 투명성
17. 빅데이터 분쟁 — 데이터 소유권, 수집 동의, 목적 외 사용
18. 데이터 감사 (Data Audit) — 접근 이력, 변경 이력, 보관 기간

---

## 11. 빅데이터 산업 응용 — 16개

1. 금융 빅데이터 — 신용평가 / 이상거래탐지(FDS) / 리스크 관리 / 알고트레이딩
2. 의료 빅데이터 — 전자의무기록(EMR) / 유전체 분석 / 임상 예측 / 신약 개발
3. 공공 빅데이터 — 교통 예측 / 범죄 예방 / 도시 계획 / 행정 서비스 개선
4. 제조 빅데이터 — 예지 정비(PdM) / 불량 감지 / 에너지 최적화
5. 유통·물류 빅데이터 — 수요 예측 / 재고 최적화 / 배송 경로 최적화
6. 미디어 빅데이터 — 시청 분석 / 콘텐츠 추천 / 광고 타겟팅
7. SNS 빅데이터 — 여론 분석 / 트렌드 감지 / 인플루언서 분석
8. 스마트시티 빅데이터 — CCTV 분석 / 교통 신호 최적화 / 에너지 그리드
9. 농업 빅데이터 — 정밀 농업 / 날씨 연계 수확량 예측 / 토양 분석
10. 교육 빅데이터 — 학습 분석(Learning Analytics) / 맞춤형 교육
11. 관광 빅데이터 — 관광 수요 예측 / 혼잡도 분석 / 관광 코스 추천
12. 통신 빅데이터 — 네트워크 장애 예측 / 고객 이탈 분석 / QoE 최적화
13. 에너지 빅데이터 — 전력 수요 예측 / 신재생에너지 출력 예측 / 스마트미터
14. 보험 빅데이터 — 보험료 산정 / 사기 탐지 / 언더라이팅 자동화
15. 부동산 빅데이터 — 시세 예측 / 상권 분석 / 인구 이동 분석
16. 국방 빅데이터 — 정보 분석 / 적 행동 예측 / 보안 위협 탐지

---

## 12. 최신 빅데이터 동향 — 12개

1. 레이크하우스 주류화 — Delta/Iceberg/Hudi 3강 경쟁, 개방형 포맷
2. 데이터 메시 확산 — 도메인 소유권, 자율 데이터 제품
3. 실시간 OLAP 성장 — Druid / Pinot / ClickHouse / StarRocks
4. AI + 빅데이터 융합 — 대규모 ML 학습, LLM 기반 데이터 분석
5. Text-to-SQL on BigData — LLM으로 자연어 → 쿼리 자동 생성
6. 스트리밍 우선 아키텍처 — 배치 → 스트리밍 전환, Kappa 아키텍처 강화
7. 데이터 계약 (Data Contract) — 스키마 안정성 보장 생산자-소비자 합의
8. 오픈소스 포맷 경쟁 — Apache Iceberg 사실상 표준화 움직임
9. 양자 컴퓨팅 + 빅데이터 — 최적화 문제, 양자 ML 초기 연구
10. 엣지 빅데이터 — 엣지에서 집계 후 클라우드 전송, 대역폭 절감
11. Databricks vs Snowflake — 레이크하우스 vs DW 진영 경쟁
12. 데이터 옵저버빌리티 — Monte Carlo / Bigeye — 데이터 파이프라인 신뢰성

---

**총 키워드 수: 216개**
