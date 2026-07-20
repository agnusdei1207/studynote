---
title: "Collaborative Robot Cobot Human Interaction"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 736
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 협동로봇(Cobot)은 ISO/TS 15066의 4가지 협동운전 모드(SRMS·SSM·HG·PFL)와 충돌방지센서(토크·비전·스킨)를 통해 산업용로봇 대비 약 1/10 수준의 안전정지거리(STO < 1ms 응답)와 250mm/s 이하의 협업속도 제약을 만족하면서 인간과 동일 작업공간을 공유하는 로봇이다.
> 2. **가치**: 펜데믹 이후 도입기업의 73%(IFR 2023 통계)에서 ROI 회수기간 12개월 이내를 달성하며, 작업자 근골격계 질환(MSD) 30~50% 감소 및 소량다품종(Small-Batch High-Mix) 생산라인 전환시간 70% 단축이라는 정량적 가치를 제공한다.
> 3. **판단 포인트**: 가변임피던스 제어(Variable Impedance Control)와 인간 의도추론(Intent Inference, RNN/LSTM 기반)의 정확도·안전성·응답성 트레이드오프, 그리고 ROS 2 + OPC UA 기반의 실시간 결정론적 통신(< 1ms 지터)과 IEC 61508 SIL 3 인증 여부, 페일세이프 아키텍처 설계가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 산업용로봇은 ISO 10218-1/2에 따라 2m/s 이상的高速으로 동작하며, 가드 울타리(Safety Fence)·안전 라이트 커튼·인터록 도어를 통한 물리적 격리가 필수였다. 그러나 스마트팩토리·SoC(System on Chip)·저출산·고령화에 따른 노동력 감소, 그리고 4차 산업혁명时代的 개별화·맞춤형 생산 요구로 인해 인간과 동일 작업공간을 공유하는 **협동로봇(Collaborative Robot, Cobot)**의 필요성이 대두되었다.

```text
[전통적 산업로봇 vs 협동로봇 작업공간 개념도]

   (기존)              ----------►           (코봇)
   +------------------+                +----------------------+
   |   +-----------+  |  Guarded       |  +--------+   사람    |
   |   | 6축 산업용 |  |  Workspace     |  | 코봇  |<-->  HRI    |
   |   |   로봇     |  |   (위험구역)    |  | UR10e | 협업구역   |
   |   | FANUC R-2000| |                |  +--------+          |
   |   +-----------+  |  사람 진입불가   |  +--------------+    |
   |   ★ Safety Fence |                |  | Shared Cell  |    |
   |   ★ Light Curtain|  물리적 격리    |  | 250mm/s 이하  |    |
   |   ★ Interlock    |                |  | PFL ≤ 80W    |    |
   +------------------+                |  +--------------+    |
                                        +----------------------+
       고속 · 고하중 · 분리                  저속 · 안전 · 공유
       2,000×2,000×2,000mm                작업자와 500mm 이내 접근
```

**필요성의 핵심 동인**:
- **경제적 동인**: 전통 6축 산업로봇 도입비용 대비 30~50% 저렴(UR5e 기준 약 35,000 USD), 별도 안전펜스 구축비용 1,000만 원 절감
- **사회적 동인**: 제조업 인력 15년간 28% 감소(통계청), MSD(근골격계 질환) 산업재해의 60%가 단순반복작업에서 발생
- **기술적 동인**: ROS 2(Humble Hawksbill), OPC UA Companion Specification for Robotics, EtherCAT, RTOS(FreeRTOS, VxWorks) 성숙으로 실시간 안전제어 가능
- **규범적 동인**: ISO/TS 15066:2016 "Collaborative Robots" 기술규격 발표, 2024년 KOSHA GUIDE 로봇협동안전 가이드라인 개정

| 구분 | 전통적 산업로봇 | 협동로봇(Cobot) |
| :--- | :--- | :--- |
| 안전 방식 | 가드·인터록(물리적 격리) | 내장형 안전기능(SF) + 센서 기반 |
| 최대 TCP 속도 | 2~10 m/s | ≤ 250 mm/s (협업모드) |
| 정지 정밀도 | ±0.02~0.05mm | ±0.03~0.1mm |
| 도입 비용 | 1억~3억 원 (펜스 별도) | 5,000만~1억 원 (일체형) |
| ROI 회수 | 24~36개월 | 8~14개월 |
| 작업자 위치 | 분리(별도 셀) | 동일 작업공간(Shared Workspace) |

