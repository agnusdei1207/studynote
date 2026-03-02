+++
title = "GPU/NPU 및 AI 가속기"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# GPU/NPU 및 AI 가속기 (AI Accelerator)

## 핵심 인사이트 (3줄 요약)
> **GPU(Graphics Processing Unit)**는 수천 개의 작은 코어로 행렬 연산을 병렬 처리하여 AI 학습의 핵심 하드웨어가 되었다. **NPU(Neural Processing Unit)**는 AI 추론에 특화된 전용 칩으로 전력 대비 성능이 우수하여 스마트폰·엣지 기기에 탑재된다. NVIDIA H100/H200이 2024년 AI 인프라 표준이며, **HBM3e·NVLink·InfiniBand** 생태계가 AI 클러스터의 핵심이다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: AI 가속기는 행렬 곱셈·합성곱 등 AI 연산을 CPU보다 수백~수천 배 빠르게 처리하는 전용 하드웨어이다. GPU·TPU·NPU·FPGA·ASIC 등 다양한 유형이 있다.

> 비유: "수학 올림피아드 선수(GPU) vs 만능 일반 직원(CPU) — 복잡한 행렬 계산은 전문가가 100배 빠르다"

**등장 배경**:
- CPU의 AI 연산 한계: 코어 수십 개, 직렬 처리 최적화
- GPU 병렬성 발견: 2009년 CUDA로 GPU를 ML에 적용 → AlexNet(2012) 성공
- 딥러닝 폭발 → GPU 부족 → NVIDIA 시가총액 1위(2024)
- LLM 등장: 수백 GPU 클러스터 필수 → AI 인프라 산업 급성장

---

### Ⅱ. 구성 요소 및 핵심 원리

**AI 가속기 분류**:
| 유형 | 특징 | 대표 제품 | 적합 용도 |
|------|------|--------|--------|
| GPU | 범용 병렬 처리, 대규모 메모리 | NVIDIA H100/A100, AMD MI300 | LLM 학습·추론 |
| TPU | 구글 설계, BF16 특화 | Google TPU v5 | LLM 학습 (GCP) |
| NPU | 저전력 AI 추론 특화 | Apple Neural Engine, Qualcomm NPU | 스마트폰·엣지 |
| AI ASIC | 특정 워크로드 최적 | Cerebras WSE-3, Groq LPU | 초고속 추론 |
| FPGA | 유연한 재프로그래밍 | Xilinx Alveo, Intel Agilex | 프로토타입·특수 |

**GPU 핵심 구조 (NVIDIA H100)**:
```
H100 SXM 스펙:
- CUDA Core: 16,896개
- Tensor Core (4세대): 528개 (FP8/BF16/FP16 행렬연산)
- HBM3: 80GB (3.35TB/s 대역폭)
- NVLink 4.0: 900GB/s (GPU 간 연결)
- FP8 성능: 3,958 TFLOPS (학습 효율 2배↑)
- 전력: 700W

행렬 연산 (Matrix Multiplication):
CPU: A[m×k] × B[k×n] → 직렬 → O(m·k·n) 시간
GPU: 블록별 병렬 → 1000배+ 빠름
→ Transformer의 Q·K·V 행렬 연산 = GPU가 지배적 이유
```

**HBM (High Bandwidth Memory)**:
```
GDDR6 (일반) vs HBM (AI용):
GDDR6: 약 900GB/s
HBM2e: 3.2TB/s
HBM3:  3.35TB/s
HBM3e: 4.8TB/s (H200)

왜 중요? LLM 추론 시 KV Cache가 메모리 대역폭에 병목
→ HBM = AI의 초고속 기억 도로
```

**분산 학습 인터커넥트**:
```
NVLink (NVIDIA)
: GPU 간 단일 노드 내 고속 연결
: H100 Transformer Engine = 900GB/s 양방향

InfiniBand (노드 간)
: GPU 서버 수천 대 연결
: HDR/NDR: 200~400Gb/s

실제 LLM 학습 클러스터:
[GPU 8개/노드] ─NVLink─ [노드 내 All-reduce]
      │                          
 InfiniBand (400Gb/s)          
      │                          
[GPU 8개/노드] ─NVLink─ [다른 노드]
수백~수천 노드 연결 → 수천~수만 GPU 규모!
```

---

### Ⅲ. 기술 비교 분석  ↔  AI 가속기 세대별/제조사별 비교

