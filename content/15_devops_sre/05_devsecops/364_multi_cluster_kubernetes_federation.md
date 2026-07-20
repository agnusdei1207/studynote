---
title: "Multi-cluster Kubernetes Federation High-Availability Deployment"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 364
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티클러스터 K8s Federation은 지리적으로 분산된 여러 Kubernetes 클러스터를 단일 제어 평면으로 관리해 재해 복구(DR), 레이턴시 최적화, 컴플라이언스 경계 분리를 동시에 달성하는 고가용성 아키텍처다.
> 2. **가치**: KubeFed v2/Cluster API는 클러스터 라이프사이클을, Argo CD ApplicationSet은 GitOps 기반 멀티클러스터 앱 배포를, Submariner는 클러스터 간 파드 네트워크 연결을 제공해, 단일 장애점 없는 글로벌 분산 서비스를 구현한다.
> 3. **판단 포인트**: Active-Active 구성은 제로 RTO (Recovery Time Objective)가 목표지만 데이터 일관성 처리가 복잡하며, Active-Passive는 RTO가 높지만 운영 단순성을 선택할 때 적합하다.

---

## Ⅰ. 개요 및 필요성

단일 Kubernetes 클러스터는 하나의 리전/데이터센터 장애 시 전체 서비스가 중단되는 단일 장애점(SPoF)이다. 금융·의료·공공 서비스처럼 99.99% 가용성이 요구되는 시스템에서는 멀티클러스터 구성이 필수다.

멀티클러스터 필요 시나리오: 지리적 DR, EU GDPR 데이터 잔류 요건, 사용자 위치 기반 레이턴시 최적화, 환경 격리(prod/staging/dev).

