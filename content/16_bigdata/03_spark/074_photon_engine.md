---
title: "Photon Engine"
date: "2026-04-29"
tags:
  - "studynote-bigdata"
weight: 74
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Photon 엔진은 Databricks가 개발한 C++ 기반 네이티브 벡터화 실행 엔진(Vectorized Execution 엔진)으로, Apache Spark의 JVM(Java Virtual Machine) 오버헤드를 제거하고 CPU SIMD (Single Instruction Multiple Data) 명령어를 활용하여 SQL/데이터프레임 연산을 최대 12배 가속화한다.
> 2. **가치**: Photon은 Databricks Runtime에 투명하게 통합되어 기존 Spark SQL 코드 변경 없이 I/O 집약적 ETL(Extract-Transform-Load), 대용량 집계(Aggregation), 조인(Join) 연산의 처리량을 대폭 향상시키고 클라우드 컴퓨팅 비용을 절감한다.
> 3. **판단 포인트**: Photon은 CPU 계산 집약적 연산(필터, 정렬, 해시 집계)에서 극적인 성능 향상을 보이지만, UDF (User-Defined Function, 사용자 정의 함수)나 Python 기반 연산은 여전히 JVM으로 폴백되므로 Photon 이점을 극대화하려면 네이티브 SQL/DataFrame API 사용이 필수다.

---

## Ⅰ. 개요 및 필요성

Photon 엔진은 Databricks가 2021년 공개한 C++ 네이티브 쿼리 실행 엔진으로, Apache Spark의 기본 Tungsten 실행 엔진을 대체하는 Databricks Runtime의 핵심 가속화 구성 요소다.

Spark는 JVM 위에서 실행되기 때문에 가비지 컬렉션(GC, Garbage Collection) 오버헤드, JIT(Just-In-Time) 컴파일 지연, 객체 직렬화 비용이 누적되어 CPU 효율이 저하된다. 특히 최신 클라우드 서버의 64코어 CPU와 NVMe SSD의 성능을 JVM이 100% 활용하지 못하는 것이 핵심 문제였다. Photon은 C++로 직접 하드웨어를 제어하여 이 격차를 메운다.

