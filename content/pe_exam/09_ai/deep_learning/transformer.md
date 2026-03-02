+++
title = "Transformer / Attention Mechanism"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# Transformer / Attention Mechanism

## 핵심 인사이트 (3줄 요약)
> **Transformer**는 "Attention Is All You Need"(2017)에서 제안된 순전히 Attention 기반 신경망으로, RNN 없이도 시퀀스를 병렬 처리한다. **Self-Attention**은 문장 내 모든 토큰 쌍의 관계를 가중합으로 계산해 장거리 의존성을 포착한다. LLM·ViT·Stable Diffusion 등 현대 AI의 99%가 Transformer로 구동된다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: Transformer는 Encoder-Decoder 구조의 딥러닝 아키텍처로, Scaled Dot-Product Attention과 Multi-Head Attention을 핵심으로 한다. 입력 시퀀스의 각 토큰이 다른 모든 토큰과의 관계를 동적으로 계산하여 문맥을 파악한다.

> 비유: "회의실에서 모든 참석자가 서로 동시에 대화 → 중요한 말에 선택적 집중"

**등장 배경**:
- RNN/LSTM 한계: 순차 처리로 병렬화 불가, 장거리 의존성 소실 (Vanishing Gradient)
- Attention 메커니즘(2015, Bahdanau): Encoder-Decoder 간 중요 위치 집중 → 기계 번역 향상
- **Transformer(2017, Vaswani et al.)**: Attention만으로 RNN 완전 대체 → 병렬 학습 가능

---

### Ⅱ. 구성 요소 및 핵심 원리  ↔  구조 + 원리 + 코드

**구성 요소**:
| 구성 요소 | 역할 | 비유 |
|----------|------|------|
| Input Embedding + Pos. Encoding | 토큰 벡터화 + 위치 정보 주입 | 이름표 + 좌석번호 |
| Multi-Head Self-Attention | 다중 관점에서 토큰 관계 학습 | 여러 각도의 동시 분석 |
| Add & LayerNorm | Residual 연결 + 정규화 | 원본 보존 + 품질 안정화 |
| Feed Forward Network (FFN) | 위치별 독립 비선형 변환 | 개별 심층 분석 |
| Encoder / Decoder | 입력 이해 / 출력 생성 | 이해·번역가 |

**핵심 원리** - Scaled Dot-Product Attention:
```
Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V

- Q (Query): "무엇을 찾고 싶은가?"
- K (Key):   "나는 이런 정보를 가지고 있어"
- V (Value): "실제 내용"
- √d_k:      과도한 dot-product 방지 (온도 조절)

Self-Attention 흐름:
입력 X → Q=WqX, K=WkX, V=WvX
→ Attention Score = QKᵀ/√dk
→ Softmax (확률 분포)
→ Weighted Sum of V
→ 문맥 반영된 새 표현
```

**Multi-Head Attention**:
```
MultiHead(Q,K,V) = Concat(head₁,...,headₕ) · Wₒ
where headᵢ = Attention(QWᵢQ, KWᵢK, VWᵢV)

각 헤드 = 다른 관점에서의 Attention
h=8~16 헤드 → 다양한 언어 관계 동시 포착
```

