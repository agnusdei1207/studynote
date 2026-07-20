---
title: "Data Orchestration Airflow Dagster"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 675
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 오케스트레이션은 분산된 데이터 파이프라인을 **DAG(Directed Acyclic Graph)** 모델로 추상화하여 스케줄링·의존성 관리·모니터링·재시도·백필을 통합 제어하는 소프트웨어 공학적 기법이며, **Airflow는 Task-centric(DAG Run/Task Instance)**, **Dagster는 Asset-centric(Software-Defined Asset + IOManager)** 패러다임을 각각 채택한 두 개의 상보적 프레임워크이다.
> 2. **가치**: 수십~수백 개의 ETL/ML 파이프라인을 단일 메타스토어(SQLite/PostgreSQL/MySQL)로 통합 운영 시 SLA 지연 분석 시간 **MTTR 60% 단축**, 파이프라인 재실행 평균 시간 **40% 감소**, 자산 단위 리니지·신선도(Freshness)·데이터 품질 체크 자동화로 **데이터 신뢰성(Data Reliability)을 3배 이상** 향상시킬 수 있다.
> 3. **판단 포인트**: 실무자 논문 작성 시 핵심 분기점은 ①**자산 우선(Asset-First) 사고**가 필요한가(데이터 리니지·신선도 SLA 강조 시 -> Dagster 우세) ②**레거시 운영 안정성·생태계 성숙도**가 우선인가(-> Airflow 2.x + KubernetesExecutor 권장) ③**테스트 가능성·타입 시스템**으로 SDLC 통합이 중요한가(-> Dagster의 `Op`/`Asset` 단위 `pytest` 친화성) ④클라우드 매니지드(AWS MWAA·GCP Cloud Composer·Astronomer vs Dagster Cloud) 비용·고가용성 요건을 기준으로 결정한다.

---

## Ⅰ. 개요 및 필요성

현대 데이터 플랫폼은 **배치 ETL(Airbyte·Fivetran)**, **스트리밍(Kafka·Flink)**, **ML 학습/배포(Kubeflow·MLflow)**, **리포팅(DBT·Looker)**, **역ETL(Hightouch·Census)** 등 100개 이상의 컴포넌트가 복합적으로 얽혀 있으며, 단일 cron·셸 스크립트 체계로는 ①의존성 추적 ②부분 실패 재처리 ③데이터 신선도(Freshness) 보장 ④리니지(Lineage) 시각화 ⑤멱등성(Idempotency) 보장이 사실상 불가능하다. 2014년 Airbnb가 Airflow를 오픈소스화한 이후 업계는 **DAG + 스케줄러 + 실행기(Executor) + 메타스토어(Metastore)** 4계층 모델로 수렴하였고, 2020년 Dagster(Elementl 사)는 **"데이터가 무엇인지(Asset)"**에 초점을 맞춘 **Software-Defined Asset(SDA)** 패러다임을 도입하며 패러다임 전환을 제시했다.

```text
[ Legacy : Cron + Shell Scripts (1세대) ]
  +----------+     +----------+     +----------+
  | crontab  |----->|  shell   |----->|   DB     |   <- 의존성 암묵적, 실패 무인, 리니지 ✕
  | 0 1 * * *|     | ./etl.sh |     |  write   |
  +----------+     +----------+     +----------+
        |                |                |
        v                v                v
   [ Silent Failure / Data Corruption / No Audit Trail ]

                          ⇣ ⇣ 패러다임 전환 ⇣ ⇣

[ Modern : DAG + Orchestrator (2~3세대) ]
  +----------------------------------------------------------+
  |  Source          Transform            Sink              |
  | +------+        +----------+        +----------+         |
  | | MySQL|--(1)--->|  Spark   |--(3)--->| BigQuery |         |
  | +------+        |  Job     |        +----------+         |
  |                  +----+-----+                            |
  |  +------+             |(2)                               |
  |  | S3   |-------------+                                  |
  |  +------+                                                |
  |       |              DAG: orders_etl_dag                 |
  |       |              +------+   +------+   +------+     |
  |       +-------------->|Task A+--->|Task B+--->|Task C|--+  |
  |                      +------+   +------+   +------+  |  |
  |                       (extract)  (transform)  (load)  |  |
  |                                                       v  |
  |                                              +----------+|
  |                                              | Slack    ||
  |                                              | Alert    ||
  |                                              +----------+|
  +----------------------------------------------------------+
   - 의존성 명시 / 자동 재시도 / 메타스토어 기반 감사 추적
   - Lineage 시각화 / SLA 모니터링 / Backfill 지원
```

