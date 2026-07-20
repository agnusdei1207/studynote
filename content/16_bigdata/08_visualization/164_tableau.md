---
title: "Tableau"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 164
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Tableau는 VizQL (Visual Query Language, 시각화 질의 언어)이라는 독자 기술로 드래그앤드롭 동작을 데이터베이스 쿼리로 자동 변환하여 SQL 없이 복잡한 분석을 가능하게 하는 업계 선도적 셀프서비스 시각화 플랫폼이다.
- **가치**: LOD (Level of Detail, 세부 수준) 표현식(FIXED/INCLUDE/EXCLUDE)은 시각화 집계 수준과 독립적인 계산을 가능하게 하여, "고객당 첫 구매일" 같은 복잡한 비즈니스 질문을 SQL 없이 해결하는 핵심 차별화 기능이다.
- **판단 포인트**: Live Connection(항상 최신, 성능 의존)과 Extract(.hyper 인메모리, 빠름, 갱신 필요)의 선택은 데이터 볼륨·갱신 빈도·보안 요건에 따라 결정되며, Power BI 대비 시각화 유연성이 높지만 Microsoft 생태계 통합은 약하다.

---

## Ⅰ. 개요 및 필요성

### Tableau의 역사와 위치

Tableau는 2003년 Pat Hanrahan(스탠퍼드 교수, Pixar 공동 창업자)와 Chris Stolte, Christian Chabot이 창업했다. 2019년 Salesforce에 157억 달러에 인수되어 현재 Salesforce 생태계의 핵심 분석 플랫폼으로 운영된다.

Gartner Magic Quadrant BI & Analytics 분야에서 지속적 리더 위치를 유지하며, 기업용 BI 시장에서 Microsoft Power BI와 1, 2위를 다툰다.

**📢 섹션 요약 비유**: Tableau는 <strong>전문 사진작가의 카메라</strong>와 같다. 기본 사진(간단한 차트)은 스마트폰(Excel)으로도 찍을 수 있지만, 전문적이고 정밀한 작업(복잡한 분석·시각화)에는 전문 장비(Tableau)가 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Tableau 플랫폼 아키텍처

```
+-------------------------------------------------------------+
|                  Tableau 플랫폼 구조                         |
+--------------------------------------------------------------+
|  데이터 연결 계층                                            |
|  +------------------------------------------------------+   |
|  |  Live Connection  |  Extract (.hyper)                |   |
|  |  - 직접 DB 쿼리   |  - 인메모리 컬럼형 엔진          |   |
|  |  - 항상 최신      |  - 빠른 쿼리 성능               |   |
|  |  - DB 성능 의존   |  - 갱신 스케줄 필요              |   |
|  +------------------------------------------------------+   |
|                          |                                   |
|  분석·계산 계층           v                                   |
|  +------------------------------------------------------+   |
|  |                   VizQL 엔진                          |   |
|  |  드래그앤드롭 -> SQL/MDX 자동 변환 -> 결과 시각화        |   |
|  |                                                      |   |
|  |  계산 유형:                                           |   |
|  |  ① 계산 필드 (Calculated Field): 커스텀 수식          |   |
|  |  ② LOD 표현식: FIXED/INCLUDE/EXCLUDE                 |   |
|  |  ③ 테이블 계산: 누적합, 순위, 전년 대비              |   |
|  +------------------------------------------------------+   |
|                          |                                   |
|  공유·배포 계층           v                                   |
|  +----------------+-------------------------------------+   |
|  |Tableau Desktop |Tableau Server / Tableau Cloud (SaaS)|   |
|  |(로컬 제작 도구)|(공유·임베딩·중앙 거버넌스)           |   |
|  +----------------+-------------------------------------+   |
+-------------------------------------------------------------+
```

### LOD (Level of Detail) 표현식

LOD 표현식은 Tableau의 가장 독특하고 강력한 기능으로, <strong>시각화의 집계 수준과 무관하게 별도의 집계 계산</strong>을 수행한다.

| LOD 유형 | 문법 | 의미 | 예시 |
|:---|:---|:---|:---|
| **FIXED** | `{FIXED [차원]: 집계}` | 지정 차원 수준에서 고정 계산 | `{FIXED [고객ID]: MIN([주문일])}` |
| <strong>INCLUDE</strong> | `{INCLUDE [차원]: 집계}` | 현재 뷰 + 추가 차원 포함 | 뷰가 지역 수준이어도 도시 수준 계산 |
| **EXCLUDE** | `{EXCLUDE [차원]: 집계}` | 현재 뷰에서 지정 차원 제외 | 지역 포함 뷰에서 지역 무관 전체 합계 |

**FIXED 사용 사례**: "고객당 첫 구매일을 계산하라"
```
// Tableau Calculated Field
First Order Date = {FIXED [Customer ID]: MIN([Order Date])}
```
-> 시각화가 제품·지역·시간 수준이어도 항상 고객 수준으로 집계

**📢 섹션 요약 비유**: LOD 표현식은 <strong>조명 개별 제어 시스템</strong>과 같다. 방 전체 조명(시각화 전체 집계)과 무관하게 특정 구역의 조명(FIXED 집계)만 독립적으로 제어할 수 있다.

---

## Ⅲ. 비교 및 연결

### Tableau vs Power BI 비교

