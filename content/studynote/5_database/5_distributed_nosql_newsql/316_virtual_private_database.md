+++
title = "316. 가상 프라이빗 데이터베이스 (VPD) - 보이지 않는 보안의 벽"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 316
+++

# 316. 가상 프라이빗 데이터베이스 (VPD, Virtual Private Database)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VPD (Virtual Private Database)는 데이터베이스 관리 시스템(DBMS)의 커널 레벨에서 사용자의 SQL 질의를 가로채어, **보안 정책에 따라 동적으로 WHERE 절(Predicate)을 주입(Rewrite)**함으로써, 사용자별로 볼 수 있는 데이터 행(Row)이나 열(Column)을 제한하는 **FGAC (Fine-Grained Access Control)** 솔루션이다.
> 2. **가치**: 애플리케이션 코드 수정 없이 DB 레벨에서 보안 정책을 중앙 집중화하여, **개발 생산성을 30% 이상 향상**시키고 보안 누락(Leakage) 리스크를 0%에 가깝게 만든다. 또한 인덱스를 활용한 필터링으로 성능 저하를 최소화한다.
> 3. **융합**: 멀티테넌트(Multi-tenant) 클라우드 아키텍처와 결합하여 논리적 데이터 격리를 구현하며, `Oracle RLS (Row Level Security)`나 `PostgreSQL Policy`와 같은 표준화된 기술로 발전하고 있다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
VPD (Virtual Private Database)는 데이터베이스 내의 데이터에 접근하는 모든 SQL 문(SELECT, INSERT, UPDATE, DELETE)을 실행하기 전에, DBMS 엔진이 자동으로 보안 규칙을 적용하여 가상의 개인 데이터베이스처럼 보이게 만드는 기술이다. 이는 단순한 권한 부여(Grant)가 아닌, 데이터의 내용(Value) 자체를 기반으로 접근을 통제하는 **FGAC (Fine-Grained Access Control)**의 핵심 구현체이다.

**💡 비유: 투명한 마법 필터**
일반적인 보안은 '출입 카드'를 찍어 건물 출입을 허용하는 것이지만, VPD는 건물 안으로 들어와서 **'자신의 사무실 층만 볼 수 있는 스마트 글래스'**를 쓰게 하는 것과 같다. 사용자는 모든 데이터가 있는 줄 알지만, 실제로는 보안 정책에 따라 자신에게 허락된 데이터만 화면에 투영된다.

**등장 배경 및 필요성**
① **기존 한계**: 애플리케이션 레벨에서 `WHERE user_id = ?` 조건을 개발자가 실수로 누락하면 정보 유출 사고로 이어진다.
② **혁신적 패러다임**: 데이터베이스 엔진(Engine) 레벨에서 질의를 재작성(Query Rewrite)하여, 애플리케이션 로직과 무관하게 강제로 보안을 적용하는 'Defense in Depth(심층 방어)' 전략이 도입되었다.
③ **비즈니스 요구**: SaaS(Software as a Service) 환경에서 다수의 고객(Tenant)이 하나의 DB를 공유하되, 데이터는 철저히 분리되어야 하는 **멀티테넌시(Multi-tenancy)** 요구가 증가했다.

**📢 섹션 요약 비유**
VPD는 **'입국 심사대의 자동 보안 검색대'**와 같습니다. 여권(로그인 정보)을 제시하면, 검색대 시스템(VPD)이 자동으로 당신이 갈 수 있는 구역으로만 이동 경로(SQL)를 수정해주고, 허되지 않은 곳은 아예 지도에서 지워버리는 원리입니다.

```text
[ Security Evolution ]

[ Level 1: Object Privilege ]
  GRANT SELECT ON Table TO User;  -> 테이블 단위 접근 (All or Nothing)

[ Level 2: View (Virtual Table) ]
  CREATE VIEW User_View AS SELECT * FROM Table WHERE ID = User; -> 관리 복잡, 유지보수 어려움

[ Level 3: VPD (Dynamic Policy) ]
  DB Engine Hooking -> Dynamic Predicate Injection -> Context-Aware Security
```

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

VPD의 동작은 **PAR (Parsing)** 단계와 **EXEC (Execution)** 단계 사이의 **Pars** 훅(Hook) 지점에서 이루어진다.

**구성 요소 상세**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/키워드 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **1. Application Context** | 세션 변수 저장소 | 세션마다 부여된 식별자(ID, Role) 등을 메모리에 저장 (`SYS_CONTEXT`) | `NAMESPACE`, `ATTRIBUTE` | 여권 정보 칩 |
| **2. Policy Function** | 보안 규칙 판별기 | PL/SQL 또는 Java로 작성되며, Context를 참조하여 반환할 WHERE 절 문자열 생성 | `Predicate` | 심사관 규칙집 |
| **3. Policy Group** | 정책 묶음 | 테이블/객체별로 함수를 매핑. 하나의 객체에 여러 정책(Policy) 적용 가능 | `DBMS_RLS` | 심사 대별 배정 |
| **4. Query Rewrite Engine** | 쿼리 변환기 | Optimizer가 실행 계획을 세우기 전, 원본 SQL에 Function에서 반환된 절을 추가 | SQL Transformation | 자동 소포 포장기 |
| **5. Shared Pool** | 라이브러리 캐시 | 동일한 Policy를 가진 세션끼리 파싱된 커서(Cursor)를 공유하여 성능 향상 | `Hard Parse` 최적화 | 검색대 대기열 |

