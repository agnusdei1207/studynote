---
title: "Distributed Tracing Trace ID"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 321
---
> **핵심 인사이트**
> - Distributed Tracing (분산 추적)은 마이크로서비스 환경에서 단일 요청의 전체 흐름을 Trace ID로 연결해 병목·오류를 추적한다.
> - Trace (트레이스)는 연관된 Span (스팬)의 집합이고, 각 Span은 하나의 서비스 작업 단위를 나타낸다.
> - W3C Trace Context 표준으로 서비스 간 Trace ID 전파가 표준화됐다.

---

## Ⅰ. Trace와 Span 구조

```
Trace ID: abc-123
------------------------------------------------------
Span 1: API Gateway       [0ms ---------------- 200ms]
  Span 2: Order Service     [10ms ------- 180ms]
    Span 3: Inventory Svc      [20ms -- 80ms]
    Span 4: DB Query              [90ms - 160ms]
------------------------------------------------------
```

| 개념       | 정의                                          |
|------------|-----------------------------------------------|
| Trace      | 단일 요청 전체 수명주기를 나타내는 Span 집합   |
| Span       | 하나의 작업 단위 (서비스 호출, DB 쿼리 등)    |
| Trace ID   | Trace 전체를 식별하는 고유 ID                 |
| Span ID    | 개별 Span을 식별하는 ID                       |
| Parent ID  | 상위 Span을 가리키는 ID (트리 구조 형성)      |

> 📢 **Ⅰ 섹션 요약 비유**
> Trace는 여행 일정 전체, Span은 각 도시에서의 일정 — Trace ID는 여행 예약 번호다.

---

## Ⅱ. Trace Context 전파

HTTP 헤더를 통해 Trace ID가 서비스 간 전달된다.

W3C Trace Context 표준 헤더:
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             버전  TraceID                          SpanID        플래그
```

B3 Propagation (Zipkin 방식):
```
X-B3-TraceId: 4bf92f3577b34da6a3ce929d0e0e4736
X-B3-SpanId:  00f067aa0ba902b7
X-B3-Sampled: 1
```

> 📢 **Ⅱ 섹션 요약 비유**
> Trace ID 전파는 릴레이 바통 — 각 주자(서비스)가 같은 바통(Trace ID)을 넘겨받아 이어 달린다.

---

## Ⅲ. Sampling 전략

| 전략             | 설명                                     |
|------------------|------------------------------------------|
| Head Sampling    | 요청 시작 시점에 확률로 샘플링 여부 결정  |
| Tail Sampling    | 요청 완료 후 오류·지연 기준으로 샘플링   |
| Rate Limiting    | 초당 N개 Trace만 샘플링                  |

Tail Sampling이 더 유용하지만 구현 복잡도가 높다 — OpenTelemetry Collector에서 지원한다.

> 📢 **Ⅲ 섹션 요약 비유**
> 샘플링은 음식점 품질 검사 — 모든 접시를 다 검사하지 않고 의심스러운 것만 골라 집중 점검한다.

---

## Ⅳ. 대표 도구

| 도구         | 특징                                       |
|--------------|--------------------------------------------|
| Jaeger       | CNCF 졸업 프로젝트, Uber 기원              |
| Zipkin       | Twitter 기원, B3 Propagation 표준화         |
| Tempo        | Grafana Labs, Loki·Prometheus와 통합        |
| AWS X-Ray    | AWS 네이티브 분산 추적 서비스              |

OpenTelemetry SDK가 각 도구의 공통 계측 레이어 역할을 한다.

> 📢 **Ⅳ 섹션 요약 비유**
> Jaeger·Zipkin·Tempo는 각각 다른 브랜드의 GPS 앱이고, OpenTelemetry는 표준 지도 데이터를 제공하는 플랫폼이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소         | 역할                                    |
|-------------------|-----------------------------------------|
| Trace             | 단일 요청 전체 수명주기                  |
| Span              | 개별 작업 단위                          |
| Trace ID          | Trace 전체 식별자                       |
| W3C Trace Context | 표준 헤더 기반 Trace 전파 규격          |
| Sampling          | 추적 오버헤드 제어 전략                 |
| Jaeger / Zipkin   | 분산 추적 백엔드 도구                   |

### 관련 키워드 및 발전 흐름도

```
Distributed Tracing
    +-- Trace / Span / Trace ID -> 기본 데이터 구조
    +-- W3C Trace Context / B3 -> 전파 표준
    +-- Sampling -> Head / Tail / Rate Limiting
    +-- OpenTelemetry -> 표준 계측 SDK + Collector
```

> 🧒 **어린이 비유**
> Trace ID는 소포 운송장 번호예요. 물건이 어느 배송센터를 거쳤는지 한 번호로 전부 추적할 수 있어요.
