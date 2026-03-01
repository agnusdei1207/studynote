+++
title = "인덱스 (Index)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 인덱스 (Index)

## 핵심 인사이트 (3줄 요약)
> **데이터 검색 속도를 향상시키는 자료구조**. 책의 색인처럼 특정 컬럼에 대한 빠른 조회 지원. B+Tree, Hash 등 다양한 구조 사용. 성능과 저장 공간의 트레이드오프 존재.

## 1. 개념
인덱스는 **테이블의 데이터를 빠르게 검색하기 위한 별도의 자료구조**로, 책의 목차나 색인과 같은 역할을 한다.

> 비유: "책의 색인" - 키워드를 찾으면 페이지 번호가 나옴

## 2. 인덱스 필요성

```
풀 테이블 스캔 (Full Table Scan):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓
  모든 데이터를 하나씩 검사 → O(n)

인덱스 사용:
        ┌───┐
        │ 5 │
        └─┬─┘
      ┌───┴───┐
      ↓       ↓
    ┌─┴─┐   ┌─┴─┐
    │ 3 │   │ 8 │
    └─┬─┘   └─┬─┘
    ┌─┴─┐   ┌─┴─┐
    ↓   ↓   ↓   ↓
   1,2 3,4 6,7 9,10

→ 이진 탐색으로 빠르게 접근 → O(log n)
```

## 3. 인덱스 구조

### 3.1 B+Tree 인덱스
```
                     ┌─────────┐
                     │ 루트    │
                     │ K1 | K2 │
                     └────┬────┘
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
     ┌─────────┐    ┌─────────┐    ┌─────────┐
     │ 내부    │    │ 내부    │    │ 내부    │
     │노드     │    │노드     │    │노드     │
     └────┬────┘    └────┬────┘    └────┬────┘
          │               │               │
    ┌─────┼─────┐   ┌─────┼─────┐   ┌─────┼─────┐
    ↓     ↓     ↓   ↓     ↓     ↓   ↓     ↓     ↓
  ┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
  │리프││리프││리프││리프││리프││리프││리프││리프││리프│
  │노드││노드││노드││노드││노드││노드││노드││노드││노드│
  └──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘
     │     │     │     │     │     │     │     │     │
     ↓     ↓     ↓     ↓     ↓     ↓     ↓     ↓     ↓
   데이터 데이터 데이터 데이터 데이터 데이터 데이터 데이터 데이터

특징:
- 리프 노드에만 데이터 존재
- 리프 노드가 연결 리스트로 연결 (범위 검색 용이)
- 균형 트리: 모든 리프 노드까지의 깊이 동일
```

### 3.2 해시 인덱스
```
해시 함수: key → 버킷 번호

┌─────────────────────────────────────┐
│        해시 테이블                   │
├────────┬────────────────────────────┤
│ 버킷 0 │ → (key1, data) → (key2, data)
├────────┼────────────────────────────┤
│ 버킷 1 │ → (key3, data)
├────────┼────────────────────────────┤
│ 버킷 2 │ → NULL
├────────┼────────────────────────────┤
│ 버킷 3 │ → (key4, data) → (key5, data)
└────────┴────────────────────────────┘

특징:
- 등가 비교(=)에 최적
- O(1) 평균 검색 시간
- 범위 검색 불가
```

## 4. 인덱스 종류

### 4.1 구조 기반 분류
```
B+Tree 인덱스:
- 가장 일반적
- 범위 검색 가능
- 정렬된 데이터

Hash 인덱스:
- 등가 검색 최적
- 범위 검색 불가
- 메모리 기반 DB에서 주로 사용

비트맵 인덱스:
- 저카디널리티(적은 종류) 컬럼
- 예: 성별, 상태코드
- 압축 효율 좋음
```

### 4.2 컬럼 기반 분류
```
단일 컬럼 인덱스:
- 하나의 컬럼으로 구성
- 가장 기본적인 형태

복합 인덱스 (Composite Index):
- 여러 컬럼으로 구성
- 순서 중요 (왼쪽 접두어 원칙)
- 예: (부서번호, 직급)

커버링 인덱스 (Covering Index):
- 쿼리에 필요한 모든 컬럼 포함
- 테이블 접근 없이 인덱스만으로 처리
```

### 4.3 데이터 기반 분류
```
클러스터형 인덱스 (Clustered Index):
- 물리적 정렬
- 테이블당 하나만 가능
- PK가 기본적으로 클러스터형
- 예: MySQL InnoDB의 PK

비클러스터형 인덱스 (Non-clustered Index):
- 별도 공간에 저장
- 여러 개 생성 가능
- 리프 노드에 데이터 위치(포인터/RID) 저장
```

## 5. 인덱스 동작 원리

