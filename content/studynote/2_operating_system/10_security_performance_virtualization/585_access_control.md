+++
title = "585. 접근 제어 (Access Control) 모델 - DAC, MAC, RBAC"
date = "2026-03-14"
weight = 585
+++

# 585. 접근 제어 (Access Control) 모델 - DAC, MAC, RBAC

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 접근 제어는 보안 정책을 시스템 수준에서 구현하는 메커니즘으로, **주체(Subject)**가 **객체(Object)**에 접근할 수 있는지를 판단하는 참조 모니터(Reference Monitor)의 핵심 논리입니다.
> 2. **가치**: 기업의 중요 자산에 대한 **기밀성(Confidentiality)**과 **무결성(Integrity)**을 보장하며, 불법적인 정보 유출이나 변조를 방지하여 법적·재무적 리스크를 최소화합니다.
> 3. **융합**: 운영체제(OS)의 커널 레벨 권한 관제부터 클라우드의 **IAM (Identity and Access Management)**, 데이터베이스의 **SQL GRANT** 구문까지 현대 보안 아키텍처의 기반을 형성합니다.

---

## Ⅰ. 개요 (Context & Background)

접근 제어(Access Control)란 정보 시스템에서 자원(Resource)에 대한 접근 권한을 제한하여 보안 목표를 달성하는 기술적·관리적 수단을 말합니다. 이는 단순한 '차단'이 아니라 누가(Who), 무엇을(What), 언제(When), 어디서(Where) 어떻게(How) 자원을 사용할 수 있는지를 정의하고 시행하는 **세분화된 제어(Micro-control)** 체계입니다.

정보 보안의 3대 요소인 **CIA (Confidentiality, Integrity, Availability)** 중 기밀성과 무결성을 직접적으로 담당합니다. 초기 컴퓨팅 환경에서는 물리적인 잠금장치에 의존했으나, 시분할 시스템(TSS)과 네트워크의 발전으로 사용자가 논리적으로 분리되면서 소프트웨어적 접근 제어의 중요성이 대두되었습니다. 이를 체계화한 것이 1980년대 미 국방부의 **TCSEC (Trusted Computer System Evaluation Criteria, 오렌지북)**이며, 이때 정립된 DAC와 MAC의 개념은 현대 보안 모델의 근간이 되고 있습니다.

💡 **비유**: 디지털 세상의 '출입 통제 시스템(CCTV와 도어락)'입니다. 건물의 중요도에 따라 단순히 열쇠를 주는 사람(DAC), 중앙 통제실에서 승인을 해주는 사람(MAC), 직급별 카드를 나눠주는 사람(RBAC)이 각기 다른 방식으로 보안을 유지합니다.

📢 **섹션 요약 비유**: 접근 제어 모델을 선택하는 것은 건물의 용도에 따라 '일반 주택(DAC)', '금고가 있는 은행(MAC)', '대기업 사무실(RBAC)' 중 출입문의 잠금 장치를 결정하는 것과 같습니다. 용도에 맞지 않는 잠금장치는 보안을 무너뜨리거나 효율을 떨어뜨립니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

접근 제어 모델은 크게 **DAC (Discretionary Access Control)**, **MAC (Mandatory Access Control)**, **RBAC (Role-Based Access Control)**의 세 가지 주요 패러다임으로 나뉩니다. 각 모델은 권한 결정의 주체와 정책 저장소의 위치가 다릅니다.

### 1. 핵심 구성 요소 비교 (Component Comparison)

| 구성 요소 | DAC (임의적) | MAC (강제적) | RBAC (역할 기반) |
|:---|:---|:---|:---|
| **권한 결정 주체** | **소유자 (Owner)**: 자원 생성 주체 | **시스템 (System)**: 보안 정책 시스템 | **관리자**: 역할(Role) 설계자 |
| **정책 저장소** | **ACL (Access Control List)**: 객체별 허가 목록 | **Label (Security Label)**: 주체/객체의 등급 | **Permission Set**: 역할별 권한 집합 |
| **데이터 흐름 제어** | 불가능 (자유로운 흐름) | 가능 (상위->하위 흐름만 허용) | 제한적 (역할 간 관계에 따름) |
| **확장성** | 낮음 (관리 항목 폭발) | 매우 낮음 (변경 어려움) | 높음 (역할 묶음으로 관리) |

### 2. 모델별 심층 메커니즘

#### A. DAC (Discretionary Access Control)
DAC는 자원의 소유자가 접근 권한을 임의로 결정하는 방식입니다. UNIX/Linux의 파일 시스템에서 Owner/Group/Others에 대한 Read/Write/Execute(rwx) 비트를 설정하는 것이 전형적인 예입니다.

