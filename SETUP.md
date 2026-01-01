# 🔧 개발 환경 설정 가이드

> Dev Container를 사용한 Rust 학습 환경 구축

## 📋 목차

1. [사전 요구사항](#사전-요구사항)
2. [환경 구성](#환경-구성)
3. [사용 방법](#사용-방법)
4. [명령어 치트시트](#명령어-치트시트)
5. [문제 해결](#문제-해결)

---

## ⚙️ 사전 요구사항

### 필수
- **Docker Desktop** (macOS, Windows, Linux)
  - [다운로드 링크](https://www.docker.com/products/docker-desktop/)

### 선택 (권장)
- **VS Code** + **Dev Containers 확장**
  - 컨테이너 내부에서 바로 코드 편집 가능

---

## 🏗️ 환경 구성

### 파일 구조
```
rust-learning/
├── docker-compose.yml    # 컨테이너 오케스트레이션
├── Dockerfile            # Rust 개발 환경 이미지
└── .devcontainer/        # VS Code Dev Container 설정 (선택)
    └── devcontainer.json
```

### 제공되는 환경
- **Rust**: 최신 stable 버전
- **Cargo**: Rust 패키지 매니저
- **rustfmt**: 코드 포매터
- **clippy**: 린터
- **rust-analyzer**: LSP (VS Code 연동시)

---

## 🚀 사용 방법

### 방법 1: 터미널에서 Docker Compose 사용

#### 1. 컨테이너 시작
```bash

docker compose up -d
```

#### 2. 컨테이너 내부에서 명령 실행
```bash
# Rust 버전 확인
docker compose exec rust-dev rustc --version

# Cargo 버전 확인
docker compose exec rust-dev cargo --version

# 새 프로젝트 생성
cargo new ch1

# 프로젝트 빌드
docker compose exec rust-dev cargo build --manifest-path ch1/Cargo.toml

# 프로젝트 실행
docker compose exec rust-dev cargo run --manifest-path ch1/Cargo.toml
```

#### 3. 컨테이너 쉘 접속 (대화형)
```bash
docker compose exec rust-dev bash
# 이제 컨테이너 내부에서 직접 명령어 실행 가능
cargo --version
```

#### 4. 컨테이너 종료
```bash
docker compose down
```

---

### 방법 2: VS Code Dev Containers 사용 (권장)

1. VS Code에서 `rust-learning` 폴더 열기
2. 좌하단 `><` 아이콘 클릭
3. "Reopen in Container" 선택
4. 자동으로 컨테이너 빌드 및 연결
5. 터미널에서 바로 `cargo` 명령 사용 가능

---

## 📝 명령어 치트시트

### Docker Compose 명령어

| 명령어 | 설명 |
|--------|------|
| `docker compose up -d` | 백그라운드에서 컨테이너 시작 |
| `docker compose down` | 컨테이너 종료 |
| `docker compose logs -f` | 로그 실시간 확인 |
| `docker compose exec rust-dev bash` | 컨테이너 쉘 접속 |
| `docker compose exec rust-dev <명령어>` | 컨테이너에서 명령 실행 |

### Cargo 명령어 (컨테이너 내부)

| 명령어 | 설명 |
|--------|------|
| `cargo new <프로젝트명>` | 새 프로젝트 생성 |
| `cargo build` | 프로젝트 빌드 |
| `cargo run` | 빌드 후 실행 |
| `cargo check` | 빠른 문법 검사 (빌드 없이) |
| `cargo test` | 테스트 실행 |
| `cargo fmt` | 코드 포매팅 |
| `cargo clippy` | 린트 검사 |
| `cargo doc --open` | 문서 생성 및 열기 |

### 자주 쓰는 조합

```bash
# 특정 챕터 디렉토리에서 실행
docker compose exec rust-dev cargo run --manifest-path ch01_hello_rust/Cargo.toml

# 또는 컨테이너 내부에서
cd ch01_hello_rust && cargo run

# 릴리즈 빌드 (최적화)
cargo build --release
cargo run --release
```

---

## 🔍 문제 해결

### 1. Docker가 실행되지 않음
```bash
# Docker 상태 확인
docker info

# Docker Desktop이 실행 중인지 확인
```

### 2. 포트 충돌
```bash
# 다른 컨테이너가 포트를 사용 중일 수 있음
docker ps
docker stop <container_id>
```

### 3. 볼륨 권한 문제
```bash
# 권한 확인
ls -la .

# 필요시 권한 수정
chmod -R 755 .
```

### 4. 컨테이너 재빌드
```bash
# 이미지부터 다시 빌드
docker compose build --no-cache
docker compose up -d
```

### 5. 디스크 정리
```bash
# 사용하지 않는 Docker 리소스 정리
docker system prune -a
```

---

## 🎓 학습 시작하기

환경 설정이 완료되면:

1. `docker compose up -d`로 컨테이너 시작
2. [README.md](./README.md)로 돌아가서 "챕터 1 시작" 요청

---

**작성일**: 2026-01-01