- **📢 섹션 요약 비유**: 전통 산업로봇이 "호랑이를 우리 안에 가두어 두는" 것이라면, 코봇은 "충분히 순화된 강아지에게 목줄과 행동교범(안전 알고리즘)을 달아 함께 걷게 하는" 것으로, 격리 대신 共生(공생)을 택한 패러다임 전환이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

협동로봇 시스템은 **인식(Perception) -> 인지(Cognition) -> 의사결정(Decision) -> 동작(Action)**의 4계층 아키텍처로 구성되며, IEC 61508 SIL 2~3 수준의 안전 무결성(Safety Integrity)이 요구된다.

```text
[코봇 HRI 시스템 아키텍처 및 안전제어 루프]

                +-----------------------------------------+
                |        Safety Layer (SIL 2/3)            |
                |  +----------+    +--------------+       |
                |  |Safety PLC|◄--►|STO/SBC/SOS   |       |
                |  |(SICK Flexi|   |Functional SF |       |
                |  | Soft)    |    +------+-------+       |
                |  +----+-----+           |               |
                |       | EtherCAT Safety (FSoE)          |
                +-------+---------------------------------+
                |  +----v--------------------------------+ |
                |  |   Real-Time Motion Control Layer    | |
                |  |   +---------+  +----------------+  | |
                |  |   | EtherCAT|  |Impedance/      |  | |
                |  |   | Master  |--|Admittance Ctrl |  | |
                |  |   |(1kHz)   |  |M = B·ẋ + K·x  |  | |
                |  |   +---------+  +----------------+  | |
                |  +----+--------------------------------+ |
                +-------+---------------------------------+
                |  +----v--------------------------------+ |
                |  |   Perception & Cognition Layer      | |
                |  |  +--------+ +--------+ +--------+  | |
                |  |  |RGB-D   | |Force/  | |Intent  |  | |
                |  |  |Camera  | |Torque  | |RNN     |  | |
                |  |  |Intel   | |Sensor  | |Predict |  | |
                |  |  |D455    | |ATI Mini| |LSTM    |  | |
                |  |  +--------+ +--------+ +--------+  | |
                |  |  +--------+ +--------+             | |
                |  |  |Skin    | |Mic     |             | |
                |  |  |Sensor  | |Array   |             | |
                |  |  |TakkStrip| |ReSpeaker|           | |
                |  |  +--------+ +--------+             | |
                |  +----+--------------------------------+ |
                +-------+---------------------------------+
                |  +----v--------------------------------+ |
                |  |   HRI Interface Layer (ROS 2 Humble) | |
                |  |  • MoveIt2 (Motion Planning)         | |
                |  |  • RViz2 (Visualization)             | |
                |  |  • BehaviorTree.CPP (Task Sequencer) | |
                |  |  • OpenHRI (Speech/Gesture)          | |
                |  |  • OPC UA (MES/ERP 연동)             | |
                |  +--------------------------------------+ |
                +-----------------------------------------+
                              ^              ^
                              |              |
                         [작업자]      [외부 시스템]
                        멀티모달 입력      MES/ERP/PLC
```

### 4대 핵심 협동운전 모드 (ISO/TS 15066)

| 협동모드 | 영문/약어 | 원리 | 적용 사례 | 안전 파라미터 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 안전감시정지** | Safety-Rated Monitored Stop (SRMS) | 작업자 접근시 로봇 정지, 퇴거시 자동 재개 | 머시닝센터 로딩/언로딩 | 정지 모니터링 시간 < 100ms |
| **2. 핸드가이딩** | Hand Guiding (HG) | 작업자가 직접 로봇 손목에 부착된 핸들(HG button)로 teach pendant 대체 | 소량 다품종 조립, 경로 기록 | HG 버튼 < 30N이탈시 정지, 직접 teach |
| **3. 속도·거리감시** | Speed & Separation Monitoring (SSM) | 작업자-로봇간 거리(d)에 반비례하여 속도(v) 동적 감속, 최소보호거리 $S_p = S_h + S_r + S_{SSM} + C$ | 동적 셀, 빈번한 접근 | $v_{max} = \sqrt{v_h^2 + a_s \cdot d - a_s \cdot S_h}$ |
| **4. 동력·힘제한** | Power & Force Limiting (PFL) | 충돌시 생체역학적 임계값 이하로 에너지 제한 | 동일 작업공간 협업 | 준정적 ≤80W, 150N / 일과적 ≤400N, 생체 한계 |

