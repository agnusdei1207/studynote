+++
title = "588. 감사 (Auditing) 및 로그 (Logging)를 통한 보안 추적"
date = "2026-03-14"
weight = 588
+++

# [감사 (Auditing) 및 로그 (Logging)를 통한 보안 추적]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 감사(Auditing)와 로깅(Logging)은 시스템의 상태 변화와 사용자 행위를 시계열(Timeline)로 기록하여 보안의 가시성(Visibility)을 확보하는 핵심 메커니즘이다.
> 2. **가치**: 사고 발생 시 포렌식(Forensics)을 위한 증거(Evidence) 제공 및 책임 추적성(Accountability) 확보를 통해 비즈니스 리스크를 최소화한다. 로그 분석을 통해 MTTD(평균 탐지 시간)를 획기적으로 단축할 수 있다.
> 3. **융합**: SIEM(Security Information and Event Management) 시스템과 연동하여 방대한 로그 데이터를 상관분석(Correlation)하고, 컴퓨팅 환경의 가상화 및 클라우드(Cloud) 환경으로 확장되는 추세이다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
**로그(Logging)**는 시스템, 네트워크, 애플리케이션에서 발생하는 이벤트나 상태 변화를 기록하는 활동이며, **감사(Auditing)**는 이러한 기록된 로그를 검토하여 보안 정책 준수 여부를 확인하고 비정상 행위를 탐지하는 관리적 절차입니다. 단순한 기록을 넘어, **부인 방지(Non-repudiation)**를 통해 사용자의 행위를 증명하고 **재난 복구(Disaster Recovery)** 시 원인 규명을 위한 기반이 됩니다.

#### 등장 배경
1.  **기존 한계**: 초기 단순 로그는 주로 시스템 디버깅이나 장애 복구에 초점을 맞추었으며, 보안 공격자가 자신의 흔적을 로그 파일에서 삭제(log tampering)하기 쉬웠습니다.
2.  **혁신적 패러다임**: 규정 준수(Compliance, 예: HIPAA, GDPR, PCI-DSS)의 강화와 함께, 로그 자체의 무결성을 보장하고 중앙 집중식으로 분석하는 **SIEM (Security Information and Event Management)** 기술이 등장했습니다.
3.  **현재 요구**: 클라우드 환경과 컨테이너(Container) 기반의 마이크로서비스 아키텍처(MSA)로 확장됨에 따라, 분산된 환경에서의 추적성을 확보하기 위한 **분산 추적(Distributed Tracing)** 기술이 요구되고 있습니다.

#### ASCII 다이어그램: 로그와 감사의 관계
아래 다이어그램은 시스템 이벤트가 로그로 변환되고, 이것이 감사 활동으로 이어지는 데이터의 흐름을 도식화한 것입니다.

```text
[Source: System/User]
      |
      | (1) Event Generation
      v
+-------------------------+
|   Logging Layer         |  <-- 자동 수집 (Data Collection)
| - App Log, Sys Log, DB  |
+-------------------------+
      |
      | (2) Storage & Aggregation
      v
+-------------------------+
|   Log Repository        |  <-- 데이터 저장 및 보호 (WORM, Encryption)
| - DB, File, S3 Bucket   |
+-------------------------+
      |
      | (3) Analysis & Review
      v
+-------------------------+
|   Auditing Process      |  <-- 정책 검증 (Policy Check)
| - Manual Review, SIEM   |
+-------------------------+
      |
      v
[Action: Alert / Report / Legal Evidence]
```
**(해설)**
1.  **이벤트 생성**: 사용자의 로그인 시도, 파일 수정, 권한 변경 등의 다양한 이벤트가 발생합니다.
2.  **로그 레이어**: 운영체제(OS)나 애플리케이션 레벨에서 이를 포맷화(Format)하여 기록합니다. 이때 중요한 것은 `Who(주체), What(행위), When(시간), Where(위치), Result(결과)`의 5W1H를 포함하는 것입니다.
3.  **저장소**: 로그는 보통 반정형화(Semi-structured) 데이터(예: JSON) 형태로 저장되며, 위변조 방지를 위해 접근 통제가 필요합니다.
4.  **감사 프로세스**: 저장된 로그를 기반으로 보안 정책 위반 여부를 판단하고, 의심스러운 패턴을 탐지하여 알림(Alert)을 생성합니다.

