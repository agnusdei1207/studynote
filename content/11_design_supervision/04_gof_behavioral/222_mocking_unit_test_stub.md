---
title: "Mocking / Unit Test / Test Double"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 222
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Test Double (테스트 더블)은 외부 의존성(DB, 네트워크, 외부 API)을 가짜(Fake) 객체로 대체하여, 테스트 대상 코드(SUT, System Under Test)만을 순수하게 검증하는 단위 테스트(Unit Test) 격리 기법이다.
> 2. **가치**: 외부 시스템 없이도 빠르고(ms 단위) 신뢰성 있는 테스트를 실행할 수 있어, TDD(Test-Driven Development)와 CI/CD 파이프라인의 기반이 된다.
> 3. **판단 포인트**: Stub은 "반환 값을 미리 지정", Mock은 "호출 여부/인수를 검증" — 두 개념의 차이를 명확히 구분하는 것이 테스트 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성
단위 테스트의 이상(Ideal): 테스트 대상 코드만 테스트한다.

현실: 비즈니스 로직이 DB, 외부 API, 파일 시스템 등에 의존한다.

```
[문제 상황]
OrderService.createOrder()
  +-> userRepository.findById()   <- DB 의존성
  +-> inventoryService.reserve()  <- 외부 서비스 의존성
  +-> emailService.send()         <- SMTP 서버 의존성

단위 테스트만으로 실행 불가:
  - DB 없이 실행 불가 -> 느림, 불안정
  - 외부 API 없이 실행 불가 -> 환경 의존
  - 이메일 실제 발송 -> 테스트 부작용
```

해결: 의존성을 <strong>Test Double</strong>로 교체하여 격리.

```
        /\
       /  \
      / E2E\  <- End-to-End 테스트 (소수, 느림, 비용 ^)
     /------\
    /Integra-\<- 통합 테스트 (중간)
   /----------\
  / Unit Tests \<- 단위 테스트 (다수, 빠름, 비용 v)
 ----------------
```

단위 테스트가 피라미드 기반을 이루는 이유:
- 실행 속도: ms 단위 (외부 I/O 없음)
- 피드백 속도: 코드 수정 즉시 검증
- 유지보수 비용: 외부 환경 변화에 무관

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 테스트 더블은 영화 촬영의 스턴트맨 — 진짜 배우(실제 DB, 외부 서비스) 대신 특정 장면(테스트)에서 대역(Test Double)을 써서, 안전하고 빠르게 촬영(테스트)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 유형 | 설명 | 검증 여부 | 사용 목적 | 예시 |
|:---|:---|:---|:---|:---|
| <strong>Dummy</strong> (더미) | 전달만 되고 사용 안 됨 | ✗ | 파라미터 채우기 | `null`, 빈 객체 |
| <strong>Stub</strong> (스텁) | 미리 정해진 값 반환 | ✗ | 간접 입력 제공 | `when(repo.find()).thenReturn(user)` |
| <strong>Spy</strong> (스파이) | 실제 객체이지만 일부 호출 기록 | ○ 일부 | 호출 사실 확인 | `@Spy` (Mockito) |
| <strong>Mock</strong> (목) | 호출 예상(Expectation) 설정 + 검증 | ✓ | 상호작용 검증 | `verify(emailSvc, times(1)).send(any())` |
| <strong>Fake</strong> (페이크) | 실제 구현의 단순화 버전 | ✗ | 경량 실제 구현 | `InMemoryRepository` |

```
테스트에서 의존성을 어떻게 다룰까?
                |
    +-----------+----------------+
    |           |                |
파라미터로      반환 값이          호출 여부를
전달만 됨      필요함             검증해야 함
    |           |                |
  Dummy       상태가 필요?      Mock 사용
              (경량 구현 필요?)
             +-----+------+
          단순 값          실제 동작
         반환 충분          필요
             |                |
           Stub             Fake
```

```java
// 1. Mock 생성
UserRepository mockRepo = mock(UserRepository.class);

// 2. Stub 설정 (반환 값 지정)
User testUser = new User(1L, "Alice");
when(mockRepo.findById(1L)).thenReturn(Optional.of(testUser));

// 3. 테스트 대상 실행
OrderService sut = new OrderService(mockRepo, mockEmailService);
Order result = sut.createOrder(1L, "PRODUCT-001");

// 4. 결과 검증 (Assert)
assertThat(result.getStatus()).isEqualTo(OrderStatus.CREATED);

// 5. 상호작용 검증 (Verify — Mock의 핵심)
verify(mockEmailService, times(1)).sendConfirmation(eq(testUser.getEmail()));
verify(mockRepo, never()).delete(any());
```