### 핵심 센서 및 구동원리

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Joint Torque Sensor (JTS)** | 각 관절별 충돌 토크 검출 | KUKA LBR iiwa는 7개 축 모두에 strain gauge 기반 토크센서(해상도 0.05Nm), 1kHz 샘플링, 외부 외란 관측기(Disturbance Observer) 기반 충돌감지 |
| **6축 F/T Sensor** | 손끝(End-Effector) 힘/모멘트 측정 | ATI Mini45(FS=±145N, ±5Nm), 4전단(strain) Wheatstone Bridge, $F_x, F_y, F_z, M_x, M_y, M_z$ 6DoF 출력, 임피던스 제어 피드백 |
| **전장(Whole-Body) 스킨센서** | 비접촉·접촉 통합 감지 | TUM의 TakkTile(전도성 고무+반석고 패턴, 0.1N 해상도), Tekscan FlexiForce, 캡슐러 네트워크 기반 접점 위치 추정 |
| **RGB-D 카메라** | 작업자 위치·자세·의도 추정 | Intel RealSense D455(스테레오+IR, 0.4~10m, 1280×720@90fps), OpenPose/HRNet 기반 skeleton 추출(17 keypoints) |
| **LiDAR/Depth** | 협업공간 안전 영역 설정 | SICK microScan3(안전 LiDAR, EN ISO 13849-1 PL d), 다중 안전영역(8개 field set), 9m 반경 모니터링 |
| **임피던스 제어기** | 외력에 대한 로봇 동적 거동 | $M\ddot{x} + B\dot{x} + Kx = F_{ext}$, M(질량), B(감쇠), K(강성) 매트릭스를 작업 상황에 따라 가변 |
| **의도추론 엔진** | 작업자 의도·다음 행동 예측 | LSTM(2-layer, 128 units) / Transformer 기반 action anticipation, 0.5~1.5s horizon 예측, 87% accuracy (KIT 데이터셋) |
| **멀티모달 퓨전** | 시·청·촉각 통합 인지 | ROS 2 message_filters 기반 time-synchronizer, 칼만필터/Extended Kalman Filter로 노이즈 제거, 결정론적 동기화(< 10ms) |

### 핵심 안전 수식 (ISO/TS 15066)

**최소보호거리 (Minimum Protective Distance) $S_p$**:

$$S_p = S_h + S_r + S_{SSM} + C$$

- $S_h$: 작업자 위치 불확실 거리 (보폭·이동속도·센서 지연 반영)
- $S_r$: 로봇 정지거리 $S_r = v_{max} \cdot T_r + \frac{v_{max}^2}{2 \cdot a_{max}}$
- $S_{SSM}$: 속도·거리감시 추가거리
- $C$: 침투거리(보통 0, ISO 13855)

**충돌 에너지 한계 (Quasi-static Contact)**:

$$E_{qs} = \frac{1}{2} m_r \cdot v^2 \leq 80 \text{ W·s (생체 한계)}$$

**충돌력 한계 (Transient Contact)**: ≤ 150N (Hand/Finger), ≤ 250N (Palm), ≤ 400N (전신 정적)

- **📢 섹션 요약 비유**: 코봇의 임피던스 제어는 마치 "무게추를 자유롭게 바꿀 수 있는 헬스 아령"과 같다. 무거운 사람에게는 가볍게, 힘이 약한 사람에게는 묵직하게 느껴지도록 강성을 실시간으로 변조하여 언제나 안전한 운동을 만들어낸다.

---

## Ⅲ. 비교 및 연결

| 구분 | 산업용 6축 로봇 | 협동로봇(Cobot) | 휴머노이드(휴먼로봇) |
| :--- | :--- | :--- | :--- |
| **자유도(DoF)** | 6 DoF (안정적 정확도) | 6~7 DoF (kinematic redundancy) | 30~50+ DoF (anthropomorphic) |
| **안전 표준** | ISO 10218-1/2 (격리) | ISO/TS 15066 (4대 협동모드) | ISO 13482 (Personal Care), UL 3300 |
| **반복 정밀도** | ±0.02~0.05 mm | ±0.03~0.1 mm | ±1~5 mm (보행 포함) |
| **페이로드** | 5~2,300 kg | 0.5~35 kg (UR30까지