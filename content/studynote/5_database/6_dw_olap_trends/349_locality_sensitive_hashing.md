+++
title = "349. LSH (Locality Sensitive Hashing) - 비슷한 것끼리 묶는 해시"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 349
+++

# 349. LSH (Locality Sensitive Hashing) - 비슷한 것끼리 묶는 해시

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LSH(Locality Sensitive Hashing)는 기존 해시 함수의 '충돌 회피' 성질을 뒤집어, **공간적으로 유사한(Similar) 데이터끼리 인위적으로 충돌(Collision)을 유도**하여 같은 버킷(Bucket)에 매핑하는 확률적 자료 구조 및 알고리즘이다.
> 2. **가치**: 고차원(High-Dimensional) 데이터 공간에서 발생하는 차원의 저주(Curse of Dimensionality)를 극복하여, $O(N)$의 선형 탐색 비용을 $O(1)$에 근접한 **서브-리니어(Sub-linear) 탐색**으로 최적화하고, 근사 이웃 탐색(ANN, Approximate Nearest Neighbor)을 통해 대규모 검색의 성능을 획기적으로 개선한다.
> 3. **융합**: 암호학(Hashing), 데이터 마이닝(Clustering), 정보 검색(Information Retrieval) 분야를 융합하며, 특히 추천 시스템의 협업 필터링(Collaborative Filtering)이나 중복 문서 검출(Deduplication) 등에서 비즈니스적 가치를 창출한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**LSH (Locality Sensitive Hashing)**은 고차원 벡터 공간에서 '근사 최근접 이웃(Approximate Nearest Neighbor)'을 빠르게 찾기 위해 설계된 기법입니다. 일반적인 해시 함수(예: SHA-256)는 입력값의 미세한 변화에도 출력값이 완전히 달라지도록(Avalanche Effect) 설계되어 무결성을 보장하지만, LSH는 **'입력값이 유사하면 해시값도 유사할 확률이 높다'**는 철학을 가집니다. 여기서 '유사함'의 정의는 거리 함수(Metric)에 따라 달라지며, 대표적으로 자카드 유사도(Jaccard Similarity), 코사인 유사도(Cosine Similarity), 유클리드 거리(Euclidean Distance) 등이 활용됩니다.

#### 2. 💡 비유: 도서관 사서 vs. 분류된 서가
일반 검색(Linear Scan)은 도서관의 모든 책을 페이지별로 하나하나 펴보며 내용이 같은지 확인하는 것과 같습니다. 반면, LSH는 책의 주제별로 분류된 '서가(버킷)'를 먼저 확인하는 것과 같습니다. 내용이 비슷한 책들은 같은 서가에 있을 확률이 높으므로, 서가 전체를 다 뒤지지 않고 해당 서가의 책들만 비교하면 원하는 책을 훨씬 빠르게 찾을 수 있습니다.

#### 3. 등장 배경 및 비즈니스 요구
- **기존 한계**: 데이터의 차원이 증가함에 따라($d \to \infty$), 모든 점 간의 거리가 거의 동일해져 '차원의 저주' 현상 발생. 인덱스 기반의 탐색(Tree-based)이 무의미해지며 선형 탐색의 속도 저하 발생.
- **혁신적 패러다임**: $100\%$ 정확도를 포기하고, 약간의 오류(False Positive)를 허용하여 검색 속도를 수백 배 이상 향상시키는 **확률적 알고리즘** 도입.
- **현재 요구**: 페이스북/인스타그램 등의 플랫폼에서 초당 수만 건의 이미지/텍스트 유사도 검사가 필요하며, GPU를 활용한 벡터 DB 검색 전략과 함께 하이브리드 검색의 필수 요소로 자리 잡음.