```text
+--------------+    +--------------+    +--------------+
| Input/State  |--->| Control Point |--->| Output/Action |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: Stub은 "미리 짜놓은 대본을 읽는 배우(항상 같은 답변 반환)", Mock은 "감독이 배우가 대본대로 연기했는지 확인하는 것(호출 검증)" 이다.

---

## Ⅲ. 비교 및 연결
```java
@Test
void 주문_생성_시_이메일_발송된다() {
    // Given (준비): 테스트 환경 설정
    User user = new User(1L, "alice@example.com");
    when(userRepo.findById(1L)).thenReturn(Optional.of(user));
    when(inventory.reserve("PROD-1", 1)).thenReturn(true);

    // When (실행): 테스트 대상 실행
    Order order = orderService.createOrder(1L, "PROD-1", 1);

    // Then (검증): 결과 및 상호작용 검증
    assertThat(order.getStatus()).isEqualTo(OrderStatus.CREATED);
    verify(emailService).sendConfirmation(user.getEmail(), order.getId());
}
```

| 항목 | 단위 테스트 (Unit) | 통합 테스트 (Integration) | E2E 테스트 |
|:---|:---|:---|:---|
| 범위 | 클래스/메서드 단위 | 모듈/서비스 간 | 전체 시스템 |
| 외부 의존성 | Test Double 사용 | 실제 DB/서버 일부 사용 | 모두 실제 |
| 실행 속도 | ms 단위 | 초 단위 | 분 단위 |
| 신뢰도 | 낮음 (격리됨) | 중간 | 높음 |
| 작성 비용 | 낮음 | 중간 | 높음 |
| 비율 권장 | 70% | 20% | 10% |

```java
// 실제 DB 컨테이너를 테스트 중에 자동으로 시작/종료
@Testcontainers
class UserRepositoryIntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:15-alpine");

    @Test
    void 사용자_저장_및_조회() {
        // 실제 PostgreSQL에 대한 통합 테스트
    }
}
```

- **📢 섹션 요약 비유**: 단위 테스트는 레고 블록 하나 검사, 통합 테스트는 블록을 조립한 구조물 검사, E2E 테스트는 완성된 레고 성에서 실제로 놀아보는 것이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock
    UserRepository userRepo;       // Mock 자동 생성

    @Mock
    EmailService emailService;

    @InjectMocks
    OrderService orderService;     // 의존성 자동 주입

    @Captor
    ArgumentCaptor<String> emailCaptor; // 전달된 인수 캡처

    @Test
    void 신규_사용자_주문_시_환영_이메일_발송() {
        // Given
        when(userRepo.findById(99L)).thenReturn(Optional.of(new User(99L, "new@test.com", true)));

        // When
        orderService.createOrder(99L, "ITEM-1");

        // Then — 캡처된 인수 검증
        verify(emailService).send(emailCaptor.capture());
        assertThat(emailCaptor.getValue()).contains("환영합니다");
    }
}
```

| 원칙 | 나쁜 설계 | 좋은 설계 |
|:---|:---|:---|
| 의존성 주입 | `new EmailService()` 직접 생성 | 생성자 주입으로 외부 주입 |
| 인터페이스 분리 | 구체 클래스 직접 참조 | 인터페이스 참조 |
| 정적 메서드 제거 | `static` 유틸 직접 호출 | 서비스 인터페이스로 래핑 |
| 단일 책임 | 하나의 메서드에 모든 로직 | 분리 -> 독립 테스트 가능 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 테스트하기 좋은 코드는 레고 — 부품(의존성)을 끼웠다 뺄 수 있어서 부품 하나만 따로 검사(Test Double 교체)할 수 있다. 반대로 고정 접착(new 직접 생성)은 부품을 분리해 검사할 수 없다.

---

## Ⅴ. 기대효과 및 결론
모킹과 단위 테스트는 고품질 소프트웨어의 기반이다:

**기대효과**:
- **빠른 피드백**: 외부 의존성 없이 ms 내 실행
- <strong>안정적인 CI/CD</strong>: 환경 의존 없이 일관된 결과
- <strong>리팩토링 안전망</strong>: 코드 변경 시 회귀 방지
- **설계 개선 유도**: 테스트 어렵다 -> 결합도가 높다는 신호

**한계와 주의**:
- 지나친 Mock 사용 -> 구현 세부사항에 결합된 취약한 테스트
- Stub과 Mock의 혼동 -> 상태 검증인지 행동 검증인지 목적 불명확
- 단위 테스트만으로는 통합 문제 미탐지 -> 피라미드 균형 유지 필수

심화 학습에서는 <strong>5가지 Test Double 비교표</strong>, <strong>Stub vs Mock의 차이</strong>, <strong>테스트 피라미드</strong>를 명확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 단위 테스트는 자동차 공장의 부품별 품질 검사 — 엔진(핵심 로직)이 정상인지 확인하기 위해 차체(DB, 네트워크) 없이 엔진만 꺼내서 검사대(Test Double)에 올려놓고 가동해본다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | TDD (Test-Driven Development) | 테스트 먼저 작성하는 개발 방법론 |
| 핵심 기법 | Test Double | Dummy/Stub/Spy/Mock/Fake의 총칭 |
| 구현 도구 | Mockito | Java 대표 Mock 프레임워크 |
| 구현 도구 | JUnit5 | Java 표준 테스트 프레임워크 |
| 연관 개념 | 의존성 주입 (DI) | Test Double 교체를 가능하게 하는 설계 |
| 연관 도구 | Testcontainers | 실제 컨테이너를 이용한 통합 테스트 |
| 연관 개념 | 테스트 피라미드 | Unit/Integration/E2E 비율 가이드 |

### 📈 관련 키워드 및 발전 흐름도
테스트 격리 -> 모킹과 단위 테스트 -> 계약 테스트

### 👶 어린이를 위한 3줄 비유 설명
1. Mock은 영화 촬영에서 진짜 폭발 대신 쓰는 가짜 폭발 효과 — 진짜(DB, 외부 API) 없이도 실제처럼 테스트할 수 있어.
2. Stub은 "이 번호로 전화하면 항상 '안녕하세요'라고 대답하는 녹음 안내" — 미리 답변을 정해두고 테스트할 수 있어.
3. Mock은 "감독이 배우가 대본대로 말했는지 확인하는 것" — 단순히 결과만 보는 게 아니라 어떻게 실행됐는지(verify)도 검증한다는 점이 Stub과 달라.
