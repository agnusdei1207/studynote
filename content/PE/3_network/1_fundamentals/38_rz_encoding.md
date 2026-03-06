+++
title = "38. RZ (Return to Zero) 부호화"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["Line-Coding", "RZ", "Digital-Signaling", "Synchronization"]
draft = false
+++

# RZ (Return to Zero) 부호화

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RZ는 **"비트 **기간**의 **절반**만 **신호**를 **유지**하고 **나머지 **절반**은 **0**으로 **복귀**하는 **디지털 **신호 **방식\\\"**으로, **NRZ**(Non-Return to Zero)와 **대조**된다.
> 2. **동기화**: 모든 **비트 **구간**에 **신호 **변화**가 **있어 **비트 **동기화**에 **유리**하지만 **대역폭**이 **2배**로 **증가**하고 **DC 성분**이 **포함**될 수 **있다**.
> 3. **변형**: **Unipolar RZ**(단극성), **Polar RZ**(극성), **Bipolar RZ**(양극성/AMI)가 **있고 **RZ**는 **주로 **광통신**과 **고속 **시리얼 **통신**에 **사용**된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
RZ 부호화는 **"신호를 0으로 되돌리는 방식"**이다.

**라인 부호화 비교**:
| 부호화 | 비트 구간 | DC 성분 | 대역폭 | 동기화 |
|--------|-----------|---------|--------|--------|
| **NRZ-L** | 전체 | 있음 | B | 불리 |
| **NRZ-I** | 전체 | 없음 | B | 불리 |
| **RZ** | 절반 | 있음/없음 | 2B | 유리 |
| **Manchester** | 절반 | 없음 | 2B | 유리 |

### 💡 비유
RZ는 **모스 부호의 점(·)**과 같다.
- **1**: 짧게 켜짐 → 끔
- **0**: 계속 끔
- **매 비트마다 변화**: 타이밍 정보 제공

---

## Ⅱ. 아키텍처 및 핵심 원리

