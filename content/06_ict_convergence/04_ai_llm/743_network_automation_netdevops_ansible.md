---
title: "Network Automation NetDevOps Ansible"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 743
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NetDevOps는 네트워크 운영에 Git 기반 소스 관리, CI/CD 파이프라인, 코드형 인프라(IaC)를 적용한 문화적·기술적 프레임워크이며, Ansible은 이 프레임워크의 사실상 표준 실행 엔진으로서 Agentless(SSH/NETCONF/RESTCONF) 아키텍처, Push 기반 배포, 선언적 YAML 플레이북, Idempotency 보장이라는 4대 특성을 통해 멀티벤더 멀티 도메인(L2/L3/WAN/SDN/Cloud) 자동화를 단일 런타임으로 통합한다.
> 2. **가치**: Cisco 기준 수동 CLI 대비 구성 배포 시간을 평균 75~90% 단축하고(MOP 1건 4시간 -> 15분), 휴먼 에러율을 60~80% 감소시키며, AWX/Ansible Tower를 통한 RBAC·감사 로그·승인 워크플로우로 ITIL Change Management 자동화를 실현한다. 또한 NAPALM/PyATS/Genie 추상화 계층을 통해 벤더 종속성을 평균 40% 이상 낮춘다.
> 3. **판단 포인트**: Push vs Pull 아모(Ansible Push vs Salt Pull), State vs Intent(NAPALM Compliance vs NSO Service Model), Stateless vs Stateful(Ansible 단독 vs Itential/Nautobot/Infoblox 통합), 그리고 Connection 플러그인 선택(CLI+TextFSM vs NETCONF YANG vs RESTCONF YANG vs gNMI/JSON-IETF vs HTTPAPI)에서 트레이드오프가 발생하며, 대규모 환경에서는 AWX/Controller의 조직 단위 분할, Execution Environment 컨테이너화, 그리고 Ansible 개발 모드(`ANSIBLE_KEEP_REMOTE_FILES=1`, `--check`, `--diff`) 전략 수립이 핵심 의사결정 사항이다.

---

## Ⅰ. 개요 및 필요성

전통적인 네트워크 운영은 CLI 기반의 1:1 수동 작업, 각 엔지니어의 암묵지(Tacit Knowledge)에 의존한 절차적 운영, 그리고 "변경 금지의 문화"로 특징지어진다. 시스코 IOS-XR, 주니퍼 Junos, 아리스타 EOS, 화웨이 VRP 등 이기종 NOS(Network Operating System)가 혼재하는 환경에서, VLAN 1,000개 추가, BGP 정책 500라인 적용, ACL 10,000건 배포 같은 단순·반복 작업이 엔지니어의 야간·주말 작업으로 이어지며, 그 결과 평균 65%가 운영(Operation)에, 35%만이 혁신에 투입되는 역피라미드형 인력 구조가 고착화되었다.

NetDevOps는 이러한 문제를 해결하기 위해 **"네트워크는 결국 소프트웨어 자산"** 이라는 대전제 아래, **PLAN -> CODE -> BUILD -> TEST -> DEPLOY -> OPERATE -> MONITOR**의 7단계 DevOps 파이프라인을 네트워크 도메인에 적용한다. 여기서 Ansible은 CODE/BUILD/DEPLOY 단계를 주도하며, Git은 소스 관리, AWX/Ansible Automation Platform은 오케스트레이션, Batfish/PyATS는 TEST, NetBox/Nautobot는 Source of Truth(SoT), Prometheus/Grafana는 MONITOR 역할을 수행한다.

```text
+----------------------------------------------------------------------+
|                   Legacy Network Ops vs NetDevOps                    |
+----------------------------------------------------------------------+
|                                                                      |
|  [Legacy: 1990s~2010s]              [NetDevOps: 2017~현재]            |
|                                                                      |
|  Operator --► SSH/Telnet            Git Push --► CI Pipeline          |
|     |             |                       |              |           |
|     v             v                       v              v           |
|  switch# conf t  Per-Device         Ansible     --►  AWX/Jenkins      |
|  switch(config)#  Manual            Playbook         |                |
|  switch(config-if)#                 (YAML)           v                |
|       |                                |         Multi-Vendor         |
|       v                                v         Network Devices      |
|  No Audit Trail                    Full Audit + Idempotent            |
|  No Version Ctrl                   Git Tagged + Reviewed             |
|  SPOF: 1 Engineer                  SPOF 제거: 1 Playbook             |
|  Change Window: 7 days             Change Window: 15 min             |
|                                                                      |
|  ▣ Problem: Scale^ Speedv Error^  ▣ Solution: Code^ Speed^ Errorv    |
+----------------------------------------------------------------------+
```

