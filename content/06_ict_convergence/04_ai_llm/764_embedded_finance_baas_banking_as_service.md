---
title: "Embedded Finance BaaS Banking as Service"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 764
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BaaS(Banking as a Service)는 은행의 핵심 기능(계좌발급, KYC/AML, 결제, 송금, 대출 실행)을 마이크로서비스형 RESTful API와 SDK로 추상화하여 비금융 플랫폼이 화이트라벨 방식으로 금융 기능을 임베드할 수 있게 하는 클라우드 네이티브 금융 인프라이며, 임베디드 금융(Embedded Finance)은 이를 비금융 UX 흐름(E-commerce, SaaS, ERP, 모빌리티) 내부에 컨텍스트 단위로 내장하여 사용자가 인지하지 못하는 사이렌트 금융(Silent Finance)을 구현하는 패러다임이다.
> 2. **가치**: 전통적으로 신규 핀테크가 은행 라이선스를 취득하는 데 18~36개월, 자본금 100~500억 원이 소요되던 진입장벽을 BaaS API 연동만으로 2~6주 / 1억 원 미만으로 축소하며, 임베디드 결제 전환율(Embedded Payment Conversion)은 일반 결제 대비 20~30% 향상, AOV(Average Order Value)는 15~50% 증가, 고객 이탈률(Churn) 40% 감소 등 정량적 가치를 창출한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 (a) BaaS 단일 벤더 종속(Lock-in) vs 멀티 BaaS 오케스트레이션, (b) 동적 분기 라우팅을 통한 결제 실패율 0.1% 이하 SLA 확보 vs 라우팅 복잡도 및 트랜잭션 멱등성 보장, (c) 호스트-바이-호스트(Hosted) UI vs 드롭-인(SDK) UI vs 헤드리스(API-only) 통합의 UX/컴플라이언스 균형, (d) KYC/AML 컴플라이언스 책임 소재(Regulated vs Unregulated Partner) 및 권리/책임 분리(BaaP: Banking as a Platform) 구조 설계이다.

---

## Ⅰ. 개요 및 필요성

기존 금융 서비스는 **소수의 대형 은행이 폐쇄형 코어뱅킹 시스템(T24, FIS Profile, Flexcube)** 위에서 통장 개설, 자금 이체, 대출 심사, 카드 발급 등 End-to-End 밸류체인을 독점하는 수직 통합(Vertically Integrated) 구조였다. 2015년경 영국의 PSD2(Payment Services Directive 2)와 EU의 Open Banking 표준이 등장하면서 은행이 보유한 결제 계좌 정보(Account Information)와 결제 개시 서비스(PIS: Payment Initiation Service)를 제3자 핀테크(TPP: Third Party Provider)에 강제 개방해야 하는 의무가 발생했고, 이것이 BaaS의 기술적·규제적 촉매제가 되었다.

이후 마이크로서비스 아키텍처(MSA), 컨테이너 오케스트레이션(Kubernetes), 그리고 gRPC/GraphQL 기반 API 게이트웨이(Kong, Apigee, AWS API Gateway)의 성숙으로 은행 코어 시스템을 모놀리식에서 도메인별 API(Account, Payment, Card, Lending, KYC) 단위로 분리(decoupling)하는 **코어-오프-뱅킹(Core-Off-Banking)**, **언번들링(Unbundling)** 트렌드가 가속화되었다. 대표적으로 BBVA가 2017년 API Market을 공개했고, Goldman Sachs가 Marcus 플랫폼을, JPMorgan이 코어 뱅킹을 API 형태로 외부에 판매하는 **Platform Banking** 모델을 본격화했다.

