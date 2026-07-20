---
title: "Cloud Native 12 Factor Design Principles"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 614
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 12팩터 앱은 **단일 코드베이스, 선언적 의존성, 환경변수 기반 설정, 외부 리소스 추상화, 빌드/릴리스/런 분리, 무상태 프로세스, 포트 바인딩, 수평 확장, 빠른 기동/종료, Dev-Prod 패리티, 이벤트 스트림 로그, 1회성 관리 프로세스**라는 12개 원칙으로 SaaS 애플리케이션의 클라우드 네이티브 적합성을 정의한 방법론이다.
> 2. **가치**: 컨테이너 오케스트레이션(K8s) 환경에서 **무중단 배포(Zero-downtime deployment)**, **자동 스케일링(Auto-scaling)**, **장애 격리(Blast radius reduction)**를 가능케 하여, 통상 배포 리드타임을 **수일 -> 수 분**, 인프라 활용률을 **15~25% -> 60~80%** 수준으로 개선한다.
> 3. **판단 포인트**: 12팩터를 무비판적으로 적용하면 **상태 영속성(세션, 파일) 처리**, **레거시 모놀리식 시스템의 점진적 이관**, **강한 트랜잭션 일관성(Strong consistency) 요구 도메인**에서 역효과가 발생하므로, 도메인 특성(MSA 적합성, 데이터 일관성 모델, 트래픽 패턴)에 따라 **15-Factor, Beyond 12-Factor**로 확장 적용 여부를 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

2000년대 후반 Heroku 엔지니어링팀(Adam Wiggins, James Lindenbaum, Mark McGranaghan, Owen Qian 등)은 당시 통상적인 LAMP 스택 웹앱이 **배포 시 환경 차이로 인한 장애**, **수직 확장의 한계**, **개발-운영 간 불일치로 인한 Hotfix 폭주**라는 고질적 문제에 직면했다. 이를 해결하기 위해 2011년 "The Twelve-Factor App" 백서를 발표하였고, 이후 Pivotal(현 VMware Tanzu), CNCF, Cloud Foundry, Red Hat OpenShift 등이 사실상 표준으로 채택하며 PaaS/CaaS 시대의 설계 철학으로 정착되었다.

본질적으로 12팩터는 **"어떻게 빌드하느냐"가 아니라 "어떻게 운영하느냐"에 관한 원칙**이다. 즉, 애플리케이션 코드 품질이 아니라 **런타임 거동(Runtime Behavior)**에 초점을 맞추며, 클라우드 인프라(특히 컨테이너 오케스트레이터)가 애플리케이션에 요구하는 **계약(Contract)**을 명시한 것이다.

```text
[12-Factor App: 패러다임 전환의 구조]

   +--------------------------------------------------------------+
   |           Traditional LAMP/Java EE Application               |
   |  +----------------------------------------------------+     |
   |  |  App Code  |  Config (XML/properties)              |     |
   |  |            |  + Local Library (.jar, .dll)         |     |
   |  |            |  + Web/App Server (Tomcat, JBoss)     |     |
   |  |  +--------------------------------------+          |     |
   |  |  |   State: Session in JVM Heap        |          |     |
   |  |  |   Files: /var/log, /uploads, /tmp   |          |     |
   |  |  |   DB Connection: Pool in-process    |          |     |
   |  |  +--------------------------------------+          |     |
   |  +----------------------------------------------------+     |
   |   v 배포: WAR/EAR 단일 패키지 -> 수동 rsync -> 서버 재기동     |
   |   v 확장: Scale-Up (CPU/RAM 추가) -> 단일 노드 한계           |
   |   v 장애: 노드 장애 시 세션 손실, 수동 복구                    |
   +--------------------------------------------------------------+
                          ⇩ 패러다임 전환 (Cloud Native)
   +--------------------------------------------------------------+
   |              12-Factor Cloud Native Application               |
   |  +----------------------------------------------------+     |
   |  |  Codebase (Git) --► Build (OCI Image)             |     |
   |  |       |                  |                         |     |
   |  |       v                  v                         |     |
   |  |  Deps (manifest)   Release (Image+Config)         |     |
   |  |  (package.json,         |                         |     |
   |  |   requirements.txt)    v                         |     |
   |  |                    Run (Container)               |     |
   |  |   +--------------------------------------+      |     |
   |  |   | Stateless Process (PID 1 = app)     |      |     |
   |  |   |  ^                ^                 |      |     |
   |  |   |  | Port Binding   | Logs to STDOUT  |      |     |
   |  |   |  +-► HTTP :8080  +-► Fluentd/Loki   |      |     |
   |  |   +--------------------------------------+      |     |
   |  |   ^          ^         ^         ^                |     |
   |  |   |          |         |         |                |     |
   |  |   Redis   PostgreSQL   S3      RabbitMQ  (백킹서비스) |     |
   |  |   (URL로 추상화, 환경변수로 주입)                       |     |
   |  +----------------------------------------------------+     |
   |   v 배포: Git Push -> CI -> Image Registry -> K8s Rolling Update |
   |   v 확장: Scale-Out (ReplicaSet 1->100) -> HPA 자동 조정       |
   |   v 장애: Pod Reschedule -> Stateless로 즉시 재기동            |
   +--------------------------------------------------------------+
```

