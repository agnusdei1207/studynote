+++
title = "네트워크 장비 (Hub, Switch, Router, Gateway)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 네트워크 장비 (Hub, Switch, Router, Gateway)

## 핵심 인사이트 (3줄 요약)
> **허브**: 1계층, 단순 중계. **스위치**: 2계층, MAC 기반 포워딩. **라우터**: 3계층, IP 기반 라우팅. **게이트웨이**: 서로 다른 네트워크 연결. 계층별로 기능과 지능도가 다르다.

## 1. 네트워크 장비 개요

```
OSI 계층별 장비:

1계층 (물리): 리피터, 허브
2계층 (링크): 브리지, L2 스위치
3계층 (네트워크): 라우터, L3 스위치
4계층 (전송): L4 스위치, 로드밸런서
7계층 (응용): L7 스위치, 게이트웨이
```

## 2. 리피터 (Repeater)

### 2.1 개념
```
기능: 신호 증폭 및 재생
계층: 1계층 (물리)

    신호 약화        증폭
───→ ═════ ═───→ [Repeater] ───→ ═════ ═───→

특징:
- 전기적 신호만 증폭
- 지연 시간 증가
- 노이즈도 증폭
```

### 2.2 장단점
| 장점 | 단점 |
|-----|------|
| 거리 연장 | 노이즈 증폭 |
| 단순 구조 | 충돌 도메인 확대 |
| 저렴 | 지연 증가 |

## 3. 허브 (Hub)

### 3.1 개념
```
기능: 다중 포트 리피터
계층: 1계층 (물리)

        ┌─── PC1
        │
───→ ───┼─── PC2
        │
        └─── PC3

동작:
- 수신 신호를 모든 포트로 전송
- 충돌 감지 시 Jam 신호
```

### 3.2 종류
```
더미 허브 (Dummy Hub):
- 단순 중계만
- 충돌 도메인 공유

스마트 허브:
- 관리 기능
- SNMP 지원
```

### 3.3 허브 문제점
```
1. 충돌 도메인 공유
   - 모든 포트가 하나의 세그먼트

2. 대역폭 공유
   - 전체 대역폭을 나누어 사용

3. 보안 취약
   - 모든 포트로 전송 (스니핑 가능)

4. 확장성 제한
   - 포트 수 증가 시 충돌 증가
```

## 4. 브리지 (Bridge)

### 4.1 개념
```
기능: 세그먼트 연결, MAC 기반 필터링
계층: 2계층 (데이터링크)

세그먼트1          세그먼트2
┌─────┬─────┐    ┌─────┬─────┐
│PC1 │ │PC2 │    │PC3 │ │PC4 │
└──┬──┴──┬──┘    └──┬──┴──┬──┘
   └────┼──────────┼────┘
      [Bridge]

동작:
- MAC 주소 학습
- 세그먼트 간 필터링
- 충돌 도메인 분리
```

### 4.2 브리지 종류
```
투명 브리지 (Transparent):
- 학습 기반
- 스패닝 트리 프로토콜

소스 라우팅 브리지:
- 출발지에서 경로 지정
- 토큰링에서 사용
```

## 5. 스위치 (Switch)

### 5.1 L2 스위치
```
기능: MAC 기반 포워딩
계층: 2계층

동작 과정:
1. Learning: SA 학습
2. Flooding: Unknown 유니캐스트/브로드캐스트
3. Forwarding: DA 기반 포워딩
4. Filtering: 동일 포트 차단

장점:
- 충돌 도메인 분리
- 전이중 통신
- 포트별 대역폭 보장
```

### 5.2 L3 스위치
```
기능: IP 라우팅 + L2 스위칭
계층: 2/3계층

특징:
- 하드웨어 기반 라우팅
- 빠른 처리 속도
- VLAN 간 라우팅

용도:
- 데이터센터
- 기업 코어 스위치
```

