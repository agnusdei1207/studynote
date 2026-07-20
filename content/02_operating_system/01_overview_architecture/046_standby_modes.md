---
title: "Standby Modes"
date: "2026-04-05"
tags:
  - "studynote-operating-system"
weight: 46
---
> **핵심 인사이트**
> 1. 대기 모드(Standby/Sleep Mode)는 OS가 시스템 전력을 절감하면서도 빠른 복귀를 보장하는 전력 관리 상태 — ACPI(Advanced Configuration and Power Interface) 표준이 S0(완전 활성)부터 S5(소프트 파워오프)까지 6단계를 정의한다.
> 2. CPU P-State와 C-State는 OS 전력 관리의 핵심 — C-State는 CPU 유휴 시 코어별 절전(C0~C10), P-State는 DVFS(Dynamic Voltage Frequency Scaling)로 성능-전력 균형을 조절하며 Linux의 cpufreq 드라이버가 이를 제어한다.
> 3. 현대 OS의 전력 관리는 반응성과 효율의 트레이드오프 — Windows Modern Standby(S0ix)는 스마트폰처럼 네트워크 연결을 유지하면서 저전력을 달성하나, 배경 프로세스 관리가 불충분하면 배터리 드레인 문제가 발생한다.

---

## Ⅰ. ACPI 전력 상태

```
ACPI (Advanced Configuration and Power Interface):
  OS와 하드웨어 간 전력 관리 표준
  Intel/Microsoft/Toshiba 공동 개발 (1996)

글로벌 시스템 상태 (G-States):
  G0: 활성 (Working)
  G1: 슬리핑 (Sleeping) -> S1~S4
  G2: 소프트 파워오프 (Soft Off) -> S5
  G3: 메카니컬 파워오프 (전원 완전 차단)

슬리핑 상태 (S-States):
  S0: 완전 활성 (Full Working)

  S1 (Power on Suspend):
    CPU 캐시 플러시, CLK 정지
    RAM 유지, 빠른 복귀
    소비전력: 약간 감소

  S2: CPU 전원 OFF, 메모리 유지

  S3 (Suspend to RAM, STR):
    RAM 유지, 나머지 OFF
    복귀 시간: 수초
    대부분 노트북의 "슬립" 모드
    소비전력: 1~2W

  S4 (Suspend to Disk, STD, Hibernation):
    RAM -> 디스크 저장 -> 전원 OFF
    복귀 시간: 수십초 (디스크에서 로드)
    소비전력: 0W (전원 OFF)

  S5 (Soft Off):
    시스템 종료 (WOL 대기 가능)
    소비전력: < 1W

Windows 대응:
  S3 -> 절전 (Sleep)
  S4 -> 최대 절전 (Hibernate)
  Modern Standby -> S0ix
```

> 📢 **섹션 요약 비유**: ACPI S-State는 회사 퇴근 단계 — S0=열심히 일하는 중, S1=잠깐 자리 비움, S3=퇴근(짐 두고), S4=완전 퇴근(PC 끔), S5=전원 off. 빠른 복귀 vs 완전 절전 트레이드오프!

---

## Ⅱ. CPU C-State와 P-State

