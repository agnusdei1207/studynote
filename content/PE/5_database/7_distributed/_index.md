+++
title = "분산 데이터베이스"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# 분산 데이터베이스

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 데이터베이스는 물리적으로 분산된 여러 노드에 데이터를 저장하면서 논리적으로는 단일 시스템처럼 투명성(Transparency)을 제공하는 데이터베이스 아키텍처다.
> 2. **가치**: 위치 투명성, 분할 투명성, 복제 투명성 등 6가지 투명성을 통해 사용자와 애플리케이션에게 분산 환경의 복잡성을 숨기고, 확장성과 가용성을 동시에 확보한다.
> 3. **융합**: 분산 트랜잭션(2PC, 3PC), 합의 알고리즘(Raft, Paxos), 데이터 분할/복제 전략은 현대 클라우드 네이티브 아키텍처의 핵심 기반이다.

---

### 학습 키워드 목록

#### 분산 DB 기본
- [261. 분산 데이터베이스](./261_distributed_database.md) - 정의, 목표, 특징
- 분산 DB 투명성 6가지 - 위치, 분할, 복제, 병행, 장애, 지역 사상 투명성
- 동종/이종 분산 DB

#### 데이터 분할 및 복제
- 수평 분할 (Horizontal Fragmentation)
- 수직 분할 (Vertical Fragmentation)
- 복제 (Replication) - 동기식/비동기식
- 마스터-슬레이브 vs 멀티 마스터
- 셰어드 낫띵 (Shared Nothing) 아키텍처

#### 분산 합의 및 일관성
- 2단계 커밋 (2PC), 3단계 커밋 (3PC)
- Raft/Paxos 알고리즘 - 리더 선출, 로그 복제
- 벡터 시계 (Vector Clock)
- 스플릿 브레인 (Split Brain) 방지
- Quorum 기반 일관성

#### 분산 DB 제품
- Oracle RAC - 공유 디스크 기반
- Google Spanner - 글로벌 분산
- CockroachDB - 생존성 중심
- Amazon Aurora - 스토리지 분리
