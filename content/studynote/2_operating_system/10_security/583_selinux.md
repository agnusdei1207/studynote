+++
title = "583. SELinux (Security-Enhanced Linux) - NSA가 만든 리눅스 커널용 강제 접근 제어 보안 모듈"
date = "2026-03-25"
[extra]
categories = ["studynote-operating-system"]
+++

# SELinux (Security-Enhanced Linux) - NSA가 만든 리눅스 커널용 강제 접근 제어 보안 모듈

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SELinux는 1990년대 NSA(미국 국가안보국)와 함께 개발된 리눅스 커널용 MAC(강제적 접근 제어) 보안 모듈로, 582장의 LSM(Linux Security Modules) 프레임워크 위에 구현된다. 모든 프로세스와 파일에 **"보안 컨텍스트(Security Context = user:role:type:level)"** 라는 4단계 라벨을 부착하고, **Type Enforcement(유형 강제)** 방식으로 접근을 통제하는 커널 레벨 보안 시스템이다.
> 2. **가치**: **유형 강제 통제(Type-Enforced Confinement)** 덕분에, Nginx 웹 서버가 해킹당해 `rm -rf /`(시스템 삭제) 명령을 내려도, LSM 훅에서 Nginx 프로세스의 유형(`httpd_t`)이 `/etc/shadow`(파일 유형 `shadow_t`)에 접근할 수 없도록 차단한다. 제로 데이(Zero-Day) 취약점이 발견되어도, 권한 상승(Privilege Escalation)을 원천 차단하는 방어선을 제공한다.
> 3. **한계**: SELinux의 가장 큰 약점은 **디버깅 지옥(Debugging Nightmare)** 과 비활성화 유혹이다. SELinux가 적용된 환경에서 접근 거부(`Permission Denied`) 오류가 발생하면, 해당 프로세스와 파일의 유형(`_t` 접미사)을 하나하나 추적해야 한다. 이 과정에서 90%의 관리자가 `/etc/selinux/config`에서 `SELINUX=disabled`로 설정하여(SELinux 끄기) 방어망을 해제하는 문제가 발생한다.

---

## 1. 개요 및 배경 (Context & Necessity)

### 1.1 전통적 DAC 방식의 한계
과거 리눅스의 **임의적 접근 제어(DAC)** 환경에서는 `root` 사용자가 시스템의 모든 권한을 보유한다. Apache 서버가 `root` 권한으로 실행되고 있다면, 공격자가 해당 서버를 침투하여 **권한 상승(Privilege Escalation)**에 성공하면 `/etc/shadow`(패스워드 데이터베이스)까지 접근하여 모든 사용자 패스워드를 탈취할 수 있다.

### 1.2 SELinux의 해결책 (Type Enforcement 방식)
NSA는 리눅스에 **"유형(Type)"** 기반 보안 모델을 도입했다. 프로세스의 유형(`httpd_t`)과 파일의 유형(`httpd_sys_content_t`)이 명시적으로 매핑되어야 접근이 허용된다. 이는 다음과 같은 원리다:

```
[ 전통 DAC ]   : root가 모든 파일 접근 가능 -> 위험!
[ SELinux MAC ]: "httpd_t 프로세스는 shadow_t 파일에 접근 불가!" -> O(1) 차단
```

### 1.3 보안 컨텍스트(Security Context)의 구조
SELinux는 모든 주체(프로세스)와 객체(파일)에 **"보안 컨텍스트(Security Context)"**라는 4단계 라벨을 부여한다:

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

**[핵심 포인트]** SELinux 접근 제어에서 가장 중요한 요소는 **`3. Type(유형)`** 이다. 일반적인 User, Role 등은 SELinux 정책에서 보조적 역할을 하며, `httpd_t`와 같이 `_t` 접미사를 가진 유형이 핵심 접근 결정 기준이 된다.

---

## 2. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 SELinux 동작 모드: Enforcing vs Permissive

SELinux는 두 가지 동작 모드를 지원하며, 운영 환경에 따라 선택적으로 적용한다.

| 구분 | Enforcing (강제 모드) | Permissive (허용 모드) |
|:---|:---|:---|
| **LSM 훅 후 동작** | `httpd_t`가 `shadow_t`에 접근 시 **`Permission Denied` 오류를 반환하고 접근을 차단.** | 접근을 허용하되, **거부(Deny) 시뮬레이션을 audit.log에 기록.** |
| **정책 튜닝 효과** | 실제 환경에서 테스트 시 **서비스 중단(Real Impact) 위험.** | 실제 환경에서도 **거부 로그만 출력**하여 정책 디버깅에 활용. |
| **운영 전환** | 문제 발생 시 `setenforce 0`으로 **Permissive로 일시 전환 가능.** | 테스트 완료 후 **NSA 제공 도구로 정책을 컴파일(.pp)하여 Enforcing으로 전환.** |

### 2.2 컨텍스트 상실 문제: 복사 vs 이동

파일 시스템을 조작할 때 **SELinux 컨텍스트가 손실(Relabeling Loss)**되는 문제가 발생한다:

