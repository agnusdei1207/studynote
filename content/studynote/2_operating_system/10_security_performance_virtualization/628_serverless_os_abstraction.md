+++
title = "628. 서버리스 (Serverless) 운영체제 추상화"
date = "2026-03-14"
weight = 628
+++

# # [628. 서버리스 (Serverless) 운영체제 추상화]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질 (Essence)**: 서버리스는 **"Ephemeral (일시적) 실행 환경"**을 통해 OS (Operating System) 및 하드웨어 관리의 책임을 개발자로부터 클라우드 공급자로 완전히 이관하여, 코드 실행 단위(Function)로만 자원을 추상화하는 패러다임입니다.
> 2. **가치 (Value)**: **Utility Computing (유틸리티 컴퓨팅)** 모델에 기반하여 유휴(Idle) 자원에 대한 비용을 제로(Zero)화하고, 트래픽 급증에 따른 **Auto-scaling (자동 확장)**을 100ms 단위로 수행하여 비즈니스 민첩성을 극대화합니다.
> 3. **융합 (Convergence)**: **Micro-VM (마이크로 가상머신)** 및 **Unikernel (유니커널)** 기술과 융합하여 **FaaS (Function as a Service)**의 성능 한계인 **Cold Start (콜드 스타트)** 지연을 극복하고, **Edge Computing (엣지 컴퓨팅)**으로 그 영역을 확장하고 있습니다.

---

### Ⅰ. 개요 (Context & Background) - 서버리스의 기원과 철학

#### 1. 개념 및 정의
서버리스(Serverless)는 물리적으로 서버가 존재하지 않다는 의미가 아니라, **"Serverless Computing (서버리스 컴퓨팅)"**이라는 용어가 시사하듯, 인프라 프로비저닝(Provisioning), 관리(Management), 스케일링(Scaling) 등의 운영적 부담(Operational Overhead)이 개발자에게 **추상화(Abstraction)**되었다는 것을 의미합니다. 이는 클라우드 컴퓨팅의 발전 단계인 **On-Premise → IaaS (Infrastructure as a Service) → PaaS (Platform as a Service) → FaaS (Function as a Service)**로 이어지는 진화의 최종 단계로 볼 수 있습니다.

핵심은 **Stateless (무상태성)**와 **Event-driven (이벤트 기반)** 실행입니다. 사용자는 애플리케이션의 상태를 유지할 필요 없이, 특정 이벤트(웹 요청, 파일 업로드, DB 레코드 변경 등)가 발생할 때만 트리거되는 함수(Function)를 작성합니다. 클라우드 제공자는 이 함수를 실행하기 위해 **OS (Operating System)** 런타임을 즉시 할당하고, 실행이 종료되면 즉시 회수하여 자원 풀(Pool)로 반환합니다.

#### 2. 등장 배경: "NoOps"의 추구
기존의 **VM (Virtual Machine)**이나 **Container (컨테이너)** 기반의 클라우드 환경에서도 개발자는 서버의 용량(CPU/Memory)을 산정하고, 패치(Patching)를 관리해야 하는 운영적 부채(Operational Debt)가 존재했습니다. 서버리스는 다음과 같은 변화의 요구를 해결하기 위해 등장했습니다.

1.  **기존 한계**: 트래픽 예측이 불가능한 스파크(Spike) 현상 발생 시, 미리 확장해 둔 서버는 비용 낭비(Idle Cost)이고, 자동 확장이 늦으면 서비스 장애(Outage)로 이어짐.
2.  **혁신적 패러다임**: **Execution Unit (실행 단위)**를 '서버'가 아닌 '함수'로 세분화하여, 요청이 들어온 시간(Millisecond 단위)에 대해서만 과금하는 **Pay-as-you-go (종량제)** 모델 도입.
3.  **비즈니스 요구**: **TTM (Time to Market)** 단축을 위한 인프라 관리 제로(Zero)화.

#### 3. 기술적 구조 (ASCII Diagram)
서버리스는 단순한 코드 호스팅이 아니라, 이벤트를 감지하고 라우팅하는 **Event Mesh (이벤트 메시)**와 이를 실행하는 **Compute Fabric (컴퓨트 패브릭)**으로 구성됩니다.

