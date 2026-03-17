+++
title = "277-280. 아키텍처 품질 속성과 시나리오"
date = "2026-03-14"
[extra]
category = "System Quality"
id = 277
+++

# 277-280. 아키텍처 품질 속성과 시나리오

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아키텍처의 본질은 기능(Function)을 만족하는 것이 아니라, 비기능적 요구사항인 **품질 속성(Quality Attributes, 이하 QA)**을 최적화하는 구조적 결정을 내리는 것에 있다.
> 2. **가치**: 모호한 QA 요구사항을 **S.S.E.A.R.M (Source, Stimulus, Environment, Artifact, Response, Measure)** 6요소로 구조화된 **품질 시나리오(Quality Scenario)**로 변환함으로써, 시스템의 성공 여부를 정량적(Quantitative)으로 검증 가능하게 한다.
> 3. **융합**: 이러한 시나리오 기반 설계는 **SA (Software Architecture)** 평가 및 **CI/CD (Continuous Integration/Continuous Deployment)** 파이프라인 내의 **NFT (Non-Functional Testing)** 자동화와 직결되는 핵심 토대이다.

---

### Ⅰ. 개요 (Context & Background) - 아키텍처 품질의 본질

소프트웨어 아키텍처(Software Architecture)에서 가장 치명적인 실수는 "모든 것을 최적화하려는 시도"이다. 자원은 한정되어 있으며, 성능(Performance)을 높이면 보안(Security)이나 변경 용이(Modifiability)가 희생되는 **Trade-off (상충 관계)**가 발생하기 때문이다. 따라서 기술자는 비즈니스의 목표에 부합하는 특정 품질 속성을 식별하고, 이를 수학적으로 정의하여 구조에 반영해야 한다.

#### 아키텍처 품질 속성의 분류
품질 속성은 관점에 따라 크게 세 가지 계층으로 분류된다.

1.  **시스템 품질 속성 (System QA)**: 최종 사용자 및 개발자가 직접 경험하는 외부 품질.
    *   **성능 (Performance)**: 반응 시간(Response Time), 처리량(Throughput), 자원 사용률.
    *   **가용성 (Availability)**: 시스템이 정상 가동되는 시간 비율 (예: 99.99%).
    *   **보안성 (Security)**: 기밀성(Confidentiality), 무결성(Integrity), 가용성 보장.
    *   **변경 용이성 (Modifiability)**: 버그 수정이나 기능 추가 시 드는 비용과 위험도.
2.  **비즈니스 품질 속성 (Business QA)**: 이해관계자(Stakeholder)에게 중요한 시장/비용적 가치.
    *   **시장 적시성 (Time to Market)**: 얼마나 빨리 출시할 수 있는가.
    *   **비용 및 수익 (Cost and Benefit)**: 개발비, 라이선스 비용, **TCO (Total Cost of Ownership)**.
    *   **시스템 수명 (Lifetime)**: 기술적 부채 없이 유지보수 가능한 기간.
3.  **아키텍처 품질 속성 (Architecture QA)**: 구조적 건전성을 위한 내부 품질.
    *   **개념적 무결성 (Conceptual Integrity)**: 설계의 일관성과 논리적 완결성.
    *   **정확성과 완결성 (Correctness & Completeness)**: 요구사항을 충실히 구현했는가.

> **💡 비유: 스마트폰의 스펙**
> *   **기능(Functional)**: 전화를 걸고, 사진을 찍을 수 있다. (당연한 것)
> *   **품질(Quality)**: 사진을 찍는데 0.1초가 걸리느냐(성능), 떨어뜨려도 깨지지 않느냐(내구성/신뢰성), 배터리가 하루 종일 지속되느냐(효율성)가 경쟁력이다.

#### 📢 섹션 요약 비유
아키텍처 품질 속성 정의는 마치 **초고층 빌딩을 짓기 위해 내진 설계(안전성)와 조망권(사용성) 중 어디에 집중할지 결정하는 '건축 기본 계획'**과 같습니다. 모든 품질을 완벽하게 만족할 수는 없으므로, 그 건물의 목적(상업용인지 주거용인지)에 따라 가장 중요한 품질 하나를 선택해야 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - 품질 시나리오(S.S.E.A.R.M)

단순히 "빠른 응답"이라는 요구사항은 아키텍처 설계 가이드가 될 수 없다. "빠름"의 기준이 사람마다 다르기 때문이다. 이를 해결하기 위해 **SEI (Software Engineering Institute)**의 **ATAM (Architecture Tradeoff Analysis Method)**에서 제안한 것이 바로 **품질 시나리오(Quality Scenario)**이다. 이는 품질 속성을 측정 가능한 단위로 세분화한 것이다.

