---
title: "Wide Column Store"
date: "2026-03-03"
tags:
  - "studynote-data-engineering"
weight: 38
---
> **핵심 인사이트**
> 1. 와이드 컬럼 저장소(Wide Column Store)는 행 키(Row Key)로 데이터를 분산 저장하되, 각 행이 서로 다른 컬럼 집합을 가질 수 있는 스파스 매트릭스 구조로, 스키마가 행마다 다를 수 있는 반정형 대용량 데이터에 최적화되어 있다.
> 2. 파티션 키(Partition Key) 설계가 Cassandra/HBase 성능의 90%를 결정 — 파티션 키가 핫스팟(Hot Spot)을 만들거나 너무 세밀하면 분산 효과가 사라지며, "쿼리 중심 데이터 모델링(Query-Driven Modeling)"이 관계형 DB의 정규화와 완전히 다른 설계 철학이다.
> 3. Cassandra는 AP 시스템(가용성 우선, CAP 정리), HBase는 CP 시스템(일관성 우선) — 같은 와이드 컬럼이지만 일관성 모델이 다르므로 유스케이스를 구분하여 선택해야 한다.

---

## I. 와이드 컬럼 구조

```
관계형 DB (Row-Oriented):
  Row:  id | name   | email          | age
  Row1:  1 | Alice  | a@example.com  |  30
  Row2:  2 | Bob    | b@example.com  | NULL

  -> 모든 행이 동일한 컬럼 구조

와이드 컬럼 (Column Family):
  Row Key: user:001
    personal: {name: Alice, age: 30}
    contact:  {email: a@example.com, phone: 010-...}

  Row Key: user:002
    personal: {name: Bob}
    social:   {twitter: @bob, github: bob-dev}
    (contact 컬럼 패밀리 없음 -> 스파스)

특징:
  - 행마다 다른 컬럼 가능 (스파스 매트릭스)
  - 컬럼 패밀리 단위로 물리 저장
  - 컬럼 타임스탬프 내장 (버전 관리)
```

> 📢 **섹션 요약 비유**: 엑셀에서 모든 행에 같은 열을 채우는 대신, 각 학생이 자신에게 필요한 과목 열만 가지는 성적표 — 없는 과목은 칸 자체가 없음.

---

## II. Apache Cassandra

```
Cassandra (Facebook 개발, Apache 오픈소스):

데이터 모델:
  Keyspace -> Table -> Row -> Column

파티션 키 (Partition Key):
  데이터가 저장될 노드를 결정
  일관된 해싱(Consistent Hashing)으로 분산

클러스터링 컬럼 (Clustering Column):
  파티션 내 데이터 정렬 기준

예시 테이블:
  CREATE TABLE sensor_data (
    device_id TEXT,         -- 파티션 키
    timestamp TIMESTAMP,    -- 클러스터링 컬럼
    temperature FLOAT,
    humidity FLOAT,
    PRIMARY KEY (device_id, timestamp)
  );

특성:
  쓰기: 매우 빠름 (순차 LSM-Tree)
  읽기: 파티션 키로 조회 시 빠름
  일관성: 튜너블 (ONE/QUORUM/ALL)
  CAP: AP (가용성 + 파티션 허용)
```

> 📢 **섹션 요약 비유**: Cassandra는 배달 기사들이 지역별로 나뉘어(파티션) 각자 담당 지역 배달 — 지역 내 빠른 배달, 전체 재고 파악은 느림.

---

## III. Apache HBase

```
HBase (Google BigTable 아키텍처, Hadoop 기반):

구조:
  HMaster (마스터) + RegionServer (워커)
  HDFS 위에서 실행 (영속성)

Row Key가 사전순 정렬:
  시계열 데이터: 타임스탬프를 reverse로
  user:20241201 -> user:20241130 정렬

컬럼 패밀리 (Column Family):
  물리적으로 같은 파일에 저장
  패밀리 내 컬럼은 동적으로 추가 가능

특성:
  CAP: CP (일관성 + 파티션 허용)
  HDFS 기반 -> Hadoop 생태계 통합
  Spark, Hive와 연동

Cassandra vs HBase:
  Cassandra: 마스터리스, AP, 낮은 지연
  HBase: 마스터 기반, CP, Hadoop 통합
```

| 특성     | Cassandra     | HBase         |
|--------|--------------|--------------|
| CAP    | AP           | CP           |
| 마스터   | 마스터리스       | HMaster       |
| Hadoop | 독립          | 필수 (HDFS)    |
| 지연    | 낮음 (ms)     | 중간 (ms~초)   |

