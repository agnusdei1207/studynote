---
title: "Pirate Metrics"
date: "2026-04-05"
tags:
  - "studynote-enterprise-systems"
weight: 43
---
> **핵심 인사이트**
> 1. AARRR(Acquisition -> Activation -> Retention -> Referral -> Revenue)은 Dave McClure가 2007년 제안한 스타트업 성장 지표 프레임워크로 — 각 단계별 전환율을 측정하고 병목(Bottleneck) 단계를 식별해 집중 개선하는 데이터 기반 성장 전략의 핵심이다.
> 2. AARRR의 핵심 통찰은 "가장 약한 단계가 전체 성장을 제한한다"는 병목 이론으로 — Activation 단계에서 30%를 잃으면 이후 아무리 Retention을 개선해도 시작 사용자가 적어 효과가 제한되므로 단계 순서대로 개선 우선순위를 정해야 한다.
> 3. 현대 PLG(Product-Led Growth) 시대에 AARRR은 RARRA(Retention -> Activation -> Referral -> Revenue -> Acquisition)로 재정렬되는 경향이 있으며 — Retention이 모든 것의 기초임을 강조하고, 기존 사용자 유지가 신규 획득보다 비용 효율이 높다는 실증 연구 결과를 반영한다.

---

## Ⅰ. AARRR 5단계 프레임워크

```
AARRR (Pirate Metrics) 프레임워크:

A - Acquisition (획득):
  정의: 잠재 사용자가 우리 제품/서비스를 처음 알게 되는 단계
  채널: SEO, SEM, SNS, 바이럴, 오프라인, PR
  핵심 지표: DAU/MAU, CAC(고객 획득 비용), 채널별 CPA
  질문: "사람들이 어디서 우리를 발견하나?"

A - Activation (활성화):
  정의: 사용자가 첫 번째 핵심 가치를 경험하는 단계
  Aha Moment: "이 제품이 왜 좋은지" 느끼는 순간
    Dropbox: 첫 파일 동기화
    Twitter: 30명 팔로우
    Slack: 팀원 메시지 2,000건
  핵심 지표: 온보딩 완료율, 첫 핵심 기능 사용률
  질문: "사람들이 서비스의 가치를 느끼나?"

R - Retention (유지):
  정의: 활성화된 사용자가 반복 사용하는 단계
  핵심 지표: D1/D7/D30 유지율, Churn Rate
  D30 벤치마크: 소비자앱 20~25%, SaaS 35~50%
  질문: "사람들이 다시 돌아오나?"

R - Referral (추천):
  정의: 만족한 사용자가 다른 사람을 추천하는 단계
  바이럴 계수 K = (초대 발송률) × (수락률)
  K > 1 = 자가 증식 성장
  질문: "사람들이 우리를 친구에게 추천하나?"

R - Revenue (수익):
  정의: 실제 수익이 발생하는 단계
  핵심 지표: ARPU, LTV, LTV:CAC 비율
  LTV:CAC > 3 = 건강한 단위 경제
  질문: "사람들이 실제로 돈을 내나?"
```

> 📢 **섹션 요약 비유**: AARRR은 고객 여정의 5개 체크포인트 — 가게 발견(A) -> 첫 방문 경험(A) -> 단골 되기(R) -> 지인 소개(R) -> 실제 구매(R).

---

## Ⅱ. 코호트 분석과 병목 탐지

