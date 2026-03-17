+++
title = "668. 비기능 요구사항 아키텍처 드라이버"
date = "2026-03-15"
weight = 668
+++

# 668. 비기능 요구사항 아키텍처 드라이버

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템이 '무엇(What)'을 하는지가 아닌, '어떻게(How)' 동작해야 하는지를 규정하는 성능, 보안, 가용성 등의 **품질 속성(Quality Attributes)**으로, 소프트웨어 아키텍처의 구조를 결정짓는 가장 강력한 힘이다.
> 2. **메커니즘**: 아키텍처 드라이버(Architecture Drivers)는 핵심 기능, 품질 속성, 비즈니스 제약, 기술적 제약의 4가지 요소로 구성되며, 이들은 서로 상충(Trade-off)하면서 설계 의사결정 트리의 뿌리가 된다.
> 3. **실무 가치**: 모호한 요구사항을 정량화된 **QA (Quality Attribute) 시나리오**로 변환하여, 개발 초기에 '구조적 위험'을 식별하고 기술 스택 선정의 명확한 근거(Rationale)를 제공한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
비기능 요구사항(Non-Functional Requirements, NFRs)은 시스템의 기능적 행위와는 별개로 시스템이 갖추어야 할 품질 수준이나 제약 조건을 정의한다. 단순히 "빠르게 처리되어야 한다"는 식의 모호한 요구사항을 넘어, 소프트웨어 아키텍처 설계 과정에서 **"어떤 구조를 선택해야 하는가"**를 강제하는 결정적 요인, 즉 **아키텍처 드라이버(Architecture Driver)**로 작용해야 한다.

### 2. 등장 배경: SW 난이도의 변천
과거의 단순한 **MIS (Management Information System)** 시대에는 기능이 곧 아키텍처였으나, 대규모 트래픽 처리가 필요한 현재의 **Distributed System (분산 시스템)** 환경에서는 '기능'보다 '성능', '확장성', '가용성'이 시스템의 성패를 가른다. 이에 따라 기능 요구사항을 충족시키는 것은 기본이고, 비기능 요구사항을 만족시키기 위한 구조적 설계가 핵심 과제로 대두되었다.

### 3. ASCII: 소프트웨어 성장과 아키텍처 복잡도
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    소프트웨어 진화에 따른 관심사의 변화                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Phase 1: Standalone]          [Phase 2: Client/Server]   [Phase 3: Cloud]│
│                                                                             │
│  Focus: Feature (기능)         Focus: Logic (비즈니스)   Focus: NFR (품질) │
│                                                                             │
│  [ 모놀리식 구조 ]              [ 3-Tier 구조 ]           [ MSA / Event-Driven]│
│                                                                             │
│  "데이터 저장되나요?"           "동시 접속 되나요?"         "초간 트랜잭션 얼마?" │
│  "버그 없나요?"                 "보안 되나요?"              "서버 죽어도 서비스 되?"│
│                                                                             │
│  ▲ 아키텍처 단순함             ▲ 구조적 고민 시작          ▲ 비기능 요구사항이   │
│                             (Middle Tier)            아키텍처 드라이버화    │
└─────────────────────────────────────────────────────────────────────────────┘
```
**해설**:
소프트웨어가 단순한 데이터 처리 도구에서 대규모 분산 시스템으로 진화함에 따라, '기능'의 구현보다 '품질(성능, 가용성 등)'의 보장이 훨씬 어려운 문제가 되었다. 따라서 현대의 아키텍처 설계는 이 비기능 요구사항(NFR)을 만족하기 위해 어떤 패턴과 기술을 조합할지를 결정하는 과정이 되었다.

### 📢 섹션 요약 비유
> 마치 건물을 지을 때, '방의 개수(기능)'는 내부 인테리어로 조정 가능하지만, '내진 설계(비기능)'는 기둥의 위치와 재질을 결정하는 것처럼, 비기능 요구사항은 시스템의 뼈대를 결정짓는 설계도의 근간이 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 아키텍처 드라이버의 4대 구성 요소 (상세)

아키텍처 드라이버는 단순한 희망사항 목록이 아니라, 설계를 강제하는 입력값이다. 이는 크게 4가지 세부 요소로 분류된다.

| 구성 요소 | 역할 | 상세 내부 동작 예시 | 비유 (자동차) |
|:---:|:---|:---|:---|
| **기능 요구사항**<br>(Functional Req) | 시스템의 존재 목적 | - 결제 처리<br>- 주문 생성<br>- 회원가입 로직 | 5명이 탈 수 있는 좌석 |
| **품질 속성**<br>(Quality Attributes) | **가장 강력한 드라이버**<br>구조를 결정함 | - **Latency (지연 시간)**: P99 < 200ms<br>- **Availability (가용성)**: 99.99%<br>- **Security (보안)**: 데이터 암호화 | 최고 시속 300km<br>충돌 시 안전성 |
| **비즈니스 제약**<br>(Business Constraints) | 예산, 일정, 인력 등의 현실적 제약 | - 예산: $1M 이내<br>- 마감: 3개월 후 출시<br>- 인력: Java 전문가만 존재 | 차값 1억 원 이내<br>내년 1월까지 인도 |
| **기술적 제약**<br>(Technical Constraints) | 사용 기술 스택, 표준, 레거시 | - **Compliance**: PCI-DSS 준수<br>- **Legacy**: 기존 DB 사용 필수<br>- **Standard**: RESTful API 사용 | 반드시 전기 모터 사용<br>규제 충족 |

### 2. 핵심 메커니즘: 품질 속성 시나리오 (Quality Attribute Scenario)

비기능 요구사항을 실무 설계에 적용하기 위해서는 모호한 요구를 구조적인 **QA 시나리오**로 변환해야 한다. 이는 6가지 요소로 구성된다.

```text
   [Source of Stimulus] ──(Stimulus)──▶ [Environment]
            │                        │
            ▼                        ▼
        [Artifact] ◀──(Response)── [Response Measure]
        
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                    EXAMPLE: Availability Scenario                      │
   ├─────────────────────────────────────────────────────────────────────────┤
   │  Source: Anonymous User (익명 사용자)                                    │
   │  Stimulus: DDoS Attack (DDoS 공격 발생)                                  │
   │  Artifact: API Gateway (시스템 진입점)                                    │
   │  Environment: Normal Operation (정상 운영 상태)                          │
   │  Response: Throttle traffic > 503 Error (트래픽 조절 및 에러 응답)        │
   │  Measure: Degraded Performance < 5%, System Not Crash (시스템存活)      │
   └─────────────────────────────────────────────────────────────────────────┘
