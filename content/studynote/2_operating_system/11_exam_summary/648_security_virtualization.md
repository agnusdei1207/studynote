+++
title = "648. 운영체제 핵심 요약 - 보안 및 가상화"
date = "2024-05-23"
weight = 648
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "보안", "Security", "Virtualization", "Hypervisor", "Container", "가상화"]
+++

> **[Insight]**
> 운영체제 보안은 인가되지 않은 접근으로부터 시스템 자원과 데이터를 보호하고 서비스의 가용성을 유지하는 신뢰 컴퓨팅의 기초이다.
> 현대 OS는 다계층 방어 체계를 구축하며, 특히 하드웨어 자원을 논리적으로 격리하는 가상화(Virtualization) 기술은 보안성과 자원 효율성을 동시에 극대화하는 핵심 트렌드로 자리 잡았다.
> 하이퍼바이저(Hypervisor) 기반의 전가상화/반가상화를 넘어, 최근에는 경량화된 격리를 제공하는 컨테이너(Container) 기술이 클라우드 네이티브 환경의 표준이 되고 있다.

+++

### Ⅰ. 운영체제 보안 모델과 메커니즘

1. 보안의 3요소 (CIA Triad)
   - **기밀성(Confidentiality)**: 인가된 사용자만 정보 접근.
   - **무결성(Integrity)**: 정보의 불법적인 변경 방지.
   - **가용성(Availability)**: 필요한 시점에 서비스 보장.
2. 접근 제어(Access Control) 모델
   - **DAC (Discretionary Access Control)**: 소유자가 권한 부여.
   - **MAC (Mandatory Access Control)**: 시스템 정책에 따른 강제적 권한 관리 (SELinux 등).
   - **RBAC (Role-Based Access Control)**: 사용자 역할에 따른 권한 부여.
3. 보호 영역(Protection Ring)
   - 커널 모드(Ring 0)부터 사용자 모드(Ring 3)까지 계층별로 하드웨어 접근 권한 제한.

📢 섹션 요약 비유: 집의 '대문 열쇠'는 DAC, '금고 비밀번호'는 MAC, '가족 역할'에 따른 심부름 권한은 RBAC과 같습니다.

+++

### Ⅱ. 시스템 가상화(System Virtualization) 기술

1. 하이퍼바이저(Hypervisor - VMM)
   - 호스트 하드웨어 위에 여러 개의 가상 머신(VM)을 실행하기 위한 관리 계층.
2. 가상화 방식 분류
   - **전가상화(Full Virtualization)**: 하드웨어를 완전 에뮬레이션. 게스트 OS 수정 불필요 (VMware 등).
   - **반가상화(Para-virtualization)**: 게스트 OS가 하이퍼바이저와 통신하도록 수정. 성능 우수 (Xen 등).

```text
[ Virtualization Architecture ]

    [ App ] [ App ]        [ App ] [ App ]
    [ Guest OS 1 ]        [ Guest OS 2 ]
    +----------------------------------+
    |      Hypervisor (Type-1/2)       |
    +----------------------------------+
    |        Physical Hardware         |
    +----------------------------------+
```

📢 섹션 요약 비유: 한 대의 컴퓨터 안에 여러 개의 가상 '컴퓨터 집'을 짓고, 하이퍼바이저라는 관리인이 각 집의 전기와 물(자원)을 배분해주는 것과 같습니다.

+++

### Ⅲ. 컨테이너(Container) 기술과 도커(Docker)

1. 컨테이너 가상화의 특징
   - 호스트 OS 커널을 공유하며 프로세스 수준의 격리를 제공 (OS-level Virtualization).
   - VM 대비 가볍고(Lightweight), 부팅이 빠르며 이식성(Portability)이 뛰어남.
2. 핵심 기술
   - **Namespaces**: 프로세스 간 자원 격리 (PID, Network 등).
   - **Cgroups (Control Groups)**: CPU, 메모리 등 자원 사용량 제한.
3. 도커(Docker)의 의의
   - 애플리케이션과 실행 환경을 이미지화하여 'Build Once, Run Anywhere' 실현.

📢 섹션 요약 비유: 아예 집을 새로 짓는 VM과 달리, 한 지붕 아래에서 '자기 방'만 확실히 격리하여 가볍게 사용하는 원룸 시스템과 같습니다.

+++

### Ⅳ. 악성 코드와 시스템 취약점 방어

1. 악성 코드 유형
   - 바이러스(Virus), 웜(Worm), 트로이 목마(Trojan), 랜섬웨어(Ransomware) 등.
2. 취약점 공격 및 방어
   - **Buffer Overflow**: 입력값 검증 및 ASLR(Address Space Layout Randomization) 적용.
   - **Side-channel Attack**: CPU 아키텍처 취약점 (Meltdown, Spectre) 대응 패치.
3. 보안 커널(Security Kernel)과 참조 모니터(Reference Monitor)
   - 모든 접근 시도를 중재하고 감시하는 핵심 보안 메커니즘.

📢 섹션 요약 비유: 도둑(악성 코드)이 들지 않게 문단속을 철저히 하고, 도둑이 들어와도 길을 찾지 못하게 방 번호를 매번 바꾸는(ASLR) 지능형 보안 시스템입니다.

+++

### Ⅴ. 신뢰 컴퓨팅과 최신 트렌드

1. 클라우드 보안(Cloud Security)
   - 다중 사용자 환경(Multi-tenancy)에서의 격리와 데이터 암호화.
2. 제로 트러스트(Zero Trust)
   - "아무도 믿지 마라"는 원칙하에 지속적인 인증과 최소 권한 부여.
3. TEE(Trusted Execution Environment)
   - 메인 프로세서 내의 보안 영역(Intel SGX 등)에서 민감한 연산 수행.

📢 섹션 요약 비유: 신분증이 있어도 건물 안 모든 방에 들어갈 때마다 다시 검사받고, 가장 중요한 보물은 '비밀의 방(TEE)'에 따로 보관하는 완벽주의 보안입니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 관리(OS Management)
- **자식 노드**: 클라우드 컴퓨팅(Cloud Computing), 사이버 보안(Cyber Security)
- **연관 키워드**: Access Control, Hypervisor, Container, Docker, SELinux, TEE, Zero Trust

### 👶 어린아이에게 설명하기
"얘야, 우리 컴퓨터를 나쁜 악당들로부터 지키는 '보안관' 대장님이 계셔. 대장님은 누가 우리 장난감을 만지는지 항상 감시하고, 중요한 일은 아무도 모르는 '비밀 기지(가상화)'에서 처리한단다. 특히 요즘은 장난감 상자를 여러 개로 나눠서 한 상자가 고장 나도 다른 건 멀쩡하게 만드는 '마법 상자(컨테이너)' 기술도 많이 쓴단다!"