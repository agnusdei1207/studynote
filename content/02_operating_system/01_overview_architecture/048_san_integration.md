---
title: "San Integration"
date: "2026-04-05"
tags:
  - "studynote-operating-system"
weight: 48
---
> **핵심 인사이트**
> 1. SAN(Storage Area Network)은 서버와 스토리지 장치를 전용 고속 네트워크로 연결하는 아키텍처 — 일반 IP 네트워크와 분리된 Fibre Channel 또는 iSCSI 전용 망으로 블록 수준 스토리지를 제공하며, 서버가 스토리지를 로컬 디스크처럼 인식한다.
> 2. SAN의 핵심 가치는 스토리지 통합과 유연한 할당 — 여러 서버가 스토리지 풀을 공유하여 스토리지 활용률을 높이고, 서버 다운 없이 스토리지를 동적으로 재할당할 수 있어 데이터센터 운영 효율을 극대화한다.
> 3. NAS(네트워크 연결 스토리지)와의 결정적 차이 — SAN은 블록 I/O(OS가 파일시스템 관리), NAS는 파일 I/O(스토리지가 파일시스템 제공). 성능 중심 DB·VM은 SAN, 파일 공유는 NAS가 적합하다.

---

## Ⅰ. SAN 아키텍처

```
SAN 구성요소:

[서버 1] [서버 2] [서버 3]
   |         |         |
  HBA       HBA       HBA   (Host Bus Adapter: FC/iSCSI)
   |         |         |
   +----[SAN 스위치 (Fabric)]----+
              |
   +----------+----------+
  [스토리지 1] [스토리지 2] [스토리지 3]
   (LUN)       (LUN)       (LUN)

핵심 컴포넌트:

HBA (Host Bus Adapter):
  서버에 설치되는 스토리지 네트워크 카드
  FC HBA: Fibre Channel 전용 (8/16/32Gbps)
  iSCSI HBA: IP 네트워크 사용

SAN 스위치 (Fabric):
  FC 스위치: Cisco MDS, Brocade
  LAN 스위치와 별개의 전용 패브릭
  포트 수: 16~512포트

LUN (Logical Unit Number):
  스토리지 어레이의 논리적 볼륨
  서버에 블록 장치로 제공
  여러 서버가 같은 LUN 공유 가능

Zoning (존 설정):
  SAN 패브릭에서의 접근 제어
  서버 A -> LUN 1, 2만 접근 허용
  보안 + 트래픽 격리
```

> 📢 **섹션 요약 비유**: SAN은 스토리지 전용 고속도로 — 일반 도로(IP 네트워크)와 분리된 전용 고속도로(FC). 서버들이 창고(스토리지)를 자기 방 서랍처럼 블록 단위로 사용!

---

## Ⅱ. Fibre Channel vs iSCSI

```
Fibre Channel (FC):
  전통적 SAN 프로토콜

  특징:
  전용 FC 패브릭 (IP 네트워크와 분리)
  FC-0 ~ FC-4 계층 구조

  속도: 8G / 16G / 32G / 64Gbps
  지연: < 1마이크로초
  신뢰성: 손실 없는 전송 (Lossless)

  장점:
  초저지연, 고성능
  미션 크리티컬 DB에 적합
  성숙한 기술, 강력한 보안 (Zoning)

  단점:
  전용 인프라 필요 -> 높은 비용
  FC HBA, FC 스위치, FC 케이블
  관리 복잡도 높음

iSCSI (Internet SCSI):
  SCSI 명령을 IP 패킷에 캡슐화

  특징:
  기존 IP 네트워크 활용 가능
  표준 이더넷 NIC 사용 가능

  속도: 10G / 25G / 100Gbps (이더넷 기반)
  지연: 수십~수백 마이크로초

  장점:
  저렴한 구축 비용 (기존 이더넷 활용)
  원거리 스토리지 연결 가능 (WAN)
  관리 단순

  단점:
  FC 대비 지연 높음
  IP 네트워크 혼잡 영향 가능

선택 기준:
  Oracle RAC, MSSQL 미션 크리티컬: FC
  VMware vSAN, 중소기업: iSCSI
  예산 제약 큰 경우: iSCSI

NVMe-oF (NVMe over Fabrics):
  차세대 SAN 프로토콜
  NVMe SSD를 네트워크로 연결
  지연: FC와 동등 또는 초과
  프로토콜: FC-NVMe, NVMe/TCP, NVMe/RoCE
```

