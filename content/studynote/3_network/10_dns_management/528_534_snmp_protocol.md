+++
title = "528-534. SNMP(Simple Network Management Protocol) 분석"
date = "2026-03-14"
[extra]
category = "DNS & Management"
id = 528
+++

# 528-534. SNMP(Simple Network Management Protocol) 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 대규모 네트워크 인프라의 가용성과 성능을 확보하기 위해 장비의 상태 정보를 표준화된 방식으로 수집하고 제어하는 **애플리케이션 계층(Application Layer) 프로토콜**이자 관리 철학이다.
> 2. **가치**: 수동 관리의 한계를 극복하여 **NMS (Network Management System)**를 통한 자동화된 모니터링 및 능동적 장애 대응(Trap)을 가능하게 하며, 운영 비용을 획기적으로 절감한다.
> 3. **융합**: **UDP (User Datagram Protocol)** 기반의 가벼운 통신과 **MIB (Management Information Base)**라는 데이터 구조를 통해 이기종 장비 간의 통합 관리를 실현하며, 보안 강화를 위한 **v3 (USM)**로 진화하고 있다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**SNMP (Simple Network Management Protocol)**는 인터넷 표준화 기구인 **IETF (Internet Engineering Task Force)**에서 정의한 프로토콜로, TCP/IP 기반 네트워크상의 장비(라우터, 스위치, 서버, 프린터 등)를 중앙에서 감시하고 제어하기 위해 사용된다. 이는 OSI 7계층 중 **애플리케이션 계층(Application Layer)**에 속하며, 물리적인 매체나 전송 계층의 종류에 독립적으로 동작하는 표준화된 인터페이스를 제공한다.

#### 2. 등장 배경 및 필요성
과거 소규모 네트워크에서는 관리자가 장비 앞에 가서 콘솔을 연결하며 상태를 확인했으나, 인터넷 폭발적으로 성장함에 따라 다음과 같은 문제가 발생했다.
- **관리의 복잡성**: 벤더별(Cisco, Juniper 등) 상이한 명령어(CLI) 체계로 인한 통합 관리 불가.
- **비효율성**: 수만 대의 장비를 주기적으로 점검하는 것은 물리적으로 불가능에 가까움.
- **수동적 대응**: 장애 발생 시 사용이 신고하기 전까지는 관리자가 인지하지 못하는 'Fire Fighting' 방식.

이를 해결하기 위해 장비의 상태 변수를 표준화된 트리 구조로 정의하고, 관리 서버가 이를 원격으로 조회(Get)하거나 제어(Set)할 수 있는 표준 프로토콜 탄생하였다.

#### 3. 통신 특성 및 구조
SNMP는 **UDP (User Datagram Protocol)** 포트 **161번**(일반 질의/응답)과 **162번**(Trap 알림)을 사용한다. 연결 지향형 TCP보다 신뢰성은 낮지만 오버헤드가 적어, 네트워크 관리 트래픽이 실제 비즈니스 트래픽에 영향을 주지 않으면서 빠른 상태 파악이 가능하다는 장점이 있다.

```ascii
[ SNMP 통신 포트 구조 ]

+----------------+                       +----------------+
|   NMS (Manager) |                       |   Device (Agent)|
|   (Active)      |                       |   (Passive)     |
+----------------+                       +----------------+
        |                                        ^
        | (1) Polling: Get/GetBulk/Set          | (2) Notification: Trap/Inform
        | "Status Check"                         | "Emergency Alert"
        v                                        |
   [ UDP : 161 ]  ---------------------->  [ UDP : 161 ]
        |                                        ^
        |                                        |
        | <-------------------------------------|
   [ UDP : 162 ]  <----------------------  [ UDP : 162 ]
   (Receive Trap)                          (Send Trap)
```
*도입 설명*: SNMP는 크게 관리자가 주도적으로 정보를 요청하는 '폴링(Polling)' 방식과 장비가 이슈 발생 시 스스로 보고하는 '트랩(Trap)' 방식으로 나뉘며, 이를 위해 각기 다른 UDP 포트를 사용한다.
*해설*: 위 다이어그램과 같이 161번 포트는 양방향 요청-응답(RPC 스타일)에 사용되며, 162번 포트는 에이전트가 매니저로 향하는 단방향 알림에 사용된다. 이를 통해 관리자는 주기적으로 장비 상태를 확인하면서도(폴링), 장애 발생 시 즉각적인 알림(트랩)을 받는 이중 모니터링 체계를 갖춘다.

