---
title: "Lsm Tree Log Structured Merge"
date: "2026-04-05"
tags:
  - "studynote-data-engineering"
weight: 46
---
> **핵심 인사이트**
> 1. LSM(Log-Structured Merge-Tree) 트리는 쓰기 집약적 워크로드에 최적화된 데이터 구조 — 임의 쓰기(Random Write)를 순차 쓰기(Sequential Write)로 변환해 HDD/SSD에서 극적인 쓰기 성능을 달성하며, RocksDB·Cassandra·HBase·LevelDB의 스토리지 엔진으로 사용된다.
> 2. LSM의 핵심 트레이드오프는 쓰기^ vs 읽기v — 컴팩션(Compaction) 과정 없이는 여러 레벨에 데이터가 분산되어 읽기 성능이 저하되며, Bloom Filter가 불필요한 디스크 읽기를 방지하는 핵심 최적화 도구다.
> 3. B-Tree vs LSM: 워크로드 특성에 따른 선택 — 읽기 많은 OLTP(MySQL, PostgreSQL)는 B-Tree, 쓰기 집약적(IoT, 로그, 이벤트 스트림)은 LSM이 적합하며, 현대 NoSQL 대부분이 LSM을 채택한 이유가 여기에 있다.

---

## Ⅰ. LSM 트리 개요

```
쓰기 문제와 LSM 솔루션:

B-Tree (전통 RDBMS):
  임의 쓰기 (Random Write):
  데이터 -> 페이지 탐색 -> 디스크 랜덤 위치 쓰기

  HDD 랜덤 쓰기: ~150 IOPS (매우 느림)
  SSD 랜덤 쓰기: ~10,000 IOPS

LSM 아이디어:
  임의 쓰기 -> 순차 쓰기로 변환

  "모든 쓰기를 메모리에 먼저 모은 후
   순차적으로 디스크에 한번에 기록"

  HDD 순차 쓰기: ~200 MB/s (랜덤 대비 1,000×)
  SSD 순차 쓰기: ~3,000 MB/s

LSM 활용 사례:
  RocksDB: Facebook 개발, 광범위 사용
  LevelDB: Google 개발 (RocksDB 원조)
  Cassandra: SSTable + LSM
  HBase: HDFS 기반 LSM
  InfluxDB: 시계열 DB LSM
  TiKV: TiDB 스토리지 엔진

LSM 장점:
  높은 쓰기 처리량
  순차 쓰기 -> HDD/SSD 친화적
  Write Amplification 낮음 (B-Tree 대비)

LSM 단점:
  읽기 성능 낮음 (여러 레벨 검색)
  Compaction 오버헤드
  Read Amplification
  Space Amplification
```

> 📢 **섹션 요약 비유**: LSM은 메모장 모아서 한번에 파일 정리 — 메모지(쓰기)를 일단 책상(메모리)에 쌓고, 나중에 한번에 서랍(디스크)에 순서대로 정리. 쓰기 속도 폭발적 향상!

---

## Ⅱ. LSM 구조와 동작

```
LSM 트리 구성:

MemTable (메모리):
  인메모리 정렬된 자료구조
  보통 Red-Black Tree 또는 Skip List

  모든 쓰기가 먼저 MemTable에 삽입
  크기 임계값 (예: 64MB) 도달 시 플러시

  WAL (Write-Ahead Log):
  장애 복구를 위해 디스크에도 순차 로그
  MemTable 소실 시 WAL로 복구

SSTable (Sorted String Table):
  MemTable이 플러시될 때 생성
  불변(Immutable): 한번 쓰면 수정 불가
  정렬된 키-값 파일

  Level 0 (L0):
  MemTable -> L0 SSTable (최신 데이터)
  L0 파일 수 임계값 -> L1으로 Compaction

  Level 1 (L1):
  키 범위가 겹치지 않도록 정렬

  Level N (Ln):
  각 레벨: 이전 레벨 × 10배 크기
  L0: 수MB
  L1: 10MB
  L2: 100MB
  L3: 1GB
  ...

쓰기 과정:
  1. WAL에 순차 쓰기 (내구성)
  2. MemTable에 삽입
  3. MemTable 가득 차면 L0에 플러시
  4. L0 가득 차면 L1으로 Compaction

읽기 과정:
  1. MemTable 검색 (최신)
  2. L0 SSTable 검색 (최신순)
  3. L1 -> L2 -> ... 검색
  -> 최악: 모든 레벨 검색 (느림)
  -> Bloom Filter로 불필요한 탐색 건너뜀
```

