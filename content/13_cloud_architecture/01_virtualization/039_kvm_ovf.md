---
title: "Kernel-based Virtual Machine & Open Virtualization Format"
date: "2026-03-04"
tags:
  - "studynote-cloud-architecture"
weight: 39
---
> **핵심 인사이트**
> 1. KVM(Kernel-based Virtual Machine)은 Linux 커널에 내장된 하이퍼바이저로, 하드웨어 가상화 지원(Intel VT-x/AMD-V)을 활용하여 최소 오버헤드로 완전 가상화를 제공하며, QEMU와 결합하여 OpenStack·AWS Nitro·Google Cloud의 기반 기술로 사용된다.
> 2. OVF(Open Virtualization Format)는 VMware·Red Hat·IBM 등이 공동 개발한 가상 어플라이언스 패키징 표준으로, 하이퍼바이저 독립적인 VM 이미지 배포를 가능하게 하는 인터오퍼러빌리티의 핵심이다.
> 3. KVM의 핵심 구성 요소는 커널 모듈(kvm.ko) + QEMU(에뮬레이터) + libvirt(관리 API)의 3계층 — 이 분리 구조 덕분에 컨테이너(Docker/Kubernetes)와 공존하며 클라우드 인프라의 실질적 기반이 되었다.

---

## I. KVM 아키텍처

```
KVM (Kernel-based Virtual Machine, 2007):
  Linux 커널 모듈 (kvm.ko, kvm-intel.ko)
  Type 1 하이퍼바이저 (베어메탈 수준 성능)

구성 요소:
  +-------------------------------------+
  |           Guest OS (VM)             |
  |  앱  앱  앱                         |
  +--------------+----------------------+
                 | QEMU-KVM
  +--------------v----------------------+
  |     Linux 커널 (KVM 모듈)           |
  |  kvm.ko: CPU/메모리 가상화          |
  |  QEMU: I/O 에뮬레이션               |
  +--------------+----------------------+
                 |
  +--------------v----------------------+
  |     하드웨어 (Intel VT-x/AMD-V)     |
  +-------------------------------------+

libvirt:
  KVM/QEMU 관리 API
  virsh, virt-manager, OpenStack 인터페이스
```

> 📢 **섹션 요약 비유**: KVM은 아파트 건물(Linux 커널) 안에 독립된 집(VM)을 만드는 것 — 건물 관리인(kvm.ko)이 CPU/메모리 자원 배분.

---

## II. KVM 가상화 메커니즘

```
하드웨어 지원 가상화:

Intel VT-x (Virtualization Technology):
  VMX Root Mode (하이퍼바이저):
    Ring -1 수준 (모든 하드웨어 접근)
  VMX Non-Root Mode (게스트):
    Ring 0~3 실행 가능 (but 제어됨)

중요 가상화 요소:
  CPU 가상화: VT-x로 게스트가 Ring 0 실행
  메모리 가상화: EPT(Extended Page Table)
    게스트 물리 주소 -> 호스트 물리 주소
    하드웨어 MMU 지원으로 오버헤드 최소화

  I/O 가상화:
    완전 에뮬레이션 (QEMU): 범용, 느림
    반가상화 (virtio): 게스트 드라이버 필요, 빠름
    SR-IOV: 하드웨어 직접 공유 (NIC 등)

성능:
  네이티브 대비 KVM 오버헤드: CPU ~1%, 메모리 ~1~3%
  (virtio 사용 시 I/O 오버헤드도 ~5% 수준)
```

> 📢 **섹션 요약 비유**: Intel VT-x는 VM이 "진짜 CPU를 사용하는 것처럼" 느끼게 해주는 특수 모드 — 마치 훈련 시뮬레이터가 실제 조종 감각을 주는 것.

---

## III. OVF / OVA 표준

```
OVF (Open Virtualization Format):
  DMTF 표준 (VMware, Red Hat, IBM, Oracle)
  하이퍼바이저 독립적 VM 패키징

OVF 패키지 구성:
  .ovf (설명자): XML 기반 VM 메타데이터
    CPU, 메모리, 디스크, 네트워크 사양
  .vmdk/.qcow2 (디스크 이미지)
  .mf (매니페스트): 무결성 체크섬

OVA (Open Virtual Appliance):
  OVF 패키지를 하나의 TAR 파일로 압축
  배포·전송이 편리

활용:
  VM 이미지를 VMware ESXi -> KVM으로 이전
  또는 VMware <-> Hyper-V 교차 배포

변환:
  virt-v2v: VMware/Hyper-V -> KVM 변환
  qemu-img convert: vmdk -> qcow2 변환

예:
  ovftool --targetType=OVA vm.ovf vm.ova
  virt-v2v -i ova vm.ova -o local -of qcow2
```

