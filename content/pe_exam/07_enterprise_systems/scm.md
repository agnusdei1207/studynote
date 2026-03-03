+++
title = "SCM (공급망 관리)"
date = 2026-03-03

[extra]
categories = "pe_exam-enterprise_systems"
+++

# SCM (공급망 관리)

## 핵심 인사이트 (3줄 요약)
> **원자재부터 최종 소비자까지 전체 흐름을 최적화하는 관리 체계**. 조달, 생산, 물류, 유통을 통합 관리하여 재고 비용 절감, 납기 단축, 고객 만족 향상을 달성한다. Bullwhip Effect 완화와 VMI, CPFR이 핵심 개념이다.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"SCM(Supply Chain Management, 공급망 관리)의 개념과 주요 기능을 설명하고, 기업 정보화 전략 관점에서의 도입 방안과 성공 요인을 논하시오."**

---

### Ⅰ. 개요

#### 1. 개념
SCM(Supply Chain Management, 공급망 관리)은 **원자재 공급업체부터 최종 소비자까지 이르는 전체 공급망을 통합적으로 관리하여 효율성을 극대화하는 경영 활동**이다. 물자, 정보, 자금의 흐름을 최적화하여 재고 비용 절감, 납기 단축, 고객 만족 향상을 달성한다.

> 💡 **비유**: SCM은 마치 **"자동차의 톱니바퀴 시스템"** 같아요. 모든 부품이 맞물려 원활하게 작동하며, 하나가 멈추면 전체가 멈춥니다.

#### 2. 등장 배경
1. **글로벌화와 경쟁 심화**: 글로벌 소싱, 다국적 생산, 전 세계 고객 대응으로 공급망 복잡성 급증
2. **재고 비용 부담**: 과다 재고는 자본 묶임, 부족 재고는 기회 손실. 최적 균형점 필요
3. **고객 요구 다양화**: 빠른 배송, 다양한 제품, 낮은 가격에 대한 고객 기대 상승

#### 3. 핵심 목적
- **비용 최소화**: 재고, 물류, 조달 비용 절감
- **서비스 극대화**: 납기 준수, 가용성 향상
- **속도 향상**: 리드타임 단축, 시장 대응 민첩성

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 4. 공급망 구조 ★
| 단계 | 영문 | 주요 활동 | 핵심 시스템 | 데이터 흐름 |
|-----|------|----------|------------|------------|
| **1단계** | Suppliers | 원자재 공급 | SRM (Supplier Relationship Management) | 공급업체 → 제조사 |
| **2단계** | Manufacturing | 생산, 제조 | MES, APS | 생산 계획, 재고 현황 |
| **3단계** | Distribution | 유통, 물류 | WMS, TMS | 배송 정보, 추적 |
| **4단계** | Retail | 소매, 판매 | POS, OMS | 판매 데이터, 수요 |
| **5단계** | Consumers | 최종 소비자 | CRM | 고객 피드백 |

