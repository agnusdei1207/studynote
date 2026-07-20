---
title: "Azure Event Hubs"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 93
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Azure Event Hubs (애저 이벤트 허브)는 Microsoft Azure의 완전 관리형 이벤트 스트리밍 서비스로, Apache Kafka 프로토콜 호환 엔드포인트를 제공하여 기존 Kafka 클라이언트 코드 변경 없이(Drop-in Replacement) 마이그레이션이 가능하다.
- **가치**: Kafka 호환 API 덕분에 온프레미스 Kafka -> Azure 마이그레이션 경로가 쉽고, AMQP/HTTPS도 지원하여 다양한 클라이언트와 통합되며, Capture 기능으로 원본 이벤트를 Azure Data Lake Storage(ADLS)에 자동 백업하여 장기 분석 파이프라인을 구성한다.
- **판단 포인트**: Event Hubs Standard vs Premium vs Dedicated 티어 선택이 핵심이다. Standard는 비용 효율적이나 처리량 제한이 있고, Premium은 전용 컴퓨팅으로 예측 가능한 성능을, Dedicated는 전용 클러스터로 최대 100TB 스토리지와 VNET 격리를 제공한다.

---

## Ⅰ. 개요 및 필요성

### 1. Azure Event Hubs 위치

Azure의 이벤트 서비스 패밀리에서 Event Hubs의 역할:

| 서비스 | 역할 | 비교 |
|:---|:---|:---|
| Event Hubs | 대용량 스트림 수집 (초당 수백만 이벤트) | Kafka, Kinesis |
| Service Bus | 큐/토픽 기반 메시징 (트랜잭션 보장) | RabbitMQ, SQS |
| Event Grid | 이벤트 라우팅 (Azure 서비스 이벤트) | EventBridge |

### 2. Kafka 호환 엔드포인트

```python
# 기존 Kafka 클라이언트 코드를 Event Hubs에서 사용
# bootstrap.servers만 변경하면 됨!

from confluent_kafka import Producer

config = {
    'bootstrap.servers': 'my-eh-namespace.servicebus.windows.net:9093',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '$ConnectionString',
    'sasl.password': 'Endpoint=sb://my-eh-namespace...',  # SAS 연결 문자열
}

producer = Producer(config)
producer.produce('my-event-hub', key='user-001', value='{"action": "click"}')
```

**📢 섹션 요약 비유**
> Kafka 호환 API는 "해외 전자 제품의 어댑터(어댑터)"와 같다. 플러그 모양(Kafka API)은 같고 소켓(Event Hubs)만 다른데, 어댑터(Kafka 프로토콜 지원)를 꽂으면 기존 제품(Kafka 클라이언트)을 그대로 사용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Event Hubs 구조

```
+-------------------------------------------------------------+
|  Event Hubs Namespace                                        |
|                                                             |
|  +-----------------------------------------------------+   |
|  |  Event Hub (토픽): "telemetry"                       |   |
|  |                                                      |   |
|  |  파티션 0 --- 이벤트 스트림 ---> Consumer Group A     |   |
|  |  파티션 1 --- 이벤트 스트림 ---> Consumer Group A     |   |
|  |  파티션 2 --- 이벤트 스트림 ---> Consumer Group B     |   |
|  |                                                      |   |
|  |  Capture: 자동 -> Azure Blob Storage / ADLS Gen2      |   |
|  +-----------------------------------------------------+   |
|                                                             |
|  프로토콜: AMQP 1.0 / Kafka API (9093) / HTTPS             |
+-------------------------------------------------------------+
                              |
         +-------------------+------------------+
         v                   v                  v
  Azure Stream           Azure Databricks    Azure Function
  Analytics              (Spark Streaming)   (서버리스)
```

### 2. 티어별 비교

| 티어 | 처리량 단위 | 파티션 수 | 스토리지 | 특징 |
|:---|:---|:---|:---|:---|
| Standard | TU (처리량 단위) | 최대 32 | 최대 1TB | 비용 효율적, 소규모 |
| Premium | PU (처리 단위) | 최대 100 | 10GB/PU | 전용 컴퓨팅, 예측 성능 |
| Dedicated | CU (용량 단위) | 최대 1,024 | 최대 100TB/CU | 전용 클러스터, VNET |

### 3. Capture 기능

```json
// Event Hub Capture 설정
{
  "capture": {
    "enabled": true,
    "encoding": "Avro",
    "intervalInSeconds": 300,       // 5분마다 캡처
    "sizeLimitInBytes": 314572800,  // 300MB마다 캡처
    "destination": {
      "storageAccountResourceId": "/subscriptions/.../storageAccounts/myStorage",
      "blobContainer": "event-hub-data",
      "archiveNameFormat": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"
    }
  }
}
```

**📢 섹션 요약 비유**
> Capture 기능은 "TV 방송 자동 녹화 기능"이다. 라이브 스트림(Event Hubs)을 보면서 동시에 녹화(ADLS에 저장)하여 나중에 다시 볼 수 있다.

---

## Ⅲ. 비교 및 연결

### 1. Azure Event Hubs vs Apache Kafka vs Amazon Kinesis

| 비교 항목 | Azure Event Hubs | Apache Kafka | Amazon Kinesis |
|:---|:---|:---|:---|
| Kafka 호환 | ✅ (드롭인 교체) | 원본 | ❌ |
| 관리 방식 | 완전 관리형 | 자체/MSK/Confluent | 완전 관리형 |
| 파티션 수 | 최대 1,024 (Dedicated) | 무제한 | 샤드 수 기반 |
| 보존 기간 | 최대 90일 | 무제한 | 최대 365일 |
| 글로벌 Geo-DR | ✅ (Event Hubs Geo-DR) | 수동 MirrorMaker 2 | ❌ 기본 |
| 프로토콜 | AMQP, Kafka, HTTPS | Kafka binary | HTTP |
| Azure 통합 | 최고 | 별도 커넥터 | ❌ |

