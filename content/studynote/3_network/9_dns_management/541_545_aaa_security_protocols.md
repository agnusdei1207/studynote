+++
title = "541-545. 네트워크 보안 인증 (AAA, RADIUS, TACACS+, Kerberos)"
description = "네트워크 접근 제어를 위한 AAA 체계와 인증 프로토콜 RADIUS, TACACS+, 그리고 티켓 기반 인증 Kerberos 분석"
date = 2026-03-14
[extra]
subject = "NW"
category = "DNS & Management"
id = 541
+++

# 541-545. 네트워크 보안 인증 (AAA, RADIUS, TACACS+, Kerberos)

> **핵심 인사이트**: 누구나 네트워크 장비에 접속하게 둘 수는 없다. '누구인지(Authentication)', '무엇을 할 수 있는지(Authorization)', '무엇을 했는지(Accounting)'를 꼼꼼히 따지는 AAA 체계가 필수적이다. 이를 실현하기 위해 RADIUS와 TACACS+ 같은 전용 인증 서버가 경비원 역할을 수행한다.

---

## Ⅰ. AAA 보안 모델
1. **Authentication (인증)**: "당신은 누구입니까?" (ID/PW 확인)
2. **Authorization (인가)**: "당신은 무엇을 할 수 있습니까?" (명령어 권한 부여)
3. **Accounting (계정 관리)**: "당신은 무엇을 했습니까?" (접속 기록, 명령어 실행 로그 수집)

---

## Ⅱ. AAA 프로토콜 비교 (RADIUS vs TACACS+)

### 1. RADIUS (Remote Authentication Dial-In User Service)
* **특징**: UDP (1812, 1813) 사용. **개방형 표준**.
* **보안**: **패스워드만 암호화**하고 나머지는 평문입니다.
* **구조**: 인증(Auth)과 인가(Author)가 하나로 묶여 있습니다.
* **용도**: 일반적인 사용자 네트워크 접속 인증 (Wi-Fi, VPN 등).

### 2. TACACS+ (Terminal Access Controller Access Control System Plus)
* **특징**: TCP (49) 사용. **시스코(Cisco) 전용**.
* **보안**: **패킷 전체를 암호화**합니다.
* **구조**: 인증, 인가, 계정 관리가 완전히 분리되어 세밀한 제어가 가능합니다.
* **용도**: 라우터/스위치 관리자의 장비 접속 및 명령어 제어.

---

## Ⅲ. 커버로스 (Kerberos) 인증
신뢰할 수 있는 제3자 기관(KDC)을 통해 '티켓'을 발행받아 인증하는 방식입니다. (윈도우 AD의 기본 인증 방식)

* **구성 요소**: 
  - **AS (Authentication Service)**: 최초 인증.
  - **TGS (Ticket Granting Service)**: 서비스 이용 티켓 발급.
  - **KDC**: AS와 TGS를 포함하는 중앙 서버.
* **특징**: 암호화된 티켓을 사용하므로 패스워드가 네트워크에 흐르지 않으며, **타임스탬프**를 포함하여 재전송 공격(Replay Attack)을 방지합니다.

---

## Ⅳ. 기타 중앙 관리 프로토콜
* **LDAP (Lightweight Directory Access Protocol)**: 네트워크상의 자원(사용자, 장치 등) 정보를 중앙에서 조회하고 관리하기 위한 가벼운 프로토콜입니다.

---

## Ⅴ. 개념 맵 및 요약

```ascii
[AAA 인증 서버 동작 구조]

  [ 관리자 ] ───(접속 시도)───> [ 라우터/스위치 ] ───(인증 요청)───> [ AAA 서버 ]
                                                               (RADIUS/TACACS+)
                                <──(권한 승인)───  (ID/PW 확인)
```

📢 **섹션 요약 비유**: **AAA**는 건물의 보안 시스템입니다. **인증**은 출입증 확인, **인가**는 사장님 방은 못 들어가게 막는 권한 등급, **계정 관리**는 CCTV로 이동 동선을 기록하는 것입니다. **RADIUS**는 아파트 공동 현관문 비번을 누르는 대중적인 방식이고, **TACACS+**는 청와대 경호실처럼 누가 어떤 행동(명령어)을 하는지 일일이 감시하고 허락하는 고강도 보안 방식입니다. **커버로스**는 놀이공원에서 자유이용권(티켓) 하나로 모든 기구를 타는 '티켓형 시스템'입니다.
