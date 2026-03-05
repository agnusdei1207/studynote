+++
title = "레지스터 파일 (Register File)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# 레지스터 파일 (Register File)

## 핵심 인사이트 (3줄 요약)
1. 레지스터 파일은 다중 포트를 가진 레지스터 배열로, 동시에 여러 레지스터를 읽고 하나를 쓸 수 있는 CPU의 핵심 저장 장치이다
2. 디코더로 레지스터를 선택하고, MUX로 읽기 데이터를 선택하며, 1클럭 내에 병렬 읽기가 가능한 조합+순차 회로이다
3. 기술사시험에서는 포트 구성, 디코더/MUX 설계, MIPS 레지스터 파일 구조가 핵심이다

## Ⅰ. 개요 (500자 이상)

레지스터 파일(Register File)은 **다중 포트를 가진 레지스터의 배열로 CPU에서 범용 레지스터들을 구현하는 하드웨어 구조**이다. 여러 개의 읽기 포트와 하나 이상의 쓰기 포트를 제공하여, 한 클럭 사이클 내에 여러 레지스터를 동시에 읽고 쓸 수 있다.

```
레지스터 파일 기본 개념:
구조: n개 × m비트 레지스터 배열
포트: r개 읽기 포트, w개 쓰기 포트
입력: 읽기 주소(r개), 쓰기 주소(1개), 쓰기 데이터
출력: 읽기 데이터(r개)

동작:
- 읽기: 조합 회로 (즉시)
- 쓰기: 동기식 (클럭 에지)

특징:
- 동시 다중 읽기
- 1클럭 쓰기
- 멀티포트 설계
- 버스 연결
```

**레지스터 파일의 핵심 특징:**

1. **다중 포트**: 동시 읽기/쓰기 지원
2. **조합+순차**: 읽기는 조합, 쓰기는 순차
3. **스케일링**: 레지스터 수와 비트 수 확장 가능
4. **밸런스**: 면적, 속도, 전력 트레이드오프

```
레지스터 vs 레지스터 파일:
레지스터:
- 1개 저장소
- 1개 입출력
- 단일 포트

레지스터 파일:
- n개 저장소
- n개 입출력
- 다중 포트
- 주소 디코딩
```

레지스터 파일은 MIPS, ARM, x86 등 모든 CPU 아키텍처의 핵심 구성 요소이다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 기본 레지스터 파일 구조

```
2R1W 레지스터 파일 (2개 읽기 포트, 1개 쓰기 포트):

Read Port 1          Read Port 2          Write Port
    │                    │                    │
  A1[4:0]            A2[4:0]             A3[4:0]
    │                    │                    │
    ↓                    ↓                    ↓
[Decoder]           [Decoder]           [Decoder]
    │                    │                    │
    └───┬────────────┬───┴───[Decoder]──┬───┘
        │            │            │       │
       R0           R0           R0      R0
       R1  ┌───────┐R1  ┌───────┐R1  ┌──┴──┐
       R2  │ REG   │R2  │ REG   │R2  │ REG │
       R3  │ FILE  │R3  │ FILE  │R3  │ FILE│
      ...  │       │... │       │... │      │
      R31  └───────┘R31 └───────┘R31 └─────┘
        │            │            │        ↑
        └──[MUX]─ RD1            │   WD3[31:0]
             ↑                  │   Write Enable
             │                  └──[Clock]
           [MUX]
             ↑
           RD2

구성 요소:
- Decoder: 주소 디코딩 (5→32)
- Register: 저장소 (32×32비트)
- MUX: 읽기 데이터 선택 (32→1)
- Control: 쓰기 제어
```

### 읽기 포트 구조

```
단일 읽기 포트:

Addr[4:0] ──[Decoder]── En[31:0]
                  │
    Reg[0] ───────┤
    Reg[1] ───────┤
     ...      ────┼──[32:1 MUX]── Data[31:0]
    Reg[31]──────┘

동작:
1. Addr로 디코더 활성화
2. 해당 레지스터 출력 활성화
3. MUX가 선택된 레지스터 출력

특징:
- 조합 회로 (지연 없음)
- 디코더 + MUX 지연
- t_read = t_decode + t_mux
```

### 쓰기 포트 구조

```
단일 쓰기 포트:

Addr[4:0] ──[Decoder]── WE[31:0]
                  │
    Reg[0] ───────┤
    Reg[1] ───────┼──[WE]──[D FF]
     ...      ────┤
    Reg[31]──────┘
                  ↑
            WD[31:0]

동작:
1. Addr로 디코더 활성화
2. WE[Addr]=1
3. Clk↑에서 WD → Reg[Addr]

특징:
- 순차 회로 (클럭 필요)
- 디코더 + FF 지연
- t_write = t_setup + t_clk_q
```

