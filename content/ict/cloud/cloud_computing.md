+++
title = "클라우드 컴퓨팅 (Cloud Computing)"
date = 2025-03-01

[extra]
categories = "ict-cloud"
+++

# 클라우드 컴퓨팅 (Cloud Computing)

## 핵심 인사이트 (3줄 요약)
> **인터넷을 통해 언제 어디서나 IT 리소스를 사용**하는 서비스 모델. IaaS/PaaS/SaaS 3가지 서비스 형태와 퍼블릭/프라이빗/하이브리드 배포 모델. 탄력적 확장, 종량제 과금이 핵심.

## 1. 개념
클라우드 컴퓨팅은 **인터넷을 통해 서버, 스토리지, 데이터베이스, 소프트웨어 등의 IT 리소스를 필요할 때마다 사용하고 사용한 만큼만 비용을 지불**하는 컴퓨팅 서비스 모델이다.

> 비유: "전기 서비스" - 발전소를 직접 짓지 않고 필요한 만큼 전기를 쓰고 요금을 냄

## 2. 클라우드 서비스 모델 (3가지)

```
┌────────────────────────────────────────────────────────┐
│                클라우드 서비스 모델                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  IaaS (Infrastructure as a Service)                   │
│  ┌────────────────────────────────────────────────┐   │
│  │ • 가상 서버, 스토리지, 네트워크 제공           │   │
│  │ • 사용자: OS~앱 직접 관리                      │   │
│  │ • 예: AWS EC2, Azure VM, GCP Compute Engine    │   │
│  └────────────────────────────────────────────────┘   │
│                       ↑                               │
│  PaaS (Platform as a Service)                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ • 개발 플랫폼, 런타임 환경 제공                │   │
│  │ • 사용자: 앱 개발에만 집중                     │   │
│  │ • 예: Heroku, AWS Elastic Beanstalk, GCP AE    │   │
│  └────────────────────────────────────────────────┘   │
│                       ↑                               │
│  SaaS (Software as a Service)                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ • 완성된 소프트웨어 서비스                     │   │
│  │ • 사용자: 바로 사용                            │   │
│  │ • 예: Gmail, Dropbox, Salesforce, Office 365   │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  책임 범위:                                            │
│  IaaS   ████████████████████████████████████ (사용자) │
│  PaaS   ████████████████████                           │
│  SaaS   ████████                                        │
│         네트워크|서버|OS|미들웨어|런타임|데이터|앱     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 클라우드 배포 모델

```
┌────────────────────────────────────────────────────────┐
│                  배포 모델 비교                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 퍼블릭 클라우드 (Public Cloud)                     │
│     - 공용 인프라를 여러 기관이 공유                   │
│     - AWS, Azure, GCP                                  │
│     - 장점: 저렴, 탄력적                               │
│     - 단점: 보안 우려                                  │
│                                                        │
│  2. 프라이빗 클라우드 (Private Cloud)                  │
│     - 단일 조직 전용 인프라                            │
│     - 온프레미스 또는 호스팅                          │
│     - 장점: 높은 보안, 통제권                          │
│     - 단점: 높은 비용                                  │
│                                                        │
│  3. 하이브리드 클라우드 (Hybrid Cloud)                 │
│     - 퍼블릭 + 프라이빗 결합                           │
│     - 중요 데이터는 프라이빗, 나머지는 퍼블릭         │
│     - 장점: 유연성, 백업                               │
│     - 단점: 복잡성                                     │
│                                                        │
│  4. 멀티 클라우드 (Multi-Cloud)                        │
│     - 여러 클라우드 제공자 동시 사용                  │
│     - 벤더 종속 방지                                   │
│     - 장점: 위험 분산, 최적화                          │
│     - 단점: 관리 복잡                                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 클라우드 핵심 특성

```
NIST 정의 5가지 핵심 특성:

1. 주문형 셀프 서비스 (On-Demand Self-Service)
   - 사용자가 직접 리소스 생성/관리
   - 사람의 개입 없이 자동화

2. 광대역 네트워크 접근 (Broad Network Access)
   - 언제 어디서나 접근 가능
   - 다양한 디바이스 지원

3. 리소스 풀링 (Resource Pooling)
   - 다중 테넌트 모델
   - 물리적/가상적 리소스 동적 할당

4. 신속한 탄력성 (Rapid Elasticity)
   - 트래픽에 따라 자동 확장/축소
   - 무한한 리소스처럼 보임

5. 측정 가능한 서비스 (Measured Service)
   - 사용량 측정 및 과금
   - 투명한 비용 관리
```

