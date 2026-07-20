---
title: "Power Bi"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 165
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Power BI는 Power Query(M 언어 데이터 변환)·DAX(Data Analysis Expressions 계산)·시각화의 3레이어로 구성되며, Microsoft 365·Azure·Fabric 생태계와의 깊은 통합을 통해 엔터프라이즈 BI의 표준 플랫폼으로 자리잡았다.
- **가치**: DAX의 필터 컨텍스트(Filter Context)와 행 컨텍스트(Row Context) 개념을 이해하고 CALCULATE로 필터를 조작하는 능력이 Power BI 고급 사용자와 기초 사용자를 구분하는 핵심 역량이다.
- **판단 포인트**: Microsoft Fabric(2023)은 Power BI + Data Factory + Synapse를 통합한 One Lake 기반 분석 플랫폼으로, 데이터 적재부터 시각화까지 단일 SaaS 환경에서 처리하는 패러다임 전환을 의미한다.

---

## Ⅰ. 개요 및 필요성

### Power BI의 위치와 성장

Power BI는 2015년 Microsoft가 출시한 클라우드 기반 BI 서비스다. 현재 Fortune 500 기업의 97% 이상이 사용하며, Gartner BI Magic Quadrant에서 Tableau와 함께 꾸준히 리더로 평가된다.

Power BI의 핵심 경쟁 우위:
- **비용**: Power BI Pro $10/사용자/월 vs Tableau Creator ~$70/월
- **Microsoft 통합**: Teams, SharePoint, Excel, Azure, OneDrive 네이티브 연동
- <strong>AI 기능</strong>: OpenAI 기반 Copilot (질의응답, 자동 인사이트, 요약)
- **학습 곡선**: Excel 사용자가 빠르게 전환 가능

**📢 섹션 요약 비유**: Power BI는 <strong>Microsoft Office 생태계의 완성판</strong>이다. Excel로 데이터를 다루던 사용자가 Power BI로 이전하면, 익숙한 환경에서 훨씬 강력한 분석·시각화·공유 능력을 얻는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Power BI 3레이어 아키텍처

```
+-------------------------------------------------------------+
|                Power BI 3레이어 구조                         |
+--------------------------------------------------------------+
|  Layer 1: Power Query (데이터 수집·변환)                     |
|  +--------------------------------------------------------+ |
|  |  M 언어 기반 ETL 엔진                                   | |
|  |  - 300+ 데이터 커넥터 (DB, API, 파일, 클라우드)         | |
|  |  - 변환: 피벗/언피벗, 조인, 텍스트 처리, 형변환         | |
|  |  - 단계별 변환 이력 관리 (Applied Steps)                | |
|  +--------------------------------------------------------+ |
|                          |                                   |
|  Layer 2: 데이터 모델 (관계·계산)                            |
|  +--------------------------------------------------------+ |
|  |  스타 스키마: 팩트 테이블 + 차원 테이블                  | |
|  |  관계 정의: 1:N, N:M, 양방향                            | |
|  |                                                        | |
|  |  DAX 계산:                                             | |
|  |  ① 계산 컬럼(Calculated Column): 행 단위 계산           | |
|  |  ② 측정값(Measure): 동적 집계 (권장)                   | |
|  |  ③ 계산 테이블(Calculated Table): 새 테이블 생성        | |
|  +--------------------------------------------------------+ |
|                          |                                   |
|  Layer 3: 시각화 (보고서·대시보드)                           |
|  +--------------------------------------------------------+ |
|  |  Power BI Desktop: 보고서 제작                          | |
|  |  Power BI Service: 게시·공유·협업                       | |
|  |  Power BI Mobile: 모바일 보고서                         | |
|  |  Power BI Report Server: 온프렘 배포                    | |
|  +--------------------------------------------------------+ |
+-------------------------------------------------------------+
```

### DAX 핵심 패턴

#### CALCULATE: 필터 컨텍스트 조작

```dax
// 기본 패턴: CALCULATE(집계, 필터1, 필터2, ...)
서울 매출 = CALCULATE([총 매출], '지역'[지역] = "서울")

// 모든 필터 제거
전체 매출 = CALCULATE([총 매출], ALL('날짜'))

// 전년 동기 대비
전년 매출 = CALCULATE([총 매출], SAMEPERIODLASTYEAR('날짜'[Date]))

// YTD (Year-to-Date)
YTD 매출 = TOTALYTD([총 매출], '날짜'[Date])
```

#### 시간 인텔리전스 함수

| 함수 | 용도 |
|:---|:---|
| `SAMEPERIODLASTYEAR` | 전년 동기 |
| `TOTALYTD / TOTALQTD / TOTALMTD` | 누적(연/분기/월) |
| `DATEADD` | n 기간 이전/이후 |
| `DATESINPERIOD` | 특정 기간 범위 |
| `PARALLELPERIOD` | 병렬 기간 비교 |

**📢 섹션 요약 비유**: CALCULATE는 <strong>조명 스포트라이트 조절기</strong>와 같다. 모든 데이터가 비추어지는 기본 상태에서 CALCULATE를 사용해 특정 부분(필터)만 집중 조명할 수 있다.

---

## Ⅲ. 비교 및 연결

### 데이터 저장 모드 비교

| 모드 | 설명 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| **Import** | 데이터를 Power BI 모델로 복사 | 최고 성능 | 갱신 필요 | 대용량, 복잡 계산 |
| **DirectQuery** | 쿼리할 때마다 소스 DB 직접 조회 | 항상 최신 | 성능 제한 | 실시간 요구 |
| <strong>Composite</strong> | Import + DirectQuery 혼합 | 유연성 | 복잡한 관리 | 일부 실시간 필요 |
| **Dual** | Import·DirectQuery 동시 가능 | 유연성 최대 | 복잡도 최대 | 집계 테이블과 함께 |