#### 1. 품질 시나리오의 구성 요소 (S.S.E.A.R.M)
품질 시나리오는 6가지 요소로 구성된 서술형 스토리이다.

| 요소 | 명칭 | 설명 | 예시 (Performance) | 예시 (Security) |
|:---:|:---|:---|:---|:---|
| **S** | **Source of Stimulus** (자극원) | 이벤트를 발생시키는 주체 (사용자, HW, 타 시스템) | 최종 사용자 (End User) | 해커 (Hacker) |
| **S** | **Stimulus** (자극) | 시스템에 가해지는 조건이나 이벤트 | 페이지 요청 (Request) | **SQL Injection** 공격 |
| **E** | **Environment** (환경) | 자극이 발생할 때의 시스템 상태 | 일반 운영 모드, 1,000명 동시 접속 | 방화벽 외부, 네트워크 혼잡 |
| **A** | **Artifact** (대상) | 자극을 받는 시스템의 일부 | 웹 서버 (Web Server) | **WAF** (Web App Firewall) |
| **R** | **Response** (응답) | 자극에 대한 시스템의 반응 | 데이터를 반환 | 접속 차단 및 관리자 알림 |
| **M** | **Response Measure** (응답 척도) | 응답의 정량적/정성적 측정 기준 | 2초 이내 응답 | 1초 이내 탐지 및 로깅 |

#### 2. 품질 시나리오 상세 ASCII 다이어그램

아래 다이어그램은 "가용성(Availability)"을 보장하기 위한 장애 조치(Failover) 시나리오를 시각화한 것이다.

```ascii
+-----------------------------------------------------------------------------+
|                    [Quality Scenario: High Availability]                   |
+-----------------------------------------------------------------------------+

   [ Source ]           [ Stimulus ]       [ Environment ]      [ Artifact ]
    
    사용자                    │                   │                   │
  (Users)          "장애 발생!"           "정상 트래픽"           "DB 주 서버"
                              │               (Runtime)          (Primary DB)
                              ▼                   │                   │
                        ┌─────────┐                │                   │
                        │ Load    │                │            (Crash) │
                        │ Balancer│                │                  (X)
                        └─────────┘                │                   │
                              │                   ▼                   ▼
                        감지 및 전송           ┌──────────────────────────┐
                              │           ───▶│   HA (High Availability)│
                              │           │   │     Cluster Manager     │
                              ▼           │   └──────────────────────────┘
   [ Response ]         ┌─────────┐    │                 │
    "서비스 중단 없음"  │Standby DB│◀───┘          [Auto Switch]
      (Seamless)       │ (Standby)│                     │
                        └─────────┘                     ▼
                                         [ Response Measure ]
                                         "장애 감지 후 3초(RTO) 이내에
                                          대기 서버로 전환 및
                                          데이터 0 손실(RPO=0)"
```

**해설**:
1.  **Source/Stimulus**: 사용자가 서비스를 이용 중인 환경(Environment)에서 **DB 주 서버(Artifact)**에 전원 장애(Stimulus)가 발생합니다.
2.  **Response**: **HA Cluster**와 같은 아키텍처 패턴이 이를 감지하고, **Standby DB(대기 서버)**로 트래픽을 자동 전환합니다.
3.  **Measure**: 사용자 입장에서는 서비스 중단을 인지하지 못하며(Seamless), **RTO (Recovery Time Objective)** 3초, **RPO (Recovery Point Objective)** 0을 만족해야 합니다.

#### 3. 품질 속성별 전술(Tactics) 구현 (코드 및 로직)
아키텍처는 이러한 시나리오를 만족시키기 위해 구체적인 '전술(Tactics)'을 배치한다.

*   **성능 최적화 (Performance)**:
    *   **Resource Management**: 자원 풀링(Pooling), **QoS (Quality of Service)** 우선순위 큐 적용.
    *   **Code Optimization**: 불필요한 연산 제거, 알고리즘 효율화($O(n^2) \rightarrow O(n \log n)$).
*   **변경 용이성 (Modifiability)**:
    *   **Cohesion/ Coupling**: 모듈 갯의 결합도(Coupling)는 낮추고, 모듈 내의 응집도(Cohesion)는 높인다.
    *   **Interface Segregation**: 추상화(Abstraction) 계층을 두어 구현체 변경 영향을 격리한다.
    *   **Polymorphism**: 다형성을 활용하여 실행 시점(Runtime)에 객체를 교체한다.

