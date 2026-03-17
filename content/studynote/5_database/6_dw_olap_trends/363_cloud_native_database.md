+++
title = "363. 클라우드 네이티브 DB - Aurora와 Cosmos DB의 혁신"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 363
+++

# 363. 클라우드 네이티브 DB - Aurora와 Cosmos DB의 혁신

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클라우드 네이티브 데이터베이스는 클라우드의 무한한 자원을 활용하기 위해 **컴퓨팅(Compute)과 스토리지(Storage)를 완전히 분리**하고, 자동 확장 및 고가용성을 기본으로 설계된 차세대 데이터 저장소다.
> 2. **가치**: 인프라 관리에 대한 부담(패치, 백업, 샤딩 등)을 클라우드 제공사에 위임하고, 개발자는 비즈니스 로직과 데이터 활용에만 집중할 수 있는 **운영 생산성**을 제공한다.
> 3. **융합**: 관계형의 정교함(Aurora)과 비관계형의 유연함(Cosmos DB)이 각각의 영역에서 클라우드 기술과 융합되어, 전 지구적 규모(Global Scale)의 데이터 처리를 실현한다.

+++

### Ⅰ. 핵심 아키텍처: 컴퓨팅과 스토리지의 분리

- **전통적 DB**: 서버 한 대에 CPU, RAM, Disk가 묶여 있어 확장이 어렵습니다.
- **클라우드 네이티브 DB**: 
    - **Compute Layer**: 쿼리 처리와 트랜잭션을 담당. 필요에 따라 대수를 늘리거나 줄임.
    - **Storage Layer**: 수천 개의 노드에 데이터를 분산 복제. 컴퓨팅 서버와 상관없이 독자적으로 수 페타바이트까지 자동 확장.

+++

### Ⅱ. 주요 모델별 시각화 (ASCII Model)

```text
[ 1. Amazon Aurora (Log-is-the-database) ]
  [ Compute Node ] ──▶ [ Log Stream ] ──▶ [ Distributed Storage ]
                                          (6-way Replication)

[ 2. Azure Cosmos DB (Multi-model & Global) ]
  [ User in Asia ]      [ User in USA ]
         │                     │
  ┌──────▼──────┐       ┌──────▼──────┐
  │ Local Shard │ ◀──▶  │ Local Shard │ (Multi-Master Sync)
  └─────────────┘       └─────────────┘
  (API: SQL, MongoDB, Cassandra, Graph supported)
```

+++

### Ⅲ. 대표 주자의 특징 비교

| 비교 항목 | AWS Aurora (NewSQL 지향) | Azure Cosmos DB (NoSQL 지향) |
|:---|:---|:---|
| **기본 모델** | 관계형 (MySQL / PostgreSQL 호환) | **멀티 모델** (Doc, Graph, KV 등) |
| **일관성 모델** | 강력한 일관성 (Strong) | **5단계 튜너블 일관성** |
| **확장 방식** | 스토리지 자동 확장, 읽기 전용 확장 | **전 세계적 수평 확장 (Global Scale)** |
| **주요 강점** | 기존 RDB의 5배 성능, 고신뢰성 | 초저지연(ms), 99.999% SLA 보장 |

- **📢 섹션 요약 비유**: 클라우드 네이티브 DB는 **'수도 시설'**과 같습니다. 예전에는 집마다 우물(전통적 DB)을 파서 직접 관리해야 했지만, 이제는 수도꼭지만 틀면(클라우드 접속) 언제든 원하는 만큼 물(데이터 처리량)이 나오고, 사용한 만큼만 요금을 내면 되는 것과 같습니다. 물탱크(스토리지)가 얼마나 큰지, 펌프(컴퓨팅)가 어디에 있는지는 사용자가 걱정할 필요가 없습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Serverless DB]**: 사용자가 없을 땐 자원을 반납하고 비용을 0으로 만드는 고도화된 클라우드 기술.
- **[Global Distribution]**: 전 세계 어디서든 10ms 이내로 데이터에 접근하게 하는 기술.
- **[Decoupled Architecture]**: 클라우드 네이티브의 핵심 설계 원칙.

📢 **마무리 요약**: **Cloud Native Database**는 현대 인프라의 마침표입니다. 물리적 한계를 넘어선 유연함과 성능을 통해, 전 지구를 대상으로 하는 혁신적인 서비스를 가능케 합니다.