> 📢 **섹션 요약 비유**: FC vs iSCSI = 전용 철로 vs 일반 도로 — FC는 KTX 전용 선로(초고속, 고비용). iSCSI는 일반 도로에 화물트럭(적당한 속도, 저비용). 용도에 맞게!

---

## Ⅲ. SAN vs NAS vs DAS

```
3가지 스토리지 아키텍처 비교:

DAS (Direct-Attached Storage):
  서버에 직접 연결된 디스크

  예: 서버 내부 SATA/SAS HDD, 외장 RAID

  장점: 단순, 저지연, 저비용
  단점: 서버 간 공유 불가, 확장성 제한
  적합: 소규모 독립 서버

NAS (Network-Attached Storage):
  파일 수준 스토리지, IP 네트워크

  프로토콜: NFS (Unix/Linux), SMB/CIFS (Windows)

  예: NetApp ONTAP, EMC Isilon, Synology

  장점:
  파일 공유 용이 (다수 클라이언트)
  관리 단순, 저렴

  단점:
  블록 수준 접근 불가
  DB 등 고성능 워크로드 부적합

  적합: 파일 공유, 백업, 아카이브

SAN (Storage Area Network):
  블록 수준 스토리지, 전용 패브릭

  프로토콜: FC, iSCSI, NVMe-oF

  예: EMC VMAX, HPE 3PAR, IBM FlashSystem

  장점:
  고성능 (DB, VM)
  스토리지 통합, 유연한 할당
  스토리지 마이그레이션 (비중단)

  단점:
  높은 구축 비용 및 복잡도

  적합: 엔터프라이즈 DB, VM 스토리지

하이퍼 컨버지드 (HCI):
  SAN + 서버를 소프트웨어 정의로 통합
  VMware vSAN, Nutanix
  -> 전통적 SAN을 대체하는 추세
```

> 📢 **섹션 요약 비유**: DAS/NAS/SAN = 개인 서랍/공용 파일함/전용 창고 — DAS(내 서랍: 빠르지만 혼자), NAS(공용 파일함: 파일 공유), SAN(전용 창고: 블록 단위, 고성능 공유)!

---

## Ⅳ. SAN 스토리지 통합

```
스토리지 통합 (Storage Consolidation):

기존 (Silo 방식):
  서버 1: 내장 디스크 500GB (사용 40%)
  서버 2: 내장 디스크 500GB (사용 30%)
  서버 3: 내장 디스크 500GB (사용 20%)

  총 용량: 1.5TB, 사용: 450GB
  활용률: 30% (낭비!)

SAN 통합 후:
  SAN 스토리지 풀: 1.5TB
  서버 1: LUN 1 (200GB 할당)
  서버 2: LUN 2 (150GB 할당)
  서버 3: LUN 3 (100GB 할당)

  활용률: 30% -> 70%+ (동적 재할당)

LUN 마스킹 & Zoning:
  LUN 마스킹: 스토리지에서 서버별 LUN 접근 제한
  Zoning: FC 스위치에서 포트별 통신 허용

  이중 보안으로 데이터 격리 보장

스토리지 마이그레이션 (무중단):
  서버 다운 없이 LUN 이동

  방법:
  스토리지 레벨 LUN 복사
  멀티패스 I/O (MPIO)로 경로 전환
  기존 LUN 삭제

HA 구성:
  멀티패스 (Multipathing):
  서버 -> [HBA 1] -> [FC 스위치 A] -> 스토리지
  서버 -> [HBA 2] -> [FC 스위치 B] -> 스토리지

  경로 1 장애 -> 경로 2 자동 전환
  Linux: DM-Multipath, Windows: MPIO
```

