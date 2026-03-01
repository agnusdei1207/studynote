+++
title = "고객관계관리 (CRM)"
date = 2025-03-01

[extra]
categories = "enterprise_systems-methodology"
+++

# 고객관계관리 (CRM, Customer Relationship Management)

## 핵심 인사이트 (3줄 요약)
> **고객과의 관계를 체계적으로 관리하여 수익 극대화**하는 전략과 시스템. 고객 데이터 통합, 분석, 타겟팅이 핵심. 마케팅 자동화, 영업 관리, 고객 서비스 통합.

## 1. 개념
CRM(Customer Relationship Management)은 **기업이 고객과의 관계를 체계적으로 관리하고 분석하여 고객 만족을 높이고 수익을 극대화**하는 경영 전략 및 시스템이다.

> 비유: "개인 비서" - 모든 고객을 완벽하게 기억하고 케어

## 2. CRM 구성 요소

```
┌────────────────────────────────────────────────────────┐
│                   CRM 시스템 구성                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 운영형 CRM (Operational CRM)                       │
│     ┌────────────────────────────────────────────┐    │
│     │ • 영업 자동화 (SFA: Sales Force Automation)│    │
│     │ • 마케팅 자동화                            │    │
│     │ • 고객 서비스 자동화                       │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 분석형 CRM (Analytical CRM)                        │
│     ┌────────────────────────────────────────────┐    │
│     │ • 고객 세분화                              │    │
│     │ • 고객 행동 분석                           │    │
│     │ • 캠페인 효과 분석                         │    │
│     │ • 데이터 마이닝                            │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  3. 협업형 CRM (Collaborative CRM)                     │
│     ┌────────────────────────────────────────────┐    │
│     │ • 채널 통합 (옴니채널)                     │    │
│     │ • 부서 간 협업                             │    │
│     │ • 고객 접점 관리                           │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. CRM 프로세스

```
┌────────────────────────────────────────────────────────┐
│                   CRM 프로세스                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  고객 획득        고객 유지        고객 확장           │
│  (Acquire)       (Retain)        (Expand)            │
│                                                        │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐         │
│  │ 마케팅  │────→│ 서비스  │────→│ 업셀링  │         │
│  │ 캠페인  │     │ 지원    │     │ 크로스셀│         │
│  └─────────┘     └─────────┘     └─────────┘         │
│       ↑              ↑               ↑                │
│       │              │               │                │
│       └──────────────┼───────────────┘                │
│                      │                                │
│               ┌──────┴──────┐                         │
│               │ 고객 데이터 │                         │
│               │  통합 관리  │                         │
│               └─────────────┘                         │
│                                                        │
│  고객 생애 가치 (CLV: Customer Lifetime Value)        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import random

class CustomerSegment(Enum):
    VIP = "VIP"
    LOYAL = "충성 고객"
    NEW = "신규 고객"
    AT_RISK = "이탈 위험"
    CHURNED = "이탈 고객"

class InteractionType(Enum):
    PURCHASE = "구매"
    INQUIRY = "문의"
    COMPLAINT = "불만"
    SUPPORT = "지원"
    MARKETING = "마케팅"

@dataclass
class Customer:
    """고객"""
    customer_id: str
    name: str
    email: str
    phone: str
    segment: CustomerSegment = CustomerSegment.NEW
    total_purchases: float = 0.0
    purchase_count: int = 0
    last_interaction: datetime = None
    join_date: datetime = None

    def __post_init__(self):
        if self.join_date is None:
            self.join_date = datetime.now()
        if self.last_interaction is None:
            self.last_interaction = datetime.now()

@dataclass
class Interaction:
    """고객 상호작용"""
    interaction_id: str
    customer_id: str
    interaction_type: InteractionType
    channel: str  # 웹, 앱, 전화, 매장
    description: str
    timestamp: datetime

@dataclass
class Campaign:
    """마케팅 캠페인"""
    campaign_id: str
    name: str
    target_segments: List[CustomerSegment]
    message: str
    channel: str
    sent_count: int = 0
    response_count: int = 0

    @property
    def response_rate(self) -> float:
        return self.response_count / self.sent_count if self.sent_count > 0 else 0

