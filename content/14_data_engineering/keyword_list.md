---
title: "Keyword List"
date: "2026-03-04"
tags:
  - "studynote-data-engineering"
weight: 50
---
# 빅데이터 (Big Data) 및 데이터 과학 키워드 목록 (심화 확장판)

IT 관리, 시스템 설계 및 데이터 사이언티스트(DS), 데이터 엔지니어(DE)를 위한 빅데이터 처리 플랫폼, 데이터 마이닝, 데이터 분석 수학/통계, 최신 데이터 레이크하우스 아키텍처 및 기계학습(ML) 전 영역 800대 핵심 키워드입니다.

---

## 1. 빅데이터 인프라 및 분산 처리 시스템 (80개)
1. [빅데이터 3V / 5V - 볼륨(Volume), 속도(Velocity), 다양성(Variety), + 진실성(Veracity), 가치(Value)](@/14_data_engineering/01_infrastructure/001_bigdata_3v_5v.md)
2. [정형 데이터 (Structured Data) - RDBMS 테이블 같이 엄격한 스키마 구조 보유](@/14_data_engineering/01_infrastructure/002_structured_data.md)
3. [반정형 데이터 (Semi-structured Data) - 데이터 내부(태그)에 구조(메타데이터)를 포함 (XML, JSON, 로그)](@/14_data_engineering/01_infrastructure/003_semi_structured_data.md)
4. [비정형 데이터 (Unstructured Data) - 스키마가 없는 텍스트, 음성, 비디오, 이미지 데이터](@/14_data_engineering/01_infrastructure/004_unstructured_data.md)
5. [데이터 웨어하우스 (DW, Data Warehouse) - 전사적 관점의 비즈니스 인텔리전스(BI)를 위한 통합/주제별/시계열 데이터 저장소 (Inmon 모델)](@/14_data_engineering/01_infrastructure/005_data_warehouse.md)
6. [데이터 마트 (Data Mart) - 부서별(영업, 재무 등) 필요에 맞춘 소규모 분석 DB (Kimball 모델)](@/14_data_engineering/01_infrastructure/006_data_mart.md)
7. [데이터 레이크 (Data Lake) - 하둡/S3 등 저렴한 스토리지에 원시(Raw) 형태의 모든 비정형/정형 데이터를 구조화 없이 무한 저장](@/14_data_engineering/01_infrastructure/007_data_lake.md)
8. [데이터 레이크하우스 (Data Lakehouse) - 데이터 레이크의 유연성/저비용과 DW의 ACID 트랜잭션, SQL 성능을 단일 계층에 결합한 현대 아키텍처 (Databricks, Snowflake)](@/14_data_engineering/01_infrastructure/008_data_lakehouse.md)
9. [스키마 온 리드 (Schema-on-Read) - 저장 시엔 원시 그대로 두고, 쿼리(읽기)할 때 스키마를 동적으로 부여 (데이터 레이크)](@/14_data_engineering/01_infrastructure/009_schema_on_read.md)
10. [스키마 온 라이트 (Schema-on-Write) - 저장 전 정규화/ETL을 통해 스키마에 맞게 정제 (DW)](@/14_data_engineering/01_infrastructure/010_schema_on_write.md)
11. [분산 컴퓨팅 스케일 아웃 (Scale-out) - 저가형 범용 x86 서버(Commodity Hardware) 대수를 늘려 성능 무한 확장](@/14_data_engineering/01_infrastructure/011_distributed_computing_scale_out.md)
12. [아파치 하둡 (Apache Hadoop) - 대용량 데이터 분산 저장 및 병렬 처리 자바 오픈소스 프레임워크](@/14_data_engineering/01_infrastructure/012_apache_hadoop.md)
13. [HDFS (Hadoop Distributed File System) - 거대 파일을 기본 128MB 블록 단위로 쪼개 수많은 데이터노드에 분산 저장](@/14_data_engineering/01_infrastructure/013_hdfs.md)
14. [네임노드 (NameNode) - 파일 디렉터리, 블록 맵핑 메타데이터 관리 마스터 노드 (SPOF 존재)](@/14_data_engineering/01_infrastructure/014_namenode.md)
15. [데이터노드 (DataNode) - 실제 데이터를 보관하는 수많은 워커 노드](@/14_data_engineering/01_infrastructure/015_datanode.md)
16. [복제 (Replication) 계수 3 - 하드웨어 장애(고장)에 대비해 동일 블록을 서로 다른 랙(Rack) 서버에 3벌 복사하여 결함 허용(Fault Tolerance) 달성](@/14_data_engineering/01_infrastructure/016_replication_factor.md)
17. [랙 인지 (Rack Awareness) 알고리즘 - 데이터 복제 시 물리적으로 동일한 스위치 전원을 공유하는 랙에 전부 넣지 않고 분산 배치](@/14_data_engineering/01_infrastructure/017_rack_awareness.md)
18. [맵리듀스 (MapReduce) - 디스크 I/O 기반 분산 병렬 연산 프레임워크 (Map: 매핑/필터링 -> Shuffle: 데이터 섞기 -> Reduce: 집계합산)](@/14_data_engineering/01_infrastructure/018_mapreduce.md)
19. [데이터 지역성 (Data Locality) - 연산 코드를 데이터가 이미 존재하는 노드로 전송하여 네트워크 전송 오버헤드 최소화 (연산 이동이 데이터 이동보다 싸다)](@/14_data_engineering/01_infrastructure/019_data_locality.md)
20. [YARN (Yet Another Resource Negotiator) - 하둡 2.0 클러스터 자원(CPU/Mem) 스케줄링 통합 관리자](@/14_data_engineering/01_infrastructure/020_yarn.md)
21. [아파치 스파크 (Apache Spark) - 하둡 맵리듀스의 느린 디스크 반복 접근 단점을 극복한 인메모리(In-Memory) 기반 초고속 범용 분산 처리 엔진](@/14_data_engineering/01_infrastructure/021_apache_spark_in_memory.md)
22. [RDD (Resilient Distributed Dataset) - 스파크 핵심. 탄력적이고 불변하는 메모리 데이터 구조. 장애 시 리니지(계보) 연산 기록을 바탕으로 즉시 자가 복구](@/14_data_engineering/01_infrastructure/022_apache_kafka.md)
23. [지연 평가 (Lazy Evaluation) - 트랜스포메이션 연산(map, filter)은 즉시 실행 안하고 DAG 궤적만 그리다가, 액션(count, save) 명령 시 옵티마이저가 묶어서 한 번에 최적 처리](@/14_data_engineering/01_infrastructure/023_lazy_evaluation.md)
24. [아파치 플링크 (Apache Flink) - 배치 모사가 아닌 네이티브 이벤트 기반 진정한 실시간 스트림 처리 엔진 (상태 관리, 워터마크 지원 우수)](@/14_data_engineering/01_infrastructure/024_apache_flink_stream_processing.md)
25. [아파치 카프카 (Apache Kafka) - 분산 이벤트 스트리밍 플랫폼 (Pub/Sub 메시지 큐), 고성능 로그 파이프라인](@/14_data_engineering/01_infrastructure/025_spark_rdd_resilient_distributed_dataset.md)
26. [토픽(Topic)과 파티션(Partition) - 메시지 저장 경로 / 파티션 분할을 통한 컨슈머 병렬 분산 처리 달성](@/14_data_engineering/01_infrastructure/026_topic_partition.md)
27. [오프셋 (Offset) 보존 및 컨슈머 그룹 (Consumer Group) 부하 분배 원리](@/14_data_engineering/01_infrastructure/027_offset_consumer_group.md)
28. [아파치 하이브 (Apache Hive) - 맵리듀스 자바 코드 대신 HiveQL(SQL) 쿼리를 날려주는 하둡 데이터 웨어하우스 추상화](@/14_data_engineering/01_infrastructure/028_apache_hive.md)
29. [아파치 즈쿠퍼 (Apache ZooKeeper) - 분산 클러스터 노드 상태 동기화, 분산 락, 스플릿 브레인 방지(리더 선출) 코디네이션](@/14_data_engineering/01_infrastructure/029_apache_zookeeper.md)
30. [스플릿 브레인 (Split Brain) 장애와 Quorum(정족수 과반 투표) 방어망 체계](@/14_data_engineering/01_infrastructure/030_split_brain_quorum.md)
31. [아파치 우지 (Apache Oozie) / 아파치 에어플로우 (Apache Airflow) - 복잡한 분산 파이프라인 작업 간 DAG 의존성 스케줄링 관리](@/14_data_engineering/01_infrastructure/031_apache_oozie_airflow.md)
32. [CDC (Change Data Capture) - 기존 RDBMS(운영 DB)의 트랜잭션 로그(Redo, Binlog)를 긁어내 DB 성능 부하 없이 실시간으로 카프카나 DW에 변경/동기화 시키는 데이터 이관 핵심 기술 (Debezium)](@/14_data_engineering/01_infrastructure/032_cdc.md)
33. [ETL (Extract, Transform, Load) - 운영계에서 데이터 추출 후 별도 서버에서 정제(T)하여 DW 적재(L) (병목 발생)](@/14_data_engineering/01_infrastructure/033_etl.md)
34. [ELT (Extract, Load, Transform) - 추출 데이터를 바로 클라우드 DW(Snowflake, BigQuery)로 쏟아넣고, 클라우드 DB 연산력 자체를 이용해 그 안에서 SQL로 정제 변환 (현대 대세)](@/14_data_engineering/01_infrastructure/034_elt.md)
35. [NoSQL (Not Only SQL) 데이터베이스 구조 유형 4가지](@/14_data_engineering/01_infrastructure/035_nosql.md)
36. [키-값 저장소 (Key-Value) - Redis, Memcached (인메모리 초고속 세션/캐시)](@/14_data_engineering/01_infrastructure/036_key_value.md)
37. [도큐먼트 저장소 (Document) - MongoDB (JSON 형태 유연한 계층 저장, 부분 필드 검색 용이)](@/14_data_engineering/01_infrastructure/037_document.md)
38. [컬럼 패밀리 저장소 (Wide-Column) - HBase, Cassandra (수십억 행의 시계열 로깅 데이터 쓰기 최적화)](@/14_data_engineering/01_infrastructure/038_wide_column.md)
39. [그래프 저장소 (Graph DB) - Neo4j (노드와 엣지 관계 맵핑, 조인 오버헤드 없는 최단경로/추천 탐색)](@/14_data_engineering/01_infrastructure/039_graph_db.md)
40. [CAP 정리 (CAP Theorem) - 분산 데이터베이스는 일관성(Consistency), 가용성(Availability), 파티션 감내(Partition Tolerance) 세 가지를 동시에 완벽히 만족할 수 없음 (P는 필수이므로 CP 또는 AP 모델 선택)](@/14_data_engineering/01_infrastructure/040_cap_theorem_consistency_availability_partition.md)
41. [PACELC 정리 - 장애(P) 시 A와 C의 상충, 정상(E) 시 지연(Latency)과 일관성(C)의 상충 관계 확장 정리](@/14_data_engineering/01_infrastructure/041_pacelc_theorem_cap_extension.md)
42. [BASE 특성 - ACID의 반대 개념. NoSQL 특성으로 Basically Available, Soft-state, Eventually Consistent(일정 시간 지나면 결국 동기화됨)](@/14_data_engineering/01_infrastructure/042_base_characteristics_nosql_eventual_consistency.md)
43. [람다 아키텍처 (Lambda Architecture) - 빅데이터 처리 시 과거 배치는 하둡(Batch Layer)으로, 실시간 처리는 스트리밍(Speed Layer)으로 듀얼 구축하여 뷰에서 합치는 모델 (복잡성 증가 단점)](@/14_data_engineering/01_infrastructure/043_lambda_architecture_batch_speed_layer.md)
44. [카파 아키텍처 (Kappa Architecture) - 람다 단점 극복, 배치 레이어를 버리고 과거/실시간 모든 데이터를 카프카 기반 단일 스트림 계층으로 통일 처리](@/14_data_engineering/01_infrastructure/044_kappa_architecture_single_streaming_layer.md)
45. [컬럼 지향 저장소 (Columnar Storage) 포맷 - RDB처럼 로우(행) 단위 저장이 아니라, 컬럼(열) 단위로 압축 보관 (Apache Parquet, ORC). OLAP 쿼리 시 불필요한 필드는 디스크에서 읽지 않아 성능 극대화](@/14_data_engineering/01_infrastructure/045_columnar_storage_format_parquet_orc.md)
46. [LSM 트리 (Log-Structured Merge-Tree) - 카산드라, RocksDB 스토리지 코어 엔진. 디스크 랜덤 쓰기 병목을 막기 위해 멤테이블(Memory)에 순차 기록 후 꽉 차면 SS테이블로 디스크 순차 플러시(Flush) (쓰기 속도 극대화)](@/14_data_engineering/01_infrastructure/046_lsm_tree_log_structured_merge.md)
47. [콤팩션 (Compaction)과 툼스톤 (Tombstone) - 디스크 파편화 병합 및 삭제 플래그(비석) 처리 기법](@/14_data_engineering/01_infrastructure/047_compaction_and_tombstone.md)
48. [컨시스턴트 해싱 (Consistent Hashing) - DB 노드 증설/삭제 시 전체 데이터 리밸런싱 해시 이동을 최소화하는 원형 링(Ring) 분할 구조](@/14_data_engineering/01_infrastructure/048_consistent_hashing_ring_structure.md)
49. [데이터 메시 (Data Mesh) - 데이터 인프라 조직론 혁신. 사일로화된 중앙 집중식 데이터팀 구조를 타파하고, 각 현업 도메인 부서가 분산 오너십을 갖고 '데이터를 하나의 독립 프로덕트'로 직접 제공](@/14_data_engineering/01_infrastructure/049_data_mesh_distributed_ownership.md)
50. [데이터 패브릭 (Data Fabric) - 물리적으로 흩어진 멀티 클라우드 DB 사일로들을 복제/이동(ETL) 없이, 지능화된 AI 메타데이터 가상화 계층(Data Virtualization)으로 연결해 실시간 단일 뷰로 활용하는 아키텍처](@/14_data_engineering/01_infrastructure/050_data_fabric_virtualization.md)
51. [데이터 카탈로그 (Data Catalog) - 메타데이터를 통합 수집/태깅하여 분석가들이 데이터를 구글처럼 쉽게 검색(Data Discovery)하고 권한을 통제하는 시스템 (AWS Glue, Amundsen)](@/14_data_engineering/01_infrastructure/051_data_catalog_metadata_discovery.md)
52. [데이터 리니지 (Data Lineage) - 데이터의 출처 소스부터 전처리 단계, 최종 타겟 대시보드까지의 데이터 흐름과 변환 이력을 족보처럼 시각적으로 추적하는 체계 (규제 감사, 영향도 분석 핵심)](@/14_data_engineering/01_infrastructure/052_data_lineage_traceability_governance.md)
53. [데이터옵스 (DataOps) - 데이터 파이프라인 개발에 DevOps 사상 적용. 품질 테스트 자동화(CI/CD), 코드로서의 파이프라인 버저닝 관리 (dbt 툴 등 활용)](@/14_data_engineering/01_infrastructure/053_dataops_ci_cd_data_pipeline.md)
54. [오픈 테이블 포맷 (Apache Iceberg, Delta Lake, Apache Hudi) - 데이터 레이크하우스를 완성하는 핵심 계층. 파케이 파일 덩어리 위에 RDB 수준의 트랜잭션(ACID) 제어, 타임트래블(스냅샷 롤백), 스키마 에볼루션 기능 부여](@/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi.md)
55. [스토리지와 컴퓨팅의 분리 (Separation of Compute and Storage) 클라우드 DW 스케일링 특성](@/14_data_engineering/01_infrastructure/055_separation_of_compute_and_storage_cloud_dw.md)
56. [데이터 가상화 연방 쿼리 (Federated Query) 엔진 (Trino, Presto)](@/14_data_engineering/01_infrastructure/056_data_virtualization_federated_query_trino.md)
57. [시계열 데이터베이스 다운샘플링 (Downsampling) 보존 정책 (Retention)](@/14_data_engineering/01_infrastructure/057_tsdb_downsampling_retention_policy.md)
58. [뉴에스큐엘 (NewSQL) 글로벌 스패너 (Spanner) 트루타임 분산 트랜잭션 융합](@/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction.md)
59. [블룸 필터 (Bloom Filter) 디스크 랜덤 I/O 긍정 오류 배제 확률망 검색](@/14_data_engineering/01_infrastructure/059_bloom_filter_false_positive_disk_io.md)
60. [다크 데이터 (Dark Data) 발굴 자산화 및 프라이버시 클린 룸 샌드박싱 결합망](@/14_data_engineering/01_infrastructure/060_dark_data_discovery_privacy_clean_room.md)

