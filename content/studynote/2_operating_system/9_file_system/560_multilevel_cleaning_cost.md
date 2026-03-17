+++
title = "560. 다단계 클리닝 및 비용 최적화 정책"
date = "2026-03-14"
weight = 560
+++

# 560. 다단계 클리닝 및 비용 최적화 정책

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다단계 클리닝(Multi-level Cleaning)은 **LFS (Log-Structured File System, 로그 구조 파일 시스템)** 환경의 플래시 메모리에서 발생하는 무효 블록(Invalid Block)을 회수할 때, 시스템 부하와 데이터의 열역학적 특성(뜨거움/차가움)에 따라 청소 강도와 시점을 지능적으로 제어하는 고급 **GC (Garbage Collection, 가비지 컬렉션)** 전략이다.
> 2. **가치**: **WA (Write Amplification, 쓰기 증폭)**을 수학적 모델링을 통해 최소화하여, 플래시 메모리의 물리적 수명인 **P/E (Program/Erase)** 사이클 한도를 획기적으로 연장하며, 청소 비용(Cleaning Cost)과 공간 확보 효율(Space Efficiency) 사이의 최적점(Pareto Optimality)을 찾아냄으로써 지연 시간(Latency) 변이를 억제한다.
> 3. **융합**: 운영체제 커널의 파일 시스템 계층과 **SSD (Solid State Drive)**의 **FTL (Flash Translation Layer, 플래시 변환 계층)**이 협력하여 **TRIM** 명령어를 통해 메타데이터를 동기화하고, **Hot (뜨거운)** 데이터와 **Cold (차가운)** 데이터의 분리(Classification)를 통해 불필요한 데이터 재기록을 방지하는 저장 장치 관리의 핵심 기술이다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**클리닝(Cleaning)**은 **LFS** 기반의 저장 장치에서 유효한 데이터(Valid Data)와 무효한 데이터(Invalid Data)가 섞여 있는 블록(Segment)을 재구성하는 **GC** 과정이다. **NAND Flash** 메모리는 Overwrite(덮어쓰기)가 불가능하므로, 업데이트 발생 시 새 위치에 기록하고 이전 위치를 무효화(Invalid) 처리한다. 이 과정이 반복되면 유효 데이터가 파편화(Fragmentation)되고 가용 공간이 고갈되므로, 주기적으로 유효 데이터만 모아 새 블록에 기록(Copy)하고 기존 블록을 소거(Erase)하는 청소 작업이 필수적이다.

#### 2. 기술적 배경 및 필요성
- **기존 한계**: 단순한 **FIFO (First-In, First-Out)** 방식이나 무조건적인 GC는 유효 데이터가 많은 블록을 재기록하게 하여 쓰기 증폭을 유발하고, 성능 저하(Stalling)를 초래한다.
- **혁신적 패러다임**: **LFS**의 등장으로 쓰기 작업을 순차적으로 처리하여 회전식 디스크(**HDD (Hard Disk Drive)**)의 **Seek Time**을 제거했으나, 이로 인해 청소(Cleaning) 부하가 새로운 병목 지점으로 부상했다.
- **현재 요구**: 데이터 센터와 엔터프라이즈 환경에서는 예측 가능한 지연 시간과 장비 수명이 중요하므로, 부하 상황에 따라 동적으로 변화하는 **다단계(Multi-level)** 전략이 요구된다.

#### 3. 핵심 메커니즘 개요
클리닝은 단순히 공간을 비우는 것이 아니라 **Swap-In/Out** 과정과 유사하다. 시스템은 여유 공간(Free Block List)이 임계치(Threshold) 이하로 떨어지면 클리닝을 개시한다. 이때, 어떤 블록을 희생양(Victim)으로 삼을지 결정하는 정책(Policy)이 전체 성능을 좌우한다.

```text
      [ Initial State ]           [ Cleaning Process ]          [ Final State ]
      +----------------+          +----------------+           +----------------+
Block | Data A (Valid) |          | Read & Select |           | Data A (Valid) |
      | Data B (Invalid)|  --->   | Copy A to New  |  --->     | Data C (Valid) |
      | Data C (Valid) |          | Erase Old      |           +----------------+
      +----------------+          +----------------+            ^ Erased Block
       Victim Block                  ^ New Block                  (Free Space)
```
*그림 1. 기본적인 클리닝 사이클: 유효 데이터(A, C)를 추출하여 새 블록으로 이주 후 기존 블록을 소거(Erase)한다.*

