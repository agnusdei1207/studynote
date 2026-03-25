+++
title = "254. RCU (Read-Copy-Update)"
date = "2026-03-22"
[extra]
categories = ["studynote-operating-system"]
+++

# RCU (Read-Copy-Update)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RCU (Read-Copy-Update)는 독자(Reader)에게 락 없이 읽기를 허용하고, 저자(Writer)는 데이터의 복사본을 수정한 뒤 포인터 교체로 업데이트하여, 독자와 저자가 서로를 차단하지 않는 리눅스 커널 핵심 동기화 기법이다.
> 2. **가치**: SMP (Symmetric Multiprocessing) 환경에서 수천 개의 CPU가 동시에 같은 데이터를 읽을 수 있으며, 읽기 경로의 오버헤드가 사실상 0에 가깝다. 리눅스 커널에서 수천 개 코드 경로에 적용된다.
> 3. **융합**: RCU는 독자-저자 문제 (Readers-Writers Problem)의 산업적 해법이며, 가비지 콜렉션의 "시대 기반 회수" (epoch-based reclamation), Rust의 Arc 소유권 모델과 깊이 연결된다.

---

## Ⅰ. 개요 및 필요성

리눅스 커널의 핵심 자료구조(라우팅 테이블, 프로세스 목록, 파일 시스템 마운트 정보)는 읽기가 쓰기보다 수백 배 빈번하다. 전통적인 ReadWriteLock조차 읽기 측 오버헤드(원자적 카운터 증감)가 존재하고, SMP 환경에서 캐시라인 경합을 유발한다.

RCU는 이 문제를 근본적으로 해결한다. 읽기는 완전한 락 프리 (Lock-Free)로, 쓰기는 복사→수정→포인터 교체→유예 기간(Grace Period) 후 원본 해제의 4단계로 처리한다.

**💡 비유**: 도서관에서 책을 빌려주는 방법 중 가장 혁신적인 방법 — 새 버전 책이 나오면(저자), 기존 책을 빌려간 사람들(독자)이 모두 반납할 때까지 원본을 보존하고, 새 사람들에게는 새 버전을 준다.

```text
┌───────────────────────────────────────────────────────────────┐
│            RCU 동작 원리: Read-Copy-Update 4단계              │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  초기 상태:                                                   │
│  ptr ──▶ [Data: A=1, B=2]                                     │
│                                                               │
│  ① READ 단계 (독자 = 락 없음):                                │
│  rcu_read_lock()                 // 선점 방지만               │
│  data = rcu_dereference(ptr)     // 현재 포인터 읽기          │
│  use(data->A)                    // 안전하게 읽기 가능        │
│  rcu_read_unlock()                                            │
│                                                               │
│  ② COPY 단계 (저자):                                          │
│  new_data = kmalloc(sizeof(*ptr))                             │
│  *new_data = *ptr               // 원본 복사                  │
│  new_data->A = 99               // 복사본 수정                │
│                                                               │
│  ③ UPDATE 단계 (저자):                                        │
│  rcu_assign_pointer(ptr, new_data) // 포인터 원자적 교체      │
│  → 신규 독자는 new_data 읽음                                  │
│  → 기존 독자는 여전히 old_data 읽음 (안전!)                   │
│                                                               │
│  ④ RECLAIM 단계:                                              │
│  synchronize_rcu()              // Grace Period 대기          │
│  kfree(old_data)                // 모든 기존 독자 완료 후 해제│
└───────────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: RCU는 고속도로 도로 공사와 같습니다 — 기존 차선(원본)을 유지한 채 새 차선(복사본)을 다 닦은 다음, 신호를 바꿔 새 차선으로 유도하고, 기존 차선의 차들이 모두 빠져나가면 기존 차선을 철거합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Grace Period (유예 기간) 메커니즘

Grace Period는 RCU의 가장 중요한 개념이다. 저자가 포인터를 교체한 후, 교체 시점에 실행 중이던 모든 독자가 rcu_read_unlock()을 완료할 때까지의 기간이다. 이 기간이 끝나야 원본을 안전하게 해제할 수 있다.

```text
┌────────────────────────────────────────────────────────────────┐
│            Grace Period 타이밍 다이어그램                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  시간 ──────────────────────────────────────────────────▶      │
│                                                                │
│  Writer: [복사수정] ─[포인터교체]─────[synchronize_rcu]──[해제]│
│                          ↑                           ↑         │
│                     새 ptr 공개                Grace Period 끝 │
│                                                                │
│  Reader1: ──[rcu_read_lock]──────────[rcu_read_unlock]         │
│           (교체 전 시작, old_data 읽음)  (Grace Period 기여)   │
│                                                                │
│  Reader2:          ──[rcu_read_lock]─[rcu_read_unlock]         │
│                    (교체 후 시작, new_data 읽음)               │
│                                                                │
│  Reader3:                 ──[rcu_read_lock]─────...            │
│                           (교체 후 시작, new_data 읽음)        │
│                                                                │
│  Grace Period: Reader1 완료 → 해제 안전                        │
└────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Grace Period의 핵심은 "교체 시점에 이미 읽고 있던 독자"가 모두 완료될 때까지만 기다리면 된다는 점이다. 교체 이후에 시작한 독자(Reader2, Reader3)는 이미 new_data를 읽으므로 Grace Period 계산에 포함되지 않는다. 리눅스는 각 CPU의 선점 포인트(context switch, 인터럽트 처리 완료)를 Quiescent State(정지점)로 사용하여, 모든 CPU가 최소 1번 Quiescent State를 통과하면 Grace Period가 완료다.

