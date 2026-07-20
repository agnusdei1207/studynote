---
title: "Logs, Centralized Logging"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 187
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로그(Logs)는 시스템과 애플리케이션에서 발생한 이벤트의 시간 순서 텍스트 기록으로, 장애 원인 분석(RCA)에 필수적인 상세 문맥을 제공하는 옵저버빌리티의 두 번째 기둥이다.
> 2. **가치**: ELK Stack(Elasticsearch + Logstash + Kibana)은 수백 개의 마이크로서비스 로그를 중앙 수집·검색·시각화하여 "바늘 하나를 수십억 줄 로그 더미에서 찾는" 능력을 제공한다.
> 3. **판단 포인트**: 구조화 로그(JSON 형식)를 작성해야 Elasticsearch 검색과 Kibana 시각화를 최대한 활용할 수 있으며, Fluentd/Fluentbit은 경량·유연성으로 ELK의 Logstash를 대체하는 추세다.

---

## Ⅰ. 개요 및 필요성

메트릭이 "서비스가 느리다"라고 알려준다면, 로그는 "왜 느린가"의 답을 담고 있다. `ERROR: 2026-04-21T14:32:01 - DB 연결 실패: connection timeout after 30000ms`처럼 구체적 원인과 컨텍스트를 포함한다.

분산 마이크로서비스 환경에서 로그는 50개 이상의 서비스 각각이 생성한다. 각 서버에 SSH로 접속해 `tail -f /var/log/app.log`하는 것은 불가능하다. 중앙 집중식 로깅(Centralized Logging)이 필수다.

ELK Stack은 이 문제의 표준 오픈소스 해법이다. E(Elasticsearch, 저장·검색), L(Logstash, 수집·변환), K(Kibana, 시각화)로 구성되며, 초당 수백만 건의 로그를 수집하고 밀리초 내 전문 검색(Full-Text Search)이 가능하다. 오늘날은 여기에 Beats(경량 수집기) 또는 Fluentd를 더해 "Elastic Stack"이라고도 부른다.

📢 **섹션 요약 비유**: 로그 중앙화는 전국 지사 모든 직원의 업무 일지를 본사 데이터베이스에 자동으로 모으는 것이다. 문제가 생기면 전체 일지를 검색해 원인을 즉시 파악한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ELK Stack 수집 흐름

```
[ELK Stack 중앙화 로깅 아키텍처]

마이크로서비스들
+-- Service A: 로그 출력 (stdout/file)
+-- Service B: 로그 출력
+-- Service C: 로그 출력
         v
[수집 에이전트]
  Filebeat / Fluentd / Fluentbit
  (각 노드에 DaemonSet으로 배포)
         v
[수집·변환·파싱]
  Logstash / Kafka (버퍼)
  (필드 추출, 필터링, 강화)
         v
[저장·인덱싱]
  Elasticsearch 클러스터
  (샤딩, 복제, 역인덱스)
         v
[시각화·검색]
  Kibana 대시보드
  (로그 검색, 시각화, 알람)
```

| 컴포넌트 | 역할 | 대안 |
|:---|:---|:---|
| Elasticsearch | 로그 저장, 전문 검색, 인덱싱 | OpenSearch, Splunk |
| Logstash | 로그 수집, 파싱, 변환 | Fluentd, Vector |
| Kibana | 로그 시각화, 검색 UI | Grafana (Loki) |
| Filebeat | 경량 파일 수집기 (Beats 계열) | Fluentbit |

📢 **섹션 요약 비유**: ELK Stack은 도서관 시스템이다. 책들(로그)을 수집하고(Logstash), 목록을 만들어 서가에 분류하고(Elasticsearch), 사서가 원하는 책을 찾아주는(Kibana) 체계다.

---

## Ⅲ. 비교 및 연결

### ELK vs Grafana Loki

| 항목 | ELK Stack | Grafana Loki |
|:---|:---|:---|
| 인덱싱 방식 | 전체 내용 인덱싱 (강력한 검색) | 레이블만 인덱싱 (경량) |
| 비용 | 높음 (인덱스 스토리지) | 낮음 |
| 검색 속도 | 빠름 | 상대적으로 느림 |
| Prometheus 통합 | 별도 설정 | 네이티브 통합 |
| 적합 환경 | 대규모, 복잡한 검색 | 쿠버네티스 네이티브, 비용 최적화 |

<strong>구조화 로그 vs 비구조화 로그:</strong>

