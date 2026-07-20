---
title: "Quantum Internet Quantum Network Sensor"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 787
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 양자 인터넷(Quantum Internet)은 얽힘(entanglement) 자원의 분배와 양자 텔레포테이션(teleportation)을 기반으로 한 **위상적(phase-coherent) 네트워크**이며, 양자 센서(Quantum Sensor)는 헤테로다인 간섭계·NV 센터·압축광(squeezed light) 등을 활용하여 **표준 양자 한계(SQL) 이하의 분해능**을 달성하는 측정 체계이다.
> 2. **가치**: QKD(Quantum Key Distribution)는 정보이론적 안전성(unconditional security, 보안 키 생성률 수 Mbps~수백 kbps@수백 km), 양자 센서는 자기장 분해능 **fT/√Hz 수준**, 중력 측정 **10⁻¹¹ g/√Hz** 등 고전 센서 대비 수십~수백 배 정밀도를 제공하며, 분산 양자 컴퓨팅(distributed quantum computing)을 통한 **1,000+ 논리 큐비트 클러스터** 구성을 가능케 한다.
> 3. **판단 포인트**: 아키텍처 선택 시 **메모리 기반 양자 중계기(memory-based repeater) vs 측정 기반(memory-less)**, **단일 광자 vs 연속 변수(CV)**, **결정론적(deterministic) vs 확률적(probabilistic) 스왑** 간의 트레이드오프, 그리고 **fidelity 임계치(F>2/3 for entanglement purification, F>0.99 for fault-tolerant)**를 기준으로 물리 계층·링크 계층·네트워크 계층을 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

기존 고전 인터넷은 전자기파의 진폭·주파수·위상 등 **고전적 자유도**를 변조하여 정보를 전달하지만, 양자 인터넷은 **광자의 편광·경로·시간빈(time-bin)·직교 위상 등 양자 상태(|ψ⟩) 자체를 전송 자원**으로 사용한다. 2024년 ITU-T Y.3800 시리즈와 ETSI ISG-QKD 표준이 사실상(de facto) 완료되면서, 단순 QKD 전송을 넘어 **얽힘 분배 네트워크(entanglement distribution network)**와 **양자-고전 융합 네트워크(quantum-classical converged network)**로 패러다임이 전환되고 있다.

NIST PQC 표준화(FIPS 203/204/205, 2024)와 병행하여 양자 키 분배는 **Harvest Now, Decrypt Later(HNDL)** 공격에 대한 장기적 안전성(forward secrecy)을 보장하는 유일한 실용적 수단으로 재조명받고 있다. 또한 양자 센서는 의료 MRI의 **10⁶배 민감도**를 갖는 마그네토미터, 지하 자원 탐사를 위한 **중력 그라디오미터**, 그리고 GPS-denied 환경에서의 **관성 항법(quantum inertial navigation)**에 활용되어 국방·에너지·헬스케어 분야의 게임 체인저로 부상했다.

그러나 **디코히어런스(decoherence, T₂: 수십 μs ~ 수 s)**, **광자 손실(0.2~0.3 dB/km @ telecom wavelength 1550nm)**, **결정론적 게이트 부재(현재 1-큐비트 게이트 충실도 99.9% 수준이나 2-큐비트 99.5% 이하)**, 그리고 **결정적 단일 광자 소스(deterministic single-photon source) 미성숙** 등 4대 난제가 상용화를 가로막고 있다.

```text
+---------------------------------------------------------------------+
|            양자 인터넷 / 양자 네트워크 / 양자 센서 통합 관점         |
+---------------------------------------------------------------------+
|                                                                     |
|   [양자 응용 계층]                                                   |
|    +----------+ +----------+ +----------+ +------------------+     |
|    | 양자암호  | | 분산양자  | | 양자클럭  | | 양자센싱 클라우드 |     |
|    | (QKD)   | | 컴퓨팅    | | 동기화   | | (Quantum Sensing) |     |
|    +----+-----+ +----+-----+ +----+-----+ +------+-----------+     |
|         +-------+----+-------+----+--------------+                 |
|                 v            v                                     |
|   [양자 네트워크 계층] - Entanglement Routing, Qubit Addressing       |
|    +------------------------------------------------------+        |
|    | Quantum Repeater (Station) -> Station -> Station ...    |        |
|    | +---------+  +---------+  +---------+  +---------+  |        |
|    | |Entangle-|-> |Entangle-|-> |Entangle-|-> |Entangle-|  |        |
|    | |ment Swap|  |ment Swap|  |ment Swap|  |ment Swap|  |        |
|    | +---------+  +---------+  +---------+  +---------+  |        |
|    +------------------------------------------------------+        |
|         |              |              |                            |
|   [양자 링크 계층]   - Purcell-enhanced, DLCZ, Entanglement Pumping|
|         |              |              |                            |
|   [양자 물리 계층]                                                   |
|    +----------+  +----------+  +----------+  +----------+         |
|    | 1550nm   |  | 1310nm   |  | NV-diamond|  |Neutral   |         |
|    | Telecom  |  | O-band   |  | Memory    |  |Atom (Rb) |         |
|    | Photon   |  | Photon   |  | (室温)    |  | Memory   |         |
|    +----------+  +----------+  +----------+  +----------+         |
|                                                                     |
|   [고전 보조 채널 - Synchronization, Classical Auth, SDN 제어]      |
|   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
+---------------------------------------------------------------------+
```