> **📢 섹션 요약 비유**: LSH는 **'전화번호부 부군 번호 시스템'**과 같습니다. 신체적인 거리가 가까운 사람들이 서로 자주 통화한다는 가정하에, 지역 번호(해시 버킷)를 먼저 확인하고 그 안에서 상세 번호를 찾는 것처럼, 데이터의 공간적 위치를 이용해 탐색 범위를 획기적으로 축소하는 원리입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 기술

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 주요 파라미터 (Parameters) |
|:---|:---|:---|:---|
| **Hash Function Family ($H$)** | 데이터를 버킷에 매핑하는 핵심 함수군 | 거리 보존(Locality Sensitive) 특성을 만족하는 $h(v)$ 함수 집합. 예: Random Projection $h(v) = sign(v \cdot r)$ | $k$ (해시 함수 개수), $L$ (해시 테이블 개수) |
| **Hash Tables ($L$)** | 충돌이 발생한 데이터를 저장하는 버킷들의 집합 | $k$개의 함수를 조합($g(v) = [h_1, ..., h_k]$)하여 생성된 키를 인덱스로 사용. | $L$ (테이블 반복 수), Collisions (버킷 크기) |
| **Candidate Set** | 1차 필터링된 유사 후보군 집합 | 쿼리 $q$와 해시 충돌이 일어난 데이터들의 집합. 여기서 정밀 검사 수행. | Threshold (거리 임계값) |
| **Distance Metric** | 유사도를 측정하는 수학적 기준 | 자카드($J(A,B)$), 코사인($\cos \theta$), 유클리드($L_2$ Norm) 등 데이터 성격에 따라 선택. | Metric Type |
| **AND-OR Construction** | 정밀도(Precision)와 재현율(Recall) 조절 | **AND($k$)**: 버킷을 좁혀 정확도 상승. **OR($L$)**: 테이블을 넓혀 재현율 상승. | $k \uparrow \to$ Precision $\uparrow$, $L \uparrow \to$ Recall $\uparrow$ |

#### 2. LSH 아키텍처 및 데이터 흐름도

LSH의 동작은 크게 '해시 함수 생성($G$)', '버킷 매핑($P$)', '후보군 선별($C$)', '정밀 검증($V$)'의 4단계로 구성됩니다.

```text
    [ LSH Architecture: AND-OR Amplification Strategy ]

          Query Vector (q)
               │
               ▼
    ┌──────────────────────┐
    │  Hash Function Set    │
    │  h1(v), h2(v), ... hk(v)  ────▶  AND Construction (Concatenation)
    └──────────────────────┘                      (Tightens the bucket)
               │
               ▼  g1(q) = [hash1, hash2, ... hashk]
    ┌──────────────────────┐
    │   Hash Table 1 (L1)  │ ───▶ Bucket #101: [id_2, id_55] ──┐
    ├──────────────────────┤                                    │
    │   Hash Table 2 (L2)  │ ───▶ Bucket #552: [id_2, id_99] ──┤
    ├──────────────────────┤                                    │
    │   ...                 │                                    ├──▶  [Candidate Set Pool]
    ├──────────────────────┤                                    │
    │   Hash Table L (L)   │ ───▶ Bucket #003: [id_2] ─────────┘
    └──────────────────────┘
               │
               ▼                           (OR Construction)
        [Union of Candidates]      ───▶ Increases Recall Probability
               │
               ▼
    ┌──────────────────────┐
    │  Exact Distance Calc │ ───▶  Dist(q, v) < Threshold ?
    └──────────────────────┘
               │
               ▼
        [Final Result Set]
```

#### 3. 심층 동작 원리 및 알고리즘
LSH의 핵심은 **$(r_1, r_2, p_1, p_2)$-sensitive** 조건을 만족하는 해시 함수족($H$)을 찾는 것입니다.
- $P[h(q)=h(p)] \ge p_1$ if $D(q,p) \le r_1$ (가까운 점은 해시가 같을 확률 높음)
- $P[h(q)=h(p)] \le p_2$ if $D(q,p) \ge r_2$ (먼 점은 해시가 같을 확률 낮음)

이를 통해 '해시 충돌'이 곧 '유사함'을 의미하도록 변환합니다.

**[MinHash Algorithm for Jaccard Similarity]**
MinHash는 문서 집합의 유사도를 측정할 때 사용됩니다. 원본 다중 집합(Multiset)의 최솟값 확률 분포가 Jaccard 유사도와 같음을 이용합니다.
```python
import numpy as np

def minhash_signature(characteristics_matrix, num_hashes):
    """
    MinHash를 사용하여 문서의 Signature 생성
    :param characteristics_matrix: Column이 Document, Row이 Shingle의 Matrix (Sparse)
    :param num_hashes: 생성할 해시 함수 개수 (k)
    """
    rows, cols = characteristics_matrix.shape
    # 1부터 rows크기의 난수 생성 배열 (해시 함수 역할)
    permutation_indices = [np.random.permutation(rows) for _ in range(num_hashes)]
    
    signature = np.full((num_hashes, cols), fill_value=np.inf) # 무한대로 초기화

    for doc_idx in range(cols):
        for hash_idx in range(num_hashes):
            # 해당 문서 컬럼에서 1(Shingle 존재)인 것만 찾음
            perm = permutation_indices[hash_idx]
            # permutation 순서대로 순회하며 가장 먼저 나오는 1의 위치를 기록
            for i in range(rows):
                if characteristics_matrix[perm[i], doc_idx] == 1:
                    signature[hash_idx, doc_idx] = min(signature[hash_idx, doc_idx], i) # Min값 갱신
                    break # 최솟값 찾으면 탈출
    return signature
```
이 시그니처 벡터들 간의 Hamming Distance를 비교하면 원본 Jaccard Similarity의 근사치를 얻을 수 있습니다.

