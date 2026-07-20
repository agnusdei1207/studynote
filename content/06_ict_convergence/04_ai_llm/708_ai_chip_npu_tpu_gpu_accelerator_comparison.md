---
title: "AI Chip NPU TPU GPU Accelerator Comparison"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 708
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI 가속기는 **SIMD/SIMT/Systolic Array**라는 세 가지 핵심 연산 패러다임으로 분류되며, GPU(SIMT/SIMD, 범용 병렬), NPU(텐서/벡터 엔진, 추론 특화), TPU(Systolic Array + HBM, 데이터센터 학습/추론)가 각각 다른 워크로드에 최적화된 **메모리 대역폭과 연산 밀도(TOPS/W)의 트레이드오프**로 설계된다.
> 2. **가치**: 동일 전력 대비 GPU 대비 NPU는 **5~15배**, TPU v5e 대비서는 **2~3배**의 에너지 효율(TOPS/W)을 달성하며, 엣지 NPU는 실시간성(<10ms latency)과 개인정보 비휘발성 추론으로 클라우드 GPU 의존도를 탈피하는 **온디바이스 AI** 시대를 가능케 한다.
> 3. **판단 포인트**: **메모리 계층(레지스터->SRAM->DRAM/HBM) 병목**, **데이터 재사용률(data reuse ratio)**, **희소성(sparsity) 활용도**, **지원 프레임워크 생태계(TensorRT/XLA/Core ML)**가 칩 선정의 4대 핵심 변수이며, 학습(throughput-oriented) vs 추론(latency-oriented) 목적에 따라 아키텍처 선택이 완전히 달라진다.

---

## Ⅰ. 개요 및 필요성

2012년 AlexNet이 GPU(CUDA)로 학습 가속을 증명한 이래, 딥러닝 모델 파라미터는 **2년마다 10배**(예: GPT-3 175B -> GPT-4 1.8T)로 성장해 왔으나, 무어의 법칙(매 2년 트랜지스터 2배)에 따른 연산 능력 증가는 정체기에 진입했다. 이로 인해 **메모리 월(Memory Wall)** 현상이 가속화되어, 2024년 기준 GPT-4 추론 1회당 약 200~500 TFLOPS, 학습 1회당 수십 PFLOPS가 요구되며, 전력 한계(데이터센터 GPU는 H100 단일 700W, B200 1000W) 때문에 **도메인 특화 아키텍처(DSA, Domain-Specific Architecture)**로의 전환이 불가피해졌다.

```text
+------------------------------------------------------------------+
|        AI 연산 수요 폭증 vs 무어의 법칙 정체 (Memory Wall)        |
+------------------------------------------------------------------+
|                                                                  |
|  모델 파라미터(FLOPS 요구량)            하드웨어 FLOPS            |
|        ^                                    ^                   |
|   10x  |   ╱--- 모델은 6개월마다 2배 성장   |   ╱-- 4년에 2배     |
|        |  ╱                                |  ╱  (덴나드 스케일링)|
|   1.0x |-╱-------------------------------- |-╱----------------  |
|        +------------------------------------+--------------►     |
|              2012  2016  2020  2024  2026                        |
|                                                                  |
|  결과: 범용 CPU로는 불가능 -> 도메인 특화 가속기(ASIC/ASSP) 등장  |
|  +--------+  +--------+  +--------+  +--------+                 |
|  |  CPU   |  |  GPU   |  |  NPU   |  |  TPU   |                 |
|  |범용제어|  |병렬연산|  |텐서전용|  |행렬전용|                 |
|  |4~16코어|  |1000+CU |  |MAC array| |Systolic|                 |
|  +--------+  +--------+  +--------+  +--------+                 |
+------------------------------------------------------------------+
```

**기존 패러다임(CPU 중심)** 은 명령어 디코딩, 분기 예측, 캐시 일관성 유지에 트랜지스터의 60% 이상을 소모하여 실제 부동소수점 연산(ALU)에는 일부만 투입된다. 반면 **AI 가속기 패러다임** 은 텐서(행렬) 연산의 규칙성, 데이터 재사용, 낮은 정밀도(INT8/FP8) 허용을 활용해 **행렬 곱셈 유닛(MXU)** 비중을 80% 이상으로 끌어올린 **Compute-centric Design** 이다. 이는 동일 7nm/5nm 공정 면적 대비 10~100배의 AI 처리량을 달성한다.

