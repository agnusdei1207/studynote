---
title: "Object Pool Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 219
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Object Pool (객체 풀) 패턴은 생성 비용이 높은 객체(DB 연결, 스레드, HTTP 클라이언트 등)를 미리 생성하여 풀(Pool)에 보관하고, 필요 시 대여(Acquire)하고 사용 후 반납(Release)하는 생명주기 관리 패턴이다.
> 2. **가치**: 객체 생성/소멸 반복 비용을 제거하고, 최대 동시 사용 수를 제한하여 외부 시스템(DB, 외부 API)의 과부하를 방지한다.
> 3. **판단 포인트**: 풀 크기 설정이 핵심이다 — 너무 작으면 대기(Starvation), 너무 크면 불필요한 자원 점유 — Little's Law(리틀의 법칙)로 최적 크기를 계산한다.

---

## Ⅰ. 개요 및 필요성
| 객체 유형 | 생성 비용 | 비용 원인 |
|:---|:---|:---|
| DB Connection | 수십~수백 ms | TCP 3-way 핸드셰이크, 인증, 소켓 할당 |
| Thread | 수 ms | OS 커널 객체, 스택 메모리 할당 |
| HTTP Client (커넥션) | 수십 ms | TCP + TLS 핸드셰이크 |
| JDBC PreparedStatement | 수 ms | DB 서버 파싱/최적화 계획 수립 |
| 암호화 컨텍스트 | 수 ms | 키 스케줄링 |

이런 객체를 요청마다 생성/소멸하면:
- 응답 지연 증가 (생성 비용이 처리 시간을 초과)
- DB 연결 한도 초과 -> 연결 거부(Connection Refused)
- GC 압박 -> 지연 시간(Latency) 급증

```
풀 초기화 (Startup):
  +-> N개 객체를 미리 생성하여 IDLE 상태로 대기

대여 (Acquire):
  +-> Client가 풀에 객체 요청
     +- IDLE 객체 존재 -> 즉시 반환
     +- IDLE 없음      -> 대기(Wait) 또는 타임아웃(Timeout) 후 예외

사용 (Use):
  +-> Client가 객체로 작업 수행

반납 (Release):
  +-> 객체를 IDLE 상태로 풀에 반환 (소멸 X)
     +-> 다음 대여자가 즉시 재사용
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 도서관 대출 시스템 — 책(객체)이 없어질 때마다 새로 인쇄하는 것이 아니라, 반납된 책을 다시 대출하는 방식으로 비용을 아낀다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+---------------------------------------------------------------+
|                    Object Pool Pattern                        |
|                                                               |
|  +-----------+  Acquire()   +----------------------------+   |
|  |  Client A |-------------->|         Object Pool        |   |
|  +-----+-----+              |  +------+ +------+         |   |
|        |                    |  | Obj1 | | Obj2 |  ...    |   |
|        | Use                |  |BUSY  | |IDLE  |         |   |
|        |                    |  +------+ +------+         |   |
|  +-----v-----+  Release()   |                            |   |
|  |  Client A |-------------->|  재사용 (소멸하지 않음)      |   |
|  +-----------+              +----------------------------+   |
|                                                               |
|  IDLE 없을 때:                                                 |
|  +-----------+              +----------------------------+   |
|  |  Client B |- Acquire() -->|  대기(Wait) or 타임아웃     |   |
|  +-----------+              +----------------------------+   |
+---------------------------------------------------------------+
```

| 파라미터 | 설명 | 기본값 |
|:---|:---|:---|
| `maximumPoolSize` | 풀 최대 커넥션 수 | 10 |
| `minimumIdle` | 항상 유지할 최소 IDLE 커넥션 | maximumPoolSize와 동일 |
| `connectionTimeout` | 커넥션 획득 대기 최대 시간 | 30,000ms |
| `idleTimeout` | IDLE 커넥션 유지 최대 시간 | 600,000ms |
| `maxLifetime` | 커넥션 최대 수명 | 1,800,000ms |
| `validationTimeout` | 커넥션 유효성 검사 시간 | 5,000ms |

```
Little's Law: L = λ × W
  L = 동시 사용 중인 평균 객체 수
  λ = 초당 요청 수 (도착률)
  W = 요청당 평균 처리 시간 (초)

예시:
  초당 100 요청, 평균 처리 시간 0.05초(50ms) -> DB 쿼리 포함
  L = 100 × 0.05 = 5 커넥션 (평균 동시 사용)
  풀 크기 권장 = L × 1.5 ~ 2 = 7~10 커넥션
```

- **📢 섹션 요약 비유**: 놀이공원 자전거 대여소 — 자전거(커넥션)는 항상 몇 대 준비(minIdle)되어 있고, 최대 N대(maximumPoolSize)까지만 대여. 모두 나가면 줄(대기)을 서다가 타임아웃(connectionTimeout)이 되면 "대여 불가"를 알린다.

---

## Ⅲ. 비교 및 연결
| 풀 유형 | 대상 객체 | 대표 구현체 | 특이사항 |
|:---|:---|:---|:---|
| Connection Pool | DB 커넥션 | HikariCP, c3p0, DBCP2 | 커넥션 유효성 검사 필수 |
| Thread Pool | 스레드 | `ThreadPoolExecutor` | 작업 큐 방식 |
| Object Pool (일반) | 고비용 객체 | Apache Commons Pool | 범용 풀 |
| ByteBuffer Pool | 메모리 버퍼 | Netty `PooledByteBufAllocator` | GC 압박 감소 목적 |
| Connection Pool (HTTP) | HTTP 커넥션 | `OkHttpClient`, `HttpClient` | Keep-Alive 활용 |

