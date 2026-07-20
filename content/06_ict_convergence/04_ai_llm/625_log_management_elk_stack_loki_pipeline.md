---
title: "Log Management ELK Stack Loki Pipeline"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 625
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 로그 관리는 **수집(Agent/Beats/Vector)** -> **전송/변환(Buffer/Logstash/Promtail)** -> **저장·인덱싱(Elasticsearch/Loki+TSDB)** -> **분석·시각화(Kibana/Grafana)**의 4-Stage 파이프라인으로 구성되며, ELK는 **풀텍스트 인덱스 기반 전문 검색**, Loki는 **라벨 인덱스 + Chunk 압축 스토어**로 상반된 인덱싱 철학을 채택한다.
> 2. **가치**: 중앙 집중 로그 파이프라인은 **MTTR(평균 복구 시간)을 60~80% 단축**, 컴플라이언스 감사 로그 보존을 통한 **ISMS-P·PCI-DSS·GDPR 준수 자동화**, 하루 수십 TB 규모 로그 처리 시 **인덱스 압축률 70%^·스토리지 비용 50%v** 효과를 제공한다.
> 3. **판단 포인트**: **"풀텍스트 검색 vs 라벨 기반 집계"**, **"인덱스 비용 vs 쿼리 유연성"**, **"ECK/Elastic Cloud SaaS vs Grafana Cloud + OSS Loki"**라는 3대 트레이드오프에서 도메인 성격(키워드 검색 빈도·시계열 상관관계·k8s 워크로드 비율)에 따라 ELK/Loki를 단독 또는 하이브리드로 결정한다.

---

## Ⅰ. 개요 및 필요성

현업의 마이크로서비스·쿠버네티스·MSA 환경에서 단일 트랜잭션은 평균 **20~40개 컨테이너, 5~15개 마이크로서비스**를 거치며, 각 컴포넌트는 stdout/stderr, 시스템 syslog, nginx access log, app-specific JSON log, audit log를 분산 출력한다. 2000년대 초반 **syslog-ng(rsyslog) + grep + awk** 기반 로그 감시는 ① 로그 손실 ② 시계열 비보존 ③ 검색 성능 저하 ④ 멀티 노드 집계 불가라는 4대 한계에 부딪혔다. 2010년 Elasticsearch + Logstash + Kibana의 **ELK 스택**이 등장해 **Lucene 역색인** 기반 ms 단위 전문 검색을 가능케 했고, 2018년 Grafana Labs가 **Loki**를 발표하며 "**Prometheus와 동일한 라벨 모델** + **로그는 압축 청크로 저장**"이라는 경량 철학으로 k8s 시대의 로그 관리 패러다임을 재정의했다.

특히 **CNCF Graduation 프로젝트**인 Loki는 **수평 확장 가능한 멀티테넌트** 구조로, **Grafana 10+**에서 ELK와 동일한 UX(Explore + LogQL)를 제공한다. 2024년 기준 Grafana Loki는 **2.x**로 진화하며 **BoltDB Shipper -> TSDB 스토어**로 마이그레이션, **split-bolt-shipper -> TSBD index**로 전환되어 색인 비용을 90% 이상 절감했다.

```text
[전통 로그 관리 vs 중앙 집중 로그 파이프라인 비교]

   (구) 2000s Syslog/Rsyslog + SSH + grep      (신) ELK / Loki 중앙 파이프라인
   +--------------------------+                  +--------------------------------------+
   | App1  -+                 |                  | App -+                               |
   | App2  -+--> syslog-ng --> /var/log  --> ssh |        +--> Filebeat --> Kafka --> Logstash-+--> Elasticsearch --> Kibana
   | App3  -+                 |   tail/grep      |        |   (Beat)       (Buffer) (ETL)  |   (Lucene Index)   (Viz)
   | App4 --> rsyslog --> 서버1  |                  | App -+                                  +--> Grafana  (검색·시각화)
   | App5 --> rsyslog --> 서버2  |                  |      +--> Promtail -----> Loki Distributor-> Loki Store(TSDB+Chunk)-> Grafana
   +--------------------------+                  +--------------------------------------+
   ✗ 로그 손실, 단일 장애점, 검색 불가            ✓ 고가용성, 무손실, ms 검색, k8s 네이티브 라벨링
```

- **📢 섹션 요약 비유**: 옛날엔 각 집(서버)이 직접 우편함(syslog)을 만들어서 손편지를 받았지만, 이제는 **중앙 우편집중국(ELK/Loki)**이 모든 우편을 한 곳으로 모아 분류·검색·보관까지 자동으로 해주는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ELK 스택 파이프라인 아키텍처

ELK는 **Beats(Family of Agents) -> Logstash(전송/변환) -> Elasticsearch(검색/분석) -> Kibana(시각화)**의 4-티어 구조다. 핵심은 **Logstash의 3단계 파이프라인(Inputs -> Filters -> Outputs)**과 **Elasticsearch의 Shard 기반 Lucene 역색인**이다.

