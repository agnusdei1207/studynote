+++
title = "251. 윈도우 동기화 (Windows Synchronization)"
date = "2026-03-22"
[extra]
categories = ["studynote-operating-system"]
+++

# 윈도우 동기화 (Windows Synchronization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Windows 동기화는 유저 모드와 커널 모드 두 계층으로 나뉘며, Critical Section (유저 모드 스핀락+뮤텍스 혼합), Mutex/Semaphore/Event (커널 모드 디스패처 객체)로 성능과 기능을 분리한다.
> 2. **가치**: 커널 모드 디스패처 객체는 프로세스 간 공유와 Wait 통지를 지원하며, SRWLOCK (Slim Reader/Writer Lock)과 CONDITION_VARIABLE은 Vista 이후 저비용 고성능 동기화를 제공한다.
> 3. **융합**: Windows I/O Completion Port (IOCP)는 비동기 I/O와 스레드 풀 동기화를 결합한 거대 규모 서버 설계의 핵심이며, ETW (Event Tracing for Windows)로 동기화 병목을 실시간 모니터링할 수 있다.

---

## Ⅰ. 개요 및 필요성

Windows NT 커널은 설계 초기부터 멀티프로세서 환경을 지원하도록 설계됐다. 동기화는 두 계층으로 분리됐는데, 유저 모드 객체는 커널 호출 없이 빠르게 동작하고, 커널 모드 객체는 프로세스 경계를 넘는 동기화와 다양한 대기 패턴을 지원한다.

**💡 비유**: Critical Section은 같은 건물 내 내부 출입문 자물쇠(빠르지만 건물 밖 불가), Kernel Mutex는 외부와도 공유할 수 있는 공식 계약서(느리지만 강력)다.

```text
┌──────────────────────────────────────────────────────────┐
│          Windows 동기화 객체 계층                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [유저 모드 — 빠른 경량 객체]                            │
│  ● Critical Section (CRITICAL_SECTION)                   │
│    - 스핀 후 커널 Mutex로 전환하는 혼합 방식             │
│  ● SRWLOCK (Slim Reader/Writer Lock) — Vista+            │
│    - 포인터 1개 크기, 읽기-쓰기 분리                     │
│  ● CONDITION_VARIABLE — Vista+                           │
│    - POSIX 조건 변수와 유사한 고수준 대기                 │
│                                                          │
│  [커널 모드 — 프로세스 간 공유 가능]                     │
│  ● Mutex — 소유권 있는 상호 배제                        │
│  ● Semaphore — 카운팅 세마포어                           │
│  ● Event — 수동/자동 리셋 신호 객체                      │
│  ● WaitableTimer — 타이머 기반 동기화                    │
│  ● FileMapping — 공유 메모리 동기화                      │
└──────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: Windows 동기화는 사내 규정과 법적 계약 두 종류 — 사내 규정(Critical Section)은 빠르지만 회사 내부만, 법적 계약(Kernel 객체)은 느리지만 외부와도 유효합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Critical Section — 유저 모드 혼합 락

```c
CRITICAL_SECTION cs;
InitializeCriticalSectionAndSpinCount(&cs, 4000); // 스핀 횟수

EnterCriticalSection(&cs);   // 락 획득 (스핀 → 커널 Mutex)
// 임계 구역
LeaveCriticalSection(&cs);   // 락 해제

DeleteCriticalSection(&cs);  // 리소스 반환
```

Critical Section은 먼저 유저 공간에서 스핀락을 시도하고, 스핀 횟수 초과 시에만 커널 뮤텍스(내부 Event 객체)로 전환한다. 단일 프로세스 내 스레드 간 동기화에만 사용 가능하며, 프로세스 경계를 넘을 수 없다.

### 커널 모드 Mutex / Event

```c
// 이름 있는 Mutex (프로세스 간 공유)
HANDLE hMutex = CreateMutex(NULL, FALSE, L"Global\\MyMutex");
WaitForSingleObject(hMutex, INFINITE);   // 락 획득
// 임계 구역
ReleaseMutex(hMutex);
CloseHandle(hMutex);

// Event 객체 (스레드 간 신호 전달)
HANDLE hEvent = CreateEvent(NULL,   // 보안
                             TRUE,   // 수동 리셋 여부
                             FALSE,  // 초기 상태 (비신호)
                             NULL);  // 이름