### 디코더 설계

```
5→32 디코더:

A[4:0]
│
├──[4:16 Decoder]───[Decoder Enable]── En[15:0]
│  ↑                              │
└──[NOT]                          │
 A'                                │
  └─[4:16 Decoder]────────────────┴── En[31:16]

구현:
En[i] = (A[4:0] == i)

게이트 수:
- 5개 NOT
- 32개 5입력 AND (또는 트리 구조)
- 약 160-200 게이트

지연:
t_decode ≈ 2-3 게이트
```

### MUX 설계

```
32:1 MUX (트리 구조):

Level 1: 16× 2:1 MUX
Reg[0] ───┐
Reg[1] ───┴──[MUX]───┐
                    │
Reg[2] ───┐         │
Reg[3] ───┴──[MUX]───┤
                    ├── Level 2: 8× 2:1 MUX
...                  │
                    │
Reg[30]──┐          │
Reg[31]──┴──[MUX]───┘

레벨 수:
- 32:1 → 5레벨 (log₂32)
- 64:1 → 6레벨

지연:
t_mux ≈ 5 게이트 @ 32:1
```

### 포트 확장

```
다중 포트 레지스터 파일:

3R2W 구조:
- 3개 읽기 포트
- 2개 쓰기 포트

구현:
Read Ports:
- 3개 디코더
- 3개 MUX
- 레지스터 3배 생성 (각 포트용)

Write Ports:
- 2개 디코더
- 2개 WE 신호
- 쓰기 충돌 검출

비용:
- 면적: O(n_ports × n_regs)
- 지연: O(log n_regs)
- 전력: O(n_ports × n_regs)
```

### 전원 관리

```
Clock Gating:

Clk ──[AND]── Reg_Clk
       ↑
    Enable

Enable=0: Clk 전파 차단 → 전력 절약

Word Line Enable:

Decoder ─[AND]── WE
            ↑
         Enable

Enable=0: 워드라인 비활성 → 전력 절약

Supply Gating:
유휴 레지스터 전원 차단
```

## Ⅲ. 융합 비교

### 포트 구성 비교

| 구성 | 읽기 | 쓰기 | 복잡도 | 응용 |
|------|------|------|--------|------|
| 1R1W | 1 | 1 | 낮음 | 단순 |
| 2R1W | 2 | 1 | 중간 | MIPS |
| 3R1W | 3 | 1 | 중간 | RISC-V |
| 3R2W | 3 | 2 | 높음 | x86 |
| nRmW | n | m | 매우 높음 | VLIW |

### 읽기/쓰기 방식

| 방식 | 타이밍 | 지연 | 장점 | 단점 |
|------|--------|------|------|------|
| Async Read | 즉시 | 작음 | 빠름 | Glitch |
| Sync Read | Clk | 큼 | 안정 | 느림 |
| Sync Write | Clk↑ | 중간 | 안정 | Clk 필요 |
| Async Write | 즉시 | 작음 | 빠름 | 위험 |

### 구현 방식

| 방식 | 면적 | 지연 | 전력 | 응용 |
|------|------|------|------|------|
| Single-Port | 작음 | 작음 | 낮음 | 임베디드 |
| Multi-Port | 큼 | 중간 | 중간 | 범용 |
| Banked | 중간 | 작음 | 낮음 | 고성능 |
| Distributed | 큼 | 작음 | 낮음 | FPGA |

## Ⅳ. 실무 적용 및 기술사적 판단

### MIPS 레지스터 파일

```
MIPS 32×32 레지스터 파일:

구조:
- 32개 레지스터 ($0~$31)
- 32비트 폭
- 2개 읽기 포트
- 1개 쓰기 포트

인터페이스:
Input:
- rs[4:0]: 첫 번째 읽기 주소
- rt[4:0]: 두 번째 읽기 주소
- rd[4:0]: 쓰기 주소
- wd[31:0]: 쓰기 데이터
- reg_write: 쓰기 가능

Output:
- rd1[31:0]: 첫 번째 읽기 데이터
- rd2[31:0]: 두 번째 읽기 데이터

특징:
- $0은 항상 0 (하드웨어 상시 0)
- 읽기는 조합 회로 (즉시)
- 쓰기는 클럭 상승 에지
```

### RISC-V 레지스터 파일

```
RISC-V 32×32 레지스터 파일:

구조:
- 32개 레지스터 (x0~x31)
- 32비트 폭
- 2개 읽기 포트
- 1개 쓰기 포트

MIPS와 차이:
- x0는 x0으로 주소 지정
- 쓰기 시 x0=0 무시
- 레지스터 명명법 다름

구현:
- 동일한 2R1W 구조
- 디코더/MUX 유사
```