임베디드 금융은 이러한 BaaS 인프라를 **Shopify Balance, Uber Cash, Apple Card, Klarna Pay-in-3, Amazon Pay** 같은 비금융 SaaS/E-commerce/Mobility 플랫폼 내부의 사용자 여정(User Journey)에 직접 삽입하여, "은행은 가게 뒤에 숨어 있고 소비자는 가게만 보는" 구조를 실현한다. 2023년 기준 글로벌 임베디드 금융 시장 규모는 약 $1,000억(약 130조 원)에 달하며, 한국에서는 토스(Toss)의 토스뱅크 연동 페이먼트, 카카오페이의 카카오뱅크 제휴 송금, 네이버파이낸셜의 네이버페이 머니, 쿠팡의 쿠팡페이 등이 임베디드 금융 모델에 해당한다.

```text
+----------------------------------------------------------------------+
|                임베디드 금융(Embedded Finance) 진화 단계              |
+----------------------------------------------------------------------+

  [1단계: 전통 은행]              [2단계: 인터넷뱅킹]
  +--------------+                +--------------+
  |  지점 창구    |   -------►     |  웹/모바일    |
  |  종이 통장    |   인터넷      |  비대면 계좌  |
  |  번호표 대기  |                |  조회/이체    |
  +--------------+                +--------------+
                                            |
                                            |  PSD2 / Open Banking
                                            v
  [3단계: BaaS API]              [4단계: 임베디드 금융]
  +--------------+                +------------------------------+
  | 银行 코어  | ◄-- REST API --► | E-commerce / SaaS / 모빌리티 |
  | +- KYC 엔진 |                | +--------------------------+|
  | +- 결제 레일 |                | | 체크아웃 -> 즉시대출/할부 ||
  | +- 카드 발급 |                | | 차량예약 -> 보험 내장     ||
  | +- 원장(Ledger)|              | | 라이드 -> 즉시 정산      ||
  +--------------+                | +--------------------------+|
        ^                         +------------------------------+
        |  BaaS Provider (Solaris, Unit, Treasury Prime, 도슨) ^
        |                                                       |
        +---------- API 레이어 추상화 --------------------------+

  -------------------------------------------------------------
  소비자(C) 인식: [은행 방문] -> [앱 설치] -> [앱 내 결제] -> [컨텍스트 금융]
  금융 가시성:   ████████   ████        ██             ▌ (거의 보이지 않음)
```

**기존 패러다임 vs 임베디드 금융/BaaS 패러다임 비교**

| 차원 | 기존 (Legacy Banking) | 임베디드 금융 / BaaS |
| :--- | :--- | :--- |
| **진입 장벽** | 은행업 인가, BIS 자기자본 100~1,000억 | API 키 발급, 1~6주 온보딩 |
| **시스템 아키텍처** | 모놀리식 코어뱅킹 (Mainframe) | 클라우드 네이티브 MSA (K8s + gRPC) |
| **사용자 여정** | 은행 앱/지점 -> 금융 행위 | E-commerce/SaaS -> 자연스러운 금융 행위 |
| **데이터 흐름** | 배치(Batch) + SOAP/ISO 8583 | 실시간(Real-time) + REST/GraphQL + Webhook |
| **규제 준수 주체** | 단일 은행 책임 | BaaP(Banking-as-a-Platform) 분산 책임 모델 |
| **수익 모델** | NIM(Net Interest Margin) 의존 | 인터체인(Interchange) + SaaS Fee + API 호출당 과금 |

- **📢 섹션 요약 비유**: 기존 금융이 "은행 창구에만 가야 돈을 넣을 수 있는 우체국"이었다면, 임베디드 금융/BaaS는 "**자동판매기, 카페, 주유기 어디서나 현금을 넣고 잔돈을 받을 수 있는 전자화폐 시대**"와 같다. 은행은 보이지 않는 뒤편의 '**발전소**'가 되고, 소비자는 '**콘센트**'만 인식한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

BaaS/임베디드 금융 시스템은 통상 **5계층 레이어드 아키텍처(Layered Architecture)** 로 구성된다. 각 계층은 명확한 책임 분리(SRP)와 SLA를 가지며, gRPC/GraphQL 게이트웨이를 통해 비동기 이벤트는 Kafka/EventBridge, 동기 트랜잭션은 REST API로 라우팅된다.

