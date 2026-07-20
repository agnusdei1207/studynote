---
title: "Cloud Native"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 40
---
> **핵심 인사이트**
> 1. 클라우드 네이티브(Cloud Native)는 단순히 클라우드에서 실행되는 것이 아니라, 클라우드의 탄력성·자동화·분산성을 최대한 활용하도록 **설계부터** 클라우드를 위해 만들어진 애플리케이션/아키텍처 방식이다.
> 2. CNCF(Cloud Native Computing Foundation)의 정의에 따르면, 마이크로서비스·컨테이너·동적 오케스트레이션·지속적 전달(CI/CD)의 4대 기둥이 클라우드 네이티브의 핵심이며, 12-Factor App이 구현 원칙의 표준이다.
> 3. Cloud Native vs Cloud-Enabled(기존 앱을 클라우드로 이전)의 차이가 핵심으로, Cloud-Enabled는 클라우드 비용은 쓰지만 클라우드 탄력성 이점은 못 누리는 "리프트앤시프트(Lift-and-Shift)" 함정에 빠지는 반면, Cloud Native는 스케일 아웃·자동 복구·무중단 배포를 기본 내장한다.

---

## Ⅰ. Cloud Native 4대 기둥

```
CNCF Cloud Native 정의의 4대 요소:

1. 컨테이너 (Container):
   Docker 이미지로 환경 표준화
   "어디서든 동일하게 실행"
   불변 인프라 (Immutable Infrastructure)

2. 마이크로서비스 (Microservices):
   기능별로 독립 배포 가능한 서비스 분리
   각 서비스 독립적 스케일링
   장애 격리 (Fault Isolation)

3. 동적 오케스트레이션 (Dynamic Orchestration):
   Kubernetes: 컨테이너 배치, 확장, 복구 자동화
   선언적 관리 (Desired State)
   자가 치유 (Self-healing)

4. DevOps / CI/CD:
   코드 변경 -> 자동 빌드/테스트/배포
   지속적 통합/전달 파이프라인
   "배포는 이벤트가 아닌 일상"
```

> 📢 **섹션 요약 비유**: Cloud Native 4대 기둥은 현대 아파트 구조 — 컨테이너(독립 세대), 마이크로서비스(분리된 공간), 쿠버네티스(아파트 관리시스템), CI/CD(자동 시설 점검).

---

## Ⅱ. 12-Factor App

```
12-Factor App (Heroku, 2011):
클라우드 네이티브 앱 설계 원칙

핵심 12가지:
  1. Codebase:   단일 코드베이스, 여러 배포
  2. Dependencies: 의존성 명시적 선언
  3. Config:     환경 변수로 설정 (코드 분리)
  4. Backing Services: DB/캐시를 교체 가능 리소스로
  5. Build/Release/Run: 빌드·릴리즈·실행 단계 분리
  6. Processes:  무상태(Stateless) 프로세스
  7. Port Binding: 포트로 서비스 노출
  8. Concurrency: 프로세스 모델로 수평 확장
  9. Disposability: 빠른 시작, 우아한 종료 (SIGTERM)
  10. Dev/Prod Parity: 개발/스테이징/운영 환경 동일
  11. Logs:      로그를 이벤트 스트림으로 처리
  12. Admin Processes: 일회성 관리 작업 분리 실행

핵심 원칙:
  상태는 외부(DB, Redis)에 저장
  서버는 언제든 죽어도 되는 가축(Cattle not Pets)
```

> 📢 **섹션 요약 비유**: 12-Factor App은 레고 블록 조립 원칙 — 각 블록이 표준화되어 있어야 어디든 끼워 맞추고 쉽게 교체할 수 있다.

---

## Ⅲ. Cloud Native vs Cloud-Enabled

```
비교:
  구분          Cloud Native         Cloud-Enabled
  설계 시점      클라우드 위해 설계    기존 앱을 클라우드로 이전
  아키텍처       마이크로서비스        모노리식 유지
  배포 방식      컨테이너/K8s         VM에 직접 설치
  스케일링       자동 수평 확장        수동 또는 제한적
  장애 복구      자가 치유 (Self-heal) 수동 재시작
  업데이트       무중단 롤링 배포      유지보수 창 필요
  비용 최적화    사용량 기반 (Pay-as-you-go) 예약 용량 기반

리프트앤시프트 함정:
  VM에 올렸다고 클라우드 이점 없음
  오히려 관리 복잡도 증가, 비용 증가
  -> Re-architecture 필요

적합 전략:
  레거시: 먼저 Lift-and-Shift -> 단계적 Cloud Native 전환
  신규: 처음부터 Cloud Native 설계
```

