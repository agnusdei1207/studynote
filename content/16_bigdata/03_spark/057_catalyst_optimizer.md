---
title: "Catalyst Optimizer"
date: "2024-03-23"
tags:
  - "studynote-bigdata"
weight: 57
---
## 핵심 인사이트 (3줄 요약)
- Catalyst는 Apache Spark SQL의 핵심 쿼리 최적화 엔진으로, Scala의 함수형 프로그래밍 특성을 활용해 쿼리 실행 계획을 자동으로 개선한다.
- 논리적 실행 계획을 물리적 실행 계획으로 변환하는 과정에서 Rule-based 및 Cost-based 최적화를 수행하여 분산 처리 성능을 극대화한다.
- 확장 가능한 구조를 가지고 있어, 데이터 소스 개발자들이 자신만의 최적화 규칙을 쉽게 추가할 수 있는 유연성을 제공한다.

### Ⅰ. 개요 (Context & Background)
- **정의**: Spark SQL과 DataFrame/Dataset API의 하단에서 작동하는 확장 가능한 쿼리 옵티마이저 프레임워크다.
- **배경**: 개발자가 작성한 SQL이나 DataFrame 코드는 항상 최적의 성능을 보장하지 않는다. Catalyst는 이를 분석하여 데이터 필터링 시점 최적화(Predicate Pushdown), 필요한 열만 선택(Projection Pruning) 등을 자동으로 수행한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Catalyst Optimization Pipeline ]

 (Unresolved)     (Resolved)      (Optimized)      (Physical)
 Logical Plan --> Logical Plan --> Logical Plan -->  Plans  --> [Code Generation]
      |               |               |               |              |
  [Analyzer]      [Catalyst]      [Optimizer]    [Cost Model]    [Tungsten]
      |               |               |               |              |
  Catalog info    Standard Rules   CBO/RBO        Selection       Java Bytecode
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 단계 | 주요 역할 | 최적화 예시 |
| :--- | :--- | :--- |
| **Analysis** | 메타데이터(Catalog)를 참조해 테이블/컬럼 존재 확인 | 잘못된 컬럼명 체크 및 바인딩 |
| **Logical Optimization** | 논리적인 관계 대수 최적화 (RBO) | Predicate Pushdown (필터링 우선 수행) |
| **Physical Planning** | 실제 실행 가능한 여러 계획 생성 및 CBO 적용 | Broadcast Join vs Shuffle Join 선택 |
| <strong>Code Generation</strong> | 런타임에 최적화된 Java 바이트코드 생성 | 전체 쿼리를 하나의 함수처럼 실행 (Whole-stage CodeGen) |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>CBO(Cost-Based Optimizer) 활성화</strong>: 데이터 통계 정보가 최신일 때 최적의 성능을 낸다. `ANALYZE TABLE` 명령을 통해 통계를 생성하면 Catalyst가 조인 순서를 더 지능적으로 결정한다.
- <strong>디버깅 전략</strong>: `explain(true)` 명령을 사용하면 분석 전(Parsed), 분석 후(Analyzed), 최적화 후(Optimized), 물리적(Physical) 계획을 모두 확인하여 병목 지점을 파악할 수 있다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- Catalyst 덕분에 Spark는 언어(Python, Scala, SQL)에 상관없이 동일한 고성능을 보장할 수 있게 되었다. 최근에는 기계 학습 모델을 쿼리 최적화에 도입하거나, 런타임 상황에 따라 계획을 수정하는 AQE(Adaptive Query Execution)와 결합되어 더욱 진화하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Apache Spark, Spark SQL
- **자식 개념**: RBO(Rule-Based), CBO(Cost-Based), Code Generation
- **연관 개념**: Tungsten 엔진, AQE, DataFrame API

### 📈 관련 키워드 및 발전 흐름도

```text
[논리 계획 (Logical Plan)]
    |
    v
[물리 계획 (Physical Plan)]
    |
    v
[Catalyst Optimizer (Catalyst Optimizer)]
    |
    v
[코드 생성 (Code Generation)]
```

이 흐름도는 논리 계획이 물리 계획을 거쳐 Catalyst Optimizer와 코드 생성으로 구체화되는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
- 우리가 시장에 가서 물건을 살 때, "어느 가게를 먼저 들러야 제일 빨리 끝날까?"를 미리 생각하는 똑똑한 비서예요.
- 어려운 수학 숙제를 할 때, 더 쉬운 풀이 방법이 없는지 찾아내서 계산 시간을 줄여준답니다.
- 이 비서 덕분에 우리가 어떻게 명령해도 컴퓨터는 가장 빠른 길로 일을 처리해요.