```text
[ Logical Architecture: Serverless Abstraction ]

 +-------------------+         +-----------------------+         +--------------------+
 |   User / System   |         |  Cloud Provider (Backend)      |                    |
 +-------------------+         +-----------------------+         +--------------------+
 |   Client App      | ------->|  1. Event Source      |         |                    |
 |   (Mobile/Web)    |  Trigger|  (HTTP, IoT, S3, DB)  |         |                    |
 +-------------------+         +----------+------------+         |                    |
                                         |                      |                    |
                                         v                      |                    |
                               +-------------------+           |                    |
                               | 2. API Gateway /  |           |                    |
                               |    Event Router   |           |                    |
                               +--------+----------+           |                    |
                                        |  (Async/Sync)        |                    |
                                        v                      |                    |
                               +--------------------------------------------------------+
                               | 3. FaaS Control Plane (The Brain)                      |
                               |  - Load Balancing (부하 분산)                          |
                               |  - Scaling Logic (스케일링 로직)                       |
                               |  - Monitoring (모니터링)                              |
                               +--------------------------------------------------------+
                                        |
                     +--------------------+--------------------+
                     |                    |                    |
                     v                    v                    v
         +-------------------+  +-------------------+  +-------------------+
         | 4. Execution Env  |  | 4. Execution Env  |  | 4. Execution Env  |
         | [Function Instance]|  | [Function Instance]|  | [Function Instance]|
         | - (Ephemeral)     |  | - (Ephemeral)     |  | - (Ephemeral)     |
         | - Isolated Runtime|  | - Isolated Runtime|  | - Isolated Runtime|
         +-------------------+  +-------------------+  +-------------------+
                     ^                    |                    ^
                     | (Pull/Scale)        | (Push/Die)         | (Re-use)
                     +--------------------+--------------------+
                                          |
                               +-------------------+
                               | 5. Shared Storage  | <--> (State Persistance)
                               | (DB, Object Store)|
                               +-------------------+
```

*   **도입**: 위 다이어그램은 사용자의 요청이 클라우드 내의 이벤트 라우터를 거쳐, 실제 코드가 실행되는 일시적인 **Execution Environment (실행 환경)**에 도달하는 과정을 보여줍니다. 관건은 4번 영역이 지속되지 않고 필요시에만 생성되었다 사라진다는 점입니다.
*   **해설**: 이 구조에서 개발자는 4번 영역의 내부(OS, Runtime, CPU)를 전혀 알 필요가 없습니다. 1번(트리거)과 5번(상태 저장소)만 연결하면, 클라우드의 제어 평면(Control Plane)이 2번, 3번 과정을 통해 즉시 4번을 **Spin-up (스핀업, 시작)** 시키고, **Spin-down (스핀다운, 종료)** 시킵니다.

📢 **섹션 요약 비유**: 서버리스는 "집을 지을 때 부지를 사고, 건축 자재를 사고, 인부를 고용하는 **'자가 건축(On-Premise/IaaS)'** 방식에서 벗어나, 필요할 때마다 **'완벽하게 설치된 프리팹(Prefab) 주방'**을 빌려서 요리만 하고 나가는 것"과 같습니다. 주방 설비(OS)의 유지보수는 주방장(클라우드 제공자)의 몫이며, 나는 요리(코드)에만 집중하고 재료(이벤트)가 들어올 때만 요리하면 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - OS 가상화의 진화

#### 1. 핵심 구성 요소 (Components)

서버리스의 추상화는 마법처럼 보이지만, 그 이면에는 OS 수준의 정교한 제어가 있습니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 주요 기술/프로토콜 (Tech/Protocol) | 비유 (Analogy) |
| :--- | :--- | :--- | :--- | :--- |
| **Event Source (이벤트 소스)** | 입력 트리거 역할 | HTTP 요청, 파일 생성, 스트림 데이터 변화 등을 감지하여 Webhook이나 Queue(Pub/Sub)로 전달 | API Gateway, S3 Event, IoT Hub | 주문서(요청) |
| **Function Orchestrator (함수 오케스트레이터)** | 자원 관리자 | 들어오는 트래픽 양에 따라 실행 중인 인스턴스의 수를 모니터링하고, 새로운 컨테이너/VM을 생성(Scale-out)하거나 제거(Scale-in)하는 스케줄링 수행 | Kubernetes Operator (내부), Custom Scheduler | 주방장(인력 배치) |
| **Execution Environment (실행 환경)** | 격리된 샌드박스 | 실제 함수 코드가 구동되는 공간. 보안을 위해 프로세스/OS 레벨에서 격리(Isolation)되어야 함. **Cold Start**는 이곳의 초기화 속도에 달림. | **Micro-VM (Firecracker)**, **gVisor**, **Container (cgroups)** | 개별 주방 부스 |
| **State Management (상태 관리)** | 비상태 연결 | 함수 실행이 끝나도 데이터가 유지되어야 할 때 사용하는 외부 저장소. 내부 파일 시스템은 Ephemeral(휘발성)이므로 사용 불가. | **S3 (Object Storage)**, **DynamoDB (NoSQL)**, **Redis** | 창고(식재료 보관) |
| **Security Monitor (보안 모니터)** | 보안 경계 | 사용자 코드가 호스트 OS나 다른 테넌트의 자원에 침투하지 못하도록 syscall(시스템 콜)을 필터링하고 자원을 제한함. | **seccomp**, **AppArmor**, **Hypervisor** | CCTV 및 보안 요원 |

