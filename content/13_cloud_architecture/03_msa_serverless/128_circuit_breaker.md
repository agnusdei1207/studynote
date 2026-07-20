---
title: "Circuit Breaker"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 128
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Circuit Breaker는 <strong>원격 서비스 호출 실패가 임계치를 초과하면 자동으로 회로를 열어(Open) 호출을 차단</strong>하고, 일정 시간 후 반 열림(Half-Open)으로 복구를 시도하는 MSA 복원력(Resilience) 패턴이다.
> 2. **가치**: Circuit Breaker 없이 서비스 B가 장애이면 서비스 A가 <strong>타임아웃까지 대기->스레드 고갈->A도 장애(Cascading Failure)</strong>가 발생하지만, Circuit Breaker가 <strong>즉시 폴백(Fallback) 응답</strong>을 반환하여 장애 전파를 차단한다.
> 3. **판단 포인트**: Closed(정상)->Open(차단)->Half-Open(복구 시도)의 3가지 상태를 이해하고, Hystrix(Netflix, 레거시)->Resilience4j(Java 표준)->Istio(서비스 메시)의 구현 진화를 파악해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Circuit Breaker 상태 전이                          |
+-------------------------------------------------------+
|  [Closed — 정상]                                      |
|   모든 요청 통과, 실패 카운트                        |
|   실패 > 임계치 -> Open                               |
|                                                       |
|  [Open — 차단]                                        |
|   모든 요청 즉시 거부, Fallback 반환                 |
|   타이머 만료 -> Half-Open                            |
|                                                       |
|  [Half-Open — 복구 시도]                              |
|   일부 요청 통과하여 테스트                           |
|   성공 -> Closed / 실패 -> Open                       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Circuit Breaker는 전기의 <strong>차단기(브레이커)</strong>이다. 과전류(장애)가 흐르면 자동으로 차단하여 화재(Cascading Failure)를 방지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Fallback 전략

| 전략 | 설명 |
|:---|:---|
| **캐시 반환** | 이전 성공 응답 반환 |
| **기본값** | 정적 기본값 제공 |
| <strong>대체 서비스</strong> | 다른 서비스 호출 |
| **에러 반환** | 사용자에게 에러 안내 |

- **📢 섹션 요약 비유**: Fallback은 비상구이다. 정문(서비스)이 막히면 비상구(대체)로 나간다.

---

## Ⅲ. 비교 및 연결

| 비교 | CB 없음 | CB 있음 |
|:---|:---|:---|
| **장애 전파** | Cascading | **차단** |
| <strong>응답 시간</strong> | 타임아웃까지 대기 | <strong>즉시 Fallback</strong> |
| <strong>복구</strong> | 수동 | **자동 (Half-Open)** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Circuit Breaker 구현

| 도구 | 특징 |
|:---|:---|
| **Resilience4j** | Java 표준, 경량 |
| <strong>Istio</strong> | 서비스 메시, 코드 무관 |
| **Envoy** | 프록시 레벨 CB |

---

## Ⅴ. 기대효과 및 결론

Circuit Breaker는 <strong>MSA 복원력의 가장 기본적이고 중요한 패턴</strong>이며, Retry·Timeout·Bulkhead와 함께 복합 적용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Circuit Breaker</strong> | 장애 전파 차단 |
| <strong>Fallback</strong> | 대체 응답 전략 |
| **Cascading Failure** | CB가 방지하는 연쇄 장애 |
| <strong>Bulkhead</strong> | 격벽 패턴 (리소스 격리) |
| **Retry** | 재시도 (CB와 함께 사용) |

### 📈 관련 키워드 및 발전 흐름도

```text
[직접 호출 (장애 전파, ~2010s)]
    |
    v
[Hystrix (Netflix, 2012~) — 최초 CB 라이브러리]
    |
    v
[Resilience4j (2018~) — Hystrix 대체, Java 표준]
    |
    v
[서비스 메시 CB (Istio/Envoy, 2018~) — 코드 무관]
    |
    v
[현재: 자동 CB 튜닝 — AI가 임계치 자동 조정]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Circuit Breaker는 전기의 <strong>차단기(브레이커)</strong>예요.
2. 과전류(장애)가 흐르면 **자동으로 끊어서** 화재(연쇄 장애)를 막아요.
3. 잠시 기다렸다가 **살짝 켜보고(Half-Open)**, 안전하면 다시 정상으로 돌아가요!