## 2. 데이터 분석 수학, 통계 및 데이터 마이닝 (60개)
61. [데이터 마이닝 (Data Mining) 프레임워크 - KDD (지식 탐색 프로세스: 선택->전처리->변환->마이닝->해석), CRISP-DM 모델](@/14_data_engineering/02_math_mining/061_data_mining_framework_kdd_crisp_dm.md)
62. [탐색적 데이터 분석 (EDA, Exploratory Data Analysis) - 가설 수립 전 데이터의 패턴, 이상치, 통계적 특성을 시각화/요약하여 통찰 도출](@/14_data_engineering/02_math_mining/062_eda_exploratory_data_analysis.md)
63. [중심 경향도 (평균, 중앙값, 최빈값) / 산포도 (분산, 표준편차, 사분위수 범위 IQR)](@/14_data_engineering/02_math_mining/063_central_tendency_dispersion_variance_iqr.md)
64. [왜도 (Skewness / 비대칭 쏠림) / 첨도 (Kurtosis / 꼬리 두께 뾰족함)](@/14_data_engineering/02_math_mining/064_skewness_kurtosis_log_transformation.md)
65. [피어슨 상관 계수 (Pearson Correlation Coefficient) - 두 연속형 변수 간의 선형적 비례 관계 측정 (-1.0 ~ 1.0)](@/14_data_engineering/02_math_mining/065_pearson_correlation_coefficient_multicollinearity.md)
66. [스피어만 순위 상관 계수 (Spearman Rank Correlation) - 서열/비선형적 비모수 상관 분석](@/14_data_engineering/02_math_mining/066_spearman_rank_correlation_nonparametric_robustness.md)
67. [가설 검정 프로세스 - 귀무 가설(H0, 차이/효과 없음) vs 대립 가설(H1, 차이 입증)](@/14_data_engineering/02_math_mining/067_hypothesis_testing_null_alternative_p_value.md)
68. [유의 수준 (Alpha) 과 유의 확률 (p-value) - p-value < 0.05 이면 우연히 일어날 확률이 극히 적으므로 귀무 가설 기각(유의미함)](@/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis.md)
69. [1종 오류 (참인 H0 기각) / 2종 오류 (거짓인 H0 기각 실패) / 검정력 (Power)](@/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power.md)
70. [T-검정 (t-Test) - 두 집단 간 평균 차이 통계적 검증 (독립 표본, 대응 표본)](@/14_data_engineering/02_math_mining/070_t_test_independent_paired_mean_difference.md)
71. [분산 분석 (ANOVA) - 3개 이상 다수 집단 간 평균 차이 검증 (F-분포 활용)](@/14_data_engineering/02_math_mining/071_anova_analysis_of_variance_f_value_post_hoc.md)
72. [카이제곱 검정 (Chi-square Test) - 범주형 명목 데이터의 독립성/적합성 검증 (교차 분석)](@/14_data_engineering/02_math_mining/072_chi_square_test_categorical_independence_goodness_of_fit.md)
73. [중심 극한 정리 (CLT, Central Limit Theorem) - 모집단 분포와 상관없이 표본의 크기(n)가 30 이상 크면 표본 평균의 분포는 정규 분포(종 모양)를 따른다는 통계학 대원칙](@/14_data_engineering/02_math_mining/073_central_limit_theorem_clt_sample_mean_normal_distribution.md)
74. [대수의 법칙 (Law of Large Numbers) - 시행을 무한히 반복하면 표본 평균이 모평균에 수렴](@/14_data_engineering/02_math_mining/074_law_of_large_numbers_lln_convergence_probability.md)
75. [조건부 확률 (Conditional Probability) 및 베이즈 정리 (Bayes' Theorem) 사후 확률 계산](@/14_data_engineering/02_math_mining/075_conditional_probability_bayes_theorem_posterior.md)
76. [이상치 (Outlier) 탐지 기법 - IQR 1.5배 벗어남, Z-Score 3 이상, DBSCAN, Isolation Forest 알고리즘](@/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest.md)
77. [결측치 (Missing Value) 처리 기법 - 단순 삭제, 평균/중앙값 대치, 다중 대치법(MICE), K-NN 대치 보간](@/14_data_engineering/02_math_mining/077_missing_value_imputation_mice_knn_dropna.md)
78. [데이터 스케일링 - 정규화 (Normalization / Min-Max 0~1 매핑), 표준화 (Standardization / 평균 0 분산 1 Z-Score 치환) (거리 기반 알고리즘 K-NN, SVM 필수 전처리)](@/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score.md)
79. [원-핫 인코딩 (One-hot Encoding) - 범주형 문자를 기계가 인식하도록 0과 1 희소 벡터 배열로 더미 변수(Dummy Variable)화](@/14_data_engineering/02_math_mining/079_one_hot_encoding_categorical_dummy_variable.md)
80. [다중 공선성 (Multicollinearity) 문제 - 회귀 분석 시 독립변수들끼리 너무 강한 상관관계를 가져 회귀 계수(기여도)가 왜곡되는 현상 (VIF 분산 팽창 지수 10 이상 시 변수 축소)](@/14_data_engineering/02_math_mining/080_multicollinearity_vif_variance_inflation_factor_regression.md)
81. [차원 축소 (Dimensionality Reduction) - 주성분 분석 (PCA, Principal Component Analysis), 변수의 분산(정보량)을 최대로 보존하는 직교 축 도출 변환 (고유값 분해 활용)](@/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis.md)
82. [선형 판별 분석 (LDA) - 클래스 간 분산 최대화, 내 분산 최소화 차원 축소 (지도 학습)](@/14_data_engineering/02_math_mining/082_lda_linear_discriminant_analysis_classification.md)
83. [연관 규칙 탐색 (Association Rule) - 장바구니 분석 (기저귀와 맥주), Apriori 알고리즘](@/14_data_engineering/02_math_mining/083_association_rule_apriori_market_basket.md)
84. [지지도 (Support) - 전체 거래 중 A와 B가 동시에 포함된 거래 비율](@/14_data_engineering/02_math_mining/084_support_association_rule_transaction.md)
85. [신뢰도 (Confidence) - A를 구매한 거래 중 B도 함께 구매한 조건부 확률 비율](@/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability.md)
86. [향상도 (Lift) - 우연적 구매를 배제한, A 구매가 B 구매를 얼마나 끌어올리는지 실제 효과 (Lift > 1 이면 유의미)](@/14_data_engineering/02_math_mining/086_lift_association_rule_marketing.md)
87. [FP-Growth 알고리즘 - Apriori의 반복 DB 스캔 속도 한계를 타파한 트리(Tree) 구조 빈발 항목 탐색법](@/14_data_engineering/02_math_mining/087_fp_growth_algorithm_frequent_pattern_tree.md)
88. [머신러닝 교차 검증 (K-Fold Cross Validation) - 훈련 데이터를 K개 조각으로 나누어 학습/검증을 교대로 반복 평가하여 과적합(Overfitting) 방지 및 일반화 검증](@/14_data_engineering/02_math_mining/088_k_fold_cross_validation_overfitting_generalization.md)
89. [머신러닝 평가 지표 혼동 행렬 (Confusion Matrix) - TP, FP, FN, TN 분할 통계표](@/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn.md)
90. [정확도 (Accuracy) - 전체 모수 중 1과 0을 모두 맞춘 정답 비율 (암 환자 데이터 등 심한 불균형 Data에서는 왜곡 함정 발생)](@/14_data_engineering/02_math_mining/090_accuracy_precision_recall_f1_score.md)
91. [정밀도 (Precision) - 모델이 "양성(Positive)"으로 예측한 것 중에 실제 양성의 비율 (FP 억제가 중요할 때, 스팸 필터링)](@/14_data_engineering/02_math_mining/091_precision_vs_recall_tradeoff.md)
92. [재현율 (Recall / 민감도) - 실제 "양성"인 데이터 전체 중에서 모델이 놓치지 않고 찾아낸 양성의 비율 (FN 억제가 중요할 때, 암 진단/불량 탐지)](@/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate.md)
93. [F1-Score - 정밀도와 재현율의 조화 평균 (불균형 데이터 평가 제1지표)](@/14_data_engineering/02_math_mining/093_f1_score_harmonic_mean.md)
94. [ROC 곡선 (Receiver Operating Characteristic) - 분류 모델 임계치 변화에 따른 FPR(위양성률) 대비 TPR(재현율) 그래프 모형](@/14_data_engineering/02_math_mining/094_roc_curve_auc_classification_performance.md)
95. [AUC (Area Under Curve) - ROC 곡선 아래 넓이 척도 (1.0에 가까울수록 완벽한 모델)](@/14_data_engineering/01_infrastructure/095_concept.md)
96. [불균형 데이터 증강 (Oversampling) - SMOTE (Synthetic Minority Over-sampling Technique) 알고리즘 (K-NN 이웃 선형 보간 기반 가상 합성 데이터 생성망)](@/14_data_engineering/02_math_mining/096_oversampling_smote.md)
97. [회귀 분석 지표 - MSE (평균 제곱 오차), RMSE (루트 보정), MAE (절대값 오차)](@/14_data_engineering/02_math_mining/097_regression_metrics_mse_rmse_mae.md)
98. [결정 계수 (R-Squared, R^2) - 0~1 사이값, 독립변수가 종속변수의 변동(Variance)을 얼마나 완벽히 설명하는가 (SSR/SST) 모델 설명력](@/14_data_engineering/02_math_mining/098_coefficient_of_determination_r_squared.md)
99. [A/B 테스트 검정력 (Power) 설계 및 p-value 해킹 통계 조작 한계](@/14_data_engineering/02_math_mining/099_ab_testing_statistical_power.md)
100. [K-Means 군집화 (Clustering) 엘보우 (Elbow) 기법 및 실루엣 (Silhouette) 스코어 클러스터 응집도 밀도 측정 함수](@/14_data_engineering/02_math_mining/100_k_means_clustering_elbow_silhouette.md)
101. [나이브 베이즈 분류 (Naive Bayes) 조건부 독립 라플라스 스무딩 결합](@/14_data_engineering/02_math_mining/101_naive_bayes_classifier.md)
102. [회귀 라쏘 (Lasso / L1) 및 릿지 (Ridge / L2) 패널티 정규화 식 파싱](@/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization.md)
103. [로지스틱 회귀 시그모이드 분류 로짓 곡선 함수](@/14_data_engineering/02_math_mining/103_logistic_regression_sigmoid.md)
104. [퍼셉트론 선형 분류 SVM 마진 튜브 서포트 벡터 내적](@/14_data_engineering/02_math_mining/104_svm_support_vector_machine.md)
105. [TF-IDF 및 텍스트 마이닝 코사인 유사도 벡터 탐색](@/14_data_engineering/02_math_mining/105_tf_idf_cosine_similarity.md)
106. [마할라노비스 거리 통계 이상치 파악](@/14_data_engineering/02_math_mining/106_mahalanobis_distance.md)
107. [텐서플로우 배열 스칼라 벡터 차원 수학](@/14_data_engineering/02_math_mining/107_tensorflow_array_tensor.md)
108. [지니 불순도 정보 이득 트리 분할 분산](@/14_data_engineering/02_math_mining/108_gini_impurity.md)
109. [유클리드 거리 L2, 맨해튼 거리 L1 측정](@/14_data_engineering/02_math_mining/109_euclidean_vs_manhattan_distance.md)
110. [편향 분산 트레이드 오프 오버피팅 언더피팅](@/14_data_engineering/02_math_mining/110_bias_variance_tradeoff.md)
111. [마르코프 체인 시간 전이 행렬 시계열](@/14_data_engineering/02_math_mining/111_markov_chain_transition_matrix.md)
112. [로버스트 (Robust) 중앙값 절사 평균](@/14_data_engineering/02_math_mining/112_robust_statistics_median_trimmed_mean.md)
113. [다차원 표면 매니폴드 가정 매핑](@/14_data_engineering/02_math_mining/113_manifold_hypothesis_dimensionality_reduction.md)
114. [가우시안 혼합 모델 GMM EM](@/14_data_engineering/02_math_mining/114_gaussian_mixture_model.md)
115. [밀도 군집 DBSCAN 노이즈 식별](@/14_data_engineering/02_math_mining/115_dbscan_clustering.md)
116. [커널 밀도 추정 KDE 스무딩](@/14_data_engineering/02_math_mining/116_kernel_density_estimation.md)
117. [베이즈 오류 최저 한계](@/14_data_engineering/02_math_mining/117_bayes_error.md)
118. [정보 이론 교차 엔트로피 KLD 발산](@/14_data_engineering/02_math_mining/118_cross_entropy_kl_divergence.md)
119. [앙상블 조합 보팅 통계망](@/14_data_engineering/02_math_mining/119_ensemble_voting_methods.md)
120. [부스팅 경사 하강 수치 오차 보완](@/14_data_engineering/02_math_mining/120_concept.md)

## 3. 머신러닝/딥러닝 알고리즘 및 초거대 AI (LLM) 트렌드 (60개)
121. [지도 학습 (Supervised Learning) - 정답(Label)이 달린 데이터를 입력하여 회귀/분류 모델 훈련](@/14_data_engineering/03_ml_dl_llm/121_supervised_learning.md)
122. [비지도 학습 (Unsupervised Learning) - 정답 없이 데이터 자체의 숨겨진 패턴, 군집, 차원 축소 연산](@/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning.md)
123. [강화 학습 (Reinforcement Learning) - 시뮬레이션 환경(MDP)에서 에이전트가 행동을 취하고 보상(Reward)을 최대화하는 방향으로 시행착오 학습 (Q-Learning)](@/14_data_engineering/03_ml_dl_llm/123_reinforcement_learning.md)
124. [결정 트리 (Decision Tree) - 스무고개 하듯 조건 분기 트리 생성 (정보 이득 극대화, 과적합 위험 높음)](@/14_data_engineering/03_ml_dl_llm/124_decision_tree.md)
125. [앙상블 학습 (Ensemble Learning) - 여러 약한 분류기를 묶어 성능과 일반화 극대화](@/14_data_engineering/03_ml_dl_llm/125_ensemble_learning.md)
126. [배깅 (Bagging, Bootstrap Aggregating) - 훈련 데이터를 랜덤 복원 추출(Bootstrap)해 여러 모델을 병렬 병렬 학습 후 다수결 (Random Forest, 분산 감소 효과)](@/14_data_engineering/03_ml_dl_llm/126_bagging_random_forest.md)
127. [부스팅 (Boosting) - 순차적 직렬 학습, 이전 트리가 틀린 데이터에 가중치 페널티를 주어 다음 트리가 보완 학습 (Gradient Boosting, XGBoost, LightGBM, 편향 감소 효과 극대화)](@/14_data_engineering/03_ml_dl_llm/127_boosting.md)
128. [인공 신경망 (ANN) 다층 퍼셉트론 (MLP) 비선형 은닉층 아키텍처](@/14_data_engineering/03_ml_dl_llm/128_ann_mlp.md)
129. [활성화 함수 (Activation Function) - 선형 덧셈 값을 비선형으로 구부려 복잡한 차원을 해석하게 만듦 (Sigmoid, Tanh, ReLU)](@/14_data_engineering/03_ml_dl_llm/129_activation_function.md)
130. [ReLU (Rectified Linear Unit) 함수 - 양수면 자기 자신, 음수면 0. 기존 Sigmoid가 역전파 시 발생시키던 '기울기 소실(Vanishing Gradient)' 문제를 해결한 딥러닝 부흥의 1등 공신](@/14_data_engineering/03_ml_dl_llm/130_relu_activation_function.md)
131. [손실 함수 (Loss Function) 및 옵티마이저 (Optimizer) 경사 하강법 (Gradient Descent)](@/14_data_engineering/03_ml_dl_llm/131_loss_function_optimizer_gradient_descent.md)
132. [Adam 옵티마이저 - 모멘텀(관성) 방향 가속과 RMSProp(적응형 스텝폭 축소)을 융합한 최신 수리 최적화 표준](@/14_data_engineering/03_ml_dl_llm/132_adam_optimizer.md)
133. [역전파 (Backpropagation) 연쇄 미분 오차 전달](@/14_data_engineering/03_ml_dl_llm/133_backpropagation_chain_rule.md)
134. [규제(Regularization) 과적합 방지 기법 - 가중치 감쇠(L1/L2), 드롭아웃(Dropout, 임의 뉴런 제거), 조기 종료(Early Stopping), 배치 정규화(Batch Normalization)](@/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm.md)
135. [CNN (합성곱 신경망) - 이미지 인식 특화. 합성곱 층(커널 필터 이동, 특성맵 추출) + 풀링 층(해상도 압축, 공간 불변성 확보)으로 구성](@/14_data_engineering/03_ml_dl_llm/135_cnn_convolutional_neural_network.md)
136. [RNN (순환 신경망) - 텍스트/음성 등 순서(시퀀스)가 있는 시계열 데이터. 이전 은닉 상태(과거 정보)가 다음 텐서 입력으로 순환](@/14_data_engineering/03_ml_dl_llm/136_rnn_recurrent_neural_network.md)
137. [LSTM (장단기 메모리) / GRU - 순환 신경망이 길어질수록 과거 정보를 까먹는(장기 의존성) 문제를 해결하기 위해 '셀 상태 컨베이어 벨트'와 게이트(망각, 입력, 출력) 구조 부착](@/14_data_engineering/03_ml_dl_llm/137_lstm_gru_long_short_term_memory.md)
138. [어텐션 메커니즘 (Attention) - 고정된 길이 압축 병목(Context Vector)의 한계를 깨고, 디코더가 매 단어 출력 시마다 인코더 입력 문장 전체 중 '가장 연관도(가중치)가 높은 단어'를 동적으로 다시 들여다보게 하는 혁신적 수리 텐서 매핑](@/14_data_engineering/03_ml_dl_llm/138_attention_mechanism_dynamic_weight.md)
139. [트랜스포머 (Transformer) 아키텍처 (2017) - RNN과 CNN을 아예 버리고 오직 '어텐션 병렬 연산'만으로 모델을 구성하여 훈련 속도를 지수적으로 폭발시킴 (초거대 AI 탄생의 시발점)](@/14_data_engineering/03_ml_dl_llm/139_transformer_architecture_self_attention.md)
140. [셀프 어텐션 (Self-Attention) / 멀티 헤드 어텐션 / 포지셔널 인코딩(위치 정보 주입) 구조체](@/14_data_engineering/03_ml_dl_llm/140_self_attention_multihead_positional_encoding.md)
141. [BERT - 트랜스포머의 '인코더'만 채용, 텍스트 양방향 문맥을 완벽히 이해해 빈칸 채우기(MLM) 등 언어 이해 분류에 최적 (구글)](@/14_data_engineering/03_ml_dl_llm/141_bert_encoder_mlm_bidirectional.md)
142. [GPT - 트랜스포머의 '디코더'만 채용, 과거 단어 컨텍스트를 보고 그 다음 올 단어 확률을 자동 회귀(Autoregressive) 생성 예측에 최적 (OpenAI)](@/14_data_engineering/03_ml_dl_llm/142_gpt_decoder_autoregressive_generation.md)
143. [파운데이션 모델 (Foundation Model) - 초거대 파라미터(수백억~수천억) 모델을 테라바이트급 무라벨 원시 텍스트로 사전 자기지도 학습(Pre-training)시켜, 세상 지식의 범용 베이스를 구축한 기본 엔진 (Llama, Claude 등)](@/14_data_engineering/03_ml_dl_llm/143_foundation_model_llm_pretraining.md)
144. [미세 조정 (Fine-Tuning / 파인 튜닝) 및 전이 학습 - 범용 사전 학습 모델 가중치를 기반으로 특정 도메인(법률, 의학) 데이터셋을 소량 추가 훈련시켜 목적에 맞게 전이](@/14_data_engineering/03_ml_dl_llm/144_fine_tuning_transfer_learning.md)
145. [파라미터 효율적 미세 조정 (PEFT) 및 LoRA (Low-Rank Adaptation) 기법 - 초거대 모델 전체 가중치를 훈련하려면 막대한 VRAM 메모리가 필요하므로, 기존 뼈대는 얼리고(Freeze) 저차원 분해 행렬 어댑터만 삽입해 훈련 후 병합하는 최적 파인튜닝 가속 기술](@/14_data_engineering/03_ml_dl_llm/145_peft_lora_low_rank_adaptation.md)
146. [양자화 (Quantization / QLoRA) 모델 경량화 - 부동소수점 FP32 파라미터를 INT8, INT4 등 정수로 압축하여 모바일/온디바이스(엣지)에 배포 구동 가능화](@/14_data_engineering/03_ml_dl_llm/146_quantization_qlora_model_compression.md)
147. [인스트럭션 튜닝 (Instruction Tuning) - 기본 모델을 "질문-답변" 지시어 포맷에 찰떡같이 응답하도록 대화형 특화 추가 훈련](@/14_data_engineering/03_ml_dl_llm/147_instruction_tuning_rlhf_alignment.md)
148. [RLHF (인간 피드백 기반 강화학습) - LLM이 내뱉는 윤리 위반 텍스트를 막기 위해, 인간이 "더 유용한 답변"에 랭킹을 매긴 리워드 모델(Reward Model)을 통과시켜 PPO 강화학습으로 모델 행동을 통제 정렬(Alignment)](@/14_data_engineering/03_ml_dl_llm/148_rlhf_human_feedback_reinforcement.md)
149. [프롬프트 엔지니어링 (Prompt 엔진ering) - 제로샷, 퓨샷(Few-shot), Chain of Thought (사고 사슬, 단계별 논리 추론 유도)](@/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot.md)
150. [할루시네이션 (Hallucination / 환각) 및 RAG (검색 증강 생성) 아키텍처 - LLM의 가장 큰 취약점인 '거짓말'을 막기 위해, 기업 프라이빗 DB를 벡터 DB로 구축해놓고 유저 질문 시 검색된 실제 팩트 문서 문단을 프롬프트에 주입(Augment)하여 정답 생성망 유도](@/14_data_engineering/03_ml_dl_llm/150_hallucination_rag_retrieval_augmented_generation.md)
151. [벡터 데이터베이스 (Vector DB, Pinecone/Milvus) - 비정형 문자열을 임베딩 텐서 좌표로 변환 저장하고 코사인 유사도(ANN: HNSW, IVFFlat)로 근접 문서 고속 검색 프레임워크](@/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search.md)
152. [지식 증류 (Knowledge Distillation) 교사 학생 모델 압축 경량 전이](@/14_data_engineering/03_ml_dl_llm/152_knowledge_distillation_soft_target_compression.md)
153. [디퓨전 모델 (Diffusion) 이미지 생성 AI 역노이즈 파괴 복원망 (Stable Diffusion, Midjourney)](@/14_data_engineering/03_ml_dl_llm/153_diffusion_model_stable_diffusion_denoising.md)
154. [생성적 적대 신경망 (GAN) 위조 경찰 적대 통계 보정](@/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network.md)
155. [AI 에이전트 (AI Agents) 도구 함수 호출 (Function Calling) 자동 과업 루프 목표 달성망](@/14_data_engineering/03_ml_dl_llm/155_ai_agents_function_calling_agentic_loop.md)
156. [추천 시스템 딥러닝 팩토라이제이션 머신 (DeepFM)](@/14_data_engineering/03_ml_dl_llm/156_recommendation_system_deepfm_collaborative_filtering.md)
157. [시계열 예측 딥러닝 TCN 병렬 합성곱 필터 변환망](@/14_data_engineering/03_ml_dl_llm/157_time_series_deep_learning_tcn_transformer.md)
158. [멀티모달 (Multimodal) 비전 오디오 동시 인코딩 임베딩 클립 (CLIP) 대조 학습 모델망](@/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding.md)
159. [GNN 그래프 노드 구조 메시지 패싱 네트워크](@/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing.md)
160. [지식 그래프 연계 GraphRAG 연동망 체제 설계](@/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration.md)

## 4. MLOps 파이프라인 및 데이터 분석 엔지니어링 (60개)
161. [MLOps (Machine Learning Operations) - AI 모델 개발(Jupyter 노트북 랩)과 실제 프로덕션 서버 운영(서빙) 간의 단절을 타파하고, CI/CD 배포 자동화를 데이터/AI 파이프라인 전 주기에 접목한 공학 체계](@/14_data_engineering/04_mlops/161_mlops_machine_learning_operations.md)
162. [CT (Continuous Training, 지속적 훈련) 파이프라인 - 모델 성능 저하가 감지되면 자동으로 재학습 사이클을 트리거](@/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining.md)
163. [데이터 드리프트 (Data Drift) - 서비스 운영 중 유입되는 새로운 사용자 입력 데이터의 통계적 분포(평균, 편차)가 훈련 데이터 분포와 심하게 이격되는 현상 (정확도 하락 원인)](@/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift.md)
164. [컨셉 드리프트 (Concept Drift) - 데이터 자체는 같으나, "개=1, 고양이=0" 식의 타겟 정답 맵핑 규칙(세상의 트렌드) 자체가 뒤바뀌어버리는 현상](@/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change.md)
165. [피처 스토어 (Feature Store) - 전처리(정규화/결측치 처리)가 끝난 머신러닝 변수 셋을 중앙 집중 관리하여, 오프라인 훈련 팀과 온라인 서빙 API 간의 피처 불일치(Training-Serving Skew)를 방지하는 실시간 캐시 DB 인프라](@/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency.md)
166. [모델 레지스트리 (Model Registry) - 학습 완료 모델 바이너리 가중치 덤프, 하이퍼파라미터 이력, 메타데이터 버전 관리 창고 (MLflow, W&B)](@/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow.md)
167. [쿠브플로우 (Kubeflow) - 쿠버네티스 컨테이너 기반 딥러닝 분산 학습, 파이프라인 오케스트레이션 플랫폼](@/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline.md)
168. [데이터 파이프라인 워크플로우 DAG 제어 (Apache Airflow) 자동화](@/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling.md)
169. [모델 서빙 엔진 - REST/gRPC 기반 추론(Inference) 서버 (TensorFlow Serving, NVIDIA Triton)](@/14_data_engineering/04_mlops/169_model_serving_engine_triton_tensorflow_serving.md)
170. [서빙 아키텍처 A/B 테스트 및 카나리 롤아웃 (Canary Rollout) 섀도우 미러링 검증 라우터](@/14_data_engineering/04_mlops/170_ab_test_canary_rollout_shadow_mirroring.md)
171. [설명 가능한 AI (XAI) 도입 - 딥러닝 블랙박스 파훼. 국소적 선형 대리 모델 LIME 및 게임이론 기반 변수 전역 기여도 SHAP 값 지표 도출](@/14_data_engineering/04_mlops/171_xai_lime_shap_explainable_ai.md)
172. [GPU 인프라 분산 학습 (Data Parallelism 데이터 병렬화 분배 vs Model Parallelism 모델 층 쪼개기 텐서 병렬화)](@/14_data_engineering/04_mlops/172_distributed_training_data_model_parallelism.md)
173. [텐서 코어 (Tensor Core) HBM GPU 병목 최적화 (혼합 정밀도 학습 FP16/FP32 믹싱 스루풋 향상)](@/14_data_engineering/04_mlops/173_tensor_core_hbm_mixed_precision_training.md)
174. [LLMOps 특화 요소 - 프롬프트 템플릿 관리, RAG 벡터 DB 동기화 파이프, PEFT 잡 스케줄링 관리망 모니터링](@/14_data_engineering/04_mlops/174_llmops_prompt_template_rag_pipeline.md)
175. [RHF (RLHF) 기반 랭킹 선호 모델 수집 파이프 인간 라벨러 루프 연동](@/14_data_engineering/04_mlops/175_rlhf_ranking_reward_model_human_labeler.md)
176. [자동화 파이프라인 (AutoML) 하이퍼파라미터 최적화 베이지안 탐색 모듈망 결합](@/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian.md)
177. [데이터 엔지니어링 성능 최적 델타 레이크하우스 스냅샷 롤백 (Time Travel) 트랜잭션](@/14_data_engineering/04_mlops/177_delta_lakehouse_time_travel_transaction.md)
178. [파케이 (Parquet) 스토리지 압축 포맷 RLE 스킵 인코딩 최적 성능 모델](@/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression.md)
179. [카프카 (Kafka) 스트림 처리 플링크 (Flink) 시간 창 (Window) ウォ터마크(Watermark) 체제](@/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window.md)
180. [CDC 실시간 로그 캡처 데베지움 파이프 동기망](@/14_data_engineering/04_mlops/180_cdc_debezium_binlog_realtime_sync.md)
181. [연방 학습 (Federated Learning) 스마트폰/분산 엣지 노드 가중치 로컬 암호 전송 클라우드 보안 병합](@/14_data_engineering/04_mlops/181_federated_learning_privacy_distributed_training.md)
182. [블록체인/스마트 컨트랙트 데이터 무결 증빙 NFT 트랜잭션 마켓](@/14_data_engineering/04_mlops/182_blockchain_smart_contract_data_integrity.md)
183. [양자 내성 암호 클라우드 인프라 키 전환](@/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition.md)
184. [프라이버시 보호 차분 프라이버시 노이즈 통계 방어](@/14_data_engineering/04_mlops/184_differential_privacy_noise_statistical_defense.md)
185. [K-익명성, 마스킹 파이프 자동 변환 전처리](@/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline.md)
186. [그래프 DB 추천 알고리즘 협업 필터링 콜드 스타트 파훼](@/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start.md)
187. [시계열 DB 보간법(Interpolation) 롤업 통계 지표 대시보드](@/14_data_engineering/04_mlops/187_time_series_interpolation_rollup_dashboard.md)
188. [OOM 메모리 보호 GC(Garbage Collection) 스파크 스왑 방어](@/14_data_engineering/04_mlops/188_oom_memory_protection_gc_spark_spill.md)
189. [카프카 컨슈머 랙 (Lag) 지연 모니터링 경보 파이프](@/14_data_engineering/04_mlops/189_kafka_consumer_lag_monitoring_alert.md)
190. [스플릿 브레인 방어 주키퍼 펜싱 합의 코디 연계망](@/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum.md)
191. [람다/카파 아키텍처 재현 (Event Sourcing Replay) 스트림 병합](@/14_data_engineering/04_mlops/191_event_sourcing_replay_lambda_kappa.md)
192. [엣지 AI 컴파일러 (ONNX, TensorRT) 모델 직렬화 패키징 배포망](@/14_data_engineering/04_mlops/192_edge_ai_onnx_tensorrt_model_serialization.md)
193. [뉴로모픽 반도체 SNN 저전력 칩 통계 추론](@/14_data_engineering/04_mlops/193_neuromorphic_chip_snn_low_power_inference.md)
194. [메들리온 아키텍처 (Bronze, Silver, Gold 테이블) 정제 적재 로직](@/14_data_engineering/04_mlops/194_medallion_architecture_bronze_silver_gold.md)
195. [연방 쿼리 데이터 패브릭 분산 메타 통계망 조인](@/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join.md)
196. [데이터옵스 CI/CD (dbt) 데이터 검증 테스트 코드 결합](@/14_data_engineering/04_mlops/196_dataops_dbt_ci_cd_data_testing.md)
197. [데이터 카탈로그 계보 (Lineage) 시각화 보안 정책 연계망](@/14_data_engineering/04_mlops/197_data_catalog_lineage_visualization_security.md)
198. [지식 증류 소프트 타겟(Soft Target) 확률 분포 모방 파이프](@/14_data_engineering/04_mlops/198_knowledge_distillation_soft_target_probability.md)
199. [인텐트 기반 네트워킹 (IBN) 트래픽 인공지능 라우팅 분배망](@/14_data_engineering/04_mlops/199_intent_based_networking_ibn_ai_traffic_routing.md)
200. [자율주행 모방 학습 시뮬레이터 디지털 트윈 동기 합성 데이터 생성 파이프라인](@/14_data_engineering/04_mlops/200_autonomous_driving_imitation_learning_digital_twin.md)

## 5. 시험 빈출 요약 및 실무자 빅데이터/AI 논술 키워드 (100개 집중)
201. [3V 5V 빅데이터 특성 다양 속도 볼륨](@/14_data_engineering/04_mlops/201_v_5v.md)
202. 스케일 아웃 분산 확장 수평 범용 노드
203. 하둡 HDFS 블록 복제 3벌 랙 인지 내결함성
204. 네임노드 메타데이터 맵리듀스 디스크 병목
205. [셔플 정렬 YARN 리소스 매니저](@/14_data_engineering/04_mlops/205_yarn.md)
206. [스파크 인메모리 RDD 지연 평가 계보 복구](@/14_data_engineering/04_mlops/206_spark_inmemory_rdd_lazy_evaluation_lineage.md)
207. 데이터 레이크 스키마 온 리드 원시 저장
208. 데이터 웨어하우스 스키마 온 라이트 Inmon 주젯
209. 데이터 마트 Kimball 다차원 분석 스타 스키마
210. [팩트 차원 테이블 스노우플레이크 눈송이](@/14_data_engineering/04_mlops/210_fact_dimension_table_snowflake_schema.md)
211. OLAP 드릴다운 롤업 서로게이트 키
212. ETL 변환 병목 ELT 클라우드 내부 연산 전이
213. 데이터 레이크하우스 트랜잭션 델타 레이크 파케이 압축
214. 카프카 Pub Sub 토픽 파티션 오프셋 분산 브로커
215. [플링크 네이티브 스트림 워터마크 윈도우 시간](@/14_data_engineering/04_mlops/215_flink_native_stream_watermark_window_time.md)
216. 람다 카파 아키텍처 배치 실시간 분할 일원화망
217. CDC 빈로그 데이터 캡처 변경 로그 추출 데베지움
218. NoSQL BASE 결과적 일관성 샤딩 해시 분산
219. CAP PACELC 트레이드오프 분산 합의
220. [키-값 도큐먼트 컬럼 패밀리 그래프 데이터베이스](@/14_data_engineering/04_mlops/220_nosql_types_keyvalue_document_wide_column_graph.md)
221. [LSM 트리 멤테이블 순차 플러시 콤팩션](@/14_data_engineering/04_mlops/221_lsm_tree_memtable_sequential_flush_compaction.md)
222. 데이터 메시 분산 오너십 데이터 프로덕트 셀프 서빙
223. 데이터 패브릭 메타 가상화 통합 연결망
224. 데이터 리니지 흐름 족보 카탈로그 탐색 태그
225. KDD 교차 분석 T검정 분산 분석 ANOVA 통계
226. 피어슨 상관 회귀 최소 제곱 R^2 결정 다중 공선 VIF
227. 로지스틱 회귀 우도 중심 극한 정리 p-value 1/2종 오류
228. PCA 주성분 LDA t-SNE 차원 축소 비지도 지도
229. [시계열 ARIMA 정상성 협업 필터링 추천](@/14_data_engineering/04_mlops/229_time_series_arima_stationarity_collaborative_filtering.md)
230. SVD 행렬 분해 랜덤 포레스트 부스팅 XGBoost
231. SMOTE 오버 샘플링 불균형 데이터 증강
232. TF-IDF 코사인 유사도 텍스트 임베딩 혼동 행렬
233. 정밀도 재현율 F1 스코어 ROC AUC 임계 곡선
234. 마스터 데이터 (MDM) 골든 레코드 클린 룸
235. 인공지능 튜링 테스트 전문가 시스템 퍼지 탐색
236. [A* 휴리스틱 미니맥스 MCTS 몬테카를로 탐험](@/14_data_engineering/04_mlops/236_mcts.md)
237. 머신러닝 지도 비지도 강화 편향 분산 오류
238. SVM 마진 커널 트릭 나이브 베이즈 확률
239. 퍼셉트론 다층 은닉층 가중치 활성화 시그모이드
240. ReLU 기울기 소실 복원 소프트맥스 역전파 연쇄
241. 옵티마이저 SGD 미니배치 Adam 관성 적응 모멘텀
242. 규제 드롭아웃 조기 종료 L1 L2 라쏘 릿지
243. CNN 스트라이드 풀링 ResNet 잔차 연결 YOLO 객체
244. RNN 시계열 LSTM 셀 게이트 장기 의존성 극복
245. Seq2Seq 컨텍스트 어텐션 동적 가중 집중 연산
246. 트랜스포머 셀프 어텐션 병렬 포지셔널 인코딩
247. 파운데이션 모델 LLM 파라미터 창발성 자기 지도
248. BERT 인코더 MLM GPT 디코더 자동 회귀
249. 인스트럭션 파인튜닝 PEFT LoRA 저차원 어댑터
250. RLHF 인간 피드백 강화 정렬 프롬프트 CoT 사슬
251. 할루시네이션 환각 RAG 증강 검색 벡터 DB
252. 지식 증류 양자화 경량 온디바이스 SLM 디퓨전 노이즈 생성
253. 강화 학습 MDP 정책 가치 Q러닝 DQN
254. MLOps 데이터/컨셉 드리프트 피처 스토어
255. XAI 설명 가능 LIME SHAP 기여 분할
256. 연합 학습 프라이버시 모델 보안 지표망
257. [(빅데이터 분석 / 클라우드 파이프라인 등 300+ 개념 연결 완성)](@/14_data_engineering/04_mlops/257_bigdata_analysis_cloud_pipeline_integration.md)
...
300. 데이터 및 AI 아키텍트 전용 고득점 암기 단어장 집대성


## 추가 학습 키워드 (Additional Study Keywords)

- Distributed Computing Scale Out

---
<strong>총정리 빅데이터 / 데이터 엔지니어링 키워드 : 총 300+ 통합 (1~6부 총 800+ 규모 핵심 토픽 포함)</strong>
(빅데이터 인프라, 하둡/스파크 구조, 실시간 카프카 파이프라인부터 데이터 메시/레이크하우스 사상 및 최신 RAG 튜닝, MLOps, 통계 분석 수학까지 데이터 전문가 과정의 지식 사전입니다.)
