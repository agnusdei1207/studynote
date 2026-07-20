---
title: "Delta Lakehouse Time Travel Transaction"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 177
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Delta Lakehouse는 Parquet 같은 오픈 파일 위에 Delta Log를 더해 ACID (Atomicity, Consistency, Isolation, Durability) 테이블 스냅샷을 만드는 방식이다.
> 2. **가치**: Time Travel은 과거 버전 조회와 `RESTORE`를 가능하게 해 배치 오류 복구, 감사, Machine Learning (ML) 재현성을 동시에 높인다.
> 3. **판단 포인트**: Delta의 강점은 `MERGE`·업서트와 Spark 생태계지만, 실제 복원 가능 기간은 `RETENTION`·`VACUUM` 정책에 달려 있으므로 저장 비용·엔진 호환성·운영 규칙을 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

Delta Lakehouse는 객체 스토리지나 분산 파일시스템 위의 데이터를 "파일 묶음"이 아니라 "버전이 있는 테이블"로 다루게 만드는 레이크하우스 프로토콜이다. 기존 데이터 레이크는 저장 비용이 낮고 포맷이 개방적이라는 장점이 있었지만, 여러 개의 Parquet 파일이 하나의 논리 테이블을 이룰 때 동시 쓰기·부분 실패·스키마 변경을 안전하게 다루기 어렵다는 약점이 있었다.

특히 분석 파이프라인이 `append only`가 아니라 `update`, `delete`, Change Data Capture (CDC), 재처리를 요구하는 순간 문제가 선명해진다. 파일 하나를 새로 쓰는 것은 쉽지만, "테이블 전체가 어느 시점에 일관된 상태였는가"를 보장하기는 어렵다. Data Warehouse처럼 신뢰성을 원하면서도 Data Lake처럼 개방성과 확장성을 유지하려다 보니 Delta Lakehouse 같은 테이블 포맷이 등장했다.

```text
+--------------------------------------------------------------+
| Plain Parquet Lake의 난점                                    |
+--------------------------------------------------------------+
| Writer A : part-001, part-002 갱신 중                        |
| Writer B : part-003 삭제 반영                                |
| Reader   : 어떤 파일 집합이 같은 시점 snapshot인지 불명확     |
|                                                              |
| 파일 저장은 쉬워도 테이블 단위 commit / rollback은 약하다     |
+--------------------------------------------------------------+
```

이 구조에서는 "어제 오전 9시 기준 데이터로 다시 학습해 달라" 같은 요구가 매우 비싸다. 결국 별도 스냅샷을 복제하거나 수동 백업을 보관해야 하고, 그만큼 저장 비용과 운영 복잡도가 늘어난다. Delta의 Time Travel은 이 문제를 테이블 수준 버전 관리로 흡수한다.

- **📢 섹션 요약 비유**: 일반 데이터 레이크가 종이 문서 더미라면, Delta Lakehouse는 날짜별 수정 이력이 붙은 문서철과 같다. 파일은 그대로 두되 어떤 묶음이 정식 버전인지 명확히 알려 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Delta 테이블의 실체는 `data files + _delta_log` 조합이다. 실제 레코드는 Parquet 파일에 있고, `_delta_log`에는 어떤 파일이 현재 테이블에 포함되는지, 어떤 파일이 제거되었는지, 스키마와 파티션이 무엇인지가 순서대로 기록된다. 즉 Delta는 저장 포맷을 바꾸는 기술이라기보다, 오픈 파일 위에 트랜잭션 메타데이터 계층을 올리는 기술이다.

| 로그 레코드 | 의미 | 왜 중요한가 |
| :--- | :--- | :--- |
| `add` | 새 데이터 파일 경로와 통계 추가 | 스냅샷 구성, Data Skipping에 사용 |
| `remove` | 더 이상 유효하지 않은 파일 표시 | `DELETE`, `UPDATE`, `MERGE` 구현 |
| `metaData` | 스키마, 파티션, 속성 정의 | 스키마 강제와 진화 기준 |
| `protocol` | reader/writer 최소 버전 선언 | 엔진 호환성 보장 |
| `txn` / `commitInfo` | 작업 종류, 앱 ID, 커밋 시간 기록 | 스트리밍 멱등성과 감사 추적 |

아래 흐름은 Delta의 커밋과 스냅샷 재구성이 어떻게 이뤄지는지 보여준다. 핵심은 새 파일을 먼저 쓰고, 마지막에 커밋 로그를 올리는 <strong>낙관적 동시성 제어(Optimistic Concurrency Control)</strong>다. 커밋 전까지 독자는 이전 버전만 보고, 커밋이 성공한 뒤에만 새 버전을 본다.

```text
+-------------------- Delta Commit --------------------+
| 1. New Parquet files written                         |
| 2. Read current table version N                      |
| 3. Conflict check (optimistic concurrency)           |
| 4. Commit _delta_log/000...N+1.json                  |
| 5. Readers jump atomically from snapshot N to N+1    |
+------------------------------------------------------+

snapshot v127 = checkpoint v120.parquet + 121.json ... 127.json
```

