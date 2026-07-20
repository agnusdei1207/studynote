---
title: "Spark 35 Improvements"
date: "2026-04-29"
tags:
  - "studynote-bigdata"
weight: 75
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Spark 3.5는 2023년 릴리스되어 Python API (PySpark)의 기능 강화, Spark Connect (원격 클라이언트 연결), ANSI SQL 지원 확대, 구조화된 스트리밍(Structured Streaming) 고도화를 통해 데이터 엔지니어링·ML 워크플로우의 생산성과 이식성을 높인 메이저 버전이다.
> 2. **가치**: Spark Connect는 Spark 서버에 경량 클라이언트로 원격 접속하여 Jupyter Notebook·로컬 IDE에서 클러스터 Spark를 직접 활용할 수 있게 하여 개발 경험(DX)을 대폭 향상시키며, Python UDTF (User-Defined Table Function)와 PyArrow 기반 최적화로 PySpark 성능 격차를 줄였다.
> 3. **판단 포인트**: Spark 3.5의 ANSI 모드 강화는 기존 Spark 코드와의 호환성 이슈를 일으킬 수 있다 — 기존 코드에서 NULL 처리·정수 오버플로우 등 ANSI 미준수 동작에 의존했다면 마이그레이션 전 회귀 테스트가 필수다.

---

## Ⅰ. 개요 및 필요성

Apache Spark 3.5는 Spark 3.x 시리즈의 주요 기능 업데이트로, 사용 편의성·성능·SQL 표준 준수를 중점적으로 개선했다.

```text
+----------------------------------------------------------+
|          Spark 3.5 핵심 개선 영역                          |
+----------------------------------------------------------+
|  1. Spark Connect — 경량 원격 클라이언트 연결               |
|  2. Python UDTF — 테이블 반환 Python 함수                  |
|  3. ANSI SQL 강화 — 표준 SQL 호환성 확대                   |
|  4. Structured Streaming — 상태 관리 고도화                |
|  5. PySpark + PyArrow — 데이터 교환 성능 향상              |
|  6. Spark SQL 함수 확장 — 300+ 신규 함수 추가              |
+----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Spark 3.5는 자동차의 대형 서비스다. 엔진(코어 처리) 튜닝, 내비게이션(SQL) 업그레이드, 원격 시동(Spark Connect), 연비 개선(PyArrow)이 동시에 이루어졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Spark Connect 아키텍처

```text
[로컬 Python/Notebook 클라이언트]
         | gRPC 연결 (Protocol Buffers)
         v
[Spark Connect Server (클러스터)]
         |
         v
[Spark 드라이버 -> 익스큐터]
```

Spark Connect 이전: 드라이버 JVM에 직접 연결 (언어 의존성, 버전 충돌).
Spark Connect 이후: 임의 언어 클라이언트에서 안정적 원격 접속.

### Python UDTF (User-Defined Table Function)

```python
# Spark 3.5: Python UDTF — 1행 -> 여러 행 반환
from pyspark.sql.functions import udtf

@udtf(returnType="num: int, squared: int")
class SquaredNumbers:
    def eval(self, n: int):
        for i in range(n):
            yield i, i ** 2

