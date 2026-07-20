---
title: "Data Product"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 154
---
## 핵심 인사이트 (3줄 요약)
1. 데이터 제품(Data Product)은 단순한 데이터셋이 아니라 <strong>명확한 인터페이스(API), SLA (Service Level Agreement), 소유권, 품질 계약</strong>을 갖춘 독립적으로 배포 가능한 데이터 단위다.
2. 데이터 계약(Data Contract)은 생산자(Producer)와 소비자(Consumer) 사이의 스키마·SLA·품질 기대값을 명시한 공식 협약으로, 파이프라인 브레이킹 체인지를 사전에 방지한다.
3. 좋은 데이터 제품은 <strong>발견 가능(Discoverable)·주소 지정 가능(Addressable)·신뢰 가능(Trustworthy)·자기 기술(Self-Describing)·상호 운용 가능(Interoperable)</strong>이라는 5가지 특성을 충족한다.

---

## Ⅰ. 개요 및 필요성

전통적 데이터 파이프라인 환경에서 데이터는 파이프라인의 부산물로 취급된다. 스키마가 변경되면 다운스트림 소비자가 조용히 깨지고, 어떤 팀이 데이터를 소유하는지 불명확하며, 데이터 품질 SLA가 없어 소비자는 항상 신뢰 가능 여부를 직접 검증해야 한다.

Data Mesh에서 등장한 데이터 제품 개념은 소프트웨어 제품 개발 방법론을 데이터에 적용한다. 소프트웨어 팀이 REST API에 버전·SLA·문서를 붙이듯, 데이터 팀도 자신의 데이터셋을 명시적 계약과 함께 게시해야 한다.

| 기존 데이터셋 | 데이터 제품 |
|:---|:---|
| 파이프라인 부산물 | 독립적 배포 단위 |
| 소유권 불명확 | 명시적 소유 팀 |
| 스키마 암묵적 가정 | 버전 관리된 스키마 계약 |
| SLA 없음 | 가용성·신선도·품질 SLA |
| 발견 어려움 | 카탈로그 등록·검색 가능 |

> 📢 **섹션 요약 비유**: 데이터 제품은 마트에서 파는 포장 식품이다. 영양 성분표(스키마), 유통기한(신선도 SLA), 제조사(소유 팀), 바코드(주소)가 모두 붙어 있어 소비자가 구매 전에 신뢰 여부를 판단할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+-------------------------------------------------------------------+
|               데이터 제품 구조 (Data Product Structure)             |
+-------------------------------------------------------------------+
|                                                                   |
|  +-------------------------------------------------------------+ |
|  |  데이터 제품: sales.gold.daily_orders                         | |
|  +-------------------------------------------------------------+ |
|  |  📋 스키마 계약 (Data Contract)                               | |
|  |  - order_date: DATE NOT NULL                                  | |
|  |  - total_amount: DECIMAL(18,2) NOT NULL                       | |
|  |  - region: STRING (values: KR/US/EU)                          | |
|  |  - 버전: v2.1.0 (SemVer)                                      | |
|  +-------------------------------------------------------------+ |
|  |  📊 SLA 지표                                                  | |
|  |  - 신선도: 매일 09:00 KST 이전 갱신 보장                       | |
|  |  - 가용성: 99.5% (월간)                                        | |
|  |  - 완전성: null_rate < 1%                                     | |
|  |  - 정확성: amount_variance < 0.01%                            | |
|  +-------------------------------------------------------------+ |
|  |  🔍 발견 가능성 (Data Catalog 등록)                            | |
|  |  - 소유 팀: Sales Analytics Team                              | |
|  |  - 연락처: #data-sales Slack 채널                             | |
|  |  - 리니지: bronze.orders -> silver.orders_clean -> gold.daily  | |
|  |  - 사용 예시 쿼리 3개 등록                                     | |
|  +-------------------------------------------------------------+ |
|  |  🔌 접근 인터페이스                                            | |
|  |  - Delta Table URI: catalog.schema.table (Spark/SQL)          | |
|  |  - Delta Sharing: REST API (외부 소비자)                       | |
|  |  - Kafka Topic: `sales.daily_orders.v2` (스트리밍)             | |
|  +-------------------------------------------------------------+ |
+-------------------------------------------------------------------+
```

<strong>데이터 제품 5대 특성 (Dehghani 정의)</strong>

| 특성 | 설명 | 구현 방법 |
|:---|:---|:---|
| Discoverable (발견 가능) | 카탈로그에서 검색·발견 가능 | Unity Catalog / DataHub 등록 |
| Addressable (주소 지정 가능) | 안정적인 URI/테이블명 | `catalog.schema.table` 영구 경로 |
| Trustworthy (신뢰 가능) | 품질 SLA 준수 이력 | DLT Expectations + 모니터링 |
| Self-Describing (자기 기술) | 스키마·리니지·문서 내장 | 카탈로그 메타데이터, README |
| Interoperable (상호 운용 가능) | 다양한 엔진에서 읽기 가능 | 오픈 포맷 (Parquet/Iceberg) |

> 📢 **섹션 요약 비유**: 좋은 데이터 제품은 좋은 레스토랑 메뉴와 같다. 요리 이름(주소), 재료(스키마), 맛 보장(SLA), 알레르기 정보(메타데이터), 다양한 언어 지원(상호 운용성)이 모두 갖춰진 메뉴다.

---

## Ⅲ. 비교 및 연결

<strong>데이터 계약 (Data Contract) 실제 구조</strong>
```yaml
# data_contract.yaml (OpenDataContract 표준)
id: sales.gold.daily_orders
version: 2.1.0
owner: sales-analytics-team
description: "일별 주문 집계 — 영업팀 BI 용도"

