+++
title = "연합학습 (Federated Learning)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 연합학습 (Federated Learning)

## 핵심 인사이트 (3줄 요약)
> **연합학습**은 데이터를 중앙 서버에 모으지 않고, 각 기기/기관에서 로컬 학습 후 모델 파라미터(Gradient)만 집계하는 분산 ML 기법이다. GDPR·개인정보보호법 환경에서 **데이터 프라이버시를 보장하면서 협력 학습**이 가능하다. 스마트폰 키보드·의료 AI·금융 이상거래 탐지에 실용화되어 있다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: 연합학습은 분산된 기기나 기관에서 데이터를 공유하지 않고 각자 학습한 모델 업데이트를 서버에서 집계(Aggregation)하여 글로벌 모델을 개선하는 프라이버시 보존 머신러닝 기법이다.

> 비유: "각 학교 학생들이 시험 답안지를 섞지 않고 각자 공부한 결과만 공유, 선생님이 종합 학습 효과를 모음"

**등장 배경**:
- 중앙집중식 ML 한계: 민감한 의료·금융·개인 데이터 수집 불가
- GDPR(2018)·개인정보보호법: 데이터 현지화·최소화 원칙
- **Google Federated Learning(2017)**: Gboard 키보드 단어 예측에 최초 적용
- 의료 AI: 병원 간 환자 데이터 공유 없이 진단 모델 협력 학습

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소**:
| 구성 요소 | 역할 |
|----------|------|
| 글로벌 서버 | 모델 집계 (FedAvg), 라운드 관리 |
| 로컬 클라이언트 | 로컬 데이터로 학습, 그라디언트 전송 |
| 통신 프로토콜 | 모델 파라미터 교환 (압축 포함) |
| 집계 알고리즘 | FedAvg, FedProx, FedNova |
| 보안 메커니즘 | 차등 프라이버시(DP), 동형암호, 시큐어 집계 |

**핵심 원리 - FedAvg 알고리즘**:
```
[글로벌 라운드 t 반복]

1. 서버: 글로벌 모델 W_t를 K개 클라이언트에 배포
2. 클라이언트 k (병렬):
   - 로컬 데이터 D_k로 E 에폭 학습
   - 로컬 업데이트 ΔW_k = W_t - W_t^k 계산
3. 서버: 가중 평균 집계
   W_{t+1} = Σ (|D_k|/|D|) × W_t^k
4. t+1 라운드 반복

FedAvg 집계:
데이터 크기에 비례하여 클라이언트 모델의 가중 평균
→ 데이터가 많은 클라이언트가 글로벌 모델에 더 큰 영향
```