spark.udtf.register("squared", SquaredNumbers)
spark.sql("SELECT * FROM squared(5)").show()
```

- **📢 섹션 요약 비유**: UDTF는 마법 복사기다. 입력 1줄을 넣으면 여러 줄의 결과를 만들어낸다. 기존 UDF(1->1)와 달리 UDTF(1->n)는 데이터를 확장(Explode)하는 함수다.

---

## Ⅲ. 비교 및 연결

| 버전 | 주요 특징 |
|:---|:---|
| **Spark 2.x** | DataFrame API, Spark SQL, ML lib |
| **Spark 3.0** | AQE(Adaptive Query Execution), 동적 파티션 프루닝 |
| **Spark 3.4** | Spark Connect 프리뷰, ANSI 강화 시작 |
| **Spark 3.5** | Spark Connect GA, Python UDTF, Streaming 고도화 |
| **Spark 4.0 (예정)** | Python-first API, 추가 통합 |

AQE (Adaptive Query Execution, 적응형 쿼리 실행)는 Spark 3.0에서 도입되어 런타임 통계 기반으로 실행 계획을 동적으로 재최적화하는 기능으로, 3.5에서 더욱 안정화되었다.

- **📢 섹션 요약 비유**: AQE는 GPS 내비게이션의 실시간 경로 재탐색이다. 출발 전(컴파일 타임)에 최적 경로를 계획하지만, 실제 도로 상황(런타임 통계)에 따라 실시간으로 경로를 변경한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오: Spark Connect 기반 노트북 개발 환경 구축
데이터 과학 팀의 Jupyter Notebook에서 원격 Spark 클러스터 직접 활용.

1. **기존**: 각 노트북 서버에 Spark 드라이버 설치, 버전 관리 복잡.
2. **Spark Connect 도입**: Databricks/EMR Spark Connect Server 활성화.
3. **클라이언트**: `pip install pyspark[connect]` 로컬 설치.
4. **연결**: `SparkSession.builder.remote("sc://spark-server:15002").getOrCreate()`.
5. **결과**: 로컬 Python 3.11 + 클러스터 Spark 3.5 독립적 버전 관리 가능.

### 안티패턴
- Spark 3.5로 업그레이드 시 ANSI 모드 변경으로 인한 기존 코드 동작 차이를 간과하는 안티패턴. 예를 들어 Spark 3.4 이전에서 `1/0`이 Infinity 반환 -> 3.5 ANSI 모드에서 ArithmeticException 발생. 마이그레이션 전 전체 파이프라인 회귀 테스트가 필수다.

- **📢 섹션 요약 비유**: Spark 버전 업그레이드는 건물 리모델링이다. 구조(API)는 대부분 그대로지만, 전기 배선(ANSI 동작)이 바뀌어 기존 가전(코드)이 작동 안 할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **개발 편의성** | Spark Connect로 원격 클라이언트 지원 |
| <strong>Python 호환성</strong> | Python UDTF, PyArrow 통합 강화 |
| **SQL 표준화** | ANSI 준수 -> 타 DB 이식성 향상 |

Spark 4.0은 Python-first 설계로 Scala API와 동등한 Python API를 목표로 하며, DataFrame API와 Dataset API의 Python 통합 강화가 예정되어 있다. Lakehouse 아키텍처(Delta Lake, Iceberg)와의 더 긴밀한 통합도 예고되어 있다.

- **📢 섹션 요약 비유**: Spark 3.5는 데이터 처리 도구상자의 최신 업그레이드다. 더 날카로운 도구(Python UDTF), 더 편한 손잡이(Spark Connect), 더 정확한 눈금(ANSI SQL)이 추가되어 장인(데이터 엔지니어)의 작업 효율이 높아진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Spark Connect** | 경량 원격 클라이언트 연결; 개발 편의성 핵심 |
| **AQE** | 런타임 적응형 쿼리 최적화; Spark 3.0+ |
| **Python UDTF** | 1행->다행 반환 Python 함수; 3.5 신규 |
| **ANSI SQL** | 표준 SQL 준수 강화; 호환성 이슈 주의 |
| **Spark 4.0** | Python-first API; 차세대 버전 방향 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Spark 2.x — DataFrame API, SparkSQL 기반 확립]
    |
    v
[Spark 3.0 — AQE, 동적 파티션 프루닝 도입]
    |
    v
[Spark 3.4 — Spark Connect 프리뷰, ANSI 강화]
    |
    v
[Spark 3.5 — Spark Connect GA, Python UDTF, Streaming^]
    |
    v
[Spark 4.0 — Python-first, Lakehouse 통합 강화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Spark 3.5는 슈퍼컴퓨터(클러스터)에 노트북(Spark Connect)으로 원격 접속해 쓸 수 있게 업그레이드된 것이에요!
2. Python으로 수십억 개의 데이터를 처리하는 함수(UDTF)를 쉽게 만들 수 있고, SQL도 더 표준에 맞게 바뀌었어요.
3. 이 업그레이드 덕분에 데이터 엔지니어들이 더 빠르고 편하게 빅데이터를 처리할 수 있답니다!
