---
title: "Compaction And Tombstone"
date: "2026-04-05"
tags:
  - "studynote-data-engineering"
weight: 47
---
> **핵심 인사이트**
> 1. 컴팩션(Compaction)은 LSM 트리 기반 DB에서 여러 SSTable을 합쳐 중복 제거와 공간 효율화를 수행하는 백그라운드 프로세스 — Cassandra·RocksDB·HBase에서 지속적으로 발생하며, 쓰기 증폭(Write Amplification)과 공간 효율 사이의 트레이드오프를 관리한다.
> 2. 툼스톤(Tombstone)은 LSM 기반 DB에서 데이터 삭제를 표시하는 특수 마커 — 실제 즉각 삭제 대신 삭제 표시(Tombstone)를 쓰고, 이후 컴팩션 시 실제 삭제가 이루어지며, 툼스톤 축적이 읽기 성능을 저하시키는 "툼스톤 문제"가 중요한 운영 과제다.
> 3. 컴팩션 전략 선택이 워크로드 성능에 결정적 영향 — Cassandra의 STCS(크기 기반)·TWCS(시계열)·LCS(레벨 기반) 중 잘못된 전략 선택은 5~10배 이상의 성능 차이를 낳으며, 워크로드 분석이 컴팩션 전략 선택의 전제다.

---

## Ⅰ. 컴팩션 개요

```
컴팩션 필요성:

LSM 쓰기 특성:
  MemTable -> 플러시 -> SSTable 생성
  같은 키의 새 값 -> 새 SSTable에 저장
  (기존 SSTable 수정 X, 불변)

  결과:
  키 K1의 버전 1: SSTable A에
  키 K1의 버전 2: SSTable B에
  키 K1의 버전 3: SSTable C에

  읽기 시: SSTable A, B, C 모두 확인 필요
  -> 읽기 오버헤드 증가

컴팩션 역할:
  SSTable A + B + C -> SSTable D (합병)
  키 K1: 버전 3만 남김 (버전 1, 2 제거)

  효과:
  1. 읽기 성능 향상 (확인할 파일 수 감소)
  2. 공간 효율화 (중복 제거)
  3. 툼스톤 실제 삭제

컴팩션 비용:
  CPU: 파일 병합, 정렬
  I/O: 대용량 파일 읽기 + 쓰기
  임시 공간: 원본 + 결과물 동시 보유

  -> 컴팩션 집중 시 프로덕션 성능 영향
  -> Rate Limiter로 속도 제한 필요

Write Amplification:
  논리적 쓰기 1MB -> 실제 디스크 쓰기 10MB?
  WA = 실제 쓰기 / 논리 쓰기

  높은 WA: 컴팩션 오버헤드 큰 전략
  SSD 수명 영향: 쓰기 횟수 제한
```

> 📢 **섹션 요약 비유**: 컴팩션은 주기적 대청소 — 빨리 넣어둔 물건(새 SSTable)들이 쌓이면 정리 정돈. 같은 물건(같은 키) 최신 것만 남기고 나머지 버리기!

---

## Ⅱ. 툼스톤 메커니즘

```
툼스톤 (Tombstone):

문제: LSM에서 즉각 삭제 불가
  SSTable은 불변(Immutable)
  -> 기존 SSTable의 특정 키 삭제 불가

해결: 삭제 마커(Tombstone) 쓰기
  DELETE FROM users WHERE id = 1
  -> MemTable에 Tombstone(id=1) 쓰기
  -> SSTable로 플러시

  실제 삭제는 컴팩션 시:
  Tombstone과 원본 데이터 같이 있으면 -> 제거

  읽기 시 Tombstone 처리:
  id=1 데이터 찾기
  SSTable에서 id=1 Tombstone 발견
  -> "삭제됨"으로 처리, 반환 안 함

Tombstone 유형 (Cassandra):

Cell Tombstone: 단일 셀 삭제
Row Tombstone: 전체 행 삭제
Range Tombstone: 범위 삭제 (CLUSTERING 컬럼)
TTL Tombstone: TTL 만료 시 자동 생성

Tombstone 문제 (Tombstone Hell):

시나리오:
  DELETE 집중 워크로드
  또는 TTL 많은 데이터 (IoT, 로그)

  컴팩션 늦으면:
  Tombstone 수백만 개 축적

  읽기 시:
  데이터 1개 찾는데 Tombstone 100만개 확인

  카산드라 tomb_failure_threshold:
  기본 100,000개 -> 초과 시 경고/오류

GC Grace Period:
  Tombstone이 실제 삭제되기까지 대기 시간
  Cassandra 기본: 10일 (864,000초)

  이유: 복제 노드가 Tombstone 전파 보장
  만약 3일 후 오프라인 노드 복귀:
  GC Grace 10일 이내 -> Tombstone 전파 OK

  단, 10일 동안 Tombstone 축적됨
```