> 📢 **섹션 요약 비유**: SAN 통합 = 창고 공유 — 회사 부서별 창고(DAS) 대신 큰 공용 창고(SAN). 활용률 30%->70%. 필요할 때 공간 재배분, 서버 꺼지지 않고도 이전!

---

## Ⅴ. 실무 시나리오 — 데이터센터 SAN 구축

```
중견 금융사 SAN 통합 프로젝트:

현황:
  Oracle DB 서버 × 10 (각 DAS 1TB)
  총 스토리지: 10TB, 활용률 35%
  DB 서버 I/O 병목: 초당 IOPS 부족
  스토리지 증설 = 서버 다운 필요

목표:
  무중단 스토리지 확장
  Oracle RAC 구성 (공유 스토리지 필수)
  활용률 개선

SAN 설계:

스토리지: HPE 3PAR 올플래시 20TB
FC 패브릭:
  Cisco MDS 스위치 (이중화)
  32G FC HBA × 2 / 서버 (멀티패스)

LUN 설계:
  DB 데이터: LUN 1~5 (각 2TB)
  DB 로그: LUN 6~10 (각 500GB)
  Oracle RAC 공유 디스크: LUN 11~13

Oracle RAC 구성:
  2개 DB 서버가 동일 LUN 공유
  Clusterware: 동시 접근 조율
  -> 서버 1대 장애 -> 서버 2 자동 이어받기

결과:
  IOPS: DAS 대비 5× 향상 (SSD + 캐시)
  P99 DB 응답시간: 50ms -> 8ms
  활용률: 35% -> 72%
  Oracle RAC: RTO < 30초 달성
  연간 스토리지 비용: 15% 절감

교훈:
  올플래시 SAN이 구식 HDD SAN보다 비용 효율적
  (IOPS 당 비용 비교 시)
  HCI(Nutanix)도 고려했지만 Oracle RAC = SAN 필수
```

> 📢 **섹션 요약 비유**: 금융사 SAN 구축 = 은행 금고 전용 엘리베이터 — 일반 복도(IP)와 분리된 전용 엘리베이터(FC SAN)로 금고(Oracle DB) 연결. 속도 5배, 응답 8ms, 무중단 확장!

---

## 📌 관련 개념 맵

```
SAN (Storage Area Network)
+-- 프로토콜
|   +-- Fibre Channel (FC)
|   +-- iSCSI
|   +-- NVMe-oF
+-- 비교
|   +-- NAS (파일 수준)
|   +-- DAS (직접 연결)
+-- 기능
|   +-- LUN 마스킹 / Zoning
|   +-- 멀티패스 (MPIO)
|   +-- 스토리지 풀링
+-- 발전
    +-- HCI (소프트웨어 정의)
    +-- 클라우드 스토리지
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[DAS 시대 (1990s)]
서버별 독립 스토리지
확장성 제한
      |
      v
[Fibre Channel SAN (1998~)]
ANSI 표준화
엔터프라이즈 스토리지 표준
      |
      v
[iSCSI 표준화 (2003)]
IP 기반 SAN
중소기업 확산
      |
      v
[올플래시 SAN (2012~)]
NVMe SSD 도입
성능 혁신
      |
      v
[HCI + 클라우드 (2015~)]
소프트웨어 정의 스토리지
vSAN, Nutanix
      |
      v
[현재: NVMe-oF + 오브젝트]
초저지연 패브릭
S3 API 통합
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. SAN = 스토리지 전용 고속도로 — 일반 도로(인터넷)와 분리된 전용 도로로 창고(스토리지) 연결. 서버가 창고를 자기 서랍처럼 쓸 수 있어요!
2. FC vs iSCSI = KTX 전용선 vs 일반도로 — FC(초고속 전용선, 비쌈) vs iSCSI(일반 도로, 저렴). 은행 DB는 KTX, 파일 서버는 일반도로!
3. LUN 마스킹 = 창고 열쇠 — 여러 서버가 공유 창고를 써도 각자 자기 칸(LUN)만 열 수 있어요. 남의 데이터에 못 접근!
