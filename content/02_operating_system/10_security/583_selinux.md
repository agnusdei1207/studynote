---
title: "SELinux"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 583
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SELinux는 1990년대 NSA(미국 국가안보국)와 함께 개발된 리눅스 커널용 MAC(강제적 접근 제어) 보안 모듈로, 582장의 LSM(Linux Security Modules) 프레임워크 위에 구현된다. 모든 프로세스와 파일에 <strong>"보안 컨텍스트(Security Context = user:role:type:level)"</strong> 라는 4단계 라벨을 부착하고, **Type Enforcement(유형 강제)** 방식으로 접근을 통제하는 커널 레벨 보안 시스템이다.
> 2. **가치**: **유형 강제 통제(Type-Enforced Confinement)** 덕분에, Nginx 웹 서버가 해킹당해 `rm -rf /`(시스템 삭제) 명령을 내려도, LSM 훅에서 Nginx 프로세스의 유형(`httpd_t`)이 `/etc/shadow`(파일 유형 `shadow_t`)에 접근할 수 없도록 차단한다. 제로 데이(Zero-Day) 취약점이 발견되어도, 권한 상승(Privilege Escalation)을 원천 차단하는 방어선을 제공한다.
> 3. **한계**: SELinux의 가장 큰 약점은 **디버깅 지옥(Debugging Nightmare)** 과 비활성화 유혹이다. SELinux가 적용된 환경에서 접근 거부(`Permission Denied`) 오류가 발생하면, 해당 프로세스와 파일의 유형(`_t` 접미사)을 하나하나 추적해야 한다. 이 과정에서 90%의 관리자가 `/etc/selinux/config`에서 `SELINUX=disabled`로 설정하여(SELinux 끄기) 방어망을 해제하는 문제가 발생한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 전통적 DAC 방식의 한계
과거 리눅스의 <strong>임의적 접근 제어(DAC)</strong> 환경에서는 `root` 사용자가 시스템의 모든 권한을 보유한다. Apache 서버가 `root` 권한으로 실행되고 있다면, 공격자가 해당 서버를 침투하여 <strong>권한 상승(Privilege Escalation)</strong>에 성공하면 `/etc/shadow`(패스워드 데이터베이스)까지 접근하여 모든 사용자 패스워드를 탈취할 수 있다.

### 1.2 SELinux의 해결책 (Type Enforcement 방식)
NSA는 리눅스에 **"유형(Type)"** 기반 보안 모델을 도입했다. 프로세스의 유형(`httpd_t`)과 파일의 유형(`httpd_sys_content_t`)이 명시적으로 매핑되어야 접근이 허용된다. 이는 다음과 같은 원리다:

```
[ 전통 DAC ]   : root가 모든 파일 접근 가능 -> 위험!
[ SELinux MAC ]: "httpd_t 프로세스는 shadow_t 파일에 접근 불가!" -> O(1) 차단
```

### 1.3 보안 컨텍스트(Security Context)의 구조
SELinux는 모든 주체(프로세스)와 객체(파일)에 <strong>"보안 컨텍스트(Security Context)"</strong>라는 4단계 라벨을 부여한다:

```text
[ 확인 방법: ls -Z (SELinux 맥락 확인) ]
=> -rw-r--r--. root root system_u:object_r:shadow_t:s0 /etc/shadow

[ 보안 컨텍스트의 4가지 구성 요소 ]

   system_u    :  object_r    :    shadow_t     :     s0
  (1. User)      (2. Role)        (3. Type)   (4. Level/Category)

  [ SELinux 유형 강제(Type Enforcement) ]
    => 웹 서버(Apache) 프로세스 유형: `system_u:system_r:httpd_t:s0`
    => 비밀 번호 파일 유형: `system_u:object_r:shadow_t:s0`

  [ 결론 ]
    OS 심판: "httpd_t(웹 서버 유형)가 shadow_t(비밀번호 유형)에 접근?
    내 정책(Policy)에 없어! 거부(Denied)!!"
```

**[핵심 포인트]** SELinux 접근 제어에서 가장 중요한 요소는 <strong><code>3. Type(유형)</code></strong> 이다. 일반적인 User, Role 등은 SELinux 정책에서 보조적 역할을 하며, `httpd_t`와 같이 `_t` 접미사를 가진 유형이 핵심 접근 결정 기준이 된다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 SELinux 동작 모드: Enforcing vs Permissive

SELinux는 두 가지 동작 모드를 지원하며, 운영 환경에 따라 선택적으로 적용한다.

| 구분 | Enforcing (강제 모드) | Permissive (허용 모드) |
|:---|:---|:---|
| **LSM 훅 후 동작** | `httpd_t`가 `shadow_t`에 접근 시 <strong><code>Permission Denied</code> 오류를 반환하고 접근을 차단.</strong> | 접근을 허용하되, <strong>거부(Deny) 시뮬레이션을 audit.log에 기록.</strong> |
| <strong>정책 튜닝 효과</strong> | 실제 환경에서 테스트 시 <strong>서비스 중단(Real Impact) 위험.</strong> | 실제 환경에서도 <strong>거부 로그만 출력</strong>하여 정책 디버깅에 활용. |
| **운영 전환** | 문제 발생 시 `setenforce 0`으로 **Permissive로 일시 전환 가능.** | 테스트 완료 후 <strong>NSA 제공 도구로 정책을 컴파일(.pp)하여 Enforcing으로 전환.</strong> |

