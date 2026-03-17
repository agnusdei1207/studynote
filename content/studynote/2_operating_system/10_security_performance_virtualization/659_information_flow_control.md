+++
title = "659. 정보 흐름 제어 (Information Flow Control)"
date = "2026-03-16"
weight = 659
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "정보 흐름 제어", "Information Flow Control", "보안 라벨링", "taint analysis"]
+++

# 정보 흐름 제어 (Information Flow Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 접근 제어(Access Control)가 "누가(Who)" 접근하는지를 다룬다면, 정보 흐름 제어(IFC, Information Flow Control)는 **"데이터가 어디서 어디로(Where)" 흐르는지**를 라벨링(Labeling)과 유형 추적(Type System)을 통해 통제하는 보안 모델이다.
> 2. **가치**: 암호화된 채널을 우회하거나 **Trojan Horse**와 같은 **Covert Channel**을 통한 정보 유출을 기술적으로 차단하며, 시스템의 기밀성(Confidentiality) 무결성(Integrity)을 수학적으로 검증 가능한 수준으로 보장한다.
> 3. **융합**: 컴파일러 이론(유형 시스템), OS 보안 커널(FLASK, SELinux), 그리고 현대 보안 분석인 **Taint Analysis**의 근간이 되는 핵심 아키텍처이다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
정보 흐름 제어(IFC, Information Flow Control)는 컴퓨터 시스템 내에서 정보가 허용된 경로를 통해 흐르도록 통제하는 보안 메커니즘이다. 기존의 **DAC (Discretionary Access Control)**나 **RBAC (Role-Based Access Control)**가 사용자 주체의 권한에 집중한다면, IFC는 **데이터 객체** 자체에 보안 등급(Security Label)을 부여하여, 고등급 정보가 저등급 정보로 유출되는 것을 방지하는 데 중점을 둔다. 이는 단순한 파일 접근 통제를 넘어, 메모리 변수 간의 할당, 함수 인자 전달, 출력 스트림 기록 등 프로그램 실행 중 발생하는 모든 데이터 이동을 추적한다.

#### 2. 등장 배경 및 필요성
1970년대 Bell-LaPadula 모델의 등장과 함께 군사적, 정부적 차원의 기밀성 보호 요구가 대두되었다. 하지만 기존의 접근 제어만으로는 **트로이 목마(Trojan Horse)** 프로그램이 정상적인 권한을 이용해 비밀 정보를 읽은 뒤, 공개 파일에 몰래 기록하는 "합법적이지만 위험한" 유출 경로(Storage Channel)를 막을 수 없었다. 이를 해결하기 위해 프로그램의 논리적 흐름 자체를 분석하고, 데이터의 흐름이 보안 정책(예: No Read Up, No Write Down)을 위반하는지 수학적으로 증명하려는 연구가 시작되었다.

#### 3. 💡 핵심 비유: "물질의 확산과 오염 방지"
정보 흐름 제어는 **"방사성 물질이 담긴 용기를 다루는 화학 실험실 규칙"**과 같다.
방사성 물질(비밀 정보)은 최초에 밀폐된 용기(고보안 영역)에 담겨 있다. 이 용기의 내용물을 빈 컵(공개 변수)에 옮겨 담는 순간, 빈 컵도 방사성 오염(비밀 라벨)이 되어야 한다. 만약 방사성 물질이 묻은 장갑을 쓰고 일반 쓰레기통에 버리려 한다면, 이는 시스템 전체의 오염(정보 유출)을 초래하므로 엄격하게 차단된다.

> 📢 **섹션 요약 비유**: 마치 **화학 실험실에서 고독성 물질이 묻은 도구를 일반 쓰레기통에 버리지 못하도록 오염 경로를 추적하고 격리하는 것과 같습니다.**

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 라벨링 시스템
IFC의 핵심은 모든 메모리 객체와 주체(Subject, 실행 중인 코드)에 보안 라벨(Security Class)을 부여하는 것이다. 주로 격자(Lattice) 구조를 사용하여 보안 등급 간의 부분 순서(Partial Order) 관계를 정의한다.

**[표: 정보 흐름 제어의 핵심 구성 요소]**
| 요소명 (Component) | 역할 (Role) | 내부 동작 및 파라미터 | 비고 (Note) |
|:---|:---|:---|:---|
| **Security Label (L)** | 데이터의 기밀성 등급 | $L(O)$: 객체의 레벨 (예: Top Secret > Secret > Unclassified) | 부분 순서 집합(Poset) 형성 |
| **Subject (S)** | 정보를 처리하는 능동 개체 | 프로세스, 스레드, 사용자 세션 | 현재 보안 클리어런스(Current Clearance) 보유 |
| **Object (O)** | 정보를 저장하는 수동 개체 | 파일, 메모리 변수, 레지스터, I/O 포트 | 읽기/쓰기 작업의 대상 |
| **Lattice Model** | 흐름의 허용 여부 판단 | $L(s_1) \leq L(s_2)$: 흐름 허용 ($s_1 \rightarrow s_2$) | Upper/Lower Bound 연산 제공 |
| **Reference Monitor** | 실행 시점 흐름 검사 | 모든 `=`, `memcpy`, `print` 명령어를 가로채서 라벨 검증 | OS 커널 혹은 하이퍼바이저에 위치 |