- **📢 섹션 요약 비유**: CPU가 "한 사람이 한 줄씩 공책에 계산하는 것"이라면, GPU는 "교실 100명이 각자 다른 문제 푸는 것", NPU는 "주방에서 칼질만 100명이 동시에 하는 것", TPU는 "컨베이어 벨트 위로 숫자가 흘러가며 1초에 1만 개 곱셈이 끝나는 공장"입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------------+
|            AI 가속기 통합 아키텍처 (Host + Device 계층)                 |
+------------------------------------------------------------------------+
|                                                                        |
| +--- Host (CPU, x86/ARM) ----------------------------------------+    |
| |  App -> Runtime(TensorRT/XLA/Core ML) -> Driver -> PCIe/CXL/NVLink|    |
| +-------------------------------+----------------------------------+    |
|                                 | DMA, MMIO, Command Queue            |
| +-----------------------------v----------------------------------+    |
| |              Device: AI 가속기 내부 구조                          |    |
| | +----------+  +----------+  +----------+  +----------+         |    |
| | |Global    |  | L2 Cache |  | L1/SRAM  |  | Register |         |    |
| | |Memory    |  | 40~80MB  |  | per SM   |  | File     |         |    |
| | |HBM3/3e   |  |          |  | 192KB    |  | 64KB/SM  |         |    |
| | |80~155GB  |  |          |  |          |  |          |         |    |
| | +----+-----+  +----+-----+  +----+-----+  +----+-----+         |    |
| |      +--------------+--------------+--------------+              |    |
| |                            | (메모리 계층)                       |    |
| | +--------------------------v---------------------------+        |    |
| | |           Compute Fabric: 1~200+ Compute Units         |       |    |
| | |  +---------+ +---------+ +---------+ +---------+     |        |    |
| | |  |   SM    | |   SM    | |   SM    | |   SM    |... |        |    |
| | |  |CUDA-Core| |Tensor   | |Tensor   | |Tensor   |     |        |    |
| | |  |(FP32)  | |Core(INT8| |Core(INT8| |Core(INT8|     |        |    |
| | |  |  64EA  | |/FP16)   | |/FP16)   | |/FP16)   |     |        |    |
| | |  |        | | 4세대    | | 4세대    | | 4세대    |     |        |    |
| | |  +---------+ +---------+ +---------+ +---------+     |        |    |
| | |  Warp Scheduler(4개/SM) -> Tensor Core로 dispatch        |       |    |
| | +---------------------------------------------------------+        |    |
| |  Special: TPU는 SM 대신 Systolic Array (128x128 MAC) 단일 칩         |    |
| |  Special: NPU는 Vector Engine + Matrix Engine + DMA 분산 배치       |    |
| +--------------------------------------------------------------------+    |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Host CPU + Runtime** | 그래프 컴파일, 작업 분할, 메모리 핀(pin), 비동기 스트림 관리 | CUDA Toolkit, TensorRT-LLM, XLA(Accelerated Linear Algebra), OpenVINO, Core ML, ONNX Runtime; 0.1~10ms 단위 latency 예산 결정 |
| **PCIe Gen5/Gen6 / NVLink / CXL** | Host↔Device 데이터 전송 (양방향 DMA) | PCIe Gen5 x16 = 128GB/s(单向), NVLink 4(72GB/s/Link, 18Link), CXL 3.0 메모리 공유로 **가중치 prefetch** 최적화 |
| **Global Memory (HBM2e/3/3e, LPDDR5X)** | 모델 파라미터·활성값 저장, 80~192GB 용량, 3~5TB/s 대역폭 | HBM3e 12-Hi 스택(예: H200 141GB, B200 192GB), 6.4TB/s; LPDDR5X는 8.5Gbps(엣지 NPU), 51.2GB/s |
| **Compute Unit (SM/CU/PE)** | 행렬·벡터·스칼라 연산을 병렬 실행 | NVIDIA SM(Hopper 132개/SM, FP8 Tensor 4세대), AMD CDNA3(CU+Matrix Core), TPU MXU(128x128 Systolic), NPU MAC array(예: Apple ANE 16-core × 16 MAC lanes) |
| **Tensor Core / Matrix Engine / MXU** | 4×4~128×128 행렬 곱셈을 한 사이클에 처리 | **WMMA/MMA PTX intrinsic** 사용, FP16·BF16·TF32·FP8·INT8·INT4 혼합 정밀도(MX Format: E2M1, E4M3) 지원 |
| **Interconnect (NVLink, ICI, NVSwitch)** | 다중 가속기 간 all-reduce, tensor parallel 통신 | NVLink 4.0: 900GB/s 양방향, NVSwitch 3.0: 64-port; **NVLink Network**로 256 GPU 클러스터(HGX Baseboard) 구성 |

