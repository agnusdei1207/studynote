---
title: "Database Per Service"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 131
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Database per Service는 <strong>각 마이크로서비스가 독립적인 데이터베이스를 소유</strong>하여 다른 서비스가 직접 DB에 접근하지 못하고 <strong>오직 API로만 통신</strong>하는 MSA 데이터 패턴이다.
> 2. **가치**: 공유 DB에서는 한 서비스의 스키마 변경이 <strong>다른 모든 서비스에 영향</strong>을 주지만, DB per Service는 <strong>독립 배포·독립 스케일링·기술 다양성(Polyglot Persistence)</strong>을 보장한다.
> 3. **판단 포인트**: 서비스 간 JOIN이 불가능해지므로 <strong>Saga(분산 트랜잭션)·CQRS(쿼리 분리)·이벤트 소싱</strong>이 함께 필요하며, 데이터 일관성은 <strong>Eventual Consistency</strong>로 관리한다.

---

## Ⅰ. 개요 및 필요성

```text
공유 DB: 서비스 A·B·C -> 같은 DB (커플링)
DB per Service: A->DB_A, B->DB_B, C->DB_C (독립)
  서비스 간: API·이벤트로만 통신
```

- **📢 섹션 요약 비유**: 공유 DB는 **공동 냉장고**(한 사람이 정리하면 다른 사람 물건이 밀려남), DB per Service는 **각자 냉장고**(독립 관리).

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | 공유 DB | DB per Service |
|:---|:---|:---|
| **커플링** | 높음 | **낮음** |
| **배포** | 종속 | **독립** |
| <strong>JOIN</strong> | 가능 | <strong>불가 -> API/이벤트</strong> |
| <strong>일관성</strong> | Strong | **Eventual** |

---

## Ⅲ~Ⅴ. 결론

DB per Service는 <strong>MSA의 데이터 독립성 핵심 원칙</strong>이며, Saga·CQRS·이벤트 소싱과 함께 적용해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>DB per Service</strong> | 서비스별 독립 DB |
| <strong>Saga</strong> | 분산 트랜잭션 패턴 |
| <strong>CQRS</strong> | 명령/쿼리 분리 |
| <strong>Eventual Consistency</strong> | 최종 일관성 |
| <strong>Polyglot Persistence</strong> | 서비스별 다른 DB 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[공유 DB (모노리스)] -> [DB per Service (MSA, 2014~)]
    -> [Saga 패턴 (분산 트랜잭션)]
    -> [CQRS + Event Sourcing (2016~)]
    -> [현재: 데이터 메시 — 도메인별 데이터 소유]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 공유 DB는 <strong>공동 냉장고</strong>예요. 한 사람이 정리하면 **다른 사람 물건이 밀려나요**.
2. DB per Service는 <strong>각자 냉장고</strong>예요. 자기 냉장고를 <strong>독립적으로 관리</strong>해요.
3. 대신 남의 냉장고 물건이 필요하면 <strong>부탁(API)</strong>해야 한답니다!