### RZ 부호화 방식

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RZ Encoding Variants                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Unipolar RZ (단극성 RZ):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Logic 1: +V for half period, then 0                                                      │  │
    │  Logic 0: 0 for entire period                                                             │  │
    │                                                                                         │  │
    │  Data:    1    1    0    1    0    0                                                      │  │
    │         ┌─┐  ┌─┐       ┌─┐                                                              │  │
    │         │ │  │ │       │ │                                                              │  │
    │    ─────┘ └──┘ └───────┘ └─────────────────────────────────────────────                  │  │
    │         ↑              ↑                                                                │  │
    │         Return to 0    Return to 0                                                       │  │
    │                                                                                         │  │
    │  → Problem: DC component (average voltage ≠ 0)                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Polar RZ (극성 RZ):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Logic 1: +V for half period, then 0                                                      │  │
    │  Logic 0: -V for half period, then 0                                                      │  │
    │                                                                                         │  │
    │  Data:    1    1    0    1    0    0                                                      │  │
    │         ┌─┐  ┌─┐  ┌─┐  ┌─┐                                                              │  │
    │         │ │  │ │  │ │  │ │                                                              │  │
    │    ─────┘ └──┘ └──┘  └──────────────────────────────────────────────────────────         │  │
    │               └──┘                                                                  │  │
    │  → No DC component (balanced), but requires 2 voltage levels                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Bipolar RZ / AMI RZ (Alternate Mark Inversion):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Logic 1: Alternating +V and -V for half period, then 0                                  │  │
    │  Logic 0: 0 for entire period                                                             │  │
    │                                                                                         │  │
    │  Data:    1    1    0    1    0    0    1    1                                            │  │
    │         ┌─┐  ┌─┐       ┌─┐      ┌─┐  ┌─┐                                                │  │
    │         │ │  │ │       │ │      │ │  │ │                                                │  │
    │    ─────┘ └──┘ └───────┘ └─────┘ └──┘ └─────────────────────────────────────────────────  │  │
    │               └──┐  ┌──┘                                                               │  │
    │                  └──┘                                                                  │  │
    │         +V      -V      0    +V     -V     +V                                           │  │
    │                                                                                         │  │
    │  → No DC component, error detection (violations indicate errors)                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### RZ vs NRZ 비교

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RZ vs NRZ Comparison                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    NRZ-L (Non-Return to Zero Level):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Data:    1    1    0    1    0    0    1    1                                            │  │
    │         ┌───────────────┐       ┌─────┐       ┌───────────────────────┐                   │  │
    │         │               │       │     │       │                       │                   │  │
    │    ─────┘               └───────┘     └───────┘                       └─────              │  │
    │                                                                                         │  │
    │  Problem: Long sequences of 1s or 0s → Clock recovery difficult                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    RZ (Return to Zero):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Data:    1    1    0    1    0    0    1    1                                            │  │
    │         ┌─┐  ┌─┐       ┌─┐      ┌─┐  ┌─┐                                                │  │
    │         │ │  │ │       │ │      │ │  │ │                                                │  │
    │    ─────┘ └──┘ └───────┘ └─────┘ └──┘ └─────────────────────────────────────────────────  │  │
    │                                                                                         │  │
    │  Advantage: Transition in every bit period → Easy clock recovery                         │  │
    │  Disadvantage: 2x bandwidth required                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Bandwidth Comparison:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  NRZ: Data rate = 1/T (T = bit period)                                                   │  │
    │  RZ:  Data rate = 1/T, but signal requires bandwidth = 2/T                               │  │
    │                                                                                         │  │
    │  Example: 1 Mbps data                                                                    │  │
    │  • NRZ: 1 MHz bandwidth                                                                  │  │
    │  • RZ:  2 MHz bandwidth                                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### RZ의 동기화 특성

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Clock Recovery in RZ                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Clock Recovery Circuit:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  RZ Signal                     Edge Detector              Clock Extractor                │  │
    │  ┌─────────┐                  ┌─────────┐                ┌─────────┐                   │  │
    │  │ ┌─┐ ┌─┐ │                  │ ↗ ↗ ↗ ↗ │                │ ┌ ┬ ┌ ┬ │                   │  │
    │  │ │ │ │ │ │ ───────────────→ │    Detect│  ───────────→ │ │ │ │ │ │  ← Recovered     │  │
    │  │ └─┘ └─┘ │                  │   Edges  │                │ └ ┴ └ ┴ │      Clock         │  │
    │  └─────────┘                  └─────────┘                └─────────┘                   │  │
    │                                                                                         │  │
    │  → Every bit has a transition → Easy to extract clock                                   │  │
    │  → PLL (Phase-Locked Loop) locks to edge frequency                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Comparison with Manchester (also has transitions every bit):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • RZ:         Transition in middle of bit, then returns to 0                            │  │
    │  • Manchester: Transition in middle of bit, direction indicates 0/1                      │  │
    │                                                                                         │  │
    │  Advantage of RZ over Manchester:                                                        │  │
    │  - Simpler decoding (no need to detect transition direction)                              │  │
    │  - Better for optical communication (ON-OFF keying)                                       │  │
    │                                                                                         │  │
    │  Disadvantage of RZ vs Manchester:                                                        │  │
    │  - DC component (Unipolar RZ)                                                             │  │
    │  - No inherent error detection (Manchester has parity-like property)                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 라인 부호화 비교

| 부호화 | 대역폭 | DC 성분 | 동기화 | 복잡도 | 주요 용도 |
|--------|--------|---------|--------|--------|-----------|
| **NRZ-L** | B | 있음 | 나쁨 | 낮음 | 간단 링크 |
| **NRZ-I** | B | 없음 | 나쁨 | 낮음 | USB |
| **RZ** | 2B | 있음/없음 | 좋음 | 중간 | 광통신 |
| **Manchester** | 2B | 없음 | 좋음 | 중간 | 이더넷 |
| **AMI** | B | 없음 | 나쁨 | 중간 | T1/E1 |
| **MLT-3** | B/2 | 없음 | 나쁨 | 중간 | Fast Ethernet |