#### 5. 공급망 흐름 구조
```
┌─────────────────────────────────────────────────────────────────┐
│                       공급망 구조 (Supply Chain)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1단계     2단계     3단계     4단계     5단계                   │
│                                                                 │
│  원자재    제조     유통/     소매/    소비자                    │
│  공급업체   기업     물류     서비스                               │
│                                                                 │
│   ┌───┐    ┌───┐    ┌───┐    ┌───┐    ┌───┐                   │
│   │원료│ ─→ │생산│ ─→ │창고│ ─→ │매장│ ─→ │고객│                   │
│   └───┘    └───┘    └───┘    └───┘    └───┘                   │
│     ↑        ↑        ↑        ↑                                │
│     │        │        │        │                                 │
│  [조달]   [생산]    [물류]   [판매]                              │
│                                                                 │
│  ════════════════════════════════════════════════════════════  │
│         ←───── 정보 흐름 (Information Flow) ─────→              │
│         ←───── 자금 흐름 (Financial Flow) ─────→                │
│         ──────→ 물자 흐름 (Material Flow) ──────→               │
│  ════════════════════════════════════════════════════════════  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 6. SCM 핵심 프로세스 ★
| 프로세스 | 영문 | 주요 활동 | 핵심 지표 |
|---------|------|----------|----------|
| **수요 계획** | Demand Planning | 수요 예측, S&OP, 판매 계획 | 수요 예측 정확도 |
| **조달** | Procurement | 공급업체 관리, 구매 발주, 전략적 조달 | 조달 리드타임, 단가 |
| **생산** | Manufacturing | 생산 계획, 스케줄링, 품질 관리 | 생산 효율, 불량률 |
| **물류** | Logistics | 창고 관리, 운송 관리, 재고 관리 | 재고 회전율, 배송 비용 |
| **주문 관리** | Order Management | 주문 접수, 처리, 출하, 추적 | 주문 충족율, 리드타임 |
| **반품 관리** | Returns | 역물류, 수리, 재활용 | 반품 처리 비용 |

#### 7. SCM 성과 지표 (KPI)
| 지표 | 영문 | 정의 | 목표 방향 | 계산식 |
|-----|------|------|----------|--------|
| **재고 회전율** | Inventory Turnover | 평균 재고 대비 매출 | 높을수록 좋음 | 매출 / 평균재고 |
| **주문 충족율** | Order Fill Rate | 정시 납품 비율 | 높을수록 좋음 | 정시납품건 / 총주문건 |
| **완벽 주문율** | Perfect Order Rate | 무결점 주문 비율 | 높을수록 좋음 | 완벽주문 / 총주문 |
| **현금전환주기** | Cash-to-Cash Cycle | 재고→현금 전환 기간 | 짧을수록 좋음 | 재고일수 + 미수금일수 - 미지급금일수 |
| **리드타임** | Lead Time | 발주~납품 소요시간 | 짧을수록 좋음 | 납품일 - 발주일 |
| **SCM 총비용** | Total SC Cost | 공급망 총운영비용 | 낮을수록 좋음 | 조달+생산+물류+재고비용 |

#### 8. Bullwhip Effect (채찍 효과) ★
```
┌─────────────────────────────────────────────────────────────────┐
│                   Bullwhip Effect (채찍 효과)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  소비자 수요의 작은 변동이 상류로 갈수록 증폭되는 현상            │
│                                                                 │
│  소비자    소매점    도매점    제조사    공급업체                │
│    ↓         ↓         ↓         ↓         ↓                    │
│   ±5%      ±15%      ±25%      ±40%      ±60%                   │
│    │         │         │         │         │                    │
│    ▼         ▼         ▼         ▼         ▼                    │
│   작음     조금 큼     더 큼     매우 큼    극단적                │
│                                                                 │
│  원인:                                                          │
│  1. 수요 예측 오차 (각 단계별 독립 예측)                         │
│  2. 주문批量 (Order Batching) - 비용 절감 위해 몰아서 주문        │
│  3. 가격 변동 (Price Fluctuation) - 프로모션 시기 선별 구매       │
│  4. 게임 행태 (Rationing Game) - 부족 시 과다 주문                │
│                                                                 │
│  해결 방안:                                                      │
│  ✓ 정보 공유 (Information Sharing)                              │
│  ✓ VMI (Vendor Managed Inventory)                              │
│  ✓ CPFR (Collaborative Planning, Forecasting, Replenishment)   │
│  ✓ EDLP (Every Day Low Price) - 가격 안정화                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 9. VMI vs CPFR 비교
| 항목 | VMI (Vendor Managed Inventory) | CPFR (Collaborative Planning) |
|-----|-------------------------------|------------------------------|
| **정의** | 공급업체가 고객 재고 관리 | 공급망 파트너간 협업 계획 |
| **주도** | 공급업체 주도 | 상호 협업 |
| **범위** | 재고 보충 | 수요 예측 + 계획 + 보충 |
| **정보** | 재고 데이터 공유 | 판매, 프로모션, 예측 공유 |
| **적용** | 안정적 수요 품목 | 계절/프로모션 품목 |
| **사례** | P&G → Walmart | P&G ↔ Walmart |

#### 10. 동작 원리 (단계별 상세)
```
① 수요 예측 → ② 계획 수립 → ③ 조달 실행 → ④ 생산 → ⑤ 물류 → ⑥ 성과 측정
```