> 📢 **섹션 요약 비유**: LSM 구조는 서류 정리 시스템 — 새 서류(쓰기)는 책상 메모장(MemTable)에 먼저. 가득 차면 파일럿(L0 SSTable)으로 이동, 주기적으로 캐비닛(더 깊은 레벨)으로 정리!

---

## Ⅲ. Compaction과 Bloom Filter

```
Compaction (컴팩션):

역할: LSM의 핵심 백그라운드 프로세스
     여러 SSTable을 합쳐 정렬된 파일 생성

왜 필요한가:
  LSM 쓰기: 항상 새 SSTable 추가
  같은 키가 여러 파일에 존재 가능
  -> 읽기 시 여러 파일 검색
  -> 오래된 데이터(tombstone) 공간 낭비

Compaction 유형:

Size-Tiered Compaction (크기 기반):
  비슷한 크기의 SSTable 여러 개 -> 하나로 합침

  장점: Compaction 적게 발생
  단점: 임시 공간 많이 필요 (1.5~2× 데이터)
  사용: Cassandra 기본

Level Compaction (레벨 기반):
  LevelDB/RocksDB 방식
  L0 -> L1으로, L1 -> L2로 단계적 합침

  각 레벨은 겹치지 않는 키 범위
  읽기: 각 레벨에서 1개 SSTable만 확인

  장점: 읽기 성능 좋음, 공간 효율적
  단점: Compaction 자주 발생 (쓰기 증폭)

Bloom Filter (블룸 필터):
  "이 키가 이 SSTable에 없을 가능성 99.9%"를 O(1)에 판단

  확률적 자료구조 (False Positive 있지만 False Negative 없음)

  읽기 최적화:
  블룸 필터: "이 SSTable에 없음" -> 건너뜀
  불필요한 디스크 I/O 90%+ 절감

Write Amplification:
  실제 쓰기 / 논리적 쓰기
  LSM Level Compaction: ~10×
  B-Tree: ~3~5× (낮음)
  -> Compaction으로 인한 추가 쓰기
```

> 📢 **섹션 요약 비유**: Compaction은 책 정리, Bloom Filter는 인덱스 — 정기적으로 흩어진 책(SSTable)을 합쳐 정리(Compaction). 목차(Bloom Filter)로 "이 책에 없다"고 빠르게 판단!

---

## Ⅳ. B-Tree vs LSM 비교

```
B-Tree vs LSM 비교:

B-Tree:
  구조: 균형 트리, 인플레이스 업데이트
  쓰기: 임의 쓰기 (페이지 탐색 후 수정)
  읽기: 빠름 (트리 경로 = O(log n))
  공간: 페이지 낭비 있음 (~30%)

  Write Amp: 낮음 (데이터 한번에 쓰기)
  Read Amp: 낮음
  Space Amp: 중간

  최적: 읽기 많은 OLTP

LSM:
  구조: 순차 쓰기, 계층적 파일
  쓰기: 순차 쓰기 (10~1,000× 빠름)
  읽기: 느림 (여러 파일 검색)
  공간: 임시 Compaction 공간 필요

  Write Amp: 높음 (Compaction 추가 쓰기)
  Read Amp: 높음 (여러 레벨 검색)
  Space Amp: 높음 (중복 데이터)

  최적: 쓰기 집약적 워크로드

RUM Conjecture:
  Read / Update / Memory 트레이드오프

  R(읽기 오버헤드) × U(쓰기 오버헤드) × M(공간 오버헤드)
  -> 셋 중 둘을 최소화하면 하나는 증가

선택 가이드:
  IoT 센서 데이터 수집: LSM (쓰기 우선)
  온라인 쇼핑 주문: B-Tree (읽기 빠름)
  시계열 DB (InfluxDB, Prometheus): LSM
  관계형 OLTP (MySQL): B-Tree
  로그 저장 (Kafka->Cassandra): LSM
```