### API 사용 패턴

```c
// 독자 측 (Reader) — 선점이 비활성화되는 것만으로 충분
rcu_read_lock();
entry = rcu_dereference(list_head);  // 메모리 배리어 포함
if (entry)
    process(entry->value);
rcu_read_unlock();

// 저자 측 (Writer) — 기존 항목 교체
struct entry *new = kmalloc(...);
new->value = 42;
old = rcu_dereference_protected(ptr, lockdep_is_held(&update_lock));
rcu_assign_pointer(ptr, new);  // 메모리 배리어 포함한 원자적 교체
synchronize_rcu();             // Grace Period 대기 (차단)
kfree(old);                    // 안전한 해제

// 비동기 해제 (차단 없음)
call_rcu(&old->rcu_head, free_callback);
```

**📢 섹션 요약 비유**: rcu_read_lock은 '현재 시대의 책을 읽는 중' 표시판 — 저자는 이 표시판이 모두 내려갈 때까지 기다렸다가 책을 폐기합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### RCU vs ReadWriteLock 비교

```text
┌──────────────────────┬──────────────────┬───────────────────────┐
│ 항목                 │ ReadWriteLock    │ RCU                   │
├──────────────────────┼──────────────────┼───────────────────────┤
│ 독자 오버헤드        │ 원자적 카운터 증감│ 사실상 0 (선점 비활) │
│ 독자-저자 차단       │ 있음 (쓰기 시)   │ 없음                  │
│ 저자 대기            │ 독자 완료 시     │ Grace Period          │
│ 데이터 일관성        │ 즉시 반영        │ 버전 분기 (일시적)    │
│ 메모리 오버헤드      │ 낮음             │ 복사본 임시 유지      │
│ 사용 적합성          │ 단순 R/W 분리    │ 읽기 집중 SMP 환경    │
└──────────────────────┴──────────────────┴───────────────────────┘
```

### 리눅스 커널 RCU 적용 사례
- **라우팅 테이블**: 네트워크 패킷 포워딩 경로 (RCU 읽기 수백만 회/초)
- **프로세스 목록**: `task_list` 순회 (`for_each_process()`)
- **VFS 덴트리 캐시**: 파일 경로 조회 고속화

**📢 섹션 요약 비유**: RCU는 독자-저자 문제에서 '읽기 차선'과 '쓰기 차선'을 완전히 분리한 고속도로 설계 — 읽기 차선에는 신호등이 없어 항상 전속력으로 달릴 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오
1. **DNS 조회 캐시**: 읽기가 압도적(수만 QPS), 쓰기는 TTL 만료 시만 발생. RCU로 읽기 경로 오버헤드 제거.
2. **공유 설정 객체**: 마이크로서비스가 공유 설정을 빈번히 읽고 관리자가 드물게 업데이트. RCU 패턴으로 읽기 성능 최대화.

### 안티패턴
- **Grace Period 전 해제**: `synchronize_rcu()` 없이 원본 해제 → 기존 독자가 해제된 메모리 접근 → Use-After-Free.
- **rcu_read_lock 중 스케줄링**: `rcu_read_lock()` 구간에서 `schedule()` 호출 → RCU 규칙 위반 (해당 CPU가 Quiescent State로 진입하지 않아 Grace Period 지연).

**📢 섹션 요약 비유**: Grace Period를 지키지 않은 RCU는 새 책을 출판했지만 도서관에서 구 책을 아직 읽고 있는 독자가 있는데 불태워버리는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | ReadWriteLock | RCU |
|:---|:---|:---|
| 읽기 처리량 | 코어 수 증가 시 경합 | 선형 확장 |
| 캐시라인 경합 | 카운터로 발생 | 없음 |
| 저자 레이턴시 | 즉시 반영 | Grace Period만큼 지연 |

RCU는 SMP 시스템에서 읽기 집중형 자료구조의 표준 동기화 기법으로 자리잡았다. 단, 저자 측에 일시적 메모리 오버헤드와 복잡한 메모리 배리어 관리가 요구된다.

---

## 📌 관련 개념 맵

| 개념 | 관계 |
|:---|:---|
| 독자-저자 문제 | RCU가 해결하는 핵심 동기화 패턴 |
| Grace Period | RCU 정확성의 핵심 타이밍 개념 |
| Quiescent State | Grace Period 종료 감지 메커니즘 |
| 메모리 배리어 | rcu_dereference/rcu_assign_pointer의 정확성 보장 |
| Epoch-based Reclamation | RCU 원리의 일반화된 메모리 관리 기법 |

## 👶 어린이를 위한 3줄 비유 설명
1. RCU는 도서관 신간 교체 방식 — 새 책이 나왔을 때, 기존 책을 빌려간 사람들이 모두 반납할 때까지 버리지 않아요.
2. 독자는 책을 빌릴 때 아무런 절차 없이(락 없이) 가져갈 수 있어요 — 항상 안전한 책이 보장됩니다.
3. 모든 기존 독자가 반납하면(Grace Period 완료), 그때서야 낡은 책을 안전하게 폐기해요!
