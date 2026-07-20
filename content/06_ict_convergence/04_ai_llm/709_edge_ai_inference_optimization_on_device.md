---
title: "Edge AI Inference Optimization On-Device"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 709
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 엣지 AI 추론 최적화 온디바이스(On-Device AI Inference Optimization)는 **PTQ(INT8/INT4/FP8)·QAT·가지치기(Structured/Unstructured)·지식 증류·연결 가지치기(Connection Pruning)·NNC(Neural Network Compression) 컴파일러 패스(TVM/MLIR/XLA)**를 결합하여, **NPU/DSP/GPU 이종 가속(예: Snapdragon 8 Gen 3 Hexagon NPU 45 TOPS, Apple A17 Pro 16-core Neural Engine 35 TOPS, Tensor G3 Edge TPU)** 위에서 ResNet-50 기준 224×224 기준 224->1.2ms 추론, 12MB 모델을 3MB로 4배 압축하는 것이 본질이다.
> 2. **가치**: **E2E 지연 10~100ms 이내, 오프라인·데이터 주권 보장(클라우드 왕복 200~800ms 제거), 모바일 디바이스 추론 시 전력 1 inference당 1~10mJ 수준, MLOps 비용 절감(클라우드 GPU 추론 대비 약 70~90% TCO 절감)**, 동시에 1차원 PII(얼굴·음성·위치) 데이터가 디바이스를 떠나지 않아 GDPR/개인정보보호법 컴플라이언스 강화.
> 3. **판단 포인트**: **정확도-지연-메모리-전력 4차원 트레이드오프**, 디바이스별 NPU ISA(Qualcomm Hexagon V73, Apple ANE, ARM Ethos-U85, MediaTek APU 790) 호환성, **Delegate 선택(Android NNAPI/GPU/NNAPI-VK, iOS Core ML + MPSGraph, Windows DirectML)**, OTA 모델 업데이트(메이저 모델 1~2회/년, 경량 patch 4~12회/년), 그리고 발열·쓰로틀링(thermal throttling) 대응까지 7개 결정 변수를 동시 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 중심 AI 추론은 ① **네트워크 지연(latency 200~800ms)**, ② **월 데이터 비용(예: 1일 1억건×2MB 영상 추론 시 6TB/일, 약 5,000만 원/월)**, ③ **개인정보 유출 리스크**, ④ **상시 연결성 의존**, ⑤ **대규모 GPU 인프라 운영비**라는 5대 구조적 한계를 가진다. 특히 **자율주행 ADAS(10ms 이내 결정), 산업용 비전 검사(50ms), AR/VR(20ms 이내 모션-포토), 헬스케어 웨어러블(실시간 ECG/PPG 분석), 스마트 팩토리 PLC 연동** 등 **"결정 주기가 네트워크 RTT보다 짧은"** 도메인에서는 **온디바이스 추론이 필수**다.

2020년 이후 모바일 SoC에 **전용 NPU(Neural Processing Unit)가 보편화**되면서, **Snapdragon 8 Gen 3(45 TOPS INT8), Apple A17 Pro(35 TOPS), Google Tensor G3(Edge TPU 통합), Samsung Exynos 2400(17 TOPS NPU), MediaTek Dimensity 9300(APU 790)** 수준이 일반화되었다. 그러나 클라우드 학습된 **원본 모델(예: ResNet-152 230MB, GPT-2 1.5GB, Whisper-Large 2.9GB)**을 그대로 디바이스에 탑재할 수 없으므로, **"동일 정확도 대비 모델 크기·연산량·전력을 1/10~1/100로 축소"**하는 다층 최적화 파이프라인이 요구된다.

또한 **2024년 Apple Intelligence, Google Gemini Nano(3.25B 파라미터, 4-bit 양자화, 온디바이스 0.7ms/token), Microsoft Phi-3-mini(3.8B, INT4 2.3GB)**, 그리고 **Qualcomm AI Hub, Hugging Face Optimum-ONNX, MediaPipe GenAI** 등 온디바이스 LLM 생태계가 폭발적으로 성장하면서, 단순 CNN 분류를 넘어 **멀티모달 LLM·Diffusion·음성合成(TTS)·실시간 번역**까지 영역이 확장되었다.