### 2.2 컨텍스트 상실 문제: 복사 vs 이동

파일 시스템을 조작할 때 <strong>SELinux 컨텍스트가 손실(Relabeling Loss)</strong>되는 문제가 발생한다:

- **문제 상황**: 사용자가 `/home/user/` 디렉터리의 `index.html`을 웹 서버 디렉터리(`/var/www/html`)로 <strong>복사(<code>cp</code>)</strong>하면, 복사된 파일은 새로운 컨텍스트(`httpd_sys_content_t`)를 할당받는다.
- **심각한 문제**: 하지만 <strong>이동(<code>mv</code>)</strong>할 경우, inode가 유지되어 기존 컨텍스트(`user_home_t`)가 그대로 유지된다. 웹 서버(`httpd_t`)가 `user_home_t` 유형의 파일에 접근하면 `Permission Error`가 발생한다.

<strong>SRE 문제 해결 방법</strong>:

1. <strong><code>restorecon -Rv /var/www/html</code></strong>: 파일 시스템에 정의된 기본 컨텍스트를 기준으로 재설정
2. <strong><code>audit2allow</code></strong>: 거부 로그를 분석하여 필요한 정책 규칙(.pp 모듈)을 자동 생성

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 문제 상황: Docker 볼륨 마운트와 SELinux 충돌

```bash
docker run -v /home/user/data:/app
```

위 명령어로 호스트 디렉터리를 컨테이너에 마운트하면, Docker 컨테이너의 유형(`container_t`)이 호스트 파일의 유형(`user_home_t`)과 맞지 않아 접근이 거부된다.

### 3.2 해결책: SELinux 레이블 지정 (:z 또는 :Z 옵션)

```bash
docker run -v /home/user/data:/app:z
```

`:z`(또는 `:Z`) 옵션은 Docker에게 <strong> SELinux 컨텍스트 재지정</strong>을 지시한다. Docker가 대상 디렉터리에 `container_file_t` 유형을 부여하여, 컨테이너가 정상적으로 접근할 수 있도록 한다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

- <strong>강제적 접근 제어(MAC) 체계</strong>는 SELinux를 통해 리눅스 커널에 내장되어, Red Hat/CentOS 등 엔터프라이즈 배포판에서 기본 보안 시스템으로 채택되었다. 이는 "관리자가 모든 접근을 통제(강제)"하는 접근 방식을 구현한다.
- **레이블 기반 통제(Label-based Confinement)** 원칙에 따라, Android(SEAndroid 포함) 등 모바일 플랫폼에서도 SELinux 기술이 활용되어,<strong> 샌드박스(Sandbox) 격리 환경</strong>을 구현한다.
- <strong>정책 디버깅의 복잡성</strong>은 여전히 과제다. "너무 복잡해서 `setenforce 0`(비활성화)으로 전환하는 관리자(admin nightmare)" 문제를 해결하기 위해, <strong><code>audit2allow</code> 도구</strong>와 <strong><code>:z</code> 옵션</strong> 등 실질적인 편의를 제공한다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

SELinux은 운영체제 보호와 보안 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 AppArmor처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 비바 모델 (Biba Model) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 리눅스 보안 모듈 (LSM, Linux Security Modules) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| AppArmor | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 시스템 보안 위협 유형 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[리눅스 보안 모듈 (LSM, Linux Security Modules)]
    |
    v
[SELinux]
    |
    +---> [AppArmor]
    +---> [시스템 보안 위협 유형]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>SELinux는 박물관 경비 시스템</strong>과 같다. 구경꾼(일반 사용자)은 일반 전시실만 돌아다닐 수 있고, 학예사(웹 서버)도 별도의 경비증을 받아야 특정 금고(비밀 파일)에 접근할 수 있다. <strong>경비원이 경비증을 확인하지 않으면 아무도 들어갈 수 없게</strong>쇄(쇠창)를 채우는 것과 같다.

2. <strong>SELinux는 "보안 라벨"을 이용해 접근을 제어</strong>한다. 웹 서버에는 `httpd_t`(웹 유형)라는 라벨이 붙어있고, 비밀 파일에는 `shadow_t`(비밀 유형)라는 라벨이 붙어있다. 웹 서버가 비밀 파일에 접근하려고 하면, **"네 라벨은 웹서비스기인데, 여기 들어갈 수 있어?"라는 질문에 "안 돼!"** 하고 쫓겨난다.

3. <strong>SELinux의 어려운 점</strong>은 <strong>설정 파일에서 <code>SELINUX=disabled</code>로 끌 수 있다는 것</strong>이다. 마치 "화재(화재) 경보기 때문에 귀찮다"고 Alarm(경보)을 꺼버리면, 정말로 화사(화재)가 났을 때 알림을 받을 수 없는 것과 같다. 이것이 SELinux를 해제하면 안 되는 이유다.
