+++
title = "08. 알고리즘/자료구조/통계 키워드 목록"
date = 2026-03-03
[extra]
categories = "studynotes-algorithm"
+++

# 알고리즘 / 자료구조 / 통계 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 알고리즘·자료구조·통계 전 영역 핵심 키워드

---

## 1. 알고리즘 기초 — 14개

1. 알고리즘 (Algorithm) 정의 — 유한성/확정성/입력/출력/효율성
2. 시간 복잡도 (Time Complexity) — Big-O / Ω / Θ 표기법
3. 공간 복잡도 (Space Complexity)
4. O(1) / O(log n) / O(n) / O(n log n) / O(n²) / O(2ⁿ) / O(n!)
5. 분할 정복 (Divide and Conquer) — 재귀 분할 + 병합
6. 탐욕 알고리즘 (Greedy Algorithm) — 지역 최적 → 전체 최적
7. 동적 프로그래밍 (Dynamic Programming) — 최적 부분구조 + 중복 부분 문제
8. 메모이제이션 (Memoization) — Top-Down DP
9. 타뷸레이션 (Tabulation) — Bottom-Up DP
10. 백트래킹 (Backtracking) — 가지치기
11. 분기 한정 (Branch and Bound) — 최적화 탐색
12. 근사 알고리즘 (Approximation Algorithm) — NP 문제
13. 랜덤화 알고리즘 (Randomized Algorithm) — Las Vegas / Monte Carlo
14. 재귀 (Recursion) — 기본 사례, 재귀 사례, 스택 오버플로우

---

## 2. 정렬 알고리즘 — 18개

1. 버블 정렬 (Bubble Sort) — O(n²), 안정, 제자리
2. 선택 정렬 (Selection Sort) — O(n²), 불안정, 제자리
3. 삽입 정렬 (Insertion Sort) — O(n²)/O(n) 최선, 안정, 소규모 효율
4. 셸 정렬 (Shell Sort) — 삽입 정렬 개선, O(n^1.5)
5. 합병 정렬 (Merge Sort) — O(n log n), 안정, O(n) 공간
6. 퀵 정렬 (Quick Sort) — 평균 O(n log n), 최악 O(n²), 불안정
7. 퀵 정렬 최적화 — 3-way Partition, Median-of-3 Pivot
8. 힙 정렬 (Heap Sort) — O(n log n), 불안정, 제자리
9. 계수 정렬 (Counting Sort) — O(n+k), 비교 불필요
10. 기수 정렬 (Radix Sort) — O(d·n), 고정 자릿수
11. 버킷 정렬 (Bucket Sort) — O(n) 평균, 균등 분포
12. 팀 정렬 (Timsort) — Python/Java 기본, 합병+삽입 혼합
13. 인트로 정렬 (Introsort) — 퀵+힙+삽입 혼합, C++ STL
14. 정렬 안정성 (Stability) — 동일 키 순서 유지 여부
15. 외부 정렬 (External Sort) — 대용량 데이터, 멀티웨이 합병
16. 정렬 비교 — 시간/공간/안정성/적합 환경
17. 네트워크 정렬 (Sorting Network) — 병렬 정렬
18. 이분 탐색 (Binary Search) — O(log n), 정렬된 배열 필수

---

## 3. 탐색 / 그래프 알고리즘 — 24개

1. 선형 탐색 (Linear Search) — O(n)
2. 이진 탐색 (Binary Search) — O(log n)
3. 해시 탐색 (Hash Search) — O(1) 평균
4. 그래프 표현 — 인접 행렬 / 인접 리스트
5. DFS (Depth-First Search) — 깊이 우선, 스택/재귀
6. BFS (Breadth-First Search) — 너비 우선, 큐, 최단 경로(비가중)
7. 다익스트라 (Dijkstra) — 단일 출발 최단 경로, 비음수 가중치
8. 벨만-포드 (Bellman-Ford) — 음수 가중치 허용, O(VE)
9. 플로이드-워샬 (Floyd-Warshall) — 전체 쌍 최단 경로, O(V³)
10. A* 알고리즘 — 휴리스틱, 최단 경로
11. 위상 정렬 (Topological Sort) — DAG, Kahn's / DFS 기반
12. 강연결 요소 (SCC) — Kosaraju / Tarjan 알고리즘
13. 최소 신장 트리 (MST) — Kruskal / Prim
14. 크루스칼 (Kruskal) — 간선 정렬 + Union-Find
15. 프림 (Prim) — 정점 기반, 우선순위 큐
16. 최대 유량 (Max Flow) — Ford-Fulkerson / Edmonds-Karp
17. 이분 매칭 (Bipartite Matching) — 헝가리안 알고리즘
18. 유니온-파인드 (Union-Find / Disjoint Set) — 경로 압축, 랭크
19. 최소 컷 (Min Cut) — Max-Flow Min-Cut 정리
20. 오일러 경로/회로 — Fleury / Hierholzer
21. 해밀턴 경로 — NP-완전, 백트래킹
22. 외판원 문제 (TSP) — NP-hard, DP+비트마스크
23. 최장 공통 부분수열 (LCS) — DP, O(mn)
24. 최장 증가 부분수열 (LIS) — DP / 이진 탐색