**핵심 아키텍처: VPD 동작 사이클 (ASCII)**

```text
┌───────────────────────────────────────────────────────────────────────┐
│                        VPD Execution Flow                             │
└───────────────────────────────────────────────────────────────────────┘

 [ User Session ]       [ DB Kernel (SGA) ]            [ Data Dictionary ]
       │                        │                              │
       │  1. Login              │                              │
       ├───────────────────────>│                              │
       │  (Set Context)         │                              │
       │                        │                              │
       │  2. SQL Issue          │                              │
       │  "SELECT * FROM Emp"   │                              │
       ├───────────────────────>│                              │
       │                        │                              │
       │                        │  3. Policy Check             │
       │                        │  (Is VPD attached?)          │
       │                        │─────────────────────────────>│
       │                        │                              │
       │                        │  4. Function Execution       │
       │                        │  (Get Predicate String)      │
       │                        │<─────────────────────────────│
       │                        │  Result: "WHERE dept = 10"   │
       │                        │                              │
       │                        │  5. Query Rewrite             │
       │                        │  Original: SELECT * FROM Emp  │
       │                        │  + Predicate                 │
       │                        │  = Modified SQL               │
       │                        │                              │
       │                        │  6. Optimizing & Executing   │
       │                        │  (Access Path Decision)      │
       │                        │                              │
       │  7. Result Set         │                              │
       │<───────────────────────│  (Filtered Rows Only)        │
       │                        │                              │
       ▼                        ▼                              ▼
```

**심층 동작 원리 (Step-by-Step)**

1.  **Context Setting**: 사용자 인증 후 `DBMS_SESSION.SET_CONTEXT` 프로시저를 통해 현재 사용자의 `USER_ID`, `IP_ADDR`, `ROLE` 등을 메모리 영역에 저장한다.
2.  **Policy Invocation**: 사용자가 `SELECT` 등의 SQL을 실행하면, Oracle은 해당 테이블에 연결된 Policy가 있는지 `SYS.DBA_POLICIES` 뷰를 참조하여 확인한다.
3.  **Predicate Generation**: Policy Function이 실행된다. 이 함수는 현재 Context를 읽어(ex: `SYS_CONTEXT('USERENV', 'SESSION_USER')`) 문자열 형태의 조건절(예: `deptno = 20`)을 반환값으로 돌려준다.
4.  **Query Transformation (Rewrite)**:
    -   **Original**: `SELECT * FROM scott.emp`
    -   **Rewritten**: `SELECT * FROM scott.emp WHERE (deptno = 20)`
    -   **Optimizer의 역할**: 변환된 SQL은 마치 사용자가 처음에 이렇게 입력한 것처럼 취급되어, `WHERE deptno = 20` 조건에 맞는 인덱스(존재 시)를 사용하거나 Full Table Scan을 결정한다. **즉, VPD는 성능을 저하시키는 것이 아니라 오히려 범위를 줄여 성능을 높일 수도 있다.**
5.  **Data Access & Return**: 데이터 파일에서 데이터를 읽을 때 이미 VPD 조건이 합쳐져 있으므로, 권한 없는 Row는 읽조차 하지 않거나(Fetch 단계에서 필터링), 결과 집합에서 제외된다.

**핵심 알고리즘 및 코드**

```sql
-- [VPD Policy Function 예시: PL/SQL]
-- 목적: 현재 세션 사용자가 속한 부서의 데이터만 반환
CREATE OR REPLACE FUNCTION auth_dept (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) RETURN VARCHAR2 IS
    v_pred VARCHAR2(2000);
BEGIN
    -- 1. Application Context에서 사용자 부서 ID 획득
    -- 만약 Context 설정이 안 되어 있으면 무조건 거짓(0=1)을 반환하여 아무 데이터도 안 보이게 함
    RETURN 'dept_id = SYS_CONTEXT(''USER_CTX'', ''DEPT_ID'')';
END;
/

-- [VPD Policy 등록]
BEGIN
    DBMS_RLS.ADD_POLICY (
        object_schema   => 'hr',            -- 대상 스키마
        object_name     => 'employees',     -- 대상 테이블/뷰
        policy_name     => 'emp_dept_policy', -- 정책 이름
        function_schema => 'sec_admin',    -- 함수 소유자
        policy_function => 'auth_dept',    -- 실행할 함수명
        statement_types => 'SELECT, UPDATE', -- 적용할 SQL 타입
        enable          => TRUE            -- 활성화 여부
    );
END;
/
```

