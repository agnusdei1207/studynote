---
title: "3D Printing Additive Manufacturing Industry"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 723
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 적층 제조(Additive Manufacturing, AM)는 ISO/ASTM 52900 기준 7대 공정군(Vat Photopolymerization, Material Extrusion, Powder Bed Fusion, Material Jetting, Binder Jetting, Directed Energy Deposition, Sheet Lamination)으로 분류되며, **CAD -> Topology Optimization -> Slice(.cli/.gcode) -> PBF/DED 빌드 -> HIP/CNC 후가공 -> CT/CMM 인증**의 디지털-물리 통합 워크플로우가 핵심이다.
> 2. **가치**: GE LEAP 연료 노즐 사례처럼 기존 19개 조립 부품->1개 통합으로 **25% 경량화·수명 5배 향상**, 리드타임 **70~90% 단축**(주 단위->일 단위), **Buy-to-Fly 비율 20:1->3:1** 개선 등 물량·시간·자원의 비약적 효율을 창출한다. Wohlers Report 2023 기준 글로벌 AM 시장규모는 약 188억 USD(2022년), 연평균 18.3% 성장이 보고된다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **빌드 볼륨 vs 해상도(EOS M400-4: 400×400×400 mm / 100 μm vs ICON Vulcan: 11.5×4.5 m / 수 mm)**, **재료 선택(Ti-6Al-4V SLM 시 다공도 <0.1% 확보 vs Inconel 718 시 cracking 대응)**, **DfAM 성숙도(Topology Optimization + Lattice Gen + Multi-Object DO)**, **인-시튜 모니터링(Melt Pool IR, Layer Imaging) -> 인증(AS9100D, ISO 13485, KS B ISO/ASTM 52900)** 간의 균형점 설계가 실무자의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

적층 제조(Additive Manufacturing, AM)는 ISO/ASTM 52900:2021에서 "재료를 적층적으로 결합하여 3D 객체로 제조하는 과정"으로 정의되며, 전통적 절삭 가공(Subtractive Manufacturing, SM) 대비 **재료 낭비율 90% -> 5~10%**, **기하학적 자유도(내부 채널, 격자 구조, 위상 최적 형상)**, **공급망 단일화(파일 단일 운송)**의 세 가지 패러다임 전환을 제공한다. 4차 산업혁명의 핵심 스택(Digital Thread, PLM, MES, AI 공정제어)과의 결합으로 **Smart Factory**의 물리적 출력 단말로서 자리매김했다.

기존 SM/Casting/Forging 패러다임은 **공구 접근성(tool accessibility)**, **언더컷 한계**, **다품종 소량 생산 시 셋업비 급증**의 제약을 가졌다. 반면 AM은 STL/3MF/STEP-AMF 등 중립 데이터 포맷과 7대 공정군의 조합으로 **Mass Customization**(예: 환자 맞춤형 임플란트, 치아 크라운), **버추얼 인벤토리**(Digital Inventory, Wärtsilä 사례: 예비품 1,200종 디스크 저장), **로컬 제조(Distributed Manufacturing)**를 가능케 한다.

그러나 AM의 산업적 확산을 제약하는 **3대 페인포인트**는 (1) **속도·빌드 볼륨 한계**(단일 PBF 금속기 평균 증착 속도 5~20 cm³/h), (2) **결함·인증 리스크**(L-PBF Inconel 718의 cracking, 잔류응력 200~600 MPa), (3) **표면 조도(Ra 5~20 μm) 및 후가공 의존도**이며, 이를 해결하기 위한 **Hybrid Manufacturing(AM+CNC 한 베드)**과 **Multi-Laser/12-Laser 시스템**, **AI 기반 Melt Pool 모니터링**이 2020년대의 핵심 기술 흐름이 되었다.

```text
            적층 제조 산업 적용 패러다임 비교 (구 패러다임 vs 신 패러다임)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[구 패러다임: 절삭/주조/단조]                      [신 패러다임: 적층 제조]
━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━       ━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━
              |                                       |
   원자재 ---> 절삭(Material Loss 80~95%)        원자재 ---> 적층(Material Loss 5~10%)
              |                                       |
   CAD -> CAM -> CNC                          CAD -> DfAM(Topology Opt) -> Slice -> PBF
              |                                       |
   공구 접근성 제약                          내부 채널/오버행 자유
   (Undercut -)                            (Lattice/Inner Channel +)
              |                                       |
   금형비 1억~수십억                          금형비 0(파일 단일)
   변경 리드타임 3~12개월                     변경 리드타임 1~3일
              |                                       |
   대량생산 친화                             다품종·소량·맞춤형 친화
              |                                       |
   Buy-to-Fly 10:1~20:1                     Buy-to-Fly 1:1~3:1
              |