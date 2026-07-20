---
title: "Resource Allocation"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
weight: 41
---
> **핵심 인사이트**
> 1. 자원 할당(Resource Allocation)은 OS의 핵심 기능으로, CPU·메모리·I/O 장치·파일 등 한정된 자원을 여러 프로세스에 공정하고 효율적으로 분배하는 문제이며, 잘못된 할당은 교착상태(Deadlock)·기아(Starvation)·스래싱(Thrashing)을 유발한다.
> 2. 자원 할당의 핵심 트레이드오프는 공정성(Fairness)·처리율(Throughput)·응답시간(Response Time)·이용률(Utilization) 간의 균형으로, 어떤 스케줄링 정책도 모든 기준을 동시에 최적화할 수 없다.
> 3. 교착상태 예방을 위한 은행원 알고리즘(Banker's Algorithm)과 RAG(Resource Allocation Graph)는 자원 할당의 안전성을 형식적으로 검증하는 핵심 도구로, OS 설계의 안전성·활성성(Liveness) 보장 메커니즘이다.

---

## Ⅰ. 자원 할당 기본 개념

```
자원 유형:
  선점 가능 (Preemptible): CPU, 메모리
    프로세스에서 강제 회수 후 재할당 가능
  선점 불가 (Non-preemptible): CD-ROM, 프린터
    작업 완료 후만 반환 가능

자원 요청 단계:
  1. 요청 (Request): 프로세스가 자원 요청
  2. 사용 (Use): 할당 후 자원 사용
  3. 반환 (Release): 사용 완료 후 자원 반환

할당 정책 목표:
  공정성:     모든 프로세스에 기회 보장
  효율성:     자원 유휴 시간 최소화
  우선순위:   중요 프로세스 먼저 처리
  안전성:     교착상태, 기아 방지
```

> 📢 **섹션 요약 비유**: 자원 할당은 도서관 좌석 배정 — 모든 학생이 공평하게 자리를 쓸 수 있도록 규칙이 필요하다.

---

## Ⅱ. RAG (Resource Allocation Graph)

```
자원 할당 그래프 (Resource Allocation Graph):

노드:
  원형: 프로세스 (P1, P2, P3)
  사각형: 자원 유형 (R1, R2)
  점: 자원 인스턴스

간선 (Edge):
  요청 간선: P -> R (프로세스가 자원 요청)
  할당 간선: R -> P (자원이 프로세스에 할당됨)

교착상태 탐지:
  단일 인스턴스 자원: 사이클 = 교착상태
  복수 인스턴스 자원: 사이클 + 추가 검사 필요

예시 (교착상태):
  P1 --요청--> R1 <--할당-- P2
  P2 --요청--> R2 <--할당-- P1
  -> 사이클 존재 -> 교착상태

예시 (교착상태 아님):
  P1 --요청--> R1 (인스턴스 2개, 1개 사용 중)
  -> R1에 여유 인스턴스 있음 -> 해결 가능
```

> 📢 **섹션 요약 비유**: RAG는 식사하는 철학자 문제 지도 — 누가 어떤 젓가락을 잡고, 누가 기다리는지 그림으로 그려 교착상태 탐지.

---

## Ⅲ. 은행원 알고리즘

```
Banker's Algorithm (Dijkstra):

전제:
  - 자원 총량 알려짐 (Max 배열)
  - 각 프로세스 최대 필요량 사전 선언
  - 실제 필요량 <= 최대 필요량

안전 상태 (Safe State):
  모든 프로세스 완료 가능한 순서가 존재
  안전 순서열 (Safe Sequence) 찾기

알고리즘:
  1. 완료 가능한 프로세스 찾기:
     Finish[i] = false이고
     Need[i] <= Work 인 프로세스
  2. Work += Allocation[i], Finish[i] = true
  3. 모든 Finish = true이면 안전 상태

안전 순서열 탐색:
  Work = Available (현재 여유 자원)
  Finish[0..n-1] = false

  반복: Work += Allocation[i] if Need[i] <= Work
  모두 Finish = true -> 안전

할당 시 검사:
  새 자원 할당 후 안전 상태인지 검사
  안전하면 할당, 불안전하면 대기
```

> 📢 **섹션 요약 비유**: 은행원 알고리즘은 대출 심사 — "모든 고객이 대출 상환할 수 있는 순서가 있는가?"를 확인하고 안전할 때만 대출 승인.

---

## Ⅳ. 자원 할당 문제들

```
교착상태 (Deadlock):
  조건 (4가지 모두 성립 시):
    1. 상호 배제 (Mutual Exclusion)
    2. 점유와 대기 (Hold and Wait)
    3. 선점 불가 (No Preemption)
    4. 순환 대기 (Circular Wait)

처리 방법:
  예방 (Prevention): 4조건 중 하나 제거
  회피 (Avoidance): 은행원 알고리즘
  탐지 (Detection): RAG 분석, 주기적 검사
  회복 (Recovery): 프로세스 종료, 자원 선점

기아 (Starvation):
  낮은 우선순위 프로세스 무한 대기
  해결: 에이징 (Aging) — 대기 시간에 따라 우선순위 상향

스래싱 (Thrashing):
  페이지 폴트 과다 -> CPU 효율 급락
  해결: 워킹 셋(Working Set) 모델
```

> 📢 **섹션 요약 비유**: 교착상태는 사거리 4방향 동시 진입 차량 — 아무도 양보 안 하면 영원히 막힌다. 은행원 알고리즘은 교통 경찰이 미리 통제.

---

## Ⅴ. 실무 시나리오 — 클라우드 자원 할당

```
클라우드 멀티테넌트 자원 할당:

문제:
  수천 VM이 동일 물리 호스트 공유
  CPU·메모리·네트워크 대역폭 경쟁

할당 정책:

CPU:
  CFS (Completely Fair Scheduler):
    각 VM에 가중치 비례 CPU 시간 할당
    우선순위: vCPU Weight 설정 (1~100)

메모리:
  Balloon Driver: 여유 VM에서 메모리 회수
  메모리 과다 할당(Overcommit): 80% 실제 사용 가정
  KSM (Kernel Samepage Merging): 중복 페이지 공유

네트워크:
  cgroups 기반 대역폭 제한
  QoS 정책 (최소 보장 + 최대 제한)

쿠버네티스 자원 관리:
  requests: Pod 최소 보장 자원
  limits: Pod 최대 사용 자원
  QoS Class: Guaranteed / Burstable / BestEffort
```

> 📢 **섹션 요약 비유**: 클라우드 자원 할당은 아파트 공용 주차장 — 각 세대에 기본 자리(requests) 보장, 빈 자리 있으면 추가 사용(limits) 가능.

---

## 📌 관련 개념 맵

```
자원 할당 (Resource Allocation)
+-- 자원 유형
|   +-- 선점 가능 (CPU, 메모리)
|   +-- 선점 불가 (I/O, 프린터)
+-- 도구
|   +-- RAG (Resource Allocation Graph)
|   +-- 은행원 알고리즘
+-- 문제
|   +-- 교착상태 (Deadlock)
|   +-- 기아 (Starvation)
|   +-- 스래싱 (Thrashing)
+-- 클라우드 적용
    +-- Kubernetes requests/limits
    +-- cgroups, CFS 스케줄러
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[다중 프로그래밍 (1960s)]
여러 프로그램 동시 실행
자원 공유 필요성 대두
      |
      v
[은행원 알고리즘 (Dijkstra, 1965)]
교착상태 회피 이론 정립
      |
      v
[Unix 프로세스 관리 (1970s)]
실용적 자원 할당 구현
      |
      v
[가상화 자원 할당 (2000s)]
VMware, Xen 하이퍼바이저
      |
      v
[컨테이너 자원 관리 (2013~)]
cgroups + Kubernetes requests/limits
      |
      v
[현재: AI 워크로드 자원 최적화]
GPU 시간 분할, 동적 자원 조정
FinOps: 비용 최적화 자원 할당
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 자원 할당은 여러 친구들이 한 대의 컴퓨터를 같이 쓸 때 누가 얼마나 쓸 수 있는지 규칙을 정하는 것이에요.
2. 교착상태는 두 사람이 서로 상대방 물건을 가져야 자기 물건을 넘겨주겠다고 버티는 상황 — 은행원 알고리즘이 이를 미리 막아줘요.
3. 클라우드에서는 쿠버네티스가 각 앱에 CPU와 메모리를 배정하고, 너무 많이 쓰면 제한하는 역할을 해요!