### 5.1 검색 (SELECT)
```sql
-- 인덱스 사용
SELECT * FROM 학생 WHERE 학번 = '2024001';

1. 루트 노드에서 시작
2. 학번 값과 비교하여 이동할 자식 노드 결정
3. 리프 노드 도달
4. 데이터 위치 획득 → 실제 데이터 접근
```

### 5.2 삽입 (INSERT)
```
1. 새 데이터 삽입
2. 인덱스에 새 키 추가
3. 필요시 노드 분할 (Split)
4. 트리 균형 유지

비용:
- 인덱스가 없으면: O(1) (맨 뒤에 추가)
- 인덱스가 있으면: O(log n) + 분할 비용
```

### 5.3 삭제 (DELETE)
```
1. 데이터 삭제
2. 인덱스에서 키 제거
3. 필요시 노드 병합 (Merge)
4. 트리 균형 유지
```

### 5.4 수정 (UPDATE)
```
1. 이전 값 삭제 (인덱스에서)
2. 새 값 삽입 (인덱스에)
3. 인덱스 컬럼 수정 시 두 번의 작업 필요
```

## 6. 인덱스 사용 전략

### 6.1 인덱스 생성 기준
```
생성 권장:
✓ WHERE 절에 자주 사용되는 컬럼
✓ JOIN 조건으로 사용되는 컬럼
✓ ORDER BY, GROUP BY에 사용되는 컬럼
✓ 카디널리티가 높은 컬럼 (중복도 낮음)

생성 비권장:
✗ 자주 변경되는 컬럼
✗ 카디널리티가 낮은 컬럼 (성별 등)
✗ 데이터가 적은 테이블
✗ WHERE 절에 함수가 적용되는 컬럼
```

### 6.2 복합 인덱스 순서
```
원칙:
1. = (등가) 조건 컬럼을 앞에
2. 범위 조건(>, <, BETWEEN) 컬럼을 뒤에
3. 카디널리티 높은 컬럼을 앞에
4. 자주 사용되는 컬럼을 앞에

예:
WHERE 부서 = 'IT' AND 연봉 > 5000
→ INDEX (부서, 연봉)  ✓
→ INDEX (연봉, 부서)  ✗ (범위 조건 뒤에)
```

## 7. 인덱스 스캔 방식

```
1. Index Range Scan
   - 범위 검색
   - 가장 일반적인 방식

2. Index Full Scan
   - 인덱스 전체 스캔
   - 풀 테이블 스캔보다 빠름 (정렬됨)

3. Index Unique Scan
   - 유니크 인덱스 등가 검색
   - 최대 1건

4. Index Skip Scan
   - 선행 컬럼을 건너뛰고 스캔
   - MySQL 8.0+ 지원
```

## 8. 인덱스 힌트

```sql
-- MySQL
SELECT /*+ INDEX(학생 idx_학과) */ *
FROM 학생
WHERE 학과 = '컴퓨터공학';

-- Oracle
SELECT /*+ INDEX(학생 idx_학과) */ *
FROM 학생
WHERE 학과 = '컴퓨터공학';

-- PostgreSQL
SET enable_seqscan = off;
SELECT * FROM 학생 WHERE 학과 = '컴퓨터공학';
```

## 9. 코드 예시

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import bisect

@dataclass
class BPlusTreeNode:
    """B+Tree 노드"""
    keys: List[int]
    children: List['BPlusTreeNode']
    values: List[str]  # 리프 노드만 사용
    is_leaf: bool
    next_leaf: Optional['BPlusTreeNode'] = None  # 리프 노드 연결

class BPlusTree:
    """B+Tree 인덱스 시뮬레이션"""

    def __init__(self, order: int = 4):
        self.order = order
        self.root = BPlusTreeNode(keys=[], children=[], values=[], is_leaf=True)

    def search(self, key: int) -> Optional[str]:
        """키 검색"""
        node = self.root

        while not node.is_leaf:
            # 이진 탐색으로 자식 노드 결정
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]

        # 리프 노드에서 값 찾기
        try:
            idx = node.keys.index(key)
            return node.values[idx]
        except ValueError:
            return None

    def range_search(self, start: int, end: int) -> List[Tuple[int, str]]:
        """범위 검색"""
        results = []

        # 시작 키가 있는 리프 노드 찾기
        node = self._find_leaf(start)

        while node:
            for i, key in enumerate(node.keys):
                if start <= key <= end:
                    results.append((key, node.values[i]))
                elif key > end:
                    return results
            node = node.next_leaf

        return results

    def _find_leaf(self, key: int) -> BPlusTreeNode:
        """키가 있을 리프 노드 찾기"""
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]
        return node

    def insert(self, key: int, value: str):
        """키-값 삽입"""
        leaf = self._find_leaf(key)

        # 순서 유지하며 삽입
        idx = bisect.bisect_left(leaf.keys, key)
        leaf.keys.insert(idx, key)
        leaf.values.insert(idx, value)

        # 노드가 가득 차면 분할 (단순화)
        if len(leaf.keys) > self.order:
            self._split_leaf(leaf)

    def _split_leaf(self, node: BPlusTreeNode):
        """리프 노드 분할"""
        mid = len(node.keys) // 2

        # 새 노드 생성
        new_node = BPlusTreeNode(
            keys=node.keys[mid:],
            children=[],
            values=node.values[mid:],
            is_leaf=True,
            next_leaf=node.next_leaf
        )

        # 기존 노드 축소
        node.keys = node.keys[:mid]
        node.values = node.values[:mid]
        node.next_leaf = new_node

        # 실제로는 부모 노드에 키 전파 필요


