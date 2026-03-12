+++
weight = 595
title = "595. 샌드박스 (Sandboxing) 및 시스템 콜 필터링 (Seccomp (Secure Computing mode))"
+++

### 💡 핵심 인사이트 (Insight)
1. **격리를 통한 피해 최소화**: 샌드박스(Sandboxing)는 신뢰할 수 없는 프로세스를 제한된 환경에 가두어, 해당 프로세스가 침해되더라도 호스트 시스템 전체로 피해가 확산되는 것을 방지하는 기술입니다.
2. **시스템 콜 제어 (Attack Surface Reduction)**: Seccomp(Secure Computing mode)는 프로세스가 커널에 요청할 수 있는 시스템 콜(System Call)의 종류를 엄격히 제한하여 공격자가 커널 취약점을 악용할 가능성을 원천 차단합니다.
3. **심층 방어 (Defense in Depth)**: 메모리 보안(ASLR/DEP)이 뚫리더라도, 샌드박스와 Seccomp가 적용되어 있다면 공격자는 파일을 읽거나 네트워크를 사용하는 등 실질적인 공격 행위를 수행할 수 없습니다.

---

## Ⅰ. 샌드박스 (Sandboxing)의 개념과 구현
### 1. 정의
애플리케이션이 실행되는 동안 접근할 수 있는 자원(파일, 네트워크, 디바이스 등)을 격리된 영역으로 한정하는 보안 메커니즘입니다.

### 2. 주요 구현 방식
- **Rule-based**: 특정 디렉토리만 접근 가능하도록 규칙 설정.
- **Resource Limitation**: CPU, 메모리 사용량 제한.
- **Environment Isolation**: 별도의 파일 시스템 뷰(chroot, Namespace) 제공.

📢 **섹션 요약 비유**: 샌드박스는 '아이들이 마음껏 놀되 밖으로 나가지 못하도록 만든 모래 놀이터'와 같습니다. 안에서 아무리 난리를 쳐도 집 전체를 어지럽힐 수는 없습니다.

---

## Ⅱ. Seccomp (Secure Computing mode) 분석
### 1. 기술적 메커니즘 (ASCII Diagram)
```text
[User Application]
       |
       | 1. System Call Request (e.g., execve("/bin/sh"))
       V
[Linux Kernel (Seccomp Filter)]
       |
       | 2. Check Filter Table (BPF Program)
       |    - Allowed List: [read, write, exit, sigreturn]
       |    - Denied List: [execve, socket, connect, ...]
       |
       | 3. Verdict:
       |    - IF Allowed: Execute Syscall
       |    - IF Denied:  Return Error (EPERM) or TERMINATE Process (SIGSYS)
       V
[Kernel Core / Hardware]
```

### 2. BPF (Berkeley Packet Filter) 활용
현대의 Seccomp-BPF는 단순한 목록 확인을 넘어, 시스템 콜의 인자(Argument)까지 검사할 수 있는 유연한 필터링 엔진을 제공합니다.

📢 **섹션 요약 비유**: Seccomp는 '건물 입구에서 허락된 물건(시스템 콜)만 들고 들어올 수 있게 검사하는 보안 요원'과 같습니다. 위험한 물건을 가져오면 바로 쫓겨납니다.

---

## Ⅲ. 샌드박스 기술의 진화: 네임스페이스와 Cgroups
### 1. 네임스페이스 (Namespaces)
프로세스가 보는 시스템 자원을 논리적으로 분리합니다.
- **PID Namespace**: 다른 프로세스를 볼 수 없음.
- **Network Namespace**: 별도의 네트워크 스택 사용.
- **Mount Namespace**: 독립된 파일 시스템 트리.

### 2. Cgroups (Control Groups)
프로세스 그룹이 사용할 수 있는 물리적 자원(CPU, Memory, I/O)의 양을 제어하여 자원 고갈 공격(DoS)을 방지합니다.

📢 **섹션 요약 비유**: 네임스페이스는 '옆방에 누가 사는지 모르게 하는 투명 벽'이고, Cgroups는 '각 방에 공급되는 전기와 물의 양을 제한하는 계량기'입니다.

---

## Ⅳ. 실제 적용 사례
### 1. 웹 브라우저 (Chrome, Firefox)
렌더러 프로세스를 샌드박스에 가두어, 악성 웹사이트 방문으로 인해 브라우저 코드가 실행되더라도 사용자 파일이 탈취되는 것을 막습니다.

### 2. 컨테이너 (Docker, Kubernetes)
컨테이너 실행 시 기본적으로 Seccomp 프로필을 적용하여 `mount`, `reboot` 등 위험한 시스템 콜 사용을 차단합니다.

### 3. 모바일 앱
Android와 iOS는 모든 앱을 개별적인 샌드박스 내에서 실행하여 앱 간의 데이터 탈취를 원천적으로 방지합니다.

📢 **섹션 요약 비유**: 브라우저 샌드박스는 '투명한 유리창 너머로 사나운 맹수(웹 콘텐츠)를 구경하는 것'과 같습니다. 맹수가 아무리 날뛰어도 관람객(사용자 시스템)은 안전합니다.

---

## Ⅴ. 한계점 및 고려사항
### 1. 설정의 복잡성
너무 엄격한 Seccomp 필터링은 프로그램의 정상적인 동작을 방해할 수 있으며, 이를 분석하고 프로필을 작성하는 데 많은 노력이 필요합니다.

### 2. 커널 표면적 공격
샌드박스 자체가 커널에 의존하므로, 허용된 시스템 콜 자체에 취약점이 있거나 커널 버그를 이용한 '샌드박스 탈출(Sandbox Escape)' 공격이 가능할 수 있습니다.

📢 **섹션 요약 비유**: 아무리 튼튼한 울타리라도 '울타리 밑을 파서 도망가는 기술'이나 '울타리 문지기(커널)를 매수하는 행위'에는 주의해야 합니다.

---

### 📌 지식 그래프 (Knowledge Graph)
- [실행 방지 비트 (NX bit/DEP)](./594_nx_bit_dep.md) → 메모리 침해 사고 발생 시의 후속 방어선
- [컨테이너 보안](./598_container_security.md) → 샌드박스 기술이 집약된 현대적 활용 사례
- [능력 기반 보안](./600_capability_based_security.md) → 시스템 콜 단위보다 더 세밀한 권한 제어 방식

### 👶 아이를 위한 3줄 비유 (Child Analogy)
1. **상황**: 낯선 장난감이 우리 집을 망가뜨릴까 봐 걱정돼요.
2. **원리**: 그래서 장난감을 아주 튼튼하고 투명한 상자 안에 넣고, 장난감이 "가위 빌려줘!"라고 해도 절대 안 빌려주게 규칙(Seccomp)을 정했어요.
3. **결과**: 이제 장난감이 상자 안에서 아무리 장난을 쳐도 우리 집 물건은 하나도 망가지지 않아요!