#### 2. 흐름 규칙 (Flow Rules) 및 Non-Interference
정보 흐름 보안의 기본 원칙은 **비밀성(Secrecy)**을 위한 **No Write Down**과 **무결성(Integrity)**을 위한 **No Read Up**으로 요약된다. 이는 수학적으로 **Non-Interference** 속성으로 정의된다.
- **Non-Interference**: 고등급 시스템의 입력이 저등급 시스템의 출력에 전혀 영향을 미치지 않아야 한다. 즉, 저등급 사용자는 고등급 입력의 존재 여부조차 알 수 없어야 한다.

#### 3. 아키텍처 다이어그램: 라벨 기반 흐름 추적

```text
    [ 실행 흐름 추적 시스템 (Execution Tracking System) ]

    시간(t=0)                 시간(t=1)                       시간(t=2)
    ---------                 ---------                       ---------
    
    [ User Input ]            [ Process (L=Secret) ]          [ Output Stream ]
    (Level: Public)           (Subject)                       (Level: Public)
         |                          |                             ^
         | 1. Read (Up)             | 3. Write (Down) ❌          |
         v                          v                             |
    +-----------+             +-----------+                   +-----------+
    | Variable A|             | Variable B|                   | Log File  |
    | L: Public |  --->       | L: Secret |  ---> (BLOCK) --->| L: Public |
    +-----------+   (S assign)+-----------+                   +-----------+
         ^                          |                             |
         |                          v                             |
         |                  [ Reference Monitor ]                 |
         |                  - Detect: B -> Log                   |
         |                  - Action: Exception Raised          |
         +-------------------------------------------------------+
              (오염(Taint) 추적: Public 변수 A가 Secret 변수 B가 되고,
               B가 Public으로 흐르려 하므로 차단됨)
```

**[다이어그램 해설]**
위 다이어그램은 프로그램 실행 도중 변수의 보안 라벨(L)이 어떻게 변화하고 흐름 제어가 수행되는지를 보여준다.
1. **초기화**: 사용자 입력(공개 레벨)이 변수 `A`에 저장된다.
2. **오염(Tainting)**: 비밀 프로세스(L=Secret)가 `A`를 읽어 계산 후 비밀 변수 `B`에 할당한다. 이때 `A`와 `B`의 흐름이 연결되며, `B`는 최소 `Secret` 레벨을 가지게 된다.
3. **차단(Sanitization Check)**: 프로그램이 `B`를 공개 로그 파일에 기록하려 시도한다. 이때 **Reference Monitor**는 `B(L=Secret) → Log(L=Public)` 흐름이 "Write Down"(비밀→공개)임을 감지하고, 이를 보안 정책 위반으로 간주하여 시스템 콜(예: `write()`)을 차단한다.

#### 4. 핵심 알고리즘: 라벨 전파 및 검증 (Pseudo-code)
IFC 시스템은 각 연산자 할당 시 라벨 병합(Lattice Join) 연산을 수행하여 라벨을 유지한다.

```python
# Security Class Lattice
class SecurityLabel:
    def __init__(self, level): self.level = level # 3:Top, 2:Secret, 1:Public
    def __le__(self, other): return self.level <= other.level # Subtyping
    
    # 흐름이 발생할 때 두 라벨의 상한(Least Upper Bound)을 계산
    def join(self, other):
        return SecurityLabel(max(self.level, other.level))

# 런타임 모니터 (Runtime Monitor)
mem_registry = {} # address -> SecurityLabel

def IF_CHECK(src_addr, dst_addr, is_explicit=True):
    src_label = mem_registry.get(src_addr, SecurityLabel.PUBLIC)
    dst_label = mem_registry.get(dst_addr, SecurityLabel.PUBLIC)

    # 명시적 흐름(Explicit Flow): assignment, copy
    if is_explicit: 
        if not (src_label <= dst_label):
            raise SecurityViolation("Illegal Flow: Secret to Public")
        # 흐름 허용 시, 목적지의 라벨을 상향 조정 (Taint Propagation)
        mem_registry[dst_addr] = dst_label.join(src_label)
    
    # 암시적 흐름(Implicit Flow): 제어 구문 (if/branch)
    else: 
        # 비밀 정보에 의존하는 분기문 내에서 공개 변수 수정 시도
        if not (src_label <= dst_label):
             # 이를 막기 위해 PC(Program Counter) 라벨을 src_label로 승격
             raise SecurityViolation("Covert Channel via Branch")
```

