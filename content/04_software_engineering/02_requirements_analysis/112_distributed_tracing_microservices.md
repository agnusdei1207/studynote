---
title: "Distributed Tracing Microservices"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 112
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 트레이싱은 MSA 환경에서 하나의 사용자 요청이 <strong>N개 서비스를 거치는 전체 경로(Trace)</strong>를 고유 ID(Trace ID)로 추적하고, 각 서비스 내 처리 구간(Span)의 <strong>레이턴시·에러를 시각화</strong>하여 병목을 특정하는 기법이다.
> 2. **가치**: 모놀리스에서는 하나의 스택트레이스로 디버깅이 가능하지만, MSA에서는 "주문->결제->배송->알림" 4개 서비스 중 **어디서 500ms가 추가됐는지** 찾는 것 자체가 난제이며, 분산 트레이싱이 유일한 해법이다.
> 3. **판단 포인트**: OpenTelemetry(OTel)가 CNCF 표준으로 계측(Instrumentation)을 통일하고, Jaeger·Tempo·Zipkin이 백엔드 저장·시각화를 담당하며, <strong>Context Propagation(W3C Trace Context)</strong>으로 서비스 간 Trace ID를 전파한다.

---

## Ⅰ. 개요 및 필요성

MSA에서 API Gateway -> Auth -> Order -> Payment -> Notification으로 이어지는 요청 체인에서, 전체 응답이 2초 걸린다. "어디서 느린가?"를 찾으려면 각 서비스의 로그를 일일이 시간순으로 대조해야 한다.

```text
+-------------------------------------------------------+
|      분산 트레이싱 Trace/Span 구조                     |
+-------------------------------------------------------+
|  Trace ID: abc-123 (전체 요청 1건)                    |
|  +- Span 1: API Gateway    [0ms --- 50ms]            |
|  +- Span 2: Auth Service   [50ms -- 100ms]           |
|  +- Span 3: Order Service  [100ms - 800ms] <- 병목!  |
|  |   +- Span 3.1: DB Query [200ms - 750ms] <- 원인!  |
|  +- Span 4: Payment        [800ms - 1200ms]          |
|  +- Span 5: Notification   [1200ms - 1250ms]         |
|  총 응답: 1250ms                                      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Trace ID는 택배 송장번호이고, 각 Span은 물류 허브(서비스)에서의 체류 시간이다. 송장을 추적하면 어느 허브에서 택배가 멈췄는지 즉시 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념

| 개념 | 정의 | 비유 |
|:---|:---|:---|
| **Trace** | 하나의 요청이 거치는 전체 경로 | 택배 배송 전체 경로 |
| **Span** | Trace 내 하나의 서비스 처리 구간 | 물류 허브 1곳에서의 체류 |
| <strong>Trace ID</strong> | 전체 Trace를 식별하는 고유 ID | 택배 송장번호 |
| **Span ID** | 개별 Span을 식별하는 ID | 허브별 스캔 바코드 |
| <strong>Context Propagation</strong> | HTTP 헤더로 Trace ID를 서비스 간 전파 | 송장을 다음 허브로 넘기기 |

### Context Propagation 방식

W3C Trace Context 표준: HTTP 헤더 `traceparent: 00-{trace-id}-{span-id}-{flags}`를 요청에 실어 다음 서비스로 전달한다.

- **📢 섹션 요약 비유**: Context Propagation은 릴레이 경주에서 바통(Trace ID)을 다음 주자(서비스)에게 넘기는 것이다. 바통을 놓치면 추적이 끊긴다.

---

## Ⅲ. 비교 및 연결

| 비교 | 로그 (Logs) | 메트릭 (Metrics) | 트레이싱 (Traces) |
|:---|:---|:---|:---|
| **질문** | 무엇이 일어났나? | 얼마나 나쁜가? | **어디서 병목인가?** |
| **형태** | 텍스트 이벤트 | 시계열 수치 | Span 트리 |
| <strong>MSA 대응</strong> | 서비스별 분산 | 서비스별 집계 | **전체 경로 추적** |
| **도구** | ELK, Loki | Prometheus | Jaeger, Tempo |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 도입 체크리스트
1. <strong>OTel SDK 계측</strong>: 각 서비스에 OpenTelemetry SDK 추가 (Auto-instrumentation 권장).
2. **Collector 배포**: OTel Collector를 사이드카 또는 DaemonSet으로 배포하여 Span 수집.
3. **백엔드 선택**: Jaeger(분석)·Tempo(비용 효율)·Datadog(SaaS).
4. <strong>샘플링 전략</strong>: 전량 수집은 비용 폭발 -> Head-based 또는 Tail-based 샘플링.

### 안티패턴
- **샘플링 없이 전량 수집**: 초당 10,000 요청 × 5 Span = 50,000 Span/s -> 저장 비용 폭발.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 트레이싱 미도입 | 트레이싱 도입 | 개선 |
|:---|:---|:---|:---|
| 병목 특정 시간 | 수시간 (로그 대조) | <strong>수분 (Span 시각화)</strong> | 90% 단축 |
| MTTR (복구 시간) | 30분+ | **10분 이하** | 66% 단축 |
| 서비스 간 의존성 가시성 | 문서 기반 | <strong>자동 서비스 맵</strong> | 실시간 |

분산 트레이싱은 eBPF 기반 무계측(Zero-instrumentation) 추적과 결합하여, 코드 변경 없이 커널 레벨에서 Span을 자동 생성하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>OpenTelemetry</strong> | 계측 표준, Metrics·Logs·Traces 통합 SDK |
| **Jaeger / Tempo** | 트레이싱 백엔드 (저장·시각화) |
| <strong>W3C Trace Context</strong> | 서비스 간 Trace ID 전파 표준 헤더 |
| <strong>Observability</strong> | 트레이싱이 속하는 3대 신호 중 하나 |
| <strong>Service Mesh (Istio)</strong> | 사이드카 프록시가 자동으로 Span 생성 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Google Dapper 논문 (2010) — 분산 트레이싱 개념 정립]
    |
    v
[Zipkin (2012, Twitter) — 최초 OSS 분산 트레이싱]
    |
    v
[Jaeger (2017, Uber) — CNCF 졸업 프로젝트]
    |
    v
[OpenTelemetry 통합 (2019~) — OpenTracing+OpenCensus 합병]
    |
    v
[현재: eBPF Zero-instrumentation — 코드 변경 없는 자동 추적]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 택배를 보내면 <strong>송장번호(Trace ID)</strong>로 지금 어디에 있는지 추적할 수 있죠?
2. 분산 트레이싱도 인터넷 요청에 송장번호를 붙여서, **어느 컴퓨터에서 오래 멈췄는지** 찾아내요.
3. 덕분에 개발자가 "아! 여기가 느렸구나!"라고 **바로 고칠 수 있답니다!**
