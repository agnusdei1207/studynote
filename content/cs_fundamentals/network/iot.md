+++
title = "사물인터넷 (IoT: Internet of Things)"
date = 2025-03-01

[extra]
categories = "cs_fundamentals-network"
+++

# 사물인터넷 (IoT: Internet of Things)

## 핵심 인사이트 (3줄 요약)
> **사물에 센서와 통신 기능을 탑재**하여 인터넷에 연결. 데이터 수집, 분석, 제어를 통해 스마트 서비스 제공. 스마트홈, 스마트시티, 산업자동화 등에 활용된다.

## 1. 개념
사물인터넷(IoT)은 **물리적 사물에 센서, 통신, 처리 기능을 탑재**하여 인터넷에 연결하고, 수집된 데이터를 분석하여 지능형 서비스를 제공하는 기술이다.

> 비유: "사물이 말하는 세상" - 냉장고가 우유 없다고 알려줌

## 2. IoT 구조

```
┌─────────────────────────────────────────────────────┐
│                    응용 계층                         │
│  스마트홈 │ 스마트시티 │ 스마트팜 │ 헬스케어        │
├─────────────────────────────────────────────────────┤
│                    플랫폼 계층                       │
│  데이터 처리 │ 분석 │ AI │ API                      │
├─────────────────────────────────────────────────────┤
│                    네트워크 계층                     │
│  WiFi │ LTE-M │ NB-IoT │ LoRa │ BLE │ Zigbee       │
├─────────────────────────────────────────────────────┤
│                    장치 계층                         │
│  센서 │ 액추에이터 │ 게이트웨이                     │
└─────────────────────────────────────────────────────┘
```

## 3. IoT 구성 요소

### 3.1 센서 (Sensor)
```
역할: 물리적 현상을 전기 신호로 변환

종류:
- 온도/습도 센서
- 가속도/자이로 센서
- 조도 센서
- 가스 센서
- 위치 센서 (GPS)
- 카메라 (이미지 센서)
```

### 3.2 액추에이터 (Actuator)
```
역할: 전기 신호를 물리적 동작으로 변환

종류:
- 모터
- 솔레노이드
- 릴레이
- 스피커
- LED
```

### 3.3 게이트웨이 (Gateway)
```
역할:
- 센서 네트워크와 인터넷 연결
- 프로토콜 변환
- 데이터 집계/필터링
- 보안 기능

예:
- 스마트홈 허브
- 산업용 게이트웨이
```

## 4. IoT 통신 기술

### 4.1 근거리 통신

| 기술 | 범위 | 속도 | 전력 | 용도 |
|------|------|------|------|------|
| WiFi | 100m | 고속 | 중간 | 스마트홈 |
| BLE | 100m | 2Mbps | 낮음 | 웨어러블 |
| Zigbee | 100m | 250kbps | 낮음 | 스마트홈 |
| Z-Wave | 30m | 100kbps | 낮음 | 홈오토메이션 |
| NFC | 10cm | 424kbps | 낮음 | 결제 |

### 4.2 LPWAN (저전력 광역망)

| 기술 | 범위 | 속도 | 전력 | 특징 |
|------|------|------|------|------|
| LoRa | 15km | 50kbps | 초저전력 | 비면허 |
| NB-IoT | 10km | 250kbps | 저전력 | LTE 기반 |
| LTE-M | 10km | 1Mbps | 저전력 | 이동성 |
| Sigfox | 50km | 100bps | 초저전력 | 단순 |

### 4.3 기술 비교

```
             전력 소모
                ↑
         높음   │    WiFi
                │         BLE
                │              Zigbee
                │
                │        LTE-M
                │    NB-IoT
                │  LoRa
         낮음   │ Sigfox
                └──────────────────→ 전송 거리
                 단거리        장거리
```

## 5. IoT 플랫폼

```
기능:
1. 디바이스 관리
2. 데이터 수집/저장
3. 데이터 분석
4. 규칙 엔진
5. API 제공

주요 플랫폼:
- AWS IoT Core
- Azure IoT Hub
- Google Cloud IoT
- Samsung ARTIK
- ThingSpeak (오픈소스)
```

## 6. IoT 보안

### 6.1 보안 위협
```
1. 디바이스 탈취
   - 물리적 공격
   - 펌웨어 변조

2. 통신 도청
   - 데이터 가로채기
   - 중간자 공격

3. 서비스 거부 (DoS)
   - DDoS 공격
   - 봇넷 활용

4. 데이터 유출
   - 개인정보 침해
   - 민감 정보 노출
```

### 6.2 보안 대책
```
1. 인증/인가
   - 디바이스 인증
   - 접근 제어

2. 암호화
   - 통신 구간 암호화 (TLS)
   - 저장 데이터 암호화

3. 펌웨어 보안
   - 보안 부팅
   - 정기 업데이트

4. 네트워크 보안
   - 방화벽
   - 침입 탐지
```

## 7. IoT 활용 분야

