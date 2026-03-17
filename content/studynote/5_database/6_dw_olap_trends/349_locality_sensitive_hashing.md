+++
title = "349. LSH (Locality Sensitive Hashing) - 비슷한 것끼리 묶는 해시"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 349
+++

# 349. LSH (Locality Sensitive Hashing) - 비슷한 것끼리 묶는 해시

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LSH는 일반 해시와 반대로 **유사한 특징을 가진 데이터들이 같은 해시값(Bucket)을 가질 확률을 극대화**하여, 고차원 공간에서 빠르게 근사 이웃을 찾아내는 알고리즘이다.
> 2. **가치**: 전체 데이터를 전수 조사하지 않고도 충돌된 버킷 내의 소수 데이터만 비교함으로써, 검색 시간을 획기적으로 줄여 **초대규모 데이터셋의 유사성 검색**을 실현한다.
> 3. **융합**: MinHash, Random Projection 등 다양한 기법과 융합되어 중복 문서 판별, 이미지 검색, 대규모 오디오 지문(Audio Fingerprinting) 인식 시스템의 핵심 엔진으로 활용된다.

+++

### Ⅰ. LSH의 핵심 원리: 해시의 역설

- **전통적 해시 (Cryptographic)**: 아주 미세한 차이도 완전히 다른 해시값을 생성. (무결성 목적)
- **LSH (Locality Sensitive)**: 비슷한 데이터는 **일부러 충돌(Collision)**이 나도록 설계. (유사성 탐색 목적)

+++

### Ⅱ. LSH 매커니즘 시각화 (ASCII Model)

```text
[ Locality Sensitive Hashing Flow ]

  (Input Vectors)       (LSH Functions)       (Hash Buckets)
  ┌───────────┐         ┌───────────┐         ┌───────────┐
  │  ● Data A │ ──▶───▶ │ Hash Func │ ──▶───▶ │ [Bucket 1]│ (A, B 충돌!) ✅
  │  ● Data B │ ──▶───▶ │    H(x)   │         ├───────────┤
  │           │         └───────────┘         │ [Bucket 2]│
  │  ■ Data C │ ──▶───────────────────────▶── │ [Bucket 3]│ (C 저장)
  └───────────┘                               └───────────┘

  * 검색 시: 질문 데이터와 같은 Bucket에 든 데이터만 정밀 비교하여 속도 향상.
```

+++

### Ⅲ. 주요 LSH 기법

1. **MinHash**: 자카드 유사도(Jaccard Similarity)를 측정할 때 사용. 텍스트 중복 제거에 탁월.
2. **Random Projection (SimHash)**: 코사인 유사도를 기반으로 고차원 벡터를 저차원의 비트열로 투영.
3. **P-stable Distribution**: 유클리드 거리를 기반으로 수치형 데이터를 버킷화.

- **📢 섹션 요약 비유**: LSH는 **'동창생 분류법'**과 같습니다. 수만 명의 사람 중에서 비슷한 사람을 찾기 위해 키, 몸무게를 일일이 재는 대신, 일단 '출신 고등학교'라는 해시값으로 분류하는 것입니다. 같은 학교(버킷) 출신들끼리만 모아서 상세히 조사하면, 전체 인구를 뒤지는 것보다 훨씬 빠르게 닮은 사람을 찾을 수 있습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Approximate Nearest Neighbor (ANN)]**: 100% 정확도 대신 압도적 속도를 택하는 검색 패러다임.
- **[Curse of Dimensionality]**: LSH가 해결하고자 하는 '차원의 저주'.
- **[Bucket]**: 해시값이 같은 데이터들이 모이는 논리적 공간.

📢 **마무리 요약**: **Locality Sensitive Hashing**은 빅데이터 탐색의 효율성을 바꾼 혁신적인 아이디어입니다. 정답과 '거의 비슷한' 결과를 광속으로 찾아내는 현대 검색 기술의 정수입니다.