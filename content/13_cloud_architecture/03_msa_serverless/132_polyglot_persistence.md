---
title: "Polyglot Persistence"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 132
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Polyglot Persistence는 <strong>각 마이크로서비스가 자신의 데이터 특성에 가장 적합한 DB 기술을 독립적으로 선택</strong>하는 패턴이며, DB per Service의 자연스러운 확장이다.
> 2. **가치**: 모든 서비스가 같은 RDBMS를 사용하면 <strong>그래프 데이터에 JOIN 지옥, 시계열에 비효율 쿼리</strong>가 발생하지만, Polyglot은 <strong>주문=RDB, 추천=그래프DB, 로그=시계열DB</strong>로 최적화한다.
> 3. **판단 포인트**: 운영 복잡도(다양한 DB 관리)가 증가하므로, <strong>관리형 서비스(RDS·DynamoDB·Neptune)</strong>로 운영 부담을 줄이는 것이 현실적이다.

---

## Ⅰ. 개요 및 필요성

```text
주문 서비스 -> PostgreSQL (관계형, ACID)
카탈로그    -> MongoDB (문서형, 유연 스키마)
추천        -> Neo4j (그래프, 관계 탐색)
캐시        -> Redis (인메모리, 고속)
로그        -> InfluxDB (시계열)
```

- **📢 섹션 요약 비유**: Polyglot은 <strong>요리마다 최적의 칼(도구)을 쓰는 것</strong>이다. 모든 요리에 식빵 칼만 쓸 순 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 데이터 유형 | 최적 DB |
|:---|:---|
| **관계형** | PostgreSQL, MySQL |
| **문서** | MongoDB |
| <strong>그래프</strong> | Neo4j |
| **키-값** | Redis, DynamoDB |
| **시계열** | InfluxDB, TimescaleDB |

---

## Ⅲ~Ⅴ. 결론

Polyglot Persistence는 <strong>MSA의 데이터 최적화 전략</strong>이며, 관리형 서비스로 운영 부담을 줄이는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Polyglot** | 서비스별 최적 DB |
| <strong>DB per Service</strong> | Polyglot의 전제 |
| <strong>NoSQL</strong> | 비관계형 DB |
| <strong>관리형 서비스</strong> | 운영 부담 감소 |
| <strong>CAP 정리</strong> | DB 선택 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 RDBMS (모노리스)] -> [NoSQL 등장 (2010s)]
    -> [Polyglot Persistence (MSA, 2014~)]
    -> [관리형 서비스 (AWS RDS/DynamoDB)]
    -> [현재: NewSQL + Polyglot — 최적 조합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Polyglot은 <strong>요리마다 최적의 칼</strong>을 쓰는 거예요. 빵에는 빵 칼, 고기에는 고기 칼!
2. 모든 요리에 **식빵 칼만 쓰면** 비효율적이에요.
3. 각 서비스에 <strong>가장 잘 맞는 DB</strong>를 골라주면 성능이 좋아진답니다!
