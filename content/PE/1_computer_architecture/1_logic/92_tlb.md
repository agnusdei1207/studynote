+++
title = "TLB (Translation Lookaside Buffer)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# TLB (Translation Lookaside Buffer)

## 핵심 인사이트 (3줄 요약)
1. TLB는 가상 주소를 물리 주소로 변환하는 Page Table Entry를 캐싱하는 하드웨어 캐시다
2. TLB Hit는 1-2 cycles, Miss는 10-100 cycles로 성능 차이가 크므로 Hit Ratio를 높이는 것이 중요하다
3. 기술사시험에서는 TLB Miss 처리, Page Table Walk, TLB Coherence, ASID가 핵심이다