기존 cron 체계는 **암묵적 의존성**, **부분 실패 시 silent data corruption**, **리니지 부재**, **개발-운영 파편화(Dev-Prod Parity)** 문제를 야기했다. 이를 해결하기 위해 ①DAG(순환 없는 방향 그래프) 모델, ②메타스토어(예: Airflow의 `airflow.db` + 별도 RDBMS) 기반 상태 영속화, ③REST/CLI/Web UI 통합 인터페이스, ④실행기-워커 분리(Executor-Worker Separation)를 통한 수평 확장 아키텍처가 등장했다. 학습 정리에서는 **"왜 단순 cron이 아닌 전용 오케스트레이터가 필요한가"**를 4가지 관점(①의존성 명시성 ②신뢰성·재시도 정책 ③관측 가능성 ④확장성)으로 정량적·정성적 근거와 함께 서술해야 한다.

- **📢 섹션 요약 비유**: 데이터 오케스트레이션은 **"오케스트라의 지휘자"**와 같다. 첼리스트(데이터 소스), 바이올리니스트(변환 엔진), 타악기(저장소)가 각자 연주하면 카오스가 되지만, **지휘자(Orchestrator)**가 악보(DAG)를 보며 **"첼로 먼저 -> 바이올린 진입 -> 3박자 후 드럼"**처럼 **의존성과 타이밍을 조율**해야 비로소 음악(신뢰 가능한 데이터)이 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. Apache Airflow 아키텍처 (v2.5+ 기준)

Airflow는 다음 5대 컴포넌트로 구성된다: ①**Webserver**(Flask + Gunicorn 기반 UI/API), ②**Scheduler**(DAG 파싱·TaskInstance 스케줄링 루프), ③**Executor**(Task 실행 정책 결정: Sequential/Local/Celery/Kubernetes/CeleryKubernetes), ④**Worker**(실제 Task 코드 실행 컨테이너/프로세스), ⑤**Metadata Database**(PostgreSQL 권장, SQLite는 dev only). Airflow 2.0부터 도입된 **TaskFlow API**(`@task` 데코레이터)는 XCom 자동 주입을 통해 보일러플레이트를 70% 이상 감소시켰으며, **DAG Serialization**(v2.1+)은 스케줄러 부하를 DAG당 평균 **40% 절감**한다.

