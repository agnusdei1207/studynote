+++
title = "75. ACPI (Advanced Configuration and Power Interface)"
weight = 75
+++

# 566. ACPI (Advanced Configuration and Power Interface)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전력 관리 및 구성 표준 인터페이스
> 2. **가치**: OS 독립적, 하드웨어 추상화
> 3. **융합**: 전력 관리, PnP, 열 관리와 연관

---

## Ⅰ. 개요

### 개념 정의
**ACPI(Advanced Configuration and Power Interface)**는 **OS와 하드웨어 간 전력 관리 및 구성 표준**입니다.

### 💡 비유: 건물 관리 시스템
ACPI는 **건물 관리 시스템**과 같습니다. 조명, 냉난방, 보안을 통합 관리합니다.

### ACPI 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                ACPI 구조                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【ACPI 계층】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  ┌─────────────────────────────────────────────────────┐    │ │   │
│  │  │                 운영체제 (OS)                          │    │ │   │
│  │  └─────────────────────────────────────────────────────┘    │ │   │
│  │                          │                                   │ │   │
│  │                          ▼                                   │ │   │
│  │  ┌─────────────────────────────────────────────────────┐    │ │   │
│  │  │              ACPI Driver (AML 인터프리터)             │    │ │   │
│  │  └─────────────────────────────────────────────────────┘    │ │   │
│  │                          │                                   │ │   │
│  │                          ▼                                   │ │   │
│  │  ┌─────────────────────────────────────────────────────┐    │ │   │
│  │  │              ACPI Tables (DSDT, SSDT, FADT)           │    │ │   │
│  │  └─────────────────────────────────────────────────────┘    │ │   │
│  │                          │                                   │ │   │
│  │                          ▼                                   │ │   │
│  │  ┌─────────────────────────────────────────────────────┐    │ │   │
│  │  │              하드웨어 (BIOS/UEFI)                       │    │ │   │
│  │  └─────────────────────────────────────────────────────┘    │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【ACPI 테이블】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  테이블            설명                                         │ │   │
│  │  ──────            ────                                         │ │   │
│  │  RSDP              Root System Description Pointer            │ │   │
│  │  RSDT/XSDT         Root/System Description Table              │ │   │
│  │  DSDT              Differentiated System Description Table    │ │   │
│  │  SSDT              Secondary System Description Table         │ │   │
│  │  FADT              Fixed ACPI Description Table               │ │   │
│  │  FACS              Firmware ACPI Control Structure            │ │   │
│  │  MADT              Multiple APIC Description Table           │ │   │
│  │  MCFG              Memory Mapped Configuration Space         │ │   │
│  │  HPET              High Precision Event Timer                │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【ACPI 기능】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  기능              설명                                         │ │   │
│  │  ────              ────                                         │ │   │
│  │  전원 관리          S0-S5 상태, 절전 모드                         │ │   │
│  │  장치 구성          PnP, 리소스 할당                             │ │   │
│  │  열 관리            온도 모니터링, 팬 제어                        │ │   │
│  │  배터리 관리        배터리 상태, 잔량 보고                        │ │   │
│  │  이벤트 처리        전원 버튼, 뚜껑 닫기 등                       │ │   │
│  │  프로세서 제어      C-State, P-State, throttling               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                ACPI 상세                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【전원 상태 (Sleep State)】                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  상태             이름                    전력                │ │   │
│  │  ────             ────                    ────                │ │   │
│  │  S0               Working (G0)            Full                │ │   │
│  │  S1               Sleep (G1)              Low                 │ │   │
│  │  S2               Sleep (G1)              Lower               │ │   │
│  │  S3               Suspend to RAM          Very Low            │ │   │
│  │  S4               Hibernate               Near Zero           │ │   │
│  │  S5               Soft Off (G2)           Zero                │ │   │
│  │                                                             │ │   │
│  │  G0: Working    G1: Sleeping    G2: Soft Off    G3: Mechanical Off│
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【AML (ACPI Machine Language)】                                     │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • 바이트코드 형태의 하드웨어 설명                              │ │   │
│  │  • OS의 AML 인터프리터가 실행                                  │ │   │
│  │  • DSDT/SSDT에 포함                                            │ │   │
│  │                                                             │ │   │
│  │  ASL (ACPI Source Language) → AML 컴파일                       │ │   │
│  │                                                             │ │   │
│  │  // ASL 예시                                                    │ │   │
│  │  Scope(\_SB) {                                                 │ │   │
│  │      Device(LID0) {                                           │ │   │
│  │          Name(_HID, "PNP0C0D")                                │ │   │
│  │          Method(_LID, 0) {                                    │ │   │
│  │              Return (LIDS)                                    │ │   │
│  │          }                                                     │ │   │
│  │      }                                                         │ │   │
│  │  }                                                             │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【ACPI 이벤트】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  이벤트            설명                                         │ │   │
│  │  ────              ────                                         │ │   │
│  │  Power Button     전원 버튼 누름                                │ │   │
│  │  Sleep Button     절전 버튼                                    │ │   │
│  │  Lid              노트북 뚜껑 닫기/열기                          │ │   │
│  │  Thermal          온도 임계값 초과                              │ │   │
│  │  Battery          배터리 상태 변화                              │ │   │
│  │  Dock             도킹 스테이션 연결/해제                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Linux ACPI 확인】                                                 │
│  ──────────────────                                                │
│  // ACPI 테이블                                                       │
│  $ ls /sys/firmware/acpi/tables/                                   │
│  DSDT  FACP  FACS  APIC  MCFG  SSDT1  SSDT2                        │
│                                                                     │
│  // DSDT 덤프                                                        │
│  $ sudo cat /sys/firmware/acpi/tables/DSDT > dsdt.aml              │
│  $ iasl -d dsdt.aml                // 디컴파일                      │
│                                                                     │
│  // ACPI 이벤트                                                       │
│  $ cat /proc/acpi/event                                            │
│                                                                     │
│  【ACPI 배터리 정보】                                                 │
│  ──────────────────                                                │
│  // 배터리 상태                                                       │
│  $ cat /sys/class/power_supply/BAT0/status                         │
│  Discharging                                                         │
│                                                                     │
│  // 배터리 용량                                                       │
│  $ cat /sys/class/power_supply/BAT0/capacity                       │
│ 75                                                                   │
│                                                                     │
│  // 배터리 정보                                                       │
│  $ cat /sys/class/power_supply/BAT0/uevent                         │
│  POWER_SUPPLY_NAME=BAT0                                            │
│  POWER_SUPPLY_STATUS=Discharging                                    │
│  POWER_SUPPLY_CAPACITY=75                                           │
│                                                                     │
│  【ACPI 열 관리】                                                      │
│  ──────────────────                                                │
│  // 열 영역 확인                                                      │
│  $ ls /sys/class/thermal/                                          │
│  thermal_zone0  thermal_zone1  cooling_device0                     │
│                                                                     │
│  // 온도 확인                                                        │
│  $ cat /sys/class/thermal/thermal_zone0/temp                       │
│ 42000  // 42°C (millidegrees)                                      │
│                                                                     │
│  // 냉각 장치                                                         │
│  $ cat /sys/class/thermal/cooling_device0/type                     │
│  Processor                                                          │
│                                                                     │
│  【ACPI 버튼 이벤트】                                                 │
│  ──────────────────                                                │
│  // 전원 버튼                                                         │
│  $ cat /proc/acpi/button/power/PWRF/state                          │
│  state:      released                                               │
│                                                                     │
│  // 뚜껑 스위치                                                        │
│  $ cat /proc/acpi/button/lid/LID0/state                            │
│  state:      open                                                   │
│                                                                     │
│  // acpid 데몬                                                       │
│  $ sudo systemctl status acpid                                      │
│                                                                     │
│  // acpid 이벤트 핸들러                                               │
│  /etc/acpi/events/power-button:                                    │
│  event=button/power                                                 │
│  action=/sbin/shutdown -h now                                      │
│                                                                     │
│  【ACPI 디버깅】                                                       │
│  ──────────────────                                                │
│  // ACPI 디버그 레벨                                                  │
│  $ cat /sys/module/acpi/parameters/debug_level                     │
│                                                                     │
│  // 디버그 레이어                                                     │
│  $ cat /sys/module/acpi/parameters/debug_layer                     │
│                                                                     │
│  // 커널 파라미터                                                      │
│  acpi.debug_layer=0x2 acpi.debug_level=0x2                         │
│                                                                     │
│  // ACPI 에러 확인                                                    │
│  $ dmesg | grep -i acpi                                             │
│  ACPI: Core revision 20210730                                      │
│  ACPI: 1 ACPI AML tables successfully acquired and loaded          │
│                                                                     │
│  【ACPI 문제 해결】                                                   │
│  ──────────────────                                                │
│  // ACPI 비활성화 (문제 시)                                           │
│  acpi=off  // 커널 파라미터                                          │
│                                                                     │
│  // 특정 기능 비활성화                                                  │
│  acpi=ht   // 하이퍼스레딩만                                          │
│  noacpi    // 레거시                                                 │
│                                                                     │
│  // suspend/hibernate 디버그                                         │
│  $ cat /sys/power/pm_test                                          │
│  [none] core processors platform devices freezer                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 전력 관리 및 구성 표준 인터페이스
• 계층: OS → ACPI Driver → ACPI Tables → Hardware
• 테이블: RSDP, DSDT, SSDT, FADT, MADT
• 언어: ASL (Source) → AML (Bytecode)
• 전원 상태: S0-S5, G0-G3
• 기능: 전원, 구성, 열, 배터리, 이벤트
• 이벤트: 전원버튼, 뚜껑, 열, 배터리
• Linux: /sys/firmware/acpi/, acpid
• 디버그: iasl, dmesg | grep acpi
• OS 독립: 하드웨어 추상화
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [전력 관리](./565_power_management.md) → C-State, P-State
- [BIOS/UEFI](./570_bios_uefi.md) → 펌웨어
- [핫 플러그](./568_hot_plug.md) → 장치 이벤트

### 👶 어린이를 위한 3줄 비유 설명
**개념**: ACPI는 "건물 관리 시스템" 같아요!

**원리**: 전원과 온도를 자동으로 관리해요!

**효과**: 컴퓨터가 알아서 절전해요!