📢 **섹션 요약 비유**: 감사와 로깅은 건물의 **'CCTV(폐쇄회로 텔레비전) 시스템과 블랙박스'**와 같습니다. 누가 언제 출입했는지, 어디서 무슨 일이 일어났는지를 기록하여, 사고 발생 시 범인을 찾고 재발 방지를 위한 증거를 확보하는 핵심 시설입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 구성 요소 상세
감사 및 로깅 시스템을 구성하는 주요 5가지 모듈과 그 역할은 다음과 같습니다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/포맷 | 비유 |
|:---|:---|:---|:---|:---|
| **Logger (기록자)** | 이벤트 감지 및 생성 | 시스템 콜, 애플리케이션 후킹(Hooking)을 통해 변경 사항을 포착 | Syslog, API | 현장 기록자 |
| **Collector (수집기)** | 로그 집중 및 버퍼링 | 분산된 에이전트로부터 로그를 수집하고 큐(Queue)에 저장 | Logstash, Fluentd | 집하장 |
| **Parser (분석기)** | 데이터 정규화 및 파싱 | 원시 로그(Raw Log)를 필드별(예: IP, User ID)로 분리하여 구조화 | Regex, Grok | 번역가 |
| **Storage (저장소)** | 영구 보관 및 인덱싱 | 빠른 검색을 위한 인덱싱(Indexing) 처리 및 압축 저장 | Elasticsearch, DB | 창고 |
| **Alert Manager** | 알림 및 대응 | 규칙 기반(Rule-based) 또는 AI 기반 이상 탐지 시 관리자에게 통보 | SMTP, SNMP | 경비원 |

#### 심층 동작 원리 및 데이터 흐름
감사 시스템은 크게 **감사 데몬(Audit Daemon)**이 시스템 콜(System Call)을 후킹(Hooking)하는 방식과 애플리케이션 레벨에서 라이브러리를 통해 로그를 남기는 방식으로 나뉩니다.

1.  **감사 정책 로딩**: 관리자가 정의한 규칙(예: "/etc/passwd 파일 접근 시도 감시")을 커널 또는 감사 서브시스템에 로드합니다.
2.  **이벤트 인터셉트 (Intercept)**: 사용자 프로세스가 리소스에 접근하려 할 때, 감사子系统이 이를 가로챕니다.
3.  **필터링 및 기록**: 정책 위반 여부나 중요도(Level)에 따라 기록 여부를 결정하고, 로그 버퍼에 씁니다.
4.  **전송 및 무결성 확보**: 네트워크를 통해 원지 로그 서버로 전송하거나, 로컬 안전 저장소에 기록합니다. 이때 **체크섬(Checksum)**이나 **디지털 서명(Digital Signature)**을 덧붙여 위변조를 방지합니다.

#### ASCII 다이어그램: Linux Auditd 아키텍처
리눅스 환경에서 가장 널리 사용되는 `auditd` 시스템의 내부 구조를 나타낸 것입니다.

```text
[User Space: Application]
      |
      | (1) System Call (open, read, write)
      v
+-------------------------+      +--------------------------+
|   Kernel Space          |      |   Audit Subsystem        |
|                         |      +--------------------------+
|  System Call Interface  | <----| (Intercepts & Checks)    |
+-------------------------+      |                          |
      ^                      |   | Audit Rules (Netlink)    |
      |                      |   +--------------------------+
      | (2) Copy to Audited  |               |
      |     Buffer           |               | (3) Multicast Event
      |                      |               v
+-------------------------+      +--------------------------+
|   Audit Daemon (auditd)  | <----|   Audit Dispatcher       |
+-------------------------+      +--------------------------+
      |                                           |
      | (4) Write to Disk                         |
      v                                           v
[ /var/log/audit/audit.log ]            [ Dispatcher Plugins ]
                                            (Prevent, Alert)
```
**(해설)**
*   **(1) 시스템 콜**: 사용자 프로세스가 커널에 자원 요청을 합니다.
*   **(2) 감사 버퍼**: 커널 내의 감사 시스템이 이 요청을 가로채어, 설정된 규칙(Audit Rules)과 비교합니다. 감사가 필요한 경우 이벤트를 큐에 넣습니다.
*   **(3) 디스패처**: 감사 데몬(`auditd`)은 커널과 통신(Netlink 소켓 등)하여 이벤트를 읽어옵니다. 동시에 이벤트를 다른 플러그인(예: 실시간 차단 플러그인)으로 전달할 수 있습니다.
*   **(4) 로그 기록**: 최종적으로 디스크의 로그 파일에 기록되며, 관리자는 `ausearch` 등의 도구로 이를 조회합니다.

#### 핵심 알고리즘: 로그 무결성을 위한 해시 체이닝
로그 파일 자체의 변조를 방지하기 위해 **체이닝(Chaining)** 기법을 사용합니다.
```python
class SecureLogEntry:
    def __init__(self, prev_hash, data, timestamp):
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        # 이전 로그의 해시값 + 현재 내용 + 시간을 합쳐 해시 생성
        raw_content = f"{self.prev_hash}{self.data}{self.timestamp}"
        return sha256(raw_content.encode()).hexdigest()

# 예시: 만약 중간의 로그가 변조되면, 그 이후의 모든 prev_hash 연결이 끊어짐
```