### x86 레지스터 파일

```
x86-64 레지스터 파일:

구조:
- 16개 범용 레지스터 (RAX~R15)
- 64비트 폭
- 다중 포트 (3R2W 이상)

특징:
- Renaming: 레지스터 리네이밍
- Alias: RAX→EAX→AX→AL
- Shadow: 스택 포인터 별도

구현:
- 물리 레지스터 파일 (100+ 레지스터)
- RAT (Register Alias Table)
- ROB (Reorder Buffer)
```

### 파이프라이닝

```
파이프라인과 레지스터 파일:

IF:
  PC → Instruction Memory

ID:
  rs, rt → RegFile → rd1, rd2

EX:
  rd1, rd2 → ALU → Result

MEM:
  Result → Data Memory

WB:
  Result → RegFile[rd] (Write)

위험 (Hazard):
1. 데이터 위험:
   EX에서 결과, ID에서 읽기
   해결: Forwarding

2. 제어 위험:
   분기 명령어
   해결: Branch Prediction

3. 구조 위험:
   동일 포트 액세스
   해결: Multi-port
```

### Forwarding

```
ALU Forwarding:

     ID      EX      MEM     WB
     rs  →   ALU
    (rd1)    (op)

         forward_rd1 ↗
                  ↗
               MEM/WB
                (result)

구현:
MEM stage 결과 → EX stage ALU 입력

MUX:
ALU_in = (Forward) ? MEM_result : rd1

장점:
- 파이프라인 스톨 감소
- 성능 향상
```

### 멀티사이클 쓰기

```
쓰기 지연 해결:

문제:
- WB stage에서 쓰기
- ID stage에서 읽기
- 같은 클럭 → 위험

해결 1: 쓰기 전 반 클럭 지연
Clk ──┬──┬──┬──┬──
      ↑  ↑  ↑  ↑
     ID  EX MEM WB
            ↑ 쓰기 (하강 에지)
          ↑ 읽기 (상승 에지)

해결 2: Forwarding
쓰기 데이터 → 바로 읽기 포트로 전송
```

## Ⅴ. 기대효과 및 결론

레지스터 파일은 CPU의 작업 메모리이다. 다중 포트로 병렬 연산을 지원한다.

## 📌 관련 개념 맵

```
레지스터 파일
├── 구조
│   ├── 레지스터 배열 (n×m비트)
│   ├── 읽기 포트 (r개)
│   ├── 쓰기 포트 (w개)
│   └── 디코더/MUX
├── 동작
│   ├── 읽기 (조합 회로)
│   ├── 쓰기 (순차 회로)
│   └── 포트 확장
├── 설계
│   ├── 포트 구성 (2R1W, 3R2W)
│   ├── 면적/지연/전력
│   └── Clock Gating
└── 응용
    ├── MIPS 2R1W
    ├── RISC-V 2R1W
    ├── x86 Multi-port
    └── Forwarding
```

## 👶 어린이를 위한 3줄 비유 설명

1. 레지스터 파일은 사물함 같아요. 32개의 사물함이 있고, 번호를 불러서 물건을 넣고 꺼낼 수 있어요
2. 읽기 포트는 사물함에서 동시에 여러 개를 꺼낼 수 있는 문이고, 쓰기 포트는 한 번에 하나씩 넣을 수 있는 문이에요
3. CPU는 명령어 실행할 때 레지스터 파일에서 두 개의 숫자를 읽어서(ALU) 계산하고, 그 결과를 다시 레지스터 파일에 저장해요

