---
title: "Jaeger Zipkin Distributed Tracing Backend"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 145
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Jaeger(Uber, CNCF)와 Zipkin(Twitter, 오픈소스)은 <strong>분산 트레이스 데이터를 수집·저장·시각화</strong>하는 트레이싱 백엔드이며, Waterfall UI로 서비스 간 호출 체인의 지연·에러를 분석한다.
> 2. **가치**: 로그만으로는 <strong>MSA의 어느 서비스가 병목인지</strong> 알 수 없지만, Jaeger/Zipkin은 <strong>전체 호출 체인을 Gantt 차트로 시각화</strong>하여 병목 서비스·쿼리를 즉시 식별한다.
> 3. **판단 포인트**: Jaeger(Go, CNCF, Kafka 지원)가 K8s 환경에서 주류이며, Grafana Tempo(저비용, 오브젝트 스토리지)가 차세대 대안이다. OTel SDK로 계측하면 백엔드를 자유롭게 교체할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
Jaeger 아키텍처:
  OTel SDK -> Collector -> Storage(ES/Cassandra) -> UI
Zipkin 아키텍처:
  SDK -> Transport(HTTP/Kafka) -> Storage(ES) -> UI
Tempo: OTel -> S3/GCS (인덱스 없음, 저비용)
```

- **📢 섹션 요약 비유**: Jaeger/Zipkin은 <strong>비행 관제탑</strong>이다. 모든 비행기(요청)의 경로·지연·이상을 **한눈에** 모니터링한다.

---

## Ⅱ~Ⅴ. 결론

Jaeger는 <strong>K8s 트레이싱의 CNCF 표준</strong>이며, Tempo(저비용)와 OTel(표준 계측)이 트렌드이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Jaeger** | CNCF 트레이싱 |
| **Zipkin** | 오픈소스 선구자 |
| **Tempo** | 저비용 대안 |
| <strong>OTel</strong> | 계측 표준 |
| **Waterfall** | 시각화 UI |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper (Google, 2010)] -> [Zipkin (Twitter, 2012)]
    -> [Jaeger (Uber/CNCF, 2017)]
    -> [Grafana Tempo (2020, 저비용)]
    -> [현재: OTel 수렴 — 백엔드 교체 자유]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Jaeger/Zipkin은 <strong>비행 관제탑</strong>이에요. 모든 비행기(요청) 경로를 봐요.
2. "이 비행기는 <strong>서울 공항에서 2시간 지연됐네!</strong>" -> 병목 발견!
3. OTel로 계측하면 **관제탑(백엔드)을 자유롭게** 바꿀 수 있어요!
