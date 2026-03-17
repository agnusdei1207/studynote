+++
title = "427. 결합 인덱스(Composite Index) - 순서가 만드는 성능"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 427
+++

# 427. 결합 인덱스(Composite Index) - 순서가 만드는 성능

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 결합 인덱스(Composite Index)는 두 개 이상의 컬럼을 조합하여 생성하는 B-Tree (Balanced Tree) 기반의 데이터 구조로, **'선행 컬럼(Leading Column)'의 정렬 순서에 따라 데이터 액세스 효율이 결정**되는 데이터베이스 핵심 최적화 기법이다.
> 2. **가치**: 다중 컬럼에 대한 단일 인덱스 생성으로 저장 공간(Space Overhead)을 절약하고, `Index Range Scan`을 통해 다중 컬럼 조건 쿼리의 성능을 비선형적으로 향상시키며, `Covering Index` 효과를 통해 디스크 I/O를 최소화한다.
> 3. **융합**: OS 파일 시스템의 블록 할당 정책과 알고리즘의 정렬(Sorting) 복잡도 이론이 결합된 구조로, 잘못된 컬럼 순서 설계는 인덱스 무효화(Table Full Scan)를 초래하여 DB 서버의 CPU 및 메모리 자원을 고갈시키는 치명적인 결과를 초래할 수 있다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**결합 인덱스(Composite Index, Multi-column Index)**란 테이블의 여러 컬럼을 하나의 논리적 단위로 묶어 생성하는 인덱스를 의미합니다. 단일 인덱스가 한 컬럼의 값을 키(Key)로 사용하는 반면, 결합 인덱스는 **(Column A, Column B)**와 같이 순서가 있는 튜플(Tuple)을 하나의 키로 사용합니다.

이 기술의 핵심 철학은 **'데이터의 물리적 배치 순서(Physical Ordering)'**입니다. 데이터베이스는 데이터를 디스크에 저장할 때, 결합 인덱스의 첫 번째 컬럼을 기준으로 먼저 정렬하고, 첫 번째 컬럼의 값이 동일할 경우 두 번째 컬럼을 기준으로 정렬하는 **계층적 정렬(Hierarchical Sorting)** 전략을 사용합니다. 이는 마치 도서관에서 책을 '대분야(100번대)' -> '소분야(10번대)' -> '저자명 순'으로 꽂아두는 것과 같은 논리입니다.

#### 2. 등장 배경 및 비즈니스 요구
① **기존 한계**: 단일 컬럼 인덱스만으로는 `WHERE col1 = 'A' AND col2 = 'B'`와 같은 복합 조건 조회 시 `Index Merge(인덱스 병합)` 연산이 발생하여 성능이 저하됩니다.
② **혁신적 패러다임**: 자주 조회되는 컬럼 조합을 미리 정렬해 둠으로써, 추가적인 정렬 연산 없이 디스크 블록(Block)을 직접 액세스하는 **'순차적 I/O(Sequential I/O)'**를 가능하게 했습니다.
③ **현재의 비즈니스 요구**: 빅데이터 환경에서 수백만 행 이상의 테이블에서 특정 고객 그룹의 최근 주문 내역을 조회하는 등의 복잡한 필터링 요구가 폭증함에 따라, 결합 인덱스의 전략적 설계는 선택이 아닌 필수가 되었습니다.

#### 3. ASCII 다이어그램: 개념적 비교
아래는 단일 인덱스와 결합 인덱스의 데이터 접근 방식 차이를 시각화한 것입니다.

