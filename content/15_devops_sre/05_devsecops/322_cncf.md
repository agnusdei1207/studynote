---
title: "OpenTelemetry CNCF"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 322
---
> **핵심 인사이트**
> - OpenTelemetry (OTel)는 Metrics·Logs·Traces 세 기둥을 단일 SDK로 계측하는 CNCF (Cloud Native Computing Foundation) 표준이다.
> - 벤더 중립적 설계로 Jaeger·Prometheus·Datadog 등 어떤 백엔드에도 연결할 수 있다.
> - OTel Collector가 파이프라인 중앙에서 수신·처리·내보내기를 담당해 언어별 SDK 변경 없이 백엔드를 교체할 수 있다.

---

## Ⅰ. OpenTelemetry 등장 배경

이전에는 Observability 도구마다 별도 SDK를 사용해야 했다. OpenTelemetry는 OpenCensus(Google)와 OpenTracing(CNCF)의 합병 프로젝트로, 단일 표준 SDK로 Metrics·Logs·Traces 모두 계측한다.

```
+--------------------------------------------------+
|           OpenTelemetry 아키텍처                |
|                                                  |
|  앱 -> OTel SDK -> OTLP -> OTel Collector          |
|                             |                   |
|                    +--------+--------+           |
|                    v        v        v           |
|                 Jaeger  Prometheus  Loki         |
+--------------------------------------------------+
```

> 📢 **Ⅰ 섹션 요약 비유**
> OTel은 USB-C 표준 — 기기(SDK)는 하나의 포트에 연결하고, 어댑터(Exporter)를 교체하면 다른 충전기(백엔드)에 꽂힌다.

---

## Ⅱ. OTel SDK 주요 구성

| 구성 요소         | 역할                                        |
|------------------|---------------------------------------------|
| Tracer Provider   | Trace 생성 팩토리                           |
| Meter Provider    | Metrics 수집 팩토리                         |
| Logger Provider   | 구조화 로그 출력 팩토리                      |
| Propagator        | Trace Context 서비스 간 전파                |
| Exporter          | 데이터 백엔드로 전송 (OTLP, Jaeger, Zipkin) |

OTLP (OpenTelemetry Protocol)는 gRPC·HTTP 기반 표준 전송 프로토콜이다.

> 📢 **Ⅱ 섹션 요약 비유**
> Tracer Provider는 GPS 모듈, Meter Provider는 속도계, OTLP는 데이터를 서버로 보내는 통신망이다.

---

## Ⅲ. OTel Collector 파이프라인

```
Receiver -> Processor -> Exporter

OTLP Receiver
  +-- Batch Processor (배치 압축)
  +-- Attributes Processor (태그 추가/제거)
  +-- Jaeger Exporter (Trace)
  +-- Prometheus Exporter (Metrics)
  +-- Loki Exporter (Logs)
```

Agent 모드(사이드카/데몬셋)와 Gateway 모드(클러스터 중앙 집결)를 조합해 사용한다.

> 📢 **Ⅲ 섹션 요약 비유**
> Collector는 우편 허브 — 여러 곳에서 온 소포를 분류·처리해 목적지별로 배달한다.

---

## Ⅳ. Auto-Instrumentation

코드 수정 없이 자동 계측:

```bash
# Java
java -javaagent:opentelemetry-javaagent.jar -jar myapp.jar

# Python
opentelemetry-instrument python myapp.py
```

Auto-instrumentation은 HTTP 클라이언트·DB 드라이버·메시지 큐 등 인기 라이브러리를 자동 계측한다.

> 📢 **Ⅳ 섹션 요약 비유**
> Auto-instrumentation은 자동차 OBD 포트에 꽂기만 하면 모든 주행 데이터를 수집하는 것이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소           | 역할                                         |
|---------------------|----------------------------------------------|
| OpenTelemetry       | Observability 표준 SDK + 프로토콜             |
| CNCF                | Cloud Native 오픈소스 프로젝트 관리 재단      |
| OTLP                | OTel 표준 전송 프로토콜 (gRPC/HTTP)          |
| OTel Collector      | 수신·처리·내보내기 파이프라인                |
| Auto-instrumentation| 코드 수정 없는 자동 계측                     |
| Propagator          | 서비스 간 Trace Context 전파                 |

### 관련 키워드 및 발전 흐름도

```
OpenTelemetry
    +-- SDK -> Metrics / Logs / Traces 계측
    +-- OTLP -> 표준 전송 프로토콜
    +-- Collector -> 중앙 파이프라인 (Agent + Gateway)
    +-- Auto-instrumentation -> 코드리스 계측
    +-- CNCF -> Cloud Native 표준화
```

> 🧒 **어린이 비유**
> OTel은 모든 가전제품의 리모컨을 하나로 통합하는 만능 리모컨이에요. 어떤 TV(백엔드)에도 같은 버튼(SDK)으로 조종할 수 있어요.
