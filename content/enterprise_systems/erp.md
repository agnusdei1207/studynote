+++
title = "전사적 자원 관리 (ERP)"
date = 2025-03-01

[extra]
categories = "enterprise_systems-main"
+++

# 전사적 자원 관리 (ERP)

## 핵심 인사이트 (3줄 요약)
> **기업의 모든 자원을 통합 관리하는 시스템**. 재무, 인사, 생산, 영업 등 부서별 시스템을 하나로 통합. 실시간 정보 공유와 프로세스 효율화가 핵심.

## 1. 개념
ERP(Enterprise Resource Planning)는 **기업의 인적, 물적, 재무 자원을 통합적으로 관리**하여 경영 효율을 극대화하는 시스템이다.

> 비유: "기업의 뇌" - 모든 부서의 정보가 모이고 처리되는 중추

## 2. ERP 등장 배경

```
전통적 시스템의 문제:
┌────────────────────────────────────────────────────┐
│                                                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │  재무   │  │  인사   │  │  생산   │           │
│  │ 시스템  │  │ 시스템  │  │ 시스템  │           │
│  └─────────┘  └─────────┘  └─────────┘           │
│       ↑            ↑            ↑                 │
│       │            │            │                 │
│    데이터      데이터 중복    데이터              │
│    단절        문제          불일치               │
│                                                    │
└────────────────────────────────────────────────────┘

ERP의 해결:
┌────────────────────────────────────────────────────┐
│                                                    │
│              ┌─────────────────┐                  │
│              │   통합 DB       │                  │
│              └────────┬────────┘                  │
│         ┌─────────────┼─────────────┐             │
│         ↓             ↓             ↓             │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│    │  재무   │  │  인사   │  │  생산   │         │
│    │ 모듈   │  │ 모듈   │  │ 모듈   │         │
│    └─────────┘  └─────────┘  └─────────┘         │
│                                                    │
│    → 실시간 데이터 공유, 일관성 유지              │
│                                                    │
└────────────────────────────────────────────────────┘
```

## 3. ERP 모듈 구성

```
┌────────────────────────────────────────────────────────┐
│                    ERP 모듈 구성                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   재무회계   │  │   인사관리   │  │   구매관리   │   │
│  │ - 총계정원장 │  │ - 급여관리   │  │ - 발주관리   │   │
│  │ - 매출채권   │  │ - 인사정보   │  │ - 공급업체   │   │
│  │ - 매입채무   │  │ - 근태관리   │  │ - 구매입고   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   생산관리   │  │   영업관리   │  │   재고관리   │   │
│  │ - 생산계획   │  │ - 주문관리   │  │ - 창고관리   │   │
│  │ - 자재소요   │  │ - 출하관리   │  │ - 재고평가   │   │
│  │ - 작업지시   │  │ - 매출관리   │  │ - 재고조회   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   원가관리   │  │   품질관리   │  │   설비관리   │   │
│  │ - 원가계산   │  │ - 품질검사   │  │ - 설비유지   │   │
│  │ - 수익분석   │  │ - 불량분석   │  │ - 예방정비   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. ERP 도입 효과

```
1. 업무 효율성
   - 프로세스 표준화
   - 자동화로 인력 절감
   - 중복 업무 제거

2. 정보의 실시간성
   - 즉각적인 현황 파악
   - 의사결정 속도 향상
   - 정확한 정보 제공

3. 데이터 일관성
   - 단일 데이터베이스
   - 데이터 중복 제거
   - 정보 신뢰성 향상

4. 비용 절감
   - 재고 비용 감소
   - 운영 비용 절감
   - 관리 비용 절감

5. 경쟁력 강화
   - 고객 대응 속도
   - 품질 향상
   - 납기 준수
```

## 5. ERP 도입 절차

```
┌────────────────────────────────────────────────────────┐
│                   ERP 도입 절차                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 프로젝트 착수                                      │
│     - 도입 목표 설정                                   │
│     - 프로젝트 팀 구성                                 │
│     - 일정 수립                                        │
│                                                        │
│  2. 업무 분석                                          │
│     - 현행 업무 분석                                   │
│     - 요구사항 정의                                    │
│     - 프로세스 정의                                    │
│                                                        │
│  3. 시스템 설계                                        │
│     - 패키지 선정                                      │
│     - Gap 분석                                         │
│     - 커스터마이징 계획                                │
│                                                        │
│  4. 개발 및 구현                                       │
│     - 패키지 설치                                      │
│     - 커스터마이징                                     │
│     - 인터페이스 개발                                  │
│                                                        │
│  5. 테스트                                             │
│     - 단위 테스트                                      │
│     - 통합 테스트                                      │
│     - 사용자 테스트                                    │
│                                                        │
│  6. 교육 및 가동                                       │
│     - 사용자 교육                                      │
│     - 데이터 이관                                      │
│     - 병행 운영                                        │
│                                                        │
│  7. 안정화                                             │
│     - 운영 지원                                        │
│     - 성능 튜닝                                        │
│     - 지속적 개선                                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 6. 주요 ERP 솔루션