> 📢 **섹션 요약 비유**: 툼스톤은 묘비 — 책(SSTable)에서 페이지를 직접 찢을 수 없어서 "이 페이지는 삭제됨" 스티커(Tombstone)를 붙여요. 나중에 책 재인쇄(컴팩션)할 때 진짜 제거!

---

## Ⅲ. Cassandra 컴팩션 전략

```
Cassandra 컴팩션 전략:

1. STCS (Size-Tiered Compaction Strategy):
  기본 전략

  동작: 비슷한 크기의 SSTable N개 -> 하나로 합침

  예:
  4개의 50MB SSTable -> 200MB SSTable
  4개의 200MB SSTable -> 800MB SSTable

  장점:
  쓰기 최적화 (Write-Heavy 적합)
  컴팩션 빈도 낮음

  단점:
  읽기 시 여러 파일 확인
  공간 사용 증가 (임시 공간 필요)
  Tombstone 오래 축적

  적합: 쓰기 집중, 데이터 변경 적음

2. LCS (Leveled Compaction Strategy):
  각 레벨에서 키 범위 비중첩 보장

  L0: 새 SSTable들
  L1: 최대 크기 제한 (예: 160MB)
  L2: L1 × 10 (1600MB)
  ...

  장점:
  읽기 최적화 (각 레벨 1개 파일만 확인)
  공간 효율적
  Tombstone 빠른 제거

  단점:
  쓰기 증폭 높음 (더 많은 컴팩션)
  쓰기 집중 워크로드에 I/O 과부하

  적합: 읽기 집중, 업데이트 많음

3. TWCS (Time Window Compaction Strategy):
  시계열 데이터 특화

  동작: 시간 윈도우(예: 1일)로 SSTable 분류
  같은 시간 윈도우 내 SSTable만 합침

  장점:
  오래된 데이터(변경 없음) = 컴팩션 안 함
  TTL 데이터 효율적 삭제

  단점:
  시계열 외 워크로드에 비효율

  적합: 시계열 IoT, 로그, 이벤트 데이터
```

> 📢 **섹션 요약 비유**: 컴팩션 전략 선택 — STCS(서류 크기별 정리: 쓰기 빠름), LCS(알파벳순 정리: 읽기 빠름), TWCS(날짜별 정리: 시계열 최적). 업무 유형에 맞는 정리법!

---

## Ⅳ. 운영 모니터링

```
컴팩션 모니터링 핵심 지표:

Cassandra 주요 메트릭:

1. PendingCompactions:
  현재 대기 중인 컴팩션 수
  정상: < 100
  위험: > 1000 (컴팩션 쌓임 = 읽기 저하)

2. TotalDiskSpaceUsed:
  데이터 디스크 사용량 추적
  급격히 증가 = Tombstone 축적 또는 컴팩션 미실행

3. LiveSSTableCount:
  테이블당 SSTable 수
  STCS: < 20 정상
  많을수록 읽기 오버헤드

4. TombstoneScannedHistogram:
  읽기 당 스캔한 Tombstone 수
  높으면 Tombstone 문제

5. CompactionBytesWrittenPerSec:
  컴팩션 I/O
  너무 높으면 프로덕션 영향

Tombstone 문제 해결:

진단:
  nodetool compactionstats
  -> 대기 컴팩션 확인

  nodetool tablestats <keyspace>.<table>
  -> LiveSSTableCount, TombstoneScannedHistogram

해결:
  1. 강제 컴팩션:
  nodetool compact <keyspace> <table>
  -> 즉시 컴팩션 실행 (IO 집중!)

  2. GC Grace 조정:
  ALTER TABLE ... WITH gc_grace_seconds = 86400;
  (10일 -> 1일)
  데이터 손실 위험 검토 후 적용

  3. TWCS 전환:
  시계열 데이터 -> TWCS로 전략 변경

RocksDB 모니터링:
  db.GetProperty("rocksdb.stats") -> 전체 통계
  db.GetProperty("rocksdb.compaction-pending") -> 대기 수
```

