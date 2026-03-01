+++
title = "데이터베이스 관리 시스템 (DBMS)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 데이터베이스 관리 시스템 (DBMS)

## 핵심 인사이트 (3줄 요약)
> **데이터를 효율적으로 저장, 관리, 검색**하는 소프트웨어 시스템. 데이터 독립성, 무결성, 보안, 동시성 제어 기능 제공. RDBMS, NoSQL, NewSQL 등 다양한 유형이 있다.

## 1. 개념
DBMS(Database Management System)는 **데이터베이스를 생성, 관리, 운영하는 소프트웨어**로, 사용자와 데이터베이스 사이에서 데이터를 효율적으로 관리하는 중개자 역할을 한다.

> 비유: "도서관 관리 시스템" - 책(데이터)을 체계적으로 저장하고 필요할 때 찾아줌

## 2. 등장 배경
```
파일 시스템의 문제점:
1. 데이터 중복 (Redundancy)
2. 데이터 불일치 (Inconsistency)
3. 데이터 종속성 (Dependency)
4. 접근 제어 어려움
5. 동시 접근 문제

DBMS의 해결:
- 데이터 통합 관리
- 논리/물리적 독립성
- 중복 최소화
- 무결성 보장
```

## 3. DBMS 구조

### 3.1 3단계 스키마 구조
```
┌─────────────────────────────────────┐
│        외부 스키마 (External)        │ ← 사용자 뷰
│    View 1    View 2    View 3       │
├─────────────────────────────────────┤
│        개념 스키마 (Conceptual)      │ ← 전체 논리 구조
│         테이블, 관계, 제약조건        │
├─────────────────────────────────────┤
│        내부 스키마 (Internal)        │ ← 물리 저장 구조
│      인덱스, 블록, 파일 구조          │
└─────────────────────────────────────┘

외부/개념 매핑: 논리적 독립성
개념/내부 매핑: 물리적 독립성
```

### 3.2 DBMS 구성 요소
```
┌────────────────────────────────────────────┐
│              응용 프로그램                  │
└─────────────────┬──────────────────────────┘
                  │ SQL
┌─────────────────▼──────────────────────────┐
│              질의 처리기                     │
│  ┌─────────┬─────────┬─────────┐          │
│  │ DDL컴파일│ DML컴파일│ 질의최적화│          │
│  └─────────┴─────────┴─────────┘          │
├────────────────────────────────────────────┤
│              저장 데이터 관리자             │
│  ┌─────────┬─────────┬─────────┐          │
│  │ 버퍼관리 │ 파일관리 │ 인덱스   │          │
│  └─────────┴─────────┴─────────┘          │
├────────────────────────────────────────────┤
│              디스크 저장소                  │
│  데이터 파일 │ 인덱스 파일 │ 로그 파일      │
└────────────────────────────────────────────┘
```

## 4. DBMS 주요 기능

### 4.1 데이터 정의 (DDL)
```sql
-- CREATE: 객체 생성
CREATE TABLE 학생 (
    학번 CHAR(10) PRIMARY KEY,
    이름 VARCHAR(20) NOT NULL,
    학과 VARCHAR(30)
);

-- ALTER: 객체 수정
ALTER TABLE 학생 ADD 이메일 VARCHAR(50);

-- DROP: 객체 삭제
DROP TABLE 학생;
```

### 4.2 데이터 조작 (DML)
```sql
-- SELECT: 조회
SELECT * FROM 학생 WHERE 학과 = '컴퓨터공학';

-- INSERT: 삽입
INSERT INTO 학생 VALUES ('2024001', '홍길동', '컴퓨터공학');

-- UPDATE: 수정
UPDATE 학생 SET 학과 = '전자공학' WHERE 학번 = '2024001';

-- DELETE: 삭제
DELETE FROM 학생 WHERE 학번 = '2024001';
```

### 4.3 데이터 제어 (DCL)
```sql
-- GRANT: 권한 부여
GRANT SELECT, INSERT ON 학생 TO user1;

-- REVOKE: 권한 회수
REVOKE INSERT ON 학생 FROM user1;
```

## 5. DBMS 특성

### 5.1 데이터 독립성
```
논리적 독립성:
- 응용 프로그램 변경 없이 데이터 구조 변경 가능
- 외부 스키마가 개념 스키마 변화에 영향 없음

물리적 독립성:
- 데이터 저장 구조 변경이 응용 프로그램에 영향 없음
- 개념 스키마가 내부 스키마 변화에 영향 없음
```

### 5.2 데이터 무결성
```
개체 무결성: 기본키는 NULL 불가, 중복 불가
참조 무결성: 외래키는 참조하는 값이거나 NULL
도메인 무결성: 속성 값은 정의된 도메인 내 값
사용자 정의 무결성: 비즈니스 규칙에 따른 제약
```

