+++
title = "476. OLAP(Online Analytical Processing) - 통찰을 만드는 집계의 힘"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 476
+++

# 476. OLAP(Online Analytical Processing) - 통찰을 만드는 집계의 힘

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OLAP은 대규모 데이터를 다양한 관점(차원)에서 **실시간으로 분석하고 집계하여, 전략적 의사결정에 필요한 통찰을 얻는 데이터 처리 방식**이다.
> 2. **가치**: 조인 성능을 극대화하기 위한 **비정규화(스타 스키마 등)** 모델을 사용하며, 대량의 데이터를 한꺼번에 읽어 들이는 읽기 중심(Read-heavy) 환경에 최적화되어 있다.
> 3. **융합**: 다차원 큐브(Cube) 기술과 데이터 웨어하우스(DW) 아키텍처가 융합되어, 드릴다운(Drill-down), 롤업(Roll-up) 등 지능형 분석 기능을 제공한다.

+++

### Ⅰ. OLAP의 핵심 특징

- **워크로드**: 복잡한 대량 조회 및 집계 연산 (SELECT 위주).
- **데이터 구조**: 비정규화된 다차원 모델 (Star/Snowflake Schema).
- **응답 속도**: 대량 데이터를 다루므로 초 단위 이상의 응답 시간 허용.
- **데이터 시점**: 과거의 이력 데이터(Historical Data) 분석에 집중.

+++

### Ⅱ. OLAP 분석 모델 시각화 (ASCII Model)

하나의 측정값(Fact)을 여러 각도(Dimension)에서 분석하는 구조입니다.

```text
[ OLAP Multi-dimensional Analysis ]

          (Time)
            ▲
            │      [ Fact: Sales ]
  (Product) ┼──▶ (Amount: 5,000) ◀── (Region)
            │
            ▼
          (Store)

  * Operations:
    - Drill-down: Year ──▶ Month (상세 분석) ✅
    - Roll-up:    City ──▶ Country (요약 분석) ✅
    - Slicing:    특정 제품만 잘라서 보기 ✅
```

+++

### Ⅲ. OLAP의 3대 유형

1. **MOLAP (Multidimensional)**: 데이터를 다차원 배열(Cube) 형태로 물리적으로 저장. 속도는 가장 빠름.
2. **ROLAP (Relational)**: 관계형 DB 테이블을 그대로 사용. 대용량 확장에 유리.
3. **HOLAP (Hybrid)**: 요약 데이터는 MOLAP, 상세 데이터는 ROLAP에 두는 절충안.

- **📢 섹션 요약 비유**: OLAP은 **'도서관의 통계 연보'**와 같습니다. 매일 책을 대출하고 반납하는 기록(OLTP)을 모아서, "작년 한 해 동안 어떤 장르의 책이 어느 연령대에게 가장 인기가 많았나?"를 분석하기 위해 미리 잘 정리해 둔 두꺼운 통계 책자와 같습니다. 당장의 거래보다는 '흐름'과 '의미'를 찾는 데 목적이 있습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Dimensional Modeling]**: OLAP을 위한 전용 설계 기법.
- **[Star Schema]**: OLAP 성능의 꽃.
- **[Decision Support System (DSS)]**: OLAP이 궁극적으로 지원하는 비즈니스 시스템.

📢 **마무리 요약**: **OLAP**은 데이터의 과거를 통해 미래를 봅니다. 복잡하게 얽힌 숫자들 속에서 다차원적인 시각으로 비즈니스의 정답을 찾아내는 지능형 분석의 정수입니다.