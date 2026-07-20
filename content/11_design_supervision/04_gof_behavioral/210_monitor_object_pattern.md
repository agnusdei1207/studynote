---
title: "Monitor Object Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 210
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Monitor Object (모니터 객체) 패턴은 멀티스레드 환경에서 객체의 메서드를 <strong>상호 배제(Mutual Exclusion)</strong>로 실행하도록 보장하며, Java의 `synchronized` 키워드가 바로 이 패턴의 언어 내장 구현이다.
> 2. **가치**: 객체 자신이 동기화 메커니즘을 캡슐화하여, 사용자가 명시적 락 관리 없이 스레드 안전(Thread-Safe)한 객체를 사용할 수 있게 한다.
> 3. **판단 포인트**: 모니터의 4요소(상호 배제, 진입 대기열, 조건 대기열, 조건 변수)를 이해하면 `synchronized` + `wait/notify` 동작을 완전히 예측하고 제어할 수 있다.

---

## Ⅰ. 개요 및 필요성
```java
// 동기화 없는 카운터 (Thread-Unsafe)
class Counter {
    private int count = 0;
    public void increment() { count++; }  // count = count + 1 (3단계 연산)
    public int get() { return count; }
}

// 2개 스레드가 동시에 increment():
// Thread A: count 읽기(0) -> Thread B: count 읽기(0)
//           +1 계산(1)    ->            +1 계산(1)
//           저장(1)       ->            저장(1)
// 결과: 2여야 하는데 1이 됨 -> Race Condition (경쟁 조건)
```

```java
// Monitor Object 패턴 적용 (synchronized)
class SynchronizedCounter {
    private int count = 0;

    public synchronized void increment() { count++; }  // Monitor Lock 자동 적용
    public synchronized int get() { return count; }
}
// -> 단 하나의 스레드만 메서드에 진입 가능 -> Race Condition 없음
```

Hoare(1974)가 제안한 Monitor 개념을 Java(1995)가 언어 수준으로 통합했다. C++, Python에서는 별도 라이브러리(`std::mutex`, `threading.Lock`) 필요하지만, Java는 모든 객체가 기본적으로 모니터를 내장한다.

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 화장실 잠금장치(Monitor) — 한 번에 한 사람만 들어갈 수 있고, 나올 때 잠금이 자동으로 해제된다. 들어가려는 다른 사람들은 밖에서 대기한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  +----------------------------------------------------------+
  |                   Monitor Object                         |
  |                                                          |
  |  1. Mutual Exclusion (상호 배제)                         |
  |     -> 한 번에 하나의 스레드만 synchronized 메서드 실행   |
  |                                                          |
  |  2. Entry Set (진입 대기열)                              |
  |     -> synchronized 진입을 위해 대기하는 스레드 집합      |
  |     -> 락 해제 시 Entry Set에서 하나가 진입              |
  |                                                          |
  |  3. Wait Set (조건 대기열)                               |
  |     -> wait() 호출 후 대기 중인 스레드 집합               |
  |     -> notify()/notifyAll()로 재활성화                   |
  |                                                          |
  |  4. Condition Variable (조건 변수)                       |
  |     -> wait()/notify() 기반 조건 동기화                  |
  +----------------------------------------------------------+
```

```
                     진입 시도
                         |
              +----------v----------+
              |  Entry Set (대기)   |
              |  Thread B, Thread C |
              +----------+----------+
                         | 락 획득
                         v
  +--------------------------------------+
  |  Monitor Object (실행 중: Thread A)  |
  |                                      |
  |  Thread A가 wait() 호출              |
  |           |                          |
  |           v                          |
  |  +--------------------+              |
  |  |  Wait Set (대기)   |              |
  |  |  Thread A          |◄- notify() -+|
  |  +--------------------+             ||
  |                                     ||
  +-------------------------------------+|
                                         |
                          notify()/notifyAll() 호출 시
                          -> Wait Set -> Entry Set으로 이동
```

```java
// Java에서 모든 객체는 Intrinsic Lock(Monitor Lock)을 보유

// 메서드 레벨 동기화
public synchronized void method() {
    // this 객체의 Intrinsic Lock 획득
}

// 블록 레벨 동기화 (더 세밀한 제어)
public void method() {
    synchronized (this) {
        // this의 Lock 획득 (더 좁은 범위)
    }
    // Lock 해제 후 이 코드는 병렬 실행 가능
}

// 클래스 레벨 동기화 (정적 메서드)
public static synchronized void staticMethod() {
    // MyClass.class 객체의 Intrinsic Lock 획득
}
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 회의실 예약 시스템 — 한 팀이 회의 중(synchronized)이면 다른 팀은 예약 목록(Entry Set)에서 기다린다. 중간에 "자료 준비 중"으로 잠깐 나오면(wait) 빈 회의실(Wait Set)에 있다가, 준비 완료 신호(notify)가 오면 다시 예약 목록으로 돌아간다.

---

## Ⅲ. 비교 및 연결
| 항목 | Mutex | Monitor | Semaphore |
|:---|:---|:---|:---|
| **기본 개념** | 상호 배제 락 | 동기화 + 조건 대기 통합 | 카운팅 기반 접근 제어 |
| <strong>허용 스레드</strong> | 1개 | 1개 (조건 대기 포함) | N개 (세마포 값) |
| **조건 대기** | ❌ (별도 구현) | ✅ (wait/notify 내장) | ❌ |
| **소유권** | 획득 스레드만 해제 | 획득 스레드만 해제 | 누구든 해제 가능 |
| **Java 구현** | ReentrantLock | synchronized | Semaphore |
| **사용 상황** | 단순 상호 배제 | 조건 기반 협력 | 자원 풀, 병렬 제한 |