```
**해설**:
이 시나리오는 단순히 "DDoS에 강해야 한다"는 말을, "공격 발생 시(Stimulus) 시스템이 죽지 않고 503 에러를 주며 트래픽을 조절(Response)하는 아키텍처가 필요하다"는 **설계 요구사항**으로 바꾼다. 이는 곧 **Rate Limiter**나 **Circuit Breaker** 패턴 도입의 근거가 된다.

### 3. 드라이버 기반 설계 의사결정 흐름
아키텍처는 드라이버를 입력으로 받아 최적의 패턴(Pattern)을 선택하는 과정이다.

```text
      INPUT: DRIVERS                 DECISION LOGIC              OUTPUT: STRUCTURE
  ┌──────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────┐
  │ • High Throughput    │    │  •  Queueing Pattern     │    │  •  Kafka Cluster    │
  │ • Low Latency        │──▶ │  •  Caching Strategy    │──▶ │  │  •  Redis Cluster   │
  │ • Strong Consistency │    │  •  Sharding Scheme     │    │  •  Database Sharding│
  └──────────────────────┘    └──────────────────────────┘    └──────────────────────┘
           │                            ▲                            │
           │         ┌──────────────────┴──────────────────┐          │
           │         │   TRADE-OFF ANALYSIS (CRITICAL)     │          │
           └────────▶│   "Consistency vs Availability"     │──────────┘
                    │   (CAP Theorem Application)          │
                    └───────────────────────────────────────┘