```text
[User A (Owner)]
   |
   +-- creates --> [File: report.txt]
                     |
   (Sets ACL: User B = Read)
                     |
                     v
              [Access Control Matrix / ACL]
                     |
   +-----------------+------------------+
   |                 |                  |
   v                 v                  v
User B (Read OK) User C (Denied) User A (RWX OK)
```
*해설*: User A는 `report.txt`의 소유자로서 자신의 재량(DAC의 핵심)에 따라 User B에게 읽기 권한을 부여하지만, User C에게는 아무 권한도 주지 않을 수 있습니다. 권한 정보는 주로 객체에 부착된 **ACL (Access Control List)**에 저장됩니다.

#### B. MAC (Mandatory Access Control)
MAC는 시스템의 최고 보안 관리자(Security Officer)가 설정한 보안 라벨(Security Label)에 따라 강제적으로 접근을 통제합니다. 주체(Subject)와 객체(Object)에 각각 기밀 등급(Top Secret, Secret, Confidential, Unclassified)을 부여하고, **비교 규칙(Rules Engine)**을 통해 판단합니다.

```text
   [Subject: User]                      [Object: Data]
   Level: Secret  ----(Compare)----> Level: Top Secret
        |                                  |
        +----> [Simple Security Property]  |
        |     (No Read Up: 상위 비밀 읽기 불가)|
        |                                  |
        v                                  v
   [Decision: DENIED] <---- [Bell-LaPadula Model]
```
*해설*: 위 다이어그램은 **Bell-LaPadula 모델**의 'No Read Up' 규칙을 도식화한 것입니다. 사용자(User)의 등급이 'Secret'이고 데이터(Data)가 'Top Secret'이면, 시스템은 강제로 접근을 거부(DENIED)합니다. 소유자라도 이 규칙을 변경할 수 없다는 점이 DAC와 결정적으로 다릅니다. 이는 **SELinux (Security-Enhanced Linux)**의 핵심 메커니즘이기도 합니다.

#### C. RBAC (Role-Based Access Control)
RBAC는 사용자에게 직접 권한을 부여하는 것이 아니라, **역할(Role)**을 정의하고 그 역할에 권한을 묶어서 할당하는 방식입니다. 사용자는 역할을 통해 간접적으로 권한을 얻습니다.

```text
      [Users]           [Roles]           [Permissions]
    (Alice, Bob)  --->  <Accountant>  --->  <Read_Invoice>
                                       <Write_Ledger>
                                       <View_Budget>

       Manager  --->  <Manager>     --->  <Approve_Payment>
                                       <View_All_Reports>
```
*해설*: RBAC는 **RBAC96 표준**에서 제안된 Core, Hierarchical, Constraint 구조를 가집니다. 위의 예시에서 'Alice'라는 사람이 퇴사하더라도 'Accountant'라는 역할과 권한은 그대로 유지되고, 새로운 사람에게 그 역할만 부여하면 되므로 관리 오버헤드가 획기적으로 줄어듭니다.

### 3. 핵심 알고리즘 및 수식

접근 제어의 판단은 기본적으로 다음과 같은 함수로 정의할 수 있습니다.

$$ f(S, O, A) \rightarrow \{ \text{True (Allow)}, \text{False (Deny)} \} $$

*   $S$: Subject (주체, 요청자)
*   $O$: Object (객체, 자원)
*   $A$: Action (행위, Read/Write/Execute)

**DAC의 의사결정 로직 (Python Style):**
```python
def check_dac(user, resource, action):
    # 객체의 ACL(접근 제어 목록)에서 사용자의 권한 조회
    acl = resource.get_acl() 
    if user in acl.permissions and action in acl.permissions[user]:
        return True # 권한 있음
    return False    # 권한 없음 (소유자 설정에 따름)
```

**MAC의 의사결정 로직 (Bell-LaPadula):**
```python
def check_mac(user_clearance, object_classification, action):
    # Simple Security Property (No Read Up)
    if action == "READ":
        if user_clearance.level < object_classification.level:
            return False # 낮은 등급은 높은 등급을 읽을 수 없음
    # *-Property (No Write Down)
    elif action == "WRITE":
        if user_clearance.level > object_classification.level:
            return False # 높은 등급은 낮은 등급에 쓸 수 없음
    
    return True # 등급이 일치하거나 적절할 때 허용
```

📢 **섹션 요약 비유**: DAC는 '개인 사무실의 열쇠회수'와 같아서 주인이 마음대로 복사하지만, MAC는 '군사 기지의 보안 구역'과 같아서 아무리 장군이라도 출입증(Rotation)이 없으면 통과할 수 없습니다. RBAC는 '회사의 출입명부'와 같아서 누가 오든지 그날 당직(Role)이면 문을 열 수 있습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

세 가지 모델은 상호 배타적이지 않으며, 실제 시스템에서는 **Hybrid (하이브리드)** 형태로 융합되어 적용됩니다.

