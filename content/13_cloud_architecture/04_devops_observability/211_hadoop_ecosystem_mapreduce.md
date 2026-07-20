---
title: "Hadoop Ecosystem"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 211
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하둡(Hadoop)은 단일 서버 한계를 넘기 위해 수천 대의 범용 서버에 데이터를 분산 저장(HDFS)하고 분산 처리(MapReduce)하는 오픈소스 프레임워크로, Apache Software Foundation(ASF)의 핵심 프로젝트다.
> 2. **가치**: HDFS·MapReduce·YARN이라는 3개의 핵심 레이어 위에 Hive(SQL)·Pig(스크립트)·HBase(NoSQL)·Spark(고속 처리)·Kafka(스트리밍) 등이 에코시스템을 형성하여 모든 빅데이터 처리 요구를 커버한다.
> 3. **판단 포인트**: 현재 하둡은 직접 운영보다 클라우드 관리형 서비스(AWS EMR, GCP Dataproc)로 사용하는 것이 주류다. 하둡을 알아야 하는 이유는 클라우드 서비스의 내부 동작 원리를 이해하기 위해서다.

---

## Ⅰ. 개요 및 필요성

하둡은 2006년 Doug Cutting과 Mike Cafarella가 구글의 두 논문(GFS: Google File System, 2003; MapReduce, 2004)을 영감받아 개발했다. 이름의 유래는 Cutting의 아들이 노란 코끼리 장난감에 붙인 이름이다.

하둡의 탄생 배경은 2000년대 웹 크롤러 데이터 문제였다. Yahoo!, Amazon 같은 회사들이 수십~수백 TB의 웹 데이터를 처리해야 했지만, 당시 단일 서버로는 불가능했다. 수천 대의 범용(Commodity) 서버를 네트워크로 연결하여 분산 처리하면 된다는 아이디어가 하둡이었다.

핵심 철학: **하드웨어는 반드시 고장 난다(Hardware Failure is the Norm).** 수천 대 서버 중 일부가 항상 고장 상태이므로, 데이터를 여러 노드에 복제(기본 3벌)하여 하드웨어 고장을 소프트웨어로 투명하게 처리한다.

📢 **섹션 요약 비유**: 하둡은 대형 마트의 물류 시스템과 같다. 상품(데이터)을 하나의 거대한 창고(단일 서버)에 모두 넣는 대신, 수천 개의 작은 창고(분산 서버)에 나눠서 보관하고, 창고 목록(HDFS NameNode)을 중앙에서 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 하둡 에코시스템 구조도

```
  +------------------------------------------------------------+
  |                  하둡 에코시스템                              |
  +------------------------------------------------------------+
  |  쿼리/SQL     |  Hive   |  Pig   |  Spark SQL |  Presto   |
  +------------------------------------------------------------+
  |  처리 엔진    |  MapReduce    |  Apache Spark    |  Flink   |
  +------------------------------------------------------------+
  |  리소스 관리  |              YARN                           |
  +------------------------------------------------------------+
  |  분산 저장    |              HDFS                           |
  +------------------------------------------------------------+
  |  NoSQL DB     |  HBase   |  Cassandra                      |
  +------------------------------------------------------------+
  |  스트리밍     |  Kafka   |  Flume   |  Spark Streaming     |
  +------------------------------------------------------------+
  |  데이터 수집  |  Sqoop (RDB ↔ HDFS)  |  Flume (로그)       |
  +------------------------------------------------------------+
  |  조율/관리    |  ZooKeeper |  Oozie (워크플로우)             |
  +------------------------------------------------------------+
```

### 핵심 컴포넌트 역할

| 컴포넌트 | 역할 |
|:---|:---|
| <strong>HDFS</strong> | Hadoop Distributed File System — 분산 파일 저장 |
| <strong>MapReduce</strong> | 분산 병렬 연산 프레임워크 |
| <strong>YARN</strong> | Yet Another Resource Negotiator — 클러스터 자원 관리 |
| <strong>Hive</strong> | HDFS 데이터에 SQL 쿼리 제공 (SQL-on-Hadoop) |
| **Pig** | 데이터 변환·분석 스크립트 언어 (Pig Latin) |
| <strong>HBase</strong> | 하둡 위의 NoSQL 칼럼 기반 분산 DB (Bigtable 영감) |
| **Spark** | 메모리 기반 고속 처리 엔진 (MapReduce 대체) |
| <strong>ZooKeeper</strong> | 분산 시스템 코디네이션 (설정 공유, 리더 선출) |
| **Sqoop** | RDBMS ↔ HDFS 양방향 데이터 전송 |
| **Oozie** | Hadoop 워크플로우 스케줄러 |

📢 **섹션 요약 비유**: 하둡 에코시스템은 공장의 생산 시스템과 같다. HDFS는 창고, YARN은 인력 배치 담당자, MapReduce/Spark는 작업 공정, Hive는 공장 보고서 시스템, HBase는 실시간 재고 관리 시스템이다.

---

## Ⅲ. 비교 및 연결

### 하둡 vs 기존 RDBMS

