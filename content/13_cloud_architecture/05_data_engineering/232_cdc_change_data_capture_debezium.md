---
title: "Change Data Capture /"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 232
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CDC(Change Data Capture, 변경 데이터 캡처)는 운영 DB의 <strong>트랜잭션 로그(Redo Log/Binlog)</strong>를 직접 읽어 INSERT·UPDATE·DELETE 이벤트를 실시간 추출하는 기술로, DB에 추가 부하 없이 변경분만 캡처한다.
> 2. **가치**: 전통적 ETL의 "전체 테이블 스캔 주기 배치" 대신, <strong>밀리초 단위 실시간 데이터 동기화</strong>를 가능하게 하여 데이터 레이크·DW의 신선도를 획기적으로 향상한다.
> 3. **판단 포인트**: <strong>Debezium</strong>이 오픈소스 CDC의 사실상 표준으로, Kafka Connect 기반으로 MySQL·PostgreSQL·Oracle·MongoDB 등 주요 DB의 로그를 Kafka 토픽으로 스트리밍한다.

---

## Ⅰ. 개요 및 필요성

전통적 ETL은 주기적으로(야간) 운영 DB에서 `SELECT * WHERE updated_at > 어제`로 변경 데이터를 추출한다. 이 방식의 문제는:
- DB 부하: 대용량 스캔 쿼리가 운영 DB 성능에 영향
- 지연: T+1일 또는 최소 수분 주기, 실시간 불가
- 삭제 감지 불가: 물리 삭제된 행은 `updated_at` 방식으로 감지 불가
- 타임스탬프 없는 테이블: 변경 감지 자체 불가

CDC는 이 모든 문제를 DB의 <strong>트랜잭션 로그</strong>를 읽는 방식으로 해결한다.

```
[전통 ETL 방식]
Batch 쿼리 (SELECT * WHERE updated > ?)
운영 DB -------------------------------> DW
        ^ DB 부하 발생, 매 시간/일 스캔

[CDC 방식]
트랜잭션 로그 (Binlog/Redo Log)
운영 DB ---> Debezium ---> Kafka ---> DW/레이크
        ^ 로그 읽기 (읽기 전용, 최소 부하)
        ^ 밀리초 단위 실시간 전송
```

📢 **섹션 요약 비유**: CDC는 CCTV 영상 기록이다. 누군가 가게(DB)에 들어와 물건을 가져가거나(DELETE), 추가하거나(INSERT), 바꾸면(UPDATE), CCTV(트랜잭션 로그)가 자동으로 기록한다. 가게를 닫고 재고 조사(배치 스캔)를 하지 않아도 실시간으로 변화를 감지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Debezium 아키텍처

```
+----------------------------------------------------------------+
|                    CDC 파이프라인 (Debezium)                    |
|                                                                |
|  MySQL/PostgreSQL        Kafka Connect          Kafka Topic    |
|  +--------------+        +---------------+      +----------+  |
|  |  운영 DB     |  로그   |   Debezium    |  이벤트| orders.  |  |
|  |  Binlog/    | -------> |  Source       | -----> | public.  |  |
|  |  WAL 읽기   |        |  Connector    |       | orders   |  |
|  |             |        |               |       +----------+  |
|  | INSERT/     |        |  변경 이벤트  |                     |
|  | UPDATE/     |        |  to JSON/Avro |  +----------------+ |
|  | DELETE      |        |               |  | Kafka Sink     | |
|  +--------------+        +---------------+  | Connector      | |
|                                             | (S3/Snowflake/ | |
|                                             |  Elasticsearch)| |
|                                             +----------------+ |
+----------------------------------------------------------------+
```

### CDC 이벤트 메시지 구조 (Debezium JSON 예시)

```json
{
  "op": "u",            // c=create, u=update, d=delete, r=read(snapshot)
  "before": {           // 변경 전 상태
    "order_id": 1001,
    "status": "pending",
    "amount": 50000
  },
  "after": {            // 변경 후 상태
    "order_id": 1001,
    "status": "shipped",
    "amount": 50000
  },
  "source": {
    "table": "orders",
    "ts_ms": 1705123456789,  // 이벤트 발생 타임스탬프
    "pos": "mysql-bin.000001:12345"  // 로그 위치
  }
}
```