```text
[ELK 스택 상세 데이터 플로우 - Filebeat -> Kafka -> Logstash -> ES -> Kibana]

 +-------------+   +---------+   +---------+   +--------------+   +---------+
 | App Container|   |Filebeat |   |  Kafka  |   |   Logstash   |   |  ES     |
 |  stdout ----+--->|input:log|--->| Topic:  |--->| Input:kafka  |--->|  Index: |
 |  json       |   |  json   |   | app-log |   | Filter:      |   |  log-   |
 |  log        |   |  harv.  |   |  (3,3)  |   |  - grok      |   |  2024.12|
 +-------------+   |  ACK   |   |  ISR=2  |   |  - date parse|   |  shard0 |
                   +----+----+   +----+----+   |  - geoip     |   |  shard1 |
                        |             |        |  - mutate    |   |  shard2 |
                        v             v        | Output:ES    |   +----+----+
                  at-least-once   partition by |              |        |
                  delivery via   hash(key)     +--------------+        v
                  registry file                                 +------------+
                  (저장 후 ACK)                                 |   Kibana   |
                                                                | Discover   |
                                                                | Dashboard  |
                                                                | Alerting   |
                                                                +------------+
```

**Filebeat 핵심**: `registry` 파일(기본 위치 `data/registry`)에 **오프셋을 영구 저장**해 프로세스 재시작/네트워크 단절 시에도 **at-least-once 전달 보장**. `backoff.init` ~ `backoff.max` (1s~10s) 스파이크 흡수, `bulk_max_size: 2048`로 배치 처리.

**Logstash 핵심**: JVM 기반, **`-Xms`/`-Xmx` 동일값 설정**(힙 리사이즈 방지), `pipeline.workers = CPU 코어 수`, `pipeline.batch.size: 125`, `pipeline.batch.delay: 50ms`. 필터에서 **grok** 패턴(`%{COMBINEDAPACHELOG}`), **dissect**(고정 구분자 파싱), **ruby**(커스텀 로직), **kv**(key=value) 활용.

**Elasticsearch 핵심**: `index.number_of_shards`(쓰기 시점 고정, **split API로 변경**), `number_of_replicas`, `refresh_interval: 1s` (기본; **30s로 변경 시 색인 throughput 2~3배^**). **ILM(Index Lifecycle Management)**로 `hot-warm-cold-delete` 4단계 자동 관리: hot(SSD, 고쓰기) -> warm(HDD, 읽기전용) -> cold(frozen + searchable snapshot, S3/Glacier) -> delete(보존기간 만료).

### 2. Loki 파이프라인 아키텍처

Loki는 Grafana Labs가 만든 **"Prometheus for logs"** 철학의 **수평 확장 멀티테넌트 로그 시스템**이다. 핵심 차별점은 **로그 본문을 인덱싱하지 않고** **라벨(labelled stream) 단위로만 인덱싱**하여 스토리지/인덱싱 비용을 극적으로 낮춘다.

```text
[Loki 2.x TSDB 기반 아키텍처 - Promtail -> Distributor -> Ingester -> TSDB -> Store -> Querier]

 +--------------+    +--------------+    +--------------+    +---------------+
 |  k8s Pod     |    |  Promtail    |    |  Distributor |    |   Ingester    |
 |  /var/log/   |---->|  - scrape    |---->|  - consistent|---->|  - chunk 빌더 |
 |  containers/ |    |  - relabel   |    |     hashing  |    |  - memory     |
 |  *.log       |    |  - pipeline  |    |  - tenant    |    |  - 1MB 청크   |
 +--------------+    |  - push      |    |     routing  |    |  - gzip/zar   |
                     +--------------+    +------+-------+    +------+--------+
                                                 |                   |
                                                 v                   v
                                          +-------------+    +------------------+
                                          |   Kafka     |    |  TSDB Index      |
                                          |  (WAL/Buffer|    |  (boltdb-shipper |
                                          |   optional) |    |   -> TSDB)        |
                                          +-------------+    |  per-tenant      |
                                                               |  per-day         |
                                                               +----------+-------+
                                                                          v
                                                               +------------------+
                                                               | Object Storage   |
                                                               |  S3 / GCS / Azure|
                                                               |  / MinIO / Swift |
                                                               |  (Chunk + TSDB)  |
                                                               +----------+-------+
                                                                          v
                                                               +------------------+
                                                               |   Querier        |
                                                               |   + Query Frontend|
                                                               |   (LogQL)        |
                                                               |   - parallelize  |
                                                               |   - cache        |
                                                               +----------+-------+
                                                                          v
                                                               +------------------+
                                                               |   Grafana        |
                                                               |   Explore /      |
                                                               |   Dashboards /   |
                                                               |   Alerting       |
                                                               +------------------+
```

**Distributor**: gRPC/HTTP 수신 -> **해시 링**(`{tenant_id, labels_hash}`)으로 Ingester 라우팅. **Quoting/캐노니컬화** 후 **replication factor(default 3)** 만큼 복제.

