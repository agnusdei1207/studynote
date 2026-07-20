---
title: "Buffer Pool Manager"
date: "2025-01-01"
tags:
  - "DBMS"
  - "InnoDB"
  - "LRU"
  - "WAL"
  - "buffer pool"
  - "clock algorithm"
  - "dirty page"
  - "page replacement"
  - "studynote-database"
weight: 50
---
> **핵심 인사이트 3줄**
> 1. 버퍼 풀(Buffer Pool)은 디스크 I/O를 줄이기 위해 자주 접근하는 페이지를 메모리에 캐시하는 DBMS의 핵심 컴포넌트다.
> 2. LRU(Least Recently Used) 알고리즘은 가장 오랫동안 참조되지 않은 페이지를 교체하며, InnoDB는 LRU 리스트를 Young/Old 영역으로 나눠 풀 스캔에 의한 캐시 오염을 방지한다.
> 3. 더티 페이지(Dirty Page)는 수정됐지만 아직 디스크에 기록되지 않은 페이지로, WAL(Write-Ahead Logging)과 체크포인트가 지속성을 보장한다.

---

## Ⅰ. 버퍼 풀의 역할과 구조

### 1.1 메모리-디스크 계층

```
SQL 쿼리
   v
버퍼 풀 (Buffer Pool, 메모리)
   +-- 페이지 테이블 (page table): page_id -> frame_id
   +-- free list: 빈 프레임 목록
   +-- LRU list: Young(Hot) | Old(Cold) 영역
   +-- flush list: 더티 페이지 목록
   <->  (miss 시 디스크 I/O)
데이터 파일 (.ibd)
```

### 1.2 페이지 요청 흐름

1. 페이지 테이블에서 page_id 조회 -> <strong>히트(hit)</strong>: 프레임 반환
2. **미스(miss)**: free list에서 프레임 확보 -> 디스크에서 페이지 로드 -> LRU 리스트 삽입

📢 **섹션 요약 비유**: 버퍼 풀은 사서가 자주 빌리는 책을 책상 서랍(메모리)에 모아두는 것 — 서랍에 없으면 서고(디스크)에서 꺼내온다.

---

## Ⅱ. 페이지 교체 알고리즘

### 2.1 LRU (Least Recently Used)

```
접근 순서: A B C D -> A 참조

LRU 리스트 (왼쪽=MRU, 오른쪽=LRU):
초기:  [D, C, B, A]
A 참조: [A, D, C, B]  <- A가 앞으로 이동
교체 필요 시: B (가장 오른쪽) 교체
```

### 2.2 InnoDB의 LRU 변형

```
Young 영역 (5/8)    | Old 영역 (3/8)
[최근 접근 페이지]  | [새로 로드된 페이지]
                    ^ midpoint
```

- 새 페이지는 Old 영역으로 삽입 (풀 스캔 오염 방지)
- Old 영역에서 1초 이상 후 재접근 시 Young 영역으로 승격

### 2.3 Clock 알고리즘

```
프레임을 원형으로 배치, reference bit 사용:
[A:1] -> [B:0] -> [C:1] -> [D:0] ...
       ^ clock hand
```

- 페이지 접근 시 reference bit = 1
- 교체 시 clock hand 이동: bit=1이면 0으로 초기화 후 통과, bit=0이면 교체

📢 **섹션 요약 비유**: LRU는 마지막으로 쓴 시간 기록, Clock은 한 바퀴 돌면서 최근 안 쓴 자리 차지.

---

## Ⅲ. 더티 페이지와 플러시 정책

### 3.1 더티 페이지 관리

```
페이지 읽기 -> 수정 -> dirty bit = 1 -> flush list 등록
                               v
                       체크포인트 발생 시
                       또는 free list 부족 시
                               v
                       디스크 플러시 (write)
```

### 3.2 플러시 트리거

| 트리거              | 설명                              |
|--------------------|-----------------------------------|
| 체크포인트(Checkpoint) | 주기적으로 더티 페이지를 디스크에 기록 |
| LRU 플러시          | 교체 대상 페이지가 더티인 경우 즉시 기록 |
| 백그라운드 플러시    | page cleaner 스레드가 주기적 기록    |
| 강제 플러시(Force)   | 트랜잭션 커밋 시 (innodb_flush_log_at_trx_commit) |