```python
# 레지스터 파일 시뮬레이션

from typing import List


class RegisterFile:
    """레지스터 파일"""

    def __init__(self, num_regs: int = 32, bits: int = 32):
        """
        레지스터 파일

        Args:
            num_regs: 레지스터 개수
            bits: 비트 수
        """
        self.num_regs = num_regs
        self.bits = bits
        self.regs = [0] * num_regs
        self.regs[0] = 0  # $0은 항상 0

    def read(self, addr: int) -> int:
        """
        레지스터 읽기 (비동기)

        Args:
            addr: 레지스터 주소

        Returns:
            레지스터 값
        """
        if not (0 <= addr < self.num_regs):
            raise ValueError(f"주소 범위 초과: {addr}")
        return self.regs[addr]

    def write(self, addr: int, data: int, we: int):
        """
        레지스터 쓰기

        Args:
            addr: 레지스터 주소
            data: 쓰기 데이터
            we: Write Enable
        """
        if not (0 <= addr < self.num_regs):
            raise ValueError(f"주소 범위 초과: {addr}")

        # $0에는 쓸 수 없음
        if addr == 0:
            return

        if we == 1:
            self.regs[addr] = data & ((1 << self.bits) - 1)

    def read_two(self, rs: int, rt: int) -> tuple:
        """
        두 레지스터 동시 읽기 (2개 읽기 포트)

        Args:
            rs: 첫 번째 레지스터 주소
            rt: 두 번째 레지스터 주소

        Returns:
            (rs 값, rt 값)
        """
        return self.read(rs), self.read(rt)

    def reset(self):
        """모든 레지스터 리셋"""
        self.regs = [0] * self.num_regs

    def __str__(self):
        result = f"Register File ({self.num_regs}x{self.bits}):\n"
        for i in range(0, self.num_regs, 8):
            row = []
            for j in range(8):
                if i + j < self.num_regs:
                    row.append(f"R{i+j:2d}=0x{self.regs[i+j]:02X}")
            result += "  " + ", ".join(row) + "\n"
        return result


class MIPSRegisterFile(RegisterFile):
    """MIPS 스타일 레지스터 파일"""

    def __init__(self):
        super().__init__(num_regs=32, bits=32)

        # MIPS 레지스터 이름
        self.names = [
            "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
            "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
            "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
            "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
        ]

    def read_with_name(self, addr: int) -> tuple:
        """이름과 함께 읽기"""
        value = self.read(addr)
        return self.names[addr], value

    def __str__(self):
        result = f"MIPS Register File (32x32):\n"
        for i in range(0, 32, 4):
            row = []
            for j in range(4):
                reg_num = i + j
                row.append(f"{self.names[reg_num]:6s}=0x{self.regs[reg_num]:08X}")
            result += "  " + ", ".join(row) + "\n"
        return result


class MultiPortRegisterFile:
    """다중 포트 레지스터 파일"""

    def __init__(self, num_regs: int = 32, bits: int = 32,
                 read_ports: int = 2, write_ports: int = 1):
        self.num_regs = num_regs
        self.bits = bits
        self.read_ports = read_ports
        self.write_ports = write_ports
        self.regs = [0] * num_regs
        self.regs[0] = 0  # $0은 항상 0

    def read_multi(self, addrs: List[int]) -> List[int]:
        """다중 읽기"""
        results = []
        for addr in addrs:
            if not (0 <= addr < self.num_regs):
                raise ValueError(f"주소 범위 초과: {addr}")
            results.append(self.regs[addr])
        return results

    def write_multi(self, addrs: List[int], data: List[int], we: List[int]):
        """다중 쓰기"""
        for addr, d, w in zip(addrs, data, we):
            if addr == 0:  # $0는 쓰기 금지
                continue
            if w == 1:
                self.regs[addr] = d & ((1 << self.bits) - 1)


class PipelineRegisterFile:
    """파이프라인용 레지스터 파일 (Forwarding 지원)"""

    def __init__(self):
        self.regs = [0] * 32
        self.ex_result = None  # EX stage 결과
        self.mem_result = None  # MEM stage 결과
        self.ex_rd = -1
        self.mem_rd = -1

    def read_with_forwarding(self, rs: int, rt: int) -> tuple:
        """
        Forwarding을 고려한 읽기

        Args:
            rs: 첫 번째 레지스터
            rt: 두 번째 레지스터

        Returns:
            (rs 값, rt 값)
        """
        # rs 읽기
        if rs == self.ex_rd and self.ex_result is not None:
            rs_val = self.ex_result  # EX에서 forwarding
        elif rs == self.mem_rd and self.mem_result is not None:
            rs_val = self.mem_result  # MEM에서 forwarding
        else:
            rs_val = self.regs[rs]  # 레지스터 파일에서 읽기

        # rt 읽기
        if rt == self.ex_rd and self.ex_result is not None:
            rt_val = self.ex_result
        elif rt == self.mem_rd and self.mem_result is not None:
            rt_val = self.mem_result
        else:
            rt_val = self.regs[rt]

        return rs_val, rt_val

    def set_ex_result(self, rd: int, result: int):
        """EX stage 결과 설정"""
        self.ex_rd = rd
        self.ex_result = result

    def set_mem_result(self, rd: int, result: int):
        """MEM stage 결과 설정"""
        self.mem_rd = rd
        self.mem_result = result

    def write_back(self, rd: int, data: int):
        """WB stage 쓰기"""
        if rd != 0:
            self.regs[rd] = data
        # forwarding 정보 초기화
        if rd == self.mem_rd:
            self.mem_result = None
            self.mem_rd = -1


def demonstration():
    """레지스터 파일 데모"""
    print("=" * 60)
    print("레지스터 파일 (Register File) 데모")
    print("=" * 60)

    # 기본 레지스터 파일
    print("\n[기본 레지스터 파일]")
    rf = RegisterFile(num_regs=8, bits=8)

    # 초기화
    print(rf)

    # 쓰기
    print("쓰기 연산:")
    for i in range(1, 5):
        rf.write(i, i * 0x11, we=1)
        print(f"  R{i} ← 0x{i * 0x11:02X}")

    print(rf)

    # 읽기
    print("\n읽기 연산:")
    rs, rt = rf.read_two(1, 3)
    print(f"  read(R1, R3) = (0x{rs:02X}, 0x{rt:02X})")

    # MIPS 레지스터 파일
    print("\n[MIPS 레지스터 파일]")
    mips_rf = MIPSRegisterFile()

    # 일부 레지스터 초기화
    mips_rf.write(1, 0x11111111, 1)  # $at
    mips_rf.write(2, 0x22222222, 1)  # $v0
    mips_rf.write(4, 0xAAAAAAAA, 1)  # $a0
    mips_rf.write(8, 0x12345678, 1)  # $t0
    mips_rf.write(31, 0xFFFFFFFF, 1)  # $ra

    print(mips_rf)

    # 명령어 시뮬레이션
    print("\n[명령어 시뮬레이션: ADD $t0, $t1, $t2]")
    # $t1 = 0x10, $t2 = 0x20
    mips_rf.write(8, 0x10, 1)  # $t0
    mips_rf.write(9, 0x20, 1)  # $t1
    mips_rf.write(10, 0x30, 1)  # $t2

    # ID stage: 읽기
    rs, rt = mips_rf.read_two(9, 10)  # $t1, $t2
    print(f"  ID: rs=$t1=0x{rs:08X}, rt=$t2=0x{rt:08X}")

    # EX stage: ALU
    result = rs + rt
    print(f"  EX: ALU result = 0x{result:08X}")

    # WB stage: 쓰기
    mips_rf.write(8, result, 1)  # $t0 ← result
    print(f"  WB: $t0 ← 0x{result:08X}")
    print(f"  확인: $t0 = 0x{mips_rf.read(8):08X}")

    # Forwarding
    print("\n[Forwarding 데모]")
    prf = PipelineRegisterFile()

    # 초기 상태
    prf.regs[1] = 0x10  # $at
    prf.regs[2] = 0x20  # $v0

    print(f"초기: $at=0x{prf.regs[1]:02X}, $v0=0x{prf.regs[2]:02X}")

    # 명령어 1: ADD $t0, $at, $v0
    print("\n명령어 1: ADD $t0, $at, $v0")
    rs, rt = prf.read_with_forwarding(1, 2)
    print(f"  ID: rs=0x{rs:02X}, rt=0x{rt:02X}")
    ex_result = rs + rt
    print(f"  EX: result=0x{ex_result:02X}")
    prf.set_ex_result(rd=8, result=ex_result)

    # EX→MEM
    prf.set_mem_result(rd=8, result=ex_result)
    prf.ex_result = None

    # 명령어 2: ADD $t1, $t0, $at (데이터 위험)
    print("\n명령어 2: ADD $t1, $t0, $at (데이터 위험)")
    rs, rt = prf.read_with_forwarding(8, 1)  # $t0는 MEM에서 forwarding
    print(f"  ID: rs=$t0=0x{rs:02X} (MEM에서 forwarding), rt=$at=0x{rt:02X}")
    print(f"  Forwarding: $t0가 아직 레지스터에 안 쓰여졌지만 MEM 결과 사용")

    # WB
    prf.write_back(rd=8, data=ex_result)
    print(f"\n  WB: $t0 ← 0x{prf.regs[8]:02X}")

    # 다중 포트
    print("\n[다중 포트 레지스터 파일 (3R2W)]")
    mp_rf = MultiPortRegisterFile(num_regs=16, bits=8, read_ports=3, write_ports=2)

    # 다중 쓰기
    mp_rf.write_multi([1, 2, 3], [0x11, 0x22, 0x33], [1, 0, 1])
    mp_rf.write_multi([4, 5], [0x44, 0x55], [1, 1])
    print("쓰기 후: R1=0x11, R3=0x33, R4=0x44, R5=0x55")

    # 다중 읽기
    results = mp_rf.read_multi([1, 3, 5])
    print(f"읽기 (R1, R3, R5): {results}")


if __name__ == "__main__":
    demonstration()
```
