+++
title = "655. Secure Boot"
date = "2026-03-16"
weight = 655
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Secure Boot", "UEFI", "부팅 보안", "부트로더 서명"]
+++

# Secure Boot

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Secure Boot는 UEFI firmware의 **부팅 체인 무결성 보장 기능**으로, 디지털 서명된 부트로더만 실행하게 하여 **초기 부팅 단계 공격을 방지**한다.
> 2. **가치**: "부트킷(Bootkit) 루트킷이 설치되어도 부팅 시 실행 방지"하며, **Windows 8+ 요구사항**이자 Linux에서도 선택적 지원된다.
> 3. **융합**: UEFI, PKI(인증서), KEK(Key Exchange Key), db(서명된 데이터베이스)와 결합하여 **신뢰할 수 있는 부팅** 환경을 구축한다.

+++

## Ⅰ. Secure Boot의 개요

### 1. 정의
- Secure Boot는 UEFI spec 2.3.1 이후 포함된 기능으로, 부팅 시 **서명된 실행 파일만 로드**한다.

### 2. 등장 배경
- **Bootkit 루트킷 위협**: 부트로더 단계에서 침투
- 2012년 Windows 8과 함께 등장

### 3. 💡 비유: '공항 보안 검색'
- Secure Boot는 **"공항 보안 검색"**과 같다.
- 검증된 여객(서명된 부트로더)만 탑승 허용된다.

- **📢 섹션 요약 비유**: 엘리베이터에 탈 때 보안 카드를 찍는 것과 같아요. 인증된 사람만 엘리베이터를 탈 수 있죠.

+++

## Ⅱ. 동작 원리 (Deep Dive)

### 1. 키 변수
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                 Secure Boot 키 변수                             │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [PK (Platform Key)]                                           │
    │   - 플랫폼 소유자의 키 (예: Dell, HP)                           │
    │   - 최상위 키                                                   │
    │                                                                 │
    │  [KEK (Key Exchange Key)]                                      │
    │   - PK로 서명된 키 교환 키                                     │
    │   - 부트로더 서명자의 공개키 추가/제거 권한                      │
    │                                                                 │
    │  [db (Signature Database)]                                     │
    │   - 신뢰할 수 있는 서명(인증서) 데이터베이스                    │
    │   - Microsoft, Canonical, Red Hat 등                            │
    │                                                                 │
    │  [dbx (Revoked Signature Database)]                            │
    │   - 해지된/신뢰 없는 서명 데이터베이스                          │
    │   - 취약한 키/인증서                                             │
    │                                                                 │
    │  * NVRAM에 저장                                                │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. 검증 과정
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                  Secure Boot 검증 과정                           │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   Power On                                                      │
    │      │                                                         │
    │      ▼                                                         │
    │   [UEFI Firmware] ──서명 확인──▶ [PK/KEK]                     │
    │      │                                                         │
    │      ▼                                                         │
    │   [Bootloader] ──서명 확인──▶ [db/dbx]                        │
    │      │                                                         │
    │      ▼                                                         │
    │   [OS Kernel] ──서명 확인──▶ [db/dbx]                         │
    │      │                                                         │
    │      ▼                                                         │
    │   [Drivers] ──서명 확인──▶ [db/dbx]                           │
    │      │                                                         │
    │      ▼                                                         │
    │   Boot Success ✅ OR Failure ❌                                 │
    │                                                                 │
    │  * 실패 시 부팅 중지                                            │
    └─────────────────────────────────────────────────────────────────┘
```

+++

## Ⅲ. Linux Secure Boot

### 1. 서명된 부트로더
- **shim.efi**: Microsoft 서명된 1단계 부트로더
- **grub.efi**: shim이 서명한 2단계 부트로더
- **Kernel**: distro가 서명한 커널

### 2. 사용자 커널 서명
```bash
# 1. 서명 키 생성
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.key -outform DER -out MOK.der -days 36500

# 2. MOK (Machine Owner Key) 등록
mokutil --import MOK.der

# 3. 재부팅 후 MOK 등록 (UEFI 화면에서)

# 4. 커널/모듈 서명
sign-file sha256 MOK.priv MOK.der /path/to/kernel
```

+++

## Ⅳ. Secure Boot 관리

### 1. UEFI 설정
- 보통 BIOS/UEFI 설정에서 활성화/비활성화

### 2. Linux 도구
```bash
# Secure Boot 상태 확인
mokutil --sb-state

# 키 목록
mokutil --list-enrolled
```

+++

## Ⅴ. 장단점

### 1. 장점
- ✅ 부트킷/루트킷 방지
- ✅ 악성 드라이버 로딩 방지

### 2. 단점
- ❌ 맞춤 커널 서명 필요
- ❌ 듀얼 부팅 시 문제 가능

+++

## Ⅵ. 실무 적용

### 1. 모범 사례
- **데이터 센터**: 활성화 권장
- **개발 머신**: 필요에 따라

### 2. 안티패턴
- **"부팅 안 되는데 Secure Boot 몰랐음"**

+++

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **초기 부팅 보안**: 루트킷 설치 방지

### 2. 미래 전맹
- **Measurement Boot**: PCR 활용

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **신뢰 컴퓨팅**: TPM
- **UEFI**: 펌웨어
- **부팅 과정**: 부팅

+++

## 👶 어린이를 위한 3줄 비유 설명
1. Secure Boot는 **"출입구의 보안 요원"**이에요.
2. 사진(ID/서명)이 맞는 사람만 건물(컴퓨터)에 들여보내죠.
3. 나쁜 사람(악성 코드)은 아무리 위장해도 걸러낸답니다!