**구체적 필요성 (정량 근거):**
- **속도**: AnsibleFest 2022 발표에서 대형 통신사는 신규 DC 팜 1,000대 스위치 초기 구성을 6주 -> 3일로 단축(95% 감소)
- **품질**: Gartner 2023 보고서: 수동 구성 오류가 전체 네트워크 장애의 약 68% 원인, 자동화 적용 후 1년 내 MTTR 평균 42% 감소
- **규정 준수**: 금융권 전자금융감독규정 제15조의2(변경관리) 충족을 위해 모든 변경의 Git 커밋 이력 + Ansible 실행 로그가 감사 증거(Audit Evidence)로 활용
- **인력**: Uptime Institute 2023 설문 - 70%의 네트워크 엔지니어가 "자동화 스킬 부족"을 커리어 장벽으로 응답 -> Python+YAML+Jinja2 역량이 신규 필수 스킬로 부상

- **📢 섹션 요약 비유**: 기존 네트워크 운영이 마치 **수작업 목공(指物) 장인이 망치와 끌로 가구 하나씩 깎아 만드는 방식**이라면, NetDevOps는 **CNC 자동 선반에 G-code(설계도)만 입력하면 동일 품질의 가구를 24시간 대량 생산하는 공장**과 같다. 핵심은 "장인의 손맛"을 "버전 관리된 코드"로 대체하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Ansible의 핵심 아키텍처는 **Control Node(제어 노드)** 와 **Managed Node(관리 대상 노드)** 로 이원화되며, Managed Node에는 별도 Agent를 설치하지 않는 **Agentless** 방식이 원칙이다. 네트워크 장비 특성상 메모리/연산 자원이 제한적이고 IOS/Junos는 Python 3.11+ 런타임 자체를 지원하지 않는 경우가 대부분이므로, 모든 실행 로직은 Control Node(주로 Linux 8/9 + Python 3.10+)에 집중된다.

```text
+--------------------------------------------------------------------+
|              Ansible Network Automation Architecture              |
+--------------------------------------------------------------------+

  +------------------- Control Node (Linux/RHEL 8+) ---------------+
  |                                                                 |
  |  +---------+  +----------+  +----------+  +------------------+ |
  |  |Inventory|  |Playbooks |  |  Roles   |  |  Collections     | |
  |  |  (YAML) |  |  (.yml)  |  | (tasks/  |  | (cisco.ios,      | |
  |  | INI/    |  |          |  |handlers/|  |  junipernetworks | |
  |  | YAML    |  |          |  |templates|  |  .junos, arista  | |
  |  +----+----+  +----+-----+  |  vars/  |  |  .eos, community | |
  |       |             |        | defaults|  |  .general)       | |
  |       |             |         +----+----+  +------+-----------+ |
  |       v             v              v              v             |
  |  +------------------------------------------------------+      |
  |  |           ansible-core (2.16/2.17) Engine            |      |
  |  |  +---------+ +----------+ +----------+ +----------+  |      |
  |  |  |Strategy | |Connection| | Modules  | | Filters/ |  |      |
  |  |  | Plugins | |  Plugins | |  (2400+) | |  Jinja2  |  |      |
  |  |  +---------+ +----+-----+ +----------+ +----------+  |      |
  |  +------------------++----------------------------------+      |
  |                     |   Push (Default) / Pull (ansible-pull)       |
  +---------------------+-------------------------------------------+
                        |
        +---------------+---------------+---------------+
        v               v               v               v
  +----------+    +----------+    +----------+    +----------+
  | Cisco    |    | Juniper  |    | Arista   |    | Nokia    |
  | IOS-XE   |    | Junos    |    | EOS      |    | SR OS    |
  | (NETCONF|    | (NETCONF |    | (eAPI/   |    | (MD-CLI/ |
  |  /RESTC.|    |  +YANG)  |    | RESTCONF)|    |  gNMI)   |
  |  /SSH)   |    |          |    |          |    |          |
  +----------+    +----------+    +----------+    +----------+
        |               |               |               |
        +---------------+---------------+---------------+
                  Network of Multi-Vendor Devices
```

### 5단계 실행 흐름 (Execution Flow)

1. **Inventory 로드**: `inventory.yml` 또는 `inventory/hosts` 파일에서 대상 호스트 그룹(예: `cisco_ios`, `juniper_junos`)과 변수(host, port, ansible_connection, ansible_network_os) 해석
2. **Playbook 파싱**: YAML 형식의 Playbook을 Python AST로 변환, Host Pattern 매칭
3. **Task별 Module 호출**: `cisco.ios.ios_vlans`, `junipernetworks.junos.junos_interfaces` 등 Collection 모듈 호출
4. **Connection Plugin을 통한 장비 통신**:
   - `network_cli` (SSH+CLI, TextFSM/regex 파싱) - 90% 레거시 호환
   - `netconf` (RFC 6241, YANG 모델, XML 트리) - 표준화/트랜잭션
   - `httpapi` (RESTCONF RFC 8040, JSON/XML) - SDN 컨트롤러 친화
   - `grpc` (gNMI, OpenConfig YANG) - Streaming Telemetry 시대
