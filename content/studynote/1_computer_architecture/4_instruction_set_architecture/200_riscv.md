+++
title = "200. RISC-V (RISC-V ISA)"
weight = 200
+++

# 200. RISC-V (RISC-V ISA)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2010년 UC Berkeley 개발, 오픈소스 RISC ISA
> 2. **가치**: 로열티 없음, 모듈형 확장, 학술/산업 표준
> 3. **융합**: IoT, AI 가속기, SiFive, 클라우드, 중국 반도체

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

RISC-V는 **2010년 UC Berkeley에서 개발된 오픈소스 RISC ISA**로, 로열티 없이 누구나 사용할 수 있고 모듈형 확장으로 유연성이 높다. x86/ARM의 폐쇄적 모델에 대한 오픈 대안이다.

### 💡 비유: 오픈소스 레시피

RISC-V는 **오픈소스 레시피**와 같다. x86/ARM은 비밀 레시피(특허)로 돈을 받는다. RISC-V는 레시피를 공개해서 누구나 무료로 요리(CPU)를 만들 수 있다. 기본 재료(기본 ISA)에 원하는 양념(확장)을 추가한다.

### RISC-V 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                RISC-V 구조                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【핵심 특징】                                                       │
│  ─────────────                                                      │
│  1. 오픈소스: 로열티 없음                                            │
│  2. 모듈형: 기본 + 확장 조합                                         │
│  3. 확장성: 32/64/128비트 지원                                       │
│  4. 단순성: 명령어 수 적음                                           │
│  5. 표준화: 국제 표준 (ISA만)                                        │
│                                                                     │
│  【vs 기존 ISA】                                                     │
│  ──────────────────                                                  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  특성          x86         ARM           RISC-V                 │ │
│  │  ───────────  ──────────  ────────────  ─────────────           │ │
│  │  라이선스      Intel 전용   ARM 라이선스   오픈 (무료)            │ │
│  │  비용          높음         중간          없음                   │ │
│  │  커스터마이즈   불가         제한적         자유                  │ │
│  │  확장          Intel 결정   ARM 결정      사용자 결정            │ │
│  │  투명성        폐쇄         폐쇄          완전 공개               │ │
│  │  검증          Intel        ARM           커뮤니티               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【RISC-V 기본 ISA】                                                 │
│  ──────────────────────                                              │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  명칭       비트    설명                                         │ │
│  │  ────────  ─────  ───────────────────────                       │ │
│  │  RV32I     32     기본 정수 (필수)                               │ │
│  │  RV32E     32     임베디드 (레지스터 16개)                        │ │
│  │  RV64I     64     64비트 기본                                    │ │
│  │  RV128I    128    128비트 (미래)                                 │ │
│  │                                                               │ │
│  │  I = Integer (기본 47개 명령어)                                  │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【RISC-V 표준 확장】                                                │
│  ──────────────────────                                              │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  확장    이름            설명                                    │ │
│  │  ─────  ──────────────  ────────────────────────                │ │
│  │  M       Integer MUL/DIV 곱셈/나눗셈                            │ │
│  │  A       Atomic          원자적 연산                            │ │
│  │  F       Single Float    단정밀도 부동소수점                    │ │
│  │  D       Double Float    배정밀도 부동소수점                    │ │
│  │  Q       Quad Float      4배 정밀도                            │ │
│  │  C       Compressed      16비트 압축 명령어                     │ │
│  │  V       Vector          벡터 확장 (SIMD)                       │ │
│  │  B       Bit Manip       비트 조작                              │ │
│  │  P       Packed SIMD     팩 SIMD                                │ │
│  │  H       Hypervisor      하이퍼바이저                           │ │
│  │  N       User Interrupt  사용자 인터럽트                        │ │
│  │                                                               │ │
│  │  예: RV64IMAFDC = RV64 + IMAFD + C                             │ │
│  │  → "RV64GC" (General + Compressed)                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【레지스터】                                                        │
│  ──────────────────                                                  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  레지스터   ABI명    용도            별칭                        │ │
│  │  ────────  ───────  ────────────    ───────                     │ │
│  │  x0        zero     항상 0           -                          │ │
│  │  x1        ra       반환 주소        return address             │ │
│  │  x2        sp       스택 포인터      stack pointer              │ │
│  │  x3        gp       전역 포인터      global pointer             │ │
│  │  x4        tp       스레드 포인터    thread pointer             │ │
│  │  x5-7      t0-2     임시             temporaries                │ │
│  │  x8        s0/fp    저장/프레임      saved/frame pointer        │ │
│  │  x9        s1       저장             saved                      │ │
│  │  x10-17    a0-7     인자/결과        arguments                  │ │
│  │  x18-27    s2-11    저장             saved                      │ │
│  │  x28-31    t3-6     임시             temporaries                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  RISC-V 철학:                                                      │ │
│  │  ──────────────                                                    │ │
│  │  1. 단순성: 명령어 수 최소화                                       │ │
│  │  2. 모듈성: 필요한 확장만 선택                                     │ │
│  │  3. 개방성: 누구나 구현 가능                                       │ │
│  │  4. 안정성: 기본 ISA 변경 없음                                     │ │
│  │  5. 전문성: 학계 + 산업 협업                                       │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. RISC-V 명령어 집합

