# OpenCode 설치 가이드

## 1. 설치

```bash
# OpenCode 설치
brew install opencode

# 설정 디렉토리 생성
mkdir -p ~/.config/opencode
echo '{}' > ~/.config/opencode/opencode.json

# Oh My OpenCode 설치
bunx oh-my-opencode install

# Alias 등록
echo "alias omoc='bunx oh-my-opencode'" >> ~/.zshrc && source ~/.zshrc
```

---

## 2. API 키 설정

### 기본 설정 (평문 저장)
```bash
cat >> ~/.zshrc << 'EOF'
export GOOGLE_API_KEY="AIza..."
export GEMINI_API_KEY="$GOOGLE_API_KEY"
export GOOGLE_GENERATIVE_AI_API_KEY="$GOOGLE_API_KEY"
EOF
source ~/.zshrc
```

### 보안 설정 (키체인 사용)
```bash
# 키체인에 저장
security add-generic-password -a "$USER" -s "OpenCode_Gemini_Key" -w "<YOUR_KEY>"

# ~/.zshrc에 추가
cat >> ~/.zshrc << 'EOF'
export GOOGLE_API_KEY=$(security find-generic-password -w -s "OpenCode_Gemini_Key")
export GEMINI_API_KEY=$GOOGLE_API_KEY
export GOOGLE_GENERATIVE_AI_API_KEY=$GOOGLE_API_KEY
EOF
source ~/.zshrc
```

---

## 3. 에이전트 설정

`~/.config/opencode/oh-my-opencode.json`:
```json
{
  "agents": {
    "Sisyphus": { "model": "google/gemini-3-pro-preview" },
    "oracle": { "model": "google/gemini-3-pro-preview" },
    "explore": { "model": "google/gemini-3-pro-preview" },
    "document-writer": { "model": "google/gemini-3-pro-preview" }
  }
}
```

---

## 4. 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `opencode` | TUI 모드 실행 |
| `opencode models google` | 사용 가능한 모델 목록 |
| `omoc run "<message>"` | AI 작업 실행 |
| `omoc doctor` | 설치 상태 점검 |

---

## 5. 트러블슈팅

| 오류 | 해결 |
|------|------|
| `AI_LoadAPIKeyError` | `GOOGLE_GENERATIVE_AI_API_KEY` 환경변수 설정 |
| `Model Not Found` | `opencode models google`로 모델명 확인 |

opencode auth logout
opencode auth login