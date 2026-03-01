+++
title = "방화벽 & IDS/IPS"
date = 2025-03-01

[extra]
categories = "security-network"
+++

# 방화벽 & IDS/IPS

## 핵심 인사이트 (3줄 요약)
> **네트워크 트래픽을 제어하고 침입을 탐지/차단**하는 보안 시스템. 방화벽은 접근 통제, IDS는 탐지, IPS는 차단. L3~L7까지 다양한 계층 보안.

## 1. 개념
- **방화벽(Firewall)**: 네트워크 트래픽을 정책에 따라 허용/차단하는 보안 시스템
- **IDS(Intrusion Detection System)**: 침입을 탐지하고 알리는 시스템
- **IPS(Intrusion Prevention System)**: 침입을 탐지하고 차단하는 시스템

> 비유: 방화벽은 "경비원", IDS는 "CCTV", IPS는 "보안 요원"

## 2. 방화벽 종류

```
┌────────────────────────────────────────────────────────┐
│                   방화벽 종류                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 패킷 필터링 방화벽 (Packet Filtering)              │
│     ┌────────────────────────────────────────────┐    │
│     │ L3/L4 계층 기반                            │    │
│     │ - IP 주소, 포트 번호로 필터링              │    │
│     │ - 상태 비저장 (Stateless)                  │    │
│     │ - 장점: 빠름                              │    │
│     │ - 단점: 컨텍스트 없음                      │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 상태 기반 방화벽 (Stateful Inspection)             │
│     ┌────────────────────────────────────────────┐    │
│     │ 연결 상태 추적                             │    │
│     │ - TCP 세션 상태 관리                       │    │
│     │ - SYN, ACK 등 플래그 확인                  │    │
│     │ - 장점: 더 안전                           │    │
│     │ - 단점: 느림                              │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  3. 애플리케이션 방화벽 (Application Layer)            │
│     ┌────────────────────────────────────────────┐    │
│     │ L7 계층 기반                               │    │
│     │ - HTTP, FTP, DNS 등 검사                   │    │
│     │ - DPI (Deep Packet Inspection)            │    │
│     │ - WAF (Web Application Firewall)          │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  4. 차세대 방화벽 (NGFW: Next-Generation Firewall)     │
│     ┌────────────────────────────────────────────┐    │
│     │ 통합 보안 기능                             │    │
│     │ - 방화벽 + IPS + 앱 인식 + URL 필터링     │    │
│     │ - 사용자 식별                             │    │
│     │ - 위협情报 연동                            │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. IDS vs IPS

```
┌────────────────────────────────────────────────────────┐
│                   IDS vs IPS                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  IDS (Intrusion Detection System):                     │
│  ┌────────────────────────────────────────────┐       │
│  │ [트래픽] → [탐지] → [알림]                 │       │
│  │                                            │       │
│  │ • 수동 대응                                │       │
│  │ • 로그, 알림                               │       │
│  │ • 탐지 전용                                │       │
│  │ • 네트워크에 영향 없음                      │       │
│  └────────────────────────────────────────────┘       │
│                                                        │
│  IPS (Intrusion Prevention System):                    │
│  ┌────────────────────────────────────────────┐       │
│  │ [트래픽] → [탐지] → [차단] → [알림]        │       │
│  │                                            │       │
│  │ • 능동 대응                                │       │
│  │ • 자동 차단                                │       │
│  │ • Inline 배치                              │       │
│  │ • 실시간 방어                              │       │
│  └────────────────────────────────────────────┘       │
│                                                        │
│  탐지 방식:                                            │
│  ┌────────────────────────────────────────┐           │
│  │ 1. 시그니처 기반 (Signature-based)     │           │
│  │    - 알려진 공격 패턴 매칭             │           │
│  │    - 장점: 정확                        │           │
│  │    - 단점: 새로운 공격 탐지 불가       │           │
│  │                                        │           │
│  │ 2. 이상 탐지 (Anomaly-based)           │           │
│  │    - 정상 패턴 학습 후 이상 탐지        │           │
│  │    - 장점: 새로운 공격 탐지            │           │
│  │    - 단점: 오탐 가능성                 │           │
│  └────────────────────────────────────────┘           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 방화벽 규칙

