---
title: "Data Drift Concept Drift Detection"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 750
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 드리프트는 입력 Feature의 분포 $P(X)$가 변화하는 현상이고, 개념 드리프트는 조건부 확률 $P(Y|X)$의 관계가 변화하는 현상으로서, MLOps 파이프라인에서 모델 성능 열화(Model Decay)의 근본 원인이 되며 통계적 거리(KL-divergence, Wasserstein, PSI) 및 적응형 윈도우(ADWIN, Page-Hinkley) 기반 탐지 알고리즘으로 식별한다.
> 2. **가치**: 실시간 모니터링 자동화를 통해 모델 정확도 하락을 5~30% 조기 감지하여 비즈니스 손실을 절감하고, 재학습 트리거(Retraining Trigger)와의 연동으로 MTTR(Mean Time To Recovery)을 평균 72시간 -> 6시간 이하로 단축할 수 있다.
> 3. **판단 포인트**: 통계적 검정(KS-test, Chi-square) vs 거리 기반(PSI, JS-divergence) vs 모델 기반(Domain Classifier, Page-Hinkley) 알고리즘의 선택, 참조 윈도우(Reference Window)와 검출 윈도우(Detection Window) 크기 결정, 그리고 다중 테스팅(Multiple Testing) 문제로 인한 False Positive 통제(예: Benjamini-Hochberg 보정)가 핵심 의사결정 요인이다.

---

## Ⅰ. 개요 및 필요성

머신러닝 모델은 학습 시점의 데이터 분포를 정적으로 가정하고 일반화(Generalization)한다. 그러나 실제 운영 환경(Production)에서는 시간의 경과, 사용자 행동 변화, 외부 환경 변화, 데이터 파이프라인의 결함 등으로 인해 입력 데이터의 통계적 특성이 변화하며, 이로 인해 모델의 예측 성능이 점진적 또는 급진적으로 열화된다. 이를 총칭하여 **분포 변화(Distribution Shift)**라 하며, 학계와 업계에서는 이를 **데이터 드리프트(Data Drift)**, **개념 드리프트(Concept Drift)**, **라벨 드리프트(Label Drift)**의 세 가지 범주로 정형화하여 다루고 있다(Garcia et al., "A Survey on Concept Drift Adaptation", IEEE TPAMI 2022).

MLPerf와 같은 벤치마크 및 산업계 보고서에 따르면, ML 모델의 약 91%가 6개월 이내 운영 환경에서 성능 열화를 경험하며, 그중 63%가 드리프트를 인지하지 못한 채 운영되는 것으로 조사되었다. 특히 금융(사기 탐지), 의료(진단 보조), 추천 시스템, 자율주행 등의 영역에서는 드리프트에 따른 예측 오류가 직접적 비즈니스 리스크와 인명 피해로 이어지므로, **지속적 모니터링(Continuous Monitoring)**과 **자동 재학습(Automated Retraining)** 체계가 필수적이다.

```text
[Data Drift vs Concept Drift vs Label Drift 시각화]

  시간축(t=0 -> t=1 -> t=2)에서의 변화 비교

  ① 데이터 드리프트 (Covariate Shift): P(X) 변화, P(Y|X) 불변
  +----------------------------------------------------+
  | t=0:  ███░░░██░      P(X) = N(0,1)                |
  | t=1:  ░███████░      P'(X) = N(2,1.5)             |
  | t=2:  ░░░█████░      P''(X) = N(3,1.0)            |
  |                                                     |
  | Feature X 분포 이동 -> 입력 패턴 변화                 |
  +----------------------------------------------------+

  ② 개념 드리프트 (Real Concept Drift): P(Y|X) 변화
  +----------------------------------------------------+
  | t=0:  Y=1 if X>0.5 (결정경계)                       |
  | t=1:  Y=1 if X>0.3  (경계 이동)                     |
  | t=2:  Y=1 if X>0.7  (경계 재이동)                  |
  |                                                     |
  | 동일한 X에 대한 Y의 매핑 규칙 변화                    |
  +----------------------------------------------------+

  ③ 라벨 드리프트 (Prior Probability Shift): P(Y) 변화
  +----------------------------------------------------+
  | t=0:  P(Y=1) = 0.1  (불균형)                       |
  | t=1:  P(Y=1) = 0.4  (증가)                         |
  | t=2:  P(Y=1) = 0.7  (지배적)                       |
  |                                                     |
  | 클래스 비율 변화 -> 임계값 재조정 필요                 |
  +----------------------------------------------------+

  ※ 실제 운영 환경에서는 ①+②+③가 혼합되어 발생하며,
    MLOps 파이프라인은 각 차원을 분리하여 진단해야 한다.
```

