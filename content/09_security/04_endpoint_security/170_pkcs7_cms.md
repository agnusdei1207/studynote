---
title: "Pkcs7 Cms"
date: "2026-04-05"
tags:
  - "studynote-security"
weight: 170
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PKCS#7 (Public-Key Cryptography Standards #7)과 그 표준화 후속 규격인 CMS (Cryptographic Message Syntax)는 원문, 전자서명, 수신자 복호화 정보, 인증서 체인을 한 컨테이너에 담는 암호 메시지 포장 문법이다.
> 2. **가치**: 서명 알고리즘과 암호 알고리즘만으로는 검증에 필요한 인증서 체인·수신자 정보·콘텐츠 타입을 함께 전달할 수 없는데, CMS는 이를 구조화해 S/MIME (Secure/Multipurpose Internet Mail Extensions), 코드 서명, 인증서 번들의 상호운용성을 만든다.
> 3. **판단 포인트**: CMS는 신뢰 자체를 보장하는 기술이 아니라 신뢰 판단 재료를 운반하는 형식이므로, SignedData·EnvelopedData 선택, attached/detached 방식, 인증서 포함 범위를 목적에 맞게 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

PKCS#7/CMS는 암호 연산 결과를 "교환 가능한 문서"로 만드는 표준 컨테이너다. 공개키 기반 구조 (PKI, Public Key Infrastructure)에서는 원문이나 암호문만 주고받아서는 실제 서비스가 동작하지 않는다. 누가 서명했는지, 어떤 인증서로 검증할지, 여러 수신자 중 누가 복호화할 수 있는지, 원문이 내부에 포함됐는지 외부에 따로 있는지까지 함께 알아야 검증기와 수신기가 같은 해석을 할 수 있다.

이 표준이 필요한 이유는 알고리즘과 파일 형식이 서로 다른 층위의 문제이기 때문이다. RSA (Rivest-Shamir-Adleman)나 AES (Advanced Encryption Standard)는 각각 서명·암호화 연산을 수행하지만, "이 결과를 어떤 구조로 전달할 것인가"는 스스로 정해 주지 않는다. 제품마다 제각각 포맷을 쓰면 메일 클라이언트, 운영체제, 게이트웨이, 서명 검증 도구가 서로 호환되지 않는다. PKCS#7이 이를 처음 정리했고, 이후 IETF (Internet 엔진ering Task Force)가 CMS로 일반화하면서 알고리즘 확장성과 상호운용성이 더 좋아졌다.

아래 그림은 CMS가 왜 "포장 표준"인지 보여 준다.

```text
+----------------------------------------------------------------------+
| Raw crypto output vs CMS container                                   |
+--------------------------+-------------------------------------------+
| Raw signature / cipher   | CMS container                            |
| - payload location vague | - content type identified                |
| - cert chain separate    | - signer / recipient metadata bundled    |
| - recipient list unclear | - certificates can travel together       |
| - tool-specific parsing  | - common syntax across products          |
+--------------------------+-------------------------------------------+
```

핵심은 CMS가 암호학적 강도를 높이는 장치가 아니라, <strong>암호 결과가 해석될 문맥을 고정하는 장치</strong>라는 점이다. 그래서 PKI 환경에서는 알고리즘 선택만큼이나 포맷 일관성이 중요하다.

- **📢 섹션 요약 비유**: 자물쇠만 튼튼하다고 택배가 완성되는 것은 아니다. 상자 안에 무엇이 들었는지, 누구만 열 수 있는지, 보증서가 어디 붙었는지까지 정리된 송장과 포장이 있어야 제대로 전달된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CMS의 외곽 구조는 `ContentInfo`다. 이 바깥 래퍼 안에 "이 안에 든 메시지가 SignedData인지, EnvelopedData인지"를 식별하는 OID (Object Identifier)와 실제 내용을 넣는다. 내부 표현은 ASN.1 (Abstract Syntax Notation One)으로 정의되고, 바이너리 직렬화는 BER (Basic Encoding Rules)나 DER (Distinguished Encoding Rules)를 사용한다. 즉 CMS는 "무엇을 담을지"와 "바이트로 어떻게 표현할지"를 함께 규정한다.

