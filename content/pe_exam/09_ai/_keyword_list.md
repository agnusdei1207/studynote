+++
title = "09. 인공지능 키워드 목록"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 인공지능 (AI) 키워드 목록

기술사 시험 대비 인공지능 전 영역 핵심 키워드 (2024~2025 최신 동향 포함)

---

## 1. AI 기초 (ai_foundations) — 34개

### 기계학습 기초
1. 지도학습 (Supervised Learning)
2. 비지도학습 (Unsupervised Learning)
3. 준지도학습 (Semi-supervised Learning)
4. 자기지도학습 (Self-supervised Learning)
5. 강화학습 (Reinforcement Learning)
6. 전이학습 (Transfer Learning)
7. 메타학습 (Meta-learning / Few-shot)
8. 연합학습 (Federated Learning)
9. 능동학습 (Active Learning)
10. 온라인학습 (Online Learning)

### 모델 학습
11. 경사하강법 (Gradient Descent) / SGD / Adam / AdaGrad / RMSProp
12. 역전파 (Backpropagation)
13. 과적합 / 과소적합 (Overfitting / Underfitting)
14. 정규화 (Regularization): L1/L2/Dropout/BatchNorm
15. 교차검증 (Cross-Validation): k-fold, LOOCV
16. 하이퍼파라미터 튜닝 (HPO)
17. 앙상블 학습 (Ensemble: Bagging/Boosting/Stacking)
18. 신경망 아키텍처 탐색 (NAS)

### 평가
19. 정밀도/재현율/F1 (Precision/Recall/F1)
20. ROC-AUC, PR-AUC
21. Confusion Matrix
22. BLEU / ROUGE / Perplexity (NLP 평가)
23. FID (Fréchet Inception Distance, 이미지 생성 평가)

### 특징 공학
24. 특성 선택 (Feature Selection)
25. 특성 추출 (Feature Extraction / PCA / t-SNE / UMAP)
26. 데이터 증강 (Data Augmentation)
27. 불균형 데이터 처리 (SMOTE, 언더샘플링)
28. 차원의 저주 (Curse of Dimensionality)

### 수학 기초
29. 확률론 / 베이즈 정리
30. 정보이론 (엔트로피 / KL 다이버전스)
31. 선형대수 (행렬 연산, SVD, 고유값)
32. 최적화 이론 (볼록함수, 라그랑주 승수법)
33. 몬테카를로 방법 (Monte Carlo)
34. 마르코프 체인 (Markov Chain)
35. 기계 망각 (Machine Unlearning)
36. 합성 데이터 생성 (Synthetic Data Generation)

---

## 2. 딥러닝 (deep_learning) — 32개

### 기본 구조
1. 퍼셉트론 (Perceptron)
2. 다층 퍼셉트론 (MLP / Feedforward)
3. 활성화 함수 (ReLU / GELU / Swish / SiLU)
4. 배치 정규화 (Batch Normalization)
5. 레이어 정규화 (Layer Normalization)
6. Residual Connection / Skip Connection
7. Dropout / DropBlock

### 합성곱 신경망 (CNN)
8. CNN (Convolutional Neural Network)
9. ResNet / VGG / EfficientNet / ConvNeXt
10. 객체 탐지: YOLO / Faster R-CNN / DETR
11. 이미지 분할: U-Net / SAM (Segment Anything)
12. Vision Transformer (ViT)

### 순환 신경망
13. RNN (Recurrent Neural Network)
14. LSTM (Long Short-Term Memory)
15. GRU (Gated Recurrent Unit)
16. Bidirectional RNN/LSTM

### Transformer 계열
17. Attention Mechanism (Self-Attention, Cross-Attention)
18. Multi-Head Attention
19. Transformer (Encoder-Decoder)
20. BERT (Bidirectional Encoder Representations)
21. GPT (Generative Pre-trained Transformer)
22. T5 / BART / FLAN-T5
23. Mamba (State Space Model, SSM)
24. Mixture of Experts (MoE)

### 생성 모델
25. GAN (Generative Adversarial Network)
26. VAE (Variational Autoencoder)
27. Diffusion Model (DDPM / DDIM)
28. Flow-based Model (Normalizing Flow)
29. Score Matching / Energy-based Model

### 그래프/특수목적
30. GNN (Graph Neural Network) / GCN / GraphSAGE / GAT
31. Capsule Network
32. Neural ODE / Physics-informed Neural Network
33. JEPA (Joint-Embedding Predictive Architecture)
34. BitNet b1.58 (1-bit LLM)
35. Test-Time Compute (추론 시 연산 확장)

---

## 3. 생성 AI (generative_ai) — 28개

