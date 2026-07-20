---
title: "Storage Engine Innodb Myisam"
date: "2026-04-05"
tags:
  - "studynote-database"
weight: 49
---
> **핵심 인사이트**
> 1. InnoDB와 MyISAM의 핵심 차이는 "트랜잭션 + 외래키 지원 여부" — InnoDB는 ACID 트랜잭션·외래키·행 단위 잠금을 지원하는 반면, MyISAM은 이 모두를 지원하지 않는 대신 단순한 구조로 읽기 전용 환경에서 빠른 성능을 보인다.
> 2. InnoDB의 클러스터드 인덱스(Clustered Index)가 핵심 설계 원리 — InnoDB는 PK를 기준으로 데이터를 B+ 트리에 정렬 저장(클러스터드)하여 PK 기반 조회가 매우 빠르지만, MyISAM은 데이터 파일과 인덱스 파일을 분리해 더 유연하다.
> 3. MySQL 5.5 이후 InnoDB가 기본 엔진으로 설정되었으나, 특수 목적(전문 검색·지리 데이터·로그 테이블)에는 MyISAM 또는 Aria·Memory·CSV·Blackhole 등 다른 엔진이 여전히 선택된다.

---

## Ⅰ. 스토리지 엔진 개요

```
스토리지 엔진 (Storage Engine):
  MySQL/MariaDB의 데이터 저장·검색 담당 컴포넌트
  테이블 단위로 엔진 선택 가능

MySQL 아키텍처:
  클라이언트
      v
  SQL 파서 / 옵티마이저 (공통)
      v
  스토리지 엔진 API (공통 인터페이스)
      v
  InnoDB | MyISAM | Memory | CSV | ...

주요 스토리지 엔진:
  InnoDB: 기본값, OLTP 범용
  MyISAM: 레거시, 읽기 전용
  Memory (Heap): 메모리 테이블, 임시
  CSV: CSV 파일 연동
  Blackhole: 데이터 버림 (로그 중계)
  Archive: 압축 저장, 대용량 로그
  Spider: 분산 DB 파티셔닝
  TokuDB/RocksDB: 고압축 + 쓰기 최적화

테이블별 엔진 지정:
  CREATE TABLE orders (
      id INT PRIMARY KEY,
      ...
  ) ENGINE=InnoDB;

  CREATE TABLE access_log (
      ...
  ) ENGINE=MyISAM;
```

> 📢 **섹션 요약 비유**: 스토리지 엔진 = 창고 관리 방식 — MySQL은 SQL 접수 데스크(파서/옵티마이저). 실제 창고 운영은 엔진마다 다름. InnoDB(정확한 ACID 창고), MyISAM(빠른 읽기 전용 창고)!

---

## Ⅱ. InnoDB

```
InnoDB 핵심 특성:

1. ACID 트랜잭션:
  BEGIN / COMMIT / ROLLBACK 지원
  애플리케이션 오류 시 자동 롤백

  BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  COMMIT;  -- 둘 다 성공 또는 둘 다 실패

2. 외래 키 (Foreign Key):
  참조 무결성 강제
  CASCADE, SET NULL, RESTRICT 옵션

3. 행 단위 잠금 (Row-Level Locking):
  UPDATE 시 해당 행만 잠금
  동시성 높음 (MyISAM: 테이블 전체 잠금)

4. MVCC (Multi-Version Concurrency Control):
  읽기-쓰기 동시성 향상
  트랜잭션별 스냅샷 제공
  -> 읽기가 쓰기를 블로킹하지 않음

5. 클러스터드 인덱스 (Clustered Index):
  PK 순서로 데이터 물리 저장

  구조:
  PK B+ 트리: 리프 노드에 실제 데이터
  세컨더리 인덱스: PK 값을 포인터로 사용

  장점: PK 범위 검색 고속
  단점: 무작위 PK(UUID) 삽입 시 페이지 분할

6. 버퍼 풀 (Buffer Pool):
  디스크 페이지를 메모리에 캐시
  innodb_buffer_pool_size: 메모리 70~80% 권장

  LRU 알고리즘으로 관리
```

