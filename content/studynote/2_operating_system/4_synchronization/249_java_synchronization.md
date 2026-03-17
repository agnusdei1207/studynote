+++
title = "249. 자바 동기화"
date = "2026-03-04"
weight = 249
[extra]
categories = "studynote-operating-system"
+++

# 자바 동기화 (Java Synchronization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 자바는 JVM(Java Virtual Machine) 수준에서 **모니터(Monitor)** 메커니즘을 내장하고 있으며, `synchronized` 키워드를 통해 객체별로 단 하나의 스레드만 접근 가능한 상호 배제를 제공한다.
> 2. **가치**: 별도의 외부 라이브러리 없이 언어 수준에서 스레드 안전성(Thread Safety)을 보장하며, `wait/notify`를 통해 생산자-소비자와 같은 정교한 협력 모델을 쉽게 구현할 수 있다.
> 3. **융합**: 현대 자바 병행성 프레임워크(`java.util.concurrent`)의 기초가 되며, 성능 최적화를 위한 편향 락(Biased Lock), 경량 락(Lightweight Lock) 등 JVM 내부의 고도화된 기술이 집약되어 있다.

+++

## Ⅰ. 개요 (Context & Background)

- **개념**: 자바의 모든 객체는 내부적으로 **고유 락(Intrinsic Lock)** 또는 **모니터 락(Monitor Lock)**을 가지고 있다. `synchronized` 블록에 진입하는 스레드는 해당 객체의 락을 획득해야 하며, 이미 다른 스레드가 점유 중이면 대기 큐에서 기다린다. 이는 고수준 동기화 도구인 '모니터'의 교과서적인 구현이다.

- **💡 비유**: 자바 객체는 "개별 잠금장치가 달린 방"과 같다. `synchronized`는 그 방의 "문을 잠그는 행위"이고, 방 안에 들어가려는 모든 스레드는 오직 하나뿐인 "열쇠"를 차지하기 위해 경쟁해야 한다.

- **📢 섹션 요약 비유**: 마치 은행 창구에서 번호표를 뽑고 들어가 상담을 받는 동안, 다른 고객들은 번호표가 나올 때까지 대기석에서 기다리는 질서 있는 서비스 체계와 같습니다.

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### synchronized의 두 가지 사용법
1. **메서드 수준**: `public synchronized void method()` — 객체 전체를 잠금.
2. **블록 수준**: `synchronized(obj) { ... }` — 특정 객체(Lock Object)만 잠금. (범위를 최소화하여 성능에 유리)

### wait(), notify(), notifyAll() 협력 모델
이 함수들은 반드시 `synchronized` 블록 내부에서만 호출 가능하며, 객체의 **대기 셋(Wait Set)**을 관리한다.

```text
  [ Thread A ]                      [ Object Monitor ]                      [ Thread B ]
       |                                    |                                    |
  1. synchronized(obj)             [ Entry Set (A) ]                             |
  2. obj.wait()                    [ Wait Set (A)  ] ◀───(Lock Released)         |
       |                                    |                                    |
       |                                    |                            3. synchronized(obj)
       |                                    |                            4. obj.notify()
       |                           [ Entry Set (A) ] ◀───(A moved to Entry)      |
       |                                    |                            5. End sync
  6. Resume A ◀──────────────────── [ Lock Acquired ]                             |
```

**[다이어그램 해설]** `wait()`를 호출하면 스레드 A는 락을 놓고 'Wait Set'으로 들어간다. 스레드 B가 락을 잡고 `notify()`를 호출하면 'Wait Set'에 있던 A가 다시 락을 얻기 위해 'Entry Set'으로 이동한다. B가 락을 완전히 해제해야만 A가 다시 락을 잡고 `wait()` 다음 줄부터 실행을 재개한다.

- **📢 섹션 요약 비유**: 진료실(Monitor) 안에서 검사 결과가 나올 때까지 잠시 밖에서 대기(wait)하다가, 간호사가 이름을 부르면(notify) 다시 진료실로 들어가 상담을 이어가는 과정과 같습니다.

+++

## Ⅲ. 융합 비교 및 다각도 분석

### synchronized vs ReentrantLock (JUC 패키지)

| 비교 항목 | synchronized (고유 락) | ReentrantLock (명시적 락) |
|:---|:---|:---|
| **편의성** | 키워드 하나로 끝 (자동 해제) | `lock/unlock` 수동 관리 필요 |
| **유연성** | 낮음 (무조건 대기) | 높음 (tryLock, 타임아웃 지원) |
| **공정성** | 비공정 (순서 보장 안 됨) | 공정/비공정 선택 가능 |
| **성능** | 최신 JVM에서 매우 최적화됨 | 경합이 극심할 때 약간 더 유리 |

- **📢 섹션 요약 비유**: `synchronized`는 건물의 '중앙 제어 시스템'이고, `ReentrantLock`은 사용자가 직접 세밀하게 조절하는 '스마트 홈 제어 앱'입니다.

+++

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오: 싱글톤 패턴 (Double-Checked Locking)
- **상황**: 멀티스레드 환경에서 싱글톤 인스턴스를 하나만 생성해야 함.
- **해결책**:
  ```java
  if (instance == null) {
      synchronized (Singleton.class) {
          if (instance == null) {
              instance = new Singleton();
          }
      }
  }
  ```
  이때 `instance` 변수는 반드시 `volatile`로 선언하여 메모리 가시성 문제를 방지해야 한다.

### 도입 체크리스트
- **Monitor Size**: 너무 큰 객체를 락으로 잡고 있지 않은가? (병목 원인)
- **Deadlock**: 서로 다른 객체의 락을 엇갈려 잡는 코드가 있는가?

- **📢 섹션 요약 비유**: 락의 범위를 좁게 잡는 것은 건물 전체를 폐쇄하지 않고 문제의 방만 폐쇄하여 다른 사람들의 활동을 보장하는 지혜와 같습니다.

+++

## Ⅴ. 기대효과 및 결론

- **기대효과**: 자바 동기화는 복잡한 병렬 프로그래밍을 대중화시켰으며, 엔터프라이즈급 서버 애플리케이션의 안정적인 토대가 되었다.
- **미래 전망**: Project Loom의 가상 스레드(Virtual Thread) 도입으로, 기존의 무거운 커널 스레드 기반 동기화 방식이 사용자 수준의 경량 동기화로 전환되며 성능이 획기적으로 향상될 것이다.

- **📢 섹션 요약 비유**: 기초가 튼튼한 집이 폭풍에도 안전하듯, 자바의 견고한 모니터 모델은 수많은 트래픽에도 흔들리지 않는 소프트웨어를 만듭니다.