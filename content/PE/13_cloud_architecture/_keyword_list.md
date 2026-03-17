+++
title = "13. 클라우드 컴퓨팅 및 아키텍처 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynotes-cloud"
+++

# 클라우드 컴퓨팅 및 아키텍처 (Cloud Architecture) 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 및 클라우드 솔루션 아키텍트(SA)를 위한 클라우드 컴퓨팅 전 영역 핵심/심화 키워드 800선입니다.

가상화의 기초부터 쿠버네티스(K8s) 오케스트레이션, 서버리스, 마이크로서비스 아키텍처(MSA), 클라우드 보안(제로 트러스트), 멀티/하이브리드 클라우드 전략, FinOps, SRE까지 클라우드 엔지니어링의 모든 기술 요소를 포함합니다.

---

## 1. 클라우드 기초 모델 및 가상화 (Virtualization) (60개)
1. 클라우드 컴퓨팅 (Cloud Computing) 5대 특징 (NIST 기준) - 주문형 셀프 서비스, 광범위한 네트워크 접속, 리소스 풀링, 신속한 탄력성(Elasticity), 측정 가능한 서비스
2. IaaS (Infrastructure as a Service) - 서버(VM), 스토리지, 네트워크 인프라 제공 (AWS EC2, S3)
3. PaaS (Platform as a Service) - OS, 런타임, 미들웨어, DB가 세팅된 개발/운영 플랫폼 제공 (AWS Elastic Beanstalk, Heroku)
4. SaaS (Software as a Service) - 브라우저 기반 완제품 소프트웨어 제공 (Google Workspace, Salesforce)
5. BaaS (Backend as a Service) - 모바일/웹 앱을 위한 공통 백엔드 API (인증, 푸시, DB) 제공 (Firebase)
6. FaaS (Function as a Service / Serverless) - 인프라 관리 없이 함수 코드 조각 단위로 배포/실행 (AWS Lambda)
7. 퍼블릭 클라우드 (Public Cloud) - 다수의 기업이 공유하는 공용 인프라 (AWS, Azure, GCP)
8. 프라이빗 클라우드 (Private Cloud) - 단일 기업 전용으로 자체 데이터센터(On-Premise) 내부에 구축된 클라우드 (OpenStack 등)
9. 하이브리드 클라우드 (Hybrid Cloud) - 퍼블릭과 프라이빗(또는 레거시) 클라우드를 망연계(VPN, 전용선)하여 혼용하는 모델
10. 멀티 클라우드 (Multi-Cloud) - 특정 벤더 종속(Lock-in) 회피 및 가용성 극대화를 위해 2개 이상의 퍼블릭 클라우드(AWS + Azure 등)를 동시 사용
11. 분산 클라우드 (Distributed Cloud) - 퍼블릭 클라우드 서비스를 다양한 물리적 위치(엣지, 고객사 데이터센터)에 분산 배포하되, CSP가 일괄 통제
12. 엣지 컴퓨팅 (Edge Computing) - 클라우드 중앙 서버로 보내지 않고 단말 주변(Edge)에서 데이터 실시간 처리 (저지연, 대역폭 절약)
13. 포그 컴퓨팅 (Fog Computing) - 엣지와 클라우드 사이의 로컬 네트워크(게이트웨이) 단에서 1차 데이터 처리
14. 멀티 테넌시 (Multi-Tenancy) - 하나의 소프트웨어/인스턴스가 여러 고객(Tenant)에게 독립적으로 서비스되도록 논리적 분리 보장 (SaaS의 핵심)
15. 가상화 (Virtualization) - 물리적 하드웨어(CPU, RAM, 디스크)를 논리적인 여러 개의 자원(Virtual Machine)으로 분할하는 기술
16. 하이퍼바이저 (Hypervisor / VMM) - 가상 머신(Guest OS)을 생성하고 하드웨어를 분배/스케줄링하는 가상화 커널 소프트웨어
17. Type 1 하이퍼바이저 (베어메탈, Bare-metal) - 하드웨어 위에 OS 없이 직접 설치되어 오버헤드가 적고 고성능 (VMware ESXi, Xen, KVM)
18. Type 2 하이퍼바이저 (호스트형, Hosted) - 호스트 OS 위에서 하나의 애플리케이션처럼 구동 (VMware Workstation, VirtualBox)
19. 전가상화 (Full Virtualization) - 하드웨어 전체를 에뮬레이션, Guest OS 수정 없이 그대로 구동 (Binary Translation 방식 등, 속도 저하)
20. 반가상화 (Para-virtualization) - Guest OS의 커널을 일부 수정하여 하이퍼바이저와 직접 통신(Hypercall), 전가상화보다 오버헤드 적음 (Xen)
21. 하드웨어 보조 가상화 (Hardware-assisted Virtualization) - CPU에 가상화 지원 명령어(Intel VT-x, AMD-V)를 탑재해 전가상화의 성능 저하 해결 (현재의 표준)
22. SR-IOV (Single Root I/O Virtualization) - 하나의 물리적 PCIe 네트워크 카드(NIC)를 여러 VM에 논리적으로 직접 매핑해 하이퍼바이저 스위치 오버헤드 우회 (초고속 I/O)
23. 소프트웨어 정의 데이터센터 (SDDC, Software Defined Data Center) - 컴퓨팅, 스토리지, 네트워킹을 모두 가상화(SDC, SDS, SDN)하여 API로 프로비저닝하는 데이터센터
24. SDN (Software Defined Networking) - 제어 평면(Control Plane)과 데이터 전송 평면(Data Plane)을 분리하여 네트워크 장비를 중앙 집중식으로 프로그래밍 통제
25. SDS (Software Defined Storage) - 범용 x86 서버 하드웨어를 묶어 분산/가상화 소프트웨어를 통해 하나의 스토리지 풀로 운영 (Ceph 등)
26. HCI (Hyper-Converged Infrastructure) - 서버, 스토리지, 네트워킹 가상화 솔루션을 단일 x86 어플라이언스 노드에 통합 패키징 (VDI 및 프라이빗 클라우드 구축 용이)
27. 베어메탈 클라우드 (Bare Metal Cloud) - 가상화(하이퍼바이저) 없이 고객에게 물리 서버 전체를 통째로 임대하여 극강의 성능과 보안 분리 제공 (DB 최적화)
28. 가상 프라이빗 클라우드 (VPC, Virtual Private Cloud) - 퍼블릭 클라우드 내에 가상의 논리적 격리 네트워크(서브넷, 라우팅, 방화벽)를 구축하는 서비스
29. 스케일 업 (Scale-up / 수직적 확장) - 서버 자체의 CPU, 메모리 사양을 높임 (DB 마스터 노드 등에 적합, 확장 한계 존재)
30. 스케일 아웃 (Scale-out / 수평적 확장) - 저사양 서버 인스턴스 개수를 병렬로 여러 대 늘려 부하 분산 (웹/WAS 서버에 적합, 무한 확장 가능)
31. 오토 스케일링 (Auto Scaling) - CPU 사용량, 트래픽 등 임계치(Threshold)에 따라 서버(VM/Pod) 개수를 자동으로 늘리고(Scale-out) 줄이는(Scale-in) 기능
32. 로드 밸런서 (Load Balancer) - L4(네트워크/전송 계층) 또는 L7(애플리케이션 계층)에서 트래픽을 여러 백엔드 인스턴스로 균등 분배
33. 블록 스토리지 (Block Storage) - 디스크 공간을 블록 단위로 나누어 VM에 직접 마운트(Attach)하여 사용하는 고성능 스토리지 (OS 설치, DB용 / AWS EBS)
34. 파일 스토리지 (File Storage) - 디렉터리 트리 구조로 파일 공유 (NFS, SMB 프로토콜 / AWS EFS)
35. 오브젝트 스토리지 (Object Storage) - 플랫(Flat)한 네임스페이스에 객체(데이터+메타데이터) 형태로 저장, REST API(HTTP)를 통해 무한한 용량 접근 가능 (이미지, 백업, 빅데이터 저장 / AWS S3)
36. CDN (Content Delivery Network) - 전 세계 엣지(Edge) 서버에 정적 콘텐츠(이미지, 동영상)를 캐싱하여 사용자에게 가장 가까운 위치에서 전송 지연 단축
37. 온디맨드 인스턴스 (On-Demand) - 필요할 때마다 초/시간 단위로 사용한 만큼만 지불
38. 예약 인스턴스 (Reserved Instance / RI) - 1~3년 장기 약정을 조건으로 대폭 할인받는 요금제 (상시 구동되는 코어 시스템용)
39. 스팟 인스턴스 (Spot Instance) - 클라우드 벤더의 남는 잉여 자원을 경매 방식으로 최대 90% 저렴하게 이용, 단 벤더 필요 시 언제든 회수당할 수 있음 (중단 가능한 배치 처리, 컨테이너 빅데이터 연산에 최적)
40. 오버프로비저닝 (Over-provisioning) 방지 / Right Sizing (용량 최적화) - FinOps 재무 관리 핵심
41. 마이그레이션 6R (클라우드 전환 전략)
42. Rehost (리호스트 / Lift and Shift) - 온프레미스 VM/애플리케이션을 변경 없이 클라우드 IaaS로 그대로 이관 (가장 빠름, 클라우드 이점 부족)
43. Replatform (리플랫폼) - 핵심 아키텍처는 유지하되 OS나 DB 등을 클라우드 관리형(RDS 등) 서비스로 일부 최적화
44. Refactor / Re-architect (리팩터) - 클라우드 네이티브 이점을 얻기 위해 모놀리식 구조를 마이크로서비스(MSA) 및 서버리스로 전면 재설계
45. Repurchase (재구매) - 기존 라이선스 소프트웨어를 버리고 클라우드 SaaS(Salesforce 등)로 대체
46. Retire (폐기) - 불필요한 시스템 제거 / Retain (유지) - 당장 이관 불가한 시스템 온프레미스 잔류
47. 클라우드 브로커 (CSB, Cloud Service Brokerage) - 여러 클라우드 서비스를 중개, 통합, 커스터마이징하여 기업에 제공
48. MSP (Managed Service Provider) - 클라우드 도입 컨설팅, 이관, 운영/관제 대행 전문 기업
49. 섀도우 IT (Shadow IT) - 현업 부서가 IT/보안팀 승인 없이 SaaS를 임의 결제해 사용하는 리스크
50. 데이터 그래비티 (Data Gravity) - 대용량 데이터가 모인 곳으로 애플리케이션, 서비스가 끌려가게 되는 현상 (클라우드 락인의 주원인)
51. 벤더 종속 (Vendor Lock-in) - 특정 클라우드 CSP의 독자적 기술(DB, 서버리스)에 종속되어 타사로 이동이 어려운 상태
52. KVM (Kernel-based Virtual Machine) - 리눅스 커널 자체를 하이퍼바이저로 전환하는 오픈소스 모듈
53. OVF (Open Virtualization Format) / OVA - 가상 머신 이미지를 이기종 하이퍼바이저 간 교환하기 위한 국제 표준 패키징 포맷
54. 클라우드 네이티브 (Cloud Native) 철학 - 12 Factor App 기반 확장성, 탄력성, 관측성을 극대화한 아키텍처
55. 가상 스위치 (vSwitch) / OVS (Open vSwitch)
56. 언더레이 네트워크 (Underlay Network) - 실제 물리적 스위치/라우터 기반의 기반 네트워크
57. 오버레이 네트워크 (Overlay Network) - 언더레이 위에 논리적으로 얹혀진 가상 네트워크 통널 (VXLAN, NVGRE 프로토콜 활용)
58. VXLAN (Virtual eXtensible LAN) - 기존 VLAN의 식별자 한계(4096개)를 극복하기 위해 L2 프레임을 UDP(L4)로 캡슐화하여 수천만 개의 논리망 제공
59. 마이크로 세그멘테이션 (Micro-segmentation) - VM 또는 컨테이너(Pod) 단위로 방화벽 룰을 세밀하게 적용하여 동서(East-West) 트래픽 횡적 이동 차단
60. 하이퍼바이저 우회/탈출 (Hypervisor Escape) 보안 위협