전통적 통계 모델은 **ERM(Empirical Risk Minimization)** 가정 하에 학습-테스트 분포가 동일(i.i.d.)하다고 가정하지만, 운영 환경에서는 **Non-stationary** 환경이므로, Vapnik의 **Transductive Reasoning** 및 Sugiyama의 **Importance Weighting** 이론을 적용하여 분포 차이를 정량화해야 한다. 최근에는 **Foundation Model** 시대가 도래하면서도 도메인 특화 모델의 드리프트 문제는 여전하며, 오히려 LLM의 응답 드리프트(예: Hallucination Rate 변화, Toxicity Score 변화)까지 모니터링 대상으로 확장되고 있다.

- **📢 섹션 요약 비유**: 데이터 드리프트는 '지하철역 유동인구의 변화'(20대 많음 -> 50대 많아짐)이고, 개념 드리프트는 '같은 신호등에서도 빨간불이 '멈춤'이라는 의미가 사회적 합의로 바뀌는 것'입니다. 데이터는 같아 보여도 그 의미는 시시각각 변합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

드리프트 탐지 시스템은 일반적으로 **참조 데이터(Reference Data)**와 **현재 데이터(Current/Incoming Data)**의 두 분포를 비교하는 구조를 갖는다. 핵심 파이프라인은 (1) 데이터 수집 -> (2) 통계적/ML 기반 비교 -> (3) 임계치(Threshold) 판정 -> (4) 알림/트리거 발생 -> (5) 재학습 오케스트레이션의 5단계로 구성된다.

