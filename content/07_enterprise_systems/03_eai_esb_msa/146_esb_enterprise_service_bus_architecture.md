---
title: "Esb Enterprise Service Bus Architecture"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 146
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ESB는 <strong>Hub-and-Spoke의 Hub를 분산 메시징 버스로 확장</strong>한 통합 미들웨어이며, 메시지 변환·라우팅·오케스트레이션·프로토콜 중재·보안을 <strong>표준화된 버스 인프라</strong>에서 수행한다.
> 2. **가치**: Hub의 SPOF 문제를 <strong>분산 버스</strong>로 해결하고, SOA(Service Oriented Architecture)의 <strong>서비스 연결 백본</strong>으로 기능하며, WSDL·SOAP·XML 기반 표준 통합을 제공한다.
> 3. **판단 포인트**: MuleSoft·TIBCO·IBM Integration Bus가 대표이며, MSA 시대에는 <strong>ESB의 무거운 중앙 집중이 안티패턴</strong>으로 간주되어 Kafka·이벤트 기반으로 전환 중이다.

---

## Ⅰ. 개요 및 필요성

```text
ESB 핵심 기능:
  메시지 변환: XML↔JSON, SOAP↔REST
  라우팅: 콘텐츠 기반·규칙 기반
  오케스트레이션: BPEL 워크플로
  프로토콜 중재: HTTP·MQ·FTP·JDBC
```

- **📢 섹션 요약 비유**: ESB는 <strong>고속도로 인터체인지</strong>이다. 다양한 방향(프로토콜)의 차량(메시지)을 자동으로 안내한다.

---

## Ⅱ~Ⅴ. 결론

ESB는 <strong>SOA 시대의 통합 표준</strong>이지만, MSA에서는 Kafka·이벤트 기반이 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ESB** | 분산 서비스 버스 |
| <strong>SOA</strong> | 서비스 지향 아키텍처 |
| **MuleSoft** | 대표 ESB |
| <strong>SOAP/WSDL</strong> | 표준 프로토콜 |
| <strong>Kafka</strong> | MSA 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Hub-and-Spoke (2000s)] -> [ESB (TIBCO·MuleSoft, 2005~)]
    -> [SOA + ESB (전성기, 2008~)]
    -> [MSA + Kafka (ESB 대체, 2015~)]
    -> [현재: iPaaS — 클라우드 통합 플랫폼]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ESB는 <strong>고속도로 인터체인지</strong>예요. 여러 방향의 차를 <strong>자동 안내</strong>해요.
2. 서울->부산, 대전->광주 차들이 <strong>인터체인지에서 방향</strong>을 바꿔요.
3. 하지만 너무 **복잡해져서** 요즘은 Kafka(우편함)로 바꾸고 있어요!
