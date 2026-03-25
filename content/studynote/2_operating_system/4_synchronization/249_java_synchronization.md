+++
title = "249. 자바 동기화 (Java Synchronization)"
date = "2026-03-22"
[extra]
categories = ["studynote-operating-system"]
+++

# 자바 동기화 (Java Synchronization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Java는 언어 수준에서 `synchronized` 키워드로 모니터 기반 상호 배제를 제공하며, `wait()/notify()/notifyAll()`로 조건 변수 동기화를 지원하는 고수준 동기화 모델을 채택했다.
> 2. **가치**: `java.util.concurrent` 패키지 (JUC)는 ReentrantLock, ReadWriteLock, Semaphore, CountDownLatch 등 세마포어·모니터를 모두 추상화한 고성능 동기화 라이브러리를 제공한다.
> 3. **융합**: JVM (Java Virtual Machine)의 객체 헤더에 내장된 모니터 락(Biased→Lightweight→Heavyweight 락 승격)은 OS 뮤텍스와 연계되어 성능과 공정성을 동적으로 조정한다.

---

## Ⅰ. 개요 및 필요성

Java는 멀티스레드를 언어 설계의 핵심으로 채택한 최초의 주류 언어 중 하나다. `synchronized` 키워드 하나로 컴파일러가 자동으로 모니터 락 획득/해제 코드를 생성하여, 개발자가 세마포어 P/V 순서를 직접 관리하는 저수준 실수를 방지한다.

그러나 `synchronized`는 단순한 반면, 타임아웃·공정성·조건별 대기 등 고급 기능이 부족하다. Java 5부터 `java.util.concurrent` (JUC) 패키지가 도입되어 이 한계를 보완했다.

**💡 비유**: `synchronized`는 건물 정문의 보안 요원(진입 시 자동 체크), JUC는 정문 외에 비상구·VIP 입구·출입 시간 제한까지 갖춘 스마트 보안 시스템이다.

```text
┌──────────────────────────────────────────────────────────┐
│        Java 동기화 계층 구조                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [고수준]  java.util.concurrent (JUC)                    │
│           ReentrantLock, ReadWriteLock, Semaphore        │
│           CountDownLatch, CyclicBarrier, Phaser          │
│           ConcurrentHashMap, CopyOnWriteArrayList        │
│                          │                               │
│  [중간]    synchronized / wait / notify                  │
│           (모니터 기반 내장 동기화)                      │
│                          │                               │
│  [저수준]  Unsafe.compareAndSwap() (CAS 직접 접근)       │
│           volatile 키워드 (메모리 가시성)                │
│                          │                               │
│  [하드웨어] JVM → OS Mutex → CPU 원자적 명령어           │
└──────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: Java 동기화 계층은 모니터(기본 자물쇠)부터 정교한 전자 잠금 시스템(JUC)까지, 문제 복잡도에 맞춰 선택하는 도구 상자입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### synchronized 키워드와 모니터

```java
// 1. 메서드 동기화: this 객체를 락으로 사용
public synchronized void increment() {
    counter++;
}

// 2. 블록 동기화: 명시적 락 객체로 세밀한 제어
private final Object lock = new Object();

public void increment() {
    synchronized (lock) {   // lock 객체의 모니터 획득
        counter++;
    }                       // 모니터 자동 해제 (예외 발생 시에도)
}

// 3. 클래스 수준 동기화 (정적 메서드)
public static synchronized void staticMethod() {
    // ClassName.class 객체를 락으로 사용
}
```

### wait() / notify() 동기화 패턴

```java
// 생산자-소비자 패턴 (Bounded Buffer)
class BoundedBuffer {
    private List<Integer> buffer = new ArrayList<>();
    private final int N;

    public synchronized void produce(int item) throws InterruptedException {
        while (buffer.size() == N)
            wait();           // 버퍼 가득 → 모니터 반환 후 대기
        buffer.add(item);
        notifyAll();          // 소비자 깨우기
    }