```text
[ Single Index vs. Composite Index Data Access ]

┌─────────────────────────────────────────────────────────────────────────┐
│  Scenario: Find "Data-3" where Group='A' AND Type='2'                  │
└─────────────────────────────────────────────────────────────────────────┘

[ Case A: Single Indexes on 'Group', 'Type' ]
   (Index 1: Group)          (Index 2: Type)            (Data Table)
   Group ────▶ Row Ptr      Type ────▶ Row Ptr        [ ID | Group | Type ]
   ┌────────┐               ┌────────┐                ────────────────────
   │ A  ────┼───┐           │ 1  ────┼───┐            │ 1  │  A     │  1   │
   │ A  ────┼───┼────────▶  │ 2  ────┼───┼────────▶  │ 2  │  B     │  2   │ (Lookup)
   │ B  ────┼───┼─┐         │ 3  ────┼───┼─┐          │ 3  │  A     │  3   │ ✅ Target
   └────────┘  │ └───────── └────────┘ │ └────────── │ 4  │  C     │  1   │
               ▼                     ▼             │ 5  │  A     │  2   │
             (Set Intersection)                     ────────────────────
               Overhead High ⚠️                       ▲
                                                       │
               Access Path: Scattered Random I/O
               ⚠ CPU Overhead (Merge & Filter)

[ Case B: Composite Index (Group, Type) ]
   (Index Key: (Group, Type))
   ┌──────────────────┐
   │ Group  │ Type    │
   ├────────┼─────────┤
   │   A    │   1     │ ◀─── Leading (A)
   │   A    │   2     │ ◀─── Leading (A) + Trailing (2)
   │   A    │   3     │
   │   B    │   1     │
   └────────┴─────────┘
          │
          ▼
   ┌─────────────────────────────────────────┐
   │  [Direct Access to Row ID]              │
   │  1. Seek Group 'A'                      │
   │  2. Within 'A', Scan Range to Type '2'  │ ✅ Direct Hit
   │  3. Fetch Data Block                    │
   └─────────────────────────────────────────┘

   Access Path: Sequential Scan within Range (High Efficiency)
```
> **해설**: 단일 인덱스는 두 개의 리스트를 교차 확인하는 느린 과정(Intersection)이 필요하지만, 결합 인덱스는 정렬된 대로 'A' 그룹 안에서 순서대로 읽기만 하면 되므로 검색 범위가 획기적으로 줄어듭니다.

#### 📢 섹션 요약 비유
결합 인덱스의 개념은 **'전화번호부의 성명 리스트'**와 같습니다. 우리는 (성, 이름) 순으로 정렬된 전화번호부를 찾습니다. 'Kim'이라는 성(Leading Column)을 모르면 'Cheol-su'라는 이름으로 사람을 찾기 위해 전화번호부 전체를 읽어야 하지만, 'Kim' 성을 안다면 해당 페이지로 바로 이동하여 뒤에 오는 이름만 훑으면 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 내부 동작 표
결합 인덱스는 **B-Tree (Balanced Tree)** 구조를 기반으로 하며, 리프 노드(Leaf Node)에 실제 데이터 행을 가리키는 **RID (Row ID)** 혹은 데이터 값을 저장합니다.

| 요소명 | 역할 | 내부 동작 및 파라미터 | 프로토콜/알고리즘 | 비유 |
|:---|:---|:---|:---|:---|
| **Leading Column (선행 컬럼)** | **1차 정렬 기준** | 인덱스 탐색의 진입점. `WHERE` 절에 반드시 포함되어야 `Index Range Scan` 가능. | B-Tree Traversal (Leftmost) | 고속도로 톨게이트 |
| **Trailing Column (후행 컬럼)** | **2차 정렬 기준** | 선행 컬럼이 동일할 때 범위를 좁히는 역할. `Equality` 조건일 때 최적화됨. | Sequential Scan within Block | 톨게이트 내 차선 |
| **Index Key (Tuple)** | 정렬 단위 | `(Col_A, Col_B, Col_C)` 값의 조합. 16바이트 등 크기 제한 존재 (DBMS 종속). | Comparison Logic | 도로 주소 체계 |
| **Leaf Node (리프 노드)** | 데이터 포인터 | 실제 데이터 페이지 위치(RID) 저장. `Double Linked List`로 연관됨. | Disk I/O Operation | 사서의 책장 위치 |
| **Selectivity (선택도)** | 필터링 효율 | `Unique Values / Total Rows`. 선행 컬럼은 선택도가 높을수록 유리함. | Cost Based Optimizer (CBO) | 낚시바늘의 크기 |

#### 2. ASCII 구조 다이어그램: B-Tree 구조와 데이터 흐름
결합 인덱스 `(Department, Salary)`가 생성된 상태에서 `WHERE Dept='Sales' AND Salary > 5000` 쿼리가 수행되는 과정입니다.

