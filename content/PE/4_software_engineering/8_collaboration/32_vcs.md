+++
title = "32. 버전 관리 시스템 (Version Control System)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["VCS", "Git", "DVCS", "Branching", "Merge", "CI/CD"]
draft = false
+++

# 버전 관리 시스템 (Version Control System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VCS는 **"파일 **변경 **이력**을 **관리**하는 **시스템"**으로, **Commit**(저장점), **Branch**(분기), **Merge**(병합) **기능**을 **제공**하며 **SVN**(중앙 집중)과 **Git**(분산)으로 **구분**된다.
> 2. **Git**: **Working Directory** → **Staging Area** → **Repository** **3계층**으로 **구성**되며 **HEAD**(현재 브랜치), **Blob**(파일 내용), **Tree**(디렉토리), **Commit**(저장점) **객체**로 **저장**하고 **SHA-1** **해시**로 **식별**한다.
> 3. **Workflow**: **Feature Branch**(기능 분기), **Gitflow**(출시 관리), **Trunk-Based**(단일 트렁크)로 **작업**하며 **Pull Request**(또는 Merge Request)로 **Code Review**를 **거쳐 **병합**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
VCS는 **"소스 코드 변경 관리 도구"**이다.

**VCS 종류**:
- **Local**: 단일 시스템 (RCS)
- **Centralized**: 중앙 서버 (SVN, CVS)
- **Distributed**: 분산 저장 (Git, Mercurial)

### 💡 비유
VCS는 **"문서 수정 **이력 ****과 같다.
- **원본**: Repository
- **수정본**: Working Directory
- **저장**: Commit
- **분기**: Branch

---

## Ⅱ. 아키텍처 및 핵심 원리

### Git 3계층 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Git Three-Stage Architecture                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Working Directory                    Staging Area                   Repository          │  │
    │  (Work Tree)                         (Index)                       (.git)                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  ┌───────────────────────────────┐        ┌──────────────────────────────────────────┐  │  │  │
    │  │  │ file1.txt (modified)          │        │ Staged Changes                         │  │  │  │
    │  │  │ file2.txt (staged)            │──┐     │ • file2.txt                            │  │  │  │
    │  │  │ file3.txt (untracked)         │  │     └──────────────────────────────────────────┘  │  │  │
    │  │  └───────────────────────────────┘  │                                                  │  │  │
    │  │                                     │       ┌──────────────────────────────────────────┐  │  │  │
    │  │  git add file2.txt ─────────────────┘       │ Commits (History)                       │  │  │  │
    │  │                                             │ ┌────────────────────────────────────────┐  │  │  │  │
    │  │  git commit -m "msg" ───────────────────→   │ │ c1a2b3d: Initial commit (HEAD)       │  │  │  │  │
    │  │                                             │ │ a4b5c6d: Add feature                │  │  │  │  │
    │  │                                             │ │ d7e8f9a: Fix bug                    │  │  │  │  │
    │  │                                             │ └────────────────────────────────────────┘  │  │  │  │
    │  │                                             └──────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Git 객체 모델

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Git Object Model                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Commit Object                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  type: commit                                                                        │  │  │
    │  │  tree: 1a2b3c4d5e6f...  (Root Tree)                                                 │  │  │
    │  │  parent: 9z8y7x6w...   (Previous Commit)                                            │  │  │
    │  │  author: John <john@example.com> 2026-03-06 10:00:00                                 │  │  │
    │  │  committer: John <john@example.com> 2026-03-06 10:00:00                              │  │  │
    │  │  message: "Add new feature"                                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │           │                                                                                 │  │
    │           ▼                                                                                 │  │
    │  Tree Object (Directory)                                                                  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  type: tree                                                                           │  │  │
    │  │  100644 blob a1b2c3d4    file1.txt                                                   │  │  │
    │  │  100644 blob e5f6g7h8    file2.txt                                                   │  │  │
    │  │  040000 tree 9i8j7k6l    subdir/                                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │           │                                                                                 │  │
    │           ▼                                                                                 │  │
    │  Blob Object (File Content)                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  type: blob                                                                           │  │  │
    │  │  size: 1024                                                                           │  │  │
    │  │  content: "Hello, World!\n"                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → 모든 객체는 SHA-1 해시로 식별                                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### VCS 비교

