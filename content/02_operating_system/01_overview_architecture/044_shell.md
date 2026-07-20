---
title: "Shell"
date: "2026-04-05"
tags:
  - "studynote-operating-system"
weight: 44
---
> **핵심 인사이트**
> 1. 셸(Shell)은 운영체제 커널과 사용자 사이의 인터페이스로 — 사용자의 명령을 해석·실행하는 명령 해석기(Command Interpreter)이며, 이름처럼 커널을 감싸는 "껍데기" 역할을 한다.
> 2. 셸 스크립트는 변수·조건·반복·함수·파이프를 지원하는 완전한 프로그래밍 언어이며 — 프로세스 포크(fork)/익스큐트(exec) 시스템 콜의 흐름을 직접 제어하므로, OS 자동화·DevOps CI/CD 파이프라인의 핵심 도구이다.
> 3. Bash(Bourne Again SHell)는 POSIX 표준 셸의 사실상 표준이지만 — Zsh(개선된 자동완성), Fish(사용자 친화), sh(POSIX 순수 호환) 등 다양한 셸이 용도에 따라 선택되며, macOS는 Catalina 이후 기본 셸을 Bash -> Zsh로 전환했다.

---

## Ⅰ. 셸 개념

```
셸 (Shell):

운영체제 구조:
  사용자
    |
    v (명령 입력)
  [셸 (Shell)]  <- 인터프리터, 스크립트 실행
    |
    v (시스템 콜)
  [커널 (Kernel)]
    |
    v (하드웨어 제어)
  [하드웨어]

셸의 역할:
  1. 명령 해석 (Command Interpretation)
  2. 명령 실행 (fork/exec 시스템 콜)
  3. 환경 변수 관리 (PATH, HOME 등)
  4. 파이프 & 리다이렉션
  5. 작업 제어 (Job Control): fg, bg, &
  6. 셸 스크립팅

명령 실행 과정:
  사용자: ls -la /tmp

  1. 셸이 입력을 파싱: 명령=ls, 인수=-la, /tmp
  2. fork(): 자식 프로세스 생성
  3. exec(): 자식에서 /bin/ls 실행
  4. wait(): 부모(셸)가 자식 종료 대기
  5. 셸 프롬프트 재표시

셸 종류:
  sh  (Bourne Shell, 1979) — POSIX 원형
  csh (C Shell, 1978) — C 문법 유사
  ksh (Korn Shell, 1983) — sh 확장
  bash (Bourne Again SHell, 1989) — Linux 표준
  zsh (Z Shell, 1990) — 강력한 자동완성
  fish (2005) — 사용자 친화, 비POSIX
```

> 📢 **섹션 요약 비유**: 셸은 번역관 — 사람의 한국어(명령)를 커널의 언어(시스템 콜)로 번역해주는 통역사. 커널은 셸이 없으면 사람과 직접 대화하기 어려워요.

---

## Ⅱ. 셸 스크립팅 기초

```
Bash 셸 스크립팅:

기본 구조:
  #!/bin/bash          # 쉬뱅 (Shebang) — 인터프리터 지정

  # 변수
  NAME="World"
  echo "Hello, $NAME"

  # 환경 변수
  export MY_VAR="value"

조건문:
  if [ $? -eq 0 ]; then
      echo "성공"
  elif [ $COUNT -gt 10 ]; then
      echo "10 초과"
  else
      echo "실패"
  fi

  # 파일 조건
  if [ -f "/etc/passwd" ]; then echo "파일 존재"; fi
  if [ -d "/tmp" ]; then echo "디렉토리 존재"; fi

반복문:
  # for 루프
  for i in {1..5}; do
      echo "처리 중: $i"
  done

  # while 루프
  COUNT=0
  while [ $COUNT -lt 10 ]; do
      COUNT=$((COUNT + 1))
  done

  # 파일 처리
  for FILE in /tmp/*.log; do
      echo "로그: $FILE"
  done

함수:
  greet() {
      local NAME=$1    # 지역 변수
      echo "Hello, $NAME"
      return 0
  }
  greet "Alice"

파이프 & 리다이렉션:
  # 파이프: 출력 -> 다음 명령 입력
  ls -la | grep ".log" | wc -l

  # 리다이렉션
  echo "로그" >> output.log   # 추가
  cat < input.txt             # 입력 리다이렉션
  find / 2>/dev/null          # 에러 버림
```

