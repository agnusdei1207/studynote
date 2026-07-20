---
title: "Context Propagation Trace Id"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 144
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Context Propagation은 <strong>Trace ID·Span ID·Baggage를 HTTP 헤더·gRPC 메타데이터·메시지 큐 속성으로 서비스 간 전파</strong>하여, 분산 요청의 전체 호출 체인을 하나의 Trace로 연결하는 메커니즘이다.
> 2. **가치**: 전파가 없으면 각 서비스의 로그·메트릭이 <strong>독립적으로 분산</strong>되어 상관 분석이 불가능하지만, Trace ID 전파로 <strong>Metrics↔Logs↔Traces 3축 상관</strong>이 가능해진다.
> 3. **판단 포인트**: W3C traceparent(표준)·B3(Zipkin 레거시)·Jaeger 헤더의 3가지 형식이 있으며, OTel SDK가 자동 전파를 제공한다. 비동기(Kafka)에서는 메시지 헤더로 전파한다.

---

## Ⅰ. 개요 및 필요성

```text
HTTP: traceparent: 00-{traceId}-{spanId}-{flags}
gRPC: metadata에 traceparent 포함
Kafka: message header에 traceparent 포함
자동 전파: OTel SDK -> HTTP Client 인터셉터
```

- **📢 섹션 요약 비유**: Context Propagation은 <strong>여권</strong>이다. 각 나라(서비스)를 방문할 때 여권(Trace ID)을 찍어 <strong>방문 이력</strong>을 추적한다.

---

## Ⅱ~Ⅴ. 결론

Context Propagation은 <strong>Observability 3축 통합의 핵심</strong>이며, W3C traceparent+OTel SDK가 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Propagation** | 컨텍스트 전파 |
| **traceparent** | W3C 표준 |
| <strong>OTel SDK</strong> | 자동 전파 |
| **Baggage** | 사용자 정의 전파 |
| <strong>Kafka 헤더</strong> | 비동기 전파 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 헤더 전달 (~2015)] -> [B3 (Zipkin)]
    -> [W3C Trace Context (2020)]
    -> [OTel Auto-instrumentation (2021)]
    -> [현재: 자동 전파 + Baggage 표준화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Context Propagation은 <strong>여권</strong>이에요. 나라(서비스)마다 <strong>도장(Span)</strong>을 찍어요.
2. 여권 번호(Trace ID)로 **어디를 방문했는지** 한눈에 볼 수 있어요.
3. OTel SDK가 **자동으로 여권을 넘겨줘서** 개발자가 편해요!
