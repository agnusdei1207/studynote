+++
title = "데이터 모델링 (Data Modeling)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 데이터 모델링 (Data Modeling)

## 핵심 인사이트 (3줄 요약)
> **현실 세계의 데이터를 데이터베이스로 표현**하는 과정. 개념→논리→물리 모델링 단계로 진행. 좋은 모델링은 데이터 품질과 시스템 성능의 기초다.

## 1. 개념
데이터 모델링은 **현실 세계의 정보를 데이터베이스에 저장하기 위한 구조로 변환**하는 과정으로, 업무를 분석하고 데이터 구조를 설계한다.

> 비유: "건축 설계도" - 집을 짓기 전에 도면을 먼저 그리는 것

## 2. 데이터 모델링 단계

```
현실 세계
    │
    ▼
┌─────────────┐
│ 개념 모델링 │ → E-R 다이어그램
│ (Conceptual)│   엔티티, 속성, 관계 식별
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 논리 모델링 │ → 관계 스키마
│  (Logical)  │   정규화, 식별자 정의
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 물리 모델링 │ → DB 구축
│ (Physical)  │   인덱스, 파티셔닝
└─────────────┘
```

## 3. 개념 데이터 모델링

### 3.1 주요 용어
```
엔티티 (Entity):
- 업무에 필요한 유/무형의 객체
- 예: 학생, 과목, 교수

속성 (Attribute):
- 엔티티가 가진 성질
- 예: 학생번호, 이름, 학과

관계 (Relationship):
- 엔티티 간의 연관성
- 예: 수강(학생-과목)

식별자 (Identifier):
- 엔티티를 유일하게 구분하는 속성
- 예: 학생번호
```

### 3.2 E-R 다이어그램
```
┌─────────────┐          ┌─────────────┐
│   학생       │          │   과목       │
├─────────────┤          ├─────────────┤
│ 학번 (PK)    │          │ 과목코드(PK) │
│ 이름         │  ────<   │ 과목명       │
│ 학과         │  수강    │ 학점         │
│ 학년         │  >────   │ 담당교수     │
└─────────────┘          └─────────────┘
       │
       │ 1
       │
       │ N
┌──────┴──────┐
│   성적       │
├─────────────┤
│ 학번 (FK)    │
│ 과목코드(FK) │
│ 점수         │
└─────────────┘

기호:
▒▒▒▒ : 엔티티
───< : 관계 (N:M)
PK : 기본키
FK : 외래키
```

### 3.3 관계 카디널리티
```
1:1 (일대일)
┌─────┐     ┌─────┐
│사람  │─────│여권  │
└─────┘  1  └─────┘ 1

1:N (일대다)
┌─────┐     ┌─────┐
│부서  │─────│사원  │
└─────┘  1  └─────┘ N

N:M (다대다)
┌─────┐     ┌─────┐
│학생  │─────│과목  │
└─────┘  N  └─────┘ M
      ↓
  ┌───────┐
  │ 수강   │ (교차엔티티)
  └───────┘
```

## 4. 논리 데이터 모델링

### 4.1 관계형 모델 변환
```
E-R → 관계 스키마:

1. 엔티티 → 테이블
   학생(학번, 이름, 학과, 학년)

2. 1:N 관계 → 외래키
   부서(부서번호, 부서명)
   사원(사원번호, 이름, 부서번호 FK)

3. N:M 관계 → 교차 테이블
   학생(학번, 이름)
   과목(과목코드, 과목명)
   수강(학번 FK, 과목코드 FK, 점수)
```

### 4.2 식별자 분류
```
기본키 (Primary Key):
- 엔티티를 대표하는 유일한 식별자
- NOT NULL, UNIQUE

후보키 (Candidate Key):
- 기본키가 될 수 있는 속성들

대체키 (Alternate Key):
- 기본키가 아닌 후보키

슈퍼키 (Super Key):
- 유일성을 만족하는 속성 집합

외래키 (Foreign Key):
- 다른 테이블의 기본키 참조
```

## 5. 물리 데이터 모델링

### 5.1 고려사항
```
1. 데이터 타입
   - VARCHAR vs CHAR
   - NUMBER vs INTEGER
   - DATE vs TIMESTAMP

2. 인덱스 설계
   - 검색 빈도
   - 카디널리티
   - 갱신 빈도

3. 파티셔닝
   - 범위 파티션
   - 해시 파티션
   - 리스트 파티션

4. 반정규화
   - 성능 향상을 위한 구조 변경
```

## 6. 모델링 품질 기준

```
1. 완전성 (Completeness)
   - 모든 요구사항 반영

2. 정확성 (Correctness)
   - 현실 세계 정확히 표현

3. 최소성 (Minimality)
   - 불필요한 중복 제거

4. 자명성 (Self-explaining)
   - 명확한 명명 규칙

5. 확장성 (Extensibility)
   - 향후 변경 용이

6. 정규화 (Normalization)
   - 이상현상 방지
```

## 7. 명명 규칙

```
엔티티:
- 한글: 복수형 회피, 명확한 의미
- 영문: PascalCase, 복수형
- 예: 학생, Student

속성:
- 한글: 엔티티명 + 속성명
- 영문: snake_case
- 예: 학생번호, student_id

테이블:
- 접두어 활용 가능
- 예: TB_STUDENT, TB_COURSE
```

## 8. 코드 예시

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Cardinality(Enum):
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "N:M"

@dataclass
class Attribute:
    """속성 정의"""
    name: str
    data_type: str
    is_pk: bool = False
    is_fk: bool = False
    is_nullable: bool = True

