---
title: "Speech Recognition TTS ASR Voice Synthesis"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 668
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 음성 인식(ASR)은 음향 모델(Acoustic Model, AM)·발음 모델(Pronunciation Lexicon)·언어 모델(Language Model, LM)의 3-그램 결합으로 음소 시퀀스를 텍스트 토큰으로 매핑하는 과정이며, TTS는 텍스트 -> 음소/멜 스펙트로그램 -> 신경망 보코더(Vocoder)를 통한 파형 합성으로 구성된다. Whisper, Conformer, VITS, FastSpeech 2와 같은 End-to-End Transformer 기반 모델이 기존 HMM/GMM 파이프라인을 대체하고 있다.
> 2. **가치**: 콜센터 자동화 시 평균通话 시간(ATT) 30~45% 단축, AI 비서 응답 지연(Latency) 300ms 이내 구현으로 인간과 자연스러운 대화 가능, 음성 데이터는 비정형 데이터 중 연평균 18% 증가하며(2024~2028 Gartner), 멀티모달 AI의 핵심 인터페이스로 부상했다.
> 3. **판단 포인트**: 실시간성(Streaming vs Batch), 도메인 특화(범용 모델 vs 화자/용도 적응), 합성 음성 자연스러움(MOS 4.0+ 목표), 저지연 추론(Edge On-device vs Cloud), 그리고 데이터 프라이버시(개인정보보호법·EU AI Act의 음성 생체정보 규제 준수) 간의 트레이드오프가 핵심 결정 변수다.

---

## Ⅰ. 개요 및 필요성

음성 인터페이스는 키보드/터치 대비 **손·눈 점유율이 0%**라는 결정적 장점 때문에车载 인포테인먼트, 스마트홈, IoT, 콜센터, 메타버스 아바타 등에서 HCI(Human-Computer Interaction)의 새로운 표준으로 자리 잡았다. 2024년 Gartner에 따르면 미국 성인의 **42%가 주 1회 이상** 음성 비서를 사용하며, 한국은 25.3%(2023년 방송통신위원회 조사)로 모바일·가전·금융 분야로 확산 중이다.

음성 인식(ASR, Automatic Speech Recognition)과 음성 합성(TTS, Text-to-Speech)는 **대칭 구조**를 가진다. ASR는 아날로그 음성 신호 `x(t)`를 샘플링(16kHz/16bit PCM)하여 MFCC·필터뱅크·멜 스펙트로그램으로 변환한 뒤 음소/단어 시퀀스 `W* = argmax P(W|X)`로 복원하는 추론 문제이며, TTS는 그 역방향으로 텍스트 `Y`를 멜 스펙트로그램 `M`을 거쳐 시간 영역 파형 `ŷ(t)`로 변환하는 생성 문제다. 두 분야 모두 2017년 Transformer 등장 이후 **End-to-End(E2E) 학습**으로 패러다임이 전환되었으며, HMM(Hidden Markov Model)·GMM-HMM·DNN-HMM 같은 모듈형 구조는 학술·연구 목적으로만 남아 있다.

기존 키워드 스팟팅(Keyword Spotting)이나 명령어 인식은 **Closed-vocabulary**(`if-else` 분기 기반)와 **Finite State Grammar**로 구현되었으나, 자연스러운 대화에서는 개방형 어휘(Open-vocabulary)와 문맥 의존성을 처리해야 하므로 **언어 모델과 음향 모델의 결합**이 필수다. 한국어의 경우 교착어 특성상 조사·어미 변형이 많아 형태소 분석기(MeCab-ko, KoNLPy)와 음성 인식 결과를 결합한 후처리 모듈이 요구된다.

```text
+----------------------------------------------------------------------+
|              음성 인터페이스 시스템의 양방향 파이프라인                  |
+----------------------------------------------------------------------+
|                                                                      |
|  [사용자 음성]                                                        |
|       |                                                              |
|       v                                                              |
|  +---------+   +---------+   +---------+   +---------+   +---------+|
|  |  AFE    |--->|  VAD    |--->|   ASR   |--->|   NLU   |--->|  Dialog ||
|  | (전처리) |   | (음성구간)|   |(음성->텍스트)|  |(의도/개체)|  |  Mgr.   ||
|  +---------+   +---------+   +---------+   +---------+   +---------+|
|       |              ^                            |          |       |
|       |    +---------+-----------+                |          v       |
|       |    |  AEC(에코 제거)      |                |      +------+   |
|       |    |  Beamforming(빔포밍) |                |      | 정책 |   |
|       |    |  NS(잡음 억제)       |                |      +------+   |
|       |    +---------------------+                |          |       |
|       |                                           |          v       |
|       |                                       +---------+  +---------+|
|       |                                       |  TTS    |<--|  NLG    ||
|       |                                       |(텍스트->음성)|(응답생성)||
|       |                                       +---------+  +---------+|
|       |                                              |                |
|       v                                              v                |
|   [마이크 입력]                                   [스피커 출력]         |
+----------------------------------------------------------------------+
        ASR 경로 (STT) <------------------------> TTS 경로
```