## 5. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
import uuid

class InstanceType(Enum):
    MICRO = ("t2.micro", 1, 1, 8)      # (이름, vCPU, RAM, 스토리지)
    SMALL = ("t2.small", 1, 2, 20)
    MEDIUM = ("t2.medium", 2, 4, 40)
    LARGE = ("t3.large", 2, 8, 80)
    XLARGE = ("t3.xlarge", 4, 16, 160)

class InstanceState(Enum):
    PENDING = "시작 중"
    RUNNING = "실행 중"
    STOPPING = "중지 중"
    STOPPED = "중지됨"
    TERMINATED = "종료됨"

@dataclass
class VirtualMachine:
    """가상 머신 인스턴스"""
    instance_id: str
    name: str
    instance_type: InstanceType
    state: InstanceState = InstanceState.PENDING
    public_ip: Optional[str] = None
    launch_time: datetime = None

    def __post_init__(self):
        if self.launch_time is None:
            self.launch_time = datetime.now()
        if self.public_ip is None:
            self.public_ip = f"54.{uuid.uuid4().int % 255}.{uuid.uuid4().int % 255}.{uuid.uuid4().int % 255}"

    @property
    def specs(self) -> Dict:
        name, cpu, ram, storage = self.instance_type.value
        return {'name': name, 'vCPU': cpu, 'RAM_GB': ram, 'Storage_GB': storage}

class AutoScalingGroup:
    """오토 스케일링 그룹"""

    def __init__(self, name: str, min_size: int, max_size: int):
        self.name = name
        self.min_size = min_size
        self.max_size = max_size
        self.instances: List[VirtualMachine] = []
        self.target_cpu_util = 70  # 목표 CPU 사용률

    def launch_instance(self, instance_type: InstanceType) -> VirtualMachine:
        """인스턴스 시작"""
        if len(self.instances) >= self.max_size:
            print(f"[{self.name}] 최대 인스턴스 수 도달")
            return None

        vm = VirtualMachine(
            instance_id=f"i-{uuid.uuid4().hex[:8]}",
            name=f"{self.name}-{len(self.instances)+1}",
            instance_type=instance_type
        )
        self.instances.append(vm)
        print(f"[{self.name}] 인스턴스 시작: {vm.instance_id} ({vm.specs['name']})")
        return vm

    def terminate_instance(self, instance_id: str):
        """인스턴스 종료"""
        for vm in self.instances:
            if vm.instance_id == instance_id:
                vm.state = InstanceState.TERMINATED
                self.instances.remove(vm)
                print(f"[{self.name}] 인스턴스 종료: {instance_id}")
                return

    def scale_based_on_load(self, current_cpu: float):
        """부하 기반 스케일링"""
        if current_cpu > self.target_cpu_util + 20:
            # 스케일 아웃
            if len(self.instances) < self.max_size:
                self.launch_instance(InstanceType.SMALL)
                print(f"  → 스케일 아웃! (CPU: {current_cpu}%)")

        elif current_cpu < self.target_cpu_util - 30:
            # 스케일 인
            if len(self.instances) > self.min_size:
                self.terminate_instance(self.instances[-1].instance_id)
                print(f"  → 스케일 인! (CPU: {current_cpu}%)")

class CloudProvider:
    """클라우드 서비스 시뮬레이션"""

    def __init__(self, name: str):
        self.name = name
        self.instances: Dict[str, VirtualMachine] = {}
        self.scaling_groups: Dict[str, AutoScalingGroup] = {}
        self.usage_log: List[Dict] = []

    def create_instance(self, name: str, instance_type: InstanceType) -> VirtualMachine:
        """VM 생성"""
        vm = VirtualMachine(
            instance_id=f"i-{uuid.uuid4().hex[:8]}",
            name=name,
            instance_type=instance_type,
            state=InstanceState.RUNNING
        )
        self.instances[vm.instance_id] = vm
        print(f"[{self.name}] 인스턴스 생성: {name}")
        return vm

    def create_scaling_group(self, name: str, min_size: int, max_size: int) -> AutoScalingGroup:
        """오토스케일링 그룹 생성"""
        asg = AutoScalingGroup(name, min_size, max_size)
        self.scaling_groups[name] = asg
        # 최소 인스턴스 시작
        for _ in range(min_size):
            asg.launch_instance(InstanceType.MICRO)
        return asg

    def calculate_cost(self, hours: int) -> Dict:
        """비용 계산 (시간당)"""
        hourly_rates = {
            InstanceType.MICRO: 0.01,
            InstanceType.SMALL: 0.02,
            InstanceType.MEDIUM: 0.04,
            InstanceType.LARGE: 0.08,
            InstanceType.XLARGE: 0.16
        }

        costs = {}
        for vm in self.instances.values():
            if vm.state == InstanceState.RUNNING:
                rate = hourly_rates[vm.instance_type]
                cost = rate * hours
                costs[vm.instance_id] = {
                    'name': vm.name,
                    'type': vm.specs['name'],
                    'hourly_rate': rate,
                    'total_cost': cost
                }

        return costs


