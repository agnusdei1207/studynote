---
title: "DevOps Cloud Integrated Keyword Summary"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 371
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DevOps/SRE와 클라우드 영역의 심화 학습은 개별 기술 암기보다 "왜 이 기술을 선택했는가, 어떤 트레이드오프가 있는가"를 논리적으로 서술하는 능력을 측정하며, 각 개념이 어떤 문제를 해결하기 위해 등장했는지를 연결하는 것이 핵심이다.
> 2. **가치**: CI/CD -> IaC -> 컨테이너/K8s -> 서비스 메시 -> 옵저버빌리티 -> SRE/SLO -> 카오스 엔지니어링으로 이어지는 DevOps 발전 흐름을 하나의 스토리로 연결하면, 개별 문제에서 통합 아키텍처 답안을 구성할 수 있다.
> 3. **판단 포인트**: 학습 정리에서는 장점만 나열하는 것이 아니라 "이 기술의 적합한 조건, 부적합한 조건, 그리고 한계"를 명시해야 심사관이 전문성을 인정한다.

---

## Ⅰ. DevOps/SRE 핵심 키워드 맵

DevOps는 개발(Dev)과 운영(Ops)의 장벽을 제거해 소프트웨어 전달 속도와 신뢰성을 동시에 높이는 문화·프랙티스·도구의 집합이다. SRE (Site Reliability 엔진ering)는 SLO/SLI/SLA 기반 에러 버짓(Error Budget)으로 안정성과 혁신 속도의 균형을 수치화한다.

<strong>CI/CD 파이프라인 핵심</strong>:
- CI (Continuous Integration): 코드 병합 시 자동 빌드·테스트. 도구: GitHub Actions, Jenkins, GitLab CI
- CD (Continuous Delivery): 언제든지 릴리즈 가능한 상태 유지
- 배포 전략: Blue-Green, Canary, Rolling Update

<strong>IaC (Infrastructure as Code)</strong>:
- Terraform: 멀티클라우드 선언적 인프라 프로비저닝
- Ansible: 에이전트리스 구성 관리, YAML Playbook

- 📢 섹션 요약 비유: DevOps는 주방과 홀 직원이 실시간으로 소통하는 레스토랑이다. 요리사(개발)가 새 메뉴를 만들면 홀(운영)이 바로 손님에게 제공하며, 불만이 생기면 즉시 주방으로 피드백이 간다.

---

## Ⅱ. 컨테이너/쿠버네티스 핵심 키워드

```text
+------------------------------------------------------------------+
|              K8s 핵심 구성 요소 요약                             |
+------------------------------------------------------------------+
|  Control Plane: kube-apiserver, etcd, scheduler, controller-mgr  |
|  Worker Node: kubelet, kube-proxy, Container Runtime (containerd)|
|  핵심 오브젝트: Pod, Deployment, Service, Ingress, ConfigMap     |
|  스케일링: HPA (CPU/메트릭), VPA (메모리), KEDA (이벤트 기반)   |
|  스토리지: PV/PVC, StorageClass (동적 프로비저닝), CSI 드라이버 |
|  네트워킹: CNI (Cilium, Calico, Flannel), Service Mesh (Istio)  |
+------------------------------------------------------------------+
```

<strong>서비스 메시 (Istio, Linkerd)</strong>:
- mTLS 자동 암호화, 트래픽 제어, Retry/Timeout/Circuit Breaker
- 분산 추적(Jaeger), 메트릭 수집(Prometheus), 가시성 제공

- 📢 섹션 요약 비유: Kubernetes는 컨테이너 오케스트라 지휘자다. 수백 개 악기(컨테이너)의 배치, 시작, 종료, 재시작을 자동으로 관리한다.

---

## Ⅲ. 옵저버빌리티 & SRE 핵심 키워드

<strong>옵저버빌리티 3대 지주</strong>:
- Metrics (메트릭): Prometheus + Grafana. RED 메트릭(Rate/Errors/Duration)
- Logs (로그): ELK Stack (Elasticsearch + Logstash + Kibana), Loki + Grafana
- Traces (추적): Jaeger, Zipkin, OpenTelemetry

<strong>SRE 핵심 지표</strong>:
- SLI (Service Level Indicator): 측정 가능한 지표 (가용성 %, 레이턴시 p99)
- SLO (Service Level Objective): 목표치 (99.9% 가용성)
- Error Budget: SLO에서 허용하는 오류 허용치 (100% - SLO%)

