---
title: "Robotics Autonomous Navigation Motion Planning"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 719
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 로보틱스 자율 내비게이션 모션 플래닝은 **C-Space(구성공간) 상에서 시작 자세(q_start)에서 목표 자세(q_goal)까지 충돌 회피와 운동학적/동역학적 제약(Kinodynamic Constraints)을 만족하는 최적 궤적 τ(t) = {q(t), q̇(t), q̈(t)}를 생성**하는 문제로, **전역 경로 계획(Global Planner)**과 **지역 궤적 최적화(Local Trajectory Optimizer)**의 이계층 구조가 핵심이다.
> 2. **가치**: 잘 설계된 모션 플래너는 동적 환경에서 **궤적 추종 오차 0.05m 이내, 재계획 주기 10~100ms, 처리량 1Hz~100Hz**를 보장하며, AGV/AMR 기준 **이동 효율성 30~50% 향상, 충돌 사고율 99% 감소, 데드락(Deadlock) 발생 확률 1% 미만**의 정량적 이득을 제공한다.
> 3. **판단 포인트**: **샘플 기반(Sampling-based: RRT/RRT*) vs 최적화 기반(Optimization-based: CHOMP/Traj-Opt) vs 학습 기반(Learning-based: NMP/BC-Z)** 패러다임 간의 **완전성(Completeness), 최적성(Optimality), 실시간성(Real-time), 차원 확장성(Dimensional Scalability)** 트레이드오프가 핵심 설계 결정 포인트이며, **Holonomic vs Non-holonomic**, **Static vs Dynamic**, **Known vs Unknown Map** 조건에 따라 알고리즘 선택 기준이 달라진다.

---

## Ⅰ. 개요 및 필요성

자율 이동 로봇(AMR, AGV, 자율주행차, 드론, 휴머노이드)의 **Navigation 2 (Nav2) 스택**에서 모션 플래닝은 **"로봇이 어디로, 어떤 속도/가속도 프로파일로, 얼마나 안전하게 움직일 것인가"**를 결정하는 두뇌 역할이다. 이는 단순히 최단 경로(Shortest Path)를 찾는 것을 넘어, **차량 동역학(Bicycle/Ackermann/Differential/Unicycle Model)**, **장애물 회피(Dynamic Obstacle Avoidance)**, **제약 조건 하 최적화(Constrained Optimization)**를 동시에 만족해야 하는 NP-hard 계열의 고차원 연속 최적화 문제이다.

기존의 **Rule-based 방식(예: Follow Wall, Bug Algorithm)**은 1970~80년대의 정적 환경에서는 동작했지만, **현대 물류창고에서 100대 이상의 AMR이 동시 운행**하고, **보행자·PALLET·지게차**가 혼재하는 비정형 환경에서는 한계가 명확하다. 이에 따라 **확률적 완전성(Probabilistic Completeness)**을 갖는 **RRT 계열**, **점근적 최적성(Asymptotic Optimality)**을 갖는 **RRT\*/Informed RRT\***, **그래프 탐색(A\*/D\*/LPA\*)**, **최적화 기반(CHOMP/STOMP/MPCC)** 알고리즘이 산업계 표준으로 자리 잡았다.

