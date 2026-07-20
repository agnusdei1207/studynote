---
title: "Space Technology NewSpace Launch Satellite"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 727
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 뉴스페이스(우주 기술 뉴스페이스 발사체 위성)는 정부·대형기관 주도의 1회성 대형 발사체(Expendable Launch Vehicle)·중대형 GEO 정지위성 위주의 전통 우주산업 패러다임을, **민간 자본·반복사용(Reusability)·소형위성 군집(Constellation)·전기추진(EP)·위성버스 표준화·C2(Command & Control) 지상 클라우드화**로 전환하는 글로벌 흐름이다. SpaceX Falcon 9 1단 재사용, Rocket Lab Electron, Relativity Space Stargate 3D프린팅 엔진, Planet Labs Dove·SpaceX Starlink·Kuiper·OneWeb 등이 그 기술·사업적 상징이다.
> 2. **가치**: 발사단가가 kg당 20,000~100,000 USD(Falcon Heavy 1회 97M USD로 약 24,000 USD/kg)에서 **Falcon 9 재사용 시 약 2,500~3,000 USD/kg**, Starship 목표는 **<100 USD/kg**으로 떨어지며, 위성 개발기간은 5~8년에서 **CubeSat 기준 12~24개월**, SWaP-C(Size, Weight, Power, Cost) 최적화로 임무비용이 **1/10~1/100** 수준으로 축소된다. 2023년 기준 글로벌 우주경제 규모는 약 546억 USD에서 2035년 약 **1.8조 USD**(뱅크오브아메리카 전망)로 성장 가능성이 보고되며, 데이터·통신·항법·관측 융합의 진입장벽을 급격히 낮추고 있다.
> 3. **판단 포인트**: 실무 관점의 핵심 판단 축은 ①**궤도-주파수-ITU 등록 선점**(Ku/Ka LEO·V-band), ②**단독위성 대비 군집 운용 아키텍처**(ISL, 위상배치, 궤도유지 ΔV 산정), ③**COTS/상용부품 vs 우주급(Class S/A/K) 신뢰성 trade-off**(TID, SEE, SEL/SEU 허용치), ④**발사체-위성-지상-서비스 SLA**(데이터 latency, revisit time), ⑤**우주교통관리(STM)·잔해·재진입·스펀지 위험**(FCC 5년 규칙, IADC 가이드라인, 한국 우주안전법 2023)이다. 잘못된 트레이드오프는 군집 위성 간 충돌(Kessler Syndrome), 주파수 분쟁, 발사슬롯 회수 실패로 직결된다.

---

## Ⅰ. 개요 및 필요성

전통적 우주산업은 1960년대 아폴로 시대 이후 60여 년간 **①조달 주체가 정부(DoD, NASA, ESA, JAXA, KARI)**이고, ②**계약 구조가 Cost-Plus** 기반이며, ③**대형 단품 위성(통신·방송용 GEO 4~6톤, 정찰용 1~3톤)**, ④**1회성 발사체(Delta IV Heavy, Ariane 5, Atlas V)** 중심이었다. 결과적으로 kg당 발사비가 2만 USD 이상이었고, 위성 1기 개발에 5~10년·수천억 원이 투입되었다. 또한 지상국은 전 세계 10여 개의 Deep Space Network·TDRS와 같은 대형 인프라로 국한되어 민간 접근이 어려웠다.

**뉴스페이스(NewSpace)** 란 용어는 2000년대 후반 NASA Ames의 Rick Tumlinson가 SpaceX·Bigelow Aerospace 등과의 협업에서 처음 사용한 후, 민간 우주자본 흐름(2010~2024년 누적 1,000억 USD 이상 VC 투자)을 상징하는 용어로 정착했다. 기술적 배경에는 ①**CubeSat 표준(1999년 Stanford·Cal Poly, 1U 10×10×10 cm, 1.33 kg)**의 등장과 ②**COTS(Commercial Off-The-Shelf) 정책**(NASA 2006), ③**Moore's Law 기반 반도체·배터리·MEMS 관성센서·CMOS/IR FPA 가격 하락**, ④**ITU의 2019년 신규 LEO 군집 주파수 할당(7,000기 이상 분배)**, ⑤**SpaceX Falcon 9 1단 재사용(2015, 2017 재사용 비행)·Starlink 킥스테이지(2019~)·수직착륙 비행 300회 이상**이라는 4대 돌파가 있었다.

