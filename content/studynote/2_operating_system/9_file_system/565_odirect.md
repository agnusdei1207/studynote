+++
title = "565. Direct I/O (O_DIRECT) - OS 캐시를 우회하여 데이터베이스 등의 자체 캐싱 최적화"
weight = 565
+++

# 565. 전력 관리 (Power Management)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 전력 소모 최적화
> 2. **가치**: 배터리 수명, 열 관리, 절전
> 3. **융합**: ACPI, 스케줄링, DVFS와 연관

---

## Ⅰ. 개요

### 개념 정의
**전력 관리(Power Management)**는 **시스템 전력 소모를 최적화하는 기술**입니다.

### 💡 비유: 스마트 조명
전력 관리는 **스마트 조명**과 같습니다. 필요할 때만 켜고 밝기를 조절합니다.

### 전력 관리 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                전력 관리 구조                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【ACPI 절전 상태】                                                   │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  상태             이름              전력            복구 시간       │ │   │
│  │  ────             ────              ────            ────────       │ │   │
│  │  S0               Working           Full            -             │ │   │
│  │  S1               Sleep (Power On)  Low             빠름          │ │   │
│  │  S2               Sleep (CPU Off)   Lower           보통          │ │   │
│  │  S3               Suspend to RAM    Very Low        보통          │ │   │
│  │  S4               Hibernate          Near Zero       느림          │ │   │
│  │  S5               Soft Off           Zero            리부트        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【CPU 전력 상태 (C-State)】                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  상태             설명              전력            지연           │ │   │
│  │  ────             ────              ────            ────           │ │   │
│  │  C0               Active            Full            0             │ │   │
│  │  C1               Halt              Low             1-10µs        │ │   │
│  │  C2               Stop-Clock        Lower           10-100µs      │ │   │
│  │  C3               Sleep             Very Low        100-1000µs    │ │   │
│  │  C6+              Deep Sleep        Near Zero       1-10ms        │ │   │
│  │                                                             │ │   │
│  │  깊은 C-State일수록 절전↑, 복구 시간↑                            │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【CPU 성능 상태 (P-State)】                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  P-State         주파수             전압            용도           │ │   │
│  │  ────────         ──────             ────            ────           │ │   │
│  │  P0               최대               최대            고성능         │ │   │
│  │  P1               중간               중간            일반          │ │   │
│  │  P2               낮음               낮음            절전          │ │   │
│  │  Pn               최저               최저            대기          │ │   │
│  │                                                             │ │   │
│  │  DVFS (Dynamic Voltage & Frequency Scaling)                     │ │   │
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
│                전력 관리 상세                                        │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【장치 전력 상태 (D-State)】                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  상태             설명                                         │ │   │
│  │  ────             ────                                         │ │   │
│  │  D0               Fully On (동작)                              │ │   │
│  │  D1               Low Power (일부 기능)                        │ │   │
│  │  D2               Lower Power (대부분 꺼짐)                     │ │   │
│  │  D3hot            Off (전력 유지, 빠른 복구)                     │ │   │
│  │  D3cold           Off (전력 차단)                              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【DVFS 동작】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  [부하 높음] → P0 (3.0GHz, 1.2V)                               │ │   │
│  │       ↓                                                         │ │   │
│  │  [부하 중간] → P1 (2.0GHz, 1.0V)                               │ │   │
│  │       ↓                                                         │ │   │
│  │  [부하 낮음] → P2 (1.0GHz, 0.8V)                               │ │   │
│  │       ↓                                                         │ │   │
│  │  [대기] → C1/C6 (Clock Gating)                                 │ │   │
│  │                                                             │ │   │
│  │  P = C × V² × f  (전력 = 정전용량 × 전압² × 주파수)              │ │   │
│  │  전압 낮추면 전력 크게 감소                                       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【CPU Governor】                                                     │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  Governor         특징                    용도                   │ │   │
│  │  ────────         ────                    ────                   │ │   │
│  │  performance      최대 주파수 유지         서버, HPC             │ │   │
│  │  powersave        최저 주파수 유지         배터리                │ │   │
│  │  ondemand         부하에 따라 조절         일반                  │ │   │
│  │  conservative     천천히 조절             절전                  │ │   │
│  │  schedutil        스케줄러 기반           최신                  │ │   │
│  │  userspace        사용자 설정             커스텀                │ │   │
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
│  【Linux 전력 관리】                                                 │
│  ──────────────────                                                │
│  // 전력 소모 확인                                                    │
│  $ cat /sys/class/power_supply/BAT0/power_now                      │
│ 8234000  // 8.234 W                                                 │
│                                                                     │
│  // 배터리 상태                                                       │
│  $ cat /sys/class/power_supply/BAT0/capacity                       │
│ 75                                                                   │
│                                                                     │
│  // CPU 주파수 확인                                                   │
│  $ cat /proc/cpuinfo | grep MHz                                     │
│  cpu MHz: 1200.000                                                  │
│  cpu MHz: 2400.000                                                  │
│                                                                     │
│  // 주파수 범위                                                       │
│  $ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq       │
│ 800000                                                               │
│  $ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq       │
│ 3500000                                                              │
│                                                                     │
│  【CPU Governor 설정】                                                │
│  ──────────────────                                                │
│  // 현재 Governor                                                     │
│  $ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor       │
│ schedutil                                                            │
│                                                                     │
│  // 사용 가능한 Governor                                              │
│  $ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors│
│ performance powersave ondemand conservative schedutil              │
│                                                                     │
│  // Governor 변경                                                     │
│  $ echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor│
│                                                                     │
│  // cpupower 도구                                                    │
│  $ sudo cpupower frequency-set -g performance                       │
│  $ sudo cpupower frequency-set -g powersave                         │
│                                                                     │
│  【C-State 설정】                                                      │
│  ──────────────────                                                │
│  // C-State 활성화                                                    │
│  $ cat /sys/module/processor/parameters/idle                       │
│  Y                                                                   │
│                                                                     │
│  // intel_idle 파라미터                                               │
│  $ cat /sys/module/intel_idle/parameters/max_cstate                │
│ 9                                                                    │
│                                                                     │
│  // C-State 제한                                                      │
│  $ echo 1 | sudo tee /sys/module/intel_idle/parameters/max_cstate  │
│                                                                     │
│  // idle=poll 커널 파라미터 (C-State 비활성화)                        │
│  GRUB_CMDLINE_LINUX="idle=poll"                                     │
│                                                                     │
│  【TLP (노트북 절전)】                                                │
│  ──────────────────                                                │
│  // 설치                                                            │
│  $ sudo apt install tlp                                             │
│  $ sudo tlp start                                                   │
│                                                                     │
│  // 상태 확인                                                        │
│  $ sudo tlp-stat                                                    │
│  --- TLP 1.4 --------------------------------------------           │
│  /etc/default/tlp installed: Yes                                    │
│  Mode: Battery                                                      │
│  CPU: Intel Core i7-8650U                                           │
│  Governor: powersave                                                │
│                                                                     │
│  // 설정                                                             │
│  /etc/default/tlp:                                                  │
│  CPU_SCALING_GOVERNOR_ON_AC=performance                             │
│  CPU_SCALING_GOVERNOR_ON_BAT=powersave                             │
│                                                                     │
│  【powertop】                                                         │
│  ──────────────────                                                │
│  // 설치                                                            │
│  $ sudo apt install powertop                                        │
│                                                                     │
│  // 분석                                                            │
│  $ sudo powertop                                                    │
│                                                                     │
│  // 자동 튜닝                                                        │
│  $ sudo powertop --auto-tune                                        │
│                                                                     │
│  // HTML 리포트                                                       │
│  $ sudo powertop --html=powertop.html                              │
│                                                                     │
│  【시스템 절전】                                                       │
│  ──────────────────                                                │
│  // Suspend (S3)                                                     │
│  $ systemctl suspend                                                │
│                                                                     │
│  // Hibernate (S4)                                                   │
│  $ systemctl hibernate                                              │
│                                                                     │
│  // Hybrid Sleep                                                     │
│  $ systemctl hybrid-sleep                                           │
│                                                                     │
│  // 타이머 설정                                                       │
│  $ sudo rtcwake -m mem -s 3600   // 1시간 후 자동 복구               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 시스템 전력 소모 최적화
• ACPI 상태: S0-S5 (Working → Off)
• C-State: C0-C6+ (Active → Deep Sleep)
• P-State: P0-Pn (DVFS 주파수/전압)
• D-State: D0-D3 (장치 전력)
• Governor: performance, powersave, schedutil
• DVFS: 동적 전압/주파수 스케일링
• P = C × V² × f (전력 공식)
• Linux: cpupower, tlp, powertop
• 절전: Suspend, Hibernate, Hybrid Sleep
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [ACPI](./xxx.md) → 전력 관리 표준
- [스케줄링](../3_process/xxx.md) → CPU Governor
- [CPU](../1_computer_architecture/xxx.md) → P-State, C-State

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 전력 관리는 "스마트 조명" 같아요!

**원리**: 필요할 때만 켜고 밝기를 조절해요!

**효과**: 배터리를 오래 사용해요!
