---
title: "Biometric Auth FIDO2 Passkey Authentication"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 702
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FIDO2는 W3C WebAuthn과 FIDO Alliance CTAP2로 구성된 공개키 기반(passwordless) 인증 표준이며, Passkey는 이 표준 위에서 RP(Relying Party)·Authenticator·User Verification(생체/PIN) 결합을 통해 비밀번호·OTP·SMS 인증을 대체하는 credential(공개키+개인키 쌍)이다.
> 2. **가치**: 피싱·크리덴셜 스터핑·MFA 피로 공격을 원천 차단(Origin-bound + no shared secret)하며, Google·Microsoft·Apple의 디바이스/클라우드 생태계로 동기화되어 사용자 평균 로그인 시간 50% 절감, 헬프데스크 비밀번호 리셋 비용 약 70% 감소 효과를 입증했다.
> 3. **판단 포인트**: Synced Passkey(클라우드 동기화)와 Device-bound Passkey(하드웨어 토큰) 중 도메인별 위기관리·규제(금융/공공) 요건을 충족하는 모델 선택, 그리고 Resident Key(`rk=true`)·PRF Extension·Conditional UI 도입 여부가 UX와 보안성의 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

전통적인 지식 기반 인증(비밀번호)과 보유 기반 인증(OTP, SMS)은 ① 피싱(Phishing) ② 크리덴셜 스터핑 ③ 중간자 공격(MitM) ④ SIM 스위핑 ⑤ MFA 피로 공격(Fatigue Attack)에 모두 취약하다. Verizon DBIR 2024 기준 80% 이상의 해킹 침해 사고가 자격 증명 탈취에서 시작되며, Microsoft·Google 자체 조사에서도 피싱 성공률 1% 미만인 키리스 인증 도입 후 계정 탈취가 99.9% 감소했다.

FIDO2는 이 문제를 **“비밀대칭 키(Asymmetric Key Cryptography) + Origin 바인딩 + 로컬 사용자 검증”** 의 3축으로 해결한다. 사용자는 비밀번호를 기억하지 않고, 단말기 내 보안 영역(TPM/SE/StrongBox)에 격리된 개인키로 서명하며, 사이트의 Origin이 변경되면 인증이 즉시 실패하므로 피싱이 구조적으로 불가능해진다.

여기에 Passkey는 FIDO2 credential에 **동기화(Synchronization)** 와 **계정 간 이전(Portability)** 의 사용성 레이어를 얹어, “키리스(Keyless) + 동기화(Synced)” 형태로 대중적 채택을 가능케 하였다. 2022년 5월 Apple·Google·Microsoft의 공동 확장성 사양 이후 2023년 “Passkey” 브랜드로 정착, 2024년 10월 현재 Google Workspace·Microsoft Entra ID·PayPal·eBay·카카오·NAVER 등에서 상용 적용 중이다.

```text
   기존 패러다임(공유 비밀 기반)                  FIDO2/Passkey 패러다임(공개키 기반)
   +------------------------+                 +----------------------------------+
   |  User  --password--->  RP Server         |  User  --biometric/PIN--->  AuthN |
   |  (DB에 hash 저장,       |                |        |                          |
   |   동일 secret 공유)     |                |        v 서명(Sign with privKey) |
   |   ^ phishing risk       |                |  RP Server --verify(pubKey)--->  |
   |   ^ DB leak -> 전사용자  |                |        ^                        |
   |   ^ replay 가능        |                |        | challenge 매번 1회성    |
   +------------------------+                 +----------------------------------+
            |                                              |
            v                                              v
   단일 실패 지점(Single Point of Failure)     단일 실패 지점 제거 (서버는 pubKey만 보관)
```

**기존 vs 신규 패러다임 비교**

| 항목 | 기존(SMS/OTP/비밀번호) | FIDO2/Passkey |
|---|---|---|
| 검증 방식 | 공유된 secret(대칭) | 공개키 서명(비대칭) |
| 피싱 내성 | 없음 | Origin-bound로 구조적 차단 |
| 자격증명 유출 시 피해 | 동일 secret 재사용 -> 전 서비스 피해 | pubKey만 노출, 개인키 부재 시 무용 |
| UX | OTP 복사/입력, 비밀번호 변경 | 생체 1탭, 동기화로 단일 등록 |
| 라이프사이클 | 분기/연 단위 강제 변경 | 키 폐기 시점에 자유, 동기화 자동 |

