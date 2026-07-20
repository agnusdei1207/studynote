---
title: "Counting Semaphore"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 226
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 카운팅 세마포어 (Counting Semaphore)는 내부 카운터 (S)가 0부터 N까지의 값을 가질 수 있어, <strong>N개의 동시 접근을 허용하는 자원 풀 (Resource Pool)</strong>을 모델링하는 데 사용되는 범용 동기화 객체다. 바이너리 세마포어 (Mutex)와 달리 N개의 스레드가 동시에 임계 구역에 진입할 수 있다.
> 2. **가치**: DB 커넥션 풀, 스레드 풀, 버스 정원 등 "정해진 수 limite resources"를 관리하는 모든 곳에서 활용되며, 초과 요청에는.sleep()을 통해 자원 반납 전까지 대기하게 만들어 무질서한 경합을 구조적으로 차단한다.
> 3. **융합**: 세마포어의 카운팅 기능은 생산자-소비자 (Producer-Consumer) 패턴에서 '남은 버퍼 수'와 '채워진 버퍼 수'를 동시에 카운팅하여 양쪽의 속도 차이를 완충하는 전형적인 유한 버퍼 (Bounded Buffer) 구현의 핵심 기반이 된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 정수형 변수 S가 0부터 N까지의 값을 가지며, P 연산 (wait)과 V 연산 (signal)에 의해 원자적으로 증감하는 세마포어다. S가 1인 바이너리 세마포어와 달리, 카운팅 세마포어는 N개의 동시 진입을 허용한다.
- **필요성**: 자원이 단 1개가 아니라 여러 개 (프린터 3대, DB 커넥션 50개, 버스 좌석 40개)일 때, 단순 mutex로 "1명만 들어가고 나머지는 대기"시키면 자원의 Utilization (활용률)이 3% (1/50)로 곤두박질인다. "3명까지는 들어가고, 4번째부터 대기하라"는 정교한인수 제어 메커니즘이 필요하다.

- **등장 배경**: 1965년 데이크스트라가 세마포어를 발표할 때, 상호 배제 (상호 배제, Mutual Exclusion) 용도만 제안한 것은 아니었다. 오히려 그 핵심 목표는 "복수 인스턴스 자원 (Multiple Instance Resource)"을 제어하는 것이었다.

```text
  [카운팅 세마포어의 자원 풀 (Pool) 관리 예시]

  [ 자원 상황: DB Connection Pool 크기 = 3개 (Semaphore S = 3) ]

   스레드 1: wait() 호출  -> (S = 2) [DB 커넥션 1개 사용]
   스레드 2: wait() 호출  -> (S = 1) [DB 커넥션 2개 사용]
   스레드 3: wait() 호출  -> (S = 0) [DB 커넥션 3개 사용]

   풀 고갈 (Pool Exhausted)

   스레드 4: wait() 호출  -> (S < 0이므로 현재 스레드를 Sleep)
   스레드 5: wait() 호출  -> (S < 0이므로 현재 스레드를 Sleep)

   [ 자원 반환 ]
    스레드 2가 DB사용을 끝내고 signal() 호출!
      - S가 1만큼 증가하고, 대기 중인 스레드 중 하나를 Wakeup
      - 스레드 4가 깨어나 DB 커넥션 2번을 할당받는다.
```

**[다이어그램 해설]** 카운팅 세마포어의 핵심은 "0 이하로 감소하면 수면"이라는 정책이다. S가 0일 때 P(wait) 연산을 수행하는 프로세스는 OS에 의해 대기 큐에투입され (수면), 다른 프로세스가 V(signal)을 호출해 S를 늘릴 때까지 영원히 깨어나지 않는다. 이 자동수신/ Wakeup 메커니즘이 자원 풀의uma 관리를 Os가 자동으로 해주는 장치다.

- **📢 섹션 요약 비유**: 놀이공원 입장에 바쁜 날 30개의 사물함 (세마포어 S=30)만 열려 있다. 손님이 올 때마다 키를 하나씩 받아가고 (wait), 나올 때 반납하고 (signal). 열쇠가 다 나가면 (S=0) 다음 손님은 현관 앞 벤치에서 1시간을 기다린다. 사물함 1개가 비는 순간 (signal) 대기자 중 한 명이입원한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 내부 자료구조와 wait/signal 의 상세 구현

카운팅 세마포어의 내부는 매우 간단하지만, 그 단순함이 응용 영역의광대さ을/를가능에하고 있는.

