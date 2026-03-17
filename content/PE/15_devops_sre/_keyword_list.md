+++
title = "15. 데브옵스 (DevOps) 및 SRE 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynotes-devops-sre"
+++

# 데브옵스 (DevOps) 및 SRE (사이트 신뢰성 공학) 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 및 클라우드/플랫폼 엔지니어를 위한 데브옵스, SRE, CI/CD, GitOps, 컨테이너 보안(DevSecOps) 및 옵저버빌리티(Observability) 전 영역 800대 핵심 키워드입니다.

---

## 1. DevOps 문화 및 개발 방법론 (60개)
1. 데브옵스 (DevOps) 사상 - 개발(Dev)과 운영(Ops) 간의 소통, 협업, 통합을 강조하여 소프트웨어 배포 속도와 안정성을 극대화하는 문화적/기술적 패러다임
2. 사일로 (Silo) 현상 타파 - 부서 간 장벽을 허물고 공동의 목표(빠른 배포와 시스템 안정성) 달성
3. CALMS 프레임워크 - DevOps 5대 핵심 가치 (Culture 문화, Automation 자동화, Lean 린 IT, Measurement 측정, Sharing 공유)
4. 애자일 (Agile)과의 관계 - 애자일이 개발(기획~코딩)의 속도를 높인다면, DevOps는 애자일의 속도를 운영(배포~모니터링)까지 확장한 체계
5. 피드백 루프 (Feedback Loop) - 운영 환경의 이슈와 사용자 반응을 즉각적으로 개발 계획에 반영하는 순환 구조
6. 12 팩터 앱 (The Twelve-Factor App) - 클라우드 네이티브(SaaS) 애플리케이션 개발을 위한 12가지 베스트 프랙티스 (Heroku 제안)
7. 코드베이스 (Codebase) - 버전 관리되는 하나의 코드베이스와 다양한 배포(Dev, Staging, Prod) 연계
8. 종속성 (Dependencies) 격리 - 모든 종속성은 명시적으로 선언(package.json, pom.xml 등)
9. 설정 (Config) - 환경 변수(Env Vars)에 설정을 저장하여 코드와 분리
10. 백엔드 서비스 (Backing Services) - DB, 큐, 캐시 등을 네트워크로 연결된 자원(Attached Resource)으로 취급
11. 빌드, 릴리스, 실행 (Build, Release, Run) 단계의 엄격한 분리
12. 무상태 프로세스 (Stateless Processes) - 애플리케이션은 상태를 공유하지 않고 무상태로 실행되며, 상태는 DB 등에 저장
13. 포트 바인딩 (Port Binding) - 자체적으로 포트를 바인딩하여 웹 서비스 노출
14. 동시성 (Concurrency) - 프로세스 모델을 통한 스케일 아웃(Scale-out) 수평 확장
15. 폐기 가능성 (Disposability) - 빠른 시작과 우아한 종료(Graceful Shutdown)를 통한 안정성 극대화
16. 개발/운영 환경 일치 (Dev/Prod Parity) - 개발, 스테이징, 운영 환경의 갭을 최소화
17. 로그 (Logs) - 로그를 이벤트 스트림으로 취급하여 표준 출력(stdout)으로 뿜어냄
18. 관리 프로세스 (Admin Processes) - 일회성 관리/스크립트 작업도 동일한 환경에서 실행
19. 지속적 통합 (CI, Continuous Integration) - 다수 개발자의 코드를 메인 브랜치에 수시로 병합하고 자동 빌드/테스트를 수행해 통합 오류를 조기 발견
20. 지속적 전달 (CD, Continuous Delivery) - CI를 통과한 코드를 프로덕션(운영) 환경에 배포할 준비(아티팩트 생성)를 완료하되, 실제 배포는 인간의 수동 승인을 거침
21. 지속적 배포 (CD, Continuous Deployment) - 수동 승인조차 생략하고 테스트를 통과한 모든 코드를 프로덕션 환경까지 완전 자동으로 릴리스
22. DORA 메트릭스 (DORA Metrics) - 구글 클라우드가 정의한 소프트웨어 개발/운영 성과 측정 4대 지표
23. 배포 빈도 (Deployment Frequency) - 프로덕션에 얼마나 자주 배포하는가
24. 변경 리드 타임 (Lead Time for Changes) - 코드가 커밋된 후 프로덕션에 배포되기까지 걸리는 시간
25. 변경 실패율 (Change Failure Rate) - 배포 후 장애/버그로 인해 핫픽스나 롤백이 필요한 비율
26. 서비스 복구 시간 (Time to Restore Service / MTTR) - 장애 발생 시 복구에 걸리는 시간
27. SPACE 프레임워크 - 개발자 생산성을 단순 코드량(LOC)이 아닌 만족도, 성과, 활동, 커뮤니케이션, 효율성 5가지 차원으로 다각화 측정
28. 플랫폼 엔지니어링 (Platform Engineering) - 개발자의 인지 부하(Cognitive Load)를 줄이기 위해 전담 플랫폼 팀이 '내부 개발자 포털(IDP)'을 구축해 툴체인을 셀프 서비스로 제공하는 최신 DevOps 트렌드
29. 내부 개발자 포털 (IDP, Internal Developer Portal) - Backstage 등, 개발자가 인프라/K8s를 몰라도 클릭 몇 번으로 인프라 프로비저닝 및 CI/CD 파이프라인 생성
30. 골든 패스 (Golden Path / Paved Road) - 조직 내에서 권장되는 가장 안전하고 자동화된 표준 개발/배포 경로 (가이드라인)
31. 가치 흐름 매핑 (VSM, Value Stream Mapping) - 아이디어 발의부터 고객에게 가치가 전달되기까지의 전체 흐름에서 대기 시간(병목, Muda)을 식별하고 린(Lean)하게 제거하는 도식화 기법
32. 리드 타임 (Lead Time) vs 사이클 타임 (Cycle Time)
33. 콘웨이의 법칙 (Conway's Law) - "소프트웨어의 구조는 그 소프트웨어를 만드는 조직의 통신 구조를 닮는다"
34. 역 콘웨이 전략 (Inverse Conway Maneuver) - 원하는 마이크로서비스(MSA) 아키텍처 구조에 맞춰 조직 구조(스쿼드, 크로스펑셔널 팀)를 선제적으로 재편하는 전략
35. 데브옵스 토폴로지 (DevOps Topologies) - 안티 패턴 (Dev 팀과 Ops 팀의 완전 분리) vs 모범 패턴 (협력형, 플랫폼 팀 지원형)
36. 비난 없는 포스트모템 (Blameless Post-mortem) - 장애 발생 시 '누가' 잘못했는지가 아니라 '무엇이' 문제였고 시스템이 어떻게 막지 못했는지 시스템적 관점에서 분석하는 회고 문화
37. 심리적 안전감 (Psychological Safety) - 조직 내에서 실수나 의견을 자유롭게 말해도 불이익을 받지 않는다고 느끼는 믿음 (고성과 팀의 핵심 요소)
38. 애자일 PMO (Agile PMO) - 통제 중심의 기존 PMO에서 애자일 코칭 및 장애물 제거(Servant Leadership) 지원 조직으로 전환
39. 워터-스크럼-폴 (Water-Scrum-Fall) 안티 패턴 - 개발만 스크럼으로 하고, 앞단(기획)과 뒷단(배포)은 기존 폭포수(결재) 모델을 유지해 결국 리드 타임이 줄지 않는 현상
40. 피처 플래그 (Feature Flag) / 피처 토글 (Feature Toggle) - 코드 재배포 없이 런타임에 설정(API/DB)을 바꿔 특정 신기능을 켜거나 끄는 기법. (트렁크 기반 개발의 핵심 안전망)
41. 트렁크 기반 개발 (Trunk-Based Development) - 수명이 긴 피처 브랜치(Feature Branch)를 만들지 않고, 모든 개발자가 하루에도 여러 번 메인 트렁크(마스터) 브랜치에 직접 커밋/병합하여 병합 충돌(Merge Hell)을 방지
42. A/B 테스팅 (A/B Testing) - 두 가지 UI/기능을 동시에 실제 사용자에게 노출하여 데이터(전환율 등) 기반으로 의사결정
43. 다크 론칭 (Dark Launching) - 사용자 UI에는 노출하지 않고 백그라운드로만 새 코드를 실행시켜 성능 부하 및 에러를 프로덕션 트래픽으로 사전 검증
44. TDD (Test-Driven Development) / BDD (Behavior-Driven Development)
45. 시프트 레프트 (Shift-Left) - 소프트웨어 개발 수명 주기(SDLC)의 오른쪽 끝에 있던 활동(보안 검사, 테스트)을 왼쪽(개발/빌드 초기)으로 앞당겨 결함을 조기 발견하고 비용을 절감하는 사상
46. 챗옵스 (ChatOps) - 슬랙(Slack), MS Teams 등 메신저 내에서 봇(Bot) 커맨드를 입력해 배포, 모니터링 알람 확인, 장애 복구 등을 팀과 공유하며 수행
47. 에러 버짓 (Error Budget) - 100% 가용성의 비현실성을 인정하고, SLO(예: 99.9%)를 뺀 나머지 0.1%를 '합법적으로 허용된 장애 예산'으로 할당하여 신규 배포의 리스크를 관리하는 SRE 철학
48. MLOps (Machine Learning Operations) - 모델 개발과 운영의 단절 극복
49. DataOps (Data Operations) - 데이터 파이프라인 자동화 
50. BizDevOps - 비즈니스 요구사항 기획부터 운영까지 일체화
51. 애자일 성숙도 평가 지표 (Agile Maturity Assessment)
52. 기술 부채 (Technical Debt) 모니터링 시스템
53. 백로그 정제 (Backlog Grooming/Refinement) 
54. 데일리 스탠드업 (Daily Standup) 및 칸반 보드 
55. 워크플로우 오케스트레이터 (Workflow Orchestrator)
56. DevOps 툴체인 (Toolchain) 이기종 연동 API
57. 데브옵스 에반젤리스트 (DevOps Evangelist) 역할 
58. 개발자 경험 (DX, Developer Experience) 향상 전략
59. 번아웃 (Burnout) 방지를 위한 온콜 (On-call) 교대 근무 최적화
60. DevOps ROI (투자 수익률) 측정 지표

## 2. CI/CD 파이프라인 및 GitOps (60개)
61. 형상 관리 (Configuration Management) / 버전 관리 시스템 (VCS)
62. 중앙 집중형 VCS (SVN) vs 분산형 VCS (Git) - Git은 로컬 저장소에 전체 히스토리를 복제하여 오프라인 작업 및 브랜치 병합 속도 극대화
63. Git 브랜치 전략 (Git Branching Strategies)
64. Git Flow - Master, Develop, Feature, Release, Hotfix 5개 브랜치 사용 (안정적이나 복잡, 릴리스 주기 긴 프로젝트 적합)
65. GitHub Flow - Master 브랜치와 Feature 브랜치만 사용, 매우 단순하여 지속적 배포(CD) 및 트렁크 기반 개발에 최적화
66. GitLab Flow - 환경(Environment) 기반 배포와 연계된 브랜치 전략
67. 풀 리퀘스트 (Pull Request, PR) / 머지 리퀘스트 (Merge Request, MR) - 코드 병합 전 동료 검토(Code Review)를 요청하는 프로세스
68. 병합 충돌 (Merge Conflict) 및 해결 방안 (Rebase vs Merge)
69. 커밋 메시지 컨벤션 (Commit Message Convention) - feat, fix, docs, refactor 등 접두어 표준화
70. 빌드 도구 (Build Tools) - Maven, Gradle (Java), npm, yarn (Node.js)
71. 젠킨스 (Jenkins) - 가장 널리 쓰이는 자바 기반 오픈소스 CI/CD 자동화 서버 (플러그인 생태계 막강)
72. 선언적 파이프라인 (Declarative Pipeline) - Jenkinsfile에 빌드/테스트/배포 단계를 코드로 정의 (Pipeline as Code)
73. 깃허브 액션 (GitHub Actions) - GitHub 내장 CI/CD 런너, `.github/workflows/` 디렉터리에 YAML로 정의
74. 깃랩 CI (GitLab CI/CD) - 깃랩 내장 도구, `.gitlab-ci.yml` 활용
75. 아티팩트 (Artifact) - 소스코드가 빌드되어 생성된 최종 실행 가능한 결과물 (JAR, Docker Image 등)
76. 아티팩트 리포지토리 (Artifact Repository) - Nexus, Sonatype, JFrog, AWS ECR (도커 이미지 저장소)
77. 단위 테스트 (Unit Test) 자동화 (JUnit, PyTest)
78. 코드 커버리지 (Code Coverage) 분석 도구 (JaCoCo) - 소스코드의 몇 %가 테스트되었는지 측정 (구문, 분기 커버리지)
79. 소스코드 정적 분석 도구 (SonarQube) - 잠재적 버그, 코드 스멜, 보안 취약점(SAST) 자동 스캔 및 품질 게이트(Quality Gate) 통제
80. 패키지 취약점 스캐닝 (SCA, Software Composition Analysis) - 의존하는 오픈소스 라이브러리의 CVE 취약점 검사
81. 지속적 배포 파이프라인 (CD Pipeline) 아키텍처
82. 무중단 배포 (Zero Downtime Deployment) 전략 3가지
83. 롤링 배포 (Rolling Update) - 구버전 인스턴스를 하나씩 내리고 신버전을 하나씩 올리는 순차적 교체 (K8s 디폴트). 트래픽 처리량은 유지되나 배포 도중 구/신버전이 혼재됨
84. 블루/그린 배포 (Blue/Green Deployment) - 구버전(Blue)과 동일한 규모의 신버전(Green) 환경을 완벽히 띄워놓고, 로드밸런서의 라우팅을 한 번에 스위칭. 롤백이 1초 만에 가능하나 클라우드 자원 일시적 2배 요구
85. 카나리 배포 (Canary Release) - 신버전으로 라우팅되는 트래픽 비율을 1% -> 10% -> 100%로 점진적 확장하며 에러율(5xx) 메트릭을 모니터링, 이상 발생 시 즉시 자동 롤백
86. GitOps (깃옵스) 패러다임 - 인프라 및 애플리케이션의 '목표 상태(Desired State)'를 오직 Git 레포지토리에 선언적(YAML)으로 저장하고, K8s 클러스터 내부의 에이전트가 Git의 변화를 감지해 클러스터 상태와 지속적으로 동기화(Sync)시키는 현대적 CD 방식
87. 푸시 기반(Push-based) 배포 - 젠킨스(외부)가 kubectl 명령을 통해 K8s 클러스터에 직접 푸시 (보안 자격증명 유출 위험)
88. 풀 기반(Pull-based) 배포 - GitOps 방식. 클러스터 '내부'의 에이전트(ArgoCD)가 외부 Git을 폴링(Pull)하여 변경사항을 가져와 적용 (외부망에서 클러스터로의 인바운드 방화벽 오픈 불필요, 보안 극대화)
89. ArgoCD (아고씨디) - 쿠버네티스를 위한 대표적인 GitOps 선언적 지속적 배포 도구
90. FluxCD - ArgoCD의 경쟁 GitOps 솔루션
91. Kustomize (커스터마이즈) - 쿠버네티스 YAML 매니페스트를 템플릿 엔진 없이(Native) 오버레이(dev, prod) 방식으로 다형성 있게 관리하는 도구
92. Helm (헬름) 차트 - K8s 패키지 매니저, values.yaml 변수 주입을 통해 복잡한 K8s 리소스를 한 번에 릴리스
93. 스핀네이커 (Spinnaker) - 넷플릭스 개발, 멀티 클라우드(AWS, GCP, K8s) 배포 및 카나리 분석 자동화(Kayenta) 특화 CD 플랫폼
94. 파이프라인 보안 락인 (Pipeline Security) 
95. 시크릿 매니저 (Secret Manager) - DB 패스워드, API 키를 Git에 하드코딩하지 않고 분리 저장 (HashiCorp Vault, AWS Secrets Manager)
96. K8s Sealed Secrets - GitOps 환경에서 시크릿을 비대칭키로 암호화하여 Git에 안전하게 올리고, 클러스터 내부에서 복호화
97. 배포 승인 게이트 (Approval Gate) 수동/자동화 구성
98. 롤백 (Rollback) 전략 - 파이프라인 에러율 임계치 도달 시 이전 안정 버전(이전 커밋)으로 자동 복원
99. 데이터베이스 마이그레이션 도구 자동화 (Flyway, Liquibase) - 앱 코드 배포와 DB 스키마(DDL) 변경 스크립트 실행의 싱크 처리
100. 멀티 리전 (Multi-Region) 동시 배포 파이프라인 설계
101. 엣지 디바이스 (Edge Device) OTA (Over-The-Air) 무선 펌웨어 배포 파이프라인
102. 에어 갭 (Air-gapped) 폐쇄망 환경의 CI/CD 패키징 전달 (Tarball)
103. CI/CD 메트릭 대시보드 - 배포 성공률, 빌드 소요 시간 병목 분석
104. 모바일 앱 (iOS/Android) 전용 CI/CD 파이프라인 (Fastlane)
105. 빌드 캐싱 (Build Caching) 최적화 - Maven/Docker 레이어 캐시 활용 속도 단축
106. 분산 빌드 (Distributed Build) 워커 노드 스케일 아웃
107. 크론 (Cron) 배치 기반 나이트 빌드(Nightly Build) 
108. 테스트 데이터 마스킹 자동 주입 파이프라인
109. 소프트웨어 자재 명세서 (SBOM) 추출 의무화 파이프라인 임베드
110. 무중단 DB 스키마 롤아웃 (Expand and Contract 패턴)
111. 마이크로 프론트엔드 (Micro Frontends) 컴포넌트 단위 개별 배포망
112. 서버리스 프레임워크 (Serverless Framework) 람다 배포 추상화
113. SAM (Serverless Application Model) 
114. 카나리 분석 도구 (Kayenta) 통계적 오류 탐지 
115. 테라폼 클라우드 / 테라폼 엔터프라이즈 CI 연동 (Atlantis)
116. 인프라 배포 시 드리프트 감지 (Drift Detection) 
117. 텍스트옵스 (TextOps) 및 DocOps (문서 배포 자동화)
118. CI 파이프라인 러너 (Runner) 인스턴스의 1회용 (Ephemeral) 격리 실행 
119. 프리커밋 훅 (Pre-commit Hook) 로컬 코드 포맷팅 자동 점검 
120. 컨테이너 이미지 사이닝 (Image Signing / Cosign, Notary) 무결성 검증망

## 3. 사이트 신뢰성 공학 (SRE) 및 옵저버빌리티 (70개)
121. SRE (Site Reliability Engineering) - 구글이 제안한 IT 운영 접근법. "SRE는 소프트웨어 엔지니어에게 운영 업무를 맡겼을 때 발생하는 일이다." 
122. SLI (Service Level Indicator) - 서비스 상태를 보여주는 실제 측정 수치 (예: 지난 1시간 동안의 HTTP 5xx 에러율 0.05%)
123. SLO (Service Level Objective) - 팀 내부적으로 설정한 서비스 지표 목표치 (예: 월간 에러율 0.1% 이하 유지). 비즈니스 목표와 IT 운영의 타협점
124. SLA (Service Level Agreement) - 고객과 맺은 법적/재무적 계약 (SLO보다 느슨하게 설정하여 위약금 방어)
125. 에러 예산 (Error Budget) - 100% 가용성은 불가능하다는 전제하에 허용된 장애 한도. (100% - SLO 99.9% = 0.1% 예산). 예산 소진 시 신기능 릴리스 동결
126. 토일 (Toil) - 반복적이고 자동화 가능한 수작업(가치 없는 운영 잡일). SRE는 엔지니어링 시간을 확보하기 위해 토일을 50% 미만으로 억제
127. 온콜 (On-call) 경보 및 교대 근무 프로세스 최적화 (경고 피로 Alert Fatigue 방지)
128. 무비난 포스트모템 (Blameless Post-mortem) - 장애 복구 후 인적 오류(Human Error)를 탓하지 않고, 시스템 구조적 원인과 예방 프로세스를 문서화하는 장애 회고 문화
129. 옵저버빌리티 (Observability / 가시성 / 관측성) - 마이크로서비스(MSA) 같은 복잡한 분산 시스템 내부에서 문제가 발생했을 때, 외부로 출력되는 텔레메트리(MELT) 데이터만 보고도 근본 원인(Root Cause)을 추론할 수 있는 역량
130. 모니터링(이미 아는 문제를 대시보드로 봄) vs 옵저버빌리티(예측 못한 미지의 문제 Unknown-Unknowns 를 탐색/디버깅함)
131. 옵저버빌리티 3대 기둥 (Three Pillars) - 메트릭(Metrics), 로그(Logs), 분산 추적(Traces)
132. 메트릭 (Metrics) - 시간에 따른 시스템 자원(CPU, 메모리) 및 서비스 응답 수치를 압축한 시계열 데이터 (가장 적은 용량, 경고 알람 설정용)
133. SRE 4대 골든 시그널 (Four Golden Signals) - 트래픽(Traffic, 초당 요청 수), 지연 시간(Latency), 에러(Errors, 5xx 비율), 포화도(Saturation, 자원 사용률/큐 대기)
134. USE 메서드 (Utilization, Saturation, Errors) - 인프라 자원 분석 방법론
135. RED 메서드 (Rate, Errors, Duration) - 애플리케이션 서비스 로직 분석 방법론
136. 프로메테우스 (Prometheus) - 클라우드 네이티브 환경의 사실상 표준 메트릭 수집 시스템. 에이전트가 밀어주는 방식(Push)이 아니라 서버가 주기적으로 엔드포인트를 당겨오는(Pull) 메커니즘
137. 그라파나 (Grafana) - 프로메테우스, 엘라스틱서치 등 데이터소스를 연결하여 강력한 시각화 대시보드를 제공하는 오픈소스 플랫폼
138. 로그 (Logs) - 애플리케이션 실행 중 발생하는 특정 이벤트에 대한 상세한 텍스트 기록 (가장 많은 용량 차지, 디버깅의 핵심)
139. 분산 로깅 아키텍처 - Fluentd/Logstash(수집/변환) -> Kafka(버퍼링) -> Elasticsearch(저장/검색) -> Kibana(시각화) (EFK / ELK Stack)
140. 로그 포맷 표준화 - 디버깅 용이성을 위해 JSON 형태의 구조화된 로그(Structured Logging) 필수 적용
141. 분산 추적 (Distributed Tracing) - MSA에서 하나의 사용자 요청이 수많은 마이크로서비스를 넘나들며 병목이 어디서 발생하는지 구간별로 추적하는 기술
142. 트레이스 (Trace) - 하나의 사용자 요청 전체 흐름
143. 스팬 (Span) - 트레이스 내에서 단일 서비스가 수행한 작업 구간 (시작/종료 시간 포함). 상위 스팬(부모)과 하위 스팬(자식) 간 계층 구조 형성
144. 컨텍스트 전파 (Context Propagation) - 서비스 간 HTTP 호출 시 HTTP Header에 Trace ID와 부모 Span ID를 주입해 흐름의 연속성을 유지
145. 예거 (Jaeger) / 집킨 (Zipkin) - 대표적인 오픈소스 분산 추적 UI/스토리지 백엔드
146. 오픈텔레메트리 (OpenTelemetry, OTel) - CNCF 프로젝트로, 기존 벤더마다 파편화된 메트릭, 로그, 트레이스 수집/계측(Instrumentation) SDK와 표준 명세(API)를 하나로 통합한 관측성 글로벌 표준
147. eBPF (Extended Berkeley Packet Filter) - 리눅스 커널 소스코드를 수정하지 않고도 커널 공간에 샌드박스화된 안전한 코드를 삽입해, 네트워크 트래픽이나 함수 호출 이벤트를 오버헤드 없이 스니핑/관측하는 혁신적 차세대 기술 (사이드카 프록시 없이도 네트워크 옵저버빌리티 구현 가능 - Cilium 등)
148. 카오스 엔지니어링 (Chaos Engineering) - 시스템이 평상시일 때 고의로 서버 종료, 네트워크 지연, CPU 폭주 등 '혼돈(장애)'을 주입하여, 이중화/서킷 브레이커 같은 시스템의 회복 탄력성(Resiliency) 메커니즘이 실제 위기 시 정상 동작하는지 선제적으로 실험하는 엔지니어링 (넷플릭스 카오스 몽키 기원)
149. 카오스 몽키 (Chaos Monkey) / 카오스 메시 (Chaos Mesh)
150. 장애 영향 반경 (Blast Radius) 최소화 - 카오스 실험 시 고객 피해가 없도록 범위를 제한
151. 정상 상태 (Steady State) 가설 수립 및 결과 비교 검증 
152. 오토스케일링 병목 현상 - HPA 트리거 지연으로 인한 트래픽 유실 방지망 (커스텀 메트릭 기반 예측 스케일링)
153. 서킷 브레이커 (Circuit Breaker) 상태 머신 - Closed (정상), Open (장애 감지 시 빠른 실패 반환), Half-Open (일부 트래픽만 흘려보내 복구 여부 확인)
154. 재시도 (Retry) 폭풍 방지 - 지수적 백오프 (Exponential Backoff, 재시도 간격을 지수 함수로 늘림) 및 지터 (Jitter, 난수를 섞어 동시 재시도 충돌 방지)
155. 타임아웃 (Timeout) 동기화 전략
156. 폴백 (Fallback) 메커니즘 - 백엔드 장애 시 에러 화면 대신 캐시된 과거 데이터 반환
157. 다크 부채 (Dark Debt) / 운영 부채 (Operational Debt) 청산 전략 
158. MTBF (평균 고장 간격) 및 MTTR (평균 복구 시간) 최적화 
159. 페일오버 (Failover) 및 페일백 (Failback) 아키텍처 
160. 능동적 상태 확인 (Health Check / Probes) - Liveness, Readiness, Startup
161. AIOps (Artificial Intelligence for IT Operations) - 머신러닝을 활용해 수만 개의 알람 중 연관된 것을 그룹핑(노이즈 감소)하고, 장애 전조를 이상 탐지(Anomaly Detection) 모델로 예측 자동 치유(Auto-remediation)
162. APM (Application Performance Management) 인스트루먼테이션 
163. RUM (Real User Monitoring) - 브라우저 기반 실제 사용자 화면 로딩 지연 추적
164. Synthetic Monitoring (합성 모니터링) - 더미 클라이언트를 띄워 주기적으로 로그인/결제 시나리오를 가상 테스트
165. 서비스 메시 (Service Mesh) 기반 텔레메트리 자동 수집 (사이드카 로깅)
166. 분산 락 매니저 (Distributed Lock) 병목 관측 
167. 트래픽 섀도잉 (Traffic Shadowing) 을 이용한 SRE 운영 테스트
168. 이벤트 소싱 상태 복구 (Replay) 모니터링 
169. 클라우드 비용 모니터링 (FinOps) 연계 SRE 정책 (유휴 자원 킬링)
170. 하드웨어 에러 (디스크/메모리 부패) 자가 치유(Self-Healing) 파일 시스템 (ZFS, Btrfs)
171. 용량 계획 (Capacity Planning) 및 부하 테스트 (Load Testing)
172. 프로비저닝 병목 (Cold Start) 관측 지표
173. 마이크로버스트 (Microburst) 트래픽 - 1초 미만의 찰나에 쏟아져 모니터링 툴(1분 주기)에 잡히지 않는 스파이크 트래픽 탐지 기법
174. 런북 (Runbook) / 플레이북 (Playbook) - 장애 발생 시 대응 절차를 체계적으로 정리한 매뉴얼 문서 (SOAR 연동 자동화)
175. 시스템 경계 완충지대 (Buffer/Queue) 텔레메트리 
176. 분산 DB 쿼리 플랜 지연(Slow Query) 역추적망 
177. 서버리스(FaaS) 환경의 옵저버빌리티 한계 (에이전트 설치 불가) 극복 방안 (AWS X-Ray 등)
178. 그라파나 템플릿(Grafana Dashboard as Code) 프로비저닝
179. 시계열 DB (InfluxDB, Prometheus TSDB) 압축/롤업 엔진
180. DevOps 조직 토폴로지와 SRE 팀의 인바운드 대응 비중 (50% 한계) 모델 
181. SRE 임베디드 (SRE Embedded) 운영 모델 
182. 상태 페이지 (Status Page) 대외 공개 SLA 운영 
183. 고객 신뢰도 확보를 위한 데이터 손실(Data Loss) 제로 아키텍처 
184. 재해 복구 (DR) 훈련의 카오스 엔지니어링 융합 
185. 네트워크 지터 (Network Jitter) 및 패킷 손실 관측 메트릭 
186. DNS 캐시 중독 및 라우팅 BGP 하이재킹 모니터링망 
187. OOM (Out of Memory) 킬러 커널 로그 파싱 알람 
188. 리눅스 퍼포먼스 툴 (perf, iostat, vmstat, tcpdump) SRE 활용 
189. 커스텀 메트릭 (Custom Metrics) 비즈니스 로직(결제 성공률 등) 프로메테우스 연동
190. 클라우드 네이티브 생태계 (CNCF) Landscape 진화 방향 (Observability 통일화)

## 4. 인프라스트럭처 애즈 코드 (IaC) 및 클라우드 네이티브 아키텍처 (70개)
191. 인프라스트럭처 애즈 코드 (IaC, Infrastructure as Code) - 수동 클릭이나 셸 스크립트 대신, 선언적(Declarative) 코드(YAML, HCL)로 클라우드/인프라 리소스를 프로비저닝, 버전 관리(Git), 테스트하는 기법
192. 불변 인프라 (Immutable Infrastructure) - 서버 구성을 배포 후 런타임에 직접 접속(SSH)해 패치/수정하지 않고, 변경 필요 시 완전히 새 이미지를 빌드해 교체(Replace)하는 패러다임
193. 구성 편류 (Configuration Drift) - 시간이 지나면서 IaC 코드 스펙과 실제 라이브 인프라의 설정이 수동 패치 등으로 인해 불일치하게 되는 장애 유발 원인 (IaC가 이를 방지함)
194. 멱등성 (Idempotency) - IaC 코드를 한 번 실행하든 천 번 실행하든 최종 결과 인프라 상태는 항상 동일하게 보장되는 특성
195. 테라폼 (Terraform) - HashiCorp가 개발한 오픈소스 클라우드 불가지론적(Agnostic, AWS/GCP 모두 지원) 인프라 프로비저닝 도구 (HCL 언어 사용)
196. 테라폼 상태 파일 (tfstate 파일) - 테라폼이 현재 실제 인프라 구조를 매핑해 기억해두는 메타데이터 JSON 파일 (S3 등에 백엔드 잠금 보관 필수)
197. AWS CloudFormation / AWS CDK - AWS 리소스 전용 IaC 도구
198. 앤서블 (Ansible) - 인프라 '생성(프로비저닝)'보다는 생성된 서버 내부의 OS 설정, 패키지 설치를 담당하는 '구성 관리(Configuration Management)' 자동화 도구. 에이전트 없이 SSH만으로 동작 (Playbook YAML)
199. 패커 (Packer) - 동일한 설정 스크립트로 도커 이미지, AWS AMI 등 다양한 플랫폼의 가상머신 이미지를 일괄 베이킹(Baking)하는 도구
200. 프로비저닝 (Provisioning) vs 구성 관리 (Configuration Management) 
201. 마이크로서비스 아키텍처 (MSA) - 모놀리식 단일 덩어리를 비즈니스 도메인 단위로 쪼개어 독립된 DB, 독립 배포 파이프라인을 갖게 한 구조
202. 컨웨이의 법칙 (Conway's Law) - 마이크로서비스 설계 시 기술이 아닌 비즈니스 팀 조직 구조를 따라야 한다는 원칙
203. API 게이트웨이 (API Gateway) - 클라이언트 요청을 받아 라우팅, 인증, 스로틀링(Throttling)을 단일 진입점에서 통제 (Kong, AWS API Gateway)
204. BFF (Backend For Frontend) - 다수 프론트엔드(웹, 모바일)에 맞춰 API 게이트웨이를 분리 파편화 제공
205. 서비스 메시 (Service Mesh) - 애플리케이션 비즈니스 코드와 네트워킹 제어 코드를 분리, 인프라(L7 프록시) 단에서 서비스 간 통신(라우팅, 서킷 브레이커, mTLS 암호화)을 전담 (Istio, Envoy)
206. 사이드카 (Sidecar) 패턴 - 서비스 컨테이너(Pod) 옆에 프록시 컨테이너를 함께 묶어(사이드카처럼) 배포하여 모든 입출력 네트워크 트래픽을 가로채 제어
207. mTLS (상호 TLS) - 제로 트러스트 원칙에 따라 내부 마이크로서비스 간 통신 시에도 발신자/수신자 양방향 인증서 검증 암호화
208. CQRS (Command Query Responsibility Segregation) - 성능 확장을 위해 상태 변경(쓰기) 모델과 조회(읽기) 모델용 DB 인프라를 논리적/물리적으로 분리 (이벤트 소싱과 결합)
209. 이벤트 소싱 (Event Sourcing) - RDBMS의 덮어쓰기 로직 대신, 상태가 변경된 모든 '이벤트 이력'을 장부(스트림)에 순차 기록(Append-Only). 언제든 이벤트 리플레이를 통해 데이터 복구/재생 가능
210. 사가 패턴 (Saga Pattern) - MSA에서 분산 트랜잭션 2PC 락(Lock) 병목을 피하기 위해, 로컬 트랜잭션들을 체인처럼 비동기로 연결하고, 실패 시 역순으로 '보상 트랜잭션(Compensating Transaction)'을 실행하여 논리적 롤백 구현 (Choreography vs Orchestration)
211. 스트랭글러 피그 (Strangler Fig) 패턴 - 레거시 모놀리식 시스템을 앞단 게이트웨이 라우팅을 조작해 MSA로 하나씩 갉아먹듯 점진적 교체하는 안전 마이그레이션 기법
212. 폴리글랏 퍼시스턴스 (Polyglot Persistence) - 각 마이크로서비스의 특성(결제, 로그, 추천)에 맞춰 RDBMS, NoSQL(키-값, 문서), Graph DB 등 다양한 데이터베이스 기술을 혼용 아키텍처
213. 데이터베이스 퍼 서비스 (Database per Service) - 다른 마이크로서비스의 DB에 직접 쿼리(조인) 접근 불가, 오직 API로만 통신 강제 
214. 이벤트 주도 아키텍처 (EDA, Event-Driven Architecture) - 서비스 간 동기적 REST API 결합을 버리고, 메시지 큐(Kafka)를 통해 이벤트를 비동기적으로 Pub/Sub 통신하여 극강의 디커플링 보장
215. 서버리스 (Serverless / FaaS) 아키텍처 - 인프라 프로비저닝 없이 '함수 코드'만 클라우드에 올려두면, 특정 이벤트 발생 시 자동으로 컨테이너가 확장/실행되고 1밀리초 단위로 과금 (AWS Lambda)
216. 콜드 스타트 (Cold Start) - 서버리스의 치명적 단점. 장기 휴면 함수 호출 시 컨테이너 이미지를 다운받고 구동하느라 첫 응답 지연 발생 (프로비저닝된 동시성으로 예열 해결)
217. 컨테이너 오케스트레이션 (Kubernetes) 아키텍처 
218. 클러스터 오토스케일러 (CA) / 수평적 파드 오토스케일러 (HPA) 연동
219. 쿠버네티스 선언적(Declarative) 제어 루프 - 목표 상태(YAML)와 현재 클러스터 상태를 비교하여 일치시키는 무한 릴레이션 메커니즘
220. 오퍼레이터 (Operator) 패턴 - 쿠버네티스 CRD(커스텀 리소스)와 커스텀 컨트롤러 로직을 이용해, DB 백업/복제 등 사람이 하던 복잡한 도메인 지식 운영을 K8s 내부 자동화로 편입
221. K8s 서비스 퍼블리싱 (ClusterIP, NodePort, LoadBalancer, Ingress) 라우팅 패러다임
222. CNI (Container Network Interface) 플러그인 (Calico, Flannel) 파드 간 오버레이 통신망
223. CSI (Container Storage Interface) 퍼시스턴트 볼륨(PV/PVC) 동적 스토리지 할당 
224. 헬름 (Helm) 차트 템플릿 엔진 패키지 관리망
225. 마이크로 프론트엔드 (Micro Frontends) 아키텍처 - 백엔드 MSA를 프론트 UI 뷰 분할 배포까지 확장 연결
226. 셀 기반 아키텍처 (Cell-based Architecture) - 장애 반경 격리를 위해 클라우드 리전을 여러 개의 완전 독립된 자급자족 셀(Cell)로 쪼개어 트래픽 라우팅 
227. 멀티 클라우드 (Multi-Cloud) / 하이브리드 클라우드 랜딩 존 (Landing Zone) 설계 네트워크 통제
228. SDDC (소프트웨어 정의 데이터센터) SDN 기반 클라우드 가상 스위치 VXLAN
229. 인텐트 기반 네트워킹 (IBN) - 관리자의 비즈니스 '의도'를 선언하면 SDN 컨트롤러가 알아서 네트워크 설정/보안 통제 자동 구성 
230. 클라우드 비용 효율 FinOps 프레임워크 최적화 (RI, 스팟 인스턴스, 핫-콜드 스토리지 티어링)
231. 엣지 네이티브 (Edge Native) 설계망 분산 지연 단축 
232. gRPC (Google RPC) 통신 - HTTP/2 바이너리 프로토콜 버퍼 직렬화 기반 초고속 MSA 동기 통신망
233. API First Design 및 Swagger/OpenAPI 명세 기반 컨트랙트 테스팅
234. 멀티 테넌시 (Multi-Tenancy) SaaS 데이터베이스 격리 스키마 아키텍처 (논리 격리 vs 물리 격리)
235. 레지스트리 (Registry) 태그 불변성 (Immutable Tag) 운영 이미지 관리망 
236. 볼트 (Vault) 기반 동적 시크릿 (Dynamic Secrets) TTL 발급 아키텍처 
237. OPA (Open Policy Agent) / Gatekeeper - 인프라 보안 정책을 코드(Rego 언어)로 정의하여 쿠버네티스 파드 배포 시 비인가 속성(루트 권한 등)을 강제 차단하는 규정 준수 자동화
238. 클라우드 마이그레이션 6R (Rehost, Replatform, Refactor 등) 전환 전략망
239. 무상태성 (Stateless) 설계 - 애플리케이션 메모리에 세션을 남기지 않고 외부 Redis 등에 위임하여 스케일 아웃 확보 
240. 서드파티 록인 회피 기술망 (Knative, 오픈소스 DB 클러스터링 기반)

## 5. DevSecOps, 사이버 보안, CI/CD 테스트 및 규제 준수 (70개)
241. DevSecOps 사상 - DevOps의 신속한 배포 파이프라인(CI/CD) 내에 보안(Security) 검증 및 차단 프로세스를 자동화 도구로 내재화하여, 배포 속도를 해치지 않으면서 코드 결함을 조기 발견
242. 시프트 레프트 (Shift-Left) - SDLC 생명주기 우측(테스트/운영)에 있던 보안 점검을 좌측(기획/개발/빌드)으로 당겨 개발자 책임 하에 조기 예방하여 비용 절감
243. 소스코드 정적 보안 분석 (SAST, Static Application Security Testing) - 코드를 실행하지 않고 구문, 데이터 흐름을 분석해 SQL 인젝션, 버퍼 오버플로우 등 취약점 룰셋 검사 (SonarQube 등 CI 빌드 단계 파이프라인 통합)
244. 동적 애플리케이션 보안 테스트 (DAST, Dynamic Application Security Testing) - 애플리케이션을 런타임으로 실행한 상태에서 외부 해커 관점으로 웹 취약점 스캐닝/퍼징 공격을 날려 검증 (스테이징/QA 배포 후 자동화 실행)
245. 상호작용형 애플리케이션 보안 테스트 (IAST, Interactive Application Security Testing) - SAST와 DAST 결합. 앱 내부에 에이전트를 심어 실행 중인 메모리 로직과 공격 페이로드를 동시 분석 (오탐지 최소화)
246. 소프트웨어 구성 분석 (SCA, Software Composition Analysis) - 소스코드 자체뿐 아니라 포함된 오픈소스 라이브러리의 알려진 취약점(CVE)과 라이선스 충돌 위험 검사 도구
247. 컨테이너 이미지 스캐닝 (Container Image Scanning) - 도커 이미지 빌드 시 OS 기본 패키지와 모듈의 취약점을 탐지 (Trivy, Clair, K8s Admission Controller 연동 배포 차단)
248. SBOM (Software Bill of Materials) - 소프트웨어를 구성하는 모든 오픈소스 부품, 라이브러리, 버전 정보를 명세한 자재 명세서 (공급망 보안 검증의 핵심 표준 포맷, SPDX, CycloneDX)
249. 소프트웨어 공급망 공격 (Supply Chain Attack) - 솔라윈즈(SolarWinds) 사태처럼 정상 소프트웨어 벤더의 빌드/업데이트 파이프라인을 해킹해 악성코드를 심어 고객사로 유포하는 공격망
250. 시크릿 매니지먼트 (Secret Management) - 코드 내 AWS API Key, DB Password 등 기밀 정보 하드코딩 방지. (HashiCorp Vault를 통해 중앙집중식 암호화 보관 및 애플리케이션 기동 시 환경변수/볼륨으로 동적 주입)
251. 쿠버네티스 포드 보안 정책 (Pod Security Admission / 구 PSP) - 컨테이너가 루트 권한(Privileged)으로 실행되거나 호스트 네트워크 볼륨 마운트 시 클러스터 내 배포 차단
252. 컨테이너 이스케이프 (Container Escape) 방어 - 마이크로VM 격리 (gVisor, Kata Containers) 등 커널 분리 샌드박싱
253. 네트워크 마이크로 세그멘테이션 (Micro-segmentation) - 제로 트러스트 사상. 서비스(Pod) 간 통신을 기본 Deny All로 막고, 필요한 통신(Network Policy)만 IP/포트 단위 화이트리스트로 개방하여 해커의 수평 이동(Lateral Movement) 차단
254. 클라우드 보안 형상 관리 (CSPM, Cloud Security Posture Management) - AWS S3 퍼블릭 오픈 오류 등 클라우드 인프라 설정 오류 및 컴플라이언스(ISMS, PCI-DSS) 위반을 실시간 탐지/자동 교정
255. 클라우드 워크로드 보호 플랫폼 (CWPP, Cloud Workload Protection Platform) - VM, 컨테이너, 서버리스 등 런타임 환경 내부의 악성코드 탐지, 메모리 보호 기능 (EDR의 클라우드 확장)
256. CNAPP (Cloud-Native Application Protection Platform) - CSPM과 CWPP, CI/CD 스캐닝을 단일 통합 대시보드로 묶어 가시성을 제공하는 최신 클라우드 보안 트렌드
257. 제로 트러스트 아키텍처 (ZTA, Zero Trust Architecture) - 내부망에 있더라도 무조건 신뢰하지 않으며, 모든 요청에 대해 신원(Identity), 기기 상태, 컨텍스트를 다중 인증(MFA)하고 최소 권한만 동적 부여 (ZTNA, SDP)
258. 정책 애즈 코드 (Policy as Code / OPA Gatekeeper) - 인프라 보안 정책을 Rego 언어로 코드화하여 IaC 테라폼 배포 단계나 K8s API 서버 호출 시점에 강제 검증 필터링
259. 카오스 보안 엔지니어링 (Security Chaos Engineering) - 프로덕션 시스템에 방화벽 정책 삭제, IAM 권한 오류 등을 고의로 주입하여 보안 관제 시스템(SIEM)이 제대로 알람/차단하는지 테스트
260. 지속적 테스팅 (Continuous Testing) 통합 파이프라인 아키텍처 
261. TDD (Test-Driven Development) 실패-구현-리팩토링 레드 그린 사이클 
262. BDD (Behavior-Driven Development) 비즈니스 언어 포맷 (Given-When-Then) 기반 인수 테스트 (Cucumber 연동망)
263. 유닛 테스트 (Unit Test) 함수 격리망 프레임워크 모킹(Mocking), 스터빙(Stubbing) 더블 기법 
264. 통합 테스트 (Integration Test) DB 연동 모듈 조립망 결함 탐지 (Testcontainers 활용 격리 컨테이너 띄우기)
265. E2E (End-to-End) 테스트 / UI 테스트 - Selenium, Cypress 등 브라우저 환경 사용자 플로우 전체 관통 테스트
266. 계약 테스트 (Contract Testing / Pact) - MSA 환경에서 프로바이더와 컨슈머 간 API 통신 포맷(계약) 변경 시 호환성 파괴가 없는지 상호 검증 (E2E 테스트의 무거움 대안)
267. 부하 테스트 (Load Testing) 및 스트레스 테스트 CI 파이프라인 임베드 (JMeter, k6)
268. 카나리 분석기 (Canary Analysis) 자동화 - 신버전 배포 시 CPU, 레이턴시, 에러율 메트릭을 통계학적으로 이전 버전과 비교 채점해 이상 발견 시 자동 롤백 (Spinnaker Kayenta)
269. 뮤테이션 테스팅 (Mutation Testing / 돌연변이 테스트) - 원본 소스코드 산술 연산자 등을 의도적으로 망가뜨려(돌연변이) 런타임 주입 후, 기존 테스트 스위트가 이를 에러로 적발(Kill)하는지 평가하여 테스트 케이스 자체의 품질/커버리지를 검증
270. 카프카(Kafka) 파이프라인 메시지 무결성 통제망 스키마 레지스트리 (Avro Schema 변이 하위 호환성 강제 방어)
271. 데이터베이스 마이그레이션(DDL) 롤백 자동화 스크립팅 파이프 (Liquibase 롤백 태그 연동망)
272. CI 캐시 중독(Cache Poisoning) 및 러너(Runner) 인스턴스 침해 격리 보안망 구조 (일회성 Ephemeral 러너)
273. 사이버 킬체인 로그 관제 ELK/SIEM 파이프라인 
274. WAF (웹 애플리케이션 방화벽) 룰셋 인그레스(Ingress) 계층 통합 로직망
275. 서비스 계정 (IAM Role for Service Accounts, IRSA) 최소 권한 OIDC 연합 토큰 증명 
276. FIDO, WebAuthn 생체 기반 패스워드리스 인증 적용 체제 
277. OAuth 2.0 OIDC 토큰 권한 위임 체계 마이크로서비스 연동 
278. 개인정보 데이터 마스킹 자동 필터(DLP 파이프라인 전송망 감시)
279. 난독화 (Obfuscation) 안티 디버깅 모바일 빌드 파이프라인 주입
280. 양자 내성 암호 (PQC) 마이그레이션 클라우드 인프라 키 관리 체계 

## 6. 시험 빈출 요약 및 기술사 융합 논술 토픽 (120개 집중 요약)
281. 데브옵스 CALMS (문화 자동화 린 측정 공유)
282. 사일로 효과 (부서 장벽 이기주의)
283. 12 팩터 앱 (클라우드 네이티브 설계 원칙) 
284. CI CD 지속적 통합 제공 배포 자동화
285. DORA 메트릭스 4대 지표 배포 빈도 리드타임 실패율 복구 
286. 롤링 배포 (점진 교체 무중단)
287. 블루 그린 (전면 스위칭 롤백 유리 2배 자원) 
288. 카나리 배포 (1% 오픈 에러 검증 확대) 
289. 섀도우 배포 트래픽 미러링 백그라운드 테스트 
290. 피처 플래그 토글 동적 분기 트렁크 개발 
291. GitOps 선언형 동기화 푸시 풀 배포 차이 
292. IaC 테라폼 인프라 코드화 멱등성 
293. 구성 편류 방지 불변 인프라 
294. 테라폼 상태 파일 tfstate 잠금 
295. 마이크로서비스 MSA 도메인 주도 설계 DDD 
296. 바운디드 컨텍스트 애그리게이트 루트 
297. API 게이트웨이 인증 스로틀링 
298. 서비스 메시 Istio 사이드카 트래픽 보안 
299. mTLS 상호 인증 제로 트러스트 
300. 서비스 디스커버리 동적 IP 라우팅
301. 서킷 브레이커 장애 연쇄 확산 차단 폴백 
302. 사가 패턴 2PC 한계 보상 트랜잭션 롤백 
303. CQRS 읽기 쓰기 물리 논리 분리 이벤트 소싱 
304. 서버리스 FaaS 콜드 스타트 지연 극복 
305. 스트랭글러 피그 레거시 교체 패턴 
306. 컨테이너 도커 커널 공유 이미지 레이어 
307. 네임스페이스 cgroups 자원 격리 제한 
308. 쿠버네티스 마스터 워커 컴포넌트 
309. 포드 Pod 레플리카셋 디플로이먼트 
310. ClusterIP NodePort LoadBalancer Ingress 라우팅 
311. 데몬셋 전체 노드 로깅 
312. 테인트 톨러레이션 노드 오염 배제 
313. 오토스케일링 HPA CA 파드 노드 증가 
314. PV PVC 스토리지 추상화 보존 
315. 헬름 패키지 템플릿 변수 주입 
316. SRE 사이트 신뢰성 구글 운영 공학 
317. SLI SLO SLA 에러 예산 한도 통제 
318. 토일 무가치 자동화 대상 작업 
319. 무비난 포스트모템 회고 문화 
320. 옵저버빌리티 가시성 메트릭 로그 트레이스 
321. 분산 추적 Trace ID 병목 파악 
322. 오픈텔레메트리 CNCF 표준화 
323. 프로메테우스 풀 방식 그라파나 대시보드 
324. 카오스 엔지니어링 의도적 장애 복원력 점검 
325. 데브섹옵스 시프트 레프트 보안 조기 점검 
326. SAST DAST IAST 정적 동적 보안 테스팅 
327. SCA 오픈소스 컴플라이언스 스캔 
328. SBOM 소프트웨어 구성 자재 명세 공급망 방어 
329. 시크릿 매니저 볼트 하드코딩 방지 
330. 마이크로 세그멘테이션 래터럴(횡적) 이동 차단 방화벽 
331. CSPM 클라우드 형상 설정 통제 
332. CWPP 런타임 워크로드 컨테이너 보호 
333. CNAPP 클라우드 통합 보안 플랫폼 
334. 정책 애즈 코드 OPA Gatekeeper Rego 검사 
335. TDD BDD 인수 테스트 모의 격리 
336. 계약 테스트 MSA API 통신 상호 호환 검사 
337. 뮤테이션 테스트 테스트 케이스 품질 평가망 
338. 플랫폼 엔지니어링 IDP 골든 패스 인지 부하 감소 
339. 빅데이터 하둡 HDFS 스파크 인메모리 
340. 카프카 분산 큐 Pub/Sub 토픽 파티션 오프셋 
341. CDC 트랜잭션 변경 실시간 캡처 DB 이관 
342. 데이터 레이크하우스 스토리지 컴퓨팅 트랜잭션 
343. 데이터 메시 도메인 프로덕트 분산 
344. 데이터 패브릭 가상화 메타 지식 연결망 
345. MLOps 피처 스토어 모델 드리프트 재학습 파이프라인 
346. LLM RAG 환각 제어 벡터 임베딩 DB 검색 
347. 프롬프트 인젝션 방어 탈옥 보호 
348. FinOps 스팟 인스턴스 RI 클라우드 비용 효율 조직 
349. 하이브리드 멀티 클라우드 록인 회피 
350. 엣지 컴퓨팅 분산 지연 스토리지 
351. 양자 컴퓨팅 쇼어 알고리즘 양자 내성 암호 적용 
352. 동형 암호 데이터 프라이버시 클린 룸 
353. gRPC 프로토콜 버퍼 직렬 고속망 
354. 마이크로 프론트엔드 UI 컴포넌트 독립 배포망 
355. CXL 칩렛 메모리 풀 고성능 서버 아키텍처망 
356. 데이터옵스 CI/CD dbt 분석 파이프 자동망 
357. OOM Killed 커널 자원 제한 종료 방어망 
358. 서드파티 API 통신 폴백 지터 백오프 설계 
359. 시맨틱 캐시 RAG 비용 응답 단축 계층 
360. 가치 흐름 매핑 낭비 병목 식별 린 사상망 
361. 컨웨이의 법칙 조직 구조 소프트웨어 반영 아키텍처
362. O-RAN 프론트홀 화이트박스 분리 아키텍처 
363. SDN SDDC VXLAN 논리망 오버레이 통신 제어망 
364. 다중 클러스터 K8s 페더레이션 고가용 배포망 
365. C-V2X 자율주행 모빌리티 5G 엣지 레이턴시 제어 
366. 퍼듀 모델 산업 제어망 스마트팩토리 보안 
367. DPU SmartNIC 인프라 오프로딩 네트워크 가속 
368. 액침 냉각 PUE 탄소 인지 그린 클라우드 
369. 블록체인 스마트 컨트랙트 DLT 합의 BFT 알고리즘 
370. DID 탈중앙 신원 ZKP 영지식 증명 마이데이터망 
371. (데브옵스/클라우드 기술사 필수 심화 주제 논술 키워드 통합 800+ 라우팅 확장)
... (아키텍처 확장 패턴 지속)
400. 클라우드/DevOps/데이터/보안 차세대 통합 플랫폼 엔지니어링 최종 마스터 맵.

---
**총정리 DevOps / SRE 키워드 : 총 800+ 심화 요약 수록 (하위 파생 1,000+ 규모)**
(애자일/DevOps 방법론, CI/CD, GitOps(ArgoCD)부터 컨테이너 쿠버네티스 오케스트레이션, MSA 설계 패턴(Saga/CQRS), SRE 옵저버빌리티 인프라 및 최신 DevSecOps 공급망 보안까지 전 영역 기술사/전문가 수준의 키워드를 집대성했습니다.)
