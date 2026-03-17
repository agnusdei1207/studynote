+++
title = "600. 능력 기반 보안 (Capability-based Security)"
date = "2026-03-14"
weight = 600
+++

# 600. 능력 기반 보안 (Capability-based Security)

### 🎯 핵심 인사이트 (Insight)
1.  **권한의 객체화 (Tokenization)**:
    능력 기반 보안은 접근 통제의 주체를 '누구(Subject)'가 아니라 '무엇을 가졌느냐(Token)'로 전환합니다. 자원(Resource)에 대한 접근 권한과 그 자원을 가리키는 주소(Pointer)를 결합한 **Capability (능력 토큰)**를 통해, 보안 정책을 커널의 참조 모니터가 아닌 토큰 자체의 소유 여부로 검증하는 객체 지향적 보안 패러다임입니다.
2.  **최소 권한의 원칙 (PoLP, Principle of Least Privilege)의 구현체**:
    **CAP_SYS_ADMIN**과 같은 거대한 권한을 통째로 부여하는 대신, 파일 쓰기(`CAP_DAC_OVERRIDE`), 네트워크 소켓 오픈(`CAP_NET_RAW`) 등 필요한 기능만을 아토믹(Atomic) 단위로 분리하여 부여합니다. 이는 프로세스가 탈취당하더라도 시스템 전체로 권한이 확대되는 **Privilege Escalation (권한 상승)**을 구조적으로 차단합니다.
3.  **Confused Deputy (혼란된 대리자) 공격 방지**:
    **ACL (Access Control List)** 방식은 자원 중심으로 접근을 통제하기 때문에, 악의적인 프로그램이 정상적인 프로그램(대리자)을 속여 자원을 변경하게 할 수 있습니다. Capability 방식은 토큰이 없으면 접근 자체가 불가능하므로, 권한 없는 대리자가 작업을 수행하는 것을 원천적으로 봉쇄합니다.

---

## Ⅰ. 개요 (Overview & Context)

### 1. 개념 및 철학
**Capability (능력)**는 컴퓨터 보안에서 특정 객체(Object)에 대해 수행할 수 있는 권한(Access Right)과 그 객체의 위치를 나타내는 참조자(Reference)를 캡슐화한 불변의 데이터 조각을 말합니다.
기존의 보안 모델이 "이 사람이 이 방에 들어갈 자격이 있는가?"(Subject-centered)를 묻는다면, Capability 보안은 "이 사람에게 이 방의 열쇠가 있는가?"(Object-centered)를 묻습니다. 이때의 열쇠는 복제되거나 위조될 수 없는 고유한 토큰 형태를 띱니다.

### 2. 등장 배경 및 필요성
1970년대 **C language**와 **UNIX**가 등장하면서 주소 공간에 대한 포인터 연산이 자유로워졌습니다. 하지만 이는 임의의 메모리 영역을 침해할 수 있는 보안 허점을 낳았습니다.
이를 해결하기 위해 **CAP (Capability-based Access Control)** 시스템이 연구되었습니다. 초기에는 하드웨어 수준에서 메모리 **Capability List**를 관리(예: Plessey System 250)하려 했으나, 현대에는 주로 운영체제 커널 차원에서 소프트웨어적으로 권한을 분리하여 관리하는 방식(예: Linux Capabilities)으로 발전했습니다.

> **ACL vs Capability 비유 이해하기**
> *   **ACL (Access Control List)**: 호텔 객실 문 앞에 "입장 가능한 손님 명단"을 붙여놓는 것. (중앙 집중식 관리, 관리자가 명단을 수정해야 함)
> *   **Capability**: 객실 키(카드 키)를 가진 사람만 문을 열 수 있게 하는 것. (분산式 관리, 키가 있으면 누구나 가능, 키를 주면 권한 위임)

### 3. 작동 원리 (기초)
커널은 사용空间(User Space)의 프로세스가 자원을 요청할 때, 해당 프로세스가 **Capability Token**을 보유하고 있는지만 확인합니다. 토큰 내부에는 [Object Pointer | Permission Bits | Signature]가 포함되어 있어, 토큰 자체를 변조하려는 시도는 서명 검증(Signature Check) 단계에서 차단됩니다.