> 📢 **섹션 요약 비유**: B-Tree vs LSM은 창고 정리법 — B-Tree: 물건 제자리 즉시 정리(느린 쓰기, 빠른 찾기). LSM: 일단 입구에 쌓고 나중에 한번에 정리(빠른 쓰기, 느린 찾기)!

---

## Ⅴ. 실무 시나리오 — RocksDB IoT 데이터 수집

```
스마트 공장 IoT 데이터 저장 (RocksDB + LSM):

요구사항:
  센서: 10,000개
  측정 주기: 1초
  데이터: 초당 10,000 쓰기
  보존 기간: 2년
  조회: 특정 센서의 최근 1시간 데이터

RocksDB 설정:
  MemTable 크기: 128MB
  L0 파일 수 트리거: 4
  L1 최대 크기: 256MB
  레벨 배율: 10×

  Bloom Filter: 활성화 (False Positive = 1%)
  Compaction: Level Compaction

  블록 캐시: 1GB (자주 조회 데이터)

성능 결과:
  쓰기 처리량: 초당 200,000 이상
  (10,000 IoT 포인트 × 20 여유)

  P99 쓰기 지연: < 1ms
  P99 읽기 지연: < 5ms (Bloom Filter 덕분)

  비교: MySQL InnoDB (B-Tree)
  동일 쓰기 워크로드:
  -> 쓰기 처리량: 초당 30,000
  -> P99 쓰기 지연: 10~50ms
  -> 디스크 IOPS 포화 현상

Compaction 관리:
  TTL Compaction: 2년 지난 데이터 자동 삭제

  Compaction 백그라운드:
  쓰기 집중 시간 회피 (일과 후 집중)
  Rate Limiter: 초당 100MB 제한
  (프로덕션 영향 최소화)

확장:
  Kafka -> Flink -> RocksDB 파이프라인
  RocksDB Replication: Leader-Follower
  스냅샷 백업: S3로 주기적 백업

  2년 데이터: 약 2TB
  S3 Glacier 아카이브: 연 20만원
```

> 📢 **섹션 요약 비유**: RocksDB IoT 수집은 고속 우체통 — 10,000개 센서가 매초 편지(데이터)를 넣어요. LSM은 편지를 먼저 트레이(MemTable)에 쌓고 한번에 정리. MySQL 대비 7배 빠른 쓰기!

---

## 📌 관련 개념 맵

```
LSM 트리 (Log-Structured Merge-Tree)
+-- 구성 요소
|   +-- MemTable (인메모리)
|   +-- SSTable (불변 파일)
|   +-- WAL (장애 복구)
+-- 핵심 프로세스
|   +-- Flush (MemTable -> SSTable)
|   +-- Compaction (SSTable 합병)
+-- 최적화
|   +-- Bloom Filter (읽기 최적화)
|   +-- Block Cache
+-- 대표 구현체
    +-- RocksDB (Facebook)
    +-- LevelDB (Google)
    +-- Cassandra (SSTable)
    +-- HBase
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[B-Tree 한계 인식 (1990s)]
HDD 랜덤 I/O 병목
로그 파일 개념 등장
      |
      v
[LSM 제안 (1996)]
Patrick O'Neil 등
Log-Structured Merge-Tree 논문
      |
      v
[LevelDB (2011)]
Google Jeff Dean 팀
오픈소스 LSM 구현체
      |
      v
[RocksDB (2012)]
Facebook이 LevelDB 포크
멀티 스레드 Compaction
      |
      v
[NoSQL 표준 스토리지 (2015~)]
Cassandra, TiKV 등 채택
모바일(SQLite 대안), 임베디드 DB
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. LSM은 빠른 우체통 — 편지(쓰기)를 먼저 입구 트레이(MemTable)에 쌓고, 나중에 한번에 정리. 줄 서기(랜덤 쓰기) 없이 빠르게 넣어요!
2. Compaction은 대청소 — 흩어진 서류(SSTable)를 주기적으로 합쳐서 정리. 안 하면 같은 파일이 곳곳에 분산돼 찾기 힘들어요!
3. Bloom Filter는 빠른 목차 — "이 파일에 없어요"를 1초 만에 판단. 없는 데이터 찾으러 30개 파일 다 열지 않아도 돼요!
