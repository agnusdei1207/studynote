---
title: "ARM TrustZone"
date: "2026-03-20"
tags:
  - "studynote-computer-architecture"
weight: 479
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ARM TrustZone은 ARM 프로세서와 시스템 버스에 Secure/Non-secure 구분을 도입해, 하나의 SoC (System on Chip) 안에서 보안 세계와 일반 세계를 하드웨어 수준으로 분리하는 플랫폼 격리 기술이다.
> 2. **가치**: 별도 보안 칩 없이도 모바일 결제, 생체 인증, 안전한 부팅, IoT 기기 키 저장을 구현할 수 있어 ARM 생태계의 사실상 표준 TEE (Trusted Execution Environment) 기반이 되었다.
> 3. **판단 포인트**: TrustZone의 강점은 시스템 전반 분리에 있지만, Secure World가 비대해지면 검증 부담도 커지므로 Secure Monitor·보안 서비스·주변기기 배치를 최소화해야 한다.

---

## Ⅰ. 개요 및 필요성

ARM TrustZone은 하나의 ARM 기반 시스템을 일반 세계와 보안 세계로 나누어, 민감한 코드와 자원을 보안 세계에서만 다루게 만드는 하드웨어 보안 확장이다. 단순한 권한 비트 하나를 더한 기능이 아니라 CPU 상태, 메모리 접근, 인터럽트, 주변기기 라우팅까지 함께 바꾸는 시스템형 격리 구조다. 그래서 TrustZone은 앱 하나를 감싸는 샌드박스보다 더 넓은 범위를 다룬다.

이 기술이 필요해진 배경은 모바일과 임베디드 기기의 모순 때문이다. 한쪽에서는 Android 같은 복잡한 운영체제를 올려 풍부한 기능을 제공해야 하고, 다른 한쪽에서는 카드 토큰·지문 템플릿·부팅 키처럼 절대로 새면 안 되는 자산을 같은 칩에서 처리해야 했다. 별도 보안 프로세서를 넣는 방법도 있지만 비용과 전력, 통합 복잡도가 커지므로, ARM은 메인 프로세서 자체에 이중 세계 모델을 넣는 방향을 택했다.

아래 그림은 TrustZone이 "하나의 칩 안에 두 개의 세계를 만든다"는 점을 보여 준다.

```text
+----------------------------------------------------------------------------+
|                ARM TrustZone의 핵심: 한 SoC 안의 두 개 세계               |
+----------------------------------------------------------------------------+
|                    ARM Core + Interconnect                                 |
|                           |                                                |
|        +------------------+------------------+                             |
|        v                                     v                             |
| Normal World                           Secure World                        |
| +- 일반 운영체제 (Rich OS)              +- 보안 운영체제 / Monitor          |
| +- 일반 앱                              +- Trusted Service                 |
| +- 일반 드라이버                        +- 키 저장, 인증, 결제             |
|        |                                     |                             |
|        +--------------- 하드웨어 분리 -------+                             |
|                        메모리 · 주변기기 · 인터럽트                        |
+----------------------------------------------------------------------------+
```

TrustZone은 그래서 "일반 OS를 조금 더 안전하게 만드는 기능"이 아니라, 일반 OS가 손상되어도 핵심 비밀을 끝까지 분리하기 위한 장치다. 다만 보안 세계에 너무 많은 서비스를 몰아넣으면 그 세계도 결국 또 하나의 큰 운영체제가 되어 버린다. 필요성은 강하지만, 설계는 항상 절제되어야 한다.

- **📢 섹션 요약 비유**: TrustZone은 같은 건물 안에 일반 사무실과 특수 금고 구역을 따로 만드는 것과 같다. 건물은 하나지만, 출입 규칙과 보안 수준은 완전히 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

TrustZone의 핵심 제어점은 NS (Non-Secure) 비트다. 프로세서는 현재 실행 흐름이 Secure 상태인지 Non-secure 상태인지 표시하고, 이 비트가 시스템 버스와 컨트롤러까지 전달되어 메모리·주변기기 접근 권한을 결정한다. ARMv8-A 기준으로는 EL3 (Exception Level 3)가 보안 상태 전환과 초기 설정을 담당하며, Secure Monitor Call로 세계 전환이 이뤄진다.

실제 시스템에서는 CPU만 나눠서는 충분하지 않다. 메모리는 TZASC (TrustZone Address Space Controller) 같은 주소 공간 제어기로, 주변기기는 TZPC (TrustZone Protection Controller) 또는 SoC별 보안 컨트롤러로, 인터럽트는 GIC (Generic Interrupt Controller)의 Secure/Non-secure 라우팅으로 나눠야 한다. 즉 TrustZone의 진짜 본체는 "CPU + 시스템 패브릭 전체의 분리 정책"이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| NS (Non-Secure) 비트 | 현재 실행 세계 구분 | 모든 접근 판단의 기본 태그 |
| EL3 / Secure Monitor | 세계 전환과 초기 보안 설정 | 코드 크기를 최소화해야 한다. |
| TZASC | 메모리 영역의 Secure/Non-secure 분리 | DMA와 DRAM 분할까지 고려해야 한다. |
| GIC (Generic Interrupt Controller) | 인터럽트 라우팅 | 보안 주변기기 인터럽트 누수 방지 |