| 항목 | RDBMS | 하둡 |
|:---|:---|:---|
| 스케일 | 수직 확장 (Scale-Up) | 수평 확장 (Scale-Out) |
| 데이터 유형 | 정형 (Structured) | 정형 + 반정형 + 비정형 |
| 스키마 | 사전 정의 (Schema-on-Write) | 사후 정의 (Schema-on-Read) |
| 비용 | 고가 서버 | 저가 범용 서버 |
| 처리 속도 | 빠른 트랜잭션 | 대규모 배치 (느린 응답) |
| ACID | ✅ 완전 지원 | ❌ 제한적 |

### 하둡 버전 진화

| 버전 | 특징 |
|:---:|:---|
| Hadoop 1.x | JobTracker + TaskTracker (단일 장애 지점 존재) |
| Hadoop 2.x | YARN 도입 (리소스 분리), HDFS HA 추가 |
| Hadoop 3.x | Erasure Coding(저장 효율^), 서비스 성숙 |

📢 **섹션 요약 비유**: RDBMS와 하둡의 차이는 정밀 시계 장인(RDBMS)과 조립 라인 공장(하둡)의 차이다. 장인은 하나를 완벽하게 만들지만, 공장은 수만 개를 동시에 만든다. 정밀도(ACID)와 규모(Scale)의 트레이드오프다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>클라우드에서의 하둡 사용 (AWS EMR)</strong>:
```
# AWS EMR 클러스터 생성 (최소 구성)
aws emr create-cluster \
  --name "MyHadoopCluster" \
  --release-label emr-6.10.0 \
  --applications Name=Hadoop Name=Spark Name=Hive \
  --instance-type m5.xlarge \
  --instance-count 3 \
  --use-default-roles

# 스팟 인스턴스로 비용 절약
# 핵심 마스터 노드: On-Demand, 워커 노드: Spot
```

<strong>Hive SQL 예시</strong>:
```sql
-- HDFS의 CSV 파일에 SQL 쿼리
CREATE EXTERNAL TABLE sales (
  date STRING,
  product_id INT,
  amount DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://mybucket/sales/';

SELECT product_id, SUM(amount) as total
FROM sales
WHERE date >= '2026-01-01'
GROUP BY product_id
ORDER BY total DESC;
```

**실무자 판단 포인트**:
- 현대 클라우드 환경에서 하둡 직접 운영보다 EMR/Dataproc 관리형 서비스 사용이 TCO(총소유비용) 관점에서 유리하다.
- HDFS vs S3 + Spark 아키텍처: 클라우드에서는 HDFS를 S3로 대체하고 Spark를 독립 실행하는 "S3 중심 아키텍처"가 운영 효율이 높다.
- HBase의 경우 AWS DynamoDB, GCP Bigtable 같은 클라우드 관리형 서비스로 대체되는 추세다.

📢 **섹션 요약 비유**: 현대에 하둡을 직접 운영하는 것은 오늘날 자가발전기를 직접 설치하는 것과 같다. 한전(클라우드 관리형 서비스)에서 전기를 구매하는 것이 훨씬 효율적이다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 수평 확장 | 서버 추가만으로 처리 용량 선형 확장 |
| 저비용 인프라 | 고가 전용 서버 없이 범용 서버로 구성 |
| 유연한 데이터 | 정형·비정형 모든 데이터 처리 가능 |
| 내결함성 | 3벌 복제로 하드웨어 고장을 투명하게 처리 |

하둡 에코시스템은 빅데이터 시대를 연 기반 기술이다. 직접 운영은 줄었지만, 클라우드 관리형 서비스(EMR, Dataproc)와 Apache Spark가 하둡의 핵심 아이디어를 계승하여 현재도 대규모 데이터 처리의 표준이다.

📢 **섹션 요약 비유**: 하둡은 인터넷의 HTTP 프로토콜과 같다. 직접 보이지 않지만, 우리가 사용하는 모든 웹서비스의 기반을 형성했다. 하둡을 모르면 현대 데이터 처리 시스템의 뿌리를 이해하지 못한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HDFS | 하둡 분산 파일 시스템, 빅데이터 저장의 토대 |
| MapReduce | 하둡 1세대 분산 처리 엔진, 스파크로 대체 중 |
| YARN | 하둡 2.x의 범용 리소스 관리자 |
| Apache Spark | 하둡 MapReduce의 후계자, 메모리 기반 고속 처리 |
| AWS EMR | 클라우드 관리형 하둡/스파크 서비스 |
| 구글 GFS/BigTable | 하둡/HBase의 영감이 된 구글 논문 |

### 👶 어린이를 위한 3줄 비유 설명

1. 하둡은 수천 개의 작은 레고 상자를 연결해서 아주 큰 작품을 만드는 것처럼, 수천 대의 작은 서버를 연결해서 엄청 큰 데이터를 처리해.

### 📈 관련 키워드 및 발전 흐름도

```text
Hadoop 1.0: HDFS + MapReduce (일체형)
    |
    v
Hadoop 2.0: YARN 분리 -> 다양한 처리 엔진 지원
    |
    v
Hadoop 3.0: Erasure Coding + GPU 지원 -> 클라우드 최적화
```
2. HDFS는 레고 조각을 여러 상자에 나눠 담고 목록을 관리하는 것이고, YARN은 어느 상자에서 누가 일할지 배정하는 담당자야.
3. 혼자(단일 서버) 할 수 없는 일을 여럿(분산 서버)이 나눠서 하는 게 핵심이야.
