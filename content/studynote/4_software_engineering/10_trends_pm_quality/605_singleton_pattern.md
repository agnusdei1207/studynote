---
title: "605. 싱글톤 패턴(Singleton Pattern) 메모리/쓰레드 세이프 설계"
date: 2026-03-15
type: "pe_exam"
id: 605
---

# 605. 싱글톤 패턴(Singleton Pattern) 메모리/쓰레드 세이프 설계

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 싱글톤(Singleton) 패턴은 **"클래스의 인스턴스가 오직 하나만 생성됨을 보장"**하고, 전역 접근점(Global Access Point)을 제공하는 생성 패턴(Creational Pattern)이다.
> 2. **가치**: 데이터베이스 연결 풀(Connection Pool), 로거(Logger), 설정 관리자(Configuration Manager) 등 공유 자원(Resource) 관리에 필수적이나, 남용 시 전역 상태(Global State)로 인한 테스트 곤란(Testability Issue)를 유발한다.
> 3. **융합**: Spring Framework의 Singleton Bean, 서블릿(Servlet) 컨테이너, 싱글톤 레지스트리(Singleton Registry) 등 프레임워크의 기본 컴포넌트 스코프이며, 모듈 간 결합도(Coupling)를 높이는 부작용을 DIP(Dependency Inversion Principle)로 완화해야 한다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 싱글톤이란 무엇인가? 애플리케이션 전체에서 특정 클래스의 인스턴스가 딱 하나만 존재해야 하는 경우가 있다. 예를 들어, 데이터베이스 연결을 100개가 만들면 리소스가 낭비되고, 설정 파일을 5개의 객체가 동시에 읽으면 일관성이 깨진다. 싱글톤 패턴은 생성자(Constructor)를 private으로 선언하여 외부에서 new를 못하게 막고, 정적 메서드(static getInstance())를 통해 유일한 인스턴스를 반환하는 구조다.

- **💡 비유**: 싱글톤은 **"한 국가의 대통령"**과 같습니다. 나라 안에 대통령이 100명 있으면 혼란이 발생하겠죠? 그래서 헌법에 "대통령은 1인"이라고 명시하고(생성자 private), 선거를 통해 그 유일한 사람을 뽑는(getInstance) 절차를 정합니다. 누가든 대통령의 이름만 부르면(getInstance) 현재 대통령에게 연결되죠.

- **등장 배경**:
    1. **전역 변수(Global Variable)의 문제**: 전역 변수는 어디서든 접근 가능하지만, 타입 안정성(Type Safety)이 없고 초기화 시점을 제어하기 어렵다.
    2. **객체 생성 비용**: 비싼 객체(데이터베이스 연결, 소켓)를 반복 생성하면 메모리 낭비.
    3. **상태 공유 필요**: 여러 컴포넌트가 동일한 설정(Configuration)을 참조해야 할 때.

- **📢 섹션 요약 비유**: 도시에 시청 건물이 하나만 있어야 하듯, 시스템의 핵심 자원을 중앙 집중식으로 관리하여 불필요한 중복과 혼란을 방지하는 "중앙 집중 제어" 패턴입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 싱글톤 구성 요소

| 요소 | 역할 및 정의 | 기술적 구현 | 위배 시 증상 | 비유 |
|:---|:---|:---|:---|:---|
| **Private Constructor** | 외부 인스턴스화 차단 | `private ClassName()` | new 생성 가능 | 출입구 봉쇄 |
| **Static Instance** | 유일한 인스턴스 저장 | `private static volatile instance` | 다중 인스턴스 | 단 하나의 자리 |
| **Static Accessor** | 전역 접근점 제공 | `public static getInstance()` | 접근 불가 | 대통령실 연락처 |
| **Thread Safety** | 멀티스레드 환경 보장 | synchronized, DCL, Enum | Race Condition | 경비원 배치 |

#### [싱글톤 구현 방식 비교 다이어그램]

