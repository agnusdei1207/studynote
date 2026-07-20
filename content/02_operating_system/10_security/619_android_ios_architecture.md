---
title: "Android vs iOS"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 619
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Android는 Google이 주도하는 오픈 소스 (Open Source) 모바일 운영체제로 리눅스 커널 (Linux Kernel) 위에 ART (Android Runtime) 가상머신과 Java/Kotlin 애플리케이션 프레임워크를 탑재한 구조이며, iOS는 Apple이 개발한 폐쇄형 모바일 운영체제로 XNU (X is Not Unix) 하이브리드 커널 위에 Swift/Objective-C 네이티브 런타임을 탑재한 구조다.
> 2. **가치**: 두 운영체제는 전 세계 모바일 시장의 99% 이상을 점유하며, 각각의 아키텍처 선택(오픈 생태계 vs 폐쇄 일체형, VM vs 네이티브, 커널 커스터마이징 vs 독자 커널)이 보안 모델, 성능 특성, 개발자 생태계, 전력 관리 전략에 근본적인 차이를 만들어낸다.
> 3. **융합**: Android의 리눅스 커널 기반 Wakelock 전력 관리, Binder IPC (Inter-Process Communication), Zygote 프로세스 포킹 (Forking) 메커니즘은 서버 운영체제 기술이 모바일에 적응한 사례이며, iOS의 XNU 커널은 Mach 마이크로커널 (Microkernel)과 BSD (Berkeley Software Distribution) 계층이 융합된 독자적 아키텍처다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
모바일 운영체제 (Mobile OS, Mobile Operating System)는 스마트폰, 태블릿, 웨어러블 (Wearable) 등 휴대용 기기에서 배터리 전력, 열 관리 (Thermal Management), 무선 통신, 터치 인터페이스라는 고유한 하드웨어 제약 아래에서 애플리케이션을 실행하고 자원을 관리하는 특수 목적 운영체제다. 데스크톱 OS와의 가장 근본적인 차이는 <strong>"배터리라는 유한 에너지원 아래에서 최대 성능과 최소 전력 소비 사이의 균형을 실시간으로 조정해야 한다"</strong> 는 점이다.

**필요성 및 등장 배경**
2007년 iPhone과 2008년 Android의 등장 이전에는 Symbian, Windows Mobile, BlackBerry OS 등이 모바일 시장을 분할하고 있었다. 그러나 이들은 데스크톱 OS를 축소하거나 기능 중심으로 설계되어 터치 UI (User Interface), 앱 생태계, 클라우드 연동, 실시간 멀티미디어 처리라는 새로운 요구를 충족하지 못했다. Android는 Google의 오픈 생태계 전략과 다양한 하드웨어 파트너십(OHA, Open Handset Alliance)을 결합하여 시장 점유율 72%를 달성했고, iOS는 Apple의 독자적 칩(AP, Application Processor)과 OS의 긴밀한 통합으로 프리미엄 시장을 장악하며 현재의 양강 구도를 형성했다.

```text
+------------------------------------------------------------------+
|           Android vs iOS 아키텍처 계층 비교                       |
+----------------------+-------------------------------------------+
|      Android         |              iOS                          |
+----------------------+-------------------------------------------+
|                      |                                           |
|  [Java/Kotlin App]   |  [Swift/Obj-C App]                        |
|        v             |        v                                  |
|  [Android Framework] |  [Cocoa Touch / SwiftUI]                  |
|        v             |        v                                  |
|  [ART / Dalvik VM]   |  [Native Runtime (LLVM)]                  |
|        v             |        v                                  |
|  [Native Libraries]  |  [Frameworks (Core ML, Metal)]            |
|        v             |        v                                  |
|  [HAL]               |  [libSystem / Darwin]                     |
|        v             |        v                                  |
|  [Linux Kernel]      |  [XNU Kernel (Mach + BSD + IOKit)]       |
|   (커스터마이징)      |   (독자 커널)                              |
|        v             |        v                                  |
|  [OEM 하드웨어]       |  [Apple Silicon (A/M 시리즈)]             |
+----------------------+-------------------------------------------+
```

