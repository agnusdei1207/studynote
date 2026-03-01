+++
title = "이더넷 (Ethernet)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 이더넷 (Ethernet)

## 핵심 인사이트 (3줄 요약)
> **가장 널리 사용되는 LAN(Local Area Network) 기술**. CSMA/CD로 매체 접근 제어. 10Mbps에서 400Gbps까지 진화했으며, 기업/데이터센터의 핵심 네트워크 기술이다.

## 1. 개념
이더넷은 **IEEE 802.3 표준으로 정의된 유선 LAN 기술**로, CSMA/CD 방식을 사용하여 공유 매체에서 데이터를 전송한다.

> 비유: "회의실 대화" - 말하고 싶을 때 조용하면 말함, 겹치면 잠시 대기

## 2. 이더넷 프레임 구조

```
┌─────────────────────────────────────────────────────────────┐
│ Preamble │ SFD │  DA  │  SA  │ Type │  Data   │ FCS │
│  7B      │ 1B  │ 6B   │ 6B   │ 2B   │ 46-1500B│ 4B  │
└─────────────────────────────────────────────────────────────┘

Preamble (7B): 동기화 비트 패턴 (10101010...)
SFD (1B): 프레임 시작 구분자 (10101011)
DA (6B): 목적지 MAC 주소
SA (6B): 출발지 MAC 주소
Type (2B): 상위 계층 프로토콜 (IPv4=0x0800)
Data (46~1500B): 페이로드
FCS (4B): CRC-32 오류 검출

최소 프레임 크기: 64바이트
최대 프레임 크기: 1518바이트 (표준)
```

## 3. CSMA/CD (Carrier Sense Multiple Access / Collision Detection)

```
동작 과정:

1. Carrier Sense (캐리어 감지)
   - 매체가 사용 중인지 확인
   - 사용 중이면 대기

2. Multiple Access (다중 접속)
   - 조용하면 전송 시작

3. Collision Detection (충돌 감지)
   - 전송 중 충돌 감지
   - 충돌 시 즉시 중단

4. Jam Signal
   - 충돌 알림 신호 전송

5. Backoff Algorithm
   - 임의 시간 대기 후 재시도
   - 최대 16회 시도

슬롯 시간: 512비트 시간 (10/100Mbps)
         10Mbps에서 51.2μs
```

### 3.1 충돌 도메인
```
공유 매체에서 충돌 가능 영역

Hub 사용 시:
┌─────┐   ┌─────┐   ┌─────┐
│ PC1 │───│ PC2 │───│ PC3 │
└─────┘   └─────┘   └─────┘
    ↑       ↑       ↑
    └───────┴───────┘
       하나의 충돌 도메인

Switch 사용 시:
┌─────┐   ┌─────┐   ┌─────┐
│ PC1 │   │ PC2 │   │ PC3 │
└──┬──┘   └──┬──┘   └──┬──┘
   └─────┬──┴──┬─────┘
       Switch
각 포트 = 개별 충돌 도메인
```

## 4. 이더넷 속도 진화

| 표준 | 속도 | 매체 | 거리 | 연도 |
|------|------|------|------|------|
| 10BASE5 | 10Mbps | 동축케이블 | 500m | 1983 |
| 10BASE-T | 10Mbps | UTP Cat3 | 100m | 1990 |
| 100BASE-TX | 100Mbps | UTP Cat5 | 100m | 1995 |
| 1000BASE-T | 1Gbps | UTP Cat5e/6 | 100m | 1999 |
| 10GBASE-T | 10Gbps | UTP Cat6a | 100m | 2006 |
| 40GBASE-T | 40Gbps | UTP Cat8 | 30m | 2016 |
| 100GBASE-T | 100Gbps | DAC/Optical | - | 2010 |
| 400GBASE-T | 400Gbps | Optical | - | 2017 |

## 5. 이더넷 케이블

### 5.1 UTP 케이블
```
카테고리별 특성:

Cat5:  100Mbps, 100MHz
Cat5e: 1Gbps, 100MHz
Cat6:  1Gbps, 250MHz
Cat6a: 10Gbps, 500MHz
Cat7:  10Gbps, 600MHz
Cat8:  25/40Gbps, 2000MHz

케이블 종류:
- Straight-through: PC-Switch 연결
- Crossover: PC-PC, Switch-Switch 연결
```

### 5.2 광케이블
```
1000BASE-SX: 단파장, 멀티모드, 550m
1000BASE-LX: 장파장, 싱글모드, 5km
10GBASE-SR: 단파장, 멀티모드, 400m
10GBASE-LR: 장파장, 싱글모드, 10km
```

## 6. 스위칭

### 6.1 스위치 동작
```
1. Learning (학습)
   - 수신 프레임의 SA로 MAC 주소 테이블 갱신

2. Flooding (플러딩)
   - unknown 유니캐스트, 브로드캐스트
   - 모든 포트로 전송

3. Forwarding (포워딩)
   - MAC 테이블 참조하여 특정 포트로 전송

4. Filtering (필터링)
   - 동일 포트면 전송 안 함
```

### 6.2 MAC 주소 테이블
```
┌─────────────┬────────┬───────────┐
│   MAC 주소   │  포트  │   VLAN    │
├─────────────┼────────┼───────────┤
│ AA:BB:CC:DD │   1    │    10     │
│ EE:FF:00:11 │   2    │    10     │
│ 22:33:44:55 │   3    │    20     │
└─────────────┴────────┴───────────┘

에이징 타임: 300초 (기본)
```

## 7. VLAN (Virtual LAN)