- **1단계 - 수요 예측**: 과거 판매 데이터, 계절성, 프로모션 효과를 분석하여 미래 수요 예측
- **2단계 - 계획 수립**: S&OP(Sales & Operations Planning)로 영업-생산-조달 계획 통합
- **3단계 - 조달 실행**: 공급업체 발주, 입고 검사, 재고 등록
- **4단계 - 생산**: 생산 계획 기반 제조, 품질 검사, 완제품 입고
- **5단계 - 물류**: 주문 접수 → 피킹 → 포장 → 배송 → 추적
- **6단계 - 성과 측정**: KPI 모니터링, 병목 분석, 지속 개선

#### 11. 코드 예시 (재고 최적화)
```python
# SCM 재고 최적화: 안전 재고 계산 및 발주점 산출

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class InventoryParameters:
    """재고 관리 파라미터"""
    avg_daily_demand: float  # 일평균 수요
    demand_std_dev: float    # 수요 표준편차
    lead_time_days: int      # 리드타임 (일)
    lead_time_std_dev: float # 리드타임 표준편차
    service_level: float     # 서비스 수준 (0.0 ~ 1.0)
    unit_cost: float         # 단가
    holding_cost_rate: float # 재고 보관비율 (연간)
    ordering_cost: float     # 발주 비용

class SCMInventoryOptimizer:
    """SCM 재고 최적화 엔진"""

    def __init__(self, params: InventoryParameters):
        self.params = params
        # 서비스 수준에 따른 Z값 (정규분포)
        self.z_values = {
            0.90: 1.28, 0.95: 1.65, 0.98: 2.05, 0.99: 2.33
        }

    def calculate_safety_stock(self) -> float:
        """
        안전 재고 (Safety Stock) 계산
        SS = Z * SQRT(LT * σd² + d² * σLT²)
        """
        z = self.z_values.get(self.params.service_level, 1.65)
        d = self.params.avg_daily_demand
        lt = self.params.lead_time_days
        sigma_d = self.params.demand_std_dev
        sigma_lt = self.params.lead_time_std_dev

        safety_stock = z * np.sqrt(
            lt * (sigma_d ** 2) + (d ** 2) * (sigma_lt ** 2)
        )
        return safety_stock

    def calculate_reorder_point(self) -> float:
        """
        발주점 (Reorder Point) 계산
        ROP = (일평균수요 × 리드타임) + 안전재고
        """
        cycle_stock = self.params.avg_daily_demand * self.params.lead_time_days
        safety_stock = self.calculate_safety_stock()
        return cycle_stock + safety_stock

    def calculate_eoq(self, annual_demand: float) -> float:
        """
        경제적 주문량 (EOQ, Economic Order Quantity)
        EOQ = SQRT((2 × D × S) / H)
        D: 연간 수요, S: 발주비용, H: 보관비용
        """
        D = annual_demand
        S = self.params.ordering_cost
        H = self.params.unit_cost * self.params.holding_cost_rate

        eoq = np.sqrt((2 * D * S) / H)
        return eoq

    def calculate_total_cost(self, order_quantity: float, annual_demand: float) -> dict:
        """총 재고 비용 계산"""
        D = annual_demand
        Q = order_quantity
        S = self.params.ordering_cost
        C = self.params.unit_cost
        H = C * self.params.holding_cost_rate
        SS = self.calculate_safety_stock()

        ordering_cost = (D / Q) * S
        holding_cost = ((Q / 2) + SS) * H
        purchase_cost = D * C
        total_cost = ordering_cost + holding_cost + purchase_cost

        return {
            'ordering_cost': ordering_cost,
            'holding_cost': holding_cost,
            'purchase_cost': purchase_cost,
            'total_cost': total_cost,
            'avg_inventory': (Q / 2) + SS
        }

    def analyze_bullwhip_effect(self, demand_variations: List[float]) -> dict:
        """
        Bullwhip Effect 분석
        각 단계별 수요 변동성 측정
        """
        variations = np.array(demand_variations)
        cv = np.std(variations) / np.mean(variations)  # 변동계수

        return {
            'mean_demand': np.mean(variations),
            'std_dev': np.std(variations),
            'coefficient_of_variation': cv,
            'bullwhip_ratio': cv / (self.params.demand_std_dev / self.params.avg_daily_demand)
        }


# 사용 예시
if __name__ == "__main__":
    # 파라미터 설정
    params = InventoryParameters(
        avg_daily_demand=100,      # 일평균 100개 판매
        demand_std_dev=20,         # 수요 변동 ±20개
        lead_time_days=7,          # 리드타임 7일
        lead_time_std_dev=2,       # 리드타임 변동 ±2일
        service_level=0.95,        # 95% 서비스 수준
        unit_cost=10000,           # 단가 10,000원
        holding_cost_rate=0.25,    # 연간 보관비율 25%
        ordering_cost=50000        # 발주비용 50,000원
    )

    optimizer = SCMInventoryOptimizer(params)

    # 재고 최적화 계산
    safety_stock = optimizer.calculate_safety_stock()
    reorder_point = optimizer.calculate_reorder_point()
    eoq = optimizer.calculate_eoq(annual_demand=36500)
    costs = optimizer.calculate_total_cost(eoq, annual_demand=36500)

    print("=" * 50)
    print("SCM 재고 최적화 결과")
    print("=" * 50)
    print(f"안전 재고 (Safety Stock): {safety_stock:.0f}개")
    print(f"발주점 (Reorder Point): {reorder_point:.0f}개")
    print(f"경제적 주문량 (EOQ): {eoq:.0f}개")
    print(f"평균 재고: {costs['avg_inventory']:.0f}개")
    print(f"연간 총 재고 비용: {costs['total_cost']:,.0f}원")
    print("=" * 50)
```