**[다이어그램 해설]** 이 계층 비교도에서 가장 눈에 띄는 차이는 Android의 중간 계층에 <strong>ART (Android Runtime) 가상머신</strong>이 존재한다는 점과 iOS가 <strong>XNU 하이브리드 커널</strong>을 사용한다는 점이다. Android는 리눅스 커널 위에 HAL (Hardware Abstraction Layer)과 ART를 올려 다양한 하드웨어에서 호환성을 확보하는 전략이며, iOS는 Apple이 직접 칩과 커널을 설계하여 하드웨어-소프트웨어 간 불필요한 추상화 계층을 최소화하는 전략이다. 이 차이는 성능, 보안, 전력 효율, 그리고 앱 개발 방식 전반에 깊은 영향을 미친다.

- **📢 섹션 요약 비유**: Android와 iOS의 차이는 **'공용 아파트'와 '단독 주택'** 의 차이와 같습니다. 공용 아파트(Android)는 다양한 건설사(OEM)가 지은 건물에 누구나 이사입주할 수 있도록 표준 규격(ART, HAL)을 갖추고 있지만, 그만큼 벽이 두껍고(추상화 계층) 관리비(오버헤드)가 더 듭니다. 반면 단독 주택(iOS)은 설계자(Apple)가 뼈대부터 인테리어까지 직접 설계하여 효율은 높지만, 다른 가구가 임의로 개조할 수 없는 폐쇄적 구조입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 커널 아키텍처 비교

| 특성 | Android (Linux Kernel) | iOS (XNU Kernel) |
|:---|:---|:---|
| <strong>커널 유형</strong> | 모놀리식 (Monolithic) + 커스터마이징 | 하이브리드 (Mach + BSD) |
| **소스 공개** | 오픈 소스 (GPL, GNU General Public License) | 폐쇄 소스 (Apple 독점) |
| **하드웨어 지원** | 다양한 OEM (Samsung, Xiaomi 등) | Apple 기기 전용 |
| <strong>IPC 메커니즘</strong> | Binder (동기 RPC) | Mach Port (메시지 패싱) |
| **전력 관리** | Wakelock + Linux PM (Power Management) | IOKit Power Management |
| **보안 모델** | SELinux + UID 격리 + seccomp | Sandbox + Entitlement + Secure Enclave |
| **드라이버 모델** | LKM (Loadable Kernel Module) + Vendor Module | IOKit Driver Kit (User-space 일부) |

### Android 핵심 메커니즘

**Zygote 프로세스 포킹 (Forking)**
Android는 부팅 시 Zygote라는 마스터 프로세스를 생성하고, 모든 앱은 Zygote를 `fork()`하여 시작된다. 이 방식은 공유 메모리 (Shared Memory)를 통해 런타임 라이브러리를 모든 앱이 공유할 수 있게 하여 메모리 사용량을 크게 줄이고, 앱 시작 시간(Cold Start)을 단축한다. 그러나 fork의 CoW (Copy-on-Write) 특성상 쓰기 작업이 많아지면 메모리가 복제되므로, 메모리 집약적 앱에서는 오히려 오버헤드가 될 수 있다.

<strong>Binder IPC (Inter-Process Communication)</strong>
Android의 시스템 서비스(Activity Manager, Window Manager 등)와 앱 간 통신은 Binder라는 독자적 IPC 메커니즘을 사용한다. Binder는 커널 모듈(`/dev/binder`)로 구현되며, 한 번의 `ioctl()` 시스템 콜로 데이터를 프로세스 간에 전송할 수 있어 기존 UNIX 도메인 소켓(Unix Domain Socket)보다 효율적이다. 그러나 동기적 RPC (Remote Procedure Call) 특성상 호출 스레드가 블록(Block)되므로, ANR (Application Not Responding)을 방지하기 위해 비동기 바인딩(Async Binding)을 활용해야 한다.

