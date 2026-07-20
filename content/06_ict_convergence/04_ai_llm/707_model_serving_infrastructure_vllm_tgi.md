---
title: "Model Serving Infrastructure vLLM TGI"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 707
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: vLLM은 PagedAttention을 통해 KV Cache를 OS 페이징처럼 비연속적 블록(Block)으로 관리하여 메모리 파편화를 제거하고, TGI(HuggingFace)는 Rust 기반의 async runtime(Tokio) 위에 tensor parallelism과 Flash Attention을 결합해 안정적인 처리량을 보장하는 LLM 추론 전용 서빙 프레임워크다.
> 2. **가치**: Static batching 대비 14~24배 처리량(throughput) 향상, GPU 메모리 utilization 90% 이상 달성, p99 latency 50% 절감, TTFT(Time-To-First-Token) 200ms 이하 유지가 가능해 동일 H100 8-GPU 노드 기준 동시접속 1,000+ 세션 처리가 현실화된다.
> 3. **판단 포인트**: `vLLM ↔ TGI` 선택은 워크로드 특성(다중 LoRA/prefix 공유 vs. 단순 text generation), `max_num_seqs·max_model_len·gpu_memory_utilization` 튜닝, 양자화 전략(AWQ/GPTQ/FP8), 그리고 speculative decoding 도입 여부에 따라 결정되며, 단일 모델·고지연 환경 vs. 멀티테넌트·저지연 환경의 trade-off를 정확히 분리해 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

LLM(Large Language Model) 서빙은 전통적인 웹 서비스와 근본적으로 다른 특성을 갖는다. (1) **Compute-bound** 단계(prefill)와 **Memory-bound** 단계(decode)가 동일 request 내에서 공존하고, (2) 각 request의 output token 수는 예측 불가(1~4,096 tokens)하여 batch 내 finish time 편차가 극심하며, (3) autoregressive decoding은 본질적으로 sequential하므로 GPU utilization이 떨어진다. 기존 `HuggingFace Transformers + FastAPI` 조합은 request를 순차적으로 처리하거나 naive padding 기반 static batching을 사용해 GPU SM(Streaming Multiprocessor) 점유율이 30~40%에 그쳤다.

