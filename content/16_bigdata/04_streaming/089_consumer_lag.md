---
title: "Consumer Lag"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 89
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Consumer Lag (소비자 지연)은 Kafka 토픽의 최신 오프셋(Latest Offset)과 Consumer 그룹이 커밋한 오프셋(Committed Offset)의 차이로, "Consumer가 Producer보다 얼마나 뒤처져 있는가"를 나타내는 스트리밍 파이프라인의 핵심 건강 지표다.
- **가치**: Consumer Lag 급증은 파이프라인 병목(처리 속도 < 수신 속도)의 조기 경보이며, Lag=0이 목표이나 일시적 급증은 정상이므로 <strong>트렌드와 임계값</strong>을 기반으로 오토스케일링과 알림 트리거를 설정해야 한다.
- **판단 포인트**: Consumer Lag이 계속 증가하면 Consumer를 수평 확장하거나(파티션 수만큼), 소비 처리 로직을 최적화하거나, 메시지 생산 속도를 낮추는 세 가지 대응 중 병목 위치에 따라 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. Consumer Lag의 정의

```
Kafka Topic "orders":
  파티션 0: 최신 오프셋 = 10,000 (Producer가 여기까지 씀)
  파티션 0: Consumer 커밋 오프셋 = 9,500 (Consumer가 여기까지 읽음)
  -> Lag = 10,000 - 9,500 = 500 (메시지 500개 미처리)

파티션 1: 최신 = 8,000, 커밋 = 8,000 -> Lag = 0
파티션 2: 최신 = 12,000, 커밋 = 11,000 -> Lag = 1,000

총 Consumer Lag = 500 + 0 + 1,000 = 1,500
```

### 2. Consumer Lag이 중요한 이유

- <strong>실시간 처리 SLA</strong>: Lag이 크면 데이터 신선도(Data Freshness)가 낮아짐
- **장애 예측**: Lag 급증 -> 처리 병목 -> 잠재적 OOM/장애 전조
- <strong>스케일링 신호</strong>: 지속적인 Lag 증가 = Consumer 추가 또는 파이프라인 최적화 필요

**📢 섹션 요약 비유**
> Consumer Lag는 "편의점 계산대 앞 대기 줄 길이"다. 줄이 0이면 실시간 처리, 줄이 100명이면 주문이 100개 밀려 있다는 의미다. 줄이 계속 길어지면 계산원(Consumer)을 더 배치해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Lag 계산 및 모니터링 방법

```bash
# Kafka CLI로 Consumer Lag 조회
kafka-consumer-groups.sh \
    --bootstrap-server kafka:9092 \
    --group my-consumer-group \
    --describe

# 출력 예시:
# TOPIC          PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# orders         0          9500            10000           500
# orders         1          8000            8000            0
# orders         2          11000           12000           1000
```

### 2. 주요 모니터링 도구

| 도구 | 특징 | 권장 사용 환경 |
|:---|:---|:---|
| Kafka CLI (`kafka-consumer-groups.sh`) | 기본 제공, 실시간 조회 | 개발/디버깅 |
| Burrow (LinkedIn 오픈소스) | 트렌드 분석, 알림, 슬라이딩 윈도우 판단 | 프로덕션 모니터링 |
| JMX Metrics | `kafka.consumer.fetch-manager-metrics` | Prometheus/Grafana 통합 |
| Kafka UI / Confluent Control Center | 시각화 대시보드 | 운영 가시성 |
| AWS MSK Console (MSK 사용 시) | 관리형 클러스터 내장 | AWS 환경 |

### 3. Burrow의 Lag 판단 로직

Burrow (LinkedIn, 오픈소스)는 단순 Lag 숫자가 아닌 <strong>Consumer의 처리 진행 여부</strong>로 판단한다.

```
판단 기준:
  OK:       Consumer가 계속 진행 중 (Lag이 있어도 줄어들고 있으면 OK)
  WARNING:  Consumer가 느려지고 있음 (Lag이 천천히 증가)
  ERROR:    Consumer가 멈춤 (커밋 오프셋이 변하지 않음)
  STALLED:  Consumer가 커밋을 못함 (처리 중이지만 커밋 미완료)
  STOPPED:  Consumer 그룹 전체 정지
```

**📢 섹션 요약 비유**
> Burrow는 "대기 줄 분석가"다. 단순히 "줄이 500명이다"가 아니라 "줄이 줄어드는 중인가, 늘어나는 중인가, 멈췄는가"를 판단한다. 줄이 500명이어도 줄어드는 중이면 문제없고, 줄이 10명이어도 계속 늘어나면 위험 신호다.

---

## Ⅲ. 비교 및 연결

### 1. Consumer Lag 급증 원인별 해결책

| 원인 | 증상 | 해결책 |
|:---|:---|:---|
| Consumer 처리 속도 부족 | Lag 지속 증가, Consumer CPU 높음 | Consumer 수 증가 (파티션 수 이내) |
| Consumer 로직 병목 | 특정 처리 단계에서 느림 | 처리 로직 최적화, I/O 비동기화 |
| 프로듀서 버스트 트래픽 | 일시적 Lag 급등 후 회복 | 버퍼 크기 조정, 처리 용량 예비 확보 |
| Consumer 장애 | Lag 무한 증가, Consumer 0개 | 장애 복구, 자동 재시작 설정 |
| 파티션 수 < Consumer 수 | 일부 Consumer 유휴 | 파티션 수 증가 |