```
글로벌 ERP:
- SAP S/4HANA (독일)
- Oracle ERP Cloud (미국)
- Microsoft Dynamics 365 (미국)

국내 ERP:
- 더존비즈온 (iCube, Smart A)
- 영림원소프트랩 (K-System)
- 대우인포메이션 (ITManager)
- 티엠디티 (ProSense)

클라우드 ERP:
- SAP Business ByDesign
- Oracle NetSuite
- Workday
```

## 7. 코드 예시

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "접수"
    CONFIRMED = "확정"
    SHIPPED = "출하"
    DELIVERED = "납품완료"

@dataclass
class Product:
    """제품"""
    code: str
    name: str
    price: float
    stock: int = 0

@dataclass
class Customer:
    """고객"""
    code: str
    name: str
    credit_limit: float
    balance: float = 0.0

@dataclass
class Order:
    """주문"""
    order_no: str
    customer_code: str
    items: List[Dict]  # [{product_code, qty, price}]
    order_date: datetime
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0.0

    def calculate_total(self) -> float:
        self.total_amount = sum(item['qty'] * item['price'] for item in self.items)
        return self.total_amount

@dataclass
class PurchaseOrder:
    """구매 주문"""
    po_no: str
    supplier_code: str
    items: List[Dict]
    order_date: datetime
    status: str = "발주"

class ERPSystem:
    """ERP 시스템 시뮬레이션"""

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.customers: Dict[str, Customer] = {}
        self.orders: List[Order] = []
        self.purchase_orders: List[PurchaseOrder] = []
        self.inventory_transactions: List[Dict] = []
        self.gl_entries: List[Dict] = []  # 총계정원장 분개

    # ===== 기준 정보 관리 =====
    def add_product(self, product: Product):
        self.products[product.code] = product

    def add_customer(self, customer: Customer):
        self.customers[customer.code] = customer

    # ===== 영업 관리 =====
    def create_order(self, customer_code: str, items: List[Dict]) -> Optional[Order]:
        """주문 생성"""
        if customer_code not in self.customers:
            print("고객을 찾을 수 없습니다")
            return None

        order = Order(
            order_no=f"SO-{len(self.orders)+1:06d}",
            customer_code=customer_code,
            items=items,
            order_date=datetime.now()
        )
        order.calculate_total()
        self.orders.append(order)
        print(f"주문 생성: {order.order_no}")
        return order

    def confirm_order(self, order_no: str) -> bool:
        """주문 확정"""
        for order in self.orders:
            if order.order_no == order_no:
                # 재고 확인
                for item in order.items:
                    product = self.products.get(item['product_code'])
                    if product and product.stock < item['qty']:
                        print(f"재고 부족: {product.name}")
                        return False

                order.status = OrderStatus.CONFIRMED
                print(f"주문 확정: {order_no}")
                return True
        return False

    def ship_order(self, order_no: str) -> bool:
        """주문 출하"""
        for order in self.orders:
            if order.order_no == order_no and order.status == OrderStatus.CONFIRMED:
                # 재고 차감
                for item in order.items:
                    product = self.products.get(item['product_code'])
                    if product:
                        product.stock -= item['qty']
                        self.inventory_transactions.append({
                            'type': '출고',
                            'product': product.code,
                            'qty': -item['qty'],
                            'date': datetime.now()
                        })

                # 매출 분개
                self.gl_entries.append({
                    'type': '매출',
                    'debit': '현금/매출채권',
                    'credit': '매출',
                    'amount': order.total_amount
                })

                order.status = OrderStatus.SHIPPED
                print(f"주문 출하: {order_no}")
                return True
        return False

    # ===== 구매 관리 =====
    def create_purchase_order(self, supplier_code: str, items: List[Dict]) -> PurchaseOrder:
        """구매 주문 생성"""
        po = PurchaseOrder(
            po_no=f"PO-{len(self.purchase_orders)+1:06d}",
            supplier_code=supplier_code,
            items=items,
            order_date=datetime.now()
        )
        self.purchase_orders.append(po)
        print(f"구매 주문 생성: {po.po_no}")
        return po

    def receive_purchase(self, po_no: str):
        """구매 입고"""
        for po in self.purchase_orders:
            if po.po_no == po_no:
                for item in po.items:
                    product = self.products.get(item['product_code'])
                    if product:
                        product.stock += item['qty']
                        self.inventory_transactions.append({
                            'type': '입고',
                            'product': product.code,
                            'qty': item['qty'],
                            'date': datetime.now()
                        })
                po.status = "입고완료"
                print(f"입고 완료: {po_no}")

    # ===== 재고 관리 =====
    def get_stock_status(self) -> Dict:
        """재고 현황"""
        return {code: p.stock for code, p in self.products.items()}

    # ===== 재무 관리 =====
    def get_sales_summary(self) -> Dict:
        """매출 요약"""
        total_sales = sum(
            o.total_amount for o in self.orders
            if o.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]
        )
        return {
            'total_orders': len(self.orders),
            'total_sales': total_sales
        }


