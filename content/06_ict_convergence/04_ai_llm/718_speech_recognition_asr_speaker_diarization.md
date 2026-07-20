---
title: "Speech Recognition ASR Speaker Diarization"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 718
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 음성 AI의 3대 축인 **ASR(음성->텍스트, Whisper/Conformer 기반 End-to-End)**, **Speaker Diarization("누가 언제 말했는가", x-vector/NeMo MSDD/EEND)**, **TTS(텍스트->음성, FastSpeech 2/VITS/HiFi-GAN)**가 결합되어 다화자·다국어·실시간 음성 인터페이스를 완성하는 통합 음성 인지·생성 파이프라인이다.
> 2. **가치**: 회의록 자동 작성(생산성 60~80% 향상), 콜센터 음성 분석(불만 분류 정확도 90% 이상), 시각장애인 접근성, 24시간 AI 상담원 운영 시 인건비 대비 약 70% 절감, 보이스피싱·딥보이스 탐지 등 보안 분야 확장.
> 3. **판단 포인트**: **WER/CER/DER/MOS** 4대 지표 간 트레이드오프, **실시간성(Streaming vs Offline)**, **온프레미스(데이터 주권·금융규제) vs 클라우드 API**, **End-to-End 단일 모델 vs 모듈형 파이프라인**, 화자 임베딩 학습 데이터의 **편향(Bias)** 및 **개인정보 비식별화** 처리 기준(KISA 가이드라인, EU AI Act 6조).

---

## Ⅰ. 개요 및 필요성

기존 음성 인식(ASR) 시스템은 1950년대 AT&T의 Audrey부터 HMM-GMM 기반 Kaldi까지 70여 년간 발전해 왔으나, 2016년 이후 End-to-End(CTC, Attention, RNN-T) 패러다임으로 패러다임 전환이 일어났다. 특히 2020년 OpenAI의 wav2vec 2.0, 2022년 Whisper, Google USM(Universal Speech Model) 등 Self-Supervised + 대규모 다국어 데이터 기반 모델이 등장하며, WER 5% 미만(클린 환경, 영어 기준) 수준에 도달했다.

그러나 **단일 화자 가정(Single-Speaker Assumption)** 위에서 학습된 ASR은 다화자 회의·상담 음성에서 "누가 말했는가"를 구분하지 못한다. 이 한계를 보완하는 것이 **화자 분리(Speaker Diarization, "Who Spoke When")** 기술이며, 회의록 자동화, 법정 녹취, 의료 다학제 회의 등에서 핵심 요구사항으로 부상했다.

**음성 합성(TTS)**은 ASR의 역방향으로, 단순 음성 안내를 넘어 **화자 클로닝(Speaker Cloning), 다국어 음성 번역(Speech-to-Speech Translation), 감정 표현(Emotional TTS)** 으로 진화하고 있다. 2023년 VALL-E·NaturalSpeech 3, 2024년 GPT-4o Realtime처럼 **In-Context Learning 기반 Zero-Shot 음성 합성**이 가능해지면서, 3초의 참조 음성만으로 임의 화자의 음색·운율을 복제할 수 있게 되었다.

이 세 기술은 단독으로도 가치가 있으나, **ASR + Diarization + TTS를 통합한 Full-Duplex 음성 인터페이스**(예: AI 콜센터, 회의 비서, 음성 비서)에서 시너지를 극대화한다. 실무 관점에서는 이 통합 아키텍처의 **모듈 결합도(Coupling), 데이터 흐름(Data Pipeline), 거버넌스(보안·윤리)** 설계가 핵심 논점이다.