vLLM(Kwon et al., SOSP'23)과 TGI(HuggingFace, 2022~)는 이러한 문제를 해결하기 위해 등장한 **추론 전용(inference-specialized) 서빙 시스템**이다. vLLM은 Berkeley에서 학계 중심의 연구 결과로 PagedAttention을 도입했고, TGI는 production-grade 안정성과 HuggingFace 모델 생태계 통합에 강점을 가진다. 두 시스템 모두 **continuous batching(continuous-batching·in-flight batching)**, **Paged KV Cache**, **FlashAttention-2**, **CUDA Graph capture**를 핵심 기법으로 채택한다.

기존 paradigm은 "request 단위 batch"였으나, 새로운 paradigm은 "**token 단위 batch + iteration-level scheduling**"이다. 이는 OS의 preemptive multitasking과 유사하며, GPU가 한 번에 처리하는 단위가 request가 아니라 token sequence 전체의 forward pass iteration이 된다.

```text
+------------------------------------------------------------------+
|          기존 Static Batching vs. Continuous Batching            |
+------------------------------------------------------------------+
|                                                                  |
|  [Static Batching - 기존]                                        |
|  +---- req1 [████████]██████████████████████░░░░░░░░░░░░░░░░░░░ | <- 짧은 답    |
|  |  req2 [██]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ | <- padding 낭비|
|  |  req3 [████████████████████████]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ | <- 중간       |
|  |  GPU: ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ | <- idle 큼   |
|  +--------------------------------------------------------------|
|  문제: 짧은 요청도 가장 긴 요청이 끝날 때까지 GPU 낭비 (O(n) tail)|
|                                                                  |
|  [Continuous Batching - vLLM/TGI]                                |
|  Iter 1: [req1(req2)(req3)               ]   <- 모두 prefill      |
|  Iter 2: [tok1,tok1,tok1   ]               <- 1st decode token  |
|  Iter 3: [tok1,tok1,tok1   ]               <- 2nd decode token  |
|  Iter 4: [--- ,tok1,tok1   ]               <- req1 종료, req4 진입|
|  Iter 5: [--- ,tok1,tok1,tok1]             <- new req 즉시 합류  |
|  GPU:   [████████████████████]            <- 100% 활용           |
|  효과: tail latency 제거, 처리량 14~24×, TTFT 안정               |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 기존 static batching은 "한 버스에 손님 30명이 타면 가장 먼 손님이 내릴 때까지 전원 대기"하는 것이고, continuous batching은 "각 손님이 내리는 즉시 새로운 손문이 탄다"는 일본의 **Belt Conveyor(회전초밥)** 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. vLLM 내부 아키텍처 (PagedAttention 중심)

```text
+---------------------------------------------------------------------+
|                       vLLM System Architecture                      |
+---------------------------------------------------------------------+
|                                                                     |
|  +------------------+   +-----------------+   +------------------+ |
|  |  OpenAI-Compatible|   |   Async LLM     |   |  Scheduler       | |
|  |  API Server       |◄--+   Engine        |◄--+  (FCFS/SJF/VLLM) | |
|  |  (FastAPI+uvicorn|   |  (ray/asyncio)  |   |  - Chunked Prefill| |
|  +--------+---------+   +--------+--------+   |  - Preemption    | |
|           |                      |             +---------+--------+ |
|           | token streaming      |                       |          |
|           v                      v                       v          |
|  +--------------------------------------------------------------+   |
|  |            BlockManager (PagedAttention Core)                |   |
|  |  +---------+ +---------+ +---------+ +---------+            |   |
|  |  |Block 0  | |Block 1  | |Block 2  | |Block 3  |  ...       |   |
|  |  |seq A[0:7]| |seq A[8:15]| |seq B[0:7]| |seq C[0:7]|          |   |
|  |  +---------+ +---------+ +---------+ +---------+            |   |
|  |  Block Size: 16 tokens (default), fixed-size pages           |   |
|  |  Block Table: seq->[blk3, blk1, blk7, ...] (logical->phys)     |   |
|  +--------------------------------------------------------------+   |
|                              |                                      |
|                              v                                      |
|  +--------------------------------------------------------------+   |
|  |   Worker (per-GPU, Ray actor)                                |   |
|  |   +----------------+  +----------------+  +---------------+  |   |
|  |   |  Model Runner   |  | CUDA Graph     |  | Attention    |  |   |
|  |   |  (forward pass) |  | (capture/replay)|  |  Backend:    |  |   |
|  |   |                 |  |                 |  |  FLASHINFER |  |   |
|  |   |                 |  |                 |  |  FLASH_ATTN |  |   |
|  |   |                 |  |                 |  |  XFORMERS   |  |   |
|  |   +----------------+  +----------------+  +---------------+  |   |
|  |   Parallel: TP(within node) + PP + DP + EP (MoE)             |   |
|  +--------------------------------------------------------------+   |
|                              |                                      |
|                              v                                      |
|            +------------------------------+                         |
|            |  GPU 0,1,2,3 (A100/H100)     |                         |
|            |  KV Cache: ~80% VRAM         |                         |
|            |  Weights:  ~15% VRAM         |                         |
|            |  Workspace: ~5%              |                         |
|            +------------------------------+                         |
+---------------------------------------------------------------------+
```

### 2. PagedAttention 동작 원리

PagedAttention은 OS의 **virtual memory paging**을 KV Cache 관리에 적용한 것이다.

- **물리 블록(Physical Block)**: GPU 메모리 상의 고정 크기(보통 16 tokens) contiguous chunk
- **논리 블록(Logical Block)**: sequence의 토큰 위치에 대응되는 가상 주소
- **Block Table**: sequence ID -> 물리 블록 배열의 매핑 테이블 (per-request)
- **Copy-on-Write(CoW)**: parallel sampling, beam search에서 동일 prefix를 공유할 때 block ref-count로 중복 저장 회피

이 구조로 인해:
1. **내부 단편화(internal fragmentation)**이 `block_size` (16 tokens) 이하로 제한됨
2. **외부 단편화(external fragmentation)**이 0 (모든 block 동일 크기)
3. 메모리 utilization 4~8% 낭비 -> **55% -> 90%+**로 향상

### 3. TGI(HuggingFace Text Generation Inference) 아키텍처

TGI는 **Rust + actix-web**으로 작성되어 Python GIL의 한계를 우회한다.

```text
+--------------------------------------------------------------------+
|                  TGI (Text Generation Inference) v3.x              |
+--------------------------------------------------------------------+
|  Client -> HTTP/gRPC (token-streaming SSE)                         |
|              |                                                     |
|              v                                                     |
|  +--------------------------------------------------+              |
|  |  Rust Server (actix-web, Tokio runtime)          |              |
|  |  - sharded client (request fan-out)              |              |
|  |  - dynamic batching queue (max_batch_size)       |              |
|  +----------------------+---------------------------+              |
|                         v                                          |
|  +--------------------------------------------------+              |
|  |  Python shard (per GPU)                          |              |
|  |  +----------------+  +----------------------+    |              |
|  |  |  Scheduler     |  |  Model:              |    |              |
|  |  |  - continuous  |  |  - PyTorch + custom  |    |              |
|  |  |    batching    |  |    CUDA kernels      |    |              |
|  |  |  - prefill/    |  |  - FlashAttention-2  |    |              |
|  |  |    decode      |  |  - bitsandbytes      |    |              |
|  |  |    disaggreg.  |  |    (INT8/INT4)       |    |              |
|  |  +----------------+  |  - Tensor Parallel   |    |              |
|  |                      |    (Megatron-style)  |    |              |
|  |                      +----------------------+    |              |
|  |                      KV Cache: Paged (vLLM과 유사)|              |
|  |                      Quantization: GPTQ, AWQ, EETQ|              |
|  +--------------------------------------------------+              |
|         |              |              |              |              |
|         v              v              v              v              |
|      GPU 0          GPU 1          GPU 2          GPU 3             |
|   (shard 0)      (shard 1)      (shard 2)      (shard 3)         |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **vLLM BlockManager** | KV Cache paging | 16-token block, Block Table, CoW, prefix sharing, logical↔physical 매핑, eviction policy (LRU) |
| **vLLM Scheduler** | Iteration-level scheduling | FCFS / SJF policy, Chunked prefill(max_num_batched_tokens), preemption(recompute vs. swap), prefix cache hit |
| **vLLM Model Runner** | GPU forward pass | CUDA Graph capture로 kernel launch overhead 제거, FlashInfer/FlashAttn-2/vLLM-Flash backend 선택, 4D parallel(TP/PP/DP/EP) |
| **vLLM Engine/AsyncLLM** | Request lifecycle | `add_request->step()->outputs`, asyncio로 비동기 처리, Ray로 multi-node orchestration |
| **TGI Rust Server** | API gateway & sharding | actix-web async I/O, sharded-client가 gRPC로 Python shard에 분배, SSE(Server-Sent Events)로 token streaming |
| **TGI Scheduler** | Batching 결정 | `max_batch_size=32`, `max_wait_tokens=20ms`, prefill/decode 시간 균형(batching window) |
| **TGI Quantization Module** | Weight 압축 | GPTQ(4-bit), AWQ(Activation-aware Weight Quant), bitsandbytes NF4(4-bit NormalFloat), EETQ, FP8(H100) |
| **TGI KV Cache** | 메모리 관리 | PagedAttention(vLLM과 동일), `max_batchable_tokens`, prefix caching, sliding window attention 지원 |
| **Speculative Decoding 모듈** (v0.6+) | 추론 가속 | draft model(EAGLE/Medusa/n-gram)로 N tokens 추측 -> target model로 1회 verify -> 2~3× 속도 향상 |
| **LoRA Adapter Manager** | Multi-tenant serving | `--enable-lora --lora-modules`, Hot-swap, base model 공유, per-request LoRA dispatch |

### 4. 핵심 파라미터와 튜닝 공식

```
Throughput(tokens/sec) ≈ min(  (batch_size × FLOPs/iter) / time_per_iter,
                                (mem_bandwidth × GPU_count) / (KV_per_token × model_dim)  )

KV Cache size per token = 2 × num_layers × num_kv_heads × head_dim × dtype_bytes
                        (예: LLaMA-70B: 2×80×8×128×2 = 327,680 bytes = 320 KB/token)
```

| 파라미터 | vLLM | TGI | 영향 |
| :--- | :--- | :--- | :--- |
| `max_num_seqs` | 256 (default) | `max_batch_size=32` | 동시 처리 request 수, GPU OOM 직접 영향 |
| `max_num_batched_tokens` | 2048 | `max_batch_total_tokens` | 1 iteration에 처리할 총 token 수 |
| `max_model_len` | 4096~32768 | `max_input_length`+`max_total_tokens` | KV cache 사전 할당량 결정 |
| `gpu_memory_utilization` | 0.9 | (자동) | KV cache에 할당할 비율 (0.6~0.95) |
| `block_size` | 16 | (내부) | PagedAttention granularity (8/16/32) |
| `enforce_eager` | True/False | (X) | CUDA Graph 비활성화 (디버깅용) |
| `quantization` | awq/gptq/squeezellm/bnb | awq/gptq/bitsandbytes/eetq/fp8 | Weight 정밀도 trade-off |

- **📢 섹션 요약 비유**: PagedAttention은 **호텔 방을 통째로 빌리는 것**이 아니라, **다닥다닥 붙은 자전거 거치대처럼 16명씩 그룹 단위로 나누어 차곡차곡 채워 넣는 것**이라 빈 공간이 거의 없다.

---

## Ⅲ. 비교 및 연결

### vLLM vs. TGI 상세 비교

| 구분 | **vLLM** | **TGI (Text Generation Inference)** |
| :--- | :--- | :--- |
| **개발 주체** | UC Berkeley (学术界) -> Anyscale 상