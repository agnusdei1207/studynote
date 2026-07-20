---
title: "Environment Variables"
date: "2026-05-08"
tags:
  - "studynote-operating-system"
weight: 156
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 환경 변수 (Environment Variables) 상속은 프로세스와 스레드의 생성·실행·협력에서 핵심 흐름을 결정하는 개념으로, 시스템이 무엇을 먼저 관리하고 어떤 순서로 제어할지를 분명하게 만든다.
> 2. **가치**: 이 개념을 이해하면 자원 효율, 응답 시간, 안정성 사이의 균형을 더 정확하게 설명할 수 있고, OOM (Out Of Memory) Killer 프로세스 종료 정책로 이어지는 이유도 자연스럽게 파악된다.
> 3. **판단 포인트**: 동적 링킹 프로세스 (ld.so) 로딩 과정과의 관계를 함께 봐야 환경 변수 (Environment Variables) 상속을 단순 정의가 아니라 실제 설계·운영 판단 기준으로 사용할 수 있다.

---

## Ⅰ. 개요 및 필요성

### 1. 정의

환경 변수(Environment Variable)는 운영체제에서 프로세스가 실행될 때 참조할 수 있는 키-값(Key-Value) 쌍으로 이루어진 문자열이다. 프로세스는 부모 프로세스(Parent Process)로부터 환경 변수를 상속(Inherit)받으며, 이를 통해 실행 환경 설정을 자식 프로세스(Child Process)에 전달한다.

> **비유**: 환경 변수는 "가족의 전통 레시피"다. 부모가 아이에게 전달하며, 아이는 그대로 사용하거나 자신만의 재료를 추가할 수 있다.

### 2. 프로세스 메모리에서의 환경 변수

```
프로세스 메모리 레이아웃 상 환경 변수의 위치

High Address
+---------------------------+
|         Stack             |
|   argv[0], argv[1], ...   |
|   envp[0], envp[1], ...  | <-- 환경 변수 포인터 배열
|   argc                     |
+---------------------------+
|          |                |  Stack grows downward
|          v                |
+---------------------------+
|        Heap               |  Heap grows upward
+---------------------------+
|       BSS                 |
|       Data                |
|       Text (Code)         |
+---------------------------+
Low Address

환경 변수 블록 (Environ Block):
+--------------------------------------+
| PATH=/usr/bin:/bin                   |
| HOME=/home/user                      |
| LANG=ko_KR.UTF-8                     |
| LD_LIBRARY_PATH=/opt/lib             |
| SHELL=/bin/bash                      |
| TERM=xterm-256color                  |
| NULL (terminator)                    |
+--------------------------------------+
```

> **비유**: 환경 변수는 프로세스라는 "가방" 주머니에 넣어둔 "메모 쪽지"들이다. 프로그램은 언제든 주머니에서 꺼내 읽을 수 있다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 시스템 핵심 환경 변수

| 환경 변수 | 설명 | 예시 |
|-----------|------|------|
| **PATH** | 실행 파일 검색 경로 | `/usr/bin:/bin:/usr/local/bin` |
| **HOME** | 사용자 홈 디렉토리 | `/home/user` |
| **LANG** | 로케일 및 언어 설정 | `ko_KR.UTF-8` |
| <strong>SHELL</strong> | 로그인 셸 경로 | `/bin/bash` |
| **TERM** | 터미널 유형 | `xterm-256color` |
| **USER** | 현재 사용자 이름 | `ubuntu` |
| **PWD** | 현재 작업 디렉토리 | `/home/user/project` |
| **LD_LIBRARY_PATH** | 동적 라이브러리 검색 경로 | `/opt/oracle/lib` |
| **LD_PRELOAD** | 사전 로드할 라이브러리 | `/tmp/malloc_hook.so` |
| **TMPDIR** | 임시 파일 디렉토리 | `/tmp` |

### 2. PATH 환경 변수

- **PATH** (Path): 셸이 명령어를 입력받았을 때 실행 파일을 검색하는 디렉토리 목록이다. 콜론(`:`)으로 구분되며, 왼쪽부터 순서대로 검색한다.

```bash
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 현재 디렉토리를 PATH에 추가 (보안 주의)
$ export PATH=.:$PATH   # 위험: 현재 디렉토리의 악성 파일 실행 가능
```

### 3. 환경 변수 설정 방법

