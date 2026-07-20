---
title: "Mlops Machine Learning Operations"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
weight: 48
---
> **핵심 인사이트**
> 1. MLOps(Machine Learning Operations)는 ML 모델의 전체 생애주기(개발->학습->배포->모니터링->재학습)를 DevOps 원칙으로 자동화하는 방법론 — 데이터 사이언티스트가 만든 모델이 "연구실"에 머무는 것을 막고, 안정적으로 프로덕션에 배포·운영되도록 한다.
> 2. ML 모델은 소프트웨어와 달리 "데이터 드리프트(Data Drift)"라는 추가 운영 도전이 있다 — 코드가 변경되지 않아도 입력 데이터 분포 변화로 모델 성능이 저하되며, 이를 자동으로 탐지하고 재학습 트리거를 설정하는 것이 MLOps의 핵심이다.
> 3. Feature Store가 MLOps 성숙도의 핵심 지표 — 특성(Feature) 재사용·공유·버전 관리를 가능하게 하는 Feature Store 없이는 학습-서빙 일관성 문제와 특성 계산 중복이 필연적으로 발생한다.

---

## Ⅰ. MLOps 개요

```
MLOps (Machine Learning Operations):
  ML 모델 개발 + 운영의 통합
  DevOps + DataOps + ModelOps

ML 생애주기:

데이터 수집/준비 -> 특성 엔지니어링 -> 모델 학습
      ^                                      v
재학습 트리거                         모델 평가
      ^                                      v
성능 모니터링                         배포 (A/B, Canary)
      ^                                      v
데이터 드리프트 탐지               서빙 (추론 API)

MLOps 없을 때의 문제:

"연구실 노트북에서 프로덕션으로":
  데이터 사이언티스트: 노트북에서 모델 학습 -> pickle 파일
  엔지니어: 수동으로 모델 배포

  문제:
  재현 불가 (어떤 데이터로 학습했는지 모름)
  배포 위험 (테스트 없이 배포)
  성능 모니터링 없음 (언제 성능 저하됐는지 모름)
  재학습 수동 (누가 언제 트리거하는지 모름)

MLOps 성숙도 (Google 3단계):

Level 0: 수동
  스크립트 기반, 수동 배포, 모니터링 없음

Level 1: ML 파이프라인 자동화
  학습 파이프라인 자동화
  데이터 드리프트 탐지 -> 자동 재학습
  모델 레지스트리

Level 2: CI/CD 파이프라인 자동화
  모델 코드 변경 -> 자동 재학습 -> 자동 배포
  A/B 테스트 자동화
  Feature Store
```

> 📢 **섹션 요약 비유**: MLOps = ML 공장 자동화 — 연구원이 레시피(모델) 개발, 공장(MLOps)이 원자재 수급(데이터)->생산(학습)->품질검사(평가)->출하(배포)->불량 탐지(드리프트) 자동화!

---

## Ⅱ. 데이터 드리프트

```
데이터 드리프트 (Data Drift):
  프로덕션 입력 데이터의 분포가 학습 데이터와 달라지는 현상

유형:

1. 데이터 드리프트 (Feature Drift):
  입력 특성의 분포 변화

  예:
  신용 점수 모델: 2019년 데이터 학습
  COVID-19 이후: 수입 패턴 급변
  -> 모델이 "정상"이라 판단하는 기준 틀어짐

2. 컨셉 드리프트 (Concept Drift):
  입력-출력 관계 자체가 변화

  예:
  스팸 필터: "Zoom 초대" = 정상 메일
  COVID 이후: "Zoom 사기" 스팸 급증
  -> 기존 관계 변화 -> 재학습 필요

3. 레이블 드리프트:
  출력 분포의 변화

  예:
  불량품 탐지 모델: 불량률 2% 기준 학습
  신규 공정 도입 후: 불량률 5%로 증가
  -> 임계값 재조정 필요

드리프트 탐지 기법:

통계적 검정:
  KS-test (Kolmogorov-Smirnov): 분포 비교
  PSI (Population Stability Index): 특성 안정성 지수

  PSI < 0.1: 정상
  PSI 0.1~0.2: 경고 (모니터링 강화)
  PSI > 0.2: 심각 (재학습 필요)

모델 성능 모니터링:
  레이블 있는 경우: 정확도, F1, AUC 추적
  레이블 없는 경우: 예측 분포 모니터링
```