기존 모놀리식/서버 중심 모델에서는 **"앱이 서버에 설치되는 것"**이 전제였지만, 12팩터는 **"앱이 환경과 분리된 독립 실행 단위이며, 모든 의존성과 설정이 외부화되어 어디서든 동일하게 동작"**함을 전제로 한다. 이는 **Infrastructure as Code(IaC)**, **GitOps**, **Observability(3 pillars)**, **eBPF 기반 런타임** 등 현대 클라우드 생태계의 근간이 된다.

- **📢 섹션 요약 비유**: 12팩터는 마치 **"이사 가방 없이도 어느 호텔에 들어가도 즉시 생활 가능한 미니멀리스트"**와 같다. 옷은 옷장에, 음식은 냉장고에, TV는 리모컨 한 개로 — 호텔(HTTP 포트)만 바뀌어도 똑같이 동작한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

12팩터는 독립적인 12개 원칙이지만, 실제로는 **빌드 파이프라인(Ⅰ~Ⅲ)** -> **런타임 거동(Ⅳ~Ⅶ)** -> **운영 거버넌스(Ⅷ~Ⅻ)**의 3개 계층으로 유기적으로 연결된다.

```text
[12-Factor 전체 아키텍처 및 데이터/제어 흐름]

  +------------ ① 코드베이스 ------------+
  | 1 Repo = N Deploys (dev/stg/prod)   |
  |   +--------------------------+      |
  |   |  main / feature/* 브랜치  |      |
  |   |  + GitOps: ArgoCD/Flux   |      |
  |   +--------------------------+      |
  +--------------+-----------------------+
                 v
  +------------ ② 의존성 ---------------+
  | 선언적 manifest:                     |
  |   - package.json (npm)              |
  |   - requirements.txt / Pipfile      |
  |   - go.mod / pom.xml / build.gradle |
  |   - Cargo.toml / Gemfile            |
  | 격리: venv, virtualenv, bundler,    |
  |       container (OCI layers)        |
  +--------------+-----------------------+
                 v
  +------------ ⑤ 빌드/릴리스/런 --------+  +-----------------+
  |  Build   ->  Release  ->   Run        |  | ③ 설정          |
  | (Compile)  (Image+Env)  (Container) |◄-+ Env Vars:       |
  |   |           |             |      |  |  DATABASE_URL   |
  |   |           |             |      |  |  REDIS_URL      |
  |   |      Config Map/       |      |  |  AWS_*_KEY      |
  |   |      Secret Mount      |      |  +-----------------+
  +--------------+-----------------------+
                 v
  +------------ ⑥/⑦/⑧ 프로세스·포트·동시성 ----+
  |  +-------+  +-------+  +-------+         |
  |  | Pod A |  | Pod B |  | Pod C | Scale-out|
  |  |:8080  |  |:8080  |  |:8080  | ◄--HPA-- |
  |  |Statel.|  |Statel.|  |Statel.|         |
  |  +---+---+  +---+---+  +---+---+         |
  |      |          |          |              |
  +------+----------+----------+--------------+
         v          v          v
  +------------ ④ 백킹 서비스 -------------+
  |  URL로 추상화된 외부 리소스:              |
  |  +------+ +------+ +------+ +------+ |
  |  |PG DB | |Redis | |  S3  | |Kafka | |
  |  +--+---+ +--+---+ +--+---+ +--+---+ |
  |     +--------+--------+--------+     |
  |         자원 교환 가능 (Adapter 패턴)   |
  +-----------------------------------------+
         |          |          |
         v          v          v
  +------------ ⑪ 로그 (Event Stream) -----+
  |  STDOUT/STDERR -> Promtail/Fluentd      |
  |              -> Loki / Elasticsearch    |
  |              -> Grafana / Kibana 대시보드|
  +-----------------------------------------+

  +------------ ⑨ 폐기 가능성 -------------+
  |  Startup: < 1s (Spring->Quarkus/Native)|
  |  Shutdown: SIGTERM -> drain -> exit     |
  |  K8s: preStop hook + gracePeriod      |
  +-----------------------------------------+

  +------------ ⑩ Dev/Prod Parity --------+
  |  동일 이미지, 동일 마이그레이션 도구,   |
  |  동일 시드 데이터 정책, 동일 시크릿 매니저|
  +-----------------------------------------+

  +------------ ⑫ 관리 프로세스 -----------+
  |  REPL / kubectl exec / Job (一次性)    |
  |  DB 마이그레이션, 배치 작업, REPL      |
  |  = 동일 환경에서 동일 이미지로 실행    |
  +-----------------------------------------+
```