> 📢 **섹션 요약 비유**: InnoDB = 은행 창고 — 거래 장부(트랜잭션), 담보 연결(외래키), 개인 금고(행 잠금), 스냅샷 열람(MVCC). 안전하고 정확하지만 체계가 복잡!

---

## Ⅲ. MyISAM

```
MyISAM 핵심 특성:

구조 (3파일):
  tablename.frm: 테이블 정의
  tablename.MYD: 실제 데이터 (MYData)
  tablename.MYI: 인덱스 (MYIndex)

특성:

1. 트랜잭션 없음:
  COMMIT/ROLLBACK 미지원
  중간 오류 시 부분 적용 상태 유지
  (크래시 후 수동 repair 필요)

2. 테이블 단위 잠금:
  INSERT/UPDATE/DELETE 시 테이블 전체 잠금
  -> 쓰기 중 읽기 불가 (반대도 가능)
  -> 동시 쓰기 성능 낮음

3. 비클러스터드 인덱스:
  인덱스 파일(MYI)과 데이터 파일(MYD) 분리
  인덱스 -> 데이터 파일 포인터

  장점: 유연한 인덱스 관리

4. 전문 검색 (Full-Text Search):
  FULLTEXT 인덱스 (MyISAM 전통 강점)
  (InnoDB도 5.6부터 지원)

5. 빠른 COUNT(*):
  테이블 전체 행 수를 메타데이터에 저장
  SELECT COUNT(*): O(1) (InnoDB: O(N) 스캔)

6. 키 캐시 (Key Cache):
  인덱스 블록만 캐시 (데이터는 OS 캐시)
  key_buffer_size 설정

적합 사용 사례:
  읽기 전용 테이블 (참고 데이터)
  로그 테이블 (쓰기만, 트랜잭션 불필요)
  전문 검색 (레거시 시스템)
```

> 📢 **섹션 요약 비유**: MyISAM = 도서관 창고 — 책(데이터)과 카드 목록(인덱스) 분리. 빠른 책 찾기(읽기). 하지만 책 수정 중엔 도서관 전체 입장 금지(테이블 잠금). 트랜잭션 없음!

---

## Ⅳ. 상세 비교

```
InnoDB vs MyISAM 비교:

항목               InnoDB          MyISAM
트랜잭션           지원 (ACID)     미지원
외래 키            지원            미지원
잠금 단위          행 (Row)        테이블
MVCC               지원            미지원
클러스터드 인덱스  O (PK 기준)     X (별도 파일)
COUNT(*)           O(N) 스캔       O(1) 메타
풀텍스트 검색      5.6부터 지원    전통 지원
크래시 복구        자동 (Redo Log) 수동 (myisamchk)
저장 파일          .ibd (단일)     .frm+.MYD+.MYI
외부 키            지원            미지원
Buffer Pool        지원            Key Cache만
적합 워크로드      OLTP, 일반      읽기 전용, 레거시

MySQL 버전별 기본 엔진:
  MySQL 5.1 이하: MyISAM
  MySQL 5.5+: InnoDB (기본값 변경)

성능 비교:
  읽기 전용(단순 SELECT): MyISAM ≥ InnoDB
  OLTP(혼합 읽기/쓰기): InnoDB >>>
  COUNT(*): MyISAM >> InnoDB (대규모)
  동시 쓰기: InnoDB >> MyISAM (행 잠금)

언제 MyISAM?
  레거시 코드 유지
  읽기 전용 참조 테이블
  MyISAM 전용 기능 (압축 테이블 등)
```

> 📢 **섹션 요약 비유**: InnoDB vs MyISAM = 스마트폰 vs 피처폰 — 스마트폰(InnoDB): 다기능, 안전, 동시 작업. 피처폰(MyISAM): 단순, 읽기 빠름, 구형 기기 호환. 새 프로젝트는 무조건 InnoDB!

