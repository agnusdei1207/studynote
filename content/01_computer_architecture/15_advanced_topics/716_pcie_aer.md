---
title: "PCIe AER (Advanced Error Reporting)"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 716
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PCIe AER (Peripheral Component Interconnect Express Advanced Error Reporting)은 PCIe 장치와 루트 포트가 오류 상태, 심각도, 패킷 헤더 정보를 구조적으로 기록하고 운영체제에 전달하는 오류 보고 확장 기능이다.
> 2. **가치**: 일시적 링크 오류는 기록만 남기고 넘어가고, 복구 가능한 장치 오류는 드라이버 리셋으로 격리하며, 치명적 결함은 더 넓은 장애로 번지기 전에 포트 단위로 차단할 수 있어 시스템 복원력이 높아진다.
> 3. **판단 포인트**: 핵심은 "오류가 있었는가"보다 "어떤 계층에서 얼마나 자주, 어떤 심각도로 반복되는가"이며, Corrected 로그가 누적되면 신호 무결성·전원·펌웨어 호환성 문제를 의심해야 한다.

---

## Ⅰ. 개요 및 필요성

PCIe (Peripheral Component Interconnect Express)는 GPU (Graphics Processing Unit), NVMe (Non-Volatile Memory Express) SSD, NIC (Network Interface Card), 가속기 같은 고속 장치를 CPU (Central Processing Unit)와 연결하는 핵심 인터커넥트다. 속도가 세대마다 커질수록 신호 무결성, 커넥터 품질, 리타이머(retimer), 케이블, 전원 품질 같은 요소가 오류 가능성에 더 큰 영향을 준다. 이때 단순히 "장치가 사라졌다" 수준의 메시지만으로는 장애 원인을 좁히기 어렵다.

PCIe AER는 이런 문제를 해결하기 위해 등장했다. 장치나 루트 포트가 오류를 만나면, 무엇이 잘못되었는지 상태 비트와 헤더 로그로 남기고, 그 오류가 Corrected인지, Uncorrectable-Non-Fatal인지, Fatal인지 구분해 상위 소프트웨어가 다르게 대응할 수 있게 만든다.

즉 AER의 필요성은 단순한 오류 감지가 아니라 <strong>오류의 등급화와 가시화</strong>에 있다. 그래야 운영체제와 드라이버가 전체 시스템을 불필요하게 멈추지 않고, 가능한 범위에서 장치만 복구하거나 격리할 수 있다.

- **📢 섹션 요약 비유**: PCIe AER는 공항 관제탑의 사고 분류 체계와 같다. 활주로에 작은 돌멩이가 있는지, 한 비행기의 장비가 고장 났는지, 활주로 자체가 막혔는지를 구분해야 전체 공항을 멈출지 부분 통제할지 결정할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

AER는 PCIe의 Extended Capability 영역에 존재하며, 엔드포인트(endpoint)와 루트 포트(root port)가 오류 상태를 기록하고 전달하는 레지스터 집합으로 구현된다. 여기에는 Correctable Error Status/Mask, Uncorrectable Error Status/Mask, Severity, Header Log, Root Error Status 같은 필드가 포함된다. 즉 AER는 "오류를 고치는 회로"라기보다 <strong>오류를 분류·기록·전파해 복구 루프를 여는 계층</strong>이다.

### 동작 흐름

1. 링크·데이터 링크·트랜잭션 계층에서 오류가 감지된다.
2. 장치 또는 루트 포트의 AER 레지스터가 상태 비트와 관련 헤더를 기록한다.
3. ERR_COR, ERR_NONFATAL, ERR_FATAL 같은 메시지가 루트 방향으로 보고된다.
4. 운영체제의 PCIe 포트 서비스 드라이버가 이를 받아 로그를 남기고 복구 루틴을 호출한다.
5. 필요 시 장치 리셋, 함수 오프라인, 포트 리셋, DPC (Downstream Port Containment) 연계가 수행된다.

| AER 구성 요소 | 역할 | 실무 해석 |
| :-- | :-- | :-- |
| Correctable Status/Mask | 재시도나 무시 가능한 오류 기록 | 누적 증가 시 링크 품질 점검 |
| Uncorrectable Status | 복구 불가 오류 기록 | 원인 범위 축소의 핵심 |
| Severity Register | 오류를 Non-Fatal/Fatal로 구분 | 서비스 영향도 판단 |
| Header Log | 문제 패킷의 헤더 저장 | 어떤 트랜잭션이 문제였는지 추적 |
| Root Error Status/Command | 루트 포트 차원의 집계·통지 | 운영체제와 RAS (Reliability, Availability, Serviceability) 정책 연동 |

