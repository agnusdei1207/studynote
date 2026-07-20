---
title: "DID Document Public Key"
date: "2026-05-01"
tags:
  - "studynote-ict-convergence"
weight: 53
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DID 문서 (DID Document)는 DID (Decentralized Identifier)에 연결된 공개 메타데이터와 검증 수단을 담는 자료다.
> 2. **가치**: 공개키 (Public Key), verification method, service endpoint를 통해 중앙 CA 없이도 인증과 검증을 수행한다.
> 3. **판단 포인트**: DID 식별자, DID 문서, DID Resolver, 검증 관계를 분리해 설명해야 구조가 선명해진다.

---

## Ⅰ. 개요 및 필요성

분산 신원에서는 중앙 서버가 "이 사람이 누구인지"를 대신 증명해 주지 않는다. 대신 사용자가 자신의 식별자와 키를 직접 관리하고, 상대는 공개 정보를 바탕으로 검증한다.

DID 문서는 이때 필요한 공개 정보 묶음이다. 누가 서명할 수 있는지, 어떤 서비스로 연결되는지, 어떤 키가 유효한지를 알려 준다.

- **📢 섹션 요약 비유**: DID 문서는 집 주소와 열쇠 정보가 적힌 신분증 표지판과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DID는 식별자이고, DID 문서는 그 식별자에 대한 상세 설명서다. Resolver가 DID를 조회하면 DID 문서가 나오고, 그 안의 verification method로 서명 검증을 수행한다.

```text
DID -> DID Resolver -> DID Document
                     +- verificationMethod (public key)
                     +- authentication
                     +- assertionMethod
                     +- service
```

| 구성 요소 | 역할 | 예시 |
| :--- | :--- | :--- |
| DID | 주체 식별자 | did:example:123 |
| DID Document | 공개 메타데이터 | 키, 서비스, 관계 |
| verificationMethod | 검증 수단 | 공개키 |
| authentication | 로그인 검증 | 서명 확인 |
| service | 외부 연결점 | VC 발급 엔드포인트 |

핵심은 공개키를 문서에 직접 "노출"하는 것이 아니라, 검증 가능한 관계로 선언하는 것이다. 그래서 키 회전과 다중 키 운영이 가능하다.

- **📢 섹션 요약 비유**: DID 문서는 열쇠 자체가 아니라, 어떤 열쇠가 진짜인지 알려 주는 자물쇠 설명서다.

---

## Ⅲ. 비교 및 연결

DID 문서는 기존 PKI (Public Key Infrastructure) 인증서와 비슷해 보이지만, 중심 철학이 다르다. PKI는 CA 중심의 신뢰 체계이고, DID는 주체 중심의 분산 신뢰 체계다.

| 항목 | PKI / X.509 | DID Document |
| :--- | :--- | :--- |
| 신뢰 기준 | CA | DID method / ledger |
| 키 관리 | 인증서 기반 | 문서 기반 |
| 제어권 | 중앙 성격 강함 | 주체 중심 |
| 활용 | 웹 TLS | 분산 신원, VC/VP |

DID 문서는 Verifiable Credential (VC)과 Verifiable Presentation (VP)의 기반이 된다. 누가 발급자이고, 누가 보유자이며, 어떤 키로 검증할지 여기서 결정한다.

- **📢 섹션 요약 비유**: PKI는 관공서 도장, DID 문서는 개인이 직접 들고 다니는 공증 카드와 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 키 회전, 서비스 엔드포인트 변경, 여러 검증 관계를 어떻게 관리할지가 핵심이다. 공개키는 바뀔 수 있으므로, 문서 갱신과 해석 규칙이 중요하다.

### 체크리스트

1. DID Document에 필요한 verification relationship이 분리되어 있는가?
2. 키 회전과 복구 절차가 정의되어 있는가?
3. Resolver가 최신 문서를 안정적으로 조회하는가?
4. 서비스 endpoint와 인증 범위가 명확한가?

### 안티패턴

- 공개키를 비밀키처럼 취급하는 경우
- 문서와 실제 서비스 상태가 불일치하는 경우
- DID와 인증서의 차이를 설명하지 못하는 경우

실무 관점에서는 DID 문서가 단순 JSON이 아니라, 분산 신원에서 검증 경로를 표준화하는 핵심 객체라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: DID 문서는 연락처와 자물쇠 그림이 함께 있는 명함이다.

---

## Ⅴ. 기대효과 및 결론

DID 문서와 공개키 구조는 중앙 기관 의존도를 낮추고, 사용자가 자신의 신원을 더 세밀하게 통제하게 해 준다.

정리하면, DID 문서는 "이 식별자를 어떻게 믿고, 어떻게 검증할지"를 적어 둔 공개 계약서다.

- **📢 섹션 요약 비유**: DID 문서는 친구에게 "이 번호로 전화하고, 이 열쇠로 열어도 돼"라고 적어 둔 안내문이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| DID | 분산 식별자 |
| DID Document | 공개 설명서 |
| Public Key | 검증 수단 |
| Resolver | 조회기 |
| VC / VP | 신원 증명 |

### 📈 관련 키워드 및 발전 흐름도

```text
ID / Password
    |
    v
PKI / Certificate
    |
    v
DID
    |
    v
DID Document / VC / VP
```

이 흐름은 중앙 인증에서 주체 중심 검증으로 이동하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. DID 문서는 내 이름표 옆에 붙은 열쇠 안내판이에요.
2. 친구는 안내판을 보고 진짜인지 확인해요.
3. 그래서 가운데 아저씨 없이도 서로 믿을 수 있어요.
