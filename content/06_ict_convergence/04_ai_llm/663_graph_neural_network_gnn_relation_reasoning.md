---
title: "Graph Neural Network GNN Relation Reasoning"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 663
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GNN 관계 추론은 노드/엣지의 특성 벡터($\mathbf{h}_v^{(l)}$, $\mathbf{h}_{(u,v)}^{(l)}$)에 대해 메시지 패싱 함수 $\mathbf{m}_{u\rightarrow v}^{(l)} = \text{MSG}^{(l)}(\mathbf{h}_u^{(l-1)}, \mathbf{h}_v^{(l-1)}, \mathbf{h}_{(u,v)}^{(l-1)})$과 집계 함수 $\mathbf{h}_v^{(l)} = \text{UPD}^{(l)}\left(\mathbf{h}_v^{(l-1)}, \text{AGG}^{(l)}\left(\{\mathbf{m}_{u\rightarrow v}^{(l)} : u \in \mathcal{N}(v)\}\right)\right)$을 반복 적용하여 그래프 구조와 관계 유형을 잠재 임베딩 공간에 공동 인코딩하는 기법이다.
> 2. **가치**: 지식 그래프 완성도 MRR 0.49(Hits@1 0.44) 수준으로 TransE 0.30 대비 약 63% 성능 향상을 달성하며, 소셜 네트워크·사기 탐지·신약 개발 등에서 명시적 라벨 없이도 관계 패턴을 학습해 F1 0.85 이상의 추론 정확도를 제공한다.
> 3. **판단 포인트**: 동질(Homogeneous) vs 이질(Heterogeneous) 그래프, 트랜스덕티브(Transductive, 예: GCN) vs 귀납적(Inductive, 예: GraphSAGE) 학습, 단일 관계(Single-relational) vs 다중 관계(Multi-relational, 예: R-GCN), 그리고 정적(Static) vs 동적(Temporal, 예: TGN) 그래프의 4가지 축을 기준으로 모델·손실 함수·샘플링 전략을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

기존의 심층학습 모델(CNN, RNN, Transformer)은 유클리드 공간의 격자(Grid) 또는 시퀀스(sequence) 데이터에 최적화되어 있어, **비유클리드(non-Euclidean)** 구조인 그래프 데이터의 **위상 정보(topological information)**와 **관계적 의존성(relational dependency)**을 직접 표현하지 못하는 한계가 있었다. 2017년 Kipf & Welling의 GCN(Graph Convolutional Network), 2018년 Veličković의 GAT(Graph Attention Network) 등장 이후 그래프 자체를 학습 가능한 구조로 처리하는 패러다임이 정착되었으며, 2020년 이후에는 단순 노드 분류를 넘어 **관계 추론(Relation Reasoning)**이 핵심 과제로 부상했다. 관계 추론이란 (1) 두 노드 간 존재하지 않는 엣지의 가능성을 점수화하는 **링크 예측(Link Prediction)**, (2) 지식 그래프의 누락 트리플 $(h, r, t)$을 완성하는 **Knowledge Graph Completion(KGC)**, (3) 하위 그래프 패턴의 논리적 결합을 추론하는 **상식 추론(Commonsense Reasoning)**을 포괄한다.

```text
[기존 패러다임 vs GNN 관계 추론 패러다임]

   +----------------------------------+        +----------------------------------+
   |   전통적 관계 추론 (Pre-2017)     |        |   GNN 기반 관계 추론 (2017~)      |
   |                                  |        |                                  |
   |   Rule-based  --- IF-THEN 규칙   |        |   End-to-End 임베딩 학습         |
   |   Statistical -- Markov 논리     |   ⇒    |   그래프 구조 + 관계 동시 학습    |
   |   Path-based  -- PRA, PathRank   |        |   메시지 패싱으로 k-hop 추론      |
   |                                  |        |   사전 라벨 없는 노드 추론 가능   |
   +----------------------------------+        +----------------------------------+
              |                                          |
              v                                          v
   +-------------------------+             +------------------------------+
   | 한계:                   |             | 해결:                        |
   | • 0/1 hard-rule 매칭    |             | • 확률적 soft reasoning       |
   | • sparse path 한계      |             | • dense embedding 활용        |
   | • feature 활용 미흡     |             | • inductive 일반화            |
   | • 확장성 저하 (O(|E|²)) |             | • linear-time inference       |
   +-------------------------+             +------------------------------+
```

