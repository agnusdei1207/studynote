---
title: "Airflow Dag Pipeline Scheduling"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 168
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Airflow는 파이썬 코드로 워크플로우를 DAG (Directed Acyclic Graph, 방향성 비순환 그래프)로 정의하고, 스케줄러가 이를 자동 실행·모니터링하는 오픈소스 오케스트레이션 플랫폼이다.
> 2. **가치**: 복잡한 데이터 파이프라인의 의존성 관리, 실패 재시도, 시각적 모니터링을 코드로 표현(Configuration as Code)하여 유지보수성과 가시성을 동시에 높인다.
> 3. **판단 포인트**: Airflow는 배치 파이프라인 스케줄링에 강력하지만 실시간 스트리밍과는 맞지 않으며, 스케일아웃 시 CeleryExecutor 또는 KubernetesExecutor로 전환해야 하는 아키텍처 결정이 필요하다.

---

## Ⅰ. 개요 및 필요성

### 1.1 Apache Airflow란?

<strong>Apache Airflow</strong>는 Airbnb가 2014년에 개발하고 2019년 Apache Top Level Project가 된 파이썬 기반 워크플로우 오케스트레이션 플랫폼이다. 데이터 파이프라인의 작업 의존성을 DAG (Directed Acyclic Graph, 방향성 비순환 그래프)로 표현하고 스케줄에 따라 자동 실행한다.

```
Airflow 없는 세상 (문제 상황)
+--------------------------------------------------------+
|  스크립트 A (00:00 실행)                                |
|  스크립트 B (01:00 실행)  <- A 완료 확인을 어떻게?      |
|  스크립트 C (02:00 실행)  <- B 실패 시 C는?             |
|  -> 크론탭(crontab)으로 시간 기반 실행                  |
|  -> 의존성 관리 없음, 실패 재시도 없음                  |
|  -> 파이프라인 현황 가시성 없음                          |
+--------------------------------------------------------+

Airflow 도입 후
+--------------------------------------------------------+
|  DAG: etl_pipeline                                     |
|  extract_task -> transform_task -> load_task             |
|                    v (실패 시)                          |
|                 자동 재시도 3회                         |
|                 -> 알람 발송                            |
|  Web UI로 실시간 현황 모니터링                          |
+--------------------------------------------------------+
```

### 1.2 DAG (Directed Acyclic Graph) 개념

```
DAG = 방향성(Directed) + 비순환(Acyclic) + 그래프(Graph)

방향성: 작업 A -> 작업 B (A가 끝나야 B 시작)
비순환: A -> B -> C -> A 같은 순환 불가 (무한 루프 방지)

예시 DAG:
extract_data
     |
     +---> validate_data ---> load_to_staging
     |                              |
     +---> profile_data             |
                                   v
                           run_dbt_models
                                   |
                           +-------+--------+
                           v               v
                    build_marts      send_report
```

📢 **섹션 요약 비유**: Airflow는 복잡한 요리 레시피를 자동으로 실행하는 주방 AI와 같다. "재료 손질(extract) -> 조리(transform) -> 담기(load)" 순서를 코드로 적어두면, AI가 알아서 순서대로 실행하고, 중간에 실패하면 다시 시도하며, 모든 과정을 화면으로 보여준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Airflow 핵심 구성요소

```
+------------------------------------------------------------------+
|                     Apache Airflow 아키텍처                      |
+----------------+-------------------------------------------------+
|  Web Server    |  Django 기반 Web UI                              |
|  (Flask)       |  DAG 시각화, 실행 현황, 로그 확인                |
+----------------+-------------------------------------------------+
|  Scheduler     |  DAG 파일 파싱, 트리거 결정                      |
|                |  스케줄 기반 또는 외부 트리거로 DagRun 생성      |
+----------------+-------------------------------------------------+
|  Executor      |  실제 작업 실행 담당                              |
|                |  Sequential/Local/Celery/Kubernetes              |
+----------------+-------------------------------------------------+
|  Workers       |  Executor에서 할당받은 Task 실행                  |
|                |  Celery: Celery Worker                          |
|                |  K8s: Pod로 Task 실행                           |
+----------------+-------------------------------------------------+
|  Metadata DB   |  DAG 메타데이터, 실행 이력                       |
|  (PostgreSQL)  |  변수(Variables), 연결(Connections)              |
+----------------+-------------------------------------------------+
|  DAG 파일      |  Python 파일로 정의된 워크플로우                  |
|  (File System) |  Scheduler가 주기적으로 파싱                     |
+----------------+-------------------------------------------------+
```

### 2.2 Airflow DAG 코드 예시

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

# DAG 기본 설정
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['alert@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,                           # 실패 시 3회 재시도
    'retry_delay': timedelta(minutes=5),    # 재시도 간격 5분
}

