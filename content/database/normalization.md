+++
title = "정규화 (Normalization)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 정규화 (Normalization)

## 핵심 인사이트 (3줄 요약)
> **데이터 중복을 최소화하고 이상현상을 방지**하는 데이터베이스 설계 기법. 함수적 종속성을 분석하여 단계적으로 정규형으로 분해. 제1정규형부터 제5정규형, BCNF까지 있다.

## 1. 개념
정규화는 **데이터베이스에서 중복을 제거하고 이상현상(Anomaly)을 방지**하기 위해 테이블을 적절하게 분해하는 과정이다.

> 비유: "중복 제거 정리" - 같은 물건이 여러 곳에 있으면 헷갈리니 하나만 두기

## 2. 이상현상 (Anomaly)

### 2.1 삽입 이상 (Insertion Anomaly)
```
문제: 데이터를 삽입하기 위해 불필요한 데이터 필요

예: 학생(학번, 이름, 학과, 학과장)

새 학생 추가 시 학과장도 같이 입력해야 함
→ 아직 학과가 정해지지 않으면 삽입 불가!
```

### 2.2 삭제 이상 (Deletion Anomaly)
```
문제: 데이터 삭제 시 원하지 않는 정보도 함께 삭제

예: 어떤 학과의 마지막 학생을 삭제
→ 그 학과의 정보(학과장 등)도 함께 사라짐!
```

### 2.3 수정 이상 (Update Anomaly)
```
문제: 중복 데이터 일부만 수정되어 불일치 발생

예: 학과장이 변경됨
→ 그 학과의 모든 학생 레코드를 수정해야 함
→ 하나라도 누락하면 데이터 불일치!
```

## 3. 함수적 종속성 (Functional Dependency)

```
정의: X → Y
X의 값이 결정되면 Y의 값도 결정됨

예: 학번 → 이름, 학과
(학번이 정해지면 이름과 학과도 정해짐)

완전 함수 종속:
- Y가 X 전체에 종속 (일부분 X' → Y 불가)

부분 함수 종속:
- Y가 X의 일부분에 종속

이행 함수 종속:
- X → Y, Y → Z 이면 X → Z
```

## 4. 정규형 단계

```
┌─────────────────────────────────────┐
│            1NF (제1정규형)          │
│        원자성 (Atomicity)           │
├─────────────────────────────────────┤
│            2NF (제2정규형)          │
│     부분 함수 종속 제거              │
├─────────────────────────────────────┤
│            3NF (제3정규형)          │
│     이행 함수 종속 제거              │
├─────────────────────────────────────┤
│           BCNF (Boyce-Codd)         │
│     결정자 후보키 조건               │
├─────────────────────────────────────┤
│            4NF (제4정규형)          │
│     다치 종속 제거                   │
├─────────────────────────────────────┤
│            5NF (제5정규형)          │
│     조인 종속 제거                   │
└─────────────────────────────────────┘
```

## 5. 각 정규형 상세

### 5.1 제1정규형 (1NF)
```
조건: 모든 속성이 원자값을 가져야 함

비정규형:
┌────────┬────────────────────┐
│ 학번   │        과목         │
├────────┼────────────────────┤
│ 001    │ 수학, 영어, 과학    │ ← 복수 값
└────────┴────────────────────┘

1NF:
┌────────┬────────┐
│ 학번   │  과목  │
├────────┼────────┤
│ 001    │  수학  │
│ 001    │  영어  │
│ 001    │  과학  │
└────────┴────────┘
```

### 5.2 제2정규형 (2NF)
```
조건: 1NF + 부분 함수 종속 제거
      (복합키인 경우 모든 비키 속성이 전체 키에 종속)

비정규형 (복합키: 학번+과목코드):
┌────────┬──────────┬────────┬────────┐
│ 학번   │ 과목코드 │ 성적   │ 과목명  │
├────────┼──────────┼────────┼────────┤
│ 001    │ A01      │ 90     │ 수학    │
└────────┴──────────┴────────┴────────┘

문제:
- (학번+과목코드) → 성적 ✓
- 과목코드 → 과목명 ✗ (부분 종속)

2NF 분해:
성적(학번, 과목코드, 성적)
과목(과목코드, 과목명)
```