### LLM 기초
1. LLM (Large Language Model) — GPT-4o, Claude, Gemini, LLaMA
2. Foundation Model (기반 모델)
3. 사전훈련 (Pre-training) — Autoregressive / MLM
4. 미세조정 (Fine-tuning)
5. PEFT (Parameter-Efficient Fine-Tuning)
6. LoRA / QLoRA / Adapter Tuning
7. Instruction Tuning
8. RLHF (Reinforcement Learning from Human Feedback)
9. DPO (Direct Preference Optimization)
10. Constitutional AI

### Prompting 기법
11. 프롬프트 엔지니어링 (Prompt Engineering)
12. Zero-shot / Few-shot / One-shot Prompting
13. Chain-of-Thought (CoT) Prompting
14. Tree-of-Thought (ToT) / ReAct
15. Self-consistency Decoding
16. System Prompt / Role Prompting

### RAG & 검색
17. RAG (Retrieval-Augmented Generation)
18. 벡터 임베딩 (Vector Embedding)
19. 벡터 데이터베이스 (Vector DB: Pinecone/Weaviate/Chroma)
20. Semantic Search / Hybrid Search
21. GraphRAG
22. Agentic RAG / Corrective RAG

### AI 에이전트
23. AI Agent (자율 에이전트)
24. ReAct (Reasoning + Acting)
25. AutoGPT / ChatGPT Plugins
26. LangChain / LlamaIndex Framework
27. Multi-Agent System (MAS)
28. Tool Use / Function Calling

### 멀티모달 & 에이전트 심화
29. 멀티모달 AI (MultiModal: CLIP, Flamingo, GPT-4V, Gemini)
30. Text-to-Image (DALL-E 3, Stable Diffusion, Midjourney)
31. Text-to-Video (Sora, Runway, Kling)
32. Text-to-Speech / Speech-to-Text (Whisper)
33. Code Generation (GitHub Copilot, Cursor, Claude Code)
34. Agentic Workflow (에이전틱 워크플로우)
35. Reasoning Model (OpenAI o1, DeepSeek-R1)
36. Compound AI System

---

## 4. MLOps — 22개

1. MLOps (Machine Learning Operations)
2. ML 파이프라인 (ML Pipeline: Kubeflow, Airflow, Metaflow)
3. Feature Store (피처 스토어: Feast, Tecton)
4. 데이터 버전 관리 (DVC, Delta Lake, LakeFS)
5. 모델 레지스트리 (Model Registry: MLflow, Weights & Biases)
6. 실험 추적 (Experiment Tracking: MLflow, W&B, Neptune)
7. 데이터 드리프트 감지 (Data Drift Detection)
8. 모델 드리프트 / 개념 드리프트 (Concept Drift)
9. 모델 모니터링 (Model Monitoring)
10. 모델 서빙 (Model Serving: TorchServe, TFServing, Triton, vLLM)
11. A/B Testing / 챔피언-챌린저
12. Shadow Deployment / Canary Deployment
13. CI/CD for ML (Continuous Training, CT)
14. LLMOps (LLM Operations)
15. 컨텍스트 윈도우 관리 (Context Window)
16. 토큰 최적화 (Token Optimization)
17. 프롬프트 버전 관리 (Prompt Versioning)
18. 가드레일 (Guardrails / LLM Safety)
19. 레이턴시 최적화 (Latency: TensorRT-LLM, speculative decoding)
20. 엣지 ML (Edge ML: TFLite, ONNX, CoreML)
21. 홈로모르픽 암호화 (Privacy in ML)
22. 차등 프라이버시 (Differential Privacy)

---

## 5. AI 응용 (ai_applications) — 24개

### 컴퓨터 비전
1. 이미지 분류 (Image Classification)
2. 객체 탐지 (Object Detection)
3. 이미지 분할 (Segmentation: Semantic/Instance/Panoptic)
4. 포즈 추정 (Pose Estimation)
5. Optical Flow / Video Understanding
6. 3D Computer Vision (NeRF, Point Cloud, 3D Gaussian Splatting)
7. SAM (Segment Anything Model)
8. OCR / 문서 이해 (Document AI)

### NLP
9. 자연어 처리 (NLP) 전처리: 토크나이제이션, 임베딩
10. 감성 분석 (Sentiment Analysis)
11. 기계 번역 (Neural Machine Translation)
12. 질의응답 (QA) / 독해 이해 (Reading Comprehension)
13. 요약 (Summarization: Extractive/Abstractive)
14. 정보 추출 (NER, Relation Extraction)
15. 대화 시스템 (Dialogue System / Chatbot)

