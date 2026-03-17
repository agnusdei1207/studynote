+++
title = "669. Measured Boot (측정 부팅)"
date = "2026-03-16"
weight = 669
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Measured Boot", "PCR", "TPM", "부팅 무결성", "Remote Attestation"]
+++

# 669. Measured Boot (측정 부팅)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Measured Boot (측정 부팅)는 시스템의 **CRTM (Core Root of Trust for Measurement)**부터 시작하여, 부팅 단계별 로딩되는 모든 펌웨어, 로더, 커널의 무결성을 해싱하여 **TPM (Trusted Platform Module)**의 **PCR (Platform Configuration Register)**에 암호학적으로 **기록(Extend)**하는 메커니즘이다.
> 2. **가치**: 단순히 악성 코드 실행을 막는 것을 넘어, "이 시스템이 **언제, 어떤 상태로 부팅되었는가**"라는 이력을 변경 불가능한 **신뢰 루트(RoT)** 저장소에 증명함으로써, **부팅 단계의 은닉 행위(Rootkit 등)**를 근본적으로 차단하고 포렌식을 가능하게 한다.
> 3. **융합**: **Secure Boot (인증 부팅)**와 결합하여 방어 계층을 강화하며, **Remote Attestation (원격 증명)** 프로토콜과 연동하여 클라우드 컴퓨팅, **Zero Trust 네트워크**, 무인 관제 서버의 **신뢰성 검증(Attestation)** 핵심 인프라로 활용된다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**Measured Boot**는 시스템이 전원이 켜진 순간(Power On)부터 운영체제(OS)가 완전히 구동되기 전까지의 모든 실행 코드(BIOS/UEFI, Bootloader, Kernel, Drivers)와 설정값을 암호학적으로 해싱(Hashing)하여, 이를 하드웨어 기반 보안 모듈인 **TPM (Trusted Platform Module)** 내부의 **PCR (Platform Configuration Register)** 레지스터에 누적하여 기록하는 프로세스이다. 이 기술의 철학은 **'측정(Measurement)'**과 **'기록(Recording)'**에 있으며, 실행을 차단하는 것이 아니라 시스템 상태에 대한 **'증명(Attestation)'** 자료를 제공하는 데 있다.

#### 2. 💡 비유: 감시 카메라와 방수 금고가 설치된 보안 구역
Measured Boot는 고도의 보안이 필요한 금고에 들어가는 모든 사람과 물건의 **'디지털 지문(Fingerprint)'**을 찍어서 **'절대 조작 불가능한 방수 금고(TPM)'** 안에 보관하는 것과 같다. 단순히 출입권(Secure Boot)을 확인하는 것을 넘어, 누가(해시 값), 언제(부팅 순서), 무엇을(컴포넌트) 들고 들어왔는지를 블록체인 장부처럼 기록(Extend)한다. 만약 낯선 침입자가 들어왔다면, 비록 문이 열려 있었더라도 침입 사실(무결성 훼손)이 기록에 남기 때문에 나중에 감사(Audit) 시 정확히 언제 침입했는지 추적할 수 있다.

#### 3. 등장 배경 및 역사
① **기존 보안의 한계 (Trust Gap)**: 전통적인 BIOS/MBR 방식이나 초기 Secure Boot는 "실행 허가 여부"만 판단했다. 해커가 정상적인 서명을 가진 취약한 펌웨어를 이용하거나, 관리자가 의도적으로 보안 설정을 낮추는 경우 이를 탐지할 수 없었다. 즉, "시스템이 안전한 상태인지"를 증명할 방법이 부재했다.
② **혁신적 패러다임 (Trusted Computing)**: **TCG (Trusted Computing Group)**는 소프트웨어가 조작될 수 없는 하드웨어 경계인 **TPM**을 도입했다. 특히, 처음 실행되는 코드인 **CRTM (Core Root of Trust for Measurement)**이 스스로를 측정하고 다음 단계를 측정하는 **Chain of Trust (신뢰의 사슬)** 구조를 확립했다.
③ **현재의 비즈니스 요구**: 클라우드 환경과 **IoT (Internet of Things)** 환경에서 "내 데이터가 안전한 서버에서 실행되고 있는가?"라는 문제는 필수적이다. **CSP (Cloud Service Provider)**는 사용자의 데이터를 처리하는 서버가 신뢰할 수 있는 상태임을 증명해야 하며, 이를 위한 **Remote Attestation**의 기반이 바로 Measured Boot이다.

```text
      [ Legacy Boot ]              [ Secure Boot ]              [ Measured Boot ]
+-------------------+      +-------------------+      +-------------------+
| 1. Power On       |      | 1. Power On       |      | 1. Power On       |
| 2. Load BIOS      |      | 2. Verify BIOS    |      | 2. Measure BIOS   | --> Record to TPM
| 3. Load OS        |      | 3. Load OS        |      | 3. Measure OS     | --> Record to TPM
| 4. Run            |      | 4. Run            |      | 4. Run            | --> Can Verify Anytime
+-------------------+      +-------------------+      +-------------------+
    No Verification         Block Malware Only        Full History & Evidence
```