체크포인트(checkpoint)는 로그가 끝없이 길어지는 문제를 줄인다. 일정 버전마다 Parquet 형식의 체크포인트를 만들어 두면, 독자는 오래된 JSON 로그를 처음부터 재생하지 않고 최근 체크포인트 이후만 읽어 빠르게 스냅샷을 복원할 수 있다. 이것이 대용량 테이블에서도 Time Travel이 실제로 가능해지는 이유다.

```sql
SELECT * FROM sales VERSION AS OF 314;
SELECT * FROM sales TIMESTAMP AS OF '2026-04-21 09:00:00';
RESTORE TABLE sales TO VERSION AS OF 313;
```

다만 중요한 함정이 있다. Time Travel은 로그만 있으면 되는 기능이 아니라, 해당 버전이 가리키는 실제 데이터 파일도 남아 있어야 한다. `VACUUM`으로 오래된 파일을 삭제하면 과거 버전의 논리 정보는 있어도 물리 파일이 없어 복원이 불가능해질 수 있다.

- **📢 섹션 요약 비유**: Delta Log는 문서 수정 이력을 적는 장부이고, 체크포인트는 중간 저장된 완성본이다. 장부만 길게 쌓아 두지 않고 중간 완성본을 남겨야 원하는 시점으로 빨리 돌아갈 수 있다.

---

## Ⅲ. 비교 및 연결

Delta를 이해할 때는 Apache Iceberg, Apache Hudi와 함께 보는 편이 경계를 잡기 쉽다. 세 기술 모두 오픈 저장소 위에 테이블 의미론을 부여하지만, 메타데이터 구조와 강점이 다르다. Delta는 Spark/Databricks 환경에서 `MERGE`, Change Data Feed (CDF), 운영 편의성이 강하고, Iceberg는 멀티 엔진 카탈로그와 파티션 진화에 강하며, Hudi는 스트리밍 업서트와 증분 처리에 강하다.

| 항목 | Delta Lake | Apache Iceberg | Apache Hudi |
| :--- | :--- | :--- | :--- |
| 메타데이터 방식 | Append Log + Checkpoint | Snapshot Manifest Tree | Timeline + COW/MOR |
| 강점 | `MERGE`, CDF, Spark 최적화 | 멀티 엔진, 히든 파티셔닝 | CDC·업서트·스트리밍 적재 |
| 잘 맞는 상황 | 업데이트가 많은 레이크하우스 | Trino·Spark·Flink 혼합 환경 | 실시간 변경 반영 비중이 큰 환경 |
| 주의점 | 보존 정책과 생태계 의존성 | 카탈로그 설계 학습 비용 | 읽기/쓰기 모드 복잡성 |

Time Travel도 백업과 같은 의미는 아니다. Time Travel은 <strong>테이블 단위 운영 복구</strong>에 강하고, 백업은 <strong>재해 복구와 장기 보존</strong>에 강하다. 예를 들어 잘못된 `DELETE`나 품질 사고에는 Delta의 `RESTORE`가 빠르지만, 리전 전체 손실이나 저장소 오염까지 커버하려면 별도 백업 전략이 필요하다.

또 Delta는 Medallion Architecture와도 잘 맞는다. Bronze, Silver, Gold 계층을 모두 Delta로 운영하면 같은 저장소 위에서 원시 데이터, 정제 데이터, 집계 데이터를 버전 관리할 수 있다. MLflow 같은 실험 추적 도구에 `versionAsOf`를 함께 기록하면 모델 학습 데이터 재현성도 크게 높아진다.

- **📢 섹션 요약 비유**: Delta, Iceberg, Hudi는 모두 같은 항구를 운영하는 방식이지만, Delta는 작업 일지가 자세한 부두, Iceberg는 선적 목록이 정교한 부두, Hudi는 실시간 입출항이 빠른 부두에 가깝다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서 가장 중요한 질문은 "몇 일 전까지 되돌릴 수 있어야 하는가"다. 이 답이 없으면 Time Travel은 멋진 기능 이름에 그친다. 예를 들어 재무 배치 오류를 30일 안에 되돌려야 한다면, 로그 보존과 데이터 파일 보존 기간이 그 기준보다 짧아서는 안 된다. 반대로 단기 운영 복구만 필요하다면 지나치게 긴 보존은 비용만 키울 수 있다.

| 상황 | 권장 판단 | 이유 |
| :--- | :--- | :--- |
| 품질 사고 시 되돌림이 자주 필요 | `VACUUM` 보존 기간을 복구 목표보다 길게 설정 | 파일이 지워지면 `RESTORE`가 불가능 |
| `MERGE`가 잦은 차원 테이블 | 정기적 `OPTIMIZE`/Compaction과 파티션 점검 | 소형 파일 폭증과 메타데이터 비용 완화 |
| 하류 시스템이 변경분만 소비 | CDF를 선택적으로 활성화 | 전체 재스캔 없이 증분 전달 가능 |
| 여러 쿼리 엔진이 같은 테이블을 사용 | 표준 포맷 호환성부터 비교 | 형식 선택이 운영 마찰을 좌우 |
| ML 재현성이 중요 | 학습 실험에 Delta 버전 기록 | 데이터·모델 관계를 정확히 복원 |

