---
title: "Ensemble Learning"
date: "2026-04-05"
tags:
  - "studynote-ai"
weight: 40
---
> **핵심 인사이트**
> 1. 앙상블 학습(Ensemble Learning)은 여러 약한 학습기(Weak Learner)를 결합하여 단일 강한 학습기보다 우수한 예측 성능을 달성하는 기법으로, "다수결의 지혜"를 알고리즘으로 구현한 것이다.
> 2. Bagging(Bootstrap Aggregating)은 분산(Variance)을 줄여 과적합을 방지하고(Random Forest), Boosting은 편향(Bias)을 줄여 강한 예측기를 만들며(XGBoost), Stacking은 이질적 모델의 예측을 메타 학습기로 결합한다.
> 3. XGBoost·LightGBM·CatBoost는 Gradient Boosting의 현대적 구현으로 Kaggle 경진대회의 70% 이상 우승 솔루션에서 사용되었으며, 표 형태(Tabular) 데이터에서는 여전히 딥러닝을 능가하는 경우가 많다.

---

## Ⅰ. 앙상블 학습 원리

```
앙상블 학습의 핵심:

단일 모델 한계:
  높은 분산 (Variance): 훈련 데이터에 과적합
  높은 편향 (Bias): 과소적합, 단순한 패턴만 학습

앙상블 해결책:
  Bias-Variance Trade-off 균형

오류 분해:
  총 오류 = 편향^ + 분산 + 노이즈

다수결 원리:
  각 모델이 독립적으로 오류를 범한다면
  다수 모델의 투표 -> 오류 확률 급감

  예: 정확도 70% 모델 10개
      다수결 투표 시 83.8% 정확도 달성
```

> 📢 **섹션 요약 비유**: 앙상블 학습은 의사 여럿의 종합 소견 — 한 의사 실수는 다른 의사가 잡아주므로 단독 진단보다 정확하다.

---

## Ⅱ. Bagging (배깅)

```
Bagging (Bootstrap Aggregating):

원리:
  1. 훈련 데이터에서 Bootstrap 샘플링 (복원 추출)
  2. 각 샘플로 독립적인 모델 훈련
  3. 예측: 분류=투표, 회귀=평균

특성:
  - 모델들이 병렬(Parallel) 학습 -> 빠름
  - 분산(Variance) 감소 효과
  - 과적합 방지에 효과적

Random Forest (랜덤 포레스트):
  - Bagging + 랜덤 특성 선택(Feature Subsampling)
  - 각 결정 트리가 랜덤 부분집합 특성 사용
  - -> 트리 간 상관관계 감소 -> 더 강한 앙상블

  특성 중요도 (Feature Importance) 제공:
    어떤 특성이 예측에 중요한지 측정 가능

Bootstrap 샘플 특성:
  n개 데이터 복원 추출 -> 평균 63.2% 포함
  나머지 36.8% = OOB(Out-of-Bag) 검증 데이터
```

> 📢 **섹션 요약 비유**: 배깅은 여러 전문가에게 각기 다른 정보 부분집합을 보여주고 각자 판단 후 다수결 투표 — 각자 다른 측면을 보기 때문에 편향이 줄어듦.

---

## Ⅲ. Boosting (부스팅)

```
Boosting (부스팅):

원리:
  1. 첫 약한 학습기 훈련
  2. 잘못 분류된 샘플에 더 높은 가중치 부여
  3. 다음 학습기는 이전 오류에 집중
  4. 순차(Sequential) 학습 -> 편향 감소

AdaBoost (Adaptive Boosting):
  가중치 조정으로 어려운 샘플 집중
  최종 예측: 가중 다수결

Gradient Boosting:
  이전 모델의 잔차(Residual)를 다음 모델이 학습
  경사 하강법으로 손실 함수 최소화

XGBoost (eXtreme Gradient Boosting):
  - 정규화 추가 (과적합 방지)
  - 병렬/분산 처리 지원
  - 결측값 자동 처리
  - Kaggle 표준 도구

LightGBM:
  - 리프 기반 트리 성장 (vs 레벨 기반)
  - 대규모 데이터 고속 처리

CatBoost:
  - 범주형 변수 자동 처리
```

> 📢 **섹션 요약 비유**: 부스팅은 틀린 문제 집중 복습 — 이전 시험에서 틀린 문제를 다음 시험에서 더 집중해서 공부하는 맞춤형 학습.

