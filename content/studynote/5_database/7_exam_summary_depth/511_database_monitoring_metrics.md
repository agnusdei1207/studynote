+++
title = "511. 데이터베이스 모니터링 지표 - 시스템의 건강 검진"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 511
+++

# 511. 데이터베이스 모니터링 지표 - 시스템의 건강 검진

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스 모니터링 지표는 시스템의 부하 상태와 성능 효율성을 수치화한 데이터로, **처리량(Throughput), 지연 시간(Latency), 자원 사용률(Resource Utilization)** 등이 핵심이다.
> 2. **가치**: 장애를 선제적으로 예측하고 성능 병목 구간을 정확히 짚어내어, 제한된 하드웨어 자원 하에서 **시스템 가용성을 극대화**하는 근거가 된다.
> 3. **융합**: 실시간 대시보드(Prometheus, Grafana) 및 AI 기반 이상 징후 탐지 기술과 융합되어, 장애 대응 시간(MTTR)을 단축시키는 핵심 관제 인프라로 작동한다.

+++

### Ⅰ. 3대 핵심 모니터링 지표 그룹

1. **처리량 (Throughput)**:
    - **TPS (Transactions Per Second)**: 초당 처리되는 트랜잭션 수.
    - **QPS (Queries Per Second)**: 초당 실행되는 쿼리 수.
2. **지연 시간 (Latency / Response Time)**:
    - 쿼리 하나가 실행되어 결과를 반환할 때까지 걸리는 시간. (사용자 체감 성능)
3. **자원 사용률 (Resource Utilization)**:
    - CPU, Memory, Disk I/O, Network 대역폭 점유율.
    - **Buffer Cache Hit Ratio**: 메모리에서 데이터를 바로 찾은 비율.

+++

### Ⅱ. 모니터링 및 성능 상관관계 시각화 (ASCII Model)

```text
[ DB Performance Correlation ]

  (Load: Users) ──▶ (TPS Increases) ──▶ (CPU/IO Rises) ──▶ (Latency Rises)
         │                 │                  │                  │
         ▼                 ▼                  ▼                  ▼
  [ 🚦 MONITOR ]    [ 🚦 MONITOR ]     [ 🚦 MONITOR ]     [ 🚦 ALERT! 💥 ]
  
  * Normal: TPS ↑ , Latency (Steady)
  * Overload: TPS (Stall) , Latency ↑↑ ✅ "병목 발생 지점 파악 필수"
```

+++

### Ⅲ. 실무에서 가장 중요한 지표: TPS와 Latency

- **TPS는 높은데 Latency도 높다면?**: 처리량은 많지만 개별 사용자는 답답함을 느끼는 상태입니다 (동시성 경합 의심).
- **TPS는 낮은데 Latency만 높다면?**: 특정 무거운 쿼리가 시스템 전체를 잡고 있거나 인덱스 부재, 네트워크 장애 등을 의심해야 합니다.
- **CPU는 낮은데 I/O가 100%라면?**: 메모리 부족으로 인해 빈번한 디스크 읽기가 발생하고 있음을 의미합니다.

- **📢 섹션 요약 비유**: 데이터베이스 모니터링은 **'운전석의 계기판'**과 같습니다. 속도계(TPS)만 보는 게 아니라 엔진 온도(CPU), 연료 잔량(Storage), 그리고 RPM(Latency)을 종합적으로 체크해야 차가 멈추지 않고 고속도로를 안전하게 달릴 수 있는 것과 같습니다. 계기판에 빨간불이 들어오기 전에 미리 점검하는 것이 프로 아키텍트의 자세입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[SLA (Service Level Agreement)]**: 지표를 기준으로 고객과 약속한 성능 품질 보증서.
- **[Wait Events]**: DB가 작업을 못 하고 멈춰 있는 구체적인 이유 (예: Lock 대기).
- **[Observability]**: 단순 수치를 넘어 시스템 내부를 깊게 통찰하는 능력.

📢 **마무리 요약**: **DB Monitoring Metrics**는 데이터베이스의 언어입니다. 숫자가 보내는 신호를 정확히 해석할 때, 우리는 장애를 막고 최고의 성능을 이끌어낼 수 있습니다.