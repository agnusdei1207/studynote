---
title: "Technology Forecasting Hype Cycle Roadmap"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 776
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Gartner Hype Cycle은 기술의 가시적 기대치(Visibility)와 성숙도(Maturity)를 5단계(Innovation Trigger -> Peak of Inflated Expectations -> Trough of Disillusionment -> Slope of Enlightenment -> Plateau of Productivity)로 시각화한 기술 예측 프레임워크이며, Technology Roadmap은 시간 축(Time Horizon)에 따른 기술 진화·이전·대체 경로를 MIL(Market-Industry-Leverage) 또는 GTM(Go-To-Market) 관점에서 매핑하는 전략 산출물이다.
> 2. **가치**: TRL(Technology Readiness Level 1~9)·BRT(Benefit Rating)·RT(Risk Rating) 3축 매트릭스를 하이프 사이클 위상에 매핑하면 R&D 포트폴리오의 편중을 정량화하고, 조기 신호 조달(T-36~T-12개월)·파일럿 전환(T-12~T-6개월)·본격 확산(T-6~0개월) 시점의 의사결정 리드타임을 평균 40~60% 단축할 수 있다.
> 3. **판단 포인트**: 핵심 트레이드오프는 (a) Trough 단계에서 조기 이탈(Early Exit) vs 관조 투자(Patient Capital), (b) 표준화·개방형(Open) 로드맵 채택 vs 독자·폐쇄(Closed) 로드맵, (c) 단일 S-curve(Inside-the-fence) 접근 vs 다중 S-curve(Outside-the-fence) 도약 결정이며, 실무자는 S-curve의 한계(discontinuity·architectural shift) 시점에서 BCF(Bandwagon-Chasm-Follower) 동기화 결정을 내려야 한다.

---

## Ⅰ. 개요 및 필요성

IT 거버넌스·EA(Enterprise Architecture)·중장기 R&D 계획 수립에서 가장 빈번하게 발생하는 실패 원인은 "기술의 실제 성숙도와 시장 과잉기대 사이의 갭(Gap)"을 정량화하지 못한 채 투자 결정을 내리는 것이다. Gartner Hype Cycle(1995년 Jackie Fenn 박사 제시)은 1,000여 개 신생 기술을 매년 추적하여 5단계 위상에 분류하고, Technology Roadmap(TRM, 1970년대 Motorola·P&G 계열에서 출발, 현재는 IEEE 2919-2022 표준까지 제정)은 시간·시장·기술 3축의 통합 경로로 발전시켜 두 프레임워크는 상호 보완적으로 사용된다.

기술 예측 프레임워크가 필요한 핵심 배경은 다음과 같다:
- **Carlota Perez의 기술-경제 패러다임(Techno-Economic Paradigm, 5~60년 주기)** 관점에서 현재 우리는 4차 산업혁명(I4.0) -> Cyber-Physical Systems로 이행 중이며, 1개 혁명 주기 안에 약 5~7개의 Hype Cycle Peak가 발생함.
- **Rogers의 기술수용이론(Diffusion of Innovation, 1962)**에서 정의한 Chasm(이 지점, 초기采纳자 ~ 초기다수采纳자 사이 16% 갭)와 Hype Cycle의 Trough는 사실 동일한 현상의 다른 시각으로, 하이프 사이클의 Trough는 시장가시성(Visibility) 차원, Chasm은 채택률(Adoption Rate) 차원.
- **PESTEL/STP/SWOT** 같은 정적 분석은 T-0 시점 스냅샷에 그치지만, 하이프 사이클 + 로드맵은 T-24~T+60개월의 동적 궤적(Dynamic Trajectory)을 제공.
- **TRL 1~9 체계**는 NASA·DARPA·ETRI(한국전자통신연구원) 등 공공 R&D에서 표준이며, 하이프 사이클 위상과의 1:1 매핑(예: TRL 1~3 = Innovation Trigger, TRL 4~6 = Peak/Trough, TRL 7~9 = Plateau)으로 양 프레임워크 통합 가능.