```text
+--------------------------------------------------------------+
|            Spark JVM vs Photon 실행 경로 비교                  |
+--------------------------------------------------------------+
|                                                              |
|  [기존 Spark (Tungsten)]                                     |
|  SQL/DF API -> Catalyst 최적화 -> JVM 바이트코드 생성           |
|  -> JVM 실행 (GC 부담, 객체 직렬화 오버헤드)                   |
|                                                              |
|  [Photon Engine]                                             |
|  SQL/DF API -> Catalyst 최적화 -> Photon C++ 코드 생성          |
|  -> CPU SIMD 벡터 명령어 직접 실행 (GC 없음, 네이티브 성능)     |
|                                                              |
|  성능 향상:                                                   |
|  +- 해시 집계: 최대 8배                                       |
|  +- 정렬: 최대 4배                                            |
|  +- 조인: 최대 12배                                           |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: JVM 위에서 Spark를 실행하는 것은 번역가(JVM)를 통해 지시하는 것이고, Photon은 현지어(C++)로 직접 말하는 것과 같다. 번역 과정이 없으니 지시가 즉각 전달되어 훨씬 빠르게 일한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 벡터화 실행(Vectorized Execution)의 원리

Photon의 핵심은 컬럼형(Columnar) 배치 처리와 SIMD 명령어 활용이다.

| 처리 방식 | 단위 | CPU 명령 | 성능 |
|:---|:---|:---|:---|
| **행 단위(Row-at-a-time)** | 1 행씩 처리 | 스칼라 연산 | 느림 |
| **벡터화(Vectorized)** | 1024행 배치 처리 | SIMD (AVX-512) | 최대 16배 빠름 |

```text
+----------------------------------------------------------+
|              벡터화 실행 vs 행 단위 실행                   |
+----------------------------------------------------------+
|                                                          |
|  행 단위:  [행1] -> 연산 -> [행2] -> 연산 -> [행3] -> ...      |
|            (루프 오버헤드 × 행 수)                         |
|                                                          |
|  벡터화:   [행1,행2,...,행1024] -> SIMD 1번 연산           |
|            (CPU 레지스터에 1024개 동시 처리)               |
|                                                          |
|  AVX-512: 512비트 레지스터 = 8개 double 동시 처리          |
+----------------------------------------------------------+
```

### Photon 지원 연산 vs 폴백

| Photon 지원 (빠름) | JVM 폴백 (기존 속도) |
|:---|:---|
| SELECT, WHERE, GROUP BY, ORDER BY | Python UDF, Pandas UDF |
| Hash Join, Sort Merge Join | ML 라이브러리 내부 연산 |
| COUNT, SUM, AVG, MIN, MAX | 스트리밍 상태 저장(Stateful) |
| Delta Lake 읽기/쓰기 | 복잡한 중첩 구조 타입 일부 |

- **📢 섹션 요약 비유**: Photon은 공장에서 1개씩 용접하던 것을 1024개를 한 번에 찍는 금형으로 바꾼 것과 같다. 같은 재료(데이터)를 훨씬 빠른 속도로 처리하지만, 특수 주문(Python UDF)은 여전히 손으로 한다.

---

## Ⅲ. 비교 및 연결

| 엔진 | 언어 | 벡터화 | Spark 호환 | 주요 플랫폼 |
|:---|:---|:---|:---|:---|
| **Photon** | C++ | ✅ (AVX-512) | ✅ (Databricks) | Databricks |
| **Spark Tungsten** | JVM | 부분적 | ✅ | Apache Spark |
| **DuckDB** | C++ | ✅ | ❌ | 단일 노드 분석 |
| **Velox** | C++ | ✅ | 일부 | Meta, Presto |
| **Apache Arrow** | C++ | ✅ (컬럼형 포맷) | ✅ (PySpark) | 크로스 플랫폼 |

Photon은 Delta Lake (오픈 테이블 포맷)와 긴밀하게 통합되어 Delta Lake의 데이터 스킵(Data Skipping)·Z-Ordering과 결합 시 I/O와 CPU 비용을 동시에 절감하는 시너지를 발휘한다.

- **📢 섹션 요약 비유**: Photon은 Ferrari 엔진(C++ 성능), Spark API는 자동차 핸들(사용 편의성)이다. 엔진을 교체해도 핸들 조작법은 동일하므로 운전자(개발자)는 코드 변경 없이 속도 향상을 누린다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오: 일 단위 대규모 ETL 비용 최적화
일 1TB의 로그 데이터를 집계하는 Databricks ETL 잡의 클라우드 비용이 과다하다.

1. **현황**: Spark 기본 설정 (Tungsten), DBU(Databricks Unit) 비용 월 $50,000.
2. **Photon 활성화**: Databricks Runtime에서 Photon 옵션 활성화 (코드 변경 없음).
3. **병목 분석**: GROUP BY + 집계 연산이 전체 실행 시간의 60% 차지.
4. **결과**: 집계 연산 8배 가속 -> 전체 잡 시간 50% 단축 -> DBU 비용 45% 절감.
5. **추가 최적화**: Python UDF를 SQL 네이티브 함수로 교체 -> 추가 20% 단축.

### 체크리스트
- Databricks Runtime 9.1 LTS 이상에서 Photon 지원 (클러스터 설정에서 활성화).
- `EXPLAIN` 명령으로 실행 계획 내 Photon 연산자 포함 여부 확인.
- Python UDF 최소화 — 가능하면 `pyspark.sql.functions` 네이티브 함수 사용.

### 안티패턴
- Photon을 활성화한 후 Python UDF가 포함된 쿼리의 성능이 개선됐다고 착각하는 오류. Python UDF 단계는 여전히 JVM 폴백이 발생하며, Photon의 이점은 네이티브 SQL/DF 연산 구간에서만 적용된다. 실행 계획을 반드시 확인해야 한다.

- **📢 섹션 요약 비유**: Photon을 켜놓고 Python UDF를 계속 쓰는 건, 고속도로에 포르쉐를 올려놓고 속도 제한 구간(UDF)에서 계속 서행하는 것과 같다. 고속 구간(네이티브 SQL)에서만 진가를 발휘한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| <strong>ETL 속도 향상</strong> | 집계·조인 연산 가속 | 최대 12배 향상 |
| **비용 절감** | 잡 실행 시간 단축 -> DBU 절감 | 40~50% 절감 |
| **코드 변경 없음** | 기존 Spark SQL 그대로 | 마이그레이션 비용 0 |

Photon은 Databricks Lakehouse 아키텍처의 핵심 성능 레이어로, Unity Catalog와의 통합으로 보안 접근 제어(ABAC)와 고성능 실행을 동시에 달성하는 방향으로 발전하고 있다. 오픈소스 진영의 Velox와 Apache Gluten 프로젝트가 유사한 C++ 네이티브 실행 가속을 Apache Spark에 이식하는 경쟁이 활발하다.

- **📢 섹션 요약 비유**: Photon 엔진은 스포츠카에 터보 엔진을 달아주는 것이다. 차의 겉모습(API)은 그대로지만, 내부 엔진(C++ 벡터화)이 바뀌면서 같은 연료(데이터)로 훨씬 빠르게 목적지에 도달한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Apache Arrow** | 컬럼형 인메모리 포맷; Photon의 데이터 교환 기반 |
| <strong>SIMD (벡터 명령어)</strong> | Photon이 1024행을 동시 처리하는 CPU 수준 병렬화 |
| <strong>Delta Lake</strong> | Photon과 통합된 오픈 테이블 포맷; 데이터 스킵 최적화 |
| **Velox** | Meta의 오픈소스 C++ 벡터화 엔진; Photon의 오픈소스 대안 |
| **JVM GC** | Photon이 제거한 Java 메모리 관리 오버헤드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Apache Spark Tungsten — JVM 기반 코드 생성, 부분 최적화]
    |
    v
[Apache Arrow — 컬럼형 포맷, 언어 간 제로카피 교환]
    |
    v
[Photon Engine (2021) — C++ 네이티브 벡터화 실행]
    |
    v
[Delta Lake + Photon 통합 — I/O + CPU 동시 최적화]
    |
    v
[Velox / Apache Gluten — 오픈소스 생태계 C++ 실행 가속]
```
JVM 기반 Tungsten에서 컬럼형 Arrow, C++ Photon을 거쳐 오픈소스 Velox/Gluten으로 확장되는 빅데이터 실행 엔진 가속화의 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. Photon 엔진은 자동차 엔진을 낡은 것에서 <strong>슈퍼카 엔진</strong>으로 바꿔주는 것과 같아요!
2. 자동차 겉모습(코드)은 그대로인데, 엔진만 바꿨더니 같은 길을 10배나 빠르게 달릴 수 있게 돼요.
3. 덕분에 수억 개의 데이터를 처리하는 시간이 확 줄어들고, 클라우드 비용도 많이 절약할 수 있답니다!
