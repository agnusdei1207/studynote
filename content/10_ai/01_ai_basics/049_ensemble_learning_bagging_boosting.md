---
title: "Ensemble Learning Bagging Boosting"
date: "2026-04-05"
tags:
  - "studynote-ai"
weight: 49
---
> **핵심 인사이트**
> 1. 앙상블 학습(Ensemble Learning)은 여러 약한 학습기(Weak Learner)를 결합하여 하나의 강한 학습기(Strong Learner)를 만드는 방법 — "두 머리가 하나보다 낫다"는 집단 지성의 수학적 구현이며, 단일 모델보다 낮은 분산(Variance) 또는 편향(Bias)을 달성한다.
> 2. 배깅(Bagging)은 분산을 줄이고, 부스팅(Boosting)은 편향을 줄이는 상이한 메커니즘 — 배깅은 부트스트랩 샘플로 독립적 모델을 병렬 훈련하여 과적합을 방지하고, 부스팅은 이전 모델의 오류에 집중하여 순차적으로 편향을 낮춘다.
> 3. XGBoost·LightGBM·CatBoost가 정형 데이터 경진 대회의 절대 강자인 이유가 바로 부스팅의 편향-분산 최적화 — 딥러닝이 이미지·자연어를 석권한 이후에도 표 형식 데이터(Tabular Data)에서 그래디언트 부스팅 기반 모델이 가장 높은 성능을 보인다.

---

## Ⅰ. 앙상블 개요

```
앙상블 학습 (Ensemble Learning):
  여러 모델의 예측을 결합하여 최종 예측

필요성:

단일 모델의 한계:
  과적합 (Overfitting): 훈련 데이터에만 잘 맞음
  과소적합 (Underfitting): 복잡한 패턴 학습 못함
  불안정: 데이터 조금 바뀌면 예측 크게 변함

앙상블 효과:
  투표 (Voting): 다수결로 안정적 예측
  평균 (Averaging): 분산 감소
  오류 보완: 한 모델의 오류를 다른 모델이 보완

편향-분산 트레이드오프:
  편향(Bias): 모델이 실제 패턴에서 벗어난 정도
  분산(Variance): 데이터 변화에 민감한 정도

  복잡한 모델: 편향v, 분산^ (과적합)
  단순한 모델: 편향^, 분산v (과소적합)

  앙상블 목표:
  배깅 -> 분산 감소
  부스팅 -> 편향 감소

앙상블 방법:
  배깅 (Bagging): 병렬, 분산 감소
  부스팅 (Boosting): 순차, 편향 감소
  스태킹 (Stacking): 메타 학습기 결합
  보팅 (Voting): 단순 다수결
```

> 📢 **섹션 요약 비유**: 앙상블 = 의사 그룹 진료 — 여러 의사(모델)가 각자 진단. 다수결(Voting)로 최종 결정. 한 의사의 실수를 다른 의사가 보완. 집단 지성!

---

## Ⅱ. 배깅 (Bagging)

```
Bagging (Bootstrap Aggregating):
  부트스트랩 샘플 -> 독립 모델 -> 결합

부트스트랩 샘플링:
  원본 데이터 N개 -> 복원 추출로 N개 샘플

  특성:
  약 63.2%의 원본 데이터 포함 (중복 허용)
  약 36.8%: Out-of-Bag (OOB) 샘플 (검증용)

배깅 절차:
  1. 훈련 데이터 D에서 T개 부트스트랩 샘플 생성
  2. 각 샘플로 독립적 모델 m1, m2, ..., mT 훈련
  3. 예측:
     분류: 다수결 투표
     회귀: 평균

분산 감소 원리:
  독립적 모델 T개의 평균:
  Var(평균) = Var(개별) / T

  -> 모델 수가 많을수록 분산 감소

Random Forest (랜덤 포레스트):
  배깅 + 특성 무작위 선택

  개선:
  각 분기점: 전체 특성 중 √m개만 무작위 선택
  -> 트리 간 상관관계 감소 -> 추가 분산 감소

  OOB 평가:
  각 트리의 OOB 샘플로 교차 검증 대체

  특성 중요도:
  OOB 오류 증가율로 특성 기여도 측정

배깅 구현:
  from sklearn.ensemble import BaggingClassifier, RandomForestClassifier

  bag = BaggingClassifier(n_estimators=100, bootstrap=True)
  rf = RandomForestClassifier(n_estimators=100, max_features='sqrt')
```

