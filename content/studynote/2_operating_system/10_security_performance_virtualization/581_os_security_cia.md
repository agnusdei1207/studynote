+++
title = "581. 운영체제 보안 (OS Security) 목표 - CIA (기밀성, 무결성, 가용성)"
date = "2026-03-14"
+++

# 581. 운영체제 보안 (OS Security) 목표 - CIA (기밀성, 무결성, 가용성)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**= 운영체제 보안의 궁극적 목표는 **CIA Triad (Confidentiality, Integrity, Availability)**라는 3대 지표를 기술적, 물리적, 관리적 관점에서 완벽하게 구현하는 데 있습니다.
> 2. **가치**= 단순한 외부 침입 방지를 넘어, 시스템의 신뢰성을 확보하여 비즈니스 연속성을 보장하며, 데이터 유출 사고 시 막대한 피해(평균 430만 달러/건)를 사전에 차단합니다.
> 3. **융합**= 커널(Kernel)의 자원 관리 메커니즘, 네트워크 패킷 필터링, 그리고 데이터베이스의 트랜잭션 무결성이 유기적으로 결합된 종합 방어 체계입니다.




### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
운영체제 보안(Operating System Security)의 **CIA (Confidentiality, Integrity, Availability)**는 정보 보호의 3대 요소를 의미합니다.
- **기밀성(Confidentiality)**: 인가되지 않은 주체로부터 정보를 보호하는 것.
- **무결성(Integrity)**: 정보가 승인된 방식으로만 변경되었음을 보장하는 것.
- **가용성(Availability)**: 필요한 시점에 정당한 사용자가 자원에 접근할 수 있도록 보장하는 것.

이는 컴퓨터 시스템의 자원(CPU, Memory, I/O 등)을 관리하는 **OS (Operating System)**의 핵심 기능인 **참조 모니터(Reference Monitor)** 개념에 기반합니다.

**등장 배경**
1.  **다중 프로그래밍(Multiprogramming) 환경의 도래**: 하나의 시스템 자원을 여러 프로세스가 공유하면서, 타인의 데이터를 훔치거나(기밀성 훼손), 시스템을 마비시키는(가용성 훼손) 사례가 급증했습니다.
2.  **네트워크 확장**: 로컬 보안을 넘어 외부의 불특정 다수로부터의 공격을 방어할 필요성이 제기되었습니다.
3.  **정보 자산의 가치 상승**: 금융, 개인신상정보(PII) 등 데이터 자체의 가치가 폭증하며, 단순한 기술적 장애 대응을 넘어선 체계적 보안 프레임워크가 요구되었습니다.

**💡 비유**
운영체제 보안 목표는 **'은행의 금고'**와 같습니다.
-   **기밀성**: 잠금장치가 되어 있어 열쇠 없이는 누구도 볼 수 없다.
-   **무결성**: 금고 안의 금괴가 가짜로 바뀌지 않았음을 보증한다.
-   **가용성**: 예금주가 찾으러 올 때 언제든 금고를 열 수 있다.

📢 **섹션 요약 비유**: CIA 보안 모델은 **'삼중 잠금 장치가 있는 안전한 집'**과 같습니다. 첫째, 열쇠 없이는 못 들어가게 막고(기밀성), 둘째, 도둑이 들어와도 물건을 바꿔치기 못하게 하고(무결성), 셋째, 주인이 문을 열려고 할 때 문고리가 고장 나지 않게 관리하는 것(가용성)입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 프로토콜/기술 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **참조 모니터**<br>(Reference Monitor) | 접근 결정의 중계자 | 요청을 가로채 보안 정책(Security Policy)에 근거하여 허가/거부 | Kernel-level Hooks | 건물 경비실 |
| **보안 커널**<br>(Security Kernel) | 참조 모니터를 구현하는 HW/SHW | TCB(Trusted Computing Base)의 일부로, 침입 불가능한 영역에서 작동 | Ring 0 Privilege | 경비원의 뇌 |
| **주체(Subject)** | 자원에 접근하는 능동적 개체 | 프로세스, 스레드, 사용자 | PID, UID | 방문자 |
| **객체(Object)** | 접근의 대상이 되는 수동적 개체 | 파일, 메모리, 포트, 장치 | Inode, Socket | 보관된 물건 |
| **보안 속성**<br>(Security Attributes) | 접근 권한 판단 기준 | ACL(Access Control List), Capability | DAC, MAC | 출입명단/명찰 |

**OS 보안의 계층별 아키텍처 (ASCII Diagram)**

아래 다이어그램은 운영체제에서 사용자의 요청이 CIA 보안 정책을 통해 검증되어 자원에 접근하는 흐름을 도식화한 것입니다.