    public synchronized int consume() throws InterruptedException {
        while (buffer.isEmpty())
            wait();           // 버퍼 비어 있음 → 대기
        int item = buffer.remove(0);
        notifyAll();          // 생산자 깨우기
        return item;
    }
}
```

```text
┌───────────────────────────────────────────────────────────────┐
│       Java wait/notify 모니터 상태 전이                       │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  [Entry Set]   ──lock 경쟁 성공──▶  [Owner Thread]            │
│  (lock 대기)                           │                      │
│      ▲                                 │ wait() 호출          │
│      │                                 ▼                      │
│  notify()/    ◀── signal ────    [Wait Set]                   │
│  notifyAll()                    (모니터 반환 후 조건 대기)    │
│      │                                 │                      │
│      └──────────────────────────────────┘                     │
│                                                               │
│  ⚠ 핵심 규칙:                                                 │
│  1. wait()는 반드시 synchronized 블록 안에서 호출             │
│  2. 깨어난 후 반드시 while 루프로 조건 재확인 (허위 기상)     │
│  3. notify()는 임의 스레드 1개만 깨움 → notifyAll() 권장      │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** wait()를 호출하면 스레드는 모니터(락)를 반환하고 Wait Set으로 이동한다. notify()/notifyAll()은 Wait Set의 스레드를 Entry Set으로 이동시키며, 다시 락 경쟁에 참여하게 한다. 이 때문에 깨어난 후에도 조건이 여전히 충족되지 않을 수 있으므로(다른 스레드가 먼저 처리) while 루프 재확인이 필수다. notify() 대신 notifyAll()을 쓰는 이유는 notify()가 임의의 스레드 1개만 깨우기 때문에, 잘못된 스레드가 깨어나도 아무 일도 못하고 다시 wait()하는 시나리오에서 무한 대기가 발생할 수 있기 때문이다.

### JUC ReentrantLock — synchronized의 고급 대안

```java
import java.util.concurrent.locks.*;

ReentrantLock lock = new ReentrantLock(true); // fair=true: 공정 모드
Condition notFull  = lock.newCondition();
Condition notEmpty = lock.newCondition();

void produce(int item) throws InterruptedException {
    lock.lock();
    try {
        while (buffer.size() == N)
            notFull.await();   // 특정 조건에서만 대기
        buffer.add(item);
        notEmpty.signal();     // 소비자 조건만 깨움 (효율적!)
    } finally {
        lock.unlock();         // 예외 시에도 반드시 해제
    }
}
```

synchronized vs ReentrantLock 비교:

```text
┌─────────────────────┬──────────────────┬─────────────────────────────────────┐
│ 기능                │ synchronized     │ ReentrantLock                       │
├─────────────────────┼──────────────────┼─────────────────────────────────────┤
│ 조건 변수 다중      │ 1개 (wait/notify)│ 여러 개 (Condition)                 │
│ 타임아웃 대기       │ 불가             │ tryLock(timeout)                    │
│ 공정성              │ 비공정           │ fair=true 옵션                      │
│ 락 상태 확인        │ 불가             │ isLocked(), isHeldByCurrentThread() │
│ 인터럽트 가능 대기  │ 불가             │ lockInterruptibly()                 │
│ 코드 안전성         │ 자동 해제        │ try-finally 필수                    │
└─────────────────────┴──────────────────┴─────────────────────────────────────┘
```

**📢 섹션 요약 비유**: synchronized는 문에 달린 단순한 자물쇠, ReentrantLock은 타이머·복수 열쇠·공정 대기 기능까지 갖춘 스마트 도어락입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### JVM 내부 락 승격 메커니즘

