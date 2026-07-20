---
title: "Uefi Vs Bios"
date: "2026-04-29"
tags:
  - "studynote-operating-system"
weight: 30
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BIOS(Basic Input/Output System)는 16비트 리얼 모드로 실행되는 레거시 펌웨어로 1MB 이하 주소 공간·MBR 디스크 구조에 묶인다. UEFI(Unified Extensible Firmware Interface)는 32/64비트 보호 모드에서 실행되며 GPT 디스크·2.2TB 이상 용량·Secure Boot를 지원한다.
> 2. **가치**: UEFI의 핵심 혁신은 ① GPU 드라이버 내장으로 그래픽 부팅 화면, ② 네트워크 스택으로 PXE 부팅 고도화, ③ Secure Boot로 부트킷 방지, ④ 빠른 부팅(Fast Boot)이다.
> 3. **판단 포인트**: 현대 서버·PC는 UEFI가 표준이지만, 레거시 BIOS 호환을 위해 CSM(Compatibility Support Module)을 제공한다. Secure Boot 활성화 여부는 악성코드 방어와 커스텀 OS 설치 사이의 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

```text
BIOS 부팅 흐름:
  전원 -> POST -> MBR(512B) -> 부트로더 -> OS 커널

  한계:
  - 16비트 실모드: 1MB 메모리만 접근
  - MBR: 최대 2.2TB 디스크
  - 파티션: 최대 4개 기본 파티션
  - 텍스트 기반 설정 화면

UEFI 부팅 흐름:
  전원 -> SEC -> PEI -> DXE -> BDS -> 부트매니저 -> OS

  장점:
  - 64비트 보호 모드
  - GPT: 최대 9.4ZB 디스크, 128개 파티션
  - GUI 설정 화면, 네트워크 스택, GPU 드라이버
  - Secure Boot: 서명된 부트로더만 실행
```

- **📢 섹션 요약 비유**: BIOS vs UEFI는 구형 피처폰 vs 스마트폰이다. 피처폰(BIOS)은 기본 통화는 되지만 앱·인터넷은 안 된다. 스마트폰(UEFI)은 UI가 풍부하고 Secure Boot(잠금 화면)도 지원한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### UEFI 부팅 단계 (PI Specification)

| 단계 | 영문 | 역할 |
|:---|:---|:---|
| **SEC** | Security | CPU 초기화, 임시 RAM 설정 |
| **PEI** | Pre-EFI Init | 메모리 초기화 |
| **DXE** | Driver Execution | 드라이버 로드, 서비스 초기화 |
| **BDS** | Boot Device Select | 부팅 디바이스 결정 |
| **RT** | Runtime | OS 실행 중 UEFI 런타임 서비스 |
| **AL** | After Life | S3 절전 복귀 등 |

### Secure Boot 흐름

```text
UEFI 펌웨어 -> db(허용 서명 목록) 확인
부트로더 서명 검증 -> 성공: 로드
                    -> 실패: 부팅 중단

Microsoft -> Windows 서명 키 포함
Linux    -> shim(MOK) 통해 GRUB 서명 검증
커스텀  -> 자체 키 등록 (MOK - Machine Owner Key)
```

- **📢 섹션 요약 비유**: Secure Boot는 공항 보안 검색대다. 여권(서명)이 유효한 승객(부트로더)만 탑승(부팅)할 수 있다. 서명 없는 부트로더는 악성 부트킷일 수 있어서 차단한다.

---

## Ⅲ. 비교 및 연결

| 비교 | BIOS | UEFI |
|:---|:---|:---|
| 실행 모드 | 16비트 실모드 | 32/64비트 보호 모드 |
| 디스크 | MBR (최대 2.2TB) | GPT (최대 9.4ZB) |
| 파티션 수 | 4개 | 128개 |
| Secure Boot | ❌ | ✅ |
| GUI 설정 | ❌ (텍스트) | ✅ |
| 부팅 속도 | 느림 | 빠름 (Fast Boot) |

- **📢 섹션 요약 비유**: BIOS vs UEFI는 도서관 카드 목록함 vs 전산화된 OPAC 시스템이다. 카드 목록함(BIOS)은 직접 손으로 찾아야 하고 느리다. OPAC(UEFI)은 빠른 검색·GUI·보안 로그인을 지원한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 디스크 구조: MBR vs GPT

```text
MBR (Master Boot Record):
  +- 512바이트 섹터 0
      +- 부트 코드 (446B)
      +- 파티션 테이블 (64B, 4엔트리)
      +- 시그니처 (2B: 0x55AA)

GPT (GUID Partition Table):
  +- 섹터 0: 보호 MBR
  +- 섹터 1: GPT 헤더 (CRC32 체크섬)
  +- 섹터 2-33: 128개 파티션 엔트리
  +- 마지막 섹터: 백업 GPT 헤더
```

### 서버 환경 UEFI 고려사항

```text
- Secure Boot: 서버 OS 서명 키 등록 필요
- iSCSI/PXE 부팅: UEFI 네트워크 스택 활용
- TPM 2.0: UEFI Secure Boot + TPM = 측정 부팅 (Measured Boot)
- 가상화: VM에서 UEFI 부팅 (OVMF 오픈소스 UEFI)
```

- **📢 섹션 요약 비유**: UEFI Secure Boot + TPM은 공항 + 여권 + 얼굴 인식이다. UEFI(공항)가 서명(여권)을 확인하고, TPM(얼굴 인식)이 부팅 과정 전체를 측정하여 무결성을 보장한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **보안 강화** | Secure Boot로 부트킷 차단 |
| **대용량 디스크** | GPT로 2.2TB 한계 초과 |
| **빠른 부팅** | Fast Boot, POST 간소화 |

ARM 기반 서버(AWS Graviton, Ampere Altra)와 임베디드 시스템에서는 U-Boot 같은 경량 부트로더가 UEFI 역할을 하며, UEFI의 복잡성 없이 빠른 부팅을 제공한다.

- **📢 섹션 요약 비유**: ARM 서버의 U-Boot는 경량 스마트폰 부트로더다. UEFI(안드로이드 같은 풀 스택)보다 가볍고 빠르게 부팅하지만, 일부 고급 기능은 없다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **GRUB** | UEFI 부트로더 표준 (Linux) |
| <strong>TPM 2.0</strong> | UEFI Secure Boot와 연계 |
| <strong>GPT</strong> | UEFI 디스크 파티션 표준 |
| <strong>Secure Boot</strong> | 부트킷·루트킷 방어 |
| **U-Boot** | ARM 임베디드 경량 부트로더 |

### 📈 관련 키워드 및 발전 흐름도

```text
[BIOS — 16비트 레거시 펌웨어, MBR]
    |
    v
[UEFI — 64비트 현대 펌웨어, GPT, Secure Boot]
    |
    v
[Secure Boot + TPM — 측정 부팅, 무결성 보장]
    |
    v
[Confidential Computing — AMD SEV, Intel TDX]
    |
    v
[ARM/RISC-V 부팅 — U-Boot, EDK2, 오픈 펌웨어 표준화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. BIOS는 구형 피처폰이에요 — 전화는 되지만 앱은 없어요!
2. UEFI는 스마트폰이에요 — 예쁜 화면, 빠른 부팅, 잠금 화면(Secure Boot)이 있어요!
3. Secure Boot는 공항 보안 검색대예요 — 서명이 없는 프로그램은 컴퓨터를 부팅할 수 없어요!