아래 그림은 TrustZone에서 접근 권한이 어떻게 나뉘는지를 한눈에 보여준다.

```text
+----------------------------------------------------------------------------+
|               TrustZone 접근 행렬: Secure는 넓고, Normal은 제한적이다      |
+----------------------------------------------------------------------------+
| 현재 상태        접근 대상            결과                                  |
| -------------------------------------------------------------------------- |
| Secure World  --> Secure Memory      허용                                  |
| Secure World  --> Normal Memory      허용                                  |
| Secure World  --> Secure Peripheral  허용                                  |
|                                                                            |
| Normal World  --> Normal Memory      허용                                  |
| Normal World  --> Secure Memory      차단                                  |
| Normal World  --> Secure Peripheral  차단                                  |
|                                                                            |
| World 전환: SMC (Secure Monitor Call) -> EL3 처리 -> 문맥 저장/복원          |
+----------------------------------------------------------------------------+
```

이 구조 덕분에 지문 센서, 키 저장소, DRM 경로처럼 반드시 보호해야 할 자원은 Secure World에만 연결할 수 있다. 반대로 일반 앱은 Rich OS를 통해 서비스를 요청하되, 실제 비밀 데이터에는 닿지 못한다. 그래서 TrustZone은 TEE를 구현하는 대표 수단이 된다.

- **📢 섹션 요약 비유**: TrustZone의 NS 비트는 건물 출입증 색깔과 같다. 파란 출입증은 일반 구역만, 빨간 출입증은 보안 구역까지 들어가게 해 주며, 문과 엘리베이터가 그 색을 보고 통과 여부를 정한다.

---

## Ⅲ. 비교 및 연결

TrustZone은 Intel SGX 같은 Enclave 방식과 자주 비교된다. TrustZone은 시스템 전체를 두 세계로 나누는 구조라서 모바일 기기처럼 "운영체제 전체와 보안 서비스 전체를 분리"하는 데 유리하다. 반면 SGX는 프로세스 일부만 떼어 보호하므로 서버 애플리케이션의 특정 계산 구간을 보호하는 데 더 적합하다.

| 구분 | ARM TrustZone | Intel SGX | Secure Element |
| :-- | :-- | :-- | :-- |
| 격리 단위 | 시스템 수준의 두 세계 | 프로세스 수준 Enclave | 별도 보안 칩 |
| 장점 | 모바일/임베디드 통합이 쉽다 | 세밀한 애플리케이션 격리 | 물리 분리가 강하다 |
| 약점 | Secure World 코드 기반이 커지기 쉽다 | EPC 제약, 인터페이스 복잡성 | 비용·성능·연동 부담 |
| 대표 용도 | 결제, DRM, IoT 보안 | 기밀 컴퓨팅 | 카드, eSIM, 키 저장 |

TrustZone은 Secure Boot와도 강하게 엮인다. Secure Boot가 Secure Monitor와 보안 운영체제가 정상 서명본인지 확인해야 보안 세계 자체가 신뢰를 얻는다. 또한 PSA (Platform Security Architecture)나 OP-TEE (Open Portable Trusted Execution Environment) 같은 생태계 요소는 TrustZone을 실제 제품 설계 언어로 바꿔 주는 역할을 한다.

즉 TrustZone은 단독 제품이 아니라 ARM 플랫폼 보안의 뼈대다. Secure Boot가 신뢰 시작점을 만들고, TrustZone이 보안 서비스를 수용하며, TPM이나 원격 증명이 그 상태를 밖에 증명하는 식으로 연결된다.

- **📢 섹션 요약 비유**: TrustZone은 건물을 두 구역으로 나누는 설계이고, SGX는 사무실 안 금고 서랍을 여러 개 두는 설계다. 둘 다 비밀을 지키지만, 공간을 나누는 방식이 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서 TrustZone을 쓸 때 가장 중요한 판단은 Secure World를 얼마나 작게 유지하느냐다. 결제 토큰 생성, 디바이스 키 보호, 안전한 OTA (Over-the-Air) 업데이트 검증처럼 꼭 필요한 기능만 Secure World에 넣어야 한다. UI, 네트워크 스택, 복잡한 파일 시스템까지 보안 세계에 끌고 들어오면 성능보다 먼저 검증과 유지보수가 무너진다.

### 적용 체크리스트