```text
+-------------------+       +-----------------------+       +-------------------+
|   User Applications|       |    Operating System   |       |   Hardware /      |
|   (Subject)        |       |   (Security Kernel)   |       |   Resources       |
+-------------------+       +-----------------------+       +-------------------+
         |                          |       |                       ^
         |  ① Request Access         |       |                       |
         +-------------------------->|       |                       |
                                    |       |                       |
            +-----------------------+       |                       |
            | ② Invoke Reference Monitor     |                       |
            | (System Call / Trap)           |                       |
            |                               v                       |
            |      +-----------------------------------+            |
            |      |   ③ Security Policy Database       |            |
            |      |   (ACL / Labels / Rules)           |            |
            |      +-----------------------------------+            |
            |              |                                 |      |
            |              | ④ Decision (Allow/Deny)         |      |
            |              v                                 |      |
            |   +-----------------------------+              |      |
            +---| ⑤ Enforcement Mechanism     |--------------+      |
                | (Apply Privilege / Context) |                     |
                +-----------------------------+                     |
                        ^                                           |
                        | ⑥ Read/Write (Protected)                 |
                        +-------------------------------------------+

[Legend]
 ①: 사용자(프로세스)가 시스템 콜을 통해 자원 접근 요청
 ②: 요청이 커널 모드(Kernel Mode)로 전환되며 참조 모니터 호출
 ③: 참조 모니터가 보안 정책 DB(ACL 등) 조회
 ④: 정책에 따른 접근 허용 여부 판단 (Confidentiality/Integrity Check)
 ⑤: 허용 시, 주체에게 권한 부여 및 객체와의 연결 설정
 ⑥: 실제 하드웨어 자원(IO, Memory)에 대한 명령 수행 (Availability Check)
```

**심층 동작 원리**
1.  **트랩(Trap)과 모드 전환**: 사용자 모드(User Mode, Ring 3)에서 실행되던 프로세스가 시스템 자원(I/O, Memory)에 접근하기 위해 **시스템 콜(System Call)**을 발생시키면, 하드웨어 인터럽트(Trap)를 통해 **커널 모드(Kernel Mode, Ring 0)**로 전환됩니다. 이때 보안 커널이 개입합니다.
2.  **주체-객체 매칭**: 커널은 요청 프로세스의 **UID(User ID)**와 **GID(Group ID)**를 확인하고, 대상 파일이나 메모리의 **Permission Bit**나 **ACL(Access Control List)**을 대조합니다.
    -   *C (Confidentiality)*: 읽기(Read) 권한이 없으면 `EACCES` 반환.
    -   *I (Integrity)*: 쓰기(Write) 권한이 없으면 거부.
3.  **자원 스케줄링**: **A (Availability)**를 위해 커널은 **스케줄러(Scheduler)**를 통해 특정 프로세스가 CPU 시간을 독점하는 것을 방지하고, 메모리 보호(Memory Protection)를 통해 다른 프로세스의 영역을 침범하지 않도록 **MMU(Memory Management Unit)**를 제어합니다.

**핵심 알고리즘 및 데이터 (DAC 예시)**
리눅스 커널의 `permission()` 함수는 다음과 같은 비트 연산을 통해 접근을 제어합니다.

```c
// Simplified Linux Kernel Permission Check Logic
// euid: Effective User ID, uid: Owner's User ID
// inode->i_mode: rwxrwxrwx (Permission Bits)

int generic_permission(struct inode *inode, int mask)
{
    // 1. Check Superuser (Root) - Root usually bypasses standard checks
    if (capable(CAP_DAC_OVERRIDE)) // Privilege check
        return 0;

    // 2. Check Owner Permission
    if (current_fsuid() == inode->i_uid)
        return (inode->i_mode & (mask >> 6)) ? 0 : -EACCES;

    // 3. Check Group Permission
    if (in_group_p(inode->i_gid))
        return (inode->i_mode & (mask >> 3)) ? 0 : -EACCES;

    // 4. Check Other Permission
    return (inode->i_mode & mask) ? 0 : -EACCES;
}
// mask: MAY_READ (4), MAY_WRITE (2), MAY_EXEC (1)
// '>>' 연산을 통해 비트 위치를 이동시켜 해당 권한 비트를 검증함.
```

📢 **섹션 요약 비유**: 운영체제의 보안 아키텍처는 **'첨단 보안 인공지능이 장착된 경비 시스템'**과 같습니다. 누가, 언제, 어디로 들어가려는지 실시간으로 감시하고(기밀성), 출입 명부를 대조한 뒤(무결성), 정상적인 출입만 허용하여 문이 막히지 않도록(가용성) 제어합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**접근 제어 모델 비교 분석 (MAC vs DAC)**

