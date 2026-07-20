---
title: "Hub And Spoke Architecture Eai"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 144
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Hub-and-Spoke 심화에서 Hub는 <strong>메시지 변환(Transformation)·라우팅(Routing)·오케스트레이션(Orchestration)·프로토콜 변환</strong>을 수행하며, 어댑터(Spoke)가 각 시스템과의 연결을 담당한다.
> 2. **가치**: Hub의 정규 데이터 모델(Canonical Data Model)로 <strong>N개 시스템의 데이터 포맷을 통일</strong>하면, 새 시스템 추가 시 어댑터 1개만 추가하면 된다.
> 3. **판단 포인트**: Hub의 HA(고가용성)·성능 확장이 핵심이며, ESB는 Hub를 분산 버스로 확장한 것이다.

---

## Ⅰ. 개요 및 필요성

```text
Hub 핵심 기능:
  Transformation: A포맷 -> 정규모델 -> B포맷
  Routing: 조건별 목적지 결정
  Orchestration: 다단계 프로세스 조합
  어댑터(Spoke): JDBC·REST·FTP·MQ 연결
```

- **📢 섹션 요약 비유**: Hub는 <strong>번역 사무소</strong>이다. 각 나라(시스템)의 언어(포맷)를 공통어(정규 모델)로 번역하여 전달한다.

---

## Ⅱ~Ⅴ. 결론

Hub의 정규 데이터 모델과 어댑터 패턴이 <strong>확장성의 핵심</strong>이며, ESB·iPaaS로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Hub</strong> | 중앙 변환·라우팅 |
| **Spoke** | 어댑터 (시스템 연결) |
| **정규 모델** | Canonical Data Model |
| **Transformation** | 포맷 변환 |
| <strong>ESB</strong> | Hub 분산 확장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[P2P] -> [Hub-and-Spoke (2000s)]
    -> [Canonical Data Model (표준화)]
    -> [ESB (분산 Hub, 2005~)]
    -> [현재: iPaaS — 클라우드 Hub]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Hub는 <strong>번역 사무소</strong>예요. 영어·한국어·일본어를 <strong>공통어로 번역</strong>해요.
2. 새 나라(시스템)가 오면 <strong>통역사(어댑터) 1명만</strong> 추가하면 돼요.
3. 번역 사무소가 <strong>바빠지면(SPOF)</strong> 지점(ESB)을 여러 개 만들어요!
