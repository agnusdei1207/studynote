+++
title = "순환 신경망 (RNN / LSTM)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 순환 신경망 (RNN / LSTM / GRU)

## 핵심 인사이트 (3줄 요약)
> **RNN(Recurrent Neural Network)**은 순차 데이터(시계열, 자연어)를 처리하기 위해 내부에 순환 구조(Hidden State)를 가진 신경망이다. RNN의 고질적 문제인 장기 의존성 소실을 해결하기 위해 게이트 메커니즘을 도입한 **LSTM(Long Short-Term Memory)과 GRU(Gated Recurrent Unit)**가 순차 데이터의 표준으로 사용되었다. 2017년 이후 Transformer에 많은 자리를 내주었으나, 시계열 예측, 경량 환경에서 여전히 활발히 사용된다.

---

### Ⅰ. 개요 (개념 + 등장 배경)

**개념**: 순환 신경망(Recurrent Neural Network, RNN)은 은닉층의 결과가 다시 동일한 은닉층의 입력으로 들어가는 순환 구조를 통해 과거의 정보를 기억하고, 이를 바탕으로 현재의 출력을 결정하는 인공신경망 아키텍처이다.

> 비유: "책을 읽을 때 앞 문장의 맥락을 기억하면서 현재 문장을 이해하는 과정"

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: 기존 FNN(Feedforward Neural Network)/CNN은 입력/출력 길이가 고정되어 있고, 연속성(순서)을 고려하지 못함. 시계열, 자연어 등 가변 길이 순차 데이터 처리 불가
2. **기술적 필요성**: 자연어, 주가 데이터, 음성 신호 등 길이를 알 수 없는 순차 데이터 처리를 위해 과거 상태를 기억하는 은닉 상태(Hidden State) 도입 필요
3. **시장/산업 요구**: RNN의 한계(긴 문장에서 기울기 소실 → 장기 기억 불가)를 극복하기 위해 LSTM(1997, Hochreiter) 등장. 게이트(Gate)와 셀 상태(Cell State)로 장기 의존성 문제 해결

