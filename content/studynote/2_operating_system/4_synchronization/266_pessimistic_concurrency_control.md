+++
title = "266. 비관적 병행성 제어 (Pessimistic Concurrency Control)"
weight = 266
+++

# 266. 지수 백오프 (Exponential Backoff)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 실패 시 대기 시간을 지수적으로 증가
> 2. **가치**: 경합 완화, 시스템 부하 감소
> 3. **융합**: 스핀락, CAS, 재시도 로직과 연관

---

## Ⅰ. 개요

### 개념 정의

지수 백오프(Exponential Backoff)는 **작업 실패 시 대기 시간을 지수적으로 증가시키는 재시도 전략**이다. 경합 완화와 시스템 과부하 방지에 효과적이다.

### 💡 비유: 공중전화 줄
지수 백오프는 **공중전화 줄**과 같다. 통화 실패하면 1분 기다린다. 또 실패하면 2분, 그 다음엔 4분. 점점 더 기다린다. 줄이 줄어들면 빨리 통화된다.

### 지수 백오프 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                지수 백오프 구조                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 패턴】                                                         │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  시도 1: 실패 → 대기 base_time                                       │ │
│  │  시도 2: 실패 → 대기 base_time × 2                                   │ │
│  │  시도 3: 실패 → 대기 base_time × 4                                   │ │
│  │  시도 4: 실패 → 대기 base_time × 8                                   │ │
│  │  ...                                                               │ │
│  │  시도 n: 실패 → 대기 base_time × 2^(n-1)                             │ │
│  │                                                             │ │
│  │  wait_time = min(base_time × 2^attempt, max_time)                  │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【대기 시간 그래프】                                                   │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  대기 시간                                                           │ │
│  │    ↑                                                                   │ │
│  │    │         ___max___                                               │ │
│  │    │       /                                                          │ │
│  │    │     /                                                            │ │
│  │    │   /                                                              │ │
│  │    │ /                                                                │ │
│  │    └──┴──┴────┴─────┴──────→ 시도 횟수                                 │ │
│  │     1  2   3      4      5                                            │ │
│  │                                                             │ │
│  │  지수적 증가 → 최대값 제한                                              │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【변형】                                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 완전 지수 백오프:                                                 │ │
│  │     wait = base × 2^attempt                                        │ │
│  │                                                             │ │
│  │  2. 제한 지수 백오프:                                                 │ │
│  │     wait = min(base × 2^attempt, max)                              │ │
│  │                                                             │ │
│  │  3. 지터 추가 (Jitter):                                             │ │
│  │     wait = random(base × 2^attempt)  // 랜덤 추가                    │ │
│  │     • 동시 재시도 분산                                                │ │
│  │     • Thundering Herd 방지                                          │ │
│  │                                                             │ │
│  │  4. Decorrelated Jitter (AWS 권장):                                 │ │
│  │     sleep = min(cap, random(base, sleep × 3))                      │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【활용 사례】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  • 스핀락 백오프                                                      │ │
│  │  • CAS 루프                                                         │ │
│  │  • 네트워크 재연결                                                    │ │
│  │  • API 재시도                                                        │ │
│  │  • 분산 락 획득                                                      │ │
│  │  • 이더넷 충돌 해결                                                   │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                지수 백오프 상세                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【백오프 알고리즘 비교】                                               │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  알고리즘              장점              단점                      │ │
│  │  ────────              ────              ────                      │ │
│  │  고정 간격             단순              동시 재시도                  │ │
│  │  선형 증가             예측 가능        여전히 동시 재시도             │ │
│  │  지수 백오프           경합 완화        긴 대기 가능                   │ │
│  │  지수 백오프 + 지터     동시 재시도 방지  복잡                         │ │
│  │                                                             │ │
│  │  AWS 권장: Full Jitter (= randomization)                            │ │
│  │  sleep = random(0, min(cap, base * 2 ^ attempt))                   │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【파라미터 설정】                                                      │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  base_time: 초기 대기 시간                                           │ │
│  │  • 스핀락: 1~100 CPU 사이클                                           │ │
│  │  • 네트워크: 100ms~1s                                                │ │
│  │                                                             │ │
│  │  max_time: 최대 대기 시간                                             │ │
│  │  • 스핀락: 1~10ms                                                    │ │
│  │  • 네트워크: 30s~60s                                                 │ │
│  │                                                             │ │
│  │  max_attempts: 최대 시도 횟수                                         │ │
│  │  • 무제한: 영구 재시도                                                │ │
│  │  • 제한: N회 후 포기                                                  │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【Thundering Herd 문제】                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  상황: 서버 복구 시 모든 클라이언트가 동시에 재연결 시도                   │ │
│  │                                                             │ │
│  │  해결:                                                               │ │
│  │  1. 지터 추가: 랜덤 대기로 분산                                        │ │
│  │  2. 제한된 동시 연결: Rate limiting                                   │ │
│  │  3. 연결 풀: 미리 생성된 연결                                          │ │
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
│  【기본 지수 백오프】                                                  │
│  ──────────────────                                                  │
│  func exponentialBackoff(base, max time.Duration,                   │
│      fn func() error) error {                                        │
│      wait := base                                                    │
│      for {                                                           │
│          err := fn()                                                 │
│          if err == nil {                                             │
│              return nil                                               │
│          }                                                           │
│          time.Sleep(wait)                                            │
│          wait = time.Duration(min(int64(wait)*2, int64(max)))        │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【지터 추가】                                                        │
│  ──────────────────                                                  │
│  import (                                                           │
│      "math/rand"                                                      │
│      "time"                                                          │
│  )                                                                  │
│                                                                     │
│  func jitterBackoff(base, max time.Duration,                         │
│      fn func() error) error {                                        │
│      wait := base                                                    │
│      for {                                                           │
│          err := fn()                                                 │
│          if err == nil {                                             │
│              return nil                                               │
│          }                                                           │
│          // 랜덤 지터 추가 (0 ~ wait)                                   │
│          jitter := time.Duration(rand.Int63n(int64(wait)))           │
│          time.Sleep(jitter)                                          │
│          wait = time.Duration(min(int64(wait)*2, int64(max)))        │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【스핀락 백오프】                                                      │
│  ──────────────────                                                  │
│  void spinlock_with_backoff(atomic_flag* lock) {                    │
│      int backoff = 1;                                                │
│      while (true) {                                                  │
│          if (!atomic_flag_test_and_set(lock)) {                     │
│              return;  // 획득 성공                                      │
│          }                                                           │
│          for (int i = 0; i < backoff; i++) {                          │
│              cpu_relax();  // PAUSE 명령어                              │
│          }                                                           │
│          backoff = min(backoff * 2, MAX_BACKOFF);                    │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【Python 재시도 데코레이터】                                          │
│  ──────────────────                                                  │
│  import time                                                         │
│  import random                                                       │
│  from functools import wraps                                        │
│                                                                     │
│  def retry_with_backoff(max_retries=5, base_delay=0.1,              │
│                         max_delay=30):                               │
│      def decorator(func):                                            │
│          @wraps(func)                                                │
│          def wrapper(*args, **kwargs):                              │
│              delay = base_delay                                      │
│              for attempt in range(max_retries):                      │
│                  try:                                                 │
│                      return func(*args, **kwargs)                    │
│                  except Exception as e:                              │
│                      if attempt == max_retries - 1:                  │
│                          raise                                       │
│                      # 지터 추가                                       │
│                      jitter = random.uniform(0, delay)               │
│                      time.sleep(jitter)                              │
│                      delay = min(delay * 2, max_delay)               │
│          return wrapper                                              │
│      return decorator                                               │
│                                                                     │
│  @retry_with_backoff(max_retries=3)                                 │
│  def fetch_data():                                                   │
│      # 네트워크 요청                                                   │
│      pass                                                            │
│                                                                     │
│  【Java AWS SDK RetryPolicy】                                        │
│  ──────────────────                                                  │
│  import com.amazonaws.retry.PredefinedRetryPolicies;                │
│                                                                     │
│  // AWS SDK 기본 정책 사용                                              │
│  AmazonDynamoDB client = AmazonDynamoDBClientBuilder.standard()     │
│      .withRetryPolicy(PredefinedRetryPolicies.DYNAMODB_DEFAULT)    │
│      .build();                                                       │
│                                                                     │
│  【HTTP 클라이언트 재시도 (axios-retry)】                              │
│  ──────────────────                                                  │
│  const axios = require('axios');                                    │
│  const axiosRetry = require('axios-retry');                         │
│                                                                     │
│  axiosRetry(axios, {                                                │
│      retries: 3,                                                      │
│      retryDelay: (retryCount) => {                                   │
│          return axiosRetry.exponentialDelay(retryCount);             │
│      }                                                              │
│  });                                                                 │
│                                                                     │
│  【이더넷 CSMA/CD 백오프】                                             │
│  ──────────────────                                                  │
│  // 충돌 후 대기 시간 = random(0, 2^n - 1) × slot_time                │
│  // n: 충돌 횟수 (최대 10)                                             │
│  // slot_time: 512 비트 시간 (10Mbps = 51.2μs)                        │
│                                                                     │
│  【Redis 분산 락 백오프】                                             │
│  ──────────────────                                                  │
│  func acquireLock(key string, ttl time.Duration) error {            │
│      const maxWait = 5 * time.Second                                │
│      wait := 10 * time.Millisecond                                   │
│      for {                                                           │
│          ok, _ := rdb.SetNX(ctx, key, "locked", ttl).Result()       │
│          if ok {                                                      │
│              return nil                                               │
│          }                                                           │
│          time.Sleep(wait)                                            │
│          wait = time.Duration(min(int64(wait)*2, int64(maxWait)))   │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【성능 비교】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  시나리오              무백오프      고정 백오프    지수 백오프        │ │
│  │  ────                  ──────        ────────      ────────        │ │
│  │  높은 경합              100 ops      500 ops       2000 ops        │ │
│  │  중간 경합              500 ops      1000 ops      1500 ops        │ │
│  │  낮은 경합              2000 ops     1800 ops      1500 ops        │ │
│  │                                                             │ │
│  │  지수 백오프: 높은 경합에서 가장 효과적                                  │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 실패 시 대기 시간 지수 증가
• 공식: wait = min(base × 2^n, max)
• 변형: 지터 추가로 동시 재시도 분산
• 활용: 스핀락, CAS, 네트워크, API
• 장점: 경합 완화, Thundering Herd 방지
• AWS: Full Jitter 권장
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [스핀락](./230_spinlock.md) → 적용 대상
- [락 스래싱](./264_lock_thrashing.md) → 완화 대상
- [CAS](./240_cas.md) → 적용 대상
- [락 타임아웃](./261_lock_timeout.md) → 관련 개념

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 지수 백오프는 "공중전화 줄" 같아요!

**원리**: 실패할 때마다 더 오래 기다려요!

**효과**: 줄이 줄어들어요!