> 📢 **섹션 요약 비유**: 컴팩션 모니터링은 청소 상태 점검 — 청소 대기 목록(PendingCompactions) 너무 많으면? 방(DB)이 지저분해서 물건(데이터) 찾기 어려움. 즉시 청소(강제 컴팩션)!

---

## Ⅴ. 실무 시나리오 — IoT 시계열 Cassandra 최적화

```
IoT 플랫폼 Cassandra 컴팩션 최적화:

현황:
  센서 10,000개, 데이터 보존 90일
  TTL 설정: 90일 (7,776,000초)
  기본 STCS 전략 사용

  문제:
  읽기 지연 급증: P99 5초 (목표 1초)
  디스크 사용량 계속 증가

  진단:
  nodetool tablestats -> TombstoneScannedHistogram: 평균 500,000!
  LiveSSTableCount: 350개 (매우 많음)

  원인:
  TTL 만료 -> Tombstone 대량 생성
  STCS: Tombstone 포함 SSTable이 쌓임
  컴팩션이 Tombstone 제거 못 따라감

최적화:

1. TWCS 전략 전환:
  ALTER TABLE sensor_data
  WITH compaction = {'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': '1'};

  효과: 오래된(TTL 만료) 시간 윈도우 자동 정리
  Tombstone 축적 90% 감소

2. GC Grace 단축:
  단일 DC, 실시간 데이터:
  ALTER TABLE sensor_data WITH gc_grace_seconds = 86400; (1일)

  주의: 2개 이상 DC면 단축 위험 있음

3. 불필요 DELETE 제거:
  TTL로 자동 만료 -> 명시적 DELETE 불필요
  비즈니스 로직 DELETE만 유지

결과:
  P99 읽기: 5초 -> 0.8초
  TombstoneScannedHistogram: 500,000 -> 2,000
  LiveSSTableCount: 350 -> 12 (시간 윈도우 수)
  디스크: 정상 범위 유지

운영 교훈:
  IoT 시계열 + TTL 많으면 TWCS 필수
  STCS + TTL + Tombstone = 읽기 재앙
  초기 설계부터 컴팩션 전략 고려
```

> 📢 **섹션 요약 비유**: IoT Cassandra 최적화 — STCS(서류 크기별 정리)로 TTL 만료 묘비(Tombstone) 쌓여 읽기 5초. TWCS(날짜별 정리)로 전환하니 만료 파일 자동 정리, 읽기 0.8초. 전략 선택이 결정적!

---

## 📌 관련 개념 맵

```
컴팩션 & 툼스톤
+-- 컴팩션 전략 (Cassandra)
|   +-- STCS (쓰기 최적, 기본)
|   +-- LCS (읽기 최적)
|   +-- TWCS (시계열 최적)
+-- 툼스톤
|   +-- 삭제 마커
|   +-- GC Grace Period
|   +-- Tombstone 문제
+-- 관련 개념
|   +-- LSM 트리
|   +-- SSTable (불변 파일)
|   +-- Write Amplification
+-- 모니터링
    +-- PendingCompactions
    +-- TombstoneScannedHistogram
    +-- LiveSSTableCount
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[LSM 트리 제안 (1996)]
Patrick O'Neil 등
컴팩션 개념 포함
      |
      v
[LevelDB (2011)]
Google 구현
Level Compaction
      |
      v
[Cassandra 컴팩션 발전 (2012~)]
STCS -> LCS -> TWCS
IoT/시계열 워크로드 최적화
      |
      v
[RocksDB 전략 다양화 (2013~)]
Universal, FIFO, Level
티어드 스토리지 통합
      |
      v
[현재: 자동 컴팩션 최적화]
머신러닝 기반 전략 선택
클라우드 관리형 서비스
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 컴팩션은 대청소 — LSM은 쓸 때마다 새 노트(SSTable) 생성. 컴팩션이 주기적으로 노트를 합치고 최신 내용만 남겨요!
2. 툼스톤은 삭제 스티커 — 책(SSTable)에서 페이지 직접 못 찢어요. "삭제됨" 스티커(Tombstone)를 붙이고, 책 재인쇄(컴팩션)할 때 진짜 제거!
3. TWCS는 날짜별 정리 — IoT 데이터는 날짜별로 정리하면 만료된 날짜 묶음을 통째로 버릴 수 있어요. 묘비 쌓임 없이 깔끔!