```text
+---------------------------------------------------------------------+
|         자율 내비게이션 모션 플래닝 5계층 아키텍처 (5-Layer Stack)  |
+---------------------------------------------------------------------+
|                                                                     |
|   +--------------------------------------------------------------+  |
|   | L5. Behavior Layer (행위 결정)                                |  |
|   |    - 상태기계(FSM): IDLE -> NAVIGATING -> AVOIDING -> RECOVERY |  |
|   |    - Task Planner: 목적지 변경, 멀티로봇 협업 우선순위        |  |
|   +--------------------------------------------------------------+  |
|                            ^                                        |
|   +--------------------------------------------------------------+  |
|   | L4. Global Planner (전역 경로 계획)                           |  |
|   |    - 알고리즘: A*, D*, NavFn, SMAC Planner (Hybric A*)       |  |
|   |    - 입력: Costmap_2D / Costmap_3D (Static + Inflation)       |  |
|   |    - 출력: Global Path (Discrete waypoints, ~1m 간격)         |  |
|   +--------------------------------------------------------------+  |
|                            ^                                        |
|   +--------------------------------------------------------------+  |
|   | L3. Local Planner / Controller (지역 궤적 최적화)            |  |
|   |    - 알고리즘: DWA, TEB, MPC, MPCC, Regulated Pure Pursuit  |  |
|   |    - 입력: Local Costmap (5~10m 윈도우, 10~20Hz 갱신)        |  |
|   |    - 출력: Velocity Cmd (v, ω) @ 20~50Hz                     |  |
|   +--------------------------------------------------------------+  |
|                            ^                                        |
|   +--------------------------------------------------------------+  |
|   | L2. Perception & SLAM (인지 및 지도)                         |  |
|   |    - LiDAR (2D/3D, 10~40Hz), Camera (RGB-D, 30Hz)            |  |
|   |    - VSLAM/ORB-SLAM3, Cartographer, LIO-SAM, FAST-LIO2      |  |
|   |    - EKF/UKF 기반 Sensor Fusion (robot_localization)         |  |
|   +--------------------------------------------------------------+  |
|                            ^                                        |
|   +--------------------------------------------------------------+  |
|   | L1. Hardware Driver (HW 추상화)                              |  |
|   |    - Wheel Odometry, IMU (100~1000Hz), Motor Controller     |  |
|   |    - ROS 2 Topics: /cmd_vel, /odom, /scan, /tf, /map        |  |
|   +--------------------------------------------------------------+  |
|                                                                     |
+---------------------------------------------------------------------+
        v 최종 출력: /cmd_vel (geometry_msgs/Twist) -> Motor Driver
```

**왜 필요한가?** 현대 물류 자동화 시장은 2027년 약 **$51B 규모**로 성장하며, **Amazon Kiva, 미라콤, 쿠팡, CJ대한통운** 등에서 **100~1,000대 AMR Fleet**이 운영된다. 이때 모션 플래너의 **재계획 지연(Replanning Latency)**이 200ms를 넘으면 충돌 위험이 급격히 증가하며, **Fleet Management System(FMS)**과의 **Deadlock 회피 및 Traffic Control**이 필수적이다. 또한 **ISO 3691-4 (Driverless Industrial Trucks)** 표준에서 **PLd 이상**의 안전성 인증을 요구하므로, 결정론적 검증이 가능한 모션 플래닝 구조 설계가 학습 주제 빈도가 높은 영역이다.

- **📢 섹션 요약 비유**: 마치 **GPS 네비게이션(전역)**과 **운전자의 눈과 핸들 조작(지역)**이 동시에 동작하는 자동차 운전과 같다. 내비게이션이 "어떤 도로로 가라"고 알려주면, 운전자는 실시간으로 보행자·차량을 보며 핸들을 조작한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

자율 내비게이션 모션 플래닝 시스템은 크게 **(1) 지도 표현(Map Representation)**, **(2) 전역 경로 계획(Global Path Planning)**, **(3) 지역 궤적 최적화(Local Trajectory Optimization)**, **(4) 제어 인터페이스(Control Interface)**의 4대 구성 요소로 나뉜다.

### 1. 지도 표현 (Map Representation)

지도는 크게 3가지로 분류된다:

- **메트릭 맵 (Metric Map)**: Occupancy Grid Map(2D), Voxel Grid(3D), OctoMap(확률적 3D 점유 지도)
- **위상 맵 (Topological Map)**: 노드(랜드마크)와 엣지(연결 관계)로 추상화
- **하이브리드 맵 (Hybrid)**: 메트릭 + 위상 (예: Hierarchical Voronoi Graph)