싱글톤을 구현하는 4가지 방식(Eager Initialization, Lazy Initialization, Synchronized, DCL, Enum)을 시각화한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Singleton Implementation Approaches                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Eager Initialization (조기 초기화)                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public class EagerSingleton {                                       │   │
│  │     private static final EagerSingleton instance = new EagerSingleton(); │   │
│  │     private EagerSingleton() {}                                     │   │
│  │     public static EagerSingleton getInstance() {                   │   │
│  │         return instance;  // 항상 생성됨                             │   │
│  │     }                                                              │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │  ✅ Thread-safe (final guarantees visibility)                       │   │
│  │  ❌ 인스턴스 미사용 시 메모리 낭비                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  2. Lazy Initialization (지연 초기화) - Thread-SAFE 하지 않음              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public class LazySingleton {                                       │   │
│  │     private static LazySingleton instance;                          │   │
│  │     private LazySingleton() {}                                      │   │
│  │     public static LazySingleton getInstance() {                    │   │
│  │         if (instance == null) {  // ⚠ Race Condition!           │   │
│  │             instance = new LazySingleton();                        │   │
│  │         }                                                          │   │
│  │         return instance;                                           │   │
│  │     }                                                              │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │  ✅ 필요할 때 생성                                                  │   │
│  │  ❌ 멀티스레드 환경에서 인스턴스 2개 이상 생성 가능                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  3. Synchronized Method (동기화 메서드)                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public class SyncSingleton {                                        │   │
│  │     private static SyncSingleton instance;                           │   │
│  │     private SyncSingleton() {}                                       │   │
│  │     public static synchronized SyncSingleton getInstance() {        │   │
│  │         if (instance == null) {                                    │   │
│  │             instance = new SyncSingleton();                         │   │
│  │         }                                                          │   │
│  │         return instance;                                           │   │
│  │     }                                                              │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │  ✅ Thread-safe                                                   │   │
│  │  ❌ 매 호출 시 동기화 오버헤드(성능 저하)                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  4. Double-Checked Locking (DCL, 이중 검사 잠금)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public class DCLSingleton {                                         │   │
│  │     private static volatile DCLSingleton instance;  // volatile!  │   │
│  │     private DCLSingleton() {}                                        │   │
│  │     public static DCLSingleton getInstance() {                      │   │
│  │         if (instance == null) {           // 1st check (no lock)   │   │
│  │             synchronized (DCLSingleton.class) {                     │   │
│  │                 if (instance == null) {   // 2nd check (with lock)│   │
│  │                     instance = new DCLSingleton();                  │   │
│  │                 }                                                  │   │
│  │             }                                                      │   │
│  │         }                                                          │   │
│  │         return instance;                                           │   │
│  │     }                                                              │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │  ✅ Thread-safe + 낮은 오버헤드                                   │   │
│  │  ⚠ Java 5+ volatile 필수 (메모리 가시성 보장)                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  5. Enum Singleton (Java 5+) - 권장 방법                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public enum EnumSingleton {                                         │   │
│  │     INSTANCE;                                                      │   │
│  │     // 메서드, 필드 추가 가능                                       │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │  ✅ Thread-safe (Java가 보장)                                      │   │
│  │  ✅ 직렬화(Serialization) 안전                                     │   │
│  │  ✅ 리플렉션(Reflection) 공격 방어                                  │   │
│  │  ⚠ 클래스 로딩 시점에 초기화 (Lazy 불가)                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상단 다이어그램은 싱글톤의 5가지 구현 방식과 장단점을 비교한다. Eager Initialization은 JVM이 클래스 로딩 시 즉시 인스턴스를 생성하므로 Thread-safe하지만, 미사용 시 메모리를 낭비한다. Lazy Initialization은 필요할 때 생성하지만, Race Condition으로 인해 멀티스레드 환경에서 인스턴스가 2개 이상 생성될 수 있다. Synchronized Method는 Thread-safe하나, 모든 호출에 동기화 비용이 든다. DCL은 최초 생성 시에만 동기화하고 이후에는 인스턴스를 반환하여 성능을 최적화한다. Enum 방식은 Java의 Enum이 Thread-safe를 보장하므로 가장 간단하고 안전하지만, 클래스 로딩 시점에 초기화되어 Lazy Loading이 불가능하다.

#### 심층 동작 원리: 메모리 모델과 volatile의 필요성

DCL(Double-Checked Locking)에서 `volatile` 키워드는 왜 필요한가? Java 5 이전에서는 volatile 없는 DCL이 작동하지 않았다. 이유는 **메모리 가시성(Memory Visibility)** 문제 때문이다. 스레드 A가 인스턴스를 생성하면, ① 메모리 할당 → ② 생성자 호출 → ③ instance 참조 할당 순으로 진행된다. JIT 컴파일러가 최적화를 위해 ②와 ③을 재배치(Instruction Reordering)할 수 있어, 스레드 B가 ③만 완료된 instance(null 아님, 초기화 안 됨)를 참조하여 오동작할 수 있다. `volatile`은 이 재배치를 금지하여(Memory Barrier), 모든 스레드가 완전히 초기화된 인스턴스를 보게 한다.

```
[volatile이 없는 경우의 Race Condition]

시간 T1: 스레드 A가 if (instance == null) 통과
시간 T2: 스레드 B가 if (instance == null) 통과
시간 T3: 스레드 A가 new Singleton() 생성 시작 (메모리 할당, 생성자 미호출)
시간 T4: 스레드 B가 new Singleton() 생성 시작 (두 번째 할당!)
시간 T5: 스레드 A가 생성자 호출 완료 후 instance에 할당
시간 T6: 스레드 B가 생성자 호출 완료 후 instance에 할당 (A의 객체를 잃어버림!)
결과: 싱글톤 파괴

[volatile이 있는 경우]

Memory Barrier에 의해:
- 스레드 A의 쓰기 연산이 volatile 변수에 대해 "happens-before" 관계 형성
- 스레드 B는 volatile 변수를 읽을 때 가장 최신 값을 보장받음
- 재배치(Reordering) 방지로 초기화 순서 보장
```

- **📢 섹션 요약 비유**: 대통령을 뽑을 때 선거관리 위원이 투표함을 감시하듯, volatile은 "메모리 감시관"이 되어서 모든 스레드가 동일한 시점에 완성된 대통령(인스턴스)을 보게 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 싱글톤 vs Static Class vs Spring Singleton

| 비교 항목 | 싱글톤(Singleton) | 정적 클래스(Static) | Spring Singleton |
|:---|:---|:---|:---|
| **객체지향** | OOP 가능 (인터페이스 구현) | OOP 불가 | OOP 가능 |
| **상속(Inheritance)** | 가능 | 불가능 | 가능 |
| **초기화 시점** | Lazy/Eager 선택 가능 | 클래스 로딩 시 | 컨테이너 시작 시 |
| **테스트 용이성** | 어려움 (Global State) | 어려움 | DI로 Mock 대체 가능 |
| **수명 주기 관리** | 개발자가 직접 관리 | JVM이 관리 | Spring이 관리 |
| **비유** | 유일한 대통령 | 헌법 전체 | 공장장이 임명한 관리자 |

#### 2. 싱글톤 남용의 문제점

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Singleton Anti-Patterns                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [문제 1] 전역 상태(Global State)                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public class GlobalConfig {                                         │   │
│  │     private static GlobalConfig instance = new GlobalConfig();      │   │
│  │     public Map<String, String> config = new HashMap<>();  // Public! │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │ 문제: 누구나 config에 접근하여 상태를 변경 가능                          │   │
│  │ 결과: 테스트 간 상태 오염(Test Contamination) 발생                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [문제 2] 의존성 주입(DI) 어려움                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ public class OrderService {                                         │   │
│  │     public void process() {                                        │   │
│  │         DatabaseConnection.getInstance().execute(...);  // 직접 호출│   │
│  │     }                                                              │   │
│  │ }                                                                  │   │
│  │                                                                     │   │
│  │ 문제: DatabaseConnection에 강하게 결합되어 Mock 대체 불가            │   │
│  │ 결과: 단위 테스트 시 실제 DB 연결 필요 (Testability 문제)              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [문제 3] 확장성(Extensability) 부족                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 문제: 싱글톤은 상속(Singleton subclassing)이 어려움                   │   │
│  │ 결과: 다른 구현(Development, Production)으로 교체 불가능            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [해결책]                                                                  │
│  - DI 컨테이너(Spring, Guice)에 싱글톤 관리 위임                              │
│  - 인터테이스(Interface)를 통한 접근                                       │
│  - 테스트 시 Profile별 Mock 구현체 사용                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 과목 융합 관점

- **운영체제(OS)**: 커널의 싱글톤 사례로는 프로세스 테이블(Process Table), 파일 시스템 레지스트리가 있다. OS는 전역 자원을 관리하기 위해 커널 모듈(Module)을 싱글톤으로 로드하며, 드라이버(Driver)도 싱글톤 패턴으로 장치별로 하나만 로드되는 경우가 많다.

- **분산 시스템(Distributed System)**: 분산 환경에서는 "진정한 싱글톤"이 불가능하다. 각 JVM(Java Virtual Machine)마다 독립적인 싱글톤이 생성되므로, 클러스터 환경에서는 Redis 같은 분산 캐시(Distributed Cache)를 활용하여 전역 상태를 관리해야 한다.

- **📢 섹션 요약 비유**: 왕국에 국왕이 한 명뿐이라도, 왕국이 여러 개의 대륙(클러스터)에 퍼져 있으면 각 대륙마다 국왕이 존재하게 됩니다. 이때는 대륙 간 연락(분산 캐시)이 필요한 것이죠.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **실무 시나리오 1: 설정 관리자의 싱글톤 구현**
    - **문제**: 애플리케이션 설정을 파일에서 로드하여 전역 공유 필요, 여러 곳에서 중복 로드 방지.
    - **의사결정**: Enum 싱글톤으로 구현하여 Thread-safe와 직렬화 안전성 확보.
    - **결과**: 설정 파일 변경 감시(File Watcher)와 결합하여 핫 리로드(Hot Reload) 기능 구현.

- **실무 시나리오 2: 데이터베이스 연결 풀**
    - **문제**: Connection Pool을 싱글톤으로 구현했으나, 테스트 시 H2(In-Memory DB)로 대체 어려움.
    - **의사결정**: 인터페이스(DataSource) 정의 후, Production은 HikariCP Singleton, Test는 MockDataSource로 DI.
    - **결과**: 싱글톤의 편리성과 테스트 용이성을 동시에 확보.

- **도입 체크리스트**:
    1. **정말 하나만 필요한가?**: 인스턴스가 2개 이상이면 논리적 오류가 발생하는가? (예: 설정 관리자)
    2. **전역 상태를 가지는가?**: 상태(State)가 없는 Stateless 클래스라면 Static Class 고려
    3. **DI 프레임워크 사용 가능?**: Spring의 @Bean, Guice의 @Singleton 활용
    4. **Thread-Safe 확인**: 멀티스레드 환경에서 DCL, Enum, volatile 적용

- **안티패턴**:
    - **Singleton as Global Variable**: 싱글톤을 전역 변수처럼 사용하여 결합도 증가.
    - **God Singleton**: 모든 기능을 담은 거대한 싱글톤 객체(SRP 위배).
    - **Singleton을 상속하려는 시도**: 싱글톤을 상속받는 자식 클래스는 결국 싱글톤이 아님.

- **📢 섹션 요약 비유**: 대통령제(싱글톤)는 효율적일 수 있지만, 독재(결합도 증가)의 위험이 있으므로, 입법부(DI 컨테이너)가 대통령의 권한을 제어하는 헌법적 장치(Interface)를 마련해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량/정성 기대효과**:

| 구분 | 싱글톤 미적용 시 | 싱글톤 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 리소스 객체 100개 생성 | 1개만 생성 | **메모리 사용량 99% 감소** |
| **정량** | 설정 파일 50번 중복 로드 | 1번만 로드 | **I/O 98% 감소** |
| **정성** | 전역 변수로 인한 결합도 | 캡슐화된 접근 | **모듈 독립성 향상** |
| **정성** | 상태 일관성 우려 | 중앙집중 관리 | **데이터 무결성 보장** |

- **미래 전망**:
    1. **DI 컨테이너의 싱글톤 관리**: Spring, Micronaut, Quarkus 등 현대 프레임워크는 싱글톤을 직접 구현하지 않고, 컨테이너에 위임한다.
    2. **애플리케이션 스코프(Application Scope) vs 요청 스코프(Request Scope)**: 웹 애플리케이션에서는 싱글톤(Application Scope) 대신 요청별 인스턴스(Request Scope)가 권장된다.

- **참고 표준**:
    - **Effective Java (Joshua Bloch)**: Item 3 - "싱글톤을 생성할 때는 private 생성자나 Enum 타입을 사용하라"
    - **Java Concurrency in Practice**: Chapter 16 - 싱글톤과 Thread-Safety
    - **Spring Framework Documentation**: @Bean, @Singleton 스코프

- **📢 섹션 요약 비유**: 과거에는 왕(싱글톤)이 모든 권력을 쥐었지만, 현대 민주주의(DI 컨테이너)에서는 국가가 대통령을 필요할 때마다 교체할 수 있는 임기제가 보편화되고 있습니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[생성 패턴(Creational Patterns)](./564_creational_patterns.md)**: 싱글톤이 속한 상위 카테고리.
- **[DIP(Dependency Inversion)](./601_solid_principles.md)**: 싱글톤의 결합도 문제를 완화하는 원칙.
- **[Thread-Safety](./323_multicore_synchronization.md)**: 싱글톤의 멀티스레드 안전성 보장 기법.
- **[DI 컨테이너](./337_dependency_injection.md)**: 싱글톤 관리를 위임하는 프레임워크.
- **[전역 변수 문제](./xx_global_state.md)**: 싱글톤 남용의 부작용.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 싱글톤은 학급에 **반장이 딱 한 명만 있는 것**과 같아요. 반장이 여러 명 있으면 누구의 말을 들어야 할지 혼란이 퍼지겠죠?
2. 그래서 선생님은 "반장은 이 친구다"라고 지정해두고, 친구들이 반장이 필요하면 그 친구를 찾아가게 해요(getInstance).
3. 하지만 반장이 너무 많은 일을 다 하면(책임이 많아지면), 친구들이 반장에게 너무 의지하게 돼서 혼자서는 아무것도 못 하게 될 수도 있어요(결합도 문제).
