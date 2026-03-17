+++
title = "가상 메모리 (Virtual Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# 가상 메모리 (Virtual Memory)

## 핵심 인사이트 (3줄 요약)
1. 가상 메모리는 논리 주소와 물리 주소를 분리하여, 물리 메모리보다 큰 주소 공간을 제공하고 다중 프로그래밍을 지원한다
2. 기술사시험에서는 Paging, Segmentation, TLB(Translation Lookaside Buffer), Page Fault 처리가 핵심이다
3. MMU(Memory Management Unit)가 가상 주소를 물리 주소로 변환하며, TLB Hit가 성능을 결정한다

## Ⅰ. 개요

가상 메모리는 **프로그램이 사용하는 논리 주소(Logical Address)와 실제 물리 메모리의 물리 주소(Physical Address)를 분리하는 기술**이다. 프로세스마다 독립적인 주소 공간을 제공하고, 물리 메모리보다 큰 메모리를 사용할 있게 한다.

```
가상 메모리 목적:
1. 주소 공간 추상화
2. 물리 메모리 확장
3. 프로세스 보호
4. 메모리 공유

구성:
- Virtual Address: 프로그램이 사용하는 주소
- Physical Address: 실제 메모리 주소
- MMU: 주소 변환 하드웨어
- Page Table: 변환 테이블
```

## Ⅱ. 아키텍처 및 핵심 원리

### Paging

```
페이징 (Paging):

고정 크기 블록(Page) 단위로 메모리 관리

구조:
Virtual Address:
┌─────────┬──────────┬──────────┐
│  VPN    │  Offset  │          │
└─────────┴──────────┴──────────┘

Physical Address:
┌─────────┬──────────┬──────────┐
│  PPN    │  Offset  │          │
└─────────┴──────────┴──────────┘

Page Table Entry (PTE):
┌─────┬──────┬───────┬──────────┬──────────┐
│ PPN │ Valid│ Dirty │ Accessed │ R/W/X    │
└─────┴──────┴───────┴──────────┴──────────┘

Valid: 페이지 존재
Dirty: 수정됨
Accessed: 접근됨
R/W/X: 읽기/쓰기/실행 권한
```

### Segmentation

```
세그먼테이션 (Segmentation):

가변 크기 논리적 단위(Segment)

구조:
Logical Address:
┌─────────┬──────────┐
│ Segment │  Offset  │
└─────────┴──────────┘

Segment Table:
┌─────────┬──────────┬──────────┬──────────┐
│  Base   │  Limit   │  R/W/X   │  Valid   │
└─────────┴──────────┴──────────┴──────────┘

장점:
- 논리적 구조 반영
- 동적 성장

단점:
- External Fragmentation
```

### TLB

```
TLB (Translation Lookaside Buffer):

주소 변환 캐시

구조:
VPN → PPN 매핑 캐시
Fully-Associative 또는 Set-Associative

성능:
TLB Hit: 1-2 cycles
TLB Miss: 10-100 cycles (Page Table Walk)

TLB Miss Handling:
1. Page Table Walk
2. TLB Update
3. Address Translation Retry

Example:
Virtual Address: 0x12345678
VPN: 0x12345
Offset: 0x678

TLB[VPN 검색]:
  Hit → PPN = 0xABCDE
  Physical = 0xABCDE678

  Miss → Page Table Walk
        → PPN = 0xABCDE
        → TLB[VPN] = PPN
```

### Page Fault

```
페이지 폴트 (Page Fault):

요청한 페이지가 메모리에 없음

처리:
1. Exception 발생
2. OS 페이지 핸들러 호출
3. 빈 프레임 찾기
4. 디스크에서 페이지 로드
5. Page Table 업데이트
6. 명령어 재시작

성능:
Page Fault: 수백만 cycles
Disk I/O: 밀리초 단위

Thrashing:
과도한 Page Fault
시스템 성능 급격 저하
Working Set insufficient
```

## Ⅲ. 융합 비교

| 기법 | 단위 | 장점 | 단점 |
|------|------|------|------|
| Paging | 고정 | 단순 | Internal Fragment |
| Segmentation | 가변 | 유연 | External Fragment |
| Paged Seg | 두가지 | 장점만 | 복잡 |

## Ⅳ. 실무 적용

### x86-64 Paging

```
4-Level Page Table:
PML4 → PDP → PDP → PT → Page

48-bit Virtual Address
256 TB Address Space
```

### ARMv8 Paging

```
4-Level Page Table:
TTBR0_EL1 → L0 → L1 → L2 → L3 → Page

48-bit Virtual (49-bit with TTBR1)
```

## Ⅴ. 결론

가상 메모리는 현대 OS의 필수 요소다. TLB와 Page Table 구조가 성능을 결정한다.