#### 📢 섹션 요약 비유
클리닝은 "서류 파일 보관함에 빈 공간이 없을 때, **아직 써야 할 문서(Valid Data)**만 골라내어 새 보관함으로 옮기고, **다 쓴 문서(Invalid Data)**가 담긴 낡은 보관함을 통째로 비우는 행정 과정**"과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 동작
다단계 클리닝 시스템은 크게 **모니터링(Monitoring)**, **정책(Policy)**, **액터(Actor)** 모듈로 구성된다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/파라미터 | 비유 |
|:---|:---|:---|:---|:---|
| **Segment Usage Table** | 블록 메타데이터 관리 | 각 세그먼트의 유효 데이터 비율(Live Ratio)과 수정 시간(Age)을 주기적 갱신 | Block Validity Map | 주소록 |
| **Cost-Benefit Unit** | 비용 계산 엔진 | 수식에 따라 각 후보 블록의 청소 비용과 이득을 실시간 산출 | `Util(u)`, `Age(t)` | 회계팀 |
| **Cleaning Scheduler** | 작업 스케줄링 | **Foreground** vs **Background** 모드 결정 및 할당량(Quota) 배분 | `Free Blocks Threshold` | 관리자 |
| **GC Thread (Worker)** | 실제 데이터 이동 | 유효 페이지 읽기 -> 새 블록 쓰기 -> Invalidate -> Erase 명령 | NAND Read/Prog/Erase | 청소부 |
| **Dynamic Threshold** | 임계값 조절 | 시스템 부하(**IOPS (Input/Output Operations Per Second)**)에 따라 GC 트리거 레벨을 동적으로 변경 | `Low/Medium/High Watermark` | 댐 수문 |

#### 2. 희생자 선택 정책 (Victim Selection Policy)
어떤 세그먼트를 청소할지 결정하는 것이 가장 핵심이다. 대표적인 두 가지 알고리즘을 비교한다.

```text
   [ Efficiency Curve: Greedy vs Cost-Benefit ]

   Write Amplification Factor (WAF)
      ▲
   5.0|            _______  Greedy (High u)
      |          /
      |        /
   2.5|------/__________  Cost-Benefit (Balanced)
      |      
   1.0|______________________________________▶
      0.2   0.5    0.7      0.9    Utilization (u)
```
*그림 2. 유효 데이터 비율(Utilization)에 따른 쓰기 증폭(WAF) 변화 추이*

- **Greedy Policy (탐욕법)**: 
  - 유효 데이터가 가장 적은 블록(`u`가 가장 낮은 블록)을 선택한다. 
  - 장점: 단기적으로 회수 효율이 좋음.
  - 단점: 높은 `u`를 가진 블록들이 방치되어 장기적으로 청소 불가 상태가 될 수 있음.
- **Cost-Benefit Policy (비용-편익)**: 
  - 수식: **`Cost = (2 * u) / (1 - u)`** 또는 **`Benefit = (Age * (1-u))`**
  - 블록의 수정 시간(Age)과 유효 데이터 비율(`u`)을 모두 고려한다. 오래되었고(`Age` 큼) 유효 데이터가 적은(`1-u` 큼) 블록을 우선 선택한다.

#### 3. 다단계(Multi-level) 클리닝 전략
시스템의 상황에 따라 클리닝의 강도와 타이밍을 조절하는 아키텍처이다.

- **Level 1: Background GC (Idle-time Cleaning)**
  - 시스템 유휴 시(I/O Queue가 비어있을 때) 저우선순위로 실행.
  - 목표: 미리미리 조금씩 청소하여 긴급 상황 방지.
  - 특징: 사용자 요청과 경합하지 않으므로 성능 저하 최소화.
- **Level 2: Foreground GC (On-demand Cleaning)**
  - 여유 공간이 임계치(예: 3% 미만) 아래로 떨어지면 강제 실행.
  - 목표: 즉시적인 블록 확보.
  - 특징: 쓰기 요청이 Blocking되므로 Latency 급증.
- **Level 3: Hybrid / Policer**
  - 사용자 패턴을 학습하여 Hot/Cold 데이터를 분리.
  - Hot 데이터(자주 변경)는 수명이 짧을 것으로 예상하여 바로바로 정리하고, Cold 데이터(보관용)는 방치했다가 일괄 처리.

```text
[ Operational State Machine ]

         I/O Idle Request
   +--------(Idle)---------+
   |    [ State: Normal ]  |---▶ [ L1: Background GC ]
   |                       |          (Trigger: Timer)
   +-----------+-----------+
               | Free Blocks < Threshold (Critical)
               v
   +-----------------------+
   |   [ State: Urgent ]   |---▶ [ L2: Foreground GC ]
   +-----------------------+          (Blocking)
```
*그림 3. 시스템 부하 상태에 따른 GC 모드 전이(State Transition) 다이어그램*