---

## Ⅴ. 실무 시나리오 — 마이그레이션 및 최적화

```
MyISAM -> InnoDB 마이그레이션:

배경:
  레거시 MySQL 5.1 시스템
  MyISAM 테이블 150개
  빈번한 "Table is marked as crashed" 오류
  동시 접속 증가로 테이블 잠금 경합 심화

마이그레이션 절차:

1. 사전 조사:
  SELECT TABLE_NAME, ENGINE, TABLE_ROWS
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = 'mydb' AND ENGINE = 'MyISAM';

2. 외래 키 제약 검증:
  자식 테이블에 없는 부모 행 확인
  (InnoDB 전환 시 외래키 오류 방지)

3. ALTER TABLE:
  ALTER TABLE orders ENGINE=InnoDB;

  대규모 테이블:
  pt-online-schema-change (Percona Toolkit)
  -> 무중단 변환 (쓰기 허용하며 복사)

4. innodb_buffer_pool 조정:
  SET GLOBAL innodb_buffer_pool_size = 8G;

결과:
  Table crash: 0건 (자동 Redo Log 복구)
  동시 쓰기 성능: +340% (테이블 -> 행 잠금)
  응답시간 P99: 120ms -> 35ms

InnoDB 추가 최적화:
  innodb_buffer_pool_instances = 8  (≥8GB일 때)
  innodb_log_file_size = 1G
  innodb_flush_log_at_trx_commit = 2  (성능^, 내구성v)
  innodb_io_capacity = 2000  (SSD 기준)

  PK 설계:
  UUID 대신 AUTO_INCREMENT -> 순차 삽입
  UUID 필요 시: UUID_TO_BIN() 또는 ULIDv7
```

> 📢 **섹션 요약 비유**: MyISAM->InnoDB 마이그레이션 = 구형 수동 금고->디지털 금고 교체 — 수동(MyISAM): 열쇠 분실 시 망가짐(크래시). 디지털(InnoDB): 자동 복구, 동시 사용 가능. 마이그레이션 후 성능 3배+!

---

## 📌 관련 개념 맵

```
스토리지 엔진 (Storage Engine)
+-- InnoDB
|   +-- ACID 트랜잭션
|   +-- 행 단위 잠금
|   +-- MVCC
|   +-- 클러스터드 인덱스
|   +-- 자동 크래시 복구
+-- MyISAM
|   +-- 트랜잭션 없음
|   +-- 테이블 잠금
|   +-- 빠른 COUNT(*)
|   +-- 전문 검색 전통
+-- 선택 기준
    +-- OLTP -> InnoDB
    +-- 읽기 전용 -> MyISAM (레거시)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[MySQL 초기 (1995)]
MyISAM 기본 엔진
단순, 빠른 읽기
      |
      v
[InnoDB 통합 (2001)]
Innobase Oy 인수
ACID 트랜잭션 지원
      |
      v
[MySQL 5.5 (2010)]
InnoDB 기본 엔진으로 변경
MyISAM 퇴조
      |
      v
[MariaDB Aria (2010s)]
MyISAM 발전 버전
크래시 안전성 개선
      |
      v
[현재: InnoDB + RocksDB]
InnoDB: OLTP 표준
RocksDB: 대용량 쓰기 최적화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. InnoDB = 은행 금고 — 거래(트랜잭션) 안전하게. 개인 칸막이(행 잠금). 사고 나도 자동 복구. 새 프로젝트 필수!
2. MyISAM = 도서관 열람실 — 책(데이터)과 카드 목록(인덱스) 분리. 읽기 빠르고 COUNT 빠름. 수정 중엔 전체 입장 금지!
3. 마이그레이션 = 구형->디지털 금고 교체 — ALTER TABLE ENGINE=InnoDB. 대규모는 pt-osc로 무중단. 성능 3배 향상!
