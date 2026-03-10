+++
title = "380. 가비지 컬렉션 (Garbage Collection) 기초 - 참조 카운팅, Mark-and-Sweep"
weight = 380
+++

# 607. Garbage Collection (GC)

weight = 380
+++

# 607. Garbage Collection (GC)
weight = 380
+++

# 607. Garbage Collection (GC)
weight = 380
+++

# 607. Garbage Collection (GC)
weight = 380
+++

# 607. Garbage Collection (GC)
weight = 380
+++

# 607. Garbage Collection (GC)
weight = 380
+++

# 607. Garbage Collection (GC)
Garbage Collection)**는 **SSD에서 삭제된 데이터를 정리하여 공간을 확보하는 프로세스**입니다.
### 💡 비유: 쓰레기 수거
가비지 컬렉션은 **쓰레기 수거**와 같습니다. 삭제된 데이터를 치웁니다.
### 가비지 컬렉션 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                가비지 컬렉션 구조                                      │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【GC 동작 원리】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. 삭제된 블록 식별 (TRIM)                                       │ │   │
│  │     └─▶ OS에서 TRIM 명령으로 삭제된 블록 표시                        │ │   │
│  │                                                             │ │   │
│  │  2. 유효 데이터 복사                                                  │ │   │
│  │     └─▶ 삭제된 블록과 같은 페이지의 유효 데이터를 새 블록으로 복사         │ │   │
│  │                                                             │ │   │
│  │  3. 블록 소거 (Erase)                                               │ │   │
│  │     └─▶ 전체 페이지(또는 블록)를 소거 상태로 변경                       │ │   │
│  │                                                             │ │   │
│  │  4. 새 데이터 쓰기                                                    │ │   │
│  │     └─▶ 소거된 블록에 새 데이터 쓰기 가능                              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【GC 종류】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  종류              설명                    시기                     │ │   │
│  │  ────              ────                    ────                     │ │   │
│  │  수동 GC          사용자 요청 시         필요 시                   │ │   │
│  │  자동 GC          백그라운드             아이들/유휴 시               │ │   │
│  │  강제 GC          공간 부족 시           즉시                       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【GC 비용】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • 읽기: 유효 데이터를 읽어야 함                                        │ │   │
│  │  • 쓰기: 유효 데이터를 새 위치에 쓰기                                    │ │   │
│  │  • 소거: 블록 전체를 소거 상태로 변경                                    │ │   │
│  │  • 매핑: 논리-물리 매핑 테이블 업데이트                                  │ │   │
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
│                가비지 컬렉션 상세                                      │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【GC 트리거】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  조건              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  여유 공간 부족      사용 가능한 블록이 임계값 미달                   │ │   │
│  │  TRIM 명령          OS에서 삭제된 블록 표시                          │ │   │
│  │  아이들 상태          I/O 작업 없음                                  │ │   │
│  │  정기적 실행          스케줄러에 의한 주기적 실행                       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【GC 알고리즘】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  알고리즘            설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  단순 GC           삭제된 블록만 정리                              │ │   │
│  │  Wear Leveling    쓰기 분산을 고려한 GC                           │ │   │
│  │  Hot/Cold 분리      자주 사용하는 블록 우선 정리                      │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【GC와 쓰기 증폭】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  NAND 플래시 특성:                                                  │ │   │
│  │  • 쓰기 전 소거 (Erase Before Write)                              │ │   │
│  │  • 페이지 단위 소거 (128KB~4MB)                                      │ │   │
│  │  • 쓰기/소거 불균형 (P/E 비율)                                        │ │   │
│  │                                                             │ │   │
│  │  쓰기 증폭 (Write Amplification):                                   │ │   │
│  │  WA = 실제 쓰기 양 / 호스트 쓰기 요청                                 │ │   │
│  │  • GC로 인한 추가 쓰기 발생                                          │ │   │
│  │  • 유효 데이터 복사가 증폭 유발                                        │ │   │
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
│                실무 적용                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【GC 상태 확인】                                                    │ |
│  ──────────────────                                                │
│  // smartctl로 GC 정보 확인                                            │
│  $ sudo smartctl -a /dev/nvme0n1                                     │
│  Available Spare: 100%                                            │
│  Percentage Used: 5%                                             │
│  Data Units Written: 1234567                                      │
│                                                                     │
│  // NVMe SMART 속성 (GC 관련)                                        │
│  $ sudo smartctl -a /dev/nvme0n1 | grep -i "Media"                 │
│  Media and Data Integrity Errors: 0                                 │
│                                                                     │
│  // 쓰기 증폭 확인                                                    │
│  $ sudo smartctl -a /dev/nvme0n1 | grep -i "Written"                │
│  Data Units Written: 1234567 [632 GB]                              │
│  Host Write Commands: 987654 [505 GB]                             │
│  // WA = 632 / 505 ≈ 1.25                                              │
│                                                                     │
│  【GC 최적화】                                                        │
│  ──────────────────                                                │
│  // Over-Provisioning (OP)                                           │
│  // 여유 공간 증가로 GC 부하 감소                                        │
│  $ sudo nvme format /dev/nvme0n1 --ses=1 --pil=0                       │
│                                                                     │
│  // TRIM 정기적 실행                                                    │
│  $ sudo systemctl enable fstrim.timer                              │
│  $ sudo fstrim -v /                                                 │
│                                                                     │
│  // 마운트 옵션                                                        │
│  $ sudo mount -o discard /dev/nvme0n1p1 /mnt                       │
│                                                                     │
│  // I/O 스케줄러                                                        │
│  $ echo none | sudo tee /sys/block/nvme0n1/queue/scheduler          │
│                                                                     │
│  【GC 부하 모니터링】                                                  │
│  ──────────────────                                                │
│  // 실시간 I/O 모니터링                                                │
│  $ sudo iostat -x 1                                                 │
│  $ sudo iotop                                                        │
│                                                                     │
│  // 쓰기 증폭 계산                                                    │
│  $ sudo smartctl -a /dev/nvme0n1 | grep "Data Units Written"         │
│  $ sudo smartctl -a /dev/nvme0n1 | grep "Host Write Commands"         │
│  // WA = Data Units / Host Commands                                  │
│                                                                     │
│  // GC 활동 로그                                                      │
│  $ dmesg | grep -i "garbage"                                        │
│  $ dmesg | grep -i "gc"                                             │
│                                                                     │
│  【GC 관련 문제 해결】                                                │
│  ──────────────────                                                │
│  // GC로 인한 성능 저하                                                │
│  $ sudo fstrim -v /                                                 │
│  $ sudo mount -o discard /dev/nvme0n1p1 /mnt                       │
│                                                                     │
│  // 공간 부족 (GC 지연)                                                │
│  $ sudo fstrim -av                                                  │
│  $ sudo nvme format /dev/nvme0n1 --ses=1                             │
│                                                                     │
│  // 쓰기 증폭 과다                                                    │
│  // Over-Provisioning 증가                                            │
│  // TRIM 빈도 증가                                                    │
│  // 더 나은 SSD 사용 (MLC → SLC)                                     │
│                                                                     │
│  【GC 성능 영향】                                                        │
│  ──────────────────                                                │
│  // GC 전/후 성능 비교                                                │
│  $ sudo fio --name=/dev/nvme0n1 --rw=randwrite --bs=4k \               │
│    --iodepth=32 --numjobs=4 --size=1G --direct=1                  │
│                                                                     │
│  // GC 없이 (TRIM 비활성화)                                            │
│  $ sudo mount -o nodiscard /dev/nvme0n1p1 /mnt                       │
│  // ... 테스트 ...                                                      │
│                                                                     │
│  // GC 있이 (TRIM 활성화)                                            │
│  $ sudo mount -o discard /dev/nvme0n1p1 /mnt                         │
│  // ... 테스트 ...                                                      │
│                                                                     │
│  【Python으로 GC 모니터링】                                          │
│  ──────────────────                                                │
│  import subprocess                                                   │
│                                                                     │
│  # SMART 데이터 가져오기                                              │
│  result = subprocess.run(['smartctl', '-a', '/dev/nvme0n1'],          │
│                          capture_output=True, text=True)             │
│                                                                     │
│  # 쓰기 증폭 계산                                                    │
│  for line in result.stdout.split('\n'):                                │
│      if 'Data Units Written' in line:                                │
│          data_units = int(line.split(':')[1].strip())               │
│      if 'Host Write Commands' in line:                                │
│          host_writes = int(line.split(':')[1].strip())              │
│                                                                     │
│  if data_units and host_writes:                                     │
│      wa = data_units / host_writes                                   │
│      print(f"Write Amplification: {wa:.2f}x")                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: SSD에서 삭제된 데이터를 정리하는 프로세스
• 목적: 공간 확보, 쓰기 성능 유지
• 원리: 유효 데이터 복사 → 블록 소거 → 재사용
• 종류: 수동 GC, 자동 GC, 강제 GC
• 비용: 읽기, 쓰기, 소거, 매핑 업데이트
• 트리거: 공간 부족, TRIM 명령, 아이들 상태
• 쓰기 증폭: WA = 실제 쓰기 / 호스트 쓰기
• 최적화: Over-Provisioning, TRIM, I/O 스케줄러
• 확인: smartctl -a, iostat -x
• 모니터링: 쓰기 증폭, GC 활동 로그
• 문제 해결: fstrim, discard 옵션, NVMe format
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [TRIM](./606_trim.md) → GC와 연동
- [SSD](./605_ssd.md) → GC가 수행되는 장치
- [Wear Leveling](./608_wear_leveling.md) → GC와 함께 수명 관리
- [Write Amplification](./617_write_amplification.md) → GC로 인한 쓰기 증가
- [Over-Provisioning](./618_over_provisioning.md) → GC 최적화
- [NVMe](./603_nvme.md) → NVMe GC 특징
- [SMART](./614_smart.md) → GC 상태 모니터링
- [fstrim](./616_fstrim.md) → TRIM 명령어

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 가비지 컬렉션은 "쓰레기 수거" 같아요!

**원리**: 삭제된 데이터를 치워 깨끗하게 만들어요!

**효과**: SSD가 빠르고 건강하게 유지돼요!