### 12팩터 각 요소의 상세 기술 매핑

| # | 팩터 (Factor) | 기술적 역할 | 핵심 구현 기술 및 동작 방식 |
| :--- | :--- | :--- | :--- |
| Ⅰ | **Codebase** | 단일 진실 원천(Single Source of Truth) | **Git(Monorepo 또는 Polyrepo) + GitOps(ArgoCD/Flux)**. 한 저장소가 dev/stg/prod의 *다중 배포(Deploys)*를 생성. CI 단계에서 동일 SHA로 빌드된 이미지를 모든 환경에 promote. |
| Ⅱ | **Dependencies** | 선언적·격리된 의존성 관리 | **Manifest 파일(package.json, requirements.txt, go.mod, pom.xml) + Lock file(package-lock.json, Pipfile.lock)**. 격리는 **Virtual Env(venv)** -> **컨테이너 레이어(OCI Image, multi-stage build)**로 발전. CVE 스캔은 **Trivy, Snyk, Grype**. |
| Ⅲ | **Config** | 코드와 설정의 엄격한 분리 | **12-factor 원칙: 설정은 환경변수(Env Vars)에 저장**. K8s 환경에서는 **ConfigMap(평문) + Secret(베이스64, 가능하면 SealedSecret/External Secrets Operator로 Vault 연동)**. **Spring Cloud Config, HashiCorp Consul+Envconsul**도 사용. **※ 코드에 있는 설정은 위반(antipattern)**. |
| Ⅳ | **Backing Services** | 외부 리소스의 등급화 제거 | DB, 캐시, 메시지 브로커, SMTP, S3를 모두 *URL 한 줄*로 추상화: `postgresql://user:pwd@host:5432/db`. **Adapter 패턴**(Repository, DataSource)으로 교체 가능. 컨테이너화 시 사이드카(Sidecar, e.g. Dapr) 활용. |
| Ⅴ | **Build, Release, Run** | 3단계 엄격 분리 + 불변 릴리스 | **Build**: 소스->아티팩트(이미지). **Release**: 아티팩트+설정=불변(Immutable) 배포 단위. **Run**: 실행 환경에서 릴리스를 프로세스로 기동. **롤백은 새 릴리스 배포로만** (in-place 패치 금지). **Helm Chart values, Kustomize overlay**가 릴리스 단위. |
| Ⅵ | **Processes** | 무상태(Stateless) 프로세스 모델 | **인메모리 상태/디스크/세션 일체 금지**. 모든 상태는 백킹 서비스(Redis, DB)로 위임. **sticky session, local file cache, JVM heap의 BigObject** 모두 위반. 영속 데이터는 **Volume(PV/PVC) 또는 외부 스토리지(S3, EBS CSI Driver)**. |
| Ⅶ | **Port Binding** | 자가 포함(Self-contained) HTTP 서비스 | 웹앱이 **Tomcat 같은 외부 WAS에 의존하지 않고** 앱 프로세스가 직접 포트(:8080)를 바인딩. K8s에서는 **Service spec.ports, liveness/readiness probe**로 노출. **Health endpoint(actuator/health, /healthz, /readyz)** 필수. |
| Ⅷ | **Concurrency** | 프로세스 모델을 통한 수평 확장 | **다중 프로세스 타입**(web, worker, scheduler)을 **다중 컨테이너/Deployment**로 모델링. 확장은 **ReplicaSet + HPA(Horizontal Pod Autoscaler)** — CPU/메모리/custom metric(KEDA) 기반. **반대개념: 스레드 기반 수직확장은 한계**. |
| Ⅸ | **Disposability** | 빠른 기동·우아한 종료 | **Cold start ≤수 초**(JVM->GraalVM Native Image로 수십 ms, Node.js는 기본 빠름). **SIGTERM 수신 시 in-flight request drain -> DB connection close -> exit 0**. K8s `terminationGracePeriodSeconds`, `preStop hook`으로 무중단 배포 보장. |
| Ⅹ | **Dev/Prod Parity** | 환경 간 일치성 극대화 | **시간 차이**(코드-배포 간격 단축: CI/CD), **인적 차이**(Dev 작성자=Prod 운영자, "벽 없는 DevOps"), **도구 차이**(동일 컨테이너 이미지, 동일 마이그레이션 도구: Flyway, Liquibase). **Docker Compose, Skaffold, Tilt**로 로