# 사용 예시
print("=== ERP 시스템 시뮬레이션 ===\n")

erp = ERPSystem()

# 기준 정보 등록
erp.add_product(Product("P001", "노트북", 1500000, 100))
erp.add_product(Product("P002", "모니터", 300000, 50))
erp.add_customer(Customer("C001", "ABC회사", 10000000))

# 영업 프로세스
print("--- 영업 관리 ---")
order = erp.create_order("C001", [
    {"product_code": "P001", "qty": 5, "price": 1500000},
    {"product_code": "P002", "qty": 5, "price": 300000}
])
erp.confirm_order(order.order_no)
erp.ship_order(order.order_no)

# 구매 프로세스
print("\n--- 구매 관리 ---")
po = erp.create_purchase_order("S001", [
    {"product_code": "P001", "qty": 20}
])
erp.receive_purchase(po.po_no)

# 재고 현황
print("\n--- 재고 현황 ---")
for code, stock in erp.get_stock_status().items():
    product = erp.products[code]
    print(f"{product.name}: {stock}개")

# 매출 요약
print("\n--- 매출 요약 ---")
summary = erp.get_sales_summary()
print(f"총 주문: {summary['total_orders']}건")
print(f"총 매출: {summary['total_sales']:,}원")
```

## 8. ERP 도입 성공 요인

```
1. 최고경영층의 지원
   - 적극적인 관심과 지원
   - 충분한 예산 확보

2. 명확한 목표 설정
   - 구체적인 기대 효과
   - 측정 가능한 지표

3. 사용자 참여
   - 현업 담당자 참여
   - 의사결정 신속성

4. 체계적인 교육
   - 충분한 교육 시간
   - 지속적인 지원

5. 전문가 활용
   - 컨설팅 업체 선정
   - 검증된 방법론
```

## 9. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 통합 관리 | 전사적 자원 통합 |
| 실시간 | 즉각적 정보 파악 |
| 표준화 | 프로세스 표준화 |
| 효율성 | 업무 자동화 |

### 단점
| 단점 | 설명 |
|-----|------|
| 비용 | 높은 도입 비용 |
| 시간 | 긴 구축 기간 |
| 복잡성 | 높은 복잡도 |
| 저항 | 조직 저항 |

## 10. 실무에선? (기술사적 판단)
- **중견/대기업**: SAP, Oracle 등 글로벌 ERP
- **중소기업**: 더존, 영림원 등 국산 ERP
- **클라우드**: 초기 비용 절감, 빠른 도입
- **BPR**: ERP 도입 전 업무 재설계 선행

## 11. 관련 개념
- CRM (고객관계관리)
- SCM (공급망관리)
- BPR (업무프로세스재설계)
- EAI (전사적 애플리케이션 통합)

---

## 어린이를 위한 종합 설명

**ERP는 "기업의 만능 리모컨"이에요!**

### 왜 필요할까요? 🏢
```
옛날엔:
재무팀 → 자기 장부
인사팀 → 자기 장부
생산팀 → 자기 장부
→ 서로 몰라요! 😵

ERP는:
모두가 같은 정보를 봐요
→ 다 같이 알아요! 😊
```

### 무엇을 관리하나요? 📋
```
돈: 재무, 회계
사람: 인사, 급여
물건: 재고, 생산
판매: 주문, 출하
```

### 어떻게 도입하나요? 🚀
```
1. 무엇이 필요한지 정해요
2. 어떤 제품이 좋은지 골라요
3. 설치하고 맞춰요
4. 교육받고 써요
5. 계속 고쳐요
```

**비밀**: 큰 회사들은 ERP 없이 일하기 힘들어요! 🏭✨
