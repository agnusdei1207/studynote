+++
title = "644. 제로 트러스트 (Zero Trust) 아키텍처의 하드웨어 루트 오브 트러스트"
date = "2026-03-14"
weight = 644
+++

### # [주제명] 제로 트러스트(Zero Trust) 아키텍처의 하드웨어 루트 오브 트러스트(Hardware Root of Trust)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 제로 트러스트(Zero Trust)의 "신뢰하지 않음(Never Trust, Always Verify)" 철학을 실현하기 위해서는 소프트웨어 검증의 한계를 넘어선, 변경 불가능한 하드웨어적 신뢰의 기점(Root of Trust, RoT)이 필수적입니다.
> 2. **가치**: 펌웨어(Firmware) 및 부팅 단계의 변조를 방지하여, 최상위 ID 인증(IDaaS/IAM)과 결합된 진정한 의미의 디바이스 무결성(Device Integrity)과 지속적 인증(Continuous Authentication)을 제공합니다.
> 3. **융합**: TPM(Trusted Platform Module), TEE(Trusted Execution Environment) 등의 HW 기술과 ZTNA(Zero Trust Network Access)가 융합되어, 클라우드 및 엣지 환경에서의 데이터 유출 방어와 컨피덴셜 컴퓨팅(Confidential Computing) 기반을 구축합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 제로 트러스트(Zero Trust)의 패러다임 전환
기존의 보안 모델은 네트워크 경계(Perimeter)를 기반으로 하는 "성과 해자(Castle and Moat)" 모델이었습니다. 내부 사용자는 기본적으로 신뢰한다는 가정하에 방화벽(Firewall)과 VPN(Virtual Private Network)이 주요 방어선이었습니다. 그러나 클라우드(Cloud) 컴퓨팅의 도입, 재택근무 등의 업무 환경 변화, 그리고 APT(Advanced Persistent Threat) 공격의 진화로 경계는 무의미해졌습니다. 이에 따라 NIST(National Institute of Standards and Technology) SP 800-207에서 정의한 바와 같이, **제로 트러스트(Zero Trust, ZT)**는 "자원에 대한 접근을 요청하는 모든 주체(Principal)와 애플리케이션에 대해 신뢰를 선행하지 않고 매번 요청 시마다 엄격하게 인증 및 인가(Authentication and Authorization)를 수행"하는 아키텍처로 자리 잡았습니다.

#### 2. 소프트웨어 기반 신뢰의 붕괴와 HW RoT의 등장
제로 트러스트 제어부(Policy Decision Point, PDP)는 접속 요청 시 사용자의 신원뿐만 아니라 단말기(Device)의 보안 상태(Health Check)를 판단합니다. 하지만 이 판단의 근거가 되는 OS(Operating System)나 에이전트(Agent) 정보 자체가 변조되었다면 어떨까요? 공격자가 관리자 권한(Root/Admin)을 탈취하여 OS 커널(Kernel)이나 펌웨어(Firmware) 레벨에서 악성코드를 심는다면, 보안 소프트웨어는 "나는 안전합니다"라는 거짓 정보를 보고할 것입니다. 이러한 **Lying Agent(거짓말하는 에이전트)** 문제를 해결하기 위해, 소프트웨어 계층보다 아래에 있으며 물리적으로 조작이 불가능한 **하드웨어 루트 오브 트러스트(Hardware Root of Trust, RoT)**가 필수적인 기반 요소로 대두되었습니다.

| 구분 | 전통적 경계 보안 (Perimeter Security) | 제로 트러스트 (Zero Trust) |
| :--- | :--- | :--- |
| **신뢰 대상** | 네트워크 위치 (내부망 = 신뢰) | 없음 (Never Trust) |
| **검증 시점** | 최초 접속 시 (One-time) | 모든 요청 시 (Always Verify) |
| **디바이스 신뢰** | 네트워크 연결성 위주 | HW 무결성 및 상태 기반 검증 |
| **주요 위협** | 외부 침입 | 내부자 위협, 자격 증명 탈취, 트러스트 된 디바이스의 감염 |

#### 3. 섹션 요약 비유
📢 **섹션 요약 비유**: 제로 트러스트는 공항의 보안 검색대와 같습니다. 과거에는 일단 공항 건물(내부망) 안에 들어오면 안전했다면, 이제는 탑승 게이트마다, 그리고 기관에 들어설 때마다 신분증과 짐을 다시 검사합니다. 하지만 검색대 요원(소프트웨어)이 위조된 여권을 진짜로 못 알아보거나, 요원 자체가 매수당했다면 보안은 무너집니다. 하드웨어 RoT는 누구도 손댈 수 없는 금고 속에 보관된 '원본 데이터베이스'를 이용해 여권을 검증하는, 절대 부패하지 않는 자동화 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 하드웨어 루트 오브 트러스트(RoT)의 정의와 구조
하드웨어 RoT는 시스템의 무결성(Integrity)과 신뢰성(Trustworthiness)을 보장하는 시작점(Anchor)입니다. 칩(Silicon) 레벨에서 구현되며, 일반적으로 CPU 내부에 통합되거나 별도의 MCU(Micro Controller Unit) 형태로 존재합니다. 이는 일반 메모리와 완전히 분리된 격리된 실행 환경(Isolated Execution Environment)을 제공합니다.

