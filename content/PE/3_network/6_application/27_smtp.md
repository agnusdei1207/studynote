+++
title = "27. SMTP (Simple Mail Transfer Protocol)"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["SMTP", "Email", "MIME", "SPF", "DKIM", "DMARC"]
draft = false
+++

# SMTP (Simple Mail Transfer Protocol)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SMTP는 **"이메일 **전송 **전용 **프로토콜"**로, **TCP 587포트**(Submission) 또는 **25포트**(Relay)를 **사용**하고 **Text-Based**(명령어-응답) **구조**로 **ASCII** **코드**만 **전송**하며 **MIME**(Multipurpose Internet Mail Extensions)로 **이진 파일**을 **처리**한다.
> 2. **구조**: **MAIL FROM**(발신자), **RCPT TO**(수신자), **DATA**(본문) **명령어**로 **전송**하며 **EHLO**(Extended Hello)로 **기능 **협상**하고 **STARTTLS**로 **TLS **암호화**를 **시작**하며 **Authentication**(SMTP AUTH)으로 **사용자**를 **인증**한다.
> 3. **보안**: **SPF**(Sender Policy Framework), **DKIM**(DomainKeys Identified Mail), **DMARC**(Domain-based Message Authentication)로 **스팸 **및 **피싱**을 **방지**하며 **25번 포트**는 **Relay**용으로 **제한**하고 **587번**(Submission) 또는 **465번**(SMTPS)을 **사용**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
SMTP는 **"이메일 전송 프로토콜"**이다.

**SMTP 특징**:
- **Push Model**: 발신자가 서버로 전송
- **Text-Based**: 명령어-응답 구조
- **Store-and-Forward**: 중계 서버 경유
- **TCP Only**: 신뢰성 필요

### 💡 비유
SMTP는 **"우편 배달 시스템"**과 같다.
- **편지**: 이메일
- **우체국**: 메일 서버
- **주소**: 이메일 주소
- **배달**: 전송

---

## Ⅱ. 아키텍처 및 핵심 원리

### SMTP 세션

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         SMTP Session                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Client (Port 587)                             SMTP Server                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  S: 220 smtp.example.com ESMTP Postfix                                               │  │  │
    │  │  C: EHLO client.example.com                                                          │  │  │
    │  │  S: 250-smtp.example.com                                                             │  │  │
    │  │  S: 250-PIPELINING                                                                   │  │  │
    │  │  S: 250-SIZE 10240000                                                                │  │  │
    │  │  S: 250-STARTTLS                                                                     │  │  │
    │  │  S: 250-AUTH PLAIN LOGIN                                                             │  │  │
    │  │  C: STARTTLS                                                                         │  │  │
    │  │  S: 220 Ready to start TLS                                                           │  │  │
    │  │  [TLS Handshake]                                                                     │  │  │
    │  │  C: EHLO client.example.com                                                          │  │  │
    │  │  C: AUTH PLAIN base64credentials                                                     │  │  │
    │  │  S: 235 Authentication successful                                                     │  │  │
    │  │  C: MAIL FROM:<sender@example.com>                                                   │  │  │
    │  │  S: 250 2.1.0 Ok                                                                     │  │  │
    │  │  C: RCPT TO:<recipient@example.com>                                                  │  │  │
    │  │  S: 250 2.1.5 Ok                                                                     │  │  │
    │  │  C: DATA                                                                             │  │  │
    │  │  S: 354 End data with <CR><LF>.<CR><LF>                                              │  │  │
    │  │  C: Subject: Test Email                                                              │  │  │
    │  │  C: From: sender@example.com                                                         │  │  │
    │  │  C: To: recipient@example.com                                                        │  │  │
    │  │  C:                                                                                  │  │  │
    │  │  C: This is a test email.                                                            │  │  │
    │  │  C: .                                                                                │  │  │
    │  │  S: 250 2.0.0 Ok: queued as ABC123                                                   │  │  │
    │  │  C: QUIT                                                                             │  │  │
    │  │  S: 221 2.0.0 Bye                                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 이메일 전송 흐름

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Email Delivery Flow                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Sender                          MTA                          MTA                        │  │
    │  (SMTP)        →                 (Relay)       →               (Delivery)                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. SMTP Submission (Port 587)                                                       │  │  │
    │  │     sender@example.com → smtp.example.com                                           │  │  │
    │  │                                                                                      │  │  │
    │  │  2. MX Lookup (DNS)                                                                  │  │  │
    │  │     recipient@example.com → mx.recipient.com (Priority 10)                          │  │  │
    │  │                                                                                      │  │  │
    │  │  3. SMTP Relay (Port 25)                                                              │  │  │
    │  │     smtp.example.com → mx.recipient.com                                             │  │  │
    │  │                                                                                      │  │  │
    │  │  4. Local Delivery                                                                   │  │  │
    │  │     mx.recipient.com → /var/mail/recipient                                          │  │  │
    │  │                                                                                      │  │  │
    │  │  5. POP3/IMAP4 Retrieval (Port 110/993, 143/995)                                    │  │  │
    │  │     Recipient → MUA                                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### SMTP 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| **EHLO** | Extended Hello | `EHLO client.example.com` |