### 5.3 동시성 제어
```
목적: 다수 사용자의 동시 접근 시 데이터 일관성 유지

기법:
- 로킹 (Locking)
- MVCC (다중 버전 동시성 제어)
- 타임스탬프
- 낙관적 검증
```

### 5.4 회복 (Recovery)
```
목적: 장애 발생 시 데이터 일관성 있는 상태로 복원

기법:
- 로그 기반 회복
- 체크포인트
- 그림자 페이징
- ARIES 알고리즘
```

## 6. DBMS 종류

### 6.1 관계형 DBMS (RDBMS)
| 제품 | 특징 | 용도 |
|------|------|------|
| Oracle | 대용량, 고가용성 | 대기업 |
| MySQL | 오픈소스, 가볍다 | 웹서비스 |
| PostgreSQL | 객체관계형, 확장성 | 복잡한 쿼리 |
| SQL Server | Microsoft 환경 | 윈도우 기반 |
| MariaDB | MySQL 호환, 오픈소스 | 범용 |

### 6.2 NoSQL DBMS
| 유형 | 제품 | 특징 |
|------|------|------|
| 문서형 | MongoDB | JSON 문서 저장 |
| 키-값 | Redis | 인메모리, 빠름 |
| 컬럼 | Cassandra | 대용량 분산 |
| 그래프 | Neo4j | 관계 분석 |

## 7. RDBMS vs NoSQL

| 항목 | RDBMS | NoSQL |
|------|-------|-------|
| 스키마 | 고정 | 유연 |
| 확장성 | 수직 | 수평 |
| 일관성 | 강한 | 결과적 |
| 쿼리 | SQL | 다양 |
| 트랜잭션 | ACID | BASE |
| 적합한 데이터 | 정형 | 비정형 |

## 8. 코드 예시

```python
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    """DBMS 연결 관리자"""

    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        """컨텍스트 매니저로 연결 관리"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def create_table(self):
        """테이블 생성 (DDL)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    department TEXT,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def insert(self, name, department, email):
        """데이터 삽입 (DML - INSERT)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, department, email)
                VALUES (?, ?, ?)
            ''', (name, department, email))
            return cursor.lastrowid

    def select_all(self):
        """데이터 조회 (DML - SELECT)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students')
            return [dict(row) for row in cursor.fetchall()]

    def update(self, student_id, department):
        """데이터 수정 (DML - UPDATE)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students SET department = ?
                WHERE id = ?
            ''', (department, student_id))
            return cursor.rowcount

    def delete(self, student_id):
        """데이터 삭제 (DML - DELETE)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            return cursor.rowcount

# 사용 예시
db = DatabaseManager('example.db')
db.create_table()

# 삽입
student_id = db.insert('홍길동', '컴퓨터공학', 'hong@example.com')
print(f"삽입된 학생 ID: {student_id}")

# 조회
students = db.select_all()
print(f"전체 학생: {students}")

# 수정
db.update(student_id, '전자공학')

# 삭제
db.delete(student_id)
```

## 9. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 데이터 독립성 | 논리/물리적 독립성 |
| 데이터 공유 | 다수 사용자 동시 접근 |
| 무결성 보장 | 제약조건을 통한 품질 유지 |
| 보안 | 접근 제어 기능 |
| 백업/회복 | 장애 대비 |

### 단점
| 단점 | 설명 |
|-----|------|
| 비용 | 라이선스, 하드웨어 |
| 복잡성 | 학습 곡선 |
| 성능 | 오버헤드 |
| 전문성 | 관리 인력 필요 |

## 10. 실무에선? (기술사적 판단)
- **대기업**: Oracle, SQL Server (안정성, 지원)
- **스타트업**: MySQL, PostgreSQL (비용, 유연성)
- **빅데이터**: NoSQL + RDBMS 하이브리드
- **실시간**: Redis, Memcached (캐싱)

## 11. 관련 개념
- SQL
- 정규화
- 트랜잭션
- 인덱스

---

## 어린이를 위한 종합 설명

**DBMS는 "스마트한 장난감 정리함"이에요!**

### 파일 시스템 vs DBMS 📁
```
파일 시스템:
- 장난감을 아무 데나 둬요
- 찾을 때 오래 걸려요 😫

DBMS:
- 종류별로 정리해 둬요
- "자동차 장난감 어디 있어?" → 바로 찾아줘요! 😊
```

### DBMS가 해주는 일 🤖
```
1. 정리: 데이터를 체계적으로 저장
2. 검색: 원하는 데이터 빠르게 찾기
3. 보안: 허락된 사람만 접근
4. 백업: 잃어버려도 복구
```

### 종류 📚
```
관계형(RDBMS): 엑셀처럼 표로 정리
NoSQL: 자유로운 형태로 저장

예:
- MySQL, Oracle: 관계형
- MongoDB: 문서형
- Redis: 빠른 저장
```

**비밀**: 게임, 은행, 쇼핑몰 모두 DBMS를 써요! 🎮🏦✨
