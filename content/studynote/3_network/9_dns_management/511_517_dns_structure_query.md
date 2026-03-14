+++
title = "511-517. DNS(Domain Name System)의 구조와 질의"
description = "전 세계 호스트 이름을 IP 주소로 변환하는 DNS의 계층적 구조와 재귀적/반복적 질의 방식 분석"
date = 2026-03-14
[extra]
subject = "NW"
category = "DNS & Management"
id = 511
+++

# 511-517. DNS(Domain Name System)의 구조와 질의

> **핵심 인사이트**: DNS는 인터넷의 거대한 '전화번호부'이자 분산 데이터베이스다. 수십억 개의 이름을 관리하기 위해 뿌리(Root)부터 끝단까지 계층적으로 역할을 나누며, 한 번 찾은 주소는 캐시에 저장하여 전 세계적인 트래픽 폭주를 막아낸다.

---

## Ⅰ. DNS의 계층적 분산 구조
도메인 이름은 오른쪽에서 왼쪽으로 갈수록 하위 계층이 됩니다.

1. **Root Domain ( . )**: 가장 꼭대기. 전 세계에 13개의 논리적 루트 서버군이 존재합니다.
2. **TLD (Top-Level Domain)**: 국가 코드(.kr, .jp)나 범용 목적(.com, .net, .org)을 나타냅니다.
3. **SLD (Second-Level Domain)**: 실제 조직이나 서비스의 이름입니다. (google, naver 등)
4. **Subdomain**: 조직 내부의 서비스 구분입니다. (www, mail, blog 등)

---

## Ⅱ. DNS 질의(Query) 방식

### 1. 재귀적 질의 (Recursive Query)
* **방식**: 클라이언트가 로컬 DNS 서버(통신사 DNS 등)에게 "주소 찾아와!"라고 맡기면, 로컬 DNS 서버가 책임지고 끝까지 알아내어 최종 답변을 주는 방식입니다.

### 2. 반복적 질의 (Iterative Query)
* **방식**: 로컬 DNS 서버가 Root 서버부터 차례대로 물어보는 과정입니다. "혹시 google.com 알아?" $\rightarrow$ "난 몰라, .com 담당자한테 물어봐" $\rightarrow$ "난 몰라, google 담당자한테 물어봐" 순으로 핑퐁하며 찾아나갑니다.

---

## Ⅲ. 주요 DNS 레코드 (Resource Record)
DNS 서버가 저장하고 있는 데이터 조각들입니다.
* **A (Address)**: 도메인 이름을 **IPv4** 주소로 매핑.
* **AAAA**: 도메인 이름을 **IPv6** 주소로 매핑.
* **CNAME (Canonical Name)**: 별칭. 도메인 주소를 다른 도메인 주소로 연결.
* **MX (Mail Exchanger)**: 해당 도메인의 이메일을 수신할 서버 정보.
* **NS (Name Server)**: 해당 도메인을 관리하는 권한 있는 네임서버 주소.
* **SOA (Start of Authority)**: 존(Zone) 파일의 기준 정보 (버전, 만료 시간 등).

---

## Ⅳ. DNS 포트와 전송 방식
* **UDP 포트 53**: 일반적인 이름 조회(Query) 시 사용합니다. 빠르고 가볍습니다.
* **TCP 포트 53**: 
  - 응답 데이터가 512바이트를 넘을 때 (Truncation 발생 시).
  - 네임서버끼리 데이터를 동기화할 때 (**Zone Transfer**).

---

## Ⅴ. 개념 맵 및 요약

```ascii
[DNS 이름 풀이 과정]

 [ User ] --(1. google.com 어딨어?)--> [ Local DNS ] 
                                            │
    ┌────────────────(2. 반복적 질의)──────────┤
    │                                       │
    ▼                                       ▼
 [ Root Server ] <─(모르니 .com 가봐)── [ .com TLD Server ]
                                            │
    ┌───────────────────────────────────────┘
    ▼
 [ google.com NS ] ──(응, IP 1.2.3.4 야)──> [ Local DNS ] ──(자, 여기!)──> [ User ]
```

📢 **섹션 요약 비유**: **DNS**는 114 안내 서비스와 같습니다. **Root**는 "서울(02)은 저기로 전화하세요"라고 알려주는 통합 센터이고, **TLD**는 "강남구는 이쪽입니다"라고 안내하는 구청입니다. **A 레코드**는 이름으로 번호를 찾는 정방향 서비스이고, **PTR 레코드(역방향)**는 번호로 이름을 거꾸로 찾는 발신자 추적 서비스입니다.
