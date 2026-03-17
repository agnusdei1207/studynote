+++
title = "248. 분산 트랜잭션 (Distributed Transaction) - 파편화된 원자성"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 248
+++

# 248. 분산 트랜잭션 (Distributed Transaction) - 파편화된 원자성

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 트랜잭션은 물리적으로 분리된 **둘 이상의 데이터베이스 노드나 서비스에 걸쳐 수행되는 작업들을 하나의 논리적인 단위(Atomic Unit)로 묶는 기술**이다.
> 2. **가치**: "전체가 성공하거나 전체가 실패해야 한다"는 원자성을 네트워크 너머의 시스템들 사이에서도 강제하여 데이터 불일치(Data Inconsistency) 위험을 방어한다.
> 3. **융합**: 마이크로서비스 아키텍처(MSA)의 확산과 함께 2단계 커밋(2PC)이나 사가(Saga) 패턴과 같은 고도의 조율 프로토콜과 결합되어 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
분산 트랜잭션은 단일 데이터베이스 내에서의 트랜잭션 처리를 넘어, 네트워크로 연결된 **이기종(Heterogeneous) 시스템** 또는 분산된 데이터 저장소에 대해 **ACID(Atomicity, Consistency, Isolation, Durability)** 특성을 보장하는 메커니즘입니다.
핵심은 분산 시스템의 고유한 특성인 **'부분 실패(Partial Failure)'** 환경에서도 데이터의 정합성을 유지하는 것입니다. 즉, 트랜잭션을 구성하는 여러 작업 중 하나라도 실패하면, 성공한 작업들까지 모두 취소하여 시스템을 실패 이전 상태로 되돌려야 합니다.

**💡 비유**
분산 트랜잭션은 **'여러 나라(서버)를 동시에 여행하는 일행'**과 같습니다. 일행 전체가 국경을 넘어 입국해야 하기 때문에, 한 명이라도 입국이 거부되면 전체 일행은 입국을 포기하고 출국 국가로 되돌아가야 합니다.

**2. 등장 배경: 단일 DB의 한계에서 분산 환경으로**
- **① 기존 한계**: 단일 장비(Monolith)로 처리 불가능한 대용량 트래픽 및 데이터 처리 요구 증가. 샤딩(Sharding)이나 MSA 도입으로 데이터가 물리적으로 분리됨.
- **② 혁신적 패러다임**: 네트워크 통신을 통해 분산된 노드들을 논리적으로 묶어주는 **분산 합의(Distributed Consensus)** 알고리즘의 등장. XA(eXtended Architecture) 표준 같은 프로토콜 정립.
- **③ 비즈니스 요구**: 금융(이체), 전자상거래(재고&주문), 항공 예약 등 데이터 정합성이 생명인 도메인에서의 강력한 무결성 요구.

**3. 기술적 난제**
네트워크 지연(Latency)과 통신 장애(Network Partition)로 인해 분산 트랜잭션은 로컬 트랜잭션보다 훨씬 복잡한 상태 관리가 필요합니다. 이로 인해 **CAP 정리(Consistency, Availability, Partition tolerance)**에 의거한 시스템 설계上的 트레이드오프가 필연적입니다.

> **📢 섹션 요약 비유**
> 분산 트랜잭션의 개요는 **'복잡한 다리 건설 현장'**과 같습니다. 강(네트워크) 건너편의 두 섬(서버)을 연결하기 위해, 양쪽 공사가 동시에 완료되지 않으면 다리를 무너뜨리고(롤백) 다시 시도해야 하는 치밀한 공정 관리가 필요합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 (5개 이상 상세화)**

| 구성 요소 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **TM (Transaction Manager)** | 트랜잭션의 전체 생명주기 관리 | 전역 트랜잭션 ID 할당, 참여자들에게 시작/커밋/롤백 지시 전달 | **지휘관** |
| **RM (Resource Manager)** | 실제 데이터 저장소 관리 (DB, MQ 등) | 로컬 트랜잭션 수행, TM의 지시에 따라 트랜잭션 커밋/중단 | **병사/부대장** |
| **AP (Application Program)** | 비즈니스 로직 수행 및 트랜잭션 경계 설정 | TM에게 트랜잭션 시작 요청, 비즈니스 로직 실행 후 완료 요청 | **작전 지휘부** |
| **Comm. Resource Manager** | 노드 간 메시지 전달 및 프로토콜 처리 | TCP/IP 기반의 원격 프로시저 호출(RPC) 전송 | **통신 병사** |
| **Transaction Log** | 장애 발생 시 복구를 위한 상태 저장 | 디스크에 Prepare, Commit, Abort 로그 기록 (Write-Ahead Logging) | **전쟁 일지** |

