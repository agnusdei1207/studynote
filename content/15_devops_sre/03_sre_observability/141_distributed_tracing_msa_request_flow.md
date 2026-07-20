---
title: "Distributed Tracing Msa Request Flow"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 141
---
<!-- top-summary -->
> - 중복 정리: 비대표 노트
> - 군집: Distributed Tracing
> - 🔗 대표 정리: [[188_distributed_tracing_opentelemetry]]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 트레이싱은 <strong>하나의 사용자 요청이 여러 마이크로서비스를 거치는 전체 경로를 Trace ID로 추적</strong>하는 기술이며, 각 서비스 구간을 Span으로 기록하여 지연·에러 지점을 정확히 식별한다.
> 2. **가치**: MSA에서 "API가 느리다"는 <strong>어떤 서비스가 병목인지</strong> 로그만으로는 알 수 없지만, 트레이싱은 <strong>A->B->C->D 전체 호출 체인의 각 구간 소요 시간</strong>을 Waterfall로 시각화한다.
> 3. **판단 포인트**: OpenTelemetry(OTel)가 계측 표준이며, Jaeger·Tempo·Zipkin이 트레이스 백엔드이다. 샘플링(1~10%)으로 오버헤드를 제어한다.

---

## Ⅰ. 개요 및 필요성

```text
요청: 사용자 -> API GW -> 주문 서비스 -> 결제 서비스 -> DB
Trace: {trace_id: "abc123"}
  Span 1: API GW (10ms)
  Span 2: 주문 서비스 (50ms)
  Span 3: 결제 서비스 (200ms) <- 병목!
  Span 4: DB 쿼리 (30ms)
```

- **📢 섹션 요약 비유**: 분산 트레이싱은 <strong>택배 추적</strong>이다. 택배(요청)가 어느 물류센터(서비스)에서 얼마나 머물렀는지 추적한다.

---

## Ⅱ~Ⅴ. 결론

분산 트레이싱은 <strong>MSA 성능 분석·장애 진단의 필수 도구</strong>이며, OTel+Jaeger/Tempo가 표준 스택이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Trace** | 전체 요청 경로 |
| **Span** | 개별 서비스 구간 |
| <strong>Trace ID</strong> | 요청 식별자 |
| <strong>OpenTelemetry</strong> | 계측 표준 |
| **Jaeger/Tempo** | 트레이스 백엔드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper (Google, 2010)] -> [Zipkin (Twitter, 2012)]
    -> [Jaeger (Uber, 2017)] -> [OpenTelemetry (2019)]
    -> [Grafana Tempo (2020)]
    -> [현재: OTel 통합 — Metrics·Logs·Traces 상관 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 분산 트레이싱은 <strong>택배 추적</strong>이에요. 택배가 **어디를 거쳤는지** 봐요.
2. "결제 센터에서 **200ms나 머물렀네!**" -> 여기가 <strong>병목</strong>이구나!
3. 모든 택배에 <strong>추적 번호(Trace ID)</strong>를 붙여서 끝까지 따라가요!
