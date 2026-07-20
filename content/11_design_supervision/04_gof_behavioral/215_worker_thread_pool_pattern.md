---
title: "Worker Thread / Thread Pool Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 215
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Thread Pool (스레드 풀) 패턴은 매 요청마다 스레드를 생성/소멸하는 비용을 제거하기 위해, 미리 생성된 재사용 가능한 스레드 집합(Pool)에 작업을 분배하는 객체 풀 특화 패턴이다.
> 2. **가치**: 스레드 생성 지연(수 ms~수십 ms)을 제거하고, 동시 실행 가능한 스레드 수를 제한하여 CPU/메모리 자원을 안정적으로 관리한다.
> 3. **판단 포인트**: 적정 스레드 수 공식 `N = CPU 코어 수 × (1 + 대기시간 / 처리시간)` — I/O 바운드 작업은 스레드를 더 많이, CPU 바운드 작업은 코어 수에 가깝게 설정한다.

---

## Ⅰ. 개요 및 필요성
스레드 하나를 생성하면:
- JVM 기준 기본 스택 메모리 512KB~1MB 할당
- OS 커널 객체 생성 (수 ms 지연)
- 컨텍스트 스위칭 오버헤드 증가

초당 1,000개 요청이 들어오는 서버에서 매 요청마다 스레드를 생성하면 초당 1,000번의 스레드 생성/소멸이 발생 -> 실제 처리보다 스레드 관리 비용이 더 커지는 역설.

```
사전 스레드 생성:
  Pool 초기화 -> N개 스레드를 미리 생성하여 대기(IDLE) 상태로 유지

요청 처리:
  요청 도착 -> Work Queue에 삽입 -> 유휴 스레드가 작업 꺼내 실행
              -> 실행 완료 -> 스레드 Pool로 반환 (소멸 X, 재사용 O)
```

- 웹 서버의 HTTP 요청 처리
- 데이터베이스 연결 관리 (Connection Pool과 혼용)
- 비동기 작업 실행 (Java `CompletableFuture.supplyAsync()`)
- 배치 처리 병렬화

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 택시 회사에서 손님이 올 때마다 기사를 새로 고용하는 것이 아니라, 기사들을 대기실(Pool)에 준비시켜두고 호출이 오면 배차하는 것이 스레드 풀이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+----------------------------------------------------------------+
|                   Thread Pool Architecture                     |
|                                                                |
|  +--------------+    submit()    +--------------------------+  |
|  |   Client     |---------------->|     Work Queue           |  |
|  |  (호출자)    |                |  [Task1][Task2][Task3]..  |  |
|  +--------------+                +------------+-------------+  |
|                                               |                |
|                         +---------------------+                |
|                         | 작업 가져가기 (take)                   |
|                         v                                      |
|  +---------------------------------------------------------+   |
|  |                   Thread Pool                           |   |
|  |  +-----------+  +-----------+  +-----------+           |   |
|  |  | Thread-1  |  | Thread-2  |  | Thread-N  |  (IDLE)   |   |
|  |  | [Task1]   |  | [Task2]   |  |  대기 중   |           |   |
|  |  +-----------+  +-----------+  +-----------+           |   |
|  |                                                         |   |
|  |  corePoolSize ~ maximumPoolSize (동적 확장 구간)         |   |
|  +---------------------------------------------------------+   |
+----------------------------------------------------------------+
```

| 파라미터 | 설명 | 기본값/권장 |
|:---|:---|:---|
| `corePoolSize` | 항상 유지할 최소 스레드 수 | CPU 코어 수 |
| `maximumPoolSize` | 최대 허용 스레드 수 | I/O 바운드: 코어 × 2~4 |
| `keepAliveTime` | core 초과 스레드 유휴 시 유지 시간 | 60초 |
| `workQueue` | 작업 대기 큐 종류 | `LinkedBlockingQueue` |
| `rejectedExecutionHandler` | 큐 가득 찰 때 정책 | `CallerRunsPolicy` |

| 큐 종류 | 특징 | 사용 시점 |
|:---|:---|:---|
| `LinkedBlockingQueue` (무제한) | 큐 무한 증가 가능 | 메모리 주의 필요 |
| `ArrayBlockingQueue` (제한) | Backpressure 자동 적용 | 프로덕션 권장 |
| `SynchronousQueue` | 큐 없음, 즉시 스레드 배정 | cachedThreadPool |
| `PriorityBlockingQueue` | 우선순위 기반 처리 | 긴급 작업 우선 처리 |

```
CPU 바운드 작업:  N_threads = N_cpu + 1
I/O 바운드 작업:  N_threads = N_cpu × (1 + 대기시간 / 처리시간)
                           = N_cpu × (1 + W/C)

예시: 4코어, I/O 대기 90ms, CPU 처리 10ms
  N = 4 × (1 + 90/10) = 4 × 10 = 40 스레드
```

- **📢 섹션 요약 비유**: 주방 요리사 수를 정할 때 — 볶음 요리(CPU 바운드)는 화구 수만큼, 오래 끓이는 탕(I/O 바운드)은 끓이는 동안 다른 요리를 할 수 있으니 화구 수보다 훨씬 많은 요리사가 필요하다.

---

## Ⅲ. 비교 및 연결
| 정책 | 동작 | 적합한 상황 |
|:---|:---|:---|
| `AbortPolicy` (기본) | `RejectedExecutionException` 발생 | 에러 즉시 감지 필요 |
| `CallerRunsPolicy` | 호출자 스레드가 직접 실행 | 자동 속도 조절(Backpressure) |
| `DiscardPolicy` | 작업 조용히 버림 | 손실 허용 가능한 로그 처리 |
| `DiscardOldestPolicy` | 가장 오래된 작업 버리고 재시도 | 최신 요청 우선 처리 |

```
스레드 기아 시나리오:
  Task A (풀 점유) -> 내부에서 Task B를 submit()
  -> Task B는 큐에서 대기
  -> 그러나 모든 스레드가 Task A로 점유되어 Task B를 실행할 스레드 없음
  -> Task A는 Task B 완료를 기다림 -> 교착 상태(Deadlock)