한국 역시 2022년 6월 21일 **한국형 발사체 누리호(KSLV-2, 200t, 1.5t LEO)** 2차 발사 성공으로 자력 발사 능력을 확보했고, 2023년 12월 누리호 3차 발사(실용위성 8기 탑재를 위한 우주검증), KSLV-3(2026년~ LEO 10t), **차세대 중형 발사체(2030년대 LEO 50t급)** 로드맵, **한화(창성 3호 2025~)**, **CONTEC(다목적실용위성 7호 2024 발사)**, **인스페이스(한누리 2022년 1단 재사용 비행 시험)**, **페리지에어로스페이스(블루오리진 1호 2023)**, **AP위성(초소형 SAR 군집)** 등 민자 뉴스페이스 생태계가 본격 형성되었다.

```text
[전통 우주 가치사슬 vs 뉴스페이스 가치사슬]

   [전통(Old Space) 패러다임]                  [뉴스페이스(NewSpace) 패러다임]
  +----------------------+               +--------------------------+
  | ①정부 발주 (Cost-Plus) |                | ①민간 VC/SPAC 직접 조달   |
  | ②1회성 대형 발사체       |                | ②반복사용 + 소형 발사체    |
  | ③중대형 단품 위성(5~6t) |                | ③소형 위성 군집(Starlink) |
  | ④전용 Deep-Space급 관제 |                | ④클라우드 관제(Kongsberg, |
  |   지상국(소수)            |                |   KSAT, Leaf Space, AWS) |
  | ⑤10~20년 임무 주기       |                | ⑤3~7년 교체형 임무       |
  +----------------------+               +--------------------------+
         |                                          |
         v                                          v
   임무 비용: $1B+/기                    임무 비용: $1M~$10M/기
   발사 단가: $20K+/kg                  발사 단가: $1K~3K/kg (Starship< $100)
   개발 주기: 5~8년                      개발 주기: 12~24개월 (CubeSat)
```

**왜 필요한가?**
- **데이터 폭증**: SAR(합성개구레이더), RGB/Multispectral/Hyperspectral 영상이 매일 24/7 글로벌 커버리지로 전환되면서 정부·보험·재난·금융·환경·국방으로 시장이 확장되고 있다.
- **대역폭·연결성 평준화**: LEO 군집 위성통신은 GEO HTS(High Throughput Satellite)의 latency 600ms를 20~40ms로 줄여 IoT·자율주행·원격진료·드론제어의 글로벌 연속성을 가능하게 한다.
- **기술민주화**: CubeSat·상용부품·오픈소스 지상(예: OpenC3 COSMOS, Kratos OpenSpace)·클라우드(Ground Station As A Service, AWS Ground Station·Azure Orbital)로 대학·중견기업·개인이 위성을 만들 수 있다.
- **안보·국방 다변화**: 우주군(Space Force), 카운터스페이스(Counter-Space), MEO-PNT(GPS-III, Galileo, KPS 2035), 우주감시(SDA Tracking Layer Tranche 0/1) 수요 폭증.
- **그린·친환경**: 재사용, 메탄-LOX(SpaceX Raptor, Blue Origin BE-4), 전기추진(Hall-thruster, ION-Xenon), 비가연소 페어링로 그린 발사 추진.

- **📢 섹션 요약 비유**: 뉴스페이스는 "버스 한 대로 손님 5명만 데리고 다니던 시대(아폴로·GEO 대위성)에서, U-Bike·U-Car 수백 대가 도시 전역을 누비는 모빌리티 전환(우주 공유경제)과 같다. 도로(궤도)와 신호등(주파수·STM) 설계가 곧 국가 경쟁력이다."

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 발사체(Launch Vehicle) 아키텍처

소형/중형 발사체는 통상 **다단 로켓(Multi-Stage)** 구조로, 1단/2단의 **공정탐색·분리·점화·유도로(Sequence)**가 핵심이다. 뉴스페이스 발사체의 대표 구분은 다음과 같다.