| 구분 | SVN (Centralized) | Git (Distributed) |
|------|-------------------|-------------------|
| **저장소** | 중앙 서버 | 로컬 + 원격 |
| **속도** | 느림 (네트워크) | 빠름 (로컬) |
| **브랜치** | 어려움 | 쉬움 |
| **오프라인** | 불가 | 가능 |

### 브랜치 전략

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Gitflow Branching Strategy                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  master (production)                                                                    │  │
    │  ──────────────────────────────────────────────────────────────────────────────────────│  │
    │       │                                                                                 │  │
    │       │  v1.0          v2.0                                                             │  │
    │       ●───────────────●                                                                 │  │
    │       │               │                                                                 │  │
    │       │               │ develop                                                        │  │
    │       │               └───────────────────────────────────────────────────────────────│  │
    │       │                       ●─────────●─────────●                                    │  │
    │       │                       │         │         │                                    │  │
    │       │               feature/login  feature/pay  feature/ui                           │  │
    │       │                       ●         ●         ●                                    │  │
    │       │                       │         │         │                                    │  │
    │       │                       └─────────┴─────────┴──→ develop (Merge Request)         │  │
    │       │                                                                                 │  │
    │       │               hotfix/critical-bug                                               │  │
    │       └───────────────────────●                                                         │  │
    │                               │                                                         │  │
    │                               └──→ master + develop                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Merge vs Rebase

| 구분 | Merge | Rebase |
|------|-------|--------|
| **History** | 분기 유지 | 선형 |
| **Conflict** | 1회 | 다수 |
| **Safety** | 안전 | 위험(공유 브랜치) |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### Git 명령어

```bash
# 기본 설정
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 저장소 초기화
git init
git clone <url>

# 스테이징 및 커밋
git add .
git commit -m "message"
git commit --amend  # 마지막 커밋 수정

# 브랜치
git branch feature/new
git checkout -b feature/new
git switch -c feature/new

# 병합
git merge feature/new
git rebase main

# 리모트
git remote add origin <url>
git push origin main
git pull --rebase

# 충돌 해결
git status
git merge tool
git add <resolved>
git commit
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Feature Branch Workflow
**상황**: 팀 개발
**판단**:

```bash
# 1. 메인 브랜치 최신화
git checkout main
git pull origin main

# 2. 기능 브랜치 생성
git checkout -b feature/user-auth

# 3. 개발 및 커밋
git add .
git commit -m "feat: add user authentication"

# 4. 리모트 푸시
git push -u origin feature/user-auth

# 5. Pull Request 생성 (GitHub/GitLab)

# 6. Code Review 후 병합
# (via UI: Squash and Merge)

# 7. 브랜치 정리
git branch -d feature/user-auth
```

---

## Ⅴ. 기대효과 및 결론

### VCS 기대 효과

| 효과 | 없음 | VCS |
|------|------|-----|
| **이력 관리** | 불가 | 전체 추적 |
| **협업** | 파일 전송 | 병합/충돌 해결 |
| **롤백** | 백업 필요 | 1초 커밋 이동 |

### 모범 사례

1. **Commit**: Atomic, 논리적 단위
2. **Message**: Conventional Commits (`feat:`, `fix:`, `docs:`)
3. **Branch**: Short-lived
4. **PR**: Code Review 필수

### 미래 전망

1. **AI Merge**: 자동 충돌 해결
2. **Cryptographic VCS**: 서명 불변성
3. **Graph-based**: 정책 자동화

### ※ 참고 표준/가이드
- **Git**: git-scm.com
- **GitHub Flow**: guides.github.com
- **Conventional Commits**: conventionalcommits.org

---

## 📌 관련 개념 맵

- [CI/CD](./13_devops_sre/1_pipeline.md) - 파이프라인
- [협업 도구](./7_tools/28_ide.md) - Git 통합
- [이슈 트래커](./7_tools/29_project_management.md) - 연동