**핵심 원리**: 모든 AI 가속기의 중심에는 **General Matrix Multiply (GEMM)** 가속이 있다. Transformer의 Attention은 `Q×K^T`(B,h,n,d × B,h,n,d -> B,h,n,n), FFN은 `X×W1`(B,n,d × d,4d)로 환원되며, 이를 처리하기 위해 **타일 기반(Tiled) 행렬 곱**이 사용된다. NVIDIA의 Tensor Core는 16×16×16 행렬 타일을 warp 단위로 처리하고, **Tensor Memory Accelerator(TMA, Hopper)** 는 다차원 데이터 복사를 비동기로 처리해 **메모리 대역폭의 80% 이상을 실효 처리량**으로 끌어올린다. TPU의 **Systolic Array** 는 데이터가 칩 내부에서 파이프라인처럼 흘러가며 128×128 MAC을 1사이클에 완료해, 외부 메모리 접근 없이 **arithmetic intensity(연산/메모리 비율)** 를 극대화한다. NPU는 **Winograd convolution**, **sparsity pruning(2:4)**, **채널별 양자화(per-channel INT8)** 등 추론 전용 최적화를 적용한다.

- **📢 섹션 요약 비유**: Systolic Array는 "수도꼭지에서 물이 떨어지듯 행렬 데이터가 칩 안으로 흘러가며 자동으로 곱셈·누적이 일어나는 컨베이어 벨트"이고, Tensor Core는 "32명이 마라톤 relay처럼 4×4 행렬을 한 사이클에 동시에 처리하는 릴레이 팀"입니다.

---

## Ⅲ. 비교 및 연결

### 가속기별 상세 비교 (2024~2025 기준)

| 구분 | **NVIDIA GPU (H100/B200)** | **Google TPU (v5e/v5p/v6 Trillium)** | **Apple NPU (ANE, M4)** | **Qualcomm Hexagon NPU** |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | SIMT (Warp 32 thread) + 4세대 Tensor Core | Systolic Array (128×128 MXU) + Vector Unit | Neural Engine (16-core, 16-lane MAC) + AMX | Hexagon V79 (4개 Wide Vector, Scalar + Matrix) |
| **정밀도** | FP64~FP4 (FP8, INT4, FP6 지원) | BF16, INT8, FP8 (Trillium) | FP16, INT8 (추론 위주) | INT8, INT16, FP16 |
| **피크 성능** | H100: 989 TFLOPS(FP8), B200: 2.25 PFLOPS(FP4) | v5e: 197 TFLOPS(BF16/칩), Trillium: 925 TFLOPS(FP8) | M4 Max: 38 TOPS(INT8) | Snapdragon 8 Gen 4: 45 TOPS(INT8) |
| **메모리** | HBM3 80GB (3.35TB/s), B200 HBM3e 192GB (8TB/s) | HBM2 16~32GB(v5e), HBM3 95GB(v5p) | 통합 LPDDR5X 128~192GB (501GB/s, UMA) | LPDDR5X 16~24GB (77GB/s) |
| **소모 전력** | H100 SXM: 700W, B200 SXM: 1000W | v5e: ~200W, Trillium: ~400W | M4 Max SoC 전체 ~50W (ANE만 ~10W) | Hexagon NPU 단독 ~5W |
| **TOPS/W** | ~1.4 (H100), ~2.2 (B200) | ~0.98 (v5e), ~2.3 (Trillium) | ~3.8 (M4 Max) | ~9.0 (Snapdragon 8 Gen 4) |
| **프레임워크** | CUDA, cuDNN, TensorRT, Triton, TensorRT-LLM | JAX, TensorFlow, PyTorch(XLA), Flax | Core ML, MLX, ONNX (제한) | Qualcomm AI Engine SDK, SNPE, ONNX |
| **확장성** | NVLink 256 GPU, NVL72 Rack-scale | 4096-chip **TPU v4 Pod** (v5p: 8960 chip), Optical OCS | Apple Silicon 1칩 (Mac Studio/Ultra) | 모바일 1칩 (Soc 내부) |
| **주 사용처** | 범용 학습·추론, LLM/HPC | Google Cloud TPU(자사 LLM, Gemini) | Mac/iPad 온디바이스 ML | 스마트폰·XR·자동차 추론 |

### 한눈에 보는 설계 철학 비교

| 구분 | **GPU** | **NPU** | **TPU** | **CPU** |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 최적화 대상** | 범용 병렬 + AI 확장 | 엣지 추론(전력/지연) | 데이터센터 학습·추론 | 순차·제어 로직 |
| **메모리 전략** | 대역폭 우선 (HBM, 캐시) | 에너지 우선 (LPDDR, on-chip SRAM) | 데이터 재사용 우선 (Systolic) | 캐시 일관성 우선 |
| **정밀도** | FP4~FP64 광범위 | INT8/INT4 중심 | BF16/INT8/FP8 | FP32/INT64 |
| **프로그래밍 모델** | SIMT (CUDA thread) | Operator-level (TFLite delegate) | XLA 컴파일 (graph-level) | SISD/MIMD |
| **지연 시간** | 수십 μs~수 ms | 1~10 ms (실시간) | 수 ms~수백 ms (배치) | 수십 ns~수 μs |
| **확장 단위** | 노드(8 GPU)->랙(72/256) | 디바이스 단위 (보드) | Pod (수천 칩)