| CMS content type | 보안 성질 | 대표 용도 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| SignedData | 무결성, 서명자 식별 | 전자서명, 코드 서명, `.p7m` | 원문 포함 여부(attached/detached), 다중 서명 가능 |
| EnvelopedData | 기밀성 | 보안 메일, 수신자별 암호화 전송 | 콘텐츠 암호화 키와 수신자별 키 래핑 구조 |
| AuthenticatedData | 무결성, 메시지 인증 코드 | 공유키 기반 보호 | 공개키 서명 대신 MAC (Message Authentication Code) 사용 |
| DigestedData / EncryptedData | 해시 또는 단순 암호화 | 특수 용도 | 오늘날은 SignedData, EnvelopedData가 주력 |
| Degenerate SignedData | 인증서/폐지목록 전달 | `.p7b` 인증서 번들 | 서명 없이 인증서 체인만 배포 가능 |

실무에서 가장 자주 보는 두 구조는 `SignedData`와 `EnvelopedData`다. `SignedData`는 원문 또는 원문의 참조를 기준으로 해시를 만들고, 서명자의 개인키로 서명값을 생성한 뒤, 검증에 필요한 인증서 체인을 함께 담을 수 있다. `EnvelopedData`는 먼저 대칭키로 원문을 암호화하고, 그 대칭키를 각 수신자의 공개키로 다시 감싸 수신자별 `RecipientInfo`를 만든다. 큰 데이터는 대칭키로 빠르게 암호화하고, 작은 키만 공개키로 포장하는 하이브리드 구조가 여기에서 표준화된다.

또한 CMS는 인증서와 인증서 폐지 목록 (CRL, Certificate Revocation List)을 함께 운반할 수 있어, 수신자가 검증에 필요한 부가 자료를 한 번에 확보하게 해 준다.

```text
+----------------------------------------------------------------------+
| Generic CMS packaging flow                                           |
+----------------------------------------------------------------------+
| Content ----------------------------------------------------------+  |
|   +- hash + signer private key ------------------------------+    |  |
|   |                                                          v    |  |
|   |                                                    SignerInfo  |  |
|   +- content-encryption key (CEK) ----------------------+          |  |
|   |                                                     v          |  |
|   |                                           EncryptedContent     |  |
|   +- CEK wrapped for each recipient ----------------+              |  |
|                                                      v              |  |
|                                                RecipientInfo        |  |
| Certificates / CRLs ------------------------------> Bundle          |  |
|                                                                    |  |
| Final CMS = ContentInfo { type + payload + metadata } ------------+  |
+----------------------------------------------------------------------+
```

여기서 중요한 선택이 `attached`와 `detached`다. 원문을 컨테이너 안에 넣으면 전달 편의성은 좋아지지만 파일이 커지고, 원문을 밖에 두면 같은 원본에 대한 서명 검증을 여러 시스템이 반복하기 쉽다. 코드 서명이나 대용량 배포에서는 detached 구조가, 메일 첨부처럼 한 덩어리 전송이 필요한 경우에는 attached 구조가 자주 쓰인다.

- **📢 섹션 요약 비유**: CMS는 선물상자라기보다 물류 허브 박스에 가깝다. 내용물, 봉인 스티커, 받는 사람별 열쇠, 보증서 묶음까지 각각의 칸에 넣어 두기 때문에 여러 사람이 같은 규칙으로 상자를 열 수 있다.

---

## Ⅲ. 비교 및 연결

PKI 문서들은 이름이 비슷해 보여도 역할이 다르다. CMS를 제대로 이해하려면 인증서 서명 요청 (CSR, Certificate Signing Request), 인증서, 키 백업 컨테이너와의 경계를 분명히 해야 한다.