**상위 GPU 비교 (2024~2025)**:
| GPU | HBM | 대역폭 | BF16 TFLOPS | 가격 | 특징 |
|-----|-----|-------|------------|------|------|
| H100 SXM | 80GB HBM3 | 3.35TB/s | 1979 | ~$35K | 학습 표준 |
| H200 SXM | 141GB HBM3e | 4.8TB/s | 1979 | ~$45K | 메모리 혁신 |
| A100 | 80GB HBM2e | 2TB/s | 312 | ~$15K | 이전 세대 |
| AMD MI300X | 192GB HBM3 | 5.2TB/s | 1307 | ~$25K | NVIDIA 도전 |
| Google TPU v5p | N/A | N/A | - | GCP 과금 | 구글 생태계 |

**모바일/엣지 NPU (2024)**:
| 칩 | 제조사 | AI 성능 | 탑재 제품 |
|----|------|--------|--------|
| Apple Neural Engine (A18) | Apple | 38 TOPS | iPhone 16 |
| Snapdragon X Elite NPU | Qualcomm | 45 TOPS | AI PC |
| Intel Core Ultra (NPU 4) | Intel | 48 TOPS | AI PC |
| Dimensity 9300 | MediaTek | 40 TOPS | 안드로이드 플래그십 |
| Gaudi 3 | Intel (구 Habana) | - | 서버 AI 추론 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (AI 인프라 선택):
| 워크로드 | 권장 하드웨어 | 이유 |
|---------|---------|------|
| LLM 학습 (70B+) | H100/H200 클러스터 | 대용량 메모리·고대역폭 필수 |
| 추론 서비스 (저지연) | A10G/L4 또는 Groq LPU | 비용·전력 효율 |
| 스마트폰 AI | NPU (Qualcomm/Apple) | 초저전력, On-device |
| 엣지 AI (산업) | Jetson Orin NX (NVIDIA) | 소형, 저전력 |
| AI PC | Core Ultra / Snapdragon X | NPU+CPU+GPU 통합 |

**모델 병렬화 전략**:
```
Data Parallelism (DP):
  같은 모델을 N개 GPU에 복제
  배치를 나눠서 동시 처리 → SGD 집계

Tensor Parallelism (TP):
  행렬을 N개 GPU에 분할
  Q,K,V 행렬을 수평 분할 → GPU간 통신 필요

Pipeline Parallelism (PP):
  Transformer 레이어를 N개 GPU에 순서대로 분배
  레이어1→GPU1, 레이어2→GPU2...

3D Parallelism (DP+TP+PP):
  GPT-3/4 규모 학습에 사용
```

**주의사항 / 흔한 실수**:
- GPU 개수 != 학습 속도 선형 비례: 통신 오버헤드 증가 → 최적 병렬화 전략 필수
- HBM 메모리 부족: LLM 추론 시 KV Cache 급증 → 적절한 배치 크기 관리
- 전력 과소 산정: H100 700W × 8 = 5.6kW/노드 → 데이터센터 전력·냉각 설계

**관련 개념**: CUDA, Tensor Core, HBM, NVLink, InfiniBand, 분산학습, 모델 병렬화, 양자화

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 학습 속도 | H100 클러스터 | CPU 대비 1000배+ 빠른 AI 학습 |
| 비용 효율 | NPU 탑재 AI PC | 클라우드 비용 없이 On-device AI |
| 추론 처리량 | Groq LPU | GPT-4급 추론 500 토큰/초 |

> **결론**: GPU/NPU는 AI 혁명의 물리적 기반 — NVIDIA H100이 현재 표준이고, HBM·NVLink·InfiniBand가 클러스터 생태계를 형성한다. 기술사는 학습·추론 워크로드별 하드웨어 선택·분산학습 아키텍처·데이터센터 전력 설계까지 이해해야 한다.  
> **※ 참고**: NVIDIA H100 Whitepaper, MLPerf 벤치마크, NVIDIA NVLink/NVSwitch 아키텍처

---

## 어린이를 위한 종합 설명

**GPU는 "수천 명의 계산 전문가 팀"이야!**

```
CPU (일반 컴퓨터):
  16개의 엄청 똑똑한 계산기
  → 복잡한 것 하나씩 빠르게

GPU (AI 전용):
  16,896개의 계산기 (H100 기준)
  → "모두 함께! 동시에! 한꺼번에!"
  → 행렬 계산: CPU의 1000배 빠름!
```

NPU (스마트폰 AI):
```
스마트폰에서 "Hey Siri / 빅스비":
  예전: 인터넷으로 서버에 보내서 처리 → 느리고 개인정보 노출
  지금: 스마트폰 내 NPU가 처리 → 빠르고 오프라인도 가능!
```

> GPU = AI 공장의 초고속 생산기계! NPU = 스마트폰 안의 초소형 AI 전용 칩! ⚡🔥

---
