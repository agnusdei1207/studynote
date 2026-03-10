+++
title = "314. 기아 상태 (Starvation) 발생 방지 (희생자 선택에 횟수 제한)"
weight = 314
+++

# 314. 타임아웃 기반 복구 (Timeout-based Recovery)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시간 제한으로 교착상태 자동 해소
> 2. **가치**: 간단하고 실용적인 복구 방법
> 3. **융합**: 교착상태 복구, 희생자 선택과 연관

---

## Ⅰ. 개요

### 개념 정의

타임아웃 기반 복구(Timeout-based Recovery)는 **자원 요청이나 보유에 시간 제한을 두어 교착상태를 자동으로 해소하는 방법**이다. 시간이 초과하면 작업을 중단하거나 재시도한다.

### 💡 비유: 주차 요금
타임아웃 기반 복구는 **주차 요금**과 같다. 일정 시간이 지나면 돈을 더 내거나 나가야 한다. 무한히 주차할 수 없다.

### 타임아웃 기반 복구 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                타임아웃 기반 복구 구조                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 원리】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  프로세스 P                                                            │ │
│  │       │                                                             │ │
│  │       │ 자원 요청                                                   │ │
│  │       ▼                                                             │ │
│  │  ┌─────────────┐                                                    │ │
│  │  │ 타이머 시작   │                                                    │ │
│  │  └──────┬──────┘                                                    │ │
│  │         │                                                             │ │
│  │    ┌────┴────┐                                                       │ │
│  │    │         │                                                       │ │
│  │   할당됨    타임아웃                                                 │ │
│  │    │         │                                                       │ │
│  │    ▼         ▼                                                       │
│  │  작업 계속   롤백/재시도                                              │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【타임아웃 종류】                                                      │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 요청 타임아웃:                                                   │ │
│  │     • 자원 요청 후 대기 시간 제한                                     │ │
│  │     • 초과 시: 요청 취소, 에러 반환                                   │ │
│  │                                                             │ │
│  │  2. 보유 타임아웃:                                                   │ │
│  │     • 자원 보유 시간 제한                                             │ │
│  │     • 초과 시: 강제 해제, 롤백                                        │ │
│  │                                                             │
│  │  3. 트랜잭션 타임아웃:                                                │ │
│  │     • 트랜잭션 전체 수행 시간 제한                                     │ │
│  │     • 초과 시: 트랜잭션 중단                                           │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【복구 동작】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  타임아웃 발생 시 선택:                                                │ │
│  │                                                             │ │
│  │  1. 작업 중단 (Abort):                                               │ │
│  │     • 자원 해제                                                       │ │
│  │     • 상태 롤백                                                       │ │
│  │     • 에러 반환                                                       │ │
│  │                                                             │ │
│  │  2. 재시도 (Retry):                                                  │ │
│  │     • 자원 해제                                                       │ │
│  │     • 대기 후 다시 시도                                               │ │
│  │     • 최대 재시도 횟수 제한                                           │ │
│  │                                                             │ │
│  │  3. 백오프 (Backoff):                                                │ │
│  │     • 재시도 간격 점진적 증가                                          │ │
│  │     • Exponential backoff                                           │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                타임아웃 기반 복구 상세                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【타임아웃 값 설정】                                                   │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  고려사항:                                                            │ │
│  │  • 너무 짧음: 정상 작업도 중단 (false positive)                      │ │
│  │  • 너무 김: 교착상태 오래 지속                                        │ │
│  │                                                             │ │
│  │  설정 방법:                                                           │ │
│  │  • 고정값: 모든 작업에 동일한 타임아웃                                 │ │
│  │  • 동적값: 작업 유형, 부하에 따라 조정                                 │ │
│  │  • 적응형: 과거 통계 기반 자동 조정                                   │ │
│  │                                                             │ │
│  │  일반적 값:                                                           │ │
│  │  • 락 대기: 1-30초                                                   │ │
│  │  • DB 트랜잭션: 30-300초                                             │ │
│  │  • 네트워크 요청: 5-60초                                             │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【장단점】                                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  장점:                                                                │ │
│  │  • 구현 간단                                                          │ │
│  │  • 교착상태 탐지 불필요                                               │ │
│  │  • 자동 복구                                                          │ │
│  │  • 오버헤드 낮음                                                      │ │
│  │                                                             │ │
│  │  단점:                                                                │ │
│  │  • 교착상태 아님에도 중단 가능                                         │ │
│  │  • 타임아웃 값 설정 어려움                                            │ │
│  │  • 작업 손실 가능                                                     │ │
│  │  • 기아 상태 가능 (계속 타임아웃)                                     │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【vs 다른 복구 방법】                                                  │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  방법              교착상태 탐지    정확도    오버헤드              │ │
│  │  ────────          ────────────    ──────    ──────────          │ │
│  │  타임아웃           불필요           낮음      낮음                 │ │
│  │  사이클 탐지        필요             높음      중간                 │ │
│  │  은행원 알고리즘     필요             높음      높음                 │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【락 타임아웃】                                                         │
│  ──────────────────                                                  │
│  // Java ReentrantLock with timeout                                 │
│  ReentrantLock lock = new ReentrantLock();                          │
│  try {                                                               │
│      if (lock.tryLock(5, TimeUnit.SECONDS)) {                       │
│          try {                                                       │
│              // 작업 수행                                              │ │
│          } finally {                                                 │
│              lock.unlock();                                          │ │
│          }                                                          │
│      } else {                                                        │
│          // 타임아웃 - 락 획득 실패                                    │ │
│          throw new TimeoutException("Lock timeout");                 │ │
│      }                                                              │
│  } catch (InterruptedException e) {                                 │
│      Thread.currentThread().interrupt();                            │
│  }                                                                  │
│                                                                     │
│  【데이터베이스 타임아웃】                                               │
│  ──────────────────                                                  │
│  // MySQL                                                            │
│  SET SESSION innodb_lock_wait_timeout = 5;  // 락 대기 5초            │ │
│  SET SESSION max_execution_time = 30000;     // 쿼리 30초             │ │
│                                                                     │
│  // PostgreSQL                                                       │
│  SET statement_timeout = '30s';                                     │
│  SET lock_timeout = '5s';                                           │
│  SET idle_in_transaction_session_timeout = '60s';                   │
│                                                                     │
│  // JDBC                                                             │
│  Connection conn = dataSource.getConnection();                      │
│  conn.setNetworkTimeout(executor, 30000);  // 30초                   │ │
│  Statement stmt = conn.createStatement();                           │
│  stmt.setQueryTimeout(30);  // 30초                                  │ │
│                                                                     │
│  【트랜잭션 타임아웃】                                                   │
│  ──────────────────                                                  │
│  // Spring @Transactional                                           │
│  @Transactional(timeout = 30)  // 30초                               │ │
│  public void doWork() {                                             │
│      // 작업                                                          │ │
│  }                                                                  │
│                                                                     │
│  // 프로그래밍 방식                                                     │ │
│  TransactionOptions options = new TransactionOptions();             │
│  options.setTimeout(Duration.ofSeconds(30));                        │
│  transactionTemplate.execute(options, status -> {                   │
│      // 작업                                                          │ │
│      return null;                                                    │ │
│  });                                                                │
│                                                                     │
│  【재시도 with 백오프】                                                 │
│  ──────────────────                                                  │
│  class RetryWithBackoff {                                           │
│      int maxRetries = 5;                                            │
│      long initialDelay = 100;  // 100ms                             │
│      long maxDelay = 10000;    // 10s                               │
│      double multiplier = 2.0;                                       │
│                                                                     │
│      void executeWithRetry(Runnable task) {                         │
│          long delay = initialDelay;                                 │
│          for (int i = 0; i < maxRetries; i++) {                     │
│              try {                                                   │
│                  task.run();                                         │ │
│                  return;  // 성공                                    │ │
│              } catch (TimeoutException e) {                         │
│                  if (i == maxRetries - 1) {                         │
│                      throw new RuntimeException("Max retries exceeded");│
│                  }                                                  │
│                  try {                                               │
│                      Thread.sleep(delay);                           │
│                  } catch (InterruptedException ie) {                │
│                      Thread.currentThread().interrupt();            │
│                      return;                                        │
│                  }                                                  │
│                  delay = Math.min((long)(delay * multiplier), maxDelay);│
│              }                                                      │
│          }                                                          │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【HTTP 요청 타임아웃】                                                 │
│  ──────────────────                                                  │
│  // OkHttp                                                           │
│  OkHttpClient client = new OkHttpClient.Builder()                   │
│      .connectTimeout(10, TimeUnit.SECONDS)                          │
│      .readTimeout(30, TimeUnit.SECONDS)                             │
│      .writeTimeout(30, TimeUnit.SECONDS)                            │
│      .build();                                                       │
│                                                                     │
│  // Apache HttpClient                                                │
│  RequestConfig config = RequestConfig.custom()                      │
│      .setConnectTimeout(10000)                                      │
│      .setSocketTimeout(30000)                                       │
│      .build();                                                       │
│                                                                     │
│  【타임아웃 모니터링】                                                   │
│  ──────────────────                                                  │
│  class TimeoutMetrics {                                             │
│      AtomicLong timeoutCount = new AtomicLong();                    │
│      AtomicLong totalWaitTime = new AtomicLong();                   │
│                                                                     │
│      void recordTimeout(long waitTime) {                            │
│          timeoutCount.incrementAndGet();                            │
│          totalWaitTime.addAndGet(waitTime);                         │
│      }                                                              │
│                                                                     │
│      double getAverageWaitTime() {                                  │
│          long count = timeoutCount.get();                           │
│          return count > 0 ? (double) totalWaitTime.get() / count : 0;│
│      }                                                              │
│  }                                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 시간 제한으로 교착상태 자동 해소
• 종류: 요청, 보유, 트랜잭션 타임아웃
• 복구: 중단, 재시도, 백오프
• 장점: 간단, 자동, 낮은 오버헤드
• 단점: false positive, 설정 어려움
• 활용: DB, 락, 네트워크 요청
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [교착상태 복구](./296_deadlock_recovery.md) → 상위 개념
- [희생자 선택](./315_victim_selection.md) → 관련
- [롤백](./316_rollback.md) → 복구 방법
- [타조 알고리즘](./318_ostrich_algorithm.md) → 대안

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 타임아웃 복구는 "주차 요금" 같아요!

**원리**: 시간이 지나면 나가야 해요!

**효과**: 무한 대기를 막아요!