with DAG(
    dag_id='ml_training_pipeline',
    default_args=default_args,
    description='ML 학습 파이프라인',
    schedule_interval='0 2 * * *',  # 매일 새벽 2시 실행 (cron 표현식)
    start_date=datetime(2024, 1, 1),
    catchup=False,  # 과거 실행 누락 복구 안 함
    tags=['ml', 'training'],
) as dag:

    # 단계 1: 데이터 추출
    extract_task = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/scripts/extract.py --date {{ ds }}',
    )

    # 단계 2: 데이터 검증
    def validate_data(**context):
        execution_date = context['ds']
        # 검증 로직...
        print(f"{execution_date} 데이터 검증 완료")

    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    # 단계 3: BigQuery 변환
    transform_task = BigQueryInsertJobOperator(
        task_id='transform_data',
        configuration={
            "query": {
                "query": "{% raw %}{% include 'sql/transform.sql' %}{% endraw %}",
                "useLegacySql": False,
            }
        },
    )

    # 단계 4: 모델 학습
    train_task = BashOperator(
        task_id='train_model',
        bash_command='python /opt/scripts/train.py --date {{ ds }}',
    )

    # 의존성 설정 (오른쪽 화살표 = 실행 순서)
    extract_task >> validate_task >> transform_task >> train_task
