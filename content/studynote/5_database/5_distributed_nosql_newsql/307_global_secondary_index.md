+++
title = "307. 글로벌 보조 인덱스 (GSI) - 분산 데이터의 전역 탐색"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 307
+++
# 307. 글로벌 보조 인덱스 (GSI, Global Secondary Index)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GSI(Global Secondary Index)는 분산 데이터베이스에서 기본 파티션 키(Partition Key)가 아닌 **일반 속성을 기준으로 데이터를 조회하기 위해, 원본 데이터와는 독립적인 파티션 구조를 가진 인덱스 테이블**이다.
> 2. **가치**: 특정 샤드에 국한되지 않고 전체 클러스터에 흩어진 데이터를 고속으로 탐색할 수 있게 하며, 원본 데이터의 샤드 키 제약을 넘어 다양한 조회 패턴을 지원한다.
> 3. **융합**: 비동기적 데이터 복제 기술과 결합되어 원본 쓰기 성능에 영향을 주지 않으면서도 강력한 검색 기능을 제공하는 현대 NoSQL(DynamoDB, Cassandra 등)의 핵심 기능이다.

+++

### Ⅰ. GSI의 정의 및 필요성

- **배경**: 분산 DB는 보통 '샤드 키'를 알아야만 특정 서버로 바로 찾아갈 수 있습니다. 만약 샤드 키가 아닌 다른 필드로 검색하려면 모든 샤드를 다 뒤져야 하는(Scatter-Gather) 비효율이 발생합니다.
- **해결책**: 조회하고 싶은 필드를 '새로운 샤드 키'로 삼는 **별도의 인덱스 테이블**을 만듭니다.

+++

### Ⅱ. GSI 아키텍처 및 데이터 흐름 (ASCII Flow)

원본 테이블이 'UserID'로 샤딩되어 있어도, GSI를 통해 'Email'로 즉시 조회가 가능해집니다.

```text
[ 원본 Table (Shard by UserID) ]      [ GSI Table (Shard by Email) ]
  UserID: 1  ──▶ (Sync / Copy) ──▶  Email: aaa@ai.com ──▶ UserID: 1
  UserID: 2  ──▶ (Sync / Copy) ──▶  Email: bbb@ai.com ──▶ UserID: 2

  [ Query Flow ]
  1. Client: "Find user with email 'aaa@ai.com'"
  2. Router: Check GSI (Finds UserID: 1) ✅
  3. Router: Fetch full data from Original Table using UserID: 1
```

+++

### Ⅲ. GSI의 특징과 제약

1. **비동기 업데이트**: 원본에 데이터가 써지면 0.x초 뒤에 GSI에 반영됩니다. (결과적 일관성)
2. **독립적 확장**: GSI는 원본 데이터와 상관없이 자신만의 처리량(Throughput)을 가질 수 있습니다.
3. **추가 비용**: 데이터를 한 번 더 쓰는 셈이므로 스토리지 용량과 쓰기 비용이 추가로 발생합니다.

- **📢 섹션 요약 비유**: GSI는 **'도서관의 주제별 색인 카드'**와 같습니다. 원래 책들은 '청구기호(샤드 키)' 순서로 꽂혀 있지만, 내가 '작가 이름'으로 찾고 싶다면 작가별로 정리된 별도의 카드함(GSI)을 보고 책의 위치를 알아낼 수 있는 것과 같습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[LSI (Local Secondary Index)]**: 데이터와 같은 파티션 내에 존재하는 인덱스 (GSI와 대조).
- **[Scatter-Gather]**: GSI가 없을 때 발생하는 최악의 전체 검색 시나리오.
- **[Throughput Provisioning]**: GSI 성능을 위해 별도로 할당하는 자원.

📢 **마무리 요약**: **GSI**는 분산 DB의 조회 자유도를 극대화합니다. 샤드 키의 한계를 극복하고 다양한 비즈니스 요구사항을 처리하기 위한 필수적인 설계 도구입니다.