아래 그림은 AER가 단일 장치 로그가 아니라, 장치->루트 포트->운영체제로 이어지는 보고 경로임을 나타낸다.

```text
+--------------+      error       +--------------+      report      +--------------+
| Endpoint /   +-----------------> | Root Port    +-----------------> | Operating    |
| Switch Port  |                  | AER Registers|                  | System AER   |
+------+-------+                  +------+-------+                  +------+-------+
       |                                  |                                 |
       | set status bits                  | root error status               |
       v                                  v                                 v
  Header Log                        ERR_COR / NONFATAL / FATAL        Reset / Quarantine
```

여기서 중요한 점은 Corrected 오류가 AER 자체로 "수리"되는 것이 아니라, 대개 데이터 링크 계층의 재전송(replay)이나 하위 메커니즘으로 이미 복구되었다는 사실이다. AER는 그 사실을 구조적으로 알리고, 반복 빈도를 운영자가 볼 수 있게 만든다. 반대로 Uncorrectable 오류는 Severity 설정에 따라 서비스 영향이 달라지며, Fatal이면 더 강한 차단과 리셋이 뒤따른다.

- **📢 섹션 요약 비유**: AER는 응급실 접수대와 같다. 환자를 직접 치료하는 수술실이 아니라, 어디가 다쳤는지 기록하고 중증도를 분류해 어느 방으로 보내야 할지 결정하는 역할을 맡는다.

---

## Ⅲ. 비교 및 연결

PCIe 오류 복원력을 이해하려면 AER 하나만 보면 안 된다. 하위 계층의 자동 재전송, AER의 보고, DPC의 차단이 서로 다른 역할을 맡는다.

| 메커니즘 | 주 역할 | 잘하는 일 | 한계 |
| :-- | :-- | :-- | :-- |
| Data Link Replay | 일시적 전송 오류 재전송 | 소규모 비트 오류를 빠르게 복구 | 원인 분석 정보가 적음 |
| AER | 구조적 오류 기록·분류·통지 | 로그, 심각도, 소프트웨어 복구 연결 | 물리적 결함 자체를 제거하지는 못함 |
| DPC (Downstream Port Containment) | 심각한 하위 포트 오류 격리 | 장애 확산 차단 | 장치가 오프라인될 수 있음 |

또한 AER가 남기는 세 가지 대표 분류는 실무 해석의 출발점이 된다.

| 분류 | 의미 | 보통의 대응 |
| :-- | :-- | :-- |
| Corrected | 하위 계층 재시도 등으로 처리됨 | 추세 관찰, 케이블/리타이머/슬롯 점검 |
| Uncorrectable Non-Fatal | 장치나 요청은 문제가 있지만 시스템 전체는 살릴 수 있음 | 드라이버 복구, 함수 리셋, 워크로드 재배치 |
| Uncorrectable Fatal | 포트·링크·장치 수준에서 강한 차단 필요 | 장치 격리, 포트 리셋, 부품 교체 |

이 비교에서 얻어야 할 핵심은 AER가 장애를 "없애는 기술"이 아니라 "장애의 폭을 줄이는 기술"이라는 점이다. 단발 Corrected 에러는 흔할 수 있지만, 특정 슬롯이나 장치에서 집중적으로 증가한다면 이미 물리 계층 문제가 진행 중일 가능성이 높다.

- **📢 섹션 요약 비유**: 재전송은 넘어져도 스스로 다시 일어나는 수준이고, AER는 넘어졌다는 사실을 기록해 보건실로 보내는 단계이며, DPC는 위험한 계단을 아예 출입 금지시키는 조치에 가깝다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서 AER 로그는 특히 고속 NIC, NVMe 백플레인, GPU 서버, 라이저 카드, 리타이머가 많은 플랫폼에서 중요하다. Linux에서는 `dmesg`, `journalctl`, `lspci -vv` 등으로 AER 상태를 추적할 수 있고, 펌웨어에서는 BIOS/UEFI에서 AER·DPC 활성화 여부를 확인할 수 있다. 문제는 로그가 떴다는 사실보다 <strong>빈도와 위치</strong>다.

### 실무 판단 기준

