+++
title = "공급망 관리 (SCM)"
date = 2025-03-01

[extra]
categories = "enterprise_systems-methodology"
+++

# 공급망 관리 (SCM, Supply Chain Management)

## 핵심 인사이트 (3줄 요약)
> **원자재 조달부터 최종 소비자 전달까지 전 과정 관리**. 수요 예측, 재고 최적화, 물류 효율화가 핵심. Bullwhip Effect 완화가 중요 과제.

## 1. 개념
SCM(Supply Chain Management)은 **원자재 조달부터 제품이 최종 소비자에게 전달되기까지의 전 과정을 통합 관리**하여 물류 비용을 절감하고 고객 만족을 높이는 경영 활동이다.

> 비유: "피자 배달" - 재료 구매 → 도우 만들기 → 토핑 → 굽기 → 배달까지 모든 과정 최적화

## 2. 공급망 구조

```
┌────────────────────────────────────────────────────────┐
│                   공급망 흐름                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  물류 흐름 (←):                                        │
│                                                        │
│  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐    │
│  │원자재│←──│제조  │←──│유통  │←──│도매  │←──│소비자│    │
│  │공급자│   │업체  │   │센터  │   │업체  │   │     │    │
│  └─────┘   └─────┘   └─────┘   └─────┘   └─────┘    │
│                                                        │
│  정보 흐름 (→):                                        │
│  주문 정보, 수요 예측, 재고 정보, 납기 정보            │
│                                                        │
│  자금 흐동 (→):                                        │
│  대금 결제, 신용 정보                                   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. SCM 구성 요소

```
┌────────────────────────────────────────────────────────┐
│                   SCM 구성 요소                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 계획 (Plan)                                        │
│     - 수요 예측                                        │
│     - 생산 계획                                        │
│     - 자원 계획                                        │
│                                                        │
│  2. 조달 (Source)                                      │
│     - 공급업체 선정                                    │
│     - 구매 발주                                        │
│     - 공급업체 관리                                    │
│                                                        │
│  3. 제조 (Make)                                        │
│     - 생산 실행                                        │
│     - 품질 관리                                        │
│     - 포장                                             │
│                                                        │
│  4. 배송 (Deliver)                                     │
│     - 주문 관리                                        │
│     - 창고 관리                                        │
│     - 운송 관리                                        │
│                                                        │
│  5. 반품 (Return)                                      │
│     - 역물류                                           │
│     - 반품 처리                                        │
│     - 재활용                                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. Bullwhip Effect (채찍 효과)