```text
[ 3대 음성 기술 통합 아키텍처 - Full-Duplex Conversational AI ]

   +--------------- 입력 음성(Inbound Audio, 16kHz PCM) ---------------+
   |                                                                     |
   v                                                                     v
+----------------+  +------------------+  +--------------------------+
|  VAD Module    |-->| Speaker Embedding |-->| Speaker Clustering       |
| (WebRTC VAD /  |  | (x-vector,        |  | (Spectral / VBx /       |
|  Silero VAD)   |  |  ECAPA-TDNN)      |  |  Agglomerative)          |
+----------------+  +------------------+  +------------+-------------+
        |                     |                          |
        v                     v                          v
+----------------------------------------------------------------------+
|        [ End-to-End ASR Engine (Whisper / Conformer / RNN-T) ]       |
|                                                                      |
|  +----------+    +-------------+    +--------------+    +----------+ |
|  | Encoder  |---->|   Decoder   |---->|  LM Shallow  |---->|  Text    | |
|  |(80-d Mel)|    |(Attention / |    |  Fusion      |    |  Output  | |
|  |          |    | RNN-T)      |    | (Optional)   |    |          | |
|  +----------+    +-------------+    +--------------+    +----------+ |
+-----------------------------+----------------------------------------+
                              |
                              v
+----------------------------------------------------------------------+
|   [ Diarization-Aligned Transcription:  "발화자#1 (00:01:23)]"  ]    |
|   [                   "발화자#2 (00:01:45)]"                       ]   |
+-----------------------------+----------------------------------------+
                              |
                              v
                  +----------------------+
                  |  NLU / Intent / RAG  | (대화이해·검색증강)
                  +----------+-----------+
                             v
+----------------------------------------------------------------------+
|       [ TTS Engine (FastSpeech 2 + HiFi-GAN / VITS / VALL-E) ]      |
|                                                                      |
|   Text --> Text Normalization --> Acoustic Model --> Vocoder --> PCM    |
|           (숫자·약어·SSML)   (Mel-Spectrogram)  (Waveform)            |
+----------------------------------------------------------------------+
                              |
                              v
                  [ 출력 음성(Outbound Audio) ]
```

기존 파이프라인은 각 단계가 독립적인 모델로 결합되어 있었으나(HMM-GMM ASR + i-vector Clustering + HTS Statistical Parametric TTS), 2020년 이후는 **단일 Transformer Encoder 공유**나 **Multi-Task Learning**으로 통합 추론이 가능해져 **지연시간(Latency)을 30% 이상 단축**했다.

- **📢 섹션 요약 비유**: ASR은 **받아쓰기 비서**, 화자분리는 **회의실 좌석 배치도**, TTS는 **원하는 목소리 대리인**입니다. 세 비서가 한 팀이 되어야 "30명이 동시에 떠드는 회의실에서도 누가 무엇을 말했는지 정리하고, 다시 음성으로 답장"하는 것이 가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ASR (Automatic Speech Recognition) — 음성 -> 텍스트

**핵심 구성**: 음향 모델(AM) + 언어 모델(LM) + 발음 사전(Lexicon) + 디코더. End-to-End 모델은 이 4단을 단일 신경망으로 통합한다.

