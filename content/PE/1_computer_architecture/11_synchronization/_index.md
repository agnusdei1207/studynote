+++
title = "11. 멀티코어 및 동기화 (Synchronization)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "여러 명의 요리사가 하나의 가스레인지를 같이 쓸 때, 서로 부딪히지 않게 '지금 내가 쓰고 있어!'라고 신호를 주고받는 규칙이에요. 순서를 잘 지켜야 맛있는 음식을 안전하게 만들 수 있답니다."
+++

# 11. 멀티코어 및 동기화 (Synchronization)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중 프로세서 환경에서 공유 자원에 대한 동시 접근을 제어하고 데이터의 일관성(Consistency)을 유지하는 메커니즘.
> 2. **가치**: 경쟁 상태(Race Condition) 방지 및 원자적 연산(Atomic Operation) 보장을 통한 병렬 컴퓨팅의 신뢰성 확보.
> 3. **융합**: 하드웨어 수준의 캐시 일관성 프로토콜(MESI)과 소프트웨어 수준의 동기화 프리미티브(Mutex, Semaphore)의 유기적 결합.

---

### Ⅰ. 개요 (Context & Background)
멀티코어 시대에 동기화는 선택이 아닌 필수다. 여러 코어가 동시에 같은 메모리 위치를 수정하려고 할 때 발생하는 데이터 오염을 막기 위해, 하드웨어는 강력한 메모리 배리어(Memory Barrier)와 일관성 유지 기능을 제공해야 한다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 동기화 기법
- **Atomic Operations**: Test-and-Set, Compare-and-Swap (CAS)
- **Cache Coherency**: MESI, MOESI (Snooping vs Directory-based)
- **Memory Consistency Models**: Sequential Consistency, TSO (Total Store Ordering)
- **Deadlock Avoidance**: 상호 배제, 점유 및 대기, 비선점, 환형 대기 조건 관리

#### 2. 캐시 일관성 프로토콜 (ASCII)
```text
    [ MESI State Transition ]
    
         (Local Read)          (Local Write)
    +-----------+        +-----------+        +-----------+
    | Invalid   | ------>| Exclusive | ------>| Modified  |
    +-----------+        +-----------+        +-----------+
          ^                    |                    |
          | (Remote Write)     | (Remote Read)      | (Remote Read)
          |                    v                    v
          +--------------+-----------+ <--------+-----------+
                         | Shared    |
                         +-----------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### Snooping vs Directory-based
| 항목 | Snooping (버스 감시) | Directory-based (디렉토리 방식) |
| :--- | :--- | :--- |
| **작동 원리** | 모든 코어가 버스 트래픽 감시 | 중앙 관리자가 상태 정보 기록 |
| **확장성** | 낮음 (버스 병목 발생) | 높음 (대규모 시스템 적합) |
| **복잡도** | 단순함 | 복잡함 |
| **적용** | 소규모 멀티코어 CPU | 서버급 멀티 프로세서, NUMA |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 과도한 동기화는 **Lock Contention**을 유발하여 병렬 처리 효율을 떨어뜨린다. 기술사는 Lock-free 알고리즘을 도입하거나, 데이터 구조를 분할하여 동기화 범위를 최소화하는 아키텍처적 결단을 내려야 한다.

---

### Ⅴ. 기대효과 및 결론
동기화는 분산 시스템과 클라우드 컴퓨팅의 정합성을 보장하는 핵심 기술이다. 향후 트랜잭셔널 메모리(Transactional Memory)와 같은 하드웨어 지원 동기화 기술이 보편화될 것으로 예상된다.