---

## 4. 자료구조 — 28개

1. 배열 (Array) — 연속 메모리, O(1) 랜덤 접근
2. 연결 리스트 (Linked List) — 단일/이중/순환, 동적 삽입/삭제
3. 스택 (Stack) — LIFO, push/pop, 재귀/DFS/수식 평가
4. 큐 (Queue) — FIFO, enqueue/dequeue, BFS/스케줄링
5. 덱 (Deque, Double-Ended Queue) — 양방향 큐
6. 우선순위 큐 (Priority Queue) — 힙 기반 구현
7. 힙 (Heap) — 최대/최소 힙, 완전 이진 트리
8. 이진 트리 (Binary Tree) — 전위/중위/후위 순회
9. 이진 탐색 트리 (BST) — O(log n) 평균, O(n) 최악
10. AVL 트리 — 높이 균형, 회전 (LL/RR/LR/RL)
11. 레드-블랙 트리 (Red-Black Tree) — O(log n) 보장, Java TreeMap
12. B-트리 (B-Tree) — 다진 탐색, 디스크 기반, 균형
13. B+트리 (B+Tree) — 리프 연결, DB 인덱스
14. 트라이 (Trie) — 접두사 탐색, 자동 완성
15. 해시 테이블 (Hash Table) — 해시 함수, 충돌 처리
16. 개방 주소법 (Open Addressing) — 선형/이차/이중 해싱
17. 체인법 (Chaining) — 연결 리스트 충돌 처리
18. 그래프 (Graph) — 방향/무방향, 가중/비가중
19. 세그먼트 트리 (Segment Tree) — 구간 쿼리/업데이트
20. 펜윅 트리 / BIT (Binary Indexed Tree / Fenwick Tree) — 구간 합
21. 압축된 트라이 (Compressed Trie / Patricia Trie)
22. 서픽스 트리 (Suffix Tree) / 서픽스 배열 (Suffix Array)
23. 해시맵 (HashMap) vs 트리맵 (TreeMap) — 순서 유무
24. 스킵 리스트 (Skip List) — 확률적 균형, O(log n)
25. 유니온-파인드 (Union-Find) — 집합 연산
26. 단조 스택 (Monotonic Stack/Queue)
27. 스파스 테이블 (Sparse Table) — O(1) 구간 최소값 (RMQ)
28. 블룸 필터 (Bloom Filter) — 확률적 집합 멤버십, 공간 효율

---

## 5. 문자열 알고리즘 — 12개

1. KMP (Knuth-Morris-Pratt) — 패턴 매칭, 실패 함수
2. 보이어-무어 (Boyer-Moore) — 역방향 비교, 실용적 최적
3. 라빈-카프 (Rabin-Karp) — 롤링 해시, 다중 패턴
4. Z 알고리즘 — 접두사 매칭 배열
5. 아호-코라식 (Aho-Corasick) — 다중 패턴 동시 매칭
6. 런-길이 인코딩 (RLE) — 압축, 연속 반복
7. 허프만 코딩 (Huffman Coding) — 가변길이 최적 코드
8. LZ77 / LZ78 / LZW — 사전 기반 압축 (ZIP, GIF)
9. 최장 공통 부분수열 (LCS) — 문자열 비교
10. 편집 거리 (Edit Distance, Levenshtein Distance) — DP
11. 정규 표현식 (Regex) — NFA/DFA, 패턴 매칭
12. 접미사 배열 + LCP 배열 — 문자열 분석

---

## 6. NP 이론 / 계산 이론 — 14개