```text
+-------------------------------------------------------------------------+
|                BaaS / 임베디드 금융 5계층 아키텍처                        |
+-------------------------------------------------------------------------+

  +------------------------------------------------------------------+
  |  Layer 5: 임베디드 채널 (Embedded Channels)                      |
  |  --------------------------------------------------------------  |
  |  [E-commerce]   [SaaS ERP]    [모빌리티 앱]   [IoT/커넥티드카]   |
  |  Shopify        Toast POS     Uber/Lyft       Tesla/Toyota       |
  |  WooCommerce    Salesforce    TADA/Bolt       Tesla Insurance    |
  |  Amazon         ServiceNow    Hyundai Link    원격 계좌개설(KYC) |
  +--------------+---------------------------------------------------+
                 | SDK (iOS/Android/Web/Server)  | iframe Drop-in
                 v                              v
  +------------------------------------------------------------------+
  |  Layer 4: 오케스트레이션 / 통합 (Orchestration)                  |
  |  --------------------------------------------------------------  |
  |  +-----------------+  +-----------------+  +----------------+  |
  |  | Payment Orchestr|  | Identity/KYC    |  | Risk & Fraud   |  |
  |  | (Smart Routing) |  | Orchestrator    |  | Engine         |  |
  |  | - 멀티 PSP 라우팅|  | - ID/Passport   |  | - ML Scor.     |  |
  |  | - 자동 재시도    |  | - KYB(사업자)   |  | - Device fp    |  |
  |  | - 멱등성 토큰   |  | - PEP/Sanction  |  | - 3DS2 인증   |  |
  |  +-----------------+  +-----------------+  +----------------+  |
  +--------------+---------------------------------------------------+
                 |  API Gateway (Kong / Apigee / AWS API GW)
                 v
  +------------------------------------------------------------------+
  |  Layer 3: BaaS 코어 API (Banking-as-a-Service Core)              |
  |  --------------------------------------------------------------  |
  |  /accounts      /cards          /payments      /lending          |
  |  /kyc           /transfers      /webhooks      /treasury         |
  |  /wallets       /fx             /statements    /beneficiaries    |
  |  --------------------------------------------------------------  |
  |  ⮕ 실제 은행/송금 라인 보유 (Bank, e-money, MSB 라이선스)        |
  +--------------+---------------------------------------------------+
                 |  내부 코어뱅킹 API (T24 / Mambu / Thought Machine)
                 v
  +------------------------------------------------------------------+
  |  Layer 2: 코어뱅킹 엔진 (Core Banking)                           |
  |  --------------------------------------------------------------  |
  |  +----------+ +----------+ +----------+ +------------------+  |
  |  | 원장     | | 결제     | | 카드     | | 대출/신용       |  |
  |  |(Ledger) | | 엔진    | | 발급기  | | 엔진            |  |
  |  | Double- | | ACH,   | | BIN/SPONSOR| | Origination    |  |
  |  | Entry   | | SEPA   | | Issuer/  | | Underwriting   |  |
  |  |         | | WIRE   | | Processor| | Servicing      |  |
  |  +----------+ +----------+ +----------+ +------------------+  |
  +--------------+---------------------------------------------------+
                 |  Fed/ACH/SWIFT/Card Network Rail
                 v
  +------------------------------------------------------------------+
  |  Layer 1: 금융 인프라 레일 (Financial Rails)                      |
  |  --------------------------------------------------------------  |
  |  [FedNow]  [ACH]   [SEPA Inst]  [SWIFT]   [Visa Direct]        |
  |  [MasterSend]  [CIPS]  [KRW EFT]  [은행공동망]                |
  +------------------------------------------------------------------+
```