음성 인터페이스의 품질은 단순 인식률(WER, Word Error Rate)로 환원되지 않는다. **응답 지연(End-to-End Latency)**, **화자 독립성(Speaker Independence)**, **잡음 환경 강건성(Noise Robustness)**, **방언·신조어 적응력**, **개인정보 비식별화**가 동시에 충족되어야 한다. 또한 2024년 발효된 EU AI Act는 실시간 원격 생체 인식(Real-Time Remote Biometric Identification)을 **고위험(High-Risk)**로 분류하여, 음성 인식 시스템은 사후 감사·데이터 거버넌스·편향성 테스트를 의무화하고 있다. 한국도 2023년 개정 개인정보보호법으로 **음성 데이터는 생체정보(고유식별정보)**로 명시되어 동의·암호화·파기 절차가 강화되었다.

- **📢 섹션 요약 비유**: 음성 인식은 "사람의 귀와 뇌"를 모방한 것이고, TTS는 "입과 성대"를 모방한 것이다. 옛날 자동 응답기(ARS)는 정해진 번호만 누를 수 있는 "옛날 유선전화" 같았다면, 현대 음성 AI는 "주문·예약·상담까지 자유롭게 통역해주는 통역사"와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

음성 인식 시스템은 크게 **전처리(Front-end)**, **음향 모델(AM)**, **언어 모델(LM)**, **디코더(Decoder)**로 구성되며, TTS는 **텍스트 분석(Front-end)**, **음향 모델(Acoustic Model)**, **보코더(Vocoder)**의 3단 구조다. End-to-End 모델은 이를 단일 신경망으로 통합한다.

```text
[ASR (Whisper/Conformer 기반) 추론 흐름]
-----------------------------------------------------------------------
입력: 16kHz PCM x(t)
   |
   v
[1단계: AFE (Audio Front-End)]
   |  - 25~30ms 윈도우, 10ms 홉(hop) STFT
   |  - 80채널 Log-Mel Spectrogram 산출
   |  - SpecAugment (주파수/시간 마스킹)
   v
[2단계: Encoder (Self-Supervised + Attention)]
   |  - CNN Down-sampling (stride 2, 채널 512)
   |  - Conformer 블록 ×N (Conv + Self-Attention + FFN)
   |  - 출력: 1280-dim 프레임 임베딩
   v
[3단계: Decoder (CTC + Attention 하이브리드)]
   |  - CTC Loss: 帧 단위 greedy/beam search
   |  - Attention Decoder: Transformer LM 결합
   |  - LM Shallow Fusion: KenLM/N-gram 외부 LM 가중합
   v
[4단계: 후처리 (Rescoring & Inverse Text Normalization)]
   |  - 발음사전(Grapheme-to-Phoneme, G2P) 보정
   |  - 한국어 형태소 분석(KoSpacing, PyKoSpacing)
   v
출력: 정규화된 텍스트 "내일 오후 3시에 강남역으로 두 명 예약해줘"
-----------------------------------------------------------------------

[TTS (VITS/FastSpeech2 기반) 합성 흐름]
-----------------------------------------------------------------------
입력: 텍스트 "안녕하세요, 음성 합성 시스템입니다."
   |
   v
[1단계: Text Front-End]
   |  - 텍스트 정규화(TN): 숫자->발음 ("3시" -> "세 시")
   |  - G2P (Grapheme-to-Phoneme): "안녕하세요" -> [a, nj, ʌŋ, ha, se, jo]
   |  - 한국어 특성: 조사 분리, 평서/의문문 운율 마킹
   |  - 음소 임베딩 (256-dim)
   v
[2단계: Acoustic Model (Mel-Spectrogram 생성)]
   |  - FastSpeech2: Duration, Pitch, Energy Predictor
   |  - Variance Adaptor -> Length Regulator
   |  - 디코더: 멜 스펙트로그램 (80-bin × T 프레임)
   v
[3단계: Vocoder (Mel -> Waveform)]
   |  - HiFi-GAN: Multi-period + Multi-scale Discriminator
   |  - 또는 VITS의 Normalizing Flow 결합 구조
   |  - 24kHz/16bit 파형 출력, RTF < 0.1
   v
출력: 음성 파형 ŷ(t), 약 2~5초 길이
-----------------------------------------------------------------------
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **AFE (Audio Front-End)** | 잡음 제거·특징 추출 | WebRTC APM, RNNoise (RNN 기반 잡음 억제), Kaldi `compute-mfcc-feats`. 빔포밍(MVDR/GEV) 알고리즘으로 마이크 어레이 신호 분리. |
| **VAD (Voice Activity Detection)** | 음성/비음성 구간 검출 | Silero-VAD (CNN), WebRTC VAD (GMM). Endpoint Detection은 ASR의 초기 발화 검출 정확도에 1차 영향을 미친다. |
| **Acoustic Model (AM)** | 음향 신호 -> 음소 확률 | HMM-GMM(전통) -> TDNN/LSTM -> Conformer -> Whisper. Wav2Vec 2.0·HuBERT는 자기지도학습(Self-Supervised) pretext task로 비지도 음성 표현 학습. |
| **Language Model (LM)** | 단어 시퀀스 확률 | N-gram(KenLM, 5-gram), Neural LM(BERT, GPT), RNN-T의 Internal LM. Shallow Fusion으로 가중합: `log p'(w) = log p_AM(w\|x) + λ·log p_LM(w)`. |
| **Decoder** | 최적 시퀀스 탐색 | CTC Greedy, Beam Search (beam=5~10), WFST(Weighted Finite State Transducer) 기반 HMM 디코더. CTC + Attention Joint Decoding이 표준. |
| **TTS Text Front-End** | 텍스트 정규화·음소 변환 | ko_KR G2P (eSpeak-ng, HMM 기반), 종성 규칙, 숫자/약어/외래어 발음 사전. KSS(Korean Single Speaker Speech) 데이터셋 활용. |
| **TTS Acoustic Model** | 음소 -> 멜 스펙트로그램 | Tacotron 2 -> FastSpeech (Non-Autoregressive, 병렬 합성) -> FastSpeech 2 (Variance Adaptor) -> VITS (VAE + Flow). |
| **Vocoder** | 멜 스펙트로그램 -> 파형 | WaveNet (Autoregressive, 24kHz) -> Parallel WaveGAN -> HiFi-GAN (Real-Time Factor 0.01) -> BigVGAN (24kHz 대역폭 확장). |
| **Wake Word Detection** | 저전력 활성화어 검출 | KWS(KeyWord Spotting), Edge Impulse, Picovoice Cheetah. TinyML 모델 (CRNN, TC-ResNet) 100KB 이하, MSP430/Cortex-M4에서 추론. |

