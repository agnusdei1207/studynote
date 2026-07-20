---
title: "Read-Write Lock Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 209
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Read-Write Lock (읽기-쓰기 락) 패턴은 여러 스레드의 동시 읽기(공유 락, Shared Lock)는 허용하고, 쓰기 시에만 단독 접근(배타 락, Exclusive Lock)을 보장하여 읽기 성능과 쓰기 일관성을 동시에 달성한다.
> 2. **가치**: 전통적인 `synchronized`(모든 접근 직렬화)는 읽기만 해도 차단되는 비효율이 있다. Read-Write Lock은 읽기가 빈번한 시나리오에서 처리량(Throughput)을 극적으로 향상시킨다.
> 3. **판단 포인트**: 읽기/쓰기 비율이 10:1 이상처럼 읽기 빈번하고 쓰기 드문 경우에 적합하다. 쓰기가 빈번하면 오버헤드로 오히려 역효과다.

---

## Ⅰ. 개요 및 필요성
```
  synchronized 블록 (모든 접근 직렬화):

  Thread A (읽기) -+
  Thread B (읽기) -+-- 모두 순차 실행 (읽기끼리도 차단)
  Thread C (쓰기) -+

  -> 읽기끼리는 서로를 차단할 이유가 없음!
    캐시 조회, 설정 읽기 등 읽기 집중 작업에서 심각한 성능 저하
```

| 접근 유형 | 동시 읽기 스레드 존재 시 | 쓰기 스레드 존재 시 |
|:---|:---|:---|
| 새 읽기 시도 | ✅ 허용 (Shared Lock 공유) | ❌ 차단 |
| 새 쓰기 시도 | ❌ 차단 | ❌ 차단 |

```
  Read-Write Lock 접근 규칙:

  상황 1: 읽기만 있을 때
  Thread A (읽기) -------------------
  Thread B (읽기) -------------------  <- 동시 실행 가능
  Thread C (읽기) -------------------

  상황 2: 쓰기 시도
  Thread A (읽기) -----+
  Thread B (읽기) -----+ 쓰기 대기
  Thread D (쓰기) -----+-----------   <- 단독 실행
  Thread E (읽기)          ---------  <- 쓰기 완료 후 실행
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 도서관 열람실 — 책을 읽는 사람은 여럿이어도 괜찮지만, 누군가 책을 수정(쓰기)할 때는 다른 사람이 읽거나 쓸 수 없게 책을 잠근다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  ReentrantReadWriteLock
  +--------------------------------------------------+
  |  ReadLock (공유 락)                              |
  |  -----------------                               |
  |  lock()   -> 읽기 락 획득 (다른 읽기와 공유 가능) |
  |  unlock() -> 읽기 락 해제                         |
  |                                                  |
  |  WriteLock (배타 락)                             |
  |  ------------------                              |
  |  lock()   -> 쓰기 락 획득 (모든 접근 차단)        |
  |  unlock() -> 쓰기 락 해제                         |
  +--------------------------------------------------+
```

```java
ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock readLock  = rwLock.readLock();
Lock writeLock = rwLock.writeLock();

// 읽기 (다수 동시 실행 가능)
public String getData(String key) {
    readLock.lock();
    try {
        return cache.get(key);
    } finally {
        readLock.unlock();
    }
}

// 쓰기 (단독 실행 보장)
public void setData(String key, String value) {
    writeLock.lock();
    try {
        cache.put(key, value);
    } finally {
        writeLock.unlock();
    }
}
```

Java 8에서 도입된 StampedLock은 <strong>낙관적 읽기(Optimistic Read Lock)</strong>를 추가:

```
  StampedLock 낙관적 읽기 흐름:

  (1) tryOptimisticRead() -> stamp 반환 (락 획득 없음!)
  (2) 데이터 읽기
  (3) validate(stamp) -> 쓰기가 없었으면 true
      -> true: 읽은 데이터 유효 -> 사용
      -> false: 충돌 발생 -> readLock으로 재시도

  일반 ReadLock 대비 성능 향상: 읽기가 매우 빈번하고
  쓰기 충돌이 거의 없을 때 극대화
```

```
  시나리오: 읽기 90%, 쓰기 10%, 스레드 10개

  synchronized:
  처리량 = 직렬화 -> ~1x 기준

  ReentrantReadWriteLock:
  처리량 = 읽기 9개 동시 -> ~4~6x 향상

  StampedLock (낙관적):
  처리량 = 락 없이 읽기 -> ~6~8x 향상

  ※ 쓰기가 50% 이상이면 오히려 오버헤드 발생
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 고속도로 하이패스 — 요금을 내는 차(쓰기)는 게이트가 닫히지만, 잠깐 표지판만 보는 차(읽기)는 그냥 통과해도 된다.

---

## Ⅲ. 비교 및 연결
| 락 종류 | 동시 읽기 | 동시 쓰기 | 읽기-쓰기 동시 | 구현 |
|:---|:---|:---|:---|:---|
| **synchronized** | ❌ | ❌ | ❌ | Java 내장 |
| **ReentrantLock** | ❌ | ❌ | ❌ | java.util.concurrent |
| **ReadWriteLock** | ✅ | ❌ | ❌ | ReentrantReadWriteLock |
| **StampedLock** | ✅ (낙관적) | ❌ | ❌ | Java 8+ |
| <strong>Semaphore(n)</strong> | n개까지 | 설정에 따라 | 설정에 따라 | java.util.concurrent |

```
  ReadWriteLock의 쓰기 기아 문제:

  Thread A (읽기) --------------------------------►
  Thread B (읽기) --------------------------------►
  Thread C (읽기) --------------------------------►
  Thread D (쓰기) --- 대기 대기 대기 ... (기아!) ►

  해결: 공정성 정책 (Fairness Policy)
  new ReentrantReadWriteLock(true);  // fair=true
  -> 대기 순서대로 락 부여 (FIFO)
  -> 단, 성능 감소 (20~30% 오버헤드)
