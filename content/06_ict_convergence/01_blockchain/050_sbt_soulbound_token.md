---
title: "Soulbound Token"
date: "2025-01-01"
tags:
  - "DID"
  - "DeSoc"
  - "NFT"
  - "SBT"
  - "Web3 identity"
  - "non-transferable"
  - "soulbound token"
  - "verifiable credential"
  - "studynote-ict-convergence"
weight: 50
---
> **핵심 인사이트 3줄**
> 1. SBT(Soulbound Token)는 특정 지갑(Soul)에 영구 귀속되어 양도·판매할 수 없는 비양도성 토큰으로, Web3 신원·자격 증명의 핵심 도구다.
> 2. 학력증명, 직업 이력, 의료 기록 등 개인의 사회적 자본을 온체인 표현으로 관리해 탈중앙화 사회(DeSoc, Decentralized Society)를 지향한다.
> 3. 비양도성이 개인정보 보호와 충돌하는 문제(영구 온체인 기록)를 해결하기 위해 영지식 증명(ZKP)과 결합한 프라이버시 SBT가 연구 중이다.

---

## Ⅰ. SBT 개요

### 1.1 배경과 제안

- 2022년 Vitalik Buterin, E. Glen Weyl, Puja Ohlhaver의 논문 "Decentralized Society: Finding Web3's Soul"에서 제안
- 기존 NFT의 문제: 모든 가치가 시장 가격(양도 가능성)에만 집중 -> 사회적 신뢰, 자격 증명 표현 불가

### 1.2 SBT vs NFT 비교

| 특성        | NFT                      | SBT                        |
|-----------|--------------------------|----------------------------|
| 양도성      | 가능 (marketplace 거래)  | 불가 (발행 지갑에 귀속)     |
| 표현 대상   | 소유권, 자산              | 신원, 자격, 성취            |
| 취소 가능성 | 불가 (소각 외)            | 발행자가 회수 가능           |
| 금전 가치   | 주요 목적                 | 부차적                      |

📢 **섹션 요약 비유**: NFT는 팔 수 있는 트로피, SBT는 박힌 훈장 — 남에게 못 주고 본인을 증명하는 데만 쓴다.

---

## Ⅱ. Soul과 DeSoc 구조

### 2.1 Soul (소울) 개념

```
Soul (지갑/DID)
+-- 학력 SBT (발행: 대학)
+-- 직업 이력 SBT (발행: 회사)
+-- 의료 기록 SBT (발행: 병원)
+-- DAO 투표권 SBT (발행: DAO)
+-- 범죄 기록 SBT (발행: 법원)
```

각 SBT는 발행자(Issuer)와 수신자(Soul) 모두 서명.

### 2.2 DeSoc 시나리오

- **담보 없는 대출**: Soul이 보유한 커뮤니티 SBT -> 신용 평가 대체
- <strong>DAO 투표 조작 방지</strong>: SBT 기반 고유 신원 -> 시빌 공격 방지
- <strong>학력 인증</strong>: 대학이 발행한 학위 SBT -> 위조 불가

📢 **섹션 요약 비유**: Soul은 디지털 이력서 가방 — 학교, 회사, 병원이 각자 도장(SBT)을 찍어주는데 다른 사람에게 못 넘긴다.

---

## Ⅲ. 기술 구현

### 3.1 EIP-5192 (최소 SBT 표준)

```solidity
// EIP-5192 인터페이스
interface IERC5192 {
    event Locked(uint256 tokenId);
    event Unlocked(uint256 tokenId);
    function locked(uint256 tokenId) external view returns (bool);
}
```

ERC-721 기반에 `locked()` 함수 추가 -> transferFrom 시 locked=true면 revert.

### 3.2 발행 흐름

```
발행자 -> [서명 요청] -> Soul 소유자
                              v
                      수락 서명 -> 온체인 민팅
                              v
                      Soul 지갑에 귀속 (양도 불가)
```

