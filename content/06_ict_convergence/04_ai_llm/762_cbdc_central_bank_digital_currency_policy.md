---
title: "CBDC Central Bank Digital Currency Policy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 762
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CBDC(중앙은행 디지털 화폐)는 중앙은행이 발행하는 **중앙은행 채무(central bank liability)**로서의 디지털 토큰으로, **직접 발행 모델(Direct)·간접 발행 모델(Indirect)·하이브리드 모델** 중 발행 구조와 **계좌 기반(Account-Based) vs 토큰 기반(Token-Based, UTXO)**, **집중형 원장 vs DLT**의 2×2 설계 매트릭스에서 정책 목표·금융안정·프라이버시 간의 트레이드오프를 결정하는 정책·기술 융합 시스템이다.
> 2. **가치**: 화폐의 **단일성(singularity)·통일성·통화정책 전달 효율**을 디지털 환경에서 회복하여, 현금 사용 감소 추세(한국 결제 비중 현금 27.7%->14.5%, 2020->2023) 대응, **스테이블코인·프라이빗 발행 CBDC·암호자산**에 대한 화패 주권(monetary sovereignty) 확보, 결제 시스템 **단일 장애점(SPOF) 제거**, 국경 간 결제 비용 15~30% 절감, 그리고 **프로그래머블 머니(programmable money)**를 통한 자동화된 정책 전달(예: 조건부 소비쿠폰, 자동 세수환급) 기반을 제공한다.
> 3. **판단 포인트**: 실무적 핵심은 ① 발행·유통·결제·환매의 4계층 책임 분리, ② **오프라인 결제(Offline Payment)**·이중사용 방지(Double-Spend)·**한도·이율(remuneration) 정책**을 통한 은행 예금 이탈(digital bank run) 억제, ③ **ZK-SNARK/zk-Rollup 등 영지식 증명**과 **선별적 감사(Selective Disclosure)**로 AML/CFT와 프라이버시를 양립, ④ **mCBDC(FX MVP, Project Agorá, mBridge)**를 통한 ISO 20022·단일 통화 차익거래 방지(UNIQUE) 통합, ⑤ **양자내성암호(PQC, CRYSTALS-Dilithium, Kyber)** 도입 시점 결정이다.

---

## Ⅰ. 개요 및 필요성

현금(Cash)은 디지털 경제에서 매년 사용 비중이 감소하고 있으며, 2024년 기준 전 세계 CBDC 파일럿은 **134개국(G20 멤버 94%)**에서 진행 중이다(Atlantic Council CBDC Tracker, 2024.12). 한국은행은 2021년 1단계(기본 기능 검토) -> 2022년 2단계(모의실험, 서울 메타버스 시뮬레이션) -> 2024년 3단계(실물 거래, 토큰 예치 기반) -> 2026년 파일럿 연장으로 「원화 디지털 화폐(KDC, Korean Digital Currency)」 사업을 단계적으로 추진하고 있다. 미국은 2025년 1월 대통령 행정명령 14178으로 CBDC 금지 및 「FedNow」 기반 대체 노선을 강화했고, EU는 2025년 11월 「Digital Euro Regulation」 초안 발의, 중국은 2024년 6월 기준 e-CNY 거래액 **7조 위안(누적 16.5억 건)** 돌파, ECB는 2025년 10월 「Preparation Phase」에 돌입했다.

```text
[CBDC의 위치: 화폐 사슬(Money Flower) 4차원 매트릭스]

                       발 행 주 체
                  중앙은행         민간은행·비은행
                +--------------+--------------+
   디  |  중앙은행   |   ◆ 현금(Cash)    |  ◆ 은행예금     |
   지  |  (B-M)     |  ◆ DCEP/e-CNY    |  ◆ 모바일뱅킹   |
   털  |            |  ◆ Sand Dollar   |  ◆ M-Pesa      |
   형  |  디지털    |  ◆ Digital Euro  |                |
   식  |            |  ◆ KDC(예정)    |                |
   |  토  |  중앙은행  |  ◆ FedNow       |  ◆ PayPal      |
   |  큰  |  (B-T)    |  ◆ TIPS         |  ◆ Venmo       |
   |  형  |  디지털  |  ◆ RTGS-Hash    |  ◆ Alipay+     |
        |            |                |  ◆ 카카오페이   |
        |  민간      |  ◆ Bitcoin      |  ◆ Libra/Diem  |
        |  (P-T)     |  ◆ USDC/USDT    |  ◆ e-KRW(이슈) |
        +--------------+--------------+--------------+

  ◆ B = Bank-issued, P = Privately-issued
  ◆ M = Money/Account-based, T = Token-based
  ※ Bechara & Bossu(컨설팅사) "The Money Flower" 4분면 재구성
```

**왜 필요한가 — 구(舊) 패러다임 vs 신(新) 패러다임**

