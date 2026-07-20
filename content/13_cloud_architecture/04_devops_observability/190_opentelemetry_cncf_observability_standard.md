---
title: "OpenTelemetry, CNCF"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 190
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OpenTelemetry(OTel)는 메트릭, 로그, 트레이스(MELT의 M·L·T) 데이터를 생성·수집·전송하는 벤더 중립 CNCF(Cloud Native Computing Foundation, 클라우드 네이티브 컴퓨팅 재단) 오픈소스 표준으로, "한 번 계측하면 어떤 백엔드로도 전송 가능"한 옵저버빌리티 인프라 표준이다.
> 2. **가치**: 벤더 종속(Vendor Lock-in)을 방지하여 Datadog에서 Prometheus/Jaeger로 또는 그 반대로 언제든 백엔드를 교체할 수 있으며, 자동 계측으로 코드 수정 없이 대부분의 프레임워크에 트레이스·메트릭을 즉시 추가할 수 있다.
> 3. **판단 포인트**: OTel SDK + OTel Collector 조합이 현재 최선의 아키텍처이며, Collector를 중간에 두어 백엔드를 결합·분기·필터링하는 파이프라인을 유연하게 구성할 수 있다.

---

## Ⅰ. 개요 및 필요성

분산 추적의 초기 시대에는 Jaeger, Zipkin, Datadog APM 등 각 도구가 자체 SDK를 제공했다. 회사가 Datadog을 쓰다가 Jaeger로 교체하려면 모든 서비스의 계측 코드를 다시 작성해야 했다. 이것이 벤더 종속 문제다.

OpenTracing(오픈 추적)과 OpenCensus(오픈 센서스) 두 경쟁 표준이 존재하다가, 2019년 두 프로젝트가 합쳐져 OpenTelemetry(오픈텔레메트리)가 탄생했다. 2023년 CNCF 졸업 프로젝트로 승격되며 사실상 업계 표준이 되었다.

OTel의 설계 철학은 "수집(Instrumentation)과 저장(Backend)의 분리"다. 애플리케이션은 OTel SDK로 데이터를 생성하고, OTel Collector가 수집·처리하여 여러 백엔드(Prometheus, Jaeger, Datadog 등)로 동시에 전송할 수 있다. 백엔드를 교체해도 애플리케이션 코드는 바꿀 필요가 없다.

📢 **섹션 요약 비유**: OTel은 USB Type-C 표준이다. 표준 케이블 하나로 충전기, 모니터, 스토리지를 모두 연결하듯, OTel SDK 하나로 Prometheus, Jaeger, Datadog 등 어떤 백엔드에도 연결된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### OTel 전체 아키텍처

```
[애플리케이션 계측]
서비스 코드
+-- OTel Java/Python/Go SDK
|   +-- 자동 계측 (Auto-instrumentation)
|   |   +-- HTTP, DB, gRPC 자동 Span 생성
|   +-- 수동 계측 (Manual)
|       +-- 비즈니스 로직 커스텀 Span
|
v OTLP (OpenTelemetry Protocol) gRPC/HTTP
|
[수집 파이프라인]
OTel Collector
+-- Receivers: OTLP, Jaeger, Zipkin, Prometheus
+-- Processors: 배치, 샘플링, 필터, 보강
+-- Exporters: Prometheus, Jaeger, Datadog, Loki
         |              |           |
         v              v           v
      Prometheus      Jaeger      Datadog
      (메트릭)        (트레이스)   (통합 APM)
```

| OTel 구성 요소 | 설명 |
|:---|:---|
| OTel SDK | 언어별 계측 라이브러리 (Java, Python, Go, JS 등) |
| Auto-instrumentation | 에이전트/바이트코드 조작으로 코드 수정 없이 계측 |
| OTLP | OpenTelemetry Line Protocol, OTel 전용 전송 프로토콜 |
| OTel Collector | 수집·처리·내보내기 파이프라인 |
| Resource | 서비스명, 버전, 환경 등 메타데이터 |

📢 **섹션 요약 비유**: OTel Collector는 물류 터미널이다. 다양한 공급처(SDK)에서 화물(텔레메트리)을 받아 분류하고, 여러 목적지(Prometheus, Jaeger, Datadog)로 동시에 배송한다.

---

## Ⅲ. 비교 및 연결

### OTel vs 이전 표준·도구

| 항목 | OpenTracing | OpenCensus | OpenTelemetry |
|:---|:---|:---|:---|
| 상태 | 아카이브 | 아카이브 | 현재 표준 |
| 범위 | 추적만 | 추적 + 메트릭 | 추적 + 메트릭 + 로그 |
| 벤더 중립 | ✅ | ✅ | ✅ |
| CNCF 상태 | 아카이브 | 아카이브 | 졸업 (2023) |

