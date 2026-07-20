---
title: "Tsne"
date: "2026-04-05"
tags:
  - "studynote-ai"
weight: 44
---
> **핵심 인사이트**
> 1. t-SNE(t-distributed Stochastic Neighbor Embedding)는 고차원 데이터의 국소적 구조(Local Structure)를 2~3차원으로 시각화하는 비선형 차원 축소 기법으로 — 유사한 데이터 포인트를 가깝게, 상이한 포인트를 멀리 배치하여 클러스터 구조를 직관적으로 드러낸다.
> 2. t-SNE의 핵심은 고차원 공간의 가우시안 분포 유사도와 저차원 공간의 t-분포(자유도 1, 코시 분포) 유사도 사이의 KL Divergence를 최소화하는 것으로 — t-분포의 두꺼운 꼬리(Heavy Tail)가 "군집 붕괴 문제(Crowding Problem)"를 해결하는 핵심이다.
> 3. t-SNE는 탐색적 데이터 분석(EDA)과 모델 디버깅에는 강력하지만 — 퍼플렉시티(Perplexity) 하이퍼파라미터에 민감하고 전역 구조 보존이 약하며 계산량이 O(n^)이라 대규모 데이터에 직접 적용이 어려워, UMAP이 실용적 대안으로 부상하고 있다.

---

## Ⅰ. t-SNE 개념

```
t-SNE (t-distributed Stochastic Neighbor Embedding):
  van der Maaten & Hinton, 2008년 제안

목적:
  고차원 데이터 (100~수만 차원) -> 2~3차원 시각화
  클러스터 구조 탐색

SNE (Stochastic Neighbor Embedding):
  t-SNE의 전신
  고차원: 가우시안 분포로 유사도 계산
  저차원: 가우시안 분포로 유사도 계산

  문제: 군집 붕괴 (Crowding Problem)
  고차원 중간 거리 점들이 저차원에서 모두 가운데 몰림

t-SNE 개선:
  저차원 공간에 t-분포 (자유도=1) 사용
  -> 두꺼운 꼬리로 멀리 떨어진 점들을 더 멀리 배치
  -> Crowding Problem 해결

직관적 이해:
  1. 각 점을 중심으로 "이웃 확률 분포" 계산
     고차원: P(j|i) = 가까울수록 높은 확률

  2. 저차원에서 같은 분포 재현 시도
     Q(j|i): t-분포 기반 유사도

  3. P와 Q의 차이(KL Divergence) 최소화
     Gradient Descent로 저차원 좌표 최적화
```

> 📢 **섹션 요약 비유**: t-SNE는 3D 지도 -> 2D 지도 변환 — 나라(고차원 점)들을 비슷한 것끼리 가깝게, 다른 것끼리 멀게 배치. t-분포는 섬나라(멀리 떨어진 그룹)를 바다 건너 확실히 분리.

---

## Ⅱ. t-SNE 알고리즘

```
t-SNE 알고리즘 상세:

1단계: 고차원 유사도 계산
  입력: N개의 고차원 점 x1, ..., xN

  조건부 확률 (가우시안):
  P(j|i) = exp(-||xi-xj||^ / 2σi^) / Σk≠i exp(-||xi-xk||^ / 2σi^)

  σi: 퍼플렉시티(Perplexity)에 의해 결정
  P(ij) = (P(j|i) + P(i|j)) / 2N  <- 대칭화

2단계: 저차원 유사도 계산
  저차원 좌표: y1, ..., yN (초기화: 랜덤 or PCA)

  t-분포 기반:
  Q(ij) = (1 + ||yi-yj||^)^(-1) / Σk≠l (1 + ||yk-yl||^)^(-1)

3단계: KL Divergence 최소화
  C = KL(P || Q) = Σij P(ij) log(P(ij)/Q(ij))

  Gradient:
  dC/dyi = 4 Σj (P(ij) - Q(ij)) (yi-yj) (1+||yi-yj||^)^(-1)

  경사하강법으로 반복 최적화

퍼플렉시티 (Perplexity):
  유효 이웃 수 설정 (5~50, 보통 30)
  낮은 Perplexity: 국소 구조 강조
  높은 Perplexity: 전역 구조 반영

  데이터 크기에 따라 조정:
  소규모 (<1,000): Perplexity 5~15
  중간 (1,000~10,000): 20~50
  대규모: 100 이상

계산 복잡도:
  기본: O(n^)
  Barnes-Hut 근사: O(n log n)
  -> 10만 개 이상 데이터에는 별도 최적화 필요
```