> 📢 **섹션 요약 비유**: 배깅 = 여론 조사 집계 — 각 조사(부트스트랩 샘플)에서 독립적 결과. 100개 조사 평균 내면 단일보다 정확. Random Forest는 조사마다 다른 질문 섞어서 중복 의견 제거!

---

## Ⅲ. 부스팅 (Boosting)

```
Boosting:
  이전 모델의 오류에 집중 -> 순차적 편향 감소

AdaBoost:
  틀린 샘플의 가중치 증가 -> 다음 모델이 집중

  1. 균등 가중치로 모델 1 훈련
  2. 오분류 샘플 가중치 증가
  3. 증가된 가중치로 모델 2 훈련
  4. 반복
  5. 최종: 가중 투표 (정확한 모델에 더 큰 가중치)

Gradient Boosting:
  잔차(Residual)를 목표로 훈련

  F(x) = F_0(x) + F_1(x) + F_2(x) + ...

  각 단계:
  r = y - F_prev(x)  # 잔차(음의 그래디언트)
  새 모델 h = 잔차 r을 예측하도록 훈련
  F_new = F_prev + 학습률 × h

XGBoost (Extreme Gradient Boosting):
  그래디언트 부스팅 최적화

  특징:
  정규화 (L1/L2): 과적합 방지
  병렬 처리: 트리 내 분기점 탐색 병렬화
  가지치기: 음수 이득 분기 제거
  결측값 처리 내장

  실용성:
  Kaggle 2015~2022: 우승 모델 다수 XGBoost

LightGBM:
  Leaf-wise 트리 성장 (XGBoost: Level-wise)
  -> 더 빠른 학습, 더 낮은 메모리

  GOSS (Gradient-based One-Side Sampling):
  큰 그래디언트 샘플 유지, 작은 것 일부만
  -> 정확도 유지하며 속도 향상

CatBoost:
  카테고리 변수 자동 처리
  Ordered Boosting: 데이터 누설 방지
```

> 📢 **섹션 요약 비유**: 부스팅 = 약점 집중 훈련 — 시험에서 틀린 문제에 집중. 다음 모델이 이전 모델의 오류(잔차)를 공략. 100번 반복 -> 점점 정확해짐!

---

## Ⅳ. 스태킹과 비교

```
스태킹 (Stacking):
  기본 학습기(Base Learner) 예측을 메타 학습기 입력으로

절차:
  1. N개 기본 모델 (SVM, RF, LGBM 등) 훈련
  2. 각 모델의 예측값 -> 새로운 특성
  3. 메타 모델(보통 선형 회귀/로지스틱): 예측값 결합

  예:
  기본 모델 3개: [0.8, 0.3, 0.7] 예측
  메타 모델: 이 3개 예측으로 최종 예측

  K-Fold 스태킹:
  데이터 누설 방지 위해 교차 검증으로 기본 예측 생성

보팅 (Voting):
  하드 보팅: 다수결 (클래스 직접)
  소프트 보팅: 확률 평균 (더 정확)

  from sklearn.ensemble import VotingClassifier
  vc = VotingClassifier([('rf', rf), ('lgbm', lgbm)], voting='soft')

방법 비교:
  방법     순서   목표    대표 알고리즘
  배깅     병렬   분산v   Random Forest
  부스팅   순차   편향v   XGBoost, LightGBM
  스태킹   2단계  둘 다   Blending
  보팅     병렬   안정    Voting Classifier

데이터 유형별:
  정형 데이터: LightGBM/XGBoost 최강
  이미지/텍스트: 딥러닝 (앙상블은 보조)
  소규모: Random Forest (해석 가능)
```