<strong>OTel Collector 설정 예시 (YAML):</strong>
```yaml
receivers:
  otlp:
    protocols:
      grpc: {endpoint: "0.0.0.0:4317"}
      http: {endpoint: "0.0.0.0:4318"}

processors:
  batch:
    timeout: 5s
  tail_sampling:
    policies: [{name: errors, type: status_code, status_code: {status_codes: [ERROR]}}]

exporters:
  prometheus:
    endpoint: "0.0.0.0:8888"
  jaeger:
    endpoint: "jaeger:14250"
  datadog:
    api:
      key: ${DD_API_KEY}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [jaeger, datadog]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

📢 **섹션 요약 비유**: OTel Collector 설정은 회사 메일 서버 규칙이다. "받은 메일 중 'ERROR' 포함된 것은 Slack에도 보내고, 모든 메일은 아카이브에 저장"처럼 데이터 흐름을 코드로 정의한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**언어별 자동 계측 방법:**

```bash
# Java (에이전트 방식)
java -javaagent:opentelemetry-javaagent.jar \
     -Dotel.service.name=my-service \
     -Dotel.exporter.otlp.endpoint=http://collector:4317 \
     -jar app.jar

# Python (SDK 방식)
pip install opentelemetry-sdk opentelemetry-instrumentation-flask
opentelemetry-instrument python app.py

# Node.js
npm install @opentelemetry/auto-instrumentations-node
node -r @opentelemetry/auto-instrumentations-node app.js
```

<strong>쿠버네티스 배포 전략:</strong>
- <strong>DaemonSet Collector</strong>: 각 노드에 배포, 노드 메트릭 수집
- <strong>Sidecar Collector</strong>: Pod마다 배포, 세밀한 필터링
- **Gateway Collector**: 중앙 집중, 외부 전송 전 처리

**Semantic Conventions(시맨틱 컨벤션):**
- OTel이 정의한 표준 속성명 규약
- `http.method`, `db.system`, `net.peer.port` 등
- 일관된 속성명으로 여러 서비스의 트레이스 비교 용이

📢 **섹션 요약 비유**: Semantic Conventions는 국제 도량형 표준이다. "1kg"가 전 세계에서 같은 무게를 의미하듯, `http.method=GET`이 모든 서비스에서 동일한 의미를 가지도록 표준화한다.

---

## Ⅴ. 기대효과 및 결론

OpenTelemetry 도입은 옵저버빌리티 인프라의 장기 투자 관점에서 필수적이다. 표준 SDK를 사용하면 어떤 백엔드 도구를 선택해도 재계측 없이 전환이 가능하여 도구 선택의 자유도가 극적으로 높아진다.

자동 계측의 가치는 초기 도입 비용을 획기적으로 낮춘다는 데 있다. Spring Boot, Django, Express.js 같은 주류 프레임워크는 OTel 에이전트 하나로 수십 개의 자동 Span이 생성되어, 개발자가 첫 날부터 트레이스를 볼 수 있다.

미래 전망으로 OTel은 로그 지원도 성숙되고 있어 MELT 전체를 하나의 표준 SDK로 다루는 날이 가까워지고 있다. 옵저버빌리티의 통합 표준으로서 OTel의 중요성은 계속 커질 것이다.

📢 **섹션 요약 비유**: OpenTelemetry는 전 세계 공통 언어다. 개발자가 영어(OTel SDK)로 한 번 작성하면 프랑스어, 중국어, 스페인어(Prometheus, Jaeger, Datadog) 사용자 모두와 소통할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| 옵저버빌리티 | OTel이 MELT 수집의 표준 인프라 |
| OTLP | OTel 전용 데이터 전송 프로토콜 |
| OTel Collector | 수집·처리·분기의 중앙 파이프라인 |
| 벤더 중립성 | OTel의 핵심 가치, 백엔드 교체 자유 |
| Semantic Conventions | 표준 속성명 규약으로 일관성 보장 |
| 자동 계측 | 코드 수정 없이 Span·메트릭 자동 생성 |

### 👶 어린이를 위한 3줄 비유 설명
1. OpenTelemetry는 전 세계 어디서나 쓸 수 있는 만능 어댑터예요.

### 📈 관련 키워드 및 발전 흐름도

```text
벤더별 전용 SDK (Jaeger SDK · Datadog SDK -> 벤더 종속)
    |
    v
OpenTelemetry (OTel): CNCF 표준
    +-► SDK: 언어별 자동 계측 (Auto-instrumentation)
    +-► Collector: 수집 · 처리 · 라우팅
    +-► OTLP: 오픈 프로토콜
    |
    v
백엔드 선택 자유: Jaeger · Grafana · Datadog · Splunk
```
2. 한 번 계측(plug-in)해두면 Prometheus, Jaeger, Datadog 어디에든 연결할 수 있어요.
3. 덕분에 더 좋은 도구가 나와도 처음부터 다시 만들 필요 없이 쉽게 바꿀 수 있어요!
