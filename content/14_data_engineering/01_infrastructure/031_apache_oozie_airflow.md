---
title: "Apache Oozie Airflow"
date: "2026-04-29"
tags:
  - "studynote-data-engineering"
weight: 31
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Oozie는 Hadoop 생태계 전용 XML 기반 워크플로 스케줄러이고, Apache Airflow는 Python DAG 기반 범용 오케스트레이터다. 현대 데이터 엔지니어링에서는 Airflow가 사실상 표준(de facto)이 됐다.
> 2. **가치**: Airflow의 핵심 강점은 ① Python 코드로 복잡한 의존성 표현, ② 풍부한 Operator(200+), ③ 강력한 모니터링 UI, ④ 클라우드 네이티브 통합(AWS/GCP/Azure)이다. 반면 Oozie는 레거시 Hadoop 환경에서 여전히 현역이다.
> 3. **판단 포인트**: 마이그레이션 결정 기준: 온프레미스 Hadoop 전용이면 Oozie 유지, 클라우드 이전 계획이 있거나 클라우드 서비스 통합이 필요하면 Airflow 마이그레이션이 합리적이다.

---

## Ⅰ. 개요 및 필요성

```text
워크플로 스케줄러 비교:

  Oozie:                    Airflow:
  workflow.xml              from airflow import DAG
  <workflow-app>            from airflow.operators import *
    <action name="hive">
      <hive>...</hive>      with DAG('etl', ...) as dag:
      <ok to="next"/>         t1 = HiveOperator(...)
      <error to="fail"/>      t2 = SparkSubmitOperator(...)
    </action>                 t1 >> t2
  </workflow-app>

  XML 설정 -> Python 코드
  복잡하고 장황 -> 직관적
```

- **📢 섹션 요약 비유**: Oozie vs Airflow는 요리 레시피 형식이다. Oozie(XML)는 고대 문서처럼 태그로 작성해야 하고, Airflow(Python)는 자연스러운 한국어 레시피처럼 읽기 쉽고 작성하기 편하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Airflow 핵심 컴포넌트

| 컴포넌트 | 역할 |
|:---|:---|
| **Scheduler** | DAG 파싱·실행 스케줄링 |
| **Executor** | 태스크 실행 (Local/Celery/K8s) |
| **Worker** | 실제 태스크 수행 |
| <strong>Metadata DB</strong> | DAG·태스크 상태 저장 (PostgreSQL) |
| **Webserver** | 모니터링 UI |
| <strong>DAG Bag</strong> | DAG 파일 디렉토리 |

### Airflow DAG 예시

```python
from airflow import DAG
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

with DAG(
    dag_id='daily_etl',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    extract = HiveOperator(
        task_id='extract',
        hql='INSERT INTO staging SELECT * FROM raw WHERE date = "{{ ds }}"'
    )

    transform = SparkSubmitOperator(
        task_id='transform',
        application='/jobs/transform.py',
        application_args=['--date', '{{ ds }}']
    )

    extract >> transform  # 의존성 정의
```

- **📢 섹션 요약 비유**: Airflow DAG는 요리 순서표다. Python으로 "재료 손질(extract) 다음에 조리(transform)"처럼 자연스럽게 의존 관계를 표현하고, 실패 시 어느 단계에서 멈췄는지 그래프로 한눈에 확인한다.

---

## Ⅲ. 비교 및 연결

| 비교 | Oozie | Airflow | Prefect | Dagster |
|:---|:---|:---|:---|:---|
| 설정 방식 | XML | Python | Python | Python |
| Hadoop 통합 | ✅ 최적 | ✅ Operator | ❌ | ❌ |
| 클라우드 | △ 제한 | ✅ 풍부 | ✅ | ✅ |
| UI | 기본 | 강력 | 강력 | 강력 |
| 데이터 인식 | ❌ | △ | ✅ | ✅ |

- **📢 섹션 요약 비유**: 4가지 스케줄러는 세대별 공장 자동화다. Oozie(1세대), Airflow(2세대 표준), Prefect·Dagster(3세대 클라우드 네이티브)로 발전했다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Oozie -> Airflow 마이그레이션 전략

```text
1단계: Oozie XML 분석
  - workflow.xml -> 태스크 그래프 추출
  - coordinator.xml -> 스케줄 패턴 추출

2단계: Airflow DAG 변환
  - Oozie Action -> Airflow Operator 매핑
  - Oozie OK/Error -> Airflow trigger_rule
  - Oozie 변수 -> Airflow Jinja 템플릿

3단계: 병행 운영
  - 동일 파이프라인 양쪽 실행 비교
  - 결과 일치 확인

4단계: Oozie 종료
```

### 관리형 Airflow 서비스

```text
AWS MWAA (Managed Workflows for Apache Airflow):
  - Airflow 클러스터 관리 자동화
  - VPC 통합, IAM 권한 관리
  - 자동 스케일링

GCP Cloud Composer:
  - GKE 기반 관리형 Airflow
  - BigQuery·GCS 네이티브 통합

Azure Data Factory:
  - 비주얼 파이프라인 (GUI 방식)
  - Airflow 아닌 독자 오케스트레이터
```

- **📢 섹션 요약 비유**: 관리형 Airflow는 클라우드 식당 렌탈이다. 직접 주방을 차리고 관리하는 대신(직접 설치), 식당 공간(AWS MWAA)을 빌려서 요리(DAG 작성)에만 집중할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:Episcopal: 내용 |
|:---|:---|
| **가시성** | DAG UI로 파이프라인 전체 상태 확인 |
| **유연성** | Python으로 복잡한 의존성 표현 |
| **통합성** | 200+ Operator로 모든 서비스 연결 |

LLM 기반 DAG 자동 생성이 등장하고 있다. "매일 새벽 2시에 S3에서 데이터 읽어서 BigQuery에 적재하고 실패 시 Slack 알림"을 자연어로 입력하면 Airflow DAG 코드를 자동 생성하는 도구가 실용화 단계에 있다. 데이터 엔지니어의 역할이 DAG 작성에서 요구사항 정의로 이동하고 있다.

- **📢 섹션 요약 비유**: LLM DAG 자동 생성은 AI 요리사다. "이런 요리를 만들어줘"라고 말하면 AI가 레시피(DAG)를 자동으로 작성해주는 것처럼, 데이터 파이프라인 코드를 자연어로 생성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>DAG</strong> | Airflow 워크플로 표현 단위 |
| <strong>Operator</strong> | Airflow 태스크 실행 단위 |
| **Celery Executor** | 분산 태스크 실행 엔진 |
| **AWS MWAA** | 관리형 Airflow 클라우드 서비스 |
| **Prefect/Dagster** | 차세대 데이터 오케스트레이터 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cron + 쉘 스크립트 — 기초 배치 스케줄링]
    |
    v
[Apache Oozie — Hadoop 전용 XML 스케줄러]
    |
    v
[Apache Airflow — Python DAG 범용 오케스트레이터]
    |
    v
[관리형 Airflow — AWS MWAA, GCP Composer]
    |
    v
[LLM DAG 생성 — 자연어 -> 파이프라인 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Oozie는 복잡한 XML 설명서, Airflow는 읽기 쉬운 Python 코드로 데이터 파이프라인을 만들어요!
2. Airflow UI에서 마치 지하철 노선도처럼 데이터가 어디서 어디로 흐르는지 한눈에 볼 수 있어요!
3. AI가 "매일 새벽 데이터 가져와서 분석해줘"라는 말만으로 자동으로 파이프라인 코드를 만들어주는 시대가 오고 있어요!
