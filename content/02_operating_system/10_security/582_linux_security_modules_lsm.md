---
title: "Linux Security Modules Lsm"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 582
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LSM(Linux Security Modules)은 리눅스 커널에 <strong>"보안 enforcement를 위한 훅(Hook)"</strong>을 제공하여, SELinux, AppArmor 등 다양한 보안 모듈이 커널을 수정하지 않고 **플러그인 방식으로** 부착할 수 있게 하는 프레임워크이다.
> 2. **가치**: 이 <strong>추상화 계층(Abstraction Layer)</strong> 덕분에 커널 코드와 보안 정책 코드가 분리되어, 다양한 보안 정책(SELinux, AppArmor, Smack, Tomoyo 등)을 자유롭게 선택하고 교체할 수 있다.
> 3. **한계**: 각 보안 모듈이 LSM 훅을 모두 지원하지는 않아서, <strong>모듈 간 기능 차이</strong>가 있으며, 동시에 두 개 이상의 주요 MAC 모듈을 사용하는 것은 권장되지 않는다.

---

## Ⅰ. 개요 및 필요성

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

LSM은 <strong>"훅(Hook)"</strong>을 통해 보안 검사를위한 인터페이스를 제공한다:

```c
// LSM 훅을 통한 보안 검사
int security_inode_permission(struct inode *inode, int mask) {
    if (security_ops && security_ops->inode_permission)
        return security_ops->inode_permission(inode, mask);
    return 0;
}
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 LSM 훅의 종류

LSM은 약 <strong>150개 이상의 훅</strong>을 제공한다:

| 카테고리 | 주요 훅 | 설명 |
|:---|:---|:---|
| **프로세스** | `task_alloc`, `task_free` | 프로세스 생성/소멸 시 |
| <strong>파일</strong> | `inode_permission`, `file_permission` | 파일 접근 시 |
| **네트워크** | `inet_conn_request`, `socket_sendmsg` | 네트워크 통신 시 |

### 2.2 주요 보안 모듈

| 모듈 | 개발자 | 특징 |
|:---|:---|:---|
| <strong>SELinux</strong> | NSA | 유형 Enforcement, 가장 강력한 MAC |
| <strong>AppArmor</strong> | Novell/SUSE | 경로 기반 MAC |
| **Smack** | NSA | 단순화된 라벨 기반 MAC |
| **Tomoyo** | NTT | 경로 기반 MAC, 관리 용이 |

### 2.3 SELinux와의관계

```text
[ SELinux 구조 ]
커널 <-- LSM Hooks --> SELinux Module
                    |
                    +-- security_ops 포인터가 selinux_ops를 가리킴
```

SELinux는 LSM의 <strong>기본 구현(security_ops)</strong>으로 등록되어 있다.

---

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

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

리눅스 보안 모듈 (LSM, Linux Security Modules)은(는) 비바 모델 (Biba Model), SELinux과 비교할 때 경계가 선명해진다. 같은 범주에 속하더라도 목표가 성능인지, 격리인지, 단순성인지에 따라 선택 기준이 달라진다. 따라서 이 개념은 독립적으로 외우기보다 앞뒤 개념과 함께 묶어 이해해야 시험과 실무에서 흔들리지 않는다.

| 비교 축 | 비바 모델 (Biba Model) | 리눅스 보안 모듈 (LSM, Linux Security Modules) | SELinux |
|:---|:---|:---|:---|
| 초점 | 기반 조건 | 현재 판단 기준 | 확장/세분화 방향 |
| 운영 관점 | 준비 단계 | 핵심 제어 단계 | 후속 최적화 단계 |

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

- **유연성**: 다양한 보안 모듈을 선택적으로 사용 가능
- <strong>모듈성</strong>: 커널 코드와 보안 정책 분리
- **표준화**: LSM API를 통해 다양한 보안 솔루션 지원

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

리눅스 보안 모듈 (LSM, Linux Security Modules)은 운영체제 보호와 보안 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 SELinux처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 벨-라파둘라 모델 (Bell-LaPadula) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 비바 모델 (Biba Model) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| SELinux | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| AppArmor | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[비바 모델 (Biba Model)]
    |
    v
[리눅스 보안 모듈 (LSM, Linux Security Modules)]
    |
    +---> [SELinux]
    +---> [AppArmor]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>LSM</strong>은 놀이공원의 <strong>"입구 보안 시스템"</strong>과 같다. 놀이공원 입장구에 **"보안 Hook"** 장치를 설치해 두고, 원하는 보안 회사(SELinux, AppArmor 등)로부터 <strong>"보안 서비스"</strong>를 선택받아 Hook에 연결할 수 있다.

2. <strong>SELinux</strong>는 놀이공원의 <strong>"NSA 인증 경비 회사"</strong>이고, <strong>AppArmor</strong>는 <strong>"SUSE 경비 회사"</strong>이다. 둘 다 Hook에 연결할 수 있지만, 동시에 두 개의 경비 회사를 고용하는 것은 불가능하다.

3. <strong>Enforcing vs Permissive</strong>는 경비 회사의 <strong>"적용 모드"</strong>와 같다. Enforcing은 규칙을 위반하면 입장 차단하고, Permissive는Violations(위반)을 기록만 하고 입장은 허용한다.
