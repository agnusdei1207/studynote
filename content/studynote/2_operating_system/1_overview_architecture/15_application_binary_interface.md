+++
title = "15. ABI (Application Binary Interface)"
date = "2026-03-14"
weight = 15
+++

# ABI (Application Binary Interface)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ABI (Application Binary Interface)는 운영체제와 응용 프로그램 (또는 라이브러리 간)이 상호작용하는 규약으로, 소스 코드가 아닌 **컴파일이 완료된 바이너리 (Binary, 기계어) 수준**에서 데이터 구조, 함수 호출 방식, 레지스터 사용 규칙 등을 정의한 이진 인터페이스다.
> 2. **가치**: 서로 다른 컴파일러로 빌드된 소프트웨어 모듈들이 하나의 시스템에서 충돌 없이 연동될 수 있게 하며, 하드웨어 아키텍처 (x86, ARM 등)와 운영체제 환경에 따른 실행 파일의 물리적 호환성을 결정하는 결정적 요인이 된다.
> 3. **융합**: 소스 코드 호환성을 다루는 API (Application Programming Interface)와 달리, ABI (Application Binary Interface)는 실행 시점의 '바이너리 호환성 (Binary Compatibility)'을 다루며, 에뮬레이션 (Emulation) 기술이나 시스템 보안 패치 시 반드시 고려해야 할 저수준 설계 표준이다.

---

## Ⅰ. 개요 (Context & Background)

- **개념**: ABI (Application Binary Interface)는 기계어 수준에서 프로그램 부품들이 어떻게 소통할 것인지를 정한 하드웨어 종속적 약속이다. 함수를 호출할 때 인자를 어느 레지스터에 넣을지, 리턴값은 어디서 받을지, 메모리 정렬은 어떻게 할지 등을 0과 1의 관점에서 규정한다.
- **💡 비유**: ABI (Application Binary Interface)는 공장에 있는 톱니바퀴들이 서로 맞물려 돌아가기 위한 **규격화된 톱니의 모양과 굵기 (물리적 치수)**와 같다. API (Application Programming Interface)가 두 나라 사람이 대화하기 위한 '공통 언어 (문법)'라면, ABI (Application Binary Interface)는 두 기계 장치가 결합되기 위한 '나사산의 간격과 크기'다. 언어가 같아도 규격이 다르면 조립이 불가능하다.
- **등장 배경**: 초기 컴퓨팅 환경에서는 같은 C 소스 코드라도 컴파일러 제조사마다 함수 파라미터를 넘기는 방식 (예: 스택에 넣느냐, 레지스터에 넣느냐)이 제각각이었다. 이로 인해 A사 컴파일러로 만든 라이브러리를 B사 프로그램에서 쓸 수 없는 심각한 파편화가 발생했고, 이를 해결하기 위해 CPU (Central Processing Unit) 아키텍처와 OS (Operating System) 벤더가 표준 ABI (Application Binary Interface)를 제정하게 되었다.

- **📢 섹션 요약 비유**: 서로 다른 회사가 만든 스마트폰 충전기 (바이너리)가 규격화된 USB-C 단자 (ABI)를 통해 모두 호환되는 것과 같은 물리적 결합 표준과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### API와 ABI의 적용 시점 및 계층 분석

API (Application Programming Interface)는 개발자가 코드를 '작성'하는 시점의 약속이고, ABI (Application Binary Interface)는 그 코드가 '기계어로 변환되어 실행'되는 시점의 약속이다.

