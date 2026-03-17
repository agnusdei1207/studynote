+++
title = "586. 도메인 (Domain) 및 행렬 (Access Matrix) 기반 접근 제어"
date = "2026-03-14"
weight = 586
+++

# 586. 도메인 (Domain) 및 행렬 (Access Matrix) 기반 접근 제어

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 보호 도메인(Protection Domain)과 접근 제어 행렬(Access Control Matrix)은 컴퓨터 시스템의 보안 정책을 수학적으로 모델링한 가장 기초적이고 강력한 추상화 도구로, 모든 접근 제어의 '원점(Origin)'입니다.
> 2. **가치**: 시스템 자원에 대한 접근 권한을 주체(Subject), 객체(Object), 권한(Right)의 3요소로 행렬화하여 보안 상태를 명확히 정의하고, '최소 권한 원칙(Principle of Least Privilege)'을 구현할 수 있는 이론적 토대를 제공합니다.
> 3. **융합**: 이론적 모델인 행렬은 실제 시스템에서는 ACL(Access Control List)이나 Capability List(C-List)로 변환되어 구현되며, 현대의 RBAC(Role-Based Access Control), ABAC(Attribute-Based Access Control) 및 OS 보안 커널(Kernel) 설계의 근간이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
보호 도메인(Protection Domain)이란 운영체제(Operating System) 내에서 프로세스(Process)가 접근할 수 있는 자원의 집합과 그에 수반할 수 있는 연산(Operation)의 권한을 정의한 **보안 영역(Security Boundary)**입니다. 접근 제어 행렬(Access Control Matrix)은 이러한 도메인 간의 권한 관계를 2차원 행렬로 표현한 수학적 모델로, 시스템의 보안 상태(State)를 명확히 정의합니다. 이는 보안 정책을 기술하는 보편적인 언어 역할을 합니다.

**2. 작동 근간 및 배경**
초기 컴퓨팅 환경에서는 모든 사용자가 모든 자원에 접근할 수 있는 '평평한(Flat)' 구조였으나, 다중 사용자(Multi-user) 및 다중 프로그래밍(Multi-programming) 환경으로 진입하며 프로세스 간의 격리(Isolation)와 제어된 자원 공유가 필수적으로 되었습니다. 이에 따라 Lampson(1971) 등에 의해 제안된 접근 제어 행렬 모델은 **"누가(Subject), 무엇을(Object), 어떻게(Right)"**라는 보안의 3요소를 체계화하여, 무분별한 접근으로 인한 정보 유출이나 시스템 파괴를 방지하고자 등장했습니다.

**3. 비유 및 구조적 이해**
보호 도메인을 물리적인 공간에 비유하자면, **'키카드 권한이 부여된 사무실 구역'**과 같습니다. 일반 사원 구역에서는 경리팀 서류만 읽을 수 있지만(Read), 관리자 구역(Domain Switch)으로 이동하면 인사 기록을 수정(Write)할 수 있는 것과 같습니다. 시스템은 이러한 권한의 경계를 관리 도메인(Domain)으로 관리하며, 프로세스는 실행 흐름에 따라 필요한 권한 집합으로 이동합니다.

**4. 기술적 진화**
단순한 행렬 모델에서 시작하여, 현대의 OS는 이를 하드웨어적인 ** protection ring (Protection Ring, 보호 링)** 구조(CPL, Current Privilege Level 레지스터 등 활용)로 구현하여 커널 모드(Kernel Mode)와 사용자 모드(User Mode)의 격리를 물리적, 논리적으로 강화하고 있습니다.

📢 **섹션 요약 비유**: 보호 도메인은 **'각종 스마트 키가 부여된 호텔 객실과 복도 구역'**과 같습니다. 손님(프로세스)은 객실 키(도메인)가 있을 때만 해당 구역의 서비스(자원)를 이용할 수 있으며, 청소용 마스터 키(권한 상승)로 다른 층의 구역에 접근할 수도 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 상세 분석**

접근 제어 모델을 구성하는 핵심 요소는 다음과 같습니다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 비고 (Note) |
|:---:|:---|:---|:---|
| **주체 (Subject)** | 능동적 개체 (Active Entity) | 접근을 요청하는 사용자, 프로세스, 혹은 도메인 그 자체. 보안 주체로 식별됨. | User, Process, Domain |
| **객체 (Object)** | 수동적 개체 (Passive Entity) | 보호 대상이 되는 자원. 접근 제어의 대상. | File, Memory, I/O Port, Socket |
| **권한 (Right)** | 연산 허가 (Permission) | 객체에 대해 수행 가능한 오퍼레이션의 집합. | Read(R), Write(W), Execute(X), Own(O) |
| **도메인 (Domain)** | 권한 공간 (Protection Space) | 특정 주체가 특정 시점에 가지고 있는 권한들의 집합. 주체의 '상태'를 정의함. | Context, Profile |
| **전환 (Switch)** | 권한 변경 (Transition) | 한 도메인에서 다른 도메인으로 이동하는 메커니즘. 이 자체도 엄격한 권한으로 제어됨. | `setuid`, System Call |

