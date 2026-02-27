+++
title = "Claude Code + Z.AI GLM 설정 가이드 (Mac / Linux)"
date = 2026-02-28

[extra]
categories = "devops"
+++

# Claude Code + Z.AI GLM 설정 가이드 (Mac / Linux)

## 핵심 인사이트 (3줄 요약)

> **Claude Code**를 Anthropic 대신 Z.AI(GLM) 백엔드로 연결해 사용할 수 있다.
> 환경 변수 `ANTHROPIC_BASE_URL`을 Z.AI 엔드포인트로 바꾸고 API Key를 설정하면 끝이다.
> Mac(M1/M2)은 Homebrew, Linux는 npm으로 설치하며, 셸 설정 파일에 환경 변수를 추가한다.

---

## 1. 설치

### Mac (M1/M2 — Homebrew)

```bash
# Homebrew Cask로 설치
brew install --cask claude-code
```

> Homebrew Formulae: https://formulae.brew.sh/cask/claude-code

### Linux / Mac (npm)

```bash
npm install -g @anthropic-ai/claude-code
```

---

## 2. 로그아웃 (기존 Anthropic 세션 초기화)

```bash
claude /logout
```

Z.AI 키로 전환하기 전에 기존 Anthropic 로그인 세션을 먼저 끊어야 한다.

---

## 3. 셸 환경 변수 설정

### 현재 셸 확인

```bash
echo $SHELL
# /bin/zsh  또는  /bin/bash
```

### zsh 사용자 (~/.zshrc)

```bash
vim ~/.zshrc
```

### bash 사용자 (~/.bashrc)

```bash
vim ~/.bashrc
```

파일 맨 아래에 다음 내용 추가:

```bash
# Z.AI Claude Code Configuration
export ANTHROPIC_AUTH_TOKEN="your_zai_api_key_here"

# Z.AI 엔드포인트 (둘 중 하나 선택)
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
# export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"

# 타임아웃 (긴 응답 대비 넉넉하게 설정)
export API_TIMEOUT_MS="3000000"

# GLM 모델로 매핑
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.7"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.7"
```

### 적용

```bash
source ~/.zshrc   # zsh
# 또는
source ~/.bashrc  # bash
```

---

## 4. 프로젝트별 설정 (`.claude/settings.json`)

특정 프로젝트에서만 Z.AI를 사용하려면 프로젝트 루트에 설정 파일을 생성:

```bash
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_zai_api_key",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-4.7"
  }
}
EOF
```

> **글로벌 설정** 파일 위치: `~/.claude/settings.json`

---

## 5. 환경 변수 설명

| 변수 | 설명 | 예시 값 |
|------|------|---------|
| `ANTHROPIC_AUTH_TOKEN` | Z.AI API Key | `sk-xxx...` |
| `ANTHROPIC_BASE_URL` | API 엔드포인트 | `https://api.z.ai/api/anthropic` |
| `API_TIMEOUT_MS` | 요청 타임아웃 (ms) | `3000000` (50분) |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 모델 매핑 | `glm-4.7` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 모델 매핑 | `glm-4.7` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 모델 매핑 | `glm-4.7` |

### 엔드포인트 선택

| 엔드포인트 | 설명 |
|-----------|------|
| `https://api.z.ai/api/anthropic` | Z.AI 글로벌 |
| `https://open.bigmodel.cn/api/anthropic` | Zhipu 직접 (중국 본토) |

---

## 6. 동작 확인

```bash
# Claude Code 실행
claude

# 또는 특정 파일과 함께
claude "이 코드를 리뷰해줘" main.py
```

정상 동작 시 GLM-4.7 모델로 응답이 반환된다.

---

## 7. 모델 선택 가이드

| Claude 원본 | Z.AI 매핑 | 특징 |
|------------|-----------|------|
| claude-haiku | `glm-4.7` | 빠른 응답 |
| claude-sonnet | `glm-4.7` | 범용 (권장) |
| claude-opus | `glm-4.7` | 복잡한 추론 |
| — | `glm-4-plus` | 고성능 |
| — | `glm-4-flash` | 최저 지연 |

---

## 8. 문제 해결

### API Key 오류

```bash
# 환경 변수 적용 확인
echo $ANTHROPIC_AUTH_TOKEN
echo $ANTHROPIC_BASE_URL
```

값이 비어있으면 `source ~/.zshrc` 재실행.

### 타임아웃 오류

```bash
# 타임아웃 값 더 늘리기
export API_TIMEOUT_MS="6000000"
```

### 기존 Anthropic 세션 충돌

```bash
claude /logout
source ~/.zshrc
claude
```

---

## 참고

- [Z.AI 공식 문서](https://docs.z.ai)
- [Z.AI API Key 발급](https://console.z.ai)
- [Homebrew Claude Code Cask](https://formulae.brew.sh/cask/claude-code)
- [Anthropic Claude Code 공식](https://docs.anthropic.com/claude-code)
