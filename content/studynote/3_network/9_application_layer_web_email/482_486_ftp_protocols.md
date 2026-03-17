+++
title = "482-486. 파일 전송 프로토콜: FTP와 변종들"
date = "2026-03-14"
[extra]
category = "Application Layer"
id = 482
+++

# 482-486. 파일 전송 프로토콜: FTP와 변종들

### # 파일 전송 프로토콜 (File Transfer Protocol)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네트워크 상에서 파일을 송수수하기 위해 **이중 채널(Dual Channel)** 구조(제어용과 데이터용 분리)를 채택한 전형적인 **애플리케이션 계층 프로토콜(Application Layer Protocol)**이다.
> 2. **가치**: 대용량 전송 효율성과 제어 신호의 독립성을 보장하나, **NAT(Network Address Translator)** 및 방화벽 환경에서의 포트 충돌 이슈와 보안 취약성을 야기하므로, 이를 해결하기 위해 암호화 계층(TLS/SSL)이나 채널 통합(SSH) 기술이 융합되었다.
> 3. **융합**: 현대적인 보안 요구사항을 충족하기 위해 **SFTP (SSH File Transfer Protocol)** 및 **FTPS (FTP over SSL/TLS)**로 진화하였으며, **TFTP (Trivial File Transfer Protocol)**는 가벼운 UDP 기반 전송으로 라우터/부팅 환경 등 특수 목적으로 분화되었다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**FTP (File Transfer Protocol)**는 인터넷의 초창기인 1971년 **RFC 114**로 제안되어, 1985년 **RFC 959**로 표준화된 파일 전송 프로토콜이다. HTTP가 웹 콘텐츠 주도에 초점을 맞춘 반면, FTP는 대용량 파일의 신뢰성 있는 전송, 파일 입출력(I/O), 디렉터리 관리 등을 목적으로 설계되었다.

**💡 비유**
FTP를 마치 **'물류 센터의 배송 시스템'**에 비유할 수 있다. 고객(사용자)이 전화(제어 연결)로 주문을 넣고 배송 조회를 하면, 별도의 화물 트럭(데이터 연결)이 실제 물건(파일)을 나중에 배송하는 방식이다. 주문 내역과 화물이 다른 차편으로 이동하는 것과 유사하다.

**등장 배경**
① **기존 한계**: 초기 단순 파일 전송 메커니즘(예: 단순 메일 전송 등)은 대용량 처리와 이어올리기(Resume) 기능이 부족했다.
② **혁신적 패러다임**: **Out-of-Band(대역 외) 제어** 방식을 도입하여, 제어 명령과 데이터 전송 경로를 분리함으로써, 전송 중에도 명령을 제어할 수 있는 우아한 아키텍처를 제시했다.
③ **현재의 비즈니스 요구**: 그러나 평문 통신은 현대 보안 규정(GDPR, 개인정보보호법 등)에 위배되며, 클라우드 및 컨테이너 환경의 동적 포트 할당(Port Allocation)과 충돌하는 문제가 발생하여 Secure FTP 계열로 대체되고 있다.

> **📢 섹션 요약 비유**: 마치 복잡한 고속도로 톨게이트에서 하이패스 차선(고속 패스)을 별도로 운영하여 병목을 해결하는 것과 같습니다. 명령어와 데이터라는 두 가지 다른 트래픽 성격을 분리하여 처리 효율을 높였지만, 두 개의 차선을 만들다 보니 진입/진출(방화벽) 통제가 더 복잡해진 셈입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

FTP의 가장 큰 기술적 특징은 **제어 연결(Control Connection)**과 **데이터 연결(Data Connection)**을 분리하여 운영하는 것이다. 이를 통해 사용자는 파일 전송 중단, 재개, 디렉터리 조회 등의 명령을 데이터 흐름과 무관하게 수행할 수 있다.

**구성 요소 및 포트 (Table)**

| 구분 (Component) | 포트 (Port) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜 | 비유 |
|:---:|:---:|:---|:---|:---:|:---|
| **Control PI** | 21 (TCP) | 명령어 제어 | **NVT (Network Virtual Terminal)** 형식으로 명령어 송수신 | TCP | 전화기 |
| **Data PI** | 20 (Active) / Random (Passive) | 파일 데이터 전송 | 파일 내용, 디렉터리 리스트 등 실제 페이로드 이동 | TCP | 화물 트럭 |
| **Server DTP** | - | 데이터 전송 처리 | Passive/Active 모드에 따라 Listen 또는 Connect 수행 | TCP | 창고 관리자 |
| **Client DTP** | Random ( ephemeral) | 데이터 송수신 | 서버의 설정에 맞춰 연결 생성 | TCP | 고객 |