| 구분 | 대표 | LEO 능력 | 재사용 | 추진제 | 특이사항 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 소형(SSL) | Rocket Lab Electron | 300 kg | 1단 일부(재사용 실험 중) | RP-1/LOX | 페어링 전자장비 항공우주등급 |
| 중형(SL) | SpaceX Falcon 9 | 22.8 t | 1단 수직착륙·재사용 20+회 | RP-1/LOX Merlin 1D | 9+ Merlin 진공/해양 추력 |
| 중대형 | Falcon Heavy | 63.8 t | 2×1단 그리드핀 | RP-1/LOX | 27 Merlin, 사이드 부스터 동시 착륙 |
| 차세대 | SpaceX Starship | 100~150 t | 완전재사용(S+SuperHeavy) | CH4/LOX Raptor 2/3 | 33 Raptor 2 (200t 추력) |
| 한국 KSLV-2 | 누리호 | 1.5 t | 1단 액체(75톤), 고체부스터 | KRE-075 LOX/Kerosene | 4×75톤 1단 + 고체 P-Δ |
| 한국 KSLV-3 | 차세대중형 | 10 t+ | 1단 재사용 검토 | LOX/Kero/CH4 | 2030~ |

```text
[뉴스페이스 발사체 일반 아키텍처(다단 로켓)]

  +----------------------+
  | 페어링(Fairing)        | <- 탄소/알루미늄 허니콤, 5m~9m 직경, 13~22m 길이
  | +------------------+ | <- ② 탑재 인터페이스(ESPA Ring, 24in, Lightband)
  | | 위성(Satellite)   | | <- ① 분리시 충격<1500g, 분리 spin 0~5rpm
  | +------------------+ |
  +----------------------+
  | 2단 (Vacuum Engine)    | <- 진공비추력 Is·300~380s, 비추력 최적화 노즐
  | +------------------+ | <- ③ 분리(2단-1단 hot/cold separation)
  | |  추력기관 (1~2기)  | | <- gimbal ±8° TVC, ④ RCS(질소/하이드라진)
  | +------------------+ |
  +----------------------+ <- ⑤ 단분리(S-IC/S-II Pneumatic Push)
  | 1단 (Main Engine)     | <- 슬래싱(Max-Q)·Pitch Program
  |  +----------------+ |
  |  | 클러스터 엔진(3~9) | | <- Merlin 1D(845kN), Raptor 2(2,256kN),
  |  +----------------+ |   Rutherford(미국 NZ 25kN), KRE-075(75톤)
  | +------------------+ |
  | | 추진제 탱크(LOX/RP)| | <- ⑥ TPS(단열), ⑦ 헬륨 가압(2024 NASA helium)
  | +------------------+ |
  +----------------------+
       v
  [지면/착륙선] <- 그리드핀, ⑧ 착륙다리(deployable), ⑨ ASDS
```

### 2) 위성(Satellite) 아키텍처 - 위성버스 + 탑재체

뉴스페이스 위성은 ①버스(플랫폼) + ②탑재체(Payload)로 모듈화된다. CubeSat 표준(1U/3U/6U/12U, 27U 확장)을 기반으로 하며, 100~500 kg급 ESPAClass 위성이 2020년 이후 사실상 **Facto-Standard**가 되었다(OneWeb, Starlink v2-mini 800kg, Capella, ICEYE 100kg SAR).

| 구성 요소(버스) | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **구조/열제어(Structure & TCS)** | 진동·열환경 보호, 전개 | 알루미늄 허니콤·CFRP 스킨, 능동/수동 TCS(MLI, OSR, 히터, 라디에이터); 위성 외부 -180~+150°C, 내부 -30~+50°C |
| **전력(EPS, Power)** | 생성·저장·분배 | 트리플정션 GaAs/삼중접합 GaInP/GaAs/Ge(30%+ 효율, BOL), Li-ion(NMC, LTO), MPPT, PCU 28V/100V, 2.0kW-12kW |
| **추진(Propulsion)** | 궤도삽입·유지·드래그 컴펜,