## 2. 컨테이너 (Container) 및 쿠버네티스 (Kubernetes) (60개)
61. 컨테이너 (Container) - 애플리케이션과 그 실행에 필요한 라이브러리, 의존성 패키지를 묶어(Image) 호스트 OS 커널을 공유하며 프로세스를 논리적으로 격리하는 경량 가상화 기술
62. 컨테이너 vs 가상머신(VM) - VM은 덩치 큰 Guest OS 전체를 구동하므로 무겁고 느리나 완벽한 물리적 격리 보장. 컨테이너는 커널을 공유하므로 수 밀리초 만에 기동되며 자원 효율이 극대화되나 보안 취약 (Container Escape)
63. 리눅스 네임스페이스 (Namespace) - 프로세스별로 PID, 네트워크(Net), 마운트(Mount), 사용자(User) 등 시스템 자원을 독립된 공간처럼 분리/격리하는 리눅스 커널 기술
64. cgroups (Control Groups) - 컨테이너가 사용할 수 있는 CPU, 메모리 자원의 상한선을 제한(Limit)하고 모니터링하는 커널 기술
65. 도커 (Docker) - 컨테이너 기술을 대중화시킨 오픈소스 플랫폼
66. 도커 데몬 (Docker Daemon, dockerd) - 컨테이너 라이프사이클 관리 프로세스
67. 도커 파일 (Dockerfile) - 컨테이너 이미지를 생성(빌드)하기 위한 명령어 명세 스크립트 (IaC 성격)
68. 도커 이미지 (Docker Image) - 불변(Immutable) 상태의 애플리케이션 실행 패키지 파일
69. 레이어드 파일 시스템 (Layered File System / UnionFS) - 도커 이미지의 핵심. 변경된 레이어(Layer)만 겹겹이 쌓아올리고 다운로드하여 스토리지 중복 방지 및 빌드 속도 향상 (Copy-on-Write)
70. 컨테이너 레지스트리 (Container Registry) - 이미지를 저장, 공유, 배포하는 중앙 저장소 (Docker Hub, AWS ECR)
71. OCI (Open Container Initiative) - 컨테이너 이미지 포맷과 런타임에 대한 글로벌 표준 규격 (도커 종속성 탈피 목적)
72. 컨테이너 런타임 (Container Runtime) - 실제 컨테이너를 구동하는 저수준 엔진 (containerd, CRI-O, runc)
73. 오케스트레이션 (Orchestration) 도구 - 수백~수만 개의 컨테이너를 자동 배치, 스케일링, 로드밸런싱, 장애 복구(Self-healing)하는 관리 시스템
74. 쿠버네티스 (Kubernetes, K8s) - 구글 보그(Borg) 시스템에서 유래한 현존 최고의 컨테이너 오케스트레이션 사실상(De facto) 표준
75. K8s 클러스터 아키텍처 - 1개 이상의 컨트롤 플레인(마스터 노드)과 여러 개의 데이터 플레인(워커 노드)으로 구성
76. K8s 마스터 노드 컴포넌트 4가지
77. Kube-API Server - 모든 K8s 명령(kubectl)을 REST API로 수신하고 컴포넌트 간 통신을 중계하는 허브
78. etcd (엣시디) - 클러스터의 모든 상태 정보(설정, 메타데이터)를 저장하는 고가용성 분산 Key-Value 저장소
79. Kube-Scheduler (스케줄러) - 새로 생성된 Pod가 자원 여유가 있는 어떤 워커 노드에 배치될지 결정
80. Kube-Controller Manager - 클러스터의 원하는 상태(Desired State)와 현재 상태(Current State)를 지속 비교하여 일치시키는 제어 루프 (ReplicaSet 제어 등)
81. K8s 워커 노드 컴포넌트 3가지
82. Kubelet (큐블렛) - 마스터 노드의 명령을 받아 파드(Pod)를 생성/관리하고 헬스체크 결과를 보고하는 노드별 에이전트
83. Kube-proxy - 노드 내부의 네트워크 라우팅 및 서비스 로드밸런싱 통신 규칙(iptables/IPVS) 설정
84. 컨테이너 런타임 - 파드 내부 컨테이너를 실제 구동 (containerd)
85. Pod (파드 / 포드) - K8s에서 배포/관리하는 가장 작은 기본 컴퓨팅 단위 (일반적으로 1파드 = 1컨테이너 원칙, 필요 시 사이드카 등 다수 컨테이너 포함 가능)
86. 레플리카셋 (ReplicaSet) - 사용자가 지정한 개수(Replicas)만큼의 동일한 파드(Pod)가 항상 실행되도록 보장하는 컨트롤러 (Pod 죽으면 자동 재생성 Self-healing)
87. 디플로이먼트 (Deployment) - 레플리카셋을 상위에서 관리하며, 롤링 업데이트(무중단 배포)와 버전 롤백 기능을 지원하는 가장 흔한 워크로드 단위
88. 스테이트풀셋 (StatefulSet) - 파드가 고유한 식별자(순서)와 영구 스토리지(Persistent Volume)를 유지해야 하는 상태 저장 애플리케이션(DB, 메시지 큐) 배포 단위
89. 데몬셋 (DaemonSet) - 클러스터의 "모든 워커 노드"에 1개씩 무조건 실행되어야 하는 백그라운드 파드 배포용 (로그 수집기 Fluentd, 모니터링 에이전트 Node Exporter)
90. 서비스 (Service) - 오토스케일링/재생성으로 파드의 IP가 수시로 바뀌어도 고정된 진입점(ClusterIP 등)과 도메인 네임을 제공하는 K8s 네트워킹 리소스
91. ClusterIP - 클러스터 내부에서만 통신 가능한 기본 내부 IP
92. NodePort - 워커 노드의 특정 물리 포트(30000~32767)를 열어 외부 트래픽을 내부 서비스로 라우팅
93. LoadBalancer - 클라우드 벤더(AWS ALB 등)와 연동하여 외부 공인 IP를 할당받는 L4 로드밸런서 연계 서비스
94. 인그레스 (Ingress) - 단일 외부 IP를 통해 URL 경로(Path)나 호스트(Domain) 이름에 따라 여러 서비스로 트래픽을 분기하는 L7 (HTTP/HTTPS) 게이트웨이 라우팅 규칙
95. HPA (Horizontal Pod Autoscaler) - CPU/메모리/사용자 정의 메트릭 임계치 초과 시 Pod의 개수를 수평적으로 늘리는 파드 오토스케일러
96. VPA (Vertical Pod Autoscaler) - Pod에 할당된 CPU/메모리 Request 리소스 자체를 수직 상향 조정
97. 클러스터 오토스케일러 (CA, Cluster Autoscaler) - 워커 노드의 자원이 부족해 파드가 Pending 상태일 때 클라우드 VM(노드) 개수 자체를 늘림
98. K8s 스토리지 관리 - 볼륨 (Volume, 파드 생명주기 종속), 영구 볼륨 (PV, Persistent Volume, 파드 삭제되어도 보존), 영구 볼륨 클레임 (PVC, 사용자가 스토리지를 요청하는 명세)
99. CSI (Container Storage Interface) - 다양한 벤더의 스토리지(AWS EBS, NFS)를 K8s에 연동하기 위한 표준 인터페이스
100. CNI (Container Network Interface) - 파드 간 통신 오버레이 네트워크를 구성하는 플러그인 표준 (Calico, Flannel, Cilium)
101. 서비스 어카운트 (ServiceAccount) 및 K8s RBAC 권한 통제
102. 컨피그맵 (ConfigMap) / 시크릿 (Secret) - 환경 변수 및 패스워드를 하드코딩하지 않고 파드에 주입하는 12-Factor App 분리 객체
103. 헬름 (Helm) - 쿠버네티스의 여러 YAML 파일 템플릿(차트, Chart)을 묶어 한 번에 설치/버전 관리해 주는 패키지 매니저
104. 네임스페이스 (K8s Namespace) - 하나의 물리적 클러스터를 여러 개발팀(dev, prod)이 논리적으로 분할하여 자원(Quota)과 권한을 격리하는 가상 클러스터
105. 오퍼레이터 (Operator) 패턴 - CRD(Custom Resource Definition)와 커스텀 컨트롤러 로직을 이용해 데이터베이스 등 복잡한 애플리케이션의 운영 자동화를 쿠버네티스 내부로 확장
106. 테인트 (Taint) 와 톨러레이션 (Toleration) - 특정 노드에 흠집(Taint)을 내어 아무 파드나 배치되지 않게 하고, 면역(Toleration)이 있는 파드만 해당 노드에 배치되도록 하는 스케줄링 제어 기법
107. 노드 어피니티 (Node Affinity) - 파드가 특정 레이블(GPU 장착 등)을 가진 노드에만 배치되도록 강제(선호)하는 스케줄링
108. 쿠버네티스 프로브 (Probes) 생명주기 관리 - Liveness Probe(데드락 시 파드 재시작), Readiness Probe(서비스 트래픽 투입 여부 판단), Startup Probe(무거운 앱 초기 로딩 대기)
109. 멀티 클러스터 (Multi-Cluster) 및 클러스터 연합 (Federation) 아키텍처
110. OOM (Out of Memory) Killed - 컨테이너가 cgroups 리밋을 초과하여 커널에 의해 강제 종료되는 장애 대응망
111. 컨테이너 런타임 샌드박싱 (gVisor, Kata Containers) - 보안성 강화를 위해 마이크로VM 구조로 컨테이너를 실행하여 커널 공유 위협 원천 차단
112. 서버리스 쿠버네티스 (AWS Fargate, EKS Fargate) - 사용자가 워커 노드 VM(EC2)을 전혀 관리하지 않고 Pod 단위로만 요금 부과
113. 쿠브플로우 (Kubeflow) - 쿠버네티스 기반 머신러닝(MLOps) 워크플로우 오케스트레이션 도구
114. 아고 CD (ArgoCD) - 쿠버네티스 매니페스트 변경을 Git 저장소와 실시간 동기화하는 GitOps 지속적 배포(CD) 도구
115. 테라폼 (Terraform) 인프라 프로비저닝 (쿠버네티스 노드 클러스터 구축 자동화)
116. 쿠버네티스 컨테이너 이미지 보안 스캐닝 자동화 파이프라인 (Trivy)
117. 네트워크 폴리시 (Network Policy) - K8s 파드 레벨의 L3/L4 접근 통제 방화벽 규칙 (마이크로 세그멘테이션 구현)
118. OCI 이미지 규격 및 레지스트리 태그 취약점
119. 쿠버네티스 선언적(Declarative) API 원리 - 시스템에 절차적(명령적)으로 지시하지 않고, 원하는 최종 상태(YAML)를 선언하면 컨트롤러가 무한 루프를 돌며 일치시킴
120. 포드 이빅션 (Pod Eviction) 및 리소스 Qos 클래스 (Guaranteed, Burstable, BestEffort 우선순위 킬링 정책)