| **MAIL FROM** | 발신자 지정 | `MAIL FROM:<sender@example.com>` |
| **RCPT TO** | 수신자 지정 | `RCPT TO:<recipient@example.com>` |
| **DATA** | 본문 시작 | `DATA` |
| **RSET** | 세션 초기화 | `RSET` |
| **VRFY** | 주소 확인 (비권장) | `VRFY user@example.com` |
| **QUIT** | 세션 종료 | `QUIT` |

### 응답 코드

| 코드 | 의미 | 예시 |
|------|------|------|
| **220** | 서비스 준비 | `220 smtp.example.com` |
| **250** | 요청 성공 | `250 2.1.0 Ok` |
| **354** | MAIL 입력 시작 | `354 End data with <CR><LF>.<CR><LF>` |
| **421** | 서비스 불가 | `421 4.4.2 Timeout` |
| **450** | 사서함 사용중 | `450 4.2.1 Mailbox busy` |
| **550** | 요청 거부 | `550 5.1.1 User unknown` |

### 포트 비교

| 포트 | 용도 | 암호화 |
|------|------|--------|
| **25** | MTA-to-MTA Relay | Optional (STARTTLS) |
| **465** | SMTPS (Deprecated) | Mandatory (TLS) |
| **587** | Submission | Optional (STARTTLS) |
| **2525** | Alternative | Optional |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 이메일 보안 (SPF, DKIM, DMARC)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Email Security Layers                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. SPF (Sender Policy Framework)                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  example.com TXT:                                                                   │  │  │
    │  │  "v=spf1 mx ip4:192.0.2.0/24 include:_spf.google.com ~all"                          │  │  │
    │  │  → 192.0.2.0/24에서 발송만 허용                                                      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. DKIM (DomainKeys Identified Mail)                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  selector._domainkey.example.com TXT:                                                │  │  │
    │  │  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCB..."                             │  │  │
    │  │  → 개인키로 서명, 공개키로 검증                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. DMARC (Domain-based Message Authentication)                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  _dmarc.example.com TXT:                                                            │  │  │
    │  │  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"                                  │  │  │
    │  │  → SPF+DKIM 실패 시 거부 (reject)                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: SMTP 서버 구성
**상황**: 이메일 발송
**판단**:

```bash
# Postfix 설정 (/etc/postfix/main.cf)
smtpd_tls_cert_file=/etc/ssl/certs/smtpd.crt
smtpd_tls_key_file=/etc/ssl/private/smtpd.key
smtpd_use_tls=yes
smtpd_tls_auth_only=yes
smtpd_sasl_auth_enable=yes
smtpd_recipient_restrictions =
    permit_sasl_authenticated,
    permit_mynetworks,
    reject_unauth_destination

# SPF 레코드 확인
dig txt example.com +short

# DMARC 확인
dig txt _dmarc.example.com +short
```

---

## Ⅴ. 기대효과 및 결론

### SMTP 기대 효과

| 효과 | 없음 | SMTP |
|------|------|------|
| **비동기 전송** | 불가 | 가능 |
| **중계** | 직접 전송 | Store-and-Forward |
| **보안** | 없음 | SPF/DKIM/DMARC |

### 모범 사례

1. **TLS**: STARTTLS 필수
2. **인증**: SMTP AUTH 강제
3. **Rate Limiting**: 스팸 방지
4. **DKIM**: 모든 발신 서명

### 미래 전망

1. **MTA-STS**: TLS 강제화
2. **SMTP TLS Reporting**: 암호화 모니터링
3. **ARC**: Forwarding 서명

### ※ 참고 표준/가이드
- **RFC 5321**: SMTP
- **RFC 7208**: SPF
- **RFC 6376**: DKIM
- **RFC 7489**: DMARC

---

## 📌 관련 개념 맵

- [MIME](./5_application/26_mime.md) - 이메일 인코딩
- [POP3/IMAP](./6_application/28_pop3_imap.md) - 이메일 수신
- [DNS](./2_dns/2_dns_overview.md) - MX 레코드