### 명령어 상세

```
┌─────────────────────────────────────────────────────────────────────┐
│                RISC-V 명령어 집합                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【R-type (레지스터-레지스터)】                                       │
│  ────────────────────────────────                                   │
│  add rd, rs1, rs2      ; rd = rs1 + rs2                             │
│  sub rd, rs1, rs2      ; rd = rs1 - rs2                             │
│  and rd, rs1, rs2      ; rd = rs1 & rs2                             │
│  or rd, rs1, rs2       ; rd = rs1 | rs2                             │
│  xor rd, rs1, rs2      ; rd = rs1 ^ rs2                             │
│  sll rd, rs1, rs2      ; rd = rs1 << rs2                            │
│  srl rd, rs1, rs2      ; rd = rs1 >> rs2 (논리)                     │
│  sra rd, rs1, rs2      ; rd = rs1 >> rs2 (산술)                     │
│  slt rd, rs1, rs2      ; rd = (rs1 < rs2) ? 1 : 0                   │
│                                                                     │
│  【I-type (즉시값)】                                                 │
│  ──────────────────                                                  │
│  addi rd, rs1, imm     ; rd = rs1 + imm                             │
│  andi rd, rs1, imm     ; rd = rs1 & imm                             │
│  ori rd, rs1, imm      ; rd = rs1 | imm                             │
│  xori rd, rs1, imm     ; rd = rs1 ^ imm                             │
│  slti rd, rs1, imm     ; rd = (rs1 < imm) ? 1 : 0                   │
│  slli rd, rs1, shamt   ; rd = rs1 << shamt                          │
│  srli rd, rs1, shamt   ; rd = rs1 >> shamt (논리)                   │
│  srai rd, rs1, shamt   ; rd = rs1 >> shamt (산술)                   │
│                                                                     │
│  【Load/Store】                                                      │
│  ──────────────────                                                  │
│  lw rd, offset(rs1)    ; rd = Mem[rs1 + offset]                     │
│  lh rd, offset(rs1)    ; halfword (부호 확장)                        │
│  lhu rd, offset(rs1)   ; halfword (0 확장)                          │
│  lb rd, offset(rs1)    ; byte (부호 확장)                           │
│  lbu rd, offset(rs1)   ; byte (0 확장)                              │
│  sw rs2, offset(rs1)   ; Mem[rs1 + offset] = rs2                    │
│  sh rs2, offset(rs1)   ; halfword                                   │
│  sb rs2, offset(rs1)   ; byte                                       │
│  ld rd, offset(rs1)    ; double (RV64)                              │
│  sd rs2, offset(rs1)   ; double (RV64)                              │
│                                                                     │
│  【분기】                                                            │
│  ──────────────────                                                  │
│  beq rs1, rs2, label   ; if (rs1 == rs2) goto label                 │
│  bne rs1, rs2, label   ; if (rs1 != rs2) goto label                 │
│  blt rs1, rs2, label   ; if (rs1 < rs2) goto label (부호)           │
│  bge rs1, rs2, label   ; if (rs1 >= rs2) goto label                 │
│  bltu rs1, rs2, label  ; if (rs1 < rs2) goto label (무부호)         │
│  bgeu rs1, rs2, label  ; if (rs1 >= rs2) goto label                 │
│  jal rd, label         ; rd = PC+4; goto label                      │
│  jalr rd, rs1, offset  ; rd = PC+4; PC = rs1 + offset               │
│                                                                     │
│  【상위 즉시값 (U-type)】                                             │
│  ──────────────────────────                                         │
│  lui rd, imm           ; rd = imm << 12                             │
│  auipc rd, imm         ; rd = PC + (imm << 12)                      │
│                                                                     │
│  【M 확장 (곱셈/나눗셈)】                                             │
│  ──────────────────────────                                         │
│  mul rd, rs1, rs2      ; rd = (rs1 * rs2)[31:0]                     │
│  mulh rd, rs1, rs2     ; rd = (rs1 * rs2)[63:32] (부호)             │
│  mulhu rd, rs1, rs2    ; rd = (rs1 * rs2)[63:32] (무부호)           │
│  div rd, rs1, rs2      ; rd = rs1 / rs2 (부호)                      │
│  divu rd, rs1, rs2     ; rd = rs1 / rs2 (무부호)                    │
│  rem rd, rs1, rs2      ; rd = rs1 % rs2 (부호)                      │
│  remu rd, rs1, rs2     ; rd = rs1 % rs2 (무부호)                    │
│                                                                     │
│  【A 확장 (원자적 연산)】                                             │
│  ──────────────────────────                                         │
│  lr.w rd, (rs1)        ; 예약 로드                                   │
│  sc.w rd, rs2, (rs1)   ; 조건부 스토어                               │
│  amoadd.w rd, rs2, (rs1) ; 원자적 덧셈                              │
│  amoswap.w rd, rs2, (rs1) ; 원자적 교환                             │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  RISC-V 명령어 형식 (32비트):                                       │ │
│  │  ────────────────────────────                                      │ │
│  │  R-type: [funct7][rs2][rs1][funct3][rd][opcode]                  │ │
│  │  I-type: [imm12   ][rs1][funct3][rd][opcode]                     │ │
│  │  S-type: [imm7][rs2][rs1][funct3][imm5][opcode]                  │ │
│  │  B-type: [imm7][rs2][rs1][funct3][imm5][opcode]                  │ │
│  │  U-type: [imm20                  ][rd  ][opcode]                 │ │
│  │  J-type: [imm20                  ][rd  ][opcode]                 │ │
│  │                                                               │ │
│  │  → 규칙적인 인코딩으로 디코딩 단순                                  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. RISC-V × 타 과목 융합

### 과목 융합 분석

```
┌─────────────────────────────────────────────────────────────────────┐
│                RISC-V × 타 과목 융합                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【컴파일러】                                                        │
│  • GCC, Clang/LLVM 공식 지원                                        │
│  • Rust, Go 지원                                                    │
│  • 자동 벡터화 (V 확장)                                              │
│  • 최적화 활발                                                       │
│                                                                     │
│  【운영체제】                                                        │
│  • Linux: 공식 지원                                                  │
│  • FreeBSD: 포트 완료                                               │
│  • RTOS: FreeRTOS, Zephyr                                           │
│  • seL4: 형식 검증 커널                                              │
│                                                                     │
│  【보안】                                                            │
│  • PMP: Physical Memory Protection                                  │
│  • ePMP: Enhanced PMP                                               │
│  • I-Ext: 권한 레벨 (M/S/U)                                         │
│  • TEE: TrustZone 유사                                              │
│                                                                     │
│  【생태계】                                                          │
│  • SiFive: 상용 RISC-V IP                                           │
│  • Western Digital: SSD 컨트롤러                                    │
│  • NVIDIA: GPU 컨트롤러                                             │
│  • Alibaba: Xuantie 코어                                            │
│  • ESP32-C3: RISC-V WiFi 칩                                         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  RISC-V 적용 분야:                                                 │ │
│  │  ──────────────────                                                │ │
│  │  1. IoT/임베디드: 저비용, 저전력                                   │ │
│  │  2. SSD 컨트롤러: WD, Seagate                                      │ │
│  │  3. AI 가속기: NPU 제어                                            │ │
│  │  4. 클라우드: Alibaba, Huawei                                      │ │
│  │  5. 슈퍼컴퓨터: EU RISC-V 클러스터                                  │ │
│  │  6. 교육: UC Berkeley, MIT                                         │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용