| 비교 항목 (Criteria) | **DAC (Discretionary Access Control)** | **MAC (Mandatory Access Control)** |
|:---|:---|:---|
| **결정 권한 (Decision Maker)** | 자원 소유자(Owner) | 시스템 관리자 및 보안 정책 |
| **자율성 (Autonomy)** | 높음 (사용자가 권한 설정 가능) | 낮음 (중앙에서 통제) |
| **기밀성 강도 (C)** | 중간 (소유자의 실수로 유출 가능) | 매우 높음 (강제적 격리) |
| **가용성/편의성 (A)** | 높음 (협업에 유연) | 낮음 (관리 복잡, 오버헤드) |
| **대표 예시 (Examples)** | Windows 파일 권한, Linux Permission | SELinux, Military MLS System |

**모델별 데이터 흐름 비교 (ASCII Diagram)**

```text
      [DAC Model]                          [MAC Model]
(자율적 접근 제어 - Owner 중심)          (강제적 접근 제어 - Label 중심)

  [File Owner]                           [Security Policy]
  (Alice)                                (Top Secret > Secret > Unclassified)
      |                                       ^
      | Sets Write for Bob                   | Classifies Object
      v                                       |
  [File ACL]                             [Object: Report.txt]
  Allow: Bob:Read                         Label: [Secret]
  Allow: Carol:Write                        ^
      |                                       |
      | Request Access                        | Request Access
      v                                       v
  [Subject: Bob]                        [Subject: User (Clearance)]
  (If Bob wants to write)                (If User Clearance < Secret)
          |                                       |
          +---> [OS Checks ACL]                   +---> [OS Compares Labels]
                       |                                       |
          Grant (Allow) or Deny                    DENY (No Write Up)
                       |                                       |
                   (Flexible)                             (Rigid)
```
**해설**:
-   **DAC**: 사용자가 자신의 파일 접근 권한을 자유롭게 설정할 수 있습니다. 협업 환경에서 유리하지만, 악의적인 코드가 사용자 권한을 탈취하면 방어가 어렵습니다.
-   **MAC**: 시스템이 부여한 보안 레벨(Label)을 기준으로 읽기(No Read Down), 쓰기(No Write Up)를 강제합니다. **기밀성(C)**을 최우선으로 하는 군사/금융 시스템에 필수적입니다.

**과목 융합 관점 (Convergence)**
1.  **네트워크(방화벽)와의 융합**:
    -   OS의 **패킷 필터링(Packet Filtering)** 기능은 네트워크 계층의 보안과 연결됩니다. 포트(Port) 번호를 기반으로 특정 IP나 프로토콜(ICMP, TCP 등)의 접근을 차단하여 **가용성(A)** 공격(예: Ping of Death)을 방어합니다.
2.  **컴퓨터 구조(메모리)와의 융합**:
    -   **가상 메모리(Virtual Memory)**와 **페이지 테이블(Page Table)**은 각 프로세스에게 독립적인 메모리 공간을 부여합니다. 이는 **기밀성(C)**을 보장하는 하드웨어적 차폐 기제입니다. 다른 프로세스의 물리 메모리를 절대 접근할 수 없게 설계되어 있습니다.

📢 **섹션 요약 비유**: MAC과 DAC의 관계는 **'일반 사무실'과 '군사 기지'**의 차이와 같습니다. 일반 사무실(DAC)은 직원이 재량으로 방문객을 들일 수 있지만, 군사 기지(MAC)는 본인의 허가가 있어도 보안 레벨 규정에 따라 출입이 엄격히 제한됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

| 시나리오 (Scenario) | 보안 위협 (Threat) | 의사결정 (Decision) | 적용 기술 (Technology) |
|:---|:---|:---|:---|
| **[S1] 금융 서버 증권 거래**| 거래 내용 위변조, 부정 거래 | **무결성(I) 최우선** <br>(트랜잭션 원자성 보장) | ACID 트랜잭션, DBMS 무결성 제약조건, 디지털 서명 |
| **[S2] 공공기관 개인정보 DB** | 개인 신용정보 유출 | **기밀성(C) 최우선** <br>(접근 통제 및 암호화) | AES-256 암호화, 망 분리, Row-Level Security |
| **[S3] 대형 커머스 쇼핑몰** | 추석 기간 트래픽 폭주 | **가용성(A) 최우선** <br>(부하 분산 및 이중화) | L4/L7 스위치, 로드 밸런싱, Auto-scaling, Failover Cluster |

**도입 체크리스트**
-   **[ ] 기술적 측면**
    -   최신 보안 패치(Patch)가 적용되었는가? (OS Kernel Version)
    -   불필요한 서비스/포트가 비활성화되었는가? (Hardening)
    -   강력한 인증(Authentication) 및 MFA(Multi-Factor Authentication)가 구현되었는가?
-   **[ ] 운영/보안적 