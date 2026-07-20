---
title: "2Pc Limitations"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 133
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2PC(Two-Phase Commit)는 <strong>분산 트랜잭션의 원자성을 보장하는 프로토콜(Prepare->Commit/Rollback)</strong>이지만, MSA에서는 <strong>서비스 자율성 침해·성능 저하·단일 장애점(Coordinator)</strong> 문제로 부적합하다.
> 2. **가치**: 2PC는 DB 간 트랜잭션에서는 동작하지만, MSA의 <strong>HTTP/gRPC 서비스 간에는 롤백이 불가능</strong>하고, 하나의 서비스가 느려지면 전체가 블로킹되므로 <strong>Saga 패턴</strong>이 대안이다.
> 3. **판단 포인트**: Choreography Saga(이벤트 기반, 각 서비스 독립)와 Orchestration Saga(중앙 오케스트레이터)를 구분하고, 보상 트랜잭션(Compensating Transaction)이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
2PC: Coordinator -> Prepare(모든 참여자) -> Commit/Rollback
  한계: 블로킹, 단일 장애점, MSA에 부적합

Saga: 서비스별 로컬 트랜잭션 + 실패 시 보상 트랜잭션
  주문 성공 -> 결제 실패 -> 주문 취소(보상)
```

- **📢 섹션 요약 비유**: 2PC는 단체 행동(전원 동시 출발), Saga는 릴레이(각자 달리고, 실패 시 되돌아옴)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | 2PC | Saga |
|:---|:---|:---|
| <strong>일관성</strong> | Strong | **Eventual** |
| **블로킹** | 있음 | **없음** |
| <strong>롤백</strong> | DB 롤백 | <strong>보상 트랜잭션</strong> |
| <strong>MSA</strong> | 부적합 | **적합** |

---

## Ⅲ~Ⅴ. 결론

MSA에서는 <strong>2PC 대신 Saga 패턴으로 Eventual Consistency</strong>를 달성하며, 보상 트랜잭션 설계가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>2PC</strong> | 분산 트랜잭션 (한계) |
| <strong>Saga</strong> | MSA 대안 패턴 |
| **Choreography** | 이벤트 기반 Saga |
| <strong>Orchestration</strong> | 중앙 조율 Saga |
| <strong>보상 트랜잭션</strong> | 실패 시 되돌리기 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2PC (X/Open DTP, 1990s)] -> [MSA 등장 -> 2PC 한계 인식]
    -> [Saga 패턴 (Garcia-Molina, 1987 -> MSA 재발견)]
    -> [이벤트 소싱 + CQRS (2016~)]
    -> [현재: Temporal/Cadence — Saga 오케스트레이션 프레임워크]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 2PC는 <strong>단체 줄넘기</strong>예요. 한 명이 실패하면 **전원 다시** 해야 해요.
2. Saga는 <strong>릴레이</strong>예요. 각자 달리고, 실패하면 **그 구간만 되돌아와요**.
3. MSA에서는 릴레이(Saga)가 더 빠르고 **문제가 적어서** 많이 사용해요!
