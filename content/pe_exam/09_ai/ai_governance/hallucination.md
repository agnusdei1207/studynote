+++
title = "Hallucination (환각)"
date = 2026-03-03

[extra]
categories = "pe_exam-ai"
+++

# Hallucination (환각)

## 핵심 인사이트 (3줄 요약)
> 환각은 LLM이 사실이 아닌 내용을 마치 진실인 것처럼 자신감 있게 생성하는 현상입니다.
> LLM의 확률적 생성 방식과 훈련 데이터의 불완전성이 주요 원인입니다.
> RAG, Fact-Checking, Citation 등 다양한 완화 기법이 개발되어 실무에서 적용 중입니다.

---

### Ⅰ. 개요

**개념**: 환각(Hallucination)은 대규모 언어모델(LLM)이 실제로 존재하지 않는 정보, 사실과 다른 내용, 혹은 논리적으로 오류가 있는 텍스트를 마치 진실인 것처럼 자신감 있게 생성하는 현상을 말한다.

> 💡 **비유**: 환각은 **학생이 시험에서 모르는 문제를 그럴듯하게 지어내서 쓰는 것**과 같다. 학생은 "이게 정답일 것 같은데?" 하고 자신 있게 쓰지만, 실제로는 틀린 답이다. LLM도 마찬가지로 다음 단어를 예측할 때 가장 그럴듯한(확률이 높은) 것을 선택하지만, 실제 사실과는 다를 수 있다.

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: ChatGPT 등 LLM이 존재하지 않는 논문을 인용하거나, 실제와 다른 역사적 사실을 말하는 등 신뢰성 문제가 대두되었다. 의료, 법률 등 중요 분야에서 오정보로 인한 피해 사례 발생.

2. **기술적 필요성**: LLM의 학습 방식(Next Token Prediction)은 사실 정확성이 아니라 텍스트 유창성에 최적화되어 있다. 내부 지식의 한계와 확률적 생성 방식이 근본적 원인.

3. **시장/산업 요구**: 의료진료, 법률자문, 금융분석 등 신뢰성이 중요한 분야에서 LLM 활용을 위해 환각 문제 해결이 필수적이었다. EU AI Act 등 규제에서도 고위험 AI의 신뢰성 요구.

**핵심 목적**: 환각 현상의 원인을 이해하고, 발생을 최소화하며, 발생 시 탐지하고 대응하는 기술적/운영적 체계를 수립하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **사실성 환각 (Factual)** | 실제와 다른 정보 생성 | 존재하지 않는 논문, 잘못된 역사 | 날조된 뉴스 |
| **충실도 환각 (Faithfulness)** | 입력과 모순되는 출력 | 문서 요약 시 원문에 없는 내용 추가 | 왜곡된 전화게임 |
| **자기 모순 (Inconsistency)** | 같은 대화에서 상충하는 정보 | 앞뒤가 안 맞는 답변 | 기억 상실 |
| **비논리적 추론 (Reasoning)** | 잘못된 논리로 결론 도출 | 수학 오류, 논리적 비약 | 엉터리 계산 |
| **과신 (Overconfidence)** | 틀린 정보를 자신감 있게 표현 | "확실히 ~입니다" 하지만 오류 | 확신범 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Hallucination Types & Causes                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  환각 유형 (Types)                                                      │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  1. Factual Hallucination (사실성 환각)                           │ │
│  │     "아인슈타인은 1955년에 달에 착륙했다" ← 사실 아님              │ │
│  │                                                                     │ │
│  │  2. Faithfulness Hallucination (충실도 환각)                       │ │
│  │     Input: "날씨가 맑았다"                                         │ │
│  │     Output: "비가 와서 우산이 필요했다" ← 입력과 모순               │ │
│  │                                                                     │ │
│  │  3. Intrinsic Hallucination (내부 모순)                            │ │
│  │     "서울은 한국의 수도다. 부산이 한국의 수도다" ← 자기 모순        │ │
│  │                                                                     │ │
│  │  4. Extrinsic Hallucination (외부 지식 없음)                       │ │
│  │     "2026년 노벨상 수상자는..." ← 아직 일어나지 않은 일             │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  환각 원인 (Causes)                                                     │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                                                                     │ │
│  │   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐      │ │
│  │   │ 데이터 문제  │     │ 모델 구조    │     │ 추론 방식    │      │ │
│  │   ├──────────────┤     ├──────────────┤     ├──────────────┤      │ │
│  │   │ • 노이즈     │     │ • 확률적 생성│     │ • Greedy     │      │ │
│  │   │ • 편향       │     │ • 긴 컨텍스트│     │   Decoding   │      │ │
│  │   │ • 불완전     │     │ • 지식 압축  │     │ • 온도 설정  │      │ │
│  │   └──────────────┘     └──────────────┘     └──────────────┘      │ │
│  │                                                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 프롬프트 입력 → ② 내부 지식 검색 → ③ 확률적 토큰 생성 → ④ 후처리 없이 출력 → ⑤ 환각 발생
```

- **1단계 (입력)**: 사용자 질문이 모델에 입력됨
- **2단계 (지식 검색)**: 모델이 학습된 파라미터에서 관련 정보를 검색. 정보가 불완전하거나 없을 수 있음
- **3단계 (생성)**: 다음 토큰을 확률적으로 선택. "가장 그럴듯한" 것을 선택하지만 "사실"은 아님
- **4단계 (출력)**: 생성된 텍스트가 그대로 출력. 팩트 체크 없음
- **5단계 (환각)**: 사실과 다른 내용이 자신감 있게 출력됨

**핵심 알고리즘/공식** (해당 시 필수):

**토큰 생성 확률**:
```
P(w_t | w_1, ..., w_{t-1}) = softmax( logits_t / T )
```
- T: Temperature (높을수록 창의적/불확실, 낮을수록 결정적)

**환각 스코어 측정**:
```
Hallucination_Score = 1 - (Fact_Accuracy × Consistency × Grounding)
```

**Self-Consistency Check**:
```
Agreement = (1/N) × Σ I(Answer_i == Majority_Vote)
```

**코드 예시** (필수: Python 또는 의사코드):

```python
import openai
import json
from typing import List, Dict

