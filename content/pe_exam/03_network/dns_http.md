+++
title = "DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)"
date = 2026-03-02

[extra]
categories = "pe_exam-network"
+++

# DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)

## 핵심 인사이트 (3줄 요약)
> **DNS는 도메인을 IP로 변환하는 인터넷 전화번호부**. HTTP는 비연결·무상태 텍스트 프로토콜이며, HTTPS는 TLS/SSL 암호화를 추가한 보안 버전. HTTP/2·HTTP/3로 성능이 지속적으로 개선된다.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)의 개념과 핵심 기술 요소를 설명하고, 관련 프로토콜·기술과 비교하여 실무 적용 방안을 논하시오."**

---

### Ⅰ. 개요

**DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)**란 [핵심 정의]이다.

- **등장 배경**: 기존 기술의 한계 → DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS) 도입의 필요성
- **핵심 목적**: 성능 향상 / 비용 절감 / 보안 강화

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 1. DNS (Domain Name System)
### 개념
인간 친화적 도메인 이름(www.example.com)을 기계 친화적 IP 주소(93.184.216.34)로 변환하는 분산 데이터베이스 시스템.

> 비유: "전화번호부" - 이름(도메인)으로 번호(IP) 찾기

### DNS 계층 구조
```
www.example.com 조회 과정:

①사용자 → 로컬 DNS (캐시 확인)
②MISS → Root DNS (. 루트)
           ↓
③ com DNS 서버 (TLD: Top Level Domain)
           ↓
④ example.com DNS (권한 있는 네임서버)
           ↓
⑤ www.example.com → 93.184.216.34 반환
           ↓
⑥ 로컬 DNS 캐시 저장 (TTL 동안)
           ↓
⑦ 사용자에게 IP 응답

총 소요: 수십 ms (캐시 히트 시 즉시)
```

### DNS 레코드 유형
| 레코드 | 설명 | 예시 |
|--------|------|------|
| A | 도메인 → IPv4 | example.com → 93.184.216.34 |
| AAAA | 도메인 → IPv6 | example.com → 2606:2800::1 |
| CNAME | 도메인 → 도메인(별칭) | www → example.com |
| MX | 메일 서버 | mail.example.com |
| NS | 네임서버 지정 | ns1.example.com |
| TXT | 텍스트 정보 | SPF, DKIM 인증 |
| PTR | IP → 도메인 (역방향) | 34.216.184.93.in-addr.arpa |

### DNS 보안 문제
```
DNS 스푸핑(캐시 포이즈닝):
- 가짜 DNS 응답 주입 → 사용자를 악성 사이트로

DNSSEC (DNS Security Extensions):
- DNS 응답에 디지털 서명 추가
- 공개키로 응답 무결성 검증
```

---

#### 2. HTTP/HTTPS
### HTTP 특성
```
비연결성 (Connectionless):
- 요청-응답 후 연결 끊음
- Keep-Alive 옵션으로 연결 재사용 가능

무상태성 (Stateless):
- 각 요청은 독립적 (이전 요청 기억 X)
- 쿠키, 세션으로 상태 유지
```

### HTTP 메서드
| 메서드 | 의미 | 멱등성 | 안전성 |
|--------|------|--------|--------|
| GET | 리소스 조회 | O | O |
| POST | 리소스 생성/처리 | X | X |
| PUT | 리소스 전체 수정 | O | X |
| PATCH | 리소스 부분 수정 | X | X |
| DELETE | 리소스 삭제 | O | X |
| HEAD | 헤더만 조회 | O | O |
| OPTIONS | 지원 메서드 확인 | O | O |

### HTTP 상태 코드
```
1xx: 정보 (처리 중)
2xx: 성공
  200 OK, 201 Created, 204 No Content
3xx: 리다이렉션
  301 Moved Permanently, 302 Found, 304 Not Modified
4xx: 클라이언트 오류
  400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests
5xx: 서버 오류
  500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable
```

### HTTPS = HTTP + TLS

```
TLS 핸드셰이크 과정:

클라이언트                                서버
   │─── ClientHello (지원 암호 목록) ───────►│
   │◄── ServerHello (선택된 암호 + 인증서) ──│
   │─── 서버 인증서 검증 (CA 서명 확인) ────►│
   │─── PreMasterSecret (공개키로 암호화) ──►│
   │       [세션 키 생성]                    │
   │─── Finished ────────────────────────►│
   │◄── Finished ────────────────────────│
   │                                        │
   │═══════════════ 암호화 통신 시작 ════════│

TLS 1.3 개선:
- 0-RTT 재연결 (기존 세션 즉시 재사용)
- 1-RTT 핸드셰이크 (기존 2-RTT)
- 안전하지 않은 알고리즘 제거 (RSA 키 교환 등)
```

