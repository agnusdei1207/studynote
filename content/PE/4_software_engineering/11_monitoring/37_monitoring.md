+++
title = "37. 모니터링 도구 (Monitoring Tools)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Monitoring", "Prometheus", "Grafana", "Metrics", "Alerting"]
draft = false
+++

# 모니터링 도구 (Monitoring Tools)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모니터링 도구는 **"시스템 **상태**를 **실시간**으로 **관찰**하고 **이상**을 **탐지**하는 **시스템"**으로, **Metrics**(지표), **Logs**(로그), **Traces**(트레이스)를 **수집**하고 **Alert**(알림)를 **발송**한다.
> 2. **구성**: **Collector**(데이터 **수집), **Storage**(시계열 **DB), **Visualization**(대시 **보드), **Alerting**(알림 **엔진)로 **구성**되며 **Pull**(주기적 **수집)과 **Push**(이벤트 **전송) **방식**이 **있다.
> 3. **도구**: **Prometheus**(수집), **Grafana**(시각화), **ELK Stack**(로그), **Jaeger**(트레이싱), **PagerDuty**(알림)가 **대표적**이며 **Observability**(관찰 **가능성)를 **제공**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
모니터링은 **"시스템 가시성"** 확보이다.

**3 Pillars of Observability**:
| Pillar | 설명 | 도구 |
|--------|------|------|
| **Metrics** | 수치화된 데이터 | Prometheus |
| **Logs** | 이벤트 기록 | ELK |
| **Traces** | 요청 경로 추적 | Jaeger |

### 💡 비유
모니터링은 ****자동차 **계기판 ****과 같다.
- **속도계**: Throughput
- **연료 게이지**: CPU/Memory
- **엔진 라이트**: Error rate

---

## Ⅱ. 아키텍처 및 핵심 원리

### 모니터링 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Monitoring Pipeline                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Application / System                                                                   │  │
    │    │                                                                                    │  │
    │    ├─→ Metrics (Prometheus format)                                                       │  │
    │    │    │                                                                               │  │
    │    │    ▼ Pull (every 15s)                                                               │  │
    │    │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │    │  │  Prometheus Server                                                               │  │  │
    │    │  │  ┌────────────────────────────────────────────────────────────────────────────┐  │  │  │  │
    │    │  │  │  • Scrape targets (/metrics endpoint)                                      │  │  │  │
    │    │  │  │  • Store in TSDB (Time Series DB)                                         │  │  │  │
    │    │  │  │  • Evaluate rules (alerting)                                                   │  │  │  │
    │    │  │  └────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │    │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    │    │                                                                                    │  │
    │    ├─→ Logs (JSON/Text)                                                                 │  │
    │    │    │                                                                               │  │
    │    │    ▼ Push/Filebeat                                                                  │  │
    │    │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │    │  │  Logstash / Fluentd → Elasticsearch → Kibana                                    │  │  │
    │    │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    │    │                                                                                    │  │
    │    └─→ Traces (OpenTelemetry)                                                            │  │
    │         │                                                                               │  │
    │         ▼ Push                                                                          │  │
    │    ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │    │  Jaeger / Tempo → Grafana Tempo                                                      │  │  │
    │    └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Grafana Dashboard                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Query Prometheus                                                                    │  │  │
    │  │  • Visualize metrics (graphs, gauges)                                                 │  │  │
    │  │  • Set up alerts                                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
            │
            ▼ Alert fires
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  AlertManager → Slack / Email / PagerDuty                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Prometheus Metrics

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Prometheus Metrics Format                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # HELP http_requests_total Total number of HTTP requests                               │  │
    │  # TYPE http_requests_total counter                                                       │  │
    │  http_requests_total{method="post",code="200"} 1237                                    │  │
    │  http_requests_total{method="post",code="400"}    14                                    │  │
    │  http_requests_total{method="get",code="200"} 53039                                   │  │
    │                                                                                         │  │
    │  # HELP http_request_duration_seconds HTTP request latencies                           │  │
    │  # TYPE http_request_duration_seconds histogram                                          │  │
    │  http_request_duration_seconds_bucket{le="0.1"} 10000                                  │  │
    │  http_request_duration_seconds_bucket{le="0.5"} 25000                                  │  │
    │  http_request_duration_seconds_bucket{le="1.0"} 30000                                  │  │
    │  http_request_duration_seconds_sum 15000                                               │  │
    │  http_request_duration_seconds_count 50000                                             │  │
    │                                                                                         │  │
    │  Metric Types:                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Counter: Monotonically increasing (requests, errors)                                  │  │  │
    │  │  Gauge: Point-in-time value (memory, temperature)                                    │  │  │
    │  │  Histogram: Distribution (latency, request size)                                    │  │  │
    │  │  Summary: Percentiles (p50, p95, p99)                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Pull vs Push 모델

| 구분 | Pull (Prometheus) | Push (StatsD, Datadog) |
|------|-------------------|------------------------|
| **방식** | 주기적 수집 | 이벤트 전송 |
| **부하** | 서버 제어 | 에이전트 제어 |
| **확장** | Service Discovery | Ingestion API |

### PromQL 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         PromQL Queries                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CPU Usage:                                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)       │  │  │
    │  │  → CPU utilization percentage per instance                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Request Rate:                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  sum(rate(http_requests_total[5m]))                                                     │  │  │
    │  │  → Requests per second (all endpoints)                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Error Rate:                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))   │  │  │
    │  │  → Error percentage                                                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  P95 Latency:                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))                │  │  │
    │  │  → 95th percentile latency                                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### Prometheus 설정

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node1:9100', 'node2:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m]))"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 마이크로서비스 모니터링
**상황**: 분산 추적 필요
**판단**: Prometheus + Grafana + Tempo

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Distributed Tracing                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Request Flow:                                                                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Client → API Gateway → Service A → Service B → Database                                │  │  │
    │  │    │         │             │          │          │                                  │  │  │
    │  │    └─────────┴─────────────┴──────────┴──────────┘                                  │  │  │
    │  │           Trace ID (correlated across all services)                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Jaeger UI:                                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  API Gateway: 5ms            Total: 120ms                                        │  │  │  │
    │  │  │  └─→ Service A: 45ms          90% of time in DB                                 │  │  │  │
    │  │  │      └─→ Service B: 30ms                                                            │  │  │  │
    │  │  │         └─→ Database: 40ms  ← Bottleneck!                                     │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Identify slow service/database                                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 모니터링 기대 효과

| 효과 | 없음 | 모니터링 |
|------|------|---------|
| **장애 감지** | 늦음 | 빠름 |
| **원인 파악** | 어려움 | 쉬움 |
| **성능** | 불확실 | 가시화 |

### 모범 사례

1. **REDLINE**: SLO/SLA 정의
2. **Golden Signals**: Latency, Traffic, Errors, Saturation
3. **Dashboard**: 팀별 대시보드
4. **Runbook**: 알림 시 조치 매뉴얼

### 미래 전망

1. **AI Anomaly**: 이상 탐지 자동화
2. **Auto-Remediation**: 자동 복구
3. **AIOps**: 인시던트 예측

### ※ 참고 표준/가이드
- **Prometheus**: prometheus.io
- **Grafana**: grafana.com
- **OpenTelemetry**: opentelemetry.io

---

## 📌 관련 개념 맵

- [CI/CD](./10_cicd/36_cicd_tools.md) - 배포 모니터링
- [로깅](./12_logging/38_logging.md) - ELK Stack
- [컨테이너](./9_virtualization/35_container.md) - cAdvisor
