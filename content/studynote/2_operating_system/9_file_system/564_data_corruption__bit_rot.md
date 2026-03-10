+++
title = "564. 데이터 파손 (Data Corruption / Bit Rot) 대응 Btrfs 자가 치유(Self-healing) 기능"
weight = 564
+++

# 564. PCIe (PCI Express)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 고속 직렬 확장 버스
> 2. **가치**: 높은 대역폭, 핫 플러그, 스케일러블
> 3. **융합**: GPU, NVMe, 네트워크 카드와 연관

---

## Ⅰ. 개요

### 개념 정의
**PCIe(PCI Express)**는 **고속 직렬 확장 버스 표준**입니다.

### 💡 비유: 초고속 데이터 고속도로
PCIe는 **초고속 데이터 고속도로**와 같습니다. 레인을 늘려 대역폭을 확장합니다.

### PCIe 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                PCIe 구조                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【PCIe 버전】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  버전             레인당 속도        x16 대역폭        특징        │ │   │
│  │  ────             ─────────        ──────────        ────        │ │   │
│  │  PCIe 1.0         250 MB/s         4 GB/s           초기         │ │   │
│  │  PCIe 2.0         500 MB/s         8 GB/s           2배          │ │   │
│  │  PCIe 3.0         985 MB/s         16 GB/s          128b/130b    │ │   │
│  │  PCIe 4.0         1.97 GB/s        32 GB/s          2배          │ │   │
│  │  PCIe 5.0         3.94 GB/s        64 GB/s          2배          │ │   │
│  │  PCIe 6.0         7.88 GB/s        128 GB/s         PAM4         │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【레인 구성】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  레인             핀 수             대역폭 (PCIe 4.0)        용도       │ │   │
│  │  ────             ─────             ───────────────        ────       │ │   │
│  │  x1               18               1.97 GB/s             와이파이     │ │   │
│  │  x2               36               3.94 GB/s             NVMe       │ │   │
│  │  x4               64               7.88 GB/s             NVMe SSD    │ │   │
│  │  x8               98              15.75 GB/s             10GbE       │ │   │
│  │  x16              164             31.51 GB/s             GPU        │ │   │
│  │                                                             │ │   │
│  │  각 레인 = TX(4핀) + RX(4핀) = 8핀 양방향                       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【PCIe vs PCI】                                                      │|
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특성              PCIe               PCI                    │ │   │
│  │  ────              ────               ────                    │ │   │
│  │  전송 방식          직렬 (풀듀플렉스)    병렬 (하프듀플렉스)       │ │   │
│  │  속도              최대 128 GB/s       133 MB/s               │ │   │
│  │  핫 플러그          지원               미지원                   │ │   │
│  │  전압              3.3V/12V           3.3V/5V/12V             │ │   │
│  │  버스 공유          없음 (Point-to-Point) 공유                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                PCIe 상세                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【PCIe 프로토콜 계층】                                               │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  계층              설명                                         │ │   │
│  │  ────              ────                                         │ │   │
│  │  Transaction     TLP (Transaction Layer Packet)               │ │   │
│  │                  Memory Read/Write, I/O, Config               │ │   │
│  │  Data Link       Sequence, CRC, Ack/Nak                       │ │   │
│  │  Physical        128b/130b 인코딩 (Gen3+), GT/s               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【TLP 타입】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  타입              설명                    방향                   │ │   │
│  │  ────              ────                    ────                   │ │   │
│  │  MRd              Memory Read             Request               │ │   │
│  │  MWr              Memory Write            Request               │ │   │
│  │  IORd             I/O Read                Request               │ │   │
│  │  IOWr             I/O Write               Request               │ │   │
│  │  CfgRd            Config Read             Request               │ │   │
│  │  CfgWr            Config Write            Request               │ │   │
│  │  CplD             Completion with Data    Response              │ │   │
│  │  Cpl              Completion              Response              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【PCIe 슬롯 타입】                                                   │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  슬롯             크기              용도                         │ │   │
│  │  ────             ────              ────                         │ │   │
│  │  x1               25mm              사운드, 와이파이              │ │   │
│  │  x4               39mm              NVMe SSD                    │ │   │
│  │  x8               56mm              10GbE, RAID                 │ │   │
│  │  x16              89mm              GPU                         │ │   │
│  │                                                             │ │   │
│  │  하위 호환: x16 슬롯에 x1 카드 삽입 가능                          │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Linux PCIe 장치 확인】                                            │
│  ──────────────────                                                │
│  // PCIe 장치 목록                                                    │
│  $ lspci                                                            │
│  00:00.0 Host bridge: Intel Corporation                             │
│  01:00.0 VGA compatible controller: NVIDIA Corporation              │
│  02:00.0 Non-Volatile memory controller: Samsung NVMe              │
│  03:00.0 Ethernet controller: Intel Corporation                    │
│                                                                     │
│  // 상세 정보                                                         │
│  $ lspci -vv -s 01:00.0                                            │
│  LnkCap: Port #0, Speed 8GT/s, Width x16, ASPM L0s L1             │
│  LnkSta: Speed 8GT/s (ok), Width x16 (ok)                         │
│                                                                     │
│  // 트리 형태                                                        │
│  $ lspci -t                                                         │
│  -[0000:00]-+-00.0                                                  │
│             +-01.0-[01]----00.0                                     │
│             +-02.0-[02]----00.0                                     │
│                                                                     │
│  【PCIe 속도/대역폭 확인】                                            │
│  ──────────────────                                                │
│  // 현재 링크 상태                                                     │
│  $ sudo lspci -vv | grep -E "LnkCap|LnkSta"                        │
│  LnkCap: Speed 8GT/s, Width x16                                    │
│  LnkSta: Speed 8GT/s, Width x16                                    │
│                                                                     │
│  // 협상 속도 (Gen)                                                   │
│  Gen 1 = 2.5 GT/s (PCIe 1.0)                                        │
│  Gen 2 = 5.0 GT/s (PCIe 2.0)                                        │
│  Gen 3 = 8.0 GT/s (PCIe 3.0)                                        │
│  Gen 4 = 16.0 GT/s (PCIe 4.0)                                       │
│  Gen 5 = 32.0 GT/s (PCIe 5.0)                                       │
│                                                                     │
│  【PCIe 설정】                                                        │
│  ──────────────────                                                │
│  // ASPM (Active State Power Management)                           │
│  $ cat /sys/module/pcie_aspm/parameters/policy                     │
│  [default] performance powersave powersupersave                    │
│                                                                     │
│  // ASPM 변경                                                        │
│  $ echo performance | sudo tee /sys/module/pcie_aspm/parameters/policy│
│                                                                     │
│  // PCIe 전원 관리                                                    │
│  $ cat /sys/bus/pci/devices/0000:01:00.0/power/control            │
│  auto                                                                │
│                                                                     │
│  【NUMA 노드 확인】                                                   │
│  ──────────────────                                                │
│  // 장치의 NUMA 노드                                                   │
│  $ cat /sys/bus/pci/devices/0000:01:00.0/numa_node                │
│  0                                                                   │
│                                                                     │
│  // IOMMU 그룹                                                       │
│  $ ls /sys/kernel/iommu_groups/                                    │
│  0  1  2  3  4  5                                                   │
│                                                                     │
│  // 장치 바인딩                                                       │
│  $ lspci -nn                                                        │
│  01:00.0 VGA [0300]: NVIDIA [10de:1b80]                            │
│                                                                     │
│  【SR-IOV】                                                           │
│  ──────────────────                                                │
│  // VF (Virtual Function) 수 확인                                    │
│  $ cat /sys/class/net/eth0/device/sriov_totalvfs                  │
│ 8                                                                   │
│                                                                     │
│  // VF 생성                                                          │
│  $ echo 4 | sudo tee /sys/class/net/eth0/device/sriov_numvfs      │
│                                                                     │
│  // VF 목록                                                          │
│  $ ls /sys/class/net/eth0/device/virtfn*                           │
│                                                                     │
│  【PCIe 문제 해결】                                                   │
│  ──────────────────                                                │
│  // 장치 리셋                                                         │
│  $ echo 1 | sudo tee /sys/bus/pci/devices/0000:01:00.0/reset      │
│                                                                     │
│  // 장치 제거                                                         │
│  $ echo 1 | sudo tee /sys/bus/pci/devices/0000:01:00.0/remove     │
│                                                                     │
│  // 재스캔                                                           │
│  $ echo 1 | sudo tee /sys/bus/pci/rescan                           │
│                                                                     │
│  // 커널 메시지                                                       │
│  $ dmesg | grep -i pci                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 고속 직렬 확장 버스
• 버전: 1.0(250MB/s) → 6.0(7.88GB/s)/레인
• 레인: x1, x2, x4, x8, x16
• 프로토콜: Transaction, Data Link, Physical
• TLP: Memory, I/O, Config, Completion
• 핫 플러그: 지원
• ASPM: 전원 관리
• SR-IOV: 가상화
• Linux: lspci, /sys/bus/pci/
• 용도: GPU, NVMe, NIC, 사운드
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [GPU](./544_gpu.md) → PCIe x16
- [NVMe](./540_nvme.md) → PCIe x4 SSD
- [DMA](./512_dma.md) → 직접 메모리 액세스

### 👶 어린이를 위한 3줄 비유 설명
**개념**: PCIe는 "초고속 데이터 고속도로" 같아요!

**원리**: 레인을 늘려 더 많은 데이터를 보내요!

**효과**: 그래픽카드가 아주 빠르게 작동해요!
