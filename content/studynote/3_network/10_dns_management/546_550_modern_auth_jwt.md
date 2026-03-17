+++
title = "546-550. 최신 인증 및 토큰 기술 (OAuth, JWT, X.509)"
date = "2026-03-14"
[extra]
category = "DNS & Management"
id = 546
+++

# 546-550. 최신 인증 및 토큰 기술 (OAuth, JWT, X.509)

## # [최신 인증 및 토큰 기술]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 현대 보안의 핵심은 단순히 '누구인가(인증)'를 넘어, '무엇을 할 수 있는가(권한)'를 안전하게 위임하고 **비상태(Stateless)**로 검증하는 아키텍처로 전환되었다.
> 2. **가치**: **OAuth 2.0 (Open Authorization)**은 자격증명 노출 없이 권한 위임을 가능하게 하여 데이터 유출 사고를 근원적으로 차단하며, **JWT (JSON Web Token)**는 서버의 세션 저장 부하를 제거하여 대용량 트래픽 처리에 최적화되어 있다.
> 3. **융합**: **X.509** 기반의 **PKI (Public Key Infrastructure)**는 신뢰 기반을 담보하고, **OIDC (OpenID Connect)**는 이를 통합하여 SSO (Single Sign-On) 및 MSA (Microservices Architecture) 환경의 보안 표준으로 자리 잡았다.

+++

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
전통적인 인증 시스템(Cookie/Session 기반)은 서버가 사용자의 상태를 메모리나 DB에 저장(Stateful)해야 하므로, 서버가 확장될 때 세션 동기화 이슈(Sticky Session)가 발생한다. 또한, 제3자 애플리케이션에 내 서비스의 데이터를 제공할 때 ID/PW를 공유하는 방식은 보안상 치명적이다. 이를 해결하기 위해 등장한 것이 '토큰 기반 보안'이다. 이는 마치 현금(토큰)을 지갑에 넣고 다니며 물건을 사는 것과 같이, 사용자가 자격 증명을 휴대하고 서버는 단순히 그 증명서의 유효성만 검증하는 방식이다.

#### 등장 배경
1.  **기존 한계**: 서버 기반 세션의 확장성 한계(Scalability Issue) 및 제3자 앱으로의 자격증명 유출 위험.
2.  **혁신적 패러다임**: **RFC 6749** (OAuth 2.0) 및 **RFC 7519** (JWT) 표준화를 통해 "권한 위임(Delegation)"과 "무결성 검증(Integrity Verification)"을 분리.
3.  **현재 요구**: MSA 및 클라우드 환경에서 서버 간 통신, 모바일 앱, IoT 디바이스 인증의 표준 프로토콜으로 자리 잡음.

> **💡 비유**: 우리가 호텔에 체크인할 때, 방마다 다른 열쇠를 주는 것이 아니라, 나의 신분을 증명하는 '카드키'를 발급받아 엘리베이터와 수영장을 자유롭게 이용하는 것과 같습니다.

#### ASCII 다이어그램: 인증 패러다임 변천

```ascii
+--------------------------+        +--------------------------+
|       [Traditional]       |        |        [Modern]          |
|     Stateful Session      |        |     Stateless Token      |
+--------------------------+        +--------------------------+
| 1. Client sends ID/PW     |        | 1. Client sends ID/PW    |
| 2. Server verifies DB     |        | 2. Server verifies DB    |
| 3. Server creates Session |        | 3. Server issues Token   |
| 4. Stores Session in Mem  |        |    (Contains User Info)  |
|    (Bottleneck)           |        | 4. No Storage Needed     |
| 5. Returns Session ID     |        | 5. Returns Token Only    |
+--------------------------+        +--------------------------+
```
*   **해설**: 왼쪽은 서버가 사용자 상태를 기억해야 하므로 로그인 요청이 몰리면 서버 메모리가 부족해집니다. 오른쪽은 서버가 기억하지 않아도 되므로, 토큰(암호화된 정보)만 있으면 누구나 검증할 수 있어 확장이 쉽습니다.

> **📢 섹션 요약 비유**: 과거에는 호텔 출입구 경비원(서버)이 모든 손님의 얼굴을 기억하고 있어야 했다면, 이제는 손님 목에 '스마트 태그(토큰)'를 달아놓아 단말기가 울리기만 하면 통과시켜 주는 시스템으로 변화한 것입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 권한 위임을 위한 **OAuth 2.0**, 자체 수신성을 가진 **JWT**, 그리고 신뢰 체인을 위한 **X.509**의 구조를 심층 분석한다.

#### 1. 구성 요소 상세 분석