### 7.1 스마트홈
```
- 조명 제어
- 온도 조절
- 보안 시스템
- 에너지 관리
- 음성 비서

기술: WiFi, Zigbee, BLE
```

### 7.2 스마트시티
```
- 교통 관리
- 주차 시스템
- 환경 모니터링
- 가로등 제어
- 쓰레기 수거

기술: LoRa, NB-IoT
```

### 7.3 스마트팜
```
- 온실 제어
- 관수 시스템
- 가축 관리
- 작물 모니터링

기술: 센서 네트워크, LoRa
```

### 7.4 산업 IoT (IIoT)
```
- 설비 모니터링
- 예지 보전
- 품질 관리
- 공정 최적화

기술: 5G, WiFi, 이더넷
```

## 8. 코드 예시

```python
import random
import time
from datetime import datetime

class Sensor:
    """센서 시뮬레이션"""

    def __init__(self, sensor_id, sensor_type, unit):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit

    def read(self):
        """센서 값 읽기"""
        if self.sensor_type == 'temperature':
            value = random.uniform(18, 28)
        elif self.sensor_type == 'humidity':
            value = random.uniform(40, 70)
        elif self.sensor_type == 'light':
            value = random.uniform(0, 1000)
        else:
            value = random.uniform(0, 100)

        return {
            'sensor_id': self.sensor_id,
            'type': self.sensor_type,
            'value': round(value, 2),
            'unit': self.unit,
            'timestamp': datetime.now().isoformat()
        }


class Actuator:
    """액추에이터 시뮬레이션"""

    def __init__(self, actuator_id, actuator_type):
        self.actuator_id = actuator_id
        self.actuator_type = actuator_type
        self.state = False

    def control(self, command):
        """액추에이터 제어"""
        if command == 'ON':
            self.state = True
        elif command == 'OFF':
            self.state = False

        return {
            'actuator_id': self.actuator_id,
            'type': self.actuator_type,
            'state': 'ON' if self.state else 'OFF',
            'timestamp': datetime.now().isoformat()
        }


class IoTHub:
    """IoT 허브 시뮬레이션"""

    def __init__(self):
        self.sensors = {}
        self.actuators = {}
        self.rules = []
        self.data_log = []

    def register_sensor(self, sensor):
        self.sensors[sensor.sensor_id] = sensor

    def register_actuator(self, actuator):
        self.actuators[actuator.actuator_id] = actuator

    def add_rule(self, condition, action):
        """자동화 규칙 추가"""
        self.rules.append({
            'condition': condition,
            'action': action
        })

    def collect_data(self):
        """센서 데이터 수집"""
        for sensor_id, sensor in self.sensors.items():
            data = sensor.read()
            self.data_log.append(data)
            self._check_rules(data)
            print(f"수집: {data}")

    def _check_rules(self, data):
        """규칙 확인 및 실행"""
        for rule in self.rules:
            if rule['condition'](data):
                action = rule['action']
                if action['type'] == 'actuator':
                    actuator = self.actuators.get(action['id'])
                    if actuator:
                        result = actuator.control(action['command'])
                        print(f"자동화 실행: {result}")

    def control_actuator(self, actuator_id, command):
        """액추에이터 제어"""
        actuator = self.actuators.get(actuator_id)
        if actuator:
            return actuator.control(command)
        return None


# 스마트홈 시뮬레이션
print("=== 스마트홈 IoT 시뮬레이션 ===\n")

# 허브 생성
hub = IoTHub()

# 센서 등록
temp_sensor = Sensor('S001', 'temperature', '°C')
humidity_sensor = Sensor('S002', 'humidity', '%')
light_sensor = Sensor('S003', 'light', 'lux')

hub.register_sensor(temp_sensor)
hub.register_sensor(humidity_sensor)
hub.register_sensor(light_sensor)

# 액추에이터 등록
ac = Actuator('A001', 'air_conditioner')
light = Actuator('A002', 'light')

hub.register_actuator(ac)
hub.register_actuator(light)

# 자동화 규칙 추가
hub.add_rule(
    condition=lambda d: d['type'] == 'temperature' and d['value'] > 26,
    action={'type': 'actuator', 'id': 'A001', 'command': 'ON'}
)

hub.add_rule(
    condition=lambda d: d['type'] == 'temperature' and d['value'] < 20,
    action={'type': 'actuator', 'id': 'A001', 'command': 'OFF'}
)

hub.add_rule(
    condition=lambda d: d['type'] == 'light' and d['value'] < 100,
    action={'type': 'actuator', 'id': 'A002', 'command': 'ON'}
)

# 데이터 수집 및 자동화 실행
print("센서 데이터 수집 및 자동화 실행:\n")
for i in range(5):
    print(f"--- 사이클 {i+1} ---")
    hub.collect_data()
    time.sleep(0.5)
    print()

# 수동 제어
print("수동 제어:")
result = hub.control_actuator('A002', 'OFF')
print(f"조명 끄기: {result}")