```json
// 나쁜 예 (비구조화)
"2026-04-21 14:32:01 ERROR User 12345 checkout failed: DB error"

// 좋은 예 (구조화 JSON)
{
  "timestamp": "2026-04-21T14:32:01Z",
  "level": "ERROR",
  "service": "checkout-service",
  "user_id": "12345",
  "event": "checkout_failed",
  "reason": "db_connection_timeout",
  "trace_id": "abc123def456"
}
```

📢 **섹션 요약 비유**: 비구조화 로그는 일기장처럼 자유롭게 쓴 메모이고, 구조화 로그는 엑셀 표처럼 각 칸에 정보가 정확히 들어간 데이터다. 엑셀이 훨씬 검색하기 쉽다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>효과적인 로그 작성 원칙:</strong>
1. **레벨 구분**: DEBUG, INFO, WARN, ERROR, FATAL 적절히 사용
2. **Correlation ID(상관 ID)**: 모든 로그에 Trace ID 포함하여 요청 추적
3. <strong>개인정보 마스킹</strong>: 비밀번호, 카드번호 로그 금지
4. **비즈니스 이벤트 로깅**: 주문 생성, 결제 완료 등 중요 이벤트 기록
5. <strong>예외 전체 스택 트레이스</strong>: 오류 시 full stack trace 포함

<strong>Kubernetes 로그 수집:</strong>
- DaemonSet으로 Fluentbit 배포: 모든 노드의 컨테이너 로그 자동 수집
- `kubectl logs` 단기 저장 한계 -> 중앙화 필수
- 컨테이너는 stdout/stderr로만 출력 (파일 로그 금지)

**실무 알람 연동:**
- Kibana Watcher: 로그 패턴 기반 알람 (특정 에러 n분 내 m회 이상)
- ElastAlert: Python 기반 알람 도구

📢 **섹션 요약 비유**: Trace ID 포함은 택배 송장 번호와 같다. 하나의 주문(요청)이 여러 물류센터(서비스)를 거쳐도 송장 번호 하나로 전체 경로를 추적할 수 있다.

---

## Ⅴ. 기대효과 및 결론

중앙화된 로깅은 분산 마이크로서비스 환경에서 장애 진단 시간을 드라마틱하게 단축한다. MTTR(Mean Time To Repair)이 "각 서버에 SSH 접속하여 로그 찾기"의 시간에서 "Kibana에서 Trace ID 검색" 30초로 줄어든다.

비용과 보존 정책이 주요 운영 과제다. 로그는 매우 빠르게 증가하므로, Hot(최근 7일, 빠른 검색) -> Warm(30일, 일반 검색) -> Cold(90일, 압축 보관) -> Delete(삭제) 레이어별 데이터 수명 주기(ILM, Index Lifecycle Management) 정책을 반드시 설정해야 한다.

📢 **섹션 요약 비유**: 로그 ILM은 편의점 유통기한 관리다. 신선식품(최근 로그)은 냉장 진열대에, 조금 지난 것은 창고에, 오래된 것은 폐기한다. 모든 걸 냉장 진열대에 두면 공간이 부족하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| 옵저버빌리티 | 로그는 3대 기둥 중 두 번째 |
| Trace ID | 로그-트레이스 상관관계 연결 키 |
| ELK Stack | 로그 중앙화의 표준 오픈소스 스택 |
| Fluentd / Fluentbit | 경량 로그 수집기, Logstash 대안 |
| Grafana Loki | 비용 효율적 로그 저장소, ELK 대안 |
| RCA | 장애 원인 분석 시 로그가 핵심 증거 |

### 👶 어린이를 위한 3줄 비유 설명
1. 로그는 서비스가 매일 쓰는 일기장이에요. 무슨 일이 있었는지 다 적혀 있어요.

### 📈 관련 키워드 및 발전 흐름도

```text
각 서버별 개별 로그 파일 (분산 시 확인 불가)
    |
    v
중앙 집중 로깅: ELK (Elastic · Logstash · Kibana) · Loki
    +-► 구조화 로그: JSON 형식 + Trace ID 포함
    +-► 로그 레벨: DEBUG · INFO · WARN · ERROR · FATAL
    |
    v
AIOps: 로그 패턴 자동 분석 · 이상 탐지
```
2. ELK Stack은 전국 모든 지점의 일기장을 한 곳에 모아서 쉽게 검색하는 시스템이에요.
3. 문제가 생기면 "14시 32분에 무슨 일이 있었나?" 한 번 검색으로 원인을 바로 찾을 수 있어요!