class CRMSystem:
    """CRM 시스템"""

    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.interactions: List[Interaction] = []
        self.campaigns: Dict[str, Campaign] = {}

    # 고객 관리
    def add_customer(self, name: str, email: str, phone: str) -> Customer:
        """고객 등록"""
        customer = Customer(
            customer_id=f"C{len(self.customers)+1:05d}",
            name=name,
            email=email,
            phone=phone
        )
        self.customers[customer.customer_id] = customer
        print(f"[CRM] 고객 등록: {name} ({customer.customer_id})")
        return customer

    def record_interaction(self, customer_id: str, interaction_type: InteractionType,
                          channel: str, description: str) -> Optional[Interaction]:
        """상호작용 기록"""
        if customer_id not in self.customers:
            return None

        interaction = Interaction(
            interaction_id=f"I{len(self.interactions)+1:06d}",
            customer_id=customer_id,
            interaction_type=interaction_type,
            channel=channel,
            description=description,
            timestamp=datetime.now()
        )
        self.interactions.append(interaction)

        # 고객 정보 업데이트
        customer = self.customers[customer_id]
        customer.last_interaction = datetime.now()

        if interaction_type == InteractionType.PURCHASE:
            customer.purchase_count += 1

        return interaction

    def record_purchase(self, customer_id: str, amount: float):
        """구매 기록"""
        customer = self.customers.get(customer_id)
        if customer:
            customer.total_purchases += amount
            customer.purchase_count += 1
            self.record_interaction(customer_id, InteractionType.PURCHASE,
                                   "시스템", f"구매: {amount:,}원")
            self._update_segment(customer_id)

    def _update_segment(self, customer_id: str):
        """고객 세그먼트 업데이트"""
        customer = self.customers.get(customer_id)
        if not customer:
            return

        # 간단한 세그먼트 로직
        days_since_last = (datetime.now() - customer.last_interaction).days

        if customer.total_purchases >= 1_000_000:
            customer.segment = CustomerSegment.VIP
        elif days_since_last > 90:
            customer.segment = CustomerSegment.AT_RISK
        elif customer.purchase_count >= 5:
            customer.segment = CustomerSegment.LOYAL
        elif days_since_last > 180:
            customer.segment = CustomerSegment.CHURNED

    # 분석
    def get_customer_insights(self, customer_id: str) -> Dict:
        """고객 인사이트"""
        customer = self.customers.get(customer_id)
        if not customer:
            return {}

        customer_interactions = [i for i in self.interactions if i.customer_id == customer_id]

        avg_purchase = (customer.total_purchases / customer.purchase_count
                       if customer.purchase_count > 0 else 0)

        return {
            'customer_id': customer_id,
            'name': customer.name,
            'segment': customer.segment.value,
            'total_purchases': customer.total_purchases,
            'purchase_count': customer.purchase_count,
            'avg_purchase': avg_purchase,
            'interaction_count': len(customer_interactions),
            'days_since_last': (datetime.now() - customer.last_interaction).days
        }

    def get_segment_summary(self) -> Dict[str, int]:
        """세그먼트별 요약"""
        summary = {}
        for segment in CustomerSegment:
            count = sum(1 for c in self.customers.values() if c.segment == segment)
            summary[segment.value] = count
        return summary

    # 캠페인
    def create_campaign(self, name: str, target_segments: List[CustomerSegment],
                       message: str, channel: str) -> Campaign:
        """캠페인 생성"""
        campaign = Campaign(
            campaign_id=f"CM{len(self.campaigns)+1:04d}",
            name=name,
            target_segments=target_segments,
            message=message,
            channel=channel
        )
        self.campaigns[campaign.campaign_id] = campaign
        return campaign

    def execute_campaign(self, campaign_id: str) -> int:
        """캠페인 실행"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return 0

        target_customers = [c for c in self.customers.values()
                          if c.segment in campaign.target_segments]

        campaign.sent_count = len(target_customers)

        # 시뮬레이션: 응답률
        campaign.response_count = int(len(target_customers) * random.uniform(0.05, 0.25))

        print(f"[캠페인] {campaign.name} 실행")
        print(f"  발송: {campaign.sent_count}명")
        print(f"  응답: {campaign.response_count}명 ({campaign.response_rate*100:.1f}%)")

        return campaign.sent_count


# 사용 예시
print("=== CRM 시스템 시뮬레이션 ===\n")

crm = CRMSystem()

# 고객 등록
c1 = crm.add_customer("김철수", "kim@example.com", "010-1111-1111")
c2 = crm.add_customer("이영희", "lee@example.com", "010-2222-2222")
c3 = crm.add_customer("박민수", "park@example.com", "010-3333-3333")

# 구매 기록
print("\n--- 구매 기록 ---")
crm.record_purchase(c1.customer_id, 500_000)
crm.record_purchase(c1.customer_id, 600_000)
crm.record_purchase(c2.customer_id, 1_500_000)
crm.record_purchase(c3.customer_id, 100_000)

# 고객 인사이트
print("\n--- 고객 인사이트 ---")
for cid in [c1.customer_id, c2.customer_id]:
    insights = crm.get_customer_insights(cid)
    print(f"{insights['name']}: {insights['segment']}, "
          f"총구매 {insights['total_purchases']:,}원")

# 세그먼트 요약
print("\n--- 세그먼트 요약 ---")
for segment, count in crm.get_segment_summary().items():
    if count > 0:
        print(f"  {segment}: {count}명")

# 캠페인 실행
print("\n--- 마케팅 캠페인 ---")
campaign = crm.create_campaign(
    "VIP 프로모션",
    [CustomerSegment.VIP, CustomerSegment.LOYAL],
    "특별 할인 쿠폰을 드립니다!",
    "이메일"
)
crm.execute_campaign(campaign.campaign_id)
