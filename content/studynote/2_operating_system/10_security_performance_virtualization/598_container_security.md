+++
weight = 598
title = "598. 컨테이너 보안 (Container Security) - 격리 및 리소스 제한"
+++

### 💡 핵심 인사이트 (Insight)
1. **공유 커널의 양면성**: 컨테이너는 호스트 OS의 커널을 공유하여 가볍고 빠르지만, 커널이 직접적인 공격 표면이 되므로 가상 머신(VM)보다 보안 경계가 상대적으로 얇습니다.
2. **리눅스 보안 기술의 집약체**: 컨테이너 보안은 네임스페이스(Namespaces), Cgroups, Seccomp, Capabilities 등 리눅스 커널의 여러 보안 기능을 조합하여 강력한 격리 환경을 구축합니다.
3. **이미지 및 런타임 보안의 결합**: 안전한 베이스 이미지 사용(Build-time)과 실행 중인 컨테이너의 행위 감시(Run-time)가 동시에 이루어져야 전체적인 컨테이너 보안이 완성됩니다.

---

## Ⅰ. 컨테이너 격리의 기초 기술
### 1. 네임스페이스 (Namespaces)
프로세스별로 시스템 자원을 독립적으로 볼 수 있게 하여 논리적 격리를 수행합니다. (PID, Network, Mount, UTS, IPC 등)

### 2. Cgroups (Control Groups)
특정 컨테이너가 호스트의 모든 CPU나 메모리를 점유하여 다른 컨테이너에 영향을 주는 자원 고갈(DoS) 공격을 방지합니다.

📢 **섹션 요약 비유**: 컨테이너 격리는 '한 지붕 아래 살면서 서로 다른 방을 쓰고, 방마다 정해진 전력(자원)만 사용하게 하는 것'과 같습니다.

---

## Ⅱ. 컨테이너 보안 아키텍처 (ASCII Diagram)
### 1. 계층별 보안 요소
```text
[Container Application]
       |
       | (1) Read-only Root Filesystem
       V
[Container Runtime (Docker/containerd)]
       |
       | (2) Seccomp: Syscall Filtering
       | (3) AppArmor/SELinux: MAC Policy
       | (4) Capabilities: Drop Unnecessary Privileges
       V
[Linux Kernel (Shared)]
       |
       | (5) Namespaces: Resource Isolation
       | (6) Cgroups: Resource Limitation
       V
[Physical Hardware]
```

### 2. Capabilities 제어
루트(Root) 권한을 세분화하여, 컨테이너에게 꼭 필요한 기능(예: 네트워크 바인딩)만 부여하고 위험한 기능(예: 커널 모듈 로드)은 제거합니다.

📢 **섹션 요약 비유**: 컨테이너 보안 아키텍처는 '여러 겹의 성벽(보안 기술)으로 둘러싸인 요새'와 같습니다. 한 겹이 뚫려도 다음 성벽이 공격을 막아줍니다.

---

## Ⅲ. 컨테이너 이미지 보안 (Image Security)
### 1. 취약점 스캔
이미지 빌드 시 포함된 라이브러리나 패키지에 알려진 취약점(CVE)이 있는지 자동으로 검사합니다.

### 2. 최소 이미지 (Minimal Base Image)
`Alpine Linux`나 `Distroless` 이미지처럼 꼭 필요한 실행 파일만 남기고 쉘(Shell)조차 제거하여 공격자가 활용할 도구를 원천 차단합니다.

### 3. 이미지 서명 (Image Signing)
`Docker Content Trust` 등을 통해 신뢰할 수 있는 레지스트리에서 서명된 이미지만 내려받아 실행하도록 보장합니다.

📢 **섹션 요약 비유**: 이미지 보안은 '밀봉된 음식을 먹기 전 상했는지 확인(스캔)하고, 믿을 수 있는 제조사(서명) 제품만 사는 것'과 같습니다.

---

## Ⅳ. 런타임 보안 (Runtime Security)
### 1. 비특권 컨테이너 (Rootless Container)
컨테이너 내부의 루트 사용자가 호스트의 실제 루트와 매핑되지 않도록 사용자 네임스페이스(User Namespace)를 사용하여 탈취 시 피해를 줄입니다.

### 2. 읽기 전용 파일 시스템
컨테이너의 루트 파일 시스템을 읽기 전용(`--read-only`)으로 설정하여, 공격자가 악성 파일을 생성하거나 기존 시스템 파일을 변조하는 것을 방지합니다.

### 3. 네트워크 정책 (Network Policy)
컨테이너 간의 통신을 꼭 필요한 포트와 IP로 제한하여, 하나가 침해되었을 때 옆 컨테이너로 공격이 확산(Lateral Movement)되는 것을 막습니다.

📢 **섹션 요약 비유**: 런타임 보안은 '방 안에 가둔 손님이 갑자기 가구를 바꾸거나(파일 변조) 다른 방 손님과 대화하는 것을 감시하는 경비원'과 같습니다.

---

## Ⅴ. 컨테이너 보안의 미래: 하드웨어 가상화 결합
### 1. Kata Containers
컨테이너의 가벼움과 VM의 강력한 격리 성능을 결합하기 위해, 각 컨테이너를 가벼운 가상 머신(MicroVM) 내부에서 실행하는 기술입니다.

### 2. gVisor
구글에서 개발한 기술로, 프로세스와 커널 사이에 유저 모드 커널(Sentry)을 두어 시스템 콜을 가로채고 필터링함으로써 보안성을 극대화합니다.

📢 **섹션 요약 비유**: 미래의 보안은 '천막(컨테이너) 대신 가벼운 조립식 건물(MicroVM)을 지어 더 튼튼한 개인 공간을 제공하는 방향'으로 발전하고 있습니다.

---

### 📌 지식 그래프 (Knowledge Graph)
- [샌드박스 및 Seccomp](./595_sandboxing_seccomp.md) → 컨테이너 런타임 보안의 핵심 엔진
- [가상화 보안](./597_virtualization_security_vm_escape.md) → 컨테이너와 VM 보안 모델의 차이점 및 결합 사례
- [능력 기반 보안](./600_capability_based_security.md) → 리눅스 Capabilities를 통한 권한 최소화 원칙

### 👶 아이를 위한 3줄 비유 (Child Analogy)
1. **상황**: 여러 명이 똑같은 놀이터(호스트 커널)에서 노는데, 어떤 아이가 다른 아이의 장난감을 뺏으려 해요.
2. **원리**: 그래서 선생님이 아이들에게 투명한 풍선 옷(컨테이너)을 입혀서 서로 만지지 못하게 하고, 각자 쓸 수 있는 모래의 양(Cgroups)도 정해줬어요.
3. **결과**: 풍선 옷 덕분에 옆 친구를 방해할 수 없고, 정해진 모래로만 노니까 모두가 즐겁고 안전해요!