하드웨어 RoT는 크게 세 가지 핵심 기능(RoT Triad)으로 정의됩니다.

1.  **RoT for Measurement (RTM)**: 부팅 과정에서 펌웨어, 부트로더(Bootloader), OS 커널 등의 암호학적 해시(Hash) 값을 측정(Calculate)하는 기능.
2.  **RoT for Storage (RTS)**: 암호화 키(Keys), 인증서(Certificates), 그리고 측정된 해시 값(PCR Values)을 변조 불가능한 저장소(NVRAM)에 보관하는 기능.
3.  **RoT for Reporting (RTR)**: 외부 검증자(Verifier)에게 시스템의 상태와 무결성 증명(Attestation)을 위한 디지털 서명(Digital Signature)을 생성하고 보고하는 기능.

#### 2. 하드웨어 RoT 구조 다이어그램

아래 다이어그램은 시스템 부팅 시 하드웨어 RoT가 어떻게 신뢰 사슬을 형성하는지를 보여줍니다.

```text
[ Layer 0: Hardware Root of Trust (Silicon) ]
   +---------------------------------------------------------------+
   |  [ Immutable Boot ROM ]          (코드 수정 불가, 신뢰의 기원) |
   |          |                                                   |
   |          v                                                   |
   |  [ Root of Trust for Measurement ]  (첫 번째 코드 Hash 측정)  |
   |          |                                                   |
   |          v (Verify Signature)                                |
   |  [ Root of Trust for Storage ]       (EK, SRK, PCR Keys 저장)  |
   +---------------------------------------------------------------+
                        |
                        | (신뢰 전달: Trust Chain)
                        v
[ Layer 1: Firmware / UEFI ]
   +---------------------------------------------------------------+
   |  [ UEFI/BIOS Code ] ----(Hash 측정 및 PCR 확장)---> [ TPM ]   |
   |          |                                                   |
   |          v (Verify Signature)                                |
   |  [ Bootloader (GRUB/IPL) ]                                   |
   +---------------------------------------------------------------+
                        |
                        v
[ Layer 2: Operating System (OS) ]
   +---------------------------------------------------------------+
   |  [ OS Kernel / Driver ] ----(Hash 측정 및 PCR 확장)---> [ TPM ]|
   |          |                                                   |
   |          v                                                   |
   |  [ Application / Security Agents ]                           |
   +---------------------------------------------------------------+
```

**다이어그램 해설**:
이 구조의 핵심은 **신뢰의 연쇄적 전달(Chain of Trust)**입니다. 가장 아래에 있는 수정 불가능한 Boot ROM이 가장 먼저 실행되며, 그 바로 위 단계인 UEFI 펌웨어의 서명을 검증합니다. 검증이 성공하면 제어권을 넘기고, 펌웨어는 다시 부트로더를 검증합니다. 이 과정에서 각 단계별 코드의 해시(Hash) 값은 PCR(Platform Configuration Register)이라는 레지스터에 누적(Extend)됩니다. 만약 해커가 펌웨어를 1비트라도 변조하면, 최종 PCR 값은 완전히 달라지며 신뢰 사슬은 끊깁니다.

#### 3. 핵심 알고리즘: PCR(Platform Configuration Register) 확장 원리

TPM의 핵심 데이터 구조인 PCR은 무결성 측정값을 저장하는 레지스터입니다. 이 값은 덮어쓰기가 불가능하며 오직 **확장(Extend)** 연산만 가능합니다.

```python
# Pseudo-code for TPM PCR Extend Operation
import hashlib

def pcr_extend(current_pcr_value, new_measurement_hash):
    """
    PCR는 이전 값과 새로운 측정값을 결합하여 다시 해시하는 방식으로 값을 갱신합니다.
    이는 측정 순서(Order)가 보존됨을 보장합니다.
    """
    # 1. 기존 PCR 값과 새로운 Hash를 이어 붙임 (Concatenation)
    combined_data = current_pcr_value + new_measurement_hash
    
    # 2. SHA-256 등의 해시 알고리즘 적용
    new_pcr_value = hashlib.sha256(combined_data).digest()
    
    return new_pcr_value

# Example:
# Initial PCR[0] = 0x00...00
# Firmware Hash = H1
# OS Kernel Hash = H2
# Final PCR = SHA256( SHA256(0x00...00 + H1) + H2 )
```