### 주요 DB별 CDC 로그 메커니즘

| DB | 로그 유형 | Debezium 커넥터 |
|:---|:---|:---|
| **MySQL** | Binary Log (Binlog) | debezium-mysql |
| **PostgreSQL** | Write-Ahead Log (WAL) | debezium-postgres |
| <strong>Oracle</strong> | Redo Log | debezium-oracle |
| **SQL Server** | Transaction Log | debezium-sqlserver |
| <strong>MongoDB</strong> | Oplog (Operations Log) | debezium-mongodb |
| <strong>DynamoDB</strong> | DynamoDB Streams | AWS native CDC |

📢 **섹션 요약 비유**: Debezium은 DB의 "일기장"을 읽는 독자다. DB는 모든 변경 내역을 일기장(트랜잭션 로그)에 자동으로 쓴다. Debezium은 이 일기장을 몰래 읽어(비침습적) Kafka에 전달한다. DB는 일기를 쓰는 것 외에 추가 작업이 없다.

---

## Ⅲ. 비교 및 연결

### CDC vs 전통 ETL 배치 비교

| 비교 항목 | CDC (Debezium + Kafka) | 전통 배치 ETL |
|:---|:---|:---|
| <strong>지연 시간</strong> | 밀리초~초 | 분~시간 |
| **DB 부하** | 매우 낮음 (로그 읽기) | 높음 (테이블 풀스캔) |
| **삭제 감지** | 가능 (DELETE 이벤트) | 불가 (행 사라짐) |
| <strong>스키마 없는 테이블</strong> | 가능 | 타임스탬프 없으면 불가 |
| <strong>초기 설정</strong> | 복잡 (Kafka Connect 설정) | 단순 (SQL 쿼리) |
| **운영 복잡성** | 높음 | 낮음 |
| **적합 환경** | 실시간 동기화 필요 | 일 배치 DW 적재 |

### CDC 활용 패턴

| 패턴 | 설명 | 사례 |
|:---|:---|:---|
| <strong>DB -> Data Lake</strong> | 운영 DB 변경분 실시간 레이크 적재 | RDS -> S3 Delta Lake |
| <strong>DB -> DW</strong> | 운영 DB -> 데이터 웨어하우스 실시간 동기화 | MySQL -> Snowflake |
| **DB -> Cache** | DB 변경 시 캐시 즉시 무효화 | PostgreSQL -> Redis |
| <strong>MSA 이벤트 소싱</strong> | 서비스 DB 변경 -> 다른 서비스 이벤트 발행 | Order DB -> Email 서비스 |
| <strong>DB -> Elasticsearch</strong> | DB 데이터 실시간 검색 인덱싱 | MySQL -> ES 전문 검색 |

📢 **섹션 요약 비유**: CDC 파이프라인은 실시간 번역가다. 한국어(MySQL 이벤트)를 즉시 영어(Kafka JSON)로 번역해서 전 세계 독자(DW, 레이크, 캐시)에게 동시에 전달한다. 번역가는 원래 연설자(DB)의 연설을 방해하지 않는다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Debezium 커넥터 설정 예시 (MySQL)

```json
{
  "name": "mysql-orders-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql-prod.example.com",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "secret",
    "database.server.id": "1",
    "database.server.name": "mysql-prod",
    "database.include.list": "ecommerce",
    "table.include.list": "ecommerce.orders,ecommerce.products",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.ecommerce",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
  }
}
```

### MySQL Binlog 설정 (사전 요건)

```sql
-- MySQL 서버 설정 확인
SHOW VARIABLES LIKE 'log_bin';          -- ON 필요
SHOW VARIABLES LIKE 'binlog_format';    -- ROW 필요
SHOW VARIABLES LIKE 'binlog_row_image'; -- FULL 권장

-- Debezium 전용 복제 권한 부여
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE,
      REPLICATION CLIENT ON *.* TO 'debezium'@'%';
```