class HallucinationDetector:
    """환각 탐지 및 완화 시스템"""

    def __init__(self, model="gpt-4"):
        self.model = model

    def generate_with_uncertainty(self, prompt: str, n_samples: int = 5) -> Dict:
        """불확실성을 추정하며 생성"""

        responses = []
        for _ in range(n_samples):
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7  # 다양성 확보
            )
            responses.append(response.choices[0].message.content)

        # 응답 간 일치도 계산
        consistency = self._calculate_consistency(responses)

        return {
            "responses": responses,
            "consistency": consistency,
            "is_uncertain": consistency < 0.6
        }

    def _calculate_consistency(self, responses: List[str]) -> float:
        """응답 간 일치도 계산 (간소화 버전)"""
        # 실제로는 NLI 모델이나 의미적 유사도 사용
        unique_responses = len(set(responses))
        return 1 - (unique_responses - 1) / len(responses)

    def fact_check_with_search(self, claim: str) -> Dict:
        """외부 검색으로 팩트 체크"""

        # 검색 쿼리 생성
        search_query = f"fact check: {claim}"

        # 실제로는 Google Search API, Wikipedia API 등 사용
        # 여기서는 개념적 구현만 표시
        search_results = self._search(search_query)

        # 검색 결과와 주장 비교 (LLM으로 검증)
        verification_prompt = f"""
        Claim: {claim}

        Search Results:
        {search_results}

        Is the claim supported by the search results?
        Answer: TRUE / FALSE / UNCERTAIN
        Reasoning: [Brief explanation]
        """

        verification = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": verification_prompt}],
            temperature=0
        )

        return {
            "claim": claim,
            "verification": verification.choices[0].message.content,
            "sources": search_results
        }

    def _search(self, query: str) -> str:
        """외부 검색 (placeholder)"""
        # 실제 구현에서는 SerperAPI, Google Custom Search 등 사용
        return "Search results would appear here..."

    def generate_with_citations(self, prompt: str, documents: List[str]) -> Dict:
        """인용을 포함한 생성 (RAG 기반)"""

        context = "\n\n".join([f"[{i+1}] {doc}" for i, doc in enumerate(documents)])

        rag_prompt = f"""
        Answer the question based ONLY on the provided documents.
        Include citation numbers [1], [2], etc. for each claim.

        Documents:
        {context}

        Question: {prompt}

        Answer with citations:
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": rag_prompt}],
            temperature=0
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": documents
        }


# 환각 완화 전략
class HallucinationMitigation:
    """환각 완화 전략 모음"""

    @staticmethod
    def prompt_engineering():
        """프롬프트 엔지니어링으로 환각 감소"""

        safe_prompt_template = """
        Answer the following question. If you don't know the answer
        or are uncertain, say "I don't have enough information to answer
        this question confidently."

        Guidelines:
        - Only state facts you are certain about
        - Use qualifying language when uncertain (e.g., "I believe", "It appears")
        - If asked about recent events, acknowledge your knowledge cutoff
        - Provide sources when possible

        Question: {question}

        Answer:
        """
        return safe_prompt_template

    @staticmethod
    def chain_of_verification():
        """Chain of Verification 방식"""

        steps = [
            "1. Generate initial response",
            "2. Extract factual claims from response",
            "3. Verify each claim independently",
            "4. Revise response based on verification",
            "5. Output final verified response"
        ]
        return steps


# 사용 예시
if __name__ == "__main__":
    detector = HallucinationDetector()

    # 불확실성 추정
    result = detector.generate_with_uncertainty(
        "What is the population of Seoul in 2026?"
    )
    print(f"Consistency: {result['consistency']:.2f}")
    print(f"Uncertain: {result['is_uncertain']}")

    # 팩트 체크
    fact_check = detector.fact_check_with_search(
        "The Eiffel Tower was built in 1900."
    )
    print(f"Verification: {fact_check['verification']}")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석** (필수: 최소 3개씩):

| 장점 (환각이 있는 이유) | 단점 (문제점) |
|------------------------|---------------|
| 창의적이고 유창한 텍스트 생성 | 오정보 전파로 사회적 피해 |
| 불확실한 정보에도 답변 가능 | 의료/법률 분야에서 위험 |
| 다양한 관점 제시 가능 | AI 신뢰성 저하 |
| 새로운 아이디어 생성에 유용 | 기업 리스크 (법적, 평판) |

**환각 완화 기법 비교** (필수: 최소 2개 대안):

| 비교 항목 | RAG | Fine-tuning | Prompting | Verification |
|---------|-----|-------------|-----------|--------------|
| 핵심 특성 | ★ 외부 지식 검색 | 도메인 특화 학습 | "모르면 모른다고 해" | 생성 후 검증 |
| 효과 | ★ 높음 | 중간 | 낮음~중간 | 높음 |
| 비용 | 중간 | 높음 | 낮음 | 중간 |
| 실시간성 | ★ 가능 | 어려움 | 가능 | 가능 |
| 적합 환경 | ★ 팩트 기반 QA | 도메인 특화 | 일반 대화 | 고신뢰 분야 |

> **★ 선택 기준**:
> - **RAG**: 팩트 기반 질의응답, 최신 정보 필요 시
> - **Fine-tuning**: 특정 도메인 깊이 있는 지식
> - **Prompting**: 비용 민감, 창의적 생성 허용
> - **Verification**: 의료/법률 등 고신뢰 분야

**환각 탐지 기법 비교**:

| 기법 | 방식 | 정확도 | 한계 |
|-----|------|--------|------|
| Self-Consistency | 여러 생성 비교 | 중간 | 계산 비용 |
| Token Probability | 낮은 확률 토큰 탐지 | 낮음 | 유창한 환각 탐지 어려움 |
| Factual Check | 외부 DB 검증 | ★ 높음 | 시간, 커버리지 |
| NLI Model | 전제-가정 모순 탐지 | 중간 | 문장 단위 한계 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **의료 AI** | RAG + 의료 DB + 전문가 검증 | 오진율 70% 감소 |
| **법률 상담** | 판례 DB 연동 + Citation 필수 | 법적 오류 80% 감소 |
| **고객 서비스** | 제품 DB RAG + 모르면 연결 | 고객 불만 40% 감소 |
| **뉴스 생성** | 팩트체크 시스템 + Human-in-loop | 오보율 90% 감소 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Perplexity AI** - RAG 기반 검색엔진으로 모든 답변에 출처 인용. 환각 감소하면서도 정보 접근성 향상.

- **사례 2: BloombergGPT** - 금융 도메인 특화 LLM으로 사실 정확성 강화. 실시간 시장 데이터 연동으로 환각 최소화.

- **사례 3: Microsoft Copilot** - 웹 검색과 결합하여 최신 정보 제공. "출처 보기" 기능으로 사용자가 검증 가능.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: RAG 시스템 구축 비용, 검색 품질이 답변 품질 결정, 실시간 업데이트 체계

2. **운영적**: Human-in-the-Loop 검증 체계, 사용자 교육 (AI 한계 인식), 피드백 수집 시스템

3. **보안적**: 오정보로 인한 법적 책임, 면책 조항 필수, 위험한 분야 제한

4. **경제적**: RAG 시스템 비용 (벡터 DB, 검색 API), 검증 인력 비용, 환각으로 인한 리스크 비용

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **100% 정확 기대**: 환각은 완전 제거 불가능. 해결: 적절한 기대치 설정, 검증 체계 구축
- ❌ **Temperature=0 믿음**: 낮은 온도도 환각 가능. 해결: RAG, 검증 병행
- ❌ **인용 신뢰**: LLM이 가짜 인용 생성 가능. 해결: 인용 링크 실제 확인
- ❌ **도메인 무관성**: 모든 도메인에서 동일 수준 기대. 해결: 도메인별 평가

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  Hallucination 핵심 연관 개념 맵                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [LLM] ←──→ [Hallucination] ←──→ [AI Safety]                  │
│      ↓              ↓                 ↓                         │
│   [RAG]        [Fact-Checking]   [Misinformation]              │
│      ↓              ↓                 ↓                         │
│   [Vector DB] ←──→ [XAI] ←──→ [Trustworthy AI]                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| RAG | 완화 기술 | 외부 지식 검색으로 환각 감소 | `[rag](../generative_ai/rag.md)` |
| XAI | 병행 기술 | 설명 가능성으로 신뢰성 향상 | `[xai](./xai.md)` |
| AI Safety | 상위 개념 | AI 위험성 관리 | `[ai_safety](./ai_safety.md)` |
| Fact-Checking | 완화 기술 | 외부 검증 시스템 | `[fact_checking](./fact_checking.md)` |
| Trustworthy AI | 목표 | 신뢰할 수 있는 AI 구축 | `[trustworthy_ai](./trustworthy_ai.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 정확성 | 사실 오류 감소 | RAG 적용 시 60~80% 감소 |
| 신뢰성 | 사용자 신뢰도 | NPS 20점 향상 |
| 리스크 | 법적/평판 피해 | 클레임 70% 감소 |
| 효율성 | 검증 비용 | 자동화로 50% 절감 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: 실시간 팩트체크, 멀티모달 검증, 인간-AI 협업 검증 시스템

2. **시장 트렌드**: EU AI Act 등 규제로 고위험 분야 환각 완화 의무화. 산업별 신뢰성 표준 수립.

3. **후속 기술**: Neuro-symbolic AI (신경망 + 기호추론), Grounded Language Generation

> **결론**: 환각은 LLM의 근본적 한계이지만, RAG, 검증 시스템, 적절한 운영 체계로 상당히 완화할 수 있다. 기술사로서 환각의 원인을 이해하고, 도메인별 적절한 완화 전략을 수립하는 능력이 필수적이다.

> **※ 참고 표준**: OpenAI Hallucination Research, Google " grounding" 연구, EU AI Act Article 13-15 (Transparency)

---

## 어린이를 위한 종합 설명

환각은 마치 **친구가 모르는 이야기를 마치 진짜처럼 지어내서 말하는 것**과 같아요.

여러분이 친구에게 "공룡에 대해 알려줘!"라고 했어요. 그런데 친구가 "티라노사우루스는 보라색이었고, 아이스크림을 좋아했어!"라고 해요.

그럴듯하게 들리지만... 틀렸죠? 티라노사우루스는 보라색이 아니었고, 아이스크림도 안 먹었어요!

AI인 ChatGPT도 가끔 이래요:
- 존재하지 않는 책을 인용해요 ("2024년에 나온 해리포터 8권에서...")
- 틀린 역사를 말해요 ("미국은 1776년에 달나라에 갔어!")
- 없는 사람을 만들어요 ("홍길동은 1990년에 태어난 유명한 과학자야...")

왜 이러냐고요? AI는 진짜로 아는 게 아니라, "다음에 올 것 같은 말"을 예측만 하는 거예요. 그래서 모르는 것도 그럴듯하게 지어내는 때가 있어요.

그래서 우리는:
1. AI가 말한 걸 그대로 믿지 말아요
2. 중요한 건 직접 확인해요
3. "출처 있어?"라고 물어봐요

AI는 정말 똑똑하지만, 가끔 엉뚱한 소리도 한다는 걸 기억해요! 🤖💭