- **📢 섹션 요약 비유**: 비밀번호는 "집 열쇠 복사본을 발신인 불명의 택배기사가 들고 다니는 것"이고, FIDO2/Passkey는 "본인 지문으로만 열리고, 어떤 사이트에서 왔는지 자체를 확인한 뒤 응답하는 호텔 키 카드"이다. 택배기사가 위조 열쇠를 만들어도 호텔은 그 열쇠가 맞는 카드인지 무시하고, 지문과 발신처가 다르면 문이 열리지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FIDO2는 다음 4계층 구조를 가진다.

```text
         +-----------------------------------------------------+
         |  Relying Party (RP) — Web Service / SSO IdP          |
         |  +----------------------+                            |
         |  | Server-Side:          |                            |
         |  |  • challenge 생성     |                            |
         |  |  • pubKey 저장        |                            |
         |  |  • signature 검증     |                            |
         |  +----------------------+                            |
         |            ^                                         |
         |            | HTTPS / JSON                            |
         +------------+-----------------------------------------+
                      |
                      v
         +-----------------------------------------------------+
         |  Client (Browser/OS) — WebAuthn API Layer            |
         |  +----------------------+  +----------------------+ |
         |  | navigator.credentials|  | PublicKeyCredential  | |
         |  |  .create() / .get()  |  |    (DOM Object)      | |
         |  +----------------------+  +----------------------+ |
         +------------+-----------------------------------------+
                      |  CTAP2 over USB / NFC / BLE / Internal
                      v
         +-----------------------------------------------------+
         |  Authenticator                                         |
         |  +--------------+ +--------------+ +--------------+ |
         |  | Platform:    | | Roaming:     | | Roaming:     | |
         |  | • Windows    | | • YubiKey 5  | | • Phone-as-  | |
         |  |   Hello(TPM) | | • Feitian    | |   Authenticator|
         |  | • Touch ID   | | • Solokey    | |   (Hybrid)   | |
         |  | • Face ID    | |              | |              | |
         |  +--------------+ +--------------+ +--------------+ |
         |  +----------------------------------------------+   |
         |  | Secure Enclave / TPM 2.0 / StrongBox (TEE)  |   |
         |  |  -> privKey 격리 저장, 서명 연산 전담          |   |
         |  +----------------------------------------------+   |
         +-----------------------------------------------------+
```

**Registration Ceremony (등록) 흐름**

```text
  User        Browser/OS        Authenticator       RP Server
   |               |                  |                  |
   | 1.회원가입 클릭|                  |                  |
   |--------------->| 2.create({pkOptions: {             |
   |               |   challenge, rp:{id,name},          |
   |               |   user:{id,name,displayName},       |
   |               |   pubKeyCredParams:[ES256,-7],      |
   |               |   authenticatorSelection:{          |
   |               |     residentKey:'required',          |
   |               |     userVerification:'required'}})   |
   |               |-------------------------------------->|
   |               |                  |                  | 3.challenge(nonce)생성
   |               |                  |                  |   32byte random
   |               |<-------CTAP2:makeCredential----------|
   |               |                  |                  |
   | 4.생체/PIN요구 |                  |                  |
   |<---------------|                  |                  |
   |   [지문/PIN]  |                  |                  |
   |--------------->|---UV verify--->   | 5.키쌍 생성:    |
   |               |                  |   (privKey, pubKey)|
   |               |                  |   privKey->SE저장 |
   |               |                  |   counter=0      |
   |               |                  | 6.attestation sig |
   |               |<--attestationObj-|   (privKey로 서명)|
   |               |                  |                  |
   |               | {id, rawId, response:{              |
   |               |   clientDataJSON,                   |
   |               |   attestationObject:{                |
   |               |     fmt,attStmt,authData:{          |
   |               |       rpIdHash,flags(UV/UP/AT),     |
   |               |       counter,                       |
   |               |       attestedCredentialData:{       |
   |               |         aaguid, credId, credPubKey  |
   |               |       }}}}}                           |
   |               |-------------------------------------->|
   |               |                  |                  | 7.attestation verify
   |               |                  |                  |   (Authenticator 신뢰)
   |               |                  |                  | 8.credId+pubKey DB저장
   |               |<----{status:ok}---------------------|
   | 9.완료       |                  |                  |
   |<---------------|                  |                  |
```

**Authentication Ceremony (로그인) 흐름**