```
+----------------------------------------------------------------------------+
|        하이프 사이클 + 기술 로드맵 통합 의사결정 프레임워크                |
+----------------------------------------------------------------------------+
|                                                                            |
|  Expectations (가시성)                                                    |
|   ^                                                                       |
|   |      Peak --------+                                                    |
|   |     ╱   ╲  Peak of |   "    . :  '.  ___  .-  -___                    |
|   |    ╱     ╲Inflated |            :   '   '.    '                       |
|   |   ╱       ╲Expect. |   "  .-'  '.   '        '                       |
|   |  ╱  Trough ╲_______|___  ___ ' .  -----  ___ --- Plateau of            |
|   | ╱  of Disill.       |  -----  ___  .---------      Productivity        |
|   |╱________ Slope of  |  ___________  .  ----  .-                         |
|   |       Enlighten.   | ---  .  .-  '.  ___                               |
|   |  Innovation        |  .  -'                                          |
|   |  Trigger           |                                                  |
|   +--------------------+-----------------------------------> Time           |
|   T-36  T-24  T-12  T-6  T-3  T0  T+6  T+12  T+24  T+36 (months)         |
|                                                                            |
|  +------------------------------------------------------------------+     |
|  |  Phase:    IT       Peak       Trough     Slope    Plateau       |     |
|  |  TRL:      1-3      4-5         5-6        6-8       8-9          |     |
|  |  Adoption: <2.5%   2.5-13%   13-16%     16-50%    >50%           |     |
|  |  투자:     시드    VC확대    전략재검토   파일럿    본격확산         |     |
|  |  표준화:    없음    PoC        Draft     v1.0      ISO/IEC       |     |
|  |  위험:     기술     시장       운영      통합      거버넌스       |     |
|  +------------------------------------------------------------------+     |
|                                                                            |
|  <--- Technology Push (기술주도) ------ Market Pull (시장견인) --->          |
+----------------------------------------------------------------------------+
```

**기존 정적 분석 vs 하이프 사이클+로드맵 동적 분석 비교**:
- **기존 SWOT/PEST**: T-0 시점 단일 스냅샷, 기술의 시간 의존성(Time Decay) 무시.
- **TRL 단독**: 기술 성숙도만 평가, 시장·비용·규제 측면 누락.
- **하이프 사이클+로드맵**: TRL × BRT(Benefit Rating) × RT(Risk Rating) × 시장 가시성을 5×5 매트릭스로 통합, 시간 축 위의 궤적과 변곡점(Inflection Point)까지 추적.

- **📢 섹션 요약 비유**: 하이프 사이클은 신상품을 매대 앞에 진열한 후 손님이 몰리는 파도(Peak)를 재는 "**슈퍼마켓 매출 모니터**"이고, 로드맵은 그 파도가 어느 코너(매대)로 언제 옮겨갈지 미리 정해두는 "**매장 동선 계획도**"입니다. 실무자는 슈퍼마켓 관리가 아니라 동선 계획까지 같이 봐야 진짜 의사결정이 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

하이프 사이클+로드맵의 5단계 위상(Phase) 각각은 독립적인 **결정 규칙(Decision Rule)**, **투자 지표(KPI)**, **산출물(Artifact)**을 가지며, 로드맵의 시간축 위에서 MIL-3-Layer(Market·Industry·Leverage) 또는 GTM-3-Stream(Buy·Build·Partner)와 직교(Cross)합니다.

