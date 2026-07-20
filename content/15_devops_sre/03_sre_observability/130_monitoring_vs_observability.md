---
title: "Monitoring Vs Observability"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 130
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MELT(Metrics·Events·Logs·Traces)는 관측 가능성의 <strong>4가지 신호</strong>이며, OpenTelemetry(OTel)가 이를 <strong>벤더 중립적으로 통합 수집</strong>하는 CNCF 표준이다.
> 2. **가치**: 과거에는 Prometheus(메트릭)+ELK(로그)+Jaeger(트레이스)를 각각 계측했지만, OTel은 <strong>단일 SDK로 3가지를 동시 수집</strong>하여 통합 관측을 실현한다.
> 3. **판단 포인트**: OTel Collector가 에이전트/게이트웨이로 데이터를 수집·변환·전송하며, 벤더(Datadog·New Relic·Grafana Cloud)에 종속되지 않는 것이 핵심 장점이다.

---

## Ⅰ. 개요 및 필요성

```text
OTel 아키텍처:
  앱 -> OTel SDK -> OTel Collector -> 백엔드
         (자동 계측)   (수집·변환)   (Grafana/Datadog)
```

- **📢 섹션 요약 비유**: OTel은 USB-C 충전기이다. 어떤 기기(벤더)든 <strong>하나의 케이블(OTel)</strong>로 연결된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 신호 | 설명 | 도구 |
|:---|:---|:---|
| <strong>Metrics</strong> | 수치 지표 | Prometheus |
| **Events** | 이벤트 | - |
| <strong>Logs</strong> | 텍스트 기록 | Loki |
| **Traces** | 분산 추적 | Tempo |

---

## Ⅲ~Ⅴ. 결론

OpenTelemetry는 <strong>벤더 종속 없는 관측 가능성의 산업 표준</strong>이며, 모든 CNCF 프로젝트의 관측 기반이 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>OpenTelemetry</strong> | CNCF 관측 표준 |
| <strong>OTel Collector</strong> | 수집·변환·전송 |
| **MELT** | 4가지 관측 신호 |
| <strong>Grafana Stack</strong> | LGTM (Loki+Grafana+Tempo+Mimir) |
| **벤더 중립** | OTel의 핵심 가치 |

### 📈 관련 키워드 및 발전 흐름도

```text
[OpenTracing + OpenCensus (2016~)] -> [OpenTelemetry 통합 (2019)]
    -> [OTel GA (2023, Traces+Metrics)]
    -> [OTel Logs GA (2024)]
    -> [현재: OTel Profiling — 프로파일링까지 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. OpenTelemetry는 <strong>만능 충전기(USB-C)</strong>예요. 어떤 벤더(기기)든 <strong>하나로 연결</strong>돼요.
2. 예전에는 메트릭·로그·트레이스마다 <strong>다른 충전기</strong>가 필요했어요.
3. OTel 덕분에 <strong>하나의 도구</strong>로 모든 관측 데이터를 모을 수 있답니다!
