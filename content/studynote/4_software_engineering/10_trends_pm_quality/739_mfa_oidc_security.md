+++
title = "739. MFA 인증 OIDC 인가 보안 구조"
date = "2026-03-15"
weight = 739
[extra]
categories = ["Software Engineering"]
tags = ["Security", "Authentication", "Authorization", "MFA", "OIDC", "OAuth2", "Identity"]
+++

# 739. MFA 인증 OIDC 인가 보안 구조

## 핵심 인사이트 (3줄 요약)
> 1. **본질 (Identity Assurance)**: 단일 탈취 지점(Password)을 제거하기 위해 지식/소유/존재 요소를 결합한 **MFA (Multi-Factor Authentication)**와, 중앙 집중식 신원 검증 및 권한 위임을 표준화한 **OIDC (OpenID Connect)** 및 **OAuth 2.0** 프레임워크의 융합 아키텍처.
> 2. **가치 (Security & UX)**: NIST SP 800-63B 기준의 디지털 신원 보증 수준(AAL)을 향상시켜 99.9% 이상의 자격증명 탈취 공격을 차단함과 동시에, 표준 프로토콜을 통해 **SSO (Single Sign-On)** 및 타 서비스 연동(연합 인증) 시의 개발 복잡도를 획기적으로 낮춤.
> 3. **융합 (Standard & Future)**: 레거시 SAML (Security Assertion Markup Language)의 XML 기반 무거움을 JWT (JSON Web Token) 기반의 경량 RESTful API로 대체하여 모바일/마이크로서비스 환경에 최적화된 보안 계층을 형성하며, 향후 FIDO2 및 **DID (Decentralized Identifier)**와 연계될 기반 기술임.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
전통적인 보안의 핵심은 "무엇을 아느냐(Knowledge)"였으나, 사회공학적 해킹(Social Engineering) 및 무차별 대입 공격(Brute Force)의 고도화로 인해 이만으로는 부족하게 되었습니다. **MFA (Multi-Factor Authentication)**는 사용자의 신원을 검증할 때 '지식(Knowledge)', '소유(Possession)', '존재(Inherence)' 중 최소 두 가지 요소를 요구하여 보안 강도를 기하급수적으로 높이는 철학입니다. 여기에 더해 현대의 복잡한 분산 시스템 환경에서는 사용자가 매번 각 서비스에 인증 정보를 노출하지 않도록, **OAuth 2.0 (Authorization Framework)**을 기반으로 한 **OIDC (OpenID Connect)**라는 표준화된 신원 위임 계층을 사용합니다. 이는 "인증(Authentication, 누구인가)"과 "인가(Authorization, 무엇을 할 수 있는가)"를 철저히 분리하여 시스템의 취약점을 최소화하는 설계 패러다임입니다.

**2. 등장 배경: 보안의 패러다임 시프트**
① **기존 한계**: 단일 패스워드에 의존하는 구조는 DB 해킹 시 대규모 정보 유출로 이어지며, 관리자가 평문(Pain text) 혹은 취약한 해시 알고리즘으로 저장할 경우 필연적으로 취약점을 가짐.
② **혁신적 패러다임**: 중앙 인증 서버(IdP)가 인증을 전담하고, 서비스 제공자(RP/Client)는 토큰(Token)만으로 세션을 관리하는 '신뢰의 위임' 모델 등장. HTTPS를 통한 암호화와 JWT 서명 검증을 통해 무결성을 보장.
③ **비즈니스 요구**: 사용자는 편리함(한 번의 로그인), 기업은 강력한 보안과 감사 추적성(Compliance)을 동시에 요구함에 따라 MFA + SSO 구조가 필수 인프라가 됨.

**💡 비유: 고속도로 요금소와 하이패스 시스템**
보안 구조는 마치 고속도로 톨게이트를 통과하는 과정과 같습니다. 구식 방식은 매次 정차하여 요금을 내고 영수증(인증 정보)을 확인받는 것(각 사이트의 로그인)과 같아 혼잡(보안 리스크)이 가중됩니다. 반면, MFA가 적용된 OIDC 시스템은 사전에 등록된 하이패스 단말기(신원 확인)를 이용해 진입 전에 미리 신원을 검증하고, 게이트에서는 단순히 센서만 인식(토큰 확인)하여 통과시키는 방식입니다. 여기서 MFA는 하이패스 단말기를 발급받을 때 신분증과 차량 번호를 이중으로 확인하는 절차에 해당합니다.

```text
   [ Legacy ]           [ Modern MFA + OIDC ]
   ID/PW ──▶ Site       ID/PW + Bio ──▶ IdP (Issue Token)
      ▲                            │
      │                            ▼
   Direct Login              Token ──▶ Site (Access)
```