# 사용 예시
print("=== 클라우드 컴퓨팅 시뮬레이션 ===\n")

# 클라우드 제공자
cloud = CloudProvider("MyCloud")

# 인스턴스 생성
print("--- 인스턴스 생성 ---")
web_server = cloud.create_instance("web-server-1", InstanceType.MEDIUM)
db_server = cloud.create_instance("db-server-1", InstanceType.LARGE)

# 오토스케일링 그룹
print("\n--- 오토스케일링 그룹 ---")
web_asg = cloud.create_scaling_group("web-asg", min_size=2, max_size=5)

# 부하 기반 스케일링 테스트
print("\n--- 스케일링 테스트 ---")
import random
for minute in range(1, 6):
    cpu = random.choice([50, 60, 90, 95, 30])
    print(f"[{minute}분] CPU: {cpu}%")
    web_asg.scale_based_on_load(cpu)

# 비용 계산
print("\n--- 월 비용 계산 (730시간) ---")
costs = cloud.calculate_cost(730)
total = 0
for iid, info in costs.items():
    print(f"{info['name']}: ${info['total_cost']:.2f}")
    total += info['total_cost']
print(f"총 비용: ${total:.2f}")
```

## 6. 주요 클라우드 제공자

```
┌─────────────────────────────────────────────────────┐
│              주요 클라우드 제공자                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  AWS (Amazon Web Services)                         │
│  - 시장 점유율 1위                                  │
│  - 가장 다양한 서비스                               │
│  - EC2, S3, Lambda, RDS                            │
│                                                     │
│  Microsoft Azure                                   │
│  - 기업 시장 강세                                   │
│  - Office 365 통합                                  │
│  - VM, Blob Storage, Functions                     │
│                                                     │
│  Google Cloud Platform (GCP)                       │
│  - 데이터/AI 강점                                   │
│  - Kubernetes 원조                                  │
│  - Compute Engine, BigQuery, GKE                   │
│                                                     │
│  국내                                              │
│  - Naver Cloud, Kakao Cloud                        │
│  - NHN Cloud, KT Cloud                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 7. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 비용 | 초기 투자 없음, 종량제 |
| 확장성 | 탄력적 리소스 |
| 가용성 | 높은 SLA |
| 접근성 | 어디서나 접근 |
| 관리 | 인프라 관리 불필요 |

### 단점
| 단점 | 설명 |
|-----|------|
| 종속성 | 벤더 락인 |
| 보안 | 데이터 외부 저장 |
| 네트워크 | 인터넷 의존 |
| 비용 | 장기적으론 비쌀 수 있음 |
| 통제권 | 인프라 통제 제한 |

## 8. 실무에선? (기술사적 판단)
- **스타트업**: AWS/Azure, SaaS 우선
- **대기업**: 하이브리드, 멀티클라우드
- **규제 산업**: 프라이빗/하이브리드
- **비용 최적화**: Reserved Instance, Spot Instance

## 9. 관련 개념
- 가상화
- 컨테이너
- 서버리스
- 엣지 컴퓨팅

---

## 어린이를 위한 종합 설명

**클라우드는 "인터넷에 있는 슈퍼 컴퓨터"예요!**

### 왜 클라우드라고 할까요? ☁️
```
옛날엔:
"내 컴퓨터에 프로그램 설치!"

지금은:
"인터넷에서 빌려 써요!"
→ 마치 구름 위에서 처리하는 것처럼
```

### 3가지 서비스 📦
```
IaaS: "빈 방을 빌려줘요"
  - 내가 가구 배치

PaaS: "가구까지 해줘요"
  - 내가 짐만 놓으면 돼요

SaaS: "다 준비됐어요"
  - 바로 살아요
```

### 좋은 점들 😊
```
필요할 때만 써요
돈은 쓴 만큼만
어디서든 접속해요
```

**비밀**: 넷플릭스도 클라우드를 써요! 🎬✨
