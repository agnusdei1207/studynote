---
title: "TDP, Thermal Design Power"
date: "2026-05-09"
tags:
  - "studynote-computer-architecture"
weight: 472
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TDP(Thermal Design Power)는 CPU/GPU/SoC가 정상 동작 시 발생하는 최대 열량(Watt)을 정의하는 **냉각 시스템 설계 기준치**이며, Intel 12세대부터는 PBP(Processor Base Power), MTP(Maximum Turbo Power)로 분리되어 PL1/PL2/PL3의 3단계 전력 제한 체계로 진화하고 있다.
> 2. **가치**: 정확한 TDP 산출은 냉각 솔루션 비용(공랭 -> 수랭 -> 2-phase/침적 냉각 등)과 시스템 신뢰성(MTBF, 50℃ 규칙)·전력 인프라(PSU 용량, 배전)·운영비(PUE, kW/h)를 동시에 최적화하며, 서버 1 rack당 약 30~70kW, AI 가속기 랙은 100kW 이상의 발열 밀도 설계로 데이터센터 CAPEX/OPEX를 좌우한다.
> 3. **판단 포인트**: TDP ≠ 실제 소비전력이며, 워크로드 특성(SPECpower ssj_ops/Watt, AVX 오프셋, sustained vs burst)에 따라 동일 TDP 등급 CPU라 해도 실질 발열이 1.2~2배 차이 발생, 따라서 **냉각 설계 시 TDP×Derating(1.3~1.5배) + Margin**을 적용하고, cTDP(±수 W), Tjmax(100~110℃), Rja/Rjc 열저항을 종합적으로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

CPU·GPU·NPU·AP 등 반도체 칩이 고집적·고주파로 진화함에 따라, 단위 면적당 발열(Heat Flux, W/cm^)이 폭증하고 있다. 2000년대 초 Pentium 4(115W, 0.18μm) 대비 2024년 Apple M3 Max(78W, 3nm), Intel Core i9-14900KS(150W PBP / 253W MTP, Intel 7), AMD Ryzen 9 7950X(170W cTDP, 5nm), NVIDIA H100 SXM(700W TDP, 4N)은 같은 footprint에서 약 6~10배의 전력을 소모한다. 이로 인해 패키지 레벨 열유속(Heat Flux)이 100 W/cm^을 초과하면서 전통적인 공랭 히트싱크의 한계(Boundary Layer 저항)에 도달했다.

TDP는 **'시스템 냉각 설계자가 반드시 확보해야 할 최소 열방출 용량'**이라는 의미로, 칩 제조사가 보증하는 '정상 부하 워크로드가 무한 지속(SPEC Power, TPC, LINPACK 류)될 때 방출해야 할 평균 열량'이다. 그러나 TDP는 실소비전력의 상한이 아니며, **과도 상태(Transient), 부스트(Turbo Boost 3.0, Thermal Velocity Boost), AVX-512/AMX 같은 SIMD 가속 명령 실행 시에는 PL2/PL3 단계에서 TDP를 1.5~2배 초과**한다. 따라서 시스템 설계자는 TDP를 기준으로 하되, 워크로드 비율(Tau_ms, 동적 행태)과 전장 환경(JEDEC JESD51 정의)을 종합 고려해야 한다.

```text
[반도체 칩 발열 진화 및 냉각 패러다임 변화]

   1990s                 2000s                 2010s                 2020s+
   +------+             +------+             +------+             +------+
   |P-III |             |P-4   |             |Xeon  |             |H100  |
   |~30W  |-- 4x ----->  |115W  |-- 3x ----->  |165W  |-- 4x ----->  |700W  |
   |Al히트|             |Cu+Fan|             |Heat- |             |Direct|
   |싱크  |             |      |             |pipe  |             |Liquid|
   +------+             +------+             +------+             +------+
   열유속<10 W/cm^     10~30 W/cm^         30~60 W/cm^         60~150+ W/cm^
                                                                   ^
                                                       Vapor Chamber/2-Phase/Immersion
   +-------------------------------------------------------------------------+
   | 냉각 방식의 임계점:                                                  |
   |  • 히트싱크만으로 1kW+ 방열 물리적 불가                              |
   |  • PUE 1.5 -> 1.1 (액침/DLC) 요구                                    |
   |  • 랙 전력밀도: 5kW(2010) -> 40kW(2020) -> 130kW+(2024, GB200 NVL72)|
   +-------------------------------------------------------------------------+
```

