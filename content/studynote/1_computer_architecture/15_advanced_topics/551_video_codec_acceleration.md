+++
title = "551. 비디오 코덱 하드웨어 가속 (H.265 / AV1)"
date = "2026-03-14"
weight = 551
+++

# 551. 비디오 코덱 하드웨어 가속 (H.265 / AV1)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **VPU (Video Processing Unit)** 또는 **MCM (Multi-Chip Module)** 형태로 구현된 **ASIC (Application-Specific Integrated Circuit)** 블록을 사용하여, HEVC(H.265)나 AV1 같은 고부하 코덱의 변환(Transform), 양자화(Quantization), 엔트로피 코딩(Entropy Coding) 과정을 범용 **CPU (Central Processing Unit)**가 아닌 전용 회로에서 처리하는 기술.
> 2. **가치**: **GPGPU (General-Purpose computing on Graphics Processing Units)** 셰이더 기반 소프트웨어 디코딩 대비 **전력 효율(Power Efficiency)**을 10배 이상 향상시키며, **4K/UHD (Ultra High Definition)**, **8K**급 고비트레이트 스트리밍 시 **CPU 점유율을 0~1% 수준**으로 억제하여 모바일 배터리 수명을 보전하고 실시간성을 확보.
> 3. **융합**: **GPU (Graphics Processing Unit)** 가속기(NVENC, Quick Sync)와 **NPU (Neural Processing Unit)** 기반 슈퍼 해상도(DLSS, FSR) 기술과 결합하여, 단순한 디코딩을 넘어 저해상도 영상을 고화질로 복원하는 AI 기반 파이프라인의 필수적인 하드웨어 기반(Hardware Foundation) 역할을 수행.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**
비디오 코덱 하드웨어 가속이란, 디지털 영상 신호를 압축(Encoding)하고 해제(Decoding)하는 과정에서 발생하는 정수 연산, 부동소수점 연산, 메모리 접근 패턴을 범용 프로세서가 아닌 특정 목적의 하드웨어 로직(주로 **ASIC** 또는 **FPGA (Field-Programmable Gate Array)**)으로 오프로딩(Offloading)하는 설계 기술을 의미한다. 현대의 **SoC (System on Chip)** 아키텍처에서는 CPU 코어 옆에 미디어 엔진(Media Engine)이라는 독립된 **VPU (Video Processing Unit)** 블록을 두어, 운영체제(OS)의 **MM (Memory Manager)**가 이를 직접 제어한다.

**💡 비유**
CPU가 동영상을 디코딩하는 것은 **'쉐프(CPU)'가 칼을 들고 수백만 개의 감자(픽셀)를 하나하나 깎아서 요리하는 것**과 같다. 아무리 유능한 쉐프라도 이 일만 하면 식당(시스템)이 멈춘다. 하드웨어 가속기는 주방 한구석에 설치된 **'全自动 감자 처리기(VPU)'**와 같다. 쉐프는 감자 포대만 투입구에 넣어주고, 기계가 내부의 컨베이어 벨트와 칼날(ASIC 로직)을 통해 순식간에 처리된 결과를 받아내어 그릇에 담기만 하면 된다.

**등장 배경 및 기술적 필요성**
1.  **해상도의 폭발적 증가와 압축 알고리즘의 복잡도**: MPEG-2 시절부터 H.264/AVC, H.265/HEVC, AV1로 진화하면서 프레임 내 예측(Intra Prediction), 움직임 보상(Motion Compensation), 변환 코딩(Transform Coding)의 계산량이 기하급수적으로 증가. 소프트웨어 처리 시 초당 30프레임(FPS)을 유지하기 위해 **수십 GFLOPs**급 연산이 필요하게 됨.
2.  **전력 연비의 벽 (Dennard Scaling 붕괴)**: 범용 CPU나 GPU의 셰이더 코어는 유연성(Flexibility)을 위해 제어 로직이 복잡하여, 단순 반복 연산인 코덱 처리에는 불필요한 전력 낭비가 심함. 모바일 디바이스의 배터리 타임을 확보하기 위해 고정된 함수(Fixed-function)를 처리하는 ASIC 방식이 필수적이 되었음.
3.  **실시간 스트리밍 서비스의 요구**: **OTT (Over-The-Top)** 서비스 및 **VOD (Video on Demand)** 플랫폼에서는 버퍼링 없는 실시간 재생을 위해 **저지연(Low Latency)** 디코딩이 필수적이며, 이는 하드웨어 가속 없이는 불가능한 과제가 됨.

**ASCII 다이어그램: 비디오 처리 파이프라인의 진화**