```text
[ B-Tree Composite Index Structure ]

           [ Root Node ]
           ┌──────────────────────────────────┐
           │ Dept: 'HR'    │ Dept: 'IT' │ ... │
           └───────┬────────────────────┬─────┘
                   │                    │
                   ▼                    ▼
          [ Branch Node: 'IT' ]  [ ... ]
          ┌──────────────────────────────┐
          │ Dept='IT' │ Salary=3000      │ ────▶ Leaf List (Sorted by Salary)
          │ Dept='IT' │ Salary=4000      │      ┌─────────────────────────────────┐
          │ Dept='IT' │ Salary=5000      │      │ (IT, 3000) → RID: 0x04         │
          └───────┬──────────────────────┘      │ (IT, 4500) → RID: 0x08         │
                  │                             │ (IT, 6000) → RID: 0x12         │ ◀─┐
                  ▼                             │ (IT, 8000) → RID: 0x15         │   │
          [ Branch Node: 'Sales']               └─────────────────────────────────┘   │
          ┌──────────────────────────────┐                                   ▲
          │ Dept='Sales'│ Salary=4000     │                              (Range Scan)
          │ Dept='Sales'│ Salary=5000     │ ────▶ Leaf List                    │
          │ Dept='Sales'│ Salary=6000     │      ┌─────────────────────────────────┤
          │ Dept='Sales'│ Salary=7500     │      │ (Sales, 4000) → RID: 0x22      │
          └───────┬──────────────────────┘      │ (Sales, 5200) → RID: 0x25      │ ✅ Start Scan
                  │                             │ (Sales, 7500) → RID: 0x29      │
                  ▼                             │ (Sales, 9000) → RID: 0x30      │
          [ Query Logic ]                        └─────────────────────────────────┘
          1. Root에서 'Sales' 탐색
          2. 'Sales' 브랜치로 이동
          3. Salary > 5000 조건 만족 스캔 시작
          4. 5200, 7500 순으로 RID 획득 (Random Access)
```
> **해설**: 쿼리 옵티마이저(Optimizer)는 루트 노드에서부터 'Sales'라는 선행 컬럼을 찾아내려갑니다. 'Sales'를 찾은 순간, 이제는 그 안에서 Salary가 정렬되어 있으므로 5000이 넘는 지점부터 순차적으로 스캔(Scan)하기만 하면 됩니다. 이 과정에서 불필요한 데이터 블록을 읽는 `Random I/O`가 발생하지 않습니다.

#### 3. 심층 동작 원리 및 핵심 알고리즘
결합 인덱스의 성능은 **'Equal(=) - Range(범위) - Sort(정렬)'** 순서의 배치에 좌우됩니다.

**① 2-Phase Search (2단계 검색)**
1.  **Seek Phase**: 선행 컬럼(Leading Column)을 이용해 B-Tree를 타고 내려가 검색 시작 범위를 찾습니다. 시간 복잡도는 $O(\log N)$입니다.
2.  **Scan Phase**: 찾은 범위 내에서 후행 컬럼(Trailing Column)의 조건을 만족하는 데이터를 순차적으로 스캔합니다. 후행 컬럼이 `=` (동등) 조건이면 범위가 매우 좁아지지만, `>`나 `BETWEEN` 같은 범위 조건이면 스캔해야 할 양이 늘어납니다.

**② 핵심 최적화 전략: Equality first, Range later**
```sql
-- ✅ Good: (Status = 'Active', Reg_Date > '2023-01-01')
-- 'Active'인 그룹을 찾은 뒤, 그 안에서 날짜를 순차적으로 비교.
CREATE INDEX idx_status_date ON Users(Status, Reg_Date);

-- ❌ Bad: (Reg_Date, Status)
-- 전체 날짜 범위를 다 스캔한 뒤, 그 안에서 Status를 필터링해야 함.
-- 선행 컬럼이 범위 조건이면, 후행 컬럼의 인덱스 정렬 속성이 무력화됨.
```

#### 📢 섹션 요약 비유
결합 인덱스의 동작은 **'정렬된 파일 캐비닛'**을 찾는 과정과 같습니다. (부서, 입사일) 순으로 되어 있다면, '영업팀' 캐비닛(선행 컬럼)을 열고 그 안에서 '2020년 이후' 파일(후행 컬럼)을 순서대로 보면 됩니다. 하지만 입사일순으로 먼저 정리되어 있다면, 전체 직원의 입사일 파일을 뒤져가며 영업팀 직원을 골라내야 하는 엄청난 노력(범위 스캔)이 필요하게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 결합 인덱스 vs. 인덱스 머지 (Index Merge) vs. 커버링 인덱스

| 비교 항목 | 결합 인덱스 (Composite) | 인덱스 머지 (Index Merge) | 커버맱 인덱스 (Covering) |
|:---|:---|:---|:---|
| **정의** | 다중 컬럼을 하나의 B-Tree로 구성 | 여러 단일 인덱스를 결과적으로 결합 | 인덱스에 쿼리所需 컬럼을 모두 포함 |
| **성능 (Latency)** | **매우 빠름 (Single Seek)** | 느림 (Multiple Seek + Sort) | **최고 (No Table Access)** |
| **CPU/메모리** | 낮음 (단일 연산) | 높음 (임시 테이블 생성, 버퍼 사용) | 낮음 (인덱스 페이지만 메모리 로드) |
| **저장 공간** | 중간 (하나의 인덱스 구조) | 낮음 (단일 컬럼 인덱스만 존재) | 높음 (비선행 컬럼까지 포함하여 크기 증가) |
| **주요 용도** | 결