📢 **섹션 요약 비유**: 감사 아키텍처는 **'도로의 과속 단속 카메라와 데이터 센터'**와 같습니다. 카메라(Logger)가 차량의 번호와 속도(이벤트)를 찍고, 이 정보가 인터넷(네트워크)을 통해 경찰서 서버(SIEM)로 전달되어, 벌점 부과(대응)를 위한 증거로 확보됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: 로깅 vs 모니터링 vs 감사
혼동하기 쉬운 개념들을 정량적/정성적으로 비교 분석합니다.

| 구분 | 로깅 (Logging) | 모니터링 (Monitoring) | 감사 (Auditing) |
|:---|:---|:---|:---|
| **목적** | 기록 및 사후 분석 | 실시간 상태 확인 및 성능 유지 | 보안 검증 및 규정 준수 (Compliance) |
| **시점** | 비동기적 (Asynchronous) | 동기적/실시간 (Real-time) | 정기적 또는 사후 (Post-mortem) |
| **데이터 형태** | 텍스트 로그 (Unstructured/Semi-structured) | 메트릭 (Metrics: 숫자) 및 상태 | 증적(Evidence) 중심의 구조화된 기록 |
| **보관 주기** | 장기 (수년) | 단기 (롤링 업데이트) | 법적 보관 의무 기간 준수 |
| **주요 도구** | ELK Stack, Splunk | Prometheus, Datadog | Auditd, GRC Tools |
| **핵심 지표** | 에러 로그 수, 로그 크기 | CPU/MEM 사용률, 응답 시간(Latency) | 정책 위반 횟수, 변경 내역 |

#### 과목 융합 관점
1.  **운영체제(OS)와의 융합**:
    *   **프로세스 추적**: 로그는 단순히 "누가" 뿐만 아니라 "어떤 프로세스(PID)"가 호출했는지 기록해야 합니다. 리눅스의 `auditd`는 PID뿐만 아니라 부모 PID(PPID)를 추적하여 트리 기반의 공격 경로를 파악할 수 있게 합니다.
    *   **커널 레벨 vs 유저레벨**: 유저레벨 로그는 해커에 의해 우회될 수 있으므로, 신뢰성을 위해 커널 레벨 감사가 필수적입니다.
2.  **네트워크와의 융합**:
    *   **NAT( Network Address Translation) 로그의 한계**: 방화벽 뒤의 사설 IP를 기록하는 것만으로는 실제 공격자를 특정하기 어렵습니다. 따라서 방화벽 로그와 내부 DHCP 로그, 그리고 웹 프록시 로그를 상관분석(Correlation)하여 실제 사용자를 식별해야 합니다.

#### ASCII 다이어그램: 상관분석(Correlation) 예시
단일 로그로는 드러나지 않는 공격 시나리오를 다각도의 로그 조합으로 발견하는 과정입니다.

```text
Time 10:00:00
[Firewall Log]   : DROP Packet from IP 1.2.3.4 (External)
[Web Server Log] : 200 OK GET /login (User: admin)
-------------------------------------------------------
=> 분석결과: 외부 차단되었으나 내부에서 정상 로그인? (이상 징후 없음)

Time 10:00:05
[Firewall Log]   : DROP Packet from IP 1.2.3.4 (External)
[Web Server Log] : 401 Unauthorized (User: admin)
[System Log]     : User 'admin' failed password 3 times
-------------------------------------------------------
=> 분석결과: 로그인 실패.

Time 10:00:10
[Firewall Log]   : ACCEPT Packet from IP 5.6.7.8 (Internal)
[Web Server Log] : 200 OK GET /admin/config (User: admin)
[Integrity Log]  : CRITICAL /etc/passwd modified by 'admin'
-------------------------------------------------------
=> **[SIEM CORRELATION ALERT]**
   1. 내부 IP(5.6.7.8)에서 관리자 설정 변경
   2. 1초 전 외부(1.2.3.4)에서 침입 시도(브루트포스)
   => 결론: 관리자 계정이 탈취되었거나 내부자 위협(Insider Threat)일 가능성
```
**(해설)**
*   개별 로그만 보면 "방화벽 차단", "패스워드 실패", "설정 변경" 등 독립적인 사건처럼 보입니다.
*   **SIEM 상관분석 엔진**은 이를 시간 순서와 소스(Source)를 기반으로 연결하여, "외부 공격자가 패스워드를 무차별 대입하다 성공한 후