```c
typedef struct {
    int value;              // 현재 카운터 (사용 가능 자원 수)
    Queue waiting_queue;     // 대기 중인 프로세스/스레드 큐
} semaphore;

// P 연산 (Wait, Proberen)
void wait(semaphore *S) {
    S->value--;             // 자원을 사용하겠다고 1 감소
    if (S->value < 0) {     // 자원이 없으면
        // 이 스레드를 대기 큐에 넣고 수면
        add_to_queue(&S->waiting_queue, current_thread);
        sleep();             // CPU 양보 (OS가 문맥 교환)
    }
}

// V 연산 (Signal, Verhogen)
void signal(semaphore *S) {
    S->value++;             // 자원 사용 완료, 1 증가
    if (S->value <= 0) {    // 대기자가 있으면
        // 대기 큐에서 한 스레드를 꺼내서 깨움
        Thread *t = remove_from_queue(&S->waiting_queue);
        wakeup(t);           // 해당 스레드를 Ready 큐로 이동
    }
}
```

### 카운팅 세마포어 vs 뮤텍스 (바이너리 세마포어)

| 특성 | 카운팅 세마포어 | 뮤텍스 (바이너리 세마포어) |
|:---|:---|:---|
| <strong>카운터 범위</strong> | 0 ~ N (복수 동시 진입) | 0 ~ 1 (1개만 진입) |
| ** Ownership** | 없음 (아무 스레드가 signal 가능) | 있음 (lock한 스레드만 unlock 가능) |
| **용도** | 자원 풀 관리, 순서 제어 | 상호 배제 |
| **재귀적 잠금** | 불가 | 가능 (재귀적 mutex) |
| <strong>priority inheritance</strong> | OS가 자동 적용 어려움 | OS가 자동 적용 가능 |

- **📢 섹션 요약 비유**: 뮤텍스는 "내 집 자물쇠"라서 내가 잠그고 내가 열어야 합니다. 카운팅 세마포어는 "공동 놀이터 entry권"으로, 30장이 있는 entry권을 그냥 반납하면 아무나 다시 집어들어 갈 수 있는 구조입니다. 엄격한 상호 배제보다는 유연한 인원 관리가 필요할 때 씁니다.

---

## Ⅲ. 비교 및 연결

### 카운팅 세마포어의 대표적 활용: Bounded Buffer (생산자-소비자)

```text
  +----------------------------------------------------------------------+
  |     3개의 세마포어로 구현하는 생산자-소비자 (유한 버퍼) 패턴          |
  +----------------------------------------------------------------------+
  |                                                                      |
  |  버퍼 크기 N = 5                                                     |
  |                                                                      |
  |  semaphore mutex = 1;        // 버퍼 자체의 상호 배제용               |
  |  semaphore empty = N;         // 빈 공간 카운트 (초기: 5)            |
  |  semaphore full = 0;          // 채워진 공간 카운트 (초기: 0)        |
  |                                                                      |
  |  [생산자 (Producer)]                [소비자 (Consumer)]               |
  |                                                                      |
  |  wait(empty);                      wait(full);                       |
  |  wait(mutex);                     wait(mutex);                      |
  |  // 버퍼에 데이터 삽입                  // 버퍼에서 데이터 꺼냄      |
  |  signal(mutex);                   signal(mutex);                    |
  |  signal(full);                    signal(empty);                    |
  |                                                                      |
  |  핵심 원리:                                                          |
  |  - empty는 "버퍼에 빈자리가 있나?"를 카운트 -> 생산자가 wait (남은 빈칸 줄음) |
  |  - full은 "버퍼에 데이터가 있나?"를 카운트 -> 소비자가 wait (남은 데이터 줄음) |
  |  - mutex는 버퍼 데이터 자체의 충돌 방지만 담당                        |
  +----------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 패턴의 아름다움은 3-way 카운팅에 있다. empty=N, full=0으로 시작하면, 생산자는 빈자리가 생길 때까지 (empty--) 대기하고, 소비자는 데이터가 채워질 때까지 (full--) 대기한다. 5개의 버퍼가 모두 채워지면 empty가 0이 되어 생산자가 blocks, 소비자가 하나씩 빼먹으면 empty가 증가하여 생산자가 깨어난다. 이 피드백 루프가 별도의 명시적Synchronization 없이 자동으로 생산자와 소비자의 속도를 맞추어 준다.

### Reader-Writer Lock에서의 활용

카운팅 세마포어는 읽기-쓰기 문제에서도 활용된다.

```c
semaphore mutex = 1;      // read_count 접근용 상호 배제
semaphore db = 1;          // 실제 DB 자체의 배타적 잠금
int read_count = 0;        // 현재 읽기 중인 리더 수

// Reader
wait(mutex);
    read_count++;
    if (read_count == 1)   // 첫 번째 Reader면
        wait(db);          // DB를 잠근다 (Writer 배제)
signal(mutex);

// ... 읽기 작업 ...

wait(mutex);
    read_count--;
    if (read_count == 0)   // 마지막 Reader면
        signal(db);        // DB를解锁한다