> 📢 **섹션 요약 비유**: SNMP는 아파트의 **중앙 제어실**과 각 가구에 설치된 **계량기**의 관계와 같습니다. 관리 사무소(매니저)는 면대면으로 방문하지 않고도 원격으로 전기/수도 값을 조회(Get)하거나 밸브를 잠글(Set) 수 있으며, 화재 감지기(에이전트)가 비상벨(Trap)을 울려 즉시 상황을 알리는 구조입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
SNMP는 크게 4가지 핵심 요소로 구성되며, 이들은 상호 밀접하게 작용한다.

| 구성 요소 | 역할 및 정의 | 내부 동작 메커니즘 | 주요 프로토콜/포트 | 비유 |
|:---|:---|:---|:---|:---|
| **NMS (Network Management System)** | **관리자(Manager)**. 네트워크 전체를 감시하는 서버. | Agent에게 요청을 보내 정보를 수집하고, GUI나 대시보드로 관리자에게 제공. | UDP 161(Send) / 162(Recv) | **교장 선생님** |
| **Agent** | **피관리자**. 장비(Router, Switch) 내에서 동작하는 프로세스. | MIB 데이터를 유지하며, Manager의 요청이 오면 로컬 데이터를 조회하여 응답. 장애 발생 시 Trap 발송. | UDP 161(Recv) / 162(Send) | **반장** |
| **MIB (Management Information Base)** | **데이터베이스**. 장비의 관리 가능한 객체를 정의한 가상 정보 저장소. | 계층적 트리 구조. OID에 의해 인덱싱됨. Agent의 RAM/Kernel에 상주하며 실시간 값 반영. | - | **학교 생활기록부** |
| **OID (Object Identifier)** | **식별자**. MIB 트리 내의 특정 객체를 가리키는 유일한 주소. | 점(.)으로 구분된 숫자. (예: `1.3.6.1.2.1.1.1.0` - SysDescr) | - | **주민등록번호** |

#### 2. 데이터 구조: SMI 및 MIB 트리
**SMI (Structure of Management Information)**는 MIB의 데이터를 정의하는 규칙이다. 모든 객체는 **OID (Object Identifier)**라는 고유한 주소를 가지며, ISO에서 정의한 전 세계 트리 구조를 따른다.

```ascii
[ MIB Tree 구조 및 OID 예시 ]

 iso(1)
  └─ org(3)
      └─ dod(6)
          └─ internet(1)
              ├─ mgmt(2)
              │   └─ mib-2(1) [RFC 1213]
              │       ├─ system(1)
              │       │   └─ sysDescr(1) [OID: 1.3.6.1.2.1.1.1]
              │       │       └─ sysUpTime(3) [OID: 1.3.6.1.2.1.1.3]
              │       └─ interfaces(2)
              │           └─ ifNumber(1)
              │           └─ ifTable(2) ... (인터페이스별 정보)
              └─ private(4) [벤더별专用]
                  └─ enterprises(1)
                      └─ cisco(9) ... [시스코 전용 OID]
```
*도입 설명*: SNMP는 데이터베이스 스키마가 없이는 작동할 수 없다. MIB는 전 세계 모든 네트워크 객체를 관리하기 위해 국가 코드나 벤더 코드를 포함한 거대한 디렉토리 트리 형태로 정보를 구성한다.
*해설*: 위 트리 구조에서 최상위 `iso(1)`에서 시작하여 하위로 내려갈수록 구체적인 객체를 가리킨다. `1.3.6.1.2.1...` 과 같이 숫자로 된 점 표기법(Dot notation)은 경로(Path)와 같다. 관리자는 이 OID를 쿼리하여 시스템 설명(sysDescr)이나 특정 인터페이스의 트래픽(ifOctets) 수치를 읽어온다. 벤더별 고유 기능은 `private(4).enterprises(1)` 하위에 정의된다.

#### 3. 핵심 PDU (Protocol Data Unit) 및 동작 원리
SNMP는 메시지 단위를 PDU라 부르며, 5가지 주요 유형이 있다.

1.  **GetRequest**: 특정 OID의 값을 요청.
2.  **GetNextRequest**: OID를 모르더라도 다음 항목을 순차적으로 가져올 때 사용 (MIB Walk의 기초).
3.  **GetBulkRequest (v2c 이상)**: 대량의 데이터를 한 번에 효율적으로 요청. (네트워크 부하 감소).
4.  **SetRequest**: 특정 OID의 값(설정)을 변경 (예: 인터페이스 Shutdown).
5.  **Trap**: 비동기적 이벤트 알림.

