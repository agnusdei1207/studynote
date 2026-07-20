---
title: "Metrics Monitoring"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 132
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Metrics는 <strong>시계열 수치 데이터(CPU·메모리·요청 수·에러율)</strong>이며, Prometheus가 Pull 방식으로 수집하고 PromQL로 조회하며 Grafana로 시각화하는 것이 클라우드 네이티브 메트릭 표준이다.
> 2. **가치**: 메트릭 없이는 "시스템이 느리다"만 알고 <strong>어떤 서비스의 어떤 지표가 임계치를 넘었는지</strong> 알 수 없으며, 메트릭 기반 알림으로 <strong>장애를 조기 감지</strong>한다.
> 3. **판단 포인트**: 4대 골든 시그널(Latency·Traffic·Errors·Saturation)이 SRE 모니터링의 핵심이며, RED(Rate·Errors·Duration)·USE(Utilization·Saturation·Errors)가 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
Prometheus -> Pull -> 서비스 /metrics 엔드포인트
  -> TSDB 저장 -> PromQL 조회
  -> Alertmanager -> PagerDuty/Slack
  -> Grafana 대시보드 시각화
```

- **📢 섹션 요약 비유**: Prometheus는 **체온계(수집)**, Grafana는 <strong>진료 차트(시각화)</strong>, Alertmanager는 <strong>비상벨(알림)</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 4대 골든 시그널 | 설명 |
|:---|:---|
| <strong>Latency</strong> | 응답 시간 |
| **Traffic** | 요청 수 |
| **Errors** | 에러율 |
| **Saturation** | 리소스 포화도 |

---

## Ⅲ~Ⅴ. 결론

Prometheus+Grafana는 <strong>클라우드 네이티브 메트릭의 사실상 표준</strong>이며, 4대 골든 시그널 기반 알림이 SRE 모니터링의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Prometheus</strong> | 메트릭 수집 (Pull) |
| <strong>Grafana</strong> | 메트릭 시각화 |
| **PromQL** | 메트릭 조회 언어 |
| <strong>Golden Signals</strong> | 4대 핵심 지표 |
| **Alertmanager** | 알림 라우팅 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Nagios/Zabbix (2000s)] -> [Prometheus (2012, SoundCloud)]
    -> [CNCF 졸업 (2018)] -> [Grafana LGTM Stack (2020~)]
    -> [현재: Mimir (장기 메트릭 저장) + Thanos (HA)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Prometheus는 <strong>체온계</strong>예요. 시스템의 <strong>건강 수치</strong>를 재요.
2. Grafana는 <strong>진료 차트</strong>예요. 수치를 <strong>그래프로 보기 쉽게</strong> 보여줘요.
3. 수치가 위험하면 <strong>비상벨(Alertmanager)</strong>이 울려서 바로 알 수 있어요!