| 형식 | 무엇을 담는가 | 개인키 포함 | 주 용도 |
| :--- | :--- | :--- | :--- |
| PKCS#10 CSR | 공개키, 신청자 정보, 신청자 서명 | 없음 | 인증서 발급 요청 |
| X.509 인증서 | 공개키, 주체 정보, 인증기관 서명 | 없음 | 신뢰 배포와 검증 |
| CMS / PKCS#7 | 콘텐츠, 서명, 수신자 정보, 인증서 체인 | 없음 | 서명 메시지, 암호 메시지, 인증서 번들 |
| PKCS#12 | 인증서와 개인키 묶음 | 있음 | 백업, 사용자 인증서 이동 |

CMS는 인증서를 "만드는" 형식이 아니라 <strong>이미 존재하는 인증서와 서명 결과를 운반하는 형식</strong>이다. 그래서 앞 단계의 PKCS#10, 뒤 단계의 X.509·PKCS#12와 연결되지만 역할은 겹치지 않는다. 또 웹 API (Application Programming Interface) 영역의 JOSE (JavaScript Object Signing and Encryption)가 JSON 친화적이라면, CMS는 X.509 인증서·ASN.1 기반 생태계에 더 강하다. 즉 둘 다 서명과 암호화를 다루지만, **운반 문법과 주변 생태계가 다르다**.

이 차이는 활용처로도 이어진다. S/MIME는 CMS를 이용해 메일 본문과 첨부파일을 서명·암호화하고, Microsoft Authenticode는 실행 파일 해시에 대한 서명 정보를 CMS 구조로 붙인다. 인증서 배포용 `.p7b`는 실질적으로 서명 없는 `SignedData` 변형을 이용해 체인만 전달한다.

- **📢 섹션 요약 비유**: PKCS#10은 입사 지원서, X.509는 합격 증명서, PKCS#12는 신분증과 도장까지 넣은 개인 가방이고, CMS는 그 서류와 물건들을 실제 전달 상황에 맞게 포장해 보내는 배송 상자다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서 CMS를 선택할 때는 "무엇을 보호할 것인가"보다 "검증자와 수신자가 어떤 재료를 받아야 동작하는가"를 먼저 따져야 한다. 예를 들어 인증서 체인만 배포할 때는 `.p7b` 형태의 certificate bundle이면 충분하지만, 메일 본문 무결성과 송신자 식별이 필요하면 `SignedData`, 특정 수신자만 읽게 해야 하면 `EnvelopedData`가 필요하다. 두 요구가 모두 있으면 sign-then-encrypt처럼 중첩 구조를 사용한다.

### 실무자 판단 체크리스트

1. 검증자에게 중간 인증서까지 제공해야 하는가, 아니면 신뢰 루트는 이미 배포돼 있는가?
2. 원문을 컨테이너 안에 넣는 attached 방식이 필요한가, 아니면 detached 서명이 더 효율적인가?
3. 수신자가 여러 명이면 `RecipientInfo`를 수신자별로 넣어야 하는가?
4. 법적 증적이나 장기 보존이 필요하면 장기검증 (LTV, Long-Term Validation) 확장까지 고려했는가?
5. CMS가 필요한 것인지, 개인키 포함이 필요한 PKCS#12가 필요한 것인지 역할을 혼동하지 않았는가?

### 자주 발생하는 안티패턴

- 루트 인증서까지 무조건 동봉해 "들어 있으면 신뢰된다"고 오해하는 것
- 중간 인증서를 누락해 검증 체인이 끊기는 것
- `.p7b`와 `.p12`를 혼동해 개인키가 없는 파일로 복호화나 클라이언트 인증을 기대하는 것
- 확장자만 보고 보안 속성을 판단하고, 내부 content type을 확인하지 않는 것

CMS는 특히 엔드포인트 보안에서 유용하다. 메일 클라이언트, 운영체제, 게이트웨이 장비가 서로 다른 공급사 제품이어도, CMS를 기준으로 서명값·인증서 체인·수신자 정보를 일관되게 파싱할 수 있기 때문이다. 반대로 ASN.1 파서 취약점이나 지원하지 않는 알고리즘 조합은 오히려 공격면이 되므로, 호환 알고리즘 집합과 파서 검증이 함께 중요하다.

