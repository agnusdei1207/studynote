+++
title = "771. 플래시 메모리 마모 평준화 (Wear Leveling)"
weight = 771
+++

# 608. Wear Leveling (마모 평준화)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: SSD 셀의 쓰기 횟수를 균등하게 분산하는 기술
> 2. **가치**: SSD 수명 연장, 특정 셀 과다 사용 방지
> 3. **융합**: SSD, Garbage Collection, TRIM과 연관

---

## Ⅰ. 개요

### 개념 정의
**Wear Leveling(마모 평준화)**은 **SSD 셀의 쓰기/소거 횟수를 고르게 분산하여 SSD 수명을 연장하는 기술**입니다.
### 💡 비유: 고르게 나누기
Wear Leveling은 **고르게 나누기**와 같습니다. 일부만 닳지 않게 분배합니다.
### Wear Leveling 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                Wear Leveling 구조                                     │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Wear Leveling 필요성】                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  NAND 플래시 특성:                                                  │ │   │
│  │  • 셀당 쓰기/소거 횟수 제한 (P/E Cycle)                              │ │   │
│  │  • SLC: ~100,000회                                                  │ │   │
│  │  • MLC: ~10,000회                                                   │ │   │
│  │  • TLC: ~3,000회                                                    │ │   │
│  │  • QLC: ~1,000회                                                    │ │   │
│  │                                                             │ │   │
│  │  문제:                                                             │ │   │
│  │  • 일부 블록에 쓰기 집중 → 조기 고장                                    │ │   │
│  │  • 핫 데이터 vs 콜드 데이터                                           │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Wear Leveling 종류】                                               │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  종류              설명                    장점        단점          │ │   │
│  │  ────              ────                    ────        ────          │ │   │
│  │  동적 Wear Leveling  사용 중인 블록만      속도 빠름    일부 집중       │ │   │
│  │  정적 Wear Leveling  모든 블록             균등 분산    오버헤드         │ │   │
│  │  하이브리드           동적+정적 결합        균형         복잡           │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Wear Leveling 동작】                                               │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. 쓰기 요청 수신                                                    │ │   │
│  │  2. 쓰기 횟수가 적은 블록 선택                                          │ │   │
│  │  3. 기존 데이터 이동 (필요 시)                                          │ │   │
│  │  4. 새 블록에 데이터 쓰기                                              │ │   │
│  │  5. 논리-물리 매핑 업데이트                                            │ │   │
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
│                Wear Leveling 상세                                     │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【동적 Wear Leveling】                                              │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특징:                                                             │ │   │
│  │  • 활성 블록만 대상                                                  │ │   │
│  │  • 쓰기 횟수 추적                                                    │ │   │
│  │  • 적은 오버헤드                                                    │ │   │
│  │                                                             │ │   │
│  │  단점:                                                             │ │   │
│  │  • 콜드 데이터 블록은 제외                                            │ │   │
│  │  • 일부 블록에 쓰기 집중 가능                                          │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【정적 Wear Leveling】                                              │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특징:                                                             │ │   │
│  │  • 모든 블록 대상 (사용 중 + 사용 안 함)                                 │ │   │
│  │  • 콜드 데이터도 이동                                                  │ │   │
│  │  • 완전한 균등 분산                                                  │ │   │
│  │                                                             │ │   │
│  │  단점:                                                             │ │   │
│  │  • 콜드 데이터 이동 오버헤드                                          │ │   │
│  │  • 추가 쓰기 발생 (쓰기 증폭)                                         │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Wear Leveling와 Garbage Collection】                               │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  관계:                                                             │ │   │
│  │  • GC는 삭제된 블록 정리                                              │ │   │
│  │  • Wear Leveling은 쓰기 분산                                         │ │   │
│  │  • 함께 작동하여 SSD 수명 관리                                         │ │   │
│  │                                                             │ │   │
│  │  충돌:                                                             │ │   │
│  │  • GC는 최적 블록 선택 (성능)                                          │ │   │
│  │  • Wear Leveling은 균등 분산 (수명)                                   │ │   │
│  │  • 균형 필요                                                        │ │   │
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
│  【Wear Leveling 상태 확인】                                          │
│  ──────────────────                                                │
│  // SMART 속성 확인                                                    │
│  $ sudo smartctl -a /dev/nvme0n1                                     │
│  Available Spare: 100%                                            │
│  Percentage Used: 5%                                             │
│                                                                     │
│  // 쓰기 횟수 확인                                                      │
│  $ sudo smartctl -a /dev/nvme0n1 | grep -i "Written"                │
│  Data Units Written: 1234567 [632 GB]                              │
│  Host Write Commands: 987654 [505 GB]                             │
│                                                                     │
│  // 쓰기 증폭 확인                                                      │
│  $ sudo smartctl -a /dev/nvme0n1 | grep -i "Percentage"             │
│  Percentage used endurance indicator: 5%                           │
│                                                                     │
│  【Wear Leveling 최적화】                                              │
│  ──────────────────                                                │
│  // TRIM 정기적 실행                                                    │
│  $ sudo systemctl enable fstrim.timer                              │
│  $ sudo fstrim -v /                                                 │
│                                                                     │
│  // Over-Provisioning (OP)                                           │
│  // 파티션 생성 시 일부 공간 미할당                                          │
│  $ sudo parted /dev/nvme0n1 mkpart primary 0% 90%                  │
│  // 10%를 OP로 남김                                                   │
│                                                                     │
│  // 마운트 옵션                                                        │
│  $ sudo mount -o discard /dev/nvme0n1p1 /mnt                       │
│                                                                     │
│  // I/O 스케줄러                                                        │
│  $ echo none | sudo tee /sys/block/nvme0n1/queue/scheduler          │
│                                                                     │
│  【수명 예측】                                                        │
│  ──────────────────                                                │
│  // TBW (Terabytes Written) 확인                                      │
│  $ sudo smartctl -a /dev/nvme0n1 | grep -i "Units Written"          │
│  Data Units Written: 1234567 [632 GB]                              │
│  // TBW = 632 GB                                                    │
│                                                                     │
│  // DWPD (Drive Writes Per Day) 계산                                  │
│  // DWPD = TBW / (용량 × 사용일수)                                      │
│  // 예: 1TB SSD, 5년, 600 TBW                                        │
│  // DWPD = 600 / (1 × 365 × 5) ≈ 0.33                                │
│                                                                     │
│  // 수명 계산                                                          │
│  $ sudo smartctl -a /dev/nvme0n1 | grep -i "Percentage"             │
│  Percentage used endurance indicator: 5%                           │
│  // 남은 수명 = 95%                                                   │
│                                                                     │
│  【문제 해결】                                                        │
│  ──────────────────                                                │
│  // Wear Leveling 실패                                                │
│  $ dmesg | grep -i "wear"                                          │
│  $ sudo smartctl -l error /dev/nvme0n1                              │
│                                                                     │
│  // 성능 저하 (Wear Leveling 부하)                                     │
│  $ sudo fstrim -v /                                                 │
│  $ sudo mount -o discard /dev/nvme0n1p1 /mnt                       │
│                                                                     │
│  // 수명 경고                                                          │
│  $ sudo smartctl -H /dev/nvme0n1                                    │
│  SMART overall-health self-assessment test result: PASSED           │
│                                                                     │
│  【Python으로 수명 모니터링】                                          │
│  ──────────────────                                                │
│  import subprocess                                                   │
│                                                                     │
│  # SMART 데이터 가져오기                                              │
│  result = subprocess.run(['smartctl', '-a', '/dev/nvme0n1'],          │
│                          capture_output=True, text=True)             │
│                                                                     │
│  # 수명 확인                                                          │
│  for line in result.stdout.split('\n'):                                │
│      if 'Percentage Used' in line:                                  │
│          percentage = float(line.split(':')[1].strip().replace('%', '')) │
│          print(f"SSD 사용량: {percentage}%")                          │
│          print(f"남은 수명: {100 - percentage}%")                       │
│                                                                     │
│  # TBW 확인                                                          │
│  for line in result.stdout.split('\n'):                                │
│      if 'Data Units Written' in line:                                │
│          # 1 Unit = 512 bytes (NVMe) 또는 1000 bytes (일부)            │
│          units = int(line.split(':')[1].split()[0])                 │
│          tbw = units * 512 / (1024**3)  # GB                         │
│          print(f"총 기록량: {tbw:.2f} GB")                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: SSD 셀의 쓰기 횟수를 균등하게 분산
• 목적: SSD 수명 연장, 특정 셀 과다 사용 방지
• 원리: 쓰기 횟수가 적은 블록 선택
• 종류: 동적 Wear Leveling, 정적 Wear Leveling
• NAND 플래시 수명: SLC (10만), MLC (1만), TLC (3천), QLC (1천)
• 관련 기술: GC, TRIM, Over-Provisioning
• 최적화: TRIM, OP, discard 옵션
• 확인: smartctl -a, Percentage Used
• 수명 지표: TBW, DWPD
• 문제 해결: fstrim, SMART 테스트
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [SSD](./605_ssd.md) → Wear Leveling이 적용되는 장치
- [Garbage Collection](./607_garbage_collection.md) → 함께 수명 관리
- [TRIM](./606_trim.md) → 삭제된 블록 표시
- [Over-Provisioning](./618_over_provisioning.md) → 여유 공간 확보
- [Write Amplification](./617_write_amplification.md) → Wear Leveling으로 인한 추가 쓰기
- [SMART](./614_smart.md) → 수명 모니터링
- [NAND 플래시](./619_nand_flash.md) → 셀 수명 제한

### 👶 어린이를 위한 3줄 비유 설명
**개념**: Wear Leveling은 "고르게 나누기" 같아요!

**원리**: 한쪽만 많이 쓰지 않고 골고루 써요!

**효과**: SSD가 오래오래 사용할 수 있어요!