기존에는 'CPU TDP = 시스템 최대 전력'이라는 단순 등식이 통용되었지만, 다중 가속기(SoC + dGPU + NPU), 빅리틀 아키텍처(A78 + A55, P-core + E-core), HBM/Power Via 등의 패키징 혁신으로 **TDP 개념 자체가 다중화(PBP+MTP+PL1/2/3)·동적화(RAPL, DVFS, Power Gating)** 되었다. 결과적으로 시스템 엔지니어는 칩의 정적 데이터시트만으로는 냉각 설계를 완료할 수 없으며, **VR(Voltage Regulator), TIM(Thermal Interface Material), IHS(Integrated Heat Spreader), Heat Sink, Fan Curve, PSU Rail, Data Center Cooling(XDCDLC, Rear Door, Immersion Tank)까지 통합적으로 설계**해야 한다.

- **📢 섹션 요약 비유**: TDP는 자동차의 '공식 연비'와 같다. 실제 도로·적재하중·에어컨 사용에 따라 30% 이상 차이 나듯, CPU TDP는 '이상 조건' 기준이므로 **운전 습관(워크로드)에 따라 실제 발열이 크게 달라진다**.

---

## Ⅱ. 아키텍처 및 핵심 원리

TDP는 칩 내부의 **전력 모델(Power Model)** P = C·V^·f + V·I_short + P_static 으로부터 도출되며, 이를 패키지/보드/시스템의 **열저항 네트워크(Foster/Cauer Network)**로 환산하여 냉각 시스템 사양을 결정한다.

핵심 식: **Tj = Ta + (P_static + P_dynamic) × Θja** = Ta + P_total × Θja

- Tj: Junction Temperature (Junction to Die 내부 측정점)
- Ta: Ambient Temperature (시스템 흡입 공기)
- Θja: Junction-to-Ambient Thermal Resistance (℃/W)
- Θjc: Junction-to-Case (히트싱크 설계 시 핵심)

TDP는 **TDP = (Tj_max − Ta_max) / Θja** 형태로 정의되며, 보통 Ta_max=35~45℃, Tj_max=100~110℃ 범위에서 결정된다. 예를 들어 Tj_max=100℃, Ta=45℃, Θja=0.36℃/W 라면 TDP = 152W 가 산출된다.