**📢 섹션 요약 비유**: 마치 보안금고가 열쇠(지식)뿐만 아니라 지문(존재)이 맞아야만 열리는 이중 잠금 장치를 기본으로 제공하되, 이 금고의 열쇠 관리를 중앙 보안 센터(IdP)가 전담하여 각 부서(애플리케이션)가 열쇠를 직접 만들지 않도록 하는 체계와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 및 상호작용 표**
OIDC 및 MFA 구조는 다음의 주요 엔티티들 간의 상호작용으로 정의됩니다. 각 구성 요소는 RFC 6749(OAuth 2.0) 및 RFC 8414(Authorization Server Metadata) 표준을 준수합니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 | 주요 프로토콜/포맷 | 비유 |
|:---|:---|:---|:---|:---|
| **Resource Owner (User)** | 자원 소유자 | 브라우저 또는 앱을 통해 인증을 시도하며, 등록된 2차 인증(OTP/Bio)을 수행. | HTTPs, Auth Code | VIP 고객 |
| **User-Agent** | 사용자 에이전트 | 리다이렉션(Redirection)을 처리하여 클라이언트와 IdP 간의 요청을 중계. | 302 Redirect, Cookie | 택배 배송원 |
| **Client (RP)** | 의존 party | 애플리케이션으로, 사용자의 자원에 접근하기 전 Access Token 및 ID Token을 검증. | OIDC RP-Initiated Logout | 체크포인트 |
| **Authorization Server (IdP)** | 인증 서버 | MFA 검증 수행, Access/ID Token 발급, 토큰 서명(JWS) 및 암호화(JWE). | JWT, Discovery | 발권소 |
| **Authenticator** | 인증자 | TOTP(Time-based OTP) 생성, 생체 인증(Push/Bio) 수행. | FIDO2, OATH TOTP | 신분증 |

**2. 인증 및 인가 플로우 상세 (ASCII)**

```text
[ 1. Authorization Request ]       [ 2. AuthN & MFA Challenge ]
+------------------+              +------------------+
|   Client (RP)    |              |   IdP (AuthZ Srv)|
|                  |--------------|                  |
| - redirect_uri   |              | - Verify User/PW |
| - response_type  |              | - Trigger MFA    |      +----------+
| - scope=openid   |              | - 2FA Check      |<-----|  User    |
+------------------+              +------------------+      +----------+
      |                                   ^
      |                                   | (3. Code)
      v                                   |
+------------------+              +------------------+
|   User-Agent     |              |   Client (RP)    |
| (Browser Redirect)|<-------------|                  |
+------------------+  (4. Code)   +------------------+
      |                                   |
      |                                   | (5. Token Exchange
      |                                   |  + client_secret)
      v                                   v
+------------------+              +------------------+
|   Client (RP)    |--------------|   IdP (AuthZ Srv)|
|                  | (6. Tokens)  |                  |
+------------------+  JWT Set     +------------------+
      |                                   ^
      |                                   | (7. Validate Signature
      |                                   |  + Claims)
      v                                   |
+------------------+              +------------------+
|   Resource       |<-------------|   Client (RP)    |
|   Server (API)   | (8. API Call |                  |
+------------------+  w/ Bearer)  +------------------+
```

**3. 심층 동작 원리 및 핵심 알고리즘**

**[단계별 상세 분석]**
1.  **인증 요청 (Request)**: 클라이언트는 `response_type=code` 및 `scope=openid profile email` 등을 포함하여 IdP로 리다이렉트. 이때 `state` 매개변수를 통해 CSRF (Cross-Site Request Forgery) 공격을 방지.
2.  **MFA 검증 (Authentication)**: IdP는 1차 인증(ID/PW) 성공 후, 등록된 MFA 요소(TOTP, SMS, FIDO)에 대한 챌린지를 발행. 사용자가 이를 해결해야만 `authorization_code` 발급.
3.  **토큰 발급 (Token Issuance)**: 클라이언트는 `code`와 `client_secret`을 사용하여 IdP의 토큰 엔드포인트에 POST 요청. IdP는 이를 검증하고 **Access Token** (권한)과 **ID Token** (신원)을 발급.
    *   **ID Token 구조 (JWT)**: `Header` (alg/typ), `Payload` (iss, sub, aud, exp, iat, nonce), `Signature`로 구성. `sub` (Subject)는 사용자의 고유 식별자.
4.  **토큰 검증 (Validation)**: 클라이언트는 ID Token의 서명을 IdP의 공개키(JWKS)로 검증하고, `aud` (Audience) 클레임이 자신의 Client ID와 일치하는지 확인하여 **Replay Attack**을 방지.