이 메커니즘 덕분에, 부팅 과정의 어떤 단계에서든 변조가 발생하면 최종 PCR 값은 원본과 완전히 다르게 됩니다.

#### 4. 섹션 요약 비유
📢 **섹션 요약 비유**: 하드웨어 RoT와 신뢰 사슬은 "증명된 도장이 찍힌 서류의 등본"을 연달아 만드는 과정과 같습니다. 첫 번째 직원(Boot ROM)이 자신이 믿는 둘째 직원에게 도장을 찍어주고, 둘째가 셋째에게... 이 과정이 반복됩니다. PCR은 이 모든 도장들이 찍힌 순서대로의 서류 목록입니다. 만약 누군가 중간에 날인을 위조하거나 순서를 바꾸면, 최종 목록의 지문(Fingerprint)은 망가집니다. 하드웨어 RoT는 이 모든 과정이 유리로 된 투명 금고 안에서 일어나도록 강제하는 장치입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 신뢰의 기점 비교: 정적(SRTM) vs 동적(DRTM)

하드웨어 RoT를 통해 신뢰를 구축하는 방식은 크게 두 가지가 있습니다. 제로 트러스트 환경에서는 이 둘의 융합이 중요합니다.

| 비교 항목 | SRTM (Static Root of Trust for Measurement) | DRTM (Dynamic Root of Trust for Measurement) |
| :--- | :--- | :--- |
| **신뢰의 시작점** | 전원이 켜질 때의 하드웨어 고정 ROM (BIOS/UEFI) | OS가 실행 중인 시점의 CPU 명령어 (Intel TXT, AMD SKINIT) |
| **검증 대상** | BIOS → Bootloader → OS → App (순차적) | 메모리 상의 Kernel/OS 이미지 (일시적 중단 후 측정) |
| **장점** | 구현이 쉽고, 초기 부팅 무결성 보장에 강함 | 부팅 후 런타임(Run-time) 환경의 안전한 재검증 가능 |
| **단점** | BIOS/UEFI 자체가 취약할 경우 전체 신뢰 붕괴 | 복잡한 하이퍼바이저(Hypervisor) 지원 필요 |
| **제로 트러스트와의 연계** | **디바이스 기반 신원 확인 (Device ID/Health)** | **지속적인 세션 무결성 모니터링** |

#### 2. 소프트웨어 변조 방지 기술과의 융합

제로 트러스트는 단순히 하드웨어만으로 구축되지 않습니다. 아래 표는 RoT 기술이 상위 계층 보안 기술들과 어떻게 시너지를 발휘하는지 보여줍니다.

| 상위 기술 (Software/Cloud) | 하위 기술 (Hardware RoT) | 융합 효과 (Synergy) | 적용 예시 |
| :--- | :--- | :--- | :--- |
| **IAM / SSO** (Identity & Access) | TPM (Attestation Identity Key) | 디바이스 무결성이 검증된 사용자만 SSO 토큰 발급 | 도난당한 노트북은 정상적인 ID/PW를 입력해도 접속 불가 |
| **ZTNA** (Software-Defined Perimeter) | TEE / Secure Enclave | 인증서 저장소의 물리적 탈취 방지, 키 추출 불가 | 피싱 사이트로 전송된 세션 쿠키라도 TEE 밖에서는 해독 불가 |
| **EDR/XDR** (Endpoint Detection) | Hardware Performance Counters | EDR 에이전트 우회/변조 감지 및 랜섬웨어 차단 | EDR 프로세스가 끊겨도 H/W 카운터로 비정상 행위 탐지 |

#### 3. 섹션 요약 비유
📢 **섹션 요약 비유**: SRTM은 집을 지을 때 '견고한 주춧돌'을 놓는 것과 같습니다. 주춧돌이 바르면 그 위에 쌓는 벽돌(소프트웨어)도 안전합니다. 하지만 주춧돌 자체에 균열이 생기면 집이 무너집니다. 반면 DRTM은 이미 지어진 집에 나쁜 사람이 숨어들었을 때, 건물 전체를 스캔하는 드론을 띄워 실시간으로 구조를 다시 점검하는 것과 같습니다. 제로 트러스트는 이 주춧돌 점검(SRTM)과 드론 정찰(DRTM)을 병행하여 집의 안전을 보장합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 원격 증명(Remote Attestation)을 이용한 접속 제어

현대의 기업 환경에서 재택근무자가 사무용 자산(PC)을 이용해 회사의 핵심 DB에 접속하려 할 때, 제로 트러스트 아키텍처는 하드웨어 RoT를 어떻게 활용하는지 시나리오로 분석합니다.

**시나리오**:
1.  **접속 요청**: 사용자가 ID/PW 및 MFA(Multi-Factor Authenticat