@dataclass
class Entity:
    """엔티티 정의"""
    name: str
    attributes: List[Attribute]

    def get_primary_key(self):
        return [attr for attr in self.attributes if attr.is_pk]

    def get_foreign_keys(self):
        return [attr for attr in self.attributes if attr.is_fk]

    def to_sql(self):
        """CREATE TABLE 문 생성"""
        cols = []
        for attr in self.attributes:
            col = f"{attr.name} {attr.data_type}"
            if attr.is_pk:
                col += " PRIMARY KEY"
            if not attr.is_nullable and not attr.is_pk:
                col += " NOT NULL"
            cols.append(col)

        return f"CREATE TABLE {self.name} (\n  " + ",\n  ".join(cols) + "\n)"

@dataclass
class Relationship:
    """관계 정의"""
    name: str
    entity1: Entity
    entity2: Entity
    cardinality: Cardinality

    def describe(self):
        return f"{self.entity1.name} {self.cardinality.value} {self.entity2.name}"

class DataModel:
    """데이터 모델 관리"""

    def __init__(self):
        self.entities: List[Entity] = []
        self.relationships: List[Relationship] = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def add_relationship(self, relationship: Relationship):
        self.relationships.append(relationship)

    def generate_ddl(self):
        """전체 DDL 생성"""
        ddl = []
        for entity in self.entities:
            ddl.append(entity.to_sql())
        return "\n\n".join(ddl)

    def er_diagram_text(self):
        """텍스트 E-R 다이어그램"""
        output = []
        for entity in self.entities:
            output.append(f"\n[{entity.name}]")
            for attr in entity.attributes:
                pk_mark = "PK" if attr.is_pk else ""
                fk_mark = "FK" if attr.is_fk else ""
                output.append(f"  {attr.name} {pk_mark}{fk_mark}")

        for rel in self.relationships:
            output.append(f"\n{rel.describe()}")

        return "\n".join(output)


# 모델링 예시
model = DataModel()

# 학생 엔티티
student = Entity("학생", [
    Attribute("학번", "CHAR(10)", is_pk=True),
    Attribute("이름", "VARCHAR(20)", is_nullable=False),
    Attribute("학과", "VARCHAR(30)"),
    Attribute("학년", "INTEGER"),
])

# 과목 엔티티
course = Entity("과목", [
    Attribute("과목코드", "CHAR(10)", is_pk=True),
    Attribute("과목명", "VARCHAR(50)", is_nullable=False),
    Attribute("학점", "INTEGER"),
])

# 수강 엔티티 (교차 테이블)
enrollment = Entity("수강", [
    Attribute("학번", "CHAR(10)", is_pk=True, is_fk=True),
    Attribute("과목코드", "CHAR(10)", is_pk=True, is_fk=True),
    Attribute("점수", "INTEGER"),
])

# 엔티티 추가
model.add_entity(student)
model.add_entity(course)
model.add_entity(enrollment)

# 관계 정의
model.add_relationship(Relationship("수강", student, enrollment, Cardinality.ONE_TO_MANY))
model.add_relationship(Relationship("개설", course, enrollment, Cardinality.ONE_TO_MANY))

# 결과 출력
print("=== E-R 다이어그램 ===")
print(model.er_diagram_text())

print("\n=== DDL ===")
print(model.generate_ddl())
```

## 9. 장단점

### 체계적 모델링의 장점
| 장점 | 설명 |
|-----|------|
| 데이터 일관성 | 정규화로 이상현상 방지 |
| 유지보수성 | 명확한 구조 파악 |
| 성능 최적화 | 적절한 인덱스 설계 |
| 의사소통 | 표준화된 표현 |

### 모델링의 주의점
| 주의점 | 설명 |
|-----|------|
| 과도한 정규화 | 성능 저하 가능 |
| 명명 불일치 | 혼란 야기 |
| 요구사항 누락 | 재작업 |

## 10. 실무에선? (기술사적 판단)
- **개념 모델링**: 업무 분석 중심, 도구: ERwin, draw.io
- **논리 모델링**: 정규화 수행, 이상현상 제거
- **물리 모델링**: 성능 고려, 반정규화 검토
- **도구**: ERDCloud, ERwin, PowerDesigner

## 11. 관련 개념
- 정규화
- E-R 다이어그램
- 엔티티
- 식별자

---

## 어린이를 위한 종합 설명

**데이터 모델링은 "장난감 정리 계획"이에요!**

### 3단계 계획 📋
```
1단계 (개념): 무슨 장난감이 있지?
   - 자동차, 인형, 블록...

2단계 (논리): 어떻게 나눌까?
   - 자동차 → 상자1
   - 인형 → 상자2
   - 블록 → 상자3

3단계 (물리): 상자를 어디에 둘까?
   - 자주 쓰는 건 앞에
   - 무거운 건 아래에
```

### E-R 다이어그램 📊
```
┌─────┐     ┌─────┐
│학생  │─────│과목  │
└─────┘     └─────┘

네모: 학생, 과목 같은 것들
선: 연결 관계
```

### 정규화는? 🧹
```
중복 제거!

나쁜 예:
홍길동 | 컴퓨터공학 | 1학년 | 컴퓨터공학
           ↑ 중복!

좋은 예:
학생: 홍길동 | 학과1
학과: 학과1 | 컴퓨터공학
```

**비밀**: 좋은 모델링은 나중에 고생 안 해요! 🏗️✨