```
코호트 분석 (Cohort Analysis):
  동일 시점 가입/행동 그룹을 시간에 따라 추적

  예시: 2026년 1월 가입자 코호트

  주(Week) | 활성 사용자 | 유지율
  ---------+-------------|-------
  Week 0   |    10,000   | 100%
  Week 1   |     5,200   |  52%
  Week 2   |     3,100   |  31%
  Week 4   |     2,000   |  20%
  Week 8   |     1,500   |  15%

  -> D30 유지율 15% (개선 필요: 업종 평균 20%)

병목 분석 퍼널:

  단계          | 전환율 | 이탈율
  --------------+--------+-------
  방문          | 100%   |
  회원가입      |  25%   | 75% 이탈 <- 병목 1
  온보딩 완료   |  40%   | 60% 이탈 <- 병목 2
  첫 결제       |  15%   | 85% 이탈
  2회 결제      |  60%   | 40% 이탈

  분석:
    회원가입 25% (산업 평균 35%) -> 랜딩 페이지 개선 필요
    온보딩 완료 40% (산업 평균 55%) -> 온보딩 UX 개선 필요

도구:
  Amplitude: 이벤트 기반 코호트 분석
  Mixpanel: 퍼널 분석, 사용자 흐름 시각화
  Google Analytics 4: 코호트 리포트
  Looker/BigQuery: 커스텀 SQL 코호트 쿼리
```

> 📢 **섹션 요약 비유**: 코호트 분석은 같은 학번 친구들 추적 — 2022년 입학생이 졸업률 몇 %인지 연도별로 추적, 어느 학년에서 많이 떠나는지 파악.

---

## Ⅲ. North Star Metric과 지표 계층

```
North Star Metric (NSM):
  회사 전체가 집중하는 단일 핵심 지표
  장기 가치 창출을 대표

  성공 사례:
    Airbnb: "예약 야간 수" (숙박 횟수)
    Spotify: "구독 청취 시간"
    WhatsApp: "메시지 발송 수"
    Slack: "팀 내 메시지 2,000건"
    Netflix: "구독 시청 시간"

지표 계층 구조:

  North Star Metric (1개)
  v
  L1 Drivers (2-5개): NSM에 직접 기여
  v
  L2 Sub-drivers (5-15개): L1 지표 분해
  v
  실험 지표: A/B 테스트 단기 측정

Leading vs Lagging Indicator:
  Leading: 미래 결과를 예측하는 선행 지표
    D7 유지율 -> 미래 LTV 예측
  Lagging: 과거 결과를 나타내는 후행 지표
    월간 매출 -> 과거 성과 반영

  실전 원칙:
    Leading으로 일상 모니터링
    Lagging으로 최종 성과 확인

Guardrail Metric:
  NSM 개선 과정에서 훼손되어선 안 되는 지표
  예: DAU 올리려다 사용자 경험 악화 방지
      "이탈률 2% 이상 증가하면 실험 중단"
```

> 📢 **섹션 요약 비유**: North Star Metric은 등대 — 모든 배(팀)가 하나의 등대(NSM)를 보며 방향을 맞추면 각자 다른 항로를 가도 결국 같은 방향.

---

## Ⅳ. RARRA와 현대적 재해석

```
RARRA 재정렬:
  원래: AARRR (Acquisition 중심)
  현대: RARRA (Retention 중심)

  Retention -> Activation -> Referral -> Revenue -> Acquisition

  이유:
    유지율이 높으면 LTV가 높아져 더 많은 CAC 투자 가능
    기존 고객 유지 = 신규 고객 획득의 5배 저렴
    "구멍 뚫린 통에 물 붓기"는 먼저 통을 고쳐야

PLG (Product-Led Growth):
  제품 자체가 성장 엔진
  영업/마케팅 없이 제품으로 고객 획득

  PLG 지표:
    PQL (Product Qualified Lead):
      제품 내 특정 행동 = 구매 의향 신호
      예: Slack - 팀원 5명 추가 완료 = PQL

  PLG 기업 사례:
    Slack: 무료 사용 -> 팀 확대 -> 유료 전환
    Figma: 링크 공유 -> 팀원 초대 -> 구독
    Dropbox: 용량 부족 -> 유료 업그레이드

AARRR 2.0 — 커뮤니티 추가:
  일부 기업: 커뮤니티(Community)를 별도 단계로 추가
  예: GitHub - Star, Fork, Discussion이 Retention + Referral
  Discord 서버 운영 = 커뮤니티 기반 Retention 전략
```

> 📢 **섹션 요약 비유**: RARRA는 집 수리 우선순위 — 새 가구 사기(Acquisition) 전에 벽 균열(Retention 문제) 먼저 고치는 게 순서. 구멍 뚫린 통에 물 부어봐야 금방 비어요.

