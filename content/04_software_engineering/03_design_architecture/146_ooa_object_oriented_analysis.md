---
title: "Ooa Object Oriented Analysis"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 146
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OOA는 <strong>문제 영역(Problem Domain)을 객체·클래스·속성·메서드·관계로 모델링</strong>하는 분석 기법이며, 구조적 분석(DFD)의 "데이터·프로세스 분리"와 달리 <strong>데이터+행위를 객체로 캡슐화</strong>한다.
> 2. **가치**: 현실 세계를 객체로 모델링하므로 <strong>분석 결과가 설계·구현으로 자연스럽게 전이(Traceability)</strong>되며, 재사용·확장성이 높다.
> 3. **판단 포인트**: Rumbaugh OMT(객체·동적·기능 모델)·Booch Method·Jacobson OOSE(유스케이스)가 통합되어 <strong>UML(Unified Modeling Language)</strong>이 탄생(1997)했다.

---

## Ⅰ. 개요 및 필요성

```text
OOA 산출물:
  유스케이스 다이어그램 (기능 범위)
  클래스 다이어그램 (구조·관계)
  시퀀스 다이어그램 (동적 상호작용)
  상태 다이어그램 (객체 생명주기)
```

- **📢 섹션 요약 비유**: OOA는 <strong>레고 설계</strong>이다. 레고 블록(객체)의 모양(속성)과 연결 방법(관계)을 먼저 설계한다.

---

## Ⅱ~Ⅴ. 결론

OOA는 <strong>현실->모델 전이가 자연스러운 분석 방법</strong>이며, UML이 표준 표현 도구이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **OOA** | 객체지향 분석 |
| **유스케이스** | 기능 범위 |
| **클래스** | 구조·관계 |
| <strong>UML</strong> | 통합 표현 |
| **OMT** | Rumbaugh 3모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[구조적 분석 (DFD, 1978)] -> [OMT (Rumbaugh, 1991)]
    -> [OOSE (Jacobson, 1992)] -> [UML 통합 (1997)]
    -> [현재: UML + Agile — 경량 모델링]
```

### 👶 어린이를 위한 3줄 비유 설명
1. OOA는 <strong>레고 설계</strong>예요. 블록(객체)의 <strong>모양과 연결 방법</strong>을 정해요.
2. "학생" 블록은 <strong>이름·학번(속성)</strong>이 있고, "수업 듣기(행위)"를 해요.
3. 레고 설계도(UML)를 그리면 <strong>조립(구현)</strong>이 쉬워요!
