+++
title = "산술 논리 장치 (ALU, Arithmetic Logic Unit)"
date = 2025-02-27
+++

# 산술 논리 장치 (ALU, Arithmetic Logic Unit)

## 핵심 인사이트 (3줄 요약)
> CPU의 **연산을 담당**하는 핵심 구성 요소. 산술 연산(+,-,*,/)과 논리 연산(AND,OR,NOT)을 수행한다. 모든 데이터 처리의 핵심이다.

## 1. 개념
ALU(Arithmetic Logic Unit)는 **산술 연산과 논리 연산을 수행**하는 CPU의 핵심 회로다. 두 개의 입력을 받아 연산 결과를 출력한다.

> 비유: "계산기" - 숫자 계산과 논리 판단을 수행

## 2. ALU 구조

```
         ┌─────────────────┐
    A ───┤                 │
         │      ALU        ├─── Result (결과)
    B ───┤                 │
         └────────┬────────┘
                  │
             Opcode (연산 선택)
                  │
         ┌────────┴────────┐
         │ Zero | Carry |  │
         │ Negative | ...  │
         └─────────────────┘
              상태 플래그
```

## 3. ALU 연산 종류

### 산술 연산
| 연산 | 기호 | 설명 |
|------|------|------|
| 덧셈 | ADD | A + B |
| 뺄셈 | SUB | A - B |
| 곱셈 | MUL | A × B |
| 나눗셈 | DIV | A ÷ B |
| 증가 | INC | A + 1 |
| 감소 | DEC | A - 1 |

### 논리 연산
| 연산 | 기호 | 설명 |
|------|------|------|
| AND | AND | A ∧ B |
| OR | OR | A ∨ B |
| NOT | NOT | Ā |
| XOR | XOR | A ⊕ B |
| 시프트 | SHL/SHR | 비트 이동 |

## 4. ALU 내부 구조

```
ALU 내부 (간소화):

    A[31:0] ──┬───[가산기]───┐
              │               │
              ├───[AND/OR]────┼─── Result[31:0]
              │               │
              ├───[시프터]────┤
              │               │
    B[31:0] ──┴───[비교기]────┘

    Opcode ──→ [MUX] ←── 각 연산 결과 중 선택
```

## 5. 상태 플래그

| 플래그 | 이름 | 의미 |
|--------|------|------|
| Z | Zero | 결과가 0 |
| C | Carry | 자리올림 발생 |
| N | Negative | 결과가 음수 |
| V | Overflow | 오버플로우 발생 |

## 6. 가산기 구조

```
전가산기 (Full Adder):

  A ──┐
      ├─[XOR]──┐
  B ──┘        ├──[XOR]── Sum
           ┌──┘
  Cin ─────┘
           │
  A,B,Cin ─┴─[AND/OR]── Cout

32비트 가산기 = 전가산기 32개 연결
```

## 7. ALU 성능

```
ALU 지연 시간:
- 덧셈/뺄셈: 1 클럭
- 곱셈: 3~5 클럭
- 나눗셈: 10~30 클럭

슈퍼스칼라:
- 여러 ALU 병렬 운영
- 정수 ALU + 부동소수점 ALU 분리
```

## 8. 코드 예시

```verilog
// ALU Verilog 구현
module alu(
    input [31:0] a, b,
    input [3:0] opcode,
    output [31:0] result,
    output zero, carry, negative
);
    always @(*) begin
        case(opcode)
            4'b0000: result = a + b;      // ADD
            4'b0001: result = a - b;      // SUB
            4'b0010: result = a & b;      // AND
            4'b0011: result = a | b;      // OR
            4'b0100: result = a ^ b;      // XOR
            4'b0101: result = ~a;         // NOT
            4'b0110: result = a << b;     // SHL
            4'b0111: result = a >> b;     // SHR
            default: result = 0;
        endcase
    end
endmodule
```

## 9. 장단점

| 장점 | 단점 |
|-----|------|
| 범용 연산 | 복잡한 연산은 느림 |
| 높은 성능 | 전력 소모 |

## 10. 실무에선? (기술사적 판단)
- **현대 CPU**: 정수 ALU + FPU + 벡터 ALU
- **GPU**: 수천 개의 단순 ALU
- **AI**: 텐서 연산용 특수 ALU

## 11. 관련 개념
- 전가산기, 반가산기
- 플래그 레지스터
- FPU (Floating Point Unit)

---

## 어린이를 위한 종합 설명

**ALU는 "만능 계산기"야!**

CPU의 두뇌 중에서 계산을 담당해요!

### 할 수 있는 것들

**산술 (수학)**
```
더하기: 5 + 3 = 8
빼기: 10 - 4 = 6
곱하기: 3 × 4 = 12
나누기: 12 ÷ 3 = 4
```

**논리 (판단)**
```
AND: 둘 다 1이면 1
OR: 하나라도 1이면 1
NOT: 반대로!
XOR: 다르면 1
```

**비트 이동**
```
왼쪽으로 한 칸: 0010 → 0100 (2배!)
오른쪽으로 한 칸: 0100 → 0010 (반!)
```

### 상태 표시등
```
💡 Zero: 결과가 0이야!
🔵 Carry: 숫자가 넘쳤어!
🔴 Negative: 음수야!
```

**비밀**: ALU는 게임 점수 계산, 사진 필터, 유튜브 영상 처리... 모든 계산을 해요! 🎮📸