### iOS 핵심 메커니즘

<strong>XNU 하이브리드 커널</strong>
XNU (X is Not Unix)는 Apple의 독자 커널로, Mach 마이크로커널의 메시지 패싱 (Message Passing) IPC와 BSD (Berkeley Software Distribution)의 POSIX 호환 계층, 그리고 IOKit 드라이버 프레임워크가 결합된 하이브리드 구조다. Mach 계층은 스레드 스케줄링, 가상 메모리, IPC를 담당하고, BSD 계층은 파일 시스템, 네트워크 스택, POSIX 시스템 콜 호환성을 제공한다.

```text
+------------------------------------------------------------------+
|           프로세스 생명주기 비교 (Process Lifecycle)              |
+------------------------------------------------------------------+
|                                                                  |
|  [Android Process Lifecycle]                                     |
|                                                                  |
|  Foreground -> Visible -> Service -> Background -> Cached -> Killed |
|      |           |          |          |          |              |
|   OOM_ADJ=0   ADJ=100    ADJ=500    ADJ=700   ADJ=900         |
|   (최고 우선)                                                      |
|                                                                  |
|  메모리 부족 시 -> lmkd (Low Memory Killer Daemon)이              |
|                    ADJ값이 높은 순서대로 프로세스를 종료           |
|                                                                  |
|  -------------------------------------------------------------  |
|                                                                  |
|  [iOS Process Lifecycle]                                         |
|                                                                  |
|  Foreground -> Inactive -> Background -> Suspended -> Terminated   |
|      |           |           |           |                       |
|   (실행 중)   (전화 등)   (제한 실행)  (메모리만 점유)           |
|                                                                  |
|  Jetsam 이벤트 -> 커널이 메모리 압박 시                           |
|                   suspended 프로세스를 우선 종료                  |
|                                                                  |
|  ※ 핵심 차이: Android는 서비스(Service)가 백그라운드에서         |
|     지속 실행 가능하지만, iOS는 백그라운드 실행이 엄격 제한됨     |
+------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 생명주기 비교에서 가장 중요한 차이는 백그라운드 처리 방식이다. Android는 Service 컴포넌트를 통해 백그라운드에서 지속적으로 실행되는 프로세스를 허용하지만, iOS는 배터리 보호를 위해 백그라운드 실행을 엄격히 제한하고 대부분의 앱을 Suspended 상태로 전환한다. 이 차이는 Android의 메모리 사용량이 iOS보다 많은 주요 원인이기도 하며, 반대로 iOS의 전력 효율이 높은 핵심 이유이기도 하다.

### 런타임 및 개발 환경 비교

| 항목 | Android | iOS |
|:---|:---|:---|
| **런타임** | ART (AOT + JIT 프로파일링) | Native (LLVM 컴파일) |
| **주 언어** | Kotlin / Java | Swift / Objective-C |
| **UI 프레임워크** | Jetpack Compose / View System | SwiftUI / UIKit |
| **메모리 관리** | GC (Garbage Collection) | ARC (Automatic Reference Counting) |
| **앱 포맷** | APK / AAB (Android App Bundle) | IPA (iOS App Store Package) |
| **배포** | Google Play + 사이드로딩 (Sideloading) | App Store (유일 공식 채널) |

- **📢 섹션 요약 비유**: Android의 ART는 **'통역사가 동시통역을 하는 회의'** 와 같고, iOS의 네이티브 런타임은 **'같은 언어를 쓰는 회의'** 와 같습니다. 통역사(ART)가 있으면 다양한 언어(Kotlin, Java)를 쓰는 사람들이 참여할 수 있지만 통역 시간(오버헤드)이 추가되고, 같은 언어(Swift)를 쓰면 소통이 빠르지만 참여자가 제한됩니다.

---

## Ⅲ. 비교 및 연결

### 보안 모델 심층 비교

| 보안 영역 | Android | iOS | 평가 |
|:---|:---|:---|:---|
| **앱 샌드박스** | UID 기반 Linux 샌드박스 + SELinux MAC | Entitlement 기능 샌드박스 + XNU Sandbox | iOS가 더 엄격 |
| <strong>커널 보호</strong> | seccomp-bpf (시스템 콜 필터링) | KPP (Kernel Patch Protection) | iOS가 하드웨어 수준 보호 |
| **암호화** | File-Based Encryption (FBE) | Data Protection (클래스 기반) | 유사한 수준 |
| <strong>앱 검증</strong> | Google Play Protect + 서명 검증 | App Store 심사 + 공증(Notarization) | iOS가 사전 심사 강력 |
| **보안 칩** | TEE (TrustZone) 기기별 상이 | Secure Enclave (Apple 독자) | iOS가 일관된 보안 칩 |
| **루팅/탈옥** | OEM Unlock -> 루팅 가능 | Checkm8 등 부팅 체인 익스플로잇 | Android가 상대적으로 개방 |

```text
+------------------------------------------------------------------+
|        보안 아키텍처 계층 비교 (Security Stack Comparison)        |
+------------------------------------------------------------------+
|                                                                  |
|  Android                          iOS                            |
|  ---------                        ---------                      |
|  [Google Play Protect]            [App Store Review]             |
|       v                                v                         |
|  [App Sandbox (UID)]              [Sandbox (Entitlements)]       |
|       v                                v                         |
|  [SELinux Policy]                 [XNU Sandbox MAC]             |
|       v                                v                         |
|  [seccomp-bpf]                    [KPP/Secure Enclave]          |
|       v                                v                         |
|  [Linux Kernel]                   [XNU Kernel]                  |
|       v                                v                         |
|  [TEE (TrustZone)]                [Secure Enclave Coprocessor]  |
|       v                                v                         |
|  [OEM 하드웨어]                    [Apple Silicon]               |
|                                                                  |
|  ※ 핵심 차이: Android는 보안 계층이 OEM마다 다를 수 있지만,     |
|     iOS는 Apple이 전체 스택을 통제하여 일관된 보안 보장           |
+------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 보안 스택 비교에서 핵심은 <strong>"보안의 일관성"</strong> 이다. Android는 다양한 OEM이 하드웨어와 펌웨어를 제조하므로, TEE (Trusted Execution Environment)의 구현이 기기마다 다르고 SELinux 정책도 커스터마이징될 수 있다. 반면 iOS는 Apple이 칩(AP)부터 Secure Enclave, 커널, 런타임, 앱스토어까지 전체 스택을 통제하므로, 보안 모델의 일관성과 검증 가능성이 훨씬 높다. 그러나 이는 동시에 **단일 공급자 의존(Single Vendor Dependency)** 의 위험도 가져온다.