| 차원 | Tableau | Power BI |
|:---|:---|:---|
| <strong>시각화 유연성</strong> | 높음 — 사용자 정의 차트 풍부 | 중간 — 주요 차트 유형 충분 |
| **계산 언어** | LOD + 테이블 계산 | DAX (강력하나 학습 곡선 있음) |
| **생태계** | Salesforce CRM 통합 강점 | Microsoft 365, Azure 깊은 통합 |
| **가격** | 높음 (Creator ~$70/월) | 낮음 (Pro $10/월) |
| <strong>데이터 준비</strong> | Tableau Prep Builder 별도 | Power Query 내장 |
| **실시간** | Live Connection + Streaming | DirectQuery + Power BI Streaming |
| <strong>AI 기능</strong> | Ask Data, Tableau Pulse | Q&A, Key Influencers, Decomp Tree |

### Tableau Prep Builder

Tableau Prep은 <strong>비주얼 데이터 준비 도구</strong>로, 플로우 캔버스에서 데이터 클렌징·변환·결합을 시각적으로 수행한다:
- 각 변환 단계의 데이터 미리보기 즉시 확인
- 자동 필드 타입 추론
- 비교 지도(Join 불일치 시각화)
- Tableau Server와 직접 통합 (게시·스케줄)

**📢 섹션 요약 비유**: Tableau vs Power BI는 <strong>Mac vs Windows</strong>와 같다. Mac(Tableau)은 디자인·유연성이 우수하고, Windows(Power BI)는 기업 생태계 통합이 강하다. 어떤 것이 더 좋은지는 조직의 생태계와 목적에 달려있다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 테이블 계산(Table Calculation) 활용

| 계산 유형 | 용도 |
|:---|:---|
| Running Total (누적 합계) | 누적 매출 추세 |
| Percent of Total | 전체 대비 비율 |
| Rank | 제품별 순위 |
| Percent Difference | 전년 대비 증감률 |
| Moving Average | 이동 평균 (7일, 30일) |

### Tableau Pulse (2024)

Tableau Pulse는 AI 기반 <strong>데이터 스토리텔링 자동화</strong> 기능:
- 자연어로 지표 설명 자동 생성
- 이상 감지 자동 알림
- Slack·이메일로 인사이트 자동 배포
- Salesforce Einstein AI와 통합

**📢 섹션 요약 비유**: Tableau Pulse는 <strong>AI 애널리스트 보조원</strong>과 같다. 데이터를 보고 "지난주 매출이 전주 대비 15% 하락했으며, 주요 원인은 서울 지역 고객 이탈"이라고 자동으로 리포트를 작성해준다.

---

## Ⅴ. 기대효과 및 결론

### Tableau 도입 효과

| 영역 | 효과 |
|:---|:---|
| **분석 민주화** | SQL 비전문가도 복잡한 분석 가능 |
| **인사이트 속도** | 리포트 생성 시간 80% 단축 |
| <strong>데이터 거버넌스</strong> | Tableau Server의 중앙 인증·접근 제어 |
| **협업** | Tableau Server/Cloud 대시보드 공유 |

### 결론

Tableau는 셀프서비스 분석의 <strong>표준</strong>을 만든 플랫폼이다. VizQL의 직관적 인터페이스와 LOD 표현식의 강력한 계산 능력은 비즈니스 사용자와 데이터 분석가 양측의 요구를 충족한다. Power BI와 비교 시 비용이 높지만, 복잡한 시각화 커스터마이징과 분석 유연성이 필요한 조직에서는 Tableau가 더 적합하다.

**📢 섹션 요약 비유**: LOD 표현식을 마스터한 Tableau 사용자는 <strong>위상수학을 이해한 지도 제작자</strong>와 같다. 단순히 지도를 그리는 것을 넘어, 어떤 각도에서 어떤 수준으로 봐도 정확한 지형을 계산할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| VizQL | 핵심 기술 | 드래그앤드롭을 DB 쿼리로 자동 변환 |
| LOD 표현식 | 차별화 기능 | FIXED/INCLUDE/EXCLUDE 독립 집계 |
| Live Connection | 데이터 모드 | 직접 DB 쿼리, 항상 최신 |
| Extract (.hyper) | 데이터 모드 | 인메모리 컬럼형, 빠른 성능 |
| Tableau Prep | 데이터 준비 | 비주얼 ETL 플로우 캔버스 |
| Tableau Pulse | AI 기능 | 자동 인사이트 생성·배포 |
| Power BI | 경쟁 제품 | Microsoft 생태계 강점, 저렴한 비용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[:---]
    |
    v
[VizQL]
    |
    v
[LOD 표현식]
    |
    v
[Live Connection]
    |
    v
[Extract (.hyper)]
    |
    v
[Tableau Prep]
    |
    v
[Tableau Pulse]
```

이 흐름도는 :---에서 출발해 Tableau Prep까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- Tableau는 <strong>레고 놀이</strong>처럼 데이터 조각을 끌어다 놓으면 자동으로 차트가 만들어지는 도구예요 — 코딩 없이도 복잡한 분석을 할 수 있어요.
- LOD 표현식은 "차트는 지역별로 보여주지만, 계산은 고객별로 해줘"라고 말할 수 있는 마법 주문이에요 — 두 가지 수준을 동시에 다룰 수 있어요.
- Live Connection은 "항상 최신 데이터를 보는 것"이고, Extract는 "빠르게 미리 준비해놓은 데이터를 보는 것"이에요 — 속도와 최신성을 바꿔서 선택하는 거예요.