**Costmap_2D**는 ROS Navigation 스택의 핵심으로, **Static Layer + Obstacle Layer + Inflation Layer**를 합성한다. Inflation Layer는 장애물로부터 로봇 반경만큼 **Lethargy Cost**를 적용한 후, **Decay 함수(Quadratic: cost = d²/r²)**로 거리에 따라 비용을 증가시켜 **안전 마진(Safety Margin)**을 보장한다.

### 2. 전역 경로 계획 (Global Path Planning)

**A*** 알고리즘은 휴리스틱 함수 h(n)을 이용한 Best-First Search로, **f(n) = g(n) + h(n)**을 최소화한다. **Admissible Heuristic(허용 휴리스틱, h(n) ≤ 실제 비용)**일 때 최적성을 보장한다. **ROS 2 Nav2의 SMAC Planner**는 **4축/8축 방향성 Hybrid A***로, **Dubin/Reeds-Shepp 곡선**을 통합하여 **Non-holonomic 제약** 하에서도 부드러운 경로를 생성한다.

**D* Lite / LPA***은 **Incremental Search**로, 환경 변화 시 **g-value**만 부분 갱신하여 **재계획 시간 90% 단축**이 가능하다.

### 3. 지역 궤적 최적화 (Local Trajectory Optimization)

DWA(Dynamic Window Approach)는 **속도 공간(v, ω) 샘플링** 후 **Cost Function**으로 최적 속도 쌍을 선택한다. Cost는 일반적으로 **① 경로 정렬(Path Alignment), ② 장애물 거리(Obstacle Clearance), ③ 전진 속도(Forward Velocity)**의 가중치 합으로 구성된다:

```
J(v, ω) = α·header(경로 정렬) + β·clearance(장애물) + γ·velocity(속도)
```

**TEB(Timed Elastic Band)**는 경로상의 포즈(Pose)에 **시간 간격 ΔTᵢ**를 추가하여 **Elastc Band**처럼 시간 최적화를 수행하며, **g²o 프레임워크** 기반 그래프 최적화로 다중 제약(속도/가속도/최소거리)을 만족한다.

**MPC(Model Predictive Control)** 기반 모션 플래너는 시스템 동역학 모델을 직접 임베드하여 **Receding Horizon(예측 수평선 N=20~50 step)**에서 최적 제어 입력을 계산한다. **MPCC(Model Predictive Contouring Control)**은 경로 추종 오차(Lateral Deviation)와 **Contouring Error**를 최소화하며, 자율주행차의 **Autoware, Apollo**에 사용된다.

### 4. 핵심 수식: 동역학적 궤적 최적화

```
min_{u(t)}  J = ∫₀ᵀ [ (x(t) - x_ref(t))ᵀQ(x(t) - x_ref(t)) + u(t)ᵀR u(t) ] dt
s.t. ẋ(t) = f(x(t), u(t))           // 차량 동역학 (Bicycle Model)
      g(x(t), u(t)) ≤ 0              // 제약: 장애물 회피, 속도 한계
      x(0) = x_init, x(T) = x_goal   // 경계 조건
```

**Bicycle Model**: `ẋ = v·cos(ψ+β), ẏ = v·sin(ψ+β), ψ̇ = (v/L)·sin(β)·cos(β)`
여기서 β = atan((lr/L)·tan(δf))는 **슬립각(Slip Angle)**, δf는 **전륜 조향각**이다.

