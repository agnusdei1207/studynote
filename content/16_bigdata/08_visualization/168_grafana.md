---
title: "Grafana"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 168
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Grafana는 메트릭(Metrics)·로그(Logs)·추적(Traces)의 3대 관측성(Observability) 기둥을 단일 UI에서 통합 시각화하는 플랫폼으로, LGTM 스택(Loki+Grafana+Tempo+Mimir)을 통해 완전한 오픈소스 관측성 환경을 구성할 수 있다.
- **가치**: Prometheus의 PromQL로 쿠버네티스 클러스터 메트릭, Loki의 LogQL로 애플리케이션 로그, Tempo로 분산 추적을 하나의 Grafana 대시보드에서 상관 분석하여 장애 근본 원인을 분 단위로 파악할 수 있다.
- **판단 포인트**: Grafana는 BI(비즈니스 인텔리전스)가 아닌 운영 관측성(Operational Observability) 도구이므로, 비즈니스 KPI 대시보드에는 Tableau/Power BI가, 인프라·애플리케이션 모니터링에는 Grafana가 각각 더 적합하다.

---

## Ⅰ. 개요 및 필요성

### 관측성(Observability)의 3대 기둥

마이크로서비스, 쿠버네티스, 분산 시스템에서 "왜 서비스가 느린가?"를 파악하려면 3가지 신호가 필요하다:

```
관측성 3대 기둥:
+------------------------------------------------------+
|  1. 메트릭 (Metrics)                                 |
|     - CPU, 메모리, 요청 수, 응답 시간, 오류율         |
|     - 시계열 데이터 (시간 + 숫자값)                   |
|     - "무슨 일이 일어나고 있나?" -> 양적 측정           |
|                                                      |
|  2. 로그 (Logs)                                      |
|     - 애플리케이션 이벤트 기록 (ERROR, INFO, WARN)    |
|     - 비정형 텍스트 + 타임스탬프                      |
|     - "왜 이런 일이 일어났나?" -> 상세 이유             |
|                                                      |
|  3. 추적 (Traces)                                    |
|     - 분산 서비스 간 요청 흐름 추적                   |
|     - Span 연결 (A서비스 -> B서비스 -> DB 순서)         |
|     - "어디서 느렸나?" -> 병목 위치 식별               |
+------------------------------------------------------+
```

**📢 섹션 요약 비유**: 관측성 3기둥은 **자동차 계기판·블랙박스·GPS** 조합과 같다. 계기판(메트릭)으로 이상을 감지하고, 블랙박스(로그)로 원인을 파악하며, GPS(추적)로 어느 경로에서 문제가 생겼는지 추적한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LGTM 스택 아키텍처

```
+--------------------------------------------------------------+
|                     LGTM 스택 구조                           |
+--------------------------------------------------------------+
|                                                              |
|  데이터 수집                                                 |
|  +------------+--------------+-----------------------------+ |
|  |Prometheus  | Promtail/    | OpenTelemetry / Jaeger /    | |
|  |(메트릭 수집)| Fluentbit   | Zipkin                      | |
|  |Pull 기반   | (로그 수집)  | (추적 데이터 수집)           | |
|  +-----+------+------+-------+--------------+--------------+ |
|        |             |                       |               |
|  저장  v             v                       v               |
|  +----------+  +----------+  +--------------------------+   |
|  |  Mimir   |  |  Loki    |  |         Tempo            |   |
|  |(메트릭   |  |(로그     |  |(추적 데이터 저장)          |   |
|  | 장기저장)|  | 집계·저장)|  |TraceQL 쿼리 지원          |   |
|  +----------+  +----------+  +--------------------------+   |
|        |             |                       |               |
|  시각화 v             v                       v               |
|  +--------------------------------------------------------+  |
|  |                    Grafana UI                          |  |
|  |  PromQL / LogQL / TraceQL 통합 쿼리                    |  |
|  |  Explore, Dashboard, Alerting                         |  |
|  +--------------------------------------------------------+  |
+--------------------------------------------------------------+
```

### 핵심 쿼리 언어 비교

| 언어 | 데이터 소스 | 주요 용도 |
|:---|:---|:---|
| **PromQL** | Prometheus, Mimir | 메트릭 쿼리·집계·알림 |
| **LogQL** | Loki | 로그 필터링·패턴 추출 |
| **TraceQL** | Tempo | 추적 검색·필터링 |

```
PromQL 예시:
  # 5분 평균 CPU 사용률 (전체 서비스)
  avg(rate(cpu_usage_seconds_total[5m])) by (service)

  # 오류율 > 5% 서비스 필터
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) > 0.05

LogQL 예시:
  # 에러 로그만 필터
  {app="api-server"} |= "ERROR"

  # 분당 오류 발생 건수
  count_over_time({app="api-server"} |= "ERROR" [1m])
```

**📢 섹션 요약 비유**: LGTM 스택은 <strong>병원 종합 진단 시스템</strong>과 같다. 혈압계(Prometheus 메트릭), 의무기록(Loki 로그), 내시경 카메라(Tempo 추적)가 모두 하나의 모니터(Grafana)에 표시되어 의사(엔지니어)가 종합 진단한다.

---

## Ⅲ. 비교 및 연결

### Grafana vs Kibana 비교

| 차원 | Grafana | Kibana |
|:---|:---|:---|
| **주 용도** | 다중 소스 메트릭·관측성 | Elasticsearch 로그 분석 |
| <strong>데이터 소스</strong> | 다수 (Prometheus, Loki, InfluxDB, 등) | Elasticsearch 전용 |
| **강점** | 멀티소스 통합, 메트릭 시각화 | 전문 로그 검색, SIEM |
| **ML 기능** | 기본 이상 감지 | Elastic ML (고급) |
| **무료 수준** | 오픈소스 전체 | 기본 기능 (고급은 유료) |