**[핵심 코드: JWT 토큰 구조 예시]**
```json
// Header
{
  "alg": "RS256",       // Asymmetric Algorithm (SHA-256 with RSA)
  "typ": "JWT",
  "kid": "key_id_1"     // Key Identifier for JWKS rotation
}
// Payload
{
  "iss": "https://idp.example.com",  // Issuer
  "sub": "user_123456",               // Subject (Unique ID)
  "aud": "client_app_id",             // Audience
  "exp": 1710451200,                  // Expiration (Unix Timestamp)
  "iat": 1710451140,                  // Issued At
  "auth_time": 1710451000,            // Time of Authentication
  "amr": ["pwd", "mfa"]               // Authentication Methods References
}
```

**📢 섹션 요약 비유**: 마치 입장권(Tokens)을 발급받는 놀이공원 시스템과 같습니다. 티켓 부스(IdP)에서 신원 확인(MFA)을 마쳐야만 손목 밴드(Access Token)와 이용자 명찰(ID Token)을 받을 수 있으며, 이때 발급된 밴드는 위변조 방지를 위해 특수 잉크(Signature)로 인쇄되어 각 기구(Resource Server) 입구의 스캐너가 진위 여부를 즉시 확인하는 구조입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: SAML vs OIDC**

| 비교 항목 | SAML (Security Assertion Markup Language) | OIDC (OpenID Connect) |
|:---|:---|:---|
| **데이터 포맷** | XML (Extensible Markup Language) 기반 | **JSON (JavaScript Object Notation)** 기반 |
| **전송 프로토콜** | SOAP, HTTP POST / Redirect | **RESTful API** (JSON over HTTP) |
| **보안 서명** | XML Signature (XMLSec) | **JWS (JSON Web Signature)** |
| **주요 사용처** | 기업 내 웹 애플리케이션(SaaS), ERP 연동 | **모바일 앱, SPA(Single Page App), 마이크로서비스** |
| **파서 오버헤드** | XML 파싱으로 인한 상대적으로 높은 리소스 소모 | 경량 JSON 파싱으로 낮은 오버헤드 |
| **브라우저 지원** | 레거시 플러그인 종속성이 있었으나 개선됨 | 모던 브라우저 네이티브 지원 |

**2. 타 과목 융합 및 시너지 분석**

*   **[네트워크] - TLS/SSL (Transport Layer Security)**:
    *   **연관성**: OIDC 프로토콜 자체는 전송 계층의 보안을 보장하지 않으므로, 모든 통신(HTTP)은 반드시 HTTPS 위에서 이루어져야 합니다.
    *   **시너지**: **TLS 핸드셰이크(Handshake)**가 계층 간의 통신 채널을 암호화하고, OIDC가 애플리케이션 계층의 사용자 신원을 검증하여 **Defense-in-Depth(심층 방어)** 전략을 완성합니다.
*   **[데이터베이스] - 토큰 저장 전략 (Stateful vs Stateless)**:
    *   **연관성**: Access Token은 클라이언트가 보관(Header 포함)하지만, **Refresh Token**의 경우 DB에 저장해야 할 필요가 있습니다.
    *   **시너지**: Refresh Token을 RDBMS에 저장할 경우 Revocation(폐기) 관리가 용이하지만, 분산 환경에서는 성능 저하가 발생할 수 있어 **Redis**와 같은 인메모리 DB(Key-Value Store)를 활용하여 TTL(Time-To-Live) 기반의 빠른 세션 회수가 가능하도록 설계해야 합니다.
*   **[AI/보안] - 지속적 인증 (Continuous Authentication)**:
    *   **연관성**: 정적인 MFA(Time-based)로는 세션 하이재킹(Session Hijacking)을 막기 어렵습니다.
    *   **시너지**: 사용자의 행동 패턴(입력 속도, 마우스 움직임, 위치)을 AI 모델에 학습시켜, 로그인 이후에도 지속적으로 신뢰 점수를 계산하고 점수가 낮아지면 재인증(Step-up Authentication)을 유도하는 융합 보안 모델이 진화하고 있습니다.

**📢 섹션 요약 비유**: SAML은 무겁고 정석적인 우편물(XML) 배달 시스템이라면, OIDC는 가볍고 빠른 메신저(JSON) 기반의 즉시 전달 시스템입니다. 메신저가 더 효율적이지만, 내용이 도청당하지 않도록 봉투(TLS)로 감싸는 보안 관행과, 배달 속도를 위해 데이터를 임시 보관함(Redis)에 두는 운영 노하우가 결합되어야 최적의 성능을 냅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 매트릭스**

*   **시나리오 A: 대규모 퍼블릭 클라우드 전환 (Legacy On-premise → Cloud)**
    *   **상황**: 기존 AD(Active Directory) 기반의 SAML 인증을