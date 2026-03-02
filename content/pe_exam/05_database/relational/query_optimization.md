+++
title = "쿼리 최적화 (Query Optimization)"
date = 2025-03-02

[extra]
categories = "pe_exam-database"
+++

# 쿼리 최적화 (Query Optimization)

## 핵심 인사이트 (3줄 요약)
> **SQL 실행을 위한 최적의 실행 계획을 수립하는 DBMS 핵심 기능**. 비용 기반 옵티마이저(CBO)가 통계 정보로 비용 계산 후 최소 비용 경로 선택. 인덱스 선택, 조인 순서, 조인 알고리즘이 최적화의 3대 핵심 요소.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 쿼리 최적화(Query Optimization)는 **SQL 문을 실행하기 위해 가능한 모든 실행 계획(Execution Plan) 중 비용(Cost)이 최소인 계획을 선택하는 DBMS의 핵심 기능**이다. 옵티마이저(Optimizer)가 이 역할을 담당한다.

> 💡 **비유**: 쿼리 최적화는 **"네비게이션의 최적 경로 탐색"** 같아요. "서울→부산"을 가는 방법은 여러 가지죠. 고속도로, 국도, KTX... 네비게이션은 현재 교통 상황(통계)을 보고 가장 빠른 길을 추천해요. 옵티마이저도 마찬가지로 데이터 분포를 보고 최적의 실행 경로를 선택해요.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 비효율적 실행**: 사용자가 작성한 SQL 그대로 실행하면 성능 저하 (풀 스캔, 잘못된 조인 순서)
2. **기술적 필요성 - 선언적 언어의 특성**: SQL은 "무엇을"만 표현, "어떻게"는 DBMS가 결정해야 함
3. **시장/산업 요구 - 대용량 처리**: 빅데이터 시대에 효율적인 쿼리 실행은 필수적

**핵심 목적**: **쿼리 응답 시간 최소화**와 **시스템 자원(CPU, I/O, 메모리) 효율적 사용**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **옵티마이저** | 최적 실행 계획 수립 | CBO/RBO 방식 | 네비게이션 |
| **통계 정보** | 데이터 분포/크기 정보 | 히스토그램, 카디널리티 | 교통 정보 |
| **실행 계획** | 쿼리 실행 전략 | 트리 형태 연산자 | 경로 지도 |
| **비용 모델** | 실행 비용 계산 | I/O + CPU 비용 | 소요 시간 |
| **카탈로그** | 메타데이터 저장 | 테이블/인덱스 정보 | 도로 정보 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    쿼리 최적화 처리 과정                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [SQL 문]                                                          │
│       │                                                             │
│       ▼                                                             │
│   ┌─────────────┐                                                  │
│   │  1. 파싱    │ → 구문 분석, 파스 트리 생성                       │
│   └──────┬──────┘                                                  │
│          ▼                                                          │
│   ┌─────────────┐                                                  │
│   │ 2. 정규화   │ → 중복 제거, 상수 전파, 조건 단순화               │
│   └──────┬──────┘                                                  │
│          ▼                                                          │
│   ┌─────────────┐                                                  │
│   │ 3. 대안     │ → 가능한 실행 계획들 생성                         │
│   │   생성      │   (조인 순서, 인덱스 선택, 알고리즘 조합)         │
│   └──────┬──────┘                                                  │
│          ▼                                                          │
│   ┌─────────────┐                                                  │
│   │ 4. 비용     │ → 각 대안의 비용 계산                             │
│   │   추정      │   (I/O 비용 + CPU 비용)                          │
│   └──────┬──────┘                                                  │
│          ▼                                                          │
│   ┌─────────────┐                                                  │
│   │ 5. 선택     │ → 최소 비용 실행 계획 선택                        │
│   └──────┬──────┘                                                  │
│          ▼                                                          │
│   ┌─────────────┐                                                  │
│   │ 6. 실행     │ → 실행 엔진이 실제 수행                           │
│   └─────────────┘                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    조인 알고리즘 비교                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   1. Nested Loop Join (중첩 루프 조인)                              │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  for each row R1 in TableA:                                 │  │
│   │      for each row R2 in TableB:                             │  │
│   │          if R1.key == R2.key: output(R1, R2)                │  │
│   │                                                              │  │
│   │  비용: O(M × N)                                              │  │
│   │  적합: 작은 테이블, 인덱스 있는 경우                         │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   2. Hash Join (해시 조인)                                          │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  Build Phase: 작은 테이블로 해시 테이블 구축                 │  │
│   │  Probe Phase: 큰 테이블 스캔하며 해시 조회                   │  │
│   │                                                              │  │
│   │  비용: O(M + N)                                              │  │
│   │  적합: 대용량 테이블, 등가 조인                              │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   3. Sort Merge Join (정렬 병합 조인)                               │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  Sort Phase: 양쪽 테이블을 조인 키로 정렬                    │  │
│   │  Merge Phase: 정렬된 상태에서 병합                           │  │
│   │                                                              │  │
│   │  비용: O(M log M + N log N)                                  │  │
│   │  적합: 이미 정렬된 데이터, 범위 조인                        │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 쿼리 파싱 → ② 논리적 최적화 → ③ 물리적 최적화 → ④ 실행 계획 생성 → ⑤ 실행
```

- **1단계 - 쿼리 파싱**: SQL 구문 분석, 파스 트리 생성, 문법 오류 검사
- **2단계 - 논리적 최적화**: 조건 푸시다운, 조인 순서 변경, 서브쿼리 펼치기
- **3단계 - 물리적 최적화**: 인덱스 선택, 조인 알고리즘 선택, 접근 방법 결정
- **4단계 - 실행 계획 생성**: 선택된 최적화 전략으로 실행 계획 트리 생성
- **5단계 - 실행**: 실행 엔진이 계획에 따라 데이터 접근

**핵심 알고리즘/공식** (해당 시 필수):

```
[비용 계산 공식 (CBO)]
Total Cost = I/O Cost + CPU Cost