기존 고전 광통신 대비 양자 네트워크는 **No-Cloning Theorem(복제 불가)**과 **측정 붕괴(measurement collapse)**로 인해 신호 증폭이 불가능하므로, 양자 중계기·양자 메모리·오류 정정(QEC, 예: surface code distance d=3~7)이 필수적이다. 이는 마치 "편지를 복사할 수 없고, 봉투를 열면 자동으로 원본이 사라지는 우편 시스템"에 비유할 수 있다.

- **📢 섹션 요약 비유**: 양자 인터넷은 **"만지면 사라지는 유리 구슬의 줄"**과 같다. 구슬(광자)을 직접 전달할 수 없고, 양자 얽힘이라는 보이지 않는 끈으로 연결된 다음 역까지 즉시 그 상태를 "텔레포트" 시켜야 한다. 도중에 누가 들여다보면(측정) 줄이 끊어버린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 양자 인터넷의 6계층 아키텍처 (Wehner et al., Science 2018 + IETF QIRG Draft)

```
Layer 6: Quantum Application          (QKD, Blind Quantum Computing, Clock Sync)
Layer 5: Quantum Network Application  (QPG, QIA, Distributed Consensus)
Layer 4: Quantum Transport            (Entanglement distillation, error correction)
Layer 3: Quantum Network              (Long-distance entanglement routing)
Layer 2: Quantum Link                 (Entanglement generation + swapping)
Layer 1: Physical (Photon, Memory)    (1550nm fiber, free-space, NV/atom)
```

### 2. 핵심 프로토콜 스택

```text
    Alice                                                  Bob
    +----+         양자 채널 (Quantum Channel)          +----+
    | QPG| ----- |ψ_AB⟩ = (|00⟩+|11⟩)/√2 --------------->| QPG|
    |    |   <----- Bell State Measurement (BSM) ----------|    |
    +-+--+                                                +-+--+
      | 고전 채널 (Classical Channel - Authenticated)         |
      | <--- Measurement outcome (2 bits per BSM) ----------->|
      v                                                      v
    +----------------------------------------------------------+
    | 1. Entanglement Purification (BBPSSW / DEJMPS)          |
    |    - Target Fidelity: F = 1 - ε (ε < 10⁻⁴ 요구)         |
    | 2. Entanglement Swapping (Probabilistic: 1/4 success)   |
    | 3. Virtual Photon / Teleportation (|ψ⟩ -> X^aZ^b|ψ⟩)    |
    | 4. Privacy Amplification (Toeplitz matrix, 2:1 ratio)   |
    +----------------------------------------------------------+
                              |
                              v
                    [Secret Key Rate: SKR]
                    SKR = QBER · f(e) · μ
                    QBER < 11% (BB84 threshold)
                    SKR ≈ 1 Mbps (10km) -> 1 kbps (100km) -> 1 bps (500km)
```

### 3. QKD 프로토콜 변형

```text
   +--------------+  +--------------+  +--------------+  +--------------+
   |   BB84       |  |   E91        |  |  MDI-QKD     |  |   TF-QKD     |
   | (Bennett-    |  | (Ekert-1991) |  | (Lo-Curty-   |  | (Lucamarini- |
   |  Brassard)   |  |              |  |  2012)       |  |  2018)       |
   | Prepare &    |  | Entangle-    |  | Detector-    |  |  Twin-Field  |
   | Measure      |  | ment-based   |  | Independent  |  |  (PLOB bound |
   | 4 states,    |  | Bell test    |  | 중앙 노드    |  |   도달)      |
   | 2 bases      |  | (CHSH>2)     |  | 신뢰 중계    |  |              |
   | SKR ~ 1Mbps  |  | SKR ~ 100kbps|  | SKR ~ 10kbps |  | SKR limit ^  |
   | @ 50km fiber |  | @ 50km       |  | @ 100km      |  | PLOB × √η   |
   +--------------+  +--------------+  +--------------+  +--------------+
```

### 4. 양자 센서 플랫폼별 비교

