# Rust 학습용 개발 환경
# Rust 공식 이미지 기반

FROM rust:1.92-bookworm

# 시스템 패키지 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Rust 추가 도구 설치
RUN rustup component add \
    rustfmt \
    clippy \
    rust-analyzer

# cargo-watch 설치 (파일 변경 감지 자동 재실행)
RUN cargo install cargo-watch

# 작업 디렉토리 설정
WORKDIR /workspace

# 기본 쉘을 bash로 설정
SHELL ["/bin/bash", "-c"]

# 컨테이너가 종료되지 않도록 유지
CMD ["tail", "-f", "/dev/null"]