> 📢 **섹션 요약 비유**: t-SNE KL Divergence 최소화는 지그소 퍼즐 맞추기 — 원본 사진(고차원 P)과 만들어진 퍼즐(저차원 Q)이 최대한 일치하도록 조각 위치를 조금씩 조정.

---

## Ⅲ. t-SNE vs PCA vs UMAP

```
차원 축소 기법 비교:

PCA (Principal Component Analysis):
  선형 변환: 분산 최대 방향으로 투영
  장점: 빠름, 전역 구조 보존, 결정론적
  단점: 비선형 구조 포착 불가
  용도: 전처리, 노이즈 제거

t-SNE:
  비선형 변환
  장점: 클러스터 구조 시각화 강력
  단점:
    - 전역 구조 보존 약함 (클러스터 간 거리 무의미)
    - O(n^) 계산 복잡도
    - 하이퍼파라미터 민감 (Perplexity)
    - 재현성 없음 (랜덤 초기화)
    - 새로운 점 추가 시 재실행 필요
  용도: EDA, 클러스터 탐색

UMAP (Uniform Manifold Approximation and Projection):
  Leland McInnes et al., 2018년
  비선형, 위상수학(Topology) 기반

  장점:
    - t-SNE보다 빠름 (O(n) 근사)
    - 전역 구조도 어느 정도 보존
    - 재현성 (random_state)
    - 새 점 추가 변환 가능 (transform 메서드)

  단점:
    - 이해하기 어려운 수학 기반

비교표:
항목        | PCA    | t-SNE  | UMAP
------------|--------|--------|-------
선형성      | 선형   | 비선형 | 비선형
속도        | 빠름   | 느림   | 중간
전역 구조   | 강     | 약     | 중간
클러스터    | 약     | 강     | 강
재현성      | 있음   | 없음   | 있음
대규모 데이터| 가능  | 어려움 | 가능
```

> 📢 **섹션 요약 비유**: PCA vs t-SNE vs UMAP은 지도 만들기 방법 — PCA는 직선 도로만, t-SNE는 구불구불한 마을 골목까지, UMAP은 골목도 잡으면서 더 빨리 그려요.

---

## Ⅳ. t-SNE 주의사항

```
t-SNE 오용 패턴:

1. 클러스터 간 거리 해석:
   잘못: "클러스터 A와 B가 C보다 더 유사하다"
   이유: t-SNE는 전역 구조 보존 안 함
   -> 클러스터 간 거리는 무의미

2. 클러스터 크기 해석:
   잘못: "A 클러스터가 B보다 크다"
   이유: t-SNE 클러스터 크기 ≠ 원래 데이터 밀도

3. Perplexity 기본값 신뢰:
   권장: 여러 Perplexity 값으로 시각화 비교
   Perplexity 5: 매우 타이트한 클러스터 (의도적 분리)
   Perplexity 50: 느슨한 배치 (전체적 경향)

4. 노이즈 클러스터 착시:
   작은 점 하나가 별개 클러스터로 보이는 경우
   -> 실제 아웃라이어인지 확인 필요

5. 랜덤 초기화 의존:
   매번 다른 레이아웃
   -> 결론 전에 여러 번 실행, 일관된 패턴 확인

올바른 t-SNE 사용:
  - "이 데이터에 클러스터 구조가 있는가?" 탐색
  - ML 모델 임베딩 품질 시각적 확인
  - 클래스 간 분리 가능성 시각화 (레이블 색상)
  - 이상치(Outlier) 탐지 보조
```

> 📢 **섹션 요약 비유**: t-SNE 오용 주의는 지도 해석 주의 — 지도에서 두 도시가 가깝다고 실제로 가까운 게 아닐 수 있어요. t-SNE 거리는 "동네 구조"를 보여주지만 "전국 거리"는 안 보여줘요.