- **📢 섹션 요약 비유**: 같은 상자라도 냉장 택배, 서류 봉투, 금고 운송 케이스는 목적이 다르다. 무엇을 보내는지에 따라 포장 방식과 동봉 서류를 다르게 골라야 사고가 나지 않는다.

---

## Ⅴ. 기대효과 및 결론

CMS의 가장 큰 효과는 <strong>상호운용성 있는 암호 메시지 유통</strong>이다. 서명, 암호화, 인증서 체인을 각각 따로 관리하던 복잡성을 하나의 문법으로 묶으면서, 메일·코드 서명·문서 보관 시스템이 같은 기본 구조를 공유할 수 있게 됐다. 다중 서명, 다중 수신자, 인증서 번들 같은 확장도 같은 프레임 안에서 다룰 수 있다.

하지만 CMS만 있다고 신뢰가 성립하는 것은 아니다. 인증서 경로 검증, 폐지 확인, 타임스탬프, 정책 식별, 신뢰 루트 배포는 여전히 별도의 운영 문제다. 또한 ASN.1 기반 포맷 특성상 구현 복잡도가 높고, 파서 품질이 약하면 오히려 취약점이 생길 수 있다. 앞으로는 CAdES (CMS Advanced Electronic Signatures) 같은 장기 전자서명 확장과 포스트 양자 암호 (PQC, Post-Quantum Cryptography) 알고리즘 수용이 더 중요해질 것이다.

결국 PKCS#7/CMS는 "암호 기술 그 자체"보다 <strong>암호 결과를 안전하게 운반하는 표준 배송 규격</strong>으로 기억하는 것이 정확하다. 신뢰는 정책과 검증이 만들고, CMS는 그 신뢰 재료를 분실되지 않게 묶어 전달한다.

- **📢 섹션 요약 비유**: 좋은 포장 상자는 내용물을 대신해 주지 않지만, 내용물이 끝까지 제모습을 유지하도록 지켜 준다. CMS는 암호기술의 힘을 현장까지 안전하게 실어 나르는 운송 상자다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PKCS#10 CSR (Certificate Signing Request) | 인증서 발급 요청 단계에서 앞서 사용되는 입력 문서 |
| X.509 인증서 | CMS 내부에 동봉돼 서명 검증과 체인 구성을 돕는 신뢰 재료 |
| PKCS#12 | CMS와 달리 개인키까지 담을 수 있는 이동·백업 컨테이너 |
| S/MIME (Secure/Multipurpose Internet Mail Extensions) | CMS를 메일 서명·암호화에 적용한 대표 응용 |
| Authenticode | 실행 파일 해시에 대한 서명을 CMS 기반으로 전달하는 코드 서명 체계 |
| ASN.1 / DER | CMS 구조와 인코딩을 정의하는 표현 문법과 직렬화 규칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
Key pair and certificate issuance
            |
            v
PKCS#10 CSR submission
            |
            v
X.509 certificate issuance
            |
            v
CMS ContentInfo packaging
      +-----+---------------+
      v                     v
 SignedData            EnvelopedData
      |                     |
      +------------+--------+
                   v
S/MIME / code signing / certificate bundle distribution
```

이 흐름은 "키 발급 준비 -> 인증서 확보 -> 서명·암호문 포장 -> 실제 배포 채널 적용"으로 CMS가 PKI 운용의 중간 배송 계층에 놓인다는 점을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CMS는 편지, 도장, 열쇠, 보증서를 한 상자에 차곡차곡 넣어 보내는 특별한 포장 상자예요.
2. 그래서 받는 사람은 상자 하나만 열어도 누가 보냈는지, 열쇠는 누구 것인지, 진짜 보증서가 맞는지 함께 확인할 수 있어요.
3. 하지만 상자가 있다고 해서 무조건 믿는 것은 아니고, 안에 든 보증서가 진짜인지도 꼭 살펴봐야 해요.
