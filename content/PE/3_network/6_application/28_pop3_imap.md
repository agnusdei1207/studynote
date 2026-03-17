+++
title = "28. POP3/IMAP (Email Retrieval)"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["POP3", "IMAP", "Email", "TCP", "Mailbox"]
draft = false
+++

# POP3/IMAP (Email Retrieval)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **POP3**(Post Office Protocol v3)와 **IMAP**(Internet Message Access Protocol)는 **"이메일 **수신 **프로토콜"**로, **SMTP**(발송)와 **함께 **사용**되며 **TCP 110**(POP3) 또는 **993**(IMAPS) **포트**를 **사용**한다.
> 2. **차이**: **POP3**는 **서버**에서 **클라이언트**로 **메일**을 **다운로드**하고 **삭제**하는 **Store-and-Forward** **방식**이며 **IMAP**은 **서버**에 **메일**을 **유지**하고 **여러 **기기**에서 **동기화**하는 **Client-Server** **방식**이다.
> 3. **선택**: **단일 **기기** 사용은 **POP3**, **다중 **기기** **동기화**는 **IMAP**을 **사용**하며 **SSL/TLS** **암호화**(POP3S: 995, IMAPS: 993)를 **권장**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
POP3/IMAP는 **"이메일 수신 프로토콜"**이다.

**특징**:
- **POP3**: Download & Delete
- **IMAP**: Server-side Sync
- **Text-Based**: 명령어-응답 구조
- **Authentication**: USER/PASS or OAuth

### 💡 비유
- **POP3**: **"택배 **수령 ****(받으면 **원본 **없음)
- **IMAP**: **"사물함 **대여 ****(여러 곳에서 **확인)

---

## Ⅱ. 아키텍처 및 핵심 원리

### POP3 세션

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         POP3 Session                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Client (Port 110)                             POP3 Server                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  S: +OK POP3 server ready                                                            │  │  │
    │  │  C: USER user@example.com                                                            │  │  │
    │  │  S: +OK                                                                               │  │  │
    │  │  C: PASS password                                                                     │  │  │
    │  │  S: +OK Logged in                                                                    │  │  │
    │  │  C: STAT                                                                              │  │  │
    │  │  S: +OK 2 320 (2 messages, 320 octets)                                               │  │  │
    │  │  C: LIST                                                                              │  │  │
    │  │  S: +OK 2 messages:                                                                   │  │  │
    │  │  S: 1 120 (Message 1: 120 octets)                                                     │  │  │
    │  │  S: 2 200 (Message 2: 200 octets)                                                     │  │  │
    │  │  S: .                                                                                 │  │  │
    │  │  C: RETR 1                                                                            │  │  │
    │  │  S: +OK 120 octets                                                                    │  │  │
    │  │  S: [Email content...]                                                                │  │  │
    │  │  S: .                                                                                 │  │  │
    │  │  C: DELE 1                                                                            │  │  │
    │  │  S: +OK message 1 deleted                                                             │  │  │
    │  │  C: QUIT                                                                              │  │  │
    │  │  S: +OK dewey POP3 server signing off (maildrop empty)                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### IMAP 세션

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         IMAP Session                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Client (Port 143)                             IMAP Server                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  S: * OK IMAP4rev1 Server ready                                                       │  │  │
    │  │  C: A001 LOGIN user@example.com password                                              │  │  │
    │  │  S: A001 OK LOGIN completed                                                           │  │  │
    │  │  C: A002 LIST "" "*"                                                                  │  │  │
    │  │  S: * LIST (\HasNoChildren) "/" INBOX                                                │  │  │
    │  │  S: * LIST (\HasChildren) "/" Archive                                                │  │  │
    │  │  S: A002 OK LIST completed                                                            │  │  │
    │  │  C: A003 SELECT INBOX                                                                 │  │  │
    │  │  S: * 3 EXISTS                                                                        │  │  │
    │  │  S: * OK [UNSEEN 2]                                                                   │  │  │
    │  │  S: * FLAGS (\Answered \Flagged \Deleted \Seen \Draft)                               │  │  │
    │  │  S: A003 OK SELECT completed                                                           │  │  │
    │  │  C: A004 FETCH 1 BODY[]                                                               │  │  │
    │  │  S: * 1 FETCH (BODY[] {123}                                                           │  │  │
    │  │  S: [Email content...]                                                                │  │  │
    │  │  S: )                                                                                 │  │  │
    │  │  S: A004 OK FETCH completed                                                           │  │  │
    │  │  C: A005 STORE 1 +FLAGS \Seen                                                         │  │  │
    │  │  S: * 1 FETCH (FLAGS (\Seen))                                                         │  │  │
    │  │  S: A005 OK STORE completed                                                           │  │  │
    │  │  C: A006 LOGOUT                                                                       │  │  │
    │  │  S: * BYE IMAP4rev1 Server logging out                                                │  │  │
    │  │  S: A006 OK LOGOUT completed                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### POP3 vs IMAP

| 구분 | POP3 | IMAP |
|------|------|------|
| **저장** | 클라이언트 | 서버 |
| **동기화** | X | O |
| **폴더** | Inbox만 | 다중 |
| **읽음 상태** | 로컬 | 서버 |
| **오프라인** | O | 제한 |