---

## Ⅴ. 실무 시나리오 — 텍스트 임베딩 시각화

```
BERT 텍스트 임베딩 t-SNE 시각화:

목적: 뉴스 기사 카테고리 임베딩 품질 확인

데이터:
  20,000개 뉴스 기사
  카테고리: 정치, 경제, 스포츠, 연예, IT, 의학

  BERT 임베딩: 각 기사 -> 768차원 벡터

t-SNE 적용:
  from sklearn.manifold import TSNE
  import matplotlib.pyplot as plt

  # PCA로 사전 압축 (100차원, 속도 향상)
  from sklearn.decomposition import PCA
  pca = PCA(n_components=100)
  X_pca = pca.fit_transform(X_bert)  # (20000, 768) -> (20000, 100)

  # t-SNE
  tsne = TSNE(n_components=2, perplexity=40,
              n_iter=1000, random_state=42)
  X_tsne = tsne.fit_transform(X_pca)  # (20000, 100) -> (20000, 2)

  # 시각화
  plt.figure(figsize=(12, 8))
  scatter = plt.scatter(X_tsne[:,0], X_tsne[:,1],
                        c=labels, cmap='tab10', s=1)
  plt.colorbar(scatter)
  plt.title("BERT 임베딩 t-SNE 시각화")

결과 해석:
  좋은 임베딩:
  - 각 카테고리가 명확히 분리된 클러스터
  - 경계가 선명함

  나쁜 임베딩:
  - 카테고리들이 섞임
  - 구분 불가능

  발견:
  - 경제 + IT: 부분적 혼합 (경제기술 뉴스 중복)
  - 스포츠: 매우 명확한 분리 (도메인 특화)

  활용: 임베딩 방법 비교 (BERT vs RoBERTa vs GPT)
        미세조정(Fine-tuning) 전후 임베딩 품질 비교

대규모 처리:
  20,000건: t-SNE 약 5분
  200,000건: UMAP 권장 (5분 내 처리)
```

> 📢 **섹션 요약 비유**: BERT 임베딩 t-SNE 시각화는 언어의 지도 — 각 뉴스가 2D 지도에 찍히는데, 같은 카테고리끼리 동네를 이루면 "좋은 임베딩!", 섞이면 "모델 개선 필요!".

---

## 📌 관련 개념 맵

```
t-SNE
+-- 알고리즘
|   +-- 고차원: 가우시안 유사도 (P)
|   +-- 저차원: t-분포 유사도 (Q)
|   +-- KL Divergence 최소화
+-- 하이퍼파라미터
|   +-- Perplexity (5~50)
|   +-- n_iter (반복 횟수)
+-- 비교
|   +-- PCA (선형, 빠름)
|   +-- UMAP (비선형, 빠름, 재현성)
+-- 주의사항
|   +-- 클러스터 간 거리 무의미
|   +-- 전역 구조 보존 약함
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[PCA (1901)]
선형 차원 축소 표준
통계 기반 분산 최대화
      |
      v
[SNE (2002)]
Hinton & Roweis: 비선형 이웃 임베딩
군집 붕괴 문제 미해결
      |
      v
[t-SNE (2008)]
van der Maaten & Hinton
t-분포로 군집 붕괴 해결
      |
      v
[UMAP 등장 (2018)]
더 빠르고 전역 구조 보존
t-SNE 대체 트렌드
      |
      v
[현재: 딥러닝 임베딩 시각화]
BERT, GPT 임베딩 탐색 도구
TensorBoard Embedding Projector
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. t-SNE는 3D 지도를 2D로 압축 — 수백 개의 특징(차원)을 가진 데이터를 평면에 찍어서 "비슷한 것끼리 뭉치게" 표현해요!
2. t-분포의 두꺼운 꼬리가 핵심 — 멀리 있는 그룹들을 더 확실히 떼어놓는 것이 t-SNE의 비법이에요. 인근 동네는 붙이고, 먼 도시는 확실히 분리!
3. 클러스터 간 거리는 무시해요 — t-SNE는 "동네 내부 구조"를 잘 보여주지만, "도시 간 실제 거리"는 믿으면 안 돼요!