```text
  [Evolution of Video Processing Pipeline]

  (A) Past: Software Decoding (CPU Bound)
  ┌──────────────────────────────────────────────────────┐
  │ Storage (HDD/SSD)                                    │
  │      │                                               │
  │      ▼ (Compressed Bitstream: H.264/HEVC)            │
  │ ┌──────────────────────────────────────────────┐    │
  │ │   System RAM (DRAM)                          │    │
  │ │   ─────────────────────────────────────       │    │
  │ │   CPU fetches data -> Decode (SW Logic)      │    │
  │ │   :  High Utilization (80%~100%)             │    │
  │ │   :  High Power Consumption (Heat/Throttle)  │    │
  │ └──────────────────────────────────────────────┘    │
  │      │                                               │
  │      ▼ (Raw YUV Frame)                               │
  │ GPU (Render to Display)                              │
  └──────────────────────────────────────────────────────┘

  (B) Present: Hardware Acceleration (VPU Offload)
  ┌──────────────────────────────────────────────────────┐
  │ Storage (HDD/SSD)                                    │
  │      │                                               │
  │      ▼ (Compressed Bitstream)                        │
  │ ┌───────────────────────┐      ┌──────────────────┐ │
  │ │   System RAM (DRAM)   │──────│  CPU (Driver)    │ │
  │ │       Buffer          │      │  - Issue Cmd     │ │
  │ └───────────────────────┘      │  - Sleep (Low %) │ │
  │      ▼                          └──────────────────┘ │
  │ ┌──────────────────────────────────────────────┐    │
  │ │   VPU / Video Codec Engine (ASIC)            │    │
  │ │   ──────────────────────────────────────     │    │
  │ │   [Entropy] -> [IDCT] -> [MC] -> [Filter]    │    │
  │ │   :  Dedicated Logic Gates (Silicon)         │    │
  │ │   :  Minimal Power, Ultra High Speed         │    │
  │ └──────────────────────────────────────────────┘    │
  │      │ (Direct DMA)                                  │
  │      ▼ (Raw YUV Frame)                               │
  │ GPU (Render to Display)                              │
  └──────────────────────────────────────────────────────┘
```
**(해설)** 위 다이어그램은 (A) 소프트웨어 디코딩 방식과 (B) 하드웨어 가속 방식의 데이터 흐름을 비교한 것이다. (A)의 경우 CPU가 주체가 되어 메모리에서 데이터를 읽고 연산을 수행하므로 CPU 부하가 급증하지만, (B)의 경우 CPU는 단순히 명령어(CMD)만 내리고, 실제 데이터 처리는 메모리 버스를 통해 VPU가 담당한다. 이때 **DMA (Direct Memory Access)** 기술을 사용하여 VPU가 직접 메모리를 액세스하므로 연산 중인 CPU의 개입 없이 고속으로 데이터를 전송한다.

> **📢 섹션 요약 비유**: 마치 복잡한 고속도로 톨게이트에서 '요금 정산(CPU)'을 위해 일일이 차량을 세우는 대신, 하이패스 차선(VPU)을 별도로 운영하여 차량이 멈추지 않고 통과하게 하여 전체 도로(시스템)의 정체를 해결하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

비디오 코덱 하드웨어 가속기는 **H.264 (Advanced Video Coding)**, **H.265 (High Efficiency Video Coding)**, **VP9**, **AV1 (AOMedia Video 1)** 등 다양한 표준을 지원하기 위해 파이프라인 형태의 회로를 구성한다.

**구성 요소 (하드웨어 파이프라인 모듈)**

| 모듈명 (Module) | 역할 (Role) | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Entropy Decoder** | 압축된 비트스트림을 해제하여 심볼(Symbol) 복원 | **CABAC (Context-Adaptive Binary Arithmetic Coding)** 또는 **CAVLC** 알고리즘을 하드웨어 유한 상태 기계(FSM)로 구현. 병렬화가 매우 어려움. | 꼬여 있는 실타래를 풀어서 실의 길이를 재는 작업. |
| **Inverse Transform / IQ** | 주파수 영역 데이터를 픽셀 영역 데이터로 역변환 | **IDCT (Inverse Discrete Cosine Transform)** 또는 정수 변환(Integer Transform) 행렬 연산 가속기. | 주파수 신호(음파)를 다시 악보(음표)로 바꾸는 해석기. |
| **Motion Compensation** | 참조 프레임(Reference Picture)에서 블록을 탐색(ME)하여 가져옴 | **SAO (Sample Adaptive Offset)**, DMVR 등의 기술 적용. 외부 **DRAM (Dynamic Random Access Memory)** 대역폭을 가장 많이 소비하는 블록. | 이전에 그린 그림을 오려내어 현재 그림에 붙여넣는 작업. |
| **Intra Prediction** | 현재 프레임 내의 주변 픽셀을 참조하여 예측 | 35가지(H.265)의 예측 모드(Direction)를 하드웨어적으로 지원. | 주변의 색깔을 보고 빈칸을 맞추는 스도쿠 퍼즐. |
| **In-Loop Filter** | 블록 왜곡(Artifact) 제거 및 화질 개선 | **Deblocking Filter**, **SAO**, **ALF (Adaptive Loop Filter)** 등. 디코딩된 픽셀 데이터를 후처리. | 울퉁불퉁한 벽면을 사포질하여 매끄럽게 다듬는 작업. |

