---
title: "AI Inference Optimization TensorRT ONNX"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 659
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ONNX(Open Neural Network Exchange)는 프레임워크 비종속 모델 교환을 위한 **프로토콜 버퍼 기반 중간 표현(Intermediate Representation, IR)** 표준이며, TensorRT는 NVIDIA GPU의 CUDA/SM(Streaming Multiprocessor)·Tensor Core 자원에 **Layer Fusion·Kernel Auto-Tuning·FP16/INT8 Quantization**을 자동 적용하는 **추론 전용 런타임 컴파일러**입니다. 두 기술은 `PyTorch/TensorFlow/JAX -> ONNX Export -> TensorRT Engine(plan)` 파이프라인으로 결합되어, 학습-배포 간 의미적·구조적 격차를 해소합니다.
> 2. **가치**: 동일 하드웨어 대비 ResNet-50 기준 **FP32 -> FP16 변환 시 약 2.0배, INT8 캘리브레이션 적용 시 약 3.7배 지연시간 감소**(NVIDIA A100 기준, TensorRT 8.6), GPU 메모리 footprint **최대 50% 절감**, 그리고 BERT-Large 같은 Transformer 모델에서는 **최대 18배의 추론 가속**(Sparsity + INT8) 효과를 검증할 수 있어, TCO(Total Cost of Ownership)와 SLA 동시 만족이 가능합니다.
> 3. **판단 포인트**: 핵심 의사결정 축은 ①**정확도-성능 트레이드오프**(INT8 캘리브레이션의 KL Divergence 손실 한계), ②**Dynamic Shape 지원 범위**(최적화된 engine이 고정 shape에 특화되는 특성), ③**NVIDIA 종속성**(AMD/Intel CPU·GPU에서는 ONNX Runtime 또는 OpenVINO 선택), ④**Calibration Dataset의 통계적 대표성**(입력 분포 왜곡 시 정확도 급락), ⑤**Triton Inference Server 연동 시 동적 Batching·Multi-Model Ensemble·Model Repository 관리 전략**입니다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델은 학습(training) 단계에서 PyTorch·TensorFlow·JAX·PaddlePaddle 등 다양한 프레임워크 위에서 개발되지만, **운영(Production) 환경에서는 학습 프레임워크의 무거운 의존성(예: PyTorch+CUDA Toolkit+cuDNN+Python Interpreter 4GB+)과 동적 그래프 특성으로 인해 GPU 자원 활용률이 30~40%에 그치는 'GPU Starvation' 현상**이 빈번합니다. 또한 동일 모델을 다수의 프레임워크·다수의 하드웨어(데이터센터 A100, 엣지 Jetson Orin, 차량용 Drive Orin)에 배포해야 하는 **모델 배포의 파편화(Fragmentation)** 문제가 발생합니다.

`ONNX`는 2017년 Facebook·Microsoft가 시작한 오픈 표준으로, **`.onnx` 파일 단일 포맷으로 모델의 Computational Graph(연산 그래프), 가중치 텐서, 메타데이터를 직렬화**하여 프레임워크 간 손실 없는 변환을 보장합니다. 연산자 사양(Operator Spec)은 `opset_version`을 통해 진화(현재 v20)하며, 200여 개의 표준 연산자와 Custom Op 확장 메커니즘을 제공합니다.

`TensorRT`는 NVIDIA가 2017년(당시 이름: TensorRT 1.0) 출시한 SDK로, 학습된 모델을 **NVIDIA GPU 하드웨어 명령어(PTX/SASS)에 최적화된 직렬화된 엔진 파일(`engine.plan` 또는 `engine.trt`)**로 변환합니다. 핵심 최적화는 ①**Vertical Layer Fusion**(Conv+BN+ReLU 통합), ②**Horizontal Layer Fusion**(동일 입력의 다중 branch 통합), ③**Kernel Auto-Tuning**(입력 shape별 최적 CUDA kernel 탐색), ④**Precision Calibration**(FP32->FP16/INT8/FP8), ⑤**Memory Pool Reuse**(텐서 메모리 사전 할당)입니다.