### RISC-V 분석

```
┌─────────────────────────────────────────────────────────────────────┐
│                RISC-V 분석                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【팩토리얼 함수 (RISC-V)】                                          │
│  ──────────────────────────                                         │
│  # int factorial(int n)                                             │
│  factorial:                                                         │
│      addi sp, sp, -16       # 스택 할당                              │
│      sw ra, 12(sp)          # 반환 주소 저장                         │
│      sw s0, 8(sp)           # s0 저장                                │
│      addi s0, sp, 16        # 프레임 설정                            │
│      sw a0, -12(s0)         # n 저장                                 │
│      lw a0, -12(s0)         # n 로드                                 │
│      addi t0, zero, 1       # t0 = 1                                 │
│      blt a0, t0, .L2        # if (n < 1) goto .L2                   │
│      addi a0, a0, -1        # n - 1                                  │
│      call factorial         # 재귀 호출                              │
│      lw t0, -12(s0)         # n 로드                                 │
│      mul a0, t0, a0         # n * factorial(n-1)                     │
│      j .L3                                                          │
│  .L2:                                                               │
│      addi a0, zero, 1       # return 1                              │
│  .L3:                                                               │
│      lw ra, 12(sp)          # 반환 주소 복원                         │
│      lw s0, 8(sp)           # s0 복원                                │
│      addi sp, sp, 16        # 스택 복원                              │
│      ret                                                            │
│                                                                     │
│  【QEMU RISC-V 실행】                                                │
│  ──────────────────────                                              │
│  $ riscv64-linux-gnu-gcc -o prog prog.c                             │
│  $ qemu-riscv64 ./prog                                              │
│                                                                     │
│  $ qemu-system-riscv64 -M virt -nographic \                         │
│      -kernel vmlinux                                                │
│                                                                     │
│  【GDB 디버깅】                                                      │
│  ──────────────────                                                  │
│  $ riscv64-linux-gnu-gdb ./prog                                     │
│  (gdb) target remote localhost:1234                                 │
│  (gdb) info registers                                               │
│  (gdb) p/x $a0                                                      │
│  (gdb) x/10i $pc                                                    │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  RISC-V 구현체:                                                    │ │
│  │  ──────────────                                                    │ │
│  │  • Rocket Chip (Chisel): UC Berkeley                              │ │
│  │  • BOOM (Out-of-Order): UC Berkeley                               │ │
│  │  • RI5CY (PULPino): ETH Zurich                                    │ │
│  │  • SiFive E/U 시리즈: 상용                                        │ │
│  │  • Xuantie (Alibaba): 64비트 고성능                               │ │
│  │  • OpenC910 (T-Head): 오픈소스                                    │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 핵심 요약

```
• RISC-V: 2010년 UC Berkeley 개발 오픈소스 RISC ISA
• 특징: 로열티 없음, 모듈형, 확장성
• 기본: RV32I/RV64I (47개 명령어)
• 확장: M(곱셈), A(원자), F/D(부동소수점), C(압축), V(벡터)
• 레지스터: x0-x31 (32개)
• 활용: IoT, SSD, AI, 클라우드, 교육
• 미래: 중국 반도체 자립, 오픈 하드웨어
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [RISC](./195_risc.md) → RISC 철학
- [Load/Store 아키텍처](./197_load_store.md) → 메모리 접근
- [ARM 아키텍처](./199_arm_architecture.md) → 경쟁자 (라이선스)
- [ISA 확장](./202_isa_extension.md) → 모듈형 확장
- [MIPS](./201_mips.md) → 유사 RISC

### 👶 어린이를 위한 3줄 비유 설명

**개념**: RISC-V는 "무료 공개 레시피"예요!

**원리**: 누구나 무료로 CPU를 만들 수 있고, 원하는 기능만 골라서 추가해요!

**효과**: 특허비 없이 내 마음대로 CPU를 만들 수 있어요!