```bash
# 임시 설정 (현재 셸만)
export MY_VAR="hello"

# 영구 설정
echo 'export MY_VAR="hello"' >> ~/.bashrc

# 자식 프로세스에만 전달 (현재 셸에는 미설정)
MY_VAR="hello" /bin/child_program

# unset으로 제거
unset MY_VAR
```

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 1. C 표준 라이브러리 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| **getenv()** | `char *getenv(const char *name)` | 환경 변수 값 조회 |
| **setenv()** | `int setenv(const char *name, const char *value, int overwrite)` | 환경 변수 설정 (overwrite=1이면 덮어씀) |
| **putenv()** | `int putenv(char *string)` | "NAME=VALUE" 형식 문자열로 설정 (버퍼 소유권 이전) |
| **unsetenv()** | `int unsetenv(const char *name)` | 환경 변수 제거 |
| **environ** | `extern char **environ` | 전체 환경 변수 배열에 대한 전역 포인터 |

### 2. 사용 예제

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 환경 변수 조회
    char *path = getenv("PATH");
    if (path) {
        printf("PATH: %s\n", path);
    }

    // 환경 변수 설정 (기존 값 있으면 덮어씀)
    setenv("MY_APP_DIR", "/opt/myapp", 1);

    // putenv: 문자열 포인터를 직접 전달 (주의: 버퍼 수정 시 문제)
    putenv("MY_TEMP_VAR=temp_value");

    // 환경 변수 제거
    unsetenv("MY_TEMP_VAR");

    // 전체 환경 변수 순회
    extern char **environ;
    for (char **env = environ; *env != NULL; env++) {
        printf("%s\n", *env);
    }

    return 0;
}
```

```
환경 변수 API 동작 흐름

[getenv("PATH")]
    |
    v
environ 배열에서 "PATH="로 시작하는 항목 검색
    |
    v
"PATH=/usr/bin:/bin"에서 '=' 이후 문자열 반환
    |
    v
포인터 반환 (복사본 아님, 수정하면 안 됨)

[setenv("KEY", "VALUE", 1)]
    |
    v
environ 배열에서 "KEY=" 검색
    |
    +-- 있고 overwrite=1 --> 기존 항목 대체
    |
    +-- 없음 --> environ 배열 확장 후 새 항목 추가
```

> **비유**: getenv()는 "전화번호부에서 이름 찾기", setenv()는 "전화번호부에 새 번호 등록하기"와 같다. putenv()는 "직접 전화번호부 책갈피에 메모지 꽂기"라서 메모지를 분실하면 번호도 사라진다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. fork() 시 환경 변수 복사

`fork()` 시스템 콜은 부모 프로세스의 환경 변수 블록(Environ Block)을 자식 프로세스로 <strong>복사(Copy)</strong>한다. 부모와 자식은 독립적인 복사본을 가지므로, 한쪽에서 `setenv()`를 호출해도 다른 쪽에 영향을 주지 않는다.

```
fork() 시 환경 변수 복사

[Parent Process]                    [Child Process]
environ:                            environ:
  PATH=/usr/bin                       PATH=/usr/bin       (복사본)
  HOME=/home/user                     HOME=/home/user     (복사본)
  MY_VAR=parent                       MY_VAR=parent       (복사본)
        |                                    |
        | fork()                             |
        v                                    v
  setenv("MY_VAR", "changed", 1)       // 영향 없음
  MY_VAR=changed                      MY_VAR=parent (그대로)
```

### 2. exec() 시 환경 변수 대체

`exec()` 계열 함수는 현재 프로세스의 이미지를 새 프로그램으로 <strong>완전히 교체</strong>한다. 이때 환경 변수 처리는 함수에 따라 다르다.

| 함수 | 환경 변수 동작 |
|------|---------------|
| `execl(path, arg...)` | 기존 환경 변수 유지 |
| `execv(path, argv)` | 기존 환경 변수 유지 |
| `execle(path, arg..., envp)` | **새 envp로 대체** |
| `execve(path, argv, envp)` | **새 envp로 대체** |
| `execlp(file, arg...)` | 기존 환경 변수 유지 + PATH 검색 |
| `execvp(file, argv)` | 기존 환경 변수 유지 + PATH 검색 |

```
exec() 계열의 환경 변수 처리

[execl("/bin/ls", "ls", NULL)]
    기존 environ 블록 그대로 유지
    --> ls가 부모와 동일한 환경 변수로 실행됨

[execle("/bin/ls", "ls", NULL, new_envp)]
    기존 environ 폐기
    --> new_envp 배열이 새 environ이 됨
    --> 부모의 환경 변수 완전히 사라짐

[execve("/bin/ls", argv, new_envp)]
    execle와 동일 (배열 형식)
```

> **비유**: fork()는 "부모의 레시피 노트를 복사해서 아이에게 주는 것"이고, execle()는 "아이가 자기만의 새 레시피 노트로 교체하는 것"이다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

### 1. LD_PRELOAD의 동작 원리

- **LD_PRELOAD**: 동적 링커가 다른 모든 라이브러리보다 먼저 로드하는 라이브러리 경로를 지정하는 환경 변수이다. 이를 이용해 표준 라이브러리 함수를 가로채거나(Hooking) 대체할 수 있다.

### 2. 공격 시나리오

```c
// malicious.c - malloc을 가로채는 악성 라이브러리
#include <stdio.h>