---

### Ⅲ. 기술 비교 분석

#### 12. 전통적 SCM vs 디지털 SCM 비교
| 비교 항목 | 전통적 SCM | 디지털 SCM |
|---------|----------|-----------|
| **가시성** | 제한적 (내부만) | End-to-End 실시간 |
| **계획 방식** | 정적, 주기적 | 동적, 실시간 |
| **협업** | 이메일, 전화 | 클라우드 플랫폼 |
| **분석** | 과거 데이터 중심 | AI/ML 예측 |
| **대응 속도** | 느림 (수일~수주) | 빠름 (실시간) |
| **유연성** | 낮음 | 높음 (시나리오 시뮬레이션) |

#### 13. 장단점 분석
| 장점 | 단점 |
|-----|------|
| 재고 비용 절감: 최적 재고 수준 유지 | 높은 구축 비용: 시스템, 프로세스 혁신 |
| 납기 준수율 향상: 리드타임 단축 | 파트너 협업 어려움: 정보 공유 저항 |
| 고객 만족 증대: 높은 가용성 | 복잡성: 글로벌 공급망 관리 난이도 |
| 민첩성 향상: 수요 변화 빠른 대응 | 리스크: 공급망 중단 시 파급효과 큼 |
| 비용 투명화: 공급망 총비용 파악 | 데이터 품질: 파트너간 데이터 표준화 |

#### 14. 대안 기술 비교
| 비교 항목 | SCM Suite | ERP SCM | APS | Control Tower |
|---------|----------|---------|-----|--------------|
| **핵심 특성** | ★ 통합 SCM | ERP 모듈 | 고급 계획 | 실시간 모니터링 |
| **범위** | 전사적 | ERP 중심 | 계획 최적화 | 가시성 중심 |
| **복잡도** | 높음 | 중간 | 높음 | 중간 |
| **비용** | 높음 | 중간 | 높음 | 중간 |
| **적합 환경** | ★ 제조/유통 | ERP 사용 기업 | 복잡한 생산 | 글로벌 공급망 |

> **★ 선택 기준**: 전사적 통합 SCM 필요 시 SCM Suite, 이미 ERP 사용 시 ERP SCM 모듈, 복잡한 생산 계획은 APS, 실시간 가시성은 Control Tower

---

### Ⅳ. 실무 적용 방안

#### 15. 기술사적 적용 시나리오
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **제조업** | 수요 예측 → 생산 계획 → 자재 조달 → 물류 통합 | 재고 25% 감소, 리드타임 30% 단축 |
| **유통업** | VMI, CPFR, 크로스도킹, 자동 보충 | 품절률 50% 감소, 물류비 20% 절감 |
| **소비재** | S&OP, 협업 계획, 포장 최적화 | 매출 10% 증대, 서비스 수준 98% 달성 |
| **의료/제약** | 온도 관리 물류, 유효기간 추적, 추적성 | 폐기율 40% 감소, 규제 준수 100% |

