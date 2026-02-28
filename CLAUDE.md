# 프로젝트 규칙

## 답변 원칙

### 기본 원칙
1. 항상 최신 데이터와 기존 데이터를 바탕으로 답변하며, 환각 현상(hallucination)을 방지하세요.
2. 모든 답변은 전문가 수준의 품질로 제공해야 합니다.
3. 약어를 사용할 때는 항상 전체 명칭(full form)을 먼저 기술한 뒤 약어를 함께 제공하세요.
   - 예: `Kubernetes (K8s)`, `Representational State Transfer (REST)`
   - 어떠한 경우에도 전체 명칭 없이 약어만 단독으로 사용해서는 안 됩니다.
4. 전문 용어, 개념, 변수명, 신호명 등이 처음 등장할 때 **무엇을 의미하는지 직관적으로 이해할 수 있는 최소한의 설명**을 함께 제공하세요.
   - 독자가 해당 분야를 처음 접하더라도 바로 이해할 수 있는 수준이어야 합니다.
   - 빠지는 부분 없이 전부 제공되어야 합니다. thoroughly
5. 설명이 장황하지 않고 핵심 인사이트가 직관적이게 제공되어야 하고 이해하기 쉬워야 합니다.
5. 전체 문단 흐름이 가독성이 좋아야 합니다.


### 기술사 시험 대비
1. 대한민국의 정보통신기술사와 컴퓨터응용시스템기술사 시험을 준비중입니다.
2. 이 시험의 실제 답안지처럼 작성해야 합니다.
3. 제한시간이 있는 시험이므로 기술사 시험의 심사위원이 심사하고자 하는 핵심 요소를 놓쳐서는 안 됩니다.

### 답변 구조
1. 무조건 길다고 좋은 것이 아니고 짧다고 좋은 것이 아닙니다.
2. 핵심 요소가 있어야 하며, 아래 요소들을 **참고하여 자유롭게 선택·구성**하세요.
   - 모든 항목이 필수는 아닙니다. 주제에 따라 필요한 것만 골라 쓰고, 필요하면 새 항목을 추가해도 됩니다.
   - **개념**: 정의 및 기본 설명
   - **등장 배경**: 왜 필요하게 되었는가 (기존의 문제점, 한계)
   - **구성 요소**: 주요 구성 요소 및 역할
   - **핵심 원리**: 동작 방식 (단계별 흐름, 알고리즘 등)
   - **장단점**: 비교 분석 (표 활용 권장)
   - **다른 것과 비교**: 대안 기술과의 비교 (선택 기준 포함)
   - **기술사적 판단**: 현업 관점 (실무 적용 사례, 선택 이유)
   - **미래 전망**: 발전 방향 및 트렌드
   - **활용 사례**: 실제 서비스/시스템에서의 사용 예시
   - **코드 예시**: 필요한 경우 핵심 코드 스니펫
   - **주의사항 / 흔한 실수**: 놓치기 쉬운 함정이나 안티패턴
   - **관련 개념**: 함께 알아야 할 연관 기술·용어
3. 표나 다이어그램을 적극 활용해 주세요.
4. 추가적으로 `---` 선으로 분리하여 **어린이 버전 설명과 비유**를 들어 학습자가 쉽게 이해할 수 있도록 부록이 추가되어야 합니다.

## 파일 작성 규칙

1. **모든 새 글은 반드시 `content/` 안의 적절한 카테고리 폴더에 작성합니다.** `_posts/` 등 Jekyll 관례 경로에 글을 쓰지 마세요.
2. 파일명은 **소문자와 언더바(`_`)** 사용하세요.
   - 예: `heap_data_structure.md`, `docker_container.md`
3. 모든 파일은 반드시 아래 **Zola TOML front matter**로 시작해야 합니다:
   ```toml
   +++
   title = "제목"
   date = YYYY-MM-DD

   [extra]
   categories = "카테고리명"
   +++
   ```
   - `categories` 값은 아래 폴더 구조의 카테고리 중 하나 (예: `cs_fundamentals-network`, `programming-rust`)
4. 새 카테고리 폴더를 만들 때는 반드시 해당 디렉토리에 `_index.md` 파일도 함께 생성합니다:
   ```toml
   +++
   title = "섹션 제목"
   description = "설명"
   sort_by = "title"
   +++
   ```