- 📢 섹션 요약 비유: 단일 클러스터는 본점 하나만 있는 은행이다. 본점이 불나면 모든 업무가 마비된다. 멀티클러스터는 전국 지점망이 있는 은행으로, 한 지점이 닫혀도 다른 지점에서 즉시 서비스가 계속된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|           멀티클러스터 K8s 아키텍처 (Active-Active)              |
+------------------------------------------------------------------+
|  [글로벌 DNS / GSLB]                                             |
|  지역별 트래픽 라우팅 (가중치, 레이턴시, 헬스체크 기반)          |
|         |                        |                              |
|  [클러스터 A: ap-northeast-2]   [클러스터 B: us-east-1]         |
|  Argo CD ApplicationSet         Argo CD ApplicationSet          |
|         |                        |                              |
|  [Submariner / Cilium ClusterMesh — 클러스터 간 파드 네트워크]   |
|         |                                                        |
|  [Cluster API — 클러스터 생성·업그레이드 자동화]                 |
+------------------------------------------------------------------+
```

| 도구                        | 역할                                           |
| :-------------------------- | :--------------------------------------------- |
| KubeFed v2                  | 리소스 페더레이션 정책 배포                    |
| Cluster API (CAPI)          | 클러스터 라이프사이클 자동화                   |
| Argo CD ApplicationSet      | GitOps 기반 멀티클러스터 앱 동기화             |
| Submariner                  | 클러스터 간 파드/서비스 IP 연결                |
| Cilium ClusterMesh          | eBPF 기반 멀티클러스터 서비스 디스커버리       |

<strong>Active-Active vs Active-Passive</strong>:
- Active-Active: 두 클러스터 모두 트래픽 처리. 데이터 동기화 복잡. RTO=0 목표.
- Active-Passive: 주 클러스터가 트래픽 처리, 대기 클러스터는 준비. 단순하지만 페일오버 시 RTO 수분.

- 📢 섹션 요약 비유: Active-Active는 두 소방서가 동시에 출동해 불을 끄는 구조고, Active-Passive는 한 소방서가 주로 출동하고 다른 하나는 대기하는 구조다.

---

## Ⅲ. 비교 및 연결

| 항목           | 단일 클러스터              | 멀티클러스터 Active-Active  |
| :------------- | :------------------------- | :--------------------------|
| 가용성         | 99.9% (클러스터 내 HA)     | 99.999% (제로 다운타임)    |
| RTO            | N/A (클러스터 전체 장애)   | ~0초                       |
| 데이터 복잡성  | 낮음                       | 높음 (동기 복제 또는 CRDT) |
| 비용           | 낮음                       | 2x + 네트워크 비용         |

GitOps와의 연계: Argo CD ApplicationSet의 `ClusterGenerator`는 등록된 모든 클러스터를 자동 탐색해 동일한 앱 배포를 선언적으로 관리한다.

- 📢 섹션 요약 비유: Argo CD ApplicationSet은 체인점 통합 관리 시스템이다. 본사(Git 저장소)에서 메뉴를 바꾸면 전국 모든 지점(클러스터)에 자동으로 반영된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>멀티클러스터 설계 체크리스트</strong>
1. HA 목표 정의: RTO/RPO 요건에 따라 Active-Active vs Active-Passive 결정
2. 클러스터 간 네트워크: Submariner 또는 Cilium ClusterMesh로 파드 IP 연결
3. 데이터 레이어: 멀티리전 DB(CockroachDB, Vitess) 또는 비동기 복제 전략
4. GitOps 파이프라인: Argo CD ApplicationSet으로 클러스터별 오버라이드 관리
5. 글로벌 트래픽 라우팅: GSLB 헬스체크와 쿠버네티스 서비스 상태 연동

<strong>안티패턴</strong>
- 클러스터 간 네트워크 미연결 -> 서비스 디스커버리 실패
- 데이터 동기화 없이 Active-Active -> 데이터 불일치
- Cluster API 없이 수동 클러스터 관리 -> 업그레이드 드리프트

- 📢 섹션 요약 비유: 멀티클러스터 데이터 동기화 없이 Active-Active를 하면, 두 금고(클러스터)가 각각 다른 잔액을 표시하는 상황이 된다.

---

## Ⅴ. 기대효과 및 결론

글로벌 서비스 기업(Netflix, Google)은 멀티클러스터 아키텍처로 단일 리전 장애에 무관한 서비스를 운영한다. 멀티클러스터는 단일 클러스터 대비 2~3배 인프라 비용이 발생하므로, 비즈니스 크리티컬 서비스에만 적용하는 계층적 전략이 현실적이다.

미래는 WASM (WebAssembly) 기반 에지 컴퓨팅과 멀티클러스터의 통합으로 클라우드-에지 연속성이 강화된다.

- 📢 섹션 요약 비유: 멀티클러스터는 여러 나라에 지점을 둔 다국적 기업이다. 한 나라에 문제가 생겨도 다른 나라 지점이 고객을 받아 서비스를 유지한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| KubeFed v2                              | 멀티클러스터 리소스 정책 페더레이션 배포                  |
| Cluster API (CAPI)                      | 클러스터 생성·업그레이드 IaC 자동화                       |
| Argo CD ApplicationSet                  | GitOps 멀티클러스터 앱 동기화, ClusterGenerator          |
| Submariner                              | IPSec 기반 클러스터 간 파드 네트워크 연결                 |
| Cilium ClusterMesh                      | eBPF 기반 클러스터 간 서비스 디스커버리                  |
| GSLB (Global Server Load Balancing)     | 글로벌 DNS 기반 트래픽 라우팅                            |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 K8s 클러스터 (단일 장애점)
    |
    v
다중 AZ 배포 (동일 리전 HA)
    |
    v
멀티클러스터 — KubeFed v2 + Cluster API
    |
    v
Argo CD ApplicationSet — GitOps 멀티클러스터 배포
    |
    v
Submariner / Cilium ClusterMesh — 클러스터 간 네트워킹
    |
    v
GSLB + Active-Active — 글로벌 제로다운타임
```

### 👶 어린이를 위한 3줄 비유 설명

1. 멀티클러스터는 여러 나라에 지점이 있는 편의점 체인이에요. 한 지점이 닫혀도 옆 지점에서 물건을 살 수 있어요.
2. Argo CD는 본사에서 신메뉴를 만들면 자동으로 모든 지점에 알려주는 통합 관리 시스템이에요.
3. Submariner는 각 지점이 땅 아래 비밀 통로로 연결되어 있어서 서로 데이터를 주고받을 수 있는 거예요.