```text
  User        Browser/OS        Authenticator       RP Server
   |               |                  |                  |
   | 1.로그인 클릭 |                  |                  |
   |               |----get({pkOptions:                  |
   |               |   challenge, rpId,                  |
   |               |   allowCredentials:[{               |
   |               |     type:'public-key',              |
   |               |     id:credId,                      |
   |               |     transports:['usb','nfc','ble']}|
   |               |   userVerification:'required'})----->|
   |               |                  |                  | 2.저장된 credId 조회
   |               |                  |                  |   counter 비교용
   |               |<-----CTAP2:getAssertion--------------|
   | 3.생체/PIN   |                  |                  |
   |<---------------|                  |                  |
   |--[지문/PIN]-->|---UV verify--->   | 4.privKey 로 서명|
   |               |                  |   sig = ECDSA(   |
   |               |                  |     privKey,      |
   |               |                  |     SHA256(challenge|
   |               |                  |        +clientData)|
   |               |                  |   counter++       |
   |               |<--assertionObj---|                  |
   |               | {id, rawId, response:{              |
   |               |   clientDataJSON,                   |
   |               |   authenticatorData:{               |
   |               |     rpIdHash,flags,signCount,       |
   |               |     extensions(HMAC,PRF...)},       |
   |               |   signature,                        |
   |               |   userHandle}}                      |
   |               |-------------------------------------->|
   |               |                  |                  | 5.signature 검증
   |               |                  |                  |   (pubKey + SHA256)
   |               |                  |                  | 6.counter > saved?  |
   |               |                  |                  |   (clone detection) |
   |               |                  |                  | 7.세션 발급(JWT/cookie)|
   |               |<--{token}----------------------------|
   | 8.로그인 완료|                  |                  |
   |<---------------|                  |                  |
```

### 구성 요소 및 핵심 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Relying Party (RP)** | 인증 주체(웹/앱 서버), 공개키·credId 저장, challenge/signature 검증 | WebAuthn Server Lib(예: `py_webauthn`, `webauthn-go`, `SimpleWebAuthn` Node.js) 사용. 검증 시 (1) clientDataJSON의 `type` 및 `origin` 검사, (2) rpIdHash와 서버 rpId의 SHA-256 일치, (3) signature를 credentialPublicKey로 `verify()` 호출, (4) signCount 단조증가 검증으로 클론 탐지 |
| **Client(WebAuthn API)** | 사용자와 Authenticator 사이의 중재자, JSON 인코딩/디코딩 | `navigator.credentials.create()`/`get()` 호출, base64url 인코딩, `PublicKeyCredential` 객체 처리. Conditional UI(`mediation:'conditional'`)로 username 필드에서 자동완성 제공 |
| **Authenticator** | 키쌍 생성·서명·생체/PIN 검증 수행, privKey 격리 보관 | (a) **Platform Authenticator**: TPM 2.0(Windows Hello), Secure Enclave(iOS/macOS), StrongBox(Android 9+)의 TEE에 privKey 저장. (b) **Roaming Authenticator**: YubiKey 5, Feitian K9, Token2. (c) **Phone-as-Authenticator**: Hybrid Transport(CTAP2.1) – QR+BLE+handshake 후 모바일 보안 영역 키 사용 |
| **CTAP2 Protocol** | Client ↔ Authenticator 간의 와이어 프로토콜 | USB HID / NFC ISO 14443 / BLE GATT. APDU 유사 명령(예: `0x01 authenticatorMakeCredential`, `0x02 authenticatorGetAssertion`). 핀/UV 프로토콜은 ISO 7816-4 VERIFY 기반 |
| **공개키 알고리즘** | 비대칭 서명 | `ES256`(ECDSA P-256 + SHA-256, WebAuthn -7, 가장 보편), `EdDSA`(Ed25519, -8), `RS256`(RSA, deprecated 추세). COSE 알고리즘 등록 |
| **Attestation** | Authenticator의 출처·무결성 입증 | (1) **Basic**: 제조사 자체 서명(Self), (2) **AttCA**: 제조사 CA 인증서 연쇄, (3) **AnonCA**: 익명화 CA로 동일 모델 식별. `fmt` 값으로 구분. RP는 MDS3(FIDO Alliance Metadata Service v3) 조회하여 AAGUID 검증 |
| **User Verification (UV)** | 사용자가 본인임을 로컬 검증 | `discouraged` / `preferred` / `required` 3단계. `required` 시 `flags.UV=1` & `authenticatorData`에 `UV count byte` 포함. 생체 False Accept Rate(FAR)는 보통 1/50,000 ~ 1/1,000,000 |
| **Extensions (확장)** | 부가 기능 | `prf`(HMAC-SHA256 파생키 -> credential 암호화 대체), `hmac-secret`(F