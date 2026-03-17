+++
title = "VulnABLE CTF [LUXORA] Write-up: Reversing Chain 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Reverse Engineering", "Bronze", "Binary Patching", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Reversing Chain 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Reversing Chain)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/reverse/bronze`
- **목표**: 다운로드로 제공되는 간단한 리눅스 ELF 바이너리 파일(예: `keygen.elf`)을 리버스 엔지니어링하여, 입력된 라이선스 키를 검증하는 로직을 무력화(Patching)하고, 어떤 키를 입력하든 "정품(Valid)"으로 인식하게 만들어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 바이너리 분석 (Reconnaissance)

`/reverse/bronze` 페이지에서 `keygen.elf` 파일을 다운로드합니다. 이 프로그램은 실행 시 시리얼 키(Serial Key)를 묻고, 키가 맞으면 내부의 플래그를 출력해 주는 구조입니다.

**[실행 및 기본 분석]**
```bash
$ chmod +x keygen.elf
$ ./keygen.elf
Enter License Key: 1234
Invalid Key. Try again.
```

바이너리의 기본 정보를 확인하기 위해 `file` 과 `strings` 명령어를 사용합니다.
```bash
$ file keygen.elf
keygen.elf: ELF 64-bit LSB executable, x86-64, dynamically linked...
$ strings keygen.elf
Enter License Key:
Invalid Key. Try again.
Valid Key! Here is your flag:
FLAG{REVERSE_🥉_BASIC_PATCHING_A1B2C3}  <-- 운 좋게 strings 명령어로 플래그가 보일 수도 있지만, 
                                            여기서는 암호화되어 안 보인다고 가정합니다.
```

---

## 💥 2. 취약점 식별 및 디스어셈블 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Binary ] --(Hex Edit: JZ -> NOP)--> [ Patched Binary ]
                                      |-- Always Validates License
```


목표는 프로그램이 "Invalid Key" 분기로 빠지는 강제로 "Valid Key" 분기로 가도록 기계어 코드를 패치(Patch)하는 것입니다.

### 💡 디스어셈블리 도구 활용 (Ghidra, IDA, Radare2, objdump)
가장 간단한 `objdump` 를 이용해 어셈블리 코드를 확인해 봅니다.

```bash
$ objdump -d -M intel keygen.elf | grep -A 20 "<main>:"
```

**[어셈블리 코드 분석]**
```nasm
00000000004011a0 <main>:
...
  4011bd: e8 5e fe ff ff          call   401020 <check_key>  ; 키 검증 함수 호출
  4011c2: 85 c0                   test   eax,eax             ; 반환값 검사 (eax가 0인지)
  4011c4: 74 12                   je     4011d8 <main+0x38>  ; eax가 0이면(틀리면) 4011d8 로 점프!
  4011c6: 48 8d 3d 47 0e 00 00    lea    rdi,[rip+0xe47]     ; "Valid Key!" 문자열 출력 준비
  4011cd: e8 3e fe ff ff          call   401010 <puts@plt>
...
  4011d8: 48 8d 3d 4f 0e 00 00    lea    rdi,[rip+0xe4f]     ; "Invalid Key" 문자열 출력 준비
  4011df: e8 2c fe ff ff          call   401010 <puts@plt>
```

**[해커의 사고 과정]**
1. `4011bd` 에서 `check_key` 함수를 부르고 결과를 `eax` 에 담는다.
2. `4011c4` 의 `je 4011d8` 명령어가 핵심이다. 키가 틀렸을 때(Jump if Equal) 실패 화면으로 점프한다.
3. 이 `je (74 12)` 명령어를 **"아무것도 하지 않음(NOP, 90)"** 으로 덮어쓰거나, 아예 점프하지 않는 조건으로 바꿔버리면 어떻게 될까?

---

## 🚀 3. 공격 수행 및 바이너리 패치

헥스 에디터(Hex Editor, 예: `hexedit`, `ghex`)를 열어 `74 12` 바이트를 `90 90` (NOP)으로 수정합니다.

### 💡 바이너리 패치 (Hex Editing)
1. `hexedit keygen.elf` 실행
2. `0x4011c4` 주변 오프셋을 찾아 `74 12` 값을 `90 90` 으로 덮어씁니다.
3. 저장하고 나옵니다.

이제 패치된 프로그램을 다시 실행해 봅니다.

```bash
$ ./keygen.elf
Enter License Key: aaaa
Valid Key! Here is your flag: FLAG{REVERSE_🥉_BASIC_PATCHING_A1B2C3}
```

조건 분기(Jump) 문이 사라졌기 때문에, 무슨 키를 입력하든 프로그램은 위에서부터 아래로 흘러내려가며 "Valid Key!"를 출력하고 숨겨진 코드를 복호화하여 보여줍니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

소프트웨어의 무결성 검증이 클라이언트(로컬 실행 파일) 단에서만 이루어질 때, 기계어 코드를 직접 조작(Binary Patching)하여 모든 보호 메커니즘을 뚫어낼 수 있음을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{REVERSE_🥉_BASIC_PATCHING_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
소프트웨어를 컴파일하여 배포할 때, 리버스 엔지니어링에 대한 방어 로직(Anti-Reversing, Anti-Debugging, Code Obfuscation)이 전혀 없었기 때문입니다.

* **안전한 패치 가이드 (난독화 및 서버 검증)**
1. **서버 사이드 검증 (가장 확실함)**: 중요한 라이선스 키 검증 로직은 로컬 실행 파일 안에서 처리하면 안 됩니다. 반드시 인터넷을 통해 중앙 서버의 API로 키를 전송하고 검증 결과를 받아야 합니다.
2. **코드 난독화 (Code Obfuscation) 및 패킹 (Packing)**: `UPX`, `Themida` 같은 패커나 OLLVM 기반의 난독화 도구를 사용하여, 해커가 디스어셈블리(IDA)를 열었을 때 `test`, `je` 같은 직관적인 흐름을 볼 수 없게 코드를 꼬아놓아야 합니다.
3. **무결성 검사 (Integrity Check / Anti-Patching)**: 프로그램이 실행될 때 자기 자신의 해시(MD5/SHA256)를 검사하여, 단 1바이트라도 변경된(Patch) 흔적이 있다면 아예 실행되지 않고 종료되도록 하는 방어 코드를 추가해야 합니다.