void *malloc(size_t size) {
    printf("[ATTACK] malloc(%zu) intercepted!\n", size);
    // 원래 malloc 대신 임의 동작 수행
    return NULL;  // DoS 공격
}
```

```bash
# 악성 라이브러리 컴파일
gcc -shared -fPIC -o /tmp/malicious.so malicious.c -ldl

# 공격 실행
LD_PRELOAD=/tmp/malicious.so /usr/bin/victim_program
# victim_program의 모든 malloc 호출이 가로채짐!
```

### 3. 방어 수단

```
LD_PRELOAD 공격 방어 레이어

+------------------------------------------+
| 1. SUID/SGID 바이너리                     |
|    -> LD_PRELOAD 무시 (보안 설정)          |
+------------------------------------------+
| 2. /etc/ld.so.preload (관리자 전용)       |
|    -> 시스템 수준 preloading만 허용        |
+------------------------------------------+
| 3. setenv("LD_PRELOAD", "", 1)           |
|    -> 프로그램 시작 시 명시적 초기화        |
+------------------------------------------+
| 4. Docker/Container 격리                  |
|    -> 호스트 환경 변수 격리                |
+------------------------------------------+
| 5. Capabilities / SELinux                 |
|    -> 라이브러리 로딩 권한 제한            |
+------------------------------------------+
```

> **비유**: LD_PRELOAD 공격은 "수업 전에 선생님의 교과서를 가짜 교과서로 몰래 바꿔치기하는 것"이다. SUID는 "출입증을 확인하는 교실 문지기" 역할을 한다.

---

### 지식 그래프

```
환경 변수 상속
+-- 기본 개념
|   +-- 키-값(Key-Value) 쌍
|   +-- 부모-자식 상속 (Inheritance)
|   +-- environ 블록 (메모리의 Stack 영역)
+-- 주요 환경 변수
|   +-- PATH (실행 파일 검색 경로)
|   +-- HOME (사용자 홈 디렉토리)
|   +-- LANG (로케일 설정)
|   +-- LD_LIBRARY_PATH (동적 라이브러리 경로)
|   +-- LD_PRELOAD (사전 로드 라이브러리)
+-- C API
|   +-- getenv() (조회)
|   +-- setenv() (설정)
|   +-- putenv() (포인터 직접 설정)
|   +-- unsetenv() (제거)
+-- 프로세스 생성 시 동작
|   +-- fork() -> 환경 변수 복사
|   +-- exec() -> 유지 또는 대체
|   +-- execl/execv -> 기존 환경 유지
|   +-- execle/execve -> 새 envp로 대체
+-- 보안
    +-- LD_PRELOAD 공격 (함수 가로채기)
    +-- SUID/SGID 바이너리 안전
    +-- 컨테이너 격리
```

### 세 줄 설명 (어린이용)

1. 환경 변수는 컴퓨터 프로그램에게 "어디에서 무엇을 찾아야 하는지" 알려주는 메모장이에요.
2. 부모 프로그램은 이 메모장을 복사해서 자식 프로그램에게 주고, 자식은 필요한 내용을 바꿀 수 있어요.
3. LD_PRELOAD는 나쁜 사람이 가짜 도구를 먼저 끼워 넣어서 프로그램을 속이는 나쁜 짓이에요, 그래서 방어가 필요해요.

### 약어 정리

| 약어 | Full Name |
|------|-----------|
| PATH | Pathname Variable |
| HOME | Home Directory |
| LANG | Language and Locale |
| API | Application Programming Interface |
| SUID | Set Owner User ID |
| SGID | Set Group ID |

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 스레드 스택 오버플로우 방지 (Guard Page) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 동적 링킹 프로세스 (ld.so) 로딩 과정 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| OOM (Out Of Memory) Killer 프로세스 종료 정책 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| oom_score_adj | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[동적 링킹 프로세스 (ld.so) 로딩 과정]
    |
    v
[환경 변수 (Environment Variables) 상속]
    |
    +---> [OOM (Out Of Memory) Killer 프로세스 종료 정책]
    +---> [oom_score_adj]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 환경 변수 (Environment Variables) 상속은 컴퓨터가 여러 일을 나눠서 처리하고 서로 기다리게 하는 약속이에요.
2. 먼저 동적 링킹 프로세스 (ld.so) 로딩 과정을 이해하면 환경 변수 (Environment Variables) 상속이 왜 필요한지 더 쉽게 보여요.
3. 그래서 환경 변수 (Environment Variables) 상속을 잘 알면 나중에 OOM (Out Of Memory) Killer 프로세스 종료 정책도 훨씬 쉽게 배울 수 있어요.
