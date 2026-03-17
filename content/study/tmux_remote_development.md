+++
title = "tmux로 모바일 원격 개발 환경 구축하기"
date = "2026-03-08"
[extra]
tags = ["tmux", "remote-development", "ubuntu", "mobile", "claude-code"]
+++

## 개요

모바일 기기에서 원격 우분투 서버에 접속해 Claude Code를 실행하면, 연결이 끊겨도 작업이 유지되어야 합니다. tmux는 이런 **persistent session**을 제공하는 터미널 멀티플렉서입니다.

---

## 1. tmux 설치

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install tmux -y

# macOS
brew install tmux
```

---

## 2. 기본 설정 파일 (~/.tmux.conf)

```bash
# 마우스 지원 (모바일에서 필수)
set -g mouse on

# 256색 지원
set -g default-terminal "screen-256color"

# Ctrl+b -> Ctrl+a로 변경 (더 편함)
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# 창 분할 단축키 (직관적으로)
bind | split-window -h    # | 로 수직 분할
bind - split-window -v    # - 로 수평 분할

# Vim 스타일 pane 이동
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# pane 크기 조절 (Shift + 화살표로도 가능하지만 키바인드로)
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# 세션 이름 표시 개선
set -g status-position bottom
set -g status-justify left
set -g status-style 'bg=colour235 fg=colour136'
set -g status-left '#[fg=colour232,bg=colour154,bold] #S #[bg=colour235] '
set -g status-right '#[fg=colour233,bg=colour241,bold] %Y-%m-%d %H:%M '

# 윈도우 리스트 스타일
set -g window-status-format '#[fg=colour245] #I:#W '
set -g window-status-current-format '#[fg=colour81,bg=colour235,bold] #I:#W '

# 활동 모니터링
set -g monitor-activity on
set -g visual-activity off

# 히스토리 크기 증가
set -g history-limit 10000

# 인덱스 1부터 시작
set -g base-index 1
setw -g pane-base-index 1

# 자동 윈도우 이름 끄기
set -g allow-rename off
```

설정 적용:
```bash
tmux source ~/.tmux.conf
```

---

## 3. 필수 단축키

### Prefix 키
모든 단축키는 **Prefix(Ctrl+a)** 를 먼저 누른 후 입력합니다.

| 단축키 | 설명 |
|--------|------|
| `Ctrl+a d` | 세션 detach (백그라운드로) |
| `Ctrl+a c` | 새 윈도우 생성 |
| `Ctrl+a n` | 다음 윈도우 |
| `Ctrl+a p` | 이전 윈도우 |
| `Ctrl+a 0-9` | 윈도우 번호로 이동 |
| `Ctrl+a \|` | 수직 분할 (커스텀) |
| `Ctrl+a -` | 수평 분할 (커스텀) |
| `Ctrl+a h/j/k/l` | pane 이동 |
| `Ctrl+a x` | pane 닫기 |
| `Ctrl+a [` | copy mode (스크롤) |
| `Ctrl+a ?` | 모든 단축키 보기 |
| `Ctrl+a :` | 명령 모드 |

### Copy Mode 스크롤
```bash
Ctrl+a [    # copy mode 진입
# 그 다음 화살표/Page Up/Page Down으로 스크롤
q           # copy mode 종료
```

---

## 4. 세션 관리

### 세션 생성 및 attach
```bash
# 새 세션 생성 (이름 지정)
tmux new -s dev

# 세션 목록
tmux ls

# 세션에 다시 접속
tmux attach -t dev
# 또는
tmux a -t dev

# 마지막 세션에 접속
tmux a

# 세션 종료 (inside tmux)
exit
# 또는
Ctrl+a :kill-session
```

### 세션 내에서 세션 전환
```bash
Ctrl+a s    # 세션 선택 메뉴
Ctrl+a (    # 이전 세션
Ctrl+a )    # 다음 세션
```

---

## 5. 모바일 개발 워크플로우

### Step 1: 우분투 서버에 tmux 세션 생성
```bash
# 서버에서
tmux new -s claude-dev
```

### Step 2: Claude Code 실행
```bash
# 세션 안에서
cd ~/projects/my-project
claude
```

### Step 3: 모바일에서 접속
1. **Termux** (Android) 또는 **iSH/Blink Shell** (iOS) 설치
2. SSH로 서버 접속:
   ```bash
   ssh user@your-server-ip
   ```
3. tmux 세션에 attach:
   ```bash
   tmux a -t claude-dev
   ```

### Step 4: 작업 후 detach
```bash
Ctrl+a d    # 세션 유지하면서 연결 해제
```

---

## 6. tmux 플러그인 관리자 (TPM) - 선택사항

```bash
# TPM 설치
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

`~/.tmux.conf`에 추가:
```bash
# 플러그인 리스트
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'    # 세션 저장/복원

# TPM 초기화 (파일 마지막에)
run '~/.tmux/plugins/tpm/tpm'
```

플러그인 설치:
```bash
tmux source ~/.tmux.conf
# 그 다음 Prefix + I (대문자 I) 눌러서 플러그인 설치
```

---

## 7. 유용한 팁

### 세션 자동 시작 스크립트
```bash
# ~/start-dev.sh
#!/bin/bash
tmux has-session -t claude-dev 2>/dev/null
if [ $? != 0 ]; then
    tmux new -d -s claude-dev -c ~/projects
fi
tmux attach -t claude-dev
```

### SSH 연결 시 바로 tmux 실행
```bash
# ~/.bashrc 또는 ~/.zshrc
if [ -z "$TMUX" ] && [ -n "$SSH_CONNECTION" ]; then
    tmux attach -t dev 2>/dev/null || tmux new -s dev
fi
```

### 세션 저장/복원 (tmux-resurrect)
```bash
Ctrl+a Ctrl+s    # 세션 저장
Ctrl+a Ctrl+r    # 세션 복원
```

---

## 8. 문제 해결

### 색상이 이상할 때
```bash
# ~/.bashrc 또는 ~/.zshrc
export TERM=xterm-256color
```

### tmux 안에서 clipboad 복사
```bash
# copy mode에서
Ctrl+a [
v              # visual mode 시작 (Vim 스타일)
y              # yank (복사)
```

### 세션이 안 보일 때
```bash
# 모든 세션 나열
tmux list-sessions
# 죽은 세션 정리
tmux kill-server
```

---

## 요약

| 상황 | 명령어 |
|------|--------|
| 세션 생성 | `tmux new -s 이름` |
| 세션 목록 | `tmux ls` |
| 세션 접속 | `tmux a -t 이름` |
| 세션 나가기 | `Ctrl+a d` |
| 세션 종료 | `exit` 또는 `Ctrl+d` |

tmux를 사용하면 모바일에서 연결이 끊겨도 Claude Code가 계속 실행되므로, 언제든 다시 접속해서 작업을 이어갈 수 있습니다.