**실무자 핵심 판단**: CDC 도입 시 "왜 배치 ETL을 CDC로 대체하는가"를 실시간성·DB 부하 감소·삭제 감지 3가지로 논리화하고, Debezium 아키텍처를 Kafka Connect Source/Sink 흐름으로 설명한다.

📢 **섹션 요약 비유**: CDC 설정은 DB에 "도청 장치"를 합법적으로 설치하는 것이다. DB의 자체 로그(Binlog)를 읽는 것이므로 DB 성능에 영향이 없고, 모든 변경 사항을 빠짐없이 실시간으로 캡처한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| <strong>실시간 데이터 신선도</strong> | 배치 T+1일 -> 밀리초 단위 동기화로 전환 |
| **DB 부하 최소화** | 풀스캔 제거, 로그 읽기로 운영 DB 보호 |
| **완전한 변경 이력** | INSERT·UPDATE·DELETE 모두 캡처, 감사 추적 |
| <strong>이벤트 기반 MSA</strong> | DB 변경을 이벤트로 발행해 서비스 간 결합 해소 |
| **캐시 자동 무효화** | DB 변경 즉시 Redis 캐시 자동 업데이트 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong>초기 스냅샷</strong> | 기존 전체 데이터 초기 적재(Initial Snapshot) 시간 소요 |
| <strong>스키마 변경</strong> | ADD COLUMN 등 DDL 변경 처리 복잡 (스키마 레지스트리 필요) |
| <strong>Binlog 설정 권한</strong> | DB 서버 설정 변경 권한 필요 (보안 승인) |
| <strong>로그 보존 정책</strong> | 빠른 처리 필요, 로그 디스크 소진 주의 |
| **운영 복잡성** | Kafka Connect 클러스터 관리, 커넥터 모니터링 |

📢 **섹션 요약 비유**: CDC는 강력하지만, 처음 설치할 때 전체 재고 조사(Initial Snapshot)는 한 번 해야 한다. 이후에는 변경분만 추적하므로 효율적이지만, "CCTV 시스템"을 유지 관리하는 관리자(Kafka Connect 운영)가 항상 필요하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| Debezium | CDC 구현의 사실상 표준 오픈소스 |
| Apache Kafka | CDC 이벤트 전송 메시지 브로커 |
| ETL | CDC로 대체되는 전통 배치 변경 추출 방식 |
| 트랜잭션 로그 | CDC의 핵심 데이터 소스 (Binlog/WAL/Redo Log) |
| 이벤트 소싱 | CDC 이벤트를 시스템 이벤트로 활용하는 패턴 |
| Kafka Connect | Debezium이 동작하는 분산 통합 플랫폼 |
| 스키마 레지스트리 | CDC 이벤트 메시지의 스키마 버전 관리 |

### 👶 어린이를 위한 3줄 비유 설명
1. CDC는 도서관 사서가 책 반납 기록부(트랜잭션 로그)를 보고 "어떤 책이 대출되고 반납됐는지" 실시간으로 확인하는 것이다. 직접 책장을 다 뒤지지 않아도 된다.

### 📈 관련 키워드 및 발전 흐름도

```text
풀 스캔 동기화 (전체 복사, 비효율)
    |
    v
CDC: 변경분만 캡처 (Log-based · Trigger-based)
    +-► Debezium: MySQL/PG WAL -> Kafka 토픽
    +-► Kafka Connect: Source/Sink 커넥터
    |
    v
실시간 ETL · 이벤트 소싱 · CQRS 패턴 연동
```
2. Debezium은 기록부를 읽는 비서다. 사서(DB)가 기록부에 쓰는 것을 지켜보다가, 새 내용이 생기면 즉시 공지 게시판(Kafka)에 붙여준다.
3. 덕분에 다른 도서관들(DW, 레이크, 서비스들)은 게시판만 보면 원본 도서관 상황을 실시간으로 알 수 있어, 일일이 원본 도서관(운영 DB)에 전화하지 않아도 된다.