| Component (구성 요소) | Full Name (전체 명칭) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/표준 |
|:---|:---|:---|:---|:---|
| **Resource Owner** | - | 사용자 (본인) | 데이터 소유자이자 접근 권한을 부여하는 주체. 브라우저 또는 앱을 조작. | - |
| **Client** | - | 제3자 애플리케이션 | 사용자를 대신하여 리소스에 접근하고자 하는 소프트웨어. | HTTP/HTTPS |
| **Authorization Server** | - | 인증 서버 | 사용자를 인증하고 **Access Token**을 발행하는 '열쇠 제작소'. | OAuth 2.0 |
| **Resource Server** | - | 자원 서버 | 보호된 데이터(API, 이미지 등)를 보유하며, Token 유효성을 확인 후 제공. | RFC 6750 |
| **JWT** | JSON Web Token | 전자 서명된 토큰 | Header.Payload.Signature로 구성되어 위변조를 방지하는 클레임(Claim) 기반 토큰. | RFC 7519 |
| **X.509** | ITU-T X.509 | 디지털 인증서 | 공개키(Public Key)와 신원 정보를 CA의 개인키로 서명한 전자 신분증. | RFC 5280 |

#### 2. ASCII 아키텍처 다이어그램: OAuth 2.0 Authorization Code Flow

```ascii
      +--------+                               +---------------+
      |        |                               |               |
      |  User  |----------(1) Request Access-->|   Client      |
      |(RO)    |<-------(2) Redirect to Auth---|   (App)       |
      +--------+                               +---------------+
                                                  |   ^
                                                  |   | (3) Authorization Code
                                                  v   |                                   +---------------+
                                          +---------------+                             |               |
                                          |  Auth Server  |                             | Resource      |
                                          | (AS / Issuer) |<----(5) Token Request-------| Server (RS)   |
                                          +---------------+   (Code + Secret)           |               |
                                                  |   |                               +---------------+
                                                  |   | (4) Auth Code + Access Token  ^   |
                                                  |   +--------------------------------+   |
                                                  |   | (6) Validate Token             |   |
                                                  |   +--------------------------------+   |
                                                  |                                       |
                                                  v                                       |
      +--------+       (7) Access Protected Data w/ Token                             |   |
      |        |<----------------------------------------------------------------------+   |
      |  User  |                                                                           |
      +--------+<---------------------------------------------------------------------------+

* [Key]: 
  (1) 사용자 로그인 요청
  (2) Client -> Auth Server로 리다이렉트
  (3) 사용자 로그인 및 권한 승인 -> Auth Code 발급
  (4) Auth Server -> Client로 Auth Code 전달
  (5) Client -> Auth Server (Auth Code 교환 for Access Token)
  (6) Auth Server -> Client (Access Token + Refresh Token + ID Token 발급)
  (7) Client -> Resource Server (Access Token으로 데이터 요청)
```
*   **해설**: 가장 안전한 방식인 **Authorization Code Flow**를 도식화했다. 핵심은 'Authorization Code'를 임시 비밀번호로 사용하여 Access Token을 교환하는 과정이다. 토큰이 브라우저 주소창(URL)에 노출되는 것을 방지하고, Client Secret을 통해 Client 자체의 신원도 함께 검증받는다.

#### 3. 핵심 기술: JWT (JSON Web Token) 구조 및 검증

JWT는 단순히 인코딩된 문자열이 아니라, 수학적 위변조 방지 기능을 탑재한 "자가 증명 가능한 데이터 패킷"이다.

*   **구조**: `xxxxx.yyyyy.zzzzz` (Base64Url 인코딩)
    1.  **Header**: `alg` (알고리즘, 예: HS256, RS256), `typ` (JWT).
    2.  **Payload**: `iss` (발행자), `exp` (만료 시간), `sub` (주체), 사용자 정의 Claim.
    3.  **Signature**: `HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)`

*   **검증 알고리즘 (서버 측 로직)**:
    ```python
    # [Pseudo-code for Signature Verification]
    def verify_jwt(token, secret_key):
        header, payload, received_signature = split_token(token)
        
        # 1. Header and Payload are just Base64 decoded (Reconstruction)
        header_b64 = urlsafe_b64encode(header)
        payload_b64 = urlsafe_b64encode(payload)
        
        # 2. Generate Signature again with Server's Secret
        # (Use Shared Secret for HS256 or Public Key for RS256)
        computed_signature = HMACSHA256(header_b64 + "." + payload_b64, secret_key)
        
        # 3. Compare Constant Time (Prevent Timing Attack)
        if constant_time_compare(computed_signature, received_signature):
            return payload # Token is valid
        else:
            raise SecurityException("Tampered Token")
    ```
    *   **핵심**: 서버는 세션을 저장하지 않는다. 토큰 안에 있는 `exp`(만료 시간)를 확인하고, 서명(Signature)이 맞는지만 확인하면 즉시 신뢰한다.