#### 16. 실제 도입 사례
- **사례 1: Walmart** - Retail Link 시스템
  - 공급업체와 실시간 판매 데이터 공유, VMI, CPFR 도입
  - **성과**: 재고 회전율 업계 최고, 물류 비용 15% 절감

- **사례 2: Dell** - Build-to-Order 모델
  - 고객 주문 기반 생산, 최소 재고, 직배송
  - **성과**: 재고 회전율 연 100회 이상, 캐시컨버전 사이클 마이너스

- **사례 3: 삼성전자** - 글로벌 SCM 통합
  - 전 세계 공급망 실시간 가시성, AI 수요 예측
  - **성과**: 수요 예측 정확도 20% 향상, 재고 15% 감소

#### 17. 도입 시 고려사항 (4가지 관점)
1. **기술적 고려사항**
   - 기존 ERP, MES, WMS와의 통합 방안
   - 클라우드 SCM vs 온프레미스 결정
   - 실시간 데이터 처리 아키텍처
   - IoT 센서 데이터 활용 (재고, 위치 추적)

2. **운영적 고려사항**
   - S&OP 프로세스 수립 (영업-생산-조달 협업)
   - KPI 체계 및 성과 측정 시스템
   - 공급망 리스크 관리 (대체 공급업체, BCP)
   - 지속적 개선 (PDCA) 체계

3. **보안적 고려사항**
   - 공급망 파트너간 데이터 보안
   - 공급망 사이버 공격 대응
   - 지적재산권 보호
   - ESG/공급망 실사 (강제노동, 환경규제)

4. **경제적 고려사항**
   - SCM 소프트웨어 라이선스 비용
   - 구현 및 컨설팅 비용
   - 파트너 온보딩 비용
   - ROI 분석: 재고 비용 절감 + 서비스 향상 - 투자 비용

#### 18. 주의사항 / 흔한 실수
- ❌ **부분 최적화**: 전체 공급망 최적화가 아닌 특정 단계만 최적화
- ❌ **정보 공유 부족**: 파트너와 데이터 공유를 꺼려 Bullwhip Effect 악화
- ❌ **과도한 JIT**: 리스크 관리 없는 Zero Inventory는 공급 중단 시 치명적
- ❌ **단기 비용 중심**: 초기 투자 비용만 보고 장기 가치 무시
- ❌ **글로벌 리스크 무시**: 지정학적 리스크, 자연재해 대응 계획 부재

---

### Ⅴ. 기대 효과 및 결론

#### 19. 정량적 기대 효과
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **재고 비용** | 최적 재고 수준 유지, 안전재고 감소 | 재고 비용 20-30% 절감 |
| **물류 비용** | 운송 최적화, 창고 효율화 | 물류 비용 15-25% 절감 |
| **서비스 수준** | 납기 준수율, 가용성 향상 | 주문 충족율 95% 이상 |
| **리드타임** | 계획~납품 기간 단축 | 리드타임 30-50% 단축 |
| **매출** | 품절 감소, 고객 만족 향상 | 매출 5-15% 증대 |
| **캐시플로우** | 현금전환주기 단축 | C2C 사이클 20-40% 단축 |

#### 20. 미래 전망 (3가지 관점)
1. **기술 발전 방향**:
   - AI 기반 수요 예측: 딥러닝으로 계절성, 프로모션, 외부 요인까지 고려
   - Digital Supply Chain Twin: 가상 공급망 복제로 시뮬레이션 및 최적화
   - Blockchain 공급망 추적: 원산지, 유효기간, 진품 여부 투명화

2. **시장 트렌드**:
   - Resilient Supply Chain: COVID-19 이후 회복탄력성 중요성 대두
   - ESG 공급망: 탄소 발자국, 윤리적 소싱 필수 요건화
   - Direct-to-Consumer (DTC): 중간 유통 없이 소비자 직거래