#### 📢 섹션 요약 비유
희생자 선택은 "치워야 할 **짐의 무게(Valid Data Amount)**와 **그짐이 방치된 시간(Age)**을 계산기에 두드려 보고, 가장 효율적으로 공간을 확보할 수 있는 짐부터 정리하는 청소 로봇의 두뇌"와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Static vs Dynamic

| 구분 | Static Policy (정적 전략) | Dynamic Policy (동적 전략) |
|:---|:---|:---|
| **대표 기법** | Greedy, FIFO | Cost-Benefit, Multi-level |
| **유효 데이터 분포** | 고르게 분포될 때 효율적 | 치우쳐질(Skewed) 때 강점 |
| **부하 변동 대응** | 약함 (임계치 고정) | 강함 (임계치 가변) |
| **쓰기 증폭(WA)** | 변동폭 큼 | 최적화 유도 |
| **연산 오버헤드** | 낮음 | 높음 (계산 필요) |
| **적용 분야** | 임베디드, 저가형 USB | 엔터프라이즈 SSD, Data Center |

#### 2. 과목 융합 관점

- **운영체제(OS) & 파일 시스템**: LFS는 파일 시스템 레벨에서의 청소를 담당하지만, 최근 **FTL** 내부에서도 이를 수행한다. OS의 **TRIM 명령**은 파일 삭제 사실을 FTL에 즉시 알려주어, 불필요한 가비지 컬렉션(삭제된 데이터를 유효 데이터로 오인하는 경우)을 방지하여 **Synergy**를 낸다.
- **컴퓨터 구조 (Architecture)**: CPU의 캐시 메모리 교체 정책(**LRU (Least Recently Used)** 등)과 청소 정책은 근본적으로 같은 "공간 효율성과 접근 시간의 트레이드오프" 문제를 다룬다. 단, SSD는 물리적 소거(Erase) 비용이 매우 크므로 정책이 더 복잡하다.

```text
[ OS-SSD Interaction Flow ]

  Application (User)
        |
        v
  File System: "Delete File.log" (Logical Delete)
        |
        v  [ TRIM Command ]
  ------------------------------
  SSD Controller (FTL)
        |
        |---> Update Bitmap: Block X = INVALID
        |
        |---> [ Cost-Benefit Calculator ]
        |       (Block X benefit now skyrockets)
        |
        v
  Garbage Collector: "Clean Block X immediately!"
        |
        v
  NAND Flash: Block X Erased (Low Cost Cleaning!)
```
*그림 4. TRIM 명령어가 연동될 때 클리닝 비용이 획기적으로 낮아지는 과정*

#### 📢 섹션 요약 비유
다단계 전략은 "단순 반복적인 업무 로봇(Static)과 달리, **업무량(Workload)을 보고 자동으로 업무 강도를 조절하며 주말(Idle)에 미리미리 일을 처리하는 스마트 매니저(Dynamic)**의 차이"와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정
**상황 A: 웹 서버 로그 저장 장치 (쓰기 집약형)**
- **특징**: 로그는 순차 기록되지만 오래된 로그는 빠르게 삭제됨(임시 데이터).
- **결정**: **Greedy Policy** 적합. 유효 비율이 급격히 떨어지는 블록이 빈번히 발생하므로, 가장 유효 데이터가 적은 블록을 즉시 회수하는 것이 효율적이다.
- **과제**: 로그 로테이션(Log Rotation) 주기와 GC 주기를 맞추기.

**상황 B: 금융권 DB 트랜잭션 로그 (랜덤 쓰기 + 무결성 중요)**
- **특징**: 쓰기 패턴이 랜덤하며, 유효 데이터 수명이 다양함(Hot/Cold mix). 지연 시간(Latency) 편차가 치명적임.
- **결정**: **Cost-Benefit + Multi-level** 필수. Foreground GC가 발동되면 트랜잭션이 멈추므로, Background GC를 적극 가동하여 여유 공간을 항상 10% 이상 확보해야 한다.
- **과제**: **OP (Over-Provisioning)** 비율을 높여(7% -> 28%) GC 빈도를 자체적으로 낮추는 설계 변경 필요.

#### 2. 도입 체크리스트

| 항목 | 기술적 (Technical) | 운영·보안적 (Operational/Security) |
|:---|:---|:---|
| **성능** | **WA (Write Amplification)** 1.5 미만 달성 가능 여부 확인 | **P99 Latency**가 GC 시 급증하지 않는지 모니터링 |
| **수명** | **P/E Cycle** 소모 분석 | 예기치 않은 전원 차단(**Power-loss**) 시 Data Safety |
| **구성** | **TRIM**