```text
[ ASR End-to-End Architecture - Whisper / Conformer-Transducer 예시 ]

   Input Audio (16kHz, 30s chunk)
            |
            v
   +---------------------+
   |  Log-Mel Spectrogram|   <- 80-channel, 25ms window, 10ms hop
   |  (T x 80 matrix)    |
   +----------+----------+
              |
              v
   +--------------------------------------+
   |       Encoder (Conformer Block)      |
   |                                      |
   |   x ---> Conv Module (1D depthwise) --+
   |      |                               |
   |      +---> Multi-Head Self-Attention -+
   |              |                       |
   |              +---> Feed-Forward (Macaron) --> LayerNorm
   |   (반복 N=12~32 layers, d_model=512)
   +----------+---------------------------+
              |
              v
   +--------------------------------------+
   |  Decoder (Transformer / RNN-T Joint) |
   |      (Cross-Attention over encoder)  |
   +----------+---------------------------+
              |
              v
        Token Sequence (BPE/SentencePiece)
              |
              v
   +--------------------------------------+
   |  Shallow Fusion with External LM     |
   |  (KenLM 5-gram or Neural LM)         |
   |   P(y|x) = log P_asr(y|x) + λ log P_lm(y)   |
   +----------+---------------------------+
              |
              v
        Text Output (Korean: "...회의를 시작하겠습니다")
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Feature Extractor** | 파형 -> 시간-주파수 표현 | Log-Mel(80ch), SpecAugment(시간/주파수 마스킹), Wav2Vec 2.0(SSL Pretext Task: Contrastive Predictive Coding) |
| **Acoustic Model** | 음향 신호 -> 음소/토큰 확률 | **CTC**(병렬 정렬, blank 토큰), **Attention Seq2Seq**(LAS: Listen Attend Spell), **RNN-Transducer**(CTC+Attention 하이브리드, Streaming 친화), **Conformer**(CNN+Attention 병렬) |
| **Language Model** | 단어 시퀀스 확률 보정 | KenLM(5-gram Modified Kneser-Ney), Neural LM(Transformer-XL), Shallow Fusion(λ≈0.3) |
| **Decoder** | 그래디센트/빔서치 | Greedy, Beam Search(b=5~10), CTC Prefix Search, k2/faster-mapped FSA |

**주요 평가 지표**: WER = (S+D+I)/N × 100 (S: 치환, D: 삭제, I: 삽입, N: 정답 단어 수). 한국어는 **CER(문자 오류율)** 사용이 보편적이며, **조음 변동(경음화, 비음화, 연음) 처리**가 WER을 좌우한다.

### 2. Speaker Diarization — "누가 언제 말했는가"

**핵심 구성**: VAD -> 화자 임베딩 추출 -> 클러스터링/분할 -> 재분할(Resegmentation).

```text
[ Speaker Diarization Pipeline - Clustering + End-to-End Hybrid ]

   입력: 회의 음성 (다채널 또는 단일 채널)
            |
            v
   +------------------+
   |   VAD (음성 구간 검출)
   |  Silero VAD / WebRTC / pyannote VAD
   |  출력: 음성 구간 리스트 [(0.5s, 2.3s), (3.0s, 5.7s), ...]
   +----------+-------+
              |  슬라이딩 윈도우 (1.5s, hop 0.75s)
              v
   +--------------------------------------+
   |  Speaker Embedding Network           |
   |  (ResNet34 / ECAPA-TDNN)             |
   |   <- AAM-Softmax Loss (margin=0.2,   |
   |      scale=30)                       |
   |  출력: 192-d x-vector 또는 512-d d-vector
   +----------+---------------------------+
              |
              v
   +--------------------------------------+
   |  Clustering (화자 수 자동 추정)       |
   |  - Spectral Clustering (Eigen-gap)    |
   |  - Agglomerative Hierarchical (AHC)  |
   |  - VBx (Variational Bayes HMM, Kaldi)|
   |  출력: 화자 ID 라벨                  |
   +----------+---------------------------+
              |
              v
   +--------------------------------------+
   |  Resegmentation (경계 정밀화)         |
   |  - VBx Reseg                        |
   |  - Spectral Subtract                |
   |  - End-to-End MSDD (Multi-Scale     |
   |    Diarization Decoder, NeMo)       |
   +----------+---------------------------+
              |
              v
   RTTM (Rich Transcription Time Marked) 출력
   SPEAKER meeting 1 12.345 4.567 <NA> <NA> SPEAKER_00 <NA>
   SPEAKER meeting 1 17.012 3.891 <NA> <NA> SPEAKER_01 <NA>
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **VAD (Voice Activity Detection)** | 비음성 구간 제거 | Silero VAD(ONNX, 4MB), WebRTC VAD(GMM), Energy-based, DNN 기반(상용 SOTA) |
| **Speaker Embedding** | 화자 특성 192~512d 벡터 추출 | **x-vector**(Kaldi, TDNN, PLDA 점수), **d-vector**(LSTM), **ECAPA-TDNN**(Squeeze-Excitation, Attentive Statistics Pooling, SOTA) |
| **Clustering** | 동일 화자 임베딩 그룹화 | Spectral Clustering(Ng-Jordan-Weiss), AHC(complete linkage, threshold 0.5~0.7), **VBx**(