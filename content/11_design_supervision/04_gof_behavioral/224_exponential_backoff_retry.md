---
title: "Exponential Backoff and Retry Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 224
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Exponential Backoff and Retry (지수 백오프 재시도) 패턴은 일시적 네트워크 오류나 서버 과부하 시 재시도 간격을 지수적으로 증가시켜(1s -> 2s -> 4s -> 8s...), 서버가 복구될 시간을 주면서 불필요한 재시도 스파이크를 방지하는 패턴이다.
> 2. **가치**: Thundering Herd Problem (천둥 떼 문제) — 모든 클라이언트가 동시에 재시도하면 복구 중인 서버가 다시 과부하 — 을 Jitter (지터, 무작위 지연)를 추가함으로써 분산 재시도로 해결한다.
> 3. **판단 포인트**: 멱등성(Idempotency) 없는 작업(결제, 주문 생성)에는 재시도가 위험하다 — 중복 실행 방지를 위한 Idempotency Key (멱등성 키) 설계가 반드시 병행되어야 한다.

---

## Ⅰ. 개요 및 필요성
```
[단순 즉시 재시도 시나리오]
  서버 과부하 -> 1,000개 클라이언트 모두 즉시 재시도
  -> 서버 복구 중에 갑자기 3,000 요청 폭발 (원래 요청 + 재시도 × 2회)
  -> 서버 다시 다운 -> 무한 루프

[Thundering Herd Problem]
  +----------------------------------------------+
  | 시각   | 요청 수                               |
  | 0s     | 1,000 (정상)     <- 서버 과부하 발생   |
  | 1s     | 3,000 (재시도 2회) <- 천둥 떼 재시도   |
  | 2s     | 3,000            <- 서버 다시 다운     |
  +----------------------------------------------+
```

```
대기 시간 = min(cap, base × 2^attempt)

파라미터:
  base    : 기본 대기 시간 (예: 1초)
  attempt : 시도 횟수 (0, 1, 2, 3, ...)
  cap     : 최대 대기 시간 상한 (예: 32초)

예시:
  시도 0: min(32, 1 × 2^0) = 1초
  시도 1: min(32, 1 × 2^1) = 2초
  시도 2: min(32, 1 × 2^2) = 4초
  시도 3: min(32, 1 × 2^3) = 8초
  시도 4: min(32, 1 × 2^4) = 16초
  시도 5: min(32, 1 × 2^5) = 32초 <- cap 이후 고정
```

- **📢 섹션 요약 비유**: 지수 백오프는 자동차 엔진이 안 걸릴 때 시동 거는 방법 — 처음엔 바로 다시 시도, 다음엔 잠깐 기다렸다가, 그다음엔 더 기다렸다가 -> 배터리를 아끼면서 엔진(서버) 복구 시간을 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
Jitter 없는 지수 백오프의 문제:
  모든 클라이언트가 동시에 같은 시간(2초, 4초, 8초...)에 재시도
  -> 여전히 주기적인 스파이크 발생

Full Jitter 공식:
  wait = random_between(0, min(cap, base × 2^attempt))

효과:
  클라이언트마다 대기 시간이 무작위로 분산
  -> 시간축에 고르게 분포 -> 서버 부하 평활화

+--------------------------------------------------------------+
|  재시도 요청 분포 비교                                         |
|                                                              |
|  Jitter 없음:                                                |
|  t=1s  ████████████████████ (모두 동시 재시도 = 스파이크)     |
|  t=2s  ████████████████████                                  |
|                                                              |
|  Full Jitter:                                                |
|  t=0~2s  ████ ██ █ ██ ███ ██ █ ██  (고르게 분산)             |
|  t=0~4s  ██ █ ██ █ ███ █ ██ █ █ ██                          |
+--------------------------------------------------------------+
```

| 전략 | 공식 | 특징 |
|:---|:---|:---|
| Fixed Interval | wait = constant | 단순, 스파이크 가능 |
| Linear Backoff | wait = base × attempt | 선형 증가 |
| Exponential Backoff | wait = base × 2^attempt | 빠른 지수 증가 |
| Exponential + Jitter | wait = random(0, base × 2^attempt) | AWS 권장 표준 |
| Decorrelated Jitter | wait = random(base, prev × 3) | 더 넓은 분산 |

```
재시도 안전한 연산 (멱등성 O):
  GET /users/1        -> 항상 같은 결과
  DELETE /orders/1    -> 이미 삭제됐으면 404 반환 (OK)
  PUT /users/1 {name} -> 동일 값으로 덮어쓰기 = 안전

재시도 위험한 연산 (멱등성 X):
  POST /orders        -> 두 번 실행 = 두 개의 주문
  POST /payments      -> 두 번 실행 = 이중 결제

해결: Idempotency Key
  헤더에 고유 키 포함: Idempotency-Key: uuid-123
  서버가 키를 기록하고 중복 요청 시 이전 결과 반환
```

- **📢 섹션 요약 비유**: 멱등성이 없는 API 재시도는 카페에서 주문 실패 후 다시 주문하면 커피가 두 잔 나오는 것 — Idempotency Key는 "주문번호 #1234번을 또 주문해도 한 잔만 만들어 달라"는 요청이다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 적합한 실패 유형 | 목적 | 상호보완 |
|:---|:---|:---|:---|
| Retry + Exponential Backoff | 일시적 오류 (순간 지연) | 자동 복구 | Circuit Breaker가 열리면 재시도 중단 |
| Circuit Breaker | 지속적 장애 (서비스 다운) | 빠른 실패 | 실패율 누적 -> Circuit Breaker 트리거 |

조합 패턴:
```
요청
 |
 +- Circuit Breaker OPEN? -> 즉시 Fallback 반환 (재시도 안 함)
 |
 +- Circuit Breaker CLOSED -> 시도
        |
        +- 성공 -> 반환
        +- 실패 -> Exponential Backoff + Retry
                    |
                    +- 최대 재시도 초과 -> Dead Letter Queue