> 📢 **섹션 요약 비유**: Cassandra는 여러 창고에 분산 보관(가용성 우선), HBase는 중앙 창고 관리자가 있어 정확한 재고 파악(일관성 우선).

---

## IV. 쿼리 중심 모델링

```
관계형 DB vs 와이드 컬럼 설계 철학:

관계형:
  "데이터를 어떻게 저장할까?" (정규화)
  -> 나중에 어떤 쿼리든 JOIN으로 해결

와이드 컬럼:
  "어떤 쿼리를 할 것인가?" (비정규화)
  -> 쿼리 패턴에 맞게 테이블을 설계
  -> JOIN 없음 (단일 테이블 조회 원칙)

예시: 사용자의 최근 주문 조회
  관계형: users JOIN orders WHERE user_id = ?
  Cassandra:
    orders_by_user 테이블 별도 생성
    PRIMARY KEY (user_id, order_timestamp)
    -> 단일 테이블 조회로 해결

비정규화 trade-off:
  중복 저장 증가 (디스크)
  대신 빠른 읽기, 분산 용이
```

> 📢 **섹션 요약 비유**: 관계형은 서류를 원본 하나만 보관(정규화), Cassandra는 자주 쓰는 서류를 각 팀에 복사본 비치(비정규화) — 찾기 빠른 대신 저장 공간 더 씀.

---

## V. 실무 시나리오 — IoT 센서 시계열

```
시나리오:
  IoT 플랫폼: 100만 개 센서
  각 센서: 1초마다 온도/습도 전송
  초당 100만 건 쓰기

Cassandra 설계:

  파티션 키: (device_id, date)
    예: ("sensor-001", "2025-03-03")
    이유: 하루치 데이터를 한 파티션에
    (device_id만 쓰면 파티션 무제한 성장)

  클러스터링 컬럼: timestamp DESC
    최신 데이터 먼저 정렬

  쿼리 패턴:
    최근 1시간 데이터 조회:
    SELECT * FROM sensor_data
    WHERE device_id = 'sensor-001'
    AND date = '2025-03-03'
    AND timestamp > 1h_ago
    -> 단일 파티션 조회 -> 빠름!

성능:
  쓰기: 초당 100만 건 (10노드 클러스터)
  읽기: 10ms 이내 (파티션 키 조회)
  가용성: 99.99% (RF=3, QUORUM)
```

> 📢 **섹션 요약 비유**: 파티션 키를 date 포함해서 자동 데이터 만료(TTL)처럼 관리 — 특정 날짜 파티션 전체를 일괄 삭제도 가능.

---

## 📌 관련 개념 맵

```
와이드 컬럼 저장소
+-- 구조
|   +-- 스파스 매트릭스 (행마다 다른 컬럼)
|   +-- 컬럼 패밀리, 타임스탬프
+-- 대표 DB
|   +-- Apache Cassandra (AP, 마스터리스)
|   +-- Apache HBase (CP, Hadoop 기반)
+-- 설계 원칙
|   +-- 쿼리 중심 모델링
|   +-- 파티션 키 핫스팟 방지
+-- 응용
    +-- IoT 시계열, 로그, SNS 피드
    +-- 시간 범위 쿼리, 대규모 쓰기
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Google BigTable (2004)]
컬럼 패밀리 개념 정립
      |
      v
[HBase (2007, Apache)]
Hadoop 기반 BigTable 오픈소스 구현
      |
      v
[Apache Cassandra (2008, Facebook)]
마스터리스 분산, P2P 토폴로지
      |
      v
[Cassandra Query Language (CQL, 2012)]
SQL 유사 문법으로 접근성 향상
      |
      v
[현재: 특수 목적 경쟁]
시계열 전용: InfluxDB, TimescaleDB
벡터 DB: Cassandra 5.0 벡터 지원
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 와이드 컬럼 저장소는 학생마다 다른 과목을 가질 수 있는 성적표처럼, 행마다 서로 다른 컬럼을 가질 수 있는 유연한 데이터 저장 방식이에요.
2. Cassandra는 창고를 여러 곳에 분산해 항상 이용 가능하게 하고(AP), HBase는 중앙 창고 관리자가 정확한 재고를 보장해요(CP).
3. IoT 기기 100만 대가 매초 데이터를 보내는 시스템에 Cassandra가 딱 맞는 이유는, 파티션 키로 데이터를 균등하게 분산해 초당 100만 건 쓰기를 처리할 수 있기 때문이에요!