> 📢 **섹션 요약 비유**: 스태킹 = 전문가 패널 + 심사위원장 — 전문가 3명(기본 모델) 의견 듣고, 심사위원장(메타 모델)이 최종 결정. 단순 다수결보다 더 정교한 결합!

---

## Ⅴ. 실무 시나리오 — Kaggle 신용 위험 예측

```
Kaggle Credit Risk 대회 앙상블 전략:

데이터:
  정형 데이터 (Tabular): 30만 행, 200 특성
  목표: 대출 불이행 확률 예측
  평가: AUC-ROC

단계별 접근:

1. 베이스라인 (LightGBM 단일):
  lgbm = LGBMClassifier(n_estimators=5000,
                        learning_rate=0.02,
                        num_leaves=63,
                        early_stopping_rounds=200)
  AUC: 0.791

2. XGBoost 추가:
  AUC: 0.789 (LightGBM과 유사하지만 다른 오류)

3. 소프트 보팅 앙상블:
  VotingClassifier([lgbm, xgb], voting='soft', weights=[0.6, 0.4])
  AUC: 0.797 (+0.006)

4. K-Fold 스태킹:
  Fold 5: LightGBM + XGBoost + CatBoost
  메타 모델: Logistic Regression
  AUC: 0.803 (+0.012)

5. 특성 공학 + 앙상블:
  신규 특성: debt_to_income, payment_history 등
  최종: AUC 0.818

Optuna 하이퍼파라미터 최적화:
  각 모델 파라미터 자동 탐색
  50~100 trial -> 최적 파라미터

결과:
  단일 LightGBM: 0.791
  최종 스태킹 앙상블: 0.818
  순위: 상위 3% (Gold Medal 권)

교훈:
  앙상블 효과: +0.027 (AUC)
  모델 다양성이 핵심 (상관관계 낮을수록 효과적)
  LightGBM + XGBoost: 상관관계 0.85 (낮은 편)
```

> 📢 **섹션 요약 비유**: Kaggle 앙상블 = 의사결정 위원회 — LightGBM(내과 전문의), XGBoost(외과), CatBoost(영상의학과). 각자 다른 오류 -> 스태킹으로 AUC 0.791->0.818. 다양성이 핵심!

---

## 📌 관련 개념 맵

```
앙상블 학습
+-- 배깅 (분산 감소)
|   +-- Random Forest
|   +-- Extra Trees
+-- 부스팅 (편향 감소)
|   +-- AdaBoost
|   +-- Gradient Boosting
|   +-- XGBoost, LightGBM, CatBoost
+-- 스태킹 (2단계 결합)
+-- 보팅 (다수결)
+-- 이론
    +-- 편향-분산 트레이드오프
    +-- 약한 학습기 -> 강한 학습기
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[AdaBoost (1995, Freund & Schapire)]
부스팅 이론 정립
약한 학습기 결합
      |
      v
[Random Forest (2001, Breiman)]
배깅 + 무작위 특성
실용적 표준
      |
      v
[Gradient Boosting (2001)]
잔차 기반 순차 학습
      |
      v
[XGBoost (2014)]
Kaggle 우승 모델 표준
정규화+병렬 최적화
      |
      v
[LightGBM (2017), CatBoost (2017)]
속도+메모리 최적화
Leaf-wise, 카테고리 변수
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 앙상블 = 의사 그룹 진료 — 여러 의사가 각자 진단 후 다수결. 한 의사 실수를 다른 의사가 보완. 혼자보다 정확!
2. 배깅(Random Forest) = 여론조사 집계 — 100개 독립 조사 평균. 과적합 방지, 분산 감소. 모두 같은 답 = 무의미하니 무작위 특성 추가!
3. 부스팅(XGBoost) = 약점 집중 훈련 — 틀린 문제에 집중. 이전 오류(잔차)를 다음 모델이 공략. 100회 반복 -> 최강 모델!