```
물리적 구분 없이 논리적으로 네트워크 분리

VLAN 10 (영업부)     VLAN 20 (개발부)
┌─────┐  ┌─────┐    ┌─────┐  ┌─────┐
│ PC1 │  │ PC2 │    │ PC3 │  │ PC4 │
└──┬──┘  └──┬──┘    └──┬──┘  └──┬──┘
   └────┬──┴─────────┬──┴────┘
      Switch (Tagged Port)

Trunk Port:
- 여러 VLAN 프레임 전송
- 802.1Q 태그 추가
```

## 8. 자동 협상 (Auto-Negotiation)

```
속도와 듀플렉스 자동 설정

협상 우선순위:
1. 1000BASE-T Full Duplex
2. 1000BASE-T Half Duplex
3. 100BASE-TX Full Duplex
4. 100BASE-TX Half Duplex
5. 10BASE-T Full Duplex
6. 10BASE-T Half Duplex

문제:
- 한쪽만 Auto인 경우
- Speed/Duplex 불일치 → 성능 저하
```

## 9. 코드 예시

```python
import random
from collections import defaultdict

class EthernetFrame:
    """이더넷 프레임 시뮬레이션"""

    def __init__(self, src_mac, dst_mac, data, ethertype=0x0800):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.data = data
        self.ethertype = ethertype

    def to_bytes(self):
        """프레임 직렬화"""
        # Preamble + SFD (8 bytes)
        preamble = bytes([0xAA] * 7 + [0xAB])

        # MAC 주소 변환
        dst = self._mac_to_bytes(self.dst_mac)
        src = self._mac_to_bytes(self.src_mac)

        # EtherType
        etype = self.ethertype.to_bytes(2, 'big')

        # Data (최소 46바이트)
        data = self.data.encode() if isinstance(self.data, str) else self.data
        if len(data) < 46:
            data += bytes(46 - len(data))

        # FCS (CRC-32)
        frame = dst + src + etype + data
        fcs = self._calculate_crc32(frame)

        return preamble + frame + fcs

    def _mac_to_bytes(self, mac):
        """MAC 문자열 → 바이트"""
        return bytes(int(b, 16) for b in mac.split(':'))

    def _calculate_crc32(self, data):
        """CRC-32 계산 (간소화)"""
        crc = 0xFFFFFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xEDB88320
                else:
                    crc >>= 1
        return (crc ^ 0xFFFFFFFF).to_bytes(4, 'little')


class Switch:
    """이더넷 스위치 시뮬레이션"""

    def __init__(self, name, num_ports=8):
        self.name = name
        self.num_ports = num_ports
        self.mac_table = {}  # MAC -> Port
        self.port_devices = defaultdict(list)  # Port -> [Devices]

    def learn(self, mac, port):
        """MAC 주소 학습"""
        if mac not in self.mac_table:
            print(f"[{self.name}] 학습: MAC {mac} → Port {port}")
        self.mac_table[mac] = port

    def forward(self, frame, src_port):
        """프레임 포워딩"""
        dst_mac = frame.dst_mac

        # 출발지 MAC 학습
        self.learn(frame.src_mac, src_port)

        # 브로드캐스트/멀티캐스트
        if dst_mac.startswith('FF:FF:FF') or dst_mac.startswith('01:00:5E'):
            print(f"[{self.name}] 플러딩: {dst_mac}")
            return 'flood'

        # 유니캐스트
        if dst_mac in self.mac_table:
            dst_port = self.mac_table[dst_mac]
            if dst_port == src_port:
                print(f"[{self.name}] 필터링: 동일 포트")
                return None
            print(f"[{self.name}] 포워딩: {dst_mac} → Port {dst_port}")
            return dst_port
        else:
            print(f"[{self.name}] 플러딩: unknown MAC {dst_mac}")
            return 'flood'


class CSMACD:
    """CSMA/CD 시뮬레이션"""

    def __init__(self):
        self.bus_busy = False
        self.collision_count = defaultdict(int)

    def transmit(self, device_id, max_attempts=16):
        """전송 시도"""
        for attempt in range(max_attempts):
            # 캐리어 감지
            if self.bus_busy:
                print(f"[{device_id}] 매체 사용 중, 대기...")
                continue

            # 전송 시작
            self.bus_busy = True

            # 충돌 시뮬레이션 (10% 확률)
            if random.random() < 0.1:
                print(f"[{device_id}] 충돌 감지!")
                self.collision_count[device_id] += 1

                # Jam 신호
                self.bus_busy = False

                # Backoff
                n = min(self.collision_count[device_id], 10)
                wait_time = random.randint(0, 2**n - 1)
                print(f"[{device_id}] Backoff: {wait_time} 슬롯 대기")
                continue

            # 성공
            print(f"[{device_id}] 전송 성공!")
            self.bus_busy = False
            return True

        print(f"[{device_id}] 최대 재시도 초과!")
        return False


# 시뮬레이션
print("=== 이더넷 프레임 생성 ===")
frame = EthernetFrame(
    src_mac="AA:BB:CC:DD:EE:FF",
    dst_mac="11:22:33:44:55:66",
    data="Hello Ethernet"
)
print(f"프레임 크기: {len(frame.to_bytes())} bytes")

print("\n=== 스위치 동작 ===")
switch = Switch("SW1")
frame1 = EthernetFrame("AA:BB:CC:DD:EE:FF", "11:22:33:44:55:66", "Data1")
frame2 = EthernetFrame("11:22:33:44:55:66", "AA:BB:CC:DD:EE:FF", "Data2")

switch.forward(frame1, 1)
switch.forward(frame2, 2)
switch.forward(frame1, 1)

print("\n=== CSMA/CD ===")
csma = CSMACD()
csma.transmit("PC1")
