---
title: "Prometheus Grafana Monitoring"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 323
---
> **핵심 인사이트**
> - Prometheus (프로메테우스)는 Pull 방식의 시계열 메트릭 수집 시스템으로, PromQL로 강력한 쿼리가 가능하다.
> - Grafana (그라파나)는 Prometheus·Loki·Tempo를 포함한 다양한 데이터소스를 시각화하는 대시보드 도구다.
> - AlertManager (알럿매니저)가 Prometheus 경보를 라우팅·그룹핑·억제해 On-call 팀에 전달한다.

---

## Ⅰ. Prometheus 아키텍처

```
+----------------------------------------------------+
|               Prometheus 수집 흐름                |
|                                                    |
|  Targets -> /metrics 노출                          |
|                |                                  |
|  Prometheus Server                                |
|  +-- Service Discovery (K8s, Consul, DNS)         |
|  +-- Scrape (15s 주기 Pull)                       |
|  +-- TSDB (시계열 DB) 저장                        |
|  +-- PromQL 쿼리 엔진                             |
|                |                                  |
|  AlertManager -> 경보 라우팅 -> Slack/PagerDuty     |
|  Grafana      -> 대시보드 시각화                   |
+----------------------------------------------------+
```

Pull 방식 장점: 수집 대상이 Push하지 않아도 되므로 보안·관리가 단순하다.

> 📢 **Ⅰ 섹션 요약 비유**
> Prometheus는 각 매장(앱)을 직접 방문해 재고를 확인하는 본사 재고 관리팀 — 매장이 보고하는 게 아니라 본사가 직접 온다.

---

## Ⅱ. PromQL (Prometheus Query Language)

```promql
# HTTP 오류율
rate(http_requests_total{status=~"5.."}[5m])
/ rate(http_requests_total[5m])

# p99 응답시간
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m]))
```

| 함수                 | 용도                          |
|----------------------|-------------------------------|
| rate()               | Counter의 초당 증가율          |
| increase()           | 구간 내 증가량                |
| histogram_quantile() | Histogram에서 퀀타일 계산     |
| avg_over_time()      | 구간 평균                     |

> 📢 **Ⅱ 섹션 요약 비유**
> PromQL은 시계열 데이터를 위한 Excel 수식 — rate()는 변화율 계산, histogram_quantile()은 분포에서 특정 백분위를 뽑는다.

---

## Ⅲ. AlertManager 경보 관리

AlertManager 주요 기능:
- <strong>Grouping</strong>: 동일 알람을 묶어 알림 폭탄 방지
- **Inhibition**: 심각 알람 발생 시 관련 경고 알람 억제
- **Silencing**: 점검 시간 동안 특정 알람 무음 처리

> 📢 **Ⅲ 섹션 요약 비유**
> AlertManager는 비서 — 중요한 연락만 사장에게 보고하고, 관련 없는 알람은 묶거나 조용히 처리한다.

---

## Ⅳ. Grafana 대시보드 구성

Grafana는 플러그인 기반으로 다양한 데이터소스를 지원한다:
- Prometheus (Metrics), Loki (Logs), Tempo (Traces), Elasticsearch, InfluxDB

**Exemplar**: 메트릭 데이터 포인트에 연결된 Trace ID — Grafana에서 메트릭 -> 트레이스 직접 드릴다운이 가능하다.

```
Grafana
  |
  +-- CPU 급등 감지 (Prometheus)
  |       +-- Exemplar 클릭 -> Trace ID -> Tempo 드릴다운
  +-- 관련 에러 로그 (Loki)
```

> 📢 **Ⅳ 섹션 요약 비유**
> Grafana는 항공 관제탑 모니터 — 레이더(Prometheus), 통신 기록(Loki), 항적 추적(Tempo)을 한 화면에서 본다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소        | 역할                                    |
|------------------|-----------------------------------------|
| Prometheus       | Pull 방식 메트릭 수집·저장·쿼리         |
| PromQL           | 시계열 쿼리 언어                        |
| AlertManager     | 경보 라우팅·억제·그룹핑                 |
| Grafana          | 다중 데이터소스 시각화 대시보드          |
| Exemplar         | 메트릭-트레이스 연결 드릴다운 포인트    |
| Push Gateway     | 배치 잡 메트릭 Push 수집 게이트웨이     |

### 관련 키워드 및 발전 흐름도

```
Prometheus + Grafana
    +-- PromQL -> 강력한 시계열 쿼리
    +-- AlertManager -> 경보 라우팅·억제
    +-- Grafana Loki -> 로그 통합 시각화
    +-- Grafana Tempo -> 트레이스 통합
    +-- Exemplar -> Metrics-to-Trace 드릴다운
```

> 🧒 **어린이 비유**
> Prometheus는 학교 성적 기록부, Grafana는 그 성적을 예쁜 그래프로 그려주는 프로그램이에요. AlertManager는 성적이 떨어지면 부모님께 문자를 보내는 시스템이에요.
