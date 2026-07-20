---
title: "Non Functional Requirements"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 133
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NFR(Non-Functional Requirements)은 <strong>시스템이 "어떻게" 동작해야 하는가의 품질 속성</strong>으로, 성능·보안·가용성·확장성·유지보수성 등을 정의하며 ISO 25010이 분류 표준이다.
> 2. **가치**: NFR이 <strong>아키텍처를 결정</strong>한다. "초당 10만 요청"이면 분산 아키텍처, "99.999% 가용성"이면 Active-Active 이중화가 필요하며, NFR 없이는 아키텍처 결정이 불가능하다.
> 3. **판단 포인트**: NFR은 <strong>측정 가능한 수치</strong>로 명세해야 검증 가능하다. "빨라야 한다"(✗) -> "P99 응답 시간 200ms 이내"(✓).

---

## Ⅰ. 개요 및 필요성

```text
ISO 25010 품질 모델 (8대 특성):
  기능 적합성, 성능 효율성, 호환성, 사용성,
  신뢰성, 보안, 유지보수성, 이식성
```

- **📢 섹션 요약 비유**: NFR은 자동차의 <strong>안전등급·연비·최고속도</strong>이다. "달린다"(FR)만으로는 차를 선택할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| NFR | 수치화 예 | 아키텍처 영향 |
|:---|:---|:---|
| <strong>성능</strong> | P99 < 200ms | 캐시, CDN |
| <strong>가용성</strong> | 99.99% | Active-Active |
| **확장성** | 10x 트래픽 | 오토스케일링 |
| **보안** | OWASP Top 10 | WAF, 암호화 |

---

## Ⅲ~Ⅴ. 결론

NFR은 <strong>아키텍처의 핵심 동인(Architecture Driver)</strong>이며, 수치로 명세하지 않으면 검증이 불가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **NFR** | 품질 속성 (How well) |
| **ISO 25010** | 8대 품질 특성 |
| <strong>ATAM</strong> | NFR 트레이드오프 분석 |
| **QAW** | 품질 속성 워크숍 |
| <strong>Architecture Driver</strong> | NFR이 아키텍처를 결정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 NFR (~2000s)] -> [ISO 9126 (2001)]
    -> [ISO 25010 (2011)] -> [QAW·ATAM (아키텍처 관점)]
    -> [현재: AI NFR 추출 — 요구사항에서 품질 속성 자동 식별]
```

### 👶 어린이를 위한 3줄 비유 설명
1. NFR은 자동차의 <strong>안전등급·연비·최고속도</strong>예요.
2. "달린다"(기능)만으로는 **좋은 차인지** 알 수 없어요.
3. "200km/h, 연비 15km/L"처럼 **숫자로 정확히** 적어야 비교할 수 있어요!