**핵심 목적**: 순차 데이터의 시간적 의존성을 학습하여 미래를 예측하거나 시퀀스를 생성하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**RNN 구성 요소** (필수: 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **입력 x_t** | 현재 시점의 입력 벡터 | 시퀀스의 각 원소 | 현재 읽는 단어 |
| **은닉 상태 h_t** | 이전 정보와 현재 입력의 결합 | 순환 구조의 핵심 | 문맥 기억 |
| **가중치 W** | 입력→은닉, 은닉→은닉 변환 | 시점 간 공유 (Weight Sharing) | 학습된 패턴 |
| **출력 y_t** | 현재 시점의 예측 | 분류/회귀/시퀀스 | 예측 결과 |
| **활성화 함수** | 비선형성 추가 | tanh, ReLU, sigmoid | 복잡성 표현 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RNN / LSTM Architecture                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [Basic RNN Structure]                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                                                                  │  │
│  │   t=1        t=2        t=3        ...        t=T               │  │
│  │  ┌─────┐    ┌─────┐    ┌─────┐              ┌─────┐            │  │
│  │  │ x_1 │    │ x_2 │    │ x_3 │              │ x_T │            │  │
│  │  └──┬──┘    └──┬──┘    └──┬──┘              └──┬──┘            │  │
│  │     │          │          │                    │                │  │
│  │     ↓          ↓          ↓                    ↓                │  │
│  │  ┌─────┐    ┌─────┐    ┌─────┐              ┌─────┐            │  │
│  │  │ h_1 │───→│ h_2 │───→│ h_3 │───→ ... ───→│ h_T │            │  │
│  │  └──┬──┘    └──┬──┘    └──┬──┘              └──┬──┘            │  │
│  │     │          │          │                    │                │  │
│  │     ↓          ↓          ↓                    ↓                │  │
│  │  ┌─────┐    ┌─────┐    ┌─────┐              ┌─────┐            │  │
│  │  │ y_1 │    │ y_2 │    │ y_3 │              │ y_T │            │  │
│  │  └─────┘    └─────┘    └─────┘              └─────┘            │  │
│  │                                                                  │  │
│  │   h_t = tanh(W_hh × h_{t-1} + W_xh × x_t + b_h)                │  │
│  │   y_t = W_hy × h_t + b_y                                        │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  [LSTM Cell Structure]                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                                                                  │  │
│  │   c_{t-1} ──────────────────────────────────────────────► c_t   │  │
│  │      │         ┌─────────────────────────┐              │        │  │
│  │      │         │                         │              │        │  │
│  │      │    ┌────┴────┐              ┌────┴────┐         │        │  │
│  │      │    │ Forget  │              │  Input  │         │        │  │
│  │      └───►│  Gate   │              │  Gate   │◄── x_t  │        │  │
│  │           │ (f_t)   │              │ (i_t)   │         │        │  │
│  │           └────┬────┘              └────┬────┘         │        │  │
│  │                │                        │              │        │  │
│  │                ▼                        ▼              │        │  │
│  │           ┌────────────────────────────────┐          │        │  │
│  │           │        Cell Update (C_t)       │◄─────────┘        │  │
│  │           │  f_t ⊙ c_{t-1} + i_t ⊙ c̃_t    │                   │  │
│  │           └───────────────┬────────────────┘                   │  │
│  │                           │                                    │  │
│  │   h_{t-1} ────────────────┼──────────────────────────────────► h_t│
│  │                           │              ┌─────────────┐       │  │
│  │                           └─────────────►│   Output    │       │  │
│  │                                          │   Gate (o_t)│       │  │
│  │                                          └──────┬──────┘       │  │
│  │                                                 │              │  │
│  │                                                 ▼              │  │
│  │                                          h_t = o_t ⊙ tanh(c_t) │  │
│  │                                                                  │  │
│  │   게이트 공식:                                                   │  │
│  │   f_t = σ(W_f × [h_{t-1}, x_t] + b_f)  # Forget Gate           │  │
│  │   i_t = σ(W_i × [h_{t-1}, x_t] + b_i)  # Input Gate            │  │
│  │   o_t = σ(W_o × [h_{t-1}, x_t] + b_o)  # Output Gate           │  │
│  │   c̃_t = tanh(W_c × [h_{t-1}, x_t] + b_c) # Candidate Cell      │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  [GRU Structure - Simplified LSTM]                                      │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │   h_{t-1} ─────────────────────────────────────────────────► h_t │  │
│  │      │         ┌───────────────────────┐              │          │  │
│  │      │         │   Update Gate (z_t)   │              │          │  │
│  │      │         │   Reset Gate (r_t)    │◄── x_t      │          │  │
│  │      │         └───────────────────────┘              │          │  │
│  │      │                                                │          │  │
│  │      └────────► h_t = (1-z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t ◄─┘          │  │
│  │                                                                  │  │
│  │   GRU = LSTM 단순화 (Cell State 제거, 2개 게이트만 사용)         │  │
│  │   장점: 파라미터 적음, 학습 빠름, 소량 데이터에서 우수           │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 입력 수신 → ② 이전 상태와 결합 → ③ 새 은닉 상태 계산 → ④ 출력 생성 → ⑤ 다음 시점으로 전파
```

- **1단계 (입력 수신)**: 현재 시점 t의 입력 x_t를 받음
- **2단계 (이전 상태 결합)**: 이전 은닉 상태 h_{t-1}과 현재 입력 x_t를 가중치와 결합
- **3단계 (은닉 상태 계산)**: 활성화 함수(tanh)를 거쳐 새로운 은닉 상태 h_t 생성
- **4단계 (출력 생성)**: 은닉 상태로부터 출력 y_t 계산 (필요 시)
- **5단계 (전파)**: h_t를 다음 시점 t+1로 전달

**LSTM 게이트별 역할**:

| 게이트 | 공식 | 역할 | 비유 |
|--------|------|------|------|
| **망각 게이트 (Forget)** | f_t = σ(W_f × [h_{t-1}, x_t]) | 과거 정보를 얼마나 버릴지 결정 (0~1) | 지우개 |
| **입력 게이트 (Input)** | i_t = σ(W_i × [h_{t-1}, x_t]) | 현재 정보를 셀 상태에 얼마나 추가할지 | 새 메모 쓰기 |
| **셀 상태 (Cell State)** | c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t | 핵심 기억을 시퀀스 끝까지 전달 | 장기 기억 컨베이어 |
| **출력 게이트 (Output)** | o_t = σ(W_o × [h_{t-1}, x_t]) | 셀 상태를 바탕으로 최종 출력 | 요약본 제출 |

**핵심 알고리즘/공식** (해당 시 필수):

**기본 RNN**:
```
h_t = tanh(W_hh × h_{t-1} + W_xh × x_t + b_h)
y_t = softmax(W_hy × h_t + b_y)

문제점: 거리가 먼 입력의 기울기가 W의 곱셈 반복으로 0 수렴
       ∂h_t/∂h_{t-k} = ∏ W_hh → 0 (Vanishing Gradient)
```

**LSTM 그래디언트 흐름**:
```
c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t

∂c_t/∂c_{t-1} = f_t (게이트에 의해 제어)
→ f_t ≈ 1이면 그래디언트 보존 (장기 기억 가능)
→ "Constant Error Carousel" 효과
```

**코드 예시** (필수: Python):

```python
import torch
import torch.nn as nn
import numpy as np

# ============================================================
# LSTM 시계열 예측 모델
# ============================================================

class LSTMModel(nn.Module):
    """LSTM 기반 시계열 예측 모델"""

    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM 레이어 (batch_first=True → 입력 형태: batch, seq, feature)
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=False
        )

        # 완전연결층
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        x: (batch_size, seq_len, input_size)
        output: (batch_size, output_size)
        """
        batch_size = x.size(0)

        # 초기 은닉 상태와 셀 상태 초기화
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(x.device)

        # LSTM 순전파
        # out: (batch_size, seq_len, hidden_size)
        # (hn, cn): 최종 은닉/셀 상태
        out, (hn, cn) = self.lstm(x, (h0, c0))

        # 시퀀스의 마지막 출력만 사용 (Many-to-One)
        out = out[:, -1, :]  # (batch_size, hidden_size)

        # 최종 예측
        out = self.fc(out)  # (batch_size, output_size)

        return out


class GRUModel(nn.Module):
    """GRU 기반 모델 (LSTM 단순화 버전)"""

    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super(GRUModel, self).__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # GRU는 셀 상태 없이 은닉 상태만 사용
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, hn = self.gru(x, h0)
        out = self.fc(out[:, -1, :])
        return out


class BiLSTMClassifier(nn.Module):
    """양방향 LSTM 텍스트 분류 모델"""

    def __init__(self, vocab_size, embed_dim=128, hidden_size=256, num_layers=2, num_classes=2):
        super(BiLSTMClassifier, self).__init__()

        # 임베딩 층
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)

        # 양방향 LSTM
        self.lstm = nn.LSTM(
            embed_dim,
            hidden_size,
            num_layers,
            batch_first=True,
            bidirectional=True,  # 양방향
            dropout=0.3
        )

        # 분류기 (양방향이므로 hidden_size * 2)
        self.fc = nn.Linear(hidden_size * 2, num_classes)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        # x: (batch_size, seq_len) - 토큰 ID
        embedded = self.embedding(x)  # (batch, seq, embed_dim)

        # BiLSTM
        lstm_out, (hn, cn) = self.lstm(embedded)

        # 마지막 시점의 양방향 출력 결합
        # hn: (num_layers * 2, batch, hidden)
        # 순방향 마지막 층: hn[-2], 역방향 마지막 층: hn[-1]
        hidden = torch.cat((hn[-2], hn[-1]), dim=1)  # (batch, hidden*2)

        # 분류
        out = self.dropout(hidden)
        out = self.fc(out)

        return out


# 시계열 데이터 준비 함수
def create_sequences(data, seq_length):
    """시계열 데이터를 시퀀스 형태로 변환"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)


# 사용 예시
if __name__ == "__main__":
    # 하이퍼파라미터
    seq_length = 30
    hidden_size = 64
    num_layers = 2

    # 더미 시계열 데이터 생성
    np.random.seed(42)
    data = np.sin(np.linspace(0, 20, 1000)) + np.random.normal(0, 0.1, 1000)

    # 시퀀스 생성
    X, y = create_sequences(data, seq_length)
    X = torch.FloatTensor(X).unsqueeze(-1)  # (batch, seq, 1)
    y = torch.FloatTensor(y).unsqueeze(-1)

    print(f"입력 형태: {X.shape}")  # (970, 30, 1)
    print(f"출력 형태: {y.shape}")  # (970, 1)

    # 모델 생성
    model = LSTMModel(input_size=1, hidden_size=hidden_size, num_layers=num_layers)

    # 순전파 테스트
    output = model(X[:10])  # 배치 10개
    print(f"예측 형태: {output.shape}")  # (10, 1)

    # 파라미터 수 계산
    total_params = sum(p.numel() for p in model.parameters())
    print(f"총 파라미터 수: {total_params:,}")
```

---

### Ⅲ. 기술 비교 분석 (장단점 + 시퀀스 모델 비교)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| 순차적 패턴(가변 길이) 처리 탁월 | 순차적 연산으로 병렬 처리 불가 (Transformer 대비 매우 느림) |
| 시계열 예측, 음성 인식 등 전통적 강자 | 매우 긴 시퀀스에서 여전히 정보 손실 우려 |
| 파라미터 수 상대적으로 적음 (가중치 공유) | 학습 속도 느림 |
| LSTM/GRU로 장기 의존성 문제 완화 | GPU 활용 효율이 Transformer 대비 낮음 |

**RNN vs LSTM vs GRU vs Transformer 비교** (필수: 최소 2개 대안):

| 비교 항목 | RNN | LSTM | GRU | ★ Transformer |
|---------|-----|------|-----|---------------|
| 핵심 특성 | 기본 순환 구조 | Cell State + 3 Gate | 2 Gate 단순화 | Self-Attention |
| 병렬 처리 | 불가 | 불가 | 불가 | ★ 가능 |
| 장기 기억력 | 매우 나쁨 | 좋음 | 좋음 | ★ 완벽 |
| 파라미터 수 | 적음 | 많음 | 중간 | 매우 많음 |
| 학습 속도 | 느림 | 느림 | LSTM보다 빠름 | ★ 빠름 (병렬) |
| 활용처 | 간단 시계열 | 금융, 신호 처리 | 경량 환경 | LLM, 범용 |

> **★ 선택 기준**:
> - **Transformer**: 초거대 언어 모델, 긴 문장 번역, 충분한 GPU 자원
> - **LSTM**: 금융 시계열, 센서 데이터, 중간 길이 시퀀스
> - **GRU**: 리소스 제한, 실시간 처리, 소량 데이터
> - **RNN**: 매우 간단한 시계열, 교육용

**RNN 아키텍처 패턴**:

| 패턴 | 입력 | 출력 | 예시 |
|------|------|------|------|
| One-to-One | 단일 | 단일 | 일반 NN |
| One-to-Many | 단일 | 시퀀스 | 이미지 캡셔닝 |
| Many-to-One | 시퀀스 | 단일 | 감성 분석 |
| Many-to-Many | 시퀀스 | 시퀀스 | 기계 번역, 비디오 분석 |

---

### Ⅳ. 실무 적용 방안 (기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융/주가 수요 예측** | LSTM으로 주식 가격, 전력 수요 예측 | 과거 30일 시퀀스 기반 MAPE 10% 이내 |
| **엣지 디바이스 음성인식** | GRU로 Wake-word 인식 ("시리야") | 모델 크기 1MB 이하, 실시간 반응 < 100ms |
| **센서 이상치 탐지** | LSTM-AutoEncoder로 설비 진동 분석 | 비정상 판정 F1 90%+ |
| **감성 분석 / 챗봇** | Bi-LSTM으로 문장 감성 분류 | 정확도 85%+ |
| **의료 신호 처리** | LSTM으로 ECG/EEG 이상 탐지 | 민감도 95%+ |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Google Speech Recognition** - LSTM 기반 음성 인식 모델로 음성 검색 정확도 20% 향상. 스마트폰 온디바이스에서 실시간 처리 가능.
- **사례 2: Amazon Alexa** - GRU 기반 Wake Word Detection ("Alexa"). 저전력 디바이스에서 24시간 대기, < 200ms 반응 시간.
- **사례 3: Uber 시계열 예측** - LSTM으로 수요 예측, 이상 탐지. 예측 정확도 15% 향상으로 운영 효율 개선.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: 시퀀스 길이에 따른 학습 시간 고려, Gradient Clipping 필수 (LSTM에서도 폭발 가능), 양방향(Bidirectional) 필요성 검토
2. **운영적**: 실시간 스트리밍 시 상태 관리, 배치 vs 스트리밍 추론 선택, 모델 경량화 (Quantization)
3. **보안적**: 시계열 데이터의 민감성 고려, 연합학습과 결합 가능
4. **경제적**: Transformer 대비 적은 GPU로 학습 가능, 엣지 디바이스 배포 용이

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **Look-ahead Bias**: 학습 데이터에 미래 데이터 포함. 해결: 시계열 Split, Rolling Window 검증
- ❌ **과도한 시퀀스 길이**: LSTM도 수백 Step 초과 시 성능 저하. 해결: Attention 추가 또는 Transformer 고려
- ❌ **Gradient Clipping 누락**: 여전히 그래디언트 폭발 가능. 해결: `torch.nn.utils.clip_grad_norm_`
- ❌ **양방향 오용**: 실시간 예측에는 양방향 부적합. 해결: 실시간은 단방향만 사용

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  RNN/LSTM 핵심 연관 개념 맵                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [MLP] ←──→ [RNN] ←──→ [LSTM/GRU] ←──→ [Attention]            │
│                ↓           ↓                ↓                   │
│           [Seq2Seq]   [Bidirectional]   [Transformer]           │
│                ↓           ↓                ↓                   │
│           [기계번역] ←──→ [음성인식] ←──→ [LLM]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| Attention | 개선 기법 | RNN에 Attention 추가로 장기 의존성 해결 | `[attention](./attention.md)` |
| Transformer | 후속 모델 | Attention만으로 RNN 대체 | `[transformer](./transformer.md)` |
| 시계열 분석 | 주요 응용 | LSTM의 대표적 활용 분야 | `[time_series](../ai_applications/time_series.md)` |
| AutoEncoder | 결합 모델 | LSTM-AE로 이상치 탐지 | `[autoencoder](../ai_foundations/autoencoder.md)` |
| Seq2Seq | 아키텍처 | Encoder-Decoder 구조 | `[seq2seq](./seq2seq.md)` |

---

### Ⅴ. 기대 효과 및 결론 (미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 시계열 성능 | 시간 종속적 피처 추출 | 선형 회귀 대비 오차 30% 이상 개선 |
| 구조적 유연성 | 가변 길이 음성/텍스트 입출력 | 패딩/잘라내기로 범용 처리 |
| 실시간 처리 | 엣지 디바이스 배포 | 모델 크기 < 5MB, 지연 < 100ms |
| 이상 탐지 | LSTM-AE 기반 탐지 | F1 Score 90%+ |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: RNN + Attention 하이브리드, Mamba 등 State Space Model이 대안으로 부상, LSTM은 특정 도메인에서 지속 사용
2. **시장 트렌드**: NLP는 Transformer 주도, 시계열/센서/IoT는 LSTM/GRU 여전히 강세, 엣지 AI에서 경량화된 RNN 수요 지속
3. **후속 기술**: RWKV, Mamba 등 RNN의 효율성 + Transformer의 성능 결합 모델 연구 활발

> **결론**: RNN과 LSTM은 순차 데이터 처리의 표준을 정립한 고전 명작 기법이다. NLP 영역에서는 Transformer(LLM)에 의해 주도권을 넘겨주었으나, 1차원 센서 데이터 기반의 이상 탐지, 금융 시계열, 경량 기기에서의 음성 인식 등 산업계 실무에서는 여전히 비용 효율성 면에서 강력한 선택지다.

> **※ 참고 표준**: Hochreiter & Schmidhuber (1997) "Long Short-Term Memory", Cho et al. (2014) "GRU", Vaswani et al. (2017) "Attention Is All You Need"

---

## 어린이를 위한 종합 설명

**RNN은 "기억력을 가진 똑똑한 책 읽기 로봇"이야!**

```
보통 로봇 (다 까먹음):
문장: "고양이가 쥐를 쫓았다."
1. "고양이" 읽음
2. "쥐" 읽음 (고양이 잊어버림!)
3. "쫓았다" 읽음 (누가 쫓았지? 모름!)

RNN 로봇 (기억함!):
1. "고양이" 읽고 메모함.
2. "쥐" 읽을 때 메모(고양이)를 함께 봄.
3. "쫓았다" 읽을 때 메모(고양이 쥐)를 봄.
→ "아! 고양이가 쥐를 쫓은 거구나!" 이해!
```

**LSTM의 등장**:
```
그런데 너무 긴 문장은 앞부분을 까먹어버렸어.

LSTM = 특수 메모장이 있는 로봇!
- 중요한 단어(주인공, 장소)는 형광펜으로 칠해서
  절대 까먹지 않게 보관!
- 안 중요한 건 과감히 지워버려!

→ 아주 긴 이야기도 끝까지 기억해서 이해해!
```

**GRU**:
```
LSTM이 너무 복잡해서 조금 단순하게 만든 버전이야.
비슷하게 잘하면서 더 빠르고 가볍워!
```

> RNN/LSTM = 기억력 있는 AI! 문맥을 이해하는 비밀! 물론 요즘은 Transformer가 더 똑똑하지만, 가볍고 빨라야 할 때는 여전히 인기 있어!

---