### 전력 관리 전략 비교

| 전력 관리 | Android | iOS |
|:---|:---|:---|
| **백그라운드 제한** | Doze + App Standby (기기별 상이) | 엄격한 백그라운드 실행 제한 |
| **CPU 절전** | Wakelock / cpuidle / HMPscheduler | Clustering + Performance Controller |
| **디스플레이** | Variable Refresh Rate (OEM 구현) | ProMotion (120Hz 적응형) |
| **네트워크** | JobScheduler / WorkManager | Background Tasks (엄격 한도) |
| **열 관리** | OEM별 thermal-engine | Apple 독자 thermal throttling |

- **📢 섹션 요약 비유**: Android의 보안은 **'여러 브랜드 자물쇠를 조합한 금고'** 와 같고, iOS의 보안은 **'하나의 브랜드가 설계부터 시공까지 담당한 금고'** 와 같습니다. 전자는 다양한 선택지와 커스터마이징이 가능하지만 약한 고리(Weak Link)가 생길 위험이 있고, 후자는 일관된 품질이 보장되지만 한 회사의 설계 결함이 치명적일 수 있습니다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오별 선택 기준

<strong>시나리오 1: 기업 MDM (Mobile Device Management) 도입</strong>
- **Android 장점**: 다양한 가격대 기기 선택, Samsung Knox와 같은 엔터프라이즈 보안 플랫폼, 커스텀 ROM 배포 가능
- **iOS 장점**: 일관된 보안 정책 적용, 빠른 OS 업데이트 전파 (5년+ 지원), Apple Business Manager를 통한 기기 관리 간소화
- **판단**: 보안이 최우선이면 iOS, 기기 다양성과 비용 절감이 필요하면 Android (Samsung Knox 권장)