추가로, 웹 스케일 환경에서는 노드 수 10억 개, 엣지 수 100B 이상의 거대 그래프(예: Twitter Follower Graph, Google Knowledge Graph 800B facts)가 존재하여 **full-batch 학습의 불가능성**과 **메모리 폭발** 문제가 발생한다. 이를 해결하기 위해 **Neighbor Sampling (GraphSAGE)**, **Cluster-GCN**, **GraphSAINT**, **LADIES** 등 미니배치 샘플링 기법이 필수적이며, 실무에서는 PyTorch Geometric / DGL / TF-GNN 같은 분산 친화적 프레임워크 선택이 관건이 된다.

- **📢 섹션 요약 비유**: GNN 관계 추론은 마치 **"우체부들의 마을 정보망"**과 같다. 각 우체부(노드)는 자신의 이웃에게서 소포(메시지)를 받아 합산(집계)한 뒤, 자신만의 주소 라벨(임베딩)을 업데이트한다. 마을 전체가 점점 정확한 우편 배달망(그래프 구조)을 학습해, 처음 가본 두 집 사이의 최적 경로(잠재 관계)도 예측해낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GNN의 학습은 **순전파(Forward Pass)** 단계에서 반복적으로 발생하며, $L$층의 GNN은 최대 $L$-hop 떨어진 이웃까지의 정보를 임베딩에 반영한다. 관계 추론에서는 여기에 **관계 임베딩(relation embedding) $\mathbf{r}_e \in \mathbb{R}^d$**을 추가하여 메시지 함수와 집계 함수를 변형한다. 일반적인 **R-GCN(Relational Graph Convolutional Network)**의 레이어별 갱신은 다음과 같다.

