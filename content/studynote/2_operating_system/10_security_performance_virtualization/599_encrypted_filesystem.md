+++
weight = 599
title = "599. 암호화 기반 파일 시스템 보안 (Encrypted File System)"
+++

### 💡 핵심 인사이트 (Insight)
1. **데이터 정지 시 보안 (Data-at-Rest)**: 파일 시스템 암호화는 디스크가 물리적으로 탈취되거나 인가되지 않은 운영체제(Live OS 등)로 부팅되었을 때, 민감한 데이터가 노출되는 것을 방지하는 최후의 방어선입니다.
2. **투명한 암호화 (Transparent Encryption)**: 사용자나 애플리케이션은 평소와 다름없이 파일을 읽고 쓰지만, 운영체제 하단에서 실시간으로 암/복호화가 이루어지도록 설계되어 편의성과 보안성을 동시에 제공합니다.
3. **키 관리의 중요성**: 암호화 알고리즘 자체보다 암호화에 사용되는 마스터 키를 어떻게 생성하고, 안전하게 보관(TPM 등 활용)하느냐가 시스템 전체의 보안 수준을 결정합니다.

---

## Ⅰ. 파일 시스템 암호화의 분류
### 1. 전 디스크 암호화 (FDE: Full Disk Encryption)
부트로더를 제외한 파티션 전체를 암호화합니다. 파일 메타데이터(이름, 크기)와 OS 시스템 파일까지 모두 보호합니다. (예: BitLocker, LUKS)

### 2. 파일 레벨 암호화 (FLE: File Level Encryption)
개별 파일이나 디렉토리 단위로 암호화합니다. 여러 사용자가 있는 시스템에서 사용자별로 다른 키를 사용하여 데이터를 격리하기에 적합합니다. (예: eCryptfs, Windows EFS)

📢 **섹션 요약 비유**: 전 디스크 암호화는 '건물 전체를 꽁꽁 싸매서 아무도 못 들어오게 하는 것'이고, 파일 레벨 암호화는 '건물 안의 특정 금고들만 따로 잠그는 것'입니다.

---

## Ⅱ. 기술적 작동 메커니즘 (ASCII Diagram)
### 1. I/O 스택 내의 암호화 계층
```text
[User Application]
       |
       | 1. Write Data (Plaintext)
       V
[VFS (Virtual File System)]
       |
       | 2. File System Driver (EXT4, NTFS)
       V
[Encryption Layer (dm-crypt / BitLocker Filter)]
       |
       | 3. AES Encryption (Key from TPM/User Pass)
       |    Plaintext -> Ciphertext
       V
[Generic Block Layer / Disk Driver]
       |
       | 4. Store Ciphertext on Physical Media
       V
[Physical HDD / SSD / NVMe]
```

### 2. 암호화 알고리즘
주로 AES-XTS (Advanced Encryption Standard with XTS mode) 모드를 사용하며, 이는 디스크 블록 단위의 암호화에 최적화되어 데이터 패턴 노출을 최소화합니다.

📢 **섹션 요약 비유**: 암호화 계층은 '우체국에서 편지를 부치기 전, 내용을 암호문으로 바꿔서 봉투에 담아주는 비밀 요원'과 같습니다.

---

## Ⅲ. 키 관리 및 신뢰의 뿌리 (Root of Trust)
### 1. 계층적 키 구조
- **FEK (File Encryption Key)**: 실제 데이터를 암호화하는 대칭키.
- **MEK (Master Encryption Key)**: FEK를 암호화하여 저장하는 키. 사용자 패스워드나 TPM에 의해 보호됩니다.

### 2. 하드웨어 연동 (TPM/HSM)
키를 소프트웨어적으로 메모리에 보관하는 대신, TPM(Trusted Platform Module) 칩 내부에 안전하게 봉인(Sealing)하여 하드웨어 분실 시에도 키 유출을 막습니다.

📢 **섹션 요약 비유**: 키 관리는 '보물상자 열쇠(FEK)를 다시 작은 상자(MEK)에 넣고, 그 작은 상자 열쇠를 은행 금고(TPM)에 보관하는 것'과 같습니다.

---

## Ⅳ. 주요 구현 기술 및 도구
### 1. Linux: LUKS (Linux Unified Key Setup)
dm-crypt 커널 모듈을 기반으로 하며, 하나의 파티션에 여러 개의 키 슬롯을 제공하여 다양한 패스워드로 접근할 수 있는 표준을 제공합니다.

### 2. Windows: BitLocker & EFS
- **BitLocker**: 드라이브 전체를 암호화하며 TPM과 강력하게 결합.
- **EFS**: NTFS 파일 시스템의 특성을 이용해 사용자별 폴더 암호화 제공.

### 3. macOS: FileVault
애플의 T2/M1 보안 칩과 연동하여 고성능 하드웨어 가속 암호화를 수행합니다.

📢 **섹션 요약 비유**: LUKS와 BitLocker는 '각 나라를 대표하는 국가 공인 튼튼한 금고 브랜드'와 같습니다.

---

## Ⅴ. 성능 및 가용성 고려사항
### 1. 성능 오버헤드
암/복호화 연산에 CPU 자원이 소모되지만, 현대 CPU는 AES-NI(Instruction Set) 명령어를 통해 성능 저하를 거의 체감할 수 없을 정도로 최소화합니다.

### 2. 데이터 복구 (Recovery)
키를 분실하면 데이터 복구가 원천적으로 불가능하므로, 복구 키(Recovery Key)를 안전한 별도 장소에 보관하거나 기업용 시스템에서는 키 복구 에이전트(KRA)를 운영합니다.

📢 **섹션 요약 비유**: 암호화 시스템은 '완벽한 방패지만, 주인이 열쇠를 잃어버리면 영원히 못 여는 양날의 검'이 될 수도 있습니다.

---

### 📌 지식 그래프 (Knowledge Graph)
- [TPM 및 보안 부트](./596_tpm_secure_boot.md) → 암호화 키를 안전하게 보관하기 위한 하드웨어 기반
- [운영체제 보안 목표 - CIA](./581_os_security_cia.md) → 파일 시스템 암호화의 주 목적 (기밀성 보장)
- [능력 기반 보안](./600_capability_based_security.md) → 파일 접근 권한 자체를 제어하는 또 다른 방식

### 👶 아이를 위한 3줄 비유 (Child Analogy)
1. **상황**: 내가 쓴 비밀 일기장을 동생이 몰래 훔쳐볼까 봐 걱정돼요.
2. **원리**: 그래서 일기장에 나만 아는 특별한 외계어(암호화)로 일기를 쓰고, 마법 열쇠(TPM)로 잠가두었어요.
3. **결과**: 동생이 일기장을 가져가도 무슨 내용인지 하나도 읽을 수 없어서 내 비밀은 안전해요!