**시나리오 2: 실시간 멀티미디어 애플리케이션 개발**
- **Android 장점**: NDK (Native Development Kit)를 통한 C/C++ 네이티브 코드 직접 실행, 오픈 소스 미디어 프레임워크
- **iOS 장점**: Metal 그래픽 API 직접 접근, Core ML의 Neural 엔진 활용, 낮은 오디오 레이턴시
- **판단**: 레이턴시 민감도가 높으면 iOS (Hardware-Accelerated Pipeline), 다양한 코덱 지원이 필요하면 Android

<strong>시나리오 3: IoT (Internet of Things) 기기 운영체제 선택</strong>
- **Android 장점**: Android Things (비록 deprecated되었으나) -> AOSP (Android Open Source Project) 기반 커스터마이징 가능, 풍부한 드라이버 생태계
- **iOS 장점**: HomeKit 프레임워크로 Apple 생태계 내 IoT 제어 (단, iOS 자체를 IoT 기기에 탑재 불가)
- **판단**: IoT 기기에 OS를 탑재해야 하면 Android (AOSP 기반), Apple 생태계 내 액세서리 제조는 HomeKit MFi (Made for iPhone) 인증 필요

```text
+------------------------------------------------------------------+
|        모바일 OS 선택 의사결정 매트릭스                           |
+---------------+--------------+--------------+-------------------+
|  평가 기준    | Android      | iOS          | 판단 포인트       |
+---------------+--------------+--------------+-------------------+
| 보안 일관성   | 중간 (OEM별) | 높음 (통합)  | 규제 산업은 iOS   |
| 하드웨어 다양 | 높음         | 낮음 (Apple) | BYOD 환경은 Android|
| 앱 성능       | 중간~높음    | 높음         | 실시간 처리는 iOS |
| 전력 효율     | 중간         | 높음         | 배터리 중시는 iOS |
| 커스터마이징  | 높음         | 낮음         | 임베디드는 Android|
| 업데이트 속도 | 느림 (OEM)   | 빠름 (직접)  | 패치 긴급성은 iOS |
| 개발 비용     | 높음 (파편화)| 중간         | 테스트 비용 고려  |
| 라이선스      | AOSP 무료   | Apple 유료   | 대량 배포는 Android|
+---------------+--------------+--------------+-------------------+
```

**[다이어그램 해설]** 이 매트릭스는 특정 프로젝트나 조직의 요구에 따라 Android와 iOS 중 어느 것을 우선 선택해야 하는지를 정량적으로 판단하는 기준을 제공한다. 핵심은 **"하나의 OS가 모든 면에서 우월하지 않다"** 는 점이다. 보안 일관성과 업데이트 속도에서 iOS가 우세하지만, 하드웨어 다양성과 커스터마이징에서는 Android가 압도적으로 유리하다. 따라서 실무에서는 비즈니스 요구사항에 따라 가중치를 부여하여 종합 판단해야 한다.

### 안티패턴 (Anti-Patterns)

| 안티패턴 | 위험 | 올바른 접근 |
|:---|:---|:---|
| **iOS 보안 맹신** | 탈옥(Jailbreak) 기기에서 앱 데이터 노출 | Device Check API + 앱 무결성 검증 |
| **Android 파편화 무시** | 다양한 화면 크기/API 레벨에서 크래시 | CI/CD (Firebase Test Lab) 자동화 테스트 |
| **백그라운드 남용** | 배터리 급소모 -> 사용자 앱 삭제 | WorkManager(Android) / BG Tasks(iOS) 준수 |
| **네이티브 코드 과도 사용** | 보안 검증 어려움, 업데이트 지연 | 플랫폼 API 우선, 네이티브는 성능 병목에만 |