---

## Ⅳ. Stacking (스태킹)

```
Stacking (Stacked Generalization):

원리:
  1. 레이어 0 (Base Models):
     이질적 알고리즘 복수 훈련
     (RF, XGBoost, SVM, Neural Net 등)

  2. 레이어 1 (Meta Model):
     Base 모델의 예측값을 새로운 특성으로 사용
     메타 학습기(Logistic Regression 등) 훈련

  3. 최종 예측: 메타 모델 출력

구조:
  훈련 데이터 -> [RF, XGB, SVM] -> 예측값들
                                     |
                               메타 학습기 훈련
                                     |
               테스트 데이터 -> [RF, XGB, SVM] -> 예측값들
                                                    |
                                               메타 학습기 -> 최종 예측

특징:
  가장 강력하지만 복잡함
  과적합 위험: K-Fold 교차 검증으로 Base 예측 생성 필수
  Kaggle 최종 단계에서 자주 사용
```

> 📢 **섹션 요약 비유**: 스태킹은 전문가 패널 토론 후 진행자가 종합 판단 — 각 분야 전문가(Base 모델) 의견을 MC(메타 모델)가 최종 정리.

---

## Ⅴ. 실무 시나리오 — 신용 리스크 예측

```
금융 신용 리스크 예측 앙상블:

문제: 대출 신청자 부도 예측 (이진 분류)
데이터: 30만 건, 150개 특성

접근법:

1단계: 단일 모델 기준선 (Baseline)
  Logistic Regression: AUC 0.78
  Decision Tree: AUC 0.72

2단계: 앙상블 적용
  Random Forest (Bagging): AUC 0.86
  XGBoost (Boosting): AUC 0.88

3단계: Stacking
  Base: RF + XGBoost + LightGBM + CatBoost
  Meta: Logistic Regression
  결과: AUC 0.91 (+6% 개선)

특성 중요도 활용:
  XGBoost Feature Importance -> 상위 20개 특성 선별
  해석 가능성 도구: SHAP 값으로 모델 설명

모니터링:
  월별 모델 성능 추적
  Distribution Shift 감지 -> 재학습 트리거
```

> 📢 **섹션 요약 비유**: 신용 리스크 앙상블은 여러 심사관의 종합 심사 — 한 심사관 판단보다 여럿의 합의가 대출 사고를 더 잘 예방한다.

---

## 📌 관련 개념 맵

```
앙상블 학습 (Ensemble Learning)
+-- 유형
|   +-- Bagging (분산 감소)
|   |   +-- Random Forest
|   +-- Boosting (편향 감소)
|   |   +-- AdaBoost
|   |   +-- Gradient Boosting
|   |   +-- XGBoost, LightGBM, CatBoost
|   +-- Stacking (이질 모델 결합)
+-- 이론
|   +-- Bias-Variance Trade-off
|   +-- 다수결 원리
+-- 도구
    +-- scikit-learn, XGBoost, LightGBM
    +-- SHAP (설명 가능성)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[단일 결정 트리 (1980s)]
CART 알고리즘
      |
      v
[Bagging / Random Forest (1990s~2001)]
Breiman의 배깅 + RF 논문
      |
      v
[AdaBoost (Freund & Schapire, 1995)]
부스팅 이론 완성
      |
      v
[Gradient Boosting (Friedman, 2001)]
XGBoost로 실용화 (2016 Kaggle 폭발)
      |
      v
[LightGBM (2017), CatBoost (2017)]
대규모 데이터 고속 처리 최적화
      |
      v
[현재: 탭형 데이터 지배]
표 형태 데이터: XGBoost/LightGBM > DL
AutoML에서 기본 모델로 채택
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 앙상블 학습은 퀴즈쇼에서 혼자 답하는 것보다 관객 투표를 이용하는 것처럼, 여러 AI 모델의 답을 모아 더 정확한 결과를 내는 방법이에요.
2. 배깅은 같은 문제를 여러 명에게 따로 풀게 해서 다수결하는 것이고, 부스팅은 틀린 문제만 골라서 더 집중적으로 다시 공부하는 방법이에요.
3. XGBoost는 이 부스팅 방법을 아주 빠르고 정확하게 구현해서 요즘 데이터 분석 대회의 단골 우승 무기가 됐어요!
