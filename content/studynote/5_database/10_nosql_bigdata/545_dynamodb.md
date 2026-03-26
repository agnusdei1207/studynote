+++
title = "Amazon DynamoDB"
description = "AWS의 관리형 NoSQL 데이터베이스 DynamoDB의 특징에 대해 설명"
date = 2024-01-01
weight = 45

[taxonomies]
subjects = ["database"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DynamoDB는 AWS의 Fully Managed NoSQL 데이터베이스로, Provisioned Capacity와 On-Demand 두 가지 모델을 제공하고, 내부적으로 SSTable과 LSM-Tree를 활용하여高性能을 지원한다.
> 2. **가치**: 운영 부담 없는 Fully Managed 서비스로, 자동 확장과グローバル复制을 지원한다.
> 3. **융합**: Amazon Dynamo의分散설계를 기반으로 하며, CAP 이론에서 AP(가용성 + 분단 내성)를 기본으로 제공한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념
DynamoDB는 Amazon Dynamo(2007년 Bezos CEO의 내부 메모)에서インスピレーションを受けて 설계된 全管理형(fully managed) NoSQL 데이터베이스 서비스다. 키-값과 문서 데이터 모델을 지원하며, 확장성, 가용성, 성능에 최적화되어 있다.

### 필요성
 traditionnelles한 관계형 数据库는 확장성에 한계가 있고, 관리 오버헤드가 크다. DynamoDB는 이러한 问题를 해결하여, DevOps 팀의 운영 부담을 줄이면서 대규모 데이터를 처리할 수 있게 한다.

### 섹션 요약 비유
DynamoDBは「完全放置型の图书管理システム」と같くて、本の整理（本を追加 • 检索）を图书委员（AWS）がすべて行って、利用者（開発者）は本の内容（本adingデータ）のみに集中できる。

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### DynamoDB 아키텍처

```text
  ┌───────────────────────────────────────────────────────────────────────┐
  │                    DynamoDB 아키텍처                                      │
  ├───────────────────────────────────────────────────────────────────────┤
  │
  │   [논리적 구조]                                                       │
  │   Table ──▶ Item (Primary Key + Attributes)                         │
  │                                                                       │
  │   [물리적 구조]                                                       │
  │   Partition ──▶ Data Stored in SSTable (compacted)                    │
  │       │                                                               │
  │       └──▶ Partition Server (EC2 instances)                           │
  │                                                                       │
  │   [ 읽기/쓰기 동작]                                                   │
  │   Client ──▶ [분산 해시로 파티션 결정]                                │
  │                  │                                                     │
  │                  ▼                                                     │
  │              ┌──────────────────┐                                      │
  │              │   Partition 1    │                                      │
  │              │   (Replication)  │                                      │
  │              │  N=3 복제份       │                                      │
  │              └──────────────────┘                                      │
  │
  │   [글로벌 테이블]                                                     │
  │   us-east-1 ◀──▶ eu-west-1 ◀──▶ ap-northeast-1                      │
  │       │                      │                     │                    │
  │       └──▶ 모든 리전에 동일 데이터 ──▶                       │
  │
  └───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DynamoDB의 핵심은 파티션 기반 아키텍처다. Primary Key의 해시 값으로 파티션(노드)을 결정하고, 각 파티션 내의 데이터는 SSTable 형식으로 저장된다. 쓰기 동작은 먼저 WAL(Write Ahead Log)에 기록된 후 SSTable에 저장되고, 읽기는 MemTable(메모리)을 먼저 확인한 후 SSTable을 스캔한다. Provisioned Capacity 모드에서는 예상 트래픽을 기반으로 용량을 선 provisioned하고, On-Demand 모드에서는 실제 사용량에 따라 요금이 과금된다. 글로벌 테이블(Global Tables)은 다중 리전에 데이터를 복제하여, 사용자 근처의 리전에서 짧은 지연으로 읽기/쓰기가 가능하다.

### 핵심 특성

| 특성 | 설명 |
|:---|:---|
| **Fully Managed** | 프로비저닝, 패치, 백업 등 AWS가 관리 |
| **Provisioned + On-Demand** | 비용 모델 유연성 |
| **Auto Scaling** | 트래픽 증가 시 자동 확장 |
| **Global Tables** | 다중 리전 복제 |
| **DAX** | In-memory 캐시 (up to 10x faster) |

### 섹션 요약 비유
DynamoDB의 파티션은大型图书馆의分散保管システムと似て、本（항목）を地理的に離れた場所（파티션）に保管し、いつでもどこでもアクセスできる。

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: DynamoDB vs MongoDB

| 구분 | DynamoDB | MongoDB |
|:---|:---|:---|
| **관리** | Fully Managed | Self-managed / Atlas |
| **확장** | 자동 | 수동/자동 (Shard) |
| **요금** | 사용량 기준 | 인프라 기준 |
| ** 글로벌 복제** | 글로벌 테이블 내장 | 별도 설정 필요 |

### 섹션 요약 비유
DynamoDB vs MongoDBは「お抱え厨师 vs Uber Eats」と 같くて、前者は AWSがすべて面倒見て、後者は自分でキッチン（インフラ）を管理する。

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 — Serverless 웹 앱**: AWS Lambda와 조합하여 서버리스 웹 앱을 구축한다. Lambda가 API Gateway를 통해 DynamoDB에 접근하고, 사용자의 세션, 주문, 좋아요 등을 저장한다. On-Demand 모드로初期비용为零で、トラフィック増加時に自動で拡張される。

### 도입 체크리스트
- **기술적**: Primary Key 설계가 접근 패턴을 반영해야 하며, 가능하다면 Single Table Design을 활용한다.
- **운영·보안적**:Provisioned 모드에서는 용량 planning이重要이고,On-Demand 모드에서는 비용관리가重要하다.

### 안티패턴
- **핫 파티션**: 특정 키에 트래픽이集中하면 해당 파티션이 병목이 된다. Partition 수를 늘리는 것이 아니라, 스로틀링이 발생할 수 있다.
- **과도한 스캔**: Scan operation은 전체 테이블을 스캔하므로 사용을 피하고, Query나 GetItem을 사용한다.

### 섹션 요약 비유
DynamoDB의 Hot Partition問題は「一箇所の売場に全員押し掛ける」ことと似ていて店侧（AWS）はokie，但是如果(設計)가 잘못되면店侧が悲鳴を上げる。

---

## Ⅴ. 기대효과 및 결론

### DynamoDB strengths

| 구분 | 효과 |
|:---|:---|
| **관리 부담** | ゼロ (fully managed) |
| **확장성** | 거의 無限制 |
| **글로벌 서비스** | 짧은 지연 시간 |
| **가용성** | 99.999% |

### 미래 전망
- **DynamoDBTransactions**: 이제跨파티션 트랜잭션을 지원하여, より 많은 워크로드에適用可能해졌다.
- **PartiQL**: SQL 호환 쿼리 언어로, 기존 SQL 사용자가更容易게 DynamoDB를活用할 수 있게 했다.

### 섹션 요약 비유
DynamoDBの進化は「置き配の 完全自动化」と似ていて、受取人（開発者）が家门口（테이블）에만 신경 쓰けば、配送（ 인프라 管理）は全部 业社（AWS）が自動的に行う。

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **SSTable** | DynamoDB의 데이터 저장 형식으로, 정렬된 Key-Value 쌍의 불변 파일이다. |
| **LSM-Tree** | SSTable을 활용하는 쓰기 최적화 자료구조로, Cassandra도 동일한 구조를 사용한다. |
| **CAP 이론** | DynamoDB는 AP를 기본으로 제공하지만, Strongly Consistent Read 옵션으로 CP로도使用可能하다. |
| **Provisioned + On-Demand** | 두 가지 비용 모델로, 다양한 워크로드에 유연하게対応한다. |
| **Global Tables** | 다중 리전 복제로, 글로벌な可用성을 제공하는 DynamoDB의 기능이다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. DynamoDBは「无人岛での 自动販売机」と같くて、機械（AWS）がすべての補充と修理を行って、利用者（開発者）はお金を選ぶだけだ。
2. 需要が増えると（トラフィック増加）自动的により多くの机械（パーティション）が増える!
3. ただし、1台の机械に客が杀到すると（ホットパーティション）その机械悲鳴を上げてしまう!