```
풀 객체 누수 시나리오:
  1. 대여 후 예외 발생 -> finally/close() 미호출 -> 영구 BUSY 상태
  2. 풀 크기 점점 감소 -> 결국 모든 요청 타임아웃

방지 전략:
  1. try-with-resources 강제 사용:
     try (Connection conn = pool.acquire()) {
         // 사용
     } // AutoCloseable.close() -> 자동 반납

  2. Leak Detection Timeout (HikariCP: leakDetectionThreshold):
     일정 시간 이상 체크아웃된 커넥션 -> 경고 로그 출력

  3. 커넥션 최대 수명 설정 (maxLifetime):
     DB 서버가 커넥션을 먼저 끊을 때 대비
```

- **📢 섹션 요약 비유**: 자동차 렌탈 회사에서 렌트한 차를 돌려주지 않으면(누수) 보유 차량이 점점 줄어들고, 결국 새 손님에게 "차 없음" — try-with-resources는 계약서에 "여행 끝나면 무조건 반납" 조항을 자동으로 넣는 것이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:postgresql://localhost:5432/mydb");
config.setMaximumPoolSize(10);        // 프로덕션에서는 부하 테스트 후 결정
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);   // 30초 대기 후 예외
config.setIdleTimeout(600000);        // 10분 IDLE 시 제거
config.setMaxLifetime(1800000);       // 30분 후 강제 갱신
config.setLeakDetectionThreshold(2000); // 2초 이상 미반납 시 경고

// PostgreSQL 권장: Hikari 공식 권장 풀 크기
// = (CPU 코어 수 × 2) + 유효 디스크 스핀들 수
```

| 비교 항목 | Object Pool Pattern | Flyweight Pattern |
|:---|:---|:---|
| 목적 | 생성 비용 절감 (재사용) | 메모리 절감 (공유) |
| 상태 | 상태 있음 (BUSY/IDLE) | 내재(Intrinsic) 상태만 공유 |
| 수명 주기 | 대여/반납 라이프사이클 | 영구 공유 (반납 없음) |
| 예시 | DB 커넥션 풀 | 문자 폰트, 아이콘 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: Flyweight는 "붕어빵 틀" — 틀(공유 상태)은 하나지만 반죽(외재 상태)을 바꿔가며 수천 개를 찍어낸다. Object Pool은 "텀블러 대여" — 대여(Acquire)하고 씻어서(정리 후) 반납(Release)하는 사용 사이클이 있다.

---

## Ⅴ. 기대효과 및 결론
Object Pool 패턴은 성능 최적화의 필수 도구이다:

**기대효과**:
- <strong>응답 지연 감소</strong>: 생성 비용 제거로 수십~수백 ms 절감
- <strong>처리량 증가</strong>: 객체 재사용으로 동일 자원에서 더 많은 요청 처리
- **자원 상한 제어**: 최대 연결 수 제한으로 외부 시스템 보호
- **GC 압박 감소**: 객체 생성/소멸 빈도 감소

**설계 시 주의사항**:
- 풀 객체 초기화 상태 보장 (반납 전 상태 초기화 필수)
- try-with-resources 또는 명시적 반납 강제
- 유효성 검사 (Validation): 네트워크 단절 후 재연결 감지
- 타임아웃 정책: 무한 대기 방지

심화 학습에서는 <strong>Little's Law를 이용한 풀 크기 계산</strong>과 <strong>누수 방지 전략</strong>(try-with-resources, leakDetectionThreshold)을 수치와 함께 제시하는 것이 고득점 포인트다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 객체 풀은 수영장 구명조끼 대여 시스템 — 미리 준비된 조끼(객체)를 빌려서(Acquire) 수영하고, 나오면 반납(Release) — 빌린 채로 집에 가면(누수) 다음 사람이 조끼 없이 물에 들어가야 한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 생성 패턴 (Creational Pattern) | 객체 생성 전략의 상위 범주 |
| 특화 유형 | Thread Pool Pattern | 스레드 객체를 풀로 관리하는 특수화 |
| 특화 유형 | Connection Pool | DB 커넥션 객체를 풀로 관리 |
| 연관 패턴 | Flyweight Pattern | 공유를 통한 메모리 절감 (반납 없음) |
| 구현체 | HikariCP | 고성능 JDBC Connection Pool |
| 측정 도구 | Little's Law | 최적 풀 크기 계산 공식 |
| 연관 개념 | try-with-resources | 자동 반납을 보장하는 Java 문법 |

### 📈 관련 키워드 및 발전 흐름도
재사용 자원 -> 객체 풀 패턴 -> 연결 풀·버퍼 풀

### 👶 어린이를 위한 3줄 비유 설명
1. 도서관에서 책(DB 커넥션)을 매번 새로 인쇄(생성)하는 게 아니라, 반납된 책을 다시 빌려주는 것이 객체 풀이야.
2. 빌린 책을 잃어버리면(누수) 도서관 책이 점점 줄어들어서 나중에는 아무도 못 빌려 — 그래서 try-with-resources라는 "자동 반납 규칙"이 있어.
3. 책 몇 권이 필요한지 계산하는 공식(Little's Law)은 "하루에 얼마나 많은 사람이 얼마나 오래 읽는지"를 보면 알 수 있어.