<strong>카오스 엔지니어링</strong>: Netflix Chaos Monkey, Chaos Mesh, Litmus로 프로덕션 장애 발생 전 시스템 약점을 발견한다.

- 📢 섹션 요약 비유: 옵저버빌리티는 자동차 계기판이다. 속도(메트릭), 경고 메시지(로그), GPS 경로(추적)가 함께 있어야 운전자(SRE)가 안전하게 운영한다.

---

## Ⅳ. 클라우드 아키텍처 핵심 패턴

**고가용성 패턴**:
- Circuit Breaker (Resilience4j): 연속 장애 시 빠른 실패 복귀
- Retry + Exponential Backoff + Jitter: 재시도 폭풍 방지
- Bulkhead: 서비스별 스레드풀 격리로 장애 전파 방지
- Saga Pattern: 분산 트랜잭션 보상 로직

<strong>클라우드 네이티브 12-Factor App</strong>: 코드베이스 단일화, 의존성 명시, 설정 환경변수 분리, 무상태 프로세스, 포트 바인딩, 로그 스트림 등.

- 📢 섹션 요약 비유: Circuit Breaker는 전기 두꺼비집이다. 과부하(연속 장애)가 걸리면 자동으로 차단해 전체 회로(시스템)를 보호한다.

---

## Ⅴ. 보안(DevSecOps) 핵심 키워드

<strong>SAST/DAST/SCA</strong>:
- SAST (Static AST): 소스코드 취약점 분석 (SonarQube)
- DAST (Dynamic AST): 실행 중 취약점 분석 (OWASP ZAP)
- SCA (Software Composition Analysis): 오픈소스 라이브러리 취약점 (Snyk)

<strong>Zero Trust</strong>: Never Trust, Always Verify 원칙. mTLS, SPIFFE/SPIRE로 서비스 간 신원 증명.

<strong>공급망 보안</strong>: SBOM (Software Bill of Materials), Cosign + Sigstore, SLSA (Supply chain Levels for Software Artifacts).

- 📢 섹션 요약 비유: DevSecOps에서 SBOM은 식품 성분표이다. 소프트웨어에 어떤 오픈소스 재료(라이브러리)가 들어있는지 명시해, 특정 재료에 문제가 생기면 즉시 확인·교체할 수 있다.

---

### 📌 관련 개념 맵

| 개념                              | 연결 포인트                                               |
| :-------------------------------- | :-------------------------------------------------------- |
| SRE / Error Budget                | SLO 기반 신뢰성과 개발 속도 균형 수치화                  |
| GitOps (Argo CD, Flux)            | Git을 단일 진실의 원천으로 K8s 상태 선언적 관리          |
| FinOps                            | 클라우드 비용 최적화                                     |
| Platform 엔진ering              | 내부 개발자 플랫폼(IDP), 셀프서비스 인프라               |
| OpenTelemetry                     | 메트릭·로그·추적 통합 관측성 표준                        |
| SLSA / SBOM                       | 소프트웨어 공급망 보안 성숙도 프레임워크                 |

### 📈 관련 키워드 및 발전 흐름도

```text
Agile + CI/CD (개발·배포 자동화)
    |
    v
IaC + GitOps (인프라 코드화, 선언적 관리)
    |
    v
컨테이너 / K8s (불변 인프라, 오케스트레이션)
    |
    v
서비스 메시 + 옵저버빌리티 (가시성, mTLS)
    |
    v
SRE + Error Budget (신뢰성 수치화)
    |
    v
Platform Engineering + FinOps (내부 플랫폼화, 비용 최적화)
    |
    v
AI-assisted DevOps (자율 장애 탐지·복구)
```

### 👶 어린이를 위한 3줄 비유 설명

1. DevOps는 요리사(개발자)와 웨이터(운영자)가 팀을 이뤄 손님에게 최고의 서비스를 빠르게 전달하는 방식이에요.
2. SRE는 레스토랑이 얼마나 자주 문제가 생겨도 되는지(에러 버짓)를 숫자로 정해서 혁신과 안정성을 균형 있게 관리해요.
3. 옵저버빌리티는 주방 CCTV(로그), 온도계(메트릭), 배달 추적(추적)이 모두 있어야 음식이 왜 문제가 생겼는지 알 수 있는 것과 같아요.