| 차원 | 기존 패러다임 | CBDC 패러다임 |
|:---|:---|:---|
| 화폐 단위성 | 현금(중앙은행) + 예금(상업은행) | 단일 디지털 화폐로 통합 가능 |
| 결제 인프라 | ACH·카드로 2~3일, 카드 수수료 1.5~3% | **즉시 결제(Instant), P2P, 수수료 ≒ 0** |
| 통화정책 전달 | 양적완화 -> 은행 -> 시중 | **헬리콥터 머니(차등 이자)** 직접 가능 |
| 프라이버시 | 현금은 무기명, 카드는 실명 추적 | **선별적 감사(Selective Disclosure)** 균형 |
| 국경 간 결제 | SWIFT(2단계) + 코레스펀딩(3일) | **원장 간 atomic swap, PvP 1초** |
| 단일 통화 정책 | 불가(해외 USD 결제 시 세금=0) | **CBDC 환차손 페널티(±5%) 정책** 가능 |
| 단일 장애점 | 카드사·은행 중앙화(SPOF) | **이중 운영(Dual Operator)**, 다중 노드 |
| 스테이블코인 대응 | USDT/USDC 시가총액 $200B(2024) | **CBDC의 법적 지급력**으로 견제 |

- **📢 섹션 요약 비유**: "한 나라의 화폐는 마치 **수도관(파이프)**과 같다. 기존 현금은 동전·지폐(배관)이고, 은행예금은 저수조다. CBDC는 **IoT 센서가 부착된 스마트 수도관**으로, 물(돈)의 흐름·양·속도·품질을 실시간으로 측정·조절할 수 있다. 카카오·토큰증권이 만들어낸 **민간 수도관(스테이블코인)**에 우리 수도물을 빼앗기지 않으려면, 국가가 직접 디지털 수도관을 깔아야 한다."

---

## Ⅱ. 아키텍처 및 핵심 원리

CBDC 시스템은 **발행·유통·결제·환매(상환)** 4계층 책임 모델이 표준이다(BIS 보고서 "Central bank digital currency: foundational principles", 2020; 2024 보완). 통상 **이중 운영자 모델(Dual-Operator Model)** — 중앙은행(CBDC 코어) + 민간 지급결제사업자(PSP, Payment Service Provider) — 로 구성되어, 중앙은행은 무결성·안정성·정책을, 민간은 UX·KYC·혁신을 담당한다.