5. 파일 본문은 한글로 작성합니다.
6. **[필수] 모든 답변/파일 작성 완료 후 무조건 클립보드에 복사하세요. 절대 까먹지 마세요!**
   - macOS: `cat 파일경로 | pbcopy`
   - 새 파일 작성, 기존 파일 수정, 답변 완료 등 **모든 경우에 항상 pbcopy 실행**
   - 사용자에게 "클립보드에 복사 완료!"라고 안내

## 폴더 구조 (Zola content/ 기반)

글은 **`content/` 안에 카테고리별 폴더**로 저장합니다. 각 폴더에 `_index.md`가 반드시 있어야 합니다.

```
studynote/
└── content/
    ├── _index.md
    ├── cs_fundamentals/
    │   ├── _index.md
    │   ├── algorithm/
    │   │   ├── _index.md
    │   │   └── heap.md          # categories = "cs_fundamentals-algorithm"
    │   ├── data_structure/
    │   ├── operating_system/
    │   ├── network/
    │   ├── computer_architecture/
    │   └── digital_logic/
    ├── programming/
    │   ├── _index.md
    │   ├── rust/
    │   ├── python/
    │   └── javascript/
    ├── database/
    │   ├── _index.md
    │   ├── relational/
    │   └── nosql/
    ├── devops/
    │   ├── _index.md
    │   ├── docker/
    │   ├── kubernetes/
    │   └── cloud/
    └── security/
        ├── _index.md
        ├── cryptography/
        └── web/
```

### categories 값 규칙

`상위카테고리-하위카테고리` 형태로 작성합니다 (하이픈 구분).

| categories 값 | 분류 |
|---|---|
| `cs_fundamentals-algorithm` | 알고리즘 (정렬, 탐색, 복잡도 등) |
| `cs_fundamentals-data_structure` | 자료구조 (힙, 트리, 그래프, 해시 등) |
| `cs_fundamentals-operating_system` | 운영체제 (프로세스, 메모리, 스케줄링 등) |
| `cs_fundamentals-network` | 네트워크 (OSI 7계층, TCP/IP, HTTP 등) |
| `cs_fundamentals-computer_architecture` | 컴퓨터 구조 (CPU, 메모리, 버스 등) |
| `cs_fundamentals-digital_logic` | 디지털 논리회로 (게이트, 플립플롭 등) |
| `programming-rust` | Rust |
| `programming-python` | Python |
| `programming-javascript` | JavaScript |
| `database-relational` | 관계형 DB (SQL, 정규화 등) |
| `database-nosql` | NoSQL (Redis, MongoDB 등) |
| `devops-docker` | Docker |
| `devops-kubernetes` | Kubernetes |
| `devops-cloud` | AWS, GCP, Azure |
| `security-cryptography` | 암호학 |
| `security-web` | 웹 보안 |

## 답변 예시 템플릿

> ⚠️ 아래는 참고용 예시입니다. 모든 섹션이 필수가 아니며, 주제에 맞게 자유롭게 추가·생략·재구성하세요.

```markdown
# [주제명]

## 핵심 인사이트 (3줄 요약)
> 이게 뭔지, 왜 쓰는지, 어떻게 동작하는지를 딱 3줄로

## 1. 개념
[한 문장 정의 + 쉬운 비유]

## 2. 등장 배경
[이전엔 어떤 문제가 있었고, 이게 어떻게 해결했는지]

## 3. 구성 요소
| 구성 요소 | 역할 | 비유 |
|----------|------|------|
| ...      | ...  | ...  |

## 4. 핵심 원리
[핵심 동작 과정을 단계별로]

## 5. 장단점
| 장점 | 단점 |
|-----|------|
| ... | ...  |

## 6. 다른 것과 비교
| 항목 | [이것] | [대안 A] | [대안 B] |
|-----|--------|----------|----------|
| ... | ...    | ...      | ...      |
[선택 기준 한 줄]

## 7. 활용 사례  ← 필요시 포함
[실제 서비스나 시스템에서 어떻게 쓰이는지]

## 8. 코드 예시  ← 필요시 포함
```언어
// 핵심 개념을 담은 최소 코드
```

## 9. 주의사항 / 흔한 실수  ← 필요시 포함
- 놓치기 쉬운 함정
- 안티패턴

## 10. 실무에선? (기술사적 판단)
[현업 관점에서 언제/왜 쓰는지]

## 11. 관련 개념  ← 필요시 포함
[함께 알아야 할 연관 기술·용어 목록]

## 12. 앞으로는? (미래 전망)
[발전 방향 한두 줄]

---

## 어린이를 위한 종합 설명
[전체 내용을 아주 쉬운 비유로 한 번 더 정리]

---
```