### 5.3 제3정규형 (3NF)
```
조건: 2NF + 이행 함수 종속 제거

비정규형:
┌────────┬────────┬────────┐
│ 학번   │ 학과   │ 학과장  │
├────────┼────────┼────────┤
│ 001    │ 컴공   │ 김교수  │
└────────┴────────┴────────┘

문제:
- 학번 → 학과
- 학과 → 학과장
- ∴ 학번 → 학과장 (이행 종속)

3NF 분해:
학생(학번, 학과)
학과(학과, 학과장)
```

### 5.4 BCNF (Boyce-Codd Normal Form)
```
조건: 3NF + 모든 결정자가 후보키

비정규형:
┌────────┬────────┬────────┐
│ 학번   │ 과목   │ 교수   │
├────────┼────────┼────────┤
│ 001    │ 수학   │ 김교수  │
│ 002    │ 수학   │ 김교수  │
└────────┴────────┴────────┘

문제:
- (학번, 과목) → 교수
- 교수 → 과목 (교수는 과목을 하나만 가르침)
- 교수는 결정자이지만 후보키가 아님!

BCNF 분해:
수강(학번, 교수)
교수(교수, 과목)
```

### 5.5 제4정규형 (4NF)
```
조건: BCNF + 다치 종속(MVD) 제거

다치 종속:
X →→ Y: X 값이 하나면 Y값이 여러 개 독립적으로 결정

비정규형:
┌────────┬────────┬────────┐
│ 학생   │ 과목   │ 동아리  │
├────────┼────────┼────────┤
│ 철수   │ 수학   │ 축구    │
│ 철수   │ 수학   │ 음악    │
│ 철수   │ 영어   │ 축구    │
│ 철수   │ 영어   │ 음악    │
└────────┴────────┴────────┘

과목과 동아리가 독립적으로 다치 종속

4NF 분해:
수강(학생, 과목)
동아리(학생, 동아리)
```

## 6. 정규화 예시

```
비정규형 테이블:
주문(주문번호, 고객번호, 고객명, 주소, 상품코드, 상품명, 수량, 단가)

함수적 종속:
- 주문번호 → 고객번호, 고객명, 주소
- 고객번호 → 고객명, 주소 (이행 종속)
- 상품코드 → 상품명, 단가
- (주문번호, 상품코드) → 수량

정규화 과정:

1NF: 이미 만족 (원자값)

2NF 분해 (부분 종속 제거):
주문(주문번호, 고객번호, 고객명, 주소)
주문상세(주문번호, 상품코드, 수량)
상품(상품코드, 상품명, 단가)

3NF 분해 (이행 종속 제거):
주문(주문번호, 고객번호)
고객(고객번호, 고객명, 주소)
주문상세(주문번호, 상품코드, 수량)
상품(상품코드, 상품명, 단가)
```

## 7. 코드 예시

