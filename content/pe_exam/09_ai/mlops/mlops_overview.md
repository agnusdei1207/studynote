+++
title = "MLOps (머신러닝 운영)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# MLOps (Machine Learning Operations)

## 핵심 인사이트 (3줄 요약)
> **MLOps**는 ML 모델의 개발·배포·모니터링·재학습을 자동화·체계화하는 방법론으로 DevOps + ML의 결합이다. 데이터 드리프트·모델 드리프트 감지와 **자동 Continuous Training(CT)** 파이프라인이 핵심이며, 2024년에는 LLM 운영을 위한 **LLMOps**로 확장되었다. 기술사 관점에서 Feature Store·Model Registry·서빙 인프라·모니터링 4대 요소 설계가 핵심이다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: MLOps는 ML 시스템의 설계·개발·배포·운영·모니터링을 통합하여 신뢰할 수 있는 ML 서비스를 지속적으로 제공하는 엔지니어링 방법론이다.

> 비유: "ML 시스템의 공장 자동화 — 모델이라는 제품을 신뢰성 있게 대량 생산·품질관리·납품하는 체계"

**등장 배경**:
- 87% ML 프로젝트 실패: 프로덕션 배포 실패, 모델 성능 저하 방치
- 데이터·모델·코드 삼중 버전 관리 복잡성
- 데이터 드리프트: 배포 후 시간 경과로 예측 성능 자연 저하
- CD4ML(2019, ThoughtWorks) 개념 제시 → MLOps 체계화
- 2022~ LLM 시대: 프롬프트 버전 관리, 파인튜닝 실험, 생성 서빙 → LLMOps 등장

---

### Ⅱ. 구성 요소 및 핵심 원리

**MLOps 3단계 성숙도 (Google)**:
| 단계 | 특징 | 자동화 수준 |
|------|------|----------|
| Level 0 | 수동 ML | 없음 |
| Level 1 | CT 파이프라인 | 데이터·학습 자동화 |
| Level 2 | CI/CD/CT 완전 자동화 | 파이프라인 빌드·배포까지 |

**4대 핵심 구성 요소**:
```
[Feature Store]          [Experiment Tracking]
  ↓                              ↓
피처 등록/서빙           실험 기록 (파라미터·메트릭)
  ↓                              ↓
[ML Pipeline]  ← 데이터 → 학습 → 평가 → 등록 →  [Model Registry]
                                                      ↓
                                               [Model Serving]
                                                      ↓
                                              [Model Monitoring]
                                                 드리프트 감지
                                                      ↓
                                               자동 재학습 트리거
```

**핵심 원리 - CI/CD/CT for ML**:
```
CI (Continuous Integration):
  코드·데이터·모델 변경 → 자동 테스트 → 파이프라인 검증

CD (Continuous Deployment):
  검증 완료 모델 → 자동 배포 (Blue/Green, Canary)

CT (Continuous Training):
  드리프트 감지 / 스케줄 → 자동 재학습 → 새 모델 등록
```

**코드 예시** (MLflow 기반 실험 추적):
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("churn_prediction_v2")