```text
+---------------------------------------------------------------------+
|           Moduel Planning Detailed Data Flow (지역 플래너)         |
+---------------------------------------------------------------------+
|                                                                     |
|  Global Path: [(x₁,y₁), (x₂,y₂), ..., (xₙ,yₙ)]                    |
|       |                                                             |
|       v                                                             |
|  +-------------------------------------------------------------+   |
|  | 1) Truncate to Local Window (3~5m lookahead)                |   |
|  +-------------------------------------------------------------+   |
|       |                                                             |
|       v                                                             |
|  +-------------------------------------------------------------+   |
|  | 2) Generate Candidate Trajectories (v ∈ [0, v_max], ω sample)|   |
|  |    - Forward Simulate Δt·N steps (v, ω) -> (x,y,θ)轨迹       |   |
|  |    - 예: 20 v × 30 ω = 600 trajectories / cycle             |   |
|  +-------------------------------------------------------------+   |
|       |                                                             |
|       v                                                             |
|  +-------------------------------------------------------------+   |
|  | 3) Score Trajectories (Multi-objective cost)                |   |
|  |    - J = w_p·path_align + w_o·obstacle + w_v·velocity      |   |
|  |    - Collision Check via Footprint vs Costmap               |   |
|  +-------------------------------------------------------------+   |
|       |                                                             |
|       v                                                             |
|  +-------------------------------------------------------------+   |
|  | 4) Select Best (v*, ω*) -> Publish /cmd_vel                  |   |
|  +-------------------------------------------------------------+   |
|       |                                                             |
|       v  (loop @ 20Hz)                                              |
+---------------------------------------------------------------------+
```

### 5. 샘플 기반 vs 최적화 기반 알고리즘 상세 비교

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Occupancy Grid / Voxel Hash** | 환경 표현 | 해상도 0.05~0.2m/cell, OpenVDB 구조로 메모리 효율화, Log-odds 업데이트 `L = L_prev + L_obs - L_prior` |
| **Global Planner (A*/D*/RRT*)** | 시작-목표 경로 탐색 | Heuristic 함수 h(n)=Euclidean/Diagonal, RRT*는 Rewire 단계에서 Near 노드들의 부모 재선택으로 점근적 최적성 보장 |
| **Local Planner (DWA/TEB/MPC)** | 동적 장애물 회피 + 제어 | Sample-based 또는 Convex Optimization(QP/IP), Horizon N=20~50, 주기 20~50Hz |
| **Recovery Behavior** | 데드락/국소최소 탈출 | Rotate Recovery(제자리 회전), BackUp Recovery(후진), Clear Costmap, Wait(1s) |
| **Costmap Layer** | 안전 마진 보장 | Inflation Radius = robot_radius + 0.3~0.5m, Decay = `1.0 - (d/r)²` (Quadratic Decay) |

### 6. 최근 학습 기반(L4) 접근법

- **Neural Motion Planning (NMP, 2019)**: Raw Sensor -> End-to-End Trajectory (NVIDIA, GPU 필요)
- **BC-Z / RT-1/RT-2 (2023)**: Behavior Cloning, Zero-shot Generalization
- **Diffusion Policy (2023)**: Denoising Diffusion으로 Multi-modal Trajectory 생성
- **MPPI (Model Predictive Path Integral)**: GPU 병렬화로 1024 샘플/50ms 처리, **Nvidia DriveWorks** 적용

- **📢 섹션 요약 비유**: 마치 **항공기 자동 조종 장치(Autopilot)**와 같다. 파일럿이 코스를 짜고(Global), 자동 조종이 바람/기류를 실시간으로 보정하며(Local) 비행한다.

---

## Ⅲ. 비교 및 연결

### 1. 모션 플래닝 알고리즘 패러다임 비교

| 구분 | A* (Graph Search) | RRT/RRT* (Sampling) | CHOMP/STOMP (Optimization) | MPPI (Sampling + Control) | NMP/Diffusion (Learning) |
|:---|:---|:---|:---|:---|:---|
| **완전성** | 결정론적 (Discretized) | 확률적 완전성 | 국소 최적 (Local Optima) | 확률적 최적화 | 보장 안됨 |
| **최적성** | Heuristic 품질 의존 | 점근적 (RRT*) | 국소 최적 | Sample 수에 의존 | 학습 데이터 의존 |
| **계산 복잡도** | O(b^d), 메모리 ^ | O(n log n) | O(N·M) iter | O(K·N) 병렬화 | O(Network FLOPs) |
| **차원 확장성** | 7~8 DoF 한계 | 10+ DoF 우수 | 7~14 DoF | 10+ DoF | 20+ DoF 가능