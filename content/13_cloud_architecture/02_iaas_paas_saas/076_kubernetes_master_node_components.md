---
title: "Kubernetes Master Node Components"
date: "2026-04-07"
tags:
  - "studynote-cloud-architecture"
weight: 76
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes(K8s)의 Control Plane은 클러스터의 desired state를 유지하는 두뇌이며, 실제 Pod를 직접 돌리는 곳이 아니다.
> 2. **가치**: API Server, etcd, Scheduler, Controller Manager가 분업해 선언형 운영과 self-healing을 가능하게 한다.
> 3. **판단 포인트**: 고가용성(HA, High Availability)은 워커를 더 많이 붙이는 것이 아니라, API Server 가용성, etcd quorum, 백업 복구를 먼저 지키는 데서 시작한다.

---

## Ⅰ. 개요 및 필요성

쿠버네티스(Kubernetes, K8s)는 수십~수백 개의 노드와 수천 개의 컨테이너를 사람이 직접 SSH로 관리할 수 없기 때문에 등장했다. 사용자는 "웹 서버 5개를 유지하라"고 선언만 하고, 시스템은 그 상태를 계속 맞춘다. 이때 상태를 결정하고 감시하는 중심이 Control Plane이다.

Control Plane이 없으면 배치, 재시작, 장애 복구, 스케일 조정이 모두 수작업이 된다. 그래서 대규모 운영에서는 "어떤 Pod가 어디서 떠야 하는가"를 정하는 제어층과 "실제로 실행하는가"를 맡는 워커층을 분리한다.

```text
kubectl
  |
  v
API Server ----> etcd
  |               ^
  +---> Scheduler  | desired state
  +---> Controller Manager
        |
        v
     kubelet ----> Pod
```

이 흐름의 핵심은 모든 변경이 API Server를 거쳐야 한다는 점이다. 그러면 상태가 기록되고, 다시 복구할 수 있다.

- **📢 섹션 요약 비유**: 학교에서 교실 배치를 직접 학생들이 바꾸지 않고 교무실에서 결정하는 것과 같다. 누가 어디에 앉을지는 관리실이 정해야 질서가 선다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Control Plane의 핵심 컴포넌트는 네 가지다. API Server는 유일한 관문, etcd는 상태 저장소, Scheduler는 배치 담당, Controller Manager는 선언된 상태를 계속 맞추는 감시자다. 여기에 cloud-controller-manager가 붙을 수 있지만, 기본 뼈대는 변하지 않는다.

| 컴포넌트 | 역할 | 장애 시 영향 |
| :-- | :-- | :-- |
| API Server | 모든 요청의 관문 | 클러스터 조작 불가 |
| etcd | 상태 저장소 | desired state 유실 위험 |
| Scheduler | Pod 배치 결정 | 새 Pod가 어디 갈지 못 정함 |
| Controller Manager | 상태 보정 | self-healing 중단 |

Control Plane은 "명령을 내리는 곳"이 아니라 "상태를 계속 맞추는 곳"이다. 이 차이 때문에 쿠버네티스는 선언형(declarative) 운영에 강하다.

- **📢 섹션 요약 비유**: 조종실은 엔진을 직접 만들지 않는다. 대신 어디로 갈지 정하고, 계기판을 보면서 계속 방향을 맞춘다.

---

## Ⅲ. 비교 및 연결

Control Plane과 Worker Node를 구분해야 쿠버네티스가 보인다. 또한 선언형과 명령형 운영의 차이도 함께 봐야 한다.

| 구분 | Control Plane | Worker Node |
| :-- | :-- | :-- |
| 목적 | 상태 결정과 제어 | 실제 실행 |
| 핵심 소프트웨어 | API Server, etcd, Scheduler, Controller Manager | kubelet, runtime, CNI |
| 장애 의미 | 클러스터 제어 불능 | 일부 워크로드 중단 |
| 운영 포인트 | HA, quorum, backup | 자원, 네트워크, 디스크 |

선언형 운영은 "원하는 상태"를 적고 시스템이 맞추게 하는 방식이다. 반대로 직접 Pod를 죽였다 살리는 임시 대응은 명령형에 가깝다. 대규모 환경일수록 선언형이 유지보수와 재현성에서 유리하다.

- **📢 섹션 요약 비유**: 화장실 청소표를 붙여 두면 누가 언제 닦을지 보인다. 매번 말로만 지시하면 금방 잊힌다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 Control Plane의 가용성과 복구 가능성이 핵심이다. 특히 etcd는 클러스터의 기억이므로 snapshot 백업과 복구 절차가 반드시 있어야 한다.

### 체크리스트
1. API Server가 로드밸런서 뒤에서 이중화되는가?
2. etcd가 3노드 이상 quorum을 유지하는가?
3. etcd snapshot 백업과 복구 리허설이 있는가?
4. RBAC(Role-Based Access Control)과 감사 로그가 남는가?
5. 버전 업그레이드 시 control plane / worker skew를 확인하는가?

### 안티패턴
- Control Plane 1대에 모든 것을 올림
- etcd 백업 없이 운영
- kubectl로 직접 Pod만 만지며 선언형 원칙을 무시
- 클라우드 연동을 위해 필요한 cloud-controller-manager를 누락

학습 정리에서는 "Pod를 띄운다"보다 "상태를 유지한다"를 강조해야 한다. 이것이 Control Plane의 본질이기 때문이다.

- **📢 섹션 요약 비유**: 학교가 잘 굴러가려면 교무실이 살아 있어야 한다. 학생 수가 많아져도 교무실의 기록과 배치표가 무너지면 운영이 멈춘다.

---

## Ⅴ. 기대효과 및 결론

Control Plane이 안정적이면 쿠버네티스는 자동 배치, 자동 복구, 자동 확장을 수행한다. 그 결과 운영자는 개별 서버가 아니라 정책과 상태에 집중할 수 있다.

단, HA는 공짜가 아니다. quorum, backup, 네트워크 지연, 인증, 버전 호환성을 함께 관리해야 한다. 그래서 Control Plane은 "많이 실행하는 곳"이 아니라 "절대 잃으면 안 되는 곳"으로 기억해야 한다.

- **📢 섹션 요약 비유**: 지휘봉이 흔들리면 연주가 흔들린다. 악기 수보다 지휘체계가 먼저다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| K8s(Kubernetes) | 컨테이너 오케스트레이션 |
| Control Plane | 상태 제어 계층 |
| API Server | 단일 관문 |
| etcd | 상태 저장과 quorum |
| Scheduler | 배치 결정 |
| Controller Manager | 상태 복원 |
| kubelet | 워커 노드 실행 에이전트 |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 서버 운영
    |
    v
선언형 배포(YAML)
    |
    v
API Server / etcd / Scheduler / Controller
    |
    v
self-healing / autoscaling / HA
    |
    v
관리형 K8s(EKS, GKE)와 Control Plane 추상화
```

이 흐름은 실행 중심 운영에서 상태 중심 운영으로의 진화를 보여준다. 다음 단계는 Control Plane 자체를 관리형 서비스로 맡기고, 사용자는 더 높은 수준의 정책에 집중하는 것이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서는 선생님이 자리를 정하고 학생은 따라가요.
2. 학생이 마음대로 자리 바꾸면 수업이 엉망이 돼요.
3. 쿠버네티스의 뇌는 자리와 규칙을 정해 주는 선생님 같아요.