### POP3 모드

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         POP3 Modes                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Delete Mode (Default):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Server                    Client                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  [MSG1, MSG2, MSG3]                                                                      │  │  │
    │  │      RETR 1 ─────────────────→ [MSG1 downloaded]                                       │  │  │
    │  │      DELE 1 ─────────────────→ [MSG1 marked for delete]                                │  │  │
    │  │      RETR 2 ─────────────────→ [MSG2 downloaded]                                       │  │  │
    │  │      DELE 2 ─────────────────→ [MSG2 marked for delete]                                │  │  │
    │  │      QUIT ──────────────────→ [MSG1, MSG2 deleted, MSG3 only]                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Keep Mode (UIDL):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Server                    Client                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  [MSG1(UID1), MSG2(UID2), MSG3(UID3)]                                                  │  │  │
    │  │      UIDL ─────────────────→ [Client records UIDs]                                    │  │  │
    │  │      RETR 1 ────────────────→ [MSG1 downloaded]                                       │  │  │
    │  │      (no DELE)                                                                        │  │  │
    │  │      QUIT ──────────────────→ [All messages kept]                                     │  │  │
    │  │      Next session: UIDL shows existing UIDs, download only new                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### IMAP 폴더 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         IMAP Folder Structure                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Server Mailbox                                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  INBOX                                                                               │  │  │
    │  │  ├── [MSG1: Unread]                                                                  │  │  │
    │  │  ├── [MSG2: Read, \Answered]                                                         │  │  │
    │  │  └── [MSG3: Unread]                                                                  │  │  │
    │  │                                                                                       │  │  │
    │  │  Archive/                                                                            │  │  │
    │  │  ├── 2025/                                                                           │  │  │
    │  │  │   ├── 01_January/                                                                 │  │  │
    │  │  │   │   ├── [MSG100]                                                                │  │  │
    │  │  │   │   └── [MSG101]                                                                │  │  │
    │  │  │   └── 02_February/                                                                │  │  │
    │  │  └── 2026/                                                                           │  │  │
    │  │                                                                                       │  │  │
    │  │  Sent/                                                                               │  │  │
    │  │  ├── [MSG50]                                                                         │  │  │
    │  │  └── [MSG51]                                                                         │  │  │
    │  │                                                                                       │  │  │
    │  │  Drafts/                                                                             │  │  │
    │  │  └── [MSG_DRAFT1]                                                                    │  │  │
    │  │                                                                                       │  │  │
    │  │  Trash/                                                                              │  │  │
    │  │  └── [MSG99: \Deleted]                                                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → All folders synced across devices (Phone, Tablet, Desktop)                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 포트 비교

| 프로토콜 | 평문 | 암호화 |
|----------|------|--------|
| **POP3** | 110 | 995 (POP3S) |
| **IMAP** | 143 | 993 (IMAPS) |

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 이메일 클라이언트 설정
**상황**: 다중 기기 사용
**판단**: IMAP 사용

```python
# IMAP 연결 (Python)
import imaplib
import ssl

# SSL 연결 (권장)
context = ssl.create_default_context()
mail = imaplib.IMAP4_SSL('imap.example.com', 993, ssl_context=context)

# 로그인
mail.login('user@example.com', 'password')

# 폴더 선택
mail.select('INBOX')

# 메일 검색
status, messages = mail.search(None, 'UNSEEN')
mail_ids = messages[0].split()

# 메일 가져오기
for mail_id in mail_ids:
    status, msg = mail.fetch(mail_id, '(BODY[])')
    # Process email

# 로그아웃
mail.close()
mail.logout()
```

```python
# POP3 연결 (Python)
import poplib
from poplib import POP3_SSL

# SSL 연결
pop3 = POP3_SSL('pop3.example.com', 995)

# 로그인
pop3.user('user@example.com')
pop3.pass_('password')

# 메일 목록
num_messages = len(pop3.list()[1])

# 메일 가져오기
for i in range(num_messages, 0, -1):
    response, msg, octets = pop3.retr(i)
    # Process email (번호별 역순)

# 종료
pop3.quit()
```

---

## Ⅴ. 기대효과 및 결론

### POP3/IMAP 기대 효과

| 효과 | POP3 | IMAP |
|------|------|------|
| **서버 공간** | 적음 | 큼 |
| **다중 기기** | 어려움 | 쉬움 |
| **오프라인** | 완전 | 제한 |
| **백업** | 사용자 | 서버 |

### 모범 사례

1. **기본**: IMAP (다중 기기)
2. **보안**: SSL/TLS 필수
3. **폴더**: IMAP (다중 폴더)
4. **POP3**: 단일 기기, 오프라인 우선

### 미래 전망

1. **JMAP**: JSON 기반 대체
2. **Push**: IMAP IDLE
3. **OAuth 2.0**: 암호 없는 인증

### ※ 참고 표준/가이드
- **RFC 1939**: POP3
- **RFC 3501**: IMAP4rev1
- **RFC 6180**: IMAP Extensions

---

## 📌 관련 개념 맵

- [SMTP](./27_smtp.md) - 이메일 발송
- [MIME](./5_application/26_mime.md) - 이메일 인코딩
- [DNS](./2_dns/2_dns_overview.md) - MX 레코드
