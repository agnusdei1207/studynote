+++
title = "연합학습 (Federated Learning)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 연합학습 (Federated Learning)

## 핵심 인사이트 (3줄 요약)
> **연합학습(Federated Learning, FL)**은 데이터를 중앙 서버에 모으지 않고, 각 기기/기관에서 로컬 학습 후 모델 파라미터(Gradient)만 집계하는 분산 ML 기법이다. GDPR, 개인정보보호법 환경에서 **데이터 프라이버시를 보장하면서 협력 학습**이 가능하다. 스마트폰 키보드, 의료 AI, 금융 이상거래 탐지에 실용화되어 있다.

---

### Ⅰ. 개요 (개념 + 등장 배경)

**개념**: 연합학습은 분산된 기기나 기관에서 데이터를 공유하지 않고 각자 학습한 모델 업데이트를 서버에서 집계(Aggregation)하여 글로벌 모델을 개선하는 프라이버시 보존 머신러닝 기법이다.

> 비유: "각 학교 학생들이 시험 답안지를 섞지 않고 각자 공부한 결과만 공유, 선생님이 종합 학습 효과를 모음"

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: 중앙집중식 ML의 한계 - 민감한 의료, 금융, 개인 데이터를 중앙 서버에 수집하는 것이 법적/윤리적으로 불가능
2. **기술적 필요성**: GDPR(2018), 개인정보보호법 등 데이터 현지화, 최소화 원칙 요구. 데이터를 이동시키지 않고 학습하는 방법 필요
3. **시장/산업 요구**: Google Federated Learning(2017) - Gboard 키보드 단어 예측에 최초 적용. 의료 AI - 병원 간 환자 데이터 공유 없이 진단 모델 협력 학습

**핵심 목적**: 데이터 프라이버시를 보장하면서 분산된 데이터로부터 협력 학습으로 더 강력한 모델 구축.

---

### Ⅱ. 구성 요소 및 핵심 원리