```text
[R-GCN 기반 관계 추론 아키텍처 및 데이터 흐름]

   입력 그래프 (Knowledge Graph 예)
   +--------------------------------------------------------------+
   |                                                              |
   |    (Tom) --[friend_of]--► (Jerry)    노드 feature:  x_v ∈ ℝ^d|
   |       |                    |          엣지 feature:  r_e ∈ ℝ^d|
   |       |                    |                                    |
   |    [owns]              [lives_in]   라벨: y_v, (h,r,t) triple  |
   |       |                    |                                    |
   |       v                    v                                    |
   |   (House) ◄--[built_in]-- (City)                                 |
   |                                                              |
   +--------------------------------------------------------------+
                          |
                          v
   +----------- Layer 0: 입력 임베딩 매핑 -------------+
   |  h_v^(0) = W_init · x_v     (선형 투영)         |
   |  h_e^(0) = Embedding(r_e)   (관계 임베딩 룩업)    |
   +---------------------------------------------------+
                          |
                          v
   +----------- Layer 1 ~ L: 메시지 패싱 (R-GCN) -----+
   |                                                    |
   |  for l = 1..L:                                     |
   |    m_{u->v}^(l) = (1/c_{v,r}) · W_r^(l) · h_u^(l-1)|
   |                  + W_self^(l) · h_v^(l-1)         |
   |                  [관계별 가중치 + self-loop]         |
   |                                                    |
   |    h_v^(l) = σ(AGG({ m_{u->v}^(l) : (u,r,v) ∈ E }))|
   |                ^                                  |
   |      sum / mean / max / attention                  |
   |                                                    |
   |  정규화 계수 c_{v,r} = |N_r(v)|  (관계별 차수)    |
   +---------------------------------------------------+
                          |
                          v
   +----------- 출력 헤드 (태스크별 분기) --------------+
   |                                                    |
   |  ① 노드 분류:  ŷ_v = softmax(MLP(h_v^(L)))        |
   |  ② 링크 예측:  score(h,r,t) = f(h_h, r, h_t)       |
   |      - DistMult: <h_h, r, h_t>                      |
   |      - TransE: -||h_h + r - h_t||_p                  |
   |      - RotatE: -||h_h ∘ r - h_t||  (복소수 회전)    |
   |  ③ 그래프 분류: ŷ_G = READOUT({h_v^(L) : v ∈ G})   |
   |                                                    |
   +---------------------------------------------------+
                          |
                          v
   +----------- 손실 함수 (예: KGC) ------------------+
   |                                                    |
   |  L = -log σ(score(h,r,t))                          |
   |      - Σ_{(h',r,t') ∈ neg} log σ(-score(h',r,t')) |
   |      [Positive vs Negative sampling, NCE 손실]     |
   |                                                    |
   +---------------------------------------------------+
                          |
                          v
   +----------- 추론 (Inference) ---------------------+
   |  후보 트리플 (h, r, ?) 또는 (?, r, t) 전체 스코어링|
   |  -> Top-K 엔티티 선택 -> Hits@K, MRR 평가          |
   +---------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **입력 임베딩 레이어** | 희소한 노드/엣지 ID를 밀집 벡터로 변환 | $\mathbf{x}_v = \text{Lookup}(V, v)$, $\mathbf{r}_e = \text{Lookup}(R, e)$; BERT/Word2Vec로 사전 학습 가능 (e.g., OGB ogbl-wikikg2) |
| **메시지 함수 MSG(·)** | 이웃의 정보를 관계 인지적으로 인코딩 | R-GCN: $\mathbf{W}_r^{(l)} \mathbf{h}_u^{(l-1)}$; CompGCN: 합성곱 $\mathbf{h}_u * \mathbf{r}_e$; GAT: $\alpha_{uv} \mathbf{W} \mathbf{h}_u$, $\alpha_{uv}=\frac{\exp(\text{LeakyReLU}(\mathbf{a}^T[\mathbf{W}\mathbf{h}_u\|\mathbf{W}\mathbf{h}_v]))}{\sum_k \exp(\cdots)}$ |
| **집계 함수 AGG(·)** | 가변 차수 이웃을 고정 크기 벡터로 축약 | sum (GCN, R-GCN), mean (GraphSAGE default), max-pool (SortPooling), LSTM (GraphSAGE advanced), attention-weighted sum (GAT, HAN) |
| **업데이트 + 활성화** | 노드 임베딩 갱신 및 비선형성 부여 | $\mathbf{h}_v^{(l)} = \text{ReLU}/\text{PReLU}\big(\mathbf{W}_{\text{self}}^{(l)}\mathbf{h}_v^{(l-1)} + \text{AGG}(\{\mathbf{m}_{u\to v}^{(l)}\})\big)$; GRU 기반 (GGNN) 가능 |
| **READOUT/풀링** | 그래프/서브그래프 단위 임베딩 산출 | sum/mean/max readout, Set2Set, DiffPool(계층적), SortPool, Jumping Knowledge (JK-Network) |
| **스코어링 함수 f(·)** | 트리플 $(h,r,t)$의 plausibility 점수화 | TransE ($-||\mathbf{h}+\mathbf{r}-\mathbf{t}||$), DistMult ($\langle \mathbf{h}, \mathbf{r}, \mathbf{t}\rangle$), ComplEx (복소 내적), RotatE ($\mathbf{t} = \mathbf{h} \circ \mathbf{r}$), QuatE (사원수) |
| **샘플러 / 미니배치** | 거대 그래프 학습을 위한 부분 그래프 추출 | Node Sampling (GraphSAGE: $S_1, S_2, ..., S_L$ fan-out), Cluster-GCN (METIS 분할), GraphSAINT (random walk sampler), ShaDow-GNN (k-hop subgraph) |

깊이 있는 설계 파라미터를 정리하면 다음과 같다.

1. **레이어 수 $L$의 trade-off**: $L$이 클수록 더 먼 거리의 정보가 임베딩에 반영되지만 **오버스무딩(over-smoothing)**이 발생한다(노드 임베딩이 서로 유사해져 구별력 저하). 보통 2~3층이 가장 흔하며, GCNII·APPNP·JK-Net이 이를 완화한다.
2. **관계별 가중치 행렬 $\mathbf{W}_r$의 파라미터 폭발**: 관계 수 $|R|$가 1,000 이상이면 R-GCN은 $O(|R| \cdot d^2)$ 파라미터로 메모리 부담. **Block-Diagonal**(basis decomposition, $\mathbf{W}_r = \sum_{b=1}^{B} a_{rb} V_b$) 또는 **CompGCN**으로 압축.
3. **평가 지표**: KGC에서 **MRR(Mean Reciprocal Rank)**, **Hits@1/3/10**이 표준. OGB 리더보드 기준 ogbl-wikikg2(2.5M nodes, 16K relations) MRR는 0.65+ (SOTA 2024 기준).
4. **Inductive vs Transductive**: 새 노드/엣지가 등장하는 환경(추천, 사기 탐지)에서는 노드 피처 기반의 **GraphSAGE** 또는 **GAT**가 필수. 학습 시 보지 못한 노드라도 임베딩 생성 가능.

- **📢 섹션 요약 비유**: 관계 추론 GNN은 **"경찰 수사 네트워크"**와 같다. 각 사건(노드)에는 담당 형사(임베딩)가 배정되고, 수사관들은 전화 통화(메시지 패싱)를 통해 단서를 공유한다. 형사 간 협력 강도(어텐션)는 관계 유형(친구/적/동료)에 따라 다르게 가중되며, 최종 보고서(READOUT)는 사건 전체의 맥락을 요약해 새로운 단서(누락된 관계)까지 추론해낸다.

---

## Ⅲ. 비교 및 연결

| 구분 | **GNN (GCN/GAT/SAGE)** | **TransE/ComplEx/RotatE (KGE)** | **Transformer Attention** | **마르코프 로직망(MLN)** | **R-GCN / CompGCN (관계형 GNN)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **입력 구조** | 비(非)유클리드 그래프 | (h, r, t) 트리플 집합 | 시퀀스/완전 연결 그래프 | 그래프 + 1차 논리 규칙 | 관계 유형이 명시된 다중 그래프 |
| **구조 정보 활용** | 인접 행렬 + 노드 피처 | 암묵적(transitive) | position encoding만 | 명시적 1차 논리 | 엣지 라벨 + 이웃 집합 |
| **관계 추론 능력** | 동질 그래프에 강함 | 관계 패턴은 강하나 멀리 떨어진 hop 약함 | 모든 토큰 쌍의 attention | 논리적 일관성 강함 | 다중 관계 + 멀티-홉 동시 인코딩 |
| **확장성 (10⁹ 노드)** | Cluster/ShaDow-GNN 필요 | O(|E|) 학습, 분산 용이 | O(L²) 메모리 (long context) | #rules 증가 시 폭발 | R-GCN은 basis 분해로 압축 |
| **설명 가능성** | 어텐션 가중치 시각화 | 거리 기반 단순 해석 | 어텐션 맵 | 규칙 직접 추출 | attention + path 기반 |
| **대표 응용** | 노드 분류, 추천, 사기 탐지 | 지식 그래프 완성 (FB15k, WN18) | LLM (GPT), 시계열 | 의료 추론