### 5.3 L4/L7 스위치
```
L4 스위치:
- 포트 기반 로드밸런싱
- TCP/UDP 세션 관리

L7 스위치:
- 애플리케이션 계층 처리
- URL, HTTP 헤더 기반 분산
- SSL 종료
```

### 5.4 스위치 기능
```
1. VLAN
   - 논리적 네트워크 분리

2. STP (Spanning Tree)
   - 루프 방지

3. 포트 미러링
   - 트래픽 복사 (모니터링)

4. PoE (Power over Ethernet)
   - 전력+데이터 전송

5. 링크 어그리게이션
   - 대역폭 확장
```

## 6. 라우터 (Router)

### 6.1 개념
```
기능: IP 기반 라우팅, 네트워크 연결
계층: 3계층 (네트워크)

네트워크1           네트워크2
192.168.1.0/24     10.0.0.0/8
    │                  │
    └────[Router]──────┘

동작:
1. 라우팅 테이블 조회
2. 최적 경로 결정
3. 패킷 포워딩
4. TTL 감소
```

### 6.2 라우터 기능
```
1. 경로 결정
   - 정적 라우팅
   - 동적 라우팅 (OSPF, BGP)

2. 패킷 분할/재조립
   - MTU 초과 시 단편화

3. QoS
   - 트래픽 우선순위

4. NAT
   - 주소 변환

5. ACL
   - 접근 제어

6. VPN
   - 터널링
```

## 7. 게이트웨이 (Gateway)

### 7.1 개념
```
기능: 서로 다른 네트워크/프로토콜 연결
계층: 3~7계층

이더넷 ───→ [Gateway] ───→ 토큰링
TCP/IP ───→ [Gateway] ───→ SNA

특징:
- 프로토콜 변환
- 주소 변환
- 데이터 형식 변환
```

### 7.2 게이트웨이 종류
```
1. 네트워크 게이트웨이
   - 기본 게이트웨이 (라우터)

2. 애플리케이션 게이트웨이
   - 프록시 서버
   - API 게이트웨이

3. 보안 게이트웨이
   - 방화벽
   - 웹 방화벽 (WAF)

4. 미디어 게이트웨이
   - VoIP 게이트웨이
```

## 8. 장비 비교표

| 항목 | 허브 | 스위치 | 라우터 | 게이트웨이 |
|------|------|--------|--------|------------|
| 계층 | 1 | 2~4 | 3 | 3~7 |
| 주소 | 없음 | MAC | IP | 다양 |
| 도메인 | 충돌 공유 | 충돌 분리 | 브로드캐스트 분리 | - |
| 속도 | 낮음 | 높음 | 중간 | 다양 |
| 지능도 | 없음 | 중간 | 높음 | 최고 |
| 용도 | 거의 안 씀 | LAN | WAN | 네트워크 연결 |

## 9. 코드 예시