**2. 아키텍처: Access Matrix (접근 제어 행렬)**

접근 제어 행렬은 시스템의 전체 보안 상태를 나타내는 $n \times m$ 행렬입니다. $S$는 주체 집합, $O$는 객체 집합일 때, 행렬의 셀 $A[s, o]$는 주체 $s$가 객체 $o$에 대해 가진 권한 집합을 나타냅니다.

```text
         [ Objects (Columns) ]         [ Domain Switching ]
   (File A)  (File B)  (Printer)   (D1)   (D2)   (D3)
     +---------+---------+-----------+-------+-------+-------+
(D1) |  Read   |   ---   |   Print   |  ---  | Switch|  ---  | <-- Domain 1 (User)
(S1) +---------+---------+-----------+-------+-------+-------+
     |   ---   |  Read   |    ---    |  ---  |  ---  | Switch| <-- Domain 2 (Guest)
(S2) +---------+---------+-----------+-------+-------+-------+
     | R/W/O   | R/W/O   |  Manage   | Switch| Switch| Switch| <-- Domain 3 (Admin)
(S3) +---------+---------+-----------+-------+-------+-------+

Legend:
R/W/O: Read / Write / Owner
---  : No Access (Empty Set)
Switch: Permission to switch to target domain
```

**3. 심층 동작 원리 및 메커니즘**

① **자원 접근 (Access Request)**:
프로세스(Subject)가 객체(Object)에 접근을 시도하면, 커널의 **Reference Monitor (참조 모니터)**는 현재 주체의 도메인(Domain)과 목표 객체를 행렬에서 조회합니다.
② **권한 검증 (Permission Check)**:
행렬의 해당 셀 $A[s, o]$에 요청한 연산(예: `Write`)이 포함되어 있는지 확인합니다. 만약 포함되어 있지 않으면 `Access Violation (접근 위반)` 예외(Exception)를 발생시킵니다.
③ **도메인 전환 (Domain Switching)**:
권한 상승이 필요한 작업(예: 시스템 콜 호출)을 위해, 프로세스는 행렬 내의 `Switch` 권한을 검사받아야만 다른 도메인(주로 관리자 도메인)으로 전환될 수 있습니다. 이는 **Toggling (토글링)** 메커니즘으로 구현되어 불필요한 권한 노출을 방지합니다.
④ **동적 변경 (Dynamic Association)**:
시스템은 객체 생성/소멸에 따라 행렬을 동적으로 확장하거나 축소합니다. 이때 행렬의 희소성(Sparsity, 빈 셀이 많음) 문제가 발생하면 메모리 효율을 위해 별도의 자료구조(ACL, C-List)로 변환하여 저장합니다.

**4. 핵심 알고리즘: 의사결정 트리 (Pseudo-code)**

```python
# Global Access Matrix M[Subject][Object]
def access_check(subject, object, operation):
    # 1. Check if subject is active
    if not is_active(subject):
        raise SecurityException("Subject Unknown")

    # 2. Retrieve Access Rights from Matrix
    rights_set = AccessMatrix.get_rights(subject, object)

    # 3. Validate Operation
    if operation in rights_set:
        return True  # Access Granted
    else:
        log_violation(subject, object, operation)
        return False # Access Denied

# Domain Switching Logic
def switch_domain(subject, target_domain):
    if 'Switch' in AccessMatrix.get_rights(subject, target_domain):
        subject.set_current_domain(target_domain)
        execute_transition_protocol(subject, target_domain)
```

📢 **섹션 요약 비유**: 접근 제어 행렬은 **'고속도로 통행료 징수 시스템의 하이패스 차선 관제표'**와 같습니다. 차량(주체)이 특정 차선(객체)으로 진입할 때, 관제센터(행렬)는 해당 차량이 미리 등록된 카드(권한)를 가지고 있는지 즉시 확인하고, 없으면 진입을 막거나 다른 요금소(도메인 전환)로 우회시킵니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 구현 방식 비교: ACL vs. Capability (C-List)**

이론적인 행렬 모델은 실제 메모리 공간 낭비(Sparsity 문제)를 방지하기 위해 다음과 같은 두 가지 주요 데이터 구조로 변환되어 구현됩니다.

