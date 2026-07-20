---
title: "Deployment Kubernetes Workload Rolling Update"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
weight: 87
---
## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: Rolling update는 Kubernetes (K8s) Deployment가 새 ReplicaSet을 점진적으로 늘리고 기존 ReplicaSet을 줄여가며 서비스 가동을 유지하는 배포 방식이다.
    > 2. **가치**: readiness probe와 maxSurge/maxUnavailable 조합이 잘 맞아야 무중단에 가까운 교체가 가능하다.
    > 3. **판단 포인트**: 버전 호환성과 종료 절차를 무시하면 롤링 업데이트는 안전한 배포가 아니라 점진적 장애 전파가 된다.

    ---

    ## Ⅰ. 개요 및 필요성

    Deployment는 Kubernetes (K8s)에서 애플리케이션 배포 상태를 선언적으로 관리한다. Rolling update는 원하는 상태를 새 버전으로 바꾸되, 모든 Pod를 한꺼번에 죽이지 않고 조금씩 교체하는 전략이다.

이 방식이 필요한 이유는 대부분의 서비스가 24/7 가동을 전제로 하기 때문이다. 갑작스런 전면 재시작은 세션 끊김과 요청 실패를 유발하므로, 신규 버전을 조용히 투입하고 기존 버전을 점차 내리는 과정이 필요하다.

    - **📢 섹션 요약 비유**: 새 학급이 준비되면 옛 학급을 조금씩 정리하는 교실 교대와 같다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    Deployment는 새 ReplicaSet을 생성하고, 설정된 비율만큼 Pod를 올린 뒤 readiness가 확인되면 기존 Pod를 내린다. 핵심 제어 변수는 `maxSurge`, `maxUnavailable`, `progressDeadlineSeconds`다.

| 항목 | 의미 | 실무 포인트 |
| :-- | :-- | :-- |
| maxSurge | 원하는 수보다 잠시 더 올릴 수 있는 Pod 수 | 여유 자원과 속도 균형 |
| maxUnavailable | 업데이트 중 허용되는 비가용 Pod 수 | 서비스 가용성 보장 |
| readiness probe | 트래픽을 받아도 되는지 판단 | 실제 의존성까지 확인 |
| liveness probe | Pod가 살아 있는지 판단 | 비정상 프로세스 자동 재시작 |

```text
Deployment
   |
   +--► New ReplicaSet -► Pod v2 -► Pod v2 -► Pod v2
   |
   +--► Old ReplicaSet -► Pod v1 -► Pod v1 (점진 축소)
```

Rolling update의 핵심은 "새 Pod가 준비되기 전에 옛 Pod를 내리지 않는 것"이다. 그래서 트래픽 분산은 Service와 readiness가 함께 책임져야 한다.

    - **📢 섹션 요약 비유**: 아이들이 다 들어왔는지 확인하고 나서만 자리를 넘기는 것이 중요하다.

    ---

    ## Ⅲ. 비교 및 연결

    Rolling update는 Recreate, Blue-Green, Canary와 비교해야 선택이 쉬워진다.

| 전략 | 다운타임 | 복잡도 | 특징 |
| :-- | :-- | :-- | :-- |
| Recreate | 큼 | 낮음 | 한 번에 교체 |
| Rolling update | 작음 | 중간 | 점진 교체 |
| Blue-Green | 거의 없음 | 높음 | 두 환경을 병행 |
| Canary | 최소 | 높음 | 일부 트래픽만 신버전으로 |

Rolling update는 서비스가 이전 버전과 새 버전을 동시에 잠깐 받아도 괜찮을 때 가장 적합하다. 반면 DB 스키마 변경처럼 구버전과 신버전이 서로 호환되지 않으면, expand/contract 방식이나 별도 전환 절차를 먼저 넣어야 한다.

    - **📢 섹션 요약 비유**: 한꺼번에 방을 비우는 것보다, 새 방과 옛 방을 잠깐 같이 쓰는 편이 안전하다.

    ---

    ## Ⅳ. 실무 적용 및 실무자 판단

    실무에서는 애플리케이션뿐 아니라 종료 절차까지 설계해야 한다. `preStop`, `terminationGracePeriodSeconds`, 세션 드레이닝, 캐시 동기화가 맞물려야 사용자 요청이 잘린 채 끝나지 않는다.

### 체크리스트
1. readiness probe가 외부 의존성까지 확인하는가?
2. 새 버전과 옛 버전이 동시에 살아도 호환되는가?
3. 종료 시 기존 연결을 안전하게 정리하는가?
4. 롤백 절차가 자동화되어 있는가?

### 안티패턴
- 헬스 체크만 통과하면 바로 트래픽을 받는 구조
- DB 마이그레이션과 앱 롤아웃을 동시에 깨는 구조
- Pod 종료 시간을 무시하고 강제 kill만 하는 구조

    - **📢 섹션 요약 비유**: 문이 열렸다고 바로 손님을 들이면 안 되고, 준비 완료 표시를 봐야 한다.

    ---

    ## Ⅴ. 기대효과 및 결론

    Rolling update는 서비스 가용성과 배포 속도를 동시에 챙기는 현실적인 전략이다. 특히 상태 없는 워크로드에서는 가볍고 안전하게 버전 전환을 할 수 있다.

다만 이 전략은 호환성 전제가 있어야 안전하다. 따라서 롤링 업데이트는 단순한 "자동 재시작"이 아니라, 버전 공존을 견디는 시스템 설계의 결과로 기억해야 한다.

    - **📢 섹션 요약 비유**: 서랍을 하나씩 바꾸면 덜 놀라지만, 옛 서랍과 새 서랍이 잘 맞아야 한다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| Kubernetes (K8s) Deployment | 선언형 배포 컨트롤러 |
| ReplicaSet | Pod 수를 유지하는 단위 |
| readiness probe | 트래픽 수용 가능 여부 |
| maxSurge / maxUnavailable | 롤링 속도와 가용성 조절 |
| Rollback | 실패 시 이전 상태로 복귀 |

    ### 📈 관련 키워드 및 발전 흐름도

    새 버전 이미지 준비
    |
    v
Deployment 롤링 시작
    |
    v
readiness 통과 Pod 교체
    |
    v
안정화 후 이전 ReplicaSet 축소

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 새 교실을 먼저 준비한 뒤, 옛 교실을 천천히 정리하는 것과 같아요.
    2. 준비가 안 된 새 교실은 손님을 받으면 안 돼요.
    3. 그래서 컴퓨터도 조금씩 바꾸면서 안전하게 옮겨요.