> 📢 **섹션 요약 비유**: 데이터 드리프트 = 지도 업데이트 누락 — 2019년 지도(학습 데이터)로 운전(예측). 2023년 도로 변경(드리프트) 후 길 안내 오류. 지도(모델) 업데이트 필요!

---

## Ⅲ. Feature Store

```
Feature Store (특성 저장소):
  특성(Feature)의 저장, 재사용, 서빙을 위한 중앙 저장소

Feature Store 없을 때 문제:

팀 A: 추천 모델 -> user_avg_purchase 특성 계산 코드
팀 B: 이탈 예측 -> user_avg_purchase 동일 계산 별도 구현
팀 C: 신용 평가 -> 또 다른 버전 구현

문제:
  계산 중복 = 비용 낭비
  각 팀 버전 불일치 = 비교 어려움
  학습 시 계산 vs 서빙 시 계산 불일치 = 성능 저하

Feature Store 해결:

중앙 특성 레지스트리:
  user_avg_purchase: 사용자 평균 구매금액 (30일)
  정의: 한 곳에 명확히

  팀 A, B, C 모두 동일 특성 재사용

학습-서빙 일관성:
  학습 시: 과거 배치 데이터에서 특성 조회 (오프라인)
  서빙 시: 실시간 특성 조회 (온라인, Redis 등)

  동일 계산 로직으로 일관성 보장

Feature Store 구성:

오프라인 스토어 (학습용):
  S3/HDFS 기반 배치 저장
  point-in-time correctness (과거 시점 특성)

온라인 스토어 (서빙용):
  Redis/DynamoDB 기반 실시간 조회
  P99 < 10ms

주요 도구:
  Feast (오픈소스): K8s 기반
  Tecton: 상용, Databricks 통합
  AWS SageMaker Feature Store
  Vertex AI Feature Store (GCP)
```

> 📢 **섹션 요약 비유**: Feature Store = 표준 식재료 창고 — 여러 팀이 같은 재료(특성)를 각자 계산하면 낭비+불일치. 창고(Feature Store)에서 표준 재료 꺼내쓰면 일관성+효율!

---

## Ⅳ. 모델 배포 전략

```
ML 모델 배포 전략:

1. Shadow 배포 (Shadow Deployment):
  현재 모델: 프로덕션 트래픽 처리 + 응답 반환
  새 모델: 동일 요청 병행 처리, 응답 미반환 (그림자)

  목적: 실제 트래픽으로 새 모델 성능 측정 (위험 없이)

  결과 비교: current vs shadow 예측 분포 비교

2. Canary 배포:
  트래픽 1% -> 새 모델
  트래픽 99% -> 기존 모델

  점진적 증가: 1% -> 5% -> 20% -> 100%

  모니터링: 각 단계에서 비즈니스 지표 확인

3. A/B 테스트:
  사용자 그룹을 분리 -> 서로 다른 모델

  KPI: 추천 클릭률, 전환율 등
  통계적 유의성 확인 후 롤아웃

4. Multi-Armed Bandit:
  A/B와 달리 성능 좋은 모델에 더 많은 트래픽 자동 할당
  탐색(Exploration) + 활용(Exploitation) 균형

모델 서빙:
  TensorFlow Serving: TF 모델 전용
  TorchServe: PyTorch 전용
  BentoML: 프레임워크 무관
  Seldon Core: K8s 기반 ML 서빙
  AWS SageMaker Endpoints: 관리형

모델 레지스트리:
  MLflow Model Registry: 버전, 스테이지 관리
  SageMaker Model Registry

  Staging -> Production 승격 워크플로우
  롤백: 이전 버전으로 즉시 전환
```