```

```
최대 재시도 횟수(maxAttempts) 초과 시:
  -> 메시지를 DLQ(Dead Letter Queue)로 이동
  -> 운영자 알림 (PagerDuty, Slack)
  -> 수동 재처리 또는 데이터 보정 절차

AWS SQS 예:
  원본 큐 -> 재시도 (maxReceiveCount: 3)
           -> 실패 시 DLQ로 자동 이동
```

- **📢 섹션 요약 비유**: DLQ는 우체국 반송 보관함 — 여러 번 배달 시도(재시도)해도 수취인이 없으면 반송함(DLQ)에 보관하고, 나중에 수취인(운영자)이 직접 처리한다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
RetryConfig config = RetryConfig.custom()
    .maxAttempts(5)
    .waitDuration(Duration.ofMillis(1000))
    .intervalFunction(IntervalFunction.ofExponentialRandomBackoff(
        1000,   // 초기 대기 ms
        2.0,    // 증가 배수 (2^n)
        0.5,    // Jitter 비율 (±50%)
        30_000  // 최대 대기 ms cap
    ))
    .retryOnException(ex -> ex instanceof TemporaryException)
    .build();

Retry retry = RetryRegistry.of(config).retry("externalService");
String result = retry.executeSupplier(() -> externalService.call());
```

AWS SDK는 기본적으로 Exponential Backoff + Full Jitter를 적용:
```
SDK 기본 설정:
  maxRetries: 3 (S3), 10 (DynamoDB)
  기본 대기: 최초 100ms
  최대 대기: 20,000ms
```

| 파라미터 | 결정 기준 | 예시 |
|:---|:---|:---|
| maxAttempts | SLA 허용 지연 시간 / 평균 복구 시간 | 3~5회 |
| base | 네트워크 왕복 시간 (RTT) × 2~5배 | 100ms~1s |
| cap | 사용자 최대 허용 대기 시간 | 30s~60s |
| Jitter | Full Jitter 권장 | random(0, wait) |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: cap(최대 대기) 없는 지수 백오프는 "고장난 알람이 계속 울리는데 비행기가 공항에 돌아오기만을 무한 대기" — cap을 설정해서 "30분 이상 기다리면 포기하고 다른 방법 찾기"로 현실적 상한을 둔다.

---

## Ⅴ. 기대효과 및 결론
Exponential Backoff and Retry 패턴은 분산 시스템의 복원력(Resilience) 기반 기법이다:

**기대효과**:
- <strong>일시적 장애 자동 복구</strong>: 네트워크 순간 오류의 90%는 재시도로 해결
- **서버 부하 감소**: Jitter로 재시도 스파이크 방지
- <strong>SLA 향상</strong>: 재시도 없이는 실패했을 요청도 성공으로 전환

**적용 원칙**:
1. 재시도 전 <strong>멱등성 확인</strong> — 비멱등성 연산에는 Idempotency Key 필수
2. <strong>Circuit Breaker 조합</strong> — 지속 장애 시 재시도 루프 방지
3. **최대 재시도 제한** + **DLQ** 연계로 무한 재시도 방지
4. 재시도 시마다 **로깅과 지표 수집** — 재시도 빈도는 인프라 건강의 바로미터

심화 학습에서는 **지수 백오프 공식**, **Jitter의 역할(Thundering Herd 방지)**, <strong>멱등성 요구사항</strong>을 함께 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 지수 백오프 + Jitter는 지하철역에서 나오는 사람들처럼 — 한꺼번에 쏟아지지 않고 에스컬레이터(지수 대기)와 무작위 보행 속도(Jitter)가 자연스럽게 분산시켜 출구(서버)가 막히지 않게 한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 분산 시스템 복원력 (Resilience) | 재시도가 제공하는 핵심 속성 |
| 연관 패턴 | Circuit Breaker | 지속 장애 시 재시도를 차단 |
| 연관 패턴 | Dead Letter Queue (DLQ) | 최대 재시도 초과 메시지 보관 |
| 연관 개념 | Idempotency Key (멱등성 키) | 비멱등성 연산 재시도 시 중복 방지 |
| 연관 개념 | Thundering Herd Problem | Jitter가 해결하는 동시 재시도 스파이크 |
| 구현체 | Resilience4j Retry | Java 표준 재시도 라이브러리 |
| 구현체 | AWS SDK 기본 재시도 | Exponential + Full Jitter 내장 |

### 📈 관련 키워드 및 발전 흐름도
재시도 정책 -> 지수 백오프 재시도 패턴 -> adaptive retry

### 👶 어린이를 위한 3줄 비유 설명
1. 게임에서 통신 오류가 났을 때 1초 후 다시 접속, 실패하면 2초 후, 또 실패하면 4초 후... 이렇게 기다리는 시간을 두 배씩 늘리는 것이 지수 백오프야.
2. 모든 친구가 동시에 재접속을 시도하면 서버가 또 터지니까(Thundering Herd), 각자 다른 시간에 재시도하도록 무작위 딜레이(Jitter)를 더해줘.
3. 결제나 주문처럼 중요한 것은 같은 요청을 두 번 하면 안 되니까 "주문번호 표(Idempotency Key)"를 들고 가서 "이 주문은 하나만요"라고 서버에게 알려줘야 해.