```
+-------------------------------------------------------------------------+
|       5-Phase Hype Cycle × Time-Mapped Technology Roadmap (T-3y -> T+3y)|
+-------------------------------------------------------------------------+
|                                                                         |
| Phase 1. Innovation Trigger (혁신촉발)         T-36 ~ T-18m             |
|   +----------------------+                                              |
|   | Signal Sources:      |   +- Tech Radar (ThoughtWorks)              |
|   |  • 학회 논문 < 50건  |   +- Patent Citation Burst                   |
|   |  • Seed Funding <$5M |   +- Github Repo Star > 1k/월               |
|   |  • 표준화안 Draft    |   +- 내부 PoC 성공률 < 30%                  |
|   +----------+-----------+                                              |
|              v                                                           |
| Phase 2. Peak of Inflated Expectations (과잉기대 정점)  T-18 ~ T-6m   |
|   +----------------------+                                              |
|   | Vendors: VC funding 폭증|   "주도 벤더 수 > 30, M&A 급증"           |
|   | 메가라운드 > $100M  |                                              |
|   | 기사 노출도 x10     |                                              |
|   +----------+-----------+                                              |
|              v  <- "Trough 진입 조기 경보(Chasm Risk)"                  |
| Phase 3. Trough of Disillusionment (환멸의 골짜기)    T-6 ~ T+12m     |
|   +----------------------+                                              |
|   | 실패율 60~80%       |   • ROI 측정 불가 / PoC 정체                |
|   | 벤더 70% 퇴출       |   • "전사 표준" 선언 후 12m 내 후퇴         |
|   | 내부 회의 무한 PoC  |   • 탈-버즈워드(De-hype) 발생               |
|   +----------+-----------+                                              |
|              v  <- "2차 도약 트리거(Adjacent Innovation)"                |
| Phase 4. Slope of Enlightenment (계몽의 경사면)       T+12 ~ T+30m    |
|   +----------------------+                                              |
|   | 실사용 사례 등장    |   • SLA 정의 가능, Interop 표준화            |
|   | SaaS 가격 모델 정착 |   • 벤더 3~5개로 통합, Reference 가능        |
|   | Reference Architecture v1.0                                            |
|   +----------+-----------+                                              |
|              v                                                           |
| Phase 5. Plateau of Productivity (생산성 안정기)    T+30 ~ T+60m    |
|   +----------------------+                                              |
|   | 채택률 > 50%        |   • ISO/IEC·NIST 표준 제정                   |
|   | TCO 안정화          |   • Best Practice Cookbook 발행              |
|   | 거버넌스·정책 수립 |   • 시장 점유율 Top 3 안정 (HHI > 2000)      |
|   +----------------------+                                              |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  |  Roadmap Layer 1 (Market): TAM $5B -> SAM $1.2B -> SOM $200M      |  |
|  |  Roadmap Layer 2 (Industry): 규제·표준·벤더 생태계 타임라인       |  |
|  |  Roadmap Layer 3 (Leverage): Buy(70%) / Build(20%) / Partner(10%)|  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Phase 1: Innovation Trigger (혁신촉발)** | 잠재 기술의 씨앗 단계 식별 | 신호원(Signal Source) 수집 체계: arXiv·IEEE Xplore·USPTO 특허 인용 네트워크(PageRank)·GitHub Trending(>1k stars/월)·시드 펀딩 Crunchbase. 내부 PoC의 성공률 < 30% 시 본격 진입 보류. TRIZ의 S-curve Level 1~2(婴儿期·成長期 入口)에 해당. |
| **Phase 2: Peak of Inflated Expectations (과잉기대 정점)** | 미디어·VC가 만들어낸 버블 정량화 | Hype Index = α·(Press Volume Growth) + β·(VC Deal Value / 100M USD) + γ·(Vendor Count) + δ·(Patent Filing Growth). α+β+γ+δ=1, 가중치는 산업별 보정. 예: 생성형 AI 2023~2024 Peak 시 Hype Index = 0.85 (0~1 스케일). |
| **Phase 3: Trough of Disillusionment (환멸의 골짜기)** | 실패 프로젝트 정량·정성 진단 | Failure Mode Tracking: (a) ROI 미달 (35%), (b) Interop 실패 (25%), (c) 스킬 갭 (20%), (d) 규제 충돌 (10%), (e) 보 안 사고 (10%) — Moriarty·Wassenhove(2014) 분류 기반. Chasm 지표: "초기采纳자(Laggard 제외 2.5~13.5%)-> 초기다수采纳자(13.5~34%)" 갭에서 누적 채택률 기울기가 음(-)으로 전환하는 시점. |
| **Phase 4: Slope of Enlightenment (계몽의 경사면)** | 실증 사례 축적·레퍼런스 아키텍처 형성 | Reference Architecture v1.0 (TOGAF ADM Phase C 매핑), SLA 99.9% 정의, RFC(Internet Draft -> Proposed Standard 승격)·ITU-T Recommendation 확정, 2차·3차 벤더 등장으로 가격 벤치마크 형성. 이 단계 진입 신호: "현실적 ROI 사례 3건 이상"·"1년 이상 운영 중인 레퍼런스". |
| **Phase 5: Plateau of Productivity (생산성 안정기)** | 표준화·거버넌스·TCO 안정화 | 표준: ISO/IEC JTC1·IEEE-SA·IETF·W3C Recommendation 단계 진입. 거버넌스: COBIT 2019·ISO 38500 기반 정책·통제 항목 ≥ 12개. TCO: 5년 평균 CAPEX+OPEX 안정(편차 < 15%), 시장 HHI(Hirschman-Herfindahl Index) > 2000 (집중 시장) 또는 < 1500 (경쟁 시장) 중 전략적 위치 선택. |

**핵심 정량 파라미터 및 공식**:
- **Adoption Rate Diff. Eq.**: Bass Diffusion Model
  $\frac{dN(t)}{dt} = (p + q\frac{N(t)}{m})(m - N(t))$
  여기서 $p$ = 혁신계수(Innovation Coefficient, 통상 0.003~0.03), $q$ = 모방계수(Imitation Coefficient, 0.3~0.5), $m$ = 시장잠재량, $N(t)$ = 누적采纳자. 하이프 사이클의 Peak 시각은 $\frac{d^2N}{dt^2}=0$, Trough 시각은 $\frac{d^3N}{dt^3}=0$ (변곡점) 기준.
- **기술 준비도(TRL) ↔ 하이프 위상 매핑 테이블**:
  - TRL 1~3 = Innovation Trigger
  - TRL 4~5 = Peak
  - TRL 5~6 = Trough
  - TRL 6~8 = Slope
  - TRL 8~9 = Plateau
- **3-Tier Risk Weighting** (Phaal et al. 2004):
  $R_{total} = 0.5 \cdot R_{tech} + 0.3 \cdot R_{market} + 0.2 \cdot R_{regulatory}$
- **S-curve 도약 판정**: 현재 S-curve의 한계(Limit) 도달 시 다음 S-curve로의 이행을 "Discontinuity(불연속)"이라 정의, Christensen(1997)