#### 📢 섹션 요약 비유
> 마치 고속도로 진입 요금소에서 단순히 통행권을 확인하는 것(Secure Boot)을 넘어, 모든 차량의 번호, 적재 화물, 진입 시간을 블록체인 원장에 기록하여, 나중에 의심스러운 차량이나 밀반입 사건이 발생했을 때 그 원인과 경로를 정확히 추적할 수 있는 **'블랙박스 및 영상 저장 시스템'**과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
Measured Boot 아키텍처는 **신뢰의 뿌리**인 CRTM에서부터 **하드웨어 격리 저장소**인 TPM, 그리고 **데이터 해석**을 위한 Event Log까지 유기적으로 연결된다.

| 요소명 | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 관련 프로토콜/알고리즘 | 비유 |
|:---|:---|:---|:---|:---|
| **CRTM** | Core Root of Trust for Measurement | 시스템 전원 투입 후 가장 먼저 실행되는 코드(주로 BIOS/UEFI 내부). 자기 자신의 무결성을 검증한 후, 다음 단계 펌웨어를 측정(Measure)하여 TPM으로 전송. 이 과정이 신뢰의 시작점(Root of Trust). | SHA-256 Hashing, TPM_Extend | 공증인의 첫 도장 |
| **TPM** | Trusted Platform Module | CPU와 분리된 독립된 하드웨어 칩. 내부의 PCR 레지스터와 비밀키(EK, AIK)를 보관. 외부 공격으로부터 보호된 실행 환경 제공. | TCG PC Client Platform TPM Profile Specification | 절대 열리지 않는 금고 |
| **PCR** | Platform Configuration Register | TPM 내부의 레지스터(일반적으로 24개, SHA-256 기준 32바이트). `PCR_new = HASH(PCR_old \| New_Hash)` 연산을 통해 값을 업데이트하며, 되돌릴 수 없는(One-way) 특성을 가짐. | Extend 연산 (HMAC) | 수정 불가한 장부 |
| **Event Log** | - | PCR에는 해시 값만 저장되므로, 실제 측정된 파일명, 경로, 해시 값 등의 사람이 읽을 수 있는 정보를 메모리 또는 디스크에 저장. PCR 값과 대조하여 무결성 검증에 사용. | TCG Event Log Format | 장부의 비고 및 명세서 |
| **IMA/EVM** | Integrity Measurement Architecture / Extended Verification Module | 리눅스 커널 레벨의 무결성 측정 프레임워크. 부팅 후 애플리케이션 실행 및 파일 접근 시 실시간으로 측정하여 PCR[10] 등을 확장. 런타임 보안 담당. | LSM (Linux Security Modules), HMAC, Digital Signature | 실시간 감시 카메라 |

#### 2. Measured Boot 신뢰 사슬 (Chain of Trust) 데이터 흐름
아래 다이어그램은 시스템 부팅 시 각 단계별 코드가 측정(Measure)되어 TPM의 PCR 레지스터에 누적(Extend)되는 과정을 도식화한 것이다.

```text
   [ Power-On ]
        |
        v
+----------------------+   Measure (Hash) & Extend (PCR[0])
|      CRTM             | --------------------------> +------------------+
| (Core Root of Trust)  |                               |       TPM        |
+----------------------+                               | (PCR[0]: CRTM)   |
        |                                            +------------------+
        | Load & Execute Next                                     |
        v                                                          |
+----------------------+   Measure (Hash) & Extend (PCR[1])        |
|      UEFI FW         | --------------------------> +------------------+
| (Firmware Volume)    |                               |       TPM        |
+----------------------+                               | (PCR[1]: UEFI)   |
        |                                            +------------------+
        | Load & Execute Next                                     |
        v                                                          |
+----------------------+   Measure (Hash) & Extend (PCR[2~4])      |
|      Bootloader      | --------------------------> +------------------+
| (GRUB / Shim / MBR)  |                               |  TPM (PCR[2-4])  |
+----------------------+                               +------------------+
        |
        | Load & Execute Kernel
        v
+----------------------+   Measure (Hash) & Extend (PCR[5~9])      |
|      OS Kernel       | --------------------------> +------------------+
| (vmlinuz / initrd)   |                               |  TPM (PCR[5-9])  |
+----------------------+                               +------------------+

        |
        | Run Applications
        v
+----------------------+   Runtime Measure (PCR[10])              |
|      App (File)      | --------------------------> +------------------+
| (Executed by IMA)    |                               |  TPM (PCR[10])   |
+----------------------+                               +------------------+

[Key Operation Details]
1. Measure: 현재 컴포넌트(UEFI, Kernel 등)의 코드를 SHA-256으로 해싱.
2. Extend: TPM PCR 레지스터 업데이트.
   PCR_New = SHA256( PCR_Old || Measured_Hash )
   * 이 연산은 가역적이지 않으므로, 이전 단계의 무결성이 현재 단계에 암호학적으로 묶임(Binding).
```