> 📢 **섹션 요약 비유**: 모델 배포 전략 = 신메뉴 출시 전략 — Shadow(그림자 주방: 손님 모르게 테스트), Canary(1개 테이블만 신메뉴), A/B(반반 비교). 문제 없으면 전체 출시!

---

## Ⅴ. 실무 시나리오 — 전자상거래 추천 MLOps

```
전자상거래 상품 추천 MLOps 구축:

AS-IS:
  데이터 과학팀: 주피터 노트북 학습
  배포: 월 1회 수동 배포
  모니터링: 없음
  재학습: 요청 시 수동

문제:
  모델 성능 하락을 2주 후에 인식
  배포 실패 시 롤백 방법 없음
  특성 계산 코드 팀마다 다름

TO-BE MLOps 구축:

1. Feature Store (Feast):
  user_30day_purchase_count (30일 구매 수)
  user_category_preference (카테고리 선호도)
  item_popularity_score (아이템 인기도)

  학습 시: Feast 과거 스냅샷 -> 오프라인 학습
  서빙 시: Feast + Redis -> P99 5ms 특성 조회

2. 학습 파이프라인 (Kubeflow):
  매일 새 데이터 -> 자동 파이프라인 실행
  모델 품질 게이트: Precision@K ≥ 0.35
  통과 시 -> MLflow 레지스트리 등록

3. 배포 (Seldon Core + Canary):
  신규 모델 -> 1% 트래픽
  2시간 후 지표 확인 -> 5% -> 20% -> 100%

4. 모니터링 + 재학습 트리거:
  Evidently: 입력 특성 PSI 모니터링
  PSI > 0.2 또는 CTR 5% 이상 하락 -> 재학습 자동 트리거

결과:
  배포 주기: 월 1회 -> 일 1회 (자동)
  드리프트 감지: 2주 -> 24시간 내
  CTR: 3.2% -> 4.1% (모델 품질 향상)
  특성 계산 비용: 팀별 중복 제거 -> 35% 감소
```

> 📢 **섹션 요약 비유**: 추천 MLOps = ML 공장 자동화 — 데이터(원자재)->학습(생산)->배포(출하)->드리프트 탐지(불량 감지)->재학습(품질 개선) 자동화. CTR 28% 향상, 배포 월1->일1회!

---

## 📌 관련 개념 맵

```
MLOps
+-- 생애주기
|   +-- 데이터 준비 -> 학습 -> 배포 -> 모니터링 -> 재학습
+-- 핵심 개념
|   +-- 데이터 드리프트 탐지
|   +-- Feature Store
|   +-- 모델 레지스트리
+-- 배포 전략
|   +-- Shadow, Canary, A/B
|   +-- Multi-Armed Bandit
+-- 도구
|   +-- Kubeflow, MLflow
|   +-- Feast (Feature Store)
|   +-- Seldon Core, BentoML
+-- 성숙도
    +-- Level 0 -> Level 1 -> Level 2
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 ML 모델 (2010s)]
노트북 실험
수동 배포
      |
      v
[TFX, MLflow 등장 (2017~)]
파이프라인 자동화
모델 버전 관리
      |
      v
[Kubeflow (2018)]
K8s 기반 ML 파이프라인
클라우드 네이티브 MLOps
      |
      v
[Feature Store 상용화 (2019~)]
Feast, Tecton
학습-서빙 일관성
      |
      v
[현재: LLMOps]
대규모 언어 모델 운영
프롬프트 버전 관리
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. MLOps = ML 공장 자동화 — 연구원(데이터 사이언티스트)이 레시피 개발, 공장(MLOps)이 재료->생산->출하->불량 탐지 자동화!
2. 데이터 드리프트 = 낡은 지도 — 2019년 지도로 2023년 운전하면 길 안내 오류. 드리프트 감지 = 지도 갱신 필요 신호!
3. Feature Store = 표준 재료 창고 — 여러 팀이 같은 재료를 따로 만들면 낭비+불일치. 창고(Feature Store)에서 표준 재료 공유!