📢 **섹션 요약 비유**: 더티 페이지는 아직 제출 안 한 과제 — 선생님(체크포인트)이 올 때까지 책상 서랍에 있지만, 자리 필요하면 먼저 제출해야 한다.

---

## Ⅳ. WAL과 버퍼 풀의 관계

### 4.1 Write-Ahead Logging 원칙

1. <strong>수정 전 로그 먼저</strong>: 페이지를 디스크에 플러시하기 전에 WAL(리두 로그)에 먼저 기록.
2. <strong>STEAL/FORCE 정책</strong>:
   - STEAL: 커밋 전 더티 페이지 플러시 허용 (버퍼 풀 공간 확보)
   - NO-FORCE: 커밋 시 페이지 직접 기록 불필요 (리두 로그로 복구 가능)

### 4.2 크래시 복구 흐름

```
크래시 발생
    v
InnoDB 재시작
    v
리두 로그 분석(Analysis) -> 리두(Redo) -> 언두(Undo)
    v
버퍼 풀 정상 복구
```

📢 **섹션 요약 비유**: WAL은 일기(로그)를 먼저 쓰고 행동하는 것 — 사고가 나도 일기를 보면 어디까지 했는지 알 수 있다.

---

## Ⅴ. InnoDB 버퍼 풀 튜닝

### 5.1 주요 파라미터

| 파라미터                          | 기본값  | 설명                          |
|----------------------------------|---------|-------------------------------|
| innodb_buffer_pool_size          | 128MB   | 버퍼 풀 총 크기 (서버 RAM의 70~80% 권장) |
| innodb_buffer_pool_instances     | 8       | 병렬 접근을 위한 인스턴스 수  |
| innodb_old_blocks_pct            | 37%     | Old 영역 비율                 |
| innodb_old_blocks_time           | 1000ms  | Old->Young 승격 대기 시간      |
| innodb_page_cleaners             | 4       | 플러시 스레드 수               |

### 5.2 히트율 모니터링

```sql
SHOW STATUS LIKE 'Innodb_buffer_pool%';
-- Innodb_buffer_pool_read_requests / Innodb_buffer_pool_reads
-- 히트율 = (read_requests - reads) / read_requests × 100
-- 목표: 99% 이상
```

📢 **섹션 요약 비유**: 히트율 99%는 100번 요청 중 99번은 메모리에서 바로 꺼낸다는 것 — 1번만 서고(디스크)에 간다.

---

## 📌 관련 개념 맵

```
버퍼 풀 매니저
+-- 페이지 교체 정책
|   +-- LRU
|   +-- InnoDB Young/Old LRU
|   +-- Clock 알고리즘
+-- 더티 페이지 관리
|   +-- 체크포인트
|   +-- WAL (Write-Ahead Log)
|   +-- 크래시 복구 (Redo/Undo)
+-- 튜닝 포인트
    +-- 버퍼 풀 크기
    +-- 인스턴스 수
    +-- 히트율 모니터링
```

---

## 📈 관련 키워드 및 발전 흐름도

```
초기 DBMS: 더블 버퍼링 (1970s)
     |  LRU 알고리즘 도입
     v
전통적 버퍼 매니저 (STEAL/NO-FORCE + WAL)
     |  풀 스캔 오염 문제
     v
InnoDB Young/Old LRU (MySQL 5.x)
     |  대용량 메모리 대응
     v
멀티 인스턴스 버퍼 풀 (MySQL 5.5+)
     |  NVM/PMEM 등장
     v
영속 버퍼 풀 (Persistent Buffer Pool, MySQL 5.7+)
재시작 후 워밍업 없이 히트율 유지
```

**핵심 키워드**: LRU, 더티 페이지, WAL, 체크포인트, STEAL, NO-FORCE, 히트율

---

## 👶 어린이를 위한 3줄 비유 설명

1. 버퍼 풀은 도서관 사서의 책상 서랍 — 자주 빌리는 책을 미리 꺼내놔서 빠르게 빌려줘.
2. 더티 페이지는 내용을 고쳤지만 아직 반납 안 한 책 — 나중에 선생님(체크포인트)이 모아서 공식 기록에 반영해.
3. WAL은 "먼저 일기 쓰고 행동" 규칙 — 갑자기 전기가 나가도 일기를 보면 어디까지 했는지 알 수 있어.