- **📢 섹션 요약 비유**: 모바일 OS 선택은 **'자동차 구매'** 와 같습니다. 모든 도로(사용 사례)에서 완벽한 자동차는 없습니다. 고속도로(성능)에서는 스포츠카(iOS), 험로(커스터마이징)에서는 SUV(Android)가 적합하며, 목적과 예산과 운전자의 기술(개발팀 역량)에 따라 최적의 선택이 달라집니다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

모바일 OS 생태계는 다음 방향으로 진화하고 있다. 첫째, Android는 Mainline Modules (Project Mainline)을 통해 OS 핵심 컴포넌트를 모듈화하여, OEM 업데이트 지연 없이 Google이 직접 보안 패치를 배포하는 방향으로 발전하고 있다. 둘째, iOS는 Apple Silicon의 통합 아키텍처를 활용하여 Mac(macOS)과 iOS 앱이 공통 플랫폼에서 실행되는 통합 생태계(Catalyst, Mac Catalyst)를 확장하고 있다. 셋째, 양쪽 모두 온디바이스 AI (On-device AI)를 강화하고 있으며, Android는 NNAPI (Neural Networks API), iOS는 Core ML과 Neural 엔진을 통해 기기 내 AI 추론(Inference) 성능을 극대화하고 있다.

### 참고 표준

- <strong>Android Compatibility Definition Document (CDD)</strong>: Google이 정의한 Android 기기 호환성 요구사항
- **Apple Human Interface Guidelines (HIG)**: iOS 앱 설계 및 UI/UX 표준 가이드라인
- <strong>OWASP Mobile Security Testing Guide (MSTG)</strong>: 모바일 앱 보안 테스트 표준 방법론
- <strong>ISO/IEC 27034 (Application Security)</strong>: 애플리케이션 보안 관리 국제 표준

- **📢 섹션 요약 비유**: 모바일 OS의 미래는 <strong>'스마트 홈의 중앙 허브'</strong> 가 되어가고 있습니다. 과거에는 단순히 전화와 앱을 실행하는 기기였지만, 이제는 웨어러블, 자동차, 스마트 홈 기기, AR (Augmented Reality) 기기까지 제어하는 생태계의 중심으로 진화하고 있어, OS의 선택이 단일 기기를 넘어 전체 디지털 라이프 스타일을 결정짓는 요소가 되고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| I/O 성능 병목 (Bottleneck) 탐색법 (iostat, vmstat) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 캐시 미스 오버헤드 측정 분석망 구조 적용 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 안드로이드 리눅스 커널 커스터마이징 (Wakelock 전력 통제 모듈) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| ART (Android Runtime) AOT/JIT 컴파일러 혼합 실행 환경 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[캐시 미스 오버헤드 측정 분석망 구조 적용]
    |
    v
[모바일 OS 특징 (Android vs iOS 아키텍처 비교)]
    |
    +---> [안드로이드 리눅스 커널 커스터마이징 (Wakelock 전력 통제 모듈)]
    +---> [ART (Android Runtime) AOT/JIT 컴파일러 혼합 실행 환경]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스마트폰 안에는 작은 컴퓨터(운영체제)가 살고 있어요. <strong>안드로이드</strong>는 여러 회사(Samsung, Xiaomi 등)가 만든 다양한 집에 누구나 이사 올 수 있는 **'공용 아파트'** 예요.
2. **아이폰(iOS)** 은 Apple이라는 한 회사가 집 설계부터 가구까지 모두 직접 만드는 **'주문제작 단독주택'** 이에요. 그래서 집이 튼튼하고 효율적이지만, 다른 회사 가구는 잘 안 맞아요.
3. 두 집 모두 장점이 있어서, 어떤 집에 살지는 가족(사용자)이 무엇을 가장 중요하게 생각하는지(다양성 vs 편리함)에 따라 결정해요!
