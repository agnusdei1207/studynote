+++
title = "04. 병행성 및 동기화 (Concurrency & Sync)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-operating-system"
kids_analogy = "공용 화장실을 쓸 때 '문 잠금장치'와 같아요. 한 사람이 들어가면 문을 잠그고, 나올 때 열어주어야 다음 사람이 안전하게 쓸 수 있죠? 만약 잠금장치가 없다면 큰 사고가 날 거예요!"
+++

# 04. 병행성 및 동기화 (Concurrency & Sync)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 여러 프로세스나 스레드가 공유 자원에 동시에 접근할 때 데이터의 일관성을 유지하기 위한 제어 메커니즘.
> 2. **가치**: 임계 구역(Critical Section) 보호 및 상호 배제(Mutual Exclusion) 보장을 통한 경쟁 상태(Race Condition) 방지.
> 3. **융합**: 하드웨어적 지원(Test-and-Set)과 소프트웨어적 도구(Semaphore, Monitor)의 결합을 통한 정합성 확보.

---

### Ⅰ. 개요 (Context & Background)
병행성은 현대 OS의 축복이자 저주다. 성능을 위해 여러 작업을 동시에 실행하지만, 이들이 공유 변수를 동시에 수정하면 결과가 엉망이 되는 '비결정적(Non-deterministic)' 문제가 발생한다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 임계 구역 해결 3대 조건
- **Mutual Exclusion**: 한 번에 하나만 진입
- **Progress**: 진입 대기 중인 프로세스 중 하나는 반드시 진입
- **Bounded Waiting**: 무한정 기다리는 프로세스가 없어야 함

#### 2. 동기화 도구 (ASCII)
```text
    [ Semaphore Concept ]
    
    Wait(S): while(S <= 0); S--; (Entry Section)
    --------------------------------------------
    |      CRITICAL SECTION (Shared Data)      |
    --------------------------------------------
    Signal(S): S++; (Exit Section)
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 뮤텍스(Mutex) vs 세마포어(Semaphore)
| 항목 | 뮤텍스 (Mutex) | 세마포어 (Semaphore) |
| :--- | :--- | :--- |
| **목적** | 상호 배제 (Locking) | 자원 개수 관리 (Signaling) |
| **소유권** | 소유자가 직접 해제해야 함 | 누구나 해제 가능 |
| **개수** | 0 또는 1 (Binary) | 0 이상의 정수 (Counting) |
| **복잡도** | 단순함 | 비교적 복잡함 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **Priority Inversion(우선순위 역전)** 현상은 시스템 마비의 주범이다. 낮은 우선순위가 락을 쥐고 있어 높은 우선순위가 대기하는 상황을 해결하기 위해, 기술사는 우선순위 상속(Priority Inheritance) 프로토콜을 적용해야 한다.

---

### Ⅴ. 기대효과 및 결론
동기화는 분산 DB의 트랜잭션과 클라우드 환경의 자원 공유에서 더욱 정교하게 발전하고 있다. 향후 하드웨어가 직접 트랜잭션을 관리하는 HTM(Hardware Transactional Memory) 기술이 병목 현상을 획기적으로 줄일 것으로 기대된다.