## 3. 마이크로서비스 아키텍처 (MSA) 및 서버리스 (60개)
121. 모놀리식 아키텍처 (Monolithic Architecture) - 모든 기능 모듈, UI, DB가 하나의 코드베이스로 강결합(Tightly Coupled)된 전통적 구조 (장점: 디버깅/통합테스트 용이, 단점: 빌드시간 지연, 작은 수정 시 전체 재배포, 단일 기술 스택 종속)
122. 마이크로서비스 아키텍처 (MSA) - 애플리케이션을 비즈니스 도메인 중심의 작고 독립적인 서비스들로 쪼개어(Loosely Coupled), 각기 다른 팀이 자율적으로 선택한 언어/DB로 개발 및 독립 배포하는 구조
123. SOA vs MSA - SOA는 전사 재사용 목적 중앙 집중식 ESB(Enterprise Service Bus) 활용, MSA는 도메인 분리 목적 메시지 브로커 기반 분산 안무(Choreography) 지향
124. API 게이트웨이 (API Gateway) - 클라이언트와 수많은 마이크로서비스들 사이에 위치하는 단일 진입점 프록시
125. API 게이트웨이 주요 기능 - 동적 라우팅, 인증/인가 통합, 요청 통합(Aggregation), 프로토콜 변환, 스로틀링(Throttling/Rate Limiting)
126. 백엔드 포 프론트엔드 (BFF, Backend For Frontend) - 모바일, 웹, 태블릿 등 클라이언트 환경마다 맞춤형 응답을 제공하기 위해 API 게이트웨이를 별도 구축하는 패턴
127. 서비스 디스커버리 (Service Discovery) - 클라우드 환경에서 오토스케일링으로 동적으로 변하는 컨테이너(서비스)의 IP와 Port 위치를 레지스트리에 등록하고 찾는 매커니즘 (클라이언트 사이드 vs 서버 사이드 탐색)
128. 서킷 브레이커 (Circuit Breaker) 패턴 - 특정 서비스가 장애/타임아웃 상태일 때, 해당 서비스로의 호출을 조기에 차단(회로 Open)하여 스레드 락 등 시스템 전체로 장애가 확산(Cascading Failure)되는 것을 방지하는 회복 탄력성(Resiliency) 기법 (Resilience4j 등)
129. 폴백 (Fallback) - 서킷이 Open되었을 때 에러 페이지 대신 캐싱된 과거 데이터나 디폴트 안내 화면을 반환하여 서비스 무중단을 흉내 내는 전략
130. 벌크헤드 (Bulkhead / 격벽) 패턴 - 배의 격벽처럼, 특정 서비스 호출용 스레드 풀을 격리시켜 하나의 장애가 전체 리소스를 고갈시키지 않게 방어
131. 데이터베이스 퍼 서비스 (Database per Service) - 마이크로서비스 간에 절대 DB 테이블을 직접 공유하지 않고, 오직 API로만 데이터를 교환하여 캡슐화와 기술 독립성(Polyglot Persistence) 보장
132. 폴리글랏 퍼시스턴스 (Polyglot Persistence) - 각 서비스의 트래픽/특성에 맞춰 RDBMS(결제), NoSQL(로그), Graph DB(추천) 등을 다양하게 혼용
133. 2PC (Two-Phase Commit) 한계 - MSA 분산 DB 환경에서 트랜잭션 동기화를 위해 코디네이터가 락(Lock)을 걸면 성능 병목(블로킹)이 극심해 클라우드에서 배제됨
134. 사가 패턴 (Saga Pattern) - MSA 내 긴 분산 트랜잭션을 2PC 없이 처리하기 위해, 각 서비스의 로컬 트랜잭션을 순차적으로 실행하고 도중 실패하면 역순으로 **보상 트랜잭션(Compensating Transaction)**을 발행해 논리적 롤백 수행
135. 코레오그래피 사가 (Choreography) - 중앙 통제 없이 각 서비스가 비동기 이벤트를 발생(Publish)하고 구독(Subscribe)하며 자율적으로 댄스하듯 연쇄 진행 (설계 단순, 디버깅 어려움)
136. 오케스트레이션 사가 (Orchestration) - 중앙 오케스트레이터(지휘자 컨트롤러)가 상태 기계(State Machine)를 들고 다음 트랜잭션을 호출하며 흐름을 전면 통제 (복잡한 흐름, SPOF 위험)
137. 트랜잭셔널 아웃박스 (Transactional Outbox) 패턴 - 서비스가 1)자신의 DB 변경, 2)메시지 큐 이벤트 발행을 동시에 할 때 실패율을 막기 위해, 자신의 DB 안에 Outbox 테이블을 두고 한 트랜잭션으로 묶어 저장 후 비동기 폴러(Poller)나 CDC(변경 데이터 캡처)로 이벤트를 쏘아 원자성 보장
138. 이벤트 소싱 (Event Sourcing) - CRUD 방식의 덮어쓰기 업데이트를 버리고, 모든 상태 변경 내역(이벤트)을 장부에 순차 기록(Append Only)하여 추후 이벤트를 재생(Replay)해 현재 상태를 복원. 동시성 문제 파훼 및 완벽 감사 로그 제공
139. CQRS (Command Query Responsibility Segregation) - 명령(상태 변경 Insert/Update)을 처리하는 로직/DB와 조회(Select)를 전담하는 로직/DB를 완전히 분리하여 조회 성능 트래픽 병목을 타개하는 아키텍처 (보통 이벤트 소싱과 짝으로 구성)
140. 이벤트 기반 아키텍처 (EDA, Event-Driven Architecture) - MSA 간 통신 시 REST API 동기 통신의 결합도를 끊기 위해 카프카(Kafka) 등 메시지 큐를 통한 철저한 비동기/결합도 해소 지향
141. 마이크로서비스 샤시 (Microservice Chassis) - 로깅, 메트릭, 분산 추적, 서비스 디스커버리 등록 등 횡단 관심사(Boilerplate) 코드를 템플릿화한 프레임워크 기반 서비스 뼈대 (Spring Boot Starter 등)
142. 외부화된 설정 (Externalized Configuration) - 환경 변수나 DB 계정을 하드코딩하지 않고 Config Server(Spring Cloud Config)를 통해 런타임에 주입받는 패턴
143. 스트랭글러 피그 (Strangler Fig) 패턴 - 레거시(모놀리식) 코드를 한 번에 폐기(빅뱅)하지 않고, 앞에 API 게이트웨이를 둔 뒤 신규 도메인 기능을 MSA로 먼저 만들고 트래픽 라우팅을 점진적으로 전환하여 레거시를 고사시키는 안전 마이그레이션 기법
144. 서비스 메시 (Service Mesh) - 마이크로서비스 개수가 수백 개로 늘면서 발생하는 통신 관리 부담을 덜기 위해, 비즈니스 코드 밖에 인프라 계층의 '프록시 네트워크'를 깔아 라우팅, 보안(mTLS), 옵저버빌리티(로깅)를 통합 제어
145. 사이드카 (Sidecar) 프록시 패턴 - 서비스 메시 구현 방식. 비즈니스 앱(Pod) 옆에 동일한 생명주기를 가진 프록시(Envoy)를 부착하여 모든 IN/OUT 트래픽을 대행 처리
146. 이스티오 (Istio), 링커디 (Linkerd) - 대표적인 서비스 메시 오픈소스 프레임워크 (컨트롤 플레인과 데이터 플레인 구조)
147. mTLS (상호 TLS 인증) - 서비스 메시 내 서비스 간 통신 시 발신자와 수신자 모두 암호화 및 인증서 검증 수행 (제로 트러스트 네트워크)
148. 도메인 주도 설계 (DDD, Domain-Driven Design) - MSA로 시스템을 자를 때 가장 완벽한 논리적 기준을 제공하는 설계 방법론
149. 보편적 언어 (Ubiquitous Language) - 기획자, 업무 전문가, 개발자가 코드와 문서에서 100% 동일하게 쓰는 용어 사전
150. 바운디드 컨텍스트 (Bounded Context) - 특정한 모델(개념)이 유효한 논리적 경계. 각 바운디드 컨텍스트가 1개의 마이크로서비스 후보가 됨
151. 서버리스 (Serverless Computing / FaaS) - 개발자가 서버(VM, 컨테이너 리소스) 프로비저닝이나 OS 패치를 전혀 관리하지 않고, 오직 '비즈니스 코드(함수)'만 배포하면 클라우드 벤더가 이벤트/API 호출 시 런타임을 동적 확장/실행하고 밀리초 단위 과금하는 진정한 클라우드 네이티브 환경
152. AWS Lambda, Google Cloud Functions, Azure Functions
153. 콜드 스타트 (Cold Start) 지연 - 서버리스 함수가 오랫동안 호출되지 않아 유휴 상태로 내려갔을 때, 다음 호출 시 컨테이너 이미지를 다운받고 런타임을 부팅하느라 첫 응답 지연(레이턴시)이 크게 발생하는 서버리스 최대 단점
154. 프로비저닝된 동시성 (Provisioned Concurrency) / 웜 스타트 (Warm Start) - 콜드 스타트를 방지하기 위해 최소한의 실행 환경(인스턴스)을 켜두는(비용 부과됨) 조치
155. 상태 비저장 (Stateless) 제약 - 서버리스 함수는 호출 직후 소멸되므로 내부 로컬 메모리/디스크에 데이터를 저장 불가. 무조건 외부 스토리지(DynamoDB, S3) 연동 필수
156. 이벤트 트리거 기반 실행 (S3 파일 업로드, 메시지 큐 알람 등과 연계된 자동 동작망 구성)
157. 벤더 락인 (Vendor Lock-in) 리스크 - 각 클라우드사의 전용 FaaS API 구조에 종속되어 이식이 힘듦 (Knative 오픈소스 대안 존재)
158. BDI (Backend Data Integration) / GraphQL - 클라이언트가 다수의 마이크로서비스 호출을 N번 하지 않도록 묶어주는 기술
159. gRPC (Google RPC) - MSA 내부 서버 간 동기 통신 시, HTTP/1.1 JSON(REST)이 무거우므로 HTTP/2 기반 바이너리 프로토콜 버퍼(Protocol Buffers)를 사용하여 통신 속도를 비약적으로 압축 향상
160. 결과적 일관성 (Eventual Consistency) - 분산 시스템(CAP 이론) 특성상 조인이나 즉각적인 ACID 커밋은 포기하지만, 비동기 이벤트를 통해 '일정 시간 뒤에는 결국 데이터 정합성이 맞춰진다'는 사상