| 구분 | ACL (Access Control List) | Capability List (C-List) |
|:---:|:---|:---|
| **기준 (Basis)** | **객체(Object) 중심** (열 Column 기반) | **주체(Subject) 중심** (행 Row 기반) |
| **저장 위치** | 객체의 헤더(Header) 또는 확장 속성 | 주체(프로세스)의 PCB 또는 별도 토큰(Token) |
| **관리 포커스** | "누가 나에게 접근하는가?" (Who can access me?) | "내가 무엇을 할 수 있는가?" (What can I access?) |
| **취소 (Revocation)** | **용이함** (리스트에서 삭제만 하면 됨) | **어려움** (주체가 가진 토큰을 찾아 폐기해야 함) |
| **대표 예시** | UNIX/Linux 파일 시스템 (`chmod`, `ls -l`) | PGP 키, Bitcoin 스크립트, Capsicum OS |
| **보안 강점** | 정보 유출 방지에 유리 (Discretionary) | 권한 위조 방지에 유리 (Mandatory/Unforgeable) |

**2. 기술 융합 관점 (Synergy)**

- **OS와의 융합 (Protection Rings)**:
    x86 아키텍처의 **Protection Ring (보호 링)** 구조(Ring 0~3)는 하드웨어 레벨에서 도메인을 구현한 예입니다. 커널(Ring 0)은 모든 하드웨어(I/O)에 접근 가능하지만, 애플리케이션(Ring 3)은 제한됩니다. 시스템 콜(System Call)이나 인터럽트(Interrupt) 발생 시 하드웨어가 자동으로 도메인 전환(Switch)을 수행하여 보안을 유지합니다.
- **분산 시스템과의 융합 (ACL in Cloud)**:
    AWS IAM이나 S3 버킷 정책은 **ACL의 확장된 형태**입니다. 수천만 개의 객체(File)가 존재하는 클라우드 환경에서는 객체별로 ACL을 관리하는 것이 확장성(Scalability) 면에서 유리합니다.
- **보안 취약점과의 연계 (Confused Deputy)**:
    C-List 기반 시스템에서 발생할 수 있는 **Confused Deputy Problem (혼동된 대리인 문제)**은 주체가 자신의 권한을 가지고 의도치 않게 악의적인 객체를 실행하는 문제입니다. 이는 행렬 모델에서 도메인 간 권한 위임(Delegation)을 제어하지 못해 발생하는 대표적인 시나리오입니다.

**3. 정량적 지표 분석**

| 지표 | Matrix (Raw) | ACL | C-List |
|:---:|:---:|:---:|:---:|
| **검색 속도 (Lookup)** | $O(1)$ (Indexing) | $O(n)$ (User List Scan) | $O(1)$ (Token Validation) |
| **저장 공간** | 매우 비효율 ($S \times O$) | 효율적 (Object별) | 효율적 (User별) |
| **권한 취소 (Revoke)** | $O(1)$ | $O(1)$ | 매우 느림 (Global Scan) |
| **확장성 (Scalability)** | 낮음 | 높음 (Object 많은 환경) | 높음 (User 많은 환경) |

📢 **섹션 요약 비유**: ACL과 C-List의 선택은 **'현관문 열쇠 관리법'**과 같습니다. ACL은 문마다 출입 허가 명단을 붙여두는 방식(누가 왔는지 확인하기 쉬움), C-List는 각자 가지고 있는 키꾸러미로 관리하는 방식(내가 열 수 있는 방이 무엇인지 확인하기 쉬움)입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 과정**

- **시나리오 A: 대규모 파일 서버 구축 (Web Server)**
    - **상황**: 수십만 개의 정적 파일(Image, CSS)을 다수의 익명 사용자 및 관리자가 접근.
    - **결정**: **ACL 기반**으로 설계.
    - **이유**: 특정 파일(객체)에 누가 접근하는지 파악하고, 특정 사용자를 차단하기가 ACL이 훨씬 유리함. 파일 생성 시 디폴트 권한(umask)을 적용하기 편리함.

- **시나리오 B: 분산 마이크로서비스 인증 (OAuth/JWT)**
    - **상황**: 사용자가 수천 개의 서비스를 호출하며, 각 서비스는 사용자의 권한을 검증해야 함.
    - **결정**: **C-List (Token) 기반**으로 설계 (JWT Claims).
    - **이유**: 매번 중앙 DB(행렬)를 조회할 수 없으므로, 사용자가 토큰(Capability)을 가지고 자신의 신분과 권한을 증명하게 함. 서버는 토큰 서명만 검증하면 되므로 부하가 적음.

**2. 도입 체크리스트 (Technical & Operational)**

- [ ] **기술적 요구사항 (Technical