---
title: "Adaptive Query Execution, AQE"
date: "2024-03-23"
tags:
  - "studynote-bigdata"
weight: 59
---
## 핵심 인사이트 (3줄 요약)
- AQE는 Spark 3.0의 핵심 기능으로, 쿼리 실행 도중에 수집된 실제 통계 데이터를 바탕으로 실행 계획을 동적으로 변경한다.
- 셔플 파티션 자동 합병(Coalesce), 조인 전략 변경(Shuffle -> Broadcast), 조인 스큐(Skew) 자동 최적화라는 3대 핵심 기능을 제공한다.
- 정적 최적화(Catalyst)의 한계인 데이터 분포 예측 불확실성을 극복하여 런타임 성능을 획기적으로 향상시킨다.

### Ⅰ. 개요 (Context & Background)
- **정의**: 실행 단계 사이의 중간 결과물(Shuffle Map Output)의 통계를 실시간으로 분석하여, 남은 쿼리 단계를 최적화하는 기법이다.
- **배경**: 기존 Catalyst는 실행 전의 정적 통계에만 의존했다. 하지만 복잡한 필터링이나 조인을 거치면 데이터 크기가 급변하여, 처음에 세운 계획이 런타임에는 비효율적이 되는 경우가 많았다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ AQE Runtime Optimization Cycle ]

  (Query Stage 1) --> [Write Shuffle Map Data]
                            |
                            V
               [ Collect Runtime Statistics ]
                            |
                            V
  (Query Stage 2) <-- [ Re-optimize Plan ]
      - Merge small partitions
      - Handle skewed data
      - Switch to Broadcast Join
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| AQE 핵심 기능 | 상세 내용 | 해결하는 문제 |
| :--- | :--- | :--- |
| **Coalescing Shuffle Partitions** | 너무 작은 여러 파티션을 하나의 적절한 크기로 합침 | 작은 파티션이 너무 많아 발생하는 오버헤드 감소 |
| <strong>Switching Join Strategies</strong> | 조인 대상 테이블이 작아진 것을 감지하면 Broadcast Join으로 변경 | 불필요한 네트워크 셔플 방지 |
| <strong>Optimizing Skew Join</strong> | 특정 파티션에 데이터가 쏠린 경우(Skew) 이를 쪼개서 분산 처리 | 일부 Task만 오래 걸리는 '꼬리 지연' 현상 해결 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>설정 활성화</strong>: Spark 3.2 버전부터 기본 활성화되어 있으나, `spark.sql.adaptive.enabled=true` 설정을 명시적으로 확인해야 한다.
- **스큐 조인 처리**: 데이터 쏠림 현상이 심한 대규모 테이블 조인 시, 힌트(Hint)를 주지 않아도 AQE가 `spark.sql.adaptive.skewJoin.enabled`를 통해 자동으로 성능을 방어해주므로 운영 안정성이 크게 향상된다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- AQE는 "데이터가 어떻게 변할지 모르니 실행하면서 배우자"는 철학을 Spark에 구현했다. 이는 클라우드 네이티브 분산 처리 환경에서 자원 예측의 불확실성을 상쇄하는 가장 강력한 무기이며, 향후 머신러닝 기반의 자동 튜닝 엔진으로 나아가는 핵심 징검다리다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Apache Spark 3.0
- **자식 개념**: Partition Coalescing, Skew Join Optimization
- **연관 개념**: Catalyst Optimizer, CBO, Shuffle

### 📈 관련 키워드 및 발전 흐름도

```text
[정적 쿼리 계획 (Static Query Plan) — CBO]
    |
    v
[런타임 통계 수집 (Runtime Statistics)]
    |
    v
[적응형 쿼리 실행 (AQE, Adaptive Query Execution)]
    |
    v
[파티션 병합 / 스큐 조인 최적화 (Skew Join)]
    |
    v
[ML 기반 자동 튜닝 엔진 (Auto-tuning)]
```

Spark 쿼리 최적화가 컴파일 시점 정적 계획에서 런타임 통계 기반 동적 최적화로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
- 처음에는 지도를 보고 길을 정했지만, 가다 보니 길이 막히는 걸 보고 바로 다른 지름길로 바꾸는 똑똑한 내비게이션이에요.
- 친구들에게 간식을 나눠줄 때, 어떤 친구가 너무 많이 받으면 다른 친구에게 조금 나눠주라고 선생님이 중간에 도와주는 것과 같아요.
- 미리 계획한 대로만 하지 않고, 상황을 보면서 가장 좋은 방법을 그때그때 찾아내는 지혜로운 기술이랍니다.