```text
[CBDC 2-tier 아키텍처 + 이중 운영자 모델 — 한국형 KDC 참조]

 +------------------------------------------------------------------+
 |                    1계층: 중앙은행 (BOK Core)                      |
 |  +----------------+  +-----------------+  +------------------+  |
 |  | CBDC 코어      |  |  분산원장(DLT)   |  | 정책 모듈         |  |
 |  |  발행/환매 엔진 |<-->| 노드 N개 (BFT)   |<-->| - 한도 관리       |  |
 |  |  정책 결정      |  | - Hot/Cold 분리 |  | - 이율(remuner.)  |  |
 |  |  감독·감사      |  | - MPC 서명       |  | - 한도초과 시 환매 |  |
 |  +----------------+  +-----------------+  +------------------+  |
 +------------------------------+-----------------------------------+
                                | [Settlement Interface]
                                |  ISO 20022, API Gateway
                                v
 +------------------------------------------------------------------+
 |             2계층: 민간 PSP(은행·핀테크·이통사)                       |
 |  +--------------+ +--------------+ +--------------+              |
 |  | 은행 지갑     | | 핀테크 지갑   | | 가맹점 단말   |              |
 |  | - 실명 KYC   | | - Kakao Pay  | | - POS/PQC    |              |
 |  | - CASP 자격  | | - Toss Pay   | | - QR/Offline |              |
 |  +--------------+ +--------------+ +--------------+              |
 +------------------------------+-----------------------------------+
                                |
                  +-------------+-------------+
                  v             v             v
            +---------+  +----------+  +----------+
            | 개인   |  |  기업    |  |  가맹점  |
            | P2P/QR |  | B2B/PvP  |  | PoS/MoMo|
            +---------+  +----------+  +----------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **① CBDC 코어(Core Ledger)** | 발행·환매·정산·감독의 단일 진실 공급원(SSOT) | Hot/Cold 월렛 분할, **HSM(Thales Luna HSM)** 기반 키 관리, **BFT 합의(Tendermint·HotStuff·Istanbul BFT)** 100노드 기준 TPS 3,000~10,000, HSM 내부 **MPC(Multi-Party Computation) 서명** (k-of-n, 2-of-3) |
| **② 정책 모듈(Policy Engine)** | 한도·이율·프로그래머빌리티 집행 | 잔액 한도(예: 개인 5,000만원, e-CNY는 1만원/일), 보유 이율(0% or 차등, ECB 디지털유로는 remuneration 미결정), 만기·조건부 결제(smart contract, **DAML·Corda·Hyperledger Fabric 체인코드**) |
| **③ 유통/지급 인프라(2-tier Distribution)** | PSP를 통한 온보딩·지갑 발급·KYC | **eIDAS 2.0 EUDI 지갑**(EU)·**신원증명 DID**(한국), PBOC의 4-tier 운영(인민은행 -> 상업은행 -> 위챗/알리페이 -> 사용자) |
| **④ 오프라인 결제 모듈** | 네트워크 미가용 시 이중사용 방지 | **단거리 통신(NFC/BLE)** + **Secure Element(SE, TEE+SE)** + **디지털 봉투(Digital Envelope)·이중사용 토큰**, Project Tourbillon(스위스 BIS+SNB)의 **키-체인지 프로토콜**, Anand-Caianiello-Visconti 기법 (ACM TISSEC 2019) |
| **⑤ 프라이버시/감사 레이어** | AML/CFT와 익명성 양립 | **ZK-SNARK(Plonk·Halo2)·ZK-STARK**, **선별적 감사(Trusted Auditor + Key Escrow)**, **링 서명·페더레이션 학습**, 상한 1,000유로까지 익명(ECB 디지털유로) |
| **⑥ 국경 간 결제(Cross-Border)** | 다국 CBDC 정산 | **Project mBridge**(BIS·BOK·PBoC·CBMA·BISIH, 2024.6 MVP 운영) — **단일 통화 차익거래 방지(UNIQUE) + 단일 공통 플랫폼**, **Project Agorá**(BIS 7개국, 2024.4~) — 통합 원장 + 토큰 상업은행예금, **Project Mariana 합성 CBDC**, **Project Pyxtrial** FX MVP |

### 핵심 프로토콜·알고리즘 — 깊이 있는 기술 검토

**1. 데이터 모델: Account-Based vs Token-Based(UTXO)**

| 항목 | Account-Based (계좌 기반) | Token-Based/UTXO (토큰 기반) |
|:---|:---|:---|
| 모델 | 잔액 필드 단일 값, 트랜잭션 = 차감/가산 | 미사용 출력(Unspent Transaction Output) 집합 |
| 대표 사례 | **Sweden e-krona(잠정)**, **Digital Euro(ECB 권고)**, **UK RTGS Renewal** | **e-CNY(DCEP)** — 일부는 account, 일부는 UTXO, **Bitcoin형** |
| 프라이버시 | 낮음(계좌 추적 용이) | 높음(일회용 토큰, 링 서명 시 거의 익명) |
| 병렬 처리 | 어려움(순서 제약) | 용이(UTXO 독립 처리) |
| 스마트 컨트랙트 | 용이 | 어려움 |
| 확장성 | 단일 원장 = 병목 | **Zerocash/Zcash Shielded Pool** 처럼 확장 시 성능 저하 |

**2. 합의 알고리즘**

- **HotStuff** (Facebook Libra 후속 Aptos/Sui 사용): 3-phase commit, 파이프라이닝으로 BFT 합의를 ms 단위로 — CBDC의 1,000~3,000 TPS 요구에 적합
- **Istanbul BFT(Quorum)**: BOK 1단계 모의실험에 사용, PBFT 변형으로 Hyperledger Besu에서 구동
- **QuorumChain**(ConsenSys): 개인정보 보호(Private State) 기능으로 영란도은행의 DUKCHOI 등

**3. 오프라인 이중사용 방지 (Double-Spend Prevention)**

- **Anand-Caianiello-Visconti(2019) 기법**: Secure Element 안에서 토큰을 한 번만 사용 가능하게 **키-체인 갱신** 후 만료. POS·오프라인 결제 단말에 적합
- **Project Tourbillon BIS Innovation Hub 2023**: 잔액 단편화(sharding) + 익명성 + 오프라인 동시 달성
- **MIT/BOK 공동연구 (2022)**: QR 기반 P2P 오프라인 + NFC 인증, latency < 2초

**4. 프로그래머빌리티(Programmable Money)**

- **DAML(Digital Asset Modeling Language)**: Digital Asset社, 2-tier에서 PSP가 자체 스마트 컨트랙트 배포
- **Solidity/EVM**: Sandbox 격리, 1계층은 whitelist만, 2계층 PSP에서 자유
- **조건부 결제 사례**: 한국 정부 긴급재난지원금(차등 이자율, 사용처 제한), PBoC의 **롯tery·red packet** 기능(가중치 기반)

**5. 양자내성암호(PQC) 도입 — 장기 보안**

- **NIST PQC 표준(2024.8)**: ML-KEM(Kyber, FIPS 203), ML-DSA(Dilithium, FIPS 204), SLH-DSA(SPHINCS+, FIPS 205)
- CBDC 서명 알고리즘은 **EdDSA/ECDSA -> Dilithium2/3** 로 2030년경 마이그레이션 권고 (BIS Cyber Resilience Guide 2024)
- HSM 펌웨어 업데이트로 무중단 전환 필요 (Thales/PKI/Fortanix)

- **📢 섹션 요약 비유**: "CBDC 시스템은 **공항 4단 구조**와 같다. 1층은 **관제탑**(중앙은행 코어, BFT