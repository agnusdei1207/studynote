---
title: "Observability Metrics Logs Traces"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 111
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 관측 가능성(Observability)은 시스템의 <strong>외부 출력(Metrics·Logs·Traces)만으로 내부 상태를 추론</strong>할 수 있는 능력이며, 기존 모니터링(알려진 문제 감시)을 넘어 <strong>"몰랐던 문제(Unknown Unknowns)"까지 진단</strong>하는 패러다임이다.
> 2. **가치**: 3대 신호(Metrics=수치, Logs=이벤트, Traces=요청 경로)를 상호 연결(Correlation)하여, MSA 환경에서 <strong>장애의 근본 원인(Root Cause)을 수분 내 특정 서비스·함수·라인</strong>까지 추적한다.
> 3. **판단 포인트**: OpenTelemetry(OTel)가 CNCF 통합 표준으로 수렴하며, <strong>벤더 종속 없는 계측(Instrumentation)</strong>이 가능해졌다. SRE의 SLI/SLO 체계와 결합하여 장애 대응 자동화의 토대가 된다.

---

## Ⅰ. 개요 및 필요성

모놀리스 시대에는 서버 1대의 CPU·메모리만 보면 됐다. MSA에서는 100개 서비스가 그물망처럼 호출하므로, "어디가 느린지" 찾는 것 자체가 난제다.

```text
+-------------------------------------------------------+
|       Monitoring vs Observability                      |
+-------------------------------------------------------+
|  [Monitoring]                [Observability]           |
|   "CPU 80% 넘으면 알림"      "왜 느린지 추론"          |
|   Known Unknowns 감시        Unknown Unknowns 진단    |
|   대시보드 기반               탐색적 질의(Ad-hoc)      |
|                                                       |
|  3대 신호 (Three Pillars):                            |
|   +---------+  +---------+  +---------+              |
|   | Metrics |  |  Logs   |  | Traces  |              |
|   | (수치)  |  |(이벤트) |  |(경로)   |              |
|   +----+----+  +----+----+  +----+----+              |
|        +------------+------------+                    |
|              Correlation (상관 연결)                   |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 모니터링은 체온계(38도 넘으면 알림), 관측 가능성은 MRI(왜 열이 나는지 내부를 투시)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3대 신호 상세

| 신호 | 정의 | 대표 도구 | 질문 |
|:---|:---|:---|:---|
| <strong>Metrics</strong> | 시계열 수치 (CPU, 레이턴시, 에러율) | Prometheus, Datadog | "얼마나 나쁜가?" |
| <strong>Logs</strong> | 이벤트 텍스트 (에러 스택트레이스) | Loki, ELK | "무엇이 일어났는가?" |
| **Traces** | 분산 요청 경로 (Span 트리) | Jaeger, Tempo | "어디서 병목인가?" |

### OpenTelemetry (OTel)

CNCF가 주도하는 **벤더 중립 계측 표준**. SDK 하나로 Metrics·Logs·Traces를 동시에 수집하고, 백엔드(Prometheus·Jaeger·Datadog)를 자유롭게 교체할 수 있다.

- **📢 섹션 요약 비유**: OTel은 USB-C 충전기다. 삼성이든 애플이든 같은 케이블(SDK)로 충전(계측)할 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 | Monitoring | Observability |
|:---|:---|:---|
| **범위** | 알려진 문제 감시 | 미지의 문제까지 진단 |
| **방식** | 사전 정의 대시보드 | 탐색적 질의 (Ad-hoc) |
| <strong>MSA 대응</strong> | 서비스별 개별 대시보드 | 분산 트레이싱으로 전체 경로 추적 |
| **도구** | Nagios, Zabbix | Prometheus+Jaeger+Loki+OTel |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 관측 가능성 성숙도 체크리스트
1. **Level 1**: 서비스별 Metrics 대시보드 (Grafana).
2. **Level 2**: 중앙 집중 Logs 수집 (ELK/Loki).
3. **Level 3**: 분산 Traces + Metrics 상관 연결.
4. **Level 4**: OTel 통합 + SLI/SLO 기반 자동 알림.

### 안티패턴
- **Logs만 수집하고 Traces 미도입**: "에러가 났다"는 알지만 "어느 서비스에서 시작됐는지" 모름.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 모니터링만 | 관측 가능성 | 개선 |
|:---|:---|:---|:---|
| 장애 원인 특정 시간 | 수시간 | **수분** | 90% 단축 |
| Unknown Unknowns | 감지 불가 | **탐색적 진단** | 신규 역량 |
| 벤더 종속 | 높음 (전용 에이전트) | **OTel로 중립** | 자유도 확보 |

Observability는 AI Ops와 결합하여 "이상 징후 자동 감지 -> 근본 원인 자동 추론 -> 자동 복구"의 자율 운영(Autonomous Operations) 시대를 여는 핵심 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Metrics</strong> | 시계열 수치 데이터, Prometheus 수집 |
| <strong>Logs</strong> | 이벤트 텍스트, ELK/Loki 수집 |
| **Traces** | 분산 요청 경로, Jaeger/Tempo |
| <strong>OpenTelemetry</strong> | 벤더 중립 계측 표준 (CNCF) |
| <strong>SLI/SLO (SRE)</strong> | 관측 데이터를 기반으로 서비스 수준 관리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[서버 모니터링 (Nagios, 2000s) — 단일 서버 CPU/메모리 감시]
    |
    v
[로그 중앙화 (ELK, 2010s) — 분산 로그 수집·검색]
    |
    v
[분산 트레이싱 (Zipkin·Jaeger, 2015~) — MSA 요청 경로 추적]
    |
    v
[OpenTelemetry 통합 (2019~) — Metrics·Logs·Traces 단일 SDK]
    |
    v
[현재: AI Ops — 이상 탐지·근본 원인 자동 추론·자동 복구]
```

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>체온계(Monitoring)</strong>는 "열이 났다!"만 알려주지만, <strong>MRI(Observability)</strong>는 "어디가 아픈지" 속까지 보여줘요.
2. 서버도 마찬가지로, 숫자(Metrics)·일기장(Logs)·발자국(Traces) 3가지를 모아야 "왜 느린지" 정확히 알 수 있어요.
3. OpenTelemetry라는 마법 도구가 이 3가지를 한 번에 모아서, 의사 선생님(SRE)이 빨리 고칠 수 있게 도와준답니다!