I/O Cost = 페이지 접근 횟수 × 페이지 읽기 비용
CPU Cost = 행 처리 횟수 × 행 처리 비용

[선택도 (Selectivity)]
선택도 = 선택된 행 수 / 전체 행 수
      = 1 / 카디널리티 (균등 분포 가정)

[카디널리티 추정]
- 균등 분포: cardinality = 전체 행 수 / distinct 값 수
- 히스토그램: 실제 분포 기반 정확한 추정

[조인 비용 모델]
Nested Loop: M + M × N (인덱스 없음)
            M + M × logN (인덱스 있음)
Hash Join:   M + N + hash_build_cost
Sort Merge:  M + N + sort_cost(M) + sort_cost(N)

[인덱스 선택 비용]
Index Scan Cost = 트리 높이 + 선택된 행 수 × 랜덤 I/O
Full Scan Cost = 전체 페이지 수 × 순차 I/O

Index Scan 유리: 선택도 < 5~20%
Full Scan 유리: 선택도 > 20% (순차 I/O가 랜덤 I/O보다 빠름)
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
import heapq

class JoinType(Enum):
    NESTED_LOOP = "Nested Loop"
    HASH_JOIN = "Hash Join"
    SORT_MERGE = "Sort Merge"

class ScanType(Enum):
    FULL_SCAN = "Full Table Scan"
    INDEX_SCAN = "Index Scan"
    INDEX_SEEK = "Index Seek"

@dataclass
class Statistics:
    """테이블 통계 정보"""
    table_name: str
    row_count: int
    page_count: int
    column_stats: Dict[str, Dict]  # column -> {distinct, min, max, histogram}

@dataclass
class IndexInfo:
    """인덱스 정보"""
    index_name: str
    table_name: str
    columns: List[str]
    height: int
    leaf_pages: int

@dataclass
class CostEstimate:
    """비용 추정 결과"""
    io_cost: float
    cpu_cost: float
    total_cost: float
    cardinality: int

    @property
    def cost(self) -> float:
        return self.total_cost