**ASCII 구조 다이어그램 (FTP 동작 흐름)**

```ascii
[FTP의 이중 채널 구조]

Client System                                    Server System
+------------------+                             +------------------+
| FTP Client App   |                             | FTP Server Daemon|
+------------------+                             +------------------+
        |                                                |
        | (1) TCP 3-Way Handshake (SYN, SYN-ACK, ACK)   |
        | <-------------------------------------------> |
        |   [Control Connection: Port 21]                |
        |                                                |
        | (2) USER/PASS Commands (Authentication)       |
        | ---------------------------------------------> |
        |                                                |
        | (3) PORT Command (Client Port: 5005)           | ---+
        | ---------------------------------------------> |    |
        |                                                |    |
        | (4) Server Initiated Data Connection           |    |
        | <-------------------------------------------> | <-(5) Data Transfer
        |   [Data Connection: Server 20 -> Client 5005]  |    |
        |                                                |    |
        | (6) 226 Transfer Complete (via Control)        | ---+
        | <-------------------------------------------> |
```

**[다이어그램 해설]**
위 다이어그램은 FTP의 **Active Mode** 동작 방식을 도시화한 것이다.
① 클라이언트는 서버의 21번 포트로 제어 연결을 생성하여 인증을 시도한다.
② 파일 전송 요청(PORT 명령어)을 보내며 자신의 데이터 수신 포트(예: 5005)를 알린다.
③ 서버는 제어 채널을 통해 확인을 보낸 후, **자신의 20번 포트**로부터 클라이언트의 5005번 포트로 능동적으로 접속을 시도한다.
④ 이때 데이터가 전송되며, 완료 시 제어 채널을 통해 상태 코드(226)를 반환한다.

**심층 동작 원리 (Active vs Passive)**
FTP는 데이터 연결을 누가 Initiate(시작)하느냐에 따라 모드가 나뉜다.

1.  **Active Mode (Standard Mode)**:
    -   **메커니즘**: 클라이언트가 제어 채널(21)로 `PORT` 명령을 보내면, 서버가 **20번 포트**로부터 클라이언트에게 연결한다.
    -   **문제점**: 클라이언트가 방화벽 뒤에 있거나 공유기(NAT) 내부에 있을 경우, 외부에서 들어오는 서버의 연결(Inbound Packet)을 보안 정책상 차단한다. **"Connection Refused"** 오류의 주원인이다.

2.  **Passive Mode (PASV Mode)**:
    -   **메커니즘**: 클라이언트가 `PASV` 명령을 보내면, 서버는 임의의 높은 포트(High Port)를 열고(Forking), 그 포트 번호를 클라이언트에게 알려준다. 클라이언트가 해당 포트로 **접속(Outbound)**한다.
    -   **해결**: 클라이언트가 나가는 연결(Outbound)은 방화벽에서 허용되는 경우가 많으므로 NAT/방화벽 환경에서 훨씬 안정적이다.

**핵심 파라미터 및 코드 (pseudo-log)**
```bash
# FTP ACTIVE MODE 통신 예시 (Client Log)
> PORT 192,168,1,5,195,149  (IP: 192.168.1.5, Port: 195*256+149 = 50029)
< 200 PORT command successful
> LIST
< 150 Opening ASCII mode data connection for file list
# (여기서 서버 20번 포트 -> 클라이언트 50029번 포트로 데이터 전송 시도)
< 226 Transfer complete
```

> **📢 섹션 요약 비유**: 액티브 모드는 택배 회사가 집까지 배송을 오는 것이고, 패시브 모드는 택배 회사 대형 센터에 내가 직접 방문하여 픽업하는 것과 같습니다. 요즘 같은 보안 엄격한 아파트(방화벽)에는 경비실이 배달 기사의 출입을 막으므로, 내가 직접 픽업(패시브)하러 가는 것이 훨씬 유리합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

보안의 부재와 방화벽 호환성 문제를 해결하기 위해 FTP는 다른 프로토콜 및 보안 기술과 융합되었다.

**심층 기술 비교 (Table)**

