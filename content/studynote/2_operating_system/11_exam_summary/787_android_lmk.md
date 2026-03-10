+++
weight = 787
title = "787. 안드로이드 LMK (Low Memory Killer)의 계층적 프로세스 종료 메커니즘"
date = "2026-03-10"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Android", "LMK", "Low Memory Killer", "OOM", "oom_adj", "메모리 관리", "모바일 OS"]
series = "운영체제 800제"
+++

# 안드로이드 LMK (Low Memory Killer) 작동 메커니즘

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리눅스의 OOM 킬러를 안드로이드 환경에 맞게 개선한 기술로, 시스템 메모리가 부족해질 때 사용자가 현재 사용 중인 앱은 보호하고 **중요도가 낮은 배경 앱부터 단계적으로 종료**하여 메모리를 확보하는 기법.
> 2. **가치**: 앱 전환 시의 빠른 속도를 위해 종료된 앱의 정보를 메모리에 캐싱하되, 시스템 가용성이 위협받을 때만 **우선순위(oom_adj)**에 따라 정밀하게 타격하여 사용자 경험을 유지한다.
> 3. **융합**: 안드로이드 프레임워크(Activity Manager)의 프로세스 상태 정보와 커널의 메모리 관리 모듈이 결합된 하이브리드 자원 회수 아키텍처다.

---

### Ⅰ. LMK (Low Memory Killer)의 핵심 지표

안드로이드는 프로세스의 중요도를 6단계 이상의 레벨로 관리한다.

| 우선순위 (Level) | 프로세스 유형 | 설명 | 비유 |
|:---|:---|:---|:---|
| **FOREGROUND** | 현재 화면에 보이는 앱 | 사용자가 직접 사용 중인 핵심 앱. | 내가 지금 쓰는 펜 |
| **VISIBLE** | 화면 일부가 가려진 앱 | 투명창 뒤에 보이거나 소리 재생 중인 앱. | 옆에 둔 공책 |
| **SERVICE** | 백그라운드 서비스 | 데이터 동기화, 위치 추적 등 배경 작업. | 가방 속 보조 배터리 |
| **CACHED** | 예전에 썼던 앱 | 나중에 빨리 켜려고 메모리에 남겨둔 상태. | 창고에 넣어둔 책 |

---

### Ⅱ. LMK 작동 아키텍처 및 흐름 (ASCII)

메모리 부족 단계(Threshold)에 따라 종료 대상이 확장되는 구조다.

```ascii
    [ RAM Usage Increasing... ]
    
    Level 1: Empty Memory < 128MB  --> KILL "CACHED" Apps (Empty Apps)
    Level 2: Empty Memory < 96MB   --> KILL "CONTENT_PROVIDER"
    Level 3: Empty Memory < 64MB   --> KILL "SERVICE" Apps
    Level 4: Empty Memory < 32MB   --> KILL "VISIBLE" Apps
    Level 5: Critical State        --> KILL "FOREGROUND" (Last Resort)
    
    [ Architecture ]
    +------------------------------------------+
    | [ Activity Manager Service (Java) ]      |
    | - Monitors App States                    |
    | - Sets 'oom_adj' score for each PID      |
    +-------------------|----------------------+
                        v
    +------------------------------------------+
    | [ Kernel LMK Driver / lmkd (Native) ]    |
    | - Monitors Free Pages                    |
    | - Executes Kill Signal based on oom_adj  |
    +------------------------------------------+
```

---

### Ⅲ. LMK vs Linux OOM Killer

| 구분 | 리눅스 OOM 킬러 | 안드로이드 LMK |
|:---|:---|:---|
| **발행 시점** | 메모리가 완전히 바닥났을 때 (임계) | **단계별 임계치**에 따라 선제적 작동 |
| **선정 기준** | 메모리 점유량이 큰 프로세스 (Badness) | **사용자 체감 중요도 (oom_adj)** |
| **목표** | 시스템 전체 패닉 방지 | **UI 부드러움 및 앱 전환 속도 유지** |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 앱 개발 시 메모리 관리 전략
- **현상**: 내 앱이 백그라운드로 가기만 하면 자꾸 죽어서 데이터가 날아감.
- **기술사적 결단**: 
  - `onSaveInstanceState()`를 통해 상태를 저장하고, `onTrimMemory()` 콜백을 구현하여 메모리 부족 신호 시 스스로 불필요한 리소스(이미지 캐시 등)를 해제하게 설계한다.
  - 중요한 배경 작업은 `Foreground Service`로 승격시켜 `oom_adj` 점수를 낮춘다.

#### 2. 기술사적 인사이트: lmkd의 진화
- 최근 안드로이드 버전은 커널 드라이버 방식에서 사용자 공간의 데몬인 **lmkd**로 이동했다. 이는 커널의 복잡도를 줄이고, 더 세밀한 메모리 압력(Pressure) 정보를 활용하여 더 똑똑하게 프로세스를 선정하기 위한 설계적 선택이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **멀티태스킹 최적화**: 한정된 RAM에서 수십 개의 앱이 마치 동시에 떠 있는 듯한 환상 제공.
- **배터리 효율성**: 불필요한 배경 프로세스 정리를 통한 전력 소모 억제.

#### 2. 미래 전망
앞으로 LMK는 단순한 종료를 넘어, **성능 인지형 스왑 (zRAM)**이나 **앱 동결(App Freezing)** 기술과 더욱 밀접하게 결합될 것이다. 인공지능이 사용자의 다음 앱 사용 패턴을 예측하여, 종료할 앱과 미리 메모리에 올려둘 앱을 결정하는 '지능형 라이프사이클 관리'가 모바일 OS의 핵심 경쟁력이 될 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[OOM 킬러](./777_oom_killer_policy.md)**: LMK의 사상적 뿌리.
- **[zRAM (메모리 압축)](../6_memory_management/TBD_zram.md)**: LMK가 작동하기 전 가용 공간을 늘리는 기술.
- **[Android Activity Lifecycle](../../4_software_engineering/TBD_android_lifecycle.md)**: `oom_adj` 점수가 결정되는 소프트웨어적 근거.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **LMK**는 거실에 장난감이 너무 많아지면 청소를 해주는 **'정리 요정'**과 같아요.
2. 지금 가지고 노는 장난감은 놔두고, 예전에 가지고 놀다가 구석에 밀어둔 오래된 장난감부터 하나씩 상자에 넣어서 치워주죠.
3. 덕분에 거실이 항상 깨끗해서 우리가 새로운 장난감을 가지고 놀 공간이 넉넉한 거랍니다!