> **📢 섹션 요약 비유**: LSH의 AND-OR 구성은 **'다중 보안 시스템'**과 같습니다. 'AND(게이트)'는 모든 열쇠(해시 함수)가 맞아야만 문이 열리므로 더 엄격하게(정확하게) 사람을 거르고, 'OR(게이트)'는 하나의 열쇠라도 맞으면 들여보내주므로 누락 없이(재현율 높게) 사람을 모읍니다. 이 둘을 섞어서 빠르고 정확하게 원하는 사람을 찾아내는 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교표 (LSH vs. KD-Tree vs. K-NN)

| 비교 항목 (Metric) | **LSH (Locality Sensitive Hashing)** | **KD-Tree (Space Partitioning)** | **Brute-force K-NN** |
|:---|:---|:---|:---|
| **핵심 전략** | 확률적 충돌 유도 및 해시 버킷 탐색 | 공간 분할 트리를 이용한 재귀적 탐색 | 전체 데이터와의 거리 계산 |
| **시간 복잡도 (Search)** | $O(d \cdot L + v \cdot d)$ (Sub-linear) | $O(d \log N)$ (Low-dim only) | $O(N \cdot d)$ (Linear) |
| **공간 복잡도** | $O(N \cdot L)$ (테이블 개수만큼 증가) | $O(N)$ | $O(N)$ |
| **고차원 성능** | **우수** (차원의 저주에 강함) | **불량** (차원이 높아지면 선형 탐색으로 퇴보) | **중립** (항상 $N$만큼 소요) |
| **결과 정확도** | 근사치 (Approximate) | 정확치 (Exact) | 정확치 (Exact) |
| **주요 용도** | 초대규모 이미지/텍스트 검색 | 저차원 수치 데이터 탐색 | 소규모 데이터셋, 정확도 중시 |

#### 2. 과목 융합 관점 분석

**[데이터베이스 & 검색 엔진 (DB & IR)]**
- **시너지**: RDBMS의 B-Tree 인덱스는 '정확히 일치(Equality)'하는 검색에 최적화되어 있어, '유사(Similarity)' 검색에는 비효율적입니다. LSH는 Vector DB(예: Pinecone, Milvus)의 핵심 인덱싱 기법으로 사용되어, 전통적인 SQL 질의 방식을 벡터 유사도 검색으로 확장합니다.
- **오버헤드**: LSH를 위한 별도의 해시 테이블 유지 비용과, 삽입/삭제 시 재해싱(Rehashing) 발생에 따른 DB Write 성능 저하 가능성 존재.

**[운영체제 & 메모리 관리 (OS)]**
- **시너지**: OS의 페이지 교체 알고리즘과 유사하게 'Locality(지역성)'를 활용합니다. LSH는 데이터의 물리적 메모리 배치가 아닌, 논리적 유사도 공간에서의 지역성을 보장하여 캐시 적중률(Cache Hit Ratio)을 높이는 데 기여할 수 있습니다.
- **오버헤드**: 고차원 벡터 연산은 CPU 부하가 높으므로, SIMD(Single Instruction Multiple Data) 명령어나 GPU 가속을 통한 하드웨어적 보완이 필요합니다.

> **📢 섹션 요약 비유**: LSH와 KD-Tree의 차이는 **'전화번호부 찾기'와 '지도상에서 위치 찾기'**의 차이와 같습니다. KD-Tree는 좌표를 잘게 쪼개어 지도(공간)에서 찾는 방식이라 데이터가 복잡하게 뒤섞이면(고차원) 길을 잃기 쉽지만, LSH는 해당하는 번호(해시)를 바로 걸어보는 방식이라 지도가 복잡해도 빠르게 연결할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스

**시나리오 A: 대규모 이커머스 상품 추천 (Real-time Recommendation)**
- **상황**: 1,000만 개의 상품 벡터 중 사용자 행동 기반으로 Top 10 추출.
- **의사결정**: HNSW(Hierarchical Navigable Small World) 같은 그래프 기반 인덱스와 함께 LSH를 1차 필터로 활용.
- **이유**: 초 milliseconds(ms) 응답이 필요하므로 정밀도보다 속도가 우선.

**시나리오 B: 뉴스 기사 중복 확인 (Deduplication System)**
- **상황**: 매시간