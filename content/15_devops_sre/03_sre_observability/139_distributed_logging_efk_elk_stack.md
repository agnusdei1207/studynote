---
title: "Distributed Logging Efk Elk Stack"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 139
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 로깅은 <strong>수십~수백 개 마이크로서비스의 로그를 중앙 수집·저장·검색하는 시스템</strong>이며, ELK(Elasticsearch·Logstash·Kibana)·EFK(Elasticsearch·Fluentd·Kibana)·Grafana Loki가 대표 스택이다.
> 2. **가치**: MSA에서 각 서비스가 개별 로그 파일을 가지면 장애 시 <strong>수십 서버를 일일이 SSH 접속</strong>해야 하지만, 중앙 로깅은 <strong>한 곳에서 전체 로그를 검색·필터·상관 분석</strong>한다.
> 3. **판단 포인트**: ELK는 **전문 검색에 강하지만 비용^**, Loki는 <strong>레이블 기반 경량(인덱스 없음)</strong>이며, Fluentd/Fluent Bit가 CNCF 표준 로그 수집기이다.

---

## Ⅰ. 개요 및 필요성

```text
ELK: Logstash(수집·파싱) -> Elasticsearch(저장·검색) -> Kibana(시각화)
EFK: Fluentd(수집, CNCF) -> Elasticsearch -> Kibana
Loki: Promtail(수집) -> Loki(레이블 저장) -> Grafana(시각화)
```

- **📢 섹션 요약 비유**: 분산 로깅은 <strong>중앙 도서관</strong>이다. 각 교실(서비스)의 일기장을 한 곳에 모아 <strong>누구든 검색</strong>할 수 있게 한다.

---

## Ⅱ~Ⅴ. 결론

중앙 집중 로깅은 <strong>MSA 운영의 필수 인프라</strong>이며, ELK(전문 검색)와 Loki(경량)를 환경에 맞게 선택한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ELK** | Elasticsearch+Logstash+Kibana |
| **EFK** | Fluentd 대체 (CNCF) |
| **Loki** | 경량 로그 (레이블 기반) |
| **Fluentd** | CNCF 로그 수집기 |
| **Correlation ID** | 분산 로그 추적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[syslog (1980s)] -> [ELK Stack (2012)]
    -> [EFK (Fluentd, CNCF)] -> [Grafana Loki (2018, 경량)]
    -> [현재: OTel Logs — 메트릭·트레이스 통합 수집]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 분산 로깅은 <strong>중앙 도서관</strong>이에요. 각 교실의 일기장을 **한 곳에 모아요**.
2. 모아놓으면 <strong>누구든 쉽게 검색</strong>할 수 있어요. "3반 수학 일기는?"
3. 일일이 교실을 돌아다니지 않아도 **한 곳에서 다 찾을** 수 있어요!
