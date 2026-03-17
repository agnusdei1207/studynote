+++
title = "651. SELinux (Security-Enhanced Linux)"
date = "2026-03-16"
weight = 651
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "SELinux", "Security-Enhanced Linux", "MAC", "Type Enforcement", "보안 강화"]
+++

# SELinux (Security-Enhanced Linux)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SELinux는 **리눅스 커널에 강제적 접근 제어(MAC, Mandatory Access Control)**를 추가하여 **기본 DAC보다 훨씬 강력한 보안**을 제공하는 NSA 개발 보안 모듈이다.
> 2. **가치**: "Root 권한을 탈취해도 시스템은 보호"되며, **제로 데이 취약점의 영향을 최소화**하고 **프로세스/파일의 최소 권한 원칙**을 강제한다.
> 3. **융합**: Type Enforcement, Role-Based Access Control, MLS(Multi-Level Security)를 지원하며, 정책 모듈화로 유연성과 보안의 균형을 맞춘다.

+++

## Ⅰ. SELinux의 개요

### 1. 정의
- SELinux는 NSA(미국 국방부)가 개발한 리눅스 보안 강화 모듈로, DAC를 넘어선 **강제적 접근 제어(MAC)**를 제공한다.

### 2. 등장 배경
- 기존 리눅스의 DAC는 root 탈취 시 무력
- **"최소 권한을 강제하는 시스템 필요"**

### 3. 💡 비유: '학교의 엄격한 규칙'
- DAC는 **"선생님 허용하면 되는 것"**이지만,
- SELinux는 **"학교 교칙에 따라 누구나 지켜야 하는 규칙"**이다.

- **📢 섹션 요약 비유**: DAC는 "가족 간의 약속"이지만, SELinux는 "법률"입니다. 어떤 경우라도 지켜야 하는 강력한 규칙이죠.

+++

## Ⅱ. DAC vs MAC (Deep Dive)

### 1. 비교
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                   DAC vs MAC 비교                               │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [DAC (Discretionary Access Control)]                          │
    │   - 소유자(Owner)가 접근 권한 결정                             │
    │   - Root는 모든 것에 접근 가능                                 │
    │   - 유연하지만 root 탈취 시 전체 위험                          │
    │   - Unix/Linux 기본 (rwx, chmod, chown)                        │
    │                                                                 │
    │  [MAC (Mandatory Access Control)]                              │
    │   - 시스템 정책이 접근 권한 결정                               │
    │   - Root라도 정책 위반 접근 불가                               │
    │   - 엄격하지만 보안성 우수                                     │
    │   - SELinux, AppArmor, SMACK                                   │
    └─────────────────────────────────────────────────────────────────┘
```

+++

## Ⅲ. SELinux 아키텍처

### 1. 핵심 개념
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                 SELinux 보안 아키텍처                           │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Subject (주체)]                         [Object (객체)]       │
    │   Process                                       File           │
    │   │                                              │             │
    │   │   [Security Context]                          │             │
    │   │   system_u:system_r:httpd_t:s0               │             │
    │   │                                              │             │
    │   │              ┌──────────────────────┐        │             │
    │   │              │   Security Server    │        │             │
    │   │              │   (Kernel 내부)       │        │             │
    │   │              └──────────┬───────────┘        │             │
    │   │                         │                  │             │
    │   │                         ▼                  │             │
    │   │              ┌──────────────────────┐        │             │
    │   │              │   Policy Database    │        │             │
    │   │              │   (이진 규칙)        │        │             │
    │   │              │                      │        │             │
    │   │              │  Allow httpd_t      │        │             │
    │   │              │    to read var_log_t│        │             │
    │   │              └──────────────────────┘        │             │
    │   │                                               │             │
    │   ▼                                               ▼             │
    │  [Decision]                                       │             │
    │   - PERMIT  (허용)                               │             │
    │   - DENY    (거부)                               │             │
    │   - AUDIT   (감사)                               │             │
    │                                                                 │
    │  * "Default Deny": 명시적으로 허용하지 않으면 모두 거부        │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Security Context 구조
```
user:role:type:level

예: system_u:system_r:httpd_t:s0

- user: SELinux 사용자 ID (system_u, user_u, root_u)
- role: 역할 (system_r, staff_r, user_r)
- type: 도메인/타입 (httpd_t, var_log_t) ★ 가장 중요
- level: MLS 레벨 (s0, s1, c0.c102)
```

+++

## Ⅳ. SELinux 모드

### 1. 동작 모드
| 모드 | 설명 | 정책 강제 |
|:---|:---|:---|
| **Enforcing** | 활성화, 정책 강제 | ✅ |
| **Permissive** | 활성화, 로그만 | ❌ (테스트용) |
| **Disabled** | 비활성화 | ❌ |

### 2. 모드 확인/변경
```bash
# 모드 확인
sestatus

# Enforcing 모드
setenforce 1

# Permissive 모드
setenforce 0

# 영구 설정 (/etc/selinux/config)
SELINUX=enforcing
```

+++

## Ⅴ. Type Enforcement

### 1. 핵심 개념
- **도메인(Domain)**: 프로세스의 타입 (예: `httpd_t`)
- **타입(Type)**: 파일/객체의 타입 (예: `httpd_content_t`)
- **규칙**: 도메인이 어떤 타입에 접근할 수 있는지 정의

```text
    httpd_t  ──can read──▶  httpd_content_t  (웹 콘텐츠)
    httpd_t  ──can write──▶  httpd_log_t     (로그 파일)
    httpd_t  ─X cannot───▶  user_home_t     (사용자 홈)
```

+++

## Ⅵ. 실무 적용

### 1. 문제 해결
```bash
# 로그 확인
ausearch -m avc -ts recent

# 문제 분석
audit2why < /var/log/audit/audit.log

# 정책 생성
audit2allow -a -M mymodule
semodule -i mymodule.pp
```

### 2. 안티패턴
- **"그냥 끄기"**: Permissive 모드 테스트 후 해결
- **"Permissive로 운영"**: 보안 효과 없음

+++

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **제로데이 방어**: 알려지지 않은 취약점의 영향 제한
- **최소 권한 강제**: 프로세스가 필요한 것만 접근

### 2. 미래 전맹
- **Container 보안**: SELinux + Docker
- **Policy as Code**: SELinux 정책을 코드로 관리

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **접근 제어**: 상위 개념
- **보안 정책**: MAC 보안 모델
- **컨테이너 보안**: SELinux 활용

+++

## 👶 어린이를 위한 3줄 비유 설명
1. SELinux는 **"학교의 엄격한 교침"** 같아요.
2. 선생님(root)이라도 교칙을 어기면 벌을 받죠.
3. 덕분에 누군가 나쁜 짓을 해도 다른 사람들을 안전하게 지킬 수 있어요!