1. <strong>Secure 서비스 범위</strong>: 정말 비밀 연산만 Secure World에 올렸는가?
2. **메모리 분할**: TZASC 설정으로 DRAM과 DMA 경로가 제대로 분리되었는가?
3. **주변기기 배치**: 지문 센서, 키 스토리지, 보안 타이머가 Secure 쪽으로 라우팅되는가?
4. **전환 비용 관리**: SMC 호출이 잦아 성능 병목이 생기지 않는가?
5. <strong>초기 무결성</strong>: Secure Boot가 EL3 펌웨어와 TEE OS를 검증하는가?

### 피해야 할 안티패턴

- Secure World에 일반 서비스까지 잔뜩 올려 "또 다른 큰 OS"를 만드는 설계
- 보안 메모리는 나눴지만 DMA 차단을 빼먹는 설계
- Non-secure 로그나 디버그 포트로 Secure 상태 정보를 과다 노출하는 설계

실무 관점에서 TrustZone의 정답 포인트는 "하드웨어 분리"와 "작은 보안 세계"를 동시에 말하는 데 있다. 하나만 강조하면 반쪽 설명이 된다. Secure World가 너무 크면, 하드웨어 분리의 장점이 검증 복잡도에 묻혀 버린다.

- **📢 섹션 요약 비유**: TrustZone 운영은 VIP실을 만드는 일과 같다. 꼭 필요한 손님만 들어가게 해야지, 일반 손님까지 다 넣어 버리면 VIP실도 결국 일반 홀과 다를 바 없어진다.

---

## Ⅴ. 기대효과 및 결론

TrustZone의 가장 큰 효과는 범용 SoC에서 보안 전용 기능을 실용적으로 구현할 수 있게 했다는 점이다. 덕분에 스마트폰, 스마트카드 대체 결제, 셋톱박스 DRM, 자동차 ECU, IoT 게이트웨이까지 하나의 프로세서 안에서 비용과 보안을 균형 있게 맞출 수 있었다. 즉 TrustZone은 ARM 기반 기기에서 "보안을 옵션이 아니라 기본 기능"으로 만드는 데 큰 역할을 했다.

하지만 한계도 분명하다. Secure World는 하나뿐인 경우가 많아 여러 서비스가 같은 신뢰 경계를 공유하게 되고, 벤더 구현 품질에 따라 공격면이 달라진다. 또한 사이드 채널, 결함 주입, 취약한 Trusted Application은 여전히 현실적인 위협이다. 최근 ARM CCA (Confidential Compute Architecture)가 Realm 같은 더 세분화된 영역을 제안하는 것도 이러한 한계를 보완하기 위해서다.

결국 TrustZone은 "ARM 기기의 보안 별실"로 기억하면 정확하다. 전체 시스템을 두 세계로 나눠 핵심 비밀을 보호하지만, 그 별실 안을 얼마나 작고 단순하게 유지하느냐가 실제 보안 수준을 결정한다.

- **📢 섹션 요약 비유**: TrustZone은 집 안의 비밀 방과 같다. 비밀 방을 만드는 것만으로 끝나지 않고, 그 안에 꼭 필요한 물건만 두어야 방이 진짜 안전해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| TEE (Trusted Execution Environment) | TrustZone은 ARM 계열 TEE를 구현하는 대표 하드웨어 기반이다. |
| NS (Non-Secure) 비트 | 현재 실행 세계를 나타내는 기본 태그로 모든 접근 판단에 관여한다. |
| EL3 (Exception Level 3) | 세계 전환과 초기 보안 설정을 담당하는 특권 레벨이다. |
| TZASC (TrustZone Address Space Controller) | 메모리 영역을 Secure/Non-secure로 나누는 핵심 컨트롤러다. |
| OP-TEE | TrustZone 위에서 널리 쓰이는 오픈소스 TEE 운영 환경이다. |
| Secure Boot | Secure Monitor와 보안 운영체제의 초기 무결성을 보장한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
ARMv6/ARMv7 TrustZone 도입
        |
        v
모바일 TEE · Secure Monitor · Secure OS
        |
        v
생체 인증 · 결제 · DRM 서비스 통합
        |
        v
IoT/자동차용 PSA (Platform Security Architecture) 확장
        |
        v
ARM CCA (Confidential Compute Architecture) · Realm 분리
```

이 흐름은 "두 세계 분리"에서 출발해 "더 세분화된 하드웨어 기밀 실행"으로 진화하는 방향을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. TrustZone은 한 집 안에 일반 방과 비밀 방을 따로 만드는 기술이에요.
2. 비밀 방 열쇠가 있는 사람만 중요한 상자를 만질 수 있어서, 거실이 어지러워져도 상자는 안전해요.
3. 그래서 스마트폰은 같은 칩을 쓰면서도 돈과 지문 같은 중요한 정보를 따로 지킬 수 있어요.