### RZ 응용 분야

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RZ Applications                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Optical Communication (광통신):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Simple ON-OFF Keying (OOK):                                                          │  │
    │    - 1: Light ON for half bit period, then OFF                                          │  │
    │    - 0: Light OFF                                                                       │  │
    │  • Advantages:                                                                          │  │
    │    - Easy to generate (LED/Laser driver)                                                 │  │
    │    - Easy clock recovery (guaranteed transition for each 1)                              │  │
    │  • Used in: Fiber optics, infrared communication                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Magnetic Recording (자기 기록):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • RZ variants used in early disk drives                                                 │  │
    │  • FM (Frequency Modulation): Clock + Data combined                                       │  │
    │  • MFM (Modified FM): Higher density                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Digital Sampling Oscilloscopes:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • RZ signals easier to trigger on edges                                                 │  │
    │  • Clear bit boundaries for analysis                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 광통신 시스템 설계
**상황**: 1Gbps 광섬유 링크
**판단**: RZ vs Manchester vs NRZ

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Optical Link Line Coding Selection                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    • 1 Gbps data rate over single-mode fiber
    • Low-cost transceiver (LED, not laser)
    • 5 km distance

    Analysis:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  NRZ:                                                                                   │  │
    │  • Bandwidth: 1 GHz                                                                     │  │
    │  • Problem: Long 1s or 0s → Clock drift at receiver                                     │  │
    │  • Requires scrambling (e.g., 8B/10B) to ensure transitions                               │  │
    │                                                                                         │  │
    │  Manchester:                                                                             │  │
    │  • Bandwidth: 2 GHz                                                                     │  │
    │  • Problem: LED cannot support 2 GHz modulation                                          │  │
    │  • Requires expensive laser transmitter                                                  │  │
    │                                                                                         │  │
    │  RZ (Unipolar):                                                                          │  │
    │  • Bandwidth: 2 GHz (theoretically)                                                      │  │
    │  • Practical: Since light is ON for only half the bit period,                           │  │
    │              usable bandwidth ~1.5x NRZ                                                  │  │
    │  • Advantage: Guaranteed transitions for clock recovery                                  │  │
    │  • LED can achieve ~1.5 GHz (pulse shaping)                                              │  │
    │                                                                                         │  │
    │  Decision: Use RZ with 4B/5B or 8B/10B scrambling                                       │  │
    │  → Balances cost (LED-based) and reliability (clock recovery)                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### RZ 변형 기술

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Advanced RZ Variants                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. CS-RZ (Carrier-Suppressed RZ):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Adjacent bits have opposite phase (0°, 180°)                                         │  │
    │  • Reduces carrier component → Better spectral efficiency                               │  │
    │  • Used in: Long-haul optical communication                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. RZ-DPSK (Differential Phase Shift Keying with RZ):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Combines RZ pulse shape with DPSK modulation                                         │  │
    │  • Better sensitivity (3 dB improvement)                                                 │  │
    │  • Used in: 40G/100G coherent optical systems                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. CRZ (Chirped RZ):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Frequency changes within pulse (chirp)                                               │  │
    │  • Compensates for dispersion in fiber                                                  │  │
    │  • Used in: Dispersion-managed links                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### RZ 부호화 기대 효과

| 애플리케이션 | 최적 방식 | 이유 |
|-------------|-----------|------|
| **광통신** | RZ (Unipolar) | OOK 간단, 동기화 용이 |
| **구리선** | Manchester | DC 없음, 오류 검출 |
| **고속 링크** | NRZ+Scrambling | 대역폭 효율 |
| **자기 기록** | RZ 변형 | 밀도 향상 |

### 모범 사례

1. **광통신**: OOK-RZ
2. **동기화**: PLL 설계
3. **스크램블링**: 8B/10B
4. **파형 정형**: Raised Cosine

### 미래 전망

1. **코히어런트**: QPSK-RZ
2. **멀티레벨**: PAM4-RZ
3. **DSP**: 기반 부호화
4. **실리콘 포토닉스**: 집적 광학

### ※ 참고 표준/가이드
- **ITU-T**: G.703 (PDH)
- **IEEE**: 802.3 (Ethernet)
- **Telcordia**: GR-253
- **Bellcore**: 광통신 표준

---

## 📌 관련 개념 맵

- [NRZ](./35_encoding.md) - 기본 부호화
- [Manchester](./37_manchester.md) - 이더넷 방식
- [4B/5B](./42_block_coding.md) - 블록 부호
- [변조](../2_modulation/45_ask.md) - RF 변조