```text
[칩 -> 시스템 열 흐름 및 전력 단계 (Intel 12세대+ 기준)]

                  +-------------------------------------+
                  |      CPU Package (LGA1700/LGA4677)   |
                  |  +-----------------------------+    |
   PL3 (Peak) ---> |  |  MTP 253W ---> PL2 253W ---> |    | <--- 10ms 이하 Burst
                  |  |   (^1회성)  (^28s 지속)   |    |
   PL2 (Turbo)---> |  |            PL1 150W(기본)  |    | <--- 무한 지속 가능
   PL1 (Base) ---> |  +-----------------------------+    |
                  |           |   ^   ^   ^              |
                  |           |   |   |   |              |
                  +-----------+---+---+---+--------------+
                              |   |   |   +- TDP/PBP(공식 발표치)
                              |   |   +----- cTDP(Down/Up 구성 가능)
                              |   +---------- RAPL(MSR 0x610) 실시간 측정
                              +------------ TJmax(100~110℃, PROCHOT#)
                                          v
                       +------------------------------------+
                       |  Thermal Resistance Path           |
                       |  Θjc(die->IHS) 0.05~0.1℃/W          |
                       |  Θcs(IHS->TIM) 0.01~0.05℃/W         |
                       |  Θsa(TIM->Heatsink) 0.05~0.2℃/W     |
                       |  Θsa(Heatsink->Air) 0.1~0.5℃/W      |
                       +------------------------------------+
                                          v
                       +------------------------------------+
                       |  Cooling Solution Sizing           |
                       |  Q = ṁ·Cp·ΔT = CFM × ΔT × 1.08    |
                       |  P(TDP) = Q -> Fan/Heatsink/Radiator|
                       +------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **PBP (Processor Base Power)** | Intel 12세대+ 이전 TDP 대체 지표 | 이전 TDP와 같은 개념의 평균 열량, 무한 워크로드 시 냉각 기준 |
| **MTP (Maximum Turbo Power)** | 부스트 모드 단기 피크 전력 | PL2(28s)/PL3(10ms) 합산, Turbo Boost 3.0/TVB 작동 시 도달, MTP는 IccMax와 관련 |
| **PL1/PL2/PL3 (Power Limits)** | 시스템 3단계 전력 제한 | PL1=PBP, PL2=MTP(28s), PL3=Transient Peak. MSR 0x610(RAPL)·0x618(PL3)·0x101A(PL4) |
| **cTDP (Configurable TDP)** | OEM이 BIOS로 TDP 변경 허용 | Down/Up 모드(예: i7-1280P 28W↔64W), 서버/노트북 OEM 라인업 차등화 |
| **RAPL (Running Average Power Limit)** | 런타임 전력 모니터링/제한 | Sandy Bridge부터 도입, MSR/PCIe 기반, OS-level(turbostat, powercap) 노출 |
| **PROCHOT# / THERTRIP#** | 온도 임계 핀 | Tj>PROCHOT 시 CLK throttling, Tj>THERTRIP(125℃) 시 즉시 shutdown |
| **Tj_max / Junction 온도** | 다이 실측 한계 | Intel 100~110℃, AMD 95~115℃, ARM Cortex-X 105℃. DTM(Dynamic Temp Monitoring) |
| **Θja / Θjc** | 열저항 (JEDEC JESD51 정의) | 1D/2D/3D 모델, Θja=Θjc+Θcs+Θsa, PCB Copper/8-layer로 Θja 20%v |
| **DVFS + Power Gating** | 동적 전압/주파수 + 유휴블록 차단 | P-state (P0~Pn), C-state (C0~C10), S0ix/Modern Standby. 100mW 이하 유휴 |
| **Turbo Boost / Precision Boost** | 순간적 성능-전력 트레이드오프 | IccMax·TDP·전력여유·온도여유 4개 축 동시 만족 시 부스트 |

**주요 정량 지표**:
- Intel 13세대 i9-13900K: PBP 125W, MTP 253W, Tjmax 100℃, cTDP Down 125W
- AMD Ryzen 9 7950X: TDP 170W, PPT 230W, Tjmax 95℃, cTDP 105~170W
- AMD EPYC 9654: TDP 360W, cTDP 320~400W, Socket SP5, 12-channel DDR5
- NVIDIA H100 SXM5: TDP 700W, cTDP 600~700W, HBM3 80GB, NVLink 900GB/s
- Apple M3 Max: Package Power ~78W (PBP 30W 추정), 92GB/s 메모리 대역폭
- Ampere Altra Max: TDP 128W (실측 60~80W), 128코어 ARM, 클라우드 네이티브

- **📢 섹션 요약 비유**: PL1/PL2/PL3는 자동차의 '정속 순항 / 5초 추월 / 시동 순간 부스트'와 같다. 차가 항상 최고속으로 달리면 냉각이 터지듯, CPU도 PL2/PL3는 순간의 힘을 의미하며, **지속 가능한 힘은 PL1(=PBP/TDP)** 이다.

---

## Ⅲ. 비교 및 연결

TDP는 동일 칩셋 내에서도 라인업별, 세대별로 의미가 달라지며, 유사 개념들(Power, TDP, PBP, cTDP, RAPL, C-state)과 명확히 구분되어야 한다.

| 구분 | TDP (구세대) | PBP/MTP (Intel 12세대+) | cTDP | RAPL | Tjmax |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **정의 시점** | 출시 시 고정 | 출시 시 PBP+MTP 동시 공개 | OEM BIOS 설정 가능 | 런타임 동적 | 칩 설계 시 결정 |
| **측정 방식** | 합성 벤치 평균 | 무한 워크로드/버스트 피크 | OEM/실리콘 검증 | MSR 0x610 카운터 | 내부 다이에센서 |
| **지속 시간** | 무한대 | PBP=무한, MTP~28s | 무한대 | 1ms~1s 윈도우 | N/A |
| **활용 계층** | 시스템 냉각 | 시스템 + VR 설계 | 라인업 차등 | OS/하이퍼바이저 | PROCHOT |
| **값 예시** | i9-9900K=95W | i9-13900K: PBP 125W, MTP 253W | i7-1280P 28W↔64W | Package 150W 측정 | 100~110℃ |
| **의사결정 권한** | Intel/AMD 정책 | Intel 정책 (마케팅 표시 통일) | OEM BIOS Lock 가능 | OS가 직접 설정 | 칩 자체 |

**관련 시스템 계층 통합**:
- **VR(Voltage Regulator)**: TDP=150W라면 Vcore 1.2V × 125A = 150W, 8-phase VRM with 90A Smart Power Stage(예: Renesas ISL99227), 80% 효율 -> 187W 입력 -> 12V 레일
- **PSU sizing**: CPU TDP + GPU TDP + 보조 + 30% Margin. RTX 4090(450W)+i9(253W)+Mobo(50W) -> 1000W PSU 권장
- **Data Center**: 40kW/랙 기준 TDP 700W GPU 56장. Immersion(0.07 PUE) vs DLC(1.05) vs 공랭(1.5) 선택
- **AI/HPC**: NVIDIA GB200 NVL72 = 72 GPU × TDP 1000W(Blackwell) = 72kW GPU only, 130kW/rack -> **냉각=시스템 bottleneck**
- **Regulation**: EU Lot 9 (2019) 서버 효율, ENERGY STAR 4.0, ErP Lot 9, California Title 24

- **📢 섹션 요약 비유**: TDP는 집의 '공급 면적'으로, PBP는 항상 거주하는 공간, MTP는 친구가 놀러와 쑥쑥 쓰는 거실, cTDP는 이사 후 리모델링으로 면적을 더 키우는 옵