class QueryOptimizer:
    """쿼리 최적화 시뮬레이터"""

    def __init__(self):
        self.statistics: Dict[str, Statistics] = {}
        self.indexes: Dict[str, List[IndexInfo]] = {}
        # 상수 (실제 DBMS에서는 측정값)
        self.RANDOM_IO_COST = 1.0
        self.SEQUENTIAL_IO_COST = 0.1
        self.CPU_TUPLE_COST = 0.01
        self.CPU_INDEX_TUPLE_COST = 0.005

    def update_statistics(self, table_name: str, row_count: int,
                         page_count: int, column_stats: Dict = None):
        """통계 정보 갱신"""
        self.statistics[table_name] = Statistics(
            table_name=table_name,
            row_count=row_count,
            page_count=page_count,
            column_stats=column_stats or {}
        )

    def estimate_selectivity(self, table: str, column: str,
                            operator: str, value: any) -> float:
        """선택도 추정"""
        stats = self.statistics.get(table)
        if not stats:
            return 0.1  # 기본값

        col_stats = stats.column_stats.get(column, {})
        distinct = col_stats.get('distinct', 10)

        if operator == '=':
            # 등호: 1/distinct
            return 1.0 / distinct
        elif operator in ('<', '>', '<=', '>='):
            # 범위: 1/3 기본값 (실제로는 히스토그램 사용)
            min_val = col_stats.get('min', 0)
            max_val = col_stats.get('max', 100)
            if max_val == min_val:
                return 1.0
            if operator in ('<', '<='):
                return (value - min_val) / (max_val - min_val)
            else:
                return (max_val - value) / (max_val - min_val)
        elif operator == 'IN':
            # IN: count / distinct
            return min(len(value) / distinct, 1.0)
        else:
            return 0.1

    def estimate_full_scan_cost(self, table: str) -> CostEstimate:
        """풀 스캔 비용 추정"""
        stats = self.statistics.get(table)
        if not stats:
            return CostEstimate(0, 0, 0, 0)

        io_cost = stats.page_count * self.SEQUENTIAL_IO_COST
        cpu_cost = stats.row_count * self.CPU_TUPLE_COST

        return CostEstimate(
            io_cost=io_cost,
            cpu_cost=cpu_cost,
            total_cost=io_cost + cpu_cost,
            cardinality=stats.row_count
        )

    def estimate_index_scan_cost(self, table: str, index: IndexInfo,
                                 selectivity: float) -> CostEstimate:
        """인덱스 스캔 비용 추정"""
        stats = self.statistics.get(table)
        if not stats:
            return CostEstimate(0, 0, 0, 0)

        selected_rows = int(stats.row_count * selectivity)

        # 인덱스 접근 비용
        io_cost = index.height * self.RANDOM_IO_COST  # 트리 탐색
        io_cost += selected_rows * self.RANDOM_IO_COST  # 테이블 접근

        cpu_cost = selected_rows * self.CPU_INDEX_TUPLE_COST

        return CostEstimate(
            io_cost=io_cost,
            cpu_cost=cpu_cost,
            total_cost=io_cost + cpu_cost,
            cardinality=selected_rows
        )

    def choose_scan_method(self, table: str, conditions: List[Tuple]) -> Tuple:
        """스캔 방법 선택"""
        stats = self.statistics.get(table)
        if not stats:
            return (ScanType.FULL_SCAN, None, self.estimate_full_scan_cost(table))

        # 조건에 맞는 인덱스 찾기
        best_index = None
        best_selectivity = 1.0
        best_cost = self.estimate_full_scan_cost(table)

        for cond in conditions:
            column, operator, value = cond
            for idx in self.indexes.get(table, []):
                if column in idx.columns:
                    selectivity = self.estimate_selectivity(table, column, operator, value)
                    idx_cost = self.estimate_index_scan_cost(table, idx, selectivity)

                    if idx_cost.total_cost < best_cost.total_cost:
                        best_cost = idx_cost
                        best_index = idx
                        best_selectivity = selectivity

        if best_index:
            return (ScanType.INDEX_SCAN, best_index, best_cost)
        return (ScanType.FULL_SCAN, None, best_cost)

    def estimate_join_cost(self, table1: str, table2: str,
                          join_type: JoinType,
                          card1: int, card2: int) -> CostEstimate:
        """조인 비용 추정"""
        stats1 = self.statistics.get(table1, Statistics(table1, card1, card1 // 100, {}))
        stats2 = self.statistics.get(table2, Statistics(table2, card2, card2 // 100, {}))

        if join_type == JoinType.NESTED_LOOP:
            # 외부 테이블 × 내부 테이블 접근
            io_cost = (card1 * self.CPU_TUPLE_COST +
                      card1 * card2 * self.CPU_INDEX_TUPLE_COST)
            cpu_cost = card1 * card2 * 0.001
            result_card = max(card1, card2)  # 간단히 추정

        elif join_type == JoinType.HASH_JOIN:
            # 해시 구축 + 탐색
            io_cost = (stats1.page_count + stats2.page_count) * self.SEQUENTIAL_IO_COST
            cpu_cost = (card1 + card2) * self.CPU_TUPLE_COST
            result_card = max(card1, card2)

        elif join_type == JoinType.SORT_MERGE:
            # 정렬 + 병합
            sort_cost = (card1 * 3.5 + card2 * 3.5)  # log n 근사
            io_cost = (stats1.page_count + stats2.page_count) * 2  # 읽기 + 쓰기
            cpu_cost = sort_cost * self.CPU_TUPLE_COST
            result_card = max(card1, card2)

        return CostEstimate(
            io_cost=io_cost,
            cpu_cost=cpu_cost,
            total_cost=io_cost + cpu_cost,
            cardinality=int(result_card)
        )

    def choose_join_order(self, tables: List[str],
                         join_conditions: List[Tuple]) -> List[Tuple]:
        """조인 순서 최적화 (동적 계획법)"""
        n = len(tables)
        if n <= 1:
            return [(t, None, self.estimate_full_scan_cost(t)) for t in tables]

        # DP로 최적 조인 순서 찾기
        # dp[mask] = (cost, join_plan)
        dp = {}

        # 초기화: 단일 테이블
        for i, table in enumerate(tables):
            mask = 1 << i
            scan_type, idx, cost = self.choose_scan_method(table, [])
            dp[mask] = (cost.total_cost, [(table, scan_type, cost)])

        # 조인 순서 확장
        for size in range(2, n + 1):
            for mask in range(1 << n):
                if bin(mask).count('1') != size:
                    continue

                best_cost = float('inf')
                best_plan = None

                # 부분 집합으로 분할
                for sub_mask in range(1, mask):
                    if sub_mask & mask != sub_mask:
                        continue
                    other_mask = mask ^ sub_mask

                    if sub_mask not in dp or other_mask not in dp:
                        continue

                    # 두 서브플랜 조인
                    cost1, plan1 = dp[sub_mask]
                    cost2, plan2 = dp[other_mask]

                    # 조인 비용 계산 (간단화)
                    card1 = plan1[-1][2].cardinality if plan1 else 1
                    card2 = plan2[-1][2].cardinality if plan2 else 1

                    join_cost = self.estimate_join_cost(
                        plan1[-1][0], plan2[-1][0],
                        JoinType.HASH_JOIN, card1, card2
                    )

                    total_cost = cost1 + cost2 + join_cost.total_cost

                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_plan = plan1 + plan2 + [(f"JOIN({plan1[-1][0]},{plan2[-1][0]})",
                                                       JoinType.HASH_JOIN, join_cost)]

                if best_plan:
                    dp[mask] = (best_cost, best_plan)

        # 전체 집합 결과 반환
        full_mask = (1 << n) - 1
        return dp.get(full_mask, (0, []))[1]

    def explain(self, table: str, conditions: List[Tuple] = None) -> Dict:
        """실행 계획 설명 (EXPLAIN)"""
        conditions = conditions or []

        scan_type, idx, cost = self.choose_scan_method(table, conditions)

        plan = {
            "operation": scan_type.value,
            "table": table,
            "index": idx.index_name if idx else None,
            "cost": {
                "io": round(cost.io_cost, 2),
                "cpu": round(cost.cpu_cost, 2),
                "total": round(cost.total_cost, 2)
            },
            "cardinality": cost.cardinality,
            "bytes": cost.cardinality * 100  # 추정 행 크기
        }

        return plan

# 사용 예시
if __name__ == "__main__":
    optimizer = QueryOptimizer()

    # 통계 정보 설정
    optimizer.update_statistics(
        "employees", row_count=100000, page_count=1000,
        column_stats={
            "dept_id": {"distinct": 10, "min": 1, "max": 10},
            "salary": {"distinct": 1000, "min": 3000000, "max": 10000000},
            "name": {"distinct": 95000}
        }
    )

    # 인덱스 설정
    optimizer.indexes["employees"] = [
        IndexInfo("idx_dept", "employees", ["dept_id"], height=3, leaf_pages=100),
        IndexInfo("idx_salary", "employees", ["salary"], height=3, leaf_pages=200)
    ]

    # 실행 계획 확인
    print("=== WHERE dept_id = 5 ===")
    plan = optimizer.explain("employees", [("dept_id", "=", 5)])
    print(f"Operation: {plan['operation']}")
    print(f"Index: {plan['index']}")
    print(f"Cost: {plan['cost']}")
    print(f"Cardinality: {plan['cardinality']}")

    print("\n=== WHERE salary > 8000000 (범위 조건) ===")
    plan = optimizer.explain("employees", [("salary", ">", 8000000)])
    print(f"Operation: {plan['operation']}")
    print(f"Cost: {plan['cost']}")

    print("\n=== 조인 순서 최적화 ===")
    optimizer.update_statistics("departments", 10, 1, {"dept_id": {"distinct": 10}})
    optimizer.update_statistics("projects", 1000, 10, {"dept_id": {"distinct": 10}})

    join_plan = optimizer.choose_join_order(["employees", "departments", "projects"], [])
    for step in join_plan:
        if isinstance(step[0], str) and step[0].startswith("JOIN"):
            print(f"{step[0]}: cost={step[2].total_cost:.2f}")
        else:
            print(f"Scan {step[0]}: {step[1].value}")
```

---

### Ⅲ. 기술 비고 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **자동 성능 최적화**: 개발자가 튜닝 지식 없어도 효율 실행 | **통계 의존성**: 오래된 통계는 잘못된 계획 유발 |
| **선언적 작성**: "무엇을"만 표현하면 됨 | **예측 불가**: 복잡한 쿼리는 비용 추정 부정확 |
| **동적 적응**: 데이터 변화에 따라 자동 조정 | **오버헤드**: 최적화 자체에 CPU/메모리 소모 |
| **일관성**: 동일 SQL은 항상 동일 결과 | **바인드 변수**: 실행 시점에 따라 다른 계획 가능 |

**옵티마이저 유형별 비교** (필수: 최소 2개 대안):
| 비교 항목 | RBO (규칙 기반) | CBO (비용 기반) |
|---------|----------------|----------------|
| **핵심 특성** | 미리 정의된 규칙 우선순위 | ★ 통계 기반 비용 계산 |
| **통계 활용** | X | ★ O (필수) |
| **적응성** | 낮음 (고정 규칙) | ★ 높음 (동적) |
| **복잡도** | 낮음 | 높음 |
| **현대 DBMS** | 거의 사용 안 함 | ★ 표준 (Oracle, MySQL, PostgreSQL) |
| **힌트 사용** | 불필요 | 필요 시 사용 |

| 비교 항목 | Nested Loop | Hash Join | Sort Merge |
|---------|------------|-----------|------------|
| **비용** | O(M×N) | ★ O(M+N) | O(M log M + N log N) |
| **메모리** | 적음 | 많음 (해시 테이블) | 중간 (정렬) |
| **인덱스** | ★ 필수 | 불필요 | 불필요 |
| **적합 환경** | OLTP, 소량 | ★ OLAP, 대량 | 정렬된 데이터 |

> **★ 선택 기준**:
> - **CBO**: 현대 DBMS의 표준, 통계 정보 최신 유지 필수
> - **Hash Join**: 대용량 데이터 조인, DW/OLAP 환경
> - **Nested Loop**: 인덱스 있는 소규모 테이블, OLTP

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **슬로우 쿼리 튜닝** | EXPLAIN 분석 → 인덱스 추가/힌트 | 쿼리 응답시간 80% 단축 |
| **대용량 배치** | Hash Join 유도, 병렬 처리 | 배치 수행시간 70% 단축 |
| **실시간 대시보드** | 서브쿼리 → 조인 변환, 커버링 인덱스 | 조회 응답 1초 이내 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 - 네이버**: 검색 로그 분석 쿼리를 Nested Loop → Hash Join으로 변경, 1시간 → 5분 단축
- **사례 2 - 카카오**: 채팅 메시지 조회 쿼리에 커버링 인덱스 적용, 100ms → 5ms 단축
- **사례 3 - 우아한형제들**: 배달 주문 통계 쿼리 최적화, 파티셔닝 + 인덱스 재설계로 10배 향상

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 통계 정보 수집 자동화 (ANALYZE)
   - 힌트(Hint)는 최후 수단
   - 바인드 변수 활용
   - 실행 계획 캐시(PgBouncer, Plan Cache)
2. **운영적**:
   - 슬로우 쿼리 로그 모니터링
   - 정기적인 통계 갱신
   - 쿼리 프로파일링 도구 활용
   - 실행 계획 변화 감지
3. **보안적**:
   - SQL Injection 방지 (Prepared Statement)
   - 실행 계획 노출 주의
4. **경제적**:
   - 최적화 투자 vs 하드웨어 증설
   - 튜닝 컨설턴트 비용
   - 쿼리 리팩토링 공수

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **오래된 통계**: ANALYZE 안 하면 비용 추정 부정확
- ❌ **함수 사용**: `WHERE UPPER(col) = 'A'` → 인덱스 미사용
- ❌ **암시적 변환**: `WHERE varchar_col = 123` → 인덱스 무효
- ❌ **OR 남용**: OR 조건은 인덱스 사용 어려움

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 쿼리 최적화와 밀접하게 연관된 핵심 개념들

┌─────────────────────────────────────────────────────────────────┐
│  쿼리 최적화 핵심 연관 개념 맵                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [인덱싱] ←──→ [쿼리최적화] ←──→ [SQL]                         │
│       ↓              ↓               ↓                          │
│   [통계정보]     [옵티마이저]   [실행계획]                        │
│       ↓              ↓               ↓                          │
│   [트랜잭션]    [동시성제어]    [조인알고리즘]                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **인덱싱** | 선행 개념 | 최적화의 핵심 수단 | `[인덱싱](./indexing.md)` |
| **SQL** | 입력 개념 | 최적화 대상 쿼리 | `[SQL](./sql.md)` |
| **동시성 제어** | 보완 개념 | 실행 중 락 경합 고려 | `[동시성제어](../concurrency_control.md)` |
| **트랜잭션** | 실행 단위 | 원자성 보장 | `[트랜잭션](../transaction.md)` |
| **분산 DB** | 확장 개념 | 분산 쿼리 최적화 | `[분산DB](../distributed_database.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **쿼리 응답 시간** | 최적 실행 계획 선택 | 50~90% 단축 |
| **리소스 사용량** | CPU, I/O 효율화 | 40% 절감 |
| **시스템 처리량** | 동시 쿼리 처리 증가 | TPS 3배 향상 |
| **개발 생산성** | 수동 튜닝 감소 | 튜닝 시간 60% 단축 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: AI/ML 기반 자동 튜닝, 학습형 옵티마이저(Learned Optimizer), 자동 인덱스 추천
2. **시장 트렌드**: 클라우드 DB의 Serverless 최적화, HTAP로 트랜잭션/분석 통합 최적화
3. **후속 기술**: 분산 쿼리 최적화, 벡터 DB 쿼리 최적화 (유사도 검색)

> **결론**: 쿼리 최적화는 DBMS 성능의 핵심 결정 요소로, 올바른 통계 관리와 이해가 필수적이다. 현대 CBO는 매우 정교하지만, 여전히 개발자의 튜닝 지식이 중요하며, AI 기반 자동 튜닝이 미래의 핵심 트렌드다.

> **※ 참고 표준**: SQL:2023, PostgreSQL Optimizer, Oracle Cost-Based Optimizer

---

## 어린이를 위한 종합 설명 (필수)

**쿼리 최적화**은(는) 마치 **"네비게이션이 최적 경로를 찾는 것"** 같아요.

서울에서 부산까지 가는 방법은 정말 많아요. 고속도로로 가거나, 국도로 가거나, 기차를 타거나... 각각 걸리는 시간이 다르죠. 네비게이션은 현재 교통 상황을 보고 **가장 빠른 길**을 추천해 줘요.

데이터베이스도 마찬가지예요. 한 학생을 찾는 방법이 여러 가지 있어요:
- **전체 스캔**: 1번부터 1000번까지 다 확인하기 (오래 걸려요 😅)
- **인덱스 사용**: 색인에서 바로 찾기 (빨라요! 🚀)

**옵티마이저**는 네비게이션처럼 **어떤 방법이 가장 빠를지 계산**해요. "학생이 1000명이니까 인덱스를 쓰는 게 100배 빠르겠네!"라고 판단하는 거예요.

하지만 **통계 정보**가 중요해요. 네비게이션이 교통 정보를 못 받으면 엉뚱한 길을 안내하듯이, 데이터베이스도 오래된 정보면 나쁜 선택을 할 수 있어요. 그래서 정기적으로 정보를 업데이트해야 해요! 🗺️📍
