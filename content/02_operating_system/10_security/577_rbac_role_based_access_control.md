---
title: "Rbac Role Based Access Control"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 577
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RBAC은 **"사용자(User)"와 **"권한(Permission)"** 사이에 **"역할(Role)"**을 매개로 두어, N:M 관계를 2개의 1:N 관계로 분할하는 모델이다.
> 2. **가치**: 직원이 10만 명이고 권한 설정이 100만 개인 환경에서, 역할(Role) 100개만 관리하면 되어 **권한 관리 복잡도를 $O(N \times M)$에서 $O(R)$로**대폭(대폭) 감소시킨다.
> 3. **한계**: 직원이 여러 역할(Role)을 동시에 보유하면, 부여하면 안 되는 권한 조합이 발생할 수 있어 **권한 분리(SoD: Separation of Duty)** 원칙을 별도로 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 ACL/Capability의 한계: 직접 매핑

기존 ACL/Capability는 **사용자-권한 직접 매핑**:
- 사용자 10만 명 × 권한 100만 개 = <strong>1조 개의 매핑 관계</strong>
- 신규 직원 입사 시: 100만 개 권한 중 필요한 권한을 직접 할당
- 직원 퇴사 시: 해당원공이 가진 모든 권한을 찾아 회수

### 1.2 RBAC의 해결책: 역할(Role) 매개

```
[ 기존 ] User <--> Permission (1만 × 100만 = 1조 매핑)
[ RBAC ] User <--> Role <--> Permission (1만 × 100 + 100 × 100만 = 관리 가능)
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 RBAC의 4가지 핵심 구성 요소

| 구성 요소 | 설명 |
|:---|:---|
| **User (사용자)** | 시스템에 접근하는 주체 |
| **Role (역할)** | 업무 분장에 따른 권한 묶음 (예: 인사팀, 회계팀) |
| **Permission (권한)** | 객체에 대한 구체적 연산 (예: 파일 읽기, 쓰기) |
| <strong>Session (세션)</strong> | 사용자가 역할을 활성화하는 동적 연결 |

### 2.2 사용자-역할 배정 (User-Role Assignment)

```text
[ 예시 ]
직원이 3명, 역할이 3개
- alice: {인사팀 역할}
- bob: {회계팀 역할}
- charlie: {인사팀, 회계팀 역할}
```

### 2.3 역할-권한 배정 (Role-Permission Assignment)

```text
[ 인사팀 역할의 권한 ]
- 사원档案(파일): {Read}
- 급여档案(파일): {Write}

[ 회계팀 역할의 권한 ]
- 재무제표(파일): {Read, Write}
```

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 Static Separation of Duty (SSD)

역할 생성 시점에 <strong>상호 배타적 역할</strong>을 정의:

```text
[ 예시 ]
{회계_요청_역할}과 {회계_승인_역할}은同一(동일) 사용자에게 동시에 할당 불가
```

### 3.2 Dynamic Separation of Duty (DSD)

실행 시점에 <strong>활성화된 역할</strong>을 제한:

```text
[ 예시 ]
특정 업무 세션에서는 오직 하나의 역할만 활성화 가능
```

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 Kubernetes의 RBAC

```yaml
# Role 정의
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

# RoleBinding 정의
kind: RoleBinding
subjects:
- kind: User
  name: alice
roleRef:
  kind: Role
  name: pod-reader
```

### 4.2 Role vs ClusterRole

| 구분 | Role | ClusterRole |
|:---|:---|:---|
| **적용 범위** | 특정 네임스페이스 | 클러스터 전체 |
| **리소스** | Namespaced 리소스 | Namespaced + Cluster-wide 리소스 |

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

- **관리 효율성**: 역할 단위의 권한 관리를 통해 관리 포인트대폭(대폭) 감소
- **보안 강화**: 권한 분리(SoD) 원칙을 통해 민감 업무의 권한 집중 방지
- **변경 대응**:인사(인사) 이동 시 역할만 재할당하면 되어 빠른 대응 가능

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 접근 제어 목록 (ACL, Access Control List) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 자격 증명 리스트 (Capability List / Ticket) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 임의적 접근 제어 (DAC, Discretionary Access Control) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 강제적 접근 제어 (MAC, Mandatory Access Control) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[자격 증명 리스트 (Capability List / Ticket)]
    |
    v
[롤 기반 접근 제어 (RBAC, Role-Based Access Control)]
    |
    +---> [임의적 접근 제어 (DAC, Discretionary Access Control)]
    +---> [강제적 접근 제어 (MAC, Mandatory Access Control)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>RBAC</strong>은 놀이공원에서 <strong>"직급증가표"</strong>를 통한 접근 제어와 같다. 직급표(역할)를 가지고 있으면, 해당 직급이 출입 가능한 모든 놀이기구를 자동으로가이리용(可以利用)할 수 있다.

2. <strong>역할 매개</strong>는 각 부서장의 역할(인사팀, 회계팀)을정의(정의)하고, 직원에게 부서 역할을 부여하는 것과 같다. 새로운 직원이 들어오면 역할만 부여하면 되고, 퇴사하면 역할을 회수하면 된다.

3. <strong>권한 분리(SoD)</strong>는 <strong>"요청하는 사람"과 "승인하는 사람"을 분리</strong>하는 것과 같다. 돈을 보내라는 요청을 직접 승인하면 사기(yscams)가 발생할 수 있으므로, 별도의 역할을 통해상호검증(상호 검증)을 수행한다.