1. P 클래스 — 다항 시간 내 해결 가능
2. NP 클래스 — 다항 시간 내 검증 가능
3. NP-완전 (NP-Complete) — NP 중 가장 어려운 문제
4. NP-어려움 (NP-Hard) — NP보다 어렵거나 동등
5. P = NP 문제 — 미해결 난제
6. 다항 시간 환산 (Polynomial Reduction)
7. SAT (Satisfiability) — 최초 NP-완전 증명 (Cook-Levin)
8. 클리크 문제 (Clique Problem) — NP-완전
9. 정점 커버 (Vertex Cover) — NP-완전
10. 외판원 문제 (TSP) — NP-hard
11. 배낭 문제 (Knapsack Problem) — NP-완전 (결정 버전)
12. 근사 알고리즘 — ρ-근사, FPTAS, PTAS
13. 지수 시간 가설 (ETH) — 알고리즘 하한 도구
14. 양자 복잡도 (Quantum Complexity) — BQP, 양자 우위

---

## 7. 수치 알고리즘 — 10개

1. 유클리드 호제법 (Euclidean Algorithm) — GCD, O(log min)
2. 에라토스테네스의 체 (Sieve of Eratosthenes) — 소수 판별
3. 소수 판별 (Primality Test) — Miller-Rabin (확률적)
4. 거듭제곱 (Fast Exponentiation) — 분할 정복, O(log n)
5. 중국인의 나머지 정리 (CRT)
6. 가우스 소거법 (Gaussian Elimination) — 연립방정식
7. FFT (Fast Fourier Transform) — 다항식 곱, O(n log n)
8. 행렬 곱셈 (Matrix Multiplication) — Strassen O(n^2.81)
9. 뉴턴-랩슨 (Newton-Raphson) — 수치 해법, 제곱근
10. 몬테카를로 수치적분 — 확률적 근사

---

## 8. 확률 / 통계 기초 — 20개

1. 확률 (Probability) — 고전/상대도수/주관 확률
2. 베이즈 정리 (Bayes' Theorem) — P(A|B) = P(B|A)P(A)/P(B)
3. 조건부 확률 (Conditional Probability)
4. 독립 사건 (Independence) / 상호 배타적 사건
5. 확률 변수 (Random Variable) — 이산/연속
6. 기댓값 (Expected Value, E[X])
7. 분산 (Variance) / 표준편차 (Standard Deviation)
8. 확률 분포 — 이항/포아송/정규/지수/균등
9. 정규 분포 (Normal Distribution) — 68-95-99.7 규칙
10. 중심 극한 정리 (Central Limit Theorem, CLT)
11. 마르코프 체인 (Markov Chain) — 전이 확률, 정상 분포
12. 마르코프 성질 (Markov Property) — 미래 ⊥ 과거 | 현재
13. 기대치 최대화 (Expectation-Maximization, EM 알고리즘)
14. 최대 우도 추정 (MLE, Maximum Likelihood Estimation)
15. 베이즈 추정 (Bayesian Estimation) — MAP (최대 사후 확률)
16. 가설 검정 (Hypothesis Testing) — 귀무/대립 가설, p-value
17. 신뢰 구간 (Confidence Interval)
18. 카이제곱 검정 (Chi-Square Test) — 독립성 검정
19. t-검정 / F-검정 / ANOVA
20. 회귀 분석 (Regression Analysis) — 단순/다중/로지스틱

---

## 9. 정보이론 — 10개

1. 정보이론 (Information Theory) — Shannon, 1948
2. 엔트로피 (Shannon Entropy) — H(X) = -Σ p·log₂p
3. 상호 정보량 (Mutual Information)
4. KL 다이버전스 (KL Divergence) — 분포 간 차이
5. 크로스 엔트로피 (Cross-Entropy) — 분류 손실 함수
6. 채널 용량 (Channel Capacity) — 샤논 용량 공식
7. 소스 부호화 정리 (Source Coding Theorem)
8. 채널 부호화 정리 (Channel Coding Theorem) — Shannon Limit
9. 오류 정정 부호 (Error Correcting Code) — 해밍/(터보)/LDPC/폴라
10. 압축 (Compression) — 무손실/손실, 허프만/LZ/웨이블릿

---

## 10. 선형대수 / 최적화 — 10개

1. 선형 연립방정식 — 행렬 표현, 가우스 소거
2. 행렬 분해 — LU / QR / SVD (Singular Value Decomposition)
3. 고유값 / 고유벡터 (Eigenvalue/Eigenvector)
4. PCA (Principal Component Analysis) — SVD 기반 차원 축소
5. 볼록 함수 (Convex Function) — 전역 최적 보장
6. 기울기 하강법 (Gradient Descent) — 최적화 기본
7. 라그랑주 승수법 (Lagrange Multiplier) — 제약 최적화
8. 선형 프로그래밍 (LP) — 심플렉스법
9. 정수 프로그래밍 (IP) — 분기 한정, MILP
10. 진화 알고리즘 — 유전 알고리즘 (GA), 입자 군집 최적화 (PSO)

---

**총 키워드 수: 160개**