```text
[End-to-End MLOps 드리프트 탐지 아키텍처]

+----------------------------------------------------------------------+
|                         Production Environment                       |
|  +----------+    +----------+    +----------+    +--------------+   |
|  | Data     |---->| Feature  |---->| Inference|---->| Prediction   |   |
|  | Source   |    | Store    |    | Service  |    | Log (Kafka)  |   |
|  | (Kafka,  |    | (Redis,  |    | (TF Serv,|    |              |   |
|  |  Kinesis)|    |  Feast)  |    |  Triton) |    +------+-------+   |
|  +----+-----+    +----+-----+    +----+-----+           |           |
|       |               |               |                 |           |
|       v               v               v                 v           |
|  +--------------------------------------------------------------+   |
|  |         Streaming Data Lake (S3 / GCS / HDFS)                |   |
|  |         Reference:  +- D+0 ~ D-30  (학습/검증 데이터셋)       |   |
|  |         Current:    +- D-30 ~ D+0  (운영 추론 데이터셋)       |   |
|  +--------------------------------------------------------------+   |
+----------------------------------------------------------------------+
                                |
                                v
+----------------------------------------------------------------------+
|                    Drift Detection Layer                              |
|                                                                       |
|   +-----------------+  +-----------------+  +-----------------+     |
|   | Feature Monitor |  | Label Monitor   |  | Prediction Mon. |     |
|   | (Univariate)    |  | (Post-hoc)      |  | (Score Distrib) |     |
|   |                 |  |                 |  |                 |     |
|   | • KS-test       |  | • Chi-square    |  | • JS-divergence |     |
|   | • PSI / CSI     |  | • Class balance |  | • Confidence Δ  |     |
|   | • Wasserstein   |  | • CMOCU         |  | • Calibration   |     |
|   +--------+--------+  +--------+--------+  +--------+--------+     |
|            +--------------------+--------------------+              |
|                                 v                                    |
|              +----------------------------------+                    |
|              |  Multivariate Detector           |                    |
|              |  • MMD (Maximum Mean Discrep.)   |                    |
|              |  • Domain Classifier (H-divergence)|                  |
|              |  • Reconstruction Error (VAE)    |                    |
|              +--------------+-------------------+                    |
|                             v                                        |
|              +----------------------------------+                    |
|              |  Statistical Process Control     |                    |
|              |  • ADWIN, Page-Hinkley, CUSUM    |                    |
|              |  • EWMA Charts                   |                    |
|              +--------------+-------------------+                    |
+-----------------------------+----------------------------------------+
                              v
              +--------------------------------------+
              |   Decision & Orchestration Layer     |
              |                                       |
              |  Drift Score ---> Threshold Logic     |
              |     |                |                |
              |     |      +---------+---------+     |
              |     |      v                   v     |
              |     |  Warning Zone      Drift Zone  |
              |     |  (0.1<PSI<0.25)   (PSI≥0.25)  |
              |     |      |                |        |
              |     +------+----------------+--------+
              |            v                v
              |       Alert (Slack)   Trigger Retrain |
              |       Dashboard       (Argo/Kubeflow) |
              +--------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Feature Monitor (단변량)** | 각 Feature별 분포 변화 독립 검출 | KS-test(연속형), Chi-square(범주형), PSI($\sum (p_{ref} - p_{cur}) \ln \frac{p_{ref}}{p_{cur}}$), CSI(특성별 PSI) — PSI≥0.1: 약간 변화, ≥0.25: 유의미한 변화 |
| **Multivariate Detector (다변량)** | Feature 간 결합 분포(Joint Distribution) 변화 검출 | MMD(Maximum Mean Discrepancy), Hotelling's T², Domain Classifier(AUC≈0.5이면 분포 동일), Reconstruction Error 기반 VAE/Autoencoder |
| **Performance Monitor** | 라벨이 지연 수집되는 경우 예측 성능 직접 모니터링 | CMOCU(Confidence Margin-based Concept-drift), 슬라이딩 윈도우 정확도, Calibration Drift(ECE: Expected Calibration Error) |
| **Sequential Detector** | 시계열적 통계 변화점(Change Point) 식별 | ADWIN(적응형 윈도우), Page-Hinkley(누적합 검정), CUSUM, Bayesian Online Change Point Detection(BOCPD) |
| **Orchestrator** | 알림·재학습·롤백 트리거 통합 | Argo Workflows, Kubeflow Pipelines, Airflow DAG, Evidently AI/NannyML/Whylogs SDK 통합 |

### 핵심 수식 및 알고리즘 심화

**① PSI (Population Stability Index)** — 가장 널리 쓰이는 단변량 드리프트 지표:
$$
\text{PSI} = \sum_{i=1}^{n} (P_{ref,i} - P_{cur,i}) \cdot \ln\left(\frac{P_{ref,i}}{P_{cur,i}}\right)
$$
- $\text{PSI} < 0.1$: 안정(Stable)
- $0.1 \le \text{PSI} < 0.25$: 약한 변화(Warning)
- $\text{PSI} \ge 0.25$: 유의미한 변화(Drift, 재학습 권고)

**② Wasserstein Distance (Earth Mover's Distance)** — 연속형 분포 간 거리:
$$
W_p(\mu, \nu) = \left( \inf_{\gamma \in \Gamma(\mu,\nu)} \int \|x-y\|^p d\gamma(x,y) \right)^{1/p}
$$
분포의 지지집합(Support)이 다르거나 멀리 떨어진 경우에도 유의미한 거리 산출 가능.

**③ ADWIN (Adaptive Windowing)** — Bifet et al.(2007):
입력 스트림의 적응형 윈도우 $W$를 내부적으로 두 개의 서브윈도우 $W_0, W_1$로 분할하여, 두 윈도우의 평균 차이가 Hoeffding bound 기반 임계치 $\epsilon_{cut}$를 초과하면 드리프트로 판정. 메모리 $O(\log W)$, 시간 $O(1)$ per sample.

**④ H-divergence (Domain Classifier)** — Ben-David et al.(2010):
임의의 도메인 분류기 $h: X \to \{0,1\}$에 대해 두 도메인 간의 **H-divergence**를 정의하고, 이의 상한이 $d_{\mathcal{H}\Delta\mathcal{H}}(U,V) = 2 \sup_{h \in \mathcal{H}} | \text{err}_U(h) - \text{err}_V(h) |$. 실제로는 $h$를 학습시켜 AUC가 0.5에 가까우면 분포 동일, 1.0에 가까우면 분포 상이.

- **📢 섹션 요약 비유**: 단변량 모니터링은 '각 과목별 시험 점수 변화'를 보는 것이고, 다변량 모니터링은 '전체 성적표 패턴의 종합적 변화'를 감지하는 것입니다. 수학 점수는 그대로여도 국어·영어 점수가 함께 떨어지면 '전체 학업 능력 패턴이 변했다'고 판단하는 것이죠.

---

## Ⅲ. 비교 및 연결

드리프트 탐지 기법은 데이터 가용성(라벨 유무), 연산 비용, 검출력(Power), 지연 시간(Latency)에 따라 트레이드오프가 존재한다. 또한 Feature Drift Detection은 데이터 검증(Data Validation) 단계의 일부이며, 개념 드리프트 대응은 Online Learning, Transfer Learning, Curriculum Learning과 같은 적응 학습(Adaptive Learning) 영역과 긴밀히 연결된다.

| 구분 | 통계적 검정 (Statistical Test) | 거리 기반 (Distance-based) | 모델 기반 (Model-based) | 시계열 검출 (Sequential) |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 기법** | KS-test, Chi-square, t-test | PSI,