```text
        [학습 단계: Model Development]                  [배포 단계: Inference Optimization]
  +------------------------------+             +---------------------------------------+
  |  PyTorch (torch.export)      |             |  NVIDIA TensorRT (Closed Loop)        |
  |  TensorFlow (SavedModel)     |  -ONNX--->  |  - Graph Optimization (Layer Fusion)  |
  |  JAX (jax2tf -> onnx)         |   Export   |  - Kernel Auto-Tuning (cuDNN/cuBLAS) |
  |  PaddlePaddle (paddle2onnx) |             |  - Precision: FP32/FP16/INT8/FP8     |
  |  Hugging Face Optimum-ONNX  |             |  - Memory: Static Pool + Reuse        |
  +------------------------------+             |  - Output: .plan (Engine File)        |
            |                                  +------------+--------------------------+
            |                                               | loadEngine()
            |                                               v
            |                                  +----------------------------+
            |                                  |  TensorRT Runtime (C++/Py) |
            |                                  |  - execute_async()         |
            |                                  |  - GPU Stream 비동기 실행 |
            |                                  |  - DLA(Deep Learning      |
            |                                  |    Accelerator) 오프로드  |
            |                                  +------------+---------------+
            |                                               | gRPC/HTTP
            |                                               v
            |                                  +----------------------------+
            |                                  |  Triton Inference Server   |
            |                                  |  - Dynamic Batcher         |
            |                                  |  - Model Ensemble          |
            |                                  |  - Multi-GPU/Multi-Node   |
            |                                  +----------------------------+
            v
  +------------------------------+
  |  ONNX Runtime (Fallback)     |  <--- Cross-Platform: x86 CPU, ARM, Mali, NNAPI
  |  - DirectML / CUDA / CPU EP  |      AMD ROCm, Apple CoreML, Qualcomm QNN
  |  - Graph Optimization        |
  +------------------------------+
```

**기존 패러다임 대비 변화**:
- **Before (2016 이전)**: Caffe `.prototxt` + `.caffemodel` -> 프레임워크 종속, GPU 활용률 30%대
- **After (2017 이후)**: PyTorch `state_dict` -> ONNX -> TensorRT engine -> GPU 활용률 70~95%, A100에서 10,000 QPS 달성
- **현재 (2024~)**: TensorRT-LLM, NeMo, NIM(NVIDIA Inference Microservice)으로 LLM 추론 최적화 영역 확장

- **📢 섹션 요약 비유**: ONNX는 **"전 세계 모든 요리사가 공용으로 쓸 수 있는 표준 레시피 카드"**이고, TensorRT는 **"그 레시피를 NVIDIA 주방의 화덕(GPU)에 맞춰 자동으로 불 세기와 칼질까지 최적화하는 5스타 셰프"**입니다. 같은 '라면' 레시피(모델)도 일반 가스레인지(CPU)와 화덕(TensorRT)에서는 조리 시간과 풍미가 완전히 달라지죠.

---

## Ⅱ. 아키텍처 및 핵심 원리

TensorRT의 추론 최적화 파이프라인은 크게 **5단계**로 구분되며, 각 단계에서 비가역적(irreversible) 변환이 수행됩니다.

```text
                +----------------------------------------------------------+
                |              TensorRT Optimization Pipeline               |
                +----------------------------------------------------------+
                                       |
   [1] Model Parsing                  [2] Network Definition
   +------------------+               +------------------------------------+
   |  .onnx (Model)   |  --parse--->  |  INetworkDefinition* network      |
   |  .pb (TF)        |               |  - Layer 등록 (Conv, MatMul, ...)  |
   |  .uff (legacy)   |               |  - Input/Output Tensor Shape 명시  |
   +------------------+               |  - Dynamic Shape Profile 설정     |
                                      +--------------+---------------------+
                                                     | addPooling
                                                     v
   [3] Builder Configuration         [4] Engine Build (수 분~수십 분)
   +---------------------------------+ +------------------------------------+
   | IBuilderConfig* config          | | ① Layer Fusion                    |
   |  - max_workspace_size = 8GB     | |    Conv+BN+ReLU -> ConvBnRelu       |
   |  - fp16 = true                  | |    MatMul+Add+GeLU -> FusedMatMul   |
   |  - int8 = true                  | | ② Kernel Auto-Tuning              |
   |  - int8_calibrator = Entropy    | |    [Conv k=3 s=1 pad=1, H×W=224]  |
   |  - sparse_weights = true        | |      -> 1024개 후보 중 SM 점유율 최적|
   |  - tactic_source = CUBLAS,     | | ③ Tensor Memory Layout Reorder    |
   |    CUDNN, CUBLASLT, etc.        | |    NCHW -> NHWC (Tensor Core 친화) |
   |  - DLA_core = -1 (GPU only)    | | ④ Constant Folding                |
   +---------------------------------+ | ⑤ Dynamic Shape: Min/Opt/Max Profile|
                                      |    등록된 profile 내에서만 최적화   |
                                      +--------------+---------------------+
                                                     | buildSerializedNetwork()
                                                     v
   [5] Deserialized Engine & Runtime
   +----------------------------------------------------------------------+
   |  ICudaEngine* engine = deserializeCudaEngine(plan_bytes);          |
   |  IExecutionContext* ctx = engine->createExecutionContext();         |
   |                                                                      |
   |  +-----------------+    +------------------+    +--------------+  |
   |  |  Host Memory    |    |  Device Memory   |    |  Async Stream |  |
   |  |  (Pinned DMA)   | --> |  - Input Buffer  |    |  cudaStream_t |  |
   |  |  Input Tensor   |    |  - Output Buffer | --->|  execute_async |  |
   |  |  Output Tensor  | <-- |  - Internal Pool | <---|  (V100/A100/H100)|
   |  +-----------------+    +------------------+    +--------------+  |
   |                                                                      |
   |  ※ Pinned Memory: cudaHostAlloc(Mapped) -> H2D/D2H 전송 2배 빠름    |
   |  ※ Stream: GPU 내 동시성, 다중 stream으로 입력-추론-출력 오버랩     |
   +----------------------------------------------------------------------+
```