signal(mutex);
```

- **📢 섹션 요약 비유**: Reader-Writer_lock에서 카운팅 세마포어는 "독서실의점유인수 세는 사람"과 같다. 첫 번째 들어온 친구(mutex)가 점유인수를 세고 점유인수가 1이면 불을 켜고( DB 잠금), 마지막 친구가 나가면 불을 끈다( DB해쇄). reading는 점유인수가 한 명이어도 할 수 있지만, writing은 혼자만 점유인수가 가능해야 한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오: HikariCP / Tomcat JDBC Connection Pool

실무의 거의 모든 DB 커넥션 풀은 내부적으로 카운팅 세마포어를 사용한다.

```java
// HikariCP의 내부 메커니즘 (개념적)
public class HikariPool {
    private final Semaphore pooledConnections;

    public HikariPool(int maximumPoolSize) {
        this.pooledConnections = new Semaphore(maximumPoolSize);
    }

    public Connection getConnection(long timeoutMs) throws SQLException {
        // 세마포어로 커넥션 획득 시도
        if (!pooledConnections.tryAcquire(timeoutMs, TimeUnit.MILLISECONDS)) {
            throw new SQLException("커넥션 획득超时");  // 타임아웃
        }

        Connection conn = null;
        try {
            conn = getPooledConnection();  // 실제 커넥션 획득
            return conn;
        } catch (Exception e) {
            pooledConnections.release();     // 실패 시 카운트 즉시 반환
            throw e;
        }
    }
}
```

### 안티패턴: 이중 wait / 이중 signal

카운팅 세마포어에서 가장 위험한 버그:

```c
// ❌ 버그: 이중 wait - 이미 획득한 세마포어를 또 기다림
wait(pool);        // 커넥션 획득
query(pool);       // 커넥션 반납 없이 또 wait() 시도
    wait(pool);    // 🚨 두 번째 wait에서 무한 대기! (이미 획득한 상태에서 대기)
    do_work();

// ❌ 버그: signal 누락 - 리턴 전에 예외가 발생하면 semaphore가 영원히 잠김
sem_wait(&pool);
if (do_work() == ERROR) {
    return;        // 🚨 signal() 호출 없이 함수 종료! 다른 스레드가永久 대기
}
sem_post(&pool);

// ✅ 올바른 패턴: try-finally로 반드시 signal 보장
sem_wait(&pool);
try {
    do_work();
} finally {
    sem_post(&pool);   // 예외가 터지든 말든 반드시 호출
}
```

- **📢 섹션 요약 비유**: 세마포어는 도어스코드입니다. 들어갈 때 (wait) 도어스를 받고, 나올 때 (signal) 도어스를 해제해야 합니다. 도어스를 안 열고 나가버리면 (signal 누락) 다음 사람은영구 대기하게 됩니다. finally문은 "반드시 도어스를 해쇄하라는 것"입니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
카운팅 세마포어를 사용하면 한정된 자원을 합리적으로분배하여 Utilization을 극대화하면서도, 초과 요청에 대해서는명시적수신/ wakeup을 통해 불필요한 폴링(polling)이나 busy-wait를 제거할 수 있다. 특히 I/O-bound 시스템에서 concurrent request 수를 자동으로 제어하는 효과를낸다.

### 결론 및 미래 전망
카운팅 세마포어는 60년 역사의 классический 동기화 primitive이지만, 현대 소프트웨어 엔지니어링에서는 고수준 concurrent 라이브러리(java.util.concurrent, std::counting_semaphore 등) 뒤에 숨겨져 직접 코딩하는 경우가 줄었다. 그러나 그 핵심 개념인 "유한 자원 N개에 대한atomic 카운팅 + 대기열 관리"는 DB 풀, 스레드 풀, I/O 리밋 등 실무 엔지니어링의 모든 곳에서 생존하며, 오히려 분산 시스템에서의 Rate Limiting (예: 토큰 버킷,Leaky Bucket)으로 그 패러다임을 확장하고 있다.

- **📢 섹션 요약 비유**: 카운팅 세마포어는 놀이공원의エントリーチケット입니다. 30장삼적주-keyframes 있으면 30명만입원시키고, 31번째는필ず 기다리게 합니다.유원지 내의모든의놀이기구가평등에자원배치される의가미しく, ITインフラ에서も동じ원리가통용します.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 선점형 커널 (Preemptive Kernel) vs 비선점형 커널 (Non-preemptive Kernel) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 피터슨의 해결책 (Peterson's Algorithm) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 하드웨어 명령어 기반 동기화 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| Test-and-Set 명령어 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[피터슨의 해결책 (Peterson's Algorithm)]
    |
    v
[카운팅 세마포어 (Counting Semaphore)]
    |
    +---> [하드웨어 명령어 기반 동기화]
    +---> [Test-and-Set 명령어]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 카운팅 세마포어 (Counting Semaphore)은 컴퓨터가 여러 친구가 동시에 만져도 부딪히지 않게 순서를 맞추는 규칙이에요.
2. 먼저 피터슨의 해결책 (Peterson's Algorithm)을 이해하면 카운팅 세마포어 (Counting Semaphore)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 카운팅 세마포어 (Counting Semaphore)을 잘 알면 나중에 하드웨어 명령어 기반 동기화도 훨씬 쉽게 배울 수 있어요.