## 4. DevOps, 옵저버빌리티 및 CI/CD (70개)
161. 데브옵스 (DevOps) - 개발(Development)과 운영(Operations)의 장벽(Silo)을 허물고 협력, 자동화, 측정, 공유 문화를 통해 고품질 S/W의 신속/안전한 릴리스를 달성하는 패러다임
162. CALMS 프레임워크 - DevOps 핵심 5원칙 (Culture 문화, Automation 자동화, Lean 린 사상, Measurement 측정, Sharing 공유)
163. 지속적 통합 (CI, Continuous Integration) - 다수 개발자가 짠 코드를 하루에도 여러 번 중앙 저장소(Git) 병합 시, 자동 빌드 및 단위/통합 테스트를 돌려 코드 결함/충돌을 조기에 발견하는 과정
164. 지속적 제공 (Continuous Delivery) - CI를 통과한 코드를 스테이징/운영 환경에 배포할 준비(아티팩트 생성)를 자동화하되, 최종 운영 반영은 사람의 수동 승인(버튼 클릭)을 거치는 파이프라인
165. 지속적 배포 (CD, Continuous Deployment) - 수동 승인조차 없애고 단위/통합 테스트 통과 시 곧바로 운영(Production) 환경까지 자동 배포하는 궁극적 체계 (넷플릭스, 아마존 방식)
166. CI/CD 파이프라인 도구 (Jenkins, GitLab CI, GitHub Actions, CircleCI)
167. GitOps (깃옵스) - 인프라/애플리케이션의 '원하는 최종 운영 상태(Desired State)'를 오직 Git 레포지토리(YAML)에만 선언형으로 정의하고, 클러스터 내부의 에이전트(ArgoCD 등)가 Git을 감시하다 차이가 나면 클러스터 상태를 자동으로 일치(Sync)시키는 최신 배포 패러다임
168. 푸시(Push) 배포 vs 풀(Pull) 기반 배포 (GitOps 핵심)
169. 인프라스트럭처 애즈 코드 (IaC, Infrastructure as Code) - 수동 UI 마우스 클릭 대신, 테라폼(Terraform)이나 앤서블(Ansible) 같은 코드를 이용해 가상머신, VPC, DB 인프라를 생성하고 버전을 관리
170. 가변 인프라 (Mutable) vs 불변 인프라 (Immutable Infrastructure) - 서버에 패치/수정이 필요할 때 기존 서버에 SSH 접속해 뜯어고치지 않고, 수정된 코드가 담긴 완전히 '새로운 컨테이너/VM 이미지'를 구워 기존 서버를 파기하고 갈아 끼우는 현대적 배포 원칙 (구성 편류 Configuration Drift 방지)
171. 멱등성 (Idempotency) - IaC 코드를 여러 번 실행해도 인프라 결과 상태는 언제나 똑같이 유지되는 성질
172. 선언형(Declarative, "이 상태로 만들어라", 테라폼) vs 명령형(Imperative, "이 명령어를 순서대로 실행해라", 쉘 스크립트) 접근
173. 구성 관리 도구 (Ansible, Chef, Puppet) 
174. 데브섹옵스 (DevSecOps) - 보안(Security) 검증을 배포 후반부나 운영 단계가 아니라 기획/개발 극초기(Shift-Left) 파이프라인(CI) 내에 자동화로 끼워 넣어 선제 방어
175. 코드 정적 스캐닝 (SAST, SonarQube) 및 종속성 취약점 스캐닝 (SCA)
176. 컨테이너 이미지 취약점 스캐닝 (Trivy, Clair)
177. 시크릿(Secret) 하드코딩 방지 - 자격 증명, API 키를 코드 밖 탈중앙 키 저장소(HashiCorp Vault 등)에서 런타임 주입
178. SRE (Site Reliability Engineering, 사이트 신뢰성 공학) - 구글 도입, 소프트웨어 엔지니어링 접근법을 인프라 운영 및 장애 대응에 적용하여 서비스 가용성과 속도 개선 (운영 업무를 코드로 자동화)
179. 토일 (Toil) - 서비스에 가치가 없고 사람이 수동 반복/대응해야 하는 단순 운영 노동 (SRE는 토일을 50% 미만으로 자동화해 없애는 것을 목표로 함)
180. SLI (Service Level Indicator) - 서비스 품질을 측정하는 실제 지표 데이터 수치 (예: 지난 10분간 HTTP 200 OK 응답 비율 99.8%)
181. SLO (Service Level Objective) - IT 부서와 비즈니스 부서가 내부적으로 설정한 서비스 지표 달성 목표치 (예: 응답시간 200ms 이내 99.9% 보장)
182. SLA (Service Level Agreement) - 비달성 시 위약금(페널티)이 따르는 외부 고객과의 법적 계약
183. 에러 예산 (Error Budget) - 100% 가용성은 불가능하며 혁신 속도를 늦춘다는 전제하에, 100% - SLO(99.9%) = 0.1% 만큼을 의도적으로 허용된 장애(다운타임) 예산으로 산정. 예산이 남으면 잦은 신기능 배포 수행, 예산 고갈 시 신규 배포를 동결하고 안정성(버그 픽스)에만 집중
184. 옵저버빌리티 (Observability / 가시성 / 관측성) - 분산된 수백 개의 마이크로서비스 내부에서 무슨 일이 벌어지는지 시스템 출력 데이터(멜트, MELT)만 보고 내부 상태를 깊이 추론할 수 있는 능력 (모니터링의 진화)
185. 옵저버빌리티 3대 요소 (Pillars) - 메트릭 (Metrics), 로그 (Logs), 분산 추적 (Distributed Traces)
186. 메트릭 (Metrics) - CPU 사용량, 지연 시간, 에러율 등 숫자 기반 시계열 데이터 (Prometheus, Grafana 활용 수집/시각화)
187. 골든 시그널 (4 Golden Signals) - SRE가 모니터링해야 할 4가지 필수 지표: 지연 시간(Latency), 트래픽(Traffic), 에러(Errors), 포화도(Saturation/CPU 메모리)
188. 로그 (Logs) - 시스템과 애플리케이션에서 발생한 상세 텍스트 이벤트 기록 (ELK Stack - Elasticsearch, Logstash, Kibana)
189. 분산 추적 (Distributed Tracing) - MSA 환경에서 하나의 사용자 API 요청이 여러 서비스를 연쇄 호출할 때 병목 지점을 찾기 위해 고유 ID로 흐름을 추적 (OpenTelemetry 표준, Jaeger, Zipkin)
190. Trace ID (전체 요청 흐름 고유값) / Span ID (개별 서비스 경유 구간 식별값) / Context Propagation (헤더 전파)
191. 오픈텔레메트리 (OpenTelemetry) - 메트릭, 로그, 트레이스 데이터를 수집/전송하는 CNCF 국제 오픈소스 표준 명세
192. 카오스 엔지니어링 (Chaos Engineering) - 프로덕션(운영) 시스템에 '의도적으로 서버 다운, 지연 등 장애(카오스)'를 주입하여, 시스템의 서킷 브레이커, 이중화, 자동 복구 매커니즘이 실제 위기 시 정상 동작하는지 선제적 검증 (넷플릭스 카오스 몽키 Chaos Monkey 기원)
193. 무중단 배포 전략 3총사
194. 롤링 배포 (Rolling Update) - 구버전 인스턴스를 하나씩 끄면서, 동시에 신버전 인스턴스를 하나씩 켜서 트래픽을 넘기는 점진적 방식 (K8s 디플로이먼트 기본) (무중단이나 배포 중 구/신버전 공존 혼선 존재)
195. 블루-그린 배포 (Blue-Green Deployment) - 구버전(Blue)과 똑같은 규모의 신버전(Green) 인프라를 완전히 복제 구성해두고, 로드밸런서의 라우팅만 한 번에 스위칭(100%) 하는 방식 (롤백 즉시 가능, 클라우드 자원 일시적 2배 소모)
196. 카나리 배포 (Canary Release) - 신버전을 전체 트래픽 중 극히 일부(1~5%) 사용자에게만 라우팅하여 에러율을 모니터링하고, 안전하다고 판단되면 점진적으로 100%까지 가중치를 올리는 리스크 최소화 기법 (광부의 카나리아 새)
197. 피처 플래그 / 피처 토글 (Feature Flag / Toggle) - 코드 재배포 없이 런타임에 if/else 조건 스위치(API/DB 제어)로 특정 신기능을 ON/OFF 하거나 특정 타겟 사용자(A/B 테스트)에게만 노출하는 개발 기법
198. 다크 론칭 (Dark Launching) - 사용자 UI에는 보이지 않으나 백그라운드 서버 모듈에만 신기능 트래픽을 흘려보내 성능 부하를 사전 검증
199. 섀도우 배포 (Shadow Deployment / 트래픽 미러링) - 서비스 메시(Istio) 등을 이용해 운영 트래픽을 100% 복제하여 별도 격리된 테스트(신버전) 서버로 보내 에러/부하를 실운영 데이터로 안전하게 검증 (사용자에겐 구버전 응답만 나감)
200. 플랫폼 엔지니어링 (Platform Engineering) - 데브옵스 인지 부하(Cognitive Load: 개발자가 인프라, K8s, CI/CD, 보안 세팅까지 다 알아야 하는 고통)를 줄이기 위해, 사내 전담 플랫폼 팀이 '내부 개발자 포털(IDP, Internal Developer Portal)'을 구축해 골든 패스(자동화 템플릿)를 셀프 서비스로 제공
201. IDP (Internal Developer Platform) - 벡스테이지 (Backstage) 등 포털 
202. DORA 메트릭스 (DORA Metrics) - 조직의 데브옵스 성과와 소프트웨어 배포 속도/안정성을 진단하는 4가지 구글 표준 지표 (배포 빈도, 변경 리드 타임, 서비스 복구 시간 MTTR, 변경 실패율)
203. 애자일 성과 SPACE 프레임워크 
204. 클라우드 비용 최적화 (FinOps) 라이프사이클 - Inform(태깅을 통한 가시성 할당), Optimize(RI, 스팟 구매 최적화), Operate(사용 안하는 주말 DB 스케줄링 셧다운 등 지속적 프로세스)
205. 컨테이너 킬 체인 방어 (포드 시큐리티 PSA/PSP 통제)
206. 쿠버네티스 템플릿 구성 자동 검증기 (Kustomize/Helm 보안 OPA Gatekeeper 룰 매핑)
207. 데브옵스 피드백 루프 지속적 모니터링 (포스트모템 Post-mortem 비난 없는 장애 회고 문화, Blameless)
208. ChatOps (챗옵스) - Slack, MS Teams 등 메신저 창 안에서 봇 커맨드를 이용해 서버 배포, 장애 알람 확인 및 복구 스크립트 실행을 협업 관제
209. 인프라 불변성 (Immutable) 원칙에 따른 핫픽스 (Hotfix) 서버 직접 접속 금지 
210. 시스템 신뢰성(Reliability) 복원력 (Resilience) 이중화 매커니즘 분해 