```
┌────────────────────────────────────────────────────────┐
│                  Bullwhip Effect                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  소비자 수요의 작은 변동이 상류로 갈수록 증폭됨        │
│                                                        │
│  소비자:  ∿  (작은 변동)                               │
│            ↓                                           │
│  소매상:  ∿∿∿  (증폭)                                 │
│            ↓                                           │
│  도매상:  ∿∿∿∿∿∿  (더 증폭)                           │
│            ↓                                           │
│  제조업: ∿∿∿∿∿∿∿∿∿  (큰 증폭)                         │
│            ↓                                           │
│  공급업: ∿∿∿∿∿∿∿∿∿∿∿∿∿  (최대 증폭)                   │
│                                                        │
│  원인:                                                 │
│  - 수요 예측 오류                                      │
│  - 주문 지연                                           │
│  - 가격 변동                                           │
│  - 일괄 주문                                           │
│                                                        │
│  해결:                                                 │
│  - 정보 공유                                           │
│  - VMI (Vendor Managed Inventory)                     │
│  - VMI (Vendor Managed Inventory)                     │
│  - EDI, 실시간 데이터                                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import random

class OrderStatus(Enum):
    PENDING = "대기"
    PROCESSING = "처리중"
    SHIPPED = "출하"
    DELIVERED = "납품완료"

@dataclass
class Product:
    """제품"""
    product_id: str
    name: str
    unit_cost: float
    lead_time: int  # 일

@dataclass
class Supplier:
    """공급업체"""
    supplier_id: str
    name: str
    products: List[str]
    reliability: float  # 0-1

@dataclass
class Inventory:
    """재고"""
    product_id: str
    quantity: int
    safety_stock: int
    reorder_point: int

@dataclass
class PurchaseOrder:
    """구매 주문"""
    po_id: str
    supplier_id: str
    product_id: str
    quantity: int
    order_date: datetime
    expected_date: datetime
    status: str = "발주"

@dataclass
class SalesOrder:
    """판매 주문"""
    so_id: str
    customer_id: str
    product_id: str
    quantity: int
    order_date: datetime
    status: OrderStatus = OrderStatus.PENDING

class SupplyChainSystem:
    """공급망 관리 시스템"""

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.suppliers: Dict[str, Supplier] = {}
        self.inventory: Dict[str, Inventory] = {}
        self.purchase_orders: List[PurchaseOrder] = []
        self.sales_orders: List[SalesOrder] = []

    def add_product(self, product_id: str, name: str, unit_cost: float, lead_time: int):
        """제품 등록"""
        self.products[product_id] = Product(product_id, name, unit_cost, lead_time)
        self.inventory[product_id] = Inventory(product_id, 0, 10, 20)

    def add_supplier(self, supplier_id: str, name: str, products: List[str], reliability: float):
        """공급업체 등록"""
        self.suppliers[supplier_id] = Supplier(supplier_id, name, products, reliability)

    def receive_inventory(self, product_id: str, quantity: int):
        """재고 입고"""
        if product_id in self.inventory:
            self.inventory[product_id].quantity += quantity
            print(f"[재고] {product_id} 입고: +{quantity} → 현재 {self.inventory[product_id].quantity}")

    def create_sales_order(self, customer_id: str, product_id: str, quantity: int) -> Optional[SalesOrder]:
        """판매 주문 생성"""
        if product_id not in self.inventory:
            return None

        inv = self.inventory[product_id]
        if inv.quantity < quantity:
            print(f"[주문] 재고 부족: {product_id} (요청 {quantity}, 재고 {inv.quantity})")
            self._check_reorder(product_id)
            return None

        # 재고 차감
        inv.quantity -= quantity

        so = SalesOrder(
            so_id=f"SO{len(self.sales_orders)+1:05d}",
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            order_date=datetime.now()
        )
        self.sales_orders.append(so)
        print(f"[주문] {so.so_id} 생성: {product_id} {quantity}개")

        # 재주문 확인
        self._check_reorder(product_id)

        return so

    def _check_reorder(self, product_id: str):
        """재주문 확인"""
        inv = self.inventory.get(product_id)
        if not inv:
            return

        if inv.quantity <= inv.reorder_point:
            print(f"[재주문] {product_id} 재주문 필요 (현재: {inv.quantity})")
            self._create_purchase_order(product_id, 50)  # 기본 50개 주문

    def _create_purchase_order(self, product_id: str, quantity: int):
        """구매 주문 생성"""
        # 적합한 공급업체 찾기
        supplier = None
        for s in self.suppliers.values():
            if product_id in s.products:
                supplier = s
                break

        if not supplier:
            print(f"[구매] 공급업체 없음: {product_id}")
            return

        product = self.products.get(product_id)
        lead_time = product.lead_time if product else 7

        po = PurchaseOrder(
            po_id=f"PO{len(self.purchase_orders)+1:05d}",
            supplier_id=supplier.supplier_id,
            product_id=product_id,
            quantity=quantity,
            order_date=datetime.now(),
            expected_date=datetime.now() + timedelta(days=lead_time)
        )
        self.purchase_orders.append(po)
        print(f"[구매] {po.po_id} 발주: {supplier.name} → {product_id} {quantity}개 "
              f"(예상: {po.expected_date.strftime('%m/%d')})")

    def receive_purchase_order(self, po_id: str):
        """구매 입고"""
        for po in self.purchase_orders:
            if po.po_id == po_id and po.status == "발주":
                # 신뢰도에 따른 실제 입고량
                supplier = self.suppliers.get(po.supplier_id)
                actual_qty = int(po.quantity * (supplier.reliability if supplier else 0.9))

                self.receive_inventory(po.product_id, actual_qty)
                po.status = "입고완료"
                return

    def get_inventory_status(self) -> Dict:
        """재고 현황"""
        status = {}
        for product_id, inv in self.inventory.items():
            product = self.products.get(product_id)
            status[product_id] = {
                'name': product.name if product else product_id,
                'quantity': inv.quantity,
                'safety_stock': inv.safety_stock,
                'status': '정상' if inv.quantity > inv.safety_stock else '부족'
            }
        return status


# 사용 예시
print("=== 공급망 관리 시뮬레이션 ===\n")

scm = SupplyChainSystem()

# 제품 등록
scm.add_product("P001", "노트북", 1_000_000, 7)
scm.add_product("P002", "마우스", 30_000, 3)

# 공급업체 등록
scm.add_supplier("S001", "전자부품(주)", ["P001", "P002"], 0.95)
scm.add_supplier("S002", "액세서리상사", ["P002"], 0.90)

# 초기 재고
scm.receive_inventory("P001", 30)
scm.receive_inventory("P002", 100)

# 판매 주문
print("\n--- 판매 주문 ---")
scm.create_sales_order("C001", "P001", 5)
scm.create_sales_order("C002", "P001", 20)  # 재고 부족 → 재주문

# 구매 입고
print("\n--- 구매 입고 ---")
for po in scm.purchase_orders:
    scm.receive_purchase_order(po.po_id)

# 재고 현황
print("\n--- 재고 현황 ---")
for pid, info in scm.get_inventory_status().items():
    print(f"  {info['name']}: {info['quantity']}개 ({info['status']})")
