---
title: "Smart Transportation ITS Autonomous V2X"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 729
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: V2X(Vehicle-to-Everything)는 차량-차량(V2V), 차량-인프라(V2I), 차량-네트워크(V2N), 차량-보행자(V2P) 간 5.9GHz 대역 DSRC(IEEE 802.11p) 또는 3GPP C-V2X(Rel.14 LTE-V2X, Rel.16 NR-V2X) 통신으로 **시야(Non-Line-of-Sight) 제약과 센서 불확실성을 보완**하는 분산 협력 인지(Cooperative Perception) 인프라이며, SAE J2735 표준 메시지(BSM, SPaT, MAP, RTCM) 기반 신호정보 및 위험경고 교환이 핵심 메커니즘이다.
> 2. **가치**: V2X는 미국 NHTSA 연구에서 충돌 회피 효과 약 80%, 신호 최적화 시 도심 주행시간 25%·연료소모 10~20% 절감을 입증했고, L4 이상 자율주행의 안전 fallback(SAE J3016 ODD 외 예외상황) 및 교차로 충돌방지(IEEE 1100건/년 사망사고 감소) 가치로 디지털 트윈·MEC 기반 1ms 이하 지연 제어를 가능케 한다.
> 3. **판단 포인트**: **DSRC(저지연·ad-hoc, 100ms) vs C-V2X(장거리·셀룰러 진화, 20ms, 5G NR은 1~3ms)** 통신기술 선택, **R-ITS 표준(한국, 5.9GHz 20MHz 7ch)·SAE J3061 사이버보안·SCMS 인증서** 적용, **MEC vs 클라우드 분산 아키텍처**, 그리고 **V2X 의존도(Sensor Fusion 비중 30~70%)**가 사업·표준·보안 관점의 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경 및 기술적 필요성

기존 교통체계는 **고정 주기 신호(Fixed-time control)**, **차량 단독 인지(Solo Perception)**, **중앙 통제형 운영(SCATS/SCOOT)** 으로 운영되어 왔다. 그러나 **도심 신호 교차로에서 전체 교통사고의 약 40%**, 사망자의 약 30%가 발생하며, 라이다(LiDAR)·카메라·레이더만으로는 **시야 차단(occlusion), 악천후(폭우·안개 시 성능 60% 저하), 도심 협곡 다중경로 오류(GNSS 정확도 ±5m -> 0.5m 요구)** 등 물리적 한계가 존재한다. 또한 SAE J3016 기준 **L3(조건부 자율) 이상**은 ODD(Operational Design Domain) 이탈 시 fallback이 필요하고, L4는 교차로·합류부에서 **V2I 협력 신호 없이는 도시 공공도로 운행 곤란**하다. 스마트 교통 ITS는 **WAVE/ETSI ITS-G5·C-V2X 표준 통신**, **IEEE 1609.x 상위계층**, **SAE J2735 ASN.1 메시지**, **MEC(ETSI ISG MEC)**, **UTM(UAS Traffic Management)** 등과의 융합을 통해 "차-인프라-네트워크"가 **결합(cooperative) 인지-판단-제어**를 수행하는 **C-ITS(Cooperative-ITS)** 패러다임으로 전환되고 있다.

### 1.2 시스템 개념도 (Cooperative V2X Signal Control)

```text
                              +--------------------------------------+
                              |  National Transport Cloud (TMC/C-ITS)|
                              |  - AI 신호최적화(Reinforcement Learning)|
                              |  - SCMS 인증서/PKI, Big Data Lake    |
                              |  - 디지털 트윈(CityGML 3.0 Map)       |
                              +--------------+-----------------------+
                                             | 광케이블 / 5G N2/N4
                                             v
        +-----------------------------------------------------------------+
        |        Roadside Unit (RSU) - 5.9 GHz, ETSI TS 102 894         |
        |  +----------+  +----------+  +----------+  +--------------+  |
        |  | 802.11p/ |  |  SPaT/   |  |  Edge    |  |  GNSS/PTP    |  |
        |  | LTE-V2X  |  |  MAP     |  |  MEC     |  |  Sync (μs)   |  |
        |  | (PC5/Uu) |  | 방송10Hz |  | (1ms)    |  |              |  |
        |  +----+-----+  +----+-----+  +----+-----+  +------+-------+  |
        +-------+-------------+-------------+---------------+----------+
                |             |             |               |
       (V2I/I2V)|    (I2V/SPaT)|   (분산AI)  |  (시간동기)   |
                v             v             v               v
   +---------------------------------------------------------------------+
   |                  On-Board Unit (OBU) / AV ECU                       |
   |  +--------+  +--------+  +--------+  +--------+  +--------------+   |
   |  | V2V    |  | V2P    |  | BSM    |  | Sensor |  | Autonomous   |   |
   |  | Msg    |  | (P2V)  |  | 10Hz   |  | Fusion |  | Stack(L3~L5) |   |
   |  | CAM    |  | Ped    |  | 송수신 |  | Cam+   |  | P->L->P->P->C    |   |
   |  +--------+  +--------+  +--------+  | LiDAR  |  +------+-------+   |
   |                                      | +Radar |         |          |
   |                                      +--------+         |          |
   +----------------------------------------------------------+----------+
                                                              | CAN-FD/AutoSAR
                                                              v
                                                   +------------------+
                                                   | Vehicle Control  |
                                                   | (Brake/Steer/ACC)|
                                                   +------------------+
```