SetEvent(hEvent);    // 수동: 모든 대기 스레드 깨움
ResetEvent(hEvent);  // 비신호 상태로 복원
```

```text
┌──────────────────────────────────────────────────────────────┐
│         자동 리셋 Event vs 수동 리셋 Event                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  자동 리셋 (Auto-Reset):                                    │
│  SetEvent() → 대기 스레드 1개만 깨우고 자동으로 비신호 복원 │
│  → 세마포어 signal과 유사 동작                              │
│                                                              │
│  수동 리셋 (Manual-Reset):                                   │
│  SetEvent() → 모든 대기 스레드 동시에 깨움                  │
│  ResetEvent() 호출 전까지 신호 유지                          │
│  → 조건 변수의 broadcast와 유사 동작                        │
│                                                              │
│  실무 예시:                                                  │
│  자동: 작업 큐 항목 추가 알림 (1명씩 처리)                  │
│  수동: 시스템 종료 신호 (모든 스레드에 동시 전파)           │
└──────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Event 객체의 자동/수동 리셋 구분은 notify() vs notifyAll()과 정확히 대응한다. 자동 리셋은 생산자-소비자에서 하나의 소비자만 깨워야 할 때, 수동 리셋은 서버 종료 신호처럼 모든 스레드에 브로드캐스트해야 할 때 사용한다.

### WaitForMultipleObjects — 다중 객체 대기

```c
HANDLE handles[2] = { hMutex, hEvent };
DWORD dwResult = WaitForMultipleObjects(2,          // 객체 수
                                         handles,    // 배열
                                         FALSE,      // OR 대기 (어느 하나)
                                         5000);      // 5초 타임아웃
switch (dwResult) {
    case WAIT_OBJECT_0:     /* hMutex 신호 */ break;
    case WAIT_OBJECT_0+1:   /* hEvent 신호 */ break;
    case WAIT_TIMEOUT:      /* 타임아웃 */    break;
}
```

**📢 섹션 요약 비유**: WaitForMultipleObjects는 여러 출구 중 먼저 열리는 곳으로 나가는 대기 체계 — 어느 자원이든 먼저 사용 가능해지면 즉시 잡는 효율적 방식입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### Critical Section vs Mutex 비교

```text
┌─────────────────────┬────────────────────┬────────────────────┐
│ 항목                │ Critical Section   │ Kernel Mutex       │
├─────────────────────┼────────────────────┼────────────────────┤
│ 동작 모드           │ 유저+커널 혼합     │ 커널 모드          │
│ 프로세스 간 공유    │ 불가               │ 가능               │
│ 타임아웃            │ 불가               │ 가능               │
│ 성능 (무경쟁)       │ ~25ns              │ ~500ns             │
│ 폐기 처리           │ DeadLock 후 복구불가│ WaitForSingleObject 타임아웃│
│ 소유권 추적         │ 있음 (재진입 가능) │ 있음               │
└─────────────────────┴────────────────────┴────────────────────┘
```

**📢 섹션 요약 비유**: Critical Section이 스피드게이트(빠르지만 건물 내부만), Kernel Mutex가 정식 경비 부스(느리지만 어디서나 유효)입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오
1. **SQL Server 내부 락**: Critical Section으로 버퍼 풀 접근을, Kernel Mutex로 파일 핸들 공유를 각각 분리 관리하여 성능 최적화.
2. **Windows 서비스 종료**: 수동 리셋 Event로 모든 워커 스레드에 종료 신호를 동시 전파, WaitForMultipleObjects로 완료 확인.

### 안티패턴
- **Critical Section 중에 대기 함수 호출**: CS 보유 중 `WaitForSingleObject` 호출 → 교착 상태. CS는 반드시 최소 범위로 유지.
- **CloseHandle 누락**: Kernel 객체 핸들을 닫지 않으면 커널 객체가 레퍼런스 카운트에 의해 누수.

**📢 섹션 요약 비유**: Windows 핸들은 빌린 열쇠 — 반드시 CloseHandle()로 반납해야 잠금장치(커널 객체)가 재사용될 수 있어요.

---

## Ⅴ. 기대효과 및 결론

Windows 동기화 설계는 유저 모드와 커널 모드의 분리를 통해 성능과 기능의 트레이드오프를 명확히 한다. 현대 Windows 개발에서는 SRWLock(읽기-쓰기)과 CONDITION_VARIABLE(조건 대기)을 Critical Section과 조합하는 것이 권장 패턴이다.

---

## 📌 관련 개념 맵

| 개념 | 관계 |
|:---|:---|
| Critical Section | Windows의 유저 모드 고성능 뮤텍스 |
| Futex (Linux) | Critical Section과 동일한 설계 철학 |
| Event 객체 | Windows의 조건 변수 대응 |
| WaitForMultipleObjects | 다중 자원 동시 대기 API |
| IOCP | Windows 비동기 I/O와 스레드 풀 동기화 결합 |

## 👶 어린이를 위한 3줄 비유 설명
1. Critical Section은 같은 반 안에서만 쓰는 내부 자물쇠 — 빠르지만 다른 반과 공유 불가.
2. Kernel Mutex는 선생님 도장이 찍힌 공식 출입증 — 느리지만 학교 전체(다른 프로세스)에서도 인정.
3. Event 객체는 '이제 들어와도 돼요' 신호등 — 자동 리셋은 한 명씩, 수동 리셋은 모두에게 신호!