> 📢 **섹션 요약 비유**: OVA는 VM의 이사 박스 — 어느 집(하이퍼바이저)에서든 열어서 그대로 설치 가능한 표준 패키징.

---

## IV. QEMU-KVM과 libvirt

```
QEMU (Quick Emulator):
  KVM 없이도 동작하는 에뮬레이터
  KVM과 결합 시: QEMU = I/O 에뮬레이션
                  KVM = CPU/메모리 가속

virtio (반가상화 드라이버):
  virtio-net: 가상 NIC (네이티브 대비 ~95% 성능)
  virtio-blk: 가상 블록 장치
  virtio-scsi: SCSI 에뮬레이션

libvirt API:
  virsh vm 관리 CLI:
    virsh list --all
    virsh start myvm
    virsh snapshot-create-as myvm snap1

  Python SDK:
    import libvirt
    conn = libvirt.open('qemu:///system')
    dom = conn.lookupByName('myvm')
    dom.create()  # VM 시작

XML 기반 VM 정의:
  <domain type='kvm'>
    <memory unit='KiB'>1048576</memory>
    <vcpu>2</vcpu>
    <devices>
      <disk type='file' device='disk'>
        <source file='/var/lib/libvirt/images/vm.qcow2'/>
      </disk>
    </devices>
  </domain>
```

> 📢 **섹션 요약 비유**: libvirt는 KVM의 관리 인터페이스 — 개별 컨트롤러(QEMU)를 통일된 API로 묶어 OpenStack, virt-manager가 사용.

---

## V. 실무 시나리오 — 프라이빗 클라우드 구성

```
OpenStack + KVM 프라이빗 클라우드:

인프라:
  물리 서버 10대 (KVM 하이퍼바이저)
  OpenStack: Nova(컴퓨팅) + Neutron(네트워크)

VM 프로비저닝 흐름:
  1. 사용자: API로 VM 생성 요청
  2. Nova: 스케줄러로 최적 호스트 선택
  3. libvirt: 선택된 호스트에 KVM VM 시작
  4. Neutron: VM에 가상 네트워크 연결
  5. 사용자: SSH로 VM 접속

OVF를 이용한 마이그레이션:
  VMware 환경 -> OpenStack(KVM) 이전
  1. VMware에서 VM을 OVA로 내보내기
  2. virt-v2v로 OVA -> qcow2 변환
  3. OpenStack Glance에 이미지 업로드
  4. Nova로 VM 시작

라이브 마이그레이션:
  virsh migrate --live myvm qemu+ssh://host2/system
  -> VM 중단 없이 호스트 간 이동 (메모리 페이지 전송)
  -> 유지보수를 위한 핵심 기능
```

> 📢 **섹션 요약 비유**: libvirt migrate는 달리는 기차의 승객을 다른 기차로 옮기기 — VM을 끄지 않고 다른 서버로 이동 (라이브 마이그레이션).

---

## 📌 관련 개념 맵

```
KVM & OVF
+-- KVM 구성
|   +-- kvm.ko (CPU/메모리 가상화)
|   +-- QEMU (I/O 에뮬레이션)
|   +-- libvirt (관리 API)
+-- 가상화 기술
|   +-- Intel VT-x, AMD-V
|   +-- EPT (메모리 가상화)
|   +-- virtio (반가상화 드라이버)
+-- OVF/OVA
|   +-- 하이퍼바이저 독립 패키징
|   +-- .ovf + .vmdk + .mf
+-- 응용
    +-- OpenStack (프라이빗 클라우드)
    +-- AWS Nitro, GCP
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[VMware ESX (1999)]
하이퍼바이저 상용화
      |
      v
[KVM Linux 커널 편입 (2007)]
오픈소스 하이퍼바이저 혁명
      |
      v
[OpenStack 출범 (2010)]
KVM + OpenStack = 프라이빗 클라우드 표준
      |
      v
[컨테이너 부상 (2013~)]
KVM + Docker 공존 (VM + 컨테이너)
      |
      v
[현재: 클라우드 하이브리드]
KVM 기반 AWS Nitro, GCP
VM과 컨테이너를 혼용하는 구조
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. KVM은 Linux 커널 안에서 여러 개의 완전한 컴퓨터(VM)를 만들어 실행하는 기술로, CPU의 가상화 기능 덕분에 거의 실제 속도로 동작해요.
2. OVF/OVA는 VM을 이삿짐처럼 표준 박스에 포장하는 방법 — VMware에서 만든 VM을 KVM에서도 열 수 있게 해주는 공통 표준이에요.
3. OpenStack과 KVM을 결합하면 AWS 같은 프라이빗 클라우드를 회사 안에 직접 구축할 수 있고, VM을 끄지 않고 다른 서버로 이동시키는 라이브 마이그레이션도 가능해요!
