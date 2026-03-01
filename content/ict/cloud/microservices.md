+++
title = "마이크로서비스 (Microservices)"
date = 2025-03-01

[extra]
categories = "ict-cloud"
+++

# 마이크로서비스 (Microservices)

## 핵심 인사이트 (3줄 요약)
> **단일 애플리케이션을 작은 독립 서비스들로 분해**하는 아키텍처 스타일. 각 서비스는 독립 배포, 확장, 개발 가능. API 게이트웨이, 서비스 디스커버리, 이벤트 버스가 핵심.

## 1. 개념
마이크로서비스 아키텍처는 **애플리케이션을 비즈니스 기능 중심의 작고 독립적인 서비스들로 분리**하여 개발하고 배포하는 아키텍처 패턴이다.

> 비유: "음식점 주방" - 각 요리사가 자기 요리만 전문적으로 담당

## 2. 모놀리식 vs 마이크로서비스

```
┌────────────────────────────────────────────────────────┐
│           모놀리식 vs 마이크로서비스                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  모놀리식 (Monolithic):                               │
│  ┌──────────────────────────────────────────────┐     │
│  │                                              │     │
│  │   ┌─────────────────────────────────────┐   │     │
│  │   │         단일 애플리케이션            │   │     │
│  │   │  ┌─────┬─────┬─────┬─────┐          │   │     │
│  │   │  │ 사용자│ 주문 │ 결제 │ 배송 │          │   │     │
│  │   │  └─────┴─────┴─────┴─────┘          │   │     │
│  │   │         ↓      ↓      ↓              │   │     │
│  │   │      ┌─────────────────┐             │   │     │
│  │   │      │   단일 데이터베이스 │             │   │     │
│  │   │      └─────────────────┘             │   │     │
│  │   └─────────────────────────────────────┘   │     │
│  │                                              │     │
│  └──────────────────────────────────────────────┘     │
│  → 전체를 다시 배포해야 함                            │
│  → 하나가 죽으면 전체 장애                            │
│                                                        │
│  마이크로서비스 (Microservices):                       │
│  ┌──────────────────────────────────────────────┐     │
│  │                                              │     │
│  │   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐    │     │
│  │   │사용자│   │ 주문 │   │ 결제 │   │ 배송 │    │     │
│  │   │서비스│   │서비스│   │서비스│   │서비스│    │     │
│  │   └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘    │     │
│  │      ↓         ↓         ↓         ↓        │     │
│  │   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐    │     │
│  │   │ DB1 │   │ DB2 │   │ DB3 │   │ DB4 │    │     │
│  │   └─────┘   └─────┘   └─────┘   └─────┘    │     │
│  │                                              │     │
│  └──────────────────────────────────────────────┘     │
│  → 서비스별 독립 배포                                 │
│  → 서비스별 독립 확장                                 │
│                                                        │
└────────────────────────────────────────────────────────┘

비교표:
┌─────────────┬─────────────┬─────────────────┐
│    구분      │  모놀리식   │  마이크로서비스 │
├─────────────┼─────────────┼─────────────────┤
│ 배포        │ 전체 재배포 │ 서비스별 배포   │
│ 확장        │ 전체 확장   │ 서비스별 확장   │
│ 기술 스택   │ 통일        │ 서비스별 가능   │
│ 장애 영향   │ 전체        │ 일부            │
│ 개발 복잡도 │ 낮음        │ 높음            │
│ 운영 복잡도 │ 낮음        │ 높음            │
│ 팀 구성     │ 중앙화      │ 분산화          │
└─────────────┴─────────────┴─────────────────┘
```

## 3. 마이크로서비스 패턴