```text
   Platform         Sensitivity         Operating   Decoherence
   -----------------------------------------------------------------
   NV-Center        B_field: 1 nT/√Hz   Room-T      T₂* ~ μs, T₁ ~ ms
   (Diamond)        Temperature: mK
                    Strain: 10⁻⁶/√Hz

   Trapped Ion      Frequency: 10⁻¹⁵  UHV, ~μK     T₂ ~ s ~ min
   (Ca⁺, Yb⁺)      Inertial: 10⁻⁹ g  (laser-cool)
                    Clocks: 10⁻¹⁸ frac

   Neutral Atom     Magnetometer: fT  Cold atoms  T_coh ~ s
   (Rb, Sr)         Gravimeter: 10⁻¹¹g
   (Lattice)        Clocks: 10⁻¹⁹ frac (Sr-87)

   Superconducting  Magnetometry: fT  mK (dilution) T₂ ~ 100 μs
   (SQUID, Flux)    Qubit readout

   Squeezed Light   LIGO strain: 10⁻²³  Optical bench
   (Interfero-      Below SQL
    metry)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **단일 광자 원 (SPDC / Quantum Dot)** | 양자 상태 캐리어 | Type-II SPDC(0.5 쌍/펄스@1550nm), InAs/GaAs QD(>0.85 indistinguishability), 박형 주기적 분극(PPKTP) |
| **양자 메모리 (Quantum Memory)** | 얽힘 동기화·버퍼링 | DLCZ(Δ->Cs, η~80%), EIT(Rb, Γ~MHz), NV ensemble(Hahn-echo, T₂~ms), ATC(rare-earth Pr:YSO) |
| **양자 중계기 (Quantum Repeater)** | 장거리 얽힘 분배 | 1세대: 확률적 swapping + purification, 2세대: 결정론적(mem-based), 3세대: QEC 기반(Stabilizer code) |
| **Bell State 측정기 (BSM)** | 얽힘 스왑·텔레포테이션 | 선형 광학 BSM(성공률 50%, 4 Bell states 중 2), 시간빈 demultiplexer + TCC, HOM 간섭(visibility > 96%) |
| **고전 보조 채널 (SDN/Fiber)** | 동기화·인증·라우팅 | ITU-T G.798 OTN, IEEE 1588v2 PTP(<ns 동기), ETSI GS QKD 015 REST API, BB84 weak coherent state 인증 |
| **양자 센서 어레이** | 분산 측량·그라디오메트리 | Magnetometer(OPM, OPM-MEG), Atom interferometer(0.1 nrad/√Hz), Photonic integrated circuit(PIC) |

### 5. 핵심 알고리즘: 얽힘 정제 (Entanglement Purification)

BBPSSW 프로토콜(1996)은 양면(local) CNOT 후 양측 측정을 통해 2개의 낮은 fidelity 얽힘 쌍으로부터 1개의 높은 fidelity 쌍을 확률적으로 생성한다:
- 입력: F < 1, 양자 비트 오류율(QBER) = (1-F)/3
- 출력: F' = F² + (1-F)²/9 (purity of Werner state)
- 재귀적 적용 시 F -> 1까지 수렴 가능 (예: 9라운드 -> F > 0.999)

DEJMPS 프로토콜(1998)은 4 Bell states 기반으로 한 번에 2개 비트를 측정하여 **수율(yield)**을 BBPSSW 대비 2배 향상시킨다.

- **📢 섹션 요약 비유**: 양자 네트워크는 **"거울의 방"**과 같다. 들어가는 정보(광자)는 한 번만 보일 수 있고, 복도 중간중간에 설치된 **"거울(메모리)"**에 잠시 비추다가 다음 거울로 보내야 끝까지 손실 없이 도달한다. 복도에 도청자(측정자)가 들어오면 즉시 거울이 깨진다(얽힘 붕괴).

---

## Ⅲ. 비교 및 연결

### 1. 양자 인터넷 vs 고전 인터넷 (네트워크 계층)

| 구분 | 고전 인터넷 (TCP/IP) | 양자 인터넷 (QIRG/IPv9 over Q) |
| :--- | :--- | :--- |
| **패킷 단위** | 비트 (0/1), 64B~1.5kB | 큐비트 (|0⟩, |1⟩, α|0⟩+β|1⟩), 1 photon |
| **신호 증폭** | EDFA, SOA(광 증폭) | 불가 (No-Cloning), 양자 중계기 필수 |
| **라우팅** | BGP, OSPF, MPLS-TE | Qubit Address(Wehner 2018), Path Identification |
| **오류 정정** | Reed-Solomon, LDPC(10⁻⁹ BER) | Surface Code(d=3~21), Bacon-Shor, Topological |
| **지연 시간** | ms~s (광속 한계) | 동일 (광속 한계), 단 teleportation 시 큐비트 확정 필요 |
|