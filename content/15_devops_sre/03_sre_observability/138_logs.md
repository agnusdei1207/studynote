---
title: "Logs"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 138
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로그는 <strong>시스템·애플리케이션이 발생시킨 이벤트의 시간순 텍스트 기록</strong>이며, Observability 3대 축(Metrics·Logs·Traces) 중 가장 상세한 정보를 제공한다.
> 2. **가치**: 메트릭은 "무엇이 이상한가", 트레이스는 "어디서 느린가"를 알려주지만, 로그는 <strong>"왜 발생했는가"의 상세 맥락(에러 메시지·스택 트레이스·요청 파라미터)</strong>을 제공한다.
> 3. **판단 포인트**: 구조화 로깅(JSON)이 필수이며, ELK(Elasticsearch·Logstash·Kibana) 또는 Grafana Loki가 중앙 집중 로그 관리의 표준 스택이다.

---

## Ⅰ. 개요 및 필요성

```text
비구조화: "2024-01-15 ERROR: Payment failed for user 123"
구조화(JSON): {"ts":"2024-01-15","level":"ERROR","msg":"Payment failed","user_id":123}
  -> 검색·필터링·분석 용이
  -> 중앙 집중: Loki/ELK로 수집 -> 쿼리·대시보드
```

- **📢 섹션 요약 비유**: 로그는 <strong>비행기 블랙박스</strong>이다. 사고(장애) 후 <strong>원인을 상세히 추적</strong>하는 유일한 기록이다.

---

## Ⅱ~Ⅴ. 결론

구조화 로그 + 중앙 집중 관리(Loki/ELK)는 <strong>장애 원인 분석의 핵심</strong>이며, 메트릭·트레이스와 상관 분석으로 완전한 관측을 달성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>로그</strong> | 상세 이벤트 기록 |
| <strong>구조화 로깅</strong> | JSON 형식 |
| **ELK** | Elasticsearch+Logstash+Kibana |
| **Loki** | Grafana 로그 시스템 |
| **Correlation ID** | 로그-트레이스 연결 |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 로그 (tail -f)] -> [syslog (중앙 수집)]
    -> [ELK Stack (2012)] -> [Fluentd/Fluent Bit (CNCF)]
    -> [Grafana Loki (2018, 경량)]
    -> [현재: OTel Logs — 메트릭·트레이스 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 로그는 <strong>비행기 블랙박스</strong>예요. 무슨 일이 있었는지 <strong>자세히 기록</strong>해요.
2. 사고(장애)가 나면 블랙박스를 열어 **원인을 찾아요**.
3. JSON으로 <strong>정리 정돈</strong>하면 검색하기 쉽고 빨리 원인을 알 수 있어요!