**심층 동작 원리: 픽셀 파이프라인**

하드웨어 가속기는 엄격한 파이프라인(Pipeline) 구조를 가진다.
1.  **비트스트림 로딩**: 외부 메모리에서 압축된 비트스트림을 내부 **SRAM (Static Random Access Memory)** 버퍼로 가져옴.
2.  **엔트로피 디코딩**: 비트 단위로 압축된 데이터를 풀어서 변환 계수(Coefficient)와 움직임 벡터(MV)를 추출.
3.  **역양자화 및 변환**: 주파수 계수를 복원하여 픽셀의 잔차(Residual) 신호를 얻음.
4.  **예측 및 보상**: 움직임 벡터를 사용하여 이전 프레임의 해당 블록을 가져오고(재구성), 잔차 신호를 더함.
5.  **루프 필터링**: 블록 경계계를 부드럽게 하고 최종적으로 **YUV (Luminance, Chrominance)** 포맷으로 출력.

이 과정에서 **버퍼 관리(Buffer Management)**가 핵심인데, 참조할 프레임이 필요할 때마다 느린 **DRAM**에 접근하면 속도가 늦어지므로, **타일(Tiling)** 기술을 사용하여 화면을 작은 조각으로 나누어 고속 온칩 메모리(On-chip Memory)에 저장하며 처리한다.

**ASCII 다이어그램: VPU 내부 하드웨어 가속기 구조**

```text
   [VPU Internal Architecture Pipeline]

   Input Bitstream (Compressed)
          │
          ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. Entropy Decoding Engine                               │
  │    (CABAC/CAVLC Decoder)                                 │
  │    Extracts: Coeffs, Motion Vectors, Modes               │
  └───────────────────────┬─────────────────────────────────┘
                          │ (Syntax Elements)
                          ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. Inverse Quantization & Transform (IQ/IDCT)            │
  │    Converts Freq Coeffs -> Spatial Residuals             │
  └───────────────────────┬─────────────────────────────────┘
                          │ (Residuals)
                          ▼
          ┌───────────────────────────────┐
          │                               │
    ┌─────▼─────┐                 ┌──────▼──────┐
    │ Reference  │◀───────────────│   Motion    │
    │ Frame Buf  │  (External DRAM)│ Estimation  │
    │ (DRAM)     │                 │  (IME/FME)  │
    └─────┬──────┘                 └──────┬──────┘
          │ (Predicted Pixels)             │ (Motion Vectors)
          │                               │
          └───────────┬───────────────────┘
                      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. Reconstruction Unit (Add + Clip)                     │
  │    Residual + Prediction = Raw Pixels                    │
  └───────────────────────┬─────────────────────────────────┘
                          │
                          ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. In-Loop Filters (Deblocking / SAO / ALF)             │
  │    Removes Blocking Artifacts                            │
  └───────────────────────┬─────────────────────────────────┘
                          │
                          ▼
                    Raw YUV Frame
              (To Display Controller)
```
**(해설)** 위 다이어그램은 하드웨어 코덱 내부의 데이터 파이프라인을 도식화한 것이다. CPU 코드와 달리 하드웨어는 이 물리적인 흐름을 따라 데이터가 흐르도록 회로가 배선되어 있다. 특히 'Reference Frame Buf'와 'Motion Estimation' 과정에서 외부 DRAM 접근이 빈번하게 발생하는데, 하드웨어는 이를 위해 전용 **Memory Controller**를 내장하여 CPU의 메모리 대역폭과 경쟁하지 않고 독립적으로 최대 대역폭을 사용한다. 이러한 구조적 분리(Decoupling)가 하드웨어 가속이 성능을 내는 핵심 비결이다.

> **📢 섹션 요약 비유**: 자동차 공장의 조립 라인과 같습니다. 엔트로피 디코딩은 '부품 공급', 역변환은 '부품 가공', 움직임 보상은 '조립', 필터링은 '도장' 과정에 비유할 수 있습니다. 이 모든 과정이 컨베이어 벨트 위에서 순차적이고 동시다발적으로(파이프라이닝) 일어나기에 완성차(YUV 프레임)가 쏟아져 나올 수 있습니다.

---

### Ⅲ. 융합 비교 및 다