### Grafana k6: 부하 테스트 통합

Grafana k6는 JavaScript 기반 부하 테스트 도구로, 테스트 결과를 Grafana 대시보드로 실시간 시각화한다:

```javascript
// k6 테스트 스크립트
import http from 'k6/http';
export const options = { vus: 100, duration: '30s' };
export default function() {
  const res = http.get('https://api.example.com/products');
  check(res, { 'status was 200': (r) => r.status == 200 });
}
```

**📢 섹션 요약 비유**: Grafana + k6의 조합은 <strong>의사 + 스트레스 테스트 장비</strong>와 같다. 부하 테스트(스트레스 테스트)를 수행하면서 실시간으로 시스템 반응(Grafana 대시보드)을 모니터링하여 한계점을 파악한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 쿠버네티스 모니터링 스택

```
쿠버네티스 표준 모니터링 스택:
  kube-state-metrics: K8s 오브젝트 상태 노출
  node-exporter: 노드 수준 메트릭 (CPU, 메모리, 디스크)
  Prometheus: 메트릭 수집 + 저장 (Pull 방식)
  Grafana: 시각화

  주요 대시보드:
  - Cluster Overview: 전체 클러스터 리소스 현황
  - Node Exporter Full: 노드별 상세 메트릭
  - Pod/Deployment: 워크로드별 CPU/메모리
  - Kubernetes Events: 이벤트 로그 연동

  커뮤니티 대시보드: grafana.com/grafana/dashboards/
  (ID 번호로 바로 가져오기 가능)
```

### Grafana Alerting

```yaml
# 알림 규칙 예시
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m])) > 0.05
  for: 5m  # 5분 이상 지속 시 발화
  annotations:
    summary: "서비스 오류율 5% 초과"
    description: "{{ $labels.service }} 오류율: {{ $value | humanizePercentage }}"
  labels:
    severity: critical
```

알림 채널: Slack, PagerDuty, OpsGenie, 이메일, Webhook

**📢 섹션 요약 비유**: Grafana Alerting은 <strong>화재경보기</strong>와 같다. 정상 범위(임계값)를 벗어나는 순간 경보가 울리고, 담당자에게 즉시 알림이 전달된다. 경보 기준(임계값)은 미리 정의한다.

---

## Ⅴ. 기대효과 및 결론

### Grafana 도입 효과

| 영역 | 효과 |
|:---|:---|
| <strong>MTTR 단축</strong> | Mean Time To Recover — 장애 원인 파악 시간 대폭 단축 |
| **관측성** | 메트릭·로그·추적 통합으로 전체 시스템 상태 파악 |
| **비용** | 오픈소스 + 클라우드 관리형 Grafana Cloud 선택 가능 |
| **표준화** | 전사 모니터링 플랫폼 단일화 |

### 결론

Grafana는 <strong>클라우드 네이티브 시대의 표준 관측성 플랫폼</strong>이다. 마이크로서비스와 쿠버네티스 환경에서 시스템의 "건강 상태"를 지속적으로 모니터링하고, 이상 감지 시 즉각 대응할 수 있는 가시성을 제공한다. 시스템 설계는 LGTM 스택의 각 컴포넌트 역할과 PromQL 기반 알림 설계를 이해하고 클라우드 인프라 모니터링 아키텍처 설계에 적용할 수 있어야 한다.

**📢 섹션 요약 비유**: Grafana가 있는 엔지니어링 팀은 <strong>항공 관제사가 있는 공항</strong>과 같다. 관제사(Grafana)가 모든 비행기(서비스)의 상태를 실시간으로 파악하고, 이상이 감지되면 즉각 대응하여 충돌(장애)을 방지한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Prometheus | 메트릭 데이터 소스 | Pull 방식 시계열 메트릭 수집·저장 |
| Loki | 로그 데이터 소스 | 수평 확장 로그 집계, LogQL 쿼리 |
| Tempo | 추적 데이터 소스 | 분산 추적 백엔드, TraceQL |
| Mimir | Prometheus 확장 | 멀티테넌트 고가용성 Prometheus |
| LGTM 스택 | 통합 관측성 | Loki+Grafana+Tempo+Mimir |
| PromQL | 쿼리 언어 | Prometheus 메트릭 쿼리 언어 |
| Grafana k6 | 부하 테스트 | JavaScript 기반 부하 테스트 + Grafana 통합 |
| Kibana | 비교 도구 | Elasticsearch 특화 로그 분석 시각화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[메트릭 수집 (Metrics) — Prometheus Pull 방식]
    |
    v
[로그 집계 (Log Aggregation) — Loki]
    |
    v
[분산 추적 (Distributed Tracing) — Tempo]
    |
    v
[Grafana 대시보드 — 통합 관측성 (Unified Observability)]
    |
    v
[LGTM 스택 (Loki + Grafana + Tempo + Mimir)]
```

관측성 기술이 개별 메트릭·로그·추적을 통합하여 Grafana 중심의 단일 가시성 플랫폼으로 수렴한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

- Grafana는 <strong>병원 중환자실 모니터</strong>예요: 환자(서버·서비스)의 심장 박동(CPU), 혈압(메모리), 체온(오류율)이 실시간으로 표시되고, 이상이 생기면 경보가 울려요.
- LGTM 스택은 <strong>의료 검사 세트</strong>예요: 혈액 검사(메트릭), 의무기록(로그), 내시경(추적) 세 가지가 함께 있어야 의사가 정확한 진단을 내릴 수 있어요.
- PromQL은 <strong>의료 데이터를 묻는 질문 형식</strong>이에요: "지난 5분간 심장 박동이 100을 넘었나?"처럼 복잡한 질문을 짧은 수식으로 표현해요.