- **Corrected 오류가 드물게 발생**: 일시적 노이즈일 수 있으므로 추세만 관찰
- **Corrected 오류가 특정 장치에서 지속 증가**: 슬롯 접점, 케이블, 냉각, 리타이머, 전원 품질 점검
- **Non-Fatal 오류 반복**: 펌웨어/드라이버 호환성, BAR (Base Address Register) 매핑, DMA (Direct Memory Access) 경로, 장치 리셋 정책 검토
- **Fatal 오류 또는 Surprise Down**: 부품 교체와 포트 격리 우선, DPC·핫플러그 회복 절차 확인

### 안티패턴

- 로그가 시끄럽다는 이유로 AER 마스킹만 하고 원인 분석을 생략
- Corrected를 무해하다고 단정해 장기간 방치
- AER는 켰지만 드라이버의 에러 복구 콜백은 검증하지 않음
- 고속 PCIe 5.0/6.0 플랫폼에서 케이블·백플레인 SI (Signal Integrity) 검증 없이 운영

실무 관점에서는 AER를 <strong>RAS 향상 메커니즘</strong>으로 서술해야 한다. 즉 오류를 조기에 감지하고, 영향 범위를 장치나 포트 수준으로 제한하고, 반복 패턴을 통해 사전 교체까지 연결하는 구조다. 특히 DPC, Hot-Plug, 드라이버 복구, 로그 분석 체계와 함께 설명하면 답안의 입체감이 커진다.

- **📢 섹션 요약 비유**: AER 로그는 자동차 계기판의 경고등과 같다. 한 번 반짝이고 끝나면 경과 관찰이 가능하지만, 같은 경고가 계속 뜨면 엔진을 열어 봐야지 테이프로 가리고 운전해서는 안 된다.

---

## Ⅴ. 기대효과 및 결론

PCIe AER를 적절히 활용하면 고속 I/O 시스템의 장애를 더 작고 더 관측 가능한 문제로 줄일 수 있다. 장치가 순간적으로 흔들려도 시스템 전체가 무조건 멈추지 않고, 오류 헤더와 심각도 정보가 남아 원인 분석 속도가 빨라진다. 이는 대규모 서버 팜에서 가동률과 정비 효율을 동시에 높인다.

하지만 AER는 물리적 결함을 마법처럼 치유하지 않는다. 반복되는 Corrected 오류는 결국 링크 품질 불량, 슬롯 마모, 케이블 문제, 발열, 전원 불안정 등 하드웨어 근본 원인을 해결해야 끝난다. 또한 고속 세대로 갈수록 로그량과 복구 정책의 복잡도도 함께 증가한다.

정리하면 PCIe AER는 "PCIe 에러 로그 기능"이 아니라, <strong>버스 장애를 분류하고 복구 가능한 범위로 묶어 시스템 복원력을 높이는 RAS 계층</strong>으로 기억해야 한다.

- **📢 섹션 요약 비유**: 좋은 안전벨트는 사고를 없애 주지 않지만, 사고가 났을 때 피해 범위를 줄여 준다. AER도 PCIe 세계에서 그런 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| PCIe Data Link Replay | 일시적 전송 오류를 하위 계층에서 재전송 |
| DPC (Downstream Port Containment) | 치명적 오류를 포트 단위로 격리 |
| Hot-Plug / Slot Reset | 장치 복구와 재열거에 필요한 운영 메커니즘 |
| RAS (Reliability, Availability, Serviceability) | AER를 도입하는 상위 목적 |
| Signal Integrity | Corrected 오류 증가 시 가장 먼저 점검할 물리 계층 품질 |

### 📈 관련 키워드 및 발전 흐름도

```text
PCIe Link Errors
      |
      v
Replay / Retry at Data Link Layer
      |
      v
AER Status + Header Log + Severity
      |
      +---> Operating System Error Handling
      +---> Driver Recovery / Reset
      +---> DPC Containment
      |
      v
Higher RAS for GPU / NVMe / NIC Platforms
```

이 흐름은 단순 재전송에서 구조적 오류 보고와 격리, 그리고 플랫폼 수준 복원력 강화로 이어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안의 빠른 길(PCIe)에서 택배 상자가 흔들리면, AER는 얼마나 심한 사고인지 먼저 적어 두는 기록관이에요.
2. 살짝 부딪힌 정도면 다시 보내고, 많이 망가졌으면 그 택배차만 잠깐 세워서 고쳐요.
3. 그래서 길 전체를 다 막지 않고도 고장 난 부분만 더 똑똑하게 다룰 수 있답니다.