📢 **섹션 요약 비유**: SBT 발행은 학교가 학생에게 졸업장 주는 것 — 학교와 학생 둘 다 서명해야 효력 발생.

---

## Ⅳ. 개인정보 이슈와 ZKP

### 4.1 온체인 공개 문제

SBT가 퍼블릭 블록체인에 기록되면 누구나 해당 Soul의 모든 SBT를 볼 수 있다 -> 프라이버시 침해.

### 4.2 ZKP 기반 프라이버시 SBT

```
증명 시나리오:
"나는 대학 졸업자다" -> SBT 내용 공개 X
ZK 증명: 졸업 SBT 보유 증명 + 내용 숨김
         v
검증자: 졸업 여부만 확인, 학교 이름·성적 모름
```

### 4.3 망각권(Right to Be Forgotten) 문제

- 블록체인의 불변성 vs GDPR 망각권 충돌
- 해결책: 오프체인에 SBT 데이터 저장 + 온체인에 해시만 -> 오프체인 데이터 삭제 시 검증 불가 처리

📢 **섹션 요약 비유**: ZKP SBT는 "나이 확인" 시 생년월일 전체가 아닌 "성인 여부만" 보여주는 것 — 필요한 사실만 증명.

---

## Ⅴ. 현황과 한계

### 5.1 실사례

| 프로젝트          | 내용                                     |
|-----------------|------------------------------------------|
| Gitcoin Passport | 온체인 신원 검증 -> 시빌 저항 투표        |
| Binance BAB     | KYC 완료 증명 SBT (최초 대형 SBT 사례)  |
| Lens Protocol   | 팔로우, 포스트 등 소셜 그래프 SBT 기반  |

### 5.2 주요 한계

- **지갑 분실**: 복구 메커니즘 미표준화 (커뮤니티 복구 proposal 연구 중)
- **부정 SBT**: 원치 않는 SBT 강제 발행 (예: 범죄 기록) 거부 메커니즘 필요
- <strong>상호운용성</strong>: 체인 간 SBT 연동 미표준

📢 **섹션 요약 비유**: SBT는 지우기 어려운 문신처럼 강력하지만 — 원치 않는 문신을 누가 새기면 막기 어렵다.

---

## 📌 관련 개념 맵

```
SBT (Soulbound Token)
+-- 기반 기술
|   +-- ERC-721 + EIP-5192
|   +-- DID (Decentralized Identity)
|   +-- ZKP (Zero-Knowledge Proof)
+-- 활용
|   +-- 학력/이력 증명
|   +-- DAO 신원 증명
|   +-- 탈중앙 신용 평가
+-- 과제
    +-- 프라이버시 (ZKP 결합)
    +-- 망각권 (GDPR 충돌)
    +-- 지갑 복구
```

---

## 📈 관련 키워드 및 발전 흐름도

```
NFT (2017~) — 양도 가능 자산 표현
     |  신원·자격 표현 필요
     v
SBT 논문 — Buterin et al. (2022)
     |  표준화 진행
     v
EIP-5192 (최소 표준, 2022)
     |  프라이버시 강화 요구
     v
ZKP SBT / 오프체인 SBT (현재 연구)
     |  DeSoc 인프라
     v
Web3 탈중앙 신원 생태계 (미래)
```

**핵심 키워드**: 비양도성, Soul, DeSoc, EIP-5192, ZKP, DID, 망각권, Gitcoin

---

## 👶 어린이를 위한 3줄 비유 설명

1. SBT는 내 이름이 새겨진 훈장처럼 — 다른 사람에게 팔거나 줄 수 없어.
2. 학교, 회사, 병원이 내 지갑에 직접 "졸업", "취업", "검진 완료" 도장을 찍어줘.
3. ZKP를 쓰면 "졸업했냐?"는 질문에 "예"라고만 대답하고 어느 학교인지는 비밀로 할 수 있어.