```ascii
[ SNMP 동작 시퀀스 ]

   Phase 1: Polling (Normal Status Check)
   Manager                       Agent
      |                            |
      | --- GetRequest(oid) -----> |
      |                            | (Read Variable)
      | <--- GetResponse(val) ----- |
      |                            |

   Phase 2: Trap (Emergency Event)
   Manager                       Agent
      |                            |
      |                            | (Link Down Event!)
      | <===== Trap(oid, val) ===== |
      | (Receive Interrupt)        |
      |                            |
```
*도입 설명*: 정상적인 상황에서는 Manager가 Agent에게 "살았니?"라고 묻는 Polling이 주를 이루지만, 장애와 같은 급박한 상황에서는 즉각적인 Trap이 필수적이다.
*해설*: Polling 방식은 주기적 확인이 가능하지만 장애 발견 지연(Latency)이 존재한다. 반면, Trap은 이벤트 발생 즉시 메시지를 보내므로 실시간 모니터링에 유리하다. 다만 UDP 기반이므로 Trap 패킷이 유실될 경우를 대비해 v2에서는 Trap에 대한 응답을 요구하는 'Inform' 메시지도 추가되었다.

#### 4. 핵심 알고리즘: MIB Walk (GetNext 순회)
관리자는 장비의 전체 구조를 몰라도 GetNextRequest를 반복하여 트리를 순회하며 모든 정보를 수집할 수 있다.

> 📢 **섹션 요약 비유**: SNMP 구조는 **거대한 도서관**과 같습니다. **NMS**는 도서관이자이고, **Agent**는 사서입니다. **MIB**는 도서관의 모든 책이 꽂힌 분류 체계이며, **OID**는 그 책의 고유한 청구 기호입니다. 도서관이자가 "이 청구기호(OID)의 책 좀 가져와라(Get)"라고 하면 사서는 책을 주고, "이 책 비치해(Set)"라고 하면 사서는 책을 꽂습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 버전별 심층 기술 비교 (v1 vs v2c vs v3)

| 비교 항목 | SNMP v1 (RFC 1157) | SNMP v2c (RFC 1901) | SNMP v3 (RFC 3414) |
|:---|:---|:---|:---|
| **보안 모델** | Community String (평문) | Community String (평문) | **USM (User-Based Security Model)** |
| **인증 (Authentication)** | None (암호 없음) | None | **MD5 / SHA** (메시지 무결성 검증) |
| **암호화 (Privacy)** | None (암호화 없음) | None | **DES / AES** (패킷 암호화) |
| **메시지 형식** | Simple | **GetBulk** 추가 (대량 조회) | **v2c 형식 계승 + 보안 헤더 추가** |
| **주요 용도** | 폐쇄망, 기본 모니터링 | 일반적인 내부말 모니터링 | **공공기관, 금융권, 외부 노출망** |

#### 2. 기술적 융합 및 시너지
- **보안 강화 (Security Convergence)**: SNMP v1/v2c는 데이터를 평문으로 전송하므로 스니핑 시 장비의 설정이나 상태 정보가 노출될 위험이 크다. 반면 **v3**는 **VPN (Virtual Private Network)** 수준의 보안성을 제공하여 최근 보안 감사의 필수 요구사항이 되었다.
- **OS 및 커널 융합**: SNMP Agent는 운영체제의 **Kernel**과 상호작용하여 CPU 사용률, 메모리 상태, 디스크 I/O 등을 수집한다. 이는 Net-SNMP 데몬이 OS System Call을 통해 '/proc' 파일 시스템(Linux) 등을 읽는 방식으로 구현된다.

> 📢 **섹션 요약 비유**: 버전별 차이는 **편지 전달 방식의 진화**와 같습니다. **v1**은 **봉투 없이 내용이 적힌 엽서**를 던져서 내용이 다 드러나고 위조되기 쉽습니다. **v2**는 배달 효율(대량 전송)은 좋아졌지만 여전히 엽서를 씁니다. **v3**는 **등기 우편**으로, 보낸 사람의 도장(인증)을 찍고 내용을 암호로 잠가(암호화) 배달합니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 프로세스

**시나리오 A: 공공기관 네트워크 모니터링 구축**
- **문제**: 보안 규정에 따라 SNMP 트래픽이 수집되어서는 안 되며, 장비 관리 정보는 기밀로 분류됨.
- **의사결정**:
    1.  SNMP v3 사용이 **강제됨**.
    2.  **AuthPriv** 모드(인증+암호화) 설정 필요 (SHA/AES-128 권장).
    3.  라우터/스위치에서 `snmp-server user` 명령어로 유저별 권한 그룹 설정.
- **결과**: 스니핑 공격에 노출되지 않는 안전