**[다이어그램 해설]**
이 아키텍처의 핵심은 **Extend 연산의 누적성**에 있다.
1. **단계별 계층 구조**: 가장 먼저 실행되는 **CRTM**은 자기 자신을 측정하여 **PCR[0]**에 기록한다. 이것이 루트 신뢰이다. 그 후 다음 단계인 **UEFI 펌웨어**를 로드하기 전에 이를 해싱하여 **PCR[1]**에 기록한다.
2. **암호학적 연결 고리**: 만약 해커가 UEFI 펌웨어를 변조한다면, PCR[1]에 기록되는 해시 값이 변한다. 이 변조된 PCR[1] 값은 다음 단계인 Bootloader 측정 시 PCR[2]를 계산하는 입력값으로 사용되므로, **최종 PCR 값은 폭발적으로 달라진다(Avalanche Effect)**.
3. **최종 증명**: 부팅이 완료된 시점의 PCR 값들은 해당 시스템이 "정상적인 CRTM -> 정상적인 UFI -> ... -> 정상적인 OS" 경로를 밟았는지를 암호학적으로 증명하는 **지문(Fingerprint)**이 된다.

#### 3. 핵심 알고리즘: PCR Extend 상세
PCR 업데이트는 단순 덮어쓰기(Overwrite)가 아니라 이력을 압축하여 포함하는 연산이다. 수식으로 표현하면 다음과 같다.

$$ PCR_{new} = \text{Hash}(PCR_{old} \|\| Digest) $$

- $PCR_{old}$: 이전 단계까지의 누적된 무결성 값 (초기값은 보통 0 or 1)
- $Digest$: 현재 측정하려는 컴포넌트의 해시 값 (예: SHA-256)
- $\|\|$: 바이트 열 연결 (Concatenation)
- $\text{Hash}$: 단방향 해시 함수

**특징**: 이 방식 덕분에 마지막 PCR 값 하나만 가지고도 모든 부팅 과정의 무결성을 역추적할 수 있으며, 중간에 누군가 PCR 값을 조작하려 해도 이전 해시 값을 알 수 없으므로 불가능하다.

#### 4. 실무 코드 스니페트 (TPM Extend 시뮬레이션)
리눅스 커널의 IMA(Integrity Measurement Architecture) 서브시스템에서 파일을 측정하고 PCR을 확장하는 개념적 코드 로직이다.

```c
// 개념적 코드: drivers/security/ima/ima_main.c (간략화)
// 주의: 실제 환경에서는 TPM 커널 드라이버와 TCG 명령어를 사용합니다.

#include <crypto/hash.h>

// PCR Extend 연산 시뮬레이션
// PCR_new = SHA256( PCR_old || Data_Digest )
void simulate_tpm_extend(u8 *pcr_old, const u8 *data_digest, u8 *pcr_new) {
    struct shash_desc *desc;
    u8 combined_buffer[64]; // 32(PCR) + 32(Digest)

    // 1. Combine: PCR_old와 Digest를 연결
    memcpy(combined_buffer, pcr_old, 32);
    memcpy(combined_buffer + 32, data_digest, 32);

    // 2. Hash: SHA-256 연산 수행
    // 실제 TPM 칩 내부에서는 하드웨어적으로 수행되어 외부에서 조작 불가
    sha256_hash(combined_buffer, 64, pcr_new); 
}

// 시스템 호출: 파일 실행 시 측정
void on_file_exec(const char *file_path) {
    u8 file_digest[32];
    u8 current_pcr[32] = {0}; // 예: PCR[10]의 현재값
    
    // 1. 파일 해싱
    compute_file_sha256(file_path, file_digest);
    
    // 2. TPM PCR Extend 요청 (Cryptographic API 호출)
    tpm_pcr_extend(TPM_NUM_PCR10, file_digest);
    
    // 3. 사용자 공간 로그에 기록 (Auditing)
    printk(KERN_INFO "IMA: Measured %s (digest: %pUr)\n", file_path, file_digest);
}
```

#### 📢 섹션 요약 비유
> 마치 거대한 도미노를 세우는 과정과 같습니다. 첫 번째 도미노(CRTM)가 넘어지며 두 번째 도미노(UEFI)를 쓰러뜨립니다. 만약 누군가 중간에 도미노 하나를 다른 모양으로 바꾸어 놓는다면(변조), 그 도미모가 쓰러지는 충격이 달라져서 최종적으로 도달하는 도미노의 위치(PCR 값)가 완전히 달라지게 됩니다. 따라서 우리는 최종 위치만 봐도 중간에 누가 장난을 쳤는지 알