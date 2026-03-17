+++
title = "652. AppArmor"
date = "2026-03-16"
weight = 652
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "AppArmor", "MAC", "프로필", "경로 기반", "SUSE"]
+++

# AppArmor

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AppArmor는 **프로세스별 접근 제어 프로필**을 기반으로 하는 MAC(강제적 접근 제어) 시스템으로, 파일 경로를 기반으로 한 간단한 접근 제어를 제공한다.
> 2. **가치**: SELinux보다 **설정이 간단하고 학습 곡선이 낮으며**, Ubuntu, SUSE에서 표준으로 사용되어 컨테이너 보안(Docker, Kubernetes)에 널리 활용된다.
> 3. **융합**: 커널 모듈로 로드되며, `aa-complain`, `aa-enforce`, `aa-logprof` 등 도구로 프로필을 생성/관리한다.

+++

## Ⅰ. AppArmor의 개요

### 1. 정의
- AppArmor는 2000년대 초 SUSE가 개발한 리눅스 보안 모듈로, **프로세스별로 파일 시스템, 네트워크, 능력(Capability)에 대한 접근을 제한**한다.

### 2. 등장 배경
- SELinux의 복잡성에 대한 대안으로 등장
- 경로 기반 프로필로 쉬운 설정

### 3. 💡 비유: '프로세스별 감옥'
- AppArmor는 **"각 프로그램(프로세스)마다 감옥을 만들어주는 보안 시스템"**과 같다.
- 웹 서버는 웹 서버 감옥에서, 데이터베이스는 DB 감옥에서만 살 수 있다.

- **📢 섹션 요약 비유**: SELinux는 "복잡한 법률"이지만, AppArmor는 "프로그램별 수침"입니다. 더 쉽고 직관적이죠.

+++

## Ⅱ. AppArmor vs SELinux (Deep Dive)

### 1. 비교
| 특성 | AppArmor | SELinux |
|:---|:---|:---|
| **기반** | 경로 기반 | 라벨 기반 |
| **복잡도** | 상대적으로 쉬움 | 복잡함 |
| **배포판** | Ubuntu, SUSE | RHEL, Fedora |
| **설정 단위** | 프로필 | 정책 모듈 |
| **학습 곡선** | 낮음 | 높음 |

### 2. 동작 원리
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                  AppArmor 동작 원리                            │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   Process (nginx)                                              │
    │      │                                                         │
    │      │ open("/var/www/html/index.html")                        │
    │      │                                                         │
    │      ▼                                                         │
    │   ┌─────────────────────────────────────────────────────────┐   │
    │   │              AppArmor Kernel Module                     │   │
    │   │                                                          │   │
    │   │  프로필 확인: /etc/apparmor.d/usr.sbin.nginx           │   │
    │   │                                                          │   │
    │   │  [Profile rules]                                        │   │
    │   │    /var/www/html/** r,                                  │   │
    │   │    /var/log/nginx/* w,                                  │   │
    │   │    /etc/nginx/** r,                                     │   │
    │   │    deny /etc/shadow rwx,                                │   │
    │   │    network inet stream,                                 │   │
    │   │    deny /home/** rw,                                    │   │
    │   └─────────────────────────────────────────────────────────┘   │
    │      │                                                         │
    │      ▼                                                         │
    │   [결과]                                                      │
    │    - ALLOW: 규칙에 일치하면 허용                               │
    │    - DENY:  deny 또는 명시 안 하면 거부                        │
    └─────────────────────────────────────────────────────────────────┘
```

+++

## Ⅲ. AppArmor 프로필

### 1. 프로필 구조
```apparmor
# /etc/apparmor.d/usr.sbin.nginx

#include <tunables/global>

profile nginx /usr/sbin/nginx {
  # 파일 접근
  /var/www/html/** r,
  /var/log/nginx/* w,
  /etc/nginx/** r,
  /run/nginx.pid rw,

  # 거부
  deny /etc/shadow rwx,
  deny /home/** rw,

  # 네트워크
  network inet stream,
  network inet6 stream,

  # 능력 (Capability)
  capability setuid,
  capability net_bind_service,

  # 포함
  include <abstractions/base>
  include <abstractions/nameservice>
}
```

### 2. 주요 지시어
| 지시어 | 설명 |
|:---|:---|
| `r` | 읽기 |
| `w` | 쓰기 |
| `rx` | 실행 |
| `rw` | 읽기/쓰기 |
| `deny` | 명시적 거부 |
| `owner` | 소유자 일치 시 |

+++

## Ⅳ. AppArmor 명령어

### 1. 관리 도구
```bash
# 상태 확인
aa-status

# 프로필 확인
aa-complain /usr/sbin/nginx  # 로그만 기록
aa-enforce /usr/sbin/nginx   # 강제 모드

# 프로필 생성 (자동 학습)
aa-genprof /usr/sbin/nginx

# 로그 분석 후 프로필 업데이트
aa-logprof /usr/sbin/nginx

# 프로필 비활성화
aa-disable /usr/sbin/nginx
```

+++

## Ⅴ. 컨테이너와 AppArmor

### 1. Docker 연동
```bash
# AppArmor 프로필로 컨테이너 실행
docker run --security-opt apparmor=nginx-profile nginx

# 프로필 확인
docker inspect nginx | grep AppArmor
```

+++

## Ⅵ. 실무 적용

### 1. 모범 사례
- **최소 권한**: 불필요한 접근 제거
- **로그 모드 먼저**: complain으로 테스트 후 enforce

### 2. 안티패턴
- **"프로필 없이 운영"**
- **"Overly permissive"**

+++

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **설정 용이**: SELinux보다 쉬움
- **컨테이너 표준**: Docker 기본

### 2. 미래 전맹
- **LSM(Linux Security Modules)과 통합**

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **SELinux**: 다른 MAC 구현
- **접근 제어**: 상위 개념
- **컨테이너 보안**: 활용 사례

+++

## 👶 어린이를 위한 3줄 비유 설명
1. AppArmor는 **"각 아이마다 다른 수칙을 정해주는 선생님"**이에요.
2. 철수는 수학만, 영희는 영어만 할 수 있게 제한하듯이, 각 프로그램도 자기 할 일만 하게 해요.
3. SELinux보다 배우기 쉬워서 초보자도 친환경 보안을 사용할 수 있답니다!