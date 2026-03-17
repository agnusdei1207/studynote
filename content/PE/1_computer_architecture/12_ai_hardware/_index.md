+++
title = "12. 가속기 및 AI 하드웨어 (AI Hardware)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "수학 문제만 엄청나게 빨리 푸는 '수학 천재 로봇' 친구예요. 평소에는 다른 친구들이 일을 하지만, 어려운 계산이 나오면 이 친구가 나타나서 눈 깜짝할 사이에 정답을 알려준답니다!"
+++

# 12. 가속기 및 AI 하드웨어 (AI Hardware)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 딥러닝의 핵심인 대규모 행렬 곱셈(Matrix Multiplication)과 벡터 연산을 극도로 효율화한 도메인 특화 아키텍처(DSA).
> 2. **가치**: 기존 CPU 대비 AI 연산 에너지 효율 100배 향상 및 데이터 전송 병목을 줄이는 PIM(Processing-In-Memory) 기술의 실현.
> 3. **융합**: 소프트웨어 프레임워크(TensorFlow, PyTorch)와 하드웨어 커널 간의 긴밀한 최적화를 통한 엔드투엔드 가속 시스템 구축.

---

### Ⅰ. 개요 (Context & Background)
AI 하드웨어는 폰 노이만 구조의 한계를 넘어서는 새로운 패러다임이다. 데이터 이동을 최소화하고 연산 유닛을 격자 형태로 배치하여 데이터가 흐르면서 연산되는 시스톨릭 어레이(Systolic Array) 구조가 핵심이다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 가속기 유형
- **GPU (Graphics Processing Unit)**: 범용 병렬 처리 (SIMT)
- **TPU (Tensor Processing Unit)**: 구글의 텐서 연산 특화 ASIC
- **NPU (Neural Processing Unit)**: 모바일/엣지용 신경망 가속기
- **PIM (Processing-In-Memory)**: 메모리 내부 연산으로 데이터 이동 혁신

#### 2. 시스톨릭 어레이 구조 (ASCII)
```text
    [ Systolic Array for Matrix Mult ]
    
    Data In -> [PE] -> [PE] -> [PE] -> Data Out
                |       |       |
               [PE] -> [PE] -> [PE]
                |       |       |
               [PE] -> [PE] -> [PE]
    
    * PE: Processing Element (MAC: Multiply-Accumulate)
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### CPU vs GPU vs NPU
| 항목 | CPU (범용) | GPU (병렬) | NPU (특화) |
| :--- | :--- | :--- | :--- |
| **설계 목표** | 복잡한 제어, 저지연 | 높은 처리량 (Throughput) | AI 연산 극대화 (Efficiency) |
| **코어 구조** | 적고 강력한 코어 | 많고 단순한 코어 | 연산 유닛 격자 구조 |
| **에너지 효율** | 낮음 | 중간 | 매우 높음 |
| **유연성** | 매우 높음 | 높음 | 낮음 (특정 연산만) |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 AI 모델의 크기가 커짐에 따라 **Memory Wall** 문제가 심화되고 있다. 기술사는 모델 양자화(Quantization)와 프루닝(Pruning)을 통해 하드웨어 자원 점유를 최적화하고, 온디바이스 AI와 클라우드 AI 사이의 부하 분산 전략을 수립해야 한다.

---

### Ⅴ. 기대효과 및 결론
AI 하드웨어는 자율주행, 로봇, 생성형 AI의 물리적 토대다. 향후 인간의 뇌를 모사한 뉴로모픽(Neuromorphic) 칩과 광컴퓨팅 기술이 결합하여 지능형 컴퓨팅의 한계를 확장할 것이다.