**코드 예시** (Flower 프레임워크 기반):
```python
import flwr as fl
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# 클라이언트 정의
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, trainloader, valloader):
        self.model = model
        self.trainloader = trainloader
        self.valloader = valloader
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def get_parameters(self, config):
        """서버에 현재 모델 파라미터 반환"""
        return [val.cpu().numpy() for val in self.model.state_dict().values()]
    
    def set_parameters(self, parameters):
        """서버에서 받은 글로벌 모델 파라미터 적용"""
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.model.load_state_dict(state_dict)
    
    def fit(self, parameters, config):
        """로컬 학습"""
        self.set_parameters(parameters)
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        
        self.model.train()
        for _ in range(config.get("local_epochs", 1)):
            for X, y in self.trainloader:
                optimizer.zero_grad()
                loss = nn.CrossEntropyLoss()(self.model(X.to(self.device)), y.to(self.device))
                loss.backward()
                optimizer.step()
        
        return self.get_parameters({}), len(self.trainloader.dataset), {}
    
    def evaluate(self, parameters, config):
        """로컬 평가"""
        self.set_parameters(parameters)
        loss, correct = 0.0, 0
        self.model.eval()
        with torch.no_grad():
            for X, y in self.valloader:
                pred = self.model(X.to(self.device))
                loss += nn.CrossEntropyLoss()(pred, y.to(self.device)).item()
                correct += (pred.argmax(1) == y.to(self.device)).sum().item()
        return loss, len(self.valloader.dataset), {"accuracy": correct/len(self.valloader.dataset)}

# 서버에서 집계 전략 설정
strategy = fl.server.strategy.FedAvg(
    fraction_fit=0.3,    # 30% 클라이언트 참여
    min_fit_clients=2,
    min_available_clients=2,
)

fl.server.start_server(
    server_address="0.0.0.0:8080",
    config=fl.server.ServerConfig(num_rounds=10),
    strategy=strategy,
)
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + 학습 방식 비교

**장단점**:
| 장점 | 단점 |
|-----|------|
| 데이터 프라이버시 보장 | Non-IID 문제 (클라이언트 간 데이터 이질성) |
| 규제 준수 (GDPR 친화) | 통신 비용 (파라미터 전송) |
| 데이터 현지화 유지 | 수렴 속도 느림 |
| 디바이스 이질성 대응 가능 | 독성 공격 (Poisoning Attack) 취약 |

**학습 방식 비교**:
| 방식 | 데이터 위치 | 프라이버시 | 통신 비용 | 적합 환경 |
|------|---------|--------|--------|--------|
| 중앙집중식 | 서버 | 낮음 | 없음 | 데이터 공유 가능 |
| 연합학습 | 클라이언트 | 높음 | 중간 | 프라이버시 중요 |
| 분산학습 | 공유 | 낮음 | 높음 | 대규모 빠른 학습 |
| 스플릿 러닝 | 분할 | 중간 | 중간 | IoT 융합 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 시나리오 | 기대 효과 |
|---------|--------|--------|
| Google Gboard | 스마트폰 키보드 다음 단어 예측 | 개인 타이핑 데이터 수집 없이 개선 |
| 의료 (병원 컨소시엄) | 병원 간 암 진단 모델 협력 | 환자 데이터 미공유 + 진단 정확도↑ |
| 금융 (이상거래 탐지) | 은행 간 사기 패턴 공유 | 개인정보 미노출 + 탐지율↑ |
| 자율주행 | 차량 간 주행 데이터 협력 | 개인화 운전 데이터 보호 |
| IoT 스마트공장 | 설비 고장 예측 모델 협력 | 공장 데이터 유출 없이 학습 |

**프라이버시 강화 기법**:
```
1. 차등 프라이버시 (DP)
   그라디언트에 Gaussian 노이즈 추가
   ε-DP: 데이터 비공개 수학적 보장

2. 동형암호 (HE)
   암호화된 데이터로 직접 학습
   → 서버도 원본 데이터 접근 불가

3. 시큐어 집계 (Secure Aggregation)
   개별 업데이트는 서버에 비공개
   → 집계 결과만 서버 확인
```

**관련 개념**: 차등 프라이버시, 동형암호, FedAvg, 분산학습, GDPR, 전이학습

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 프라이버시 보장 | GDPR 준수 + 데이터 유출 감소 | 법적 리스크 90% 감소 |
| 모델 품질 | 다양한 분산 데이터 학습 | 중앙집중식 대비 80~90% 성능 |
| 협력 생태계 | 데이터 고립 문제 극복 | 미활용 데이터 AI 학습 활용 |

> **결론**: 연합학습은 "데이터 프라이버시와 AI 협력의 타협점". EU AI Act·GDPR 시대에 의료·금융·자동차 산업 필수 기술로 자리잡고 있다. 기술사는 FedAvg 알고리즘·Non-IID 대응·독성 공격 방어·차등 프라이버시 설계를 핵심 역량으로 갖춰야 한다.

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

> 연합학습 = 비밀 레시피는 공개 안 하면서 요리 실력은 함께 키우는 방법! 🏥🔒📊

---