class HashIndex:
    """해시 인덱스 시뮬레이션"""

    def __init__(self, size: int = 1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key: int) -> int:
        """해시 함수"""
        return key % self.size

    def insert(self, key: int, value: str):
        """삽입"""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        # 이미 있으면 업데이트
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def search(self, key: int) -> Optional[str]:
        """검색 - O(1) 평균"""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key: int) -> bool:
        """삭제"""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False


# 사용 예시
print("=== B+Tree 인덱스 테스트 ===")
bpt = BPlusTree(order=4)

# 데이터 삽입
for i in range(1, 11):
    bpt.insert(i, f"데이터{i}")

# 검색
print(f"키 5 검색: {bpt.search(5)}")
print(f"키 15 검색: {bpt.search(15)}")

# 범위 검색
print(f"범위 검색 (3~7): {bpt.range_search(3, 7)}")

print("\n=== 해시 인덱스 테스트 ===")
hi = HashIndex(size=10)

# 데이터 삽입
for i in range(1, 11):
    hi.insert(i * 100, f"값{i}")

# 검색
print(f"키 300 검색: {hi.search(300)}")
print(f"키 500 검색: {hi.search(500)}")
```

## 10. 인덱스 성능 분석

### 10.1 인덱스 사용 확인 (MySQL)
```sql
-- 실행 계획 확인
EXPLAIN SELECT * FROM 학생 WHERE 학과 = '컴퓨터공학';

-- 상세 실행 계획
EXPLAIN ANALYZE SELECT * FROM 학생 WHERE 학과 = '컴퓨터공학';

-- 인덱스 사용 통계
SHOW INDEX FROM 학생;
```

### 10.2 성능 비교
```
테이블: 100만 행
검색 조건: 1개 행 조회

풀 테이블 스캔:
- 디스크 I/O: 수만 번
- 시간: 수초

인덱스 사용:
- 디스크 I/O: 3-4번 (트리 깊이)
- 시간: 수밀리초
```

## 11. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 검색 속도 향상 | O(n) → O(log n) |
| 정렬 비용 절감 | 이미 정렬된 상태 |
| 중복 방지 | 유니크 인덱스 |

### 단점
| 단점 | 설명 |
|-----|------|
| 저장 공간 | 추가 디스크 사용 |
| 쓰기 성능 저하 | INSERT/UPDATE/DELETE 시 갱신 |
| 메모리 사용 | 버퍼 풀 사용 |

## 12. 실무에선? (기술사적 판단)
- **PK**: 자동으로 클러스터형 인덱스 생성
- **외래키**: 인덱스 생성 권장 (JOIN 성능)
- **카디널리티**: 높은 컬럼 우선
- **복합 인덱스**: 사용 패턴 분석 후 생성
- **모니터링**: 미사용 인덱스 제거
- **실무 비율**: 읽기 90% / 쓰기 10% → 인덱스 적극 활용

## 13. 관련 개념
- B+Tree
- 해싱
- 클러스터링
- 옵티마이저
- 실행 계획

---

## 어린이를 위한 종합 설명

**인덱스는 "책의 색인"이에요!**

### 책에서 찾기 📚
```
색인 없이:
"사과가 어디 있지?"
→ 책을 처음부터 끝까지 다 봐야 해요 😫

색인 사용:
"사과 → 45쪽"
→ 바로 찾을 수 있어요! 😊
```

### 인덱스 종류 🗂️
```
B+Tree 인덱스:
    ┌───┐
    │ 5 │
  ┌─┴─┴─┐
  ↓     ↓
 1~4   6~10
→ 숫자 크기로 정리

해시 인덱스:
"사과" → 3번 상자
"바나나" → 7번 상자
→ 이름으로 바로 찾기
```

### 인덱스를 언제 쓸까? 🤔
```
좋아요 ✓
- 자주 찾는 것
- 종류가 다양한 것

안 좋아요 ✗
- 가끔 찾는 것
- 종류가 별로 없는 것 (남/여)
```

### 단점도 있어요 😅
```
- 책이 두꺼워져요 (공간 필요)
- 새 내용 추가할 때 색인도 고쳐야 해요
```

**비밀**: 데이터베이스도 색인처럼 인덱스를 써서 빠르게 찾아요! 📖✨