```
CPU 절전 상태 (C-States):
  각 CPU 코어의 유휴(Idle) 절전 단계

C-State 계층:
  C0: 활성 (Active, 명령 실행 중)
  C1: Halt (클럭 게이팅, 즉시 복귀)
  C1E: C1 + 전압 감소
  C3: Sleep (캐시 플러시)
  C6: Deep Power Down (코어 전원 OFF 일부)
  C7: Enhanced Deep Power Down
  C10: 가장 깊은 절전 (최신 CPU)

  진입: OS 스케줄러 유휴 감지 -> Halt 명령

  복귀 지연:
  C1: <1 μs, C3: <100 μs, C6: <1 ms, C10: <10ms

CPU P-State (성능 상태):
  DVFS: 전압+주파수 동적 조절

  P0: 최고 주파수/전압 (최대 성능)
  P1, P2, ...: 낮은 주파수/전압

  전력: P ≈ α × C × V^ × f
  V 20% 감소 -> 전력 36% 감소 (V^ 효과)

Linux cpufreq 드라이버:
  Governor (정책):
  - performance: 항상 최고 주파수
  - powersave: 항상 최저 주파수
  - ondemand: 부하에 따라 동적 (기본)
  - schedutil: CFS 스케줄러 연계 (현대적)

  확인: cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
  변경: echo schedutil > .../scaling_governor

Package C-State:
  모든 코어 C-State 진입 시 패키지(CPU 전체) 절전
  PC0, PC2, PC6, PC8, PC10 등
```

> 📢 **섹션 요약 비유**: C-State는 공장 가동 단계 — C0(풀가동), C1(일시정지), C6(라인 셧다운). 주문 없으면(유휴) 라인 끄고 절전!

---

## Ⅲ. Modern Standby (S0ix)

```
Modern Standby (Windows S0ix):
  스마트폰처럼 네트워크 연결 유지하면서 저전력

기존 S3 대비:
  S3: 네트워크 완전 차단 -> 이메일/알림 수신 불가
  S0ix: 저전력 상태에서 Wi-Fi 유지 -> 알림 수신

S0ix 동작:
  디스플레이 꺼짐 -> 화면 전원 OFF
  -> 앱 정지 (일시 중단)
  -> CPU C10 절전
  -> Wi-Fi 저전력 수신 유지 (Wi-Fi DTIM)
  -> 이메일 도착 -> CPU 웨이크업 -> 처리 -> 다시 C10

  목표 전력: < 5~10 mW (화면 꺼진 상태)

S0ix 문제:
  배경 프로세스 미관리 -> 전력 소모

  배터리 드레인 원인:
  - 전력 비효율 드라이버 깨어남
  - 백그라운드 앱 웨이크락 남용

  진단 도구:
  powercfg /sleepstudy -> 수면 품질 리포트
  powercfg /energy -> 전력 이슈 진단

Linux: 유사 개념
  SATA Link Power Management
  PCIe ASPM (Active State Power Management)
  Suspend-to-Idle (s2idle): S0ix 유사

Android Doze 모드:
  S0ix와 유사한 모바일 개념
  화면 꺼짐 + 일정 시간 후 Doze 진입
  네트워크 제한 + CPU 활동 제한
  유지보수 윈도우(Maintenance Window)에서만 동기화
```

> 📢 **섹션 요약 비유**: Modern Standby는 스마트워치 대기 모드 — 손목에 차고 있어도 배터리 오래가면서 카카오 알림(네트워크)은 계속 받아요!

---

## Ⅳ. OS 전력 관리 메커니즘

```
OS 전력 관리 소프트웨어 스택:

Linux 전력 관리:

  사용자공간: powertop, tlp, laptop-mode-tools
  v
  커널 전력 관리 서브시스템:
  - pm-utils
  - /sys/power/ 인터페이스
  v
  디바이스 드라이버 PM 콜백:
  - suspend(), resume()
  - runtime_suspend(), runtime_resume()
  v
  하드웨어: ACPI, 칩셋

Linux Runtime PM:
  장치 사용 없을 때 자동 절전

  USB 마우스: 움직임 없으면 USB 포트 절전
  SATA 드라이브: 활동 없으면 스핀다운

  커널 코드 패턴:
  pm_runtime_put_autosuspend(dev) -> 절전
  pm_runtime_get_sync(dev) -> 깨우기

Windows 전력 계획:
  균형 (Balanced): 성능-전력 균형
  고성능 (High Performance): 절전 없음
  절전 (Power Saver): 최대 절전

  Modern Standby 정책:
  PowerCfg /setactive <GUID>
  Connected Standby vs Disconnected

macOS:
  App Nap: 포커스 없는 앱 자동 제한
  Power Nap: 슬립 중 이메일 동기화
  Compressed Memory: 절전 RAM 사용
```

