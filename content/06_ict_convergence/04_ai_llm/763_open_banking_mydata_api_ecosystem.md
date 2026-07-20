---
title: "Open Banking MyData API Ecosystem"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 763
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오픈 뱅킹 마이데이터 API 생태계는 **PSD2·UK CMA·FAPI 1.0/2.0·OAuth 2.0 Authorization Code + PKCE + mTLS(또는 DPoP)** 기반의 표준화된 REST/OpenAPI 3.x 인터페이스로, 정보제공자(IP)·마이데이터사업자(MSP)·정보이용자(IU)·본인확인기관(CA) 간 **사용자 중심 데이터 이동권(Portability)**을 실현하는 금융 API 거버넌스 체계다.
> 2. **가치**: 한국 마이데이터는 2022년 1월 본격 시행 이후 누적 동의 건수 약 **9억 건**(2024년 말 기준)을 돌파하며, **신용정보집중기관의 조회 API 비용 ~70% 절감**, 핀테크 신규서비스 출시 기간 **6~12개월 -> 2~4개월 단축**, 데이터 기반 **가명결합·맞춤형 대출 금리 스프레드 50~150bp 개선** 효과를 창출하고 있다.
> 3. **판단 포인트**: **보안 모델 선택(OAuth 2.0 + FAPI-RW + mTLS vs DPoP)**, **본인의사확인 요건(이용자확인 1건 vs 매 전송 2채널 인증)**, **가명정보 결합·가명처리 정책(SAFE 17항목)**, **API 게이트웨이 용량(OpenAPI Throttling·Circuit Breaker)**, 그리고 **자본시장·핀테크 확장을 위한 ISO 20022·CBDC·DEPA interoperability**가 핵심 아키텍처 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

오픈 뱅킹(Open Banking)은 **EU PSD2(2018)**, **영국 CMA의 Open Banking Implementation Entity(OBIE, 2016)**, **호주의 CDR(Consumer Data Right, 2020~)** 등 각국 규제当局가 은행의 **고객 거래정보(TXS, Transactions) 및 식별정보(PI, Personal Information)** 를 강제 개방토록 한 정책 프레임워크다. 한국은 이를 **2020년 3월 개정된 「신용정보법」** 에서 **‘본인신용정보관리업(마이데이터)’** 으로 법제화하고, **2022년 1월 17일** 부로 1차 시행(신용정보집중기관 5사, 카드 6사 등), **2023년 8월** 부로 2차 시행(전 금융회사)을 거쳐 **3차 시행(2025년 보험사·할부사 추가)** 까지 단계적으로 확대해 왔다.

기존의 **스크래핑 기반 핀테크 어그리게이터(토스·뱅크샐러드·핀다 초기 버전)** 는 다음과 같은 **4대 기술·법률·운영 이슈** 를 야기했다.

| # | 기존 방식의 한계 | 마이데이터 API로 인한 해결 |
| :--- | :--- | :--- |
| ① | **크롤링 대상 사이트 변경 -> 파서 매일 깨짐** (HTML 셀렉터 의존) | OpenAPI 3.0+ 정적 스키마 + Semantic Versioning으로 계약 기반 통합 |
| ② | **이용자 아이디·비밀번호를 핀테크사가 직접 보관** (Password Anti-Pattern) | OAuth 2.0 토큰 기반 **위임 접근(Delegated Authorization)**, 비밀번호 비저장 |
| ③ | **2-Way TLS·상호운용성 부재** (사 별 상이한 데이터 모델) | 금융결제원 **표준 API 규격 v3.x**(2024.06), ISO 20022 매핑 |
| ④ | **본인확인·동의서 위·변조 시 입증 곤란** | **본인의사확인(전자서명법)** + **Consent Receipt(ISO 27560)** + **전송요구 이력 블록체인 보존** |

```text
[기존 스크래핑 핀테크]              [오픈 뱅킹 · 마이데이터 API 생태계]

  사용자 --ID/PW 직접 입력---> 핀테크 --HTML 스크래핑---> 은행
   |                            |                         |
   |  <---계좌 잔액·거래내역------+                         |
   |  (평문 보관, 파서 깨짐)                                |

                                   사용자 --동의·본인확인---> 핀테크(MSP)
                                                              | OAuth 2.0
                                                              v
                                                정보제공자(IP) --표준 API---> MSP
                                                              |  (PSD2/FAPI)
                                                              v
                                                마이데이터 허브/통합조회
```

