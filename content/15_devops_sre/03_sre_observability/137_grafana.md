---
title: "Grafana"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Grafana는 <strong>Prometheus·Loki·Tempo·Elasticsearch 등 다양한 데이터 소스를 통합하여 대시보드로 시각화</strong>하는 오픈소스 관측 가능성 플랫폼이며, LGTM Stack(Loki+Grafana+Tempo+Mimir)의 중심이다.
> 2. **가치**: 메트릭·로그·트레이스를 <strong>하나의 대시보드에서 상관 분석</strong>할 수 있어, 장애 시 "메트릭 이상->로그 확인->트레이스 추적"의 워크플로를 단일 도구에서 수행한다.
> 3. **판단 포인트**: Grafana는 시각화 레이어이지 저장소가 아니며, 데이터 소스(Prometheus·Loki·Tempo)와의 조합이 핵심이다. Grafana Cloud는 SaaS 관리형 서비스이다.

---

## Ⅰ. 개요 및 필요성

```text
Grafana = 다중 데이터 소스 -> 통합 대시보드
  Prometheus (메트릭) + Loki (로그) + Tempo (트레이스)
  -> 하나의 대시보드에서 상관 분석
  -> 알림 -> PagerDuty/Slack
```

- **📢 섹션 요약 비유**: Grafana는 <strong>병원 종합 모니터</strong>이다. 심전도·혈압·체온을 **한 화면에서** 동시에 본다.

---

## Ⅱ~Ⅴ. 결론

Grafana는 <strong>관측 가능성의 "눈(시각화)"</strong>이며, LGTM Stack으로 오픈소스 관측 표준을 구축할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Grafana</strong> | 통합 시각화 |
| <strong>LGTM Stack</strong> | Loki+Grafana+Tempo+Mimir |
| **Dashboard** | 대시보드 |
| <strong>Data Source</strong> | Prometheus·Loki·Tempo |
| <strong>Grafana Cloud</strong> | 관리형 SaaS |

### 📈 관련 키워드 및 발전 흐름도

```text
[Kibana (ELK, 2012)] -> [Grafana (2014, Torkel Ödegaard)]
    -> [Grafana Labs (2015~)] -> [LGTM Stack (2020~)]
    -> [현재: Grafana 11 — Scenes·App Platform]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Grafana는 <strong>병원 종합 모니터</strong>예요. 심전도·혈압·체온을 **한 화면에서** 봐요.
2. 여러 기계(데이터 소스)의 정보를 <strong>예쁜 그래프</strong>로 보여줘요.
3. 이상이 생기면 <strong>알림</strong>을 보내서 바로 알 수 있답니다!
