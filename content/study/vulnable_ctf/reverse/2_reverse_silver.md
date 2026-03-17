+++
title = "VulnABLE CTF [LUXORA] Write-up: Reversing Chain 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Reverse Engineering", "Silver", "Dynamic Debugging", "GDB", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Reversing Chain 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Reversing Chain)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/reverse/silver`
- **목표**: 안티 패칭(Anti-Patching) 기법이 적용되어 실행 파일을 직접 수정(Hex Edit)할 수 없는 바이너리(`secure_keygen.elf`)에 대해, **동적 디버거(GDB)**를 연결하여 메모리상의 분기문(Register)을 강제로 조작하고 인증을 우회하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/reverse/silver` 에서 제공하는 `secure_keygen.elf` 를 다운로드하여 실행해 봅니다.

**[실행 결과]**
```bash
$ ./secure_keygen.elf
Enter VIP License Key: AAAA
[Error] Verification failed.
```

Bronze에서 했던 것처럼 Hex Editor로 `je` 명령어를 `nop` 으로 패치한 뒤 실행해 봅니다.
```bash
$ ./secure_keygen_patched.elf
[Fatal] Binary integrity check failed! Exiting.
```
**[해커의 사고 과정]**
1. 파일이 변경되었는지 검사하는 자체 무결성 검증(MD5 Hash Check) 기능이 들어있다.
2. 하드디스크에 있는 파일을 물리적으로 고치는(Static Patching) 방식은 사용할 수 없다.
3. 그렇다면, 파일이 메모리에 로드된 후 CPU 위에서 실행되는 순간(Runtime)을 낚아채서, 프로그램의 뇌(Register) 상태를 거짓으로 꾸며보자. (Dynamic Debugging)

---

## 💥 2. 취약점 식별 및 동적 분석 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Binary ] --(Hex Edit: JZ -> NOP)--> [ Patched Binary ]
                                      |-- Always Validates License
```


`gdb` (GNU Debugger)를 사용하여 프로그램을 한 줄씩 실행시키면서(Tracing), 키 검증을 수행하는 함수 직후에 개입할 계획을 세웁니다.

### 💡 디스어셈블 및 중단점(Breakpoint) 설정
먼저 `objdump`나 `gdb` 내에서 검증 함수의 주소를 찾습니다.

```bash
$ gdb ./secure_keygen.elf
(gdb) set disassembly-flavor intel
(gdb) disassemble main
```

**[GDB 디스어셈블리 확인 (일부)]**
```nasm
...
0x0000000000401200 <+40>: call   0x401050 <verify_vip_key>
0x0000000000401205 <+45>: test   eax, eax
0x0000000000401207 <+47>: je     0x401215 <main+61>   <-- 이 곳이 점프 조건!
...
```

`check_vip_key` 함수가 실행된 직후, 그 결과값이 `eax` 레지스터에 담깁니다. (`eax`가 0이면 실패, 1이면 성공)
우리는 이 검사 직후인 `*main+45` 위치에 **중단점(Breakpoint)**을 겁니다.

```bash
(gdb) break *main+45
Breakpoint 1 at 0x401205
```

---

## 🚀 3. 공격 수행 및 레지스터 변조 (Register Manipulation)

이제 디버거 위에서 프로그램을 실행합니다.

**[GDB 실행]**
```bash
(gdb) run
Starting program: /path/to/secure_keygen.elf
Enter VIP License Key: dummy_key
```
(터미널에서 아무 키나 입력하고 엔터를 치면, 방금 걸어둔 중단점에서 프로그램이 딱 멈춥니다.)

```text
Breakpoint 1, 0x0000000000401205 in main ()
(gdb)
```

이 시점에서 현재 레지스터(`eax`)의 상태를 확인해 봅니다.
```bash
(gdb) info registers eax
eax            0x0      0
```
내가 `dummy_key`를 넣었기 때문에 검증 함수가 실패(0)를 리턴했습니다. 이대로 진행하면 `je` 분기를 타고 에러 메시지를 띄울 것입니다.

### 💡 메모리(레지스터) 덮어쓰기
해커는 마치 자기가 신이라도 된 것처럼, 이 `eax` 레지스터의 값을 강제로 `1` (성공)로 바꾸어 버립니다.

```bash
(gdb) set $eax=1
```

값이 잘 바뀌었는지 확인합니다.
```bash
(gdb) info registers eax
eax            0x1      1
```

### 🔍 프로그램 실행 재개 (Continue)
이제 프로그램을 계속 실행(Continue)시킵니다.
```bash
(gdb) continue
Continuing.
Valid VIP Key! Welcome.
FLAG{REVERSE_🥈_DYNAMIC_GDB_BYPASS_F1A2B3}
[Inferior 1 (process 1234) exited normally]
```

---

## 🚩 4. 롸잇업 결론 및 플래그

실행 파일의 바이너리가 잠겨있더라도(Anti-Patching), 운영체제의 디버깅 권한을 이용해 런타임에 메모리의 분기 플래그(Register)를 변조함으로써 손쉽게 인증 로직을 무력화할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{REVERSE_🥈_DYNAMIC_GDB_BYPASS_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
애플리케이션이 자신이 "디버깅 당하고 있는지"를 전혀 알지 못했기 때문입니다.

* **안전한 패치 가이드 (Anti-Debugging 적용)**
바이너리를 배포할 때, `ptrace` 시스템 콜 등을 활용하여 디버거(GDB, Frida 등)의 부착(Attach)을 원천 차단하는 방어 로직을 넣어야 합니다.

```c
// C 언어 Anti-Debugging (Linux) 예시
#include <sys/ptrace.h>
#include <stdio.h>
#include <stdlib.h>

void anti_debug() {
    // ptrace를 호출하여 자기 자신을 추적하려고 시도함.
    // 만약 이미 GDB 같은 디버거가 붙어있다면 ptrace는 실패(-1)를 리턴함.
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Debugger detected! Exiting...\n");
        exit(1);
    }
}

int main() {
    anti_debug();
    // 프로그램 메인 로직...
}
```
또한, 인증 결과(`eax` 체크)를 단 한 번만 검사하는 것이 아니라, 여러 곳에서 다중 분기 및 해시 검증을 교차로 수행하게 만들면 해커가 디버깅으로 우회해야 할 포인트가 기하급수적으로 늘어나 포기하게 만들 수 있습니다.