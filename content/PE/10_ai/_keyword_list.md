+++
title = "10. 인공지능 (AI) 및 머신러닝 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynotes-ai"
+++

# 인공지능 (AI) / 머신러닝 / 딥러닝 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 및 AI/데이터 사이언티스트를 위한 인공지능 전 영역 핵심 및 심화 키워드 800선입니다.

기초 머신러닝 알고리즘부터 최신 딥러닝(CNN, RNN, Transformer), 초거대 언어 모델(LLM), 생성형 AI(Generative AI, RAG), MLOps, AI 윤리 및 최신 AI 아키텍처 동향까지 총망라하였습니다.

---

## 1. 인공지능 기초 및 탐색 / 전문가 시스템 (60개)
1. 인공지능 (Artificial Intelligence)의 정의 - 지능적 기계 및 에이전트를 설계하는 학문
2. 튜링 테스트 (Turing Test) - 앨런 튜링 제안, 기계가 지능이 있는지를 판별하는 텍스트 대화 시험
3. 강인공지능 (Strong AI / AGI, Artificial General Intelligence) - 인간과 같거나 뛰어난 범용 지능
4. 약인공지능 (Weak AI / Narrow AI) - 특정 작업(바둑, 번역, 인식)에만 특화된 지능
5. 초인공지능 (ASI, Artificial Super Intelligence) - 모든 면에서 인간을 초월한 지능
6. 싱귤래리티 (Singularity / 특이점) - 인공지능이 스스로 자신보다 나은 AI를 만들어내어 기술 발전이 무한히 폭발하는 시점
7. 지식 표현 (Knowledge Representation) - 규칙 기반, 의미망, 프레임, 스크립트 등
8. 지식 베이스 (Knowledge Base) / 추론 엔진 (Inference Engine)
9. 전문가 시스템 (Expert System) - 특정 분야 전문가의 지식을 룰 기반으로 구현 (MYCIN, DENDRAL)
10. 전향 추론 (Forward Chaining) - 데이터에서 시작하여 결론 도출 (데이터 주도)
11. 후향 추론 (Backward Chaining) - 가설/목표에서 시작하여 조건 데이터 검증 (목표 주도)
12. 퍼지 논리 (Fuzzy Logic) - 0과 1 사이의 확률적 연속값(소속도)을 이용해 애매한 개념 처리 (Zadeh 제안)
13. 상태 공간 탐색 (State Space Search)
14. 맹목적 탐색 (Uninformed Search) - DFS(깊이 우선 탐색), BFS(너비 우선 탐색)
15. 휴리스틱 탐색 (Heuristic Search / Informed Search) - 직관이나 경험 기반 정보(휴리스틱 함수)를 활용한 최적 탐색
16. 언덕 오르기 탐색 (Hill Climbing) - 현재 상태에서 이웃 상태 중 가장 좋은 곳으로만 이동 (지역 최적해에 빠질 위험)
17. A* (A-Star) 알고리즘 - f(n) = g(n) + h(n), 시작점부터의 실제 비용 g(n)과 목표까지의 예상 비용 h(n)을 합산하여 최단 경로 탐색
18. 허용적 휴리스틱 (Admissible Heuristic) - A*가 최적해를 보장하기 위한 조건, h(n)이 실제 목표까지의 비용을 과대평가하지 않아야 함
19. 미니맥스 알고리즘 (Minimax Algorithm) - 턴제 게임 트리(체스, 틱택토)에서 자신은 최대(Max), 상대는 최소(Min)를 선택한다고 가정하고 탐색
20. 알파-베타 가지치기 (Alpha-Beta Pruning) - 미니맥스 트리에서 탐색할 필요가 없는 가지를 잘라내어 연산량 감소
21. 몬테카를로 트리 탐색 (MCTS, Monte Carlo Tree Search) - 바둑(알파고) 등 경우의 수가 방대한 게임에서 무작위 시뮬레이션(롤아웃)을 통해 승률을 계산하여 최적 경로를 확장하는 탐색 기법
22. MCTS 4단계 - 선택(Selection) -> 확장(Expansion) -> 시뮬레이션(Simulation) -> 역전파(Backpropagation)
23. 머신러닝 (Machine Learning) 개념 - 데이터를 통해 기계가 스스로 규칙과 패턴을 학습
24. 학습의 3가지 패러다임 - 지도 학습(Supervised), 비지도 학습(Unsupervised), 강화 학습(Reinforcement)
25. 편향-분산 트레이드오프 (Bias-Variance Trade-off)
26. 편향 (Bias) - 모델이 너무 단순하여 실제 데이터 패턴을 놓침 (과소적합, Underfitting)
27. 분산 (Variance) - 모델이 학습 데이터의 노이즈까지 과도하게 외워버림 (과대적합, Overfitting)
28. 오캄의 면도날 (Occam's Razor) 원칙 - 같은 성능이면 구조가 단순한 모델이 낫다.
29. 차원의 저주 (Curse of Dimensionality) - 특성(변수) 공간 차원이 늘어날수록, 데이터 간 거리가 희소해지고 학습 효율이 급감하는 현상
30. 차원 축소 (Dimensionality Reduction) 기법
31. 독립 변수 (Independent Variable / Feature) / 종속 변수 (Dependent Variable / Target/Label)
32. 회귀 (Regression) - 연속적인 수치 예측 (집값, 주가)
33. 분류 (Classification) - 이산적인 클래스 판별 (스팸 여부, 개/고양이 사진)
34. 군집화 (Clustering) - 정답(Label) 없이 데이터의 유사도에 따라 그룹 묶기
35. 연관 규칙 (Association Rules) - 장바구니 분석 (A를 사면 B도 산다)
36. 특성 공학 (Feature Engineering) - 도메인 지식을 활용하여 모델 학습에 좋은 피처(Feature)를 추출/가공
37. 원-핫 인코딩 (One-Hot Encoding) - 범주형 데이터를 0과 1의 벡터로 변환
38. 라벨 인코딩 (Label Encoding) / 정수 인코딩
39. 스케일링 (Scaling) - 정규화(Normalization, 0~1), 표준화(Standardization, 평균 0 표준편차 1 Z-score)
40. 교차 검증 (Cross-Validation) - K-Fold 분할 모델 평가 기법 (과적합 방지, 일반화 성능 확인)
41. 하이퍼파라미터 (Hyperparameter) - 모델 학습 전 인간(엔지니어)이 직접 설정해야 하는 변수 (학습률, 트리 깊이 등)
42. 그리드 서치 (Grid Search) / 랜덤 서치 (Random Search) / 베이지안 최적화 - 하이퍼파라미터 튜닝 기법
43. 평가 지표 - 혼동 행렬 (Confusion Matrix: TP, FP, FN, TN)
44. 정확도 (Accuracy) - 전체 대비 정답 비율 (데이터 불균형 시 왜곡)
45. 정밀도 (Precision) - 모델이 Positive로 예측한 것 중 실제 Positive의 비율
46. 재현율 (Recall / 민감도 / TPR) - 실제 Positive 중에서 모델이 맞춘 비율
47. F1-Score - 정밀도와 재현율의 조화 평균
48. ROC 커브 (Receiver Operating Characteristic) & AUC (Area Under Curve) - 임계값 변화에 따른 FPR 대비 TPR 그래프
49. 앙상블 학습 (Ensemble Learning) - 여러 개의 약한 분류기를 결합하여 강력한 하나의 모델 구성
50. 보팅 (Voting) - 다수결 (Hard Voting) 및 확률 평균 (Soft Voting)
51. 배깅 (Bagging, Bootstrap Aggregating) - 훈련 데이터를 랜덤 복원 추출하여 독립 모델 병렬 학습 후 평균/다수결 (Random Forest)
52. 부스팅 (Boosting) - 앞 모델이 틀린 오차(잔차)에 가중치를 부여해 다음 모델이 순차적으로 보완 (AdaBoost, GBM, XGBoost, LightGBM)
53. 스태킹 (Stacking) - 여러 모델의 예측 결과를 다시 훈련 데이터로 삼아 메타 모델이 최종 학습
54. 결정 트리 (Decision Tree) 학습 (불순도 기준 - 엔트로피, 지니 지수)
55. 로지스틱 회귀 (Logistic Regression) - Sigmoid 함수 기반 이진 분류 선형 모델
56. K-NN (K-Nearest Neighbors) - 새로운 데이터를 가장 가까운 K개 이웃의 클래스 중 다수결로 판별 (게으른 학습, Lazy Learning)
57. K-Means 군집화 (비지도 학습) - K개의 중심점(Centroid)을 잡고 거리 기반 데이터 할당, 중심점 이동 반복 EM(Expectation Maximization)
58. SVM (Support Vector Machine) - 두 클래스 간의 마진(Margin)을 최대화하는 초평면(Hyperplane)을 찾는 분류/회귀 모델
59. 커널 트릭 (Kernel Trick) - 선형 분류 불가능 데이터를 고차원 내적 공간으로 매핑해 분리 (RBF 커널, 다항식 커널)
60. 나이브 베이즈 분류기 (Naive Bayes) - 변수들이 조건부 독립이라 가정하고 베이즈 정리를 적용한 확률적 분류기 (스팸 필터링)

## 2. 딥러닝 기초 및 신경망 아키텍처 (70개)
61. 인공 신경망 (ANN, Artificial Neural Network) - 인간 두뇌의 뉴런 생물학적 구조를 모방한 모델
62. 퍼셉트론 (Perceptron) - 로젠블랫 제안, 입력값 덧셈 후 임계치 넘으면 1 출력 (단층 신경망)
63. 단층 퍼셉트론의 한계 - XOR(배타적 논리합) 문제 등 선형 분리 불가 문제 해결 못함 (AI의 1차 암흑기 원인)
64. 다층 퍼셉트론 (MLP, Multi-Layer Perceptron) - 은닉층(Hidden Layer) 도입으로 비선형 문제 해결 가능
65. 심층 신경망 (DNN, Deep Neural Network) - 2개 이상의 은닉층을 가진 다층 퍼셉트론
66. 가중치 (Weight, W) / 편향 (Bias, b) - 선형 방정식의 파라미터 (y = Wx + b)
67. 활성화 함수 (Activation Function) - 신경망 층 사이에 비선형성(Non-linearity)을 부여하는 필수 함수
68. 계단 함수 (Step Function) - 0 이하면 0, 0 이상이면 1 반환 (미분 불가)
69. 시그모이드 함수 (Sigmoid) - 0~1 사이 반환, 기울기 소실(Vanishing Gradient) 문제 발생
70. 하이퍼볼릭 탄젠트 (tanh) - -1~1 사이 반환, 중심이 0으로 수렴 (시그모이드보다 우수)
71. ReLU (Rectified Linear Unit) 함수 - x>0이면 x, x<0이면 0 (기울기 소실 해결, 연산 빠름, 현재 가장 대중적)
72. Leaky ReLU / ELU - ReLU의 죽은 뉴런(Dying ReLU, 음수 입력 시 가중치 미갱신) 문제 해결 (음수 구간에 미세한 기울기 부여)
73. 소프트맥스 함수 (Softmax) - 다중 클래스 분류 시 출력층 적용, 결과값 총합을 1로 만들어 확률화
74. 순전파 (Forward Propagation) - 입력 데이터가 신경망 층을 통과하여 최종 출력(예측값) 계산 과정
75. 손실 함수 (Loss Function / Cost Function) - 정답(실제값)과 예측값의 오차 계산 (학습 방향 지시)
76. MSE (Mean Squared Error) - 평균 제곱 오차, 회귀 문제 손실 함수
77. 크로스 엔트로피 오차 (Cross-Entropy Error) / Log Loss - 이진 및 다중 분류 문제 손실 함수
78. 역전파 (Backpropagation) - 연쇄 법칙(Chain Rule)을 적용, 출력층의 오차를 입력층 방향으로 거슬러 전달하며 각 층의 가중치 미분값(기울기)을 구하는 핵심 알고리즘
79. 옵티마이저 (Optimizer) - 손실 함수의 값을 최소화하도록 가중치를 갱신하는 최적화 알고리즘
80. 경사 하강법 (GD, Gradient Descent) - 손실 함수의 기울기가 감소하는 방향으로 학습률(Learning Rate)만큼 이동
81. 확률적 경사 하강법 (SGD, Stochastic Gradient Descent) - 전체 데이터가 아닌 미니배치(Mini-batch)로 기울기 계산 (속도 향상, 노이즈 수반)
82. 미니배치 사이즈 (Mini-batch Size) / 에폭 (Epoch) / 이터레이션 (Iteration)
83. 지역 최솟값 (Local Minima) vs 전역 최솟값 (Global Minimum) 안착 문제
84. 모멘텀 (Momentum) - 이전 기울기 관성을 활용하여 가속 이동 (Local Minima 탈출 효과)
85. 적응형 학습률 (Adaptive Learning Rate) - 변수별로 학습률 크기를 자동 조절 (Adagrad, RMSProp)
86. Adam (Adaptive Moment Estimation) - 모멘텀(관성) 방향성 + RMSProp(스텝 사이즈 자동조절) 결합 (최신 딥러닝 기본 옵티마이저)
87. 가중치 초기화 (Weight Initialization) - 0초기화 금지, 사비에르(Xavier) 초기화(Sigmoid 특화), He 초기화(ReLU 특화)
88. 기울기 소실 (Vanishing Gradient) - 역전파 중 미분값이 0에 가까워져 앞쪽 은닉층 가중치 갱신 불가 현상 (ReLU, 잔차 연결 제안)
89. 기울기 폭발 (Exploding Gradient) - 갱신폭이 기하급수적 커짐 (가중치 클리핑 / Gradient Clipping 적용)
90. 정규화 및 과적합 방지 기법 (Regularization)
91. L1/L2 규제 (L1/L2 Regularization / 가중치 감쇠 Weight Decay) - 손실 함수에 가중치 절대값 합(L1)이나 제곱합(L2) 페널티 추가 
92. 드롭아웃 (Dropout) - 학습 시 은닉층 뉴런의 일부를 임의 확률(예 50%)로 비활성화하여 과의존 및 과적합 방지 (추론 시엔 모두 사용)
93. 조기 종료 (Early Stopping) - 검증 데이터(Validation)의 손실이 줄어들지 않으면 에폭이 남아도 훈련 조기 중단
94. 배치 정규화 (Batch Normalization) - 미니배치 단위로 층의 입력을 평균 0, 분산 1로 정규화 연산 삽입 (학습 가속 및 안정화 효과)
95. 합성곱 신경망 (CNN, Convolutional Neural Network) - 이미지/영상 인식 특화 공간 정보 보존 신경망 아키텍처
96. 합성곱 층 (Convolution Layer) - 필터/커널(Filter/Kernel)을 입력 이미지 위로 이동(Stride)시키며 합성곱 연산 수행 (특성 추출)
97. 스트라이드 (Stride) - 커널의 이동 보폭 칸 수
98. 패딩 (Padding) - 이미지 크기 축소 방지 및 가장자리 데이터 보존을 위해 가장자리에 0 등 추가 (Zero Padding)
99. 특성 맵 (Feature Map) / 액티베이션 맵 - 합성곱 결과 출력 배열
100. 풀링 층 (Pooling Layer) - 특성 맵의 주요 정보만 남기고 크기(해상도)를 줄여 공간 불변성(Translation Invariance) 확보 및 연산량 감소
101. 최대 풀링 (Max Pooling) / 평균 풀링 (Average Pooling)
102. 완전 연결 층 (FC, Fully Connected Layer / Dense Layer) - 추출된 특성을 1차원으로 펴서(Flatten) 분류/회귀 수행
103. CNN 주요 아키텍처 발전 - LeNet-5, AlexNet(ReLU 도입), VGGNet, GoogLeNet(Inception 구조), ResNet
104. ResNet (Residual Network) - 잔차 연결(Skip Connection / Shortcut) 구조 도입으로 100층 이상 깊은 네트워크의 기울기 소실 문제 파훼
105. 1x1 합성곱 연산의 차원 축소/병목(Bottleneck) 최적화 역할
106. 객체 탐지 (Object Detection) 기술 - 이미지 내의 객체 종류(Classification)와 박스 위치 좌표(Bounding Box/Localization) 판별
107. R-CNN, Fast R-CNN, Faster R-CNN (2-Stage 탐지기) / Region Proposal Network (RPN)
108. YOLO (You Only Look Once), SSD (1-Stage 탐지기) - 실시간/초고속 탐지 
109. 이미지 분할 (Image Segmentation) - 단순 박스가 아닌 픽셀 단위 픽셀 분류
110. 의미적 분할 (Semantic Segmentation / FCN, U-Net 구조) vs 인스턴스 분할 (Instance Segmentation / Mask R-CNN)
111. 순환 신경망 (RNN, Recurrent Neural Network) - 음성, 텍스트 등 시계열 (Sequential) 순차 데이터 처리에 특화된 구조
112. 은닉 상태 (Hidden State) 순환 루프 - 이전 시간(t-1) 연산 결과가 다음 시간(t) 입력의 일부로 재활용되어 문맥(Context) 기억
113. 장기 의존성 문제 (Long-term Dependency) - RNN 시퀀스가 길어지면 초기 정보가 희석(기울기 소실)되는 한계
114. BPTT (Backpropagation Through Time) - 시간에 따른 오차 역전파
115. LSTM (Long Short-Term Memory) - RNN 한계 극복, 은닉 상태(단기기억) 외에 셀 상태(Cell State, 장기기억) 컨베이어 벨트 도입
116. LSTM의 3가지 게이트 - 입력 게이트(Input), 삭제 게이트(Forget, 기존 기억 폐기 비율 결정), 출력 게이트(Output)
117. GRU (Gated Recurrent Unit) - LSTM의 복잡한 구조를 간소화(업데이트/리셋 게이트), 연산 속도 개선
118. 양방향 RNN (Bidirectional RNN) - 과거뿐만 아니라 미래의 문맥 역방향 연산 결과도 활용
119. Seq2Seq (Sequence to Sequence) 모델 - 인코더(Encoder)-디코더(Decoder) 구조, 기계 번역 및 챗봇 뼈대
120. 컨텍스트 벡터 (Context Vector) - 인코더의 최종 은닉 상태, 고정된 크기 배열에 모든 의미를 압축해야 하는 병목 한계 (어텐션 탄생 배경)

## 3. 어텐션, 트랜스포머, 초거대 언어 모델 (LLM) 및 생성형 AI (60개)
121. 어텐션 메커니즘 (Attention Mechanism) - Seq2Seq 한계 극복, 디코더가 매 단어를 생성할 때마다 인코더의 전체 시퀀스 중 '어느 부분에 집중(Attention)해야 하는지' 동적 가중치 연산
122. 쿼리(Query), 키(Key), 값(Value) 체계 - 데이터베이스 검색과 유사, Q(현재 상태)와 가장 일치하는 K(인코더 출력)를 찾아 V(인코더 값)를 가중합
123. 트랜스포머 (Transformer) 아키텍처 - 2017년 구글 "Attention Is All You Need" 논문 제안. RNN/CNN을 완전히 배제하고 '오직 어텐션'만으로 구성, 병렬 연산 극대화
124. 셀프 어텐션 (Self-Attention) - 입력 시퀀스 내부 단어들끼리의 상호 연관성/문맥을 계산 (it이 가리키는 대명사 유추 등)
125. 멀티 헤드 어텐션 (Multi-Head Attention) - 어텐션 연산을 병렬로 N개 수행하여 다각도(문법, 의미, 구조 등)의 특성 정보 추출
126. 포지셔널 인코딩 (Positional Encoding) - 트랜스포머는 RNN과 달리 단어를 한 번에 병렬 입력받으므로 순서 정보가 소실됨 -> 단어 위치(순서) 수학 값을 벡터에 더해줌
127. 마스크드 셀프 어텐션 (Masked Self-Attention) - 디코더 훈련 시 미래의 단어를 미리 보지 못하도록(정답 컨닝 방지) 행렬을 가리는 마스킹 연산
128. 인코더-디코더 어텐션 (Cross Attention)
129. 피드 포워드 신경망 (FFNN, Position-wise Feed-Forward) 적용망
130. 파운데이션 모델 (Foundation Model) - 대규모 정제되지 않은 데이터(Self-supervised)로 사전 학습(Pre-training)되어 여러 다운스트림(Downstream) 태스크로 전이(Adaptable)할 수 있는 초대형 모델 체계
131. 자기 지도 학습 (Self-Supervised Learning) - 정답 라벨 없이 데이터 자체의 구조(빈칸 채우기, 다음 단어 예측)로 학습 목표를 자동 설정
132. 전이 학습 (Transfer Learning) - 대규모 데이터로 학습된 기본 모델(가중치)을 가져와 내 작은/특화된 데이터에 맞게 재학습(파인튜닝)하여 시간/비용 절약
133. 파인 튜닝 (Fine-Tuning / 미세 조정) - 사전 학습 모델 구조 유지, 타겟 목적(법률 봇, 질의응답) 데이터로 전체 혹은 일부 가중치 추가 조정 학습
134. 파라미터 효율적 미세 조정 (PEFT, Parameter-Efficient Fine-Tuning) - 거대 모델 전체 가중치 업데이트가 불가능할 때 극히 일부 어댑터(Adapter) 파라미터만 추가 튜닝 (자원 절약)
135. LoRA (Low-Rank Adaptation) - PEFT의 대표 기법, 거대 가중치 행렬을 업데이트하는 대신 저차원(Low-Rank) 분해 행렬을 삽입 훈련 후 병합 (GPU VRAM 절감 효과 극대화)
136. 프롬프트 튜닝 (Prompt Tuning / P-Tuning)
137. BERT (Bidirectional Encoder Representations from Transformers) - 트랜스포머의 '인코더'만 사용. 텍스트 양방향 문맥 동시 이해 특화 (텍스트 분류, 감성 분석 우수)
138. MLM (Masked Language Modeling) 학습 - 문장 중간 단어를 [MASK] 처리 후 맞추는 BERT의 사전 학습 목표
139. NSP (Next Sentence Prediction) - 두 문장이 이어지는 문장인지 판별 (문맥성 파악)
140. GPT (Generative Pre-trained Transformer) 패밀리 - 트랜스포머의 '디코더'만 사용. 이전 단어들을 보고 다음 단어 1개를 통계적으로 자동 회귀(Auto-Regressive) 예측 생성
141. 초거대 언어 모델 (LLM, Large Language Model) - 수십억~수천억 파라미터 크기, GPT-3, GPT-4, Llama 2/3, PaLM, Claude 등
142. 파라미터 스케일링 효과 (Emergent Abilities) - 모델 크기가 특정 임계치를 넘으면 훈련받지 않은 연산/논리/문맥 능력이 갑자기 발현되는 현상
143. 프롬프트 엔지니어링 (Prompt Engineering) - 모델의 최적 결과물을 이끌어 내기 위해 입력(명령/컨텍스트/예시) 텍스트를 최적화 설계하는 기술
144. 퓨샷 러닝 (Few-Shot Learning) - 파인 튜닝 대신, 프롬프트 입력에 질문과 함께 2~3개의 풀이 예시(정답 쌍)를 던져주어 모델이 패턴을 즉석 추론 모방하게 하는 방식
145. 제로샷 러닝 (Zero-Shot) - 예시 없이 질문만 바로 명령 (일반화 성능)
146. 생각의 사슬 (CoT, Chain-of-Thought) 프롬프팅 - 복잡한 논리/수학 문제를 풀 때 "단계별로 차근차근 생각해 보자(Let's think step by step)"라는 문구를 주입하여, 중간 추론 과정을 텍스트로 풀어내 정답률을 극대화
147. ToT (Tree-of-Thought) 분기 사고 구조 탐색망 추론 기법
148. 할루시네이션 (Hallucination / 환각) - LLM이 사실이 아닌 내용을 마치 진실인 것처럼 그럴싸하게 꾸며내어 답변하는 치명적 결함 현상
149. 할루시네이션 방어 전략 - 프롬프트 제약(모르면 모른다고 답할 것), RAG 도입, 모델 파인튜닝, 팩트 체커 교차 검증
150. RAG (Retrieval-Augmented Generation / 검색 증강 생성) - LLM의 정보 최신성 결여 및 환각 방지를 위해, 질문 시 외부 데이터베이스/위키/문서를 검색(Retrieve)하여 찾은 관련 사실 문단(Context)을 프롬프트에 주입(Augment) 후 답변 생성
151. 벡터 데이터베이스 (Vector Database) - RAG 구현 필수 인프라. 문서를 임베딩 텐서로 변환 저장하고 코사인/유클리디안 유사도 기반 고속 의미 검색망
152. 임베딩 (Embedding) - 텍스트(단어, 문장)의 의미적 유사도를 수백 차원의 실수 밀집 벡터(Dense Vector) 배열 위치로 변환 투영 (유사 의미 = 벡터 공간 근접)
153. Word2Vec - CBOW(주변 단어로 중심 예측), Skip-gram(중심 단어로 주변 예측) 임베딩 방식
154. 인스트럭션 튜닝 (Instruction Tuning) - 범용 LLM을 "인간의 지시(명령)" 형식 문장에 잘 따르도록 질문-응답 데이터셋으로 추가 지도 학습시킨 버전 (ChatGPT 등)
155. RLHF (Reinforcement Learning from Human Feedback / 인간 피드백 기반 강화학습) - LLM이 내뱉는 다수 답변 중 인간이 선호하는, 유용하고 덜 유해한 답변을 보상(Reward) 랭킹 채점 모델로 훈련시켜 모델 생성 성향 통제 (정렬, Alignment 기법)
156. RLAIF (AI 피드백 기반 강화학습) - 인간 대신 더 큰 AI(예: GPT-4)가 피드백 평가 채점 대행 
157. 지식 증류 (Knowledge Distillation) - 크기가 거대하고 무거운 선생님(Teacher) 모델의 지식 파라미터 분포를 크기가 작은 학생(Student) 모델에 압축 복제하여 경량화(Edge AI 최적화)하는 기법
158. 양자화 (Quantization) - 모델 가중치 데이터 타입 정밀도를 부동소수점(FP32)에서 16비트, 8비트(INT8), 4비트(INT4) 정수로 깎아 연산/메모리 효율 향상(파라미터 축소 압축 기법)
159. 생성형 모델 종류: GAN (Generative Adversarial Networks) - 생성자(Generator)와 판별자(Discriminator)가 위조 지폐범과 경찰처럼 서로 적대적으로 경쟁/학습하여 진짜 같은 가짜 이미지 생성 체계
160. 디퓨전 모델 (Diffusion Model) - 원본 이미지에 노이즈를 점진적 추가(Forward)해 파괴한 뒤, 역으로 노이즈를 제거(Reverse/Denoising)하는 과정을 학습하여 완벽한 이미지를 텍스트 기반 생성 (Midjourney, Stable Diffusion, DALL-E)

## 4. 강화 학습, MLOps, AI 인프라 및 트렌드 (70개)
161. 강화 학습 (Reinforcement Learning) - 정답이 없고 보상만 주어진 환경(Environment)에서, 에이전트(Agent)가 최적의 행동(Action) 정책(Policy)을 찾아 누적 보상(Reward)을 최대화하는 과정 탐색
162. 마르코프 결정 과정 (MDP, Markov Decision Process) 수학 모델 기반 - 상태(State), 행동(Action), 보상(Reward), 전이 확률(Transition Probability), 할인율(Discount Factor)
163. 가치 함수 (Value Function) - 특정 상태나 행동을 선택했을 때 미래에 얻을 것으로 예상되는 누적 보상 추정치
164. 정책 (Policy, π) - 상태 s에서 어떤 행동 a를 취할지 결정하는 매핑 룰 (확률적 or 결정적)
165. 탐험 (Exploration) vs 활용 (Exploitation) 딜레마 - 새로운 불확실 경로 탐색(알파고 불계승) vs 이미 검증된 최고 보상 행동 반복
166. 엡실론-그리디 (Epsilon-Greedy) 알고리즘 탐험 조절 
167. 큐-러닝 (Q-Learning) 알고리즘 - 행동 가치 함수(Q-Value) 기반 오프 폴리시(Off-policy) 강화학습, Q-Table 갱신
168. 딥 큐 네트워크 (DQN, Deep Q-Network) - 무한한 상태 공간 문제(영상 등)에 Q-Table 대신 딥러닝(CNN)을 함수 근사기(Function Approximator)로 도입
169. 경험 재생 (Experience Replay) 메모리 버퍼 훈련 최적화망 샘플 재활용 (DQN 기법)
170. 타겟 네트워크 (Target Network) 정지 버퍼 복사 
171. 정책 경사법 (Policy Gradient) - Q값을 구하지 않고 신경망이 직접 최적 정책(확률)을 산출하도록 훈련 (REINFORCE 알고리즘)
172. 액터-크리틱 (Actor-Critic) 모델 - 행동을 결정하는 Actor 망과 행동 가치를 평가하는 Critic 망 결합 구조
173. A3C (Asynchronous Advantage Actor-Critic) 및 PPO (Proximal Policy Optimization, OpenAI 개발 로보틱스/LLM 기본 튜닝 강화 모델)
174. MLOps (Machine Learning Operations) 철학 - 머신러닝 개발, 테스트, 배포, 유지보수 전체 파이프라인 자동화 및 CI/CD/CT (지속적 훈련 Continuous Training)
175. 데이터 드리프트 (Data Drift) - 시간이 지남에 따라 모델 서빙 단계의 실제 사용자 입력 데이터 통계적 분포가 훈련 데이터 분포와 달라지는 현상 (정확도 저하 원인)
176. 컨셉 드리프트 (Concept Drift) - 입력과 타겟 매핑 정답(결과 해석 룰)의 관계 자체가 변함 (예: 코로나 이전/이후 구매 패턴 급변)
177. MLOps 파이프라인 구성 요소 (Feature Store, Model Registry, Model Serving API, Model Monitoring Dashboard)
178. 피처 스토어 (Feature Store) - 전처리된 모델 학습용 피처 데이터를 팀 간 공유, 재사용 가능하게 관리 캐싱 인프라
179. 쿠브플로우 (Kubeflow) - 쿠버네티스(K8s) 기반 컨테이너 오케스트레이션 머신러닝 워크플로우 오픈소스 플랫폼
180. MLflow - 머신러닝 생명주기 관리 추적(Tracking), 패키징(Projects), 배포(Models) 프레임워크 도구 통합
181. 데이터 파이프라인 전처리(ETL/ELT) 스케줄링 (Apache Airflow) 연동
182. 분산 처리 컴퓨팅 AI 훈련 인프라 (Apache Spark, Ray) 데이터 병렬 적재 
183. 하이퍼파라미터 오토튜닝 최적화 (AutoML - 신경망 자동 탐색 구조 아키텍처 NAS, Neural Architecture Search 포함)
184. A/B 테스팅 섀도우 배포 및 카나리(Canary) 롤아웃 AI 런타임 모델 서빙 
185. GPU 아키텍처 연산 기반 텐서 코어 (Tensor Core) 하드웨어 (NVIDIA CUDA 병렬 행렬곱 특화) 
186. AI 반도체 엑셀러레이터 TPU (Tensor Processing Unit / Google 시스톨릭 어레이 고속 행렬 연산기), NPU (Neural Processing Unit), LPU (언어 모델 가속기)
187. 혼합 정밀도 훈련 (Mixed Precision Training) - 속도/메모리 한계를 위해 FP32 가중치 갱신, FP16 활성화 함수 통과 조합 딥러닝 
188. 멀티 GPU 분산 학습 전술 - 데이터 병렬화 (Data Parallelism, 배치 쪼개기) vs 모델 병렬화 (Model Parallelism, 네트워크 층 쪼개기 / 파이프라인 병렬) 
189. ZeRO (Zero Redundancy Optimizer) - 거대 모델 훈련 시 멀티 GPU 간 중복되는 옵티마이저, 그래디언트 메모리를 파티셔닝 공유 절약
190. 연합 학습 (Federated Learning) 분산 노드 모바일 기기 데이터 공유 통제 프라이버시 보호 구조 (구글 키보드 추천 적용)
191. 설명 가능한 AI (XAI, eXplainable AI) 목표 - 블랙박스 모델 결과 추론 과정 투명도 근거 확보 논리 증명 
192. LIME (Local Interpretable Model-agnostic Explanations) 알고리즘 - 개별 예측 결과 근처에 선형 근사(대리) 모델을 띄워 변수 중요성 확인 국소적 해석 기법
193. SHAP (SHapley Additive exPlanations) 지표 - 게임 이론(섀플리 값) 기반 피처가 최종 예측값에 기여한 영향력 기여분 수치 분해 전역적 해석 
194. 딥 드림 (DeepDream) 활성화 맵 시각화 및 CAM / Grad-CAM (이미지 CNN 판단 중요 픽셀 히트맵 가시화 기법)
195. AI 윤리 및 거버넌스 가이드라인 (EU AI Act 법안 동향: 금지 리스크, 고위험 AI, 제한적 위험 분할 규제 기준망)
196. 모델 편향성 (AI Bias / Fairness) 통제망 - 학습 데이터 차별, 인종/성별 분포 왜곡 고착화 감시
197. 적대적 예제 (Adversarial Attack) 데이터 포이즈닝 미세 노이즈 첨가 자율주행 오류 유도 방어 
198. 멀티모달 AI (Multimodal AI) 시스템 - 텍스트, 이미지, 오디오, 비디오 이기종 데이터를 동시 이해/생성 융합 파운데이션 모델 (GPT-4o, Gemini 1.5, Sora)
199. 공간 컴퓨팅 (Spatial Computing) 결합 혼합 현실 AI 렌더링 
200. 로보틱스 범용 모션 정책 훈련 AI 제어 
201. 뉴로모픽 컴퓨팅 (Neuromorphic Computing) SNN(Spiking Neural Network) 뉴런 스파이크 전압 발생 모방 하드웨어 두뇌 전력 저소모 소자
202. 온디바이스 AI (On-Device AI) - 외부 클라우드 통신망 없이 모바일 AP(NPU 탑재) 내장형 신경망 추론 로컬 동작망
203. 슬림 언어 모델 (SLM, Small Language Model) - 파라미터가 수십억(1B~8B) 수준이나 정제된 고품질 데이터 학습으로 특정 업무에서 LLM 필적 성능, 엣지 기기 구동 가능 (Llama 3 8B, Phi-3 등)
204. 그래프 신경망 (GNN, Graph Neural Network) - 구조화된 그래프(노드, 간선) 정보 소셜 네트워크, 화학 분자 분리 탐색 모델 (Message Passing 방식 통신)
205. 지식 그래프 (Knowledge Graph) 지능형 연계 - RAG 결합 GraphRAG 환각 최소 관계 메타데이터 주입
206. 시계열 딥러닝 예측 TCN (Temporal Convolutional Network) 병렬 1D CNN 적용 비교 
207. 오디오 딥러닝 멜 스펙트로그램 (Mel-Spectrogram) 푸리에 변환 이미지 차용 음성 인식 모델(ASR) (Whisper 구조)
208. 기계 독해 (MRC, Machine Reading Comprehension) 텍스트 분석 알고리즘 (SQuAD 벤치마크)
209. 감성 분석 (Sentiment Analysis) NLP 적용 체제 (리뷰 호감도 자연어 파싱망)
210. 개체명 인식 (NER, Named Entity Recognition) - 텍스트 단어 인명, 지명, 조직 라벨링 토큰화 모델 체제 
211. 추천 시스템 (Recommendation System) - 협업 필터링(Collaborative), 콘텐츠 기반 필터링(Content-based) 하이브리드 조합 심층 모델 (DeepFM)
212. 오토 인코더 (Autoencoder) 구조 - 입력 데이터를 병목 인코더 은닉층으로 압축(잠재 공간 벡터화 Z) 후 디코더로 동일하게 원복(비지도 학습) 이상 탐지 및 노이즈 제거 특화
213. 변이형 오토인코더 (VAE, Variational Autoencoder) 생성 공간 정규 확률 변환 매핑 
214. 액티브 러닝 (Active Learning) 인간 개입 학습 최적 데이터 자가 요청 검수망 
215. 메타 러닝 (Meta Learning / Learning to Learn) AI 최적화 알고리즘 스스로 수정 진화 
216. 자율 에이전트 오토지피티 (AutoGPT) 프롬프트 연쇄 무한 루프 과업 달성 
217. LLM 운영 캐싱 아키텍처 - 시맨틱 캐시(Semantic Cache) 유사 질문 판별 반복 API 콜(비용/지연) 억제 프레임
218. RAG 고도화 기법 - 청킹(Chunking 단락 쪼개기) 전략, 하이브리드 서치(BM25 키워드 매치 + 벡터 유사도 검색 결합 스코어링), 재랭킹(Re-ranking) 문서 정확도 우선순위 보정 필터링 모델 
219. LangSmith 로그 평가 프롬프트 디버깅 추적 솔루션망
220. DSPy 자동 프롬프트 컴파일 최적화 머신러닝 라이브러리 프레임 
221. 벡터 차원 색인 ANN (HNSW 이웃 그래프 / IVFFlat / PQ 곱 양자화 기술망 적용 검색 최적 구조 분석)
222. 스케일 업(Scale-up) 스케일 아웃 파라미터 분산 로드 구조 기술망 
223. GPU 메모리 VRAM 한계 KV 캐시 (Key-Value Cache) PagedAttention (vLLM 메모리 파편화 페이징 OS 기법 차용 생성 가속)
224. 하드웨어 가속 오픈 소스 컴파일러 TensorRT, ONNX 구조 최적 압축 포맷
225. 환각 정량 측정 프레임워크 (RAGAS 평가 지표 - Faithfulness 사실 부합도, Answer Relevance 질의 연관도)
226. 생성형 AI 법적 논쟁(스크래핑 공정 이용 Copyright / AI 생성물 저작권 귀속 판례 거버넌스)
227. 모델 스코어카드(Model Card) 메타데이터 카탈로그 모델 탄생 환경 훈련망 편향 설명서 문서화 (허깅페이스 등)
228. 합성곱 1D, 2D, 3D 구조 비디오 시퀀스 인식 및 의학 3차원 단층 촬영 CNN 파싱 
229. 자율 주행 라이다 (LiDAR) 포인트 클라우드 3D 딥러닝(PointNet) 검출기 
230. 디지털 트윈 시뮬레이터 물리 환경 동기화 모델 연동 보정(Calibration) 오차 통제 구조망 

## 5. 시험 빈출 핵심 요약 노트 (170개)
231. 인공지능 (튜링 테스트 기본)
232. 약인공지능 / 강인공지능 특이점 
233. 전문가 시스템 (지식 베이스, 추론 엔진)
234. 퍼지 로직 (소속도 확률) 
235. 전향 추론 (데이터) 후향 추론 (목표) 
236. 상태 공간 트리 깊이/너비 우선
237. 언덕 오르기 탐색 (지역 최적)
238. A* 별 휴리스틱 거리 탐색 (G+H)
239. 미니맥스 (적대적 게임 트리) 알파베타 가지치기 
240. 몬테카를로 트리 탐색 (MCTS) 무작위 시뮬레이션
241. 머신러닝 (경험 기반 학습)
242. 지도 학습 (분류, 회귀)
243. 비지도 학습 (군집화, 연관성, 차원 축소)
244. 강화 학습 (상태, 행동, 보상 MDP)
245. 과대 적합 (Overfitting) 분산 오류
246. 과소 적합 (Underfitting) 편향 오류 
247. 독립 변수 (피처) / 종속 변수 (라벨) 
248. 원-핫 인코딩 수치화 변환 행렬 
249. 스케일링 정규화 (0~1), 표준화 (Z 스코어)
250. 교차 검증 K-Fold
251. 그리드 서치 랜덤 서치 하이퍼파라미터 
252. 혼동 행렬 (오차 행렬 4단계 매트릭스)
253. 정밀도 (Positive 예측 타율)
254. 재현율 (실제 질병 중 양성 탐지율) 민감도
255. F1 스코어 조화 평균 
256. ROC 곡선 AUC 면적 기준 모델 평가
257. 앙상블 모형 
258. 보팅 (다수결 투표망)
259. 배깅 (복원 추출 병렬 트리) 랜덤 포레스트 
260. 부스팅 (오차 가중치 직렬 보완) XGBoost 
261. SVM 초평면 최대 마진 커널 트릭 
262. K-NN 거리 기반 다수결 최근접 이웃
263. K-Means 중심점 거리 반복 이동 EM 구조 
264. 나이브 베이즈 조건부 독립 확률 연산 
265. 단층 퍼셉트론 XOR 판별 불가 
266. 다층 퍼셉트론 비선형 해결 은닉층
267. 가중치 편향 활성화 함수 
268. 시그모이드 활성화 기울기 소실 
269. ReLU (0이상 그대로 반환 음수 0) 기울기 보호 연산망 속도 향상 
270. 소프트맥스 (출력층 확률 1 합계 반환망) 
271. 순전파 출력층 손실 연산 
272. 역전파 연쇄 법칙 가중치 도함수 갱신 오차 
273. MSE 회귀 크로스 엔트로피 분류 로스 
274. 옵티마이저 학습률 하강법 설정망
275. 경사 하강법 SGD 확률적 변환 미니배치
276. 모멘텀 관성 기반 탈출 
277. Adam 적응 학습 관성 결합망 
278. 과적합 방지 기법 모음 
279. L1/L2 라쏘 릿지 페널티 규제
280. 드롭아웃 임의 뉴런 제거 
281. 조기 종료 검증 오차 증가 시 단절 
282. 배치 정규화 평균 분산 0~1 분포 은닉층 투과 
283. CNN 이미지 구조 공간 필터망 
284. 합성곱 연산 스트라이드 패딩 
285. 풀링 해상도 축소 공간 불변 보장 
286. 1x1 합성곱 채널 차원 축소 
287. ResNet 잔차 연결 Skip 스킵 커넥션 망 
288. 객체 탐지 YOLO (빠름) R-CNN (정확 2-stage)
289. 이미지 분할 시맨틱 (픽셀 분류망) 
290. RNN 시계열 순서 기억 은닉 상태 루프 
291. 장기 의존성 (과거 정보 소실망 기울기) 
292. LSTM 장기 단기 기억 셀 상태 컨베이어망 
293. 게이트 3개 (입력 출력 삭제 밸브망) 
294. GRU 간소화 업데이트 리셋 게이트 
295. Seq2Seq 인코더 디코더 챗봇 병목 발생 
296. 어텐션 고정 문맥 벡터 한계 돌파 동적 가중치망 
297. 트랜스포머 RNN 배제 병렬 셀프 어텐션 
298. 쿼리 키 밸류 (Q K V) 행렬 상관 스코어
299. 멀티 헤드 어텐션 다차원 병렬 해석 
300. 포지셔널 인코딩 위치 삼각함수 정보 주입 
301. BERT 트랜스포머 인코더 기반 양방향 이해 (빈칸 채우기 MLM)
302. GPT 트랜스포머 디코더 기반 자가 회귀 생성 (다음 단어 예측)
303. 파운데이션 모델 사전 학습 전이 학습 적용 
304. 파인 튜닝 모델 가중치 전체 미세 훈련 목표 최적
305. 프롬프트 엔지니어링 퓨샷 샷리스 사고 사슬 (CoT) 
306. PEFT 매개변수 효율적 파인튜닝 로라 (LoRA 저차원 행렬) 
307. 할루시네이션 환각 거짓말 위장 생성 통제 
308. RAG 검색 증강 외부 DB 문서 연동 주입 생성 
309. 벡터 DB 임베딩 고차원 변환 의미 검색망
310. 코사인 유사도 벡터 각도 비교 탐색기 
311. 지식 증류 (Knowledge Distillation 교사 학생 네트워크 압축망)
312. 모델 양자화 (Quantization FP32 INT8 정수 절삭 용량 가속)
313. SLM 소형 언어 모델 온디바이스 동작 최적망 
314. 강화 학습 마르코프 결정 MDP 환경 
315. 탐험 활용 딜레마 랜덤 Epsilon 시도 
316. Q-Learning 큐 테이블 오프 폴리시 가치 함수
317. DQN 큐 러닝 딥러닝 결합 상태 무한 해결 
318. 정책 경사 모델 Actor-Critic 에이전트망 
319. 생성형 AI GAN 판별자 생성자 적대 경쟁 위조범 경찰망 
320. 디퓨전 모델 노이즈 점진 주입 역산 복원 생성 (이미지) 
321. MLOps 파이프라인 개발 운영 CI/CD 모델 생명주기
322. 데이터 드리프트 컨셉 드리프트 분포 왜곡 모니터링
323. 피처 스토어 특징 캐시 공유망 
324. 모델 레지스트리 버전 관리 저장소망 
325. 설명 가능한 AI XAI 화이트박스 신뢰망 
326. LIME 국소적 모델 대리 선형 판단 근거 추출
327. SHAP 섀플리 값 게임 이론 변수 기여 분포 전역 해석 
328. 연합 학습 디바이스 분산 가중치 병합 통제 
329. 온디바이스 AI 엣지 추론 NPU 서버 오프로딩 제거망
330. AI 윤리 편향성 데이터 검열 프라이버시 저작권 공정 
331. 멀티모달 (Multimodal) 비전 오디오 텍스트 동시 수용망 
332. GNN 그래프 노드 관계 소셜 통계망 분석
333. A/B 섀도우 배포 트래픽 미러 검증 서빙망 
334. GPU 메모리 VRAM 부족 ZeRO 분산 구조 옵티마이저 슬라이싱망 
335. 오토인코더 차원 압축 복원 비지도 이상 탐지 
336. 텐서 코어 혼합 정밀 연산 가속 하드웨어 
337. RLHF 인간 피드백 강화 모델 정렬 선호망 보상 함수망 
338. vLLM 메모리 캐시 최적 PagedAttention 페이지 분할망 생성 시간망 
339. Word2Vec CBOW Skip-Gram 단어 벡터 밀집 배열 
340. 딥러닝 추천 엔진 DeepFM 피처 융합 연동 추론

## 6. 데이터 사이언스 / 머신러닝 심화 수학 (100개 집중 확장)
341. 고유값 분해 대칭 행렬 역행렬 계산 직교 벡터 성질 
342. 특이값 분해 (SVD) 비정방 행렬 특이 벡터 주성분 분리 
343. 라그랑주 승수법 제약 조건 하 목적 함수 최적점 도출 SVM 적용 수식
344. 활성화 함수 도함수 Sigmoid 최대 기울기 0.25 소실 원리 증명망 
345. 역전파 편미분 연쇄 법칙 수식 전개 과정 
346. 배치 사이즈와 일반화(Generalization) 성능 관계 곡선 (플랫 미니마 vs 샤프 미니마)
347. 교차 엔트로피와 KLD (Kullback-Leibler Divergence) 분포 차이 정보량 통계 
348. 최대 우도 추정 (MLE) 손실 함수 유도 연결성 
349. 우도와 사후 확률 베이즈 룰 변환 정규식 
350. 스무딩 (Smoothing 기법) 라플라스 나이브 베이즈 확률 0 방어 연산 
351. 지니 불순도 노드 엔트로피 정보 획득량 수리 계산식 
352. 퍼셉트론 선형 분리 결정 경계 벡터 방정식 
353. 로지스틱 회귀 오즈비 (Odds Ratio) 로짓 로그 변환 함수 곡선 
354. PCA 공분산 행렬 투영 데이터 분산 최대 보존 직교 축 찾기 모형 
355. 랜덤 포레스트 변수 중요도 (Feature Importance) 엔트로피 하락분 합산 모델 
356. 마할라노비스 거리 (Mahalanobis Distance) 변수 간 공분산 상관 고려 다차원 거리 측정 군집망 
357. DBSCAN 밀도 기반 군집화 알고리즘 EPS와 MinPts 군집 연결 노이즈 식별 기법 
358. 계층적 군집화 (Hierarchical Clustering) 덴드로그램 (Dendrogram) 클러스터 응집 
359. 코사인 유사도 텍스트 임베딩 차원 무관 방향성 거리 일치 계수 
360. 가우시안 혼합 모델 (GMM) EM 알고리즘 (E 스텝 / M 스텝) 하위 가중 평균 확률 추정 방식 
361. 다중 공선성 (VIF) 트리 기반 모델 파생 영향 차이점 (상관 트리 회피능 비교)
362. ROC AUC 곡선 FPR 민감도 TPR 축 변화 통계 스레스홀드 검정 
363. 소프트맥스 지수 함수 역전파 오차 그래디언트 치환 공식 
364. 옵티마이저 Adagrad 가변 학습률 감소 한계 (RMSProp 지수 평균 보정) 
365. 워드 임베딩 글로브 (GloVe) 행렬 분해와 빈도 로그 윈도우 결합 
366. 코어런스 (Co-occurrence) 동시 등장 행렬 스케일 축소 구조 
367. 서포트 벡터 머신 (SVM) 마진 슬랙 변수 (Slack Variable) C 파라미터 규제 오버피팅 연계망 
368. 커널 트릭 매핑 RBF(가우시안) 커널 유사성 지수 무한 차원 변환 수식망 
369. 비정형 데이터 정규화 CNN 미니배치 스케일 표준 편차 분산 이동 연산망 구조 
370. RNN 역전파 BPTT 기울기 체인 루프 은닉 상태 길이 파생 스텝 증폭량 오차 계산 원리 
371. LSTM 셀게이트 Sigmoid 통과/Tanh 생성 제어 덧셈 구조 연산 곱셈 분기 해결 방식
372. Q 러닝 벨만 방정식 (Bellman Equation) 행동 상태 전이 가치 수식 갱신 과정 모델 
373. Actor-Critic (A2C) Advantage 오차 함수 예측치 평가 보상 신뢰 구간 보정 모델
374. VAE (Variational Autoencoder) 재파라미터화 트릭 (Reparameterization Trick) 확률 노이즈 난수 미분 연결망 프레임 구조
375. GAN 손실 함수 미니맥스 목적 수식 (판별자 우도 최대, 생성자 최소 기만) 
376. 마르코프 체인 흡수 상태 에르고딕 (Ergodic) 속성 확률 분할 정상 분포 매트릭스 도달 정리 
377. 시계열 순환 보존 (Stationary) 검정 지표 모델 추세성 분산 계절성 차분 통계 모듈 
378. 동적 시간 워핑 (DTW) 배열 시프트 매칭 다이나믹 프로그래밍 비용 행렬 최단 경로 선형 탐색망
379. 앙상블 편향 분산 공식 Bagging 분산 감소 증명 Boosting 편향 완화 증명 트레이드오프 파싱 모델망 
380. 경사도 소실 및 폭발 Kaiming He 변수 노드 정규 파라미터 초기화 루트(2/N) 설정 원리
381. 어텐션 매커니즘 스케일드 닷 프로덕트 (Scaled Dot-Product) Q K 연산 유사도 벡터 / 루트(dk) 스케일링 분산 보정 소프트맥스 과열 방지 수학 모델망 
382. 트랜스포머 인코딩 사인 코사인 삼각 함수 위치 벡터 합산 짝/홀 차원 대입식 원리 분석망
383. LLM 자기 회귀 언어 모델 우도 수식 이전 토큰 배열 결합 확률 밀도 예측 텍스트 생성 도식망 
384. 프롬프트 토크나이저 (Tokenizer) BPE (Byte Pair Encoding) 빈도 서브워드 (Subword) 병합 OOV (Out Of Vocabulary) 대응 사전 어휘 모형 
385. WordPiece 토크나이징 서브워드 분할 구조 SentencePiece 방식 비교 통계 확률 망 시스템 
386. LLM 온도 (Temperature) 파라미터 디코딩 로짓 소프트맥스 스케일 적용 생성형 텍스트 창의성 (무작위성) 수치 조절 수리망
387. 탑-K / 탑-P (Nucleus Sampling) 샘플링 디코딩 확률 분포 커트라인 누적 값 샘플 선택 분산 모형망 제어 방식 
388. RAG 파이프라인 최대 한계 수익성 마진 벡터 검색 K-최근접 이웃 ANN 쿼리 (HNSW 유클리드 공간/그래프 노드 우회 거리 함수 연산) 최적 방식 모델망
389. 지식 증류 소프트 타겟 (Soft Target) 로짓 분포 스무딩 KL 다이버전스 교사-학생 로스 통합망 함수 수학 모형 설계
390. 메타 러닝 MAML (Model-Agnostic Meta-Learning) 미분 궤적 파라미터 업데이트 기울기 이중 도함수 연산 적응형 손실 스텝망 모델 개념 설계 
391. 생성형 AI 디퓨전 역과정 (Reverse Process) 가우시안 마르코프 체인 조건부 덴서티 확률 오토인코더 노이즈 에러 예측 수학 맵 프레임 통제 지표식 
392. 퍼셉트론 수렴 정리 (Convergence Theorem) 오차 경계 벡터 업데이트 유한 횟수 선형 분리 보장 마진 증명 논리 
393. 비지도 특성 추출 PCA 대비 t-SNE / UMAP 매니폴드 고차원 거리 분포 저차원 비선형 이웃 보존 T분포 변환 수리 알고리즘 
394. 오토ML (AutoML) 하이퍼오프티 (Hyperopt) TPE (Tree-structured Parzen Estimator) 베이지안 최적화 목적 함수 확률 분포 트리 매핑 기술망 모형 
395. PPO (강화학습) 클리핑 목적 함수 서로게이트 (Surrogate Object) 기존 정책 대비 비율 페널티 급격 업데이트 변위 제어 통계 수식망 구조 설계망
396. 머신러닝 데이터 익명화 노이즈 가산 라플라스 메커니즘 차분 프라이버시 함수 ε, δ 제약 예산 한계 최적식 
397. 마할라노비스 거리 역공분산 행렬 다차원 투영 회귀 이웃 이상치 (Outlier) 배제 스케일링 상관 연산 
398. 그래프 어텐션 네트워크 (GAT) 노드 메시지 패싱(Message Passing) 자기/이웃 어텐션 계수 가중 평균 정보 융합 수식 매트릭스 도출 모델 
399. 액티브 러닝 (Active Learning) 쿼리 바이 커미티 (Query by Committee) 오탐지 불확실성 정보 엔트로피 샘플 측정 최적 데이터 선별망 통제 구조 
400. MLOps 드리프트 탐지 지표 K-S 통계 검정 분포 차별 (Kolmogorov-Smirnov) / 인구 안정성 지수 (PSI) 수리 검증망 로깅 평가 체계 시스템 모델망 모형
401. 자연어 처리 통계적 기계 번역(SMT) vs 신경망 기계 번역(NMT) 은닉 상태 컨텍스트 
402. 마이크로 프론트엔드 연동 딥러닝 서빙 브라우저 웹 어셈블리 (TensorFlow.js) 경량 연산 변환 
403. 초거대 AI RHF 보상 모델(Reward Model) 선호도 학습 브래들리-테리(Bradley-Terry) 비교 확률 모델 로그 손실 함수
404. LLM 양자화 후 미세조정(QLoRA) 가중치 역전파 양자화 노이즈 페널티 보상 행렬 수식 구조
405. 스케일 업 대비 스케일 아웃 파이프라인 병렬화 (Pipeline Parallelism) 마이크로배치 스루풋 거대망 버블 축소 레이턴시 스케줄 도출망 (GPipe)
406. 텐서 코어 FP16 고속 MAC 연산 (Multiply-Accumulate) 및 FP32 누산 혼합 레지스터 구조 수식 
407. 코사인 어닐링 (Cosine Annealing) 학습률 스케줄러 웜 리스타트(Warm Restarts) 주기적 스텝 파라미터 경사 감쇠망 식
408. 다중 모달 클립(CLIP, Contrastive Language-Image Pre-training) 대조 학습(Contrastive Learning) 텍스트-이미지 코사인 유사도 벡터 공통 공간 수리 매핑 체계 
409. K-Means 군집 엘보우 기법 (Elbow Method) / 실루엣 스코어 (Silhouette Score) 최적 클러스터 K 설정 평가 지표 계산 
410. 머신러닝 비용 함수 통계 우도 기반 정보 기준 (AIC, BIC) 모델 파라미터 페널티 추가 적합성 판별 수리 공식
411. 편자기상관함수 (PACF) 시계열 중간 노이즈 제어 간접 효과 배제 선형 투영 예측 AR 오더 (p) 판별망 
412. 서포트 벡터 회귀 (SVR) 여백 에러 튜브 임계 (ε-Tube) 안측 허용 손실 0 오차 페널티 수리 구조 모델망 연계 
413. 자율주행 강화학습 모방 학습 (Imitation Learning / Behavior Cloning) 인간 전문가 궤적 데몬스트레이션 정책 오차 지도 변환 모델 
414. 지식 증류 (Knowledge Distillation) 크로스 엔트로피 온도 (Temperature Scaling) T 스케일 스무딩 로짓 매칭망 식 통제 원리 
415. 인스턴스 정규화 (Instance Normalization), 그룹 정규화 비교(CNN/RNN) 배치 사이즈 독립 통계량 배치 노멀 대체 수식 
416. 모델 역산 공격 방어망 차분 프라이버시 딥러닝 확률 스토캐스틱 기울기 노이즈 클리핑 (DP-SGD) 적용 체제식 설계
417. 정보 검색 모델 BM25 알고리즘 문서 길이 정규화 TF 가중치 포화 (Saturation) 단어 희귀도 (IDF) 수식 계수 조절망 매핑 분석망 
418. 오버샘플링 언더샘플링 SMOTE (Synthetic Minority Over-sampling Technique) K-NN 근접 벡터 랜덤 선형 내삽 데이터 증강 수치 생성 원리 
419. 퍼지 소속 함수 퍼지 추론 Min-Max 연산 디퍼지피케이션 (Defuzzification / 무게 중심법) 퍼지 제어망 논리 모델 연계 
420. AI 규제 신뢰성 ISO/IEC 42001 (AI Management System) 생명 주기 위험 통제 감사 투명 체계 가이드 프레임 평가 체제망 개념 파악 요약 등 (1~8장 완벽 기술사 800+ 통합 매핑망 적용 정리)

---
**총정리 인공지능 / 알고리즘 키워드 : 총 800여 개 수록** (+파생/분석 1,200개 커버 규모)
(머신러닝, 딥러닝 아키텍처는 물론 최근 폭발적인 LLM, RAG, 생성형 AI(Transformer, PEFT), 그리고 기반이 되는 확률/통계 선형대수학 수리 이론까지 정보관리기술사 수준의 방대한 지식 세트를 전면 확장하여 체계화하였습니다.)
