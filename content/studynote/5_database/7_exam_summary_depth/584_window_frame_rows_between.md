+++
title = "584. 윈도우 함수 ROWS BETWEEN - 정밀한 데이터 구간 연산"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 584
+++

# 584. 윈도우 함수 ROWS BETWEEN - 정밀한 데이터 구간 연산

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: `ROWS BETWEEN`은 윈도우 함수에서 현재 행을 기준으로 **계산에 포함될 물리적인 행의 범위를 더 세밀하게 지정하는 윈도우 프레임(Window Frame) 절**이다.
> 2. **가치**: 전체 파티션이 아닌 특정 구간(예: 앞의 2행부터 현재 행까지)에 대한 연산을 수행하여, **누적 합계(Running Total), 이동 평균(Moving Average)** 등 정교한 시계열 분석을 가능케 한다.
> 3. **융합**: `OVER`, `PARTITION BY`, `ORDER BY`와 융합되어, 데이터의 흐름 속에서 현재의 위치를 기반으로 한 동적 집계(Dynamic Aggregation)를 수행한다.

+++

### Ⅰ. ROWS BETWEEN의 주요 키워드와 문법

- **PRECEDING**: 현재 행보다 앞에 있는 행. (예: `1 PRECEDING` ──▶ 직전 1개 행)
- **FOLLOWING**: 현재 행보다 뒤에 있는 행. (예: `1 FOLLOWING` ──▶ 다음 1개 행)
- **CURRENT ROW**: 현재 행 그 자체.
- **UNBOUNDED**: 파티션의 시작(`UNBOUNDED PRECEDING`) 또는 끝(`UNBOUNDED FOLLOWING`).

+++

### Ⅱ. 누적 합계 및 이동 평균 연산 시각화 (ASCII Model)

```text
[ Moving Average (3 Rows Window) ]
  Calculation: (Prev + Prev + Current) / 3

  Data Row | Value | Window Frame Logic                     | Result
  ---------|-------|----------------------------------------|--------
    Row 1  |  10   | [10]                                   |  10.0
    Row 2  |  20   | [10, 20]                               |  15.0
    Row 3  |  30   | [10, 20, 30] ✅ (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
    Row 4  |  40   | [20, 30, 40] ✅ (Frame slides down)    |  30.0
```

+++

### Ⅲ. 실무 활용 사례

1. **누적 합계 (Running Total)**:
   - `SUM(Sales) OVER(ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`
   - 날짜순으로 지금까지의 매출을 모두 더해나갈 때 사용합니다.
2. **이동 평균 (Moving Average)**:
   - `AVG(Stock_Price) OVER(ORDER BY Time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)`
   - 최근 5일간의 주가 평균을 구해 변동성을 분석할 때 사용합니다. ✅
3. **이상치 제거**:
   - 현재 행의 앞뒤 행들과의 차이를 계산하여 갑작스러운 데이터 튐(Spike) 현상을 탐지합니다.

- **📢 섹션 요약 비유**: `ROWS BETWEEN`은 **'데이터로 만든 움직이는 돋보기'**와 같습니다. 우리가 한 줄 한 줄 데이터를 읽어 내려가면서, 그 옆에 있는 돋보기의 크기(프레임 범위)를 조절하는 것입니다. 돋보기를 통해 보이는 범위 안의 숫자들만 쏙쏙 골라 더하거나 평균을 내어 현재 내 위치 옆에 기록해 두는 아주 편리하고 정밀한 작업 도구입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Window Frame]**: 윈도우 함수가 계산을 수행하는 구체적인 행들의 부분 집합.
- **[RANGE vs ROWS]**: 값이 같은 행을 하나로 묶느냐(Range) 아니면 무조건 물리적 행 단위로 쪼개느냐(Rows)의 차이.
- **[Analytical SQL]**: 윈도우 함수를 통해 실현되는 고차원 분석 쿼리.

📢 **마무리 요약**: **ROWS BETWEEN**은 윈도우 함수의 디테일을 완성합니다. 파티션이라는 큰 틀 안에서 '구간'의 논리를 세움으로써, 데이터의 연속된 흐름 속에서 유의미한 패턴을 찾아내게 돕습니다.