**Ingester**: 로그 스트림을 메모리에서 **chunk 단위(기본 1.5MB, 1시간 flush)**로 압축 저장 후 **Object Storage(S3/GCS/MinIO)**로 flush. **WAL(Write-Ahead Log) -> Kafka/Kinesis**로 Ingester 장애 시 데이터 손실 방지.

**TSDB 인덱스**: Loki 2.8+ 에서 도입된 **TSDB Store**는 **per-tenant per-day 단위 인덱스 파일**(`index_<tenant>_<day>_<idx>.tsdb`)을 Object Storage에 저장. **boltdb-shipper 대비 쓰기 10x, 읽기 2~3x 향상**.

**Querier + Query Frontend**: LogQL(구문은 PromQL + `{label="value"} |="filter" |~"regex"` line filter) 실행. Query Frontend가 **쿼리 분할·결과 병합·캐시**를 처리해 Querier 부하 경감.

### 3. 구성 요소 비교표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Filebeat / Promtail** | 경량 로그 수집기 | Filebeat: `libbeat` Go 기반, `registry` 오프셋 영구화, 멀티라인/JSON 파서, `prospector`로 k8s autodiscover; Promtail: k8s `service`/POD 라벨 자동 부착, `pipeline_stages`(regex/json/timestamp), `loki_push_api` |
| **Kafka / Redis Buffer** | 메시지 버퍼·백프레셔 처리 | Kafka: `acks=all`, `min.insync.replicas=2`, **partition key = `app-name`+`host`**로 순서 보장; Logstash `kafka` input은 **consumer group rebalance** 자동 |
| **Logstash (ELK)** | ETL 변환 엔진 | JVM 17, `pipeline.workers`(병렬 처리), `persistent queues`(디스크 큐), `dead_letter_queue`(처리 실패 격리), 필터: grok, dissect, mutate, date, ruby |
| **Distributor (Loki)** | 로그 수신·해시 라우팅 | gRPC/HTTP, **mTLS(인증)**, **tenant ID별 rate-limit**, **IngestionRateLimiter**(샘플링/드롭) |
| **Ingester (Loki)** | 메모리 청크 빌더 | **stream 단위**(`labels hash`) 키잉, **gzip/zstd 압축**, `chunk_idle_period`(기본 1h), `max_chunk_age`(1h), `flush_op_timeout`(10m) |
| **Elasticsearch** | 분산 검색·분석 엔진 | **Lucene inverted index**, **Shard(Primary/Replica)**, **Segment Merge 정책**(tiered/force), **ILM + ILM rollover**, **Cross-cluster search**, **Frozen tier + searchable snapshot** |
| **Loki Store** | 객체 스토리지 기반 로그 저장 | **S3/GCS/Azure Blob** 호환, **TSDB 인덱스 + Chunk** 분리 저장, **SSE-KMS 암호화**, **Versioning(삭제 보호)** |
| **Kibana / Grafana** | 시각화·대시보드·알림 | Kibana: **ES|QL**(신규 쿼리 언어), **Lens**, **Alerting with Watcher**; Grafana: **Explore(LogQL/PromQL)**, **Unified Alerting**, **Loki ↔ Prometheus join** |
| **Metricbeat / Promtail metrics** | 파이프라인 자체 모니터링 | **self-monitoring**: Filebeat `monitoring` -> ES, Loki `/metrics` -> Prometheus, **Grok/Regex 패턴 검증**, **dead_letter_queue depth** 알람 |

**Grok/Dissect vs Loki Pipeline Stages**: ELK의 `grok`은 정규식 기반 비싸지만 **강력한 파싱**, Loki는 **pipeline_stages에서 regex/JSON/template 수행**하지만 **단순화** 추구. 또한 ELK는 **필드 단위 색인 -> 집계/통계 가능**(Kibana Lens), Loki는 **메트릭화(line sample/metric extraction)**만 지원.

- **📢 섹션 요약 비유**: ELK는 **모든 책의 모든 단어마다 색인(찾아보기)을 다 만드는 도서관**, Loki는 **"어느 서가의 어떤 책"**이라는 표지만 기록하고 책 전체는 서고(S3)에 압축해 두는 도서관이다. 책 내용을 찾고 싶을 때 Loki는 **표지로 서고에서 꺼내 펼치는** 추가 단계가 필요하다.

---

## Ⅲ. 비교 및 연결

### 1. ELK vs Loki vs EFK vs Splunk 핵심 비교

| 구분 | **ELK Stack (8.x)** | **Loki (2.9+)** | **EFK (Fluent Bit -> ES)** | **Splunk Enterprise** |
| :--- | :--- | :--- | :--- | :--- |
| **인덱싱 방식** | **Lucene 풀텍스트 역색인** (필드별 토크나이저) | **라벨만 인덱싱**, 본문은 압축 chunk | ES와 동일(Lucene) | **tsidx**(자체 인덱스, sparse index) |
| **검색 성능** | ms 단위 풀텍스트 `match_phrase` | `\|~` regex는 **full scan**, `\|=` exact는 라벨 인