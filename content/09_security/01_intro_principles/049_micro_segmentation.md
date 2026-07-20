---
title: "Micro Segmentation"
date: "2026-04-05"
tags:
  - "studynote-security"
weight: 49
---
> **핵심 인사이트**
> 1. 마이크로 세그먼테이션(Micro-Segmentation)은 네트워크를 개별 워크로드 또는 애플리케이션 단위로 격리하여 동서 트래픽(East-West: 서버 간)을 제어하는 제로 트러스트 아키텍처의 핵심 기술 — 전통적 경계 방어(Perimeter Defense)가 외부 위협에 집중했다면, 마이크로 세그먼테이션은 내부 침투 후 횡적 이동(Lateral Movement)을 차단한다.
> 2. "최소 권한 원칙(Least Privilege)"을 네트워크 통신에 적용한 것이 마이크로 세그먼테이션의 본질 — 워크로드 A가 워크로드 B와 통신할 명시적 이유가 없다면 기본적으로 차단하며, 필요한 통신만 화이트리스트로 허용한다.
> 3. SDN(Software-Defined Networking) 기반 마이크로 세그먼테이션이 현대 구현의 표준 — VMware NSX, Cisco ACI, Illumio처럼 소프트웨어 정의 방식으로 VLAN 재구성 없이 정책을 동적으로 적용하며, 클라우드·컨테이너 환경의 동적 IP에도 대응한다.

---

## Ⅰ. 기존 보안 모델의 한계

```
전통적 경계 방어 (Perimeter Defense):

외부 인터넷
    v (방화벽이 막음)
내부 네트워크 ---------------------
                  서버A ↔ 서버B ↔ 서버C
                  (내부는 신뢰)

"성벽 모델" 문제:
  성벽(방화벽) 안에 들어오면 자유롭게 이동

  공격 시나리오:
  1. 피싱으로 내부 PC 감염
  2. 내부 PC -> 데이터베이스 서버 (자유롭게 이동)
  3. DB에서 민감 데이터 탈취

  방화벽이 허용했어도 내부 이동은 무방비

VLAN 기반 세그먼테이션 한계:
  VLAN으로 부서 간 분리

  문제:
  같은 VLAN 내 서버들은 자유 통신
  VLAN 변경 = 네트워크 재구성 (고비용)
  동적 클라우드/컨테이너 IP에 대응 어려움

현실 통계:
  평균 침해 탐지 시간: 197일 (IBM 2022)
  내부 이동 시간: 침해 후 4~10일
  -> 조기 발견/차단이 피해 최소화 핵심
```

> 📢 **섹션 요약 비유**: 전통 경계 방어 = 성벽 도시 — 성문(방화벽)만 지키면 내부는 자유. 적이 성문 통과(계정 탈취)하면 내부 모든 곳 이동. 마이크로 세그먼테이션은 건물마다 별도 잠금!

---

## Ⅱ. 마이크로 세그먼테이션 원리

```
마이크로 세그먼테이션:
  워크로드 단위 격리 + 동서 트래픽 제어

개념:
  기존: 서버 A ↔ 서버 B (자유 통신)
  마이크로 세그먼테이션:

  [웹 서버] <--> [앱 서버] <--> [DB 서버]
      ^             ^            ^
  (정책: 80/443만) (정책: 8080) (정책: 3306, 앱서버만)

핵심 원칙:
  묵시적 거부 (Implicit Deny):
  명시적 허용 없으면 기본 차단

  최소 권한 (Least Privilege):
  필요한 포트/프로토콜만 허용

세그먼트 단위:

1. 서브넷/VLAN 기반 (전통):
  IP 대역으로 그룹 구분
  변경 어려움

2. ID 기반 (현대):
  호스트명, 태그, 레이블로 그룹 정의
  IP 변경에 독립적

  예:
  role=web -> role=app: TCP/8080 허용
  role=app -> role=db: TCP/3306 허용
  기타 모든 통신: 차단

3. 프로세스 레벨 (고급):
  서버 내 프로세스 단위 정책
  nginx -> java-app: 허용
  sshd -> 외부: 차단

Zero Trust Network Access와 결합:
  "Never Trust, Always Verify"
  마이크로 세그먼테이션: 동서 트래픽
  ZTNA: 남북 트래픽 (사용자->앱)
```

> 📢 **섹션 요약 비유**: 마이크로 세그먼테이션 = 건물 내 출입증 통제 — 회사 건물 들어왔어도(방화벽 통과) 각 방(워크로드)마다 별도 출입증 필요. 적이 1개 방 침투해도 다른 방 이동 차단!

---

## Ⅲ. 구현 기술

```
구현 방식:

1. 호스트 기반 방화벽:
  각 서버에 iptables/Windows Firewall 설정

  중앙 관리 도구:
  Illumio Core: 에이전트 기반, 자동 정책 학습

  장점: 물리/VM/클라우드 모두 적용
  단점: 에이전트 설치 필요

2. SDN (Software-Defined Networking):
  네트워크 계층에서 정책 적용

  VMware NSX:
  vSphere 환경의 소프트웨어 오버레이
  VLAN 변경 없이 방화벽 정책 적용
  마이크로 세그먼테이션 핵심 솔루션

  Cisco ACI:
  Application Centric Infrastructure
  하드웨어 + 소프트웨어 통합

3. 클라우드 네이티브:
  AWS: Security Group (인스턴스 레벨 방화벽)
  Azure: NSG (Network Security Group)
  GCP: Firewall Rules + VPC-native

  서버리스/컨테이너:
  Kubernetes Network Policy:
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: db-policy
  spec:
    podSelector:
      matchLabels:
        role: db
    ingress:
    - from:
      - podSelector:
          matchLabels:
            role: app
      ports:
      - port: 3306

서비스 메시:
  Istio, Linkerd
  사이드카 프록시로 mTLS + 정책 적용
  컨테이너 간 통신 암호화 + 인증
```