**2. 아키텍처: 2단계 커밋(2PC) 프로토콜 상세 도해**

아래는 분산 트랜잭션의 가장 대표적인 프로토콜인 **2PC (Two-Phase Commit)**의 동학 과정입니다.

```text
      [ Application ]              [ Coordinator (TM) ]              [ Participant (RM) ] 
          |                                   |                               |
          | -------- 1. Begin TX ----------> |                               |
          |                                   |                               |
          | ---- 2. Execute SQL (Node A) --> |                               |
          |                                   | ------- 3. Prepare Req ------> | (Lock Resources)
          |                                   | <------ 4. Prepare OK -------- | (Can Commit?)
          |                                   |                               |
          |                                   | ------- 3. Prepare Req ------> | (Lock Resources)
          |                                   | <------ 4. Prepare NO -------- | (Error Detected!)
          |                                   |                               |
          |                                   | [ 5. Global Decision: Abort ]  |
          |                                   |                               |
          |                                   | ------- 6. Rollback Req -----> | (Unlock)
          | <------ 7. TX Abort (Error) ----- |                               |
```

**다이어그램 해설**
위 과정은 **2PC의 각 단계(Phase 1: Prepare, Phase 2: Commit)**를 시각화한 것입니다.
1.  **Prepare Phase (단계 1)**: 코디네이터는 모든 참여자에게 `Prepare` 요청을 보냅니다. 각 참여자는 트랜잭션을 수행하고 리소스를 잠금(Lock)한 뒤, "할 준비 됨(OK)" 또는 "불가(NO)"를 응답합니다. 이때 데이터는 아직 디스크에 최종 커밋되지 않은 상태(Uncommitted)로 대기합니다.
2.  **Commit Phase (단계 2)**: 모든 참여자가 OK라고 하면 코디네이터는 `Commit` 명령을 내립니다. 하나라도 NO가 있거나 통신에 실패하면 즉시 `Abort`를 명령합니다.
3.  **Blocking 문제**: Prepare 단계에서 참여자는 코디네이터의 최종 명령을 기다리며 리소스를 잠그고 대기하게 되는데, 이때 코디네이터가 다운되면 전체 시스템이 멈추는 **Blocking** 상태에 빠지게 됩니다.

**3. 심층 동작 원리 및 핵심 로직**

분산 트랜잭션의 원자성을 보장하기 위해 다음과 같은 상세 동작 메커니즘이 적용됩니다.

**A. 로그 기반 복구 (Logging & Recovery)**
코디네이터와 참여자는 각 단계의 상태를 안정 저장장치(Non-Volatile Memory)에 기록합니다.
- **Undo Log**: 트랜잭션 롤백 시 변경 전 데이터로 복원하기 위한 정보.
- **Redo Log**: 시스템 장애 후 재가동 시 커밋되었지만 디스크에 반영되지 않은 데이터를 복구하기 위한 정보.

**B. 시간 초과 및 재시도 (Timeout & Retry)**
네트워크 분단 상황을 대비해 각 구성 요소는 타이머(Time-to-Live)를 가집니다.
- **Participant Timeout**: 코디네이터의 응답이 없으면 일정 시간 후 트랜잭션을 중단하고 잠금을 해제하여 시스템 멈춤을 방지(자가 복구).

**4. 핵심 알고리즘: XID 할당 및 분산 락 (Pseudo-Code)**
```java
// Java/JTA (Java Transaction API) 스타일 의사코드
public void executeDistributedTransaction() {
    XAResource xaRes1 = getDBResource(); // DB 연결
    XAResource xaRes2 = getFileResource(); // 파일 시스템 연결
    
    Xid xid = new MyXid(12345); // 전역 트랜잭션 ID 생성

    try {
        // 1단계: Prepare (리소스 등록 및 예비 단계)
        xaRes1.start(xid, TMNOFLAGS);
        updateDB();
        xaRes1.end(xid, TMSUCCESS);
        
        xaRes2.start(xid, TMNOFLAGS);
        writeFile();
        xaRes2.end(xid, TMSUCCESS);

        int prepare1 = xaRes1.prepare(xid); //Vote: OK
        int prepare2 = xaRes2.prepare(xid); //Vote: OK

        // 2단계: Commit or Rollback 결정
        if (prepare1 == XA_OK && prepare2 == XA_OK) {
            xaRes1.commit(xid, false); // 1-phase commit optimization 가능
            xaRes2.commit(xid, false);
        } else {
            xaRes1.rollback(xid);
            xaRes2.rollback(xid);
        }
    } catch (Exception e) {
        // 장애 발생 시 전체 롤백
        xaRes1.rollback(xid);
        xaRes2.rollback(xid);
    }
}
```