### 2. Kafka Lag 기반 오토스케일링

```yaml
# KEDA (Kubernetes Event-Driven Autoscaling) 예시
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
spec:
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka:9092
      consumerGroup: my-consumer-group
      topic: orders
      lagThreshold: "100"   # Lag 100 초과 시 스케일아웃
      offsetResetPolicy: latest
```

**📢 섹션 요약 비유**
> Kafka Lag 기반 오토스케일링은 "주문 대기열에 따라 배달원을 자동으로 더 투입하는 시스템"이다. 주문이 100개 밀리면(Lag > 100) 배달원(Consumer Pod)을 자동으로 추가하고, 다 처리되면 줄인다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Consumer Lag 모니터링 아키텍처

```
Kafka Cluster
    v JMX Metrics 수집
JMX Exporter (Prometheus)
    v
Prometheus -> Grafana 대시보드
    v Lag > 임계값
AlertManager -> PagerDuty / Slack 알림
    v Lag 지속 증가
KEDA / Custom HPA -> Consumer Pod 스케일아웃
```

### 2. 알림 임계값 설정 가이드

| Lag 수준 | 의미 | 권장 대응 |
|:---|:---|:---|
| Lag < 허용_지연 × EPS | 정상 | 모니터링 유지 |
| Lag 증가 추세 지속 5분+ | 경고 | 원인 분석 시작 |
| Lag > 최대_허용_지연 × EPS | 알림 | 즉시 대응 |
| Consumer 진행 멈춤 | 긴급 | PagerDuty 알림 |

(EPS = Events Per Second = 초당 이벤트 수)

### 3. 체크리스트

- [ ] Prometheus + JMX Exporter로 Consumer Lag 지표 수집
- [ ] Grafana 대시보드에 파티션별 Lag 시각화
- [ ] Lag 증가 추세에 대한 알림 규칙 설정 (단순 임계값이 아닌 트렌드)
- [ ] Burrow 또는 유사 도구로 Consumer 상태 분류 모니터링
- [ ] KEDA/HPA 기반 오토스케일링 설정

**📢 섹션 요약 비유**
> Consumer Lag 모니터링은 "혈압 측정"과 같다. 단일 측정값보다 시간 추이가 중요하다. 혈압이 높아도 안정적이면 문제없지만, 계속 오르는 추세면 의사에게 가야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 장애 조기 예방 | Lag 증가 추세로 병목 사전 감지 |
| SLA 보장 | 데이터 신선도(Data Freshness) 모니터링 |
| 비용 최적화 | Lag 기반 오토스케일링으로 불필요한 과잉 Consumer 방지 |

### 2. 결론

Consumer Lag는 Kafka 기반 스트리밍 파이프라인의 <strong>가장 중요한 단일 건강 지표</strong>다. 학습 정리에서는 Lag의 수식 정의(Latest - Committed Offset), 모니터링 도구(Burrow, JMX), 원인별 해결 전략, 오토스케일링과의 연계를 체계적으로 서술하면 된다.

**📢 섹션 요약 비유**
> Consumer Lag는 공장 생산라인의 "미완성 재공품(WIP) 수량"이다. WIP가 0이면 완벽한 흐름, WIP가 늘어나면 어딘가 병목이 있다는 신호다. 공장 관리자(모니터링 시스템)는 WIP 추이를 실시간으로 보고 라인을 조정한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Kafka 파티셔닝 | 전제 구조 | 파티션별 Lag을 개별 추적 |
| Consumer Group | 측정 단위 | Lag는 Consumer Group 기준 측정 |
| Burrow | 모니터링 도구 | LinkedIn의 Lag 상태 분류 도구 |
| KEDA | 오토스케일링 | Lag 기반 K8s Consumer 자동 확장 |
| Kafka MirrorMaker 2 | 연관 운영 | 복제 클러스터 간 Lag 차이 모니터링 |


### 📈 관련 키워드 및 발전 흐름도

```text
[Kafka 프로듀서 (Producer) — 토픽 파티션에 메시지 비동기 발행]
    |
    v
[오프셋 (Offset) — 파티션 내 메시지 위치, LEO vs 커밋 오프셋 구분]
    |
    v
[Consumer Lag — LEO - Current Offset, 소비 지연 누적량 정량 측정]
    |
    v
[컨슈머 그룹 모니터링 — Burrow·kafka-consumer-groups로 실시간 Lag 추적]
    |
    v
[자동 스케일링 (KEDA) — Lag 임계값 기반 컨슈머 인스턴스 수평 확장·축소]
```

이 흐름은 Kafka 메시지 발행에서 오프셋 개념으로 Consumer Lag이 정의되고, 모니터링 도구로 가시화된 뒤 KEDA 기반 자동 스케일링으로 Lag을 능동적으로 제어하는 스트리밍 파이프라인 운영의 핵심 계보를 보여준다.


### 👶 어린이를 위한 3줄 비유 설명

카카오톡 메시지를 받았지만 아직 읽지 않은 것처럼, Consumer Lag는 "Kafka에 메시지가 왔는데 아직 처리 못한 개수"예요. 읽지 않은 메시지가 0개면 실시간 처리, 1000개면 1000개 뒤처진 것이에요. 메시지가 계속 쌓이면(Lag 증가) 더 많은 처리자(Consumer)를 투입하거나 읽는 속도를 높여야 해요!