#### 4. X.509 인증서 체인 (PKI)

X.509는 **CA (Certificate Authority)**에 의해 서명된 데이터 구조다.
*   **필드**: Version, Serial Number, Signature Algorithm, Issuer (CA), Validity (Not Before/After), Subject (Server Name), Subject Public Key Info, Extensions (SAN, CRL Distribution Points).
*   **신뢰 사슬**: Root CA -> Intermediate CA -> Leaf Certificate (Server Cert).

> **📢 섹션 요약 비유**: **OAuth**는 '판타지 앱'이 '구글'에게 "이 사용자 정보 좀 줘"라고 요청하는 일종의 **'사전 동의 시스템'**이고, **JWT**는 **'위조 방지된 여권'**이다. 입국 심사관(서버)은 여권 발급국가의 서명을 확인만 하면 될 뿐, 발급국가에 전화를 걸어 확인할 필요가 없다. **X.509**는 **'공무원의 공인 인증도장'**이다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술 비교 분석표

| 비교 항목 | **Session (Cookie)** | **OAuth 2.0 / Token** | **SAML vs OIDC** |
|:---|:---|:---|:---|
| **저장소 위치** | **Server (Stateful)** | **Client (Stateless)** | Identity Provider (IdP) |
| **확장성** | 낮음 (서버 메모리 의존) | **매우 높음** (수평 확장 용이) | 높음 (중앙 집중식 인증) |
| **보안성** | CSRF 취약, 세션 하이재킹 | Token 탈취 시 위험하지만 유효기간 존재 | XML 기반(SAML) vs JSON/REST(OIDC) |
| **주요 용도** | 전통적인 웹사이트 | API, 모바일, 마이크로서비스 | 기업 SSO (SAML), 모던 웹 (OIDC) |
| **데이터 형식** | N/A | JSON (JWT) | XML (SAML) vs JSON (OIDC) |

*   **의사결정 메트릭**:
    *   **Latency**: JWT 검증은 DB 조회가 없으므로 Session DB 조회보다 **~1-5ms** 빠름.
    *   **Payload Size**: Session ID는 일반적으로 **32B**이나, JWT는 Claim에 따라 **几百 Bytes**~**1KB**로 커질 수 있어 HTTP Header 오버헤드 고려 필요.

#### 2. OIDC (OpenID Connect)와의 융합

**OIDC**는 OAuth 2.0 위에 구축된 **인증(Authentication)** 계층이다.
*   **OAuth**: 접근 허가권(Access Token) 부여 ("리소스 접근 OK")
*   **OIDC**: 신원 확인(ID Token = JWT 형태) 부여 ("당신이 누구지?")
*   **시너지**: 개발자는 하나의 프로토콜(OIDC)로 구글/카카오 로그인(인증)과 구글 캘린더 연동(권한)을 동시에 해결할 수 있다.

#### 3. 보안 위협 및 완화 (Security Considerations)

| 위협 (Threat) | **OAuth/JWT/X.509 대응** |
|:---|:---|
| **Token Hijacking** | **HTTPS (TLS)** 사용 의무화. Short-lived Access Token (짧은 수명) + Refresh Token 사용. |
| **Replay Attack** | JWT에 `jti` (JWT ID)와 `exp` (Expiration) 포함하여 재사용 방지. Nonce 사용. |
| **Man-in-the-Middle (MITM)** | X.509 인증서 기반의 **TLS/SSL 핸드셰이크**로 통구간 암호화 강제. |
| **Code Injection** | Authorization Server는 Client Secret을 검증하여 가짜 앱을 차단. |

> **📢 섹션 요약 비유**: **Session**은 '매번 출입부에 서명하는 방식'이고 **JWT/OAuth**는 '회원증을 목에 걸고 다니는 방식'입니다. 회원증이 너무 크면(Header Overhead) 불편하지만, 출입부를 찾을 필요가 없어서 속도가 매우 빠릅니다. **OIDC**는 회원증에 얼굴 사진(ID)을 추가로 붙여 신분 확인까지 완료한 **'신분증 통합 시스템'**이라고 볼 수 있습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정

**Scenario 1: 마이크로서비스 아키텍처(MSA) 도입**
*   **문제**: 서비스가 50개로 쪼개졌다. 사용자가 서비스 A에서 로그인하면 B~Z에서도 로그인이 유지되어야 한다. 모든 서버가 세션을 공유하는 것은 레거시하다.
*   **판단**: **OAuth 2.0 + JWT** 방식 채택. 사용자는 인증 서버(UAA)만 믿으면 되고, 각 서비스(MS)는 토큰만 검증하면 된