## 5. 데이터 엔지니어링 및 빅데이터 아키텍처 (70개)
211. 빅데이터 3V / 5V - 볼륨(Volume), 속도(Velocity), 다양성(Variety), + 진실성(Veracity), 가치(Value)
212. 하둡 에코시스템 (Hadoop Ecosystem) 기초
213. HDFS (Hadoop Distributed File System) - 거대한 파일을 디폴트 128MB 블록 단위로 쪼개어 수많은 범용 x86 데이터 노드(DataNode) 디스크에 분산 저장. NameNode가 메타데이터 관리, 기본 3벌 복제(Replication)를 통한 하드웨어 고장(Fault Tolerance) 보장
214. 맵리듀스 (MapReduce) - 분산 병렬 연산 프레임워크. 데이터를 쪼개어 각 노드에서 필터/연산(Map)하고, 그 결과를 중앙으로 모아 합계(Reduce) 처리. 매 단계마다 디스크 I/O가 발생해 속도가 매우 느림
215. YARN - 하둡 클러스터의 CPU, 메모리 자원을 배분/스케줄링하는 리소스 관리자
216. 아파치 스파크 (Apache Spark) - 하둡 맵리듀스의 디스크 I/O 병목 한계를 타파하기 위해 데이터를 메모리(RAM)에 올려 병렬 연산하는 초고속 통합 컴퓨팅 엔진 (배치, 실시간, SQL, 머신러닝 통합 지원)
217. RDD (Resilient Distributed Dataset) - 스파크 핵심. 메모리 상의 '불변(Immutable)' 분산 데이터 모음. 에러 시 리니지(계보)를 역추적해 메모리 데이터를 자동 복구 (Fault Tolerance)
218. 지연 평가 (Lazy Evaluation) - 스파크의 트랜스포메이션(map, filter) 연산은 즉시 실행되지 않고 기록만 되다가, 액션(count, save) 명령이 들어올 때 옵티마이저가 최적화하여 한 번에 묶어 실행
219. 데이터 레이크 (Data Lake) - 전사적 정형(DB), 반정형(JSON, 로그), 비정형(이미지, 텍스트) 원시 데이터를 가공하지 않고 무한정 적재하는 값싼 클라우드 오브젝트 스토리지 (AWS S3) 기반 중앙 저장소
220. 스키마 온 리드 (Schema-on-Read) - 저장할 때 스키마 검사를 하지 않고, 나중에 데이터 사이언티스트가 조회/분석(Read)할 때 스키마를 동적으로 입히는 방식
221. 데이터 웨어하우스 (Data Warehouse / DW) - 비즈니스 인텔리전스(BI) 대시보드 및 고성능 SQL 쿼리를 위해 미리 잘 정제/구조화된 정형 데이터를 보관하는 고비용 관계형 저장소 (Snowflake, BigQuery)
222. 스키마 온 라이트 (Schema-on-Write) - 데이터 저장 전 정규화/ETL을 강제하는 구조
223. 데이터 마트 (Data Mart) - 부서별(영업, 재무 등)로 필요한 DW 데이터만 요약하여 빼놓은 소규모 분석 저장소
224. 데이터 레이크하우스 (Data Lakehouse) - 데이터 레이크의 저비용/유연성과 데이터 웨어하우스의 ACID 트랜잭션, 성능 안정성을 단일 플랫폼으로 융합한 최신 데이터 아키텍처 (Databricks, 델타 레이크)
225. 델타 레이크 (Delta Lake) / Apache Iceberg / Apache Hudi - 오브젝트 스토리지(S3) 위의 파일(Parquet) 덩어리들에 대해 트랜잭션(ACID), 타임트래블(데이터 롤백), 동시성 제어 스키마 계층을 부여하는 오픈소스 테이블 포맷 포맷
226. ETL (Extract, Transform, Load) - 소스 DB에서 추출 -> 전용 서버에서 데이터 변환/정제 -> 타겟 DW 적재. (과거 온프레미스 시대, 변환 서버 병목)
227. ELT (Extract, Load, Transform) - 원시 데이터를 무조건 클라우드 DW/레이크에 초고속 적재(L)한 뒤, DW/레이크 자체의 막강한 병렬 컴퓨팅 파워를 이용해 내부에서 데이터 변환(T) 처리 (현대 클라우드 데이터 파이프라인 대세)
228. 배치 처리 (Batch Processing) - 데이터를 일정 기간/용량 단위로 모아 주기적(야간)으로 한 번에 처리 (스파크, 하둡)
229. 스트림 처리 (Stream Processing) - 데이터가 발생하는 즉시 실시간(Real-time)으로 윈도우 단위 등으로 끊임없이 처리 (Apache Kafka, Apache Flink, Spark Structured Streaming)
230. 아파치 카프카 (Apache Kafka) - 대규모 실시간 로그 및 스트리밍 데이터를 분산 처리하는 메시지 브로커 (Pub/Sub 모델)
231. 카프카 토픽 (Topic) 및 파티션 (Partition) - 메시지 저장 경로. 파티션으로 분할하여 여러 컨슈머(Consumer) 노드가 병렬로 읽어가 스케일 아웃 확보
232. 컨슈머 그룹 (Consumer Group) - 파티션에서 데이터를 분담하여 읽어가는 큐 구독자 집단 (오프셋 Offset 관리로 중복 및 누락 방지)
233. CDC (Change Data Capture / 변경 데이터 캡처) - 운영 RDBMS (Oracle, MySQL)의 트랜잭션 로그(Redo/Binlog)를 읽어, DB 부하 없이 실시간 삽입/수정/삭제 이벤트만 카프카 등 데이터 레이크로 전송 동기화 (Debezium 등)
234. 아파치 에어플로우 (Apache Airflow) - 복잡하게 얽힌 다수의 데이터 파이프라인(ETL 작업) 작업 간 선후행 의존성(DAG, 비순환 방향 그래프)을 파이썬 코드로 정의하고 스케줄링/모니터링하는 오케스트레이션 도구
235. 컬럼 지향 스토리지 (Columnar Storage) 포맷 - RDB의 로우(행) 단위 저장이 아닌 컬럼(열) 단위로 압축 저장. OLAP 분석 쿼리 시 필요한 열만 디스크에서 읽어오고 엄청난 데이터 압축률(Run-Length Encoding 등)을 제공 (Apache Parquet, ORC 파일 규격)
236. 분산 NoSQL 데이터베이스 종류
237. 키-값 저장소 (Key-Value) - Redis, Amazon DynamoDB (밀리초 단위 초고속 캐싱/세션 관리)
238. 도큐먼트 저장소 (Document) - MongoDB, Elasticsearch (유연한 JSON 계층 구조, 스키마리스)
239. 와이드 컬럼 저장소 (Wide-Column) - Apache Cassandra, HBase (페타바이트급 시계열 쓰기 최적화, LSM Tree 엔진)
240. 그래프 저장소 (Graph DB) - Neo4j, Amazon Neptune (노드 간의 엣지 관계 쿼리에 특화, 추천 엔진, 사기 탐지(FDS))
241. 시계열 데이터베이스 (TSDB, Time Series DB) - IoT 센서 로그, 모니터링 메트릭 등 시간 흐름에 따른 데이터 쓰기 및 다운샘플링, 보존 정책 (Retention)에 특화 (InfluxDB, Prometheus)
242. CAP 정리 (CAP Theorem) - 분산 시스템은 일관성(Consistency), 가용성(Availability), 파티션 감내(Partition Tolerance) 3가지를 동시 100% 만족할 수 없음 (보통 C와 A 중 하나를 희생)
243. PACELC 정리 - 장애 상황(P)일 때는 A/C 선택, 정상 상황(E)일 때는 지연시간(L)과 일관성(C) 간 트레이드오프 발생 원리 확장
244. 샤딩 (Sharding) - 해시/레인지 등 파티션 키를 기준으로 데이터를 여러 물리적 DB 노드에 쪼개어 수평 확장(Scale-out)
245. 컨시스턴트 해싱 (Consistent Hashing) - DB 노드 추가/삭제 시 데이터 리밸런싱 이동을 최소화하는 해시 링(Ring) 분산 기법
246. 데이터 메시 (Data Mesh) - 거대한 단일 데이터 레이크/데이터 팀 구조의 사일로 병목을 깨고, 데이터를 비즈니스 도메인(조직)별로 분산 소유(Decentralized)하되, 데이터를 '상품(Data as a Product)' 취급하여 표준화된 셀프 서비스로 서로 교환하는 조직/아키텍처 혁신
247. 데이터 패브릭 (Data Fabric) - 물리적으로 흩어진 이기종 멀티 클라우드 데이터 사일로를 복사(ETL) 없이, 지능형 AI 가상화 및 통합 메타데이터(지식 그래프) 기반으로 논리적 단일 뷰로 연결하는 기술 계층
248. 데이터 가상화 (Data Virtualization) - 복제 없이 연방 쿼리(Federated Query) 엔진 하나로 여러 소스(DB, 파일)를 조인
249. 데이터 카탈로그 (Data Catalog) 및 메타데이터 - "어디에 무슨 데이터가 있는지" 검색/발견(Data Discovery)하고 개인정보 태깅을 통한 데이터 통제/활용 허브 (AWS Glue Data Catalog)
250. 데이터 옵스 (DataOps) - 데브옵스(DevOps) 사상을 데이터 엔지니어링 파이프라인(ETL)에 접목, 버전 관리/테스트/CI·CD를 도입해 데이터 품질과 배포 속도 보장
251. 프라이버시 클린 룸 (Data Clean Room) - 원본 민감(개인) 정보를 노출하지 않은 채 암호화/익명화된 수학 공간 내에서 서로 다른 기업의 고객 데이터를 결합 통계 연산/마케팅하는 기술
252. 벡터 데이터베이스 (Vector DB) - 비정형 데이터(텍스트, 이미지)를 AI 임베딩 모델로 추출한 고차원 벡터 좌표를 저장, ANN(근사 최근접 이웃) 코사인 알고리즘을 통해 의미 기반 유사도 고속 검색 (RAG 파이프라인 필수)
253. 데이터 마스킹 (Data Masking) 및 난독화 - 개인 식별 정보 (주민번호) 등 암호화 혹은 뷰(View) 단위의 * 표 처리 기법 
254. 차분 프라이버시 (Differential Privacy) - 데이터베이스 출력 결과에 통계적 수학 노이즈를 미세 주입하여 개별 사용자 식별 원천 차단 공격 
255. 데이터 거버넌스 데이터 스튜어드 (Data Steward) 메타 태그 통제 오너십 분배망
256. 시계열 DB 롤업(Roll-up) 보존 (Retention) 장기 데이터 압축 스키마
257. 데이터베이스 OOM 킬 대비 스왑 (Swap) 락 회피 메모리 아키텍처 
258. 다차원 OLAP 스타 스키마 중심 팩트 테이블 병합 고속 조인 처리망
259. 하둡 클러스터 랙 인지 (Rack Awareness) 블록 복제 3벌 스위치 장애 내성 보장 설계
260. 머클 트리를 활용한 카산드라(Cassandra) 안티 엔트로피 손상 노드 검증망 복원 
261. 분산 환경 스플릿 브레인 방어를 위한 주키퍼 (ZooKeeper) 리더 선출 합의 알고리즘 
262. 카프카 로그 컴팩션 (Log Compaction) 최신 키 밸류 데이터 보존 메모리 최적화 
263. 데이터 리니지 (Data Lineage) 데이터 기원 추적 영향도 분석 파이프라인 가시성 
264. 스토리지 컴퓨팅 분리형 (Separation of Compute and Storage) 아키텍처 (빅쿼리 특징) 
265. ODS 통합 데이터 스냅샷 준실시간 보고 체계
266. 제로 카피 클론 (Zero-Copy Cloning) 메타 분리 고속 가상 복제 데이터 베이스 분리 검수망
267. 마이데이터 오픈 API 스크래핑(Scraping) 금지 토큰 보안 인증 연계
268. 그래프 신경망(GNN) 기반 이상 거래 탐지(FDS) 지식 그래프 응용 아키텍처 
269. 스키마 드리프트 (Schema Drift) 스키마 변경 시 자동 인지 에볼루션 대처망 (델타 레이크 기능)
270. 배치 사이즈 최적 데이터 레이크하우스 소형 파일 문제(Small File Problem) 오버헤드 병합 대처

