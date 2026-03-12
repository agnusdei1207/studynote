+++
weight = 600
title = "600. 능력 기반 보안 (Capability-based Security)"
+++

### 💡 핵심 인사이트 (Insight)
1. **권한의 객체화**: 능력(Capability) 기반 보안은 '누가(Subject)' 자원에 접근하는지가 아니라, '어떤 티켓(Capability)'을 가지고 있는지를 기준으로 접근을 제어하는 객체 지향적 보안 모델입니다.
2. **최소 권한의 원칙 (PoLP) 실현**: 프로세스에게 시스템의 모든 권한을 주는 대신, 특정 작업을 수행하는 데 필요한 최소한의 '토큰'만 부여하여 권한 남용 및 침해 사고의 파급 효과를 차단합니다.
3. **혼란된 대리자 (Confused Deputy) 문제 해결**: 접근 제어 목록(ACL) 방식의 고질적 문제인 권한 대행 공격을 방지할 수 있는 구조적 이점을 제공합니다.

---

## Ⅰ. 능력 기반 보안 (Capability-based Security)의 개념
### 1. 정의
특정 객체(파일, 디바이스, 프로세스 등)에 대한 접근 권한과 그 객체를 가리키는 포인터를 결합한 '티켓' 혹은 '토큰'을 의미합니다. 이 토큰을 소유한 프로세스만이 해당 객체에 접근할 수 있습니다.

### 2. ACL (Access Control List)과의 비교
- **ACL**: 자원 측면에서 "내 방에 들어올 수 있는 사람 명단"을 관리 (누구인가?).
- **Capability**: 사용자 측면에서 "특정 방에 들어갈 수 있는 열쇠"를 소유 (무엇을 가졌는가?).

📢 **섹션 요약 비유**: ACL은 '문 앞의 경비원이 명단을 확인하는 것'이고, Capability는 '문 앞에 경비원은 없지만 열쇠가 있는 사람만 문을 열 수 있는 것'과 같습니다.

---

## Ⅱ. 작동 메커니즘 분석 (ASCII Diagram)
### 1. Capability 전달 및 검증
```text
[Parent Process]
       |
       | 1. Create Resource (e.g., File A)
       | 2. Receive 'Capability Token' from Kernel
       | 3. Fork Child Process
       | 4. Pass 'Capability Token' to Child (via IPC or Inheritance)
       V
[Child Process]
       |
       | 5. Request Action (e.g., Write to File A)
       |    Request includes [Token ID]
       V
[Operating System Kernel]
       |
       | 6. Validate Token ID in Capability Table
       | 7. Perform Operation on Object
       V
[Target Resource (File A)]
```

### 2. 위조 방지 (Unforgeability)
능력 토큰은 유저 모드에서 직접 조작할 수 없으며, 커널의 보호된 메모리 영역(Capability Table)에 저장되거나 강력한 암호화 기법으로 보호되어야 합니다.

📢 **섹션 요약 비유**: Capability는 '위조가 불가능한 특수 바코드 티켓'과 같습니다. 티켓이 있으면 입장이 가능하지만, 내 마음대로 바코드를 수정할 수는 없습니다.

---

## Ⅲ. 리눅스 Capabilities (Linux Capabilities)
### 1. 도입 배경
전통적인 유닉스 시스템의 '루트(Root) 아니면 일반 사용자'라는 이분법적 권한 모델의 한계를 극복하기 위해, 루트의 막강한 권한을 수십 개의 세부 항목으로 쪼갠 것입니다.

### 2. 주요 Capability 항목
- **CAP_NET_ADMIN**: 네트워크 설정 변경 권한.
- **CAP_SYS_TIME**: 시스템 시간 설정 변경 권한.
- **CAP_CHOWN**: 파일 소유자 변경 권한.

📢 **섹션 요약 비유**: 리눅스 Capabilities는 '만능 마스터키 하나를 주는 대신, 현관문 열쇠, 화장실 열쇠, 창고 열쇠를 각각 따로 나누어 주는 것'과 같습니다.

---

## Ⅳ. 능력 기반 보안의 장점과 과제
### 1. 장점
- **세밀한 제어 (Fine-grained Control)**: 필요한 기능만 핀포인트로 부여 가능.
- **동적 권한 위임**: 프로세스 간에 권한(티켓)을 쉽게 전달하거나 회수할 수 있음.
- **보안 설계의 명확성**: 권한의 범위가 객체 단위로 명확히 정의됨.

### 2. 과제
- **권한 회수 (Revocation)**: 이미 배포된 티켓을 다시 뺏어오기가 ACL 방식보다 복잡할 수 있음.
- **관리 복잡성**: 수많은 프로세스와 자원 간의 티켓 배포 현황을 추적하기 어려움.

📢 **섹션 요약 비유**: 장점은 '꼭 필요한 권한만 줄 수 있어 안전하다는 점'이고, 과제는 '너무 많은 열쇠가 돌아다니면 관리하기 힘들다'는 점입니다.

---

## Ⅴ. 현대 보안 아키텍처에서의 활용
### 1. 컨테이너 보안
도커(Docker)나 쿠버네티스(Kubernetes) 환경에서 컨테이너에게 루트 권한을 주지 않고, 필요한 Capability만 선별적으로 부여하여 호스트 탈취 위험을 최소화합니다.

### 2. 차세대 운영체제 (Fuchsia 등)
구글의 Fuchsia OS 등 최신 마이크로커널 운영체제는 설계 초기 단계부터 모든 자원 접근을 Capability 기반으로 처리하도록 구축되고 있습니다.

📢 **섹션 요약 비유**: 현대 보안은 '모든 사람에게 신분증(ID)을 묻기보다, 각 상황에 맞는 이용권(Capability)을 확인하는 시스템'으로 진화하고 있습니다.

---

### 📌 지식 그래프 (Knowledge Graph)
- [최소 권한의 원칙 (Principle of Least Privilege)](./587_principle_of_least_privilege.md) → Capability 보안이 추구하는 철학적 기초
- [컨테이너 보안](./598_container_security.md) → Linux Capabilities가 가장 활발하게 사용되는 실무 분야
- [접근 제어 모델](./585_access_control.md) → ACL 모델과 Capability 모델의 비교 분석

### 👶 아이를 위한 3줄 비유 (Child Analogy)
1. **상황**: 놀이터에 있는 모든 놀이기구를 다 탈 수 있는 '마법 팔찌'는 너무 위험해요. (나쁜 사람이 뺏어갈 수 있거든요!)
2. **원리**: 그래서 미끄럼틀만 탈 수 있는 티켓, 그네만 탈 수 있는 티켓을 따로 만들어서 필요한 티켓만 나눠줬어요.
3. **결과**: 티켓이 없는 친구는 다른 기구를 탈 수 없어서 놀이터가 훨씬 안전해졌어요!