오픈 뱅킹은 단순한 “데이터 개방”이 아니라 **“데이터 이동권(Portability)·동의 기반 자기통제(Self-sovereign Identity)·금융 포용(Financial Inclusion)”** 이라는 3대 정책 의제를 코드와 계약(OpenAPI 명세)으로 실현하는 **금융 API 경제(API Economy)** 의 인프라다.

- **📢 섹션 요약 비유**: 기존 스크래핑은 **“남의 집 창문을 들여다보기(매번 창문 위치가 바뀌고, 열쇠도 빌려야 함)”** 라면, 마이데이터 API는 **“공인된 우편함(Consent Vault)에 본인 열쇠(OAuth Token)를 넣어두고, 택배 기사(FAPI)가 신분증(mTLS Client Cert) 확인 후 배달해주는 시스템”** 이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

마이데이터 API 생태계의 기술 아키텍처는 **OAuth 2.0 / FAPI 1.0 Advanced(또는 FAPI 2.0 Security Profile)** 의 4-Layer Trust Stack 위에 구성된다.

```text
                        +-------------------------------------------+
                        |  Layer 4.  Governance · Data Schema        |
                        |   - 금융결제원 「표준 API 규격 v3.x」          |
                        |   - 한국형 OpenAPI 3.0 + JSON Schema Draft7  |
                        |   - ISO 20022 pacs/camt/cain/catm 매핑      |
                        |   - 가명정보 처리 SAFE 17항목 (PIPC 가이드)   |
                        +-------------------------------------------+
                                       ^
                        +-------------------------------------------+
                        |  Layer 3.  Consent · Identity               |
                        |   - 본인의사확인 (전자서명법, 2채널·생체)     |
                        |   - Consent Receipt (ISO 27560, KR)        |
                        |   - 전송요구 이력(블록체인 Anchoring)        |
                        |   - 마이데이터 사업자 등록/허가 (금위원)      |
                        +-------------------------------------------+
                                       ^
                        +-------------------------------------------+
                        |  Layer 2.  Authorization (FAPI Profile)    |
                        |   - OAuth 2.0 Authorization Code Grant     |
                        |   - PKCE (RFC 7636)                        |
                        |   - PAR (RFC 9126, Pushed Auth Request)    |
                        |   - JARM (RFC 9201, JWT-secured Auth Resp) |
                        |   - Client Authentication:                |
                        |       · mTLS (RFC 8705)                    |
                        |       · 또는 private_key_jwt (RFC 7521)    |
                        |   - DPoP (RFC 9449, 점진적 도입)           |
                        +-------------------------------------------+
                                       ^
                        +-------------------------------------------+
                        |  Layer 1.  Transport · Channel Security     |
                        |   - TLS 1.3 (RFC 8446) Mandatory          |
                        |   - HPKP / HSTS / OCSP Stapling           |
                        |   - Rate Limiting (Token Bucket, 1000 RPS) |
                        |   - WAF · Bot Defense · DAST/SAST         |
                        +-------------------------------------------+

   +---------------------------- 5-주체(5-Party) Flow ----------------------+
   |                                                                        |
   |  정보주체(User) --동의---> 정보이용자(IU) --PAR---> 정보제공자(IP)         |
   |      |                       |                      |                 |
   |      |  본인확인(CA)         |  OAuth Code          |  표준 API호출    |
   |      v                       v                      v                 |
   |  CA(나이스·SCI)          MSP 허브(통합조회)       표준API/REST         |
   |      |                       |                      |                 |
   |      +-----본인의사확인 전자서명(본인+CA)----------+                 |
   |                                                                        |
   +----------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **정보주체(Data Subject)** | 본인 신용정보의 권리자 | 「신용정보법」 제35조의2에 따라 **열람·정정·삭제·처리정지·이동권** 행사, 마이데이터 앱(MyData App)을 통해 **동의 UI·동의 철회·전송요구 이력** 열람 |
| **정보제공자(IP, Information Provider)** | 금융회사(은행·카드·보험·할부·저축은행·캐피탈·핀테크·BNPL 등) | **OAuth 2.0 Authorization Server + 표준 Resource Server** 역할. `/oauth2/authorize`, `/oauth2/token`, `/accounts`, `/transactions`, `/cards`, `/loans` 등의 REST API 제공. **표준 API 규격 v3.x** (금융결제원) 준수, **TPS 보장** (IP별 평균 300~1,000 RPS, Peak 5,000 RPS), **24×7 SLA 99.9%** 필수 |
| **마이데이터 사업자(MSP, MyData Service Provider)** | 본인의사확인·동의수집·전송요구 중계, 데이터 가공·분석 | **클라이언트(Confidential Client) + Resource Server** 역할. **금융위원회 허가제** (신용정보법 §36조의2). 1차 47개사, 2·3차 확대 후 약 200여개사 진입. **가명결합·가명정보 처리·통계모델** 기반 개인화 서비스 제공 |
| **본인확인기관(CA, Certificate Authority)** | 정보주체 본인확인·전자서명 | **공동인증서(구 공인인증서)**, **간편인증(PASS·카카오페이·NAVER·토스·페이코·뱅크페이)**, **생체인증(FIDO2/WebAuthn)**, **본인명의 모바일 신분증(MDID)**. **2채널 인증 + 추가 인증수단** 으로 **본인의사확인 적정성 평가**(연 1회, 한국인터넷진흥원) 통과 필수 |
| **통합조회 허브(Hub, 금융결제원)** | IP의 표준 API 라우팅, 트래픽 제어, 인증서/PKI 배포 | 금융결제원 **KOSCOM Open API Gateway** (Apache APISIX/Kong 기반), **OAuth 2.0 Client Registry**, **JWT/JWS 서명 검증·발급**, **멀티 IP 폴링(Polling) Fallback** (특정 IP 장애 시 타 IP 우선 호출) |
| **전송요구·동의 관리 시스템** | 사용자 동의 영속 저장, 감사 추적, 가명정보 결합 통제 | **Consent Receipt (ISO 27560)** JSON/XML 포맷, **블록체인 앵커링(Klaytn·Hyperledger Besu·LGCNS 체인)** 으로 위·변조 방지, **데이터 항목별 옵트인/옵트아웃 Granularity** (e.g. "계좌 잔액만 허용, 거래내역은 미허용") |
| **가명처리·가명결합 엔진** | 통계·AI 모델링용 가명정보 생성·결합 | **PIPC 가이드라인의 7단계 가명처리 절차**(식별자 제거·범주화·암호화·마스킹·교환·해시·검증) + **결합키(Linkage Key) -> HMAC-SHA256(Salt)**, **k-익명성(k≥5)**, **ℓ-다양성(ℓ≥3)**, **t-근접성** 등 프라이버시 모델 적용 |
| **API Gateway · 보안 계층** | 트래픽 관리·인증·인가·로깅 | **OAuth 2.0 + FAPI Profile Validator**(e.g. PingFederate, Authlete, Gluu), **mTLS Client Cert** (한국정보인증·글로벌사인), **OWASP API Security Top 10**(BOLA, BFLA, SSRF 대응), **WAF·Rate Limit·Circuit Breaker** |

### 핵심 프로토콜 동작 — Step-by-Step

1. **Step 1 (동의 수집)**: IU(예: 토스)가 사용자에게 “OO은행 적금·계좌 정보를 토스 마이데이터에서 조회하겠습니까?” UI 제시 -> **본인의사확인** (간편인증 1채널 + 생체 1채널, 또는 공동인증서 1채널 + ARS 등 추가수단).
2. **Step 2 (전송요구·PAR)**: IU가 **Pushed Authorization Request(RFC 9126)** 로 `/as/par` 엔드포인트에 `client_id`, `scope=accounts transactions cards`, `claims` JSON, `code_challenge=S256`, `request_uri` 를 전송 -> IP의 AS가 `request_uri` 응답.
3. **Step 3 (사용자 인증·인가)**: 사용자는 IP의 `/oauth2/authorize` 로 리다이렉트, **공인인증·간편인증·생체** 로 로그인 후 동의 항목 체크.
4. **Step 4 (Code 발급)**: IP AS가 `redirect_uri` 로 `code` (10분 TTL, 1회용) + **JARM-signed JWT Response**(선택) 반환.
5. **Step 5 (Token 교환)**: IU가 `code` + `code_verifier` + **mTLS Client Cert** 또는 `client_assertion`(private_key_jwt) 로 `/oauth2/token` 호출 -> `access_token`(RFC 9068, JWT Bearer, TTL 1~24h), `refresh_token`(TTL 90일), `id_token`(OIDC) 수신.
6. **Step 6 (Resource 호출)**: IU가 `Authorization: DPoP <proof_jwt>` (또는 Bearer+JWT) 로 `/accounts`, `/accounts/{id}/transactions?from=20240101&to=20241231` 호출 -> IP Resource Server가 JWKS로 서명 검증·scope 검증 후 **표준 API v3.x** 응답.
7. **Step 7 (데이터 활용·저장)**: MSP가 가공·저장 (가명처리 후 DB 암호화 저장) -> IU 서비스로 시각화·추천·신용평가 모델 학습에 활용.
8. **Step 8 (동의 철회·만료)**: 사용자 철회 시 **Consent Revoke API** 호출, MSP는 30일 내 파기, **전송요구 이력**