---
title: "Observability Metrics Logs Traces"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 320
---
> **핵심 인사이트**
> - Observability (관측 가능성)는 Metrics·Logs·Traces 세 기둥(Three Pillars)으로 시스템 내부 상태를 외부에서 추론하는 능력이다.
> - Monitoring(모니터링)은 알고 있는 것을 감시하지만, Observability는 알 수 없는 것도 질문할 수 있게 한다.
> - 분산 시스템에서 단일 지표로는 문제 진단이 불가능하기 때문에 세 기둥의 상관관계 분석이 필수다.

---

## Ⅰ. Three Pillars of Observability

```
+------------------------------------------------------+
|             Observability 세 기둥                   |
|                                                      |
|  Metrics (수치 집계)  Logs (이벤트)  Traces (흐름)  |
|     무엇이               왜              어디서       |
+------------------------------------------------------+
```

| 기둥      | 질문               | 도구 예시                     |
|-----------|-------------------|-------------------------------|
| Metrics   | 무엇이 느린가?     | Prometheus, Datadog           |
| Logs      | 왜 오류가 났나?    | ELK Stack, Loki              |
| Traces    | 어느 서비스 병목?  | Jaeger, Zipkin, Tempo         |

> 📢 **Ⅰ 섹션 요약 비유**
> Metrics는 체중계, Logs는 일기, Traces는 GPS 이동 경로 — 셋이 함께야 건강 상태를 정확히 안다.

---

## Ⅱ. Metrics (메트릭)

4가지 메트릭 유형(Prometheus 기준):

| 타입      | 특성                   | 예시              |
|-----------|------------------------|-------------------|
| Counter   | 단조 증가 카운터        | HTTP 요청 총 수    |
| Gauge     | 오르내리는 현재값       | 메모리 사용량      |
| Histogram | 버킷별 분포 측정        | 응답시간 분포      |
| Summary   | 퀀타일(p50, p99) 계산  | 레이턴시 p99      |

> 📢 **Ⅱ 섹션 요약 비유**
> Counter는 걸음 수 측정기, Gauge는 온도계, Histogram은 성적 분포표다.

---

## Ⅲ. Logs (로그)

구조화 로그(Structured Logging)는 JSON 형식으로 ELK 또는 Loki에서 쿼리·필터링이 쉽다.

```
{timestamp, level, service, trace_id, message, latency_ms}
```

> 📢 **Ⅲ 섹션 요약 비유**
> 구조화 로그는 정형화된 업무 보고서 — 날짜·담당자·결과가 정해진 형식에 맞아야 검색이 빠르다.

---

## Ⅳ. Traces (트레이스)와 Observability 연결

Distributed Tracing은 단일 요청이 여러 서비스를 거치는 경로를 Trace ID로 연결해 시각화한다.

```
User Request -> API Gateway -> Order Svc -> Inventory Svc -> DB
      Trace ID: xyz   Span 1         Span 2           Span 3
```

세 기둥 연결 흐름:
- Alert(Metrics) -> 문제 시간대 특정
- Log 검색 -> 에러 원인 확인
- Trace 시각화 -> 병목 서비스 특정

> 📢 **Ⅳ 섹션 요약 비유**
> 택배 추적 시스템이 Tracing — 어느 물류센터에서 얼마나 지체됐는지 한눈에 보인다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소          | 역할                               |
|--------------------|------------------------------------|
| Observability      | 시스템 내부 상태 외부 추론 능력     |
| Metrics            | 집계 수치 시계열 지표               |
| Logs               | 이벤트 텍스트 기록                 |
| Traces             | 분산 요청 흐름 추적                |
| Prometheus         | 메트릭 수집·저장 오픈소스          |
| ELK / Loki         | 로그 수집·검색 스택                |
| Jaeger / Tempo     | 분산 트레이싱 백엔드               |

### 관련 키워드 및 발전 흐름도

```
Observability
    +-- Metrics -> Prometheus + Grafana
    +-- Logs -> ELK Stack / Loki
    +-- Traces -> Jaeger / Zipkin / Tempo
    +-- OpenTelemetry -> 세 기둥 통합 표준 SDK
```

> 🧒 **어린이 비유**
> 몸이 아플 때 체온계(Metrics)·의사 일지(Logs)·혈액 이동 경로 사진(Traces), 이 세 가지가 있어야 정확한 진단이 가능해요.