### 1. 심층 기술 비교표 (Deep Comparison)

| 구분 | DAC (Discretionary) | MAC (Mandatory) | RBAC (Role-Based) |
|:---|:---|:---|:---|
| **핵심 철학** | "내 것은 내가 관리한다" | "시스템의 안전이 최우선이다" | "직무에 따라 권한을 부여한다" |
| **권한 부여 단위** | 개별 사용자/파일 단위 | 시스템 레벨 보안 등급 | 역할(Role) 그룹 단위 |
| **주요 구현 메커니즘** | **ACL** (Access Control List), Permission Bits | **Security Labels**, Capabilities | **Role Hierarchy**, Session |
| **장점 (Pros)** | 구현 간단, 유연성 높음 | 데이터 유출 방지, 강력한 통제 | 관리 용이성, 확장성 우수 |
| **단점 (Cons)** | 권한 관리 어려움, **Trojan Horse** 취약 | 사용성 저하, 비용 높음 | **Role Explosion** 문제 발생 가능 |
| **활용 예시** | Windows 파일 공유, Linux 파일 시스템 | SELinux, Trusted Solaris, 방화벽 | AWS IAM, Active Directory, ERP |

### 2. 융합 및 시너지 (Convergence)

현대의 **OS (Operating System)**는 이러한 모델들을 계층적으로 결합하여 사용합니다.
*   **OS 레벨 (Kernel)**: **MAC** 방식을 적용하여 시스템 파일이나 프로세스 간의 메모리 접근을 통제합니다. (예: iOS의 샌드박스, Android의 SELinux)
*   **사용자 레벨 (Application)**: **DAC** 또는 **RBAC** 방식을 적용하여 사용자가 자신의 문서를 공유하거나 앱 내의 기능을 사용하도록 허용합니다.
*   **클라우드 환경 (Cloud)**: **RBAC**가 사실상의 표준이나, 민감한 데이터에 대해서는 **ABAC (Attribute-Based Access Control)**의 속성 기반 논리를 결합하여 더욱 정교한 제어를 수행합니다.

> **Trojan Horse의 위험성**: DAC 하위에서는 사용자가 정상적인 프로그램(Word)을 실행할 때, 그 프로그램이 사용자의 권한을 도용하여 악의적인 행위(파일 전송)를 할 수 있습니다. 반면 MAC는 프로그램(주체)에도 라벨을 부여하여, Word 프로세스가 네트워크 전송(쓰기)을 시도할 때 권한이 없다면 차단합니다.

📢 **섹션 요약 비유**: 접근 제어 모델의 비교는 '자동차의 안전 장치'와 같습니다. 에어백(DAC)은 운전자의 편의를 위해 있지만, 시스템 자체의 파손을 막는 뼈대(MAC)가 없다면 무용지물입니다. 현대의 자동차는 이 둘을 결합하고 운전자의 숙련도(역할)에 따라 시스템이 조절되는 스마트 기능(RBAC)을 탑재한 셈입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

보안 담당자나 시스템 아키텍트는 시스템의 목적과 보안 등급 요구사항(Level of Assurance)에 따라 적절한 모델을 선정해야 합니다.

### 1. 도입 의사결정 시나리오

#### 시나리오 A: 금융권 핵심 시스템 (High Security)
*   **상황**: 고객의 개인정보와 거래 내역을 관리하는 데이터베이스 서버.
*   **요구사항**: **기밀성(Confidentiality)**이 최우선이며, 관리자의 실수로 인한 권한 오남용을 방지해야 함.
*   **판단**: **MAC (SELinux)** 기반의 **RBAC** 도입을 권장.
*   **이유**: 관리자가 root 권한을 가지더라도 시스템 정책(MAC)에 의해 보호된 중요 파일을 함부로 수정하거나 유출할 수 없도록 강제 통제해야 한다. 또한, 업무 분장을 위해 RBAC를 병행하여 Smurf(하나의 계정에 모든 권한 부여) 방지.

#### 시나리오 B: 협업형 R&D 센터 (Flexibility)
*   **상황**: 연구원들이 프로젝트별로 자유롭게 데이터를 생성하고 공유해야 하는 환경.
*   **요구사항**: 빈번한 권한 변경이 필요하며, 관리자가 개별 승인하는 것은 비효율적임.
*   **판단**: **DAC**와 **RBAC**의 혼합 모델.
*   **이유**: 연구원(Owner)이 자신의 연구 결과물을 동료들에게 쉽게 공유(DAC)할 수 있도록 하되, 시스템 접속이나 공용 장비 사용은 RBAC로 통제하여 무분별한 접근을 방지.

### 2. 실무 도입 체크리스트

1.  **기술적 검증**:
    *   [ ] 운영체제가 제공하는 보안 모듈 지원 여부 확인 (Linux: SELinux vs AppArmor).
    *   [ ] 파일