---
title: "Descriptive Statistics"
date: "2025-05-22"
tags:
  - "studynote-bigdata"
weight: 100
---
## 핵심 인사이트 (3줄 요약)
- <strong>기술 통계 (Descriptive Statistics)</strong>: 수집된 데이터의 전체적인 특징을 요약하고 설명하기 위해 평균, 분산, 분포 등을 산출하는 기초 통계 방법론.
- <strong>데이터 가시화</strong>: 숫자로 된 대규모 데이터를 중심 경향성(Central Tendency)과 산포도(Dispersion) 지표로 압축하여 데이터의 '모양'을 파악함.
- **분석의 기초**: 추론 통계로 나아가기 전, 데이터의 이상치(Outlier)를 확인하고 변수의 성질을 이해하는 데이터 과학의 필수 관문.

### Ⅰ. 개요 (Context & Background)
수백만 건의 원시 데이터(Raw Data) 자체는 인간이 해석하기 어렵습니다. 기술 통계는 이러한 방대한 정보를 몇 개의 대표적인 수치와 그래프로 요약하여, 데이터가 무엇을 말하고 있는지 직관적으로 전달하는 역할을 합니다. 이는 모든 빅데이터 분석 및 기계 학습 모델링의 출발점입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
기술 통계의 주요 측정 지표와 데이터 요약 프로세스 아키텍처입니다.

```text
[ Descriptive Statistics Architecture Map ]

         Raw Data Pool (ZB Scale)
                |
                v
+---------------------------------------+
|      [ Data Summary Metrics ]         |
|                                       |
| 1. Central Tendency (중심 경향성)     |
|    - Mean, Median, Mode               |
|                                       |
| 2. Dispersion / Variability (산포도)  |
|    - Variance, Std Dev, IQR, Range    |
|                                       |
| 3. Shape / Distribution (분포/모양)   |
|    - Skewness (왜도), Kurtosis (첨도) |
+---------------------------------------+
                |
                v
+---------------------------------------+
|      [ Visualization Methods ]        |
|  (Histogram, Box Plot, Scatter Plot)  |
+---------------------------------------+
```

**핵심 원리:**
1. **중심 경향성**: 데이터가 어디에 모여 있는가? (평균은 이상치에 민감하므로 중앙값과 함께 고려).
2. **산포도**: 데이터가 얼마나 퍼져 있는가? (표준편차가 클수록 데이터의 불확실성이 높음).
3. **분포의 비대칭성**: 왜도(Skewness)가 양수면 왼쪽으로 치우친(긴 꼬리가 오른쪽) 형태이며, 이는 데이터 전처리(로그 변환 등)의 근거가 됨.
4. **IQR (Interquartile Range)**: 데이터의 중간 50% 범위를 의미하며, 박스 플롯(Box Plot)을 통해 이상치를 정의하는 기준이 됨.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 기술 통계 (Descriptive) | 추론 통계 (Inferential) |
| :--- | :--- | :--- |
| **목적** | 데이터 설명 및 요약 | 표본을 통한 모집단 특성 예측 |
| **결과물** | 평균, 도표, 그래프 | p-value, 신뢰구간, 가설 채택 |
| **범위** | 현재 보유한 데이터 전체 | 불확실성을 포함한 전체 모집단 |
| **수행 시점** | 분석 초기 (EDA 단계) | 분석 중기 (가설 검정 단계) |
| **핵심 질문** | "데이터가 어떻게 생겼는가?" | "이 결과가 우연이 아닌가?" |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
* <strong>적용 전략 (Implementation Strategy)</strong>:
  * <strong>이상치 탐지</strong>: 기술 통계 산출 시 평균과 중앙값의 차이가 크다면 이상치 존재를 의심하고, Box Plot의 Whisker를 벗어나는 데이터에 대한 정제 로직(Capping, Trimming) 적용.
  * <strong>데이터 스케일링</strong>: 분포(왜도/첨도)를 확인하여 정규 분포를 따르지 않는 경우 정규화(Normalization)를 통해 ML 모델의 학습 효율 극대화.
* **실무적 판단 (Architectural Judgment)**:
  * 빅데이터 환경에서는 극단적인 이상치 하나가 전체 평균을 왜곡하기 쉬움. 따라서 단순 평균(Arithmetic Mean)보다는 절사 평균(Trimmed Mean)이나 중앙값(Median)을 대표값으로 설정하는 견고한(Robust) 분석 설계가 필요함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
기술 통계는 데이터에 대한 '객관적인 요약본'을 제공하여 의사결정의 편향을 방지합니다. 향후에는 수조 개의 행을 가진 초거대 데이터셋에서도 실시간으로 기술 통계 지표를 계산하고 시각화하는 스트리밍 통계 기술(Sketching algorithms 등)이 플랫폼의 핵심 경쟁력이 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **기초 통계**: Mean/Median/Mode, Variance/Standard Deviation
* **분포 분석**: Normal Distribution, Skewness/Kurtosis, Z-Score
* <strong>시각화 도구</strong>: Histogram, Box-and-Whisker Plot, Five-number Summary

### 📈 관련 키워드 및 발전 흐름도

```text
[기초 통계]
    |
    v
[분포 분석]
    |
    v
[상관 분석]
    |
    v
[시각화 도구]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 우리 반 친구들의 키를 일일이 다 말하는 대신, "우리 반 평균 키는 140cm야"라고 짧게 줄여 말하는 것이 기술 통계예요.
2. 키가 제일 큰 친구와 작은 친구의 차이가 얼마나 나는지도 알려주면 우리 반의 특징을 더 잘 알 수 있죠.
3. 복잡한 관찰 일기를 사진 한 장으로 요약해서 보여주는 것과 같답니다.
