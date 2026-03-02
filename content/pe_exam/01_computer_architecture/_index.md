+++
title = "1. 컴퓨터 구조"
description = "컴퓨터 구조, CPU, 메모리, 입출력, 디지털 논리 회로"
sort_by = "title"
weight = 1
+++

# 제1과목: 컴퓨터 구조

컴퓨터 시스템의 구성요소와 동작 원리를 다룹니다.

## 핵심 키워드

### CPU / 처리장치
- [CPU 구조](cpu_architecture.md) - ALU, 제어장치, 레지스터
- [명령어 사이클](instruction_cycle.md) - Fetch→Decode→Execute
- [파이프라이닝](instruction_pipeline.md) - 명령어 병렬 처리
- [파이프라인 스톨](stall.md) - Hazard, Stall 해결
- [CISC vs RISC](cisc.md) - 명령어 집합 비교
- [VLIW](vliw.md) - 초장 명령어 구조
- [EISC](eisc.md) - 임베디드 명령어 집합

### 메모리 계층
- [메모리 계층 구조](memory_hierarchy.md) - 캐시~보조기억장치
- [캐시 메모리](cache_memory.md) - 지역성, 히트율, 매핑
- [가상 메모리](virtual_memory.md) - 페이징, 세그멘테이션
- [RAM](ram.md) / [ROM](rom.md) / [플래시 메모리](flash_memory.md)

### 입출력 / 버스
- [DMA](dma.md) - 직접 메모리 접근
- [인터럽트](interrupt.md) - 하드웨어 인터럽트
- [버스](bus.md) - 시스템 버스 구조
- [핸드쉐이킹](handshaking.md) - 동기화 프로토콜
- [디스크 스케줄링](disk_scheduling.md) - SSTF, SCAN, C-SCAN

### 병렬 처리
- [SIMD/MIMD](simd_mimd.md) - 병렬 처리 분류
- [다중 처리기](multiprocessor.md) - UMA/NUMA
- [파이프라인](pipeline.md) - 처리 단계 중첩
- [하이퍼큐브](hypercube.md) - 상호연결망

### 디지털 논리 회로
- [불 대수](boolean_algebra.md) - 논리 연산
- [AND/OR/NOT/NAND/NOR/XOR/XNOR 게이트](and_gate.md)
- [플립플롭](flip_flop.md) - RS/JK/D/T 플립플롭
- [ALU](alu.md) - 산술논리장치

### 마이크로 구조
- [마이크로 명령어](microinstruction.md) - 제어 기억장치
- [주소 지정 방식](addressing_mode.md) - 직접/간접/즉시
- [레지스터](register.md) - PC, IR, MAR, MBR
- [부동 소수점](floating_point.md) - IEEE 754

### 컴퓨터 유형
- [폰 노이만 vs 하버드 구조](von_neumann_harvard.md)
- [양자 컴퓨터](quantum_computer.md)
- [하이브리드 컴퓨터](hybrid_computer.md)
- [ENIAC](eniac.md) - 최초의 전자식 컴퓨터
- [RAID](raid.md) - 디스크 어레이