- **문제 상황**: 사용자가 `/home/user/` 디렉터리의 `index.html`을 웹 서버 디렉터리(`/var/www/html`)로 **복사(`cp`)**하면, 복사된 파일은 새로운 컨텍스트(`httpd_sys_content_t`)를 할당받는다.
- **심각한 문제**: 하지만 **이동(`mv`)**할 경우, inode가 유지되어 기존 컨텍스트(`user_home_t`)가 그대로 유지된다. 웹 서버(`httpd_t`)가 `user_home_t` 유형의 파일에 접근하면 `Permission Error`가 발생한다.

**SRE 문제 해결 방법**:

1. **`restorecon -Rv /var/www/html`**: 파일 시스템에 정의된 기본 컨텍스트를 기준으로 재설정
2. **`audit2allow`**: 거부 로그를 분석하여 필요한 정책 규칙(.pp 모듈)을 자동 생성

---

## 3. Docker와 SELinux의 연계

### 3.1 문제 상황: Docker 볼륨 마운트와 SELinux 충돌

```bash
docker run -v /home/user/data:/app
```

위 명령어로 호스트 디렉터리를 컨테이너에 마운트하면, Docker 컨테이너의 유형(`container_t`)이 호스트 파일의 유형(`user_home_t`)과 맞지 않아 접근이 거부된다.

### 3.2 해결책: SELinux 레이블 지정 (:z 또는 :Z 옵션)

```bash
docker run -v /home/user/data:/app:z
```

`:z`(또는 `:Z`) 옵션은 Docker에게 ** SELinux 컨텍스트 재지정**을 지시한다. Docker가 대상 디렉터리에 `container_file_t` 유형을 부여하여, 컨테이너가 정상적으로 접근할 수 있도록 한다.

---

## 4. 기대효과 및 결론

- **강제적 접근 제어(MAC) 체계**는 SELinux를 통해 리눅스 커널에 내장되어, Red Hat/CentOS 등 엔터프라이즈 배포판에서 기본 보안 시스템으로 채택되었다. 이는 "관리자가 모든 접근을 통제(강제)"하는 접근 방식을 구현한다.
- **레이블 기반 통제(Label-based Confinement)** 원칙에 따라, Android(SEAndroid 포함) 등 모바일 플랫폼에서도 SELinux 기술이 활용되어,** 샌드박스(Sandbox) 격리 환경**을 구현한다.
- **정책 디버깅의 복잡성**은 여전히 과제다. "너무 복잡해서 `setenforce 0`(비활성화)으로 전환하는 관리자(admin nightmare)" 문제를 해결하기 위해, **`audit2allow` 도구**와 **`:z` 옵션** 등 실질적인 편의를 제공한다.

---

## 관련 개념 맵 (Knowledge Graph)

| 관련 개념 | 설명 |
|:---|:---|
| **LSM 프레임워크 (582장)** | SELinux는 582장의 LSM(150개 훅) 위에 구현되는 보안 모듈이다. SELinux는 150개의 LSM 훅 중 '보안 검사' 훅에 부착되는 주요 플러그인이다. |
| **MAC 강제적 접근 제어 (579장)** | SELinux는 579장의 MAC(Mandatory Access Control) 접근 방식을 구현한다. SELinux의 컨텍스트(Context) 매핑이 O(1) 시간에 접근 권한을 결정하는 것이 DAC와의 핵심 차이다. |
| **AppArmor (584장)** | RedHat 진영의 SELinux와 달리, Ubuntu/SUSE 진영에서는 AppArmor를 사용한다. SELinux가 유형(Type) 라벨로 접근을 제어한다면, AppArmor는 경로(Path `/var/www/`) 기반으로 접근을 제어하는 것이 핵심 차이다. |
| **도메인 전환 (Domain Transition)** | 프로세스가 다른 보안 도메인으로 전환할 때, CPU 권한 레벨과 SELinux 컨텍스트가 동시에 변경되어야 한다. 이 이중 검사가 O(1) 시간에 수행되어야 시스템 성능을 보장한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. **SELinux는 박물관 경비 시스템**과 같다. 구경꾼(일반 사용자)은 일반 전시실만 돌아다닐 수 있고, 학예사(웹 서버)도 별도의 경비증을 받아야 특정 금고(비밀 파일)에 접근할 수 있다. **경비원이 경비증을 확인하지 않으면 아무도 들어갈 수 없게**锁(쇠창)를 채우는 것과 같다.

2. **SELinux는 "보안 라벨"을 이용해 접근을 제어**한다. 웹 서버에는 `httpd_t`(웹 유형)라는 라벨이 붙어있고, 비밀 파일에는 `shadow_t`(비밀 유형)라는 라벨이 붙어있다. 웹 서버가 비밀 파일에 접근하려고 하면, **"네 라벨은 웹服务器인데, 여기 들어갈 수 있어?"라는 질문에 "안 돼!"** 하고 쫓겨난다.

3. **SELinux의 어려운 점**은 **설정 파일에서 `SELINUX=disabled`로 끌 수 있다는 것**이다. 마치 "火灾(화재) 경보기 때문에 귀찮다"고 Alarm(경보)을 꺼버리면, 정말로 火事(화재)가 났을 때 알림을 받을 수 없는 것과 같다. 이것이 SELinux를 해제하면 안 되는 이유다.
