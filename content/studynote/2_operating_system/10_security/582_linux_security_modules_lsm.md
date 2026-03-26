+++
title = "582. 리눅스 보안 모듈 (LSM, Linux Security Modules)"
date = "2026-03-25"
[extra]
categories = ["studynote-operating-system"]
+++

# 리눅스 보안 모듈 (LSM, Linux Security Modules) - 리눅스 커널에 보안 정책 enforcement 기능을 플러그인 방식으로 제공 하는 프레임워크

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LSM(Linux Security Modules)은 리눅스 커널에 **"보안 enforcement를 위한 훅(Hook)"**을 제공하여, SELinux, AppArmor 등 다양한 보안 모듈이 커널을 수정하지 않고 **플러그인 방식으로** 부착할 수 있게 하는 프레임워크이다.
> 2. **가치**: 이 **추상화 계층(Abstraction Layer)** 덕분에 커널 코드와 보안 정책 코드가 분리되어, 다양한 보안 정책(SELinux, AppArmor, Smack, Tomoyo 등)을 자유롭게 선택하고 교체할 수 있다.
> 3. **한계**: 각 보안 모듈이 LSM 훅을 모두 지원하지는 않아서, **모듈 간 기능 차이**가 있으며, 동시에 두 개 이상의 주요 MAC 모듈을 사용하는 것은 권장되지 않는다.

---

## 1. 개요 및 배경 (Context & Necessity)

### 1.1 LSM 이전의 문제점

과거에는 보안 기능이 커널 코드에 직접 구현되었다:

```c
// 과거 구현 예시
int sys_open(const char *filename, int flags) {
    // 보안检查(검사)를 직접 구현
    if (!check_security_policy(filename))
        return -EACCES;
    // ...
}
```

**문제점**:
- 커널 코드 변경 필요
- 보안 모듈 간 코드 중복
- 유지보수 어려움

### 1.2 LSM의 해결책

LSM은 **"훅(Hook)"**을 통해 보안 검사를위한 인터페이스를 제공한다:

```c
// LSM 훅을 통한 보안 검사
int security_inode_permission(struct inode *inode, int mask) {
    if (security_ops && security_ops->inode_permission)
        return security_ops->inode_permission(inode, mask);
    return 0;
}
```

---

## 2. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 LSM 훅의 종류

LSM은 약 **150개 이상의 훅**을 제공한다:

| 카테고리 | 주요 훅 | 설명 |
|:---|:---|:---|
| **프로세스** | `task_alloc`, `task_free` | 프로세스 생성/소멸 시 |
| **파일** | `inode_permission`, `file_permission` | 파일 접근 시 |
| **네트워크** | `inet_conn_request`, `socket_sendmsg` | 네트워크 통신 시 |

### 2.2 주요 보안 모듈

| 모듈 | 개발자 | 특징 |
|:---|:---|:---|
| **SELinux** | NSA | 유형 Enforcement, 가장 강력한 MAC |
| **AppArmor** | Novell/SUSE | 경로 기반 MAC |
| **Smack** | NSA | 단순화된 라벨 기반 MAC |
| **Tomoyo** | NTT | 경로 기반 MAC, 관리 용이 |

### 2.3 SELinux와의關係

```text
[ SELinux 구조 ]
커널 <-- LSM Hooks --> SELinux Module
                    |
                    +-- security_ops 포인터가 selinux_ops를 가리킴
```

SELinux는 LSM의 **기본 구현(security_ops)**으로 등록되어 있다.

---

## 3. LSM의 동작 흐름

### 3.1 파일 접근 시 security check 흐름

```text
[ 파일 접근 요청 ]
    |
    v
[ DAC 검사 (传统的 리눅스 권한 검사) ]
    - owner/group/others 확인
    - rwx 비트 검사
    |
    v
[ LSM Hook 호출 ]
    |
    v
[ 보안 모듈 (SELinux/AppArmor) ]
    - 보안 정책 확인
    - 접근 허용/거부 결정
    |
    v
[ 결과 반환 ]
```

### 3.2 Enforcing vs Permissive

| 모드 | 설명 |
|:---|:---|
| **Enforcing** | 보안 정책 위반 시 접근 거부 |
| **Permissive** | 위반 시ログ(로그)만 기록, 접근은 허용 |

---

## 4. 기대효과 및 결론

- **유연성**: 다양한 보안 모듈을 선택적으로 사용 가능
- **모듈성**: 커널 코드와 보안 정책 분리
- **표준화**: LSM API를 통해 다양한 보안 솔루션 지원

---

## 관련 개념 맵 (Knowledge Graph)

| 관련 개념 | 설명 |
|:---|:---|
| **SELinux (583장)** | LSM 기반의 대표적인 MAC 구현 |
| **AppArmor (584장)** | LSM 기반의 경로 기반 MAC 구현 |
| **MAC (579장)** | LSM이 구현하는 상위 보안 체계 |
| **DAC (578장)** | LSM 훅 이전에 수행되는 기본 접근 제어 |

---

## 👶 어린이를 위한 3줄 비유 설명

1. **LSM**은 놀이공원의 **"입구 보안 시스템"**과 같다. 놀이공원 입장구에 **"보안 Hook"** 장치를 설치해 두고, 원하는 보안 회사(SELinux, AppArmor 등)로부터 **"보안 서비스"**를 선택받아 Hook에 연결할 수 있다.

2. **SELinux**는 놀이공원의 **"NSA 인증 경비 회사"**이고, **AppArmor**는 **"SUSE 경비 회사"**이다. 둘 다 Hook에 연결할 수 있지만, 동시에 두 개의 경비 회사를 고용하는 것은 불가능하다.

3. **Enforcing vs Permissive**는 경비 회사의 **"적용 모드"**와 같다. Enforcing은 규칙을 위반하면 입장 차단하고, Permissive는Violations(위반)을 기록만 하고 입장은 허용한다.