```
┌────────────────────────────────────────────────────────┐
│              마이크로서비스 아키텍처 패턴               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. API 게이트웨이                                     │
│     ┌────────────────────────────────────────┐        │
│     │              API Gateway               │        │
│     │  - 라우팅, 인증, 속도 제한             │        │
│     └───────────┬────────────────────────────┘        │
│           ┌─────┼─────┬─────┬─────┐                   │
│           ↓     ↓     ↓     ↓                        │
│        [서비스A][서비스B][서비스C][서비스D]            │
│                                                        │
│  2. 서비스 디스커버리                                  │
│     - 서비스 등록 및 찾기                              │
│     - Eureka, Consul, etcd                            │
│                                                        │
│  3. 이벤트 버스 / 메시지 큐                            │
│     - 비동기 통신                                      │
│     - Kafka, RabbitMQ, AWS SQS                        │
│                                                        │
│  4. 서비스 메시                                        │
│     - 서비스 간 통신 관리                              │
│     - Istio, Linkerd                                  │
│                                                        │
│  5. CQRS (Command Query Responsibility Segregation)   │
│     - 읽기/쓰기 분리                                   │
│     - 성능 최적화                                      │
│                                                        │
│  6. 사가 (Saga) 패턴                                   │
│     - 분산 트랜잭션                                    │
│     - 보상 트랜잭션                                    │
│                                                        │
│  7. 회로 차단기 (Circuit Breaker)                     │
│     - 장애 전파 방지                                   │
│     - Hystrix, Resilience4j                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import uuid
import json
from datetime import datetime

class ServiceStatus(Enum):
    UP = "UP"
    DOWN = "DOWN"
    STARTING = "STARTING"

@dataclass
class Service:
    """마이크로서비스"""
    name: str
    host: str
    port: int
    status: ServiceStatus = ServiceStatus.UP
    endpoints: List[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

class ServiceRegistry:
    """서비스 디스커버리 (서비스 등록소)"""

    def __init__(self):
        self.services: Dict[str, List[Service]] = {}

    def register(self, service: Service):
        """서비스 등록"""
        if service.name not in self.services:
            self.services[service.name] = []
        self.services[service.name].append(service)
        print(f"[Registry] 서비스 등록: {service.name} @ {service.url}")

    def deregister(self, service_name: str, url: str):
        """서비스 해제"""
        if service_name in self.services:
            self.services[service_name] = [
                s for s in self.services[service_name] if s.url != url
            ]

    def discover(self, service_name: str) -> Optional[Service]:
        """서비스 찾기 (라운드 로빈)"""
        instances = self.services.get(service_name, [])
        active = [s for s in instances if s.status == ServiceStatus.UP]
        if active:
            return active[0]  # 간단히 첫 번째 반환
        return None

class APIGateway:
    """API 게이트웨이"""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.routes: Dict[str, str] = {}  # path -> service_name
        self.rate_limits: Dict[str, int] = {}
        self.request_counts: Dict[str, int] = {}

    def add_route(self, path: str, service_name: str):
        """라우트 추가"""
        self.routes[path] = service_name
        print(f"[Gateway] 라우트 추가: {path} → {service_name}")

    def request(self, path: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
        """요청 처리"""
        # 라우트 찾기
        service_name = None
        for route_path, svc in self.routes.items():
            if path.startswith(route_path):
                service_name = svc
                break

        if not service_name:
            return {"error": "Route not found", "status": 404}

        # 속도 제한 확인
        if service_name in self.rate_limits:
            count = self.request_counts.get(service_name, 0)
            if count >= self.rate_limits[service_name]:
                return {"error": "Rate limit exceeded", "status": 429}
            self.request_counts[service_name] = count + 1

        # 서비스 찾기
        service = self.registry.discover(service_name)
        if not service:
            return {"error": "Service unavailable", "status": 503}

        # 요청 전달 (시뮬레이션)
        print(f"[Gateway] {method} {path} → {service.url}")
        return {"status": 200, "service": service.name, "data": data}

class EventBus:
    """이벤트 버스 (메시지 큐 시뮬레이션)"""

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.events: List[Dict] = []

    def subscribe(self, event_type: str, handler: Callable):
        """구독"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: Dict):
        """발행"""
        event = {
            'id': str(uuid.uuid4()),
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.events.append(event)
        print(f"[EventBus] 이벤트 발행: {event_type}")

        # 핸들러 실행
        handlers = self.subscribers.get(event_type, [])
        for handler in handlers:
            handler(event)

class OrderService:
    """주문 서비스"""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.orders: Dict[str, Dict] = {}

    def create_order(self, user_id: str, items: List[Dict]) -> str:
        """주문 생성"""
        order_id = str(uuid.uuid4())[:8]
        order = {
            'order_id': order_id,
            'user_id': user_id,
            'items': items,
            'status': 'CREATED',
            'total': sum(item['price'] for item in items)
        }
        self.orders[order_id] = order

        # 이벤트 발행
        self.event_bus.publish('ORDER_CREATED', order)
        return order_id

class PaymentService:
    """결제 서비스"""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.payments: Dict[str, Dict] = {}
        # 이벤트 구독
        event_bus.subscribe('ORDER_CREATED', self.handle_order_created)

    def handle_order_created(self, event):
        """주문 생성 이벤트 처리"""
        order = event['data']
        print(f"[Payment] 주문 결제 처리: {order['order_id']}")
        # 결제 처리 시뮬레이션
        payment_id = str(uuid.uuid4())[:8]
        self.payments[payment_id] = {
            'payment_id': payment_id,
            'order_id': order['order_id'],
            'amount': order['total'],
            'status': 'COMPLETED'
        }
        # 결제 완료 이벤트 발행
        self.event_bus.publish('PAYMENT_COMPLETED', {
            'order_id': order['order_id'],
            'payment_id': payment_id
        })


# 사용 예시
print("=== 마이크로서비스 시뮬레이션 ===\n")

# 인프라 설정
registry = ServiceRegistry()
gateway = APIGateway(registry)
event_bus = EventBus()

# 서비스 등록
user_service = Service("user-service", "10.0.1.1", 8080, endpoints=["/users"])
order_service = Service("order-service", "10.0.1.2", 8080, endpoints=["/orders"])
payment_service = Service("payment-service", "10.0.1.3", 8080, endpoints=["/payments"])

registry.register(user_service)
registry.register(order_service)
registry.register(payment_service)

# 게이트웨이 라우팅 설정
gateway.add_route("/users", "user-service")
gateway.add_route("/orders", "order-service")
gateway.add_route("/payments", "payment-service")

# 비즈니스 서비스 생성
order_svc = OrderService(event_bus)
payment_svc = PaymentService(event_bus)

# 주문 생성 (이벤트 체인 시작)
print("\n--- 주문 프로세스 ---")
order_id = order_svc.create_order("user123", [
    {"name": "노트북", "price": 1500000},
    {"name": "마우스", "price": 50000}
])

# API 요청 시뮬레이션
print("\n--- API 요청 ---")
response = gateway.request("/orders/123", "GET")
print(f"응답: {response}")