> **📢 섹션 요약 비유**
> 이 과정은 **'군대의 작전 훈련'**과 같습니다. 대장(Coordinator)이 "준비(Prepare)!"를 외치면 모든 부대원(Participant)은 "준비 완료!"를 대답하고 대기 자세를 취합니다(Blocking). 대장이 "실행(Commit)!"을 외쳐야만 비로소 총을 쏠 수 있습니다. 만약 대장이 기절하면(장애), 부대원들은 영원히 총을 쏘지 못한 채 얼어붙게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 분산 트랜잭션 제어 기법 비교 (정량적/구조적 분석)**

| 구분 | 2PC (Two-Phase Commit) | 3PC (Three-Phase Commit) | Saga Pattern | TCC (Try-Confirm-Cancel) |
|:---|:---|:---|:---|:---|
| **일관성 모델** | 강한 일관성 (Strong Consistency) | 강한 일관성 | 결과적 일관성 (Eventual Consistency) | 결과적 일관성 |
| **동기 방식** | 동기 (Synchronous) | 동기 | 비동기 (Asynchronous) | 동기/비동기 혼합 |
| **Blocking** | **O (Blocking 가능)** | **X (Non-blocking)** | **X (Non-blocking)** | **X (Non-blocking)** |
| **Locking** | 긴 시간 동안 리소스 Lock | Lock 시간 단축 | Lock 없음 (또는 짧음) | 비즈니스 레벨 Lock (예약) |
| **성능 (TPS)** | **낮음** (지연 높음) | 중간 | **높음** | 높음 |
| **복잡도** | 구현 단순, 운영 복잡 | 구현 복잡 | 로직 설계 복잡 (보상 트랜잭션 필요) | 비즈니스 로직에 의존적 |
| **사용처** | 동기식 금융 거래, RDBMS 간 연동 | 이론적 모델, 실무 적용 적음 | 마이크로서비스(MSA), 오래 걸리는 프로세스 | 고도의 일관성이 필요한 콘텐츠 서비스 |

**2. 타 과목 융합 관점**

**A. 네트워크 (Network)와의 시너지**
분산 트랜잭션의 성능은 **네트워크 지연 시간(Round Trip Time: RTT)**에 지배적입니다. 2PC 프로토콜은 최소 2번의 왕복(Prepare, Commit)이 필요하므로, 데이터센터 간( WAN 환경) 트랜잭션은 동일 LAN 내에서보다 수십 배의 지연이 발생할 수 있습니다. 따라서 네트워크 토폴로지 설계 시 분산 트랜잭션 빈도를 고려해야 합니다.

**B. 운영체제 (OS) 및 캡슐화**
OS의 **IPC(Inter-Process Communication)**나 **RPC(Remote Procedure Call)** 메커니즘 위에서 분산 트랜잭션 제어가 구현됩니다. 트랜잭션 컨텍스트(Context)가 프로세스 경계를 넘어 스레드 간에 전파되어야 하므로, TLS(Thread Local Storage) 관리가 중요합니다.

**3. 비교 분석: 2PC vs Saga**
- **2PC**: "원자성은 보장하지만, 성능과 가용성을 희생한다." (시스템 전체가 Lock에 걸릴 위험)
- **Saga**: "시스템의 가용성과 성능을 높이지만, 원자성을 포기하고 보상 로직(Compensating Transaction)을 통해 데이터를 수습해야 한다." (데이터 일시적 불일치 허용)

> **📢 섹션 요약 비유**
> 분산 트랜잭션 기법의 선택은 **'택시와 버스의 선택'**과 같습니다. **2PC**는 목적지에 도착할 때까지 다른 사람을 태우지 않고 직행하는 **'전세 택시(고비용, 확실)'**이고, **Saga**는 중간에 내려서 다른 버스를 갈아타며 가는 **'환승 버스(저비용, 번거로움)'**와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 과정**

**시나리오 1: 금융 시스템의 계좌 이체 (결정: 2PC 채택)**
- **상황**: A 은행에서 B 은행으로 1억 원 이체. A의 인출과 B의 입금은 반드시 동시에 일어나야 함.
- **판단**: 데이터 정합성이 최우선이며, 서버 간 통신 지연을 어느 정도 허용할 수 있는 내부망 환경임.
- **전략**: XA 표준 기반의 2PC를 사용하여 강한 일관성을 보장하고, 장애 시 복구 절차를 자동화한다.

**시나리오 2: 이커머스