---
title: "Microservice Chassis"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 141
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Microservice Chassis는 <strong>로깅·설정·헬스체크·메트릭·보안 등 모든 마이크로서비스에 공통으로 필요한 횡단 관심사(Cross-cutting Concerns)를 프레임워크로 제공</strong>하여 보일러플레이트를 제거하는 패턴이다.
> 2. **가치**: 각 서비스가 로깅·트레이싱·설정 로딩을 개별 구현하면 <strong>중복·불일치</strong>가 발생하지만, Chassis가 표준화된 구현을 제공하면 <strong>일관성·개발 속도</strong>가 향상된다.
> 3. **판단 포인트**: Spring Boot(Java)·Go-kit(Go)·Dapr(사이드카 기반, 언어 무관)이 대표 Chassis이며, 서비스 메시(Istio)와 역할이 일부 중복된다.

---

## Ⅰ. 개요 및 필요성

```text
Chassis 제공 기능:
  로깅 (구조화, 표준 포맷)
  설정 (외부 설정, Config Server)
  헬스체크 (/health, /ready)
  메트릭 (/metrics, Prometheus)
  보안 (인증·인가, JWT)
  서킷 브레이커 (Resilience4j)
```

- **📢 섹션 요약 비유**: Chassis는 <strong>자동차 차대(프레임)</strong>이다. 엔진(비즈니스 로직)만 올리면 바퀴·핸들·브레이크(공통 기능)는 이미 있다.

---

## Ⅱ~Ⅴ. 결론

Microservice Chassis는 <strong>MSA 공통 기능의 표준화 프레임워크</strong>이며, Dapr(사이드카)가 언어 무관 차세대 Chassis이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Chassis** | 공통 관심사 프레임워크 |
| **Spring Boot** | Java Chassis |
| **Dapr** | 사이드카 Chassis |
| <strong>서비스 메시</strong> | 네트워크 레벨 Chassis |
| **Cross-cutting** | 횡단 관심사 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 보일러플레이트 (~2015)] -> [Spring Boot (2014, Java)]
    -> [Go-kit (Go)] -> [Dapr (2019, 사이드카)]
    -> [현재: Chassis + 서비스 메시 하이브리드]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Chassis는 자동차의 <strong>차대(프레임)</strong>예요. 바퀴·핸들·브레이크가 **이미 있어요**.
2. 개발자는 **엔진(비즈니스 로직)만** 만들면 돼요. 나머지는 Chassis가 제공해요.
3. 모든 차(서비스)가 <strong>같은 차대</strong>를 쓰면 <strong>부품 호환</strong>이 쉬워요!