**연합학습 기본 구성** (필수: 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **글로벌 서버** | 모델 집계, 라운드 관리 | FedAvg 알고리즘 실행 | 학교 선생님 |
| **로컬 클라이언트** | 로컬 데이터로 학습 | 그라디언트/파라미터 전송 | 각 학교 학생 |
| **통신 프로토콜** | 모델 파라미터 교환 | 압축, 암호화 포함 | 답안 전송 방법 |
| **집계 알고리즘** | 클라이언트 업데이트 결합 | FedAvg, FedProx, FedNova | 성적 집계 방식 |
| **보안 메커니즘** | 프라이버시 강화 | 차등 프라이버시, 동형암호, 시큐어 집계 | 답안 비공개 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Federated Learning Architecture                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────┐      │
│   │                    Central Server                             │      │
│   │  ┌─────────────────────────────────────────────────────┐    │      │
│   │  │              Global Model W_t                        │    │      │
│   │  │                                                     │    │      │
│   │  │         Aggregation: FedAvg, FedProx               │    │      │
│   │  │         W_{t+1} = Σ (n_k/n) × W_k^t                │    │      │
│   │  └─────────────────────────────────────────────────────┘    │      │
│   │                          ↑↓                                  │      │
│   │              Distribute & Aggregate                          │      │
│   └─────────────────────────────────────────────────────────────┘      │
│                              ↑↓                                        │
│     ┌───────────────────────┼───────────────────────┐                 │
│     │                       │                       │                  │
│     ↓                       ↓                       ↓                  │
│ ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│ │ Client 1 │          │ Client 2 │          │ Client K │              │
│ │ (병원 A) │          │ (병원 B) │          │ (병원 C) │              │
│ ├──────────┤          ├──────────┤          ├──────────┤              │
│ │ Local    │          │ Local    │          │ Local    │              │
│ │ Data D_1 │          │ Data D_2 │          │ Data D_K │              │
│ │ (환자X)  │          │ (환자Y)  │          │ (환자Z)  │              │
│ │          │          │          │          │          │              │
│ │ Local    │          │ Local    │          │ Local    │              │
│ │ Training │          │ Training │          │ Training │              │
│ │     ↓    │          │     ↓    │          │     ↓    │              │
│ │ ΔW_1     │          │ ΔW_2     │          │ ΔW_K     │              │
│ └──────────┘          └──────────┘          └──────────┘              │
│                                                                         │
│   Key: 데이터는 로컬에 유지! 파라미터만 전송!                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

FedAvg Algorithm Flow:
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   Round t 반복:                                                         │
│                                                                         │
│   1. 서버: 글로벌 모델 W_t를 K개 클라이언트에 배포                       │
│                              ↓                                          │
│   2. 클라이언트 k (병렬):                                               │
│      - 로컬 데이터 D_k로 E 에폭 학습                                    │
│      - 로컬 업데이트 W_k^t 계산                                         │
│                              ↓                                          │
│   3. 서버: 가중 평균 집계                                               │
│      W_{t+1} = Σ (|D_k|/|D|) × W_k^t                                   │
│                              ↓                                          │
│   4. t+1 라운드 반복                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 모델 배포 → ② 로컬 학습 → ③ 업데이트 전송 → ④ 집계 → ⑤ 글로벌 모델 갱신 → ⑥ 반복
```

- **1단계 (모델 배포)**: 중앙 서버가 현재 글로벌 모델 W_t를 선택된 클라이언트들에 배포
- **2단계 (로컬 학습)**: 각 클라이언트가 자신의 로컬 데이터 D_k로 E 에폭 동안 학습
- **3단계 (업데이트 전송)**: 학습된 로컬 모델 또는 그라디언트 ΔW_k를 서버에 전송 (데이터는 전송 안 함)
- **4단계 (집계)**: 서버가 FedAvg 알고리즘으로 가중 평균 집계
- **5단계 (글로벌 모델 갱신)**: W_{t+1} = Σ (n_k/n) × W_k^t
- **6단계 (반복)**: 수렴할 때까지 T 라운드 반복

**핵심 알고리즘/공식** (해당 시 필수):

**FedAvg (Federated Averaging)**:
```
FedAvg 집계:
W_{t+1} = Σ_{k=1}^{K} (n_k / n) × W_k^t

W_k^t: 클라이언트 k의 로컬 모델
n_k: 클라이언트 k의 데이터 수
n: 전체 데이터 수 (Σ n_k)
K: 참여 클라이언트 수

특징: 데이터가 많은 클라이언트가 글로벌 모델에 더 큰 영향
```

**FedProx (Non-IID 대응)**:
```
FedProx 목적함수:
min_w Σ_{k=1}^{K} (n_k/n) × F_k(w) + (μ/2) × ||w - w^t||²

μ: 근접 항(proximal term) 계수
→ 로컬 최적해와 글로벌 모델 간 거리 제한
→ Non-IID 데이터에서 수렴 안정화
```

**코드 예시** (필수: Python):

```python
import flwr as fl
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# 1. 간단한 신경망 모델 정의
class SimpleNet(nn.Module):
    def __init__(self, input_size=20, hidden_size=64, output_size=2):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# 2. Flower 클라이언트 정의
class FlowerClient(fl.client.NumPyClient):
    """Flower 프레임워크 기반 연합학습 클라이언트"""

    def __init__(self, model, trainloader, valloader):
        self.model = model
        self.trainloader = trainloader
        self.valloader = valloader
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def get_parameters(self, config):
        """서버에 현재 모델 파라미터 반환"""
        return [val.cpu().numpy() for val in self.model.state_dict().values()]

    def set_parameters(self, parameters):
        """서버에서 받은 글로벌 모델 파라미터 적용"""
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        """로컬 학습 (클라이언트 사이드)"""
        self.set_parameters(parameters)

        # 로컬 학습 설정
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        criterion = nn.CrossEntropyLoss()
        local_epochs = config.get("local_epochs", 1)

        self.model.train()
        for _ in range(local_epochs):
            for X, y in self.trainloader:
                X, y = X.to(self.device), y.to(self.device)
                optimizer.zero_grad()
                loss = criterion(self.model(X), y)
                loss.backward()
                optimizer.step()

        return self.get_parameters({}), len(self.trainloader.dataset), {}

    def evaluate(self, parameters, config):
        """로컬 평가"""
        self.set_parameters(parameters)
        criterion = nn.CrossEntropyLoss()

        loss, correct = 0.0, 0
        self.model.eval()
        with torch.no_grad():
            for X, y in self.valloader:
                X, y = X.to(self.device), y.to(self.device)
                pred = self.model(X)
                loss += criterion(pred, y).item()
                correct += (pred.argmax(1) == y).sum().item()

        accuracy = correct / len(self.valloader.dataset)
        return loss, len(self.valloader.dataset), {"accuracy": accuracy}


# 3. 클라이언트 생성 함수
def create_client(cid: str, data_fraction=0.1):
    """각 클라이언트에 데이터 분할"""
    # 더미 데이터 생성 (실제로는 각 기관의 로컬 데이터)
    np.random.seed(int(cid))
    n_samples = 1000
    X = np.random.randn(n_samples, 20).astype(np.float32)
    y = np.random.randint(0, 2, n_samples).astype(np.int64)

    # DataLoader 생성
    dataset = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    train_size = int(0.8 * len(dataset))
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, len(dataset) - train_size]
    )

    trainloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    valloader = DataLoader(val_dataset, batch_size=32)

    model = SimpleNet()
    return FlowerClient(model, trainloader, valloader)