```python
from collections import defaultdict
import time

class Device:
    """네트워크 장비 기본 클래스"""
    def __init__(self, name):
        self.name = name
        self.ports = {}

    def connect(self, port, device):
        self.ports[port] = device


class Hub(Device):
    """허브 시뮬레이션"""

    def __init__(self, name, num_ports=4):
        super().__init__(name)
        self.num_ports = num_ports
        self.collision = False

    def send(self, data, src_port):
        """모든 포트로 브로드캐스트"""
        print(f"[{self.name}] 수신 (Port {src_port}): {data}")
        print(f"[{self.name}] 모든 포트로 전송")

        for port, device in self.ports.items():
            if port != src_port:
                print(f"  → Port {port}")
                device.receive(data)


class Switch(Device):
    """L2 스위치 시뮬레이션"""

    def __init__(self, name, num_ports=8):
        super().__init__(name)
        self.num_ports = num_ports
        self.mac_table = {}  # MAC -> Port

    def learn(self, mac, port):
        """MAC 주소 학습"""
        if mac not in self.mac_table:
            print(f"[{self.name}] 학습: {mac} → Port {port}")
        self.mac_table[mac] = port

    def send(self, data, src_mac, dst_mac, src_port):
        """프레임 처리"""
        print(f"[{self.name}] 수신: {src_mac} → {dst_mac}")

        # 학습
        self.learn(src_mac, src_port)

        # 브로드캐스트
        if dst_mac == "FF:FF:FF:FF:FF:FF":
            print(f"[{self.name}] 브로드캐스트")
            self._flood(data, src_port)
            return

        # 유니캐스트
        if dst_mac in self.mac_table:
            dst_port = self.mac_table[dst_mac]
            print(f"[{self.name}] 포워딩 → Port {dst_port}")
            self.ports[dst_port].receive(data)
        else:
            print(f"[{self.name}] Unknown MAC, 플러딩")
            self._flood(data, src_port)

    def _flood(self, data, src_port):
        for port, device in self.ports.items():
            if port != src_port:
                device.receive(data)


class Router(Device):
    """라우터 시뮬레이션"""

    def __init__(self, name):
        super().__init__(name)
        self.routing_table = {}  # Network -> (Interface, NextHop)

    def add_route(self, network, interface, next_hop=None):
        """라우팅 테이블 추가"""
        self.routing_table[network] = (interface, next_hop)
        print(f"[{self.name}] 라우트 추가: {network}")

    def route(self, packet):
        """패킷 라우팅"""
        dst_ip = packet['dst_ip']
        print(f"[{self.name}] 라우팅: {dst_ip}")

        # 최장 프리픽스 매칭 (간소화)
        for network, (interface, next_hop) in self.routing_table.items():
            if dst_ip.startswith(network.split('.')[0:3]):
                print(f"[{self.name}] 경로: {network} → Interface {interface}")
                return interface, next_hop

        # 기본 경로
        if '0.0.0.0' in self.routing_table:
            return self.routing_table['0.0.0.0']

        print(f"[{self.name}] 경로 없음")
        return None, None


class Gateway:
    """게이트웨이 시뮬레이션"""

    def __init__(self, name):
        self.name = name
        self.protocols = {}

    def register_protocol(self, protocol_name, handler):
        """프로토콜 핸들러 등록"""
        self.protocols[protocol_name] = handler
        print(f"[{self.name}] 프로토콜 등록: {protocol_name}")

    def translate(self, data, src_protocol, dst_protocol):
        """프로토콜 변환"""
        print(f"[{self.name}] 변환: {src_protocol} → {dst_protocol}")

        if src_protocol in self.protocols and dst_protocol in self.protocols:
            # 변환 로직 (간소화)
            translated = f"[{dst_protocol}]{data}"
            return translated

        print(f"[{self.name}] 변환 실패")
        return None


# 시뮬레이션
print("=== 허브 시뮬레이션 ===")
hub = Hub("Hub1", 4)
hub.connect(1, type('Device', (), {'receive': lambda d: print(f"  PC1 수신: {d}")})())
hub.connect(2, type('Device', (), {'receive': lambda d: print(f"  PC2 수신: {d}")})())
hub.connect(3, type('Device', (), {'receive': lambda d: print(f"  PC3 수신: {d}")})())
hub.send("Hello", 1)

print("\n=== 스위치 시뮬레이션 ===")
switch = Switch("SW1")
switch.connect(1, type('Device', (), {'receive': lambda d: print(f"  Port1 수신: {d}")})())
switch.connect(2, type('Device', (), {'receive': lambda d: print(f"  Port2 수신: {d}")})())
switch.send("Data1", "AA:BB:CC:DD:EE:FF", "11:22:33:44:55:66", 1)
switch.send("Data2", "11:22:33:44:55:66", "AA:BB:CC:DD:EE:FF", 2)

print("\n=== 라우터 시뮬레이션 ===")
router = Router("R1")
router.add_route("192.168.1.0/24", "eth0")
router.add_route("10.0.0.0/8", "eth1")
router.add_route("0.0.0.0/0", "eth0", "192.168.1.1")
router.route({'dst_ip': '10.0.5.10'})
router.route({'dst_ip': '172.16.0.1'})