```python
# 예시: 변경 용이성을 위한 Dependency Injection (의존성 주입) 패턴
# 대상(Artifact)이 변경되더라도 클라이언트 코드 수정을 최소화하는 전술

from abc import ABC, abstractmethod

# 1. Abstraction (추상화): 인터페이스 정의
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount):
        pass

# 2. Concrete Component (구현체 A)
class CardPayment(PaymentProcessor):
    def process(self, amount):
        return f"Processing {amount} via Card"

# 3. Concrete Component (구현체 B - 변경되는 부분)
class CryptoPayment(PaymentProcessor):
    def process(self, amount):
        return f"Processing {amount} via Crypto"

# 4. Context (아키텍처 전술 적용부)
class PaymentService:
    def __init__(self, processor: PaymentProcessor): # 의존성 주입
        self._processor = processor

    def execute(self, amount):
        # 자극(Stimulus)에 대한 응답(Response) 로직
        return self._processor.process(amount)

# 결과: '모듈' 교체가 용이해짐 (Modification Scenario 만족)
```

#### 📢 섹션 요약 비유
품질 시나리오와 전술은 **'자동차 사고 시뮬레이션 테스트'**와 같습니다. 엔지니어는 단순히 "안전한 차"라고 말하는 대신, "시속 60km로 전면 충돌 시(Stimulus), 에어백이 전개되어(Response) 승객의 중상 방지(Measure)"라는 구체적인 스크립트를 작성하고, 이를 위해 섀시를 보강하는 등(Tactic) 설계에 반영합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

품질 속성들은 독립적이지 않으며, 하나의 아키텍처 결정이 다른 속성에 미치는 영향(Trade-off)을 면밀히 분석해야 한다.

#### 1. 상충 관계 (Trade-off) 분석 매트릭스

| 비교 대상 A | 비교 대상 B | 관계 (Synergy vs Trade-off) | 상세 분석 |
|:---|:---|:---:|:---|
| **Security** | **Usability** | ⚠️ 상충 | 보안을 강화하기 위해 **2FA (2-Factor Authentication)**를 도입하면, 로그인 절차가 복잡해져 사용성(Usability)이 저하됨. |
| **Performance** | **Security** | ⚠️ 상충 | **TLS/SSL (Transport Layer Security)** 암호화 통신은 CPU 오버헤드를 유발하여 순수 처리량(Throughput)을 감소시킴. |
| **Modifiability** | **Performance** | ⚠️ 상충 | 변경 용이성을 위해 **Facade** 패턴이나 **Microservices**로 쪼개면, 네트워크 호출이 늘어나 **Latency**가 증가할 수 있음. |
| **Availability** | **Security** | ⚠️ 상충 | **DoS (Denial of Service)** 공격 방지를 위해 의심스러운 요청을 모두 차단하면, 정상 사용자의 서비스 접근 가능성(Availability)이 차단됨. |
| **Testability** | **Modifiability** | ✅ 상승 | 테스트 용이성을 높이기 위해 인터페이스를 잘 분리해두면, 결과적으로 변경 용이성도 함께 높아지는 시너지 효과. |

#### 2. 타 영역(Subject) 융합 분석

**A. SW 엔지니어링 (SE) & 네트워크 (Network): latency vs Throughput**
*   **SE 관점**: 사용자 경험(UX)을 위해 **Latency (지연 시간)** 최소화가 중요. 단건 요청 속도가 빨라야 애플리케이셩 반응성이 좋음.
*   **Network 관점**: 대량의 데이터 전송 효율성을 위해 **Throughput (처리량)** 최적화가 중요. 파이프라이닝(Pipelining)이나 배치(Batch) 처리를 선호함.
*   **아키텍처 의사결정**: **CDN (Content Delivery Network)** 도입은 정적 리소스의 Latency를 줄이는 동시에 Origin 서버의 부하를 줄여 전체 Throughput을 증대시키는 융합 솔루션.

**B. 보안 (Security) & 운영체제 (OS): 보안 전술과 커널 오버헤드**
*   **Security**: **ASLR (Address Space Layout Randomization)** 같은 기법을 통해 버퍼 오버플로우 공격을 방지.
*   **OS**: 메모리 주소를 무작위화하는 과정은 OS의 **MMU (Memory Management Unit)** 자원을 소모하여 컨텍스트 스위칭(Context Switching) 비용을 증가시킴.
*   **Analogy**: 보안 검색대를 통과하는 공항. 검색을 강화하면(Security 강화), 대기 시간이 길어져 비행기 출발 늦어질 수 있음(Performance 저하).

#### 📢 섹션 요약 비유
품질