# 4. 서버 측 집계 전략
def get_server_strategy():
    """FedAvg 집계 전략 설정"""
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=0.3,        # 각 라운드에 30% 클라이언트 참여
        fraction_evaluate=0.3,   # 평가에 30% 참여
        min_fit_clients=2,       # 최소 학습 클라이언트 수
        min_evaluate_clients=2,  # 최소 평가 클라이언트 수
        min_available_clients=3, # 최소 사용 가능 클라이언트
    )
    return strategy


# 5. 연합학습 실행
def run_federated_learning():
    """연합학습 메인 실행"""
    # 서버 시작 (별도 프로세스)
    # fl.server.start_server(
    #     server_address="0.0.0.0:8080",
    #     config=fl.server.ServerConfig(num_rounds=10),
    #     strategy=get_server_strategy(),
    # )

    # 클라이언트 시작 (각 기관에서 실행)
    client = create_client("1")
    fl.client.start_numpy_client(server_address="0.0.0.0:8080", client=client)


# 6. 차등 프라이버시 (Differential Privacy) 적용
class DPFlowerClient(FlowerClient):
    """차등 프라이버시가 적용된 클라이언트"""

    def __init__(self, model, trainloader, valloader, noise_multiplier=1.0):
        super().__init__(model, trainloader, valloader)
        self.noise_multiplier = noise_multiplier

    def get_parameters(self, config):
        """그라디언트에 노이즈 추가 (DP)"""
        params = super().get_parameters(config)

        # Gaussian 노이즈 추가
        noisy_params = []
        for param in params:
            noise = np.random.normal(0, self.noise_multiplier * np.std(param), param.shape)
            noisy_params.append(param + noise.astype(np.float32))

        return noisy_params


# 7. Non-IID 데이터 분할 시뮬레이션
def create_noniid_data(n_clients=5, n_classes=2):
    """Non-IID 데이터 분할 (클래스 불균형)"""
    all_data = []

    for client_id in range(n_clients):
        # 각 클라이언트는 특정 클래스에 편향됨
        dominant_class = client_id % n_classes
        n_samples = 1000
        class_ratio = 0.8  # 80%가 dominant class

        X = np.random.randn(n_samples, 20).astype(np.float32)
        y = np.zeros(n_samples, dtype=np.int64)
        y[:int(n_samples * class_ratio)] = dominant_class
        y[int(n_samples * class_ratio):] = 1 - dominant_class

        all_data.append((X, y))

    return all_data


# 메인 실행 예시
if __name__ == "__main__":
    print("=== Federated Learning with Flower ===")
    print("서버와 클라이언트를 별도 프로세스로 실행해야 합니다.")
    print("\n서버 실행:")
    print("  python -c 'import flwr as fl; fl.server.start_server(...)'")
    print("\n클라이언트 실행:")
    print("  python this_script.py --client")
