---
title: "Carbon Capture CCS CCUS Net Zero Strategy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 726
---
# 726. 탄소 포집 CCS / CCUS / 넷제로 전략 (Carbon Capture CCS CCUS Net Zero Strategy)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CCS는 산업배출원·대기 중 CO₂를 **분리(Separation) -> 압축(Compression) -> 수송(Transport) -> 지중저장(Geological Storage)**의 4단 공정으로 격리하는 기술이며, CCUS는 여기에 EOR·화학원료·광물화·합성연료 등 **Utilization(활용)** 경로를 결합해 탄소를 순환시키는 폐쇄루프 시스템이다.
> 2. **가치**: IEA *Net Zero by 2050* 시나리오에서 CCUS는 **누적 약 6Gt CO₂/yr** 감축을 담당(전체 감축의 15%), 시멘트·철강·석유화학·시멘트·해운 등 **hard-to-abate 섹터**(전력·산업 전환만으로는 감축 불가한 영역)의 사실상 유일한 decarbonization path로 작동한다.
> 3. **판단 포인트**: (a) **포집 방식** — 화학흡수(amine)/막분리/MOF·PSA/DAC(Direct Air Capture) 간 LCOA(Levelized Cost of Avoided CO₂) trade-off, (b) **수송 모드** — 100km 미만은 truck·ship, 장거리 대용량은 pipeline(직경 16~48인치, 80~150bar), (c) **저장 매체** — 咸水層/고갈유전/ECBM/탄산염암(반응성 광물화) 간 영구 격리 안전성·MRV(Measurement, Reporting, Verification)·누출 리스크, (d) **활용 가치사슬** — EOR(단기 cash-flow) -> CCU(중기) -> 광물화(장기 영구성).

---

## Ⅰ. 개요 및 필요성

### 1) 등장 배경 — 1.5℃ 시나리오와 Hard-to-Abate 섹터
2015년 파리협정 이후 IPCC AR6는 1.5℃ 목표를 위해 **2030년 43% 감축(2019 대비), 2050년 Net Zero**를 요구한다. 그러나 글로벌 CO₂ 배출의 약 **24%**는 **산업 공정(process emission)**에서 발생하며, 이는 연소를 멈춰도 라임·시멘트·철강 환원제 등 화학적으로 고정되어 발생하는 **"inevitable emission"**이다. 시멘트(clinker kiln)·철강(blast furnace)·에틸렌(steam cracker)·암모니아(grey H₂)·해운·항공은 신재생 전력·전기로 전환만으로는 감축이 불가능한 영역이며, IEA는 이 섹터에서 CCS/CCUS 비중을 **2050년 약 50% 이상**으로 전망한다.

### 2) 왜 CCS인가 — 음배출(Negative Emission)의 필요성
재생에너지·전기화·수소 전환만으로는 잔여배출(residual emission)이 발생하며, 이를 상쇄하려면 **CDR(Carbon Dioxide Removal)**이 필수다. CDR은 (a) **자연기반** — 산림·습지·토양(BNF: Biochar with CCS 가능)·해양, (b) **공학기반** — DAC·BECCS·광물화(Olivine weathering)·해양알칼리도(OA)로 분류된다. 그중 BECCS·DAC는 **CCUS와 결합될 때에만** 영구적·검증 가능한 음배출이 가능하다.

### 3) 산업 패러다임의 전환 — "배출 후 처리"에서 "탄소 순환"으로
| 구분 | 기존 패러다임 (Fossil Linear) | 신규 패러다임 (CCUS Circular) |
| :--- | :--- | :--- |
| 탄소 흐름 | 채굴 -> 연소 -> 대기배출 (one-way) | 채굴·대기·배출 -> 포집 -> 활용·저장 (loop) |
| KPI | 단가(원/kWh, 원/ton) | **LCOA(원/ton CO₂eq avoided)**, CCUS Intensity |
| 자산 | 화력·정유 단일 | 포집 플랜트 + 수송 + 클러스터 + 저장 허브 |
| 정책 | RPS·REC·에너지 효율 | **ETS(carbon price $80-200/t) + CBAM + 45Q 세액공제 + CDR 인증** |

