---
title: "Kube Api Server K8S Hub"
date: "2026-04-07"
tags:
  - "studynote-cloud-architecture"
weight: 77
---
# Kube-API Server - 쿠버네티스 통제망의 허브

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kube-API Server는 K8s (Kubernetes) 클러스터에서 모든 요청이 먼저 도달하는 중앙 API 관문이다.
> 2. **가치**: 인증, 인가, 승인, 저장, 감시를 한 곳에 모아 클러스터 상태의 단일 진실을 만든다.
> 3. **판단 포인트**: API Server가 멈추면 워크로드는 잠시 돌아가도, 새 제어와 변경은 사실상 멈춘다.

---

## Ⅰ. 개요 및 필요성
쿠버네티스는 여러 컴포넌트가 협업하는 제어평면(control plane) 구조다. 그 가운데 Kube-API Server는 외부 사용자, 컨트롤러, 스케줄러, kubelet이 모두 거쳐 가는 REST API 입구다. 입구가 하나여야 상태 변경을 일관되게 기록할 수 있다.

API Server가 필요한 이유는 분산된 명령을 하나의 규칙과 하나의 저장소로 모아야 하기 때문이다. 그렇지 않으면 각 컴포넌트가 서로 직접 통신하며 상태 충돌을 일으키기 쉽다.

📢 섹션 요약 비유: 건물의 모든 민원 창구를 하나의 안내 데스크로 모아 두는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리
요청은 `인증(Authentication) -> 인가(Authorization) -> 승인(Admission) -> 저장(etcd) -> 감시(Watch)` 순서로 흐른다. API Server는 단순 전달기가 아니라, 정책을 적용하고 상태를 기록하고 변경을 배포하는 관문이다.

| 단계 | 역할 | 관련 요소 |
| :--- | :--- | :--- |
| Authentication | 신원 확인 | 토큰, 인증서 |
| Authorization | 권한 판단 | RBAC (Role-Based Access Control) |
| Admission | 정책 검증/변경 | Admission Controller, Webhook |
| Persistence | 클러스터 상태 저장 | etcd |
| Watch | 변경 알림 | scheduler, controller, kubelet |

```text
kubectl / controller / kubelet
           |
           v
  +------------------+
  |  Kube-API Server  |
  +-------+----------+
          | authn / authz / admission
          v
         etcd
          |
          +- watch -> controller manager
          +- watch -> scheduler
          +- watch -> kubelet
```

API Server는 원하는 상태(desired state)를 수락하고, 그 상태를 etcd에 저장한 뒤, 다른 컴포넌트가 watch로 반응하게 만든다. 그래서 Kubernetes의 제어는 API Server를 중심으로 수렴한다.

📢 섹션 요약 비유: 접수창구가 신청서를 받아 심사하고, 기록하고, 관련 부서에 동시에 알려주는 흐름이다.

---

## Ⅲ. 비교 및 연결
API Server는 스케줄러나 kubelet과 다르다. 스케줄러는 어떤 노드에 배치할지 결정하고, kubelet은 노드에서 실제 컨테이너를 실행하며, API Server는 그 모든 결정을 받아들이는 통제 허브다.

etcd는 상태 저장소이고, API Server는 그 저장소 앞의 정책 관문이다. 즉 저장소와 관문을 혼동하면 안 된다. 또한 control plane의 고가용성(HA)은 API Server 자체를 여러 개 두고 로드밸런서(LB) 뒤에 배치하는 방식으로 확보한다.

📢 섹션 요약 비유: 교통경찰, 차고, 운행기록부는 역할이 다르다. 겉으로는 다 연결돼 보여도 기능은 분리되어 있다.

---

## Ⅳ. 실무 적용 및 실무자 판단
실무에서는 TLS (Transport Layer Security), RBAC, 감사 로그, rate limit, etcd 백업이 중요하다. 업그레이드 시에는 버전 호환성과 watch 부하를 확인해야 한다.

- 채택: 중앙 정책, 감사, 확장성이 중요한 클러스터
- 회피: API Server 단일 장애점(SPOF)을 허용하는 설계
- 체크리스트
  1. 인증·인가·승인 정책이 분리되어 있는가?
  2. 다중 API Server와 LB가 구성되어 있는가?
  3. etcd 백업과 복구 절차가 준비되어 있는가?
  4. audit log로 누가 무엇을 바꿨는지 추적되는가?

Kube-API Server는 단순 포트가 아니라 운영 통제의 기준점이다. 따라서 가용성과 보안은 함께 봐야 한다.

📢 섹션 요약 비유: 회사의 모든 도장을 한 사무실에 모아두되, 그 사무실이 멈추지 않게 해야 한다.

---

## Ⅴ. 기대효과 및 결론
API Server를 제대로 설계하면 클러스터 변경이 일관되고, 감사 가능하며, 자동화하기 쉬워진다. 결국 이 개념은 "쿠버네티스의 입구이자 기록원"으로 기억하는 것이 맞다.

📢 섹션 요약 비유: 건물의 본관 접수처처럼, 여기서 통과한 일만 전체 건물에 반영된다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| K8s (Kubernetes) | 컨테이너 오케스트레이션 |
| REST API | 외부/내부 제어 인터페이스 |
| RBAC (Role-Based Access Control) | 권한 제어 |
| etcd | 클러스터 상태 저장소 |
| Admission Controller | 정책 검증과 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
kubectl / controller / kubelet
    |
    v
Kube-API Server
    |
    v
인증 -> 인가 -> 승인 -> 저장(etcd)
    |
    v
Watch 기반 제어평면 반응
```

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 모든 신청서는 먼저 행정실로 가요.
2. 행정실이 확인하고 기록한 뒤 필요한 반에 알려줘요.
3. 쿠버네티스의 API 서버도 그 행정실 같은 역할을 해요.
