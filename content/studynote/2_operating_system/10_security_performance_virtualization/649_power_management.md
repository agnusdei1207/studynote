+++
title = "649. 전력 관리 (Power Management)"
date = "2026-03-16"
weight = 649
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "전력 관리", "Power Management", "ACPI", "CPU Frequency Scaling", "절전 모드"]
+++

# 전력 관리 (Power Management)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전력 관리는 **CPU, 디스크, 화면 등 하드웨어의 전력 소모를 제어**하여 배터리 수명을 연장하고 에너지 효율을 높이는 기술이다.
> 2. **가치**: 모바일 기기에서는 배터리 수명이, 데이터센터에서는 **전력 비용과 발열 관리**가 핵심이며, ACPI, C-State, P-State, DVFS가 핵심 메커니즘이다.
> 3. **융합**:: OS의 전력 관리 계층, 하드웨어의 절전 모드, 애플리케이션의 배터리 인식형 설계가 결합하여 **그린 컴퓨팅**을 실현한다.

+++

## Ⅰ. 전력 관리의 개요

### 1. 정의
- 전력 관리는 시스템의 전력 소모를 줄이기 위해 **전력 상태를 제어**하고 **유휴 시 저전력 모드로 전환**하는 기술이다.

### 2. 등장 배경
- 모바일 컴퓨팅(노트북, 스마트폰)의 보급
- 데이터센터의 전력 비용 증가 (전력 + 냉각)

### 3. 💡 비유: '자동차의 시동 정지 시스템'
- 전력 관리는 **'신호 대기 중 엔진 끄는 자동차'**와 같다.
- 필요할 때만 엔진(CPU)을 켜고, 대기할 때는 꺼서 연료(배터리)를 아낀다.

- **📢 섹션 요약 비유**: 방 안에 있을 때는 불을 밝히고, 나갈 때는 끄는 것처럼, 컴퓨터도 일하지 않을 때는 전력을 줄입니다.

+++

## Ⅱ. ACPI (Advanced Configuration and Power Interface)

### 1. ACPI 개요
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                  ACPI 전력 상태                                 │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Global System States] (G-State)                              │
    │   G0 (Working)   : 정상 작동                                    │
    │   G1 (Sleep)     : S1~S4 절전 모드                             │
    │   G2 (Soft Off)  : S5 (전원 스위치 꺼짐)                       │
    │   G3 (Mech Off)  : 전원 코드 분리                               │
    │                                                                 │
    │  [Sleep States] (S-State)                                      │
    │   S0 : Working                                                 │
    │   S1 : CPU만 정지 (CPU context 보존)                           │
    │   S2 : CPU + Cache 정지                                        │
    │   S3 : Suspend to RAM (대부분 장치 전원 off)                    │
    │   S4 : Suspend to Disk (Hiberate)                              │
    │                                                                 │
    │  [Device Power States] (D-State)                               │
    │   D0 : Full On                                                 │
    │   D1~D3 : 중간 단계                                            │
    │                                                                 │
    │  [CPU Performance States] (P-State)                            │
    │   P0 : 최고 성능                                                │
    │   P1~Pn : 점진적으로 낮은 성능, 낮은 전력                       │
    │                                                                 │
    │  [Processor Idle States] (C-State)                             │
    │   C0 : 실행 중                                                │
    │   C1 : Halt (명령 실행 중단)                                   │
    │   C2~Cn : 점진적으로 깊은 수면 상태                            │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Linux 전력 관리 도구
```bash
# CPU 정보 확인
cat /proc/cpuinfo | grep MHz

# C-State 확인
cat /sys/devices/system/cpu/cpu0/cpuidle/state*/name

# Governor 확인
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# 배터리 상태
upower -i /org/freedesktop/UPower/devices/battery_BAT0
```

+++

## Ⅲ. CPU Frequency Scaling (DVFS)

### 1. Dynamic Voltage and Frequency Scaling
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │            DVFS (전압/주파수 동적 스케일링)                      │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [관계식]                                                      │
    │   Power ∝ Voltage² × Frequency                                 │
    │   - 주파수 낮추면 → 전압도 낮출 수 있음                         │
    │   - 전력 소비는 제곱으로 감소                                   │
    │                                                                 │
    │  [CPU Governor]                                                │
    │   performance  : 최대 주파수 유지 (성능 우선)                   │
    │   powersave   : 최소 주파수 유지 (전력 우선)                    │
    │   ondemand    : 부하에 따라 동적 (레거시)                       │
    │   conservative : 천천히 증감 (안정성)                           │
    │   schedutil   : 스케줄러 연동 (최신)                           │
    │                                                                 │
    │  [예시]                                                        │
    │   Idle       → CPU 800 MHz (0.9V)                              │
    │   Light Load → CPU 1.2 GHz (1.0V)                              │
    │   Heavy Load → CPU 3.0 GHz (1.3V)                              │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Governor 설정
```bash
# Governor 확인
cpupower frequency-info

# Governor 변경
cpupower frequency-set -g powersave

# 최대/최소 주파수 설정
cpupower frequency-set -d 800MHz -u 3GHz
```

+++

## Ⅳ. 장치별 전력 관리

### 1. 디스크
- **스핀다운**: 일정 시간 사용 없으면 회전 정지
- **APM (Advanced Power Management)**: 디스크 전력 모드
```bash
# hdparm으로 설정
hdparm -S 240 /dev/sda  # 20분 후 스플다운
```

### 2. 네트워크
- **Wake-on-LAN**: 네트워크 패킷으로 깨우기
- **Wol 무효화**: 전력 절약
```bash
ethtool -s eth0 wol d
```

### 3. 화면
- **밝기 제어**: 낮출수록 전력 절약
- **DPMS (Display Power Management Signaling)**: 대기 시 화면 끔

+++

## Ⅴ. 데이터센터 전력 관리

### 1. 전력 효율성 지표
- **PUE (Power Usage Effectiveness)**: 총 전력 / IT 장비 전력
  - 이상적 PUE = 1.0
  - 일반적 PUE = 1.2~1.5
- **DCiE (Data Center Infrastructure Efficiency)**: 1 / PUE

### 2. 전력 캡핑 (Power Capping)
- 서버의 최대 전력 소비 제한
- RAPL (Running Average Power Limit)

+++

## Ⅵ. 실무 적용

### 1. 노트북 최적화
- **TLP (Linux Advanced Power Management)**
- **powertop**: 전력 소모 분석 및 최적화 제안

### 2. 안티패턴
- **"절전 모드 과도 사용"**: 성능 저하
- **"절전 기능 끄기"**: 배터리 급격 소모

+++

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **배터리 수명**: 30~50% 연장
- **발열 감소**: 시스템 안정성 향상

### 2. 미래 전맹
- **ARM 서버**: 저전력 데이터센터
- **에너지 하베스팅**: 낭비 에너지 회수

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **CPU 스케줄링**: 전력 인식 스케줄링
- **노트북/모바일**: 전력 관리 중요 기기
- **데이터센터**: 전력 효율

+++

## 👶 어린이를 위한 3줄 비유 설명
1. 전력 관리는 **"불 밝기를 조절하는 것"** 같아요.
2. 낮에는 밝게, 밤에는 어둡게, 방에 없을 때는 불을 끄면 전기료를 아낄 수 있죠.
3. 컴퓨터도 일하지 않을 때는 잠깐 쉬어서(절전 모드) 배터리를 아낀답니다!