### HTTP 버전 비교

| 특성 | HTTP/1.0 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|----------|--------|--------|
| 연결 | 매 요청 재연결 | Keep-Alive | 다중화 | QUIC |
| 헤더 | 텍스트 | 텍스트 | 바이너리+압축 | 바이너리 |
| 전송 | 순차 | 파이프라이닝 | 멀티플렉싱 | QUIC 스트림 |
| HOL 블록 | O | O | TCP에서 O | 해결 |
| 프로토콜 | TCP | TCP | TCP | UDP(QUIC) |
| 서버 푸시 | X | X | O | O |

```
HOL (Head-of-Line) 블로킹:
- TCP는 패킷 순서 보장 → 앞 패킷 손실 시 뒤 패킷 대기
- HTTP/2: TCP HOL은 있음 (다중화해도 TCP 레벨에서 블로킹)
- HTTP/3(QUIC): UDP 기반, 스트림별 독립 → HOL 완전 해결
```

---

### Ⅲ. 기술 비교 분석

#### 3. 쿠키 vs 세션 vs JWT
| 항목 | 쿠키 | 세션 | JWT |
|------|------|------|-----|
| 저장 위치 | 클라이언트 | 서버 | 클라이언트 |
| 보안 | 낮음 | 높음 | 중간 (서명) |
| 서버 부하 | 없음 | 메모리/DB | 없음 |
| 확장성 | 좋음 | 세션 공유 필요 | 좋음 |
| 만료 | 설정 가능 | 서버 제어 | 토큰에 포함 |
| 사용 | 자동 로그인 | 로그인 상태 | API 인증 |

---

### Ⅳ. 실무 적용 방안

#### 4. 실무에선? (기술사적 판단)
- **DNS TTL**: 짧으면 유연하지만 부하 증가
- **HTTPS 의무화**: 구글 SEO 페널티, 현대 표준
- **인증서 관리**: Let's Encrypt (무료 자동 갱신)
- **HTTP/2**: 멀티플렉싱으로 병렬 리소스 로딩
- **HTTP/3**: 모바일/고손실 환경에서 유리

---

### Ⅴ. 기대 효과 및 결론


| 효과 영역 | 내용 | 정량적 목표 |
|---------|-----|-----------|
| **통신 성능** | 최적화된 프로토콜·라우팅으로 지연 및 패킷 손실 감소 | 네트워크 지연 50% 단축 |
| **확장성** | 소프트웨어 정의 방식으로 트래픽 급증에도 유연 대응 | 대역폭 활용률 80% 이상 |
| **보안·안정성** | 계층적 보안 아키텍처로 가용성 및 무결성 보장 | SLA 99.99% (4-nine) 달성 |

#### 결론
> **DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)**은(는) 네트워크 기술은 5G·SDN·NFV를 통해 소프트웨어 중심으로 진화하고 있으며, AI 기반 자율 네트워크(Autonomous Network)가 차세대 통신 인프라의 핵심이 될 것이다.

> **※ 참고 표준**: RFC 표준 시리즈, ETSI NFV ISG, 3GPP TS 23.501, ITU-T 권고안

---

## 어린이를 위한 종합 설명

**DNS와 HTTP/HTTPS를 쉽게 이해해보자!**

> DNS는 도메인을 IP로 변환하는 인터넷 전화번호부. HTTP는 비연결·무상태 텍스트 프로토콜이며, HTTPS는 TLS/SSL 암호화를 추가한 보안 버전. HTTP/2·HT

```
왜 필요할까?
  핵심 목적: 성능 향상 / 비용 절감 / 보안 강화

어떻게 동작하나?
  복잡한 문제 → DNS와 HTTP/HTTPS 적용 → 더 빠르고 안전한 결과!

핵심 한 줄:
  DNS와 HTTP/HTTPS = 똑똑하게 문제를 해결하는 방법
```

> **비유**: DNS와 HTTP/HTTPS은 마치 요리사가 레시피를 따르는 것과 같아.
> 혼란스러운 재료들을 정해진 순서대로 조합하면 → 맛있는 요리(최적 결과)가 나오지! 🍳

---