#### 2. 심층 동작 원리: 추상화 계층의 이해
서버리스 플랫폼은 전통적인 가상화 계층에서 더 나아가, **OS (Operating System)** 자체를 필요한 만큼만 쪼개서 사용합니다. 크게 **Container-based (컨테이너 기반)** 방식과 **Micro-VM (마이크로 VM)** 방식으로 나뉩니다.

```text
[ OS Virtualization Stack Comparison ]

+------------------------------------------------------------------+
|                     Host Hardware (Physical Server)               |
+------------------------------------------------------------------+
|                     Host OS (Linux Kernel)                        |
+--------------------------+-------------------------+-------------+
|                          |                         |             |
| [Type 1: Legacy VM]      | [Type 2: Container]     | [Type 3: Serverless Micro-VM] |
| +----------------------+ | +---------------------+ | +---------------------------+ |
| | Guest OS (Full Linux)| | | App B (Isolated)    | | | Guest Kernel (Lite)      | |
| | +--------------------| | | (User Space Only)   | | | (Minimal Linux)          | |
| | | Application        | | +---------------------+ | | +-------------------------+ |
| | +--------------------| | No Kernel             | | | User Function (Code)     | |
| | Hypervisor           | | Shared Kernel         | | | (Seccomp Filter)         | |
| +----------------------+ | Security Boundary: Proc| | +---------------------------+ |
| High Overhead (Slow)    | Low Overhead (Fast)     | Hypervisor (Firecracker)    |
|                         | Security Risk (Shared)  | Medium Overhead / High Sec. |
+--------------------------+-------------------------+-------------+

 Key Metrics:
  - Boot Time: 500ms ~ 1s (VM) / 100ms (Cont) / 20ms (Micro-VM)
  - Isolation: Strong (VM) / Weak (Cont) / Strong (Micro-VM)
```

*   **도입**: 서버리스의 성능과 보안은 실행 환경을 어떻게 격리하느냐에 달려있습니다. 초기에는 도커(Docker) 컨테이너를 그대로 사용했으나, 보안 이슈로 인해 커널을 공유하지 않으면서 가볍게 부팅하는 **Micro-VM (마이크로 가상머신)** 기술이 주류로 자리 잡고 있습니다.
*   **해설**:
    *   **Type 2 (Container)**: 단일 호스트 커널을 공유하기 때문에 부팅이 매우 빠르지만(Cold Start 유리), 커널 취약점(예: Dirty Cow) 공격에 다른 테넌트의 코드가 노출될 위험이 있습니다.
    *   **Type 3 (Micro-VM)**: **AWS Lambda (Firecracker)**가 채택한 방식입니다. 가상화 계층(Hypervisor)을 유지하여 보안성을 확보하되, 불필요한 하드웨어 에뮬레이션과 장치 드라이버를 모두 제거하여 **Lightweight OS (경량 OS)**를 구축, 수십 밀리초 만에 부팅을 완료합니다.

#### 3. 핵심 알고리즘: 실행 수명 주기 (Lifecycle Management)
서버리스 함수는 수명이 매우 짧습니다. 다음은 그 수명 주기를 관리하는 의사 코드(Pseudo-code)입니다.

```python
class ServerlessWorker:
    def __init__(self, config):
        self.max_duration = config.timeout_ms  # e.g., 900000 (15 mins)
        self.state = "IDLE" # IDLE, INIT, RUNNING, FROZEN, TERMINATED

    def invoke(self, event):
        # 1. 단계: 스케줄링 및 할당
        if self.state == "IDLE":
            # [Cold Start] 환경 초기화
            self.allocate_compute_resource()
            self.load_function_code()
            self.state = "INIT"
        
        # 2. 단계: 실행
        self.state = "RUNNING"
        try:
            result = self.execute_user_code(event)
        except Exception as e:
            return self.handle_error(e)
        
        # 3. 단계: 종료 및 재사용 결정 (Keep-alive Strategy)
        if self.get_idle_time() > THRESHOLD:
            self.release_resources() # Overhead 발생 지점
            self.state = "TERMINATED"
        else:
            self.state = "FROZEN" # Warm Start 대기 (임시 보존)
            return result
```

📢 **섹션 요약 비유**: 서버리스 아키텍처는 "자동차 조립 공장"과 같습니다. 과거(IaaS)는 공장을 지어 유지해야 했지만, 서버리스는 **"주문이 들어올 때마다 로봇 팔(Micro-VM)을 자동으로 설치하여 부품을 조립하고, 작업이 끝나면 로봇 팔을 뜯어낸 뒤 창고에 보관"**하는 방식입니다. 공장 지을 때 드는 비용(Capex)이 없고, 조립하는 데 걸리는 시간(Latency)만 비용으로 지불합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Monolith vs Microservices vs Serverless

| 비교 지표 (Metric) | Monolithic (모놀리식) | Microservices (MSA) | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **단위 (Unit)** | 단일 애플리케이션 (서버 단위) | 서비스별 서버 (컨테이너 단위) | 함수 단위 (Function) |
| **실행 주체** | **