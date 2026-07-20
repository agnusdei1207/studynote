---
title: "EAI (Enterprise Application Integration) - Hub-and-Spoke"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EAI Hub-and-Spoke는 <strong>중앙 Hub가 모든 애플리케이션 간 메시지 라우팅·변환·오케스트레이션</strong>을 수행하여 P2P 스파게티를 해소하는 통합 아키텍처이다.
> 2. **가치**: N개 시스템이 Hub에만 연결하면 <strong>N개 인터페이스</strong>만 필요(P2P는 N(N-1)/2)하며, 메시지 포맷 변환·라우팅 규칙을 Hub에서 중앙 관리한다.
> 3. **판단 포인트**: Hub가 <strong>단일 장애점(SPOF)·성능 병목</strong>이 될 수 있으며, 이를 해결하기 위해 ESB(분산 버스)로 진화했다.

---

## Ⅰ. 개요 및 필요성

```text
Hub-and-Spoke:
  시스템 A -> Hub -> 시스템 B
  시스템 C -> Hub -> 시스템 D
  Hub: 메시지 변환 + 라우팅 + 로깅
  -> N개 시스템 = N개 연결 (vs P2P의 N(N-1)/2)
```

- **📢 섹션 요약 비유**: Hub는 <strong>허브 공항</strong>이다. 모든 비행기(시스템)가 허브를 경유하여 목적지로 간다.

---

## Ⅱ~Ⅴ. 결론

Hub-and-Spoke는 <strong>P2P 스파게티의 해결책</strong>이지만, SPOF 문제로 ESB·이벤트 기반으로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Hub-and-Spoke</strong> | 중앙 통합 |
| <strong>Hub</strong> | 라우팅·변환 |
| <strong>SPOF</strong> | 단일 장애점 |
| <strong>ESB</strong> | 분산 버스 (진화) |
| **EAI** | 애플리케이션 통합 |

### 📈 관련 키워드 및 발전 흐름도

```text
[P2P (스파게티)] -> [Hub-and-Spoke (2000s)]
    -> [ESB (2005~, SPOF 해소)]
    -> [iPaaS (클라우드, 2015~)]
    -> [현재: 이벤트 기반 통합 (Kafka)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Hub는 <strong>허브 공항</strong>이에요. 모든 비행기가 <strong>허브를 거쳐</strong> 목적지로 가요.
2. 직항(P2P)보다 <strong>허브 경유</strong>가 노선(연결)이 적어요.
3. 하지만 허브가 **고장나면 전체가 멈추는** 문제(SPOF)가 있어요!