| 항목 | synchronized (Monitor) | ReentrantLock |
|:---|:---|:---|
| **코드 간결성** | ✅ 자동 해제 | 수동 unlock() 필요 |
| **세밀한 제어** | ❌ 제한적 | ✅ tryLock, lockInterruptibly |
| **여러 조건** | ❌ 1개 (wait/notify) | ✅ 여러 Condition |
| <strong>공정성 정책</strong> | ❌ | ✅ fair=true |
| <strong>성능</strong> | JVM 최적화됨 | 유사 |

- **📢 섹션 요약 비유**: Mutex는 "열쇠", Monitor는 "열쇠 + 대기실 + 호출벨을 포함한 완전한 접수 시스템", Semaphore는 "주차장 입구의 빈 자리 수 표시".

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// Thread-Safe Counter with Monitor Pattern
public class MonitorCounter {
    private long count = 0;
    private long maxValue;

    public MonitorCounter(long max) { this.maxValue = max; }

    // synchronized = Monitor Lock 적용
    public synchronized void increment() throws InterruptedException {
        while (count >= maxValue) {
            wait();  // Wait Set으로 이동
        }
        count++;
        notifyAll();  // 대기 중인 스레드들 깨움
    }

    public synchronized void decrement() throws InterruptedException {
        while (count <= 0) {
            wait();  // 0이 되면 대기
        }
        count--;
        notifyAll();
    }

    public synchronized long getCount() { return count; }
}
```

```
  ❌ 흔한 실수들:
  1. notify() vs notifyAll()
     - notify(): Wait Set에서 임의 1개만 깨움 -> 특정 조건 대기 스레드 미깨움 위험
     - notifyAll(): 모두 깨움 -> 안전하지만 오버헤드
     -> 일반적으로 notifyAll() 권장

  2. wait()를 if가 아닌 while 안에서 사용
     - Spurious Wakeup(허위 깨움): notify 없이 깨어나는 경우
     - while(condition) wait(); 로 조건 재확인 필수

  3. synchronized 범위 최소화
     - synchronized(this) { ... } 블록 안을 최소화
     - I/O, 원격 호출 등을 synchronized 밖으로 이동
```

- Monitor의 **4요소** (상호 배제, Entry Set, Wait Set, Condition Variable) 명시
- Java `synchronized`가 언어 수준의 Monitor 구현임을 설명
- `notify()` vs `notifyAll()` 차이 및 `while` 패턴의 필요성 설명

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 모니터 패턴은 "공유 프린터 관리 소프트웨어" — 인쇄 중이면(모니터 점유) 다른 인쇄 요청은 대기열(Entry Set)에서 기다리고, 용지 없으면 인쇄 중인 스레드도 잠시 대기(Wait Set)한다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| Race Condition 방지 | 공유 상태에 대한 원자적 접근 보장 |
| 캡슐화된 동기화 | 사용자가 락 관리 불필요 |
| 조건 기반 협력 | wait/notify로 스레드 간 협력 구현 |
| JVM 최적화 | 비경합 상황에서 Biased Locking 등으로 오버헤드 최소화 |

- <strong>Lock Contention</strong>: 높은 경합 시 성능 저하
- <strong>교착상태(Deadlock)</strong>: 잘못된 lock 순서로 발생 가능
- <strong>모니터 범위</strong>: 너무 넓으면 병렬성 감소, 너무 좁으면 관리 복잡

Monitor Object (모니터 객체) 패턴은 Java 동시성의 근간이다. `synchronized`, `wait/notify`, `Object.notify/wait` 모두 이 패턴의 구현이다. 4요소(Mutual Exclusion, Entry Set, Wait Set, Condition Variable)를 이해하면 Java 멀티스레딩 동작을 완전히 예측할 수 있다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 모니터는 "자동 잠금 회의실" — 들어가면 자동으로 잠기고, 나오면 자동으로 열린다. 대기 중인 팀은 순서대로 들어간다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 동시성 패턴 (Concurrency Pattern) | 병렬 처리 설계 패턴 그룹 |
| 연관 개념 | Mutual Exclusion (상호 배제) | Monitor의 핵심 제공 기능 |
| 연관 개념 | Intrinsic Lock (내재 락) | Java 객체의 Monitor Lock |
| 연관 개념 | wait/notify | Monitor의 조건 동기화 메커니즘 |
| 연관 개념 | ReentrantLock | Monitor보다 유연한 명시적 락 |
| 연관 개념 | Semaphore | Monitor와 비교되는 카운팅 동기화 |

### 📈 관련 키워드 및 발전 흐름도
임계구역 보호 -> 모니터 객체 패턴 -> Condition Queue

### 👶 어린이를 위한 3줄 비유 설명
1. 화장실에는 잠금장치가 있어서 한 명만 들어갈 수 있어요(상호 배제).
2. 다른 사람들은 밖에서 줄을 서서 기다려요(Entry Set).
3. 안에서 "잠깐만요!"하고 기다리는 사람은 대기실로 가고(Wait Set), 부르면 다시 나올 수 있어요!
