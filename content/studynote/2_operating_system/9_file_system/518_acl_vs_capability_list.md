+++
title = "518. 파일 보호 메커니즘 - 접근 제어 리스트 (ACL) vs 능력 리스트 (Capability List)"
date = "2026-03-14"
weight = 518
+++

# 518. 파일 보호 메커니즘 - 접근 제어 리스트 (ACL) vs 능력 리스트 (Capability List)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **ACL (Access Control List)**과 **C-List (Capability List)**는 추상적인 **접근 행렬 (Access Matrix)**을 물리적으로 구현하는 두 가지 상호 보완적인 데이터 구조로, 각각 자원 중심의 '명부 관리'와 사용자 중심의 '권한 증명'을 담당한다.
> 2. **가치**: ACL은 관리성(권한 회수 용이성)과 무결성에서 우위를 점해 **권장 보안 정책 (Discretionary Access Control)** 구현에 적합하며, C-List는 접근 검증의 **속도(Latency)**와 분산 환경에서의 **위임(Delegation)** 효율성에서 월등한 성능을 발휘한다.
> 3. **융합**: 현대 OS(운영체제)는 이 둘을 대립시키지 않고, 파일 오픈 시점의 엄격한 ACL 검증과 이후 **FD (File Descriptor)**를 통한 Capability 방식의 고속 처리를 결합한 하이브리드 아키텍처를 통해 보안과 성능의 균형을 달성한다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
운영체제에서의 파일 보호는 **주체 (Subject, Process/User)**가 **객체 (Object, File/Device)**에 접근을 시도할 때, 보안 정책에 부합하는지 심사하는 기능이다. 이를 이론적으로 모델링한 것이 **Access Matrix (접근 행렬)**로, 행(Row)은 주체, 열(Column)은 객체를 나타내며 셀(Cell)은 권한(R/W/X)을 저장한다. 그러나 현대의 시스템은 수백만 개의 파일과 사용자를 가지므로, 이 행렬을 그대로 메모리에 적재하면 대부분의 엔트리가 'Null(Sparse)'인 희소 행렬 문제로 인해 막대한 공간 낭비가 발생한다. 이를 해결하기 위해 행렬의 열(Column)을 자르면 **ACL**, 행(Row)을 자르면 **C-List**가 되는 구조적 최적화가 적용된다.

**2. 기술적 배경 및 진화**
- **초기 컴퓨팅**: 시분할 시스템(TSS) 등장 이전 단일 사용자 환경에서는 파일 잠금(File Lock) 정도만으로 충분했다.
- **다중 사용자 및 보안 요청**: 다중 사용자 환경에서는 정보 격리(Isolation)와 공유(Sharing)가 동시에 요구되었다. 단순한 9비트 모드(User/Group/Other)로는 정교한 권한 제어가 불가능하여, 리스트 기반의 접근 제어가 도입되었다.
- **분산 시스템의 도입**: 네트워크 환경에서는 중앙 집중식 ACL 관리가 병목이 되어, 토큰 기반의 Capability 개념이 웹(Web) 및 클라우드(Cloud) 보안으로 확장되었다.

```text
     [ Theoretical Access Matrix ]
            
                 File_A    File_B    File_C
     User_1      Read      -         Write
     User_2      -         Read      Execute
     User_3      R/W       -         -
     
     ▼ Physical Decomposition ▼
     
     [ ACL Logic (Column-wise) ]         [ Capability Logic (Row-wise) ]
     
     File_A Header:                       User_1's C-List:
     ┌─────────────────────┐              ┌──────────────────────────┐
     │ User_1: Read        │              │ Token_A: (ptr_A, Read)   │
     │ User_3: R/W         │              │ Token_C: (ptr_C, Write)  │
     │ (Others: None)      │              └──────────────────────────┘
     └─────────────────────┘
```

> **다이어그램 해설**: 이 다이어그램은 논리적인 접근 행렬이 어떻게 물리적인 저장소의 구분으로 대응되는지 보여줍니다. ACL은 파일(객체)마다 "누가 나에게 들어올 수 있는가?"라는 명단을 헤더에 붙이는 방식(Sparse Column)이고, Capability List는 사용자(주체)마다 "내가 무엇을 할 수 있는 권한(티켓)을 가졌는가?"라는 지갑을 소지하게 하는 방식(Sparse Row)입니다. 시스템 설계자는 메모리 효율성과 검색 속도 사이에서 이 둘 중 하나를 선택하거나 혼용하게 됩니다.

📢 **섹션 요약 비유**: ACL은 각 상점마다 "출입 허가 명단"을 걸어두고 확인하는 것과 같고, Capability List는 손님마다 "회원증(Key)"을 지니게 하여 제시하면 통과시키는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 동작 메커니즘 비교**