**📢 섹션 요약 비유**
VPD의 아키텍처는 **'자율 주행 자동차의 내비게이션'**과 같습니다. 사용자(운전자)는 목적지만 입력(질의)하지만, 내비게이션(Policy Function)은 교통 상황(Context)을 보고 자동으로 우회 경로(Rewrite)를 설정합니다. 운전자는 그 경로가 수정되었다는 사실조차 모르고 쾌적하게(보안되게) 이동하게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 비교: VPD vs. 일반 뷰(View) vs. TDE**

| 비교 항목 (Criteria) | VPD (Virtual Private Database) | View (Standard) | TDE (Transparent Data Encryption) |
|:---|:---|:---|:---|
| **접근 제어 단위** | Row (행) / Column (열) | Row (행) (정적) | Data File (Storage) |
| **동적성 (Dynamic)** | **매우 높음 (Session Context 기반)** | 낮음 (Hardcoded) | 낮음 (Key 기반) |
| **관리 복잡도** | 중앙 집중식 관리 (Easy) | 객체 수 증가로 어려움 | 키 관리 복잡 |
| **성능 오버헤드** | 함수 호출 비용 발생 (Minimal) | Merge View 시 성능 저하 가능 | 암복호화 비용 발생 (CPU) |
| **Data Leak 방지** | 강력 (OS Tool 접속 시에도 적용) | 약함 (Native Tool 접속 시 우회 가능) | **물리적 탈취 방지 (최강)** |

*   **Table Column Masking**: VPD의 확장 기능인 `SEC_RELEVANT_COLS`을 사용하여, 민감한 컬럼(Salary 등)에 접근 시 해당 컬럼을 NULL로 반환하거나 레코드 자체를 숨길 수 있다.

**2. 타 과목 융합 (OS 및 네트워크)**

-   **OS (Operating System)와의 관계**: DB 내의 보안 정책이므로 OS 레벨의 File Permission이나 Disk Encryption과 무관하게 작동한다. 즉, DBA가 OS 파일을 복사해가더라도 DB 복원 시 VPD 정책이 다시 적용되어 데이터를 볼 수 없으므로 **2차 방어선** 역할을 수행한다.
-   **네트워크 보안과의 시너지**: VPN이나 IP 기반 접근 제어가 "누가 접속하는가(Who)"를 막는다면, VPD는 "접속 후 무엇을 보는가(What)"를 제어한다. 이 둘의 결합이 보안의 **AOP (Aspect Oriented Programming)**적 완성도를 높인다.
    -   *예: VPN(외부 접속 차단) + VPD(내부 직원 별 권한 분리)*

**정량적 의사결정 메트릭스**
-   **TPS (Transactions Per Second) 영향도**: 잘못된 VPD 함수(예: `SELECT * FROM huge_table`를 포함한 함수)는 호출 시마다 Full Scan을 유발하여 TPS를 급격히 떨어뜨릴 수 있음. (주의 필요)
-   **보안 등급**: 전체 공개(L0)에서부터 기밀(L5)까지, VPD는 L3 이상의 세분화된 보안이 필요한 대형 시스템에 필수적임.

**📢 섹션 요약 비유**
VPD는 **'쇼핑몰의 VIP 전용 멤버십'**과 유사합니다. 쇼핑몰(데이터베이스)에는 모든 상품이 진열되어 있지만, VIP 멤버십(VPD Policy)을 가진 고객에게는 특별한 할인가와 VIP 라운지(특정 데이터)가 보이고, 일반 고객에게는 일반 상품만 보입니다. 겉으로는 같은 매장이지만 보이는 세계가 다릅니다.

```text
[ Security Layers ]

┌─────────────────────────────────────────────┐
│  [ Network Firewall ] : Block IP/Port       │  <- Entry Control
├─────────────────────────────────────────────┤
│  [ DB Authentication ] : User/Password      │  <- Identity Check
├─────────────────────────────────────────────┤
│  [ VPD (System Privs) ] : Row Filtering     │  <- Content Visibility
├─────────────────────────────────────────────┤
│  [ Data ] : Actual Files on Disk            │  <- Raw Asset
└─────────────────────────────────────────────┘
```

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 문제 해결**

-   **시나리오 A: 금융권 지점별 데이터 격리**
    -   **상황**: 전국 100개 지점이 하나의 DB를 쓰지만, 서울 지점 직원은 서울 거주자 정보만 봐야 한다.
    -   **해결**: `LOGIN_TRIG` 로그인 트리거에서 `SET_CONTEXT('REGION', 'SEOUL')`를 설정하고, VPD Function이 `region = SYS_CONTEXT(...)`를 반환하게 한다.
    -   **효과**: �