5. **Result 콜백**: `json`, `yaml`, `junit` 등의 Callback 플러그인을 통해 AWX/Jenkins로 결과 전송, JSON 결과 내 `changed: true/false` 필드로 Idempotency 확인

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Node** | Ansible 엔진 실행, 인증키 보관, Playbook 해석 | Python 3.10+, ansible-core 2.16+, SSH Key(vault)/PKI/Cert 인증, FQCN(`cisco.ios.ios_vlans`) 기반 Collection 로딩, 병렬 처리를 위한 `forks` 기본 5 -> 25+ 권장 |
| **Inventory** | 대상 장비 목록 및 그룹화 변수 정의 | YAML 1.2 형식, `group_vars/`, `host_vars/` 디렉토리, 동적 인벤토리 플러그인(`plugin: netbox`, `plugin: aws_ec2`, `plugin: foreman`)로 SoT/CMDB 연동 |
| **Playbook** | 실행 정책(What, Where, How) 선언 | YAML 1.2, `hosts:`, `gather_facts: no`(네트워크는 facts 비권장), `tasks:`, `handlers:`, `serial: 1`(rolling update), `order: sorted`(의존성), `max_fail_percentage: 25` |
| **Module** | 실제 명령 실행 단위 | Ansible 2.10부터 FQCN 강제. 네트워크용 1,200+ 모듈, Network Resource Module은 `resource_definition:` 또는 `config:`/`state:` 키 표준, `state: merged/replaced/overridden/deleted/rendered/parsed` 6상태 |
| **Connection Plugin** | 장비와의 통신 채널 추상화 | `network_cli`(기본), `netconf`(RFC 6241, NETCONF v1.1 base:1.1), `httpapi`(RESTCONF, Cisco/Huawei/Nokia), `grpc`(gNMI), `local` |
| **Role / Collection** | 재사용 가능한 코드 패키지 | `ansible-galaxy collection install cisco.ios -p ./collections`, `roles/` 디렉토리 표준(`tasks/main.yml`, `handlers/main.yml`, `templates/`, `vars/main.yml`, `defaults/main.yml`, `meta/main.yml`) |
| **Jinja2 Template** | 장비별/환경별 동적 구성 생성 | `{{ hostname }}`, `{% for vlan in vlans %}`, 필터(`ipaddr`, `network_in_network`, `ipmath`, `cisco.ios.facts` 커스텀 필터) |
| **Ansible Vault / EDA** | 비밀 관리 및 이벤트 기반 자동화 | `ansible-vault encrypt_string` (AES-256-GCM), `EVENT-DRIVEN ANSIBLE` (Kafka/SNS/Webhook 트리거), Controller 2.4+ |
| **AWX / Ansible Automation Platform** | 엔터프라이즈 오케스트레이션 | REST API(컨트롤 + 노드 분리), RBAC, Workflow(여러 Job Template 체이닝), Credential Types, Survey, Job Slice(대규모 병렬), Execution Environment(컨테이너 기반) |
| **NAPALM / PyATS / Genie** | 멀티벤더 추상화 및 검증 | NAPALM: `get_facts()`, `get_interfaces()`, `get_config()`, `compliance_report()` - Cisco/Juniper/Arista/Nokia/FRR 통합. PyATS/Genie: `genie parse show version` -> JSON 트리, 테스트 자동화 |

### Idempotency(멱등성)의 동작 원리

Ansible의 가장 중요한 설계 철학. 동일 Playbook을 100회 실행해도 시스템 상태가 1회 실행 후와 동일하게 유지됨. **Network Resource Module**은 내부적으로 `get_config`(현재 상태) -> `desired_config`(사용자 정의) -> Diff 계산 -> 변경 필요 시에만 NETCONF `<edit-config>` 또는 CLI `apply` 실행 -> 변경 없으면 `ok`, 변경 시 `changed`로 보고. 이는 **Configuration Drift Detection** 자동화의 핵심으로, 매일 새벽 3시 `cron + ansible-playbook --check --diff` 실행으로 비인가 변경 탐지.

### Connection 플러그인별 트레이드오프

| Connection | 데이터 모델 | 트랜잭션 | 성능 | 트러블슈팅 난이도 | 적합 사례 |
|---|---|---|---|---|---|
| `network_cli` + TextFSM/regex | 비정형 텍스트 | ❌ 부분 적용 위험 | 빠름 (1초/명령) | 상 (정규식 깨짐) | 레거시 IOS, 첫 자동화 도입 |
| `netconf` + YANG | XML 트리 | ✅ Candidate/Lock | 중간 (200~500ms/RPC) | 중 (YANG 모델 이해 필수) | 신규 도입 IOS-XR, Junos, 표준화 |
| `httpapi` + RESTCONF | JSON/XML | ⚠️ PATCH 일부만 | 중간 | 중 | IOS-XE 16.12+, SDN 컨트롤러 |
| `grpc` + gNMI/JSON-IETF | protobuf/JSON | ✅ Set/Replace/Delete | 매우 빠름 (스트리밍) | 상 (protobuf 디버깅) | Streaming Telemetry, OpenConfig |
| `httpapi` + vendor SDK (eAPI/ConfD) | JSON | △ | 빠름 | 하 | Arista EOS, Nokia SR OS |

- **📢 섹션 요약 비유**: Ansible의 구조는 **심부름 센터 콜센터**와 같다. 손님(엔지니어)이 주문서(Playbook)를 작성해 전화하면, 콜센터 직원(Control Node)이 배