### 📋 구성 요소별 상세 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **BaaS Provider (Bank/Tenancy)** | 규제 라이선스(Banking, EMI, MSB) 보유, 예금 보호(FDIC/DGS), 코어뱅킹 호스팅 | Solaris SE(독일), Treezor(프랑스), Unit(US), Treasury Prime(US), Synctera(US), ClearBank(UK), Starling Bank(UK), 한국: 도슨, 핀다, 토스뱅크 제휴형 |
| **KYC/AML Engine** | 고객 신원 확인(신분증 OCR + 생체인증 + Liveness), 사업자 실소유UBO 확인, AML 리스트 스크리닝(OFAC, UN, EU) | Onfido, Jumio, Veriff, Persona, Sumsub, Trulioo, Smile ID. KYC 절차: ID 검증 -> 주소증명 -> 생체인증 -> 리스크 스코어링 -> PEP/Sanction 매칭 -> Enhanced Due Diligence(EDD) 분기 |
| **결제 오케스트레이터 (Payment Orchestrator)** | 멀티 PSP(Payment Service Provider) 간 라우팅, 자동 폴백(Fallback), 멱등성(Idempotency) 관리, 정합성 검증(Reconciliation) | Primer.io, Spreedly, Adyen(자체), Cellpoint Digital, Gr4vy, ROOX. 라우팅 로직: BIN 기반, 거래금액 기반, 국가별 코스트 최적화, 가용성 기반 Health-check 라우팅 |
| **원장 시스템 (Ledger DB)** | Double-Entry 복식부기, 실시간 잔액 계산, ISO 20022 메시지, 이벤트 소싱(Event Sourcing) + CQRS | PostgreSQL(파티셔닝 + Citus), Apache Iceberg 데이터레이크, AWS QLDB(불변 원장), TigerBeetle(고성능 금융 원장 DB), 전용 솔루션: Mambu, 10x Banking, Thought Machine Vault |
| **카드 발급기 (Card Issuer)** | BIN/Sponsorship, 카드 가상화(Tokenization), 3D Secure(3DS2), MDES/VTS 토큰화 | Marqeta, Lithic, Galileo(SoFi), Stripe Issuing, Greenlight. 카드생애주기: 발급 -> 활성 -> 토큰요청(VTS/MDES) -> 인증 -> 거래 -> 정지/재발급 |
| **임베디드 SDK / Drop-in UI** | 비금융 앱 내 금융 UX 삽입(원클릭 결제, 즉시 계좌개설, 원터치 송금) | Web/Mobile SDK(Plaid Link, Stripe Elements, Toss SDK), iframe Drop-in, Headless(API-only), Webhook(상태 비동기 통지) |
| **리스크 & 사기 탐지 (FRAML)** | 거래 모니터링(Transaction Monitoring), 사기 패턴 탐지, 디바이스 핑거프린팅, 행동 분석 | Feedzai, FICO Falcon, Featurespace, Sardine, Sift. Rule-based + ML Hybrid, 3-Layer Defense(Entry -> Transaction -> Post-trade) |
| **규제 보고 & 컴플라이언스 자동화** | CTR(현금거래보고), SAR(의심거래보고), PSD2 SCA, 한국 전자금융감독규정, 마이데이터 | NICE Actimize, Oracle FCC, 전자금융거래법 §17(본인확인), 신용정보법 §32(마이데이터 API) |

### 🔍 핵심 동작 메커니즘 (Deep Dive)

**1. 임베디드 결제 라우팅 및 멱등성 알고리즘**
- **Smart Routing**: 단일 트랜잭션 발생 시, Payment Orchestrator는 사전 정의된 라우팅 룰셋(예: `amount < $50 AND country=US -> Stripe; else -> Adyen`)을 평가하여 PSP를 선정. Health-check 엔드포인트(`/health`)를 5초 주기로 Ping하여 장애 시 자동 Failover.
- **멱등성 키(Idempotency Key)**: 클라이언트가 `Idempotency-Key: <UUID v4>` 헤더를 동봉하면, 오케스트레이터는 24시간 캐시(KV Store: Redis)에 `(key, response_hash)`를 저장. 네트워크 재시도 시 동일 응답을 반환하여 중복 결제 방지.
- **분산 트랜