**코드 예시** (PyTorch 간단 구현):
```python
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, n_heads=8):
        super().__init__()
        self.d_k = d_model // n_heads
        self.n_heads = n_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        weights = torch.softmax(scores, dim=-1)
        return torch.matmul(weights, V)
    
    def forward(self, x):
        B, L, D = x.shape
        # Linear projection + reshape to heads
        Q = self.W_q(x).view(B, L, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(B, L, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(B, L, self.n_heads, self.d_k).transpose(1, 2)
        
        # Attention
        attn_out = self.scaled_dot_product_attention(Q, K, V)
        
        # Concat + Project
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, L, D)
        return self.W_o(attn_out)
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + 비교

**장단점**:
| 장점 | 단점 |
|-----|------|
| 완전 병렬화 (GPU 효율 극대화) | Self-Attention 복잡도 O(n²) — 긴 시퀀스에 비효율 |
| 장거리 의존성 포착 (어떤 거리도 1홉) | 위치 정보 별도 주입 필요 |
| 사전훈련 + 미세조정 패러다임 |  메모리 사용량 큼 |
| 멀티모달 확장 용이 | 해석 가능성 낮음 |

**Transformer 변형 비교**:
| 모델 | 구조 | 특징 | 용도 |
|------|------|------|------|
| Encoder-only (BERT) | 인코더만 | 양방향 문맥 | 분류, NER, QA |
| Decoder-only (GPT) | 디코더만 | 자동회귀 생성 | 텍스트 생성, LLM |
| Encoder-Decoder (T5, BART) | 인코더+디코더 | 조건부 생성 | 번역, 요약 |
| Vision Transformer (ViT) | 이미지 패치 | 이미지 인식 | 컴퓨터 비전 |
| Mamba (SSM) | 상태공간 | O(n) 선형 복잡도 | 긴 시퀀스 대안 |

> **선택 기준**: 생성 → GPT 계열; 이해 → BERT 계열; 긴 시퀀스 효율 → Mamba/Longformer

---

### Ⅳ. 실무 적용 방안  ↔  기술사적 판단 + 활용 + 주의사항

**기술사적 판단** (활용 사례):
| 적용 분야 | 활용 방법 | 기대 효과 |
|---------|--------|--------|
| 기계번역 | Encoder-Decoder Transformer | 번역 품질 BLEU +20% |
| 기업 챗봇 | GPT-기반 Decoder-only | 자연스러운 대화 생성 |
| 문서 분류 | 사전훈련 BERT 미세조정 | 분류 정확도 90%+ |
| 이미지 인식 | ViT (Vision Transformer) | CNN 대비 대규모 데이터서 우수 |
| 코드 생성 | CodeLLaMA / StarCoder | 개발 생산성 30~50% 향상 |

**주의사항 / 흔한 실수**:
- **Attention 복잡도**: 시퀀스 길이 4배 → 메모리·시간 16배 → FlashAttention 활용
- **위치 인코딩 선택**: 절대 (sinusoidal) vs 상대 (RoPE, ALiBi) — 긴 컨텍스트는 RoPE
- **Gradient Vanishing**: 깊은 Transformer → Pre-LayerNorm, Residual 설계 중요

**관련 개념**: Self-Attention, Multi-Head Attention, Positional Encoding, BERT, GPT, ViT, Mamba, Flash Attention

---

### Ⅴ. 기대 효과 및 결론  ↔  미래 전망

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| NLP 혁신 | RNN 대체, 범용 사전훈련 가능 | 기계번역 BLEU 30~50% 향상 |
| 비전 | CNN 대체 가능성 (ViT) | ImageNet 최고 성능 |
| 다중 모달 | 텍스트+이미지+음성 통합 | 범용 AI 기반 |

> **결론**: Transformer는 현대 AI의 "만능 엔진". RNN·CNN을 통합하며 언어·시각·음성·과학 모든 도메인의 기반 모델을 구동한다. 차세대는 O(n) 효율의 Mamba(SSM)·Flash Attention 등 장시퀀스 최적화가 핵심 연구 방향이다.  
> **※ 참고**: "Attention Is All You Need"(Vaswani et al., 2017), Flash Attention 논문(Dao 2022)

---

## 어린이를 위한 종합 설명

**Transformer는 "모든 사람이 동시에 서로 대화하는 회의"야!**

예전 AI (RNN):
```
왼쪽 사람 → 오른쪽 사람 → 오른쪽 사람 → ...
한 명씩 차례로 → 느리고 앞을 잊어버려
```

Transformer (새 방식):
```
모든 사람이 동시에 서로 대화!
"저 단어가 이 단어랑 관련 있어?" → 모두 그렇다!
병렬 처리 → 엄청나게 빠름!
```

Attention이란?:
```
문장: "고양이가 쥐를 쫓아 잡았다 — 그것이 빨랐기 때문이다"
"그것"이 뭔지 어떻게 알아?

Attention: "그것 ← → 고양이" (높은 점수)
            "그것 ← → 쥐" (낮은 점수)
→ "그것 = 고양이"라고 이해!
```

> Transformer = 모든 AI가 달리는 초강력 엔진! LLM, 이미지 AI, 번역 모두 여기서 시작해 🚀

---