### 2. Schema Registry (Event Hubs)

Azure Event Hubs는 <strong>Schema Registry</strong>를 내장하여 Avro/JSON Schema 기반의 메시지 스키마를 중앙에서 관리한다.

```python
# Event Hubs Schema Registry 활용
from azure.schemaregistry import SchemaRegistryClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
schema_registry = SchemaRegistryClient(
    fully_qualified_namespace="my-namespace.servicebus.windows.net",
    credential=credential
)
```

**📢 섹션 요약 비유**
> Event Hubs의 Kafka 호환성은 "국제 표준 철도 궤도 폭 채택"과 같다. 한국(Kafka 애플리케이션) 열차가 유럽(Azure) 선로에서도 달릴 수 있도록 궤도 폭(프로토콜)을 맞춘 것이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Azure + Kafka 마이그레이션 경로

```
온프레미스 Kafka 클러스터
  v MirrorMaker 2 (병렬 복제)
Azure Event Hubs (Kafka 호환)
  v 검증 완료 후 기존 클러스터 종료
```

### 2. 이벤트 처리 아키텍처

```
IoT 디바이스/웹앱 -> Event Hubs -> Azure Stream Analytics -> Power BI (실시간 대시보드)
                              +---> Azure Databricks/Spark -> ADLS Gen2 (배치 분석)
                              +---> Azure Functions -> Azure Cosmos DB (실시간 상태 업데이트)
                              +---> Capture -> ADLS Gen2 (원본 보존)
```

### 3. 체크리스트

- [ ] 처리량 요구사항 기반 티어 선택 (Standard -> Premium -> Dedicated)
- [ ] Kafka 마이그레이션: 연결 문자열만 변경하여 테스트
- [ ] Capture 설정: 원본 이벤트 보존 정책 수립
- [ ] Geo-DR 설정: 페어링 네임스페이스로 DR 구성
- [ ] Consumer Group 격리: 서비스별 독립적 오프셋 관리

**📢 섹션 요약 비유**
> Event Hubs Standard -> Dedicated는 "공용 수영장 -> 개인 수영장 임대"와 같다. 공용(Standard)은 저렴하지만 피크 시간에 혼잡하고, 개인(Dedicated)은 비싸지만 항상 전용 레인을 보장한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| Kafka 마이그레이션 용이 | 코드 변경 없이 Azure로 전환 |
| Azure 통합 | Databricks/Stream Analytics/Functions 네이티브 연동 |
| Geo-DR | 자동 지역 페일오버로 비즈니스 연속성 보장 |
| Capture | 원본 이벤트 자동 보관으로 감사 및 재처리 지원 |

### 2. 결론

Azure Event Hubs는 <strong>Kafka 호환성을 통한 점진적 마이그레이션</strong>과 Azure 생태계 최적화를 동시에 달성하는 엔터프라이즈 스트리밍 플랫폼이다. 학습 정리에서는 Kafka 드롭인 교체의 의미, 티어별 특성, Capture를 통한 레이크하우스 연계, Geo-DR 구성을 중심으로 서술하면 된다.

**📢 섹션 요약 비유**
> Event Hubs는 "Microsoft의 스트리밍 다리"다. Azure라는 섬으로 Kafka라는 대륙에서 건너올 수 있는 다리를 놓아서, 기존 Kafka 여행자들이 배(완전한 이식)가 아닌 차(Kafka 호환 API)로 바로 건너올 수 있게 했다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Apache Kafka | 호환 대상 | Kafka 프로토콜 드롭인 교체 |
| Amazon Kinesis | 경쟁 서비스 | AWS 동등 포지션 |
| Azure Databricks | 통합 처리 | Spark Structured Streaming과 연동 |
| Azure Data Lake Gen2 | 저장 대상 | Capture 기능으로 자동 보관 |
| Kafka MirrorMaker 2 | 마이그레이션 도구 | 온프레미스 -> Event Hubs 마이그레이션 |


### 📈 관련 키워드 및 발전 흐름도

```text
[이벤트 소스 (Event Sources) — IoT·앱·클릭스트림, 초당 수백만 이벤트]
    |
    v
[아파치 카프카 (Apache Kafka) — 오픈소스 고처리량 메시지 스트리밍]
    |
    v
[Azure Event Hubs — Kafka 호환, 완전 관리형 이벤트 스트리밍 서비스]
    |
    v
[Azure Stream Analytics — 실시간 SQL 쿼리 처리, 창 집계(Window)]
    |
    v
[Azure Synapse Analytics / Power BI — 배치 분석 및 시각화 대시보드]
```
Azure Event Hubs는 Apache Kafka 호환 API를 제공하며, 완전 관리형 서비스로 대규모 이벤트를 수집하여 Azure 분석 파이프라인의 진입점 역할을 한다.
### 👶 어린이를 위한 3줄 비유 설명

Azure Event Hubs는 Microsoft의 편지 배달 시스템이에요. 특별한 점은 Kafka라는 다른 우편 시스템의 편지(Kafka 메시지)도 받을 수 있어요(Kafka 호환 API). 중요한 편지는 자동으로 사진을 찍어 보관(Capture -> ADLS)하고, 다른 도시(다른 Azure 리전)에도 복사본을 보내서 편지가 절대 없어지지 않도록 해요(Geo-DR)!