### 특수 응용
16. 자율주행 (Autonomous Driving): L1~L5, CARLA
17. 로보틱스 AI (Robot Learning, Manipulation)
18. AI 헬스케어 (Medical AI: 영상진단, Drug Discovery)
19. AI 금융 (FinAI: 이상거래탐지, Robo-advisor)
20. 추천시스템 (Recommender System: CF, CB, DNN 기반)
21. 음성인식/합성 (ASR/TTS: Whisper, VITS)
22. AI 코드 생성 (Code LLM)
23. 과학 AI (AlphaFold, AlphaGeometry, AI Scientist)
24. 디지털 트윈 + AI (AI Digital Twin)

---

## 6. AI 거버넌스 (ai_governance) — 18개

1. AI 윤리 (AI Ethics)
2. 설명 가능한 AI (XAI: Explainable AI)
3. LIME / SHAP 해석 기법
4. AI 편향성 (AI Bias / Fairness)
5. 알고리즘 감사 (Algorithm Audit)
6. 투명성 (Transparency / Accountability)
7. AI 안전성 (AI Safety)
8. AI 정렬 문제 (AI Alignment)
9. 환각 (Hallucination)
10. AI 규제 (AI Regulation)
11. EU AI Act (EU AI법, 2024)
12. NIST AI RMF (AI Risk Management Framework)
13. 저작권 & AI (Copyright Issues)
14. 딥페이크 (Deepfake Detection)
15. Responsible AI
16. AI 거버넌스 프레임워크 (OECD AI Principles)
17. 워터마킹 (AI Watermarking, C2PA)
18. AI 탄소발자국 (AI Carbon Footprint / Green AI)
19. AI TRiSM (Trust, Risk and Security Management)
20. Digital Provenance (디지털 출처/이력 관리)
21. 소버린 AI (Sovereign AI)

---

## 7. AI 인프라 (ai_infrastructure) — 20개

### 하드웨어
1. GPU (Graphics Processing Unit: NVIDIA H100/H200, A100)
2. TPU (Tensor Processing Unit: Google)
3. NPU (Neural Processing Unit: Apple, Qualcomm)
4. AI 가속기 (FPGA, ASIC, Cerebras, Groq)
5. HBM (High Bandwidth Memory: HBM3, HBM3e)
6. 뉴로모픽 칩 (Neuromorphic: Intel Loihi, IBM TrueNorth)
7. NVLink / NVSwitch (GPU 상호연결)
8. InfiniBand (고속 클러스터 네트워크)

### 분산 학습
9. 데이터 병렬화 (Data Parallelism)
10. 모델 병렬화 (Model Parallelism: Tensor/Pipeline)
11. 분산 학습 프레임워크 (Megatron-LM, DeepSpeed, PyTorch FSDP)
12. NCCL (NVIDIA Collective Communications Library)
13. 그래디언트 압축 (Gradient Compression)

### 모델 최적화
14. 모델 압축 (Knowledge Distillation / Pruning / Quantization)
15. 추론 최적화 (Inference Optimization: TensorRT, ONNX Runtime)
16. KV Cache (Key-Value Cache for LLM)
17. 양자화 (Quantization: INT8/INT4/FP8)
18. 지식 증류 (Knowledge Distillation)
19. 연속 배치 (Continuous Batching: vLLM)
20. Speculative Decoding
21. AI Supercomputing Platform (GPU/NPU/ASIC 통합)
22. Physical AI (피지컬 AI / 로보틱스 지능)

---

## 8. 최신 AI 동향 (2025~2026) — 특별 키워드

1. OpenAI o1/o3 (System 2 Thinking, CoT 추론)
2. Agentic AI & Workflow Automation (ReAct 고도화)
3. Sovereign AI (자국 중심 인프라 및 모델 전략)
4. BitNet b1.58 & 고효율 추론 아키텍처
5. Multi-Agent System (MAS) 및 에이전트 협업
6. Machine Unlearning (저작권/개인정보 데이터 삭제)
7. Physical AI (피지컬 AI, 구현된 AI)
8. Compound AI System (단일 모델에서 시스템 중심으로)
9. GraphRAG & 하이브리드 검색 최적화
10. AI TRiSM 기반 거버넌스 강화
11. Test-Time Compute 확장 전략
12. 도메인 특화 모델 (DSLM: Domain-Specific Language Models)
13. AI 네이티브 소프트웨어 개발 (Cursor, Claude Code)
14. 컨피덴셜 컴퓨팅 (Confidential Computing) 기반 보안
15. 디지털 출처 및 진위 확인 (Digital Provenance)
16. 합성 데이터 기반 학습 데이터 한계 극복
17. 효율적 MoE (Mixture of Experts) 전략
18. Long Context Window (2M+ 토큰)를 활용한 지식 처리
19. EU AI Act 본격 시행 대응 및 AI 규제 준수
20. On-device AI/Edge LLM용 NPU 하드웨어 가속