> 📢 **섹션 요약 비유**: **식당 주방의 위생 규칙**과 같습니다. 날생선을 썰던 칼(비밀 라벨)을 씻지 않고 샐러드(공개 정보)를 자르는 데 사용하면, 샐러드는 '오염'되어 버려져야 합니다. IFC는 이 '칼이 무엇에 쓰였는지'를 기억했다가 샐러드에 닿는 순간 주방장을 제지하는 시스템입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술 비교: 접근 제어(AC) vs 정보 흐름 제어(IFC)

| 구분 (Criteria) | 접근 제어 (Access Control) | 정보 흐름 제어 (Information Flow Control) |
|:---|:---|:---|
| **통제 대상** | 주체(Subject)의 권한 | 데이터 객체(Object)의 라벨 |
| **검사 시점** | 접근 시점 (File Open, Login) | 연산 시점 (Read/Write/Assign/Compute) |
| **주요 메커니즘** | ACL, Capability, Role | Lattice Model, Type System, Taint Tracking |
| **Covert Channel** | 우회 가능성 높음 (Trojan Horse 등) | 내부적으로 분석 및 차단 가능 |
| **구현 난이도** | 상대적으로 쉬움 (OS/DB 기본 기능) | 매우 높음 (컴파일러/언어 수준 지원 필요) |
| **성능 오버헤드** | 낮음 (Lookup 수준) | 높음 (모든 명령어/분기 추적) |

#### 2. 융합 관점: OS 및 컴파일러와의 시너지
- **컴파일러와의 융합 (Static Analysis)**:
    컴파일 타임에 코드의 제어 흐름 그래프(CFG, Control Flow Graph)를 분석하여 변수 간 의존성을 추론한다. 예를 들어, **Jif** 언어는 컴파일러 자체가 IFC 정책을 강제하여, 보안 정책을 위반하는 코드는 아예 컴파일되지 않게 한다.
- **OS 보안 커널과의 융합 (Dynamic Enforcement)**:
    **SELinux (Security-Enhanced Linux)**의 **MLS (Multi-Level Security)** 정책은 IFC를 OS 레벨로 구현한 사례이다. 파일뿐만 아니라 소켓, 파이프, 공유 메모리 등 IPC(Inter-Process Communication) 메커니즘을 통해 데이터가 이동할 때마다 보안 컨텍스트(Security Context)를 검사하여 불법적인 흐름을 차단한다.

#### 3. Taint Analysis와의 연계
현대의 웹 보안에서 사용되는 **Taint Analysis**는 IFC의 실용적 구현체이다. 사용자 입력(External Input)을 'Tainted'(오염됨)로 마킹하고, 이 데이터가 SQL 쿼리나 시스템 명령어 실행 경로(Sink)로 흐르는지를 추적한다.

```text
    [Taint Analysis Flow]
    
    Source (Input)
       ↓ (Tag Taint)
    Variable (Sanitized?)
       ↓ (No) --> [SQL Query String] --> SQL Injection Risk!
       ↓ (Yes)
    Safe Execution
```

> 📢 **섹션 요약 비유**: 접근 제어는 **'건물의 보안 카드 시스템'**이라면, 정보 흐름 제어는 **'건물 내부의 CCTV와 녹화 시스템'**입니다. 카드가 있어도 누가 방 안으로 무엇을 들고 들어갔는지, 그것이 밖으로 나오지 않았는지 끝까지 추적하는 것이 IFC의 역할입니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스

**[시나리오 1: 금융권 시스템의 혼합 데이터 처리]**
- **상황**: 대외적인 API 서버(Public Zone)와 내부 결제 로직(Secret Zone)이 같은 애플리케이션 서버에서 실행되는 **Multitenancy 환경**이다.
- **문제**: 해커가 공개 API에 버그를 주입하여 결제 로직의 메모리 내용을 읽거나, 로그 파일에 비밀 키를 기록하게 하려 한다.
- **기술사적 판단**:
    1. **기존 방식**: 네트워크 단계의 **Firewall**이나 OS 수준의 **File Permission**만으로는 프로세스 내부 메모리 간의 데이터 유출을 막을 수 없다.
    2. **IFC 도입 결정**: **Secret Zones**의 데이터는 절대 **Public Zones**으로 흐르지 못하도록 IFC를 강제해야 한다.
    3. **구현**: 언어 수준의 라이브러리(Java Security Manager 등) 또는 컨테이너 기반의 **Runtime Policy Enforcement**를 적용한다.

#### 2. 도입 체크리스트
- **기술적 검증**:
    - [ ] 라벨링 시스템의 오버헤드(Performance) 측정