```text
┌──────────────────────────────────────────────────────────┐
│       JVM 모니터 락 상태 전이 (락 팽창)                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [Unlocked]                                              │
│      │ 동일 스레드 반복 접근                             │
│      ▼                                                   │
│  [Biased Lock] ← 편향 잠금: 헤더에 스레드 ID만 기록      │
│  (CAS 없이 접근, 가장 빠름)                              │
│      │ 다른 스레드 경쟁 발생                             │
│      ▼                                                   │
│  [Thin Lock] ← 경량 잠금: CAS로 스택의 락 레코드 시도    │
│  (OS 호출 없음, 짧은 경합에 적합)                        │
│      │ 스핀 실패(경합 심화)                              │
│      ▼                                                   │
│  [Fat Lock] ← 중량 잠금: OS Mutex 사용                   │
│  (스레드 차단, 컨텍스트 스위칭 발생)                     │
└──────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** JVM은 락 경쟁 수준에 따라 자동으로 락 구현을 승급시킨다. 단일 스레드 환경에서는 Biased Lock이 사실상 무비용으로 동작하고, 경쟁이 발생하면 CAS 기반 Thin Lock으로, 심한 경쟁에서는 OS Mutex로 전환된다. 개발자는 이 과정을 인식하지 않아도 되지만, 잦은 락 경쟁은 Thin→Fat 전환으로 성능이 급락하므로 락 범위를 최소화해야 한다.

**📢 섹션 요약 비유**: JVM 락 승격은 주차장 시스템과 같습니다 — 평소엔 간단한 RFID 게이트(편향 잠금), 차가 많으면 번호표 대기(경량), 꽉 차면 전면 통제(중량 잠금).

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오
1. **고성능 캐시 업데이트**: `ConcurrentHashMap` + `ReadWriteLock`으로 읽기 우세 환경에서 독자-저자 문제 해결. `computeIfAbsent()`로 원자적 캐시 미스 처리.
2. **배치 처리 완료 대기**: `CountDownLatch`로 N개 작업 스레드가 모두 완료될 때까지 메인 스레드를 대기시키는 패턴. 유한 버퍼 소비자의 일괄 처리 완료 확인에 활용.

### 도입 체크리스트
- **while 루프 재확인**: `wait()` 이후 조건을 while로 재확인하는가?
- **예외 안전**: ReentrantLock 사용 시 finally 블록에서 `unlock()` 호출되는가?
- **범위 최소화**: synchronized 블록 내부에 I/O나 긴 연산이 없는가?

### 안티패턴
- **notify() 단독 사용**: 잘못된 스레드가 깨어나면 아무 조건도 충족하지 못하고 다시 wait() → 무한 대기.
- **이중 락 확인(Double-Checked Locking) 미완성**: `volatile` 없이 구현하면 JIT 최적화로 초기화 전 객체 참조 노출.

```java
// ❌ 잘못된 DCLK
if (instance == null) {
    synchronized (this) {
        if (instance == null)
            instance = new Singleton(); // JIT가 초기화 전 참조 노출 가능
    }
}

// ✅ 올바른 DCLK
private volatile static Singleton instance;
```

**📢 섹션 요약 비유**: notify() 단독 사용은 복권 1장만 파는 추첨 — 당첨자가 아닌 사람이 나올 수 있어요. notifyAll()은 모두 깨워 배 아프지 않게 하는 게 더 안전합니다.

---

## Ⅴ. 기대효과 및 결론

| 도구 | 사용 시나리오 | 주의 사항 |
|:---|:---|:---|
| synchronized | 단순 상호 배제 | 락 범위 최소화 |
| ReentrantLock | 타임아웃·공정성·다중 조건 | try-finally 필수 |
| Semaphore | 자원 풀 카운팅 | 초기값·permit 수 설계 필요 |
| ReadWriteLock | 읽기 집중 공유 데이터 | 저자 기아 모니터링 |
| CountDownLatch | 작업 완료 동기화 | 재사용 불가 (CyclicBarrier 대안) |

---

## 📌 관련 개념 맵

| 개념 | 관계 |
|:---|:---|
| 모니터 (Monitor) | synchronized의 이론적 기반 |
| volatile | 메모리 가시성 보장, DCLK 안전화 |
| CAS (Compare-And-Swap) | JUC 동기화 클래스의 내부 구현 기반 |
| JVM Biased Locking | synchronized 성능 최적화 내부 메커니즘 |
| POSIX Pthreads | Java 동기화의 OS 수준 기반 |

## 👶 어린이를 위한 3줄 비유 설명
1. `synchronized`는 화장실 문 자물쇠 — 들어갈 때 잠그고, 나올 때(예외가 나도!) 자동으로 열려요.
2. `wait()`는 "줄이 너무 길면 잠깐 대기실로 가세요", `notify()`는 "이제 들어오세요!" 신호예요.
3. `ReentrantLock`은 더 똑똑한 자물쇠 — "5초 기다려도 안 열리면 포기"나 "키 가진 사람 순서대로" 같은 세밀한 규칙도 설정할 수 있어요!
