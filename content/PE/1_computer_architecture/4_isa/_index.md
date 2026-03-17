+++
title = "04. 명령어 세트 아키텍처 (ISA)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "컴퓨터와 사람이 대화할 때 사용하는 '공통의 언어'예요. 사람이 '숙제해!'라고 말하면 컴퓨터가 어떤 부품을 써서 어떻게 일을 해야 하는지 아주 자세하게 적어놓은 백과사전 같은 규칙이랍니다."
+++

# 04. 명령어 세트 아키텍처 (ISA)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 하드웨어가 실행할 수 있는 명령어들의 집합이자, 소프트웨어와 하드웨어 사이의 추상적 계약 계층(Abstract Interface).
> 2. **가치**: 명령어의 포맷, 주소 지정 방식(Addressing Mode), 레지스터 구조를 정의하여 바이너리 수준의 호환성과 최적화 기폭제 제공.
> 3. **융합**: RISC-V와 같은 오픈 ISA를 통한 하드웨어 민주화 및 특정 도메인 전용 명령어(DSA) 확장을 통한 AI 연산 가속.

---

### Ⅰ. 개요 (Context & Background)
ISA는 컴퓨터 구조의 '헌법'이다. 소프트웨어 개발자는 하드웨어 내부의 물리적 전선을 알 필요 없이 ISA만 알면 프로그램을 작성할 수 있고, 하드웨어 설계자는 ISA만 준수하면 내부를 자유롭게 최적화할 수 있다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 구성 요소
- **Instructions**: Arithmetic, Logic, Data Transfer, Branch
- **Registers**: PC(Program Counter), SP(Stack Pointer), GPR
- **Addressing Modes**: Immediate, Direct, Indirect, Indexing
- **Endianness**: Big Endian vs Little Endian

#### 2. ISA 추상화 계층 (ASCII)
```text
    +---------------------------------------+
    |   High Level Language (C, Rust)       |
    +---------------------------------------+
                | Compiler
    +-----------v---------------------------+
    |   ISA (x86, ARM, RISC-V)              |  <-- The Contract
    +-----------+---------------------------+
                | Microarchitecture (Hardware)
    +-----------v-----------+---------------+
    |   Control Logic       |   Datapath    |
    +-----------------------+---------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### RISC vs CISC
| 항목 | RISC (Reduced) | CISC (Complex) |
| :--- | :--- | :--- |
| **명령어 수** | 적음 (단순함) | 많음 (복잡함) |
| **명령어 길이** | 고정 (Fixed) | 가변 (Variable) |
| **메모리 접근** | Load/Store 구조 | 명령어 내부에서 직접 접근 |
| **파이프라이닝** | 매우 용이함 | 어려움 (디코딩 병목) |
| **대표 사례** | ARM, MIPS, RISC-V | Intel x86, AMD64 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 최신 ISA는 **SIMD(Single Instruction Multiple Data)**와 같은 벡터 연산 명령어를 강화하여 멀티미디어 및 AI 처리 효율을 높이고 있다. 기술사는 시스템 설계 시 특정 ISA의 라이선스 비용, 에코시스템 성숙도, 전력 효율을 종합적으로 고려하여 플랫폼을 선택해야 한다.

---

### Ⅴ. 기대효과 및 결론
ISA는 이제 하이브리드 컴퓨팅과 엣지 디바이스로 확장되고 있다. 특히 오픈 소스 기반의 RISC-V는 특정 벤더에 종속되지 않는 하드웨어 설계의 새로운 지평을 열고 있다.