> 📢 **섹션 요약 비유**: 셸 스크립팅은 요리 레시피 — 변수는 재료 이름, 조건은 "소금이 있으면", 반복은 "재료마다 씻고", 함수는 재사용 가능한 레시피 단위.

---

## Ⅲ. 환경 변수와 프로세스

```
환경 변수 (Environment Variables):

주요 환경 변수:
  PATH: 실행 파일 검색 경로
  HOME: 홈 디렉토리 (/root, /home/user)
  USER: 현재 사용자 이름
  SHELL: 현재 셸 경로
  PS1: 프롬프트 형식 (user@host:~$)
  LANG: 언어/인코딩 (ko_KR.UTF-8)
  PWD: 현재 작업 디렉토리

PATH 동작:
  PATH=/usr/local/bin:/usr/bin:/bin

  ls 명령 실행:
  1. /usr/local/bin/ls 있나? 없음
  2. /usr/bin/ls 있나? 없음
  3. /bin/ls 있나? 있음 -> 실행

셸 변수 vs 환경 변수:
  MY_VAR="local"   -> 현재 셸만 (export 없음)
  export MY_VAR    -> 자식 프로세스에게 상속

  확인: env | grep MY_VAR
  삭제: unset MY_VAR

특수 변수:
  $0: 스크립트 이름
  $1~$9: 위치 매개변수
  $#: 인수 개수
  $@: 모든 인수 (배열)
  $?: 이전 명령 종료 코드 (0=성공)
  $$: 현재 프로세스 PID
  $!: 마지막 백그라운드 PID

셸에서 프로세스 생성:
  fg_job: 포그라운드 (셸 대기)
  bg_job &: 백그라운드 (셸 즉시 프롬프트)

  작업 제어:
  Ctrl+Z: 일시 중지 (SIGTSTP)
  bg: 백그라운드 재개
  fg: 포그라운드로 가져오기
  jobs: 백그라운드 작업 목록
```

> 📢 **섹션 요약 비유**: 환경 변수는 작업 도시락 — PATH는 식당 위치 목록, HOME은 집 주소, 셸은 도시락을 자식(프로세스)에게 전달할 때 export로 챙겨줘요.

---

## Ⅳ. 고급 셸 기능

```
고급 셸 기능:

프로세스 치환 (Process Substitution):
  diff <(ls dir1) <(ls dir2)
  -> 명령 출력을 파일처럼 사용

Here Document:
  cat <<EOF
  여러 줄 텍스트
  변수 $NAME 사용 가능
  EOF

배열:
  ARR=("a" "b" "c")
  echo ${ARR[0]}        # a
  echo ${#ARR[@]}       # 3 (길이)
  for ITEM in "${ARR[@]}"; do echo $ITEM; done

문자열 조작:
  STR="hello_world.txt"
  echo ${STR^^}          # 대문자: HELLO_WORLD.TXT
  echo ${STR%.*}         # 확장자 제거: hello_world
  echo ${STR#*_}         # 앞부분 제거: world.txt
  echo ${STR/hello/Hi}   # 치환: Hi_world.txt

정규 표현식:
  [[ "hello123" =~ ^[a-z]+[0-9]+$ ]] && echo "매치"

Zsh 차이점:
  자동완성: 탭키로 경로/명령 자동완성 (bash보다 강력)
  플러그인: Oh-My-Zsh 생태계
  Globbing: **/*.txt (재귀 탐색)

fish 특징:
  문법: if command; echo OK; end
  자동 제안: 이력 기반 실시간 제안
  비POSIX: bash 스크립트와 호환 안 됨

셸 최적화:
  .bashrc vs .bash_profile:
    .bash_profile: 로그인 셸 (한 번)
    .bashrc: 인터랙티브 셸 (매번)

  alias 정의:
    alias ll="ls -la"
    alias gs="git status"
```