### 핵심 알고리즘 심층 분석

**1) CTC (Connectionist Temporal Classification) Loss**
음성 프레임 길이 `T`와 출력 토큰 길이 `U`의 정렬 불일치를 해결하기 위해 Graves(2006)가 제안한 손실 함수. `L_CTC = -log P(Y|X) = -log Σ_π ∏_t p_t(π_t)`이며, blank 토큰(∅)으로 가능한 모든 alignment를 합산한다. Forward-Backward 알고리즘으로 `O(T·U)` 시간에 계산 가능하다.

**2) Attention 기반 Seq2Seq**
Bahdanau Attention(2015)을 음성에 적용한 Listen-Attend-Spell(LAS). `α_t = softmax(score(h_enc, s_dec))`, `c_t = Σ α_t · h_enc`로 컨텍스트 벡터를 만들고, 점진적으로 문자를 생성한다. 단, **Attention Collapse**(반복 생성) 현상이 있어 monotonic attention, CTC prefix score로 보정한다.

**3) Conformer (Gulati et al., 2020)**
Convolution + Self-Attention의 결합: `x' = x + 1/2 FFN(x)`, `x'' = x' + MHSA(x')`, `x''' = x'' + Conv(LN(x''))`, `y = LN(x''') + 1/2 FFN(LN(x'''))`. CNN은 지역적 패턴(Local), Attention은 전역 의존성(Global)을 동시에 포착해 WER 5~15% 개선.

**4) Self-Supervised Pretraining (Wav2Vec 2.0, HuBERT)**
대규모 unlabeled 음성(예: 960h Librispeech, 31k hours CommonVoice)으로 Contrastive Task 학습 후 labeled data로 fine-tuning. **Labeled data 10분 만으로 WER 4.8/8.2%** 달성(Librispeech clean/other). 한국어에서는 `kresnik` 라이브러리, ETRI `koswav2vec`, Kakao `K-Wav2Vec`이 대표적이다.

**5) Whisper (OpenAI, 2022)**
68만 시간 다국어·다중작업(Multitask) 약지도학습. 30초 청크 단위 인코더-디코더, timestamp 토큰·언어 토큰을 직접 예측. 한국어 WER 약 8~12%, 도메인 일반화 우수. **Var-VAD(Variable VAD) + 길이 페널티**로 hallucination 제어.

**6) FastSpeech 2 & VITS의 진화**
FastSpeech 2는 **Duration·Pitch·Energy Predictor**를 명시적으로 모델링해 teacher-forcing 오차를 제거(병렬 합성 50x 가속). VITS는 **VAE + Normalizing Flow**로 멜-파형을 통합 생성해 MOS 4.4 달성(20kHz). 2023년 **StyleTTS 2**, **NaturalSpeech 3**(Factorized Codec) 등장.

**7) 실시간 스트리밍 처리**
- **Chunk-based ASR**: 200~300ms 청크 단위 처리, Emformer/Conformer-XL의 Memory Bank로 문맥 유지
- **Server-Sent Events (SSE)** + **WebSocket** 전송: 부분 결과(Partial) -> 최종 결과(Final) 점진 응답
- **단어 단위 지연 200~400ms**가 자연스러운 대화