```text
                       [ End User / Data Engineer ]
                                  |
                  +---------------+---------------+
                  |                               |
                  v                               v
          +--------------+                +--------------+
          |  Webserver   |<---REST API----->|  Triggerer   |
          | (Flask+Guni) |                | (Deferred    |
          |   :8080      |                |  Sensors)    |
          +------+-------+                +--------------+
                 | reads/writes                   | async
                 v                                v
        +------------------------------------------------+
        |      Metadata DB (PostgreSQL 12+)              |
        |   - dag_run, task_instance, serialized_dag,    |
        |     log, slot_pool, sla_miss, dag_code,         |
        |     callback_request, variable, connection      |
        +------------+-----------------------------------+
                     |  Scheduler Loop (5s default)
                     v
        +--------------------------------------+
        |            Scheduler                 |
        |  1. DAG File Processor (parsing)    |
        |     - min_file_process_interval     |
        |     - max_active_runs_per_dag       |
        |  2. SchedulerJob (loop)             |
        |     - create DagRun (Cron/Manual)   |
        |     - schedule TaskInstance         |
        |     - verify dependencies (UP_FOR_  |
        |       RETRY, UPSTREAM_FAILED)       |
        |  3. Pools / Priority Weights        |
        +------------+-------------------------+
                     | queue: celery/k8s/celery_k8s
                     v
        +--------------------------------------+
        |             Executor                |
        |  +----------+ +----------+ +------+ |
        |  |LocalExec | |CeleryEx. | |K8sEx.| |
        |  |(단일호스트)| |(Redis MQ)| |(Pod) | |
        |  +----+-----+ +----+-----+ +--+---+ |
        +-------+-------------+---------+-----+
                v             v         v
         +----------+  +----------+  +----------+
         | Sub-     |  | Celery   |  | K8s Pod  |
         | process  |  | Worker   |  |(per Task)|
         +----+-----+  +----+-----+  +----+-----+
              v             v             v
        +--------------------------------------+
        |           Task Execution             |
        |  extract() -> transform() -> load()    |
        |  XCom: { "row_count": 1,234,567 }    |
        +--------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Webserver** | DAG/TaskInstance 조회, 수동 Trigger, Log/Variable/Connection 관리, RBAC UI | Flask + Gunicorn(`worker_class=gevent`), `airflow.www.app` Blueprint, JWT 기반 RBAC, `expose_config=False` 권장 |
| **Scheduler** | DAG 파싱 -> DagRun 생성 -> TaskInstance 스케줄 -> Executor 큐 적재 | `DagFileProcessorManager` 멀티프로세스 파싱, `SchedulerJob._execute_loop()`에서 `schedule_dag_run()`, `executor.heartbeat()` 폴링, `min_serialized_dag_update_interval=30s` |
| **Executor** | Task 실행 정책 결정: 동시성·격리·자원 할당 | `LocalExecutor`(병렬 Subprocess), `CeleryExecutor`(Redis/RabbitMQ 브로커, `worker_prefetch_multiplier=1`), `KubernetesExecutor`(Task=Pod, `base_operator_pod_template`, `priority_class`), `CeleryKubernetesExecutor`(혼합) |
| **Metadata DB** | DAG 정의·실행 이력·연결 정보 영속화 (SSoT) | PostgreSQL 권장(Concurrency Lock `psycopg2` Advisory Lock 사용), `airflow db upgrade`로 마이그레이션, Connection은 Fernet Key로 컬럼 암호화(`crypto._fernet`) |
| **Worker / Triggerer** | Task 코드 실행 / Deferrable Operator의 비동기 폴링 | Celery Worker: `--concurrency=16 --prefetch-multiplier=1`, Triggerer: `asyncio` 기반 `Trigger` 객체로 `S3KeySensor` 등 외부 이벤트 대기 시 슬롯 점유 해소 |

### B. Dagster 아키텍처 (v1.3+ 기준)

Dagster는 ①**User Code(Definitions / Assets / Ops)** ②**Dagster Webserver** ③**Dagster Daemon**(Sensor/Schedule/Backfill/Run Coordinator/Asset Materialization 큐) ④**Code Location**(gRPC 서버, `dagster api grpc`) ⑤**Instance Storage**(Runs/Event Logs/SQLite or Postgres)로 구성된다. 핵심 차별점은 **`@asset` 데코레이터**로 표현되는 **Software-Defined Asset**이며, **IOManager**를 통해 Pandas DataFrame -> Parquet/Delta Lake으로 자동 직렬화·역직렬화한다. **Dagster Types**(`@dagster_type`)는 런타임 타입 체크를 통해 데이터 품질을 **컴파일 타임에 가깝게** 보장한다.

```text
   +---------------------------------------------------------+
   |              Definitions (repository.py)                |
   |  +--------------+  +--------------+  +--------------+  |
   |  |  @asset      |  | @job         |  | @sensor      |  |
   |  |  raw_orders  |  | etl_job      |  | s3_sensor    |  |
   |  |  (Pandas DF) |  | (legacy ops) |  |              |  |
   |  +------+-------+  +------+-------+  +------+-------+  |
   |         |                 |                 |           |
   |         +---- IOManager -+----- Resource --+           |
   |           (parquet_io,   (snowflake,                     |
   |            delta_io)      s3)                            |
   +----------------+----------------------------------------+
                    | gRPC :4000 / 0.0.0.0
                    v
   +---------------------------------------------------------+
   |             Dagster Webserver :3000                     |
   |   - Asset Catalog (Lineage Graph)                       |
   |   - Run Timeline / Gantt                                |
   |   - Asset Materialization Logs                          |
   |   - Dagster Types Error Trace                           |
   +------------+--------------------------------------------+
                | event log
                v
   +---------------------------------------------------------+
   |             Dagster Daemon                              |
   |