> 📢 **섹션 요약 비유**: 고급 셸 기능은 개인 비서 커스터마이징 — alias는 단축 명령어(습관 단어), .bashrc는 출근 시 비서에게 전달하는 설정 메모. 셸을 내 입맛에 맞게 꾸밀 수 있어요.

---

## Ⅴ. 실무 시나리오 — CI/CD 배포 자동화

```
CI/CD 배포 셸 스크립트:

deploy.sh:
  #!/bin/bash
  set -e            # 오류 시 즉시 종료
  set -u            # 미정의 변수 사용 시 오류
  set -o pipefail   # 파이프 중 오류 감지

  # 설정
  APP_NAME="myapp"
  DEPLOY_DIR="/opt/$APP_NAME"
  BACKUP_DIR="/opt/backup"

  # 함수 정의
  log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }

  check_health() {
      local URL=$1
      local HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)
      [ "$HTTP_CODE" = "200" ]
  }

  # 현재 버전 백업
  log "백업 시작"
  cp -r $DEPLOY_DIR $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)

  # 새 버전 배포
  log "배포 시작"
  git -C $DEPLOY_DIR pull origin main

  # 의존성 설치
  pip install -r requirements.txt --quiet

  # 서비스 재시작
  systemctl restart $APP_NAME

  # 헬스체크
  log "헬스체크 중..."
  RETRY=0
  while ! check_health "http://localhost:8080/health"; do
      RETRY=$((RETRY+1))
      if [ $RETRY -gt 10 ]; then
          log "헬스체크 실패 — 롤백"
          cp -r $BACKUP_DIR/latest $DEPLOY_DIR
          systemctl restart $APP_NAME
          exit 1
      fi
      sleep 3
  done

  log "배포 완료"

사용:
  chmod +x deploy.sh
  ./deploy.sh 2>&1 | tee -a /var/log/deploy.log
```

> 📢 **섹션 요약 비유**: CI/CD 셸 스크립트는 자동 이사 — 기존 짐 백업 -> 새 짐 배치 -> 입주 확인(헬스체크) -> 문제면 자동 되돌리기. 사람 손 없이 자동으로 안전하게 배포.

---

## 📌 관련 개념 맵

```
셸 (Shell)
+-- 종류
|   +-- sh (POSIX), bash (Linux 표준)
|   +-- zsh (자동완성), fish (UX)
+-- 핵심 기능
|   +-- 명령 실행 (fork/exec)
|   +-- 파이프 & 리다이렉션
|   +-- 환경 변수 (PATH, HOME)
+-- 스크립팅
|   +-- 변수, 조건, 반복, 함수
|   +-- 특수 변수 ($?, $$, $@)
+-- 응용
|   +-- CI/CD 자동화
|   +-- 시스템 관리 (cron)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Thompson Shell (1971)]
Unix v1 최초 셸
기본 명령 실행만
      |
      v
[Bourne Shell sh (1979)]
스크립팅 기초 (조건, 반복, 함수)
POSIX 표준의 원형
      |
      v
[Bash (1989)]
GNU 프로젝트 sh 대체
Linux 표준 셸로 자리잡음
      |
      v
[Zsh + Oh-My-Zsh (2009~)]
플러그인 생태계 형성
macOS 기본 셸 전환 (2019)
      |
      v
[현재: DevOps 자동화]
Bash + CI/CD (GitHub Actions)
Container 셸 (Alpine sh)
셸 대신 Python 스크립트 증가
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 셸은 번역관 — 사람의 말(ls -la)을 컴퓨터 커널 언어(시스템 콜)로 번역해주는 통역사예요!
2. 셸 스크립트는 자동 요리 레시피 — 재료 준비->가열->담기 순서를 스크립트로 써두면 버튼 하나로 자동으로 실행!
3. bash vs zsh — bash는 기본 잘 되는 도구, zsh는 자동완성이 뛰어난 스마트 도구. macOS는 zsh로 업그레이드했어요!
