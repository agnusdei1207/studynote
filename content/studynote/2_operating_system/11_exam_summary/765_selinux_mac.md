+++
weight = 765
title = "765. SELinux의 강제 접근 통제 (MAC) 메커니즘과 보안 정책"
date = "2026-03-10"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "SELinux", "MAC", "Mandatory Access Control", "강제 접근 통제", "DAC", "보안 컨텍스트", "LSM"]
series = "운영체제 800제"
+++

# SELinux의 강제 접근 통제 (MAC) 메커니즘

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 커널 수준에서 모든 주체(프로세스)와 객체(파일, 포트)에 **보안 라벨(Security Context)**을 부여하고, 중앙 집중식 정책에 따라 접근을 강제로 제어하는 보안 강화 프레임워크.
> 2. **가치**: 관리자(root) 권한조차도 정책에 정의되지 않은 행위는 수행할 수 없게 하여, 기존 DAC(임의적 접근 통제)의 취약점인 권한 남용과 관리자 탈취 문제를 해결한다.
> 3. **융합**: 리눅스 커널의 **LSM (Linux Security Module)** 인터페이스를 기반으로 작동하며, 벨-라파듈라(Confidentiality) 및 비바(Integrity) 보안 모델의 실질적인 구현체다.

---

### Ⅰ. DAC vs MAC 상세 비교

| 구분 | DAC (Discretionary Access Control) | MAC (Mandatory Access Control) |
|:---|:---|:---|
| **통제 방식** | 소유자가 임의로 권한 부여 (rwxrwxrwx) | **시스템(커널) 정책**에 의해 강제됨 |
| **관리 주체** | 파일 소유자 (User) | 시스템 관리자 (Security Admin) |
| **보안 수준** | 낮음 (관리자 탈취 시 전권 장악) | **매우 높음** (root도 정책에 묶임) |
| **구현 예시** | 표준 리눅스 파일 권한 | **SELinux, AppArmor** |

---

### Ⅱ. SELinux 아키텍처 및 동작 원리 (ASCII)

보안 정책 결정(Policy Decision)과 집행(Enforcement)이 분리된 구조다.

```ascii
    [ Subject (Process) ] ---- (1) Request Access ----> [ Object (File/Port) ]
           |                                                   ^
           |                                                   |
    +------|---------------------------------------------------|------+
    | Kernel (LSM Hook)                                        |      |
    |      | (2) Ask for Decision                              |      |
    |      v                                                   |      |
    | [ SELinux Security Server ] <--- (3) Check Policy DB     |      |
    |      |                                                   |      |
    |      +--- (4) Allow / Deny ? ----------------------------+      |
    +-----------------------------------------------------------------+
```

**[핵심 요소: 보안 컨텍스트 (Security Context)]**
- `user:role:type:level` (예: `system_u:system_r:httpd_t:s0`)
- 특히 **Type (타입)** 기반의 전이가 핵심이며, 이를 **TE (Type Enforcement)**라고 부른다.

---

### Ⅲ. SELinux 실행 모드

1. **Enforcing**: 정책을 강제하고, 위반 시 차단 및 로그 기록 (운영 표준).
2. **Permissive**: 위반 시 차단은 하지 않고 로그만 기록 (디버깅용).
3. **Disabled**: SELinux 기능을 완전히 끔 (보안 취약).

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. "SELinux를 끄는 것이 정답인가?"
- **현상**: 많은 엔지니어가 앱 실행 에러 시 해결이 어려워 SELinux를 꺼버린다.
- **기술사적 결단**: 
  - 이는 시스템을 무방비 상태로 노출시키는 행위다. 
  - `audit2allow` 도구를 사용하여 위반 로그를 분석하고, 필요한 권한만 정밀하게 허용하는 **Custom Policy**를 생성하여 적용해야 한다.

#### 2. 기술사적 인사이트: 최소 권한의 구현
- 웹 서버(httpd)가 해킹당하더라도, SELinux 정책이 httpd 타입의 프로세스가 `/etc/shadow` 파일을 읽지 못하게 막고 있다면, 공격자는 관리자 비밀번호를 탈취할 수 없다. 이것이 바로 **샌드박싱(Sandboxing)**의 실체다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **보안 가시성 확보**: 시스템 내 모든 자원 흐름에 대한 로그 기록.
- **제로 데이 공격 방어**: 알려지지 않은 취약점을 이용한 비정상적 자원 접근 원천 차단.

#### 2. 미래 전망
최근의 클라우드 네이티브 환경(Kubernetes)에서는 SELinux가 컨테이너 간의 격리를 보장하는 최종 방어선 역할을 한다. 앞으로는 컨테이너 워크로드에 맞춰 정책을 자동으로 생성하고 배포하는 **Dynamic Policy** 기술이 인프라 보안의 핵심이 될 것이며, 모바일 OS(Android) 등 이미 검증된 영역에서 범용 IoT 기기로 그 적용 범위가 확대될 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[LSM (Linux Security Module)](../10_security_performance_virtualization/619_lsm.md)**: SELinux가 기생하는 커널 프레임워크.
- **[벨-라파듈라 모델](../../9_security/TBD_blp.md)**: SELinux의 기반이 되는 다층 보안 모델.
- **[최소 권한 원칙](./740_protection_domain_least_privilege.md)**: SELinux가 실현하고자 하는 철학.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **SELinux**는 컴퓨터 성을 지키는 아주 엄격한 **'보안 AI 경비원'**이에요.
2. 경비원은 "요리사는 주방 도구만 만질 수 있고, 청소부는 빗자루만 만질 수 있다"라는 규칙책(정책)을 한시도 잊지 않죠.
3. 아무리 높은 사람(root)이 와도 규칙책에 없는 짓을 하려고 하면 경비원이 단호하게 "안 돼!"라고 막아준답니다!
