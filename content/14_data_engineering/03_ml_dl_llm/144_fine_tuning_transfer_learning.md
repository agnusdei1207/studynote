---
title: "Fine Tuning Transfer Learning"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 144
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Fine-tuning은 <strong>사전 학습된 Foundation Model의 가중치를 특정 도메인·작업의 라벨 데이터로 추가 학습</strong>하여 적응시키는 Transfer Learning 기법이다.
> 2. **가치**: 처음부터 학습하면 <strong>수백만 달러·수개월</strong>이 소요되지만, Fine-tuning은 <strong>소량 데이터(수천~수만)로 수시간</strong>만에 도메인 특화 모델을 만들어 비용을 100배+ 절감한다.
> 3. **판단 포인트**: Full Fine-tuning(전체 가중치)->PEFT(LoRA·QLoRA, 일부만)->Instruction Tuning(지시-응답 쌍)으로 구분하며, LoRA가 LLM Fine-tuning의 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
Full Fine-tuning: 모든 파라미터 업데이트 (비용^)
LoRA: 저랭크 행렬만 추가 학습 (비용vv)
QLoRA: 4비트 양자화 + LoRA (단일 GPU 가능)
Instruction Tuning: 지시-응답 쌍으로 지시 따르기 학습
```

- **📢 섹션 요약 비유**: Fine-tuning은 <strong>대학 졸업생(사전 학습)의 직무 교육(OJT)</strong>이다. 기초 능력이 있으니 적은 교육으로도 전문가가 된다.

---

## Ⅱ~Ⅴ. 결론

Fine-tuning은 <strong>FM을 도메인에 적응시키는 핵심 기법</strong>이며, LoRA/QLoRA가 효율적 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Fine-tuning</strong> | 가중치 적응 |
| <strong>Transfer Learning</strong> | 지식 이전 |
| <strong>LoRA</strong> | 저랭크 PEFT |
| <strong>QLoRA</strong> | 양자화+LoRA |
| <strong>Instruction Tuning</strong> | 지시 따르기 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ImageNet Pre-train (2012)] -> [BERT Fine-tuning (2018)]
    -> [Full FT -> LoRA (2021)] -> [QLoRA (2023)]
    -> [현재: DoRA·LoRA+ — PEFT 고도화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Fine-tuning은 <strong>대학 졸업 후 직무 교육(OJT)</strong>이에요.
2. 기초(사전 학습)가 있으니 <strong>적은 교육</strong>만으로 전문가가 돼요.
3. LoRA는 <strong>핵심 부분만 교육</strong>해서 시간과 비용을 아껴요!