### Microsoft Fabric: Power BI의 미래

```
Microsoft Fabric (2023) = 통합 분석 플랫폼

  One Lake (단일 데이터 저장소)
       |
  +----+------------------------------------+
  |  Data Factory  |  Synapse   |  Power BI |
  |  (데이터 통합) |  (분석)    |  (시각화)  |
  +-----------------------------------------+

  특징:
  - 모든 데이터가 One Lake의 Delta Parquet 형식 저장
  - 복사 없이 각 서비스에서 직접 접근
  - 단일 과금 체계 (F-SKU)
  - 직물처럼 모든 서비스가 연결(Fabric 명칭 유래)
```

**📢 섹션 요약 비유**: Microsoft Fabric은 <strong>올인원 주방 시스템</strong>과 같다. 냉장고(Data Lake)·가스레인지(Data Factory)·오븐(Synapse)·식탁(Power BI)이 각각 따로 있던 것을 하나의 통합 주방으로 만들어, 요리의 모든 단계를 하나의 공간에서 처리한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 행 수준 보안 (RLS: Row-Level Security)

RLS는 사용자 역할에 따라 볼 수 있는 데이터 행을 제한하는 보안 기능:

```dax
// RLS 규칙 정의 (영업 담당자는 자기 지역 데이터만 접근)
[담당자] = USERPRINCIPALNAME()

// 또는 동적 RLS
[지역] IN VALUES(RELATED('담당자 지역 매핑'[지역]))
```

### 고급 개발 도구

| 도구 | 용도 |
|:---|:---|
| **DAX Studio** | DAX 쿼리 성능 분석, 모델 문서화 |
| **Tabular Editor** | 모델 개발, CI/CD, 배포 파이프라인 |
| <strong>ALM Toolkit</strong> | 모델 비교·병합 (Git Flow 지원) |
| <strong>Power BI Helper</strong> | 모델 문서 자동 생성 |

**📢 섹션 요약 비유**: DAX Studio는 <strong>쿼리 디버거</strong>와 같다. 차트가 느릴 때 DAX Studio로 어떤 쿼리가 얼마나 오래 걸리는지 분석하고 최적화할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### Power BI 도입 효과

| 영역 | 효과 |
|:---|:---|
| **비용 효율** | Tableau 대비 1/7 수준 비용으로 유사한 BI 능력 |
| **생태계 통합** | Microsoft 365 환경에서 Teams/SharePoint 내장 보고서 |
| <strong>데이터 민주화</strong> | Excel 사용자 -> Power BI 전환 학습 곡선 최소화 |
| **거버넌스** | Premium 워크스페이스 배포 파이프라인, RLS |

### 결론

Power BI는 <strong>비용 효율성·Microsoft 생태계 통합·AI 기능</strong>의 3가지 강점으로 엔터프라이즈 BI 시장의 주류가 되었다. DAX는 Excel 함수와 유사한 구조지만, 필터 컨텍스트 이해가 핵심이다. Microsoft Fabric으로의 전환은 데이터 플랫폼의 패러다임 변화를 의미하며, 시스템 설계는 이 통합 플랫폼 전략을 이해하고 클라우드 데이터 전략에 반영해야 한다.

**📢 섹션 요약 비유**: Power BI의 CALCULATE는 <strong>마법 지우개</strong>와 같다. 이미 색칠된 그림(현재 필터 컨텍스트)에서 특정 색깔(필터)만 지우거나(ALL), 새로운 색을 추가하여(FILTER) 원하는 부분만 강조할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAX | 계산 언어 | Data Analysis Expressions — 측정값·계산 컬럼 |
| CALCULATE | 핵심 DAX 함수 | 필터 컨텍스트 조작의 핵심 |
| Power Query | 데이터 변환 | M 언어 기반 300+ 커넥터 ETL |
| Import 모드 | 데이터 모드 | 복사 저장, 최고 성능 |
| DirectQuery | 데이터 모드 | 소스 직접 쿼리, 항상 최신 |
| RLS | 보안 기능 | 역할별 행 수준 데이터 필터 |
| Microsoft Fabric | 통합 플랫폼 | Power BI + Data Factory + Synapse |

### 📈 관련 키워드 및 발전 흐름도

```text
[DAX (Data Analysis Expressions)]
    |
    v
[CALCULATE (필터 조작)]
    |
    v
[Power Query (M 언어)]
    |
    v
[Import 모드 vs DirectQuery]
    |
    v
[Microsoft Fabric (통합 플랫폼)]
```

이 흐름도는 DAX (Data Analysis Expressions)에서 출발해 Microsoft Fabric (통합 플랫폼)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- Power BI는 <strong>Microsoft 레고 세트</strong>예요: Excel이라는 기본 레고에서 시작해서, Power BI를 더하면 훨씬 멋진 집(대시보드)을 만들 수 있어요.
- DAX의 CALCULATE는 "이 계산을 할 때 이 조건만 봐줘"라고 말하는 마법 주문이에요 — "서울 지역 매출만 계산해줘", "작년 같은 기간 매출을 계산해줘" 등이에요.
- Microsoft Fabric은 "데이터 수집·분석·시각화를 모두 한 곳에서 하는 통합 주방"이에요 — 여러 도구를 왔다 갔다 할 필요 없이 한 곳에서 모든 것을 처리할 수 있어요.