```python
from dataclasses import dataclass
from typing import List, Set, Tuple

@dataclass
class FunctionalDependency:
    """함수적 종속성"""
    determinant: Set[str]  # 결정자 (X)
    dependent: Set[str]    # 종속자 (Y)

    def __str__(self):
        det = ','.join(sorted(self.determinant))
        dep = ','.join(sorted(self.dependent))
        return f"{det} → {dep}"

class NormalizationAnalyzer:
    """정규화 분석기"""

    def __init__(self, attributes: Set[str], fds: List[FunctionalDependency]):
        self.attributes = attributes
        self.fds = fds

    def find_candidate_keys(self) -> List[Set[str]]:
        """후보키 찾기"""
        from itertools import combinations

        candidate_keys = []
        for size in range(1, len(self.attributes) + 1):
            for subset in combinations(self.attributes, size):
                subset = set(subset)
                closure = self._compute_closure(subset)

                if closure == self.attributes:
                    # 최소성 검사
                    is_minimal = True
                    for ck in candidate_keys:
                        if ck.issubset(subset):
                            is_minimal = False
                            break

                    if is_minimal:
                        candidate_keys.append(subset)

        return candidate_keys

    def _compute_closure(self, attributes: Set[str]) -> Set[str]:
        """속성 폐포 계산"""
        closure = set(attributes)
        changed = True

        while changed:
            changed = False
            for fd in self.fds:
                if fd.determinant.issubset(closure):
                    if not fd.dependent.issubset(closure):
                        closure.update(fd.dependent)
                        changed = True

        return closure

    def check_1nf(self, table_data: List[dict]) -> bool:
        """1NF 검사"""
        for row in table_data:
            for value in row.values():
                if isinstance(value, (list, set, tuple)):
                    return False
        return True

    def find_partial_dependencies(self, pk: Set[str]) -> List[FunctionalDependency]:
        """부분 함수 종속 찾기"""
        partial = []
        for fd in self.fds:
            if fd.determinant.issubset(pk) and fd.determinant != pk:
                partial.append(fd)
        return partial

    def find_transitive_dependencies(self, pk: Set[str]) -> List[Tuple]:
        """이행 함수 종속 찾기"""
        transitive = []

        # X → Y, Y → Z 인데 X → Z인 경우
        for fd1 in self.fds:
            if fd1.determinant.issubset(pk):
                for fd2 in self.fds:
                    if fd2.determinant == fd1.dependent:
                        if not fd2.determinant.issubset(pk):
                            transitive.append((fd1, fd2))

        return transitive

    def analyze(self):
        """정규화 분석"""
        print("=== 정규화 분석 ===")
        print(f"속성: {self.attributes}")

        print("\n함수적 종속성:")
        for fd in self.fds:
            print(f"  {fd}")

        candidate_keys = self.find_candidate_keys()
        print(f"\n후보키: {[','.join(sorted(ck)) for ck in candidate_keys]}")

        if candidate_keys:
            pk = candidate_keys[0]
            print(f"\n기본키: {','.join(sorted(pk))}")

            partial = self.find_partial_dependencies(pk)
            print(f"\n부분 함수 종속: {[str(p) for p in partial]}")

            transitive = self.find_transitive_dependencies(pk)
            print(f"이행 함수 종속: {[(str(t[0]), str(t[1])) for t in transitive]}")

# 분석 예시
print("=== 주문 테이블 정규화 분석 ===\n")

attributes = {'주문번호', '고객번호', '고객명', '주소', '상품코드', '상품명', '수량', '단가'}

fds = [
    FunctionalDependency({'주문번호'}, {'고객번호', '고객명', '주소'}),
    FunctionalDependency({'고객번호'}, {'고객명', '주소'}),
    FunctionalDependency({'상품코드'}, {'상품명', '단가'}),
    FunctionalDependency({'주문번호', '상품코드'}, {'수량'}),
]

analyzer = NormalizationAnalyzer(attributes, fds)
analyzer.analyze()
```

## 8. 반정규화 (Denormalization)

```
정규화의 역과정: 성능 향상을 위해 중복 허용

반정규화 기법:
1. 테이블 병합
2. 중복 컬럼 추가
3. 파생 컬럼 추가
4. 요약 테이블 생성

주의:
- 데이터 일관성 유지 필요
- 트리거/배치로 동기화
```

## 9. 장단점

### 정규화 장점
| 장점 | 설명 |
|-----|------|
| 중복 제거 | 저장 공간 절약 |
| 이상현상 방지 | 데이터 일관성 |
| 유지보수 용이 | 구조 명확 |

### 정규화 단점
| 단점 | 설명 |
|-----|------|
| 조인 증가 | 조회 성능 저하 |
| 복잡한 쿼리 | SQL 작성 어려움 |

## 10. 실무에선? (기술사적 판단)
- **OLTP**: 3NF까지 정규화 권장
- **OLAP**: 반정규화 허용 (성능 중심)
- **실무**: 3NF + 필요시 반정규화
- **트레이드오프**: 정규화 vs 성능

## 11. 관련 개념
- 함수적 종속성
- 이상현상
- 반정규화
- 후보키

---

## 어린이를 위한 종합 설명

**정규화는 "중복 없이 정리하기"야!**

### 이상현상 (이상해요!) 😵
```
삽입 이상:
"학생을 추가하고 싶은데 학과 정보도 넣어야 해?"

삭제 이상:
"마지막 학생을 지웠더니 학과 정보도 사라졌어!"

수정 이상:
"학과장이 바뀌었는데 100명의 학생 정보를 다 고쳐야 해?"
```

### 정규화 단계 📊
```
1NF: 한 칸에 하나만!
    나쁨: 사과, 배, 포도
    좋음: 사과 | 배 | 포도 (각각 따로)

2NF: 복합키일 때 모두에 종속해야 함
    (학번+과목) → 성적 ✓
    과목만 → 과목명 ✗

3NF: 직접 관계만!
    학번 → 학과 → 학과장
    → 분리해야 함!
```

### 쉬운 예시 📚
```
비정규형:
학생 | 학과 | 학과장
철수 | 컴공 | 김교수
영희 | 컴공 | 김교수 ← 중복!

정규화:
학생(학생, 학과)
학과(학과, 학과장)
```

**비밀**: 정규화하면 데이터가 깔끔해져요! ✨
