---
title: "Prometheus"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 136
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Prometheus는 <strong>Pull 방식으로 서비스의 /metrics 엔드포인트에서 시계열 메트릭을 수집·저장</strong>하는 CNCF 졸업 프로젝트이며, 클라우드 네이티브 모니터링의 사실상 표준이다.
> 2. **가치**: Push 기반(StatsD)은 서비스가 모니터링 시스템에 종속되지만, Prometheus의 Pull은 <strong>서비스가 메트릭을 노출만 하면</strong> Prometheus가 주기적으로 가져가므로 느슨한 결합이다.
> 3. **판단 포인트**: PromQL(쿼리 언어)·Alertmanager(알림)·Service Discovery(K8s 자동 발견)·장기 저장(Thanos·Mimir)이 핵심 에코시스템이다.

---

## Ⅰ. 개요 및 필요성

```text
서비스 -> /metrics 노출 -> Prometheus (Pull, 15초 주기)
  -> TSDB 저장 -> PromQL 조회 -> Grafana 시각화
  -> Alertmanager -> PagerDuty/Slack 알림
```

- **📢 섹션 요약 비유**: Prometheus는 <strong>우편배달부(Pull)</strong>이다. 각 집(서비스)의 우편함(/metrics)에서 편지(메트릭)를 수거한다.

---

## Ⅱ~Ⅴ. 결론

Prometheus는 <strong>K8s 환경의 메트릭 표준</strong>이며, Thanos/Mimir로 장기 저장·고가용성을 확보한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Prometheus** | Pull 메트릭 수집 |
| **PromQL** | 메트릭 조회 언어 |
| **Alertmanager** | 알림 라우팅 |
| **Thanos** | 장기 저장·HA |
| **Mimir** | Grafana Labs 장기 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Borgmon (Google 내부, 2000s)] -> [Prometheus (SoundCloud, 2012)]
    -> [CNCF 졸업 (2018)] -> [Thanos (2018, HA)]
    -> [Mimir (2022, Grafana Labs)]
    -> [현재: OTel Metrics -> Prometheus 호환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Prometheus는 <strong>우편배달부</strong>예요. 각 서비스(집)의 우편함(/metrics)에서 <strong>편지를 수거</strong>해요.
2. 수거한 편지를 <strong>정리(TSDB)</strong>하고 <strong>그래프(Grafana)</strong>로 보여줘요.
3. 위험한 편지(이상 지표)가 오면 <strong>비상벨(Alertmanager)</strong>을 울려요!