---

## Ⅴ. 실무 시나리오 — SaaS 성장 전략

```
B2B SaaS 그로스 해킹 AARRR 분석:

회사 현황: 생산성 도구 SaaS
  MAU: 15,000명
  월간 매출: 1.5억원
  목표: 1년 내 MAU 100,000명

AARRR 현황 진단:
  Acquisition:
    주요 채널: 오가닉 SEO 50%, 유료 광고 30%, 추천 20%
    CAC: SEO $15, 유료 광고 $120

  Activation:
    온보딩 완료율: 38% (업계 평균 55%) <- 문제
    Aha Moment: "첫 팀 프로젝트 생성 + 팀원 초대"

  Retention:
    D30 유지율: 42% (SaaS 평균 40%) <- 보통
    Churn Rate: 4%/월 (연간 38%) <- 개선 여지

  Referral:
    K 계수: 0.25 <- 낮음 (추천 인센티브 부재)

  Revenue:
    ARPU: $10/월
    LTV: $250 (25개월 평균 유지)
    LTV:CAC = 250:15 = 16.7 (SEO 채널 우수)
    LTV:CAC = 250:120 = 2.1 (유료 광고 위험)

개선 로드맵:
  Q1: Activation 개선 (38% -> 55%)
    -> 인터랙티브 온보딩 재설계
    -> 첫 5분 내 팀원 초대 유도

  Q2: Retention 개선 (42% -> 55%)
    -> 주간 사용량 리포트 이메일
    -> 비활성 사용자 재활성화 캠페인

  Q3: Referral 추가 (K: 0.25 -> 0.7)
    -> 팀원 추천 인센티브 (무료 플랜 연장)

  Q4: CAC 최적화
    -> 유료 광고 줄이고 SEO/Referral 확대

예상 결과:
  MAU 15,000 -> 45,000 (3배, Activation+Retention 개선)
  + Referral K=0.7 -> 추가 20% 바이럴 성장
  -> MAU 50,000~60,000 달성 예상
```

> 📢 **섹션 요약 비유**: AARRR 분석은 자동차 점검표 — 각 바퀴(단계)의 공기압을 확인하고, 가장 빠진 타이어(병목)부터 먼저 수리해야 달릴 수 있어요.

---

## 📌 관련 개념 맵

```
AARRR 퍼널
+-- 5단계
|   +-- Acquisition (획득)
|   +-- Activation (활성화) - Aha Moment
|   +-- Retention (유지) - Cohort
|   +-- Referral (추천) - K 계수
|   +-- Revenue (수익) - LTV:CAC
+-- 분석 도구
|   +-- 코호트 분석
|   +-- North Star Metric
|   +-- Guardrail Metric
+-- 현대 변형
|   +-- RARRA (Retention 중심)
|   +-- PLG, PQL
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 마케팅 퍼널 (AIDA, 1898)]
Awareness -> Interest -> Desire -> Action
      |
      v
[Dave McClure AARRR 제안 (2007)]
500 Startups 컨퍼런스
"Startup Metrics for Pirates"
      |
      v
[린 스타트업과 결합 (2011~)]
Eric Ries Lean Startup
검증된 학습 + AARRR 지표 통합
      |
      v
[데이터 도구 성숙 (2015~)]
Mixpanel, Amplitude 등장
AARRR 자동화 측정 가능
      |
      v
[PLG 시대 (2020s~)]
RARRA 재정렬 트렌드
Product-Led Growth 주류화
Figma, Notion, Slack 모델
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. AARRR은 고객 여행의 5단계 — 가게 발견, 첫 방문, 단골, 친구 소개, 구매까지 각 단계를 측정해요!
2. 가장 약한 단계가 병목 — 10명이 들어와서 5명이 나가면, 뒤에서 아무리 열심히 해도 시작이 5명이에요.
3. 현대는 RARRA — 새 손님 끌기 전에 기존 손님이 왜 떠나는지 먼저 고치는 게 훨씬 효율적이에요!