```

- **📢 섹션 요약 비유**: 버스 우선 신호 — 읽기(일반 차)는 많이 다닐 수 있지만, 쓰기(버스)도 너무 오래 기다리면 안 된다. 공정성 정책은 버스 전용 신호와 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 고성능 캐시 with ReadWriteLock
public class ReadHeavyCache<K, V> {
    private final Map<K, V> cache = new HashMap<>();
    private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

    public V get(K key) {
        lock.readLock().lock();       // 다수 동시 읽기 허용
        try { return cache.get(key); }
        finally { lock.readLock().unlock(); }
    }

    public void refresh(K key, V value) {
        lock.writeLock().lock();      // 쓰기 시 단독 점유
        try { cache.put(key, value); }
        finally { lock.writeLock().unlock(); }
    }
}
```

```
  ReadWriteLock 도입 판단:
  +------------------------------------------------+
  |  읽기 비율이 70% 이상인가?                     |
  |    YES -> ReadWriteLock 적합                    |
  |                                                |
  |  쓰기 지연이 허용되는가?                       |
  |    YES -> 공정성 정책 불필요                    |
  |    NO  -> fair=true 또는 StampedLock            |
  |                                                |
  |  동일 스레드에서 읽기->쓰기 락 업그레이드 필요? |
  |    YES -> StampedLock.tryConvertToWriteLock()   |
  +------------------------------------------------+
```

- <strong>Shared Lock(공유 락) vs Exclusive Lock(배타 락)</strong> 용어 명확히 구분
- <strong>쓰기 기아(Write Starvation)</strong>와 공정성(Fairness) 정책 언급
- 읽기/쓰기 비율에 따른 패턴 선택 기준 제시
- StampedLock의 낙관적 읽기(Optimistic Read) 고급 최적화 언급

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 공공 Wi-Fi — 여러 명이 인터넷을 함께 사용(읽기)할 수 있지만, 네트워크 설정을 변경(쓰기)할 때는 혼자만 접근해야 한다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| 읽기 처리량 대폭 향상 | 읽기 90% 시나리오에서 ~5x 성능 향상 |
| 쓰기 일관성 보장 | 쓰기 시 단독 접근으로 데이터 무결성 |
| 배압 없는 읽기 | 읽기 스레드 간 서로 차단하지 않음 |

- 읽기/쓰기 비율이 균등하면 오버헤드로 `synchronized`보다 느릴 수 있음
- 쓰기 기아(Starvation) 방지를 위한 공정성 정책 검토 필요
- 락 업그레이드(Read -> Write) 불가 -> 해제 후 재획득 필요

Read-Write Lock (읽기-쓰기 락) 패턴은 읽기 집중적인 시스템에서 동시성과 일관성을 모두 달성하는 핵심 기법이다. 캐시, 설정 관리, 조회 API 등에 광범위하게 적용된다. StampedLock을 활용한 낙관적 읽기는 그 진화형으로 더 높은 성능을 제공한다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 도서관 규칙 — "책을 빌려 읽는 것"은 동시에 여러 명이 가능하지만, "책 내용을 수정하는 것"은 한 번에 한 명만 가능한 것처럼, Read-Write Lock도 이 원칙을 코드로 구현한 것이다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 동시성 패턴 (Concurrency Pattern) | 병렬 처리 설계 패턴 그룹 |
| 연관 개념 | Shared Lock (공유 락) | 다수 읽기 허용 락 |
| 연관 개념 | Exclusive Lock (배타 락) | 단독 쓰기 보장 락 |
| 연관 개념 | ReentrantReadWriteLock | Java 표준 구현 |
| 연관 개념 | StampedLock | 낙관적 읽기 지원 고급 구현 |
| 연관 개념 | Starvation (기아) | Write Starvation 방지 필요 |

### 📈 관련 키워드 및 발전 흐름도
Mutex 보호 -> 읽기-쓰기 락 패턴 -> 락 세분화

### 👶 어린이를 위한 3줄 비유 설명
1. 그림책은 여러 친구가 동시에 볼 수 있어요 — 읽기 락은 공유해요!
2. 하지만 그림책에 낙서(쓰기)할 때는 다른 친구들이 잠깐 기다려야 해요.
3. 그래서 읽기-쓰기 락은 "함께 읽되, 쓸 때는 혼자만"이라는 규칙이에요!
