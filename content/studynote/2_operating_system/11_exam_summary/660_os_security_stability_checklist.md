+++
weight = 660
title = "660. 운영체제 보안 및 안정성 확보를 위한 체크리스트"
date = "2024-05-23"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Security", "Stability", "Access Control", "Kernel Protection", "ASLR"]
+++

> **[Insight]**
> 운영체제의 보안과 안정성은 시스템의 무결성(Integrity), 가용성(Availability), 기밀성(Confidentiality)을 보장하는 최후의 보루이다.
> 하드웨어 수준의 모드 보호부터 소프트웨어 수준의 접근 제어, 메모리 오염 방지 기술이 겹겹이 쌓인 다층 방어(Defense in Depth) 구조를 형성한다.
> 현대 OS는 날로 지능화되는 공격으로부터 시스템을 보호하기 위해 가상화(Virtualization), 샌드박싱(Sandboxing), 난수화(ASLR) 등의 첨단 기법을 적극 활용한다.

---

### Ⅰ. 운영체제 보안의 3대 핵심 목표 (CIA Triad)

1. Confidentiality (기밀성)
   - 허가되지 않은 사용자가 데이터를 읽지 못하도록 제한한다 (암호화, 접근 권한).
2. Integrity (무결성)
   - 허가되지 않은 사용자가 데이터를 수정하지 못하도록 보장한다 (디지털 서명, 해시).
3. Availability (가용성)
   - 정당한 사용자가 필요할 때 언제든 시스템을 사용할 수 있도록 보장한다 (DoS 방어, 이중화).

📢 섹션 요약 비유: 운영체제 보안은 '보물 창고(데이터)'를 지키기 위해 '자물쇠(기밀성)', 'CCTV(무결성)', '정상 영업(가용성)'을 동시에 유지하는 보안 업체와 같습니다.

---

### Ⅱ. 하드웨어 및 커널 수준 보안 체크리스트

1. 메모리 보호 기술 다이어그램
   - 버퍼 오버플로우와 같은 메모리 공격을 방어하는 메커니즘이다.

```text
[ Memory Protection Mechanisms ]

 +-----------------------+   [ Stack Canary ]
 |      Stack            |   <- Check for corruption
 +-----------------------+
 |  [ Random Padding ]   |   <- ASLR (Address Space Layout Randomization)
 +-----------------------+
 |      Heap             |
 +-----------------------+
 |      Data / Code      |   <- NX Bit / DEP (Data Execution Prevention)
 +-----------------------+
```

2. 체크리스트
   - [ ] NX/DEP (Data Execution Prevention): 데이터 영역의 코드가 실행되는 것을 차단하는가?
   - [ ] ASLR (Address Space Layout Randomization): 주소 공간을 무작위 배치하여 공격 지점 예측을 어렵게 하는가?
   - [ ] Kernel Patch Protection: 커널 메모리의 무단 수정을 실시간으로 감시하는가?

📢 섹션 요약 비유: 도둑이 집 구조를 알지 못하게 매일 가구 배치를 바꾸고(ASLR), 거실(Data Area)에서는 춤(Code Execution)을 못 추게 금지하는 규칙과 같습니다.

---

### Ⅲ. 사용자 인증 및 접근 제어 (Access Control)

1. 인증(Authentication)
   - ID/PW, 생체 인식, 다요소 인증(MFA) 등을 통해 정당한 사용자인지 확인한다.
2. 접근 제어 모델
   - **DAC (Discretionary)**: 자원 소유자가 권한을 부여 (사용자 중심).
   - **MAC (Mandatory)**: 시스템 정책에 의해 엄격히 제한 (관리자 중심, 보안 중시).
   - **RBAC (Role-Based)**: 역할별로 권한을 묶어서 부여 (효율적 관리).
3. 최소 권한 원칙 (Principle of Least Privilege)
   - 작업 수행에 꼭 필요한 최소한의 권한만 부여하여 피해 확산을 방지한다.

📢 섹션 요약 비유: 아르바이트생에게는 매장 열쇠만 주고, 금고 열쇠는 주지 않는 '역할 분담' 보안 시스템입니다.

---

### Ⅳ. 악성코드 방어 및 시스템 안정성 확보

1. 샌드박싱 (Sandboxing)
   - 응용 프로그램을 격리된 환경에서 실행하여 시스템 전체에 미치는 영향을 차단한다.
2. 루트킷(Rootkit) 및 안티바이러스
   - 커널 수준의 침입을 탐지하고 무단 변조된 파일을 복구한다.
3. 안정성을 위한 결함 허용 (Fault Tolerance)
   - 시스템의 일부 부품이 고장 나도 전체가 멈추지 않도록 예비 자원을 활용한다.

📢 섹션 요약 비유: 위험할 수 있는 실험은 특수 유리 상자(Sandbox) 안에서 진행하여 실험실 전체가 오염되지 않게 막는 것과 같습니다.

---

### Ⅴ. 보안 감사 및 무결성 검증

1. 로깅 및 감사 (Audit Trail)
   - 모든 중요한 활동을 로그로 남겨 사후에 추적 가능하게 한다.
2. Secure Boot (안전 부팅)
   - 부팅 과정에서 디지털 서명된 신뢰할 수 있는 커널만 로드되도록 보장한다.
3. 주기적인 패치 및 취약점 관리
   - 제로 데이(Zero-day) 공격에 대비하여 최신 보안 업데이트를 유지한다.

📢 섹션 요약 비유: 출입 명부(Audit Log)를 꼼꼼히 적고, 아침에 문을 열 때 검증된 직원만 출근하게 하는 출입 보안과 같습니다.

---

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 컴퓨터 보안(Computer Security)
- **자식 노드**: CIA, ASLR, DEP, DAC/MAC, Sandboxing, Secure Boot
- **연관 키워드**: Encryption, Authentication, Buffer Overflow, Rootkit, Least Privilege

### 👶 어린아이에게 설명하기
"스마트폰이나 컴퓨터는 아주 소중한 우리들의 사진과 편지를 보관하는 금고와 같단다. 나쁜 사람들이 몰래 훔쳐보거나 망가뜨리지 못하게 대장님이 튼튼한 문(Password)을 만들고, 혹시 나쁜 벌레(Virus)가 들어오면 바로 쫓아내고, 중요한 물건들은 비밀 장소에 숨겨두는 거야. 대장님이 밤낮으로 보초를 서기 때문에 우리가 안심하고 사용할 수 있는 거란다!"