| 항목 | FTP (Active/Passive) | TFTP (Trivial File Transfer Protocol) | FTPS (FTP over SSL/TLS) | SFTP (SSH File Transfer Protocol) |
|:---|:---|:---|:---|:---|
| **기반 프로토콜** | TCP | **UDP (User Datagram Protocol)** | TCP | TCP (SSH 위) |
| **포트** | 21 (Ctrl), 20/Pasv (Data) | **69** | 21 (Ctrl), 989/990 (Implicit) | **22** |
| **보안** | None (Plaintext) | None (Plaintext) | **Encryption (SSL/TLS)** | **Encryption (AES via SSH)** |
| **속도/효율** | 중간 (Connection overhead) | 빠름 (No handshake overhead) | 느림 (Encryption overhead) | 중간 (Encryption overhead) |
| **방화벽 친화도** | 낮음 (Active), 중간 (Passive) | 높음 (UDP Helper 필요 시) | 낮음 ( 복잡한 포트 협상) | **높음 (Single Port 22)** |
| **주요 용도** | 일반 파일 전송 | 네트워크 부팅(PXE), 설정 백업 | 기존 FTP 시스템의 보안 강화 | **보안 파일 전송 표준, 관리자 접속** |

**과목 융합 관점**

1.  **보안 (Security) & 암호학 (Cryptography)**:
    -   **FTPS**는 전송 계층 보안(TLS)을 사용하여 **Control Channel**과 **Data Channel**을 모두 암호화한다. 하지만 설정 시 Explicit(명시적, 21번 후 TLS 협상)과 Implicit(암묵적, 바로 TLS 사용) 모드가 섞여 있어 방화벽 설정이 까다롭다.
    -   **SFTP**는 애플리케이션 계층 위가 아닌 SSH(Secure Shell) 프로토콜의 하위 시스템으로 동작한다. 이는 **인증(Authentication)**과 **무결성(Integrity)**을 동시에 해결한다.

2.  **시스템 아키텍처 (System Design)**:
    -   **TFTP**는 UDP 기반으로 신뢰성을 보장하지 않지만, 네트워크 부팅(Netboot) 시스템이나 임베디드 장비의 펌웨어 업데이트 등 **Bootstrapping** 단계에서 구현이 간단하고 메모리 오버헤드가 적어 필수적으로 사용된다.

**비교 시각화 (Port Traffic)**

```ascii
[Protocol Traffic Patterns]

1. Standard FTP (Multiple Ports, Firewall Nightmare)
   Client_A (Random+) <----> Server_B (21)  : Command (Who are you?)
   Client_A (Random+) <----> Server_B (20)  : Data (Here is file)
   => 방화벽: "20번 포트에서 들어오는 건 막아야겠네? 차단!"

2. SFTP (Single Port, Firewall Friendly)
   Client_C (Random+) <=====> Server_D (22) : [Encrypted Cmd] + [Encrypted Data]
   => 방화벽: "22번 포트만 뚫어놔. 관리자 접속이구나 허용."
```

> **📢 섹션 요약 비유**: FTP는 일반 우편(내용노출), FTPS는 등기 우편(봉투에 봉인), SFTP는 관용으로 운반되는 기밀 문서(철통 보안)입니다. TFTP는 포스트잇에 메모를 던져주는 것처럼 매우 가볍고 빠르지만 가끔 날아갈 수도(UDP 손실) 있는 방식입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **공공기관/금융권 데이터 수집**:
    -   **상황**: 타 금융권에서 대량의 정산 파일을 매일 밤 전송받아야 함.
    -   **의사결정**: 법적 암호화 의무가 있으므로 **FTP(S)**는 배제. 방화벽 정책 변경이 어려운 외부 네트워크이므로 **SFTP**를 선택. 포트 22번만 뚫으면 되므로 협업이 용이함.
    -   **고려사항**: SFTP는 전송 속도가 FTP보다 다소 느릴 수 있으나(암호화 오버헤드), **Chroot 설정**을 통해 사용자 접근 경로를 루트(/) 이하로 제한하여 보안을 강화해야 함.

2.  **내부 서버 간 대용량 로그 전송**:
    -   **상황**: WAS(Web Application Server)에서 대용량 로그를 분석 서버로 이동.
    -   **의사결정**: 내부망이며 속도가 생명이므로 **Passive Mode FTP** 또는 **rsync** 사용. 굳이 무거운 암호화가 필요 없으나, 내부 보안 규정에 따라 **FTPS** 적용 여부를 결정.

3.  **네트워크 장비(스위치, 라우터) 펌웨어 업그레이드**:
    -   **상황**: 공장 자동화 장비의 펌웨어 업데이트.
    -   **의사결정**: 장비의 OS가 매우 단순하거나 복잡한 클라이언트 기능이 없을 경우, 가볍고 구현이 쉬운 **TFTP** 사용.

**도입 체크리스트**

| 구분 | 항목 | 점검 포인트 |
|:---|:---|:---|
| **기술** | 모드 설정 | 내부망이면 Active 가능성, 외부/