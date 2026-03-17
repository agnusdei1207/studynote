+++
title = "트랜잭션, 동시성 제어 및 복구"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# 트랜잭션, 동시성 제어 및 복구

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션은 데이터베이스에서 논리적 작업 단위로서 ACID(원자성, 일관성, 격리성, 영속성) 특성을 보장받는 일련의 연산 집합이며, 동시성 제어와 회복 기법은 이를 구현하는 핵심 메커니즘이다.
> 2. **가치**: 동시성 제어(2PL, MVCC)는 다중 사용자 환경에서 데이터 일관성 유지와 처리량 극대화를 동시에 달성하게 하고, WAL 기반 회복 기법은 장애 발생 시 데이터 손실 없는 복구를 보장한다.
> 3. **융합**: 분산 트랜잭션(2PC, Saga), CAP 이론, 결과적 일관성 모델은 현대 클라우드/마이크로서비스 아키텍처에서 핵심적인 설계 결정 사항이다.

---

### 학습 키워드 목록

#### 트랜잭션 기본
- [191. 트랜잭션](./191_transaction.md) - 정의 및 ACID 특성
- 원자성 (Atomicity) - All or Nothing
- 일관성 (Consistency) - 무결성 제약조건 유지
- 격리성 (Isolation) - 트랜잭션 간 간섭 방지
- 영속성 (Durability) - 영구 반영 보장
- 트랜잭션 상태 전이 - Active, Committed, Aborted

#### 동시성 제어
- 동시성 문제 - Lost Update, Dirty Read, Unrepeatable Read, Phantom Read
- 락킹 (Locking) - Shared Lock, Exclusive Lock
- 2단계 락킹 (2PL) - Growing Phase, Shrinking Phase
- 격리 수준 - Read Uncommitted ~ Serializable
- MVCC - 다중 버전 동시성 제어
- 타임스탬프 순서 기법
- 낙관적 동시성 제어

#### 회복 기법
- Redo/Undo 연산
- WAL (Write-Ahead Logging) 프로토콜
- 체크포인트 (Checkpoint) 기법
- ARIES 알고리즘
- 그림자 페이징 (Shadow Paging)

#### 분산 트랜잭션
- 2단계 커밋 (2PC) - Prepare, Commit/Rollback
- 3단계 커밋 (3PC)
- Saga 패턴 - 보상 트랜잭션
- CAP 정리 - Consistency, Availability, Partition Tolerance
- BASE 속성 - Basically Available, Soft-state, Eventually consistent