schema:
  fields:
    - name: order_date
      type: date
      required: true
    - name: total_amount
      type: decimal(18,2)
      required: true

sla:
  freshness: "09:00 KST 이전 갱신"
  availability: 99.5%
  completeness: "null_rate < 1%"

quality_checks:
  - check: null_check
    column: order_date
    threshold: 0
```

<strong>데이터 제품 성숙도 모델</strong>

| 수준 | 특징 | 예시 |
|:---|:---|:---|
| Level 1 (데이터셋) | 스키마·소유권만 있음 | 내부용 Silver 테이블 |
| Level 2 (제품) | SLA + 카탈로그 등록 | Gold 테이블 + 문서화 |
| Level 3 (플랫폼 제품) | API + 버전 + 변경 알림 | Delta Sharing + SemVer |
| Level 4 (비즈니스 제품) | 수익화 가능한 외부 공유 | 데이터 마켓플레이스 등록 |

> 📢 **섹션 요약 비유**: 데이터 제품 성숙도는 스타트업의 성장 단계와 같다. 아이디어(Level 1) -> MVP(Level 2) -> 안정적 서비스(Level 3) -> 수익화(Level 4)로 발전한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>데이터 계약 도입 체크리스트</strong>
- [ ] 주요 Gold 테이블에 소유팀·SLA 명시
- [ ] 스키마 변경 시 소비자 팀에 사전 공지 프로세스
- [ ] 품질 모니터링 대시보드 (신선도·완전성·정확성)
- [ ] 브레이킹 체인지 시 버전 업 (v2.0.0) + 이전 버전 지원 기간 설정
- [ ] 카탈로그(Unity Catalog / DataHub)에 메타데이터 등록

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 데이터 제품 정의 | 인터페이스·SLA·소유권·품질 계약을 갖춘 독립 데이터 단위 |
| 데이터 계약 필요성 | 파이프라인 브레이킹 체인지 사전 방지, 소비자 신뢰 구축 |
| SLA 주요 지표 | 신선도(freshness), 가용성(availability), 완전성(completeness), 정확성(accuracy) |
| 5대 특성 | Discoverable, Addressable, Trustworthy, Self-Describing, Interoperable |

> 📢 **섹션 요약 비유**: 데이터 계약은 임대 계약서와 같다. 임대인(생산자)과 임차인(소비자)이 무엇을 제공하고 무엇을 기대하는지 명시하여, 나중에 분쟁이 생겨도 계약서가 기준이 된다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 신뢰성 향상 | SLA 준수 이력 공개로 소비자 신뢰 구축 |
| 파이프라인 안정성 | 계약 기반 변경 관리로 브레이킹 체인지 사전 차단 |
| 데이터 발견성 | 카탈로그 등록으로 중복 데이터 생성 방지 |
| 책임 명확화 | 소유팀 명시로 데이터 품질 책임 소재 확보 |

데이터 제품과 데이터 계약은 데이터 메시 시대의 핵심 운영 패러다임이다. 기술적으로는 OpenDataContract, DataHub, Unity Catalog가 구현 도구를 제공하고 있으며, 2024년 이후 데이터 거버넌스 성숙 조직에서 빠르게 도입되고 있다. 심화 학습에서는 **5대 특성**, <strong>데이터 계약 구성 요소</strong>, <strong>SLA 지표 유형</strong>이 핵심 논점이다.

> 📢 **섹션 요약 비유**: 데이터 제품은 제조물 책임법이 적용되는 제품이다. 결함(품질 위반)이 발생하면 제조사(소유 팀)가 책임지고, 리콜(파이프라인 수정) 후 소비자에게 통보해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Data Contract | 핵심 메커니즘 | 생산자-소비자 간 스키마·SLA 계약 |
| SLA 지표 | 품질 기준 | 신선도·가용성·완전성·정확성 |
| Discoverable | 5대 특성 | 카탈로그 등록·검색 가능 |
| Data Mesh | 상위 원칙 | 데이터 제품 = Data Mesh 원칙 2 |
| Unity Catalog | 등록 인프라 | 데이터 제품 메타데이터 관리 |
| OpenDataContract | 표준 | 데이터 계약 YAML 스펙 표준 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 레이크 (Data Lake) — 원시 데이터 저장]
    |
    v
[데이터 메시 (Data Mesh) — 도메인 소유권]
    |
    v
[데이터 제품 (Data Product) — 소비 가능 단위]
    |
    v
[데이터 계약 (Data Contract) — SLA 보장]
    |
    v
[데이터 마켓플레이스 (Data Marketplace) — 내부 거래]
```

이 흐름은 원시 데이터를 모으는 레이크에서 출발해 도메인 소유권을 가진 메시로 분산되고, 소비 가능한 데이터 제품과 계약을 거쳐 마켓플레이스로 거래되는 흐름을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 제품은 마트 진열대에 있는 상품이에요. 가격표(SLA), 영양 성분(스키마), 제조사(소유 팀)가 모두 붙어 있어요.
2. 데이터 계약은 상품을 팔 때 쓰는 계약서예요. 상품 내용이 바뀌면 구매자에게 미리 알려줘야 해요.
3. 좋은 데이터 제품은 쉽게 찾고, 믿을 수 있고, 어떤 레시피(엔진)에도 쓸 수 있어야 해요.