### 1.3 구 vs 신 패러다임

| 구분 | 기존 교통체계 (Pre-ITS) | 스마트 V2X 기반 C-ITS |
|---|---|---|
| 신호 제어 | 고정 주기(Fixed Cycle, SCOOT 단독 적응) | SPaT-MAP 연계 **실시간 적응형(MOVA+AI)**, GLOSA |
| 인지 범위 | 자차 센서 100~200m, 단일 시야 | **R-ITS 협력인지(Collective Perception, CPM) 500m+** |
| 통신 | 없음 / DSRC(일부), 광섬유 | 5.9GHz DSRC·C-V2X 4G/5G, 5G MEC <3ms |
| 안전 모델 | 반응형(사고 후 처리) | **예측형·예방형**(Collision Avoidance, 100ms 전 경고) |
| 데이터 | 집계(SCATS) | 차량-인프라 다중모달 빅데이터 + 디지털 트윈 |
| 표준화 | 특정업체 폐쇄 | ETSI EN 302 637 / SAE J2735 / IEEE 1609 / 3GPP Rel.14~17 |

- **📢 섹션 요약 비유**: 기존 신호 체계가 **각자 보고 판단하는 외딴 섬**이었다면, V2X는 **서로 무전기로 실시간 대화하며 비행하는 비행관제 시스템**과 같다. 비행기는 레이더만 보지 않고 ATC(항공관제)·ADS-B로 서로 위치를 공유하기에 안전해진 것처럼, 차량도 RSU·OBU·MEC와 끊임없이 데이터를 교환한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 V2X 4계층 아키텍처

```text
+----------------------------------------------------------------------+
|  Layer 4 : Application (응용)                                         |
|  +- V2V: Forward Collision Warning, Emergency Brake Light, BSM       |
|  +- V2I: SPaT (Signal Phase & Timing), MAP, GLOSA, Eco-Approach     |
|  +- V2P: Pedestrian Crossing Info (PC5)                              |
|  +- V2N: HD Map 업데이트, OTA, 혼잡통제                               |
|  +- V2D: Drone Delivery Coordination (DAA)                          |
+----------------------------------------------------------------------+
|  Layer 3 : Networking (네트워크/메시지 표준)                            |
|  +- SAE J2735 ASN.1 메시지(BSM/CAM/DENM/SPaT/MAP/RTCM/PSM/SSM/SAEM)  |
|  +- ETSI ITS-G5: CAM, DENM, IVIM, SREM/SSEM, CPM, VRU                |
|  +- BTP (Basic Transport Protocol), GeoNetworking                     |
|  +- WAVE Short Message (WSM), IEEE 1609.3/4 (WSMP, Security)         |
+----------------------------------------------------------------------+
|  Layer 2 : Access (전송)                                              |
|  +- DSRC : IEEE 802.11p (5.9 GHz, OFDM, 27 Mbps, Ad-hoc)             |
|  |       - 미국 5.850~5.925 GHz (채널 172~184, 10MHz×7)               |
|  |       - 한국 R-ITS 5.855~5.875 GHz (R-ITS A/B, C는 reserved)        |
|  +- C-V2X: 3GPP Rel.14(PC5/Uu) -> Rel.15(5G 슬라이스) -> Rel.16(NR-V2X)|
|            - PC5(Sidelink, 5.9GHz, 모드3/4 자원할당, 자원풀 감시)       |
|            - Uu(Up/Downlink, LTE/5G, 광역 V2N)                          |
|            - Rel.16 5G NR-V2X: 1ms subframe, URLLC, 3GPP TS 36.300   |
+----------------------------------------------------------------------+
|  Layer 1 : Physical (물리)                                            |
|  - 5.9 GHz, OFDM, 10MHz 채널, 27/54 Mbps, QPSK-64QAM                   |
|  - GNSS 동기(GPS L1+L5, BeiDou B1I/B3I, Galileo E1/E5) ±100ns        |
|  - PTP(IEEE 1588v2) / SyncE RSU 간 시간동기                             |
+----------------------------------------------------------------------+
```

### 2.2 신호제어 프로토콜 시퀀스 (I2V + V2V)

```text
  TMC(중앙)        RSU+신호기        OBU(자차)         주변 OBU들        Cloud MEC
     |                |                |                  |                |
     | ① 신호데이터   |                |                  |                |
     |  (4단계 현시,  |                |                  |                |
     |  잔여시간)     |                |                  |                |
     | -------------►|                |                  |                |
     |                | ② SPaT 브로드  |                  |                |
     |                |  (10Hz, ASN.1) |                  |                |
     |                | --------------►|                  |                |
     |                | ③ MAP 메시지   |                  |                |
     |                |  (Intersection|                  |                |
     |                |   Geometry)    |                  |                |
     |                | --------------►|                  |                |
     |                |                | ④ BSM 10Hz      |                |
     |                |                |