> 📢 **섹션 요약 비유**: OS 전력 관리는 스마트 사무실 — 아무도 없으면(유휴) 에어컨·조명 자동 끄기(C-State), 퇴근 전 프린터 대기 모드(S3), 주말엔 전원 차단(S5)!

---

## Ⅴ. 실무 시나리오 — 배터리 드레인 진단

```
노트북 배터리 빠른 방전 문제 해결:

현상:
  Surface Pro 9 슬립 상태에서
  8시간 동안 배터리 40% 소모 (비정상)
  정상: < 5%

진단:

1. powercfg /sleepstudy 실행:
   수면 보고서 생성 (HTML)

   의심 항목:
   - 총 드레인: 8시간 × 480mA = 과다
   - 배터리 드레인 상위 드라이버 표시

2. powercfg /energy 실행:
   에너지 효율 보고서

   발견:
   - Bluetooth 드라이버: 과도한 활동
   - Intel Display Driver: S0ix 진입 방해

3. 이벤트 뷰어 분석:
   전원 이벤트 로그
   웨이크 소스 분석

수정:
  블루투스 드라이버 업데이트
  디스플레이 드라이버 업데이트

  레지스트리:
  HKLM\SYSTEM\CurrentControlSet\Control\Power
  DisconnectedStandbyEnabled = 1

  결과:
  슬립 중 8시간 드레인: 40% -> 4% (정상화)

서버 전력 최적화 (다른 시나리오):
  데이터센터 서버 전력 관리
  IPMI/BMC: C-State 조정
  BIOS: C-State 깊이 설정
  OS: cpufreq governor 최적화

  효과: 서버 1대 절전 상태 10~20W 절감
  1000대 × 20W = 20kW = 연 1,750만원 절감
```

> 📢 **섹션 요약 비유**: 배터리 드레인 진단은 전기 누수 찾기 — powercfg는 전력계, 이상한 드라이버(블루투스)가 잠자는 동안 몰래 전기 쓰는 것을 잡아내요!

---

## 📌 관련 개념 맵

```
OS 대기 모드
+-- ACPI S-States
|   +-- S3 (Suspend to RAM)
|   +-- S4 (Hibernate)
|   +-- Modern Standby (S0ix)
+-- CPU 절전
|   +-- C-States (C0~C10)
|   +-- P-States (DVFS)
+-- OS 구현
|   +-- Linux cpufreq, runtime PM
|   +-- Windows 전력 계획
|   +-- Android Doze
+-- 진단
    +-- powercfg /sleepstudy
    +-- powertop (Linux)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[ACPI 표준 제정 (1996)]
Intel/MS/Toshiba
S0~S5 표준화
      |
      v
[멀티코어 C-State (2007~)]
인텔 Core 시리즈
패키지 C-State 도입
      |
      v
[Connected Standby / S0ix (2012)]
Windows 8 Surface
스마트폰식 대기 모드
      |
      v
[현재: Modern Standby 성숙]
Windows 11 최적화
Android Doze 고도화
      |
      v
[미래: AI 전력 예측]
사용 패턴 학습 -> 선제적 절전
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 대기 모드는 컴퓨터 졸기 — S3는 "잠깐 조는 것"(금방 깨어남), S4는 "푹 자는 것"(느리게 깨어남). 많이 잘수록 배터리 절약!
2. C-State는 CPU 쉬는 정도 — C0=열심히 일하기, C6=점심 휴식(전원 끄기). 쉬는 동안 전기 절약!
3. Modern Standby는 스마트폰 대기 — 화면은 꺼졌어도 카톡 알림은 와요! 노트북이 스마트폰처럼 저전력 유지하며 연결!