> 📢 **섹션 요약 비유**: K8s NetworkPolicy = 아파트 동·호수별 인터폰 통제 — "앱 파드(302호)는 DB 파드(101호)에만 전화 가능". 나머지 파드 통화 자동 차단!

---

## Ⅳ. 구현 전략

```
마이크로 세그먼테이션 도입 단계:

Phase 1 - 가시성 확보:
  현재 통신 패턴 파악

  도구:
  Illumio 탐색 모드 (트래픽 기록만, 차단 없음)
  VMware NSX Flow Monitoring
  VPC Flow Logs (AWS)

  결과:
  "어떤 서버가 어디와 통신하는가" 맵핑

Phase 2 - 그룹화 및 정책 설계:
  워크로드를 역할 기반 그룹으로 정의

  예: 그룹 정의
  G1: Web servers (role=web)
  G2: App servers (role=app)
  G3: Database (role=db)
  G4: Management (role=mgmt)

  정책:
  인터넷 -> G1: TCP/80,443 허용
  G1 -> G2: TCP/8080 허용
  G2 -> G3: TCP/3306 허용
  G4 -> All: TCP/22 허용 (관리)
  기타: 차단

Phase 3 - 테스트 모드:
  정책 시뮬레이션 (차단 전 기록)
  오탐(False Positive) 확인

Phase 4 - 점진적 적용:
  비중요 시스템부터 시작
  모니터링 후 중요 시스템 확대

Phase 5 - 지속적 관리:
  새 워크로드 배포 시 자동 태그 적용
  정책 드리프트 모니터링
```

> 📢 **섹션 요약 비유**: 마이크로 세그먼테이션 도입 = 공장 안전 구역 설정 — 먼저 직원 이동 패턴 기록(Phase 1), 구역 설정(Phase 2), 가상 울타리 테스트(Phase 3), 단계적 실제 울타리 설치(Phase 4)!

---

## Ⅴ. 실무 시나리오 — 금융권 랜섬웨어 방어

```
금융회사 마이크로 세그먼테이션 도입:

배경:
  2021년 유사 금융사 랜섬웨어 피해 100억+
  내부 서버 간 자유 통신 -> 전사 확산

  현황:
  - 3-Tier 아키텍처 (웹/앱/DB) × 12개 시스템
  - VMware vSphere 환경

구현 (VMware NSX):

가시성:
  NSX Intelligence로 6주간 트래픽 기록
  예상치 못한 통신 발견:
  - HR 서버 -> 생산 DB 직접 통신 (이상)
  - 개발 서버 -> 운영 서버 통신 (위험!)

정책 설계:
  운영 존 (Production):
  Web -> App: 8443
  App -> DB: 5432
  App -> Redis: 6379
  나머지 동서 통신: 전부 차단

  개발 ↔ 운영 격리:
  개발 존 -> 운영 존: 완전 차단

단계적 적용:
  1단계 (2주): 비중요 HR 시스템
  2단계 (2주): 내부 업무 시스템
  3단계 (4주): 핵심 금융 시스템

결과:
  탐색 중 발견 이상 통신: 23건 (즉시 차단)
  시뮬레이션 랜섬웨어 공격:
  - 기존: 전사 확산 (4시간)
  - NSX 적용 후: 최초 감염 서버 1대 격리

  컴플라이언스:
  금융보안원 평가 + 3점 (마이크로 세그 적용)
```

> 📢 **섹션 요약 비유**: 금융 마이크로 세그먼테이션 = 방화 구역 설정 — 공장 각 구역을 방화문으로 분리. 한 구역 화재(랜섬웨어)가 전체 확산 방지. 기존 4시간 확산 -> 1대 격리!

---

## 📌 관련 개념 맵

```
마이크로 세그먼테이션
+-- 목적: 횡적 이동(Lateral Movement) 차단
+-- 원칙
|   +-- 묵시적 거부 (Implicit Deny)
|   +-- 최소 권한 (Least Privilege)
+-- 구현
|   +-- 호스트 방화벽 (Illumio)
|   +-- SDN (VMware NSX, Cisco ACI)
|   +-- 클라우드 (Security Group, NSG)
|   +-- K8s NetworkPolicy
|   +-- 서비스 메시 (Istio)
+-- 연계
    +-- Zero Trust 아키텍처
    +-- ZTNA (남북 트래픽)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[VLAN 세그먼테이션 (1990s)]
부서 간 분리
변경 어려움
      |
      v
[SDN 등장 (2010s)]
소프트웨어 정의 네트워크
동적 정책 적용
      |
      v
[마이크로 세그먼테이션 (2012~)]
워크로드 단위 격리
VMware NSX, Illumio
      |
      v
[Zero Trust 아키텍처 (2018~)]
NIST SP 800-207
마이크로 세그먼테이션 핵심 기술
      |
      v
[현재: 서비스 메시+eBPF]
Cilium, Istio
eBPF 기반 고성능 정책
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 전통 방화벽 = 성벽 — 성문(방화벽) 통과하면 내부 자유. 마이크로 세그먼테이션은 건물마다 별도 출입증!
2. K8s NetworkPolicy = 아파트 인터폰 통제 — "앱 파드(302호)만 DB 파드(101호) 전화 가능". 나머지 자동 차단!
3. 금융 적용 결과 = 방화 구역 — 랜섬웨어 침투해도 1대만 격리. 기존 4시간 전사 확산 차단!