```

---

### Ⅲ. 기술 비교 분석 (장단점 + 학습 방식 비교)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| 데이터 프라이버시 보장 (데이터 미이동) | Non-IID 문제 (클라이언트 간 데이터 이질성) |
| 규제 준수 (GDPR, 개인정보보호법) | 통신 비용 (파라미터 전송 오버헤드) |
| 데이터 현지화 유지 (법적 요구 충족) | 수렴 속도 느림 (분산 학습 특성) |
| 디바이스 이질성 대응 가능 | 독성 공격 (Poisoning Attack) 취약 |
| 다양한 기관 간 협력 학습 | 클라이언트 드롭아웃 (Straggler) |

**학습 방식 비교** (필수: 최소 2개 대안):

| 비교 항목 | 중앙집중식 | 연합학습 | 분산학습 | 스플릿 러닝 |
|---------|-----------|---------|---------|----------|
| 핵심 특성 | 데이터 중앙 집결 | ★ 데이터 로컬 유지 | 데이터 분산 저장 | 모델 분할 |
| 데이터 위치 | 서버 | 클라이언트 | 공유 | 분할 |
| 프라이버시 | 낮음 | ★ 높음 | 낮음 | 중간 |
| 통신 비용 | 없음 | 중간 | 높음 | 중간 |
| 적합 환경 | 데이터 공유 가능 | 프라이버시 중요 | 대규모 빠른 학습 | IoT 융합 |

> **★ 선택 기준**:
> - **프라이버시 필수 (의료/금융)**: 연합학습
> - **빠른 학습 우선**: 중앙집중식 (데이터 이동 가능 시)
> - **IoT/엣지 디바이스**: 스플릿 러닝 또는 연합학습
> - **대규모 데이터센터**: 분산학습

**집계 알고리즘 비교**:

| 알고리즘 | 특징 | 장점 | 단점 |
|---------|------|------|------|
| ★ FedAvg | 가중 평균 | 단순, 효과적 | Non-IID에 취약 |
| FedProx | 근접 항 추가 | Non-IID 안정 | 하이퍼파라미터 μ |
| FedNova | 정규화된 평균 | 이질성 보정 | 복잡도 증가 |
| SCAFFOLD | 제어 변수 사용 | 빠른 수렴 | 메모리 증가 |
| FedAdam | 적응형 옵티마이저 | 빠른 수렴 | 하이퍼파라미터 많음 |

---

### Ⅳ. 실무 적용 방안 (기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **Google Gboard** | 스마트폰 키보드 다음 단어 예측 | 개인 타이핑 데이터 수집 없이 예측 정확도 10% 향상 |
| **의료 (병원 컨소시엄)** | 병원 간 암 진단 모델 협력 학습 | 환자 데이터 미공유 + 진단 정확도 15% 향상 |
| **금융 (이상거래 탐지)** | 은행 간 사기 패턴 공유 | 개인정보 미노출 + 탐지율 20% 향상 |
| **자율주행** | 차량 간 주행 데이터 협력 | 개인화 운전 데이터 보호 + 학습 속도 3배 |
| **IoT 스마트공장** | 설비 고장 예측 모델 협력 | 공장 데이터 유출 없이 + 예측 정확도 90%+ |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Google Gboard** - 스마트폰 사용자의 타이핑 데이터를 서버로 전송하지 않고, 기기 내에서 학습 후 모델 업데이트만 전송. 수억 명 사용자의 프라이버시 보호하며 다음 단어 예측 정확도 향상.
- **사례 2: NVIDIA Clara FL** - 의료 영상 AI를 위한 연합학습 플랫폼. 여러 병원이 환자 데이터를 공유하지 않고 협력 학습. COVID-19 CT 영상 분석 모델 등 개발.
- **사례 3: WeBank (중국)** - 금융 기관 간 신용평가 모델 협력 학습. 각 은행의 고객 데이터를 공유하지 않고 이상거래 탐지 모델 개발.

**프라이버시 강화 기법**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Privacy Enhancement Techniques                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 차등 프라이버시 (Differential Privacy, DP)                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  그라디언트에 Gaussian/Laplacian 노이즈 추가             │   │
│  │  ε-DP: 데이터 비공개 수학적 보장                         │   │
│  │  Trade-off: ε↓ (프라이버시↑) ↔ 정확도↓                  │   │
│  │                                                          │   │
│  │  ΔW_DP = ΔW + N(0, σ²)  (σ = sensitivity/ε)             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  2. 동형암호 (Homomorphic Encryption, HE)                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  암호화된 데이터로 직접 연산 가능                        │   │
│  │  E(a) + E(b) = E(a+b)                                   │   │
│  │  → 서버도 원본 파라미터 접근 불가                        │   │
│  │  단점: 연산 비용 매우 높음 (100~1000배)                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  3. 시큐어 집계 (Secure Aggregation)                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  개별 클라이언트 업데이트는 서버에 비공개                │   │
│  │  집계 결과(합계)만 서버 확인 가능                        │   │
│  │  암호화 합계: Σ encrypted(ΔW_k) = encrypted(Σ ΔW_k)     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: Non-IID 데이터 대응 (FedProx, SCAFFOLD), 통신 압축 (Gradient Compression), 클라이언트 선택 전략
2. **운영적**: 클라이언트 드롭아웃 대응, 비동기 집계, 모델 버전 관리
3. **보안적**: 독성 공격(Poisoning) 방어, 추론 공격(Inference Attack) 대응, 차등 프라이버시 적용
4. **경제적**: 통신 비용 vs 중앙집중식 학습 비용 비교, 엣지 디바이스 컴퓨팅 자원 고려

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **Non-IID 무시**: 클라이언트 간 데이터 분포 차이로 성능 저하. 해결: FedProx, 데이터 공유 일부 허용
- ❌ **독성 공격 방어 미흡**: 악의적 클라이언트가 잘못된 업데이트 전송. 해결: Byzantine-robust 집계, 이상치 탐지
- ❌ **과도한 통신 비용**: 압축 없이 전체 파라미터 전송. 해결: Gradient Compression, Sparse 업데이트
- ❌ **클라이언트 드롭아웃**: 불안정한 네트워크로 참여율 저하. 해결: 비동기 집계, 충분한 클라이언트 풀

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  Federated Learning 핵심 연관 개념 맵                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [Differential Privacy] ←──→ [Federated Learning] ←──→ [Secure│
│            ↓                         ↓                    Aggregation]   │
│   [동형암호]                    [FedAvg/FedProx]              ↓        │
│            ↓                         ↓                    [Byzantine│
│   [GDPR] ←──→ [Privacy-Preserving ML] ←──→ [Poisoning Defense]│
│                                     ↓                           │
│                              [Distributed ML]                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 차등 프라이버시 | 프라이버시 강화 | 노이즈 추가로 개인정보 보호 | `[differential_privacy](./differential_privacy.md)` |
| 분산학습 | 유사 기술 | 데이터 분산 저장 학습 | `[distributed_learning](./distributed_learning.md)` |
| 동형암호 | 보안 기술 | 암호화된 상태로 연산 | `[homomorphic_encryption](./homomorphic_encryption.md)` |
| MLOps | 운영 체계 | ML 모델 배포 관리 | `[mlops](../mlops/mlops_overview.md)` |
| 기계학습 기초 | 상위 개념 | ML의 기본 패러다임 | `[machine_learning](./machine_learning.md)` |
| GDPR | 법적 요구 | 데이터 보호 규정 | `[gdpr](./gdpr.md)` |

---

### Ⅴ. 기대 효과 및 결론 (미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 프라이버시 보장 | GDPR 준수 + 데이터 유출 감소 | 법적 리스크 90% 감소 |
| 모델 품질 | 다양한 분산 데이터 학습 | 중앙집중식 대비 80~90% 성능 |
| 협력 생태계 | 데이터 고립 문제 극복 | 미활용 데이터 AI 학습 활용 |
| 규제 준수 | 개인정보보호법, GDPR 충족 | 법적 컴플라이언스 100% |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: Cross-silo FL (기관 간), Cross-device FL (수십억 기기), Personalized FL (개인화)
2. **시장 트렌드**: EU AI Act, GDPR 시대에 필수 기술, 의료, 금융, 자동차 산업 표준화
3. **후속 기술**: Federated Analytics (분석만), Split Learning, Swarm Learning

> **결론**: 연합학습은 "데이터 프라이버시와 AI 협력의 타협점". EU AI Act, GDPR 시대에 의료, 금융, 자동차 산업 필수 기술로 자리잡고 있다. 기술사는 FedAvg 알고리즘, Non-IID 대응, 독성 공격 방어, 차등 프라이버시 설계를 핵심 역량으로 갖춰야 한다.

> **※ 참고 표준**: McMahan et al. (2017) "Communication-Efficient Learning of Deep Networks from Decentralized Data", Li et al. (2020) "Federated Optimization in Heterogeneous Networks", Google AI Blog (2017) Federated Learning

---

## 어린이를 위한 종합 설명

**연합학습은 "비밀 노트 없이 함께 공부하는 방법"이야!**

```
문제: 여러 병원이 AI를 만들려면?
환자 기록을 한곳에 모아야 하는데... → 개인정보 법 위반!

연합학습 해결법:
병원 A: 자기 환자로 AI 학습 → 학습 결과(공식)만 보냄
병원 B: 자기 환자로 AI 학습 → 학습 결과(공식)만 보냄
병원 C: 자기 환자로 AI 학습 → 학습 결과(공식)만 보냄
                           ↓
중앙 서버: 공식들을 합쳐서 → 더 똑똑한 AI 완성!
→ 환자 데이터는 각 병원에 그대로! 아무도 남의 데이터를 못 봐!
```

비밀 유지 마법들:
```
1. 차등 프라이버시: 숙제에 살짝 지저분한 낙서 추가 → 누가 뭘 썼는지 모름!
2. 동형암호: 비밀 암호로 쓴 숙제 → 선생님도 내용 모르지만 채점은 가능!
3. 시큐어 집계: 반 전체 점수만 공개 → 개인 점수는 비밀!
```

> 연합학습 = 비밀 레시피는 공개 안 하면서 요리 실력은 함께 키우는 방법! 협력은 하되 비밀은 지키는 똑똑한 기술!

---