> 📢 **섹션 요약 비유**: Cloud Native vs Cloud-Enabled는 전기차 vs 엔진 개조 — 전기차(Native)는 처음부터 전기에 최적화, 개조차는 배터리 달았지만 원래 구조의 한계가 있다.

---

## Ⅳ. Kubernetes 핵심 개념

```
Kubernetes (K8s) Cloud Native 오케스트레이션:

핵심 리소스:
  Pod:         컨테이너 실행 단위 (1~N 컨테이너)
  Deployment:  Pod 복제본 관리 + 롤링 업데이트
  Service:     Pod 집합에 고정 IP/DNS 부여
  Ingress:     외부 트래픽 라우팅 규칙
  ConfigMap:   설정 데이터 (12-Factor Config)
  Secret:      민감 데이터 암호화 저장

Cloud Native 패턴:
  Auto-scaling:
    HPA (Horizontal Pod Autoscaler)
    CPU 사용률 80% -> 자동 Pod 수 증가

  Self-healing:
    Pod 죽으면 -> K8s가 자동 재시작
    노드 장애 -> 다른 노드로 Pod 재배치

  Rolling Update:
    v1 -> v2 교체 시 트래픽 무중단 유지
    문제 시 자동 롤백
```

> 📢 **섹션 요약 비유**: Kubernetes는 레스토랑 자동화 매니저 — 주문(요청) 많아지면 요리사(Pod) 추가 고용, 요리사 쓰러지면 바로 대체.

---

## Ⅴ. 실무 시나리오 — 금융 서비스 Cloud Native 전환

```
금융 서비스 A사 Cloud Native 전환 사례:

기존 상황 (모노리식):
  단일 Java EE 애플리케이션 (10년 레거시)
  배포 주기: 분기 1회 (2주 테스트 필요)
  장애 복구: 2~4시간 소요
  스케일: 수동 서버 증설 (2주 소요)

단계적 전환 전략:
  1단계 (6개월): 컨테이너화
     Docker 이미지 변환, K8s 도입
     -> 배포 주기 주 1회로 단축

  2단계 (1년): 마이크로서비스 분리
     결제, 계좌, 알림 서비스 분리
     각 서비스 독립 배포 가능

  3단계 (6개월): 완전 Cloud Native
     CI/CD 파이프라인 자동화
     HPA 자동 확장 설정
     배포 주기: 일 3회 이상

결과:
  배포 빈도: 분기 -> 하루 3회 (+50배)
  장애 복구: 4시간 -> 5분 (MTTR 98% 감소)
  인프라 비용: 30% 절감 (자동 스케일 다운)
  개발 생산성: 팀당 독립 배포 (의존성 제거)
```

> 📢 **섹션 요약 비유**: Cloud Native 전환은 대형 백화점을 독립 가게 거리(마이크로서비스)로 바꾸기 — 한 가게 화재가 전체 백화점을 닫는 일이 없어진다.

---

## 📌 관련 개념 맵

```
클라우드 네이티브 (Cloud Native)
+-- CNCF 4대 기둥
|   +-- 컨테이너 (Docker)
|   +-- 마이크로서비스
|   +-- K8s (동적 오케스트레이션)
|   +-- CI/CD (DevOps)
+-- 설계 원칙
|   +-- 12-Factor App
|   +-- 불변 인프라, Stateless
+-- 비교
|   +-- Cloud-Enabled (Lift-and-Shift)
|   +-- 모노리식 vs 마이크로서비스
+-- 도구 생태계
    +-- Docker, Kubernetes
    +-- Helm, Istio, Prometheus
    +-- GitHub Actions, ArgoCD
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[가상화 (VMware, 2001)]
물리 서버 추상화
      |
      v
[AWS EC2 (2006)]
퍼블릭 클라우드 시작
      |
      v
[12-Factor App (Heroku, 2011)]
클라우드 네이티브 원칙 정의
      |
      v
[Docker (2013)]
컨테이너 표준화 혁명
      |
      v
[Kubernetes (Google, 2014)]
컨테이너 오케스트레이션 표준
CNCF 설립 (2015)
      |
      v
[현재: 클라우드 네이티브 기본값]
Serverless, eBPF, Service Mesh 발전
플랫폼 엔지니어링(Platform Engineering) 부상
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 네이티브는 물고기가 물속에 맞게 설계된 것처럼, 앱이 클라우드에 맞게 처음부터 설계된 방식이에요.
2. 레고 블록처럼 각 기능을 독립적으로 만들어서 한 블록이 망가져도 전체가 무너지지 않게 하는 것이 마이크로서비스예요.
3. 쿠버네티스는 레고 자동 조립 로봇 — 필요할 때 블록을 더 붙이고(자동 확장), 부서진 블록은 바로 교체해줘요(자가 치유)!