```

### 2.3 Operator 종류

| Operator | 설명 | 사용 예시 |
|:---|:---|:---|
| **BashOperator** | 셸 명령어 실행 | 스크립트 실행, 파일 이동 |
| **PythonOperator** | Python 함수 실행 | 데이터 처리, API 호출 |
| **SparkSubmitOperator** | Spark 잡 제출 | 대용량 배치 처리 |
| **BigQueryOperator** | BigQuery SQL 실행 | 데이터 변환, 집계 |
| **S3ToRedshiftOperator** | S3 -> Redshift 복사 | 데이터 로딩 |
| **KubernetesPodOperator** | K8s Pod 실행 | 컨테이너 기반 작업 |
| **DummyOperator** | 빈 작업 (분기 포인트) | DAG 구조화 |
| **BranchPythonOperator** | 조건부 분기 | A/B 실행 경로 선택 |

### 2.4 Executor 비교

```
+---------------------------------------------------------------+
|                     Executor 비교                              |
+------------------+--------------+----------------------------+
| SequentialExecutor| 단일 프로세스| 개발/테스트용, 병렬 불가  |
+------------------+--------------+----------------------------+
| LocalExecutor     | 로컬 멀티프로| 소규모 운영, 단일 서버    |
|                   | 세스 (fork) | (수십 개 태스크 동시)     |
+------------------+--------------+----------------------------+
| CeleryExecutor    | 분산 워커    | 중~대규모, 고가용성       |
|                   | (RabbitMQ/  | 워커 수평 확장 가능       |
|                   |  Redis)     | 복잡한 설정 필요          |
+------------------+--------------+----------------------------+
| KubernetesExecutor| 태스크별    | 클라우드 네이티브         |
|                   | K8s Pod 생성| 자원 격리, 동적 스케일링  |
|                   |             | 태스크 시작 오버헤드 있음 |
+------------------+--------------+----------------------------+
```

📢 **섹션 요약 비유**: Airflow Executor는 배달 시스템과 같다. SequentialExecutor는 혼자 한 명씩 배달(순차), LocalExecutor는 같은 빌딩의 여러 배달원(로컬 병렬), CeleryExecutor는 여러 지점의 배달원들(분산), KubernetesExecutor는 주문마다 드론을 새로 보내는 방식(Pod 생성)이다.

---

## Ⅲ. 비교 및 연결

### 3.1 Airflow vs Luigi vs Prefect vs Dagster

| 항목 | Airflow | Luigi | Prefect | Dagster |
|:---|:---|:---|:---|:---|
| **개발사** | Apache/Airbnb | Spotify | Prefect Technologies | Elementl |
| **정의 방식** | Python DAG | Python Task | Python Flow | Python Asset/Job |
| <strong>동적 DAG</strong> | 제한적 | 없음 | 완전 지원 | 완전 지원 |
| **관찰성** | 기본 UI | 기본 UI | 강력한 UI | 매우 강력한 UI |
| <strong>데이터 자산</strong> | 없음 | 없음 | 제한적 | 핵심 개념 |
| <strong>클라우드 서비스</strong> | MWAA, Composer | 없음 | Prefect Cloud | Dagster Cloud |
| **활성 커뮤니티** | 매우 높음 | 낮음 | 높음 | 높음 |
| **러닝 커브** | 중간 | 쉬움 | 쉬움 | 중간 |

### 3.2 Airflow의 한계와 대안

| 한계 | 설명 | 대안 |
|:---|:---|:---|
| **실시간 스트리밍 불가** | 배치 지향 설계 | Apache Flink, Kafka Streams |
| <strong>동적 태스크 제한</strong> | DAG 구조 런타임 변경 어려움 | Prefect, Dagster |
| <strong>스케줄러 단일 장애점</strong> | 스케줄러 다운 시 전체 중단 | Airflow 2.x HA 스케줄러 |
| **무거운 설치** | Celery + Redis 설정 복잡 | MWAA, Cloud Composer 관리형 |
| **의존성 표현 한계** | 크로스-DAG 의존성 어려움 | 외부 센서 + 이벤트 |

### 3.3 Airflow 관리형 서비스

| 서비스 | 제공사 | 특징 |
|:---|:---|:---|
| **Amazon MWAA** | AWS | EKS 기반, IAM 통합 |
| **Cloud Composer** | GCP | GKE 기반, GCP 서비스 완전 통합 |
| **Astronomer** | Astronomer | 전문 Airflow 관리형 SaaS |

📢 **섹션 요약 비유**: Airflow vs Prefect/Dagster는 전통 지도(Airflow)와 내비게이션 앱(Prefect/Dagster)의 차이다. 전통 지도는 넓은 생태계와 검증된 신뢰성이 있지만, 내비게이션은 실시간 경로 변경(동적 DAG)과 더 나은 UX를 제공한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 Airflow 모범 사례

```
+--------------------------------------------------------------+
|                  Airflow 모범 사례 (Best Practices)          |
+--------------------------------------------------------------+
|  DAG 설계                                                    |
|  □ 한 DAG당 하나의 논리적 워크플로우만                       |
|  □ 태스크를 원자적(Atomic)으로 설계 (재시도 안전)            |
|  □ 비즈니스 로직은 DAG 외부 (Python 모듈)에 위치             |
|  □ XCom은 소량 데이터만 (대용량은 S3/GCS 경유)              |
+--------------------------------------------------------------+
|  성능                                                        |
|  □ schedule_interval 최소 5분 이상 (너무 잦은 실행 금지)     |
|  □ max_active_runs로 동시 실행 제한                          |
|  □ 연결 풀링 (Connections Pool) 활용                         |
+--------------------------------------------------------------+
|  운영                                                        |
|  □ Variables/Connections에 민감 정보 저장 (하드코딩 금지)    |
|  □ SLA (Service Level Agreement) 설정으로 지연 알람          |
|  □ 로그 외부화 (S3/GCS)로 장기 보관                         |
+--------------------------------------------------------------+
```

### 4.2 심화 학습 핵심 포인트

**Q. Apache Airflow와 Luigi, Prefect를 비교하고 각각의 적합 사용 사례를 설명하시오.**

- **Airflow**: 복잡한 의존성의 대규모 배치 파이프라인, 풍부한 Operator 생태계, 안정성이 검증된 운영 환경에 적합
- **Luigi**: 간단한 파이프라인, 소규모 팀에서 빠른 도입이 필요할 때 적합
- **Prefect**: 동적 워크플로우(런타임 DAG 변경), 마이크로서비스 아키텍처, 데이터 품질 검증에 적합
- **Dagster**: 데이터 자산(Asset) 중심 파이프라인, 데이터 품질 가시성, ML 파이프라인에 적합

**Q. Airflow KubernetesExecutor의 동작 원리와 장단점을 설명하시오.**

KubernetesExecutor는 각 Airflow Task를 독립된 쿠버네티스 Pod로 실행한다. Scheduler가 Task를 대기 큐에서 꺼내면, K8s API를 통해 Pod를 생성하고 Task를 실행한다. Task 완료 후 Pod는 자동 삭제된다.
- **장점**: 완전한 자원 격리, 동적 스케일링, Task별 다른 Docker 이미지 사용 가능
- **단점**: Pod 생성 오버헤드(수십 초), 단발성 Task가 많으면 오버헤드 누적, K8s 운영 지식 필요

### 4.3 실무 배포 구조 (엔터프라이즈)

```
+--------------------------------------------------------------+
|              엔터프라이즈 Airflow 배포 구조                   |
+--------------------------------------------------------------+
|                                                              |
|  Git (DAG 코드 관리)                                         |
|       | CI/CD                                                |
|       v                                                      |
|  DAG 파일 서버 (NFS/S3)                                      |
|       | 마운트                                               |
|       v                                                      |
|  Airflow Web Server <--- 운영자 모니터링                      |
|  Airflow Scheduler                                           |
|       | 태스크 할당                                          |
|       v                                                      |
|  +-----------------------------------------+               |
|  |  Celery Workers (Auto Scaling Group)    |               |
|  |  Worker 1  Worker 2  ...  Worker N      |               |
|  +-----------------------------------------+               |
|       |                                                      |
|       v                                                      |
|  외부 시스템: BigQuery, Spark, S3, Redis, ML 서버            |
|                                                              |
|  메타데이터: Aurora PostgreSQL (Multi-AZ)                    |
|  브로커: Redis ElastiCache                                   |
+--------------------------------------------------------------+
```

📢 **섹션 요약 비유**: 엔터프라이즈 Airflow는 항공사 운항 관리 시스템과 같다. 스케줄러는 관제탑, 워커는 비행기 조종사, Web UI는 항공편 현황판이다. CeleryExecutor는 여러 활주로에서 동시에 비행기를 이륙시키고, KubernetesExecutor는 비행마다 새 조종석을 만들어 격리 운항하는 방식이다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 Airflow 도입 기대효과

| 항목 | 크론탭 기반 | Airflow 기반 | 개선 |
|:---|:---|:---|:---|
| **의존성 관리** | 없음 (시간 기반만) | DAG로 명확한 관계 표현 | 파이프라인 신뢰성 향상 |
| **실패 처리** | 수동 확인 후 재실행 | 자동 재시도 + 알람 | 운영 공수 80% 감소 |
| **가시성** | 없음 | Web UI 실시간 모니터링 | 이슈 감지 속도 향상 |
| **코드 관리** | 분산된 쉘 스크립트 | Git 기반 버전 관리 | 코드 품질 향상 |
| **확장성** | 서버 증설 | CeleryExecutor 워커 추가 | 수평 확장 가능 |

### 5.2 결론

Apache Airflow는 데이터 엔지니어링과 MLOps 분야에서 사실상 표준(De Facto Standard) 워크플로우 오케스트레이션 도구다. DAG 기반 의존성 관리, 풍부한 Operator 생태계, 시각적 모니터링은 복잡한 데이터 파이프라인 운영을 코드로 관리할 수 있게 한다. 실시간 스트리밍이 아닌 배치 파이프라인에서 검증된 선택이다.

📢 **섹션 요약 비유**: Apache Airflow는 복잡한 공사 현장의 공정 관리 시스템과 같다. 기초 공사 -> 골조 -> 배관 -> 마감 순서의 의존성을 DAG로 표현하고, 어느 한 공정이 지연되거나 실패하면 즉시 감리자(운영자)에게 알람을 보내며, 현장 전체 진행 상황을 실시간으로 한눈에 볼 수 있다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 개념 | DAG (Directed Acyclic Graph) | 작업 의존성 표현 그래프 |
| 핵심 구성 | Scheduler | DAG 파싱 및 실행 트리거 |
| 핵심 구성 | Executor | 태스크 실행 방식 결정 |
| 핵심 구성 | Operator | 개별 태스크 실행 단위 |
| 비교 도구 | Luigi (Spotify) | 범용 파이프라인 (경쟁) |
| 비교 도구 | Prefect | 동적 워크플로우 (경쟁) |
| 비교 도구 | Dagster | 데이터 자산 중심 (경쟁) |
| 연관 | Kubeflow Pipelines | ML 특화 파이프라인 (협력/경쟁) |
| 상위 개념 | MLOps | Airflow는 CT 파이프라인 스케줄링에 활용 |
| 클라우드 | Amazon MWAA | AWS 관리형 Airflow |
| 클라우드 | Cloud Composer | GCP 관리형 Airflow |

---

### 👶 어린이를 위한 3줄 비유 설명

1. Airflow는 자동 청소 로봇의 청소 순서 프로그램 같아요. "방 청소 -> 화장실 청소 -> 쓰레기 버리기" 순서를 코드로 적어두면, 매일 새벽에 자동으로 청소를 실행하고 중간에 실패하면 다시 시도해요.
2. DAG는 레고 설명서 같아요. 어느 부품을 먼저 조립해야 다음 부품을 붙일 수 있는지 순서도로 그려두면, 로봇이 알아서 순서대로 조립해요.
3. Executor는 음식 배달 방법 같아요. 혼자 다 배달하거나(Sequential), 여러 명이 나눠서 하거나(Celery), 각 주문마다 드론을 보내는(Kubernetes) 방법 중 상황에 맞게 골라요.

### 📈 관련 키워드 및 발전 흐름도

```text
cron + 쉘 스크립트 (원시적 스케줄링)
    |
    v
Apache Airflow: Python DAG 기반 워크플로우
    +-► Scheduler: DAG 실행 스케줄링
    +-► Executor: Sequential · Celery · Kubernetes
    +-► Web UI: 실행 현황 · 로그 · 재시도 관리
    |
    v
Airflow + Kubernetes Executor -> 동적 Pod 스케일링
    |
    v
차세대 오케스트레이터
    +-► Dagster: 자산 기반 (Asset-centric)
    +-► Prefect: Pythonic, 클라우드 네이티브
    +-► Mage AI: 통합 데이터 파이프라인
```