📢 **섹션 요약 비유**:
Capability 보안은 "VIP 라운지에 출입 명단을 확인하는 경비원(ACL)을 두는 대신, 출입 가능한 카드 키(Capability)를 지니고 있는 사람만이 태그를 찍고 들어가게 하는 무인 게이트 시스템"과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석
능력 기반 보안 시스템을 구성하는 핵심 요소들은 다음과 같이 세분화됩니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/포맷 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Capability Token** | 권한과 주소의 결합체 | 객체 ID + 권한 비트(R/W/X) + 무결성 태그를 포함한 불변 구조체 | C-structure / Kernel Object | VIP 티켓 |
| **C-List (Capability List)** | 토큰의 저장소 | 프로세스의 커널 자원구조체 내에 연결 리스트 혹은 트리 형태로 보관 | Kernel Data Structure | 지갑 혹은 키링 |
| **Reference Monitor** | 검증기 | 시스템 콜(System Call) 시 요청된 토큰이 유효한지(위조 여부, 권한 범위) 확인 | Kernel Space Logic | 티켓 단말기 |
| **Sealed Objects** | 캡슐화된 데이터 | 특정 Capability를 가진 주체만 내용을 읽거나 실행할 수 있는 보호된 객체 | Encrypted Blob | 열쇠가 필요는 보관함 |
| **Revocation Table** | 권한 회수 레지스트리 | (선택적) 토큰 자체를 무효화하기 어렵기 때문에, 커널 차원에서 특정 토큰 ID를 블랙리스트 처리 | Kernel Map | 분실 신고 리스트 |

### 2. 권한 위임 및 검증 플로우 (Architecture)

아키텍처는 크게 **Token Creation**, **Inheritance/Transfer**, **Validation**의 단계를 거칩니다.

```text
   [User Space: Process A (Parent)]           [Kernel Space]
           |                                       |
   (1) Open Resource (/etc/shadow)               |
           |                                       |
   +-------+---------------------------------------+-------+
   |       |  (2) Kernel returns File Descriptor   |       |
   |       v       + 'Capability Token' (Read)     |       |
   |  [Capability Token]                          |       |
   |  [ Ref: 0x4A2 | Perms: R----- | Sign: Key_K ] |       |
   |       |                                       |       |
   +-------+---------------------------------------+-------+
           |                                       |
   (3) Fork() / IPC msg_send()                    |
           |                                       |
           v  (4) Pass Token Copy to Child         |
   [User Space: Process B (Child)]                 |
           |                                       |
   (5) Syscall: write(Ref: 0x4A2, "Data") -------->---+
           |                                       |
           |                              (6) Lookup Capability Table
           |                              (7) Validate Token Signature
           |                              (8) Check Permission (Write?)
           |                                       |
           | <------ (9) -EACCES (Error) ----------+  (Failed: Read-only Token)
           |
           v
```

**[다이어그램 해설]**
1.  **부모 프로세스(A)**가 커널에게 자원(`/etc/shadow`)을 요청하면, 커널은 해당 자원에 대한 **읽기 전용(Read-only)** 토큰을 생성하여 반환합니다.
2.  자식 프로세스(B)는 `fork()` 혹은 IPC를 통해 이 토큰을 상속받거나 전달받습니다. 이 과정에서 토큰의 내용(권한 비트)은 수정될 수 없습니다.
3.  자식 프로세스가 `write()` 시스템 콜을 통해 해당 자원에 쓰기를 시도합니다.
4.  커널의 **레퍼런스 모니터(Reference Monitor)**는 전달된 토큰을 검사합니다. 토큰이 가진 권한이 '읽기(Read)'이므로 '쓰기(Write)' 작업은 거부됩니다(`-EACCES`).
5.  이 과정에서 자식 프로세스가 토큰의 권한 비트를 '쓰기'로 조작하여 위조하려 하면, 커널의 암호화 서명(Cryptographic Signature) 또는 보호된 메모리 영역 검사를 통해 이를 감지하고 프로세스를 강제 종료시킵니다.

### 3. 핵심 기술: Linux Capabilities (실무 적용)
리눅스 커널 2.2 이후부터 도입된 **POSIX Capabilities**는 `root` 권한(UID 0)의 특권을 30개 이상의 세부 권한으로 분할했습니다.
*   **CAP_CHOWN**: 파일 소유자 변경 가능
*   **CAP_NET_BIND_SERVICE**: 1024번 이하의 포트(Well-known Port) 바인드 가능
*   **CAP_SYS_ADMIN**: "만능 권한". 이 권한만 있으면 사실상 루트와 같음. (따라서 이 권한을 제거하는 것이 보안의 핵심)

**[코드 예시: Docker Container에서 불필요한 Capability 제거]**
도커는 기본적으로 컨테이너에게 많은 Capability를 부여합니다. 공격 표면 감소를 위해 `--cap-drop` 옵션을 사용합니다.

```bash
# 안전하지 않은 설정 (모든 권한 부여)
docker run --privileged ubuntu bash

# 안전한 설정 (SYS_ADMIN, NET_ADMIN 등 불필요한 권한 제거)
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx
# 1. --cap-drop=ALL: 모든 토큰을 회수
# 2. --cap-add=NET_BIND_SERVICE: 웹 서버 운영을 위해 80번 포트 바인드 권한만 재부여
```