```text
 ┌───────────────────────────────────────────────────────────────┐
 │               소스코드에서 실행 파일까지: API vs ABI 계층           │
 ├───────────────────────────────────────────────────────────────┤
 │                                                               │
 │   [ 소스 코드 (Source Code) ]                                   │
 │       printf("Hello"); ◀──────────────── API 계층 (POSIX 등) │
 │                                          (소스 호환성 보장)    │
 │           │                                                   │
 │           ▼  (컴파일러: GCC, Clang, MSVC)                       │
 │                                                               │
 │   [ 이진 파일 (Binary / Machine Code) ]                         │
 │       MOV RDI, 0x401010  (문자열 주소)                          │
 │       CALL printf@PLT                                         │
 │       ...                ◀──────────────── ABI 계층 (System V) │
 │                                          (실행 호환성 보장)    │
 │           │                                                   │
 │           ▼  (OS 로더 및 링커)                                  │
 │                                                               │
 │   [ 운영체제 커널 (OS Kernel) / CPU ]                            │
 └───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 소스 코드 레벨에서 `printf`를 쓰는 규칙 (API)이 동일하더라도, 컴파일러가 이를 기계어로 바꿀 때 첫 번째 인자인 "Hello" 문자열 주소를 `RDI` 레지스터에 넣을지 혹은 `ECX` 레지스터에 넣을지는 해당 플랫폼의 ABI (Application Binary Interface) 규약에 따라 결정된다. 만약 라이브러리는 `RDI`를 기대하는데 실행 파일은 `ECX`에 값을 넣고 호출한다면, 프로그램은 런타임에 쓰레기 값을 출력하거나 크래시 (Segmentation Fault)가 발생하게 된다.

### ABI (Application Binary Interface)를 구성하는 핵심 요소

| 구성 요소 | 역할 | 상세 동작 내용 | 비유 |
|:---|:---|:---|:---|
| **호출 규약 (Calling Convention)** | 함수 인자 전달 규칙 | 인자를 레지스터에 넣을 순서, 스택 정리 주체 (Caller/Callee) 결정 | 바통 터치 규칙 |
| **데이터 타입 및 정렬** | 메모리 레이아웃 정의 | `int`의 크기 (4/8 Byte), 8/16바이트 경계 정렬 규칙 정의 | 벽돌 쌓기 규격 |
| **시스템 호출 인터페이스** | 커널 진입 규약 | 시스템 호출 번호 위치, Trap 명령어 종류 (`SYSCALL`/`SYSENTER`) | 게이트 통과 절차 |
| **이진 파일 포맷** | 실행 파일 구조 | ELF (Linux), PE (Windows), Mach-O (macOS) 구조 정의 | 제품 포장 박스 |

1. **호출 규약 (Calling Convention)**: x86-64 시스템의 대표적인 ABI (Application Binary Interface)인 'System V ABI'는 인자 6개까지 `RDI`, `RSI`, `RDX`, `RCX`, `R8`, `R9` 레지스터를 순서대로 사용하도록 강제한다.
2. **이진 호환성 (Binary Compatibility)**: ABI (Application Binary Interface)가 유지된다면, OS (Operating System) 커널이 업데이트되어도 기존에 빌드된 실행 파일은 재컴파일 없이 그대로 실행될 수 있다.

- **📢 섹션 요약 비유**: 축구 경기에서 선수들이 서로의 이름 (API)을 몰라도 '공을 발로 차고 골대에 넣는다'는 물리적 규칙 (ABI)을 공유하기 때문에 처음 만난 선수들끼리도 경기가 가능한 것과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### API vs ABI 명확한 비교 분석표

| 비교 항목 | API (Application Programming Interface) | ABI (Application Binary Interface) |
|:---|:---|:---|:---|
| **대상 레벨** | 소스 코드 (Source Code) | 바이너리 (Binary / 기계어) |
| **적용 시점** | 코딩 및 컴파일 (Build-time) | 실행 및 런타임 (Run-time) |
| **표준 예시** | POSIX, Win32 API, Java API | System V ABI, ARM EABI, MS x64 ABI |
| **종속성** | OS 표준에 종속 | **CPU 아키텍처 + OS 환경**에 절대 종속 |
| **변경 시 파급** | 재컴파일 필요 (Source Compatibility) | **재컴파일 없이도 실행 불가** (Binary Fragility) |
| **주요 관련 도구** | IDE, 컴파일러, 헤더 파일 | 링커, 로더, 디버거 (GDB), 리버싱 도구 |

### 과목 융합 관점: 보안 및 리버스 엔지니어링
- **보안 (Security)**: 버퍼 오버플로우 (Buffer Overflow) 공격 시, 공격자는 해당 시스템의 ABI (Application Binary Interface) 호출 규약을 파악하여 리턴 주소를 변조하고 레지스터에 특정 값을 세팅하는 쉘코드를 작성한다.
- **리버스 엔지니어링 (Reversing)**: 디컴파일러가 기계어 코드를 보고 "아, 이 레지스터 값은 함수의 첫 번째 파라미터구나"라고 판단할 수 있는 근거는 모두 ABI (Application Binary Interface) 규약 덕분이다.

- **📢 섹션 요약 비유**: API (Application Programming Interface)가 요리법 (레시피)을 공유하는 것이라면, ABI (Application Binary Interface)는 완성된 요리가 포장 용기 (바이너리 포맷)에 딱 맞게 들어가서 배달 오토바이 (CPU/OS)에 실릴 수 있도록 규격화하는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오: 애플 M1 (ARM) 전환과 Rosetta 2의 바이너리 번역
- **상황**: Apple이 Mac의 아키텍처를 Intel (x86_64)에서 자체 칩 (ARM64)으로 변경했다. 기존 Intel용으로 빌드된 수만 개의 앱은 ARM64 ABI (Application Binary Interface)와 맞지 않아 실행이 불가능해졌다.
- **판단**: 모든 개발자에게 즉각적인 재컴파일 (API 호환성)을 요구하는 것은 현실적으로 불가능하다.
- **해결**: Apple은 **Rosetta 2**라는 동적 바이너리 번역 (Dynamic Binary Translation) 기술을 도입했다. 이는 실행 직전에 x86_64 ABI 규격의 기계어를 ARM64 ABI 규격으로 실시간 변환해줌으로써, '바이너리 호환성'을 하드웨어적으로 우회하여 생태계를 보호한 성공적인 기술사적 사례다.

### 도입 체크리스트 및 안티패턴
- **체크리스트**: C++로 작성된 동적 라이브러리 (DLL/SO)를 배포할 때, 컴파일러 제조사가 달라도 호환되도록 `extern "C"`를 사용하여 C ABI (Application Binary Interface)를 따르게 했는지 확인하라. (C++는 컴파일러마다 Name Mangling 방식이 달라 ABI 호환성이 매우 취약함)
- **안티패턴**: 속도를 높이기 위해 특정 CPU (Central Processing Unit)의 레지스터를 직접 조작하는 하드코딩된 어셈블리 코드를 프로젝트 전반에 사용하는 행위. 이는 시스템의 ABI (Application Binary Interface)가 조금만 바뀌어도 전체 프로그램이 붕괴되는 결과를 초래한다.

- **📢 섹션 요약 비유**: 110V 가전을 220V 환경에서 쓰기 위해 변압기 (Rosetta 2)를 사용하여 물리적 규격 차이 (ABI)를 극복하고 기기를 작동시키는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### ABI (Application Binary Interface) 표준화의 기대효과

| 구분 | 도입 전 (파편화) | 도입 후 (표준화) | 기대효과 |
|:---|:---|:---|:---|
| **소프트웨어 유통** | 각 컴파일러 버전별로 배포 | 단일 바이너리 배포 가능 | 유통 비용 80% 절감 |
| **시스템 통합** | 라이브러리 간 충돌 빈번 | 안정적인 모듈 결합 | 시스템 안정성 (MTBF) 향상 |
| **이기종 호환** | 아키텍처 변경 시 폐기 | 에뮬레이션/번역 기술 적용 가능 | 소프트웨어 자산 수명 연장 |

- **결론**: ABI (Application Binary Interface)는 소프트웨어가 '이론'을 넘어 '물리적 실체'로서 하드웨어와 결합되는 최후의 약속이다. 우리가 웹에서 내려받은 실행 파일을 더블클릭만으로 즉시 실행할 수 있는 평범한 일상은, 보이지 않는 곳에서 수천 페이지의 ABI (Application Binary Interface) 규약을 철저히 준수한 컴파일러와 OS (Operating System)의 노력 덕분이다.

- **📢 섹션 요약 비유**: 건물 설계도 (API)가 아무리 훌륭해도, 실제 벽돌의 크기와 철근의 굵기 규격 (ABI)이 맞지 않으면 건물을 올릴 수 없는 것처럼, ABI (Application Binary Interface)는 디지털 건축물을 실체화하는 최소한의 물리적 규격입니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **API (Application Programming Interface)**: 소스 레벨의 인터페이스. ABI와 상호 보완적 관계.
- **시스템 호출 (System Call)**: ABI에서 정의하는 가장 핵심적인 커널-사용자 소통 인터페이스.
- **링커와 로더 (Linker & Loader)**: ABI 규격에 맞춰 바이너리를 메모리에 배치하고 결합하는 도구.
- **엔디언 (Endianness)**: ABI에서 규정하는 바이트 저장 순서 (Little/Big Endian).

---

## 👶 어린이를 위한 3줄 비유 설명
1. ABI는 컴퓨터 부품끼리 서로 딱 맞게 끼워지도록 정한 **'물리적 크기 규격'**이에요.
2. API가 설명서라면, ABI는 **진짜 레고 블록의 올록볼록한 구멍 크기**와 같아요. 구멍 크기가 0.1mm라도 다르면 블록은 절대 끼워지지 않죠.
3. 이 약속 덕분에 서로 다른 회사에서 만든 프로그램 부품들이 내 컴퓨터 안에서 사이좋게 합체해서 돌아갈 수 있는 거랍니다!