### 4) 한국의 정책 프레임
- **2020.10** 2050 탄소중립 선언
- **2021.09** 탄소중립·녹색성장 기본법 제정(2022.3 시행)
- **2023.10** 제1차 국가결정기여(NDC) 갱신 — **2030년 2018년 대비 40% 감축**(이전 26.3%)
- **2025.01** K-ETS 3기(2026-2030) 출범 — 배출권 가격 8~15만 원/吨
- **2027+** EU **CBAM 본격 시행**(2026말까지 전환기) — 철강·시멘트·알루미늄·비료·전력·수소에 **CO₂ 배출량 기반 관세** 부과 -> 한국 수출기업은 **자체 감축 또는 CBAM 인증서 구매** 압박

### 5) CCS/CCUS 핵심 개념 흐름도

```text
                  +--------------------------------------------------+
                  |           CCS / CCUS 4-Stage Process Flow        |
                  |           (Capture -> Compress -> Transport -> Use/Store) |
                  +--------------------------------------------------+

   +------------------+    +------------------+    +------------------+    +------------------+
   |  ① CAPTURE       |    | ② COMPRESSION    |    | ③ TRANSPORT      |    | ④ USE / STORE    |
   |  (분리·포집)      |---->|  (압축·건조)      |---->|  (수송)           |---->|  (활용·저장)      |
   |  85–95% recovery |    |  80–150 bar      |    |  pipeline/ship   |    |  Class VI well   |
   |  0.04–0.06 MPa   |    |  -30℃ dehyd.    |    |  100–1000+ km    |    |  >800m depth     |
   +------------------+    +------------------+    +------------------+    +------------------+
           |                       |                       |                       |
           v                       v                       v                       v
   Post / Pre / Oxy-fuel      Multi-stage        Onshore pipeline (gas)    EOR (단기)
   DAC (Climeworks,           Compressor         Ship (LCO₂ 7,000-30,000m³)  盐水層(Sleipner) - 영구
   Carbon Eng.)              + Dehyd unit        Truck (소규모 분산)         광물화(반응성 basalt)
   BECCS                      + Impurity          Tanker truck  -196℃        ECBM
```

- **📢 섹션 요약 비유**: CCS는 화석연료 산업의 **"인공 신장(Kidney Dialysis)"**이다. 몸(산업)이 정상적으로 활동(연소·생산)하면서 배출되는 노폐물(CO₂)을 별도의 외부 장치가 걸러내 깨끗한 혈액(대기) 중으로 돌려보내되, 걸러진 노폐물은 안전한 저장고(지중)에 격리한다. CCUS는 신장 투석에 더해 걸러진 노폐물을 재활용(투석수 비료화)까지 하는 **"투석 + 자원화 통합 시스템"**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 4단계 아키텍처 상세

```text
  +----------------------------------------------------------------------------+
  |                      CCS/CCUS Value Chain Architecture                    |
  +----------------------------------------------------------------------------+

  [1] CAPTURE PLANT                [2] COMPRESSION & DEHYDRATION
  +--------------+                 +------------------+
  | Flue gas      |---> Absorber --->| Multi-stage Comp |---> CO₂ stream
  |  (3-15% CO₂)  |   MEA 30wt%   |  1bar -> 80-150bar|    (≥95% purity)
  |  50-150℃      |   Stripper    |  + Dehydration   |    <50 ppm H₂O
  |  SOx/NOx/PM   |   100-120℃   |  + SOx/NOx scrub |
  +--------------+   0.2 MPa     +------------------+
        |                    |
        |                    +-- Reboiler duty 3.0-4.0 GJ/ton CO₂ (energy penalty)
        |                         (신재생 폐열 활용 시 1.5-2.0 GJ/ton)
        |
        +-- Alternative paths:
        |   • Membrane: Polyimide/ZIF-8 hollow fiber, ΔP 30 bar, >90% purity
        |   • Adsorption: Zeolite 13X, VSA cycle, dry flue gas 한정
        |   • Cryogenic: Dual-pressure distillation, 고농도(>50%) 적용
        |   • Chemical Looping: CuO/C