해결책:
  1. 독립 스레드 풀 사용 (작업 유형별 풀 분리)
  2. maximumPoolSize를 충분히 크게 설정
  3. CompletableFuture 비동기 체이닝으로 블로킹 제거
```

| 메서드 | 특징 | 주의사항 |
|:---|:---|:---|
| `newFixedThreadPool(n)` | n개 고정 스레드, 무제한 큐 | OOM 위험 (무제한 큐) |
| `newCachedThreadPool()` | 요청마다 스레드 생성, 60s 유휴 시 제거 | 스레드 폭발 위험 |
| `newSingleThreadExecutor()` | 스레드 1개, 순차 실행 보장 | 처리량 낮음 |
| `newScheduledThreadPool(n)` | 지연/반복 작업 지원 | - |
| `newWorkStealingPool()` | ForkJoinPool 기반, 코어 수 | 재귀 작업에 최적 |

- **📢 섹션 요약 비유**: 무제한 큐 = 주문을 무한히 받다가 주방이 터지는 레스토랑, 제한 큐 = "지금 자리 없습니다. 기다리시겠어요?" 라고 미리 알려주는 레스토랑이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
Java 21의 Virtual Thread (가상 스레드)는 스레드 수 제한 없이 경량 스레드를 활용하여 I/O 블로킹 문제를 OS 레벨에서 해결한다:

```java
// Java 21 Virtual Thread Executor
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
executor.submit(() -> {
    // I/O 블로킹 발생 시 OS 스레드를 반환하고 재사용
    database.query(...);
});
```

Virtual Thread를 사용해도 CPU 바운드 작업에서는 기존 Platform Thread Pool이 여전히 유리하다.

| 지표 | 설명 | 임계값 |
|:---|:---|:---|
| Active Thread Count | 현재 작업 중인 스레드 수 | maxPoolSize의 80% 초과 시 경고 |
| Queue Size | 대기 중인 작업 수 | 목표치의 2배 초과 시 경고 |
| Rejected Task Count | 거부된 작업 수 | 0이어야 정상 |
| Thread Creation Rate | 단위시간당 스레드 생성 수 | 풀 크기 재검토 신호 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 스레드 풀 모니터링은 공장 대시보드 — 가동 중인 기계 수(Active), 컨베이어 벨트의 미완성 제품 수(Queue), 작업 거부 횟수(Rejected)를 실시간으로 보는 것이다.

---

## Ⅴ. 기대효과 및 결론
Thread Pool 패턴은 현대 서버 소프트웨어의 가장 보편적인 동시성 관리 기법이다. 올바르게 설정된 스레드 풀은:

- <strong>응답 지연 감소</strong>: 스레드 생성 오버헤드 제거
- **자원 안정화**: 스레드 수 상한으로 OOM/CPU 폭발 방지
- <strong>처리량 극대화</strong>: I/O 대기 중에 다른 요청 처리 병행

잘못 설정된 스레드 풀은:
- **무제한 큐 + FixedThreadPool**: OOM (Out of Memory)
- **너무 큰 maximumPoolSize**: 컨텍스트 스위칭 폭발
- <strong>단일 풀에서 Task 내 Task submit</strong>: 교착 상태(Deadlock)

학습 문제에서는 <strong><code>ThreadPoolExecutor</code> 파라미터의 역할</strong>과 <strong>스레드 수 결정 공식</strong>을 정확히 서술하고, <strong>거부 정책(RejectedExecutionHandler)</strong> 별 차이를 비교하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 스레드 풀은 여름 아르바이트생 관리와 같다 — 항상 최소 인원(corePoolSize)은 유지하고, 바쁠 때만 임시 충원(maximumPoolSize)하며, 너무 여유로우면 계약 종료(keepAliveTime)하고, 그래도 일이 밀리면 거부 정책(RejectedExecutionHandler)을 적용한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Object Pool Pattern | 스레드 풀은 스레드 객체를 풀로 관리 |
| 연관 개념 | Half-Sync/Half-Async | 동기 계층의 Worker Thread Pool로 활용 |
| 연관 개념 | Proactor Pattern | Completion Handler 실행에 스레드 풀 사용 |
| 구현체 | Java ThreadPoolExecutor | Java 표준 스레드 풀 구현 |
| 구현체 | ForkJoinPool | 재귀 분할-정복 작업에 특화된 스레드 풀 |
| 연관 개념 | Virtual Thread (Java 21) | OS 스레드 없이 경량 스레드로 대체 |
| 측정 도구 | Micrometer / Prometheus | 스레드 풀 지표 모니터링 |

### 📈 관련 키워드 및 발전 흐름도
작업 큐 -> 워커 스레드/스레드 풀 패턴 -> Executor 서비스

### 👶 어린이를 위한 3줄 비유 설명
1. 놀이공원에서 놀이기구 마다 안전요원이 항상 대기(Pool)해 있어서 줄 서는 손님(요청)이 오면 바로 운행(처리)할 수 있어.
2. 안전요원을 손님 올 때마다 새로 뽑으면 시간이 많이 걸리니까, 미리 뽑아서 기다리게 해두는 것이 스레드 풀이야.
3. 안전요원 수(maximumPoolSize)를 너무 많이 뽑으면 급여(메모리)가 너무 많이 들고, 너무 적게 뽑으면 손님이 기다리다 포기(RejectedExecution)하니 딱 적당하게 뽑는 것이 핵심이야.