| 구분 | ACL (Access Control List) | Capability List (C-List) |
|:---|:---|:---|
| **기본 단위** | **ACE (Access Control Entry)** | **Token (Capability)** |
| **관점** | 객체(Object) 중심 ("내 허락은 누구에게?") | 주체(Subject) 중심 ("내 권한은 무엇인가?") |
| **저장 위치** | 자원의 **Inode** / **MFT** (디스크 메타데이터) | 주체의 **PCB (Process Control Block)** / **CAP Table** (메모리) |
| **검증 방식** | `Lookup(Object, Subject_ID)` → 순회 검색 | `Validation(Token)` → 즉시 참조 |
| **보안 강화** | 관리자 주도의 통제 용이 | **Tagged Architecture** / **Encryption** 필요 |
| **주요 용도** | 일반적인 파일 시스템 (Linux, Windows) | 마이크로커널, 분산 시스템, GPU 드라이버 |

**2. ACL (Access Control List) 심층 분석**
ACL은 파일 시스템 객체 내부에 **ACE (Access Control Entry)**의 연결 리스트 형태로 저장된다. 현대 파일 시스템(예: **NTFS**, **ext4 with xattr**)은 소유자, 그룹, 그리고 **DACL (Discretionary ACL)**을 포함한 복잡한 구조를 가진다.

- **동작 원리 (System Call Flow)**:
  1. 사용자 프로세스가 `open("secret.txt", O_RDONLY)` 호출.
  2. **VFS (Virtual File System)**는 해당 파일의 Inode를 로드.
  3. 커널은 Inode 내의 ACL 리스트를 **Linear Search**하여 현재 프로세스의 **UID (User ID)**, **GID (Group ID)** 및 권한 비트를 비교.
  4. 일치하는 항목 발견 시, 커널은 **Open File Description**을 생성하고 사용자 공간에 **FD (File Descriptor)**를 반환한다. 이후 I/O 요청은 FD를 통해 이루어지므로 추가 검사가 필요 없다.

**3. Capability List 심층 분석**
Capability는 단순한 포인터가 아니라 "권한을 가진 비트"다. 해커가 임의의 포인터를 조작해 권한을 탈취하지 못하도록, 하드웨어적으로 주소 공간을 분리하거나 **Cryptographic Capabilities**를 사용한다.

- **구조**: `struct capability { void *obj_ptr; uint32_t rights; bool valid; }`
- **동작 원리**:
  1. 프로세스가 Capability(C-List 내의 인덱스)를 통해 자원 접근 요청.
  2. 하드웨어 또는 커널은 해당 Capability가 **User Space**에서 위조되지 않았는지 **Tagged Bit**나 암호학적 서명을 확인.
  3. 검증 즉시 `obj_ptr`을 통해 **Memory Mapping**을 수행하므로 별도의 권한 테이블 검색이 없어 매우 빠르다.

```text
    [ ACL Implementation: Linux ext4 Inode ]
    
    Inode #12345 (Metadata)
    ┌─────────────────────────────────────┐
    │ Mode: 0644 (rw-r--r--)              │
    │ Owner: uid=1000 (admin)             │
    │ Extended Attributes (xattr):        │
    │   system.posix_acl_access:          │
    │     { ACL_USER_OBJ: rwx }           │
    │     { ACL_USER: uid=1001: r-- } ◄───┐ Explicit ACE
    │     { ACL_OTHER: --- }              │
    └─────────────────────────────────────┘
                                        │
                [Access Check]           │
                Is uid=1001 in list? ────┘
    
    ========================================
    
    [ Capability Implementation: Memory Token ]
    
    Process Kernel Stack
    ┌─────────────────────────────────────┐
    │ C-List (Capability List):           │
    │ [0] │ Addr: 0xF00... │ Perms: RW │ 1 │ ◄─── Valid Token (Ticket)
    │ [1] │ Addr: 0xBA0... │ Perms: R  │ 1 │
    │ [2] │ Addr: 0x000... │ Perms: -  │ 0 │ ◄─── Invalid/Expired
    └─────────────────────────────────────┘
          │
          ▼ Present Capability
    [ Hardware / MMU Check ]
    Is Token[0].Tag == VALID? ──▶ YES ──▶ Direct Memory Access
```

> **다이어그램 해설**: 위 도표는 두 메커니즘의 구현적 차이를 메모리 관점에서 나타낸 것입니다. ACL은 디스크의 Inode와 같은 정적 메타데이터에 의존하여 접근 시마다 명단을 검색(Search)하는 비용이 발생합니다. 반면, Capability는 프로세스의 메모리 공간에 이미 '승인된 키(Token)' 형태로 존재하며, 하드웨어(MMU)는 이 키의 유효성만 확인(Check)하면 즉시 자원에 연결해 주므로 접근 속도가 훨씬 빠릅니다.