with mlflow.start_run(run_name="RF_v3_hyperopt"):
    # 하이퍼파라미터 기록
    params = {"n_estimators": 200, "max_depth": 10, "min_samples_leaf": 5}
    mlflow.log_params(params)
    
    # 학습
    model = RandomForestClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    
    # 메트릭 기록
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred, average="weighted"),
    }
    mlflow.log_metrics(metrics)
    
    # 모델 저장 + 레지스트리 등록
    mlflow.sklearn.log_model(
        model, "model",
        registered_model_name="churn_rf",
        signature=infer_signature(X_train, y_pred)
    )
    print(f"Run ID: {mlflow.active_run().info.run_id}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + MLOps 툴 비교

**장단점**:
| 장점 | 단점 |
|-----|------|
| 모델 성능 지속적 유지 (드리프트 대응) | 도입 초기 비용 및 복잡성 높음 |
| 재현 가능한 실험 (재현성) | 팀 문화 변화 필요 (DevOps 협업) |
| 빠른 배포 사이클 (CD/CT) | 툴 파편화 (MLflow, W&B, KFP 등) |
| 모델 거버넌스 강화 (감사 추적) | LLM 시대 기존 도구로 한계 |

**MLOps 플랫폼 비교**:
| 도구 | 범위 | 특징 | 적합 환경 |
|------|------|------|--------|
| MLflow | 실험·레지스트리·서빙 | 오픈소스, 범용 | 모든 조직 |
| Kubeflow | 전체 ML 파이프라인 | K8s 기반, K8s 친화 | 대규모 K8s 환경 |
| Weights & Biases | 실험 추적·시각화 | UX 탁월, 팀 협업 | ML 연구팀 |
| SageMaker | 통합 ML 플랫폼 | AWS 네이티브 | AWS 기업 |
| Vertex AI | 통합 ML 플랫폼 | GCP 네이티브 | GCP 기업 |
| ZenML | MLOps 파이프라인 | 클라우드 불가지론 | 멀티클라우드 |

---

### Ⅳ. 실무 적용 방안  ↔  기술사적 판단 + 활용 + 주의사항

**기술사적 판단**:
| 적용 시나리오 | MLOps 전략 | 기대 효과 |
|------------|---------|--------|
| 이상거래 탐지 | 실시간 드리프트 감지 + CT | 탐지율 유지, 재학습 자동화 |
| 추천 시스템 | A/B 테스트 + 챔피언-챌린저 | 클릭률 5~15% 향상 |
| 수요 예측 | 주간 자동 재학습 스케줄 | 예측 오차 20% 감소 |
| LLM 챗봇 | LLMOps: 프롬프트 버전 관리 + Guardrails | 품질 일관성 유지 |

**LLMOps 특수 고려사항**:
```
1. 프롬프트 버전 관리
   → PromptLayer, LangSmith, Phoenix

2. 파인튜닝 실험 추적
   → W&B + HuggingFace Training

3. 환각·안전성 모니터링
   → Guardrails AI, Lakera Guard

4. 비용 모니터링
   → 토큰 사용량 대시보드, 예산 알림

5. 레이턴시 최적화
   → vLLM 서빙, KV Cache 관리
```

**주의사항 / 흔한 실수**:
- **Training-Serving Skew**: 학습 피처와 서빙 피처 불일치 → Feature Store 필수
- **모델 드리프트 방치**: 배포 후 모니터링 없이 방치 → 6개월 내 성능 급락
- **실험 추적 생략**: 어떤 모델이 좋은지 재현 불가 → MLflow/W&B 필수

**관련 개념**: DevOps, CI/CD, Feature Store, Model Registry, Model Monitoring, Kubeflow, LLMOps

---

### Ⅴ. 기대 효과 및 결론  ↔  미래 전망

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 배포 속도 | 자동화로 수주 → 수일 단축 | 배포 주기 10배 단축 |
| 모델 품질 유지 | 드리프트 자동 감지·재학습 | 성능 저하 80% 방지 |
| 운영 비용 | 수동 운영 자동화 | ML 엔지니어 운영 부담 50% 감소 |

> **결론**: MLOps는 "ML 모델의 DevOps" — 데이터·코드·모델 삼중 자동화를 통해 신뢰할 수 있는 AI 서비스를 지속 제공한다. LLM 시대에는 LLMOps로 진화하며, 기술사는 Feature Store·Model Serving·Monitoring·LLMOps를 설계할 수 있어야 한다.  
> **※ 참고**: Google MLOps Whitepaper, Sculley et al. "Hidden Technical Debt in ML Systems"(NIPS 2015)

---

## 어린이를 위한 종합 설명

**MLOps는 "AI 공장 자동화 시스템"이야!**

```
예전에는:
데이터 과학자가 손으로 모델 만들기 → 개발팀에 이메일 전달
→ "이거 어떻게 씁니까?" → 못씀 → 실패!

MLOps가 있으면:
데이터 변경 → 자동 학습 시작 → 자동 테스트 → 자동 배포 → 자동 모니터링
→ 공장처럼 자동으로 돌아가!
```

자동화 단계:
```
1. 데이터 들어옴 → 자동으로 정리·변환
2. 알아서 학습 시작
3. "이전 모델보다 좋음? YES" → 자동 배포
4. 배포 후에도 계속 감시 ("성능 떨어지면 알려줘!")
5. 성능 저하 감지 → 자동으로 다시 학습
```

> MLOps = AI가 혼자 성장하는 자동화 공장! 개발자는 설계만 하면 돼 🏭🤖

---
