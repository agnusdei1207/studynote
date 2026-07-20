---
title: "Mtls Mutual Tls"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 146
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: mTLS는 <strong>클라이언트와 서버가 양쪽 모두 인증서를 검증(상호 인증)</strong>하는 TLS 확장이며, 서비스 메시(Istio)에서 <strong>서비스 간 통신의 암호화·인증·무결성</strong>을 보장하는 핵심 메커니즘이다.
> 2. **가치**: 일반 TLS는 <strong>서버만 인증</strong>(클라이언트는 아무나)하지만, mTLS는 <strong>양쪽 모두 인증</strong>하여 Zero Trust 네트워크에서 "네트워크 내부라도 신뢰하지 않는" 원칙을 실현한다.
> 3. **판단 포인트**: 서비스 메시(Istio)가 <strong>자동 인증서 발급·회전·mTLS 적용</strong>을 사이드카에서 처리하므로, 애플리케이션 코드 변경 없이 적용된다.

---

## Ⅰ. 개요 및 필요성

```text
TLS:   클라이언트 -> 서버 인증서 검증 (서버만 인증)
mTLS:  클라이언트 ↔ 서버 양쪽 인증서 교환·검증
  -> Zero Trust: 내부 네트워크도 암호화
  Istio: 자동 인증서 발급 -> Envoy 사이드카에서 mTLS
```

- **📢 섹션 요약 비유**: TLS는 <strong>신분증 확인(서버만)</strong>, mTLS는 <strong>양쪽 모두 신분증 확인</strong>이다.

---

## Ⅱ~Ⅴ. 결론

mTLS는 <strong>Zero Trust·서비스 메시의 보안 핵심</strong>이며, Istio가 자동화를 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>mTLS</strong> | 상호 인증 |
| <strong>Zero Trust</strong> | 내부도 불신 |
| <strong>Istio</strong> | 자동 mTLS |
| <strong>인증서 회전</strong> | 자동 갱신 |
| **SPIFFE** | 서비스 ID 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[평문 통신 (~2015)] -> [TLS (서버 인증)]
    -> [mTLS (상호 인증, 2017~)]
    -> [Istio 자동 mTLS (2018)]
    -> [현재: SPIFFE/SPIRE — 서비스 ID 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. TLS는 <strong>가게(서버)만 신분증</strong>을 보여주는 거예요.
2. mTLS는 <strong>손님(클라이언트)도 신분증</strong>을 보여야 들어갈 수 있어요.
3. 이렇게 하면 <strong>가짜 손님</strong>이 못 들어와서 안전해요!