### 체크리스트

1. `VACUUM` 정책이 비용 절감이 아니라 실제 복구 목표(예: 7일, 30일, 90일)에 맞춰 설정되어 있는가?
2. 스키마 자동 병합을 모든 계층에 허용하지 않고, 어디까지 진화를 허용할지 명확히 정해 두었는가?
3. 소형 파일 문제를 `OPTIMIZE` 또는 엔진별 compaction 전략으로 관리하고 있는가?
4. `DESCRIBE HISTORY`와 `RESTORE`를 운영 사고 대응 절차에 실제로 포함해 보았는가?

### 안티패턴

- 저장 비용을 아끼려고 `VACUUM RETAIN 0 HOURS`처럼 공격적으로 정리하는 경우
- Time Travel이 있으니 외부 백업이 필요 없다고 오해하는 경우
- `MERGE`가 많은 테이블에 compaction 없이 계속 쓰기만 하는 경우
- 스키마 자동 진화를 과도하게 켜 두어 원치 않는 컬럼 확장을 허용하는 경우

Delta는 기술보다 운영 규칙이 더 중요하다. 기본 7일 보존을 아무 생각 없이 따르거나, 반대로 무한 보존을 선언해 비용을 폭증시키면 둘 다 실패다. 복구 목표, 규제 요구, 엔진 구성에 맞춘 보존·최적화·감사 정책이 함께 있어야 Time Travel이 실전 기능이 된다.

- **📢 섹션 요약 비유**: Time Travel을 잘 쓰는 조직은 타임머신 버튼만 가진 곳이 아니라, 몇 시점까지 돌아갈지와 언제 오래된 기록을 폐기할지를 함께 정한 아카이브 팀을 가진 곳과 같다.

---

## Ⅴ. 기대효과 및 결론

Delta Lakehouse를 도입하면 데이터 레이크가 "싸지만 불안한 저장소"에서 "오픈 포맷이면서도 회복 가능한 테이블 플랫폼"으로 변한다. 배치 실패 시 전체 재처리 대신 버전 확인과 `RESTORE`로 대응할 수 있고, CDC·업서트·삭제 작업도 파일 시스템 수준이 아니라 테이블 수준에서 일관되게 다룰 수 있다. ML 관점에서는 데이터 버전이 실험 이력과 연결되어 재현성이 좋아진다.

그러나 Delta가 만능은 아니다. 로그와 체크포인트 관리, 저장 비용, 엔진 호환성, 운영 자동화가 뒷받침되지 않으면 오히려 복잡한 메타데이터 계층만 얹은 셈이 된다. 특히 Time Travel은 보존된 파일 위에서만 성립하므로, 저장 정책을 가볍게 다루면 핵심 가치가 바로 사라진다.

결론적으로 Delta Lakehouse는 단순히 "Parquet에 기능이 좀 더 붙은 것"이 아니다. 기억해야 할 핵심은 <strong>오픈 파일 저장소 위에 트랜잭션 로그와 보존 규칙을 올려, 데이터 테이블을 버전 있는 자산으로 바꾸는 기술</strong>이라는 점이다.

- **📢 섹션 요약 비유**: Delta Lakehouse는 창고에 타임머신을 붙인 시스템이 아니라, 입출고 장부와 재고 기준일을 함께 관리하는 창고다. 장부와 재고를 같이 관리할 때만 과거 상태로 정확히 돌아갈 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Delta Log | 테이블 버전과 파일 포함 관계를 기록하는 트랜잭션 메타데이터 계층 |
| Snapshot Isolation | 독자가 항상 커밋 완료된 일관된 버전만 읽게 하는 읽기 격리 방식 |
| Checkpoint | 긴 JSON 로그를 압축해 빠른 스냅샷 복원을 돕는 Parquet 메타데이터 |
| `MERGE` | CDC와 업서트를 테이블 수준에서 안전하게 반영하는 대표 연산 |
| Change Data Feed (CDF) | 변경분만 하류 시스템으로 전달하는 증분 소비 메커니즘 |
| Medallion Architecture | Bronze·Silver·Gold 계층을 Delta 테이블로 운영하는 레이크하우스 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
Parquet 중심 Data Lake
    |
    v
Delta Log 추가
    |
    v
ACID Snapshot · Schema Enforcement · MERGE
    |
    v
Time Travel · RESTORE · CDF
    |
    v
Lakehouse Governance · ML Reproducibility
```

이 흐름은 "저장소" 중심 사고에서 "버전 있는 테이블 자산" 중심 사고로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Delta Lake는 데이터 창고에 날짜별 기록장이 붙어 있어서 어제 물건이 어디 있었는지 다시 볼 수 있어요.
2. 누가 잘못 정리해도 이전 기록을 보고 바로 원래대로 돌릴 수 있어요.
3. 그래서 같은 데이터로 다시 공부하거나, 실수한 날의 상태를 다시 꺼내 보는 일이 쉬워져요.