📢 **섹션 요약 비유**:
이 아키텍처는 "도장관리 센터가 모든 문서를 열어보고 허가하는 것(ACL) 대신, 진짜 도장(Capability)을 가진 사람만 도장을 찍을 수 있게 하고, 도장 자체에 '이 도장은 계약서에만 찍을 수 있다'는 규제가 새겨져 있는 시스템"과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Analysis)

### 1. ACL vs Capability: 심층 기술 비교

| 구분 | ACL (Access Control List) | Capability (Cap-based) |
|:---|:---|:---|
| **접근 제어 위치** | **자원(Object) 측면**<br>파일 메타데이터에 허용된 주체 목록 저장 | **주체(Subject) 측면**<br>프로세스가 자원에 대한 열쇠(Token)를 소유 |
| **검증 메커니즘** | 자원에 접근할 때마다 중앙 DB(파일 시스템) 쿼리 필요 | 토큰의 소유 여부만 확인 (빠른 경로) |
| **권한 위임 (Delegation)** | 복잡하고 구조적으로 어려움 (관리자 개입 필요) | 토큰 복사/전송만으로 자유로운 위임 가능 |
| **권한 회수 (Revocation)** | 리스트에서 제거만 하면 됨 (쉬움) | 이미 흩어진 토큰을 일일이 찾아야 함 (어려움) |
| **Confused Deputy 방어** | 취약함 (경비원을 속일 수 있음) | 강력함 (열쇠가 없으면 경비원도 못 들어감) |
| **주요 사용처** | **기업 내부 DB, 파일 서버** (관리 중심) | **분산 시스템, 마이크로커널, 블록체인** (신뢰 최소화) |

### 2. 보안 공격 시나리오 분석 (Confused Deputy)

**[시나리오]**
컴파일러(Compiler)는 사용자의 소스 코드를 읽고, 결과를 목적 파일(Object File)로 씁니다. 사용자는 컴파일러에게 "시스템 설정 파일(/etc/passwd)을 삭제하라"는 악의적인 명령을 포함하여 전달합니다.

*   **ACL 환경 (취약)**: 컴파일러는 시스템 관리자의 권한을 가집니다. 컴파일러가 "이 사용자가 파일을 쓰라고 했다"고 하면, 시스템은 컴파일러의 권한을 보고 /etc/passwd 삭제를 승인합니다. (컴파일러가 악의적인 사용자의 '대리자'로 작동)
*   **Capability 환경 (안전)**: 컴파일러는 소스 코드에 대한 `Read Token`과 목적 파일에 대한 `Write Token`만 가지고 있습니다. 사용자가 `/etc/passwd`에 대한 `Delete Token`을 가지고 있지 않다면, 컴파일러에게 해당 명령을 내려도 실행할 수 있는 토큰이 없으므로 시스템은 거부합니다.

### 3. 타 기술과의 융합 (Convergence)
*   **Blockchain (Web3)**: 이더리움(Ethereum)의 스마트 컨트랙트나 NFT는 사실상 Capability의 일종입니다. "이 주소(Private Key)를 가진 사람만 이 토큰(NFT)을 옮길 수 있다"는 논리는 Capability의 핵심 메커니즘과 동일합니다.
*   **Microkernel OS (Minix, seL4)**: 모든 디바이스 드라이버와 서비스가 사용자 공간에서 실행되며, 서로 간의 통신을 **IPC (Inter-Process Communication)**와 Capability 토큰으로만 제어합니다. 이로 인해 커널 버그가 발생해도 전체 시스템 장애로 이어지는 것을 막습니다.

📢 **섹션 요약 비유**:
ACL vs Capability의 차이는 "VIP 라운지 입장(ACL)"과 "놀이터 자유이용권(Capability)"의 차이와 같습니다. VIP 라운지는 명단을 관리해야 하고 입장 시마다 확인해야 하지만, 자유이용권은 손님끼리 서로 양도하기 쉽고 입구 게이트가 별도로 필요 없습니다. 다만, 자유이용권을 잃어버리거나 남에게 뺏기면 관리가 어려운 단점이 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 취약점 분석 및 완화
**상황**: 웹 서버(Nginx)가 해킹당하여 **RCE (Remote Code Execution)** 공격을 받았습니다. 공격자는 리눅스 커널에 직접 접근하려 합니다.

*   **기존 방식 (Root 권한으로 실행)**: 공격자가 웹 서버 프로세스를 탈취하면 `root` 권한을 얻습니다. 공격자는 방화벽 규칙(`iptables`)을 삭제하거나, 시스템 로그를 지우거나, `/etc/sh