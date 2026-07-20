---
title: "Structured Analysis Dfd Dd Minispec"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 구조적 분석은 <strong>DFD(데이터 흐름도)·DD(데이터 사전)·Mini-Spec(프로세스 명세서)</strong>로 시스템의 데이터 흐름과 변환을 체계적으로 분석하는 전통적 방법론(DeMarco, 1978)이다.
> 2. **가치**: DFD는 시스템의 <strong>"무엇(What)"을 데이터 흐름 중심으로</strong> 표현하여, 사용자·분석가·개발자 간 <strong>공통 이해</strong>를 형성한다.
> 3. **판단 포인트**: DFD의 4대 구성요소(프로세스·데이터 흐름·데이터 저장소·외부 엔티티)와 레벨링(Context->Level 0->Level 1)이 핵심이며, 현재는 UML·User Story에 의해 보완되었다.

---

## Ⅰ. 개요 및 필요성

```text
DFD 4대 구성요소:
  ○ 프로세스 (데이터 변환)
  -> 데이터 흐름 (화살표)
  - 데이터 저장소 (DB)
  □ 외부 엔티티 (사용자·외부 시스템)
레벨링: Context DFD -> Level 0 -> Level 1 (분해)
```

- **📢 섹션 요약 비유**: DFD는 <strong>수도관 배관도</strong>이다. 물(데이터)이 어디서 와서 어디로 흐르는지 보여준다.

---

## Ⅱ~Ⅴ. 결론

구조적 분석은 <strong>데이터 흐름 중심의 전통적 분석 방법</strong>이며, DFD·DD·Mini-Spec의 3종 세트가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>DFD</strong> | 데이터 흐름도 |
| <strong>DD</strong> | 데이터 사전 |
| <strong>Mini-Spec</strong> | 프로세스 명세 |
| <strong>Context DFD</strong> | 최상위 레벨 |
| <strong>UML</strong> | 현대적 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[구조적 분석 (DeMarco, 1978)] -> [SSADM (영국, 1980s)]
    -> [UML (1997)] -> [Agile User Story (2001)]
    -> [현재: DFD는 정보처리기사 시험 필수 + 레거시 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DFD는 <strong>수도관 배관도</strong>예요. 물(데이터)이 **어디서 어디로** 흐르는지 보여줘요.
2. DD(데이터 사전)는 <strong>단어장</strong>이에요. "주문"이 뭔지 **정확히** 정의해요.
3. Mini-Spec은 <strong>요리 레시피</strong>예요. 프로세스가 **무엇을 하는지** 자세히 설명해요!