```text
+--------------------------------------------------------------------------+
|            Edge AI On-Device Inference Optimization Paradigm           |
+--------------------------------------------------------------------------+
|                                                                          |
|   +---- Cloud-Centric (Legacy) ------+    +---- Edge-Centric (2024+) --+|
|   |                                  |    |                            ||
|   |  [Sensor]                        |    |  [Sensor]                  ||
|   |     |  (raw data 2~50MB/event)   |    |     |  (raw data)          ||
|   |     v                            |    |     v                      ||
|   |  [Device] --upload---> [Cloud]    |    |  [Preprocess]              ||
|   |                                  |    |     |  (DSP, ISP)          ||
|   |   Latency: 200~800ms (RTT)       |    |     v                      ||
|   |   Bandwidth: 5~50GB/day/device   |    |  [Optimized Model]         ||
|   |   Privacy: ❌ PII 노출            |    |     |  INT4/INT8, 3~50MB  ||
|   |   Offline: ❌                     |    |     v                      ||
|   |   GPU cost: $0.0005/1K tokens    |    |  [NPU/DSP Delegate]        ||
|   |                                  |    |     |  < 10ms inference   ||
|   |                                  |    |     v                      ||
|   |                                  |    |  [Postprocess + Action]    ||
|   |                                  |    |                            ||
|   |                                  |    |  Latency: 1~50ms           ||
|   |                                  |    |  Bandwidth: 0 (local)      ||
|   |                                  |    |  Privacy: ✅ (on-device)    ||
|   |                                  |    |  Offline: ✅                ||
|   +----------------------------------+    +----------------------------+|
|                                                                          |
|   ※ 3대 전환 동인: ① SoC NPU 보편화(40+ TOPS)  ② LLM 양자화(4-bit)     |
|                  ③ 프라이버시 규제(GDPR, AI Basic Act, PIPC)             |
+--------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 AI는 "택배로 그림 그려달라고 하는 것"(왕복 며칠), 엣지 AI는 "내 방에 화가가 살고 있는 것"(1초 안에 그려줌). 대신 화가(모델)를 우리 집 냉장고(메모리)에 맞게 슬림화·전문화시켜야 하므로 그 과정이 곧 "추론 최적화"다.

---

## Ⅱ. 아키텍처 및 핵심 원리

엣지 AI 최적화는 **4계층 스택**으로 구성된다: **① Model Optimization Layer(압축·변환) -> ② Compiler/Layer Layer(TVM/MLIR/XLA) -> ③ Runtime/Delegate Layer(TFLite/ONNX RT/CoreML) -> ④ Hardware Acceleration Layer(NPU/DSP/GPU)**. 각 계층은 독립 최적화되며, **상위 계층의 결정이 하위 계층의 효율을 2~10배 좌우**한다.

### 2.1 4계층 엣지 AI 스택 아키텍처

```text
+-------------------------------------------------------------------------+
|                Edge AI On-Device 4-Layer Stack                          |
+-------------------------------------------------------------------------+
|                                                                         |
|  +--------------------------------------------------------------------+ |
|  | L1. Model Optimization (오프라인, 학습 후 1회)                      | |
|  |                                                                    | |
|  |  FP32 원본  --->  PTQ(INT8)  --->  QAT(INT4)  --->  Pruning  --->    | |
|  |  1.2GB      --->   300MB       --->   150MB      --->  sparse     | |
|  |                                                                    | |
|  |  +------------+------------+--------------+------------------+   | |
|  |  | Quantize   | Prune      | Distill      | NNC Compiler     |   | |
|  |  | PTQ/QAT    | Magnitude/ | Teacher->     | TVM, OpenVINO,   |   | |
|  |  | INT8/INT4  | Structured | Student KD   | SNPE, TensorRT   |   | |
|  |  | AWQ/GPTQ   | 2:4/4:8    | + DKD + CRD  | -LLM, AIMET     |   | |
|  |  +------------+------------+--------------+------------------+   | |
|  +--------------------------------------------------------------------+ |
|                                  |                                       |
|                                  v  (변환된 .tflite / .onnx / .mlmodel) |
|  +--------------------------------------------------------------------+ |
|  | L2. Device Compiler & Graph Optimization (디바이스 내 1회 JIT)    | |
|  |                                                                    | |
|  |  +-------------------------------------------------------------+  | |
|  |  | Graph Transform: Constant Folding, Op Fusion, Layout Opt    |  | |
|  |  |   Conv+BN+ReLU  --fuse--->  ConvReLU (1 op)                 |  | |
|  |  |   MatMul+Softmax --fuse---> FusedMatMul                      |  | |
|  |  | Memory Planning:  Activation Reuse, Buffer Sharing          |  | |
|  |  |   peak memory 3GB  --plan--->  800MB (4× 압축)               |  | |
|  |  | Kernel Auto-Tune:  best tile size per NPU core             |  | |
|  |  |   16×16, 32×32, 64×64 후보  --measure--->  32×32 선택       |  | |
|  |  +-------------------------------------------------------------+  | |
|  |                                                                    | |
|  |  대표 컴파일러: Apache TVM(0.18+), MLIR(2024), XLA, Glow,         | |
|  |                Qualcomm AI Engine SDK, ARM Compute Library (ACL)   | |
|  +--------------------------------------------------------------------+ |
|                                  |                                       |
|                                  v  (최적화된 .dlc / .bin / .xmodel)      |
|  +--------------------------------------------------------------------+ |
|  | L3. Runtime & Delegate (디바이스 내 매 추론 호출)                 | |
|  |                                                                    | |
|  |  +-------------------------------------------------------------+  | |
|  |  |  Inference Runtime: TFLite(2.16), ONNX Runtime Mobile,     |  | |
|  |  |  PyTorch Mobile(2.3), Core ML(7.0), Executorch(0.4)        |  | |
|  |  |  LLM Runtime: MediaPipe LLM, llama.cpp, MNN, ExecuTorch     |  | |
|  |  |                                                             |  | |
|  |  |  +--------------+--------------+--------------+            |  | |
|  |  |  | CPU Delegate | GPU Delegate | NPU/DSP     |            |  | |
|  |  |  | XNNPACK      | OpenGL ES    | Vendor SDK  |            |  | |
|  |  |  | 1~3 TOPS     | 30~80 TOPS   | 30~70 TOPS  |            |  | |
|  |  |  | 범용 fallback| float only   | INT4~INT8   |            |  | |
|  |  |  +--------------+--------------+--------------+            |  | |
|  |  |                                                             |  | |
|  |  |  동적 라우팅: 모델 그래프 일부만 NPU, 나머지는 GPU/CPU      |  | |
|  |  |  (예: Softmax는 CPU, Conv는 NPU -> heterogeneous exec)       |  | |
|  |  +-------------------------------------------------------------+  | |
|  +--------------------------------------------------------------------+ |
|                                  |                                       |
|                                  v                                       |
|  +--------------------------------------------------------------------+ |
|  | L4. Hardware Acceleration (물리 계층)                              | |
|  |                                                                    | |
|  |  +-----------------+------------------+----------------------+   | |
|  |  | NPU (MAC array) | DSP (vector)     | GPU (shader)         |   | |
|  |  | systolic        | Hexagon V73      | Adreno 750           |   | |
|  |  | 4096 MACs/cycle | 1024 MACs/cycle  | 2048 ALUs            |   | |
|  |  | 1 TOPS/W        | 0.3 TOPS/W       | 0.5 TOPS/W           |   | |
|  |  | INT4~INT16      | INT8~FP16        | FP16~FP32            |   | |
|  |  | Apple ANE       | Qualcomm Hexagon | Mali, Adreno         |   | |
|  |  | Snapdragon Hex  | MediaTek APU