```
**해설**:
이 흐름도에서 가장 중요한 점은 **'결정 논리(Decision Logic)'** 단계다. 예를 들어 'High Throughput'과 'Strong Consistency'라는 두 개의 상충하는 드라이버가 들어오면, 아키텍트는 **CAP Theorem (CAP 정리)**에 근거하여 일관성을 포기할지(Priority on Availability) 아니면 성능을 포기할지(Priority on Consistency) 판단해야 한다. 이것이 기술사적 판단의 핵심이다.

### 📢 섹션 요약 비유
> 마치 고속도로를 건설할 때, 단순히 '차가 다니는 곳'이 아니라 '시속 100km로 1만 대가 동시에 달려야(성능) 하는 곳'이라는 요건에 따라 차선 수, 톨게이트 위치, 진입로 구조를 설계하는 것과 같습니다. 요건이 구체적일수록 설계는 명확해집니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기능 요구사항 vs 비기능 요구사항 (정량적 비교)

두 요구사항의 차이는 명확히 구분되어야 하며, 특히 아키텍처에 미치는 영향력은 비기능 요구사항이 훨씬 크다.

| 구분 | 기능 요구사항 (Functional) | 비기능 요구사항 (Non-Functional) |
|:---|:---|:---|
| **핵심 질문** | What (시스템이 무엇을 하는가?) | How (시스템이 어떻게 수행하는가?) |
| **설계 영향도** | **Low**: 모듈 내부 로직(Class, Function)에 영향 | **High**: 시스템 전체 구조(Component, Topology)에 영향 |
| **변경 비용** | 상대적으로 낮음 (모듈 단위 수정) | 매우 높음 (아키텍처 재설계 필요) |
| **테스트 방법** | Functional Testing (Unit, Integration) | NFR Testing (Load, Stress, Penetration) |
| **실무 예시** | '장바구니 담기' 버튼 구현 | '장바구니 담기' 응답 속도 < 100ms 보장 |

### 2. 타 과목 융합 분석: CAP Theorem & Cloud Computing

비기능 요구사항인 '일관성(Consistency)'과 '가용성(Availability)'은 분산 시스템의 핵심 이론인 **CAP Theorem (CAP 정리)**와 직접 연결된다.

```text
   [Requirements]                 [Distributed Theory]          [Tech Stack]
                 ↘                            ↘                    ↘
  "Must Handle      +          CAP Theorem Choice       →    CP System (RDBMS)
   Split Brain"                  (Consistency vs              └ HBase
    Availability)                   Availability)
           │                            │                    AP System (Cassandra)
           ▼                            ▼                    └ DynamoDB
   [Architecture Driver]
   분산 환경에서의 데이터
   무결성/가용성 정책 선택
```
**해설**:
만약 비즈니스 요구사항이 "재고 관리이므로 절대 과 판매가 나면 안 된다"라면 **CP(Consistency/Partition Tolerance)** 유형의 아키텍처(MySQL Cluster)를 선택해야 한다. 반면 "SNS 댓글이 조금 늦게 보여도 되고, 서버가 죽어도 글은 써져야 한다"라면 **AP(Availability/Partition Tolerance)** 유형(Cassandra, DynamoDB)을 선택한다. 즉, 비기능 요구사항이 곧 기술 스택 선택의 좌표가 된다.

### 📢 섹션 요약 비유
> 집을 지을 때 '화장실이 몇 개냐(기능)'는 방 배치만 바꾸면 되지만, '지진이 나도 무너지지 않아야 한다(비기능)'는 요건은 벽돌 재료, 기둥 배치, 심지어 부지 선택까지 모두 바꾸는 것과 같습니다. 비기능 요구사항은 공사의 난이도와 예산을 결정하는 '메이저 키'입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 초대규모 커머스 플랫폼 아키텍처

**상황**: 글로벌 전자상거래 시스템 재설계.
**아키텍처 드라이버 도출**:
1.  **Performance**: 5만 TPS (Transactions Per Second) 처리.
2.  **Availability**: 연간 중단 시간 5분 이내 (99.999%).
3.  **Security**: PCI-DSS 준수 및 개인정보 암호화.

**의사결정 매트릭스 (Decision Matrix)**:
| 후보 아키텍처 | 성능 (TPS) | 가용성 구현 난이도 | 보안 구현 비용 | **종합 의사결정** |
|:---|:---:|:---:|:---:|:---|
| **Monolithic (Legacy)** | ❌ 1만 미만 | ✅ Low | ✅ Low | **Drop**<br>성능 드라이버 불만족 |
| **Microservices + Sync API** | ⚠️ 2~3만 (Latency 누적) | ⚠️ Medium | ⚠️ Medium | **Drop**<br>네트워크 병목 위험 |
| **MSA + Event-Driven (Async)** | ✅ 5만+ | ⚠️ High (복잡함) | ⚠️ High | **Select**<br>드라이버 충족 가능 |

**최종 전략**:
성능 드라이버(5만 TPS)를 충족하기 위해 동기식 호출을 지양하고 **Event-Driven Architecture (EDA)**를 도입한다. 단, 비동기 처리로 인한 데이터 일