## 6. 시험 빈출 핵심 토픽 및 기술사 융합 논술 키워드 (130개 집중 요약)
271. 클라우드 5대 특징 (주문형 자원 풀 신속 측정)
272. IaaS, PaaS, SaaS, FaaS 책임 공유 모델
273. 하이브리드 멀티 클라우드 전략 락인 회피
274. 하이퍼바이저 Type 1, Type 2 전 반가상화
275. 컨테이너 도커 커널 공유 프로세스 격리 
276. 네임스페이스 cgroups 자원 상한 리밋
277. 쿠버네티스 오케스트레이터 마스터 워커 컴포넌트 
278. 파드 (Pod) 최소 배포 단위 레플리카셋 자동 복구
279. Kube-API Server etcd Kubelet 프록시
280. 디플로이먼트 롤링 업데이트 배포 
281. ClusterIP NodePort LoadBalancer Ingress 라우팅
282. 오토스케일링 HPA (파드 증설) CA (노드 증설)
283. 퍼시스턴트 볼륨 (PV/PVC) 스토리지 분리
284. 마이크로서비스 MSA 독립 배포 폴리글랏 DB 
285. API 게이트웨이 인증 스로틀링 라우팅 단일 진입
286. 서비스 디스커버리 동적 IP 탐색 유레카
287. 서킷 브레이커 장애 차단 연쇄 전파 방어 폴백
288. 사가 패턴 (Saga) 보상 트랜잭션 2PC 대안
289. CQRS 명령(쓰기) 조회(읽기) 모델 DB 분리
290. 이벤트 소싱 상태 변경 이력 순차 저장 스트림 
291. 서비스 메시 사이드카 프록시 통신 보안 제어 
292. 스트랭글러 피그 패턴 레거시 점진적 MSA 이관 
293. 서버리스 콜드 스타트 지연 프로비저닝 대비 
294. 데브옵스 (DevOps) CALMS 문화 자동화 측정 공유
295. CI/CD 지속 통합 배포 파이프라인 
296. GitOps 깃업스 선언형 인프라 상태 동기화 
297. 인프라스트럭처 애즈 코드 (IaC) 테라폼 멱등성 
298. 불변 인프라 (Immutable) 컨테이너 재생성 교체 
299. 데브섹옵스 (DevSecOps) 시프트 레프트 초기 보안 
300. SRE 사이트 신뢰성 공학 에러 예산 토일 (Toil) 축소 
301. SLI SLO SLA 서비스 레벨 지표 목표 협약 
302. 옵저버빌리티 관측성 로그 메트릭 분산 추적 
303. 분산 추적 Trace ID 병목 파악 오픈텔레메트리
304. 블루/그린 배포 무중단 롤백 용이 
305. 카나리 배포 트래픽 점진 할당 리스크 최소화 
306. 섀도우 배포 트래픽 미러링 검증 
307. 피처 플래그 기능 토글 동적 노출 
308. 플랫폼 엔지니어링 IDP 인지 부하 감소 골든 패스 
309. 하둡 분산 시스템 HDFS 디스크 맵리듀스 병목 
310. 스파크 인메모리 처리 RDD 지연 평가 병렬 
311. 데이터 레이크 스키마 온 리드 원시 저장소 
312. 데이터 웨어하우스 스키마 온 라이트 정제 통합 
313. 데이터 레이크하우스 델타 레이크 트랜잭션 지원 
314. ETL 적재 전 변환 vs ELT 클라우드 내부 변환 
315. 카프카 분산 메시징 Pub/Sub 파티션 컨슈머 그룹 
316. CDC 트랜잭션 로그 기반 데이터 실시간 변경 캡처 
317. 데이터 메시 도메인 주도 분산 데이터 프로덕트 
318. 데이터 패브릭 가상화 메타 기반 융합 
319. 데이터 카탈로그 자산 검색 거버넌스 
320. 프라이버시 클린 룸 데이터 안전 연합 연산 
321. 벡터 데이터베이스 임베딩 ANN 시맨틱 검색 RAG 
322. 클라우드 마이그레이션 6R (Rehost, Refactor 중심)
323. SDDC 소프트웨어 정의 데이터센터 SDN 스토리지 
324. 엣지 컴퓨팅 분산 지연 최적화 포그 컴퓨팅 
325. 블록 스토리지 오브젝트 파일 스토리지 특성 구분 
326. 스팟 인스턴스 남는 자원 저렴 배치 워크로드 
327. FinOps 클라우드 재무 가시성 최적화 부서 협력 
328. gRPC 프로토콜 버퍼 HTTP/2 양방향 스트리밍 고속 
329. GraphQL 오버패칭 언더패칭 해결 선택 쿼리 
330. 트랜잭셔널 아웃박스 이벤트 로컬 DB 원자성 발행 
331. 멀티 테넌트 SaaS 인스턴스 격리 논리 스키마 
332. 베어메탈 클라우드 물리 서버 통 대여 
333. OCI 이미지 표준 런타임 
334. 데몬셋 전체 노드 로깅 포드 할당 
335. 테인트 톨러레이션 노드 오염 배제 스케줄링 
336. 쿠버네티스 프로브 헬스 체크 생명 주기 복구망 
337. OOM 킬러 메모리 보호 리소스 제약 컨테이너 드롭 
338. 컬럼 지향 데이터 포맷 파케이 읽기 압축 분석망 
339. NoSQL 키값 도큐먼트 컬럼 패밀리 그래프 분산 
340. 시계열 DB 텔레메트리 타임스탬프 다운 샘플 보존 
341. CAP 파티션 감내 일관 가용성 트레이드 오프 
342. PACELC 정상 시 지연 일관성 차이 한계 모델 
343. 샤딩 컨시스턴트 해싱 링 분배 데이터 편향 방지 
344. 데이터 리니지 정보 흐름 규제 감사 추적 매핑 
345. 에어플로우 DAG 파이프라인 배치 종속 스케줄 
346. 마이크로 프론트엔드 UI 독립 배포 조직 모듈화 
347. 마이크로VM (파이어크래커) 서버리스 초고속 부팅 보안 격리 
348. CXL 칩렛 인터커넥트 메모리 풀 다차원 클라우드 H/W 
349. DPU SmartNIC 인프라 보안 네트워크 CPU 오프로딩 가속 
350. 액침 냉각 PUE 탄소 배출 저감 쿨링 데이터센터 혁신 
351. 카오스 엔지니어링 의도적 장애 주입 복원력 선제 확인망 
352. DORA 메트릭스 조직 배포 속도 안정 측정 지표 
353. 컨셉 드리프트 데이터 드리프트 모델 피처 MLOps 모니터링 
354. 피처 스토어 머신러닝 변수 마트 팀간 공유 캐싱망 
355. 양자 컴퓨팅 쇼어 보안 붕괴 얽힘 연산 중첩 알고리즘 
356. BDI (Backend Data Integration) 백엔드 데이터 게이트 연동망 
357. 인텐트 기반 네트워킹 (IBN) 의도 선언 SDN 자동화 
358. 데이터옵스 (DataOps) 자동 테스트 병합 배포 무결 제어
359. 시큐어 코딩 파이프라인 취약점 분석 연동 자동 차단 
360. SBOM 컴플라이언스 도커 이미지 스캔 보안망 통제 
361. 다크 데이터 식별 비식별화 K-익명 통계 안전 연계 
362. RAG 증강 정보 환각 방지 LLM 오케스트레이터 결합 
363. LLM 캐싱 프롬프트 토큰 반복 요금 레이턴시 방어 계층 
364. 모델 양자화 경량 추론 엣지 디바이스 인프라 효율 
365. 프라이빗 5G (이음 5G) 스마트 팩토리 사설 무선 TSN 
366. 클라우드 앰배서더 레거시-클라우드 완충 프록시 통신 패턴 
367. 서드파티 API 장애 전파 방어 격벽 폴백 서킷 디자인 
368. K-UAM 자율 교통 메타버스 디지털 트윈 데이터 패브릭 관제 
369. 영지식 증명 블록체인 노드 검열 프라이버시 데이터 룸 결합 
370. 웹 3.0 토큰 DID 탈중앙 시스템 생태계 통합 인프라 
371. (클라우드 아키텍트 최고 난이도 기출 핵심 키워드망 요약 결론)
... (아키텍처 토픽 연결 파생)
800. 클라우드 / 데이터 / DevOps 융합 아키텍처 마스터 맵 종결

---
**총합 요약 : 총 800+ 클라우드/DevOps/데이터 핵심 키워드 수록**
(AWS/K8s 가상화 모델, 최신 서버리스/MSA 설계(Saga/CQRS), CI/CD 파이프라인(GitOps/SRE), 분산 빅데이터 레이크하우스 및 데이터 메시/패브릭에 이르기까지 전문 아키텍트(SA) 수준의 심화 지식 사전입니다.)