```
┌────────────────────────────────────────────────────────┐
│                  방화벽 규칙 예시                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  규칙 구조:                                            │
│  [번호] [액션] [출발지] [목적지] [포트] [프로토콜]     │
│                                                        │
│  예시:                                                 │
│  ┌─────┬────────┬──────────┬──────────┬──────┬──────┐│
│  │ 번호│ 액션   │ 출발지   │ 목적지   │ 포트 │ 프로 ││
│  ├─────┼────────┼──────────┼──────────┼──────┼──────┤│
│  │ 1   │ 허용   │ Any      │ 웹서버   │ 80   │ TCP  ││
│  │ 2   │ 허용   │ Any      │ 웹서버   │ 443  │ TCP  ││
│  │ 3   │ 허용   │ 내부망   │ DB서버   │ 3306 │ TCP  ││
│  │ 4   │ 차단   │ 외부     │ DB서버   │ Any  │ Any  ││
│  │ 5   │ 차단   │ Any      │ Any      │ Any  │ Any  ││
│  └─────┴────────┴──────────┴──────────┴──────┴──────┘│
│                                                        │
│  규칙 적용 순서: 위에서 아래로                         │
│  기본 정책: Deny All (모두 차단 후 필요한 것만 허용)   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import re

class Action(Enum):
    ALLOW = "허용"
    DENY = "차단"
    LOG = "로그"

class Protocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    ANY = "ANY"

@dataclass
class FirewallRule:
    """방화벽 규칙"""
    rule_id: int
    action: Action
    source_ip: str
    dest_ip: str
    port: str  # "80", "443", "any", "1024-65535"
    protocol: Protocol
    description: str = ""

@dataclass
class Packet:
    """네트워크 패킷"""
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: Protocol
    payload: str = ""
    flags: List[str] = field(default_factory=list)

@dataclass
class Connection:
    """연결 상태"""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: Protocol
    state: str = "NEW"
    packets: int = 0
    bytes: int = 0

class StatefulFirewall:
    """상태 기반 방화벽"""

    def __init__(self):
        self.rules: List[FirewallRule] = []
        self.connections: Dict[str, Connection] = {}
        self.log: List[Dict] = []
        self.default_action = Action.DENY

    def add_rule(self, action: Action, source: str, dest: str,
                 port: str, protocol: Protocol, desc: str = ""):
        """규칙 추가"""
        rule = FirewallRule(
            rule_id=len(self.rules) + 1,
            action=action,
            source_ip=source,
            dest_ip=dest,
            port=port,
            protocol=protocol,
            description=desc
        )
        self.rules.append(rule)
        print(f"[방화벽] 규칙 #{rule.rule_id} 추가: {action.value} {source}→{dest}:{port}")

    def process_packet(self, packet: Packet) -> Tuple[bool, str]:
        """패킷 처리"""
        # 1. 연결 상태 확인
        conn_key = f"{packet.source_ip}:{packet.source_port}->{packet.dest_ip}:{packet.dest_port}"

        if conn_key in self.connections:
            # 기존 연결 - 상태 업데이트
            conn = self.connections[conn_key]
            conn.packets += 1
            conn.state = "ESTABLISHED"
            return True, "기존 연결"

        # 2. 규칙 매칭
        for rule in self.rules:
            if self._match_rule(rule, packet):
                # 로그 기록
                log_entry = {
                    'timestamp': datetime.now(),
                    'rule_id': rule.rule_id,
                    'action': rule.action.value,
                    'packet': f"{packet.source_ip}:{packet.source_port} → {packet.dest_ip}:{packet.dest_port}"
                }
                self.log.append(log_entry)

                if rule.action == Action.ALLOW:
                    # 새 연결 생성
                    self.connections[conn_key] = Connection(
                        src_ip=packet.source_ip,
                        dst_ip=packet.dest_ip,
                        src_port=packet.source_port,
                        dst_port=packet.dest_port,
                        protocol=packet.protocol,
                        state="NEW"
                    )
                    return True, f"규칙 #{rule.rule_id} 허용"
                else:
                    return False, f"규칙 #{rule.rule_id} 차단"

        # 3. 기본 정책
        return False, f"기본 정책: {self.default_action.value}"

    def _match_rule(self, rule: FirewallRule, packet: Packet) -> bool:
        """규칙 매칭"""
        # 출발지 IP
        if rule.source_ip != "any" and not self._ip_match(packet.source_ip, rule.source_ip):
            return False

        # 목적지 IP
        if rule.dest_ip != "any" and not self._ip_match(packet.dest_ip, rule.dest_ip):
            return False

        # 포트
        if rule.port != "any":
            if not self._port_match(packet.dest_port, rule.port):
                return False

        # 프로토콜
        if rule.protocol != Protocol.ANY and packet.protocol != rule.protocol:
            return False

        return True

    def _ip_match(self, packet_ip: str, rule_ip: str) -> bool:
        """IP 매칭 (간단한 버전)"""
        if rule_ip == "any":
            return True
        if "/" in rule_ip:
            # CIDR (간단히 처리)
            return packet_ip.startswith(rule_ip.split("/")[0][:-1])
        return packet_ip == rule_ip

    def _port_match(self, packet_port: int, rule_port: str) -> bool:
        """포트 매칭"""
        if rule_port == "any":
            return True
        if "-" in rule_port:
            start, end = map(int, rule_port.split("-"))
            return start <= packet_port <= end
        return packet_port == int(rule_port)

    def get_log(self, limit: int = 10) -> List[Dict]:
        """로그 조회"""
        return self.log[-limit:]

class IDSSimulator:
    """IDS 시뮬레이터"""

    def __init__(self):
        self.signatures: Dict[str, str] = {
            "sql_injection": r"(?i)(union.*select|select.*from|insert.*into)",
            "xss": r"(?i)(<script|javascript:|onerror=)",
            "port_scan": "rapid_connections",
            "ddos": "high_volume"
        }
        self.alerts: List[Dict] = []

    def analyze_packet(self, packet: Packet) -> Optional[Dict]:
        """패킷 분석"""
        # 시그니처 기반 탐지
        for attack_type, pattern in self.signatures.items():
            if attack_type in ["sql_injection", "xss"]:
                if re.search(pattern, packet.payload):
                    alert = {
                        'type': attack_type,
                        'severity': 'HIGH',
                        'source': packet.source_ip,
                        'timestamp': datetime.now(),
                        'payload_sample': packet.payload[:50]
                    }
                    self.alerts.append(alert)
                    return alert

        return None

    def analyze_traffic_pattern(self, packets: List[Packet]) -> List[Dict]:
        """트래픽 패턴 분석"""
        alerts = []

        # DDoS 탐지 (같은 출발지에서 많은 요청)
        source_counts = {}
        for p in packets:
            source_counts[p.source_ip] = source_counts.get(p.source_ip, 0) + 1

        for ip, count in source_counts.items():
            if count > 100:  # 임계값
                alert = {
                    'type': 'ddos',
                    'severity': 'CRITICAL',
                    'source': ip,
                    'count': count
                }
                alerts.append(alert)
                self.alerts.append(alert)

        return alerts


# 사용 예시
print("=== 방화벽 & IDS 시뮬레이션 ===\n")

# 방화벽 설정
print("--- 방화벽 규칙 설정 ---")
fw = StatefulFirewall()
fw.add_rule(Action.ALLOW, "any", "192.168.1.10", "80", Protocol.TCP, "웹 서버 HTTP")
fw.add_rule(Action.ALLOW, "any", "192.168.1.10", "443", Protocol.TCP, "웹 서버 HTTPS")
fw.add_rule(Action.ALLOW, "192.168.1.0/24", "192.168.1.20", "3306", Protocol.TCP, "내부 DB 접근")
fw.add_rule(Action.DENY, "any", "192.168.1.20", "any", Protocol.ANY, "외부 DB 접근 차단")

# 패킷 처리
print("\n--- 패킷 처리 ---")
packets = [
    Packet("1.2.3.4", "192.168.1.10", 54321, 80, Protocol.TCP, "GET /index.html"),
    Packet("5.6.7.8", "192.168.1.20", 12345, 3306, Protocol.TCP, "SELECT * FROM users"),
    Packet("1.2.3.4", "192.168.1.10", 54322, 443, Protocol.TCP, "GET /secure"),
]

for p in packets:
    allowed, reason = fw.process_packet(p)
    print(f"{p.source_ip}→{p.dest_ip}:{p.dest_port} → {reason}")

# IDS 분석
print("\n--- IDS 탐지 ---")
ids = IDSSimulator()
attack_packet = Packet("10.0.0.1", "192.168.1.10", 1234, 80, Protocol.TCP,
                       "GET /?id=1 UNION SELECT * FROM users")
alert = ids.analyze_packet(attack_packet)
if alert:
    print(f"[ALERT] {alert['type']}: {alert['severity']} from {alert['source']}")