📢 **섹션 요약 비유**: ACL은 **"매번 입장권을 확인하고 명단을 찾아보는 야구장 티켓 부스"** 같고, Capability는 **"이미 등록된 사원증을 리더기에 찍기만 하면 통과하는 사무실 출입문"**과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 정량적 지표에 따른 비교 분석**

| 비교 항목 | ACL (Access Control List) | Capability List |
|:---|:---|:---|
| **검색 시간 복잡도** | **O(N)**: 사용자 그룹이 많을수록 느려짐 (Linear Search) | **O(1)**: 인덱스를 통한 직접 접근 |
| **권한 회수 (Revocation)** | **매우 용이함**: 파일 설정에서 ACE 삭제만으로 즉시 차단됨 (Global Revocation) | **매우 어려움**: 사용자가 가진 토큰 회수가 불가능능함. **Indirection Table** 사용 필요 |
| **위임 (Delegation)** | **불가능**: 중앙 관리자만 설정 가능 (DAC 원칙) | **자유로움**: 토큰 복사로 타인에게 권한 양도 가능 (분산 환경 유리) |
| **저장 공간 효율** | **자원 중심**: 공유자가 적은 파일에 유리 | **사용자 중심**: 접근 자원이 적은 사용자에게 유리 |
| **무결성 및 보안** | 높음: 데이터의 소유자가 제어 | 낮음(위험): 토큰 탈취 시 권한 노출, 암호화 필수 |

**2. 타 영역과의 융합 및 시너지**

- **분산 시스템 및 웹 보안 (Cloud Computing)**:
  클라우드 환경(예: AWS S3)에서는 **S3 Bucket Policy**와 **IAM Policy**의 조합으로 ACL의 개념을 확장 사용합니다. 한편, 현대 웹의 **OAuth 2.0**이나 **JWT (JSON Web Token)**는 전형적인 Capability List 구조입니다. 사용자가 Access Token(권한 증명)을 발급받으면, 서버는 매번 DB(ACL)를 조회하지 않고 Token의 **Signature**만 검증하여 요청을 처리합니다. 이는 대규모 트래픽 처리에서 **Statelessness**를 유지하는 핵심 기술입니다.

- **마이크로커널 아키텍처 (OS)**:
  **seL4**나 **MINIX 3** 같은 마이크로커널은 IPC(Inter-Process Communication)를 통해 모든 서비스를 수행합니다. 이때 프로세스 간 서비스 요청은 Capability(메시지에 포함된 권한)를 통해 이루어지며, 이는 커널의 오버헤드를 최소화하고 격리를 강화합니다.

```text
          [ Scenario: Access Revocation Difficulty ]
          
     (ACL Model) User A ──▶ [ File: data.txt ]
                             │
                      System Admin
                             │
                   [ Edit ACL: Remove A ] ──▶ A is immediately BLOCKED.
     
     
     (Capability Model) User A holds Token ──▶ [ System Gate ]
                               │
                               │  (Revocation is hard!)
                               ▼
     ┌─────────────────────────────────────────┐
     │ Global Indirection Table (Master List)  │
     │ Token_A ──▶ Valid (True) ──▶ GRANT     │
     │ Token_B ──▶ Valid (True) ──▶ GRANT     │
     └─────────────────────────────────────────┘
     
     ▶ To revoke A:
     System must change Table_A to False.
     (Even if A has Token, System says "Expired")
```

> **다이어그램 해설**: 이 도표는 권한 회수(Revocation) 문제에서 오는 두 철학의 차이를 보여줍니다. ACL은 명단 관리자가 이름을 지우면 그 즉시 모든 접근이 차단되는 직관적이고 강력한 통제력을 제공합니다. 반면 Capability는 이미 나간 '티켓'을 회수하기 위해 시스템 전체의 '유효성 데이터베이스(Indirection Table)'를 업데이트해야 하거나, 티켓의 유효 기간(Expiry)을 짧게 설정하여 주기적으로 재갱신하게 만드는 간접적인 방법을 사용해야 합니다.

📢 **섹션 요약 비유**: ACL은 **"출입 명단에서 이름을 지워서 방지하는 것"**이고, Capability는 **"이미 나눠준 입장권을 무효화시키기 위해 무선 주파수로 방송(RFID Kill)해야 하는 것"**과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오: 하이브리드 전략의 필연성**
리눅스나 윈도우 같은 범용 OS는 완전한 ACL 방식을 채택하지만, 성능 최적화를 위해 내부적으로 Capability의 개념을 차용합니다.

- **문제 상황**: 매번 `read()` 시스템 콜마다 디스크의 ACL을 검색하면 성