**Layer Fusion의 상세 메커니즘**:
- **Conv-BN-Add-ReLU Fusion**: Convolution의 bias와 BatchNorm의 scale·shift·epsilon을 Conv weight에 **수학적 동치(Equivalence)** 변환으로 흡수. `W_fused = γ·W/σ`, `b_fused = γ·(b-μ)/σ + β`. 이렇게 통합된 단일 CUDA 커널은 **메모리 접근 횟수 4회 -> 1회, 커널 launch overhead 4회 -> 1회**로 줄어 latency가 대폭 감소합니다.
- **Q/DQ (Quantize-Dequantize) Node 삽입**: INT8 변환 시 Conv 입력에 `QuantizeLinear`, 가중치에 `DequantizeLinear` 노드가 자동 삽입되며, 이는 추후 `QDQ` 형식(ONNX Runtime Quantization과 호환)으로 캘리브레이션됩니다.

**Precision Calibration 알고리즘**:
- **Entropy Calibration (Default)**: KL Divergence를 최소화하는 threshold T를 탐색 -> 활성화 분포의 상위 99.99%를 255개 bin에 매핑
- **MinMax Calibration**: 단순 min/max -> 빠른 대신 정확도 손실 큼
- **Percentile Calibration**: 99.9% percentile 사용 -> outlier에 강건

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ONNX Graph (Proto)** | 프레임워크 비종속 모델 표현 | `onnx.proto` 스키마 기반 protobuf 직렬화, `ir_version`/`opset_import`/`graph.initializer`(가중치) 포함. `onnx.checker.check_model()`로 사양 적합성 검증 |
| **TensorRT Builder** | 최적화 그래프 -> Engine 변환 | `IBuilder::buildSerializedNetwork()` 호출 시 위 5단계 자동 수행. **빌드 시간은 수 분~수십 분**(최적 tactic 조합 탐색 때문), 한 번 빌드 후 engine 직렬화하여 재사용 |
| **TensorRT Engine (plan)** | 직렬화된 GPU 실행 계획 | `.plan` 파일은 하드웨어·TensorRT 버전·GPU 모델에 **강하게 종속**(A100용 engine은 V100에서 실행 불가). IExecutionContext가 상태(state) 보관 -> **각 context는 단일 thread**로 사용해야 함(Safe하지 않음) |
| **Calibrator (INT8)** | FP32 -> INT8 스케일 팩터 산출 | `IInt8EntropyCalibrator2` 구현 시 `getBatch()`로 calibration batch 반환 -> 내부적으로 activation histogram 누적 -> `computeCalibrationScores()`에서 KL Divergence 최소화. **Calibration Data는 학습 데이터의 1~5%**(500~2000 샘플)면 충분 |
| **Polygraphy (Toolkit)** | 엔진 검증·디버깅 | `polygraphy run model.onnx --trt --save-engine=plan`로 변환, `polygraphy run plan --validate`로 FP32/INT8 결과 비교(최대 1e-3 atol), `inspect` 명령으로 layer별 tactic dump 가능 |
| **Triton Inference Server** | 다중 모델 서빙·라우팅 | TensorRT backend로 engine 로드, Dynamic Batcher(예: 5ms window 내 최대 batch_size=32), Model Ensemble(전처리-TensorRT-후처리 파이프라인), Prometheus 메트릭 노출 |

**핵심 파라미터 (BuilderConfig)**:

```python
config = builder.create_builder_config()
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 8 << 30)  # 8GB
config.set_flag(trt.BuilderFlag.FP