3. **후속 기술**:
   - Autonomous Supply Chain: AI가 자율적으로 계획, 실행, 최적화
   - Circular Supply Chain: 순환 경제 기반 공급망 (재사용, 재활용)
   - Supply Chain as a Service (SCaaS): 클라우드 기반 공급망 서비스

#### 결론
> **SCM(Supply Chain Management, 공급망 관리)**는 기업 경쟁력의 핵심 동력으로, 원자재부터 최종 소비자까지 전체 가치사슬을 최적화하여 비용 절감과 서비스 향상을 동시에 달성한다. 특히 Bullwhip Effect 완화를 위한 정보 공유, VMI, CPFR 등 협업 모델이 성공의 열쇠다. 기술사로서 SCM 도입 시에는 전체 공급망 관점의 최적화, 파트너와의 신뢰 기반 협업, 그리고 리스크 관리를 균형있게 고려해야 한다. 디지털 전환 시대에는 AI, IoT, Blockchain 기술이 결합하여 실시간 가시성, 예측 최적화, 추적성을 제공하는 지능형 공급망으로 진화하고 있다.

> **※ 참고 표준**: SCOR Model (Supply Chain Council), ISO 28000(Supply Chain Security), ISO 31000(Risk Management), GS1 Standards

---

### 관련 개념 / 확장 학습

```
📌 SCM 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                       SCM (공급망 관리)                          │
│                       연관 개념 맵                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [ERP] ←──────────────→ [SCM] ←──────────────→ [CRM]          │
│      ↓                      ↓                      ↓            │
│   [MES] ←─────────→ [APS/WMS/TMS] ←─────────→ [POS/OMS]        │
│                             ↓                                   │
│                    [Bullwhip Effect]                            │
│                             ↓                                   │
│              [VMI / CPFR / Cross-Docking]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **ERP** | 백본 시스템 | SCM 실행을 위한 트랜잭션 처리 | `[ERP](../erp/erp_system.md)` |
| **CRM** | 수요 출처 | 고객 수요 데이터 제공 | `[CRM](./crm.md)` |
| **MES** | 생산 실행 | 생산 현장 데이터 제공 | `[MES](../mes.md)` |
| **Cross-Docking** | 물류 전략 | 보관 없이 즉시 출고 | `[Cross-Docking](./cross_docking.md)` |
| **VMI** | 재고 관리 | 공급업체 재고 관리 | `[자동 보충](./automatic_replenishment.md)` |
| **Bullwhip Effect** | 핵심 개념 | 수요 변동 증폭 현상 | `[Bullwhip Effect](#8-bullwhip-effect-채찍-효과)` |
| **SCOR** | 표준 모델 | 공급망 성과 참조 모델 | SCOR Model (SCC) |

---

## 어린이를 위한 종합 설명

**SCM을 쉽게 이해해보자!**

SCM은 마치 **"피자 배달의 모든 과정"** 같아요.

### 첫 번째 이야기: 피자가 만들어지기까지
피자 한 판이 집에 오기까지 많은 단계가 필요해요:
1. 농부가 밀을 재배해요 (원자재)
2. 공장에서 밀가루를 만들어요 (제조)
3. 창고에 저장해요 (물류)
4. 피자가게로 배달해요 (유통)
5. 피자를 만들어요 (생산)
6. 집으로 배달해요 (최종 소비자)

SCM은 이 모든 과정을 관리해요!

### 두 번째 이야기: 비밀 요술 상자
SCM은 요술 상자처럼 모든 것을 알아요:
- 지금 밀가루가 얼마나 남았는지
- 내일 피자를 얼마나 팔지
- 배달에 얼마나 걸리는지

이 정보로 낭비를 줄이고, 빠르게 배달해요!

### 세 번째 이야기: 채찍 효과 (Bullwhip Effect)
한 명이 피자를 덜 주문하면:
- 피자가게는 "앗, 안 팔리네?" 하고 밀가루를 훨씬 덜 주문해요
- 창고는 "수요가 급감했나?" 하고 공장에 훨씬 덜 주문해요
- 공장은 "큰일 났다!" 하고 농부에게 훨씬 덜 주문해요

작은 변화가 점점 커지는 거예요! SCM은 이것을 막아줘요.

```
SCM = 모든 과정 연결 + 정보 공유 + 낭비 제거
```

---
