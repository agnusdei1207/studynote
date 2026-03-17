+++
title = "571. Spark Streaming vs Flink - 마이크로 배치와 네이티브 스트림"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 571
+++

# 571. Spark Streaming vs Flink - 마이크로 배치와 네이티브 스트림

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Spark Streaming은 흐르는 데이터를 아주 짧은 시간 단위로 끊어서 처리하는 **마이크로 배치(Micro-batch)** 방식인 반면, Flink는 데이터가 들어오는 즉시 하나씩 처리하는 **네이티브 스트리밍(Native Streaming)** 방식이다.
> 2. **가치**: Spark는 배치와 스트리밍의 통합 코드를 제공하여 개발이 용이하고 처리량(Throughput)이 높으며, Flink는 초저지연(Ultra-low Latency)과 정교한 상태 관리(State Mgmt)를 통해 실시간성에 최적화되어 있다.
> 3. **융합**: 인메모리 연산 기술과 분산 체크포인트 기술이 융합되어, 두 엔진 모두 장애 시에도 데이터 유실 없는 'Exactly-once' 처리를 보장하는 현대 실시간 분석의 중추가 된다.

+++

### Ⅰ. 두 스트리밍 엔진의 상세 비교

| 비교 항목 | Apache Spark Streaming | Apache Flink |
|:---|:---|:---|
| **처리 방식** | **마이크로 배치** (Micro-batch) | **네이티브 스트림** (One-by-one) |
| **지연 시간 (Latency)** | 수백 ms ~ 수 초 | **밀리초 (ms) 미만** |
| **처리량 (Throughput)** | 매우 높음 (배치 효율) | 높음 |
| **시간 개념** | 처리 시간 (Processing Time) 위주 | **이벤트 시간 (Event Time)** 완벽 지원 |
| **상태 관리** | 상대적으로 단순 | **매우 강력 (Stateful Functions)** |

+++

### Ⅱ. 처리 매커니즘 시각화 (ASCII Model)

```text
[ 1. Spark: Micro-batch ]
  Stream ──▶ [ Interval 1s ] ──▶ [ Interval 1s ] ✅ "Chunk by Chunk"
                │ (Processing)      │ (Processing)
                ▼                   ▼
[ 2. Flink: Native Stream ]
  Stream ──▶ [E][V][E][N][T] ──▶ ✅ "Immediate Processing per event"
             │  │  │  │  │
             ▼  ▼  ▼  ▼  ▼
```

+++

### Ⅲ. 실무적 선택 가이드

- **Spark Streaming 선택**: 
    - 이미 Spark 배치 시스템을 쓰고 있어 코드를 재사용하고 싶을 때.
    - 실시간 응답이 1초 내외여도 충분하고, 대량의 데이터를 한꺼번에 집계(Aggregation)하는 것이 중요할 때.
- **Flink 선택**: 
    - 이상 결제 탐지(FDS)나 실시간 알림처럼 0.1초의 지연도 허용되지 않을 때.
    - 데이터가 늦게 도착하거나 순서가 뒤바뀌는 복잡한 상황에서도 정확한 시간 기반 분석이 필요할 때.

- **📢 섹션 요약 비유**: 이 두 엔진은 **'배달 시스템'**과 같습니다. Spark Streaming은 배달원(엔진)이 주문 5개가 모일 때까지 기다렸다가 한꺼번에 오토바이에 싣고 나가는(마이크로 배치) 방식입니다. 효율은 좋지만 첫 번째 주문 손님은 조금 기다려야 합니다. Flink는 주문이 들어오는 즉시 배달원이 자전거를 타고 바로 출발하는(네이티브 스트림) 방식입니다. 한 번에 많이 나르진 못해도 손님에게 가장 빨리 도착하는 기동성이 특징입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Exactly-once]**: 중복이나 누락 없이 정확히 한 번만 처리하는 보장 수준.
- **[Checkpointing]**: 상태 정보를 주기적으로 저장하여 장애에 대비하는 기술.
- **[Windowing]**: 흐르는 데이터를 시간이나 개수 단위로 묶어서 연산하는 기법.

📢 **마무리 요약**: **Spark vs Flink**는 속도와 효율의 선택입니다. 시스템의 요구 지연 시간과 기존 인프라와의 정합성을 고려하여, 데이터의 흐름을 가장 우아하게 다룰 수 있는 엔진을 선택해야 합니다.